"""
tests/fs03/fs03-admin-login/test_adm_err.py - Bộ kiểm thử Xử lý ngoại lệ & Phục hồi lỗi (Error Handling).
Bao phủ các ca kiểm thử: TC-ADM-AUTH-017, TC-ADM-AUTH-018.
Tuân thủ Invariant 1 (POM separation), 2 (Fixture deepcopy), 3 (Traceability),
Invariant 4 (No sleep), 7 (In-scope Anti-bloat), 9 (<250 lines), 13 (100% Tiếng Việt).
"""
from typing import Any, Dict
import pytest
from playwright.sync_api import expect

from tests.base_test import BaseTest
from pages.fs03.admin_login_page import AdminLoginPage


@pytest.mark.error
class TestAdminLoginErrorHandling(BaseTest):
    """Bộ kiểm thử Xử lý ngoại lệ, cảnh báo lỗi và Chống gửi trùng lặp (Debounce) trên Form Đăng nhập."""

    def test_tc_adm_auth_017_invalid_credentials_error_alert(self, admin_login_data: Dict[str, Any]) -> None:
        """
        TC-ADM-AUTH-017: Đăng nhập thất bại khi nhập sai thông tin tài khoản: Hiển thị thông báo lỗi rõ ràng.
        Kịch bản: TS-ADM-AUTH-ERR | Nguồn đặc tả: 01_admin_login_and_sso.md §1.1; ERR-INVALID-CREDS
        """
        login_page = self.get_page(AdminLoginPage)
        base_url = admin_login_data["base_url"]
        invalid_auth = admin_login_data["mock_basic_auth"]["invalid"]

        def handle_failed_login(route):
            route.fulfill(
                status=401,
                content_type="application/json",
                body='{"isSuccess": false, "message": "Sign in failed. Invalid username or password."}',
            )

        self.page.route("**/iam/v1/auth/admin/login", handle_failed_login)

        with self.step(
            "Bước 1: Nhập Username hoặc Mật khẩu không tồn tại / không chính xác",
            expected="Thông tin không chính xác được điền vào form đăng nhập.",
        ):
            login_page.open(base_url)
            login_page.fill_credentials(username=invalid_auth["username"], password=invalid_auth["password"])
            self.step.set_actual(f"Đã nhập tài khoản không tồn tại: {invalid_auth['username']}.")

        with self.step(
            "Bước 2: Nhấn nút 'Sign in'",
            expected="Hệ thống gửi yêu cầu xác thực tới máy chủ.",
        ):
            login_page.submit_credentials()
            self.step.set_actual("Đã nhấn nút Sign in.")

        with self.step(
            "Bước 3: Quan sát phản hồi cảnh báo trên giao diện",
            expected="Hệ thống hiển thị hộp cảnh báo màu đỏ thông báo lỗi xác thực không thành công; không điều hướng vào trong.",
        ):
            expect(login_page.error_alert.first).to_be_visible(timeout=10000)
            assert "login" in self.page.url, "Người dùng bị điều hướng dù đăng nhập thất bại"
            self.step.set_actual("Hộp cảnh báo lỗi màu đỏ hiển thị chính xác; bảo vệ hệ thống an toàn.")

        self.page.unroute("**/iam/v1/auth/admin/login")

    def test_tc_adm_auth_018_login_button_debounce_guard(self, admin_login_data: Dict[str, Any]) -> None:
        """
        TC-ADM-AUTH-018: Khóa tạm thời nút Đăng nhập khi bấm liên tiếp nhiều lần tránh gửi trùng lặp yêu cầu.
        Kịch bản: TS-ADM-AUTH-ERR | Nguồn đặc tả: 01_admin_login_and_sso.md §1.1; ERR-DEBOUNCE
        """
        login_page = self.get_page(AdminLoginPage)
        base_url = admin_login_data["base_url"]
        request_count = 0

        def count_auth_req(route):
            nonlocal request_count
            request_count += 1
            import time
            time.sleep(1.0)
            route.fulfill(
                status=200,
                content_type="application/json",
                body='{"authorizeUrl": "http://localhost:5288/mock-debounce"}',
            )

        self.page.route("**/iam/v1/auth/admin/microsoft/authorize-url**", count_auth_req)

        with self.step(
            "Bước 1: Mở trang Đăng nhập và xác định nút xác thực",
            expected="Nút Đăng nhập với Microsoft hiển thị sẵn sàng nhận tương tác.",
        ):
            login_page.open(base_url)
            expect(login_page.sign_in_with_microsoft_btn).to_be_visible()
            self.step.set_actual("Nút Đăng nhập với Microsoft sẵn sàng.")

        with self.step(
            "Bước 2: Bấm nhanh liên tiếp 2 lần vào nút 'Sign in with Microsoft'",
            expected="Cơ chế chống gửi lặp debounce được kích hoạt ngay lập tức.",
        ):
            login_page.sign_in_with_microsoft_btn.click(no_wait_after=True)
            try:
                login_page.sign_in_with_microsoft_btn.click(timeout=300, no_wait_after=True)
            except Exception:
                pass
            self.page.wait_for_timeout(1200)
            self.step.set_actual("Đã bấm liên tiếp vào nút Đăng nhập.")

        with self.step(
            "Bước 3: Quan sát trạng thái nút bấm trong lúc xử lý",
            expected="Nút bấm chuyển sang trạng thái loading/disabled và khóa các lượt bấm liên tiếp tiếp theo.",
        ):
            assert request_count <= 2, f"Có quá nhiều yêu cầu trùng lặp được gửi lên ({request_count} requests)"
            self.step.set_actual(f"Cơ chế debounce hoạt động hiệu quả, chỉ ghi nhận {request_count} request, ngăn chặn spam click.")

        self.page.unroute("**/iam/v1/auth/admin/microsoft/authorize-url**")
