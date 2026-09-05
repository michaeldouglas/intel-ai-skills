# Quickstart: Intel Hardware Advisor

## Run live discovery

From the directory containing the promoted skill:

```powershell
python scripts/hardware_probe.py
python scripts/hardware_probe.py --format json
```

The command is read-only. OpenVINO is optional. Missing tools or unsupported
platforms appear in the report as explicit statuses.

## Run a deterministic fixture

Fixture execution is used by the harness and does not inspect the host:

```powershell
python scripts/hardware_probe.py --fixture ../../fixtures/hardware-advisor/windows-supported.json --format json
```

The promoted skill does not require the harness fixture directory; fixtures
are only for development and release validation.

## Interpret the result

- Start with `collection_status` to see whether discovery was complete or
  partial.
- Inspect `facts` and follow their `evidence_ids` into `evidence`.
- Inspect `runtime.additional_configurations` for lightweight GPU, NPU, GenAI,
  OpenCV, and WSL/container indicators. `incomplete` or `not_checked` means
  that a documented setup check is still required.
- Treat `recommendation.decision: no_decision` as the correct result when
  evidence is missing, conflicting, stale, or out of scope.
- A runtime-visible device is not by itself proof of model compatibility,
  precision support, performance, or memory savings.
