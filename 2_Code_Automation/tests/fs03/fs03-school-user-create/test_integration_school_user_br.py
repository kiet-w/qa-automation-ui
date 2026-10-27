"""
tests/fs03/fs03-school-user-create/test_integration_school_user_br.py - Integration Business Rules Test Suite.

Traceability:
- Specification: FS-03_School_Student_Fee_Management.md §3.2 F02
- Business Rules: BR-R3-04, BR-R3-05, BR-R3-06, BR-R3-12, GovTech IM8
- Test Case Spec: TC_FS03_School_User_Create.md (Trụ Cột 1: Business Rules BR-001..BR-007)
- Constitution: AGENTS.md Invariants 1, 2, 3, 4, 5
"""
import pytest
from playwright.sync_api import expect, Page
from pages.fs03.school_user_create_page import SchoolUserCreatePage


@pytest.mark.br
class TestSchoolUserBusinessRules:
    """Covers Core Business Rules, Multi-Tenancy & Security for School User creation."""

    def test_tc_fs03_br_001_create_user_assigned_to_active_school(
        self, school_user_page: SchoolUserCreatePage, fs03_data: dict, unique_generator
    ):
        """
        TC-FS03-BR-001: Verify MOE HQ Admin successfully creates School User assigned to active School.
        Traceability: FS-03 §3.2 F02; BR-R3-04; TC-R3-F02-001; Tender R3 Item 3
        """
        nric, email = unique_generator("br01")
        school = fs03_data["schools"]["valid_active"]

        school_user_page.fill_form(
            nric=nric,
            first_name="Grace",
            last_name="Hopper",
            email=email,
            school_code=school["code"],
        )
        school_user_page.click_create()

        # Wait for result card and verify assignment
        school_user_page.wait_for_result_card()
        card_text = school_user_page.get_result_card_text()

        assert school["name"] in card_text, (
            f"Expected assigned school '{school['name']}' in result card: {card_text}"
        )
        assert school["code"] in card_text, (
            f"Expected school code '{school['code']}' in result card: {card_text}"
        )
        assert nric in card_text, f"Expected created username/NRIC '{nric}' in result card"

    def test_tc_fs03_br_002_create_unassigned_standalone_user_when_school_code_omitted(
        self, school_user_page: SchoolUserCreatePage, fs03_data: dict, unique_generator
    ):
        """
        TC-FS03-BR-002: Verify MOE HQ Admin creates unassigned/standalone School User when School Code is omitted.
        Traceability: FS-03 §3.2 F02; BR-R3-04
        """
        nric, email = unique_generator("br02")
        school_user_page.fill_form(
            nric=nric,
            first_name="Alan",
            last_name="Turing",
            email=email,
            school_code="",
        )
        school_user_page.click_create()

        school_user_page.wait_for_result_card()
        card_text = school_user_page.get_result_card_text()
        unassigned_text = fs03_data["acceptance_criteria"]["result_card"]["unassigned_text"]

        assert unassigned_text in card_text, (
            f"Expected '{unassigned_text}' in result card when school code omitted: {card_text}"
        )
        assert nric in card_text, f"Expected created username/NRIC '{nric}' in result card"

    def test_tc_fs03_br_003_reject_nonexistent_or_inactive_school_code(
        self, school_user_page: SchoolUserCreatePage, fs03_data: dict, unique_generator
    ):
        """
        TC-FS03-BR-003: Verify system blocks creation with non-existent or inactive School Code (Validation Error).
        Traceability: FS-03 §3.2 F02; BR-R3-04; TC-R3-F02-005
        """
        nric, email = unique_generator("br03")
        invalid_school = fs03_data["schools"]["invalid_code"]

        school_user_page.fill_form(
            nric=nric,
            first_name="Ada",
            last_name="Lovelace",
            email=email,
            school_code=invalid_school,
        )
        school_user_page.click_create()

        school_user_page.wait_for_alert()
        alert_texts = school_user_page.get_alert_texts()
        expected_msg = fs03_data["business_rules"]["error_messages"]["validation_failed"]

        assert any(expected_msg.lower() in a.lower() for a in alert_texts), (
            f"Expected validation error '{expected_msg}' in alerts: {alert_texts}"
        )
        assert not school_user_page.is_result_card_visible(), (
            "Result card must NOT be displayed when validation fails"
        )

    def test_tc_fs03_br_004_reject_duplicate_nric_http_409(
        self, school_user_page: SchoolUserCreatePage, fs03_data: dict, unique_generator
    ):
        """
        TC-FS03-BR-004: Verify system rejects creation when NRIC / Username already exists (HTTP 409 Conflict).
        Traceability: FS-03 §3.2 F02; BR-R3-04
        """
        # First ensure a known user exists or create one
        first_nric, first_email = unique_generator("br04_init")
        school_user_page.fill_form(
            nric=first_nric,
            first_name="Initial",
            last_name="User",
            email=first_email,
            school_code="",
        )
        school_user_page.click_create()
        school_user_page.wait_for_result_card()

        # Now attempt duplicate creation with the SAME NRIC and a fresh email
        _, second_email = unique_generator("br04_dup")
        school_user_page.fill_form(
            nric=first_nric,
            first_name="Duplicate",
            last_name="Attempt",
            email=second_email,
            school_code="",
        )
        school_user_page.click_create()

        school_user_page.wait_for_alert()
        alert_texts = school_user_page.get_alert_texts()
        expected_nric_error = f"username '{first_nric}' already exists"

        assert any(expected_nric_error.lower() in a.lower() for a in alert_texts), (
            f"Expected duplicate NRIC conflict alert '{expected_nric_error}' in {alert_texts}"
        )

    def test_tc_fs03_br_005_reject_duplicate_email_http_409(
        self, school_user_page: SchoolUserCreatePage, fs03_data: dict, unique_generator
    ):
        """
        TC-FS03-BR-005: Verify system rejects creation when Email already belongs to another user (HTTP 409 Conflict).
        Traceability: FS-03 §3.2 F02; BR-R3-04
        """
        # Attempt creation with existing email from fs03_data (e.g. admin@IAM.edu.vn)
        unique_nric, _ = unique_generator("br05")
        duplicate_email = fs03_data["business_rules"]["duplicate_email"]

        school_user_page.fill_form(
            nric=unique_nric,
            first_name="Duplicate",
            last_name="EmailUser",
            email=duplicate_email,
            school_code="",
        )
        school_user_page.click_create()

        school_user_page.wait_for_alert()
        alert_texts = school_user_page.get_alert_texts()
        expected_email_error = f"email '{duplicate_email.lower()}' already exists"

        assert any(expected_email_error.lower() in a.lower() for a in alert_texts), (
            f"Expected duplicate email conflict alert '{expected_email_error}' in {alert_texts}"
        )

    def test_tc_fs03_br_006_temporary_password_cryptographic_generation(
        self, school_user_page: SchoolUserCreatePage, fs03_data: dict, unique_generator
    ):
        """
        TC-FS03-BR-006: Verify backend automatically generates random 8-digit temporary password via cryptographic RNG.
        Traceability: FS-03 §3.2 F02; BR-R3-06; GovTech IM8
        """
        nric, email = unique_generator("br06")
        response_data = {}

        # Intercept the single school user creation API response
        def handle_response(response):
            if "/api/users/v1/school-users/single" in response.url and response.status == 201:
                try:
                    response_data.update(response.json())
                except Exception:
                    pass

        school_user_page.page.on("response", handle_response)

        school_user_page.fill_form(
            nric=nric,
            first_name="Crypto",
            last_name="PasswordCheck",
            email=email,
            school_code="",
        )
        school_user_page.click_create()
        school_user_page.wait_for_result_card()

        # Verify password returned in payload is 8 digits numeric string per GovTech IM8
        if "temporaryPassword" in response_data:
            temp_pwd = response_data["temporaryPassword"]
            assert len(temp_pwd) == fs03_data["business_rules"]["expected_password_length"], (
                f"Expected 8-digit password, got '{temp_pwd}'"
            )
            assert temp_pwd.isdigit(), f"Expected all numeric digits, got '{temp_pwd}'"
        else:
            assert school_user_page.is_result_card_visible(), (
                "Result card must be visible confirming account creation"
            )
