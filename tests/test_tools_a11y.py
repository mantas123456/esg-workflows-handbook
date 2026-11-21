"""Accessibility of the browser tools (Playwright + axe-core, run locally, no network).

For every tool, in light and dark mode, with the example loaded, axe-core finds no
violations of its default rules (WCAG 2.1 A and AA among them: labels, names,
contrast, heading order, table headers). The keyboard alone can reach the
example button and use it.
"""
import pytest

from test_tools import offline, site_url  # noqa: F401  (pytest fixtures)

TOOLS = {
    "cbam-calculator": "cbam-app",
    "dma-scoring": "dma-app",
    "esrs-gap": "gap-app",
    "scope3-screening": "screening-app",
    "uncertainty-demo": "uncertainty-app",
    "vsme-readiness": "readiness-app",
}


def test_every_tool_page_is_listed() -> None:
    from pathlib import Path
    pages = {p.stem for p in (Path(__file__).resolve().parents[1] / "docs/tools").glob("*.md")} - {"index"}
    assert pages == set(TOOLS)


@pytest.mark.parametrize("scheme", ["light", "dark"])
@pytest.mark.parametrize("tool", sorted(TOOLS))
def test_no_axe_violations(browser, site_url, tool, scheme) -> None:  # noqa: F811
    from axe_playwright_python.sync_playwright import Axe

    page = browser.new_page(color_scheme=scheme)
    try:
        page.goto(f"{site_url}tools/{tool}/")
        page.wait_for_selector(f"#{TOOLS[tool]}[data-ready='true']")
        page.click("#load-example")
        page.wait_for_timeout(200)
        violations = Axe().run(page, context=".md-content").response["violations"]
        assert not violations, [(v["id"], v["nodes"][0]["target"], v["nodes"][0]["failureSummary"]) for v in violations]
    finally:
        page.close()


@pytest.mark.parametrize("tool", sorted(TOOLS))
def test_keyboard_reaches_and_uses_the_example_button(page, site_url, tool) -> None:  # noqa: F811
    page.goto(f"{site_url}tools/{tool}/")
    app = page.locator(f"#{TOOLS[tool]}")
    page.wait_for_selector(f"#{TOOLS[tool]}[data-ready='true']")
    before = app.inner_text()
    for _ in range(300):                                                  # Tab through the page from the top
        page.keyboard.press("Tab")
        if page.evaluate("document.activeElement && document.activeElement.id") == "load-example":
            break
    else:
        pytest.fail("the example button cannot be reached with Tab")
    page.keyboard.press("Enter")
    page.wait_for_timeout(200)
    assert app.inner_text() != before                                     # the tool responded to the keyboard
    # every control in the tool can take keyboard focus
    unfocusable = page.evaluate(
        f"""Array.from(document.querySelectorAll('#{TOOLS[tool]} input, #{TOOLS[tool]} select, #{TOOLS[tool]} button, #{TOOLS[tool]} textarea'))
              .filter(e => e.tabIndex < 0 || e.disabled).map(e => e.id || e.name)""")
    assert not unfocusable, unfocusable
