# Feature Specification: GitHub Pages Documentation Site

**Feature Branch**: `feature/logo-directions`

**Created**: 2026-09-05

**Status**: Draft

**Input**: User description: "Create a modern GitHub Pages documentation site inside docs/site, keep the existing Markdown files in docs untouched and independent, use the selected logo and visual identity, publish automatically when main changes, provide a local preview command, and offer the site in English, Brazilian Portuguese, and Spanish."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Understand the project and get started (Priority: P1)

As a developer discovering Intel AI Skills, I want a clear project overview,
installation guidance, and a short explanation of how the skills work so that I
can decide whether the project fits my OpenVINO workflow and start using it.

**Why this priority**: The public site must communicate the project's value and
the first-use path before a visitor explores individual skills.

**Independent Test**: Open the site home page and verify that a new visitor can
identify the project purpose, understand that the skills are portable across
agents, find the installation command, and reach the skill catalog without
reading repository-internal documentation.

**Acceptance Scenarios**:

1. **Given** a visitor opens the site, **When** the home page loads, **Then**
   it presents the project purpose, the relationship to OpenVINO, the
   distinction between published skills and the internal harness, and a clear
   next action.
2. **Given** a visitor wants to install a skill, **When** they follow the
   getting-started guidance, **Then** they see a copyable `npx skills add`
   example, understand that Codex is only one target, and can choose Claude or
   another compatible agent.

### User Story 2 - Explore and select a skill (Priority: P1)

As a developer with a specific hardware or OpenVINO task, I want a catalog
with grouped navigation and a detailed page for every published skill so that
I can choose the right capability without knowing the repository structure.

**Why this priority**: The skills are the project's main public product, so the
site must make their boundaries and use cases easy to understand.

**Independent Test**: From the catalog, open every published skill page and
verify that each page explains its purpose, when to use it, what it does, what
it does not do, installation, and links to related skills.

**Acceptance Scenarios**:

1. **Given** a visitor opens the catalog, **When** they inspect the navigation,
   **Then** skills are grouped into understandable categories and each
   published skill has a visible detail link.
2. **Given** a visitor opens a skill page, **When** they scan the page, **Then**
   they can find its role, activation examples, expected behavior, boundaries,
   installation command, and related skills.
3. **Given** a visitor uses a narrow screen, **When** they open the navigation,
   **Then** the catalog remains usable without horizontal scrolling or hidden
   skill pages.

### User Story 3 - Maintain and preview the public documentation (Priority: P2)

As a project maintainer, I want the site to build and publish automatically
from `main` while keeping the existing `docs/` files untouched, and I want a
simple local preview command so that documentation changes can be reviewed
before publication.

**Why this priority**: Reliable publication and local review prevent the public
documentation from drifting or requiring manual deployment steps.

**Independent Test**: Run the documented local preview command and open the
  site locally; then inspect the publication workflow and verify that a successful
  change on `main` builds the site from `docs/site/` and deploys it to GitHub Pages.
  Maintainer-only preview instructions belong in repository development docs,
  not in the public skill onboarding page.

**Acceptance Scenarios**:

1. **Given** the repository is checked out locally, **When** a maintainer runs
   the documented preview command, **Then** the home page and skill pages are
   available from a local web server.
2. **Given** a change reaches `main`, **When** the quality and build steps
   succeed, **Then** the publication workflow deploys the generated site to
   GitHub Pages.
3. **Given** the existing `docs/` files contain localized READMEs, **When** the
   site is built, **Then** those files remain unchanged and are not required as
   site input.

### User Story 4 - Read the site in a preferred language (Priority: P2)

As a visitor who prefers Brazilian Portuguese or Spanish, I want the same
project and skill documentation available in my language so that I can learn
and install the skills without translating the site manually.

**Independent Test**: Build the site, open `/pt-br/` and `/es/`, and verify
that the overview, catalog, skill details, navigation, and language switcher
are translated and link to the equivalent page in each language.

**Acceptance Scenarios**:

1. **Given** a visitor opens a localized home page, **When** they navigate the
   site, **Then** the overview, installation guidance, categories, and skill
   descriptions remain in the selected language.
2. **Given** a visitor is on any generated page, **When** they use the language
   switcher, **Then** they reach the equivalent route in English, pt-BR, or
   Spanish.

