# Implementation Plan: Intel Hardware Advisor

**Branch**: `feature/adjustments` | **Date**: 2026-09-03 | **Spec**: [spec.md](./spec.md)

## Summary

Build the first distributable Agent Skill as a self-contained, read-only
hardware and runtime advisor. The skill will collect conservative platform
facts, optionally inspect OpenVINO runtime visibility, preserve collection
status and evidence, and emit a stable JSON report or a concise human-readable
report. Deterministic Windows and Linux fixtures will exercise successful,
partial, unsupported, permission-failure, malformed, and conflicting cases so
release validation never depends on physical hardware.

## Technical Context

**Language/Version**: Python 3.13.7+

**Primary Dependencies**: Python standard library only for the promoted skill;
OpenVINO is an optional runtime discovered at execution time. Pytest is used
by the harness when available, with standard-library-compatible test modules.

**Storage**: No persistent storage. Input fixtures are JSON files used only by
the harness and are not runtime state.

**Testing**: Contract tests for the JSON schema, unit tests for collection and
recommendation behavior, integration tests for the CLI, fixture validation, and
scenario evaluations.

**Target Platform**: Windows and Linux first; unsupported platforms return an
explicit status.

**Project Type**: Self-contained command-line Agent Skill with Python helper
scripts and Markdown operating instructions.

**Performance Goals**: Fixture-mode execution completes in under two seconds;
live discovery uses bounded command timeouts and never waits indefinitely.

**Constraints**: Read-only discovery, no shell interpolation, bounded output,
no secrets or arbitrary file collection, offline-capable fixture validation,
and no dependency on `harness/`, `.codex/`, or `.agents/` after promotion.

**Scale/Scope**: One local host profile, a small stable report contract, two
supported platform fixture families, and evidence-aware guidance for first
diagnosis. Remote inventory, telemetry, benchmarks, installation, and model
execution are out of scope.

## Constitution Check

*GATE: Pass before research and re-check after design.*

- **Evidence-first**: PASS. Facts carry source, status, and evidence class;
  recommendation logic refuses unsupported capability claims.
- **Portable and deterministic**: PASS. The product has no third-party
  dependency, uses relative/self-contained paths, and fixture mode isolates
  platform behavior from the host.
- **Test-first**: PASS. Tasks put contract, unit, integration, fixture, and
  evaluation tests before or alongside each implementation slice.
- **Privacy and safe discovery**: PASS. Probes are read-only, command arguments
  are explicit, outputs are bounded, and fixture validation checks sensitive
  fields.
- **Review-gated release**: PASS with release deferred. This plan creates a
  candidate under `candidates/`; promotion to sibling `skills/` remains a later
  quality-review and release-manager action.

## Research Decisions

See [research.md](./research.md) for the decision log. The main decisions are:

1. Use a small standard-library probe layer with injected command results so
   live discovery and deterministic fixtures share the same report builder.
2. Treat OpenVINO as an optional signal. Import failure is a report state, not
   a fatal error and not evidence that no hardware exists.
3. Keep recommendation policy intentionally conservative: a device name alone
   can never establish vendor, capability, compatibility, precision support,
   performance, or memory savings.
4. Make the report contract explicit and versioned before implementation.

## Data and Contract Design

See [data-model.md](./data-model.md) and [contracts/report-schema.md](./contracts/report-schema.md).

The report has stable top-level fields: `schema_version`, `platform`,
`runtime`, `facts`, `evidence`, `recommendation`, and `collection_status`.
Unknown and unavailable values are represented by status-bearing objects, never
by fabricated strings or omitted context.

## Project Structure

### Documentation

```text
specs/001-intel-hardware-advisor/
├── spec.md
├── checklists/requirements.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/report-schema.md
└── tasks.md
```

### Product candidate and harness

```text
candidates/intel-hardware-advisor/
├── SKILL.md
├── scripts/
│   ├── hardware_probe.py
│   └── report_model.py
└── references/
    └── evidence-guide.md

fixtures/hardware-advisor/
├── windows-supported.json
├── linux-supported.json
├── openvino-missing.json
├── permission-failure.json
├── unsupported-platform.json
├── conflicting-evidence.json
└── malformed-sensitive.json

tests/
├── contract/test_hardware_advisor_contract.py
├── integration/test_hardware_advisor_cli.py
├── unit/test_hardware_advisor.py
└── test_fixture_safety.py

evaluations/intel-hardware-advisor/
├── scenarios.json
└── README.md
```

**Structure Decision**: Use the existing skill-factory layout. Product files
remain under `candidates/` and import only their own sibling scripts. Fixtures,
tests, and evaluations remain harness-owned and are never required by the
promoted skill.

## Implementation Notes

- The CLI accepts `--fixture` for deterministic validation and otherwise runs
  conservative live discovery.
- `--format json` is the machine contract; `--format text` renders the same
  report without dropping evidence or uncertainty.
- The command runner uses argument arrays, a timeout, an output cap, and
  redacted failure metadata. It never invokes a shell or dumps the environment.
- OpenVINO collection is isolated from platform collection and records only
  runtime-visible device identifiers and explicitly readable properties.
- Recommendation output includes `decision`, `confidence`, `rationale`, and
  `evidence_ids`; when evidence is insufficient, `decision` is `no_decision`.

## Complexity Tracking

No constitution violations. The design deliberately avoids a package manager,
database, service layer, or remote inventory system because none is required by
the first skill and each would weaken portability or deterministic validation.
