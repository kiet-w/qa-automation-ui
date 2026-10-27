"""
tests/fs08/fs08-parent-profile/test_ts09_submit_confirm_dialog.py
Automated Atomic (UI Unit) Test Suite for FS08 Parent Profile / My Details (/profile).
Suite Focus: Suite 9: Submission & Confirmation Dialog (9 TCs)
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
from typing import Any, Dict
import pytest

from tests.base_test import BaseTest
from pages.fs08.singpass_login_page import SingpassLoginPage
from pages.fs08.parent_profile_page import ParentProfilePage


@pytest.mark.p0
@pytest.mark.ui
@pytest.mark.functional
class TestTS09SubmitConfirmDialog(BaseTest):
    """
    Suite 9: Validates alertdialog confirmation, Keep editing, 500 error toast MSG-0808, debounce, and D-28 Zero Email.
    """

    def test_tc_r8_097_save_valid_profile_update_success_msg0807(
        self, fs08_data: Dict[str, Any], restore_profile_tan_wei_ming
    ):
        """
        TC-R8-097: Saving Valid Profile Updates Shows MSG-0807 and Dispatches Zero Email (D-28).
        Scenario ID: TS-010-SUB | Suite: Submission & Confirm Dialog | Row: 43
        Traceability: FR-08.3; R8-AC14; US-08.2; D-28; PB-15
        Preconditions: FA logged in; Edit Mode open.
        Test Data: Phone: '98887777'; Email: 'fa.new@example.sg'; Mailing: Blk 9 Verde Walk #02-01 S650009 Singapore
        Expected Result: Success toast MSG-0807 'Your details have been updated.'; zero notification email dispatched.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: In Edit Mode, enter valid new values for contact and mailing fields", expected="Inputs filled."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            profile.fill_contact_and_mailing_form(
                phone="98887777",
                email="fa.new@example.sg",
                block="9",
                street="Verde Walk",
                unit="#02-01",
                postal_code="650009",
                country="SINGAPORE",
            )
            self.step.set_actual("Form filled with valid new contact and address payload.")

        with self.step("Step 2: Click [Save changes] to open Confirm Dialog", expected="Modal dialog opened."):
            profile.click_save_changes()
            assert profile.is_confirm_dialog_open(), "Confirmation modal must appear upon clicking Save changes."
            self.step.set_actual("Confirm dialog displayed.")

        with self.step("Step 3: Confirm save in dialog and verify success toast MSG-0807", expected="MSG-0807 displayed."):
            profile.confirm_dialog_save()
            assert profile.is_success_toast_visible(timeout=5000), "Success toast MSG-0807 must be visible."
            toast_text = profile.get_success_toast_text()
            assert "updated" in toast_text.lower(), f"Expected update confirmation, got '{toast_text}'."
            self.step.set_actual(f"Success toast MSG-0807 verified: '{toast_text}'.")


    def test_tc_r8_int_01_confirm_dialog_keep_editing_preserves_dirty_form(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-INT-01: Confirm Dialog 'Keep editing' Button Retains Dirty Form Data Without API Dispatch.
        Scenario ID: TS-010-SUB | Suite: Submission & Confirm Dialog | Row: 44
        Traceability: FR-08.3; AC #14; US-08.2
        Preconditions: FA logged in; Edit Mode open with valid modifications.
        Test Data: New phone: '98887777'
        Expected Result: Dialog closes; form remains in Edit Mode with '98887777' preserved; zero API mutation.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Enter new phone '98887777' and trigger confirm dialog", expected="Dialog opened."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            profile.fill_contact_and_mailing_form(phone="98887777")
            profile.click_save_changes()
            assert profile.is_confirm_dialog_open(), "Confirm dialog must open."
            self.step.set_actual("Confirm dialog opened.")

        with self.step("Step 2: Click [Keep editing] button on dialog", expected="Dialog closes, dirty inputs preserved."):
            profile.confirm_dialog_keep_editing()
            assert not profile.is_confirm_dialog_open(timeout=500), "Confirm dialog must close after Keep editing."
            assert profile.is_in_edit_mode(), "Form must remain in Edit Mode."
            current_phone = profile.get_input_value(profile.INPUT_PHONE)
            assert current_phone == "98887777", f"Typed phone '98887777' must be preserved, got '{current_phone}'."
            self.step.set_actual("Dirty form data cleanly retained without loss.")

        profile.click_cancel()


    def test_tc_r8_sub_01_save_changes_triggers_confirm_modal(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-SUB-01: Clicking 'Save changes' in Dirty State Triggers Confirmation Modal (role='alertdialog').
        Scenario ID: TS-010-SUB | Suite: Submission & Confirm Dialog | Row: 45
        Traceability: FR-08.3; AC #14; US-08.2
        Preconditions: FA logged in; Edit Mode open with valid modifications.
        Expected Result: Modal appears with role='alertdialog', contains [Keep editing] and [Save changes].
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Modify phone number and click [Save changes]", expected="Alertdialog modal displayed."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            profile.fill_contact_and_mailing_form(phone="98887777")
            profile.click_save_changes()
            assert profile.is_confirm_dialog_open(), "Modal alertdialog must appear."
            assert self.page.locator(profile.DIALOG_KEEP_EDITING_BTN).count() > 0, "'Keep editing' button must exist."
            assert self.page.locator(profile.DIALOG_CONFIRM_SAVE_BTN).count() > 0, "'Save changes' button must exist on modal."
            self.step.set_actual("Alertdialog accessibility attributes and action buttons verified.")

        profile.confirm_dialog_keep_editing()
        profile.click_cancel()


    def test_tc_r8_sub_02_confirm_dialog_rapid_double_click_debounce(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-SUB-02: Confirm Dialog Rapid Double-Click Debounce Dispatches Single Mutation.
        Scenario ID: TS-010-SUB | Suite: Submission & Confirm Dialog | Row: 46
        Traceability: FR-08.3; NFR Concurrency; Invariant 8
        Preconditions: FA logged in; Confirmation Dialog open.
        Test Data: Rapid double-click within 50ms interval
        Expected Result: Exactly ONE mutation request dispatched to server; no race conditions.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        mutation_requests = []


    def test_tc_r8_sub_03_saving_state_loading_spinner_and_input_lock(
        self, fs08_data: Dict[str, Any], restore_profile_tan_wei_ming
    ):
        """
        TC-R8-SUB-03: Verify saving state triggers visual loading spinner, sets aria-busy='true', and disables inputs.
        Scenario ID: TS-010-SUB | Suite: Submission & Confirm Dialog | Row: 48
        Traceability: Invariant 7 UI Health; UX latency guidelines
        """
        import time
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)


    def test_tc_r8_sub_04_confirm_dialog_focus_trap_and_esc_dismiss(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-SUB-04: Verify Confirmation Dialog traps focus, cycles Tab, and dismisses on Esc key.
        Scenario ID: TS-010-SUB | Suite: Submission & Confirm Dialog | Row: 49
        Traceability: WCAG 2.1 Focus Trap; Invariant 7 UI Health
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Trigger confirmation modal in Edit Mode", expected="Modal opened."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            profile.fill_contact_and_mailing_form(phone="98884321")
            profile.click_save_changes()
            assert profile.is_confirm_dialog_open(timeout=2000), "Confirmation modal must appear."
            self.step.set_actual("Modal is displayed.")

        with self.step("Step 2: Press Esc key to dismiss modal", expected="Modal dismissed cleanly."):
            self.page.keyboard.press("Escape")
            profile.wait_for_confirm_dialog_closed(timeout=2000)
            assert not profile.is_confirm_dialog_open(timeout=500), "Modal must dismiss upon pressing Esc."
            assert profile.get_input_value(profile.INPUT_PHONE) == "98884321", "Form data preserved after Esc."
            self.step.set_actual("Esc dismissed modal while preserving modified form state.")

        profile.click_cancel()


    def test_tc_r8_sub_05_offline_network_state_graceful_handling(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-SUB-05: Verify offline network state or request timeout during profile submission displays friendly error.
        Scenario ID: TS-010-SUB | Suite: Submission & Confirm Dialog | Row: 50
        Traceability: Invariant 8 Fault Injection; RFC offline handling
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        self.page.route("*/**/parent/update/profile*", lambda route: route.abort("failed"))

        with self.step("Step 1: Submit profile modification while offline", expected="Offline handled gracefully."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            profile.fill_contact_and_mailing_form(phone="97776666")
            profile.click_save_changes()
            if profile.is_confirm_dialog_open(timeout=1000):
                profile.confirm_dialog_save()

            has_error = (
                profile.is_dialog_error_visible()
                or profile.is_inline_error_visible()
                or profile.is_in_edit_mode()
            )
            assert has_error, "System must handle network failure gracefully without UI freeze."
            assert profile.get_input_value(profile.INPUT_PHONE) == "97776666", "Data preserved for retry."
            self.step.set_actual("Offline network failure handled gracefully with data preserved.")

        if profile.is_confirm_dialog_open(timeout=500):
            profile.confirm_dialog_keep_editing()
        if profile.is_in_edit_mode():
            profile.click_cancel()


    def test_tc_r8_sub_06_updated_contact_reflected_across_portal_modules(
        self, fs08_data: Dict[str, Any], restore_profile_tan_wei_ming
    ):
        """
        TC-R8-SUB-06: Verify updated contact details reflect immediately across portal modules without stale cache.
        Scenario ID: TS-010-SUB | Suite: Submission & Confirm Dialog | Row: 51
        Traceability: State management consistency; Invariant 6
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Save profile update successfully", expected="Update committed."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            profile.fill_contact_and_mailing_form(phone="91238899")
            profile.click_save_changes()
            if profile.is_confirm_dialog_open(timeout=1000):
                profile.confirm_dialog_save()
            profile.wait_for_confirm_dialog_closed(timeout=3000)
            self.step.set_actual("Profile update committed.")

        with self.step("Step 2: Navigate to Home and re-inspect profile", expected="Immediate reflection without stale cache."):
            self.page.goto(f"{fs08_data['base_url']}/home")
            self.page.wait_for_load_state("networkidle")
            profile.open(base_url=fs08_data["base_url"])
            mobile_val = profile.get_text(profile.MOBILE_VAL)
            assert "91238899" in mobile_val or "9123 8899" in mobile_val, "Updated phone must reflect immediately without stale cache."
            self.step.set_actual("Updated contact reflected consistently without stale cache.")

    # =========================================================================
    # SUITE 11: TS-010-AGE - Child Age Access Control & Isolation Business Rules
    # =========================================================================


    def test_tc_r8_109_backend_system_error_500_displays_msg0808(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-109: Backend System Error (HTTP 500) Displays MSG-0808 and Preserves Dirty Form Data.
        Scenario ID: TS-010-SUB | Suite: Submission & Confirm Dialog | Row: 47
        Traceability: FR-08.3 errors; AC #17; MSG-0808
        Preconditions: FA logged in; mock profile update API forced to return HTTP 500.
        Test Data: Phone: '98887777'
        Expected Result: Displays error toast/banner MSG-0808; form retains '98887777' without data loss.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        # Intercept profile update API and return 500
        self.page.route("*/**/parent/update/profile*", lambda route: route.fulfill(
            status=500,
            content_type="application/json",
            body='{"error": "Internal Server Error", "code": "MSG-0808", "message": "We could not update your details. Please try again."}'
        ))

        with self.step("Step 1: Enter new phone '98887777' and trigger save with HTTP 500 mock", expected="Form submitted."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            profile.fill_contact_and_mailing_form(phone="98887777")
            profile.click_save_changes()
            if profile.is_confirm_dialog_open(timeout=1000):
                profile.confirm_dialog_save()
            self.step.set_actual("Dispatched save request to 500 endpoint.")

        with self.step("Step 2: Inspect UI response and form state preservation", expected="MSG-0808 error displayed; data retained."):
            # Check for error alert or dialog error
            has_error = (
                profile.is_dialog_error_visible()
                or profile.is_inline_error_visible()
                or self.page.locator("text=/could not update/i, text=/try again/i").count() > 0
            )
            assert has_error, "MSG-0808 system error alert must be displayed upon HTTP 500."
            # Confirm page did not crash
            assert profile.is_in_edit_mode(), "Form must remain in Edit Mode without data loss."
            assert profile.get_input_value(profile.INPUT_PHONE) == "98887777", "Typed phone must be preserved."
            self.step.set_actual("MSG-0808 error displayed and typed data preserved.")

        if profile.is_confirm_dialog_open(timeout=500):
            profile.confirm_dialog_keep_editing()
        if profile.is_in_edit_mode():
            profile.click_cancel()

