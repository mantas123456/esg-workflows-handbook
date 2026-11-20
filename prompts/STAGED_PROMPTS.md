# Staged prompts for Claude Code (VS Code)

How to use:

1. Open the repo folder in VS Code and start Claude Code.
2. Run one prompt at a time. Start each stage in **plan mode** (Shift+Tab),
   read the plan, then approve.
3. After each prompt: check the preview (`mkdocs serve`), read the diff, commit.
4. Type `/clear` between stages so each stage starts fresh. `CLAUDE.md`
   keeps the rules across sessions.
5. Do not skip the "verify facts" prompt at the start of each track.

Every prompt ends with the same check. Claude Code should run it itself:

> Run build_pages.py, check_workflows.py, pytest -q and mkdocs build --strict.
> Fix anything that fails. Then show me a short summary and the files changed.
> Do not commit until I say so.

(Called **[CHECK]** below. Paste it at the end of each prompt.)

---

## Stage 0: Set up and publish

### 0.1 Local setup

```
Read CLAUDE.md and DEVELOPMENT_PLAN.md. Set up the project on this Windows machine:
create .venv with Python 3.12, install requirements-dev.txt, and run the four checks.
Then explain the repo structure to me in 10 lines. [CHECK]
```

### 0.2 Push and turn on Pages

```
The empty GitHub repo mantas123456/esg-workflows-handbook exists. Add it as origin,
push main, and tell me the exact clicks to set GitHub Pages source to "GitHub Actions".
After I confirm, check that the docs workflow runs green using gh run list.
```

---

## Stage 1: Release 0.1 Skeleton

### 1.1 Regulation timeline (T2)

```
Write docs/start-here/timeline.md (step T2) using only facts from data/regulations.yml.
First re-verify every fact with web search against official sources (EUR-Lex, DG TAXUD,
EFRAG, Commission) and update last_checked. Show one table per regime: date,
what happens, who it affects, source. Follow docs/_chapter_template.md where it fits.
Set T2 status to draft. [CHECK]
```

### 1.2 Triage (T1)

```
Write docs/start-here/triage.md (step T1): "Which regime applies to me?".
Make it a decision tree with 4 branches (CBAM, CSRD, VSME, Scope 3 requests).
Use Mermaid flowchart (enable it in mkdocs.yml via pymdownx.superfences custom fence).
Each branch ends with a link to the first step of that track and the legal test with
source. Never say "you are in scope". Add 3 short fictional examples: a Maltese
steel importer with 30 t/year, one with 400 t/year, and a 120-person supplier asked
for emissions by a large customer. Set T1 to draft. [CHECK]
```

### 1.3 Evidence locker (F1)

```
Write docs/foundations/evidence-locker.md (F1). Explain how to keep evidence so each
reported number traces back to its source: folder structure, file naming, SHA-256
hashing, a register (CSV) linking reported value -> calculation -> source file hash,
retention periods (cite sources, CBAM record-keeping article). Add
scripts/hash_evidence.py: walks a folder, writes evidence_register.csv
(path, sha256, size, modified, note) and verifies an existing register. Add tests
with a temp folder. Link the script from the page. Set F1 to draft. [CHECK]
```

### 1.4 One dataset, many reports (F3)

```
Write docs/foundations/one-dataset-many-reports.md (F3). Show a reuse map: which
data (energy use, fuel, purchased goods spend, supplier emissions, imports by CN code,
headcount) feeds CBAM, Scope 3, VSME and ESRS E1. Use one table and one Mermaid
diagram. Add a data dictionary at data/datasets.yml (name, unit, owner role,
frequency, used_by list) and render it into the page with build_pages.py.
Set F3 to draft. [CHECK]
```

### 1.5 Release 0.1

```
Update docs/roadmap.md and README.md status to 0.1 done. Add docs/changelog.md
with a dated entry. Add the handbook link to the README of mantas123456/mantas123456
only if I confirm. Merge to main and tag v0.1. [CHECK]
```

---

## Stage 2: Release 0.2 CBAM

### 2.0 Verify facts

