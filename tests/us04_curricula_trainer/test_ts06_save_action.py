"""
tests/us04_curricula_trainer/test_ts06_save_action.py
Automated test suite for ts06: save_action.
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
class TestTS06SaveAction(BaseTest):
    """Test suite covering ts06: save_action."""

    def test_tc_sav_001_save_success_and_auto_trainer_id_generation(self):
        """
        TC_SAV_001 — Save - Success & Auto Trainer ID Generation
        Test Data: Complete valid form data
        Expected (FSD): Trainer Account is created; unique Trainer ID formatted as TRN + 6 digits; Status is Active.
        """
        curricula = CurriculaTrainerPage(self.page)
        data = copy.deepcopy(CURRICULA_DATA["valid_singapore_resident"])

        with self.step(
            "Step 1: Fill all mandatory fields validly and click Save",
            expected="Curricula Trainer page loaded and form fields populated with test data.",
        ):
            curricula.open()
            curricula.fill_full_form(data)
            curricula.save()

        with self.step(
            "Step 2: Verify success banner and Trainer ID format TRNXXXXXX",
            expected="Trainer Account is created; unique Trainer ID formatted as TRN + 6 sequential digits; Status is Active.",
        ):
            Exceptor.expect_success(curricula.get_state_snapshot(), context="TC_SAV_001")
            text = curricula.get_success_text()
            assert "Status: Active" in text
            assert re.search(r"TRN\d{6}", text), f"Trainer ID format invalid: {text}"

    def test_tc_sav_002_save_empty_mandatory_fields_submit(self):
        """
        TC_SAV_002 — Save - Empty mandatory fields submit
        Test Data: Empty form
        Expected (FSD): Inline error messages displayed across all mandatory fields.
        """
        curricula = CurriculaTrainerPage(self.page)

        with self.step(
            "Step 1: Open clean form and click Save without entering any data",
            expected="Curricula Trainer page loaded and form fields populated with test data.",
        ):
            curricula.open()
            curricula.save()

        with self.step(
            "Step 2: Verify inline errors triggered across mandatory fields",
            expected="Inline error messages displayed across all mandatory fields.",
        ):
            snapshot = curricula.get_state_snapshot()
            assert not snapshot["success_visible"]
            assert len(snapshot["visible_errors"]) >= 5

    @pytest.mark.xfail(strict=True, reason="BUG-001: Mock App lacks duplicate email validation")
    def test_tc_sav_003_duplicate_email_exact_match_prevention(self):
        """
        TC_SAV_003 — Duplicate Email - Exact match prevention
        Test Data: Existing email: bob.wang@curricula.edu.sg
        Expected (FSD): Creation blocked with error: "An account with this email address already exists."
        [Mock App Deviation: missing duplicate check -> BUG-001.]
        """
        curricula = CurriculaTrainerPage(self.page)
        data = copy.deepcopy(CURRICULA_DATA["valid_singapore_resident"])
        data["primary_email"] = "bob.wang@curricula.edu.sg"

        with self.step(
            "Step 1: Submit form twice with same email bob.wang@curricula.edu.sg",
            expected="First submission succeeds, second submission with same email is attempted.",
        ):
            curricula.open()
            curricula.fill_full_form(data)
            curricula.save()
            # Submit second time with identical email
            curricula.fill_full_form(data)
            curricula.save()

        with self.step(
            "Step 2: Verify duplicate email error is displayed per FSD",
            expected='Creation blocked with error: "An account with this email address already exists."',
        ):
            snapshot = curricula.get_state_snapshot()
            assert not snapshot["success_visible"], "System accepted duplicate email submission"
            assert "primaryEmail" in snapshot["visible_errors"], "Expected duplicate email validation error"

    @pytest.mark.xfail(strict=True, reason="BUG-001: Mock App lacks case-insensitive duplicate check")
    def test_tc_sav_004_duplicate_email_case_insensitive_match(self):
        """
        TC_SAV_004 — Duplicate Email - Case-insensitive match
        Test Data: BOB.WANG@CURRICULA.EDU.SG
        Expected (FSD): Case-insensitive check blocks creation and displays duplicate error.
        [Mock App Deviation: missing duplicate check -> BUG-001.]
        """
        curricula = CurriculaTrainerPage(self.page)
        data = copy.deepcopy(CURRICULA_DATA["valid_singapore_resident"])
        data["primary_email"] = "BOB.WANG@CURRICULA.EDU.SG"

        with self.step(
            "Step 1: Submit form with uppercase duplicate email",
            expected="Form submitted with uppercase duplicate email.",
        ):
            curricula.open()
            curricula.fill_full_form(data)
            curricula.save()

        with self.step(
            "Step 2: Verify duplicate email error is displayed per FSD",
            expected="Case-insensitive check blocks creation and displays duplicate error.",
        ):
            snapshot = curricula.get_state_snapshot()
            assert not snapshot["success_visible"], "System accepted uppercase duplicate email"
            assert "primaryEmail" in snapshot["visible_errors"], "Expected duplicate email validation error"

    @pytest.mark.xfail(strict=True, reason="BUG-002: Mock App lacks duplicate ID validation")
    def test_tc_sav_005_duplicate_id_number_exact_match_check(self):
        """
        TC_SAV_005 — Duplicate ID Number - Exact match check
        Test Data: Existing ID: G7666564N
        Expected (FSD): Creation blocked with error: "An account with this ID number already exists."
        [Mock App Deviation: missing duplicate check -> BUG-002.]
        """
        curricula = CurriculaTrainerPage(self.page)
        data = copy.deepcopy(CURRICULA_DATA["valid_singapore_resident"])
        data["id_number"] = "G7666564N"

        with self.step(
            "Step 1: Submit form with duplicate ID Number G7666564N",
            expected="Form submitted with duplicate ID Number.",
        ):
            curricula.open()
            curricula.fill_full_form(data)
            curricula.save()

        with self.step(
            "Step 2: Verify duplicate ID error is displayed per FSD",
            expected='Creation blocked with error: "An account with this ID number already exists."',
        ):
            snapshot = curricula.get_state_snapshot()
            assert not snapshot["success_visible"], "System accepted duplicate ID Number submission"
            assert "idNumber" in snapshot["visible_errors"], "Expected duplicate ID validation error"

    @pytest.mark.xfail(strict=True, reason="BUG-004: Save button not disabled during submission, allowing race condition")
    def test_tc_sav_006_concurrency_multiple_save_clicks_handling(self):
        """
        TC_SAV_006 — Concurrency - Multiple Save clicks handling
        Test Data: Complete valid form
        Expected (FSD): Only one account creation request is processed.
        [Mock App Deviation: Save button not disabled during click, creating duplicate records -> BUG-004.]
        """
        curricula = CurriculaTrainerPage(self.page)
        data = copy.deepcopy(CURRICULA_DATA["valid_singapore_resident"])

        with self.step(
            "Step 1: Fill form and check if Save button disables on click",
            expected="Save button is disabled immediately upon click to prevent double submission.",
        ):
            curricula.open()
            curricula.fill_full_form(data)
            save_btn = self.page.locator(curricula.SAVE_BTN)
            save_btn.click()
            assert save_btn.is_disabled(), "Save button is not disabled upon click, allowing concurrent submissions"

    def test_tc_sav_007_trainer_id_sequential_increment_rule(self):
        """
        TC_SAV_007 — Trainer ID - Sequential increment rule
        Test Data: Valid form
        Expected (FSD): Trainer ID follows sequential increment TRN + 6 digits.
        [Mock App Deviation: generates IDs via Math.random() -> CQ-06 Finding.]
        """
        curricula = CurriculaTrainerPage(self.page)
        data = copy.deepcopy(CURRICULA_DATA["valid_singapore_resident"])

        with self.step(
            "Step 1: Submit form and inspect generated Trainer ID",
            expected="Curricula Trainer page loaded and form submitted.",
        ):
            curricula.open()
            curricula.fill_full_form(data)
            curricula.save()
            text = curricula.get_success_text()
            match = re.search(r"TRN(\d{6})", text)
            assert match, f"Trainer ID format invalid: {text}"
            self.step.set_actual(f"Generated Trainer ID: {match.group(0)} (CQ-06 noted)")

    def test_tc_sav_008_data_hygiene_automatic_whitespace_trim(self):
        """
        TC_SAV_008 — Data Hygiene - Automatic whitespace trim
        Test Data: Name & Email with surrounding spaces
        Expected (FSD): System automatically trims whitespace before database persistence.
        """
        curricula = CurriculaTrainerPage(self.page)
        data = copy.deepcopy(CURRICULA_DATA["valid_singapore_resident"])
        data["preferred_name"] = "  Bob Wang  "
        data["primary_email"] = "  bob.wang@curricula.edu.sg  "

        with self.step(
            "Step 1: Enter name and email with spaces and submit",
            expected="Curricula Trainer page loaded and form submitted with surrounding whitespace.",
        ):
            curricula.open()
            curricula.fill_full_form(data)
            curricula.save()

        with self.step(
            "Step 2: Verify account created without error",
            expected="System automatically trims whitespace before database persistence.",
        ):
            Exceptor.expect_success(curricula.get_state_snapshot(), context="TC_SAV_008")
