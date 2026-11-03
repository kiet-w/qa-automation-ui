"""
tests/testcase5173/01_admin_login_and_sso/test_adm_val.py - Bộ kiểm thử Xác thực dữ liệu & Trạng thái Form (Validation).
Bao phủ các ca kiểm thử: TC-ADM-AUTH-010, TC-ADM-AUTH-011, TC-ADM-AUTH-012, TC-ADM-AUTH-013.
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

    def test_tc_adm_auth_010_mandatory_fields_validation(self, admin_login_data: Dict[str, Any]) -> None:
        """
        TC-ADM-AUTH-010: Kiểm tra bắt buộc nhập (Mandatory Fields): Báo lỗi khi để trống Tên đăng nhập hoặc Mật khẩu.
        Kịch bản: TS-ADM-AUTH-VAL | Nguồn đặc tả: 01_admin_login_and_sso.md §1.1; VAL-MANDATORY; LoginPage.tsx:132-150
        """
        login_page = self.get_page(AdminLoginPage)
        base_url = admin_login_data["base_url"]
        user_req_msg = admin_login_data["expected_strings"]["en"]["usernameRequired"]
        pass_req_msg = admin_login_data["expected_strings"]["en"]["passwordRequired"]

        with self.step(
            "Bước 1: Truy cập http://localhost:5173/login, để trống cả ô Username và Password",
            expected="Các ô nhập liệu hoàn toàn trống dữ liệu.",
        ):
            login_page.open(base_url)
            login_page.fill_credentials(username="", password="")
            self.step.set_actual("Đã để trống Username và Password.")

        with self.step(
            "Bước 2: Nhấn nút 'Sign in'",
            expected="Form chặn submit, không gửi request tới API backend.",
        ):
            login_page.submit_credentials()
            self.step.set_actual("Đã nhấn nút Sign in.")

        with self.step(
            "Bước 3: Quan sát trạng thái các ô nhập và thông báo lỗi",
            expected=f"Ô Username báo lỗi '{user_req_msg}'; ô Password báo lỗi '{pass_req_msg}'; các trường bật viền đỏ/aria-invalid.",
        ):
            username_el = login_page.username_input
            password_el = login_page.password_input

            # required có sẵn trước khi submit nên không chứng minh validation
            # đã chạy. Kiểm tra trạng thái lỗi và đúng thông báo sau thao tác.
            expect(username_el).to_have_attribute("aria-invalid", "true")
            expect(password_el).to_have_attribute("aria-invalid", "true")
            expect(self.page.get_by_text(user_req_msg, exact=True)).to_be_visible()
            expect(self.page.get_by_text(pass_req_msg, exact=True)).to_be_visible()
            self.step.set_actual("Hệ thống hiển thị trạng thái bắt buộc nhập liệu chính xác.")

    def test_tc_adm_auth_011_trim_username_whitespace(self, admin_login_data: Dict[str, Any]) -> None:
        """
        TC-ADM-AUTH-011: Tự động cắt tỉa khoảng trắng (Trim Whitespace) ở Tên đăng nhập trước khi gửi xác thực.
        Kịch bản: TS-ADM-AUTH-VAL | Nguồn đặc tả: 01_admin_login_and_sso.md §1.1; VAL-TRIM-WHITESPACE; LoginPage.tsx:45/69
        """
        login_page = self.get_page(AdminLoginPage)
        base_url = admin_login_data["base_url"]
        raw_user = "  admin@IAM.edu.vn  "
        expected_trimmed = "admin@IAM.edu.vn"
        submitted_payloads = []

        def capture_login_payload(route):
            submitted_payloads.append(route.request.post_data_json or {})
            route.fulfill(
                status=401,
                content_type="application/json",
                body='{"isSuccess":false,"message":"Invalid credentials"}',
            )

        self.page.route("**/iam/v1/auth/admin/login", capture_login_payload)

        with self.step(
            f"Bước 1: Tại ô Username, nhập chuỗi có khoảng trắng ở đầu và cuối: '{raw_user}'",
            expected=f"Ô Username nhận chuỗi nhập thô '{raw_user}'.",
        ):
            login_page.open(base_url)
            login_page.fill_credentials(username=raw_user, password="Password123!")
            self.step.set_actual(f"Đã nhập Username có khoảng trắng: '{raw_user}'.")

        with self.step(
            "Bước 2: Nhập mật khẩu hợp lệ vào ô Password",
            expected="Ô Password nhận dữ liệu mật khẩu an toàn.",
        ):
            expect(login_page.password_input).not_to_be_empty()
            self.step.set_actual("Mật khẩu đã được điền sẵn sàng.")

        with self.step(
            "Bước 3: Gửi đăng nhập nội bộ và kiểm tra payload xác thực",
            expected=f"Payload gửi tới API chứa username đã trim là '{expected_trimmed}'.",
        ):
            login_page.submit_credentials()
            expect(login_page.error_alert.first).to_be_visible()
            assert len(submitted_payloads) == 1, "Không ghi nhận đúng một request đăng nhập nội bộ"
            submitted_username = submitted_payloads[0].get("username")
            assert submitted_username == expected_trimmed, (
                f"Username gửi lên API chưa được trim: {submitted_username!r}"
            )
            self.step.set_actual(f"Payload xác thực gửi username đã trim: '{submitted_username}'.")

        self.page.unroute("**/iam/v1/auth/admin/login")

    def test_tc_adm_auth_012_toggle_password_visibility(self, admin_login_data: Dict[str, Any]) -> None:
        """
        TC-ADM-AUTH-012: Nút ẩn/hiện mật khẩu (Show/Hide Password): Chuyển đổi thuộc tính type giữa password và text.
        Kịch bản: TS-ADM-AUTH-VAL | Nguồn đặc tả: 01_admin_login_and_sso.md §1.1; DOM-TOGGLE; LoginPage.tsx:143-158
        """
        login_page = self.get_page(AdminLoginPage)
        base_url = admin_login_data["base_url"]
        sample_pwd = "AdminSecret@2026"

        with self.step(
            f"Bước 1: Nhập mật khẩu '{sample_pwd}' vào ô Password",
            expected="Ô Password lưu giữ chuỗi mật khẩu.",
        ):
            login_page.open(base_url)
            login_page.fill_credentials(password=sample_pwd)
            self.step.set_actual("Đã nhập mật khẩu mẫu vào form.")

        with self.step(
            "Bước 2: Kiểm tra thuộc tính type ban đầu của ô Password",
            expected="Ban đầu ô Password có type='password' (ký tự bị che dấu).",
        ):
            initial_type = login_page.get_password_input_type()
            assert initial_type == "password", f"Type ban đầu không phải là 'password': {initial_type}"
            self.step.set_actual("Trường mật khẩu ban đầu được che dấu dạng password.")

        with self.step(
            "Bước 3: Nhấn vào nút biểu tượng con mắt (Show password)",
            expected=f"Thuộc tính type chuyển sang 'text', hiển thị rõ chuỗi '{sample_pwd}'.",
        ):
            login_page.toggle_password_visibility()
            revealed_type = login_page.get_password_input_type()
            assert revealed_type == "text", f"Sau khi bật hiển thị, type không chuyển sang 'text': {revealed_type}"
            assert login_page.password_input.input_value() == sample_pwd
            self.step.set_actual("Mật khẩu đã hiển thị dưới dạng văn bản rõ ràng.")

        with self.step(
            "Bước 4: Nhấn lại vào nút biểu tượng con mắt một lần nữa (Hide password)",
            expected="Thuộc tính type chuyển ngược lại thành 'password'; giá trị mật khẩu bảo toàn nguyên vẹn 100%.",
        ):
            login_page.toggle_password_visibility()
            hidden_type = login_page.get_password_input_type()
            assert hidden_type == "password", f"Sau khi ẩn lại, type không chuyển về 'password': {hidden_type}"
            assert login_page.password_input.input_value() == sample_pwd
            self.step.set_actual("Mật khẩu đã được ẩn lại an toàn, bảo toàn giá trị nguyên vẹn.")

    def test_tc_adm_auth_013_clear_validation_on_retyping(self, admin_login_data: Dict[str, Any]) -> None:
        """
        TC-ADM-AUTH-013: Tự động xóa thông báo lỗi khi người dùng bắt đầu nhập lại vào ô dữ liệu.
        Kịch bản: TS-ADM-AUTH-VAL | Nguồn đặc tả: 01_admin_login_and_sso.md §1.1; VAL-CLEAR-ON-INPUT; LoginPage.tsx:132
        """
        login_page = self.get_page(AdminLoginPage)
        base_url = admin_login_data["base_url"]
        username_required = admin_login_data["expected_strings"]["en"]["usernameRequired"]

        with self.step(
            "Bước 1: Để trống ô Username và Password, nhấn nút 'Sign in' để kích hoạt trạng thái lỗi validation",
            expected="Kích hoạt cảnh báo lỗi bắt buộc nhập.",
        ):
            login_page.open(base_url)
            login_page.fill_credentials(username="", password="")
            login_page.submit_credentials()
            self.step.set_actual("Đã kích hoạt trạng thái lỗi validation.")

        with self.step(
            "Bước 2: Đặt con trỏ vào ô Username và nhập một ký tự bất kỳ ('a')",
            expected="Ô nhập nhận ký tự mới.",
        ):
            login_page.username_input.type("a")
            self.step.set_actual("Đã bắt đầu nhập ký tự 'a' vào ô Username.")

        with self.step(
            "Bước 3: Quan sát thông báo lỗi dưới ô Username",
            expected="Ngay khi gõ ký tự vào ô Username, thông báo lỗi và viền đỏ cảnh báo lập tức biến mất.",
        ):
            aria_invalid = login_page.username_input.get_attribute("aria-invalid")
            assert aria_invalid != "true", "Trạng thái aria-invalid vẫn còn kích hoạt sau khi nhập lại"
            expect(self.page.get_by_text(username_required, exact=True)).to_be_hidden()
            self.step.set_actual("Trạng thái lỗi đã được xóa bỏ tự động khi người dùng bắt đầu nhập lại.")
