---
description: A free CBAM calculator that runs in your browser. Enter imports by CN code and net mass, actual or default emissions, and a certificate price; get the 50-tonne threshold result, embedded emissions, certificates, cost and the quarterly holding.
hide:
  - toc
---

# CBAM calculator

Enter your imports for one calendar year. The calculator shows the
50-tonne threshold result, the embedded emissions, the certificates to
surrender, their cost and, from 2027, the minimum quarterly holding. It
uses the same method as the handbook's
[`esgcalc`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/esgcalc/cbam.py)
package and the steps in [CB1](../cbam/cb1-scope-check.md),
[CB4](../cbam/cb4-embedded-emissions.md) and [CB8](../cbam/cb8-certificates.md).

!!! danger "Not legal advice"
    This is a planning tool. It does not decide whether CBAM applies to
    you, and its results are not your CBAM declaration. The regulation,
    the CBAM registry and your competent authority always take priority.
    The example figures are **made up**. Use real default values,
    free allocation benchmarks and certificate prices.

!!! info "Your data stays in your browser"
    The calculator runs entirely on this page. Nothing you enter is sent
    anywhere or stored.

<div id="cbam-app" class="tool-app" data-ready="false" markdown="0">

<div class="tool-bar">
  <label class="tool-field">Year of import <input type="number" id="year" min="2026" max="2100" step="1" value="2026"></label>
  <label class="tool-field">Certificate price (EUR) <input type="number" id="price" min="0" step="0.01" value=""></label>
  <label class="tool-field">Carbon price paid reduction (certificates) <input type="number" id="cpp" min="0" step="0.001" value="0"></label>
</div>
<div class="tool-bar">
  <button type="button" id="add-line" class="md-button md-button--primary">Add line</button>
  <button type="button" id="load-example" class="md-button">Load the Melita Metals example</button>
  <button type="button" id="clear" class="md-button">Clear</button>
</div>

<div class="tool-scroll">
<table id="lines" class="tool-table">
  <thead>
    <tr>
      <th>Quarter</th><th>CN code</th><th>Sector</th><th>Net mass (t)</th><th>Basis</th>
      <th>Actual SEE (tCO2e/t)</th><th>Base default value (tCO2e/t)</th>
      <th>Free allocation adjustment per t</th><th>Embedded emissions (tCO2e)</th><th></th>
    </tr>
  </thead>
  <tbody></tbody>
</table>
</div>

<p id="errors" class="tool-errors" role="alert"></p>

<h2>Results</h2>
<table class="tool-results">
  <tbody>
    <tr><th>Net mass counted towards the threshold</th><td><span id="out-total-mass" data-value=""></span> t</td></tr>
    <tr><th>Threshold test (50 t or less is exempt)</th><td id="out-threshold" data-value=""></td></tr>
    <tr><th>Total embedded emissions</th><td><span id="out-embedded" data-value=""></span> tCO2e</td></tr>
    <tr><th>Free allocation adjustment</th><td><span id="out-fa" data-value=""></span> tCO2e</td></tr>
    <tr><th>Certificates to surrender</th><td><strong id="out-certs" data-value=""></strong></td></tr>
    <tr><th>Cost</th><td>EUR <strong id="out-cost" data-value=""></strong></td></tr>
  </tbody>
</table>
<p id="out-notes" class="tool-notes"></p>

<h3>Minimum quarterly holding</h3>
<p id="holding-note" class="tool-notes"></p>
<table id="holding" class="tool-table">
  <thead><tr><th>End of</th><th>Emissions YTD (tCO2e)</th><th>Adjustment YTD (tCO2e)</th><th>Minimum holding (certificates)</th></tr></thead>
  <tbody></tbody>
</table>

</div>

## How it calculates

- **Threshold:** adds the net mass of every line except hydrogen (CN 2804
  10 00) and electricity (CN 2716 00 00), which have no threshold. Above
  50 t, CBAM covers all lines of the year.
- **Embedded emissions:** net mass × SEE. With basis *Actual*, the SEE is
  the verified figure from the installation (it already includes
  precursors; see [CB5](../cbam/cb5-precursors.md)). With basis
  *Default*, it is the base default value plus the mark-up for the year
  (10% in 2026, 20% in 2027, 30% from 2028; 1% for fertilisers).
