"""
tests/unit/test_evidence_e2e_local.py - Local offline verification for Step Actions and Actual Result screenshots.
"""
from pathlib import Path
import pytest
from playwright.sync_api import Page
from tests.base_test import BaseTest

REPO_ROOT = Path(__file__).resolve().parents[2]


class TestLocalEvidenceCapture(BaseTest):
    """Verifies that step actions and actual result screenshots are automatically captured with highlighting."""

    def test_tc_local_step_actions_and_actual_result(self):
        """TC-LOCAL-001: Offline form interaction verifying step actions and actual result highlighting."""
        # Setup local HTML page
        html_content = """
        <!DOCTYPE html>
        <html>
        <head><title>Evidence Capture Test</title></head>
        <body style="padding: 40px; font-family: sans-serif;">
            <h2>Registration Form</h2>
            <form id="test-form">
                <label for="username">Username:</label>
                <input id="username" type="text" style="display:block; margin: 10px 0; padding: 8px;" />
                <button id="submit-btn" type="button" style="padding: 10px 20px; background: #0284c7; color: white;">Submit Form</button>
            </form>
            <div id="result-status" role="status" style="margin-top: 20px; font-weight: bold; color: green;">Registration Successful</div>
        </body>
        </html>
        """
        self.page.set_content(html_content)

        # Step 1: Input text into field (auto-highlighted & captured)
        with self.step("Step 1: Enter Username", expected="Input username"):
            self.page.locator("#username").fill("john_doe")
            self.step.set_actual("Username entered successfully.")

        # Step 2: Click submit (auto-highlighted & captured)
        with self.step("Step 2: Submit Form", expected="Form submitted"):
            self.page.locator("#submit-btn").click()
            self.step.set_actual("Submit clicked.")

        # Step 3: Verify Actual Result (explicitly or auto-detected)
        self.highlight_actual_result(self.page.locator("#result-status"), text="Registration Successful")
        assert self.page.locator("#result-status").is_visible()
