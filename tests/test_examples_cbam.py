"""Recompute every number in the CBAM worked examples (CB1-CB10) with esgcalc.

The fictional data lives in data/examples/melita_metals.yml. Each test checks
that the page shows the number esgcalc produces.
"""
import re
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

import pytest
import yaml

from esgcalc.cbam import authorisation_decision_deadline, may_import_pending_decision, threshold_check

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = yaml.safe_load((ROOT / "data/examples/melita_metals.yml").read_text(encoding="utf-8"))
IMPORTS = EXAMPLE["imports_2026"]


def page(name: str) -> str:
    """Page text with whitespace collapsed, so table cells and wrapped lines match."""
    return " ".join((ROOT / "docs/cbam" / name).read_text(encoding="utf-8").split())


def fmt(x: float) -> str:
    """Format a number as the pages show it: thousands separators, no float noise."""
    x = round(float(x), 6)   # 104,000 x 0.55 = 57,200.00000000001 in binary floats
    return f"{x:,.0f}" if x.is_integer() else f"{x:,}"


# --- CB1 Scope check -------------------------------------------------------

def test_cb1_totals_by_cn_code() -> None:
    text = page("cb1-scope-check.md")
    by_code: dict[str, float] = defaultdict(float)
    for line in IMPORTS:
        by_code[line["cn_code"]] += line["mass_t"]
    assert by_code == {"7214 20 00": 250, "7214 99 10": 150, "7604 29 10": 35}
    for code, mass in by_code.items():
        assert f"| {code} |" in text and f"| {fmt(mass)} |" in text

    result = threshold_check([(c, m) for c, m in by_code.items()])
    assert result.total_mass_t == 435
    assert result.above_threshold is True
    assert result.excluded_cn_codes == []
    assert f"**{fmt(result.total_mass_t)}**" in text
    assert f"{fmt(result.total_mass_t)} tonnes is more than 50 tonnes" in text
    assert "print(result.total_mass_t, result.above_threshold) # 435.0 True" in text


def test_cb1_running_total_by_quarter() -> None:
    text = page("cb1-scope-check.md")
    so_far: list[tuple[str, float]] = []
    first_above = None
    for q in ("Q1", "Q2", "Q3", "Q4"):
        lines = [(l["cn_code"], l["mass_t"]) for l in IMPORTS if l["quarter"] == q]
        so_far += lines
        in_quarter = sum(m for _, m in lines)
        r = threshold_check(so_far)
        above = "Yes" if r.above_threshold else "No"
        assert f"| {q} | {fmt(in_quarter)} | {fmt(r.total_mass_t)} | {above} |" in text, q
        if r.above_threshold and first_above is None:
            first_above = q
    assert first_above == "Q1"
    assert "went over 50 tonnes in the first quarter" in text


def test_cb1_steel_total_matches_t1_example() -> None:
    steel = sum(l["mass_t"] for l in IMPORTS if l["cn_code"].startswith("72"))
    assert steel == 400
    triage = " ".join((ROOT / "docs/start-here/triage.md").read_text(encoding="utf-8").split())
    assert "about 400 tonnes of steel bars" in triage


# --- CB2 Authorisation -----------------------------------------------------

def _d(d: date) -> str:
    """Format a date as on the page: 12 May 2026."""
    return f"{d.day} {d:%b %Y}"


def test_cb2_deadlines_and_transitional_rule() -> None:
    text = page("cb2-authorisation.md")
    a = EXAMPLE["authorisation"]
    received, info, effective = a["received"], a["info_requested"], a["decision_effective"]

    plain = authorisation_decision_deadline(received)
    extended = authorisation_decision_deadline(received, a["extension_days"])
    # 12 Jan + 120 days = 12 May; + 30 more = 11 Jun (150 days, under the 180 maximum)
    assert (plain, extended) == (date(2026, 5, 12), date(2026, 6, 11))
    assert received < info < effective <= extended

    timeline = [(received, "Competent authority receives"), (info, "asks for more information"),
                (plain, "receipt + 120 days"), (effective, "Decision takes effect"),
                (extended, "receipt + 150 days")]
    for d, label in timeline:
        assert f"| {_d(d)} | " in text and label in text, d
    page_dates = [datetime.strptime(m, "%d %b %Y").date()
                  for m in re.findall(r"\| (\d{1,2} [A-Z][a-z]{2} 2026) \|", text)]
    assert page_dates == sorted(page_dates) == sorted(d for d, _ in timeline)

    assert may_import_pending_decision(received, 2026) is True
    assert may_import_pending_decision(a["late_applicant_applied"], 2026) is False
    late = a["late_applicant_applied"]
    assert f"applies on {late.day} {late:%B %Y}" in text   # prose uses the full month name

    q1_t = sum(l["mass_t"] for l in IMPORTS if l["quarter"] == "Q1")
    assert q1_t == 68 and f"**{q1_t} tonnes**" in text
    for shown in ("# 2026-05-12", "# 2026-06-11", "# True", "# False"):
        assert shown in text


