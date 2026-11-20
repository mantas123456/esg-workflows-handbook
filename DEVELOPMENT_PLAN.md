# Development plan: ESG Workflows Handbook

Version 1 of this plan, 20 November 2026. Owner: Mantas Valantinavicius.

## 1. What we are building

A free, practical handbook of **step-by-step workflows** for four EU
sustainability regimes that small and mid-sized companies meet in practice:

| Track | Who it is for | Why it matters now |
|---|---|---|
| **CBAM** | EU importers of iron and steel, aluminium, cement, fertilisers, hydrogen and electricity, and their customs representatives | Definitive period started 1 Jan 2026. Certificate sales open 1 Feb 2027. First annual declaration and surrender due 30 Sep 2027. |
| **Scope 3** | Any company asked by a customer, bank or investor for its value-chain emissions | Scope 3 feeds ESRS E1, VSME and supplier questionnaires. Most SMEs have never done one. |
| **VSME** | SMEs outside CSRD scope that still get ESG data requests | Adopted by the Commission as the voluntary standard in July 2026. Large reporters may not ask "protected" value-chain companies for more than it covers. |
| **CSRD / ESRS** | Companies still in scope after Omnibus I (over 1,000 employees and over EUR 450 m turnover), and the advisers who help them | Simplified ESRS adopted July 2026. Mandatory from FY2027 for the companies that remain in scope; optional for FY2026. |

