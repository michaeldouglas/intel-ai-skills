import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path


ROOT = Path(__file__).parents[2]
READER_DIR = ROOT / "candidates" / "openvino-docs-reader" / "scripts"
sys.path.insert(0, str(READER_DIR))

import read_openvino_docs as reader  # noqa: E402


def make_snapshot(root: Path, *, skipped=None):
    root.mkdir(parents=True)
    (root / "index.md").write_text(
        "---\ntitle: OpenVINO Docs\nsource_url: https://docs.openvino.ai/2026/index.html\nextracted_at: 2026-09-03\n---\n# OpenVINO Docs\n",
        encoding="utf-8",
    )
    (root / "manifest.json").write_text(
        json.dumps(
            {
                "coverage": {"discovered": 2, "extracted": 2, "skipped": skipped or []},
                "source_url": "https://docs.openvino.ai/2026/index.html",
                "extracted_at": "2026-09-03",
            }
        ),
        encoding="utf-8",
    )
    (root / "npu.md").write_text(
        "---\ntitle: NPU Plugin\nsource_url: https://docs.openvino.ai/2026/openvino_docs_OVUG\nextracted_at: 2026-09-03\n---\n# NPU Plugin\nConfigure the OpenVINO NPU device and inspect supported properties.\n",
        encoding="utf-8",
    )


class OpenVinoDocsReaderTests(unittest.TestCase):
    def test_query_returns_local_citation_and_source_url(self):
        with tempfile.TemporaryDirectory() as directory:
            snapshot = Path(directory) / "openvino"
            make_snapshot(snapshot)
            result = reader.search_docs("NPU device", snapshot)
            self.assertEqual(result["cache_status"], "valid")
            self.assertEqual(result["matches"][0]["local_path"], "npu.md")
            self.assertIn("https://docs.openvino.ai", result["matches"][0]["source_url"])

    def test_missing_cache_is_reported_without_network_fallback(self):
        with tempfile.TemporaryDirectory() as directory:
            result = reader.search_docs("runtime", Path(directory) / "missing")
            self.assertEqual(result["cache_status"], "missing")
            self.assertEqual(result["matches"], [])
            self.assertTrue(any("update" in item.lower() for item in result["limitations"]))

    def test_skipped_pages_make_limitation_visible(self):
        with tempfile.TemporaryDirectory() as directory:
            snapshot = Path(directory) / "openvino"
            make_snapshot(snapshot, skipped=["https://docs.openvino.ai/2026/skipped"])
            result = reader.search_docs("NPU", snapshot)
            self.assertEqual(result["cache_status"], "incomplete")
            self.assertTrue(result["limitations"])

    def test_reader_source_has_no_sync_or_network_capability(self):
        source = (READER_DIR / "read_openvino_docs.py").read_text(encoding="utf-8")
        for forbidden in ("openvino_docs_sync", "subprocess", "requests", "urllib", "httpx"):
            self.assertNotIn(forbidden, source)

    def test_reader_cli_uses_the_same_local_only_path(self):
        with tempfile.TemporaryDirectory() as directory:
            snapshot = Path(directory) / "openvino"
            make_snapshot(snapshot)
            output = StringIO()
            with redirect_stdout(output):
                code = reader.main(["--query", "NPU", "--docs-dir", str(snapshot), "--format", "json"])
            self.assertEqual(code, 0)
            self.assertEqual(json.loads(output.getvalue())["matches"][0]["local_path"], "npu.md")


if __name__ == "__main__":
    unittest.main()
