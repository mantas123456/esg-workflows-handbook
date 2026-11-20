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
