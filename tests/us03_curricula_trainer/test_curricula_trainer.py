"""
tests/us03_curricula_trainer/test_curricula_trainer.py - Comprehensive Test Suite
for Curricula Trainer Account Creation form.

Covers:
- Group 1: Happy Path & End-to-End Scenarios (TC01 - TC07)
- Group 2: Validation Errors & Bug Detection (TC08 - TC20)
- Group 3: Dynamic UI Interactions & State Management (TC21 - TC27)
- Group 4: Boundary Values & Security Resilience (TC28 - TC32)

Built for high-concurrency parallel execution with pytest-xdist (-n).
Inherits from BaseTest (self.page, self.step, report helpers).
"""
from datetime import datetime, timedelta
import json
from pathlib import Path
import re
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
class TestCurriculaHappyPath(BaseTest):
    """Group 1: Happy Path & End-to-End Successful Account Creations."""

    def test_hp01_singapore_resident_full_valid_submission(self):
        """HP-01: Valid Singapore resident with all required & optional fields."""
        curricula = CurriculaTrainerPage(self.page)
        data = CURRICULA_DATA["valid_singapore_resident"]

        with self.step(
            "Step 1: Open Curricula Trainer Account page",
            expected="Page loads with HTTP 200 and title contains 'Curricula'",
            actual="Curricula Trainer page loaded successfully",
        ):
            curricula.open()
            self.assert_contains(curricula.get_title(), "Curricula")

        with self.step(
            "Step 2: Fill full valid Singapore resident form",
            expected="All form inputs populated with valid Singapore resident data via sequential keystrokes",
        ):
            curricula.fill_full_form(data)
            self.step.set_actual("Form filled with Singapore profile (Tan Wei Ling)")

        with self.step(
            "Step 3: Scroll to Save button, submit form, and verify successful account creation",
            expected="Success box appears displaying Trainer ID matching 'TRN\\d{6}' and 'Status: Active'",
        ):
            Interceptor.run(lambda: curricula.save(), action_name="submit_sg_form")
            Exceptor.expect_success(curricula.get_state_snapshot(), context="HP-01 Valid SG Resident")
            success_text = curricula.get_success_text()
            self.assert_contains(success_text, "Trainer account has been created successfully")
            self.assert_contains(success_text, "Status: Active")
            assert re.search(r"Trainer ID:\s*TRN\d{6}", success_text), f"Trainer ID format invalid: {success_text}"

            evidence = self.get_report_path("hp01_sg_success.png", test_scoped=True)
            curricula.take_screenshot(evidence)
            self.step.attach_screenshot(evidence)
            self.step.set_actual(f"Account created successfully. {success_text.splitlines()[1]}")

    def test_hp02_non_singapore_resident_vietnam_submission(self):
        """HP-02: Valid Non-Singapore resident (Vietnam) submission."""
        curricula = CurriculaTrainerPage(self.page)
        data = CURRICULA_DATA["valid_non_singapore_resident"]

        with self.step("Step 1: Open Curricula Trainer page"):
            curricula.open()

        with self.step("Step 2: Fill Non-Singapore resident form (Vietnam profile)"):
            curricula.fill_full_form(data)
            self.step.set_actual("Non-Singapore profile (Vietnam) filled")

        with self.step("Step 3: Scroll to Save button, submit, and verify successful international account creation"):
            Interceptor.run(lambda: curricula.save(), action_name="submit_non_sg_form")
            Exceptor.expect_success(curricula.get_state_snapshot(), context="HP-02 Non-SG Resident (Vietnam)")
            success_text = curricula.get_success_text()
            self.assert_contains(success_text, "Trainer account has been created successfully")
            evidence = self.get_report_path("hp02_non_sg_vn_success.png", test_scoped=True)
            curricula.take_screenshot(evidence)
            self.step.attach_screenshot(evidence)

    def test_hp03_singapore_resident_floor_not_applicable(self):
        """HP-03: Valid Singapore resident with 'Floor/Unit number is not applicable' checked."""
        curricula = CurriculaTrainerPage(self.page)
        data = CURRICULA_DATA["valid_singapore_resident_floor_na"]

        with self.step("Step 1: Open Curricula Trainer Account page"):
            curricula.open()

        with self.step("Step 2: Fill form with Floor/Unit N/A enabled"):
            curricula.fill_full_form(data)
            assert not curricula.is_element_enabled(curricula.FLOOR_NUMBER), "Floor number should be disabled"
            assert not curricula.is_element_enabled(curricula.UNIT_NUMBER), "Unit number should be disabled"
            self.step.set_actual("Floor/Unit inputs confirmed disabled")

        with self.step("Step 3: Scroll to Save button, submit, and verify success without floor/unit inputs"):
            Interceptor.run(lambda: curricula.save(), action_name="submit_sg_floor_na")
            Exceptor.expect_success(curricula.get_state_snapshot(), context="HP-03 SG Floor/Unit N/A")
            evidence = self.get_report_path("hp03_sg_floor_na_success.png", test_scoped=True)
            curricula.take_screenshot(evidence)
            self.step.attach_screenshot(evidence)

    # Backward-compatibility aliases
    test_tc01_singapore_resident_full_valid_submission = test_hp01_singapore_resident_full_valid_submission
    test_tc02_singapore_resident_floor_not_applicable = test_hp03_singapore_resident_floor_not_applicable
    test_tc03_non_singapore_resident_vietnam_submission = test_hp02_non_singapore_resident_vietnam_submission

    def test_tc04_non_singapore_resident_malaysia_with_optional_fields(self):
        """TC04: Valid Non-Singapore resident (Malaysia) with optional Address 2 and State."""
        curricula = CurriculaTrainerPage(self.page)
        data = CURRICULA_DATA["valid_malaysia_resident"]

        with self.step("Step 1: Open Curricula Trainer page"):
            curricula.open()

        with self.step("Step 2: Fill Non-Singapore profile with optional address fields"):
            curricula.fill_full_form(data)

        with self.step("Step 3: Submit and confirm successful registration"):
            Interceptor.run(lambda: curricula.save(), action_name="submit_non_sg_malaysia")
            Exceptor.expect_success(curricula.get_state_snapshot(), context="TC04 Malaysia Resident with optional fields")


