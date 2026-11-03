"""Simulated approval, real Git/Docker: nested Win32 evidence must remain visible."""
import difflib
from pathlib import Path
import tempfile
import unittest

import approval_executor as ae


class LongPathExecution(unittest.TestCase):
    def test_approved_fixture_runs_and_replays_beyond_max_path(self):
        root = ae.ROOT / 'artifacts/tests'
        root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=root) as name:
            home = Path(name)
            base = home / 'baseline'
            base.mkdir()
            (base / ae.SOURCE).write_bytes(b'def Common_Items(left, right):\n    return [v for v in left if v in right]\n')
            ae.git(base, 'init')
            ae.git(base, 'add', ae.SOURCE)
            ae.git(base, '-c', 'user.name=Simulated long-path fixture', '-c',
                   'user.email=fixture@example.invalid', 'commit', '-m', 'original fixture')
            # Candidate files remain short enough for SQLite; descendant test exceeds 260.
            padding = max(8, 220 - len(str(home.resolve())) - 1)
            candidate = home / ('c' * padding)
            candidate.mkdir()
            content = b'import unittest\nfrom collection_ops import Common_Items\nclass Behavior(unittest.TestCase):\n'
            checks = [([],[],[]), ([1],[],[]), ([],[1],[]), ([2,1],[1,2],[2,1]),
                      ([2,2],[2],[2,2]), ([1],[1,1],[1]), ([[1]],[[1]],[[1]])]
            for index, (left, right, expected) in enumerate(checks):
                content += f' def test_{index}(self): self.assertEqual(Common_Items({left!r}, {right!r}), {expected!r})\n'.encode()
            patch = ''.join(difflib.unified_diff([], content.decode().splitlines(keepends=True),
                fromfile='/dev/null', tofile='b/' + ae.TARGET)).encode()
            (candidate / 'candidate.patch').write_bytes(patch)
            manifest = dict(run_id='simulated-long-path-only', candidate_id='simulated', plan_version=1,
                parent_commit=ae.git(base,'rev-parse','HEAD').decode().strip(),
                parent_tree_hash=ae.git(base,'rev-parse','HEAD^{tree}').decode().strip(),
                patch_sha256=ae.digest(patch), policy=ae.POLICY, scope=[ae.SOURCE,ae.TARGET])
            ledger = ae.Ledger(candidate / 'ledger.sqlite')
            try:
                grant = ledger.decision(manifest, 'simulated-actor', 'approve', simulated=True)
                outcome = ae.execute(candidate, manifest, ledger, grant, 'simulated-actor', simulated=True,
                    validate_fn=lambda _: manifest, baseline_repo=base)
                self.assertEqual(outcome['state'], 'VERIFIED', outcome)
                operation_root, workspace, _ = ae.operation_paths(candidate,outcome['operation_id'])
                self.assertGreater(len(str(operation_root / 'candidate.log')), 260)
                self.assertLess(len(str(workspace / ae.TARGET)), 260)
                self.assertEqual((workspace / ae.TARGET).read_bytes(), content)
                replay = ae.execute(candidate, manifest, ledger, grant, 'simulated-actor', simulated=True,
                    validate_fn=lambda _: manifest, baseline_repo=base)
                self.assertTrue(replay['replayed'])
                self.assertEqual(ledger.db.execute('SELECT count(*) FROM operations').fetchone()[0], 1)
                self.assertFalse((base / ae.TARGET).exists())
            finally:
                ledger.db.close()
            # tempfile's Windows cleanup needs the same extended path as the executor.
            import shutil
            import os, stat
            def remove_readonly(function, path, error):
                os.chmod(path, stat.S_IWRITE)
                function(path)
            self.assertTrue(home.resolve().is_relative_to(root.resolve()))
            self.assertEqual(workspace.parent.name, outcome['operation_id'])
            self.assertTrue(workspace.parent.is_relative_to(ae.filesystem_path(ae.PROJECT / 'artifacts/ws')))
            shutil.rmtree(workspace.parent, onexc=remove_readonly)
            shutil.rmtree(ae.filesystem_path(home), onexc=remove_readonly)


if __name__ == '__main__':
    unittest.main()
