"""Tests for scripts/hash_evidence.py and the F1 worked example."""
import csv
import hashlib
import importlib.util
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("hash_evidence", ROOT / "scripts/hash_evidence.py")
he = importlib.util.module_from_spec(spec)
sys.modules["hash_evidence"] = he  # dataclasses look the module up here
spec.loader.exec_module(he)

PAGE = " ".join((ROOT / "docs/foundations/evidence-locker.md").read_text(encoding="utf-8").split())


def make_locker(tmp_path: Path) -> Path:
    folder = tmp_path / "evidence" / "2026"
    (folder / "energy").mkdir(parents=True)
    (folder / "cbam").mkdir()
    (folder / "energy" / "invoice-jan.txt").write_bytes(b"jan 410 MWh\n")
    (folder / "cbam" / "customs.txt").write_bytes(b"CN 7214, 400 t\n")
    return folder


def read_rows(register: Path) -> list[dict[str, str]]:
    with register.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_build_writes_register(tmp_path: Path) -> None:
    folder = make_locker(tmp_path)
    assert he.main(["build", str(folder)]) == 0
    register = folder / "evidence_register.csv"
    rows = read_rows(register)
    assert [r["path"] for r in rows] == ["cbam/customs.txt", "energy/invoice-jan.txt"]
    assert list(rows[0]) == he.FIELDS
    jan = rows[1]
    assert jan["sha256"] == hashlib.sha256(b"jan 410 MWh\n").hexdigest()
    assert jan["size"] == "12"
    assert jan["modified"].endswith("+00:00")


def test_verify_clean_then_detects_change_missing_and_new(tmp_path: Path, capsys) -> None:
    folder = make_locker(tmp_path)
    he.main(["build", str(folder)])
    assert he.main(["verify", str(folder)]) == 0

    (folder / "energy" / "invoice-jan.txt").write_bytes(b"jan 411 MWh\n")
    (folder / "cbam" / "customs.txt").unlink()
    (folder / "energy" / "invoice-feb.txt").write_bytes(b"feb 395 MWh\n")

    result = he.verify(folder, folder / "evidence_register.csv")
    assert result.changed == ["energy/invoice-jan.txt"]
    assert result.missing == ["cbam/customs.txt"]
    assert result.unregistered == ["energy/invoice-feb.txt"]
    capsys.readouterr()
    assert he.main(["verify", str(folder)]) == 1
    out = capsys.readouterr().out
    assert "CHANGED: energy/invoice-jan.txt" in out
    assert "MISSING: cbam/customs.txt" in out
    assert "NOT REGISTERED: energy/invoice-feb.txt" in out


def test_rebuild_keeps_notes(tmp_path: Path) -> None:
    folder = make_locker(tmp_path)
    register = folder / "evidence_register.csv"
    he.main(["build", str(folder)])
    rows = read_rows(register)
    rows[1]["note"] = "received by email 31 Jan"
    with register.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=he.FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    he.main(["build", str(folder)])
    assert read_rows(register)[1]["note"] == "received by email 31 Jan"


def test_register_outside_folder_and_errors(tmp_path: Path) -> None:
    folder = make_locker(tmp_path)
    register = tmp_path / "registers" / "reg.csv"
    assert he.main(["build", str(folder), "--register", str(register)]) == 0
    assert len(read_rows(register)) == 2
    assert he.main(["verify", str(folder), "--register", str(register)]) == 0
    assert he.main(["verify", str(folder), "--register", str(tmp_path / "none.csv")]) == 2
    assert he.main(["build", str(tmp_path / "no-such-folder")]) == 2


def test_large_file_hashed_in_chunks(tmp_path: Path) -> None:
    data = os.urandom(he.CHUNK_BYTES * 2 + 7)
    p = tmp_path / "big.bin"
    p.write_bytes(data)
    assert he.sha256_of(p) == hashlib.sha256(data).hexdigest()


def test_worked_example_numbers() -> None:
    q1_mwh = 410 + 395 + 445
    assert q1_mwh == 1250
    for n in ("| 410 |", "| 395 |", "| 445 |", "**1,250**", "| 1250 |"):
        assert n in PAGE
    jan = b"Melita Metals Ltd, electricity invoice, January 2026\n"
    edited = b"Melita Metals Ltd, electricity invoice, January 2026!\n"
    assert hashlib.sha256(jan).hexdigest() in PAGE
    assert hashlib.sha256(edited).hexdigest() in PAGE
    assert hashlib.sha256(jan).hexdigest() == "9f6b69d7da7a903199542b29ecdcc9beb38495b43756f5eb7688045b3b90baa5"


def test_cbam_retention_matches_regulations() -> None:
    import yaml
    regs = {r["id"]: r for r in yaml.safe_load((ROOT / "data/regulations.yml").read_text(encoding="utf-8"))}
    assert regs["cbam-records"]["values"]["retention_years_after_declaration_year"] == 4
    assert "**fourth year**" in PAGE
