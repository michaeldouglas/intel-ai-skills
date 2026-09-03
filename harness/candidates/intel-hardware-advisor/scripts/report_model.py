"""Stable report model and conservative recommendation policy for the skill."""

from __future__ import annotations

from typing import Any


REQUIRED_TOP_LEVEL = (
    "schema_version",
    "platform",
    "runtime",
    "facts",
    "evidence",
    "recommendation",
    "collection_status",
)
VALID_STATUSES = {
    "detected",
    "documented",
    "measured",
    "estimated",
    "inferred",
    "unavailable",
    "unknown",
    "unsupported",
    "permission_denied",
    "failed",
}
VALID_EVIDENCE_KINDS = {"detected", "documented", "measured", "estimate", "inference"}


def _text(value: Any, default: str = "") -> str:
    return value if isinstance(value, str) else default


def _evidence(
    evidence_id: str,
    kind: str,
    source: str,
    limitations: list[str] | None = None,
    version: str | None = None,
) -> dict[str, Any]:
    return {
        "id": evidence_id,
        "kind": kind,
        "source": source,
        "version": version,
        "scope": None,
        "limitations": limitations or [],
    }


def _fact(
    fact_id: str,
    name: str,
    value: Any,
    status: str,
    source: str,
    evidence_ids: list[str],
    scope: str | None = None,
) -> dict[str, Any]:
    return {
        "id": fact_id,
        "name": name,
        "value": value,
        "status": status,
        "source": source,
        "evidence_ids": evidence_ids,
        "scope": scope,
    }


def build_recommendation(facts: list[dict[str, Any]], evidence: list[dict[str, Any]]) -> dict[str, Any]:
    """Return guidance only when evidence supports a bounded conclusion."""
    device_facts = [fact for fact in facts if fact.get("name", "").startswith("runtime.device.")]
    vendor_facts = [fact for fact in facts if fact.get("name", "").endswith(".vendor")]
    evidence_by_id = {item.get("id"): item for item in evidence}
    related_evidence = list(dict.fromkeys(
        evidence_id
        for fact in device_facts + vendor_facts
        for evidence_id in fact.get("evidence_ids", [])
        if evidence_id in evidence_by_id
    ))

    vendors = {
        _text(fact.get("value")).strip().lower()
        for fact in vendor_facts
        if fact.get("status") == "detected" and _text(fact.get("value")).strip()
    }
    runtime_available = any(
        fact.get("name") == "runtime.openvino" and fact.get("status") == "detected" for fact in facts
    )
    if len(vendors) > 1:
        return {
            "decision": "no_decision",
            "confidence": "none",
            "rationale": ["Vendor evidence conflicts across the supplied sources."],
            "evidence_ids": related_evidence,
            "next_steps": ["Re-run discovery and verify the device vendor from an authoritative source."],
        }

    if not vendors:
        rationale = "Vendor or capability evidence is missing; a device name alone is insufficient."
        if not runtime_available:
            rationale += " OpenVINO runtime evidence is unavailable."
        return {
            "decision": "no_decision",
            "confidence": "none",
            "rationale": [rationale],
            "evidence_ids": related_evidence,
            "next_steps": ["Collect version- and scope-matched vendor and runtime capability evidence."],
        }

    if "intel" not in vendors:
        return {
            "decision": "no_decision",
            "confidence": "low",
            "rationale": ["The supplied evidence does not confirm an Intel device for this advisor."],
            "evidence_ids": related_evidence,
            "next_steps": ["Use the hardware vendor documentation to determine the supported inference path."],
        }

    rationale = ["Local evidence confirms an Intel device is visible to the inspected profile."]
    next_steps = ["Verify model, precision, driver, and device support for the intended workload."]
    if runtime_available:
        rationale.append("OpenVINO is available in the profile, but visibility does not prove model compatibility.")
        confidence = "medium"
    else:
        rationale.append("OpenVINO is not available, so runtime compatibility remains unresolved.")
        next_steps.insert(0, "Install or inspect the intended runtime according to its official documentation.")
        confidence = "low"
    return {
        "decision": "guidance",
        "confidence": confidence,
        "rationale": rationale,
        "evidence_ids": related_evidence,
        "next_steps": next_steps,
    }


