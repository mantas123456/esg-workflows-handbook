---
step: "CB5"
status: draft
last_checked: 2026-11-20
---

# CB5 Precursors and complex goods

!!! warning "Not legal advice"
    This page explains how precursors enter the calculation. The binding
    list of relevant precursors for each production route is in the
    current implementing rules; check it for your goods.

## In one sentence

When your goods are made from other CBAM goods (precursors), their
embedded emissions include the precursors' emissions too, level by level,
using the mass of each precursor that was used up.

## Who does this and when

Ask the installation operator for the calculation; you, the importer,
check it. Do it when you receive the operator's data in
[CB3](cb3-supplier-data.md), before you use it in
[CB4](cb4-embedded-emissions.md).

## Inputs

- The operator's data for the goods you import: production, direct (and,
  where they count, indirect) emissions.
- For each precursor: the **mass consumed**, where it came from, and its
  specific embedded emissions with the verification report covering the
  period it was produced.

## Steps

### 1. Simple or complex?

- **Simple goods** are made only from inputs and fuels with zero embedded
  emissions.
- **Complex goods** are all other goods. Their embedded emissions include
  those of their **relevant precursors**: goods with non-zero embedded
  emissions inside the production boundary.

Steel bars rolled from crude steel, or aluminium bars made from unwrought
aluminium, are complex goods: their input carries embedded emissions.

### 2. List the precursors

Ask the operator to list each relevant precursor. Examples (not the legal
list):

| Your goods | Precursors you may see |
|---|---|
| Iron and steel products | Crude steel, pig iron, direct reduced iron, ferro-alloys |
| Aluminium products | Unwrought aluminium, other aluminium products |

The precursor examples for iron and steel come from the rules for the
transitional period. Check the current implementing rules for the binding
list for your production route.

### 3. Use the mass consumed

Count the tonnes of precursor **used up** in production, not the tonnes
that end up in the product. Losses, offcuts and scale all count.

### 4. Work down level by level

If a precursor is itself a complex good, first work out its own specific
embedded emissions the same way. Repeat until no precursor is left.

```text
SEE of goods = (direct + indirect if they count
                + sum of (precursor mass consumed x precursor SEE))
               / tonnes of goods produced
```

### 5. EU precursors count as zero

A precursor that comes from the EU (or an exempted country) counts with
**zero** embedded emissions. It must still be listed and its quantity
reported.

### 6. Check the evidence for each precursor

Actual data for a precursor may be used only from a **verification report
that covers the period the precursor was produced**. Without it, use the
default value for that precursor (see [CB4](cb4-embedded-emissions.md)).

## Worked example

In [CB4](cb4-embedded-emissions.md), Installation A's steel bars used
104,000 t of crude steel at **0.55 tCO2e/t**. Here is where that figure
comes from. All numbers are made up.

**Level 2: pig iron.** Installation A's electric arc furnace uses pig iron
bought from Installation C, outside the EU. Installation C sends verified
data: **1.90 tCO2e/t**.

**Level 1: crude steel at Installation A.**

| Item | Value |
|---|---|
| Crude steel produced | 104,000 t |
| Direct emissions (electric arc furnace) | 30,600 tCO2e |
| Pig iron consumed | 14,000 t x 1.90 tCO2e/t = 26,600 tCO2e |

SEE of crude steel = (30,600 + 26,600) / 104,000 = **0.55 tCO2e/t**

**Level 0: steel bars.** Installation A used all 104,000 t of crude steel
to roll **100,000 t** of bars. The 4,000 t difference is lost in
production, but it still counts, because the rule uses the mass
consumed.

SEE of bars = (8,000 + 104,000 x 0.55) / 100,000 = **0.652 tCO2e/t**,
and 0.652 x 400 t = **260.8 tCO2e**, as in CB4.

**What if the pig iron came from the EU?** Then it would count as zero,
though Installation A would still list the 14,000 t:

| | Pig iron from outside the EU | Pig iron from the EU |
|---|---|---|
| SEE of crude steel | 0.55 tCO2e/t | 30,600 / 104,000 = 0.294 tCO2e/t |
| SEE of steel bars | 0.652 tCO2e/t | 0.386 tCO2e/t |
| Melita Metals' 400 t | 260.8 tCO2e | 154.4 tCO2e |

**Installation B (aluminium)** sent no verified data, so Melita Metals
uses the default value for the aluminium bars (see CB4) and no precursor
calculation is needed on its side.

In Python, with
[`esgcalc`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/esgcalc/cbam.py),
one call per level:

```python
from esgcalc.cbam import Precursor, embedded_emissions

crude = embedded_emissions(sector="iron_steel", production_mass_t=104_000,
                           direct_tco2e=30_600, precursors=[Precursor(14_000, 1.90)],
                           imported_mass_t=0)
bars = embedded_emissions(sector="iron_steel", production_mass_t=100_000,
                          direct_tco2e=8_000,
                          precursors=[Precursor(104_000, crude.see_tco2e_per_t)],
                          imported_mass_t=400)
print(crude.see_tco2e_per_t, bars.see_tco2e_per_t, bars.total_tco2e)   # 0.55 0.652 260.8

# Pig iron from the EU: listed, but counts as zero
crude_eu = embedded_emissions(sector="iron_steel", production_mass_t=104_000,
                              direct_tco2e=30_600,
                              precursors=[Precursor(14_000, 1.90, zero_rated=True)],
                              imported_mass_t=0)
```

## Common mistakes

- **Treating complex goods as simple.** If the goods were made from steel
  or aluminium with embedded emissions, the precursors count.
- **Using the mass in the product.** Use the mass consumed. In the
  example, that is 104,000 t, not 100,000 t.
- **Stopping one level too early.** If a precursor is itself complex,
  work out its emissions first.
- **Leaving EU precursors off the list.** They count as zero, but you
  still list them and report the quantity.
- **Accepting precursor data from the wrong period.** The verification
  report must cover the period the precursor was produced.

## Evidence to keep

- The operator's precursor list with mass consumed, origin and SEE for
  each precursor.
- The verification report for each precursor with actual data, or the
  default value used.
- Proof of origin for any precursor counted as zero.

File them under `cbam/suppliers/` in the evidence locker (see
[F1](../foundations/evidence-locker.md)).

## Templates and tools

- [`esgcalc.cbam.embedded_emissions`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/esgcalc/cbam.py)
  with `Precursor(mass_t, see_tco2e_per_t, zero_rated=False)`: one call
  per level, as in the example.
- The embedded-emissions workbook planned for this release will have a
  precursor sheet.

## Reuse in other reports

The precursor chain is the same "cradle-to-gate" logic used for product
carbon footprints and supplier-specific Scope 3 factors. The verified
data from the operator can serve both. See
[F3](../foundations/one-dataset-many-reports.md).

## Sources

Facts come from `data/regulations.yml` (ids `cbam-complex-goods`,
`cbam-precursor-examples`, `cbam-actual-or-default`, `cbam-direct-only`),
last checked 20 November 2026.

- Regulation (EU) 2023/956, Annex IV, consolidated text:
  [EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:02023R0956-20251020)
- European Commission, Guidance No. 3, methods for calculating embedded
  emissions:
  [DG TAXUD](https://taxation-customs.ec.europa.eu/document/download/29b9eec7-1a4b-4eb6-ab85-96a0c9e35fd0_en?filename=Guidance+No.+3+-+CBAM+methods+for+the+calculation+of+emissions+embedded+in+goods.pdf)
- Implementing Regulation (EU) 2023/1773 (transitional period), Annex II,
  for the precursor examples:
  [EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX%3A32023R1773)
