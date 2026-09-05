# Feature Specification: OpenVINO Runtime Skills Suite

**Feature Branch**: `feature/openvino-runtime-skills`
**Created**: 2026-09-05
**Status**: Draft for implementation
**Input**: Create the next standalone skills required to move from hardware and runtime installation to model preparation, inference, measurement, serving, and GenAI workflows.

## Goal

Extend Intel AI Skills with six focused, agent-neutral skills that cover the
documented OpenVINO workflow after runtime installation without creating a
single super-skill or introducing dependencies between published skills.

## User Stories & Acceptance Scenarios

### US1 — Convert and prepare models (P1)

As a developer, I want to prepare a model for OpenVINO so that I can run it
with a documented and reproducible conversion plan.

**Acceptance Scenarios**

1. Given a PyTorch, ONNX, TensorFlow, Keras, PaddlePaddle, or JAX request,
   the converter selects the corresponding documented conversion profile.
2. Given an input-shape request, the converter shows the shape change and
   expected output artifacts before writing anything.
3. Given an unsupported framework or missing source model, the converter
   reports a blocked or partial result instead of guessing.

### US2 — Run inference on a selected device (P1)

As a developer, I want to execute a prepared model locally or in Docker and
know whether compilation, inference, and device access each succeeded.

**Acceptance Scenarios**

1. Given an OpenVINO model and a detected runtime, the runner reports model
   inputs, outputs, available devices, selected device, and inference status.
2. Given `AUTO`, `MULTI`, or `HETERO`, the runner preserves the requested mode
   and reports the effective device without claiming unsupported hardware.
3. Given a compile-only request, the runner validates model/device compatibility
   without running user inference.
4. Given Docker execution, the runner keeps the workspace and container
   configuration visible and does not mutate the host without confirmation.

### US3 — Measure performance (P1)

As an engineer, I want reproducible latency and throughput measurements so that
I can compare devices and configurations using evidence rather than guesses.

**Acceptance Scenarios**

1. Given a model, device, iterations, and batch size, the benchmark produces a
   report containing configuration, measurements, and limitations.
2. Given two device configurations, the benchmark compares them without
   presenting a benchmark as a universal hardware guarantee.
3. Given an unavailable benchmark tool or device, the report distinguishes
   unavailable measurements from poor performance.

### US4 — Optimize models (P1)

As a model owner, I want to plan quantization and weight compression while
keeping accuracy and original artifacts protected.

**Acceptance Scenarios**

1. Given post-training quantization, accuracy-control quantization, QAT, or
   weight compression, the optimizer selects the corresponding documented
   profile.
2. The optimizer requires confirmation before generating or replacing artifacts.
3. The report identifies accuracy evaluation as required evidence and never
   claims that a compressed model is equivalent without measurements.

### US5 — Serve models (P1)

As a developer, I want to serve an OpenVINO model through OpenVINO Model Server
in Docker so that I can validate a local service before production deployment.

**Acceptance Scenarios**

1. Given a model repository, the server skill shows image, volumes, ports,
   model versions, and health/API verification commands before starting Docker.
2. Given a confirmed Docker plan, it starts or verifies only the requested
   local server resources and reports endpoints and health separately.
3. Given a missing model, image, volume, or port, it reports the blocker without
   deleting existing repositories or containers.

### US6 — Run GenAI workflows (P2)

As a GenAI developer, I want to run documented OpenVINO GenAI workflows and
understand device and generation metrics without confusing them with classic
model inference.

**Acceptance Scenarios**

1. Given a text, chat, GGUF, VLM, speech, embedding, or image-generation
   request, the runner selects the corresponding documented profile.
2. Given an NPU request, the runner reports prerequisites and troubleshooting
   separately from successful model loading.
3. Given unavailable GenAI packages or model assets, the runner stops with an
   explicit partial or blocked result and does not download arbitrary assets.

## Functional Requirements

- **FR-001**: Publish exactly six new skills named `intel-openvino-model-converter`,
  `intel-openvino-inference-runner`, `intel-openvino-benchmark`,
  `intel-openvino-model-optimizer`, `intel-openvino-model-server`, and
  `intel-openvino-genai-runner`.
- **FR-002**: Each skill MUST contain a valid `SKILL.md`, a bundled script, and
  a focused reference file when detailed routing is needed.
- **FR-003**: Each skill MUST invoke its own bundled script automatically and
  MUST NOT ask users to change directories or execute internal scripts.
- **FR-004**: Each skill MUST be usable without `harness/`, `.codex/`,
  `.agents/`, another published skill, or a project-specific path.
- **FR-005**: Mutating workflows MUST expose a plan, require explicit
  confirmation, and report apply and verification separately.
- **FR-006**: Reports MUST use stable JSON keys for context, request, plan,
  execution, verification, warnings, and issues.
- **FR-007**: Scripts MUST redact secrets, avoid arbitrary environment dumps,
  and preserve unknown, unavailable, blocked, and partial outcomes.
- **FR-008**: Documentation and references MUST use the versioned local OpenVINO
  2026 archive as the research source and record the relevant page paths.
- **FR-009**: The inference runner MUST cover classic device modes and Docker
  execution without installing drivers or changing BIOS/global host settings.
- **FR-010**: The benchmark MUST report measured configuration and MUST NOT
  convert a local measurement into an unconditional device recommendation.
- **FR-011**: The optimizer MUST protect original model artifacts and identify
  accuracy validation as a separate required step.
- **FR-012**: The model-server skill MUST focus its first release on local and
  Docker OpenVINO Model Server workflows; Kubernetes and production security
  remain documented boundaries rather than hidden automation.
- **FR-013**: The GenAI runner MUST keep model assets, package installation,
  generation metrics, and NPU prerequisites explicit.
- **FR-014**: Public English, Portuguese, and Spanish README catalogs MUST list
  all published skills and provide agent-neutral installation commands.

## Non-Goals

- Automatic driver, BIOS, kernel, WSL, or global environment configuration.
- A universal model compatibility guarantee based only on a device name.
- Automatic deletion or replacement of models, repositories, containers, or
  benchmark results.
- A single skill that combines conversion, optimization, inference, benchmark,
  serving, and GenAI.
- Kubernetes orchestration, cloud provisioning, or production secret management
  in the first model-server release.

## Success Criteria

- **SC-001**: All six skills pass structural validation and have no references
  to internal harness paths.
- **SC-002**: Every skill has deterministic plan, success, and negative fixtures
  with automated coverage.
- **SC-003**: The full repository test suite passes, including documentation
  link and installation checks.
- **SC-004**: A user can install all nine skills with one `npx skills add`
  command for a supported agent.
- **SC-005**: The skills clearly separate installation, conversion, execution,
  measurement, optimization, serving, and GenAI evidence.
- **SC-006**: Each final skill can be copied outside this repository and still
  locate and invoke its own bundled script.
