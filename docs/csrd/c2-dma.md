---
step: "C2"
status: draft
last_checked: 2026-11-21
---

# C2 Double materiality assessment

!!! warning "Not legal advice"
    This page explains the method in the revised ESRS and shows one way to
    score it. The scale and thresholds here are this handbook's choices, not
    the standard's. Your auditor and adviser decide what is acceptable for you.

## In one sentence

List the impacts, risks and opportunities of your business and its value
chain, score each one from both sides (impact on people and the environment,
and financial effect on you), and report on every topic that is material
from either side.

## Who does this and when

A sustainability lead, with finance, operations, HR and purchasing, and
input from affected stakeholders. The board approves the result. Start
about a year before the first reporting year ends, and review it every year.

## Inputs

- Your business model and value chain: what you buy, from where, and who
  your customers are.
- Existing data: Scope 3 screening ([S2](../scope3/s2-screening.md)),
  accident records, complaints, risk register.
- Views of affected stakeholders: workers, suppliers, customers,
  communities.
- The ten topical standards as a checklist: E1 to E5, S1 to S4 and G1.

## Steps

### 1. List impacts, risks and opportunities

Go through each topical standard. For each topic, write down:

- **impacts** you have, or could have, on people or the environment, in
  your own operations **and in your value chain**;
- **risks and opportunities**: things that could affect your cash flows,
  costs, access to finance or value.

Mark each impact as **actual or potential**, **negative or positive**, and
whether it concerns **human rights**. Note for each item **where** it arises
(own operations, upstream or downstream) and its **time horizon** (short,
medium or long term): the financial side asks about effects over all three
horizons. The IRO register (download below) has columns for both.

Talk to affected stakeholders, or their representatives, before scoring,
and keep a note of who you spoke to and what they said.

### 2. Score impact materiality

The revised ESRS (ESRS 1, chapter 3) say, in short:

- The **severity** of a negative impact depends on its **scale**, **scope**
  and **irremediable character**. Any one of the three can make it severe.
- **Actual** negative impacts are judged on severity. **Potential** ones on
  severity and **likelihood**.
- For potential **human rights** impacts, severity takes precedence over
  likelihood.
- Positive impacts are judged on scale and scope (and likelihood if
  potential).
- Count prevention and mitigation only if they are already in place and
  work.

### 3. Score financial materiality

A risk or opportunity is material if it triggers, or could reasonably be
expected to trigger, material financial effects in the short, medium or
long term. This handbook scores **magnitude x likelihood**.

### 4. Set and write down your thresholds

The ESRS give **no numbers**. You choose the scale, how to combine the
scores and the thresholds, and you explain them. This handbook uses a 1 to
5 scale and a threshold of 3.0 on both sides. See
[`data/dma_parameters.yml`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/data/dma_parameters.yml),
where each setting is marked as an ESRS rule or a handbook choice.

### 5. Roll up to topics

A topic is **material if any of its items is material, from either side**.
That is the "double" in double materiality.

### 6. Document the process

ESRS 2 asks for a concise description of how you did the assessment,
including how it covered own operations and the value chain
([C4](c4-general.md)). Keep the scores, the reasons and who took part.

## Worked example

Mediterranean Logistics Group (fictional) scores nine items, after
talking to drivers' and warehouse staff representatives, two supermarket
customers and its main hauliers. The IRO register records where each item
arises and its time horizon. All scores are made up.

| Item | Topic | Description | Type | How it is scored | Score | Material? |
|---|---|---|---|---|---|---|
| S1-I1 | S1 | Serious road and warehouse accidents involving drivers and staff | Impact | potential human rights impact: severity 5 takes precedence over likelihood 3 | 5.0 | Yes |
| E1-I1 | E1 | GHG emissions from the diesel truck fleet and the cold stores | Impact | actual negative: severity 4 | 4.0 | Yes |
| E1-R1 | E1 | Rising fuel and carbon costs for the diesel fleet | Risk | magnitude 4 x likelihood 4 / 5 | 3.2 | Yes |
| E5-I1 | E5 | Food wasted when the cold chain fails | Impact | actual negative: severity 3 | 3.0 | Yes |
| E2-I1 | E2 | Air pollution from trucks in towns | Impact | potential negative: severity 3 x likelihood 4 / 5 | 2.4 | No |
| S1-R1 | S1 | Shortage of truck drivers | Risk | magnitude 3 x likelihood 4 / 5 | 2.4 | No |
| E1-O1 | E1 | Supermarkets choosing low-carbon logistics | Opportunity | magnitude 3 x likelihood 3 / 5 | 1.8 | No |
| S2-I1 | S2 | Poor working conditions on farms that supply food suppliers | Impact | potential negative: severity 3 x likelihood 2 / 5 | 1.2 | No |
| G1-R1 | G1 | Bribery at ports and customs | Risk | magnitude 2 x likelihood 2 / 5 | 0.8 | No |

