"""Recompute the T1 triage worked examples against the thresholds in data/regulations.yml."""
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PAGE = " ".join((ROOT / "docs/start-here/triage.md").read_text(encoding="utf-8").split())
REGS = {r["id"]: r for r in yaml.safe_load((ROOT / "data/regulations.yml").read_text(encoding="utf-8"))}


def cbam_exemption_met(mass_t: float, max_exempt_mass_t: float) -> bool:
    return mass_t <= max_exempt_mass_t


def test_thresholds_match_page() -> None:
    assert REGS["cbam-threshold"]["values"]["max_exempt_mass_t"] == 50
    assert REGS["csrd-scope"]["values"]["min_employees_exclusive"] == 1000
    assert REGS["csrd-value-chain-cap"]["values"]["max_employees"] == 1000
    assert "50 tonnes or less" in PAGE
    assert "more than 1,000 employees and more than EUR 450 m" in PAGE


def test_gozo_forge_30_t_meets_exemption() -> None:
    limit = REGS["cbam-threshold"]["values"]["max_exempt_mass_t"]
    assert "about 30 tonnes net mass" in PAGE
    assert cbam_exemption_met(30, limit)
    assert "exemption test is met" in PAGE


def test_melita_metals_400_t_exceeds_threshold() -> None:
    limit = REGS["cbam-threshold"]["values"]["max_exempt_mass_t"]
    assert "about 400 tonnes" in PAGE
    assert not cbam_exemption_met(400, limit)
    assert "exemption test is not met" in PAGE


def test_marsa_packaging_120_employees() -> None:
    employees = 120
    csrd_min = REGS["csrd-scope"]["values"]["min_employees_exclusive"]
    cap_max = REGS["csrd-value-chain-cap"]["values"]["max_employees"]
    assert "120 employees" in PAGE
    assert not employees > csrd_min  # first CSRD condition not met
    assert employees <= cap_max  # value-chain cap protects
