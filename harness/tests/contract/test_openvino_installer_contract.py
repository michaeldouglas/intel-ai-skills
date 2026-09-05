import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "candidates" / "intel-openvino-installer" / "scripts" / "openvino_installer.py"
FIXTURE = ROOT / "fixtures" / "openvino-installer" / "environments" / "windows-python.json"
GENAI_FIXTURE = ROOT / "fixtures" / "openvino-installer" / "methods" / "genai-pip.json"


class OpenVINOInstallerContractTests(unittest.TestCase):
    def test_report_has_stable_top_level_contract(self):
        result = subprocess.run(
            [sys.executable, str(CLI), "--fixture", str(FIXTURE), "--mode", "plan", "--format", "json"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(
            set(report),
            {"schema_version", "collection_status", "context", "selection", "plan", "execution", "verification", "issues"},
        )
        self.assertEqual(report["schema_version"], "1.0")
        self.assertTrue(report["plan"]["confirmation_required"])

    def test_optional_genai_is_explicit_and_driver_installation_is_out_of_scope(self):
        result = subprocess.run(
            [sys.executable, str(CLI), "--fixture", str(GENAI_FIXTURE), "--mode", "plan", "--format", "json"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        commands = " ".join(action["display"] for action in report["plan"]["actions"])
        self.assertIn("openvino-genai", commands)
        self.assertNotRegex(commands.lower(), r"driver|bios|level.zero|opencl")


if __name__ == "__main__":
    unittest.main()
