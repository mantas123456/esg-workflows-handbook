---
step: "V3"
status: draft
last_checked: 2026-11-21
---

# V3 GHG emissions for VSME

!!! warning "Not legal advice"
    This page explains which greenhouse gas figures the voluntary standard
    asks for, and how they connect to the Scope 3 track. The numbers in the
    worked example are made up.

## In one sentence

The Basic Module needs Scope 1 and location-based Scope 2 emissions and an
intensity per turnover; Scope 3 is not required, but if you already have it,
you can add it.

## Who does this and when

Whoever prepares the VSME report, together with whoever calculates
emissions for customers. Do it with the B3 data ([V2](v2-basic.md)).

## Inputs

- Fuel, refrigerant and electricity data for the year ([V2](v2-basic.md)).
- The grid emission factor for your country.
- Your Scope 3 inventory, if you have one ([S9](../scope3/s9-reporting.md)).

## Steps

### 1. Know what the Basic Module asks for

| Emissions | Basic Module (B3) | Where in this handbook |
|---|---|---|
| Scope 1: fuels burned, company vehicles, refrigerant leaks | **Required** | [V2](v2-basic.md) |
| Scope 2, location-based: purchased electricity × average grid factor | **Required** | [V2](v2-basic.md) |
| Scope 2, market-based: based on your electricity contracts | Not required; add it if customers ask | – |
| Scope 3: the value chain | **Not required** in the Basic Module | [Scope 3 track](../scope3/s1-boundary.md) |
| GHG intensity: emissions per turnover | **Required** | this page |

<!-- generated from data/vsme_datapoints.yml: disclosures=B3 -->
| Datapoint | What it covers | Unit | Dataset | Checked against |
|---|---|---|---|---|
| B3-energy | Total energy consumption, split into renewable and non-renewable where the data can be obtained | MWh | `electricity_use` | 2025 Recommendation |
| B3-energy-fuels | Energy from fuels, part of total energy consumption | MWh | `fuel_use` | 2025 Recommendation |
| B3-scope1 | Gross Scope 1 GHG emissions, following the GHG Protocol Corporate Standard | tCO2e | `fuel_use` | 2025 Recommendation |
| B3-scope2-location | Gross location-based Scope 2 GHG emissions | tCO2e | `electricity_use` | 2025 Recommendation |
| B3-intensity | GHG intensity: total GHG emissions divided by turnover | tCO2e per EUR | – | 2025 Recommendation |
<!-- end generated vsme datapoints -->

### 2. Calculate Scope 1 and 2 with the GHG Protocol

The standard refers to the GHG Protocol Corporate Standard. Use one
boundary ([S1](../scope3/s1-boundary.md)), the reporting year, and record
each factor's source ([S5](../scope3/s5-emission-factors.md)).

### 3. Calculate the intensity

Divide the emissions reported in B3 by turnover. If you also report
Scope 3, say whether your intensity includes it; the simplest is to keep
the intensity on Scope 1 and 2, as B3 requires them.

### 4. Decide whether to add Scope 3

Not required in the Basic Module, but often asked for by customers that
report under the CSRD. If you have it, add it as extra information, with
its methods, data quality and uncertainty ([S9](../scope3/s9-reporting.md)).
If you do not, [V5](v5-requests.md) explains how to answer such requests.

### 5. Keep the same numbers everywhere

The Scope 1 and 2 in your VSME report, in customer questionnaires and in
your Scope 3 inventory's boundary note should be the same figures.

## Worked example

Gozo Fresh Foods Ltd (fictional) reports its 2026 emissions under the
voluntary standard, and adds the Scope 3 it calculated for the supermarket.
All numbers are made up.

| Emissions | tCO2e | Share | In the Basic Module? | Source |
|---|---|---|---|---|
| Scope 1 | 600.00 | 7.94% | Required | [V2](v2-basic.md) |
| Scope 2 (location-based) | 1,200.00 | 15.89% | Required | [V2](v2-basic.md) |
| Scope 3 | 5,752.59 | 76.17% | Added voluntarily | [S9](../scope3/s9-reporting.md) |
| **Total** | **7,552.59** | **100%** | | |

- **Intensity (B3):** Scope 1 and 2, 1,800 tCO2e / EUR 14,000,000 =
  **128.57 tCO2e per EUR million**. Gozo states that the intensity does
  not include Scope 3.
- **Scope 3 is three-quarters of the total.** The Basic Module alone would
  show less than a quarter of Gozo's emissions, which is why the
  supermarket asks for Scope 3.
- **Same figures everywhere.** The 1,800 tCO2e of Scope 1 and 2 is the
  same as in the Scope 3 inventory's boundary ([S1](../scope3/s1-boundary.md)).
  Gozo sends the supermarket the same Scope 3 figure, 5,750 ± 420 tCO2e
  as rounded in [S9](../scope3/s9-reporting.md).

In Python, with
[`esgcalc`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/esgcalc/vsme.py):

```python
from esgcalc.vsme import ghg_intensity

scope1, scope2, scope3 = 600.0, 1200.0, 5752.59
print(round(scope3 / (scope1 + scope2 + scope3), 4))   # 0.7617
print(round(ghg_intensity(scope1 + scope2, 14_000_000), 2))   # 128.57
```

## Common mistakes

- **Reporting market-based Scope 2 as B3.** The Basic Module asks for
  location-based.
- **An intensity that mixes scopes without saying so.** State what it
  covers.
- **Different Scope 1 and 2 in different reports.** Use one figure.
- **Treating "not required" as "not relevant".** For many smaller
  companies Scope 3 is most of the footprint.
- **Adding Scope 3 without its methods and uncertainty.** Share it with
  the notes from [S9](../scope3/s9-reporting.md).

## Evidence to keep

- The Scope 1 and 2 calculation with every factor's source.
- If Scope 3 is added: the inventory and its notes
  ([S9](../scope3/s9-reporting.md)).

File them in the evidence locker (see
[F1](../foundations/evidence-locker.md)).

## Templates and tools

- [`esgcalc.vsme.ghg_intensity`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/esgcalc/vsme.py).
- The [Scope 3 inventory workbook](../downloads/scope3-inventory.xlsx), if
  you add Scope 3.

## Reuse in other reports

Scope 1, 2 and 3 are the same numbers your customers' ESRS E1 reports and
questionnaires use. Calculate once. See
[F3](../foundations/one-dataset-many-reports.md).

## Sources

Facts come from `data/regulations.yml` (ids `vsme-basic-metrics`,
`vsme-modules`, `ghgp-scope3-categories`), last checked 20 November 2026.

- Commission Delegated Regulation (EU) 2026/1560 (voluntary standard):
  [EUR-Lex](https://eur-lex.europa.eu/eli/reg_del/2026/1560/oj/eng)
- Commission Recommendation (EU) 2025/1710 (VSME), B3:
  [EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX%3A32025H1710)
- GHG Protocol Corporate Standard (cited, not copied):
  [ghgprotocol.org](https://ghgprotocol.org/corporate-standard)
