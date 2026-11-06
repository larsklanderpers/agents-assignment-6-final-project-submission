import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from repository_intake import freeze, validate, safe_path


class IntakeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        self.git('init', '-q')
        (self.repo / 'module.py').write_text('def add(a, b):\n    return a + b\n')
        (self.repo / 'test_module.py').write_text('from module import add\n')
        (self.repo / '.env').write_text('DUMMY=never-export\n')
        self.git('add', '.')
        self.git('-c', 'user.name=Test', '-c', 'user.email=test@example.invalid', 'commit', '-qm', 'fixture')

    def git(self, *args):
        return subprocess.check_output(['git', '-C', str(self.repo), *args])

    def tearDown(self):
        # Git objects can be read-only on Windows; retain these isolated test fixtures
        # for the TemporaryDirectory cleanup handler to reset permissions.
        self.tmp.cleanup()

    def test_committed_selection_excludes_secrets_and_dirty_edits(self):
        (self.repo / 'module.py').write_text('raise RuntimeError("not imported")\n')
        before = self.git('status', '--porcelain')
        snapshot = freeze(self.repo)
        self.assertNotIn('.env', snapshot['files'])
        self.assertIn('return a + b', snapshot['files']['module.py']['content'])
        self.assertTrue(snapshot['working_tree_changes_excluded'])
        self.assertEqual(before, self.git('status', '--porcelain'))
        self.assertEqual(snapshot, validate(snapshot))

    def test_tampering_is_rejected(self):
        snapshot = freeze(self.repo)
        snapshot['files']['module.py']['content'] = 'tampered'
        with self.assertRaises(ValueError): validate(snapshot)

    def test_unsafe_and_unsupported_paths(self):
        for name in ['../x.py', '/x.py', 'a\\x.py', 'a/../x.py', '.env', 'CON.py', 'a.py:stream', '.git/a.py']:
            with self.assertRaises(ValueError): safe_path(name)
        with self.assertRaises(ValueError): freeze(self.repo, paths=['missing.py'])
        with self.assertRaises(ValueError): freeze(self.repo, revision='--help')

    def test_scope_and_diff_are_pinned(self):
        base = self.git('rev-parse', 'HEAD').decode().strip()
        (self.repo / 'module.py').write_text('def add(a,b):\n    return a-b\n')
        self.git('add', 'module.py')
        self.git('-c', 'user.name=Test', '-c', 'user.email=test@example.invalid', 'commit', '-qm', 'change')
        result = freeze(self.repo, paths=['module.py'], base=base)
        self.assertEqual(result['base_commit'], base)
        self.assertEqual(result['changed_paths'], ['module.py'])
        self.assertEqual(result['excluded_file_count'], 2)


if __name__ == '__main__':
    unittest.main()
