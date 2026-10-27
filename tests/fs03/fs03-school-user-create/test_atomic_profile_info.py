"""
tests/fs03/fs03-school-user-create/test_atomic_profile_info.py - Field-Level Names & Email Test Suite.
Verifies First Name, Last Name, and Email validation, Unicode support, case normalization, and required states.
Traceability: FS-03 §3.2 F02 | TC-FS03-FNM-001..004, TC-FS03-LNM-001..003, TC-FS03-EML-001..005
"""
import pytest
from pages.fs03.school_user_create_page import SchoolUserCreatePage


@pytest.mark.tech_ui
class TestSchoolUserProfileInfoFields:
    """Field-level verification for First Name, Last Name, and Email on Create School User component."""

    # =========================================================================
    # FIRST NAME
    # =========================================================================
    def test_tc_fs03_fnm_001_whitespace_only_disables_create(
        self, school_user_page: SchoolUserCreatePage, fs03_data: dict, unique_generator
    ):
        """TC-FS03-FNM-001: All-whitespace First Name -> Create disabled, user NOT created."""
        nric, email = unique_generator("fnm01")
        school_user_page.fill_form(
            nric=nric,
            first_name="     ",
            last_name="LastNameValid",
            email=email,
            school_code="",
        )
        assert school_user_page.is_create_button_disabled(), (
            "Create button must remain disabled when First Name contains only whitespace"
        )
        assert not school_user_page.is_result_card_visible()

    def test_tc_fs03_fnm_002_unicode_multicultural_names(
        self, school_user_page: SchoolUserCreatePage, fs03_data: dict, unique_generator
    ):
        """TC-FS03-FNM-002: Unicode multicultural First Name -> Create succeeds, user created."""
        nric, email = unique_generator("fnm02")
        unicode_first_name = "Nguyễn Văn"
        school_user_page.fill_form(
            nric=nric,
            first_name=unicode_first_name,
            last_name="Minh",
            email=email,
            school_code="",
        )
        school_user_page.click_create()
        school_user_page.wait_for_result_card()
        card_text = school_user_page.get_result_card_text()
        assert unicode_first_name in card_text, (
            f"Expected Unicode name '{unicode_first_name}' preserved in result card: {card_text}"
        )

    def test_tc_fs03_fnm_003_hyphen_apostrophe_punctuation(
        self, school_user_page: SchoolUserCreatePage, fs03_data: dict, unique_generator
    ):
        """TC-FS03-FNM-003: First Name with hyphen/apostrophe -> Create succeeds, user created."""
        nric, email = unique_generator("fnm03")
        punct_name = "Mary-Jane"
        school_user_page.fill_form(
            nric=nric,
            first_name=punct_name,
            last_name="O'Neil",
            email=email,
            school_code="",
        )
        school_user_page.click_create()
        school_user_page.wait_for_result_card()
        card_text = school_user_page.get_result_card_text()
        assert punct_name in card_text, f"Expected '{punct_name}' in result card: {card_text}"

    def test_tc_fs03_fnm_004_missing_field_disables_create(
        self, school_user_page: SchoolUserCreatePage, fs03_data: dict, unique_generator
    ):
        """TC-FS03-FNM-004: Missing First Name -> Create disabled, user NOT created."""
        nric, email = unique_generator("fnm04")
        school_user_page.fill_form(
            nric=nric,
            first_name="",
            last_name="Doe",
            email=email,
            school_code="",
        )
        assert school_user_page.is_create_button_disabled()
        assert not school_user_page.is_result_card_visible()

    # =========================================================================
    # LAST NAME
    # =========================================================================
    def test_tc_fs03_lnm_001_whitespace_only_disables_create(
        self, school_user_page: SchoolUserCreatePage, fs03_data: dict, unique_generator
    ):
        """TC-FS03-LNM-001: All-whitespace Last Name -> Create disabled, user NOT created."""
        nric, email = unique_generator("lnm01")
        school_user_page.fill_form(
            nric=nric,
            first_name="FirstNameValid",
            last_name="      ",
            email=email,
            school_code="",
        )
        assert school_user_page.is_create_button_disabled()
        assert not school_user_page.is_result_card_visible()

    def test_tc_fs03_lnm_002_unicode_multicultural_surnames(
        self, school_user_page: SchoolUserCreatePage, fs03_data: dict, unique_generator
    ):
        """TC-FS03-LNM-002: Unicode surname -> Create succeeds, user created."""
        nric, email = unique_generator("lnm02")
        surname = "Trần"
        school_user_page.fill_form(
            nric=nric,
            first_name="Bảo",
            last_name=surname,
            email=email,
            school_code="",
        )
        school_user_page.click_create()
        school_user_page.wait_for_result_card()
        card_text = school_user_page.get_result_card_text()
        assert surname in card_text, f"Expected surname '{surname}' in result card: {card_text}"

    def test_tc_fs03_lnm_003_missing_field_disables_create(
        self, school_user_page: SchoolUserCreatePage, fs03_data: dict, unique_generator
    ):
        """TC-FS03-LNM-003: Missing Last Name -> Create disabled, user NOT created."""
        nric, email = unique_generator("lnm03")
        school_user_page.fill_form(
            nric=nric,
            first_name="John",
            last_name="",
            email=email,
            school_code="",
        )
        assert school_user_page.is_create_button_disabled()
        assert not school_user_page.is_result_card_visible()

    # =========================================================================
    # EMAIL
    # =========================================================================
    def test_tc_fs03_eml_001_valid_rfc_syntax(
        self, school_user_page: SchoolUserCreatePage, fs03_data: dict, unique_generator
    ):
        """TC-FS03-EML-001: Valid RFC email -> Create succeeds, user created."""
        nric, _ = unique_generator("eml01")
        rfc_email = f"officer.test+sub@{nric.lower()}.schools.gov.sg"
        school_user_page.fill_form(
            nric=nric,
            first_name="RFC",
            last_name="EmailValid",
            email=rfc_email,
            school_code="",
        )
        school_user_page.click_create()
        school_user_page.wait_for_result_card()
        card_text = school_user_page.get_result_card_text()
        assert rfc_email in card_text, f"Expected email '{rfc_email}' in result card: {card_text}"

    def test_tc_fs03_eml_002_invalid_syntax_rejection(
        self, school_user_page: SchoolUserCreatePage, fs03_data: dict, unique_generator
    ):
        """TC-FS03-EML-002: Invalid email syntax without '@' -> Form invalid, user NOT created."""
        nric, _ = unique_generator("eml02")
        school_user_page.fill_form(
            nric=nric,
            first_name="Invalid",
            last_name="EmailFormat",
            email="invalidemaildomain.com",
            school_code="",
        )
        is_valid = school_user_page.email_input.evaluate("el => el.checkValidity()")
        assert not is_valid, "HTML5 email input validity must evaluate to False"
        assert not school_user_page.is_result_card_visible()

    def test_tc_fs03_eml_003_lowercase_normalization(
        self, school_user_page: SchoolUserCreatePage, fs03_data: dict, unique_generator
    ):
        """TC-FS03-EML-003: Uppercase email -> Create succeeds with normalized lowercase email."""
        nric, _ = unique_generator("eml03")
        mixed_email = f"Officer.Alpha_{nric.lower()}@Schools.GOV.SG"
        school_user_page.fill_form(
            nric=nric,
            first_name="Case",
            last_name="Normalizer",
            email=mixed_email,
            school_code="",
        )
        school_user_page.click_create()
        school_user_page.wait_for_result_card()
        card_text = school_user_page.get_result_card_text()
        assert mixed_email.lower() in card_text, (
            f"Expected lowercase email '{mixed_email.lower()}' in result card: {card_text}"
        )

    def test_tc_fs03_eml_004_whitespace_only_disables_create(
        self, school_user_page: SchoolUserCreatePage, fs03_data: dict, unique_generator
    ):
        """TC-FS03-EML-004: All-whitespace Email -> Create disabled, user NOT created."""
        nric, _ = unique_generator("eml04")
        school_user_page.fill_form(
            nric=nric,
            first_name="FirstNameValid",
            last_name="LastNameValid",
            email="       ",
            school_code="",
        )
        assert school_user_page.is_create_button_disabled()
        assert not school_user_page.is_result_card_visible()

    def test_tc_fs03_eml_005_missing_field_disables_create(
        self, school_user_page: SchoolUserCreatePage, fs03_data: dict, unique_generator
    ):
        """TC-FS03-EML-005: Missing Email -> Create disabled, user NOT created."""
        nric, _ = unique_generator("eml05")
        school_user_page.fill_form(
            nric=nric,
            first_name="John",
            last_name="Doe",
            email="",
            school_code="",
        )
        assert school_user_page.is_create_button_disabled()
        assert not school_user_page.is_result_card_visible()
