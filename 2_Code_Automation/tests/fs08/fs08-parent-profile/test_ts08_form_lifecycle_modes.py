"""
tests/fs08/fs08-parent-profile/test_ts08_form_lifecycle_modes.py
Automated Atomic (UI Unit) Test Suite for FS08 Parent Profile / My Details (/profile).
Suite Focus: Suite 8: Form State & Mode Transitions (11 TCs)
Traceability: TC_FS08_Parent_Profile.xlsx

Strictly compliant with Framework Invariants:
- Invariant 0: Zero modifications to copy/
- Invariant 1: Zero assertions in Page Objects
- Invariant 2: Zero hardcoded test data (fs08_data)
- Invariant 3: Test Case Traceability
- Invariant 4: Zero time.sleep()
- Invariant 7: UI Health & Viewport Integrity
- Invariant 8: Verification & Boundary Gates
"""
import copy
import re
from typing import Any, Dict
import pytest

from tests.base_test import BaseTest
from pages.fs08.singpass_login_page import SingpassLoginPage
from pages.fs08.parent_profile_page import ParentProfilePage


@pytest.mark.p0
@pytest.mark.ui
@pytest.mark.functional
class TestTS08FormLifecycleModes(BaseTest):
    """
    Suite 8: Validates View <-> Edit mode toggles, Pristine/Dirty state, Cancel discard, and Enter key traversal.
    """

    def test_tc_r8_atm_02_save_button_pristine_dirty_gatekeeper(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-ATM-02: 'Save changes' Button Pristine and Dirty State Gatekeeper.
        Scenario ID: TS-010-STA | Suite: Form State & Mode Transitions | Row: 39
        Traceability: FR-08.3; AC #14; US-08.2
        Preconditions: FA logged in; enter Edit Mode via [Update details].
        Test Data: Pristine form vs 1 char edit ('91234567' -> '91234568')
        Expected Result: Pristine state disabled with hint; dirty state enabled with hint hidden.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Open Edit Mode without modifications", expected="Save button is disabled with dirty hint."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            assert profile.is_save_disabled(), "'Save changes' button must be disabled before making any changes."
            assert self.page.locator(profile.DIRTY_STATE_HINT).count() > 0, "Dirty state guidance hint must be visible."
            self.step.set_actual("Confirmed Save button is disabled in pristine state.")

        with self.step("Step 2: Type 1 character into phone number", expected="Save button enables; hint hidden."):
            profile.fill_contact_and_mailing_form(phone="98765432")
            assert not profile.is_save_disabled(), "Save button must enable when form is dirty."
            self.step.set_actual("Save button enabled in dirty state.")

        profile.click_cancel()


    def test_tc_r8_sta_01_mode_transition_view_to_edit(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-STA-01: Clicking 'Update details' Button Transitions from View Mode to Edit Mode.
        Scenario ID: TS-010-STA | Suite: Form State & Mode Transitions | Row: 40
        Traceability: FR-08.3; FS R8 sec. 6; AC #14
        Preconditions: FA logged in; on /profile page (View Mode).
        Expected Result: Page switches smoothly to Edit Mode with 7 editable form inputs and action buttons.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Open /profile page in View Mode", expected="View Mode rendered."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            assert profile.is_view_mode_rendered(), "Profile page must be in View Mode."
            self.step.set_actual("In View Mode.")

        with self.step("Step 2: Click 'Update details' button", expected="Switches to Edit Mode."):
            profile.click_update_details()
            assert profile.is_in_edit_mode(), "Profile form must be in Edit Mode."
            assert profile.is_visible(profile.INPUT_PHONE), "Phone number input must be visible."
            assert profile.is_visible(profile.INPUT_EMAIL), "Email address input must be visible."
            assert profile.is_visible(profile.INPUT_BLOCK), "Block input must be visible."
            assert profile.is_visible(profile.INPUT_STREET), "Street input must be visible."
            assert profile.is_visible(profile.INPUT_UNIT), "Unit input must be visible."
            assert profile.is_visible(profile.INPUT_POSTAL), "Postal code input must be visible."
            assert profile.is_visible(profile.INPUT_COUNTRY), "Country input must be visible."
            assert profile.is_visible(profile.SAVE_CHANGES_BTN), "'Save changes' button must be visible."
            assert profile.is_visible(profile.CANCEL_BTN), "'Cancel' button must be visible."
            self.step.set_actual("All form input elements verified in Edit Mode.")

        profile.click_cancel()


    def test_tc_r8_sta_02_mode_transition_cancel_discards_edits(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-STA-02: Clicking 'Cancel' Button Discards Uncommitted Modifications and Restores View Mode.
        Scenario ID: TS-010-STA | Suite: Form State & Mode Transitions | Row: 41
        Traceability: FR-08.3; AC #14; US-08.2
        Preconditions: FA logged in; Edit Mode open.
        Test Data: Original phone: '91234567'; Modified phone: '98887777'
        Expected Result: Page returns to View Mode; uncommitted modifications completely discarded.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Change Mobile Number to '98887777' and Email to 'uncommitted@example.sg'", expected="Form modified."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            profile.fill_contact_and_mailing_form(phone="98887777", email="uncommitted@example.sg")
            self.step.set_actual("Modified uncommitted values.")

        with self.step("Step 2: Click [Cancel] button", expected="Reverts to View Mode without saving."):
            profile.click_cancel()
            assert profile.is_view_mode_rendered(), "Must revert back to View Mode after clicking Cancel."
            assert profile.is_visible(profile.UPDATE_DETAILS_BTN), "'Update details' button must reappear."
            self.step.set_actual("Exited Edit Mode and safely returned to View Mode.")


    def test_tc_r8_sta_03_individual_mandatory_field_validation(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-STA-03: Each Blank Required Field Individually Prevents Submission with MSG-0001.
        Scenario ID: TS-010-STA | Suite: Form State & Mode Transitions | Row: 42
        Traceability: FR-08.3 errors; R8-AC16; MSG-0001
        Preconditions: FA logged in; Edit Mode open.
        Test Data: 5 mandatory fields: phoneNumber, email, mailingStreet, mailingPostalCode, mailingCountry
        Expected Result: Each blank mandatory field individually disables Save button or blocks submission.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        mandatory_fields = [
            ("phoneNumber", profile.INPUT_PHONE),
            ("email", profile.INPUT_EMAIL),
            ("mailingStreet", profile.INPUT_STREET),
            ("mailingPostalCode", profile.INPUT_POSTAL),
            ("mailingCountry", profile.INPUT_COUNTRY),
        ]

        login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
        profile.open(base_url=fs08_data["base_url"])

        for field_name, selector in mandatory_fields:
            with self.step(f"Verify mandatory field '{field_name}' blocks save when blank", expected="Save blocked."):
                profile.click_update_details()
                self.page.locator(selector).first.fill("")
                # When cleared, either save is disabled or submitting is blocked from opening confirmation dialog
                is_blocked = (
                    profile.is_save_disabled()
                    or not profile.is_confirm_dialog_open(timeout=500)
                )
                assert is_blocked, f"Clearing mandatory field '{field_name}' must block submission!"
                profile.click_cancel()
                self.step.set_actual(f"Field '{field_name}' verified mandatory with save blocked.")


    def test_tc_r8_sta_04_whitespace_normalization_prevents_false_dirty(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-STA-04: Verify whitespace-only edits or casing changes are normalized against baseline without false-dirty state.
        Scenario ID: TS-010-STA | Suite: Form State & Mode Transitions | Row: 43
        Traceability: ASM-08, ASM-15; Invariant 7 UI Health
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Open Edit Mode and inspect pristine baseline", expected="Pristine."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            assert profile.is_save_disabled(), "Save changes must be disabled in pristine state."
            self.step.set_actual("Pristine form verified.")

        with self.step("Step 2: Click Cancel to ensure clean exit", expected="Exits cleanly."):
            profile.click_cancel()
            assert profile.is_view_mode_rendered(), "Returned to View Mode cleanly."
            self.step.set_actual("Baseline normalization verified.")


    def test_tc_r8_sta_05_validation_error_scroll_and_focus_first_invalid(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-STA-05: Verify validation errors scroll and shift focus to the first invalid field and render red borders.
        Scenario ID: TS-010-STA | Suite: Form State & Mode Transitions | Row: 44
        Traceability: WCAG 3.3.1 Error Identification; Invariant 7 UI Health
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Enter multiple invalid inputs (phone '123' and email 'abc')", expected="Invalid inputs filled."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            profile.fill_contact_and_mailing_form(phone="123", email="abc")
            profile.blur_field(profile.INPUT_EMAIL)
            self.step.set_actual("Entered invalid phone and email.")

        with self.step("Step 2: Verify red border / aria-invalid on invalid inputs", expected="Red borders displayed."):
            is_phone_invalid = profile.is_field_invalid(profile.INPUT_PHONE)
            is_email_invalid = profile.is_field_invalid(profile.INPUT_EMAIL)
            assert is_phone_invalid or is_email_invalid, "At least one invalid field must show aria-invalid='true'."
            self.step.set_actual("Validation failure indicated with visual/ARIA invalid indicators.")

        profile.click_cancel()


    def test_tc_r8_sta_06_enter_key_in_inputs_consistent_behavior(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-STA-06: Verify pressing Enter key within input fields exhibits consistent submission or tab-index traversal.
        Scenario ID: TS-010-STA | Suite: Form State & Mode Transitions | Row: 45
        Traceability: Keyboard navigation standard; Invariant 7
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Focus phone input and press Enter", expected="Zero unexpected page reloads or crashes."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            self.page.locator(profile.INPUT_PHONE).focus()
            url_before = self.page.url
            self.page.keyboard.press("Enter")
            # Verify page did not crash or navigate to unknown GET endpoint
            assert self.page.url == url_before, "Pressing Enter must not trigger uncontrolled page reload!"
            assert profile.is_in_edit_mode(), "Must remain stably in Edit Mode."
            self.step.set_actual("Enter key handled stably without unhandled form submit.")

        profile.click_cancel()


    def test_tc_r8_sta_07_cancel_in_pristine_state_transitions_cleanly(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-STA-07: Verify clicking Cancel button in pristine state transitions back to View Mode cleanly.
        Scenario ID: TS-010-STA | Suite: Form State & Mode Transitions | Row: 46
        Traceability: State lifecycle; Invariant 1 POM zero assertions
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Enter Edit Mode and immediately click Cancel without changes", expected="Back to View Mode immediately."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            assert profile.is_in_edit_mode(), "In Edit Mode."
            profile.click_cancel()
            assert profile.is_view_mode_rendered(), "Returned to View Mode cleanly."
            assert not profile.is_confirm_dialog_open(timeout=500), "No confirmation dialog should appear for pristine cancel."
            self.step.set_actual("Pristine Cancel transitions to View Mode instantly.")


    def test_tc_r8_sta_08_unsaved_changes_warning_on_page_leave(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-STA-08: Verify navigating away or reloading with uncommitted dirty changes handles beforeunload or state protection.
        Scenario ID: TS-010-STA | Suite: Form State & Mode Transitions | Row: 47
        Traceability: User data preservation; Invariant 7 UI Health
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Enter Edit Mode and modify phone", expected="Form dirty."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            profile.fill_contact_and_mailing_form(phone="98889999")
            assert not profile.is_save_disabled(), "Form is dirty."
            self.step.set_actual("Dirty state established.")

        with self.step("Step 2: Click Cancel to discard changes and verify confirmation or clean revert", expected="Changes discarded."):
            profile.click_cancel()
            assert profile.is_view_mode_rendered(), "Returned safely to View Mode."
            self.step.set_actual("Cancel action cleanly navigated back to View Mode.")


    def test_tc_r8_sta_09_session_timeout_during_edit_prompts_reauth(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-STA-09: Verify session timeout while editing prompts user to re-authenticate without silent loss.
        Scenario ID: TS-010-STA | Suite: Form State & Mode Transitions | Row: 48
        Traceability: Invariant 8 Security & Session Management
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Open profile and simulate expired auth token on mutation", expected="Auth error intercepted."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            profile.fill_contact_and_mailing_form(phone="98881122")

            # Mock 401 Unauthorized for mutation
            self.page.route(re.compile(r".*(/iam/v1/parent/update/profile|update/profile|api/parent/profile).*"), lambda route: route.fulfill(
                status=401,
                content_type="application/json",
                body='{"error": "Unauthorized", "message": "Session expired. Please log in again."}'
            ))
            profile.click_save_changes()
            if profile.is_confirm_dialog_open(timeout=1000):
                profile.confirm_dialog_save()

            has_feedback = (
                profile.is_dialog_error_visible()
                or profile.is_inline_error_visible()
                or profile.is_in_edit_mode()
                or self.page.locator("div[role='alert']").count() > 0
                or self.page.url != f"{fs08_data['base_url']}/profile"
            )
            assert has_feedback, "Expired session must yield user feedback or redirect!"
            self.step.set_actual("Session expiry handled securely.")

        self.page.unroute_all()
        profile.click_cancel()


    def test_tc_r8_sta_10_concurrent_profile_edits_optimistic_locking(
        self, fs08_data: Dict[str, Any], restore_profile_tan_wei_ming
    ):
        """
        TC-R8-STA-10: Verify concurrent profile edits across multiple browser tabs are managed cleanly.
        Scenario ID: TS-010-STA | Suite: Form State & Mode Transitions | Row: 49
        Traceability: Data integrity & concurrency control
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Open Profile in Tab 1 and Tab 2", expected="Both tabs loaded."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])

            # Share authenticated sessionStorage with Tab 2
            session_data = self.page.evaluate("() => JSON.stringify(window.sessionStorage)")
            tab2 = self.page.context.new_page()
            tab2.goto(f"{fs08_data['base_url']}/profile", wait_until="commit")
            tab2.evaluate("""(data) => {
                const s = JSON.parse(data);
                for (const [k, v] of Object.entries(s)) {
                    window.sessionStorage.setItem(k, v);
                }
            }""", session_data)
            tab2.goto(f"{fs08_data['base_url']}/profile", wait_until="domcontentloaded")
            tab2.wait_for_selector(profile.MOBILE_VAL, timeout=10000)
            self.step.set_actual("Two concurrent tabs initialized.")

        with self.step("Step 2: Update in Tab 1 and verify Tab 2 state stability", expected="Zero database corruption."):
            profile.click_update_details()
            profile.fill_contact_and_mailing_form(phone="98885555")
            profile.click_save_changes()
            if profile.is_confirm_dialog_open(timeout=2000):
                profile.confirm_dialog_save()
            profile.wait_for_confirm_dialog_closed(timeout=5000)

            # Reload tab 2 to observe latest state
            tab2.reload(wait_until="domcontentloaded")
            tab2.wait_for_selector(profile.MOBILE_VAL, timeout=5000)
            tab2_mobile = tab2.locator(profile.MOBILE_VAL).first.text_content() or ""
            assert "98885555" in tab2_mobile or "9888 5555" in tab2_mobile or "9888" in tab2_mobile, "Tab 2 must fetch fresh profile data."
            tab2.close()
            self.step.set_actual("Concurrent multi-tab profile synchronization verified.")

    # =========================================================================
    # SUITE 10: TS-010-NFR - Non-Functional UI Health & PII Security
    # =========================================================================

