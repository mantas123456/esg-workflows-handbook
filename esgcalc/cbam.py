"""CBAM calculations: threshold check, embedded emissions, certificates and cost.

Legal basis: Regulation (EU) 2023/956 as amended by Regulation (EU) 2025/2083
(consolidated text of 20 October 2025). Parameters come from
``data/cbam_parameters.yml``; each function names the article it follows.

These functions show the method. They are not legal advice and do not
replace the CBAM registry's own calculation.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import date, timedelta
from decimal import ROUND_HALF_UP, Decimal
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable, Sequence

import yaml

PARAMETERS_PATH = Path(__file__).resolve().parents[1] / "data" / "cbam_parameters.yml"
CENT = Decimal("0.01")


@lru_cache(maxsize=None)
def _load(path: str) -> dict[str, Any]:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def load_parameters(path: Path | None = None) -> dict[str, Any]:
    """Read CBAM parameters (threshold, sectors, holding rule) from YAML."""
    return _load(str(path or PARAMETERS_PATH))


def normalise_cn_code(cn_code: str) -> str:
    """Remove spaces and dots: ``"7208 51 20"`` -> ``"72085120"``."""
    code = cn_code.replace(" ", "").replace(".", "")
    if not code.isdigit():
        raise ValueError(f"CN code must contain digits only: {cn_code!r}")
    return code


def _non_negative(name: str, value: float) -> None:
    if value < 0 or math.isnan(value):
        raise ValueError(f"{name} must be zero or more, got {value}")


# --- Threshold -------------------------------------------------------------

@dataclass(frozen=True)
class ThresholdResult:
    total_mass_t: float
    """Net mass of CBAM goods counted towards the threshold (hydrogen and electricity excluded)."""
    threshold_t: float
    above_threshold: bool
    """True when ``total_mass_t`` exceeds the threshold. Exactly 50 t is not above."""
    excluded_cn_codes: list[str] = field(default_factory=list)
    """Hydrogen or electricity codes found: the threshold never covers these."""
    notes: list[str] = field(default_factory=list)


def threshold_check(imports: Iterable[tuple[str, float]], params: dict[str, Any] | None = None) -> ThresholdResult:
    """Check the single mass-based threshold for one importer and one calendar year.

    Article 2a and Annex VII of Regulation (EU) 2023/956: an importer is exempt
    when the net mass of its CBAM goods does not cumulatively exceed 50 t in a
    calendar year, all CN codes added together. The exemption does not cover
    hydrogen (CN 2804 10 00) or electricity (CN 2716 00 00). If the year's total
    goes over the threshold, obligations cover all goods imported that year.

    Args:
        imports: ``(cn_code, mass_t)`` pairs for CBAM goods only (Annex I). Mass is
            net mass in tonnes. Electricity lines are listed but not added up.
        params: parameters dict; defaults to ``data/cbam_parameters.yml``.

    Returns:
        A :class:`ThresholdResult`. It shows the test; it does not decide scope.
    """
    p = (params or load_parameters())["threshold"]
    limit_t = Decimal(str(p["max_exempt_mass_t"]))
    excluded = {normalise_cn_code(c): name for c, name in p["excluded_cn_codes"].items()}

    # Sum as decimals: masses are entered as decimal numbers, and a binary float
    # sum of e.g. 45 x 1.1 t + 0.5 t gives 50.00000000000001, wrongly "above" 50 t.
    total = Decimal(0)
    found_excluded: list[str] = []
    for cn_code, mass_t in imports:
        _non_negative("mass_t", mass_t)
        code = normalise_cn_code(cn_code)
        if code in excluded:
            found_excluded.append(code)
        else:
            total += Decimal(str(mass_t))
    notes = ["Hydrogen and electricity have no threshold: any quantity needs an authorised CBAM declarant."]
    if found_excluded:
        names = sorted({excluded[c] for c in found_excluded})
        notes.append(f"Imports include {', '.join(names)}: the exemption does not apply to these goods.")
    return ThresholdResult(
        total_mass_t=float(total),
        threshold_t=float(limit_t),
        above_threshold=total > limit_t,
        excluded_cn_codes=sorted(set(found_excluded)),
        notes=notes,
    )


# --- Authorisation ---------------------------------------------------------

def authorisation_decision_deadline(
    received: date,
    extension_days: int = 0,
    params: dict[str, Any] | None = None,
) -> date:
    """Latest date for the competent authority's decision on an application.

    Implementing Regulation (EU) 2025/486, Article 4: the authority assesses the
    application within 120 calendar days of receipt. When it asks for more
    information it may extend this by up to 30 calendar days, and the total may
    not exceed 180 days from receipt.

    Args:
        received: date the competent authority received the application.
        extension_days: days of extension the authority notified (0 if none).
    """
    p = (params or load_parameters())["authorisation"]
    if not 0 <= extension_days <= int(p["max_extension_days"]):
        raise ValueError(f"extension_days must be between 0 and {p['max_extension_days']}")
    days = min(int(p["decision_days"]) + extension_days, int(p["max_total_days"]))
    return received + timedelta(days=days)


def may_import_pending_decision(applied: date, year: int, params: dict[str, Any] | None = None) -> bool:
    """Whether the 2026 transitional rule lets an applicant import before the decision.

    Regulation (EU) 2023/956, Article 17(7a): an application made by 31 March
    2026 lets the applicant keep importing in 2026 until the decision takes
    effect. Outside 2026, or for later applications, the answer is False:
    authorisation is needed before importing above the threshold.
    """
    p = (params or load_parameters())["authorisation"]
    apply_by = p["transitional_apply_by"]
    return year == apply_by.year and applied <= apply_by


# --- Embedded emissions ----------------------------------------------------

@dataclass(frozen=True)
class Precursor:
    """A relevant precursor consumed to make the goods."""
    mass_t: float
    see_tco2e_per_t: float
    """Specific embedded emissions of the precursor (tCO2e per tonne)."""


@dataclass(frozen=True)
class EmbeddedEmissions:
    see_tco2e_per_t: float
    """Specific embedded emissions of the goods (tCO2e per tonne)."""
    total_tco2e: float
    """Embedded emissions in the imported quantity (tCO2e)."""
    indirect_included: bool


def embedded_emissions(
    *,
    sector: str,
    production_mass_t: float,
    direct_tco2e: float,
    indirect_tco2e: float = 0.0,
    precursors: Sequence[Precursor] = (),
    imported_mass_t: float,
    params: dict[str, Any] | None = None,
) -> EmbeddedEmissions:
    """Specific and total embedded emissions of imported goods (actual values).

    Method of Annex IV to Regulation (EU) 2023/956, in short:

        SEE = (direct + indirect + sum(precursor mass x precursor SEE)) / production mass
        total = SEE x imported mass

    Indirect emissions count only for goods not listed in Annex II (Article 7
    and Annex II): they count for cement and fertilisers, not for iron and
    steel, aluminium or hydrogen. For an Annex II sector the ``indirect_tco2e``
    argument is ignored and ``indirect_included`` is False. Electricity uses a
    separate method and is rejected here.

    Args:
        sector: one of ``cement``, ``fertilisers``, ``iron_steel``, ``aluminium``, ``hydrogen``.
        production_mass_t: activity level of the production process in the reporting period (t).
        direct_tco2e: direct emissions attributed to the production process (tCO2e).
        indirect_tco2e: emissions from electricity consumed by the process (tCO2e).
        precursors: relevant precursors consumed; empty for simple goods.
        imported_mass_t: net mass of the goods imported (t).
    """
    sectors = (params or load_parameters())["sectors"]
    if sector not in sectors or not isinstance(sectors[sector], dict):
        raise ValueError(f"unknown CBAM sector {sector!r}")
    if sectors[sector].get("separate_method"):
        raise ValueError(f"{sector}: embedded emissions use a separate method (Annex IV); not covered here")
    for name, value in (("direct_tco2e", direct_tco2e), ("indirect_tco2e", indirect_tco2e),
                        ("imported_mass_t", imported_mass_t)):
        _non_negative(name, value)
    if production_mass_t <= 0:
        raise ValueError("production_mass_t must be more than zero")

    include_indirect = not sectors[sector]["direct_only"]
    precursor_tco2e = math.fsum(pr.mass_t * pr.see_tco2e_per_t for pr in precursors)
    attributed_tco2e = math.fsum([direct_tco2e, indirect_tco2e if include_indirect else 0.0, precursor_tco2e])
    see = attributed_tco2e / production_mass_t
    return EmbeddedEmissions(see_tco2e_per_t=see, total_tco2e=see * imported_mass_t,
                             indirect_included=include_indirect)


# --- Certificates ----------------------------------------------------------

def certificates_needed(
    total_tco2e: float,
    free_allocation_adjustment_tco2e: float = 0.0,
    carbon_price_paid_tco2e: float = 0.0,
    params: dict[str, Any] | None = None,
) -> float:
    """Number of CBAM certificates to surrender for one year's imports.

    certificates = (embedded emissions - free allocation adjustment
                    - carbon-price-paid reduction) / tCO2e per certificate,
    never below zero.

    One certificate is one tonne of CO2e (Article 3). The free allocation
    adjustment follows Article 31 and Implementing Regulation (EU) 2025/2620.
    The reduction for carbon price paid abroad follows Article 9, already
    converted into tCO2e-equivalent certificates; the conversion rules are set
    by implementing act. If the reductions exceed the embedded emissions the
    result is zero: no refund is due through this calculation.

    The result is not rounded. How the registry rounds is not modelled here.
    """
    for name, value in (("total_tco2e", total_tco2e),
                        ("free_allocation_adjustment_tco2e", free_allocation_adjustment_tco2e),
                        ("carbon_price_paid_tco2e", carbon_price_paid_tco2e)):
        _non_negative(name, value)
    per_cert = float((params or load_parameters())["certificate"]["tco2e_per_certificate"])
    return max(0.0, total_tco2e - free_allocation_adjustment_tco2e - carbon_price_paid_tco2e) / per_cert


def certificate_cost(certificates: float | Decimal, price_eur_per_tco2e: float | Decimal) -> Decimal:
    """Cost in EUR of buying certificates at one price, rounded to the cent.

    The certificate price is set under Article 21: the quarterly average of
    EU ETS auction clearing prices for 2026 imports, and the weekly average
    from 2027. Use the price for the period you buy in. Decimal arithmetic is
    used so the result matches a hand calculation to the cent.
    """
    certs = Decimal(str(certificates))
    price = Decimal(str(price_eur_per_tco2e))
    if certs < 0 or price < 0:
        raise ValueError("certificates and price must be zero or more")
    return (certs * price).quantize(CENT, rounding=ROUND_HALF_UP)


def quarterly_holding(
    embedded_tco2e_ytd: float,
    year: int,
    free_allocation_adjustment_tco2e_ytd: float = 0.0,
    params: dict[str, Any] | None = None,
) -> float:
    """Minimum certificates to hold on the registry account at a quarter end.

    Article 22(2) as amended by Regulation (EU) 2025/2083: from 2027, at the
    end of each quarter the declarant holds certificates for at least 50% of
    the embedded emissions in goods imported since the start of the calendar
    year, taking into account the free allocation adjustment.

        required = 50% x max(0, embedded emissions YTD - free allocation adjustment YTD)

    ``embedded_tco2e_ytd`` should be measured as the article allows: default
    values without mark-up, or based on the previous year's surrendered
    certificates. Before 2027 the rule does not apply and the result is 0.
    """
    _non_negative("embedded_tco2e_ytd", embedded_tco2e_ytd)
    _non_negative("free_allocation_adjustment_tco2e_ytd", free_allocation_adjustment_tco2e_ytd)
    p = params or load_parameters()
    rule = p["quarterly_holding"]
    if year < int(rule["from_year"]):
        return 0.0
    per_cert = float(p["certificate"]["tco2e_per_certificate"])
    net = max(0.0, embedded_tco2e_ytd - free_allocation_adjustment_tco2e_ytd)
    return float(rule["min_share"]) * net / per_cert