Two items show the rules at work:

- **S1-I1** is unlikely (likelihood 3), but a fatal accident cannot be put
  right (irremediability 5). It is a human rights impact, so severity takes
  precedence: score 5.0.
- **S2-I1** is also about human rights, but its severity is 3, below this
  handbook's cut-off of 4, so likelihood counts: 3 x 2 / 5 = 1.2.

Rolled up to topics:

| Topic | Impact material? | Financial material? | Material? |
|---|---|---|---|
| E1 | Yes | Yes | Yes |
| E2 | No | No | No |
| E5 | Yes | No | Yes |
| G1 | No | No | No |
| S1 | Yes | No | Yes |
| S2 | No | No | No |

The group also went through E3, E4, S3 and S4 and found no impacts, risks
or opportunities worth scoring; it records why for each.

So the group reports on **E1, E5 and S1**, plus the general disclosures in
ESRS 2. E1 is material from both sides. E5 and S1 are material from the
impact side only, which is enough.

In Python, with
[`esgcalc.dma`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/esgcalc/dma.py):

```python
from esgcalc.dma import IRO, assess

s1 = IRO("S1-I1", "S1", "Serious accidents", "impact", actual=False, human_rights=True,
         scale=4, scope=3, irremediability=5, likelihood=3)
a = assess(s1)
print(a.score, a.material)   # 5.0 True
```

## Common mistakes

- **Only looking at your own operations.** The assessment must cover the
  value chain too. Use your Scope 3 screening and supplier data
  ([C3](c3-value-chain.md)).
- **Averaging away a severe impact.** Any one of scale, scope and
  irremediability can make an impact severe.
- **Letting likelihood hide a human rights impact.** For potential human
  rights impacts, severity comes first.
- **Counting planned measures.** Only prevention that is in place and works
  can lower a score.
- **Presenting the thresholds as the standard's.** They are yours. Explain
  them.
- **Doing it once.** Review it every year.

## Evidence to keep

- The list of items, with scores and the reason for each score.
- The scale, method and thresholds, and who approved them.
- Who took part, including stakeholders consulted.
- The board's approval.

File them in the evidence locker (see
[F1](../foundations/evidence-locker.md)).

## Templates and tools

<!-- generated from data/workflows.yml templates: do not edit by hand -->
- **[Double materiality assessment workbook](../downloads/dma-workbook.xlsx)** (Excel): Score impacts, risks and opportunities on a 1 to 5 scale, from the impact side and the financial side, and roll them up to the ten topical standards.
- **[IRO register](../downloads/iro-register.xlsx)** (Excel): A register of impacts, risks and opportunities (IROs) with where they arise in the value chain, the time horizon, the materiality result, the owner, the actions and the ESRS datapoints they feed.
<!-- end generated templates -->

- [DMA scoring tool](../tools/dma-scoring.md): score items in your browser.
- [`esgcalc.dma`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/esgcalc/dma.py):
  `assess`, `assess_all` and `topics`.

## Reuse in other reports

The same list of impacts, risks and opportunities feeds the climate risks
in a VSME report ([V4](../vsme/v4-comprehensive.md)) and the Scope 3
significance reasons ([S2](../scope3/s2-screening.md)). See
[F3](../foundations/one-dataset-many-reports.md).

## Sources

Facts come from `data/regulations.yml` (ids `esrs-dma-method`,
`esrs-structure`, `esrs-simplified`), last checked 20 November 2026. The
method is cited, not copied.

- Delegated Regulation (EU) 2026/1563 (revised ESRS), Annex I, ESRS 1
  chapter 3:
  [EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ%3AL_202601563)
- EFRAG Knowledge Hub, revised ESRS 1:
  [EFRAG](https://knowledgehub.efrag.org/eng/interactive/simplified-esrs/esrs-1/2026-09-21-official-journal)
