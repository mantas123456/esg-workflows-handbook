"""CI check: every step has a page with the right front matter, ids are unique,
and regulation facts have been re-checked in the last 90 days (warning only)."""
from datetime import date, timedelta
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
STATUSES = {"planned", "draft", "examples-checked", "reviewed"}
DRAFT_HEADINGS = ["## In one sentence", "## Steps", "## Worked example", "## Sources"]
TEMPLATES_MARKER = "<!-- generated from data/workflows.yml templates: do not edit by hand -->"


def main() -> int:
    errors: list[str] = []
    data = yaml.safe_load((ROOT / "data/workflows.yml").read_text(encoding="utf-8"))
    seen = set()
    for track in data["tracks"]:
        for step in track["steps"]:
            sid = step["id"]
            if sid in seen:
                errors.append(f"duplicate id {sid}")
            seen.add(sid)
            if step["status"] not in STATUSES:
                errors.append(f"{sid}: unknown status {step['status']}")
            page = ROOT / "docs" / track["folder"] / step["file"]
            if not page.exists():
                errors.append(f"{sid}: missing page {page.relative_to(ROOT)} (run scripts/build_pages.py)")
                continue
            text = page.read_text(encoding="utf-8")
            if f'step: "{sid}"' not in text:
                errors.append(f"{sid}: front matter does not name this step")
            if step["status"] != "planned":
                errors += [f"{sid}: missing heading '{h}'" for h in DRAFT_HEADINGS if h not in text]
                for tid in step.get("templates", []):
                    if not any((ROOT / "templates" / d / f"{tid}.{ext}").exists()
                               for d, ext in (("src", "md"), ("sheets", "yml"))):
                        errors.append(f"{sid}: template {tid} has no source in templates/")
                if step.get("templates") and TEMPLATES_MARKER not in text:
                    errors.append(f"{sid}: lists templates but the page has no generated download block")

    regs = yaml.safe_load((ROOT / "data/regulations.yml").read_text(encoding="utf-8"))
    for r in regs:
        if date.today() - r["last_checked"] > timedelta(days=90):
            print(f"WARNING: regulation fact '{r['id']}' last checked {r['last_checked']}")

    for e in errors:
        print(f"ERROR: {e}")
    print(f"{len(seen)} steps checked, {len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
