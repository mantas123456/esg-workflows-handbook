"""Recompute the CSRD worked examples (C1-C9) with esgcalc, and unit-test esgcalc.csrd.

The fictional group lives in data/examples/mediterranean_logistics.yml; its suppliers
are Gozo Fresh Foods and Melita Metals from the other tracks.
"""
from pathlib import Path

import pytest
import yaml

from esgcalc.csrd import protected_by_value_chain_cap, scope_test

ROOT = Path(__file__).resolve().parents[1]
MLG = yaml.safe_load((ROOT / "data/examples/mediterranean_logistics.yml").read_text(encoding="utf-8"))
GOZO = yaml.safe_load((ROOT / "data/examples/gozo_fresh_foods.yml").read_text(encoding="utf-8"))
MELITA = yaml.safe_load((ROOT / "data/examples/melita_metals.yml").read_text(encoding="utf-8"))


def page(name: str) -> str:
    return " ".join((ROOT / "docs/csrd" / name).read_text(encoding="utf-8").split())


def yes(b: bool) -> str:
    return "Yes" if b else "No"


def companies() -> list[tuple[str, int, float]]:
    """(name, employees, net turnover) of the group and its two suppliers."""
    return [
        (MLG["company"]["name"], MLG["company"]["employees"], MLG["company"]["net_turnover_eur"]),
        (GOZO["company"]["name"], GOZO["company"]["employees"], GOZO["vsme_basic"]["turnover_eur"]),
        (MELITA["company"]["name"], MELITA["company"]["employees"], MELITA["company"]["net_turnover_eur"]),
    ]


# --- C1 Scope ------------------------------------------------------------------------

def test_c1_scope_table() -> None:
    text = page("c1-scope.md")
    for name, emp, turnover in companies():
        t = scope_test(emp, turnover)
        first = str(t.first_financial_year) if t.first_financial_year else "–"
        row = (f"| {name} | {emp:,} | {turnover:,.0f} | {yes(t.employees_test)} | {yes(t.turnover_test)} | "
               f"{yes(t.in_scope)} | {first} |")
        assert row in text, row
    group = scope_test(MLG["company"]["employees"], MLG["company"]["net_turnover_eur"])
    assert group.in_scope and group.first_financial_year == 2027
    assert "first report is for **financial year 2027**" in text


def test_c1_what_if_and_cap() -> None:
    text = page("c1-scope.md")
    what_if = scope_test(MLG["company"]["employees"], 400_000_000)
    assert what_if.employees_test and not what_if.turnover_test and not what_if.in_scope
    assert "turnover were EUR 400 million" in text and "**not in scope**" in text
    for name, emp, _ in companies()[1:]:
        assert protected_by_value_chain_cap(emp), name
    assert "With 140 and 60 employees they are protected by the value-chain cap" in text
    assert "# True 2027" in text and "# False" in text and "# True" in text


def test_c1_suppliers_are_the_other_tracks_companies() -> None:
    names = [s["name"] for s in MLG["suppliers"]]
    assert names == [GOZO["company"]["name"], MELITA["company"]["name"]]


# --- esgcalc.csrd ---------------------------------------------------------------------

def test_scope_test_edges() -> None:
    assert not scope_test(1000, 500_000_000).in_scope                    # exactly 1,000 is not "more than"
    assert not scope_test(1001, 450_000_000).in_scope                    # exactly EUR 450 m is not "more than"
    assert scope_test(1001, 450_000_001).in_scope
    wave1 = scope_test(1200, 600_000_000, reported_from_fy2024=True)
    assert wave1.first_financial_year == 2024
    below = scope_test(800, 600_000_000, reported_from_fy2024=True)
    assert not below.in_scope and "may exempt" in below.note
    with pytest.raises(ValueError):
        scope_test(-1, 0)


def test_value_chain_cap_edges() -> None:
    assert protected_by_value_chain_cap(1000)                            # "1,000 or fewer"
    assert not protected_by_value_chain_cap(1001)
    with pytest.raises(ValueError):
        protected_by_value_chain_cap(-5)


# --- C2 Double materiality assessment -------------------------------------------------

def _iros():
    from esgcalc.dma import IRO
    return [IRO(i["id"], i["topic"], i["description"], i["kind"], actual=i.get("actual", False),
                human_rights=i.get("human_rights", False), scale=i.get("scale"), scope=i.get("scope"),
                irremediability=i.get("irremediability"), likelihood=i.get("likelihood"),
                magnitude=i.get("magnitude")) for i in MLG["dma"]["iros"]]


