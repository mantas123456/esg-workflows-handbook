---
step: "V4"
status: draft
last_checked: 2026-11-20
---

# V4 Comprehensive module

!!! warning "Not legal advice"
    This page covers the Comprehensive Module at the level of its topics.
    This handbook has checked the titles of C1 to C9, not their full
    content: read Annex I of Delegated Regulation (EU) 2026/1560 for what
    each disclosure asks. The numbers in the worked example are made up.

## In one sentence

If a bank, investor or large customer needs more than the Basic Module,
plan the Comprehensive disclosures C1 to C9 on top of it, starting with the
ones you were actually asked about.

## Who does this and when

The owner or finance lead, with HR and the site manager, after choosing
Option B in [V1](v1-modules.md) and collecting the Basic Module data
([V2](v2-basic.md)). Most C disclosures are short texts; plan a few weeks.

## Inputs

- The requests that led to Option B ([V1](v1-modules.md)).
- The Basic Module data, which the C disclosures build on ([V2](v2-basic.md)).
- Board and management decisions: targets, policies, plans.

## Steps

### 1. Start from the Basic Module

The Comprehensive Module comes on top of B1 to B11, never instead of them.

### 2. Know the nine topics

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

Some parts are voluntary for undertakings with 10 employees or fewer. The
2026 act renamed C7 ("Human rights incidents") and C8 ("Revenues from
certain activities") compared with the 2025 Recommendation.

### 3. Read the exact content in Annex I

Before writing each disclosure, read what Annex I of the act asks. This
handbook does not reproduce it, and has not checked the detail of each C
disclosure.

### 4. Put the most effort where you were asked

A bank asking about climate needs a real answer to C3 (targets and
transition) and C4 (climate risks). Other C disclosures may be a few lines.

### 5. For targets, set them yourself and show the path

A target is your decision. State the scope, base year, target year and
reduction, and show how you plan to get there year by year. Use the same
base year as your inventory ([S8](../scope3/s8-base-year.md)).

### 6. Plan who writes what, by when

One owner and one date per disclosure, as for the data plan
([S3](../scope3/s3-data-plan.md)).

## Worked example

Gozo Fresh Foods Ltd (fictional) chose Option B because its bank asked
about climate targets and risks ([V1](v1-modules.md)). All plans and
numbers are made up.

**The plan**

| Disclosure | What Gozo will report | Source | Ready by |
|---|---|---|---|
| C1 | Products (prepared vegetables, sauces, ready meals), main customers (supermarkets in Malta), one site in Gozo | Management | 31 Jan 2027 |
| C2 | More detail on the energy, waste and workforce practices listed in B2 | Site manager and HR | 31 Jan 2027 |
| C3 | Target: Scope 1 and 2 down 30% by 2030 from 2026; actions: heat pumps instead of LPG, refrigerant replacement, electric vans | Management | 28 Feb 2027 |
| C4 | Heatwaves straining the cold chain; water scarcity in Malta; higher energy prices; customers asking for lower-carbon products | Management with the site manager | 28 Feb 2027 |
| C5 | More workforce detail, from payroll | HR | 31 Jan 2027 |
| C6 | Human rights policy and how workers can raise concerns | HR | 28 Feb 2027 |
| C7 | Incidents in 2026: none recorded | HR and legal records | 31 Jan 2027 |
| C8 | Check whether any revenue comes from the activities the standard lists; Gozo expects none | Finance | 31 Jan 2027 |
| C9 | Board of 5: 2 women, 3 men | Company secretary | 31 Jan 2027 |

**C3: the target path.** Scope 1 and 2 were **1,800 tCO2e** in 2026
([V2](v2-basic.md)). Gozo's own target is **−30% by 2030**, so
1,800 × 0.70 = **1,260 tCO2e**. A straight line falls by 135 tCO2e a year:

| Year | Scope 1 and 2 on the path (tCO2e) |
|---|---|
| 2026 (base) | 1,800 |
| 2027 | 1,665 |
| 2028 | 1,530 |
| 2029 | 1,395 |
| 2030 (target) | 1,260 |

Each year Gozo compares its actual Scope 1 and 2 with this path, and
recalculates the base year under its policy if needed
([S8](../scope3/s8-base-year.md)). The target is Gozo's own; this
handbook does not judge whether it is enough.

**C9: the board.** Five members, 2 women and 3 men (40% women). Gozo
checks in Annex I how the standard wants the ratio expressed.

In Python, with
[`esgcalc`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/esgcalc/vsme.py):

```python
from esgcalc.vsme import linear_target_path

print(linear_target_path(1800, 2026, 2030, 0.30))
# {2026: 1800.0, 2027: 1665.0, 2028: 1530.0, 2029: 1395.0, 2030: 1260.0}
```

## Common mistakes

- **Writing every C disclosure at the same length.** Put the effort where
  you were asked.
- **A target without a base year or scope.** State scope, base year,
  target year and reduction.
- **A target with no path.** Show the yearly steps and the actions behind
  them.
- **Climate risks copied from a template.** Name the risks that apply to
  your sites and products.
- **Relying on this page for the exact content.** Read Annex I.

## Evidence to keep

- Board or management decisions on targets and policies, dated.
- The target calculation and the yearly comparison with the path.
- The sources behind each C disclosure.

File them in the evidence locker (see
[F1](../foundations/evidence-locker.md)).

## Templates and tools

- [`esgcalc.vsme.linear_target_path`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/esgcalc/vsme.py):
  the target path above.

## Reuse in other reports

A bank's climate questions, a customer's supplier questionnaire and C3 and
C4 ask much the same. One set of answers serves all of them
([V5](v5-requests.md)). See [F3](../foundations/one-dataset-many-reports.md).

## Sources

Facts come from `data/regulations.yml` (ids `vsme`, `vsme-modules`) and
`data/vsme_datapoints.yml`, last checked 20 November 2026.

- Commission Delegated Regulation (EU) 2026/1560 (voluntary standard),
  Annex I:
  [EUR-Lex](https://eur-lex.europa.eu/eli/reg_del/2026/1560/oj/eng)
- EFRAG Knowledge Hub, 2026 Voluntary Standard:
  [knowledgehub.efrag.org](https://knowledgehub.efrag.org/eng/interactive/voluntary-standard)
