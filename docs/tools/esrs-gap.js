/*
 * ESRS datapoint gap check for the ESG Workflows Handbook.
 * A port of esgcalc.csrd (datapoints_in_scope, gap_summary). Runs in the browser:
 * no network requests, no storage. Not legal advice. Licence: MIT.
 */
(function () {
  "use strict";

  var DATA = JSON.parse(document.getElementById("esrs-gap-data").textContent);
  var STATUSES = ["Ready", "Partial", "Gap", "Phase-in"];
  var tbody = document.querySelector("#points tbody");
  var status = {};          // datapoint id -> status, kept when a topic is unticked and ticked again

  // ------------------------------------------------------------ calculation (same as esgcalc)

  function datapointsInScope(datapoints, materialStandards) {
    return datapoints.filter(function (d) {
      return d.standard === "ESRS 2" || materialStandards.indexOf(d.standard) >= 0;
    });
  }

  function gapSummary(inScope, st) {
    var ids = inScope.map(function (d) { return d.id; });
    var missing = ids.filter(function (i) { return !(i in st); });
    var extra = Object.keys(st).filter(function (i) { return ids.indexOf(i) < 0; });
    if (missing.length || extra.length) throw new Error("status must cover exactly the datapoints in scope");
    Object.keys(st).forEach(function (i) {
      if (STATUSES.indexOf(st[i]) < 0) throw new Error("unknown status " + st[i]);
    });
    var counts = {};
    STATUSES.forEach(function (s) { counts[s] = ids.filter(function (i) { return st[i] === s; }).length; });
    return { counts: counts, total: ids.length, ready_share: ids.length ? counts.Ready / ids.length : 0 };
  }

  // ------------------------------------------------------------ page

  var box = document.getElementById("standards");
  DATA.standards.filter(function (s) { return s.kind === "topical"; }).forEach(function (s) {
    var label = document.createElement("label");
    label.className = "tool-field";
    var cb = document.createElement("input");
    cb.type = "checkbox"; cb.name = "material"; cb.value = s.standard;
    label.appendChild(cb);
    label.appendChild(document.createTextNode(" " + s.standard + " " + s.topic));
    box.appendChild(label);
  });

  function material() {
    return Array.prototype.map.call(box.querySelectorAll("input:checked"), function (c) { return c.value; });
  }

  function render() {
    var scope = datapointsInScope(DATA.datapoints, material());
    tbody.innerHTML = "";
    scope.forEach(function (d) {
      var tr = document.createElement("tr");
      tr.setAttribute("data-id", d.id);
      [d.id, d.standard, d.description, d.dataset || "–"].forEach(function (v) {
        var td = document.createElement("td"); td.textContent = v; tr.appendChild(td);
      });
      var td = document.createElement("td");
      var sel = document.createElement("select");
      sel.name = "status"; sel.setAttribute("aria-label", "Status of " + d.id); sel.setAttribute("data-id", d.id);
      [""].concat(STATUSES).forEach(function (s) {
        var o = document.createElement("option"); o.value = s; o.textContent = s || "Choose"; sel.appendChild(o);
      });
      sel.value = status[d.id] || "";
      td.appendChild(sel); tr.appendChild(td);
      tbody.appendChild(tr);
    });
    update();
  }

  function out(id, text, value) {
    var el = document.getElementById(id);
    el.textContent = text; el.setAttribute("data-value", String(value));
  }

  function update() {
    var scope = datapointsInScope(DATA.datapoints, material());
    var st = {};
    scope.forEach(function (d) { if (status[d.id]) st[d.id] = status[d.id]; });
    // datapoints without a status yet count as not ready: summarise those that have one,
    // over the whole scope
    var withStatus = scope.filter(function (d) { return st[d.id]; });
    var s = gapSummary(withStatus, st);
    var none = scope.length - withStatus.length;
    out("out-total", String(scope.length), scope.length);
    STATUSES.forEach(function (k) { out("out-" + k, String(s.counts[k]), s.counts[k]); });
    out("out-none", String(none), none);
    var share = scope.length ? s.counts.Ready / scope.length : 0;
    out("out-share", (share * 100).toFixed(1) + "%", share);
  }

  tbody.addEventListener("change", function (e) {
    if (e.target.name === "status") {
      if (e.target.value) status[e.target.getAttribute("data-id")] = e.target.value;
      else delete status[e.target.getAttribute("data-id")];
      update();
    }
  });
  box.addEventListener("change", render);

  function setMaterial(list) {
    Array.prototype.forEach.call(box.querySelectorAll("input"), function (c) { c.checked = list.indexOf(c.value) >= 0; });
  }

  document.getElementById("load-example").addEventListener("click", function () {
    status = {};
    Object.keys(DATA.example.status).forEach(function (k) { status[k] = DATA.example.status[k]; });
    setMaterial(DATA.example.material);
    render();
  });
  document.getElementById("clear").addEventListener("click", function () { status = {}; setMaterial([]); render(); });

  render();
  document.getElementById("gap-app").setAttribute("data-ready", "true");
  window.esrsGap = { datapointsInScope: datapointsInScope, gapSummary: gapSummary };
})();
