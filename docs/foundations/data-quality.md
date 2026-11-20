---
step: "F2"
status: draft
last_checked: 2026-11-20
---

# F2 Data quality and uncertainty

!!! warning "Not legal advice"
    This page explains a measurement-science way to treat emissions data.
    The scores and uncertainties in the worked example are made up.

## In one sentence

Treat every emissions number as a measurement: score how good its data
is, state how uncertain it is, combine the uncertainties properly, and
report the result with a coverage interval and an uncertainty budget that
shows where to improve.

## Who does this and when

Whoever calculates the inventory ([S4](../scope3/s4-methods.md)), for
every line, at the same time as the calculation. It takes little extra
effort if done then, and a lot if done later.

## Inputs

- The inventory lines: inputs, factors and sources ([S4](../scope3/s4-methods.md),
  [S5](../scope3/s5-emission-factors.md)).
- What you know about each input: was it measured, invoiced, surveyed,
  estimated? Was the supplier's figure verified?
- Any uncertainty the factor's publisher states.

## Steps

### 1. State the measurand

Say exactly what the number is, as a lab states what it measures. For
example: "Category 1 emissions of Gozo Fresh Foods Ltd, calendar year 2026,
in tonnes of CO2e, cradle to gate." A vague measurand cannot have a clear
uncertainty.

### 2. Write the measurement model

Write how the result is calculated from its inputs. For a Scope 3
category it is usually a sum of lines, each a product:

```text
E = sum over lines of (activity_i x factor_i)     or a supplier's allocated share
```

### 3. Score the data quality of each line

Score five indicators from 1 (very good) to 5 (very poor):

| Indicator | Question |
|---|---|
| Technology | Does the data match how the goods were really made? |
| Time | Is it for the reporting year? |
| Geography | Is it for the place of production? |
| Completeness | Does it cover the whole activity and all sites? |
| Reliability | Was it measured and verified, or estimated? |

The line's score is the mean of the five. The category's score is the
mean of its lines **weighted by their emissions**, so a large poor line is
not hidden by many small good ones.

### 4. Evaluate the uncertainty of each input

Give each input a 95% uncertainty, as a ± percentage. Two kinds of
evidence, as in a lab:

- **from data**: the spread of repeated readings or of several suppliers'
  values;
- **from other knowledge**: the factor publisher's statement, the
  supplier's verification, or a documented judgement (an unverified
  supplier figure might be ±15%; a sector spend factor ±50% or more).

Write down where each value comes from.

### 5. Combine

For independent inputs, as in the Guide to the expression of uncertainty
in measurement (GUM):

- **a product** (activity × factor): the **relative** uncertainties add in
  quadrature: u = √(u_activity² + u_factor²);
- **a sum** of lines: the **absolute** uncertainties add in quadrature:
  U = √(U₁² + U₂² + …).

If the same factor is used on many lines, those lines are **correlated**:
the simple sum rule then understates the uncertainty. Treat such lines
together, or use Monte Carlo with the shared factor drawn once.

### 6. Report a coverage interval

Report the result with its expanded uncertainty and coverage probability,
for example "4,850 ± 410 tCO2e (95%)". Round the uncertainty to two
significant figures, and the result to the same digit.

### 7. Use Monte Carlo when uncertainties are large or skewed

The sum and product rules are approximations. When uncertainties are
large (more than about 30%) or the distributions are skewed, as emission
factors often are, simulate: draw each input from its distribution many
times and read the 2.5th and 97.5th percentiles of the result (the method
of GUM Supplement 1). The interval is then usually **asymmetric**.

### 8. Read the uncertainty budget

List each line's share of the combined variance. The largest shares tell
you where better data would help most. This is where the next year's
data plan starts ([S3](../scope3/s3-data-plan.md)).

## Worked example

**Measurand:** category 1 emissions of Gozo Fresh Foods Ltd (fictional),
2026, tCO2e, from the inventory in [S4](../scope3/s4-methods.md). All
scores and uncertainties are made up.

**Uncertainty budget**

| Line | tCO2e | Basis | DQ score | ±95% | U (tCO2e) | Share of variance |
|---|---|---|---|---|---|---|
| Maltese Farmers Cooperative | 900.00 | Supplier figure, verified | 1.2 | 10.0% | 90.00 | 4.9% |
| Sicilian Tomato Co | 1,200.00 | Supplier figure, verified | 1.4 | 10.0% | 120.00 | 8.8% |
| Gozo Greens Ltd | 500.00 | Supplier figure, not verified | 1.8 | 15.0% | 75.00 | 3.4% |
| Island Dairy Ltd | 420.00 | Supplier figure, not verified | 1.8 | 15.0% | 63.00 | 2.4% |
| Mediterranean Oils | 200.00 | Supplier figure, partial year | 2.4 | 20.0% | 40.00 | 1.0% |
| Other ingredient suppliers | 686.44 | Spend-based sector factor | 3.2 | 50.0% | 343.22 | 71.7% |
| Services (cleaning, IT, maintenance) | 63.56 | Spend-based sector factor | 3.2 | 50.0% | 31.78 | 0.6% |
| Cardboard packaging | 320.00 | Weighed tonnes, DESNZ factor | 2.0 | 20.6% | 65.97 | 2.7% |
| Plastic film packaging | 375.00 | Weighed tonnes, DESNZ factor | 2.0 | 20.6% | 77.31 | 3.6% |
| Glass jars | 180.00 | Weighed tonnes, DESNZ factor | 2.0 | 20.6% | 37.11 | 0.8% |
| **Category 1** | **4,845.00** | | **1.87** | **8.4%** | **405.23** | **100%** |

