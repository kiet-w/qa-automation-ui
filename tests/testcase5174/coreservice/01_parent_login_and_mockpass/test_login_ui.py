"""UI automation mapped to testcase5174 core-service login cases."""
import pytest
from playwright.sync_api import expect

from pages.fs08.singpass_login_page import SingpassLoginPage
from tests.base_test import BaseTest


@pytest.mark.ui
@pytest.mark.ac
class TestParentLoginUI(BaseTest):
    def test_tc_auth_03_login_screen_exposes_accessible_controls(self, fs08_data):
        """TC-AUTH-03: login heading and Singpass entry control are visible and enabled."""
        login = SingpassLoginPage(self.page)
        with self.step("Mở trang đăng nhập", expected="Tiêu đề và nút Singpass hiển thị."):
            login.open(fs08_data["base_url"])
            expect(self.page.get_by_role("heading", name="Parent portal login", exact=True)).to_be_visible()
            expect(self.page.get_by_role("button", name="Sign in with Singpass", exact=True)).to_be_enabled()
            self.step.set_actual("Trang đăng nhập hiển thị tiêu đề và nút Singpass đang bật.")

    def test_tc_auth_04_valid_test_persona_reaches_dashboard(self, fs08_data):
        """TC-AUTH-04: selecting a configured test persona completes the visible login flow."""
        persona = fs08_data["personas"]["PAR-NORMAL-01"]
        login = SingpassLoginPage(self.page)
        with self.step("Mở Singpass simulator và chọn persona fixture", expected="Danh sách persona cho phép chọn tài khoản test."):
            login.open(fs08_data["base_url"])
            login.click_sign_in_with_singpass()
            expect(self.page.get_by_role("heading", name="Log in with Singpass", exact=True)).to_be_visible()
            login.select_mockpass_persona(persona["nric"])
            self.step.set_actual("Đã chọn persona được cấu hình trong fixture.")

        with self.step("Xác nhận đăng nhập", expected="Portal chuyển đến dashboard đã xác thực."):
            login.submit_mockpass_login()
            expect(self.page.get_by_role("heading", name="Your family’s education, at a glance", exact=True)).to_be_visible(timeout=25000)
            self.step.set_actual(f"Dashboard hiển thị tại {self.page.url}.")
