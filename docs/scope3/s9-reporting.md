---
step: "S9"
status: draft
last_checked: 2026-11-20
---

# S9 Reporting the inventory

!!! warning "Not legal advice"
    This page shows a clear way to report a Scope 3 inventory. If you report
    under ESRS E1, its disclosure requirements apply. All numbers in the
    worked example are made up.

## In one sentence

Report Scope 3 per category with its method, data-quality score and
uncertainty, a total with a coverage interval, and notes that let a reader
check every choice you made.

## Who does this and when

The inventory lead, with a reviewer who did not prepare the numbers.
Report once a year, at the same time as Scope 1 and 2, and send the
customer or report the same figures.

## Inputs

- The inventory per category with its method mix ([S4](s4-methods.md)).
- Data-quality scores ([S6](s6-data-quality.md)) and uncertainties
  ([F2](../foundations/data-quality.md)).
- The screening and the reasons for exclusions ([S2](s2-screening.md)).
- The boundary ([S1](s1-boundary.md)), factor register ([S5](s5-emission-factors.md))
  and base-year policy ([S8](s8-base-year.md)).

## Steps

### 1. One row per category

Give every category you report its emissions, main method, data-quality
score and ±95% uncertainty. List excluded categories with their reason.

### 2. A total with a coverage interval

Add up the categories and combine their uncertainties
([F2](../foundations/data-quality.md)). Round as a lab would.

### 3. Notes a reader needs

Boundary and consolidation approach, reporting period, significance
threshold, factor sources, data-quality guide, uncertainty method, base
year and recalculation policy, and any overlaps or known gaps.

### 4. If you report under ESRS E1

Revised ESRS E1 asks for gross Scope 3 as a **total and for each
significant category**, with the significant categories identified by
size and other criteria and reviewed every year ([S2](s2-screening.md)).

!!! info "Phase-in not confirmed here"
    This handbook could not confirm whether the revised ESRS give a phase-in
    for Scope 3 in a company's first reporting years. Check the transitional
    provisions in ESRS 1 (chapter 10) of Delegated Regulation (EU)
    2026/1563 for your first year.

### 5. Review before sending

A second person checks that totals add up, every exclusion has a reason,
and every number traces to the evidence locker.

## Worked example

Gozo Fresh Foods Ltd (fictional) reports its 2026 Scope 3 inventory to the
supermarket. All numbers are made up.

**Scope 3 inventory 2026**

| # | Category | tCO2e | Main method | Data-quality score | ±95% | Significant |
|---|---|---|---|---|---|---|
| 1 | Purchased goods and services | 4,845.00 | Supplier-specific | 1.87 | 8.4% | Yes |
| 2 | Capital goods | 135.59 | Spend-based | 3.00 | 50.0% | Yes |
| 3 | Fuel- and energy-related activities | 180.00 | Average-data | 2.00 | 15.0% | Yes |
| 4 | Upstream transportation and distribution | 175.00 | Supplier-specific | 1.79 | 13.3% | Yes |
| 5 | Waste generated in operations | 31.00 | Average-data | 2.80 | 41.5% | No |
| 6 | Business travel | 10.00 | Spend-based | 3.00 | 50.0% | No |
| 7 | Employee commuting | 117.00 | Average-data | 2.20 | 22.0% | Yes |
| 9 | Downstream transportation and distribution | 114.00 | Average-data | 2.55 | 30.9% | Yes |
| 12 | End-of-life treatment of sold products | 92.50 | Average-data | 2.85 | 40.8% | Yes |
| 15 | Investments | 75.00 | Supplier-specific | 1.80 | 15.0% | No |
| | **Total Scope 3** | **5,775.09** | | **1.94** | **7.2%** | |

**Reported total: 5,780 ± 420 tCO2e (95%).** Significant categories:
**5,659.09 tCO2e**, 97.99% of the total.

**Not included, with reasons:** 8 upstream leased assets, 10 processing
of sold products, 11 use of sold products, 13 downstream leased assets and
14 franchises. The reason for each is in [S2](s2-screening.md).

**Notes to the inventory**

1. **Boundary:** operational control ([S1](s1-boundary.md)); Scope 1 and 2
   are reported separately.
2. **Period:** calendar year 2026.
3. **Significance:** categories at or above 2% of the screened total, or
   significant for another reason (category 9: customer request).
4. **Methods:** 58.61% supplier-specific, 25.88% average-data, 15.51%
   spend-based ([S4](s4-methods.md)). Spend is deflated to the factor's
   price year.
