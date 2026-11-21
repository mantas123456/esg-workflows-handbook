"""Check how long ago each regulatory fact was last checked.

Every fact in data/regulations.yml has a ``last_checked`` date. This script
warns when a fact has not been re-checked for 90 days and fails (exit code 1)
at 180 days, so CI stops the site from going on stating stale rules. Page
front matter ``last_checked`` dates are reported the same way, as warnings only.

    python scripts/check_regulations.py                # today
    python scripts/check_regulations.py --today 2027-06-01
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
WARN_DAYS = 90
FAIL_DAYS = 180


@dataclass(frozen=True)
class Age:
    item: str
    last_checked: date
    days: int

    @property
    def level(self) -> str:
        """'ok', 'warn' (90 days or more) or 'fail' (180 days or more)."""
        if self.days >= FAIL_DAYS:
            return "fail"
        if self.days >= WARN_DAYS:
            return "warn"
        return "ok"


def fact_ages(today: date, path: Path = ROOT / "data" / "regulations.yml") -> list[Age]:
    facts = yaml.safe_load(path.read_text(encoding="utf-8"))
    out = []
    for f in facts:
        checked = f.get("last_checked")
        if not isinstance(checked, date):
            raise ValueError(f"fact {f.get('id')!r} has no valid last_checked date")
        out.append(Age(f["id"], checked, (today - checked).days))
    return out


def page_ages(today: date, docs: Path = ROOT / "docs") -> list[Age]:
    out = []
    for page in sorted(docs.rglob("*.md")):
        m = re.search(r"^last_checked: (\d{4}-\d{2}-\d{2})\s*$", page.read_text(encoding="utf-8"), re.M)
        if m:
            checked = date.fromisoformat(m.group(1))
            out.append(Age(page.relative_to(docs).as_posix(), checked, (today - checked).days))
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--today", type=date.fromisoformat, default=date.today(), help="YYYY-MM-DD (default: today)")
    args = parser.parse_args(argv)

    facts = fact_ages(args.today)
    pages = page_ages(args.today)
    failed = [a for a in facts if a.level == "fail"]
    for a in sorted(facts, key=lambda a: -a.days):
        if a.level != "ok":
            word = "FAIL" if a.level == "fail" else "WARNING"
            print(f"{word}: fact '{a.item}' last checked {a.last_checked} ({a.days} days ago)")
    for a in sorted(pages, key=lambda a: -a.days):
        if a.level != "ok":
            print(f"WARNING: page {a.item} last checked {a.last_checked} ({a.days} days ago)")
    warned = sum(a.level == "warn" for a in facts)
    print(f"{len(facts)} facts checked on {args.today}: {len(failed)} over {FAIL_DAYS} days, "
          f"{warned} over {WARN_DAYS} days")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
