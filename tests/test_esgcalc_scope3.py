"""Tests for esgcalc.scope3 and esgcalc.quality. Expected values are worked out by hand."""
import math

import pytest

from esgcalc import quality, scope3
from esgcalc.quality import DataQuality
from esgcalc.scope3 import Line


# --- spend-based -------------------------------------------------------------

def test_spend_based_plain() -> None:
    # 10,000 EUR x 0.5 kg/EUR = 5,000 kg = 5.0 t
    assert scope3.spend_based(10_000, 0.5) == pytest.approx(5.0)


def test_spend_based_deflated_to_factor_year() -> None:
    # Spend in a year with index 120, factor priced in a year with index 100:
    # 10,000 x 100 / 120 = 8,333.33 EUR; x 0.5 = 4,166.67 kg = 4.16667 t
    t = scope3.spend_based(10_000, 0.5, price_index_spend_year=120, price_index_factor_year=100)
    assert t == pytest.approx(4.166_666_7)


def test_spend_based_other_currency() -> None:
    # Factor per USD, 1.10 USD per EUR: 10,000 EUR = 11,000 USD; x 0.4 = 4,400 kg = 4.4 t
    assert scope3.spend_based(10_000, 0.4, factor_currency_per_eur=1.10) == pytest.approx(4.4)


def test_spend_based_currency_and_inflation() -> None:
    # 10,000 x 1.10 = 11,000 USD; x 100/110 = 10,000 USD of factor year; x 0.4 = 4,000 kg = 4.0 t
    t = scope3.spend_based(10_000, 0.4, factor_currency_per_eur=1.10,
                           price_index_spend_year=110, price_index_factor_year=100)
    assert t == pytest.approx(4.0)


@pytest.mark.parametrize("kwargs", [
    {"spend_eur": -1},
    {"factor_kgco2e_per_currency_unit": -0.1},
    {"factor_currency_per_eur": 0},
    {"price_index_spend_year": 110},                                   # one index only
    {"price_index_spend_year": 0, "price_index_factor_year": 100},
])
def test_spend_based_rejects_bad_input(kwargs: dict) -> None:
    args = {"spend_eur": 10_000, "factor_kgco2e_per_currency_unit": 0.5} | kwargs
    with pytest.raises(ValueError):
        scope3.spend_based(**args)


# --- average-data and supplier-specific -------------------------------------

def test_average_data() -> None:
    # 1,250 MWh x 300 kg/MWh = 375,000 kg = 375 t
    assert scope3.average_data(1_250, 300) == pytest.approx(375.0)


def test_supplier_specific_allocation() -> None:
    # Supplier emits 10,000 t for 100,000 t of output; we bought 400 t: 10,000 x 400 / 100,000 = 40 t
    assert scope3.supplier_specific(10_000, 400, 100_000) == pytest.approx(40.0)


def test_supplier_specific_rejects_bad_input() -> None:
    with pytest.raises(ValueError):
        scope3.supplier_specific(10_000, 400, 0)
    with pytest.raises(ValueError):
        scope3.supplier_specific(10_000, 200_000, 100_000)      # bought more than produced
    with pytest.raises(ValueError):
        scope3.average_data(-1, 300)


# --- hybrid combination -------------------------------------------------------

def test_combine_per_category_and_method_mix() -> None:
    lines = [
        Line(1, "supplier_specific", 40.0, "steel bars, Installation A"),
        Line(1, "average_data", 375.0, "electricity-intensive inputs"),
        Line(1, "spend_based", 5.0, "office supplies"),
        Line(4, "average_data", 12.5, "inbound road freight"),
    ]
    totals = scope3.combine(lines)
    assert list(totals) == [1, 4]
    c1 = totals[1]
    # 40 + 375 + 5 = 420 t; supplier-specific share 40/420 = 9.52%; spend 5/420 = 1.19%
    assert c1.tco2e == pytest.approx(420.0)
    assert c1.lines == 3
    assert c1.share("supplier_specific") == pytest.approx(40 / 420)
    assert c1.share("spend_based") == pytest.approx(5 / 420)
    assert sum(c1.share(m) for m in scope3.METHODS) == pytest.approx(1.0)
    assert totals[4].share("supplier_specific") == 0.0


def test_line_rejects_bad_values() -> None:
    with pytest.raises(ValueError):
        Line(16, "average_data", 1.0)
    with pytest.raises(ValueError):
        Line(1, "guess", 1.0)          # type: ignore[arg-type]
    with pytest.raises(ValueError):
        Line(1, "average_data", -1.0)


# --- data quality -------------------------------------------------------------

def test_quality_score_equal_weights() -> None:
    # (1 + 2 + 1 + 2 + 1) / 5 = 1.4
    assert DataQuality(1, 2, 1, 2, 1).score() == pytest.approx(1.4)


