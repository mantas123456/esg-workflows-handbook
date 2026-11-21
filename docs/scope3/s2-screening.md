---
step: "S2"
status: draft
last_checked: 2026-11-21
---

# S2 Screening the 15 categories

!!! warning "Not legal advice"
    This page shows how to screen Scope 3 with rough numbers. The factors in
    the worked example are **made up**. See [S5](s5-emission-factors.md)
    for real sources.

## In one sentence

Make a rough estimate for **all 15** Scope 3 categories, then decide which
ones are significant and need proper data, and write down why the others
are left out.

## Who does this and when

Whoever leads the inventory, with finance (for spend data) and purchasing.
Do it **before** collecting detailed data ([S3](s3-data-plan.md)), so the
effort goes where the emissions are. Repeat it every year.

## Inputs

- Your boundary from [S1](s1-boundary.md).
- Last year's spend by type (from the accounts), and simple activity data
  you already have: energy use, freight, waste, staff numbers.
- Rough emission factors. Accuracy is not the point yet; finding the big
  categories is.
- What your customers, lenders or investors have asked for.

## Steps

### 1. List all 15 categories

The GHG Protocol Scope 3 Standard has 15 categories: 8 upstream (1 to 8)
and 7 downstream (9 to 15). Screen every one. If a category does not
apply, give it 0 and write the reason.

### 2. Make a rough estimate for each

Use the quickest method that gives an order of magnitude:

- **spend-based** for purchases and capital goods (spend × factor per
  euro);
- **average-data** where you know a quantity (MWh, tonne.km, kg of waste,
  km commuted);
- **supplier-specific** where a supplier already gave you its figure.

[S4](s4-methods.md) explains the methods.

**Food, drink and other farm-based goods:** emissions from land use and
land-use change on the farms can be a large part of category 1. The GHG
Protocol Land Sector and Removals Standard takes effect on 1 January 2027.
Note in the screening which purchases come from farms or forests, so the
inventory can treat them under that standard.

### 3. Rank and work out each share

Add up the estimates and work out each category's share of the total.

### 4. Apply a size threshold you choose

Choose a threshold, for example **2% of the screened total**, and state it.
Categories at or above it are significant by size.

### 5. Apply the other criteria

A small category can still be significant. ESRS E1 names criteria besides
size: **spend**, **influence** (can you reduce it?), **transition risks and
opportunities**, and **stakeholder views** (for example, a customer asked
for it).

### 6. Write a reason for every category left out

"Not relevant" is not a reason. Say what the company does or does not do
that makes the category zero or small.

### 7. Repeat every year

Under ESRS E1, the significant categories are updated every year and the
full inventory at least every three years, or after a significant event
such as an acquisition.

## Worked example

Gozo Fresh Foods Ltd (fictional, Malta, 140 employees) screens its 2026
Scope 3 for the supermarket ([S1](s1-boundary.md)). It chooses a size
threshold of **2%**. All numbers and factors are made up.

| # | Category | Estimate (tCO2e) | Share | Significant? | Reason |
|---|---|---|---|---|---|
| 1 | Purchased goods and services | 6,375 | 85.12% | Yes | Size: above 2% |
| 2 | Capital goods | 160 | 2.14% | Yes | Size: above 2% |
| 3 | Fuel- and energy-related activities | 180 | 2.40% | Yes | Size: above 2% |
| 4 | Upstream transportation and distribution | 180 | 2.40% | Yes | Size: above 2% |
| 5 | Waste generated in operations | 31 | 0.41% | No | Below 2%, no other reason |
| 6 | Business travel | 10 | 0.13% | No | Below 2%, no other reason |
| 7 | Employee commuting | 157.08 | 2.10% | Yes | Size: above 2% |
| 8 | Upstream leased assets | 0 | 0.00% | No | No leased assets outside the boundary. The warehouse Gozo leases is operated by Gozo, so it is in Scope 1 and 2. |
| 9 | Downstream transportation and distribution | 126 | 1.68% | Yes | The supermarket asked for it, and Gozo can reduce it through packaging and shelf life. |
| 10 | Processing of sold products | 0 | 0.00% | No | Products are sold ready to heat or eat. Nobody processes them further. |
| 11 | Use of sold products | 0 | 0.00% | No | Food products use no energy and release no gases in use. Home cooking and refrigeration are not estimated. |
| 12 | End-of-life treatment of sold products | 195 | 2.60% | Yes | Size: above 2% |
| 13 | Downstream leased assets | 0 | 0.00% | No | Gozo leases out no assets. |
| 14 | Franchises | 0 | 0.00% | No | Gozo has no franchises. |
| 15 | Investments | 75 | 1.00% | No | Below 2%, no other reason |
| | **Total screened** | **7,489.08** | **100%** | | |

The **7 significant categories** (1, 2, 3, 4, 7, 9 and 12) cover
**7,373.08 tCO2e**, or **98.45%** of the screened total. Category 1 alone is
85.12%, so that is where Gozo Fresh Foods will spend most of its
data-collection effort ([S3](s3-data-plan.md)).

Two things to notice:

- **Category 9 is below the threshold but significant.** The supermarket
  asked for it, and Gozo can reduce it. Size is not the only test.
- **Island Cold Store appears twice, for different reasons.** In category 4
  for the storage service Gozo buys, and in category 15 for Gozo's 25%
  stake in it. Check for overlap when the full inventory is built
  ([S4](s4-methods.md)).

??? info "How each estimate was made (made-up factors)"

    | # | What | Calculation | tCO2e |
    |---|---|---|---|
    | 1 | Ingredients | EUR 6,000,000 × 0.9 kg/EUR | 5,400 |
    | 1 | Packaging | EUR 1,500,000 × 0.6 kg/EUR | 900 |
    | 1 | Services (cleaning, IT, maintenance) | EUR 500,000 × 0.15 kg/EUR | 75 |
    | 2 | Machinery and equipment bought in 2026 | EUR 400,000 × 0.4 kg/EUR | 160 |
    | 3 | Upstream emissions of purchased electricity (3,000 MWh) | 3,000 MWh × 40 kg/MWh | 120 |
    | 3 | Upstream emissions of fuels burned (2,000 MWh) | 2,000 MWh × 30 kg/MWh | 60 |
    | 4 | Inbound road freight by hauliers | 900,000 tonne.km × 0.1 kg/tonne.km | 90 |
    | 4 | Chilled storage at Island Cold Store (30% of its capacity) | 300 t × 30 / 100 | 90 |
    | 5 | Food waste to anaerobic digestion | 600,000 kg × 0.01 kg/kg | 6 |
    | 5 | General waste to landfill | 50,000 kg × 0.5 kg/kg | 25 |
    | 6 | Flights and hotels | EUR 40,000 × 0.25 kg/EUR | 10 |
    | 7 | Commuting by car: 140 staff x 220 days x 30 km | 924,000 km × 0.17 kg/km | 157.08 |
    | 9 | Chilled storage of Gozo products at the supermarket | 3,000,000 kg × 0.03 kg/kg | 90 |
    | 9 | Supermarket transport to its stores | 360,000 tonne.km × 0.1 kg/tonne.km | 36 |
    | 12 | Packaging thrown away by consumers | 300,000 kg × 0.4 kg/kg | 120 |
    | 12 | Food wasted by consumers | 150,000 kg × 0.5 kg/kg | 75 |
    | 15 | 25% equity in Island Cold Store (Scope 1 and 2: 300 t) | 300 t × 25 / 100 | 75 |

In Python, with
[`esgcalc`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/esgcalc/scope3.py):

```python
from esgcalc.scope3 import screen

estimates = {1: 6375, 2: 160, 3: 180, 4: 180, 5: 31, 6: 10, 7: 157.08, 8: 0,
             9: 126, 10: 0, 11: 0, 12: 195, 13: 0, 14: 0, 15: 75}
rows = screen(estimates, size_threshold_share=0.02,
              other_reasons={9: "Customer request; Gozo can reduce it"})
print([r.category for r in rows if r.significant])   # [1, 2, 3, 4, 7, 9, 12]
```

## Common mistakes

- **Screening only the categories you expect.** Screen all 15 and write a
  reason for each zero.
- **Using size alone.** A category your customer asks about, or one you
  can easily reduce, can be significant even when small.
- **Treating the screening numbers as the inventory.** They are rough. The
  significant categories need better data ([S3](s3-data-plan.md),
  [S4](s4-methods.md)).
- **Forgetting the threshold.** State it, and use the same one next year.
- **Counting your own companies.** Companies inside the boundary are Scope
  1 and 2, not Scope 3 suppliers ([S1](s1-boundary.md)).

## Evidence to keep

- The screening table with every estimate, its data and factor, and the
  reason for each decision.
- The threshold and who approved it.
- The customer request that made category 9 significant.

File them in the evidence locker (see
[F1](../foundations/evidence-locker.md)).

## Templates and tools

<!-- generated from data/workflows.yml templates: do not edit by hand -->
- **[Scope 3 screening matrix](../downloads/scope3-screening-matrix.xlsx)** (Excel): Screen all 15 Scope 3 categories with a rough estimate each, test them against a size threshold you choose and other criteria, and record the reason for every decision.
<!-- end generated templates -->

- [`esgcalc.scope3.screen`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/esgcalc/scope3.py):
  the screening above.
- [Scope 3 screening tool](../tools/scope3-screening.md): the same
  screening in your browser, with the Gozo Fresh Foods example.

## Reuse in other reports

The list of significant categories is what ESRS E1 asks for, and it tells
you which data to request from suppliers for VSME and customer
questionnaires. See [F3](../foundations/one-dataset-many-reports.md).

## Sources

Facts come from `data/regulations.yml` (ids `ghgp-scope3-categories`,
`esrs-e1-scope3`), last checked 20 November 2026.

- GHG Protocol Corporate Value Chain (Scope 3) Standard (cited, not
  copied):
  [ghgprotocol.org](https://ghgprotocol.org/corporate-value-chain-scope-3-standard)
- Delegated Regulation (EU) 2026/1563, ESRS E1 (Scope 3 disclosure):
  [EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32026R1563)