5. **Factors:** DESNZ 2026 conversion factors (Open Government Licence
   v3.0) for 13 lines; 4 lines still use placeholder factors while a
   usable source is chosen ([S5](s5-emission-factors.md)).
6. **Data quality:** scored 1 (very good) to 5 (very poor) on five
   indicators with the guide in [S6](s6-data-quality.md), weighted by
   emissions.
7. **Uncertainty:** 95% intervals combined by the sum and product rules,
   treating lines and categories as independent
   ([F2](../foundations/data-quality.md)). Lines sharing the same DESNZ
   factors are in fact correlated, so the total's uncertainty is somewhat
   understated.
8. **Overlap:** Island Cold Store's emissions appear in category 4 (the
   storage service, 90 tCO2e) and category 15 (Gozo's 25% stake, 75
   tCO2e), from the same 300 tCO2e ([S4](s4-methods.md)).
9. **Base year:** 2026. Recalculation policy: 5% of the base-year total,
   changes added up in absolute terms ([S8](s8-base-year.md)).
10. **Gases:** all greenhouse gases as CO2e, with the global warming
    potentials used by the factor sources. All sources should use the same
    IPCC assessment report values; this is checked as factors are chosen
    ([S5](s5-emission-factors.md)).
11. **Land:** emissions from land use and land-use change on the farms
    behind the ingredients are not separated. The GHG Protocol Land Sector
    and Removals Standard takes effect on 1 January 2027, so the 2027
    inventory will need to follow it.

In Python, with
[`esgcalc`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/esgcalc/quality.py):

```python
from esgcalc.quality import round_result, sum_uncertainty

categories = [4845.00, 135.59, 180.00, 175.00, 31.00, 10.00, 117.00, 114.00, 92.50, 75.00]
u95 = [0.0836, 0.50, 0.1498, 0.1332, 0.4145, 0.50, 0.2203, 0.3095, 0.4083, 0.15]
total = sum_uncertainty(categories, u95)
print(round_result(total.value, total.u95_abs))   # (5780.0, 420.0)
```

## Common mistakes

- **A single total with no breakdown.** Readers need the categories, the
  methods and the quality behind them.
- **Exclusions without reasons.** Every category not reported needs one.
- **No uncertainty.** A number without it suggests more precision than
  there is.
- **Hiding overlaps and placeholders.** Disclose them; they will be found.
- **Ignoring land.** For food, drink and other farm-based goods, land use
  and land-use change can be a large part of category 1. Check the Land
  Sector and Removals Standard.
- **Different numbers for different readers.** Send everyone the same
  inventory.

## Evidence to keep

- The report as sent, with the date and recipient.
- The working file and every source behind it, hashed
  ([F1](../foundations/evidence-locker.md)).
- The reviewer's sign-off.

## Templates and tools

<!-- generated from data/workflows.yml templates: do not edit by hand -->
- **[Scope 3 inventory workbook](../downloads/scope3-inventory.xlsx)** (Excel): A Scope 3 inventory line by line, with spend-based, average-data and supplier-specific tabs, a data-quality score and a 95% uncertainty on every line, and a summary by category.
<!-- end generated templates -->

- [`esgcalc.scope3`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/esgcalc/scope3.py)
  and [`esgcalc.quality`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/esgcalc/quality.py):
  everything in the table above.

## Reuse in other reports

The same table answers the supermarket, a bank's questionnaire, VSME and
ESRS E1 (for the significant categories). See
[F3](../foundations/one-dataset-many-reports.md).

## Sources

Facts come from `data/regulations.yml` (ids `esrs-e1-scope3`,
`ghgp-scope3-categories`, `ghgp-base-year`, `ghgp-land-sector`, `jcgm-gum`) and
`data/factor_sources.yml`, last checked 20 November 2026.

- Delegated Regulation (EU) 2026/1563, ESRS E1 and ESRS 1:
  [EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32026R1563)
- GHG Protocol Corporate Value Chain (Scope 3) Standard (cited, not
  copied):
  [ghgprotocol.org](https://ghgprotocol.org/corporate-value-chain-scope-3-standard)
- GHG Protocol Land Sector and Removals Standard v1.1 (cited, not copied):
  [ghgprotocol.org](https://ghgprotocol.org/land-sector-and-removals-standard)
- DESNZ conversion factors 2026, Open Government Licence v3.0:
  [GOV.UK](https://www.gov.uk/government/publications/greenhouse-gas-reporting-conversion-factors-2026)
