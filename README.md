# ESG Workflows Handbook

[![docs](https://github.com/mantas123456/esg-workflows-handbook/actions/workflows/docs.yml/badge.svg)](https://github.com/mantas123456/esg-workflows-handbook/actions/workflows/docs.yml)
[![Text: CC BY 4.0](https://img.shields.io/badge/text-CC%20BY%204.0-lightgrey.svg)](LICENSE-docs)
[![Code: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE)

**Read it here: https://mantas123456.github.io/esg-workflows-handbook/**

A free, practical handbook of step-by-step workflows for four EU
sustainability regimes:

- **CBAM**: from the 50-tonne scope check to the annual declaration
- **Scope 3**: screening, calculation, data quality, supplier engagement
- **VSME**: the voluntary standard for SMEs, and answering customer and bank requests
- **CSRD / ESRS**: the simplified ESRS after Omnibus I

One page per step: what it is, inputs, steps, a worked example with made-up
numbers, common mistakes, templates, tools and sources. Emissions numbers
are treated as measurements, with traceable inputs and stated uncertainty.

**Status:** version 0.1 (skeleton) released 20 November 2026: triage,
regulation timeline, evidence locker and data reuse map are drafted; every
other step has a placeholder. Next: 0.2 CBAM track. See the
[changelog](docs/changelog.md), the [roadmap](docs/roadmap.md),
[DEVELOPMENT_PLAN.md](DEVELOPMENT_PLAN.md) and the
[staged build prompts](prompts/STAGED_PROMPTS.md).

> Not legal advice. The handbook explains the rules in its own words and
> links the sources. The regulation, the Commission's guidance and your
> competent authority always take priority.

## Build locally

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
pip install -r requirements-dev.txt
python scripts/build_pages.py     # placeholder pages, workflow map, nav
python scripts/check_workflows.py
mkdocs serve                      # http://127.0.0.1:8000
```

## How it is built

- `data/workflows.yml` is the single source for every step: id, title,
  page, release, status, templates and tools.
- `data/regulations.yml` holds the regulatory facts with sources and a
  `last_checked` date.
- `data/datasets.yml` is the data dictionary behind the reuse map in F3.
- `scripts/build_pages.py` creates a Planned page for any step without one,
  writes the workflow map, the navigation and the F3 reuse-map table.
- `scripts/hash_evidence.py` builds and verifies a SHA-256 evidence
  register for a folder (see F1).
- `scripts/check_workflows.py` (run in CI) fails if a step has no page or a
  written page lacks a standard heading, and warns when a regulation fact
  has not been re-checked for 90 days.
- `docs/_chapter_template.md` is the format every step page follows.

## Licences

Text and templates: [CC BY 4.0](LICENSE-docs). Code: [MIT](LICENSE).
