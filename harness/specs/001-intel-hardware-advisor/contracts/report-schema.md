# Report Contract: Intel Hardware Advisor v1

The machine-readable command output is a single JSON object with these
required top-level keys, in any JSON object order:

```json
{
  "schema_version": "1.0",
  "platform": {},
  "runtime": {},
  "facts": [],
  "evidence": [],
  "recommendation": {},
  "collection_status": {}
}
```

Required nested behavior:

- `facts` is always an array; each fact has `id`, `name`, `value`, `status`,
  `source`, and `evidence_ids`.
- `evidence` is always an array; each item has `id`, `kind`, `source`, and
  `limitations`.
- `recommendation` always has `decision`, `confidence`, `rationale`,
  `evidence_ids`, and `next_steps`.
- `collection_status` always has `status` and `issues`.
- `platform` may include `distribution`, `distribution_version`, `kernel`,
  `architecture`, `os_version`, and `context` without changing the top-level
  contract.
- `runtime.additional_configurations` may contain lightweight status entries
  for GPU, NPU, GenAI, OpenCV, and execution context.
- An unavailable or unknown value is represented with a non-success status and
  a null value where a value is expected.
- A report with insufficient evidence MUST use `decision: "no_decision"` and
  explain the gap in `rationale` or `next_steps`.

The text renderer is a presentation of this same object. It MUST retain the
recommendation decision, confidence, evidence classes, collection status, and
uncertainty messages.
