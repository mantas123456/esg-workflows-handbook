"""Recompute every number in the Scope 3 worked examples (S1-S9, F2) with esgcalc.

The fictional data lives in data/examples/gozo_fresh_foods.yml.
"""
from pathlib import Path

import pytest
import yaml

from esgcalc.boundary import APPROACHES, Entity, consolidate

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = yaml.safe_load((ROOT / "data/examples/gozo_fresh_foods.yml").read_text(encoding="utf-8"))
REGS = {r["id"]: r for r in yaml.safe_load((ROOT / "data/regulations.yml").read_text(encoding="utf-8"))}


def page(name: str, folder: str = "scope3") -> str:
    """Page text with whitespace collapsed, so table cells and wrapped lines match."""
    return " ".join((ROOT / "docs" / folder / name).read_text(encoding="utf-8").split())


def fmt(x: float) -> str:
    x = round(float(x), 6)
    return f"{x:,.0f}" if x.is_integer() else f"{x:,}"


def yes(flag: bool) -> str:
    return "Yes" if flag else "No"


# --- S1 Boundary -----------------------------------------------------------

def test_s1_group_table() -> None:
    text = page("s1-boundary.md")
    for e in EXAMPLE["entities"]:
        row = (f"| {e['name']} | {fmt(e['scope12_tco2e'])} | {e['equity_share']:.0%} | "
               f"{yes(e['financial_control'])} | {yes(e['operational_control'])} |")
        assert row in text, row


def test_s1_three_approaches() -> None:
    text = page("s1-boundary.md")
    entities = [Entity(**e) for e in EXAMPLE["entities"]]
    results = {a: consolidate(entities, a) for a in APPROACHES}
    # equity 1,200 + 240 + 100 + 75 = 1,615; financial control 1,600; operational control 1,800
    assert {a: r.tco2e for a, r in results.items()} == {
        "equity_share": 1615, "financial_control": 1600, "operational_control": 1800}
    for e in entities:
        cells = " | ".join(fmt(results[a].by_entity[e.name]) for a in APPROACHES)
        assert f"| {e.name} | {cells} |" in text, e.name
    totals = " | ".join(f"**{fmt(results[a].tco2e)}**" for a in APPROACHES)
    assert f"| **Scope 1 and 2 inside the boundary** | {totals} |" in text
    assert "= 1,200 + 240 + 100 + 75 = 1,615 tCO2e" in text
    assert "# equity_share 1615.0 / financial_control 1600.0 / operational_control 1800.0" in text

    chosen = results[EXAMPLE["chosen_approach"]]
    assert f"**operational control**: {fmt(chosen.tco2e)} tCO2e in Scope 1 and 2" in text
    assert chosen.outside == ["Island Cold Store Ltd (associate)"]
    assert "Island Cold Store is outside the boundary" in text


def test_s1_value_chain_cap_applies() -> None:
    text = page("s1-boundary.md")
    employees = EXAMPLE["company"]["employees"]
    assert employees <= REGS["csrd-value-chain-cap"]["values"]["max_employees"]
    assert f"**{employees} employees**" in text and f"has {employees} employees, so the CSRD value-chain cap applies" in text


# --- S2 Screening ----------------------------------------------------------

def _line_tco2e(line: dict) -> float:
    from esgcalc import scope3

    if line["method"] == "spend_based":
        return scope3.spend_based(line["spend_eur"], line["factor"])
    if line["method"] == "average_data":
        return scope3.average_data(line["activity"], line["factor"])
    return scope3.supplier_specific(line["supplier_total_tco2e"], line["purchased"], line["total"])


def screening_rows():
    from esgcalc.scope3 import screen

    s = EXAMPLE["screening"]
    estimates = {c: 0.0 for c in range(1, 16)}
    for line in s["lines"]:
        estimates[line["category"]] += _line_tco2e(line)
    return screen(estimates, s["size_threshold_share"], {int(k): v for k, v in s["other_reasons"].items()})