@pytest.mark.curricula
class TestCurriculaUnhappyPathAndBugs(BaseTest):
    """
    Group: Unhappy Path & Bug Hunting Test Suite.
    Every test strictly follows the enterprise verification flow:
    1. Fill form with intentional invalid/buggy input.
    2. Scroll down and click Submit / Save button.
    3. Detect submission rejection.
    4. Smooth-scroll directly to the erroneous field and highlight it with a red glow halo.
    5. Pause for 1.5s for crystal-clear video and visual evidence recording.
    6. Assert error message text.
    7. Capture deliverable screenshot of the highlighted error state.
    """

    def test_up01_bug_singapore_unit_alphanumeric_regex(self):
        """
        UP-01 (Bug Hunting): Singapore unit numbers often contain alphanumeric characters (e.g. '#04-12A', '#B1-02').
        The system's regex '/^\\d{1,9}$/' incorrectly rejects them.
        Flow: Fill valid form -> set unit '12A' -> Save -> Detect defect -> Scroll to Floor/Unit error -> Glow red -> Screenshot -> Raise AssertionError [BUG DETECTED] -> Status FAILED.
        """
        curricula = CurriculaTrainerPage(self.page)
        data = CURRICULA_DATA["valid_singapore_resident"].copy()
        data["unit_number"] = "12A"  # Bug trigger: Alphanumeric unit number

        with self.step(
            "Step 1: Fill Singapore resident form with authentic alphanumeric unit number '#04-12A'",
            expected="Form filled with authentic Singapore address: Commonwealth Drive #04-12A",
        ):
            curricula.open()
            curricula.fill_full_form(data)

        with self.step(
            "Step 2: Scroll down to Save, submit form, and verify account creation",
            expected="Form should accept valid Singapore unit '#04-12A' and create Trainer Account successfully",
        ):
            Interceptor.run(lambda: curricula.save(), action_name="submit_sg_alphanumeric_unit")

        with self.step(
            "Step 3: Defect Verification - Scroll to Floor/Unit error, highlight with red halo, and report bug",
            expected="System should allow alphanumeric unit '#04-12A'. If rejected, mark test as FAILED with [BUG DETECTED].",
        ):
            snapshot = curricula.get_state_snapshot()
            if not snapshot["success_visible"]:
                curricula.scroll_to_error("floorUnit", highlight=True, pause_ms=1500)
                err_text = snapshot["visible_errors"].get("floorUnit", "")
                evidence = self.get_report_path("up01_bug_unit_regex.png", test_scoped=True)
                curricula.take_screenshot(evidence)
                self.step.attach_screenshot(evidence)
                self.step.set_actual(f"[PRODUCT DEFECT] Valid unit '12A' rejected with: '{err_text}'. Highlighted in red.")
            else:
                self.step.set_actual("[PASSED] Form accepted unit '12A'")

            Exceptor.expect_bug_if_rejected(
                snapshot,
                field="floorUnit",
                context="UP-01 Singapore Alphanumeric Unit '#04-12A' incorrectly rejected by numeric-only regex",
            )

    def test_up02_future_date_of_birth_scroll_error(self):
        """
        UP-02: Future Date of Birth rejection.
        Flow: Fill valid form -> set future DOB (e.g. 2030-01-01) -> Save -> Form rejects -> Scroll up to DOB field -> Glow red -> Screenshot -> Assert defense.
        """
        curricula = CurriculaTrainerPage(self.page)
        data = CURRICULA_DATA["valid_singapore_resident"].copy()
        future_dob = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
        data["dob"] = future_dob

        with self.step(
            f"Step 1: Fill Singapore form with future date of birth '{future_dob}'",
            expected="Personal information filled with future birth date",
        ):
            curricula.open()
            curricula.fill_full_form(data)

        with self.step(
            "Step 2: Scroll to Save button, click submit, and verify submission is blocked",
            expected="Form rejects submission because birth date is in the future",
        ):
            Interceptor.run(lambda: curricula.save(), action_name="submit_future_dob")

        with self.step(
            "Step 3: Scroll up to Date of Birth field, highlight with red halo, and verify rejection",
            expected="Viewport scrolls to Personal Info, highlights DOB and reports submission rejection defense",
        ):
            curricula.scroll_to_error("dob", highlight=True, pause_ms=1500)
            snapshot = curricula.get_state_snapshot()
            evidence = self.get_report_path("up02_future_dob_error.png", test_scoped=True)
            curricula.take_screenshot(evidence)
            self.step.attach_screenshot(evidence)
            err_text = snapshot["visible_errors"].get("dob", "")
            self.step.set_actual(f"[SUBMISSION REJECTED] Future birth date rejected with error: '{err_text}'. Highlighted in red.")

            Exceptor.expect_rejection(
                snapshot,
                field="dob",
                message_contains="Enter a valid date of birth",
                context="UP-02 Future Date of Birth rejection defense",
            )

    def test_up03_malformed_email_scroll_error(self):
        """
        UP-03: Malformed Email Address (missing '@').
        Flow: Fill valid form -> set primary email 'trainer_invalid_email.com' -> Save -> Form rejects -> Scroll to Primary Email -> Glow red -> Screenshot -> Raise AssertionError -> Status FAILED.
        """
        curricula = CurriculaTrainerPage(self.page)
        data = CURRICULA_DATA["valid_singapore_resident"].copy()
        data["primary_email"] = "trainer_invalid_email.com"

        with self.step(
            "Step 1: Fill form with malformed email 'trainer_invalid_email.com' (missing '@')",
            expected="Contact information contains malformed email without @ domain",
        ):
            curricula.open()
            curricula.fill_full_form(data)

        with self.step(
            "Step 2: Scroll down to Save, submit form, and verify submission is blocked",
            expected="Validation blocks submission due to invalid email format",
        ):
            Interceptor.run(lambda: curricula.save(), action_name="submit_malformed_email")

        with self.step(
            "Step 3: Scroll to Primary Email field, highlight with red halo, and verify rejection",
            expected="Viewport scrolls to Contact Info, highlights primaryEmail and reports submission rejection defense",
        ):
            curricula.scroll_to_error("primaryEmail", highlight=True, pause_ms=1500)
            snapshot = curricula.get_state_snapshot()
            evidence = self.get_report_path("up03_malformed_email_error.png", test_scoped=True)
            curricula.take_screenshot(evidence)
            self.step.attach_screenshot(evidence)
            err_text = snapshot["visible_errors"].get("primaryEmail", "")
            self.step.set_actual(f"[SUBMISSION REJECTED] Malformed email rejected with error: '{err_text}'. Highlighted in red.")

            Exceptor.expect_rejection(
                snapshot,
                field="primaryEmail",
                message_contains="Enter a valid email address",
                context="UP-03 Malformed email address rejection defense",
            )

    def test_up04_invalid_singapore_phone_length_scroll_error(self):
        """
        UP-04: Invalid Singapore Phone Number (6 digits instead of 8).
        Flow: Fill valid form -> set primary phone '123456' -> Save -> Form rejects -> Scroll to Primary Phone -> Glow red -> Screenshot -> Raise AssertionError -> Status FAILED.
        """
        curricula = CurriculaTrainerPage(self.page)
        data = CURRICULA_DATA["valid_singapore_resident"].copy()
        data["primary_phone"] = "123456"

        with self.step(
            "Step 1: Fill form with 6-digit Singapore phone '123456' (requires 8 digits starting with 8 or 9)",
            expected="Primary phone filled with invalid short phone number",
        ):
            curricula.open()
            curricula.fill_full_form(data)

        with self.step(
            "Step 2: Scroll down to Save, submit form, and verify submission is blocked",
            expected="Validation blocks submission due to invalid Singapore phone format",
        ):
            Interceptor.run(lambda: curricula.save(), action_name="submit_short_sg_phone")

        with self.step(
            "Step 3: Scroll to Primary Phone field, highlight with red halo, and verify rejection",
            expected="Viewport scrolls to Contact Info, highlights primaryPhone and reports submission rejection defense",
        ):
            curricula.scroll_to_error("primaryPhone", highlight=True, pause_ms=1500)
            snapshot = curricula.get_state_snapshot()
            evidence = self.get_report_path("up04_invalid_sg_phone_error.png", test_scoped=True)
            curricula.take_screenshot(evidence)
            self.step.attach_screenshot(evidence)
            err_text = snapshot["visible_errors"].get("primaryPhone", "")
            self.step.set_actual(f"[SUBMISSION REJECTED] Invalid phone rejected with error: '{err_text}'. Highlighted in red.")

            Exceptor.expect_rejection(
                snapshot,
                field="primaryPhone",
                message_contains="Enter a valid contact number",
                context="UP-04 Invalid Singapore phone length rejection defense",
            )

    def test_up05_disallowed_file_extension_scroll_error(self):
        """
        UP-05: Disallowed File Upload Extension (executable 'malicious.exe').
        Flow: Fill valid form -> attach 'malicious.exe' -> Save -> Form rejects -> Scroll to Upload Box -> Glow red -> Screenshot -> Raise AssertionError -> Status FAILED.
        """
        curricula = CurriculaTrainerPage(self.page)
        data = CURRICULA_DATA["valid_singapore_resident"].copy()
        data["id_document"] = "data/fixtures/malicious.exe"

        with self.step(
            "Step 1: Fill form and attach disallowed executable file 'malicious.exe'",
            expected="Document upload attached with disallowed .exe file",
        ):
            curricula.open()
            curricula.fill_full_form(data)

        with self.step(
            "Step 2: Scroll down to Save, submit form, and verify security rejection",
            expected="Form rejects upload because .exe is not allowed MIME type (JPG, PNG, PDF)",
        ):
            Interceptor.run(lambda: curricula.save(), action_name="submit_disallowed_file")

        with self.step(
            "Step 3: Scroll up to ID Document upload area, highlight with red halo, and verify rejection",
            expected="Viewport scrolls to Personal Info, highlights idDocument and reports submission rejection defense",
        ):
            curricula.scroll_to_error("idDocument", highlight=True, pause_ms=1500)
            snapshot = curricula.get_state_snapshot()
            evidence = self.get_report_path("up05_disallowed_file_error.png", test_scoped=True)
            curricula.take_screenshot(evidence)
            self.step.attach_screenshot(evidence)
            err_text = snapshot["visible_errors"].get("idDocument", "")
            self.step.set_actual(f"[SUBMISSION REJECTED] Disallowed file rejected with error: '{err_text}'. Highlighted in red.")

            Exceptor.expect_rejection(
                snapshot,
                field="idDocument",
                message_contains="valid document",
                context="UP-05 Disallowed file extension rejection defense",
            )

    @pytest.mark.parametrize(
        "entry",
        CURRICULA_DATA["postal_code_auto_populates"],
        ids=[f"PC_{e['postal_code']}" for e in CURRICULA_DATA["postal_code_auto_populates"]],
    )
    def test_tc05_07_postal_code_auto_population(self, entry):
        """TC05-07: Auto-populate Block and Street Name on Singapore postal code blur."""
        curricula = CurriculaTrainerPage(self.page)
        pc = entry["postal_code"]
        exp_block = entry["expected_block"]
        exp_street = entry["expected_street"]

        with self.step(f"Step 1: Open page and enter Singapore postal code '{pc}'"):
            curricula.open()
            curricula.set_postal_code(pc, trigger_blur=True)

        with self.step(
            f"Step 2: Verify auto-population of Block '{exp_block}' and Street '{exp_street}'",
            expected=f"Block Number == '{exp_block}', Street Name == '{exp_street}'",
        ):
            actual_block = curricula.get_field_value(curricula.BLOCK_NUMBER)
            actual_street = curricula.get_field_value(curricula.STREET_NAME)
            assert actual_block == exp_block, f"Expected block {exp_block}, got {actual_block}"
            assert actual_street == exp_street, f"Expected street {exp_street}, got {actual_street}"
            self.step.set_actual(f"Auto-filled Block: {actual_block}, Street: {actual_street}")


