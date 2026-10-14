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
