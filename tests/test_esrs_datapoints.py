"""data/esrs_datapoints.yml is complete, linked to real datasets and consistent with the ESRS facts."""
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
POINTS = yaml.safe_load((ROOT / "data/esrs_datapoints.yml").read_text(encoding="utf-8"))["datapoints"]
DATASETS = {d["name"] for d in yaml.safe_load((ROOT / "data/datasets.yml").read_text(encoding="utf-8"))["datasets"]}
REGS = {r["id"]: r for r in yaml.safe_load((ROOT / "data/regulations.yml").read_text(encoding="utf-8"))}
STANDARDS = {"ESRS 2", "E1", "E2", "E3", "E4", "E5", "S1", "S2", "S3", "S4", "G1"}
REQUIRED = {"id", "standard", "dr", "description", "unit", "dataset", "basis"}


def test_every_datapoint_is_complete_and_unique() -> None:
    ids = [p["id"] for p in POINTS]
    assert len(ids) == len(set(ids))
    for p in POINTS:
        assert set(p) == REQUIRED, p["id"]
        assert p["standard"] in STANDARDS, p["id"]
        assert p["basis"] in {"efrag-kh", "title"}, p["id"]
        assert p["id"].split("-")[0] == p["standard"].replace(" ", ""), p["id"]
        assert p["dr"] is None or p["dr"].startswith(p["standard"] + "-"), p["id"]
        assert p["description"] and p["unit"], p["id"]


def test_every_topical_standard_and_esrs2_is_covered() -> None:
    assert {p["standard"] for p in POINTS} == STANDARDS
    assert "12 standards" in REGS["esrs-structure"]["fact"]


def test_linked_datasets_exist_and_e1_reuses_the_handbook_data() -> None:
    for p in POINTS:
        assert p["dataset"] is None or p["dataset"] in DATASETS, p["id"]
    e1 = {p["dataset"] for p in POINTS if p["standard"] == "E1" and p["dataset"]}
    assert {"electricity_use", "fuel_use", "purchased_goods_spend", "supplier_emissions"} <= e1


def test_consistent_with_the_facts() -> None:
    by_id = {p["id"]: p for p in POINTS}
    assert "each significant" in by_id["E1-scope3"]["description"]
    assert "for each significant Scope 3 category" in REGS["esrs-e1-scope3"]["fact"]
    # the phase-in topics named in the fact are flagged on their datapoints
    for pid in ("E4-biodiversity", "S2-value-chain-workers", "S3-communities", "S4-consumers",
                "E1-financial-effects", "E2-substances-of-concern"):
        assert "phase-in applies" in by_id[pid]["description"], pid
    assert "No phase-in specific to Scope 3" in REGS["esrs-phase-in"]["fact"]
    assert "phase-in" not in by_id["E1-scope3"]["description"]