```
Create branch release/0.2-cbam. Using web search on official sources only
(EUR-Lex: Regulation 2023/956, 2025/2083 and implementing acts; DG TAXUD CBAM pages),
re-verify all CBAM facts in data/regulations.yml and add any new ones the CBAM track
needs: goods in Annex I, threshold rules, authorisation, default values publication,
verification, carbon price paid deduction, certificate price, holding rule,
declaration content, penalties, record keeping. One entry per fact with source URL
and article. List anything still pending or unclear. Do not write pages yet.
```

### 2.1 esgcalc package and CBAM calculations

```
Create the esgcalc Python package (pyproject.toml, esgcalc/__init__.py, esgcalc/cbam.py).
Functions with type hints and docstrings:
- threshold_check(imports: list of (cn_code, mass_t)) -> result with total mass,
  whether above 50 t, and the note that hydrogen and electricity have no threshold
- embedded_emissions(direct, indirect, precursors) -> specific and total embedded
  emissions (tCO2e/t and tCO2e)
- certificates_needed(total_tco2e, free_allocation_adjustment, carbon_price_paid_tco2e)
- certificate_cost(certificates, price_eur_per_tco2e)
- quarterly_holding(certificates_ytd) using the 50% rule
Reference article numbers in docstrings. Write pytest tests with hand-calculated
values, including edge cases (exactly 50 t, zero precursors, carbon price paid
above liability). Keep CBAM-specific parameters in data/cbam_parameters.yml with
sources, not hard-coded. [CHECK]
```

### 2.2 CBAM pages CB1–CB5

```
Write CB1 to CB5 following docs/_chapter_template.md. Use one fictional importer
through the whole track: "Melita Metals Ltd" (Malta) importing steel products and
aluminium from two non-EU installations. Every number in worked examples must come
from esgcalc and be checked by a test in tests/test_examples_cbam.py. Only state
facts that are in data/regulations.yml. Set each to draft. Do one page at a time and
pause after CB1 so I can review the style. [CHECK]
```

### 2.3 CBAM pages CB6–CB10

```
Write CB6 to CB10, continuing the Melita Metals example (verification, carbon price
paid, certificates and quarterly holding, annual declaration, records). CB10 must link
the evidence locker (F1) and hash_evidence.py. Same rules as before. [CHECK]
```

### 2.4 CBAM templates

```
Create the template build system like the lab handbook: templates/sheets/*.yml for
Excel (openpyxl) and templates/src/*.md for Word (pandoc), built by
scripts/build_templates.py into docs/downloads/. Make:
- cbam-goods-register.xlsx (CN code, description, origin, installation, mass_t,
  running total vs 50 t with formulas)
- cbam-emissions-workbook.xlsx (direct, indirect, precursors, default vs actual,
  formulas matching esgcalc)
- cbam-supplier-request.docx (cover letter asking operators for emissions data;
  link to the Commission's official communication template, do not copy it)
- cbam-declaration-checklist.docx
Add tests: each file opens, formulas give the same results as esgcalc for the
Melita Metals example. Link templates from the pages via data/workflows.yml.
Update CI to build templates and run tests. [CHECK]
```

### 2.5 CBAM browser calculator

```
Build docs/tools/cbam-calculator.md with an embedded client-side tool (plain JS, no
framework, no external calls): enter imports by CN code and mass, emissions data or
"use default", price; get threshold result, embedded emissions, certificates, cost,
quarterly holding. Port the formulas from esgcalc and add a Playwright test that
checks the tool gives the same numbers as esgcalc for the Melita example.
Clear "not legal advice" banner. Link from CB1, CB4 and CB8. [CHECK]
```

### 2.6 Release 0.2

```
Review the whole CBAM track as a strict CBAM practitioner would: list factual risks,
unclear steps and missing sources. Fix what you can, list what needs me.
Then update roadmap, changelog, README; merge release/0.2-cbam and tag v0.2. [CHECK]
```

---

## Stage 3: Release 0.3 Scope 3

### 3.0 Verify facts

