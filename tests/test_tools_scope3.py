"""Browser tests for the Scope 3 screening tool and the uncertainty demo (Playwright).

Uses the site_url and offline fixtures from test_tools.py. The screening tool must
match esgcalc.scope3.screen exactly; the demo's sum rule must match
esgcalc.quality.sum_uncertainty exactly, and its Monte Carlo must agree with
esgcalc.quality.monte_carlo_sum within sampling noise (different random generators).
"""
from urllib.parse import urlparse

import pytest

from esgcalc import quality
from test_examples_scope3 import screening_rows
from test_examples_scope3_report import all_lines
from test_tools import SITE_ASSET_HOSTS, offline, site_url  # noqa: F401  (pytest fixtures)


def _open(page, site_url, path: str, app: str):
    errors: list[str] = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(site_url + path)
    page.wait_for_selector(f"#{app}[data-ready='true']")
    return errors


# --- Scope 3 screening ------------------------------------------------------------

@pytest.fixture()
def screening(page, site_url):
    errors = _open(page, site_url, "tools/scope3-screening/", "screening-app")
    yield page
    assert not errors, errors


def test_screening_example_matches_esgcalc(screening) -> None:
    screening.click("#load-example")
    rows = screening_rows()
    for i, r in enumerate(rows):
        tr = screening.locator("#categories tbody tr").nth(i)
        assert tr.get_attribute("data-category") == str(r.category)
        assert float(tr.locator(".share").get_attribute("data-value")) == pytest.approx(r.share), r.category
        assert tr.locator(".significant").get_attribute("data-value") == ("yes" if r.significant else "no"), r.category
    significant = [r.category for r in rows if r.significant]
    assert screening.locator("#out-significant").get_attribute("data-value") == ",".join(map(str, significant))
    covered = sum(r.tco2e for r in rows if r.significant) / sum(r.tco2e for r in rows)
    assert float(screening.locator("#out-coverage").get_attribute("data-value")) == pytest.approx(covered)
    assert float(screening.locator("#out-total").get_attribute("data-value")) == pytest.approx(7489.08)
    assert "other reason" in screening.locator("#categories tbody tr").nth(8).locator(".significant").inner_text()


def test_screening_threshold_edge_matches_esgcalc(screening) -> None:
    from esgcalc.scope3 import screen

    est = {c: 0.0 for c in range(1, 16)}
    est.update({1: 98.0, 2: 2.0})                              # exactly 2% for category 2
    js = screening.evaluate("e => window.scope3Screening.screen(e, 0.02, {})", {str(k): v for k, v in est.items()})
    py = screen(est, 0.02)
    assert [r["significant_by_size"] for r in js] == [r.significant_by_size for r in py]


def test_screening_needs_all_15(screening) -> None:
    screening.locator("#categories tbody tr").first.locator("[name='estimate']").fill("100")
    assert "category 2" in screening.locator("#errors").inner_text()
    assert screening.locator("#out-total").get_attribute("data-value") == ""


# --- Uncertainty demo ------------------------------------------------------------

@pytest.fixture()
def demo(page, site_url):
    errors = _open(page, site_url, "tools/uncertainty-demo/", "uncertainty-app")
    yield page
    assert not errors, errors


def _cat1():
    return all_lines()[1]


def test_demo_sum_rule_matches_esgcalc(demo) -> None:
    demo.click("#load-example")
    rows = _cat1()
    total = quality.sum_uncertainty([r["value"] for r in rows], [r["u95"] for r in rows])
    assert float(demo.locator("#sum-value").get_attribute("data-value")) == pytest.approx(total.value)
    assert float(demo.locator("#sum-interval").get_attribute("data-low")) == pytest.approx(total.value - total.u95_abs, abs=1e-3)
    assert float(demo.locator("#sum-interval").get_attribute("data-high")) == pytest.approx(total.value + total.u95_abs, abs=1e-3)
    assert float(demo.locator("#sum-rel").get_attribute("data-value")) == pytest.approx(total.u95_rel, abs=1e-6)


def test_demo_monte_carlo_agrees_with_esgcalc(demo) -> None:
    demo.click("#load-example")
    rows = _cat1()
    values = [r["value"] for r in rows]
    py = quality.monte_carlo_sum(values, [1.0] * len(values), [quality.gsd_from_u95(r["u95"]) for r in rows],
                                 n=100_000, seed=20260101)
    js_low = float(demo.locator("#mc-interval").get_attribute("data-low"))
    js_high = float(demo.locator("#mc-interval").get_attribute("data-high"))
    js_median = float(demo.locator("#mc-median").get_attribute("data-value"))
    js_mean = float(demo.locator("#mc-mean").get_attribute("data-value"))
    # different random generators: agreement within sampling noise
    assert js_median == pytest.approx(py.median, rel=0.005)
    assert js_mean == pytest.approx(py.mean, rel=0.005)
    assert js_low == pytest.approx(py.low, rel=0.01)
    assert js_high == pytest.approx(py.high, rel=0.01)
    # the asymmetry F2 describes
    total = quality.sum_uncertainty(values, [r["u95"] for r in rows])
    assert js_low > total.value - total.u95_abs
    assert demo.locator("#histogram rect").count() == 40


def test_demo_is_seeded(demo) -> None:
    demo.click("#load-example")
    first = demo.locator("#mc-interval").get_attribute("data-low")
    demo.click("#run")
    assert demo.locator("#mc-interval").get_attribute("data-low") == first       # same seed, same result
    demo.fill("#seed", "7")
    demo.click("#run")
    assert demo.locator("#mc-interval").get_attribute("data-low") != first


def test_demo_gsd_matches_esgcalc(demo) -> None:
    for u in (0.0, 0.1, 0.2, 0.5):
        assert demo.evaluate("u => window.uncertaintyDemo.gsdFromU95(u)", u) == pytest.approx(quality.gsd_from_u95(u))


def test_demo_rejects_bad_input(demo) -> None:
    demo.locator("#lines tbody tr").first.locator("[name='value']").fill("-5")
    demo.locator("#lines tbody tr").first.locator("[name='u95']").fill("10")
    demo.click("#run")
    assert "zero or more" in demo.locator("#errors").inner_text()


# --- both tools ------------------------------------------------------------------

@pytest.mark.parametrize("path, app, button", [
    ("tools/scope3-screening/", "screening-app", "#load-example"),
    ("tools/uncertainty-demo/", "uncertainty-app", "#load-example"),
])
def test_tools_make_no_requests_of_their_own(page, site_url, offline, path, app, button) -> None:  # noqa: F811
    _open(page, site_url, path, app)
    page.click(button)
    page.wait_for_timeout(300)
    assert {urlparse(u).netloc for u in offline} <= SITE_ASSET_HOSTS


@pytest.mark.parametrize("path, app", [("tools/scope3-screening/", "screening-app"),
                                       ("tools/uncertainty-demo/", "uncertainty-app")])
def test_tools_phone_layout(page, site_url, path, app) -> None:
    page.set_viewport_size({"width": 375, "height": 800})
    _open(page, site_url, path, app)
    page.click("#load-example")
    assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 1")
