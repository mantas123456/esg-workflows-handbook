---
step: "CB6"
status: draft
last_checked: 2026-11-20
---

# CB6 Verification of emissions data

!!! warning "Not legal advice"
    This page explains what to check in a verification report. The
    verification rules are in Implementing Regulation (EU) 2025/2546.

## In one sentence

Before you use an installation's actual emissions data, make sure an
accredited verifier has checked it and that the report covers your goods
and the right year.

## Who does this and when

The person preparing the CBAM declaration, when the operator sends its
data ([CB3](cb3-supplier-data.md)) and again before the declaration
([CB9](cb9-declaration.md)). The operator sends you verified data; your
job is to check the verification before you rely on it.

## Inputs

- The operator's emissions data and the verifier's final report.
- The verifier's accreditation details.

## Steps

### 1. Check the verifier is accredited for CBAM

The verifier must be accredited for CBAM by a **national accreditation
body in the EU**. The accreditation must be valid **on the day the
verifier issues the final verification report**.

### 2. Check the report covers your goods

The report should name the installation and cover the CN codes you
imported from it.

### 3. Check the period

The operator's reporting period is the **calendar year of production**.
For a precursor with actual data, the report must cover the period the
precursor was produced ([CB5](cb5-precursors.md)).

### 4. Match the numbers

The specific embedded emissions in the report should be the ones the
operator sent you and the ones you use in [CB4](cb4-embedded-emissions.md).

### 5. Keep a copy for the declaration

Where you use actual values, the CBAM declaration includes copies of the
verification reports ([CB9](cb9-declaration.md)).

### 6. If something is missing

Without a valid verification, you cannot use the actual data. Use the
default values for those goods (see [CB4](cb4-embedded-emissions.md)) and
ask the operator to fix it for next year.

## Worked example

Melita Metals Ltd (fictional) uses actual data from Installation A and
default values for Installation B ([CB3](cb3-supplier-data.md)). All names
and dates are made up.

| Check | Installation A's report | OK? |
|---|---|---|
| Verifier | Verifier V (fictional), accredited for CBAM by an EU national accreditation body | Yes |
| Accreditation valid when report issued | Report issued 15 Mar 2027; accreditation valid until 30 Jun 2029 | Yes |
| Goods covered | Steel bars CN 7214 20 00 and 7214 99 10 | Yes |
| Period | Production year 2026 | Yes |
| Numbers match | 0.652 tCO2e/t, as used in CB4 | Yes |

Melita Metals can use Installation A's actual data. That covers **260.8
of its 341.65 tCO2e**, or **76.3%** of its 2026 embedded emissions. The
other 80.85 tCO2e (Installation B) use default values.

## Common mistakes

- **Accepting a report from a verifier without CBAM accreditation.**
  Check the accreditation, not just the company name.
- **Checking accreditation today instead of on the report date.** It must
  have been valid when the final report was issued.
- **A report for the wrong year or the wrong plant.** The period is the
  calendar year of production, for the installation that made your goods.
- **Numbers that differ between the data sheet and the report.** Use the
  verified figure.
- **Forgetting precursors.** Precursor actual data needs its own valid
  verification.

## Evidence to keep

- The final verification report for each installation using actual
  values.
- A record of your checks (a copy of the table above) with the date.
- Proof of the verifier's accreditation at the report date.

File them under `cbam/suppliers/` in the evidence locker (see
[F1](../foundations/evidence-locker.md)).

## Templates and tools

<!-- generated from data/workflows.yml templates: do not edit by hand -->
- **[CBAM declaration preparation checklist](../downloads/cbam-declaration-checklist.docx)** (Word): Step-by-step checks before submitting the annual CBAM declaration and surrendering certificates by 30 September.
<!-- end generated templates -->

- The table in the worked example works as a quick checklist for one
  report.

## Reuse in other reports

A verified emissions figure is high-quality supplier data for Scope 3.
Note "verified" in your data-quality scoring.

## Sources

Facts come from `data/regulations.yml` (ids `cbam-verification`,
`cbam-actual-or-default`, `cbam-declaration-content`), last checked
20 November 2026.

- Regulation (EU) 2023/956, Articles 8 and 18, consolidated text:
  [EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:02023R0956-20251020)
- DG TAXUD, CBAM verification:
  [taxation-customs.ec.europa.eu](https://taxation-customs.ec.europa.eu/carbon-border-adjustment-mechanism/cbam-verification_en)
- European Commission, Guidance on CBAM verification and accreditation:
  [DG TAXUD](https://taxation-customs.ec.europa.eu/document/download/030fe146-38e5-46b8-82b5-5f72da089a7b_en?filename=GUIDANCE+ON+CBAM+VERIFICATION+AND+ACCREDITATION+FOR+VERIFIERS+AND+NATIONAL+ACCREDITATION+BODIES.pdf)
