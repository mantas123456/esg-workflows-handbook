---
step: "CB10"
status: draft
last_checked: 2026-11-20
---

# CB10 Records and evidence for CBAM

!!! warning "Not legal advice"
    This page shows the CBAM record-keeping rules and a practical way to
    meet them. Check any national rules that apply on top.

## In one sentence

Keep every file behind your CBAM declaration, fingerprinted with SHA-256,
for at least four years after the year of the declaration.

## Who does this and when

The authorised CBAM declarant. File evidence as it arrives during the
year; hash and verify it before the declaration; keep it until the
retention period ends.

## Inputs

- The files from CB1 to CB9: customs declarations, supplier data,
  verification reports, carbon-price evidence, calculations, certificate
  purchases and the declaration.
- The [evidence locker](../foundations/evidence-locker.md) set up in F1.

## Steps

### 1. Know how long to keep what

| What | Keep until | Source |
|---|---|---|
| Information used to calculate embedded emissions, including the verifier's report | End of the **fourth year after** the year the declaration was or should have been submitted | Article 7(6) |
| Evidence of carbon price paid abroad | End of the **fourth year after** the year it was certified | Article 9(3), as amended |

### 2. File everything in the locker

Use the structure from [F1](../foundations/evidence-locker.md): one
folder per year, with `cbam/customs/`, `cbam/suppliers/` and
`cbam/carbon-price-paid/`, plus `calculations/`.

### 3. Hash and verify

Run [`scripts/hash_evidence.py`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/scripts/hash_evidence.py)
to record a SHA-256 hash of every file, and verify it before you submit
the declaration:

```powershell
python scripts/hash_evidence.py build evidence/2026
python scripts/hash_evidence.py verify evidence/2026
```

### 4. Link each declared number to its files

In `reported_values.csv` (see [F1](../foundations/evidence-locker.md)),
add one row for each number in the declaration, pointing to the
calculation and the source files with their hashes.

### 5. Set a deletion date, not a deletion habit

Write the retention end date on the folder. Do not delete anything
before it.

## Worked example

Melita Metals Ltd (fictional) submits its declaration for 2026 imports in
**2027**. The retention period for the emissions records runs to the end
of the fourth year after 2027: **31 December 2031**.

Its 2026 folder:

```text
evidence/2026/
  evidence_register.csv
  reported_values.csv
  cbam/
    customs/              # 11 import lines, 435 t
    suppliers/            # Installation A data + Verifier V report; Installation B: default values used
    carbon-price-paid/    # Installation A evidence (no reduction claimed)
  calculations/           # CB4, CB5 and CB8 working file
  RETENTION.txt           # "Keep until 31 Dec 2031"
```

One row of `reported_values.csv`:

| report | datapoint | value | unit | calculation | source_files |
|---|---|---|---|---|---|
| CBAM declaration 2026 | Certificates to surrender | 39.4 | certificates | `calculations/2026_cbam_v1.xlsx`, sheet Certificates | `suppliers/…verification-report…pdf`; `customs/…` |

```python
from esgcalc.cbam import records_retention_end
print(records_retention_end(2027))   # 2031-12-31
```

## Common mistakes

- **Counting four years from the import year.** It is four years after
  the **declaration** year: for 2026 imports, until the end of 2031.
- **Keeping the declaration but not the inputs.** The rule covers the
  information used to calculate the emissions, including the verifier's
  report.
- **Editing files after the declaration.** Save a new version; keep the
  hashed original.
- **Forgetting carbon-price evidence.** It has its own four-year rule,
  counted from the year it was certified.

## Evidence to keep

This page is the evidence step. In short: everything in the folder above,
the two registers and a dated `verify` run before submission.

## Templates and tools

- [F1 Evidence locker and audit trail](../foundations/evidence-locker.md):
  folder structure, file naming and the registers.
- [`scripts/hash_evidence.py`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/scripts/hash_evidence.py):
  builds and verifies `evidence_register.csv`. Runs offline.
- [`esgcalc.cbam.records_retention_end`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/esgcalc/cbam.py):
  the retention end date.

## Reuse in other reports

The same locker holds the evidence for Scope 3, VSME and ESRS. See
[F3](../foundations/one-dataset-many-reports.md).

## Sources

Facts come from `data/regulations.yml` (ids `cbam-records`,
`cbam-carbon-price-records`), last checked 20 November 2026.

- Regulation (EU) 2023/956, Articles 7(6) and 9(3), consolidated text:
  [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2023/956/2025-10-20)
