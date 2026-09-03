# Tasks: On-Demand OpenVINO Documentation

**Input**: Design documents from `specs/002-openvino-docs-sync/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, and `contracts/sync-contract.md`

**Tests**: Included because explicit no-download behavior, cache safety, verification, and portability are release requirements.

## Phase 1: Setup

- [X] T001 Create repository script directory `scripts` and candidate directories `candidates/openvino-docs-reader/scripts` and `candidates/openvino-docs-reader/references`
- [X] T002 [P] Add the subagent role contract in `.codex/agents/openvino-docs-sync.md`
- [X] T003 [P] Add the subagent runtime configuration in `.codex/agents/openvino-docs-sync.toml`
- [X] T004 [P] Add candidate reader instructions in `candidates/openvino-docs-reader/SKILL.md`

## Phase 2: Foundational

- [X] T005 [P] [US1] Write synchronization command construction and guard tests in `tests/unit/test_openvino_docs_sync.py`
- [X] T006 [P] [US2] Write local reader cache-state and citation tests in `tests/integration/test_openvino_docs_reader.py`
- [X] T007 [P] [US3] Write snapshot portability and metadata tests in `tests/integration/test_openvino_docs_sync.py`
- [X] T008 [US1] Define explicit source URL, cache path, extractor paths, and status contract in `scripts/openvino_docs_sync.py`

**Checkpoint**: Tests exist for no-op behavior, explicit update, cache states, and clean-copy boundaries.

## Phase 3: User Story 1 - Update the documentation cache on demand (Priority: P1)

**Goal**: Run the approved extractor and verifier only when an explicit update action is supplied.

**Independent Test**: Mock the extractor/verifier processes and confirm command arguments, environment, target protection, and failure status.

### Tests first

- [X] T009 [P] [US1] Add tests for missing `--update`, `--verify-only`, and explicit update argument construction in `tests/unit/test_openvino_docs_sync.py`
- [X] T010 [P] [US1] Add tests for unrecognized existing cache protection and generated-cache refresh in `tests/unit/test_openvino_docs_sync.py`

### Implementation

- [X] T011 [US1] Implement safe subprocess execution without shell interpolation in `scripts/openvino_docs_sync.py`
- [X] T012 [US1] Implement generated-cache inspection, output preparation, and safe failure statuses in `scripts/openvino_docs_sync.py`
- [X] T013 [US1] Implement explicit extractor invocation with `extract.mjs`, scoped environment, reusable dependency directory, and request controls in `scripts/openvino_docs_sync.py`
- [X] T014 [US1] Implement verifier invocation with `verify.mjs` and success/blocked/incomplete result reporting in `scripts/openvino_docs_sync.py`
- [X] T015 [US1] Implement candidate snapshot publication with staging, marker, manifest hash, and replace-only-generated protection in `scripts/openvino_docs_sync.py`
- [X] T016 [US1] Add update and no-browser instructions, scope, and attribution rules to `.codex/agents/openvino-docs-sync.md`

**Checkpoint**: No ordinary reader path can start the sync process; explicit update failures remain visible and non-authoritative.

## Phase 4: User Story 2 - Read the cached documentation (Priority: P1)

**Goal**: Search local Markdown and return ranked citations without any network or sync behavior.

**Independent Test**: Run the reader against a small local fixture with valid, missing, incomplete, and invalid metadata.

### Tests first

- [X] T017 [P] [US2] Add reader query, ranking, excerpt, source URL, and no-download assertions in `tests/integration/test_openvino_docs_reader.py`
- [X] T018 [P] [US2] Add candidate CLI invocation and clean relative-path assertions in `tests/integration/test_openvino_docs_reader.py`

### Implementation

- [X] T019 [US2] Implement local manifest/index inspection and cache status classification in `candidates/openvino-docs-reader/scripts/read_openvino_docs.py`
- [X] T020 [US2] Implement bounded Markdown search, relevance ranking, frontmatter parsing, and excerpt rendering in `candidates/openvino-docs-reader/scripts/read_openvino_docs.py`
- [X] T021 [US2] Implement JSON and human-readable reader output with limitations and citations in `candidates/openvino-docs-reader/scripts/read_openvino_docs.py`
- [X] T022 [US2] Document cache-only operation, update request phrases, and citation behavior in `candidates/openvino-docs-reader/SKILL.md`

**Checkpoint**: A normal OpenVINO question reads only the local snapshot and clearly asks for an explicit update when needed.

## Phase 5: User Story 3 - Preserve a distributable, reviewable snapshot (Priority: P2)

**Goal**: Ensure the reader candidate can be copied without harness or machine-specific dependencies.

**Independent Test**: Use a fixture snapshot, copy the candidate to a temporary clean directory, and answer a query without network access.

### Tests first

- [X] T023 [P] [US3] Add fixture snapshot and clean-copy integration coverage in `tests/integration/test_openvino_docs_sync.py`
- [X] T024 [P] [US3] Add checks for attribution, source URLs, extraction date, skipped pages, and coverage metadata in `tests/integration/test_openvino_docs_sync.py`

### Implementation

- [X] T025 [US3] Add sanitized reader snapshot fixtures under `tests/fixtures/openvino-docs/` with `index.md`, `manifest.json`, and representative pages
- [X] T026 [US3] Add candidate metadata and attribution preservation to `scripts/openvino_docs_sync.py`
- [X] T027 [US3] Add structural scans for internal paths, absolute paths, credentials, and network imports in `tests/integration/test_openvino_docs_sync.py`

**Checkpoint**: The candidate is locally usable and does not depend on `harness/`, `.codex/`, `.agents/`, or network access.

## Phase 6: Polish and release readiness

- [X] T028 [P] [US1] Add repository documentation for the on-demand workflow in `scripts/README.md`
- [X] T029 [P] [US2] Validate `specs/002-openvino-docs-sync/quickstart.md` against the implemented commands
- [X] T030 [US3] Run all unit and integration tests, fixture checks, and Python compilation
- [X] T031 [US3] Perform a read-only skill quality review of `candidates/openvino-docs-reader`
- [X] T032 [US3] Run `graphify update .` after all product and harness artifacts are complete

## Dependencies and execution order

- Phase 1 precedes Phase 2; Phase 2 blocks both user stories.
- US1 owns the network-capable synchronization path. US2 must not import or
  invoke it. US3 validates the boundary and snapshot distribution.
- Tests are written before their implementation tasks. Sync process tests use
  mocks and never contact the documentation site.
- T009-T010, T017-T018, and T023-T024 can run in parallel because they touch
  separate test concerns; implementation tasks touching the same file remain sequential.
- Promotion from `candidates/` to sibling `skills/` is not part of this change.
