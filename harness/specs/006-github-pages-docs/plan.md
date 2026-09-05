# Implementation Plan: GitHub Pages Documentation Site

**Branch**: `feature/logo-directions` | **Date**: 2026-09-05 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/006-github-pages-docs/spec.md`

**Note**: This template is filled in by the `$speckit-plan` command; its definition describes the execution workflow.

## Summary

Create a dependency-free multilingual static documentation site under `docs/site/` that
explains Intel AI Skills, provides grouped navigation and detailed pages for
all published skills, and uses the selected Open Monogram identity. A
standard-library Python build script will validate the catalog and links,
generate the final static output under `docs/site/build/site/`, and copy the official
logo assets without changing `docs/`. GitHub Actions will build and deploy that
output to GitHub Pages only after changes reach `main`; a local preview script
will run the same build before serving the result.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: HTML/CSS/vanilla JavaScript; Python 3.11+ for build and preview scripts

**Primary Dependencies**: Python standard library; GitHub Pages Actions (`configure-pages@v5`, `upload-pages-artifact@v4`, `deploy-pages@v4`)

**Storage**: Versioned files under `docs/site/`; generated `docs/site/build/site/` is disposable

**Testing**: Existing pytest quality suite plus deterministic build/link/catalog checks

**Target Platform**: GitHub Pages and any modern desktop/mobile browser; local Python web server

**Project Type**: Static documentation site with build tooling

**Performance Goals**: First meaningful content should be available without client-side JavaScript; generated site should remain small enough for fast repository-hosted navigation

**Constraints**: Keep `docs/` untouched; no runtime backend; no third-party frontend dependency; core navigation and content must work without JavaScript; generated files must not be committed

**Scale/Scope**: One overview, one getting-started page, one catalog, and one generated detail page for each current published skill in English, pt-BR, and Spanish

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

* **Evidence and scope**: PASS. Public skill descriptions will be derived from
  versioned skill metadata and will distinguish documented behavior from
  examples and boundaries.
* **Portability and determinism**: PASS. The site has no backend and the build
  uses only the Python standard library; `docs/` remains outside the build
  input.
* **Test-first engineering**: PASS. Build, catalog-coverage, link, and workflow
  validation will be added to the existing automated suite.
* **Privacy and safe discovery**: PASS. The site copies only selected public
  logo assets and authored content; it does not inspect user machines.
* **Review-gated release**: PASS. The generated site is validated before the
  Pages deployment job and the change remains subject to the existing PR gates.

## Project Structure

### Documentation (this feature)

```text
specs/006-github-pages-docs/
├── plan.md              # This file ($speckit-plan command output)
├── research.md          # Phase 0 output ($speckit-plan command)
├── data-model.md        # Phase 1 output ($speckit-plan command)
├── quickstart.md        # Phase 1 output ($speckit-plan command)
├── contracts/           # Phase 1 output ($speckit-plan command)
└── tasks.md             # Phase 2 output ($speckit-tasks command - NOT created by $speckit-plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
docs/site/
├── content/skills.json       # English catalog metadata and detailed skill copy
├── content/locales.json      # pt-BR and Spanish UI and skill translations
├── templates/                # HTML page templates and shared navigation
└── static/                   # CSS, progressive-enhancement JS, favicon assets

├── scripts/
│   ├── build_site.py         # Validate content and generate build/site/
│   └── serve_site.py         # Build, then serve build/site locally

harness/tests/test_site.py    # Build, coverage, link, and output checks
.github/workflows/deploy-pages.yml
└── build/site/               # Ignored generated publication artifact
```

**Structure Decision**: Keep authored site content isolated in `docs/site/` so
the existing Markdown files directly under `docs/` remain untouched. A small Python generator is
preferred over a frontend framework because the project needs a portable,
reviewable static site with a zero-install local preview. The generator emits
complete HTML pages, so JavaScript can enhance navigation and theme controls
without being required for the main content.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
No constitution violations. The build script and authored metadata are the
smallest design that supports generated detail pages, coverage validation, and
the requested local preview without adding a package manager or runtime.