The packaging lines combine the weighed tonnes (±5%) and the factor
(±20%) by the product rule: √(0.05² + 0.20²) = 20.6%. The category's
data-quality score, weighted by emissions, is **1.87**.

**Combined result (sum rule):** 4,845.00 ± 405.23 tCO2e, an interval of
4,439.77 to 5,250.23 tCO2e.

**Reported:** **4,850 ± 410 tCO2e (95%)**.

**Monte Carlo check.** Each line drawn from a lognormal whose 97.5th
percentile matches its stated uncertainty, 200,000 draws, seed 20260101:

| | Sum rule | Monte Carlo |
|---|---|---|
| Central value | 4,845.0 | 4,859.7 (median) |
| 95% interval | 4,439.8 to 5,250.2 | 4,546.8 to 5,250.2 |

The Monte Carlo interval is **asymmetric**: it reaches as high as the sum
rule but not as low, because the lognormal lines cannot fall as far below
their central value as they can rise above it.

**What the budget says.** One line, the spend-based estimate for the other
ingredient suppliers, contributes **71.7%** of the variance. Getting
supplier data for the next largest of those suppliers
([S3](../scope3/s3-data-plan.md)) would shrink the category's uncertainty
more than anything else Gozo Fresh Foods could do.

A browser Monte Carlo demo is planned for this release.

In Python, with
[`esgcalc`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/esgcalc/quality.py):

```python
from esgcalc.quality import round_result, sum_uncertainty, variance_shares

values = [900, 1200, 500, 420, 200, 686.44, 63.56, 320, 375, 180]
u95 = [0.10, 0.10, 0.15, 0.15, 0.20, 0.50, 0.50, 0.2062, 0.2062, 0.2062]
total = sum_uncertainty(values, u95)
print(round_result(total.value, total.u95_abs))      # (4850.0, 410.0)
print(round(variance_shares(values, u95)[5], 3))     # 0.717
```

## Common mistakes

- **No measurand.** "Our Scope 3" is not specific enough to have an
  uncertainty. State scope, year, boundary and unit.
- **Adding percentages.** Relative uncertainties add in quadrature for a
  product, absolute ones for a sum, not in a straight line.
- **Ignoring correlation.** The same factor on many lines is one source of
  uncertainty, not many independent ones.
- **False precision.** "4,845.00 tCO2e" with ±8% claims more than you
  know. Round as a lab would.
- **Treating the score as the uncertainty.** A data-quality score says how
  good the data is; it is not a ± value. Report both.
- **Not using the budget.** The point of the uncertainty budget is to show
  where to improve.

## Evidence to keep

- For each line: the data-quality scores and the basis for its
  uncertainty.
- The uncertainty budget and the Monte Carlo settings (draws, seed), so
  the result can be reproduced.

File them in the evidence locker (see [F1](evidence-locker.md)).

## Templates and tools

- [`esgcalc.quality`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/esgcalc/quality.py):
  `DataQuality`, `category_score`, `sum_uncertainty`, `product_uncertainty`,
  `variance_shares`, `round_result`, `gsd_from_u95` and the seeded
  `monte_carlo_sum`.

## Reuse in other reports

The same scores and uncertainties apply to every report that uses these
numbers: ESRS E1, VSME answers and customer questionnaires. CBAM data from
verified suppliers scores well on reliability. See
[F3](one-dataset-many-reports.md).

## Sources

Facts come from `data/regulations.yml` (ids `jcgm-gum`,
`ghgp-scope3-categories`), last checked 20 November 2026.

- JCGM 100:2008, Evaluation of measurement data: Guide to the expression of
  uncertainty in measurement (GUM), cited, not copied:
  [BIPM](https://www.bipm.org/en/doi/10.59161/jcgm100-2008e)
- JCGM 101:2008, Supplement 1 to the GUM, propagation of distributions
  using a Monte Carlo method (cited, not copied):
  [BIPM](https://www.bipm.org/en/doi/10.59161/jcgm101-2008)
- GHG Protocol Corporate Value Chain (Scope 3) Standard, data quality
  indicators (cited, not copied):
  [ghgprotocol.org](https://ghgprotocol.org/corporate-value-chain-scope-3-standard)
