<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/intel-ai-skills-logo-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="./assets/intel-ai-skills-logo-light.svg">
  <img src="./assets/intel-ai-skills-logo.svg" alt="Intel AI Skills" width="820">
</picture>

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
| **Intel Hardware Advisor** | Inspect a local Windows, Linux, or macOS inference environment and understand what the available evidence supports. | [`intel-hardware-advisor/SKILL.md`](./skills/intel-hardware-advisor/SKILL.md) |
| **Intel Docs Reader** | Search and cite the versioned local archive of official OpenVINO documentation. | [`intel-docs-reader/SKILL.md`](./skills/intel-docs-reader/SKILL.md) |
| **Intel OpenVINO Installer** | Choose, install, and verify OpenVINO Runtime with a documented method for the user's platform and ecosystem. | [`intel-openvino-installer/SKILL.md`](./skills/intel-openvino-installer/SKILL.md) |
| **Intel OpenVINO Model Converter** | Convert supported framework models to OpenVINO IR with explicit shapes and artifacts. | [`intel-openvino-model-converter/SKILL.md`](./skills/intel-openvino-model-converter/SKILL.md) |
| **Intel OpenVINO Inference Runner** | Compile and run models locally or in Docker while reporting devices and compatibility evidence. | [`intel-openvino-inference-runner/SKILL.md`](./skills/intel-openvino-inference-runner/SKILL.md) |
| **Intel OpenVINO Benchmark** | Measure reproducible latency and throughput across OpenVINO configurations. | [`intel-openvino-benchmark/SKILL.md`](./skills/intel-openvino-benchmark/SKILL.md) |
| **Intel OpenVINO Model Optimizer** | Plan quantization and weight compression while protecting original artifacts. | [`intel-openvino-model-optimizer/SKILL.md`](./skills/intel-openvino-model-optimizer/SKILL.md) |
| **Intel OpenVINO Model Server** | Validate local OpenVINO Model Server deployments with Docker, repositories, APIs, and health checks. | [`intel-openvino-model-server/SKILL.md`](./skills/intel-openvino-model-server/SKILL.md) |
| **Intel OpenVINO GenAI Runner** | Plan and verify text, chat, GGUF, VLM, speech, and other OpenVINO GenAI workflows. | [`intel-openvino-genai-runner/SKILL.md`](./skills/intel-openvino-genai-runner/SKILL.md) |

### Intel Hardware Advisor

Use this skill when your agent needs to understand the local inference
environment before selecting an Intel execution path. It performs read-only
discovery, separates platform facts from runtime facts, follows evidence
identifiers, and keeps `unknown`, `unavailable`, and `no_decision` outcomes
visible.

It does not install packages, change drivers, run benchmarks, scan arbitrary
files, or infer model compatibility, latency, throughput, memory savings, or
precision support from a device name alone.

It also reports lightweight GPU, NPU, GenAI, OpenCV, and execution-context
configuration statuses; detailed support and setup questions belong to the
versioned Docs Reader.

### Intel Docs Reader

Use this skill when your agent needs authoritative OpenVINO documentation
about APIs, devices, setup, configuration, or documented limitations. It uses
a local cache and cites the source page for useful results.

### Intel OpenVINO Installer

Use this skill when your agent needs to choose, install, or verify OpenVINO
Runtime. It selects a documented method for the platform and ecosystem,
previews the commands, asks for confirmation before changing the machine, and
reports installation and runtime verification separately.

### Runtime workflow skills

After the runtime is ready, use the focused skills for model conversion,
inference, benchmarking, optimization, local Model Server validation, and
GenAI workflows. Each one invokes its own bundled script and keeps its scope
independent.

## Quickstart

### Install for your agent

Use the command for each skill you want to add. The example targets Codex;
replace `codex` with `claude-code` or another supported agent when needed.

```bash
npx skills add michaeldouglas/intel-ai-skills --skill intel-hardware-advisor -a codex
npx skills add michaeldouglas/intel-ai-skills --skill intel-docs-reader -a codex
npx skills add michaeldouglas/intel-ai-skills --skill intel-openvino-installer -a codex
npx skills add michaeldouglas/intel-ai-skills --skill intel-openvino-model-converter -a codex
npx skills add michaeldouglas/intel-ai-skills --skill intel-openvino-inference-runner -a codex
npx skills add michaeldouglas/intel-ai-skills --skill intel-openvino-benchmark -a codex
npx skills add michaeldouglas/intel-ai-skills --skill intel-openvino-model-optimizer -a codex
npx skills add michaeldouglas/intel-ai-skills --skill intel-openvino-model-server -a codex
npx skills add michaeldouglas/intel-ai-skills --skill intel-openvino-genai-runner -a codex
```

Or install all nine skills in one command:

```bash
npx skills add michaeldouglas/intel-ai-skills --skill intel-hardware-advisor --skill intel-docs-reader --skill intel-openvino-installer --skill intel-openvino-model-converter --skill intel-openvino-inference-runner --skill intel-openvino-benchmark --skill intel-openvino-model-optimizer --skill intel-openvino-model-server --skill intel-openvino-genai-runner -a codex
```

### Use the installed skills

After installation, ask your agent to inspect the hardware or answer an
OpenVINO question. The skill invokes its bundled scripts automatically. You do
not need to change directories or execute Python scripts manually.

### Preview the documentation site locally

The public documentation site lives in `docs/site/`. The existing Markdown
files directly under `docs/` remain independent and untouched. To build and preview the same
artifact used by GitHub Pages, run this from the repository root:

```bash
python docs/site/scripts/serve_site.py
```

Then open `http://127.0.0.1:8000/`. The site build validates the published
skill catalog, internal links, and logo assets before starting the local server.
Changes merged into `main` run the same build through
`.github/workflows/deploy-pages.yml` and publish the generated site to GitHub
Pages.

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
