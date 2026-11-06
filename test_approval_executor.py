"""Simulated approvals on temporary fixtures only; never approve the real candidate."""
from datetime import timedelta
import difflib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import approval_executor as ae


def make_patch(content="import unittest\nfrom collection_ops import Common_Items\n"):
    return ''.join(difflib.unified_diff([], content.splitlines(keepends=True),
        fromfile='/dev/null', tofile='b/' + ae.TARGET)).encode()


class LedgerSafety(unittest.TestCase):
    def setUp(self):
        root = ae.ROOT / 'artifacts/tests'
        root.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=root)
        self.directory = Path(self.temp.name)
        self.ledger = ae.Ledger(self.directory / 'ledger.sqlite')
        self.manifest = {'patch_sha256': 'test-only-patch', 'parent_tree_hash': 'test-only-parent',
                         'plan_version': 1, 'run_id': 'simulated-test-only', 'policy': ae.POLICY}

    def tearDown(self):
        self.ledger.db.close()
        self.temp.cleanup()

    def approval(self, **kwargs):
        return self.ledger.decision(self.manifest, 'test-actor', 'approve', simulated=True, **kwargs)

    def consume(self, identity, manifest=None, actor='test-actor', simulated=True):
        return self.ledger.consume(identity, manifest or self.manifest, actor, simulated=simulated)

    def test_single_use_duplicate_and_reopened_ledger(self):
        identity = self.approval()
        first = self.consume(identity)
        self.assertEqual(first['state'], 'PREPARED')
        self.ledger.db.close()
        self.ledger = ae.Ledger(self.directory / 'ledger.sqlite')
        self.assertEqual(first['id'], self.consume(identity)['id'])
        second_approval = self.approval()
        with self.assertRaises(ValueError):
            self.consume(second_approval)
        self.assertEqual(self.ledger.db.execute('SELECT count(*) FROM operations').fetchone()[0], 1)

    def test_expired_rejected_and_forged_approvals_never_create_operation(self):
        expired = self.approval(at=ae.now() - timedelta(minutes=31))
        rejected = self.ledger.decision(self.manifest, 'test-actor', 'reject', simulated=True)
        for identity in [expired, rejected, 'forged-id']:
            with self.assertRaises(ValueError):
                self.consume(identity)
        self.assertEqual(self.ledger.db.execute('SELECT count(*) FROM operations').fetchone()[0], 0)

    def test_changed_patch_parent_plan_policy_scope_and_run_rejected(self):
        identity = self.approval()
        for key in ['patch_sha256','parent_tree_hash','plan_version','policy','scope','run_id']:
            changed = dict(self.manifest, **{key: 'changed'})
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.consume(identity, changed)

    def test_actor_and_simulated_mode_cannot_impersonate_operator(self):
        identity = self.approval()
        with self.assertRaises(ValueError):
            self.consume(identity, actor='other-actor')
        with self.assertRaises(ValueError):
            self.consume(identity, simulated=False)

    def test_deferral_has_no_expiration_and_cannot_authorize(self):
        identity = self.ledger.decision(self.manifest, 'test-actor', 'defer', simulated=True)
        row = self.ledger.db.execute('SELECT * FROM decisions WHERE id=?', (identity,)).fetchone()
        self.assertIsNone(row['expires'])
        with self.assertRaises(ValueError):
            self.consume(identity)

    def test_patch_traversal_binary_and_second_file_rejected(self):
        valid = make_patch()
        self.assertTrue(ae.patch_content(valid).startswith(b'import unittest'))
        bad = [valid.replace(b'b/tests/test_collection_ops.py', b'b/../escape.py'),
               valid + b'--- /dev/null\n+++ b/other.py\n', b'GIT binary patch\n',
               valid.replace(b'import unittest', b'import subprocess')]
        for value in bad:
            with self.subTest(value=value), self.assertRaises((ValueError, SyntaxError)):
                ae.patch_content(value)

    def test_export_excludes_git_env_and_unrelated_files(self):
        import io, tarfile
        (self.directory / ae.SOURCE).write_text('original = True\n')
        (self.directory / '.env').write_text('FAKE_TEST_ONLY=do-not-export\n')
        (self.directory / 'secret.txt').write_text('test-only')
        with tarfile.open(fileobj=io.BytesIO(ae.export_source(self.directory))) as archive:
            self.assertEqual(archive.getnames(), [ae.SOURCE])

    def test_durable_lock_excludes_second_executor(self):
        with ae.run_lock(self.directory):
            with self.assertRaises(ValueError):
                with ae.run_lock(self.directory):
                    self.fail('Second executor acquired run')

    def test_applied_workspace_reconciliation_does_not_apply_again(self):
        # Independent simulated repository; not the pending human candidate.
        repo = self.directory / 'fixture'
        repo.mkdir()
        (repo / ae.SOURCE).write_text('original = True\n')
        ae.git(repo, 'init')
        ae.git(repo, '-c', 'core.autocrlf=false', 'add', ae.SOURCE)
        ae.git(repo, '-c', 'user.name=Simulated Test', '-c', 'user.email=test@example.invalid',
               'commit', '-m', 'Simulated test fixture')
        m = {'parent_commit': ae.git(repo, 'rev-parse', 'HEAD').decode().strip()}
        content = b'import unittest\nfrom collection_ops import Common_Items\n'
        ae.git(repo, 'apply', '-', data=make_patch(content.decode()))
        first = ae.reconcile_workspace(repo, m, content)
        with patch.object(ae, 'git', wraps=ae.git) as calls:
            self.assertEqual(ae.reconcile_workspace(repo, m, content), first)
            self.assertFalse(any('apply' in call.args for call in calls.call_args_list))
        (repo / ae.SOURCE).write_text('tampered = True\n')
        with self.assertRaises(ValueError):
            ae.reconcile_workspace(repo, m, content)

    def execution_fixture(self):
        baseline = self.directory / 'artifacts/first-patch/baseline'
        baseline.mkdir(parents=True)
        (baseline / ae.SOURCE).write_bytes(b'original = True\n')
        ae.git(baseline, 'init')
        ae.git(baseline, 'add', ae.SOURCE)
        ae.git(baseline, '-c', 'user.name=Simulated Test', '-c', 'user.email=test@example.invalid',
               'commit', '-m', 'Simulated executor fixture')
        candidate = self.directory / 'candidate'
        candidate.mkdir()
        patch_bytes = make_patch()
        (candidate / 'candidate.patch').write_bytes(patch_bytes)
        manifest = dict(self.manifest, parent_commit=ae.git(baseline,'rev-parse','HEAD').decode().strip(),
                        patch_sha256=ae.digest(patch_bytes))
        identity = self.ledger.decision(manifest, 'test-actor', 'approve', simulated=True)
        return baseline, candidate, manifest, identity

    def test_missing_isolation_blocks_before_approval_consumption(self):
        baseline, candidate, manifest, identity = self.execution_fixture()
        with patch.object(ae, 'validate',return_value=manifest), patch.object(ae, 'preflight', side_effect=ValueError('No container')):
            with self.assertRaises(ValueError):
                ae.execute(candidate, manifest, self.ledger, identity, 'test-actor', simulated=True)
        self.assertEqual(self.ledger.db.execute('SELECT count(*) FROM operations').fetchone()[0], 0)
        self.assertFalse((baseline / ae.TARGET).exists())

    def test_crash_window_after_apply_reconciles_without_reapply_and_replay_is_noop(self):
        baseline, candidate, manifest, identity = self.execution_fixture()
        operation = self.ledger.consume(identity, manifest, 'test-actor', simulated=True)
        workspace = candidate / 'operations' / operation['id'] / 'workspace'
        workspace.parent.mkdir(parents=True)
        ae.git(baseline,'clone','--no-hardlinks',str(baseline),str(workspace))
        ae.git(workspace,'apply','-',data=(candidate/'candidate.patch').read_bytes())
        # Durable PREPARED intent with already-applied bytes models the crash window.
        outcomes = [{'status':'no_tests'}, {'status':'passed','tests':7}]
        with patch.object(ae,'ROOT',self.directory), patch.object(ae,'validate',return_value=manifest), patch.object(ae,'preflight'), \
             patch.object(ae,'container_check',side_effect=outcomes) as runner, patch.object(ae,'git',wraps=ae.git) as calls:
            result = ae.execute(candidate,manifest,self.ledger,identity,'test-actor',simulated=True)
            self.assertEqual(result['state'],'VERIFIED')
            self.assertFalse(any('apply' in call.args for call in calls.call_args_list))
            repeated = ae.execute(candidate,manifest,self.ledger,identity,'test-actor',simulated=True)
            self.assertTrue(repeated['replayed'])
            self.assertEqual(runner.call_count,2)
        self.assertFalse((baseline / ae.TARGET).exists())

    def test_failed_verification_quarantines_workspace_and_blocks_reapplication(self):
        baseline, candidate, manifest, identity = self.execution_fixture()
        with patch.object(ae,'ROOT',self.directory), patch.object(ae,'validate',return_value=manifest), patch.object(ae,'preflight'), \
             patch.object(ae,'container_check',side_effect=[{'status':'no_tests'},{'status':'failed','tests':7}]) as runner:
            result = ae.execute(candidate,manifest,self.ledger,identity,'test-actor',simulated=True)
            self.assertEqual(result['state'],'FAILED')
            operation_root, workspace, quarantine = ae.operation_paths(candidate,result['operation_id'])
            self.assertTrue(quarantine.exists())
            self.assertFalse(workspace.exists())
            ae.execute(candidate,manifest,self.ledger,identity,'test-actor',simulated=True)
            self.assertEqual(runner.call_count,2)
        self.assertFalse((baseline/ae.TARGET).exists())


if __name__ == '__main__':
    unittest.main()