def test_quality_score_weighted() -> None:
    # Reliability counts double: (3 + 3 + 4 + 3 + 2 x 4) / 6 = 21 / 6 = 3.5
    w = {"technology": 1, "time": 1, "geography": 1, "completeness": 1, "reliability": 2}
    assert DataQuality(3, 3, 4, 3, 4).score(w) == pytest.approx(3.5)


def test_category_score_is_emissions_weighted() -> None:
    # (40 x 1.4 + 375 x 3.4) / 415 = (56 + 1,275) / 415 = 3.2072
    s = quality.category_score([(40, DataQuality(1, 2, 1, 2, 1)), (375, DataQuality(3, 3, 4, 3, 4))])
    assert s == pytest.approx(1331 / 415)


@pytest.mark.parametrize("bad", [(0, 1, 1, 1, 1), (1, 6, 1, 1, 1), (1, 1, 2.5, 1, 1), (True, 1, 1, 1, 1)])
def test_quality_rejects_out_of_range(bad: tuple) -> None:
    with pytest.raises(ValueError):
        DataQuality(*bad)


def test_quality_bad_weights_and_empty_category() -> None:
    with pytest.raises(ValueError):
        DataQuality(1, 1, 1, 1, 1).score({"technology": 1})
    with pytest.raises(ValueError):
        quality.category_score([(0, DataQuality(1, 1, 1, 1, 1))])


# --- analytic uncertainty -----------------------------------------------------

def test_sum_uncertainty() -> None:
    # 100 +/-10% and 200 +/-20%: U = sqrt(10^2 + 40^2) = sqrt(1,700) = 41.231; 41.231 / 300 = 13.744%
    u = quality.sum_uncertainty([100, 200], [0.10, 0.20])
    assert u.value == 300
    assert u.u95_abs == pytest.approx(math.sqrt(1700))
    assert u.u95_rel == pytest.approx(0.137_437, rel=1e-5)


def test_sum_of_equal_independent_parts_shrinks_relative_uncertainty() -> None:
    # four equal parts at +/-20%: U = sqrt(4 x 20^2) = 40 on 400 -> 10%
    assert quality.sum_uncertainty([100] * 4, [0.2] * 4).u95_rel == pytest.approx(0.10)


def test_product_uncertainty() -> None:
    # activity +/-5%, factor +/-20%: sqrt(0.05^2 + 0.20^2) = 0.206155
    assert quality.product_uncertainty([0.05, 0.20]) == pytest.approx(0.206_155, rel=1e-5)


def test_uncertainty_rejects_bad_input() -> None:
    with pytest.raises(ValueError):
        quality.sum_uncertainty([100, 200], [0.1])
    with pytest.raises(ValueError):
        quality.product_uncertainty([-0.1])


# --- Monte Carlo ----------------------------------------------------------------

def test_monte_carlo_single_lognormal_matches_closed_form() -> None:
    # median 100, GSD 1.5: sigma = ln 1.5 = 0.405465
    # mean = 100 x exp(sigma^2 / 2) = 108.566
    # 2.5% = 100 x exp(-1.959964 x sigma) = 45.172; 97.5% = 100 x exp(+1.959964 x sigma) = 221.38
    r = quality.monte_carlo_sum([1.0], [100.0], [1.5], n=200_000)
    sigma = math.log(1.5)
    assert r.mean == pytest.approx(100 * math.exp(sigma ** 2 / 2), rel=0.01)
    assert r.median == pytest.approx(100, rel=0.01)
    assert r.low == pytest.approx(100 * math.exp(-1.959964 * sigma), rel=0.015)
    assert r.high == pytest.approx(100 * math.exp(1.959964 * sigma), rel=0.015)


def test_monte_carlo_without_uncertainty_is_exact() -> None:
    # GSD 1 means no spread: 1,250 x 0.3 + 400 x 0.652 = 375 + 260.8 = 635.8
    r = quality.monte_carlo_sum([1_250, 400], [0.3, 0.652], [1.0, 1.0], n=1_000)
    assert (r.low, r.median, r.high) == pytest.approx((635.8, 635.8, 635.8))


def test_monte_carlo_is_seeded() -> None:
    a = quality.monte_carlo_sum([10, 20], [2.0, 3.0], [1.3, 1.8], n=5_000, seed=7)
    b = quality.monte_carlo_sum([10, 20], [2.0, 3.0], [1.3, 1.8], n=5_000, seed=7)
    c = quality.monte_carlo_sum([10, 20], [2.0, 3.0], [1.3, 1.8], n=5_000, seed=8)
    assert a == b
    assert a.mean != c.mean


