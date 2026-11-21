"""scripts/check_regulations.py (warn at 90 days, fail at 180) and the F4 worked example."""
import re
import sys
from datetime import date, timedelta
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import check_regulations as cr  # noqa: E402

FACTS = {r["id"]: r for r in yaml.safe_load((ROOT / "data/regulations.yml").read_text(encoding="utf-8"))}
F4 = " ".join((ROOT / "docs/foundations/keeping-up.md").read_text(encoding="utf-8").split())


def test_levels_at_the_boundaries() -> None:
    d = date(2026, 1, 1)
    assert cr.Age("x", d, 89).level == "ok"
    assert cr.Age("x", d, 90).level == "warn"
    assert cr.Age("x", d, 179).level == "warn"
    assert cr.Age("x", d, 180).level == "fail"


def test_exit_codes(capsys) -> None:
    oldest = min(f["last_checked"] for f in FACTS.values())
    assert cr.main(["--today", str(oldest + timedelta(days=179))]) == 0
    assert cr.main(["--today", str(oldest + timedelta(days=180))]) == 1
    assert "FAIL: fact" in capsys.readouterr().out


def test_missing_date_is_an_error(tmp_path) -> None:
    bad = tmp_path / "r.yml"
    bad.write_text("- {id: x, fact: y}\n", encoding="utf-8")
    with pytest.raises(ValueError):
        cr.fact_ages(date(2027, 1, 1), bad)


def test_f4_check_table() -> None:
    checked = {f["last_checked"] for f in FACTS.values()}
    assert checked == {date(2026, 11, 20)}                                # "All 51 facts were last checked on 20 November 2026"
    n = len(FACTS)
    assert f"All {n} facts were last checked on 20 November 2026" in F4
    for run, days, result in ((date(2026, 11, 21), 1, f"{n} facts ok"),
                              (date(2027, 2, 18), 90, f"{n} warnings, build passes"),
                              (date(2027, 5, 19), 180, f"{n} over 180 days, **build fails**")):
        ages = cr.fact_ages(run)
        assert {a.days for a in ages} == {days}
        level = {1: "ok", 90: "warn", 180: "fail"}[days]
        assert {a.level for a in ages} == {level}
        assert f"| {run.day} {run:%b %Y} | {days} | {result} |" in F4, run
    assert "due by **18 February 2027**" in F4
    assert f"# {n} facts checked on 2027-02-18: 0 over 180 days, {n} over 90 days" in F4


WATCH = {   # row on the F4 page -> (fact id, phrase in the fact)
    "| End of 2026 | EFRAG plans to hand over the final ESRS XBRL taxonomy | `esrs-digital-tagging` |": ("esrs-digital-tagging", "by the end of 2026"),
    "| 1 Jan 2027 | GHG Protocol Land Sector and Removals Standard takes effect | `ghgp-land-sector` |": ("ghgp-land-sector", "takes effect on 1 January 2027"),
    "| 1 Jan 2027 | Revised ESRS mandatory for financial years starting from this date | `esrs-simplified` |": ("esrs-simplified", "mandatory for financial years starting on or after 1 Jan 2027"),
    "| 19 Mar 2027 | Deadline for Member States to transpose the CSRD changes of Omnibus I | `omnibus-i-transposition` |": ("omnibus-i-transposition", "by 19 Mar 2027"),
    "| Q2 2027 | GHG Protocol: draft revised Scope 3 Standard for public consultation (estimate) | `ghgp-scope3-standard` |": ("ghgp-scope3-standard", "estimated for Q2 2027"),
    "| 1 Jul 2027 | Deadline for the Commission to adopt limited assurance standards | `csrd-assurance` |": ("csrd-assurance", "1 July 2027"),
    "| 30 Sep 2027 | First CBAM annual declaration and surrender, for 2026 imports | `cbam-declaration` |": ("cbam-declaration", "30 Sep 2027 for 2026 imports"),
    "| Dec 2027 | Latest date to revise the CBAM default values and mark-ups | `cbam-default-values` |": ("cbam-default-values", "revised by December 2027 at the latest"),
}


def test_f4_watch_list_matches_the_facts() -> None:
    for row, (fid, phrase) in WATCH.items():
        assert row in F4, row
        assert phrase in FACTS[fid]["fact"], fid
    rows = re.findall(r"\| [^|]+ \| [^|]+ \| `([a-z0-9-]+)` \|", F4)
    assert rows == [fid for fid, _ in WATCH.values()]                     # nothing on the page that is not checked
    sources = re.search(r"Facts come from `data/regulations.yml` \(ids (.*?)\)", F4).group(1)
    assert set(re.findall(r"`([a-z0-9-]+)`", sources)) == {fid for fid, _ in WATCH.values()}
