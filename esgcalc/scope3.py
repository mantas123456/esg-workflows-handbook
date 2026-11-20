"""Scope 3 calculation methods: spend-based, average-data and supplier-specific,
and the hybrid combination of all three per category.

The method names follow the GHG Protocol Corporate Value Chain (Scope 3)
Standard and its calculation guidance (cited, not copied). Results are in
tonnes of CO2e; factors in kg CO2e per unit, as most open databases publish
them. These functions show the method; they do not choose factors for you.
"""
from __future__ import annotations

import math
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Iterable, Literal

from esgcalc.quality import DataQuality

CATEGORY_NAMES: dict[int, str] = {
    1: "Purchased goods and services",
    2: "Capital goods",
    3: "Fuel- and energy-related activities",
    4: "Upstream transportation and distribution",
    5: "Waste generated in operations",
    6: "Business travel",
    7: "Employee commuting",
    8: "Upstream leased assets",
    9: "Downstream transportation and distribution",
    10: "Processing of sold products",
    11: "Use of sold products",
    12: "End-of-life treatment of sold products",
    13: "Downstream leased assets",
    14: "Franchises",
    15: "Investments",
}

Method = Literal["supplier_specific", "average_data", "spend_based"]
METHODS: tuple[Method, ...] = ("supplier_specific", "average_data", "spend_based")
KG_PER_T = 1000.0


def _non_negative(name: str, value: float) -> None:
    if value < 0 or math.isnan(value):
        raise ValueError(f"{name} must be zero or more, got {value}")


def _positive(name: str, value: float) -> None:
    if not value > 0:
        raise ValueError(f"{name} must be more than zero, got {value}")


def spend_based(
    spend_eur: float,
    factor_kgco2e_per_currency_unit: float,
    *,
    factor_currency_per_eur: float = 1.0,
    price_index_spend_year: float | None = None,
    price_index_factor_year: float | None = None,
) -> float:
    """Emissions from money spent, with an environmentally extended spend factor.

    Steps, in short:

    1. convert the spend into the factor's currency:
       ``spend x factor_currency_per_eur`` (1.0 if the factor is per EUR);
    2. deflate it to the factor's price year:
       ``x price_index_factor_year / price_index_spend_year``
       (both indices from the same series, in the factor's currency area);
    3. multiply by the factor (kg CO2e per currency unit) and convert to tonnes.

    Without step 2, inflation since the factor's year overstates emissions.

    Returns:
        tCO2e.
    """
    _non_negative("spend_eur", spend_eur)
    _non_negative("factor_kgco2e_per_currency_unit", factor_kgco2e_per_currency_unit)
    _positive("factor_currency_per_eur", factor_currency_per_eur)
    if (price_index_spend_year is None) != (price_index_factor_year is None):
        raise ValueError("give both price indices or neither")
    spend = spend_eur * factor_currency_per_eur
    if price_index_spend_year is not None:
        _positive("price_index_spend_year", price_index_spend_year)
        _positive("price_index_factor_year", price_index_factor_year)
        spend = spend * price_index_factor_year / price_index_spend_year
    return spend * factor_kgco2e_per_currency_unit / KG_PER_T


def average_data(activity_amount: float, factor_kgco2e_per_unit: float) -> float:
    """Emissions from a physical quantity (kg, t, MWh, km...) and an average factor.

    ``activity x factor (kg CO2e per unit of activity) / 1000``. The activity and
    the factor must use the same unit; this function cannot check that.

    Returns:
        tCO2e.
    """
    _non_negative("activity_amount", activity_amount)
    _non_negative("factor_kgco2e_per_unit", factor_kgco2e_per_unit)
    return activity_amount * factor_kgco2e_per_unit / KG_PER_T


def supplier_specific(supplier_total_tco2e: float, purchased_quantity: float, supplier_total_quantity: float) -> float:
    """Your share of a supplier's emissions, allocated by quantity.

    ``supplier total x purchased quantity / supplier total output``. Use the
    same unit for both quantities (tonnes, units or revenue). The supplier's
    total should cover the goods you bought, cradle to gate.

    Returns:
        tCO2e.
    """
    _non_negative("supplier_total_tco2e", supplier_total_tco2e)
    _non_negative("purchased_quantity", purchased_quantity)
    _positive("supplier_total_quantity", supplier_total_quantity)
    if purchased_quantity > supplier_total_quantity:
        raise ValueError("purchased_quantity cannot exceed supplier_total_quantity")
    return supplier_total_tco2e * purchased_quantity / supplier_total_quantity


