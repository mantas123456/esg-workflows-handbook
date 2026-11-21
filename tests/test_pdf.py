"""The PDF edition (scripts/build_pdf.py): every nav page is included, and a small build works."""
import sys
from pathlib import Path

from test_tools import offline, site_url  # noqa: F401  (pytest fixtures)

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_pdf  # noqa: E402


def test_nav_pages_cover_every_page_in_the_nav() -> None:
    pages = build_pdf.nav_pages()
    paths = [p for _, _, p in pages]
    assert paths[0] == "index.md" and len(paths) == len(set(paths))
    for p in paths:
        assert (ROOT / "docs" / p).exists(), p
    nav = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    assert len(paths) == nav.split("\nnav:")[1].count(".md")          # nothing in the nav is skipped
    assert {"Start here", "CBAM", "Scope 3", "VSME", "CSRD / ESRS", "Tools and templates"} <= {s for s, _, _ in pages}


def test_page_urls() -> None:
    assert build_pdf.page_url("http://h/", "index.md") == "http://h/"
    assert build_pdf.page_url("http://h/", "tools/index.md") == "http://h/tools/"
    assert build_pdf.page_url("http://h/", "cbam/cb1-scope-check.md") == "http://h/cbam/cb1-scope-check/"


def test_small_build(browser, site_url, tmp_path) -> None:  # noqa: F811
    from pypdf import PdfReader

    pages = [p for p in build_pdf.nav_pages() if p[2] in ("index.md", "cbam/cb1-scope-check.md", "csrd/c1-scope.md")]
    out = tmp_path / "h.pdf"
    n = build_pdf.build_pdf(site_url, out, version="test", pages=pages, browser=browser)
    reader = PdfReader(str(out))
    assert len(reader.pages) == n >= 4                                   # cover + at least one page each
    text = " ".join(reader.pages[i].extract_text() for i in range(n))
    assert "Version test" in text and "Not legal advice" in text
    assert "CB1 Scope check" in text and "C1 Am I in scope after Omnibus I?" in text
    titles = [o.title for o in reader.outline if not isinstance(o, list)]
    assert titles[0] == "Cover" and "CBAM" in titles and "CSRD / ESRS" in titles
    assert reader.metadata.title == "ESG Workflows Handbook test"
