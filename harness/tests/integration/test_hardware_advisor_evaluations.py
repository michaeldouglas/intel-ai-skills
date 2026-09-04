import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[2]
SCRIPTS = ROOT / "candidates" / "intel-hardware-advisor" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from hardware_probe import load_fixture  # noqa: E402
from report_model import build_report  # noqa: E402


class HardwareAdvisorEvaluationTests(unittest.TestCase):
    def test_release_scenarios_match_their_expected_outcomes(self):
        scenarios = json.loads(
            (ROOT / "evaluations" / "intel-hardware-advisor" / "scenarios.json").read_text(encoding="utf-8")
        )["scenarios"]
        for scenario in scenarios:
            report = build_report(load_fixture(ROOT / "fixtures" / "hardware-advisor" / scenario["fixture"]))
            self.assertEqual(report["recommendation"]["decision"], scenario["expected_decision"], scenario["id"])
            if "expected_status" in scenario:
                self.assertEqual(report["collection_status"]["status"], scenario["expected_status"], scenario["id"])
            if "required_rationale" in scenario:
                rationale = " ".join(report["recommendation"]["rationale"]).lower()
                self.assertIn(scenario["required_rationale"], rationale, scenario["id"])
            for forbidden in scenario.get("forbidden_claims", []):
                rendered_guidance = " ".join(report["recommendation"]["rationale"] + report["recommendation"]["next_steps"]).lower()
                self.assertNotIn(f"supports {forbidden}", rendered_guidance, scenario["id"])


if __name__ == "__main__":
    unittest.main()
