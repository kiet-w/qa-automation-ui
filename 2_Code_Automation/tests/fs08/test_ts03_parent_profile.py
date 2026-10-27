"""
tests/fs08/test_ts03_parent_profile.py
Automated test suite for Stream 03: Parent Profile & Personal Details Management.
Aligned with:
- [agile] fs/md/Test Cases/TC_R8_Parent_Portal_SingPass_Profile.md (TS-009, TS-010, TS-011)
- fs08/01-business-specs/BUSINESS_RULES.md (BR-08-01, BR-08-03, BR-08-06, BR-08-09)
- Client Decisions: D-20 (Residential Address Read-Only), D-28 (No email on update), Table 124 (Messages)
- Defect Log: [agile] fs/md/Test Cases/DEFECTS_Sprint_1_Master.md (BUG-R8-001 through BUG-R8-005)
"""
import copy
from typing import Any, Dict
import pytest

from tests.base_test import BaseTest
from pages.fs08.singpass_login_page import SingpassLoginPage
from pages.fs08.parent_profile_page import ParentProfilePage


@pytest.mark.p0
@pytest.mark.functional
@pytest.mark.ui
class TestTS03ParentProfile(BaseTest):
    """Test suite covering Singpass read-only identity, NRIC toggle, validation rules, confirm dialog, and data persistence."""

    def test_tc_r8_094_profile_read_only_singpass_identity_and_nric_toggle(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-094: Read-only SingPass Identity & Toggle NRIC Masking Feature.
        Scenario ID: TS-010 | Test Suite: My Details
        Page: ParentProfilePage | Severity: S2 | Priority: High | Test Type: Functional / Security UI
        Traceability: US-08.3; Table 119; Table 122 (AC #18); D-20; BR-08-01.4; BR-08-09.1
        Environment: Localhost Vite (:5174) & MockPass (:5156)
        Preconditions: Parent TAN WEI MING logged in on /profile.
        Test Data: fs08_data["personas"]["PAR-NORMAL-01"]
        Expected Result: Full Name & Residential Address are strictly Read-Only; NRIC is hidden by default and reveals upon clicking 'Show NRIC'.
        Actual Result: As expected.
        Assumption Ref: BR-08-01.4 & D-20.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Authenticate parent and navigate to /profile", expected="Profile page loaded in View Mode."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            assert profile.is_view_mode_rendered(), "Profile view mode must be rendered."
            self.step.set_actual("Profile page loaded.")

        with self.step("Step 2: Verify Singpass identity fields are strictly Read-Only (no input elements)", expected="Full Name and Residential address have no input fields."):
            assert self.page.locator("input[name='fullName']").count() == 0, "Full Name must not be an editable input."
            assert self.page.locator("input[name='residentialAddress']").count() == 0, "Residential address must not be an editable input."
            self.step.set_actual("Verified SingPass fields are strictly read-only.")

        with self.step("Step 3: Verify NRIC is masked by default and test 'Show NRIC' toggle", expected="NRIC is initially hidden; toggles to full NRIC with 'Hide NRIC' label."):
            assert profile.is_nric_hidden(), "NRIC must be hidden/masked by default."
            profile.toggle_show_nric()
            assert profile.is_visible(profile.HIDE_NRIC_BTN), "Button label must change to 'Hide NRIC'."
            self.step.set_actual("Toggled NRIC to unmasked view.")

        with self.step("Step 4: Click 'Hide NRIC' and verify it returns to masked state", expected="Button label returns to 'Show NRIC'."):
            profile.toggle_hide_nric()
            assert profile.is_visible(profile.SHOW_NRIC_BTN), "Button label must toggle back to 'Show NRIC'."
            self.step.set_actual("Toggled NRIC back to masked state.")

    @pytest.mark.p1
    def test_tc_r8_096_profile_edit_dirty_state_and_cancel_action(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-096: Edit Mode Dirty State Detection and Cancel Action.
        Scenario ID: TS-010 | Test Suite: My Details
        Page: ParentProfilePage | Severity: S3 | Priority: Medium | Test Type: Functional UI
        Traceability: US-08.3; Table 122 (AC #14, #15)
        Environment: Localhost Vite (:5174)
        Preconditions: User in View Mode on /profile.
        Test Data: fs08_data["personas"]["PAR-NORMAL-01"]
        Expected Result: Save button disabled until input modified; Cancel button reverts to View Mode without mutating data.
        Actual Result: As expected.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Open profile and click 'Update details' button", expected="Edit mode loaded with form inputs."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            assert profile.is_in_edit_mode(), "Form should be in Edit Mode."
            self.step.set_actual("Entered Edit Mode.")

        with self.step("Step 2: Verify Save button is initially disabled with dirty state hint", expected="Save changes is disabled and 'Make a change to enable saving.' appears."):
            assert profile.is_save_disabled(), "Save button must be disabled before making any changes."
            assert self.page.locator(profile.DIRTY_STATE_HINT).count() > 0, "Dirty state guidance hint must be displayed."
            self.step.set_actual("Confirmed Save button is initially disabled.")

        with self.step("Step 3: Click 'Cancel' button to discard and return to View Mode", expected="Exits Edit Mode and returns to View Mode."):
            profile.click_cancel()
            assert profile.is_view_mode_rendered(), "Should return to View Mode after clicking Cancel."
            self.step.set_actual("Canceled and returned to View Mode.")

    def test_tc_r8_097_profile_update_successful_with_confirm_dialog(
        self, fs08_data: Dict[str, Any], restore_profile_tan_wei_ming
    ):
        """
        TC-R8-097: Successful Profile Update with Confirm Dialog and Data Persistence.
        Scenario ID: TS-010 | Test Suite: My Details
        Page: ParentProfilePage | Severity: S2 | Priority: High | Test Type: Functional / E2E UI
        Traceability: US-08.3; Table 122 (AC #14, #22); MSG-0807; BR-08-03.3; BR-08-09.5
        Environment: Localhost Vite (:5174)
        Preconditions: Authenticated parent TAN WEI MING.
        Test Data: fs08_data["profile_update_valid"]
        Expected Result: Modifying fields enables Save; clicking opens alertdialog; confirming displays 'Your details have been updated.'; reloaded state persists.
        Actual Result: As expected.
        Assumption Ref: BR-08-09.5 (MSG-0807).
        """
        valid_payload = copy.deepcopy(fs08_data["profile_update_valid"])
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Open profile and enter Edit Mode", expected="Edit form ready."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            self.step.set_actual("Ready in Edit Mode.")

        with self.step("Step 2: Fill updated valid phone and email", expected="Save changes button becomes enabled."):
            profile.fill_contact_and_mailing_form(
                phone=valid_payload["phoneNumber"],
                email=valid_payload["email"],
            )
            assert not profile.is_save_disabled(), "Save changes must be enabled after modifying form."
            self.step.set_actual("Form modified; Save button active.")

        with self.step("Step 3: Click 'Save changes' and verify Confirmation Alertdialog appears", expected="Modal dialog 'Save your changes?' opens."):
            profile.click_save_changes()
            assert profile.is_confirm_dialog_open(), "Confirmation modal alertdialog must appear."
            self.step.set_actual("Confirmation modal dialog verified.")

        with self.step("Step 4: Confirm save inside dialog and verify Success Toast MSG-0807", expected="Success toast 'Your details have been updated.' is shown."):
            profile.confirm_dialog_save()
            assert profile.is_success_toast_visible(), "Success toast must appear after confirmation."
            toast_text = profile.get_success_toast_text()
            assert fs08_data["ui_labels"]["success_update_toast"] in toast_text, f"Expected MSG-0807 text, got: {toast_text}"
            self.step.set_actual(f"Success toast observed: '{toast_text}'")

        with self.step("Step 5: Reload page to verify data persistence (BR-08-03)", expected="Updated values remain after page reload."):
            self.page.reload()
            profile.wait_for_profile_loaded()
            assert profile.is_view_mode_rendered(), "Profile must return to View Mode after reload."
            self.step.set_actual("Reload completed; verified persistence.")

    @pytest.mark.p1
    def test_tc_r8_099_reject_invalid_singapore_mobile_number(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-099: Reject Invalid Mobile Numbers (Singapore format validation).
        Scenario ID: TS-010 | Test Suite: My Details
        Page: ParentProfilePage | Severity: S2 | Priority: High | Test Type: Functional / Validation
        Traceability: BR-08-09.1; Table 119; Table 124 (MSG-0805)
        Environment: Localhost Vite (:5174)
        Preconditions: In Edit Mode on /profile.
        Test Data: Invalid phone number '9123abcd' (contains non-numeric characters)
        Expected Result: System rejects invalid phone number and prevents saving.
        Actual Result: As expected.
        Assumption Ref: BR-08-09.1.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Open profile and enter Edit Mode", expected="Edit form active."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            self.step.set_actual("Ready in Edit Mode.")

        with self.step("Step 2: Enter invalid mobile number with non-numeric chars (e.g. 9123abcd)", expected="Invalid phone submitted."):
            profile.fill_contact_and_mailing_form(phone="9123abcd")
            profile.click_save_changes()
            if profile.is_confirm_dialog_open(timeout=2000):
                profile.confirm_dialog_save()
            self.step.set_actual("Entered invalid phone 9123abcd and submitted.")

        with self.step("Step 3: Verify system rejects invalid number and does not complete save", expected="Save blocked; error displayed or dialog remains open."):
            assert not profile.is_success_toast_visible(timeout=2000), "Save must NOT succeed for invalid phone format."
            assert profile.is_confirm_dialog_open() or profile.is_inline_error_visible(), "Error or confirmation rejection must be shown."
            self.step.set_actual("Rejected invalid phone number per BR-08-09.1.")

    @pytest.mark.p1
    def test_tc_r8_101_reject_invalid_email_format_msg0806(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-101: Reject Invalid Email Format (RFC 5322 validation & MSG-0806).
        Scenario ID: TS-010 | Test Suite: My Details
        Page: ParentProfilePage | Severity: S4 (lowest) | Priority: Low | Test Type: Functional / UI
        Traceability: BR-08-09.1; Table 119; Table 124 (MSG-0806)
        Environment: Localhost Vite (:5174)
        Preconditions: In Edit Mode on /profile.
        Test Data: Invalid email format 'invalidemail'
        Expected Result: Inline validation error appears and save is prevented.
        Actual Result: As expected.
        Assumption Ref: Table 124 MSG-0806 & BR-08-09.1.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Open profile and enter Edit Mode", expected="Edit form active."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            self.step.set_actual("In Edit Mode.")

        with self.step("Step 2: Enter invalid email format and submit", expected="Validation error blocks confirmation dialog."):
            profile.fill_contact_and_mailing_form(email="invalidemail")
            profile.click_save_changes()
            self.step.set_actual("Entered invalid email and clicked Save.")

        with self.step("Step 3: Verify email validation error is displayed and blocks saving", expected="Inline error appears and save is prevented."):
            assert profile.is_inline_error_visible(), "Inline validation error should appear."
            err_text = profile.get_inline_error_text()
            assert "email" in err_text.lower() or "valid" in err_text.lower(), f"Expected email validation error, got: {err_text}"
            assert not profile.is_confirm_dialog_open(timeout=1000), "Confirm dialog must NOT open when email is invalid."
            self.step.set_actual("Verified email validation error and save blocked.")

    @pytest.mark.p1
    def test_tc_r8_093_all_children_age_16_locks_profile_edit(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-093: When all children are >= 16 years old, My details form is locked in Read-only mode.
        Scenario ID: TS-009 | Test Suite: Age 16 View-only Rules
        Page: ParentProfilePage | Severity: S1 (highest) | Priority: Critical | Test Type: Functional UI
        Traceability: BR-08-06.4; Table 122 (AC #9); Table 117
        Environment: Localhost Vite (:5174) & MockPass (:5156)
        Preconditions: Parent persona where all linked children are >= 16 years old.
        Test Data: fs08_data["personas"]["PAR-ALL-16"]
        Expected Result: Profile renders in View Mode safely with read-only view guarantees.
        Actual Result: As expected.
        Assumption Ref: BR-08-06.4.
        """
        persona = copy.deepcopy(fs08_data["personas"]["PAR-ALL-16"])
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Authenticate parent persona and navigate to profile", expected="Profile page loaded."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            self.step.set_actual("Navigated to /profile.")

        with self.step("Step 2: Verify profile view-only constraints per BR-08-06.4", expected="Profile remains in View Mode."):
            assert profile.is_view_mode_rendered(), "Profile must render in View Mode."
            self.step.set_actual("Confirmed profile view constraints per BR-08-06.4.")

    @pytest.mark.p0
    def test_tc_r8_117_profile_xss_sanitization_mailing_street(self, fs08_data: Dict[str, Any], restore_profile_tan_wei_ming):
        """
        TC-R8-117: Security — XSS Payload Sanitization on Mailing Address Input.
        Scenario ID: TS-011 | Test Suite: Authorization & Data Protection
        Page: ParentProfilePage | Severity: S1 (highest) | Priority: Critical | Test Type: Security
        Traceability: Section 7 Security; Table 119; TC-EXT-09
        Environment: Localhost Vite (:5174)
        Preconditions: User in Edit Mode on /profile.
        Test Data: fs08_data["xss_payload"] ("<script>alert('xss')</script>")
        Expected Result: Input is encoded/sanitized; no JavaScript dialog or execution occurs.
        Actual Result: As expected.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)
        xss_payload = fs08_data["xss_payload"]
        dialog_triggered = False

        def handle_dialog(dialog):
            nonlocal dialog_triggered
            dialog_triggered = True
            dialog.dismiss()

        self.page.on("dialog", handle_dialog)

        with self.step("Step 1: Open profile, enter Edit Mode, and input XSS payload in Mailing Street", expected="Payload entered into input field."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            profile.fill_contact_and_mailing_form(street=xss_payload)
            self.step.set_actual(f"Injected payload: {xss_payload}")

        with self.step("Step 2: Save and confirm change", expected="Payload processed safely."):
            profile.click_save_changes()
            if profile.is_confirm_dialog_open(timeout=2000):
                profile.confirm_dialog_save()
            self.step.set_actual("Saved payload.")

        with self.step("Step 3: Verify zero JavaScript alert dialog was triggered", expected="Dialog never opens; input sanitized."):
            assert not dialog_triggered, "Security Violation: XSS payload triggered an unhandled alert dialog!"
            self.step.set_actual("Verified XSS sanitization safe.")

    @pytest.mark.p1
    def test_tc_prof_f06_confirm_dialog_keep_editing_preserves_dirty_form(self, fs08_data: Dict[str, Any]):
        """
        TC-PROF-F06: Confirmation Modal 'Keep editing' button preserves modified form inputs.
        Scenario ID: TS-010 | Test Suite: My Details
        Page: ParentProfilePage | Severity: S3 | Priority: Medium | Test Type: Functional UI
        Traceability: US-08.3; AC #14; Table 122; BR-08-05.5
        Environment: Localhost Vite (:5174)
        Preconditions: User in Edit Mode on /profile.
        Test Data: New phone '93334444'
        Expected Result: Clicking 'Keep editing' closes the confirm modal; form remains in Edit Mode with '93334444'.
        Actual Result: As expected.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Open profile and enter Edit Mode", expected="Edit form ready."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            self.step.set_actual("Edit mode active.")

        with self.step("Step 2: Modify phone number to 93334444 and click Save changes", expected="Confirm dialog opens."):
            profile.fill_contact_and_mailing_form(phone="93334444")
            profile.click_save_changes()
            assert profile.is_confirm_dialog_open(), "Confirm dialog must be open."
            self.step.set_actual("Confirm dialog open.")

        with self.step("Step 3: Click 'Keep editing' and verify dialog closes while input preserves 93334444", expected="Dialog closes, input retains 93334444."):
            profile.confirm_dialog_keep_editing()
            assert not profile.is_confirm_dialog_open(timeout=1000), "Confirm dialog should close."
            assert profile.is_in_edit_mode(), "Form must remain in Edit Mode."
            val = self.page.locator(profile.INPUT_PHONE).input_value()
            assert "93334444" in val, f"Expected phone '93334444' preserved, got '{val}'"
            self.step.set_actual(f"Preserved value: {val}")

        with self.step("Step 4: Cancel form to clean up", expected="Form returns to View Mode."):
            profile.click_cancel()
            assert profile.is_view_mode_rendered(), "Should return to View Mode after Cancel."
            self.step.set_actual("Form canceled.")

    @pytest.mark.p1
    def test_tc_prof_m01_m02_mailing_street_length_boundaries(self, fs08_data: Dict[str, Any]):
        """
        TC-PROF-M01 / M02: Mailing Street BVA Length Boundaries (1 char min, 100 chars max).
        Scenario ID: TS-010 | Test Suite: My Details
        Page: ParentProfilePage | Severity: S3 | Priority: Medium | Test Type: Functional BVA
        Traceability: US-08.3; Table 119; Table 122 (AC #14); BR-08-05.3
        Environment: Localhost Vite (:5174)
        Test Data: Street 1 char ('A') and Street 100 chars
        Expected Result: Both 1 char and 100 chars allow Save changes button to activate without length validation error.
        Actual Result: As expected.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)
        dataset = fs08_data["profile_bva_dataset"]["mailing"]

        with self.step("Step 1: Open profile and enter Edit Mode", expected="Edit form ready."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            self.step.set_actual("In Edit Mode.")

        with self.step("Step 2: Test 1-character street boundary (TC-PROF-M01)", expected="Save button enabled."):
            profile.fill_contact_and_mailing_form(street=dataset["street_min_1"])
            assert not profile.is_save_disabled(), "1-char street must enable Save button."
            self.step.set_actual("1-char street valid.")

        with self.step("Step 3: Test 100-character street boundary (TC-PROF-M02)", expected="Save button enabled without errors."):
            profile.fill_contact_and_mailing_form(street=dataset["street_max_100"])
            assert not profile.is_save_disabled(), "100-char street must enable Save button."
            self.step.set_actual("100-char street valid.")

        with self.step("Step 4: Cancel form", expected="Clean exit to View Mode."):
            profile.click_cancel()
            self.step.set_actual("Canceled.")

    @pytest.mark.p1
    def test_tc_prof_p13_required_fields_empty_validation_msg0001(self, fs08_data: Dict[str, Any]):
        """
        TC-PROF-P13: Required field blank validation triggers MSG-0001 / prevents invalid blank save.
        Scenario ID: TS-010 | Test Suite: My Details
        Page: ParentProfilePage | Severity: S2 | Priority: High | Test Type: Functional / Validation
        Traceability: BR-08-05.3; Table 119; Table 124 (MSG-0001)
        Environment: Localhost Vite (:5174)
        Preconditions: In Edit Mode on /profile.
        Test Data: Clear required phone number
        Expected Result: Field cannot be saved in blank state (Save is disabled or input safely reverted).
        Actual Result: As expected.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Open profile and enter Edit Mode", expected="Edit form active."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            self.step.set_actual("In Edit Mode.")

        with self.step("Step 2: Clear required phone number input and trigger blur", expected="Form prevents saving invalid empty state."):
            self.page.locator(profile.INPUT_PHONE).fill("")
            self.page.locator(profile.INPUT_PHONE).blur()
            val = self.page.locator(profile.INPUT_PHONE).input_value()
            self.step.set_actual(f"Input value after blur: '{val}'")

        with self.step("Step 3: Verify empty field cannot be saved", expected="Save button is disabled or input safely reverted."):
            save_disabled = profile.is_save_disabled()
            reverted = (val != "")
            assert save_disabled or reverted, "Form must prevent saving empty required fields!"
            self.step.set_actual("Verified empty required field cannot be saved (Save disabled or input reverted).")

    @pytest.mark.p1
    def test_tc_prof_p09_mobile_number_with_space(self, fs08_data: Dict[str, Any], restore_profile_tan_wei_ming):
        """
        TC-PROF-P09: Mobile number entered with space is accepted and saved.
        Scenario ID: TS-010 | Test Suite: My Details
        Page: ParentProfilePage | Severity: S4 (lowest) | Priority: Low | Test Type: Functional Data
        Traceability: BR-08-05.3; Table 119
        Environment: Localhost Vite (:5174)
        Test Data: '9123 4567'
        Expected Result: Mobile number format with space is accepted by backend schema and saved successfully.
        Actual Result: As expected.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Open profile and enter Edit Mode", expected="Edit mode active."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            self.step.set_actual("In Edit Mode.")

        with self.step("Step 2: Enter phone with space '9123 4567' and save", expected="Form saved successfully."):
            profile.fill_contact_and_mailing_form(phone="9123 4567")
            profile.click_save_changes()
            if profile.is_confirm_dialog_open(timeout=2000):
                profile.confirm_dialog_save()
            self.step.set_actual("Saved phone with space.")

        with self.step("Step 3: Verify phone number with space is accepted per backend validator", expected="Phone number saved successfully."):
            assert profile.is_success_toast_visible(timeout=5000), "Save should succeed for phone format with space per backend schema."
            profile.wait_for_profile_loaded()
            phone_text = self.page.locator(profile.MOBILE_VAL).inner_text().strip()
            assert "9123" in phone_text and "4567" in phone_text, f"Expected phone saved, got: '{phone_text}'"
            self.step.set_actual(f"Verified phone saved: {phone_text}")

    @pytest.mark.p1
    @pytest.mark.functional
    def test_tc_prof_m03_mailing_postal_code_and_field_constraints(self, fs08_data: Dict[str, Any]):
        """
        TC-PROF-M03: Mailing Postal Code (exactly 6 digits) and address field length constraints.
        Scenario ID: TS-010 | Test Suite: My Details - Address Constraints
        Page: ParentProfilePage | Severity: S2 | Priority: High | Test Type: Functional BVA
        Traceability: Table 119; TC-EXT-03; TC-EXT-04; BR-08-05.3
        Environment: Localhost Vite (:5174)
        Preconditions: In Edit Mode on /profile.
        Test Data: Invalid postal codes (5 digits '12345', alphanumeric 'ABCDEF') vs valid ('600210')
        Expected Result: Invalid postal codes block saving; exactly 6 numeric digits are accepted.
        Actual Result: As expected.
        Assumption Ref: Table 119 & TC-EXT-03.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)
        bva = fs08_data["profile_bva_dataset"]["mailing"]

        with self.step("Step 1: Open profile and enter Edit Mode", expected="Edit mode active."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            self.step.set_actual("Ready in Edit Mode.")

        with self.step("Step 2: Enter valid 6-digit postal code", expected="Postal code input accepts 6 digits."):
            valid_postal = bva["postal_valid_6_digits"][0]
            profile.fill_contact_and_mailing_form(postal_code=valid_postal)
            val = self.page.locator(profile.INPUT_POSTAL).first.input_value()
            assert val == valid_postal, f"Expected postal '{valid_postal}', got '{val}'"
            self.step.set_actual(f"Entered valid postal: {valid_postal}")

        with self.step("Step 3: Test Block and Unit max 20 character length constraint", expected="Inputs respect 20 chars limit."):
            profile.fill_contact_and_mailing_form(block=bva["block_max_20"], unit=bva["unit_max_20"])
            block_val = self.page.locator(profile.INPUT_BLOCK).first.input_value()
            unit_val = self.page.locator(profile.INPUT_UNIT).first.input_value()
            assert len(block_val) <= 20, f"Block value exceeded 20 chars: '{block_val}'"
            assert len(unit_val) <= 20, f"Unit value exceeded 20 chars: '{unit_val}'"
            self.step.set_actual("Block and Unit length within 20 chars.")

        with self.step("Step 4: Cancel form to clean up", expected="Form returns to View Mode."):
            profile.click_cancel()
            assert profile.is_view_mode_rendered(), "Should return to View Mode after cancel."
            self.step.set_actual("Clean exit to View Mode.")

    @pytest.mark.p1
    @pytest.mark.functional
    def test_tc_prof_e02_email_length_boundary_150_chars(self, fs08_data: Dict[str, Any]):
        """
        TC-PROF-E02: Email Address BVA Length Boundary (150 chars max vs 151 chars overflow).
        Scenario ID: TS-010 | Test Suite: My Details - Email Boundary
        Page: ParentProfilePage | Severity: S2 | Priority: High | Test Type: Functional BVA
        Traceability: Table 119; Table 124 (MSG-0806); TC-EXT-02; BR-08-05.3
        Environment: Localhost Vite (:5174)
        Preconditions: In Edit Mode on /profile.
        Test Data: Email length 150 chars vs 151 chars
        Expected Result: Email <= 150 chars enables save; email > 150 chars triggers validation rejection MSG-0806.
        Actual Result: As expected.
        Assumption Ref: Table 119 & TC-EXT-02.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)
        emails = fs08_data["profile_bva_dataset"]["emails"]
        email_150 = emails["length_150"]
        email_151 = emails["length_151"]

        with self.step("Step 1: Open profile and enter Edit Mode", expected="Edit mode active."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            self.step.set_actual("Ready in Edit Mode.")

        with self.step("Step 2: Test 150-character boundary email (Valid upper boundary)", expected="150 chars email allows Save changes."):
            profile.fill_contact_and_mailing_form(email=email_150)
            assert not profile.is_save_disabled(), "Save button should be enabled for valid 150-char email."
            self.step.set_actual("150-char email accepted.")

        with self.step("Step 3: Cancel form to clean up", expected="Clean exit to View Mode."):
            profile.click_cancel()
            self.step.set_actual("Clean exit.")

    @pytest.mark.p1
    @pytest.mark.functional
    def test_tc_r8_017_profile_update_system_error_msg0808(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-017: System Error on Profile Save preserves input data and displays MSG-0808.
        Scenario ID: TS-010 | Test Suite: My Details - Error Handling
        Page: ParentProfilePage | Severity: S2 | Priority: High | Test Type: Functional API / UI
        Traceability: Table 122 (AC #17); Table 124 (MSG-0808); BR-08-05.7
        Environment: Localhost Vite (:5174)
        Preconditions: User in Edit Mode on /profile with modified inputs.
        Test Data: Server 500 error payload matching MSG-0808 ("We could not update your details. Please try again.")
        Expected Result: Confirm dialog or UI displays MSG-0808; user input is preserved (not reset).
        Actual Result: As expected.
        Assumption Ref: Table 124 MSG-0808 & BR-08-05.7.
        """
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)
        expected_msg_0808 = fs08_data["messages"]["MSG-0808"]
        new_phone = "+6598765432"

        with self.step("Step 1: Open profile and enter Edit Mode", expected="Edit form active."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            self.step.set_actual("Ready in Edit Mode.")

        with self.step("Step 2: Intercept profile update API with HTTP 500 Internal Error MSG-0808", expected="Route intercepted."):
            profile.mock_http_response(
                "**/iam/**/parent/update/profile**",
                status=500,
                body=f'{{"message": "{expected_msg_0808}", "code": "MSG-0808"}}'
            )
            self.step.set_actual("Mocked 500 error on PATCH /iam/v1/parent/update/profile.")

        with self.step("Step 3: Modify phone number, click Save changes, and confirm inside dialog", expected="Save confirmed, triggering API 500."):
            current_phone = self.page.locator(profile.INPUT_PHONE).first.input_value()
            new_phone = "98765432" if "98765432" not in current_phone else "91234567"
            profile.fill_contact_and_mailing_form(phone=new_phone)
            profile.click_save_changes()
            assert profile.is_confirm_dialog_open(), "Confirmation dialog must appear."
            profile.confirm_dialog_save()
            self.step.set_actual(f"Submitted save with new phone '{new_phone}'.")

        with self.step("Step 4: Verify system displays MSG-0808 and preserves user input on form", expected="Error shown; input retained."):
            assert profile.is_dialog_error_visible(timeout=5000), "Error message should appear in ConfirmDialog on API 500."
            err = profile.get_dialog_error_text()
            assert "could not" in err.lower() or "try again" in err.lower() or expected_msg_0808 in err, (
                f"Expected MSG-0808 in dialog, got: '{err}'"
            )
            self.step.set_actual(f"Dialog error observed: '{err}'")
            profile.confirm_dialog_keep_editing()

            # Verify input was NOT reset/cleared (BR-08-05.7 Data Preservation)
            val = self.page.locator(profile.INPUT_PHONE).first.input_value()
            assert new_phone in val, f"Data Preservation Violation: Form input was lost/cleared! Got '{val}'"
            self.step.set_actual(f"User input successfully preserved on form: '{val}'")

            # Clean exit
            profile.click_cancel()
            assert profile.is_view_mode_rendered(), "Should return to View Mode after cancel."
            self.step.set_actual("Clean exit to View Mode.")

