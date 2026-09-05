from __future__ import annotations

import re
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
DOCUMENTS = {
    "english": REPOSITORY_ROOT / "README.md",
    "portuguese": REPOSITORY_ROOT / "docs" / "README.pt-BR.md",
    "spanish": REPOSITORY_ROOT / "docs" / "README.es.md",
}
PUBLISHED_SKILLS = (
    "skills/intel-docs-reader/SKILL.md",
    "skills/intel-hardware-advisor/SKILL.md",
)


def local_markdown_links(document: Path) -> list[Path]:
    content = document.read_text(encoding="utf-8")
    links = re.findall(r"\]\(([^)#]+)(?:#[^)]+)?\)", content)
    links.extend(re.findall(r'href="([^"#]+)(?:#[^"]+)?"', content))
    targets = []
    for link in links:
        if link.startswith(("http://", "https://", "mailto:")):
            continue
        targets.append((document.parent / link).resolve())
    return targets


def test_localized_documents_and_language_switcher_exist() -> None:
    assert all(document.is_file() for document in DOCUMENTS.values())

    english = DOCUMENTS["english"].read_text(encoding="utf-8")
    assert '<a href="./docs/README.pt-BR.md">🇧🇷 Português (Brasil)</a>' in english
    assert '<a href="./docs/README.es.md">🇪🇸 Español</a>' in english

    portuguese = DOCUMENTS["portuguese"].read_text(encoding="utf-8")
    spanish = DOCUMENTS["spanish"].read_text(encoding="utf-8")
    assert "../README.md" in portuguese
    assert "../README.md" in spanish
    assert "README.es.md" in portuguese
    assert "README.pt-BR.md" in spanish


def test_each_readme_catalogs_the_published_skills_before_project_details() -> None:
    for document in DOCUMENTS.values():
        content = document.read_text(encoding="utf-8")
        assert "intel-docs-reader" in content
        assert "intel-hardware-advisor" in content
        details_heading = next(
            (heading for heading in ("## Why Intel AI Skills?", "## Por que Intel AI Skills?", "## ¿Por qué Intel AI Skills?") if heading in content),
            None,
        )
        assert details_heading is not None
        skills_position = min(content.index(skill) for skill in ("intel-docs-reader", "intel-hardware-advisor"))
        assert skills_position < content.index(details_heading)


def test_readme_local_links_resolve() -> None:
    for document in DOCUMENTS.values():
        missing = [str(target) for target in local_markdown_links(document) if not target.exists()]
        assert not missing, f"Broken links in {document}: {missing}"


def test_each_readme_links_to_both_published_skill_files() -> None:
    for document in DOCUMENTS.values():
        targets = set(local_markdown_links(document))
        expected = {(document.parent / ".." / path).resolve() if document.parent.name == "docs" else (document.parent / path).resolve() for path in PUBLISHED_SKILLS}
        assert expected <= targets, f"Missing skill links in {document}"


def test_each_readme_documents_agent_neutral_installation() -> None:
    for document in DOCUMENTS.values():
        content = document.read_text(encoding="utf-8")
        for skill in ("intel-hardware-advisor", "intel-docs-reader"):
            assert f"npx skills add michaeldouglas/intel-ai-skills --skill {skill} -a codex" in content
        assert "claude-code" in content
        assert "outro agente" in content or "otro agente" in content or "another supported agent" in content
        assert "cd skills/intel-" not in content


def test_public_readmes_do_not_expose_harness_internals() -> None:
    forbidden = ("harness/", ".codex", ".agents", "Spec Kit", "Graphify")
    for document in DOCUMENTS.values():
        content = document.read_text(encoding="utf-8")
        assert not any(term in content for term in forbidden), f"Internal harness detail leaked into {document}"


def test_openvino_skills_instruct_agents_to_run_bundled_scripts() -> None:
    hardware_skill = (REPOSITORY_ROOT / "skills/intel-hardware-advisor/SKILL.md").read_text(encoding="utf-8")
    docs_skill = (REPOSITORY_ROOT / "skills/intel-docs-reader/SKILL.md").read_text(encoding="utf-8")
    assert "invoke the bundled" in hardware_skill
    assert "Do not ask the user" in hardware_skill
    assert "scripts/hardware_probe.py" in hardware_skill
    assert "invoke the bundled" in docs_skill
    assert "Do not ask the user" in docs_skill
    assert "scripts/read_openvino_docs.py" in docs_skill


def test_harness_uses_local_openvino_docs_as_sdd_knowledge_base() -> None:
    harness_instructions = (REPOSITORY_ROOT / "harness/AGENTS.md").read_text(encoding="utf-8")
    assert "docs/2026/" in harness_instructions
    assert "primary agent MUST consult" in harness_instructions
    assert "openvino-researcher" in harness_instructions


def test_published_skills_have_standard_agent_skill_frontmatter() -> None:
    for relative_path in PUBLISHED_SKILLS:
        skill = (REPOSITORY_ROOT / relative_path).read_text(encoding="utf-8")
        assert skill.startswith("---\n")
        assert re.search(r"^name:\s*[a-z0-9][a-z0-9-]*$", skill, re.MULTILINE)
        assert re.search(r"^description:\s*.+$", skill, re.MULTILINE)


def test_published_skills_do_not_depend_on_internal_harness_paths() -> None:
    forbidden = ("harness/", ".codex", ".agents")
    for skill_root in (REPOSITORY_ROOT / "skills").iterdir():
        if not skill_root.is_dir():
            continue
        for file in skill_root.rglob("*"):
            if file.is_file() and file.suffix.lower() in {".md", ".py", ".json", ".toml"}:
                content = file.read_text(encoding="utf-8")
                assert not any(term in content for term in forbidden), f"Internal path leaked into {file}"
