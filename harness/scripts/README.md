# Documentation synchronization scripts

The OpenVINO documentation updater is intentionally explicit:

```powershell
python scripts/openvino_docs_sync.py --update
```

Without `--update`, the script does not contact the network and exits without
changing the cache. Use `--verify-only` to validate an existing generated cache
without downloading it. The default cache is `docs/openvino/`.

After a successful verification, `--publish-snapshot` may copy the generated
cache into the candidate reader's own `references/openvino/` directory. That
copy is protected by a generated-snapshot marker and must still pass the
candidate review before promotion to `skills/`.
