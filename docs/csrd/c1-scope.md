---
step: "C1"
status: draft
last_checked: 2026-11-20
---

# C1 Am I in scope after Omnibus I?

!!! warning "Not legal advice"
    This page shows the scope test and its sources. It does not tell you
    whether the CSRD applies to your company: your national law, the full
    definitions in Directive 2013/34/EU and your adviser decide that.

## In one sentence

Check both size conditions of the amended CSRD, find your first reporting
year, and check your national law, because Member States are still putting
Omnibus I into their own rules.

## Who does this and when

The finance director or company secretary of a larger EU company, with the
auditor. Do it now, and again each year with the annual accounts, because
the result depends on that year's figures and on national law.

## Inputs

- Your average number of employees and your net turnover, from the annual
  accounts.
- Whether you already reported under the CSRD for financial year 2024.
- The national law of your Member State.

## Steps

### 1. Apply both conditions

After Omnibus I (Directive (EU) 2026/470), the CSRD covers EU companies
with:

- **more than 1,000 employees, and**
- **more than EUR 450 million net turnover.**

**Both** must be met. A company with 1,300 employees but EUR 400 million
turnover is not in scope.

### 2. Find your first reporting year

| Your situation | What it means |
|---|---|
| Never reported, and meet both conditions | First report for **financial year 2027**: the "stop-the-clock" Directive (EU) 2025/794 postponed later waves by two years |
| Reported from financial year 2024 ("wave one"), and meet both conditions | Keep reporting |
| Wave one, but below the new thresholds | Out of scope from 2027; your Member State **may** exempt you for 2025 and 2026 |
| Below the thresholds, never reported | Not in scope; see step 5 |

The revised ESRS apply to financial years from 1 January 2027
([C4](c4-general.md)).

### 3. Check your national law

Member States must transpose the CSRD changes of Omnibus I by **19 March
2027**. Until your country has done so, your national law may still follow
the original CSRD. In **Malta**, for example, the original CSRD was
transposed by the Corporate Sustainability Reporting Regulations, 2026
(Legal Notice 39 of 2026), and Act I of 2026 amended related laws. This
handbook did not find a Maltese law transposing Omnibus I, and could not
confirm when Legal Notice 39 starts to apply: check
[legislation.mt](https://legislation.mt/eli/ln/2026/39/eng) and ask your
adviser.

### 4. Plan backwards from the first year

A first report for financial year 2027 means collecting 2027 data during
2027. The double materiality assessment ([C2](c2-dma.md)) and the data
requests to suppliers ([C3](c3-value-chain.md)) should start in 2026.

### 5. If you are not in scope

You may still be asked for data by customers that are. Companies with on
average 1,000 employees or fewer are protected by the value-chain cap: see
[V5](../vsme/v5-requests.md) and the voluntary standard ([V1](../vsme/v1-modules.md)).

## Worked example

Mediterranean Logistics Group (fictional, Malta) distributes chilled and
frozen food and runs its own warehouses and trucks. It is not listed and
has never reported under the CSRD. Two of its suppliers are the fictional
companies from the other tracks. All numbers are made up.

| Company | Employees | Net turnover (EUR) | More than 1,000 employees? | More than EUR 450 m? | In scope? | First year |
|---|---|---|---|---|---|---|
| Mediterranean Logistics Group | 1,300 | 520,000,000 | Yes | Yes | Yes | 2027 |
| Gozo Fresh Foods Ltd | 140 | 14,000,000 | No | No | No | – |
| Melita Metals Ltd | 60 | 9,000,000 | No | No | No | – |

- **Mediterranean Logistics Group** meets both conditions. It never
  reported, so its first report is for **financial year 2027**. It plans to
  start its double materiality assessment in 2026 ([C2](c2-dma.md)).
- **What if** its turnover were EUR 400 million? The employee condition
  would be met, the turnover condition not: **not in scope**.
- **Gozo Fresh Foods** and **Melita Metals** are not in scope. With 140 and
  60 employees they are protected by the value-chain cap when the group asks
  them for data ([C3](c3-value-chain.md)).
- As a Maltese company, the group also checks how Malta transposes
  Omnibus I before its first report.

In Python, with
[`esgcalc`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/esgcalc/csrd.py):

```python
from esgcalc.csrd import protected_by_value_chain_cap, scope_test

group = scope_test(1300, 520_000_000)
print(group.in_scope, group.first_financial_year)   # True 2027
print(scope_test(1300, 400_000_000).in_scope)       # False
print(protected_by_value_chain_cap(140))            # True
```

## Common mistakes

- **Checking one condition.** Both must be met.
- **Using the old thresholds.** Omnibus I replaced the earlier scope rules
  with these two conditions.
- **Assuming the EU text applies directly.** It applies through your
  national law, which may still be changing.
- **Starting in 2027 for a 2027 report.** The materiality assessment and
  supplier data take months.
- **Forgetting the value chain.** Even out of scope, you will be asked for
  data, and the cap protects smaller companies.

## Evidence to keep

- The employee and turnover figures used, from the annual accounts.
- The national law checked, with the date.
- The board's decision on scope and first year.

File them in the evidence locker (see
[F1](../foundations/evidence-locker.md)).

## Templates and tools

- [`esgcalc.csrd`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/esgcalc/csrd.py):
  `scope_test` and `protected_by_value_chain_cap`.
- [T1 Which regime applies to me?](../start-here/triage.md) for a first
  check across all four regimes.

## Reuse in other reports

The same employee and turnover figures are in your annual accounts, and
the same headcount drives the value-chain cap for your suppliers
([V5](../vsme/v5-requests.md)). See
[F3](../foundations/one-dataset-many-reports.md).

## Sources

Facts come from `data/regulations.yml` (ids `csrd-scope`,
`csrd-wave1-exemption`, `csrd-stop-the-clock`, `omnibus-i-transposition`,
`malta-csrd`, `csrd-value-chain-cap`, `esrs-simplified`), last checked
20 November 2026.

- Directive (EU) 2026/470 (Omnibus I):
  [EUR-Lex](https://eur-lex.europa.eu/eli/dir/2026/470/oj/eng)
- Directive (EU) 2025/794 (stop-the-clock):
  [EUR-Lex](https://eur-lex.europa.eu/eli/dir/2025/794/oj/eng)
- Malta, Legal Notice 39 of 2026:
  [legislation.mt](https://legislation.mt/eli/ln/2026/39/eng)
