"""Data quality and uncertainty for emissions data.

Emissions are treated as measurements: every line gets a data-quality score
and a stated uncertainty, and totals carry both.

- Data quality: five indicators (technology, time, geography, completeness,
  reliability), each scored 1 (very good) to 5 (very poor). These are the
  indicators the GHG Protocol Scope 3 Standard names for assessing data
  quality; the 1-5 scale follows the common "pedigree matrix" convention.
  Neither source is copied here.
- Uncertainty, analytic: first-order propagation for independent inputs
  (sums add absolute uncertainties in quadrature; products add relative ones).
- Uncertainty, Monte Carlo: lognormal factors, seeded, so results repeat.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, fields
from typing import Iterable, Sequence

INDICATORS = ("technology", "time", "geography", "completeness", "reliability")


# --- data quality ----------------------------------------------------------

@dataclass(frozen=True)
class DataQuality:
    """Scores for one line: 1 = very good, 5 = very poor."""
    technology: int
    time: int
    geography: int
    completeness: int
    reliability: int

    def __post_init__(self) -> None:
        for f in fields(self):
            v = getattr(self, f.name)
            if not isinstance(v, int) or isinstance(v, bool) or not 1 <= v <= 5:
                raise ValueError(f"{f.name} must be a whole number from 1 to 5, got {v!r}")

    def score(self, weights: dict[str, float] | None = None) -> float:
        """Weighted mean of the five indicators (equal weights by default)."""
        w = weights or {name: 1.0 for name in INDICATORS}
        if set(w) != set(INDICATORS) or any(v < 0 for v in w.values()) or not sum(w.values()) > 0:
            raise ValueError(f"weights must give a non-negative value for each of {INDICATORS}")
        return math.fsum(getattr(self, k) * w[k] for k in INDICATORS) / math.fsum(w.values())


def category_score(items: Iterable[tuple[float, DataQuality]], weights: dict[str, float] | None = None) -> float:
    """Emissions-weighted data-quality score of a category: sum(tCO2e x score) / sum(tCO2e).

    Lines with more emissions count more, so a poor estimate for a large line
    is not hidden by many good small ones.
    """
    pairs = [(t, q.score(weights)) for t, q in items]
    for t, _ in pairs:
        if t < 0:
            raise ValueError("tCO2e must be zero or more")
    total = math.fsum(t for t, _ in pairs)
    if total == 0:
        raise ValueError("no emissions to weight the score")
    return math.fsum(t * s for t, s in pairs) / total


# --- analytic uncertainty --------------------------------------------------

@dataclass(frozen=True)
class Uncertain:
    value: float
    u95_abs: float
    """Half-width of the 95% interval, in the unit of ``value``."""

    @property
    def u95_rel(self) -> float:
        return self.u95_abs / abs(self.value) if self.value else math.inf


def sum_uncertainty(values: Sequence[float], u95_rel: Sequence[float]) -> Uncertain:
    """Total of independent values and its 95% half-width.

    ``U_total = sqrt(sum((value_i x u_i)^2))``. Valid for independent inputs;
    correlated inputs (the same factor used on many lines) need Monte Carlo
    or a covariance term.
    """
    if len(values) != len(u95_rel):
        raise ValueError("values and u95_rel must have the same length")
    for u in u95_rel:
        if u < 0:
            raise ValueError("u95_rel must be zero or more")
    total = math.fsum(values)
    u_abs = math.sqrt(math.fsum((v * u) ** 2 for v, u in zip(values, u95_rel)))
    return Uncertain(total, u_abs)


def product_uncertainty(u95_rel: Sequence[float]) -> float:
    """Relative 95% half-width of a product of independent factors (activity x factor).

    ``u = sqrt(sum(u_i^2))``. A first-order approximation, good while each
    u_i is small (below about 30%); for larger ones, use Monte Carlo.
    """
    for u in u95_rel:
        if u < 0:
            raise ValueError("u95_rel must be zero or more")
    return math.sqrt(math.fsum(u * u for u in u95_rel))


def round_result(value: float, u95_abs: float, digits: int = 2) -> tuple[float, float]:
    """Round an uncertainty to ``digits`` significant figures, and the value to match.

    Common practice in measurement reports: 405.228 -> 410, so 4,845.0 -> 4,850.
    The uncertainty is rounded half up at its last kept digit (to the nearest
    value, not always upwards); some labs always round it up instead.
    """
    from decimal import ROUND_HALF_UP, Decimal

    if u95_abs <= 0:
        raise ValueError("u95_abs must be more than zero")
    u = Decimal(repr(u95_abs))
    exponent = u.adjusted() - (digits - 1)          # position of the last kept digit
    quantum = Decimal(1).scaleb(exponent)
    u_r = u.quantize(quantum, rounding=ROUND_HALF_UP) if exponent < 0 else \
        (u / quantum).quantize(Decimal(1), rounding=ROUND_HALF_UP) * quantum
    v = Decimal(repr(value))
    v_r = v.quantize(quantum, rounding=ROUND_HALF_UP) if exponent < 0 else \
        (v / quantum).quantize(Decimal(1), rounding=ROUND_HALF_UP) * quantum
    return float(v_r), float(u_r)


def variance_shares(values: Sequence[float], u95_rel: Sequence[float]) -> list[float]:
    """Each input's share of the combined variance (an uncertainty budget). Shares add to 1."""
    if len(values) != len(u95_rel):
        raise ValueError("values and u95_rel must have the same length")
    parts = [(v * u) ** 2 for v, u in zip(values, u95_rel)]
    total = math.fsum(parts)
    if total == 0:
        raise ValueError("no uncertainty to share")
    return [p / total for p in parts]


