---
description: A free double materiality scoring tool that runs in your browser. Score impacts, risks and opportunities on a 1 to 5 scale and see which ESRS topics are material.
hide:
  - toc
---

# DMA scoring

Score each impact, risk or opportunity from 1 (very low) to 5 (very high).
The tool shows the score of each item, whether it is material, and which of
the ten topical standards are material, from the impact side, the financial
side or both. See [C2 Double materiality assessment](../csrd/c2-dma.md).

!!! danger "Not legal advice"
    A planning aid. The method follows ESRS 1 chapter 3 in this handbook's
    words. The scale, the thresholds and the human rights cut-off are this
    handbook's choices, not the standard's. The example is the fictional
    Mediterranean Logistics Group.

!!! info "Your data stays in your browser"
    Nothing you type is sent anywhere or stored.

<div id="dma-app" class="tool-app" data-ready="false" markdown="0">

<div class="tool-bar">
  <button type="button" id="add-row" class="md-button">Add a row</button>
  <button type="button" id="load-example" class="md-button">Load the Mediterranean Logistics Group example</button>
  <button type="button" id="clear" class="md-button">Clear</button>
</div>

<div class="tool-scroll">
<table id="items" class="tool-table">
  <thead><tr>
    <th>ID</th><th>Standard</th><th>Description</th><th>Type</th>
    <th>Negative</th><th>Actual</th><th>Human rights</th>
    <th>Scale</th><th>Scope</th><th>Irremediability</th><th>Likelihood</th><th>Magnitude</th>
    <th>Score</th><th>Material?</th>
  </tr></thead>
  <tbody></tbody>
</table>
</div>

<h3>Topics</h3>
<div class="tool-scroll">
<table id="topics" class="tool-table" data-material="">
  <thead><tr><th>Standard</th><th>Topic</th><th>Items</th><th>Impact material?</th><th>Financial material?</th><th>Material?</th></tr></thead>
  <tbody></tbody>
</table>
</div>

<p id="summary" data-value=""></p>

</div>

## How it calculates

- **Negative impacts:** severity is the **highest** of scale, scope and
  irremediability, because any one can make an impact severe. Actual: the
  score is the severity. Potential: severity x likelihood / 5.
- **Potential negative human rights impacts:** if severity is 4 or more,
  severity takes precedence and the score is the severity.
- **Positive impacts:** the average of scale and scope; potential ones
  x likelihood / 5.
- **Risks and opportunities:** magnitude x likelihood / 5.
- An item is **material** if its score is at least **3.0**. A topic is
  material if any of its items is.
- Same method and settings as
  [`esgcalc.dma`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/esgcalc/dma.py)
  and `data/dma_parameters.yml`. For your own settings, use the
  [DMA workbook](../downloads/dma-workbook.xlsx).

<!-- generated tool data: dma-scoring-data: do not edit by hand -->
<script type="application/json" id="dma-scoring-data">
{
 "example": [
  {
   "actual": true,
   "description": "GHG emissions from the diesel truck fleet and the cold stores",
   "human_rights": false,
   "id": "E1-I1",
   "irremediability": 4,
   "kind": "impact",
   "likelihood": null,
   "magnitude": null,
   "negative": true,
   "scale": 4,
   "scope": 3,
   "topic": "E1"
  },
  {
   "actual": false,
   "description": "Rising fuel and carbon costs for the diesel fleet",
   "human_rights": false,
   "id": "E1-R1",
   "irremediability": null,
   "kind": "risk",
   "likelihood": 4,
   "magnitude": 4,
   "negative": true,
   "scale": null,
   "scope": null,
   "topic": "E1"
  },
  {
   "actual": false,
   "description": "Supermarkets choosing low-carbon logistics",
   "human_rights": false,
   "id": "E1-O1",
   "irremediability": null,
   "kind": "opportunity",
   "likelihood": 3,
   "magnitude": 3,
   "negative": true,
   "scale": null,
   "scope": null,
   "topic": "E1"
  },
  {
   "actual": false,
   "description": "Air pollution from trucks in towns",
   "human_rights": false,
   "id": "E2-I1",
   "irremediability": 2,
   "kind": "impact",
   "likelihood": 4,
   "magnitude": null,
   "negative": true,
   "scale": 2,
   "scope": 3,
   "topic": "E2"
  },
  {
   "actual": true,
   "description": "Food wasted when the cold chain fails",
   "human_rights": false,
   "id": "E5-I1",
   "irremediability": 2,
   "kind": "impact",
   "likelihood": null,
   "magnitude": null,
   "negative": true,
   "scale": 3,
   "scope": 2,
   "topic": "E5"
  },
  {
   "actual": false,
   "description": "Serious road and warehouse accidents involving drivers and staff",
   "human_rights": true,
   "id": "S1-I1",
   "irremediability": 5,
   "kind": "impact",
   "likelihood": 3,
   "magnitude": null,
   "negative": true,
   "scale": 4,
   "scope": 3,
   "topic": "S1"
  },
  {
   "actual": false,
   "description": "Shortage of truck drivers",
   "human_rights": false,
   "id": "S1-R1",
   "irremediability": null,
   "kind": "risk",
   "likelihood": 4,
   "magnitude": 3,
   "negative": true,
   "scale": null,
   "scope": null,
   "topic": "S1"
  },
  {
   "actual": false,
   "description": "Poor working conditions on farms that supply food suppliers",
   "human_rights": true,
   "id": "S2-I1",
   "irremediability": 3,
   "kind": "impact",
   "likelihood": 2,
   "magnitude": null,
   "negative": true,
   "scale": 3,
   "scope": 3,
   "topic": "S2"
  },
  {
   "actual": false,
   "description": "Bribery at ports and customs",
   "human_rights": false,
   "id": "G1-R1",
   "irremediability": null,
   "kind": "risk",
   "likelihood": 2,
   "magnitude": 2,
   "negative": true,
   "scale": null,
   "scope": null,
   "topic": "G1"
  }
 ],
 "params": {
  "human_rights": {
   "severity_precedence_from": 4
  },
  "scale": {
   "max": 5,
   "min": 1
  },
  "severity_aggregation": "max",
  "thresholds": {
   "financial": 3.0,
   "impact": 3.0
  }
 },
 "standards": [
  {
   "kind": "topical",
   "standard": "E1",
   "topic": "Climate change"
  },
  {
   "kind": "topical",
   "standard": "E2",
   "topic": "Pollution"
  },
  {
   "kind": "topical",
   "standard": "E3",
   "topic": "Water and marine resources"
  },
  {
   "kind": "topical",
   "standard": "E4",
   "topic": "Biodiversity and ecosystems"
  },
  {
   "kind": "topical",
   "standard": "E5",
   "topic": "Resource use and circular economy"
  },
  {
   "kind": "topical",
   "standard": "S1",
   "topic": "Own workforce"
  },
  {
   "kind": "topical",
   "standard": "S2",
   "topic": "Workers in the value chain"
  },
  {
   "kind": "topical",
   "standard": "S3",
   "topic": "Affected communities"
  },
  {
   "kind": "topical",
   "standard": "S4",
   "topic": "Consumers and end-users"
  },
  {
   "kind": "topical",
   "standard": "G1",
   "topic": "Business conduct"
  }
 ]
}
</script>
<!-- end generated tool data: dma-scoring-data -->

<script src="../dma-scoring.js"></script>
