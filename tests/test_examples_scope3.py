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
    assert grand == pytest.approx(5775.09322, abs=1e-5)
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
    assert totals[15].tco2e == pytest.approx(75)
    assert "(90 tCO2e, 30% of the cold store's emissions)" in text and "Gozo's 25% stake (75 tCO2e)" in text
