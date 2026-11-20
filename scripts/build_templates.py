"""Build the downloadable templates.

    templates/src/<id>.md      letters, checklists      -> docs/downloads/<id>.docx (Pandoc)
    templates/sheets/<id>.yml  registers, workbooks     -> docs/downloads/<id>.xlsx (openpyxl)

Each source starts with metadata (Markdown front matter, or top-level YAML keys):

    title:        the name shown on the site and in the file
    type:         letter, checklist, register, workbook, ...
    description:  one sentence for the page that links it

Which page links a template is set in data/workflows.yml (``templates:``).

Sheet formulas may use placeholders filled from data/cbam_parameters.yml, so
regulatory numbers live in one place: {threshold_t}, {excluded_test},
{direct_only_test}, {markup_expr}, {tco2e_per_certificate}. ``{r}`` is the
row number. Built files get fixed internal timestamps (SOURCE_DATE_EPOCH, or
BUILD_DATE below), so rebuilding an unchanged template gives identical bytes.

    python scripts/build_templates.py           # rebuild what changed
    python scripts/build_templates.py --force   # rebuild everything
"""
from __future__ import annotations

import copy
import io
import os
import re
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "templates" / "src"
SHEETS = ROOT / "templates" / "sheets"
OUT = ROOT / "docs" / "downloads"
REFERENCE_DOCX = ROOT / "templates" / ".build" / "reference.docx"
PARAMETERS = ROOT / "data" / "cbam_parameters.yml"
BUILD_DATE = datetime(2026, 1, 1, tzinfo=timezone.utc)

SITE = "https://mantas123456.github.io/esg-workflows-handbook/"
FOOTER = ("ESG Workflows Handbook template · CC BY 4.0 · Not legal advice; "
          "the regulation and your competent authority take priority.")

GREEN = "2E7D32"
LABEL_FILL = "E8F5E9"
EXAMPLE_FONT_COLOR = "808080"


# ---------------------------------------------------------------- catalogue

