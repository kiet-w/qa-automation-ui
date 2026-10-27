"""
pages/fs08/singpass_login_page.py - Page Object Model for Singpass Login & Mockpass Portal.
Compliant with Framework Invariant 1 (Zero assertions in Page Objects).
"""
import os
from typing import Any, Dict, Optional
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError

from pages.base_page import BasePage


class SingpassLoginPage(BasePage):
    """Page Object for Singpass Login, MockPass Simulator, and Callback error handling."""

    URL_PATH = "/parent/login"

    # Landing Page Locators
    LOGIN_WITH_SINGPASS_BTN = "button:has-text('Sign in with Singpass')"
    HEADING = "h2:has-text('Parent portal login')"
    DESCRIPTION = "p:has-text('Use Singpass')"

    # Mockpass Simulator Locators (:5156)
    MOCKPASS_TAB_APP = "button[role='tab']:has-text('Singpass app')"
    MOCKPASS_TAB_PASSWORD = "button[role='tab']:has-text('Password login')"
    MOCKPASS_CITIZEN_SELECT = "select"
    MOCKPASS_SUBMIT_BTN = "button:has-text('Log in with Singpass')"
    MOCKPASS_PASSWORD_NRIC_INPUT = "input[name='singpass-id']"
    MOCKPASS_PASSWORD_INPUT = "input[type='password']"
    MOCKPASS_PASSWORD_SUBMIT_BTN = "button[type='submit']:has-text('Log in')"

    # Callback Page Locators (/parent/callback)
    CALLBACK_ALERT = "div[role='alert']"
    CALLBACK_HEADING = "div[role='alert'] h2, main h2"
    CALLBACK_STATUS_MSG = "p[role='status']"

    # Shell Navigation & Session
    LOGOUT_BTN = "header button:has-text('Log out'), button[class*='_desktopLogout_']"
    BRAND_LOGO = "header a:has-text('EduSave E-Service')"
    SESSION_EXPIRED_DIALOG = "div[role='dialog']:has-text('Session expired'), div[role='dialog']"
    SESSION_EXPIRED_ACTION_BTN = "div[role='dialog'] button:has-text('Sign in again')"

    def __init__(self, page: Page):
        super().__init__(page)
        self.portal_base_url = os.environ.get("BASE_URL", "http://localhost:5174").rstrip("/")

    def open(self, base_url: Optional[str] = None):
        """Open the parent portal login page and ensure clean unauthenticated state."""
        target_base = (base_url or self.portal_base_url).rstrip("/")
        self.page.goto(f"{target_base}{self.URL_PATH}")
        try:
            # Wait for either Login button or Logout button if auto-redirected to home
            self.page.wait_for_selector(f"{self.LOGIN_WITH_SINGPASS_BTN}, header button:has-text('Log out')", timeout=10000)
        except Exception:
            pass
        if self.page.locator("header button:has-text('Log out')").count() > 0:
            self.logout()
        self.page.evaluate("() => { try { localStorage.clear(); sessionStorage.clear(); } catch(e){} }")
        self.page.wait_for_selector(self.LOGIN_WITH_SINGPASS_BTN, timeout=10000)

    def is_login_page_loaded(self) -> bool:
        """Check if login landing page is rendered."""
        return self.is_visible(self.LOGIN_WITH_SINGPASS_BTN) and self.is_visible(self.HEADING)

    def get_heading_text(self) -> str:
        """Return heading text on landing page."""
        return self.page.locator(self.HEADING).inner_text()

    def click_sign_in_with_singpass(self):
        """Click 'Sign in with Singpass' to navigate to MockPass simulator."""
        self.page.click(self.LOGIN_WITH_SINGPASS_BTN)

    def select_mockpass_persona(self, keyword_or_nric: str):
        """Select test citizen persona from dropdown matching keyword or NRIC."""
        self.page.wait_for_selector(self.MOCKPASS_CITIZEN_SELECT)
        self.page.evaluate("""(keyword) => {
            const select = document.querySelector('select');
            if (!select) return;
            const opt = Array.from(select.options).find(o => 
                o.text.toLowerCase().includes(keyword.toLowerCase()) || 
                o.value.toLowerCase().includes(keyword.toLowerCase())
            );
            if (opt) {
                select.value = opt.value;
                select.dispatchEvent(new Event('change', { bubbles: true }));
            }
        }""", keyword_or_nric)

    def submit_mockpass_login(self):
        """Click submit button on Mockpass app tab."""
        self.page.wait_for_selector(self.MOCKPASS_SUBMIT_BTN)
        self.page.click(self.MOCKPASS_SUBMIT_BTN)

    def login_via_password_tab(self, nric: str, password: str = "password123"):
        """Use Mockpass password tab to submit a specific arbitrary NRIC."""
        self.page.wait_for_selector(self.MOCKPASS_TAB_PASSWORD)
        self.page.click(self.MOCKPASS_TAB_PASSWORD)
        self.page.wait_for_selector(self.MOCKPASS_PASSWORD_NRIC_INPUT)
        self.page.fill(self.MOCKPASS_PASSWORD_NRIC_INPUT, nric)
        if self.is_visible(self.MOCKPASS_PASSWORD_INPUT):
            self.page.fill(self.MOCKPASS_PASSWORD_INPUT, password)
        self.page.click(self.MOCKPASS_PASSWORD_SUBMIT_BTN)

    def login_with_persona(self, persona_keyword: str, base_url: Optional[str] = None):
        """Complete standard end-to-end login flow using MockPass App tab."""
        self.open(base_url=base_url)
        self.click_sign_in_with_singpass()
        self.select_mockpass_persona(persona_keyword)
        self.submit_mockpass_login()
        # Await completion of OAuth callback redirect to landing portal
        try:
            if "LIM SHU XIN" not in persona_keyword and "INVALID" not in persona_keyword:
                self.page.wait_for_selector("h1:has-text('EduSave E-Service Portal')", timeout=25000)
            else:
                self.page.wait_for_selector(self.CALLBACK_ALERT, timeout=15000)
        except Exception:
            pass

    def is_callback_alert_visible(self, timeout: int = 5000) -> bool:
        """Check if an error alert is displayed on the callback page."""
        try:
            self.page.wait_for_selector(self.CALLBACK_ALERT, timeout=timeout)
            return True
        except PlaywrightTimeoutError:
            return False

    def get_callback_alert_text(self) -> str:
        """Retrieve the alert message text on callback failure."""
        if self.is_callback_alert_visible():
            return self.page.locator(self.CALLBACK_ALERT).inner_text().strip()
        return ""

    def get_callback_status_text(self) -> str:
        """Retrieve the auto-redirect status countdown text on callback page."""
        try:
            self.page.wait_for_selector(self.CALLBACK_STATUS_MSG, timeout=3000)
            return self.page.locator(self.CALLBACK_STATUS_MSG).inner_text().strip()
        except PlaywrightTimeoutError:
            return ""

    def logout(self):
        """Click logout button in header shell."""
        try:
            mobile_nav = self.page.locator("button[aria-label='Open navigation']")
            if mobile_nav.count() > 0 and mobile_nav.first.is_visible():
                mobile_nav.first.click(timeout=1500)
        except Exception:
            pass
        logout_btn = self.page.locator("button:has-text('Log out')").first
        if logout_btn.count() > 0:
            logout_btn.click(timeout=5000)
            try:
                self.page.wait_for_selector(self.LOGIN_WITH_SINGPASS_BTN, timeout=10000)
            except Exception:
                pass

    def is_logged_in(self) -> bool:
        """Check if user session is active (Logout button or Brand header is present)."""
        return self.is_visible(self.LOGOUT_BTN) or self.is_visible(self.BRAND_LOGO)

    def inject_session_storage(self, user_data: Dict[str, Any]):
        """Inject user auth session directly into browser window.sessionStorage for fast setup."""
        import json
        payload_json = json.dumps(user_data)
        self.page.evaluate(f"""() => {{
            window.sessionStorage.setItem('edusave.parent-auth.user', JSON.stringify({payload_json}));
        }}""")

    def is_session_expired_dialog_open(self, timeout: int = 3000) -> bool:
        """Check if ExpiredSessionDialog modal is visible."""
        try:
            loc = self.page.locator(self.SESSION_EXPIRED_DIALOG)
            return loc.count() > 0 and loc.first.is_visible(timeout=timeout)
        except Exception:
            return False

    def get_session_expired_dialog_text(self) -> str:
        """Retrieve text inside the session expired modal."""
        if self.is_session_expired_dialog_open():
            return self.page.locator(self.SESSION_EXPIRED_DIALOG).first.inner_text().strip()
        return ""

    def click_session_expired_action(self):
        """Click 'Sign in again' in the session expired dialog."""
        self.page.wait_for_selector(self.SESSION_EXPIRED_ACTION_BTN)
        self.page.click(self.SESSION_EXPIRED_ACTION_BTN)
