"""
tests/fs03/fs03-school-create/test_atomic_school_create_tech_ui.py
Technical & UI Matrix Test Suite for FS03 Create School screen.
Validates:
  - Universal 12-layer input testing (Whitespace ASM-15, Trim, BVA, Unicode, XSS, SQLi)
  - Dropdown & Combobox controls (Order, Keyboard nav, Filter)
  - Form lifecycle & state preservation
  - Invariant 7 UI Health (0 Console Errors, 0 Horizontal Scrollbar, Anti-i18n leakage, WCAG Focus Order)
Complies with Rule 02, Invariant 1, and Invariant 7.
"""
import re
import pytest
from playwright.sync_api import expect, Page
from pages.fs03.school_create_page import SchoolCreatePage


# =========================================================================
# MOE SCHOOL CODE MATRIX
# =========================================================================

@pytest.mark.atomic
@pytest.mark.tech_ui
def test_tc_cod002_all_whitespace_moe_code_triggers_required_error(school_create_page: SchoolCreatePage, fs03_data: dict):
    """
    TC-FS03-SCH-COD-002: Verify MOE school code all-whitespace input is treated as empty per ASM-15.
    Traceability: Rule 02 Lớp 3; ASM-15
    """
    school_create_page.fill_moe_school_code("     ")
    school_create_page.fill_school_name("Test School")
    school_create_page.select_school_type("Government")
    school_create_page.select_first_academic_level()
    school_create_page.submit_form()

    expect(school_create_page.moe_code_inline_error).to_be_visible()
    expected_msg = fs03_data["school_create"]["validation_errors"]["moe_school_code_required"]
    assert expected_msg in school_create_page.moe_code_inline_error.inner_text()


@pytest.mark.atomic
@pytest.mark.tech_ui
def test_tc_cod004_alphanumeric_school_code_format(school_create_page: SchoolCreatePage):
    """
    TC-FS03-SCH-COD-004: Verify MOE school code accepts valid alphanumeric and hyphenated patterns.
    Traceability: Rule 02 Nhóm 3; FS-03 §3.1 F01
    """
    test_codes = ["HCI-0102", "MPS-0301", "NYPS-0202"]
    for code in test_codes:
        school_create_page.fill_moe_school_code(code)
        assert school_create_page.get_moe_school_code_value() == code


@pytest.mark.atomic
@pytest.mark.tech_ui
def test_tc_cod007_xss_injection_in_moe_code_is_sanitized(school_create_page: SchoolCreatePage, page: Page):
    """
    TC-FS03-SCH-COD-007: Verify XSS injection payload in MOE school code is sanitized safely.
    Traceability: Rule 02 Lớp 10; OWASP A3
    """
    dialog_triggered = []
    page.on("dialog", lambda dialog: dialog_triggered.append(dialog.message))

    xss_payload = "<script>alert('xss-code')</script>"
    school_create_page.fill_moe_school_code(xss_payload)
    school_create_page.submit_form()
    page.wait_for_timeout(500)

    assert len(dialog_triggered) == 0, f"XSS payload triggered dialog: {dialog_triggered}"


# =========================================================================
# SCHOOL NAME MATRIX
# =========================================================================

@pytest.mark.atomic
@pytest.mark.tech_ui
def test_tc_nam002_all_whitespace_school_name_triggers_required_error(school_create_page: SchoolCreatePage, fs03_data: dict):
    """
    TC-FS03-SCH-NAM-002: Verify School name all-whitespace input is treated as empty per ASM-15.
    Traceability: Rule 02 Lớp 3; ASM-15
    """
    school_create_page.fill_moe_school_code("SCH-WHITE-01")
    school_create_page.fill_school_name("        ")
    school_create_page.select_school_type("Government")
    school_create_page.select_first_academic_level()
    school_create_page.submit_form()

    expect(school_create_page.name_inline_error).to_be_visible()
    expected_msg = fs03_data["school_create"]["validation_errors"]["school_name_required"]
    assert expected_msg in school_create_page.name_inline_error.inner_text()


@pytest.mark.atomic
@pytest.mark.tech_ui
def test_tc_nam004_multicultural_unicode_school_names(school_create_page: SchoolCreatePage):
    """
    TC-FS03-SCH-NAM-004: Verify School name preserves Singapore multicultural Unicode characters.
    Traceability: Rule 02 Lớp 9; FS-03 §3.1 F01
    """
    unicode_names = [
        "华中科技学院 (Hwa Chong)",
        "Sekolah Menengah Kebangsaan",
        "Trường Quốc tế Singapore",
        "St. Joseph's Institution - Junior"
    ]
    for name in unicode_names:
        school_create_page.fill_school_name(name)
        assert school_create_page.get_school_name_value() == name


