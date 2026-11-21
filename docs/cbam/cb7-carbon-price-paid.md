---
step: "CB7"
status: draft
last_checked: 2026-11-21
---

# CB7 Carbon price paid abroad

!!! warning "New rules, not legal advice"
    The detailed rules are in Implementing Regulation (EU) 2026/2498
    (adopted 5 November 2026, published 16 November 2026). This page
    explains them in plain words. The Commission's electronic templates
    for the reports are in the CBAM registry; follow them, not this page,
    when you fill them in.

## In one sentence

If a carbon price was actually paid for your goods' emissions in the
country of production, you may reduce the certificates you surrender, as
long as the operator's carbon price report is certified.

## Who does this and when

- The **installation operator** works out the price paid per tonne of
  each good and writes the **carbon price report**, for the same period
  as its verified emissions report ([CB6](cb6-verification.md)).
- An **independent person** certifies that report.
- The **authorised CBAM declarant** (you) asks for the report in the
  supplier request ([CB3](cb3-supplier-data.md)), checks it, and claims the
  reduction in the annual declaration ([CB9](cb9-declaration.md)).

## Inputs

- The operator's **certified carbon price report** for the installation
  and year your goods were made.
- The installation's **satisfactory verification report** for the same
  period ([CB6](cb6-verification.md)).
- For complex goods: the precursor installations' certification reports,
  if a carbon price was paid there too.
- The Commission's yearly average **exchange rate** and the yearly
  **reference price** of CBAM certificates.

## Steps

### 1. Ask whether a carbon price applies

In your supplier request ([CB3](cb3-supplier-data.md)), ask whether the
installation pays a carbon price, under which law, and on which emissions.
A price can come from an emissions trading system, a carbon tax on the
installation's emissions, or a carbon tax on the fuels it burns.

### 2. The operator works out the price per tonne of emissions

For each carbon price mechanism, the operator finds one price per tonne
of the emissions the mechanism covers (Annex I, section 3):

| Mechanism | Price per tonne of covered emissions |
|---|---|
| Emissions trading system | Weighted average auction price of the period, as published by the authority (or, if none, the published average market price). Or: the average cost of the operator's own units still in its registry account at the end of the period |
| Carbon tax on emissions | The tax rate actually applied, including any reduced rate; a time-weighted average if the rate changed |
| Carbon tax on fuels | Tax paid per unit of fuel, divided by the fuel's emission factor (national, then UNFCCC inventory, then IPCC default) |

If part of the obligation was met with **carbon credits**, the price is a
weighted average of the options used. **International credits** (Paris
Agreement Article 6.2 and 6.4) count for at most **10%** of the covered
emissions of that mechanism; above that they count at zero. Credits the
operator did not buy count at zero unless their market price is
evidenced. A **refund in money** is turned into a refund per tonne and
taken off the price.

### 3. The operator attributes emissions and rebates to each good

- The covered emissions of the period are attributed to each good per
  tonne, **in the same way as embedded emissions**
  ([CB4](cb4-embedded-emissions.md), [CB5](cb5-precursors.md)).
- For goods where CBAM counts only direct emissions, such as iron and
  steel, **indirect emissions are not attributed**.
- **Rebated emissions** are attributed the same way: emissions covered by
  free allowances, below a baseline or threshold, or exempted for another
  reason (Annex I, section 5; Article 9).

If the operator is entitled to a rebate but cannot show how much, it gets
**no deduction at all**. A rebate that was officially set but not yet
received still counts. Some subsidies paid from carbon price revenues to
cut emissions do not count as rebates, if all the conditions of Article
9(3) are met.

### 4. The operator calculates the price paid per tonne of good

```text
price paid (EUR per t of good) = (covered emissions per t - rebated emissions per t)
                                 x (price per tCO2e - refund per tCO2e)
                                 x yearly average exchange rate (EUR per local unit)
```

