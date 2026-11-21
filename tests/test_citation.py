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
