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


# --- Monte Carlo -----------------------------------------------------------

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
