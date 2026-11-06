"""Independent fixtures only; does not run or approve the optimization candidate."""
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import approval_executor as ae
import optimization_step as opt

ORIGINAL = b'def find_users(connection, name):\n    return name\n\ndef Common_Items(list, other):\n    return list\n'
PROPOSED = ORIGINAL.replace(b'    return list\n', b'    # Independent simulated source change\n    return list\n')


class OptimizationGuards(unittest.TestCase):
    def test_normalization_removes_whitespace_only_lines(self):
        self.assertEqual(opt.normalize_source('def f():\n    \n    return 1   \n'),b'def f():\n\n    return 1\n')

    def test_normalization_preserves_string_contents(self):
        text='def f():\n    """retained  \n    \n    text  """\n    return "a  "\n'
        self.assertEqual(opt.normalize_source(text),text.encode())

    def test_run_artifacts_do_not_relocate_trusted_harness(self):
        import io, tarfile
        root=ae.PROJECT/'artifacts/tests';root.mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(dir=root) as name:
            home=Path(name)
            (home/ae.SOURCE).write_bytes(ORIGINAL)
            (home/'tests').mkdir()
            (home/ae.TARGET).write_bytes(b'# packaging fixture only\n')
            expected=(ae.PROJECT/'optimization_checks.py').read_bytes()
            with patch.object(opt,'ROOT',home/'artifacts-only'),patch.object(opt,'BASE',home):
                self.assertEqual(opt.policy()['acceptance_harness_sha256'],ae.digest(expected))
                with tarfile.open(fileobj=io.BytesIO(opt.export(home))) as archive:
                    self.assertEqual(archive.extractfile('optimization_checks.py').read(),expected)

    def test_source_validator_rejects_sql_signature_import_and_rename_changes(self):
        opt.validate_source(ORIGINAL,PROPOSED)
        for bad in [PROPOSED.replace(b'return name',b'return connection'),
                    PROPOSED.replace(b'(list, other)',b'(items, other)'),
                    PROPOSED+b'\nimport os\n',PROPOSED.replace(b'Common_Items',b'common_items')]:
            with self.subTest(bad=bad),self.assertRaises(ValueError):
                opt.validate_source(ORIGINAL,bad)

    def test_existing_source_is_applied_once_and_tests_preserved(self):
        root=ae.ROOT/'artifacts/tests';root.mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(dir=root) as name:
            home=Path(name);base=home/'base';(base/'tests').mkdir(parents=True)
            (base/ae.SOURCE).write_bytes(ORIGINAL)
            test_bytes=b'# Original simulated test fixture\n'
            (base/ae.TARGET).write_bytes(test_bytes)
            ae.git(base,'init');ae.git(base,'add','--',ae.SOURCE,ae.TARGET)
            ae.git(base,'-c','user.name=Simulated Test','-c','user.email=test@example.invalid','commit','-m','Independent fixture')
            directory=home/'candidate';directory.mkdir()
            patch_bytes=opt.diff(ORIGINAL,PROPOSED)
            (directory/'candidate.patch').write_bytes(patch_bytes)
            (directory/'candidate_source.txt').write_bytes(PROPOSED)
            manifest={'run_id':'simulated-source-test','parent_commit':ae.git(base,'rev-parse','HEAD').decode().strip(),
                      'patch_sha256':ae.digest(patch_bytes)}
            ledger=ae.Ledger(directory/'ledger.sqlite')
            try:
                approval=ledger.decision(manifest,'simulated-operator','approve',simulated=True)
                with patch.object(ae,'preflight'),patch.object(opt,'BASE',base):
                    result=ae.execute(directory,manifest,ledger,approval,'simulated-operator',simulated=True,
                        validate_fn=lambda d:manifest,check_fn=lambda *args,**kwargs:{'status':'passed','tests':7},
                        reconcile_fn=opt.reconcile,content_fn=lambda p:opt.source_content(directory),
                        baseline_repo=base,changed_path=ae.SOURCE)
                    self.assertEqual(result['state'],'VERIFIED')
                    _,ws,_=ae.operation_paths(directory,result['operation_id'])
                    self.assertEqual((ws/ae.SOURCE).read_bytes(),PROPOSED)
                    self.assertEqual((ws/ae.TARGET).read_bytes(),test_bytes)
                    self.assertEqual((base/ae.SOURCE).read_bytes(),ORIGINAL)
                    (directory/'candidate.patch').write_bytes(patch_bytes.replace(b'b/collection_ops.py',b'b/escape.py'))
                    with self.assertRaises(ValueError): opt.source_content(directory)
            finally:
                ledger.db.close()


if __name__=='__main__':unittest.main()