def test_s2_every_line_of_the_calculation_table() -> None:
    text = page("s2-screening.md")
    for line in EXAMPLE["screening"]["lines"]:
        t = _line_tco2e(line)
        if line["method"] == "spend_based":
            calc = f"EUR {fmt(line['spend_eur'])} × {line['factor']} kg/EUR"
        elif line["method"] == "average_data":
            calc = f"{fmt(line['activity'])} {line['unit']} × {line['factor']} kg/{line['unit']}"
        else:
            calc = f"{fmt(line['supplier_total_tco2e'])} t × {line['purchased']} / {line['total']}"
        row = f"| {line['category']} | {line['description']} | {calc} | {fmt(t)} |"
        assert row in text, row


def test_s2_screening_table_matches_esgcalc() -> None:
    text = page("s2-screening.md")
    s = EXAMPLE["screening"]
    rows = screening_rows()
    assert len(rows) == 15
    for r in rows:
        reason = (s["not_applicable"].get(r.category) or r.other_reason
                  or ("Size: above 2%" if r.significant_by_size else "Below 2%, no other reason"))
        row = (f"| {r.category} | {r.name} | {fmt(r.tco2e)} | {r.share:.2%} | "
               f"{'Yes' if r.significant else 'No'} | {reason} |")
        assert row in text, row
    total = sum(r.tco2e for r in rows)
    significant = [r for r in rows if r.significant]
    covered = sum(r.tco2e for r in significant)
    # 6,375 + 160 + 180 + 180 + 157.08 + 126 + 195 = 7,373.08 of 7,489.08 = 98.45%
    assert [r.category for r in significant] == [1, 2, 3, 4, 7, 9, 12]
    assert (round(total, 6), round(covered, 6)) == (7489.08, 7373.08)
    assert f"| **Total screened** | **{fmt(total)}** | **100%** |" in text
    assert f"**{len(significant)} significant categories** (1, 2, 3, 4, 7, 9 and 12) cover **{fmt(covered)} tCO2e**, or **{covered / total:.2%}**" in text
    assert "# [1, 2, 3, 4, 7, 9, 12]" in text


def test_s2_category_9_is_significant_for_another_reason() -> None:
    nine = screening_rows()[8]
    assert nine.category == 9 and not nine.significant_by_size and nine.significant


def test_s2_every_zero_category_has_a_reason() -> None:
    zero = {r.category for r in screening_rows() if r.tco2e == 0}
    assert zero == set(EXAMPLE["screening"]["not_applicable"]) == {8, 10, 11, 13, 14}


# --- S3 Data collection plan -------------------------------------------------

def test_s3_supplier_coverage_table() -> None:
    from esgcalc.scope3 import suppliers_to_cover

    text = page("s3-data-plan.md")
    spend = EXAMPLE["ingredient_spend_by_supplier"]
    total = sum(spend.values())
    assert total == 6_000_000
    running = 0.0
    for name, s in spend.items():
        running += s
        assert f"| {name} | {fmt(s)} | {s / total:.2%} | {running / total:.2%} |" in text, name
    c = suppliers_to_cover(spend, EXAMPLE["supplier_target_share"])
    # 30 + 20 + 15 + 11.67 = 76.67% < 80%; adding the 5th gives 85%
    assert len(c.suppliers) == 5 and c.share == pytest.approx(0.85)
    assert f"**top {len(c.suppliers)} suppliers cover {c.share:.2%}**" in text
    rest = total - sum(spend[n] for n in c.suppliers)
    assert f"other EUR {fmt(rest)}" in text
    assert "# 5 0.85" in text


def test_s3_plan_covers_exactly_the_significant_categories() -> None:
    from datetime import datetime

    import test_examples_scope3 as me

    text = page("s3-data-plan.md")
    significant = [r.category for r in me.screening_rows() if r.significant]
    plan = EXAMPLE["data_plan"]
    assert [r["category"] for r in plan] == significant
    assert f"found {len(significant)} significant categories" in text
    deadline = EXAMPLE["inventory_deadline"]
    for r in plan:
        row = (f"| {r['category']} | {r['data']} | {r['screening']} | {r['target']} | "
               f"{r['owner']} | {r['source']} | {r['ready_by']} |")
        assert row in text, r["category"]
        ready = datetime.strptime(r["ready_by"], "%d %b %Y").date()
        assert (deadline - ready).days >= 28, r["category"]      # "at least four weeks"
    assert f"inventory by {deadline.day} {deadline:%B %Y}" in text


# --- S4 Calculation methods --------------------------------------------------

