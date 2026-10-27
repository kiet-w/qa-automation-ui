"""
pages/fs08/transactions_page.py - Page Object Model for Transactions & Sổ cái Giao dịch.
Compliant with Framework Invariant 1 (Zero assertions in Page Objects).
"""
import os
from typing import Any, Dict, List, Optional
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError

from pages.base_page import BasePage


class TransactionsPage(BasePage):
    """Page Object for Transaction History, Student filtering, and Pagination."""

    URL_PATH = "/transactions"

    # Locators
    HEADING = "h1, h2"
    STUDENT_SELECT = "div[class*='toolbar'] select, select[class*='_select_'], select"
    SUMMARY_REGION = "section[class*='_summary_'], region"
    SUMMARY_BALANCE = "strong:has-text('SGD')"
    SUMMARY_ACCOUNT = "p:has-text('A/C:')"

    # Transaction Table Locators
    TABLE = "table[aria-label='Transaction history'], table"
    TABLE_HEADERS = "table th"
    TABLE_ROWS = "table tbody tr"

    # Pagination and Controls
    ROWS_PER_PAGE_SELECT = "label:has-text('Rows per page') ~ select, select:has(option[value='10'])"
    PAGINATION_PREV = "button:has-text('Previous')"
    PAGINATION_NEXT = "button:has-text('Next')"
    TOTAL_COUNT = "span:has-text('total')"

    # Empty State & Pending Alert
    EMPTY_STATE = "p:has-text('No transactions found'), div:has-text('No transactions found')"
    PENDING_ALERT = "div[class*='pending'], section[class*='pending'], div[class*='_pending_']"
    UNABLE_TO_LOAD = "h3:has-text('Unable to load data'), div:has-text('Unable to load data')"

    def __init__(self, page: Page):
        super().__init__(page)
        self.portal_base_url = os.environ.get("BASE_URL", "http://localhost:5174").rstrip("/")

    def open(self, student_id: Optional[str] = None, base_url: Optional[str] = None):
        """Open transactions page, optionally filtered by student_id."""
        target_base = (base_url or self.portal_base_url).rstrip("/")
        query = f"?student={student_id}" if student_id else ""
        self.page.goto(f"{target_base}{self.URL_PATH}{query}")
        self.wait_for_page_loaded()

    def wait_for_page_loaded(self, timeout: int = 20000):
        """Wait for transactions page heading and dynamic content to finish loading."""
        self.page.wait_for_selector(self.HEADING, timeout=timeout)
        try:
            loading = self.page.locator("p[role='status']").filter(has_text="Loading")
            if loading.count() > 0:
                loading.wait_for(state="detached", timeout=timeout)
        except Exception:
            pass
        try:
            self.page.wait_for_selector(f"{self.STUDENT_SELECT}, {self.TABLE}", timeout=timeout)
        except Exception:
            pass

    def is_student_selector_visible(self, timeout: int = 10000) -> bool:
        """Check if student selector dropdown is visible."""
        try:
            self.page.wait_for_selector(self.STUDENT_SELECT, timeout=timeout)
            return True
        except PlaywrightTimeoutError:
            return False

    def select_student(self, student_name_or_value: str):
        """Switch student filter from combobox."""
        self.page.wait_for_selector(self.STUDENT_SELECT)
        select_locator = self.page.locator(self.STUDENT_SELECT).first
        options = select_locator.locator("option")
        count = options.count()
        matched_val = None
        for i in range(count):
            opt = options.nth(i)
            text = opt.inner_text().strip()
            val = opt.get_attribute("value") or ""
            if student_name_or_value.lower() in text.lower() or student_name_or_value.lower() == val.lower():
                matched_val = val
                break
        if matched_val is not None:
            select_locator.select_option(value=matched_val)
        else:
            select_locator.select_option(index=0)
        self.wait_for_page_loaded()

    def get_summary_balance(self) -> str:
        """Return available balance text displayed in the summary box."""
        if self.is_visible(self.SUMMARY_BALANCE):
            return self.page.locator(self.SUMMARY_BALANCE).first.inner_text().strip()
        return ""

    def get_headers(self) -> List[str]:
        """Return list of column header texts in transaction table."""
        if self.is_visible(self.TABLE):
            headers = self.page.locator(self.TABLE_HEADERS)
            return [headers.nth(i).inner_text().strip() for i in range(headers.count())]
        return []

    def get_transaction_rows(self) -> List[Dict[str, str]]:
        """Extract table rows as structured dictionaries based on current column headers."""
        if not self.is_visible(self.TABLE):
            return []

        headers = self.get_headers()
        rows = self.page.locator(self.TABLE_ROWS)
        results = []

        for i in range(rows.count()):
            row = rows.nth(i)
            cells = row.locator("td")
            cell_count = cells.count()
            row_dict = {}
            for col_idx, header in enumerate(headers):
                if col_idx < cell_count:
                    row_dict[header] = cells.nth(col_idx).inner_text().strip()
            if row_dict:
                results.append(row_dict)

        return results

    def is_prev_disabled(self) -> bool:
        """Check if 'Previous' pagination button is disabled."""
        btn = self.page.locator(self.PAGINATION_PREV)
        return btn.is_disabled() if btn.count() > 0 else True

    def is_next_disabled(self) -> bool:
        """Check if 'Next' pagination button is disabled."""
        btn = self.page.locator(self.PAGINATION_NEXT)
        return btn.is_disabled() if btn.count() > 0 else True

    def get_total_count_text(self) -> str:
        """Get the '{N} total' summary text."""
        if self.is_visible(self.TOTAL_COUNT):
            return self.page.locator(self.TOTAL_COUNT).inner_text().strip()
        return ""

    def is_empty_state_visible(self) -> bool:
        """Check if 'No transactions found.' empty state is visible."""
        return self.is_visible(self.EMPTY_STATE)

    def get_empty_state_text(self) -> str:
        """Get empty state text."""
        if self.is_empty_state_visible():
            return self.page.locator(self.EMPTY_STATE).inner_text().strip()
        return ""

    def is_pending_alert_visible(self) -> bool:
        """Check if pending transaction box is visible."""
        return self.is_visible(self.PENDING_ALERT)

    def get_student_options(self) -> List[str]:
        """Return list of student options rendered in the dropdown."""
        if not self.is_student_selector_visible(timeout=3000):
            return []
        options = self.page.locator(f"{self.STUDENT_SELECT} option")
        return [options.nth(i).inner_text().strip() for i in range(options.count())]

    def is_unable_to_load_visible(self, timeout: int = 8000) -> bool:
        """Check if 'Unable to load data' error state is displayed."""
        try:
            self.page.locator(self.UNABLE_TO_LOAD).first.wait_for(state="visible", timeout=timeout)
            return True
        except Exception:
            return False

    def get_error_panel_text(self) -> str:
        """Retrieve text from error panel on data load rejection."""
        if self.is_unable_to_load_visible():
            return self.page.locator(self.UNABLE_TO_LOAD).first.inner_text().strip()
        return ""
