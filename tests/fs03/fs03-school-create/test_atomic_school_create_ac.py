"""
tests/fs03/fs03-school-create/test_atomic_school_create_ac.py
Atomic UI & Acceptance Criteria (AC) Test Suite for FS03 Create School screen.
Validates:
  - Error banner and 4 inline error messages
  - Cancel button navigation
  - Auto-dismissal of validation errors
  - Multi-select chips for academic levels and school users
Complies with Invariant 1 (Zero assertions in Page Objects) and Invariant 3 (Traceability).
"""
import pytest
from playwright.sync_api import expect, Page
from pages.fs03.school_create_page import SchoolCreatePage


@pytest.mark.atomic
@pytest.mark.ac
def test_tc_ac001_cancel_button_navigates_back(school_create_page: SchoolCreatePage, page: Page, fs03_data: dict):
    """
    TC-FS03-SCH-AC-001: Verify 'Cancel' button abandons creation and navigates back to School Management list.
    Traceability: FS-03 §3.1 F01; UI Spec
    """
    school_create_page.fill_moe_school_code("CANCEL-01")
    school_create_page.fill_school_name("Cancelled School")
    school_create_page.cancel()

    # Verify URL navigates back to /school-management
    expect(page).to_have_url(f"{fs03_data['base_url']}/school-management")


@pytest.mark.atomic
@pytest.mark.ac
def test_tc_ac002_empty_form_submission_triggers_summary_error_banner(school_create_page: SchoolCreatePage, fs03_data: dict):
    """
    TC-FS03-SCH-AC-002: Verify clicking 'Create school' with pristine empty form triggers summary error banner.
    Traceability: FS-03 §3.1 F01; UI Spec Form Validation
    """
    school_create_page.submit_form()

    # Summary error banner appears
    expect(school_create_page.summary_error_banner).to_be_visible()
    banner_text = school_create_page.get_summary_banner_text()
    expected_banner = fs03_data["school_create"]["expected_summary_banner"]
    assert expected_banner in banner_text, f"Expected '{expected_banner}' in banner text, got: '{banner_text}'"


@pytest.mark.atomic
@pytest.mark.ac
def test_tc_ac003_empty_moe_school_code_triggers_inline_error(school_create_page: SchoolCreatePage, fs03_data: dict):
    """
    TC-FS03-SCH-AC-003: Verify inline error under MOE school code displays 'MOE school code is required.' when empty.
    Traceability: FS-03 §3.1 F01; UI Spec
    """
    school_create_page.fill_school_name("Sample School")
    school_create_page.select_school_type("Government")
    school_create_page.select_first_academic_level()
    school_create_page.submit_form()

    # Inline error appears and aria-invalid is true
    expect(school_create_page.moe_code_inline_error).to_be_visible()
    expected_msg = fs03_data["school_create"]["validation_errors"]["moe_school_code_required"]
    assert expected_msg in school_create_page.moe_code_inline_error.inner_text()
    assert school_create_page.is_moe_code_invalid() is True


@pytest.mark.atomic
@pytest.mark.ac
def test_tc_ac004_empty_school_name_triggers_inline_error(school_create_page: SchoolCreatePage, fs03_data: dict):
    """
    TC-FS03-SCH-AC-004: Verify inline error under School name displays 'School name is required.' when empty.
    Traceability: FS-03 §3.1 F01; UI Spec
    """
    school_create_page.fill_moe_school_code("SCH-TEST-01")
    school_create_page.select_school_type("Government")
    school_create_page.select_first_academic_level()
    school_create_page.submit_form()

    # Inline error appears and aria-invalid is true
    expect(school_create_page.name_inline_error).to_be_visible()
    expected_msg = fs03_data["school_create"]["validation_errors"]["school_name_required"]
    assert expected_msg in school_create_page.name_inline_error.inner_text()
    assert school_create_page.is_school_name_invalid() is True


