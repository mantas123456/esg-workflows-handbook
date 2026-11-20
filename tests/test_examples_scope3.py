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
