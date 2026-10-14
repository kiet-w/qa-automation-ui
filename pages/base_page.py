"""
pages/base_page.py - Base Page Object providing shared web interactions and utilities.
All specific Page Objects inherit from this class to ensure reusability and consistent behavior.
"""
import os
from pathlib import Path
import time
from typing import Any, Callable, Dict, List, Optional, Union
from playwright.sync_api import ConsoleMessage, Dialog, Error as PlaywrightError, Locator, Page

WORKSPACE_DIR = Path(__file__).resolve().parent.parent




class BasePage:
    """Base class for all Page Objects in the automation framework."""

    def __init__(self, page: Page):
        self.page = page
        self._js_exceptions: List[str] = []
        self._console_errors: List[str] = []
        self._register_technical_listeners()

    def _register_technical_listeners(self) -> None:
        """Passively collect uncaught page errors and console.error messages."""
        try:
            self.page.on("pageerror", self._on_page_error)
            self.page.on("console", self._on_console_message)
        except Exception:
            pass

    def _on_page_error(self, exc: PlaywrightError) -> None:
        self._js_exceptions.append(f"{getattr(exc, 'name', 'Error')}: {getattr(exc, 'message', str(exc))}")

    def _on_console_message(self, msg: ConsoleMessage) -> None:
        try:
            if msg.type == "error":
                self._console_errors.append(msg.text)
        except Exception:
            pass

    def get_technical_snapshot(self) -> Dict[str, List[str]]:
        """Return snapshot of technical/runtime errors observed on the current page."""
        return {
            "js_exceptions": list(self._js_exceptions),
            "console_errors": list(self._console_errors),
        }

    def clear_technical_errors(self) -> None:
        """Reset technical error counters before next step or action."""
        self._js_exceptions.clear()
        self._console_errors.clear()

    def get_a11y_snapshot(self, impact_filter: Optional[List[str]] = None) -> Dict[str, Any]:
        """Scan active DOM using axe-core and return accessibility violations dictionary."""
        try:
            from axe_core_python.sync_playwright import Axe
            results = Axe().run(self.page)
            violations = results.get("violations", [])
            if impact_filter:
                violations = [v for v in violations if v.get("impact") in impact_filter]
            return {
                "violation_count": len(violations),
                "violations": [
                    {
                        "id": v["id"],
                        "impact": v.get("impact"),
                        "description": v.get("description"),
                        "nodes": [n.get("html") for n in v.get("nodes", [])[:3]],
                    }
                    for v in violations
                ],
            }
        except ImportError:
            return {
                "violation_count": 0,
                "violations": [],
                "warning": "axe-core-python is not installed. Install via pip to enable accessibility scanning.",
            }

    def mock_http_response(
        self, url_pattern: str, status: int = 500, body: str = '{"error": "Internal Server Error"}'
    ) -> None:
        """Simulate HTTP error status (500, 502, etc.) or custom payload."""
        def _handle(route):
            route.fulfill(status=status, content_type="application/json", body=body)
        self.page.route(url_pattern, _handle)

    def simulate_network_failure(self, url_pattern: str, error_code: str = "failed") -> None:
        """Simulate network disconnection / abortion (failed, timedout, connectionrefused)."""
        self.page.route(url_pattern, lambda route: route.abort(error_code))

    def navigate(self, url: str, wait_until: str = "domcontentloaded"):
        """Navigate to a specified URL, automatically prepending BASE_URL if relative."""
        target_url = url
        if url.startswith("/") and not url.startswith("//"):
            base_url = os.environ.get("BASE_URL") or getattr(self.page, "_base_url", None)
            if base_url:
                target_url = base_url.rstrip("/") + url
        self.page.goto(target_url, wait_until=wait_until)
        return self

    def get_locator(self, selector_or_locator: Union[str, Locator]) -> Locator:
        """Helper to normalize selector strings or Locator objects."""
        if isinstance(selector_or_locator, str):
            return self.page.locator(selector_or_locator)
        return selector_or_locator

    def wait_for_visible(self, selector_or_locator: Union[str, Locator], timeout: int = 10000) -> Locator:
        """Wait until an element is visible on the page."""
        locator = self.get_locator(selector_or_locator)
        locator.wait_for(state="visible", timeout=timeout)
        return locator

    def click_element(self, selector_or_locator: Union[str, Locator], timeout: int = 10000):
        """Wait for an element to be visible and clickable, then click it."""
        locator = self.wait_for_visible(selector_or_locator, timeout=timeout)
        locator.click()

    def fill_text(self, selector_or_locator: Union[str, Locator], text: str, timeout: int = 10000):
        """Wait for an input element and fill text."""
        locator = self.wait_for_visible(selector_or_locator, timeout=timeout)
        locator.fill(text)

    def get_title(self) -> str:
        """Return the current document title."""
        return self.page.title()

    def get_current_url(self) -> str:
        """Return the current browser URL."""
        return self.page.url

    def wait_for_page_load(self, state: str = "domcontentloaded", timeout: int = 15000):
        """Wait for page load state."""
        self.page.wait_for_load_state(state, timeout=timeout)

    def take_screenshot(self, filepath: Union[str, Path], full_page: bool = False) -> str:
        """Capture screenshot and save to the given file path."""
        path_obj = Path(filepath)
        path_obj.parent.mkdir(parents=True, exist_ok=True)
        self.page.screenshot(path=str(path_obj), full_page=full_page)
        return str(path_obj)

    def handle_next_dialog(self, accept: bool = True, prompt_text: Optional[str] = None):
        """
        Register a one-time event listener to automatically respond to the next browser dialog (alert, confirm, prompt).
        Solves unhandled native dialog blocking or unintended auto-dismissal.
        """
        def _handler(dialog: Dialog):
            try:
                if prompt_text is not None:
                    dialog.accept(prompt_text)
                elif accept:
                    dialog.accept()
                else:
                    dialog.dismiss()
            except Exception:
                pass

        self.page.once("dialog", _handler)
        return self

    def resolve_fixture_path(self, relative_path: Union[str, Path]) -> Path:
        """
        Resolve relative test data/fixture file path to an absolute path.
        Guarantees path resolution across pytest-xdist workers and different CWDs.
        """
        p = Path(relative_path)
        if p.is_absolute() and p.exists():
            return p
        resolved = WORKSPACE_DIR / p
        return resolved

    def scroll_and_click(self, selector_or_locator: Union[str, Locator], timeout: int = 10000):
        """Scroll element smoothly into view, wait until clickable, and click."""
        locator = self.wait_for_visible(selector_or_locator, timeout=timeout)
        locator.scroll_into_view_if_needed()
        self.page.wait_for_timeout(50)
        locator.click()

    def wait_for_condition(
        self, predicate: Callable[[], bool], timeout: int = 10000, interval: int = 200
    ) -> bool:
        """
        Poll a predicate function until it returns True or timeout expires.
        Zero time.sleep; relies on Playwright page.wait_for_timeout for non-blocking event loops.
        """
        start_time = time.time()
        timeout_sec = timeout / 1000.0
        while time.time() - start_time < timeout_sec:
            try:
                if predicate():
                    return True
            except Exception:
                pass
            self.page.wait_for_timeout(interval)
        return bool(predicate())

    def download_file(self, trigger_fn: Callable[[], Any], save_name: Optional[str] = None) -> Path:
        """
        Trigger an action and capture the downloaded file.
        Saves the file to reports/downloads/ and returns its absolute Path.
        """
        downloads_dir = WORKSPACE_DIR / "reports" / "downloads"
        downloads_dir.mkdir(parents=True, exist_ok=True)
        with self.page.expect_download() as download_info:
            trigger_fn()
        download = download_info.value
        filename = save_name or download.suggested_filename
        target_path = downloads_dir / filename
        download.save_as(str(target_path))
        return target_path

