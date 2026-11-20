"""Recompute the VSME worked examples (V1-V6) and check the generated datapoint tables.

The fictional data lives in data/examples/gozo_fresh_foods.yml (block `vsme`) and
the datapoints in data/vsme_datapoints.yml.
"""
import importlib.util
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = yaml.safe_load((ROOT / "data/examples/gozo_fresh_foods.yml").read_text(encoding="utf-8"))
VSME = EXAMPLE["vsme"]
POINTS = yaml.safe_load((ROOT / "data/vsme_datapoints.yml").read_text(encoding="utf-8"))["datapoints"]

spec = importlib.util.spec_from_file_location("build_pages", ROOT / "scripts/build_pages.py")
bp = importlib.util.module_from_spec(spec)
sys.modules["build_pages"] = bp
spec.loader.exec_module(bp)


def raw(name: str) -> str:
    return (ROOT / "docs/vsme" / name).read_text(encoding="utf-8")


def page(name: str) -> str:
    return " ".join(raw(name).split())


# --- generated tables ------------------------------------------------------

def test_every_generated_table_matches_the_data() -> None:
    for path in sorted((ROOT / "docs/vsme").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        for m in bp.VSME_START.finditer(text):
            body = text[m.end():text.index(bp.VSME_END, m.end())].strip()
            assert body == bp.render_vsme_datapoints(POINTS, m.group("filter").strip()), (path.name, m.group("filter"))


def test_table_filters() -> None:
    import pytest

    assert bp.render_vsme_datapoints(POINTS, "disclosures=B3").count("| B3-") == 5
    with pytest.raises(ValueError):
        bp.render_vsme_datapoints(POINTS, "module=extra")
    with pytest.raises(ValueError):
        bp.render_vsme_datapoints(POINTS, "colour=green")


# --- V1 Choosing the modules -----------------------------------------------

def _option(requests: list[dict]) -> str:
    """Option B if any request needs a Comprehensive (C) disclosure, otherwise Option A."""
    return "B" if any(d.startswith("C") for r in requests for d in r["disclosures"]) else "A"


def test_v1_requests_and_option() -> None:
    text = page("v1-modules.md")
    for r in VSME["requests"]:
        row = f"| {r['from']} | {r['asks']} | {', '.join(r['disclosures'])} |"
        assert row in text, row
        known = {p["disclosure"] for p in POINTS}
        assert set(r["disclosures"]) <= known
    assert _option(VSME["requests"]) == VSME["option"] == "B"
    basic = sum(p["module"] == "basic" for p in POINTS)
    comprehensive = sum(p["module"] == "comprehensive" for p in POINTS)
    assert (basic, comprehensive) == (22, 9)
    assert (f"chooses **Option {VSME['option']}**: the Basic Module ({basic} datapoints) plus the "
            f"Comprehensive Module ({comprehensive} disclosures)") in text
    c_needed = sorted({d for r in VSME["requests"] for d in r["disclosures"] if d.startswith("C")})
    assert c_needed == ["C3", "C4"] and "need **C3** and **C4**" in text


def test_v1_scope3_request_is_beyond_basic() -> None:
    # B3 has no Scope 3 datapoint: the supermarket's Scope 3 request goes beyond the Basic Module
    b3 = [p["id"] for p in POINTS if p["disclosure"] == "B3"]
    assert not any("scope3" in i for i in b3)
    assert "asks for **Scope 3**, which the Basic Module does not require" in page("v1-modules.md")
