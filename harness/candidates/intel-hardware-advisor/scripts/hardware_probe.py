"""Read-only local hardware/runtime probe with deterministic fixture support."""

from __future__ import annotations

import argparse
import json
import platform
import subprocess
import sys
from pathlib import Path
from typing import Any

from report_model import build_report


MAX_OUTPUT = 64_000
ALLOWED_FIXTURE_KEYS = {"fixture_version", "platform", "runtime", "collector_status"}
ALLOWED_PLATFORM_KEYS = {"system", "release", "machine", "status"}
ALLOWED_RUNTIME_KEYS = {"openvino"}
ALLOWED_OPENVINO_KEYS = {"status", "version", "devices"}
ALLOWED_DEVICE_KEYS = {"id", "name", "vendor", "status"}
FORBIDDEN_TOKENS = {"password", "secret", "token", "api_key", "username", "user_name", "serial_number"}


def run_command(args: list[str], timeout: float = 2.0) -> dict[str, Any]:
    """Run an explicit command without a shell and return safe metadata only."""
    if not args or not all(isinstance(item, str) and item for item in args):
        return {"status": "failed", "message": "invalid command arguments"}
    try:
        completed = subprocess.run(
            args,
            shell=False,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except FileNotFoundError:
        return {"status": "unavailable", "message": "tool is not installed"}
    except subprocess.TimeoutExpired:
        return {"status": "failed", "message": "tool timed out"}
    except PermissionError:
        return {"status": "permission_denied", "message": "tool permission denied"}
    except OSError:
        return {"status": "failed", "message": "tool could not be executed"}
    if completed.returncode != 0:
        return {"status": "failed", "message": "tool returned an error"}
    # The live first release intentionally does not parse arbitrary command output.
    _ = (completed.stdout or "")[:MAX_OUTPUT]
    return {"status": "detected", "message": "tool completed"}


def collect_platform() -> dict[str, Any]:
    system = platform.system() or ""
    status = "detected" if system in {"Windows", "Linux"} else "unsupported"
    return {
        "system": system or None,
        "release": platform.release() or None,
        "machine": platform.machine() or None,
        "status": status,
    }


def collect_openvino() -> dict[str, Any]:
    try:
        import openvino as ov  # type: ignore

        core = ov.Core()
        devices = []
        for device_id in core.available_devices:
            name = device_id
            try:
                name = str(core.get_property(device_id, "FULL_DEVICE_NAME"))[:256]
            except Exception:
                name = device_id
            devices.append({"id": str(device_id)[:64], "name": name, "status": "detected"})
        return {"status": "available", "version": str(getattr(ov, "__version__", "unknown"))[:64], "devices": devices}
    except ImportError:
        return {"status": "unavailable", "version": None, "devices": []}
    except PermissionError:
        return {"status": "permission_denied", "version": None, "devices": []}
    except Exception:
        return {"status": "failed", "version": None, "devices": []}


def collect_live() -> dict[str, Any]:
    platform_profile = collect_platform()
    openvino_profile = collect_openvino()
    return {
        "platform": platform_profile,
        "runtime": {"openvino": openvino_profile},
        "collector_status": {
            "platform": platform_profile["status"],
            "openvino": "available" if openvino_profile.get("status") == "available" else openvino_profile.get("status"),
        },
    }


def _walk_for_forbidden(value: Any) -> bool:
    if isinstance(value, dict):
        for key, nested in value.items():
            lowered = str(key).lower()
            if lowered in FORBIDDEN_TOKENS or any(token in lowered for token in FORBIDDEN_TOKENS):
                return True
            if _walk_for_forbidden(nested):
                return True
    elif isinstance(value, list):
        return any(_walk_for_forbidden(item) for item in value)
    return False


def validate_fixture(payload: dict[str, Any]) -> None:
    if not isinstance(payload, dict) or set(payload) != ALLOWED_FIXTURE_KEYS:
        raise ValueError("fixture shape is not allowed")
    if payload.get("fixture_version") != "1":
        raise ValueError("unsupported fixture version")
    if _walk_for_forbidden(payload):
        raise ValueError("fixture contains a forbidden field")
    if not isinstance(payload.get("platform"), dict) or not isinstance(payload.get("runtime"), dict):
        raise ValueError("fixture platform and runtime must be objects")
    if not set(payload["platform"]).issubset(ALLOWED_PLATFORM_KEYS) or not set(payload["runtime"]).issubset(ALLOWED_RUNTIME_KEYS):
        raise ValueError("fixture contains an unknown platform or runtime field")
    openvino = payload["runtime"].get("openvino")
    if not isinstance(openvino, dict) or not set(openvino).issubset(ALLOWED_OPENVINO_KEYS) or not isinstance(openvino.get("devices", []), list):
        raise ValueError("fixture OpenVINO data is malformed")
    for device in openvino.get("devices", []):
        if not isinstance(device, dict) or not set(device).issubset(ALLOWED_DEVICE_KEYS) or not isinstance(device.get("id"), str):
            raise ValueError("fixture device is malformed")


def load_fixture(path: str | Path) -> dict[str, Any]:
    try:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        raise ValueError("fixture could not be read") from None
    validate_fixture(payload)
    return payload


def render_text(report: dict[str, Any]) -> str:
    recommendation = report["recommendation"]
    lines = [
        "Intel Hardware Advisor",
        f"Collection status: {report['collection_status']['status']}",
        f"Platform: {report['platform'].get('system')} {report['platform'].get('release')} ({report['platform'].get('machine')})",
        f"OpenVINO: {report['runtime']['openvino'].get('status')} {report['runtime']['openvino'].get('version') or ''}".rstrip(),
        f"Recommendation: {recommendation['decision']} (confidence: {recommendation['confidence']})",
        "Rationale:",
    ]
    lines.extend(f"- {item}" for item in recommendation["rationale"])
    lines.append("Evidence:")
    lines.extend(f"- {item['id']}: {item['kind']} from {item['source']}" for item in report["evidence"])
    if report["collection_status"]["issues"]:
        lines.append("Issues:")
        lines.extend(f"- {issue['collector']}: {issue['message']}" for issue in report["collection_status"]["issues"])
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read-only Intel hardware and OpenVINO environment advisor")
    parser.add_argument("--fixture", type=Path, help="Use a sanitized deterministic fixture")
    parser.add_argument("--validate-fixture", action="store_true", help="Validate a fixture without running discovery")
    parser.add_argument("--format", choices=("json", "text"), default="text")
    args = parser.parse_args(argv)
    try:
        profile = load_fixture(args.fixture) if args.fixture else collect_live()
    except ValueError:
        print("hardware-advisor: invalid or unsafe fixture", file=sys.stderr)
        return 2
    if args.validate_fixture:
        print("valid")
        return 0
    report = build_report(profile)
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(render_text(report), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