def _inventory_tco2e(line: dict) -> float:
    from esgcalc import scope3

    inv = EXAMPLE["inventory"]
    if line["method"] == "spend_based":
        return scope3.spend_based(line["spend_eur"], line["factor"],
                                  price_index_spend_year=inv["price_index_spend_year"],
                                  price_index_factor_year=inv["price_index_factor_year"])
    return _line_tco2e(line)


def inventory_totals():
    """The 2026 inventory per category (esgcalc.scope3.combine), as in S4."""
    from esgcalc.scope3 import Line, combine

    inv = EXAMPLE["inventory"]
    lines = [Line(l["category"], l["method"], _inventory_tco2e(l), l["description"]) for l in inv["lines"]]
    for cat in inv["kept_from_screening"]:
        for l in EXAMPLE["screening"]["lines"]:
            if l["category"] == cat:
                lines.append(Line(cat, l["method"], _line_tco2e(l), l["description"]))
    return combine(lines)


def test_s4_category_1_lines() -> None:
    text = page("s4-methods.md")
    inv = EXAMPLE["inventory"]
    method_name = {"supplier_specific": "Supplier-specific", "average_data": "Average-data", "spend_based": "Spend-based"}
    for l in [x for x in inv["lines"] if x["category"] == 1]:
        if l["method"] == "supplier_specific":
            calc = f"{fmt(l['supplier_total_tco2e'])} t × {fmt(l['purchased'])} / {fmt(l['total'])}"
        elif l["method"] == "spend_based":
            calc = (f"EUR {fmt(l['spend_eur'])} × {inv['price_index_factor_year']}/{inv['price_index_spend_year']}"
                    f" × {l['factor']} kg/EUR")
        else:
            calc = f"{fmt(l['activity'])} {l['unit']} × {l['factor']} kg/{l['unit']}"
        row = f"| {l['description']} | {method_name[l['method']]} | {calc} | {_inventory_tco2e(l):,.2f} |"
        assert row in text, row
    # 3,220 supplier + 750 spend (885,000 / 1.18 kg) + 875 packaging = 4,845
    category_1 = inventory_totals()[1].tco2e
    assert category_1 == pytest.approx(4845.0)
    assert f"| **Category 1** | | | **{category_1:,.2f}** |" in text


def test_s4_all_categories_and_method_mix() -> None:
    from esgcalc.scope3 import CATEGORY_NAMES, METHODS

    text = page("s4-methods.md")
    totals = inventory_totals()
    assert sorted(totals) == [1, 2, 3, 4, 5, 6, 7, 9, 12, 15]
    for c, ct in totals.items():
        shares = " | ".join(f"{ct.share(m):.2%}" for m in METHODS)
        row = f"| {c} | {CATEGORY_NAMES[c]} | {ct.tco2e:,.2f} | {shares} |"
        assert row in text, row
    grand = sum(ct.tco2e for ct in totals.values())
    by_method = {m: sum(ct.by_method.get(m, 0.0) for ct in totals.values()) for m in METHODS}
    assert grand == pytest.approx(5752.59322, abs=1e-5)
    mix = " | ".join(f"**{by_method[m] / grand:.2%}**" for m in METHODS)
    assert f"| | **Total Scope 3** | **{grand:,.2f}** | {mix} |" in text


def test_s4_comparison_with_screening() -> None:
    text = page("s4-methods.md")
    totals = inventory_totals()
    screened = {r.category: r.tco2e for r in screening_rows()}
    for c in (1, 2, 4, 7, 9, 12):
        assert f"| {c} | {screened[c]:,.2f} | {totals[c].tco2e:,.2f} |" in text, c
    assert f"screening ({sum(screened.values()):,.2f} tCO2e)" in text
    top5 = [l for l in EXAMPLE["inventory"]["lines"] if l["method"] == "supplier_specific" and l["category"] == 1]
    own = sum(_inventory_tco2e(l) for l in top5)
    spend_top5 = sum(EXAMPLE["ingredient_spend_by_supplier"][l["description"]] for l in top5)
    assert (own, spend_top5) == (3220, 5_100_000)
    assert f"own data gives {fmt(own)} tCO2e" in text
    assert f"EUR {fmt(spend_top5)} of spend at 0.9 kg/EUR, without deflation, gave {fmt(spend_top5 * 0.9 / 1000)} tCO2e" in text
    # the five supplier lines replace exactly that spend; the remaining spend line is the rest of the 6,000,000
    rest = next(l for l in EXAMPLE["inventory"]["lines"] if l["description"] == "Other ingredient suppliers")
    assert rest["spend_eur"] == 6_000_000 - spend_top5


