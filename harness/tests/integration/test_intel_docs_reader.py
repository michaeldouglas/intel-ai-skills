import json
import sys
import tempfile
import unittest
import zipfile
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path


ROOT = Path(__file__).parents[2]
READER_DIR = ROOT / "candidates" / "intel-docs-reader" / "scripts"
sys.path.insert(0, str(READER_DIR))

import read_openvino_docs as reader  # noqa: E402


def make_snapshot(root: Path):
    root.mkdir(parents=True)
    (root / "index.html").write_text(
        "<html><head><title>OpenVINO Docs</title></head><body><main><h1>OpenVINO Docs</h1></main></body></html>",
        encoding="utf-8",
    )
    (root / "npu.html").write_text(
        "<html><head><title>NPU Plugin</title></head><body><main>"
        "<h1>NPU Plugin</h1><p>Configure the OpenVINO NPU device and inspect supported properties.</p>"
        "</main></body></html>",
        encoding="utf-8",
    )


def make_archive(path: Path):
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(
            "2026/index.html",
            "<html><head><title>OpenVINO Docs</title></head><body><main>OpenVINO Docs</main></body></html>",
        )
        archive.writestr(
            "2026/npu.html",
            "<html><head><title>NPU Plugin</title></head><body><main>"
            "Configure the OpenVINO NPU device."
            "</main></body></html>",
        )


class IntelDocsReaderTests(unittest.TestCase):
    def test_query_returns_local_citation_and_source_url(self):
        with tempfile.TemporaryDirectory() as directory:
            snapshot = Path(directory) / "openvino"
            make_snapshot(snapshot)
            result = reader.search_docs("NPU device", snapshot)
            self.assertEqual(result["cache_status"], "valid")
            self.assertEqual(result["matches"][0]["local_path"], "npu.html")
            self.assertIn("https://docs.openvino.ai/2026/npu.html", result["matches"][0]["source_url"])

    def test_missing_cache_is_reported_without_network_fallback(self):
        with tempfile.TemporaryDirectory() as directory:
            result = reader.search_docs("runtime", Path(directory) / "missing", allow_download=False)
            self.assertEqual(result["cache_status"], "missing")
            self.assertEqual(result["matches"], [])
            self.assertTrue(any("missing" in item.lower() for item in result["limitations"]))

    def test_archive_is_downloaded_only_when_allowed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            archive = root / "2026.zip"
            snapshot = root / "cache"
            make_archive(archive)
            result = reader.search_docs(
                "NPU device",
                snapshot,
                allow_download=True,
                archive_url=archive.as_uri(),
            )
            self.assertEqual(result["cache_status"], "valid")
            self.assertTrue(result["downloaded"])
            self.assertTrue((snapshot / "npu.html").is_file())
            self.assertTrue((snapshot / ".intel-docs-reader.json").is_file())

    def test_existing_cache_is_reused_without_downloading(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            archive = root / "2026.zip"
            snapshot = root / "cache"
            make_archive(archive)
            first = reader.search_docs("NPU", snapshot, allow_download=True, archive_url=archive.as_uri())
            second = reader.search_docs(
                "NPU",
                snapshot,
                allow_download=True,
                archive_url="file:///missing/archive.zip",
            )
            self.assertTrue(first["downloaded"])
            self.assertFalse(second["downloaded"])
            self.assertEqual(second["cache_status"], "valid")

    def test_reader_has_no_process_or_browser_dependency(self):
        source = (READER_DIR / "read_openvino_docs.py").read_text(encoding="utf-8")
        for forbidden in ("subprocess", "requests", "httpx", "webbrowser"):
            self.assertNotIn(forbidden, source)

    def test_reader_cli_uses_the_same_local_path(self):
        with tempfile.TemporaryDirectory() as directory:
            snapshot = Path(directory) / "openvino"
            make_snapshot(snapshot)
            output = StringIO()
            with redirect_stdout(output):
                code = reader.main(
                    ["--query", "NPU", "--docs-dir", str(snapshot), "--offline", "--format", "json"]
                )
            self.assertEqual(code, 0)
            self.assertEqual(json.loads(output.getvalue())["matches"][0]["local_path"], "npu.html")


if __name__ == "__main__":
    unittest.main()