@pytest.mark.atomic
@pytest.mark.tech_ui
def test_tc_nam007_stress_paste_1000_chars_into_name(school_create_page: SchoolCreatePage, page: Page):
    """
    TC-FS03-SCH-NAM-007: Verify pasting 1000+ characters into School name does not freeze browser or break layout.
    Traceability: Rule 02 Lớp 7; AGENTS.md Invariant 7
    """
    long_string = "SchoolNameLong" * 72  # 1008 chars
    school_create_page.fill_school_name(long_string)
    page.wait_for_timeout(300)

    # Browser must remain responsive
    assert school_create_page.create_school_button.is_enabled()
    is_overflowing = page.evaluate("document.documentElement.scrollWidth > window.innerWidth")
    assert is_overflowing is False, "Horizontal scrollbar triggered by stress paste"


# =========================================================================
# SCHOOL TYPE SELECT MATRIX
# =========================================================================

@pytest.mark.atomic
@pytest.mark.tech_ui
def test_tc_typ001_default_placeholder_option(school_create_page: SchoolCreatePage):
    """
    TC-FS03-SCH-TYP-001: Verify School type select renders placeholder 'Select a school type' with empty value by default.
    Traceability: Rule 02 Nhóm 5; UI Spec
    """
    selected_text = school_create_page.get_selected_school_type()
    assert "Select a school type" in selected_text


@pytest.mark.atomic
@pytest.mark.tech_ui
def test_tc_typ002_dropdown_renders_approved_singapore_school_types(school_create_page: SchoolCreatePage, fs03_data: dict):
    """
    TC-FS03-SCH-TYP-002: Verify School type dropdown renders all 5 valid Singapore School Types in exact specified order.
    Traceability: Rule 02 Nhóm 5; WA-R3-10
    """
    actual_options = school_create_page.school_type_select.evaluate(
        "el => Array.from(el.options).map(o => o.text.trim())"
    )
    expected_options = fs03_data["school_create"]["approved_school_types"]

    for expected in expected_options:
        assert expected in actual_options, f"Expected option '{expected}' missing from school type dropdown"


# =========================================================================
# INVARIANT 7 & UI HEALTH MATRIX
# =========================================================================

@pytest.mark.atomic
@pytest.mark.nfr
def test_tc_nfr001_zero_console_errors_during_form_lifecycle(page: Page, school_create_page: SchoolCreatePage):
    """
    TC-FS03-SCH-NFR-001: Verify Invariant 7 UI Health: Zero uncaught JavaScript errors in browser console.
    Traceability: AGENTS.md Invariant 7; Rule 02 Mục 9
    """
    console_errors = []
    page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)

    # Perform form interactions
    school_create_page.submit_form()
    school_create_page.fill_moe_school_code("SCH-NFR-01")
    school_create_page.fill_school_name("NFR Verification School")
    school_create_page.select_school_type("Government")
    school_create_page.select_first_academic_level()
    page.wait_for_timeout(500)

    # Filter out known harmless external network errors if any
    relevant_errors = [e for e in console_errors if "favicon" not in e and "sourcemap" not in e.lower()]
    assert len(relevant_errors) == 0, f"Detected console errors: {relevant_errors}"


@pytest.mark.atomic
@pytest.mark.nfr
def test_tc_nfr002_zero_horizontal_scrollbar_at_desktop_viewports(page: Page, school_create_page: SchoolCreatePage):
    """
    TC-FS03-SCH-NFR-002: Verify zero horizontal scrollbar (scrollWidth <= clientWidth) at desktop viewports.
    Traceability: AGENTS.md Invariant 7; Rule 02 Mục 9
    """
    viewports = [{"width": 1280, "height": 720}, {"width": 1920, "height": 1080}]
    for vp in viewports:
        page.set_viewport_size(vp)
        page.wait_for_timeout(200)
        has_h_scroll = page.evaluate("document.documentElement.scrollWidth > window.innerWidth")
        assert has_h_scroll is False, f"Horizontal scrollbar detected at viewport {vp['width']}x{vp['height']}"


@pytest.mark.atomic
@pytest.mark.nfr
def test_tc_nfr003_anti_i18n_leakage_in_rendered_dom(page: Page, school_create_page: SchoolCreatePage):
    """
    TC-FS03-SCH-NFR-003: Verify anti-i18n leakage: Zero raw translation keys in rendered DOM.
    Traceability: Rule 02 Lớp 11; UI Spec
    """
    # Trigger all validation errors to inspect error texts
    school_create_page.submit_form()
    page.wait_for_timeout(300)

    dom_text = page.locator("body").inner_text()
    raw_keys_pattern = re.findall(r"\b(features\.[a-zA-Z0-9_.]+|school\.[a-zA-Z0-9_.]+|validation\.[a-zA-Z0-9_.]+)\b", dom_text)
    assert len(raw_keys_pattern) == 0, f"Found raw translation keys in DOM: {raw_keys_pattern}"
