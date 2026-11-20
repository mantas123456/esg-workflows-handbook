"""Generate Planned pages, the workflow map and the mkdocs nav from data/workflows.yml,
the reuse-map table in F3 from data/datasets.yml, and the template download
links in each page whose step lists ``templates``.

Existing pages are never overwritten; only the marked generated blocks are
refreshed. Run before `mkdocs build`.
"""
import re
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


def write_json_block(page: Path, element_id: str, payload: dict) -> None:
    """Embed ``payload`` as a JSON script in a tool page, between its generated-data markers."""
    import json

    start = f"<!-- generated tool data: {element_id}: do not edit by hand -->"
    end = f"<!-- end generated tool data: {element_id} -->"
    if not page.exists():
        return
    text = page.read_text(encoding="utf-8")
    if start not in text:
        return
    head, _, rest = text.partition(start)
    _, _, tail = rest.partition(end)
    body = json.dumps(payload, indent=1, sort_keys=True, ensure_ascii=False)
    new = f'{head}{start}\n<script type="application/json" id="{element_id}">\n{body}\n</script>\n{end}{tail}'
    if new != text:
        page.write_text(new, encoding="utf-8")


def _gozo() -> dict:
    return yaml.safe_load((ROOT / "data" / "examples" / "gozo_fresh_foods.yml").read_text(encoding="utf-8"))


def _gozo_line_tco2e(line: dict, deflate: dict | None = None) -> float:
    from esgcalc import scope3

    if line["method"] == "spend_based":
        kw = ({"price_index_spend_year": deflate["price_index_spend_year"],
               "price_index_factor_year": deflate["price_index_factor_year"]} if deflate else {})
        return scope3.spend_based(line["spend_eur"], line["factor"], **kw)
    if line["method"] == "average_data":
        return scope3.average_data(line["activity"], line["factor"])
    return scope3.supplier_specific(line["supplier_total_tco2e"], line["purchased"], line["total"])


def screening_tool_data() -> dict:
    """Category names and the Gozo Fresh Foods screening (S2) for the screening tool."""
    from esgcalc.scope3 import CATEGORY_NAMES

    s = _gozo()["screening"]
    estimates = {c: 0.0 for c in CATEGORY_NAMES}
    for line in s["lines"]:
        estimates[line["category"]] += _gozo_line_tco2e(line)
    return {"categories": {str(c): n for c, n in CATEGORY_NAMES.items()},
            "example": {"threshold_share": s["size_threshold_share"],
                        "estimates": {str(c): round(v, 6) for c, v in estimates.items()},
                        "reasons": {str(c): r for c, r in s["other_reasons"].items()}}}


def uncertainty_tool_data() -> dict:
    """Gozo Fresh Foods' category 1 lines with their stated uncertainty (F2) for the demo."""
    from esgcalc import quality

    g = _gozo()
    inv = g["inventory"]
    values = {l["description"]: _gozo_line_tco2e(l, inv) for l in inv["lines"] if l["category"] == 1}
    lines = []
    for l in g["uncertainty_category_1"]["lines"]:
        u = l["u95"] if "u95" in l else quality.product_uncertainty([l["activity_u95"], l["factor_u95"]])
        lines.append({"name": l["description"], "value": round(values[l["description"]], 6), "u95": round(u, 6)})
    mc = g["uncertainty_category_1"]["monte_carlo"]
    return {"example": {"lines": lines, "draws": 100000, "seed": mc["seed"]}}


VSME_START = re.compile(r"<!-- generated from data/vsme_datapoints.yml: (?P<filter>[^>]*?) -->")
VSME_END = "<!-- end generated vsme datapoints -->"
BASIS_TEXT = {"act": "2026 act", "rec-2025": "2025 Recommendation", "title": "Topic only"}


def render_vsme_datapoints(points: list[dict], filter_text: str) -> str:
    """A table of VSME datapoints. ``filter_text`` is ``module=basic``, ``module=comprehensive``,
    ``disclosures=B3,B8`` or ``all``."""
    key, _, value = filter_text.partition("=")
    if key == "module":
        chosen = [p for p in points if p["module"] == value]
    elif key == "disclosures":
        wanted = value.split(",")
        chosen = [p for p in points if p["disclosure"] in wanted]
    elif key == "all":
        chosen = list(points)
    else:
        raise ValueError(f"unknown VSME table filter {filter_text!r}")
    if not chosen:
        raise ValueError(f"VSME table filter {filter_text!r} matches no datapoint")
    rows = ["| Datapoint | What it covers | Unit | Dataset | Checked against |", "|---|---|---|---|---|"]
    for p in chosen:
        dataset = f"`{p['dataset']}`" if p["dataset"] else "–"
        rows.append(f"| {p['id']} | {p['description']} | {p['unit']} | {dataset} | {BASIS_TEXT[p['basis']]} |")
    return "\n".join(rows)


def write_vsme_tables() -> None:
    """Fill every generated VSME datapoint table in the VSME pages."""
    points = yaml.safe_load((ROOT / "data" / "vsme_datapoints.yml").read_text(encoding="utf-8"))["datapoints"]
    for page in sorted((DOCS / "vsme").glob("*.md")):
        text = page.read_text(encoding="utf-8")
        out, pos = [], 0
        for m in VSME_START.finditer(text):
            if m.start() < pos:
                continue
            end = text.index(VSME_END, m.end())
            out.append(text[pos:m.end()])
            out.append("\n" + render_vsme_datapoints(points, m.group("filter").strip()) + "\n")
            pos = end
        if out:
            new = "".join(out) + text[pos:]
            if new != text:
                page.write_text(new, encoding="utf-8")


