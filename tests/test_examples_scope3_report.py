"""Recompute the numbers on S6-S9 (scores, supplier engagement, base year, inventory report).

Builds on the helpers in test_examples_scope3.py, so S2-S9 and F2 all come from the
same data (data/examples/gozo_fresh_foods.yml) and the same esgcalc functions.
"""
import pytest
import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

from esgcalc import quality, scope3
from esgcalc.quality import DataQuality, category_score
from esgcalc.scope3 import CATEGORY_NAMES
from test_examples_scope3 import (EXAMPLE, _inventory_tco2e, _line_tco2e, fmt, inventory_totals, page,
                                  screening_rows)

METHOD_NAME = {"supplier_specific": "Supplier-specific", "average_data": "Average-data", "spend_based": "Spend-based"}


def all_lines() -> dict[int, list[dict]]:
    """Every 2026 inventory line by category: value (tCO2e), u95 and quality, as in S4, F2 and S6."""
    spec = {x["description"]: x for x in EXAMPLE["uncertainty_category_1"]["lines"] + EXAMPLE["line_quality"]}
    lines = [(l, _inventory_tco2e(l)) for l in EXAMPLE["inventory"]["lines"]]
    lines += [(l, _line_tco2e(l)) for l in EXAMPLE["screening"]["lines"]
              if l["category"] in EXAMPLE["inventory"]["kept_from_screening"]]
    assert sorted(spec) == sorted(l["description"] for l, _ in lines), "every line needs a score and a u95"
    out: dict[int, list[dict]] = {}
    for l, value in lines:
        s = spec[l["description"]]
        u = s["u95"] if "u95" in s else quality.product_uncertainty([s["activity_u95"], s["factor_u95"]])
        out.setdefault(l["category"], []).append({"description": l["description"], "method": l["method"],
                                                  "value": value, "u95": u, "quality": DataQuality(*s["quality"])})
    return dict(sorted(out.items()))


def category_summary() -> dict[int, dict]:
    summary = {}
    for cat, rows in all_lines().items():
        total = quality.sum_uncertainty([r["value"] for r in rows], [r["u95"] for r in rows])
        summary[cat] = {"tco2e": total.value, "u95_rel": total.u95_rel, "u95_abs": total.u95_abs,
                        "score": category_score([(r["value"], r["quality"]) for r in rows])}
    return summary


def significant() -> set[int]:
    return {r.category for r in screening_rows() if r.significant}


def inventory_score() -> float:
    return category_score([(r["value"], r["quality"]) for rows in all_lines().values() for r in rows])


# --- S6 Data quality scoring -------------------------------------------------

def test_s6_category_scores_and_target() -> None:
    text = page("s6-data-quality.md")
    summary = category_summary()
    sig = significant()
    target = EXAMPLE["quality_target"]
    for cat, s in summary.items():
        meets = ("Yes" if s["score"] <= target else "No") if cat in sig else "–"
        row = (f"| {cat} | {CATEGORY_NAMES[cat]} | {s['tco2e']:,.2f} | {s['score']:.2f} | "
               f"{'Yes' if cat in sig else 'No'} | {meets} |")
        assert row in text, row
    assert [c for c, s in summary.items() if c in sig and s["score"] > target] == [2, 9, 12]
    assert "miss the target: **2, 9 and 12**" in text
    total = sum(s["tco2e"] for s in summary.values())
    assert f"| | **Whole inventory** | **{total:,.2f}** | **{inventory_score():.2f}** | | |" in text
    assert f"inventory scores **{inventory_score():.2f}**" in text
    assert f"target of **{target}**" in text
    assert f"# {summary[12]['score']:.2f}" in text          # the Python snippet on the page


# --- S7 Supplier engagement --------------------------------------------------

