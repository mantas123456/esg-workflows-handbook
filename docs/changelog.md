# Changelog

What changed in the handbook, newest first. Regulatory updates are listed
here too, with the date the facts were re-checked. See the
[roadmap](roadmap.md) for what comes next.

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
