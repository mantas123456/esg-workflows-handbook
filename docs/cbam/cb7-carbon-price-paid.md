---
step: "CB7"
status: draft
last_checked: 2026-11-20
---

# CB7 Carbon price paid abroad

!!! warning "New rules, not legal advice"
    The detailed rules were adopted on 16 November 2026 in Implementing
    Regulation (EU) 2026/2498. This page explains the principle and the
    evidence. It does **not** model the conversion into certificates,
    because this handbook has not yet checked the text of that formula.

## In one sentence

If a carbon price was actually paid for your goods' emissions in the
country of production, you may reduce the certificates you surrender, as
long as you have certified evidence.

## Who does this and when

The authorised CBAM declarant, with evidence from the installation
operator. Collect the evidence during the year; claim the reduction in
the annual declaration ([CB9](cb9-declaration.md)).

## Inputs

- Evidence from the operator that a carbon price was **effectively paid**
  for the embedded emissions of your goods.
- Details of any **rebate or compensation** the operator received,
  including free allowances, and the references to that country's law.
- Certification of that evidence by an independent person.

## Steps

### 1. Ask whether a carbon price applies

In your supplier request ([CB3](cb3-supplier-data.md)), ask whether the
installation pays a carbon price, under which law, and on which emissions.

### 2. Net off rebates and free allowances

Only the price **effectively paid** counts. If the operator got a rebate,
compensation or free allowances, that benefit reduces the price that can
be counted.

### 3. Get the evidence certified

The evidence must be certified by a person independent of you and of
the third country's authorities.

| Years | Who may certify |
|---|---|
| 2026 and 2027 | Accredited CBAM verifiers, without extra accreditation |
| From 2028 | A certifier with a specific accreditation from an EU national accreditation body |

### 4. Check carbon credits

If the operator used international carbon credits, only credits
authorised and issued under **Article 6 of the Paris Agreement** count.

### 5. When the price paid cannot be determined

You may instead use **yearly default carbon prices**, which the Commission
may set from 2027 for countries with carbon pricing rules.

### 6. Claim it in the declaration

The reduction lowers the number of certificates to surrender. It can
bring the number down to zero, not below. The conversion follows
Implementing Regulation (EU) 2026/2498.

## Worked example

Installation A's country (fictional) has a carbon price, and the operator
offers certified evidence for 2026. Installation B's data is on default
values and no evidence was offered. All numbers are made up.

**Main example: no reduction claimed.** The conversion rules are new and
not modelled here, so Melita Metals claims no reduction in this example.
From [CB8](cb8-certificates.md): 341.65 tCO2e embedded emissions, minus a
302.25 tCO2e free allocation adjustment, gives **39.4 certificates**.

**What if the evidence is worth 5 certificates?** Suppose that, under the
2026/2498 rules, Installation A's certified evidence converts into a
reduction of **5 certificates** (a made-up figure):

| | No claim | With a reduction of 5 |
|---|---|---|
| Certificates to surrender | 39.4 | 34.4 |
| Cost at an assumed EUR 80.00 per certificate | EUR 3,152.00 | EUR 2,752.00 |

```python
from esgcalc.cbam import certificate_cost, certificates_needed

certs = certificates_needed(341.65, 302.25, carbon_price_paid_tco2e=5)
print(round(certs, 2), certificate_cost(round(certs, 6), 80.00))   # 34.4 2752.00
```

**Carbon price paid above the liability.** A reduction can bring the
certificates to zero but not below: no refund is due through this
calculation ([CB8](cb8-certificates.md)).

## Common mistakes

- **Counting the headline carbon price.** Only the price effectively paid,
  after rebates, compensation and free allowances, counts.
- **No independent certification.** Without it, the evidence cannot be
  used (unless you use default carbon prices).
- **Using credits that do not qualify.** Only Paris Agreement Article 6
  credits count.
- **Throwing away the evidence.** Keep it for four years after the year it
  was certified ([CB10](cb10-records.md)).

## Evidence to keep

- The operator's evidence of the price paid, and of any rebate or
  compensation, with references to the country's law.
- The independent certification.
- Your calculation of the reduction claimed.

File them under `cbam/carbon-price-paid/` (see
[F1](../foundations/evidence-locker.md)).

## Templates and tools

- [`esgcalc.cbam.certificates_needed`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/esgcalc/cbam.py)
  takes the reduction as `carbon_price_paid_tco2e`, already converted into
  certificates. It does not do the 2026/2498 conversion.

## Reuse in other reports

Evidence of carbon prices paid by suppliers is useful context for climate
risk in ESRS E1 and for supplier engagement in Scope 3.

## Sources

Facts come from `data/regulations.yml` (ids `cbam-carbon-price-paid`,
`cbam-carbon-price-records`, `cbam-declaration-content`), last checked
20 November 2026.

- Regulation (EU) 2023/956, Article 9, as amended by Regulation (EU)
  2025/2083: [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2025/2083/oj/eng)
- European Commission, "Commission adopts rules on the recognition of
  carbon prices paid in non-EU countries", 16 November 2026:
  [DG TAXUD](https://taxation-customs.ec.europa.eu/news/cbam-commission-adopts-rules-recognition-carbon-prices-paid-non-eu-countries-2026-11-16_en)
