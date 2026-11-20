---
step: "V1"
status: draft
last_checked: 2026-11-20
---

# V1 Choosing the modules

!!! warning "Not legal advice"
    This page explains the voluntary standard's structure in plain words.
    It does not copy the standard. Read Delegated Regulation (EU) 2026/1560
    for the exact requirements.

## In one sentence

Decide whether to report the Basic Module only (Option A) or the Basic and
Comprehensive Modules (Option B), based on what your customers, banks and
investors actually ask for.

## Who does this and when

The owner or finance lead of a smaller company, usually after the first
customer or bank questionnaire arrives. Decide once a year, before you
start collecting data ([V2](v2-basic.md)).

## Inputs

- The questionnaires and requests you received in the last year, and who
  sent them.
- Your average number of employees.
- The data you already collect, for example for Scope 3 or CBAM
  ([F3](../foundations/one-dataset-many-reports.md)).

## Steps

### 1. Check that the voluntary standard fits you

The voluntary standard is for undertakings with on average **1,000
employees or fewer**. Using it is **voluntary**, and it requires no
assurance. The delegated act applies to financial years from 1 January
2027; it builds on the VSME standard of the 2025 Commission Recommendation,
which you can already follow for 2026.

### 2. Know the two modules

| Module | Disclosures | What it is for |
|---|---|---|
| **Basic** | B1 to B11 | The minimum: energy and emissions, pollution, biodiversity, water, waste, workforce, corruption |
| **Comprehensive** | C1 to C9 | More detail that banks, investors and large customers often ask for: business model, climate targets and risks, human rights, revenues from certain activities, board gender diversity |

You always report the **Basic** Module first. The Comprehensive Module
comes on top of it, never instead of it.

### 3. List what you are being asked

Write down each request and match it to a disclosure (B1 to B11, C1 to C9).
The datapoint tables below and in [V2](v2-basic.md) and
[V4](v4-comprehensive.md) help.

### 4. Choose the option

- **Option A, Basic Module only**, if every request maps to B1 to B11.
- **Option B, Basic and Comprehensive Modules**, if any request needs a
  C disclosure.

State the option in B1, with a statement that you comply with the
standard.

### 5. Small companies: check what is voluntary

Some disclosures are voluntary for undertakings with **10 employees or
fewer**. Check which before you collect data.

### 6. Review every year

Requests change. A new bank or customer can move you from Option A to B.

## Basic Module datapoints

<!-- generated from data/vsme_datapoints.yml: module=basic -->
| Datapoint | What it covers | Unit | Dataset | Checked against |
|---|---|---|---|---|
| B1-option | Which option is used: Basic only (A) or Basic and Comprehensive (B), with a statement of compliance | text | – | 2026 act |
| B1-basis | Basis for preparation: consolidated or individual, the entities and sites covered | text | – | Topic only |
| B2-practices | Practices, policies and future plans for moving towards a more sustainable economy | text | – | Topic only |
| B3-energy | Total energy consumption, split into renewable and non-renewable where the data can be obtained | MWh | `electricity_use` | 2025 Recommendation |
| B3-energy-fuels | Energy from fuels, part of total energy consumption | MWh | `fuel_use` | 2025 Recommendation |
| B3-scope1 | Gross Scope 1 GHG emissions, following the GHG Protocol Corporate Standard | tCO2e | `fuel_use` | 2025 Recommendation |
| B3-scope2-location | Gross location-based Scope 2 GHG emissions | tCO2e | `electricity_use` | 2025 Recommendation |
| B3-intensity | GHG intensity: total GHG emissions divided by turnover | tCO2e per EUR | – | 2025 Recommendation |
| B4-pollution | Emissions of pollutants to air, water and soil, where the undertaking already reports them under law or an environmental management system | kg | – | Topic only |
| B5-sensitive-sites | Number and area of sites owned, leased or managed in or near biodiversity-sensitive areas | count and ha | – | 2025 Recommendation |
| B5-land-use | Land use: total, sealed and nature-oriented area (optional) | ha | – | 2025 Recommendation |
| B6-water-consumption | Water consumption (withdrawal minus discharge), for undertakings whose production uses water significantly | m3 | – | 2025 Recommendation |
| B7-waste | Waste generated, split into hazardous and non-hazardous | t | – | 2025 Recommendation |
| B7-waste-recycled | Waste diverted to recycling or reuse | t | – | 2025 Recommendation |
| B8-employees | Employees by contract type (permanent or temporary), gender and, if in more than one country, by country | headcount or FTE | `headcount` | 2025 Recommendation |
| B8-turnover-rate | Employee turnover rate, for undertakings with 50 or more employees | % | `headcount` | 2025 Recommendation |
| B9-accidents | Number and rate of recordable work-related accidents (per 100 full-time workers, based on 2,000 hours a year) | count and rate | – | 2025 Recommendation |
| B9-fatalities | Fatalities from work-related injuries and ill health | count | – | 2025 Recommendation |
| B10-pay-gap | Gender pay gap (may be left out below 150 employees; below 100 from 7 June 2031) | % | – | 2025 Recommendation |
| B10-collective-bargaining | Share of employees covered by collective bargaining agreements | % | – | 2025 Recommendation |
| B10-training | Average annual training hours per employee, by gender | hours | – | 2025 Recommendation |
| B11-corruption | Convictions and total fines for breaches of anti-corruption and anti-bribery laws | count and EUR | – | 2025 Recommendation |
<!-- end generated vsme datapoints -->

