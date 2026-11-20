"""Organisational boundary: consolidate entity emissions under one approach.

GHG Protocol Corporate Standard (cited, not copied): equity share, financial
control or operational control. Under a control approach an entity counts
100% or 0%; under equity share it counts in proportion to the equity held.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable, Literal

Approach = Literal["equity_share", "financial_control", "operational_control"]
APPROACHES: tuple[Approach, ...] = ("equity_share", "financial_control", "operational_control")


@dataclass(frozen=True)
class Entity:
    name: str
    scope12_tco2e: float
    """The entity's own Scope 1 and 2 emissions at 100%."""
    equity_share: float
    """0 to 1."""
    financial_control: bool
    operational_control: bool

    def __post_init__(self) -> None:
        if not 0 <= self.equity_share <= 1:
            raise ValueError(f"{self.name}: equity_share must be 0 to 1")
        if self.scope12_tco2e < 0:
            raise ValueError(f"{self.name}: scope12_tco2e must be zero or more")

    def share_included(self, approach: Approach) -> float:
        """Fraction of this entity's emissions inside the boundary (0 to 1)."""
        if approach == "equity_share":
            return self.equity_share
        if approach == "financial_control":
            return 1.0 if self.financial_control else 0.0
        if approach == "operational_control":
            return 1.0 if self.operational_control else 0.0
        raise ValueError(f"unknown approach {approach!r}")


@dataclass(frozen=True)
class Consolidated:
    approach: Approach
    tco2e: float
    by_entity: dict[str, float]
    outside: list[str]
    """Entities left fully outside the boundary: their emissions linked to your
    activities may belong in Scope 3."""


def consolidate(entities: Iterable[Entity], approach: Approach) -> Consolidated:
    """Scope 1 and 2 emissions inside the organisational boundary for one approach."""
    if approach not in APPROACHES:
        raise ValueError(f"unknown approach {approach!r}")
    ents = list(entities)
    names = [e.name for e in ents]
    if len(names) != len(set(names)):
        raise ValueError("entity names must be unique")
    by_entity = {e.name: e.scope12_tco2e * e.share_included(approach) for e in ents}
    return Consolidated(approach=approach, tco2e=math.fsum(by_entity.values()), by_entity=by_entity,
                        outside=[e.name for e in ents if e.share_included(approach) == 0])
