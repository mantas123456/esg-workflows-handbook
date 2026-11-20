---
step: "S8"
status: draft
last_checked: 2026-11-20
---

# S8 Base year and recalculation

!!! warning "Not legal advice"
    This page explains base years and recalculation in plain words. The
    GHG Protocol's base-year rules are being revised. The numbers in the
    worked example are made up.

## In one sentence

Choose a base year to compare against, write a policy that says when you
will recalculate it, including a significance threshold you disclose, and
apply the policy every year.

## Who does this and when

The inventory lead with finance, once, after the first full inventory.
Then check the policy every year, when the new inventory is done.

## Inputs

- Your first full, checked inventory ([S4](s4-methods.md)).
- Anything that changed since: acquisitions and sales, new factors or
  methods, errors found.

## Steps

### 1. Choose a base year

Usually the first year with a complete inventory you trust. Targets and
progress are measured against it.

### 2. Write a recalculation policy

The policy says which changes lead to recalculating the base year. Under
the GHG Protocol these are significant:

- **structural changes**: acquisitions, sales, outsourcing or insourcing;
- **changes in calculation method or data source**, such as a new factor;
- **errors found**, including several small ones that are significant
  together.

### 3. Set and disclose a significance threshold

The Scope 3 Standard requires you to set and disclose the threshold that
triggers a recalculation. It can be a number, for example a percentage of
the base-year total, or a description. GHG Protocol guidance gives 2% as
an example.

### 4. Decide how you add up changes

State whether you test each change on its own or all of the year's changes
together. Adding their absolute sizes, so that changes in opposite
directions do not cancel out, is the cautious choice.

### 5. Recalculate when the test says so

Apply the change to the base year as if it had always been there: a
structural change for the **whole** base year, a new method by
recalculating the base year with that method.

### 6. Disclose

Say what changed, by how much, and that the base year was recalculated,
next to the inventory ([S9](s9-reporting.md)).

## Worked example

Gozo Fresh Foods Ltd (fictional) takes **2026** as its base year, at
**5,775.09 tCO2e** of Scope 3 ([S4](s4-methods.md)). Its policy: recalculate
if the absolute changes found in a year add up to **5%** or more of the
base-year total. All numbers are made up.

**Changes found in 2027.**

| Change | Type | Effect on the 2026 base year | tCO2e | Share of base year |
|---|---|---|---|---|
| Acquisition of 100% of Island Cold Store (1 July 2027) | Structural | Its emissions move into Scope 1 and 2: remove category 4 storage (90 t) and category 15 equity (75 t) from the base year | -165.00 | 2.86% |
| New spend factor for other ingredient suppliers | Methodology | Factor source chosen (S5): 1.1 instead of 0.9 kg/EUR, same deflation | +152.54 | 2.64% |
| Commuting survey counted part-time staff as full-time | Error | Car km corrected from 600,000 to 560,000 | -6.80 | 0.12% |
| **Added up (absolute)** | | | **324.34** | **5.62%** |

On its own, no change reaches 5%. Together they reach **5.62%**, so Gozo
**recalculates** the 2026 base year. Applying all three, Scope 3 for 2026
becomes 5,775.09 − 165.00 + 152.54 − 6.80 = **5,755.84 tCO2e**. Gozo also
adds the cold store's emissions to its 2026 Scope 1 and 2 base year, for
the whole year, and discloses all three changes.

Had Gozo let changes in opposite directions cancel out, the net change,
−19.26 tCO2e (0.33%), would have hidden a real change in what the base year
contains.

In Python, with
[`esgcalc`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/esgcalc/scope3.py):

```python
from esgcalc.scope3 import check_recalculation

check = check_recalculation(5775.09, {"acquisition": -165.0, "new factor": 152.54,
                                      "survey error": -6.80}, threshold_share=0.05)
print(round(check.share, 4), check.recalculate)   # 0.0562 True
```

## Common mistakes

- **No written policy.** Then every recalculation looks like an attempt to
  improve the trend.
- **No disclosed threshold.** The Scope 3 Standard requires one.
- **Letting changes cancel out.** An acquisition and a lower factor can
  hide each other.
- **Recalculating only part of the year.** A structural change is applied
  to the whole base year.
- **Updating the current year but not the base year.** Then the comparison
  is between two different methods.

## Evidence to keep

- The recalculation policy, dated and approved.
- For each year: the changes found, their size, the test result and the
  recalculated base year.

File them in the evidence locker (see
[F1](../foundations/evidence-locker.md)).

## Templates and tools

<!-- generated from data/workflows.yml templates: do not edit by hand -->
- **[Base-year recalculation policy](../downloads/recalculation-policy.docx)** (Word): One-page policy stating the base year, which changes trigger a recalculation, the significance threshold you disclose, and how changes are added up.
<!-- end generated templates -->

- [`esgcalc.scope3.check_recalculation`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/esgcalc/scope3.py):
  the test above.

## Reuse in other reports

The same base year and policy apply to Scope 1 and 2, and to any climate
target under ESRS E1 or VSME. See
[F3](../foundations/one-dataset-many-reports.md).

## Sources

Facts come from `data/regulations.yml` (id `ghgp-base-year`), last checked
20 November 2026.

- GHG Protocol Corporate Accounting and Reporting Standard, chapter 5
  (cited, not copied):
  [ghgprotocol.org](https://ghgprotocol.org/sites/default/files/standards/ghg-protocol-revised.pdf)
- GHG Protocol Corporate Value Chain (Scope 3) Standard (cited, not
  copied):
  [ghgprotocol.org](https://ghgprotocol.org/sites/default/files/standards/Corporate-Value-Chain-Accounting-Reporing-Standard_041613_2.pdf)
