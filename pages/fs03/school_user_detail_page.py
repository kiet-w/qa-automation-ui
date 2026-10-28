"""
pages/fs03/school_user_detail_page.py - Page Object for School User Detail (/school-user-management/:id)
plus route-agnostic sensitive-surface inspection helpers used by SUM-010 / SUM-067 security audits.
Complies with Invariant 1 (Zero assertions in Page Objects) and ADR-0006.
Source: specs/ui_bsk/localhost-5173/academic-and-users/04_school_user_management.md §1.3/§4.
"""
import json
from typing import Dict, List, Optional
from playwright.sync_api import Locator, Page, Response
from pages.base_page import BasePage
from pages.fs03.school_user_mgmt_locators import SchoolUserDetailLocators as L


class SchoolUserDetailPage(BasePage):
    """Page Object for the detail/assignment screen and cross-screen PII/password inspection."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page_heading: Locator = self.page.locator(L.PAGE_HEADING)
        self.back_to_list_button: Locator = self.page.locator(L.BACK_TO_LIST)
        self.account_card: Locator = self.page.locator(L.ACCOUNT_CARD)
        self.profile_card: Locator = self.page.locator(L.PROFILE_CARD)
        self.school_card: Locator = self.page.locator(L.SCHOOL_CARD)
        self.school_combobox: Locator = self.page.locator(L.SCHOOL_COMBOBOX)
        self.assign_button: Locator = self.page.locator(L.ASSIGN_BUTTON)
        self.password_fields: Locator = self.page.locator(L.PASSWORD_FIELDS)
        self._api_bodies: List[str] = []
        self._api_capture_pattern: Optional[str] = None

    # --- Navigation ---
    def open(self, base_url: str = "http://localhost:5173", user_id: str = "") -> None:
        """Navigate to a school-user detail screen with session recovery."""
        target_url = f"{base_url}/school-user-management/{user_id}" if user_id else f"{base_url}/school-user-management"
        self.page.goto(target_url, wait_until="domcontentloaded")
        try:
            self.page.wait_for_selector(
                "section h2, button:has-text('Sign in with Microsoft')", timeout=5000
            )
        except Exception:
            pass
        if "login" in self.page.url:
            from pages.fs03.admin_login_page import AdminLoginPage
            AdminLoginPage(self.page).login_with_microsoft_as_admin(base_url=base_url)
            self.page.goto(target_url, wait_until="domcontentloaded")
        self.wait_for_loaded()

    def wait_for_loaded(self, timeout: int = 10000) -> None:
        """Wait until a detail card or the page heading is mounted."""
        self.page.wait_for_selector(
            "section:has(h2), h1", timeout=timeout
        )

    def get_user_id_from_url(self) -> str:
        """Extract the trailing :id segment from the current URL (empty for /new or list)."""
        tail = self.page.url.rstrip("/").split("/")[-1]
        return "" if tail in ("new", "school-user-management", "") else tail

    # --- State reading ---
    def get_account_card_text(self) -> str:
        """Return User account card text (code, username, name, email, role, status)."""
        return self.account_card.first.inner_text().strip() if self.account_card.first.is_visible() else ""

    def get_school_card_text(self) -> str:
        """Return School card text (assigned school details) or empty when unassigned."""
        return self.school_card.first.inner_text().strip() if self.school_card.first.is_visible() else ""

    def is_unassigned(self) -> bool:
        """Return True when no School card with school details is rendered."""
        return not self.school_card.first.is_visible()

    def get_page_text(self) -> str:
        """Return full visible body text of the current screen."""
        return self.page.locator("body").inner_text()

    # --- Security inspection helpers (route-agnostic) ---
    def count_password_fields(self) -> int:
        """Count password-like inputs rendered on the current screen."""
        return self.password_fields.count()

    def get_storage_dump(self) -> Dict[str, str]:
        """Return localStorage and sessionStorage as flat {store: key=value} maps."""
        raw = self.page.evaluate(
            """() => {
                const out = {};
                for (const store of [window.localStorage, window.sessionStorage]) {
                    const name = store === window.localStorage ? 'localStorage' : 'sessionStorage';
                    for (let i = 0; i < store.length; i++) {
                        const k = store.key(i);
                        out[name + ':' + k] = store.getItem(k);
                    }
                }
                return out;
            }"""
        )
        return raw if isinstance(raw, dict) else {}

    def count_attribute_occurrences(self, value: str) -> int:
        """Count DOM attribute values (excluding input value/placeholder) containing the sentinel."""
        return int(
            self.page.evaluate(
                """(v) => {
                    let hits = 0;
                    document.querySelectorAll('*').forEach(el => {
                        for (const attr of el.attributes) {
                            if (attr.name === 'value' || attr.name === 'placeholder') continue;
                            if (attr.value && attr.value.includes(v)) hits++;
                        }
                    });
                    return hits;
                }""",
                value,
            )
        )

    def start_api_body_capture(self, url_substring: str = "/iam/") -> None:
        """Start collecting response bodies whose URL matches the substring."""
        self._api_bodies = []
        self._api_capture_pattern = url_substring

        def _on_response(resp: Response) -> None:
            if not self._api_capture_pattern or self._api_capture_pattern not in resp.url:
                return
            try:
                self._api_bodies.append(resp.text() or "")
            except Exception:
                self._api_bodies.append("")

        self.page.on("response", _on_response)

    def get_captured_api_bodies(self) -> List[str]:
        """Return response bodies collected since start_api_body_capture()."""
        return list(self._api_bodies)

    def get_storage_as_text(self) -> str:
        """Return concatenated storage dump as JSON text for sentinel scans."""
        return json.dumps(self.get_storage_dump(), ensure_ascii=False)