# --- CB3 Supplier data -----------------------------------------------------

def test_cb3_tonnes_by_installation_and_outcomes() -> None:
    text = page("cb3-supplier-data.md")
    by_inst: dict[str, float] = defaultdict(float)
    for line in IMPORTS:
        by_inst[line["installation"]] += line["mass_t"]
    total = threshold_check([(l["cn_code"], l["mass_t"]) for l in IMPORTS]).total_mass_t
    assert dict(by_inst) == {"A": 400, "B": 35} and total == 435

    shares = {k: round(100 * v / total) for k, v in by_inst.items()}
    assert shares == {"A": 92, "B": 8}          # 400/435 = 91.95%, 35/435 = 8.05%
    assert sum(shares.values()) == 100
    assert f"| {fmt(by_inst['A'])} | {shares['A']}% |" in text
    assert f"| {fmt(by_inst['B'])} | {shares['B']}% |" in text
    assert f"| **{fmt(total)}** | **100%** |" in text

    outcome = {r["installation"]: r for r in EXAMPLE["supplier_requests"]}
    label = {"actual": "Actual values", "default": "Default values"}
    for inst, r in outcome.items():
        assert f"| {inst} | {r['answer']} | {label[r['outcome']]} |" in text
        assert f"On {r['sent'].day} {r['sent']:%B %Y}" in text
    actual_share = sum(shares[i] for i, r in outcome.items() if r["outcome"] == "actual")
    assert f"**{actual_share}%** of Melita Metals' tonnes will have actual" in text
    assert f"other **{100 - actual_share}%**" in text


# --- CB4 Embedded emissions ------------------------------------------------

def _mass(inst: str) -> float:
    return sum(l["mass_t"] for l in IMPORTS if l["installation"] == inst)


def _installation_a():
    from esgcalc.cbam import Precursor, embedded_emissions
    a = EXAMPLE["installation_A_2026"]
    return embedded_emissions(
        sector="iron_steel", production_mass_t=a["production_mass_t"], direct_tco2e=a["direct_tco2e"],
        indirect_tco2e=a["indirect_tco2e"],
        precursors=[Precursor(p["mass_t"], p["see_tco2e_per_t"]) for p in a["precursors"]],
        imported_mass_t=_mass("A"))


def test_cb4_actual_values_installation_a() -> None:
    text = page("cb4-embedded-emissions.md")
    a = EXAMPLE["installation_A_2026"]
    e = _installation_a()
    prec = a["precursors"][0]
    precursor_tco2e = prec["mass_t"] * prec["see_tco2e_per_t"]
    # (8,000 + 104,000 x 0.55) / 100,000 = 65,200 / 100,000 = 0.652; x 400 t = 260.8
    assert precursor_tco2e == pytest.approx(57_200)
    assert e.see_tco2e_per_t == pytest.approx(0.652)
    assert e.total_tco2e == pytest.approx(260.8)
    assert e.indirect_included is False
    for shown in (f"| {fmt(a['production_mass_t'])} t |", f"| {fmt(a['direct_tco2e'])} tCO2e |",
                  f"| {fmt(a['indirect_tco2e'])} tCO2e, **not counted**",
                  f"{fmt(prec['mass_t'])} t x {prec['see_tco2e_per_t']} tCO2e/t = {fmt(precursor_tco2e)} tCO2e",
                  "SEE = (8,000 + 57,200) / 100,000 = **0.652 tCO2e/t**",
                  "0.652 x 400 t = **260.8 tCO2e**",
                  "print(a.see_tco2e_per_t, a.total_tco2e, a.indirect_included) # 0.652 260.8 False"):
        assert shown in text, shown


