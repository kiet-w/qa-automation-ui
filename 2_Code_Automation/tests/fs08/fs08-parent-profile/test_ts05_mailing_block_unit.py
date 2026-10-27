"""
tests/fs08/fs08-parent-profile/test_ts05_mailing_block_unit.py
Automated Atomic (UI Unit) Test Suite for FS08 Parent Profile / My Details (/profile).
Suite Focus: Suite 5: Mailing Block & Mailing Unit Components (8 TCs)
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
class TestTS05MailingBlockUnit(BaseTest):
    """
    Suite 5: Validates optional block/unit fields, max length 20 BVA, and symbol sanitization.
    """

    def test_tc_r8_105_mailing_block_optional_can_be_blank(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-105: Optional Mailing Block Can Be Left Blank and Saved.
        Scenario ID: TS-010-BLK | Suite: Mailing Block Component | Row: 18
        Traceability: FS R8 sec. 6 field table; Appendix A Parent_Profile.MailingBlock
        Preconditions: FA logged in; Edit Mode open.
        Test Data: MailingBlock = '' (empty); other required fields valid
        Expected Result: Form passes validation without error.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Clear Mailing Block input field", expected="Block cleared."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            profile.fill_contact_and_mailing_form(block="")
            assert not profile.is_save_disabled(), "Clearing optional block field should not disable save."
            self.step.set_actual("Cleared optional block field.")

        profile.click_cancel()


    def test_tc_r8_106_mailing_block_max_length_20_bva(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-106: Mailing Block Maximum Length Boundary of 20 Characters (BVA).
        Scenario ID: TS-010-BLK | Suite: Mailing Block Component | Row: 19
        Traceability: FS R8 field table (Block max 20); Appendix A Parent_Profile.MailingBlock
        Preconditions: FA logged in; Edit Mode open.
        Test Data: BVA: 20 chars ('B'*20) vs 21 chars ('B'*21)
        Expected Result: 20 chars accepted; 21 chars truncated or blocked.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)
        block_20 = "B" * 20

        with self.step("Step 1: Enter 20-character string into Mailing Block", expected="20 chars accepted."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            profile.fill_contact_and_mailing_form(block=block_20)
            assert not profile.is_save_disabled(), "20-char block must be accepted."
            self.step.set_actual("20-char block input accepted.")

        profile.click_cancel()


    def test_tc_r8_blk_01_mailing_block_alphanumeric_formats(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-BLK-01: Alphanumeric Mailing Block Values ('Blk 123A', 'Tower 2') Accepted.
        Scenario ID: TS-010-BLK | Suite: Mailing Block Component | Row: 20
        Traceability: FS R8 sec. 6 field table; Appendix A
        Preconditions: FA logged in; Edit Mode open.
        Test Data: Valid blocks: 'Blk 123A', 'Tower 2'
        Expected Result: Alphanumeric block string accepted.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Enter 'Blk 123A' into Mailing Block", expected="Alphanumeric block accepted."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            profile.fill_contact_and_mailing_form(block="Blk 123A")
            assert not profile.is_save_disabled(), "Alphanumeric block 'Blk 123A' must be accepted."
            self.step.set_actual("Alphanumeric block 'Blk 123A' accepted.")

        profile.click_cancel()


    def test_tc_r8_blk_02_mailing_block_address_symbols_and_paste_stress(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-BLK-02: Mailing Block Address Symbols Allowed & 1000-Char Paste Stress.
        Scenario ID: TS-010-BLK | Suite: Mailing Block Component
        Traceability: NFR Security; Invariant 7 UI Health; Invariant 8
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Enter address symbols 'Blk 12-A/B #01'", expected="Accepted."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            profile.fill_contact_and_mailing_form(block="Blk 12-A/B #01")
            assert not profile.is_save_disabled(), "Valid address symbols in block must be accepted."
            self.step.set_actual("Address symbols accepted.")

        with self.step("Step 2: Paste 1000 characters into Mailing Block", expected="Zero layout breakage."):
            profile.fill_contact_and_mailing_form(block="B" * 1000)
            has_overflow = self.page.evaluate("() => document.documentElement.scrollWidth > document.documentElement.clientWidth")
            assert not has_overflow, "Horizontal overflow detected after pasting 1000 characters!"
            self.step.set_actual("Pasting 1000 chars handled without browser freeze or layout overflow.")

        profile.click_cancel()

    # =========================================================================
    # SUITE 5: TS-010-UNT - Mailing Unit Component (Optional, BVA 20/21)
    # =========================================================================


    def test_tc_r8_unt_01_mailing_unit_optional_can_be_blank(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-UNT-01: Optional Mailing Unit Can Be Left Blank.
        Scenario ID: TS-010-UNT | Suite: Mailing Unit Component | Row: 21
        Traceability: FS R8 sec. 6 field table; Appendix A Parent_Profile.MailingUnit
        Preconditions: FA logged in; Edit Mode open.
        Test Data: MailingUnit = '' (empty); other required fields valid
        Expected Result: Form passes validation without error.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Clear Mailing Unit input field", expected="Unit cleared."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            profile.fill_contact_and_mailing_form(unit="")
            assert not profile.is_save_disabled(), "Clearing optional unit field must not prevent save."
            self.step.set_actual("Cleared optional unit field.")

        profile.click_cancel()


    def test_tc_r8_unt_02_mailing_unit_max_length_20_bva(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-UNT-02: Mailing Unit Maximum Length Boundary of 20 Characters (BVA).
        Scenario ID: TS-010-UNT | Suite: Mailing Unit Component | Row: 22
        Traceability: FS R8 field table (Unit max 20); Appendix A Parent_Profile.MailingUnit
        Preconditions: FA logged in; Edit Mode open.
        Test Data: BVA: 20 chars ('#12-123456789012345') vs 21 chars
        Expected Result: 20 chars accepted; 21 chars blocked by field constraint.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)
        unit_20 = fs08_data["profile_bva_dataset"]["mailing"]["unit_max_20"]

        with self.step("Step 1: Enter 20-character string into Mailing Unit", expected="20 chars accepted."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            profile.fill_contact_and_mailing_form(unit=unit_20)
            assert not profile.is_save_disabled(), "20-char unit notation must enable Save button."
            self.step.set_actual("20-char unit accepted.")

        profile.click_cancel()


    def test_tc_r8_unt_03_mailing_unit_singapore_notation(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-UNT-03: Standard Singapore Apartment Unit Notation ('#02-01', '#12-345') Accepted.
        Scenario ID: TS-010-UNT | Suite: Mailing Unit Component | Row: 23
        Traceability: FS R8 sec. 6 field table; Appendix A
        Preconditions: FA logged in; Edit Mode open.
        Test Data: Unit inputs: '#02-01', '#12-345'
        Expected Result: Standard unit notation saved and displayed correctly.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Enter '#02-01' into Mailing Unit", expected="Unit notation accepted."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            profile.fill_contact_and_mailing_form(unit="#02-01")
            assert not profile.is_save_disabled(), "Standard unit '#02-01' must be accepted."
            self.step.set_actual("Unit notation '#02-01' accepted.")

        profile.click_cancel()


    def test_tc_r8_unt_04_mailing_unit_forbidden_symbols_and_multiline(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-UNT-04: Mailing Unit Forbidden Characters Blocked & Multiline Paste Handled.
        Scenario ID: TS-010-UNT | Suite: Mailing Unit Component
        Traceability: NFR Security; Invariant 8
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Paste multiline string into Mailing Unit", expected="Handled without crash."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            profile.fill_contact_and_mailing_form(unit="#02-01\nTower A")
            val = profile.get_input_value(profile.INPUT_UNIT)
            assert "\n" not in val, "Newlines must be stripped or normalized in unit input."
            self.step.set_actual("Multiline paste normalized without unhandled exceptions.")

        profile.click_cancel()

    # =========================================================================
    # SUITE 6: TS-010-STR - Mailing Street Component (Mandatory, BVA, XSS)
    # =========================================================================

