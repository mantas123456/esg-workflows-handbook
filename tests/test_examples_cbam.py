"""Recompute every number in the CBAM worked examples (CB1-CB10) with esgcalc.

The fictional data lives in data/examples/melita_metals.yml. Each test checks
that the page shows the number esgcalc produces.
"""
import re
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

import yaml

from esgcalc.cbam import authorisation_decision_deadline, may_import_pending_decision, threshold_check

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = yaml.safe_load((ROOT / "data/examples/melita_metals.yml").read_text(encoding="utf-8"))
IMPORTS = EXAMPLE["imports_2026"]


def page(name: str) -> str:
    """Page text with whitespace collapsed, so table cells and wrapped lines match."""
    return " ".join((ROOT / "docs/cbam" / name).read_text(encoding="utf-8").split())


def fmt(x: float) -> str:
    return f"{x:,.0f}" if float(x).is_integer() else f"{x:,}"


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