# --- Monte Carlo -----------------------------------------------------------

Z95 = 1.959964  # standard normal quantile for a 95% two-sided interval


def gsd_from_u95(u95_rel: float) -> float:
    """Geometric standard deviation of a lognormal whose 95% range reaches +u95_rel.

    A stated "+/-20%" becomes a lognormal with median 1 whose 97.5th percentile
    is 1.20: ``GSD = (1 + u)^(1 / 1.96)``. The lower end is then 1 / 1.20 = 0.833,
    not 0.80: the lognormal is skewed, as emission factors often are. A
    convention, not a rule; state it when you use it.
    """
    if u95_rel < 0:
        raise ValueError("u95_rel must be zero or more")
    return (1.0 + u95_rel) ** (1.0 / Z95)

@dataclass(frozen=True)
class MonteCarloResult:
    mean: float
    median: float
    low: float
    """2.5th percentile."""
    high: float
    """97.5th percentile."""
    n: int
    seed: int


def monte_carlo_sum(
    activities: Sequence[float],
    factor_medians: Sequence[float],
    factor_gsds: Sequence[float],
    *,
    n: int = 100_000,
    seed: int = 20260101,
) -> MonteCarloResult:
    """Total of ``activity_i x factor_i`` with lognormal factors, by simulation.

    Each factor is lognormal with the given median and geometric standard
    deviation (GSD): ``ln(factor) ~ Normal(ln(median), ln(GSD))``. A GSD of 1
    means no uncertainty; the 95% range of one factor is about
    median / GSD^1.96 to median x GSD^1.96. Activities are taken as exact.
    Factors are independent. Seeded, so the same inputs give the same result.

    Returns:
        mean, median and the 2.5th and 97.5th percentiles of the total, in the
        unit of ``activity x factor``.
    """
    import numpy as np

    if not (len(activities) == len(factor_medians) == len(factor_gsds)) or not activities:
        raise ValueError("give the same, non-zero number of activities, medians and GSDs")
    if n < 1000:
        raise ValueError("use at least 1,000 draws")
    for a, m, g in zip(activities, factor_medians, factor_gsds):
        if a < 0 or m <= 0 or g < 1:
            raise ValueError("activities must be >= 0, medians > 0 and GSDs >= 1")
    rng = np.random.default_rng(seed)
    a = np.asarray(activities, dtype=float)
    mu = np.log(np.asarray(factor_medians, dtype=float))
    sigma = np.log(np.asarray(factor_gsds, dtype=float))
    draws = rng.normal(mu, sigma, size=(n, len(a)))
    totals = (np.exp(draws) * a).sum(axis=1)
    low, median, high = np.percentile(totals, [2.5, 50, 97.5])
    return MonteCarloResult(mean=float(totals.mean()), median=float(median), low=float(low),
                            high=float(high), n=n, seed=seed)
