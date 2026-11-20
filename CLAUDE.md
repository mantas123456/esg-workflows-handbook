# CLAUDE.md: ESG Workflows Handbook

Project memory for Claude Code. Read this before every task.

## What this repo is

A free MkDocs Material handbook of step-by-step workflows for CBAM, Scope 3,
VSME and CSRD/ESRS, published on GitHub Pages. Plan: `DEVELOPMENT_PLAN.md`.
Staged build prompts: `prompts/STAGED_PROMPTS.md`.
Sister project with the same conventions: `mantas123456/lab-accreditation-handbook`.

## Single sources of truth

- `data/workflows.yml`: every step (id, title, file, release, status, templates, tools).
  Never add a page without adding it here first.
- `data/regulations.yml`: every regulatory fact with source URL and `last_checked`.
  Pages state facts that are in this file; if a page needs a new fact, add it here with a source.
- `docs/_chapter_template.md`: the format every step page follows.

## Commands (Windows PowerShell)

```powershell
.venv\Scripts\activate
python scripts/build_templates.py  # Word/Excel templates into docs/downloads (mkdocs needs them)
python scripts/build_pages.py      # placeholders, workflow map, nav, download links
python scripts/check_workflows.py  # must print 0 errors
pytest -q                          # must pass
mkdocs build --strict              # must pass
mkdocs serve                       # preview at http://127.0.0.1:8000
```

Run all four checks before every commit.

## Writing rules

- Plain English, short sentences. Many readers work in a second language.
- Explain rules in your own words. Cite EU law by regulation + article and link EUR-Lex.
  Never copy text from the GHG Protocol, EFRAG guidance, ISO standards or paid sources.
- Worked examples: fictional companies (e.g. "Melita Metals Ltd", Malta), made-up but
  realistic numbers. Every worked-example number must be recomputed by a test in `tests/`.
- Every emission factor: source, version, year, unit, licence. Prefer open sources
  (DESNZ/DEFRA, EEA, EU CBAM default values). Do not paste licensed ecoinvent data.
- Treat emissions as measurements: show inputs, units, data-quality score and uncertainty.
- Each page ends with "Sources". Set `last_checked` in front matter to today's date.
- When a page is written, set its `status` in `data/workflows.yml` to `draft`.
- Not legal advice: never tell a reader they are or are not in scope; show the test and the source.

## Regulatory facts

Rules are still moving (CBAM secondary legislation, ESRS/VSME delegated acts, national
transposition of Omnibus I). Before writing any track, use web search to re-verify the
facts in `data/regulations.yml` against official sources (EUR-Lex, DG TAXUD, EFRAG,
European Commission). Update the file and tell me what changed. If sources disagree,
stop and ask me.

## Code

- Calculations live in the `esgcalc/` Python package (3.12, type hints, no network calls).
- Units explicit in names: `mass_t`, `see_tco2e_per_t`, `price_eur_per_tco2e`.
- Browser tools: single HTML + JS under `docs/tools/`, fully client-side, no tracking, no data
  leaves the browser. Test with Playwright.
- Templates: sources under `templates/`, built by `scripts/build_templates.py` into
  `docs/downloads/` (not committed).

## Git

- Small commits, one step or tool per commit, message `CB4: embedded emissions page and calculator`.
- Work on a branch per release (`release/0.2-cbam`), merge to `main` when the release checks pass.
- Never commit `.venv/`, `site/`, `docs/downloads/` or any real client data.
