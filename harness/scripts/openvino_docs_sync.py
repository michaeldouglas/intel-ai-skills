"""Explicit OpenVINO documentation cache synchronization.

This module is intentionally not imported by the local documentation reader.
The only network-capable path is the command line action that includes
``--update``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Mapping, Sequence
from urllib.parse import urlparse


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_START_URL = "https://docs.openvino.ai/2026/index.html"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "docs" / "openvino"
DEFAULT_SNAPSHOT_DIR = REPO_ROOT / "candidates" / "openvino-docs-reader" / "references" / "openvino"
EXTRACTOR_DIR = REPO_ROOT / ".agents" / "skills" / "extract-spa-docs" / "scripts"
EXTRACTOR = EXTRACTOR_DIR / "extract.mjs"
VERIFIER = EXTRACTOR_DIR / "verify.mjs"
DEFAULT_DEPS_DIR = Path(tempfile.gettempdir()) / "intel-ai-skills-spa-docs"


class CacheProtectionError(RuntimeError):
    """Raised when a target contains content not identified as generated."""


@dataclass(frozen=True)
class ProcessResult:
    returncode: int
    message: str


@dataclass(frozen=True)
class SyncResult:
    status: str
    message: str
    output_dir: Path
    snapshot_dir: Path | None = None


Runner = Callable[..., ProcessResult]


def build_extract_command(node: str, extractor: Path, start_url: str, output_dir: Path) -> list[str]:
    """Build an argument-array command; runtime options are supplied via env."""
    return [node, str(extractor)]


def build_verify_command(node: str, verifier: Path, output_dir: Path) -> list[str]:
    return [node, str(verifier), str(output_dir)]


def run_process(command: Sequence[str], *, cwd: Path | None = None, env: Mapping[str, str] | None = None) -> ProcessResult:
    """Run a process without a shell and return only safe status metadata."""
    try:
        completed = subprocess.run(
            list(command),
            cwd=str(cwd) if cwd else None,
            env=dict(env) if env else None,
            shell=False,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return ProcessResult(127, "required tool is unavailable")
    except PermissionError:
        return ProcessResult(126, "required tool permission denied")
    except OSError:
        return ProcessResult(125, "required process could not be started")
    # Do not return stdout/stderr: extractor output can contain arbitrary page text.
    return ProcessResult(completed.returncode, "process completed")


def _read_manifest(directory: Path) -> dict:
    try:
        value = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def is_generated_cache(directory: Path) -> bool:
    """Recognize only extractor-shaped output, protecting unknown content."""
    if not directory.is_dir() or not (directory / "index.md").is_file():
        return False
    manifest = _read_manifest(directory)
    coverage = manifest.get("coverage")
    return isinstance(coverage, dict) and any(key in coverage for key in ("discovered", "extracted", "pages"))


def ensure_output_directory(directory: Path) -> None:
    if directory.exists():
        files = list(directory.iterdir()) if directory.is_dir() else [directory]
        if files and not is_generated_cache(directory):
            raise CacheProtectionError("output directory contains unrecognized content")
    directory.mkdir(parents=True, exist_ok=True)


def _environment(
    start_url: str,
    output_dir: Path,
    deps_dir: Path,
    *,
    page_limit: int | None,
    request_delay: int,
    force: bool,
) -> dict[str, str]:
    values = {
        "START_URL": start_url,
        "OUT_DIR": str(output_dir.resolve()),
        "DEPS_DIR": str(deps_dir.resolve()),
        "SITEMAP": "1",
        "RECURSE": "1",
        "REQUEST_DELAY": str(request_delay),
    }
    if page_limit is not None:
        values["PAGE_LIMIT"] = str(page_limit)
    if force:
        values["FORCE"] = "1"
    return values


def is_allowed_source_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme == "https" and parsed.netloc == "docs.openvino.ai" and parsed.path.startswith("/2026/")


def _safe_environment(values: Mapping[str, str]) -> dict[str, str]:
    """Keep credentials and unrelated user environment variables out of child processes."""
    safe = {key: os.environ[key] for key in ("PATH", "Path", "SystemRoot", "TEMP", "TMP", "TMPDIR") if key in os.environ}
    safe.update(values)
    return safe


def _manifest_hash(directory: Path) -> str:
    return hashlib.sha256((directory / "manifest.json").read_bytes()).hexdigest()


def publish_snapshot(source: Path, destination: Path, *, source_url: str = DEFAULT_START_URL) -> None:
    """Copy only a verified generated cache into a tagged candidate snapshot."""
    if not is_generated_cache(source):
        raise ValueError("cannot publish an unverified documentation cache")
    if destination.exists():
        marker = destination / ".openvino-snapshot.json"
        if not marker.is_file():
            raise CacheProtectionError("snapshot destination is not a generated snapshot")
    destination.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix="openvino-snapshot-", dir=str(destination.parent)))
    try:
        shutil.copytree(source, staging / destination.name)
        snapshot = staging / destination.name
        marker = {
            "schema_version": "1",
            "source_url": source_url,
            "cache_source": "docs/openvino",
            "copied_at": datetime.now(timezone.utc).date().isoformat(),
            "manifest_sha256": _manifest_hash(source),
        }
        (snapshot / ".openvino-snapshot.json").write_text(json.dumps(marker, indent=2) + "\n", encoding="utf-8")
        if destination.exists():
            shutil.rmtree(destination)
        shutil.move(str(snapshot), str(destination))
    finally:
        if staging.exists():
            shutil.rmtree(staging)


def execute_update(
    *,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    start_url: str = DEFAULT_START_URL,
    node: str = "node",
    deps_dir: Path = DEFAULT_DEPS_DIR,
    page_limit: int | None = None,
    request_delay: int = 300,
    force: bool = False,
    skip_install: bool = False,
    verify_only: bool = False,
    publish: bool = False,
    snapshot_dir: Path = DEFAULT_SNAPSHOT_DIR,
    runner: Runner | None = None,
) -> SyncResult:
    runner = runner or run_process
    output_dir = output_dir.resolve()
    if not is_allowed_source_url(start_url):
        return SyncResult("blocked", "source URL is outside the approved OpenVINO documentation scope", output_dir)
    if verify_only and not is_generated_cache(output_dir):
        return SyncResult("incomplete", "no generated documentation cache is available to verify", output_dir)
    try:
        ensure_output_directory(output_dir)
    except CacheProtectionError as exc:
        return SyncResult("blocked", str(exc), output_dir)

    if not EXTRACTOR.is_file() or not VERIFIER.is_file():
        return SyncResult("blocked", "extract-spa-docs scripts are unavailable", output_dir)

    if verify_only:
        result = runner(build_verify_command(node, VERIFIER, output_dir), cwd=deps_dir)
        return SyncResult("verified" if result.returncode == 0 else "incomplete", "verification completed" if result.returncode == 0 else "verification failed", output_dir)

    deps_dir.mkdir(parents=True, exist_ok=True)
    if not (deps_dir / "node_modules").is_dir():
        if skip_install:
            return SyncResult("blocked", "extractor dependencies are not installed", output_dir)
        install = runner(
            ["npm", "install", "--no-save", "--no-package-lock", "playwright-core", "turndown", "turndown-plugin-gfm"],
            cwd=deps_dir,
            env=_safe_environment({}),
        )
        if install.returncode != 0:
            return SyncResult("blocked", "extractor dependencies could not be installed", output_dir)

    env = _safe_environment(_environment(start_url, output_dir, deps_dir, page_limit=page_limit, request_delay=request_delay, force=force))
    extracted = runner(build_extract_command(node, EXTRACTOR, start_url, output_dir), cwd=deps_dir, env=env)
    if extracted.returncode != 0:
        return SyncResult("blocked", "rendered extraction failed; connect a real browser and retry", output_dir)

    verified = runner(build_verify_command(node, VERIFIER, output_dir), cwd=deps_dir, env=env)
    if verified.returncode != 0:
        return SyncResult("incomplete", "extraction completed but verification did not pass", output_dir)

    published = None
    if publish:
        try:
            publish_snapshot(output_dir, snapshot_dir, source_url=start_url)
            published = snapshot_dir
        except (CacheProtectionError, OSError, ValueError):
            return SyncResult("incomplete", "cache verified but candidate snapshot was not published", output_dir)
    return SyncResult("updated", "documentation cache updated and verified", output_dir, published)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Explicitly update the local OpenVINO documentation cache")
    parser.add_argument("--update", action="store_true", help="authorize the network-capable extraction")
    parser.add_argument("--verify-only", action="store_true", help="verify an existing generated cache without downloading")
    parser.add_argument("--start-url", default=DEFAULT_START_URL)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--snapshot-dir", type=Path, default=DEFAULT_SNAPSHOT_DIR)
    parser.add_argument("--deps-dir", type=Path, default=DEFAULT_DEPS_DIR)
    parser.add_argument("--page-limit", type=int)
    parser.add_argument("--request-delay", type=int, default=300)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--skip-install", action="store_true")
    parser.add_argument("--publish-snapshot", action="store_true")
    args = parser.parse_args(argv)

    if not args.update and not args.verify_only:
        print("No documentation update requested. Use --update explicitly.")
        return 0
    result = execute_update(
        output_dir=args.output_dir,
        start_url=args.start_url,
        deps_dir=args.deps_dir,
        page_limit=args.page_limit,
        request_delay=args.request_delay,
        force=args.force,
        skip_install=args.skip_install,
        verify_only=args.verify_only,
        publish=args.publish_snapshot,
        snapshot_dir=args.snapshot_dir,
    )
    print(f"{result.status}: {result.message}")
    return {"updated": 0, "verified": 0, "blocked": 2, "incomplete": 3}.get(result.status, 1)


if __name__ == "__main__":
    raise SystemExit(main())
