# Changelog

What changed in the handbook, newest first. Regulatory updates are listed
here too, with the date the facts were re-checked. See the
[roadmap](roadmap.md) for what comes next.

## 1.0 (21 November 2026)

All four tracks, self-reviewed and corrected. Every page is still a draft:
no external practitioner has reviewed the handbook yet.

**Self-review and fixes**

- A self-review read each track as a CBAM customs specialist, a GHG verifier
  and a CSRD limited-assurance provider: 32 findings, none critical, all
  fixed ([review on GitHub](https://github.com/mantas123456/esg-workflows-handbook/blob/main/review/self-review-1.0.md)).
- The key facts were re-read in the Official Journal: the consolidated CBAM
  Regulation and its implementing acts on verification (2025/2546), free
  allocation (2025/2620) and carbon prices paid (2026/2498); the
  consolidated Accounting Directive (Articles 19a, 29a, 29d, 34, 40a); the
  revised ESRS (2026/1563); the voluntary standard (2026/1560); and the
  Taxonomy Regulation (Article 8). 20 facts were added or corrected.
- Corrections a reader should know about:
  - **Scope 3 (Gozo Fresh Foods):** the cold store's emissions were counted
    in two categories; now counted once. The total is **5,750 ± 420
    tCO2e** (was 5,780 ± 420).
  - **ESRS codes:** health and safety is **S1-13**, not S1-14.
  - **Value-chain cap:** it covers only the datapoints in Annex II of the
    voluntary standard, fewer for companies with 10 employees or fewer (C3,
    V5).
  - **CBAM data in Scope 3:** add the electricity CBAM leaves out for steel
    and aluminium, and remove the default-value mark-up (CB3, CB4, CB9,
    F3).
  - **Malta:** only parts of Act I of 2026 are in force (Legal Notice 61
    of 2026); no commencement notice for Legal Notice 39 was found.
- New content: groups and non-EU parents in C1, the EU Taxonomy step in
  C4, the CBAM guarantee (CB2), verification opinion and site visits (CB6),
  the carbon-price conversion (CB7), the free allocation formula (CB8), and
  the declaration review (CB9).

**PDF edition and citation**

- Each release now has a [PDF edition](https://github.com/mantas123456/esg-workflows-handbook/releases/latest) and a ZIP of the templates,
  built in CI (`scripts/build_pdf.py`).
- A citation file (`CITATION.cff`). A DOI will follow once releases are
  archived on Zenodo.

## 0.6 Polish (21 November 2026)

Keeping the handbook current, consistent and usable. No new rules: the
facts are as checked on 20 November 2026.

**New pages**

- [F4 Keeping up with changes](foundations/keeping-up.md): one fact list,
  a 90/180-day re-check cycle, and a watch list of known dates to the end
  of 2027.
- [All tools](tools/index.md) and [All templates](templates.md), with the
  steps that use each one.

**Checks**

- `scripts/check_regulations.py` runs in CI: a warning when a fact has not
  been re-checked for 90 days, a failed build at 180.
- Tests now check that every written page follows the chapter format and
  has a `last_checked` date, that every template is linked from a step, and
  that every tool has a page, a step and a browser test.
- `scripts/check_links.py` checks the external links by hand.
- Tool links in `data/workflows.yml` now name real tool pages (CB1, CB8, F2).

**Accessibility**

- The six browser tools pass axe-core checks in light and dark mode, and
  work with the keyboard alone: stronger link, code and button contrast,
  underlined links, labelled table headers, ordered headings.

**Report an error**

- A GitHub [issue form](https://github.com/mantas123456/esg-workflows-handbook/issues/new?template=report-error.yml)
  asks for the page, the problem and the official source.

**Known gaps:** EUR-Lex refuses automated requests, so its links are
checked by hand; the accessibility check covers the tools, not every page;
the open fact checks listed under 0.5 remain open.

## 0.5 CSRD / ESRS track (20 November 2026)

The CSRD and revised ESRS after Omnibus I, with Mediterranean Logistics
Group (fictional, Malta, 1,300 employees, EUR 520 m turnover) and its
suppliers Gozo Fresh Foods and Melita Metals from the other tracks, so the
value chain links all four tracks. All pages are drafts, reviewed once in this
release as a limited-assurance provider would, not yet by a practitioner.

**New pages (draft)**

- [C1 Am I in scope after Omnibus I?](csrd/c1-scope.md),
  [C2 Double materiality assessment](csrd/c2-dma.md),
  [C3 Value chain and data requests](csrd/c3-value-chain.md),
  [C4 General disclosures](csrd/c4-general.md),
  [C5 Climate (E1)](csrd/c5-climate.md),
  [C6 Other topical standards](csrd/c6-topical.md),
  [C7 Datapoint gap analysis](csrd/c7-gap-analysis.md),
  [C8 Assurance readiness](csrd/c8-assurance.md),
  [C9 Digital tagging and publication](csrd/c9-tagging.md).
- C3 keeps every request to smaller suppliers within the value-chain cap;
  C5 brings Gozo's Scope 3 and Melita's CBAM data into E1.

**New tools and templates**

- [DMA scoring](tools/dma-scoring.md) and [ESRS gap check](tools/esrs-gap.md),
  in your browser.
- Downloads: double materiality assessment workbook, IRO register and ESRS
  datapoint gap list (Excel, generated from the handbook's datapoint list).
- `esgcalc.dma` (impact and financial materiality, topic roll-up) and
  `esgcalc.csrd` (scope test, value-chain cap, gap summary).
- `data/esrs_datapoints.yml`: the standards and the key datapoints, linked
  to the handbook's datasets.

**Fixes**

- The About sheet of the Scope 3 and VSME workbooks now names their
  example company (Gozo Fresh Foods), not Melita Metals.

**Facts and sources (checked 20 November 2026)**

- Scope after Omnibus I (Directive (EU) 2026/470): more than 1,000
  employees and more than EUR 450 m net turnover; transposition by
  19 March 2027.
- Stop-the-clock (Directive (EU) 2025/794): companies that never reported
  start with financial year 2027.
- Revised ESRS (Delegated Regulation (EU) 2026/1563): mandatory from
  financial year 2027; materiality method, structure, phase-ins, E1 Scope 3.
- Limited assurance only; what the opinion covers; the sustainability
  statement in the management report; tagging not yet mandatory.
- Malta: Legal Notice 39 of 2026 and Act I of 2026 (original CSRD).

**Known gaps:** EUR-Lex did not load, so Articles 19a, 29a, 29d and 34 of
Directive 2013/34/EU and the scope article were read through the
consolidated CSRD and summaries; the phase-in years, Scope 2 on both bases
and the disclosure requirement numbers are to check against the Official
Journal; Malta's Legal Notice 39 start date and its Omnibus I transposition
are not confirmed; limited assurance standards and tagging rules are not
adopted yet.

## 0.4 VSME track (20 November 2026)

The voluntary standard for smaller companies, with Gozo Fresh Foods Ltd
(fictional, Malta) reusing its Scope 3 data. All pages are drafts, not yet
reviewed by a practitioner.

**New pages (draft)**

- [V1 Choosing the modules](vsme/v1-modules.md),
  [V2 Basic Module data collection](vsme/v2-basic.md),
  [V3 GHG emissions for VSME](vsme/v3-ghg.md),
  [V4 Comprehensive module](vsme/v4-comprehensive.md),
  [V5 Answering customer and bank requests](vsme/v5-requests.md),
  [V6 Publishing and updating](vsme/v6-publishing.md).

**New tools and templates**

- [VSME readiness](tools/vsme-readiness.md): completeness by module and a
  to-do list, in your browser.
- Downloads: VSME Basic Module workbook (Excel, generated from the
  handbook's datapoint list) and questionnaire response bank (Word).
- `esgcalc.vsme`: energy total, GHG intensity, accident rate, water
  consumption, pay gap, turnover rate, target path and readiness.
- `data/vsme_datapoints.yml`: every Basic datapoint and Comprehensive
  disclosure in the handbook's own words, with how far each was checked.

**Facts and sources (checked 20 November 2026)**

- The voluntary standard is Delegated Regulation (EU) 2026/1560, published
  21 September 2026, applying from financial year 2027.
- Module structure, Basic metrics, and EFRAG's digital template and XBRL
  taxonomy (version 2.0.0, 4 November 2026).
- The value-chain cap, now with its article (Directive 2013/34/EU, Article
  29b(4)) and conditions.

**Known gaps:** the full wording of the 2026 act's Annex I and II was not
re-read (most Basic metric details come from the 2025 Recommendation); the
Comprehensive Module is covered at topic level; two definitions (pay gap,
turnover rate) are flagged for checking.

## 0.3 Scope 3 track (20 November 2026)

The full Scope 3 track, from boundary to reporting, with one fictional
company (Gozo Fresh Foods Ltd, Malta) followed through every step, and a
foundation page on data quality and uncertainty. All pages are drafts, not
yet reviewed by a practitioner.

**New pages (draft)**

- [S1 Boundary](scope3/s1-boundary.md), [S2 Screening](scope3/s2-screening.md),
  [S3 Data plan](scope3/s3-data-plan.md), [S4 Methods](scope3/s4-methods.md),
  [S5 Emission factors](scope3/s5-emission-factors.md),
  [S6 Data quality scoring](scope3/s6-data-quality.md),
  [S7 Supplier engagement](scope3/s7-suppliers.md),
  [S8 Base year](scope3/s8-base-year.md), [S9 Reporting](scope3/s9-reporting.md).
- [F2 Data quality and uncertainty](foundations/data-quality.md): emissions
  treated as measurements, with an uncertainty budget and Monte Carlo.

**New tools and templates**

- [Scope 3 screening](tools/scope3-screening.md) and
  [uncertainty demo](tools/uncertainty-demo.md), in your browser.
- Downloads: Scope 3 screening matrix and inventory workbook (Excel),
  supplier letter and base-year recalculation policy (Word).
- `esgcalc`: Scope 3 methods (spend-based with deflation and currency,
  average-data, supplier-specific, hybrid), screening, supplier coverage,
  organisational boundary, factor choice, base-year recalculation, data
  quality and uncertainty (analytic and seeded Monte Carlo).

**Facts and sources (checked 20 November 2026)**

- Added: the GHG Protocol Scope 3 Standard and its revision timeline
  (draft for consultation estimated Q2 2027), organisational boundary
  approaches and the December 2025 revision proposal, the 15 categories,
  base-year recalculation, the Land Sector and Removals Standard (in effect
  from 1 January 2027), revised ESRS E1 Scope 3 requirements, and the
  JCGM GUM documents.
- New `data/factor_sources.yml`: DESNZ 2026 (Open Government Licence) and
  EEA (CC BY 4.0) may be quoted; EXIOBASE 3.9+ (non-commercial) and
  ecoinvent (licensed) are linked only; EPA USEEIO and EU legal texts still
  to check.

**Known gaps** (see the note on S1): land use and land-use change, the ESRS
E1 Scope 3 phase-in (not confirmed), and spend-based factor sources for
companies that cannot use EXIOBASE.

## 0.2 CBAM track (20 November 2026)

The full CBAM track, from the scope check to records, with one fictional
importer (Melita Metals Ltd, Malta) followed through every step. All
pages are drafts, not yet reviewed by a practitioner.

**New pages (draft)**

- [CB1 Scope check](cbam/cb1-scope-check.md),
  [CB2 Authorisation](cbam/cb2-authorisation.md),
  [CB3 Supplier data](cbam/cb3-supplier-data.md),
  [CB4 Embedded emissions](cbam/cb4-embedded-emissions.md),
  [CB5 Precursors](cbam/cb5-precursors.md),
  [CB6 Verification](cbam/cb6-verification.md),
  [CB7 Carbon price paid](cbam/cb7-carbon-price-paid.md),
  [CB8 Certificates](cbam/cb8-certificates.md),
  [CB9 Declaration](cbam/cb9-declaration.md),
  [CB10 Records](cbam/cb10-records.md).

**New tools and templates**

- [CBAM calculator](tools/cbam-calculator.md): threshold, embedded
  emissions, certificates, cost and quarterly holding, in your browser.
- Downloads: CBAM goods register and embedded emissions workbook (Excel),
  supplier data request letter and declaration checklist (Word).
- `esgcalc`: the Python package behind every number. Worked examples,
  workbook formulas and the browser tool are all checked against it on
  every build.

**Regulatory facts (re-checked 20 November 2026)**

- Added CBAM facts with article references: Annex I goods, exempt origins
  (Annex III), direct-only sectors (Annex II), authorisation and its
  deadlines, the 2026 transitional rule, actual vs default values,
  verification, complex goods and precursors, carbon price paid
  (including Implementing Regulation (EU) 2026/2498 of 16 November 2026),
  the free allocation adjustment and CBAM factor, declaration content,
  penalties and record keeping.
- Corrected: default values. Implementing Regulation (EU) 2026/1740
  removed the pre-calculated marked-up columns, so the mark-up is applied
  to the base value; fertilisers have a 1% mark-up; electricity default
  values are set separately and carry no mark-up.
- Corrected: the threshold exempts imports that **do not exceed** 50
  tonnes, so exactly 50 tonnes is exempt.

**Known gaps** (see the note on CB1): electricity imports, customs
special procedures, repurchase of certificates, and the exact formulas for
the free allocation adjustment and the carbon-price-paid conversion.

## 0.1 Skeleton (20 November 2026)

First public release. All four tracks have a placeholder page for every
step; the pages below are written as drafts.

**New pages (draft)**

- [T1 Which regime applies to me?](start-here/triage.md): a decision tree
  for CBAM, CSRD, VSME and Scope 3 requests, with the legal test and source
  for each branch, and three worked examples.
- [T2 Regulation timeline](start-here/timeline.md): key dates for
  CSRD/ESRS, VSME and CBAM, one table per regime.
- [F1 Evidence locker and audit trail](foundations/evidence-locker.md):
  folder structure, file naming, SHA-256 hashing, evidence registers and
  CBAM retention periods.
- [F3 One dataset, many reports](foundations/one-dataset-many-reports.md):
  a reuse map showing which data feeds CBAM, Scope 3, VSME and ESRS E1.

**New tools and data**

- `scripts/hash_evidence.py`: builds and verifies an evidence register of
  SHA-256 hashes. Runs offline.
- `data/datasets.yml`: a data dictionary for the six core datasets,
  rendered into F3.
- Workflow map and site navigation generated from `data/workflows.yml`.
- Worked-example numbers re-computed by tests on every build.

**Regulatory facts (re-checked 20 November 2026)**

Every fact in `data/regulations.yml` was re-verified against EUR-Lex,
DG TAXUD and the Commission. Changes:

- Revised ESRS: now dated precisely as Delegated Regulation (EU)
  2026/1563, published 21 September 2026, in force 10 November 2026,
  mandatory from financial years starting 1 January 2027.
- CBAM threshold: exempt when imports **do not exceed** 50 tonnes a year
  (so exactly 50 tonnes is exempt); hydrogen and electricity not covered;
  exceeding the threshold brings in the whole year's imports.
- Added: Omnibus I transposition deadlines, the wave 1 exemption option,
  the value-chain cap, the CBAM definitive period start, the 50% quarterly
  certificate holding rule, and CBAM record-keeping periods
  (Articles 7(6) and 9(3)).
- Sources moved from law-firm articles to EUR-Lex, DG TAXUD and
  Commission pages.
