import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "candidates" / "intel-openvino-installer" / "scripts" / "openvino_installer.py"
FIXTURE = ROOT / "fixtures" / "openvino-installer" / "methods" / "ecosystems.json"


class OpenVINOInstallerCliTests(unittest.TestCase):
    def test_documented_ecosystems_select_the_requested_method(self):
        scenarios = json.loads(FIXTURE.read_text(encoding="utf-8"))["scenarios"]
        for scenario in scenarios:
            fixture = {
                "context": {
                    "system": scenario["system"],
                    "distribution": scenario.get("distribution"),
                    "architecture": "x86_64",
                    "execution_context": "native",
                    "ecosystem": scenario["ecosystem"],
                    "permissions": "available",
                    "available_tools": {scenario["tool"]: True},
                },
                "request": {
                    "ecosystem": scenario["ecosystem"],
                    "method": scenario["method"],
                    "version": scenario.get("version", "maintenance"),
                },
            }
            temp = ROOT / "fixtures" / "openvino-installer" / "methods" / f"_{scenario['name']}.json"
            temp.write_text(json.dumps(fixture), encoding="utf-8")
            try:
                result = subprocess.run(
                    [sys.executable, str(CLI), "--fixture", str(temp), "--mode", "plan", "--format", "json"],
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                report = json.loads(result.stdout)
                self.assertEqual(report["selection"]["method"], scenario["method"])
            finally:
                temp.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