def test_monte_carlo_sum_is_narrower_than_its_parts() -> None:
    # Two independent equal terms: the total's relative 95% range is narrower than one term's.
    one = quality.monte_carlo_sum([1.0], [100.0], [1.5], n=50_000)
    two = quality.monte_carlo_sum([1.0, 1.0], [100.0, 100.0], [1.5, 1.5], n=50_000)
    assert (two.high - two.low) / two.median < (one.high - one.low) / one.median


@pytest.mark.parametrize("args", [
    ([], [], []),
    ([1.0], [100.0], [0.9]),          # GSD below 1
    ([1.0], [0.0], [1.5]),            # median not positive
    ([-1.0], [100.0], [1.5]),
    ([1.0, 2.0], [100.0], [1.5]),
])
def test_monte_carlo_rejects_bad_input(args: tuple) -> None:
    with pytest.raises(ValueError):
        quality.monte_carlo_sum(*args, n=1_000)


# --- organisational boundary ----------------------------------------------------

def test_boundary_three_approaches() -> None:
    from esgcalc.boundary import Entity, consolidate

    group = [Entity("A", 1000, 1.0, True, True), Entity("B", 500, 0.4, False, True), Entity("C", 200, 0.3, False, False)]
    # equity: 1000 + 0.4 x 500 + 0.3 x 200 = 1000 + 200 + 60 = 1260
    assert consolidate(group, "equity_share").tco2e == pytest.approx(1260)
    # financial control: only A = 1000; operational control: A + B = 1500
    fc, oc = consolidate(group, "financial_control"), consolidate(group, "operational_control")
    assert (fc.tco2e, fc.outside) == (1000, ["B", "C"])
    assert (oc.tco2e, oc.outside) == (1500, ["C"])


def test_boundary_rejects_bad_input() -> None:
    from esgcalc.boundary import Entity, consolidate

    with pytest.raises(ValueError):
        Entity("A", 100, 1.2, True, True)
    with pytest.raises(ValueError):
        Entity("A", -1, 1.0, True, True)
    with pytest.raises(ValueError):
        consolidate([Entity("A", 1, 1, True, True), Entity("A", 2, 1, True, True)], "equity_share")
    with pytest.raises(ValueError):
        consolidate([Entity("A", 1, 1, True, True)], "headcount")      # type: ignore[arg-type]


# --- screening -------------------------------------------------------------------

def test_screen_size_and_other_reasons() -> None:
    est = {c: 0.0 for c in range(1, 16)}
    est.update({1: 90.0, 2: 6.0, 4: 4.0})            # total 100
    rows = scope3.screen(est, 0.05, {4: "customer asked"})
    by = {r.category: r for r in rows}
    assert len(rows) == 15 and by[1].name == "Purchased goods and services"
    assert (by[1].share, by[2].share, by[4].share) == (0.9, 0.06, 0.04)
    assert by[2].significant_by_size and not by[4].significant_by_size     # 6% >= 5%, 4% < 5%
    assert by[4].significant and not by[3].significant


def test_screen_exactly_at_threshold_counts() -> None:
    est = {c: 0.0 for c in range(1, 16)}
    est.update({1: 98.0, 2: 2.0})                     # 2.0 / 100 = exactly 2%
    assert scope3.screen(est, 0.02)[1].significant_by_size


def test_screen_rejects_missing_categories_and_bad_threshold() -> None:
    with pytest.raises(ValueError, match="missing"):
        scope3.screen({1: 10.0}, 0.02)
    est = {c: 1.0 for c in range(1, 16)}
    for bad in (0, 1, -0.1):
        with pytest.raises(ValueError):
            scope3.screen(est, bad)
    with pytest.raises(ValueError):
        scope3.screen({c: 0.0 for c in range(1, 16)}, 0.02)


# --- supplier coverage --------------------------------------------------------------

def test_suppliers_to_cover() -> None:
    # 50 + 30 = 80 of 100 -> two suppliers reach exactly 80%
    c = scope3.suppliers_to_cover({"B": 30, "A": 50, "C": 20}, 0.80)
    assert (c.suppliers, c.share) == (["A", "B"], 0.8)
    assert scope3.suppliers_to_cover({"A": 50, "B": 30, "C": 20}, 1.0).suppliers == ["A", "B", "C"]


def test_suppliers_to_cover_rejects_bad_input() -> None:
    for bad in (0, 1.1):
        with pytest.raises(ValueError):
            scope3.suppliers_to_cover({"A": 1}, bad)
    with pytest.raises(ValueError):
        scope3.suppliers_to_cover({"A": 0}, 0.8)
    with pytest.raises(ValueError):
        scope3.suppliers_to_cover({"A": -1}, 0.8)
