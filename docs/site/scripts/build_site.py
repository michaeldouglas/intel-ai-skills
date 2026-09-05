"""Build and validate the dependency-free multilingual Intel AI Skills site."""

from __future__ import annotations

import argparse
import html
import json
import posixpath
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
REQUIRED_UI_KEYS = {
    "UI_SKIP", "UI_MENU", "UI_THEME", "UI_LANGUAGE_LABEL", "UI_HOME_LABEL",
    "UI_PRIMARY_NAV", "UI_NAV_HOME", "UI_NAV_GETTING_STARTED", "UI_NAV_SKILLS",
    "UI_DOCS_NAV", "UI_ON_THIS_PAGE", "UI_BREADCRUMB_HOME", "UI_BREADCRUMB_GETTING",
    "UI_BREADCRUMB_SKILLS", "UI_SIDEBAR_CATALOG", "UI_PREVIOUS_SKILL", "UI_NEXT_SKILL",
    "UI_FOOTER_TAGLINE", "UI_REPO_LINK", "UI_GET_STARTED_LINK",
    "UI_HOME_EYEBROW", "UI_HOME_TITLE", "UI_HOME_LEDE", "UI_START_BUTTON",
    "UI_CATALOG_BUTTON", "UI_FACTS", "UI_SKILLS", "UI_OPENVINO",
    "UI_PROJECT_HIGHLIGHTS", "UI_PUBLISHED_SKILLS", "UI_FOCUS_AREAS",
    "UI_INTERNAL_DEPENDENCIES", "UI_SECTION_EYEBROW", "UI_SECTION_TITLE",
    "UI_VIEW_ALL", "UI_CALLOUT_EYEBROW", "UI_CALLOUT_TITLE", "UI_CALLOUT_TEXT",
    "UI_GETTING_EYEBROW", "UI_GETTING_TITLE", "UI_GETTING_LEDE",
    "UI_INSTALL_ONE_KICKER", "UI_INSTALL_ONE_TITLE", "UI_INSTALL_ONE_TEXT",
    "UI_INSTALL_PAIR_KICKER", "UI_INSTALL_PAIR_TITLE", "UI_INSTALL_PAIR_TEXT",
    "UI_COPY", "UI_COPY_INSTALL", "UI_HOW_EYEBROW", "UI_HOW_TITLE",
    "UI_STEP_ONE_TITLE", "UI_STEP_ONE_TEXT", "UI_STEP_TWO_TITLE", "UI_STEP_TWO_TEXT",
    "UI_STEP_THREE_TITLE", "UI_STEP_THREE_TEXT", "UI_BOUNDARY_EYEBROW",
    "UI_BOUNDARY_TITLE", "UI_BOUNDARY_TEXT", "UI_PREVIEW_EYEBROW",
    "UI_PREVIEW_TITLE", "UI_PREVIEW_TEXT", "UI_PREVIEW_FOOTER",
    "UI_AGENTS_EYEBROW", "UI_AGENTS_TITLE", "UI_AGENTS_TEXT", "UI_INSTALL_NOTE",
    "UI_CATALOG_EYEBROW", "UI_CATALOG_TITLE", "UI_CATALOG_LEDE",
    "UI_SKILLS_IN_COLLECTION", "UI_CATALOG_INTRO", "UI_CARD_EXPLORE",
    "UI_CARD_READ_DETAILS", "UI_BACK_TO_CATALOG", "UI_WHAT_IT_IS",
    "UI_SKILL_H2_SUFFIX", "UI_USE_IT_WHEN", "UI_WORKFLOW", "UI_BOUNDARY",
    "UI_RELATED_SKILLS", "UI_RELATED_LABEL", "UI_ASIDE_NOTE", "UI_INSTALL_LABEL",
    "UI_NOT_FOUND_EYEBROW", "UI_NOT_FOUND_TITLE", "UI_NOT_FOUND_LEDE",
    "UI_RETURN_HOME", "UI_BROWSE_SKILLS",
}
SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_PATTERN = re.compile(r'''(?:href|src)="([^"#]+)"''')


class BuildError(RuntimeError):
    """Raised when authored site content cannot produce a safe artifact."""


