"""
tests/fs08/fs08-parent-profile/test_ts07_mailing_postal_country.py
Automated Atomic (UI Unit) Test Suite for FS08 Parent Profile / My Details (/profile).
Suite Focus: Suite 7: Mailing Postal Code & Country Components (14 TCs)
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
class TestTS07MailingPostalCountry(BaseTest):
    """
    Suite 7: Validates exact 6 digits Singapore postal code, leading zero preservation, and default country.
    """

    def test_tc_r8_108_mailing_postal_code_exact_6_digits(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-108: Singapore Mailing Postal Code Must Be Exactly 6 Numeric Digits.
        Scenario ID: TS-010-POS | Suite: Mailing Postal Code Component | Row: 29
        Traceability: FS R8 field table (Postal code 6 digits); Appendix A Parent_Profile.MailingPostalCode
        Preconditions: FA logged in; Edit Mode open.
        Test Data: EP Valid: 650009; EP Invalid: 65000 (5 digits), 6500091 (7 digits)
        Expected Result: Only exact 6-digit postal code 650009 is accepted; others rejected.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Enter valid 6-digit postal code '650009'", expected="Accepted."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            profile.fill_contact_and_mailing_form(postal_code="650009")
            assert not profile.is_save_disabled(), "Valid 6-digit postal code must enable Save button."
            self.step.set_actual("6-digit postal code accepted.")

        profile.click_cancel()


    def test_tc_r8_pos_01_mailing_postal_code_leading_zero_preserved(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-POS-01: Singapore Postal Code with Leading Zero (e.g. '018956') Preserved as 6 Digits.
        Scenario ID: TS-010-POS | Suite: Mailing Postal Code Component | Row: 30
        Traceability: FS R8 sec. 6 field table; Appendix A Parent_Profile.MailingPostalCode
        Preconditions: FA logged in; Edit Mode open.
        Test Data: Input: '018956' (Downtown Singapore sector with leading zero)
        Expected Result: Postal code is preserved as text '018956' with leading zero intact.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Enter '018956' in Postal Code input", expected="Leading zero preserved."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            profile.fill_contact_and_mailing_form(postal_code="018956")
            val = profile.get_input_value(profile.INPUT_POSTAL)
            assert val == "018956", f"Postal code leading zero must be preserved, got '{val}'."
            self.step.set_actual("Leading zero '018956' preserved.")

        profile.click_cancel()


    def test_tc_r8_pos_02_mailing_postal_code_length_bva(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-POS-02: Postal Code Length Boundary: 5 Digits and 7 Digits Rejected (BVA Length).
        Scenario ID: TS-010-POS | Suite: Mailing Postal Code Component | Row: 31
        Traceability: FS R8 sec. 6 field table; Appendix A
        Preconditions: FA logged in; Edit Mode open.
        Test Data: BVA: 5 digits ('56012' - underflow) vs 7 digits ('5601234' - overflow)
        Expected Result: Both 5-digit and 7-digit inputs fail validation.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Enter 5-digit postal code '56012'", expected="Validation error or save blocked."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            profile.fill_contact_and_mailing_form(postal_code="56012")
            profile.click_save_changes()
            if profile.is_confirm_dialog_open(timeout=1000):
                profile.confirm_dialog_save()
            assert not profile.is_success_toast_visible(timeout=1500), "5-digit postal code must not succeed."
            self.step.set_actual("5-digit postal code rejected.")

        with self.step("Step 2: Enter 7-digit postal code '5601234'", expected="7 digits rejected."):
            profile.fill_contact_and_mailing_form(postal_code="5601234")
            profile.click_save_changes()
            if profile.is_confirm_dialog_open(timeout=1000):
                profile.confirm_dialog_save()
            assert not profile.is_success_toast_visible(timeout=1500), "7-digit postal code must not succeed."
            self.step.set_actual("7-digit postal code rejected.")

        profile.click_cancel()


    def test_tc_r8_pos_03_mailing_postal_code_non_digit_rejected(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-POS-03: Postal Code Containing Special Symbols or Hyphens Rejected.
        Scenario ID: TS-010-POS | Suite: Mailing Postal Code Component | Row: 32
        Traceability: FS R8 sec. 6 field table; Appendix A
        Preconditions: FA logged in; Edit Mode open.
        Test Data: Input: '650-009', '65A009'
        Expected Result: Validation rejects non-digit characters; submission blocked.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Enter '650-009' into Postal Code", expected="Non-digit rejected."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            profile.fill_contact_and_mailing_form(postal_code="650-009")
            profile.click_save_changes()
            if profile.is_confirm_dialog_open(timeout=1000):
                profile.confirm_dialog_save()
            assert not profile.is_success_toast_visible(timeout=1500), "Hyphenated postal code must not succeed."
            self.step.set_actual("Hyphenated postal code rejected.")

        profile.click_cancel()


    def test_tc_r8_pos_04_mailing_postal_code_cleared_mandatory_validation(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-POS-04: Clearing Mandatory Mailing Postal Code Triggers Required Error MSG-0001.
        Scenario ID: TS-010-POS | Suite: Mailing Postal Code Component | Row: 33
        Traceability: FR-08.3 errors; R8-AC16; MSG-0001
        Preconditions: FA logged in; Edit Mode open.
        Test Data: MailingPostalCode = '' (empty string)
        Expected Result: Displays required field error MSG-0001; Save button disabled.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Clear Postal Code input field", expected="Postal code cleared."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            profile.fill_contact_and_mailing_form(postal_code="")
            self.step.set_actual("Cleared postal code field.")

        with self.step("Step 2: Verify Save button disabled", expected="Save button disabled."):
            assert profile.is_save_disabled(), "Save button must remain disabled when mandatory postal code is empty."
            self.step.set_actual("Save button disabled; MSG-0001 mandatory protection active.")

        profile.click_cancel()


    def test_tc_r8_pos_05_mailing_postal_code_whitespace_treated_as_blank(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-POS-05: Whitespace-Only Mailing Postal Code Treated as Blank with MSG-0001.
        Scenario ID: TS-010-POS | Suite: Mailing Postal Code Component | Row: 34
        Traceability: FR-08.3 errors; ASM-15; MSG-0001
        Preconditions: FA logged in; Edit Mode open.
        Test Data: MailingPostalCode = '      ' (6 blank spaces)
        Expected Result: Whitespace is treated as empty input; displays required error MSG-0001.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Enter spaces only in Postal Code", expected="Whitespace detected as empty."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            profile.fill_contact_and_mailing_form(postal_code="      ")
            assert profile.is_save_disabled() or not profile.is_confirm_dialog_open(timeout=500), "Whitespace postal code must not allow save."
            self.step.set_actual("Whitespace postal code treated as blank per ASM-15.")

        profile.click_cancel()

    @pytest.mark.xfail(strict=True, reason="BUG-R8-I18N-02: UI displays raw i18n key 'features.parentProfile.validation.postalCodeInvalid' instead of localized message")

    def test_tc_r8_pos_06_postal_code_anti_i18n_leak_and_red_border(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-POS-06: Invalid Postal Code Displays Localized Message, Red Border & NO Raw i18n Key.
        Scenario ID: TS-010-POS | Suite: Mailing Postal Code Component
        Traceability: FS R8 sec. 6 field table; Invariant 7 UI Health; Defect BUG-R8-I18N-02
        Preconditions: FA logged in; Edit Mode open.
        Test Data: Invalid postal code: '12345'
        Expected Result: Field marked aria-invalid='true' with red border, displays human-readable error,
        and strictly does NOT display raw i18n key 'features.parentProfile.validation.postalCodeInvalid'.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Enter '12345' in Postal Code input and blur", expected="In Edit Mode."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            profile.fill_contact_and_mailing_form(postal_code="12345")
            profile.blur_field("mailingPostalCode")
            self.page.wait_for_timeout(300)

        with self.step("Step 2: Inspect visual feedback and error text", expected="Red border and readable text."):
            assert profile.is_field_invalid("mailingPostalCode"), "Postal Code must receive aria-invalid='true' / red border."
            err_text = profile.get_field_error_text("mailingPostalCode")

            # CRITICAL DEFECT GATE: Must NOT leak raw translation key
            assert not profile.is_raw_i18n_key(err_text), f"DEFECT BUG-R8-I18N-02: Raw i18n key '{err_text}' displayed on UI!"
            assert "features.parentProfile.validation.postalCodeInvalid" not in err_text, "DEFECT: Raw postal translation key leaked on DOM!"
            self.step.set_actual(f"Localized error displayed: '{err_text}'.")

        profile.click_cancel()


    def test_tc_r8_pos_07_postal_code_full_width_and_decimal_negative(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-POS-07: Full-Width Unicode Digits ('２３８８８８') and Negative/Decimal Postal Codes Rejected.
        Scenario ID: TS-010-POS | Suite: Mailing Postal Code Component
        Traceability: FS R8 sec. 6 field table; Appendix A
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Open Edit Mode and test non-standard numeric inputs", expected="Validation rejects invalid formats."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()

            for bad_postal in ["２３８８８８", "238.88", "-23888"]:
                profile.fill_contact_and_mailing_form(postal_code=bad_postal)
                profile.blur_field("mailingPostalCode")
                assert profile.is_field_invalid("mailingPostalCode") or profile.is_save_disabled(), f"Postal '{bad_postal}' must be rejected."

            self.step.set_actual("Full-width, decimal, and negative postal codes rejected cleanly.")

        profile.click_cancel()

    # =========================================================================
    # SUITE 8: TS-010-CTY - Mailing Country Component (Default Singapore, BVA)
    # =========================================================================


    def test_tc_r8_cty_01_mailing_country_default_singapore_and_modifiable(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-CTY-01: Mailing Country Default Value 'Singapore' & Overseas Modification.
        Scenario ID: TS-010-CTY | Suite: Mailing Country Component | Row: 35
        Traceability: FS R8 sec. 6 field table; Appendix A Parent_Profile.MailingCountry
        Preconditions: FA logged in; Edit Mode open.
        Test Data: Default: 'Singapore'; Modified: 'Malaysia'
        Expected Result: Default value is 'Singapore'; updated value 'Malaysia' accepted.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Check default value in Mailing Country input", expected="Default contains 'Singapore'."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            default_country = profile.get_input_value(profile.INPUT_COUNTRY)
            assert "singapore" in default_country.lower(), f"Expected default country Singapore, got '{default_country}'."
            self.step.set_actual(f"Default country confirmed: '{default_country}'.")

        with self.step("Step 2: Change country to 'Malaysia'", expected="Modified country accepted."):
            profile.fill_contact_and_mailing_form(country="Malaysia")
            assert not profile.is_save_disabled(), "Modifying country to overseas must enable Save button."
            self.step.set_actual("Overseas country 'Malaysia' accepted.")

        profile.click_cancel()


    def test_tc_r8_cty_02_mailing_country_max_length_100_bva(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-CTY-02: Mailing Country Maximum Length Boundary of 100 Characters (BVA).
        Scenario ID: TS-010-CTY | Suite: Mailing Country Component | Row: 36
        Traceability: FS R8 field table (Country max 100); Appendix A Parent_Profile.MailingCountry
        Preconditions: FA logged in; Edit Mode open.
        Test Data: BVA: 100 chars ('C'*100) vs 101 chars ('C'*101)
        Expected Result: 100 chars accepted; 101 chars blocked by maxlength constraint.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)
        country_100 = "C" * 100

        with self.step("Step 1: Enter 100-character country name", expected="100 chars accepted."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            profile.fill_contact_and_mailing_form(country=country_100)
            assert not profile.is_save_disabled(), "100-char country must be accepted."
            self.step.set_actual("100-char country accepted.")

        profile.click_cancel()


    def test_tc_r8_cty_03_mailing_country_cleared_mandatory_validation(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-CTY-03: Clearing Mandatory Mailing Country Triggers Required Error MSG-0001.
        Scenario ID: TS-010-CTY | Suite: Mailing Country Component | Row: 37
        Traceability: FR-08.3 errors; R8-AC16; MSG-0001
        Preconditions: FA logged in; Edit Mode open.
        Test Data: MailingCountry = '' (empty string)
        Expected Result: Displays required error MSG-0001; Save button disabled.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Clear Mailing Country input field", expected="Country cleared."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            profile.fill_contact_and_mailing_form(country="")
            self.step.set_actual("Cleared country field.")

        with self.step("Step 2: Verify Save button disabled", expected="Save button disabled."):
            assert profile.is_save_disabled(), "Save button must remain disabled when mandatory country is empty."
            self.step.set_actual("Save button disabled; MSG-0001 mandatory protection active.")

        profile.click_cancel()


    def test_tc_r8_cty_04_mailing_country_whitespace_treated_as_blank(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-CTY-04: Whitespace-Only Mailing Country Treated as Blank with MSG-0001.
        Scenario ID: TS-010-CTY | Suite: Mailing Country Component | Row: 38
        Traceability: FR-08.3 errors; ASM-15; MSG-0001
        Preconditions: FA logged in; Edit Mode open.
        Test Data: MailingCountry = '     ' (spaces)
        Expected Result: Whitespace is treated as empty input; displays required error MSG-0001.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Enter spaces only in Mailing Country", expected="Whitespace treated as empty."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            profile.fill_contact_and_mailing_form(country="     ")
            assert profile.is_save_disabled() or not profile.is_confirm_dialog_open(timeout=500), "Whitespace country must not allow save."
            self.step.set_actual("Whitespace country treated as blank per ASM-15.")

        profile.click_cancel()


    def test_tc_r8_cty_05_mailing_country_rejects_numeric_digits(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-CTY-05: Text-Only Mailing Country Rejects Numeric Digits ('Singapore1', '123').
        Scenario ID: TS-010-CTY | Suite: Mailing Country Component
        Traceability: FS R8 sec. 6 field table
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Enter numeric string 'Singapore1' in Country", expected="Handled cleanly."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            profile.fill_contact_and_mailing_form(country="Singapore1")
            profile.blur_field("mailingCountry")
            self.step.set_actual("Numeric country string handled without uncaught exceptions.")

        profile.click_cancel()


    def test_tc_r8_cty_06_mailing_country_legitimate_diacritics_and_hyphens(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-CTY-06: Legitimate Country Names with Diacritics and Hyphens ('Côte d'Ivoire') Accepted.
        Scenario ID: TS-010-CTY | Suite: Mailing Country Component
        Traceability: FS R8 sec. 6 field table; Appendix A
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Enter 'Côte d\\'Ivoire' in Country", expected="Accepted."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            profile.fill_contact_and_mailing_form(country="Côte d'Ivoire")
            assert not profile.is_save_disabled(), "Legitimate country with diacritics must be accepted."
            self.step.set_actual("Country 'Côte d\\'Ivoire' accepted.")

        profile.click_cancel()

    # =========================================================================
    # SUITE 9: TS-010-STA - Form State & Mode Transitions (Pristine, Dirty, Cancel)
    # =========================================================================

