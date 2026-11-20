/*
 * Scope 3 screening tool for the ESG Workflows Handbook.
 * A port of esgcalc.scope3.screen. Runs in the browser: no network requests, no storage.
 * Not legal advice. Licence: MIT.
 */
(function () {
  "use strict";

  var DATA = JSON.parse(document.getElementById("scope3-screening-data").textContent);
  var CATS = Object.keys(DATA.categories).map(Number).sort(function (a, b) { return a - b; });
  var tbody = document.querySelector("#categories tbody");

  // ------------------------------------------------------------ calculation (same as esgcalc)

  function screen(estimates, thresholdShare, reasons) {
    if (!(thresholdShare > 0 && thresholdShare < 1)) throw new Error("The threshold must be between 0% and 100%.");
    CATS.forEach(function (c) {
      var v = estimates[c];
      if (v === null || v === undefined || isNaN(v)) throw new Error("Enter an estimate for category " + c + " (0 if it does not apply).");
      if (v < 0) throw new Error("Category " + c + ": the estimate cannot be negative.");
    });
    var total = CATS.reduce(function (s, c) { return s + estimates[c]; }, 0);
    if (total === 0) throw new Error("No emissions to screen.");
    return CATS.map(function (c) {
      var share = estimates[c] / total;
      var bySize = share >= thresholdShare;
      var reason = (reasons[c] || "").trim();
      return { category: c, name: DATA.categories[c], tco2e: estimates[c], share: share,
               significant_by_size: bySize, other_reason: reason, significant: bySize || reason !== "" };
    });
  }

  // ------------------------------------------------------------ page

  function pct(x) { return (x * 100).toFixed(2) + "%"; }

  CATS.forEach(function (c) {
    var tr = document.createElement("tr");
    tr.setAttribute("data-category", c);
    tr.innerHTML = "<td>" + c + "</td><td>" + DATA.categories[c] + "</td>" +
      "<td><input type='number' name='estimate' min='0' step='any' aria-label='estimate " + c + "'></td>" +
      "<td><input type='text' name='reason' aria-label='other reason " + c + "'></td>" +
      "<td class='share' data-value=''></td><td class='significant' data-value=''></td>";
    tbody.appendChild(tr);
  });

  function read() {
    var est = {}, reasons = {};
    Array.prototype.forEach.call(tbody.rows, function (tr) {
      var c = Number(tr.getAttribute("data-category"));
      var v = tr.querySelector("[name='estimate']").value;
      est[c] = v === "" ? null : Number(v);
      reasons[c] = tr.querySelector("[name='reason']").value;
    });
    return { estimates: est, reasons: reasons, threshold: Number(document.getElementById("threshold").value) / 100 };
  }

  function set(id, value, text) {
    var el = document.getElementById(id);
    el.setAttribute("data-value", value === null ? "" : String(value));
    el.textContent = text;
  }

  function update() {
    var s = read(), rows;
    var errors = document.getElementById("errors");
    try {
      rows = screen(s.estimates, s.threshold, s.reasons);
      errors.textContent = "";
    } catch (e) {
      errors.textContent = e.message;
      Array.prototype.forEach.call(tbody.rows, function (tr) {
        tr.querySelector(".share").textContent = ""; tr.querySelector(".significant").textContent = "";
        tr.classList.remove("tool-significant");
      });
      set("out-total", null, "–"); set("out-significant", null, "–"); set("out-coverage", null, "–");
      return;
    }
    var total = 0, covered = 0, sig = [];
    rows.forEach(function (r, i) {
      var tr = tbody.rows[i];
      var share = tr.querySelector(".share"), flag = tr.querySelector(".significant");
      share.textContent = pct(r.share); share.setAttribute("data-value", String(r.share));
      flag.textContent = r.significant ? (r.significant_by_size ? "Yes (size)" : "Yes (other reason)") : "No";
      flag.setAttribute("data-value", r.significant ? "yes" : "no");
      tr.classList.toggle("tool-significant", r.significant);
      total += r.tco2e;
      if (r.significant) { covered += r.tco2e; sig.push(r.category); }
    });
    set("out-total", total, total.toLocaleString("en-GB", { maximumFractionDigits: 2 }));
    set("out-significant", sig.join(","), sig.length ? sig.length + ": " + sig.join(", ") : "none");
    set("out-coverage", covered / total, pct(covered / total));
  }

  function loadExample() {
    var ex = DATA.example;
    document.getElementById("threshold").value = (ex.threshold_share * 100).toString();
    Array.prototype.forEach.call(tbody.rows, function (tr) {
      var c = tr.getAttribute("data-category");
      tr.querySelector("[name='estimate']").value = ex.estimates[c];
      tr.querySelector("[name='reason']").value = ex.reasons[c] || "";
    });
    update();
  }

  document.getElementById("load-example").addEventListener("click", loadExample);
  document.getElementById("clear").addEventListener("click", function () {
    Array.prototype.forEach.call(tbody.querySelectorAll("input"), function (i) { i.value = ""; });
    update();
  });
  document.getElementById("screening-app").addEventListener("input", update);

  update();
  document.getElementById("screening-app").setAttribute("data-ready", "true");
  window.scope3Screening = { screen: screen };
})();
