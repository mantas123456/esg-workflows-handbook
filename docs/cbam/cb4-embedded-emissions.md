---
step: "CB4"
status: draft
last_checked: 2026-11-21
---

# CB4 Embedded emissions: actual vs default values

!!! warning "Not legal advice"
    This page explains the method in plain words. The default values in the
    worked example are **made up**. Use the real values from Implementing
    Regulation (EU) 2025/2621 for your goods and country of origin.

## In one sentence

For each CBAM good, take the specific embedded emissions per tonne, either
actual (verified, from the installation) or default (from the Commission),
and multiply by the tonnes you imported.

## Who does this and when

Whoever prepares the CBAM declaration, with the data collected in
[CB3](cb3-supplier-data.md).

- **During the year:** estimate, to plan certificate purchases and the
  quarterly holding (see [CB8](cb8-certificates.md)).
- **Before the declaration:** final numbers for the year's imports. For
  2026 imports, the declaration is due on 30 September 2027.

## Inputs

- Your import list by CN code, installation and tonnes ([CB1](cb1-scope-check.md)).
- For each installation, either **verified actual data** or the decision
  to use **default values** ([CB3](cb3-supplier-data.md)).
- The default values in Implementing Regulation (EU) 2025/2621, as
  corrected by Implementing Regulation (EU) 2026/1740.

## Steps

### 1. Know what counts for your sector

| Sector | What counts |
|---|---|
| Iron and steel, aluminium, hydrogen | Direct emissions only |
| Cement, fertilisers | Direct **and** indirect emissions |
| Electricity | Separate method, not covered on this page. Its default values are based on the grid emission factor of the country of origin, without the mark-up below |

Direct emissions come from the production process itself. Indirect
emissions come from the electricity the process used.

### 2. Actual values: from the installation's verified data

You may use actual values only when the operator provides data
**verified by an accredited verifier**. The specific embedded emissions
(SEE) of the goods are, in short:

```text
SEE (tCO2e/t) = (direct emissions + indirect emissions if they count
                 + emissions embedded in the precursors used)
                / tonnes of goods produced
```

Ask the operator for the SEE per CN code, with the inputs behind it. Check that it covers the **calendar year of production**, and
that the verification report is attached. [CB5](cb5-precursors.md) shows
the precursor part in detail.

### 3. Default values: when no verified data is available

1. Look up the default value for the CN code and country of origin in
   Annex I of Implementing Regulation (EU) 2025/2621. For iron and steel,
   aluminium and hydrogen, use the **direct** emissions value.
2. Add the **mark-up** for the year of import (goods other than
   electricity):

| Year of import | Mark-up | Fertilisers |
|---|---|---|
| 2026 | 10% | 1% |
| 2027 | 20% | 1% |
| 2028 onwards | 30% | 1% |

The 2026/1740 correction removed the tables' pre-calculated columns
with the mark-up included, to avoid rounding differences. So you apply
the mark-up yourself to the base value.

### 4. Multiply by the tonnes imported

```text
embedded emissions (tCO2e) = SEE (tCO2e/t) x net mass imported (t)
```

Do this per CN code and installation, then add up.

### 5. Compare actual with default

Defaults grow more expensive each year because of the mark-up. Where the
gap is large, it can pay to help an installation get verified (see
[CB6](cb6-verification.md)).

## Worked example

Melita Metals Ltd (fictional, Malta) imported **400 t** of steel bars from
Installation A and **35 t** of aluminium bars from Installation B in 2026
([CB1](cb1-scope-check.md)). Installation A sent verified data;
Installation B did not ([CB3](cb3-supplier-data.md)). All numbers are made
up.

**Installation A: actual values (iron and steel, direct only).** Its
verified 2026 data:

| Item | Value |
|---|---|
| Steel bars produced | 100,000 t |
| Direct emissions (rolling mill) | 8,000 tCO2e |
| Indirect emissions (electricity) | 12,000 tCO2e, **not counted** for iron and steel |
| Crude steel used (precursor) | 104,000 t x 0.55 tCO2e/t = 57,200 tCO2e |

SEE = (8,000 + 57,200) / 100,000 = **0.652 tCO2e/t**

Embedded emissions = 0.652 x 400 t = **260.8 tCO2e**

**Installation B: default values (aluminium, direct only).** Suppose the
base default direct value for these aluminium bars from B's country is
**2.10 tCO2e/t** (made up). With the 2026 mark-up of 10%:

SEE = 2.10 x 1.10 = **2.31 tCO2e/t**

