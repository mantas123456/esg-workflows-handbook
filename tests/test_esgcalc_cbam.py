"""Tests for esgcalc.cbam. Expected values are worked out by hand in the comments."""
from decimal import Decimal
from pathlib import Path

import pytest
import yaml

from esgcalc import cbam
from esgcalc.cbam import Precursor

ROOT = Path(__file__).resolve().parents[1]
REGS = {r["id"]: r for r in yaml.safe_load((ROOT / "data/regulations.yml").read_text(encoding="utf-8"))}
P = cbam.load_parameters()


# --- parameters stay in step with data/regulations.yml ---------------------

def test_parameters_match_regulation_facts() -> None:
    assert P["threshold"]["max_exempt_mass_t"] == REGS["cbam-threshold"]["values"]["max_exempt_mass_t"]
    assert P["quarterly_holding"]["min_share"] == REGS["cbam-quarterly-holding"]["values"]["min_share"]
    assert P["quarterly_holding"]["from_year"] == REGS["cbam-quarterly-holding"]["values"]["from_year"]
    assert P["certificate"]["tco2e_per_certificate"] == REGS["cbam-certificate-unit"]["values"]["tco2e_per_certificate"]
    assert P["cbam_factor_by_year"]["values"] == REGS["cbam-free-allocation-adjustment"]["values"]["cbam_factor_by_year"]
    assert P["default_value_markup_by_year"]["values"] == REGS["cbam-default-values"]["values"]["markup_by_year"]
    assert P["default_value_markup_by_year"]["sector_markup"]["fertilisers"] == REGS["cbam-default-values"]["values"]["fertilisers_markup"]
    for block in ("threshold", "sectors", "certificate", "quarterly_holding"):
        assert P[block]["fact"] in REGS, block


# --- threshold_check --------------------------------------------------------

def test_threshold_below() -> None:
    # 30 + 15 = 45 t, not above 50 t
    r = cbam.threshold_check([("7208 51 20", 30.0), ("7601 10 00", 15.0)])
    assert r.total_mass_t == 45.0
    assert r.threshold_t == 50.0
    assert r.above_threshold is False
    assert r.excluded_cn_codes == []


def test_threshold_exactly_50_t_is_not_above() -> None:
    # "does not cumulatively exceed" 50 t -> exactly 50 t is still exempt
    assert cbam.threshold_check([("72142000", 50.0)]).above_threshold is False


def test_threshold_exactly_50_t_from_many_lines() -> None:
    # 45 x 1.1 + 0.5 = 49.5 + 0.5 = 50.0 t exactly, so not above.
    # A binary float sum (sum or math.fsum) gives 50.00000000000001 here.
    lines = [("7214 20 00", 1.1)] * 45 + [("7214 20 00", 0.5)]
    r = cbam.threshold_check(lines)
    assert r.total_mass_t == 50.0
    assert r.above_threshold is False


def test_threshold_just_above() -> None:
    # 50.001 t > 50 t
    assert cbam.threshold_check([("7214 20 00", 50.001)]).above_threshold is True


def test_threshold_400_t() -> None:
    # Melita Metals: 400 t of steel bars
    r = cbam.threshold_check([("7214 20 00", 250.0), ("7214 99 10", 150.0)])
    assert (r.total_mass_t, r.above_threshold) == (400.0, True)


def test_hydrogen_and_electricity_not_counted_but_flagged() -> None:
    # 2 t hydrogen + 10 t steel: only steel counts (10 t); hydrogen is flagged
    r = cbam.threshold_check([("2804 10 00", 2.0), ("7214 20 00", 10.0), ("2716 00 00", 500.0)])
    assert r.total_mass_t == 10.0
    assert r.above_threshold is False
    assert r.excluded_cn_codes == ["27160000", "28041000"]
    assert any("electricity, hydrogen" in n for n in r.notes)


def test_threshold_note_always_present() -> None:
    assert "no threshold" in cbam.threshold_check([]).notes[0]


