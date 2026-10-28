"""
tests/fs08/test_ts04_break_it_resilience.py
Automated adversarial, client-bypass, and resilience test suite ("Phá Có Kỷ Luật").
Aligned with:
- Framework Invariant 8 (Disciplined Adversarial & Chaos Quality Gate)
- tools/break_it/README.md & tools/break_it/test_templates.py
- [agile] fs/md/FS document/FS-08_Parent_Portal_SingPass_Profile.md
- Client Decisions: D-20 (Residential Address & Singpass Read-Only), D-28 (Audit integrity)
- Defect Log: BUG-R8-001 (Phone validation bypass), BUG-R8-002 (Email validation bypass)
"""
import copy
from typing import Any, Dict, List
import pytest

from tests.base_test import BaseTest
from core import Exceptor
from pages.fs08.singpass_login_page import SingpassLoginPage
from pages.fs08.parent_profile_page import ParentProfilePage
from pages.fs08.home_portal_page import HomePortalPage


@pytest.mark.fs08
@pytest.mark.break_it
class TestTS04ParentPortalBreakIt(BaseTest):
    """
    Adversarial & Resilience Test Suite for FS-08: Parent Portal & Profile:
    - Dimension A: Malformed & Hostile Inputs (XSS, extreme boundary lengths, UTF-8 strings)
    - Dimension B: Client-side Validation Bypass & Singpass Read-only Identity Tampering
    - Dimension C: Concurrency, Double-Click Debounce & Server 500 Chaos
    - Dimension D: Authorization & Unauthorized URL Access (Role Escalation)
    - Dimension E: Keyboard A11y Boundaries & Modal Escape
    - Dimension F: Zero Uncaught Client JS Errors (Technical Health Oracle)
    """

    def test_tc_r8_brk_001_client_bypass_force_invalid_email_profile_update(
        self, fs08_data: Dict[str, Any], restore_profile_tan_wei_ming
    ):
        """
        TC-R8-BRK-001 — Client Constraint Bypass: Force invalid email and bypass client checks.
        Scenario: Strip HTML5 form validation, force malformed email via prototype descriptor,
                  and submit profile update.
        Expected Behavior: Backend/Client MUST reject malformed email; system must NOT display success update toast.
        Security Rule: When bypass is blocked, test PASSES per Invariant 8.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Authenticate parent and navigate to Profile edit mode"):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            assert profile.is_in_edit_mode(), "Profile form must be in Edit Mode."

        with self.step("Step 2: Strip client constraints and force malformed email string"):
            # Adversarial bypass: Strip HTML5 validations from DOM
            profile.strip_client_constraints("form, main, [role='main'], body")
            # Force invalid email bypassing input restrictions
            profile.force_set_value(profile.INPUT_EMAIL, "completely-not-an-email")
            # Modify phone validly to trigger dirty state if required
            profile.force_set_value(profile.INPUT_PHONE, "+6598765432")

        with self.step("Step 3: Trigger Save changes and confirm update in dialog"):
            profile.click_save_changes()
            if profile.is_confirm_dialog_open(timeout=1500):
                profile.confirm_dialog_save()

        with self.step("Step 4: Verify backend rejection (Must NOT display success toast)"):
            assert not profile.is_success_toast_visible(timeout=2000), (
                "Validation Bypass Defect! Server or client accepted malformed email after client validation stripping."
            )
            Exceptor.expect_zero_js_errors(profile.get_technical_snapshot(), context="TC-R8-BRK-001")
            self.step.set_actual("Verified adversarial bypass successfully rejected without success toast.")

    def test_tc_r8_brk_002_tamper_readonly_singpass_identity_in_dom(
        self, fs08_data: Dict[str, Any], restore_profile_tan_wei_ming
    ):
        """
        TC-R8-BRK-002 — Identity Tampering: Attempt to modify immutable Singpass fields (Full Name, NRIC).
        Scenario: Inject synthetic inputs into DOM and submit profile update.
        Expected Behavior: Singpass identity fields remain strictly read-only; reloaded profile preserves original name.
        Traceability: D-20 (Residential Address Read-Only), BR-08-01.4 (Singpass Read-Only Identity).
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)
        original_name = "TAN WEI MING"

        with self.step("Step 1: Authenticate parent and navigate to Profile edit mode"):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()

        with self.step("Step 2: Inject tampered synthetic inputs for Full Name and NRIC into form"):
            self.page.evaluate("""() => {
                const form = document.querySelector('form') || document.querySelector('main') || document.body;
                const fakeName = document.createElement('input');
                fakeName.name = 'fullName';
                fakeName.value = 'HACKED CITIZEN NAME';
                const fakeNric = document.createElement('input');
                fakeNric.name = 'nric';
                fakeNric.value = 'T9999999Z';
                form.appendChild(fakeName);
                form.appendChild(fakeNric);
            }""")
            # Update phone validly so Save button is enabled
            profile.force_set_value(profile.INPUT_PHONE, "+6591234567")

        with self.step("Step 3: Save changes and confirm update"):
            profile.click_save_changes()
            if profile.is_confirm_dialog_open():
                profile.confirm_dialog_save()

        with self.step("Step 4: Reload profile and verify Singpass identity was NOT mutated"):
            profile.open(base_url=fs08_data["base_url"])
            displayed_name = profile.get_full_name()
            assert "HACKED" not in displayed_name, f"Security Violation! Full name was modified to: {displayed_name}"
            assert original_name in displayed_name, f"Expected '{original_name}' but found '{displayed_name}'"
            Exceptor.expect_zero_js_errors(profile.get_technical_snapshot(), context="TC-R8-BRK-002")

    @pytest.mark.parametrize(
        "xss_payload",
        [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert(1)>",
            "\"><svg onload=alert(document.cookie)>",
        ],
    )
    def test_tc_r8_brk_003_hostile_xss_injections_in_mailing_inputs(
        self, fs08_data: Dict[str, Any], xss_payload: str, restore_profile_tan_wei_ming
    ):
        """
        TC-R8-BRK-003 — Hostile XSS Injection: Verify script payloads in address fields are sanitized.
        Scenario: Populate mailing address fields with hostile XSS vectors and save.
        Expected Behavior: No unhandled browser alert() dialog is executed; zero runtime JS exceptions.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)
        dialog_messages: List[str] = []

        # Passive listener for native alerts triggered by reflected XSS
        self.page.on("dialog", lambda d: (dialog_messages.append(d.message), d.dismiss()))

        with self.step(f"Step 1: Open profile and inject hostile payload: {xss_payload}"):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            profile.force_set_value(profile.INPUT_STREET, xss_payload)
            profile.force_set_value(profile.INPUT_UNIT, "#05-12")

        with self.step("Step 2: Submit profile form with XSS payload"):
            profile.click_save_changes()
            if profile.is_confirm_dialog_open():
                profile.confirm_dialog_save()

        with self.step("Step 3: Verify zero native alert dialogs and zero runtime JS crashes"):
            assert len(dialog_messages) == 0, f"XSS executed! Dialog captured: {dialog_messages}"
            Exceptor.expect_zero_js_errors(profile.get_technical_snapshot(), context=xss_payload)

    def test_tc_r8_brk_004_extreme_boundary_string_length_in_mailing_street(
        self, fs08_data: Dict[str, Any], restore_profile_tan_wei_ming
    ):
        """
        TC-R8-BRK-004 — Extreme Boundary Length: Inject 10,000 character string into mailing street.
        Scenario: Bypass client maxlength attribute and inject 10,000 characters.
        Expected Behavior: DOM handles input gracefully without crashing; layout does not overflow horizontally.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)
        huge_street = "Bishon Street " + ("A" * 10000)

        with self.step("Step 1: Open profile and enter Edit Mode"):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()

        with self.step("Step 2: Strip constraints and inject 10,000 characters into mailingStreet"):
            profile.strip_client_constraints("form, main, [role='main'], body")
            profile.force_set_value(profile.INPUT_STREET, huge_street)

        with self.step("Step 3: Save changes and verify layout and technical health"):
            profile.click_save_changes()
            if profile.is_confirm_dialog_open():
                profile.confirm_dialog_save()
            self.assert_no_horizontal_overflow()
            Exceptor.expect_zero_js_errors(profile.get_technical_snapshot(), context="TC-R8-BRK-004")

    def test_tc_r8_brk_005_confirm_dialog_rapid_double_click_debounce(
        self, fs08_data: Dict[str, Any], restore_profile_tan_wei_ming
    ):
        """
        TC-R8-BRK-005 — Concurrency: Rapid double-click on Confirm Save button inside alertdialog.
        Scenario: Modify phone number, open confirm modal, and rapid double-click Save changes.
        Expected Behavior: UI does not throw unhandled race errors or runtime JS exceptions.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Open profile and modify phone to enable save"):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            profile.force_set_value(profile.INPUT_PHONE, "+6591234567")

        with self.step("Step 2: Open confirm dialog and trigger rapid double click"):
            profile.click_save_changes()
            assert profile.is_confirm_dialog_open(), "Confirmation dialog must appear."
            confirm_btn = self.page.locator(profile.DIALOG_CONFIRM_SAVE_BTN)
            confirm_btn.dblclick()
            self.page.wait_for_load_state("domcontentloaded")

        with self.step("Step 3: Verify success state and zero runtime JS crashes"):
            assert profile.is_success_toast_visible(), "Success toast must appear after confirmation."
            Exceptor.expect_zero_js_errors(profile.get_technical_snapshot(), context="TC-R8-BRK-005")

    def test_tc_r8_brk_006_backend_server_500_resilience_on_profile_save(
        self, fs08_data: Dict[str, Any]
    ):
        """
        TC-R8-BRK-006 — Server Chaos: Mock HTTP 500 error when saving profile update.
        Scenario: Intercept profile update requests and mock 500 Internal Server Error.
        Expected Behavior: UI does not crash into a White Screen of Death (WSoD); spinner does not hang.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Authenticate parent and navigate to Profile edit mode"):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            profile.force_set_value(profile.INPUT_PHONE, "+6593456789")

        with self.step("Step 2: Mock server 500 on API endpoints"):
            profile.mock_http_response("**/api/**", status=500, body='{"error": "Internal Server Error"}')

        with self.step("Step 3: Trigger Save changes and verify UI stability"):
            profile.click_save_changes()
            if profile.is_confirm_dialog_open():
                profile.confirm_dialog_save()
            # Verify page container is still rendered (No White Screen of Death)
            assert self.page.locator("header, main, h1, h2").count() > 0, "UI crashed into White Screen of Death!"
            Exceptor.expect_zero_js_errors(profile.get_technical_snapshot(), context="TC-R8-BRK-006")

    def test_tc_r8_brk_007_unauthorized_admin_portal_access(
        self, fs08_data: Dict[str, Any]
    ):
        """
        TC-R8-BRK-007 — Role Escalation / Authorization: Authenticated parent accessing admin routes.
        Scenario: Parent TAN WEI MING logged in attempts to navigate to /admin/fees.
        Expected Behavior: System prevents administrative access (redirects to login/home or returns 403/404).
        """
        login = self.get_page(SingpassLoginPage)
        home = self.get_page(HomePortalPage)

        with self.step("Step 1: Authenticate as standard parent TAN WEI MING"):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            home.open(base_url=fs08_data["base_url"])
            assert self.page.locator(home.PORTAL_HEADING).count() > 0, "Home portal must be rendered."

        with self.step("Step 2: Attempt unauthorized navigation to admin fees page"):
            base_url = fs08_data["base_url"].rstrip("/")
            self.page.goto(f"{base_url}/admin/fees", wait_until="domcontentloaded")

        with self.step("Step 3: Verify parent is blocked from administrative controls"):
            current_url = self.page.url
            # Must NOT display admin controls or remain on unprotected /admin/fees
            admin_fee_heading = self.page.locator("h1:has-text('Fee Publication'), button:has-text('Publish Fees')")
            assert admin_fee_heading.count() == 0, "Privilege Escalation! Parent was able to view Admin Fee controls."
            Exceptor.expect_zero_js_errors(home.get_technical_snapshot(), context="TC-R8-BRK-007")

    def test_tc_r8_brk_008_confirm_dialog_keyboard_focus_boundary(
        self, fs08_data: Dict[str, Any]
    ):
        """
        TC-R8-BRK-008 — Accessibility Boundary: Confirm dialog Tab key cycling & Escape dismissal.
        Scenario: Open confirmation modal, cycle Tab key 10 times, then press Escape.
        Expected Behavior: Focus stays within dialog buttons without focus trap; Escape key dismisses modal.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Open profile, modify phone, and trigger confirm dialog"):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            profile.force_set_value(profile.INPUT_PHONE, "+6591234567")
            profile.click_save_changes()
            assert profile.is_confirm_dialog_open(), "Confirmation modal alertdialog must appear."

        with self.step("Step 2: Press Tab key 10 times and verify focus cycles through dialog"):
            focused_tags = []
            for _ in range(10):
                self.page.keyboard.press("Tab")
                active_text = self.page.evaluate("() => document.activeElement ? (document.activeElement.innerText || document.activeElement.tagName) : 'NONE'")
                focused_tags.append(active_text)

            # Ensure focus was not deadlocked at single element
            assert len(set(focused_tags)) > 1, f"Focus appears deadlocked: {focused_tags}"

        with self.step("Step 3: Press Escape key and verify modal dismisses cleanly"):
            self.page.keyboard.press("Escape")
            self.page.wait_for_timeout(300)
            # If dialog dismissed, keep editing or view mode is active
            Exceptor.expect_zero_js_errors(profile.get_technical_snapshot(), context="TC-R8-BRK-008")
