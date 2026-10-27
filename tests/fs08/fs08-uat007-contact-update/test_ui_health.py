"""UAT-007 live UI inventory, accessibility smoke checks, and health gates."""
import pytest

from pages.fs08.parent_profile_page import ParentProfilePage
from pages.fs08.singpass_login_page import SingpassLoginPage
from tests.base_test import BaseTest


def _open_profile(test, data):
    login = test.get_page(SingpassLoginPage)
    profile = test.get_page(ParentProfilePage)
    login.login_with_persona(data["uat_007"]["persona"]["name"], base_url=data["base_url"])
    profile.open(base_url=data["base_url"])
    return profile


@pytest.mark.p1
@pytest.mark.ui
class TestUIHealth(BaseTest):
    def test_tc_uat007_78_editable_and_identity_dom_inventory(self, fs08_data):
        profile = _open_profile(self, fs08_data)
        profile.click_update_details()
        editable = fs08_data["uat_007"]["ui_health"]["editable_field_names"]
        identity = fs08_data["uat_007"]["ui_health"]["identity_field_names"]
        assert all(self.page.locator(f"input[name='{name}']").count() == 1 for name in editable)
        assert all(self.page.locator(f"input[name='{name}']").count() == 0 for name in identity)
        profile.click_cancel()

    def test_tc_uat007_79_zero_uncaught_console_and_page_errors(self, fs08_data):
        console_errors = []
        page_errors = []
        self.page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        self.page.on("pageerror", lambda error: page_errors.append(str(error)))
        profile = _open_profile(self, fs08_data)
        profile.click_update_details()
        profile.click_cancel()
        assert not console_errors, f"Console errors: {console_errors}"
        assert not page_errors, f"Uncaught page errors: {page_errors}"

    def test_tc_uat007_80_zero_horizontal_overflow(self, fs08_data):
        profile = _open_profile(self, fs08_data)
        health = fs08_data["uat_007"]["ui_health"]
        for viewport in (health["desktop_viewport"], health["mobile_viewport"]):
            self.page.set_viewport_size(viewport)
            profile.open(base_url=fs08_data["base_url"])
            has_overflow = self.page.evaluate(
                "() => document.documentElement.scrollWidth > document.documentElement.clientWidth"
            )
            assert not has_overflow, f"Horizontal overflow at {viewport}"

    def test_tc_uat007_81_keyboard_update_and_cancel(self, fs08_data):
        profile = _open_profile(self, fs08_data)
        self.page.locator(profile.UPDATE_DETAILS_BTN).focus()
        self.page.keyboard.press("Enter")
        assert profile.is_in_edit_mode()
        self.page.locator(profile.CANCEL_BTN).focus()
        self.page.keyboard.press("Enter")
        assert profile.is_view_mode_rendered()

    def test_tc_uat007_82_no_raw_i18n_key_visible(self, fs08_data):
        profile = _open_profile(self, fs08_data)
        profile.click_update_details()
        visible_text = self.page.locator("body").inner_text()
        prefixes = fs08_data["uat_007"]["ui_health"]["raw_i18n_prefixes"]
        assert all(prefix not in visible_text for prefix in prefixes)
        profile.click_cancel()

    def test_tc_uat007_83_inputs_have_programmatic_labels(self, fs08_data):
        profile = _open_profile(self, fs08_data)
        profile.click_update_details()
        names = fs08_data["uat_007"]["ui_health"]["editable_field_names"]
        for name in names:
            field = self.page.locator(f"input[name='{name}']").first
            field_id = field.get_attribute("id")
            labelled = field.get_attribute("aria-label") or field.get_attribute("aria-labelledby")
            assert labelled or (field_id and self.page.locator(f"label[for='{field_id}']").count() == 1)
        profile.click_cancel()
