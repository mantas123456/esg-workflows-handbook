"""The VSME templates: the Basic workbook is generated from data/vsme_datapoints.yml, its
example is Gozo Fresh Foods' status, its completeness matches esgcalc.vsme.readiness, and
the response bank asks what V5 maps."""
import re
from pathlib import Path

import pytest
import yaml

from esgcalc.vsme import readiness
from test_templates import _docx_text, built, recalculate  # noqa: F401  (built is a fixture)

ROOT = Path(__file__).resolve().parents[1]
DATA = yaml.safe_load((ROOT / "data/vsme_datapoints.yml").read_text(encoding="utf-8"))
POINTS = DATA["datapoints"]
GOZO = yaml.safe_load((ROOT / "data/examples/gozo_fresh_foods.yml").read_text(encoding="utf-8"))
BASIC = [p for p in POINTS if p["module"] == "basic"]


def _wb(built):
    from openpyxl import load_workbook

    return load_workbook(built["vsme-basic-workbook"])


def test_basic_rows_are_generated_from_the_datapoints(built) -> None:
    ws = _wb(built)["Basic"]
    rows = [[ws.cell(r, c).value for c in range(1, 5)] for r in range(2, 2 + len(BASIC))]
    assert rows == [[p["id"], p["disclosure"], p["description"], p["unit"]] for p in BASIC]
    assert ws.cell(2 + len(BASIC), 1).value is None                       # nothing after the last datapoint


def test_by_disclosure_rows_are_b1_to_b11(built) -> None:
    ws = _wb(built)["By disclosure"]
    topics = {d["disclosure"]: d["topic"] for d in DATA["disclosures"]}
    got = [(ws.cell(r, 1).value, ws.cell(r, 2).value) for r in range(2, 13)]
    assert got == [(f"B{i}", topics[f"B{i}"]) for i in range(1, 12)]


def test_examples_are_gozo_status(built) -> None:
    ws = _wb(built)["Basic"]
    status = GOZO["vsme_status"]
    assert set(status) == {p["id"] for p in BASIC}
    for r in range(2, 2 + len(BASIC)):
        pid = ws.cell(r, 1).value
        expected = [v if v != "" else None for v in status[pid]]
        assert [ws.cell(r, c).value for c in range(5, 9)] == expected, pid


def test_completeness_matches_esgcalc(built) -> None:
    got = recalculate(built["vsme-basic-workbook"])
    done = [k for k, v in GOZO["vsme_status"].items() if v[3] in ("Collected", "Not applicable")]
    r = readiness(POINTS, done, "A")
    assert got["COMPLETENESS!B1"] == len(BASIC) == r["modules"]["basic"]["total"] == 22
    assert got["COMPLETENESS!B2"] == r["modules"]["basic"]["done"] == 21
    assert got["COMPLETENESS!B3"] == pytest.approx(r["modules"]["basic"]["share"])
    for row in range(2, 13):
        disc = f"B{row - 1}"
        in_d = [p["id"] for p in BASIC if p["disclosure"] == disc]
        assert got[f"BY DISCLOSURE!C{row}"] == len(in_d), disc
        assert got[f"BY DISCLOSURE!D{row}"] == sum(i in done for i in in_d), disc
    assert got["BY DISCLOSURE!E6"] == pytest.approx(0.5)                     # B5: 1 of 2 done
    for r_, p in enumerate(BASIC, start=2):
        assert got[f"BASIC!I{r_}"] == (1 if p["id"] in done else 0), p["id"]


def test_response_bank_matches_v5(built) -> None:
    text = _docx_text(built["questionnaire-response-bank"])
    v5 = (ROOT / "docs/vsme/v5-requests.md").read_text(encoding="utf-8")
    section = v5.split("### 2. Map each question to a datapoint")[1].split("### 3.")[0]
    pairs = re.findall(r"^\| ([^|]+?) \| ([^|]+?) \|$", section, flags=re.M)
    pairs = [(q, d) for q, d in pairs if q not in ("Common question", "---")]
    assert len(pairs) == 13
    bank = (ROOT / "templates/src/questionnaire-response-bank.md").read_text(encoding="utf-8")
    for q, d in pairs:
        assert f"| {q} | {d} | | | |" in bank, q
        assert q in text
    for phrase in ("Delegated Regulation (EU) 2026/1560", "1,000", "Declining, politely"):
        assert phrase in text, phrase


def test_readiness_unit() -> None:
    done = ["B1-option", "C3-targets"]
    a = readiness(POINTS, done, "A")
    b = readiness(POINTS, done, "B")
    assert a["modules"]["basic"] == {"done": 1, "total": 22, "share": 1 / 22}
    assert "comprehensive" not in a["modules"] and "C3-targets" not in a["todo"]
    assert b["modules"]["comprehensive"]["done"] == 1 and b["overall"] == pytest.approx(2 / 31)
    with pytest.raises(ValueError):
        readiness(POINTS, ["X1-nope"], "B")
    with pytest.raises(ValueError):
        readiness(POINTS, [], "C")
