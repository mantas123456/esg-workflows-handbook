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
