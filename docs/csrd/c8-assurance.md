---
step: "C8"
status: draft
last_checked: 2026-11-21
---

# C8 Assurance readiness

!!! warning "Not legal advice"
    Who may give assurance, and under which standard, depends on your
    national law. The list of what a provider asks for is this handbook's
    practical guide, not a legal requirement.

## In one sentence

Your sustainability statement needs a limited assurance opinion, so make
every reported number traceable to its source files before the provider
arrives.

## Who does this and when

The sustainability lead and finance, with the auditor. Agree the
timetable with the provider early in the reporting year, and do a
trial run on the dry-run figures.

## Inputs

- The draft sustainability statement and the materiality assessment.
- The evidence locker ([F1](../foundations/evidence-locker.md)).
- The gap list ([C7](c7-gap-analysis.md)).

## Steps

### 1. Know what the opinion covers

After Omnibus I, sustainability statements need **limited assurance only**;
the planned move to reasonable assurance was removed. Under Article
34(1)(aa) of Directive 2013/34/EU, the opinion covers:

- compliance with the Directive and the ESRS;
- the process used to identify the reported information (the materiality
  assessment);
- the marking-up (digital tagging) requirement of Article 29d;
- the EU Taxonomy disclosures (Article 8 of Regulation (EU) 2020/852).

The statutory auditor gives it. Member States may also allow a different
auditor or an independent assurance services provider (Article 34(3) and
(4)). The opinion must respect the right of value-chain companies with
1,000 employees or fewer to decline information beyond the cap (Article
34(2a); see [C3](c3-value-chain.md)). The Commission must adopt limited
assurance standards by **1 July 2027**; until then, national standards may
apply. When they are adopted, check the list in step 2 against them.

### 2. Expect what a provider asks for

In practice, a limited-assurance provider will usually ask for:

- the materiality assessment, with scores, reasons and who took part
  ([C2](c2-dma.md));
- for sampled numbers, the calculation and the source files behind them;
- the emission factors with source, version and year
  ([S5](../scope3/s5-emission-factors.md));
- how estimates were made, and their uncertainty ([F2](../foundations/data-quality.md));
- supplier data and whether it was verified ([C3](c3-value-chain.md));
- controls: who prepared and who reviewed each figure;
- any restatement of earlier figures ([S8](../scope3/s8-base-year.md)).

### 3. Build the evidence trail

For each number, keep the source files in the evidence locker, hash them,
and record in the register which files support which figure
([F1](../foundations/evidence-locker.md)).

### 4. Do a trial run

Pick a few figures and trace them from the statement to the source files,
as the provider would.

## Worked example

Mediterranean Logistics Group (fictional) traces four figures from its
2026 dry run ([C5](c5-climate.md)):

| Figure | tCO2e | Source files in the locker | Owner |
|---|---|---|---|
| Scope 1 | 24,900 | Fuel card statements; refrigerant service records | Fleet manager |
| Scope 2 | 16,000 | Electricity invoices for 40,000 MWh; grid factor source | Facilities |
| Category 1: Gozo Fresh Foods | 1,823.5 | Gozo's emailed figure and basis; purchase ledger for Gozo | Purchasing |
| Category 2: Melita Metals | 98.2 | Melita's CBAM data and Installation A verification report; delivery notes for 100 t and 10 t | Projects |

What the trial run showed:

- Scope 1 and 2 trace cleanly to invoices and records.
- **Gozo's figure** is an email. The group asks Gozo for the basis in
  writing (its Scope 3 inventory summary, [S9](../scope3/s9-reporting.md))
  and records that it is not verified.
- **Melita's steel figure** comes with a CBAM verification report
  ([CB6](../cbam/cb6-verification.md)), which helps. The aluminium figure is
  a default value and is marked as an estimate.

## Common mistakes

- **Collecting evidence after the year ends.** Build the trail as data
  comes in.
- **Numbers without a calculation file.** The provider needs to rerun
  each step.
- **Hiding estimates.** Mark them, with the method and uncertainty.
- **Treating supplier data as verified when it is not.** Record its
  status.

## Evidence to keep

- The evidence register linking each figure to its files and hashes.
- Review sign-offs.
- The trial-run notes and fixes.

File them in the evidence locker (see
[F1](../foundations/evidence-locker.md)).

## Templates and tools

- [`scripts/hash_evidence.py`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/scripts/hash_evidence.py)
  and the register in [F1](../foundations/evidence-locker.md).

## Reuse in other reports

The same evidence trail supports a CBAM verification
([CB6](../cbam/cb6-verification.md)) and customer questions on Scope 3
([S9](../scope3/s9-reporting.md)). See
[F3](../foundations/one-dataset-many-reports.md).

## Sources

Facts come from `data/regulations.yml` (ids `csrd-assurance`,
`csrd-assurance-scope`, `eu-taxonomy-article8`), last checked 21 November
2026.

- Directive 2013/34/EU, Article 34, as amended by Directive (EU)
  2026/470, consolidated text of 18 March 2026:
  [EUR-Lex](https://eur-lex.europa.eu/eli/dir/2013/34/2026-03-18/eng)
- Directive (EU) 2022/2464 (CSRD), consolidated:
  [EUR-Lex](https://eur-lex.europa.eu/eli/dir/2022/2464/2026-03-18/eng)
- European Commission, consultation on limited assurance standards:
  [European Commission](https://finance.ec.europa.eu/news/commission-seeks-feedback-limited-assurance-standards-sustainability-reporting-2026-11-12_en)
