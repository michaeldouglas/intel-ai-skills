import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import openvino_docs_sync as sync  # noqa: E402


class OpenVinoDocsSyncTests(unittest.TestCase):
    def test_update_command_is_explicit_and_shell_free(self):
        command = sync.build_extract_command(
            "node",
            Path("extract.mjs"),
            "https://docs.openvino.ai/2026/index.html",
            Path("docs/openvino"),
        )
        self.assertEqual(command[0], "node")
        self.assertEqual(command[1], "extract.mjs")
        self.assertNotIn("&&", command)
        self.assertNotIn("|", command)

    def test_no_update_argument_is_a_no_op_and_does_not_run_process(self):
        with patch.object(sync, "run_process") as runner:
            result = sync.main([])
        runner.assert_not_called()
        self.assertEqual(result, 0)

    def test_unrecognized_non_empty_cache_is_protected(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            (target / "human.md").write_text("do not overwrite", encoding="utf-8")
            self.assertFalse(sync.is_generated_cache(target))
            with self.assertRaises(sync.CacheProtectionError):
                sync.ensure_output_directory(target)

    def test_generated_cache_is_recognized_by_manifest(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            (target / "index.md").write_text("# OpenVINO", encoding="utf-8")
            (target / "manifest.json").write_text(json.dumps({"coverage": {"discovered": 1, "extracted": 1}}), encoding="utf-8")
            self.assertTrue(sync.is_generated_cache(target))
            sync.ensure_output_directory(target)

    def test_verify_only_never_runs_extractor(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            (target / "index.md").write_text("# OpenVINO", encoding="utf-8")
            (target / "manifest.json").write_text(json.dumps({"coverage": {"discovered": 1, "extracted": 1}}), encoding="utf-8")
            with patch.object(sync, "run_process", return_value=sync.ProcessResult(0, "")) as runner:
                result = sync.execute_update(output_dir=target, verify_only=True, node="node")
            self.assertEqual(result.status, "verified")
            self.assertEqual(runner.call_count, 1)
            self.assertIn("verify.mjs", " ".join(runner.call_args.args[0]))

    def test_verify_only_does_not_create_a_missing_cache(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "missing"
            with patch.object(sync, "run_process") as runner:
                result = sync.execute_update(output_dir=target, verify_only=True, node="node")
            self.assertEqual(result.status, "incomplete")
            runner.assert_not_called()
            self.assertFalse(target.exists())

    def test_snapshot_marker_contains_manifest_hash(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "cache"
            destination = root / "snapshot"
            source.mkdir()
            (source / "index.md").write_text("# OpenVINO", encoding="utf-8")
            (source / "manifest.json").write_text(json.dumps({"coverage": {"discovered": 1, "extracted": 1}}), encoding="utf-8")
            sync.publish_snapshot(source, destination, source_url="https://docs.openvino.ai/2026/index.html")
            marker = json.loads((destination / ".openvino-snapshot.json").read_text(encoding="utf-8"))
            self.assertEqual(marker["schema_version"], "1")
            self.assertTrue(marker["manifest_sha256"])

    def test_sync_child_environment_excludes_unrelated_secrets(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            dependencies = root / "deps"
            (dependencies / "node_modules").mkdir(parents=True)
            calls = []

            def fake_runner(command, **kwargs):
                calls.append(kwargs)
                return sync.ProcessResult(0, "")

            with patch.dict(os.environ, {"OPENAI_API_KEY": "must-not-leak"}, clear=False):
                result = sync.execute_update(
                    output_dir=root / "cache",
                    deps_dir=dependencies,
                    skip_install=True,
                    runner=fake_runner,
                )
            self.assertEqual(result.status, "updated")
            self.assertNotIn("OPENAI_API_KEY", calls[0]["env"])

    def test_sync_rejects_a_source_outside_openvino_scope(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(sync, "run_process") as runner:
                result = sync.execute_update(output_dir=Path(directory) / "cache", start_url="https://example.com/docs")
            self.assertEqual(result.status, "blocked")
            runner.assert_not_called()


if __name__ == "__main__":
    unittest.main()
