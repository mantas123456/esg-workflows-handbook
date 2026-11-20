---
description: A free Scope 3 screening tool that runs in your browser. Enter a rough estimate for each of the 15 categories, a size threshold and any other reasons; see each category's share and which are significant.
hide:
  - toc
---

# Scope 3 screening

Enter a rough estimate for **every one** of the 15 Scope 3 categories (0
where a category does not apply), choose a size threshold, and add any
other reason that makes a category significant. The tool shows each
category's share and which categories are significant. It follows
[S2 Screening the 15 categories](../scope3/s2-screening.md) and the
handbook's [`esgcalc`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/esgcalc/scope3.py)
package.

!!! danger "Not legal advice"
    A planning tool. Screening estimates are rough; the significant
    categories need better data. The example is the fictional Gozo Fresh
    Foods with made-up factors.

!!! info "Your data stays in your browser"
    The tool runs entirely on this page. Nothing you enter is sent anywhere
    or stored.

<div id="screening-app" class="tool-app" data-ready="false" markdown="0">

<div class="tool-bar">
  <label class="tool-field">Size threshold (% of total) <input type="number" id="threshold" min="0.1" max="99" step="0.1" value="2"></label>
  <button type="button" id="load-example" class="md-button">Load the Gozo Fresh Foods example</button>
  <button type="button" id="clear" class="md-button">Clear</button>
</div>

<div class="tool-scroll">
<table id="categories" class="tool-table">
  <thead>
    <tr><th>#</th><th>Category</th><th>Estimate (tCO2e)</th><th>Other reason (spend, influence, risk, stakeholder)</th><th>Share</th><th>Significant?</th></tr>
  </thead>
  <tbody></tbody>
</table>
</div>

<p id="errors" class="tool-errors" role="alert"></p>

<table class="tool-results">
  <tbody>
    <tr><th>Total screened</th><td><span id="out-total" data-value=""></span> tCO2e</td></tr>
    <tr><th>Significant categories</th><td id="out-significant" data-value=""></td></tr>
    <tr><th>Share covered by significant categories</th><td id="out-coverage" data-value=""></td></tr>
  </tbody>
</table>

</div>

## How it calculates

- **Share** = the category's estimate / the total of all 15.
- **Significant by size** if the share is at or above the threshold.
- **Significant** if significant by size **or** another reason is given.

<!-- generated tool data: scope3-screening-data: do not edit by hand -->
<script type="application/json" id="scope3-screening-data">
{
 "categories": {
  "1": "Purchased goods and services",
  "10": "Processing of sold products",
  "11": "Use of sold products",
  "12": "End-of-life treatment of sold products",
  "13": "Downstream leased assets",
  "14": "Franchises",
  "15": "Investments",
  "2": "Capital goods",
  "3": "Fuel- and energy-related activities",
  "4": "Upstream transportation and distribution",
  "5": "Waste generated in operations",
  "6": "Business travel",
  "7": "Employee commuting",
  "8": "Upstream leased assets",
  "9": "Downstream transportation and distribution"
 },
 "example": {
  "estimates": {
   "1": 6375.0,
   "10": 0.0,
   "11": 0.0,
   "12": 195.0,
   "13": 0.0,
   "14": 0.0,
   "15": 75.0,
   "2": 160.0,
   "3": 180.0,
   "4": 180.0,
   "5": 31.0,
   "6": 10.0,
   "7": 157.08,
   "8": 0.0,
   "9": 126.0
  },
  "reasons": {
   "9": "The supermarket asked for it, and Gozo can reduce it through packaging and shelf life."
  },
  "threshold_share": 0.02
 }
}
</script>
<!-- end generated tool data: scope3-screening-data -->

<script src="../scope3-screening.js"></script>
