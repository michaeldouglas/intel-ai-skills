import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).parents[2]
SCRIPTS = ROOT / "candidates" / "intel-hardware-advisor" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import hardware_probe  # noqa: E402
from report_model import build_recommendation, build_report, validate_report  # noqa: E402


def fixture(name):
    return json.loads((ROOT / "fixtures" / "hardware-advisor" / name).read_text(encoding="utf-8"))


class HardwareAdvisorUnitTests(unittest.TestCase):
    def test_supported_windows_fixture_has_separate_platform_and_runtime(self):
        report = build_report(fixture("windows-supported.json"))
        validate_report(report)
        self.assertEqual(report["platform"]["system"], "Windows")
        self.assertEqual(report["runtime"]["openvino"]["status"], "available")
        self.assertTrue(report["facts"])
        self.assertTrue(report["evidence"])
        self.assertEqual(report["runtime"]["openvino"]["devices"][0]["type"], "GPU")
        self.assertEqual(report["runtime"]["additional_configurations"]["gpu"]["status"], "incomplete")
        self.assertIn("additional configuration", " ".join(report["recommendation"]["rationale"]).lower())

    def test_macos_arm64_is_detected_and_keeps_device_specific_scope(self):
        report = build_report(fixture("macos-supported.json"))
        self.assertEqual(report["platform"]["system"], "macOS")
        self.assertEqual(report["platform"]["architecture"], "arm64")
        self.assertEqual(report["runtime"]["additional_configurations"]["gpu"]["status"], "not_applicable")
        self.assertEqual(report["runtime"]["openvino"]["devices"][0]["type"], "CPU")

    def test_platform_metadata_is_preserved_as_facts(self):
        report = build_report(fixture("linux-supported.json"))
        facts = {fact["name"]: fact["value"] for fact in report["facts"]}
        self.assertEqual(facts["platform.distribution"], "ubuntu")
        self.assertEqual(facts["platform.kernel"], "6.8-test")
        self.assertEqual(facts["platform.architecture"], "x86_64")

    def test_missing_openvino_does_not_hide_platform_facts(self):
        report = build_report(fixture("openvino-missing.json"))
        self.assertEqual(report["platform"]["system"], "Linux")
        self.assertEqual(report["runtime"]["openvino"]["status"], "unavailable")
        self.assertEqual(report["recommendation"]["decision"], "no_decision")

    def test_device_name_alone_cannot_produce_capability_guidance(self):
        recommendation = build_recommendation(
            [{"id": "device", "name": "runtime.device", "value": "Intel GPU", "status": "detected"}],
            [{"id": "ev", "kind": "detected", "source": "runtime", "limitations": ["name only"]}],
        )
        self.assertEqual(recommendation["decision"], "no_decision")
        self.assertIn("vendor", " ".join(recommendation["next_steps"]).lower())

    def test_conflicting_vendor_evidence_is_no_decision(self):
        report = build_report(fixture("conflicting-evidence.json"))
        self.assertEqual(report["recommendation"]["decision"], "no_decision")
        self.assertIn("conflict", " ".join(report["recommendation"]["rationale"]).lower())

    def test_live_command_runner_is_shell_free_and_maps_missing_tool(self):
        result = hardware_probe.run_command(["definitely-not-a-real-tool"], timeout=0.1)
        self.assertEqual(result["status"], "unavailable")
        self.assertNotIn("Traceback", result.get("message", ""))

    def test_live_openvino_import_failure_is_explicit(self):
        with patch.dict(sys.modules, {"openvino": None}):
            result = hardware_probe.collect_openvino()
        self.assertIn(result["status"], {"unavailable", "failed"})

    def test_live_macos_platform_collection_is_supported_and_normalized(self):
        with patch.object(hardware_probe.platform, "system", return_value="Darwin"), patch.object(
            hardware_probe.platform, "release", return_value="23.6-test"
        ), patch.object(hardware_probe.platform, "machine", return_value="arm64"), patch.object(
            hardware_probe.platform, "mac_ver", return_value=("14.6", ("", "", ""), "")
        ):
            profile = hardware_probe.collect_platform()
        self.assertEqual(profile["system"], "macOS")
        self.assertEqual(profile["architecture"], "arm64")
        self.assertEqual(profile["status"], "detected")

    def test_failure_fixture_preserves_non_success_status(self):
        report = build_report(fixture("permission-failure.json"))
        validate_report(report)
        statuses = {fact["status"] for fact in report["facts"]}
        self.assertTrue(statuses & {"permission_denied", "unavailable", "failed"})


if __name__ == "__main__":
    unittest.main()
