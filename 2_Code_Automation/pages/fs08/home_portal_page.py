"""
pages/fs08/home_portal_page.py - Page Object Model for EduSave E-Service Parent Home Portal.
Compliant with Framework Invariant 1 (Zero assertions in Page Objects).
"""
import os
from typing import Any, Dict, List, Optional
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError

from pages.base_page import BasePage


class HomePortalPage(BasePage):
    """Page Object encapsulating Home Portal child cards, EA balances, and navigation."""

    URL_PATH = "/"

    # Header and General Portal Elements
    PORTAL_HEADING = "h1:has-text('EduSave E-Service Portal')"
    CARDS_CONTAINER = "ul[aria-label='Education accounts']"
    CARD_ARTICLES = "ul[aria-label='Education accounts'] article, article[class*='_card_']"

    # Shell Navigation Links
    NAV_HOME = "nav a[href='/']"
    NAV_PROFILE = "nav a[href='/profile']"
    NAV_TRANSACTIONS = "nav a[href='/transactions']"
    NAV_FEES = "nav a[href='/billing']"
    LOGOUT_BTN = "header button:has-text('Log out'), button[class*='_desktopLogout_']"

    # Pagination on Home (if applicable)
    HOME_PAGINATION = "nav[aria-label='Pagination']"

    def __init__(self, page: Page):
        super().__init__(page)
        self.portal_base_url = os.environ.get("BASE_URL", "http://localhost:5174").rstrip("/")

    def open(self, base_url: Optional[str] = None):
        """Open the Home Portal URL directly."""
        target_base = (base_url or self.portal_base_url).rstrip("/")
        self.page.goto(f"{target_base}{self.URL_PATH}")
        self.wait_for_portal_loaded()

    def wait_for_portal_loaded(self, timeout: int = 25000):
        """Wait for home portal heading and accounts list to finish loading (accommodates 10s Gov API sync)."""
        self.page.wait_for_selector(self.PORTAL_HEADING, timeout=timeout)
        try:
            # If "Loading education accounts" is shown, wait for it to detach
            loading = self.page.locator("p[role='status']:has-text('Loading education accounts')")
            if loading.count() > 0:
                loading.wait_for(state="detached", timeout=timeout)
            # Await either cards list or empty state
            self.page.wait_for_selector(f"{self.CARD_ARTICLES}, div[role='status'] strong", timeout=timeout)
            # If "Loading balance" is shown on cards, wait for balances to resolve
            loading_balance = self.page.locator("span[role='status']:has-text('Loading balance')")
            if loading_balance.count() > 0:
                loading_balance.first.wait_for(state="detached", timeout=timeout)
        except Exception:
            pass

    def is_portal_loaded(self) -> bool:
        """Check if portal main heading is visible."""
        return self.is_visible(self.PORTAL_HEADING)

    def get_portal_heading_text(self) -> str:
        """Get portal header title text."""
        return self.page.locator(self.PORTAL_HEADING).inner_text().strip()

    def get_child_cards_count(self) -> int:
        """Return total number of child cards displayed on Home."""
        cards = self.page.locator(self.CARD_ARTICLES)
        return cards.count()

    def get_child_card_data(self, index: int = 0) -> Dict[str, Any]:
        """Extract data attributes from a single child card by index."""
        cards = self.page.locator(self.CARD_ARTICLES)
        if index >= cards.count():
            return {}

        card = cards.nth(index)
        full_text = card.inner_text()

        # Extract title link / child name
        card_link = card.locator("a[class*='_cardLink_'], h2 a, h3 a, a").first
        child_name = card_link.inner_text().strip() if card_link.count() > 0 else ""
        link_href = card_link.get_attribute("href") if card_link.count() > 0 else ""

        # Extract status badge (Active / Due for closure / Closed)
        status = "Unknown"
        for st in ("Active", "Due for closure", "Closed", "Not eligible", "To be created", "Not yet 7"):
            if st in full_text:
                status = st
                break

        # Check for EA balance SGD
        balance_text = ""
        balance_locator = card.locator("button:has-text('EA balance'), dt:has-text('EA balance') + dd, dt:has-text('EA Balance') + dd")
        if balance_locator.count() > 0:
            try:
                balance_locator.first.locator("span[role='status']").wait_for(state="detached", timeout=6000)
            except Exception:
                pass
            balance_text = balance_locator.first.inner_text().strip()

        # Check for Masked NRIC
        masked_nric = ""
        nric_locator = card.locator("button:has-text('NRIC'), dt:has-text('NRIC') + dd")
        if nric_locator.count() > 0:
            masked_nric = nric_locator.first.inner_text().strip()

        return {
            "name": child_name,
            "href": link_href,
            "status": status,
            "balance_text": balance_text,
            "masked_nric": masked_nric,
            "raw_text": full_text,
        }

    def get_all_child_cards(self) -> List[Dict[str, Any]]:
        """Extract information from all child cards on the Home Portal."""
        count = self.get_child_cards_count()
        return [self.get_child_card_data(i) for i in range(count)]

    def click_child_card_link(self, index: int = 0):
        """Click on the child card link to view student transactions."""
        cards = self.page.locator(self.CARD_ARTICLES)
        if index < cards.count():
            card_link = cards.nth(index).locator("a[class*='_cardLink_'], a").first
            card_link.click()
            self.page.wait_for_load_state("domcontentloaded")

    def navigate_to_profile(self):
        """Click 'My Profile' in header navigation."""
        self.page.click(self.NAV_PROFILE)
        self.page.wait_for_load_state("domcontentloaded")

    def navigate_to_transactions(self):
        """Click 'Transactions' in header navigation."""
        self.page.click(self.NAV_TRANSACTIONS)
        self.page.wait_for_load_state("domcontentloaded")

    def navigate_to_fees(self):
        """Click 'Fees & Payments' in header navigation."""
        self.page.click(self.NAV_FEES)
        self.page.wait_for_load_state("domcontentloaded")

    def get_pending_alerts_count(self) -> int:
        """Query count of yellow pending payment alert boxes."""
        return self.page.locator("div[class*='pending'], div[class*='warning'], div[role='status'][class*='yellow']").count()

    def get_child_card_fee_items_count(self, card_index: int = 0) -> int:
        """Count preview fee items rendered inside a specific child card."""
        cards = self.page.locator(self.CARD_ARTICLES)
        if card_index >= cards.count():
            return 0
        card = cards.nth(card_index)
        return card.locator("ul li, div[class*='feeItem']").count()

    def has_fee_more_link(self, card_index: int = 0) -> bool:
        """Check if '+N more' fees link is visible in a child card."""
        cards = self.page.locator(self.CARD_ARTICLES)
        if card_index >= cards.count():
            return False
        card = cards.nth(card_index)
        return card.locator("text=/\\+\\d+\\s+more/").count() > 0

    def is_pay_fees_action_active(self, card_index: int = 0) -> bool:
        """Check if 'Pay Fees' or payment action is present and enabled in card."""
        cards = self.page.locator(self.CARD_ARTICLES)
        if card_index >= cards.count():
            return False
        card = cards.nth(card_index)
        pay_btn = card.locator("button:has-text('Pay'), a:has-text('Pay')")
        if pay_btn.count() == 0:
            return False
        return not pay_btn.first.is_disabled()

    def is_apply_fas_action_active(self, card_index: int = 0) -> bool:
        """Check if 'Apply FAS' action is present and enabled in card."""
        cards = self.page.locator(self.CARD_ARTICLES)
        if card_index >= cards.count():
            return False
        card = cards.nth(card_index)
        fas_btn = card.locator("button:has-text('FAS'), a:has-text('FAS')")
        if fas_btn.count() == 0:
            return False
        return not fas_btn.first.is_disabled()

    def is_non_citizen_notice_visible(self, card_index: int = 0) -> bool:
        """Check if 'Education Accounts are for Singapore Citizens' notice appears in card or page."""
        cards = self.page.locator(self.CARD_ARTICLES)
        if card_index < cards.count():
            card = cards.nth(card_index)
            if card.locator("text=/Education Accounts are for Singapore Citizens/i").count() > 0:
                return True
        return self.page.locator("text=/Education Accounts are for Singapore Citizens/i").count() > 0

    def get_non_citizen_notice_text(self, card_index: int = 0) -> str:
        """Retrieve non-citizen notice text."""
        loc = self.page.locator("text=/Education Accounts are for Singapore Citizens/i").first
        return loc.inner_text().strip() if loc.count() > 0 else ""

    def is_under_7_notice_visible(self, card_index: int = 0) -> bool:
        """Check if child under 7 notice ('will be opened on') is displayed."""
        cards = self.page.locator(self.CARD_ARTICLES)
        if card_index < cards.count():
            card = cards.nth(card_index)
            if card.locator("text=/opened on|Not yet 7/i").count() > 0:
                return True
        return self.page.locator("text=/opened on|Not yet 7/i").count() > 0

    def is_ea_uninitialized_alert_visible(self) -> bool:
        """Check if MSG-0804 'This student does not have an Education Account.' alert is visible."""
        return self.page.locator("text=/does not have an Education Account/i, div[role='alert']:has-text('Education Account')").count() > 0

    def get_ea_uninitialized_alert_text(self) -> str:
        """Get MSG-0804 alert text."""
        loc = self.page.locator("text=/does not have an Education Account/i, div[role='alert']:has-text('Education Account')").first
        return loc.inner_text().strip() if loc.count() > 0 else ""
