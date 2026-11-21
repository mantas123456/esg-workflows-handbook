---
step: "S1"
status: draft
last_checked: 2026-11-21
---

# S1 Boundary and organisational approach

!!! warning "Not legal advice"
    This page explains the GHG Protocol's boundary choices in plain words.
    If you report under the CSRD, check the boundary rules of ESRS E1 too.

!!! note "What the Scope 3 track does not cover yet"
    Land use, land-use change and removals in the value chain (the GHG
    Protocol Land Sector and Removals Standard, in effect from 1 January
    2027), sector guidance for financial institutions (category 15),
    and the optional indirect use-phase emissions of sold products. They
    are planned for later releases.

## In one sentence

Decide which companies and sites are "yours" (inside the boundary,
Scope 1 and 2) and which are "in your value chain" (outside it, Scope 3),
and stick to that choice every year.

## Who does this and when

The finance lead with whoever prepares the emissions inventory. Do it
**once, before** you collect any Scope 3 data, and review it when the
group changes: a purchase, a sale, a new joint venture.

## Inputs

- The group structure: every company, the share you own, and who runs it.
- For each one, whether you **financially control** it (you direct its
  financial and operating policies to benefit from it) and whether you
  **operate** it (you set its operating policies on site).
- The reporting year, the same as for Scope 1 and 2.
- Who asked for the data, and what they asked for.

## Steps

### 1. List every company and site

Include subsidiaries, joint ventures, associates and sites you lease. For
each, note your equity share, and whether you have financial control and
operational control.

### 2. Choose one consolidation approach

The GHG Protocol Corporate Standard offers three:

| Approach | What is inside the boundary |
|---|---|
| **Equity share** | Each company's emissions in proportion to the share you own, whether or not you control it |
| **Financial control** | 100% of the companies you financially control; none of the others |
| **Operational control** | 100% of the companies whose operating policies you set; none of the others |

Use the **same approach** for all companies and every year.

!!! info "A revision is being discussed"
    A GHG Protocol proposal of December 2025, **not final**, would require
    a control approach, recommend financial control and drop equity share.
    If you choose an approach now, note that equity share may not remain
    available, and check the final text before your next base-year review.

### 3. Put each company in or out

Under a control approach a company is either **fully in** or **fully
out**. Under equity share, each company counts in part.

### 4. Decide what goes to Scope 3

Scope 3 covers emissions in your value chain **outside** the boundary.
A company left out at step 3 does not disappear: if you buy from it or
sell to it, its emissions linked to your business can belong in Scope 3.
[S2](s2-screening.md) shows where.

### 5. Write it down

Record the approach, the list of companies in and out, and the reasons, in
one page. Your customer, your auditor and next year's team will need it.

## Worked example

Gozo Fresh Foods Ltd is a fictional food processor in Malta with **140
employees**. A large supermarket chain that reports under the CSRD asks
it for its Scope 3 emissions for 2026. All companies and numbers are made
up.

**Step 1: the group.** Scope 1 and 2 emissions of each company at 100%,
2026:

| Company | Scope 1 and 2 (tCO2e) | Equity share | Financial control | Operational control |
|---|---|---|---|---|
| Gozo Fresh Foods Ltd (processing plant) | 1,200 | 100% | Yes | Yes |
| Gozo Fresh Logistics Ltd | 400 | 60% | Yes | Yes |
| Harbour Packing Ltd (joint venture run by Gozo Fresh Foods) | 200 | 50% | No | Yes |
| Island Cold Store Ltd (associate) | 300 | 25% | No | No |

**Step 2 and 3: the three approaches compared.**

| Company | Equity share | Financial control | Operational control |
|---|---|---|---|
| Gozo Fresh Foods Ltd (processing plant) | 1,200 | 1,200 | 1,200 |
| Gozo Fresh Logistics Ltd | 240 | 400 | 400 |
| Harbour Packing Ltd (joint venture run by Gozo Fresh Foods) | 100 | 0 | 200 |
| Island Cold Store Ltd (associate) | 75 | 0 | 0 |
| **Scope 1 and 2 inside the boundary** | **1,615** | **1,600** | **1,800** |

For example, equity share: 1,200 + 60% × 400 + 50% × 200 + 25% × 300
= 1,200 + 240 + 100 + 75 = 1,615 tCO2e.

Gozo Fresh Foods runs Harbour Packing day to day, so it chooses
**operational control**: 1,800 tCO2e in Scope 1 and 2.

**Step 4: what goes to Scope 3.** Island Cold Store is outside the
boundary. Gozo Fresh Foods pays it to store chilled goods, so the
emissions of that service can belong in Scope 3. The supplier's own
Scope 1 and 2 are not Gozo Fresh Foods' Scope 1 and 2.

**About the request.** Gozo Fresh Foods has 140 employees, so the
CSRD value-chain cap applies: the supermarket may not *require* more than
the voluntary standard covers (see [T1](../start-here/triage.md)). Gozo
Fresh Foods decides to provide Scope 3 anyway, because it wants to keep
the contract.

In Python, with
[`esgcalc`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/esgcalc/boundary.py):

```python
from esgcalc.boundary import Entity, consolidate

group = [
    Entity("Plant", 1200, 1.00, financial_control=True, operational_control=True),
    Entity("Logistics", 400, 0.60, financial_control=True, operational_control=True),
    Entity("Harbour Packing", 200, 0.50, financial_control=False, operational_control=True),
    Entity("Island Cold Store", 300, 0.25, financial_control=False, operational_control=False),
]
for approach in ("equity_share", "financial_control", "operational_control"):
    print(approach, consolidate(group, approach).tco2e)
# equity_share 1615.0 / financial_control 1600.0 / operational_control 1800.0
```

## Common mistakes

- **Mixing approaches.** Equity share for one company and control for
  another gives a number that means nothing. Choose one.
- **Changing the approach every year.** Then the years cannot be compared.
  If you must change, recalculate the base year (see
  [S8](s8-base-year.md)).
- **Dropping companies outside the boundary.** Their emissions linked to
  your business may still belong in Scope 3.
- **Counting the same emissions twice.** A company inside the boundary is
  Scope 1 and 2. Do not count it again as a supplier in Scope 3.
- **Leaving out leased sites.** Check who operates each site you lease.

## Evidence to keep

- The group structure with equity shares, from the annual accounts.
- The reasons for each control decision (contracts, board minutes,
  management agreements).
- The one-page boundary statement, dated and signed off.

File them in the evidence locker (see
[F1](../foundations/evidence-locker.md)).

## Templates and tools

- [`esgcalc.boundary.consolidate`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/esgcalc/boundary.py):
  compares the three approaches for your group, as above.

## Reuse in other reports

The same boundary statement serves Scope 1 and 2, VSME and ESRS E1. Write
it once. See [F3](../foundations/one-dataset-many-reports.md).

## Sources

Facts come from `data/regulations.yml` (ids `ghgp-organisational-boundary`,
`ghgp-scope3-categories`, `csrd-value-chain-cap`), last checked 20 November
2026.

- GHG Protocol Corporate Accounting and Reporting Standard, organisational
  boundaries (cited, not copied):
  [ghgprotocol.org](https://ghgprotocol.org/corporate-standard)
- GHG Protocol, Corporate Standard revisions, Phase 1 progress update,
  December 2025:
  [ghgprotocol.org](https://ghgprotocol.org/sites/default/files/2025-12/CS-Phase1-ProgressUpdate.pdf)
- GHG Protocol Corporate Value Chain (Scope 3) Standard (cited, not
  copied):
  [ghgprotocol.org](https://ghgprotocol.org/corporate-value-chain-scope-3-standard)
