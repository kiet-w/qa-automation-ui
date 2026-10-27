"""
pages/fs03/admin_login_page.py - Page Object for Admin Portal Login & SSO Authentication.
Complies with Invariant 1 (Zero assertions in Page Objects).
"""
from pathlib import Path
from typing import Optional
from playwright.sync_api import Page
from pages.base_page import BasePage

WORKSPACE_DIR = Path(__file__).resolve().parents[2]
AUTH_STATE_PATH = WORKSPACE_DIR / "data" / "fs03" / "auth_state.json"


class AdminLoginPage(BasePage):
    """Encapsulates interaction with the EduFAMS Admin Portal Login page and Microsoft SSO."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.sign_in_with_microsoft_btn = self.page.locator("button:has-text('Sign in with Microsoft')")
        self.username_input = self.page.locator("input[placeholder*='username' i]")
        self.password_input = self.page.locator("input[type='password']")
        self.sign_in_btn = self.page.locator("button[type='submit']")
        self.admin_tile = self.page.locator(".account-tile:has-text('admin@IAM.edu.vn'), [onclick*='admin@IAM.edu.vn']")
        self.portal_header = self.page.locator("text=EduFAMS Admin Portal")

    def open(self, base_url: str = "http://localhost:5173") -> None:
        """Navigate to admin login page."""
        self.page.goto(f"{base_url}/login")
        self.page.wait_for_load_state("domcontentloaded")

    def login_with_microsoft_as_admin(self, base_url: str = "http://localhost:5173") -> None:
        """
        Authenticate as MOE HQ Admin (admin@IAM.edu.vn) via Microsoft Entra Simulator.
        Saves storage_state to reuse session across test runs.
        """
        if not ("login" in self.page.url or self.sign_in_with_microsoft_btn.is_visible()):
            self.open(base_url)

        self.sign_in_with_microsoft_btn.wait_for(state="visible", timeout=10000)
        self.sign_in_with_microsoft_btn.click()

        # Wait for Microsoft Entra Simulator
        self.page.wait_for_url("**/microsoft-provider/**", timeout=15000)
        self.admin_tile.first.wait_for(state="visible", timeout=10000)
        self.admin_tile.first.click()

        # Wait for landing on admin portal
        self.portal_header.wait_for(state="visible", timeout=20000)
        self.page.wait_for_load_state("domcontentloaded")

        # Save auth state
        try:
            AUTH_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
            self.page.context.storage_state(path=str(AUTH_STATE_PATH))
        except Exception:
            pass

    def is_logged_in(self) -> bool:
        """Check if currently authenticated by looking for admin portal banner."""
        return "login" not in self.page.url and self.portal_header.is_visible()
