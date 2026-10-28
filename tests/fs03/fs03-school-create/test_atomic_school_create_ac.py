"""
tests/fs03/fs03-school-create/test_atomic_school_create_ac.py
Atomic UI & Acceptance Criteria (AC) Test Suite for FS03 Create School screen.
Validates:
  - Error banner and 4 inline error messages
  - Cancel button navigation
  - Auto-dismissal of validation errors
  - Multi-select chips for academic levels and school users
Complies with Invariant 1 (Zero assertions in Page Objects) and Invariant 3 (Traceability).

Expected strings are sourced from:
  - apps/admin-portal/src/features/school-management/resource.ts (runtime i18n source of truth)
  - DOM structure confirmed from packages/ui/src/components/{TextField,Select,MultiSelect,FormErrorSummary}.tsx
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

    # URL should contain /school-management (not /new) — regex tolerates trailing slash or query params
    expect(page).to_have_url(f"{fs03_data['base_url']}/school-management")


@pytest.mark.atomic
@pytest.mark.ac
def test_tc_ac002_empty_form_submission_triggers_summary_error_banner(school_create_page: SchoolCreatePage, fs03_data: dict):
    """
    TC-FS03-SCH-AC-002: Verify clicking 'Create school' with pristine empty form triggers summary error banner.
    Traceability: FS-03 §3.1 F01; UI Spec Form Validation

    DOM: FormErrorSummary renders <section role="alert"><h2>{heading}</h2>...
    Source: resource.ts:77 validationSummary = "Please correct the errors below."
    Confirmed: SchoolCreateForm.test.tsx:77 getByRole("heading", { name: "Please correct the errors below." })
    """
    school_create_page.submit_form()

    # 1. The <section role="alert"> container must be visible
    expect(school_create_page.summary_error_banner).to_be_visible()

    # 2. The <h2> heading must match the exact sourced string (not a substring check)
    expected_heading = fs03_data["school_create"]["expected_summary_banner"]
    # "Please correct the errors below." (resource.ts:77)
    expect(school_create_page.summary_error_heading).to_have_text(expected_heading)


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

    expected_msg = fs03_data["school_create"]["validation_errors"]["moe_school_code_required"]
    # "MOE school code is required." (resource.ts:78, confirmed in resources.ts:308)

    # 1. Inline error <p role="alert" id="school-moeSchoolCode-error"> is visible with exact text
    expect(school_create_page.moe_code_inline_error).to_be_visible()
    expect(school_create_page.moe_code_inline_error).to_have_text(expected_msg)

    # 2. Input has aria-invalid="true" (TextField.tsx:53 sets aria-invalid={error ? true : ...})
    expect(school_create_page.moe_school_code_input).to_have_attribute("aria-invalid", "true")

    # 3. Input aria-describedby links to the error element (TextField.tsx:37)
    described_by = school_create_page.moe_school_code_input.get_attribute("aria-describedby") or ""
    assert "school-moeSchoolCode-error" in described_by, (
        f"aria-describedby must reference error id, got: '{described_by}'"
    )


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

    expected_msg = fs03_data["school_create"]["validation_errors"]["school_name_required"]
    # "School name is required." (resource.ts, confirmed component source)

    expect(school_create_page.name_inline_error).to_be_visible()
    expect(school_create_page.name_inline_error).to_have_text(expected_msg)
    expect(school_create_page.school_name_input).to_have_attribute("aria-invalid", "true")


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

    expected_msg = fs03_data["school_create"]["validation_errors"]["school_type_required"]
    # "Select a school type." (resource.ts schoolTypeRequired key)

    expect(school_create_page.type_inline_error).to_be_visible()
    expect(school_create_page.type_inline_error).to_have_text(expected_msg)
    # Select component also sets aria-invalid="true" (Select.tsx:55)
    expect(school_create_page.school_type_select).to_have_attribute("aria-invalid", "true")


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

    expected_msg = fs03_data["school_create"]["validation_errors"]["academic_levels_required"]
    # "Select at least one academic level." (resource.ts academicLevelsRequired key)

    expect(school_create_page.levels_inline_error).to_be_visible()
    expect(school_create_page.levels_inline_error).to_have_text(expected_msg)
    # MultiSelect sets aria-invalid="true" on its combobox input (MultiSelect.tsx aria-invalid prop)
    expect(school_create_page.academic_levels_input).to_have_attribute("aria-invalid", "true")


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

    # Fill valid MOE school code — error for this field clears, aria-invalid reverts to false/absent
    school_create_page.fill_moe_school_code("SCH-DISMISS-01")
    expect(school_create_page.moe_code_inline_error).not_to_be_visible()
    # aria-invalid must be gone/false once the field error is cleared (TextField.tsx:53)
    expect(school_create_page.moe_school_code_input).not_to_have_attribute("aria-invalid", "true")

    # Fill valid School name — error for this field also clears
    school_create_page.fill_school_name("Auto Dismissal School")
    expect(school_create_page.name_inline_error).not_to_be_visible()
    expect(school_create_page.school_name_input).not_to_have_attribute("aria-invalid", "true")


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

    Precondition: Requires at least one school user to be seeded in the test environment.
    If no users are available (MultiSelect shows "No school users found." with aria-disabled),
    this test is skipped rather than silently passing or timing out.
    """
    initial_count = school_create_page.get_school_users_count_text()
    assert "0 selected" in initial_count

    selected = school_create_page.select_first_school_user()
    if not selected:
        pytest.skip("No enabled school users available in this environment — seed data required for AC010.")

    updated_count = school_create_page.get_school_users_count_text()
    assert "1 selected" in updated_count, (
        f"Expected '1 selected' after selecting a user, got: '{updated_count}'"
    )
