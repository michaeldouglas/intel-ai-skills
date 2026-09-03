import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
SCRIPTS = ROOT / "candidates" / "intel-hardware-advisor" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from hardware_probe import load_fixture, validate_fixture  # noqa: E402


FIXTURES = ROOT / "fixtures" / "hardware-advisor"


class FixtureSafetyTests(unittest.TestCase):
    def test_fixture_set_contains_no_sensitive_keys_or_values(self):
        forbidden = {"password", "secret", "token", "api_key", "username", "user_name", "serial_number"}
        for path in FIXTURES.glob("*.json"):
            payload = json.loads(path.read_text(encoding="utf-8"))
            if path.name == "malformed-sensitive.json":
                with self.assertRaises(ValueError):
                    validate_fixture(payload)
                continue
            flattened = json.dumps(payload, sort_keys=True).lower()
            self.assertFalse(any(key in flattened for key in forbidden), path.name)
            validate_fixture(payload)

    def test_malformed_fixture_is_rejected_without_echoing_content(self):
        with self.assertRaises(ValueError) as context:
            load_fixture(FIXTURES / "malformed-sensitive.json")
        self.assertNotIn("token-should-not-appear", str(context.exception))

    def test_unknown_nested_fields_are_rejected(self):
        payload = json.loads((FIXTURES / "windows-supported.json").read_text(encoding="utf-8"))
        payload["platform"]["unexpected"] = "not allowed"
        with self.assertRaises(ValueError):
            validate_fixture(payload)


if __name__ == "__main__":
    unittest.main()
