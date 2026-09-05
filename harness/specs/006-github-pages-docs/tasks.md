# Tasks: GitHub Pages Documentation Site

**Input**: Design documents from `/specs/006-github-pages-docs/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Tests**: Required for build, coverage, links, and publication configuration.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Establish the authored site structure and public content model.

- [x] T001 Create the authored site directories under `docs/site/content/`, `docs/site/templates/`, and `docs/site/static/`
- [x] T002 [P] Define the complete published-skill catalog metadata in `docs/site/content/skills.json`
- [x] T003 [P] Add the selected logo and theme asset references in `docs/site/static/branding/README.md`
- [x] T004 [P] Add the site metadata and navigation labels in `docs/site/content/site.json`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Provide deterministic generation, validation, and test scaffolding.

- [x] T005 [P] Create failing build and catalog coverage tests in `harness/tests/test_site.py`
- [x] T006 Implement the deterministic site builder, catalog validation, link validation, page generation, and logo copying in `docs/site/scripts/build_site.py`
- [x] T007 Implement the one-command local build-and-serve flow in `docs/site/scripts/serve_site.py`
- [x] T008 Add the GitHub Pages build-and-deploy workflow triggered by `main` in `.github/workflows/deploy-pages.yml`
- [x] T009 Update the repository local-development guidance with the site preview command in `README.md`

**Checkpoint**: The generator can produce a complete artifact and the quality suite can validate its structure.

---

## Phase 3: User Story 1 - Understand the Project and Get Started (Priority: P1) 🎯 MVP

**Goal**: Give new visitors a clear project overview, installation path, and explanation of the public skill model.

**Independent Test**: Build the site, open `build/site/index.html` and `build/site/getting-started.html`, and verify the project purpose, OpenVINO relationship, agent portability, harness boundary, and copyable install examples are visible.

- [x] T010 [P] [US1] Create the shared semantic page shell, header, footer, theme controls, and navigation in `docs/site/templates/layout.html`
- [x] T011 [US1] Create the project overview content and primary calls to action in `docs/site/templates/index.html`
- [x] T012 [US1] Create installation, agent portability, and portable-skill guidance in `docs/site/templates/getting-started.html`
- [x] T013 [US1] Add responsive branded styling for overview and getting-started pages in `docs/site/static/site.css`

**Checkpoint**: A new visitor can understand the project and install a skill without reading repository-internal files.

---

## Phase 4: User Story 2 - Explore and Select a Skill (Priority: P1)

**Goal**: Provide grouped navigation and detailed generated pages for every published skill.

**Independent Test**: Build the site and verify that `skills/index.html` lists every directory under `skills/`, every generated skill page contains its required sections, and every related-skill link resolves.

- [x] T014 [US2] Create the grouped skill catalog template in `docs/site/templates/skills-index.html`
- [x] T015 [US2] Create the generated skill detail template with purpose, use cases, workflow, boundaries, installation, and related links in `docs/site/templates/skill-detail.html`
- [x] T016 [US2] Add catalog cards, skill detail layout, code blocks, and responsive sidebar styling in `docs/site/static/site.css`
- [x] T017 [US2] Add progressive-enhancement navigation behavior and theme persistence in `docs/site/static/site.js`
- [x] T018 [US2] Add the branded not-found page and generated fallback routes in `docs/site/templates/404.html`

**Checkpoint**: Every published skill has a discoverable, detailed, responsive public page.

---

## Phase 5: User Story 3 - Maintain and Preview the Public Documentation (Priority: P2)

**Goal**: Publish the generated site from `main` and make the same artifact easy to review locally.

**Independent Test**: Run `python docs/site/scripts/serve_site.py`, open the local home page, and inspect the workflow for a `main` trigger, build validation, Pages artifact upload, and Pages deployment permissions.

- [x] T019 [US3] Add workflow assertions and generated-output checks for `docs/site/`, `docs/site/build/site/`, and `.github/workflows/deploy-pages.yml` in `harness/tests/test_site.py`
- [x] T020 [US3] Document the local preview, generated output, and publication behavior in `README.md`

**Checkpoint**: Maintainers can preview locally and the repository has a repeatable Pages deployment path from `main`.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Validate the finished experience and repository integration.

- [x] T021 [P] Add accessibility labels, skip navigation, focus states, reduced-motion handling, and dark/light contrast checks in `docs/site/templates/layout.html` and `docs/site/static/site.css`
- [x] T022 [P] Add favicon and social metadata using the selected mark in `docs/site/templates/layout.html`
- [x] T023 Run the quickstart scenarios from `specs/006-github-pages-docs/quickstart.md` and record the result in `harness/tests/test_site.py`
- [x] T024 Run `python -m pytest -q` from `harness/` and resolve any documentation or workflow regressions
- [x] T025 Run `graphify update .` and inspect the final repository status for generated artifacts or unintended changes

---

## Phase 7: User Story 4 - Localized Documentation (Priority: P2)

**Goal**: Publish equivalent English, pt-BR, and Spanish documentation routes
without changing the existing Markdown files directly under `docs/`.

**Independent Test**: Build the site and verify every locale contains the
overview, getting-started, catalog, fallback, and all published skill pages;
then verify every language-switcher link resolves.

- [x] T026 Add the locale data contract and complete pt-BR and Spanish translations in `docs/site/content/locales.json`
- [x] T027 Add localized page generation, language-aware navigation, and route validation in `docs/site/scripts/build_site.py`
- [x] T028 Add language-switcher markup and localized accessibility labels to the shared templates and styles
- [x] T029 Add localized route, translation, and switcher assertions in `harness/tests/test_site.py`
- [x] T030 Document the three local preview routes for maintainers and update the feature artifacts for localization

---

## Phase 8: Documentation Navigation Experience (Priority: P1)

**Goal**: Organize the public site as a documentation product with predictable
navigation around the project and every published skill.

- [x] T031 Add the shared documentation shell with grouped sidebar, breadcrumbs, and contextual table of contents in `docs/site/templates/layout.html` and `docs/site/scripts/build_site.py`
- [x] T032 Add previous/next skill navigation and stable section anchors to the getting-started, catalog, and skill detail templates
- [x] T033 Add responsive documentation-shell styling that preserves access to the catalog and skill pages on narrow screens in `docs/site/static/site.css`
- [x] T034 Add localized navigation labels and generated-output assertions for the documentation shell in `docs/site/content/locales.json` and `harness/tests/test_site.py`
- [x] T035 Update the feature specification, data model, and quickstart with the documentation navigation contract

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies; establishes authored content and site metadata.
- **Foundational (Phase 2)**: Depends on Phase 1 and blocks all user stories.
- **User Story 1 (Phase 3)**: Depends on the shared shell and builder from Phase 2.
- **User Story 2 (Phase 4)**: Depends on the shared shell, builder, and catalog metadata from Phases 1–2.
- **User Story 3 (Phase 5)**: Depends on the generated output and validation from Phases 2–4.
- **User Story 4 (Phase 7)**: Depends on the shared templates, catalog model, and deterministic builder from Phases 1–6.
- **Polish (Phase 6)**: Depends on all user stories.

### Parallel Opportunities

- T002, T003, and T004 can run in parallel after the directories exist.
- T005 and T008 can be drafted in parallel because they target different files.
- T010, T011, and T012 can be developed in parallel after the shell contract is established.
- T014, T015, and T018 can be developed in parallel after the metadata contract is established.
- T021 and T022 can run in parallel after the final layout is available.

## Implementation Strategy

### MVP First

1. Complete Phases 1 and 2.
2. Complete User Story 1.
3. Validate the overview, getting-started flow, and local build.

### Incremental Delivery

1. Add the skill catalog and generated pages for User Story 2.
2. Add the Pages workflow and maintainer documentation for User Story 3.
3. Apply accessibility, metadata, and final quality checks.
4. Add and validate the localized routes without copying or rewriting `docs/README.pt-BR.md` or `docs/README.es.md`.
