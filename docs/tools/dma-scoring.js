/*
 * Double materiality scoring for the ESG Workflows Handbook.
 * A port of esgcalc.dma (assess, topics). Runs in the browser: no network requests, no storage.
 * Not legal advice. Licence: MIT.
 */
(function () {
  "use strict";

  var DATA = JSON.parse(document.getElementById("dma-scoring-data").textContent);
  var P = DATA.params;
  var tbody = document.querySelector("#items tbody");
  var SCORES = ["scale", "scope", "irremediability", "likelihood", "magnitude"];

  // ------------------------------------------------------------ calculation (same as esgcalc)

  function check(name, value, p, iro) {
    var lo = p.scale.min, hi = p.scale.max;
    if (value === null || value === undefined) throw new Error(iro.id + ": " + name + " is needed for this kind of IRO");
    if (typeof value !== "number" || Math.floor(value) !== value || value < lo || value > hi) {
      throw new Error(iro.id + ": " + name + " must be a whole number from " + lo + " to " + hi);
    }
    return value;
  }

  function severity(iro, p) {
    var v = ["scale", "scope", "irremediability"].map(function (n) { return check(n, iro[n], p, iro); });
    if (p.severity_aggregation === "max") return Math.max.apply(null, v);
    if (p.severity_aggregation === "mean") return (v[0] + v[1] + v[2]) / 3;
    throw new Error("unknown severity_aggregation " + p.severity_aggregation);
  }

  function assess(iro, p) {
    p = p || P;
    var top = p.scale.max, score, lik;
    if (iro.kind === "impact") {
      if (iro.negative) {
        var sev = severity(iro, p);
        if (iro.actual) {
          score = sev;
        } else {
          lik = check("likelihood", iro.likelihood, p, iro);
          score = (iro.human_rights && sev >= p.human_rights.severity_precedence_from) ? sev : sev * lik / top;
        }
      } else {
        var base = (check("scale", iro.scale, p, iro) + check("scope", iro.scope, p, iro)) / 2;
        if (iro.actual) {
          score = base;
        } else {
          lik = check("likelihood", iro.likelihood, p, iro);
          score = base * lik / top;
        }
      }
      return { id: iro.id, score: score, material: score >= p.thresholds.impact, dimension: "impact" };
    }
    if (iro.kind === "risk" || iro.kind === "opportunity") {
      var mag = check("magnitude", iro.magnitude, p, iro);
      lik = check("likelihood", iro.likelihood, p, iro);
      score = mag * lik / top;
      return { id: iro.id, score: score, material: score >= p.thresholds.financial, dimension: "financial" };
    }
    throw new Error(iro.id + ": unknown kind " + iro.kind);
  }

  function topics(iros, assessed) {
    var by = {};
    assessed.forEach(function (a, i) {
      var t = iros[i].topic;
      if (!by[t]) by[t] = { topic: t, impact_material: false, financial_material: false, iros: [] };
      by[t].iros.push(a.id);
      if (a.material) by[t][a.dimension + "_material"] = true;
    });
    return Object.keys(by).sort().map(function (k) {
      var t = by[k];
      t.iros.sort();
      t.material = t.impact_material || t.financial_material;
      return t;
    });
  }

  // ------------------------------------------------------------ page

  function cell(tr, el) { var td = document.createElement("td"); td.appendChild(el); tr.appendChild(td); return el; }

  function input(type, name, label) {
    var el = document.createElement("input");
    el.type = type; el.name = name; el.setAttribute("aria-label", label);
    if (type === "number") { el.min = P.scale.min; el.max = P.scale.max; el.step = 1; el.style.width = "3.5rem"; }
    return el;
  }

  function select(name, options, label) {
    var el = document.createElement("select");
    el.name = name; el.setAttribute("aria-label", label);
    options.forEach(function (o) {
      var opt = document.createElement("option"); opt.value = o[0]; opt.textContent = o[1]; el.appendChild(opt);
    });
    return el;
  }

  function addRow(iro) {
    iro = iro || {};
    var tr = document.createElement("tr");
    cell(tr, input("text", "id", "ID")).value = iro.id || "";
    cell(tr, select("topic", DATA.standards.map(function (s) { return [s.standard, s.standard]; }), "Standard")).value = iro.topic || "E1";
    cell(tr, input("text", "description", "Description")).value = iro.description || "";
    cell(tr, select("kind", [["impact", "Impact"], ["risk", "Risk"], ["opportunity", "Opportunity"]], "Type")).value = iro.kind || "impact";
    cell(tr, input("checkbox", "negative", "Negative")).checked = iro.negative !== false;
    cell(tr, input("checkbox", "actual", "Actual")).checked = !!iro.actual;
    cell(tr, input("checkbox", "human_rights", "Human rights")).checked = !!iro.human_rights;
    SCORES.forEach(function (n) {
      var el = cell(tr, input("number", n, n));
      el.value = iro[n] === null || iro[n] === undefined ? "" : String(iro[n]);
    });
    var score = document.createElement("td"); score.className = "out-score"; tr.appendChild(score);
    var mat = document.createElement("td"); mat.className = "out-material"; tr.appendChild(mat);
    tbody.appendChild(tr);
  }

  function readRow(tr, i) {
    function f(n) { return tr.querySelector("[name='" + n + "']"); }
    var iro = {
      id: f("id").value.trim() || "Row " + (i + 1), topic: f("topic").value, description: f("description").value,
      kind: f("kind").value, negative: f("negative").checked, actual: f("actual").checked,
      human_rights: f("human_rights").checked
    };
    SCORES.forEach(function (n) { var v = f(n).value; iro[n] = v === "" ? null : Number(v); });
    return iro;
  }

  function update() {
    var iros = [], assessed = [];
    Array.prototype.forEach.call(tbody.rows, function (tr, i) {
      var iro = readRow(tr, i);
      var s = tr.querySelector(".out-score"), m = tr.querySelector(".out-material");
      try {
        var a = assess(iro);
        iros.push(iro); assessed.push(a);
        s.textContent = a.score.toFixed(1); s.setAttribute("data-value", String(a.score));
        m.textContent = a.material ? "Yes" : "No";
        tr.className = a.material ? "tool-significant" : "";
      } catch (e) {
        s.textContent = e.message.replace(/^[^:]*: /, ""); s.setAttribute("data-value", "");
        m.textContent = ""; tr.className = "";
      }
      tr.setAttribute("data-id", iro.id);
    });
    var res = {};
    topics(iros, assessed).forEach(function (t) { res[t.topic] = t; });
    var tb = document.querySelector("#topics tbody");
    tb.innerHTML = "";
    var material = [];
    DATA.standards.forEach(function (s) {
      var t = res[s.standard], tr = document.createElement("tr");
      tr.setAttribute("data-standard", s.standard);
      [s.standard, s.topic, t ? String(t.iros.length) : "0",
       t && t.impact_material ? "Yes" : "No", t && t.financial_material ? "Yes" : "No",
       t && t.material ? "Yes" : "No"].forEach(function (v) {
        var td = document.createElement("td"); td.textContent = v; tr.appendChild(td);
      });
      if (t && t.material) { material.push(s.standard); tr.className = "tool-significant"; }
      tb.appendChild(tr);
    });
    document.getElementById("topics").setAttribute("data-material", material.join(","));
    var n = assessed.filter(function (a) { return a.material; }).length;
    var sum = document.getElementById("summary");
    sum.textContent = n + " of " + assessed.length + " items material; material topics: " + (material.join(", ") || "none") + ".";
    sum.setAttribute("data-value", String(n));
  }

  function clearRows() { tbody.innerHTML = ""; }

  document.getElementById("add-row").addEventListener("click", function () { addRow(); update(); });
  document.getElementById("load-example").addEventListener("click", function () {
    clearRows(); DATA.example.forEach(addRow); update();
  });
  document.getElementById("clear").addEventListener("click", function () { clearRows(); addRow(); update(); });
  var app = document.getElementById("dma-app");
  app.addEventListener("input", update);
  app.addEventListener("change", update);

  addRow();
  update();
  app.setAttribute("data-ready", "true");
  window.dmaScoring = { assess: assess, topics: topics, params: P };
})();