def test_s4_island_cold_store_overlap() -> None:
    text = page("s4-methods.md")
    totals = inventory_totals()
    assert totals[4].by_method["supplier_specific"] == pytest.approx(90)
    # GHG-1: the stake covers only the emissions not already in category 4
    cold_store_total = 300
    assert totals[15].tco2e == pytest.approx(0.25 * (cold_store_total - totals[4].by_method["supplier_specific"])) == pytest.approx(52.5)
    assert "(90 tCO2e, 30% of the cold store's emissions)" in text
    assert "25% x (300 - 90) = **52.50 tCO2e**" in text and "22.50 tCO2e of the storage would have been" in text
    assert "| 15 | 75.00 | 52.50 | Storage already in category 4 left out |" in text


# --- S5 Choosing emission factors --------------------------------------------

FACTOR_SOURCES = yaml.safe_load((ROOT / "data/factor_sources.yml").read_text(encoding="utf-8"))["sources"]


def _options():
    from esgcalc.factors import FactorOption
    from esgcalc.quality import DataQuality

    return [FactorOption(o["name"], o["source_id"], o["version"], o["year"], o["unit"],
                         DataQuality(**o["quality"]), o["licence_allows_use"])
            for o in EXAMPLE["factor_choice"]["options"]]


def test_s5_options_table_and_choice() -> None:
    from esgcalc.factors import choose_factor

    text = page("s5-emission-factors.md")
    sources = {s["id"]: s for s in FACTOR_SOURCES}
    label = {"ecoinvent": "ecoinvent", "desnz-2026": "DESNZ 2026", "exiobase-3": "EXIOBASE 3.11.2"}
    for raw, o in zip(EXAMPLE["factor_choice"]["options"], _options()):
        assert o.source_id in sources
        q = raw["quality"]
        scores = ", ".join(str(q[k]) for k in ("technology", "time", "geography", "completeness", "reliability"))
        allowed = ("Yes: " if o.licence_allows_use else "No: ") + raw["why"]
        row = f"| {o.name} | {label[o.source_id]} | {scores} | {o.quality.score():.1f} | {allowed} |"
        assert row in text, row
    chosen = choose_factor(_options())
    assert chosen.source_id == "desnz-2026"
    assert f"Gozo chooses the **{chosen.name}**" in text
    assert "# DESNZ 2026" in text


def test_s5_licence_flags_agree_with_factor_sources() -> None:
    # An option counts as usable only if its source may be used by a company: never for
    # ecoinvent (no licence held) or EXIOBASE 3.9+ (non-commercial); DESNZ is OGL v3.0.
    sources = {s["id"]: s for s in FACTOR_SOURCES}
    for o in _options():
        if o.licence_allows_use:
            assert sources[o.source_id]["licence_status"] == "verified"
            assert sources[o.source_id]["republish"] == "yes"
    assert "non-commercial" in sources["exiobase-3"]["licence"]


def test_s5_factor_register_covers_every_line() -> None:
    text = page("s5-emission-factors.md")
    register = EXAMPLE["factor_register"]
    lines = [l["description"] for l in EXAMPLE["inventory"]["lines"] if l["method"] != "supplier_specific"]
    assert sorted(register) == sorted(lines)
    ids = {s["id"] for s in FACTOR_SOURCES} | {"to-choose"}
    shown = {"desnz-2026": "DESNZ 2026", "to-choose": "To choose"}
    for line, source in register.items():
        assert source in ids
        assert f"| {line} | {shown[source]} |" in text, line
    done = sum(1 for s in register.values() if s != "to-choose")
    assert (done, len(register) - done) == (13, 4)
    assert f"**{done}** of the {len(register)} lines" in text and f"The **{len(register) - done}** spend-" in text


