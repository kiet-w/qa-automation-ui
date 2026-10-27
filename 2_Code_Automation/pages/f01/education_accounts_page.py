"""
pages/f01/education_accounts_page.py - Page Object for Education Accounts Management (F01).
Complies with Invariant 1 (Zero assertions in Page Objects) and Invariant 9 (< 200 lines).

BSK Source: specs/ui_bsk/localhost-5173/finance-and-fas/01_education_accounts.md
Route: http://localhost:5173/education-accounts (SCR-ADM-01)
RBAC: MOEHQ (admin@IAM.edu.vn)
"""
from typing import Dict, List, Optional
from playwright.sync_api import Locator, Page
from pages.base_page import BasePage
from pages.f01 import locators
from pages.f01.components.ea_sync_dialog import EaSyncDialog
from pages.f01.components.student_profile_dialog import StudentProfileDialog


class EducationAccountsPage(BasePage):
    """
    Main Orchestrator for SCR-ADM-01 Education Accounts (/education-accounts).
    Delegates to EaSyncDialog and StudentProfileDialog sub-components.
    """

    def __init__(self, page: Page):
        super().__init__(page)
        self.sync_dialog = EaSyncDialog(page)
        self.profile_dialog = StudentProfileDialog(page)

        # Main page locators
        self.heading = self.page.locator(locators.PAGE_HEADING)
        self.search_input = self.page.locator(locators.SEARCH_INPUT)
        self.status_select = self.page.locator(locators.STATUS_SELECT)
        self.citizenship_select = self.page.locator(locators.CITIZENSHIP_SELECT)
        self.apply_search_btn = self.page.locator(locators.APPLY_SEARCH_BTN)
        self.clear_search_btn = self.page.locator(locators.CLEAR_SEARCH_BTN)
        self.manual_sync_btn = self.page.locator(locators.MANUAL_SYNC_BTN)
        self.table = self.page.locator(locators.ACCOUNTS_TABLE)
        self.table_rows = self.page.locator(locators.TABLE_ROWS)
        self.error_alert = self.page.locator(locators.ERROR_ALERT)
        self.retry_btn = self.page.locator(locators.RETRY_BTN)

    # ─── Navigation ────────────────────────────────────────────────────────────

    def open(self, base_url: str = "http://localhost:5173") -> None:
        """Navigate to Education Accounts page and wait for heading."""
        self.page.goto(f"{base_url}/education-accounts", wait_until="domcontentloaded")
        self.heading.wait_for(state="visible", timeout=15000)

    # ─── Manual Sync Trigger ───────────────────────────────────────────────────

    def trigger_manual_sync(self) -> EaSyncDialog:
        """Click 'Manual sync' button; returns EaSyncDialog for chaining."""
        self.manual_sync_btn.wait_for(state="visible", timeout=10000)
        self.manual_sync_btn.click()
        self.sync_dialog.dialog.first.wait_for(state="visible", timeout=5000)
        return self.sync_dialog

    def perform_sync_and_wait(self) -> None:
        """
        Full sync flow: open dialog → confirm → wait for table to reflect new data.
        Used by E2E tests (TC-UAT001-15) for Sync #1 and Sync #2.
        """
        self.trigger_manual_sync()
        # Wait for table to reload after sync completes
        self.sync_dialog.confirm()
        self.page.wait_for_load_state("domcontentloaded")

    # ─── Search & Filter ────────────────────────────────────────────────────────

    def search(self, query: str) -> None:
        """Fill search query and submit filter."""
        self.search_input.wait_for(state="visible", timeout=5000)
        self.search_input.fill(query)
        self.apply_search_btn.click()
        self.page.wait_for_load_state("domcontentloaded")

    def clear_search(self) -> None:
        """Click the clear search (×) button if visible."""
        if self.clear_search_btn.is_visible(timeout=2000):
            self.clear_search_btn.click()
            self.page.wait_for_load_state("domcontentloaded")

    def filter_by_status(self, status_val: str) -> None:
        """Select status ('all', '1' for Active, '2' for Deactive) and submit."""
        self.status_select.wait_for(state="visible", timeout=5000)
        self.status_select.select_option(status_val)
        self.apply_search_btn.click()
        self.page.wait_for_load_state("domcontentloaded")

    def filter_by_citizenship(self, citizenship_val: str) -> None:
        """Select citizenship ('all', '1' for Singapore Citizen, '5' for Exported) and submit."""
        self.citizenship_select.wait_for(state="visible", timeout=5000)
        self.citizenship_select.select_option(citizenship_val)
        self.apply_search_btn.click()
        self.page.wait_for_load_state("domcontentloaded")

    # ─── Table Data Access ──────────────────────────────────────────────────────

    def get_row_count(self) -> int:
        """Return number of visible student rows in table body."""
        return self.table_rows.count()

    def get_row_data(self, index: int) -> Dict[str, str]:
        """Extract text data from a specific row by index (0-based)."""
        row = self.table_rows.nth(index)
        cells = row.locator(locators.TABLE_ROW_CELLS).all()
        texts = [c.inner_text().strip() for c in cells]
        return {
            "code": texts[0] if len(texts) > 0 else "",
            "nric": texts[1] if len(texts) > 1 else "",
            "fullName": texts[2] if len(texts) > 2 else "",
            "age": texts[3] if len(texts) > 3 else "",
            "gender": texts[4] if len(texts) > 4 else "",
            "citizenship": texts[5] if len(texts) > 5 else "",
            "status": texts[6] if len(texts) > 6 else "",
            "address": texts[7] if len(texts) > 7 else "",
        }

    def get_all_rows_data(self) -> List[Dict[str, str]]:
        """Return list of row data dicts for all visible rows."""
        count = self.get_row_count()
        return [self.get_row_data(i) for i in range(count)]

    def find_row_by_nric(self, nric: str) -> Optional[Dict[str, str]]:
        """Return row data dict matching given NRIC, or None if not found."""
        for row_data in self.get_all_rows_data():
            if nric.upper() in row_data.get("nric", "").upper():
                return row_data
        return None

    # ─── Student Profile Modal ──────────────────────────────────────────────────

    def open_student_details(self, index: int = 0) -> StudentProfileDialog:
        """Click 'View details' button on specific row index; returns StudentProfileDialog."""
        view_btn = self.table_rows.nth(index).locator(locators.VIEW_DETAILS_BTN)
        view_btn.wait_for(state="visible", timeout=5000)
        view_btn.click()
        self.profile_dialog.dialog.first.wait_for(state="visible", timeout=5000)
        return self.profile_dialog

    def open_student_details_by_nric(self, nric: str) -> Optional["StudentProfileDialog"]:
        """Search for student by NRIC, then open their profile dialog."""
        self.search(nric)
        if self.get_row_count() > 0:
            return self.open_student_details(0)
        return None

    # ─── State Snapshot for Exceptor / Assertions ──────────────────────────────

    def get_state_snapshot(self) -> Dict:
        """
        Return a minimal UI snapshot dict for Exceptor consumption.
        Captures: table visibility, row count, error state, page heading.
        """
        has_rows = self.get_row_count() > 0
        heading_visible = False
        try:
            self.heading.wait_for(state="visible", timeout=3000)
            heading_visible = True
        except Exception:
            pass
        error_visible = False
        try:
            error_visible = self.error_alert.is_visible(timeout=1000)
        except Exception:
            pass
        return {
            "success_visible": has_rows and heading_visible and not error_visible,
            "visible_errors": {"api_error": "Accounts failed to load"} if error_visible else {},
            "row_count": self.get_row_count(),
        }
