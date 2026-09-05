# Tasks: Localized Skills-First README

**Input**: Design documents from `/specs/003-localized-skills-readme/`

**Prerequisites**: [plan.md](plan.md), [spec.md](spec.md)

## Phase 1: Tests and documentation contract

- [X] T001 [P] Add documentation contract tests in `tests/test_documentation.py` for language links, localized files, published skill links, and skills-first ordering.

## Phase 2: Published skills catalog

- [X] T002 Rewrite the opening and navigation sections of root `../README.md` so the published skills catalog and language selector appear before project internals.
- [X] T003 [P] Update the root README quickstart and skill usage sections to cover both `intel-docs-reader` and `intel-hardware-advisor` accurately.
- [X] T003a Add direct `npx skills add` commands for both published skills and state that `codex` is only an example destination.
- [X] T003b Update harness SDD guidance and the OpenVINO researcher fallback to use `docs/2026/` as the primary knowledge base.
- [X] T003c Update the OpenVINO skills so the agent invokes bundled scripts automatically instead of asking users to run them.

## Phase 3: Localized documentation (P1)

- [X] T004 [P] Create `../docs/README.pt-BR.md` with the skills catalog, usage instructions, project context, contribution flow, and language navigation in Brazilian Portuguese.
- [X] T005 [P] Create `../docs/README.es.md` with the skills catalog, usage instructions, project context, contribution flow, and language navigation in Spanish.
- [X] T006 Verify that localized documentation preserves skill names, commands, paths, safety boundaries, and evidence limitations.

## Phase 4: Validation and quality review

- [X] T007 Run the documentation contract test and the existing test suite.
- [X] T008 Run `graphify update .` after product/documentation changes and inspect the resulting worktree.
- [X] T009 Review the rendered Markdown links and confirm every referenced target exists.

## Dependencies & Execution Order

- T001 defines the validation contract and may be written before content changes.
- T002 and T003 affect the same root README and must run sequentially.
- T004 and T005 can run in parallel because they use separate files.
- T006 depends on T002-T005.
- T007-T009 depend on all content and test changes.

## Implementation Strategy

1. Establish the documentation contract test.
2. Refactor the English entry point around the two published skills.
3. Add complete pt-BR and Spanish documents under `docs/`.
4. Run focused and full validation, refresh Graphify, then commit locally.
