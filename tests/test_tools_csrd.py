"""Browser tests for the DMA scoring tool and the ESRS gap check (Playwright):
same results as esgcalc.dma and esgcalc.csrd, no requests, phone layout."""
import random
from pathlib import Path
from urllib.parse import urlparse

import pytest
import yaml

from esgcalc.csrd import datapoints_in_scope, gap_summary
from esgcalc.dma import IRO, assess, assess_all, topics
from test_tools import SITE_ASSET_HOSTS, offline, site_url  # noqa: F401  (pytest fixtures)

ROOT = Path(__file__).resolve().parents[1]
ESRS = yaml.safe_load((ROOT / "data/esrs_datapoints.yml").read_text(encoding="utf-8"))
MLG = yaml.safe_load((ROOT / "data/examples/mediterranean_logistics.yml").read_text(encoding="utf-8"))


def _iros() -> list[IRO]:
    return [IRO(i["id"], i["topic"], i["description"], i["kind"], actual=i.get("actual", False),
                human_rights=i.get("human_rights", False), scale=i.get("scale"), scope=i.get("scope"),
                irremediability=i.get("irremediability"), likelihood=i.get("likelihood"),
                magnitude=i.get("magnitude")) for i in MLG["dma"]["iros"]]


def _open(page, url: str, app: str):
    errors: list[str] = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(url)
    page.wait_for_selector(f"#{app}[data-ready='true']")
    return errors


# --- DMA scoring --------------------------------------------------------------------------

@pytest.fixture()
def dma_tool(page, site_url):
    errors = _open(page, site_url + "tools/dma-scoring/", "dma-app")
    yield page
    assert not errors, errors


def test_dma_example_matches_esgcalc(dma_tool) -> None:
    dma_tool.click("#load-example")
    for a in assess_all(_iros()):
        row = dma_tool.locator(f"#items tbody tr[data-id='{a.iro.id}']")
        assert float(row.locator(".out-score").get_attribute("data-value")) == pytest.approx(a.score), a.iro.id
        assert row.locator(".out-material").inner_text() == ("Yes" if a.material else "No"), a.iro.id
    material = [t.topic for t in topics(assess_all(_iros())) if t.material]
    assert dma_tool.locator("#topics").get_attribute("data-material") == ",".join(material) == "E1,E5,S1"
    assert dma_tool.locator("#summary").get_attribute("data-value") == "4"
    assert dma_tool.locator("#topics tr[data-standard='E1'] td").nth(4).inner_text() == "Yes"   # financial side


def test_dma_editing_a_score_updates(dma_tool) -> None:
    dma_tool.click("#load-example")
    row = dma_tool.locator("#items tbody tr[data-id='S2-I1']")
    row.locator("input[name='likelihood']").fill("5")                     # 3 x 5 / 5 = 3.0: now material
    i = next(x for x in _iros() if x.id == "S2-I1")
    a = assess(IRO(**{**i.__dict__, "likelihood": 5}))
    assert a.score == pytest.approx(3.0) and a.material
    assert float(row.locator(".out-score").get_attribute("data-value")) == pytest.approx(a.score)
    assert dma_tool.locator("#topics").get_attribute("data-material") == "E1,E5,S1,S2"
    row.locator("input[name='scale']").fill("")
    assert row.locator(".out-score").inner_text() == "scale is needed for this kind of IRO"


def test_dma_port_matches_esgcalc_on_random_items(dma_tool) -> None:
    # boundaries first: human rights severity exactly at the cut-off (4), and a score exactly at 3.0
    edges = [IRO("E-hr", "S1", "x", "impact", human_rights=True, scale=4, scope=1, irremediability=1, likelihood=1),
             IRO("E-thr", "E1", "x", "risk", magnitude=5, likelihood=3)]
    for iro in edges:
        py = assess(iro)
        js = dma_tool.evaluate("i => window.dmaScoring.assess(i)", {**iro.__dict__})
        assert (js["score"], js["material"]) == (pytest.approx(py.score), py.material), iro.id
    assert assess(edges[0]).score == 4.0 and assess(edges[1]).score == 3.0
    rng = random.Random(11)
    kinds = ["impact", "risk", "opportunity"]
    for n in range(300):
        kind = rng.choice(kinds)
        s = lambda: rng.randint(1, 5)  # noqa: E731
        if kind == "impact":
            neg, actual = rng.random() < 0.7, rng.random() < 0.4
            iro = IRO(f"X{n}", "S1", "x", kind, negative=neg, actual=actual, human_rights=rng.random() < 0.4,
                      scale=s(), scope=s(), irremediability=s() if neg else None,
                      likelihood=None if actual else s())
        else:
            iro = IRO(f"X{n}", "E1", "x", kind, likelihood=s(), magnitude=s())
        py = assess(iro)
        js = dma_tool.evaluate("i => window.dmaScoring.assess(i)", {**iro.__dict__})
        assert js["score"] == pytest.approx(py.score), iro
        assert js["material"] == py.material and js["dimension"] == py.dimension, iro
    with pytest.raises(Exception):
        dma_tool.evaluate("() => window.dmaScoring.assess({id: 'B', kind: 'risk', magnitude: 6, likelihood: 1})")