Embedded emissions = 2.31 x 35 t = **80.85 tCO2e**

**Total for 2026:** 260.8 + 80.85 = **341.65 tCO2e**.

**How the default grows.** The same 35 t from Installation B, imported in
later years:

| Year | Mark-up | SEE (tCO2e/t) | Embedded emissions (tCO2e) |
|---|---|---|---|
| 2026 | 10% | 2.31 | 80.85 |
| 2027 | 20% | 2.52 | 88.2 |
| 2028 | 30% | 2.73 | 95.55 |

**What actual data was worth.** Suppose Installation A had sent nothing,
and the base default direct value for its steel bars were **1.60
tCO2e/t** (made up). With the 10% mark-up: 1.60 x 1.10 = 1.76 tCO2e/t,
and 1.76 x 400 t = **704 tCO2e**, instead of 260.8 tCO2e with actual
data.

The same calculation in Python, with
[`esgcalc`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/esgcalc/cbam.py):

```python
from esgcalc.cbam import Precursor, default_value_with_markup, embedded_emissions

a = embedded_emissions(sector="iron_steel", production_mass_t=100_000,
                       direct_tco2e=8_000, indirect_tco2e=12_000,
                       precursors=[Precursor(104_000, 0.55)], imported_mass_t=400)
print(a.see_tco2e_per_t, a.total_tco2e, a.indirect_included)   # 0.652 260.8 False

b_see = default_value_with_markup(2.10, 2026, "aluminium")
print(round(b_see, 2), round(b_see * 35, 2))                     # 2.31 80.85
```

## Common mistakes

- **Adding indirect emissions for steel or aluminium.** They do not count
  for Annex II goods. In the example, adding them would raise
  Installation A's figure.
- **Using unverified "actual" data.** Without verification by an
  accredited verifier, you must use default values.
- **Forgetting the mark-up.** Apply it to the base default value for the
  year of import.
- **Using the total default value for an Annex II good.** For iron and
  steel, aluminium and hydrogen, use the direct value.
- **Mixing years.** Actual data must cover the calendar year of
  production of the goods you imported.
- **Rounding early.** Keep full precision until the final number.

## Evidence to keep

- The operator's data and verification report for each installation using
  actual values.
- The default value used, with the CN code, country, annex reference and
  mark-up year.
- Your calculation file, linked to both in `reported_values.csv` (see
  [F1](../foundations/evidence-locker.md)).

## Templates and tools

<!-- generated from data/workflows.yml templates: do not edit by hand -->
- **[CBAM embedded emissions workbook](../downloads/cbam-emissions-workbook.xlsx)** (Excel): Embedded emissions per CN code from actual installation data (direct, indirect, precursors) or default values with the yearly mark-up, and the certificates and cost that follow.
<!-- end generated templates -->

- [`esgcalc.cbam.embedded_emissions`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/esgcalc/cbam.py)
  and `default_value_with_markup`: the calculations above. Run offline.
- [CBAM calculator](../tools/cbam-calculator.md): actual or default values per CN code, with the
  mark-up, in your browser.

## Reuse in other reports

The embedded emissions per tonne are also supplier-specific emission
factors for Scope 3 category 1, and note whether each is actual or
default. Two cautions before you use them there
([C5](../csrd/c5-climate.md)): for iron and steel and aluminium, CBAM
counts **direct emissions only**, so add the electricity used if the
operator has the figure; and default values carry a **mark-up**, which is a
penalty, not an emission, so take it off. See
[F3](../foundations/one-dataset-many-reports.md).

## Sources

Facts come from `data/regulations.yml` (ids `cbam-direct-only`,
`cbam-actual-or-default`, `cbam-default-values`, `cbam-verification`,
`cbam-declaration`), last checked 20 November 2026.

- Regulation (EU) 2023/956, Article 7 and Annexes II and IV, consolidated
  text:
  [EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:02023R0956-20251020)
- Implementing Regulation (EU) 2025/2621 (default values):
  [EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32025R2621)
- Implementing Regulation (EU) 2026/1740 (correction of the default
  values): [EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ%3AL_202601740)
- European Commission, Guidance No. 3, methods for calculating embedded
  emissions:
  [DG TAXUD](https://taxation-customs.ec.europa.eu/document/download/29b9eec7-1a4b-4eb6-ab85-96a0c9e35fd0_en?filename=Guidance+No.+3+-+CBAM+methods+for+the+calculation+of+emissions+embedded+in+goods.pdf)
