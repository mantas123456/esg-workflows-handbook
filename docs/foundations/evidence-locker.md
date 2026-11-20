---
step: "F1"
status: draft
last_checked: 2026-11-20
---

# F1 Evidence locker and audit trail

!!! warning "Not legal advice"
    Retention rules depend on the regime and on national law. This page
    shows the CBAM rule and its source. Check your own obligations with
    your adviser, auditor or competent authority.

## In one sentence

Keep every source file in one place, give each one a fingerprint
(a SHA-256 hash), and keep a register that links each reported number to
its calculation and to the exact files behind it.

## Who does this and when

The person who collects the data: often finance, the sustainability lead,
or the customs broker for CBAM. Set the locker up **before** the first
data comes in, and add files as they arrive. Hash and verify the folder
before every report, declaration or audit.

## Inputs

- A shared folder that only a few people can change (a company drive,
  SharePoint or a NAS with backups).
- The source documents: invoices, meter readings, customs declarations,
  supplier emissions data, verifier reports.
- Python 3.12 to run the hashing script, or any tool that computes
  SHA-256.

## Steps

### 1. Set up the folder structure

One folder per reporting year, one sub-folder per topic. Keep the
registers at the top of each year.

```text
evidence/
  2026/
    evidence_register.csv      # every file, with its SHA-256 hash
    reported_values.csv        # every reported number -> calculation -> files
    cbam/
      customs/                 # customs declarations, CN codes, net mass
      suppliers/               # installation operator data, verifier reports
      carbon-price-paid/       # proof of carbon price paid abroad
    energy/                    # electricity, gas and fuel invoices, meter readings
    scope3/                    # spend data, supplier data, emission factor sources
    calculations/              # workbooks and scripts that produce the numbers
```

### 2. Name files the same way every time

`YYYY-MM-DD_source_description_vN.ext`

- `2026-01-31_enemalta_electricity-invoice-jan_v1.pdf`
- `2026-03-15_supplier-ankara-steel_emissions-data-q4-2025_v2.xlsx`

The date is the date on the document, not the day you saved it. Never
overwrite a file. Save a new version (`_v2`) and keep the old one.

### 3. Hash every file with SHA-256

A SHA-256 hash is a 64-character fingerprint of a file's exact bytes.
If a single character in the file changes, the hash changes completely.
If the hash is the same, the file is the same. This lets you show an
auditor that the file you used in March is the file you have now.

Use the script
[`scripts/hash_evidence.py`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/scripts/hash_evidence.py).
It runs on your own computer and sends nothing over the network.

```powershell
# Write or refresh the register (keeps any notes you added)
python scripts/hash_evidence.py build evidence/2026

# Check that nothing changed, went missing, or was added without registering
python scripts/hash_evidence.py verify evidence/2026
```

`build` writes `evidence_register.csv` with these columns:

| Column | Meaning |
|---|---|
| `path` | File path inside the year folder |
| `sha256` | The file's SHA-256 hash |
| `size` | Size in bytes |
| `modified` | Last-modified time (UTC) |
| `note` | Your comment, e.g. "received from supplier by email 15 Mar" |

`verify` lists every file that is **changed**, **missing** or **not
registered**, and exits with an error code if it finds any. Run it before
you sign off a report.

### 4. Link each reported number to its evidence

Keep a second register, `reported_values.csv`, with one row per number
you report:

| Column | Example |
|---|---|
| `report` | CBAM declaration 2026 |
| `datapoint` | Electricity use Q1 2026 |
| `value` | 1250 |
| `unit` | MWh |
| `calculation` | `calculations/2026_energy_v1.xlsx`, sheet Q1, cell D5 |
| `source_files` | `energy/2026-01-31_enemalta_electricity-invoice-jan_v1.pdf`; ... |
| `source_sha256` | the hashes from `evidence_register.csv`, in the same order |

An auditor can now start from any reported number, open the calculation,
and check that each source file still has the same hash.

### 5. Keep the files long enough