def test_c2_item_table_in_ranked_order() -> None:
    from esgcalc.dma import assess_all
    text = page("c2-dma.md")
    assessed = assess_all(_iros())
    positions = []
    for a in assessed:
        row = (f"| {a.iro.id} | {a.iro.topic} | {a.iro.description} | {a.iro.kind.capitalize()} | "
               f"{a.explanation} | {a.score:.1f} | {yes(a.material)} |")
        assert row in text, row
        positions.append(text.index(row))
    assert positions == sorted(positions)                                 # same order as esgcalc ranks them
    assert [a.iro.id for a in assessed if a.material] == ["S1-I1", "E1-I1", "E1-R1", "E5-I1"]
    assert "3 x 2 / 5 = 1.2" in text and "cut-off of 4" in text


def test_c2_topic_rollup() -> None:
    from esgcalc.dma import assess_all, load_parameters, topics
    text = page("c2-dma.md")
    result = topics(assess_all(_iros()))
    for t in result:
        assert f"| {t.topic} | {yes(t.impact_material)} | {yes(t.financial_material)} | {yes(t.material)} |" in text, t
    assert [t.topic for t in result if t.material] == ["E1", "E5", "S1"]
    assert "reports on **E1, E5 and S1**" in text
    p = load_parameters()
    assert p["human_rights"]["severity_precedence_from"] == 4
    assert p["thresholds"]["impact"] == p["thresholds"]["financial"] == 3.0
    assert "threshold of 3.0 on both sides" in text
    assert "print(a.score, a.material) # 5.0 True" in text


# --- C3 Value chain and data requests --------------------------------------------------

CAP = {d["id"]: d for d in yaml.safe_load((ROOT / "data/value_chain_cap.yml").read_text(encoding="utf-8"))["datapoints"]}


def _cap_label(cap_id: str) -> str:
    """'B3-32' -> 'B3 para 32'; 'B8-40a' -> 'B8 para 40(a)'."""
    disc, ref = cap_id.split("-")
    num = "".join(ch for ch in ref if ch.isdigit())
    letter = ref[len(num):]
    return f"{disc} para {num}" + (f"({letter})" if letter else "")


def test_c3_suppliers_are_protected() -> None:
    text = page("c3-value-chain.md")
    for name, emp, _ in companies()[1:]:
        assert protected_by_value_chain_cap(emp)
        assert f"| {name} | {emp:,} | Yes |" in text


def test_c3_request_table() -> None:
    text = page("c3-value-chain.md")
    for r in MLG["data_requests"]:
        for q in r["questions"]:
            if q["cap"] is not None:
                assert set(q["cap"]) <= set(CAP), q["cap"]
                # both suppliers have more than 10 employees: the longer list applies
                assert all(CAP[c]["large"] for c in q["cap"]), q["cap"]
                cells = f"{', '.join(_cap_label(c) for c in q['cap'])} | Yes"
            else:
                assert q["outcome"] in ("shared voluntarily", "declined")     # beyond: the supplier chose
                cells = "none | No: flagged, may refuse"
            row = f"| {r['supplier']} | {q['ask']} | {cells} | {q['outcome']} |"
            assert row in text, row
    assert "right to refuse" in text
    assert all(e > 10 for _, e, _ in companies()[1:]) and "more than 10 employees" in text
    # energy and GHG are outside the cap for the smallest suppliers
    assert not CAP["B3-32"]["small"] and not CAP["B3-33"]["small"] and CAP["B8-40a"]["small"]
    assert "shorter for suppliers with 10 employees or fewer" in text


# --- C4 General disclosures -------------------------------------------------------------

ESRS = {d["id"]: d for d in yaml.safe_load((ROOT / "data/esrs_datapoints.yml").read_text(encoding="utf-8"))["datapoints"]}


def test_c4_plan_covers_every_esrs2_datapoint() -> None:
    text = page("c4-general.md")
    plan = MLG["esrs2_plan"]
    assert {p["datapoint"] for p in plan} == {k for k, v in ESRS.items() if v["standard"] == "ESRS 2"}
    for p in plan:
        d = p["ready_by"]
        assert f"| {p['datapoint']} | {p['what']} | {p['owner']} | {d.day} {d:%b %Y} |" in text, p
    dates = {p["datapoint"]: p["ready_by"] for p in plan}
    assert min(dates, key=dates.get) == "ESRS2-materiality-process"       # "ready first"
    assert max(dates, key=dates.get) == "ESRS2-basis"
    assert "ESRS 1 chapter 10" in text and "paragraph 127" in text
    assert "first three years" in text and "(paragraph 123)" in text
    assert "proportion of its turnover, capital expenditure and" in text            # Taxonomy (CSRD-4)