@pytest.mark.curricula
class TestCurriculaValidationAndErrors(BaseTest):
    """Group 2: Validation Rules, Mandatory Fields, and Bug Hunting Scenarios."""

    def test_tc08_empty_form_submission_triggers_all_errors(self):
        """TC08: Clicking Save on a pristine empty form triggers required field validations."""
        curricula = CurriculaTrainerPage(self.page)

        with self.step("Step 1: Open form and submit blank"):
            curricula.open()
            Interceptor.run(lambda: curricula.save(), action_name="submit_empty_form")

        with self.step("Step 2: Verify all mandatory validation errors are visible"):
            expected_error_keys = [
                "preferredName",
                "gender",
                "idType",
                "idNumber",
                "idDocument",
                "nationality",
                "dob",
                "race",
                "birthCountry",
                "taxResident",
                "primaryEmail",
                "primaryPhone",
                "emergencyName",
                "emergencyRelationship",
                "emergencyPhone",
                "postalCode",
                "blockNumber",
                "streetName",
                "floorUnit",
            ]
            snapshot = curricula.get_state_snapshot()
            missing_errors = [k for k in expected_error_keys if k not in snapshot["visible_errors"]]

            evidence = self.get_report_path("tc08_empty_form_errors.png", test_scoped=True)
            curricula.take_screenshot(evidence)
            self.step.attach_screenshot(evidence)

            assert not missing_errors, f"Validation errors missing for fields: {missing_errors}"
            Exceptor.expect_rejection(
                snapshot,
                field="preferredName",
                message_contains="required",
                context="TC08 Empty Form Submission",
            )
            self.step.set_actual(f"All {len(expected_error_keys)} required validation messages verified")

    def test_tc09_missing_mandatory_personal_info(self):
        """TC09: Submitting form with partial personal info highlights missing required inputs."""
        curricula = CurriculaTrainerPage(self.page)

        with self.step("Step 1: Open page and set only preferred name"):
            curricula.open()
            curricula.set_preferred_name("Alex Tan")
            Interceptor.run(lambda: curricula.save(), action_name="submit_partial_personal_info")

        with self.step("Step 2: Verify preferredName has no error but gender and ID type display errors"):
            snapshot = curricula.get_state_snapshot()
            assert not curricula.is_error_visible("preferredName"), "preferredName should not have error"
            Exceptor.expect_rejection(snapshot, field="gender", message_contains="required", context="TC09 missing gender")
            Exceptor.expect_rejection(snapshot, field="idType", message_contains="required", context="TC09 missing idType")
            Exceptor.expect_rejection(snapshot, field="idNumber", message_contains="required", context="TC09 missing idNumber")

    def test_tc10_invalid_dob_future_date_rejected(self):
        """TC10: Future Date of Birth triggers 'Enter a valid date of birth.' validation."""
        curricula = CurriculaTrainerPage(self.page)
        future_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")

        with self.step(f"Step 1: Enter future date of birth '{future_date}'"):
            curricula.open()
            curricula.set_dob(future_date)
            Interceptor.run(lambda: curricula.save(), action_name="submit_future_dob")

        with self.step("Step 2: Verify DOB error is visible"):
            snapshot = curricula.get_state_snapshot()
            Exceptor.expect_rejection(
                snapshot,
                field="dob",
                message_contains="Enter a valid date of birth",
                context="TC10 Future DOB rejection",
            )

    @pytest.mark.parametrize(
        "invalid_email",
        CURRICULA_DATA["invalid_emails"],
        ids=[f"Email_{i+1}" for i in range(len(CURRICULA_DATA["invalid_emails"]))],
    )
    def test_tc11_invalid_primary_email_formats(self, invalid_email):
        """TC11: Malformed email formats trigger 'Enter a valid email address.'."""
        curricula = CurriculaTrainerPage(self.page)

        with self.step(f"Step 1: Enter invalid email '{invalid_email}' and save"):
            curricula.open()
            curricula.set_primary_email(invalid_email)
            Interceptor.run(lambda: curricula.save(), action_name="submit_invalid_email")

        with self.step(f"Step 2: Verify email error displays for '{invalid_email}'"):
            snapshot = curricula.get_state_snapshot()
            Exceptor.expect_rejection(
                snapshot,
                field="primaryEmail",
                message_contains="valid email address",
                context=f"TC11 invalid email {invalid_email}",
            )

    @pytest.mark.parametrize(
        "phone",
        CURRICULA_DATA["invalid_singapore_phones"],
        ids=[f"SGPhone_{i+1}" for i in range(len(CURRICULA_DATA["invalid_singapore_phones"]))],
    )
    def test_tc12_invalid_singapore_phone_numbers(self, phone):
        """TC12: Singapore phone (+65) with non-8 digits or non-numeric characters triggers error."""
        curricula = CurriculaTrainerPage(self.page)

        with self.step(f"Step 1: Set Singapore phone to '{phone}'"):
            curricula.open()
            curricula.set_primary_phone("+65", phone)
            Interceptor.run(lambda: curricula.save(), action_name="submit_invalid_sg_phone")

        with self.step(f"Step 2: Verify primary phone error for '{phone}'"):
            snapshot = curricula.get_state_snapshot()
            Exceptor.expect_rejection(
                snapshot,
                field="primaryPhone",
                message_contains="Enter a valid contact number",
                context=f"TC12 invalid SG phone {phone}",
            )

    @pytest.mark.parametrize(
        "phone",
        CURRICULA_DATA["invalid_foreign_phones"],
        ids=[f"ForeignPhone_{i+1}" for i in range(len(CURRICULA_DATA["invalid_foreign_phones"]))],
    )
    def test_tc13_invalid_foreign_phone_numbers(self, phone):
        """TC13: Foreign phone numbers (+84) shorter than 8 digits or longer than 15 digits trigger error."""
        curricula = CurriculaTrainerPage(self.page)

        with self.step(f"Step 1: Set Vietnam phone (+84) to '{phone}'"):
            curricula.open()
            curricula.set_primary_phone("+84", phone)
            Interceptor.run(lambda: curricula.save(), action_name="submit_invalid_foreign_phone")

        with self.step(f"Step 2: Verify foreign phone error for '{phone}'"):
            snapshot = curricula.get_state_snapshot()
            Exceptor.expect_rejection(
                snapshot,
                field="primaryPhone",
                message_contains="Enter a valid contact number",
                context=f"TC13 invalid foreign phone {phone}",
            )

    def test_tc14_secondary_phone_optional_when_blank_invalid_when_malformed(self):
        """TC14: Secondary phone is optional when blank, but validates format when entered."""
        curricula = CurriculaTrainerPage(self.page)

        with self.step("Step 1: When secondary phone is blank, no secondaryPhone error"):
            curricula.open()
            Interceptor.run(lambda: curricula.save(), action_name="submit_blank_secondary_phone")
            assert not curricula.is_error_visible("secondaryPhone"), "Secondary phone shouldn't error when blank"

        with self.step("Step 2: When secondary phone is malformed, error is triggered"):
            curricula.set_secondary_phone("+65", "123")  # too short
            Interceptor.run(lambda: curricula.save(), action_name="submit_invalid_secondary_phone")
            snapshot = curricula.get_state_snapshot()
            Exceptor.expect_rejection(
                snapshot,
                field="secondaryPhone",
                message_contains="Enter a valid contact number",
                context="TC14 secondary phone format",
            )

    def test_tc15_missing_emergency_contact_validation(self):
        """TC15: Missing emergency contact name, relationship, or phone triggers error."""
        curricula = CurriculaTrainerPage(self.page)

        with self.step("Step 1: Open page and submit without emergency contact"):
            curricula.open()
            Interceptor.run(lambda: curricula.save(), action_name="submit_missing_emergency_contact")

        with self.step("Step 2: Check emergency fields validation messages"):
            snapshot = curricula.get_state_snapshot()
            Exceptor.expect_rejection(snapshot, field="emergencyName", message_contains="required", context="TC15 missing emergencyName")
            Exceptor.expect_rejection(snapshot, field="emergencyRelationship", message_contains="required", context="TC15 missing emergencyRelationship")
            Exceptor.expect_rejection(snapshot, field="emergencyPhone", message_contains="Enter a valid contact number", context="TC15 missing emergencyPhone")

    @pytest.mark.parametrize(
        "pc",
        CURRICULA_DATA["invalid_postal_codes"],
        ids=[f"Postal_{i+1}" for i in range(len(CURRICULA_DATA["invalid_postal_codes"]))],
    )
    def test_tc16_invalid_singapore_postal_code(self, pc):
        """TC16: Singapore postal code not matching exactly 6 digits triggers validation error."""
        curricula = CurriculaTrainerPage(self.page)

        with self.step(f"Step 1: Enter invalid postal code '{pc}' and save"):
            curricula.open()
            curricula.set_residential_type("Singapore")
            curricula.set_postal_code(pc, trigger_blur=True)
            Interceptor.run(lambda: curricula.save(), action_name="submit_invalid_postal_code")

        with self.step(f"Step 2: Verify postal code error for '{pc}'"):
            snapshot = curricula.get_state_snapshot()
            Exceptor.expect_rejection(
                snapshot,
                field="postalCode",
                message_contains="Enter a valid postal code",
                context=f"TC16 invalid postal code {pc}",
            )

    @pytest.mark.parametrize(
        "unit",
        CURRICULA_DATA["invalid_unit_numbers"],
        ids=[f"Unit_{i+1}" for i in range(len(CURRICULA_DATA["invalid_unit_numbers"]))],
    )
    def test_tc17_invalid_floor_unit_format_bug_detection(self, unit):
        """
        TC17 (Bug Hunting): Singapore floor/unit validation requires pure digits (/^\\d{1,9}$/).
        Alphanumeric units like '12A' or 'B1-02' (common in Singapore) trigger validation failure.
        """
        curricula = CurriculaTrainerPage(self.page)

        with self.step(f"Step 1: Enter alphanumeric unit '{unit}' with floor '04'"):
            curricula.open()
            curricula.set_singapore_address(
                postal_code="120047",
                block="142",
                street="Commonwealth Drive",
                floor="04",
                unit=unit,
            )
            Interceptor.run(lambda: curricula.save(), action_name="submit_alphanumeric_unit")

        with self.step(f"Step 2: Defect detection - Unit '{unit}' rejected by numeric-only regex"):
            snapshot = curricula.get_state_snapshot()
            if not snapshot["success_visible"]:
                curricula.scroll_to_error("floorUnit", highlight=True, pause_ms=1000)
                err_text = snapshot["visible_errors"].get("floorUnit", "")
                self.step.set_actual(f"[DEFECT DETECTED] Unit '{unit}' was rejected by regex with: '{err_text}'")
            else:
                self.step.set_actual(f"Unit '{unit}' accepted")

            Exceptor.expect_bug_if_rejected(
                snapshot,
                field="floorUnit",
                context=f"TC17 Singapore alphanumeric unit '{unit}' rejected by numeric regex",
            )

    def test_tc18_non_singapore_selecting_singapore_country_rejected(self):
        """TC18: In Non-Singapore mode, selecting Singapore as Country/Region is rejected."""
        curricula = CurriculaTrainerPage(self.page)

        with self.step("Step 1: Switch to Non-Singapore and force select 'Singapore'"):
            curricula.open()
            curricula.set_residential_type("Non-Singapore")
            curricula.select_country_region("Singapore")
            Interceptor.run(lambda: curricula.save(), action_name="submit_non_sg_country_singapore")

        with self.step("Step 2: Verify countryRegion error is displayed"):
            snapshot = curricula.get_state_snapshot()
            Exceptor.expect_rejection(
                snapshot,
                field="countryRegion",
                message_contains="required",
                context="TC18 countryRegion Singapore in Non-SG mode",
            )

    def test_tc19_non_singapore_missing_mandatory_address_fields(self):
        """TC19: Non-Singapore mode requires Address Line 1 and City."""
        curricula = CurriculaTrainerPage(self.page)

        with self.step("Step 1: Switch to Non-Singapore mode with empty address"):
            curricula.open()
            curricula.set_residential_type("Non-Singapore")
            curricula.select_country_region("Vietnam")
            Interceptor.run(lambda: curricula.save(), action_name="submit_non_sg_empty_address")

        with self.step("Step 2: Verify address1 and city errors are displayed"):
            snapshot = curricula.get_state_snapshot()
            Exceptor.expect_rejection(snapshot, field="address1", message_contains="required", context="TC19 missing address1")
            Exceptor.expect_rejection(snapshot, field="city", message_contains="required", context="TC19 missing city")

    def test_tc20_invalid_file_upload_extension_rejected(self):
        """TC20: Uploading a prohibited file type (.txt) triggers document validation error."""
        curricula = CurriculaTrainerPage(self.page)
        invalid_file = WORKSPACE_DIR / "data" / "fixtures" / "invalid_document.txt"

        with self.step("Step 1: Upload .txt file and click Save"):
            curricula.open()
            curricula.upload_document(invalid_file)
            Interceptor.run(lambda: curricula.save(), action_name="submit_invalid_file_txt")

        with self.step("Step 2: Verify idDocument error message is visible"):
            snapshot = curricula.get_state_snapshot()
            Exceptor.expect_rejection(
                snapshot,
                field="idDocument",
                message_contains="valid document",
                context="TC20 invalid file extension .txt",
            )


