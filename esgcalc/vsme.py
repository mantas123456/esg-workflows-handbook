"""Small calculations behind the VSME Basic Module metrics.

The voluntary standard (Delegated Regulation (EU) 2026/1560) says what to
report; these functions do the arithmetic. Where this handbook has not
checked the standard's exact definition, the docstring says so.
"""
from __future__ import annotations

import math
from typing import Iterable

HOURS_PER_FULL_TIME_WORKER = 2000
ACCIDENT_RATE_BASE_HOURS = 100 * HOURS_PER_FULL_TIME_WORKER   # 200,000 h = 100 full-time workers


def _non_negative(name: str, value: float) -> None:
    if value < 0 or math.isnan(value):
        raise ValueError(f"{name} must be zero or more, got {value}")


def energy_mwh(amounts_mwh: Iterable[float]) -> float:
    """Total energy consumption in MWh (B3): electricity plus fuels, all in MWh."""
    values = list(amounts_mwh)
    for v in values:
        _non_negative("energy", v)
    return math.fsum(values)


def ghg_intensity(total_tco2e: float, turnover_eur: float, per_eur: float = 1_000_000) -> float:
    """GHG intensity (B3): total GHG emissions divided by turnover.

    Returned per ``per_eur`` of turnover (default: tCO2e per EUR million), a
    readable scale; the value itself is total / turnover.
    """
    _non_negative("total_tco2e", total_tco2e)
    if not turnover_eur > 0:
        raise ValueError("turnover_eur must be more than zero")
    return total_tco2e / turnover_eur * per_eur


def accident_rate(recordable_accidents: int, hours_worked: float) -> float:
    """Rate of recordable work-related accidents (B9) per 100 full-time workers.

    ``accidents / hours worked x 200,000``: 200,000 hours are 100 workers at
    2,000 hours a year, the basis the standard uses.
    """
    _non_negative("recordable_accidents", recordable_accidents)
    if not hours_worked > 0:
        raise ValueError("hours_worked must be more than zero")
    return recordable_accidents / hours_worked * ACCIDENT_RATE_BASE_HOURS


def water_consumption_m3(withdrawal_m3: float, discharge_m3: float) -> float:
    """Water consumption (B6): withdrawal minus discharge."""
    _non_negative("withdrawal_m3", withdrawal_m3)
    _non_negative("discharge_m3", discharge_m3)
    if discharge_m3 > withdrawal_m3:
        raise ValueError("discharge cannot exceed withdrawal")
    return withdrawal_m3 - discharge_m3


def pay_gap(average_pay_men: float, average_pay_women: float) -> float:
    """Gender pay gap (B10) as a share: (men's average - women's average) / men's average.

    The usual definition, expressed as a share of men's average pay. This
    handbook has not checked the standard's exact wording; check it before
    reporting.
    """
    if not average_pay_men > 0:
        raise ValueError("average_pay_men must be more than zero")
    _non_negative("average_pay_women", average_pay_women)
    return (average_pay_men - average_pay_women) / average_pay_men


def readiness(points: Iterable[dict], done_ids: Iterable[str], option: str = "B") -> dict:
    """How ready a VSME report is: completeness by module and the datapoints still to do.

    ``points`` are the entries of data/vsme_datapoints.yml; ``done_ids`` the ids
    already collected (or marked not applicable). Option ``A`` counts the Basic
    Module only; option ``B`` counts both modules.

    Returns ``{"modules": {module: {"done", "total", "share"}}, "overall": share,
    "todo": [ids in order]}``.
    """
    if option not in ("A", "B"):
        raise ValueError("option must be 'A' or 'B'")
    modules = ("basic",) if option == "A" else ("basic", "comprehensive")
    pts = [p for p in points if p["module"] in modules]
    done = set(done_ids)
    unknown = done - {p["id"] for p in points}
    if unknown:
        raise ValueError(f"unknown datapoint ids: {sorted(unknown)}")
    out = {}
    for m in modules:
        in_m = [p for p in pts if p["module"] == m]
        d = sum(p["id"] in done for p in in_m)
        out[m] = {"done": d, "total": len(in_m), "share": d / len(in_m) if in_m else 0.0}
    total = len(pts)
    return {"modules": out,
            "overall": sum(p["id"] in done for p in pts) / total if total else 0.0,
            "todo": [p["id"] for p in pts if p["id"] not in done]}


def linear_target_path(base_value: float, base_year: int, target_year: int,
                       reduction_share: float) -> dict[int, float]:
    """A straight-line path from a base-year value to a reduction target.

    For example 1,800 tCO2e in 2026 and -30% by 2030 gives 1,260 tCO2e in 2030,
    falling by the same amount (135 tCO2e) each year. A planning aid for a
    target the company sets itself; it says nothing about whether the target
    is enough.
    """
    if not base_value > 0:
        raise ValueError("base_value must be more than zero")
    if target_year <= base_year:
        raise ValueError("target_year must be after base_year")
    if not 0 < reduction_share < 1:
        raise ValueError("reduction_share must be between 0 and 1")
    step = base_value * reduction_share / (target_year - base_year)
    return {year: base_value - step * (year - base_year) for year in range(base_year, target_year + 1)}


def turnover_rate(leavers: int, average_employees: float) -> float:
    """Employee turnover rate (B8): leavers / average number of employees.

    A common working definition; this handbook has not checked the
    standard's exact wording. Required from 50 employees.
    """
    _non_negative("leavers", leavers)
    if not average_employees > 0:
        raise ValueError("average_employees must be more than zero")
    return leavers / average_employees
