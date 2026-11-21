---
step: "CB3"
status: draft
last_checked: 2026-11-21
---

# CB3 Requesting data from installation operators

!!! warning "Not legal advice"
    This page explains how to ask producers outside the EU for emissions
    data. It does not replace the CBAM Regulation or the Commission's
    guidance for operators.

## In one sentence

Ask each installation that makes your CBAM goods for verified embedded
emissions data early in the year, so you can choose between actual
values and default values in good time.

## Who does this and when

Purchasing or the supplier manager, with the sustainability lead or
whoever prepares the CBAM declaration.

- **When:** at the start of each calendar year, or when you sign a new
  supplier. For operators the reporting period is the **calendar year in
  which the goods were produced**, and the data must be verified before
  you can use it. For 2026 imports, the declaration is due on 30 September
  2027.
- **Why early:** without verified actual data you must use the
  Commission's default values (see [CB4](cb4-embedded-emissions.md)).

## Inputs

- Your CB1 import list, grouped by **installation** (the plant that made
  the goods), not just by supplier or trader.
- Contact details for each installation, through your supplier if
  needed.
- The Commission's operator template and guidance (links under
  *Templates and tools*).

## Steps

### 1. Find the installation behind each import

Your supplier may be a trader. CBAM data comes from the **installation
that produced the goods**. Ask your supplier to name each installation
and to put you in contact with its operator.

### 2. Rank installations by tonnes

Start with the installations behind most of your tonnes. Those are the
ones where actual data can change your certificate cost the most.

### 3. Send one clear request per installation

Ask for:

| What to ask for | Why you need it | Used in |
|---|---|---|
| Installation name, location and the CN codes it made for you | To match data to your imports | [CB1](cb1-scope-check.md), [CB4](cb4-embedded-emissions.md) |
| Specific embedded emissions per CN code for the calendar year of production (tCO2e per tonne), direct and, for cement and fertilisers, indirect | The core number for the declaration | [CB4](cb4-embedded-emissions.md) |
| The precursors used, with their own embedded emissions and the period they were produced | Complex goods include precursor emissions | [CB5](cb5-precursors.md) |
| The verification report from an accredited verifier | Actual data can only be used when verified | [CB6](cb6-verification.md) |
| Evidence of any carbon price paid in the country of production | May reduce the certificates you surrender | [CB7](cb7-carbon-price-paid.md) |

Ask the operator to use the **Commission's operator emissions report
template**. It is made for passing this data to authorised CBAM
declarants. Ask whether the operator has registered in the **Operators
Portal of the CBAM Registry**.

### 4. Agree dates in writing

Agree when you will receive the verified data for each production year.
Put it in the supply contract or a side letter if you can. Leave enough
time before your own declaration deadline to check the data.

### 5. Record the answer and decide

For each installation, record one of two outcomes:

- **Actual values:** the operator will send verified data.
- **Default values:** no verified data is coming. Plan to use the
  Commission's default values for those goods, and budget for the
  mark-up (see [CB4](cb4-embedded-emissions.md)).

Re-ask every year. An operator that could not help this year may have a
verifier next year.

## Worked example

Melita Metals Ltd (fictional, Malta) imports from two installations
outside the EU. From [CB1](cb1-scope-check.md), by installation:

| Installation | Goods | Net mass 2026 (t) | Share of tonnes |
|---|---|---|---|
| A (steel mill) | Rebar and steel bars, CN 7214 | 400 | 92% |
| B (aluminium plant) | Aluminium alloy bars, CN 7604 | 35 | 8% |
| **Total** | | **435** | **100%** |

On 2 February 2026, Melita Metals sends the same request to both.

| Installation | Answer | Outcome |
|---|---|---|
| A | Will provide 2026 data, verified by an accredited verifier, using the Commission template | Actual values |
| B | Cannot arrange verification for 2026 | Default values |

So **92%** of Melita Metals' tonnes will have actual, verified data. For
the other **8%** it will use default values. [CB4](cb4-embedded-emissions.md)
shows what that means in tonnes of CO2e.

## Common mistakes

- **Asking the trader instead of the installation.** The data must come
  from the plant that made the goods.
- **Accepting unverified numbers.** Actual data can only be used when an
  accredited verifier has checked it. Unverified numbers are not enough.
- **Asking once, late.** Ask at the start of the year, agree dates, and
  follow up.
- **One request covering the wrong year.** The operator's period is the
  calendar year of **production**, which can differ from the year you
  imported.
- **Forgetting precursors.** For complex goods, the embedded emissions
  include those of the precursors used to make them. Ask for them in the
  same request. See [CB5](cb5-precursors.md).
- **Writing your own form from scratch.** Point operators to the
  Commission's template. It was made for passing this data to authorised
  declarants, and many operators already know it.

## Evidence to keep

- Each request, with date and recipient.
- Each answer, the data received, and the verification report.
- Your decision per installation (actual or default) and why.

File them under `cbam/suppliers/` in the evidence locker (see
[F1](../foundations/evidence-locker.md)).

## Templates and tools

<!-- generated from data/workflows.yml templates: do not edit by hand -->
- **[CBAM supplier data request](../downloads/cbam-supplier-request.docx)** (Word): Cover letter asking an installation operator outside the EU for verified embedded emissions data, pointing to the Commission's official operator template.
<!-- end generated templates -->

- **Commission operator template and guidance:** on the DG TAXUD
  [CBAM legislation and guidance](https://taxation-customs.ec.europa.eu/carbon-border-adjustment-mechanism/cbam-legislation-and-guidance_en)
  page, and
  [Guidance No. 2 for non-EU operators](https://taxation-customs.ec.europa.eu/system/files/2026-08/Guidance%20No.%202%20-%20Quick%20guide%20for%20non-EU%20operators%20on%20CBAM%20implementation.pdf).
  Use the official template; this handbook links to it and does not copy
  it.

## Reuse in other reports

The same verified data per installation is **supplier-specific data** for
Scope 3 category 1. It replaces a spend-based estimate for those goods.
Two cautions before you use them there
([C5](../csrd/c5-climate.md)): for iron and steel and aluminium, CBAM
counts **direct emissions only**, so add the electricity used if the
operator has the figure; and default values carry a **mark-up**, which is a
penalty, not an emission, so take it off. Send one request that covers both. See
[F3](../foundations/one-dataset-many-reports.md).

## Sources

Facts come from `data/regulations.yml` (ids `cbam-actual-or-default`,
`cbam-operator-template-and-portal`, `cbam-verification`,
`cbam-direct-only`, `cbam-declaration`), last checked 20 November 2026.

- Regulation (EU) 2023/956, Articles 7, 8 and 10 and Annex IV,
  consolidated text:
  [EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:02023R0956-20251020)
- European Commission, Guidance No. 1, Introduction to CBAM concepts:
  [DG TAXUD](https://taxation-customs.ec.europa.eu/system/files/2026-08/Guidance%20No.%201%20-%20Introduction%20to%20CBAM%20concepts.pdf)
- European Commission, Guidance No. 2, Quick guide for non-EU operators:
  [DG TAXUD](https://taxation-customs.ec.europa.eu/system/files/2026-08/Guidance%20No.%202%20-%20Quick%20guide%20for%20non-EU%20operators%20on%20CBAM%20implementation.pdf)
