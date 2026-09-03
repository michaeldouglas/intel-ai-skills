## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

When the user types `/graphify`, use the installed graphify skill or instructions before doing anything else.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- Dirty graphify-out/ files are expected after hooks or incremental updates; dirty graph files are not a reason to skip graphify. Only skip graphify if the task is about stale or incorrect graph output, or the user explicitly says not to use it.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).

## Branch and pull-request policy

All changes MUST be developed on a branch named `feature/<kebab-case-name>`.
Feature branches MUST target `develop` through a pull request. The `main`
branch MUST receive changes only through a pull request whose source is exactly
`develop`; direct commits and direct pushes to `main` are forbidden.

The normal flow is:

```text
feature/<name> -> develop -> main
```

Before starting work, ask which branch to use. If a new feature branch is
approved, sync `develop` and create it from there, then implement the change
in the local repository. The intended changes MUST be
committed locally and pushed with Git before opening the first PR against
`develop`; opening a PR is the final step after the remote feature ref exists.
After that PR is merged and the integrated state is validated, GitHub Actions
automatically opens or reuses a promotion PR from `develop` to `main`. Do not
open a feature PR directly against `main`.

Before creating or switching to a branch, the agent MUST ask which branch the
user wants to use. If the user names an existing compliant `feature/...`
branch, the agent MUST reuse it and MUST NOT create another branch. A new
branch may be created only after the user requests one or confirms the proposed
branch name. If the user selects `develop` or `main` for implementation work,
the agent MUST explain the protection rule and ask for a compliant feature
branch or an explicitly documented exception.

Every feature must also follow the Spec Kit sequence documented in the project
constitution: specification, clarification when needed, plan, tasks,
analysis, implementation, evaluation, and quality review. Branch policy is
enforced by `.github/workflows/branch-policy.yml` and project checks are run by
the quality-gate workflow.

### Publication consent

The agent MUST keep the local repository and the remote repository as separate
steps. It MAY prepare and commit intended changes locally, but MUST NOT run
`git push`, publish a branch, or open/update a pull request silently.

When a change set is broad (multiple files or commits, workflow/configuration
changes, generated artifacts, or changes across more than one project area),
the agent MUST stop after the local commit and ask for explicit confirmation
before publishing. The question should summarize the branch, commit(s), file
count, and destination, for example: "A alteração está commitada localmente
em `feature/<name>`. Deseja que eu faça o push e abra o PR para `develop`?"

After explicit confirmation, the agent MUST push the existing local branch
with Git first and only then create or update the pull request. GitHub MCP may
be used for the PR operation after the push; it MUST NOT replace the local
commit-and-push sequence.

## Skill factory workflow

This directory is the internal engineering harness. Its job is to research,
generate, test, evaluate, and review Agent Skills before release.

The final distributable skills live in the sibling directory:

```text
..\skills\
```

For the current feature, the candidate and release paths are:

```text
harness/candidates/intel-hardware-advisor/
skills/intel-hardware-advisor/
```

The candidate must pass validation, automated tests, evaluations, and quality
review before it is promoted to `skills/`. The final skill must not depend on
`harness/`, `.codex/`, `.agents/`, or any other internal project file.

## Sub-agent responsibilities

Sub-agents are defined in `.codex/agents/`. The primary agent coordinates them
and remains responsible for the final decision.

- `openvino-researcher`: research authoritative, versioned OpenVINO and Intel
  hardware evidence; write research artifacts under `research/` only.
- `openvino-docs-sync`: refresh the generated OpenVINO documentation cache
  under `docs/openvino/` only after an explicit request; use the
  `extract-spa-docs` browser workflow and do not own candidate skill content.
- `hardware-probe-engineer`: build deterministic hardware probes and fixtures;
  write candidate scripts and harness tests, but do not own the candidate
  `SKILL.md`.
- `skill-author`: assemble the distributable skill candidate under
  `candidates/`; keep product content independent from the harness.
- `evaluation-engineer`: create and run tests, fixtures, and recommendation
  evaluations under `tests/`, `fixtures/`, and `evaluations/`.
- `skill-quality-reviewer`: perform a read-only conformance, portability,
  security, and release-readiness review.
- `skill-release-manager`: promote only an approved candidate from
  `candidates/` to the sibling `..\skills\` directory, then validate the final
  copy again.
- `git-workflow-manager`: own branch selection, local Git status, local
  commits, publication consent, Git pushes, and pull-request coordination;
  never edit product files or bypass the branch policy.

Do not run multiple write-capable agents against the same files concurrently.
Keep the main skill author as the single owner of the candidate `SKILL.md`,
and treat the release manager as the only normal writer to the final
`skills/` directory.
