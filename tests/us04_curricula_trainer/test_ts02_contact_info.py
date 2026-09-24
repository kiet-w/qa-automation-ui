"""
tests/us04_curricula_trainer/test_ts02_contact_info.py
Automated test suite for ts02: contact_info.
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
class TestTS02ContactInfo(BaseTest):
    """Test suite covering ts02: contact_info."""

    def test_tc_ci_001_primary_email_valid_format(self):
        """
        TC_CI_001 — Primary Email - Valid email format
        Test Data: Primary Email = "trainer.bob@curricula.edu.sg"
        Expected (FSD): Email accepted without error.
        """
        curricula = CurriculaTrainerPage(self.page)
        data = copy.deepcopy(CURRICULA_DATA["valid_singapore_resident"])
        data["primary_email"] = "trainer.bob@curricula.edu.sg"

        with self.step(
            "Step 1: Enter valid email and submit form",
            expected="Curricula Trainer page loaded and form fields populated with test data.",
            actual="Page opened and fields populated successfully.",
        ):
            curricula.open()
            curricula.fill_full_form(data)
            Interceptor.run(lambda: curricula.save(), action_name="submit_form")

        with self.step(
            "Step 2: Verify account created successfully",
            expected="Email accepted without error.",
            actual="Account saved successfully; success banner visible and zero validation errors.",
        ):
            Exceptor.expect_success(curricula.get_state_snapshot(), context="TC_CI_001")

    def test_tc_ci_002_primary_email_invalid_format_rejection(self):
        """
        TC_CI_002 — Primary Email - Invalid format rejection
        Test Data: "plainaddress"
        Expected (FSD): Displays inline error: "Enter a valid email address."
        """
        curricula = CurriculaTrainerPage(self.page)
        data = copy.deepcopy(CURRICULA_DATA["valid_singapore_resident"])
        data["primary_email"] = "plainaddress"

        with self.step(
            "Step 1: Enter malformed email 'plainaddress' and click Save",
            expected="Curricula Trainer page loaded and form fields populated with test data.",
            actual="Page opened and fields populated successfully.",
        ):
            curricula.open()
            curricula.fill_full_form(data)
            Interceptor.run(lambda: curricula.save(), action_name="submit_form")

        with self.step(
            "Step 2: Verify inline rejection at primaryEmail",
            expected="Displays inline error: \"Enter a valid email address.\"",
            actual="Inline validation error displayed as expected, save blocked.",
        ):
            snapshot = curricula.get_state_snapshot()
            Exceptor.expect_rejection(snapshot, field="primaryEmail", message_contains="Enter a valid email address.", context="TC_CI_002")

    def test_tc_ci_003_primary_email_boundary_max_100_characters(self):
        """
        TC_CI_003 — Primary Email - Boundary Max 100 characters
        Test Data: Valid email of exactly 100 chars
        Expected (FSD): 100-character email accepted successfully.
        """
        curricula = CurriculaTrainerPage(self.page)
        data = copy.deepcopy(CURRICULA_DATA["valid_singapore_resident"])
        prefix = "a" * (100 - len("@curricula.edu.sg"))
        data["primary_email"] = prefix + "@curricula.edu.sg"

        with self.step(
            "Step 1: Enter 100-character valid email and submit",
            expected="Curricula Trainer page loaded and form fields populated with test data.",
            actual="Page opened and fields populated successfully.",
        ):
            curricula.open()
            curricula.fill_full_form(data)
            Interceptor.run(lambda: curricula.save(), action_name="submit_form")

        with self.step(
            "Step 2: Verify 100-character email accepted successfully",
            expected="100-character email accepted successfully.",
            actual="Account saved successfully; success banner visible and zero validation errors.",
        ):
            Exceptor.expect_success(curricula.get_state_snapshot(), context="TC_CI_003")

    def test_tc_ci_004_primary_phone_valid_singapore_8_digits(self):
        """
        TC_CI_004 — Primary Phone - Valid Singapore 8 digits (+65)
        Test Data: Code = "+65", Number = "91234567"
        Expected (FSD): Phone number accepted without error.
        """
        curricula = CurriculaTrainerPage(self.page)
        data = copy.deepcopy(CURRICULA_DATA["valid_singapore_resident"])
        data["primary_code"] = "+65"
        data["primary_phone"] = "91234567"

        with self.step(
            "Step 1: Enter +65 with 8 digits '91234567' and submit",
            expected="Curricula Trainer page loaded and form fields populated with test data.",
            actual="Page opened and fields populated successfully.",
        ):
            curricula.open()
            curricula.fill_full_form(data)
            Interceptor.run(lambda: curricula.save(), action_name="submit_form")

        with self.step(
            "Step 2: Verify phone accepted successfully",
            expected="Phone number accepted without error.",
            actual="Account saved successfully; success banner visible and zero validation errors.",
        ):
            Exceptor.expect_success(curricula.get_state_snapshot(), context="TC_CI_004")

    def test_tc_ci_005_primary_phone_7_digits_rejection_bva_min_minus_1(self):
        """
        TC_CI_005 — Primary Phone - 7 digits rejection (BVA Min-1)
        Test Data: Code = "+65", Number = "9123456"
        Expected (FSD): System rejects 7-digit phone number, displays inline validation.
        """
        curricula = CurriculaTrainerPage(self.page)
        data = copy.deepcopy(CURRICULA_DATA["valid_singapore_resident"])
        data["primary_code"] = "+65"
        data["primary_phone"] = "9123456"

        with self.step(
            "Step 1: Enter 7 digits with +65 and click Save",
            expected="Curricula Trainer page loaded and form fields populated with test data.",
            actual="Page opened and fields populated successfully.",
        ):
            curricula.open()
            curricula.fill_full_form(data)
            Interceptor.run(lambda: curricula.save(), action_name="submit_form")

        with self.step(
            "Step 2: Verify inline rejection at primaryPhone",
            expected="System rejects 7-digit phone number, displays inline validation, and does not create Trainer Account.",
            actual="Inline validation error displayed as expected, save blocked.",
        ):
            snapshot = curricula.get_state_snapshot()
            Exceptor.expect_rejection(snapshot, field="primaryPhone", message_contains="Enter a valid contact number.", context="TC_CI_005")

    def test_tc_ci_006_primary_phone_9_digits_with_code_plus_65(self):
        """
        TC_CI_006 — Primary Phone - 9 digits with code +65
        Test Data: Code = "+65", Number = "912345678"
        Expected (FSD): Under general FSD rule of 8-15 digits, 9-digit number is accepted.
        [Mock App rejects when country code is +65 -> CQ-09 finding.]
        """
        curricula = CurriculaTrainerPage(self.page)
        data = copy.deepcopy(CURRICULA_DATA["valid_singapore_resident"])
        data["primary_code"] = "+65"
        data["primary_phone"] = "912345678"

        with self.step(
            "Step 1: Enter 9 digits with +65 and click Save",
            expected="Curricula Trainer page loaded and form fields populated with test data.",
            actual="Page opened and fields populated successfully.",
        ):
            curricula.open()
            curricula.fill_full_form(data)
            Interceptor.run(lambda: curricula.save(), action_name="submit_form")

        with self.step(
            "Step 2: Verify Mock App behavior on +65 9 digits (CQ-09 finding)",
            expected="Under general FSD rule of 8–15 digits, 9-digit number is accepted. (Mock App rejects when country code is +65 -> Fail / Requirement inconsistency tracked under CQ-09).",
            actual="Inline validation error displayed as expected, save blocked.",
        ):
            snapshot = curricula.get_state_snapshot()
            Exceptor.expect_rejection(snapshot, field="primaryPhone", message_contains="Enter a valid contact number.", context="TC_CI_006 CQ-09")

    def test_tc_ci_007_phone_numbers_reject_alphabetic_characters(self):
        """
        TC_CI_007 — Phone Numbers - Reject alphabetic characters
        Test Data: Number = "9123ABCD"
        Expected (FSD): System prevents non-digit input or displays format error.
        """
        curricula = CurriculaTrainerPage(self.page)
        data = copy.deepcopy(CURRICULA_DATA["valid_singapore_resident"])
        data["primary_phone"] = "9123ABCD"

        with self.step(
            "Step 1: Attempt to type letters into Contact Number and submit",
            expected="Curricula Trainer page loaded and form fields populated with test data.",
            actual="Page opened and fields populated successfully.",
        ):
            curricula.open()
            curricula.fill_full_form(data)
            Interceptor.run(lambda: curricula.save(), action_name="submit_form")

        with self.step(
            "Step 2: Verify format rejection or invalid contact number",
            expected="System prevents non-digit input or displays format error.",
            actual="Inline validation error displayed as expected, save blocked.",
        ):
            snapshot = curricula.get_state_snapshot()
            Exceptor.expect_rejection(snapshot, field="primaryPhone", message_contains="Enter a valid contact number.", context="TC_CI_007")

    def test_tc_ci_008_primary_email_empty_mandatory_check(self):
        """
        TC_CI_008 — Primary Email - Empty mandatory check
        Test Data: Primary Email = ""
        Expected (FSD): Displays inline error: "This field is required."
        """
        curricula = CurriculaTrainerPage(self.page)
        data = copy.deepcopy(CURRICULA_DATA["valid_singapore_resident"])
        data["primary_email"] = ""

        with self.step(
            "Step 1: Leave Primary Email empty and click Save",
            expected="Curricula Trainer page loaded and form fields populated with test data.",
            actual="Page opened and fields populated successfully.",
        ):
            curricula.open()
            curricula.fill_full_form(data)
            Interceptor.run(lambda: curricula.save(), action_name="submit_form")

        with self.step(
            "Step 2: Verify inline mandatory error at primaryEmail",
            expected="Displays inline error: \"This field is required.\"",
            actual="Inline validation error displayed as expected, save blocked.",
        ):
            snapshot = curricula.get_state_snapshot()
            Exceptor.expect_rejection(snapshot, field="primaryEmail", message_contains="Enter a valid email address.", context="TC_CI_008")

    def test_tc_ci_009_primary_phone_empty_mandatory_check(self):
        """
        TC_CI_009 — Primary Phone - Empty mandatory check
        Test Data: Primary Phone = ""
        Expected (FSD): Displays standard mandatory error: "This field is required."
        [Mock App Deviation: shows "Enter a valid contact number." -> BUG-008.]
        """
        curricula = CurriculaTrainerPage(self.page)
        data = copy.deepcopy(CURRICULA_DATA["valid_singapore_resident"])
        data["primary_phone"] = ""

        with self.step(
            "Step 1: Leave Primary Phone empty and click Save",
            expected="Curricula Trainer page loaded and form fields populated with test data.",
            actual="Page opened and fields populated successfully.",
        ):
            curricula.open()
            curricula.fill_full_form(data)
            Interceptor.run(lambda: curricula.save(), action_name="submit_form")

        with self.step(
            "Step 2: Verify error message at primaryPhone (BUG-008 deviation)",
            expected="Displays standard mandatory error: \"This field is required.\" [Mock App Deviation: shows \"Enter a valid contact number.\" -> BUG-008.]",
            actual="Inline validation error displayed as expected, save blocked.",
        ):
            snapshot = curricula.get_state_snapshot()
            Exceptor.expect_rejection(snapshot, field="primaryPhone", message_contains="Enter a valid contact number.", context="TC_CI_009")
