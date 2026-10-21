"""
core/pytest_plugins/step_and_video_hook.py - StepTracker execution timeline, evidence capture,
and pytest_runtest_makereport error classification hook.
"""
import os
from pathlib import Path
import re
import time
from typing import Optional, Any
import pytest
from playwright.sync_api import Page
from core.catalog import classify
from core.exceptions import BusinessAssertionError, InfrastructureError

REPO_ROOT = Path(__file__).resolve().parents[2]
WORKSPACE_DIR = REPO_ROOT
DEFAULT_REPORTS_DIR = WORKSPACE_DIR / "reports"


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Centrally capture test execution failure outcomes.
    Differentiates between business assertion failures, infrastructure exceptions,
    and unhandled Playwright technical errors, attaching diagnostic category and hint to test metadata.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        exc = call.excinfo.value if call.excinfo else None
        if exc is not None:
            if isinstance(exc, (BusinessAssertionError, AssertionError)):
                category = "BUSINESS_ASSERTION"
                hint = "Business expectation failed; actual application state did not match specification."
            elif isinstance(exc, InfrastructureError):
                category = getattr(exc, "category", "INFRASTRUCTURE")
                hint = getattr(exc, "hint", "Infrastructure error occurred during test execution.")
            else:
                category, hint = classify(exc)

            item.user_properties.append(("error_category", category))
            item.user_properties.append(("error_hint", hint))

            if hasattr(item, "funcargs") and "json_metadata" in item.funcargs:
                jm = item.funcargs["json_metadata"]
                if isinstance(jm, dict):
                    jm["error_category"] = category
                    jm["error_hint"] = hint

    if hasattr(report, "wasxfail") and report.wasxfail:
        item.user_properties.append(("wasxfail", str(report.wasxfail)))
        if hasattr(item, "funcargs") and "json_metadata" in item.funcargs:
            jm = item.funcargs["json_metadata"]
            if isinstance(jm, dict):
                jm["wasxfail"] = str(report.wasxfail)


