"""Citation metadata: .zenodo.json (read by Zenodo) agrees with CITATION.cff (read by GitHub)."""
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_zenodo_json_matches_citation_cff() -> None:
    zen = json.loads((ROOT / ".zenodo.json").read_text(encoding="utf-8"))
    cff = yaml.safe_load((ROOT / "CITATION.cff").read_text(encoding="utf-8"))
    assert zen["title"] == cff["title"]
    author = cff["authors"][0]
    assert zen["creators"] == [{"name": f"{author['family-names']}, {author['given-names']}"}]
    assert zen["license"] == cff["license"][0].lower()          # one licence for Zenodo: the handbook text
    assert zen["upload_type"] == cff["type"] == "software"
    assert set(cff["keywords"]) <= set(zen["keywords"])
    assert "version" not in zen                                  # Zenodo takes the version from the release tag


def test_concept_doi_is_the_same_everywhere() -> None:
    doi = "10.5281/zenodo.24423578"                              # Zenodo concept DOI (all versions)
    cff = yaml.safe_load((ROOT / "CITATION.cff").read_text(encoding="utf-8"))
    assert cff["doi"] == doi and cff["identifiers"][0]["value"] == doi
    for path in ("README.md", "docs/about.md"):
        text = (ROOT / path).read_text(encoding="utf-8")
        assert f"https://doi.org/{doi}" in text, path