def test_c4_phase_ins_not_needed_for_non_material_topics() -> None:
    from esgcalc.dma import assess_all, topics
    material = {t.topic for t in topics(assess_all(_iros())) if t.material}
    assert not material & {"E4", "S2", "S3", "S4"}
    assert "none of those topics was material in C2" in page("c4-general.md")


# --- C5 Climate (E1) --------------------------------------------------------------------

C = MLG["climate_2026"]


def _gozo_cradle_to_gate() -> tuple[float, float]:
    """Gozo Fresh Foods' Scope 1 and 2, and its upstream Scope 3 (categories 1-8), tCO2e."""
    from test_examples_scope3 import inventory_totals
    from test_examples_vsme_basic import scope12
    s1, s2 = scope12()
    upstream = sum(v.tco2e for k, v in inventory_totals().items() if k <= 8)
    return sum(s1) + s2, upstream


def _melita_lines() -> tuple[float, float, float]:
    """Steel (CBAM actual), steel indirect, aluminium (base default, no mark-up), tCO2e."""
    from test_examples_cbam import EXAMPLE as M, _installation_a
    a = M["installation_A_2026"]
    steel = _installation_a().see_tco2e_per_t * C["melita"]["steel_bars_t"]
    indirect = a["indirect_tco2e"] / a["production_mass_t"] * C["melita"]["steel_bars_t"]
    alu = M["default_values_base"]["aluminium_bars_B"]["base_direct_see_tco2e_per_t"] * C["melita"]["aluminium_bars_t"]
    return steel, indirect, alu


def _climate():
    from esgcalc import scope3
    s1 = [scope3.average_data(l["activity"], l["factor"]) for l in C["scope1_lines"]]
    s2 = scope3.average_data(C["scope2_location"]["activity_mwh"], C["scope2_location"]["factor_kg_per_mwh"])
    s12, up = _gozo_cradle_to_gate()
    gozo = scope3.supplier_specific(round(s12 + up), C["gozo"]["group_purchases_eur"],
                                    GOZO["vsme_basic"]["turnover_eur"])
    other = [scope3.spend_based(l["spend_eur"], l["factor"]) for l in C["other_lines"]]
    est = {k: float(v) for k, v in C["screening_other_categories"].items()}
    est[1] = gozo + other[0] + other[1]
    est[2] = sum(_melita_lines()) + other[2]
    rows = scope3.screen(est, C["size_threshold_share"], C["other_reasons"])
    return s1, s2, gozo, other, rows


def test_c5_scope1_and_2() -> None:
    from test_examples_scope3 import fmt
    text = page("c5-climate.md")
    s1, s2, *_ = _climate()
    assert s1 == pytest.approx([23_400, 1_500]) and s2 == pytest.approx(16_000)
    assert f"| Diesel for the truck fleet | 9,000,000 litre | 2.6 kg/litre | {fmt(s1[0])} |" in text
    assert f"| from service records | {fmt(s1[1])} |" in text
    assert f"| **Scope 1** | | | **{fmt(sum(s1))}** |" in text
    assert f"| Grid electricity (location-based) | 40,000 MWh | 400 kg/MWh | **{fmt(s2)}** |" in text
    from esgcalc.scope3 import average_data
    m = C["scope2_market"]
    s2m = average_data(m["activity_mwh"], m["factor_kg_per_mwh"])
    assert s2m == pytest.approx(18_000)
    assert (f"| Grid electricity (market-based: residual mix, no green contracts) | 40,000 MWh | "
            f"450 kg/MWh | **{fmt(s2m)}** |") in text
    assert f"| {fmt(s2)} tCO2e location-based; {fmt(s2m)} tCO2e market-based |" in text


def test_c5_uncertainty_of_the_spend_line() -> None:
    from test_examples_scope3 import fmt
    text = page("c5-climate.md")
    s1, s2, _, other, rows = _climate()
    u95 = C["spend_based_u95"]
    gozo_spend_u95 = {l["description"]: l.get("u95") for l in GOZO["uncertainty_category_1"]["lines"]}
    assert gozo_spend_u95["Other ingredient suppliers"] == u95             # "as Gozo's spend-based lines do in F2"
    food = other[0]
    rest = sum(s1) + s2 + sum(r.tco2e for r in rows) - food
    assert food * u95 > rest                                              # "more than all the other lines together"
    assert f"{fmt(food)} ± {fmt(food * u95)} tCO2e" in text
    assert f"({fmt(round(rest, 1))} tCO2e)" in text
    assert f"±{u95:.0%} at 95%" in text


