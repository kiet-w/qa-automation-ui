"""
pages/fs03/school_user_bulk_csv_page.py - Page Object for Bulk CSV mode on Create School User.
Complies with Invariant 1 (Zero assertions in Page Objects) and ADR-0006.
Source: specs/ui_bsk/localhost-5173/academic-and-users/04_school_user_management.md §1.2/§4.
"""
from typing import Dict, List, Optional
from playwright.sync_api import Locator, Page
from pages.base_page import BasePage
from pages.fs03.school_user_mgmt_locators import BulkCsvLocators

# Conservative success markers for bulk import feedback. Exact success wording is a SPEC GAP
# (ui_bsk §4.1 gives oracles for Single only); record creation is verified in the list by tests.
_SUCCESS_MARKERS = ("success", "created", "imported", "completed")


class SchoolUserBulkCsvPage(BasePage):
    """Page Object for /school-user-management/new -> Bulk CSV tab (upload, import, feedback)."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.bulk_tab: Locator = self.page.locator(BulkCsvLocators.BULK_TAB)
        self.file_input: Locator = self.page.locator(BulkCsvLocators.FILE_INPUT)
        self.import_button: Locator = self.page.locator(BulkCsvLocators.IMPORT_BUTTON)
        self.template_button: Locator = self.page.locator(BulkCsvLocators.TEMPLATE_BUTTON)
        self.reset_button: Locator = self.page.locator(BulkCsvLocators.RESET_BUTTON)
        self.feedback: Locator = self.page.locator(BulkCsvLocators.FEEDBACK)
        self.result_region: Locator = self.page.locator(BulkCsvLocators.RESULT_REGION)

    # --- Navigation ---
    def open(self, base_url: str = "http://localhost:5173") -> None:
        """Navigate to Create School User with session recovery, then activate Bulk CSV tab."""
        target_url = f"{base_url}/school-user-management/new"
        self.page.goto(target_url, wait_until="domcontentloaded")
        try:
            self.page.wait_for_selector(
                "#school-user-nric, button:has-text('Sign in with Microsoft')", timeout=5000
            )
        except Exception:
            pass

        if target_url not in self.page.url or "login" in self.page.url:
            from pages.fs03.admin_login_page import AdminLoginPage
            AdminLoginPage(self.page).login_with_microsoft_as_admin(base_url=base_url)
            self.page.goto(target_url, wait_until="domcontentloaded")

        self.switch_to_bulk_tab()

    def switch_to_bulk_tab(self) -> None:
        """Activate the Bulk CSV tab."""
        self.bulk_tab.first.wait_for(state="visible", timeout=10000)
        self.bulk_tab.first.click()

    # --- Actions ---
    def select_file(self, file_path: str) -> None:
        """Attach a file to the CSV file input."""
        self.file_input.first.set_input_files(file_path)

    def clear_file(self) -> None:
        """Detach any selected file."""
        self.file_input.first.set_input_files([])

    def click_import(self) -> None:
        """Trigger the bulk import/upload action."""
        self.import_button.first.click()

    def download_template(self, save_name: Optional[str] = None):
        """Click template download and return the saved file path."""
        return self.download_file(lambda: self.template_button.first.click(), save_name=save_name)

    def is_import_disabled(self) -> bool:
        """Return True when the import/upload button is disabled."""
        return bool(self.import_button.first.is_disabled())

    # --- Feedback reading ---
    def get_feedback_texts(self) -> List[str]:
        """Return visible feedback texts (alerts, toasts, aria-live regions)."""
        count = self.feedback.count()
        return [
            self.feedback.nth(i).inner_text().strip()
            for i in range(count)
            if self.feedback.nth(i).is_visible() and self.feedback.nth(i).inner_text().strip()
        ]

    def has_feedback(self) -> bool:
        """Return True when at least one feedback element carries text."""
        return bool(self.get_feedback_texts())

    def wait_for_feedback(self, timeout: int = 8000) -> None:
        """Wait (Playwright wait, no fixed sleep) until any feedback surface becomes visible."""
        self.feedback.first.wait_for(state="visible", timeout=timeout)

    def has_result_region(self) -> bool:
        """Return True when a bulk result/preview region is rendered."""
        return self.result_region.first.is_visible()

    def get_import_snapshot(self) -> Dict:
        """
        Produce standardized state snapshot for Exceptor adjudication after an import attempt.
        `visible_errors["csv_file"]` carries the joined visible feedback text.
        """
        feedback = self.get_feedback_texts()
        joined = " | ".join(feedback)
        lowered = joined.lower()
        success_visible = self.has_result_region() and any(m in lowered for m in _SUCCESS_MARKERS)
        return {
            "success_visible": success_visible,
            "visible_errors": {"csv_file": joined} if joined else {},
            "alerts": feedback,
        }
