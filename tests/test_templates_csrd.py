"""The CSRD templates: the DMA workbook scores like esgcalc.dma, the IRO register matches C2,
and the ESRS gap list is generated from data/esrs_datapoints.yml and counts like esgcalc.csrd."""
from pathlib import Path

import pytest
import yaml

from esgcalc.csrd import datapoints_in_scope, gap_summary
from esgcalc.dma import IRO, assess_all, load_parameters, topics
from test_templates import built, recalculate  # noqa: F401  (built is a fixture)

ROOT = Path(__file__).resolve().parents[1]
ESRS = yaml.safe_load((ROOT / "data/esrs_datapoints.yml").read_text(encoding="utf-8"))
MLG = yaml.safe_load((ROOT / "data/examples/mediterranean_logistics.yml").read_text(encoding="utf-8"))
TOPICAL = [s for s in ESRS["standards"] if s["kind"] == "topical"]


def _iros() -> list[IRO]:
    return [IRO(i["id"], i["topic"], i["description"], i["kind"], actual=i.get("actual", False),
                human_rights=i.get("human_rights", False), scale=i.get("scale"), scope=i.get("scope"),
                irremediability=i.get("irremediability"), likelihood=i.get("likelihood"),
                magnitude=i.get("magnitude")) for i in MLG["dma"]["iros"]]


def _yn(b: bool) -> str:
    return "Yes" if b else "No"


# --- DMA workbook -------------------------------------------------------------------------

def test_dma_examples_are_the_c2_items(built) -> None:
    from openpyxl import load_workbook
    ws = load_workbook(built["dma-workbook"])["Items"]
    for r, i in enumerate(_iros(), start=2):
        imp = i.kind == "impact"
        row = [ws.cell(r, c).value for c in range(1, 13)]
        assert row == [i.id, i.topic, i.description, i.kind.capitalize(),
                       "Yes" if imp else None, _yn(i.actual) if imp else None, _yn(i.human_rights) if imp else None,
                       i.scale, i.scope, i.irremediability, i.likelihood, i.magnitude], i.id
    assert ws.cell(2 + len(_iros()), 1).value is None


def test_dma_settings_match_the_parameters(built) -> None:
    got = recalculate(built["dma-workbook"])
    p = load_parameters()
    assert p["severity_aggregation"] == "max"                             # the workbook uses MAX
    assert got["SETTINGS!B1"] == p["scale"]["max"]
    assert got["SETTINGS!B2"] == p["thresholds"]["impact"]
    assert got["SETTINGS!B3"] == p["thresholds"]["financial"]
    assert got["SETTINGS!B4"] == p["human_rights"]["severity_precedence_from"]


def test_dma_scores_and_topics_match_esgcalc(built) -> None:
    got = recalculate(built["dma-workbook"])
    by_id = {a.iro.id: a for a in assess_all(_iros())}
    for r, i in enumerate(_iros(), start=2):
        a = by_id[i.id]
        assert got[f"ITEMS!N{r}"] == pytest.approx(a.score), i.id
        assert got[f"ITEMS!O{r}"] == _yn(a.material), i.id
    result = {t.topic: t for t in topics(by_id.values())}
    for r, s in enumerate(TOPICAL, start=2):
        assert got[f"TOPICS!A{r}"] == s["standard"]
        t = result.get(s["standard"])
        assert got[f"TOPICS!C{r}"] == (len(t.iros) if t else 0), s["standard"]
        assert got[f"TOPICS!D{r}"] == _yn(bool(t and t.impact_material)), s["standard"]
        assert got[f"TOPICS!E{r}"] == _yn(bool(t and t.financial_material)), s["standard"]
        assert got[f"TOPICS!F{r}"] == _yn(bool(t and t.material)), s["standard"]
    assert got["SETTINGS!B5"] == 9 and got["SETTINGS!B6"] == 4 and got["SETTINGS!B7"] == 3


