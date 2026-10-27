"""
tests/fs03/fs03-school-user-create/test_atomic_security_nfr.py - Security, Stress & UI Health Test Suite.
Verifies XSS sanitization, SQL injection safety, stress input handling, console errors, scrollbars, i18n, and responsive viewport.
Traceability: FS-03 §3.2 F02 | TC-FS03-SEC-001..002, TC-FS03-STR-001, TC-FS03-NFR-001..005
"""
import re
import pytest
from playwright.sync_api import expect
from pages.fs03.school_user_create_page import SchoolUserCreatePage


@pytest.mark.tech_ui
class TestSchoolUserSecurityAndNFR:
    """Security, Stress, and Non-Functional Requirements verification for Create School User."""

    # =========================================================================
    # COMPONENT SECURITY & STRESS (OWASP A3)
    # =========================================================================
    def test_tc_fs03_sec_001_xss_sanitization(
        self, school_user_page: SchoolUserCreatePage, fs03_data: dict, unique_generator
    ):
        """TC-FS03-SEC-001: XSS script injection -> Escaped safely, no dialog, user created safely."""
        nric, email = unique_generator("sec01")
        xss_payload = "<script>alert('xss')</script>"
        dialog_triggered = False

        def on_dialog(dialog):
            nonlocal dialog_triggered
            dialog_triggered = True
            dialog.dismiss()

        school_user_page.page.on("dialog", on_dialog)
        school_user_page.fill_form(
            nric=nric,
            first_name=xss_payload,
            last_name="SanitizationCheck",
            email=email,
            school_code="",
        )
        school_user_page.click_create()
        school_user_page.wait_for_result_card()
        card_text = school_user_page.get_result_card_text()

        assert not dialog_triggered, "XSS script alert dialog must NEVER be triggered"
        assert xss_payload in card_text, "XSS payload must be rendered safely as literal text"

    def test_tc_fs03_sec_002_sqli_safety(
        self, school_user_page: SchoolUserCreatePage, fs03_data: dict, unique_generator
    ):
        """TC-FS03-SEC-002: SQL injection string -> Handled safely as literal text, user created."""
        nric, email = unique_generator("sec02")
        sqli_payload = "' OR 1=1 --"
        school_user_page.fill_form(
            nric=nric,
            first_name=sqli_payload,
            last_name="SQLiCheck",
            email=email,
            school_code="",
        )
        school_user_page.click_create()
        school_user_page.wait_for_result_card()
        card_text = school_user_page.get_result_card_text()
        assert sqli_payload in card_text, "SQL injection string must be handled safely as literal text"

    def test_tc_fs03_str_001_stress_paste_1000_chars(
        self, school_user_page: SchoolUserCreatePage, fs03_data: dict, unique_generator
    ):
        """TC-FS03-STR-001: Paste 1000 chars into text field -> Handled without crashing."""
        stress_text = "A" * 1000
        school_user_page.fill_first_name(stress_text)
        val = school_user_page.get_first_name_value()
        assert len(val) > 0, "Input should accept pasted text without crashing"
        assert school_user_page.create_button.is_visible(), "Page must remain responsive"

    # =========================================================================
    # COMPONENT UI HEALTH & NFR (INVARIANT 7 & WCAG)
    # =========================================================================
    def test_tc_fs03_nfr_001_zero_console_errors(
        self, school_user_page: SchoolUserCreatePage, fs03_data: dict, unique_generator
    ):
        """TC-FS03-NFR-001: Zero uncaught JavaScript errors in browser console during page lifecycle."""
        nric, email = unique_generator("nfr01")
        school_user_page.fill_form(
            nric=nric,
            first_name="Console",
            last_name="ErrorCheck",
            email=email,
            school_code="",
        )
        school_user_page.click_reset()

        tech_snapshot = school_user_page.get_technical_snapshot()
        console_errors = tech_snapshot["console_errors"]
        critical_errors = [e for e in console_errors if "401" not in e and "favicon" not in e]
        assert len(critical_errors) == 0, f"Expected 0 uncaught console errors, found: {critical_errors}"

    def test_tc_fs03_nfr_002_zero_horizontal_scrollbar(
        self, school_user_page: SchoolUserCreatePage
    ):
        """TC-FS03-NFR-002: Zero horizontal scrollbar at desktop viewports."""
        has_hscroll = school_user_page.page.evaluate(
            "() => document.documentElement.scrollWidth > window.innerWidth"
        )
        assert not has_hscroll, "No horizontal scrollbar allowed at desktop viewport"

    def test_tc_fs03_nfr_003_anti_i18n_leakage(
        self, school_user_page: SchoolUserCreatePage
    ):
        """TC-FS03-NFR-003: Zero raw translation keys (features.*, *.undefined) rendered in DOM."""
        body_text = school_user_page.page.locator("body").inner_text()
        raw_key_matches = re.findall(
            r"(features\.[a-zA-Z0-9_.]+|validation\.[a-zA-Z0-9_.]+|\w+\.undefined)",
            body_text,
        )
        assert len(raw_key_matches) == 0, (
            f"Detected raw i18n translation key leakages in rendered UI: {raw_key_matches}"
        )

    def test_tc_fs03_nfr_004_keyboard_navigation_tab_order(
        self, school_user_page: SchoolUserCreatePage
    ):
        """TC-FS03-NFR-004: Logical keyboard Tab navigation order through input fields."""
        school_user_page.nric_input.focus()
        assert school_user_page.page.evaluate("() => document.activeElement.id") == "school-user-nric"

        school_user_page.page.keyboard.press("Tab")
        assert school_user_page.page.evaluate("() => document.activeElement.id") == "school-user-first-name"

        school_user_page.page.keyboard.press("Tab")
        assert school_user_page.page.evaluate("() => document.activeElement.id") == "school-user-last-name"

        school_user_page.page.keyboard.press("Tab")
        assert school_user_page.page.evaluate("() => document.activeElement.id") == "school-user-email"

        school_user_page.page.keyboard.press("Tab")
        assert school_user_page.page.evaluate("() => document.activeElement.id") == "school-user-moe-school-code"

    def test_tc_fs03_nfr_005_tablet_viewport_responsiveness(
        self, school_user_page: SchoolUserCreatePage
    ):
        """TC-FS03-NFR-005: Responsive layout adapts cleanly to tablet viewport (768x1024)."""
        school_user_page.page.set_viewport_size({"width": 768, "height": 1024})
        expect(school_user_page.nric_input).to_be_visible()
        expect(school_user_page.create_button).to_be_visible()
        expect(school_user_page.reset_button).to_be_visible()
        has_hscroll = school_user_page.page.evaluate(
            "() => document.documentElement.scrollWidth > window.innerWidth"
        )
        assert not has_hscroll, "No horizontal overflow permitted at tablet 768px viewport"
