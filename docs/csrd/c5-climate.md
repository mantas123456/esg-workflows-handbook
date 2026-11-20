---
step: "C5"
status: draft
last_checked: 2026-11-20
---

# C5 Climate (E1)

!!! warning "Not legal advice"
    This page shows how GHG data flows into ESRS E1. It is not the full list
    of E1 disclosures, and the numbers are made up.

## In one sentence

Build your E1 GHG figures from the same data as your Scope 1, 2 and 3
inventory, and use supplier data, including your suppliers' CBAM data,
for the significant Scope 3 categories.

## Who does this and when

The sustainability lead with finance and operations. Do a dry run on the
year before your first reporting year, so gaps show up in time.

## Inputs

- Fuel and refrigerant records (Scope 1) and electricity use (Scope 2).
- A Scope 3 screening of all 15 categories ([S2](../scope3/s2-screening.md)).
- Supplier data from [C3](c3-value-chain.md), including embedded emissions
  from suppliers that import CBAM goods ([CB4](../cbam/cb4-embedded-emissions.md)).

## Steps

### 1. Calculate gross Scope 1 and Scope 2

As in [V2](../vsme/v2-basic.md): activity x emission factor, for each fuel,
refrigerant and electricity supply.

### 2. Screen all 15 Scope 3 categories

Revised ESRS E1 asks for gross Scope 3 emissions as a **total** and for
**each significant category**. Significance depends on the size of the
estimate **and** other criteria such as spend, influence, transition risks
and opportunities, or stakeholder views. Screening uses the 15 GHG Protocol
categories. Update the significant categories every year, and the full
inventory at least every three years.

### 3. Use supplier data for the significant categories

Replace estimates with supplier figures where you can
([S4](../scope3/s4-methods.md)):

- **Allocate a supplier's cradle-to-gate total** by your share of its
  output, by quantity or by revenue.
- **Use CBAM embedded emissions** for steel, aluminium and other CBAM
  goods. Your supplier already has them per tonne. Two cautions:
    - For iron and steel and aluminium, CBAM counts **direct emissions
      only**. Add indirect emissions (electricity) if the supplier has them.
    - CBAM **default values carry a mark-up** that rises each year. It is
      a penalty, not an emission. This handbook uses the default **without**
      the mark-up for Scope 3.

### 4. Map the figures to E1

Each figure goes to an E1 datapoint, and comes from one dataset (see
[F3](../foundations/one-dataset-many-reports.md)). No phase-in specific to
Scope 3 was found in the revised ESRS.

## Worked example

Mediterranean Logistics Group (fictional) does a dry run on **2026** data,
a year before its first report. All numbers and factors are made up.

**Scope 1 and 2**

| Source | Activity | Factor | tCO2e |
|---|---|---|---|
| Diesel for the truck fleet | 9,000,000 litre | 2.6 kg/litre | 23,400 |
| Refrigerant leaks from cold stores and trucks (service records) | – | from service records | 1,500 |
| **Scope 1** | | | **24,900** |
| Grid electricity (location-based) | 40,000 MWh | 400 kg/MWh | **16,000** |

**Category 1: Gozo Fresh Foods' share**

Gozo Fresh Foods shared its cradle-to-gate total for 2026: Scope 1 and 2
of 1,800 tCO2e plus upstream Scope 3 (categories 1 to 8) of 5,493.6 tCO2e,
**7,294 tCO2e** rounded. The group bought EUR 3,500,000 of Gozo's EUR
14,000,000 sales:

```
7,294 x 3,500,000 / 14,000,000 = 1,823.5 tCO2e
```

**Category 2: Melita Metals' steel and aluminium for the new cold store**

From Melita Metals' 2026 CBAM data:

| Line | Calculation | tCO2e |
|---|---|---|
| Steel bars, CBAM embedded emissions (actual, direct and precursors) | 100 t x 0.652 | 65.2 |
| Steel bars, indirect emissions at the mill (not counted by CBAM) | 100 t x 0.12 | 12 |
| Aluminium bars, CBAM default value without mark-up (the made-up base value from CB4) | 10 t x 2.10 | 21 |
| **Melita Metals total** | | **98.2** |

The aluminium default value covers direct emissions only. The electricity
used to make aluminium is missing, so this line is an **underestimate**. The
group notes it and asks Melita Metals to get actual data next year.

**Scope 3 screening**

The group sets a size threshold of **5%** of the screened total.