@pytest.mark.parametrize("bad", [("72AB", 1.0), ("7214", -1.0), ("7214", float("nan"))])
def test_threshold_rejects_bad_input(bad: tuple[str, float]) -> None:
    with pytest.raises(ValueError):
        cbam.threshold_check([bad])


# --- embedded_emissions -----------------------------------------------------

def test_cement_counts_indirect() -> None:
    # (800 + 50) / 1000 = 0.85 tCO2e/t; 200 t x 0.85 = 170 tCO2e
    e = cbam.embedded_emissions(sector="cement", production_mass_t=1000, direct_tco2e=800,
                                indirect_tco2e=50, imported_mass_t=200)
    assert e.see_tco2e_per_t == pytest.approx(0.85)
    assert e.total_tco2e == pytest.approx(170.0)
    assert e.indirect_included is True


def test_steel_ignores_indirect_and_adds_precursors() -> None:
    # Annex II: indirect 100 ignored. Precursor 900 t x 1.8 = 1620.
    # (400 + 1620) / 1000 = 2.02 tCO2e/t; 400 t x 2.02 = 808 tCO2e
    e = cbam.embedded_emissions(sector="iron_steel", production_mass_t=1000, direct_tco2e=400,
                                indirect_tco2e=100, precursors=[Precursor(900, 1.8)], imported_mass_t=400)
    assert e.see_tco2e_per_t == pytest.approx(2.02)
    assert e.total_tco2e == pytest.approx(808.0)
    assert e.indirect_included is False


def test_zero_precursors() -> None:
    # 400 / 1000 = 0.4 tCO2e/t; 400 t x 0.4 = 160 tCO2e
    e = cbam.embedded_emissions(sector="iron_steel", production_mass_t=1000, direct_tco2e=400,
                                precursors=[], imported_mass_t=400)
    assert e.see_tco2e_per_t == pytest.approx(0.4)
    assert e.total_tco2e == pytest.approx(160.0)


def test_two_precursors_fertiliser() -> None:
    # 500 + 20 + (300 x 2.0) + (100 x 0.5) = 1170; / 1000 = 1.17; x 50 t = 58.5
    e = cbam.embedded_emissions(sector="fertilisers", production_mass_t=1000, direct_tco2e=500,
                                indirect_tco2e=20, precursors=[Precursor(300, 2.0), Precursor(100, 0.5)],
                                imported_mass_t=50)
    assert e.see_tco2e_per_t == pytest.approx(1.17)
    assert e.total_tco2e == pytest.approx(58.5)


def test_zero_imported_mass() -> None:
    e = cbam.embedded_emissions(sector="aluminium", production_mass_t=10, direct_tco2e=20, imported_mass_t=0)
    assert (e.see_tco2e_per_t, e.total_tco2e) == (2.0, 0.0)


@pytest.mark.parametrize("kwargs", [
    {"sector": "electricity"},
    {"sector": "plastics"},
    {"sector": "fact"},
    {"production_mass_t": 0},
    {"direct_tco2e": -1},
])
def test_embedded_emissions_rejects_bad_input(kwargs: dict) -> None:
    args = {"sector": "cement", "production_mass_t": 100, "direct_tco2e": 10, "imported_mass_t": 1} | kwargs
    with pytest.raises(ValueError):
        cbam.embedded_emissions(**args)


# --- certificates_needed ----------------------------------------------------

def test_certificates_with_both_reductions() -> None:
    # 808 - 700 - 50 = 58 certificates
    assert cbam.certificates_needed(808, 700, 50) == pytest.approx(58.0)


def test_certificates_no_reductions() -> None:
    assert cbam.certificates_needed(170) == 170.0


def test_carbon_price_paid_above_liability_gives_zero() -> None:
    # 100 - 60 - 80 = -40 -> 0, never negative
    assert cbam.certificates_needed(100, 60, 80) == 0.0


