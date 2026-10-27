"""
pages/fs09/payment_result_page.py - Page Object for Payment Result (/payment-result).
Encapsulates receipt presentation, settlement status, funding sources breakdown,
and automated reversal notifications.
Complies strictly with Invariant 1 (Zero assertions in Page Objects).
"""
import os
from typing import Any, Dict, List, Optional
from playwright.sync_api import Locator, Page

from pages.base_page import BasePage


class PaymentResultPage(BasePage):
    """Page Object for /payment-result receipt and outcome view."""

    URL_PATH = "/payment-result"

    # Headings
    PAGE_HEADING = "h1#payment-result-heading"
    INVALID_HEADING = "h1#payment-result-invalid-heading"

    # Status Banner
    RESULT_STATUS_BANNER = "div[class*='resultStatus']"
    STATUS_HEADING = "div[class*='resultStatus'] h2"
    STATUS_DESCRIPTION = "div[class*='resultStatus'] p:first-of-type"
    EA_REVERSAL_NOTICE = (
        "div[class*='resultStatus'] p:has-text('returned'), "
        "div[class*='resultStatus'] p:has-text('Education Account has been returned'), "
        "div[class*='resultStatus'] p:has-text('refunded')"
    )
    EA_DEDUCTION_PENDING_NOTICE = "div[class*='resultStatus'] p:has-text('still be deducted')"

    # Receipt Description List
    RECEIPT_CARD = "article[class*='resultCard'], [class*='resultCard']"
    DESCRIPTION_LIST = "dl"
    DESCRIPTION_ITEMS = "dl div, dl [class*='item']"

    # Specific Receipt Field Selectors (Labels & Values)
    TRANSACTION_ID_VALUE = "dt:has-text('Transaction ID') + dd, dt:has-text('Transaction') + dd"
    INVOICE_NUMBER_VALUE = "dt:has-text('Invoice number') + dd, dt:has-text('Invoice') + dd"
    INVOICE_STATUS_VALUE = "dt:has-text('Invoice status') + dd"
    COMPLETED_AT_VALUE = "dt:has-text('Completed at') + dd"
    REQUESTED_AMOUNT_VALUE = "dt:has-text('Requested amount') + dd"
    SETTLED_AMOUNT_VALUE = "dt:has-text('Settled amount') + dd"

    # Invoice Line Items
    INVOICE_ITEMS_LIST = "ul[class*='invoiceItems'] > li"

    # Actions
    HOME_LINK = "a[class*='homeLink'], a:has-text('Home'), a[href='/']"
    BILLING_LINK = "a:has-text('Billing'), a[href='/billing']"
    PRINT_RECEIPT_BTN = "button:has-text('Print receipt'), button:has-text('Print')"
    RETRY_BTN = "button:has-text('Retry')"

    # Errors & Loading
    ALERT = "div[role='alert']"
    LOADING_INDICATOR = "div[role='status']"

    def __init__(self, page: Page):
        super().__init__(page)
        self.portal_base_url = os.environ.get("BASE_URL", "http://localhost:5174").rstrip("/")

    def open(self, base_url: Optional[str] = None) -> "PaymentResultPage":
        """Navigate to the payment result page directly."""
        target_base = (base_url or self.portal_base_url).rstrip("/")
        self.page.goto(f"{target_base}{self.URL_PATH}")
        self.wait_for_result_loaded()
        return self

    def wait_for_result_loaded(self, timeout: int = 15000) -> None:
        """Wait for result banner, invalid heading, or error alert to appear."""
        try:
            # Wait for loading indicator to detach if present
            loading = self.page.locator("div[role='status']")
            if loading.count() > 0:
                loading.first.wait_for(state="detached", timeout=timeout)
        except Exception:
            pass

        self.page.wait_for_selector(
            f"{self.RESULT_STATUS_BANNER}, {self.INVALID_HEADING}, {self.ALERT}",
            timeout=timeout,
        )

    def wait_for_terminal_status(self, timeout: int = 15000) -> str:
        """Wait for result to transition out of pending into a terminal status (success/failure/reconciliation)."""
        try:
            self.page.locator(
                "div[class*='resultStatus']:not([class*='pending']), "
                "div[class*='resultStatus'] h2:not(:has-text('processed'))"
            ).first.wait_for(state="visible", timeout=timeout)
        except Exception:
            pass
        return self.get_result_tone()

    def is_loaded(self) -> bool:
        """Check if payment result page or invalid context view is visible."""
        return self.is_visible(self.PAGE_HEADING) or self.is_visible(self.INVALID_HEADING)

    def get_result_title(self) -> str:
        """Return the outcome heading text from the result status banner."""
        loc = self.page.locator(self.STATUS_HEADING)
        return loc.inner_text().strip() if loc.count() > 0 else ""

    def get_result_description(self) -> str:
        """Return the outcome descriptive message from the result status banner."""
        loc = self.page.locator(self.STATUS_DESCRIPTION)
        return loc.inner_text().strip() if loc.count() > 0 else ""

    def get_result_tone(self) -> str:
        """
        Extract the tone style indicator of the result status banner.
        Returns one of: 'success' | 'failure' | 'reconciliation' | 'pending' | 'unknown'
        """
        banner = self.page.locator(self.RESULT_STATUS_BANNER).first
        if banner.count() == 0:
            return "unknown"
        title = self.get_result_title().lower()
        if "succeeded" in title or "success" in title:
            return "success"
        if "reconciliation" in title:
            return "reconciliation"
        if "failed" in title or "failure" in title or "cancelled" in title:
            return "failure"
        if "processing" in title or "processed" in title:
            return "pending"
        class_attr = banner.get_attribute("class") or ""
        for tone in ("success", "failure", "reconciliation", "pending"):
            if tone in class_attr.lower():
                return tone
        return "unknown"

    def has_ea_reversal_notice(self) -> bool:
        """Check if the education account refund/reversal notice is displayed."""
        return self.is_visible(self.EA_REVERSAL_NOTICE)

    def get_ea_reversal_text(self) -> str:
        """Return the text of the EA reversal notice paragraph."""
        loc = self.page.locator(self.EA_REVERSAL_NOTICE)
        return loc.inner_text().strip() if loc.count() > 0 else ""

    def has_ea_deduction_pending_notice(self) -> bool:
        """Check if notice that EA deduction may still have occurred is displayed."""
        return self.is_visible(self.EA_DEDUCTION_PENDING_NOTICE)

    def get_receipt_details(self) -> Dict[str, str]:
        """
        Extract all key-value items from the primary receipt description list.
        Includes Transaction ID, Invoice number, Invoice status, Completed at,
        Requested amount, and Settled amount.
        """
        details: Dict[str, str] = {}
        card = self.page.locator(self.RECEIPT_CARD).first
        items = card.locator("dl > div, dl > [class*='item']") if card.count() > 0 else self.page.locator("dl > div, dl > [class*='item']")
        count = items.count()

        for i in range(count):
            item = items.nth(i)
            dt = item.locator("dt").first
            dd = item.locator("dd").first
            if dt.count() > 0 and dd.count() > 0:
                details[dt.inner_text().strip()] = dd.inner_text().strip()

        # Direct lookups as backup
        if "Transaction ID" not in details:
            tid_loc = self.page.locator(self.TRANSACTION_ID_VALUE)
            if tid_loc.count() > 0:
                details["Transaction ID"] = tid_loc.first.inner_text().strip()

        if "Invoice number" not in details:
            inv_loc = self.page.locator(self.INVOICE_NUMBER_VALUE)
            if inv_loc.count() > 0:
                details["Invoice number"] = inv_loc.first.inner_text().strip()

        if "Invoice status" not in details:
            inv_status_loc = self.page.locator(self.INVOICE_STATUS_VALUE)
            if inv_status_loc.count() > 0:
                details["Invoice status"] = inv_status_loc.first.inner_text().strip()

        if "Requested amount" not in details:
            req_loc = self.page.locator(self.REQUESTED_AMOUNT_VALUE)
            if req_loc.count() > 0:
                details["Requested amount"] = req_loc.first.inner_text().strip()

        if "Settled amount" not in details:
            set_loc = self.page.locator(self.SETTLED_AMOUNT_VALUE)
            if set_loc.count() > 0:
                details["Settled amount"] = set_loc.first.inner_text().strip()

        return details

    def get_funding_sources_details(self) -> List[Dict[str, str]]:
        """
        Extract details of each funding source row (e.g., Education Account, Online Gateway).
        Returns a list of dicts with: label, requested_amount, settled_amount, raw_value.
        """
        sources: List[Dict[str, str]] = []
        card = self.page.locator(self.RECEIPT_CARD).first
        items = card.locator("dl > div, dl > [class*='item']") if card.count() > 0 else self.page.locator("dl > div, dl > [class*='item']")
        count = items.count()

        for i in range(count):
            item = items.nth(i)
            dt = item.locator("dt").first
            dd = item.locator("dd").first
            if dt.count() > 0 and dd.count() > 0:
                label = dt.inner_text().strip()
                val = dd.inner_text().strip()
                # Funding sources have format: "<Method> — <Status>"
                if "—" in label or "Education Account" in label or "Online Gateway" in label:
                    sources.append({
                        "label": label,
                        "raw_value": val,
                    })

        return sources

    def get_invoice_items(self) -> List[Dict[str, str]]:
        """
        Extract items from the invoice line items list if an invoice was generated.
        """
        items_list: List[Dict[str, str]] = []
        rows = self.page.locator(self.INVOICE_ITEMS_LIST)
        count = rows.count()
        for i in range(count):
            row = rows.nth(i)
            row_dict: Dict[str, str] = {}
            dl_items = row.locator("dl div, dl [class*='item']")
            dl_count = dl_items.count()
            for j in range(dl_count):
                item = dl_items.nth(j)
                dt = item.locator("dt")
                dd = item.locator("dd")
                if dt.count() > 0 and dd.count() > 0:
                    row_dict[dt.inner_text().strip()] = dd.inner_text().strip()
            if row_dict:
                items_list.append(row_dict)
        return items_list

    def click_home(self) -> None:
        """Click the link returning to the home portal."""
        self.click_element(self.HOME_LINK)

    def has_print_receipt_button(self) -> bool:
        """Check if the Print Receipt button is visible."""
        return self.is_visible(self.PRINT_RECEIPT_BTN)

    def click_print_receipt(self) -> None:
        """Click the Print Receipt button."""
        self.click_element(self.PRINT_RECEIPT_BTN)

    def has_error_alert(self) -> bool:
        """Check if an error alert is visible."""
        return self.is_visible(self.ALERT)

    def get_error_alert_text(self) -> Optional[str]:
        """Get the text of the error alert if visible."""
        loc = self.page.locator(self.ALERT)
        if loc.count() > 0 and loc.first.is_visible():
            return loc.first.inner_text().strip()
        return None

    def click_retry(self) -> None:
        """Click retry button on error."""
        self.click_element(self.RETRY_BTN)
