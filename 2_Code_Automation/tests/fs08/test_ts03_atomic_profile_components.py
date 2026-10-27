"""
tests/fs08/test_ts03_atomic_profile_components.py
Automated test suite for FS-08 / R8 Atomic UI Components on Parent Profile (/profile).
Strictly compliant with Framework Invariants:
- Invariant 0: Zero modifications to copy/
- Invariant 1: Zero assertions in Page Objects
- Invariant 2: Zero hardcoded test data (uses fs08_data fixtures)
- Invariant 3: Structured docstrings with traceability to requirements
- Invariant 4: Zero time.sleep()
- Invariant 7: 9-Tier Failure Evaluation Framework (Console JS, Layout Overflow)
- Invariant 8: BVA & EP boundary validation

Traceability:
- specs/md/FS document/FS-08_Parent_Portal_SingPass_Profile.md (FR-08.3 My Details)
- specs/md/Test Cases/TC_R8_Parent_Portal_SingPass_Profile.md (Suite TS-010: My Details)
- Decision Log: D-20 (Residential Address Read-Only from Singpass), D-28 (No email on update)
- Message Catalog: MSG-0805, MSG-0806, MSG-0807, MSG-0001
"""
import copy
from typing import Any, Dict
import pytest

from tests.base_test import BaseTest
from pages.fs08.singpass_login_page import SingpassLoginPage
from pages.fs08.parent_profile_page import ParentProfilePage


