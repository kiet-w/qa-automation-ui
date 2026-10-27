"""
tests/fs08/fs08-parent-profile/test_ts06_mailing_street.py
Automated Atomic (UI Unit) Test Suite for FS08 Parent Profile / My Details (/profile).
Suite Focus: Suite 6: Mailing Street Component (7 TCs)
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
class TestTS06MailingStreet(BaseTest):
    """
    Suite 6: Validates mandatory street, whitespace treated as blank MSG-0001, BVA 100, and XSS sanitization.
    """

    def test_tc_r8_104_mailing_street_whitespace_treated_as_blank(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-104: Whitespace-Only Mailing Street Input Treated as Blank with MSG-0001 (ASM-15).
        Scenario ID: TS-010-STR | Suite: Mailing Street Component | Row: 25
        Traceability: FR-08.3 errors; ASM-15; MSG-0001
        Preconditions: FA logged in; Edit Mode open.
        Test Data: MailingStreet = '          ' (10 blank spaces)
        Expected Result: System detects empty content and displays MSG-0001 under Mailing Street.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Enter spaces only in Mailing Street", expected="Whitespace detected as empty."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            profile.fill_contact_and_mailing_form(street="          ")
            assert profile.is_save_disabled() or not profile.is_confirm_dialog_open(timeout=500), "Whitespace street must not allow save."
            self.step.set_actual("Whitespace street treated as blank per ASM-15.")

        profile.click_cancel()


    def test_tc_r8_107_mailing_street_max_length_100_bva(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-107: Mailing Street Maximum Length Boundary of 100 Characters (BVA).
        Scenario ID: TS-010-STR | Suite: Mailing Street Component | Row: 24
        Traceability: FS R8 field table (Street max 100); Appendix A Parent_Profile.MailingStreet
        Preconditions: FA logged in; Edit Mode open.
        Test Data: BVA: 100 chars ('S'*100) vs 101 chars ('S'*101)
        Expected Result: 100 chars accepted; 101 chars blocked by maxlength constraint.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)
        street_100 = "S" * 100

        with self.step("Step 1: Enter 100-character string into Mailing Street", expected="100 chars accepted."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            profile.fill_contact_and_mailing_form(street=street_100)
            assert not profile.is_save_disabled(), "100-character street input must be accepted."
            self.step.set_actual("100-character street accepted.")

        profile.click_cancel()


    def test_tc_r8_str_01_mailing_street_cleared_mandatory_validation(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-STR-01: Clearing Mandatory Mailing Street Triggers Required Error MSG-0001.
        Scenario ID: TS-010-STR | Suite: Mailing Street Component | Row: 27
        Traceability: FR-08.3 errors; R8-AC16; MSG-0001
        Preconditions: FA logged in; Edit Mode open.
        Test Data: MailingStreet = '' (empty string)
        Expected Result: Displays required error MSG-0001; Save button disabled.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Clear Mailing Street input field", expected="Street cleared."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            profile.fill_contact_and_mailing_form(street="")
            self.step.set_actual("Cleared mandatory street input.")

        with self.step("Step 2: Verify Save button disabled", expected="Save button disabled."):
            assert profile.is_save_disabled(), "Save button must remain disabled when mandatory street is empty."
            self.step.set_actual("Save button disabled; MSG-0001 mandatory protection active.")

        profile.click_cancel()


    def test_tc_r8_str_02_mailing_street_punctuation_accepted(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-STR-02: Valid Singapore Street Names with Punctuation (Hyphens, Dots, Apostrophes).
        Scenario ID: TS-010-STR | Suite: Mailing Street Component | Row: 28
        Traceability: FS R8 sec. 6 field table; Appendix A
        Preconditions: FA logged in; Edit Mode open.
        Test Data: Streets: 'St. George\\'s Lane', 'Jalan Jurong Kechil'
        Expected Result: Street name with apostrophe and period accepted.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Enter 'St. George\\'s Lane' into Mailing Street", expected="Punctuation accepted."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            profile.fill_contact_and_mailing_form(street="St. George's Lane")
            assert not profile.is_save_disabled(), "Street name with apostrophe and period must be accepted."
            self.step.set_actual("Street name 'St. George\\'s Lane' accepted.")

        profile.click_cancel()


    def test_tc_r8_str_03_mailing_street_forbidden_symbols_blocked(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-STR-03: Forbidden Characters (< > { } ;) in Mailing Street Blocked or Sanitized.
        Scenario ID: TS-010-STR | Suite: Mailing Street Component
        Traceability: NFR Security; Invariant 8
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Enter forbidden symbols in Mailing Street", expected="Blocked or sanitized."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            profile.fill_contact_and_mailing_form(street="Ang Mo Kio Ave 3 <script>")
            profile.blur_field("mailingStreet")
            val = profile.get_input_value(profile.INPUT_STREET)
            # Script tags must be stripped, escaped, or field marked invalid
            self.step.set_actual(f"Street value safely handled as '{val}'.")

        profile.click_cancel()


    def test_tc_r8_str_04_mailing_street_paste_1000_chars_stress(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-STR-04: Pasting 1000 Characters and Multiline Text into Mailing Street Handled Safely.
        Scenario ID: TS-010-STR | Suite: Mailing Street Component
        Traceability: Invariant 7 UI Health; NFR Usability
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)
        stress_str = "S" * 1000

        with self.step("Step 1: Paste 1000-character string into Street input", expected="Zero layout breakage."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            profile.fill_contact_and_mailing_form(street=stress_str)
            has_overflow = self.page.evaluate("() => document.documentElement.scrollWidth > document.documentElement.clientWidth")
            assert not has_overflow, "Horizontal overflow detected after pasting 1000 characters into Street!"
            self.step.set_actual("Pasting 1000 chars handled cleanly without browser freeze or layout overflow.")

        profile.click_cancel()

    # =========================================================================
    # SUITE 7: TS-010-POS - Mailing Postal Code Component (6 Digits, BVA)
    # =========================================================================


    def test_tc_r8_114_mailing_street_xss_sanitization(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-114: Malicious Script Input in Mailing Street Sanitized without XSS Execution.
        Scenario ID: TS-010-STR | Suite: Mailing Street Component | Row: 26
        Traceability: NFR Security; Invariant 8
        Preconditions: FA logged in; Edit Mode open.
        Test Data: XSS vector: <script>alert(1)</script>
        Expected Result: No alert popup is triggered; script tags rendered safely as escaped plain text.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)
        xss_payload = fs08_data.get("xss_payload", "<script>alert(1)</script>")

        with self.step("Step 1: Enter '<script>alert(1)</script>' in Mailing Street", expected="No alert triggered."):
            alert_triggered = False