ENGLISH_UI = {
    "UI_SKIP": "Skip to content", "UI_MENU": "Menu", "UI_THEME": "Toggle theme",
    "UI_LANGUAGE_LABEL": "Language", "UI_HOME_LABEL": "Intel AI Skills home",
    "UI_PRIMARY_NAV": "Primary navigation", "UI_NAV_HOME": "Home",
    "UI_NAV_GETTING_STARTED": "Get started", "UI_NAV_SKILLS": "Skills",
    "UI_DOCS_NAV": "Documentation navigation", "UI_ON_THIS_PAGE": "On this page",
    "UI_BREADCRUMB_HOME": "Home", "UI_BREADCRUMB_GETTING": "Get started",
    "UI_BREADCRUMB_SKILLS": "Skills", "UI_SIDEBAR_CATALOG": "Skill catalog",
    "UI_PREVIOUS_SKILL": "Previous skill", "UI_NEXT_SKILL": "Next skill",
    "UI_FOOTER_TAGLINE": "Evidence-first skills for practical Intel AI and OpenVINO work.",
    "UI_REPO_LINK": "GitHub repository", "UI_GET_STARTED_LINK": "Get started",
    "UI_HOME_EYEBROW": "OpenVINO, made actionable",
    "UI_HOME_TITLE": "Portable skills<br><em>for real inference work.</em>",
    "UI_HOME_LEDE": "Intel AI Skills gives agents a grounded way to inspect hardware, install OpenVINO, prepare models, run workloads, and measure what happened.",
    "UI_START_BUTTON": "Start here", "UI_CATALOG_BUTTON": "Explore skills",
    "UI_FACTS": "FACTS", "UI_SKILLS": "SKILLS", "UI_OPENVINO": "OPENVINO",
    "UI_PROJECT_HIGHLIGHTS": "Project highlights", "UI_PUBLISHED_SKILLS": "published skills",
    "UI_FOCUS_AREAS": "focus areas", "UI_INTERNAL_DEPENDENCIES": "internal dependencies",
    "UI_SECTION_EYEBROW": "The collection",
    "UI_SECTION_TITLE": "Start with the question<br><em>you need answered.</em>",
    "UI_VIEW_ALL": "View all skills", "UI_CALLOUT_EYEBROW": "A clear boundary",
    "UI_CALLOUT_TITLE": "Public skills stay portable.",
    "UI_CALLOUT_TEXT": "Each published skill is self-contained after installation. Add the capability you need to the agent you already use, then combine skills when a task crosses boundaries.",
    "UI_GETTING_EYEBROW": "Install once, ask naturally",
    "UI_GETTING_TITLE": "Give your agent<br><em>the right starting point.</em>",
    "UI_GETTING_LEDE": "Install one skill for a focused workflow or combine several when a task crosses hardware, runtime, and model boundaries.",
    "UI_INSTALL_ONE_KICKER": "One skill", "UI_INSTALL_ONE_TITLE": "Inspect the machine first",
    "UI_INSTALL_ONE_TEXT": "A read-only starting point for understanding the Intel devices and runtime signals available on the current system.",
    "UI_INSTALL_PAIR_KICKER": "A useful pair", "UI_INSTALL_PAIR_TITLE": "Hardware plus runtime",
    "UI_INSTALL_PAIR_TEXT": "Install the advisor and installer together when you want an evidence-based path from device discovery to an OpenVINO setup.",
    "UI_COPY": "Copy", "UI_COPY_INSTALL": "Copy install command",
    "UI_HOW_EYEBROW": "How it works",
    "UI_HOW_TITLE": "A skill is an instruction layer,<br><em>not a hidden dependency.</em>",
    "UI_STEP_ONE_TITLE": "Install the capability", "UI_STEP_ONE_TEXT": "Use the skills CLI to add the published skill to the agent you use.",
    "UI_STEP_TWO_TITLE": "Ask in plain language", "UI_STEP_TWO_TEXT": "Describe the outcome you need. The skill selects its bundled scripts and workflow when they are relevant.",
    "UI_STEP_THREE_TITLE": "Review the evidence", "UI_STEP_THREE_TEXT": "Results keep facts, assumptions, prerequisites, and boundaries visible so you can choose the next action.",
    "UI_BOUNDARY_EYEBROW": "Portable by design", "UI_BOUNDARY_TITLE": "Use the skill, not the repository.",
    "UI_BOUNDARY_TEXT": "The published skill contains the instructions and bundled resources it needs. You do not need to clone this project, open a scripts folder, or know how the project is tested.",
    "UI_PREVIEW_EYEBROW": "For maintainers", "UI_PREVIEW_TITLE": "Preview the same site locally.",
    "UI_PREVIEW_TEXT": "Build and serve the generated documentation with Python from the repository root:",
    "UI_PREVIEW_FOOTER": "The local preview includes the English, Portuguese, and Spanish routes generated for GitHub Pages.",
    "UI_AGENTS_EYEBROW": "Choose your agent", "UI_AGENTS_TITLE": "Codex is an example, not a limitation.",
    "UI_AGENTS_TEXT": "The commands on this site show `-a codex` because Codex is one supported target. The skill itself is agent-agnostic: install it for Claude or another compatible agent through the skills CLI, then ask that agent for the task in natural language.",
    "UI_INSTALL_NOTE": "This example targets Codex. The skill is portable: choose Claude or another compatible agent as your installation target.",
    "UI_CATALOG_EYEBROW": "Skill catalog", "UI_CATALOG_TITLE": "Choose the skill for your task.",
    "UI_CATALOG_LEDE": "Browse the published skills below. Open a card to see what the skill handles, when to ask for it, what it does automatically, and where its responsibility stops.",
    "UI_SKILLS_IN_COLLECTION": "skills in the collection",
    "UI_CATALOG_INTRO": "Select a card to open the complete guide for that skill. The groups are only a starting point; you can install any combination that matches your workflow.",
    "UI_CARD_EXPLORE": "Explore skill", "UI_CARD_READ_DETAILS": "Read details",
    "UI_BACK_TO_CATALOG": "Back to catalog", "UI_WHAT_IT_IS": "What this skill does",
    "UI_SKILL_H2_SUFFIX": "in practice", "UI_USE_IT_WHEN": "Ask for it when",
    "UI_WORKFLOW": "What happens automatically", "UI_BOUNDARY": "What it does not do",
    "UI_RELATED_SKILLS": "Related skills", "UI_RELATED_LABEL": "Related skills",
    "UI_ASIDE_NOTE": "Skills are modular by design. Add only the capability that matches the question, then compose more when the workflow grows.",
    "UI_INSTALL_LABEL": "Install", "UI_NOT_FOUND_EYEBROW": "404",
    "UI_NOT_FOUND_TITLE": "This page is not in the catalog.",
    "UI_NOT_FOUND_LEDE": "The route may have changed, or the skill you want may be one step away.",
    "UI_RETURN_HOME": "Return home", "UI_BROWSE_SKILLS": "Browse skills",
}


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
    missing, extra = sorted(discovered - indexed), sorted(indexed - discovered)
    if missing or extra:
        problems = []
        if missing:
            problems.append(f"missing catalog entries: {', '.join(missing)}")
        if extra:
            problems.append(f"catalog entries without skill directories: {', '.join(extra)}")
        raise BuildError("Skill catalog coverage mismatch; " + "; ".join(problems))
    categories = {item.get("id") for item in site.get("categories", [])}
    by_id, slugs = {}, set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise BuildError("Every skill catalog entry must be an object")
        missing_fields = [field for field in REQUIRED_SKILL_FIELDS if not entry.get(field)]
        if missing_fields:
            raise BuildError(f"{entry.get('id', '<unknown>')} is missing: {', '.join(missing_fields)}")
        skill_id, slug = entry["id"], entry["slug"]
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
        by_id[skill_id], slugs = entry, slugs | {slug}
    for entry in entries:
        for related in entry["related"]:
            if related not in by_id:
                raise BuildError(f"{entry['id']} references missing related skill {related}")
    return entries, by_id


