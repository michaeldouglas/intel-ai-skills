# Implementation Plan: Localized Skills-First README

**Branch**: `feature/localized-skills-readme` | **Date**: 2026-09-05 | **Spec**: [spec.md](spec.md)

## Summary

Reorder the root README so the published skills are the first product-facing
content, add a visible language switcher, and provide complete Portuguese
(Brazil) and Spanish versions under `docs/`. Add a focused automated test for
the documentation contract so future edits cannot silently break the language
links or skill catalog.

## Technical Context

**Language/Version**: Markdown; Python 3.11+ for repository tests

**Primary Dependencies**: Existing pytest test suite; no new runtime dependency

**Storage**: Version-controlled Markdown files

**Testing**: `python -m pytest -q`

**Target Platform**: GitHub-rendered repository documentation and local checkouts

**Project Type**: Documentation and test contract for a skills repository

**Performance Goals**: Documentation validation completes within the existing test suite runtime

**Constraints**: Relative links only; no dependency on harness-only paths from the distributable skill descriptions; preserve exact commands and skill directory names

**Scale/Scope**: One root README, two localized documents, and one documentation contract test

## Constitution Check

- Evidence and product boundaries: PASS. The README will describe only the published skills and documented behavior already present in their `SKILL.md` files.
- Portable and deterministic skills: PASS. No skill implementation changes; links to published skills remain self-contained.
- Test-first engineering: PASS. The documentation contract test is planned alongside the content changes and will validate deterministic repository paths.
- Privacy and safe discovery: PASS. Documentation will preserve the existing read-only and privacy boundaries.
- Review-gated release: PASS. This change updates discovery documentation only and will be validated before local commit.

## Project Structure

```text
intel-ai-skills/
├── README.md                         # English entry point and language switcher
├── docs/
│   ├── README.pt-BR.md               # Portuguese (Brazil) documentation
│   └── README.es.md                  # Spanish documentation
├── skills/
│   ├── intel-docs-reader/SKILL.md
│   └── intel-hardware-advisor/SKILL.md
└── harness/
    └── tests/test_documentation.py   # Documentation contract checks
```

**Structure Decision**: Keep user-facing localized documentation in a root
`docs/` directory and keep its links relative to the repository root. Put the
contract test in the harness because the harness owns automated validation.

## Design Details

### Information architecture

1. Banner and language selector.
2. Published skills catalog with direct links and short use cases.
3. Quickstart with direct `npx skills add` commands and an agent-neutral destination note.
4. Harness SDD guidance that makes `harness/docs/2026/` the primary OpenVINO knowledge base and keeps script execution inside the skills.
4. Project purpose, evidence model, architecture, and release flow.
5. Harness quickstart, contribution guidance, and license.

The localized documents mirror this order so readers can switch language
without losing the primary navigation path.

### Link contract

- Root README links to `docs/README.pt-BR.md` and `docs/README.es.md`.
- Each localized README links back to `../README.md` and to the other localized README.
- All three README files link to `skills/intel-docs-reader/SKILL.md` and
  `skills/intel-hardware-advisor/SKILL.md` from their own relative location.
- The test resolves every declared target from the file containing the link.

### Content contract

The catalog must name both skills, explain when to use each one, and retain
the safety/evidence caveats. Translation may change prose but not commands,
paths, schema names, or skill identifiers.
