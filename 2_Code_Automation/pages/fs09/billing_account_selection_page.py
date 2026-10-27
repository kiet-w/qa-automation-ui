"""
pages/fs09/billing_account_selection_page.py - Page Object for Education Account Selection (/billing).
Represents the screen where a parent selects an education account to view fees.
Complies strictly with Invariant 1 (Zero assertions in Page Objects).
"""
import os
from typing import Any, Dict, List, Optional
from playwright.sync_api import Locator, Page

from pages.base_page import BasePage


class BillingAccountSelectionPage(BasePage):
    """Page Object for /billing account selection page."""

    URL_PATH = "/billing"

    # Locators
    HEADING = "h1#billing-account-selection-heading"
    PAGE_HEADER = "header[class*='pageHeader']"
    PAGE_DESCRIPTION = "section[aria-labelledby='billing-account-selection-heading'] header p"
    ACCOUNT_GRID = "ul[aria-label='Education accounts'], ul[class*='accountGrid']"
    ACCOUNT_CARD_ARTICLES = (
        "ul[class*='accountGrid'] li article, "
        "ul[aria-label='Education accounts'] li article, "
        "article[class*='accountCard']"
    )
    ACCOUNT_CARDS = "ul[class*='accountGrid'] > li, ul[aria-label='Education accounts'] > li"
    ACCOUNT_LINK_PREFIX = "a:has-text('View fees for'), a:has-text('Select account'), a[class*='accountLink']"

    EMPTY_STATE = "div[class*='accountState'][role='status'], div[role='status']:has-text('No education accounts'), div[role='status']:has-text('No accounts found')"
    LOADING_STATE = "p[class*='accountState'][role='status'], p[role='status']:has-text('Loading education accounts')"
    ERROR_ALERT = "div[role='alert'], [class*='alert']"
    RETRY_BUTTON = "button:has-text('Retry'), button:has-text('Try again')"

    PAGINATION_NAV = "nav[aria-label='Pagination'], nav[class*='pagination']"
    PAGINATION_PREV = "nav[aria-label='Pagination'] button:has-text('Previous')"
    PAGINATION_NEXT = "nav[aria-label='Pagination'] button:has-text('Next')"

    def __init__(self, page: Page):
        super().__init__(page)
        self.portal_base_url = os.environ.get("BASE_URL", "http://localhost:5174").rstrip("/")

    def open(self, base_url: Optional[str] = None) -> "BillingAccountSelectionPage":
        """Navigate to the Billing Account Selection page."""
        target_base = (base_url or self.portal_base_url).rstrip("/")
        self.page.goto(f"{target_base}{self.URL_PATH}")
        self.wait_for_page_loaded()
        return self

    def wait_for_page_loaded(self, timeout: int = 15000) -> None:
        """Wait for either the account list, empty state, or error alert to appear."""
        try:
            # If loading indicator is visible, wait for it to detach
            loading = self.page.locator(self.LOADING_STATE)
            if loading.count() > 0:
                loading.first.wait_for(state="detached", timeout=timeout)
        except Exception:
            pass

        # Wait for any of heading, empty state, or error
        self.page.wait_for_selector(
            f"{self.HEADING}, {self.EMPTY_STATE}, {self.ERROR_ALERT}",
            timeout=timeout,
        )

    def is_loaded(self) -> bool:
        """Check if the billing account selection page heading is visible."""
        return self.is_visible(self.HEADING)

    def get_heading_text(self) -> str:
        """Get the heading text of the account selection page."""
        loc = self.page.locator(self.HEADING)
        return loc.inner_text().strip() if loc.count() > 0 else ""

    def get_description_text(self) -> str:
        """Get the descriptive text under the heading."""
        loc = self.page.locator(self.PAGE_DESCRIPTION)
        return loc.inner_text().strip() if loc.count() > 0 else ""

    def get_account_cards_count(self) -> int:
        """Return total number of account cards displayed."""
        return self.page.locator(self.ACCOUNT_CARD_ARTICLES).count()

    def get_account_names(self) -> List[str]:
        """Return a list of all child / account names displayed in the cards."""
        cards = self.page.locator(self.ACCOUNT_CARD_ARTICLES)
        count = cards.count()
        names: List[str] = []
        for i in range(count):
            card = cards.nth(i)
            # Heading in Card component is usually h2 or h3 or [class*='heading']
            heading = card.locator("h2, h3, [class*='heading']").first
            if heading.count() > 0:
                names.append(heading.inner_text().strip())
            else:
                # Fallback to link text
                link = card.locator(self.ACCOUNT_LINK_PREFIX).first
                if link.count() > 0:
                    names.append(link.inner_text().strip())
        return names

    def get_account_card_data(self, index: int = 0) -> Dict[str, Any]:
        """Extract data attributes from a single account card by index."""
        cards = self.page.locator(self.ACCOUNT_CARD_ARTICLES)
        if index >= cards.count():
            return {}

        card = cards.nth(index)
        full_text = card.inner_text()

        heading = card.locator("h2, h3, [class*='heading']").first
        child_name = heading.inner_text().strip() if heading.count() > 0 else ""

        # Extract account code (e.g., 'Account EDU-2024-001')
        account_code = ""
        code_locator = card.locator("p[class*='accountMeta']:has-text('Account')")
        if code_locator.count() > 0:
            account_code = code_locator.first.inner_text().strip()

        # Extract account status (e.g., 'Status: Active')
        status = ""
        status_locator = card.locator("p[class*='accountMeta']:has-text('Status')")
        if status_locator.count() > 0:
            status = status_locator.first.inner_text().strip()

        # Extract link URL
        link_elem = card.locator("a[class*='accountLink'], a").first
        link_href = link_elem.get_attribute("href") if link_elem.count() > 0 else ""

        return {
            "name": child_name,
            "account_code": account_code,
            "status": status,
            "href": link_href,
            "raw_text": full_text,
        }

    def select_child_by_name(self, child_name: str) -> None:
        """Click the 'View fees for <child_name>' link for the given child."""
        # Find card containing the child name
        cards = self.page.locator(self.ACCOUNT_CARD_ARTICLES)
        count = cards.count()
        for i in range(count):
            card = cards.nth(i)
            if child_name.lower() in card.inner_text().lower():
                link = card.locator("a").first
                link.click()
                return

        # Direct link fallback
        fallback = self.page.locator(f"a:has-text('{child_name}')").first
        fallback.click()

    def select_account_by_index(self, index: int = 0) -> None:
        """Click the selection link on the card at index."""
        cards = self.page.locator(self.ACCOUNT_CARD_ARTICLES)
        if index < cards.count():
            card = cards.nth(index)
            link = card.locator("a").first
            link.click()

    def has_empty_state(self) -> bool:
        """Check if empty state is visible."""
        return self.is_visible(self.EMPTY_STATE)

    def get_empty_state_text(self) -> str:
        """Return the text inside the empty state component."""
        loc = self.page.locator(self.EMPTY_STATE)
        return loc.inner_text().strip() if loc.count() > 0 else ""

    def has_error_alert(self) -> bool:
        """Check if an error alert is displayed."""
        return self.is_visible(self.ERROR_ALERT)

    def get_error_alert_text(self) -> Optional[str]:
        """Return the text inside the error alert if visible."""
        loc = self.page.locator(self.ERROR_ALERT)
        if loc.count() > 0 and loc.first.is_visible():
            return loc.first.inner_text().strip()
        return None

    def click_retry(self) -> None:
        """Click the retry button on error."""
        self.click_element(self.RETRY_BUTTON)

    def has_pagination(self) -> bool:
        """Check if pagination controls are displayed."""
        return self.is_visible(self.PAGINATION_NAV)

    def go_to_page(self, page_number: int) -> None:
        """Click on a specific pagination page number button."""
        btn = self.page.locator(f"{self.PAGINATION_NAV} button:has-text('{page_number}')").first
        btn.click()
