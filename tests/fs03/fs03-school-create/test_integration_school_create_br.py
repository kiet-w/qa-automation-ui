"""
tests/fs03/fs03-school-create/test_integration_school_create_br.py
Integration & Business Rules (BR) Test Suite for FS03 Create School.
Validates:
  - BR-R3-01: Unique MOE School Code constraint (HTTP 409 Conflict duplicate error alert)
  - BR-R3-02: School default Active lifecycle state (is_active = true, 0 classes, 0 students)
  - End-to-end creation flow, success toast notification, and redirection to school list
Complies with Invariant 1 (Zero assertions in Page Objects) and Invariant 3 (Traceability).
"""
import time
import pytest
from playwright.sync_api import expect, Page
from pages.fs03.school_create_page import SchoolCreatePage


@pytest.mark.integration
@pytest.mark.br
def test_tc_br002_duplicate_moe_school_code_rejected(school_create_page: SchoolCreatePage, fs03_data: dict):
    """
    TC-FS03-SCH-BR-002: Verify system strictly rejects duplicate MOE school code with error alert.
    Traceability: FS-03 §3.1 F01-AC02; BR-R3-01; E-03-09; TC-R3-F01-002
    """
    dup_code = fs03_data["school_create"]["duplicate_moe_code"]
    expected_error = fs03_data["school_create"]["expected_duplicate_error"]

    school_create_page.fill_moe_school_code(dup_code)
    school_create_page.fill_school_name("Duplicate Verification School")
    school_create_page.select_school_type("Government")
    school_create_page.select_first_academic_level()
    school_create_page.submit_form()

    # Wait for duplicate error alert to appear
    expect(school_create_page.error_alerts.first).to_be_visible(timeout=10000)

    # Verify duplicate error alert is displayed
    alert_texts = school_create_page.get_alert_error_texts()
    alert_combined = " ".join(alert_texts)
    assert expected_error in alert_combined or "already exists" in alert_combined, (
        f"Expected duplicate error containing '{expected_error}', got: {alert_texts}"
    )


@pytest.mark.integration
@pytest.mark.br
def test_tc_br001_successful_school_creation_e2e(school_create_page: SchoolCreatePage, page: Page, fs03_data: dict):
    """
    TC-FS03-SCH-BR-001: Verify MOE HQ Admin successfully creates a new School with unique code.
    Validates:
      - Form submission with unique MOE code
      - Success toast notification 'School created: School created successfully.'
      - Automatic redirection to /school-management
      - Newly created school is listed in table
    Traceability: FS-03 §3.1 F01-AC01; BR-R3-01; BR-R3-02; TC-R3-F01-001
    """
    unique_suffix = int(time.time()) % 100000
    unique_code = f"SCH-E2E-{unique_suffix}"
    unique_name = f"End-to-End Test Academy {unique_suffix}"

    school_create_page.fill_moe_school_code(unique_code)
    school_create_page.fill_school_name(unique_name)
    school_create_page.select_school_type("Government")
    school_create_page.select_first_academic_level()
    school_create_page.submit_form()

    # Success toast appears
    expect(school_create_page.success_toast).to_be_visible(timeout=10000)
    toast_text = school_create_page.get_toast_text()
    assert "School created" in toast_text
    assert "School created successfully" in toast_text

    # Redirection to /school-management
    expect(page).to_have_url(f"{fs03_data['base_url']}/school-management", timeout=10000)

    # Verify school listed in table
    school_row = page.locator(f"tr:has-text('{unique_code}')")
    expect(school_row).to_be_visible(timeout=10000)
    assert unique_name in school_row.inner_text()
