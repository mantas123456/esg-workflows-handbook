"""Browser tests for the VSME readiness check (Playwright): same results as esgcalc.vsme.readiness."""
from pathlib import Path
from urllib.parse import urlparse

import pytest
import yaml

from esgcalc.vsme import readiness
from test_tools import SITE_ASSET_HOSTS, offline, site_url  # noqa: F401  (pytest fixtures)

ROOT = Path(__file__).resolve().parents[1]
POINTS = yaml.safe_load((ROOT / "data/vsme_datapoints.yml").read_text(encoding="utf-8"))["datapoints"]
GOZO = yaml.safe_load((ROOT / "data/examples/gozo_fresh_foods.yml").read_text(encoding="utf-8"))
DONE = [k for k, v in GOZO["vsme_status"].items() if v[3] in ("Collected", "Not applicable")] + GOZO["vsme_comprehensive_done"]


@pytest.fixture()
def tool(page, site_url):
    errors: list[str] = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(site_url + "tools/vsme-readiness/")
    page.wait_for_selector("#readiness-app[data-ready='true']")
    yield page
    assert not errors, errors


def value(page, element_id: str) -> str:
    return page.locator(f"#{element_id}").get_attribute("data-value")


def test_example_option_b_matches_esgcalc(tool) -> None:
    tool.click("#load-example")
    r = readiness(POINTS, DONE, "B")
    assert float(value(tool, "out-basic")) == pytest.approx(r["modules"]["basic"]["share"])          # 21/22
    assert float(value(tool, "out-comprehensive")) == pytest.approx(r["modules"]["comprehensive"]["share"])  # 4/9
    assert float(value(tool, "out-overall")) == pytest.approx(r["overall"])                           # 25/31
    assert tool.locator("#todo").get_attribute("data-todo") == ",".join(r["todo"])
    assert len(r["todo"]) == 6
    # the to-do list groups by disclosure, with the topic
    assert tool.locator("#todo li[data-disclosure='C3']").inner_text().startswith("C3 GHG reduction targets")


def test_option_a_counts_basic_only(tool) -> None:
    tool.click("#load-example")
    tool.select_option("#option", "A")
    r = readiness(POINTS, DONE, "A")
    assert float(value(tool, "out-overall")) == pytest.approx(r["overall"]) == pytest.approx(21 / 22)
    assert tool.locator("#todo").get_attribute("data-todo") == "B5-land-use"
    assert tool.locator("#row-comprehensive").is_hidden()
    assert tool.locator("#points tbody tr[data-module='comprehensive']").first.is_hidden()


def test_ticking_updates(tool) -> None:
    tool.click("#load-example")
    tool.locator("input[value='B5-land-use']").check()
    r = readiness(POINTS, DONE + ["B5-land-use"], "B")
    assert float(value(tool, "out-basic")) == pytest.approx(1.0)
    assert float(value(tool, "out-overall")) == pytest.approx(r["overall"])
    tool.click("#clear")
    assert float(value(tool, "out-overall")) == 0.0


def test_port_matches_esgcalc_on_random_selections(tool) -> None:
    import random

    rng = random.Random(7)
    ids = [p["id"] for p in POINTS]
    for _ in range(10):
        done = rng.sample(ids, rng.randint(0, len(ids)))
        for option in ("A", "B"):
            js = tool.evaluate("([p, d, o]) => window.vsmeReadiness.readiness(p, d, o)", [POINTS, done, option])
            py = readiness(POINTS, done, option)
            assert js["todo"] == py["todo"]
            assert js["overall"] == pytest.approx(py["overall"])


def test_no_requests_and_phone_layout(page, site_url, offline) -> None:  # noqa: F811
    page.set_viewport_size({"width": 375, "height": 800})
    page.goto(site_url + "tools/vsme-readiness/")
    page.wait_for_selector("#readiness-app[data-ready='true']")
    page.click("#load-example")
    page.wait_for_timeout(300)
    assert {urlparse(u).netloc for u in offline} <= SITE_ASSET_HOSTS
    assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 1")