Add the results for each mechanism. For precursors made in another
installation, add the price shown in **that** installation's
certification report. Without such a report, nothing is added for that
precursor (unless a default carbon price is used).

### 5. The operator writes the carbon price report

The report is in English, on the Commission's electronic template in the
CBAM registry. If the operator is registered there, it sends the report to
the independent person through the registry (Article 8). It contains at
least (Annex III):

- the installation and operator ids in the CBAM registry, the report id,
  version and period, and the ids of the verified emissions report and
  its verification report;
- for each mechanism, direct and indirect separately: its name and law,
  the price per tonne and how it was found, the covered emissions, any
  emission factors, credits used, units surrendered, and how the period
  and the attribution to goods were handled;
- per tonne of each good: the covered and rebated emissions, the price
  paid in local currency, the exchange rate and its year, and the price
  paid in euro;
- for precursors made elsewhere: the precursor installation's
  certification report id and the price per tonne, or the default price
  used;
- the total price paid in euro per tonne of good across all mechanisms.

### 6. Get the report certified

The independent person must be independent of you (Article 9 of the CBAM
Regulation), and of the operator, the EU competent authority, the
Commission and the third country's carbon pricing authorities (Article
10(2) of 2026/2498). They rely on the installation's
verification report only if it is **satisfactory** and covers the same
period (Article 15). The certification ends in one opinion:
**satisfactory** or **unsatisfactory** (Article 19). From 1 February 2027
the certification report is issued in the CBAM registry.

| Years | Who may certify |
|---|---|
| 2026 and 2027 | Accredited CBAM verifiers, without extra accreditation |
| From 2028 | A certifier with a specific accreditation from an EU national accreditation body |

### 7. When the price paid cannot be determined

You may instead use **yearly default carbon prices**, which the Commission
may set from 2027 for countries with carbon pricing rules.

### 8. Claim it in the declaration

For each good, you turn the certified price into fewer certificates:

```text
reduction (certificates) = price paid (EUR per tonne of good)
                           / yearly reference price of CBAM certificates (EUR per tCO2e)
                           x tonnes of the good declared
```

The reference price is the average of the published certificate prices for
the year of import, rounded to the cent. With a default carbon price
instead, the price per tonne of good is the default price x the specific
embedded emissions. The reduction lowers the number of certificates to
surrender. It can bring the number down to zero, not below.

## Worked example

Installation A's country (fictional) has an emissions trading system.
Installation B's data is on default values and no evidence was offered.
All numbers are made up, including the currency (the crown).

**Main example: no reduction claimed.** The certified report for 2026
was not ready when Melita Metals prepared its figures, so the main
example claims no reduction.
From [CB8](cb8-certificates.md): 341.65 tCO2e embedded emissions, minus a
302.25 tCO2e free allocation adjustment, gives **39.4 certificates**.

**What if the report is certified?** Installation A's carbon price report
for 2026 shows:

| Item | Value |
|---|---|
| Covered emissions (arc furnace 30,600 + rolling mill 8,000) | 38,600 tCO2e |
| Of which covered by free allowances (rebated) | 28,600 tCO2e |
| Compliance units surrendered | 38,600 |
| Weighted average auction price, 2026 | 50 crowns per tCO2e |
| Monetary refund | none |
| Exchange rate (Commission yearly average) | EUR 0.20 per crown |
| Bars produced (all covered emissions relate to them) | 100,000 t |

Per tonne of bars:

```text
covered emissions  = 38,600 / 100,000 = 0.386 tCO2e
rebated emissions  = 28,600 / 100,000 = 0.286 tCO2e
price paid         = (0.386 - 0.286) x (50 - 0) x 0.20 = EUR 1.00 per tonne of bars
```

The pig iron from Installation C ([CB5](cb5-precursors.md)) adds 0.266
tCO2e per tonne of bars to the embedded emissions. Installation C has no
certification report, so **no carbon price is counted for it**. Check:
0.386 + 0.266 = 0.652 tCO2e per tonne, the bars' specific embedded
emissions from [CB4](cb4-embedded-emissions.md).