def test_c5_gozo_allocation() -> None:
    from test_examples_scope3 import fmt
    text = page("c5-climate.md")
    s12, up = _gozo_cradle_to_gate()
    assert s12 == pytest.approx(1_800) and round(up, 1) == 5_493.6
    assert round(s12 + up) == 7_294
    gozo = _climate()[2]
    assert gozo == pytest.approx(1_823.5)
    assert f"of {fmt(s12)} tCO2e plus upstream Scope 3 (categories 1 to 8) of {round(up, 1):,} tCO2e" in text
    assert "**7,294 tCO2e** rounded" in text
    assert "7,294 x 3,500,000 / 14,000,000 = 1,823.5 tCO2e" in text


def test_c5_melita_cbam_lines() -> None:
    from test_examples_scope3 import fmt
    text = page("c5-climate.md")
    steel, indirect, alu = _melita_lines()
    assert (steel, indirect, alu) == pytest.approx((65.2, 12, 21))
    assert f"| 100 t x 0.652 | {fmt(steel)} |" in text
    assert f"| 100 t x 0.12 | {fmt(indirect)} |" in text
    assert f"| 10 t x 2.10 | {fmt(alu)} |" in text
    assert f"| **Melita Metals total** | | **{fmt(steel + indirect + alu)}** |" in text


def test_c5_screening_table_and_e1() -> None:
    from test_examples_scope3 import fmt
    text = page("c5-climate.md")
    s1, s2, gozo, other, rows = _climate()
    for r in rows:
        if r.tco2e == 0:
            continue
        row = (f"| {r.category} {r.name} | {fmt(r.tco2e)} | {fmt(round(100 * r.share, 2))}% | "
               f"{yes(r.significant_by_size)} | {r.other_reason} | {yes(r.significant)} |")
        row = " ".join(row.split())                                       # an empty cell collapses like the page
        assert row in text, row
    zeros = [str(r.category) for r in rows if r.tco2e == 0]
    assert f"Categories {', '.join(zeros[:-1])} and {zeros[-1]} are 0" in text
    assert [r.category for r in rows if r.significant] == [1, 2, 4]
    total3 = sum(r.tco2e for r in rows)
    assert total3 == pytest.approx(398_721.7)
    assert f"| {fmt(round(total3, 1))} tCO2e; significant: 1, 2, 4 |" in text
    assert f"Gozo Fresh Foods {fmt(gozo)} tCO2e; Melita Metals {fmt(sum(_melita_lines()))} tCO2e" in text
    for o in other:
        assert f"= {fmt(o)})" in text, o
    grand = sum(s1) + s2 + total3
    assert f"**{round(100 * total3 / grand, 1)}%** of the group's total of {fmt(round(grand, 1))} tCO2e" in text


def _material_standards() -> list[str]:
    from esgcalc.dma import assess_all, topics
    return [t.topic for t in topics(assess_all(_iros())) if t.material]


# --- C6 Other topical standards ---------------------------------------------------------

TOPICAL = ["E1", "E2", "E3", "E4", "E5", "S1", "S2", "S3", "S4", "G1"]
WHOLE_STANDARD_PHASE_IN = {"E4", "S2", "S3", "S4"}            # fact esrs-phase-in: first two years


def test_c6_overview_table() -> None:
    text = page("c6-topical.md")
    regs = {r["id"]: r for r in yaml.safe_load((ROOT / "data/regulations.yml").read_text(encoding="utf-8"))}
    assert "all DRs of E4, S2, S3 and S4 for their first two financial years" in regs["esrs-phase-in"]["fact"]
    assert {d["standard"] for d in ESRS.values()} - {"ESRS 2"} == set(TOPICAL)
    material = _material_standards()
    for std in TOPICAL:
        ids = [k for k, d in ESRS.items() if d["standard"] == std]
        if std in WHOLE_STANDARD_PHASE_IN:
            phase = "Yes"
        elif any("phase-in" in ESRS[i]["description"] for i in ids):
            phase = "Some datapoints"
        else:
            phase = "–"
        row = f"| {std} | {yes(std in material)} | {', '.join(ids)} | {phase} |"
        assert row in text, row
    assert "found E1, E5 and S1 material" in text


# --- C7 Datapoint gap analysis ----------------------------------------------------------

def _gap():
    from esgcalc.csrd import datapoints_in_scope, gap_summary
    scope = datapoints_in_scope(ESRS.values(), _material_standards())
    return scope, gap_summary(scope, MLG["gap_status"])