def _highlight_failure_in_browser(page: Optional[Page], step_title: str, error_msg: str):
    """
    Highlights the defective / failing UI element in the browser DOM before capturing screenshot and video.
    - Accurately targets the tested input field (e.g. mobile number '71234567', invalid email, boundary street).
    - Dismisses any unwanted modal dialog / backdrop covering the form so the defective field is visible.
    - Scrolls the defective field into the center of the viewport.
    - Injects high-contrast red outline, floating defect badge, and top diagnostic evidence banner.
    - Holds the frame for 1.2s so the recorded WebM video shows the highlighted defect clearly.
    """
    if not page:
        return
    try:
        if page.is_closed():
            return
        clean_err = error_msg.splitlines()[0] if error_msg else "Assertion / Execution Failure"
        clean_err = clean_err.replace("\\", "\\\\").replace('"', '\\"').replace("'", "\\'")
        clean_title = step_title.replace("\\", "\\\\").replace('"', '\\"').replace("'", "\\'")

        page.evaluate(f"""(() => {{
            // 1. Inject Top Diagnostic Banner
            let banner = document.getElementById('__qa_evidence_banner__');
            if (!banner) {{
                banner = document.createElement('div');
                banner.id = '__qa_evidence_banner__';
                banner.style.position = 'fixed';
                banner.style.top = '0';
                banner.style.left = '0';
                banner.style.right = '0';
                banner.style.zIndex = '2147483647';
                banner.style.background = 'linear-gradient(90deg, #cf222e 0%, #b31d28 100%)';
                banner.style.color = '#ffffff';
                banner.style.padding = '8px 16px';
                banner.style.fontFamily = '-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif';
                banner.style.fontSize = '13px';
                banner.style.fontWeight = 'bold';
                banner.style.display = 'flex';
                banner.style.alignItems = 'center';
                banner.style.justifyContent = 'space-between';
                banner.style.boxShadow = '0 4px 14px rgba(207, 34, 46, 0.4)';
                banner.style.borderBottom = '2px solid rgba(255, 255, 255, 0.6)';
                document.body.appendChild(banner);
            }}
            banner.innerHTML = `
                <div style="display:flex;align-items:center;gap:8px;">
                    <span style="background:#ffffff;color:#cf222e;padding:2px 6px;border-radius:3px;font-size:11px;font-weight:900;">DEFECT EVIDENCE</span>
                    <span style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:65vw;">{clean_err[:120]}</span>
                </div>
                <span style="font-size:11px;opacity:0.9;font-weight:normal;">Step: {clean_title[:45]}</span>
            `;

            // 2. Identify candidate failure elements with smart context detection
            const contextText = (`{clean_title} {clean_err}`).toLowerCase();

            // Extract quoted tokens like '71234567' or '7' from error/title
            const tokens = [];
            const quoteRegex = /['"]([^'"]+)['"]/g;
            let match;
            while ((match = quoteRegex.exec(`{clean_title} {clean_err}`)) !== null) {{
                if (match[1].trim()) tokens.push(match[1].trim());
            }}

            let targetEl = null;
            let defectDescription = "POINT OF DEFECT / ASSERTION";

            // (A) Priority 1: Match input whose value contains one of the tested tokens (e.g. 71234567)
            const allInputs = Array.from(document.querySelectorAll('input, textarea, select'));
            for (const input of allInputs) {{
                const val = (input.value || "").trim();
                if (!val) continue;
                for (const tok of tokens) {{
                    if (val === tok || val.includes(tok) || tok.includes(val)) {{
                        targetEl = input;
                        defectDescription = `DEFECT: Value "${{val}}" accepted without validation`;
                        break;
                    }}
                }}
                if (targetEl) break;
            }}

            // (B) Priority 2: Semantic field mapping from error & step keywords
            if (!targetEl) {{
                let semanticSelector = null;
                if (/phone|mobile|prefix|7/.test(contextText)) {{
                    semanticSelector = "input[name='phoneNumber'], input[type='tel'], input[name*='phone' i], input[name*='mobile' i]";
                    defectDescription = "DEFECT: Invalid Mobile Phone Number";
                }} else if (/email|mail/.test(contextText)) {{
                    semanticSelector = "input[name='email'], input[type='email'], input[name*='email' i]";
                    defectDescription = "DEFECT: Invalid Email Address";
                }} else if (/postal|zip/.test(contextText)) {{
                    semanticSelector = "input[name*='postal' i], input[name*='zip' i]";
                    defectDescription = "DEFECT: Postal Code";
                }} else if (/street|address/.test(contextText)) {{
                    semanticSelector = "input[name*='street' i], input[name*='address' i]";
                    defectDescription = "DEFECT: Street Address";
                }} else if (/block/.test(contextText)) {{
                    semanticSelector = "input[name*='block' i]";
                    defectDescription = "DEFECT: Block Number";
                }} else if (/nric/.test(contextText)) {{
                    semanticSelector = "[data-testid='nric'], input[name*='nric' i]";
                    defectDescription = "DEFECT: NRIC Identity Field";
                }}

                if (semanticSelector) {{
                    const found = document.querySelector(semanticSelector);
                    if (found) {{
                        targetEl = found;
                        const val = (targetEl.value || "").trim();
                        if (val) {{
                            defectDescription = `DEFECT: Value "${{val}}" accepted without validation`;
                        }}
                    }}
                }}
            }}

            // (C) Priority 3: Native / ARIA invalid attributes
            if (!targetEl) {{
                const candidateSelectors = [
                    ':invalid',
                    '[aria-invalid="true"]',
                    '.is-invalid',
                    '.error-message',
                    '.field-error',
                    '.invalid-feedback',
                    '[role="alert"]',
                    '.text-danger',
                    '.toast-error'
                ];
                for (const sel of candidateSelectors) {{
                    const el = document.querySelector(sel);
                    if (el && el.offsetParent !== null) {{
                        targetEl = el;
                        defectDescription = "DEFECT: Validation Failure";
                        break;
                    }}
                }}
            }}

            // (D) Handle obstructive modal/dialog:
            // If an unwanted modal dialog is covering the target element on the form,
            // dismiss / hide the modal so the form field is clearly visible!
            const modalDialog = document.querySelector('div[role="alertdialog"], [aria-modal="true"], .modal');
            if (modalDialog && targetEl && !modalDialog.contains(targetEl)) {{
                // The dialog popped up when it shouldn't have!
                // Dismiss modal to reveal the defective input field behind it:
                modalDialog.style.display = 'none';
                document.querySelectorAll('.fixed.inset-0, [class*="backdrop" i]').forEach(b => {{
                    b.style.display = 'none';
                }});
            }}

            // (E) Priority 4: Fallback to activeElement ONLY IF no modal button
            if (!targetEl && document.activeElement && document.activeElement !== document.body) {{
                const tag = document.activeElement.tagName.toLowerCase();
                if (tag === 'input' || tag === 'textarea' || tag === 'select') {{
                    targetEl = document.activeElement;
                }}
            }}

            // (F) Highlight the target element!
            if (targetEl) {{
                targetEl.scrollIntoView({{ behavior: 'instant', block: 'center' }});
                targetEl.style.outline = '4px solid #cf222e';
                targetEl.style.outlineOffset = '4px';
                targetEl.style.boxShadow = '0 0 24px rgba(207, 34, 46, 0.9)';
                targetEl.style.backgroundColor = 'rgba(207, 34, 46, 0.12)';

                // Add floating pointer badge directly above the element
                let badge = document.getElementById('__qa_target_badge__');
                if (!badge) {{
                    badge = document.createElement('div');
                    badge.id = '__qa_target_badge__';
                    badge.style.position = 'absolute';
                    badge.style.background = '#cf222e';
                    badge.style.color = '#ffffff';
                    badge.style.fontSize = '12px';
                    badge.style.fontWeight = 'bold';
                    badge.style.padding = '4px 10px';
                    badge.style.borderRadius = '4px';
                    badge.style.zIndex = '2147483647';
                    badge.style.boxShadow = '0 3px 10px rgba(0,0,0,0.4)';
                    document.body.appendChild(badge);
                }}
                badge.textContent = defectDescription;
                const rect = targetEl.getBoundingClientRect();
                badge.style.top = Math.max(45, window.scrollY + rect.top - 30) + 'px';
                badge.style.left = Math.max(10, window.scrollX + rect.left) + 'px';
            }}
        }})();""")
        page.wait_for_timeout(1200)
    except Exception:
        pass