def test_s7_answers_next_supplier_and_uncertainty() -> None:
    text = page("s7-suppliers.md")
    answers = EXAMPLE["supplier_answers"]
    cat1 = {r["description"]: r for r in all_lines()[1]}
    for a in answers:
        row = (f"| {a['supplier']} | {'Yes' if a['answered'] else 'No'} | {'Yes' if a['verified'] else 'No'} | "
               f"{cat1[a['supplier']]['value']:,.2f} |")
        assert row in text, row
    answered, verified = sum(a["answered"] for a in answers), sum(a["verified"] for a in answers)
    assert f"**{answered} of {len(answers)}** answered; **{verified}** of the figures were verified" in text

    nxt = scope3.suppliers_to_cover(EXAMPLE["ingredient_spend_by_supplier"], EXAMPLE["next_year_target_share"])
    new = EXAMPLE["next_supplier_estimate"]
    assert len(nxt.suppliers) == 6 and nxt.suppliers[-1] == new["supplier"]
    assert f"**{new['supplier']}**: the top {len(nxt.suppliers)} cover {nxt.share:.2%}" in text

    rows = all_lines()[1]
    before = quality.sum_uncertainty([r["value"] for r in rows], [r["u95"] for r in rows])
    other = next(l for l in EXAMPLE["inventory"]["lines"] if l["description"] == "Other ingredient suppliers")
    rest_spend = other["spend_eur"] - EXAMPLE["ingredient_spend_by_supplier"][new["supplier"]]
    rest_t = scope3.spend_based(rest_spend, other["factor"], price_index_spend_year=118, price_index_factor_year=100)
    values = [rest_t if r["description"] == "Other ingredient suppliers" else r["value"] for r in rows]
    after = quality.sum_uncertainty(values + [new["tco2e"]], [r["u95"] for r in rows] + [new["u95"]])
    assert (f"from EUR {fmt(other['spend_eur'])} to EUR {fmt(rest_spend)} "
            f"({_inventory_tco2e(other):,.2f} to {rest_t:,.2f} tCO2e)") in text
    assert f"| 2026, top 5 suppliers | {before.value:,.2f} | {before.u95_abs:,.2f} | {before.u95_rel:.2%} |" in text
    assert f"| With Spice Traders as well | {after.value:,.2f} | {after.u95_abs:,.2f} | {after.u95_rel:.2%} |" in text
    assert 0.18 < 1 - after.u95_abs / before.u95_abs < 0.25      # "about a fifth"


# --- S8 Base year and recalculation ---------------------------------------------

def test_s8_recalculation() -> None:
    text = page("s8-base-year.md")
    base = sum(s["tco2e"] for s in category_summary().values())
    other = next(l for l in EXAMPLE["inventory"]["lines"] if l["description"] == "Other ingredient suppliers")
    car = next(l for l in EXAMPLE["inventory"]["lines"] if l["description"] == "Commuting by car (staff survey)")
    ch = {c["kind"]: c for c in EXAMPLE["changes_2027"]}
    effects = {
        "Structural": ch["Structural"]["tco2e"],
        "Methodology": scope3.spend_based(other["spend_eur"], ch["Methodology"]["new_factor"],
                                          price_index_spend_year=118, price_index_factor_year=100)
        - _inventory_tco2e(other),
        "Error": scope3.average_data(ch["Error"]["corrected_activity"], car["factor"]) - _inventory_tco2e(car),
    }
    # the acquisition removes exactly the two Island Cold Store lines (category 4 service, category 15 equity)
    totals = inventory_totals()
    assert -effects["Structural"] == pytest.approx(totals[4].by_method["supplier_specific"] + totals[15].tco2e)
    threshold = EXAMPLE["recalculation_threshold_share"]
    check = scope3.check_recalculation(base, effects, threshold)
    for kind, c in ch.items():
        share = abs(effects[kind]) / base
        assert share < threshold, kind                                     # no change triggers it alone
        sign = "-" if effects[kind] < 0 else "+"
        row = f"| {c['name']} | {kind} | {c['effect']} | {sign}{abs(effects[kind]):,.2f} | {share:.2%} |"
        assert row in text, row
    assert check.recalculate
    assert f"| **Added up (absolute)** | | | **{check.cumulative_abs_tco2e:,.2f}** | **{check.share:.2%}** |" in text
    net = sum(effects.values())
    assert f"= **{base + net:,.2f} tCO2e**" in text
    sign = "+" if net > 0 else "−"
    assert f"{sign}{abs(net):,.2f} tCO2e ({abs(net) / base:.2%})" in text
    assert f"at **{base:,.2f} tCO2e** of Scope 3" in text
    assert f"# {round(check.share, 4)} True" in text and round(check.share, 4) == 0.0525


# --- S9 Reporting the inventory -------------------------------------------------

