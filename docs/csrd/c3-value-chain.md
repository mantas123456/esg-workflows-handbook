---
step: "C3"
status: draft
last_checked: 2026-11-20
---

# C3 Value chain and data requests

!!! warning "Not legal advice"
    This page explains the value-chain cap and shows how to word requests.
    It does not tell you what you may or may not ask a particular supplier.

## In one sentence

Ask your suppliers for the data you need, but respect the value-chain cap:
for smaller suppliers, stay within the voluntary standard, flag anything
beyond it, and tell them they may refuse.

## Who does this and when

Purchasing and the sustainability lead. Send requests early in the
reporting year, after the materiality assessment ([C2](c2-dma.md)) shows
which topics need value-chain data.

## Inputs

- The material topics from C2 and the datapoints you need for them.
- Your supplier list with each supplier's average number of employees, or
  their own statement of size.
- The voluntary standard's datapoints (see [V1](../vsme/v1-modules.md)).

## Steps

### 1. Check each supplier against the cap

A company reporting under the CSRD may not require a value-chain company
with **on average 1,000 employees or fewer** (previous financial year,
headcount) to give more information than the voluntary standard covers.
You may rely on the supplier's own statement of its size, unless you know
or should know it is manifestly wrong. The cap applies to value-chain
reporting from financial year 2027.

### 2. Map each question to the voluntary standard

For each question, find the voluntary-standard datapoint that answers it.
If there is one, the question is **within the standard**. If there is
none, it is **beyond the standard**.

### 3. Flag what goes beyond, and say the supplier may refuse

For a protected supplier, a request that goes beyond the standard must say
so, and must tell the supplier it has a right to refuse. The cap does not
stop a supplier from sharing more if it wants to, and does not change
existing contracts or legal duties.

### 4. Keep the answers and their quality

Record what each supplier sent, how it was calculated, and whether it was
verified. Use it in your reporting ([C5](c5-climate.md)), and estimate
what is missing.

## Worked example

Mediterranean Logistics Group (fictional) needs supplier data for E1 and
S1 (see C2). Two of its suppliers are the fictional companies from the
other tracks.

| Supplier | Employees | Protected by the cap? |
|---|---|---|
| Gozo Fresh Foods Ltd | 140 | Yes |
| Melita Metals Ltd | 60 | Yes |

Both are protected, so the group maps every question and flags those
beyond the standard:

| Supplier | Question | Voluntary-standard datapoints | Within the standard? | Outcome |
|---|---|---|---|---|
| Gozo Fresh Foods Ltd | Energy use and Scope 1 and 2 emissions for 2026 | B3-energy, B3-scope1, B3-scope2-location | Yes | answered |
| Gozo Fresh Foods Ltd | Number of employees and work accidents | B8-employees, B9-accidents | Yes | answered |
| Gozo Fresh Foods Ltd | Cradle-to-gate emissions of all products sold in 2026 | none | No: flagged, may refuse | shared voluntarily |
| Gozo Fresh Foods Ltd | Carbon footprint per kg of each product | none | No: flagged, may refuse | declined |
| Melita Metals Ltd | Scope 1 and 2 emissions for 2026 | B3-scope1, B3-scope2-location | Yes | answered |
| Melita Metals Ltd | Embedded emissions per tonne of the steel and aluminium bars sold to the group | none | No: flagged, may refuse | shared voluntarily |
| Melita Metals Ltd | Indirect emissions per tonne at the steel mill | none | No: flagged, may refuse | shared voluntarily |

- **Gozo Fresh Foods** already has its Scope 3 inventory
  ([S9](../scope3/s9-reporting.md)) and VSME report
  ([V5](../vsme/v5-requests.md)), so answering costs little. It declines the
  per-product footprint for now, as it did for the supermarket.
- **Melita Metals** already gets embedded emissions from its suppliers for
  CBAM ([CB4](../cbam/cb4-embedded-emissions.md)), so it shares them.

The group uses both answers in its climate figures ([C5](c5-climate.md)).

A request line beyond the standard could read:

> This question goes beyond the voluntary standard for SMEs. You have the
> right to refuse to answer it. If you can share it, it helps us replace an
> estimate with your real figure.

## Common mistakes

- **Sending a full ESRS questionnaire to small suppliers.** Stay within the
  voluntary standard, or flag the extra questions.
- **Not saying the supplier may refuse.** The request must say so for
  questions beyond the standard.
- **Treating a refusal as zero.** Estimate the missing figure instead
  ([S4](../scope3/s4-methods.md)).
- **Asking for data you already have.** Check what the supplier publishes
  first (for example its VSME report).

## Evidence to keep

- Each supplier's size statement and the date.
- The requests sent, with the flags for questions beyond the standard.
- The answers received, with their basis and verification status.

File them in the evidence locker (see
[F1](../foundations/evidence-locker.md)).

## Templates and tools

- [`esgcalc.csrd.protected_by_value_chain_cap`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/esgcalc/csrd.py)
- Supplier questionnaire guidance: [S7](../scope3/s7-suppliers.md).
- The other side of the request: [V5](../vsme/v5-requests.md).

## Reuse in other reports

The supplier data feeds your Scope 3 inventory ([S4](../scope3/s4-methods.md))
and ESRS E1 ([C5](c5-climate.md)). A supplier's CBAM data
([CB4](../cbam/cb4-embedded-emissions.md)) is a ready source of
supplier-specific emission factors. See
[F3](../foundations/one-dataset-many-reports.md).

## Sources

Facts come from `data/regulations.yml` (ids `csrd-value-chain-cap`,
`vsme`), last checked 20 November 2026.

- Directive 2013/34/EU, Article 29b(4), as amended by Directive (EU)
  2026/470: [EUR-Lex](https://eur-lex.europa.eu/eli/dir/2026/470/oj/eng)
- European Commission, explanatory information on the value-chain cap:
  [European Commission](https://finance.ec.europa.eu/news/feedback-sustainability-reporting-standards-additional-explanatory-information-regarding-value-chain-2026-05-06_en)
