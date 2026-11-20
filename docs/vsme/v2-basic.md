---
step: "V2"
status: draft
last_checked: 2026-11-20
---

# V2 Basic Module data collection

!!! warning "Not legal advice"
    This page explains what the Basic Module asks for, in plain words, and
    where the data usually is. It does not copy the standard. The numbers in
    the worked example are made up.

## In one sentence

Collect the data for disclosures B1 to B11 from the places it already
exists, finance, payroll, energy bills, waste invoices, the Scope 3
inventory, and record each value with its source.

## Who does this and when

The person who prepares the report, with finance, HR and the site manager.
Start after the year ends; most data is ready once the year's invoices and
payroll are closed.

## Inputs

- The option chosen in [V1](v1-modules.md).
- Annual accounts (turnover), payroll and HR records, energy and water
  bills, waste transfer notes, accident records.
- The Scope 1 and 2 figures, if you already calculated them for a customer
  ([S1](../scope3/s1-boundary.md)).

## Steps

### 1. B1 and B2: basis and practices

State the option (A or B), that you comply with the standard, and what the
report covers: the company alone or a group, and which sites. Use the same
boundary as for your emissions ([S1](../scope3/s1-boundary.md)). In B2,
describe in a few lines what you do, or plan, on climate, pollution,
water, waste, workforce and business conduct.

### 2. B3: energy and greenhouse gases

<!-- generated from data/vsme_datapoints.yml: disclosures=B3 -->
| Datapoint | What it covers | Unit | Dataset | Checked against |
|---|---|---|---|---|
| B3-energy | Total energy consumption, split into renewable and non-renewable where the data can be obtained | MWh | `electricity_use` | 2025 Recommendation |
| B3-energy-fuels | Energy from fuels, part of total energy consumption | MWh | `fuel_use` | 2025 Recommendation |
| B3-scope1 | Gross Scope 1 GHG emissions, following the GHG Protocol Corporate Standard | tCO2e | `fuel_use` | 2025 Recommendation |
| B3-scope2-location | Gross location-based Scope 2 GHG emissions | tCO2e | `electricity_use` | 2025 Recommendation |
| B3-intensity | GHG intensity: total GHG emissions divided by turnover | tCO2e per EUR | – | 2025 Recommendation |
<!-- end generated vsme datapoints -->

- **Energy:** add electricity and fuels, all in MWh. Split renewable and
  non-renewable where you can get the data.
- **Scope 1:** fuels burned on site and in your vehicles, and refrigerant
  leaks.
- **Scope 2, location-based:** electricity × the average grid factor of
  your country.
- **Intensity:** total GHG emissions divided by turnover.

Scope 3 is not required in the Basic Module. See [V3](v3-ghg.md).

### 3. B4 to B7: pollution, biodiversity, water and waste

<!-- generated from data/vsme_datapoints.yml: disclosures=B4,B5,B6,B7 -->
| Datapoint | What it covers | Unit | Dataset | Checked against |
|---|---|---|---|---|
| B4-pollution | Emissions of pollutants to air, water and soil, where the undertaking already reports them under law or an environmental management system | kg | – | Topic only |
| B5-sensitive-sites | Number and area of sites owned, leased or managed in or near biodiversity-sensitive areas | count and ha | – | 2025 Recommendation |
| B5-land-use | Land use: total, sealed and nature-oriented area (optional) | ha | – | 2025 Recommendation |
| B6-water-consumption | Water consumption (withdrawal minus discharge), for undertakings whose production uses water significantly | m3 | – | 2025 Recommendation |
| B7-waste | Waste generated, split into hazardous and non-hazardous | t | – | 2025 Recommendation |
| B7-waste-recycled | Waste diverted to recycling or reuse | t | – | 2025 Recommendation |
<!-- end generated vsme datapoints -->

- **B4:** only if you already report pollutants under law or an
  environmental management system.
- **B5:** check each site against maps of protected areas.
- **B6:** water consumption applies if your production uses water
  significantly: withdrawal minus discharge, from your water bills and
  discharge permit.
- **B7:** from waste transfer notes, by type and by what happened to it.

### 4. B8 to B10: workforce

