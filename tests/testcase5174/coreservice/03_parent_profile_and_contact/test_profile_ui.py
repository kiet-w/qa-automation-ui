"""UI automation mapped to profile cases with live-confirmed accessible controls."""
import pytest
from playwright.sync_api import expect

from pages.fs08.parent_profile_page import ParentProfilePage
from pages.fs08.locators import ParentProfileLocators as Loc
from tests.base_test import BaseTest


def _open_profile_form(page, fs08_data):
    profile = ParentProfilePage(page)
    profile.open(fs08_data["base_url"])
    profile.click_update_details()
    return page.get_by_role("form", name="Update details", exact=True)


def _profile_validation_cases():
    return [
        pytest.param("TC-PRF-VAL-01", "Mobile Number", "phones.valid_prefixes.0", "valid", id="TC-PRF-VAL-01"),
        pytest.param("TC-PRF-VAL-02", "Mobile Number", "phones.invalid_lengths.0", "invalid", id="TC-PRF-VAL-02"),
        pytest.param("TC-PRF-VAL-03", "Mobile Number", "phones.invalid_prefixes.0", "invalid", id="TC-PRF-VAL-03"),
        pytest.param("TC-PRF-VAL-04", "Mobile Number", "phones.invalid_alphanumeric.0", "invalid", id="TC-PRF-VAL-04"),
        pytest.param("TC-PRF-VAL-05", "Mobile Number", "phones.with_space", "normalize_phone", id="TC-PRF-VAL-05"),
        pytest.param("TC-PRF-VAL-06", "Mobile Number", "universal_vectors.empty", "invalid", id="TC-PRF-VAL-06"),
        pytest.param("TC-PRF-VAL-07", "Email Address", "emails.valid_formats.2", "valid", id="TC-PRF-VAL-07"),
        pytest.param("TC-PRF-VAL-08", "Email Address", "emails.invalid_formats.0", "invalid", id="TC-PRF-VAL-08"),
        pytest.param("TC-PRF-VAL-09", "Email Address", "emails.length_150", "max_email", id="TC-PRF-VAL-09"),
        pytest.param("TC-PRF-VAL-10", "Email Address", "emails.invalid_formats.7", "invalid", id="TC-PRF-VAL-10"),
        pytest.param("TC-PRF-VAL-11", "Email Address", "universal_vectors.empty", "invalid", id="TC-PRF-VAL-11"),
        pytest.param("TC-PRF-VAL-12", "Postal code", "mailing.postal_valid_6_digits.0", "valid", id="TC-PRF-VAL-12"),
        pytest.param("TC-PRF-VAL-13", "Postal code", "mailing.postal_valid_6_digits.1", "preserve_zero", id="TC-PRF-VAL-13"),
        pytest.param("TC-PRF-VAL-14", "Postal code", "mailing.postal_invalid_lengths.0", "invalid", id="TC-PRF-VAL-14"),
        pytest.param("TC-PRF-VAL-15", "Postal code", "mailing.postal_invalid_chars.0", "invalid", id="TC-PRF-VAL-15"),
        pytest.param("TC-PRF-VAL-16", "Postal code", "universal_vectors.empty", "invalid", id="TC-PRF-VAL-16"),
        pytest.param("TC-PRF-VAL-17", "Street", "universal_vectors.leading_trailing_spaces", "trim", id="TC-PRF-VAL-17"),
        pytest.param("TC-PRF-VAL-18", "Street", "mailing.street_max_100", "max_length", id="TC-PRF-VAL-18"),
        pytest.param("TC-PRF-VAL-19", "Street", "universal_vectors.empty", "invalid", id="TC-PRF-VAL-19"),
        pytest.param("TC-PRF-VAL-20", "Block", "universal_vectors.empty", "optional", id="TC-PRF-VAL-20"),
        pytest.param("TC-PRF-VAL-21", "Block", "mailing.block_valid_alphanumeric.0", "valid", id="TC-PRF-VAL-21"),
        pytest.param("TC-PRF-VAL-22", "Unit", "universal_vectors.empty", "optional", id="TC-PRF-VAL-22"),
        pytest.param("TC-PRF-VAL-23", "Unit", "mailing.unit_valid_notations.0", "valid", id="TC-PRF-VAL-23"),
        pytest.param("TC-PRF-VAL-24", "Country", "mailing.country_default", "default", id="TC-PRF-VAL-24"),
        pytest.param("TC-PRF-VAL-25", "Country", "mailing.country_max_100", "max_length", id="TC-PRF-VAL-25"),
        pytest.param("TC-PRF-VAL-26", "Street", "universal_vectors.security_injection.0", "safe_text", id="TC-PRF-VAL-26"),
        pytest.param("TC-PRF-VAL-27", "Street", "universal_vectors.security_injection.1", "safe_text", id="TC-PRF-VAL-27"),
    ]


