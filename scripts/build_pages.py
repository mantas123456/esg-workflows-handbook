"""Generate Planned pages, the workflow map and the mkdocs nav from data/workflows.yml.

Existing pages are never overwritten. Run before `mkdocs build`.
"""
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DATA = yaml.safe_load((ROOT / "data" / "workflows.yml").read_text(encoding="utf-8"))

PLACEHOLDER = """---
step: "{id}"
status: planned
---

# {id} {title}

!!! note "Planned for version {release}"
    This page is not written yet. See the [roadmap](../roadmap.md).
"""

NAV_START = "# --- generated nav: do not edit by hand ---"
NAV_END = "# --- end generated nav ---"


def main() -> None:
    map_rows = ["# Workflow map", "",
                "Every step in the handbook. Generated from `data/workflows.yml`.", "",
                "| Step | Track | Page | Release | Status |", "|---|---|---|---|---|"]
    nav = ["nav:", "  - Home: index.md"]
    for track in DATA["tracks"]:
        nav.append(f"  - {track['title']}:")
        if track["id"] == "start":
            nav += ["      - Workflow map: workflow-map.md", "      - Roadmap: roadmap.md"]
        for step in track["steps"]:
            rel = f"{track['folder']}/{step['file']}"
            page = DOCS / rel
            if not page.exists():
                page.parent.mkdir(parents=True, exist_ok=True)
                page.write_text(PLACEHOLDER.format(**step), encoding="utf-8")
            nav.append(f"      - \"{step['id']} {step['title']}\": {rel}")
            map_rows.append(f"| {step['id']} | {track['title']} | [{step['title']}]({rel}) "
                            f"| {step['release']} | {step['status']} |")
    nav += ["  - Reference:", "      - Glossary: glossary.md", "      - About: about.md"]
    (DOCS / "workflow-map.md").write_text("\n".join(map_rows) + "\n", encoding="utf-8")

    cfg = ROOT / "mkdocs.yml"
    text = cfg.read_text(encoding="utf-8")
    head, _, rest = text.partition(NAV_START)
    _, _, tail = rest.partition(NAV_END)
    cfg.write_text(f"{head}{NAV_START}\n" + "\n".join(nav) + f"\n{NAV_END}{tail}", encoding="utf-8")


if __name__ == "__main__":
    main()
