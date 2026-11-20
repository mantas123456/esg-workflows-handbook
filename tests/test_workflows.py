import subprocess, sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_build_pages_and_check_pass():
    subprocess.run([sys.executable, "scripts/build_pages.py"], cwd=ROOT, check=True)
    r = subprocess.run([sys.executable, "scripts/check_workflows.py"], cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stdout


def test_every_cited_fact_id_exists() -> None:
    """A page's Sources line names fact ids; each must be in data/regulations.yml."""
    import re

    ids = {r["id"] for r in yaml.safe_load((ROOT / "data/regulations.yml").read_text(encoding="utf-8"))}
    checked = set()
    for page in sorted((ROOT / "docs").rglob("*.md")):
        m = re.search(r"Facts come from `data/regulations.yml` \(ids? (.*?)\)", page.read_text(encoding="utf-8"), re.S)
        if not m:
            continue
        cited = set(re.findall(r"`([a-z0-9-]+)`", m.group(1)))
        assert cited and cited <= ids, (page.name, sorted(cited - ids))
        checked.add(page.name)
    csrd = {p.name for p in (ROOT / "docs/csrd").glob("c*.md")}
    assert len(csrd) == 9 and csrd <= checked                             # every CSRD page names its facts