class StepTracker:
    """Tracks and records execution steps, statuses, durations, and screenshots."""

    def __init__(self, page: Page, json_metadata=None, reports_dir=None, test_name: str = ""):
        self.page = page
        self.json_metadata = json_metadata if json_metadata is not None else {}
        if "steps" not in self.json_metadata:
            self.json_metadata["steps"] = []
        self.steps = self.json_metadata["steps"]
        self.reports_dir = Path(reports_dir) if reports_dir else DEFAULT_REPORTS_DIR
        self.screenshots_dir = self.reports_dir / "screenshots"
        self.test_name = test_name
        self.test_slug = re.sub(r"[^\w]+", "_", test_name.lower()).strip("_") if test_name else ""
        self.current_step = None
        self._step_counter = 0
        self._step_stack = []
        self.test_start_time = time.time()

    def set_page(self, page: Page):
        """Update current active page for taking screenshots when switching context or tab."""
        self.page = page

    def attach_screenshot(self, path: str):
        """Attach a screenshot file path to the current active step (or most recent step)."""
        if self.current_step is not None:
            self.current_step["screenshot"] = str(path)
        elif self.steps:
            self.steps[-1]["screenshot"] = str(path)

    def set_actual(self, actual_text: str):
        """Set actual execution outcome description for the current step."""
        if self.current_step is not None:
            self.current_step["actual"] = actual_text

    def set_expected(self, expected_text: str):
        """Set expected behavior description for the current step."""
        if self.current_step is not None:
            self.current_step["expected"] = expected_text

    def __call__(
        self,
        title: str,
        page: Optional[Page] = None,
        capture_screenshot: bool = False,
        expected: Optional[str] = None,
        actual: Optional[str] = None,
    ):
        """Context manager factory: with step('title', expected=..., actual=...):"""
        return _StepContext(
            tracker=self,
            title=title,
            page=page,
            capture_screenshot=capture_screenshot,
            expected=expected,
            actual=actual,
        )