<!-- generated from data/vsme_datapoints.yml: disclosures=B8,B9,B10 -->
| Datapoint | What it covers | Unit | Dataset | Checked against |
|---|---|---|---|---|
| B8-employees | Employees by contract type (permanent or temporary), gender and, if in more than one country, by country | headcount or FTE | `headcount` | 2025 Recommendation |
| B8-turnover-rate | Employee turnover rate, for undertakings with 50 or more employees | % | `headcount` | 2025 Recommendation |
| B9-accidents | Number and rate of recordable work-related accidents (per 100 full-time workers, based on 2,000 hours a year) | count and rate | – | 2025 Recommendation |
| B9-fatalities | Fatalities from work-related injuries and ill health | count | – | 2025 Recommendation |
| B10-pay-gap | Gender pay gap (may be left out below 150 employees; below 100 from 7 June 2031) | % | – | 2025 Recommendation |
| B10-collective-bargaining | Share of employees covered by collective bargaining agreements | % | – | 2025 Recommendation |
| B10-training | Average annual training hours per employee, by gender | hours | – | 2025 Recommendation |
<!-- end generated vsme datapoints -->

- **B8:** from payroll: employees by contract type and gender. From 50
  employees, also the turnover rate.
- **B9:** from the accident book: recordable accidents and fatalities. The
  rate is per 100 full-time workers, counting 2,000 hours a year each.
- **B10:** the gender pay gap (you may leave it out below 150 employees),
  the share covered by collective agreements, and training hours.

### 5. B11: corruption and bribery

<!-- generated from data/vsme_datapoints.yml: disclosures=B11 -->
| Datapoint | What it covers | Unit | Dataset | Checked against |
|---|---|---|---|---|
| B11-corruption | Convictions and total fines for breaches of anti-corruption and anti-bribery laws | count and EUR | – | 2025 Recommendation |
<!-- end generated vsme datapoints -->

From legal records: convictions and fines in the year, usually zero.

### 6. Record each value with its source

Keep a line for each datapoint: value, unit, source document and who
provided it. File the sources in the evidence locker.

## Worked example

Gozo Fresh Foods Ltd (fictional, Malta) collects its Basic Module data for
2026, with the same operational-control boundary as its Scope 3 inventory
([S1](../scope3/s1-boundary.md)). Turnover: **EUR 14,000,000**. All
numbers are made up.

**B3: energy and greenhouse gases**

| Line | Calculation | tCO2e |
|---|---|---|
| LPG for ovens and boilers | 1,000 MWh × 230 kg/MWh | 230.00 |
| Diesel for the delivery fleet | 100,000 litre × 2.6 kg/litre | 260.00 |
| Refrigerant leaks from the cold rooms (service records) | from service records | 110.00 |
| **Scope 1** | | **600.00** |
| Grid electricity, location-based | 3,000 MWh × 400 kg/MWh | 1,200.00 |
| **Scope 2 (location-based)** | | **1,200.00** |
| **Scope 1 and 2** | | **1,800.00** |

The 400 kg/MWh grid factor is made up; Gozo would use the EEA figure for
Malta ([S5](../scope3/s5-emission-factors.md)). Scope 1 and 2 together,
**1,800 tCO2e**, is the same total as in [S1](../scope3/s1-boundary.md),
because the boundary is the same.

**The Basic Module at a glance**

| Datapoint | Gozo Fresh Foods 2026 | Source |
|---|---|---|
| B3-energy | 5,000 MWh (3,000 grid electricity, 2,000 fuels); no renewable split available | Energy bills |
| B3-scope1 | 600 tCO2e | Fuel invoices, refrigerant service records |
| B3-scope2-location | 1,200 tCO2e | Electricity bills, grid factor |
| B3-intensity | 128.57 tCO2e per EUR million of turnover | Accounts |
| B5-sensitive-sites | 0 sites | Protected-area map check |
| B6-water-consumption | 8,000 m3 (40,000 withdrawn, 32,000 discharged) | Water bills, discharge records |
| B7-waste | 732 t (730 non-hazardous, 2 hazardous) | Waste transfer notes |
| B7-waste-recycled | 80 t | Waste transfer notes |
| B8-employees | 140 (120 permanent, 20 temporary; 70 women, 70 men) | Payroll |
| B8-turnover-rate | 15.0% (21 leavers) | Payroll |
| B9-accidents | 3, rate 2.4 per 100 full-time workers (250,000 hours) | Accident book |
| B9-fatalities | 0 | Accident book |
| B10-pay-gap | 8.0% (EUR 15.00 and EUR 13.80 per hour) | Payroll |
| B10-collective-bargaining | 60% | HR |
| B10-training | 12 hours (men), 10 hours (women) | Training records |
| B11-corruption | 0 convictions, EUR 0 | Legal records |

