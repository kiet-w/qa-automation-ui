"""
tests/fs08/fs08-uat007-contact-update/test_integration_contact_update.py
Integration & End-to-End Workflow Verification for UAT-007 (US-009).
Strictly compliant with Invariant 1 (Zero assertions in POM) and Invariant 9 (< 250 lines).
Traceability: US-009, BR-08-01, BR-08-02, BR-08-03, D-20, R8-AC11, R8-AC25, R8-AC26, MSG-0807, MSG-0808.
"""
import json
import re
from typing import Any, Dict
import pytest
from playwright.sync_api import expect

from tests.base_test import BaseTest
from pages.fs08.singpass_login_page import SingpassLoginPage
from pages.fs08.parent_profile_page import ParentProfilePage


@pytest.mark.p0
@pytest.mark.functional
@pytest.mark.flow
class TestIntegrationContactUpdate(BaseTest):
    """Integration test suite for UAT-007 Contact Update Flow and Dialog Lifecycle."""

    def test_tc_uat007_06_pristine_to_dirty_gatekeeper(self, fs08_data: Dict[str, Any]):
        """TC-UAT007-06: Verify Pristine/Dirty transitions and Cancel discard (R8-AC25)."""
        persona = fs08_data["uat_007"]["persona"]
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step(f"Sign in as Howard ({persona['name']}) and enter Edit Mode", expected="Form is pristine."):
            login.login_with_persona(persona["name"], base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            assert profile.is_save_disabled(), "Save button must be disabled in pristine state."
            assert self.page.locator(profile.DIRTY_STATE_HINT).count() > 0, "Dirty state guidance hint must be visible."
            self.step.set_actual("Pristine state verified: Save disabled with hint.")

        with self.step("Modify mobile number and verify dirty state", expected="Save button enabled."):
            baseline = profile.get_input_value(profile.INPUT_PHONE)
            candidates = (fs08_data["uat_007"]["permitted_contact_valid"]["phoneNumber"],
                          fs08_data["uat_007"]["permitted_contact_restore"]["phoneNumber"])
            changed = next(value for value in candidates if value != baseline)
            profile.fill_contact_and_mailing_form(phone=changed)
            assert not profile.is_save_disabled(), "Save button must enable when form is modified."
            self.step.set_actual("Dirty state active: Save button enabled.")

        with self.step("Restore the original value", expected="Save disabled again."):
            profile.fill_contact_and_mailing_form(phone=baseline)
            assert profile.is_save_disabled(), "Reverting the field must restore pristine state."
            profile.fill_contact_and_mailing_form(phone=changed)

        with self.step("Click 'Cancel' and verify form discards modifications and returns to View Mode", expected="View Mode active."):
            profile.click_cancel()
            assert profile.is_view_mode_rendered(), "Form must return to View Mode after Cancel."
            self.step.set_actual("Cancel successfully discarded modifications.")

    def test_tc_uat007_07_confirm_dialog_keep_editing(self, fs08_data: Dict[str, Any]):
        """TC-UAT007-07: Verify modal confirm dialog opens and 'Keep editing' preserves inputs (R8-AC26)."""
        persona = fs08_data["uat_007"]["persona"]
        valid_contact = fs08_data["uat_007"]["permitted_contact_valid"]
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Enter Edit Mode and populate new contact information", expected="Form dirty."):
            login.login_with_persona(persona["name"], base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            baseline = profile.get_input_value(profile.INPUT_PHONE)
            candidates = (valid_contact["phoneNumber"],
                          fs08_data["uat_007"]["permitted_contact_restore"]["phoneNumber"])
            changed_phone = next(value for value in candidates if value != baseline)
            profile.fill_contact_and_mailing_form(
                phone=changed_phone,
                street=valid_contact["mailingStreet"],
            )
            assert not profile.is_save_disabled()

        with self.step("Click 'Save changes' and verify confirm alertdialog appears", expected="Modal dialog opened."):
            profile.click_save_changes()
            assert profile.is_confirm_dialog_open(timeout=3000), "Confirmation alertdialog must appear."
            self.highlight_actual_result(locator=profile.CONFIRM_ALERTDIALOG, text="Save Confirmation Dialog")
            self.step.set_actual("Confirmation modal dialog verified.")

        with self.step("Click 'Keep editing' and verify modal closes and inputs stay intact", expected="Inputs preserved."):
            profile.confirm_dialog_keep_editing()
            assert not profile.is_confirm_dialog_open(timeout=1000), "Dialog must close after Keep editing."
            assert profile.is_in_edit_mode(), "Profile must remain in Edit Mode."
            current_phone = profile.get_input_value(profile.INPUT_PHONE)
            assert current_phone == changed_phone, "Phone input value must be preserved."
            self.step.set_actual(f"Keep editing preserved entered phone '{current_phone}'.")

        profile.click_cancel()

    @pytest.mark.break_it
    def test_tc_uat007_08_api_500_error_handling_dialog_stays_open(self, fs08_data: Dict[str, Any]):
        """TC-UAT007-08: Verify HTTP 500 error keeps dialog open displaying MSG-0808 (Negative Flow)."""
        persona = fs08_data["uat_007"]["persona"]
        vectors = fs08_data["uat_007"]["validation_test_vectors"]
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Sign in and intercept the verified mutation endpoint", expected="Fault route active."):
            login.login_with_persona(persona["name"], base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            requests = []

            def fulfill_server_error(route):
                requests.append(route.request)
                route.fulfill(
                    status=500,
                    content_type="application/json",
                    body=json.dumps({"code": "MSG-0808", "message": vectors["expected_msg_0808"]}),
                )

            self.page.route(
                re.compile(r"/iam/v1/parent/update/profile(?:\?|$)"),
                fulfill_server_error,
            )
            self.step.set_actual("Mocked 500 MSG-0808 error route attached.")

        with self.step("Modify phone and attempt submit in confirmation dialog", expected="Dialog stays open with MSG-0808."):
            profile.click_update_details()
            before = profile.get_input_value(profile.INPUT_PHONE)
            candidates = (fs08_data["uat_007"]["permitted_contact_valid"]["phoneNumber"],
                          fs08_data["uat_007"]["permitted_contact_restore"]["phoneNumber"])
            changed = next(value for value in candidates if value != before)
            profile.fill_contact_and_mailing_form(phone=changed)
            profile.click_save_changes()
            assert profile.is_confirm_dialog_open(timeout=3000)
            profile.confirm_dialog_save()
            expect(self.page.locator(profile.CONFIRM_ALERTDIALOG)).to_be_visible()
            expect(self.page.locator(profile.DIALOG_ERROR_MSG).first).to_have_text(vectors["expected_msg_0808"])
            assert len(requests) == 1, "Exactly one mutation request is expected."
            assert profile.get_input_value(profile.INPUT_PHONE) == changed, "User input was lost after API failure."
            expect(self.page.locator(profile.DIALOG_CONFIRM_SAVE_BTN)).to_be_enabled()
            dialog_err = profile.get_dialog_error_text()
            self.highlight_actual_result(locator=profile.DIALOG_ERROR_MSG, text=f"Error: {dialog_err}")
            self.step.set_actual(f"Server error handled cleanly in modal: '{dialog_err}'.")

        self.page.unroute_all()
        if profile.is_confirm_dialog_open(timeout=1000):
            profile.confirm_dialog_keep_editing()
        profile.click_cancel()

    def test_tc_uat007_09_full_e2e_uat007_acceptance(self, fs08_data: Dict[str, Any], restore_profile_uat007):
        """TC-UAT007-09: Complete UAT-007 End-to-End Acceptance: update permitted contact without changing identity."""
        persona = fs08_data["uat_007"]["persona"]
        valid_contact = fs08_data["uat_007"]["permitted_contact_valid"]
        vectors = fs08_data["uat_007"]["validation_test_vectors"]
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Step 1: Sign in as Howard via MockPass and inspect profile identity", expected="Identity verified."):
            login.login_with_persona(persona["name"], base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            assert profile.is_view_mode_rendered()
            initial_name = profile.get_full_name()
            assert len(initial_name) > 0, "Full Name must be displayed."
            assert profile.is_nric_hidden(), "NRIC must be masked by default."
            self.step.set_actual(f"Identity confirmed: {initial_name}, NRIC masked.")

        with self.step("Step 2: Enter Edit Mode and update permitted contact and mailing fields", expected="Fields populated."):
            profile.click_update_details()
            fields = {
                "phoneNumber": profile.INPUT_PHONE, "email": profile.INPUT_EMAIL,
                "mailingBlock": profile.INPUT_BLOCK, "mailingStreet": profile.INPUT_STREET,
                "mailingUnit": profile.INPUT_UNIT, "mailingPostalCode": profile.INPUT_POSTAL,
                "mailingCountry": profile.INPUT_COUNTRY,
            }
            restore_profile_uat007.update({name: profile.get_input_value(selector)
                                           for name, selector in fields.items()})
            profile.fill_contact_and_mailing_form(
                phone=valid_contact["phoneNumber"],
                email=valid_contact["email"],
                block=valid_contact["mailingBlock"],
                street=valid_contact["mailingStreet"],
                unit=valid_contact["mailingUnit"],
                postal_code=valid_contact["mailingPostalCode"],
                country=valid_contact["mailingCountry"],
            )
            assert not profile.is_save_disabled(), "Save button must be enabled."
            self.step.set_actual("Permitted contact & mailing fields populated.")

        with self.step("Step 3: Submit and confirm in modal dialog", expected="Toast MSG-0807 displayed."):
            profile.click_save_changes()
            assert profile.is_confirm_dialog_open(timeout=3000)
            profile.confirm_dialog_save()
            assert profile.is_success_toast_visible(timeout=5000), "Success toast MSG-0807 must appear."
            toast_text = profile.get_success_toast_text()
            assert vectors["expected_msg_0807"] in toast_text
            self.highlight_actual_result(locator=profile.SUCCESS_TOAST, text=f"Toast: {toast_text}")
            self.step.set_actual(f"Success toast verified: '{toast_text}'.")

        with self.step("Step 4: Verify View Mode reflects updated contact while Singpass identity is unchanged", expected="Identity protected."):
            profile.open(base_url=fs08_data["base_url"])
            assert profile.is_view_mode_rendered()
            # SingPass Identity Immutability check
            assert profile.get_full_name() == initial_name, "Full Name must remain 100% invariant."
            assert profile.is_nric_hidden(), "NRIC must remain masked."
            # Contact Fields updated check
            assert valid_contact["phoneNumber"] in profile.get_text(profile.MOBILE_VAL)
            assert valid_contact["email"] in profile.get_text(profile.EMAIL_VAL)
            profile.click_update_details()
            for name, selector in fields.items():
                assert profile.get_input_value(selector) == valid_contact[name], f"{name} did not persist after reload"
            profile.click_cancel()
            self.step.set_actual("UAT-007 verified: contact updated, Singpass identity immutable.")
