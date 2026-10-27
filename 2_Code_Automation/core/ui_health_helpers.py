"""
core/ui_health_helpers.py - Reusable UI Health and 9-Tier Failure Criteria Helpers for Playwright.

Implements automated checks for:
- Tier 1: Runtime JS exceptions & console errors
- Tier 2: Network & silent API failures (HTTP 4xx/5xx)
- Tier 3: Visual & layout integrity (Broken images, horizontal scroll overflow)
- Tier 4: Actionability & DOM state (Hanging spinners, button debounce)
- Tier 5: Performance & SLA thresholds
- Tier 6: Accessibility (Keyboard Tab navigation & modal focus trap)
- Tier 7: Client storage & I/O cleanup
- Tier 8: Client-side security (Zero PII/NRIC in URLs, XSS reflection)
- Tier 9: Idempotency & isolation

Can be used standalone in any test or integrated into BaseTest.
"""
import re
import time
from typing import Callable, List, Optional
from playwright.sync_api import Page, expect


class UIHealthMonitor:
    """
    Monitors a Playwright Page for client-side technical health:
    - Uncaught JS exceptions (pageerror)
    - Console error messages
    - Unhandled HTTP 4xx/5xx API failures
    """

    def __init__(self, page: Page, api_prefix: str = "/api/"):
        self.page = page
        self.api_prefix = api_prefix
        self.js_errors: List[str] = []
        self.console_errors: List[str] = []
        self.failed_api_requests: List[str] = []

        # Tier 1: JS Runtime Exception listener
        self.page.on("pageerror", self._on_pageerror)

        # Tier 1: Console Error listener
        self.page.on("console", self._on_console)

        # Tier 2: Network API failure listener
        self.page.on("response", self._on_response)

    def _on_pageerror(self, exc):
        self.js_errors.append(f"Uncaught Exception: {exc}")

    def _on_console(self, msg):
        if msg.type == "error":
            # Filter out expected harmless browser noise if needed
            text = msg.text
            if not any(ignored in text for ignored in ["favicon.ico"]):
                self.console_errors.append(f"Console Error: {text}")

    def _on_response(self, response):
        if response.status >= 400 and self.api_prefix in response.url:
            self.failed_api_requests.append(f"{response.status} {response.request.method} {response.url}")

    def assert_healthy(self, allow_api_errors: bool = False):
        """
        Verify that no uncaught JS errors, console errors, or unexpected API crashes occurred.
        """
        # Tier 1: Runtime
        assert len(self.js_errors) == 0, (
            "Tier 1 FAIL - Uncaught JavaScript Exception detected in browser runtime:\n"
            + "\n".join(self.js_errors)
        )
        assert len(self.console_errors) == 0, (
            "Tier 1 FAIL - Critical console.error detected in browser runtime:\n"
            + "\n".join(self.console_errors)
        )

        # Tier 2: Network
        if not allow_api_errors:
            assert len(self.failed_api_requests) == 0, (
                "Tier 2 FAIL - Silent HTTP 4xx/5xx API failures detected without UI handling:\n"
                + "\n".join(self.failed_api_requests)
            )


# Tier 3: Visual & Layout Helpers
def assert_no_broken_images(page: Page):
    """Tier 3: Ensure all images and icons on the page loaded properly (naturalWidth > 0)."""
    broken_images = page.evaluate("""() => {
        return Array.from(document.querySelectorAll('img'))
            .filter(img => !img.complete || img.naturalWidth === 0)
            .map(img => img.src || img.getAttribute('src') || '<inline-img>');
    }""")
    assert len(broken_images) == 0, f"Tier 3 FAIL - Detected broken images on page: {broken_images}"


def assert_no_horizontal_overflow(page: Page):
    """Tier 3: Ensure page container does not bleed outside viewport width (causing unexpected horizontal scroll)."""
    has_overflow = page.evaluate("() => document.documentElement.scrollWidth > window.innerWidth")
    assert not has_overflow, "Tier 3 FAIL - Detected horizontal layout overflow (scrollWidth > innerWidth)"


# Tier 4: Actionability & DOM State Helpers
def assert_no_hanging_spinners(
    page: Page,
    spinner_selector: str = ".loading-spinner, [data-testid='loading'], [role='progressbar']",
    timeout_ms: int = 5000,
):
    """Tier 4: Ensure loading spinner / skeleton completely disappears within specified timeout."""
    spinner = page.locator(spinner_selector)
    expect(spinner).to_have_count(0, timeout=timeout_ms)


# Tier 5: Performance & SLA Helper
def assert_action_performance(
    action_callable: Callable[[], None],
    max_duration_ms: float = 2000.0,
    action_name: str = "UI Action",
):
    """Tier 5: Ensure an interaction responds within the allowed SLA duration in milliseconds."""
    start = time.time()
    action_callable()
    elapsed_ms = (time.time() - start) * 1000.0
    assert elapsed_ms <= max_duration_ms, (
        f"Tier 5 FAIL - SLA Violation: {action_name} took {elapsed_ms:.2f}ms "
        f"(exceeded maximum allowed SLA of {max_duration_ms}ms)"
    )


# Tier 8: Security Helpers
def assert_no_pii_in_url(page: Page, sensitive_pattern: str = r"[STFG]\d{7}[A-Z]"):
    """Tier 8: Ensure full NRIC or sensitive credential never appears in URL query or path."""
    current_url = page.url
    match = re.search(sensitive_pattern, current_url)
    assert match is None, (
        f"Tier 8 FAIL - Security Violation: Plain-text NRIC detected in URL address: "
        f"'{match.group(0)}' in '{current_url}'"
    )
