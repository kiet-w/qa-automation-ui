"""
pages/fs08/transactions_page.py - Page Object Model for Transactions & Sổ cái Giao dịch.
Complies with Invariant 1 (UI actions & state reading only) and Invariant 9 (<200 lines).
"""
import os
from typing import Any, Dict, List, Optional
from playwright.sync_api import Locator, Page, TimeoutError as PlaywrightTimeoutError

from pages.base_page import BasePage
from pages.fs08.locators import TransactionsLocators as Loc
from components.transaction_helper import TransactionHelper


class TransactionsPage(BasePage):
    """Page Object for Transaction History, Student filtering, Disclosures, and Pagination."""

    URL_PATH = "/transactions"
    TABLE = Loc.TABLE
    STUDENT_SELECT = Loc.STUDENT_SELECT
    EMPTY_STATE = Loc.EMPTY_STATE
    PAGE_HEADING = Loc.PAGE_HEADING

    def __init__(self, page: Page):
        super().__init__(page)
        self.portal_base_url = os.environ.get("BASE_URL", "http://localhost:5174").rstrip("/")
        self.grid = TransactionHelper(page, table_selector=Loc.TABLE)

    def open(self, student_id: Optional[str] = None, base_url: Optional[str] = None):
        """Open transactions page, optionally filtered by student_id."""
        target_base = (base_url or self.portal_base_url).rstrip("/")
        query = f"?student={student_id}" if student_id else ""
        self.page.goto(f"{target_base}{self.URL_PATH}{query}")
        self.wait_for_page_loaded()
        return self

    def wait_for_page_loaded(self, timeout: int = 15000):
        """Wait for transactions page heading and dynamic content to finish loading."""
        self.page.wait_for_selector(Loc.PAGE_HEADING, timeout=timeout)
        try:
            loading = self.page.locator(Loc.LOADING_SPINNER)
            if loading.count() > 0:
                loading.wait_for(state="detached", timeout=timeout)
        except Exception:
            pass

    def is_student_selector_visible(self, timeout: int = 5000) -> bool:
        """Check if student selector dropdown is visible."""
        try:
            self.page.wait_for_selector(Loc.STUDENT_SELECT, timeout=timeout)
            return True
        except PlaywrightTimeoutError:
            return False

    def select_student(self, student_name_or_value: str):
        """Switch student filter from combobox."""
        select_locator = self.page.locator(Loc.STUDENT_SELECT).first
        options = select_locator.locator("option")
        matched_val = None
        for i in range(options.count()):
            opt = options.nth(i)
            text = opt.inner_text().strip()
            val = opt.get_attribute("value") or ""
            if student_name_or_value.lower() in text.lower() or student_name_or_value.lower() == val.lower():
                matched_val = val
                break
        select_locator.select_option(value=matched_val if matched_val is not None else "all")
        self.wait_for_page_loaded()

    def get_headers(self) -> List[str]:
        """Return list of column header texts in transaction table."""
        return self.grid.get_headers()

    def get_transaction_rows(self) -> List[Dict[str, str]]:
        """Extract table rows as structured dictionaries based on current column headers."""
        return self.grid.get_rows_data()

    def toggle_invoice_details(self, invoice_number: str, open: bool = True):
        """Click disclosure button on row matching invoice_number to expand/collapse."""
        self.grid.toggle_disclosure(invoice_number, open=open)

    def is_invoice_details_open(self, invoice_number: str) -> bool:
        """Check if row's detail panel is currently expanded."""
        return self.grid.is_disclosure_open(invoice_number)

    def get_funding_sources(self, invoice_id: str) -> List[Dict[str, str]]:
        """Extract funding sources table for the expanded invoice."""
        detail_panel = self.grid.get_disclosure_panel(f"invoice-details-{invoice_id}")
        table = detail_panel.locator(Loc.FUNDING_TABLE).first
        if table.count() == 0 or not table.is_visible():
            return []
        headers = [h.inner_text().strip() for h in table.locator("thead th").all()]
        rows = []
        for r in table.locator("tbody tr").all():
            cells = [c.inner_text().strip() for c in r.locator("th, td").all()]
            rows.append(dict(zip(headers, cells)))
        return rows

    def get_invoice_charges(self, invoice_id: str) -> List[Dict[str, str]]:
        """Extract itemized charges table for the expanded invoice."""
        detail_panel = self.grid.get_disclosure_panel(f"invoice-details-{invoice_id}")
        charges_sec = detail_panel.locator("section[aria-label*='charges']")
        table = charges_sec.locator("table").first
        if table.count() == 0 or not table.is_visible():
            return []
        headers = [h.inner_text().strip() for h in table.locator("thead th").all()]
        rows = []
        for r in table.locator("tbody tr").all():
            cells = [c.inner_text().strip() for c in r.locator("th, td").all()]
            rows.append(dict(zip(headers, cells)))
        return rows

    def select_page_size(self, size: int):
        """Select number of rows per page."""
        self.grid.select_page_size(size)
        self.wait_for_page_loaded()

    def get_error_alert(self) -> Optional[Dict[str, Any]]:
        """Extract information from any active transaction error or warning alert."""
        return self.grid.get_alert_state()

    def click_retry(self):
        """Click retry button on error alert."""
        self.grid.click_retry()
        self.wait_for_page_loaded()

    def is_empty_state_visible(self) -> bool:
        """Check if 'No transactions found.' empty state is visible."""
        empty_state = self.page.locator(Loc.EMPTY_STATE)
        return empty_state.count() > 0 and empty_state.first.is_visible()

    def get_empty_state_text(self) -> str:
        """Get empty state text."""
        empty_state = self.page.locator(Loc.EMPTY_STATE)
        return empty_state.first.inner_text().strip() if empty_state.count() > 0 else ""

    def get_state_snapshot(self) -> Dict[str, Any]:
        """Produce standard snapshot for Exceptor consumption."""
        alert = self.get_error_alert()
        return {
            "success_visible": not bool(alert),
            "visible_errors": {alert["heading"]: alert["message"]} if alert else {},
            "row_count": len(self.get_transaction_rows()),
            "is_empty": self.is_empty_state_visible(),
        }
