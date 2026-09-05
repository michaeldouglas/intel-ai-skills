# Research Notes: Intel Hardware Advisor

## Decision 1: Optional runtime inspection

**Decision**: OpenVINO is an optional local signal. The probe attempts to load
the runtime only when it is installed, captures available device identifiers
and safe readable properties, and records an unavailable status when the import
or enumeration cannot complete.

**Rationale**: Basic platform discovery must remain useful on machines that do
not have OpenVINO installed. Treating an import failure as “no hardware” would
turn missing software into a false hardware conclusion.

**Constraint**: The first release does not claim model, precision, performance,
or memory support from an OpenVINO device name. Those claims require
version- and scope-matched evidence.

## Decision 2: Explicit evidence classes

**Decision**: Each fact and recommendation distinguishes detected local facts,
documented facts, measurements, estimates, inferences, and unavailable data.

**Rationale**: Hardware guidance is easy to overstate. A stable evidence class
lets users and evaluators see whether a value was observed locally or merely
described by documentation.

**Constraint**: The advisor may recommend a next verification step, but it may
not turn that step into a present capability claim.

## Decision 3: Deterministic fixture injection

**Decision**: Fixture mode supplies sanitized collector results to the same
report and recommendation code used by live mode. Fixtures describe outcomes,
not arbitrary commands to execute.

**Rationale**: Tests must run without Intel hardware, OpenVINO, network access,
or secrets and must reproduce failures consistently across Windows and Linux.

**Constraint**: Fixture validation rejects secret-like keys, user or machine
identifiers, and unexpected data outside the report input contract.

## Decision 4: Safe command execution

**Decision**: Live probes use explicit executable/argument arrays, bounded
timeouts, bounded output, and sanitized error status. Shell execution,
environment dumps, recursive filesystem scans, and automatic installation are
out of scope.

**Rationale**: Hardware discovery should be read-only and safe even when a tool
is missing or returns malformed output.

## Alternatives rejected

- **Third-party hardware inventory package**: rejected for the first skill
  because it adds installation and portability risk and would not remove the
  need for explicit uncertainty handling.
- **Benchmarking during discovery**: rejected because it changes the system,
  is machine-dependent, and exceeds the evidence needed for an initial advisor.
- **Device-name lookup table as a recommendation engine**: rejected because it
  cannot prove version, SKU scope, driver state, model compatibility, or
  precision support.

## OpenVINO 2026 documentation basis

Consulted on 2026-09-05 before this scope amendment:

- `docs/2026/about-openvino/release-notes-openvino/system-requirements.html` —
  platform, architecture, CPU/GPU/NPU operating-system scope, and driver
  caveats.
- `docs/2026/get-started/install-openvino/configurations.html` — additional
  GPU/NPU drivers, GenAI dependencies, and OpenCV scope.
- `docs/2026/get-started/install-openvino/configurations/configurations-intel-gpu.html` —
  OpenCL, Level Zero, Linux kernel, Windows, and WSL indicators.
- `docs/2026/get-started/install-openvino/configurations/configurations-intel-npu.html` —
  NPU driver and Linux/Windows setup indicators.

These pages define the evidence questions the advisor can surface. They are not
copied into the distributable skill; detailed support answers remain the job of
`intel-docs-reader`.
