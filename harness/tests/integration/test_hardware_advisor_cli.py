import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[2]
CLI = ROOT / "candidates" / "intel-hardware-advisor" / "scripts" / "hardware_probe.py"
FIXTURES = ROOT / "fixtures" / "hardware-advisor"


class HardwareAdvisorCliTests(unittest.TestCase):
    def run_cli(self, fixture_name, output_format="json"):
        return subprocess.run(
            [sys.executable, str(CLI), "--fixture", str(FIXTURES / fixture_name), "--format", output_format],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_json_output_is_machine_readable(self):
        result = self.run_cli("linux-supported.json")
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["schema_version"], "1.0")
        self.assertIn("recommendation", report)

    def test_text_output_preserves_status_and_evidence(self):
        result = self.run_cli("openvino-missing.json", "text")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Collection status", result.stdout)
        self.assertIn("Evidence", result.stdout)
        self.assertIn("no_decision", result.stdout)

    def test_every_valid_fixture_produces_a_report(self):
        for path in FIXTURES.glob("*.json"):
            if path.name == "malformed-sensitive.json":
                continue
            result = self.run_cli(path.name)
            self.assertEqual(result.returncode, 0, f"{path.name}: {result.stderr}")
            self.assertIsInstance(json.loads(result.stdout), dict)

    def test_sensitive_fixture_is_rejected_before_reporting(self):
        result = self.run_cli("malformed-sensitive.json")
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("token-should-not-appear", result.stderr)


if __name__ == "__main__":
    unittest.main()
