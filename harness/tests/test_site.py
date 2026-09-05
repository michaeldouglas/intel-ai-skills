from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
SITE_ROOT = REPOSITORY_ROOT / "docs" / "site"
OUTPUT_ROOT = SITE_ROOT / "build" / "site"
sys.path.insert(0, str(SITE_ROOT / "scripts"))

import build_site  # noqa: E402


def test_site_build_covers_every_published_skill() -> None:
    catalog = json.loads((SITE_ROOT / "content" / "skills.json").read_text(encoding="utf-8"))
    indexed = {entry["id"] for entry in catalog["skills"]}
    discovered = {path.name for path in (REPOSITORY_ROOT / "skills").iterdir() if path.is_dir()}
    assert indexed == discovered


def test_site_build_generates_expected_routes_and_assets() -> None:
    output = build_site.build()
    catalog = json.loads((SITE_ROOT / "content" / "skills.json").read_text(encoding="utf-8"))
    expected = {
        "index.html",
        "getting-started.html",
        "skills/index.html",
        "404.html",
        *(f"skills/{entry['slug']}.html" for entry in catalog["skills"]),
    }
    expected |= {
        f"{locale}/{route}"
        for locale in ("pt-br", "es")
        for route in expected.copy()
    }
    actual = {str(path.relative_to(output)).replace("\\", "/") for path in output.rglob("*.html")}
    assert actual == expected
    for logo in build_site.REQUIRED_LOGOS:
        assert (output / "assets" / logo).is_file()


def test_site_build_generates_localized_content_and_language_switchers() -> None:
    output = build_site.build()
    portuguese_home = (output / "pt-br" / "index.html").read_text(encoding="utf-8")
    spanish_home = (output / "es" / "index.html").read_text(encoding="utf-8")
    portuguese_skill = (output / "pt-br" / "skills" / "intel-hardware-advisor.html").read_text(encoding="utf-8")
    assert '<html lang="pt-BR">' in portuguese_home
    assert "Comece aqui" in portuguese_home
    assert "Empieza aquí" in spanish_home
    assert "Inspecione o ambiente local" in portuguese_skill
    assert 'data-language-select' in portuguese_home
    assert 'value="../index.html"' in portuguese_home
    assert 'value="../es/index.html"' in portuguese_home
    assert 'value="../../es/skills/intel-hardware-advisor.html"' in portuguese_skill
    assert all("{{" not in page.read_text(encoding="utf-8") for page in output.rglob("*.html"))


def test_public_site_explains_agent_portability_and_keeps_maintainer_preview_out() -> None:
    output = build_site.build()
    getting_started = (output / "getting-started.html").read_text(encoding="utf-8")
    catalog = (output / "skills" / "index.html").read_text(encoding="utf-8")
    installer = (output / "skills" / "intel-openvino-installer.html").read_text(encoding="utf-8")
    assert "Claude" in getting_started
    assert "agent-agnostic" in getting_started
    assert "Choose the skill for your task." in catalog
    assert "The skill is portable" in installer
    assert "python docs/site/scripts/serve_site.py" not in getting_started
    assert "For maintainers" not in getting_started
    assert "What happens automatically" in installer
    assert "What it does not do" in installer


def test_docs_pages_use_grouped_navigation_and_contextual_page_navigation() -> None:
    output = build_site.build()
    skill = (output / "skills" / "intel-openvino-installer.html").read_text(encoding="utf-8")
    portuguese_skill = (output / "pt-br" / "skills" / "intel-openvino-installer.html").read_text(encoding="utf-8")
    getting_started = (output / "getting-started.html").read_text(encoding="utf-8")

    assert 'class="docs-frame docs-layout"' in skill
    assert 'class="docs-sidebar"' in skill
    assert 'class="docs-nav"' in skill
    assert 'class="breadcrumbs"' in skill
    assert 'class="docs-toc"' in skill
    assert 'href="#workflow"' in skill
    assert 'class="prev-next"' in skill
    assert 'data-skill-search' in skill
    assert '<details class="docs-nav-section"' in skill
    assert 'data-back-to-top' in skill
    assert 'id="icon-search"' in skill
    assert 'Navegação da documentação' in portuguese_skill
    assert 'href="#agents"' in getting_started
    assert "Comece pelo" in (output / "pt-br" / "getting-started.html").read_text(encoding="utf-8")


def test_site_keeps_existing_localized_markdown_outside_generated_output() -> None:
    assert (REPOSITORY_ROOT / "docs" / "README.pt-BR.md").is_file()
    assert (REPOSITORY_ROOT / "docs" / "README.es.md").is_file()
    assert not (OUTPUT_ROOT / "README.pt-BR.md").exists()
    assert not (OUTPUT_ROOT / "README.es.md").exists()


def test_pages_workflow_builds_docs_site_from_main() -> None:
    workflow = (REPOSITORY_ROOT / ".github" / "workflows" / "deploy-pages.yml").read_text(encoding="utf-8")
    assert "branches: [main]" in workflow
    assert "python docs/site/scripts/build_site.py" in workflow
    assert "path: docs/site/build/site" in workflow
    assert "actions/upload-pages-artifact@v4" in workflow
    assert "actions/deploy-pages@v4" in workflow
    assert "pages: write" in workflow
    assert "id-token: write" in workflow


def test_site_specific_tools_are_inside_docs_site() -> None:
    assert (SITE_ROOT / "scripts" / "build_site.py").is_file()
    assert (SITE_ROOT / "scripts" / "serve_site.py").is_file()
    assert not (REPOSITORY_ROOT / "website").exists()
    assert not (REPOSITORY_ROOT / "scripts" / "build_site.py").exists()
    assert not (REPOSITORY_ROOT / "scripts" / "serve_site.py").exists()
    assert not (REPOSITORY_ROOT / "build" / "site").exists()


def test_site_interactions_are_local_and_javascript_is_syntax_valid() -> None:
    script = (SITE_ROOT / "static" / "site.js").read_text(encoding="utf-8")
    assert "data-language-select" in script
    assert "data-back-to-top" in script
    assert "scrollIntoView" in script
    assert "new URLSearchParams" in script
    node = shutil.which("node")
    if node:
        result = subprocess.run([node, "--check", str(SITE_ROOT / "static" / "site.js")], capture_output=True, text=True)
        assert result.returncode == 0, result.stderr
