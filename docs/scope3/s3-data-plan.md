---
step: "S3"
status: draft
last_checked: 2026-11-20
---

# S3 Data collection plan

!!! warning "Not legal advice"
    This page is a planning method. The suppliers and amounts in the
    worked example are made up.

## In one sentence

For each significant category, decide what data you need, which method you
will use, who collects it, from where, and by when, and start with the few
suppliers that cover most of the spend.

## Who does this and when

The inventory lead, agreed with the people who own the data: purchasing,
finance, facilities, logistics, HR, sales. Do it right after screening
([S2](s2-screening.md)), early in the year after the reporting year, and
work back from the date your customer or report needs the numbers.

## Inputs

- The significant categories from [S2](s2-screening.md).
- Spend by supplier from the purchase ledger.
- Names of the people who hold each kind of data.
- The deadline you are working to.

## Steps

### 1. Start from the significant categories

One row in the plan per significant category from S2. Categories that are
not significant keep their screening estimate.

### 2. Choose a target method for each

Better data costs more effort. For each category, choose the method you
can realistically reach this year:

- **supplier-specific** where a few suppliers matter and will answer;
- **average-data** where you know the physical quantity (tonnes, MWh,
  tonne.km, km);
- **spend-based** for the rest.

Mixing methods in one category is normal ([S4](s4-methods.md)).

### 3. Pick the suppliers to ask first

Sort suppliers by spend and take the fewest that together cover a target
share, for example **80%**. Ask those for their own emissions data
([S7](s7-suppliers.md)). Keep the spend-based estimate for the rest.

### 4. Name an owner, a source and a date for each row

The owner collects the data and files it in the evidence locker. The date
leaves time to check the data and calculate before your deadline.

### 5. Set a data-quality target

Decide how good each category's data should be, using the five
data-quality indicators ([F2](../foundations/data-quality.md)). Aim higher
for the large categories.

### 6. Check progress monthly

A missing supplier answer is the most common reason an inventory is late.
Chase early, and decide in advance what you will use if the answer does
not come (usually the average-data or spend-based estimate).

## Worked example

Gozo Fresh Foods Ltd (fictional) found 7 significant categories in
[S2](s2-screening.md). The supermarket wants the 2026 inventory by 30
April 2027. All suppliers and amounts are made up.

**Step 3: which ingredient suppliers to ask first.** Ingredients are
EUR 6,000,000 of spend, the largest part of category 1. Target: 80% of
ingredient spend.

| Supplier | Spend 2026 (EUR) | Share | Running share |
|---|---|---|---|
| Maltese Farmers Cooperative | 1,800,000 | 30.00% | 30.00% |
| Sicilian Tomato Co | 1,200,000 | 20.00% | 50.00% |
| Gozo Greens Ltd | 900,000 | 15.00% | 65.00% |
| Island Dairy Ltd | 700,000 | 11.67% | 76.67% |
| Mediterranean Oils | 500,000 | 8.33% | 85.00% |
| Spice Traders Ltd | 300,000 | 5.00% | 90.00% |
| Valletta Grain Mill | 250,000 | 4.17% | 94.17% |
| Ghajnsielem Egg Farm | 200,000 | 3.33% | 97.50% |
| Herb Garden Gozo | 100,000 | 1.67% | 99.17% |
| Other small suppliers | 50,000 | 0.83% | 100.00% |

The first four reach 76.67%, just short of 80%. The **top 5 suppliers
cover 85.00%** of ingredient spend. Gozo Fresh Foods asks those five for
supplier-specific data, and keeps the spend-based estimate for the other
EUR 900,000.

**Steps 1, 2 and 4: the plan.**

| # | Data to collect | Screening method | Target method | Owner | Source | Ready by |
|---|---|---|---|---|---|---|
| 1 | Spend by supplier; tonnes bought from the top 5 ingredient suppliers; their emissions data; packaging tonnes by material | Spend-based | Supplier-specific for the top 5 ingredient suppliers; average-data for packaging; spend-based for the rest | Purchasing | Purchase ledger, supplier questionnaires (S7), packaging specifications | 31 Mar 2027 |
| 2 | Assets bought in 2026, by type and cost | Spend-based | Spend-based | Finance | Fixed asset register | 31 Jan 2027 |
| 3 | MWh of electricity and of each fuel | Average-data | Average-data with sourced factors (S5) | Facilities | Energy invoices and meter readings | 31 Jan 2027 |
| 4 | Tonne.km per haulier; Island Cold Store's emissions and Gozo's share of its capacity | Average-data and supplier-specific | Average-data from haulier records; supplier-specific for the cold store | Logistics | Haulier invoices, Island Cold Store's emissions report | 28 Feb 2027 |
| 7 | Distance, transport mode and days on site per employee | Average-data (estimate) | Average-data from a staff survey | HR | Staff survey | 31 Jan 2027 |
| 9 | Storage time and transport distance of Gozo products at the supermarket | Average-data (estimate) | Average-data from the supermarket's figures | Sales | The supermarket | 28 Feb 2027 |
| 12 | Packaging tonnes by material; share of food wasted by consumers | Average-data | Average-data with material-specific factors | Quality and packaging | Packaging specifications, published food-waste studies | 31 Jan 2027 |

Every date leaves at least four weeks before the supermarket's deadline to
calculate ([S4](s4-methods.md)) and check the result.

In Python, with
[`esgcalc`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/esgcalc/scope3.py):

```python
from esgcalc.scope3 import suppliers_to_cover

spend = {"Maltese Farmers Cooperative": 1_800_000, "Sicilian Tomato Co": 1_200_000,
         "Gozo Greens Ltd": 900_000, "Island Dairy Ltd": 700_000, "Mediterranean Oils": 500_000,
         "Spice Traders Ltd": 300_000, "Valletta Grain Mill": 250_000,
         "Ghajnsielem Egg Farm": 200_000, "Herb Garden Gozo": 100_000,
         "Other small suppliers": 50_000}
c = suppliers_to_cover(spend, 0.80)
print(len(c.suppliers), round(c.share, 4))   # 5 0.85
```

## Common mistakes

- **Asking every supplier at once.** Most will not answer. Start with the
  few that cover most of the spend.
- **No owner.** "Sustainability will get it" means nobody will. Name a
  person for each row.
- **No fallback.** Decide in advance what you will use if a supplier does
  not answer.
- **Dates too close to the deadline.** Leave time to check and calculate.
- **Planning for categories that are not significant.** Keep their
  screening estimates and spend the effort where the emissions are.

## Evidence to keep

- The plan, with owners and dates, and the version history.
- Each request sent and each answer received, with dates.
- The decision for each fallback used.

File them in the evidence locker (see
[F1](../foundations/evidence-locker.md)).

## Templates and tools

- [`esgcalc.scope3.suppliers_to_cover`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/esgcalc/scope3.py):
  the supplier selection above.
- An inventory workbook with spend, average-data and supplier-specific
  tabs is planned for this release.

## Reuse in other reports

The same supplier list and requests serve CBAM ([CB3](../cbam/cb3-supplier-data.md))
where the goods are CBAM goods, and VSME or customer questionnaires. Send
one request per supplier. See [F3](../foundations/one-dataset-many-reports.md).

## Sources

Facts come from `data/regulations.yml` (ids `ghgp-scope3-categories`,
`esrs-e1-scope3`), last checked 20 November 2026.

- GHG Protocol Corporate Value Chain (Scope 3) Standard (cited, not
  copied):
  [ghgprotocol.org](https://ghgprotocol.org/corporate-value-chain-scope-3-standard)
