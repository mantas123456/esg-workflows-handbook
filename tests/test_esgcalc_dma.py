"""Tests for esgcalc.dma. Expected values are worked out by hand in the comments."""
import copy
from pathlib import Path

import pytest
import yaml

from esgcalc import dma
from esgcalc.dma import IRO

ROOT = Path(__file__).resolve().parents[1]
P = dma.load_parameters()
REGS = {r["id"]: r for r in yaml.safe_load((ROOT / "data/regulations.yml").read_text(encoding="utf-8"))}


def params(**changes):
    p = copy.deepcopy(P)
    for key, value in changes.items():
        p[key] = value
    return p


# --- parameters --------------------------------------------------------------------

def test_parameters_point_to_the_fact_and_say_what_is_a_choice() -> None:
    assert P["fact"] == "esrs-dma-method" and P["fact"] in REGS
    assert "any one of the three can make a negative impact severe" in REGS["esrs-dma-method"]["fact"]
    assert "severity takes precedence over likelihood" in REGS["esrs-dma-method"]["fact"]
    assert "handbook choice" in P["thresholds"]["basis"]
    assert "handbook choice" in P["human_rights"]["basis"]
    assert (P["scale"]["min"], P["scale"]["max"]) == (1, 5)
    assert P["severity_aggregation"] == "max"


# --- impacts -----------------------------------------------------------------------

def test_actual_negative_uses_severity_max() -> None:
    # scale 4, scope 2, irremediability 1: severity = max = 4 >= 3 -> material
    a = dma.assess(IRO("I1", "E1", "x", "impact", negative=True, actual=True, scale=4, scope=2, irremediability=1))
    assert (a.score, a.material, a.dimension) == (4.0, True, "impact")


def test_actual_negative_with_mean_is_not_material() -> None:
    # mean (4 + 2 + 1) / 3 = 2.333 < 3
    p = params(severity_aggregation="mean")
    a = dma.assess(IRO("I1", "E1", "x", "impact", actual=True, scale=4, scope=2, irremediability=1), p)
    assert a.score == pytest.approx(7 / 3) and not a.material


def test_potential_negative_combines_severity_and_likelihood() -> None:
    # severity max(5, 3, 2) = 5; likelihood 2: 5 x 2 / 5 = 2.0 < 3
    a = dma.assess(IRO("I2", "E2", "x", "impact", scale=5, scope=3, irremediability=2, likelihood=2))
    assert (a.score, a.material) == (2.0, False)


def test_potential_human_rights_severity_takes_precedence() -> None:
    # severity 4 >= cut-off 4: score = 4.0 whatever the likelihood (1)
    a = dma.assess(IRO("I3", "S2", "x", "impact", human_rights=True, scale=4, scope=2, irremediability=3, likelihood=1))
    assert (a.score, a.material) == (4.0, True)
    assert "takes precedence" in a.explanation
    # below the cut-off: severity 3, likelihood 2 -> 3 x 2 / 5 = 1.2
    b = dma.assess(IRO("I4", "S2", "x", "impact", human_rights=True, scale=3, scope=2, irremediability=1, likelihood=2))
    assert b.score == pytest.approx(1.2) and not b.material
    # the same impact without the human-rights flag: 4 x 1 / 5 = 0.8
    c = dma.assess(IRO("I5", "S2", "x", "impact", scale=4, scope=2, irremediability=3, likelihood=1))
    assert c.score == pytest.approx(0.8)


def test_positive_impacts_use_scale_and_scope_only() -> None:
    # actual positive: (4 + 3) / 2 = 3.5 -> material; irremediability is not needed
    a = dma.assess(IRO("P1", "S1", "x", "impact", negative=False, actual=True, scale=4, scope=3))
    assert (a.score, a.material) == (3.5, True)
    # potential positive: (4 + 2) / 2 = 3, x likelihood 3 / 5 = 1.8
    b = dma.assess(IRO("P2", "S1", "x", "impact", negative=False, scale=4, scope=2, likelihood=3))
    assert b.score == pytest.approx(1.8) and not b.material


# --- risks and opportunities -------------------------------------------------------

def test_financial_materiality() -> None:
    # risk: 4 x 4 / 5 = 3.2 -> material; opportunity: 5 x 2 / 5 = 2.0 -> not
    r = dma.assess(IRO("R1", "E1", "x", "risk", magnitude=4, likelihood=4))
    o = dma.assess(IRO("O1", "E1", "x", "opportunity", magnitude=5, likelihood=2))
    assert (r.score, r.material, r.dimension) == (pytest.approx(3.2), True, "financial")
    assert (o.score, o.material) == (2.0, False)


def test_threshold_is_inclusive_and_configurable() -> None:
    # magnitude 5, likelihood 3: 5 x 3 / 5 = 3.0 -> exactly at 3.0 is material
    iro = IRO("R2", "E1", "x", "risk", magnitude=5, likelihood=3)
    assert dma.assess(iro).material
    assert not dma.assess(iro, params(thresholds={"impact": 3.0, "financial": 3.5, "basis": "test"})).material


# --- ranking and topics ------------------------------------------------------------

def test_ranking_and_topic_rollup() -> None:
    iros = [
        IRO("O1", "E1", "x", "opportunity", magnitude=5, likelihood=2),                        # 2.0, not material
        IRO("I1", "E1", "x", "impact", actual=True, scale=4, scope=2, irremediability=1),      # 4.0, material
        IRO("R1", "E5", "x", "risk", magnitude=4, likelihood=4),                               # 3.2, material
        IRO("I2", "E2", "x", "impact", scale=5, scope=3, irremediability=2, likelihood=2),     # 2.0, not material
    ]
    ranked = dma.assess_all(iros)
    assert [a.iro.id for a in ranked] == ["I1", "R1", "I2", "O1"]     # material first, then score, then id
    t = {r.topic: r for r in dma.topics(ranked)}
    assert (t["E1"].impact_material, t["E1"].financial_material, t["E1"].material) == (True, False, True)
    assert (t["E5"].impact_material, t["E5"].financial_material) == (False, True)
    assert not t["E2"].material
    assert t["E1"].iros == ["I1", "O1"]


# --- bad input ----------------------------------------------------------------------

@pytest.mark.parametrize("iro", [
    IRO("X1", "E1", "x", "impact", actual=True, scale=4, scope=2),                     # negative needs irremediability
    IRO("X2", "E1", "x", "impact", scale=4, scope=2, irremediability=1),               # potential needs likelihood
    IRO("X3", "E1", "x", "impact", actual=True, scale=6, scope=2, irremediability=1),  # above the scale
    IRO("X4", "E1", "x", "impact", actual=True, scale=True, scope=2, irremediability=1),
    IRO("X5", "E1", "x", "risk", likelihood=3),                                        # risk needs magnitude
    IRO("X6", "E1", "x", "guess", magnitude=3, likelihood=3),                          # type: ignore[arg-type]
])
def test_bad_input_is_rejected(iro) -> None:
    with pytest.raises(ValueError):
        dma.assess(iro)


def test_duplicate_ids_and_unknown_aggregation() -> None:
    i = IRO("D1", "E1", "x", "risk", magnitude=3, likelihood=3)
    with pytest.raises(ValueError):
        dma.assess_all([i, i])
    with pytest.raises(ValueError):
        dma.severity(IRO("D2", "E1", "x", "impact", scale=1, scope=1, irremediability=1), params(severity_aggregation="median"))