def localized_catalog(site: dict, entries: list[dict], locales: dict) -> list[dict]:
    if not isinstance(locales, dict) or not isinstance(locales.get("locales"), dict):
        raise BuildError("docs/site/content/locales.json must contain a locales object")
    result = [{
        "id": "en", "lang": "en", "label": "EN", "path": "", "ui": ENGLISH_UI,
        "site": dict(site), "categories": site["categories"],
        "skills": {entry["id"]: entry for entry in entries},
    }]
    for route, definition in locales["locales"].items():
        if route == "en":
            continue
        if not isinstance(definition, dict):
            raise BuildError(f"Locale {route} must be an object")
        ui = definition.get("ui")
        missing_ui = sorted(REQUIRED_UI_KEYS - set(ui or {}))
        if not isinstance(ui, dict) or missing_ui:
            raise BuildError(f"Locale {route} is missing UI keys: {', '.join(missing_ui)}")
        categories = definition.get("categories")
        if not isinstance(categories, dict):
            raise BuildError(f"Locale {route} must define category translations")
        translated_categories = []
        for category in site["categories"]:
            translated = categories.get(category["id"])
            if not isinstance(translated, dict) or not translated.get("label") or not translated.get("description"):
                raise BuildError(f"Locale {route} is missing category {category['id']}")
            translated_categories.append({"id": category["id"], **translated})
        overrides = definition.get("skills")
        if not isinstance(overrides, dict) or set(overrides) != {entry["id"] for entry in entries}:
            raise BuildError(f"Locale {route} must translate every published skill")
        translated_skills = {}
        for entry in entries:
            translated = overrides[entry["id"]]
            required = ("name", "tagline", "purpose", "when_to_use", "workflow", "boundaries")
            missing = [field for field in required if not translated.get(field)] if isinstance(translated, dict) else list(required)
            if missing or any(not isinstance(translated[field], list) for field in ("when_to_use", "workflow", "boundaries")):
                raise BuildError(f"Locale {route} skill {entry['id']} is incomplete: {', '.join(missing)}")
            merged = dict(entry)
            merged.update(translated)
            translated_skills[entry["id"]] = merged
        translated_site = dict(site)
        translated_site.update(definition.get("site", {}))
        translated_site["categories"] = translated_categories
        result.append({
            "id": route, "lang": definition.get("lang", route), "label": definition.get("label", route.upper()),
            "path": route, "ui": ui, "site": translated_site,
            "categories": translated_categories, "skills": translated_skills,
        })
    if not {"pt-br", "es"} <= {locale["id"] for locale in result}:
        raise BuildError("locales.json must define pt-br and es")
    return result


