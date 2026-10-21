"""
pages/fs08/parent_profile_page.py - Page Object Model for Parent Profile & My Details.
Compliant with Framework Invariant 1 (Zero assertions in Page Objects).
"""
import os
from typing import Any, Dict, Optional
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError

from pages.base_page import BasePage


class ParentProfilePage(BasePage):
    """Page Object for Parent Profile, NRIC toggle, Contact details editing, and Confirmation Modal."""

    URL_PATH = "/profile"

    # View Mode Locators
    PROFILE_HEADING = "h1:has-text('My Profile'), h2:has-text('My Profile')"
    UPDATE_DETAILS_BTN = "button:has-text('Update details')"
    SHOW_NRIC_BTN = "button:has-text('Show NRIC')"
    HIDE_NRIC_BTN = "button:has-text('Hide NRIC')"

    # Singpass Identity (Read-only) Locators
    FULL_NAME_VAL = "dt:has-text('Full Name') + dd, [data-testid='full-name']"
    NRIC_VAL = "dt:has-text('NRIC') + dd, [data-testid='nric']"
    RESIDENTIAL_ADDRESS_VAL = "dt:has-text('Residential') + dd, [data-testid='residential-address']"

    # Contact & Mailing Summary Locators (View Mode)
    MOBILE_VAL = "dt:has-text('Mobile') + dd, [data-testid='mobile-phone']"
    EMAIL_VAL = "dt:has-text('Email') + dd, [data-testid='email-address']"

    # Edit Mode Form Inputs
    INPUT_PHONE = "input[name='phoneNumber']"
    INPUT_EMAIL = "input[name='email']"
    INPUT_BLOCK = "input[name='mailingBlock']"
    INPUT_STREET = "input[name='mailingStreet']"
    INPUT_UNIT = "input[name='mailingUnit']"
    INPUT_POSTAL = "input[name='mailingPostalCode']"
    INPUT_COUNTRY = "input[name='mailingCountry']"

    # Edit Mode Controls & Alerts
    DIRTY_STATE_HINT = "p:has-text('Make a change to enable saving.')"
    SAVE_CHANGES_BTN = "button[type='submit']:has-text('Save changes'), button:has-text('Save changes')"
    CANCEL_BTN = "button:has-text('Cancel')"
    INLINE_ALERT = "div[role='alert'], p[role='alert'], p[class*='error']"

    # Confirm Dialog Locators
    CONFIRM_ALERTDIALOG = "div[role='alertdialog']"
    DIALOG_KEEP_EDITING_BTN = "div[role='alertdialog'] button:has-text('Keep editing')"
    DIALOG_CONFIRM_SAVE_BTN = "div[role='alertdialog'] button:has-text('Save changes')"
    DIALOG_ERROR_MSG = "div[role='alertdialog'] p[role='alert'], div[role='alertdialog'] p[class*='error']"

    # Success Toast
    SUCCESS_TOAST = "p[role='status']:has-text('Your details have been updated.')"

    def __init__(self, page: Page):
        super().__init__(page)
        self.portal_base_url = os.environ.get("BASE_URL", "http://localhost:5174").rstrip("/")

    def open(self, base_url: Optional[str] = None):
        """Open the /profile page."""
        target_base = (base_url or self.portal_base_url).rstrip("/")
        self.page.goto(f"{target_base}{self.URL_PATH}")
        self.wait_for_profile_loaded()

    def wait_for_profile_loaded(self, timeout: int = 20000):
        """Wait for profile page heading and content to finish loading."""
        self.page.wait_for_selector(self.PROFILE_HEADING, timeout=timeout)
        try:
            loading = self.page.locator("p[role='status']:has-text('Loading your profile')")
            if loading.count() > 0:
                loading.wait_for(state="detached", timeout=timeout)
            self.page.wait_for_selector(f"{self.UPDATE_DETAILS_BTN}, {self.SAVE_CHANGES_BTN}", timeout=timeout)
        except Exception:
            pass

    def is_view_mode_rendered(self) -> bool:
        """Check if Profile view mode is rendered."""
        return self.is_visible(self.PROFILE_HEADING) and self.is_visible(self.UPDATE_DETAILS_BTN)

    def get_full_name(self) -> str:
        """Retrieve displayed Full Name (Read-only Singpass identity)."""
        if self.is_visible(self.FULL_NAME_VAL):
            return self.page.locator(self.FULL_NAME_VAL).first.inner_text().strip()
        # Fallback to search around term
        loc = self.page.locator("text='Full Name'").first
        if loc.count() > 0:
            return loc.evaluate("el => el.closest('div') ? el.closest('div').innerText : ''")
        return ""

    def get_nric_display(self) -> str:
        """Retrieve current text displayed for NRIC."""
        # Find container near NRIC
        loc = self.page.locator("text='NRIC / FIN'").first
        if loc.count() > 0:
            parent_text = loc.evaluate("el => el.closest('div') ? el.closest('div').innerText : ''")
            return parent_text.strip()
        return ""

    def is_nric_hidden(self) -> bool:
        """Check if NRIC is masked/hidden."""
        return self.is_visible(self.SHOW_NRIC_BTN) or "NRIC hidden" in self.page.content()

    def toggle_show_nric(self):
        """Click 'Show NRIC' button."""
        if self.is_visible(self.SHOW_NRIC_BTN):
            self.page.click(self.SHOW_NRIC_BTN)

    def toggle_hide_nric(self):
        """Click 'Hide NRIC' button."""
        if self.is_visible(self.HIDE_NRIC_BTN):
            self.page.click(self.HIDE_NRIC_BTN)

    def click_update_details(self):
        """Click 'Update details' button to enter Edit mode."""
        self.page.wait_for_selector(self.UPDATE_DETAILS_BTN)
        self.page.click(self.UPDATE_DETAILS_BTN)
        self.page.wait_for_selector(self.INPUT_EMAIL)

    def is_in_edit_mode(self) -> bool:
        """Check if profile form is currently in edit mode."""
        return self.is_visible(self.INPUT_EMAIL) and self.is_visible(self.SAVE_CHANGES_BTN)

    def is_save_disabled(self) -> bool:
        """Check if 'Save changes' button is disabled."""
        btn = self.page.locator(self.SAVE_CHANGES_BTN).first
        return btn.is_disabled() if btn.count() > 0 else True

    def fill_contact_and_mailing_form(
        self,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        block: Optional[str] = None,
        street: Optional[str] = None,
        unit: Optional[str] = None,
        postal_code: Optional[str] = None,
        country: Optional[str] = None,
    ):
        """Populate form inputs in Edit Mode."""
        if phone is not None and self.is_visible(self.INPUT_PHONE):
            self.page.locator(self.INPUT_PHONE).first.fill(phone)
        if email is not None and self.is_visible(self.INPUT_EMAIL):
            self.page.locator(self.INPUT_EMAIL).first.fill(email)
        if block is not None and self.is_visible(self.INPUT_BLOCK):
            self.page.locator(self.INPUT_BLOCK).first.fill(block)
        if street is not None and self.is_visible(self.INPUT_STREET):
            self.page.locator(self.INPUT_STREET).first.fill(street)
        if unit is not None and self.is_visible(self.INPUT_UNIT):
            self.page.locator(self.INPUT_UNIT).first.fill(unit)
        if postal_code is not None and self.is_visible(self.INPUT_POSTAL):
            self.page.locator(self.INPUT_POSTAL).first.fill(postal_code)
        if country is not None and self.is_visible(self.INPUT_COUNTRY):
            self.page.locator(self.INPUT_COUNTRY).first.fill(country)

    def click_save_changes(self):
        """Click 'Save changes' submit button."""
        self.page.click(self.SAVE_CHANGES_BTN)

    def is_confirm_dialog_open(self, timeout: int = 2000) -> bool:
        """Check if confirm alertdialog modal is visible."""
        try:
            loc = self.page.locator(self.CONFIRM_ALERTDIALOG)
            return loc.count() > 0 and loc.first.is_visible(timeout=timeout)
        except Exception:
            return False

    def wait_for_confirm_dialog_closed(self, timeout: int = 3000) -> bool:
        """Wait for confirmation modal to detach or hide."""
        try:
            self.page.locator(self.CONFIRM_ALERTDIALOG).first.wait_for(state="detached", timeout=timeout)
            return True
        except Exception:
            return not self.is_confirm_dialog_open(timeout=500)

    def confirm_dialog_save(self):
        """Click 'Save changes' button inside the confirmation dialog."""
        self.page.wait_for_selector(self.DIALOG_CONFIRM_SAVE_BTN)
        self.page.click(self.DIALOG_CONFIRM_SAVE_BTN)

    def confirm_dialog_keep_editing(self):
        """Click 'Keep editing' button inside the confirmation dialog."""
        self.page.wait_for_selector(self.DIALOG_KEEP_EDITING_BTN)
        self.page.click(self.DIALOG_KEEP_EDITING_BTN)
        self.wait_for_confirm_dialog_closed()

    def is_dialog_error_visible(self, timeout: int = 3000) -> bool:
        """Check if error message inside confirmation dialog is visible."""
        try:
            loc = self.page.locator(self.DIALOG_ERROR_MSG)
            return loc.count() > 0 and loc.first.is_visible(timeout=timeout)
        except Exception:
            return False

    def get_dialog_error_text(self) -> str:
        """Retrieve error text displayed inside the confirmation dialog."""
        if self.is_dialog_error_visible():
            return self.page.locator(self.DIALOG_ERROR_MSG).first.inner_text().strip()
        return ""

    def click_cancel(self):
        """Click 'Cancel' button to exit edit mode."""
        self.page.click(self.CANCEL_BTN)

    def is_inline_error_visible(self) -> bool:
        """Check if any validation error alert is visible."""
        return self.is_visible(self.INLINE_ALERT)

    def get_inline_error_text(self) -> str:
        """Get text content of inline validation error."""
        if self.is_inline_error_visible():
            return self.page.locator(self.INLINE_ALERT).first.inner_text().strip()
        return ""

    def is_success_toast_visible(self, timeout: int = 5000) -> bool:
        """Check if update success message appears."""
        try:
            self.page.wait_for_selector(self.SUCCESS_TOAST, timeout=timeout)
            return True
        except PlaywrightTimeoutError:
            return False

    def get_success_toast_text(self) -> str:
        """Retrieve success toast message text."""
        if self.is_success_toast_visible():
            return self.page.locator(self.SUCCESS_TOAST).first.inner_text().strip()
        return ""

    def get_state_snapshot(self) -> Dict[str, Any]:
        """Capture state snapshot for Exceptor adjudication."""
        success = self.is_success_toast_visible(timeout=1000)
        errors = {}
        if self.is_inline_error_visible():
            errors["validation"] = self.get_inline_error_text()
        return {
            "success_visible": success,
            "visible_errors": errors,
            "in_edit_mode": self.is_in_edit_mode(),
            "save_disabled": self.is_save_disabled(),
        }
