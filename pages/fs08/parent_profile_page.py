"""
pages/fs08/parent_profile_page.py - Page Object Model for Parent Profile & My Details.
Complies with Invariant 1 (UI actions & state reading only) and Invariant 9 (<200 lines).
"""
import os
import re
from typing import Any, Dict, Optional
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError

from pages.base_page import BasePage
from pages.fs08.locators import ParentProfileLocators as Loc
from components.form_helper import FormHelper


class ParentProfilePage(BasePage):
    """Page Object for Parent Profile, NRIC toggle, Contact details editing, and Confirmation Modal."""

    URL_PATH = "/profile"
    PROFILE_HEADING = Loc.PROFILE_HEADING
    UPDATE_DETAILS_BTN = Loc.UPDATE_DETAILS_BTN
    SHOW_NRIC_BTN = Loc.SHOW_NRIC_BTN
    HIDE_NRIC_BTN = Loc.HIDE_NRIC_BTN
    INPUT_PHONE = Loc.INPUT_PHONE
    INPUT_EMAIL = Loc.INPUT_EMAIL
    INPUT_BLOCK = Loc.INPUT_BLOCK
    INPUT_STREET = Loc.INPUT_STREET
    INPUT_UNIT = Loc.INPUT_UNIT
    INPUT_POSTAL = Loc.INPUT_POSTAL
    INPUT_COUNTRY = Loc.INPUT_COUNTRY
    SAVE_CHANGES_BTN = Loc.SAVE_CHANGES_BTN
    CANCEL_BTN = Loc.CANCEL_BTN
    CONFIRM_ALERTDIALOG = Loc.CONFIRM_ALERTDIALOG

    def __init__(self, page: Page):
        super().__init__(page)
        self.portal_base_url = os.environ.get("BASE_URL", "http://localhost:5174").rstrip("/")
        self.form = FormHelper(page, container=Loc.UPDATE_FORM)

    def open(self, base_url: Optional[str] = None):
        """Open the /profile page."""
        target_base = (base_url or self.portal_base_url).rstrip("/")
        self.page.goto(f"{target_base}{self.URL_PATH}")
        self.wait_for_profile_loaded()
        return self

    def wait_for_profile_loaded(self, timeout: int = 15000):
        """Wait for profile page heading and content to finish loading."""
        self.page.wait_for_selector(Loc.PROFILE_HEADING, timeout=timeout)
        try:
            self.page.locator("p[role='status']:has-text('Loading')").wait_for(state="detached", timeout=3000)
        except Exception:
            pass

    def is_view_mode_rendered(self) -> bool:
        """Check if Profile view mode is rendered."""
        return self.is_visible(Loc.PROFILE_HEADING) and self.is_visible(Loc.UPDATE_DETAILS_BTN)

    def get_full_name(self) -> str:
        """Retrieve displayed Full Name (Read-only Singpass identity)."""
        loc = self.page.locator(Loc.FULL_NAME_VAL).first
        return loc.inner_text().strip() if loc.count() > 0 and loc.is_visible() else ""

    def get_nric_display(self) -> str:
        """Retrieve current text displayed for NRIC."""
        loc = self.page.locator(Loc.NRIC_VAL).first
        return loc.inner_text().strip() if loc.count() > 0 and loc.is_visible() else ""

    def is_nric_hidden(self) -> bool:
        """Check if NRIC is masked/hidden."""
        return self.is_visible(Loc.SHOW_NRIC_BTN) or "NRIC hidden" in self.page.content()

    def toggle_show_nric(self):
        """Click 'Show NRIC' button."""
        if self.is_visible(Loc.SHOW_NRIC_BTN):
            self.page.click(Loc.SHOW_NRIC_BTN)

    def toggle_hide_nric(self):
        """Click 'Hide NRIC' button."""
        if self.is_visible(Loc.HIDE_NRIC_BTN):
            self.page.click(Loc.HIDE_NRIC_BTN)

    def click_update_details(self):
        """Click 'Update details' button to enter Edit mode."""
        self.page.click(Loc.UPDATE_DETAILS_BTN)
        self.page.wait_for_selector(Loc.INPUT_EMAIL)

    def is_in_edit_mode(self) -> bool:
        """Check if profile form is currently in edit mode."""
        return self.is_visible(Loc.INPUT_EMAIL) and self.is_visible(Loc.SAVE_CHANGES_BTN)

    def is_save_disabled(self) -> bool:
        """Check if 'Save changes' button is disabled."""
        btn = self.page.locator(Loc.SAVE_CHANGES_BTN).first
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
        data = {
            "phoneNumber": (Loc.INPUT_PHONE, phone),
            "email": (Loc.INPUT_EMAIL, email),
            "mailingBlock": (Loc.INPUT_BLOCK, block),
            "mailingStreet": (Loc.INPUT_STREET, street),
            "mailingUnit": (Loc.INPUT_UNIT, unit),
            "mailingPostalCode": (Loc.INPUT_POSTAL, postal_code),
            "mailingCountry": (Loc.INPUT_COUNTRY, country),
        }
        for selector, value in data.values():
            if value is not None:
                self.page.locator(selector).fill(value)

    def click_save_changes(self):
        """Click 'Save changes' submit button."""
        self.page.click(Loc.SAVE_CHANGES_BTN)

    def is_confirm_dialog_open(self, timeout: int = 2000) -> bool:
        """Check if confirm alertdialog modal is visible."""
        return self.is_visible(Loc.CONFIRM_ALERTDIALOG, timeout=timeout)

    def confirm_dialog_save(self):
        """Click 'Save changes' button inside the confirmation dialog."""
        self.page.click(Loc.DIALOG_CONFIRM_SAVE_BTN)

    def confirm_dialog_keep_editing(self):
        """Click 'Keep editing' button inside the confirmation dialog."""
        self.page.click(Loc.DIALOG_KEEP_EDITING_BTN)

    def get_dialog_error_text(self) -> str:
        """Retrieve error text displayed inside the confirmation dialog."""
        loc = self.page.locator(Loc.DIALOG_ERROR_MSG).first
        return loc.inner_text().strip() if loc.count() > 0 and loc.is_visible() else ""

    def click_cancel(self):
        """Click 'Cancel' button to exit edit mode."""
        if self.is_visible(Loc.CANCEL_BTN):
            self.page.click(Loc.CANCEL_BTN)

    def get_field_error_text(self, field_name: str) -> str:
        """Get error message for a specific field name."""
        errors = self.form.get_field_errors()
        return errors.get(field_name, "")

    def is_field_invalid(self, field_name: str) -> bool:
        """Check if an input field is marked as invalid."""
        selector = self._field_selector(field_name)
        control = self.page.locator(selector)
        return control.count() > 0 and control.get_attribute("aria-invalid") == "true"

    def blur_field(self, field_name: str):
        """Trigger blur event on an input field to invoke inline field-level validation."""
        self.page.locator(self._field_selector(field_name)).blur()

    @staticmethod
    def _field_selector(field_name: str) -> str:
        """Map existing test data keys to the current accessible field names."""
        return {
            "phoneNumber": Loc.INPUT_PHONE,
            "email": Loc.INPUT_EMAIL,
            "mailingBlock": Loc.INPUT_BLOCK,
            "mailingStreet": Loc.INPUT_STREET,
            "mailingUnit": Loc.INPUT_UNIT,
            "mailingPostalCode": Loc.INPUT_POSTAL,
            "mailingCountry": Loc.INPUT_COUNTRY,
        }.get(field_name, field_name)

    def is_success_toast_visible(self, timeout: int = 5000) -> bool:
        """Check if update success message appears."""
        return self.is_visible(Loc.SUCCESS_TOAST, timeout=timeout)

    def get_state_snapshot(self) -> Dict[str, Any]:
        """Capture state snapshot for Exceptor adjudication."""
        errors = self.form.get_field_errors()
        dialog_err = self.get_dialog_error_text()
        if dialog_err:
            errors["dialog"] = dialog_err
        return {
            "success_visible": self.is_success_toast_visible(timeout=1000),
            "visible_errors": errors,
            "in_edit_mode": self.is_in_edit_mode(),
            "save_disabled": self.is_save_disabled(),
        }

    @staticmethod
    def is_raw_i18n_key(text: str) -> bool:
        """Adjudicate whether a displayed error string is an un-translated i18n key."""
        if not text:
            return False
        patterns = [r"^(features|validation|common|errors|profile)\.[a-zA-Z0-9_.]+$", r"\{\{\s*[\w.]+\s*\}\}"]
        return any(re.match(p, text.strip()) for p in patterns)
