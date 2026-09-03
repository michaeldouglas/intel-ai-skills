# Data Model: On-Demand OpenVINO Documentation

## Documentation Cache

Generated folder under `docs/openvino/` containing Markdown pages, `index.md`,
`manifest.json`, and optional downloaded linked documents under `assets/`.

## Extraction Manifest

The extractor-owned `manifest.json` is preserved as the cache's primary
metadata. The sync utility requires enough information to identify generated
output and expose:

```text
source URL
extraction date
coverage (discovered/extracted/skipped or equivalent)
page list
skipped pages
linked documents
verification result
attribution notes
```

## Reader Snapshot Marker

The snapshot-owned `.openvino-snapshot.json` contains:

```json
{
  "schema_version": "1",
  "source_url": "https://docs.openvino.ai/2026/index.html",
  "cache_source": "docs/openvino",
  "copied_at": "YYYY-MM-DD",
  "manifest_sha256": "..."
}
```

The marker is not a replacement for the extractor manifest; it records how the
reviewed copy was produced.

## Reader Result

```text
cache_status: valid | missing | incomplete | invalid
query: user query
matches: [{title, local_path, source_url, score, excerpt}]
limitations: list of disclosures
```

The reader returns no matches with an actionable limitation when the snapshot
is missing or invalid. It never treats a missing cache as permission to fetch
the website.
