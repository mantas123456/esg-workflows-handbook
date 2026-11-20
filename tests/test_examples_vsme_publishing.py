"""Recompute V6 (publishing and restating) from the Gozo example."""
import pytest

from esgcalc import scope3, vsme
from test_examples_scope3 import _inventory_tco2e, fmt
from test_examples_scope3_report import category_summary
from test_examples_vsme import EXAMPLE, page
from test_examples_vsme_basic import scope12

P = EXAMPLE["publication"]


def _d(d) -> str:
    return f"{d.day} {d:%b %Y}"


def test_v6_calendar() -> None:
    text = page("v6-publishing.md")
    dates = [c["date"] for c in P["calendar"]]
    assert dates == sorted(dates)
    for c in P["calendar"]:
        assert f"| {_d(c['date'])} | {c['step']} |" in text, c["step"]
    margin = (P["deadline"] - dates[-1]).days
    assert margin == 10 and f"Published **{margin} days** before the deadline" in text
    assert P["deadline"] == EXAMPLE["inventory_deadline"]                 # the supermarket's deadline from S3
    assert f"by **{P['deadline'].day} {P['deadline']:%B %Y}**" in text


def _restated():
    s1_lines, s2 = scope12()
    published_12 = sum(s1_lines) + s2
    acquired = next(e for e in EXAMPLE["entities"] if e["name"] == P["restatement_2027"]["acquired_entity"])
    restated_12 = published_12 + acquired["scope12_tco2e"]                  # now 100% inside the boundary
    base3 = sum(s["tco2e"] for s in category_summary().values())
    other = next(l for l in EXAMPLE["inventory"]["lines"] if l["description"] == "Other ingredient suppliers")
    car = next(l for l in EXAMPLE["inventory"]["lines"] if l["description"] == "Commuting by car (staff survey)")
    ch = {c["kind"]: c for c in EXAMPLE["changes_2027"]}
    effects = (ch["Structural"]["tco2e"]
               + scope3.spend_based(other["spend_eur"], ch["Methodology"]["new_factor"],
                                    price_index_spend_year=118, price_index_factor_year=100) - _inventory_tco2e(other)
               + scope3.average_data(ch["Error"]["corrected_activity"], car["factor"]) - _inventory_tco2e(car))
    return published_12, restated_12, acquired["scope12_tco2e"], base3, base3 + effects


def test_v6_restatement_table() -> None:
    text = page("v6-publishing.md")
    p12, r12, cold, p3, r3 = _restated()
    assert (p12, r12, cold) == (1800, 2100, 300)
    assert round(r3, 2) == 5755.84                                          # as recalculated in S8
    assert f"| Scope 1 and 2 (tCO2e) | {p12:,.2f} | {r12:,.2f} | Island Cold Store's {cold} tCO2e now inside the boundary |" in text
    assert f"| Scope 3 (tCO2e) | {p3:,.2f} | {r3:,.2f} |" in text


def test_v6_rebased_target() -> None:
    text = page("v6-publishing.md")
    _, r12, *_ = _restated()
    t = EXAMPLE["vsme_comprehensive"]["target"]
    path = vsme.linear_target_path(r12, t["base_year"], t["target_year"], t["reduction_share"])
    old = vsme.linear_target_path(1800, t["base_year"], t["target_year"], t["reduction_share"])
    assert path[t["target_year"]] == pytest.approx(1470)
    assert f"{r12:,.0f} × {1 - t['reduction_share']:.2f} = **{path[t['target_year']]:,.0f} tCO2e** in 2030, instead of {old[t['target_year']]:,.0f}" in text
    for year, value in path.items():
        label = f"{year} (base)" if year == t["base_year"] else f"{year} (target)" if year == t["target_year"] else str(year)
        assert f"| {label} | {fmt(value)} |" in text, year
