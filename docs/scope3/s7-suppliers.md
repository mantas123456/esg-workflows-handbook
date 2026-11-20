---
step: "S7"
status: draft
last_checked: 2026-11-20
---

# S7 Supplier engagement

!!! warning "Not legal advice"
    This page is about asking suppliers for data. The suppliers and numbers
    in the worked example are made up.

## In one sentence

Ask your largest suppliers for their own emissions data in a way they can
answer, check what comes back, and widen the circle each year, starting
where it reduces your uncertainty most.

## Who does this and when

Purchasing, with the inventory lead. Start early in the year
([S3](s3-data-plan.md)), and build the request into the yearly supplier
review so it becomes routine.

## Inputs

- The suppliers to ask first ([S3](s3-data-plan.md)).
- What you bought from each, in tonnes or units, for the year.
- Last year's uncertainty budget ([F2](../foundations/data-quality.md)), to
  see where supplier data helps most.

## Steps

### 1. Ask clearly and once

One short letter per supplier: what you need, for which year, in which
unit, by when, and why. Ask for:

- the supplier's emissions for the year, Scope 1, 2 and, if they have it,
  the upstream part, for the products you buy;
- their total output in the same unit you buy in, so you can work out
  your share ([S4](s4-methods.md));
- what the figure covers (sites, gases, cradle to gate or not) and whether
  it was verified.

If you also buy CBAM goods from them, combine the request with the CBAM
one ([CB3](../cbam/cb3-supplier-data.md)).

### 2. Make it easy

Small suppliers may never have calculated emissions. Offer a simple form,
accept their energy bills and production volumes instead, and calculate
for them if needed. A rough supplier figure is often better than a sector
average.

### 3. Check each answer

| Check | Question |
|---|---|
| Period | Is it the year you asked for? |
| Boundary | Does it cover the sites that make your products? |
| Allocation | Is the total output in the same unit as your purchases? |
| Plausibility | Is the emissions per tonne in a believable range? |
| Verification | Was it verified? If not, score reliability lower ([S6](s6-data-quality.md)). |

### 4. Record and score

Put each answer in the evidence locker, record it in the inventory, and
score it ([S6](s6-data-quality.md)).

### 5. Thank them and share the result

Tell each supplier how their data was used. Suppliers who see the point
answer again next year.

### 6. Widen the circle next year

Use the uncertainty budget to choose the next suppliers: the ones whose
spend-based estimates carry the most uncertainty.

## Worked example

Gozo Fresh Foods Ltd (fictional) asked its top 5 ingredient suppliers
([S3](s3-data-plan.md)) for their 2026 data. All numbers are made up.

**The answers.**

| Supplier | Answered? | Verified? | Used in the inventory (tCO2e) |
|---|---|---|---|
| Maltese Farmers Cooperative | Yes | Yes | 900.00 |
| Sicilian Tomato Co | Yes | Yes | 1,200.00 |
| Gozo Greens Ltd | Yes | No | 500.00 |
| Island Dairy Ltd | Yes | No | 420.00 |
| Mediterranean Oils | Yes | No | 200.00 |

**5 of 5** answered; **2** of the figures were verified. The three
unverified ones carry a wider uncertainty and a lower reliability score
([F2](../foundations/data-quality.md)).

**Next year: who to ask.** Raising the target from 80% to **90%** of
ingredient spend adds one supplier, **Spice Traders Ltd**: the top 6 cover
90.00%.

**What it would do to the uncertainty.** Suppose Spice Traders reports
**150 tCO2e** with ±15%. The spend-based line for the other suppliers then
shrinks from EUR 900,000 to EUR 600,000 (686.44 to 457.63 tCO2e), and
category 1 becomes:

| | Category 1 (tCO2e) | ±95% (tCO2e) | ±95% |
|---|---|---|---|
| 2026, top 5 suppliers | 4,845.00 | 405.23 | 8.36% |
| With Spice Traders as well | 4,766.19 | 315.07 | 6.61% |

One more supplier answering cuts the category's uncertainty by about a
fifth, because it replaces part of the line that dominates the budget.

## Common mistakes

- **A long questionnaire.** Ask for the few numbers you will use.
- **Asking for "your carbon footprint".** Ask for emissions, total output
  and boundary for a given year, so you can allocate.
- **Accepting any number.** Check the period, boundary, unit and
  plausibility.
- **Not saying why.** Suppliers answer when they understand the request and
  see the result.
- **Asking everyone.** Start with the suppliers that matter most, and widen
  each year.

## Evidence to keep

- Each request and answer, with dates.
- Your checks on each answer and the score given.
- The list of suppliers asked, answered and verified, by year.

File them in the evidence locker (see
[F1](../foundations/evidence-locker.md)).

## Templates and tools

<!-- generated from data/workflows.yml templates: do not edit by hand -->
- **[Supplier emissions data request](../downloads/supplier-letter.docx)** (Word): Short letter asking a supplier for its emissions, total output and boundary for one year, so you can allocate your share for Scope 3.
<!-- end generated templates -->

- [`esgcalc.scope3.suppliers_to_cover`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/esgcalc/scope3.py)
  and [`esgcalc.quality.sum_uncertainty`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/esgcalc/quality.py):
  the selection and the what-if above.

## Reuse in other reports

The same supplier data serves CBAM ([CB3](../cbam/cb3-supplier-data.md)),
VSME and customer questionnaires. One request per supplier, used many
times. See [F3](../foundations/one-dataset-many-reports.md).

## Sources

Facts come from `data/regulations.yml` (id `ghgp-scope3-categories`), last
checked 20 November 2026.

- GHG Protocol Corporate Value Chain (Scope 3) Standard (cited, not
  copied):
  [ghgprotocol.org](https://ghgprotocol.org/corporate-value-chain-scope-3-standard)
