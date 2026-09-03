# Feature Specification: On-Demand OpenVINO Documentation

**Feature Branch**: `feature/adjustments`

**Created**: 2026-09-03

**Status**: Draft

**Input**: User description: "Create a sub-agent that downloads OpenVINO documentation only when explicitly requested, stores it locally, and a skill that reads the cached documentation without downloading it for every question."

## User Scenarios & Testing

### User Story 1 - Update the documentation cache on demand (Priority: P1)

As a maintainer, I want to explicitly request an OpenVINO documentation
update so that the local knowledge source can be refreshed without causing a
download during normal questions.

**Why this priority**: A reliable, intentional refresh is the foundation of a
useful local documentation source and protects time, network access, and
reproducibility.

**Independent Test**: Invoke the update workflow with a controlled extraction
input and confirm that it writes the site index, pages, metadata, and coverage
result to the agreed local directory.

**Acceptance Scenarios**:

1. **Given** no update request, **when** a user asks a question about OpenVINO,
   **then** the system reads the local documentation and performs no download.
2. **Given** the user explicitly asks to update the OpenVINO documentation,
   **when** a browser is available, **then** the synchronization workflow runs
   the approved extraction process against the requested documentation scope.
3. **Given** no browser is available, **when** an update is requested, **then**
   the workflow stops with a clear instruction to connect a browser and does
   not create a partial mirror presented as complete.

### User Story 2 - Read the cached documentation (Priority: P1)

As an AI practitioner, I want a skill to search and summarize the downloaded
OpenVINO documentation so that answers are fast, reproducible, and traceable
to the captured source pages.

**Why this priority**: The cache only creates value when the reader uses it
consistently instead of reopening the website for every question.

**Independent Test**: Place a sanitized documentation fixture in the local
cache and ask the reader for a known topic; verify that it cites local files,
reports cache metadata, and does not invoke the synchronization workflow.

**Acceptance Scenarios**:

1. **Given** a valid local cache, **when** the reader receives an OpenVINO
   question, **then** it identifies relevant Markdown pages and cites their
   local paths and original source URLs.
2. **Given** the cache is missing or empty, **when** the reader receives a
   question, **then** it explains that an explicit documentation update is
   required instead of silently downloading content.
3. **Given** the cache contains skipped pages or incomplete coverage, **when**
   the reader responds, **then** it discloses the limitation and avoids
   presenting the cache as a complete reference.

### User Story 3 - Preserve a distributable, reviewable snapshot (Priority: P2)

As a project maintainer, I want the generated reader skill to use a reviewed
local snapshot without depending on harness internals so that it can be
promoted safely and audited later.

**Why this priority**: The skill factory must preserve the separation between
working cache, candidate skill, and final distributable skill.

**Independent Test**: Copy the candidate reader and its documentation snapshot
to a clean directory and confirm that it can answer fixture questions without
the harness, network, or credentials.

**Acceptance Scenarios**:

1. **Given** a refreshed cache, **when** the candidate is prepared, **then** a
   versioned snapshot and metadata are placed under the candidate's own
   references directory.
2. **Given** a clean copy of the candidate, **when** a reader question is
   asked, **then** it reads only the bundled relative documentation paths.
3. **Given** third-party documentation is bundled, **when** it is distributed,
   **then** attribution, source URLs, extraction date, and skipped-page notes
   are retained.

## Edge Cases

- The source page is inaccessible, requires authentication, or the browser is
  unavailable.
- The extractor encounters rate limiting, timeouts, failed pages, or a sitemap
  whose route count differs from the extracted count.
- The target cache already contains generated pages or human-authored content.
- An update is interrupted after only some pages are written.
- The cache has no index, invalid metadata, broken relative links, or stale
  extraction date.
- A user asks a question outside the captured OpenVINO scope.
- Documentation contains external images or linked PDF/Office documents that
  cannot be rendered as Markdown.
- A candidate path contains credentials, machine-specific paths, symlinks, or
  references to harness-only files.

## Requirements

### Functional Requirements

- **FR-001**: The update workflow MUST run only after an explicit user request
  to update or download OpenVINO documentation.
- **FR-002**: The update workflow MUST use the approved rendered-documentation
  extraction process and a real browser; it MUST NOT substitute an unverified
  static mirror when browser extraction is unavailable.
- **FR-003**: The generated documentation MUST be stored under
  `docs/openvino/`, with an index, metadata manifest, Markdown pages, relative
  links, skipped-page information, and attribution notes.
- **FR-004**: A normal documentation question MUST read the local cache and
  MUST NOT start a download or browser session automatically.
- **FR-005**: The reader MUST cite the local Markdown path and preserve the
  original source URL for each cited page.
- **FR-006**: The reader MUST disclose missing, stale, partial, invalid, or
  out-of-scope cache state before presenting an answer.
- **FR-007**: The update workflow MUST validate frontmatter, link resolution,
  extraction coverage, and page fidelity using the extractor's verification
  gate before reporting success.
- **FR-008**: Interrupted or failed updates MUST be reported as incomplete and
  MUST NOT be represented as a complete documentation snapshot.
- **FR-009**: The candidate reader MUST bundle or receive an explicit reviewed
  documentation snapshot under its own relative references path and MUST NOT
  depend on `harness/`, `.codex/`, `.agents/`, absolute machine paths, or
  credentials.
- **FR-010**: The bundled snapshot MUST retain source URL, extraction date,
  coverage, skipped pages, linked documents, and attribution metadata.
- **FR-011**: The update workflow MUST avoid overwriting human-authored files
  without inspection and MUST keep generated output distinguishable.
- **FR-012**: Tests MUST cover cache hit, cache missing, explicit update,
  browser unavailable, partial extraction, invalid metadata, and clean-copy
  portability behavior.

### Key Entities

- **Documentation Cache**: The generated local site folder containing Markdown,
  index, assets, and manifest metadata.
- **Extraction Manifest**: Machine-readable source, date, route, coverage,
  skipped-page, linked-document, and verification information.
- **Reader Snapshot**: The reviewed copy of the cache bundled with the
  candidate or final skill.
- **Update Request**: An explicit maintainer instruction that authorizes one
  documentation refresh.

## Success Criteria

### Measurable Outcomes

- **SC-001**: One hundred percent of ordinary reader requests execute without a
  documentation download when a valid local cache exists.
- **SC-002**: One hundred percent of explicit update requests either produce a
  verification-passing cache or report a clear incomplete/blocked result.
- **SC-003**: One hundred percent of reader answers based on the cache include
  at least one local file citation and its original source URL, when relevant
  content exists.
- **SC-004**: A clean copy of the candidate answers all bundled fixture queries
  without access to the harness, network, or secrets.
- **SC-005**: One hundred percent of incomplete, stale, invalid, or partial
  cache fixtures are disclosed before content is presented as authoritative.

## Assumptions

- The OpenVINO documentation scope begins at
  `https://docs.openvino.ai/2026/index.html` and remains limited to the
  documentation area discovered from that route and its in-scope sitemap.
- The project accepts `docs/openvino/` as the canonical cache path because it
  follows the `extract-spa-docs` output contract; a display label may call it
  the “OpenVINO docs cache”.
- A browser connection is available only when a maintainer explicitly requests
  an update.
- The working cache and the distributable reader snapshot are separate; a
  refreshed cache does not become release content until validation and review
  pass.
- The first reader supports Markdown search and citation; semantic indexing,
  automatic web fallback, and answer generation from uncaptured pages are out
  of scope.
