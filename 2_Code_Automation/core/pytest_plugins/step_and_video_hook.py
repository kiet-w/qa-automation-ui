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
from reporting.core.sanitizer import clean_error_message

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
        setattr(item, "_has_failed", True)
        exc = call.excinfo.value if call.excinfo else None
        if exc is not None:
            setattr(item, "_failure_exc", exc)
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
    elif report.when == "setup" and report.failed:
        setattr(item, "_has_failed", True)
        if call.excinfo and call.excinfo.value:
            setattr(item, "_failure_exc", call.excinfo.value)

    if hasattr(report, "wasxfail") and report.wasxfail:
        item.user_properties.append(("wasxfail", str(report.wasxfail)))
        if hasattr(item, "funcargs") and "json_metadata" in item.funcargs:
            jm = item.funcargs["json_metadata"]
            if isinstance(jm, dict):
                jm["wasxfail"] = str(report.wasxfail)


def _highlight_failure_in_browser(page: Optional[Page], step_title: str, error_msg: str):
    """
    Highlights the defective / failing UI element in the browser DOM before capturing screenshot and video
    using SketchVLM-style SVG primitives, directional arrows, and diagnostic evidence cards.
    """
    if not page:
        return
    try:
        from core.sketch_annotator import SketchAnnotator
        SketchAnnotator.highlight_defect(page, step_title=step_title, error_msg=error_msg, hold_ms=3000)
    except Exception:
        pass


class StepTracker:
    """Tracks and records execution steps, statuses, durations, and screenshots."""

    def __init__(self, page: Page, json_metadata=None, reports_dir=None, test_name: str = "", node=None):
        self.page = page
        self.node = node
        self.json_metadata = json_metadata if json_metadata is not None else {}
        if "steps" not in self.json_metadata:
            self.json_metadata["steps"] = []
        self.steps = self.json_metadata["steps"]
        self.reports_dir = Path(reports_dir) if reports_dir else DEFAULT_REPORTS_DIR
        self.screenshots_dir = self.reports_dir / "screenshots"
        self.test_name = test_name
        self.test_slug = re.sub(r"[^\w]+", "_", test_name.lower()).strip("_") if test_name else ""
        self.test_screenshots_dir = self.screenshots_dir / self.test_slug if self.test_slug else self.screenshots_dir
        self.test_screenshots_dir.mkdir(parents=True, exist_ok=True)
        self.current_step = None
        self._step_counter = 0
        self._step_stack = []
        self.test_start_time = time.time()
        self._attach_navigation_listener(self.page)

    def _attach_navigation_listener(self, page: Optional[Page]):
        """Persist active Step HUD across page.goto and SPA navigations."""
        if not page:
            return
        try:
            if page.is_closed() or getattr(page, "_qa_hud_listener_attached", False):
                return

            def _restore_hud(*args, **kwargs):
                try:
                    if page.is_closed() or not self.current_step:
                        return
                    step_title = self.current_step.get("title", "")
                    step_idx = self.current_step.get("step_index", self._step_counter)
                    if step_title:
                        from core.sketch_annotator import SketchAnnotator
                        SketchAnnotator.show_step_hud(page, step_title=step_title, step_index=step_idx)
                except Exception:
                    pass

            def _on_nav(frame):
                try:
                    if frame == page.main_frame:
                        _restore_hud()
                except Exception:
                    pass

            page.on("framenavigated", _on_nav)
            page.on("domcontentloaded", _restore_hud)
            setattr(page, "_qa_hud_listener_attached", True)
        except Exception:
            pass

    def set_page(self, page: Page):
        """Update current active page for taking screenshots when switching context or tab."""
        self.page = page
        self._attach_navigation_listener(page)

    def attach_screenshot(self, path: str):
        """Attach a screenshot file path to the current active step (or most recent step)."""
        if self.current_step is not None:
            self.current_step["screenshot"] = str(path)
        elif self.steps:
            self.steps[-1]["screenshot"] = str(path)

    def set_actual(self, actual_text: str, locator: Optional[Any] = None):
        """Set actual execution outcome description and optional locator for the current step."""
        if self.current_step is not None:
            self.current_step["actual"] = actual_text
            if locator is not None:
                self.current_step["actual_locator"] = locator
        if self.node:
            if locator is not None:
                setattr(self.node, "_qa_actual_locator", locator)
            if actual_text:
                setattr(self.node, "_qa_actual_text", actual_text)

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

    def set_actual(self, actual_text: str, locator: Optional[Any] = None):
        self.tracker.set_actual(actual_text, locator=locator)

    def set_expected(self, expected_text: str):
        self.tracker.set_expected(expected_text)

    def __enter__(self):
        self.tracker._step_counter += 1
        self.step_index = self.tracker._step_counter
        self.start_time = time.time()
        start_offset = max(0.0, round(self.start_time - self.tracker.test_start_time, 2))

        if self.page is not None:
            self.tracker.set_page(self.page)

        active_page = self.page or self.tracker.page
        if active_page:
            self.tracker._attach_navigation_listener(active_page)

        self.step_data = {
            "title": self.title,
            "step_index": self.step_index,
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

        if active_page:
            try:
                from core.sketch_annotator import SketchAnnotator
                SketchAnnotator.show_step_hud(active_page, self.title, self.step_index)
            except Exception:
                pass

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
            clean_err = clean_error_message(str(exc_val))
            self.step_data["error"] = clean_err
            self.step_data["actual"] = f"FAILED: {clean_err}"

            fail_filename = f"fail_{prefix}step_{self.step_index}_{timestamp}.png"
            fail_path = self.tracker.screenshots_dir / fail_filename
            try:
                rel_fail_path = str(fail_path.relative_to(WORKSPACE_DIR))
            except Exception:
                rel_fail_path = str(fail_path)
            try:
                if active_page and not active_page.is_closed():
                    _highlight_failure_in_browser(active_page, step_title=self.title, error_msg=clean_err)
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

        # Auto-capture screenshot for EVERY step ("lúc thực hiện/nhập" và "lúc pass/kết quả")
        should_capture = True

        if should_capture and not self.step_data.get("screenshot"):
            step_filename = f"step_{self.step_index}.png"
            step_path = self.tracker.test_screenshots_dir / step_filename
            legacy_filename = f"{prefix}step_{self.step_index}_{timestamp}.png"
            legacy_path = self.tracker.screenshots_dir / legacy_filename
            try:
                rel_step_path = str(step_path.relative_to(WORKSPACE_DIR))
            except Exception:
                rel_step_path = str(step_path)
            try:
                if active_page and not active_page.is_closed():
                    active_page.screenshot(path=str(step_path), full_page=False)
                    try:
                        shutil.copy2(step_path, legacy_path)
                    except Exception:
                        pass
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
    return StepTracker(page=page, json_metadata=json_metadata, reports_dir=reports_dir, test_name=test_name, node=request.node)