Each workflow step gets **one page** with the same parts: what it is,
inputs, steps, a worked example with made-up numbers, common mistakes,
templates, tools and sources. The site is built with MkDocs Material and
published on GitHub Pages, exactly like the
[Lab Accreditation Handbook](https://github.com/mantas123456/lab-accreditation-handbook).

### Why this handbook, and why by me

- **Measurement-science angle.** Most ESG guides treat emissions numbers as
  bookkeeping. This one treats them as measurements: traceable inputs,
  stated uncertainty, data-quality scores, recalculation rules. That is the
  gap I can fill from 14+ years of lab quality work.
- **One dataset, many reports.** The same activity data and emission
  factors feed CBAM, Scope 3, VSME and ESRS E1. The handbook shows the reuse
  map so companies collect data once.
- **Portfolio and business value.** It is a public showcase for data-science
  and ESG roles, and the method library behind ValantiData / CarbonTrack
  Advisory (CBAM, supplier emissions, evidence locker).

### Out of scope (for 1.0)

- Legal opinions or "you are / are not in scope" verdicts. The triage tool
  gives an indication and points to the source.
- Sector-specific ESRS, non-EU (third-country) ESRS, EU Taxonomy, CSDDD,
  EUDR. Listed in the backlog.
- Reproducing the GHG Protocol or EFRAG guidance. We cite and explain in our
  own words. EU legal texts are cited by article and linked on EUR-Lex.

## 2. Regulatory baseline (checked 20 Nov 2026)

Every page shows a "Last checked" date. `data/regulations.yml` holds the
facts below with their sources, and CI warns when an entry is more than
90 days old.

| Fact | Value | Source |
|---|---|---|
| Omnibus I Directive | (EU) 2026/470, published OJ 26 Feb 2026, in force 18 Mar 2026; member-state transposition still to follow | Council / CMS |
| CSRD scope after Omnibus I | EU companies with over 1,000 employees **and** over EUR 450 m net turnover | Council |
| Wave 1 companies now below thresholds | Member States may exempt them for FY2025 and FY2026 | Council |
| Simplified ESRS | 12 revised standards; delegated act adopted 3 Jul 2026; apply from FY2027, early use for FY2026 allowed once published in OJ | EFRAG / Commission |
| Voluntary standard (VSME) | Delegated act adopted 3 Jul 2026 alongside simplified ESRS | Commission |
| CBAM definitive period | Since 1 Jan 2026; Regulation (EU) 2023/956 as amended by (EU) 2025/2083 | DG TAXUD |
| CBAM de minimis | 50 tonnes net mass per year (not for hydrogen or electricity) | DG TAXUD |
| CBAM certificates | Sales from 1 Feb 2027; price = EU ETS auction average, quarterly in 2026, weekly from 2027 | DG TAXUD |
| CBAM declaration | First annual declaration and surrender by 30 Sep 2027 for 2026 imports; 50% quarterly holding thereafter | DG TAXUD |

**Open items to watch:** Malta's transposition of Omnibus I; the
Official Journal publication of the ESRS and VSME delegated acts; CBAM
secondary legislation (default values, verification, downstream
extension); GHG Protocol standard revisions (Scope 2 and Corporate
Standard).

## 3. Information architecture

```
Start here
  Which regime applies to me? (triage)      How to use this handbook
  Regulation timeline                       Workflow map
Foundations (shared by all tracks)
  F1 Evidence locker and audit trail        F3 One dataset, many reports
  F2 Data quality and uncertainty           F4 Keeping up with changes
CBAM          CB1-CB10   (scope check -> declaration)
Scope 3       S1-S9      (boundary -> inventory report)
VSME          V1-V6      (choose modules -> publish and answer requests)
CSRD / ESRS   C1-C9      (scope -> digital tagging)
Templates & tools
Reference     Glossary, Sources, About
```

The full step list with paths, templates and tools is in
[`data/workflows.yml`](data/workflows.yml). That file is the single source
of truth: the placeholder pages, the workflow map and the CI checks are all
generated from it.

## 4. Release plan

Assumes about 10-12 hours a week. Each release is useful on its own. Order
follows the hard external deadlines: CBAM first, because money and the
30 Sep 2027 declaration are on the line; CSRD last, because the companies
still in scope have large teams and first report in 2028.

| Version | Target | Adds | Done when |
|---|---|---|---|
| **0.1 Skeleton** | mid-Dec 2026 | Site, workflow map, chapter format, regulation tracker, triage page, F1 and F3, CI and Pages deploy | Site live; `check_workflows.py` and `mkdocs build --strict` pass in CI |
| **0.2 CBAM track** | end Feb 2027 | CB1-CB10 drafted; CBAM threshold checker and embedded-emissions calculator (Python + browser); supplier data request and declaration-prep workbooks | Worked example reconciles to the cent in tests; reviewed against current DG TAXUD guidance |
| **0.3 Scope 3 track** | end Apr 2027 | S1-S9 and F2; Scope 3 screening tool; inventory workbook with spend, average-data and supplier-specific methods; data-quality scoring | Example inventory recomputed in CI; every emission factor has a source and licence note |
| **0.4 VSME track** | end Jun 2027 | V1-V6; VSME Basic module workbook; "answering customer and bank questionnaires" playbook; value-chain cap explainer | Basic module workbook filled end to end for a fictional Maltese SME |
| **0.5 CSRD / ESRS track** | end Sep 2027 | C1-C9 on the simplified ESRS; double materiality workbook; datapoint gap analysis linked to the Scope 3 and VSME data | All pages cite the published delegated act article numbers |
| **0.6 Tools polish** | end Oct 2027 | All browser tools tested with Playwright; template pack built in CI; F4 change-log process | Every template linked from a page and opens in tests |
| **1.0 Reviewed** | Dec 2027 | Practitioner review (one ESG assurance person, one customs/CBAM person), PDF edition, Zenodo DOI | Each page status "reviewed" or clearly marked draft |

After each regulatory change: update `data/regulations.yml`, re-run the
worked examples, add a dated entry to `docs/changelog.md`.

## 5. Work breakdown for 0.1 (next three weeks)

1. Create the GitHub repo `esg-workflows-handbook`, enable Pages (source:
   GitHub Actions). *Blocked on you: see README.*
2. Push this scaffold. CI builds the site with every page marked Planned.
3. Write `start-here/triage.md`: a decision tree across the four regimes.
4. Write `foundations/evidence-locker.md`: hashing source files (SHA-256),
   naming, retention, linking each reported number to its evidence.
5. Write `foundations/one-dataset-many-reports.md`: the reuse map.
6. Add `scripts/check_regulations.py`: warn when `last_checked` is older
   than 90 days.
7. Link the handbook from the portfolio site and the GitHub profile README.

## 6. Templates and tools (by release)

| Release | Templates (Excel / Word) | Tools |
|---|---|---|
| 0.2 | CBAM goods register; supplier emissions data request (cover letter, linked to the Commission's official communication template rather than copying it); embedded-emissions workbook; declaration prep checklist | `cbam` Python module: threshold check, embedded emissions (direct + indirect + precursors), certificate cost estimate; browser calculator |
| 0.3 | Scope 3 screening matrix; inventory workbook; supplier engagement letter; recalculation policy | Screening tool; spend-based calculator with data-quality score; Monte Carlo uncertainty demo |
| 0.4 | VSME Basic module workbook; Comprehensive add-on; questionnaire response bank | VSME readiness checker |
| 0.5 | Double materiality workbook (impact and financial scoring); IRO register; datapoint gap list | DMA scoring tool; ESRS gap analysis |

Calculations live in a small Python package in `esgcalc/` (added in 0.2)
with tests. Browser tools run fully client-side, like the lab handbook's
gap analysis, so no company data leaves the user's machine.

## 7. Quality rules

- **Own words only.** No copying of GHG Protocol, EFRAG guidance or paid
  standards. EU legal texts are cited by article and linked.
- **Every number traceable.** Worked examples use made-up companies and
  realistic numbers, and are recomputed by tests on every build.
- **Every emission factor sourced.** Name, version, year, unit and licence.
  Prefer open sources (DEFRA/DESNZ, EEA, EU CBAM default values, EXIOBASE)
  and flag licensed ones (ecoinvent).
- **Status on every page:** planned -> draft -> examples-checked ->
  reviewed.
- **Not advice.** Banner on every page; the regulation and the competent
  authority take priority.
- **Plain English, short sentences.** Many readers work in a second
  language.

## 8. Risks

| Risk | Effect | Mitigation |
|---|---|---|
| Rules keep moving (CBAM secondary acts, ESRS publication, national transposition) | Pages go stale | Regulation tracker with review dates; CI warning; dated changelog |
| Scope creep across four regimes | Nothing reaches 1.0 | One track per release; backlog for everything else |
| Licensing of emission-factor databases | Cannot publish factors | Open factors only in examples; licensed sources described, not copied |
| No practitioner reviewer | 1.0 lacks credibility | Ask from 0.2 onward; LinkedIn ESG/CBAM groups; former colleagues |
| Overlap with ValantiData commercial work | Giving away the product | Handbook = method (open); ValantiData = automation, evidence locker service and support (paid) |

## 9. Backlog (after 1.0)

EU Taxonomy alignment workflow; CSDDD basics for suppliers; EUDR due
diligence; packaging (PPWR) and EPR reporting, including Lithuanian GPAIS;
product carbon footprint (ISO 14067); Lithuanian and Maltese language
summaries; ESRS XBRL tagging walkthrough with Arelle.

## 10. Sources

- Council of the EU, Omnibus I final adoption, 24 Feb 2026; Directive (EU) 2026/470
- European Commission, delegated acts on simplified ESRS and the voluntary standard, 3 Jul 2026 (EFRAG news page)
- DG TAXUD, Carbon Border Adjustment Mechanism: https://taxation-customs.ec.europa.eu/carbon-border-adjustment-mechanism_en
- Regulation (EU) 2023/956 and Regulation (EU) 2025/2083 (EUR-Lex)
- GHG Protocol Corporate Value Chain (Scope 3) Standard