@pytest.mark.curricula
class TestCurriculaUIInteractions(BaseTest):
    """Group 3: Dynamic UI Transitions, State Toggles, and Dialog Handlers."""

    def test_tc21_toggle_residential_to_non_singapore(self):
        """TC21: Switching to Non-Singapore reveals international fields and enables Country dropdown."""
        curricula = CurriculaTrainerPage(self.page)

        with self.step("Step 1: Open form and switch residential type to Non-Singapore"):
            curricula.open()
            curricula.set_residential_type("Non-Singapore")

        with self.step("Step 2: Verify Singapore fields hidden and Non-Singapore fields visible"):
            assert not self.page.locator(curricula.SG_BLOCK_FIELD).is_visible(), "SG block field should be hidden"
            assert not self.page.locator(curricula.SG_STREET_FIELD).is_visible(), "SG street field should be hidden"
            assert self.page.locator(curricula.NON_SG_ADDRESS1).is_visible(), "Non-SG address1 should be visible"
            assert self.page.locator(curricula.NON_SG_CITY).is_visible(), "Non-SG city should be visible"
            assert curricula.is_element_enabled(curricula.COUNTRY_REGION), "Country dropdown should be enabled"

    def test_tc22_toggle_residential_back_to_singapore(self):
        """TC22: Switching back to Singapore restores Singapore inputs and disables Country dropdown."""
        curricula = CurriculaTrainerPage(self.page)

        with self.step("Step 1: Switch to Non-Singapore then back to Singapore"):
            curricula.open()
            curricula.set_residential_type("Non-Singapore")
            curricula.set_residential_type("Singapore")

        with self.step("Step 2: Verify SG fields restored and Country reset to Singapore & disabled"):
            assert self.page.locator(curricula.SG_BLOCK_FIELD).is_visible(), "SG block field should be visible"
            assert self.page.locator(curricula.SG_STREET_FIELD).is_visible(), "SG street field should be visible"
            assert not self.page.locator(curricula.NON_SG_ADDRESS1).is_visible(), "Non-SG address1 should be hidden"
            assert not curricula.is_element_enabled(curricula.COUNTRY_REGION), "Country dropdown should be disabled"
            assert curricula.get_field_value(curricula.COUNTRY_REGION) == "Singapore"

    def test_tc23_floor_unit_not_applicable_toggle(self):
        """TC23: Checking 'Floor/Unit N/A' disables inputs and clears values; unchecking restores."""
        curricula = CurriculaTrainerPage(self.page)

        with self.step("Step 1: Enter floor and unit numbers, then check N/A checkbox"):
            curricula.open()
            curricula.fill_text(curricula.FLOOR_NUMBER, "05")
            curricula.fill_text(curricula.UNIT_NUMBER, "102")
            curricula.set_floor_not_applicable(True)

        with self.step("Step 2: Verify inputs disabled and cleared"):
            assert not curricula.is_element_enabled(curricula.FLOOR_NUMBER)
            assert not curricula.is_element_enabled(curricula.UNIT_NUMBER)
            assert curricula.get_field_value(curricula.FLOOR_NUMBER) == ""
            assert curricula.get_field_value(curricula.UNIT_NUMBER) == ""

        with self.step("Step 3: Uncheck N/A checkbox and verify inputs re-enabled"):
            curricula.set_floor_not_applicable(False)
            assert curricula.is_element_enabled(curricula.FLOOR_NUMBER)
            assert curricula.is_element_enabled(curricula.UNIT_NUMBER)

    def test_tc24_cancel_button_dirty_form_dismiss_confirm(self):
        """TC24: Clicking Cancel with dirty form triggers confirm dialog; dismissing preserves form data."""
        curricula = CurriculaTrainerPage(self.page)

        with self.step("Step 1: Populate preferred name and register dialog dismiss handler"):
            curricula.open()
            curricula.set_preferred_name("Draft Trainer Name")

            dialog_message = []

            def on_dialog(dialog):
                dialog_message.append(dialog.message)
                dialog.dismiss()

            self.page.once("dialog", on_dialog)

        with self.step("Step 2: Click Cancel and dismiss confirmation"):
            curricula.cancel()
            assert len(dialog_message) == 1, "Expected confirmation dialog to appear"
            self.assert_contains(dialog_message[0], "unsaved changes")
            assert curricula.get_field_value(curricula.PREFERRED_NAME) == "Draft Trainer Name"
            self.step.set_actual("Dialog dismissed; form input value preserved")

    def test_tc25_cancel_button_dirty_form_accept_confirm(self):
        """TC25: Clicking Cancel with dirty form and accepting confirm reloads and resets page."""
        curricula = CurriculaTrainerPage(self.page)

        with self.step("Step 1: Populate preferred name and register dialog accept handler"):
            curricula.open()
            curricula.set_preferred_name("Temporary Name")

            dialog_handled = []

            def on_dialog(dialog):
                dialog_handled.append(True)
                dialog.accept()

            self.page.once("dialog", on_dialog)

        with self.step("Step 2: Click Cancel, accept confirm and verify page reloaded with empty form"):
            curricula.cancel()
            self.page.wait_for_load_state("domcontentloaded")
            assert len(dialog_handled) == 1
            assert curricula.get_field_value(curricula.PREFERRED_NAME) == ""
            self.step.set_actual("Dialog accepted; form was reset cleanly")

    def test_tc26_cancel_button_clean_form_direct_reload(self):
        """TC26: Clicking Cancel with clean form reloads without showing confirm dialog."""
        curricula = CurriculaTrainerPage(self.page)

        with self.step("Step 1: Open clean form and listen for dialog"):
            curricula.open()
            dialog_triggered = []
            self.page.on("dialog", lambda d: dialog_triggered.append(d))

        with self.step("Step 2: Click Cancel on empty form"):
            curricula.cancel()
            self.page.wait_for_load_state("domcontentloaded")
            assert len(dialog_triggered) == 0, "No dialog should trigger on pristine form"

    def test_tc27_success_box_content_and_trainer_id_format(self):
        """TC27: Verify structure of success notification box and Trainer ID pattern."""
        curricula = CurriculaTrainerPage(self.page)
        data = CURRICULA_DATA["valid_singapore_resident"]

        with self.step("Step 1: Complete and submit valid registration"):
            curricula.open()
            curricula.fill_full_form(data)
            Interceptor.run(lambda: curricula.save(), action_name="submit_valid_registration")

        with self.step("Step 2: Verify success DOM structure"):
            Exceptor.expect_success(curricula.get_state_snapshot(), context="TC27 Valid registration DOM structure")
            trainer_id_span = self.page.locator("#successBox .trainer-id")
            assert trainer_id_span.is_visible(), ".trainer-id span should be visible"
            span_text = trainer_id_span.inner_text().strip()
            match = re.match(r"^Trainer ID:\s*(TRN\d{6})$", span_text)
            assert match, f"Trainer ID should match TRN followed by 6 digits. Got '{span_text}'"
            self.step.set_actual(f"Validated format: {match.group(1)}")


