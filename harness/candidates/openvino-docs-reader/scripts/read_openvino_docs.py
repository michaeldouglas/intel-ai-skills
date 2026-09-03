"""Local-only OpenVINO Markdown reader.

This script deliberately has no network, browser, process-runner, or
synchronizer dependency. It can be copied with the candidate skill and used
offline.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


SNAPSHOT_DIR = Path(__file__).resolve().parents[1] / "references" / "openvino"
WORD_RE = re.compile(r"[a-z0-9][a-z0-9_+-]*", re.IGNORECASE)


def _load_json(path: Path) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def _frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    fields: dict[str, str] = {}
    for line in text.splitlines()[1:]:
        if line.strip() == "---":
            break
        match = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if match:
            fields[match.group(1)] = match.group(2).strip().strip('"').strip("'")
    return fields


def _coverage_limitations(manifest: dict[str, Any]) -> list[str]:
    limitations: list[str] = []
    coverage = manifest.get("coverage", {})
    if not isinstance(coverage, dict):
        return ["Coverage metadata is invalid; do not treat this snapshot as complete."]
    discovered = coverage.get("discovered")
    extracted = coverage.get("extracted")
    if isinstance(discovered, int) and isinstance(extracted, int) and extracted < discovered:
        limitations.append(f"Only {extracted} of {discovered} discovered routes were extracted.")
    skipped = coverage.get("skipped", [])
    if skipped:
        count = len(skipped) if isinstance(skipped, list) else "some"
        limitations.append(f"The extractor recorded {count} skipped route(s).")
    if manifest.get("verification") not in (None, "passed", True):
        limitations.append("The extraction verification result is not recorded as passed.")
    return limitations


def inspect_cache(snapshot: Path) -> tuple[str, dict[str, Any] | None, list[str]]:
    if not snapshot.is_dir():
        return "missing", None, ["The local OpenVINO documentation is missing; request an explicit documentation update."]
    manifest = _load_json(snapshot / "manifest.json")
    index = snapshot / "index.md"
    if manifest is None or not index.is_file():
        return "invalid", manifest, ["The local documentation index or manifest is invalid; request a fresh update."]
    limitations = _coverage_limitations(manifest)
    return ("incomplete" if limitations else "valid"), manifest, limitations


def _excerpt(text: str, tokens: list[str]) -> str:
    body = text.split("---", 2)[-1].strip()
    lowered = body.lower()
    positions = [lowered.find(token) for token in tokens if lowered.find(token) >= 0]
    start = max(0, (min(positions) if positions else 0) - 80)
    excerpt = re.sub(r"\s+", " ", body[start : start + 320]).strip()
    return excerpt + ("…" if start + 320 < len(body) else "")


def search_docs(query: str, snapshot: Path = SNAPSHOT_DIR, *, limit: int = 5) -> dict[str, Any]:
    status, manifest, limitations = inspect_cache(snapshot)
    result: dict[str, Any] = {"cache_status": status, "query": query, "matches": [], "limitations": limitations}
    if status in {"missing", "invalid"}:
        return result
    tokens = [token.lower() for token in WORD_RE.findall(query) if len(token) > 1]
    if not tokens:
        result["limitations"].append("The query did not contain searchable terms.")
        return result
    candidates = []
    for path in snapshot.rglob("*.md"):
        if path.name.lower() == "index.md" or any(part.startswith(".") for part in path.relative_to(snapshot).parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        fields = _frontmatter(text)
        searchable = text.lower()
        score = sum(searchable.count(token) for token in tokens)
        title = fields.get("title", path.stem.replace("-", " ").title())
        score += sum(3 for token in tokens if token in title.lower())
        if score:
            candidates.append((score, path, fields, text))
    candidates.sort(key=lambda item: (-item[0], str(item[1])))
    for score, path, fields, text in candidates[:limit]:
        result["matches"].append(
            {
                "title": fields.get("title", path.stem),
                "local_path": path.relative_to(snapshot).as_posix(),
                "source_url": fields.get("source_url") or (manifest or {}).get("source_url"),
                "extracted_at": fields.get("extracted_at") or (manifest or {}).get("extracted_at"),
                "score": score,
                "excerpt": _excerpt(text, tokens),
            }
        )
    if not result["matches"]:
        result["limitations"].append("No matching local page was found; uncaptured web pages were not consulted.")
    return result


def render_text(result: dict[str, Any]) -> str:
    lines = [f"OpenVINO docs cache: {result['cache_status']}", f"Query: {result['query']}"]
    if result["limitations"]:
        lines.append("Limitations:")
        lines.extend(f"- {item}" for item in result["limitations"])
    lines.append("Matches:")
    if not result["matches"]:
        lines.append("- No local matches.")
    for match in result["matches"]:
        lines.extend(
            [
                f"- {match['title']} [{match['local_path']}]",
                f"  Source: {match.get('source_url') or 'not recorded'}",
                f"  {match['excerpt']}",
            ]
        )
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Search the local OpenVINO documentation snapshot")
    parser.add_argument("--query", required=True)
    parser.add_argument("--docs-dir", type=Path, default=SNAPSHOT_DIR)
    parser.add_argument("--format", choices=("json", "text"), default="text")
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args(argv)
    result = search_docs(args.query, args.docs_dir, limit=max(1, min(args.limit, 20)))
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(render_text(result), end="")
    return 0 if result["cache_status"] == "valid" else 2


if __name__ == "__main__":
    raise SystemExit(main())
