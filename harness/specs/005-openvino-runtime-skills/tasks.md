# Tasks: OpenVINO Runtime Skills Suite

**Input**: Design documents from `/specs/005-openvino-runtime-skills/`

## Phase 1 — Specification and foundation

- [x] T001 Create the six candidate and six release skill directories.
- [x] T002 Define the common report contract and status vocabulary.
- [x] T003 [P] Create sanitized fixtures for each skill's success and blocked paths.
- [x] T004 [P] Create unit, integration, and contract test files for the suite.

## Phase 2 — Model converter

- [x] T005 [US1] Implement framework and input-shape profile selection.
- [x] T006 [US1] Implement plan/apply/verify and artifact-protection behavior.
- [x] T007 [US1] Write the converter skill instructions and documentation reference.

## Phase 3 — Inference runner

- [x] T008 [US2] Implement model/device/execution-context detection.
- [x] T009 [US2] Implement compile-only, inference, Docker, and verification profiles.
- [x] T010 [US2] Write the runner skill instructions and device-mode reference.

## Phase 4 — Benchmark and optimizer

- [x] T011 [US3] Implement benchmark configuration and measurement comparison.
- [x] T012 [US3] Write benchmark safety and evidence guidance.
- [x] T013 [US4] Implement quantization, compression, accuracy, and protected-output profiles.
- [x] T014 [US4] Write optimizer instructions and evidence boundaries.

## Phase 5 — Model Server and GenAI

- [x] T015 [US5] Implement OVMS Docker/model-repository/health/API profiles.
- [x] T016 [US5] Write local server safety and production boundary guidance.
- [x] T017 [US6] Implement GenAI workload/package/device/metric profiles.
- [x] T018 [US6] Write GenAI and NPU prerequisite guidance.

## Phase 6 — Integration and release

- [x] T019 Update English, Portuguese, and Spanish README catalogs and all-nine installation commands.
- [x] T020 Run structural validation on candidates and release copies.
- [x] T021 Run unit, integration, contract, full-suite, and quickstart tests.
- [x] T022 Run a read-only portability, privacy, and security review.
- [x] T023 Refresh Graphify and verify no temporary artifacts are staged.
- [x] T024 Promote only matching candidate files into `skills/` and commit locally.
