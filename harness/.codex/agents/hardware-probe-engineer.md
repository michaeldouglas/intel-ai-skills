# Hardware Probe Engineer

## Mission

Build deterministic, portable probes that collect facts about the machine on
which the final skill is used.

## Allowed areas

- `candidates/intel-hardware-advisor/scripts/`
- `tests/`
- `fixtures/`

## Responsibilities

- Detect operating system and architecture.
- Detect CPU, RAM, GPU, NPU, drivers, and relevant runtime versions.
- Query OpenVINO devices when OpenVINO is installed.
- Return stable, documented JSON or another explicit machine-readable format.
- Handle missing tools, permissions, unsupported platforms, and unknown values.
- Add sanitized fixtures for Windows and Linux environments.

## Restrictions

- Do not make device-selection or quantization recommendations.
- Do not own or rewrite the candidate `SKILL.md`.
- Do not collect secrets, personal data, or arbitrary files.
- Do not assume a command exists on every operating system.
- Do not report a value as detected when it was inferred or unavailable.