def vsme_readiness_tool_data() -> dict:
    """VSME datapoints, disclosure topics and Gozo Fresh Foods' status for the readiness tool."""
    d = yaml.safe_load((ROOT / "data" / "vsme_datapoints.yml").read_text(encoding="utf-8"))
    g = _gozo()
    done = [k for k, v in g["vsme_status"].items() if v[3] in ("Collected", "Not applicable")]
    done += g["vsme_comprehensive_done"]
    return {
        "datapoints": [{k: p[k] for k in ("id", "module", "disclosure", "description")} for p in d["datapoints"]],
        "topics": {x["disclosure"]: x["topic"] for x in d["disclosures"]},
        "example": {"option": g["vsme"]["option"], "done": done},
    }


def _mlg() -> dict:
    return yaml.safe_load((ROOT / "data" / "examples" / "mediterranean_logistics.yml").read_text(encoding="utf-8"))


def _esrs() -> dict:
    return yaml.safe_load((ROOT / "data" / "esrs_datapoints.yml").read_text(encoding="utf-8"))


IRO_KEYS = ("id", "topic", "description", "kind", "actual", "human_rights", "scale", "scope",
            "irremediability", "likelihood", "magnitude")


def _mlg_iros() -> list[dict]:
    """Mediterranean Logistics Group's items in esgcalc.dma.IRO form (all impacts negative)."""
    return [{**{k: i.get(k) for k in IRO_KEYS}, "negative": True,
             "actual": bool(i.get("actual", False)), "human_rights": bool(i.get("human_rights", False))}
            for i in _mlg()["dma"]["iros"]]


def dma_scoring_tool_data() -> dict:
    """DMA parameters, the topical standards and the Mediterranean Logistics Group example."""
    p = yaml.safe_load((ROOT / "data" / "dma_parameters.yml").read_text(encoding="utf-8"))
    return {
        "params": {"scale": {"min": p["scale"]["min"], "max": p["scale"]["max"]},
                   "severity_aggregation": p["severity_aggregation"],
                   "human_rights": {"severity_precedence_from": p["human_rights"]["severity_precedence_from"]},
                   "thresholds": {"impact": p["thresholds"]["impact"], "financial": p["thresholds"]["financial"]}},
        "standards": [s for s in _esrs()["standards"] if s["kind"] == "topical"],
        "example": _mlg_iros(),
    }


def esrs_gap_tool_data() -> dict:
    """ESRS key datapoints, the standards, and the group's material topics and statuses."""
    from esgcalc.dma import IRO, assess_all, topics

    d = _esrs()
    material = [t.topic for t in topics(assess_all(IRO(**i) for i in _mlg_iros())) if t.material]
    return {
        "datapoints": [{k: x[k] for k in ("id", "standard", "description", "dataset")} for x in d["datapoints"]],
        "standards": d["standards"],
        "example": {"material": material, "status": _mlg()["gap_status"]},
    }


FACTORS_PAGE = DOCS / "scope3" / "s5-emission-factors.md"
FACTORS_START = "<!-- generated from data/factor_sources.yml: do not edit by hand -->"
FACTORS_END = "<!-- end generated factor sources -->"
REPUBLISH_TEXT = {"yes": "Yes, with attribution", "no": "No: link and cite only", "check": "Not yet: licence to check"}
METHOD_TEXT = {"spend_based": "Spend-based", "average_data": "Average-data", "supplier_specific": "Supplier-specific"}


def render_factor_sources(data: dict) -> str:
    rows = ["| Source | Version | Coverage | Method | Licence | Values copied in this handbook? |",
            "|---|---|---|---|---|---|"]
    for s in data["sources"]:
        rows.append(f"| [{s['name']}]({s['url']}) ({s['publisher']}) | {s['version']} | {s['coverage']} | "
                    f"{METHOD_TEXT[s['method']]} | {s['licence']} | {REPUBLISH_TEXT[s['republish']]} |")
    return "\n".join(rows)


def write_factor_sources_section() -> None:
    """Replace the generated factor-source table in S5, if the page has the markers."""
    if not FACTORS_PAGE.exists():
        return
    text = FACTORS_PAGE.read_text(encoding="utf-8")
    if FACTORS_START not in text:
        return
    data = yaml.safe_load((ROOT / "data" / "factor_sources.yml").read_text(encoding="utf-8"))
    head, _, rest = text.partition(FACTORS_START)
    _, _, tail = rest.partition(FACTORS_END)
    new = f"{head}{FACTORS_START}\n{render_factor_sources(data)}\n{FACTORS_END}{tail}"
    if new != text:
        FACTORS_PAGE.write_text(new, encoding="utf-8")


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
    write_factor_sources_section()
    write_vsme_tables()
    write_json_block(DOCS / "tools" / "scope3-screening.md", "scope3-screening-data", screening_tool_data())
    write_json_block(DOCS / "tools" / "uncertainty-demo.md", "uncertainty-demo-data", uncertainty_tool_data())
    write_json_block(DOCS / "tools" / "vsme-readiness.md", "vsme-readiness-data", vsme_readiness_tool_data())
    write_json_block(DOCS / "tools" / "dma-scoring.md", "dma-scoring-data", dma_scoring_tool_data())
    write_json_block(DOCS / "tools" / "esrs-gap.md", "esrs-gap-data", esrs_gap_tool_data())


if __name__ == "__main__":
    main()
