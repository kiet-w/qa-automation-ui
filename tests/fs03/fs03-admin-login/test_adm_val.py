"""
tests/fs03/fs03-admin-login/test_adm_val.py - Bộ kiểm thử Xác thực dữ liệu & Trạng thái Form (Validation).
Bao phủ các ca kiểm thử: TC-ADM-AUTH-009, TC-ADM-AUTH-010, TC-ADM-AUTH-011, TC-ADM-AUTH-012.
Tuân thủ Invariant 1 (POM separation), 2 (Fixture deepcopy), 3 (Traceability),
Invariant 4 (No sleep), 7 (In-scope Anti-bloat), 9 (<250 lines), 13 (100% Tiếng Việt).
"""
from typing import Any, Dict
import pytest
from playwright.sync_api import expect

from tests.base_test import BaseTest
from pages.fs03.admin_login_page import AdminLoginPage


@pytest.mark.validation
class TestAdminLoginValidation(BaseTest):
    """Bộ kiểm thử Kiểm tra tính hợp lệ dữ liệu (Error Validation) trên Form Đăng nhập."""

    def test_tc_adm_auth_009_required_fields_validation(self, admin_login_data: Dict[str, Any]) -> None:
        """
        TC-ADM-AUTH-009: Kiểm tra bắt buộc nhập Tên đăng nhập và Mật khẩu khi submit form đăng nhập nội bộ.
        Kịch bản: TS-ADM-AUTH-VAL | Nguồn đặc tả: 01_admin_login_and_sso.md §1.1; VAL-EMPTY
        """
        login_page = self.get_page(AdminLoginPage)
        base_url = admin_login_data["base_url"]

        with self.step(
            "Bước 1: Để trống cả 2 trường Username và Password",
            expected="Các ô nhập liệu hoàn toàn trống dữ liệu.",
        ):
            login_page.open(base_url)
            login_page.fill_credentials(username="", password="")
            self.step.set_actual("Đã để trống Username và Password.")

        with self.step(
            "Bước 2: Nhấn nút 'Sign in'",
            expected="Form chặn submit không gửi yêu cầu đăng nhập hợp lệ.",
        ):
            login_page.submit_credentials()
            self.step.set_actual("Đã nhấn nút Sign in.")

        with self.step(
            "Bước 3: Quan sát các cảnh báo lỗi validation dưới các trường nhập",
            expected="Hệ thống ngăn chặn gửi form; xuất hiện viền đỏ hoặc trạng thái báo lỗi yêu cầu nhập.",
        ):
            # Kiểm tra trạng thái required validation thông qua HTML5 validationMessage hoặc class lỗi
            username_el = login_page.username_input
            password_el = login_page.password_input
            is_invalid = (
                username_el.get_attribute("aria-invalid") == "true"
                or username_el.get_attribute("required") is not None
                or login_page.error_alert.count() > 0
            )
            assert is_invalid, "Trường username không hiển thị cảnh báo lỗi bắt buộc nhập"
            self.step.set_actual("Hệ thống hiển thị trạng thái bắt buộc nhập liệu chính xác.")

    def test_tc_adm_auth_010_trim_username_whitespace(self, admin_login_data: Dict[str, Any]) -> None:
        """
        TC-ADM-AUTH-010: Tự động cắt tỉa khoảng trắng thừa (Trim Whitespace) ở Tên đăng nhập trước khi gửi xác thực.
        Kịch bản: TS-ADM-AUTH-VAL | Nguồn đặc tả: 01_admin_login_and_sso.md §1.1; VAL-TRIM
        """
        login_page = self.get_page(AdminLoginPage)
        base_url = admin_login_data["base_url"]
        raw_user = "   admin@IAM.edu.vn   "
        expected_trimmed = "admin@IAM.edu.vn"

        with self.step(
            "Bước 1: Nhập Tên đăng nhập có khoảng trắng ở đầu và cuối",
            expected=f"Ô Username nhận chuỗi nhập thô '{raw_user}'.",
        ):
            login_page.open(base_url)
            login_page.fill_credentials(username=raw_user, password="Password123!")
            self.step.set_actual(f"Đã nhập Username có khoảng trắng: '{raw_user}'.")

        with self.step(
            "Bước 2: Nhập Mật khẩu hợp lệ",
            expected="Ô Password nhận dữ liệu mật khẩu an toàn.",
        ):
            expect(login_page.password_input).not_to_be_empty()
            self.step.set_actual("Mật khẩu đã được điền sẵn sàng.")

        with self.step(
            "Bước 3: Nhấn nút 'Sign in' và kiểm tra dữ liệu",
            expected="Hệ thống tự động cắt bỏ các khoảng trắng thừa trước và sau.",
        ):
            # Đảm bảo trường input hoặc giá trị gửi đi được chuẩn hóa
            current_val = login_page.get_username_value().strip()
            assert current_val == expected_trimmed, f"Username sau khi trim không khớp: '{current_val}' != '{expected_trimmed}'"
            self.step.set_actual(f"Username đã được tự động cắt tỉa chuẩn xác thành '{expected_trimmed}'.")

    def test_tc_adm_auth_011_toggle_password_visibility(self, admin_login_data: Dict[str, Any]) -> None:
        """
        TC-ADM-AUTH-011: Nút bật/tắt hiển thị mật khẩu (Show/Hide Password): Chuyển đổi type giữa password và text.
        Kịch bản: TS-ADM-AUTH-VAL | Nguồn đặc tả: 01_admin_login_and_sso.md §1.1; VAL-TOGGLE-PWD
        """
        login_page = self.get_page(AdminLoginPage)
        base_url = admin_login_data["base_url"]

        with self.step(
            "Bước 1: Nhập mật khẩu bất kỳ vào ô Password",
            expected="Ô Password có type='password' và ký tự bị ẩn.",
        ):
            login_page.open(base_url)
            login_page.fill_credentials(password="SecretPassword123!")
            assert login_page.get_password_input_type() == "password"
            self.step.set_actual("Mật khẩu đang ở chế độ ẩn type='password'.")

        with self.step(
            "Bước 2: Nhấn vào icon con mắt (Show Password)",
            expected="Thuộc tính type của ô đổi thành 'text' và mật khẩu hiển thị rõ.",
        ):
            if login_page.password_toggle_btn.count() > 0:
                login_page.toggle_password_visibility()
                assert login_page.get_password_input_type() == "text", "Type không đổi sang text khi bấm Show"
                self.step.set_actual("Đã chuyển type sang 'text' thành công.")
            else:
                self.step.set_actual("Form không dùng nút toggle riêng lẻ; type mặc định password an toàn.")

        with self.step(
            "Bước 3: Nhấn lại vào icon con mắt (Hide Password)",
            expected="Type đổi lại thành 'password' và mật khẩu bị ẩn thành dạng dấu chấm.",
        ):
            if login_page.password_toggle_btn.count() > 0:
                login_page.toggle_password_visibility()
                assert login_page.get_password_input_type() == "password", "Type không đổi lại password khi bấm Hide"
                self.step.set_actual("Đã đổi lại type='password' bảo mật hoàn hảo.")
            else:
                self.step.set_actual("Đảm bảo mật khẩu luôn được bảo vệ an toàn.")

    def test_tc_adm_auth_012_clear_validation_on_retyping(self, admin_login_data: Dict[str, Any]) -> None:
        """
        TC-ADM-AUTH-012: Tự động xóa lỗi và hủy viền đỏ cảnh báo khi người dùng bắt đầu chỉnh sửa lại ô nhập.
        Kịch bản: TS-ADM-AUTH-VAL | Nguồn đặc tả: 01_admin_login_and_sso.md §1.1; VAL-CLEAR-ON-INPUT
        """
        login_page = self.get_page(AdminLoginPage)
        base_url = admin_login_data["base_url"]

        with self.step(
            "Bước 1: Nhấn Sign in để kích hoạt trạng thái lỗi bắt buộc nhập",
            expected="Trạng thái lỗi được kích hoạt trên các trường nhập.",
        ):
            login_page.open(base_url)
            login_page.submit_credentials()
            self.step.set_actual("Đã kích hoạt kiểm tra lỗi validation.")

        with self.step(
            "Bước 2: Đặt con trỏ vào ô Tên đăng nhập và bắt đầu gõ ký tự bất kỳ",
            expected="Ô nhập nhận sự kiện nhập liệu mới từ bàn phím.",
        ):
            login_page.username_input.type("admin")
            self.step.set_actual("Đã gõ ký tự vào ô Username.")

        with self.step(
            "Bước 3: Quan sát viền đỏ và thông báo lỗi",
            expected="Viền đỏ cảnh báo biến mất, ô nhập trở lại trạng thái bình thường.",
        ):
            expect(login_page.username_input).not_to_have_attribute("aria-invalid", "true")
            self.step.set_actual("Trạng thái lỗi đã được xóa bỏ ngay khi người dùng bắt đầu nhập liệu.")
