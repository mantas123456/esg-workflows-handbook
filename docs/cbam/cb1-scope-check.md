---
step: "CB1"
status: draft
last_checked: 2026-11-21
---

# CB1 Scope check: CN codes and the 50 t threshold

!!! warning "Not legal advice"
    This page shows the CBAM scope test and its source. It does not decide
    whether CBAM applies to you. Check your own codes and totals, and ask
    your customs broker or competent authority if you are not sure.

!!! note "What the CBAM track does not cover yet"
    Imports of electricity (beyond the threshold rule), customs special
    procedures such as inward processing, the repurchase and cancellation
    of unused certificates, and the exact formulas for the free allocation
    adjustment and for converting a carbon price paid abroad into fewer
    certificates. Check these with your customs broker and the official
    texts. They are planned for later releases.

## In one sentence

Find out whether your imports are CBAM goods, add up their net mass for
the year, and compare the total with the 50-tonne threshold.

## Who does this and when

The importer, usually finance or purchasing, together with the customs
broker who files the customs declarations.

- **Before the first import of the year.** If you expect to go over the
  threshold, you need authorised CBAM declarant status first (see
  [CB2](cb2-authorisation.md)).
- **After every shipment.** Keep a running total. Once the year goes over
  50 tonnes, CBAM covers all goods imported that year, including those
  imported before.

## Inputs

- The 8-digit CN code of every product you import from outside the EU.
  Your customs declarations show it.
- The net mass in tonnes of each import, from the customs declaration.
- [Annex I to the CBAM Regulation](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:02023R0956-20251020),
  the list of CBAM goods.

## Steps

### 1. List your imports by CN code

Export one year of import lines from your customs broker or ERP: date,
CN code, description, net mass, country of origin. One row per customs
declaration line.

### 2. Mark the CBAM goods

Compare each CN code with Annex I. CBAM goods fall in six sectors:
cement, electricity, fertilisers, iron and steel, aluminium and hydrogen.

- Where Annex I lists a code shorter than 8 digits, **every** CN code that
  starts with it is covered.
- Iron and steel cover **chapter 72**, except listed ferro-alloys under
  7202 (ferro-silicon, ferro-silico-manganese, ferro-silico-chromium,
  ferro-molybdenum, ferro-tungsten, ferro-titanium, ferro-vanadium,
  ferro-niobium and other ferro-alloys under 7202 99) and **heading 7204,
  ferrous waste and scrap**. They also cover agglomerated iron ores
  (2601 12 00) and listed chapter 73 goods.
- Aluminium covers the headings **7601 to 7616** that Annex I lists.
- Electricity is CN 2716 00 00 and hydrogen is CN 2804 10 00.

If a code is not in Annex I, that line is not a CBAM good. Leave it out
of the total.

**Check the origin too.** CBAM does not apply to goods **originating**
in Iceland, Liechtenstein, Norway or Switzerland, or in the territories
of Büsingen, Heligoland, Livigno, Ceuta and Melilla (Annex III). Leave
those lines out as well. The Commission can change this list.

### 3. Add up the net mass

Add the net mass of **all** CBAM goods for the calendar year, across all
CN codes and all countries. Do not test each code on its own.

**Leave out hydrogen and electricity.** The threshold does not cover them.
If you import any quantity of hydrogen or electricity, you need
authorised CBAM declarant status for it.

### 4. Compare with 50 tonnes

| Year's total net mass | What the test shows |
|---|---|
| 50 tonnes **or less** | Exemption test met. Declare the exemption in each customs declaration. |
| **More than** 50 tonnes | Exemption test not met. CBAM covers **all** CBAM goods imported that year. |

Exactly 50 tonnes is still within the exemption: the rule is "does not
exceed".

### 5. Keep the running total

Update the total after every shipment. Plan ahead: an importer without
authorisation that goes over the threshold faces a penalty on the
embedded emissions of **all** its imports that year. The authority may
reduce it if the threshold was exceeded by no more than 10%.

## Worked example

Melita Metals Ltd is a fictional importer in Malta. It buys steel
reinforcing bars from **Installation A**, a steel mill outside the EU, and
aluminium bars from **Installation B**, an aluminium plant outside the EU.
All numbers are made up.

**Step 1 and 2: imports in 2026 by CN code.** All four codes start with
72 or 7604, so they are in Annex I.

