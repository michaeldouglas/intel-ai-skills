---
name: intel-hardware-advisor
description: Inspect a local Windows or Linux inference environment, optionally discover OpenVINO runtime visibility, and provide evidence-aware Intel hardware guidance without inventing compatibility or performance claims.
---

# Intel Hardware Advisor

Use this skill when a user needs to understand the local inference environment
before selecting an Intel execution path. It is designed for first diagnosis:
read-only discovery, explicit uncertainty, and safe next steps.

## Run it

From the directory containing this skill:

```text
python scripts/hardware_probe.py
python scripts/hardware_probe.py --format json
```

The JSON report is the stable interface. Text output is a human-friendly view
of the same report and must not be treated as a different source of truth.

## Interpret it

1. Read `collection_status` first. `partial`, `unavailable`, `unsupported`,
   and `failed` are valid outcomes, not reasons to fill in missing facts.
2. Separate `platform` facts from `runtime` facts. A host operating system or
   runtime-visible device does not establish support for a specific workload.
3. Follow each fact's `evidence_ids` into `evidence`. Keep detected,
   documented, measured, estimated, and inferred information distinct.
4. Use `recommendation` only within its stated confidence and rationale.
   `decision: no_decision` is required when evidence is absent, conflicting,
   stale, or outside the relevant version and hardware scope.

## Safety boundaries

- Discovery is read-only and does not install packages, change drivers, run
  benchmarks, or scan arbitrary files.
- OpenVINO is optional. Its absence does not prove that the host has no Intel
  hardware, and its device list does not prove model or precision support.
- Never claim compatibility, throughput, latency, memory savings, or a
  supported precision from a device name alone.
- Do not request, print, or persist credentials, tokens, serial numbers, user
  names, environment dumps, or unrelated filesystem contents.
- When a user asks for a stronger claim, ask for version- and scope-matched
  authoritative documentation or a reproducible measurement.

## Maintainer validation

The project runs this skill with sanitized fixtures. A fixture is a test input,
not a runtime dependency of the promoted skill:

```text
python scripts/hardware_probe.py --fixture <fixture.json> --format json
```

The release candidate must remain self-contained when copied to the sibling
`skills/` directory. Promotion requires the project quality gates and a
read-only review.
