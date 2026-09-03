---
name: openvino-docs-reader
description: Read and cite the reviewed local OpenVINO documentation snapshot without downloading pages or opening a browser during normal questions.
---

# OpenVINO Documentation Reader

Use this skill for questions about OpenVINO APIs, devices, plugins, setup,
configuration, model conversion, and documented limitations when a local
snapshot is available.

## Default behavior

The reader is local-only. It searches the bundled
`references/openvino/` Markdown snapshot and never downloads documentation,
opens a browser, invokes the synchronization agent, or falls back to an
uncaptured web page during an ordinary question.

Run a local search from this skill's directory:

```text
python scripts/read_openvino_docs.py --query "NPU device"
python scripts/read_openvino_docs.py --query "NPU device" --format json
```

For every useful result, cite both the relative Markdown path and the
`source_url` from its frontmatter. Disclose the cache status, extraction date,
coverage, skipped pages, or missing metadata before presenting the content as
authoritative.

## When the cache is missing or incomplete

Do not download automatically. Tell the user that the local OpenVINO snapshot
is missing or incomplete and ask whether they want to explicitly update it with
the `openvino-docs-sync` agent.

The update phrases are explicit requests such as “vamos atualizar a
documentação do OpenVINO” or “baixe novamente a documentação do OpenVINO”.

## Evidence boundaries

The snapshot contains third-party OpenVINO documentation and must retain its
source URLs, extraction date, attribution, and skipped-page notes. Distinguish
documented claims from local hardware detection, measurements, estimates, and
inferences. Do not extend a page's claim beyond its documented version or
hardware scope.