def build_report(profile: dict[str, Any]) -> dict[str, Any]:
    """Build a deterministic report from live or fixture-shaped collector data."""
    platform_input = profile.get("platform", {})
    runtime_input = profile.get("runtime", {})
    openvino = runtime_input.get("openvino", {})
    platform_status = _text(platform_input.get("status"), "detected")
    openvino_status = _text(openvino.get("status"), "unavailable")
    platform_evidence_id = "ev.platform"
    openvino_evidence_id = "ev.openvino"
    evidence = [
        _evidence(
            platform_evidence_id,
            "detected",
            "local platform collector",
            ["Values describe the current host and are not a compatibility guarantee."],
        ),
        _evidence(
            openvino_evidence_id,
            "detected",
            "local OpenVINO collector",
            ["Runtime visibility does not establish model or precision support."],
            version=_text(openvino.get("version")) or None,
        ),
    ]
    facts: list[dict[str, Any]] = []

    for name, key in (("platform.system", "system"), ("platform.release", "release"), ("platform.machine", "machine")):
        value = platform_input.get(key)
        status = platform_status if value not in (None, "") else "unknown"
        facts.append(_fact(name, name, value, status, "platform", [platform_evidence_id]))

    openvino_version = openvino.get("version")
    facts.append(
        _fact(
            "runtime.openvino",
            "runtime.openvino",
            openvino_version,
            "detected" if openvino_status == "available" else openvino_status,
            "openvino",
            [openvino_evidence_id],
        )
    )
    devices = openvino.get("devices") if isinstance(openvino.get("devices"), list) else []
    for index, device in enumerate(devices):
        if not isinstance(device, dict):
            continue
        device_id = _text(device.get("id"), f"device-{index}")
        safe_id = "".join(character if character.isalnum() else "_" for character in device_id).lower()
        fact_id = f"runtime.device.{safe_id or index}"
        device_status = _text(device.get("status"), "detected")
        device_name = device.get("name") or device.get("id")
        facts.append(_fact(fact_id, fact_id, device_name, device_status, "openvino", [openvino_evidence_id]))
        vendor = device.get("vendor")
        if vendor:
            facts.append(
                _fact(f"{fact_id}.vendor", f"{fact_id}.vendor", vendor, "detected", "openvino", [openvino_evidence_id])
            )

    collector_status = profile.get("collector_status", {})
    issues = []
    statuses = []
    for collector, status in (
        ("platform", platform_status),
        ("openvino", openvino_status),
    ):
        explicit = collector_status.get(collector) if isinstance(collector_status, dict) else None
        current = _text(explicit, status)
        statuses.append(current)
        if current not in {"complete", "detected", "available"}:
            issues.append({"collector": collector, "status": current, "message": f"{collector} collection is {current}."})

    if platform_status == "unsupported":
        overall = "unsupported"
    elif all(status in {"complete", "detected", "available"} for status in statuses):
        overall = "complete"
    elif any(status in {"failed", "permission_denied"} for status in statuses):
        overall = "failed" if platform_status in {"failed", "permission_denied"} else "partial"
    else:
        overall = "partial"

    report = {
        "schema_version": "1.0",
        "platform": {
            "system": platform_input.get("system"),
            "release": platform_input.get("release"),
            "machine": platform_input.get("machine"),
            "status": platform_status,
        },
        "runtime": {
            "openvino": {
                "status": openvino_status,
                "version": openvino_version,
                "devices": [
                    {"id": item.get("id"), "name": item.get("name"), "status": item.get("status", "detected")}
                    for item in devices
                    if isinstance(item, dict)
                ],
            }
        },
        "facts": facts,
        "evidence": evidence,
        "recommendation": build_recommendation(facts, evidence),
        "collection_status": {"status": overall, "issues": issues},
    }
    validate_report(report)
    return report


def validate_report(report: dict[str, Any]) -> None:
    if not isinstance(report, dict) or set(report) != set(REQUIRED_TOP_LEVEL):
        raise ValueError("report does not match the v1 top-level contract")
    if report["schema_version"] != "1.0":
        raise ValueError("unsupported report schema")
    if not isinstance(report["platform"], dict) or not isinstance(report["runtime"], dict):
        raise ValueError("platform and runtime must be objects")
    if not isinstance(report["facts"], list) or not isinstance(report["evidence"], list):
        raise ValueError("facts and evidence must be arrays")
    evidence_ids = {item.get("id") for item in report["evidence"] if isinstance(item, dict)}
    for fact in report["facts"]:
        if not isinstance(fact, dict) or not {"id", "name", "value", "status", "source", "evidence_ids"}.issubset(fact):
            raise ValueError("fact does not match the report contract")
        if fact["status"] not in VALID_STATUSES:
            raise ValueError("fact has an invalid status")
        if not set(fact["evidence_ids"]).issubset(evidence_ids):
            raise ValueError("fact references missing evidence")
    for item in report["evidence"]:
        if not isinstance(item, dict) or not {"id", "kind", "source", "limitations"}.issubset(item):
            raise ValueError("evidence does not match the report contract")
        if item["kind"] not in VALID_EVIDENCE_KINDS or not isinstance(item["limitations"], list):
            raise ValueError("evidence has an invalid shape")
    recommendation = report["recommendation"]
    if not isinstance(recommendation, dict) or not {"decision", "confidence", "rationale", "evidence_ids", "next_steps"}.issubset(recommendation):
        raise ValueError("recommendation does not match the report contract")
    if recommendation["decision"] not in {"guidance", "no_decision"} or recommendation["confidence"] not in {
        "high", "medium", "low", "none"
    }:
        raise ValueError("recommendation has an invalid decision")
    if not set(recommendation["evidence_ids"]).issubset(evidence_ids):
        raise ValueError("recommendation references missing evidence")
    collection = report["collection_status"]
    if not isinstance(collection, dict) or not {"status", "issues"}.issubset(collection) or not isinstance(collection["issues"], list):
        raise ValueError("collection status does not match the report contract")
    if collection["status"] not in {"complete", "partial", "unavailable", "unsupported", "failed"}:
        raise ValueError("collection status has an invalid value")