def test_cb4_default_values_installation_b_and_total() -> None:
    from esgcalc.cbam import default_value_with_markup
    text = page("cb4-embedded-emissions.md")
    base = EXAMPLE["default_values_base"]["aluminium_bars_B"]["base_direct_see_tco2e_per_t"]
    mass_b = _mass("B")
    rows = {y: default_value_with_markup(base, y, "aluminium") for y in (2026, 2027, 2028)}
    expected = {2026: (2.31, 80.85), 2027: (2.52, 88.2), 2028: (2.73, 95.55)}
    for y, see in rows.items():
        assert see == pytest.approx(expected[y][0])
        assert see * mass_b == pytest.approx(expected[y][1])
        markup = {2026: 10, 2027: 20, 2028: 30}[y]
        assert f"| {y} | {markup}% | {expected[y][0]} | {expected[y][1]} |" in text
    assert f"**{base:.2f} tCO2e/t**" in text
    assert "SEE = 2.10 x 1.10 = **2.31 tCO2e/t**" in text
    assert "2.31 x 35 t = **80.85 tCO2e**" in text
    assert "print(round(b_see, 2), round(b_see * 35, 2)) # 2.31 80.85" in text

    total = _installation_a().total_tco2e + rows[2026] * mass_b
    assert total == pytest.approx(341.65)
    assert "260.8 + 80.85 = **341.65 tCO2e**" in text


def test_cb4_what_actual_data_was_worth() -> None:
    from esgcalc.cbam import default_value_with_markup
    text = page("cb4-embedded-emissions.md")
    base = EXAMPLE["default_values_base"]["steel_bars_A"]["base_direct_see_tco2e_per_t"]
    see = default_value_with_markup(base, 2026, "iron_steel")
    assert see == pytest.approx(1.76)
    assert see * _mass("A") == pytest.approx(704)
    assert _mass("A") * see > _installation_a().total_tco2e
    assert "1.60 x 1.10 = 1.76 tCO2e/t" in text
    assert "1.76 x 400 t = **704 tCO2e**, instead of 260.8 tCO2e" in text


# --- CB5 Precursors --------------------------------------------------------

def _crude_steel(zero_rated: bool = False):
    from esgcalc.cbam import Precursor, embedded_emissions
    c = EXAMPLE["installation_A_crude_steel_2026"]
    return embedded_emissions(
        sector="iron_steel", production_mass_t=c["production_mass_t"], direct_tco2e=c["direct_tco2e"],
        precursors=[Precursor(p["mass_t"], p["see_tco2e_per_t"], zero_rated=zero_rated) for p in c["precursors"]],
        imported_mass_t=0)


def _bars_from(crude_see: float):
    from esgcalc.cbam import Precursor, embedded_emissions
    a = EXAMPLE["installation_A_2026"]
    return embedded_emissions(
        sector="iron_steel", production_mass_t=a["production_mass_t"], direct_tco2e=a["direct_tco2e"],
        precursors=[Precursor(a["precursors"][0]["mass_t"], crude_see)], imported_mass_t=_mass("A"))


def test_cb5_levels_rebuild_cb4_figure() -> None:
    text = page("cb5-precursors.md")
    c = EXAMPLE["installation_A_crude_steel_2026"]
    pig = c["precursors"][0]
    crude = _crude_steel()
    # (30,600 + 14,000 x 1.90) / 104,000 = 57,200 / 104,000 = 0.55
    assert pig["mass_t"] * pig["see_tco2e_per_t"] == pytest.approx(26_600)
    assert crude.see_tco2e_per_t == pytest.approx(0.55)
    # CB5's crude steel figure is the one CB4 used, and the bars match CB4
    assert crude.see_tco2e_per_t == pytest.approx(EXAMPLE["installation_A_2026"]["precursors"][0]["see_tco2e_per_t"])
    bars = _bars_from(crude.see_tco2e_per_t)
    assert (bars.see_tco2e_per_t, bars.total_tco2e) == (pytest.approx(0.652), pytest.approx(260.8))

    a = EXAMPLE["installation_A_2026"]
    assert c["production_mass_t"] == a["precursors"][0]["mass_t"]       # all crude steel used for the bars
    loss_t = c["production_mass_t"] - a["production_mass_t"]
    assert loss_t == 4_000 and f"The {fmt(loss_t)} t difference" in text

    for shown in ("**1.90 tCO2e/t**", "| 104,000 t |", "| 30,600 tCO2e |",
                  "14,000 t x 1.90 tCO2e/t = 26,600 tCO2e",
                  "(30,600 + 26,600) / 104,000 = **0.55 tCO2e/t**",
                  "(8,000 + 104,000 x 0.55) / 100,000 = **0.652 tCO2e/t**",
                  "0.652 x 400 t = **260.8 tCO2e**",
                  "# 0.55 0.652 260.8"):
        assert shown in text, shown


