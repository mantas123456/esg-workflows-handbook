---
description: A free VSME readiness check that runs in your browser. Tick the datapoints of the voluntary standard you already have; see completeness by module and a to-do list.
hide:
  - toc
---

# VSME readiness

Tick each datapoint of the voluntary standard you already have, or that does
not apply to you. The check shows how complete you are, module by module,
and lists what is still to do, grouped by disclosure. See
[V1 Choosing the modules](../vsme/v1-modules.md) and
[V2 Basic Module data collection](../vsme/v2-basic.md).

!!! danger "Not legal advice"
    A planning aid. The datapoint descriptions are this handbook's own
    words; read Annex I of Delegated Regulation (EU) 2026/1560 for the exact
    requirements. The example is the fictional Gozo Fresh Foods.

!!! info "Your data stays in your browser"
    Nothing you tick is sent anywhere or stored.

<div id="readiness-app" class="tool-app" data-ready="false" markdown="0">

<div class="tool-bar">
  <label class="tool-field">Option
    <select id="option">
      <option value="A">A: Basic Module only</option>
      <option value="B">B: Basic and Comprehensive</option>
    </select>
  </label>
  <button type="button" id="load-example" class="md-button">Load the Gozo Fresh Foods example</button>
  <button type="button" id="clear" class="md-button">Clear</button>
</div>

<table class="tool-results">
  <tbody>
    <tr><th>Basic Module</th><td id="out-basic" data-value=""></td></tr>
    <tr id="row-comprehensive"><th>Comprehensive Module</th><td id="out-comprehensive" data-value=""></td></tr>
    <tr><th>Overall</th><td><strong id="out-overall" data-value=""></strong></td></tr>
  </tbody>
</table>

<h2>Still to do</h2>
<ul id="todo" class="tool-todo"></ul>

<h2>Datapoints</h2>
<div class="tool-scroll">
<table id="points" class="tool-table">
  <thead><tr><th>Have it</th><th>Datapoint</th><th>What it covers</th></tr></thead>
  <tbody></tbody>
</table>
</div>

</div>

## How it calculates

- **Completeness** of a module = datapoints ticked / datapoints in the
  module.
- Option A counts the Basic Module only; Option B counts both.
- The to-do list shows every unticked datapoint, under its disclosure.

