"""The template pack builds, every file opens, and the Excel formulas give the
same results as esgcalc for the Melita Metals example (data/examples/melita_metals.yml)."""
import importlib.util
import shutil
import sys
import warnings
from decimal import Decimal
from pathlib import Path

import pytest
import yaml

from esgcalc import cbam
from esgcalc.cbam import Precursor

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("build_templates", ROOT / "scripts/build_templates.py")
bt = importlib.util.module_from_spec(spec)
sys.modules["build_templates"] = bt
spec.loader.exec_module(bt)

EXAMPLE = yaml.safe_load((ROOT / "data/examples/melita_metals.yml").read_text(encoding="utf-8"))
WORKFLOWS = yaml.safe_load((ROOT / "data/workflows.yml").read_text(encoding="utf-8"))
EXPECTED_IDS = {"cbam-goods-register", "cbam-emissions-workbook", "cbam-supplier-request", "cbam-declaration-checklist",
                "scope3-screening-matrix", "scope3-inventory", "supplier-letter", "recalculation-policy",
                "vsme-basic-workbook", "questionnaire-response-bank",
                "dma-workbook", "iro-register", "esrs-gap-list"}


@pytest.fixture(scope="session")
def built() -> dict[str, Path]:
    bt.build(quiet=True)
    return {t["id"]: bt.output_path(t) for t in bt.catalog()}


def recalculate(path: Path) -> dict[str, object]:
    """Recalculate every formula with the `formulas` package: {'SHEET!A1': value}."""
    import formulas

    warnings.filterwarnings("ignore")
    solution = formulas.ExcelModel().loads(str(path)).finish().calculate()
    out = {}
    for key, value in solution.items():
        if "!" not in key or ":" in key.split("!")[-1]:
            continue
        sheet = key.split("]")[-1].split("!")[0].strip("'").upper()
        v = value.value[0, 0] if hasattr(value, "value") else value
        out[f"{sheet}!{key.split('!')[-1].upper()}"] = v.item() if hasattr(v, "item") else v
    return out


def edited_copy(src: Path, tmp_path: Path, edits: dict[str, dict[str, object]]) -> Path:
    """A copy of a workbook with some cells changed: {sheet: {cell: value}}."""
    from openpyxl import load_workbook

    dst = tmp_path / src.name
    shutil.copy(src, dst)
    wb = load_workbook(dst)
    for sheet, cells in edits.items():
        for cell, value in cells.items():
            wb[sheet][cell] = value
    wb.save(dst)
    return dst


# --- every template ---------------------------------------------------------

def test_catalog_has_the_cbam_templates(built) -> None:
    assert set(built) == EXPECTED_IDS


def test_every_file_opens(built) -> None:
    from docx import Document
    from openpyxl import load_workbook

    for tid, path in built.items():
        assert path.exists() and path.stat().st_size > 0, tid
        if path.suffix == ".xlsx":
            wb = load_workbook(path)
            assert wb.sheetnames[0] == "About"
            assert any(bt.FOOTER == c.value for row in wb["About"].iter_rows() for c in row), tid
        else:
            assert Document(str(path)).paragraphs, tid


def test_build_is_reproducible(built, tmp_path) -> None:
    before = {tid: p.read_bytes() for tid, p in built.items()}
    bt.build(force=True, quiet=True)
    assert {tid: p.read_bytes() for tid, p in built.items()} == before


def test_every_listed_template_is_linked_from_its_page(built) -> None:
    catalog = {t["id"]: t for t in bt.catalog()}
    for track in WORKFLOWS["tracks"]:
        for step in track["steps"]:
            if step["status"] == "planned":
                continue
            text = (ROOT / "docs" / track["folder"] / step["file"]).read_text(encoding="utf-8")
            for tid in step.get("templates", []):
                assert f"downloads/{tid}.{catalog[tid]['format']}" in text, (step["id"], tid)


def test_formula_parameters_come_from_cbam_parameters() -> None:
    p = cbam.load_parameters()
    fp = bt.formula_params()
    assert fp["threshold_t"] == str(p["threshold"]["max_exempt_mass_t"])
    for code in p["threshold"]["excluded_cn_codes"]:
        assert f'"{code}"' in fp["excluded_test"]
    for sector, v in p["sectors"].items():
        if isinstance(v, dict) and v.get("direct_only"):
            assert f'"{sector}"' in fp["direct_only_test"]


