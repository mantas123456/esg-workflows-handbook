"""Consistency of the whole handbook: page format, dates, templates and tools.

Broken internal links and anchors fail `mkdocs build --strict` (mkdocs.yml, validation).
"""
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
WORKFLOWS = yaml.safe_load((ROOT / "data/workflows.yml").read_text(encoding="utf-8"))
HEADINGS = ["## In one sentence", "## Who does this and when", "## Inputs", "## Steps", "## Worked example",
            "## Common mistakes", "## Evidence to keep", "## Templates and tools", "## Reuse in other reports",
            "## Sources"]
sys.path.insert(0, str(ROOT / "scripts"))


def _steps():
    for track in WORKFLOWS["tracks"]:
        for step in track["steps"]:
            yield track, step, DOCS / track["folder"] / step["file"]


def test_template_lists_the_same_headings() -> None:
    template = (DOCS / "_chapter_template.md").read_text(encoding="utf-8")
    assert [l.strip() for l in template.splitlines() if l.startswith("## ")] == HEADINGS


def test_every_written_page_follows_the_template() -> None:
    for _, step, page in _steps():
        if step["status"] == "planned":
            continue
        text = page.read_text(encoding="utf-8")
        heads = [l.strip() for l in text.splitlines() if l.startswith("## ")]
        assert [h for h in heads if h in HEADINGS] == HEADINGS, (step["id"], sorted(set(HEADINGS) - set(heads)))
        assert re.search(r"^last_checked: \d{4}-\d{2}-\d{2}$", text, re.M), step["id"]
        assert re.search(r"^# " + re.escape(step["id"]) + " ", text, re.M), step["id"]
        assert "not legal advice" in text.lower(), step["id"]


def test_every_template_is_linked_from_a_step() -> None:
    import build_templates

    listed = {t for _, s, _ in _steps() for t in s.get("templates", [])}
    assert listed == {t["id"] for t in build_templates.catalog()}


def test_every_tool_has_a_page_a_step_and_a_test() -> None:
    pages = {p.stem for p in (DOCS / "tools").glob("*.md")} - {"index"}
    listed = {t for _, s, _ in _steps() for t in s.get("tools", [])}
    assert listed == pages
    tests = " ".join(p.read_text(encoding="utf-8") for p in (ROOT / "tests").glob("test_tools*.py"))
    for tool in pages:
        assert f"tools/{tool}/" in tests, tool
        assert (DOCS / "tools" / f"{tool}.js").exists(), tool


def test_index_pages_are_up_to_date() -> None:
    import build_pages

    assert (DOCS / "tools/index.md").read_text(encoding="utf-8") == build_pages.render_tools_index()
    assert (DOCS / "templates.md").read_text(encoding="utf-8") == build_pages.render_templates_index()
    nav = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    assert "All tools: tools/index.md" in nav and "All templates: templates.md" in nav


def test_issue_form_asks_for_the_page_and_a_source() -> None:
    form = yaml.safe_load((ROOT / ".github/ISSUE_TEMPLATE/report-error.yml").read_text(encoding="utf-8"))
    assert form["name"] == "Report an error or outdated rule"
    ids = {b.get("id") for b in form["body"]}
    assert {"page", "kind", "what", "source"} <= ids
    f4 = (DOCS / "foundations/keeping-up.md").read_text(encoding="utf-8")
    assert "issues/new?template=report-error.yml" in f4
