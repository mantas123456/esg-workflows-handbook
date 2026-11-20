"""Browser tests for the CBAM calculator (Playwright).

The site is built into a temporary folder and served locally. The tests load
the Melita Metals example and check that the tool gives the same numbers as
esgcalc, call the ported functions directly for edge cases, and check that
the tool makes no network requests of its own.

    pip install -r requirements-dev.txt
    python -m playwright install chromium
    pytest tests/test_tools.py
"""
from __future__ import annotations

import functools
import http.server
import os
import subprocess
import sys
import threading
from decimal import Decimal
from pathlib import Path
from urllib.parse import urlparse

import pytest
import yaml

from esgcalc import cbam

ROOT = Path(__file__).resolve().parent.parent
EXAMPLE = yaml.safe_load((ROOT / "data/examples/melita_metals.yml").read_text(encoding="utf-8"))
# Third-party hosts the theme itself may load on every page. The tool must add none.
SITE_ASSET_HOSTS = {"fonts.googleapis.com", "fonts.gstatic.com", "api.github.com", "cdn.jsdelivr.net"}


class _QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


@pytest.fixture(scope="session")
def site_url(tmp_path_factory):
    out = tmp_path_factory.mktemp("site")
    subprocess.run([sys.executable, "-m", "mkdocs", "build", "--strict", "--site-dir", str(out)],
                   cwd=ROOT, check=True, capture_output=True, env={**os.environ, "NO_MKDOCS_2_WARNING": "1"})
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(_QuietHandler, directory=str(out)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{server.server_address[1]}/"
    server.shutdown()


@pytest.fixture(autouse=True)
def offline(context, site_url):
    """Block every request that leaves the local server, and record it."""
    origin = urlparse(site_url).netloc
    attempts: list[str] = []

    def handle(route):
        if urlparse(route.request.url).netloc == origin:
            route.continue_()
        else:
            attempts.append(route.request.url)
            route.abort()

    context.route("**/*", handle)
    return attempts


@pytest.fixture()
def tool(page, site_url):
    errors: list[str] = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(site_url + "tools/cbam-calculator/")
    page.wait_for_selector("#cbam-app[data-ready='true']")
    yield page
    assert not errors, errors


def value(page, element_id: str) -> str:
    return page.locator(f"#{element_id}").get_attribute("data-value")


def _mass(inst: str, quarters=("Q1", "Q2", "Q3", "Q4")) -> float:
    return sum(l["mass_t"] for l in EXAMPLE["imports_2026"] if l["installation"] == inst and l["quarter"] in quarters)


def _expected(year: int, fa_per_t: dict[str, float]) -> dict:
    """The Melita Metals figures from esgcalc for a year of import."""
    bars = EXAMPLE["installation_A_2026"]
    crude = EXAMPLE["installation_A_crude_steel_2026"]
    crude_see = cbam.embedded_emissions(
        sector="iron_steel", production_mass_t=crude["production_mass_t"], direct_tco2e=crude["direct_tco2e"],
        precursors=[cbam.Precursor(p["mass_t"], p["see_tco2e_per_t"]) for p in crude["precursors"]],
        imported_mass_t=0).see_tco2e_per_t
    a_see = cbam.embedded_emissions(
        sector="iron_steel", production_mass_t=bars["production_mass_t"], direct_tco2e=bars["direct_tco2e"],
        precursors=[cbam.Precursor(bars["precursors"][0]["mass_t"], crude_see)], imported_mass_t=0).see_tco2e_per_t
    base = EXAMPLE["default_values_base"]
    b_see = cbam.default_value_with_markup(base["aluminium_bars_B"]["base_direct_see_tco2e_per_t"], year, "aluminium")
    embedded = a_see * _mass("A") + b_see * _mass("B")
    fa = fa_per_t["A"] * _mass("A") + fa_per_t["B"] * _mass("B")
    certs = cbam.certificates_needed(embedded, fa)
    holding = {}
    quarters: list[str] = []
    for q in ("Q1", "Q2", "Q3", "Q4"):
        quarters.append(q)
        e = (_mass("A", quarters) * base["steel_bars_A"]["base_direct_see_tco2e_per_t"]
             + _mass("B", quarters) * base["aluminium_bars_B"]["base_direct_see_tco2e_per_t"])
        f = _mass("A", quarters) * fa_per_t["A"] + _mass("B", quarters) * fa_per_t["B"]
        holding[q] = cbam.quarterly_holding(e, year, f)
    return {"embedded": embedded, "fa": fa, "certs": certs,
            "cost": cbam.certificate_cost(round(certs, 6), EXAMPLE["certificate_price_assumed_eur_per_tco2e"]),
            "holding": holding}


# --- the Melita Metals example ----------------------------------------------

def test_example_2026_matches_esgcalc(tool) -> None:
    tool.click("#load-example")
    assert tool.locator("#lines tbody tr").count() == len(EXAMPLE["imports_2026"])
    threshold = cbam.threshold_check([(l["cn_code"], l["mass_t"]) for l in EXAMPLE["imports_2026"]])
    assert float(value(tool, "out-total-mass")) == threshold.total_mass_t == 435
    assert value(tool, "out-threshold") == ("above" if threshold.above_threshold else "within")

    e = _expected(2026, EXAMPLE["free_allocation_adjustment_tco2e_per_t"][2026])
    assert float(value(tool, "out-embedded")) == pytest.approx(e["embedded"])     # 341.65
    assert float(value(tool, "out-fa")) == pytest.approx(e["fa"])                 # 302.25
    assert float(value(tool, "out-certs")) == pytest.approx(e["certs"])           # 39.4
    assert Decimal(value(tool, "out-cost")) == e["cost"] == Decimal("3152")       # EUR 3,152.00
    assert tool.locator("#out-cost").inner_text() == "3,152.00"
    assert "applies from 2027" in tool.locator("#holding-note").inner_text()
    assert tool.locator("#holding tbody tr").count() == 0


def test_example_lines_match_esgcalc(tool) -> None:
    tool.click("#load-example")
    e_a = cbam.default_value_with_markup(2.10, 2026, "aluminium")
    spans = tool.locator(".line-embedded")
    for i, line in enumerate(EXAMPLE["imports_2026"]):
        got = float(spans.nth(i).get_attribute("data-value"))
        expected = line["mass_t"] * (0.652 if line["installation"] == "A" else e_a)
        assert got == pytest.approx(expected), i


def test_example_2027_quarterly_holding_matches_esgcalc(tool) -> None:
    tool.click("#load-example")
    fa_2027 = EXAMPLE["free_allocation_adjustment_tco2e_per_t"][2027]
    rows = tool.locator("#lines tbody tr")
    for i, line in enumerate(EXAMPLE["imports_2026"]):
        rows.nth(i).locator("[name='fa_per_t']").fill(str(fa_2027[line["installation"]]))
    tool.fill("#year", "2027")
    e = _expected(2027, fa_2027)
    assert float(value(tool, "out-certs")) == pytest.approx(e["certs"])           # 20% mark-up for B in 2027
    assert Decimal(value(tool, "out-cost")) == e["cost"]
    got = {q: float(tool.locator(f"#holding tr[data-quarter='{q}'] td").nth(3).get_attribute("data-value"))
           for q in ("Q1", "Q2", "Q3", "Q4")}
    assert got == pytest.approx(e["holding"])
    assert got == pytest.approx({"Q1": 31.7, "Q2": 89.25, "Q3": 146.9, "Q4": 209.5})   # as in CB8


# --- the ported functions, edge cases ---------------------------------------

@pytest.mark.parametrize("lines", [
    [("7214 20 00", 1.1)] * 45 + [("7214 20 00", 0.5)],     # exactly 50 t from many lines
    [("7214 20 00", 50)],
    [("7214 20 00", 50.001)],
    [("2804 10 00", 2), ("7214 20 00", 10), ("2716 00 00", 500)],
    [],
])
def test_threshold_check_matches_esgcalc(tool, lines) -> None:
    js = tool.evaluate("l => window.cbamCalculator.thresholdCheck(l)",
                       [{"cn_code": c, "mass_t": m} for c, m in lines])
    py = cbam.threshold_check(lines)
    assert js["total_mass_t"] == pytest.approx(py.total_mass_t)
    assert js["above"] is py.above_threshold
    assert js["excluded"] == py.excluded_cn_codes


@pytest.mark.parametrize("year, sector", [(2026, "aluminium"), (2027, "cement"), (2028, "iron_steel"),
                                          (2035, "aluminium"), (2026, "fertilisers"), (2030, "fertilisers")])
def test_markup_matches_esgcalc(tool, year, sector) -> None:
    js = tool.evaluate("([y, s]) => 2 * (1 + window.cbamCalculator.markup(y, s))", [year, sector])
    assert js == pytest.approx(cbam.default_value_with_markup(2.0, year, sector))


@pytest.mark.parametrize("certs, price", [(58, 75.36), (0.5, 0.01), (3, 33.335), (39.4, 80), (0, 82.32)])
def test_cost_rounding_matches_esgcalc(tool, certs, price) -> None:
    js = tool.evaluate("([c, p]) => window.cbamCalculator.certificateCost(c, p)", [certs, price])
    assert Decimal(str(js)) == cbam.certificate_cost(certs, str(price))


def test_certificates_and_holding_edges_match_esgcalc(tool) -> None:
    f = "window.cbamCalculator"
    assert tool.evaluate(f"{f}.certificatesNeeded(100, 60, 80)") == cbam.certificates_needed(100, 60, 80) == 0
    assert tool.evaluate(f"{f}.quarterlyHolding(808, 2026, 0)") is None     # rule starts in 2027
    assert cbam.quarterly_holding(808, 2026) == 0
    assert tool.evaluate(f"{f}.quarterlyHolding(100, 2027, 150)") == cbam.quarterly_holding(100, 2027, 150) == 0


# --- behaviour --------------------------------------------------------------

def test_bad_input_shows_an_error(tool) -> None:
    row = tool.locator("#lines tbody tr").first
    row.locator("[name='cn_code']").fill("72AB")
    row.locator("[name='mass_t']").fill("10")
    assert "digits only" in tool.locator("#errors").inner_text()
    assert value(tool, "out-certs") == ""
    row.locator("[name='cn_code']").fill("2716 00 00")
    assert "electricity" in tool.locator("#errors").inner_text()


def test_tool_makes_no_requests_of_its_own(tool, offline) -> None:
    tool.click("#load-example")
    tool.fill("#year", "2028")
    tool.wait_for_timeout(300)
    hosts = {urlparse(u).netloc for u in offline}
    assert hosts <= SITE_ASSET_HOSTS, hosts


def test_phone_layout_has_no_page_scroll(page, site_url) -> None:
    page.set_viewport_size({"width": 375, "height": 800})
    page.goto(site_url + "tools/cbam-calculator/")
    page.wait_for_selector("#cbam-app[data-ready='true']")
    page.click("#load-example")
    assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 1")
