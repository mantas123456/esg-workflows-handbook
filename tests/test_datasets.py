"""data/datasets.yml is valid, rendered into F3, and the F3 worked example adds up."""
import importlib.util
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("build_pages", ROOT / "scripts/build_pages.py")
bp = importlib.util.module_from_spec(spec)
sys.modules["build_pages"] = bp
spec.loader.exec_module(bp)

DATA = yaml.safe_load((ROOT / "data/datasets.yml").read_text(encoding="utf-8"))
PAGE_PATH = ROOT / "docs/foundations/one-dataset-many-reports.md"
REQUIRED = {"name", "title", "unit", "owner_role", "frequency", "used_by", "note"}


def test_every_dataset_is_complete() -> None:
    names = [d["name"] for d in DATA["datasets"]]
    assert len(names) == len(set(names))
    for d in DATA["datasets"]:
        assert REQUIRED <= set(d), d["name"]
        assert d["used_by"] and set(d["used_by"]) <= set(DATA["reports"]), d["name"]


def test_page_table_is_in_sync() -> None:
    bp.main()
    page = PAGE_PATH.read_text(encoding="utf-8")
    assert f"{bp.DATASETS_START}\n{bp.render_datasets(DATA)}\n{bp.DATASETS_END}" in page
    for d in DATA["datasets"]:
        assert f"`{d['name']}`" in page


def test_unknown_report_is_rejected() -> None:
    bad = {"reports": {"cbam": "CBAM"}, "datasets": [{**DATA["datasets"][0], "used_by": ["nope"]}]}
    with pytest.raises(ValueError, match="nope"):
        bp.render_datasets(bad)


def test_mermaid_matches_datasets() -> None:
    """Every arrow in the diagram matches a tick in datasets.yml, and vice versa."""
    page = PAGE_PATH.read_text(encoding="utf-8")
    node = {"electricity_use": "E", "fuel_use": "F", "purchased_goods_spend": "P",
            "supplier_emissions": "S", "imports_by_cn_code": "I", "headcount": "H"}
    report = {"cbam": "CBAM", "scope3": "S3", "vsme": "V", "esrs-e1": "E1"}
    expected = {f"{node[d['name']]} --> {report[r]}" for d in DATA["datasets"] for r in d["used_by"]}
    block = page.split("```mermaid", 1)[1].split("```", 1)[0]
    arrows = {line.strip() for line in block.splitlines() if "-->" in line}
    assert arrows == expected


def test_worked_example_counts() -> None:
    page = " ".join(PAGE_PATH.read_text(encoding="utf-8").split())
    n_datasets = len(DATA["datasets"])
    n_uses = sum(len(d["used_by"]) for d in DATA["datasets"])
    assert (n_datasets, n_uses) == (6, 15)
    assert f"names **{n_datasets}** datasets" in page
    assert f"in **{n_uses}** places" in page
    assert "Six core datasets feed four reports" in page
