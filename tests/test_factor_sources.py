"""data/factor_sources.yml is complete and its republish rule is consistent."""
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SOURCES = yaml.safe_load((ROOT / "data/factor_sources.yml").read_text(encoding="utf-8"))["sources"]
REQUIRED = {"id", "name", "publisher", "version", "year", "coverage", "method", "unit_basis",
            "licence", "licence_status", "republish", "url", "notes"}


def test_every_source_is_complete() -> None:
    ids = [s["id"] for s in SOURCES]
    assert len(ids) == len(set(ids))
    for s in SOURCES:
        assert REQUIRED <= set(s), s["id"]
        assert s["url"].startswith("https://"), s["id"]
        assert s["method"] in {"spend_based", "average_data", "supplier_specific"}, s["id"]


def test_republish_needs_a_verified_licence() -> None:
    for s in SOURCES:
        assert s["licence_status"] in {"verified", "unverified"}, s["id"]
        assert s["republish"] in {"yes", "no", "check"}, s["id"]
        if s["licence_status"] == "unverified":
            assert s["republish"] == "check", f"{s['id']}: an unread licence cannot allow or forbid republishing"
        if s["republish"] == "yes":
            assert s["licence_status"] == "verified", s["id"]


def test_licensed_and_non_commercial_sources_are_never_republished() -> None:
    by_id = {s["id"]: s for s in SOURCES}
    assert by_id["ecoinvent"]["republish"] == "no"
    assert by_id["exiobase-3"]["republish"] == "no"
