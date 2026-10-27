"""
pages/fs09/components/review_step.py - Step 3: Payment Review & Authorization Component.
Encapsulates review summary items, charge verification, and payment authorization action.
Complies strictly with Invariant 1 (Zero assertions in Page Objects/Components).
"""
from typing import Any, Dict
from playwright.sync_api import Page
from pages.fs09.locators import BillingPaymentLocators as Loc


class PaymentReviewStep:
    """Component managing Step 3: Payment Review, Authorization, and Confirmation."""

    def __init__(self, page: Page):
        self.page = page

    def is_loaded(self) -> bool:
        """Check if Step 3 (Payment Review & Authorization) is currently active."""
        return self.page.locator(Loc.REVIEW_HEADING).is_visible()

    def wait_for_loaded(self, timeout: int = 10000) -> None:
        """Wait for the Step 3 review heading to be visible."""
        self.page.wait_for_selector(Loc.REVIEW_HEADING, timeout=timeout)

    def get_review_summary(self) -> Dict[str, Any]:
        """
        Extract review details:
        - List of charges in the review table (Description, Net Amount)
        - Key-value summary items (Total, EA Balance, Payment Method, Funding allocations)
        """
        details: Dict[str, Any] = {
            "charges": [],
            "items": {},
        }

        # Extract review charges table
        rows = self.page.locator("table tbody tr")
        count = rows.count()
        for i in range(count):
            row = rows.nth(i)
            cells = row.locator("td")
            if cells.count() >= 2:
                details["charges"].append({
                    "description": cells.nth(0).inner_text().strip(),
                    "net_amount": cells.nth(1).inner_text().strip(),
                    "due_date": cells.nth(2).inner_text().strip() if cells.count() >= 3 else "",
                })

        # Extract dl dt/dd items in the review layout
        dl_items = self.page.locator("[class*='reviewLayout'] dl div, [class*='reviewLayout'] dl [class*='item']")
        for i in range(dl_items.count()):
            item = dl_items.nth(i)
            dt = item.locator("dt").first
            dd = item.locator("dd").first
            if dt.count() > 0 and dd.count() > 0:
                details["items"][dt.inner_text().strip()] = dd.inner_text().strip()

        return details

    def click_confirm_pay(self) -> None:
        """Click the Confirm and Pay button to submit the payment."""
        self.page.locator(Loc.CONFIRM_PAY_BTN).first.click()

    def click_back(self) -> None:
        """Click Back on Step 3 to return to Step 2."""
        self.page.locator(Loc.STEP3_BACK_BTN).first.click()

    def is_pay_button_disabled(self) -> bool:
        """Check if the Authorize and Pay button is disabled."""
        btn = self.page.locator(Loc.CONFIRM_PAY_BTN).first
        return not btn.is_enabled() if btn.count() > 0 else True

    def is_pay_button_loading(self) -> bool:
        """Check if the Authorize and Pay button is currently in a loading state."""
        btn = self.page.locator(Loc.CONFIRM_PAY_BTN).first
        if btn.count() == 0:
            return False
        aria_busy = btn.get_attribute("aria-busy")
        has_spinner = btn.locator("[class*='spinner'], svg").count() > 0
        return aria_busy == "true" or has_spinner
