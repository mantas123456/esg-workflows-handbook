---
step: "S5"
status: draft
last_checked: 2026-11-20
---

# S5 Choosing emission factors

!!! warning "Not legal advice"
    This page explains how to choose and document emission factors. The
    factor **values** in the worked examples are made up. Check each
    source's licence before you use its data.

## In one sentence

For each line of the inventory, choose the factor that best matches what
you bought, where and when, **among those whose licence lets you use
them**, and record its source, version, year, unit and licence.

## Who does this and when

The inventory lead, while calculating ([S4](s4-methods.md)). Review the
choices every year: most sources publish new versions.

## Inputs

- The inventory lines and their units ([S4](s4-methods.md)).
- The candidate sources below, and any supplier data or product
  declarations you received.
- Your own position: are you a company using the data for your own
  inventory? Some licences allow only non-commercial or academic use.

## Steps

### 1. Prefer data closest to what you bought

In order: the supplier's own figure for the product ([S7](s7-suppliers.md));
an average factor for that **material or activity**; a spend-based factor
for the **sector**. Each step down usually means a worse data-quality
score.

### 2. Check the factor fits the line

| Check | Question |
|---|---|
| Unit | Is it per kg, per kWh, per tonne.km, per EUR, the same as your activity data? |
| Boundary | Does it cover cradle to gate, or only part of it? |
| Geography | Is it for the country where the goods were made? |
| Time | Is it for the reporting year, or close to it? |
| Technology | Does it match how the goods were made? |
| Gases | Does it cover all greenhouse gases as CO2e, with the same global warming potentials as the rest of your inventory? |

### 3. Check the licence allows **your** use

A good factor you are not allowed to use is not an option. Read the
licence, not a summary of it. Watch for "non-commercial" and
"share-alike" terms, and for databases that need a paid licence.

### 4. Score the options and choose

Score each usable option on the five data-quality indicators
([F2](../foundations/data-quality.md)) and take the best. If two score the
same, take the newer one.

### 5. Record every factor in a factor register

For each factor: source, version, year, unit, licence, and the line it is
used on. When you change a factor, keep the old entry and note why.

### 6. Re-check every year

New versions change values. If a change is large, it may affect your base
year ([S8](s8-base-year.md)).

## Sources this handbook points to

