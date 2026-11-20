import subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_build_pages_and_check_pass():
    subprocess.run([sys.executable, "scripts/build_pages.py"], cwd=ROOT, check=True)
    r = subprocess.run([sys.executable, "scripts/check_workflows.py"], cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stdout
