# Tasks: Intel Hardware Advisor

**Input**: Design documents from `specs/001-intel-hardware-advisor/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, and `contracts/report-schema.md`

**Tests**: Included because deterministic validation and release gates are explicit feature requirements.

## Phase 1: Setup

**Purpose**: Create the isolated candidate, fixture, test, and evaluation layout.

- [X] T001 Create candidate directories `candidates/intel-hardware-advisor/scripts` and `candidates/intel-hardware-advisor/references`
- [X] T002 [P] Create harness directories `fixtures/hardware-advisor`, `tests/unit`, `tests/contract`, `tests/integration`, and `evaluations/intel-hardware-advisor`
- [X] T003 [P] Add candidate operating instructions in `candidates/intel-hardware-advisor/SKILL.md` with invocation, safety, evidence, and interpretation rules
- [X] T004 [P] Add the candidate evidence policy in `candidates/intel-hardware-advisor/references/evidence-guide.md`

## Phase 2: Foundational

**Purpose**: Establish the report contract, safe normalization, and fixture boundary before story implementation.

- [X] T005 [P] [US1] Write report model and validation primitives in `candidates/intel-hardware-advisor/scripts/report_model.py`
- [X] T006 [P] [US1] Write the v1 contract assertions in `tests/contract/test_hardware_advisor_contract.py` before implementation
- [X] T007 [P] [US3] Write fixture safety tests in `tests/test_fixture_safety.py` covering secret-like keys, machine identifiers, and malformed root data
- [X] T008 [US1] Define the candidate-only import and command entry conventions in `candidates/intel-hardware-advisor/scripts/hardware_probe.py`

**Checkpoint**: Contract and safety tests exist; user-story implementation may proceed.

## Phase 3: User Story 1 - Inspect the local inference environment (Priority: P1)

**Goal**: Produce stable text and JSON reports from deterministic fixtures and conservative live discovery.

**Independent Test**: Run the CLI against Windows and Linux supported fixtures and assert platform, runtime, facts, evidence, and collection status are present.

### Tests first

- [X] T009 [P] [US1] Write unit tests for platform/runtime normalization and unavailable states in `tests/unit/test_hardware_advisor.py`
- [X] T010 [P] [US1] Write CLI integration tests for JSON and text output in `tests/integration/test_hardware_advisor_cli.py`

### Implementation

- [X] T011 [US1] Implement bounded, shell-free command execution and safe error mapping in `candidates/intel-hardware-advisor/scripts/hardware_probe.py`
- [X] T012 [US1] Implement platform collectors for Windows/Linux and explicit unsupported status in `candidates/intel-hardware-advisor/scripts/hardware_probe.py`
- [X] T013 [US1] Implement optional OpenVINO runtime collection with isolated unavailable/failed states in `candidates/intel-hardware-advisor/scripts/hardware_probe.py`
- [X] T014 [US1] Implement fixture loading with strict shape validation and deterministic report generation in `candidates/intel-hardware-advisor/scripts/hardware_probe.py`
- [X] T015 [US1] Implement `--format json` and `--format text` rendering while preserving evidence and uncertainty in `candidates/intel-hardware-advisor/scripts/hardware_probe.py`
- [X] T016 [US1] Add sanitized supported Windows and Linux fixtures in `fixtures/hardware-advisor/windows-supported.json` and `fixtures/hardware-advisor/linux-supported.json`
- [X] T017 [US1] Run the independent User Story 1 contract, unit, and integration tests and record the result in `evaluations/intel-hardware-advisor/README.md`

**Checkpoint**: A user can inspect a fixture or live host without a missing optional runtime causing a crash.

## Phase 4: User Story 2 - Receive qualified guidance (Priority: P2)

**Goal**: Return evidence-linked guidance only when the profile supports a bounded conclusion.

**Independent Test**: Complete, incomplete, and conflicting fixtures produce guidance or an explicit no-decision result with rationale.

### Tests first

- [X] T018 [P] [US2] Write recommendation unit tests for sufficient, missing, device-name-only, stale, and conflicting evidence in `tests/unit/test_hardware_advisor.py`
- [X] T019 [P] [US2] Add scenario expectations for qualified guidance and no-decision behavior in `evaluations/intel-hardware-advisor/scenarios.json`

### Implementation

- [X] T020 [US2] Implement evidence-linked recommendation policy in `candidates/intel-hardware-advisor/scripts/report_model.py`
- [X] T021 [US2] Add explicit next-step guidance and no-capability-claim guardrails in `candidates/intel-hardware-advisor/SKILL.md`
- [X] T022 [US2] Add missing-runtime, conflicting-evidence, and unsupported fixtures in `fixtures/hardware-advisor/openvino-missing.json`, `fixtures/hardware-advisor/conflicting-evidence.json`, and `fixtures/hardware-advisor/unsupported-platform.json`
- [X] T023 [US2] Evaluate all recommendation scenarios and document expected evidence classes in `evaluations/intel-hardware-advisor/README.md`

**Checkpoint**: The advisor never turns a device name into an unsupported capability claim.

## Phase 5: User Story 3 - Validate without special hardware (Priority: P3)

**Goal**: Make negative paths deterministic, sanitized, and suitable for pull-request gates.

**Independent Test**: All fixture files validate and all failure scenarios produce schema-valid reports without hardware, internet, or secrets.

### Tests first

- [X] T024 [P] [US3] Write failure-path tests for missing tools, permission denial, malformed output, and unsupported hardware in `tests/unit/test_hardware_advisor.py`
- [X] T025 [P] [US3] Write fixture-to-report integration coverage for every fixture in `tests/integration/test_hardware_advisor_cli.py`

### Implementation

- [X] T026 [US3] Add permission-failure and malformed-sensitive fixtures in `fixtures/hardware-advisor/permission-failure.json` and `fixtures/hardware-advisor/malformed-sensitive.json`
- [X] T027 [US3] Add a deterministic fixture validator in `candidates/intel-hardware-advisor/scripts/hardware_probe.py`
- [X] T028 [US3] Add fixture validation and clean-copy checks to `tests/test_fixture_safety.py`
- [X] T029 [US3] Complete evaluation scenario coverage and release limitations in `evaluations/intel-hardware-advisor/scenarios.json` and `evaluations/intel-hardware-advisor/README.md`

**Checkpoint**: The full deterministic suite passes on a machine without Intel hardware or OpenVINO.

## Phase 6: Polish and release readiness

- [X] T030 [P] [US1] Update `candidates/README.md` with the candidate validation command and promotion boundary
- [X] T031 [P] [US1] Validate `specs/001-intel-hardware-advisor/quickstart.md` against the candidate CLI
- [X] T032 [US3] Run the complete test suite and candidate structural checks from the repository root
- [X] T033 [US3] Perform a read-only portability, privacy, and release-readiness review of `candidates/intel-hardware-advisor`
- [X] T034 [US3] Run `graphify update .` after product and harness artifacts are complete

## Dependencies and execution order

- Phase 1 precedes Phase 2; Phase 2 blocks all user stories.
- US1 establishes the report and collection path. US2 depends on the report
  model but does not change the discovery safety boundary. US3 validates both.
- Within each story, tests are written before the implementation they cover.
- T005-T007 may run in parallel; T009-T010 may run in parallel; T018-T019
  may run in parallel; T024-T025 may run in parallel.
- Promotion to `skills/intel-hardware-advisor/` is not part of this task list;
  it requires the release-manager gate after review approval.
