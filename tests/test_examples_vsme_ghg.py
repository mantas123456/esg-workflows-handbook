"""Recompute V3 (GHG emissions for VSME) from the V2 data and the S9 inventory."""
import pytest

from esgcalc import quality, vsme
from test_examples_scope3_report import category_summary
from test_examples_vsme import EXAMPLE, page
from test_examples_vsme_basic import scope12


def test_v3_emissions_table() -> None:
    text = page("v3-ghg.md")
    s1_lines, s2 = scope12()
    s1 = sum(s1_lines)
    s3 = sum(s["tco2e"] for s in category_summary().values())          # the S9 inventory total
    total = s1 + s2 + s3
    assert (s1, s2, round(s3, 2)) == (600.0, 1200.0, 5775.09)
    for name, value, status in (("Scope 1", s1, "Required"), ("Scope 2 (location-based)", s2, "Required"),
                                ("Scope 3", s3, "Added voluntarily")):
        assert f"| {name} | {value:,.2f} | {value / total:.2%} | {status} |" in text, name
    assert f"| **Total** | **{total:,.2f}** | **100%** | | |" in text
    assert "three-quarters of the total" in text and 0.70 < s3 / total < 0.80
    assert "less than a quarter" in text and (s1 + s2) / total < 0.25


def test_v3_intensity_and_same_figures() -> None:
    text = page("v3-ghg.md")
    s1_lines, s2 = scope12()
    intensity = vsme.ghg_intensity(sum(s1_lines) + s2, EXAMPLE["vsme_basic"]["turnover_eur"])
    assert f"{sum(s1_lines) + s2:,.0f} tCO2e / EUR {EXAMPLE['vsme_basic']['turnover_eur']:,} = **{intensity:,.2f} tCO2e per EUR million**" in text
    # the Scope 3 figure sent to the supermarket is S9's rounded result
    summary = category_summary()
    total = quality.sum_uncertainty([s["tco2e"] for s in summary.values()], [s["u95_rel"] for s in summary.values()])
    v, u = quality.round_result(total.value, total.u95_abs)
    assert f"{v:,.0f} ± {u:,.0f} tCO2e" in text


def test_v3_python_snippet() -> None:
    text = page("v3-ghg.md")
    assert round(5775.09 / (600 + 1200 + 5775.09), 4) == 0.7624
    assert round(vsme.ghg_intensity(1800, 14_000_000), 2) == pytest.approx(128.57)
    assert "# 0.7624" in text and "# 128.57" in text
