<!--
Sync Impact Report
- Version change: 1.0.0 -> 1.1.0
- Modified principles: replaced all five placeholder principles with project
  rules for evidence, portability, testing, uncertainty, and release quality
- Added sections: Evidence, Privacy, and Portability Constraints; Development
  Workflow and Quality Gates; automatic develop-to-main promotion
- Removed sections: none; replaced only unresolved template content
- Follow-up TODO: confirm the original constitution ratification date
-->

# Intel AI Skills Harness Constitution

## Core Principles

### I. Evidence-First Recommendations
Every research finding and hardware recommendation MUST be traceable to an
authoritative source, a reproducible local measurement, or an explicitly
identified inference. Research artifacts MUST record the source, relevant
version or scope, access date, and any known limitations. The project MUST NOT
invent benchmark results, compatibility claims, memory requirements, or device
capabilities.

### II. Portable and Deterministic Skills
Each candidate skill MUST be independently usable after promotion to the
`skills/` directory and MUST NOT depend on `harness/`, `.codex/`, `.agents/`,
or other internal project files. Detection and probe behavior MUST be
deterministic, documented, and portable across supported operating systems.
Unavailable tools, unsupported platforms, permission failures, and unknown
hardware MUST produce explicit unknown or unavailable results rather than
fabricated values.

### III. Test-First Engineering
New behavior MUST have automated coverage before it is considered complete.
Tests MUST include sanitized fixtures for supported environments and negative
cases for missing tools, unsupported hardware, permission failures, and
uncertain results. Physical hardware MAY be used for supplemental validation,
but release readiness MUST NOT depend on access to a particular machine.

### IV. Privacy and Safe Discovery
Hardware discovery MUST collect only the information required for the stated
recommendation and MUST NOT collect secrets, arbitrary files, or unrelated
personal data. Scripts MUST avoid destructive operations, clearly report the
source and confidence of detected values, and handle command failures without
exposing sensitive environment contents.

### V. Review-Gated Release
No candidate skill MAY be promoted to the sibling `skills/` directory until
structural validation, automated tests, evaluations, and read-only quality
review have passed or their limitations have been documented. Write ownership
MUST remain separated between research, probes, candidate authoring,
evaluation, review, and release. A simpler design MUST be preferred when it
meets the requirements and evidence standard.

## Evidence, Privacy, and Portability Constraints

- Official Intel and OpenVINO documentation MUST be preferred for technical
  claims, with version and scope recorded when support varies by release or
  hardware SKU.
- Recommendations MUST distinguish detected facts, documented facts,
  inferences, estimates, measured benchmarks, and unavailable information.
- Fixture data MUST be sanitized and reproducible. It MUST NOT contain user
  names, credentials, machine identifiers, tokens, or arbitrary filesystem
  contents.
- Product content MUST use relative paths and self-contained scripts so that a
  promoted skill works outside this harness.

## Development Workflow and Quality Gates

Every feature MUST follow the Spec Kit sequence: specification, clarification
when needed, plan, task generation, consistency analysis, implementation,
evaluation, and quality review. Each stage MUST be reviewed before the next
stage begins when the workflow defines a review gate.

All feature work MUST use a branch named `feature/<kebab-case-name>`. Feature
branches MUST merge into `develop` through pull requests. Promotion to `main`
MUST happen through a pull request whose source branch is exactly `develop`.
Direct commits and direct pushes to `main` are prohibited. The repository's
branch protection settings are part of this requirement; the workflow check
alone is not a substitute for protected branches.

When changes enter `develop`, GitHub Actions MUST automatically open or reuse
the promotion pull request from `develop` to `main`. The promotion workflow
MUST NOT merge that pull request automatically.

The project MUST preserve the ownership boundaries defined in `AGENTS.md`:
researchers write research artifacts, probe engineers write probes and
fixtures, skill authors own candidate product files, evaluation engineers own
tests and evaluations, reviewers remain read-only, and the release manager is
the normal writer to the final `skills/` directory.

After code or product artifacts change, the Graphify index MUST be refreshed
with `graphify update .`. Releases MUST be checked for accidental inclusion of
temporary files, logs, secrets, fixtures not intended for distribution, or
dependencies on internal harness files.

## Governance

This constitution is authoritative for engineering and release decisions in
this harness. A change to a principle or mandatory constraint requires an
explicit constitution amendment, a sync impact report, and a semantic version
bump. Editorial clarifications that do not change obligations use a PATCH
bump; new or materially expanded obligations use a MINOR bump; removal or
incompatible redefinition of obligations uses a MAJOR bump.

All feature specifications, plans, tasks, evaluations, and release reviews
MUST be checked for compliance with this constitution. When a conflict exists,
the conflict MUST be resolved in the specification, plan, or tasks before
implementation. Exceptions MUST be documented with their scope, rationale,
risk, owner, and expiration or review condition.

**Version**: 1.1.0 | **Ratified**: TODO(RATIFICATION_DATE): confirm original adoption date | **Last Amended**: 2026-09-03
