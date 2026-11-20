"""Recompute V2 (Basic Module) from data/examples/gozo_fresh_foods.yml with esgcalc,
and unit-test esgcalc.vsme."""
import pytest

from esgcalc import scope3, vsme
from esgcalc.boundary import Entity, consolidate
from test_examples_vsme import EXAMPLE, page

B = EXAMPLE["vsme_basic"]


def scope12():
    s1 = [scope3.average_data(l["activity"], l["factor"]) for l in B["scope1_lines"]]
    s2 = scope3.average_data(B["scope2_location"]["activity_mwh"], B["scope2_location"]["factor_kg_per_mwh"])
    return s1, s2


def test_v2_b3_lines_and_totals() -> None:
    text = page("v2-basic.md")
    s1, s2 = scope12()
    for line, t in zip(B["scope1_lines"], s1):
        if line["unit"] == "tCO2e":
            calc = "from service records"
        else:
            calc = f"{line['activity']:,} {line['unit']} × {line['factor']:g} kg/{line['unit']}"
        assert f"| {line['description']} | {calc} | {t:,.2f} |" in text, line["description"]
    assert (sum(s1), s2) == (600.0, 1200.0)
    assert f"| **Scope 1** | | **{sum(s1):,.2f}** |" in text
    assert f"| **Scope 2 (location-based)** | | **{s2:,.2f}** |" in text
    assert f"| **Scope 1 and 2** | | **{sum(s1) + s2:,.2f}** |" in text
    sl = B["scope2_location"]
    assert f"{sl['activity_mwh']:,} MWh × {sl['factor_kg_per_mwh']} kg/MWh | {s2:,.2f}" in text


def test_v2_scope12_equals_the_s1_boundary_total() -> None:
    s1, s2 = scope12()
    chosen = consolidate([Entity(**e) for e in EXAMPLE["entities"]], EXAMPLE["chosen_approach"])
    assert sum(s1) + s2 == pytest.approx(chosen.tco2e) == pytest.approx(1800)
    assert f"**{chosen.tco2e:,.0f} tCO2e**, is the same total" in page("v2-basic.md")


def test_v2_energy_matches_scope3_category_3() -> None:
    # the electricity and fuel MWh are the same as the S2 category 3 screening lines
    e = B["energy"]
    cat3 = {l["description"]: l["activity"] for l in EXAMPLE["screening"]["lines"] if l["category"] == 3}
    assert sorted(cat3.values()) == sorted([e["fuels_mwh"], e["electricity_grid_mwh"]])
    assert vsme.energy_mwh([e["electricity_grid_mwh"], e["fuels_mwh"]]) == 5000


def test_v2_glance_table() -> None:
    text = page("v2-basic.md")
    s1, s2 = scope12()
    e, w, s, p, wa, waste = B["energy"], B["workforce"], B["safety"], B["pay"], B["water"], B["waste_t"]
    intensity = vsme.ghg_intensity(sum(s1) + s2, B["turnover_eur"])
    rate = vsme.accident_rate(s["recordable_accidents"], s["hours_worked"])
    gap = vsme.pay_gap(p["average_hourly_pay_men_eur"], p["average_hourly_pay_women_eur"])
    turnover = vsme.turnover_rate(w["leavers"], w["employees"])
    water = vsme.water_consumption_m3(wa["withdrawal_m3"], wa["discharge_m3"])
    energy = vsme.energy_mwh([e["electricity_grid_mwh"], e["fuels_mwh"]])
    expected = [
        f"| B3-energy | {energy:,.0f} MWh ({e['electricity_grid_mwh']:,} grid electricity, {e['fuels_mwh']:,} fuels); no renewable split available |",
        f"| B3-scope1 | {sum(s1):,.0f} tCO2e |",
        f"| B3-scope2-location | {s2:,.0f} tCO2e |",
        f"| B3-intensity | {intensity:,.2f} tCO2e per EUR million of turnover |",
        f"| B5-sensitive-sites | {B['sensitive_sites']} sites |",
        f"| B6-water-consumption | {water:,} m3 ({wa['withdrawal_m3']:,} withdrawn, {wa['discharge_m3']:,} discharged) |",
        f"| B7-waste | {waste['non_hazardous'] + waste['hazardous']} t ({waste['non_hazardous']} non-hazardous, {waste['hazardous']} hazardous) |",
        f"| B7-waste-recycled | {waste['recycled_or_reused']} t |",
        f"| B8-employees | {w['employees']} ({w['permanent']} permanent, {w['temporary']} temporary; {w['women']} women, {w['men']} men) |",
        f"| B8-turnover-rate | {turnover:.1%} ({w['leavers']} leavers) |",
        f"| B9-accidents | {s['recordable_accidents']}, rate {rate:g} per 100 full-time workers ({s['hours_worked']:,} hours) |",
        f"| B9-fatalities | {s['fatalities']} |",
        f"| B10-pay-gap | {gap:.1%} (EUR {p['average_hourly_pay_men_eur']:.2f} and EUR {p['average_hourly_pay_women_eur']:.2f} per hour) |",
        f"| B10-collective-bargaining | {p['collective_bargaining_share']:.0%} |",
        f"| B10-training | {p['training_hours_men']} hours (men), {p['training_hours_women']} hours (women) |",
        f"| B11-corruption | {B['corruption']['convictions']} convictions, EUR {B['corruption']['fines_eur']} |",
    ]
    for row in expected:
        assert row in text, row
    assert w["permanent"] + w["temporary"] == w["women"] + w["men"] == w["employees"]
    assert f"Turnover: **EUR {B['turnover_eur']:,}**" in text
    assert f"= {intensity:,.2f}" in text and f"× 200,000 = {rate:g}" in text and f"= {gap:.1%}" in text
    assert "# 128.57" in text and "# 2.4" in text and "# 0.08" in text


def test_v2_datapoints_in_glance_table_exist() -> None:
    from test_examples_vsme import POINTS

    ids = {p["id"] for p in POINTS}
    import re
    shown = set(re.findall(r"\| (B\d+-[a-z0-9-]+) \|", page("v2-basic.md")))
    assert shown and shown <= ids


# --- esgcalc.vsme -------------------------------------------------------------------

def test_vsme_functions() -> None:
    assert vsme.energy_mwh([3000, 2000]) == 5000
    assert vsme.ghg_intensity(1800, 14_000_000) == pytest.approx(128.5714, rel=1e-5)   # per EUR million
    assert vsme.ghg_intensity(1800, 14_000_000, per_eur=1) == pytest.approx(1800 / 14_000_000)
    assert vsme.accident_rate(3, 250_000) == pytest.approx(2.4)                          # 3 / 250,000 x 200,000
    assert vsme.accident_rate(1, 2000) == pytest.approx(100.0)                           # 1 accident, 1 full-time worker
    assert vsme.water_consumption_m3(40_000, 32_000) == 8000
    assert vsme.pay_gap(15.0, 13.8) == pytest.approx(0.08)
    assert vsme.turnover_rate(21, 140) == pytest.approx(0.15)


@pytest.mark.parametrize("call", [
    lambda: vsme.energy_mwh([1, -1]),
    lambda: vsme.ghg_intensity(10, 0),
    lambda: vsme.accident_rate(1, 0),
    lambda: vsme.water_consumption_m3(10, 20),
    lambda: vsme.pay_gap(0, 10),
    lambda: vsme.turnover_rate(1, 0),
])
def test_vsme_rejects_bad_input(call) -> None:
    with pytest.raises(ValueError):
        call()
