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
        assert p["basis"] in {"oj", "oj-topic"}, p["id"]
        assert (p["dr"] is None) == (p["basis"] == "oj-topic"), p["id"]
        assert p["id"].split("-")[0] == p["standard"].replace(" ", ""), p["id"]
        prefixes = ("BP-", "GOV-", "SBM-", "IRO-") if p["standard"] == "ESRS 2" else (p["standard"] + "-",)
        assert p["dr"] is None or p["dr"].startswith(prefixes), p["id"]
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


# Disclosure requirement codes and titles read in Delegated Regulation (EU) 2026/1563 (OJ L, 21.9.2026).
OJ_DRS = {
    "BP-1": "Basis for preparation of the sustainability statement",
    "GOV-1": "The role of the administrative, management and supervisory bodies",
    "SBM-1": "Strategy, business model and value chain",
    "IRO-1": "Description of the process to identify and assess material impacts, risks and opportunities",
    "E1-1": "Transition plan for climate change mitigation", "E1-6": "Targets related to climate change",
    "E1-7": "Energy consumption and mix", "E1-8": "Gross scope 1, 2, 3 GHG emissions",
    "E1-11": "Anticipated financial effects from material physical and transition risks",
    "E2-4": "Pollution of air, water and soil", "E2-5": "Substances of concern and substances of very high concern",
    "E3-4": "Water metrics", "E4-5": "Metrics related to biodiversity and ecosystems change",
    "E5-5": "Resource outflows", "S1-5": "Characteristics of the undertaking's employees",
    "S1-13": "Health and safety metrics", "G1-4": "Metrics related to corruption or bribery",
}


def test_every_code_is_a_real_disclosure_requirement() -> None:
    used = {p["dr"] for p in POINTS if p["dr"]}
    assert used == set(OJ_DRS)
    by_id = {p["id"]: p for p in POINTS}
    assert by_id["S1-health-safety"]["dr"] == "S1-13"                    # S1-14 is work-life balance
    assert {by_id[i]["dr"] for i in ("E1-scope1", "E1-scope2", "E1-scope3", "E1-scope3-suppliers")} == {"E1-8"}
    assert "location-based and a market-based" in REGS["esrs-e1-scope2"]["fact"]
