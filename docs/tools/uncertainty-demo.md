---
description: A free Monte Carlo uncertainty demo that runs in your browser. Enter emissions lines with their 95% uncertainty; compare the sum rule with a simulation and see the histogram.
hide:
  - toc
---

# Uncertainty demo

Enter the lines that make up a total, each with its value and its 95%
uncertainty (±%). The demo combines them two ways: the **sum rule**, and a
**Monte Carlo** simulation in which every line follows a lognormal
distribution. See [F2 Data quality and uncertainty](../foundations/data-quality.md)
for the method.

!!! danger "Not legal advice"
    A teaching tool. The example is the fictional Gozo Fresh Foods'
    category 1, with made-up uncertainties.

!!! info "Your data stays in your browser"
    The simulation runs entirely on this page. Nothing you enter is sent
    anywhere or stored.

<div id="uncertainty-app" class="tool-app" data-ready="false" markdown="0">

<div class="tool-bar">
  <label class="tool-field">Draws <input type="number" id="draws" min="1000" max="500000" step="1000" value="100000"></label>
  <label class="tool-field">Seed <input type="number" id="seed" min="1" step="1" value="20260101"></label>
  <button type="button" id="run" class="md-button md-button--primary">Run</button>
  <button type="button" id="add-line" class="md-button">Add line</button>
  <button type="button" id="load-example" class="md-button">Load the Gozo Fresh Foods example</button>
</div>

<div class="tool-scroll">
<table id="lines" class="tool-table">
  <thead><tr><th>Line</th><th>Value (tCO2e)</th><th>±95% (%)</th><th><span class="visually-hidden">Remove line</span></th></tr></thead>
  <tbody></tbody>
</table>
</div>

<p id="errors" class="tool-errors" role="alert"></p>

<table class="tool-results">
  <thead><tr><th><span class="visually-hidden">Result</span></th><th>Sum rule</th><th>Monte Carlo</th></tr></thead>
  <tbody>
    <tr><th>Central value</th><td id="sum-value" data-value=""></td><td id="mc-median" data-value=""></td></tr>
    <tr><th>95% interval</th><td id="sum-interval" data-low="" data-high=""></td><td id="mc-interval" data-low="" data-high=""></td></tr>
    <tr><th>±95%</th><td id="sum-rel" data-value=""></td><td id="mc-mean" data-value=""></td></tr>
  </tbody>
</table>

<svg id="histogram" class="tool-histogram" viewBox="0 0 600 220" role="img" aria-label="Histogram of the simulated totals"></svg>

</div>

## How it calculates

- **Sum rule:** U = √(Σ (value × u)²), assuming the lines are independent.
- **Monte Carlo:** each line is drawn as value × a lognormal factor with
  median 1, whose 97.5th percentile is 1 + u (so ±20% runs from 0.833 to
  1.20). The total's 2.5th and 97.5th percentiles give the interval. The
  draws use a seeded random generator, so the same seed gives the same
  result. The bottom-right cell shows the simulated mean.

<!-- generated tool data: uncertainty-demo-data: do not edit by hand -->
<script type="application/json" id="uncertainty-demo-data">
{
 "example": {
  "draws": 100000,
  "lines": [
   {
    "name": "Maltese Farmers Cooperative",
    "u95": 0.1,
    "value": 900.0
   },
   {
    "name": "Sicilian Tomato Co",
    "u95": 0.1,
    "value": 1200.0
   },
   {
    "name": "Gozo Greens Ltd",
    "u95": 0.15,
    "value": 500.0
   },
   {
    "name": "Island Dairy Ltd",
    "u95": 0.15,
    "value": 420.0
   },
   {
    "name": "Mediterranean Oils",
    "u95": 0.2,
    "value": 200.0
   },
   {
    "name": "Other ingredient suppliers",
    "u95": 0.5,
    "value": 686.440678
   },
   {
    "name": "Services (cleaning, IT, maintenance)",
    "u95": 0.5,
    "value": 63.559322
   },
   {
    "name": "Cardboard packaging",
    "u95": 0.206155,
    "value": 320.0
   },
   {
    "name": "Plastic film packaging",
    "u95": 0.206155,
    "value": 375.0
   },
   {
    "name": "Glass jars",
    "u95": 0.206155,
    "value": 180.0
   }
  ],
  "seed": 20260101
 }
}
</script>
<!-- end generated tool data: uncertainty-demo-data -->

<script src="../uncertainty-demo.js"></script>
