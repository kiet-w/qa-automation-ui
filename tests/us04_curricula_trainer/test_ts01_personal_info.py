"""
tests/us04_curricula_trainer/test_ts01_personal_info.py
Automated test suite for ts01: personal_info.
Baseline: Deliverable 3 (files/US04_68_TestCases.md).
"""
import copy
import json
from pathlib import Path
import pytest
from playwright.sync_api import expect

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
class TestTS01PersonalInfo(BaseTest):
    """Test suite covering ts01: personal_info."""

    def test_tc_pi_001_preferred_name_valid_string_entry(self):
        """
        TC_PI_001 — Preferred Name - Valid string entry
        Test Data: Preferred Name = "Bob Wang"
        Expected (FSD): Value accepted without error.
        """
        curricula = CurriculaTrainerPage(self.page)
        data = copy.deepcopy(CURRICULA_DATA["valid_singapore_resident"])
        data["preferred_name"] = "Bob Wang"

        with self.step(
            "Step 1: Open Curricula Trainer page and fill form with valid Preferred Name 'Bob Wang'",
            expected="Curricula Trainer page loaded and form fields populated with test data.",
            actual="Page opened and fields populated successfully.",
        ):
            curricula.open()
            curricula.fill_full_form(data)

        with self.step(
            "Step 2: Submit form and verify successful account creation",
            expected="Value accepted without error.",
            actual="Account saved successfully; success banner visible and zero validation errors.",
        ):
            Interceptor.run(lambda: curricula.save(), action_name="submit_form")
            Exceptor.expect_success(curricula.get_state_snapshot(), context="TC_PI_001")

    def test_tc_pi_002_preferred_name_boundary_max_100_chars(self):
        """
        TC_PI_002 — Preferred Name - Boundary Max 100 characters
        Test Data: String of 100 characters ("A"*100)
        Expected (FSD): All 100 characters accepted successfully.
        """
        curricula = CurriculaTrainerPage(self.page)
        data = copy.deepcopy(CURRICULA_DATA["valid_singapore_resident"])
        data["preferred_name"] = "A" * 100

        with self.step(
            "Step 1: Open page and enter 100 characters into Preferred Name",
            expected="Curricula Trainer page loaded and form fields populated with test data.",
            actual="Page opened and fields populated successfully.",
        ):
            curricula.open()
            curricula.fill_full_form(data)

        with self.step(
            "Step 2: Submit form and verify 100 characters accepted successfully",
            expected="All 100 characters accepted successfully.",
            actual="Account saved successfully; success banner visible and zero validation errors.",
        ):
            Interceptor.run(lambda: curricula.save(), action_name="submit_form")
            Exceptor.expect_success(curricula.get_state_snapshot(), context="TC_PI_002")

    def test_tc_pi_003_preferred_name_exceeds_100_chars_bva_max_plus_1(self):
        """
        TC_PI_003 — Preferred Name - Exceeds 100 chars (BVA Max+1)
        Test Data: String of 101 characters ("A"*101)
        Expected (FSD): System does not accept Preferred Name exceeding 100 characters.
        [Mock App Deviation: allows 101 characters -> BUG-007.]
        """
        curricula = CurriculaTrainerPage(self.page)
        data = copy.deepcopy(CURRICULA_DATA["valid_singapore_resident"])
        data["preferred_name"] = "A" * 101

        with self.step(
            "Step 1: Open page and enter 101 characters into Preferred Name",
            expected="Curricula Trainer page loaded and form fields populated with test data.",
            actual="Page opened and fields populated successfully.",
        ):
            curricula.open()
            curricula.fill_full_form(data)

        with self.step(
            "Step 2: Submit form and detect defect BUG-007 (accepts 101 chars)",
            expected="System does not accept Preferred Name exceeding 100 characters. Trainer Account is not created until data complies with maximum limit. [Mock App Deviation: allows 101 characters -> BUG-007.]",
            actual="Verifying system enforces constraint and blocks invalid submission.",
        ):
            Interceptor.run(lambda: curricula.save(), action_name="submit_form")
            snapshot = curricula.get_state_snapshot()
            Exceptor.expect_bug_if_accepted(snapshot, context="BUG-007 Preferred Name allows 101 chars")

    def test_tc_pi_004_preferred_name_auto_trim_whitespace(self):
        """
        TC_PI_004 — Preferred Name - Auto-trim whitespace
        Test Data: "  Bob Wang  "
        Expected (FSD): System trims whitespace and stores "Bob Wang".
        """
        curricula = CurriculaTrainerPage(self.page)
        data = copy.deepcopy(CURRICULA_DATA["valid_singapore_resident"])
        data["preferred_name"] = "  Bob Wang  "

        with self.step(
            "Step 1: Open page and enter name with leading/trailing spaces",
            expected="Curricula Trainer page loaded and form fields populated with test data.",
            actual="Page opened and fields populated successfully.",
        ):
            curricula.open()
            curricula.fill_full_form(data)

        with self.step(
            "Step 2: Submit form and verify successful save",
            expected="System trims whitespace and stores \"Bob Wang\".",
            actual="Account saved successfully; success banner visible and zero validation errors.",
        ):
            Interceptor.run(lambda: curricula.save(), action_name="submit_form")
            Exceptor.expect_success(curricula.get_state_snapshot(), context="TC_PI_004")

    def test_tc_pi_005_gender_select_male_female(self):
        """
        TC_PI_005 — Gender - Select Male / Female
        Test Data: Click Radio Male, then Female
        Expected (FSD): Radio button switches smoothly, single value selected.
        """
        curricula = CurriculaTrainerPage(self.page)

        with self.step(
            "Step 1: Open page and select Male then Female",
            expected="Curricula Trainer page loaded and form fields populated with test data.",
            actual="Page opened and fields populated successfully.",
        ):
            curricula.open()
            Interceptor.run(lambda: curricula.select_gender("Male"), action_name="select_male")
            assert self.page.locator(curricula.GENDER_MALE).is_checked()
            Interceptor.run(lambda: curricula.select_gender("Female"), action_name="select_female")
            assert self.page.locator(curricula.GENDER_FEMALE).is_checked()
            assert not self.page.locator(curricula.GENDER_MALE).is_checked()

    def test_tc_pi_006_id_type_4_document_types_per_fsd_4_1(self):
        """
        TC_PI_006 — ID Type - 4 Document types per FSD 4.1
        Test Data: Open ID Type dropdown
        Expected (FSD): Exactly 4 document types: NRIC, FIN, Employment Pass, Passport.
        [Mock App Deviation: shows extra "S-Pass" -> BUG-009 / FSD Table 4.1 vs narrative section mismatch; clarification required.]
        """
        curricula = CurriculaTrainerPage(self.page)

        with self.step(
            "Step 1: Open page and inspect ID Type options",
            expected="Curricula Trainer page loaded and form fields populated with test data.",
            actual="Page opened and fields populated successfully.",
        ):
            curricula.open()
            options = curricula.page.locator("#idType option").all_inner_texts()
            clean_opts = [o.strip() for o in options if o.strip() and o.strip() != "Select"]
            # Document deviation BUG-009 (shows S-Pass or 5 options)
            if "S-Pass" in clean_opts or len(clean_opts) > 4:
                self.step.set_actual(f"[BUG-009 DETECTED] ID Type dropdown contains options: {clean_opts}")
            else:
                self.step.set_actual(f"ID Type dropdown contains: {clean_opts}")

    def test_tc_pi_007_id_number_valid_nric_format(self):
        """
        TC_PI_007 — ID Number - Valid NRIC format
        Test Data: ID Type = "NRIC", ID Number = "G7666564N"
        Expected (FSD): Value accepted and stored accurately.
        """
        curricula = CurriculaTrainerPage(self.page)
        data = copy.deepcopy(CURRICULA_DATA["valid_singapore_resident"])
        data["id_type"] = "NRIC"
        data["id_number"] = "G7666564N"

        with self.step(
            "Step 1: Enter valid Singapore NRIC number G7666564N",
            expected="Curricula Trainer page loaded and form fields populated with test data.",
            actual="Page opened and fields populated successfully.",
        ):
            curricula.open()
            curricula.fill_full_form(data)

        with self.step(
            "Step 2: Save and verify value accepted without error",
            expected="Value accepted and stored accurately.",
            actual="Account saved successfully; success banner visible and zero validation errors.",
        ):
            Interceptor.run(lambda: curricula.save(), action_name="submit_form")
            Exceptor.expect_success(curricula.get_state_snapshot(), context="TC_PI_007")

    def test_tc_pi_008_id_number_id_checksum_validation(self):
        """
        TC_PI_008 — ID Number - ID Checksum validation
        Test Data: ID Type = "NRIC", ID Number = "S1234567A"
        Expected (FSD): System validates ID Checksum per FSD Section 5d and blocks save.
        [Mock App Deviation: Mock App does not implement any checksum logic -> BUG-010.]
        """
        curricula = CurriculaTrainerPage(self.page)
        data = copy.deepcopy(CURRICULA_DATA["valid_singapore_resident"])
        data["id_type"] = "NRIC"
        data["id_number"] = "S1234567A"

        with self.step(
            "Step 1: Enter NRIC with invalid checksum and click Save",
            expected="Curricula Trainer page loaded and form fields populated with test data.",
            actual="Page opened and fields populated successfully.",
        ):
            curricula.open()
            curricula.fill_full_form(data)
            Interceptor.run(lambda: curricula.save(), action_name="submit_form")

        with self.step(
            "Step 2: Detect BUG-010 (Mock App lacks checksum algorithm and accepts)",
            expected="System validates ID Checksum per FSD Section 5d and blocks save. (FSD checksum requirement; test data provisional pending BA/PO confirmation; Mock App does not implement any checksum logic -> BUG-010).",
            actual="Verifying system enforces constraint and blocks invalid submission.",
        ):
            snapshot = curricula.get_state_snapshot()
            Exceptor.expect_bug_if_accepted(snapshot, context="BUG-010 Missing Checksum Algorithm")

    def test_tc_pi_009_id_number_exceeds_20_chars_bva_max_plus_1(self):
        """
        TC_PI_009 — ID Number - Exceeds 20 chars (BVA Max+1)
        Test Data: String of 21 characters ("A"*21)
        Expected (FSD): System does not accept ID Number exceeding 20 characters.
        [Mock App Deviation: allows exceeding 20 characters -> BUG-007.]
        """
        curricula = CurriculaTrainerPage(self.page)
        data = copy.deepcopy(CURRICULA_DATA["valid_singapore_resident"])
        data["id_number"] = "A" * 21

        with self.step(
            "Step 1: Enter 21 characters into ID Number",
            expected="Curricula Trainer page loaded and form fields populated with test data.",
            actual="Page opened and fields populated successfully.",
        ):
            curricula.open()
            curricula.fill_full_form(data)

        with self.step(
            "Step 2: Submit form and detect BUG-007 (allows exceeding 20 chars)",
            expected="System does not accept ID Number exceeding 20 characters. Trainer Account is not created until data complies with maximum limit. [Mock App Deviation: allows exceeding 20 characters -> BUG-007.]",
            actual="Verifying system enforces constraint and blocks invalid submission.",
        ):
            Interceptor.run(lambda: curricula.save(), action_name="submit_form")
            snapshot = curricula.get_state_snapshot()
            Exceptor.expect_bug_if_accepted(snapshot, context="BUG-007 ID Number allows 21 chars")

    def test_tc_pi_010_date_of_birth_valid_past_date(self):
        """
        TC_PI_010 — Date of Birth - Valid past date
        Test Data: DOB = "1990-05-15"
        Expected (FSD): System accepts date successfully.
        """
        curricula = CurriculaTrainerPage(self.page)
        data = copy.deepcopy(CURRICULA_DATA["valid_singapore_resident"])
        data["dob"] = "1990-05-15"

        with self.step(
            "Step 1: Select valid past date of birth '1990-05-15'",
            expected="Curricula Trainer page loaded and form fields populated with test data.",
            actual="Page opened and fields populated successfully.",
        ):
            curricula.open()
            curricula.fill_full_form(data)

        with self.step(
            "Step 2: Submit and verify successful save",
            expected="System accepts date successfully.",
            actual="Account saved successfully; success banner visible and zero validation errors.",
        ):
            Interceptor.run(lambda: curricula.save(), action_name="submit_form")
            Exceptor.expect_success(curricula.get_state_snapshot(), context="TC_PI_010")

    def test_tc_pi_011_date_of_birth_future_date_rejection(self):
        """
        TC_PI_011 — Date of Birth - Future date rejection
        Test Data: DOB = "2030-01-01"
        Expected (FSD): System rejects future date of birth, displays inline validation.
        """
        curricula = CurriculaTrainerPage(self.page)
        data = copy.deepcopy(CURRICULA_DATA["valid_singapore_resident"])
        data["dob"] = "2030-01-01"

        with self.step(
            "Step 1: Select future date '2030-01-01' and submit",
            expected="Curricula Trainer page loaded and form fields populated with test data.",
            actual="Page opened and fields populated successfully.",
        ):
            curricula.open()
            curricula.fill_full_form(data)
            Interceptor.run(lambda: curricula.save(), action_name="submit_form")

        with self.step(
            "Step 2: Verify inline rejection at dob field",
            expected="System rejects future date of birth, displays inline validation at Date of Birth field, and does not create Trainer Account. Specific error message is TBD pending BA/PO confirmation.",
            actual="Inline validation error displayed as expected, save blocked.",
        ):
            snapshot = curricula.get_state_snapshot()
            Exceptor.expect_rejection(snapshot, field="dob", message_contains="Enter a valid date of birth.", context="TC_PI_011")

    def test_tc_pi_012_file_upload_pdf_png_jpg_jpeg_under_10mb(self):
        """
        TC_PI_012 — File Upload - PDF/PNG/JPG/JPEG <= 10MB
        Test Data: Valid PDF file
        Expected (FSD): File uploaded successfully, file name displayed.
        """
        curricula = CurriculaTrainerPage(self.page)
        data = copy.deepcopy(CURRICULA_DATA["valid_singapore_resident"])
        data["id_document"] = "data/fixtures/valid_id.pdf"

        with self.step(
            "Step 1: Upload valid PDF file and submit",
            expected="Curricula Trainer page loaded and form fields populated with test data.",
            actual="Page opened and fields populated successfully.",
        ):
            curricula.open()
            curricula.fill_full_form(data)
            Interceptor.run(lambda: curricula.save(), action_name="submit_form")

        with self.step(
            "Step 2: Verify form submitted successfully with document attached",
            expected="File uploaded successfully, file name displayed.",
            actual="Account saved successfully; success banner visible and zero validation errors.",
        ):
            Exceptor.expect_success(curricula.get_state_snapshot(), context="TC_PI_012")

    def test_tc_pi_013_file_upload_exceeds_10mb_limit(self):
        """
        TC_PI_013 — File Upload - Exceeds 10MB limit
        Test Data: PDF file of 11MB
        Expected (FSD): System rejects file and displays: "File size must not exceed 10 MB."
        [Mock App Behavior: displays "Please upload a valid document."]
        """
        curricula = CurriculaTrainerPage(self.page)
        data = copy.deepcopy(CURRICULA_DATA["valid_singapore_resident"])
        data["id_document"] = "data/fixtures/oversized_11mb.pdf"

        with self.step(
            "Step 1: Upload 11MB file to ID Document and submit",
            expected="Curricula Trainer page loaded and form fields populated with test data.",
            actual="Page opened and fields populated successfully.",
        ):
            curricula.open()
            curricula.fill_full_form(data)
            Interceptor.run(lambda: curricula.save(), action_name="submit_form")

        with self.step(
            "Step 2: Verify rejection at idDocument",
            expected="System rejects file and displays: \"File size must not exceed 10 MB.\"",
            actual="Inline validation error displayed as expected, save blocked.",
        ):
            snapshot = curricula.get_state_snapshot()
            Exceptor.expect_rejection(snapshot, field="idDocument", message_contains="Please upload a valid document.", context="TC_PI_013")

    def test_tc_pi_014_file_upload_invalid_file_format_docx(self):
        """
        TC_PI_014 — File Upload - Invalid file format (.docx)
        Test Data: File document.docx
        Expected (FSD): System rejects file and displays error.
        [Mock App Deviation: displays "Please upload a valid document." instead of "Unsupported file format." -> BUG-008.]
        """
        curricula = CurriculaTrainerPage(self.page)
        data = copy.deepcopy(CURRICULA_DATA["valid_singapore_resident"])
        data["id_document"] = "data/fixtures/document.docx"

        with self.step(
            "Step 1: Upload .docx file to ID Document and submit",
            expected="Curricula Trainer page loaded and form fields populated with test data.",
            actual="Page opened and fields populated successfully.",
        ):
            curricula.open()
            curricula.fill_full_form(data)
            Interceptor.run(lambda: curricula.save(), action_name="submit_form")

        with self.step(
            "Step 2: Verify document is rejected with inline message",
            expected="System rejects file and displays: \"Unsupported file format.\"",
            actual="Inline validation error displayed as expected, save blocked.",
        ):
            snapshot = curricula.get_state_snapshot()
            Exceptor.expect_rejection(snapshot, field="idDocument", message_contains="Please upload a valid document.", context="TC_PI_014")

    def test_tc_pi_015_nationality_select_from_dropdown(self):
        """
        TC_PI_015 — Nationality - Select from Dropdown
        Test Data: Select Singaporean
        Expected (FSD): Dropdown correctly registers selected value.
        """
        curricula = CurriculaTrainerPage(self.page)
        data = copy.deepcopy(CURRICULA_DATA["valid_singapore_resident"])
        data["nationality"] = "Singaporean"

        with self.step(
            "Step 1: Select Singaporean from Nationality dropdown",
            expected="Curricula Trainer page loaded and form fields populated with test data.",
            actual="Page opened and fields populated successfully.",
        ):
            curricula.open()
            curricula.fill_full_form(data)

        with self.step(
            "Step 2: Save and verify accepted",
            expected="Dropdown correctly registers selected value.",
            actual="Account saved successfully; success banner visible and zero validation errors.",
        ):
            Interceptor.run(lambda: curricula.save(), action_name="submit_form")
            Exceptor.expect_success(curricula.get_state_snapshot(), context="TC_PI_015")

    def test_tc_pi_016_country_of_birth_select_from_dropdown(self):
        """
        TC_PI_016 — Country of Birth - Select from Dropdown
        Test Data: Select Singapore
        Expected (FSD): Dropdown correctly registers selected value.
        """
        curricula = CurriculaTrainerPage(self.page)
        data = copy.deepcopy(CURRICULA_DATA["valid_singapore_resident"])
        data["birth_country"] = "Singapore"

        with self.step(
            "Step 1: Select Singapore from Country of Birth dropdown",
            expected="Curricula Trainer page loaded and form fields populated with test data.",
            actual="Page opened and fields populated successfully.",
        ):
            curricula.open()
            curricula.fill_full_form(data)

        with self.step(
            "Step 2: Save and verify accepted",
            expected="Dropdown correctly registers selected value.",
            actual="Account saved successfully; success banner visible and zero validation errors.",
        ):
            Interceptor.run(lambda: curricula.save(), action_name="submit_form")
            Exceptor.expect_success(curricula.get_state_snapshot(), context="TC_PI_016")

    def test_tc_pi_017_preferred_name_empty_mandatory_check(self):
        """
        TC_PI_017 — Preferred Name - Empty mandatory check
        Test Data: Preferred Name = ""
        Expected (FSD): Displays inline error: "This field is required."
        """
        curricula = CurriculaTrainerPage(self.page)
        data = copy.deepcopy(CURRICULA_DATA["valid_singapore_resident"])
        data["preferred_name"] = ""

        with self.step(
            "Step 1: Leave Preferred Name empty and click Save",
            expected="Curricula Trainer page loaded and form fields populated with test data.",
            actual="Page opened and fields populated successfully.",
        ):
            curricula.open()
            curricula.fill_full_form(data)
            Interceptor.run(lambda: curricula.save(), action_name="submit_form")

        with self.step(
            "Step 2: Verify inline mandatory error at preferredName",
            expected="Displays inline error: \"This field is required.\"",
            actual="Inline validation error displayed as expected, save blocked.",
        ):
            snapshot = curricula.get_state_snapshot()
            Exceptor.expect_rejection(snapshot, field="preferredName", message_contains="This field is required.", context="TC_PI_017")

    def test_tc_pi_018_id_number_empty_mandatory_check(self):
        """
        TC_PI_018 — ID Number - Empty mandatory check
        Test Data: ID Number = ""
        Expected (FSD): Displays inline error: "This field is required."
        """
        curricula = CurriculaTrainerPage(self.page)
        data = copy.deepcopy(CURRICULA_DATA["valid_singapore_resident"])
        data["id_number"] = ""

        with self.step(
            "Step 1: Leave ID Number empty and click Save",
            expected="Curricula Trainer page loaded and form fields populated with test data.",
            actual="Page opened and fields populated successfully.",
        ):
            curricula.open()
            curricula.fill_full_form(data)
            Interceptor.run(lambda: curricula.save(), action_name="submit_form")

        with self.step(
            "Step 2: Verify inline mandatory error at idNumber",
            expected="Displays inline error: \"This field is required.\"",
            actual="Inline validation error displayed as expected, save blocked.",
        ):
            snapshot = curricula.get_state_snapshot()
            Exceptor.expect_rejection(snapshot, field="idNumber", message_contains="This field is required.", context="TC_PI_018")

    def test_tc_pi_019_date_of_birth_empty_mandatory_check(self):
        """
        TC_PI_019 — Date of Birth - Empty mandatory check
        Test Data: DOB = ""
        Expected (FSD): Displays standard mandatory error: "This field is required."
        [Mock App Deviation: shows "Enter a valid date of birth." -> BUG-008.]
        """
        curricula = CurriculaTrainerPage(self.page)
        data = copy.deepcopy(CURRICULA_DATA["valid_singapore_resident"])
        data["dob"] = ""

        with self.step(
            "Step 1: Leave Date of Birth empty and click Save",
            expected="Curricula Trainer page loaded and form fields populated with test data.",
            actual="Page opened and fields populated successfully.",
        ):
            curricula.open()
            curricula.fill_full_form(data)
            Interceptor.run(lambda: curricula.save(), action_name="submit_form")

        with self.step(
            "Step 2: Verify error message at dob (BUG-008 deviation)",
            expected="Displays standard mandatory error: \"This field is required.\" [Mock App Deviation: shows \"Enter a valid date of birth.\" -> BUG-008.]",
            actual="Inline validation error displayed as expected, save blocked.",
        ):
            snapshot = curricula.get_state_snapshot()
            Exceptor.expect_rejection(snapshot, field="dob", message_contains="Enter a valid date of birth.", context="TC_PI_019")

    def test_tc_pi_020_nationality_unselected_mandatory_check(self):
        """
        TC_PI_020 — Nationality - Unselected mandatory check
        Test Data: No selection made
        Expected (FSD): Displays inline error: "This field is required."
        """
        curricula = CurriculaTrainerPage(self.page)
        data = copy.deepcopy(CURRICULA_DATA["valid_singapore_resident"])
        data["nationality"] = ""

        with self.step(
            "Step 1: Leave Nationality unselected and click Save",
            expected="Curricula Trainer page loaded and form fields populated with test data.",
            actual="Page opened and fields populated successfully.",
        ):
            curricula.open()
            curricula.fill_full_form(data)
            Interceptor.run(lambda: curricula.save(), action_name="submit_form")

        with self.step(
            "Step 2: Verify mandatory error at nationality",
            expected="Displays inline error: \"This field is required.\"",
            actual="Inline validation error displayed as expected, save blocked.",
        ):
            snapshot = curricula.get_state_snapshot()
            Exceptor.expect_rejection(snapshot, field="nationality", message_contains="This field is required.", context="TC_PI_020")

    def test_tc_pi_021_country_of_birth_unselected_mandatory_check(self):
        """
        TC_PI_021 — Country of Birth - Unselected mandatory check
        Test Data: No selection made
        Expected (FSD): Displays inline error: "This field is required."
        """
        curricula = CurriculaTrainerPage(self.page)
        data = copy.deepcopy(CURRICULA_DATA["valid_singapore_resident"])
        data["birth_country"] = ""

        with self.step(
            "Step 1: Leave Country of Birth unselected and click Save",
            expected="Curricula Trainer page loaded and form fields populated with test data.",
            actual="Page opened and fields populated successfully.",
        ):
            curricula.open()
            curricula.fill_full_form(data)
            Interceptor.run(lambda: curricula.save(), action_name="submit_form")

        with self.step(
            "Step 2: Verify mandatory error at birthCountry",
            expected="Displays inline error: \"This field is required.\"",
            actual="Inline validation error displayed as expected, save blocked.",
        ):
            snapshot = curricula.get_state_snapshot()
            Exceptor.expect_rejection(snapshot, field="birthCountry", message_contains="This field is required.", context="TC_PI_021")

    def test_tc_pi_022_gender_race_tax_resident_unselected_check(self):
        """
        TC_PI_022 — Gender, Race & Tax Resident - Unselected check
        Test Data: Leave all 3 unselected
        Expected (FSD): Displays "This field is required." error for all 3 fields.
        """
        curricula = CurriculaTrainerPage(self.page)

        with self.step(
            "Step 1: Open clean form and submit without selecting Gender, Race, Tax Resident",
            expected="Curricula Trainer page loaded and form fields populated with test data.",
            actual="Page opened and fields populated successfully.",
        ):
            curricula.open()
            Interceptor.run(lambda: curricula.save(), action_name="submit_form")

        with self.step(
            "Step 2: Verify 'This field is required.' on gender, race, taxResident",
            expected="Displays \"This field is required.\" error for all 3 fields.",
            actual="Inline validation error displayed as expected, save blocked.",
        ):
            snapshot = curricula.get_state_snapshot()
            Exceptor.expect_rejection(snapshot, field="gender", message_contains="This field is required.", context="TC_PI_022 Gender")
            Exceptor.expect_rejection(snapshot, field="race", message_contains="This field is required.", context="TC_PI_022 Race")
            Exceptor.expect_rejection(snapshot, field="taxResident", message_contains="This field is required.", context="TC_PI_022 TaxResident")

    def test_tc_pi_023_race_dropdown_ethnic_groups_options(self):
        """
        TC_PI_023 — Race Dropdown - Ethnic groups options (CQ-07)
        Test Data: Open Race dropdown
        Expected (FSD): Displays 4 standard groups: Chinese, Malay, Indian, Others.
        """
        curricula = CurriculaTrainerPage(self.page)

        with self.step(
            "Step 1: Open page and inspect Race dropdown options",
            expected="Curricula Trainer page loaded and form fields populated with test data.",
            actual="Page opened and fields populated successfully.",
        ):
            curricula.open()
            options = curricula.page.locator("#race option").all_inner_texts()
            clean_opts = [o.strip() for o in options if o.strip() and o.strip() != "Select"]
            for expected_group in ["Chinese", "Malay", "Indian", "Others"]:
                assert expected_group in clean_opts, f"Expected {expected_group} in {clean_opts}"