def list_items(items: list[str], class_name: str) -> str:
    return "".join(f'<li class="{class_name}">{esc(item)}</li>' for item in items)


def nav_html(prefix: str, current: str, ui: dict[str, str]) -> str:
    links = (("home", ui["UI_NAV_HOME"], f"{prefix}index.html"),
             ("getting-started", ui["UI_NAV_GETTING_STARTED"], f"{prefix}getting-started.html"),
             ("skills", ui["UI_NAV_SKILLS"], f"{prefix}skills/index.html"))
    return "".join(f'<a href="{href}"{(" aria-current=\"page\"" if current == key else "")}>{esc(label)}</a>' for key, label, href in links)


def sidebar_html(locale: dict, entries: list[dict], route: str, local_prefix: str) -> str:
    ui = locale["ui"]
    current_skill = route.removeprefix("skills/") if route.startswith("skills/") else ""
    html_parts = [
        f'<nav class="docs-nav"><p class="docs-nav-label">{esc(ui["UI_DOCS_NAV"])}</p>',
        f'<a class="docs-nav-link" href="{local_prefix}index.html">{esc(ui["UI_NAV_HOME"])}</a>',
        f'<a class="docs-nav-link" href="{local_prefix}getting-started.html">{esc(ui["UI_NAV_GETTING_STARTED"])}</a>',
        f'<a class="docs-nav-link" href="{local_prefix}skills/index.html"{(" aria-current=\"page\"" if route == "skills/index.html" else "")}>{esc(ui["UI_SIDEBAR_CATALOG"])}</a>',
    ]
    by_category = {category["id"]: [] for category in locale["site"]["categories"]}
    for entry in entries:
        by_category.setdefault(entry["category"], []).append(entry)
    for category in locale["site"]["categories"]:
        html_parts.append(f'<p class="docs-nav-group">{esc(category["label"])}</p>')
        for entry in by_category.get(category["id"], []):
            active = ' aria-current="page"' if current_skill == entry["slug"] else ""
            html_parts.append(f'<a class="docs-nav-link" href="{local_prefix}skills/{entry["slug"]}.html"{active}>{esc(entry["name"])}</a>')
    html_parts.append("</nav>")
    return "".join(html_parts)