With a reference price for 2026 of **EUR 80.00** (made up), for the 400 t
of bars Melita imported from Installation A:

```text
reduction = 1.00 / 80.00 x 400 t = 5 certificates
```

| | No claim | With a reduction of 5 |
|---|---|---|
| Certificates to surrender | 39.4 | 34.4 |
| Cost at an assumed EUR 80.00 per certificate | EUR 3,152.00 | EUR 2,752.00 |

```python
from esgcalc.cbam import (carbon_price_reduction, certificate_cost,
                          certificates_needed, effective_carbon_price_per_t)

price = effective_carbon_price_per_t(0.386, 0.286, price_per_tco2e=50, eur_per_local_unit=0.20)
reduction = carbon_price_reduction(price, 80.00, 400)                # 5 certificates
certs = certificates_needed(341.65, 302.25, carbon_price_paid_tco2e=reduction)
print(round(price, 2), round(certs, 2), certificate_cost(round(certs, 6), 80.00))   # 1.0 34.4 2752.00
```

**Carbon price paid above the liability.** A reduction can bring the
certificates to zero but not below: no refund is due through this
calculation ([CB8](cb8-certificates.md)).

## Common mistakes

- **Counting the headline carbon price.** Only the price effectively paid,
  after rebates, compensation and free allowances, counts.
- **Counting emissions twice.** Free allowances reduce the emissions on
  which a price was paid; they are not a second deduction from the price.
- **Claiming a price on a precursor made elsewhere** without that
  installation's own certification report.
- **Mixing periods.** The carbon price report covers the same period as
  the verified emissions report.
- **No independent certification, or an unsatisfactory one.** Then the
  report cannot be used (unless you use default carbon prices).
- **Too many international credits.** Above 10% of the covered emissions
  they count at zero.
- **Throwing away the evidence.** Keep it for four years after the year it
  was certified ([CB10](cb10-records.md)).

## Evidence to keep

- The operator's carbon price report and its certification report, with
  their ids in the CBAM registry.
- The verification report the certification relied on.
- The exchange rate and reference price used, and your calculation of the
  reduction claimed.

File them under `cbam/carbon-price-paid/` (see
[F1](../foundations/evidence-locker.md)).

## Templates and tools

- [`esgcalc.cbam.effective_carbon_price_per_t`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/esgcalc/cbam.py):
  the price paid per tonne of good for one mechanism (Annex I, equations 6,
  12 and 15).
- [`esgcalc.cbam.carbon_price_reduction`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/esgcalc/cbam.py):
  the Article 7(1) conversion; pass the result to `certificates_needed` as
  `carbon_price_paid_tco2e`.

## Reuse in other reports

Evidence of carbon prices paid by suppliers is useful context for climate
risk in ESRS E1 and for supplier engagement in Scope 3.

## Sources

Facts come from `data/regulations.yml` (ids `cbam-carbon-price-paid`,
`cbam-carbon-price-report`, `cbam-carbon-price-records`,
`cbam-declaration-content`), last checked 21 November 2026.

- Implementing Regulation (EU) 2026/2498, Articles 3, 6 to 9, 15 and 19,
  Annexes I and III:
  [EUR-Lex](https://eur-lex.europa.eu/eli/reg_impl/2026/2498/oj/eng)
- Regulation (EU) 2023/956, Article 9, as amended by Regulation (EU)
  2025/2083: [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2025/2083/oj/eng)
- European Commission, "Commission adopts rules on the recognition of
  carbon prices paid in non-EU countries", 16 November 2026:
  [DG TAXUD](https://taxation-customs.ec.europa.eu/news/cbam-commission-adopts-rules-recognition-carbon-prices-paid-non-eu-countries-2026-11-16_en)
