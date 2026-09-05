import json
import sys
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).parents[2] / "candidates" / "intel-hardware-advisor" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from report_model import REQUIRED_TOP_LEVEL, validate_report  # noqa: E402


class HardwareAdvisorContractTests(unittest.TestCase):
    def test_required_top_level_fields_are_stable(self):
        self.assertEqual(
            REQUIRED_TOP_LEVEL,
            (
                "schema_version",
                "platform",
                "runtime",
                "facts",
                "evidence",
                "recommendation",
                "collection_status",
            ),
        )

    def test_valid_report_satisfies_v1_contract(self):
        report = {
            "schema_version": "1.0",
            "platform": {},
            "runtime": {},
            "facts": [
                {
                    "id": "platform.system",
                    "name": "platform.system",
                    "value": "Windows",
                    "status": "detected",
                    "source": "platform",
                    "evidence_ids": ["ev.platform.system"],
                }
            ],
            "evidence": [
                {
                    "id": "ev.platform.system",
                    "kind": "detected",
                    "source": "platform module",
                    "limitations": [],
                }
            ],
            "recommendation": {
                "decision": "no_decision",
                "confidence": "none",
                "rationale": ["More evidence is required."],
                "evidence_ids": [],
                "next_steps": ["Inspect the runtime-visible device list."],
            },
            "collection_status": {"status": "partial", "issues": []},
        }
        validate_report(report)
        self.assertEqual(json.loads(json.dumps(report)), report)

    def test_nested_platform_metadata_and_configurations_are_accepted(self):
        report = {
            "schema_version": "1.0",
            "platform": {
                "system": "macOS",
                "architecture": "arm64",
                "context": {"wsl": False, "container": False},
            },
            "runtime": {
                "additional_configurations": {
                    "gpu": {
                        "status": "not_applicable",
                        "checks": {},
                        "notes": [],
                    }
                }
            },
            "facts": [
                {
                    "id": "configuration.gpu",
                    "name": "configuration.gpu",
                    "value": {"status": "not_applicable"},
                    "status": "not_applicable",
                    "source": "additional_configurations",
                    "evidence_ids": ["ev.configurations"],
                }
            ],
            "evidence": [
                {
                    "id": "ev.configurations",
                    "kind": "detected",
                    "source": "local additional-configuration collector",
                    "limitations": [],
                }
            ],
            "recommendation": {
                "decision": "no_decision",
                "confidence": "none",
                "rationale": ["No workload decision requested."],
                "evidence_ids": ["ev.configurations"],
                "next_steps": [],
            },
            "collection_status": {"status": "complete", "issues": []},
        }
        validate_report(report)

    def test_top_level_json_object_order_is_not_significant(self):
        report = {
            "collection_status": {"status": "complete", "issues": []},
            "recommendation": {
                "decision": "no_decision",
                "confidence": "none",
                "rationale": ["More evidence is required."],
                "evidence_ids": [],
                "next_steps": [],
            },
            "evidence": [],
            "facts": [],
            "runtime": {},
            "platform": {},
            "schema_version": "1.0",
        }
        validate_report(report)

    def test_invalid_report_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_report({"schema_version": "1.0"})


if __name__ == "__main__":
    unittest.main()
