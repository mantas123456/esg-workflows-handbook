"""Recompute V5 (answering requests) from the Gozo questionnaire and the VSME datapoints."""
import re

from esgcalc import quality
from test_examples_scope3_report import category_summary
from test_examples_vsme import EXAMPLE, POINTS, page

Q = EXAMPLE["questionnaire"]
DECISION = {"answer": "Answer from the VSME report", "share": "Share voluntarily", "decline": "Decline for now"}
REGS_CAP = 1000


def test_v5_questionnaire_table() -> None:
    text = page("v5-requests.md")
    ids = {p["id"] for p in POINTS}
    for i, q in enumerate(Q["questions"], start=1):
        assert q["datapoint"] is None or set(q["datapoint"].split(", ")) <= ids, q["question"]
        # a question answered from the report needs a datapoint; one beyond the standard has none
        assert (q["datapoint"] is not None) == (q["decision"] == "answer"), q["question"]
        shown = q["datapoint"] or "Beyond the standard"
        row = f"| {i} | {q['question']} | {shown} | {'Yes' if in_cap(q) else 'No'} | {DECISION[q['decision']]} |"
        assert row in text, row
    within = sum(in_cap(q) for q in Q["questions"])
    assert within == 5
    assert f"So **{within} of {len(Q['questions'])}** questions are within the cap" in text
    assert f"and **{len(Q['questions']) - within}** are outside it" in text


def in_cap(q: dict) -> bool:
    """A question is within the cap if every datapoint answering it is linked to Annex II (more than 10 employees)."""
    if q["datapoint"] is None:
        return False
    by_id = {p["id"]: p for p in POINTS}
    return all(by_id[d]["cap"] for d in q["datapoint"].split(", "))


def test_v5_counts_and_cap() -> None:
    text = page("v5-requests.md")
    questions = Q["questions"]
    answered = sum(q["decision"] == "answer" for q in questions)
    beyond = len(questions) - answered
    assert (answered, beyond, len(questions)) == (6, 2, 8)
    assert f"**{answered} of {len(questions)}** questions are answered straight from the VSME report" in text
    assert f"**{beyond}** go beyond the" in text
    employees = EXAMPLE["company"]["employees"]
    assert employees <= REGS_CAP
    assert f"Gozo Fresh Foods Ltd (fictional, {employees} employees)" in text


def test_v5_scope3_shared_is_the_s9_figure() -> None:
    summary = category_summary()
    total = quality.sum_uncertainty([s["tco2e"] for s in summary.values()], [s["u95_rel"] for s in summary.values()])
    v, u = quality.round_result(total.value, total.u95_abs)
    assert f"shares it voluntarily: {v:,.0f} ± {u:,.0f} tCO2e" in page("v5-requests.md")


def test_v5_common_questions_map_to_real_datapoints() -> None:
    text = page("v5-requests.md")
    section = text.split("### 2. Map each question to a datapoint")[1].split("### 3.")[0]
    shown = set(re.findall(r"\b([BC]\d+-[a-z0-9-]+)\b", section))
    ids = {p["id"] for p in POINTS}
    assert shown and shown <= ids, shown - ids
    assert len(shown) >= 12


def test_v5_cap_wording_matches_the_fact() -> None:
    import yaml
    from pathlib import Path

    fact = {r["id"]: r for r in yaml.safe_load(
        (Path(__file__).resolve().parents[1] / "data/regulations.yml").read_text(encoding="utf-8"))}["csrd-value-chain-cap"]
    text = page("v5-requests.md")
    assert fact["values"]["max_employees"] == REGS_CAP and "**1,000 employees or fewer**" in text
    for phrase in ("Annex II", "right to refuse", "self-declaration", "manifestly"):
        assert phrase in fact["fact"] or phrase in fact["article"], phrase
    assert "Annex II of Delegated Regulation (EU) 2026/1560" in text and "**right to refuse**" in text


def test_v5_cap_list_matches_the_mapping() -> None:
    """The sentence after the step-2 table lists, for each datapoint in the table, whether it is in the cap."""
    text = page("v5-requests.md")
    by_id = {p["id"]: p for p in POINTS}
    inside = {"energy": "B3-energy", "Scope 1 and 2": "B3-scope1", "waste": "B7-waste", "employees": "B8-employees",
              "work accidents": "B9-accidents", "the human rights policy": "C6-human-rights-policies"}
    outside = {"Scope 3": None, "targets": "C3-targets", "climate risks": "C4-climate-risks",
               "water consumption": "B6-water-consumption", "fatalities": "B9-fatalities",
               "the pay gap": "B10-pay-gap", "corruption": "B11-corruption", "product footprints": None}
    for pid in inside.values():
        assert by_id[pid]["cap"], pid
    for pid in outside.values():
        assert pid is None or by_id[pid]["cap"] is None, pid
    assert "the cap covers " + ", ".join(list(inside)[:-1]) + " and " + list(inside)[-1] in text
    assert "It does **not** cover " + ", ".join(list(outside)[:2]) in text
    # every datapoint in the step-2 table is classified above
    section = text.split("### 2. Map each question to a datapoint")[1].split("### 3.")[0]
    shown = set(re.findall(r"\b([BC]\d+-[a-z0-9-]+)\b", section))
    classified = {v for v in {**inside, **outside}.values() if v} | {"B3-scope2-location", "B7-waste-recycled"}
    assert shown <= classified, shown - classified