## Comprehensive Module disclosures

<!-- generated from data/vsme_datapoints.yml: module=comprehensive -->
| Datapoint | What it covers | Unit | Dataset | Checked against |
|---|---|---|---|---|
| C1-business-model | Business model and sustainability-related initiatives (some parts voluntary for 10 employees or fewer) | text | – | 2026 act |
| C2-practices | More detail on the practices, policies and future plans reported in B2 | text | – | Topic only |
| C3-targets | GHG reduction targets and climate transition | text and tCO2e | – | 2025 Recommendation |
| C4-climate-risks | Climate-related hazards and transition risks, and how the undertaking responds | text | – | 2025 Recommendation |
| C5-workforce | More characteristics of the workforce | various | `headcount` | Topic only |
| C6-human-rights-policies | Human rights policies and processes for the own workforce | text | – | Topic only |
| C7-human-rights-incidents | Human rights incidents involving the workforce or the value chain | text and count | – | 2026 act |
| C8-revenues | Revenues from certain activities | EUR | – | 2026 act |
| C9-board-gender | Gender diversity ratio in the governance body | ratio | – | 2026 act |
<!-- end generated vsme datapoints -->

"Checked against" says how far this handbook verified each line: against
the 2026 delegated act, against the 2025 Recommendation the act builds on,
or only its topic.

## Worked example

Gozo Fresh Foods Ltd (fictional, Malta, 140 employees) receives four
requests about 2026 ([S1](../scope3/s1-boundary.md)). All requests are made
up.

| From | Asks for | Disclosures |
|---|---|---|
| Supermarket (reports under the CSRD) | Energy use, Scope 1 and 2 emissions, and Scope 3 | B3 |
| Bank (loan renewal) | Workforce size and work accidents | B8, B9 |
| Bank (loan renewal) | Climate targets and how climate change could affect the business | C3, C4 |
| Supermarket (reports under the CSRD) | Waste and packaging | B7 |

The bank's climate questions need **C3** and **C4**, which are in the
Comprehensive Module. So Gozo Fresh Foods chooses **Option B**: the Basic
Module (22 datapoints) plus the Comprehensive Module (9 disclosures).

The supermarket also asks for **Scope 3**, which the Basic Module does not
require. Gozo already has it from its Scope 3 inventory
([S9](../scope3/s9-reporting.md)), so it can share it anyway.
[V3](v3-ghg.md) shows how the emissions fit together, and
[V5](v5-requests.md) how to answer requests beyond the standard.

## Common mistakes

- **Starting with the Comprehensive Module.** The Basic Module always comes
  first.
- **Choosing Option B "to be safe".** It is more work. Choose it when a
  request needs it.
- **Forgetting the statement in B1.** Say which option you use and that you
  comply with the standard.
- **Treating the standard as a legal duty.** It is voluntary; customers'
  questionnaires are what make it useful.
- **Collecting new data you already have.** Reuse Scope 3, CBAM and payroll
  data ([F3](../foundations/one-dataset-many-reports.md)).

## Evidence to keep

- The requests received, with dates and senders.
- The mapping of each request to a disclosure, and the option chosen.

File them in the evidence locker (see
[F1](../foundations/evidence-locker.md)).

## Templates and tools

- [VSME readiness](../tools/vsme-readiness.md): tick the datapoints you
  have, for Option A or B, and get completeness and a to-do list.
- [`data/vsme_datapoints.yml`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/data/vsme_datapoints.yml):
  the datapoint list behind the tables above.

## Reuse in other reports

The same datapoints answer customer and bank questionnaires
([V5](v5-requests.md)), and many of them reuse data from Scope 3, CBAM and
payroll. See [F3](../foundations/one-dataset-many-reports.md).

## Sources

Facts come from `data/regulations.yml` (ids `vsme`, `vsme-modules`,
`vsme-basic-metrics`) and `data/vsme_datapoints.yml`, last checked
20 November 2026.

- Commission Delegated Regulation (EU) 2026/1560 (voluntary standard):
  [EUR-Lex](https://eur-lex.europa.eu/eli/reg_del/2026/1560/oj/eng)
- Commission Recommendation (EU) 2025/1710 (VSME):
  [EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX%3A32025H1710)
- EFRAG Knowledge Hub, 2026 Voluntary Standard:
  [knowledgehub.efrag.org](https://knowledgehub.efrag.org/eng/interactive/voluntary-standard)
