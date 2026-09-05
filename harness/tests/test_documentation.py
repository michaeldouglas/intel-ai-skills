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
