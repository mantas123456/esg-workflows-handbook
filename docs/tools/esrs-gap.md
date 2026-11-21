---
description: A free ESRS datapoint gap check that runs in your browser. Choose your material topics, give each datapoint in scope a status, and see what is ready and what is missing.
hide:
  - toc
---

# ESRS gap check

Tick the topical standards your double materiality assessment found
material. The check lists the datapoints in scope (ESRS 2 plus the material
standards). Give each one a status and see how ready you are. See
[C7 Datapoint gap analysis](../csrd/c7-gap-analysis.md).

!!! danger "Not legal advice"
    A planning aid built on this handbook's key datapoints, not EFRAG's full
    datapoint list. The descriptions are the handbook's own words. The
    example is the fictional Mediterranean Logistics Group.

!!! info "Your data stays in your browser"
    Nothing you choose is sent anywhere or stored.

<div id="gap-app" class="tool-app" data-ready="false" markdown="0">

<div class="tool-bar">
  <button type="button" id="load-example" class="md-button">Load the Mediterranean Logistics Group example</button>
  <button type="button" id="clear" class="md-button">Clear</button>
</div>

<h2>Material topics</h2>
<div id="standards" class="tool-bar"></div>

<table class="tool-results">
  <tbody>
    <tr><th>Datapoints in scope</th><td id="out-total" data-value=""></td></tr>
    <tr><th>Ready</th><td id="out-Ready" data-value=""></td></tr>
    <tr><th>Partial</th><td id="out-Partial" data-value=""></td></tr>
    <tr><th>Gap</th><td id="out-Gap" data-value=""></td></tr>
    <tr><th>Phase-in</th><td id="out-Phase-in" data-value=""></td></tr>
    <tr><th>No status yet</th><td id="out-none" data-value=""></td></tr>
    <tr><th>Ready share</th><td><strong id="out-share" data-value=""></strong></td></tr>
  </tbody>
</table>

<h2>Datapoints in scope</h2>
<div class="tool-scroll">
<table id="points" class="tool-table">
  <thead><tr><th>Datapoint</th><th>Standard</th><th>What it covers</th><th>Dataset</th><th>Status</th></tr></thead>
  <tbody></tbody>
</table>
</div>

</div>

## How it calculates

- **In scope:** every ESRS 2 datapoint, plus the datapoints of each
  material topical standard.
- **Ready share** = Ready / datapoints in scope. A datapoint with no status
  yet counts as not ready.
- Same method as
  [`esgcalc.csrd`](https://github.com/mantas123456/esg-workflows-handbook/blob/main/esgcalc/csrd.py)
  (`datapoints_in_scope`, `gap_summary`). To add owners and dates, use the
  [ESRS gap list workbook](../downloads/esrs-gap-list.xlsx).

<!-- generated tool data: esrs-gap-data: do not edit by hand -->
<script type="application/json" id="esrs-gap-data">
{
 "datapoints": [
  {
   "dataset": null,
   "description": "Basis for preparation, including any phase-in used",
   "id": "ESRS2-basis",
   "standard": "ESRS 2"
  },
  {
   "dataset": null,
   "description": "Who oversees sustainability matters, and how",
   "id": "ESRS2-governance",
   "standard": "ESRS 2"
  },
  {
   "dataset": null,
   "description": "Strategy, business model and value chain, including financial effects",
   "id": "ESRS2-strategy",
   "standard": "ESRS 2"
  },
  {
   "dataset": null,
   "description": "How the double materiality assessment was done, covering own operations and the value chain",
   "id": "ESRS2-materiality-process",
   "standard": "ESRS 2"
  },
  {
   "dataset": null,
   "description": "Transition plan for climate change mitigation",
   "id": "E1-transition-plan",
   "standard": "E1"
  },
  {
   "dataset": null,
   "description": "GHG reduction targets",
   "id": "E1-targets",
   "standard": "E1"
  },
  {
   "dataset": "electricity_use",
   "description": "Energy consumption and mix",
   "id": "E1-energy",
   "standard": "E1"
  },
  {
   "dataset": "fuel_use",
   "description": "Gross Scope 1 GHG emissions",
   "id": "E1-scope1",
   "standard": "E1"
  },
  {
   "dataset": "electricity_use",
   "description": "Gross Scope 2 GHG emissions, location-based and market-based",
   "id": "E1-scope2",
   "standard": "E1"
  },
  {
   "dataset": "purchased_goods_spend",
   "description": "Gross Scope 3 GHG emissions, in total and for each significant category",
   "id": "E1-scope3",
   "standard": "E1"
  },
  {
   "dataset": "supplier_emissions",
   "description": "Supplier-specific data used for significant Scope 3 categories",
   "id": "E1-scope3-suppliers",
   "standard": "E1"
  },
  {
   "dataset": null,
   "description": "Anticipated financial effects of climate risks and opportunities (phase-in applies)",
   "id": "E1-financial-effects",
   "standard": "E1"
  },
  {
   "dataset": null,
   "description": "Pollution of air, water and soil",
   "id": "E2-pollution",
   "standard": "E2"
  },
  {
   "dataset": null,
   "description": "Substances of concern (phase-in applies)",
   "id": "E2-substances-of-concern",
   "standard": "E2"
  },
  {
   "dataset": null,
   "description": "Water and marine resources",
   "id": "E3-water",
   "standard": "E3"
  },
  {
   "dataset": null,
   "description": "Biodiversity and ecosystems (phase-in applies)",
   "id": "E4-biodiversity",
   "standard": "E4"
  },
  {
   "dataset": "imports_by_cn_code",
   "description": "Resource use, circular economy and waste",
   "id": "E5-resources-waste",
   "standard": "E5"
  },
  {
   "dataset": "headcount",
   "description": "Employees by contract type, gender and country",
   "id": "S1-headcount",
   "standard": "S1"
  },
  {
   "dataset": "headcount",
   "description": "Health and safety of the own workforce (phase-in applies to some datapoints)",
   "id": "S1-health-safety",
   "standard": "S1"
  },
  {
   "dataset": null,
   "description": "Workers in the value chain (phase-in applies)",
   "id": "S2-value-chain-workers",
   "standard": "S2"
  },
  {
   "dataset": null,
   "description": "Affected communities (phase-in applies)",
   "id": "S3-communities",
   "standard": "S3"
  },
  {
   "dataset": null,
   "description": "Consumers and end-users (phase-in applies)",
   "id": "S4-consumers",
   "standard": "S4"
  },
  {
   "dataset": null,
   "description": "Business conduct, including corruption and bribery",
   "id": "G1-business-conduct",
   "standard": "G1"
  }
 ],
 "example": {
  "material": [
   "E1",
   "E5",
   "S1"
  ],
  "status": {
   "E1-energy": "Ready",
   "E1-financial-effects": "Phase-in",
   "E1-scope1": "Ready",
   "E1-scope2": "Ready",
   "E1-scope3": "Partial",
   "E1-scope3-suppliers": "Partial",
   "E1-targets": "Gap",
   "E1-transition-plan": "Gap",
   "E5-resources-waste": "Partial",
   "ESRS2-basis": "Gap",
   "ESRS2-governance": "Partial",
   "ESRS2-materiality-process": "Ready",
   "ESRS2-strategy": "Partial",
   "S1-headcount": "Ready",
   "S1-health-safety": "Ready"
  }
 },
 "standards": [
  {
   "kind": "cross-cutting",
   "standard": "ESRS 2",
   "topic": "General disclosures"
  },
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
<!-- end generated tool data: esrs-gap-data -->

<script src="../esrs-gap.js"></script>
