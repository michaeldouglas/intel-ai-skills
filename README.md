<div align="center">

<img src="./assets/intel-ai-skills-logo.svg" alt="Intel AI Skills" width="820">

<p><strong>Evidence-first agent skills for Intel AI and OpenVINO workloads.</strong></p>

<p>
  <a href="https://github.com/michaeldouglas/intel-ai-skills/actions/workflows/quality-gates.yml"><img src="https://github.com/michaeldouglas/intel-ai-skills/actions/workflows/quality-gates.yml/badge.svg?branch=develop" alt="Quality gates"></a>
  <a href="https://github.com/michaeldouglas/intel-ai-skills/actions/workflows/branch-policy.yml"><img src="https://github.com/michaeldouglas/intel-ai-skills/actions/workflows/branch-policy.yml/badge.svg?branch=develop" alt="Branch policy"></a>
  <a href="https://github.com/michaeldouglas/intel-ai-skills/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-Apache--2.0-2ea44f?style=flat-square" alt="Apache 2.0 license"></a>
  <a href="https://github.com/michaeldouglas/intel-ai-skills"><img src="https://img.shields.io/github/stars/michaeldouglas/intel-ai-skills?style=flat-square&logo=github" alt="GitHub stars"></a>
</p>

<p>
  <a href="#available-skills">Skills</a> ·
  <a href="#quickstart">Quickstart</a> ·
  <a href="#why-intel-ai-skills">Project</a> ·
  <a href="#contributing">Contributing</a>
</p>

<p>
  <a href="./docs/README.pt-BR.md">🇧🇷 Português (Brasil)</a> ·
  <a href="./docs/README.es.md">🇪🇸 Español</a>
</p>

</div>

> **Build with evidence. Deploy with confidence.**

This repository publishes portable Agent Skills for Intel hardware,
OpenVINO runtimes, and evidence-aware AI workload decisions. Start with the
skills below; the engineering harness and release workflow are documented
after the product guidance.

## Available skills

The published skills live in [`skills/`](./skills/). Each one is self-contained
and can be copied or installed independently of the internal harness.

| Skill | Use it when you need to | Documentation |
|---|---|---|
| **Intel Hardware Advisor** | Inspect a local Windows or Linux inference environment and understand what the available evidence supports. | [`skills/intel-hardware-advisor/SKILL.md`](./skills/intel-hardware-advisor/SKILL.md) |
| **Intel Docs Reader** | Search and cite the versioned local archive of official OpenVINO documentation. | [`skills/intel-docs-reader/SKILL.md`](./skills/intel-docs-reader/SKILL.md) |

### Intel Hardware Advisor

Use this skill for first diagnosis of an inference environment. It performs
read-only discovery, separates platform facts from runtime facts, follows
evidence identifiers, and keeps `unknown`, `unavailable`, and `no_decision`
outcomes visible.

It does not install packages, change drivers, run benchmarks, scan arbitrary
files, or infer model compatibility, latency, throughput, memory savings, or
precision support from a device name alone.

```bash
cd skills/intel-hardware-advisor
python scripts/hardware_probe.py --format text
python scripts/hardware_probe.py --format json
```

Read the complete behavior and safety contract in
[`intel-hardware-advisor/SKILL.md`](./skills/intel-hardware-advisor/SKILL.md).

### Intel Docs Reader

Use this skill when a question needs authoritative OpenVINO documentation
about APIs, devices, setup, configuration, or documented limitations. The
reader uses a local cache and reports the source page for useful results.

```bash
cd skills/intel-docs-reader
python scripts/read_openvino_docs.py --query "NPU device"
python scripts/read_openvino_docs.py --query "NPU device" --offline
```

The skill does not download anything at installation time. If its cache is
missing, the first online query retrieves the configured official archive into
the user's local cache, outside the installed skill and repository.

Read the complete source and version-boundary contract in
[`intel-docs-reader/SKILL.md`](./skills/intel-docs-reader/SKILL.md).

## Quickstart

### Use the published skills

Clone the repository and run either skill from its own directory:

```bash
git clone https://github.com/michaeldouglas/intel-ai-skills.git
cd intel-ai-skills

python skills/intel-hardware-advisor/scripts/hardware_probe.py --format json
python skills/intel-docs-reader/scripts/read_openvino_docs.py --query "NPU device"
```

For deterministic hardware validation, pass a sanitized fixture to the
hardware advisor. A fixture is a test input, not a runtime dependency of the
published skill:

```bash
python skills/intel-hardware-advisor/scripts/hardware_probe.py \
  --fixture path/to/sanitized-fixture.json \
  --format json
```

### Run the engineering harness

The harness validates candidates before they are released to `skills/`:

```bash
cd harness
python -m venv .venv
source .venv/bin/activate             # macOS/Linux
# .venv\Scripts\Activate.ps1          # Windows PowerShell

python -m pip install --upgrade pip pytest
python -m pytest -q
```

The deterministic suite is designed to run without Intel hardware, OpenVINO,
internet access, or access to secrets. Live hardware checks are supplemental.

## Why Intel AI Skills?

AI workloads are increasingly heterogeneous. The same model can behave very
differently depending on the processor, accelerator, runtime version, driver,
precision, memory budget, and deployment target.

Intel AI Skills turns that complexity into a disciplined workflow:

- **Hardware-aware** — discover the local platform and runtime instead of guessing from a device name.
- **Evidence-qualified** — separate detected facts, official documentation, measurements, estimates, and inferences.
- **Portable by design** — keep product skills independent from the internal engineering harness.
- **Deterministic** — make the same fixture produce the same answer on every machine and in every pull request.
- **Privacy-first** — collect only what is needed and never inspect secrets or unrelated files.
- **Honest about uncertainty** — an unknown result is valid when evidence is incomplete, conflicting, stale, or unavailable.

## What makes this different?

```text
Local environment
      │
      ▼
Read-only discovery → Facts + sources + confidence → Qualified guidance
      │                                      │
      └──────────────→ Unknown stays unknown ┘
```

The project moves from research to a distributable skill through explicit
artifacts, reproducible fixtures, automated tests, evaluation, and review.

## Architecture

```text
intel-ai-skills/
├── harness/
│   ├── .specify/             # Constitution and Spec Kit project memory
│   ├── candidates/           # Skills under active development
│   ├── evaluations/          # Recommendation and behavior evaluations
│   ├── fixtures/             # Sanitized, reproducible environments
│   ├── research/             # Versioned evidence and technical research
│   ├── specs/                # Feature specifications, plans, and tasks
│   └── tests/                # Unit, contract, and integration tests
├── skills/                   # Reviewed, distributable Agent Skills
├── docs/                     # Localized project documentation
├── .github/workflows/        # Branch policy and quality automation
├── CONTRIBUTING.md           # Contribution and promotion flow
└── LICENSE                   # Apache License 2.0
```

The separation is deliberate:

1. Research establishes what is documented and what is still unknown.
2. Spec Kit turns requirements into an explicit design and task sequence.
3. Candidate skills implement product behavior inside the harness.
4. Fixtures and tests make behavior reproducible across supported platforms.
5. Evaluations and read-only quality review gate promotion.
6. Only reviewed artifacts reach `skills/`.

## Branch and release flow

Every change follows this path:

```mermaid
flowchart LR
    F[feature/name] -->|PR + checks| D[develop]
    D -->|automatic promotion PR| M[main]
    M --> R[release-ready]

    style F fill:#102a43,stroke:#6ee7f9,color:#fff
    style D fill:#16213e,stroke:#f59e0b,color:#fff
    style M fill:#163b2f,stroke:#34d399,color:#fff
    style R fill:#163b2f,stroke:#34d399,color:#fff
```

- Work starts on `feature/<kebab-case-name>`.
- Feature pull requests target `develop`.
- After a feature enters `develop`, GitHub Actions opens or reuses a PR to `main` automatically.
- The promotion PR is reviewed and merged manually.
- Direct commits and direct pushes to `main` are not part of the workflow.

Read the complete process in [`CONTRIBUTING.md`](./CONTRIBUTING.md).

## Spec Kit + Graphify

This project combines two complementary ways to keep engineering work clear:

| System | Role |
|---|---|
| **Spec Kit** | Turns a feature idea into a specification, plan, tasks, implementation, evaluation, and review trail. |
| **Graphify** | Provides scoped codebase navigation through concepts, relationships, paths, and cross-file structure. |

For a feature, the intended sequence is:

```text
Specify → Clarify → Plan → Tasks → Analyze → Implement → Evaluate → Review
```

Graphify's generated index is an engineering aid and may remain local; it is
refreshed after code or product-artifact changes and is not a substitute for
tests or review.

## Engineering principles

| Principle | What it means |
|---|---|
| **Evidence first** | Every claim has a source, measurement, or explicit inference. |
| **Portable skills** | Promoted skills cannot depend on internal harness files. |
| **Test before release** | Fixtures and negative cases are required for reliable behavior. |
| **Privacy by default** | Discovery is read-only and limited to the stated purpose. |
| **Uncertainty is data** | Unknown, unavailable, and conflicting evidence remain visible. |
| **Review-gated promotion** | Only tested and reviewed skills reach `skills/`. |

## Roadmap

- [x] Establish the research-to-release harness.
- [x] Define constitution, branch policy, Spec Kit flow, and quality gates.
- [x] Build the initial Intel Hardware Advisor candidate architecture.
- [x] Add deterministic fixture, contract, integration, and evaluation paths.
- [x] Publish the first skills: Intel Hardware Advisor and Intel Docs Reader.
- [ ] Expand version-scoped OpenVINO capability evidence.
- [ ] Add more Intel CPU, GPU, and NPU guidance scenarios.
- [ ] Publish richer examples and reusable skill integration patterns.

## Contributing

Ideas, bug reports, evidence improvements, fixtures, and new skills are
welcome. Before opening a change:

1. Create `feature/<kebab-case-name>` from `develop`.
2. Follow the Spec Kit artifacts for the feature.
3. Keep fixtures sanitized and reproducible.
4. Run the relevant tests and evaluations.
5. Commit the intended changes in the local repository.
6. Push the feature branch with Git.
7. Open the PR against `develop` and describe the evidence behind the change.

For agent-assisted work, broad changes are committed locally first. The agent
must ask for explicit confirmation before pushing a broad change set or
opening its PR; no remote publication happens silently.

Please read [`CONTRIBUTING.md`](./CONTRIBUTING.md) and the project
[constitution](./harness/.specify/memory/constitution.md) first.

## License

Distributed under the [Apache License 2.0](./LICENSE).

<div align="center">

**If reliable, explainable Intel AI tooling matters to you, ⭐ this project and help shape the next generation of agent skills.**

</div>
