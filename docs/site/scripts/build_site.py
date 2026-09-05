"""Build and validate the dependency-free Intel AI Skills documentation site."""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[3]
WEBSITE = ROOT / "docs" / "site"
SKILLS_ROOT = ROOT / "skills"
SOURCE_ASSETS = ROOT / "assets"
OUTPUT = WEBSITE / "build" / "site"
REQUIRED_LOGOS = (
    "intel-ai-skills-logo.svg",
    "intel-ai-skills-logo-light.svg",
    "intel-ai-skills-logo-dark.svg",
    "intel-ai-skills-logo-monochrome.svg",
    "intel-ai-skills-mark.svg",
)
REQUIRED_SKILL_FIELDS = (
    "id", "slug", "name", "category", "tagline", "purpose", "when_to_use",
    "workflow", "boundaries", "install", "related",
)
SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_PATTERN = re.compile(r'''(?:href|src)="([^"#]+)"''')


class BuildError(RuntimeError):
    """Raised when authored site content cannot produce a safe artifact."""


def read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise BuildError(f"Cannot read JSON content from {path}: {exc}") from exc


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def validate_catalog(catalog: dict, site: dict) -> tuple[list[dict], dict[str, dict]]:
    entries = catalog.get("skills")
    if not isinstance(entries, list) or not entries:
        raise BuildError("docs/site/content/skills.json must contain a non-empty skills list")

    discovered = {path.name for path in SKILLS_ROOT.iterdir() if path.is_dir()}
    indexed = {entry.get("id") for entry in entries if isinstance(entry, dict)}
    missing = sorted(discovered - indexed)
    extra = sorted(indexed - discovered)
    if missing or extra:
        problems = []
        if missing:
            problems.append(f"missing catalog entries: {', '.join(missing)}")
        if extra:
            problems.append(f"catalog entries without skill directories: {', '.join(extra)}")
        raise BuildError("Skill catalog coverage mismatch; " + "; ".join(problems))

    categories = {item.get("id") for item in site.get("categories", [])}
    by_id: dict[str, dict] = {}
    slugs: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise BuildError("Every skill catalog entry must be an object")
        missing_fields = [field for field in REQUIRED_SKILL_FIELDS if not entry.get(field)]
        if missing_fields:
            raise BuildError(f"{entry.get('id', '<unknown>')} is missing: {', '.join(missing_fields)}")
        skill_id = entry["id"]
        slug = entry["slug"]
        if skill_id in by_id:
            raise BuildError(f"Duplicate skill id: {skill_id}")
        if slug in slugs or not SLUG_PATTERN.fullmatch(slug):
            raise BuildError(f"Invalid or duplicate skill slug: {slug}")
        if entry["category"] not in categories:
            raise BuildError(f"Unknown category for {skill_id}: {entry['category']}")
        if not entry["install"].startswith("npx skills add "):
            raise BuildError(f"Install command for {skill_id} must use npx skills add")
        for field in ("when_to_use", "workflow", "boundaries", "related"):
            if not isinstance(entry[field], list):
                raise BuildError(f"{skill_id}.{field} must be a list")
        by_id[skill_id] = entry
        slugs.add(slug)

    for entry in entries:
        for related in entry["related"]:
            if related not in by_id:
                raise BuildError(f"{entry['id']} references missing related skill {related}")
    return entries, by_id


def list_items(items: list[str], class_name: str) -> str:
    return "".join(f'<li class="{class_name}">{esc(item)}</li>' for item in items)


def nav_html(prefix: str, current: str) -> str:
    links = (
        ("home", "Home", f"{prefix}index.html"),
        ("getting-started", "Get started", f"{prefix}getting-started.html"),
        ("skills", "Skills", f"{prefix}skills/index.html"),
    )
    return "".join(
        f'<a href="{href}"{(" aria-current=\"page\"" if current == key else "")}>{label}</a>'
        for key, label, href in links
    )


def render_layout(template: str, *, title: str, description: str, content: str,
                  prefix: str, current: str, repo: str) -> str:
    values = {
        "TITLE": esc(title),
        "META_DESCRIPTION": esc(description),
        "CONTENT": content,
        "ASSET_PREFIX": prefix + "assets/",
        "HOME_LINK": prefix + "index.html",
        "GETTING_STARTED_LINK": prefix + "getting-started.html",
        "SKILLS_LINK": "index.html" if current == "skills" else prefix + "skills/index.html",
        "NAV": nav_html(prefix, current),
        "REPO_LINK": esc(repo),
        "BODY_CLASS": current,
    }
    output = template
    for key, value in values.items():
        output = output.replace("{{" + key + "}}", value)
    return output


def render_template(path: Path, replacements: dict[str, str]) -> str:
    output = path.read_text(encoding="utf-8")
    for key, value in replacements.items():
        output = output.replace("{{" + key + "}}", value)
    return output


def featured_cards(entries: list[dict]) -> str:
    cards = []
    for entry in entries[:3]:
        cards.append(
            f'<a class="feature-card" href="skills/{esc(entry["slug"])}.html">'
            f'<span class="card-icon" aria-hidden="true">{("◌" if entry["category"] == "discovery" else "↗" if entry["category"] == "runtime" else "✦")}</span>'
            f'<span><h3>{esc(entry["name"])}</h3><p>{esc(entry["tagline"])}</p></span>'
            '<span class="card-arrow">Explore skill ↗</span></a>'
        )
    return "".join(cards)


