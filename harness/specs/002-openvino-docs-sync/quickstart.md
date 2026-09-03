# Quickstart: OpenVINO Documentation Cache

## Explicitly update the working cache

From the harness root, after connecting a real browser:

```powershell
python scripts/openvino_docs_sync.py --update --publish-snapshot
```

The default source is `https://docs.openvino.ai/2026/index.html` and the
working output is `docs/openvino/`. The command runs extraction and verification
and stops if browser access or the coverage gate is unavailable.

## Read the local snapshot

From the candidate skill directory:

```powershell
python scripts/read_openvino_docs.py --query "OpenVINO NPU"
```

This command is local-only. If the snapshot is missing or incomplete, request
an explicit documentation update; the reader does not download automatically.

## Refresh policy

Ask for an update when the user says “atualizar a documentação do OpenVINO”,
“baixar a documentação do OpenVINO”, or gives an equivalent explicit command.
Normal OpenVINO questions use the last reviewed snapshot.
