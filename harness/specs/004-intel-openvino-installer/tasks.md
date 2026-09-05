# Tasks: Intel OpenVINO Installer

**Input**: Design documents from `/specs/004-intel-openvino-installer/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md,
contracts/installation-plan.md, quickstart.md

**Tests**: Required by the project constitution and feature specification.

## Phase 1: Setup

- [x] T001 Create the candidate and release skill directories with `SKILL.md`, `references/installation-methods.md`, and `scripts/openvino_installer.py`.
- [x] T002 Create sanitized environment, method, and failure fixture directories under `fixtures/openvino-installer/`.
- [x] T003 [P] Create the unit, integration, and contract test files under `tests/` for the installer report contract.

## Phase 2: Foundational

- [x] T004 Define the installation report schema and status vocabulary in `harness/candidates/intel-openvino-installer/scripts/openvino_installer.py` and synchronize the release copy.
- [x] T005 [P] Add the versioned method matrix and official documentation references to `harness/candidates/intel-openvino-installer/references/installation-methods.md` and synchronize the release copy.
- [x] T006 [P] Add the plan/apply/verify safety rules and standalone boundaries to both `SKILL.md` files.
- [x] T007 Implement sanitized command execution, environment detection, and fixture loading in `harness/candidates/intel-openvino-installer/scripts/openvino_installer.py`.

## Phase 3: User Story 1 - Python installation MVP (Priority: P1)

**Goal**: Plan, confirm, execute and verify a Python/Pip installation without
requiring a second skill.

**Independent Test**: A Windows, Linux or macOS Python fixture produces a plan
without mutation; a fake command runner applies it and verifies the runtime.

- [x] T008 [P] [US1] Add positive and negative Python environment fixtures in `fixtures/openvino-installer/environments/` and `fixtures/openvino-installer/failures/`.
- [x] T009 [P] [US1] Add unit tests for Python method selection, version handling, confirmation gating, and sanitized failures in `tests/unit/test_openvino_installer.py`.
- [x] T010 [US1] Implement Python virtual-environment and Pip planning in `harness/candidates/intel-openvino-installer/scripts/openvino_installer.py`.
- [x] T011 [US1] Implement confirmation-gated apply mode and Python/OpenVINO verification in `harness/candidates/intel-openvino-installer/scripts/openvino_installer.py`.
- [x] T012 [US1] Add the user-facing standalone workflow and safety instructions to both `SKILL.md` files.

## Phase 4: User Story 2 - Platform and ecosystem methods (Priority: P1)

**Goal**: Select one compatible documented method for native OS, Conda, Docker,
npm, C++ package managers, or Yocto contexts.

**Independent Test**: Each method fixture produces the expected method, commands,
prerequisites, alternatives and no unintended cross-ecosystem commands.

- [x] T013 [P] [US2] Add method-selection fixtures for APT, YUM, Zypper, WinGet, Homebrew, archive, Conda, Docker, npm, vcpkg, Conan, and Yocto in `fixtures/openvino-installer/methods/`.
- [x] T014 [P] [US2] Add integration tests for method routing and unsupported contexts in `tests/integration/test_openvino_installer_cli.py`.
- [x] T015 [US2] Implement native package-manager and archive method profiles in `harness/candidates/intel-openvino-installer/scripts/openvino_installer.py`.
- [x] T016 [US2] Implement Conda, Docker, npm, vcpkg, Conan, Yocto, and source-build planning profiles without host mutation in `harness/candidates/intel-openvino-installer/scripts/openvino_installer.py`.
- [x] T017 [US2] Add method-specific prerequisites, alternatives, and version-status guidance to `references/installation-methods.md` in both copies.

## Phase 5: User Story 3 - Optional components and failure handling (Priority: P2)

**Goal**: Handle GenAI and optional integrations while reporting driver and
permission blockers without installing drivers automatically.

**Independent Test**: GenAI, missing-manager, permission, network, driver and
post-install verification fixtures produce distinct safe outcomes.

- [x] T018 [P] [US3] Add GenAI and failure fixtures in `fixtures/openvino-installer/methods/` and `fixtures/openvino-installer/failures/`.
- [x] T019 [P] [US3] Add contract tests for optional components, driver boundaries, and sanitized command output in `tests/contract/test_openvino_installer_contract.py`.
- [x] T020 [US3] Implement optional GenAI and framework-extra planning and verification in `harness/candidates/intel-openvino-installer/scripts/openvino_installer.py`.
- [x] T021 [US3] Implement failure classification, redaction, partial verification, and driver/NPU/GPU boundary reporting in `harness/candidates/intel-openvino-installer/scripts/openvino_installer.py`.

## Phase 6: Polish and release review

- [x] T022 [P] Synchronize candidate and release copies and verify the release copy has no harness references.
- [x] T023 [P] Run structural validation, unit/integration/contract tests, fixture safety checks, and the quickstart scenarios.
- [x] T024 Run Graphify update and complete the read-only portability, security, and release-readiness review.
- [x] T025 Update the public English, Portuguese and Spanish README skill catalog with `intel-openvino-installer` after release approval.

## Dependencies and Execution Order

- Phase 1 precedes all other phases.
- Phase 2 blocks all user-story phases.
- US1 is the MVP and must pass before expanding to the method matrix.
- US2 depends on the report contract and command runner from Phase 2, but not on optional GenAI work.
- US3 depends on the verification and redaction helpers from US1.
- Polish follows all desired user stories and precedes promotion.

## Parallel Opportunities

- T003, T005 and T006 can proceed in parallel after the initial structure exists.
- T008 and T009 can proceed in parallel before T010.
- T013 and T014 can proceed in parallel before T015.
- T018 and T019 can proceed in parallel before T020.
- T022 and T023 can proceed in parallel after implementation stabilizes.

## Implementation Strategy

1. Deliver US1 as the MVP with plan/apply/verify and Python/Pip.
2. Add native and ecosystem-specific routing in US2 without changing the report contract.
3. Add optional GenAI and safe failure classification in US3.
4. Run the quality gates and promote only the self-contained release copy.
