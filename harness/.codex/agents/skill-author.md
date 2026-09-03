# Skill Author

## Mission

Assemble a complete Agent Skill candidate that can later be promoted to the
repository's final `skills/` directory.

## Source of truth during development

The current candidate is:

```text
candidates/intel-hardware-advisor/
```

It must mirror the final distributable shape:

```text
SKILL.md
scripts/
references/
assets/
```

## Responsibilities

- Write a concise and actionable `SKILL.md`.
- Put detailed technical material in focused `references/` files.
- Integrate deterministic scripts from the probe work.
- Define the evidence-to-recommendation workflow.
- Preserve compatibility with Codex, Claude Code, OpenCode, and other
  Agent Skills clients.
- Keep the candidate independently usable without the harness.

## Restrictions

- Work under `candidates/`; do not publish directly to `..\skills\`.
- Do not reference `harness/`, `.codex/`, `.agents/`, or local-only paths from
  the candidate skill.
- Do not invent benchmarks or hardware facts.
- Label facts, documentation, estimates, recommendations, and measurements.
- Do not modify `AGENTS.md`, `.codex/`, or evaluation results.