```
Create branch release/0.3-scope3. Using web search, collect the current state of
GHG Protocol Scope 3 Standard and any revisions in progress, the ESRS E1 Scope 3
requirements in the simplified ESRS, and open emission-factor sources (DESNZ/DEFRA
latest year, EEA, EXIOBASE licence terms, USEEIO). Add to data/regulations.yml and a
new data/factor_sources.yml (name, version, year, coverage, licence, URL).
Summarise what can and cannot be republished.
```

### 3.1 esgcalc Scope 3 and data quality

```
Add esgcalc/scope3.py and esgcalc/quality.py:
- spend_based(spend_eur, factor_kgco2e_per_eur, inflation/currency adjustment)
- average_data(activity, factor), supplier_specific(allocated emissions)
- hybrid combination per category
- data-quality score per line (technology, time, geography, completeness, reliability;
  1-5) and a weighted category score
- uncertainty: propagate stated uncertainties analytically for sums, and a Monte Carlo
  function (numpy, seeded) for lognormal factors; return mean and 95% interval
Tests with hand-calculated values. [CHECK]
```

### 3.2 Scope 3 pages S1–S5 and F2

```
Write S1 to S5 and F2 (data quality and uncertainty) using a fictional Maltese
company "Gozo Fresh Foods Ltd" (food processing, 140 staff) asked by a supermarket
for Scope 3. In S2 show screening of all 15 categories with a relevance reason for
each. F2 must explain uncertainty the way a measurement lab would (input
uncertainties, combination, coverage interval) and link to the Monte Carlo demo.
Numbers from esgcalc, tested. Pause after S1 for style review. [CHECK]
```

### 3.3 Scope 3 pages S6–S9

```
Write S6 to S9 (data quality scoring, supplier engagement, base year and
recalculation policy with a significance threshold, reporting the inventory).
Continue Gozo Fresh Foods. S9 includes a sample inventory table with method,
data-quality score and uncertainty per category. [CHECK]
```

### 3.4 Scope 3 templates and tools

```
Add templates: scope3-screening-matrix.xlsx, scope3-inventory.xlsx (spend, average,
supplier-specific tabs with data-quality scores), supplier-letter.docx,
recalculation-policy.docx. Add browser tools: docs/tools/scope3-screening.md and
docs/tools/uncertainty-demo.md (Monte Carlo in the browser with a histogram).
Tests and Playwright tests as for CBAM. [CHECK]
```

### 3.5 Release 0.3

```
Practitioner review of the Scope 3 track (as a GHG verifier would), fix, update
roadmap/changelog/README, merge and tag v0.3. [CHECK]
```

---

## Stage 4: Release 0.4 VSME

### 4.0 Verify facts

```
Create branch release/0.4-vsme. Using web search, confirm the current status of the
voluntary standard (VSME) delegated act (adoption, OJ publication, application), its
module structure (Basic, Comprehensive), the datapoints in each, and the value-chain
cap / protected undertaking rules from Omnibus I. Add to data/regulations.yml with
article references. Create data/vsme_datapoints.yml listing each datapoint (id,
module, short description in our own words, unit, linked dataset from
data/datasets.yml). Do not copy the standard's text.
```

### 4.1 VSME pages V1–V6

```
Write V1 to V6 using Gozo Fresh Foods again (so readers see Scope 3 data reused in
VSME). V3 links the Scope 3 track and explains which emissions the Basic module
needs. V5 is a playbook for answering customer and bank questionnaires: map common
questions to VSME datapoints, explain the value-chain cap in plain words, include
polite reply wording. Generate the datapoint tables from data/vsme_datapoints.yml in
build_pages.py. Pause after V1. [CHECK]
```

### 4.2 VSME templates and tool

```
Add vsme-basic-workbook.xlsx (one row per Basic datapoint, generated from
data/vsme_datapoints.yml, with completeness tracking) and a questionnaire response
bank (docx). Add docs/tools/vsme-readiness.md: tick what data you have, get
completeness by module and a to-do list. Tests. [CHECK]
```

### 4.3 Release 0.4

