import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "candidates" / "intel-openvino-installer" / "scripts" / "openvino_installer.py"
FIXTURES = ROOT / "fixtures" / "openvino-installer"


def run_cli(*args):
    result = subprocess.run(
        [sys.executable, str(CLI), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise AssertionError(result.stderr or result.stdout)
    return json.loads(result.stdout)


class OpenVINOInstallerTests(unittest.TestCase):
    def test_python_plan_requires_confirmation_and_does_not_execute(self):
        report = run_cli(
            "--fixture", str(FIXTURES / "environments" / "windows-python.json"),
            "--mode", "plan",
            "--format", "json",
        )
        self.assertEqual(report["selection"]["method"], "pip")
        self.assertTrue(report["plan"]["confirmation_required"])
        self.assertEqual(report["execution"]["status"], "not_run")

    def test_fixture_apply_verifies_runtime(self):
        report = run_cli(
            "--fixture", str(FIXTURES / "methods" / "pip-success.json"),
            "--mode", "apply",
            "--confirm",
            "--format", "json",
        )
        self.assertEqual(report["execution"]["status"], "passed")
        self.assertEqual(report["verification"]["status"], "passed")
        self.assertEqual(report["verification"]["installed_version"], "2026.3.0")

    def test_permission_failure_is_redacted(self):
        report = run_cli(
            "--fixture", str(FIXTURES / "failures" / "permission.json"),
            "--mode", "apply",
            "--confirm",
            "--format", "json",
        )
        serialized = json.dumps(report)
        self.assertEqual(report["execution"]["status"], "failed")
        self.assertNotIn("SECRET_VALUE", serialized)


if __name__ == "__main__":
    unittest.main()