@pytest.mark.ui
@pytest.mark.ac
class TestParentProfileUI(BaseTest):
    def test_tc_prf_ac_01_profile_view_exposes_identity_contact_and_mailing_regions(self, authenticated_parent, fs08_data):
        """TC-PRF-AC-01: the profile view exposes the three observed information regions."""
        profile = ParentProfilePage(self.page)
        profile.open(fs08_data["base_url"])
        with self.step("Kiểm tra chế độ xem hồ sơ", expected="Heading và ba vùng thông tin hồ sơ hiển thị."):
            expect(self.page.locator(Loc.PROFILE_HEADING)).to_be_visible()
            expect(self.page.locator(Loc.IDENTITY_REGION)).to_be_visible()
            expect(self.page.locator(Loc.CONTACT_REGION)).to_be_visible()
            expect(self.page.locator(Loc.MAILING_REGION)).to_be_visible()
            expect(self.page.locator(Loc.UPDATE_DETAILS_BTN)).to_be_enabled()
            self.step.set_actual("Hồ sơ hiển thị vùng định danh, liên hệ và địa chỉ nhận thư.")

    def test_tc_prf_ac_02_nric_visibility_button_toggles_accessible_name(self, authenticated_parent, fs08_data):
        """TC-PRF-AC-02: Show NRIC and Hide NRIC are mutually visible states."""
        profile = ParentProfilePage(self.page)
        profile.open(fs08_data["base_url"])
        with self.step("Hiện rồi che NRIC", expected="Tên nút đổi từ Show NRIC sang Hide NRIC và trở lại."):
            show = self.page.get_by_role("button", name="Show NRIC", exact=True)
            expect(show).to_be_visible()
            show.click()
            expect(self.page.get_by_role("button", name="Hide NRIC", exact=True)).to_be_visible()
            self.page.get_by_role("button", name="Hide NRIC", exact=True).click()
            expect(self.page.get_by_role("button", name="Show NRIC", exact=True)).to_be_visible()
            self.step.set_actual("Trạng thái che/hiện NRIC đổi theo accessible name của nút.")

    def test_tc_prf_ac_03_edit_mode_exposes_seven_labeled_fields(self, authenticated_parent, fs08_data):
        """TC-PRF-AC-03: edit mode exposes all seven observed textboxes."""
        profile = ParentProfilePage(self.page)
        profile.open(fs08_data["base_url"])
        labels = ("Mobile Number", "Email Address", "Block", "Street", "Unit", "Postal code", "Country")
        with self.step("Mở biểu mẫu cập nhật", expected="Form có đủ bảy trường với accessible labels."):
            profile.click_update_details()
            form = self.page.get_by_role("form", name="Update details", exact=True)
            expect(form).to_be_visible()
            for label in labels:
                expect(form.get_by_role("textbox", name=label, exact=True)).to_be_visible()
            expect(form.get_by_role("button", name="Save changes", exact=True)).to_be_disabled()
            expect(form.get_by_role("button", name="Cancel", exact=True)).to_be_visible()
            self.step.set_actual("Form cập nhật hiển thị đủ bảy trường, Save disabled và Cancel.")

    def test_tc_prf_ac_04_pristine_form_keeps_save_disabled(self, authenticated_parent, fs08_data):
        """TC-PRF-AC-04: Save remains disabled before any form field is changed."""
        profile = ParentProfilePage(self.page)
        profile.open(fs08_data["base_url"])
        with self.step("Mở form và kiểm tra trạng thái ban đầu", expected="Save changes bị disabled khi form chưa thay đổi."):
            profile.click_update_details()
            expect(self.page.get_by_role("button", name="Save changes", exact=True)).to_be_disabled()
            self.step.set_actual("Form ở trạng thái pristine và Save changes đang disabled.")

    def test_tc_prf_ac_05_dirty_form_enables_save(self, authenticated_parent, fs08_data):
        """TC-PRF-AC-05: a valid fixture value different from the current value enables Save."""
        profile = ParentProfilePage(self.page)
        profile.open(fs08_data["base_url"])
        with self.step("Thay Mobile Number bằng dữ liệu test hợp lệ", expected="Save changes chuyển sang enabled."):
            profile.click_update_details()
            mobile = self.page.get_by_role("textbox", name="Mobile Number", exact=True)
            test_value = fs08_data["profile_update_valid"]["phoneNumber"]
            if mobile.input_value() == test_value:
                test_value = fs08_data["profile_update_restore"]["phoneNumber"]
            mobile.fill(test_value)
            expect(self.page.get_by_role("button", name="Save changes", exact=True)).to_be_enabled()
            self.step.set_actual("Thay đổi fixture đã bật nút Save changes; chưa submit form.")

    def test_tc_prf_ac_06_cancel_discards_unsaved_edit(self, authenticated_parent, fs08_data):
        """TC-PRF-AC-06: Cancel returns to view mode without submitting the edit."""
        profile = ParentProfilePage(self.page)
        profile.open(fs08_data["base_url"])
        with self.step("Thay đổi Mobile Number rồi hủy", expected="Cancel thoát edit mode mà không lưu."):
            profile.click_update_details()
            mobile = self.page.get_by_role("textbox", name="Mobile Number", exact=True)
            test_value = fs08_data["profile_update_valid"]["phoneNumber"]
            if mobile.input_value() == test_value:
                test_value = fs08_data["profile_update_restore"]["phoneNumber"]
            mobile.fill(test_value)
            expect(self.page.get_by_role("button", name="Save changes", exact=True)).to_be_enabled()
            self.page.get_by_role("button", name="Cancel", exact=True).click()
            expect(self.page.get_by_role("heading", name="My Profile", exact=True)).to_be_visible()
            expect(self.page.get_by_role("button", name="Update details", exact=True)).to_be_visible()
            self.step.set_actual("Hủy thay đổi quay về view mode, không gửi thao tác lưu.")

    @pytest.mark.validation
    @pytest.mark.parametrize("case_id,label,data_path,check", _profile_validation_cases())
    def test_tc_prf_val_profile_fields(self, authenticated_parent, fs08_data, case_id, label, data_path, check):
        """Profile field validation cases use fixture vectors and observed accessible labels."""
        form = _open_profile_form(self.page, fs08_data)
        field = form.get_by_role("textbox", name=label, exact=True)
        value = fs08_data["profile_bva_dataset"]
        for part in data_path.split("."):
            value = value[int(part)] if part.isdigit() else value[part]
        with self.step(f"{case_id}: nhập dữ liệu vào {label}", expected="Field phản ánh validation theo ma trận."):
            expect(field).to_be_visible()
            if check == "default":
                expect(field).to_have_value("Singapore")
            elif check == "optional":
                field.fill("")
                field.press("Tab")
                expect(field).not_to_have_attribute("aria-invalid", "true")
            else:
                field.fill(value)
                field.press("Tab")
                if check == "invalid":
                    expect(field).to_have_attribute("aria-invalid", "true")
                elif check == "normalize_phone":
                    expect(field).to_have_value("91234567")
                elif check == "preserve_zero":
                    expect(field).to_have_value("018956")
                elif check == "trim":
                    expect(field).to_have_value("Test Street")
                elif check == "max_length":
                    expect(field).to_have_value(value[:100])
                elif check == "max_email":
                    assert len(value) == 150
                    expect(field).to_have_value(value)
                elif check == "safe_text":
                    expect(field).to_have_value(value)
                    expect(self.page.get_by_role("heading", name="My Profile", exact=True)).to_be_visible()
                elif valid:
                    expect(field).not_to_have_attribute("aria-invalid", "true")
            self.step.set_actual(f"{case_id}: kiểm tra trạng thái trực tiếp trên form, không submit thay đổi.")