# --- goods register ---------------------------------------------------------

def test_goods_register_examples_are_the_melita_imports(built) -> None:
    from openpyxl import load_workbook

    ws = load_workbook(built["cbam-goods-register"])["Register"]
    imports = EXAMPLE["imports_2026"]
    for r, line in enumerate(imports, start=2):
        quarter, cn, inst, mass = ws[f"A{r}"].value, ws[f"C{r}"].value, ws[f"F{r}"].value, ws[f"G{r}"].value
        assert (quarter, cn, inst, mass) == (f"2026 {line['quarter']}", line["cn_code"], line["installation"], line["mass_t"])


def test_goods_register_running_total_matches_esgcalc(built) -> None:
    got = recalculate(built["cbam-goods-register"])
    so_far: list[tuple[str, float]] = []
    for r, line in enumerate(EXAMPLE["imports_2026"], start=2):
        so_far.append((line["cn_code"], line["mass_t"]))
        result = cbam.threshold_check(so_far)
        assert got[f"REGISTER!H{r}"] == "No"
        assert got[f"REGISTER!J{r}"] == pytest.approx(result.total_mass_t)
        assert got[f"REGISTER!K{r}"] == ("Above 50 t" if result.above_threshold else "Within 50 t")
    assert got[f"REGISTER!J{len(EXAMPLE['imports_2026']) + 1}"] == pytest.approx(435)
    assert got[f"REGISTER!K{len(EXAMPLE['imports_2026']) + 2}"] == ""     # empty row stays blank


def test_goods_register_exactly_50_t_and_hydrogen(built, tmp_path) -> None:
    # 30 t + 20 t of steel = exactly 50 t (within); 5 t hydrogen is flagged and not counted
    rows = [("7214 20 00", 30), ("7214 20 00", 20), ("2804 10 00", 5)]
    edits = {"Register": {}}
    for r in range(2, 13):
        for col in "ABCDEFG":
            edits["Register"][f"{col}{r}"] = None
    for r, (cn, mass) in enumerate(rows, start=2):
        edits["Register"].update({f"C{r}": cn, f"G{r}": mass})
    got = recalculate(edited_copy(built["cbam-goods-register"], tmp_path, edits))
    expected = cbam.threshold_check(rows)
    assert (expected.total_mass_t, expected.above_threshold) == (50.0, False)
    assert [got[f"REGISTER!H{r}"] for r in (2, 3, 4)] == ["No", "No", "Yes"]
    assert got["REGISTER!I4"] == 0
    assert got["REGISTER!J4"] == pytest.approx(expected.total_mass_t)
    assert got["REGISTER!K4"] == "Within 50 t"


# --- emissions workbook -----------------------------------------------------

def _esgcalc_example() -> dict[str, float]:
    """The Melita Metals figures from esgcalc, as in CB4, CB5 and CB8."""
    crude = EXAMPLE["installation_A_crude_steel_2026"]
    bars = EXAMPLE["installation_A_2026"]
    mass = lambda inst: sum(l["mass_t"] for l in EXAMPLE["imports_2026"] if l["installation"] == inst)  # noqa: E731
    by_code = lambda code: sum(l["mass_t"] for l in EXAMPLE["imports_2026"] if l["cn_code"] == code)  # noqa: E731
    crude_see = cbam.embedded_emissions(
        sector="iron_steel", production_mass_t=crude["production_mass_t"], direct_tco2e=crude["direct_tco2e"],
        precursors=[Precursor(p["mass_t"], p["see_tco2e_per_t"]) for p in crude["precursors"]],
        imported_mass_t=0).see_tco2e_per_t
    bars_see = cbam.embedded_emissions(
        sector="iron_steel", production_mass_t=bars["production_mass_t"], direct_tco2e=bars["direct_tco2e"],
        indirect_tco2e=bars["indirect_tco2e"], precursors=[Precursor(bars["precursors"][0]["mass_t"], crude_see)],
        imported_mass_t=0).see_tco2e_per_t
    b_see = cbam.default_value_with_markup(
        EXAMPLE["default_values_base"]["aluminium_bars_B"]["base_direct_see_tco2e_per_t"], 2026, "aluminium")
    fa = EXAMPLE["free_allocation_adjustment_tco2e_per_t"][2026]
    embedded = bars_see * mass("A") + b_see * mass("B")
    adjustment = fa["A"] * mass("A") + fa["B"] * mass("B")
    certs = cbam.certificates_needed(embedded, adjustment)
    return {"crude_see": crude_see, "bars_see": bars_see, "b_see": b_see,
            "j2": bars_see * by_code("7214 20 00"), "j3": bars_see * by_code("7214 99 10"), "j4": b_see * mass("B"),
            "embedded": embedded, "adjustment": adjustment, "certs": certs,
            "cost": cbam.certificate_cost(round(certs, 6), EXAMPLE["certificate_price_assumed_eur_per_tco2e"])}


