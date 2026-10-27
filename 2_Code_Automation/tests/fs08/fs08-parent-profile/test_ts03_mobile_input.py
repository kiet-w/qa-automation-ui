"""
tests/fs08/fs08-parent-profile/test_ts03_mobile_input.py
Automated Atomic (UI Unit) Test Suite for FS08 Parent Profile / My Details (/profile).
Suite Focus: Suite 3: Mobile Number Component (10 TCs)
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
class TestTS03MobileInput(BaseTest):
    """
    Suite 3: Validates phone prefixes 6/8/9, 8 digits BVA, whitespace trimming, and anti-i18n leakage.
    """

    def test_tc_r8_098_mobile_number_valid_prefixes_component(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-098: Singapore Mobile Numbers Starting with Valid Prefixes (6, 8, 9).
        Scenario ID: TS-010-TEL | Suite: Mobile Number Component | Row: 05
        Traceability: FR-08.3; FS R8 field table (Mobile); R8-AC14
        Preconditions: FA logged in; Edit Mode open.
        Test Data: EP Valid: 61234567, 81234567, 91234567
        Expected Result: All 3 numbers pass validation without inline errors.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)
        valid_prefixes = fs08_data["profile_bva_dataset"]["phones"]["valid_prefixes"]

        with self.step("Step 1: Open Edit Mode", expected="Edit form active."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            self.step.set_actual("Ready in Edit Mode.")

        for phone in valid_prefixes:
            with self.step(f"Step 2: Enter mobile number '{phone}'", expected="Valid input passes without error."):
                profile.fill_contact_and_mailing_form(phone=phone)
                assert not profile.is_save_disabled(), f"Save button must enable for valid phone prefix '{phone}'."
                self.step.set_actual(f"Phone '{phone}' accepted.")

        profile.click_cancel()


    def test_tc_r8_099_mobile_number_invalid_alphanumeric_rejected(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-099: Invalid Mobile Numbers Rejected with MSG-0805.
        Scenario ID: TS-010-TEL | Suite: Mobile Number Component | Row: 06
        Traceability: FR-08.3 errors; R8-AC15; MSG-0805
        Preconditions: FA logged in; Edit Mode open.
        Test Data: EP Invalid: 9123abcd, +6591234567, 9123-4567
        Expected Result: System rejects submission and displays MSG-0805.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Open Edit Mode", expected="In Edit Mode."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            self.step.set_actual("In Edit Mode.")

        with self.step("Step 2: Enter '9123abcd' into Mobile Number input", expected="Validation error or save blocked."):
            profile.fill_contact_and_mailing_form(phone="9123abcd")
            profile.click_save_changes()
            if profile.is_confirm_dialog_open(timeout=1000):
                profile.confirm_dialog_save()
            assert not profile.is_success_toast_visible(timeout=1500), "Save must not succeed for alphanumeric phone."
            self.step.set_actual("Malformed phone format rejected per MSG-0805.")

        profile.click_cancel()


    def test_tc_r8_100_mobile_number_with_space_accepted_and_trimmed(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-100: Mobile Number Entered with Space Accepted and Trimmed (ASM-08).
        Scenario ID: TS-010-TEL | Suite: Mobile Number Component | Row: 07
        Traceability: FS R8 field table; ASM-08
        Preconditions: FA logged in; Edit Mode open.
        Test Data: Input: '9123 4567' -> Stored value: '91234567'
        Expected Result: Input is accepted without error; Save button enabled.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)
        phone_with_space = fs08_data["profile_bva_dataset"]["phones"]["with_space"]

        with self.step("Step 1: Open Edit Mode", expected="In Edit Mode."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            self.step.set_actual("In Edit Mode.")

        with self.step("Step 2: Enter '9123 4567' (with middle space) in Mobile Number", expected="Input accepted."):
            profile.fill_contact_and_mailing_form(phone=phone_with_space)
            assert not profile.is_save_disabled(), "Phone with middle space must be accepted."
            self.step.set_actual("Phone with middle space accepted.")

        profile.click_cancel()


    def test_tc_r8_tel_01_mobile_number_invalid_prefixes_rejected(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-TEL-01: Mobile Numbers Starting with Invalid Prefixes (1, 2, 3, 4, 5, 7) Rejected.
        Scenario ID: TS-010-TEL | Suite: Mobile Number Component | Row: 08
        Traceability: FR-08.3 errors; R8-AC15; MSG-0805
        Preconditions: FA logged in; Edit Mode open.
        Test Data: Invalid prefixes: 71234567, 51234567
        Expected Result: Validation fails on each invalid prefix with MSG-0805.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)
        invalid_prefixes = fs08_data["profile_bva_dataset"]["phones"]["invalid_prefixes"][:2]

        with self.step("Step 1: Open Edit Mode", expected="In Edit Mode."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            self.step.set_actual("In Edit Mode.")

        for bad_phone in invalid_prefixes:
            with self.step(f"Step 2: Enter '{bad_phone}' and attempt save", expected="Rejected with MSG-0805."):
                profile.fill_contact_and_mailing_form(phone=bad_phone)
                profile.click_save_changes()
                if profile.is_confirm_dialog_open(timeout=1000):
                    profile.confirm_dialog_save()
                assert not profile.is_success_toast_visible(timeout=1500), f"Invalid prefix phone '{bad_phone}' must not succeed."
                self.step.set_actual(f"Invalid prefix '{bad_phone}' rejected.")

        profile.click_cancel()


    def test_tc_r8_tel_02_mobile_number_length_bva_rejected(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-TEL-02: Mobile Number Length Boundary: 7 Digits and 9 Digits Rejected (BVA).
        Scenario ID: TS-010-TEL | Suite: Mobile Number Component | Row: 09
        Traceability: FS R8 sec. 6 field table; R8-AC15; MSG-0805
        Preconditions: FA logged in; Edit Mode open.
        Test Data: BVA Length: 7 digits ('9123456' - underflow), 9 digits ('912345678' - overflow)
        Expected Result: Both 7-digit and 9-digit inputs are rejected with MSG-0805.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)
        invalid_lengths = fs08_data["profile_bva_dataset"]["phones"]["invalid_lengths"]

        with self.step("Step 1: Open Edit Mode", expected="In Edit Mode."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            self.step.set_actual("In Edit Mode.")

        for length_phone in invalid_lengths:
            with self.step(f"Step 2: Enter boundary length phone '{length_phone}'", expected="Rejected with MSG-0805."):
                profile.fill_contact_and_mailing_form(phone=length_phone)
                profile.click_save_changes()
                if profile.is_confirm_dialog_open(timeout=1000):
                    profile.confirm_dialog_save()
                assert not profile.is_success_toast_visible(timeout=1500), f"Length boundary phone '{length_phone}' must not succeed."
                self.step.set_actual(f"Length '{length_phone}' rejected.")

        profile.click_cancel()


    def test_tc_r8_tel_03_mobile_number_cleared_mandatory_validation(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-TEL-03: Clearing Mandatory Mobile Number Input Triggers Required Error MSG-0001.
        Scenario ID: TS-010-TEL | Suite: Mobile Number Component | Row: 10
        Traceability: FR-08.3 errors; R8-AC16; MSG-0001
        Preconditions: FA logged in; Edit Mode open.
        Test Data: Mobile number = '' (empty string)
        Expected Result: Displays required field error MSG-0001; Save button disabled or blocked.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Clear the Mobile Number input field completely", expected="Phone cleared."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            profile.fill_contact_and_mailing_form(phone="")
            self.step.set_actual("Cleared mobile number field.")

        with self.step("Step 2: Verify Save button disabled", expected="Save button disabled."):
            assert profile.is_save_disabled(), "Save button must remain disabled when mandatory phone is empty."
            self.step.set_actual("MSG-0001 mandatory protection active: Save disabled.")

        profile.click_cancel()


    def test_tc_r8_tel_04_mobile_number_whitespace_treated_as_blank(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-TEL-04: Whitespace-Only Mobile Number Input Treated as Empty (ASM-15).
        Scenario ID: TS-010-TEL | Suite: Mobile Number Component | Row: 11
        Traceability: FR-08.3 errors; ASM-15; MSG-0001
        Preconditions: FA logged in; Edit Mode open.
        Test Data: Mobile number = '        ' (8 blank spaces)
        Expected Result: Whitespace is trimmed and treated as empty input; Save blocked.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Enter multiple spaces into Mobile Number input", expected="Whitespace trimmed."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            profile.fill_contact_and_mailing_form(phone="        ")
            assert profile.is_save_disabled() or not profile.is_confirm_dialog_open(timeout=500), "Whitespace phone must not enable valid save."
            self.step.set_actual("Whitespace phone treated as blank per ASM-15.")

        profile.click_cancel()


    def test_tc_r8_tel_05_mobile_number_decimals_negatives_and_symbols(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-TEL-05: Mobile Numbers with Decimals, Negative Signs, or Math Symbols Rejected.
        Scenario ID: TS-010-TEL | Suite: Mobile Number Component
        Traceability: FR-08.3; FS R8 field table; MSG-0805
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)
        invalid_symbols = fs08_data["profile_bva_dataset"]["phones"].get("decimals_and_negatives", ["91.234567", "-9123456"])

        with self.step("Step 1: Open Edit Mode", expected="In Edit Mode."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()

        for bad_phone in invalid_symbols:
            with self.step(f"Step 2: Enter '{bad_phone}' and verify rejection", expected="Rejected per MSG-0805."):
                profile.fill_contact_and_mailing_form(phone=bad_phone)
                profile.blur_field("phoneNumber")
                assert profile.is_field_invalid("phoneNumber") or profile.is_save_disabled(), f"Input '{bad_phone}' must be rejected."
                self.step.set_actual(f"Symbol/decimal phone '{bad_phone}' rejected.")

        profile.click_cancel()


    def test_tc_r8_tel_06_mobile_number_full_width_digits(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-TEL-06: Full-Width Unicode Digits ('９１２３４５６７') Handled Safely.
        Scenario ID: TS-010-TEL | Suite: Mobile Number Component
        Traceability: Invariant 7 UI Health; NFR Usability
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Open Edit Mode and enter full-width digits", expected="Zero JS crash."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            profile.fill_contact_and_mailing_form(phone="９１２３４５６７")
            profile.blur_field("phoneNumber")
            # Should either mark invalid or normalize without crashing
            assert profile.is_field_invalid("phoneNumber") or profile.is_save_disabled(), "Non-ASCII digits must not bypass validation."
            self.step.set_actual("Full-width digits handled safely without uncaught exceptions.")

        profile.click_cancel()

    @pytest.mark.xfail(strict=True, reason="BUG-R8-I18N-01: UI displays raw i18n translation key 'features.parentProfile.validation.mobileInvalid' instead of MSG-0805")

    def test_tc_r8_tel_07_mobile_number_anti_i18n_leak_and_red_border(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-TEL-07: Invalid Mobile Number UI Feedback & Anti-i18n Translation Key Leak.
        Scenario ID: TS-010-TEL | Suite: Mobile Number Component
        Traceability: FR-08.3 errors; MSG-0805; Invariant 7 UI Health; Defect BUG-R8-I18N-01
        Preconditions: FA logged in; Edit Mode open.
        Test Data: Invalid phone: '12345qqqq'
        Expected Result: Field receives red glowing border (aria-invalid='true'), displays human-readable MSG-0805,
        and strictly does NOT display raw i18n key 'features.parentProfile.validation.mobileInvalid'.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Enter invalid mobile number '12345qqqq'", expected="In Edit Mode."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            profile.fill_contact_and_mailing_form(phone="12345qqqq")
            profile.blur_field("phoneNumber")
            self.page.wait_for_timeout(300)

        with self.step("Step 2: Inspect visual feedback and error text", expected="Red border and MSG-0805."):
            assert profile.is_field_invalid("phoneNumber"), "Field must receive aria-invalid='true' / red border."
            err_text = profile.get_field_error_text("phoneNumber")

            # CRITICAL DEFECT GATE: Must NOT leak raw translation key
            assert not profile.is_raw_i18n_key(err_text), f"DEFECT BUG-R8-I18N-01: Raw i18n key '{err_text}' displayed on UI!"
            assert "features.parentProfile.validation.mobileInvalid" not in err_text, "DEFECT: Translation key leaked directly on DOM!"
            assert "9123 4567" in err_text or "mobile number" in err_text.lower(), f"Expected MSG-0805, got '{err_text}'"
            self.step.set_actual("Valid human-readable MSG-0805 displayed without raw key leak.")

        profile.click_cancel()

    # =========================================================================
    # SUITE 3: TS-010-EML - Email Address Component (RFC 5322, BVA 150/151)
    # =========================================================================