# --- hybrid combination ----------------------------------------------------

@dataclass(frozen=True)
class Line:
    """One line of a Scope 3 inventory."""
    category: int
    """GHG Protocol Scope 3 category, 1 to 15."""
    method: Method
    tco2e: float
    description: str = ""
    quality: DataQuality | None = None
    u95_rel: float | None = None
    """Relative half-width of the 95% interval, e.g. 0.2 for +/-20%."""

    def __post_init__(self) -> None:
        if not 1 <= self.category <= 15:
            raise ValueError(f"category must be 1 to 15, got {self.category}")
        if self.method not in METHODS:
            raise ValueError(f"unknown method {self.method!r}")
        _non_negative("tco2e", self.tco2e)
        if self.u95_rel is not None:
            _non_negative("u95_rel", self.u95_rel)


@dataclass(frozen=True)
class CategoryTotal:
    category: int
    tco2e: float
    by_method: dict[str, float] = field(default_factory=dict)
    lines: int = 0

    def share(self, method: Method) -> float:
        """Share of the category's emissions calculated with one method (0 to 1)."""
        return self.by_method.get(method, 0.0) / self.tco2e if self.tco2e else 0.0


def combine(lines: Iterable[Line]) -> dict[int, CategoryTotal]:
    """Hybrid method: add the lines of each category and show the mix of methods.

    Each purchase must appear in one line only: when supplier-specific data
    replaces an estimate, remove the estimate. This function adds what it is
    given; it cannot detect double counting.
    """
    totals: dict[int, list[float]] = defaultdict(list)
    by_method: dict[int, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    for line in lines:
        totals[line.category].append(line.tco2e)
        by_method[line.category][line.method].append(line.tco2e)
    return {
        cat: CategoryTotal(
            category=cat,
            tco2e=math.fsum(values),
            by_method={m: math.fsum(v) for m, v in by_method[cat].items()},
            lines=len(values),
        )
        for cat, values in sorted(totals.items())
    }


# --- screening ---------------------------------------------------------------

@dataclass(frozen=True)
class ScreeningRow:
    category: int
    name: str
    tco2e: float
    share: float
    """Share of the total screened Scope 3 (0 to 1)."""
    significant_by_size: bool
    other_reason: str
    """A reason other than size (spend, influence, risk, stakeholder views), or ''."""

    @property
    def significant(self) -> bool:
        return self.significant_by_size or bool(self.other_reason)


def screen(
    estimates_tco2e: dict[int, float],
    size_threshold_share: float,
    other_reasons: dict[int, str] | None = None,
) -> list[ScreeningRow]:
    """Screen all 15 categories: share of the total, size test and other reasons.

    Every category 1-15 must have an estimate (0 where it does not apply), so
    none is skipped silently. A category is significant by size when its share
    of the total is at least ``size_threshold_share`` (a threshold the company
    chooses and states). It is significant overall if it passes the size test
    or has another reason, such as spend, influence, transition risk or a
    stakeholder's request (the criteria ESRS E1 names).
    """
    if set(estimates_tco2e) != set(CATEGORY_NAMES):
        missing = sorted(set(CATEGORY_NAMES) - set(estimates_tco2e))
        raise ValueError(f"give an estimate for all 15 categories (0 if none); missing: {missing}")
    if not 0 < size_threshold_share < 1:
        raise ValueError("size_threshold_share must be between 0 and 1")
    for cat, t in estimates_tco2e.items():
        _non_negative(f"category {cat}", t)
    reasons = other_reasons or {}
    total = math.fsum(estimates_tco2e.values())
    if total == 0:
        raise ValueError("no emissions to screen")
    return [ScreeningRow(category=c, name=CATEGORY_NAMES[c], tco2e=estimates_tco2e[c],
                         share=estimates_tco2e[c] / total,
                         significant_by_size=estimates_tco2e[c] / total >= size_threshold_share,
                         other_reason=reasons.get(c, ""))
            for c in sorted(CATEGORY_NAMES)]
