/*
 * VSME readiness check for the ESG Workflows Handbook.
 * A port of esgcalc.vsme.readiness. Runs in the browser: no network requests, no storage.
 * Not legal advice. Licence: MIT.
 */
(function () {
  "use strict";

  var DATA = JSON.parse(document.getElementById("vsme-readiness-data").textContent);
  var tbody = document.querySelector("#points tbody");

  // ------------------------------------------------------------ calculation (same as esgcalc)

  function readiness(points, doneIds, option) {
    if (option !== "A" && option !== "B") throw new Error("option must be A or B");
    var modules = option === "A" ? ["basic"] : ["basic", "comprehensive"];
    var done = {};
    doneIds.forEach(function (id) { done[id] = true; });
    var pts = points.filter(function (p) { return modules.indexOf(p.module) >= 0; });
    var out = {};
    modules.forEach(function (m) {
      var inM = pts.filter(function (p) { return p.module === m; });
      var d = inM.filter(function (p) { return done[p.id]; }).length;
      out[m] = { done: d, total: inM.length, share: inM.length ? d / inM.length : 0 };
    });
    var doneAll = pts.filter(function (p) { return done[p.id]; }).length;
    return { modules: out, overall: pts.length ? doneAll / pts.length : 0,
             todo: pts.filter(function (p) { return !done[p.id]; }).map(function (p) { return p.id; }) };
  }

  // ------------------------------------------------------------ page

  DATA.datapoints.forEach(function (p) {
    var tr = document.createElement("tr");
    tr.setAttribute("data-id", p.id);
    tr.setAttribute("data-module", p.module);
    var td = document.createElement("td");
    var cb = document.createElement("input");
    cb.type = "checkbox"; cb.name = "have"; cb.value = p.id; cb.setAttribute("aria-label", p.id);
    td.appendChild(cb); tr.appendChild(td);
    var id = document.createElement("td"); id.textContent = p.id; tr.appendChild(id);
    var desc = document.createElement("td"); desc.textContent = p.description; tr.appendChild(desc);
    tbody.appendChild(tr);
  });

  function pct(x) { return (x * 100).toFixed(1) + "%"; }

  function update() {
    var option = document.getElementById("option").value;
    var done = Array.prototype.map.call(tbody.querySelectorAll("input:checked"), function (c) { return c.value; });
    var r = readiness(DATA.datapoints, done, option);

    Array.prototype.forEach.call(tbody.rows, function (tr) {
      tr.hidden = option === "A" && tr.getAttribute("data-module") === "comprehensive";
    });
    var b = r.modules.basic;
    var out = document.getElementById("out-basic");
    out.textContent = pct(b.share) + " (" + b.done + " of " + b.total + ")";
    out.setAttribute("data-value", String(b.share));
    var rowC = document.getElementById("row-comprehensive");
    rowC.hidden = option === "A";
    var c = r.modules.comprehensive, outC = document.getElementById("out-comprehensive");
    outC.textContent = c ? pct(c.share) + " (" + c.done + " of " + c.total + ")" : "";
    outC.setAttribute("data-value", c ? String(c.share) : "");
    var o = document.getElementById("out-overall");
    o.textContent = pct(r.overall); o.setAttribute("data-value", String(r.overall));

    var todo = document.getElementById("todo");
    todo.innerHTML = "";
    var byDisc = {};
    var order = [];
    r.todo.forEach(function (id) {
      var p = DATA.datapoints.filter(function (x) { return x.id === id; })[0];
      if (!byDisc[p.disclosure]) { byDisc[p.disclosure] = []; order.push(p.disclosure); }
      byDisc[p.disclosure].push(p);
    });
    if (!order.length) {
      var li = document.createElement("li"); li.textContent = "Nothing left: every datapoint is ticked."; todo.appendChild(li);
    }
    order.forEach(function (disc) {
      var li = document.createElement("li");
      li.setAttribute("data-disclosure", disc);
      var head = document.createElement("strong");
      head.textContent = disc + " " + (DATA.topics[disc] || "") + ": ";
      li.appendChild(head);
      li.appendChild(document.createTextNode(byDisc[disc].map(function (p) { return p.id; }).join(", ")));
      todo.appendChild(li);
    });
    todo.setAttribute("data-todo", r.todo.join(","));
  }

  function setDone(ids) {
    Array.prototype.forEach.call(tbody.querySelectorAll("input"), function (c) { c.checked = ids.indexOf(c.value) >= 0; });
  }

  document.getElementById("load-example").addEventListener("click", function () {
    document.getElementById("option").value = DATA.example.option;
    setDone(DATA.example.done);
    update();
  });
  document.getElementById("clear").addEventListener("click", function () { setDone([]); update(); });
  document.getElementById("readiness-app").addEventListener("change", update);

  document.getElementById("option").value = "B";
  update();
  document.getElementById("readiness-app").setAttribute("data-ready", "true");
  window.vsmeReadiness = { readiness: readiness };
})();
