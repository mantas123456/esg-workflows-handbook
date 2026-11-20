"""Choosing and documenting emission factors.

Every factor used in an inventory is recorded with its source, version,
year, unit and licence. When several factors could be used for a line,
choose among those whose licence allows your use, the one with the best
data-quality score (esgcalc.quality.DataQuality: 1 = very good).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from esgcalc.quality import DataQuality


@dataclass(frozen=True)
class FactorOption:
    name: str
    source_id: str
    """Id in data/factor_sources.yml, or 'supplier' for a supplier's own figure."""
    version: str
    year: int
    unit: str
    quality: DataQuality
    licence_allows_use: bool
    """Does the licence allow *your* use (for example, a company's own inventory)?"""
    value: float | None = None

    def __post_init__(self) -> None:
        if not self.unit:
            raise ValueError(f"{self.name}: a factor needs a unit")
        if self.value is not None and self.value < 0:
            raise ValueError(f"{self.name}: value must be zero or more")


def choose_factor(options: Sequence[FactorOption]) -> FactorOption:
    """The usable option with the best (lowest) data-quality score.

    Options whose licence does not allow your use are skipped, however good
    their data. Ties go to the newer factor, then to the order given.
    """
    usable = [o for o in options if o.licence_allows_use]
    if not usable:
        raise ValueError("no option has a licence that allows your use")
    return min(usable, key=lambda o: (o.quality.score(), -o.year))


def age_years(option: FactorOption, reporting_year: int) -> int:
    """How many years older the factor is than the reporting year (0 if the same year)."""
    return max(0, reporting_year - option.year)