def test_cb5_eu_pig_iron_counts_as_zero() -> None:
    text = page("cb5-precursors.md")
    crude_eu = _crude_steel(zero_rated=True)
    bars_eu = _bars_from(crude_eu.see_tco2e_per_t)
    # 30,600 / 104,000 = 0.2942...; (8,000 + 30,600) / 100,000 = 0.386; x 400 = 154.4
    assert crude_eu.see_tco2e_per_t == pytest.approx(30_600 / 104_000)
    assert round(crude_eu.see_tco2e_per_t, 3) == 0.294
    assert bars_eu.see_tco2e_per_t == pytest.approx(0.386)
    assert bars_eu.total_tco2e == pytest.approx(154.4)
    assert "| SEE of crude steel | 0.55 tCO2e/t | 30,600 / 104,000 = 0.294 tCO2e/t |" in text
    assert "| SEE of steel bars | 0.652 tCO2e/t | 0.386 tCO2e/t |" in text
    assert "| Melita Metals' 400 t | 260.8 tCO2e | 154.4 tCO2e |" in text


# --- CB6-CB10: verification, carbon price, certificates, declaration, records

def _emissions_2026() -> tuple[float, float]:
    """Embedded emissions (tCO2e) for Installation A (actual) and B (default + 2026 mark-up)."""
    from esgcalc.cbam import default_value_with_markup
    base_b = EXAMPLE["default_values_base"]["aluminium_bars_B"]["base_direct_see_tco2e_per_t"]
    return _installation_a().total_tco2e, default_value_with_markup(base_b, 2026, "aluminium") * _mass("B")


def _fa_2026() -> tuple[float, float]:
    fa = EXAMPLE["free_allocation_adjustment_tco2e_per_t"][2026]
    return fa["A"] * _mass("A"), fa["B"] * _mass("B")


def _certs_2026(reduction: float = 0.0) -> float:
    from esgcalc.cbam import certificates_needed
    return certificates_needed(sum(_emissions_2026()), sum(_fa_2026()), reduction)


def test_cb6_verification_checks_and_share() -> None:
    text = page("cb6-verification.md")
    v = EXAMPLE["verification_A"]
    assert v["report_issued"] <= v["accreditation_valid_until"]      # valid on the report date
    assert f"Report issued {_d(v['report_issued'])}; accreditation valid until {_d(v['accreditation_valid_until'])}" in text
    a, b = _emissions_2026()
    share = round(100 * a / (a + b), 1)
    # 260.8 / 341.65 = 76.3%
    assert share == 76.3
    assert f"**{fmt(a)} of its {fmt(a + b)} tCO2e**, or **{share}%**" in text
    assert f"The other {fmt(b)} tCO2e" in text
    assert f"{_installation_a().see_tco2e_per_t:.3f} tCO2e/t, as used in CB4" in text


def test_cb7_what_if_reduction() -> None:
    from esgcalc.cbam import certificate_cost
    text = page("cb7-carbon-price-paid.md")
    cp = EXAMPLE["carbon_price_paid"]
    price = EXAMPLE["certificate_price_assumed_eur_per_tco2e"]
    base, what_if = _certs_2026(cp["claimed_certificates"]), _certs_2026(cp["what_if_reduction_certificates"])
    assert (round(base, 6), round(what_if, 6)) == (39.4, 34.4)
    cost_base, cost_if = certificate_cost(round(base, 6), price), certificate_cost(round(what_if, 6), price)
    assert (str(cost_base), str(cost_if)) == ("3152.00", "2752.00")
    assert f"| Certificates to surrender | {fmt(round(base, 6))} | {fmt(round(what_if, 6))} |" in text
    assert "| EUR 3,152.00 | EUR 2,752.00 |" in text
    assert f"reduction of **{cp['what_if_reduction_certificates']} certificates**" in text
    assert "# 34.4 2752.00" in text


