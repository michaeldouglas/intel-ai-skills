# Implementation Plan: On-Demand OpenVINO Documentation

**Branch**: `feature/adjustments` | **Date**: 2026-09-03 | **Spec**: [spec.md](./spec.md)

## Summary

Add an explicit documentation synchronization subagent and a local-only
OpenVINO documentation reader. The sync path invokes the existing
`extract-spa-docs` crawler and verifier only after an update command is
requested. It writes the generated site to `docs/openvino/`, records the
extractor manifest as the cache metadata, and can publish a reviewed snapshot
into the candidate reader. The reader path searches only its relative local
snapshot and reports cache freshness and coverage limitations without creating
a browser session or downloading anything.

## Technical Context

**Language/Version**: Python 3.13.7+ orchestration and reader; Node.js with a
Chromium-capable browser and the existing extractor dependencies for updates.

**Primary Dependencies**: Python standard library; existing
`.agents/skills/extract-spa-docs/scripts/extract.mjs` and `verify.mjs`; npm
packages `playwright-core`, `turndown`, and `turndown-plugin-gfm` installed in a
temporary reusable dependency directory only for explicit updates.

**Storage**: Generated Markdown cache at `docs/openvino/`; reviewed snapshot at
`candidates/openvino-docs-reader/references/openvino/`; no database.

**Testing**: Python `unittest`/`pytest` tests for command construction, no-op
reader behavior, cache states, snapshot portability, metadata, and mocked
extractor/verifier outcomes.

**Target Platform**: Windows and Linux development environments; the sync
wrapper uses `sys.executable` and `subprocess` without shell interpolation.

**Project Type**: Skill-factory subagent, synchronization utility, and
self-contained local documentation reader skill.

**Performance Goals**: Reader queries complete locally in under one second for
a normal snapshot. Synchronization is bounded by the extractor's configured
page timeout and request delay and is not run during reader queries.

**Constraints**: No automatic network access, no static-source substitution
when rendered extraction is required, no overwrite of an unrecognized target,
preserve third-party attribution, and no promoted dependency on harness paths.

**Scale/Scope**: The OpenVINO 2026 documentation area rooted at the supplied
index URL, with route discovery and coverage recorded by the extractor.

## Constitution Check

- **Evidence-first**: PASS. The cache keeps source URLs, extraction date,
  coverage, skipped pages, and attribution from the extractor manifest.
- **Portable and deterministic**: PASS. Reader code uses only local relative
  paths; snapshot tests run without network or browser access.
- **Test-first**: PASS. Tests cover explicit update, no-download reading,
  missing/partial cache states, and clean-copy behavior.
- **Privacy and safe discovery**: PASS. The wrapper passes fixed arguments,
  avoids shell execution, does not read environment dumps, and does not expose
  command output as documentation.
- **Review-gated release**: PASS. Sync cache publication and candidate
  promotion remain separate; final release remains owned by the release gate.

## Design Decisions

1. `docs/openvino/` is the canonical working cache because it follows the
   `extract-spa-docs` output contract. The user-facing phrase may call it the
   “OpenVINO docs cache”.
2. The sync script refuses to act unless `--update` is present. Reader code has
   no sync import and no network-capable path.
3. Existing generated caches are refreshable only when `manifest.json`
   identifies them as extractor output. An unrecognized non-empty directory is
   blocked to protect human-authored content.
4. A candidate snapshot is copied through a staging directory and tagged with
   `.openvino-snapshot.json`; later refreshes may replace only tagged generated
   snapshots.
5. The subagent describes the browser interaction required by
   `extract-spa-docs`. The wrapper is the fast local execution path; if no
   browser is available, the operation reports blocked rather than falling
   back to static scraping.

## Project Structure

```text
.codex/agents/openvino-docs-sync.md
.codex/agents/openvino-docs-sync.toml
scripts/openvino_docs_sync.py

candidates/openvino-docs-reader/
├── SKILL.md
├── scripts/read_openvino_docs.py
└── references/openvino/              # reviewed snapshot, generated on update

docs/openvino/                         # working generated cache, on update

tests/
├── unit/test_openvino_docs_sync.py
├── integration/test_openvino_docs_reader.py
└── integration/test_openvino_docs_sync.py
```

**Structure Decision**: Keep orchestration in repository-level `scripts/`,
keep the subagent contract in `.codex/agents/`, and keep the reader runtime
self-contained under its candidate directory. The working cache is not a
runtime dependency of the promoted reader.

## Contract and Data Flow

```text
explicit update request
  -> openvino-docs-sync subagent
  -> scripts/openvino_docs_sync.py --update
  -> extract.mjs (real browser) -> docs/openvino/
  -> verify.mjs -> manifest/index coverage gate
  -> optional publish snapshot -> candidate references/openvino/

OpenVINO question
  -> openvino-docs-reader
  -> read snapshot locally
  -> return ranked pages, excerpts, local paths, source URLs, and cache status
```

See [data-model.md](./data-model.md), [contracts/sync-contract.md](./contracts/sync-contract.md),
and [quickstart.md](./quickstart.md).

## Complexity Tracking

No constitution violations. The two-stage cache/snapshot flow is required to
keep the final skill independent from internal harness paths while avoiding a
network call for every reader question.
