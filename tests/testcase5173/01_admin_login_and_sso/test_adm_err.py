"""
tests/testcase5173/01_admin_login_and_sso/test_adm_err.py - Bộ kiểm thử Xử lý ngoại lệ & Phục hồi lỗi (Error Handling).
Bao phủ các ca kiểm thử: TC-ADM-AUTH-014, TC-ADM-AUTH-015, TC-ADM-AUTH-016, TC-ADM-AUTH-017, TC-ADM-AUTH-018.
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
    """Bộ kiểm thử Xử lý ngoại lệ, cảnh báo lỗi và Chống gửi trùng lặp (Debounce) trên Form Đăng nhập & SSO."""

    def test_tc_adm_auth_014_invalid_credentials_error_alert(self, admin_login_data: Dict[str, Any]) -> None:
        """
        TC-ADM-AUTH-014: Đăng nhập thất bại do sai Tên đăng nhập hoặc Mật khẩu: Hiển thị Alert báo lỗi.
        Kịch bản: TS-ADM-AUTH-ERR | Nguồn đặc tả: 01_admin_login_and_sso.md §1.1; ERR-INVALID-CREDS; LoginPage.tsx:103
        """
        login_page = self.get_page(AdminLoginPage)
        base_url = admin_login_data["base_url"]
        invalid_auth = admin_login_data["mock_basic_auth"]["invalid"]
        login_failed_msg = admin_login_data["expected_strings"]["en"]["loginFailed"]

        def handle_failed_login(route):
            route.fulfill(
                status=401,
                content_type="application/json",
                body=f'{{"isSuccess": false, "message": "{login_failed_msg}. Invalid username or password."}}',
            )

        self.page.route("**/iam/v1/auth/admin/login", handle_failed_login)

        with self.step(
            f"Bước 1: Nhập Username ({invalid_auth['username']}) không tồn tại hoặc sai Mật khẩu vào form",
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
            "Bước 3: Quan sát thông báo lỗi và trạng thái trang",
            expected=f"Hiển thị Alert [role='alert'] tiêu đề '{login_failed_msg}'; giữ nguyên tại trang /login.",
        ):
            expect(login_page.error_alert.first).to_be_visible(timeout=10000)
            expect(login_page.error_alert.first).to_contain_text(login_failed_msg)
            assert "login" in self.page.url, "Người dùng bị điều hướng dù đăng nhập thất bại"
            self.step.set_actual(f"Hộp cảnh báo lỗi hiển thị chính xác tiêu đề '{login_failed_msg}'.")

        self.page.unroute("**/iam/v1/auth/admin/login")

    def test_tc_adm_auth_015_oauth_state_mismatch_csrf(self, admin_login_data: Dict[str, Any]) -> None:
        """
        TC-ADM-AUTH-015: Trạng thái OAuth State không hợp lệ (State Mismatch / CSRF): Hiển thị Toast lỗi và chuyển về /login.
        Kịch bản: TS-ADM-AUTH-ERR | Nguồn đặc tả: 01_admin_login_and_sso.md §2.2; ERR-INVALID-STATE; MicrosoftCallbackPage.tsx:113
        """
        login_page = self.get_page(AdminLoginPage)
        base_url = admin_login_data["base_url"]
        oauth_data = admin_login_data["oauth"]
        expected_msg = admin_login_data["expected_strings"]["en"]["oauthInvalidState"]

        with self.step(
            "Bước 1: Truy cập URL callback với giá trị state bị sai lệch không khớp với sessionStorage",
            expected="Khởi tạo phiên callback với state giả mạo.",
        ):
            login_page.open(base_url)
            # Lưu state gốc vào sessionStorage
            self.page.evaluate(
                f"""sessionStorage.setItem('edusave.admin.microsoft-oauth', JSON.stringify({{
                    'redirectUri': '{base_url}/login/microsoft/callback',
                    'state': '{oauth_data['valid_state']}',
                    'codeVerifier': 'verifier-abc',
                    'returnTo': '/'
                }}));"""
            )
            # Truy cập callback với state sai lệch
            login_page.open_callback(
                base_url=base_url,
                params=f"?code={oauth_data['valid_code']}&state={oauth_data['tampered_state']}",
            )
            self.step.set_actual(f"Đã mở callback với state sai: {oauth_data['tampered_state']}.")

        with self.step(
            "Bước 2: Quan sát phản hồi của trang callback",
            expected=f"Hệ thống phát hiện state không khớp, hiển thị Toast '{expected_msg}', tự động điều hướng về /login.",
        ):
            self.page.wait_for_url(f"**/login**", timeout=15000)
            expect(login_page.sign_in_with_microsoft_btn).to_be_visible()
            expect(login_page.toast_error).to_contain_text(expected_msg)
            self.step.set_actual(f"Phát hiện mismatch CSRF; bảo vệ hệ thống và chuyển về /login.")

    def test_tc_adm_auth_016_oauth_session_expired(self, admin_login_data: Dict[str, Any]) -> None:
        """
        TC-ADM-AUTH-016: Phiên làm việc OAuth hết hạn hoặc không tồn tại (Session Expired): Hiển thị Toast lỗi và chuyển về /login.
        Kịch bản: TS-ADM-AUTH-ERR | Nguồn đặc tả: 01_admin_login_and_sso.md §4.2; ERR-SESSION-EXPIRED; MicrosoftCallbackPage.tsx:105
        """
        login_page = self.get_page(AdminLoginPage)
        base_url = admin_login_data["base_url"]
        expected_msg = admin_login_data["expected_strings"]["en"]["oauthSessionExpired"]

        with self.step(
            "Bước 1: Mở phiên làm việc mới (không có OAuth session trong sessionStorage)",
            expected="Bộ nhớ sessionStorage hoàn toàn trống.",
        ):
            login_page.open(base_url)
            self.page.evaluate("sessionStorage.removeItem('edusave.admin.microsoft-oauth');")
            self.step.set_actual("Đã dọn sạch session trong sessionStorage.")

        with self.step(
            "Bước 2: Truy cập trực tiếp đường dẫn callback /login/microsoft/callback?code=any-code&state=any-state",
            expected="Trang callback tải và kiểm tra điều kiện session.",
        ):
            login_page.open_callback(base_url=base_url, params="?code=any-code&state=any-state")
            self.step.set_actual("Đã truy cập trực tiếp URL callback khi không có session.")

        with self.step(
            "Bước 3: Quan sát phản hồi của hệ thống",
            expected=f"Hệ thống kiểm tra !oauthSession, thông báo '{expected_msg}' và tự động chuyển về /login.",
        ):
            self.page.wait_for_url(f"**/login**", timeout=15000)
            expect(login_page.sign_in_with_microsoft_btn).to_be_visible()
            expect(login_page.toast_error).to_contain_text(expected_msg)
            self.step.set_actual("Tự động chuyển hướng về /login an toàn khi phiên OAuth không tồn tại.")

    def test_tc_adm_auth_017_oauth_provider_error(self, admin_login_data: Dict[str, Any]) -> None:
        """
        TC-ADM-AUTH-017: Lỗi phản hồi từ nhà cung cấp OAuth (Provider Error): Hiển thị Toast thông báo lỗi từ Provider.
        Kịch bản: TS-ADM-AUTH-ERR | Nguồn đặc tả: 01_admin_login_and_sso.md §4.2; ERR-PROVIDER-ERROR; MicrosoftCallbackPage.tsx:84
        """
        login_page = self.get_page(AdminLoginPage)
        base_url = admin_login_data["base_url"]
        error_desc = "The+user+declined+the+consent"

        with self.step(
            "Bước 1: Giả lập tình huống lỗi từ phía Microsoft Entra với tham số error và error_description",
            expected="Trang callback tiếp nhận URL chứa tham số báo lỗi của Provider.",
        ):
            login_page.open(base_url)
            login_page.open_callback(
                base_url=base_url,
                params=f"?error=access_denied&error_description={error_desc}",
            )
            self.step.set_actual("Đã điều hướng về callback với tham số lỗi của Provider.")

        with self.step(
            "Bước 2: Quan sát cách hệ thống tiếp nhận và xử lý tham số lỗi",
            expected="Hệ thống đọc tham số lỗi từ Provider, hiển thị Toast cảnh báo và tự động chuyển hướng về /login.",
        ):
            self.page.wait_for_url(f"**/login**", timeout=15000)
            expect(login_page.sign_in_with_microsoft_btn).to_be_visible()
            expect(login_page.toast_error).to_contain_text("The user declined the consent")
            self.step.set_actual("Đã xử lý thông điệp lỗi của Provider và chuyển người dùng về /login an toàn.")

    def test_tc_adm_auth_018_login_button_debounce_guard(self, admin_login_data: Dict[str, Any]) -> None:
        """
        TC-ADM-AUTH-018: Khóa tạm thời nút bấm (Debounce / Loading Guard): Ngăn chặn gửi trùng lặp yêu cầu khi bấm liên tiếp.
        Kịch bản: TS-ADM-AUTH-ERR | Nguồn đặc tả: 01_admin_login_and_sso.md §1.1; ERR-DEBOUNCE; LoginPage.tsx:54/165/179
        """
        login_page = self.get_page(AdminLoginPage)
        base_url = admin_login_data["base_url"]
        request_count = 0

        pending_route = None

        def count_auth_req(route):
            nonlocal request_count, pending_route
            request_count += 1
            pending_route = route

        self.page.route("**/iam/v1/auth/admin/microsoft/authorize-url**", count_auth_req)

        with self.step(
            "Bước 1: Tại trang Đăng nhập, chuẩn bị nhấn nút 'Sign in with Microsoft'",
            expected="Nút 'Sign in with Microsoft' hiển thị sẵn sàng nhận tương tác.",
        ):
            login_page.open(base_url)
            expect(login_page.sign_in_with_microsoft_btn).to_be_visible()
            self.step.set_actual("Nút Đăng nhập với Microsoft sẵn sàng.")

        with self.step(
            "Bước 2: Thực hiện click nhanh liên tiếp 2 lần vào nút 'Sign in with Microsoft'",
            expected="Nút chuyển trạng thái loading và bị vô hiệu hóa; chỉ có 1 request được gửi lên máy chủ.",
        ):
            login_page.sign_in_with_microsoft_btn.click(no_wait_after=True)
            # Chờ nút chuyển sang trạng thái disabled/loading
            expect(login_page.sign_in_with_microsoft_btn).to_be_disabled(timeout=5000)
            try:
                login_page.sign_in_with_microsoft_btn.click(timeout=300, no_wait_after=True, force=True)
            except Exception:
                pass

            # Fulfill request đang chờ
            if pending_route:
                pending_route.fulfill(
                    status=200,
                    content_type="application/json",
                    body='{"authorizeUrl": "http://localhost:5288/mock-debounce"}',
                )
            self.step.set_actual("Đã kích hoạt click nhanh và hoàn tất phản hồi.")

        with self.step(
            "Bước 3: Quan sát trạng thái nút bấm trong lúc đang gửi yêu cầu xác thực",
            expected="Ngăn chặn hoàn toàn việc gửi trùng lặp yêu cầu xác thực (request_count == 1).",
        ):
            assert request_count == 1, f"Kỳ vọng đúng một request, phát hiện {request_count} requests!"
            self.step.set_actual(f"Cơ chế debounce hoạt động hoàn hảo: Chỉ gửi {request_count} yêu cầu duy nhất.")

        self.page.unroute("**/iam/v1/auth/admin/microsoft/authorize-url**")
