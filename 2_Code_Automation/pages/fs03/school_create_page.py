"""
pages/fs03/school_create_page.py - Page Object for FS03 Create School screen.
Complies with Invariant 1 (Zero assertions in Page Objects) and ADR-0006.
"""
from typing import List, Optional
from playwright.sync_api import Locator, Page
from pages.base_page import BasePage


class SchoolCreatePage(BasePage):
    """
    Page Object encapsulating DOM elements and actions for:
    EduFAMS Admin Portal > School Management > Create School (/school-management/new)
    """

    def __init__(self, page: Page):
        super().__init__(page)
        # Form Container & Section Headings
        self.form: Locator = self.page.locator("form")
        self.page_heading: Locator = self.page.locator("h1, h2:has-text('Create a school')")
        self.section_heading: Locator = self.page.locator("h2, h3:has-text('School details')")

        # Form Input Fields
        self.moe_school_code_input: Locator = self.page.locator("#school-moeSchoolCode")
        self.school_name_input: Locator = self.page.locator("#school-name")
        self.school_type_select: Locator = self.page.locator("#school-schoolType")
        self.school_users_input: Locator = self.page.locator("#school-schoolUsers")
        self.academic_levels_input: Locator = self.page.locator("#school-academicLevels")

        # Chip Counters & Screen Reader Indicators
        self.school_users_counter: Locator = self.page.locator("#school-schoolUsers-selected")
        self.academic_levels_counter: Locator = self.page.locator("#school-academicLevels-selected")

        # Action Buttons
        self.cancel_button: Locator = self.page.locator("button:has-text('Cancel')")
        self.create_school_button: Locator = self.page.locator("button:has-text('Create school')")
        self.load_more_buttons: Locator = self.page.locator("button:has-text('Load more')")

        # Validation Alerts & Error Containers
        self.summary_error_banner: Locator = self.page.locator("div:has-text('Please correct the errors below.')").first
        self.error_alerts: Locator = self.page.locator("[role='alert'], .alert-error, div:has-text('Unable to create school')")

        # Field-Level Inline Error Messages
        self.moe_code_inline_error: Locator = self.page.locator("p:has-text('MOE school code is required.')")
        self.name_inline_error: Locator = self.page.locator("p:has-text('School name is required.')")
        self.type_inline_error: Locator = self.page.locator("p:has-text('Select a school type.')")
        self.levels_inline_error: Locator = self.page.locator("p:has-text('Select at least one academic level.')")

        # Toast Feedback
        self.success_toast: Locator = self.page.locator("div:has-text('School created')").first
        self.toast_close_button: Locator = self.page.locator("button[aria-label='Close'], button:has-text('×')")

    # --- Navigation Methods ---
    def open(self, base_url: str = "http://localhost:5173") -> None:
        """Navigate to Create School page with fast session check and robust fallback."""
        target_url = f"{base_url}/school-management/new"
        self.page.goto(target_url, wait_until="domcontentloaded")

        # Fast path: already authenticated and target form input rendered
        try:
            self.page.wait_for_selector("#school-moeSchoolCode", timeout=3000)
            return
        except Exception:
            pass

        # Fallback: Recover login if redirected to Microsoft SSO / login page
        if target_url not in self.page.url or "login" in self.page.url or self.page.locator("button:has-text('Sign in with Microsoft')").is_visible():
            from pages.fs03.admin_login_page import AdminLoginPage
            login_page = AdminLoginPage(self.page)
            login_page.login_with_microsoft_as_admin(base_url=base_url)
            self.page.goto(target_url, wait_until="domcontentloaded")

        self.wait_for_form_ready()

    def wait_for_form_ready(self, timeout: int = 15000) -> None:
        """Ensure form fields are rendered and ready for interaction."""
        self.moe_school_code_input.wait_for(state="visible", timeout=timeout)
        self.create_school_button.wait_for(state="visible", timeout=timeout)

    # --- Form Fill Actions ---
    def fill_moe_school_code(self, code: str) -> None:
        """Fill the MOE school code input field."""
        self.moe_school_code_input.fill(code)

    def fill_school_name(self, name: str) -> None:
        """Fill the School name input field."""
        self.school_name_input.fill(name)

    def select_school_type(self, school_type: str) -> None:
        """Select a school type from the dropdown by visible label or value."""
        self.school_type_select.select_option(label=school_type)

    def select_academic_level(self, level_name: str) -> None:
        """Click academic levels combobox to open listbox, select an option by text, and close listbox."""
        self.academic_levels_input.click()
        option = self.page.locator(f"[role='option']:has-text('{level_name}')").first
        if option.is_visible():
            option.click()
        else:
            first_opt = self.page.locator("[role='option']").first
            first_opt.click()
        self.page.keyboard.press("Escape")

    def select_first_academic_level(self) -> None:
        """Click academic levels combobox to open listbox, select first option, and close listbox."""
        self.academic_levels_input.click()
        first_opt = self.page.locator("[role='option']").first
        first_opt.wait_for(state="visible", timeout=5000)
        first_opt.click()
        self.page.keyboard.press("Escape")

    def select_first_school_user(self) -> None:
        """Click school users combobox to open listbox, select first user option, and close listbox."""
        self.school_users_input.click()
        first_opt = self.page.locator("[role='option']").first
        if first_opt.is_visible():
            first_opt.click()
        self.page.keyboard.press("Escape")

    def remove_first_academic_level_chip(self) -> None:
        """Click the remove icon (x) on the first selected academic level chip."""
        remove_btn = self.page.locator("button[aria-label*='Remove'], .chip-remove, button:has-text('×')").first
        if remove_btn.is_visible():
            remove_btn.click()

    def submit_form(self) -> None:
        """Click the Create school submit button."""
        self.create_school_button.click()

    def cancel(self) -> None:
        """Click the Cancel button."""
        self.cancel_button.click()

    def create_school(self, moe_code: str, name: str, school_type: str, level_name: Optional[str] = None) -> None:
        """High-level helper to fill all mandatory fields and submit the form."""
        self.fill_moe_school_code(moe_code)
        self.fill_school_name(name)
        self.select_school_type(school_type)
        if level_name:
            self.select_academic_level(level_name)
        else:
            self.select_first_academic_level()
        self.submit_form()

    # --- State Inquiry Methods (Zero Assertions) ---
    def get_moe_school_code_value(self) -> str:
        """Retrieve current value of MOE school code input."""
        return self.moe_school_code_input.input_value()

    def get_school_name_value(self) -> str:
        """Retrieve current value of School name input."""
        return self.school_name_input.input_value()

    def get_selected_school_type(self) -> str:
        """Retrieve current selected option text of School type select."""
        return self.school_type_select.evaluate("el => el.options[el.selectedIndex].text")

    def get_academic_levels_count_text(self) -> str:
        """Retrieve screen reader text for selected academic levels (e.g. '1 selected')."""
        return self.academic_levels_counter.inner_text().strip()

    def get_school_users_count_text(self) -> str:
        """Retrieve screen reader text for selected school users."""
        return self.school_users_counter.inner_text().strip()

    def is_moe_code_invalid(self) -> bool:
        """Check if MOE school code input has aria-invalid set to true."""
        return self.moe_school_code_input.get_attribute("aria-invalid") == "true"

    def is_school_name_invalid(self) -> bool:
        """Check if School name input has aria-invalid set to true."""
        return self.school_name_input.get_attribute("aria-invalid") == "true"

    def get_summary_banner_text(self) -> str:
        """Retrieve text from summary error banner if present."""
        if self.summary_error_banner.is_visible():
            return self.summary_error_banner.inner_text().strip()
        return ""

    def get_alert_error_texts(self) -> List[str]:
        """Retrieve all visible alert error texts."""
        return [text.strip() for text in self.error_alerts.all_inner_texts() if text.strip()]

    def is_toast_visible(self) -> bool:
        """Check if success toast notification is visible."""
        return self.success_toast.is_visible()

    def get_toast_text(self) -> str:
        """Retrieve text inside the success toast."""
        if self.success_toast.is_visible():
            return self.success_toast.inner_text().strip()
        return ""