| CN code | Goods | Installation | Net mass 2026 (t) |
|---|---|---|---|
| 7214 20 00 | Steel bars with ribs (rebar) | A | 250 |
| 7214 99 10 | Other steel bars for concrete reinforcement | A | 150 |
| 7604 29 10 | Aluminium alloy bars and rods | B | 35 |
| **Total** | | | **435** |

**Step 3 and 4: the threshold test.** 435 tonnes is more than 50 tonnes,
so the exemption test is not met. No hydrogen or electricity is
imported.

**Step 5: the running total.** The table shows when the year went over
the threshold.

| Quarter | Imported in quarter (t) | Running total (t) | Above 50 t? |
|---|---|---|---|
| Q1 | 68 | 68 | Yes |
| Q2 | 119 | 187 | Yes |
| Q3 | 120 | 307 | Yes |
| Q4 | 128 | 435 | Yes |

Melita Metals went over 50 tonnes in the first quarter. So it needs
authorised CBAM declarant status, and CBAM covers all 435 tonnes. For
2026 there is a transitional rule for applications made by 31 March; see
[CB2](cb2-authorisation.md).

The same test in Python, with the
[`esgcalc`](https://github.com/mantas123456/esg-workflows-handbook/tree/main/esgcalc)
package that recomputes this example on every build:

```python
from esgcalc.cbam import threshold_check

result = threshold_check([
    ("7214 20 00", 250),
    ("7214 99 10", 150),
    ("7604 29 10", 35),
])
print(result.total_mass_t, result.above_threshold)   # 435.0 True
```

## Common mistakes

- **Testing each CN code on its own.** The threshold is one total for all
  CBAM goods in the year.
- **Counting only the first months.** The test is for the whole calendar
  year. One large order late in the year can push you over, and then all
  of that year's imports count.
- **Treating 50 tonnes as "over".** Exactly 50 tonnes is within the
  exemption.
- **Forgetting the customs declaration.** Even when you are within the
  exemption, you declare it in each customs declaration.
- **Assuming hydrogen or electricity fall under the threshold.** They do
  not. Any quantity needs authorisation.
- **Counting goods from Norway, Switzerland, Iceland or Liechtenstein.**
  Goods originating there are outside CBAM. Check the origin on the
  customs declaration, not the supplier's address.
- **Counting scrap.** Ferrous waste and scrap (7204) is not a CBAM good.
- **Using a 4- or 6-digit code from an invoice.** Use the 8-digit CN code
  from the customs declaration, and check it against Annex I.

## Evidence to keep

- The customs declarations behind every import line, with CN code and net
  mass.
- Your yearly import list, with the CBAM goods marked and the total.
- The running total by date, so you can show when the threshold was
  crossed.

File them in the evidence locker and hash them (see
[F1](../foundations/evidence-locker.md)).

## Templates and tools

<!-- generated from data/workflows.yml templates: do not edit by hand -->
- **[CBAM goods register](../downloads/cbam-goods-register.xlsx)** (Excel): One row per import line of CBAM goods, with a running total of net mass against the 50-tonne threshold that calculates itself.
<!-- end generated templates -->

- [`esgcalc.cbam.threshold_check`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/esgcalc/cbam.py):
  adds up the net mass, leaves out hydrogen and electricity, and compares
  the total with the threshold. Runs offline.
- [CBAM calculator](../tools/cbam-calculator.md): the same threshold test in your browser, with embedded
  emissions and certificates. Nothing leaves your browser.

## Reuse in other reports

The same import list by CN code feeds Scope 3 category 1 (average-data
estimates) and category 4 (transport). See
[F3 One dataset, many reports](../foundations/one-dataset-many-reports.md).

## Sources

Facts come from `data/regulations.yml` (ids `cbam-goods`,
`cbam-iron-steel-scope`, `cbam-exempt-origins`, `cbam-threshold`,
`cbam-authorisation`, `cbam-penalties`), last checked 21 November 2026.

- Regulation (EU) 2023/956, Article 2(1) and Annex I (CBAM goods), Article
  2(4) and Annex III (exempt origins), Article
  2a and Annex VII (threshold), Article 26(2a) (penalty), consolidated text:
  [EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:02023R0956-20251020)
- Regulation (EU) 2025/2083, which inserted the threshold:
  [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2025/2083/oj/eng)
