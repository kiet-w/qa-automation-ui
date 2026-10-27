"""
tests/unit/test_sketch_annotator.py - Unit tests for SketchAnnotator and SketchVLMOracle.
"""
from pathlib import Path
from unittest.mock import MagicMock
from core.sketch_annotator import SketchAnnotator
from tools.sketch_vlm_oracle import SketchVLMOracle


def test_sketch_annotator_step_hud_handles_none_page():
    # Should not raise exception when page is None
    SketchAnnotator.show_step_hud(None, "Test Step", 1)


def test_sketch_annotator_spotlight_handles_none_page():
    SketchAnnotator.spotlight_action(None, "#button", action_type="click")


def test_sketch_annotator_defect_handles_none_page():
    SketchAnnotator.highlight_defect(None, "Step Title", "Sample Error")


def test_sketch_annotator_clear_handles_none_page():
    SketchAnnotator.clear_overlays(None)


def test_sketch_annotator_invokes_page_evaluate():
    mock_page = MagicMock()
    mock_page.is_closed.return_value = False

    SketchAnnotator.show_step_hud(mock_page, "Step 1: Open Form", 1)
    assert mock_page.evaluate.called


def test_sketch_vlm_oracle_offline_generation(tmp_path: Path):
    dummy_img = tmp_path / "test.png"
    dummy_img.write_bytes(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15c4\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82")

    oracle = SketchVLMOracle(offline_mode=True)
    res = oracle.analyze_screenshot(dummy_img, "Test Failure Context")

    assert res["status"] == "offline_mode"
    assert len(res["annotations"]) >= 3

    svg_content = oracle.render_svg_overlay(res, width=1280, height=720)
    assert "<svg" in svg_content
    assert "</svg>" in svg_content
    assert "qa-sketch-arrowhead" in svg_content or "vlm-arrow" in svg_content


def test_sketch_annotator_content_aware_bounding_box(page):
    """Verifies that wide block containers wrap inner content tightly with 100% transparent fill."""
    page.set_content("""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { margin: 0; font-family: sans-serif; background: #f1f5f9; }
            .full-width-container {
                width: 1200px;
                margin: 40px auto;
                background: #ffffff;
                padding: 40px;
            }
            .error-box {
                max-width: 400px;
                margin: 0 auto;
                padding: 20px;
                background: #fef2f2;
                border: 1px solid #fee2e2;
                border-radius: 8px;
            }
        </style>
    </head>
    <body>
        <div class="full-width-container" role="alert">
            <div class="error-box">
                <h4>Unable to load education accounts</h4>
                <p>System.ResourceNotFound</p>
                <button>Try again</button>
            </div>
        </div>
    </body>
    </html>
    """)

    SketchAnnotator.highlight_defect(
        page,
        step_title="Load accounts",
        error_msg="System.ResourceNotFound: Unable to load education accounts",
        hold_ms=50
    )

    data = page.evaluate("""() => {
        const svg = document.getElementById('__qa_sketch_defect_svg__');
        const badge = document.getElementById('__qa_sketch_defect_badge__');
        const mask = document.getElementById('qa-spotlight-mask');
        let highlightRect = null;
        svg.querySelectorAll('rect').forEach(r => {
            if (r.getAttribute('filter') && r.getAttribute('filter').includes('qa-sketch-glow')) {
                highlightRect = {
                    x: parseFloat(r.getAttribute('x')),
                    y: parseFloat(r.getAttribute('y')),
                    width: parseFloat(r.getAttribute('width')),
                    height: parseFloat(r.getAttribute('height')),
                    fill: r.getAttribute('fill'),
                    stroke: r.getAttribute('stroke')
                };
            }
        });
        const badgeRect = badge ? badge.getBoundingClientRect() : null;
        return {
            hasSvg: !!svg,
            hasMask: !!mask,
            highlightRect: highlightRect,
            badgeRect: badgeRect ? { top: badgeRect.top, height: badgeRect.height } : null
        };
    }""")

    assert data["hasSvg"] is True
    assert data["hasMask"] is True
    assert data["highlightRect"] is not None
    assert data["highlightRect"]["fill"] == "none", "Fill must be 100% transparent"
    assert data["highlightRect"]["stroke"] == "#ef4444"
    # Highlight rect must tightly wrap ~420px content, NOT 1200px container
    assert data["highlightRect"]["width"] < 600, f"Expected < 600, got {data['highlightRect']['width']}"
    assert data["highlightRect"]["width"] > 350

    # Clean overlays
    SketchAnnotator.clear_overlays(page)


def test_step_hud_persistence_on_page_navigation(page, step):
    """Verifies that active Step HUD persists across page.goto and client-side navigations."""
    with step("Step 1: Initial Page"):
        page.goto("data:text/html,<html><body><h1>Initial Page</h1></body></html>")
        hud = page.locator("#__qa_sketch_step_hud__")
        assert hud.is_visible(), "HUD must be visible on initial load"
        assert "Initial Page" in hud.inner_text()

        # Navigate to a new URL inside the step
        page.goto("data:text/html,<html><body><h1>Navigated Page</h1></body></html>")
        hud_after = page.locator("#__qa_sketch_step_hud__")
        assert hud_after.is_visible(), "HUD must persist after page navigation"
        assert "STEP 1" in hud_after.inner_text()
        assert "Initial Page" in hud_after.inner_text()

    with step("Step 2: Second Action"):
        page.goto("data:text/html,<html><body><h1>Second Navigated Page</h1></body></html>")
        hud_step2 = page.locator("#__qa_sketch_step_hud__")
        assert hud_step2.is_visible(), "HUD must be visible in step 2 after navigation"
        assert "STEP 2" in hud_step2.inner_text()
        assert "Second Action" in hud_step2.inner_text()

