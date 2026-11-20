/*
 * CBAM calculator for the ESG Workflows Handbook.
 *
 * A port of esgcalc/cbam.py: threshold_check, default_value_with_markup,
 * certificates_needed, certificate_cost and quarterly_holding. Parameters come
 * from the JSON block on the page, generated from data/cbam_parameters.yml.
 * Runs entirely in the browser: no network requests, no storage.
 * Not legal advice. Licence: MIT.
 */
(function () {
  "use strict";

  var DATA = JSON.parse(document.getElementById("cbam-tool-data").textContent);
  var P = DATA.params;
  var SECTORS = ["cement", "fertilisers", "iron_steel", "aluminium", "hydrogen"];
  var QUARTERS = ["Q1", "Q2", "Q3", "Q4"];
  var SCALE = 1000000; // masses summed as integer micro-tonnes, so 45 x 1.1 + 0.5 is exactly 50

  // ------------------------------------------------------------ calculations (same as esgcalc)

  function normaliseCn(code) {
    var c = String(code || "").replace(/[\s.]/g, "");
    if (!/^\d+$/.test(c)) throw new Error("CN code must contain digits only: " + code);
    return c;
  }

  function thresholdCheck(lines) {
    var totalMicro = 0;
    var excluded = [];
    lines.forEach(function (l) {
      var code = normaliseCn(l.cn_code);
      if (Object.prototype.hasOwnProperty.call(P.excluded_cn_codes, code)) {
        if (excluded.indexOf(code) < 0) excluded.push(code);
      } else {
        totalMicro += Math.round(l.mass_t * SCALE);
      }
    });
    return {
      total_mass_t: totalMicro / SCALE,
      above: totalMicro > P.max_exempt_mass_t * SCALE,
      excluded: excluded.sort()
    };
  }

  function markup(year, sector) {
    var years = Object.keys(P.markup_by_year).map(Number);
    var first = Math.min.apply(null, years), last = Math.max.apply(null, years);
    if (year < first) throw new Error("Default values with mark-up apply from " + first);
    if (Object.prototype.hasOwnProperty.call(P.sector_markup, sector)) return P.sector_markup[sector];
    return P.markup_by_year[String(Math.min(year, last))];
  }

  function lineSee(l, year) {
    if (l.basis === "actual") return l.actual_see;
    return l.base_default * (1 + markup(year, l.sector));
  }

  function certificatesNeeded(embedded, fa, cpp) {
    return Math.max(0, embedded - fa - cpp) / P.tco2e_per_certificate;
  }

  // certificates x price, rounded half up to the cent, in exact decimal arithmetic
  function certificateCost(certs, price) {
    var c = BigInt(Math.round(certs * 1e6));   // 6 decimals
    var p = BigInt(Math.round(price * 1e4));   // 4 decimals
    var product = c * p;                       // 10 decimals
    var cents = (product + 50000000n) / 100000000n;
    return Number(cents) / 100;
  }

  function quarterlyHolding(emissionsYtd, year, faYtd) {
    if (year < P.holding_from_year) return null;
    return P.holding_min_share * Math.max(0, emissionsYtd - faYtd) / P.tco2e_per_certificate;
  }

  function calculate(state) {
    var errors = [];
    var lines = state.lines.filter(function (l) { return l.cn_code !== "" || l.mass_t !== null; });
    lines.forEach(function (l, i) {
      var row = "Line " + (i + 1) + ": ";
      try { normaliseCn(l.cn_code); } catch (e) { errors.push(row + e.message); }
      if (l.mass_t === null || l.mass_t < 0) errors.push(row + "enter a net mass of zero or more.");
      var excluded = false;
      try { excluded = P.excluded_cn_codes[normaliseCn(l.cn_code)] === "electricity"; } catch (e) { /* reported above */ }
      if (excluded) errors.push(row + "electricity uses a separate method and is not covered by this calculator.");
      if (l.basis === "actual" && (l.actual_see === null || l.actual_see < 0)) errors.push(row + "enter the actual SEE.");
      if (l.basis === "default" && (l.base_default === null || l.base_default < 0)) errors.push(row + "enter the base default value.");
      if (l.fa_per_t !== null && l.fa_per_t < 0) errors.push(row + "the free allocation adjustment cannot be negative.");
    });
    if (state.year === null || state.year < 2026) errors.push("Enter a year of import from 2026.");
    if (state.price !== null && state.price < 0) errors.push("The price cannot be negative.");
    if (state.cpp < 0) errors.push("The carbon price paid reduction cannot be negative.");
    if (errors.length) return { errors: errors };

    var threshold = thresholdCheck(lines);
    var embedded = 0, fa = 0;
    var perLine = lines.map(function (l) {
      var e = l.mass_t * lineSee(l, state.year);
      embedded += e;
      fa += l.mass_t * (l.fa_per_t || 0);
      return e;
    });
    var certs = certificatesNeeded(embedded, fa, state.cpp);
    var cost = state.price === null ? null : certificateCost(certs, state.price);

    var holding = [];
    if (state.year >= P.holding_from_year) {
      var eYtd = 0, fYtd = 0;
      QUARTERS.forEach(function (q) {
        lines.filter(function (l) { return l.quarter === q; }).forEach(function (l) {
          var see = l.base_default !== null ? l.base_default : l.actual_see;
          eYtd += l.mass_t * see;
          fYtd += l.mass_t * (l.fa_per_t || 0);
        });
        holding.push({ quarter: q, emissions: eYtd, fa: fYtd, min: quarterlyHolding(eYtd, state.year, fYtd) });
      });
    }
    return { errors: [], threshold: threshold, perLine: perLine, embedded: embedded, fa: fa,
             certs: certs, cost: cost, holding: holding };
  }

  // ------------------------------------------------------------ page

  var tbody = document.querySelector("#lines tbody");

  function num(v) {
    if (v === "" || v === null || v === undefined) return null;
    var n = Number(v);
    return isNaN(n) ? null : n;
  }

  function fmt(x) {
    return (Math.round(x * 1e6) / 1e6).toLocaleString("en-GB", { maximumFractionDigits: 6 });
  }

  function option(value, label, selected) {
    var o = document.createElement("option");
    o.value = value; o.textContent = label; o.selected = value === selected;
    return o;
  }

  function addLine(line) {
    line = line || { quarter: "Q1", cn_code: "", sector: "iron_steel", mass_t: "", basis: "default",
                     actual_see: "", base_default: "", fa_per_t: "" };
    var tr = document.createElement("tr");
    function cell(el) { var td = document.createElement("td"); td.appendChild(el); tr.appendChild(td); return el; }
    function input(name, value, type) {
      var i = document.createElement("input");
      i.type = type || "number"; i.name = name; i.step = "any"; i.min = "0";
      i.value = value === null || value === undefined ? "" : value;
      i.setAttribute("aria-label", name);
      return cell(i);
    }
    var q = cell(document.createElement("select")); q.name = "quarter"; q.setAttribute("aria-label", "quarter");
    QUARTERS.forEach(function (x) { q.appendChild(option(x, x, line.quarter)); });
    input("cn_code", line.cn_code, "text");
    var s = cell(document.createElement("select")); s.name = "sector"; s.setAttribute("aria-label", "sector");
    SECTORS.forEach(function (x) { s.appendChild(option(x, x.replace("_", " and "), line.sector)); });
    input("mass_t", line.mass_t);
    var b = cell(document.createElement("select")); b.name = "basis"; b.setAttribute("aria-label", "basis");
    b.appendChild(option("actual", "Actual (verified)", line.basis));
    b.appendChild(option("default", "Default", line.basis));
    input("actual_see", line.actual_see);
    input("base_default", line.base_default);
    input("fa_per_t", line.fa_per_t);
    var out = document.createElement("span"); out.className = "line-embedded"; cell(out);
    var del = document.createElement("button");
    del.type = "button"; del.className = "md-button tool-remove"; del.textContent = "Remove";
    del.addEventListener("click", function () { tr.remove(); update(); });
    cell(del);
    tbody.appendChild(tr);
  }

  function readState() {
    var lines = Array.prototype.map.call(tbody.rows, function (tr) {
      function v(name) { return tr.querySelector("[name='" + name + "']").value; }
      return { quarter: v("quarter"), cn_code: v("cn_code").trim(), sector: v("sector"), mass_t: num(v("mass_t")),
               basis: v("basis"), actual_see: num(v("actual_see")), base_default: num(v("base_default")),
               fa_per_t: num(v("fa_per_t")) };
    });
    return { year: num(document.getElementById("year").value), price: num(document.getElementById("price").value),
             cpp: num(document.getElementById("cpp").value) || 0, lines: lines };
  }

  function set(id, value, text) {
    var el = document.getElementById(id);
    el.setAttribute("data-value", value === null ? "" : String(value));
    el.textContent = text;
  }

  function update() {
    var state = readState();
    var r = calculate(state);
    document.getElementById("errors").textContent = r.errors.join(" ");
    var hbody = document.querySelector("#holding tbody");
    hbody.innerHTML = "";
    var spans = tbody.querySelectorAll(".line-embedded");
    if (r.errors.length) {
      ["out-total-mass", "out-threshold", "out-embedded", "out-fa", "out-certs", "out-cost"].forEach(function (id) { set(id, null, "–"); });
      spans.forEach(function (s) { s.textContent = ""; });
      return;
    }
    var used = state.lines.filter(function (l) { return l.cn_code !== "" || l.mass_t !== null; });
    var k = 0;
    state.lines.forEach(function (l, i) {
      var isUsed = used.indexOf(l) >= 0;
      spans[i].textContent = isUsed ? fmt(r.perLine[k]) : "";
      spans[i].setAttribute("data-value", isUsed ? String(r.perLine[k]) : "");
      if (isUsed) k += 1;
    });
    var t = r.threshold;
    set("out-total-mass", t.total_mass_t, fmt(t.total_mass_t));
    set("out-threshold", t.above ? "above" : "within",
        t.above ? "Above " + P.max_exempt_mass_t + " t: CBAM covers all of the year's imports"
                : P.max_exempt_mass_t + " t or less: exemption test met (declare it in each customs declaration)");
    set("out-embedded", r.embedded, fmt(r.embedded));
    set("out-fa", r.fa, fmt(r.fa));
    set("out-certs", r.certs, fmt(r.certs));
    set("out-cost", r.cost, r.cost === null ? "enter a price"
        : r.cost.toLocaleString("en-GB", { minimumFractionDigits: 2, maximumFractionDigits: 2 }));
    var notes = ["Hydrogen and electricity have no threshold: any quantity needs an authorised CBAM declarant."];
    if (t.excluded.length) notes.push("Your lines include " + t.excluded.map(function (c) { return P.excluded_cn_codes[c]; }).join(", ") + ".");
    document.getElementById("out-notes").textContent = notes.join(" ");

    var hn = document.getElementById("holding-note");
    if (state.year < P.holding_from_year) {
      hn.textContent = "The quarterly holding rule applies from " + P.holding_from_year + ".";
    } else {
      hn.textContent = "At the end of each quarter, hold at least " + P.holding_min_share * 100 +
        "% of the year-to-date requirement.";
      r.holding.forEach(function (h) {
        var tr = document.createElement("tr");
        tr.setAttribute("data-quarter", h.quarter);
        [h.quarter + " " + state.year, fmt(h.emissions), fmt(h.fa), fmt(h.min)].forEach(function (text, i) {
          var td = document.createElement("td");
          td.textContent = text;
          if (i === 3) td.setAttribute("data-value", String(h.min));
          tr.appendChild(td);
        });
        hbody.appendChild(tr);
      });
    }
  }

  function loadExample() {
    var ex = DATA.example;
    tbody.innerHTML = "";
    ex.lines.forEach(addLine);
    document.getElementById("year").value = ex.year;
    document.getElementById("price").value = ex.price_eur;
    document.getElementById("cpp").value = ex.carbon_price_paid_certificates;
    update();
  }

  document.getElementById("add-line").addEventListener("click", function () { addLine(); update(); });
  document.getElementById("load-example").addEventListener("click", loadExample);
  document.getElementById("clear").addEventListener("click", function () { tbody.innerHTML = ""; addLine(); update(); });
  document.getElementById("cbam-app").addEventListener("input", update);
  document.getElementById("cbam-app").addEventListener("change", update);

  addLine();
  update();
  document.getElementById("cbam-app").setAttribute("data-ready", "true");

  // For tests and curious readers: the same functions as esgcalc.cbam.
  window.cbamCalculator = { thresholdCheck: thresholdCheck, markup: markup, certificatesNeeded: certificatesNeeded,
                            certificateCost: certificateCost, quarterlyHolding: quarterlyHolding, calculate: calculate };
})();
