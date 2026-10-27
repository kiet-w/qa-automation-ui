"""
tests/fs03/fs03-school-user-create/test_atomic_nric.py - Field-Level NRIC Test Suite.
Verifies NRIC format regex, BVA boundaries (8, 9, 10 chars), casing normalization, trimming, and required state.
Traceability: FS-03 §3.2 F02 | TC-FS03-NRIC-001 -> 009
"""
import pytest
from pages.fs03.school_user_create_page import SchoolUserCreatePage


@pytest.mark.tech_ui
class TestSchoolUserNRICField:
    """Field-level verification for NRIC on Create School User component."""

    def test_tc_fs03_nric_001_format_regex_validation(
        self, school_user_page: SchoolUserCreatePage, fs03_data: dict, unique_generator
    ):
        """TC-FS03-NRIC-001: Valid NRIC pattern -> Create succeeds and user is created."""
        nric, email = unique_generator("nric01")
        school_user_page.fill_form(
            nric=nric,
            first_name="Regex",
            last_name="ValidNRIC",
            email=email,
            school_code="",
        )
        school_user_page.click_create()
        school_user_page.wait_for_result_card()
        card_text = school_user_page.get_result_card_text()
        assert nric in card_text, f"Expected NRIC {nric} in result card: {card_text}"
        assert school_user_page.is_result_card_visible(), "User must be created successfully"

    def test_tc_fs03_nric_002_invalid_format_rejection(
        self, school_user_page: SchoolUserCreatePage, fs03_data: dict, unique_generator
    ):
        """TC-FS03-NRIC-002: Invalid format (digits only) -> Create rejected, user NOT created."""
        _, email = unique_generator("nric02")
        school_user_page.fill_form(
            nric="12345678",
            first_name="Invalid",
            last_name="NRICFormat",
            email=email,
            school_code="",
        )
        school_user_page.click_create()
        school_user_page.wait_for_alert()
        alert_texts = school_user_page.get_alert_texts()
        expected_msg = fs03_data["business_rules"]["error_messages"]["validation_failed"]
        assert any(expected_msg.lower() in a.lower() for a in alert_texts), (
            f"Expected validation failure alert '{expected_msg}' in {alert_texts}"
        )
        assert not school_user_page.is_result_card_visible(), "User must NOT be created"

    def test_tc_fs03_nric_003_uppercase_normalization(
        self, school_user_page: SchoolUserCreatePage, fs03_data: dict, unique_generator
    ):
        """TC-FS03-NRIC-003: Lowercase NRIC -> Create succeeds with normalized uppercase username."""
        nric, email = unique_generator("nric03")
        nric_lower = nric.lower()
        school_user_page.fill_form(
            nric=nric_lower,
            first_name="Norm",
            last_name="Uppercase",
            email=email,
            school_code="",
        )
        school_user_page.click_create()
        school_user_page.wait_for_result_card()
        card_text = school_user_page.get_result_card_text()
        assert nric_lower.upper() in card_text, (
            f"Expected uppercase NRIC '{nric_lower.upper()}' in result card: {card_text}"
        )

    def test_tc_fs03_nric_004_whitespace_trimming(
        self, school_user_page: SchoolUserCreatePage, fs03_data: dict, unique_generator
    ):
        """TC-FS03-NRIC-004: Padded whitespace NRIC -> Create succeeds with trimmed NRIC."""
        nric, email = unique_generator("nric04")
        nric_padded = f"   {nric}   "
        school_user_page.fill_form(
            nric=nric_padded,
            first_name="Trim",
            last_name="Spaces",
            email=email,
            school_code="",
        )
        school_user_page.click_create()
        school_user_page.wait_for_result_card()
        card_text = school_user_page.get_result_card_text()
        assert nric in card_text, f"Expected clean trimmed NRIC '{nric}' in result card: {card_text}"

    def test_tc_fs03_nric_005_bva_min_length_8_chars_rejected(
        self, school_user_page: SchoolUserCreatePage, fs03_data: dict, unique_generator
    ):
        """TC-FS03-NRIC-005: 8 chars (Min-1) -> Create rejected, user NOT created."""
        _, email = unique_generator("nric05")
        school_user_page.fill_form(
            nric="S123456A",
            first_name="BVA",
            last_name="EightChars",
            email=email,
            school_code="",
        )
        school_user_page.click_create()
        school_user_page.wait_for_alert()
        alert_texts = school_user_page.get_alert_texts()
        assert any("validation failed" in a.lower() for a in alert_texts)
        assert not school_user_page.is_result_card_visible(), "User must NOT be created"

    def test_tc_fs03_nric_006_bva_max_length_10_chars_rejected(
        self, school_user_page: SchoolUserCreatePage, fs03_data: dict, unique_generator
    ):
        """TC-FS03-NRIC-006: 10 chars (Max+1) -> Create rejected, user NOT created."""
        _, email = unique_generator("nric06")
        school_user_page.fill_form(
            nric="S12345678A",
            first_name="BVA",
            last_name="TenChars",
            email=email,
            school_code="",
        )
        school_user_page.click_create()
        school_user_page.wait_for_alert()
        alert_texts = school_user_page.get_alert_texts()
        assert any("validation failed" in a.lower() for a in alert_texts)
        assert not school_user_page.is_result_card_visible(), "User must NOT be created"

    def test_tc_fs03_nric_007_special_characters_rejected(
        self, school_user_page: SchoolUserCreatePage, fs03_data: dict, unique_generator
    ):
        """TC-FS03-NRIC-007: Special character in NRIC -> Create rejected, user NOT created."""
        _, email = unique_generator("nric07")
        school_user_page.fill_form(
            nric="S1234#67A",
            first_name="Special",
            last_name="CharNRIC",
            email=email,
            school_code="",
        )
        school_user_page.click_create()
        school_user_page.wait_for_alert()
        alert_texts = school_user_page.get_alert_texts()
        assert any("validation failed" in a.lower() for a in alert_texts)
        assert not school_user_page.is_result_card_visible(), "User must NOT be created"

    def test_tc_fs03_nric_008_whitespace_only_disables_create(
        self, school_user_page: SchoolUserCreatePage, fs03_data: dict, unique_generator
    ):
        """TC-FS03-NRIC-008: Whitespace-only NRIC -> Create button disabled, user NOT created."""
        _, email = unique_generator("nric08")
        school_user_page.fill_form(
            nric="         ",
            first_name="Spaces",
            last_name="NRIC",
            email=email,
            school_code="",
        )
        assert school_user_page.is_create_button_disabled(), "Create button must remain disabled"
        assert not school_user_page.is_result_card_visible(), "User must NOT be created"

    def test_tc_fs03_nric_009_missing_field_disables_create(
        self, school_user_page: SchoolUserCreatePage, fs03_data: dict, unique_generator
    ):
        """TC-FS03-NRIC-009: Missing NRIC -> Create button disabled, user NOT created."""
        _, email = unique_generator("nric09")
        school_user_page.fill_form(
            nric="",
            first_name="Missing",
            last_name="NRICField",
            email=email,
            school_code="",
        )
        assert school_user_page.is_create_button_disabled(), "Create button must remain disabled when NRIC is missing"
        assert not school_user_page.is_result_card_visible(), "User must NOT be created when NRIC is missing"
