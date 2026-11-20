---
step: "CB9"
status: draft
last_checked: 2026-11-20
---

# CB9 The annual CBAM declaration

!!! warning "Not legal advice"
    This page summarises what the declaration contains. Submit it in the
    CBAM registry following your competent authority's instructions.

## In one sentence

Once a year, the authorised CBAM declarant reports the goods imported in
the previous year, their embedded emissions and the certificates to
surrender, and surrenders them by 30 September.

## Who does this and when

The authorised CBAM declarant. The first declaration, for 2026 imports,
and the surrender are due by **30 September 2027**.

## Inputs

Everything from the earlier steps:

- quantities by type of goods ([CB1](cb1-scope-check.md));
- embedded emissions, actual or default ([CB4](cb4-embedded-emissions.md),
  [CB5](cb5-precursors.md));
- verification reports where actual values are used ([CB6](cb6-verification.md));
- any carbon-price-paid reduction ([CB7](cb7-carbon-price-paid.md));
- the free allocation adjustment and certificates ([CB8](cb8-certificates.md)).

## Steps

### 1. Assemble the content

The declaration states:

1. the **total quantity of each type of goods** imported in the previous
   year;
2. their **total embedded emissions**;
3. the **number of certificates to surrender**, after the carbon-price-paid
   reduction and the free allocation adjustment;
4. **copies of the verification reports** where actual values are used.

### 2. Check it against the evidence

Every number should trace back to a file in your evidence locker
([CB10](cb10-records.md)).

### 3. Make sure the certificates are there

Your account must hold enough certificates to surrender
([CB8](cb8-certificates.md)).

### 4. Submit and surrender by 30 September

Submit early. Leave time to fix registry or data problems.

## Worked example

Melita Metals Ltd's (fictional) declaration for 2026 imports, submitted
on **10 September 2027**, before the 30 September deadline. All numbers
are made up.

| Item | Steel bars (Installation A) | Aluminium bars (Installation B) | Total |
|---|---|---|---|
| Quantity imported (t) | 400 | 35 | 435 |
| Basis | Actual, verified | Default value + 10% mark-up | |
| Embedded emissions (tCO2e) | 260.8 | 80.85 | 341.65 |
| Free allocation adjustment (tCO2e) | 234.0 | 68.25 | 302.25 |
| Carbon-price-paid reduction | | | 0 |
| **Certificates to surrender** | | | **39.4** |
| Verification report attached | Yes (Verifier V, issued 15 Mar 2027) | Not needed (default values) | |

## Common mistakes

- **Leaving it to September.** Data, verification and certificates take
  months. Start the year before.
- **Missing verification reports.** Where you use actual values, attach
  them.
- **Mismatched totals.** Quantities should match your customs data; the
  certificates should match your calculation.
- **Not enough certificates on the account.** Check the balance before you
  submit.

## Evidence to keep

- The declaration as submitted, with the submission date.
- The working file behind every number, and the source files it uses.

## Templates and tools

<!-- generated from data/workflows.yml templates: do not edit by hand -->
- **[CBAM declaration preparation checklist](../downloads/cbam-declaration-checklist.docx)** (Word): Step-by-step checks before submitting the annual CBAM declaration and surrendering certificates by 30 September.
<!-- end generated templates -->

- The table above can be produced with
  [`esgcalc.cbam`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/esgcalc/cbam.py).

## Reuse in other reports

The declared embedded emissions are a verified number you can reuse in
Scope 3 category 1 for these goods.

## Sources

Facts come from `data/regulations.yml` (ids `cbam-declaration`,
`cbam-declaration-content`, `cbam-certificates`), last checked
20 November 2026.

- Regulation (EU) 2023/956, Articles 6 and 22, as amended by Regulation
  (EU) 2025/2083:
  [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2025/2083/oj/eng)
- DG TAXUD, CBAM definitive regime:
  [taxation-customs.ec.europa.eu](https://taxation-customs.ec.europa.eu/carbon-border-adjustment-mechanism/cbam-definitive-regime_en)