- **Certificates:** embedded emissions − free allocation adjustment −
  carbon price paid reduction, never below zero. One certificate is one
  tonne of CO2e. Rounding by the registry is not modelled.
- **Cost:** certificates × price, rounded to the cent.
- **Quarterly holding (from 2027):** 50% × (emissions year-to-date −
  adjustment year-to-date). Emissions here use the base default value
  without mark-up where one is entered, otherwise the actual SEE.

<!-- generated from data/cbam_parameters.yml and data/examples/melita_metals.yml: do not edit by hand -->
<script type="application/json" id="cbam-tool-data">
{
 "example": {
  "carbon_price_paid_certificates": 0,
  "lines": [
   {
    "actual_see": 0.652,
    "base_default": 1.6,
    "basis": "actual",
    "cn_code": "7214 20 00",
    "fa_per_t": 0.585,
    "mass_t": 60,
    "quarter": "Q1",
    "sector": "iron_steel"
   },
   {
    "actual_see": null,
    "base_default": 2.1,
    "basis": "default",
    "cn_code": "7604 29 10",
    "fa_per_t": 1.95,
    "mass_t": 8,
    "quarter": "Q1",
    "sector": "aluminium"
   },
   {
    "actual_see": 0.652,
    "base_default": 1.6,
    "basis": "actual",
    "cn_code": "7214 20 00",
    "fa_per_t": 0.585,
    "mass_t": 70,
    "quarter": "Q2",
    "sector": "iron_steel"
   },
   {
    "actual_see": 0.652,
    "base_default": 1.6,
    "basis": "actual",
    "cn_code": "7214 99 10",
    "fa_per_t": 0.585,
    "mass_t": 40,
    "quarter": "Q2",
    "sector": "iron_steel"
   },
   {
    "actual_see": null,
    "base_default": 2.1,
    "basis": "default",
    "cn_code": "7604 29 10",
    "fa_per_t": 1.95,
    "mass_t": 9,
    "quarter": "Q2",
    "sector": "aluminium"
   },
   {
    "actual_see": 0.652,
    "base_default": 1.6,
    "basis": "actual",
    "cn_code": "7214 20 00",
    "fa_per_t": 0.585,
    "mass_t": 65,
    "quarter": "Q3",
    "sector": "iron_steel"
   },
   {
    "actual_see": 0.652,
    "base_default": 1.6,
    "basis": "actual",
    "cn_code": "7214 99 10",
    "fa_per_t": 0.585,
    "mass_t": 45,
    "quarter": "Q3",
    "sector": "iron_steel"
   },
   {
    "actual_see": null,
    "base_default": 2.1,
    "basis": "default",
    "cn_code": "7604 29 10",
    "fa_per_t": 1.95,
    "mass_t": 10,
    "quarter": "Q3",
    "sector": "aluminium"
   },
   {
    "actual_see": 0.652,
    "base_default": 1.6,
    "basis": "actual",
    "cn_code": "7214 20 00",
    "fa_per_t": 0.585,
    "mass_t": 55,
    "quarter": "Q4",
    "sector": "iron_steel"
   },
   {
    "actual_see": 0.652,
    "base_default": 1.6,
    "basis": "actual",
    "cn_code": "7214 99 10",
    "fa_per_t": 0.585,
    "mass_t": 65,
    "quarter": "Q4",
    "sector": "iron_steel"
   },
   {
    "actual_see": null,
    "base_default": 2.1,
    "basis": "default",
    "cn_code": "7604 29 10",
    "fa_per_t": 1.95,
    "mass_t": 8,
    "quarter": "Q4",
    "sector": "aluminium"
   }
  ],
  "price_eur": 80.0,
  "year": 2026
 },
 "params": {
  "excluded_cn_codes": {
   "27160000": "electricity",
   "28041000": "hydrogen"
  },
  "holding_from_year": 2027,
  "holding_min_share": 0.5,
  "markup_by_year": {
   "2026": 0.1,
   "2027": 0.2,
   "2028": 0.3
  },
  "max_exempt_mass_t": 50,
  "sector_markup": {
   "fertilisers": 0.01
  },
  "tco2e_per_certificate": 1
 }
}
</script>
<!-- end generated tool data -->

<script src="../cbam-calculator.js"></script>
