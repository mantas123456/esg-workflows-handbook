---
step: "CB2"
status: draft
last_checked: 2026-11-20
---

# CB2 Authorised CBAM declarant status

!!! warning "Not legal advice"
    This page explains the authorisation procedure in plain words. Your
    Member State's competent authority decides on your application. Ask it,
    or your customs broker, if you are not sure.

## In one sentence

Apply in the CBAM registry to become an authorised CBAM declarant, so
that customs will release your CBAM goods once you go over the threshold.

## Who does this and when

The importer, or an indirect customs representative acting for it. Usually
the finance director or the person responsible for customs.

- **When:** as soon as [CB1](cb1-scope-check.md) shows you may go over 50
  tonnes in a year, or before you import **any** hydrogen or electricity.
- **Why early:** the authority has up to 120 days to decide, and longer if
  it asks for more information. Only an authorised CBAM declarant may
  import CBAM goods above the threshold.

## Inputs

- Your EORI number.
- Evidence for the criteria below. The competent authority says what it
  needs; recent annual accounts and a short description of how you will
  run CBAM are a sensible start.
- Access to the CBAM registry for your company.
- Your CB1 import list, so you can show expected volumes.

## Steps

### 1. Decide who applies

Two options:

- **The importer applies itself.** You file the declarations and hold the
  certificates.
- **An indirect customs representative applies.** Agree in writing with
  your broker, before anyone applies, who does what: declarations,
  certificates, supplier data and records.

### 2. Check the criteria

The competent authority checks, in short:

- no serious or repeated breaches of customs, tax or CBAM rules;
- the **financial and operational capacity** to meet CBAM obligations;
- an **EORI number**.

If something in your history may raise questions, explain it in the
application instead of waiting to be asked.

### 3. Apply in the CBAM registry

Submit the application through the CBAM registry. It goes to the
competent authority of the Member State where you are established.

### 4. Answer questions quickly

The authority has **120 calendar days** from receipt to assess the
application. When it asks for more information, it may extend this by
up to **30 days** and must tell you why. The total can never go beyond
**180 days** from receipt. Answer each request fast and completely.

### 5. If a refusal is coming, respond

Before refusing, the authority tells you its reasons and gives you up to
**30 calendar days** to comment. Use that time: correct mistakes and add
missing evidence.

### 6. Start using the status

The decision takes effect when the authority registers it in the CBAM
registry and you are notified there. Then:

- tell your customs broker the same day, so customs declarations for
  CBAM goods name the authorised declarant;
- set up the rest of the track: supplier data ([CB3](cb3-supplier-data.md)),
  certificates ([CB8](cb8-certificates.md)) and the declaration
  ([CB9](cb9-declaration.md)).

!!! info "2026 only: applications made by 31 March 2026"
    An importer or indirect customs representative that applied by
    **31 March 2026** may keep importing CBAM goods in 2026, also above
    the threshold, until the decision on its application takes effect.
    For any later application, you need the status **before** you go over
    the threshold. The recital of the amending regulation says the
    application had to be *submitted* by that date; the implementing act
    says *registered in the CBAM registry*. If your case depends on the
    difference, ask your competent authority.

## Worked example

Melita Metals Ltd (fictional, Malta) found in [CB1](cb1-scope-check.md)
that it went over 50 tonnes in the first quarter of 2026. It applies
itself, without a customs representative. All dates are made up.

| Date | What happens |
|---|---|
| 12 Jan 2026 | Competent authority receives the application |
| 3 Mar 2026 | Authority asks for more information and extends the deadline by 30 days |
| 12 May 2026 | Original deadline (receipt + 120 days), now extended |
| 28 May 2026 | Decision takes effect: status registered in the CBAM registry |
| 11 Jun 2026 | Extended deadline (receipt + 150 days, below the 180-day maximum) |

Because Melita Metals applied before 31 March 2026, it could keep
importing while the application was pending. That covered the **68
tonnes** it imported in the first quarter.

**Comparison.** A company that applies on 15 April 2026 is too late for
the transitional rule. It needs the decision before it goes over 50
tonnes.

The dates in Python, with
[`esgcalc`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/esgcalc/cbam.py):

```python
from datetime import date
from esgcalc.cbam import authorisation_decision_deadline, may_import_pending_decision

received = date(2026, 1, 12)
print(authorisation_decision_deadline(received))                     # 2026-05-12
print(authorisation_decision_deadline(received, extension_days=30))  # 2026-06-11
print(may_import_pending_decision(received, 2026))                   # True
print(may_import_pending_decision(date(2026, 4, 15), 2026))          # False
```

## Common mistakes

- **Applying after the first big order.** The authority may need up to
  180 days. Apply as soon as CB1 shows you may go over the threshold.
- **Leaving the customs broker out.** Customs will not release CBAM goods
  above the threshold without an authorised declarant on the declaration.
  Tell your broker your status on the day it takes effect.
- **Assuming the 2026 rule applies to you.** It covers only applications
  made by 31 March 2026, and only for imports in 2026.
- **Treating hydrogen or electricity like other goods.** The threshold
  never covers them. Any quantity needs an authorised declarant.
- **Slow answers to the authority.** Each request for information can add
  up to 30 days.

## Evidence to keep

- The application as submitted, with the date of receipt from the
  registry.
- Every request from the authority and your answer, with dates.
- The decision and its registration date.
- Any written agreement with an indirect customs representative.

File them in the evidence locker (see
[F1](../foundations/evidence-locker.md)).

## Templates and tools

- [`esgcalc.cbam.authorisation_decision_deadline`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/esgcalc/cbam.py)
  and `may_import_pending_decision`: the deadline and the 2026 rule, as
  shown in the worked example.

## Reuse in other reports

The financial and operational capacity evidence (accounts, process
description, named responsible person) is the same kind of evidence a
bank or customer may ask for in a VSME or supplier questionnaire.

## Sources

Facts come from `data/regulations.yml` (ids `cbam-authorisation`,
`cbam-authorisation-procedure`, `cbam-authorisation-transitional-2026`,
`cbam-threshold`), last checked 20 November 2026.

- Regulation (EU) 2023/956, Articles 5, 17 and 25, consolidated text:
  [EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:02023R0956-20251020)
- Regulation (EU) 2025/2083, which inserted Article 17(7a):
  [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2025/2083/oj/eng)
- Implementing Regulation (EU) 2025/486, Articles 4, 5 and 7:
  [EUR-Lex](https://eur-lex.europa.eu/eli/reg_impl/2025/486/oj/eng)
- Implementing Regulation (EU) 2025/2549, amending 2025/486:
  [EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32025R2549)
