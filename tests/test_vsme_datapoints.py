"""data/vsme_datapoints.yml is complete, consistent with data/datasets.yml and with the VSME facts."""
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
POINTS = yaml.safe_load((ROOT / "data/vsme_datapoints.yml").read_text(encoding="utf-8"))["datapoints"]
DATASETS = {d["name"] for d in yaml.safe_load((ROOT / "data/datasets.yml").read_text(encoding="utf-8"))["datasets"]}
REGS = {r["id"]: r for r in yaml.safe_load((ROOT / "data/regulations.yml").read_text(encoding="utf-8"))}
REQUIRED = {"id", "module", "disclosure", "description", "unit", "dataset", "basis", "cap"}
CAP = {d["id"]: d for d in yaml.safe_load((ROOT / "data/value_chain_cap.yml").read_text(encoding="utf-8"))["datapoints"]}


def test_every_datapoint_is_complete_and_unique() -> None:
    ids = [p["id"] for p in POINTS]
    assert len(ids) == len(set(ids))
    for p in POINTS:
        assert set(p) == REQUIRED, p["id"]
        assert p["module"] in {"basic", "comprehensive"}, p["id"]
        assert p["basis"] in {"act", "rec-2025", "title"}, p["id"]
        assert p["id"].startswith(p["disclosure"] + "-"), p["id"]
        assert p["description"] and p["unit"], p["id"]


def test_every_disclosure_b1_to_b11_and_c1_to_c9_is_listed() -> None:
    disclosures = {p["disclosure"] for p in POINTS}
    assert disclosures == {f"B{i}" for i in range(1, 12)} | {f"C{i}" for i in range(1, 10)}
    for p in POINTS:
        assert (p["module"] == "basic") == p["disclosure"].startswith("B"), p["id"]


def test_linked_datasets_exist() -> None:
    for p in POINTS:
        assert p["dataset"] is None or p["dataset"] in DATASETS, p["id"]
    # the datasets VSME energy, emissions and workforce rely on are all linked
    linked = {p["dataset"] for p in POINTS if p["dataset"]}
    assert {"electricity_use", "fuel_use", "headcount"} <= linked


def test_consistent_with_the_vsme_facts() -> None:
    assert "2026/1560" in REGS["vsme"]["fact"]
    assert "B1 to B11" in REGS["vsme-modules"]["fact"] and "C1 to C9" in REGS["vsme-modules"]["fact"]
    by_id = {p["id"]: p for p in POINTS}
    # B3 asks for location-based Scope 2 and no Scope 3 in the Basic Module
    assert "B3-scope2-location" in by_id and not any("scope3" in i for i in by_id if i.startswith("B"))
    assert "Scope 3 is not required in the Basic Module" in REGS["vsme-basic-metrics"]["fact"]
    # titles the 2026 act changed
    assert by_id["C7-human-rights-incidents"]["description"].startswith("Human rights incidents")
    assert by_id["C8-revenues"]["description"] == "Revenues from certain activities"


def test_cap_links_point_to_annex_ii() -> None:
    """Each datapoint names the Annex II rows of the value-chain cap it falls under, or none."""
    for p in POINTS:
        for c in p["cap"] or []:
            assert c in CAP, (p["id"], c)
            assert CAP[c]["disclosure"] == p["disclosure"], (p["id"], c)
    linked = {c for p in POINTS for c in (p["cap"] or [])}
    # Annex II rows with no datapoint in this list: general information (B1 27(e)), water withdrawal
    # (B6 36; the list has consumption), circular economy principles (B7 38) and minimum wage (B10 42(a))
    assert set(CAP) - linked == {"B1-27e", "B6-36", "B7-38", "B10-42a"}
    by_id = {p["id"]: p for p in POINTS}
    for outside in ("B10-pay-gap", "B11-corruption", "C3-targets", "C4-climate-risks", "B9-fatalities", "B6-water-consumption"):
        assert by_id[outside]["cap"] is None, outside
    ids = [d["id"] for d in CAP.values()]
    assert len(ids) == len(set(ids)) and all(d["small"] <= d["large"] for d in CAP.values())
