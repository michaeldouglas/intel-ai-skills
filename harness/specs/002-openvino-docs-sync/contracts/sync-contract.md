# Synchronization and Reader Contract

## Synchronization command

The only network-capable repository command is explicit:

```text
python scripts/openvino_docs_sync.py --update
```

Useful options are `--start-url`, `--output-dir`, `--force`, `--page-limit`,
`--request-delay`, `--deps-dir`, and `--publish-snapshot`. Invoking the command
without `--update` is a no-op/help path. `--verify-only` performs no download.

Successful synchronization requires:

1. a rendered-browser extraction;
2. generated `index.md` and `manifest.json`;
3. the extractor verification command to exit successfully; and
4. no unrecognized existing content to be overwritten.

## Reader command

```text
python scripts/read_openvino_docs.py --query "NPU device"
```

The reader searches only its local `references/openvino/` directory by default.
It returns cache status, ranked Markdown matches, local paths, source URLs, and
limitations. It MUST NOT invoke the sync command, browser, network, package
installer, or arbitrary filesystem scan.
