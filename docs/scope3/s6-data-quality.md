---
step: "S6"
status: draft
last_checked: 2026-11-20
---

# S6 Data quality scoring

!!! warning "Not legal advice"
    The scoring guide below is this handbook's own. The scores in the worked
    example are made up.

## In one sentence

Score every inventory line on five indicators with one shared scoring
guide, roll the scores up by category weighted by emissions, and set a
target for the significant categories.

## Who does this and when

The inventory lead, line by line while calculating ([S4](s4-methods.md)),
and a second person who checks a sample. Use the same guide every year so
the scores can be compared.

## Inputs

- Every inventory line with its source and basis.
- The scoring guide below, or your own, written down before you start.
- The concepts in [F2](../foundations/data-quality.md).

## Steps

### 1. Agree a scoring guide

Without a guide, two people give the same line different scores. This
handbook uses:

| Indicator | 1 (very good) | 3 (fair) | 5 (very poor) |
|---|---|---|---|
| Technology | The supplier's own data for this product and process | An average for a similar product or process | A sector average or an unrelated product |
| Time | The reporting year | Within about 5 years | Older than 10 years, or unknown |
| Geography | The country, or the site, where it was made | The same region, or a nearby country as a proxy | Global or another continent |
| Completeness | All sites and the whole year | Most sites or most of the year | A small or unknown part |
| Reliability | Measured and verified | Measured but not verified, or partly estimated | A rough estimate or assumption |

Use 2 and 4 for cases in between.

### 2. Score each line

Score each line on all five indicators, and write one sentence on why.
The line's score is their mean.

### 3. Roll up by category, weighted by emissions

The category's score is the mean of its lines weighted by their tCO2e.
The inventory's score is the same across all lines.

### 4. Set a target and compare

Set a target score for the significant categories, for example **2.5**.
Categories above it go to the top of next year's data plan
([S3](s3-data-plan.md)).

### 5. Report the scores

Report each category's score next to its emissions ([S9](s9-reporting.md)),
with the guide, so readers can see how good the data behind each number
is.

## Worked example

Gozo Fresh Foods Ltd (fictional) scores every line of its 2026 inventory
([S4](s4-methods.md)) and sets a target of **2.5** for its significant
categories. All scores are made up.

| # | Category | tCO2e | Score | Significant? | Meets the 2.5 target? |
|---|---|---|---|---|---|
| 1 | Purchased goods and services | 4,845.00 | 1.87 | Yes | Yes |
| 2 | Capital goods | 135.59 | 3.00 | Yes | No |
| 3 | Fuel- and energy-related activities | 180.00 | 2.00 | Yes | Yes |
| 4 | Upstream transportation and distribution | 175.00 | 1.79 | Yes | Yes |
| 5 | Waste generated in operations | 31.00 | 2.80 | No | – |
| 6 | Business travel | 10.00 | 3.00 | No | – |
| 7 | Employee commuting | 117.00 | 2.20 | Yes | Yes |
| 9 | Downstream transportation and distribution | 114.00 | 2.55 | Yes | No |
| 12 | End-of-life treatment of sold products | 92.50 | 2.85 | Yes | No |
| 15 | Investments | 75.00 | 1.80 | No | – |
| | **Whole inventory** | **5,775.09** | **1.94** | | |

Three significant categories miss the target: **2, 9 and 12**. Category 2
rests on a spend-based factor; categories 9 and 12 on customer figures and
published averages. They go into the 2027 data plan.

The whole inventory scores **1.94**, because category 1, with most of the
emissions, now rests largely on supplier data. That is the point of the
emissions weighting.

In Python, with
[`esgcalc`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/esgcalc/quality.py):

```python
from esgcalc.quality import DataQuality, category_score

# category 12: three packaging lines and food waste, (tCO2e, scores)
lines = [(8.0, DataQuality(3, 1, 3, 2, 2)), (7.5, DataQuality(3, 1, 3, 2, 2)),
         (2.0, DataQuality(3, 1, 3, 2, 2)), (75.0, DataQuality(3, 2, 3, 3, 4))]
print(round(category_score(lines), 2))   # 2.85
```

## Common mistakes

- **No written guide.** Scores become personal opinions and cannot be
  compared year to year.
- **A simple average across lines.** A large poor line then hides behind
  many small good ones. Weight by emissions.
- **Scoring once and forgetting.** Score every year with the same guide.
- **Treating a good score as a small uncertainty.** They are related but
  not the same. Report both ([F2](../foundations/data-quality.md)).
- **Generous scores for your own estimates.** Ask a second person to check
  a sample.

## Evidence to keep

- The scoring guide, dated.
- Each line's five scores and the reason for them.
- The category and inventory scores, and the target.

File them in the evidence locker (see
[F1](../foundations/evidence-locker.md)).

## Templates and tools

<!-- generated from data/workflows.yml templates: do not edit by hand -->
- **[Scope 3 inventory workbook](../downloads/scope3-inventory.xlsx)** (Excel): A Scope 3 inventory line by line, with spend-based, average-data and supplier-specific tabs, a data-quality score and a 95% uncertainty on every line, and a summary by category.
<!-- end generated templates -->

- [`esgcalc.quality.DataQuality` and `category_score`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/esgcalc/quality.py).

## Reuse in other reports

Many customer questionnaires ask how much of Scope 3 rests on primary
(supplier) data. The scores and the method mix ([S4](s4-methods.md))
answer that, and the same scores sit next to the ESRS E1 figures. See [F3](../foundations/one-dataset-many-reports.md).

## Sources

Facts come from `data/regulations.yml` (ids `ghgp-scope3-categories`,
`esrs-e1-scope3`), last checked 20 November 2026.

- GHG Protocol Corporate Value Chain (Scope 3) Standard, data quality
  indicators (cited, not copied):
  [ghgprotocol.org](https://ghgprotocol.org/corporate-value-chain-scope-3-standard)
