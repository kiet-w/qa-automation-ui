"""
pages/fs03/school_directory_page.py - Page Object for FS03 School Management directory (/school-management).
Source: 1_Nghiep_Vu_va_Specs/specs/ui_bsk/localhost-5173/academic-and-users/03_school_management.md §1.1 / §4.
Complies with Invariant 1 (zero assertions in Page Objects) and page size limit (< 200 lines).
"""
from typing import Dict, List
from playwright.sync_api import Locator, Page
from pages.base_page import BasePage
from pages.fs03.locators import SchoolDirectoryLocators as L


class SchoolDirectoryPage(BasePage):
    """POM for the school directory: toolbar search/filter, table rows, inline edit and lifecycle dialog."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page_heading: Locator = page.locator(L.PAGE_HEADING)
        self.search_input: Locator = page.locator(L.SEARCH_INPUT)
        self.type_filter: Locator = page.locator(L.TYPE_FILTER)
        self.search_button: Locator = page.locator(L.SEARCH_BUTTON)
        self.reset_button: Locator = page.locator(L.RESET_BUTTON)
        self.create_button: Locator = page.locator(L.CREATE_BUTTON)
        self.table_headers: Locator = page.locator(L.TABLE_HEADERS)
        self.rows: Locator = page.locator(L.ROWS)
        self.empty_state: Locator = page.locator(L.EMPTY_STATE)
        self.alerts: Locator = page.locator(L.ALERT)
        self.dialog: Locator = page.locator(L.DIALOG)
        self.dialog_confirm: Locator = page.locator(L.DIALOG_CONFIRM)
        self.dialog_cancel: Locator = page.locator(L.DIALOG_CANCEL)
        self.dialog_alert: Locator = page.locator(L.DIALOG_ALERT)
        self.inline_name_input: Locator = page.locator(L.INLINE_NAME)
        self.inline_type_select: Locator = page.locator(L.INLINE_TYPE)
        self.save_inline_button: Locator = page.locator(L.SAVE_INLINE)
        self.discard_inline_button: Locator = page.locator(L.DISCARD_INLINE)
        self._native_dialog_registered = False

    # --- Navigation -------------------------------------------------------
    def open(self, base_url: str) -> None:
        """Open the directory, recovering the SSO session when the stored state expired."""
        target = f"{base_url}/school-management"
        self.page.goto(target, wait_until="domcontentloaded")
        try:
            self.page.wait_for_selector(L.SEARCH_INPUT, timeout=8000)
            return
        except Exception:
            pass
        if "login" in self.page.url or self.page.locator("button:has-text('Sign in with Microsoft')").is_visible():
            from pages.fs03.admin_login_page import AdminLoginPage
            AdminLoginPage(self.page).login_with_microsoft_as_admin(base_url=base_url)
            self.page.goto(target, wait_until="domcontentloaded")
            self.page.wait_for_selector(L.SEARCH_INPUT, timeout=15000)

    # --- Toolbar actions --------------------------------------------------
    def fill_search(self, query: str) -> None:
        self.search_input.fill(query)

    def click_search(self) -> None:
        self.search_button.click()

    # --- Table state (read-only) ------------------------------------------
    def get_header_texts(self) -> List[str]:
        return [h.strip() for h in self.table_headers.all_inner_texts()]

    def get_rows_data(self) -> List[Dict[str, str]]:
        """Return per-row values keyed by the six sourced column names; skip empty-state rows."""
        collected: List[Dict[str, str]] = []
        for idx in range(self.rows.count()):
            row = self.rows.nth(idx)
            cells = [c.strip() for c in row.locator("td").all_inner_texts()]
            if len(cells) < 5:
                continue
            badge = row.locator(L.ROW_BADGE)
            status = badge.first.inner_text().strip() if badge.count() else ""
            if not status:
                status = self._status_from_actions(row)
            collected.append({
                "code": cells[0], "name": cells[1], "type": cells[2],
                "classes": cells[3], "students": cells[4], "status": status,
            })
        return collected

    @staticmethod
    def _status_from_actions(row: Locator) -> str:
        """Derive row status from the sourced lifecycle action label (Deactive=Active row, Active=Inactive row)."""
        labels = [v for v in row.locator(L.ROW_ACTION_BUTTON).evaluate_all(
            "els => els.map(e => e.getAttribute('aria-label'))") if v]
        if "Deactive" in labels:
            return "Active"
        if "Active" in labels:
            return "Inactive"
        return ""

    def get_row_cells(self, code: str) -> List[str]:
        return [c.strip() for c in self.row_by_code(code).locator("td").all_inner_texts()]

    def row_lifecycle_button(self, code: str) -> Locator:
        return self.row_by_code(code).locator(L.ROW_LIFECYCLE_BUTTON)

    def row_by_code(self, code: str) -> Locator:
        return self.rows.filter(has_text=code).first

    def get_row_action_labels(self, code: str) -> List[str]:
        buttons = self.row_by_code(code).locator(L.ROW_ACTION_BUTTON)
        return [str(v) for v in buttons.evaluate_all("els => els.map(e => e.getAttribute('aria-label'))") if v]

    def is_empty_state_visible(self) -> bool:
        return self.empty_state.first.is_visible()

    def get_empty_state_text(self) -> str:
        return self.empty_state.first.inner_text().strip() if self.is_empty_state_visible() else ""

    def get_alert_error_texts(self) -> List[str]:
        """Visible [role="alert"] texts on the directory screen (read-only state, no assertion)."""
        return [t.strip() for t in self.alerts.all_inner_texts() if t and t.strip()]

    def click_detail(self, code: str) -> None:
        self.row_by_code(code).locator(L.ROW_DETAIL_BUTTON).click()

    def click_edit(self, code: str) -> None:
        self.row_by_code(code).locator(L.ROW_EDIT_BUTTON).click()
        self.inline_name_input.wait_for(state="visible", timeout=5000)

    # --- Inline edit ------------------------------------------------------
    def fill_inline_name(self, name: str) -> None:
        self.inline_name_input.fill(name)

    def select_inline_type(self, label: str) -> None:
        try:
            self.inline_type_select.select_option(value=label)
        except Exception:
            self.inline_type_select.select_option(label=label)

    def save_inline(self) -> None:
        self.save_inline_button.click()

    def discard_inline(self) -> None:
        self.discard_inline_button.click()

    # --- Lifecycle dialog -------------------------------------------------
    def open_deactivate_dialog(self, code: str) -> None:
        """Open the confirm dialog; native JS dialogs are handled before the triggering click."""
        self._register_native_dialog_handler()
        self.row_by_code(code).locator(L.ROW_DEACTIVE_BUTTON).click()
        self.dialog.wait_for(state="visible", timeout=5000)

    def activate_row(self, code: str) -> None:
        self._register_native_dialog_handler()
        self.row_by_code(code).locator(L.ROW_ACTIVE_BUTTON).click()

    def confirm_activation_if_dialog_present(self) -> None:
        """Confirm only when a confirm dialog is actually presented (short guarded wait)."""
        try:
            self.dialog.wait_for(state="visible", timeout=2000)
        except Exception:
            return
        self.dialog_confirm.click()

    def confirm_deactivation(self) -> None:
        self.dialog_confirm.click()

    def cancel_deactivation(self) -> None:
        """Guarded cleanup-style cancel: short timeout so a closed dialog cannot hang the step."""
        try:
            self.dialog_cancel.click(timeout=2000)
        except Exception:
            return
        self.dialog.wait_for(state="hidden", timeout=5000)

    def get_dialog_alert_text(self) -> str:
        return self.dialog_alert.first.inner_text().strip() if self.dialog_alert.count() else ""

    def _register_native_dialog_handler(self) -> None:
        if not self._native_dialog_registered:
            self.page.on("dialog", lambda d: d.accept())
            self._native_dialog_registered = True
