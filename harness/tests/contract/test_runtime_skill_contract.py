from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SKILL_NAMES = (
    "intel-openvino-model-converter",
    "intel-openvino-inference-runner",
    "intel-openvino-benchmark",
    "intel-openvino-model-optimizer",
    "intel-openvino-model-server",
    "intel-openvino-genai-runner",
)
REPORT_KEYS = {"schema_version", "collection_status", "context", "request", "selection", "plan", "execution", "verification", "warnings", "issues"}


class RuntimeSkillContractTests(unittest.TestCase):
    def test_candidate_and_release_have_valid_frontmatter_and_scripts(self):
        for name in SKILL_NAMES:
            for root in (ROOT / "candidates" / name, ROOT.parent / "skills" / name):
                skill = (root / "SKILL.md").read_text(encoding="utf-8")
                self.assertTrue(skill.startswith("---\n"), str(root))
                self.assertIn(f"name: {name}", skill)
                self.assertTrue((root / "scripts").is_dir(), str(root))
                self.assertTrue(any((root / "scripts").glob("*.py")), str(root))

    def test_report_keys_are_documented(self):
        contract = (ROOT / "specs/005-openvino-runtime-skills/contracts/runtime-skill-report.md").read_text(encoding="utf-8")
        for key in REPORT_KEYS:
            self.assertIn(f"`{key}`", contract)


if __name__ == "__main__":
    unittest.main()
