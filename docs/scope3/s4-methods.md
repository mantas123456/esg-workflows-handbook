---
step: "S4"
status: draft
last_checked: 2026-11-20
---

# S4 Calculation methods

!!! warning "Not legal advice"
    This page explains the three calculation methods in plain words. All
    numbers and factors in the worked example are **made up**.

## In one sentence

Calculate each significant category with the best data you have,
supplier-specific, average-data or spend-based, mix them line by line, and
make sure every purchase is counted exactly once.

## Who does this and when

The inventory lead, once the data from the plan ([S3](s3-data-plan.md)) is
in. Calculate in a working file that keeps each line's inputs, factor and
source, so anyone can check it.

## Inputs

- The data collected under the plan: supplier answers, quantities, spend.
- Emission factors with their source, year and unit ([S5](s5-emission-factors.md)).
- A price index for the spend years and the factor's year, if you use
  spend-based factors.
- The screening estimates for the categories that are not significant
  ([S2](s2-screening.md)).

## Steps

### 1. Supplier-specific: your share of the supplier's emissions

```text
tCO2e = supplier's emissions x what you bought / supplier's total output
```

Use the same unit for "what you bought" and "total output" (tonnes, units
or revenue). The supplier's figure should cover the goods you bought, from
cradle to their gate. **A supplier's Scope 1 and 2 alone are not cradle to
gate**: they leave out what the supplier buys (fertiliser, feed, packaging).
If that is all you get, add an estimate for the missing upstream part, or
score completeness lower and say so ([S6](s6-data-quality.md)).

### 2. Average-data: quantity x average factor

```text
tCO2e = quantity x factor (kg CO2e per unit) / 1000
```

The quantity and the factor must use the **same unit**: kg with
kg CO2e/kg, tonne.km with kg CO2e/tonne.km.

### 3. Spend-based: money x spend factor, deflated

```text
tCO2e = spend x (price index of the factor's year / price index of the spend year)
        x factor (kg CO2e per EUR) / 1000
```

Spend factors are priced in a base year. Prices rise, so a euro buys less
each year. **Deflate** the spend to the factor's year, or inflation alone
will raise your emissions. If the factor is in another currency, convert
the spend first.

### 4. Mix methods line by line: the hybrid method

One category can use all three. When better data replaces an estimate,
**remove the estimate**. Each purchase belongs on one line only.

### 5. Keep the screening estimate for categories that are not significant

Carry them over, marked as screening estimates.

### 6. Add up and show the method mix

Report each category's total and how much of it came from each method. A
growing supplier-specific share year after year shows progress.

## Worked example

Gozo Fresh Foods Ltd (fictional) calculates its 2026 inventory from the
data collected under its plan ([S3](s3-data-plan.md)). Spend factors are
priced in 2022; the producer price index is **100 in 2022** and **118 in
2026**. All numbers are made up.

**Category 1, the hybrid in detail.**

| What | Method | Calculation | tCO2e |
|---|---|---|---|
| Maltese Farmers Cooperative | Supplier-specific | 12,000 t × 3,000 / 40,000 | 900.00 |
| Sicilian Tomato Co | Supplier-specific | 30,000 t × 2,400 / 60,000 | 1,200.00 |
| Gozo Greens Ltd | Supplier-specific | 2,500 t × 1,600 / 8,000 | 500.00 |
| Island Dairy Ltd | Supplier-specific | 9,000 t × 700 / 15,000 | 420.00 |
| Mediterranean Oils | Supplier-specific | 20,000 t × 250 / 25,000 | 200.00 |
| Other ingredient suppliers | Spend-based | EUR 900,000 × 100/118 × 0.9 kg/EUR | 686.44 |
| Services (cleaning, IT, maintenance) | Spend-based | EUR 500,000 × 100/118 × 0.15 kg/EUR | 63.56 |
| Cardboard packaging | Average-data | 400,000 kg × 0.8 kg/kg | 320.00 |
| Plastic film packaging | Average-data | 150,000 kg × 2.5 kg/kg | 375.00 |
| Glass jars | Average-data | 200,000 kg × 0.9 kg/kg | 180.00 |
| **Category 1** | | | **4,845.00** |

The five supplier lines **replace** EUR 5,100,000 of ingredient spend.
That spend is no longer on a spend-based line; only the other EUR 900,000
is. Packaging is now calculated from tonnes by material instead of spend.

**All categories.**