def test_cb8_certificates_and_cost() -> None:
    from esgcalc.cbam import certificate_cost
    text = page("cb8-certificates.md")
    a, b = _emissions_2026()
    fa_a, fa_b = _fa_2026()
    # 0.585 x 400 = 234.0; 1.95 x 35 = 68.25; total 302.25
    assert (fa_a, fa_b) == (pytest.approx(234.0), pytest.approx(68.25))
    certs = round(_certs_2026(), 6)
    assert certs == 39.4                                    # 341.65 - 302.25 - 0
    assert str(certificate_cost(certs, EXAMPLE["certificate_price_assumed_eur_per_tco2e"])) == "3152.00"
    assert f"| Embedded emissions (tCO2e), from CB4 | {fmt(a)} | {fmt(b)} | {fmt(a + b)} |" in text
    assert "| Free allocation adjustment (tCO2e) | 234.0 | 68.25 | 302.25 |" in text
    assert "341.65 − 302.25 − 0 = **39.4 certificates**" in text
    assert "39.4 × 80.00 = **EUR 3,152.00**" in text
    assert "# 39.4 3152.00" in text


def test_cb8_cbam_factor_table_matches_parameters() -> None:
    from esgcalc.cbam import load_parameters
    text = page("cb8-certificates.md")
    factors = load_parameters()["cbam_factor_by_year"]["values"]
    cells = " | ".join("none" if f == 0 else f"{f * 100:g}%" for _, f in sorted(factors.items()))
    assert f"| CBAM factor | {cells} |" in text


def test_cb8_quarterly_holding_2027() -> None:
    from esgcalc.cbam import quarterly_holding
    text = page("cb8-certificates.md")
    assert EXAMPLE["imports_2027_same_as_2026"] is True
    base = EXAMPLE["default_values_base"]
    see_a, see_b = base["steel_bars_A"]["base_direct_see_tco2e_per_t"], base["aluminium_bars_B"]["base_direct_see_tco2e_per_t"]
    fa = EXAMPLE["free_allocation_adjustment_tco2e_per_t"][2027]
    expected = {"Q1": 31.7, "Q2": 89.25, "Q3": 146.9, "Q4": 209.5}
    quarters: list[str] = []
    for q in ("Q1", "Q2", "Q3", "Q4"):
        quarters.append(q)
        ma = sum(l["mass_t"] for l in IMPORTS if l["installation"] == "A" and l["quarter"] in quarters)
        mb = sum(l["mass_t"] for l in IMPORTS if l["installation"] == "B" and l["quarter"] in quarters)
        emissions, adjustment = ma * see_a + mb * see_b, ma * fa["A"] + mb * fa["B"]
        hold = quarterly_holding(emissions, 2027, adjustment)
        assert hold == pytest.approx(expected[q])
        assert f"| {q} 2027 | {fmt(ma)} | {fmt(mb)} | {fmt(emissions)} | {fmt(adjustment)} | {fmt(hold)} |" in text, q
    assert "50% × (112.8 − 49.4) = **31.7 certificates**" in text
    assert "# 31.7" in text


def test_cb9_declaration_summary() -> None:
    text = page("cb9-declaration.md")
    a, b = _emissions_2026()
    fa_a, fa_b = _fa_2026()
    submitted = EXAMPLE["declaration_2026"]["submitted"]
    assert submitted <= date(2027, 9, 30)
    assert f"**{submitted.day} {submitted:%B %Y}**" in text
    assert f"| Quantity imported (t) | {fmt(_mass('A'))} | {fmt(_mass('B'))} | {fmt(_mass('A') + _mass('B'))} |" in text
    assert f"| Embedded emissions (tCO2e) | {fmt(a)} | {fmt(b)} | {fmt(a + b)} |" in text
    assert f"| Free allocation adjustment (tCO2e) | 234.0 | {fmt(fa_b)} | {fmt(fa_a + fa_b)} |" in text
    assert f"| **Certificates to surrender** | | | **{fmt(round(_certs_2026(), 6))}** |" in text
    assert f"issued {_d(EXAMPLE['verification_A']['report_issued'])}" in text


def test_cb10_retention_and_folder() -> None:
    from esgcalc.cbam import records_retention_end
    text = page("cb10-records.md")
    end = records_retention_end(2027)
    assert end == date(2031, 12, 31)
    assert f"**{end.day} {end:%B %Y}**" in text and f"Keep until {_d(end)}" in text
    assert "# 2031-12-31" in text
    assert f"# {len(IMPORTS)} import lines, {fmt(_mass('A') + _mass('B'))} t" in text
    assert f"| Certificates to surrender | {fmt(round(_certs_2026(), 6))} | certificates |" in text
    for link in ("../foundations/evidence-locker.md", "scripts/hash_evidence.py"):
        assert link in text
