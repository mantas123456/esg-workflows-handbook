"""Build or verify an evidence register of SHA-256 hashes for a folder.

Usage:
    python scripts/hash_evidence.py build  EVIDENCE_FOLDER [--register PATH]
    python scripts/hash_evidence.py verify EVIDENCE_FOLDER [--register PATH]

`build` walks the folder and writes a CSV with one row per file:
path, sha256, size, modified, note. Paths are relative to the folder and use
forward slashes. Notes from an existing register are kept for files that are
still there. The register file itself is skipped.

`verify` re-hashes every file and compares with the register. It prints
files that changed, went missing or are not yet registered, and exits with
code 1 if any are found. Runs offline; nothing leaves your machine.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_REGISTER = "evidence_register.csv"
FIELDS = ["path", "sha256", "size", "modified", "note"]
CHUNK_BYTES = 1024 * 1024


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(CHUNK_BYTES):
            digest.update(chunk)
    return digest.hexdigest()


def iter_files(folder: Path, register: Path) -> list[Path]:
    reg = register.resolve()
    return sorted(p for p in folder.rglob("*") if p.is_file() and p.resolve() != reg)


def read_register(register: Path) -> dict[str, dict[str, str]]:
    if not register.exists():
        return {}
    with register.open(newline="", encoding="utf-8") as f:
        return {row["path"]: row for row in csv.DictReader(f)}


def build(folder: Path, register: Path) -> int:
    old = read_register(register)
    rows = []
    for p in iter_files(folder, register):
        rel = p.relative_to(folder).as_posix()
        stat = p.stat()
        rows.append({
            "path": rel,
            "sha256": sha256_of(p),
            "size": str(stat.st_size),
            "modified": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(timespec="seconds"),
            "note": old.get(rel, {}).get("note", ""),
        })
    register.parent.mkdir(parents=True, exist_ok=True)
    with register.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"{len(rows)} files written to {register}")
    return 0


@dataclass
class VerifyResult:
    changed: list[str]
    missing: list[str]
    unregistered: list[str]

    @property
    def ok(self) -> bool:
        return not (self.changed or self.missing or self.unregistered)


def verify(folder: Path, register: Path) -> VerifyResult:
    if not register.exists():
        raise FileNotFoundError(f"register not found: {register}")
    expected = read_register(register)
    actual = {p.relative_to(folder).as_posix(): p for p in iter_files(folder, register)}
    return VerifyResult(
        changed=sorted(r for r in expected if r in actual and sha256_of(actual[r]) != expected[r]["sha256"]),
        missing=sorted(r for r in expected if r not in actual),
        unregistered=sorted(r for r in actual if r not in expected),
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=["build", "verify"])
    parser.add_argument("folder", type=Path)
    parser.add_argument("--register", type=Path, help=f"CSV path (default: FOLDER/{DEFAULT_REGISTER})")
    args = parser.parse_args(argv)

    folder: Path = args.folder.resolve()
    if not folder.is_dir():
        print(f"ERROR: not a folder: {folder}")
        return 2
    register: Path = args.register or folder / DEFAULT_REGISTER

    if args.command == "build":
        return build(folder, register)

    try:
        result = verify(folder, register)
    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        return 2
    for label, items in (("CHANGED", result.changed), ("MISSING", result.missing),
                         ("NOT REGISTERED", result.unregistered)):
        for item in items:
            print(f"{label}: {item}")
    total = len(read_register(register))
    print(f"{total} registered files checked, "
          f"{len(result.changed)} changed, {len(result.missing)} missing, "
          f"{len(result.unregistered)} not registered")
    return 0 if result.ok else 1


if __name__ == "__main__":
    sys.exit(main())