# --- ESRS gap check -----------------------------------------------------------------------

@pytest.fixture()
def gap_tool(page, site_url):
    errors = _open(page, site_url + "tools/esrs-gap/", "gap-app")
    yield page
    assert not errors, errors


def _out(page, key: str) -> float:
    return float(page.locator(f"#out-{key}").get_attribute("data-value"))


def test_gap_example_matches_esgcalc(gap_tool) -> None:
    gap_tool.click("#load-example")
    material = [t.topic for t in topics(assess_all(_iros())) if t.material]
    scope = datapoints_in_scope(ESRS["datapoints"], material)
    s = gap_summary(scope, MLG["gap_status"])
    assert _out(gap_tool, "total") == s.total == 15
    for k, n in s.counts.items():
        assert _out(gap_tool, k) == n, k
    assert _out(gap_tool, "none") == 0
    assert _out(gap_tool, "share") == pytest.approx(s.ready_share)
    rows = gap_tool.locator("#points tbody tr")
    assert [rows.nth(i).get_attribute("data-id") for i in range(rows.count())] == [d["id"] for d in scope]


def test_gap_unticking_and_new_topic(gap_tool) -> None:
    gap_tool.click("#load-example")
    gap_tool.locator("input[name='material'][value='E1']").uncheck()       # 8 E1 datapoints leave the scope
    assert _out(gap_tool, "total") == 7
    assert _out(gap_tool, "Ready") == 3                                    # materiality process, S1 x2
    gap_tool.locator("input[name='material'][value='E2']").check()         # 2 new datapoints, no status
    assert _out(gap_tool, "total") == 9 and _out(gap_tool, "none") == 2
    assert _out(gap_tool, "share") == pytest.approx(3 / 9)
    gap_tool.locator("input[name='material'][value='E1']").check()         # statuses kept
    assert _out(gap_tool, "Ready") == 6
    gap_tool.select_option("select[data-id='E2-pollution']", "Ready")
    assert _out(gap_tool, "Ready") == 7 and _out(gap_tool, "none") == 1


def test_gap_port_matches_esgcalc(gap_tool) -> None:
    rng = random.Random(5)
    standards = [s["standard"] for s in ESRS["standards"] if s["kind"] == "topical"]
    for _ in range(10):
        material = rng.sample(standards, rng.randint(0, len(standards)))
        scope = datapoints_in_scope(ESRS["datapoints"], material)
        status = {d["id"]: rng.choice(["Ready", "Partial", "Gap", "Phase-in"]) for d in scope}
        js_scope = gap_tool.evaluate("([d, m]) => window.esrsGap.datapointsInScope(d, m)", [ESRS["datapoints"], material])
        assert [d["id"] for d in js_scope] == [d["id"] for d in scope]
        js = gap_tool.evaluate("([s, st]) => window.esrsGap.gapSummary(s, st)", [scope, status])
        py = gap_summary(scope, status)
        assert js["counts"] == py.counts and js["total"] == py.total
        assert js["ready_share"] == pytest.approx(py.ready_share)


# --- both ---------------------------------------------------------------------------------

@pytest.mark.parametrize("path, app", [("tools/dma-scoring/", "dma-app"), ("tools/esrs-gap/", "gap-app")])
def test_no_requests_and_phone_layout(page, site_url, offline, path, app) -> None:  # noqa: F811
    page.set_viewport_size({"width": 375, "height": 800})
    page.goto(site_url + path)
    page.wait_for_selector(f"#{app}[data-ready='true']")
    page.click("#load-example")
    page.wait_for_timeout(300)
    assert {urlparse(u).netloc for u in offline} <= SITE_ASSET_HOSTS
    assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 1")
