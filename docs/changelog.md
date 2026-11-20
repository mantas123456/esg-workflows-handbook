# Changelog

What changed in the handbook, newest first. Regulatory updates are listed
here too, with the date the facts were re-checked. See the
[roadmap](roadmap.md) for what comes next.

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
