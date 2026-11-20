"""Recompute V4 (Comprehensive Module) from the Gozo example, and unit-test linear_target_path."""
import pytest

from esgcalc import vsme
from test_examples_vsme import EXAMPLE, POINTS, page
from test_examples_vsme_basic import scope12

C = EXAMPLE["vsme_comprehensive"]


def test_v4_plan_covers_c1_to_c9() -> None:
    text = page("v4-comprehensive.md")
    assert [r["disclosure"] for r in C["plan"]] == [f"C{i}" for i in range(1, 10)]
    assert {r["disclosure"] for r in C["plan"]} == {p["disclosure"] for p in POINTS if p["module"] == "comprehensive"}
    for r in C["plan"]:
        row = f"| {r['disclosure']} | {r['what']} | {r['source']} | {r['ready_by']} |"
        assert row in text, r["disclosure"]


def test_v4_target_path() -> None:
    text = page("v4-comprehensive.md")
    t = C["target"]
    s1_lines, s2 = scope12()
    base = sum(s1_lines) + s2                                          # 1,800 from V2
    path = vsme.linear_target_path(base, t["base_year"], t["target_year"], t["reduction_share"])
    assert path[t["target_year"]] == pytest.approx(base * (1 - t["reduction_share"])) == pytest.approx(1260)
    step = base * t["reduction_share"] / (t["target_year"] - t["base_year"])
    assert step == pytest.approx(135)
    for year, value in path.items():
        label = f"{year} (base)" if year == t["base_year"] else f"{year} (target)" if year == t["target_year"] else str(year)
        assert f"| {label} | {value:,.0f} |" in text, year
    assert f"falls by {step:,.0f} tCO2e a year" in text
    assert f"{base:,.0f} × {1 - t['reduction_share']:.2f} = **{path[t['target_year']]:,.0f} tCO2e**" in text
    assert "# {2026: 1800.0, 2027: 1665.0, 2028: 1530.0, 2029: 1395.0, 2030: 1260.0}" in text


def test_v4_board() -> None:
    b = C["board"]
    assert b["women"] + b["men"] == b["members"]
    text = page("v4-comprehensive.md")
    assert b["members"] == 5 and "Five members" in text
    assert f"{b['women']} women and {b['men']} men ({b['women'] / b['members']:.0%} women)" in text


def test_linear_target_path_edges() -> None:
    assert vsme.linear_target_path(100, 2026, 2027, 0.5) == {2026: 100.0, 2027: 50.0}
    for args in ((0, 2026, 2030, 0.3), (100, 2030, 2030, 0.3), (100, 2026, 2030, 0), (100, 2026, 2030, 1)):
        with pytest.raises(ValueError):
            vsme.linear_target_path(*args)
