"""Boundary tests: reading evidence must never grant approval or modify history."""
import hashlib
import json
from pathlib import Path
import sqlite3
import tempfile
import threading
import unittest
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from http.server import ThreadingHTTPServer
import dashboard


class DashboardTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.home = self.root / 'artifacts/runs/example'
        self.home.mkdir(parents=True)
        (self.home / 'run.json').write_text('{"run_id":"example"}')
        self.candidate = self.home / 'artifacts/failure-demo/fault'
        self.candidate.mkdir(parents=True)
        patch = b'example patch'
        (self.candidate / 'candidate.patch').write_bytes(patch)
        (self.candidate / 'manifest.json').write_text(json.dumps({'candidate_id': 'fault', 'patch_sha256': hashlib.sha256(patch).hexdigest()}))

    def tearDown(self):
        self.tmp.cleanup()

    def hashes(self):
        return {p.relative_to(self.root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in self.root.rglob('*') if p.is_file()}

    def test_missing_ledger_not_created(self):
        before = self.hashes()
        result = dashboard.snapshot(self.root, 'example')
        self.assertEqual(result['candidates'][0]['operations'], [])
        self.assertEqual(before, self.hashes())

    def test_modes_and_ledger_remain_unchanged(self):
        with sqlite3.connect(self.candidate / 'ledger.sqlite') as db:
            db.executescript('CREATE TABLE decisions(id,mode); CREATE TABLE operations(id,approval,state,result);')
            db.execute("INSERT INTO decisions VALUES('decision','simulated')")
            db.execute("INSERT INTO operations VALUES('op','decision','VERIFIED','{}')")
        db.close()
        before = self.hashes()
        result = dashboard.snapshot(self.root, 'example')['candidates'][0]
        self.assertTrue(result['simulated'])
        self.assertEqual(result['operations'][0]['mode'], 'simulated')
        self.assertEqual(before, self.hashes())

    def test_invalid_run_and_hash_mismatch(self):
        for identity in ['../example', '/example', 'missing', 'a\\b']:
            with self.assertRaises(ValueError): dashboard.snapshot(self.root, identity)
        (self.candidate / 'candidate.patch').write_text('changed')
        self.assertFalse(dashboard.snapshot(self.root, 'example')['candidates'][0]['patch_matches'])

    def test_incomplete_evidence_reported(self):
        (self.candidate / 'manifest.json').write_text('{')
        result = dashboard.snapshot(self.root, 'example')
        self.assertTrue(result['warnings'])
        self.assertFalse(result['candidates'])

    def test_http_has_no_file_access_or_mutations(self):
        server = ThreadingHTTPServer(('127.0.0.1', 0), dashboard.handler(self.root))
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        url = f'http://127.0.0.1:{server.server_port}'
        before = self.hashes()
        try:
            with urlopen(url + '/api/run?id=example') as r:
                self.assertEqual(r.status, 200)
            with urlopen(url + '/api/scope') as r:
                self.assertEqual(json.load(r)['candidates'], [])
            for path, method, host in [('/.env','GET',None), ('/api/run?id=example','POST',None), ('/api/runs','GET','foreign.example')]:
                request = Request(url + path, method=method, headers={'Host': host} if host else {})
                with self.assertRaises(HTTPError) as caught: urlopen(request)
                self.assertIn(caught.exception.code, [403,404,501])
            self.assertEqual(before, self.hashes())
        finally:
            server.shutdown(); server.server_close(); thread.join()

    def test_additional_scope_reads_current_ledger_without_private_answers(self):
        directory = self.root / 'artifacts/hardening/example/candidate'
        directory.mkdir(parents=True)
        patch = b'example change'
        (directory / 'candidate.patch').write_bytes(patch)
        (directory / 'manifest.json').write_text(json.dumps({'kind':'bounded_repository_repair',
            'candidate_id':'new', 'mode':'interactive', 'patch_sha256':hashlib.sha256(patch).hexdigest()}))
        (directory / 'bundle.json').write_text('{"acceptance":"PRIVATE_ANSWER"}')
        before = self.hashes()
        result = dashboard.scope_snapshot(self.root)
        self.assertEqual(result['candidates'][0]['operations'], [])
        self.assertNotIn('PRIVATE_ANSWER', json.dumps(result))
        self.assertEqual(before, self.hashes())
        with sqlite3.connect(directory / 'ledger.sqlite') as db:
            db.executescript('CREATE TABLE decisions(id,mode); CREATE TABLE operations(id,approval,state,result);')
            db.execute("INSERT INTO decisions VALUES('human','interactive')")
            db.execute("INSERT INTO operations VALUES('op','human','VERIFIED','{}')")
        db.close()
        before = self.hashes()
        updated = dashboard.scope_snapshot(self.root)['candidates'][0]
        self.assertFalse(updated['simulated'])
        self.assertEqual(updated['operations'][0]['state'], 'VERIFIED')
        self.assertEqual(updated['operations'][0]['mode'], 'interactive')
        self.assertEqual(before, self.hashes())


if __name__ == '__main__':
    unittest.main()