def test_c7_gap_table_and_summary() -> None:
    text = page("c7-gap-analysis.md")
    scope, summary = _gap()
    for d in scope:
        row = f"| {d['id']} | {d['standard']} | {d['dataset'] or '–'} | {MLG['gap_status'][d['id']]} |"
        assert row in text, row
    for status, n in summary.counts.items():
        assert f"| {status} | {n} |" in text, status
    assert f"| **Total** | **{summary.total}** |" in text
    assert (summary.counts["Ready"], summary.total) == (6, 15)
    assert f"**{summary.counts['Ready']} of {summary.total} ({summary.ready_share:.0%})** are ready" in text
    assert "# 6 15" in text
    gaps = [i for i, s in MLG["gap_status"].items() if s == "Gap"]
    assert gaps == ["ESRS2-basis", "E1-transition-plan", "E1-targets"]
    assert "The three gaps are the basis for preparation" in text


def test_c7_gap_summary_rejects_bad_status() -> None:
    from esgcalc.csrd import gap_summary
    scope, _ = _gap()
    status = dict(MLG["gap_status"])
    status.pop("E1-scope1")
    with pytest.raises(ValueError):
        gap_summary(scope, status)                                       # a datapoint without status
    with pytest.raises(ValueError):
        gap_summary(scope, {**MLG["gap_status"], "E2-pollution": "Gap"}) # not in scope
    with pytest.raises(ValueError):
        gap_summary(scope, {**MLG["gap_status"], "E1-scope1": "Done"})  # unknown status


# --- C8 Assurance readiness -------------------------------------------------------------

def test_c8_trail_values_come_from_c5() -> None:
    from test_examples_scope3 import fmt
    text = page("c8-assurance.md")
    s1, s2, gozo, _, _ = _climate()
    values = [sum(s1), s2, gozo, sum(_melita_lines())]
    for t, v in zip(MLG["assurance_trail"], values, strict=True):
        row = f"| {t['figure']} | {fmt(v)} | {t['files']} | {t['owner']} |"
        assert row in text, row
    assert "**limited assurance only**" in text and "**1 July 2027**" in text


# --- C9 Digital tagging and publication -------------------------------------------------

def test_c9_timeline() -> None:
    text = page("c9-tagging.md")
    steps = MLG["publication"]
    dates = [s["date"] for s in steps]
    assert dates == sorted(dates)
    for s in steps:
        d = s["date"]
        assert f"| {d.day} {d:%b %Y} | {s['step']} |" in text, s
    assert dates[0].year == 2028 and scope_test(1300, 520_000_000).first_financial_year == 2027
    assert f"takes **{(dates[-1] - dates[0]).days} days**" in text
    assert "consultation until 11 November 2026" in text


def test_c5_e1_datapoints_and_datasets() -> None:
    text = page("c5-climate.md")
    for dp in ("E1-scope1", "E1-scope2", "E1-scope3", "E1-scope3-suppliers"):
        d = ESRS[dp]
        assert f"| {dp}: {d['description']} | {d['dataset']} |" in text, dp



# --- 7.2 review fixes ---------------------------------------------------------------------

REGS = {r["id"]: r for r in yaml.safe_load((ROOT / "data/regulations.yml").read_text(encoding="utf-8"))}


def test_c1_groups_subsidiaries_and_non_eu_parents() -> None:
    text = page("c1-scope.md")
    assert "group, on a consolidated basis" in text and "29a(1)" in REGS["csrd-scope"]["article"]
    assert "**exempted**" in text and "Article 19a(9)" in REGS["csrd-subsidiary-exemption"]["article"]
    third = REGS["csrd-third-country"]["fact"]
    assert "above EUR 200 m" in third and "above EUR 450 m in each of the last two" in third
    assert "**more than EUR 200 million**" in text and "**EUR 450 million** in each of the last two years" in text
    assert "uses the **consolidated**" in text


def test_c1_malta_wording_matches_the_fact() -> None:
    text = page("c1-scope.md")
    fact = REGS["malta-csrd"]["fact"]
    assert "no such commencement notice was found" in fact and "Legal Notice 61 of 2026" in fact
    assert "**no commencement notice for Legal Notice 39**" in text
    assert "Legal Notice 61 of 2026, in force 20 March 2026" in text


def test_c8_and_c9_cite_the_articles_read() -> None:
    c8, c9 = page("c8-assurance.md"), page("c9-tagging.md")
    assert "Article 34(2a)" in c8 and "34(2a)" in REGS["csrd-assurance-scope"]["article"]
    assert "not required** to tag" in c9 and "not required to mark up" in REGS["csrd-management-report"]["fact"]
