"""Double materiality assessment (DMA): score impacts, risks and opportunities.

Follows the method the revised ESRS describe in ESRS 1 chapter 3 (Delegated
Regulation (EU) 2026/1563, Annex I), cited, not copied:

- impact materiality: severity from scale, scope and irremediable character
  (any one can make a negative impact severe); actual negative impacts on
  severity; potential negative impacts on severity and likelihood, with
  severity taking precedence for human rights impacts; positive impacts on
  scale and scope, plus likelihood if potential;
- financial materiality: whether a topic triggers, or could reasonably be
  expected to trigger, material financial effects, scored here on magnitude
  and likelihood.

The ESRS state principles, not a formula. Every number this module needs
(scale, how severity is combined, how likelihood is applied, the human-rights
cut-off, the thresholds) comes from data/dma_parameters.yml, where each is
marked as an ESRS rule or a handbook choice. Prevention and mitigation must
already be reflected in the inputs, and only if implemented and effective.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable, Literal

import yaml

PARAMETERS_PATH = Path(__file__).resolve().parents[1] / "data" / "dma_parameters.yml"

Kind = Literal["impact", "risk", "opportunity"]


@lru_cache(maxsize=None)
def _load(path: str) -> dict[str, Any]:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def load_parameters(path: Path | None = None) -> dict[str, Any]:
    return _load(str(path or PARAMETERS_PATH))


@dataclass(frozen=True)
class IRO:
    """One impact, risk or opportunity. Scores are whole numbers on the parameter scale.

    Impacts use ``negative``, ``actual``, ``human_rights``, ``scale``, ``scope``,
    ``irremediability`` (negative only) and ``likelihood`` (potential only).
    Risks and opportunities use ``magnitude`` and ``likelihood``.
    """
    id: str
    topic: str
    """ESRS topical standard, e.g. E1 or S1."""
    description: str
    kind: Kind
    negative: bool = True
    actual: bool = False
    human_rights: bool = False
    scale: int | None = None
    scope: int | None = None
    irremediability: int | None = None
    likelihood: int | None = None
    magnitude: int | None = None


@dataclass(frozen=True)
class Assessed:
    iro: IRO
    score: float
    material: bool
    dimension: Literal["impact", "financial"]
    explanation: str


@dataclass(frozen=True)
class TopicResult:
    topic: str
    impact_material: bool
    financial_material: bool
    iros: list[str] = field(default_factory=list)

    @property
    def material(self) -> bool:
        """Double materiality: material from either perspective."""
        return self.impact_material or self.financial_material


def _check(name: str, value: int | None, p: dict[str, Any], iro: IRO) -> int:
    lo, hi = p["scale"]["min"], p["scale"]["max"]
    if value is None:
        raise ValueError(f"{iro.id}: {name} is needed for this kind of IRO")
    if not isinstance(value, int) or isinstance(value, bool) or not lo <= value <= hi:
        raise ValueError(f"{iro.id}: {name} must be a whole number from {lo} to {hi}, got {value!r}")
    return value


def severity(iro: IRO, params: dict[str, Any] | None = None) -> float:
    """Severity of a negative impact: scale, scope and irremediability combined.

    With ``severity_aggregation: max`` (default) the highest of the three, because
    any one can make an impact severe; with ``mean`` their average.
    """
    p = params or load_parameters()
    values = [_check(n, getattr(iro, n), p, iro) for n in ("scale", "scope", "irremediability")]
    how = p["severity_aggregation"]
    if how == "max":
        return float(max(values))
    if how == "mean":
        return sum(values) / 3
    raise ValueError(f"unknown severity_aggregation {how!r}")


def assess(iro: IRO, params: dict[str, Any] | None = None) -> Assessed:
    """Score one IRO and decide whether it is material."""
    p = params or load_parameters()
    top = p["scale"]["max"]
    if iro.kind == "impact":
        if iro.negative:
            sev = severity(iro, p)
            if iro.actual:
                score, how = sev, f"actual negative: severity {sev:g}"
            else:
                lik = _check("likelihood", iro.likelihood, p, iro)
                if iro.human_rights and sev >= p["human_rights"]["severity_precedence_from"]:
                    score, how = sev, f"potential human rights impact: severity {sev:g} takes precedence over likelihood {lik}"
                else:
                    score, how = sev * lik / top, f"potential negative: severity {sev:g} x likelihood {lik} / {top}"
        else:
            base = (_check("scale", iro.scale, p, iro) + _check("scope", iro.scope, p, iro)) / 2
            if iro.actual:
                score, how = base, f"actual positive: mean of scale and scope {base:g}"
            else:
                lik = _check("likelihood", iro.likelihood, p, iro)
                score, how = base * lik / top, f"potential positive: {base:g} x likelihood {lik} / {top}"
        threshold = float(p["thresholds"]["impact"])
        return Assessed(iro, score, score >= threshold, "impact", how)
    if iro.kind in ("risk", "opportunity"):
        mag = _check("magnitude", iro.magnitude, p, iro)
        lik = _check("likelihood", iro.likelihood, p, iro)
        score = mag * lik / top
        threshold = float(p["thresholds"]["financial"])
        return Assessed(iro, score, score >= threshold, "financial", f"magnitude {mag} x likelihood {lik} / {top}")
    raise ValueError(f"{iro.id}: unknown kind {iro.kind!r}")


def assess_all(iros: Iterable[IRO], params: dict[str, Any] | None = None) -> list[Assessed]:
    """Assess every IRO and rank them: material first, then by score, then by id."""
    items = list(iros)
    ids = [i.id for i in items]
    if len(ids) != len(set(ids)):
        raise ValueError("IRO ids must be unique")
    out = [assess(i, params) for i in items]
    return sorted(out, key=lambda a: (not a.material, -a.score, a.iro.id))


def topics(assessed: Iterable[Assessed]) -> list[TopicResult]:
    """Roll the assessed IROs up to topics: material from the impact side, the financial side, or both."""
    by: dict[str, dict[str, Any]] = {}
    for a in assessed:
        t = by.setdefault(a.iro.topic, {"impact": False, "financial": False, "iros": []})
        t["iros"].append(a.iro.id)
        if a.material:
            t[a.dimension] = True
    return [TopicResult(k, v["impact"], v["financial"], sorted(v["iros"])) for k, v in sorted(by.items())]
