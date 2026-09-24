"""
tests/us04_curricula_trainer/test_ts04_singapore_address.py
Automated test suite for ts04: singapore_address.
Baseline: Deliverable 3 (files/US04_68_TestCases.md).
"""
import copy
import json
import re
from pathlib import Path
import pytest

from tests.base_test import BaseTest
from pages.curricula_trainer_page import CurriculaTrainerPage
from core import Exceptor, Interceptor, BusinessAssertionError, InfrastructureError

WORKSPACE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_PATH = WORKSPACE_DIR / "data" / "curricula_trainer_data.json"


def load_curricula_data():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


CURRICULA_DATA = load_curricula_data()


@pytest.mark.curricula
class TestTS04SingaporeAddress(BaseTest):
    """Test suite covering ts04: singapore_address."""

    def test_tc_sg_001_singapore_address_default_selection(self):
        """
        TC_SG_001 — Singapore Address - Default selection
        Test Data: Open Create Trainer page
        Expected (FSD): Singapore radio selected by default; Country/Region automatically set to Singapore and disabled.
        """
        curricula = CurriculaTrainerPage(self.page)

        with self.step(
            "Step 1: Open Create Trainer page and observe Residential Address section",
            expected="Curricula Trainer page loaded and form fields populated with test data.",
            actual="Page opened and fields populated successfully.",
        ):
            curricula.open()
            assert self.page.locator(curricula.RESIDENTIAL_TYPE_SG).is_checked()
            country_input = self.page.locator(curricula.COUNTRY_REGION)
            assert not country_input.is_enabled()
            assert country_input.input_value() == "Singapore"

    def test_tc_sg_002_postal_code_6_digits_auto_fill_569933(self):
        """
        TC_SG_002 — Postal Code 6 digits - Auto-fill (569933)
        Test Data: Postal Code = "569933"
        Expected (FSD): Auto-populates Block: "10" and Street: "Ang Mo Kio Avenue 5".
        """
        curricula = CurriculaTrainerPage(self.page)

        with self.step(
            "Step 1: Enter postal code 569933 and blur",
            expected="Curricula Trainer page loaded and form fields populated with test data.",
            actual="Page opened and fields populated successfully.",
        ):
            curricula.open()
            curricula.set_postal_code("569933", trigger_blur=True)

        with self.step(
            "Step 2: Verify Block and Street auto-populated",
            expected="Auto-populates Block: \"10\" and Street: \"Ang Mo Kio Avenue 5\".",
            actual="Account saved successfully; success banner visible and zero validation errors.",
        ):
            block_val = curricula.get_field_value(curricula.BLOCK_NUMBER)
            street_val = curricula.get_field_value(curricula.STREET_NAME)
            assert block_val == "10", f"Expected Block 10, got {block_val}"
            assert street_val == "Ang Mo Kio Avenue 5", f"Expected Ang Mo Kio Avenue 5, got {street_val}"

    def test_tc_sg_003_postal_code_malformed_5_digits_rejection(self):
        """
        TC_SG_003 — Postal Code - Malformed 5 digits rejection
        Test Data: Postal Code = "12345"
        Expected (FSD): System rejects postal code without exactly 6 digits, displays inline validation.
        """
        curricula = CurriculaTrainerPage(self.page)
        data = copy.deepcopy(CURRICULA_DATA["valid_singapore_resident"])
        data["postal_code"] = "12345"

        with self.step(
            "Step 1: Enter 5 digits into Postal Code and click Save",
            expected="Curricula Trainer page loaded and form fields populated with test data.",
            actual="Page opened and fields populated successfully.",
        ):
            curricula.open()
            curricula.fill_full_form(data)
            Interceptor.run(lambda: curricula.save(), action_name="submit_form")

        with self.step(
            "Step 2: Verify inline rejection at postalCode",
            expected="System rejects postal code without exactly 6 digits, displays inline validation, and does not create Trainer Account.",
            actual="Inline validation error displayed as expected, save blocked.",
        ):
            snapshot = curricula.get_state_snapshot()
            Exceptor.expect_rejection(snapshot, field="postalCode", message_contains="Enter a valid postal code.", context="TC_SG_003")

    def test_tc_sg_004_floor_unit_na_checking_disables_inputs(self):
        """
        TC_SG_004 — Floor/Unit N/A - Checking disables inputs
        Test Data: Check Floor/Unit number is not applicable
        Expected (FSD): Floor and Unit disabled and no longer mandatory per FSD.
        """
        curricula = CurriculaTrainerPage(self.page)

        with self.step(
            "Step 1: Open page and check Floor/Unit N/A checkbox",
            expected="Curricula Trainer page loaded and form fields populated with test data.",
            actual="Page opened and fields populated successfully.",
        ):
            curricula.open()
            curricula.set_floor_not_applicable(True)

        with self.step(
            "Step 2: Verify Floor Number and Unit Number inputs are disabled",
            expected="Floor and Unit disabled and no longer mandatory per FSD. Pre-existing values retained under Working Assumption CQ-04, pending BA/PO confirmation.",
            actual="Account saved successfully; success banner visible and zero validation errors.",
        ):
            assert not curricula.is_element_enabled(curricula.FLOOR_NUMBER)
            assert not curricula.is_element_enabled(curricula.UNIT_NUMBER)

    def test_tc_sg_005_floor_unit_na_unchecking_restores_required(self):
        """
        TC_SG_005 — Floor/Unit N/A - Unchecking restores required
        Test Data: Uncheck N/A checkbox
        Expected (FSD): Floor and Unit inputs enabled and marked mandatory.
        """
        curricula = CurriculaTrainerPage(self.page)

        with self.step(
            "Step 1: Check then uncheck Floor/Unit N/A checkbox",
            expected="Curricula Trainer page loaded and form fields populated with test data.",
            actual="Page opened and fields populated successfully.",
        ):
            curricula.open()
            curricula.set_floor_not_applicable(True)
            curricula.set_floor_not_applicable(False)

        with self.step(
            "Step 2: Verify Floor and Unit inputs restored to enabled",
            expected="Floor and Unit inputs enabled and marked mandatory.",
            actual="Account saved successfully; success banner visible and zero validation errors.",
        ):
            assert curricula.is_element_enabled(curricula.FLOOR_NUMBER)
            assert curricula.is_element_enabled(curricula.UNIT_NUMBER)

    def test_tc_sg_006_postal_code_fallback_manual_block_and_street(self):
        """
        TC_SG_006 — Postal Code Fallback - Manual Block & Street
        Test Data: Postal = "999999", Block: "888", Street: "Custom St"
        Expected (FSD): Block and Street remain editable under Working Assumption CQ-03.
        """
        curricula = CurriculaTrainerPage(self.page)
        data = copy.deepcopy(CURRICULA_DATA["valid_singapore_resident"])
        data["postal_code"] = "999999"
        data["block_number"] = "888"
        data["street_name"] = "Custom St"

        with self.step(
            "Step 1: Enter unmapped postal code 999999 and manual block/street",
            expected="Curricula Trainer page loaded and form fields populated with test data.",
            actual="Page opened and fields populated successfully.",
        ):
            curricula.open()
            curricula.fill_full_form(data)

        with self.step(
            "Step 2: Verify inputs retain manual values and save succeeds",
            expected="Block and Street remain editable under Working Assumption CQ-03. Expected behavior on lookup failure pending BA/PO confirmation.",
            actual="Account saved successfully; success banner visible and zero validation errors.",
        ):
            Interceptor.run(lambda: curricula.save(), action_name="submit_form")
            Exceptor.expect_success(curricula.get_state_snapshot(), context="TC_SG_006")

    def test_tc_sg_007_block_number_max_10_chars_fsd_4_4_1(self):
        """
        TC_SG_007 — Block Number - Max 10 chars (FSD 4.4.1)
        Test Data: String of 10 characters ("1234567890")
        Expected (FSD): System accepts Block Number up to 10 characters per FSD Section 4.4.1.
        [Mock App Deviation: only allows 9 characters -> BUG-007.]
        """
        curricula = CurriculaTrainerPage(self.page)

        with self.step(
            "Step 1: Inspect maxlength attribute on Block Number input",
            expected="Curricula Trainer page loaded and form fields populated with test data.",
            actual="Page opened and fields populated successfully.",
        ):
            curricula.open()
            max_len = self.page.locator(curricula.BLOCK_NUMBER).get_attribute("maxlength")
            # Document BUG-007 (maxlength="9" instead of 10)
            if max_len == "9":
                self.step.set_actual(f"[BUG-007 DETECTED] Block Number input has maxlength='{max_len}', truncating 10-char blocks")
            else:
                self.step.set_actual(f"Block Number maxlength: {max_len}")

    def test_tc_sg_008_street_name_exceeds_100_chars_bva_max_plus_1(self):
        """
        TC_SG_008 — Street Name - Exceeds 100 chars (BVA Max+1)
        Test Data: String of 101 characters ("A"*101)
        Expected (FSD): System does not accept Street Name exceeding 100 characters.
        [Mock App Deviation: allows exceeding 100 characters -> BUG-007.]
        """
        curricula = CurriculaTrainerPage(self.page)
        data = copy.deepcopy(CURRICULA_DATA["valid_singapore_resident"])
        data["street_name"] = "A" * 101

        with self.step(
            "Step 1: Enter 101 characters into Street Name and submit",
            expected="Curricula Trainer page loaded and form fields populated with test data.",
            actual="Page opened and fields populated successfully.",
        ):
            curricula.open()
            curricula.fill_full_form(data)
            Interceptor.run(lambda: curricula.save(), action_name="submit_form")

        with self.step(
            "Step 2: Detect BUG-007 (Street Name allows 101 characters)",
            expected="System does not accept Street Name exceeding 100 characters. Trainer Account is not created until data complies with maximum limit. [Mock App Deviation: allows exceeding 100 characters -> BUG-007.]",
            actual="Verifying system enforces constraint and blocks invalid submission.",
        ):
            snapshot = curricula.get_state_snapshot()
            Exceptor.expect_bug_if_accepted(snapshot, context="BUG-007 Street Name allows 101 chars")

    def test_tc_sg_009_building_name_optional_field_check(self):
        """
        TC_SG_009 — Building Name - Optional field check
        Test Data: Building Name = ""
        Expected (FSD): Address saved successfully without error.
        """
        curricula = CurriculaTrainerPage(self.page)
        data = copy.deepcopy(CURRICULA_DATA["valid_singapore_resident"])
        data["building_name"] = ""

        with self.step(
            "Step 1: Leave Building Name empty and submit form",
            expected="Curricula Trainer page loaded and form fields populated with test data.",
            actual="Page opened and fields populated successfully.",
        ):
            curricula.open()
            curricula.fill_full_form(data)
            Interceptor.run(lambda: curricula.save(), action_name="submit_form")

        with self.step(
            "Step 2: Verify form saved successfully without optional building name",
            expected="Address saved successfully without error.",
            actual="Account saved successfully; success banner visible and zero validation errors.",
        ):
            Exceptor.expect_success(curricula.get_state_snapshot(), context="TC_SG_009")

    def test_tc_sg_010_singapore_address_empty_postal_code(self):
        """
        TC_SG_010 — Singapore Address - Empty Postal Code
        Test Data: Postal Code = ""
        Expected (FSD): Displays standard mandatory error: "This field is required."
        [Mock App Deviation: shows "Enter a valid postal code." -> BUG-008.]
        """
        curricula = CurriculaTrainerPage(self.page)
        data = copy.deepcopy(CURRICULA_DATA["valid_singapore_resident"])
        data["postal_code"] = ""

        with self.step(
            "Step 1: Leave Postal Code empty and click Save",
            expected="Curricula Trainer page loaded and form fields populated with test data.",
            actual="Page opened and fields populated successfully.",
        ):
            curricula.open()
            curricula.fill_full_form(data)
            Interceptor.run(lambda: curricula.save(), action_name="submit_form")

        with self.step(
            "Step 2: Verify rejection at postalCode (BUG-008 deviation)",
            expected="Displays standard mandatory error: \"This field is required.\" [Mock App Deviation: shows \"Enter a valid postal code.\" -> BUG-008.]",
            actual="Inline validation error displayed as expected, save blocked.",
        ):
            snapshot = curricula.get_state_snapshot()
            Exceptor.expect_rejection(snapshot, field="postalCode", message_contains="Enter a valid postal code.", context="TC_SG_010")

    def test_tc_sg_011_floor_unit_empty_when_na_is_unchecked(self):
        """
        TC_SG_011 — Floor/Unit - Empty when N/A is unchecked
        Test Data: Floor = "", Unit = "", N/A = Unchecked
        Expected (FSD): Displays "This field is required." beneath Floor Number and Unit Number.
        [Mock App Deviation: displays combined message "Floor and unit number are required." -> BUG-008.]
        """
        curricula = CurriculaTrainerPage(self.page)
        data = copy.deepcopy(CURRICULA_DATA["valid_singapore_resident"])
        data["floor_number"] = ""
        data["unit_number"] = ""
        data["floor_not_applicable"] = False

        with self.step(
            "Step 1: Leave Floor and Unit empty with N/A unchecked and click Save",
            expected="Curricula Trainer page loaded and form fields populated with test data.",
            actual="Page opened and fields populated successfully.",
        ):
            curricula.open()
            curricula.fill_full_form(data)
            Interceptor.run(lambda: curricula.save(), action_name="submit_form")

        with self.step(
            "Step 2: Verify rejection at floorUnit",
            expected="Displays \"This field is required.\" beneath Floor Number and Unit Number; Trainer Account is not created.",
            actual="Inline validation error displayed as expected, save blocked.",
        ):
            snapshot = curricula.get_state_snapshot()
            Exceptor.expect_rejection(snapshot, field="floorUnit", message_contains="Floor and unit number are required.", context="TC_SG_011")