def breadcrumb_html(locale: dict, route: str, title: str, local_prefix: str) -> str:
    ui = locale["ui"]
    if route == "getting-started.html":
        items = [(local_prefix + "index.html", ui["UI_BREADCRUMB_HOME"]), (None, ui["UI_BREADCRUMB_GETTING"])]
    elif route == "skills/index.html":
        items = [(local_prefix + "index.html", ui["UI_BREADCRUMB_HOME"]), (None, ui["UI_BREADCRUMB_SKILLS"])]
    elif route.startswith("skills/"):
        items = [(local_prefix + "index.html", ui["UI_BREADCRUMB_HOME"]), (local_prefix + "skills/index.html", ui["UI_BREADCRUMB_SKILLS"]), (None, title)]
    else:
        return ""
    parts = []
    for index, (href, label) in enumerate(items):
        if index:
            parts.append('<span class="breadcrumb-separator" aria-hidden="true">/</span>')
        if href:
            parts.append(f'<a href="{href}">{esc(label)}</a>')
        else:
            parts.append(f'<span class="breadcrumb-current">{esc(label)}</span>')
    return "".join(parts)


def toc_html(locale: dict, route: str) -> str:
    ui = locale["ui"]
    if route == "getting-started.html":
        items = (("install", ui["UI_INSTALL_ONE_TITLE"]), ("how-it-works", ui["UI_HOW_EYEBROW"]), ("agents", ui["UI_AGENTS_TITLE"]), ("boundary", ui["UI_BOUNDARY_TITLE"]))
    elif route == "skills/index.html":
        items = (("catalog", ui["UI_CATALOG_TITLE"]),)
    elif route.startswith("skills/"):
        items = (("overview", ui["UI_WHAT_IT_IS"]), ("when-to-use", ui["UI_USE_IT_WHEN"]), ("workflow", ui["UI_WORKFLOW"]), ("boundaries", ui["UI_BOUNDARY"]), ("related", ui["UI_RELATED_SKILLS"]))
    else:
        return ""
    return '<nav class="docs-toc-list">' + "".join(f'<a href="#{anchor}">{esc(label)}</a>' for anchor, label in items) + "</nav>"


def prev_next_html(locale: dict, entries: list[dict], current: dict, local_prefix: str) -> str:
    index = next((position for position, entry in enumerate(entries) if entry["slug"] == current["slug"]), -1)
    if index < 0:
        return ""
    links = []
    if index > 0:
        previous = entries[index - 1]
        links.append(f'<a href="{previous["slug"]}.html"><small>← {esc(locale["ui"]["UI_PREVIOUS_SKILL"])}</small><strong>{esc(previous["name"])}</strong></a>')
    else:
        links.append("<span></span>")
    if index + 1 < len(entries):
        following = entries[index + 1]
        links.append(f'<a href="{following["slug"]}.html"><small>{esc(locale["ui"]["UI_NEXT_SKILL"])} →</small><strong>{esc(following["name"])}</strong></a>')
    else:
        links.append("<span></span>")
    return '<nav class="prev-next" aria-label="' + esc(locale["ui"]["UI_DOCS_NAV"]) + '">' + "".join(links) + "</nav>"


def language_switcher(current_locale: dict, locales: list[dict], page_relative: str) -> str:
    page_parent = posixpath.dirname(page_relative) or "."
    if page_relative.startswith("skills/"):
        route = page_relative
    elif "/skills/" in page_relative:
        route = "skills/" + page_relative.rsplit("/skills/", 1)[1]
    else:
        route = posixpath.basename(page_relative)
    links = []
    for locale in locales:
        target = posixpath.join(locale["path"], route) if locale["path"] else route
        href = posixpath.relpath(target, page_parent)
        current = ' aria-current="true"' if locale["id"] == current_locale["id"] else ""
        links.append(f'<a href="{href}"{current}>{esc(locale["label"])}</a>')
    return "".join(links)


