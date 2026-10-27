"""
pages/f10/fas_application_page.py - Page Orchestrator for FAS Direct Application.
Compliant with Invariant 1 (Zero assertions) and Invariant 9 (< 200 lines).
"""
import json
import os
from typing import Any, Dict, Optional
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError

from pages.base_page import BasePage
from pages.f10 import locators
from pages.f10.components.fas_applicant_form import FasApplicantForm
from pages.f10.components.fas_beneficiary_form import FasBeneficiaryForm


class FasApplicationPage(BasePage):
    """Page Orchestrator for the FAS Direct Application Single-Page Form."""

    URL_PATH = "/fas-application"

    DEFAULT_USER = {
        "id": "c51ae3f0-8481-4df9-bc49-eb2591afa912",
        "code": "c51ae3f0-8481-4df9-bc49-eb2591afa912",
        "username": "S7890123F",
        "email": "s7890123f@singpass.local",
        "schoolId": None,
        "roles": [{"id": "01A159A5-0E5F-7C8B-8FA8-ADD41046C499", "code": "ROL-00019", "name": "PARENT"}]
    }

    def __init__(self, page: Page):
        super().__init__(page)
        self.portal_base_url = os.environ.get("BASE_URL", "http://localhost:5174").rstrip("/")
        self.applicant = FasApplicantForm(page)
        self.beneficiary = FasBeneficiaryForm(page)

    def open(self, base_url: Optional[str] = None) -> None:
        """Navigate to FAS application page, injecting mock auth session for fast setup (Invariant 8)."""
        target_base = (base_url or self.portal_base_url).rstrip("/")
        target_url = f"{target_base}{self.URL_PATH}"

        user_json = json.dumps(self.DEFAULT_USER)
        self.page.add_init_script(f"""
            window.sessionStorage.setItem('edusave.parent-auth.user', JSON.stringify({user_json}));
        """)

        self.page.goto(target_url, wait_until="domcontentloaded")
        try:
            self.page.wait_for_selector(locators.APPLICANT_FULL_NAME, timeout=5000)
            return
        except Exception:
            pass

        # Fallback if redirect occurred
        if "login" in self.page.url or self.page.locator("button:has-text('Sign in with Singpass')").count() > 0:
            from pages.fs08.singpass_login_page import SingpassLoginPage
            login = SingpassLoginPage(self.page)
            login.login_with_persona("LIM WEI MINH", base_url=target_base)
            self.page.goto(target_url, wait_until="domcontentloaded")

        self.page.wait_for_selector(locators.APPLICANT_FULL_NAME, timeout=15000)

    def submit(self) -> None:
        """Click the submit application button."""
        self.page.click(locators.BTN_SUBMIT)

    def is_submit_disabled(self) -> bool:
        """Check if submit button is disabled."""
        btn = self.page.locator(locators.BTN_SUBMIT)
        return btn.is_disabled()

    def get_submit_button_text(self) -> str:
        """Get current text of submit button (e.g. Submitting application...)."""
        return self.page.locator(locators.BTN_SUBMIT).inner_text().strip()

    def is_server_error_visible(self, timeout: int = 3000) -> bool:
        """Check if server error alert banner is displayed."""
        try:
            self.page.wait_for_selector(locators.ALERT_SERVER_ERROR, timeout=timeout)
            return True
        except PlaywrightTimeoutError:
            return False

    def get_server_error(self) -> str:
        """Get the error message inside the server error alert."""
        if self.is_server_error_visible():
            return self.page.locator(locators.ALERT_SERVER_ERROR).inner_text().strip()
        return ""

    def is_confirmation_visible(self, timeout: int = 5000) -> bool:
        """Check if application confirmation card is visible."""
        try:
            self.page.wait_for_selector(locators.CONFIRMATION_TITLE, timeout=timeout)
            return True
        except PlaywrightTimeoutError:
            return False

    def get_confirmation_code(self) -> str:
        """Get application reference code from confirmation card."""
        self.page.wait_for_selector(locators.CONFIRMATION_CODE, timeout=5000)
        return self.page.locator(locators.CONFIRMATION_CODE).inner_text().strip()

    def get_confirmation_status(self) -> str:
        """Get status text from confirmation card."""
        self.page.wait_for_selector(locators.CONFIRMATION_STATUS, timeout=5000)
        return self.page.locator(locators.CONFIRMATION_STATUS).inner_text().strip()

    def click_start_new_application(self) -> None:
        """Click the Start a new application button on confirmation card."""
        self.page.click(locators.BTN_START_NEW)
        self.page.wait_for_selector(locators.APPLICANT_FULL_NAME, timeout=10000)
