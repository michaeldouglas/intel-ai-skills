<div align="center">

<img src="./assets/intel-ai-skills-logo.svg" alt="Intel AI Skills" width="820">

<p><strong>Evidence-first agent skills for Intel AI and OpenVINO workloads.</strong></p>

<p>
  <a href="https://github.com/michaeldouglas/intel-ai-skills/actions/workflows/quality-gates.yml"><img src="https://github.com/michaeldouglas/intel-ai-skills/actions/workflows/quality-gates.yml/badge.svg?branch=develop" alt="Quality gates"></a>
  <a href="https://github.com/michaeldouglas/intel-ai-skills/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-Apache--2.0-2ea44f?style=flat-square" alt="Apache 2.0 license"></a>
</p>

<p>
  <a href="#available-skills">Skills</a> ·
  <a href="#quickstart">Quickstart</a> ·
  <a href="#why-intel-ai-skills">Why this project</a>
</p>

<p>
  <a href="./docs/README.pt-BR.md">🇧🇷 Português (Brasil)</a> ·
  <a href="./docs/README.es.md">🇪🇸 Español</a>
</p>

</div>

> **Build with evidence. Deploy with confidence.**

This repository publishes portable Agent Skills for Intel hardware, OpenVINO
runtimes, and evidence-aware AI workload decisions. Install the skill you need
and let your agent use it when the task requires it.

## Available skills

The published skills live in [`skills/`](./skills/). Each one is self-contained
and can be installed independently.

| Skill | Use it when you need | Documentation |
|---|---|---|
| **Intel Hardware Advisor** | Inspect a local Windows or Linux inference environment and understand what the available evidence supports. | [`intel-hardware-advisor/SKILL.md`](./skills/intel-hardware-advisor/SKILL.md) |
| **Intel Docs Reader** | Search and cite the versioned local archive of official OpenVINO documentation. | [`intel-docs-reader/SKILL.md`](./skills/intel-docs-reader/SKILL.md) |

### Intel Hardware Advisor

Use this skill when your agent needs to understand the local inference
environment before selecting an Intel execution path. It performs read-only
discovery, separates platform facts from runtime facts, follows evidence
identifiers, and keeps `unknown`, `unavailable`, and `no_decision` outcomes
visible.

It does not install packages, change drivers, run benchmarks, scan arbitrary
files, or infer model compatibility, latency, throughput, memory savings, or
precision support from a device name alone.

### Intel Docs Reader

Use this skill when your agent needs authoritative OpenVINO documentation
about APIs, devices, setup, configuration, or documented limitations. It uses
a local cache and cites the source page for useful results.

## Quickstart

### Install for your agent

Use the command for each skill you want to add. The example targets Codex;
replace `codex` with `claude-code` or another supported agent when needed.

```bash
npx skills add michaeldouglas/intel-ai-skills --skill intel-hardware-advisor -a codex
npx skills add michaeldouglas/intel-ai-skills --skill intel-docs-reader -a codex
```

Or install both skills in one command:

```bash
npx skills add michaeldouglas/intel-ai-skills --skill intel-hardware-advisor --skill intel-docs-reader -a codex
```

### Use the installed skills

After installation, ask your agent to inspect the hardware or answer an
OpenVINO question. The skill invokes its bundled scripts automatically. You do
not need to change directories or execute Python scripts manually.

## Why Intel AI Skills?

AI workloads are increasingly heterogeneous. The same model can behave very
differently depending on the processor, accelerator, runtime version, driver,
precision, memory budget, and deployment target.

Intel AI Skills turns that complexity into a disciplined workflow:

- **Hardware-aware** — discover the local platform and runtime instead of guessing from a device name.
- **Evidence-qualified** — separate detected facts, official documentation, measurements, estimates, and inferences.
- **Portable by design** — each published skill is self-contained and independent.
- **Deterministic** — make the same fixture produce the same answer on every machine and in every pull request.
- **Privacy-first** — collect only what is needed and never inspect secrets or unrelated files.
- **Honest about uncertainty** — an unknown result is valid when evidence is incomplete, conflicting, stale, or unavailable.

## How the skills work

```text
Local environment or OpenVINO question
                  │
                  ▼
Agent invokes the installed skill and its bundled scripts
                  │
                  ▼
Facts + sources + confidence → Qualified guidance
```

## Safety and evidence

The skills are read-only by design where discovery is involved. They separate
detected facts, official documentation, measurements, estimates, and
inferences. Unknown, unavailable, or conflicting evidence remains visible
instead of being replaced with a guess.

## License

Distributed under the [Apache License 2.0](./LICENSE).
