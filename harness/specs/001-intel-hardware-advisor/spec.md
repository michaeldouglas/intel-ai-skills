# Feature Specification: Intel Hardware Advisor

**Feature Branch**: `feature/adjustments`

**Created**: 2026-09-03

**Status**: Draft

**Input**: User description: "Create the first real Intel Hardware Advisor Agent Skill that detects local Intel inference hardware and OpenVINO runtime facts, reports evidence and uncertainty, and provides safe guidance."

## Scope amendment — 2026-09-05

The advisor remains a read-only first-diagnosis skill. It now covers Windows,
Linux, and macOS platform metadata, normalizes common CPU architectures, and
reports lightweight additional-configuration indicators for GPU, NPU, GenAI,
OpenCV, and WSL/container context. It does not install, repair, benchmark, or
replace the versioned OpenVINO documentation reader.

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.

  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - Inspect the local inference environment (Priority: P1)

As an AI practitioner, I want to inspect the local inference environment so that
I can understand which platform facts and runtime-visible devices are actually
available before choosing an inference path.

**Why this priority**: Reliable discovery is the minimum useful capability and
prevents recommendations from being based on assumptions.

**Independent Test**: Run the advisor against a sanitized supported-platform
fixture and confirm that the report contains platform facts, runtime facts,
evidence, and collection status without requiring physical Intel hardware.

**Acceptance Scenarios**:

1. **Given** a supported host with discoverable platform information, **When**
   the user runs the advisor, **Then** it returns a human-readable report with
   the detected facts and their collection status.
2. **Given** a supported host, **When** the user requests machine-readable
   output, **Then** the report contains stable fields for platform, runtime,
   facts, evidence, recommendation, and collection status.
3. **Given** that OpenVINO is unavailable, **When** the user runs the advisor,
   **Then** independent platform discovery still completes and OpenVINO facts
   are marked unavailable rather than inferred.

---

### User Story 2 - Receive qualified guidance (Priority: P2)

As an AI practitioner, I want guidance to be tied to evidence and confidence
so that I can distinguish a safe recommendation from an unresolved question.

**Why this priority**: Discovery is valuable, but users need a clear boundary
between what was detected, what is documented, and what remains uncertain.

**Independent Test**: Run the advisor with complete, incomplete, conflicting,
and out-of-scope evidence fixtures and verify that the recommendation changes
appropriately, including an explicit no-decision result.

**Acceptance Scenarios**:

1. **Given** sufficient version- and scope-matched evidence, **When** the
   profile is evaluated, **Then** the report presents guidance with the
   supporting evidence and its confidence.
2. **Given** missing, conflicting, stale, or out-of-scope evidence, **When**
   the profile is evaluated, **Then** the report presents an explicit
   no-decision or unknown result and explains the evidence gap.
3. **Given** a device name without capability evidence, **When** the profile is
   evaluated, **Then** the advisor does not claim model support, precision
   support, performance, or memory savings.

---

### User Story 3 - Validate without special hardware (Priority: P3)

As a maintainer, I want deterministic sanitized fixtures and failure scenarios
so that the skill can be tested in pull requests and on machines without Intel
hardware or OpenVINO.

**Why this priority**: Reproducible validation is required for portability and
prevents release readiness from depending on one physical machine.

**Independent Test**: Run the fixture and contract suites in an environment
without Intel hardware, internet access, or secrets and confirm stable results.

**Acceptance Scenarios**:

1. **Given** sanitized Windows, Linux, and macOS fixtures, **When** the test suite runs,
   **Then** both platforms produce schema-valid reports.
2. **Given** missing tools, permission failures, unsupported hardware, or
   incomplete runtime properties, **When** the test suite runs, **Then** the
   report marks the affected values unavailable or unknown without crashing.
3. **Given** fixture data containing machine-specific identifiers or secrets,
   **When** fixtures are validated, **Then** validation rejects or prevents
   those values from entering the distributable test set.

---

[Add more user stories as needed, each with an assigned priority]

### Edge Cases

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right edge cases.
-->

- A discovery command is missing, times out, returns malformed data, or exits
  with an error.
- The process lacks permission to read a supported system property.
- The host has no Intel GPU or NPU, or has an unsupported accelerator.
- OpenVINO is not installed, cannot enumerate a property, or reports a device
  that conflicts with independent platform facts.
- Evidence is incomplete, conflicting, stale, or outside its documented
  version or hardware scope.
- A fixture is malformed, contains unknown fields, or includes sensitive data.
- The host platform is unsupported or cannot be identified reliably.
- A supported device is visible but its driver, OpenCL/Level Zero runtime, or
  NPU device node cannot be verified by the portable probe.
- Optional GenAI/OpenCV packages are absent or have versions that were not
  checked.

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: The advisor MUST collect only read-only information required to
  describe the local inference environment.
