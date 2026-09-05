# Research: OpenVINO Runtime Skills Suite

## Research scope

The local archive under `harness/docs/2026/` is authoritative for this feature.
The skills are designed around documented workflows rather than inferred
capabilities or current internet pages.

## Evidence map

| Skill | Primary local documentation | Scope captured |
|---|---|---|
| Model Converter | `openvino-workflow/model-preparation.html` and `model-preparation/` | Framework conversion, IR generation, conversion parameters, input shapes |
| Inference Runner | `openvino-workflow/running-inference.html` and `running-inference/` | Core, model compilation, input/output, CPU/GPU/NPU, AUTO, MULTI, HETERO, dynamic shapes, preprocessing |
| Benchmark | `about-openvino/performance-benchmarks/` and `get-started/learn-openvino/openvino-samples/*benchmark*` | Latency, throughput, benchmark methodology, reproducible configuration |
| Model Optimizer | `openvino-workflow/model-optimization.html` and `model-optimization-guide/` | Post-training quantization, accuracy control, QAT, weight compression, 4-bit and microscaling |
| Model Server | `model-server/ovms_what_is_openvino_model_server.html`, `ovms_docs_deploying_server_docker.html`, `ovms_docs_serving_model.html` | Local/Docker server, model repository, classic models, endpoints, metrics, troubleshooting |
| GenAI Runner | `openvino-workflow-generative/inference-with-genai.html` and `inference-with-genai-on-npu.html` | Chat, GGUF, GenAI API, text/VLM/speech workflows, NPU prerequisites |

## Decisions

1. Keep Docker test execution in the inference runner and Model Server rather
   than creating a separate generic Docker skill.
2. Keep conversion and optimization separate because their evidence, risks,
   and acceptance checks differ.
3. Keep model compatibility as a compile/inference result, not a promise made
   by the hardware advisor.
4. Treat unavailable tools, missing model assets, unsupported operations, and
   driver prerequisites as explicit report states.
5. Use plan/apply/verify for conversion, optimization, and server workflows;
   benchmark and inference runs remain non-destructive unless a user requests
   output generation or container startup.

## Known limitations

- A local fixture cannot prove physical GPU/NPU performance.
- Docker image tags and hardware passthrough remain version- and host-specific;
  the skills must not invent tags or claim accelerator access.
- GenAI model assets may require separate downloads, licenses, or conversion;
  the runner must show those prerequisites instead of hiding them.