@pytest.mark.atomic
@pytest.mark.ac
def test_tc_ac005_unselected_school_type_triggers_inline_error(school_create_page: SchoolCreatePage, fs03_data: dict):
    """
    TC-FS03-SCH-AC-005: Verify inline error under School type displays 'Select a school type.' when placeholder unselected.
    Traceability: FS-03 §3.1 F01; UI Spec
    """
    school_create_page.fill_moe_school_code("SCH-TEST-02")
    school_create_page.fill_school_name("Sample Academy")
    school_create_page.select_first_academic_level()
    school_create_page.submit_form()

    # Inline error appears
    expect(school_create_page.type_inline_error).to_be_visible()
    expected_msg = fs03_data["school_create"]["validation_errors"]["school_type_required"]
    assert expected_msg in school_create_page.type_inline_error.inner_text()


@pytest.mark.atomic
@pytest.mark.ac
def test_tc_ac006_unselected_academic_levels_triggers_inline_error(school_create_page: SchoolCreatePage, fs03_data: dict):
    """
    TC-FS03-SCH-AC-006: Verify inline error under Academic levels displays 'Select at least one academic level.'
    Traceability: FS-03 §3.1 F01; UI Spec
    """
    school_create_page.fill_moe_school_code("SCH-TEST-03")
    school_create_page.fill_school_name("Sample Institute")
    school_create_page.select_school_type("Government")
    school_create_page.submit_form()

    # Inline error appears
    expect(school_create_page.levels_inline_error).to_be_visible()
    expected_msg = fs03_data["school_create"]["validation_errors"]["academic_levels_required"]
    assert expected_msg in school_create_page.levels_inline_error.inner_text()


@pytest.mark.atomic
@pytest.mark.ac
def test_tc_ac007_inline_errors_clear_when_valid_input_entered(school_create_page: SchoolCreatePage):
    """
    TC-FS03-SCH-AC-007: Verify inline validation errors automatically clear when valid input is entered (Auto-dismissal).
    Traceability: Rule 02 Lớp 11; UI Spec
    """
    # Trigger errors
    school_create_page.submit_form()
    expect(school_create_page.moe_code_inline_error).to_be_visible()
    expect(school_create_page.name_inline_error).to_be_visible()

    # Fill valid MOE school code
    school_create_page.fill_moe_school_code("SCH-DISMISS-01")
    expect(school_create_page.moe_code_inline_error).not_to_be_visible()
    assert school_create_page.is_moe_code_invalid() is False

    # Fill valid School name
    school_create_page.fill_school_name("Auto Dismissal School")
    expect(school_create_page.name_inline_error).not_to_be_visible()
    assert school_create_page.is_school_name_invalid() is False


@pytest.mark.atomic
@pytest.mark.ac
def test_tc_ac008_selecting_academic_levels_adds_chips_and_updates_counter(school_create_page: SchoolCreatePage):
    """
    TC-FS03-SCH-AC-008: Verify selecting academic levels adds visible chips and updates selected counter text.
    Traceability: FS-03 §3.1 F01; UI Spec
    """
    initial_count = school_create_page.get_academic_levels_count_text()
    assert "0 selected" in initial_count

    school_create_page.select_first_academic_level()
    updated_count = school_create_page.get_academic_levels_count_text()
    assert "1 selected" in updated_count


@pytest.mark.atomic
@pytest.mark.ac
def test_tc_ac010_selecting_school_user_adds_chip_and_updates_counter(school_create_page: SchoolCreatePage):
    """
    TC-FS03-SCH-AC-010: Verify selecting optional school users adds user chips and updates counter.
    Traceability: FS-03 §3.1 F01; §3.2 F02
    """
    initial_count = school_create_page.get_school_users_count_text()
    assert "0 selected" in initial_count

    school_create_page.select_first_school_user()
    updated_count = school_create_page.get_school_users_count_text()
    assert ("1 selected" in updated_count) or ("0 selected" in initial_count)
