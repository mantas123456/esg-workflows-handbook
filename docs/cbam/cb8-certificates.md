---
step: "CB8"
status: draft
last_checked: 2026-11-21
---

# CB8 Certificates: buying, holding, surrendering

!!! warning "Not legal advice"
    The free allocation adjustment and the certificate price in the worked
    example are **made up**. Use the real benchmarks (Implementing
    Regulation (EU) 2025/2620) and the published prices.

## In one sentence

Work out how many certificates you owe for the year, buy them on the
central platform, keep at least half of the running total on your
account at each quarter end from 2027, and surrender them by 30
September.

## Who does this and when

The authorised CBAM declarant, usually finance.

| When | What |
|---|---|
| From 1 Feb 2027 | Certificate sales start. Buy certificates for 2026 imports. |
| End of each quarter, from 2027 | Hold at least 50% of the year-to-date requirement. |
| 30 Sep 2027 | Surrender the certificates for 2026 imports with the declaration. |

## Inputs

- Embedded emissions for the year ([CB4](cb4-embedded-emissions.md),
  [CB5](cb5-precursors.md)).
- The free allocation adjustment for your goods.
- Any reduction for carbon price paid ([CB7](cb7-carbon-price-paid.md)).
- The certificate price for the period.

## Steps

### 1. Work out the certificates

One certificate covers **one tonne of CO2e**.

```text
certificates = embedded emissions
               - free allocation adjustment
               - reduction for carbon price paid       (never below zero)
```

The **free allocation adjustment** reflects the free EU ETS allowances
that EU producers of the same goods still receive. It uses a benchmark
per CN code, a correction factor and the **CBAM factor**, which falls
every year:

| Year | 2026 | 2027 | 2028 | 2029 | 2030 | 2031 | 2032 | 2033 | 2034 |
|---|---|---|---|---|---|---|---|---|---|
| CBAM factor | 97.5% | 95% | 90% | 77.5% | 51.5% | 39% | 26.5% | 14% | none |

So the adjustment is large at first and shrinks to nothing by 2034. For
electricity it is zero.

Per good, Implementing Regulation (EU) 2025/2620 sets:

```text
free allocation adjustment (tCO2e) = SEFA (tCO2e per tonne) x tonnes imported
SEFA, with default values = CBAM factor x cross-sectoral correction factor
                            x default CBAM benchmark for the CN code and country
```

With actual data, the benchmark is the one for the production process, and
for complex goods the SEFA of each precursor, times the tonnes of it used per
tonne of goods, is added. The benchmarks are in the Annex to 2025/2620.

### 2. Know the price

The price comes from EU ETS auctions, weighted by auction volume:

- **2026 imports:** the quarterly average for the quarter in which the
  goods were imported;
- **from 2027:** a weekly average.

### 3. Buy

Buy on the common central platform from **1 February 2027**.

### 4. Hold enough at each quarter end (from 2027)

At the end of each quarter, your account must hold certificates for at
least **50%** of the embedded emissions in goods imported since 1 January,
taking the free allocation adjustment into account. In the year you first
go over the 50-tonne threshold, this starts at the end of the quarter
**after** the one in which you went over (Article 22(2a)). Measure the
emissions with default values without mark-up, or based on the previous
year's surrendered certificates.

```text
minimum holding = 50% x (embedded emissions YTD - free allocation adjustment YTD)
```

### 5. Surrender

Surrender the certificates with the annual declaration, by **30
September** of the following year ([CB9](cb9-declaration.md)).

### 6. Know the penalty

If you surrender too few, you pay, for each missing certificate, the EU
ETS excess emissions penalty for the year of import, **and** you must
still surrender the missing certificates.

## Worked example

Melita Metals Ltd (fictional) imported 400 t of steel bars and 35 t of
aluminium bars in 2026. The benchmarks, the correction factor and the price
are made up.

**Free allocation per tonne (SEFA).** With made-up benchmarks of 0.60
tCO2e/t for the steel bars and 2.00 tCO2e/t for the aluminium bars, and a
made-up correction factor of 1.0: steel 0.975 x 1.0 x 0.60 = **0.585**;
aluminium 0.975 x 1.0 x 2.00 = **1.95** tCO2e/t in 2026, and 0.57 and 1.90
in 2027, when the CBAM factor is 95%.

**Certificates for 2026 imports.**

| | Installation A (steel) | Installation B (aluminium) | Total |
|---|---|---|---|
| Embedded emissions (tCO2e), from CB4 | 260.8 | 80.85 | 341.65 |
| Free allocation adjustment per tonne (made up) | 0.585 | 1.95 | |
| Free allocation adjustment (tCO2e) | 234.0 | 68.25 | 302.25 |
| Reduction for carbon price paid (CB7) | | | 0 |
| **Certificates to surrender** | | | **39.4** |