def test_emissions_workbook_examples_are_the_melita_data(built) -> None:
    from openpyxl import load_workbook

    wb = load_workbook(built["cbam-emissions-workbook"])
    inst = wb["Installations"]
    crude, bars = EXAMPLE["installation_A_crude_steel_2026"], EXAMPLE["installation_A_2026"]
    assert [inst[f"{c}2"].value for c in "CDHI"] == [crude["production_mass_t"], crude["direct_tco2e"],
                                                     crude["precursors"][0]["mass_t"], crude["precursors"][0]["see_tco2e_per_t"]]
    assert [inst[f"{c}3"].value for c in "CDEH"] == [bars["production_mass_t"], bars["direct_tco2e"],
                                                     bars["indirect_tco2e"], bars["precursors"][0]["mass_t"]]
    assert inst["I3"].value == "=T2"
    goods = wb["Goods"]
    assert goods["F4"].value == EXAMPLE["default_values_base"]["aluminium_bars_B"]["base_direct_see_tco2e_per_t"]
    assert [goods[f"K{r}"].value for r in (2, 3, 4)] == [0.585, 0.585, 1.95]
    assert wb["Summary"]["B5"].value == EXAMPLE["certificate_price_assumed_eur_per_tco2e"]


def test_emissions_workbook_matches_esgcalc(built) -> None:
    got = recalculate(built["cbam-emissions-workbook"])
    e = _esgcalc_example()
    assert got["INSTALLATIONS!F3"] == "No"                         # indirect does not count for steel
    assert got["INSTALLATIONS!T2"] == pytest.approx(e["crude_see"])     # 0.55
    assert got["INSTALLATIONS!T3"] == pytest.approx(e["bars_see"])      # 0.652
    assert got["GOODS!I2"] == pytest.approx(e["bars_see"])
    assert got["GOODS!H4"] == pytest.approx(0.10)
    assert got["GOODS!I4"] == pytest.approx(e["b_see"])                 # 2.31
    for cell in ("j2", "j3", "j4"):
        assert got[f"GOODS!{cell.upper()}"] == pytest.approx(e[cell])
    assert got["SUMMARY!B1"] == pytest.approx(e["embedded"])            # 341.65
    assert got["SUMMARY!B2"] == pytest.approx(e["adjustment"])          # 302.25
    assert got["SUMMARY!B4"] == pytest.approx(e["certs"])               # 39.4
    assert Decimal(str(got["SUMMARY!B6"])) == e["cost"] == Decimal("3152.00")


@pytest.mark.parametrize("year, sector", [(2026, "aluminium"), (2027, "aluminium"), (2028, "aluminium"),
                                          (2031, "aluminium"), (2027, "fertilisers")])
def test_markup_formula_matches_esgcalc(built, tmp_path, year, sector) -> None:
    path = edited_copy(built["cbam-emissions-workbook"], tmp_path, {"Goods": {"G4": year, "C4": sector}})
    got = recalculate(path)
    assert got["GOODS!I4"] == pytest.approx(cbam.default_value_with_markup(2.10, year, sector))


def test_eu_precursor_counts_as_zero_in_workbook(built, tmp_path) -> None:
    path = edited_copy(built["cbam-emissions-workbook"], tmp_path, {"Installations": {"J2": "Yes"}})
    got = recalculate(path)
    expected = cbam.embedded_emissions(sector="iron_steel", production_mass_t=104_000, direct_tco2e=30_600,
                                       precursors=[Precursor(14_000, 1.90, zero_rated=True)],
                                       imported_mass_t=0).see_tco2e_per_t
    assert got["INSTALLATIONS!T2"] == pytest.approx(expected)          # 30,600 / 104,000