```
Practitioner review of VSME track, fix, update roadmap/changelog/README, merge, tag v0.4. [CHECK]
```

---

## Stage 5: Release 0.5 CSRD / ESRS

### 5.0 Verify facts

```
Create branch release/0.5-csrd. Using web search on official sources, confirm: OJ
publication and entry into force of the simplified ESRS delegated act, list and
structure of the revised standards, materiality approach, phase-in reliefs,
assurance requirements after Omnibus I, digital tagging (ESEF/XBRL taxonomy)
status, and Malta's transposition status. Update data/regulations.yml. Create
data/esrs_datapoints.yml (our own short descriptions only, linked to datasets).
Report anything still pending.
```

### 5.1 esgcalc DMA

```
Add esgcalc/dma.py: impact materiality score (scale, scope, irremediability,
likelihood for potential impacts) and financial materiality score (magnitude,
likelihood), with configurable thresholds from data/dma_parameters.yml, following
the method as described in the adopted ESRS (cite, do not copy). Return a ranked IRO
list. Tests. [CHECK]
```

### 5.2 CSRD pages C1–C5

```
Write C1 to C5 with a fictional in-scope group "Mediterranean Logistics Group"
(1,300 employees, EUR 520 m turnover) whose suppliers include Gozo Fresh Foods and
Melita Metals, to show the value chain linking all four tracks. C3 must respect the
value-chain cap. C5 links Scope 3 and CBAM data into E1. Pause after C1. [CHECK]
```

### 5.3 CSRD pages C6–C9

```
Write C6 to C9: overview of other topical standards, datapoint gap analysis,
assurance readiness (what a limited-assurance provider asks for, linked to the
evidence locker), digital tagging and publication. [CHECK]
```

### 5.4 CSRD templates and tools

```
Add dma-workbook.xlsx, iro-register.xlsx, esrs-gap-list.xlsx (generated from
data/esrs_datapoints.yml). Add docs/tools/dma-scoring.md and docs/tools/esrs-gap.md
(client-side). Tests and Playwright tests. [CHECK]
```

### 5.5 Release 0.5

```
Practitioner review of the CSRD track (as a limited-assurance provider would), fix,
update roadmap/changelog/README, merge, tag v0.5. [CHECK]
```

---

## Stage 6: Release 0.6 Polish

```
Create branch release/0.6-polish. Do all of:
1. Write F4 "Keeping up with changes" and add scripts/check_regulations.py to CI
   (warn at 90 days, fail at 180).
2. Consistency pass: every page follows the template, every page has last_checked,
   every template is linked, every tool has a test, no broken links.
3. Accessibility pass on tools (labels, keyboard use, contrast).
4. Add a templates index page and a tools index page.
5. Add a GitHub issue template "Report an error or outdated rule".
List anything you could not fix. [CHECK]
```

---

## Stage 7: Release 1.0

### 7.1 Self review

```
Act as three reviewers in turn: a CBAM customs specialist, a GHG verifier, and a
CSRD limited-assurance provider. For each, read the relevant track and list errors,
outdated facts, unclear steps and missing sources, ranked by severity. Do not fix
yet. Save the result to review/self-review-1.0.md.
```

### 7.2 Fixes, PDF and DOI

```
Fix the items from review/self-review-1.0.md that I approve. Then add a PDF edition
(mkdocs-with-pdf or a pandoc pipeline) built in CI and attached to GitHub releases,
add CITATION.cff, and prepare the Zenodo GitHub integration steps for a DOI (tell
me the clicks). Update status of reviewed pages only where an external practitioner
has actually reviewed them. Tag v1.0. [CHECK]
```

---

## Useful one-off prompts

Rule changed:

```
A rule changed: <paste news / link>. Verify it on the official source, update
data/regulations.yml, find every page, template, parameter file and test affected,
update them, and add a changelog entry. [CHECK]
```

Style review of a page:

```
Review docs/<path>.md against CLAUDE.md writing rules and the chapter template:
plain English, short sentences, own words, sourced facts, tested numbers. List
issues, then fix them. [CHECK]
```
