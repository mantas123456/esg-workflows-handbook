"""CSRD scope after Omnibus I, the start year, and the value-chain cap.

The thresholds come from data/regulations.yml (facts csrd-scope and
csrd-value-chain-cap), not from this code. These functions show the tests;
they do not decide whether the CSRD applies to a company: national law and
the full definitions in Directive 2013/34/EU do.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable

import yaml

REGULATIONS = Path(__file__).resolve().parents[1] / "data" / "regulations.yml"
FIRST_YEAR_NEW_REPORTERS = 2027        # fact csrd-stop-the-clock


@lru_cache(maxsize=None)
def _facts() -> dict[str, Any]:
    return {r["id"]: r for r in yaml.safe_load(REGULATIONS.read_text(encoding="utf-8"))}


@dataclass(frozen=True)
class ScopeTest:
    employees_test: bool
    """More than 1,000 employees."""
    turnover_test: bool
    """More than EUR 450 million net turnover."""
    first_financial_year: int | None
    """First financial year to report under the amended CSRD, or None if out of scope."""
    note: str

    @property
    def in_scope(self) -> bool:
        """Both conditions must be met."""
        return self.employees_test and self.turnover_test


def scope_test(employees: float, net_turnover_eur: float, reported_from_fy2024: bool = False) -> ScopeTest:
    """The CSRD scope test after Omnibus I, for an EU company.

    More than 1,000 employees **and** more than EUR 450 million net turnover.
    A company that never reported (not "wave one") and passes the test starts
    with financial year 2027 (stop-the-clock). A wave-one company below the
    thresholds leaves the scope from 2027, and its Member State may exempt it
    for 2025 and 2026.
    """
    if employees < 0 or net_turnover_eur < 0:
        raise ValueError("employees and turnover must be zero or more")
    v = _facts()["csrd-scope"]["values"]
    emp = employees > v["min_employees_exclusive"]
    turn = net_turnover_eur > v["min_turnover_eur_exclusive"]
    if emp and turn:
        if reported_from_fy2024:
            return ScopeTest(emp, turn, 2024, "Already reporting since financial year 2024 (wave one); continues.")
        return ScopeTest(emp, turn, FIRST_YEAR_NEW_REPORTERS,
                         "Never reported before: first report for financial year 2027 (stop-the-clock).")
    if reported_from_fy2024:
        return ScopeTest(emp, turn, None, "Wave one but below the thresholds: out of scope from 2027; "
                                          "the Member State may exempt 2025 and 2026.")
    return ScopeTest(emp, turn, None, "Below the thresholds: not in scope.")


GAP_STATUSES = ("Ready", "Partial", "Gap", "Phase-in")


def datapoints_in_scope(datapoints: Iterable[dict[str, Any]], material_standards: Iterable[str]) -> list[dict[str, Any]]:
    """The datapoints to cover: all of ESRS 2, plus those of the material topical standards."""
    material = set(material_standards)
    return [d for d in datapoints if d["standard"] == "ESRS 2" or d["standard"] in material]


@dataclass(frozen=True)
class GapSummary:
    counts: dict[str, int]
    """Number of datapoints per status, in the order of GAP_STATUSES."""
    total: int

    @property
    def ready_share(self) -> float:
        """Share of the datapoints in scope that are ready (0 to 1)."""
        return self.counts["Ready"] / self.total if self.total else 0.0


def gap_summary(in_scope: Iterable[dict[str, Any]], status: dict[str, str]) -> GapSummary:
    """Count the datapoints in scope by status. Every datapoint needs a status, and only those."""
    ids = [d["id"] for d in in_scope]
    missing = sorted(set(ids) - set(status))
    extra = sorted(set(status) - set(ids))
    if missing or extra:
        raise ValueError(f"status must cover exactly the datapoints in scope; missing {missing}, not in scope {extra}")
    unknown = sorted({s for s in status.values() if s not in GAP_STATUSES})
    if unknown:
        raise ValueError(f"unknown status {unknown}; use one of {GAP_STATUSES}")
    counts = {s: sum(1 for i in ids if status[i] == s) for s in GAP_STATUSES}
    return GapSummary(counts, len(ids))


def protected_by_value_chain_cap(average_employees: float) -> bool:
    """Whether a value-chain company is protected by the cap: on average 1,000 employees or fewer."""
    if average_employees < 0:
        raise ValueError("average_employees must be zero or more")
    return average_employees <= _facts()["csrd-value-chain-cap"]["values"]["max_employees"]