- **FR-002**: The advisor MUST report platform facts separately from runtime
  facts.
- **FR-003**: The advisor MUST represent unavailable, unknown, unsupported, and
  permission-denied values explicitly.
- **FR-004**: The advisor MUST provide both human-readable and machine-readable
  report formats.
- **FR-005**: The machine-readable report MUST expose stable top-level fields
  for schema version, platform, runtime, facts, evidence, recommendation, and
  collection status.
- **FR-006**: Every detected fact MUST identify its source and collection
  status when that information is available.
- **FR-007**: OpenVINO information MUST be optional and MUST NOT prevent
  independent platform discovery when OpenVINO is absent.
- **FR-008**: The advisor MUST NOT infer device capabilities, model support,
  precision support, performance, throughput, or memory savings from a device
  name alone.
- **FR-009**: The advisor MUST distinguish detected facts, documented facts,
  measurements, estimates, and inferences in its guidance.
- **FR-010**: The advisor MUST return an explicit no-decision result when
  required evidence is missing, conflicting, stale, or out of scope.
- **FR-011**: The advisor MUST handle discovery failures without exposing
  secrets, arbitrary file contents, or unrelated environment data.
- **FR-012**: The fixture suite MUST cover supported platform profiles,
  missing tools, permission failures, unsupported hardware, and incomplete or
  conflicting runtime properties.
- **FR-013**: Fixtures MUST be sanitized and MUST NOT contain credentials,
  tokens, user names, machine identifiers, or arbitrary filesystem contents.
- **FR-014**: The distributable skill MUST operate from its promoted directory
  without requiring internal harness paths.
- **FR-015**: The release process MUST preserve the evidence and uncertainty
  fields when rendering or transporting a report.
- **FR-016**: The advisor MUST identify Windows, Linux, and macOS explicitly and
  MUST expose Linux distribution, kernel, operating-system version, and
  normalized architecture when available.
- **FR-017**: The runtime report MUST expose additional-configuration statuses
  for GPU, NPU, GenAI, OpenCV, and execution context without modifying the
  host or claiming workload compatibility.
- **FR-018**: Configuration statuses MUST distinguish configured, incomplete,
  not checked, not applicable, unavailable, and unknown outcomes.
- **FR-019**: Documented support and setup claims MUST remain sourced from
  versioned documentation; the local probe MUST NOT become a compatibility
  matrix or installation tool.

### Key Entities *(include if feature involves data)*

- **Environment Profile**: The observed host context, including platform,
  operating-system scope, and collection status.
- **Fact**: A detected property with a value, source, evidence class, and
  availability or confidence status.
- **Evidence**: A documented source, local measurement, or explicit inference
  tied to a fact or guidance statement, including version and scope when known.
- **Recommendation**: Guidance derived from the profile and evidence, with a
  confidence level, rationale, and explicit no-decision state when needed.
- **Collection Status**: The overall outcome of discovery, including complete,
  partial, unavailable, unsupported, or failed states.

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: A user can obtain a human-readable environment report in one
  command on each supported platform profile.
- **SC-002**: One hundred percent of deterministic supported-platform fixtures
  produce schema-valid machine-readable reports.
- **SC-003**: One hundred percent of failure fixtures preserve execution and
  label the affected information as unavailable, unknown, unsupported, or
  failed rather than fabricating a value.
- **SC-004**: One hundred percent of recommendation decisions include a
  rationale and evidence classification, or explicitly state no decision.
- **SC-005**: The deterministic validation suite completes without physical
  Intel hardware, OpenVINO installation, internet access, or secret access.
- **SC-006**: A promoted skill can be copied to a clean supported environment
  and run without resolving paths inside the engineering harness.
- **SC-007**: Supported-platform fixtures expose platform metadata and
  additional-configuration statuses without changing the existing top-level
  report contract.

## Assumptions

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right assumptions based on reasonable defaults
  chosen when the feature description did not specify certain details.
-->

- The primary users are AI practitioners and maintainers evaluating local
  inference readiness.
- The first release targets supported Windows, Linux, and macOS profiles;
  unsupported platforms return an explicit unsupported status.
- OpenVINO is an optional runtime signal, not a required dependency for basic
  platform discovery.
- Additional configurations are lightweight read-only indicators. Detailed
  support, driver, and version claims are answered from `intel-docs-reader` or
  another version- and scope-matched authoritative source.
- Recommendations are limited to version- and scope-matched evidence available
  to the skill; universal benchmark or compatibility claims are out of scope.
- Live hardware validation is supplemental; deterministic sanitized fixtures
  are the release gate.
- The first release exposes a command-line entry point and structured output;
  GUI, remote inventory, telemetry, and automatic installation are out of
  scope.