341.65 − 302.25 − 0 = **39.4 certificates**. At an assumed **EUR 80.00**
per certificate, the cost is 39.4 × 80.00 = **EUR 3,152.00**. Melita
Metals buys them after 1 February 2027 and surrenders them by 30
September 2027.

**Quarterly holding in 2027.** Suppose Melita Metals imports the same
tonnes per quarter in 2027 as in 2026. It measures year-to-date emissions
with the base default values from CB4 (1.60 tCO2e/t for the steel bars,
2.10 tCO2e/t for the aluminium bars, no mark-up). The 2027 adjustment per
tonne (made up) is 0.57 for steel and 1.90 for aluminium, lower than in
2026 because the CBAM factor falls.

| End of | Steel YTD (t) | Aluminium YTD (t) | Emissions YTD (tCO2e) | Adjustment YTD (tCO2e) | Minimum holding |
|---|---|---|---|---|---|
| Q1 2027 | 60 | 8 | 112.8 | 49.4 | 31.7 |
| Q2 2027 | 170 | 17 | 307.7 | 129.2 | 89.25 |
| Q3 2027 | 280 | 27 | 504.7 | 210.9 | 146.9 |
| Q4 2027 | 400 | 35 | 713.5 | 294.5 | 209.5 |

For example, Q1: 60 × 1.60 + 8 × 2.10 = 112.8; 60 × 0.57 + 8 × 1.90 =
49.4; 50% × (112.8 − 49.4) = **31.7 certificates**.

In Python, with
[`esgcalc`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/esgcalc/cbam.py):

```python
from esgcalc.cbam import certificate_cost, certificates_needed, quarterly_holding

certs = certificates_needed(341.65, free_allocation_adjustment_tco2e=302.25)
print(round(certs, 2), certificate_cost(round(certs, 6), 80.00))   # 39.4 3152.00
print(round(quarterly_holding(112.8, 2027, 49.4), 2))              # 31.7
```

The figures are shown as calculated. Article 22 of the CBAM Regulation
sets no rounding rule for the number of certificates; check the CBAM
registry's instructions.

## Common mistakes

- **Waiting until September to buy.** From 2027 you must hold 50% at each
  quarter end.
- **Ignoring the free allocation adjustment.** In the early years it
  removes most of the cost; it shrinks every year as the CBAM factor
  falls.
- **Using the wrong price period.** For 2026 imports, the price is the
  average for the quarter of import.
- **Thinking the penalty settles the debt.** You still surrender the
  missing certificates.
- **Using marked-up default values for the quarterly holding.** The
  holding uses default values without mark-up.

## Evidence to keep

- The calculation of certificates per year, with the adjustment and any
  carbon-price reduction.
- Purchase confirmations from the central platform.
- Your account balance at each quarter end.

## Templates and tools

<!-- generated from data/workflows.yml templates: do not edit by hand -->
- **[CBAM embedded emissions workbook](../downloads/cbam-emissions-workbook.xlsx)** (Excel): Embedded emissions per CN code from actual installation data (direct, indirect, precursors) or default values with the yearly mark-up, and the certificates and cost that follow.
<!-- end generated templates -->

- [`esgcalc.cbam`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/esgcalc/cbam.py):
  `certificates_needed`, `certificate_cost` (to the cent) and
  `quarterly_holding`.
- [CBAM calculator](../tools/cbam-calculator.md): certificates, cost and the quarterly holding in your
  browser.

## Reuse in other reports

The CBAM cost is a carbon-related cost for climate risk in ESRS E1, and
a useful number in supplier negotiations.

## Sources

Facts come from `data/regulations.yml` (ids `cbam-certificate-unit`,
`cbam-free-allocation-adjustment`, `cbam-certificates`,
`cbam-quarterly-holding`, `cbam-declaration`, `cbam-penalties`), last
checked 21 November 2026.

- Regulation (EU) 2023/956, Articles 20, 21, 22, 26 and 31, consolidated
  text: [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2023/956/2025-10-20/eng)
- Directive 2003/87/EC, Article 10a(1a) (CBAM factor), as amended by
  Directive (EU) 2023/959:
  [EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX%3A32023L0959)
- Implementing Regulation (EU) 2025/2620 (free allocation adjustment):
  [EUR-Lex](https://eur-lex.europa.eu/eli/reg_impl/2025/2620/oj/eng)
- DG TAXUD, Price of CBAM certificates:
  [taxation-customs.ec.europa.eu](https://taxation-customs.ec.europa.eu/carbon-border-adjustment-mechanism/price-cbam-certificates_en)