def category_sections(entries: list[dict], site: dict) -> str:
    by_category = {category["id"]: [] for category in site["categories"]}
    for entry in entries:
        by_category.setdefault(entry["category"], []).append(entry)
    sections = []
    for category in site["categories"]:
        cards = []
        for entry in by_category.get(category["id"], []):
            cards.append(
                f'<a class="catalog-card" href="{esc(entry["slug"])}.html">'
                f'<span class="card-icon" aria-hidden="true">{("◌" if category["id"] == "discovery" else "↗" if category["id"] == "runtime" else "✦")}</span>'
                f'<h3>{esc(entry["name"])}</h3><p>{esc(entry["tagline"])}</p>'
                '<span class="card-arrow">Read details ↗</span></a>'
            )
        sections.append(
            f'<section class="catalog-group"><div class="catalog-group-heading"><h2>{esc(category["label"])}</h2><p>{esc(category["description"])}</p></div><div class="catalog-cards">{"".join(cards)}</div></section>'
        )
    return "".join(sections)


def related_links(entry: dict, by_id: dict[str, dict]) -> str:
    return "".join(
        f'<a href="{esc(by_id[related]["slug"])}.html">{esc(by_id[related]["name"])} <span>↗</span></a>'
        for related in entry["related"]
    )


def copy_static_assets() -> None:
    static_root = WEBSITE / "static"
    output_assets = OUTPUT / "assets"
    for source in static_root.rglob("*"):
        if not source.is_file() or source.suffix.lower() == ".md":
            continue
        destination = output_assets / source.relative_to(static_root)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    for filename in REQUIRED_LOGOS:
        source = SOURCE_ASSETS / filename
        if not source.is_file():
            raise BuildError(f"Required logo asset is missing: {source}")
        shutil.copy2(source, output_assets / filename)


def validate_output_links() -> None:
    problems: list[str] = []
    for page in OUTPUT.rglob("*.html"):
        for target in LINK_PATTERN.findall(page.read_text(encoding="utf-8")):
            parsed = urlparse(target)
            if parsed.scheme or target.startswith(("//", "#")):
                continue
            resolved = (page.parent / target).resolve()
            if not resolved.is_file():
                problems.append(f"{page.relative_to(OUTPUT)} -> {target}")
    if problems:
        raise BuildError("Broken generated links:\n  " + "\n  ".join(problems))


def build() -> Path:
    site = read_json(WEBSITE / "content" / "site.json")
    catalog = read_json(WEBSITE / "content" / "skills.json")
    entries, by_id = validate_catalog(catalog, site)
    template_root = WEBSITE / "templates"
    layout = (template_root / "layout.html").read_text(encoding="utf-8")

    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    OUTPUT.mkdir(parents=True)
    copy_static_assets()

    def write_page(relative: str, content_template: str, *, title: str, description: str,
                   prefix: str, current: str, replacements: dict[str, str]) -> None:
        replacements = dict(replacements)
        replacements.setdefault("HOME_LINK", prefix + "index.html")
        replacements.setdefault("GETTING_STARTED_LINK", prefix + "getting-started.html")
        replacements.setdefault("SKILLS_LINK", "index.html" if current == "skills" else prefix + "skills/index.html")
        content = render_template(template_root / content_template, replacements)
        page = render_layout(layout, title=title, description=description, content=content,
                             prefix=prefix, current=current, repo=site["repo"])
        destination = OUTPUT / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(page, encoding="utf-8")

    common = {
        "INSTALL_ONE": esc(site["install_one"]),
        "INSTALL_MULTIPLE": esc(site["install_multiple"]),
        "SKILL_COUNT": str(len(entries)),
        "FEATURED_CARDS": featured_cards(entries),
        "CATEGORY_SECTIONS": category_sections(entries, site),
    }
    write_page("index.html", "index.html", title=site["name"], description=site["description"],
               prefix="", current="home", replacements=common)
    write_page("getting-started.html", "getting-started.html", title="Get started",
               description="Install and use portable Intel AI Skills with your agent.",
               prefix="", current="getting-started", replacements=common)
    write_page("skills/index.html", "skills-index.html", title="Skill catalog",
               description="Explore the published Intel AI Skills catalog.", prefix="../",
               current="skills", replacements=common)
    for entry in entries:
        replacements = {
            "CATEGORY_LABEL": next(item["label"] for item in site["categories"] if item["id"] == entry["category"]),
            "SKILL_NAME": esc(entry["name"]),
            "TAGLINE": esc(entry["tagline"]),
            "INSTALL": esc(entry["install"]),
            "PURPOSE": esc(entry["purpose"]),
            "WHEN_TO_USE": list_items(entry["when_to_use"], ""),
            "WORKFLOW": list_items(entry["workflow"], ""),
            "BOUNDARIES": list_items(entry["boundaries"], ""),
            "RELATED": related_links(entry, by_id),
        }
        write_page(f"skills/{entry['slug']}.html", "skill-detail.html", title=entry["name"],
                   description=entry["purpose"], prefix="../", current="skills",
                   replacements=replacements)
    write_page("404.html", "404.html", title="Page not found",
               description="The requested Intel AI Skills page was not found.", prefix="",
               current="home", replacements={})
    validate_output_links()
    return OUTPUT


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quiet", action="store_true", help="Only report failures")
    args = parser.parse_args()
    try:
        output = build()
    except BuildError as exc:
        print(f"Site build failed: {exc}", file=sys.stderr)
        return 1
    if not args.quiet:
        pages = len(list(output.rglob("*.html")))
        print(f"Built {pages} HTML pages at {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
