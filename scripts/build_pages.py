"""Generate Planned pages, the workflow map and the mkdocs nav from data/workflows.yml,
the reuse-map table in F3 from data/datasets.yml, and the template download
links in each page whose step lists ``templates``.

Existing pages are never overwritten; only the marked generated blocks are
refreshed. Run before `mkdocs build`.
"""
import sys
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


TEMPLATES_START = "<!-- generated from data/workflows.yml templates: do not edit by hand -->"
TEMPLATES_END = "<!-- end generated templates -->"
FORMAT_NAMES = {"docx": "Word", "xlsx": "Excel"}


def render_templates(template_ids: list[str], catalog: dict[str, dict], depth: int) -> str:
    """Download links for a page ``depth`` folders below docs/."""
    prefix = "../" * depth + "downloads/"
    lines = []
    for tid in template_ids:
        if tid not in catalog:
            raise ValueError(f"template {tid!r} is listed in data/workflows.yml but has no source in templates/")
        t = catalog[tid]
        lines.append(f"- **[{t['title']}]({prefix}{tid}.{t['format']})** "
                     f"({FORMAT_NAMES[t['format']]}): {t['description']}")
    return "\n".join(lines)


def write_templates_sections() -> None:
    """Fill the generated download block in every page whose step lists templates."""
    sys.path.insert(0, str(ROOT / "scripts"))
    import build_templates

    catalog = {t["id"]: t for t in build_templates.catalog()}
    for track in DATA["tracks"]:
        for step in track["steps"]:
            page = DOCS / track["folder"] / step["file"]
            if not step.get("templates") or not page.exists():
                continue
            text = page.read_text(encoding="utf-8")
            if TEMPLATES_START not in text:
                continue
            head, _, rest = text.partition(TEMPLATES_START)
            _, _, tail = rest.partition(TEMPLATES_END)
            body = render_templates(step["templates"], catalog, depth=len(Path(track["folder"]).parts))
            new = f"{head}{TEMPLATES_START}\n{body}\n{TEMPLATES_END}{tail}"
            if new != text:
                page.write_text(new, encoding="utf-8")


CBAM_TOOL_PAGE = DOCS / "tools" / "cbam-calculator.md"
TOOL_START = "<!-- generated from data/cbam_parameters.yml and data/examples/melita_metals.yml: do not edit by hand -->"
TOOL_END = "<!-- end generated tool data -->"


def cbam_tool_data() -> dict:
    """Parameters and the Melita Metals example for the CBAM browser calculator."""
    from esgcalc.cbam import Precursor, embedded_emissions

    p = yaml.safe_load((ROOT / "data" / "cbam_parameters.yml").read_text(encoding="utf-8"))
    ex = yaml.safe_load((ROOT / "data" / "examples" / "melita_metals.yml").read_text(encoding="utf-8"))
    crude, bars = ex["installation_A_crude_steel_2026"], ex["installation_A_2026"]
    crude_see = embedded_emissions(
        sector="iron_steel", production_mass_t=crude["production_mass_t"], direct_tco2e=crude["direct_tco2e"],
        precursors=[Precursor(x["mass_t"], x["see_tco2e_per_t"]) for x in crude["precursors"]],
        imported_mass_t=0).see_tco2e_per_t
    bars_see = embedded_emissions(
        sector="iron_steel", production_mass_t=bars["production_mass_t"], direct_tco2e=bars["direct_tco2e"],
        indirect_tco2e=bars["indirect_tco2e"], precursors=[Precursor(bars["precursors"][0]["mass_t"], crude_see)],
        imported_mass_t=0).see_tco2e_per_t
    base = ex["default_values_base"]
    fa = ex["free_allocation_adjustment_tco2e_per_t"][2026]
    per_installation = {
        "A": {"sector": "iron_steel", "basis": "actual", "actual_see": round(bars_see, 6),
              "base_default": base["steel_bars_A"]["base_direct_see_tco2e_per_t"], "fa_per_t": fa["A"]},
        "B": {"sector": "aluminium", "basis": "default", "actual_see": None,
              "base_default": base["aluminium_bars_B"]["base_direct_see_tco2e_per_t"], "fa_per_t": fa["B"]},
    }
    lines = [{"quarter": l["quarter"], "cn_code": l["cn_code"], "mass_t": l["mass_t"], **per_installation[l["installation"]]}
             for l in ex["imports_2026"]]
    return {
        "params": {
            "max_exempt_mass_t": p["threshold"]["max_exempt_mass_t"],
            "excluded_cn_codes": {k.replace(" ", ""): v for k, v in p["threshold"]["excluded_cn_codes"].items()},
            "markup_by_year": {str(k): float(v) for k, v in p["default_value_markup_by_year"]["values"].items()},
            "sector_markup": {k: float(v) for k, v in p["default_value_markup_by_year"].get("sector_markup", {}).items()},
            "holding_min_share": p["quarterly_holding"]["min_share"],
            "holding_from_year": p["quarterly_holding"]["from_year"],
            "tco2e_per_certificate": p["certificate"]["tco2e_per_certificate"],
        },
        "example": {"year": 2026, "price_eur": ex["certificate_price_assumed_eur_per_tco2e"],
                    "carbon_price_paid_certificates": ex["carbon_price_paid"]["claimed_certificates"], "lines": lines},
    }


def write_cbam_tool_data() -> None:
    """Embed the calculator's parameters and example in its page as JSON."""
    import json

    if not CBAM_TOOL_PAGE.exists():
        return
    text = CBAM_TOOL_PAGE.read_text(encoding="utf-8")
    if TOOL_START not in text:
        return
    head, _, rest = text.partition(TOOL_START)
    _, _, tail = rest.partition(TOOL_END)
    payload = json.dumps(cbam_tool_data(), indent=1, sort_keys=True)
    new = f'{head}{TOOL_START}\n<script type="application/json" id="cbam-tool-data">\n{payload}\n</script>\n{TOOL_END}{tail}'
    if new != text:
        CBAM_TOOL_PAGE.write_text(new, encoding="utf-8")


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
    tools = sorted((DOCS / "tools").glob("*.md"))
    if tools:
        nav.append("  - Tools:")
        for tool in tools:
            title = next((l[2:].strip() for l in tool.read_text(encoding="utf-8").splitlines() if l.startswith("# ")),
                         tool.stem)
            nav.append(f"      - \"{title}\": tools/{tool.name}")
    nav += ["  - Reference:", "      - Glossary: glossary.md", "      - Changelog: changelog.md",
            "      - About: about.md"]
    (DOCS / "workflow-map.md").write_text("\n".join(map_rows) + "\n", encoding="utf-8")

    cfg = ROOT / "mkdocs.yml"
    text = cfg.read_text(encoding="utf-8")
    head, _, rest = text.partition(NAV_START)
    _, _, tail = rest.partition(NAV_END)
    cfg.write_text(f"{head}{NAV_START}\n" + "\n".join(nav) + f"\n{NAV_END}{tail}", encoding="utf-8")
    write_datasets_section()
    write_templates_sections()
    write_cbam_tool_data()


if __name__ == "__main__":
    main()