def test_certificates_rejects_negative() -> None:
    with pytest.raises(ValueError):
        cbam.certificates_needed(100, -1, 0)


# --- certificate_cost -------------------------------------------------------

def test_cost_to_the_cent() -> None:
    # 58 x 75.36 = 4350 + 20.88 = 4370.88 EUR
    assert cbam.certificate_cost(58, 75.36) == Decimal("4370.88")


def test_cost_rounds_half_up() -> None:
    # 0.5 x 0.01 = 0.005 -> 0.01; 3 x 33.335 = 100.005 -> 100.01
    assert cbam.certificate_cost(0.5, 0.01) == Decimal("0.01")
    assert cbam.certificate_cost(3, "33.335") == Decimal("100.01")


def test_cost_zero_and_negative() -> None:
    assert cbam.certificate_cost(0, 82.32) == Decimal("0.00")
    with pytest.raises(ValueError):
        cbam.certificate_cost(-1, 80)


# --- quarterly_holding ------------------------------------------------------

def test_quarterly_holding_2027() -> None:
    # 50% x (400 - 300) = 50 certificates
    assert cbam.quarterly_holding(400, 2027, 300) == pytest.approx(50.0)


def test_quarterly_holding_without_adjustment() -> None:
    # 50% x 808 = 404
    assert cbam.quarterly_holding(808, 2028) == pytest.approx(404.0)


def test_quarterly_holding_not_before_2027() -> None:
    assert cbam.quarterly_holding(808, 2026) == 0.0


def test_quarterly_holding_adjustment_above_emissions() -> None:
    assert cbam.quarterly_holding(100, 2027, 150) == 0.0


def test_quarterly_holding_rejects_negative() -> None:
    with pytest.raises(ValueError):
        cbam.quarterly_holding(-1, 2027)


# --- authorisation ----------------------------------------------------------

def test_decision_deadline() -> None:
    from datetime import date
    # 1 Feb + 120 days = 1 Jun; with 30-day extension = 1 Jul
    assert cbam.authorisation_decision_deadline(date(2026, 2, 1)) == date(2026, 6, 1)
    assert cbam.authorisation_decision_deadline(date(2026, 2, 1), 30) == date(2026, 7, 1)


@pytest.mark.parametrize("bad", [-1, 31])
def test_decision_deadline_rejects_bad_extension(bad: int) -> None:
    from datetime import date
    with pytest.raises(ValueError):
        cbam.authorisation_decision_deadline(date(2026, 2, 1), bad)


def test_transitional_rule_edges() -> None:
    from datetime import date
    assert cbam.may_import_pending_decision(date(2026, 3, 31), 2026) is True   # last day counts
    assert cbam.may_import_pending_decision(date(2026, 4, 1), 2026) is False
    assert cbam.may_import_pending_decision(date(2026, 3, 1), 2027) is False   # 2026 imports only


# --- default_value_with_markup ----------------------------------------------

@pytest.mark.parametrize("year, expected", [
    (2026, 2.2),   # 2.0 x 1.10
    (2027, 2.4),   # 2.0 x 1.20
    (2028, 2.6),   # 2.0 x 1.30
    (2035, 2.6),   # 30% stays from 2028 onwards
])
def test_markup_by_year(year: int, expected: float) -> None:
    assert cbam.default_value_with_markup(2.0, year, "aluminium") == pytest.approx(expected)


def test_fertilisers_markup_is_one_percent_every_year() -> None:
    # 2.0 x 1.01 = 2.02, in 2026 and in 2030
    assert cbam.default_value_with_markup(2.0, 2026, "fertilisers") == pytest.approx(2.02)
    assert cbam.default_value_with_markup(2.0, 2030, "fertilisers") == pytest.approx(2.02)


def test_markup_rejects_bad_input() -> None:
    with pytest.raises(ValueError):
        cbam.default_value_with_markup(2.0, 2025, "aluminium")
    with pytest.raises(ValueError):
        cbam.default_value_with_markup(-1.0, 2026, "aluminium")
