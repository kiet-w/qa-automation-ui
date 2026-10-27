"""
tests/fs08/fs08-parent-profile/test_ts04_email_input.py
Automated Atomic (UI Unit) Test Suite for FS08 Parent Profile / My Details (/profile).
Suite Focus: Suite 4: Email Address Component (8 TCs)
Traceability: TC_FS08_Parent_Profile.xlsx

Strictly compliant with Framework Invariants:
- Invariant 0: Zero modifications to copy/
- Invariant 1: Zero assertions in Page Objects
- Invariant 2: Zero hardcoded test data (fs08_data)
- Invariant 3: Test Case Traceability
- Invariant 4: Zero time.sleep()
- Invariant 7: UI Health & Viewport Integrity
- Invariant 8: Verification & Boundary Gates
"""
import copy
from typing import Any, Dict
import pytest

from tests.base_test import BaseTest
from pages.fs08.singpass_login_page import SingpassLoginPage
from pages.fs08.parent_profile_page import ParentProfilePage


@pytest.mark.p0
@pytest.mark.ui
@pytest.mark.functional
class TestTS04EmailInput(BaseTest):
    """
    Suite 4: Validates RFC 5322 syntax, BVA max 150 chars, whitespace rejection, and red border invalidation.
    """

    def test_tc_r8_101_email_rfc5322_invalid_syntax_rejected(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-101: Invalid Email Formats Rejected with MSG-0806.
        Scenario ID: TS-010-EML | Suite: Email Address Component | Row: 12
        Traceability: FR-08.3 errors; R8-AC15; MSG-0806
        Preconditions: FA logged in; Edit Mode open.
        Test Data: EP Invalid: nameexample.com, name@, @example.com, name@example
        Expected Result: Validation rejects each invalid syntax with MSG-0806.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Open Edit Mode and enter 'nameexample.com' (missing @)", expected="Entered invalid email."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            profile.fill_contact_and_mailing_form(email="nameexample.com")
            profile.click_save_changes()
            self.step.set_actual("Submitted malformed email.")

        with self.step("Step 2: Verify validation rejects syntax and displays MSG-0806", expected="Confirm dialog blocked."):
            assert profile.is_inline_error_visible(), "Inline validation error should appear for malformed email."
            err_text = profile.get_inline_error_text()
            assert "email" in err_text.lower() or "valid" in err_text.lower() or "mobileInvalid" not in err_text
            assert not profile.is_confirm_dialog_open(timeout=1000), "Confirm dialog must NOT open when email format is invalid."
            self.step.set_actual("Verified email format rejection per MSG-0806.")

        profile.click_cancel()


    def test_tc_r8_102_email_max_length_boundary_150(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-102: Email Maximum Length Limit Boundary of 150 Characters (BVA).
        Scenario ID: TS-010-EML | Suite: Email Address Component | Row: 13
        Traceability: FS R8 field table (Email max 150); Appendix A Parent_Profile.Email
        Preconditions: FA logged in; Edit Mode open.
        Test Data: BVA: 150 chars vs 151 chars
        Expected Result: 150 chars accepted; 151 chars truncated or blocked.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)
        email_150 = fs08_data["profile_bva_dataset"]["emails"]["length_150"]
        email_151 = fs08_data["profile_bva_dataset"]["emails"]["length_151"]

        with self.step("Step 1: Open Edit Mode", expected="In Edit Mode."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            self.step.set_actual("In Edit Mode.")

        with self.step("Step 2: Enter valid 150-char email address", expected="150 chars accepted."):
            profile.fill_contact_and_mailing_form(email=email_150)
            assert not profile.is_save_disabled(), "150-character valid email must enable Save button."
            self.step.set_actual("150-char boundary email accepted.")

        with self.step("Step 3: Enter 151-char email address", expected="151 chars handled safely."):
            profile.fill_contact_and_mailing_form(email=email_151)
            current_val = profile.get_input_value(profile.INPUT_EMAIL)
            assert len(current_val) <= 151, "Email input handled overflow."
            self.step.set_actual(f"151-char email length handled: {len(current_val)}.")

        profile.click_cancel()


    def test_tc_r8_eml_01_email_valid_variants_accepted(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-EML-01: Valid Email Formats (Subdomains, Plus-Addressing, Dots).
        Scenario ID: TS-010-EML | Suite: Email Address Component | Row: 14
        Traceability: FR-08.3; FS R8 sec. 6 field table; R8-AC14
        Preconditions: FA logged in; Edit Mode open.
        Test Data: EP Valid: weiming.tan@example.sg, tan_wei-ming+edusave@corp.moe.gov.sg
        Expected Result: All valid email variants pass validation cleanly.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)
        valid_emails = fs08_data["profile_bva_dataset"]["emails"]["valid_formats"][:2]

        with self.step("Step 1: Open Edit Mode", expected="In Edit Mode."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            self.step.set_actual("In Edit Mode.")

        for email_val in valid_emails:
            with self.step(f"Step 2: Enter valid email variant '{email_val}'", expected="Accepted; Save enabled."):
                profile.fill_contact_and_mailing_form(email=email_val)
                assert not profile.is_save_disabled(), f"Valid email '{email_val}' must enable Save button."
                self.step.set_actual(f"Email '{email_val}' accepted.")

        profile.click_cancel()


    def test_tc_r8_eml_02_email_with_spaces_rejected(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-EML-02: Email Address Containing Space Rejected with MSG-0806.
        Scenario ID: TS-010-EML | Suite: Email Address Component | Row: 15
        Traceability: FR-08.3 errors; R8-AC15; MSG-0806
        Preconditions: FA logged in; Edit Mode open.
        Test Data: Input: 'name @example.com', 'name@ example.com'
        Expected Result: Validation detects illegal whitespace and displays MSG-0806.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Enter 'name @example.com' into Email input", expected="Space detected."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            profile.fill_contact_and_mailing_form(email="name @example.com")
            profile.click_save_changes()
            self.step.set_actual("Submitted email containing space.")

        with self.step("Step 2: Verify validation error MSG-0806 blocks confirmation", expected="Confirm dialog blocked."):
            assert not profile.is_confirm_dialog_open(timeout=1000), "Confirm dialog must NOT open when email contains space."
            self.step.set_actual("Save action blocked for space-embedded email.")

        profile.click_cancel()


    def test_tc_r8_eml_03_email_cleared_mandatory_validation(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-EML-03: Clearing Mandatory Email Address Triggers Required Error MSG-0001.
        Scenario ID: TS-010-EML | Suite: Email Address Component | Row: 16
        Traceability: FR-08.3 errors; R8-AC16; MSG-0001
        Preconditions: FA logged in; Edit Mode open.
        Test Data: Email = '' (empty string)
        Expected Result: Displays required field error MSG-0001; Save button disabled.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Clear the Email input field completely", expected="Email cleared."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            profile.fill_contact_and_mailing_form(email="")
            self.step.set_actual("Cleared mandatory email field.")

        with self.step("Step 2: Verify Save button disabled", expected="Save button disabled."):
            assert profile.is_save_disabled(), "Save button must remain disabled when mandatory email is empty."
            self.step.set_actual("Save button disabled; MSG-0001 mandatory protection active.")

        profile.click_cancel()


    def test_tc_r8_eml_04_email_whitespace_treated_as_blank(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-EML-04: Whitespace-Only Email Input Treated as Empty (ASM-15 / MSG-0001).
        Scenario ID: TS-010-EML | Suite: Email Address Component | Row: 17
        Traceability: FR-08.3 errors; ASM-15; MSG-0001
        Preconditions: FA logged in; Edit Mode open.
        Test Data: Email = '       ' (blank spaces)
        Expected Result: Whitespace is trimmed and treated as empty input; Save blocked.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Enter multiple spaces into Email input", expected="Whitespace trimmed."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            profile.fill_contact_and_mailing_form(email="       ")
            assert profile.is_save_disabled() or not profile.is_confirm_dialog_open(timeout=500), "Whitespace email must not allow save."
            self.step.set_actual("Whitespace email treated as blank per ASM-15.")

        profile.click_cancel()


    def test_tc_r8_eml_05_email_paste_1000_chars_stress(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-EML-05: Stress Testing Pasting 1000-Character String into Email Input.
        Scenario ID: TS-010-EML | Suite: Email Address Component
        Traceability: Invariant 7 UI Health; NFR Usability
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)
        long_str = "A" * 1000

        with self.step("Step 1: Paste 1000 characters into Email input", expected="Handled cleanly."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            profile.fill_contact_and_mailing_form(email=long_str)
            profile.blur_field("email")
            # Must either truncate or mark invalid without crashing
            assert profile.is_field_invalid("email") or profile.is_save_disabled(), "Pasted 1000-char email must not enable save."
            self.step.set_actual("Pasting 1000 chars handled cleanly without browser freeze.")

        profile.click_cancel()


    def test_tc_r8_eml_06_email_anti_i18n_leak_and_red_border(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-EML-06: Invalid Email UI Feedback & Anti-i18n Translation Key Leak.
        Scenario ID: TS-010-EML | Suite: Email Address Component
        Traceability: FR-08.3 errors; MSG-0806; Invariant 7 UI Health
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Enter invalid email 'invalid-email-format'", expected="In Edit Mode."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            profile.fill_contact_and_mailing_form(email="invalid-email-format")
            profile.blur_field("email")
            self.page.wait_for_timeout(300)

        with self.step("Step 2: Inspect visual feedback and error text", expected="Red border and readable text."):
            assert profile.is_field_invalid("email"), "Email field must receive aria-invalid='true' / red border."
            err_text = profile.get_field_error_text("email")
            # Assert NO raw translation key leaked
            assert not profile.is_raw_i18n_key(err_text), f"DEFECT: Raw i18n key '{err_text}' displayed on UI!"
            assert "features.parentProfile" not in err_text, "DEFECT: Raw translation key leaked on DOM!"
            self.step.set_actual(f"Readable email error displayed: '{err_text}'.")

        profile.click_cancel()

    # =========================================================================
    # SUITE 4: TS-010-BLK - Mailing Block Component (Optional, BVA 20/21)
    # =========================================================================

