"""
pages/fs03/school_create_page.py - Page Object for FS03 Create School screen.
Complies with Invariant 1 (Zero assertions in Page Objects) and ADR-0006.

DOM source: SchoolCreateForm.tsx, TextField.tsx, Select.tsx, MultiSelect.tsx, FormErrorSummary.tsx
(packages/ui/src/components/ + apps/admin-portal/src/features/school-management/)
"""
from typing import List, Optional
from playwright.sync_api import Locator, Page
from pages.base_page import BasePage


class SchoolCreatePage(BasePage):
    """
    Page Object encapsulating DOM elements and actions for:
    EduFAMS Admin Portal > School Management > Create School (/school-management/new)

    Locator strategy (sourced from component DOM, not guessed):
    - Text inputs: stable #id from SchoolCreateForm (id="school-*")
    - School type: native <select id="school-schoolType"> (Select component)
    - School users / Academic levels: <input role="combobox" id="school-*"> (MultiSelect)
    - Field errors: <p role="alert" id="${id}-error"> (TextField/Select/MultiSelect pattern)
    - Summary banner: <section role="alert"><h2>{heading}</h2></section> (FormErrorSummary)
    - Success toast: locate by role="status" or text content
    """

    def __init__(self, page: Page):
        super().__init__(page)
        # Form Container
        self.form: Locator = self.page.locator("form")

        # --- Form Input Fields ---
        # TextField component: <input id="school-moeSchoolCode" aria-invalid="true" when error>
        self.moe_school_code_input: Locator = self.page.locator("#school-moeSchoolCode")
        # TextField component: <input id="school-name">
        self.school_name_input: Locator = self.page.locator("#school-name")
        # Select component: native <select id="school-schoolType"> — use .select_option(label=...)
        self.school_type_select: Locator = self.page.locator("#school-schoolType")
        # MultiSelect component: <input role="combobox" id="school-schoolUsers">
        self.school_users_input: Locator = self.page.locator("#school-schoolUsers")
        # MultiSelect component: <input role="combobox" id="school-academicLevels">
        self.academic_levels_input: Locator = self.page.locator("#school-academicLevels")

        # --- Chip Counters (MultiSelect screen-reader span) ---
        # <span id="${id}-selected"> renders "N selected" via localization
        self.school_users_counter: Locator = self.page.locator("#school-schoolUsers-selected")
        self.academic_levels_counter: Locator = self.page.locator("#school-academicLevels-selected")

        # --- Action Buttons ---
        # Role-based: more resilient than :has-text() across DOM refactors
        self.cancel_button: Locator = self.page.get_by_role("button", name="Cancel")
        self.create_school_button: Locator = self.page.get_by_role("button", name="Create school")
        self.load_more_buttons: Locator = self.page.get_by_role("button", name="Load more")

        # --- Summary Error Banner ---
        # FormErrorSummary renders: <section role="alert"><h2>{heading}</h2><ul>...</ul></section>
        # heading prop = t("features.schoolManagement.validationSummary")
        #             = "Please correct the errors below." (resource.ts:77, confirmed in .test.tsx:77)
        # Locator: role="alert" scoped to the section, then heading child.
        self.summary_error_banner: Locator = self.page.locator(
            "section[role='alert']"
        )
        self.summary_error_heading: Locator = self.page.locator(
            "section[role='alert'] h2"
        )

        # --- Field-Level Inline Error Messages ---
        # TextField/Select/MultiSelect pattern: <p role="alert" id="${fieldId}-error">{message}</p>
        # IDs are stable (constructed from explicit id prop, not useId() generated).
        # Source: TextField.tsx:36 `const errorId = error ? \`${id}-error\` : undefined`
        self.moe_code_inline_error: Locator = self.page.locator("#school-moeSchoolCode-error")
        self.name_inline_error: Locator = self.page.locator("#school-name-error")
        self.type_inline_error: Locator = self.page.locator("#school-schoolType-error")
        self.levels_inline_error: Locator = self.page.locator("#school-academicLevels-error")

        # --- API Submit Error Alert ---
        # Alert component (non-form-summary) rendered on mutation failure / duplicate HTTP 409
        self.error_alerts: Locator = self.page.locator("[role='alert']:not(section[role='alert']), .alert-error")
        self.submit_api_error: Locator = self.error_alerts

        # --- Toast Feedback ---
        # Toast typically renders with role="status" or role="alert"; locate by text
        self.success_toast: Locator = self.page.get_by_role("status").filter(
            has_text="School created"
        )

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

    def select_first_school_user(self) -> bool:
        """Click school users combobox, select first enabled option, and close listbox.

        Returns True if a user was selected, False if no enabled options are available
        (e.g. "No school users found." placeholder with aria-disabled="true").
        Callers should check the return value and skip or xfail as appropriate.
        """
        self.school_users_input.click()
        # Wait briefly for listbox to open
        self.page.wait_for_selector("[role='listbox']", timeout=3000)
        # Only consider options that are NOT aria-disabled (excludes "No options" placeholder)
        selectable = self.page.locator("[role='option']:not([aria-disabled='true'])")
        if selectable.count() == 0:
            self.page.keyboard.press("Escape")
            return False
        selectable.first.click()
        self.page.keyboard.press("Escape")
        return True

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
        """Check if MOE school code input has aria-invalid=true (set by TextField when error exists)."""
        return self.moe_school_code_input.get_attribute("aria-invalid") == "true"

    def is_school_name_invalid(self) -> bool:
        """Check if School name input has aria-invalid=true."""
        return self.school_name_input.get_attribute("aria-invalid") == "true"

    def is_school_type_invalid(self) -> bool:
        """Check if School type select has aria-invalid=true (Select component pattern)."""
        return self.school_type_select.get_attribute("aria-invalid") == "true"

    def is_academic_levels_invalid(self) -> bool:
        """Check if Academic levels combobox has aria-invalid=true (MultiSelect pattern)."""
        return self.academic_levels_input.get_attribute("aria-invalid") == "true"

    def get_summary_banner_heading(self) -> str:
        """Retrieve the <h2> heading text inside the FormErrorSummary section[role=alert]."""
        if self.summary_error_banner.is_visible():
            return self.summary_error_heading.inner_text().strip()
        return ""

    def get_moe_code_error_text(self) -> str:
        """Retrieve inline error text for MOE school code field (id=school-moeSchoolCode-error)."""
        if self.moe_code_inline_error.is_visible():
            return self.moe_code_inline_error.inner_text().strip()
        return ""

    def get_name_error_text(self) -> str:
        """Retrieve inline error text for School name field."""
        if self.name_inline_error.is_visible():
            return self.name_inline_error.inner_text().strip()
        return ""

    def get_type_error_text(self) -> str:
        """Retrieve inline error text for School type field."""
        if self.type_inline_error.is_visible():
            return self.type_inline_error.inner_text().strip()
        return ""

    def get_levels_error_text(self) -> str:
        """Retrieve inline error text for Academic levels field."""
        if self.levels_inline_error.is_visible():
            return self.levels_inline_error.inner_text().strip()
        return ""

    def is_toast_visible(self) -> bool:
        """Check if success toast notification is visible."""
        return self.success_toast.is_visible()

    def get_toast_text(self) -> str:
        """Retrieve text inside the success toast."""
        if self.success_toast.is_visible():
            return self.success_toast.inner_text().strip()
        return ""

    def get_alert_error_texts(self) -> List[str]:
        """Retrieve all visible alert error texts."""
        return [text.strip() for text in self.error_alerts.all_inner_texts() if text.strip()]

    def get_state_snapshot(self) -> dict:
        """Produce standardized state snapshot for Exceptor adjudication."""
        from core.error_diagnostics import ErrorDiagnostics
        diag = ErrorDiagnostics.capture(self.page, container=self.form)
        return {
            "success_visible": self.is_toast_visible(),
            "visible_errors": diag.get("field_errors", {}),
            "summary_banner_heading": self.get_summary_banner_heading(),
        }