B4 is not reported: Gozo has no legal or management-system duty to report
pollutants.

Two judgement calls Gozo states in its report:

- **B7:** the 600 t of food waste sent to anaerobic digestion is **not**
  counted as recycled; only the 80 t of cardboard and plastic is. Whether
  anaerobic digestion counts as recycling depends on the standard's
  definitions: check them, and say which way you counted.
- **B10:** with 140 employees Gozo **may** leave the pay gap out (the
  threshold is 150), but reports it because its bank asked.

A few checks on the arithmetic:

- **B3 intensity:** 1,800 tCO2e / EUR 14,000,000 × 1,000,000 = 128.57
  tCO2e per EUR million.
- **B9 rate:** 3 / 250,000 hours × 200,000 = 2.4.
- **B10 pay gap:** (15.00 − 13.80) / 15.00 = 8.0%.

!!! info "Definitions to check"
    The turnover rate (leavers / average employees) and the pay gap
    (difference as a share of men's average pay) use common definitions.
    This handbook has not checked the standard's exact wording for these
    two; check it before reporting.

In Python, with
[`esgcalc`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/esgcalc/vsme.py):

```python
from esgcalc.vsme import accident_rate, ghg_intensity, pay_gap

print(round(ghg_intensity(1800, 14_000_000), 2))   # 128.57
print(accident_rate(3, 250_000))                    # 2.4
print(round(pay_gap(15.00, 13.80), 3))              # 0.08
```

## Common mistakes

- **A different boundary from your emissions.** Use the same companies and
  sites as for Scope 1 and 2.
- **Market-based instead of location-based Scope 2.** The Basic Module asks
  for location-based.
- **Forgetting refrigerants.** Leaks from cold rooms and air conditioning
  are Scope 1, and can be large for food companies.
- **Mixing headcount and full-time equivalents.** Say which one you use.
- **Leaving fields blank without a reason.** Write "not applicable" and
  why, as Gozo does for B4.

## Evidence to keep

- One line per datapoint: value, unit, source document, who provided it.
- The source documents themselves, hashed.

File them in the evidence locker (see
[F1](../foundations/evidence-locker.md)).

## Templates and tools

<!-- generated from data/workflows.yml templates: do not edit by hand -->
- **[VSME Basic Module workbook](../downloads/vsme-basic-workbook.xlsx)** (Excel): One row per Basic Module datapoint of the voluntary standard, with the value, its source, an owner and a status, and completeness tracked overall and by disclosure.
<!-- end generated templates -->

- [`esgcalc.vsme`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/esgcalc/vsme.py):
  energy total, GHG intensity, accident rate, water consumption, pay gap
  and turnover rate.
- [VSME readiness](../tools/vsme-readiness.md): tick what you have and see
  what is still to do, in your browser.

## Reuse in other reports

The energy and emissions are the same as your Scope 1 and 2 for customers
and ESRS E1; workforce figures come from the same payroll as your annual
accounts. See [F3](../foundations/one-dataset-many-reports.md).

## Sources

Facts come from `data/regulations.yml` (ids `vsme`, `vsme-modules`,
`vsme-basic-metrics`) and `data/vsme_datapoints.yml`, last checked
20 November 2026.

- Commission Delegated Regulation (EU) 2026/1560 (voluntary standard):
  [EUR-Lex](https://eur-lex.europa.eu/eli/reg_del/2026/1560/oj/eng)
- Commission Recommendation (EU) 2025/1710 (VSME), Basic Module:
  [EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX%3A32025H1710)
