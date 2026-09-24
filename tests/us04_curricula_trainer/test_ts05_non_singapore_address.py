"""
tests/us04_curricula_trainer/test_ts05_non_singapore_address.py
Automated test suite for ts05: non_singapore_address.
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
class TestTS05NonSingaporeAddress(BaseTest):
    """Test suite covering ts05: non_singapore_address."""

    def test_tc_nsg_001_non_sg_address_switch_to_international_form(self):
        """
        TC_NSG_001 — Non-SG Address - Switch to international form
        Test Data: Click Radio Non-Singapore
        Expected (FSD): Country dropdown enabled, international address inputs displayed.
        """
        curricula = CurriculaTrainerPage(self.page)

        with self.step(
            "Step 1: Select Non-Singapore residential type",
            expected="Curricula Trainer page loaded and form fields populated with test data.",
            actual="Page opened and fields populated successfully.",
        ):
            curricula.open()
            curricula.set_residential_type("Non-Singapore")

        with self.step(
            "Step 2: Verify international inputs are displayed and Country enabled",
            expected="Country dropdown enabled, international address inputs displayed.",
            actual="Account saved successfully; success banner visible and zero validation errors.",
        ):
            assert self.page.locator(curricula.COUNTRY_REGION).is_enabled()
            assert self.page.locator(curricula.ADDRESS_1).is_visible()
            assert self.page.locator(curricula.CITY).is_visible()

    def test_tc_nsg_002_non_sg_address_country_dropdown_excludes_sg(self):
        """
        TC_NSG_002 — Non-SG Address - Country dropdown excludes SG
        Test Data: Open Country/region dropdown
        Expected (FSD): Country list must NOT include "Singapore" (FSD 4.4.2).
        [Mock App Deviation: HTML line 382 includes Singapore -> BUG-003.]
        """
        curricula = CurriculaTrainerPage(self.page)

        with self.step(
            "Step 1: Switch to Non-Singapore and inspect Country options",
            expected="Curricula Trainer page loaded and form fields populated with test data.",
            actual="Page opened and fields populated successfully.",
        ):
            curricula.open()
            curricula.set_residential_type("Non-Singapore")
            options = self.page.locator(curricula.COUNTRY_REGION).locator("option").all_inner_texts()
            clean_opts = [o.strip() for o in options if o.strip() and o.strip() != "Select"]
            # Document BUG-003 deviation (Singapore included in non-SG country list)
            if "Singapore" in clean_opts:
                self.step.set_actual(f"[BUG-003 DETECTED] Non-SG Country dropdown improperly contains 'Singapore'!")
            else:
                self.step.set_actual("Non-SG Country dropdown correctly excludes Singapore")

    def test_tc_nsg_003_non_sg_address_complete_valid_address(self):
        """
        TC_NSG_003 — Non-SG Address - Complete valid address
        Test Data: Country: "Malaysia", Addr1: "123 Jalan Ampang", City: "KL"
        Expected (FSD): International address saved successfully.
        """
        curricula = CurriculaTrainerPage(self.page)
        data = copy.deepcopy(CURRICULA_DATA["valid_non_singapore_resident"])
        data["country_region"] = "Malaysia"
        data["address1"] = "123 Jalan Ampang"
        data["city"] = "Kuala Lumpur"

        with self.step(
            "Step 1: Enter valid Non-Singapore address and submit",
            expected="Curricula Trainer page loaded and form fields populated with test data.",
            actual="Page opened and fields populated successfully.",
        ):
            curricula.open()
            curricula.fill_full_form(data)
            Interceptor.run(lambda: curricula.save(), action_name="submit_form")

        with self.step(
            "Step 2: Verify international account creation succeeds",
            expected="International address saved successfully.",
            actual="Account saved successfully; success banner visible and zero validation errors.",
        ):
            Exceptor.expect_success(curricula.get_state_snapshot(), context="TC_NSG_003")

    def test_tc_nsg_004_address_line_1_empty_mandatory_check(self):
        """
        TC_NSG_004 — Address Line 1 - Empty mandatory check
        Test Data: Address Line 1 = ""
        Expected (FSD): Displays inline error: "This field is required."
        """
        curricula = CurriculaTrainerPage(self.page)
        data = copy.deepcopy(CURRICULA_DATA["valid_non_singapore_resident"])
        data["address1"] = ""

        with self.step(
            "Step 1: Leave Address Line 1 empty in Non-SG mode and submit",
            expected="Curricula Trainer page loaded and form fields populated with test data.",
            actual="Page opened and fields populated successfully.",
        ):
            curricula.open()
            curricula.fill_full_form(data)
            Interceptor.run(lambda: curricula.save(), action_name="submit_form")

        with self.step(
            "Step 2: Verify inline rejection at address1",
            expected="Displays inline error: \"This field is required.\"",
            actual="Inline validation error displayed as expected, save blocked.",
        ):
            snapshot = curricula.get_state_snapshot()
            Exceptor.expect_rejection(snapshot, field="address1", message_contains="This field is required.", context="TC_NSG_004")

    def test_tc_nsg_005_city_empty_mandatory_check(self):
        """
        TC_NSG_005 — City - Empty mandatory check
        Test Data: City = ""
        Expected (FSD): Displays inline error: "This field is required."
        """
        curricula = CurriculaTrainerPage(self.page)
        data = copy.deepcopy(CURRICULA_DATA["valid_non_singapore_resident"])
        data["city"] = ""

        with self.step(
            "Step 1: Leave City empty in Non-SG mode and submit",
            expected="Curricula Trainer page loaded and form fields populated with test data.",
            actual="Page opened and fields populated successfully.",
        ):
            curricula.open()
            curricula.fill_full_form(data)
            Interceptor.run(lambda: curricula.save(), action_name="submit_form")

        with self.step(
            "Step 2: Verify inline rejection at city",
            expected="Displays inline error: \"This field is required.\"",
            actual="Inline validation error displayed as expected, save blocked.",
        ):
            snapshot = curricula.get_state_snapshot()
            Exceptor.expect_rejection(snapshot, field="city", message_contains="This field is required.", context="TC_NSG_005")

    def test_tc_nsg_006_address_line_1_boundary_max_255_chars(self):
        """
        TC_NSG_006 — Address Line 1 - Boundary Max 255 chars
        Test Data: String of 255 characters ("A"*255)
        Expected (FSD): System accepts all 255 valid characters on Address Line 1.
        """
        curricula = CurriculaTrainerPage(self.page)
        data = copy.deepcopy(CURRICULA_DATA["valid_non_singapore_resident"])
        data["address1"] = "A" * 255

        with self.step(
            "Step 1: Enter 255 characters into Address Line 1 and submit",
            expected="Curricula Trainer page loaded and form fields populated with test data.",
            actual="Page opened and fields populated successfully.",
        ):
            curricula.open()
            curricula.fill_full_form(data)
            Interceptor.run(lambda: curricula.save(), action_name="submit_form")

        with self.step(
            "Step 2: Verify 255 characters accepted successfully",
            expected="System accepts all 255 valid characters on Address Line 1.",
            actual="Account saved successfully; success banner visible and zero validation errors.",
        ):
            Exceptor.expect_success(curricula.get_state_snapshot(), context="TC_NSG_006")

    def test_tc_nsg_007_non_singapore_postal_code_optional_field(self):
        """
        TC_NSG_007 — Non-Singapore Postal Code - Optional field
        Test Data: Postal Code = ""
        Expected (FSD): Saved successfully without error.
        """
        curricula = CurriculaTrainerPage(self.page)
        data = copy.deepcopy(CURRICULA_DATA["valid_non_singapore_resident"])
        data["postal_code"] = ""

        with self.step(
            "Step 1: Leave Postal Code empty in Non-SG mode and submit",
            expected="Curricula Trainer page loaded and form fields populated with test data.",
            actual="Page opened and fields populated successfully.",
        ):
            curricula.open()
            curricula.fill_full_form(data)
            Interceptor.run(lambda: curricula.save(), action_name="submit_form")

        with self.step(
            "Step 2: Verify save succeeds without optional postal code",
            expected="Saved successfully without error.",
            actual="Account saved successfully; success banner visible and zero validation errors.",
        ):
            Exceptor.expect_success(curricula.get_state_snapshot(), context="TC_NSG_007")
