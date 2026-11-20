"""Generate Planned pages, the workflow map and the mkdocs nav from data/workflows.yml,
and the reuse-map table in F3 from data/datasets.yml.

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

DATASETS_PAGE = DOCS / "foundations" / "one-dataset-many-reports.md"
DATASETS_START = "<!-- generated from data/datasets.yml: do not edit by hand -->"
DATASETS_END = "<!-- end generated datasets -->"


def render_datasets(datasets: dict) -> str:
    """Render data/datasets.yml as one Markdown table (the reuse map)."""
    reports: dict[str, str] = datasets["reports"]
    rows = ["| Dataset | Unit | Owner | Frequency | " + " | ".join(reports.values()) + " | Notes |",
            "|---|---|---|---|" + "---|" * len(reports) + "---|"]
    for d in datasets["datasets"]:
        unknown = set(d["used_by"]) - set(reports)
        if unknown:
            raise ValueError(f"{d['name']}: unknown report(s) in used_by: {sorted(unknown)}")
        marks = " | ".join("✓" if key in d["used_by"] else "" for key in reports)
        rows.append(f"| **{d['title']}** (`{d['name']}`) | {d['unit']} | {d['owner_role']} "
                    f"| {d['frequency']} | {marks} | {d['note']} |")
    return "\n".join(rows)


def write_datasets_section() -> None:
    """Replace the generated block in the F3 page, if the page has the markers."""
    if not DATASETS_PAGE.exists():
        return
    text = DATASETS_PAGE.read_text(encoding="utf-8")
    if DATASETS_START not in text:
        return
    datasets = yaml.safe_load((ROOT / "data" / "datasets.yml").read_text(encoding="utf-8"))
    head, _, rest = text.partition(DATASETS_START)
    _, _, tail = rest.partition(DATASETS_END)
    DATASETS_PAGE.write_text(f"{head}{DATASETS_START}\n{render_datasets(datasets)}\n{DATASETS_END}{tail}",
                             encoding="utf-8")


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
    nav += ["  - Reference:", "      - Glossary: glossary.md", "      - Changelog: changelog.md",
            "      - About: about.md"]
    (DOCS / "workflow-map.md").write_text("\n".join(map_rows) + "\n", encoding="utf-8")

    cfg = ROOT / "mkdocs.yml"
    text = cfg.read_text(encoding="utf-8")
    head, _, rest = text.partition(NAV_START)
    _, _, tail = rest.partition(NAV_END)
    cfg.write_text(f"{head}{NAV_START}\n" + "\n".join(nav) + f"\n{NAV_END}{tail}", encoding="utf-8")
    write_datasets_section()


if __name__ == "__main__":
    main()
