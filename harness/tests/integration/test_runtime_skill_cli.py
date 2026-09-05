from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CASES = [
    ("intel-openvino-model-converter", "scripts/model_converter.py", "converter/onnx-success.json", "onnx"),
    ("intel-openvino-inference-runner", "scripts/inference_runner.py", "inference/docker-success.json", "AUTO"),
    ("intel-openvino-benchmark", "scripts/benchmark_runner.py", "benchmark/comparison-success.json", "CPU"),
    ("intel-openvino-model-optimizer", "scripts/model_optimizer.py", "optimizer/ptq-success.json", "ptq"),
    ("intel-openvino-model-server", "scripts/model_server.py", "server/docker-success.json", "docker-local"),
    ("intel-openvino-genai-runner", "scripts/genai_runner.py", "genai/chat-success.json", "chat"),
]


class RuntimeSkillCliTests(unittest.TestCase):
    def test_profiles_select_expected_workflows(self):
        for name, script, fixture, expected in CASES:
            result = subprocess.run([sys.executable, str(ROOT / "candidates" / name / script), "--fixture", str(ROOT / "fixtures/openvino-runtime-skills" / fixture), "--mode", "plan", "--format", "json"], cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(result.stdout)
            selection = report["selection"]
            values = {str(value) for value in selection.values()}
            self.assertIn(expected, values, name)


if __name__ == "__main__":
    unittest.main()
