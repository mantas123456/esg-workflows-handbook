---
step: "C6"
status: draft
last_checked: 2026-11-20
---

# C6 Other topical standards

!!! warning "Not legal advice"
    This page is an overview in the handbook's own words. It does not list
    every disclosure in each standard. Read the standard for what applies to
    a material topic.

## In one sentence

Besides climate (E1), the revised ESRS have nine topical standards; you
report on a standard only where the materiality assessment found the topic
material, and you plan its data the same way as for E1.

## Who does this and when

The sustainability lead, with the owner of each topic (operations, HR,
purchasing, legal). Start right after the materiality assessment
([C2](c2-dma.md)).

## Inputs

- The list of material topics from C2.
- The key datapoints in
  [`data/esrs_datapoints.yml`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/data/esrs_datapoints.yml).
- Existing data: HR and payroll, waste records, permits, supplier
  questionnaires.

## Steps

### 1. Know the ten topical standards

| Standard | Topic |
|---|---|
| E1 | Climate change (see [C5](c5-climate.md)) |
| E2 | Pollution |
| E3 | Water and marine resources |
| E4 | Biodiversity and ecosystems |
| E5 | Resource use and circular economy |
| S1 | Own workforce |
| S2 | Workers in the value chain |
| S3 | Affected communities |
| S4 | Consumers and end-users |
| G1 | Business conduct |

### 2. Report only on material topics

ESRS 2 applies to everyone ([C4](c4-general.md)). A topical standard
applies where the topic is material, from either side. Keep the reasons
for each topic you found not material.

### 3. Check the phase-ins

First-time reporters may leave out E4, S2, S3 and S4 disclosures in their
first two years, and some datapoints in other standards (see
[C4](c4-general.md)). Say so in the basis for preparation.

### 4. Plan the data for each material topic

For each material standard, list the datapoints, the dataset behind each,
the owner and the date. Reuse data you already collect for other reports
(see [F3](../foundations/one-dataset-many-reports.md)). The gap analysis in
[C7](c7-gap-analysis.md) then shows what is missing.

## Worked example

Mediterranean Logistics Group (fictional) found E1, E5 and S1 material in
C2. Its overview of the topical standards, with the key datapoints this
handbook lists:

| Standard | Material for the group? | Key datapoints | Phase-in for first-time reporters |
|---|---|---|---|
| E1 | Yes | E1-transition-plan, E1-targets, E1-energy, E1-scope1, E1-scope2, E1-scope3, E1-scope3-suppliers, E1-financial-effects | Some datapoints |
| E2 | No | E2-pollution, E2-substances-of-concern | Some datapoints |
| E3 | No | E3-water | – |
| E4 | No | E4-biodiversity | Yes |
| E5 | Yes | E5-resources-waste | – |
| S1 | Yes | S1-headcount, S1-health-safety | Some datapoints |
| S2 | No | S2-value-chain-workers | Yes |
| S3 | No | S3-communities | Yes |
| S4 | No | S4-consumers | Yes |
| G1 | No | G1-business-conduct | – |

For the two material topics besides E1:

- **E5 Resource use and circular economy**: the group starts weighing the
  food it throws away at each cold store, by cause (power cuts, broken
  cold chain, expired stock), because its material impact (E5-I1 in C2) is
  food waste.
- **S1 Own workforce**: headcount and accidents come from payroll and the
  accident book, the same data a VSME report uses (B8, B9 in
  [V2](../vsme/v2-basic.md)). Its material impact (S1-I1) is serious
  accidents, so it also records near misses.

## Common mistakes

- **Reporting on every standard.** Report on material topics, and explain
  the others in the materiality description.
- **Dropping a topic without reasons.** Keep why each topic is not
  material.
- **Using the phase-in silently.** State it.
- **Collecting new data where you already have it.** Payroll, waste
  records and supplier data often serve several reports.

## Evidence to keep

- The reasons for each topic found not material.
- The data plan for each material topic.

File them in the evidence locker (see
[F1](../foundations/evidence-locker.md)).

## Templates and tools

- [`data/esrs_datapoints.yml`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/data/esrs_datapoints.yml):
  the key datapoints per standard.
- [ESRS gap check](../tools/esrs-gap.md), see [C7](c7-gap-analysis.md).

## Reuse in other reports

S1 headcount and accident data also answer VSME B8 and B9
([V2](../vsme/v2-basic.md)) and customer questionnaires
([V5](../vsme/v5-requests.md)). See
[F3](../foundations/one-dataset-many-reports.md).

## Sources

Facts come from `data/regulations.yml` (ids `esrs-structure`,
`esrs-phase-in`, `esrs-simplified`), last checked 20 November 2026.
Standard titles are summarised, not copied.

- Delegated Regulation (EU) 2026/1563 (revised ESRS):
  [EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ%3AL_202601563)
- EFRAG Knowledge Hub, revised ESRS:
  [EFRAG](https://knowledgehub.efrag.org/interactive/simplified-esrs/esrs-1)
