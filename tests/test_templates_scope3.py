"""The Scope 3 templates: the inventory workbook recalculates to the same numbers as
esgcalc and the S9 inventory, its example rows are the Gozo Fresh Foods data, and the
Word templates contain what their pages promise."""
import pytest

from esgcalc import quality, scope3
from esgcalc.scope3 import CATEGORY_NAMES
from test_examples_scope3 import EXAMPLE, _inventory_tco2e, _line_tco2e, inventory_totals
from test_examples_scope3_report import all_lines, category_summary, inventory_score
from test_templates import _docx_text, built, bt, recalculate  # noqa: F401  (built is a fixture)

AVG = "AVERAGE-DATA"


def _all_example_lines() -> list[dict]:
    inv = EXAMPLE["inventory"]
    return list(inv["lines"]) + [l for l in EXAMPLE["screening"]["lines"]
                                 if l["category"] in inv["kept_from_screening"]]


def test_inventory_examples_are_the_gozo_inventory(built) -> None:
    from openpyxl import load_workbook

    wb = load_workbook(built["scope3-inventory"])
    tabs = {"spend_based": ("Spend", "C"), "average_data": ("Average-data", "C"), "supplier_specific": ("Supplier", "C")}
    seen: dict[str, list[str]] = {m: [] for m in tabs}
    for method, (sheet, _) in tabs.items():
        ws = wb[sheet]
        for r in range(2, 42):
            if ws[f"B{r}"].value:
                seen[method].append(ws[f"B{r}"].value)
    for l in _all_example_lines():
        assert l["description"] in seen[l["method"]], l["description"]
    assert sum(len(v) for v in seen.values()) == len(_all_example_lines()) == 27


def test_inventory_lines_match_esgcalc(built) -> None:
    from openpyxl import load_workbook

    got = recalculate(built["scope3-inventory"])
    wb = load_workbook(built["scope3-inventory"])
    value_col = {"Spend": "H", "Average-data": "F", "Supplier": "F"}
    expected = {l["description"]: (_inventory_tco2e(l) if l["category"] not in EXAMPLE["inventory"]["kept_from_screening"]
                                   else _line_tco2e(l)) for l in _all_example_lines()}
    for sheet, col in value_col.items():
        ws = wb[sheet]
        for r in range(2, 42):
            name = ws[f"B{r}"].value
            if name:
                assert got[f"{sheet.upper()}!{col}{r}"] == pytest.approx(expected[name]), name


def test_inventory_summary_matches_s9(built) -> None:
    got = recalculate(built["scope3-inventory"])
    summary = category_summary()
    totals = inventory_totals()
    for r, cat in zip(range(2, 17), CATEGORY_NAMES):
        assert got[f"SUMMARY!A{r}"] == cat
        if cat not in summary:
            assert got[f"SUMMARY!F{r}"] == 0 and got[f"SUMMARY!G{r}"] == ""
            continue
        s, t = summary[cat], totals[cat]
        assert got[f"SUMMARY!C{r}"] == pytest.approx(t.by_method.get("supplier_specific", 0.0)), cat
        assert got[f"SUMMARY!D{r}"] == pytest.approx(t.by_method.get("average_data", 0.0)), cat
        assert got[f"SUMMARY!E{r}"] == pytest.approx(t.by_method.get("spend_based", 0.0)), cat
        assert got[f"SUMMARY!F{r}"] == pytest.approx(s["tco2e"]), cat
        assert got[f"SUMMARY!G{r}"] == pytest.approx(s["score"]), cat          # emissions-weighted score
        assert got[f"SUMMARY!H{r}"] == pytest.approx(s["u95_abs"]), cat        # combined U
        assert got[f"SUMMARY!I{r}"] == pytest.approx(s["u95_rel"]), cat


def test_inventory_totals_match_s9(built) -> None:
    got = recalculate(built["scope3-inventory"])
    summary = category_summary()
    total = quality.sum_uncertainty([s["tco2e"] for s in summary.values()], [s["u95_rel"] for s in summary.values()])
    totals = inventory_totals()
    grand = sum(t.tco2e for t in totals.values())
    assert got["TOTALS!B1"] == pytest.approx(total.value) == pytest.approx(5752.59322, abs=1e-5)
    for row, method in ((2, "supplier_specific"), (3, "average_data"), (4, "spend_based")):
        share = sum(t.by_method.get(method, 0.0) for t in totals.values()) / grand
        assert got[f"TOTALS!B{row}"] == pytest.approx(share), method
    assert got["TOTALS!B5"] == pytest.approx(inventory_score())                  # 1.94
    assert got["TOTALS!B6"] == pytest.approx(total.u95_abs)                      # 416.81
    assert got["TOTALS!B7"] == pytest.approx(total.u95_rel)


def test_inventory_line_uncertainty_uses_product_rule(built) -> None:
    got = recalculate(built["scope3-inventory"])
    rows = {r["description"]: r for rows in all_lines().values() for r in rows}
    from openpyxl import load_workbook

    ws = load_workbook(built["scope3-inventory"])["Average-data"]
    for r in range(2, 42):
        name = ws[f"B{r}"].value
        if name:
            assert got[f"{AVG}!O{r}"] == pytest.approx(rows[name]["u95"]), name
            assert got[f"{AVG}!P{r}"] == pytest.approx(rows[name]["value"] * rows[name]["u95"]), name


def test_inventory_currency_and_deflation(built, tmp_path) -> None:
    from test_templates import edited_copy

    # Spend row 2: EUR 10,000, 1.10 USD per EUR, indices 110 -> 100, factor 0.4 -> 4.0 t (as esgcalc)
    path = edited_copy(built["scope3-inventory"], tmp_path,
                       {"Spend": {"C2": 10_000, "D2": 1.10, "E2": 110, "F2": 100, "G2": 0.4}})
    got = recalculate(path)
    assert got["SPEND!H2"] == pytest.approx(scope3.spend_based(10_000, 0.4, factor_currency_per_eur=1.10,
                                                               price_index_spend_year=110,
                                                               price_index_factor_year=100)) == pytest.approx(4.0)


def test_supplier_letter_asks_what_s7_asks(built) -> None:
    text = _docx_text(built["supplier-letter"])
    for needed in ("Scope 1, Scope 2", "total output", "cradle to gate", "verified", "energy bills",
                   "production volume", "Please reply by"):
        assert needed in text, needed


def test_recalculation_policy_matches_s8(built) -> None:
    text = _docx_text(built["recalculation-policy"])
    for needed in ("Structural change", "Change in calculation method or data source", "Error",
                   "absolute", "whole base year", "disclose"):
        assert needed in text, needed
