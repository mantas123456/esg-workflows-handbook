"""Build the PDF edition of the handbook from the built site.

Each page in the mkdocs.yml nav is printed by Chromium (Playwright, already used
for the browser tests) with the theme's print styles, so diagrams and tables look
as they do on the site. The pages are merged into one PDF with a cover page and a
bookmark per page (pypdf).

    mkdocs build --strict
    python scripts/build_pdf.py                         # site/ -> esg-workflows-handbook.pdf
    python scripts/build_pdf.py --site site --out handbook.pdf --version 1.0
"""
from __future__ import annotations

import argparse
import functools
import html
import http.server
import io
import re
import threading
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def nav_pages(mkdocs_yml: Path = ROOT / "mkdocs.yml") -> list[tuple[str, str, str]]:
    """(section, title, docs path) for every page in the nav, in order."""
    text = mkdocs_yml.read_text(encoding="utf-8")
    start = re.search(r"^nav:\s*$", text, re.M)
    if not start:
        raise ValueError("no nav: in mkdocs.yml")
    nav = text[start.start():]
    out, section = [], ""
    for line in nav.splitlines()[1:]:
        if not line.startswith("  "):
            break
        m = re.match(r"^  - (?:\"?(.+?)\"?): (\S+\.md)\s*$", line)
        if m:                                             # a top-level page, such as Home
            out.append(("", m.group(1), m.group(2)))
            continue
        m = re.match(r"^  - (.+?):\s*$", line)
        if m:
            section = m.group(1).strip('"')
            continue
        m = re.match(r"^      - (?:\"(.+?)\"|(.+?)): (\S+\.md)\s*$", line)
        if m:
            out.append((section, m.group(1) or m.group(2), m.group(3)))
    if not out:
        raise ValueError("no pages found in the mkdocs.yml nav")
    return out


def page_url(base_url: str, docs_path: str) -> str:
    """URL of a page with use_directory_urls (the mkdocs default)."""
    stem = docs_path[:-3]
    if stem == "index":
        return base_url
    if stem.endswith("/index"):
        return base_url + stem[: -len("index")]
    return base_url + stem + "/"


def cover_html(version: str, built: date) -> str:
    v = html.escape(version)
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>ESG Workflows Handbook</title>
<style>
  body {{ font-family: Arial, Helvetica, sans-serif; margin: 0; color: #1b1b1b; }}
  .page {{ height: 260mm; display: flex; flex-direction: column; justify-content: center; padding: 0 20mm; }}
  h1 {{ font-size: 32pt; margin: 0 0 6mm; color: #1b5e20; }}
  p {{ font-size: 12pt; line-height: 1.5; margin: 0 0 4mm; }}
  .small {{ font-size: 9.5pt; color: #444; }}
</style></head><body><div class="page">
  <h1>ESG Workflows Handbook</h1>
  <p>Step-by-step workflows for CBAM, Scope 3, VSME and CSRD / ESRS.</p>
  <p>Version {v}, built {built:%d %B %Y}.</p>
  <p class="small">Self-reviewed by its author; not yet reviewed by an external practitioner. All pages are drafts.
  Not legal advice: the handbook explains the rules in its own words and links the sources. The regulation,
  the Commission's guidance and your competent authority always take priority. Worked examples use fictional
  companies and made-up numbers.</p>
  <p class="small">Online edition: https://mantas123456.github.io/esg-workflows-handbook/<br>
  Source: https://github.com/mantas123456/esg-workflows-handbook<br>
  Text and templates: CC BY 4.0. Code: MIT.</p>
</div></body></html>"""


def build_pdf(base_url: str, out: Path, version: str = "dev", pages: list[tuple[str, str, str]] | None = None,
              browser: Any = None, built: date | None = None) -> int:
    """Print the cover and every page to one PDF; return the number of PDF pages.

    Pass a Playwright ``browser`` to reuse one (as the tests do); otherwise one is launched.
    """
    from pypdf import PdfReader, PdfWriter

    pages = pages if pages is not None else nav_pages()
    own = None
    if browser is None:
        from playwright.sync_api import sync_playwright
        own = sync_playwright().start()
        browser = own.chromium.launch()
    writer = PdfWriter()
    pdf_options = dict(format="A4", print_background=True,
                       margin={"top": "16mm", "bottom": "16mm", "left": "14mm", "right": "14mm"})
    try:
        tab = browser.new_page()
        tab.emulate_media(media="print")
        tab.set_content(cover_html(version, built or date.today()))
        for p in PdfReader(io.BytesIO(tab.pdf(**pdf_options))).pages:
            writer.add_page(p)
        writer.add_outline_item(title="Cover", page_number=0)
        parents: dict[str, Any] = {}
        for section, title, docs_path in pages:
            tab.goto(page_url(base_url, docs_path), wait_until="networkidle")
            tab.wait_for_timeout(300)                                 # let diagrams finish drawing
            first = len(writer.pages)
            for p in PdfReader(io.BytesIO(tab.pdf(**pdf_options))).pages:
                writer.add_page(p)
            if section and section not in parents:
                parents[section] = writer.add_outline_item(title=section, page_number=first)
            writer.add_outline_item(title=title, page_number=first, parent=parents.get(section))
        tab.close()
    finally:
        if own is not None:
            browser.close()
            own.stop()
    writer.add_metadata({"/Title": f"ESG Workflows Handbook {version}", "/Author": "ESG Workflows Handbook"})
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("wb") as f:
        writer.write(f)
    return len(writer.pages)


class _Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args: Any) -> None:
        pass


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--site", type=Path, default=ROOT / "site", help="built site folder (mkdocs build)")
    parser.add_argument("--out", type=Path, default=ROOT / "esg-workflows-handbook.pdf")
    parser.add_argument("--version", default="dev")
    args = parser.parse_args(argv)
    if not (args.site / "index.html").exists():
        parser.error(f"{args.site} has no index.html: run mkdocs build first")
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(_Quiet, directory=str(args.site)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        n = build_pdf(f"http://127.0.0.1:{server.server_address[1]}/", args.out, args.version)
    finally:
        server.shutdown()
    print(f"built {args.out} ({n} pages)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
