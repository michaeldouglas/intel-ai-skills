# Data Model: Intel Hardware Advisor

## Report

The top-level transport object. It is schema-versioned and preserves all
collection and recommendation uncertainty.

| Field | Type | Required | Meaning |
|---|---|---:|---|
| `schema_version` | string | yes | Report contract version, initially `1.0`. |
| `platform` | object | yes | Host platform facts, metadata, context, and status. |
| `runtime` | object | yes | Runtime facts, optional OpenVINO status, and lightweight additional-configuration checks. |
| `facts` | array | yes | Normalized observed facts. |
| `evidence` | array | yes | Sources and limitations linked by ID. |
| `recommendation` | object | yes | Qualified guidance or `no_decision`. |
| `collection_status` | object | yes | Overall and per-collector outcomes. |

## Fact

```text
id: stable string
name: normalized fact name
value: JSON scalar/object/array or null
status: detected | documented | measured | estimated | inferred |
         unavailable | unknown | unsupported | permission_denied | failed
source: collector or fixture source
evidence_ids: list of Evidence.id
scope: optional platform/runtime/version scope
```

`null` is required when a value is not available. A missing value is not
silently interpreted as false.

Platform metadata may include Linux distribution/version, kernel, normalized
architecture, OS version, and WSL/container context. These are observations,
not compatibility claims.

`runtime.additional_configurations` may contain `gpu`, `npu`, `genai`,
`opencv`, and `environment` entries. Each entry has a status, optional check
map, and concise notes. `configured` means only that the portable indicators
were observed; detailed driver and workload support remains documented evidence.

## Evidence

```text
id: stable string
kind: detected | documented | measured | estimate | inference
source: safe source label
version: optional version or null
scope: optional hardware/platform scope or null
limitations: list of strings
```

## Recommendation

```text
decision: guidance | no_decision
confidence: high | medium | low | none
rationale: list of concise statements
evidence_ids: list of Evidence.id
next_steps: list of safe verification actions
```

## Collection status

```text
status: complete | partial | unavailable | unsupported | failed
issues: list of {collector, status, message}
```

Messages contain safe diagnostic labels only; they do not include command
output, environment variables, arbitrary paths, or exception tracebacks.