def test_certificates_never_below_zero_in_workbook(built, tmp_path) -> None:
    path = edited_copy(built["cbam-emissions-workbook"], tmp_path, {"Summary": {"B3": 1000}})
    got = recalculate(path)
    assert got["SUMMARY!B4"] == cbam.certificates_needed(341.65, 302.25, 1000) == 0


# --- Word templates ---------------------------------------------------------

def _docx_text(path: Path) -> str:
    from docx import Document

    doc = Document(str(path))
    parts = [p.text for p in doc.paragraphs]
    parts += [c.text for t in doc.tables for row in t.rows for c in row.cells]
    return "\n".join(parts)


def test_supplier_request_links_to_the_commission_template(built) -> None:
    from docx import Document

    text = _docx_text(built["cbam-supplier-request"])
    rels = " ".join(r.target_ref for r in Document(str(built["cbam-supplier-request"])).part.rels.values())
    for url in ("https://taxation-customs.ec.europa.eu/carbon-border-adjustment-mechanism/cbam-legislation-and-guidance_en",
                "Guidance%20No.%202"):
        assert url in text or url in rels, url
    assert "operator emissions report template" in text
    assert "accredited verifier" in text


def test_declaration_checklist_covers_every_cbam_step(built) -> None:
    text = _docx_text(built["cbam-declaration-checklist"])
    for heading in ("Goods and quantities (CB1)", "Authorisation (CB2)", "Embedded emissions (CB3 to CB5)",
                    "Verification (CB6)", "Carbon price paid (CB7)", "Certificates (CB8)",
                    "Declaration and surrender (CB9)", "Records (CB10)"):
        assert heading in text, heading
    assert "30 September" in text


# --- Scope 3 screening matrix ----------------------------------------------------

def test_screening_matrix_matches_esgcalc(built) -> None:
    from esgcalc.scope3 import screen
    from openpyxl import load_workbook

    ws = load_workbook(built["scope3-screening-matrix"])["Screening"]
    estimates = {ws[f"A{r}"].value: ws[f"C{r}"].value for r in range(2, 17)}
    reasons = {ws[f"A{r}"].value: ws[f"G{r}"].value for r in range(2, 17) if ws[f"G{r}"].value}
    threshold = load_workbook(built["scope3-screening-matrix"])["Settings"]["B1"].value
    rows = screen(estimates, threshold, reasons)
    got = recalculate(built["scope3-screening-matrix"])
    for r, row in zip(range(2, 17), rows):
        assert got[f"SCREENING!E{r}"] == pytest.approx(row.share), row.category
        assert got[f"SCREENING!F{r}"] == ("Yes" if row.significant_by_size else "No"), row.category
        assert got[f"SCREENING!H{r}"] == ("Yes" if row.significant else "No"), row.category
    assert got["SETTINGS!B2"] == pytest.approx(7489.08)
    assert got["SETTINGS!B3"] == 7
    assert got["SETTINGS!B4"] == pytest.approx(7373.08)
    assert got["SETTINGS!B5"] == pytest.approx(7373.08 / 7489.08)


def test_screening_matrix_examples_are_the_gozo_screening() -> None:
    from openpyxl import load_workbook

    import test_examples_scope3 as ex   # same folder; recomputes the S2 estimates with esgcalc

    ws = load_workbook(bt.OUT / "scope3-screening-matrix.xlsx")["Screening"]
    for r, row in zip(range(2, 17), ex.screening_rows()):
        assert ws[f"A{r}"].value == row.category
        assert ws[f"B{r}"].value == row.name
        assert ws[f"C{r}"].value == pytest.approx(row.tco2e), row.category


def test_about_sheet_names_the_example_company(built) -> None:
    """Each workbook says whose made-up example it shows, and that company appears in its instructions or rows."""
    from openpyxl import load_workbook

    for path in sorted((ROOT / "templates" / "sheets").glob("*.yml")):
        spec = yaml.safe_load(path.read_text(encoding="utf-8"))
        company = spec.get("example_company", "Melita Metals Ltd")
        about = [c.value for c in load_workbook(built[path.stem])["About"]["A"] if c.value]
        assert any(f"made-up example ({company})" in v for v in about), path.stem
        short = company.split()[0]                                     # Gozo, Melita, Mediterranean
        others = {"Gozo", "Melita", "Mediterranean"} - {short}
        text = path.read_text(encoding="utf-8")
        assert short in text or "Gozo" not in text and "Mediterranean" not in text, path.stem
        assert not any(f"fictional {o}" in text for o in others), path.stem
