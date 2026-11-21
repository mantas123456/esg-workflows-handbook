---
step: "F4"
status: draft
last_checked: 2026-11-21
---

# F4 Keeping up with changes

!!! warning "Not legal advice"
    This page shows how this handbook tracks rule changes, and how you can
    do the same. A date here is only as good as its last check: always
    open the source.

## In one sentence

Keep every rule you rely on in one list with its source and the date you
last checked it, re-check it on a fixed cycle, and watch the dates you
already know are coming.

## Who does this and when

Whoever owns compliance for each regime: the customs lead for CBAM, the
sustainability lead for Scope 3, VSME and CSRD. Check the list every
quarter, and before every report, declaration or audit.

## Inputs

- A list of the rules you rely on, each with its source and the date you
  last checked it. This handbook keeps its list in
  [`data/regulations.yml`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/data/regulations.yml).
- The official sources: EUR-Lex, the Commission (DG TAXUD for CBAM, DG FISMA
  for CSRD), EFRAG, the GHG Protocol, and your national authority.

## Steps

### 1. Keep one list of facts

One row per rule you rely on: what it says in your words, the regulation
and article, the source link, and the date you last checked it. Pages,
templates and tools then point to the list instead of repeating rules.

### 2. Re-check on a fixed cycle

This handbook re-checks a fact within **90 days**, and treats a fact not
checked for **180 days** as unusable. The script
[`scripts/check_regulations.py`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/scripts/check_regulations.py)
runs on every change:

- 90 days or more: a warning;
- 180 days or more: the build fails, so the site stops publishing it.

Change the date only after you have re-read the source. If two sources
disagree, do not choose: write down both and ask.

### 3. Watch the dates you already know

Some changes are announced in advance. Put them in your calendar with the
fact they will change.

### 4. When something changes

1. Update the fact, its source and the date.
2. Find every page, template and tool that uses it (search for its id).
3. Rerun the checks and the worked examples.
4. Note the change in the [changelog](../changelog.md).

### 5. Tell us about errors

Found an error or an outdated rule in this handbook? Use the
[issue form](https://github.com/mantas123456/esg-workflows-handbook/issues/new?template=report-error.yml)
on GitHub. Please link the official source.

## Worked example

**The watch list** on 21 November 2026, from the handbook's facts:

| When | What changes | Fact |
|---|---|---|
| End of 2026 | EFRAG plans to hand over the final ESRS XBRL taxonomy | `esrs-digital-tagging` |
| 1 Jan 2027 | GHG Protocol Land Sector and Removals Standard takes effect | `ghgp-land-sector` |
| 1 Jan 2027 | Revised ESRS mandatory for financial years starting from this date | `esrs-simplified` |
| 19 Mar 2027 | Deadline for Member States to transpose the CSRD changes of Omnibus I | `omnibus-i-transposition` |
| Q2 2027 | GHG Protocol: draft revised Scope 3 Standard for public consultation (estimate) | `ghgp-scope3-standard` |
| 1 Jul 2027 | Deadline for the Commission to adopt limited assurance standards | `csrd-assurance` |
| 30 Sep 2027 | First CBAM annual declaration and surrender, for 2026 imports | `cbam-declaration` |
| Dec 2027 | Latest date to revise the CBAM default values and mark-ups | `cbam-default-values` |

**The 90- and 180-day checks.** Of the 59 facts, 39 were last checked on
20 November 2026 and 20 on 21 November 2026 (re-read in the Official
Journal for 1.0):

| Run on | Days since the oldest check | Result |
|---|---|---|
| 21 Nov 2026 | 1 | 59 facts ok |
| 18 Feb 2027 | 90 | 39 warnings, 20 ok, build passes |
| 19 May 2027 | 180 | 39 over 180 days, 20 warnings, **build fails** |

So the next full re-check is due by **18 February 2027**, before the
Omnibus I transposition deadline.

```
python scripts/check_regulations.py --today 2027-02-18
# 59 facts checked on 2027-02-18: 0 over 180 days, 39 over 90 days
```

## Common mistakes

- **Updating the date without re-reading the source.** The date means "a
  person read the source on this day".
- **Copying a rule into many places.** Then one change means many edits,
  and some are missed. Point to one list.
- **Relying on summaries.** Law firms and consultants are useful for
  finding changes; the Official Journal is what counts.
- **Forgetting national law.** EU directives apply through national
  transposition, on national dates.

## Evidence to keep

- The fact list with its history (this handbook uses git).
- For each change: the source, the date and what you updated.

File them in the evidence locker (see
[F1](evidence-locker.md)).

## Templates and tools

- [`scripts/check_regulations.py`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/scripts/check_regulations.py):
  warns at 90 days, fails at 180.
- [`scripts/check_links.py`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/scripts/check_links.py):
  checks the external links (run by hand; some official sites refuse
  automated checks, so open those yourself).
- [T2 Regulation timeline](../start-here/timeline.md): the main dates of
  all four regimes.

## Reuse in other reports

One fact list serves every regime: a change to the value-chain cap, for
example, affects C3, V5 and S7 at once. See
[F3](one-dataset-many-reports.md).

## Sources

Facts come from `data/regulations.yml` (ids `esrs-digital-tagging`,
`ghgp-land-sector`, `esrs-simplified`, `omnibus-i-transposition`,
`ghgp-scope3-standard`, `csrd-assurance`, `cbam-declaration`,
`cbam-default-values`), last checked 20 and 21 November 2026.

- EUR-Lex, the Official Journal of the EU:
  [EUR-Lex](https://eur-lex.europa.eu/oj/direct-access.html)
- European Commission, CBAM:
  [DG TAXUD](https://taxation-customs.ec.europa.eu/carbon-border-adjustment-mechanism_en)
- European Commission, corporate sustainability reporting:
  [DG FISMA](https://finance.ec.europa.eu/capital-markets-union-and-financial-markets/company-reporting-and-auditing/company-reporting/corporate-sustainability-reporting_en)
- GHG Protocol standards and updates:
  [GHG Protocol](https://ghgprotocol.org/standards-and-guidance)