def render_layout(template: str, *, title: str, description: str, content: str,
                  asset_prefix: str, local_prefix: str, current: str, repo: str,
                  locale: dict, locales: list[dict], page_relative: str,
                  sidebar: str, breadcrumb: str, toc: str, layout_class: str) -> str:
    ui = locale["ui"]
    values = {**ui, "TITLE": esc(title), "META_DESCRIPTION": esc(description), "CONTENT": content,
              "LANG": esc(locale["lang"]), "ASSET_PREFIX": asset_prefix + "assets/",
              "HOME_LINK": local_prefix + "index.html", "GETTING_STARTED_LINK": local_prefix + "getting-started.html",
              "SKILLS_LINK": local_prefix + "skills/index.html", "NAV": nav_html(local_prefix, current, ui),
              "LANG_SWITCHER": language_switcher(locale, locales, page_relative), "REPO_LINK": esc(repo),
              "BODY_CLASS": current, "SIDEBAR": sidebar, "BREADCRUMB": breadcrumb,
              "TOC": toc, "LAYOUT_CLASS": layout_class}
    output = template
    for key, value in values.items():
        output = output.replace("{{" + key + "}}", str(value))
    return output


def render_template(path: Path, replacements: dict[str, str]) -> str:
    output = path.read_text(encoding="utf-8")
    for key, value in replacements.items():
        output = output.replace("{{" + key + "}}", value)
    return output


def featured_cards(entries: list[dict], ui: dict[str, str]) -> str:
    cards = []
    for entry in entries[:3]:
        icon = "◌" if entry["category"] == "discovery" else "↗" if entry["category"] == "runtime" else "✦"
        cards.append(f'<a class="feature-card" href="skills/{esc(entry["slug"])}.html"><span class="card-icon" aria-hidden="true">{icon}</span><span><h3>{esc(entry["name"])}</h3><p>{esc(entry["tagline"])}</p></span><span class="card-arrow">{esc(ui["UI_CARD_EXPLORE"])} ↗</span></a>')
    return "".join(cards)


def category_sections(entries: list[dict], site: dict, ui: dict[str, str]) -> str:
    by_category = {category["id"]: [] for category in site["categories"]}
    for entry in entries:
        by_category.setdefault(entry["category"], []).append(entry)
    sections = []
    for category in site["categories"]:
        cards = []
        for entry in by_category.get(category["id"], []):
            icon = "◌" if category["id"] == "discovery" else "↗" if category["id"] == "runtime" else "✦"
            cards.append(f'<a class="catalog-card" href="{esc(entry["slug"])}.html"><span class="card-icon" aria-hidden="true">{icon}</span><h3>{esc(entry["name"])}</h3><p>{esc(entry["tagline"])}</p><span class="card-arrow">{esc(ui["UI_CARD_READ_DETAILS"])} ↗</span></a>')
        sections.append(f'<section class="catalog-group"><div class="catalog-group-heading"><h2>{esc(category["label"])}</h2><p>{esc(category["description"])}</p></div><div class="catalog-cards">{"".join(cards)}</div></section>')
    return "".join(sections)


def related_links(entry: dict, by_id: dict[str, dict]) -> str:
    return "".join(f'<a href="{esc(by_id[related]["slug"])}.html">{esc(by_id[related]["name"])} <span>↗</span></a>' for related in entry["related"])


def copy_static_assets() -> None:
    static_root, output_assets = WEBSITE / "static", OUTPUT / "assets"
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
    problems = []
    for page in OUTPUT.rglob("*.html"):
        for target in LINK_PATTERN.findall(page.read_text(encoding="utf-8")):
            parsed = urlparse(target)
            if parsed.scheme or target.startswith(("//", "#")):
                continue
            if not (page.parent / target).resolve().is_file():
                problems.append(f"{page.relative_to(OUTPUT)} -> {target}")
    if problems:
        raise BuildError("Broken generated links:\n  " + "\n  ".join(problems))