def _front_matter(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n", text.replace("\r\n", "\n"), re.S)
    return (yaml.safe_load(m.group(1)) or {}) if m else {}


def catalog() -> list[dict]:
    """Every template with its id, title, type, description, format and source path."""
    items = []
    for path in sorted(SRC.glob("*.md")):
        items.append({**_meta(_front_matter(path.read_text(encoding="utf-8")), path), "format": "docx", "source": path})
    for path in sorted(SHEETS.glob("*.yml")):
        items.append({**_meta(yaml.safe_load(path.read_text(encoding="utf-8")), path), "format": "xlsx", "source": path})
    ids = [t["id"] for t in items]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        raise ValueError(f"template ids used twice: {sorted(dupes)}")
    return items


def _meta(meta: dict, path: Path) -> dict:
    missing = [k for k in ("title", "type", "description") if not meta.get(k)]
    if missing:
        raise ValueError(f"{path.relative_to(ROOT)}: missing {', '.join(missing)}")
    return {"id": path.stem, "title": meta["title"], "type": meta["type"], "description": meta["description"]}


def output_path(template: dict) -> Path:
    return OUT / f"{template['id']}.{template['format']}"


# ---------------------------------------------------------------- parameters

def formula_params() -> dict[str, str]:
    """Placeholders for sheet formulas, built from data/cbam_parameters.yml."""
    p = yaml.safe_load(PARAMETERS.read_text(encoding="utf-8"))
    excluded = [c.replace(" ", "") for c in p["threshold"]["excluded_cn_codes"]]
    direct_only = [s for s, v in p["sectors"].items() if isinstance(v, dict) and v.get("direct_only")]
    markups = {int(y): float(v) for y, v in p["default_value_markup_by_year"]["values"].items()}
    first, last = min(markups), max(markups)
    expr = "NA()"
    for year in sorted(markups, reverse=True):
        op = ">=" if year == last else "="
        expr = f"IF(G{{r}}{op}{year},{markups[year]},{expr})"
    for sector, m in p["default_value_markup_by_year"].get("sector_markup", {}).items():
        expr = f'IF(C{{r}}="{sector}",{float(m)},{expr})'
    assert first == min(markups)
    return {
        "r": "{r}",
        "threshold_t": str(p["threshold"]["max_exempt_mass_t"]),
        "excluded_test": "OR(" + ",".join(f'SUBSTITUTE(C{{r}}," ","")="{c}"' for c in excluded) + ")",
        "direct_only_test": "OR(" + ",".join(f'B{{r}}="{s}"' for s in direct_only) + ")",
        "markup_expr": expr,
        "tco2e_per_certificate": str(p["certificate"]["tco2e_per_certificate"]),
    }


def fill(formula: str, row: int | None = None) -> str:
    """Fill parameter placeholders, then the row number."""
    text = formula.format_map(formula_params())
    return text.format(r=row) if row is not None else text


# ---------------------------------------------------------------- Word

def _reference_docx() -> Path:
    """Pandoc's default reference document, restyled once with python-docx."""
    if REFERENCE_DOCX.exists() and REFERENCE_DOCX.stat().st_mtime >= Path(__file__).stat().st_mtime:
        return REFERENCE_DOCX
    import subprocess

    import pypandoc
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Pt, RGBColor

    REFERENCE_DOCX.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([pypandoc.get_pandoc_path(), "-o", str(REFERENCE_DOCX),
                    "--print-default-data-file", "reference.docx"], check=True)
    doc = Document(str(REFERENCE_DOCX))
    names = [s.name for s in doc.styles]
    for name in ("Normal", "Body Text", "First Paragraph", "Compact"):
        if name in names:
            doc.styles[name].font.name, doc.styles[name].font.size = "Calibri", Pt(10.5)
    for name, size in (("Title", 20), ("Heading 1", 15), ("Heading 2", 12.5), ("Heading 3", 11)):
        if name in names:
            f = doc.styles[name].font
            f.name, f.size, f.bold, f.color.rgb = "Calibri", Pt(size), True, RGBColor.from_string(GREEN)
    if "Table" in names:   # visible borders so forms print with boxes
        style_el = doc.styles["Table"].element
        tbl_pr = style_el.find(qn("w:tblPr"))
        if tbl_pr is None:
            tbl_pr = OxmlElement("w:tblPr")
            after = [a for a in (style_el.find(qn(t)) for t in ("w:trPr", "w:tcPr", "w:tblStylePr")) if a is not None]
            after[0].addprevious(tbl_pr) if after else style_el.append(tbl_pr)
        old = tbl_pr.find(qn("w:tblBorders"))
        if old is not None:
            tbl_pr.remove(old)
        borders = OxmlElement("w:tblBorders")
        for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
            el = OxmlElement(f"w:{edge}")
            for k, v in (("w:val", "single"), ("w:sz", "4"), ("w:space", "0"), ("w:color", "999999")):
                el.set(qn(k), v)
            borders.append(el)
        later = [x for x in (tbl_pr.find(qn(t)) for t in ("w:shd", "w:tblLayout", "w:tblCellMar", "w:tblLook")) if x is not None]
        later[0].addprevious(borders) if later else tbl_pr.append(borders)
    footer = doc.sections[0].footer
    para = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
    para.text = FOOTER
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in para.runs:
        run.font.size, run.font.color.rgb = Pt(7.5), RGBColor(0x80, 0x80, 0x80)
    doc.save(str(REFERENCE_DOCX))
    return REFERENCE_DOCX


def build_docx(template: dict, out: Path) -> None:
    import pypandoc

    pypandoc.convert_file(str(template["source"]), "docx", format="markdown", outputfile=str(out),
                          extra_args=["--reference-doc", str(_reference_docx())])


# ---------------------------------------------------------------- Excel

def _styles() -> dict[str, Any]:
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

    thin = Side(style="thin", color="BBBBBB")
    return {
        "header_font": Font(bold=True, color="FFFFFF"),
        "header_fill": PatternFill("solid", fgColor=GREEN),
        "calc_fill": PatternFill("solid", fgColor=LABEL_FILL),
        "border": Border(left=thin, right=thin, top=thin, bottom=thin),
        "wrap": Alignment(wrap_text=True, vertical="top"),
        "example_font": Font(italic=True, color=EXAMPLE_FONT_COLOR),
        "title_font": Font(bold=True, size=14, color=GREEN),
        "bold": Font(bold=True),
    }


def _about_sheet(wb, spec: dict) -> None:
    from openpyxl.styles import Font

    st = _styles()
    ws = wb.create_sheet("About", 0)
    ws.column_dimensions["A"].width = 100
    rows = [(spec["title"], st["title_font"]), (spec["description"], None), ("", None), ("How to use", st["bold"])]
    rows += [(f"• {line}", None) for line in spec.get("instructions", [])]
    rows += [("• Rows in grey italics are a made-up example (Melita Metals Ltd). Replace or delete them.", None),
             ("• Green cells calculate themselves. Do not type over them.", None),
             ("", None), (FOOTER, Font(size=8, color="808080")),
             (f"Source and guidance: {SITE}", Font(size=8, color="808080"))]
    for i, (text, font) in enumerate(rows, start=1):
        cell = ws.cell(row=i, column=1, value=text)
        cell.alignment = st["wrap"]
        if font:
            cell.font = font


def _prefill(sheet: dict) -> None:
    """Fill a sheet's first columns from a data file, so the template stays in step with it.

    ``prefill: {file, key, where, fields}`` takes the list ``key`` from the YAML
    ``file``, keeps the items matching every ``where`` pair, and writes ``fields``
    into the first columns, one row per item. ``examples_by_id`` (optional) maps
    the first field's value to example values for the remaining input columns.
    The result becomes the sheet's ``fixed`` rows (and ``examples`` for the rest).
    """
    spec = sheet.pop("prefill", None)
    if not spec:
        return
    data = yaml.safe_load((ROOT / spec["file"]).read_text(encoding="utf-8"))
    items = data[spec["key"]] if spec.get("key") else data
    where = spec.get("where", {})
    items = [i for i in items if all(i.get(k) == v for k, v in where.items())]
    if not items:
        raise ValueError(f"{sheet['name']}: prefill matched nothing in {spec['file']}")
    fixed = [[i[f] for f in spec["fields"]] for i in items]
    examples = sheet.pop("examples_by_id", {}) or {}
    if spec.get("examples"):           # {file, key}: example values kept with the worked example
        src = yaml.safe_load((ROOT / spec["examples"]["file"]).read_text(encoding="utf-8"))
        examples = {**src[spec["examples"]["key"]], **examples}
    unknown = set(examples) - {row[0] for row in fixed}
    if unknown:
        raise ValueError(f"{sheet['name']}: examples for unknown ids {sorted(unknown)}")
    sheet["fixed"] = fixed
    sheet["examples"] = [examples.get(row[0]) for row in fixed]
    sheet["rows"] = len(fixed)


def _table_sheet(wb, sheet: dict) -> None:
    from openpyxl.formatting.rule import FormulaRule
    from openpyxl.styles import PatternFill
    from openpyxl.utils import get_column_letter
    from openpyxl.worksheet.datavalidation import DataValidation

    st = _styles()
    ws = wb.create_sheet(sheet["name"])
    cols = sheet["columns"]
    examples = sheet.get("examples", [])
    last = 1 + max(sheet.get("rows", 50), len(examples))

    for j, col in enumerate(cols, start=1):
        cell = ws.cell(row=1, column=j, value=col["header"])
        cell.font, cell.fill, cell.alignment, cell.border = st["header_font"], st["header_fill"], st["wrap"], st["border"]
        ws.column_dimensions[get_column_letter(j)].width = col.get("width", 14)
    ws.row_dimensions[1].height = 45
    ws.freeze_panes = "A2"

    fixed = sheet.get("fixed", [])
    n_fixed = len(fixed[0]) if fixed else 0
    for i in range(2, last + 1):
        example = examples[i - 2] if i - 2 < len(examples) else None
        fixed_row = fixed[i - 2] if i - 2 < len(fixed) else None
        for j, col in enumerate(cols, start=1):
            cell = ws.cell(row=i, column=j)
            cell.border, cell.alignment = st["border"], st["wrap"]
            k = j - 1 - n_fixed                       # index into the example, after the fixed columns
            if "formula" in col:
                cell.value = fill(col["formula"], i)
                cell.fill = st["calc_fill"]
                if example is not None and not fixed:
                    cell.font = st["example_font"]
            elif fixed_row is not None and j <= n_fixed:
                cell.value = fixed_row[j - 1]         # template content from a data file: normal font
            elif example is not None and 0 <= k < len(example) and example[k] is not None:
                value = example[k]
                cell.value = fill(value) if isinstance(value, str) and value.startswith("=") else value
                cell.font = st["example_font"]
            elif example is not None and not fixed:
                cell.font = st["example_font"]
            if col.get("format"):
                cell.number_format = {"percent": "0%", "date": "yyyy-mm-dd"}.get(col["format"], col["format"])

    for j, col in enumerate(cols, start=1):
        letter = get_column_letter(j)
        if col.get("choices"):
            dv = DataValidation(type="list", formula1='"' + ",".join(col["choices"]) + '"', allow_blank=True)
            dv.error, dv.errorTitle = "Choose a value from the list.", "Not in the list"
            ws.add_data_validation(dv)
            dv.add(f"{letter}2:{letter}{last}")
    for rule in sheet.get("highlights", []):
        rng = f"A2:{get_column_letter(len(cols))}{last}"
        ws.conditional_formatting.add(rng, FormulaRule(formula=[fill(rule["formula"])],
                                                       fill=PatternFill("solid", fgColor=rule.get("color", "FFCDD2"))))
    ws.auto_filter.ref = f"A1:{get_column_letter(len(cols))}{last}"
    ws.print_title_rows = "1:1"
    ws.page_setup.orientation = "landscape"
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.fitToWidth, ws.page_setup.fitToHeight = 1, 0


def _summary_sheet(wb, sheet: dict) -> None:
    """Label / value rows: inputs (example values) and calculated results."""
    st = _styles()
    ws = wb.create_sheet(sheet["name"])
    ws.column_dimensions["A"].width = 52
    ws.column_dimensions["B"].width = 18
    ws.column_dimensions["C"].width = 60
    for i, row in enumerate(sheet["rows"], start=1):
        label = ws.cell(row=i, column=1, value=row["label"])
        if row.get("bold"):
            label.font = st["bold"]
        cell = ws.cell(row=i, column=2)
        cell.border = st["border"]
        if "formula" in row:
            cell.value, cell.fill = fill(row["formula"], i), st["calc_fill"]
        else:
            cell.value, cell.font = row.get("example"), st["example_font"]
        if row.get("format"):
            cell.number_format = row["format"]
        if row.get("note"):
            ws.cell(row=i, column=3, value=row["note"]).alignment = st["wrap"]


def build_xlsx(template: dict, out: Path) -> None:
    from openpyxl import Workbook

    spec = yaml.safe_load(template["source"].read_text(encoding="utf-8"))
    wb = Workbook()
    wb.remove(wb.active)
    _about_sheet(wb, spec)
    for sheet in spec.get("sheets", []):
        sheet = copy.deepcopy(sheet)
        _prefill(sheet)
        (_summary_sheet if sheet.get("kind") == "summary" else _table_sheet)(wb, sheet)
    wb.active = 1 if len(wb.sheetnames) > 1 else 0
    wb.properties.title = template["title"]
    wb.properties.creator = "ESG Workflows Handbook"
    wb.save(str(out))


# ---------------------------------------------------------------- reproducible output

def build_date() -> datetime:
    epoch = os.environ.get("SOURCE_DATE_EPOCH")
    return datetime.fromtimestamp(int(epoch), tz=timezone.utc) if epoch else BUILD_DATE


def normalise_ooxml(path: Path) -> None:
    """Give a .docx or .xlsx fixed entry timestamps and document dates, so builds are reproducible."""
    stamp = build_date().strftime("%Y-%m-%dT%H:%M:%SZ")
    with zipfile.ZipFile(path) as src:
        entries = [(info, src.read(info)) for info in src.infolist()]
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as dst:
        for info, data in entries:
            if info.filename == "docProps/core.xml":
                data = re.sub(rb"(<dcterms:(?:created|modified)[^>]*>)[^<]*(</dcterms:)",
                              lambda m: m.group(1) + stamp.encode() + m.group(2), data)
            entry = zipfile.ZipInfo(info.filename, date_time=build_date().timetuple()[:6])
            entry.compress_type, entry.external_attr = zipfile.ZIP_DEFLATED, 0o644 << 16
            dst.writestr(entry, data, compresslevel=9)
    path.write_bytes(buf.getvalue())


# ---------------------------------------------------------------- driver

def build(force: bool = False, quiet: bool = False) -> list[Path]:
    """Build every template whose output is missing or older than its source, the
    parameters or this script, and remove outputs with no source."""
    OUT.mkdir(parents=True, exist_ok=True)
    # Sheets read data/ files (parameters, prefilled rows, example values): any change rebuilds.
    data_files = [p.stat().st_mtime for p in (ROOT / "data").rglob("*.yml")]
    newest_dependency = max([Path(__file__).stat().st_mtime, PARAMETERS.stat().st_mtime, *data_files])
    built = []
    templates = catalog()
    for t in templates:
        out = output_path(t)
        stale = force or not out.exists() or out.stat().st_mtime < max(t["source"].stat().st_mtime, newest_dependency)
        if not stale:
            continue
        (build_docx if t["format"] == "docx" else build_xlsx)(t, out)
        normalise_ooxml(out)
        built.append(out)
        if not quiet:
            print(f"built {out.relative_to(ROOT)}")
    known = {output_path(t).name for t in templates}
    for old in OUT.iterdir():
        if old.is_file() and old.name not in known:
            old.unlink()
            if not quiet:
                print(f"removed {old.relative_to(ROOT)}")
    return built


if __name__ == "__main__":
    print(f"{len(build(force='--force' in sys.argv))} template(s) built")
