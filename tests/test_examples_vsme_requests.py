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
        row = f"| {i} | {q['question']} | {shown} | {DECISION[q['decision']]} |"
        assert row in text, row


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
