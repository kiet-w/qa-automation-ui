"""
tests/fs03/fs03-school-user-create/test_atomic_school_user_ac.py - Atomic Acceptance Criteria Test Suite.

Traceability:
- Specification: FS-03_School_Student_Fee_Management.md §3.2 F02
- Test Case Spec: TC_FS03_School_User_Create.md (Trụ Cột 2: Acceptance Criteria AC-001..AC-014)
- Constitution: AGENTS.md Invariants 1, 2, 3, 4, 5
"""
import pytest
from playwright.sync_api import expect, Page
from pages.fs03.school_user_create_page import SchoolUserCreatePage


@pytest.mark.ac
class TestSchoolUserAcceptanceCriteria:
    """Covers User Story Acceptance Criteria for the Single and Bulk School User creation screen."""

    def test_tc_fs03_ac_001_back_to_list_navigation(
        self, school_user_page: SchoolUserCreatePage, fs03_data: dict
    ):
        """TC-FS03-AC-001: Verify 'Back to list' button navigates back to School User Management table."""
        school_user_page.click_back_to_list()
        expect(school_user_page.page).to_have_url(f"{fs03_data['base_url']}/school-user-management")

    def test_tc_fs03_ac_002_single_tab_default_active(
        self, school_user_page: SchoolUserCreatePage, fs03_data: dict
    ):
        """TC-FS03-AC-002: Verify 'Single' tab is selected by default and renders single user creation form."""
        assert school_user_page.is_single_tab_active(), "Expected Single tab to be active by default"
        expect(school_user_page.nric_input).to_be_visible()
        expect(school_user_page.first_name_input).to_be_visible()
        expect(school_user_page.last_name_input).to_be_visible()
        expect(school_user_page.email_input).to_be_visible()
        expect(school_user_page.moe_school_code_input).to_be_visible()

    def test_tc_fs03_ac_003_create_button_disabled_when_empty(
        self, school_user_page: SchoolUserCreatePage
    ):
        """TC-FS03-AC-003: Verify 'Create' button is strictly disabled when form is pristine/empty."""
        assert school_user_page.is_create_button_disabled(), "Create button must be disabled when form is pristine"
        assert not school_user_page.is_result_card_visible(), "User must NOT be created"

    def test_tc_fs03_ac_004_create_button_disabled_missing_nric(
        self, school_user_page: SchoolUserCreatePage, fs03_data: dict
    ):
        """TC-FS03-AC-004: Missing NRIC -> Create button remains disabled, user cannot be created."""
        payload = fs03_data["sample_payloads"]["valid_standalone"]
        school_user_page.fill_first_name(payload["first_name"])
        school_user_page.fill_last_name(payload["last_name"])
        school_user_page.fill_email(f"{payload['email_prefix']}@schools.gov.sg")

        assert school_user_page.is_create_button_disabled(), "Create button must remain disabled when NRIC is missing"
        assert not school_user_page.is_result_card_visible(), "User must NOT be created when NRIC is missing"

    def test_tc_fs03_ac_005_create_button_disabled_missing_first_name(
        self, school_user_page: SchoolUserCreatePage, fs03_data: dict, unique_generator
    ):
        """TC-FS03-AC-005: Missing First Name -> Create button remains disabled, user cannot be created."""
        nric, email = unique_generator("ac05")
        payload = fs03_data["sample_payloads"]["valid_standalone"]
        school_user_page.fill_nric(nric)
        school_user_page.fill_last_name(payload["last_name"])
        school_user_page.fill_email(email)

        assert school_user_page.is_create_button_disabled(), "Create button must remain disabled when First Name is missing"
        assert not school_user_page.is_result_card_visible(), "User must NOT be created when First Name is missing"

    def test_tc_fs03_ac_006_create_button_disabled_missing_last_name(
        self, school_user_page: SchoolUserCreatePage, fs03_data: dict, unique_generator
    ):
        """TC-FS03-AC-006: Missing Last Name -> Create button remains disabled, user cannot be created."""
        nric, email = unique_generator("ac06")
        payload = fs03_data["sample_payloads"]["valid_standalone"]
        school_user_page.fill_nric(nric)
        school_user_page.fill_first_name(payload["first_name"])
        school_user_page.fill_email(email)

        assert school_user_page.is_create_button_disabled(), "Create button must remain disabled when Last Name is missing"
        assert not school_user_page.is_result_card_visible(), "User must NOT be created when Last Name is missing"

    def test_tc_fs03_ac_007_create_button_disabled_missing_email(
        self, school_user_page: SchoolUserCreatePage, fs03_data: dict, unique_generator
    ):
        """TC-FS03-AC-007: Missing Email -> Create button remains disabled, user cannot be created."""
        nric, _ = unique_generator("ac07")
        payload = fs03_data["sample_payloads"]["valid_standalone"]
        school_user_page.fill_nric(nric)
        school_user_page.fill_first_name(payload["first_name"])
        school_user_page.fill_last_name(payload["last_name"])

        assert school_user_page.is_create_button_disabled(), "Create button must remain disabled when Email is missing"
        assert not school_user_page.is_result_card_visible(), "User must NOT be created when Email is missing"

    def test_tc_fs03_ac_008_create_button_enabled_all_4_required_fields(
        self, school_user_page: SchoolUserCreatePage, fs03_data: dict, unique_generator
    ):
        """TC-FS03-AC-008: Fill all 4 required fields without School Code -> Create button enables."""
        nric, email = unique_generator("ac08")
        payload = fs03_data["sample_payloads"]["valid_standalone"]
        school_user_page.fill_form(
            nric=nric,
            first_name=payload["first_name"],
            last_name=payload["last_name"],
            email=email,
            school_code="",
        )
        assert not school_user_page.is_create_button_disabled(), (
            "Create button must be enabled when 4 required fields are populated"
        )

    def test_tc_fs03_ac_009_reset_button_clears_form_and_disables_create(
        self, school_user_page: SchoolUserCreatePage, fs03_data: dict, unique_generator
    ):
        """TC-FS03-AC-009: Reset clears form inputs and restores disabled state on Create button."""
        nric, email = unique_generator("ac09")
        school_user_page.fill_form(
            nric=nric,
            first_name="ResetTestFirst",
            last_name="ResetTestLast",
            email=email,
            school_code=fs03_data["schools"]["valid_active"]["code"],
        )
        assert not school_user_page.is_create_button_disabled()

        school_user_page.click_reset()

        assert school_user_page.get_nric_value() == "", "NRIC input must be cleared"
        assert school_user_page.get_first_name_value() == "", "First Name input must be cleared"
        assert school_user_page.get_last_name_value() == "", "Last Name input must be cleared"
        assert school_user_page.get_email_value() == "", "Email input must be cleared"
        assert school_user_page.get_school_code_value() == "", "School code input must be cleared"
        assert school_user_page.is_create_button_disabled(), "Create button must be re-disabled after reset"
        assert not school_user_page.is_result_card_visible(), "Result card must be dismissed"

    def test_tc_fs03_ac_010_success_toast_notification_rendered(
        self, school_user_page: SchoolUserCreatePage, fs03_data: dict, unique_generator
    ):
        """TC-FS03-AC-010: Valid user creation -> Renders success toast notification."""
        nric, email = unique_generator("ac10")
        school_user_page.fill_form(
            nric=nric,
            first_name="Toast",
            last_name="Tester",
            email=email,
            school_code=fs03_data["schools"]["valid_active"]["code"],
        )
        school_user_page.click_create()

        expect(school_user_page.toasts.first).to_be_visible(timeout=10000)
        toast_texts = school_user_page.get_toast_texts()
        expected_title = fs03_data["acceptance_criteria"]["toast"]["success_title"]
        assert any(expected_title in t for t in toast_texts), (
            f"Expected toast '{expected_title}' in {toast_texts}"
        )

    def test_tc_fs03_ac_011_created_user_result_card_content_and_aria_live(
        self, school_user_page: SchoolUserCreatePage, fs03_data: dict, unique_generator
    ):
        """TC-FS03-AC-011: Valid user creation -> Renders result card with account details and polite aria-live."""
        nric, email = unique_generator("ac11")
        school_user_page.fill_form(
            nric=nric,
            first_name="Polite",
            last_name="AriaTest",
            email=email,
            school_code=fs03_data["schools"]["valid_active"]["code"],
        )
        school_user_page.click_create()

        school_user_page.wait_for_result_card()
        card_text = school_user_page.get_result_card_text()

        expect(school_user_page.result_card).to_have_attribute("aria-live", "polite")
        assert nric in card_text, f"Expected NRIC {nric} in card"
        assert "Polite AriaTest" in card_text, "Expected Full Name in card"
        assert email in card_text, f"Expected Email {email} in card"
        assert fs03_data["schools"]["valid_active"]["name"] in card_text, "Expected School Name in card"

    def test_tc_fs03_ac_012_bulk_csv_tab_content_and_get_template(
        self, school_user_page: SchoolUserCreatePage, fs03_data: dict
    ):
        """TC-FS03-AC-012: Switch to 'Bulk CSV' tab -> Renders bulk upload form and 'Get Template' button."""
        school_user_page.switch_to_bulk_tab()

        assert school_user_page.is_bulk_tab_active(), "Expected Bulk CSV tab to be active"
        expect(school_user_page.get_template_button).to_be_visible()
        expect(school_user_page.file_input).to_be_attached()
        expect(school_user_page.import_button).to_be_visible()

    def test_tc_fs03_ac_013_tab_switching_preserves_form_state(
        self, school_user_page: SchoolUserCreatePage, fs03_data: dict, unique_generator
    ):
        """TC-FS03-AC-013: Tab switching between Single and Bulk preserves form values seamlessly."""
        nric, email = unique_generator("ac13")
        school_user_page.fill_nric(nric)
        school_user_page.fill_email(email)

        school_user_page.switch_to_bulk_tab()
        assert school_user_page.is_bulk_tab_active()

        school_user_page.switch_to_single_tab()
        assert school_user_page.is_single_tab_active()

        assert school_user_page.get_nric_value() == nric, "NRIC value must persist across tab switches"
        assert school_user_page.get_email_value() == email, "Email value must persist across tab switches"

    def test_tc_fs03_ac_014_bulk_csv_import_button_disabled_without_file(
        self, school_user_page: SchoolUserCreatePage
    ):
        """TC-FS03-AC-014: 'Import' button on Bulk CSV tab is disabled when no file is selected."""
        school_user_page.switch_to_bulk_tab()
        assert school_user_page.is_import_button_disabled(), (
            "Import button must remain disabled when no CSV file has been attached"
        )
