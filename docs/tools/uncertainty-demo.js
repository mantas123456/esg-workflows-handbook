/*
 * Uncertainty demo for the ESG Workflows Handbook.
 * Sum rule as in esgcalc.quality.sum_uncertainty; Monte Carlo as in
 * esgcalc.quality.monte_carlo_sum with gsd_from_u95, but with its own seeded
 * random generator (mulberry32 + Box-Muller), so results match esgcalc within
 * sampling noise, not to the digit. No network requests, no storage. MIT licence.
 */
(function () {
  "use strict";

  var DATA = JSON.parse(document.getElementById("uncertainty-demo-data").textContent);
  var Z95 = 1.959964;
  var tbody = document.querySelector("#lines tbody");

  // ------------------------------------------------------------ calculations

  function sumUncertainty(lines) {
    var total = 0, sq = 0;
    lines.forEach(function (l) { total += l.value; sq += Math.pow(l.value * l.u95, 2); });
    var u = Math.sqrt(sq);
    return { value: total, u95_abs: u, u95_rel: total ? u / total : Infinity };
  }

  function gsdFromU95(u) { return Math.pow(1 + u, 1 / Z95); }

  function mulberry32(seed) {
    var a = seed >>> 0;
    return function () {
      a = (a + 0x6D2B79F5) >>> 0;
      var t = a;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  function percentile(sorted, p) {      // linear interpolation, as numpy's default
    var idx = (sorted.length - 1) * p, lo = Math.floor(idx), hi = Math.ceil(idx);
    return sorted[lo] + (sorted[hi] - sorted[lo]) * (idx - lo);
  }

  function monteCarlo(lines, n, seed) {
    var rand = mulberry32(seed);
    var sigmas = lines.map(function (l) { return Math.log(gsdFromU95(l.u95)); });
    var totals = new Float64Array(n), spare = null, sum = 0;
    function normal() {
      if (spare !== null) { var s = spare; spare = null; return s; }
      var u1 = 0;
      while (u1 === 0) u1 = rand();
      var r = Math.sqrt(-2 * Math.log(u1)), th = 2 * Math.PI * rand();
      spare = r * Math.sin(th);
      return r * Math.cos(th);
    }
    for (var i = 0; i < n; i++) {
      var t = 0;
      for (var j = 0; j < lines.length; j++) t += lines[j].value * Math.exp(sigmas[j] * normal());
      totals[i] = t; sum += t;
    }
    var sorted = Array.prototype.slice.call(totals).sort(function (a, b) { return a - b; });
    return { mean: sum / n, median: percentile(sorted, 0.5), low: percentile(sorted, 0.025),
             high: percentile(sorted, 0.975), sorted: sorted };
  }

  // ------------------------------------------------------------ page

  function fmt(x) { return x.toLocaleString("en-GB", { minimumFractionDigits: 1, maximumFractionDigits: 1 }); }

  function addLine(l) {
    l = l || { name: "", value: "", u95: "" };
    var tr = document.createElement("tr");
    tr.innerHTML = "<td><input type='text' name='name' aria-label='line name'></td>" +
      "<td><input type='number' name='value' min='0' step='any' aria-label='value'></td>" +
      "<td><input type='number' name='u95' min='0' step='any' aria-label='uncertainty'></td>" +
      "<td><button type='button' class='md-button tool-remove'>Remove</button></td>";
    tr.querySelector("[name='name']").value = l.name;
    tr.querySelector("[name='value']").value = l.value;
    tr.querySelector("[name='u95']").value = l.u95 === "" ? "" : +(l.u95 * 100).toFixed(4);
    tr.querySelector("button").addEventListener("click", function () { tr.remove(); });
    tbody.appendChild(tr);
  }

  function read() {
    var lines = [], errors = [];
    Array.prototype.forEach.call(tbody.rows, function (tr, i) {
      var v = tr.querySelector("[name='value']").value, u = tr.querySelector("[name='u95']").value;
      if (v === "" && u === "") return;
      v = Number(v); u = Number(u) / 100;
      if (!(v >= 0) || !(u >= 0)) errors.push("Line " + (i + 1) + ": enter a value and an uncertainty of zero or more.");
      lines.push({ name: tr.querySelector("[name='name']").value, value: v, u95: u });
    });
    var n = Number(document.getElementById("draws").value), seed = Number(document.getElementById("seed").value);
    if (!(n >= 1000 && n <= 500000)) errors.push("Draws must be between 1,000 and 500,000.");
    if (!(seed >= 1)) errors.push("The seed must be a whole number of 1 or more.");
    if (!lines.length) errors.push("Add at least one line.");
    return { lines: lines, n: Math.round(n), seed: Math.round(seed), errors: errors };
  }

  function set(id, attrs, text) {
    var el = document.getElementById(id);
    Object.keys(attrs).forEach(function (k) { el.setAttribute(k, String(attrs[k])); });
    el.textContent = text;
  }

  function histogram(sorted, low, high) {
    var svg = document.getElementById("histogram"), W = 600, H = 220, pad = 20, bins = 40;
    var min = sorted[0], max = sorted[sorted.length - 1], width = (max - min) / bins || 1;
    var counts = new Array(bins).fill(0);
    sorted.forEach(function (x) { counts[Math.min(bins - 1, Math.floor((x - min) / width))] += 1; });
    var top = Math.max.apply(null, counts), bw = (W - 2 * pad) / bins, parts = [];
    counts.forEach(function (c, i) {
      var h = (H - 2 * pad) * c / top, x = pad + i * bw, mid = min + (i + 0.5) * width;
      var inside = mid >= low && mid <= high;
      parts.push("<rect x='" + x.toFixed(1) + "' y='" + (H - pad - h).toFixed(1) + "' width='" + (bw - 1).toFixed(1) +
                 "' height='" + h.toFixed(1) + "' class='" + (inside ? "bar-in" : "bar-out") + "'></rect>");
    });
    parts.push("<text x='" + pad + "' y='" + (H - 4) + "' class='axis'>" + fmt(min) + "</text>");
    parts.push("<text x='" + (W - pad) + "' y='" + (H - 4) + "' class='axis' text-anchor='end'>" + fmt(max) + "</text>");
    svg.innerHTML = parts.join("");
    svg.setAttribute("data-bins", String(bins));
  }

  function run() {
    var s = read();
    document.getElementById("errors").textContent = s.errors.join(" ");
    if (s.errors.length) return;
    var a = sumUncertainty(s.lines);
    set("sum-value", { "data-value": a.value }, fmt(a.value));
    set("sum-interval", { "data-low": a.value - a.u95_abs, "data-high": a.value + a.u95_abs },
        fmt(a.value - a.u95_abs) + " to " + fmt(a.value + a.u95_abs));
    set("sum-rel", { "data-value": a.u95_rel }, "±" + (a.u95_rel * 100).toFixed(1) + "%");
    var mc = monteCarlo(s.lines, s.n, s.seed);
    set("mc-median", { "data-value": mc.median }, fmt(mc.median) + " (median)");
    set("mc-interval", { "data-low": mc.low, "data-high": mc.high }, fmt(mc.low) + " to " + fmt(mc.high));
    set("mc-mean", { "data-value": mc.mean }, "mean " + fmt(mc.mean));
    histogram(mc.sorted, mc.low, mc.high);
  }

  function loadExample() {
    tbody.innerHTML = "";
    DATA.example.lines.forEach(addLine);
    document.getElementById("draws").value = DATA.example.draws;
    document.getElementById("seed").value = DATA.example.seed;
    run();
  }

  document.getElementById("run").addEventListener("click", run);
  document.getElementById("add-line").addEventListener("click", function () { addLine(); });
  document.getElementById("load-example").addEventListener("click", loadExample);

  addLine();
  document.getElementById("uncertainty-app").setAttribute("data-ready", "true");
  window.uncertaintyDemo = { sumUncertainty: sumUncertainty, gsdFromU95: gsdFromU95, monteCarlo: monteCarlo };
})();
