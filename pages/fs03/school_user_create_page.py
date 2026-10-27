"""
pages/fs03/school_user_create_page.py - Page Object for FS03 Create School User screen.
Complies with Invariant 1 (Zero assertions in Page Objects) and ADR-0006.
"""
from typing import List, Optional
from playwright.sync_api import Locator, Page
from pages.base_page import BasePage


class SchoolUserCreatePage(BasePage):
    """
    Page Object encapsulating DOM elements and actions for:
    EduFAMS Admin Portal > School Users > Create (/school-user-management/new)
    """

    def __init__(self, page: Page):
        super().__init__(page)
        # Form Input Fields
        self.nric_input: Locator = self.page.locator("#school-user-nric")
        self.first_name_input: Locator = self.page.locator("#school-user-first-name")
        self.last_name_input: Locator = self.page.locator("#school-user-last-name")
        self.email_input: Locator = self.page.locator("#school-user-email")
        self.moe_school_code_input: Locator = self.page.locator("#school-user-moe-school-code")

        # Action Buttons
        self.create_button: Locator = self.page.locator("button:has-text('Create')")
        self.reset_button: Locator = self.page.locator("button:has-text('Reset')")
        self.back_to_list_button: Locator = self.page.locator("button:has-text('Back to list')")

        # Tab Navigation
        self.single_tab: Locator = self.page.locator("button[role='tab']:has-text('Single')")
        self.bulk_tab: Locator = self.page.locator("button[role='tab']:has-text('Bulk CSV')")

        # Bulk CSV Controls
        self.get_template_button: Locator = self.page.locator("button:has-text('Get Template')")
        self.file_input: Locator = self.page.locator("#school-users-csv")
        self.import_button: Locator = self.page.locator("button:has-text('Import')")

        # Feedback & Announcements
        self.alerts: Locator = self.page.locator("[role='alert']")
        self.toasts: Locator = self.page.locator("[role='status']")
        self.result_card: Locator = self.page.locator("div[aria-live='polite']")

        # Structure & Headings
        self.page_heading: Locator = self.page.locator("h1, h2:has-text('Create school user')")
        self.portal_logo: Locator = self.page.locator("text=EduFAMS Admin Portal")

    # --- Navigation Methods ---
    def open(self, base_url: str = "http://localhost:5173") -> None:
        """Navigate to Create School User page with robust session validation and recovery."""
        target_url = f"{base_url}/school-user-management/new"
        self.page.goto(target_url)
        self.page.wait_for_load_state("domcontentloaded")

        try:
            # Wait briefly for either form input or login redirect
            self.page.wait_for_selector(
                "#school-user-nric, button:has-text('Sign in with Microsoft')",
                timeout=5000
            )
        except Exception:
            pass

        if target_url not in self.page.url or "login" in self.page.url or self.page.locator("button:has-text('Sign in with Microsoft')").is_visible():
            from pages.fs03.admin_login_page import AdminLoginPage
            login_page = AdminLoginPage(self.page)
            login_page.login_with_microsoft_as_admin(base_url=base_url)
            self.page.goto(target_url)
            self.page.wait_for_load_state("domcontentloaded")

        self.wait_for_page_loaded()

    def wait_for_page_loaded(self) -> None:
        """Wait until form elements are fully mounted in DOM."""
        self.nric_input.wait_for(state="visible", timeout=15000)

    # --- Tab Switching ---
    def switch_to_single_tab(self) -> None:
        """Switch to Single tab."""
        self.single_tab.click()

    def switch_to_bulk_tab(self) -> None:
        """Switch to Bulk CSV tab."""
        self.bulk_tab.click()

    def is_single_tab_active(self) -> bool:
        """Return True if Single tab has active state."""
        return self.single_tab.get_attribute("data-state") == "active" or "active" in (self.single_tab.get_attribute("class") or "")

    def is_bulk_tab_active(self) -> bool:
        """Return True if Bulk CSV tab has active state."""
        return self.bulk_tab.get_attribute("data-state") == "active" or "active" in (self.bulk_tab.get_attribute("class") or "")

    # --- Form Interactions ---
    def fill_nric(self, value: str) -> None:
        """Fill NRIC input field."""
        self.nric_input.fill(value)

    def fill_first_name(self, value: str) -> None:
        """Fill First Name input field."""
        self.first_name_input.fill(value)

    def fill_last_name(self, value: str) -> None:
        """Fill Last Name input field."""
        self.last_name_input.fill(value)

    def fill_email(self, value: str) -> None:
        """Fill Email input field."""
        self.email_input.fill(value)

    def fill_school_code(self, value: str) -> None:
        """Fill MOE School Code input field."""
        self.moe_school_code_input.fill(value)

    def fill_form(
        self,
        nric: str,
        first_name: str,
        last_name: str,
        email: str,
        school_code: Optional[str] = None,
    ) -> None:
        """Convenience method to populate all fields."""
        self.fill_nric(nric)
        self.fill_first_name(first_name)
        self.fill_last_name(last_name)
        self.fill_email(email)
        if school_code is not None:
            self.fill_school_code(school_code)

    def clear_all_fields(self) -> None:
        """Directly clear values in all 5 form fields."""
        self.nric_input.fill("")
        self.first_name_input.fill("")
        self.last_name_input.fill("")
        self.email_input.fill("")
        self.moe_school_code_input.fill("")

    # --- Button Actions ---
    def click_create(self) -> None:
        """Click Create button to submit form."""
        self.create_button.click()

    def click_reset(self) -> None:
        """Click Reset button to restore pristine form state."""
        self.reset_button.click()

    def click_back_to_list(self) -> None:
        """Click 'Back to list' button."""
        self.back_to_list_button.click()

    def is_create_button_disabled(self) -> bool:
        """Return True if Create button is disabled."""
        return self.create_button.is_disabled()

    def is_import_button_disabled(self) -> bool:
        """Return True if Import button on bulk tab is disabled."""
        return self.import_button.is_disabled()

    def is_get_template_button_visible(self) -> bool:
        """Return True if Get Template button is visible."""
        return self.get_template_button.is_visible()

    # --- Value Inspection ---
    def get_nric_value(self) -> str:
        """Get current value of NRIC input."""
        return self.nric_input.input_value()

    def get_first_name_value(self) -> str:
        """Get current value of First Name input."""
        return self.first_name_input.input_value()

    def get_last_name_value(self) -> str:
        """Get current value of Last Name input."""
        return self.last_name_input.input_value()

    def get_email_value(self) -> str:
        """Get current value of Email input."""
        return self.email_input.input_value()

    def get_school_code_value(self) -> str:
        """Get current value of School Code input."""
        return self.moe_school_code_input.input_value()

    # --- Status, Alerts & Result Card Inspection ---
    def get_alert_texts(self) -> List[str]:
        """Return list of text contents from all visible alert elements."""
        count = self.alerts.count()
        return [self.alerts.nth(i).inner_text().strip() for i in range(count) if self.alerts.nth(i).is_visible()]

    def get_toast_texts(self) -> List[str]:
        """Return list of text contents from all visible toast elements."""
        count = self.toasts.count()
        return [self.toasts.nth(i).inner_text().strip() for i in range(count) if self.toasts.nth(i).is_visible()]

    def is_result_card_visible(self) -> bool:
        """Return True if Created User Result card is visible."""
        return self.result_card.is_visible()

    def get_result_card_text(self) -> str:
        """Return inner text of Created User Result card."""
        if self.is_result_card_visible():
            return self.result_card.inner_text().strip()
        return ""

    def wait_for_result_card(self, timeout: int = 10000) -> None:
        """Wait for result card to appear."""
        self.result_card.wait_for(state="visible", timeout=timeout)

    def wait_for_alert(self, timeout: int = 10000) -> None:
        """Wait for any error alert to appear."""
        self.alerts.first.wait_for(state="visible", timeout=timeout)

    def wait_for_toast(self, timeout: int = 10000) -> None:
        """Wait for any toast notification to appear."""
        self.toasts.first.wait_for(state="visible", timeout=timeout)

