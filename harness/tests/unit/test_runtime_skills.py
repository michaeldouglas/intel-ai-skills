from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "fixtures" / "openvino-runtime-skills"
SKILLS = {
    "converter": ROOT / "candidates/intel-openvino-model-converter/scripts/model_converter.py",
    "inference": ROOT / "candidates/intel-openvino-inference-runner/scripts/inference_runner.py",
    "benchmark": ROOT / "candidates/intel-openvino-benchmark/scripts/benchmark_runner.py",
    "optimizer": ROOT / "candidates/intel-openvino-model-optimizer/scripts/model_optimizer.py",
    "server": ROOT / "candidates/intel-openvino-model-server/scripts/model_server.py",
    "genai": ROOT / "candidates/intel-openvino-genai-runner/scripts/genai_runner.py",
}


def run(skill: str, fixture: Path, *extra: str) -> dict:
    result = subprocess.run([sys.executable, str(SKILLS[skill]), "--fixture", str(fixture), "--mode", "plan", "--format", "json", *extra], cwd=ROOT, capture_output=True, text=True)
    if result.returncode:
        raise AssertionError(result.stderr or result.stdout)
    return json.loads(result.stdout)


class RuntimeSkillTests(unittest.TestCase):
    def test_all_success_fixtures_have_common_report(self):
        fixtures = {"converter": "converter/onnx-success.json", "inference": "inference/docker-success.json", "benchmark": "benchmark/comparison-success.json", "optimizer": "optimizer/ptq-success.json", "server": "server/docker-success.json", "genai": "genai/chat-success.json"}
        expected = {"schema_version", "collection_status", "context", "request", "selection", "plan", "execution", "verification", "warnings", "issues"}
        for skill, relative in fixtures.items():
            report = run(skill, FIXTURES / relative)
            self.assertEqual(set(report), expected, skill)
            self.assertEqual(report["schema_version"], "1.0")
            self.assertFalse(report["issues"], skill)

    def test_converter_and_server_require_confirmation(self):
        for skill, fixture in (("converter", FIXTURES / "converter/onnx-success.json"), ("server", FIXTURES / "server/docker-success.json")):
            result = subprocess.run([sys.executable, str(SKILLS[skill]), "--fixture", str(fixture), "--mode", "apply", "--format", "json"], cwd=ROOT, capture_output=True, text=True)
            report = json.loads(result.stdout)
            self.assertEqual(report["execution"]["status"], "not_run")
            self.assertTrue(any("confirmation" in item["message"].lower() for item in report["issues"]))

    def test_missing_model_is_blocked(self):
        report = run("inference", FIXTURES / "failures/missing-model.json")
        self.assertEqual(report["plan"]["status"], "blocked")
        self.assertTrue(report["issues"])


if __name__ == "__main__":
    unittest.main()
