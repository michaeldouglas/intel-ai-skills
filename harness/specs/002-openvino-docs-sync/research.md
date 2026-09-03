# Research Notes: On-Demand OpenVINO Documentation

## Decision 1: Use the existing extraction skill as the source of truth

The repository already contains `extract-spa-docs`, whose contract requires a
rendered browser extraction, an `index.md`, page frontmatter, relative links,
coverage checks, and attribution. The new sync flow delegates to that skill's
reference scripts and does not implement a second scraper.

This avoids silently treating a static HTML or source-code fetch as equivalent
to rendered documentation. If a real browser is not available, synchronization
is blocked and the reason is reported.

## Decision 2: Cache once, read many times

Normal reader requests use the reviewed local Markdown snapshot. Only a command
containing an explicit update action invokes synchronization. Missing or stale
metadata produces a visible warning and an instruction to request an update;
it never triggers an implicit download.

## Decision 3: Separate working cache from distributed snapshot

The working cache belongs to the harness at `docs/openvino/`. A candidate reader
copies only a verified cache into its own `references/openvino/` directory and
records the source, date, coverage, and attribution. This keeps a promoted skill
independent of `harness/`, `.codex/`, and `.agents/`.

## Decision 4: Protect existing files

The sync utility recognizes a generated cache only when `manifest.json` exists
and contains extractor coverage metadata. A non-empty directory without that
marker is treated as human-authored or unknown and is not overwritten. A
published candidate snapshot is replaceable only when its own marker exists.

## Alternatives rejected

- Downloading on every question: slower, non-reproducible, and contrary to the
  requested explicit-update behavior.
- Automatic web fallback from the reader: makes offline behavior surprising and
  hides cache gaps.
- Bundling a reference to `harness/docs/openvino/`: violates the portability
  rule for promoted skills.
- Writing a new crawler: duplicates the approved extraction logic and risks
  losing the extractor's coverage and fidelity checks.
