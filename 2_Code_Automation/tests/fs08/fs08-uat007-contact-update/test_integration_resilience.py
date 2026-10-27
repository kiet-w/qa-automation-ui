"""UAT-007 resilience and request-contract coverage for the profile update flow."""
import json
import re

import pytest
from playwright.sync_api import expect

from pages.fs08.parent_profile_page import ParentProfilePage
from pages.fs08.singpass_login_page import SingpassLoginPage
from tests.base_test import BaseTest


UPDATE_ENDPOINT = re.compile(r"/iam/v1/parent/update/profile(?:\?|$)")


def _open_dirty_profile(test, data):
    """Open a valid dirty form without embedding business data in test code."""
    login = test.get_page(SingpassLoginPage)
    profile = test.get_page(ParentProfilePage)
    login.login_with_persona(data["uat_007"]["persona"]["name"], base_url=data["base_url"])
    profile.open(base_url=data["base_url"])
    profile.click_update_details()
    baseline = profile.get_input_value(profile.INPUT_PHONE)
    candidates = (
        data["uat_007"]["permitted_contact_valid"]["phoneNumber"],
        data["uat_007"]["permitted_contact_restore"]["phoneNumber"],
    )
    changed = next(value for value in candidates if value != baseline)
    profile.fill_contact_and_mailing_form(phone=changed)
    return profile, changed


@pytest.mark.p0
@pytest.mark.integration
@pytest.mark.break_it
class TestIntegrationResilience(BaseTest):
    """Negative flows use the live verified mutation endpoint and always unroute."""

    def test_tc_uat007_74_network_failure_preserves_dialog_and_data(self, fs08_data):
        profile, changed = _open_dirty_profile(self, fs08_data)
        requests = []

        def abort_network(route):
            requests.append(route.request)
            route.abort("failed")

        self.page.route(UPDATE_ENDPOINT, abort_network)
        try:
            profile.click_save_changes()
            assert profile.is_confirm_dialog_open(timeout=3000)
            profile.confirm_dialog_save()
            expect(self.page.locator(profile.DIALOG_ERROR_MSG).first).to_have_text(
                fs08_data["uat_007"]["validation_test_vectors"]["expected_msg_0808"]
            )
            assert profile.is_confirm_dialog_open(timeout=1000)
            assert profile.get_input_value(profile.INPUT_PHONE) == changed
            assert len(requests) == 1
            expect(self.page.locator(profile.DIALOG_CONFIRM_SAVE_BTN)).to_be_enabled()
        finally:
            self.page.unroute_all()

    def test_tc_uat007_75_double_submit_sends_one_mutation(self, fs08_data):
        profile, _ = _open_dirty_profile(self, fs08_data)
        requests = []
        error_message = fs08_data["uat_007"]["validation_test_vectors"]["expected_msg_0808"]

        def fulfill_error(route):
            requests.append(route.request)
            route.fulfill(
                status=500,
                content_type="application/json",
                body=json.dumps({"code": "MSG-0808", "message": error_message}),
            )

        self.page.route(UPDATE_ENDPOINT, fulfill_error)
        try:
            profile.click_save_changes()
            assert profile.is_confirm_dialog_open(timeout=3000)
            button = self.page.locator(profile.DIALOG_CONFIRM_SAVE_BTN)
            button.evaluate("element => { element.click(); element.click(); }")
            expect(self.page.locator(profile.DIALOG_ERROR_MSG).first).to_have_text(error_message)
            assert len(requests) == 1, "Rapid clicks emitted duplicate mutation requests"
        finally:
            self.page.unroute_all()

    def test_tc_uat007_76_partial_payload_excludes_identity_and_unchanged_fields(self, fs08_data):
        profile, changed = _open_dirty_profile(self, fs08_data)
        captured = []
        error_message = fs08_data["uat_007"]["validation_test_vectors"]["expected_msg_0808"]

        def capture_payload(route):
            captured.append(route.request.post_data_json)
            route.fulfill(
                status=500,
                content_type="application/json",
                body=json.dumps({"code": "MSG-0808", "message": error_message}),
            )

        self.page.route(UPDATE_ENDPOINT, capture_payload)
        try:
            profile.click_save_changes()
            profile.confirm_dialog_save()
            expect(self.page.locator(profile.DIALOG_ERROR_MSG).first).to_have_text(error_message)
            assert len(captured) == 1
            payload = captured[0]
            assert payload == {"phoneNumber": changed}, "PATCH payload included unchanged fields"
            identity_names = fs08_data["uat_007"]["ui_health"]["identity_field_names"]
            assert not set(identity_names).intersection(payload), "Identity field leaked into mutation"
        finally:
            self.page.unroute_all()

    def test_tc_uat007_77_confirmation_dialog_traps_focus(self, fs08_data):
        profile, _ = _open_dirty_profile(self, fs08_data)
        profile.click_save_changes()
        dialog = self.page.locator(profile.CONFIRM_ALERTDIALOG).first
        expect(dialog).to_be_visible()
        assert dialog.evaluate("element => element.contains(document.activeElement)")
        for _ in range(4):
            self.page.keyboard.press("Tab")
            assert dialog.evaluate("element => element.contains(document.activeElement)")
        profile.confirm_dialog_keep_editing()
        profile.click_cancel()
