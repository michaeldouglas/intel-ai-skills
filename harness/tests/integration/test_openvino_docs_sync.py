import json
import shutil
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[2]
SCRIPT = ROOT / "scripts" / "openvino_docs_sync.py"
FIXTURE = ROOT / "tests" / "fixtures" / "openvino-docs"


class OpenVinoDocsSnapshotTests(unittest.TestCase):
    def test_fixture_snapshot_has_required_metadata_and_no_internal_paths(self):
        manifest = json.loads((FIXTURE / "manifest.json").read_text(encoding="utf-8"))
        self.assertIn("coverage", manifest)
        self.assertIn("source_url", manifest)
        self.assertIn("extracted_at", manifest)
        content = "\n".join(path.read_text(encoding="utf-8") for path in FIXTURE.rglob("*.md"))
        self.assertNotIn("harness/", content)
        self.assertNotIn("C:\\Users\\", content)

    def test_clean_copy_contains_reader_and_snapshot_without_harness_reference(self):
        with tempfile.TemporaryDirectory() as directory:
            clean = Path(directory) / "reader"
            shutil.copytree(ROOT / "candidates" / "openvino-docs-reader", clean)
            shutil.copy2(FIXTURE / "manifest.json", clean / "references" / "openvino" / "manifest.json")
            shutil.copy2(FIXTURE / "index.md", clean / "references" / "openvino" / "index.md")
            shutil.copy2(FIXTURE / "npu.md", clean / "references" / "openvino" / "npu.md")
            candidate_text = "\n".join(path.read_text(encoding="utf-8") for path in clean.rglob("*.py"))
            self.assertNotIn("harness", candidate_text)
            self.assertTrue((clean / "scripts" / "read_openvino_docs.py").exists())


if __name__ == "__main__":
    unittest.main()