@pytest.mark.curricula
class TestCurriculaBoundaryAndSecurity(BaseTest):
    """Group 4: Boundary Values, Max Lengths, and Security Injections."""

    def test_tc28_preferred_name_maxlength_boundary(self):
        """TC28: Preferred Name accepts up to 255 characters (HTML maxlength='255')."""
        curricula = CurriculaTrainerPage(self.page)
        long_name = "A" * 255

        with self.step("Step 1: Input 255 characters into Preferred Name"):
            curricula.open()
            curricula.set_preferred_name(long_name)

        with self.step("Step 2: Verify input contains exactly 255 characters"):
            val = curricula.get_field_value(curricula.PREFERRED_NAME)
            assert len(val) == 255, f"Expected length 255, got {len(val)}"

    def test_tc29_preferred_name_unicode_vietnamese_characters(self):
        """TC29: Preferred Name handles Unicode and multi-byte Vietnamese characters gracefully."""
        curricula = CurriculaTrainerPage(self.page)
        vietnamese_name = "Nguyễn Đặng Hoàng Ánh"

        with self.step(f"Step 1: Enter Vietnamese name '{vietnamese_name}'"):
            curricula.open()
            curricula.set_preferred_name(vietnamese_name)

        with self.step("Step 2: Verify name is preserved without distortion"):
            val = curricula.get_field_value(curricula.PREFERRED_NAME)
            assert val == vietnamese_name, f"Expected '{vietnamese_name}', got '{val}'"

    def test_tc30_email_maxlength_boundary(self):
        """TC30: Primary Email respects maxlength='100' boundary."""
        curricula = CurriculaTrainerPage(self.page)
        max_email_prefix = "user" + ("x" * 80)
        test_email = f"{max_email_prefix}@curricula.edu.sg"[:100]

        with self.step("Step 1: Enter 100-character email"):
            curricula.open()
            curricula.set_primary_email(test_email)

        with self.step("Step 2: Verify email input length is at most 100"):
            val = curricula.get_field_value(curricula.PRIMARY_EMAIL)
            assert len(val) <= 100, f"Email exceeded 100 characters: {len(val)}"

    def test_tc31_xss_injection_resilience(self):
        """TC31: Preferred Name handles script injection payload without executing script."""
        curricula = CurriculaTrainerPage(self.page)
        xss_payload = "<script>window._xss_executed=true;</script>"

        with self.step("Step 1: Enter XSS payload into preferred name"):
            curricula.open()
            curricula.set_preferred_name(xss_payload)
            Interceptor.run(lambda: curricula.save(), action_name="submit_xss_payload")

        with self.step("Step 2: Verify JavaScript did not execute in document window"):
            executed = self.page.evaluate("() => window._xss_executed === true")
            assert not executed, "Security Failure: Script injection payload was executed!"
            self.step.set_actual("Form treated XSS payload as literal text; no execution")

    def test_tc32_sqli_special_characters_resilience(self):
        """TC32: Special SQL Injection strings (' OR '1'='1) do not break form inputs or layout."""
        curricula = CurriculaTrainerPage(self.page)
        sqli_payload = "admin' OR '1'='1' --"

        with self.step(f"Step 1: Enter SQLi payload '{sqli_payload}' into ID Number"):
            curricula.open()
            curricula.set_id_number(sqli_payload)
            Interceptor.run(lambda: curricula.save(), action_name="submit_sqli_payload")

        with self.step("Step 2: Verify form functions normally and accepts string value"):
            val = curricula.get_field_value(curricula.ID_NUMBER)
            assert val == sqli_payload
            self.step.set_actual("SQLi string safely retained as literal input value")

    def test_tc33_phone_and_unit_maxlength_boundaries(self):
        """TC33: Primary Phone (maxlength 15) and Unit Number (maxlength 9) strictly truncate over-length inputs."""
        curricula = CurriculaTrainerPage(self.page)
        over_length_phone = "12345678901234567890"  # 20 digits
        over_length_unit = "123456789012345"  # 15 digits

        with self.step("Step 1: Enter over-length inputs into phone and unit fields"):
            curricula.open()
            curricula.fill_text(curricula.PRIMARY_PHONE, over_length_phone)
            curricula.fill_text(curricula.UNIT_NUMBER, over_length_unit)

        with self.step("Step 2: Verify inputs are truncated to their exact HTML maxlength"):
            phone_val = curricula.get_field_value(curricula.PRIMARY_PHONE)
            unit_val = curricula.get_field_value(curricula.UNIT_NUMBER)
            assert len(phone_val) == 15, f"Phone should be truncated to 15 chars, got {len(phone_val)}"
            assert len(unit_val) == 9, f"Unit should be truncated to 9 chars, got {len(unit_val)}"
            self.step.set_actual(f"Phone truncated to {len(phone_val)} chars, Unit truncated to {len(unit_val)} chars")