### Edge Cases

- A skill directory may contain supporting scripts or references that are useful
  to its agent but are not appropriate to reproduce verbatim on the public site;
  the site must provide a concise public explanation instead.
- A new skill may be added without a matching site page; the build validation
  must make the omission visible rather than silently presenting an incomplete
  catalog.
- A link to a removed or renamed skill must fail validation before publication.
- The site must remain readable when JavaScript is unavailable for core content
  and navigation.
- The logo must remain legible on both light and dark surfaces and at narrow
  viewport widths.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The site MUST live under `docs/site/`; the existing Markdown
  files directly under `docs/` MUST remain untouched and MUST NOT be required
  as site input.
- **FR-002**: The site MUST provide a home page that explains the project's
  purpose, OpenVINO relationship, portable-agent model, published-skills scope,
  and the internal harness boundary.
- **FR-003**: The site MUST provide installation guidance using the supported
  `npx skills add` pattern and MUST include examples for installing one or
  multiple skills.
- **FR-004**: The site MUST provide a catalog and detail page for every
  published skill in `skills/`, including purpose, appropriate use cases,
  behavior, limitations, installation, and related skills.
- **FR-005**: The site MUST provide grouped navigation or submenus so visitors
  can move between the project overview, getting started content, and skill
  details without relying on repository paths.
- **FR-006**: The site MUST use the selected Intel AI Skills logo assets and
  their wine, cyan, navy, and dark-surface visual language consistently across
  light and dark surfaces.
- **FR-007**: The site MUST be responsive, keyboard navigable, readable at
  mobile widths, and usable for core content without requiring JavaScript.
- **FR-008**: The repository MUST provide a documented one-command local
  preview that serves the same `docs/site/` content intended for publication.
- **FR-009**: A GitHub Actions workflow MUST build and deploy the site to
  GitHub Pages after successful changes to `main`, using the generated site and
  not the existing `docs/` directory.
- **FR-010**: Build validation MUST check required site entry points, skill-page
  coverage, internal links, and the presence of the selected logo assets before
  a deployment is attempted.
- **FR-011**: The site MUST generate English, Brazilian Portuguese (`/pt-br/`),
  and Spanish (`/es/`) versions of the overview, getting-started, catalog,
  fallback, and every published skill page.
- **FR-012**: Every generated page MUST expose a language switcher that points
  to the equivalent route in all supported languages and marks the active
  language accessibly.
- **FR-013**: Build validation MUST verify that every supported locale contains
  translated UI labels, category copy, and metadata for every published skill.

### Key Entities

- **Project Overview**: The public explanation of Intel AI Skills, its OpenVINO
  focus, supported agent usage, and the harness boundary.
- **Published Skill**: A distributable skill represented by its name, purpose,
  triggers, workflow, boundaries, installation command, and related skills.
- **Documentation Site**: The navigable public pages generated from content in
  `docs/site/` and published through GitHub Pages.
- **Publication Build**: The repeatable validation and deployment process
  triggered by changes to `main`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A first-time visitor can reach the catalog and an individual skill
  page from the home page in no more than two navigation actions.
- **SC-002**: One hundred percent of published skills have a linked public
  detail page before a publication build succeeds.
- **SC-003**: The local preview starts with one documented command and serves
  the home page plus at least one skill page without additional setup.
- **SC-004**: Every internal navigation link and required logo reference passes
  validation before the deployment step runs.
- **SC-005**: A successful change to `main` triggers one automated build and
  publication path without manual file copying.
- **SC-006**: The primary content remains usable at mobile widths and when
  client-side scripting is disabled.
- **SC-007**: A successful build generates the same complete route set for all
  three supported languages, and every language-switcher link resolves.

## Assumptions

- The current directories under `skills/` are the source of truth for the
  published skill catalog.
- The site is a static documentation experience and does not need a backend,
  authentication, or user-generated content.
- The existing `docs/README.pt-BR.md` and `docs/README.es.md` remain repository
  documentation and are not rewritten or copied into the site automatically.
- GitHub Pages and GitHub Actions will be enabled for the repository by the
  maintainer if repository settings require an explicit activation.
- English is the default site language; Brazilian Portuguese and Spanish are
  generated as first-class localized routes. The existing localized READMEs
  remain repository documentation and are not rewritten or used as site input.
