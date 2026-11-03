import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import approval_executor as ae
from repository_intake import freeze
from repository_repair import (RepairPlan, RepairProposal, Step, Change, prepare, validate, simulate,
                               validate_plan, execute, freshness)
from pr_intake import parse_url, ingest


class RepositoryRepairTests(unittest.TestCase):
    def inputs(self):
        files = {'a.py': {'role': 'source', 'content': 'def a(x):\n    return x-1\n'},
                 'b.py': {'role': 'source', 'content': 'def b(x):\n    return x-1\n'}}
        plan = RepairPlan(rationale='fix both', steps=[Step(id='fix', goal='increment', paths=list(files),
                          depends_on=['baseline'], contract_ids=['increment'])])
        proposal = RepairProposal(rationale='increment', changes=[Change(path=p, content=f['content'].replace('-1', '+1')) for p,f in files.items()])
        return files, plan, proposal

    def candidate(self, path):
        files, plan, proposal = self.inputs()
        return prepare(path, files, {'increment': 'Increment by one'}, {}, plan, 'fix', proposal,
                       {'status': 'passed'}, simulated=True)

    def test_multiple_files_verified_original_unchanged_and_no_replay(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'candidate'
            self.candidate(path)
            original = (path/'bundle.json').read_bytes()
            with patch('repository_repair.run_tests', return_value={'status': 'passed', 'tests': 2}) as run:
                result = simulate(path)
                self.assertEqual(result['state'], 'VERIFIED')
                with self.assertRaises(ValueError): simulate(path)
                self.assertEqual(run.call_count, 1)
            self.assertEqual((path/'bundle.json').read_bytes(), original)
            self.assertIn('x+1', json.loads((path/'verified-export.json').read_text())['b.py']['content'])

    def test_failed_candidate_quarantined(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'candidate'; self.candidate(path)
            with patch('repository_repair.run_tests', return_value={'status': 'failed'}):
                self.assertEqual(simulate(path)['state'], 'FAILED')
            self.assertTrue((path/'quarantined-export.json').exists())
            self.assertFalse((path/'verified-export.json').exists())

    def test_tampered_bundle_patch_and_wrong_mode_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            for mode in ['bundle', 'patch', 'approval']:
                path = Path(tmp)/mode; manifest = self.candidate(path)
                if mode == 'bundle':
                    value = json.loads((path/'bundle.json').read_text()); value['contracts'] = {}
                    (path/'bundle.json').write_text(json.dumps(value))
                elif mode == 'patch': (path/'candidate.patch').write_text('changed')
                else:
                    ledger = ae.Ledger(path/'ledger.sqlite')
                    try:
                        grant = ledger.decision(manifest, 'person', 'approve')
                        with self.assertRaises(ValueError): execute(path, manifest, ledger, grant, 'person', simulated=True)
                    finally: ledger.db.close()
                    continue
                with self.assertRaises(ValueError): validate(path)

    def test_dependencies_and_test_changes_rejected(self):
        files, plan, proposal = self.inputs()
        plan.steps[0].depends_on = ['future']
        with self.assertRaises(ValueError): validate_plan(plan, files, {'increment': 'Increment'})
        plan.steps[0].depends_on = ['baseline']; files['a.py']['role'] = 'test'
        with self.assertRaises(ValueError): validate_plan(plan, files, {'increment': 'Increment'})

    def test_stale_pr_and_closed_pr_rejected(self):
        original = {'kind':'github_pr', 'url':'https://github.com/owner/repo/pull/1', 'head':'a'*40, 'base':'b'*40, 'state':'open'}
        for changed in [{'head':'c'*40}, {'base':'c'*40}, {'state':'closed'}]:
            with patch('pr_intake.metadata', return_value={**original, **changed}):
                with self.assertRaises(ValueError): freshness(original)

    def test_url_restrictions(self):
        for url in ['http://github.com/a/b/pull/1', 'https://example.com/a/b/pull/1',
                    'https://github.com/a/../pull/1', 'https://github.com/a/b/pull/1?token=secret']:
            with self.assertRaises(ValueError): parse_url(url)
        self.assertEqual(parse_url('https://github.com/a/b/pull/1'), ('a','b','1'))

    def test_pr_race_retains_download_but_does_not_issue_snapshot(self):
        origin = {'head':'a'*40, 'base':'b'*40, 'state':'open'}
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)/'intake'
            with patch('pr_intake.metadata', side_effect=[origin, {**origin, 'head':'c'*40}]), \
                 patch('pr_intake.subprocess.run'), patch('pr_intake.git', side_effect=[b'a'*40, b'b'*40]):
                with self.assertRaises(ValueError): ingest('https://github.com/a/b/pull/1', output)
            self.assertTrue((output/'origin.json').exists())
            self.assertFalse((output/'snapshot.json').exists())

    def test_live_terminal_rejects_piped_decisions(self):
        from repository_repair import review
        with patch('repository_repair.sys.stdin.isatty', return_value=False):
            with self.assertRaises(ValueError): review(Path('unused'))

    def test_interrupted_execution_is_not_replayed(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'candidate'; manifest = self.candidate(path)
            ledger = ae.Ledger(path/'ledger.sqlite')
            try:
                grant = ledger.decision(manifest, 'simulation', 'approve', simulated=True)
                with patch('repository_repair.run_tests', side_effect=RuntimeError('interruption')) as run:
                    with self.assertRaises(RuntimeError): execute(path, manifest, ledger, grant, 'simulation', simulated=True)
                    with self.assertRaises(ValueError): execute(path, manifest, ledger, grant, 'simulation', simulated=True)
                    self.assertEqual(run.call_count, 1)
                self.assertEqual(ledger.db.execute('SELECT state FROM operations').fetchone()['state'], 'AMBIGUOUS')
            finally: ledger.db.close()

    def test_bare_committed_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)/'source'; repo.mkdir()
            def git(*args): return subprocess.run(['git','-C',str(repo),*args], check=True, capture_output=True)
            git('init'); (repo/'a.py').write_text('x = 1\n')
            git('add','a.py'); git('-c','user.name=Test','-c','user.email=test@example.invalid','commit','-m','fixture')
            bare = Path(tmp)/'bare.git'
            subprocess.run(['git','clone','--bare',str(repo),str(bare)], check=True, capture_output=True)
            snap = freeze(bare)
            self.assertFalse(snap['working_tree_changes_excluded'])
            self.assertEqual(snap['files']['a.py']['content'], 'x = 1\n')
            origin = {'kind':'local','repo':str(repo),'revision':'HEAD','paths':['a.py'],'commit':snap['commit']}
            freshness(origin)
            (repo/'a.py').write_text('x = 2\n')
            with self.assertRaises(ValueError): freshness(origin)


if __name__ == '__main__': unittest.main()