def build() -> Path:
    site = read_json(WEBSITE / "content" / "site.json")
    catalog = read_json(WEBSITE / "content" / "skills.json")
    locales_file = read_json(WEBSITE / "content" / "locales.json")
    entries, _ = validate_catalog(catalog, site)
    locales = localized_catalog(site, entries, locales_file)
    template_root = WEBSITE / "templates"
    layout = (template_root / "layout.html").read_text(encoding="utf-8")
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    OUTPUT.mkdir(parents=True)
    copy_static_assets()

    for locale in locales:
        locale_site = locale["site"]
        localized_entries = [locale["skills"][entry["id"]] for entry in entries]
        by_id = {entry["id"]: entry for entry in localized_entries}

        def write_page(route: str, content_template: str, *, title: str, description: str,
                       current: str, replacements: dict[str, str]) -> None:
            relative = posixpath.join(locale["path"], route) if locale["path"] else route
            destination = OUTPUT / Path(relative)
            page_parent = destination.parent.relative_to(OUTPUT)
            asset_prefix = "../" * len(page_parent.parts)
            local_prefix = "../" if route.startswith("skills/") else ""
            values = dict(locale["ui"])
            values.update(replacements)
            values.setdefault("PREV_NEXT", "")
            content = render_template(template_root / content_template, values)
            docs_route = route != "index.html"
            sidebar = sidebar_html(locale, localized_entries, route, local_prefix) if docs_route else ""
            breadcrumb = breadcrumb_html(locale, route, title, local_prefix) if docs_route else ""
            toc = toc_html(locale, route) if docs_route else ""
            page = render_layout(layout, title=title, description=description, content=content,
                                 asset_prefix=asset_prefix, local_prefix=local_prefix, current=current,
                                 repo=locale_site["repo"], locale=locale, locales=locales, page_relative=relative,
                                 sidebar=sidebar, breadcrumb=breadcrumb, toc=toc,
                                 layout_class="home-layout" if route == "index.html" else "docs-layout")
            if "{{" in page or "}}" in page:
                raise BuildError(f"Unresolved template token in {relative}")
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(page, encoding="utf-8")

        common = {"INSTALL_ONE": esc(locale_site["install_one"]), "INSTALL_MULTIPLE": esc(locale_site["install_multiple"]),
                  "SKILL_COUNT": str(len(localized_entries)), "FEATURED_CARDS": featured_cards(localized_entries, locale["ui"]),
                  "CATEGORY_SECTIONS": category_sections(localized_entries, locale_site, locale["ui"])}
        write_page("index.html", "index.html", title=locale_site["name"], description=locale_site["description"], current="home", replacements=common)
        getting_title = locale["ui"]["UI_GETTING_TITLE"].replace("<br>", " ").replace("<em>", "").replace("</em>", "")
        write_page("getting-started.html", "getting-started.html", title=getting_title, description=locale["ui"]["UI_GETTING_LEDE"], current="getting-started", replacements=common)
        write_page("skills/index.html", "skills-index.html", title=locale["ui"]["UI_CATALOG_TITLE"], description=locale["ui"]["UI_CATALOG_LEDE"], current="skills", replacements=common)
        for entry in localized_entries:
            replacements = {"CATEGORY_LABEL": esc(next(item["label"] for item in locale_site["categories"] if item["id"] == entry["category"])),
                            "SKILL_NAME": esc(entry["name"]), "TAGLINE": esc(entry["tagline"]), "INSTALL": esc(entry["install"]),
                            "PURPOSE": esc(entry["purpose"]), "WHEN_TO_USE": list_items(entry["when_to_use"], ""),
                            "WORKFLOW": list_items(entry["workflow"], ""), "BOUNDARIES": list_items(entry["boundaries"], ""),
                            "RELATED": related_links(entry, by_id),
                            "PREV_NEXT": prev_next_html(locale, localized_entries, entry, "../")}
            write_page(f"skills/{entry['slug']}.html", "skill-detail.html", title=entry["name"], description=entry["purpose"], current="skills", replacements=replacements)
        write_page("404.html", "404.html", title=locale["ui"]["UI_NOT_FOUND_TITLE"], description=locale["ui"]["UI_NOT_FOUND_LEDE"], current="home", replacements={})
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
