"""Check the external links in the pages and data files (manual: needs the network).

Internal links and anchors are checked by `mkdocs build --strict`. This script
finds every http(s) link in docs/ and data/, requests each once, and lists the
ones that fail. Some official sites refuse automated requests (403) or answer
with an empty 202: those are listed as "could not check", not as broken.

    python scripts/check_links.py
"""
from __future__ import annotations

import re
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
URL = re.compile(r"https?://[^\s)\]\"'<>`|]+")        # Markdown: a link ends at ")"
URL_YAML = re.compile(r"https?://[^\s\"'<>`|]+")       # YAML: a URL may contain brackets
SKIP = ("127.0.0.1", "localhost", "example.com")
HEADERS = {"User-Agent": "Mozilla/5.0 (link check; esg-workflows-handbook)"}


def find_links() -> dict[str, set[str]]:
    """URL -> files that use it."""
    out: dict[str, set[str]] = {}
    files = [p for p in (ROOT / "docs").rglob("*.md")] + list((ROOT / "data").rglob("*.yml"))
    for f in files:
        pattern = URL_YAML if f.suffix == ".yml" else URL
        for url in pattern.findall(f.read_text(encoding="utf-8")):
            url = url.rstrip(".,;:}")                      # trailing punctuation, end of a YAML flow map
            if not any(s in url for s in SKIP):
                out.setdefault(url, set()).add(f.relative_to(ROOT).as_posix())
    return out


def status(url: str) -> tuple[str, int | str]:
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return url, r.status
    except urllib.error.HTTPError as e:
        return url, e.code
    except Exception as e:  # noqa: BLE001 (timeouts, DNS, TLS)
        return url, type(e).__name__


def main() -> int:
    links = find_links()
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = dict(pool.map(status, sorted(links)))
    broken = {u: s for u, s in results.items() if isinstance(s, int) and s in (404, 410)}
    unsure = {u: s for u, s in results.items() if u not in broken and not (isinstance(s, int) and 200 <= s < 300 and s != 202)}
    for title, group in (("BROKEN", broken), ("COULD NOT CHECK", unsure)):
        for u, s in sorted(group.items()):
            print(f"{title} ({s}): {u}\n    used in: {', '.join(sorted(links[u]))}")
    print(f"{len(links)} links: {len(broken)} broken, {len(unsure)} could not check")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
