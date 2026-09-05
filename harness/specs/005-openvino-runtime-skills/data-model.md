# Data Model: OpenVINO Runtime Skills Suite

## Common report

| Field | Meaning |
|---|---|
| `schema_version` | Version of the script report contract |
| `collection_status` | `complete`, `partial`, `blocked`, or `failed` |
| `context` | Sanitized OS, architecture, execution context, tools, and permissions |
| `request` | User-selected workflow, model, device, version, and options |
| `selection` | Chosen profile and reason, with alternatives when available |
| `plan` | Read-only actions, prerequisites, confirmation requirement, warnings |
| `execution` | `not_run`, `passed`, `partial`, `blocked`, or `failed` plus redacted results |
| `verification` | Runtime/model/device/API/measurement results |
| `warnings` | Non-blocking version, accuracy, performance, or prerequisite notes |
| `issues` | Actionable blockers or failures without secrets |

## Skill-specific entities

- **Conversion request**: framework, source model, output directory, input
  shapes, precision, and requested version.
- **Inference request**: model path, device mode, execution context, input
  payload policy, compile-only flag, and verification scope.
- **Benchmark request**: model, device, iterations, warmup, batch, streams,
  performance hint, and comparison set.
- **Optimization request**: method, calibration source, accuracy policy, output
  directory, and artifact-protection policy.
- **Server request**: image/version, model repository, model name/version,
  ports, volumes, device, and health/API checks.
- **GenAI request**: workload type, model asset, package profile, device,
  generation parameters, and requested metrics.
