---
step: "V6"
status: draft
last_checked: 2026-11-21
---

# V6 Publishing and updating

!!! warning "Not legal advice"
    The voluntary standard does not require you to publish or to get
    assurance. This page suggests a practical way to do both well. The
    numbers in the worked example are made up.

## In one sentence

Have the report checked and approved, publish it in a form people can use,
send it to those who asked, and update it every year, restating earlier
figures openly when they change.

## Who does this and when

The owner or board approves; whoever prepared the report publishes it.
Once a year, after the year's data is in. Work back from the earliest date
a customer or bank needs it.

## Inputs

- The finished report: B1 to B11, and C1 to C9 under Option B
  ([V2](v2-basic.md), [V4](v4-comprehensive.md)).
- The evidence behind every figure ([F1](../foundations/evidence-locker.md)).
- The base-year policy, if figures changed since last year
  ([S8](../scope3/s8-base-year.md)).

## Steps

### 1. Review before you publish

A second person checks each figure against its source and the arithmetic.
The standard requires no assurance; a careful internal review is the
minimum. Some customers or banks may ask for more.

### 2. Get it approved

The board or owner approves the report, as for the annual accounts. Record
the date.

### 3. Choose the format

- **A PDF** on your website is easy to share and to find.
- **EFRAG's digital template** (an Excel file with an XBRL taxonomy behind
  it) gives the figures in a form that customers' and banks' systems can
  read. Use the version for the 2026 standard.

### 4. Send it to those who asked

Send the report to every customer and bank that asked, with a short note
([V5](v5-requests.md)). One report answers many questionnaires.

### 5. Update every year

Report the same year as your annual accounts, with last year's figures
next to this year's, so readers can see the trend.

### 6. Restate openly when earlier figures change

If last year's figures change, because of an acquisition, a new method or
an error ([S8](../scope3/s8-base-year.md)), show both: the figure as
published and as restated, with the reason. Rebase any target that uses
the restated year.

## Worked example

**Publishing the 2026 report.** Gozo Fresh Foods Ltd (fictional) must
send its report by **30 April 2027** (the supermarket's deadline,
[S3](../scope3/s3-data-plan.md)). All dates and numbers are made up.

| Date | Step |
|---|---|
| 31 Mar 2027 | All data in; Scope 3 inventory finished (S3, S9) |
| 9 Apr 2027 | Second person reviews the report against the evidence locker |
| 15 Apr 2027 | Board approves the report |
| 20 Apr 2027 | Published on the website as PDF, with the EFRAG digital template; sent to the supermarket and the bank |

Published **10 days** before the deadline.

**Updating in 2028: restating 2026.** In July 2027 Gozo bought all of
Island Cold Store ([S8](../scope3/s8-base-year.md)). Under its policy, it
restates 2026 in its 2027 report:

| 2026 figure | As published | Restated | Why |
|---|---|---|---|
| Scope 1 and 2 (tCO2e) | 1,800.00 | 2,100.00 | Island Cold Store's 300 tCO2e now inside the boundary |
| Scope 3 (tCO2e) | 5,752.59 | 5,755.84 | Acquisition, new spend factor and survey error ([S8](../scope3/s8-base-year.md)) |

**Rebasing the C3 target.** The target was −30% on 2026 Scope 1 and 2
([V4](v4-comprehensive.md)). On the restated base: 2,100 × 0.70 =
**1,470 tCO2e** in 2030, instead of 1,260.

| Year | Path on the restated base (tCO2e) |
|---|---|
| 2026 (base) | 2,100 |
| 2027 | 1,942.5 |
| 2028 | 1,785 |
| 2029 | 1,627.5 |
| 2030 (target) | 1,470 |

Gozo shows both the original and the rebased target, and why it changed.
Readers can then see that the higher number comes from the acquisition, not
from going backwards.

## Common mistakes

- **Publishing without a review.** No assurance is required, but errors
  found by a customer cost more than a second pair of eyes.
- **A PDF only.** Customers' and banks' systems read the digital template
  more easily.
- **Silently changing last year's figures.** Show the published and the
  restated figure, and why.
- **Keeping a target on an old base.** Rebase it when the base year is
  restated.
- **Updating the website but not the people who asked.** Send them the new
  report too.

## Evidence to keep

- The approved report, with the approval date.
- The review notes.
- Each restatement: old and new figure, reason and calculation.

File them in the evidence locker (see
[F1](../foundations/evidence-locker.md)).

## Templates and tools

- EFRAG's digital template and XBRL taxonomy for the voluntary standard:
  [efrag.org](https://www.efrag.org/en/vs-digital-template-and-xbrl-taxonomy).
- [`esgcalc.vsme.linear_target_path`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/esgcalc/vsme.py):
  the rebased target path above.

## Reuse in other reports

The published report is the single source for every questionnaire
([V5](v5-requests.md)). The same restatements apply to your Scope 3
inventory and to any figures you gave customers. See
[F3](../foundations/one-dataset-many-reports.md).

## Sources

Facts come from `data/regulations.yml` (ids `vsme`, `vs-digital-template`,
`ghgp-base-year`), last checked 20 November 2026.

- Commission Delegated Regulation (EU) 2026/1560 (voluntary standard):
  [EUR-Lex](https://eur-lex.europa.eu/eli/reg_del/2026/1560/oj/eng)
- EFRAG, VS Digital Template and XBRL Taxonomy:
  [efrag.org](https://www.efrag.org/en/vs-digital-template-and-xbrl-taxonomy)
