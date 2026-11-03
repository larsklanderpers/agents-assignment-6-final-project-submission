"""Exercise durable state across distinct operating-system processes."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


class PersistenceExperiment(unittest.TestCase):
    def test_restart_wait_resume_and_duplicate_resume(self):
        artifact_root = Path(__file__).parent / "artifacts"
        artifact_root.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=artifact_root) as directory:
            db = str(Path(directory) / "checkpoint.sqlite")

            def invoke(action, success=True):
                result = subprocess.run(
                    [sys.executable, str(Path(__file__).with_name("spike_persistence.py")),
                     action, "--db", db], capture_output=True, text=True,
                    timeout=30,
                )
                if success:
                    self.assertEqual(result.returncode, 0, result.stderr)
                    return json.loads(result.stdout)
                self.assertNotEqual(result.returncode, 0)

            pending = invoke("start")
            self.assertEqual(pending["next"], ["gate"])
            self.assertEqual(set(pending["values"]["reviews"]),
                             {"security", "performance", "style", "test_gap"})
            self.assertNotIn("decision", pending["values"])
            self.assertEqual(invoke("inspect"), pending)
            invoke("start", success=False)
            completed = invoke("resume")
            self.assertEqual(completed["next"], [])
            self.assertEqual(completed["values"]["decision"], "reject")
            invoke("resume", success=False)
            self.assertEqual(invoke("inspect"), completed)


if __name__ == "__main__":
    unittest.main()