def test_s5_generated_source_table_matches_factor_sources() -> None:
    import importlib.util
    import sys

    spec = importlib.util.spec_from_file_location("build_pages", ROOT / "scripts/build_pages.py")
    bp = importlib.util.module_from_spec(spec)
    sys.modules["build_pages"] = bp
    spec.loader.exec_module(bp)
    raw = (ROOT / "docs/scope3/s5-emission-factors.md").read_text(encoding="utf-8")
    table = bp.render_factor_sources({"sources": FACTOR_SOURCES})
    assert f"{bp.FACTORS_START}\n{table}\n{bp.FACTORS_END}" in raw


# --- F2 Data quality and uncertainty -------------------------------------------

def _f2_budget():
    """Category 1 lines with value, stated u95, data-quality score, from the data and S4's inventory."""
    from esgcalc import quality
    from esgcalc.quality import DataQuality

    inventory = {l["description"]: _inventory_tco2e(l) for l in EXAMPLE["inventory"]["lines"] if l["category"] == 1}
    rows = []
    for l in EXAMPLE["uncertainty_category_1"]["lines"]:
        u = l["u95"] if "u95" in l else quality.product_uncertainty([l["activity_u95"], l["factor_u95"]])
        rows.append({"line": l, "value": inventory[l["description"]], "u95": u, "quality": DataQuality(*l["quality"])})
    return rows


def test_f2_budget_rows() -> None:
    from esgcalc import quality

    text = page("data-quality.md", "foundations")
    rows = _f2_budget()
    # every category 1 line of S4 has exactly one budget row
    assert sorted(r["line"]["description"] for r in rows) == sorted(
        l["description"] for l in EXAMPLE["inventory"]["lines"] if l["category"] == 1)
    shares = quality.variance_shares([r["value"] for r in rows], [r["u95"] for r in rows])
    for r, share in zip(rows, shares):
        expected = (f"| {r['line']['description']} | {r['value']:,.2f} | {r['line']['basis']} | "
                    f"{r['quality'].score():.1f} | {r['u95']:.1%} | {r['value'] * r['u95']:,.2f} | {share:.1%} |")
        assert expected in text, expected
    assert max(shares) == shares[5] and f"{shares[5]:.1%}" == "71.7%"
    assert f"contributes **{shares[5]:.1%}** of the variance" in text


def test_f2_combined_and_reported_result() -> None:
    from esgcalc import quality

    text = page("data-quality.md", "foundations")
    rows = _f2_budget()
    total = quality.sum_uncertainty([r["value"] for r in rows], [r["u95"] for r in rows])
    score = quality.category_score([(r["value"], r["quality"]) for r in rows])
    # sqrt(90^2 + 120^2 + 75^2 + 63^2 + 40^2 + 343.22^2 + 31.78^2 + 65.97^2 + 77.31^2 + 37.11^2) = 405.23
    assert total.value == pytest.approx(4845.0) and total.u95_abs == pytest.approx(405.228, abs=1e-3)
    assert (f"| **Category 1** | **{total.value:,.2f}** | | **{score:.2f}** | **{total.u95_rel:.1%}** | "
            f"**{total.u95_abs:,.2f}** | **100%** |") in text
    assert f"weighted by emissions, is **{score:.2f}**" in text
    assert (f"{total.value:,.2f} ± {total.u95_abs:,.2f} tCO2e, an interval of "
            f"{total.value - total.u95_abs:,.2f} to {total.value + total.u95_abs:,.2f} tCO2e") in text
    v, u = quality.round_result(total.value, total.u95_abs)
    assert (v, u) == (4850.0, 410.0)
    assert f"**{v:,.0f} ± {u:,.0f} tCO2e (95%)**" in text
    assert f"√(0.05² + 0.20²) = {quality.product_uncertainty([0.05, 0.20]):.1%}" in text