<!-- generated from data/factor_sources.yml: do not edit by hand -->
| Source | Version | Coverage | Method | Licence | Values copied in this handbook? |
|---|---|---|---|---|---|
| [UK Government GHG Conversion Factors for Company Reporting](https://www.gov.uk/government/collections/government-conversion-factors-for-company-reporting) (Department for Energy Security and Net Zero (DESNZ)) | 2026 | Activity-based factors for the UK: fuels, bioenergy, UK grid electricity (generation and T&D losses), passenger and freight transport, materials, waste, homeworking | Average-data | Open Government Licence v3.0 (GOV.UK publication page footer: all content under OGL v3.0 except where otherwise stated; no exception stated for the factor spreadsheets). Attribution required; commercial reuse allowed | Yes, with attribution |
| [Greenhouse gas emission intensity of electricity generation (country level)](https://www.eea.europa.eu/en/analysis/indicators/greenhouse-gas-emission-intensity-of-1) (European Environment Agency (EEA)) | Indicator covering 1990-2025 (latest years partly provisional) | EU Member States and the EU: CO2e from public electricity production divided by gross electricity production | Average-data | CC BY 4.0 (EEA legal notice, https://www.eea.europa.eu/en/legal-notice): commercial and non-commercial reuse allowed if the EEA is acknowledged as the source and the meaning is not distorted; third-party content excluded | Yes, with attribution |
| [EXIOBASE 3 (multi-regional environmentally extended input-output database)](https://zenodo.org/records/14614930) (EXIOBASE consortium, on Zenodo) | 3.11.2 per the EXIOBASE GitHub page (3.11.3 in preparation); the Zenodo record seen is 3.10.2 of 13 May 2026 | Many countries and rest-of-world regions, about 200 products; monetary (spend-based) multipliers | Spend-based | v3.9 and later: customised derivative of CC BY-SA-NC (non-commercial academic use; commercial licences in development). v3.8.x and earlier: CC BY-SA 4.0 | No: link and cite only |
| [Supply Chain Greenhouse Gas Emission Factors for US Industries and Commodities (USEEIO-based)](https://catalog.data.gov/dataset/supply-chain-greenhouse-gas-emission-factors-v1-3-by-naics-6) (US Environmental Protection Agency (EPA), Office of Research and Development) | v1.3 by NAICS-6 (data.gov record modified 2024-07-05) | 1,016 US commodities (NAICS 2017, 6 digits), GHG data for 2022, with and without margins | Spend-based | EPA Data License (https://pasteur.epa.gov/license/sciencehub-license.html): EPA data is public domain by default (17 U.S.C. 105) unless otherwise specified in the dataset's metadata; the v1.3 metadata has not yet been read | Not yet: licence to check |
| [CBAM default values](https://eur-lex.europa.eu/eli/reg_impl/2025/2621/oj/eng) (European Commission (Implementing Regulation (EU) 2025/2621, corrected by 2026/1740)) | 2025/2621 as corrected by 2026/1740 | Default specific embedded emissions of CBAM goods by CN code and country of origin | Average-data | EU legal act on EUR-Lex; the EUR-Lex legal notice could not be read (empty page), so the reuse terms are not yet confirmed | Not yet: licence to check |
| [ecoinvent life cycle inventory database](https://ecoinvent.org/) (ecoinvent Association) | not tracked | Process-based life cycle inventories for many products and services | Average-data | Commercial licence | No: link and cite only |
<!-- end generated factor sources -->

Only sources whose licence has been read and allows reuse have their
values copied into this handbook. The others are linked and cited only,
and the worked examples use made-up values instead.

## Worked example

Gozo Fresh Foods Ltd (fictional) chooses a factor for its 150,000 kg of
**plastic film packaging** ([S4](s4-methods.md)). No supplier figure is
available yet. All factor values are made up.

| Option | Source | Scores (technology, time, geography, completeness, reliability) | Score | Licence allows Gozo's use? |
|---|---|---|---|---|
| ecoinvent dataset for plastic film | ecoinvent | 2, 2, 3, 1, 2 | 2.0 | No: Gozo holds no ecoinvent licence |
| DESNZ 2026 material-use factor for plastic film | DESNZ 2026 | 2, 1, 3, 2, 2 | 2.0 | Yes: Open Government Licence v3.0 |
| EXIOBASE multiplier for plastic products (spend-based) | EXIOBASE 3.11.2 | 4, 3, 2, 3, 3 | 3.0 | No: v3.9 and later: non-commercial academic use only |

Gozo chooses the **DESNZ 2026 material-use factor for plastic film**. The
ecoinvent dataset scores the same, but Gozo has no licence for it. The
EXIOBASE multiplier is a rougher, spend-based factor, and its licence
allows only non-commercial academic use. The geography score of 3 reflects
a UK factor used for packaging bought in Malta.

**Gozo's factor register** for the average-data and spend-based lines in
[S4](s4-methods.md):

| Line | Source | Note |
|---|---|---|
| Cardboard packaging | DESNZ 2026 | Material use |
| Plastic film packaging | DESNZ 2026 | Material use |
| Glass jars | DESNZ 2026 | Material use |
| Upstream emissions of purchased electricity | DESNZ 2026 | Grid losses (UK, as a proxy); check the 2026 set for the upstream part of generation |
| Upstream emissions of fuels burned | DESNZ 2026 | Fuels; check the 2026 set for the upstream (well-to-tank) part |
| Road freight from haulier records | DESNZ 2026 | Freight, per tonne.km |
| Commuting by car (staff survey) | DESNZ 2026 | Passenger vehicles |
| Commuting by bus (staff survey) | DESNZ 2026 | Public transport |
| Supermarket transport to its stores (its figures) | DESNZ 2026 | Freight, per tonne.km |
| Cardboard at end of life | DESNZ 2026 | Waste disposal |
| Plastic film at end of life | DESNZ 2026 | Waste disposal |
| Glass at end of life | DESNZ 2026 | Waste disposal |
| Food wasted by consumers | DESNZ 2026 | Waste disposal |
| Other ingredient suppliers | To choose | Spend-based: EXIOBASE is not usable without a commercial licence; EPA USEEIO needs a currency conversion and its dataset terms checked |
| Services (cleaning, IT, maintenance) | To choose | As above |
| Machinery and equipment bought in 2026 | To choose | As above |
| Chilled storage at the supermarket (its figures) | To choose | Ask the supermarket which factor it uses |

**13** of the 17 lines have a usable, documented source. The **4** spend-
and storage lines are still open; until they are settled, S4's
placeholder factors stay, marked as such.

In Python, with
[`esgcalc`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/esgcalc/factors.py):

```python
from esgcalc.factors import FactorOption, choose_factor
from esgcalc.quality import DataQuality

options = [
    FactorOption("ecoinvent", "ecoinvent", "not tracked", 2024, "kg CO2e/kg",
                 DataQuality(2, 2, 3, 1, 2), licence_allows_use=False),
    FactorOption("DESNZ 2026", "desnz-2026", "2026", 2026, "kg CO2e/kg",
                 DataQuality(2, 1, 3, 2, 2), licence_allows_use=True),
    FactorOption("EXIOBASE", "exiobase-3", "3.11.2", 2022, "kg CO2e/EUR",
                 DataQuality(4, 3, 2, 3, 3), licence_allows_use=False),
]
print(choose_factor(options).name)   # DESNZ 2026
```

## Common mistakes

- **Using a database you are not licensed to use.** Free to download is
  not free to use. Check the licence for your purpose.
- **Unit mismatch.** A factor per tonne applied to kilograms is out by
  1,000.
- **Old factors.** A factor from years ago may no longer fit. Note its
  year and update it.
- **No record.** A number without its source, version, year and unit
  cannot be checked.
- **Different gas sets.** Mixing factors with different global warming
  potentials makes totals inconsistent.
- **Using an electricity *generation* intensity for *upstream* emissions.**
  They measure different things: check what the factor covers.

## Evidence to keep

- The factor register, with every change dated and explained.
- A copy of each factor table used, and its licence text.
- The scoring of options for the large lines.

File them in the evidence locker (see
[F1](../foundations/evidence-locker.md)).

## Templates and tools

- [`esgcalc.factors.choose_factor`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/esgcalc/factors.py):
  picks the best usable option, as above.
- [`data/factor_sources.yml`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/data/factor_sources.yml):
  the source list behind the table above, with licence notes.

## Reuse in other reports

The same factor register serves Scope 1 and 2, VSME and ESRS E1, and the
same electricity and fuel factors appear in each. Keep one register. See
[F3](../foundations/one-dataset-many-reports.md).

## Sources

Facts and licences come from `data/regulations.yml` and
`data/factor_sources.yml`, last checked 20 November 2026.

- GHG Protocol Corporate Value Chain (Scope 3) Standard (cited, not
  copied):
  [ghgprotocol.org](https://ghgprotocol.org/corporate-value-chain-scope-3-standard)
- DESNZ, Government conversion factors for company reporting 2026, Open
  Government Licence v3.0:
  [GOV.UK](https://www.gov.uk/government/publications/greenhouse-gas-reporting-conversion-factors-2026)
- EEA, legal notice (CC BY 4.0):
  [eea.europa.eu](https://www.eea.europa.eu/en/legal-notice)
- EXIOBASE 3 licence notes:
  [Zenodo](https://zenodo.org/records/14614930)
- EPA data licence:
  [pasteur.epa.gov](https://pasteur.epa.gov/license/sciencehub-license.html)