| Category | tCO2e | Share | Significant by size? | Other reason | Significant? |
|---|---|---|---|---|---|
| 1 Purchased goods and services | 381,323.5 | 95.64% | Yes | | Yes |
| 2 Capital goods | 698.2 | 0.18% | No | Transition risk: Melita Metals passes on CBAM costs for steel and aluminium | Yes |
| 3 Fuel- and energy-related activities | 7,000 | 1.76% | No | | No |
| 4 Upstream transportation and distribution | 3,000 | 0.75% | No | Influence: the group chooses and briefs its subcontracted hauliers | Yes |
| 5 Waste generated in operations | 500 | 0.13% | No | | No |
| 6 Business travel | 200 | 0.05% | No | | No |
| 7 Employee commuting | 2,000 | 0.5% | No | | No |
| 12 End-of-life treatment of sold products | 4,000 | 1% | No | | No |

Categories 8, 9, 10, 11, 13, 14 and 15 are 0: the group delivers with its
own trucks (Scope 1), sells food that uses no energy, and has no leased
assets, franchises or investments to count.

Category 1 is 381,323.5 tCO2e: Gozo's 1,823.5, plus food bought from other
suppliers (EUR 376,500,000 x 1.0 kg/EUR = 376,500) and packaging and
services (EUR 10,000,000 x 0.3 kg/EUR = 3,000). Category 2 adds other
building work (EUR 2,000,000 x 0.3 kg/EUR = 600) to Melita's 98.2.

**Into E1**

| E1 datapoint | Dataset | 2026 dry run |
|---|---|---|
| E1-scope1: Gross Scope 1 GHG emissions | fuel_use | 24,900 tCO2e |
| E1-scope2: Gross Scope 2 GHG emissions | electricity_use | 16,000 tCO2e |
| E1-scope3: Gross Scope 3 GHG emissions, in total and for each significant category | purchased_goods_spend | 398,721.7 tCO2e; significant: 1, 2, 4 |
| E1-scope3-suppliers: Supplier-specific data used for significant Scope 3 categories | supplier_emissions | Gozo Fresh Foods 1,823.5 tCO2e; Melita Metals 98.2 tCO2e |

Scope 3 is **90.7%** of the group's total of 439,621.7 tCO2e, and almost all
of it is food bought for resale on a spend basis. The next step is supplier
data from the largest food suppliers ([S7](../scope3/s7-suppliers.md)).

## Common mistakes

- **Copying CBAM figures into Scope 3 unchanged.** Add indirect emissions
  where you have them, and take the mark-up off default values.
- **Counting a supplier twice.** When a supplier figure replaces a spend
  estimate, remove the spend from the estimate (as the group did for Gozo).
- **Ranking categories on size only.** E1 also names spend, influence,
  transition risks and stakeholder views.
- **Waiting for the first reporting year.** A dry run on the year before
  shows the gaps in time.

## Evidence to keep

- Fuel, refrigerant and electricity records, with factors and sources.
- The screening of all 15 categories, with the reasons.
- Supplier answers, including the CBAM data and its verification status.

File them in the evidence locker (see
[F1](../foundations/evidence-locker.md)).

## Templates and tools

- [`esgcalc.scope3`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/esgcalc/scope3.py):
  `screen`, `supplier_specific`, `spend_based`.
- [`esgcalc.cbam`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/esgcalc/cbam.py):
  `embedded_emissions`.
- [Scope 3 screening tool](../tools/scope3-screening.md).

## Reuse in other reports

The same Scope 1 and 2 figures go into a VSME report (B3), and the same
Scope 3 inventory answers customer requests ([S9](../scope3/s9-reporting.md)).
A supplier's CBAM data serves its own CBAM declaration
([CB9](../cbam/cb9-declaration.md)) and your Scope 3. See
[F3](../foundations/one-dataset-many-reports.md).

## Sources

Facts come from `data/regulations.yml` (ids `esrs-e1-scope3`,
`esrs-phase-in`, `cbam-direct-only`, `cbam-default-values`,
`ghgp-scope3-categories`), last checked 20 November 2026. GHG Protocol and
ESRS text are cited, not copied.

- Delegated Regulation (EU) 2026/1563 (revised ESRS), ESRS E1:
  [EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32026R1563)
- Regulation (EU) 2023/956 (CBAM), Article 7 and Annex II:
  [EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:02023R0956-20251020)
- GHG Protocol Corporate Value Chain (Scope 3) Standard:
  [GHG Protocol](https://ghgprotocol.org/corporate-value-chain-scope-3-standard)
