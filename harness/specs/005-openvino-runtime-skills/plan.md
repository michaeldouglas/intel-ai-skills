# Implementation Plan: OpenVINO Runtime Skills Suite

## Architecture

Create six independent candidate directories under `harness/candidates/` and
matching release directories under the sibling `skills/` directory. Each
candidate contains a concise `SKILL.md`, one executable standard-library script,
and one focused reference file. Fixture-driven tests exercise the same report
contracts without requiring OpenVINO, Docker, NNCF, OVMS, or GenAI packages on
the test host.

## Report contract

All scripts expose `--mode plan|apply|verify` where mutation is relevant and
`--format json|text`. The stable top-level report is:

```text
schema_version
collection_status
context
request
selection
plan
execution
verification
warnings
issues
```

Fixture input can provide deterministic command results and verification values.
Live execution is conservative, bounded, redacted, and never performs driver,
BIOS, global environment, or arbitrary cleanup actions.

## Skill-specific implementation

- Converter: framework profile selection, output artifact plan, shape handling,
  conversion command preview, and fixture verification.
- Inference runner: model/device context, compile-only or inference plan,
  local/Docker context, device selection, and verification report.
- Benchmark: benchmark configuration, tool selection, fixture measurements,
  comparison, and limitations.
- Optimizer: optimization profile selection, protected output directory,
  accuracy-validation warning, and fixture result.
- Model Server: OVMS Docker plan, model repository/ports/volumes, health/API
  verification, and no-delete safety boundary.
- GenAI runner: workload profile selection, package/model prerequisites,
  device context, generation metrics, and NPU boundary reporting.

## Documentation integration

Add concise catalog rows and grouped workflow descriptions to the English,
Portuguese, and Spanish public READMEs. Keep the README installation command
usable with all nine skills while leaving detailed behavior in each skill.

## Quality strategy

Run structural validation for all candidates and release copies, unit tests for
selection and redaction, integration tests for CLI/report behavior, contract
tests for all six stable interfaces, full repository tests, Graphify update, and
a read-only final scan for internal paths and temporary artifacts.