def test_f2_monte_carlo_table() -> None:
    from esgcalc import quality

    text = page("data-quality.md", "foundations")
    rows = _f2_budget()
    mc_set = EXAMPLE["uncertainty_category_1"]["monte_carlo"]
    values = [r["value"] for r in rows]
    mc = quality.monte_carlo_sum(values, [1.0] * len(values), [quality.gsd_from_u95(r["u95"]) for r in rows],
                                 n=mc_set["n"], seed=mc_set["seed"])
    total = quality.sum_uncertainty(values, [r["u95"] for r in rows])
    assert f"{mc_set['n']:,} draws, seed {mc_set['seed']}" in text
    assert f"| Central value | {total.value:,.1f} | {mc.median:,.1f} (median) |" in text
    assert (f"| 95% interval | {total.value - total.u95_abs:,.1f} to {total.value + total.u95_abs:,.1f} | "
            f"{mc.low:,.1f} to {mc.high:,.1f} |") in text
    # the asymmetry the page describes: the lower end moves up, the upper end stays close
    assert mc.low > total.value - total.u95_abs
    assert mc.high == pytest.approx(total.value + total.u95_abs, rel=0.005)


def test_f2_python_snippet_output() -> None:
    from esgcalc import quality

    text = page("data-quality.md", "foundations")
    values = [900, 1200, 500, 420, 200, 686.44, 63.56, 320, 375, 180]
    u95 = [0.10, 0.10, 0.15, 0.15, 0.20, 0.50, 0.50, 0.2062, 0.2062, 0.2062]
    total = quality.sum_uncertainty(values, u95)
    assert quality.round_result(total.value, total.u95_abs) == (4850.0, 410.0)
    assert round(quality.variance_shares(values, u95)[5], 3) == 0.717
    assert "# (4850.0, 410.0)" in text and "# 0.717" in text



def test_s4_supplier_boundaries() -> None:
    """GHG-4: the page says what each supplier's figure covers and how it is allocated."""
    text = page("s4-methods.md")
    for a in EXAMPLE["supplier_answers"]:
        row = f"| {a['supplier']} | {a['covers']} | {a['allocated_by']} | {yes(a['verified'])} |"
        assert row in text, row
    partial = [a for a in EXAMPLE["supplier_answers"] if not a["covers"].startswith("Cradle to gate")]
    assert [a["supplier"] for a in partial] == ["Mediterranean Oils"]
    q = {l["description"]: l for l in EXAMPLE["uncertainty_category_1"]["lines"]}["Mediterranean Oils"]
    assert q["quality"][3] == 3 and q["u95"] == 0.20                    # completeness scored lower, wider uncertainty


def test_s2_s4_land_and_biogenic_notes() -> None:
    regs = {r["id"]: r for r in yaml.safe_load((ROOT / "data/regulations.yml").read_text(encoding="utf-8"))}
    assert "takes effect on 1 January 2027" in regs["ghgp-land-sector"]["fact"]
    assert "takes effect on 1 January 2027" in page("s2-screening.md")
    assert "**Keep biogenic CO2 separate.**" in page("s4-methods.md")
    assert "reported separately for each category" in regs["ghgp-scope3-reporting"]["fact"]
    assert "Many companies use a control approach" not in page("s1-boundary.md")



def test_f2_correlation_check_and_other_seeds() -> None:
    """GHG-6 and GHG-7: the fully correlated packaging bound, and the Monte Carlo upper end with other seeds."""
    import math
    from esgcalc import quality
    text = page("data-quality.md", "foundations")
    rows = _f2_budget()
    U = [r["value"] * r["u95"] for r in rows]
    pack = [u for r, u in zip(rows, U) if "packaging" in r["line"]["description"] or "jars" in r["line"]["description"]]
    assert len(pack) == 3
    independent = math.sqrt(sum(u * u for u in U))
    pack_ind, pack_cor = math.sqrt(sum(u * u for u in pack)), sum(pack)
    correlated = math.sqrt(independent ** 2 - pack_ind ** 2 + pack_cor ** 2)
    assert f"±{pack_ind:,.2f}" in text and f"= ±{pack_cor:,.2f}" in text
    assert f"from ±{independent:,.2f} to **±{correlated:,.2f}" in text
    v, u = quality.round_result(4845.0, correlated)
    assert f"**{v:,.0f} ± {u:,.0f} tCO2e**" in text
    values = [r["value"] for r in rows]
    gsds = [quality.gsd_from_u95(r["u95"]) for r in rows]
    for seed in (1, 2):
        high = quality.monte_carlo_sum(values, [1.0] * len(values), gsds, n=200_000, seed=seed).high
        assert 5_250 <= high <= 5_252, (seed, high)
    assert "stays between 5,250 and 5,252 tCO2e" in text