| Regime | What to keep | How long | Source |
|---|---|---|---|
| CBAM | Information used to calculate embedded emissions, including the verifier's report | Until the end of the **fourth year** after the year the CBAM declaration was or should have been submitted | Regulation (EU) 2023/956, [Article 7(6)](https://eur-lex.europa.eu/eli/reg/2023/956/2025-10-20) |
| CBAM | Documents that support a deduction for carbon price paid abroad | Until the end of the **fourth year** after the year the independent person certified them | Regulation (EU) 2023/956, [Article 9(3)](https://eur-lex.europa.eu/eli/reg/2023/956/2025-10-20), as amended |
| CSRD / ESRS, VSME, Scope 3 | Data and calculations behind the report | This handbook does not yet list an EU-wide period. Follow national accounting law and agree a period with your auditor | Your national law |

Keep the hashes and registers for as long as the files themselves.

## Worked example

Melita Metals Ltd is a fictional importer in Malta. It reports electricity
use for its CBAM and Scope 2 data. The numbers are made up.

**The number.** Electricity use in Q1 2026 is the sum of three monthly
invoices:

| Month | Invoice file | MWh |
|---|---|---|
| January | `energy/2026-01-31_enemalta_electricity-invoice-jan_v1.pdf` | 410 |
| February | `energy/2026-02-28_enemalta_electricity-invoice-feb_v1.pdf` | 395 |
| March | `energy/2026-03-31_enemalta_electricity-invoice-mar_v1.pdf` | 445 |
| **Q1 total** | | **1,250** |

**The hash.** To keep the example short, imagine the January invoice
contains only this one line of text (with a line break at the end):

```text
Melita Metals Ltd, electricity invoice, January 2026
```

Its SHA-256 hash is:

```text
9f6b69d7da7a903199542b29ecdcc9beb38495b43756f5eb7688045b3b90baa5
```

Someone adds one exclamation mark after "2026". The hash becomes:

```text
6c2bbd10d6b22eb5d14dff01b0d220d491b5a3fd2916495fab20b05631232a16
```

Every character is different. `verify` reports the file as **CHANGED**,
and Melita Metals knows to find out who edited the invoice and why.

**The trail.** The row in `reported_values.csv` links 1,250 MWh to the
workbook cell that adds the three invoices, and to the three invoice
hashes. Both numbers and the January hash are recomputed by a test on
every build.

## Common mistakes

- Saving files in personal email or on a laptop. Move them to the locker
  the day they arrive.
- Overwriting a file with a corrected version. Save `_v2` and keep `_v1`.
- Hashing once and never verifying. Run `verify` before every report.
- Editing a file after hashing it, even just to "tidy" it. The hash will
  no longer match. Save a new version instead.
- Linking a reported number to a folder, not to specific files and
  hashes.
- Deleting CBAM evidence too early. The four-year period starts after
  the declaration year, not the import year.

## Evidence to keep

This page is the evidence process. In short: the source files, the two
registers (`evidence_register.csv` and `reported_values.csv`), the
calculation files, and a dated record of each `verify` run.

## Templates and tools

- [`scripts/hash_evidence.py`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/scripts/hash_evidence.py):
  builds and verifies `evidence_register.csv`. Works offline.
- An evidence register workbook is planned with the CBAM templates in
  version 0.2.

## Reuse in other reports

One locker serves every regime. The same electricity invoice supports
CBAM indirect emissions, Scope 2, VSME and ESRS E1. Register it once and
link it from each report's rows in `reported_values.csv`. See
[F3 One dataset, many reports](one-dataset-many-reports.md).

## Sources

Retention facts come from `data/regulations.yml`, last checked 20 November
2026.

- Regulation (EU) 2023/956 (CBAM), Articles 7(6) and 9(3), consolidated
  version of 20 October 2025:
  [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2023/956/2025-10-20)
- Regulation (EU) 2025/2083, amending the CBAM Regulation:
  [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2025/2083/oj/eng)
- SHA-256 is defined in the US Federal Information Processing Standard
  FIPS 180-4, Secure Hash Standard:
  [NIST](https://csrc.nist.gov/pubs/fips/180-4/upd1/final)
