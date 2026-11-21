---
step: "C7"
status: draft
last_checked: 2026-11-21
---

# C7 Datapoint gap analysis

!!! warning "Not legal advice"
    This page uses the key datapoints this handbook lists, not EFRAG's full
    datapoint list. Use the full list for your real gap analysis.

## In one sentence

List every datapoint you must report (ESRS 2 plus your material
standards), mark each one Ready, Partial, Gap or Phase-in, and plan the
work to close the gaps before the reporting year ends.

## Who does this and when

The sustainability lead, with each data owner. Do it once the material
topics are known ([C2](c2-dma.md)), then update it every month or quarter
until the first report.

## Inputs

- The material topics from C2.
- The datapoint list: EFRAG's full list, or the key datapoints in
  [`data/esrs_datapoints.yml`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/data/esrs_datapoints.yml).
- What you already collect: the datasets in
  [F3](../foundations/one-dataset-many-reports.md).

## Steps

### 1. List the datapoints in scope

All ESRS 2 datapoints, plus the datapoints of each material topical
standard.

### 2. Give each one a status

| Status | Meaning |
|---|---|
| Ready | Data, method and owner in place; a dry run worked |
| Partial | Some data, but estimates, missing sites or no owner |
| Gap | Nothing yet |
| Phase-in | You will use a phase-in for it, and say so |

### 3. Link each datapoint to a dataset

A datapoint linked to a dataset you already collect for another report
(Scope 3, VSME, CBAM) is usually quicker to close.

### 4. Plan the gaps

Give each Gap and Partial an owner and a date, and start with the ones
that take longest (transition plan, supplier data).

## Worked example

Mediterranean Logistics Group (fictional) after its 2026 dry run
([C5](c5-climate.md)), on 20 November 2026:

| Datapoint | Standard | Dataset | Status |
|---|---|---|---|
| ESRS2-basis | ESRS 2 | – | Gap |
| ESRS2-governance | ESRS 2 | – | Partial |
| ESRS2-strategy | ESRS 2 | – | Partial |
| ESRS2-materiality-process | ESRS 2 | – | Ready |
| E1-transition-plan | E1 | – | Gap |
| E1-targets | E1 | – | Gap |
| E1-energy | E1 | electricity_use | Ready |
| E1-scope1 | E1 | fuel_use | Ready |
| E1-scope2 | E1 | electricity_use | Ready |
| E1-scope3 | E1 | purchased_goods_spend | Partial |
| E1-scope3-suppliers | E1 | supplier_emissions | Partial |
| E1-financial-effects | E1 | – | Phase-in |
| E5-resources-waste | E5 | – | Partial |
| S1-headcount | S1 | headcount | Ready |
| S1-health-safety | S1 | headcount | Ready |

| Status | Datapoints |
|---|---|
| Ready | 6 |
| Partial | 5 |
| Gap | 3 |
| Phase-in | 1 |
| **Total** | **15** |

**6 of 15 (40%)** are ready. The three gaps are the basis for preparation,
which waits for the phase-in decision, and the transition plan and targets,
which need board decisions. The group starts with those. For the
financial effects phase-in, it checks which E1 paragraphs are excluded
from it.

In Python, with
[`esgcalc.csrd`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/esgcalc/csrd.py):

```python
from esgcalc.csrd import datapoints_in_scope, gap_summary

# datapoints: the list in data/esrs_datapoints.yml
# status: {"ESRS2-basis": "Gap", ...} as in the table above
scope = datapoints_in_scope(datapoints, ["E1", "E5", "S1"])
summary = gap_summary(scope, status)
print(summary.counts["Ready"], summary.total)   # 6 15
```

## Common mistakes

- **Only checking the material topics.** ESRS 2 is always in scope.
- **Marking estimates as Ready.** A spend-based Scope 3 total is Partial
  until the significant categories have better data.
- **One big list with no owners.** Each gap needs an owner and a date.
- **Using the key list as the full list.** This handbook's list is a
  starting point; EFRAG publishes the full one.

## Evidence to keep

- The gap list with dates, so progress can be shown to the board and the
  assurance provider.

File it in the evidence locker (see
[F1](../foundations/evidence-locker.md)).

## Templates and tools

<!-- generated from data/workflows.yml templates: do not edit by hand -->
- **[ESRS datapoint gap list](../downloads/esrs-gap-list.xlsx)** (Excel): The handbook's key ESRS datapoints, generated from its datapoint list, with whether each is in scope for you, its status (Ready, Partial, Gap or Phase-in), an owner and a date, and a summary.
<!-- end generated templates -->

- [ESRS gap check](../tools/esrs-gap.md): the same analysis in your browser.
- [`esgcalc.csrd`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/esgcalc/csrd.py):
  `datapoints_in_scope` and `gap_summary`.

## Reuse in other reports

The dataset column shows where VSME, Scope 3 and CBAM data already cover
an ESRS datapoint. See [F3](../foundations/one-dataset-many-reports.md).

## Sources

Facts come from `data/regulations.yml` (ids `esrs-structure`,
`esrs-phase-in`), last checked 20 November 2026.

- Delegated Regulation (EU) 2026/1563 (revised ESRS):
  [EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ%3AL_202601563)
- EFRAG Knowledge Hub, revised ESRS:
  [EFRAG](https://knowledgehub.efrag.org/interactive/simplified-esrs/esrs-1)