def test_s9_inventory_table_and_total() -> None:
    text = page("s9-reporting.md")
    summary = category_summary()
    totals = inventory_totals()
    sig = significant()
    for cat, s in summary.items():
        main = max(totals[cat].by_method.items(), key=lambda kv: kv[1])[0]
        row = (f"| {cat} | {CATEGORY_NAMES[cat]} | {s['tco2e']:,.2f} | {METHOD_NAME[main]} | {s['score']:.2f} | "
               f"{s['u95_rel']:.1%} | {'Yes' if cat in sig else 'No'} |")
        assert row in text, row
    total = quality.sum_uncertainty([s["tco2e"] for s in summary.values()], [s["u95_rel"] for s in summary.values()])
    assert (f"| | **Total Scope 3** | **{total.value:,.2f}** | | **{inventory_score():.2f}** | "
            f"**{total.u95_rel:.1%}** | |") in text
    v, u = quality.round_result(total.value, total.u95_abs)
    assert (v, u) == (5750.0, 420.0)
    assert f"**Reported total: {v:,.0f} ± {u:,.0f} tCO2e (95%).**" in text
    sig_total = sum(summary[c]["tco2e"] for c in sig)
    assert f"**{sig_total:,.2f} tCO2e**, {sig_total / total.value:.2%} of the total" in text
    assert sorted(EXAMPLE["screening"]["not_applicable"]) == [8, 10, 11, 13, 14]
    assert not set(EXAMPLE["screening"]["not_applicable"]) & set(summary)
    reg = list(EXAMPLE["factor_register"].values())
    assert f"for {reg.count('desnz-2026')} lines; {reg.count('to-choose')} lines" in text


def test_s9_method_mix_note_matches_s4() -> None:
    text = page("s9-reporting.md")
    totals = inventory_totals()
    grand = sum(t.tco2e for t in totals.values())
    mix = {m: sum(t.by_method.get(m, 0.0) for t in totals.values()) / grand for m in scope3.METHODS}
    assert (f"{mix['supplier_specific']:.2%} supplier-specific, {mix['average_data']:.2%} average-data, "
            f"{mix['spend_based']:.2%}") in text


def test_s9_python_snippet() -> None:
    text = page("s9-reporting.md")
    categories = [4845.00, 135.59, 180.00, 175.00, 31.00, 10.00, 117.00, 114.00, 92.50, 52.50]
    u95 = [0.0836, 0.50, 0.1498, 0.1332, 0.4147, 0.50, 0.2203, 0.3095, 0.4083, 0.15]
    # the snippet's rounded inputs are the category results of S9's table
    summary = category_summary()
    assert [round(v["tco2e"], 2) for v in summary.values()] == categories
    assert [round(v["u95_rel"], 4) for v in summary.values()] == u95
    total = quality.sum_uncertainty(categories, u95)
    assert quality.round_result(total.value, total.u95_abs) == (5750.0, 420.0)
    assert "# (5750.0, 420.0)" in text


# --- esgcalc.scope3.check_recalculation ------------------------------------------

def test_check_recalculation_adds_absolute_changes() -> None:
    # +30 and -30 on 1,000: net 0, but |30| + |30| = 60 = 6% >= 5% -> recalculate
    c = scope3.check_recalculation(1000, {"a": 30, "b": -30}, 0.05)
    assert (c.cumulative_abs_tco2e, c.share, c.recalculate) == (60, 0.06, True)
    assert not scope3.check_recalculation(1000, {"a": 49}, 0.05).recalculate      # 4.9%
    assert scope3.check_recalculation(1000, {"a": 50}, 0.05).recalculate          # exactly 5%
    with pytest.raises(ValueError):
        scope3.check_recalculation(0, {"a": 1}, 0.05)
    with pytest.raises(ValueError):
        scope3.check_recalculation(1000, {"a": 1}, 1.5)



def test_s9_provisional_gwp_and_biogenic_notes() -> None:
    """GHG-2, GHG-3, GHG-5: the S9 notes name the GWP basis, biogenic CO2 and the placeholder share."""
    from test_examples_scope3 import _inventory_tco2e
    text = page("s9-reporting.md")
    register = EXAMPLE["factor_register"]
    placeholders = [l for l in EXAMPLE["inventory"]["lines"] if register.get(l["description"]) == "to-choose"]
    ph = sum(_inventory_tco2e(l) for l in placeholders)
    total = sum(s["tco2e"] for s in category_summary().values())
    assert len(placeholders) == 4
    assert f"**{ph:,.2f} tCO2e ({ph / total:.1%})**" in text
    regs = {r["id"]: r for r in yaml.safe_load((ROOT / "data/regulations.yml").read_text(encoding="utf-8"))}
    assert "AR5: CH4 28, N2O 265" in regs["desnz-2026-gwp"]["fact"]
    assert "(AR5:\n    methane 28, nitrous oxide 265)".replace("\n    ", " ") in text
    assert "12. **Biogenic CO2:**" in text