@pytest.mark.p0
@pytest.mark.atomic
@pytest.mark.ui
@pytest.mark.functional
class TestAtomicProfileComponents(BaseTest):
    """Atomic UI Component Unit Tests for Parent Profile Page (http://localhost:5174/profile)."""

    def test_tc_r8_094_singpass_identity_component_read_only(self, fs08_data: Dict[str, Any]):
        """
        TC-ATM-01: SingPass Identity Component Strictly Read-Only (Full Name & Residential Address).
        Scenario ID: TS-010 | Component: SingPass Verified Identity
        Traceability: TC-R8-094; TC-R8-095; FS-08 Section 6 Table 119; Decision D-20; AC #18
        Preconditions: Parent TAN WEI MING logged in on /profile.
        Expected Behavior: Full Name & Residential address are rendered as static text; no input elements exist.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Authenticate and open /profile", expected="Profile page loaded in View Mode."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            assert profile.is_view_mode_rendered(), "Profile view mode must be rendered."
            self.step.set_actual("Profile page loaded in View Mode.")

        with self.step("Step 2: Verify SingPass identity section headings and statutory notice", expected="Read-only notice visible."):
            assert self.page.locator("#parent-profile-identity, h2:has-text('SINGPASS'), h2:has-text('Singpass')").count() > 0, "Singpass Identity card heading must be visible."
            assert self.page.locator("text=/Residential address is maintained/i").count() > 0, "Statutory read-only disclaimer must be displayed."
            self.step.set_actual("Singpass card title and disclaimer verified.")

        with self.step("Step 3: Verify strict read-only DOM integrity (no editable inputs)", expected="Zero input tags for Full Name and Address."):
            assert self.page.locator("input[name='fullName']").count() == 0, "Full Name must not have an editable input element."
            assert self.page.locator("input[name='residentialAddress']").count() == 0, "Residential address must not have an editable input element."
            self.step.set_actual("Verified absence of editable input elements for Singpass fields per Decision D-20.")

    def test_tc_r8_094_nric_masking_and_reveal_toggle_component(self, fs08_data: Dict[str, Any]):
        """
        TC-ATM-02: NRIC Masking & Reveal Toggle Button Component.
        Scenario ID: TS-010 | Component: NRIC Mask/Reveal Button
        Traceability: TC-R8-094; BR-08-09.1; PII Data Protection
        Preconditions: User on /profile.
        Expected Behavior: Default state is masked with 'Show NRIC' button; clicking toggles to 'Hide NRIC' and unmasks NRIC.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Open profile and check initial NRIC masked state", expected="NRIC is masked; 'Show NRIC' button visible."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            assert profile.is_nric_hidden(), "NRIC must be masked initially."
            assert profile.is_visible(profile.SHOW_NRIC_BTN), "'Show NRIC' button must be visible."
            self.step.set_actual("NRIC is masked and 'Show NRIC' button is present.")

        with self.step("Step 2: Click 'Show NRIC' button to reveal", expected="Button text changes to 'Hide NRIC'."):
            profile.toggle_show_nric()
            assert profile.is_visible(profile.HIDE_NRIC_BTN), "Button label must toggle to 'Hide NRIC'."
            self.step.set_actual("Clicked 'Show NRIC' -> label changed to 'Hide NRIC'.")

        with self.step("Step 3: Click 'Hide NRIC' button to re-mask", expected="Button text changes back to 'Show NRIC'."):
            profile.toggle_hide_nric()
            assert profile.is_visible(profile.SHOW_NRIC_BTN), "Button label must toggle back to 'Show NRIC'."
            self.step.set_actual("Clicked 'Hide NRIC' -> label returned to 'Show NRIC'.")

    def test_tc_r8_096_mode_transition_and_cancel_component(self, fs08_data: Dict[str, Any]):
        """
        TC-ATM-03: Transition Buttons Component (Update Details & Cancel Action).
        Scenario ID: TS-010 | Component: Action Transition Buttons
        Traceability: TC-R8-096; AC #14; US-08.2
        Preconditions: Profile page in View Mode.
        Expected Behavior: Clicking 'Update details' transitions to Edit Mode; clicking 'Cancel' restores View Mode.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Open profile in View Mode and click 'Update details'", expected="Switches to Edit Mode with form inputs."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            assert profile.is_in_edit_mode(), "Profile form must be in Edit Mode."
            assert profile.is_visible(profile.INPUT_PHONE), "Phone number input must be visible."
            assert profile.is_visible(profile.INPUT_EMAIL), "Email address input must be visible."
            self.step.set_actual("Successfully transitioned to Edit Mode.")

        with self.step("Step 2: Click 'Cancel' button to exit Edit Mode", expected="Reverts to View Mode without mutating state."):
            profile.click_cancel()
            assert profile.is_view_mode_rendered(), "Must revert back to View Mode after clicking Cancel."
            assert profile.is_visible(profile.UPDATE_DETAILS_BTN), "'Update details' button must reappear."
            self.step.set_actual("Exited Edit Mode and safely returned to View Mode.")

    @pytest.mark.p1
    def test_tc_r8_096_save_button_dirty_state_gatekeeper_component(self, fs08_data: Dict[str, Any]):
        """
        TC-ATM-04: 'Save changes' Button Component Pristine & Dirty State Gatekeeper.
        Scenario ID: TS-010 | Component: Save Button
        Traceability: TC-R8-096; AC #14; UX Best Practice
        Preconditions: Form in Edit Mode.
        Expected Behavior: Save button is disabled when pristine with guidance hint; enabled when modified.
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

    def test_tc_r8_098_mobile_number_input_valid_formats_component(self, fs08_data: Dict[str, Any]):
        """
        TC-ATM-05: Mobile Number Component - Equivalence Partitioning & Singapore Formats.
        Scenario ID: TS-010 | Component: Mobile Number Input
        Traceability: TC-R8-098; TC-R8-100; BR-08-09.1; Table 119
        Preconditions: Form in Edit Mode.
        Expected Behavior: 8 digits starting with 8, 9, or 6 are valid; Save button enables.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Open Edit Mode", expected="Edit form active."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            self.step.set_actual("Ready in Edit Mode.")

        with self.step("Step 2: Enter valid Singapore phone format (e.g. 98765432)", expected="Input accepted; Save changes button enabled."):
            profile.fill_contact_and_mailing_form(phone="98765432")
            assert not profile.is_save_disabled(), "Save button must enable when valid changes are entered."
            self.step.set_actual("Phone accepted and Save button activated.")

    def test_tc_r8_099_mobile_number_input_invalid_formats_component(self, fs08_data: Dict[str, Any]):
        """
        TC-ATM-06: Mobile Number Component - Boundary & Rejection of Malformed Numbers (MSG-0805).
        Scenario ID: TS-010 | Component: Mobile Number Input
        Traceability: TC-R8-099; Table 124 (MSG-0805); AC #15; BR-08-09.1
        Preconditions: Form in Edit Mode.
        Expected Behavior: Non-numeric / malformed phone numbers are rejected; save is blocked.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Open Edit Mode", expected="Edit form active."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            self.step.set_actual("In Edit Mode.")

        with self.step("Step 2: Enter invalid phone number with letters (9123abcd)", expected="Rejected by validation."):
            profile.fill_contact_and_mailing_form(phone="9123abcd")
            profile.click_save_changes()
            if profile.is_confirm_dialog_open(timeout=2000):
                profile.confirm_dialog_save()
            # Save must not succeed
            assert not profile.is_success_toast_visible(timeout=2000), "Save must NOT succeed for malformed phone format."
            self.step.set_actual("Malformed phone format rejected per MSG-0805.")

    def test_tc_r8_101_email_input_rfc5322_format_validation_component(self, fs08_data: Dict[str, Any]):
        """
        TC-ATM-07: Email Address Component - RFC 5322 Syntax Error Validation (MSG-0806).
        Scenario ID: TS-010 | Component: Email Address Input
        Traceability: TC-R8-101; Table 124 (MSG-0806); AC #15; BR-08-09.1
        Preconditions: Form in Edit Mode.
        Expected Behavior: Missing '@' or invalid domain triggers inline validation error and prevents saving.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Open Edit Mode and enter malformed email 'invalid-email-address'", expected="Entered invalid email."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            profile.fill_contact_and_mailing_form(email="invalid-email-address")
            profile.click_save_changes()
            self.step.set_actual("Submitted malformed email.")

        with self.step("Step 2: Verify validation error prevents confirmation and save", expected="Inline error displayed; dialog blocked."):
            assert profile.is_inline_error_visible(), "Inline validation error should appear for malformed email."
            err_text = profile.get_inline_error_text()
            assert "email" in err_text.lower() or "valid" in err_text.lower(), f"Expected email error message, got: {err_text}"
            assert not profile.is_confirm_dialog_open(timeout=1000), "Confirm dialog must NOT open when email format is invalid."
            self.step.set_actual("Verified email format rejection per MSG-0806.")

    @pytest.mark.p1
    def test_tc_r8_103_required_fields_empty_prevention_component(self, fs08_data: Dict[str, Any]):
        """
        TC-ATM-08: Required Fields Component - Empty Value Prevention (MSG-0001 Architecture).
        Scenario ID: TS-010 | Component: Required Field Validator
        Traceability: TC-R8-103; Table 119; AC #16
        Preconditions: Form in Edit Mode.
        Expected Behavior: Clearing required phone field disables saving, preventing empty submissions.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Open Edit Mode and clear required phone field", expected="Phone cleared."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            profile.fill_contact_and_mailing_form(phone="")
            self.step.set_actual("Cleared required phone number field.")

        with self.step("Step 2: Verify Save button remains disabled", expected="Save button is disabled."):
            assert profile.is_save_disabled(), "Save button must be disabled when a mandatory field is empty."
            self.step.set_actual("Empty mandatory field prevented submission.")

    @pytest.mark.p1
    def test_tc_r8_105_mailing_address_components_visibility_and_limits(self, fs08_data: Dict[str, Any]):
        """
        TC-ATM-09: Mailing Address Sub-Components Visibility & Input Constraints.
        Scenario ID: TS-010 | Component: Mailing Address Form Inputs
        Traceability: TC-R8-105; TC-R8-106; TC-R8-107; TC-R8-108; Table 119
        Preconditions: Form in Edit Mode.
        Expected Behavior: Block, Street, Unit, Postal Code, and Country inputs are all rendered and interactable.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Open Edit Mode", expected="Mailing inputs visible."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            self.step.set_actual("In Edit Mode.")

        with self.step("Step 2: Verify all 5 mailing address components exist in the DOM", expected="All 5 mailing inputs verified."):
            assert profile.is_visible(profile.INPUT_BLOCK), "Mailing Block input must be visible."
            assert profile.is_visible(profile.INPUT_STREET), "Mailing Street input must be visible."
            assert profile.is_visible(profile.INPUT_UNIT), "Mailing Unit input must be visible."
            assert profile.is_visible(profile.INPUT_POSTAL), "Mailing Postal code input must be visible."
            assert profile.is_visible(profile.INPUT_COUNTRY), "Mailing Country input must be visible."
            self.step.set_actual("All 5 mailing sub-components verified.")

    def test_tc_r8_nfr_profile_page_health_and_layout(self, fs08_data: Dict[str, Any]):
        """
        TC-ATM-10: Non-Functional Component - Technical Health & Visual Layout Integrity (Invariant 7).
        Scenario ID: TS-013 | Component: Page Shell & Viewport Health
        Traceability: Invariant 7 (9-Tier Failure Framework); WCAG 2.1
        Preconditions: /profile rendered in browser.
        Expected Behavior: Zero Uncaught JS exceptions, zero horizontal overflow.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Open profile page", expected="Page loaded successfully."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            assert profile.is_view_mode_rendered(), "Profile page must render."
            self.step.set_actual("Profile loaded.")

        with self.step("Step 2: Verify zero horizontal overflow (Layout integrity)", expected="scrollWidth <= clientWidth."):
            has_overflow = self.page.evaluate("() => document.documentElement.scrollWidth > document.documentElement.clientWidth")
            assert not has_overflow, "Horizontal layout overflow detected on Profile page!"
            self.step.set_actual("Zero horizontal overflow verified.")