| # | Category | tCO2e | Supplier-specific | Average-data | Spend-based |
|---|---|---|---|---|---|
| 1 | Purchased goods and services | 4,845.00 | 66.46% | 18.06% | 15.48% |
| 2 | Capital goods | 135.59 | 0.00% | 0.00% | 100.00% |
| 3 | Fuel- and energy-related activities | 180.00 | 0.00% | 100.00% | 0.00% |
| 4 | Upstream transportation and distribution | 175.00 | 51.43% | 48.57% | 0.00% |
| 5 | Waste generated in operations | 31.00 | 0.00% | 100.00% | 0.00% |
| 6 | Business travel | 10.00 | 0.00% | 0.00% | 100.00% |
| 7 | Employee commuting | 117.00 | 0.00% | 100.00% | 0.00% |
| 9 | Downstream transportation and distribution | 114.00 | 0.00% | 100.00% | 0.00% |
| 12 | End-of-life treatment of sold products | 92.50 | 0.00% | 100.00% | 0.00% |
| 15 | Investments | 75.00 | 100.00% | 0.00% | 0.00% |
| | **Total Scope 3** | **5,775.09** | **58.61%** | **25.88%** | **15.51%** |

Categories 5, 6 and 15 are not significant: their screening estimates are
carried over. Categories 8, 10, 11, 13 and 14 are zero, with the reasons
given in [S2](s2-screening.md).

**Why the inventory is lower than the screening (7,489.08 tCO2e).**

| # | Screening (tCO2e) | Inventory (tCO2e) | Main reason |
|---|---|---|---|
| 1 | 6,375.00 | 4,845.00 | Suppliers' own data, deflated spend, packaging by material |
| 2 | 160.00 | 135.59 | Spend deflated to the factor's year |
| 4 | 180.00 | 175.00 | Haulier records instead of an estimate |
| 7 | 157.08 | 117.00 | Staff survey: some staff take the bus |
| 9 | 126.00 | 114.00 | The supermarket's own figures |
| 12 | 195.00 | 92.50 | End-of-life factors by packaging material |

For example, the five suppliers' own data gives 3,220 tCO2e. Their
EUR 5,100,000 of spend at 0.9 kg/EUR, without deflation, gave 4,590 tCO2e
at screening.

**Island Cold Store, counted twice on purpose.** Category 4 holds the
storage service Gozo buys (90 tCO2e, 30% of the cold store's emissions).
Category 15 holds Gozo's 25% stake (75 tCO2e). Both come from the same 300
tCO2e. Gozo keeps both, because they are two different relationships, and
discloses the overlap in its inventory notes ([S9](s9-reporting.md)).

In Python, with
[`esgcalc`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/esgcalc/scope3.py):

```python
from esgcalc.scope3 import Line, combine, spend_based, supplier_specific

lines = [
    Line(1, "supplier_specific", supplier_specific(12_000, 3_000, 40_000)),     # 900
    Line(1, "spend_based", spend_based(900_000, 0.9, price_index_spend_year=118,
                                       price_index_factor_year=100)),           # 686.44
    # ... one Line per row of the tables above
]
category_1 = combine(lines)[1]
print(round(category_1.tco2e, 2), round(category_1.share("supplier_specific"), 4))
```

## Common mistakes

- **Counting a purchase twice.** When a supplier's data comes in, delete
  the spend line it replaces.
- **Not deflating spend.** Without it, inflation alone raises Scope 3 every
  year.
- **Mixing units.** kg with a factor per tonne is out by a factor of 1,000.
- **Allocating by the wrong quantity.** Use the same unit for what you
  bought and the supplier's total output.
- **Hiding overlaps.** If the same emissions appear in two categories for
  different reasons, say so.
- **Leaving out the method mix.** Readers need to know how much rests on
  rough spend-based factors.

## Evidence to keep

- The working file with every line: inputs, factor, source, method and
  result.
- Each supplier's answer and its basis (period, boundary, verification).
- The price index used, with its source.

File them in the evidence locker (see
[F1](../foundations/evidence-locker.md)).

## Templates and tools

<!-- generated from data/workflows.yml templates: do not edit by hand -->
- **[Scope 3 inventory workbook](../downloads/scope3-inventory.xlsx)** (Excel): A Scope 3 inventory line by line, with spend-based, average-data and supplier-specific tabs, a data-quality score and a 95% uncertainty on every line, and a summary by category.
<!-- end generated templates -->

- [`esgcalc.scope3`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/esgcalc/scope3.py):
  `supplier_specific`, `average_data`, `spend_based` (with deflation and
  currency) and `combine`.

## Reuse in other reports

The same line-by-line file gives ESRS E1 its Scope 3 per significant
category, and the supplier-specific lines can be reused when the same
goods come up in CBAM ([CB4](../cbam/cb4-embedded-emissions.md)). See
[F3](../foundations/one-dataset-many-reports.md).

## Sources

Facts come from `data/regulations.yml` (ids `ghgp-scope3-categories`,
`esrs-e1-scope3`), last checked 20 November 2026.

- GHG Protocol Corporate Value Chain (Scope 3) Standard and its Technical
  Guidance for Calculating Scope 3 Emissions (cited, not copied):
  [ghgprotocol.org](https://ghgprotocol.org/corporate-value-chain-scope-3-standard)
