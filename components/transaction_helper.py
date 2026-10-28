"""
components/transaction_helper.py - Reusable Component for Transactional Grids & Flows.

Provides robust tabular data extraction, row disclosure toggling, pagination controls,
and transaction failure diagnostics across transaction history and billing modules.
Complies with Invariant 1 (UI interaction and state reading only; zero assertions).
"""
from typing import Any, Dict, List, Optional, Union
from playwright.sync_api import Locator, Page


class TransactionHelper:
    """Component helper to automate transaction tables, disclosures, and alerts."""

    def __init__(self, page: Page, table_selector: str = "table"):
        self.page = page
        self.table_selector = table_selector

    @property
    def table(self) -> Locator:
        return self.page.locator(self.table_selector).first

    def get_headers(self) -> List[str]:
        """Extract column headers from the transaction table."""
        headers = self.table.locator("thead th, tr:first-child th")
        return [headers.nth(i).inner_text().strip() for i in range(headers.count())]

    def get_rows_data(self) -> List[Dict[str, str]]:
        """Extract all rows as structured dictionaries mapped to headers."""
        headers = self.get_headers()
        rows = self.table.locator("tbody tr")
        results = []
        for i in range(rows.count()):
            row = rows.nth(i)
            # Skip expanded disclosure detail rows
            if row.locator("td[colspan]").count() > 0:
                continue
            cells = row.locator("th, td")
            data = {}
            for col_idx, header in enumerate(headers):
                if col_idx < cells.count():
                    data[header] = cells.nth(col_idx).inner_text().strip()
            if data:
                results.append(data)
        return results

    def toggle_disclosure(self, row_matcher: str, open: bool = True) -> None:
        """Find disclosure button in a row matching text or invoice number and set state."""
        row = self.table.locator("tbody tr").filter(has_text=row_matcher).first
        btn = row.locator("button[aria-expanded]")
        if btn.count() == 0:
            btn = row.locator("button[class*='disclosureButton'], button[aria-label*='details']")
        is_currently_open = btn.get_attribute("aria-expanded") == "true"
        if is_currently_open != open:
            btn.click()

    def is_disclosure_open(self, row_matcher: str) -> bool:
        """Check if row's detail panel is currently expanded."""
        row = self.table.locator("tbody tr").filter(has_text=row_matcher).first
        btn = row.locator("button[aria-expanded]")
        return btn.get_attribute("aria-expanded") == "true" if btn.count() > 0 else False

    def get_disclosure_panel(self, detail_id: str) -> Locator:
        """Return locator for the expanded detail container."""
        return self.page.locator(f"#{detail_id}, [id='{detail_id}']")

    def get_alert_state(self) -> Optional[Dict[str, Any]]:
        """Extract information from any active transaction error or warning alert."""
        alert = self.page.locator("div[role='alert'], [class*='Alert_root']").first
        if alert.count() > 0 and alert.is_visible():
            heading = alert.locator("h2, h3, h4").first
            heading_text = heading.inner_text().strip() if heading.count() > 0 else ""
            msg = alert.locator("p").first
            msg_text = msg.inner_text().strip() if msg.count() > 0 else alert.inner_text().strip()
            has_retry = alert.locator("button:has-text('Retry'), button:has-text('Try again')").count() > 0
            return {
                "visible": True,
                "heading": heading_text,
                "message": msg_text,
                "has_retry": has_retry,
            }
        return None

    def click_retry(self) -> None:
        """Click retry button on error alert."""
        btn = self.page.locator("div[role='alert'] button:has-text('Retry'), button:has-text('Try again')").first
        btn.click()

    def is_empty_state_visible(self) -> bool:
        """Check if empty data state is displayed."""
        loc = self.page.locator("[class*='emptyState'], [role='status']:has-text('No transactions')")
        return loc.first.is_visible(timeout=1000) if loc.count() > 0 else False

    def get_empty_state_text(self) -> str:
        """Get empty state text."""
        loc = self.page.locator("[class*='emptyState'], [role='status']:has-text('No transactions')")
        return loc.first.inner_text().strip() if loc.count() > 0 else ""

    def select_page_size(self, size: int) -> None:
        """Change items per page via select dropdown."""
        select_loc = self.page.locator("div[class*='paginationBar'] select, select[class*='pageSize']").first
        select_loc.select_option(str(size))

    def go_to_page(self, page_number: int) -> None:
        """Navigate to a specific page number."""
        btn = self.page.locator(
            f"nav[aria-label*='Pagination'] button:has-text('{page_number}'), "
            f"[class*='paginationBar'] button:has-text('{page_number}')"
        ).first
        btn.click()