def test_dma_formulas_handle_positive_and_potential_impacts(built, tmp_path) -> None:
    """Rows not in the example: a potential positive impact and a human rights impact below the cut-off."""
    from openpyxl import load_workbook
    wb = load_workbook(built["dma-workbook"])
    ws = wb["Items"]
    extra = [IRO("X1", "S4", "x", "impact", negative=False, actual=False, scale=4, scope=3, likelihood=5),
             IRO("X2", "S3", "x", "impact", negative=False, actual=True, scale=5, scope=4),
             IRO("X3", "S2", "x", "impact", human_rights=True, scale=3, scope=2, irremediability=3, likelihood=5)]
    for r, i in enumerate(extra, start=20):
        values = [i.id, i.topic, i.description, "Impact", _yn(i.negative), _yn(i.actual), _yn(i.human_rights),
                  i.scale, i.scope, i.irremediability, i.likelihood, None]
        for c, v in enumerate(values, start=1):
            ws.cell(r, c).value = v
    path = tmp_path / "dma.xlsx"
    wb.save(path)
    got = recalculate(path)
    for r, i in enumerate(extra, start=20):
        a = assess_all([i])[0]
        assert got[f"ITEMS!N{r}"] == pytest.approx(a.score), i.id      # 3.5 x 5 / 5 = 3.5; 4.5; 3 x 5 / 5 = 3
        assert got[f"ITEMS!O{r}"] == _yn(a.material), i.id


# --- IRO register -------------------------------------------------------------------------

def test_iro_register_matches_c2(built) -> None:
    from openpyxl import load_workbook
    ws = load_workbook(built["iro-register"])["Register"]
    assessed = assess_all(_iros())                                         # ranked as on the C2 page
    for r, a in enumerate(assessed, start=2):
        row = [ws.cell(r, c).value for c in range(1, 9)]
        assert row[:4] == [a.iro.id, a.iro.topic, a.iro.description, a.iro.kind.capitalize()], a.iro.id
        assert row[6] == pytest.approx(a.score) and row[7] == _yn(a.material), a.iro.id
        datapoints = ws.cell(r, 12).value
        if a.material:
            ids = {d["id"] for d in ESRS["datapoints"]}
            assert datapoints and set(datapoints.split(", ")) <= ids, a.iro.id
            assert all(d.startswith(a.iro.topic) for d in datapoints.split(", ")), a.iro.id
        else:
            assert datapoints is None, a.iro.id


# --- ESRS gap list ------------------------------------------------------------------------

def test_gap_list_rows_are_generated_from_the_datapoints(built) -> None:
    from openpyxl import load_workbook
    wb = load_workbook(built["esrs-gap-list"])
    ws = wb["Gap list"]
    points = ESRS["datapoints"]
    rows = [[ws.cell(r, c).value for c in range(1, 7)] for r in range(2, 2 + len(points))]
    assert rows == [[p["id"], p["standard"], p["dr"], p["description"], p["unit"], p["dataset"]] for p in points]
    assert ws.cell(2 + len(points), 1).value is None
    status = MLG["gap_status"]
    for r, p in enumerate(points, start=2):
        assert ws.cell(r, 7).value == status.get(p["id"]), p["id"]
    mt = wb["Material topics"]
    assert [(mt.cell(r, 1).value, mt.cell(r, 2).value) for r in range(2, 12)] == \
        [(s["standard"], s["topic"]) for s in TOPICAL]


def test_gap_list_summary_matches_esgcalc(built) -> None:
    got = recalculate(built["esrs-gap-list"])
    material = [t.topic for t in topics(assess_all(_iros())) if t.material]
    for r in range(2, 12):                                                 # the example's material column is C2's result
        assert got[f"MATERIAL TOPICS!C{r}"] == _yn(got[f"MATERIAL TOPICS!A{r}"] in material)
    scope = datapoints_in_scope(ESRS["datapoints"], material)
    s = gap_summary(scope, MLG["gap_status"])
    in_scope = {p["id"] for p in scope}
    for r, p in enumerate(ESRS["datapoints"], start=2):
        assert got[f"GAP LIST!K{r}"] == _yn(p["id"] in in_scope), p["id"]
    assert got["SUMMARY!B1"] == s.total == 15
    for row, status in enumerate(("Ready", "Partial", "Gap", "Phase-in"), start=2):
        assert got[f"SUMMARY!B{row}"] == s.counts[status], status
    assert got["SUMMARY!B6"] == 0
    assert got["SUMMARY!B7"] == pytest.approx(s.ready_share) == pytest.approx(0.4)


def test_standards_list_matches_the_datapoints_and_c6() -> None:
    assert [s["standard"] for s in ESRS["standards"]] == ["ESRS 2"] + [s["standard"] for s in TOPICAL]
    assert {s["standard"] for s in ESRS["standards"]} == {p["standard"] for p in ESRS["datapoints"]}
    c6 = (ROOT / "docs/csrd/c6-topical.md").read_text(encoding="utf-8")
    for s in TOPICAL:
        assert f"| {s['standard']} | {s['topic']}" in c6, s["standard"]
