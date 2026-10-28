"""
tests/fs03/fs03-school-user-create/test_atomic_school_user_validation.py - Error Handling & Field Validation Matrix.

Traceability:
- Specification: FS-03_School_Student_Fee_Management.md §3.2 F02
- Business Rules: BR-R3-04, BR-R3-05, BR-R3-06, BR-R3-12
- Acceptance Criteria: R3-F02-AC01..AC14
- Constitution: AGENTS.md Invariants 1, 2, 3, 4, 5
"""
import pytest
from playwright.sync_api import expect, Page
from pages.fs03.school_user_create_page import SchoolUserCreatePage


@pytest.mark.validation
class TestSchoolUserValidationAndErrorHandling:
    """
    Priority 1 Test Suite: Verification of all Validation rules & Error Handling.
    Covers invalid NRIC format, duplicate email conflict, duplicate NRIC conflict,
    invalid school code, and mandatory fields gatekeeping.
    """

    def test_tc_fs03_val_001_invalid_nric_format_shows_validation_failed(
        self, school_user_page: SchoolUserCreatePage, fs03_data: dict, unique_generator
    ):
        """
        TC-FS03-VAL-001: Verify entering invalid NRIC format triggers 'Validation failed' error alert.
        Traceability: User Rule: "đây là lỗi khi mà nric sai Validation failed"
        """
        _, valid_email = unique_generator("val01")
        invalid_nric = fs03_data["business_rules"]["user_provided_examples"]["invalid_nric"]
        expected_msg = fs03_data["business_rules"]["error_messages"]["validation_failed"]

        school_user_page.fill_form(
            nric=invalid_nric,
            first_name="Invalid",
            last_name="NRICUser",
            email=valid_email,
            school_code="",
        )
        school_user_page.click_create()

        # Wait for error alert and verify exact error text
        school_user_page.wait_for_alert()
        alert_texts = school_user_page.get_alert_texts()

        assert any(expected_msg.lower() in a.lower() for a in alert_texts), (
            f"Expected validation failure alert '{expected_msg}', got: {alert_texts}"
        )
        assert not school_user_page.is_result_card_visible(), (
            "Result card must NOT be displayed when NRIC validation fails"
        )

    def test_tc_fs03_val_002_duplicate_email_error_handling(
        self, school_user_page: SchoolUserCreatePage, fs03_data: dict, unique_generator
    ):
        """
        TC-FS03-VAL-002: Verify duplicate email triggers 'A user with email \'<email>\' already exists.' error alert.
        Traceability: User Rule: "A user with email 'lpokmoppokid@gmail.com' already exists. đã là lỗi khi cùng email"
        """
        unique_nric, _ = unique_generator("val02")
        duplicate_email = fs03_data["business_rules"]["duplicate_email"]

        school_user_page.fill_form(
            nric=unique_nric,
            first_name="Duplicate",
            last_name="EmailCheck",
            email=duplicate_email,
            school_code="",
        )
        school_user_page.click_create()

        # Wait for conflict alert
        school_user_page.wait_for_alert()
        alert_texts = school_user_page.get_alert_texts()
        expected_pattern = f"email '{duplicate_email.lower()}' already exists"

        assert any(expected_pattern in a.lower() for a in alert_texts), (
            f"Expected duplicate email conflict '{expected_pattern}' in alerts: {alert_texts}"
        )
        assert not school_user_page.is_result_card_visible(), (
            "Result card must NOT be displayed when duplicate email conflict occurs"
        )

    def test_tc_fs03_val_003_duplicate_nric_error_handling(
        self, school_user_page: SchoolUserCreatePage, fs03_data: dict, unique_generator
    ):
        """
        TC-FS03-VAL-003: Verify duplicate NRIC/username triggers 'A user with username \'<nric>\' already exists.' error alert.
        Traceability: User Rule: "thông báo lỗi khi mà nric trùng A user with username 'S1234567A' already exists."
        """
        known_nric = fs03_data["business_rules"]["known_existing_nric"]
        _, unique_email = unique_generator("val03")

        school_user_page.fill_form(
            nric=known_nric,
            first_name="Duplicate",
            last_name="NRICCheck",
            email=unique_email,
            school_code="",
        )
        school_user_page.click_create()

        school_user_page.wait_for_alert()
        alert_texts = school_user_page.get_alert_texts()
        expected_pattern = f"username '{known_nric.lower()}' already exists"

        assert any(expected_pattern in a.lower() for a in alert_texts), (
            f"Expected duplicate username conflict '{expected_pattern}' in alerts: {alert_texts}"
        )
        assert not school_user_page.is_result_card_visible(), (
            "Result card must NOT be displayed when duplicate NRIC conflict occurs"
        )

    def test_tc_fs03_val_004_nonexistent_school_code_shows_validation_failed(
        self, school_user_page: SchoolUserCreatePage, fs03_data: dict, unique_generator
    ):
        """
        TC-FS03-VAL-004: Verify non-existent or invalid MOE School Code triggers 'Validation failed' error alert.
        Traceability: FS-03 §3.2 F02; BR-R3-04
        """
        unique_nric, unique_email = unique_generator("val04")
        invalid_school = fs03_data["schools"]["invalid_code"]
        expected_msg = fs03_data["business_rules"]["error_messages"]["validation_failed"]

        school_user_page.fill_form(
            nric=unique_nric,
            first_name="Ada",
            last_name="Lovelace",
            email=unique_email,
            school_code=invalid_school,
        )
        school_user_page.click_create()

        school_user_page.wait_for_alert()
        alert_texts = school_user_page.get_alert_texts()

        assert any(expected_msg.lower() in a.lower() for a in alert_texts), (
            f"Expected validation error '{expected_msg}' in alerts: {alert_texts}"
        )
        assert not school_user_page.is_result_card_visible(), (
            "Result card must NOT be displayed when school code validation fails"
        )

    def test_tc_fs03_val_005_mandatory_fields_gatekeeper_create_disabled(
        self, school_user_page: SchoolUserCreatePage, unique_generator
    ):
        """
        TC-FS03-VAL-005: Verify Create button remains disabled when any mandatory field is missing or whitespace only.
        Traceability: R3-F02-AC03..AC07; ASM-15
        """
        nric, email = unique_generator("val05")

        # 1. Pristine / Empty
        school_user_page.clear_all_fields()
        assert school_user_page.is_create_button_disabled(), "Create button must be disabled when form is empty"

        # 2. Missing NRIC
        school_user_page.fill_form(nric="", first_name="John", last_name="Doe", email=email)
        assert school_user_page.is_create_button_disabled(), "Create button must be disabled when NRIC is missing"

        # 3. Missing First Name
        school_user_page.fill_form(nric=nric, first_name="", last_name="Doe", email=email)
        assert school_user_page.is_create_button_disabled(), "Create button must be disabled when First Name is missing"

        # 4. Missing Last Name
        school_user_page.fill_form(nric=nric, first_name="John", last_name="", email=email)
        assert school_user_page.is_create_button_disabled(), "Create button must be disabled when Last Name is missing"

        # 5. Missing Email
        school_user_page.fill_form(nric=nric, first_name="John", last_name="Doe", email="")
        assert school_user_page.is_create_button_disabled(), "Create button must be disabled when Email is missing"

        # 6. Whitespace only across required fields
        school_user_page.fill_form(nric="   ", first_name="   ", last_name="   ", email="   ")
        assert school_user_page.is_create_button_disabled(), "Create button must be disabled when fields are whitespace only"

    def test_tc_fs03_val_006_reset_button_restores_pristine_validation_state(
        self, school_user_page: SchoolUserCreatePage, fs03_data: dict, unique_generator
    ):
        """
        TC-FS03-VAL-006: Verify Reset button clears all 5 fields and restores disabled button state.
        Traceability: R3-F02-AC09
        """
        nric, email = unique_generator("val06")
        school_code = fs03_data["schools"]["valid_active"]["code"]

        school_user_page.fill_form(
            nric=nric,
            first_name="Reset",
            last_name="Tester",
            email=email,
            school_code=school_code,
        )
        assert not school_user_page.is_create_button_disabled(), "Create button should be enabled with all fields filled"

        school_user_page.click_reset()

        assert school_user_page.get_nric_value() == "", "NRIC input must be cleared"
        assert school_user_page.get_first_name_value() == "", "First Name input must be cleared"
        assert school_user_page.get_last_name_value() == "", "Last Name input must be cleared"
        assert school_user_page.get_email_value() == "", "Email input must be cleared"
        assert school_user_page.get_school_code_value() == "", "MOE School Code input must be cleared"
        assert school_user_page.is_create_button_disabled(), "Create button must be disabled after Reset"
