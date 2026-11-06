"""Real Docker probes on original test fixtures; never applies the human candidate."""
from pathlib import Path
import tempfile
import unittest

from approval_executor import ROOT, container_check, preflight

PROBES = '''import os,pathlib,unittest
class BoundaryProbes(unittest.TestCase):
 def test_nonroot(self): self.assertEqual(os.getuid(),65534)
 def test_no_network_interfaces(self): self.assertEqual(sorted(p.name for p in pathlib.Path('/sys/class/net').iterdir()),['lo'])
 def test_no_capabilities(self): self.assertIn('CapEff:\\t0000000000000000',pathlib.Path('/proc/self/status').read_text())
 def test_no_new_privileges(self): self.assertIn('NoNewPrivs:\\t1',pathlib.Path('/proc/self/status').read_text())
 def test_memory_limit(self): self.assertEqual(pathlib.Path('/sys/fs/cgroup/memory.max').read_text().strip(),'134217728')
 def test_process_limit(self): self.assertEqual(pathlib.Path('/sys/fs/cgroup/pids.max').read_text().strip(),'32')
 def test_no_credentials_or_git(self):
  self.assertNotIn('GOOGLE_API_KEY',os.environ)
  self.assertFalse(pathlib.Path('/workspace/.git').exists())
  self.assertFalse(pathlib.Path('/workspace/.env').exists())
 def test_root_readonly(self):
  with self.assertRaises(OSError): pathlib.Path('/readonly-probe').write_text('x')
 def test_cpu_limit(self): self.assertEqual(pathlib.Path('/sys/fs/cgroup/cpu.max').read_text().split(),['50000','100000'])
'''

class ContainerBoundary(unittest.TestCase):
    def test_real_container_isolation_and_zero_test_baseline(self):
        preflight()
        root = ROOT / 'artifacts/tests'
        root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=root) as name:
            workspace = Path(name)
            (workspace / 'collection_ops.py').write_text('# Original boundary probe fixture\n')
            baseline = container_check(workspace, workspace / 'baseline.log', baseline=True)
            self.assertEqual(baseline['status'], 'no_tests')
            (workspace / 'tests').mkdir()
            (workspace / 'tests/test_collection_ops.py').write_text(PROBES)
            result = container_check(workspace, workspace / 'candidate.log')
            self.assertEqual(result['status'], 'passed', (workspace / 'candidate.log').read_text())
            self.assertEqual(result['tests'], 9)


if __name__ == '__main__':
    unittest.main()
