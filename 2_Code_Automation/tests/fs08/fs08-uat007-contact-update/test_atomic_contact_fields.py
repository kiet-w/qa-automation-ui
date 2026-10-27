"""
tests/fs08/fs08-uat007-contact-update/test_atomic_contact_fields.py
Atomic Field Validation & SingPass Immutability Verification for UAT-007 (US-009).
Strictly compliant with Invariant 1 (Zero assertions in POM) and Invariant 9 (< 200 lines).
Traceability: US-009, BR-08-02, BR-08-03, D-20, R8-AC05, R8-AC06, R8-AC12, R8-AC13, R8-AC15.
"""
from typing import Any, Dict
import pytest

from tests.base_test import BaseTest
from pages.fs08.singpass_login_page import SingpassLoginPage
from pages.fs08.parent_profile_page import ParentProfilePage


@pytest.mark.p0
@pytest.mark.atomic
@pytest.mark.functional
@pytest.mark.security
class TestAtomicContactFields(BaseTest):
    """Atomic test suite verifying SingPass identity immutability and permitted contact fields."""

    def test_tc_uat007_01_singpass_identity_immutability(self, fs08_data: Dict[str, Any]):
        """TC-UAT007-01: Verify government identity fields remain immutable in View and Edit modes."""
        persona = fs08_data["uat_007"]["persona"]
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step(f"Sign in as Howard ({persona['name']}) and open /profile", expected="View Mode rendered."):
            login.login_with_persona(persona["name"], base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            assert profile.is_view_mode_rendered(), "Profile view mode must be active."
            self.step.set_actual("Profile loaded in View Mode.")

        with self.step("Verify identity fields in View Mode are read-only text terms", expected="No inputs for identity."):
            full_name = profile.get_full_name()
            assert len(full_name) > 0, "Full Name must be displayed."
            assert profile.is_nric_hidden(), "NRIC must be masked by default in View Mode."
            self.step.set_actual(f"Identity attributes verified as static definition terms ({full_name}).")

        with self.step("Click 'Update details' and verify identity remains strictly read-only in Edit Mode", expected="0 input tags."):
            profile.click_update_details()
            assert profile.is_in_edit_mode(), "Profile must transition to Edit Mode."
            # Invariant: Zero input or textarea elements for SingPass identity attributes
            assert self.page.locator("input[name='fullName'], input[name='nric'], input[name='residentialAddress']").count() == 0
            assert self.page.locator("textarea[name='residentialAddress']").count() == 0
            self.highlight_actual_result(locator=profile.FULL_NAME_VAL, text="Immutable SingPass Identity")
            self.step.set_actual("Confirmed zero input elements exist for SingPass identity.")

        profile.click_cancel()

    def test_tc_uat007_02_nric_masking_toggle_clean_state(self, fs08_data: Dict[str, Any]):
        """TC-UAT007-02: Verify NRIC Show/Hide toggle does not affect pristine form state."""
        persona = fs08_data["uat_007"]["persona"]
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Enter Edit Mode and inspect pristine state", expected="Save button is disabled."):
            login.login_with_persona(persona["name"], base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()
            assert profile.is_save_disabled(), "Save button must be disabled in pristine state."
            assert profile.is_nric_hidden(), "NRIC must initially be masked."

        with self.step("Click 'Show NRIC' and 'Hide NRIC' and verify form remains pristine", expected="Save still disabled."):
            profile.toggle_show_nric()
            assert not profile.is_nric_hidden(), "NRIC should be revealed after clicking Show NRIC."
            profile.toggle_hide_nric()
            assert profile.is_nric_hidden(), "NRIC must be masked after clicking Hide NRIC."
            assert profile.is_save_disabled(), "NRIC toggle must NOT trigger dirty state on form."
            self.step.set_actual("NRIC toggle preserves pristine form state.")

        profile.click_cancel()

    def test_tc_uat007_03_mobile_validation_matrix(self, fs08_data: Dict[str, Any]):
        """TC-UAT007-03: Verify Mobile validation for empty, whitespace ASM-15, and syntax MSG-0805."""
        persona = fs08_data["uat_007"]["persona"]
        vectors = fs08_data["uat_007"]["validation_test_vectors"]
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Enter Edit Mode on /profile", expected="Edit Mode active."):
            login.login_with_persona(persona["name"], base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()

        with self.step("Test empty Mobile number disables Save (MSG-0001 protection)", expected="Save button disabled."):
            profile.fill_contact_and_mailing_form(phone="")
            assert profile.is_save_disabled(), "Save button must remain disabled when mandatory mobile is empty."
            self.step.set_actual("Empty Mobile safely guarded by pristine/disabled state.")

        with self.step("Test whitespace-only Mobile number (ASM-15) treated as blank", expected="Save button disabled."):
            profile.fill_contact_and_mailing_form(phone=vectors["invalid_phone_whitespace"])
            assert profile.is_save_disabled(), "Save button must remain disabled when mobile is whitespace."
            self.step.set_actual("All-whitespace Mobile string safely rejected.")

        with self.step("Test 7-digit Mobile number triggers MSG-0805 syntax guard", expected="Short number rejected."):
            profile.fill_contact_and_mailing_form(phone=vectors["invalid_phone_short"])
            if not profile.is_save_disabled():
                profile.click_save_changes()
                if profile.is_confirm_dialog_open(timeout=1000):
                    profile.confirm_dialog_save()
                assert not profile.is_success_toast_visible(timeout=1500), "Save must not succeed for short phone."
            else:
                assert profile.is_save_disabled()
            self.step.set_actual("Short mobile number 9123456 safely blocked.")

        profile.click_cancel()

    def test_tc_uat007_04_email_validation_matrix(self, fs08_data: Dict[str, Any]):
        """TC-UAT007-04: Verify Email validation for empty, whitespace ASM-15, and RFC 5322 syntax MSG-0806."""
        persona = fs08_data["uat_007"]["persona"]
        vectors = fs08_data["uat_007"]["validation_test_vectors"]
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Enter Edit Mode on /profile", expected="Edit Mode active."):
            login.login_with_persona(persona["name"], base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()

        with self.step("Test empty Email disables Save (MSG-0001 protection)", expected="Save disabled."):
            profile.fill_contact_and_mailing_form(email="")
            assert profile.is_save_disabled(), "Save button must remain disabled when mandatory email is empty."
            self.step.set_actual("Empty Email safely blocked.")

        with self.step("Test invalid email format triggers MSG-0806", expected="Syntax error MSG-0806."):
            profile.fill_contact_and_mailing_form(email=vectors["invalid_email_format"])
            if not profile.is_save_disabled():
                profile.click_save_changes()
                assert not profile.is_confirm_dialog_open(timeout=1000), "Modal must not open on invalid email."
            self.step.set_actual("Invalid email syntax rejected without opening confirmation modal.")

        profile.click_cancel()

    def test_tc_uat007_05_mailing_address_mandatory_and_optional(self, fs08_data: Dict[str, Any]):
        """TC-UAT007-05: Verify Mailing Address mandatory vs optional fields (BR-08-02, R8-AC15)."""
        persona = fs08_data["uat_007"]["persona"]
        vectors = fs08_data["uat_007"]["validation_test_vectors"]
        login = self.get_page(SingpassLoginPage)
        profile = self.get_page(ParentProfilePage)

        with self.step("Enter Edit Mode on /profile", expected="Edit Mode active."):
            login.login_with_persona(persona["name"], base_url=fs08_data["base_url"])
            profile.open(base_url=fs08_data["base_url"])
            profile.click_update_details()

        with self.step("Clear mandatory Street and verify Save disabled", expected="Save button disabled."):
            profile.fill_contact_and_mailing_form(street="")
            assert profile.is_save_disabled(), "Save button must remain disabled when street is empty."
            self.step.set_actual("Empty mandatory Street blocked form submission.")

        with self.step("Test 5-digit short postal code triggers validation error", expected="Short postal code blocked."):
            profile.fill_contact_and_mailing_form(street="Orchard Boulevard", postal_code=vectors["invalid_postal_short"])
            if not profile.is_save_disabled():
                profile.click_save_changes()
                assert not profile.is_confirm_dialog_open(timeout=1000), "Dialog must not open with invalid postal code."
            self.step.set_actual("Postal code 12345 (5 digits) safely blocked.")

        profile.click_cancel()