<!-- generated tool data: vsme-readiness-data: do not edit by hand -->
<script type="application/json" id="vsme-readiness-data">
{
 "datapoints": [
  {
   "description": "Which option is used: Basic only (A) or Basic and Comprehensive (B), with a statement of compliance",
   "disclosure": "B1",
   "id": "B1-option",
   "module": "basic"
  },
  {
   "description": "Basis for preparation: consolidated or individual, the entities and sites covered",
   "disclosure": "B1",
   "id": "B1-basis",
   "module": "basic"
  },
  {
   "description": "Practices, policies and future plans for moving towards a more sustainable economy",
   "disclosure": "B2",
   "id": "B2-practices",
   "module": "basic"
  },
  {
   "description": "Total energy consumption, split into renewable and non-renewable where the data can be obtained",
   "disclosure": "B3",
   "id": "B3-energy",
   "module": "basic"
  },
  {
   "description": "Energy from fuels, part of total energy consumption",
   "disclosure": "B3",
   "id": "B3-energy-fuels",
   "module": "basic"
  },
  {
   "description": "Gross Scope 1 GHG emissions, following the GHG Protocol Corporate Standard",
   "disclosure": "B3",
   "id": "B3-scope1",
   "module": "basic"
  },
  {
   "description": "Gross location-based Scope 2 GHG emissions",
   "disclosure": "B3",
   "id": "B3-scope2-location",
   "module": "basic"
  },
  {
   "description": "GHG intensity: total GHG emissions divided by turnover",
   "disclosure": "B3",
   "id": "B3-intensity",
   "module": "basic"
  },
  {
   "description": "Emissions of pollutants to air, water and soil, where the undertaking already reports them under law or an environmental management system",
   "disclosure": "B4",
   "id": "B4-pollution",
   "module": "basic"
  },
  {
   "description": "Number and area of sites owned, leased or managed in or near biodiversity-sensitive areas",
   "disclosure": "B5",
   "id": "B5-sensitive-sites",
   "module": "basic"
  },
  {
   "description": "Land use: total, sealed and nature-oriented area (optional)",
   "disclosure": "B5",
   "id": "B5-land-use",
   "module": "basic"
  },
  {
   "description": "Water consumption (withdrawal minus discharge), for undertakings whose production uses water significantly",
   "disclosure": "B6",
   "id": "B6-water-consumption",
   "module": "basic"
  },
  {
   "description": "Waste generated, split into hazardous and non-hazardous",
   "disclosure": "B7",
   "id": "B7-waste",
   "module": "basic"
  },
  {
   "description": "Waste diverted to recycling or reuse",
   "disclosure": "B7",
   "id": "B7-waste-recycled",
   "module": "basic"
  },
  {
   "description": "Employees by contract type (permanent or temporary), gender and, if in more than one country, by country",
   "disclosure": "B8",
   "id": "B8-employees",
   "module": "basic"
  },
  {
   "description": "Employee turnover rate, for undertakings with 50 or more employees",
   "disclosure": "B8",
   "id": "B8-turnover-rate",
   "module": "basic"
  },
  {
   "description": "Number and rate of recordable work-related accidents (per 100 full-time workers, based on 2,000 hours a year)",
   "disclosure": "B9",
   "id": "B9-accidents",
   "module": "basic"
  },
  {
   "description": "Fatalities from work-related injuries and ill health",
   "disclosure": "B9",
   "id": "B9-fatalities",
   "module": "basic"
  },
  {
   "description": "Gender pay gap (may be left out below 150 employees; below 100 from 7 June 2031)",
   "disclosure": "B10",
   "id": "B10-pay-gap",
   "module": "basic"
  },
  {
   "description": "Share of employees covered by collective bargaining agreements",
   "disclosure": "B10",
   "id": "B10-collective-bargaining",
   "module": "basic"
  },
  {
   "description": "Average annual training hours per employee, by gender",
   "disclosure": "B10",
   "id": "B10-training",
   "module": "basic"
  },
  {
   "description": "Convictions and total fines for breaches of anti-corruption and anti-bribery laws",
   "disclosure": "B11",
   "id": "B11-corruption",
   "module": "basic"
  },
  {
   "description": "Business model and sustainability-related initiatives (some parts voluntary for 10 employees or fewer)",
   "disclosure": "C1",
   "id": "C1-business-model",
   "module": "comprehensive"
  },
  {
   "description": "More detail on the practices, policies and future plans reported in B2",
   "disclosure": "C2",
   "id": "C2-practices",
   "module": "comprehensive"
  },
  {
   "description": "GHG reduction targets and climate transition",
   "disclosure": "C3",
   "id": "C3-targets",
   "module": "comprehensive"
  },
  {
   "description": "Climate-related hazards and transition risks, and how the undertaking responds",
   "disclosure": "C4",
   "id": "C4-climate-risks",
   "module": "comprehensive"
  },
  {
   "description": "More characteristics of the workforce",
   "disclosure": "C5",
   "id": "C5-workforce",
   "module": "comprehensive"
  },
  {
   "description": "Human rights policies and processes for the own workforce",
   "disclosure": "C6",
   "id": "C6-human-rights-policies",
   "module": "comprehensive"
  },
  {
   "description": "Human rights incidents involving the workforce or the value chain",
   "disclosure": "C7",
   "id": "C7-human-rights-incidents",
   "module": "comprehensive"
  },
  {
   "description": "Revenues from certain activities",
   "disclosure": "C8",
   "id": "C8-revenues",
   "module": "comprehensive"
  },
  {
   "description": "Gender diversity ratio in the governance body",
   "disclosure": "C9",
   "id": "C9-board-gender",
   "module": "comprehensive"
  }
 ],
 "example": {
  "done": [
   "B1-option",
   "B1-basis",
   "B2-practices",
   "B3-energy",
   "B3-energy-fuels",
   "B3-scope1",
   "B3-scope2-location",
   "B3-intensity",
   "B4-pollution",
   "B5-sensitive-sites",
   "B6-water-consumption",
   "B7-waste",
   "B7-waste-recycled",
   "B8-employees",
   "B8-turnover-rate",
   "B9-accidents",
   "B9-fatalities",
   "B10-pay-gap",
   "B10-collective-bargaining",
   "B10-training",
   "B11-corruption",
   "C1-business-model",
   "C5-workforce",
   "C7-human-rights-incidents",
   "C9-board-gender"
  ],
  "option": "B"
 },
 "topics": {
  "B1": "Basis for preparation",
  "B10": "Workforce: pay, collective bargaining and training",
  "B11": "Corruption and bribery",
  "B2": "Sustainability practices and plans",
  "B3": "Energy and greenhouse gases",
  "B4": "Pollution of air, water and soil",
  "B5": "Biodiversity",
  "B6": "Water",
  "B7": "Waste and resource use",
  "B8": "Workforce: general characteristics",
  "B9": "Workforce: health and safety",
  "C1": "Business model and sustainability initiatives",
  "C2": "Practices and plans in more detail",
  "C3": "GHG reduction targets and climate transition",
  "C4": "Climate risks",
  "C5": "Workforce: more characteristics",
  "C6": "Human rights policies and processes",
  "C7": "Human rights incidents",
  "C8": "Revenues from certain activities",
  "C9": "Gender diversity in the governance body"
 }
}
</script>
<!-- end generated tool data: vsme-readiness-data -->

<script src="../vsme-readiness.js"></script>
