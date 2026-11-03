"""Namespace isolation and frozen-metric contracts, without real approvals."""
import hashlib
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

import review_ledger as cli
from evaluation.run import score, summarize


class RunIsolation(unittest.TestCase):
    def setUp(self):
        (cli.PROJECT / 'artifacts/tests').mkdir(parents=True, exist_ok=True)

    def test_reject_path_escape_and_accept_named_run(self):
        for value in ('../old', 'C:\\old', '.', '', 'a/b', 'a b'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                cli.run_home(value)
        self.assertEqual(cli.run_home('thursday-1').parent, cli.PROJECT / 'artifacts/runs')

    def test_status_does_not_create_ledger_or_mutate_candidate(self):
        with tempfile.TemporaryDirectory(dir=cli.PROJECT / 'artifacts/tests') as name:
            home = Path(name)
            (home / 'run.json').write_text('{"run_id":"test"}')
            candidate = home / 'artifacts/first-patch/candidate-one'
            candidate.mkdir(parents=True)
            (candidate / 'candidate.patch').write_bytes(b'test patch')
            (candidate / 'manifest.json').write_text(json.dumps(dict(candidate_id='one',
                patch_sha256=hashlib.sha256(b'test patch').hexdigest(), plan_version=1)))
            before = {p.relative_to(home): p.read_bytes() for p in home.rglob('*') if p.is_file()}
            result = cli.status(home)
            self.assertTrue(result['candidates'][0]['patch_hash_matches'])
            self.assertEqual(before, {p.relative_to(home): p.read_bytes() for p in home.rglob('*') if p.is_file()})
            (candidate / 'candidate.patch').write_bytes(b'changed')
            self.assertFalse(cli.status(home)['candidates'][0]['patch_hash_matches'])

    def test_manifest_binds_candidate_within_run(self):
        import runtime_paths
        with tempfile.TemporaryDirectory(dir=cli.PROJECT / 'artifacts/tests') as name:
            home = Path(name)
            (home / 'run.json').write_text('{"first_candidate":"../history"}')
            with patch.object(runtime_paths, 'ROOT', home):
                with self.assertRaises(ValueError):
                    runtime_paths.first_candidate()

    def test_duplicate_finding_cannot_inflate_true_positives_and_failure_counts_fn(self):
        case = {'source': 'def lookup(x):\n    return x\n',
                'labels': [{'category': 'security', 'symbol': 'lookup'}]}
        finding = {'category': 'security', 'line': 2}
        counts = score(case, {'reviews': {'security': {'findings': [finding, finding]}}})
        self.assertEqual(counts['security'], {'tp': 1, 'fp': 1, 'fn': 0})
        self.assertEqual(score(case, {})['security']['fn'], 1)

    def test_empty_metric_denominator_is_not_perfect_score(self):
        summary = summarize([], [])
        self.assertIsNone(summary['held_out']['macro_precision'])
        self.assertIsNone(summary['held_out']['macro_recall'])

    def test_container_marker_survives_stream_interleaving_but_not_spoofing(self):
        import approval_executor as ae
        payload = b'LEDGER_RESULT:{"tests":7,"failures":0,"errors":0,"skipped":0}'
        self.assertEqual(ae.container_counts(b'test_last ... '+payload+b'ok\n')['tests'], 7)
        self.assertIsNone(ae.container_counts(payload+b'\n'+payload))
        self.assertIsNone(ae.container_counts(b'LEDGER_RESULT:{"tests":true}'))


if __name__ == '__main__':
    unittest.main()
