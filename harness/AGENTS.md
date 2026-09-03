## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

When the user types `/graphify`, use the installed graphify skill or instructions before doing anything else.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- Dirty graphify-out/ files are expected after hooks or incremental updates; dirty graph files are not a reason to skip graphify. Only skip graphify if the task is about stale or incorrect graph output, or the user explicitly says not to use it.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).

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

Do not run multiple write-capable agents against the same files concurrently.
Keep the main skill author as the single owner of the candidate `SKILL.md`,
and treat the release manager as the only normal writer to the final
`skills/` directory.
