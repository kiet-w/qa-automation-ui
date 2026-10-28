"""
pages/fs03/admin_login_page.py - Page Object for Admin Portal Login & SSO Authentication.
Complies with Invariant 1 (Zero assertions in Page Objects) and line limit (<200 lines).
"""
from pathlib import Path
from typing import Optional
from playwright.sync_api import Locator, Page
from pages.base_page import BasePage
from pages.fs03.locators import AdminLoginLocators, MicrosoftSimulatorLocators, AdminShellLocators

WORKSPACE_DIR = Path(__file__).resolve().parents[2]
AUTH_STATE_PATH = WORKSPACE_DIR / "data" / "fs03" / "auth_state.json"


class AdminLoginPage(BasePage):
    """Encapsulates interaction with the EduFAMS Admin Portal Login page and Microsoft SSO."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.sign_in_with_microsoft_btn = self.page.locator(AdminLoginLocators.SIGN_IN_MICROSOFT_BTN)
        self.username_input = self.page.locator(AdminLoginLocators.USERNAME_INPUT)
        self.password_input = self.page.locator(AdminLoginLocators.PASSWORD_INPUT)
        self.sign_in_btn = self.page.locator(AdminLoginLocators.SIGN_IN_BTN)
        self.language_select = self.page.locator(AdminLoginLocators.LANGUAGE_SELECT)
        self.mock_role_select = self.page.locator(AdminLoginLocators.MOCK_ROLE_SELECT)
        self.password_toggle_btn = self.page.locator(AdminLoginLocators.PASSWORD_TOGGLE_BTN)
        self.heading = self.page.locator(AdminLoginLocators.PAGE_HEADING)
        self.mock_alert = self.page.locator(AdminLoginLocators.MOCK_ALERT)
        self.error_alert = self.page.locator(AdminLoginLocators.ALERT)
        self.error_alert_failed = self.page.locator(AdminLoginLocators.ALERT_FAILED)
        self.admin_tile = self.page.locator(MicrosoftSimulatorLocators.MOEHQ_ACCOUNT_TILE)
        self.portal_header = self.page.locator(AdminShellLocators.PORTAL_HEADER)
        self.dashboard_shell = self.page.locator(AdminShellLocators.DASHBOARD_SHELL)
        self.callback_status = self.page.locator(AdminShellLocators.CALLBACK_STATUS)

    def open(self, base_url: str = "http://localhost:5173") -> None:
        """Navigate to admin login page."""
        self.page.goto(f"{base_url}/login", wait_until="domcontentloaded")

    def click_sign_in_with_microsoft(self) -> None:
        """Trigger Microsoft SSO flow with hydration safety."""
        self.sign_in_with_microsoft_btn.wait_for(state="visible", timeout=10000)
        self.page.wait_for_timeout(500)
        self.sign_in_with_microsoft_btn.click()

    def fill_credentials(self, username: Optional[str] = None, password: Optional[str] = None) -> None:
        """Fill Basic Auth / Mock credentials without submitting."""
        if username is not None:
            self.username_input.fill(username)
        if password is not None:
            self.password_input.fill(password)

    def select_language(self, language: str) -> None:
        """Select language by value or visible label."""
        self.language_select.wait_for(state="visible", timeout=10000)
        target = "vi-VN" if "vi" in language.lower() else "en-US"
        try:
            self.language_select.select_option(value=target)
        except Exception:
            self.language_select.select_option(label=language)

    def select_mock_role(self, role: str) -> None:
        """Select Mock Role (e.g. 'MOEHQ', 'SCHOOL')."""
        self.mock_role_select.select_option(value=role)

    def submit_credentials(self) -> None:
        """Click submit button for basic/mock login."""
        self.sign_in_btn.click()

    def toggle_password_visibility(self) -> None:
        """Click password visibility toggle button."""
        self.password_toggle_btn.click()

    def get_password_input_type(self) -> str:
        """Return input type attribute ('password' or 'text')."""
        return self.password_input.get_attribute("type") or "password"

    def get_username_value(self) -> str:
        """Return currently entered username."""
        return self.username_input.input_value()

    def get_alert_text(self) -> str:
        """Return alert message text if present."""
        if self.error_alert.count() > 0 and self.error_alert.first.is_visible():
            return self.error_alert.first.inner_text()
        return ""

    def login_with_microsoft_as_admin(self, base_url: str = "http://localhost:5173") -> None:
        """
        Authenticate as MOE HQ Admin (admin@IAM.edu.vn) via Microsoft Entra Simulator.
        Saves storage_state to reuse session across test runs.
        """
        if not ("login" in self.page.url or self.sign_in_with_microsoft_btn.is_visible()):
            self.open(base_url)

        self.sign_in_with_microsoft_btn.wait_for(state="visible", timeout=10000)
        self.page.wait_for_timeout(500)
        self.sign_in_with_microsoft_btn.click()

        self.page.wait_for_url("**/microsoft-provider/**", timeout=15000)
        self.admin_tile.first.wait_for(state="visible", timeout=10000)
        self.admin_tile.first.click()

        self.portal_header.first.wait_for(state="visible", timeout=20000)
        self.page.wait_for_load_state("domcontentloaded")

        try:
            AUTH_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
            self.page.context.storage_state(path=str(AUTH_STATE_PATH))
        except Exception:
            pass

    def is_logged_in(self) -> bool:
        """Check if currently authenticated by looking for admin portal banner."""
        return "login" not in self.page.url and self.portal_header.is_visible()