class _StepContext:
    """Context manager for an individual execution step."""

    def __init__(
        self,
        tracker: StepTracker,
        title: str,
        page: Optional[Page] = None,
        capture_screenshot: bool = False,
        expected: Optional[str] = None,
        actual: Optional[str] = None,
    ):
        self.tracker = tracker
        self.title = title
        self.page = page
        self.capture_screenshot = capture_screenshot
        self.expected = expected
        self.actual = actual
        self.step_data = None
        self.start_time = None
        self.step_index = 0

    def set_page(self, page: Page):
        self.tracker.set_page(page)

    def attach_screenshot(self, path: str):
        self.tracker.attach_screenshot(path)

    def set_actual(self, actual_text: str):
        self.tracker.set_actual(actual_text)

    def set_expected(self, expected_text: str):
        self.tracker.set_expected(expected_text)

    def __enter__(self):
        self.tracker._step_counter += 1
        self.step_index = self.tracker._step_counter
        self.start_time = time.time()
        start_offset = max(0.0, round(self.start_time - self.tracker.test_start_time, 2))

        if self.page is not None:
            self.tracker.set_page(self.page)

        self.step_data = {
            "title": self.title,
            "status": "passed",
            "duration": 0.0,
            "start_offset": start_offset,
            "end_offset": start_offset,
            "expected": self.expected,
            "actual": self.actual,
            "screenshot": None,
            "error": None,
        }
        self.tracker.steps.append(self.step_data)
        self.tracker._step_stack.append(self.step_data)
        self.tracker.current_step = self.step_data
        return self.tracker

    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = round(time.time() - self.start_time, 2)
        self.step_data["duration"] = duration
        self.step_data["end_offset"] = round(self.step_data["start_offset"] + duration, 2)

        self.tracker.screenshots_dir.mkdir(parents=True, exist_ok=True)
        timestamp = int(time.time() * 1000)
        prefix = f"{self.tracker.test_slug}_" if self.tracker.test_slug else ""
        active_page = self.page or self.tracker.page

        if exc_type is not None:
            self.step_data["status"] = "failed"
            self.step_data["error"] = str(exc_val)
            self.step_data["actual"] = f"FAILED: {str(exc_val)}"

            fail_filename = f"fail_{prefix}step_{self.step_index}_{timestamp}.png"
            fail_path = self.tracker.screenshots_dir / fail_filename
            try:
                rel_fail_path = str(fail_path.relative_to(WORKSPACE_DIR))
            except Exception:
                rel_fail_path = str(fail_path)
            try:
                if active_page and not active_page.is_closed():
                    _highlight_failure_in_browser(active_page, step_title=self.title, error_msg=str(exc_val))
                    active_page.screenshot(path=str(fail_path), full_page=False)
                    self.step_data["screenshot"] = rel_fail_path
            except Exception:
                pass

            if self.tracker._step_stack:
                self.tracker._step_stack.pop()
            self.tracker.current_step = (
                self.tracker._step_stack[-1] if self.tracker._step_stack else None
            )
            return False  # Propagate exception to pytest

        if not self.step_data.get("actual"):
            self.step_data["actual"] = "Passed: Step completed successfully."

        if self.capture_screenshot and not self.step_data.get("screenshot"):
            step_filename = f"{prefix}step_{self.step_index}_{timestamp}.png"
            step_path = self.tracker.screenshots_dir / step_filename
            try:
                rel_step_path = str(step_path.relative_to(WORKSPACE_DIR))
            except Exception:
                rel_step_path = str(step_path)
            try:
                if active_page and not active_page.is_closed():
                    active_page.screenshot(path=str(step_path), full_page=False)
                    self.step_data["screenshot"] = rel_step_path
            except Exception:
                pass

        if self.tracker._step_stack:
            self.tracker._step_stack.pop()
        self.tracker.current_step = (
            self.tracker._step_stack[-1] if self.tracker._step_stack else None
        )
        return False


@pytest.fixture
def step(request, page: Page, json_metadata):
    """Fixture providing an isolated StepTracker instance for each test method."""
    reports_dir = getattr(request.config, "_ticket_reports_dir", DEFAULT_REPORTS_DIR)
    test_name = request.node.name
    return StepTracker(page=page, json_metadata=json_metadata, reports_dir=reports_dir, test_name=test_name)
