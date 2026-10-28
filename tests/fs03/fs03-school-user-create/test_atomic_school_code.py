"""
tests/fs03/fs03-school-user-create/test_atomic_school_code.py - Field-Level MOE School Code Test Suite.
Verifies whitespace trimming, optional empty behavior, and invalid code rejection.
Traceability: FS-03 §3.2 F02 | TC-FS03-SCH-001..003
"""
import pytest
from pages.fs03.school_user_create_page import SchoolUserCreatePage


@pytest.mark.tech_ui
class TestSchoolUserSchoolCodeField:
    """Field-level verification for MOE School Code on Create School User component."""

    def test_tc_fs03_sch_001_whitespace_trimming(
        self, school_user_page: SchoolUserCreatePage, fs03_data: dict, unique_generator
    ):
        """TC-FS03-SCH-001: Padded School Code -> Create succeeds, linked to active School."""
        nric, email = unique_generator("sch01")
        school = fs03_data["schools"]["valid_active"]
        padded_code = f"   {school['code']}   "

        school_user_page.fill_form(
            nric=nric,
            first_name="Trim",
            last_name="SchoolCode",
            email=email,
            school_code=padded_code,
        )
        school_user_page.click_create()
        school_user_page.wait_for_result_card()
        card_text = school_user_page.get_result_card_text()
        assert school["name"] in card_text, (
            f"Expected school '{school['name']}' in result card: {card_text}"
        )

    def test_tc_fs03_sch_002_optional_empty_creates_unassigned(
        self, school_user_page: SchoolUserCreatePage, fs03_data: dict, unique_generator
    ):
        """TC-FS03-SCH-002: Optional School Code omitted -> Create succeeds with 'Not assigned'."""
        nric, email = unique_generator("sch02")
        school_user_page.fill_form(
            nric=nric,
            first_name="Unassigned",
            last_name="Standalone",
            email=email,
            school_code="",
        )
        school_user_page.click_create()
        school_user_page.wait_for_result_card()
        card_text = school_user_page.get_result_card_text()
        assert "Not assigned" in card_text, "Expected 'Not assigned' on result card"

    def test_tc_fs03_sch_003_invalid_school_code_rejected(
        self, school_user_page: SchoolUserCreatePage, fs03_data: dict, unique_generator
    ):
        """TC-FS03-SCH-003: Invalid School Code -> Create rejected, user NOT created."""
        nric, email = unique_generator("sch03")
        school_user_page.fill_form(
            nric=nric,
            first_name="Invalid",
            last_name="SchoolCode",
            email=email,
            school_code=fs03_data["schools"]["invalid_code"],
        )
        school_user_page.click_create()
        school_user_page.wait_for_alert()
        alert_texts = school_user_page.get_alert_texts()
        assert any("validation failed" in a.lower() for a in alert_texts)
        assert not school_user_page.is_result_card_visible(), "User must NOT be created"
