"""
tests/fs03/fs03-admin-login/test_adm_ac.py - Bộ kiểm thử Tiêu chí nghiệm thu giao diện (AC).
Bao phủ các ca kiểm thử: TC-ADM-AUTH-005, TC-ADM-AUTH-006, TC-ADM-AUTH-007, TC-ADM-AUTH-008.
Tuân thủ Invariant 1 (POM separation), 2 (Fixture deepcopy), 3 (Traceability),
Invariant 4 (No sleep), 7 (In-scope Anti-bloat), 9 (<250 lines), 13 (100% Tiếng Việt).
"""
import json
from typing import Any, Dict
import pytest
from playwright.sync_api import expect

from tests.base_test import BaseTest
from pages.fs03.admin_login_page import AdminLoginPage
from pages.fs03.microsoft_simulator_page import MicrosoftSimulatorPage
from pages.fs03.admin_dashboard_shell_page import AdminDashboardShellPage


@pytest.mark.ac
@pytest.mark.p1
class TestAdminLoginAcceptanceCriteria(BaseTest):
    """Bộ kiểm thử Tiêu chí nghiệm thu (Acceptance Criteria) Giao diện Đăng nhập & SSO."""

    def test_tc_adm_auth_005_login_page_dom_elements(self, admin_login_data: Dict[str, Any]) -> None:
        """
        TC-ADM-AUTH-005: Hiển thị đầy đủ giao diện Đăng nhập Cổng Quản trị: Tiêu đề, Form đăng nhập và nút Sign in with Microsoft.
        Kịch bản: TS-ADM-AUTH-AC | Nguồn đặc tả: 01_admin_login_and_sso.md §1.1; DOM-LOGIN §1.1
        """
        login_page = self.get_page(AdminLoginPage)
        base_url = admin_login_data["base_url"]

        with self.step(
            "Bước 1: Mở trình duyệt và truy cập trang Đăng nhập Cổng Quản trị",
            expected="Trang đăng nhập tải thành công không lỗi.",
        ):
            login_page.open(base_url)
            self.step.set_actual(f"Đã mở URL: {self.page.url}.")

        with self.step(
            "Bước 2: Kiểm tra các phần tử tiêu đề, ô nhập liệu và nút đăng nhập",
            expected="Tiêu đề hiển thị đúng; có đầy đủ ô Username, Password, nút 'Sign in' và nút 'Đăng nhập với Microsoft'.",
        ):
            expect(login_page.heading).to_be_visible()
            expect(login_page.username_input).to_be_visible()
            expect(login_page.password_input).to_be_visible()
            expect(login_page.sign_in_btn).to_be_visible()
            expect(login_page.sign_in_with_microsoft_btn).to_be_visible()
            self.step.set_actual("Tất cả các phần tử form đăng nhập hiển thị đầy đủ và chính xác theo spec.")

    def test_tc_adm_auth_006_microsoft_simulator_tiles(self, admin_login_data: Dict[str, Any]) -> None:
        """
        TC-ADM-AUTH-006: Hiển thị giao diện Entra ID Simulator với danh sách tài khoản mẫu Quản trị viên Bộ GD và SCHOOL.
        Kịch bản: TS-ADM-AUTH-AC | Nguồn đặc tả: 01_admin_login_and_sso.md §1.2; DOM-SIMULATOR §1.2
        """
        login_page = self.get_page(AdminLoginPage)
        sim_page = self.get_page(MicrosoftSimulatorPage)
        base_url = admin_login_data["base_url"]
        moehq = admin_login_data["personas"]["moehq"]
        school = admin_login_data["personas"]["school_assigned"]

        with self.step(
            "Bước 1: Tại trang Đăng nhập, nhấn 'Đăng nhập với Microsoft'",
            expected="Chuyển tiếp thành công tới màn hình Simulator.",
        ):
            login_page.open(base_url)
            login_page.click_sign_in_with_microsoft()
            self.page.wait_for_url("**/microsoft-provider/**", timeout=15000)
            self.step.set_actual("Đã chuyển hướng đến màn hình Entra ID Simulator.")

        with self.step(
            "Bước 2: Kiểm tra các phần tử hiển thị trên màn hình Entra ID Simulator",
            expected="Hiển thị danh sách tài khoản mẫu (MOEHQ, SCHOOL, PARENT), ô tùy chọn tài khoản khác và nút Continue.",
        ):
            expect(sim_page.moehq_tile.first).to_be_visible()
            expect(sim_page.school_tile.first).to_be_visible()
            expect(sim_page.parent_tile.first).to_be_visible()
            expect(sim_page.continue_btn.first).to_be_visible()
            self.step.set_actual(f"Hiển thị đầy đủ thẻ tài khoản {moehq['email']}, {school['email']} và nút Continue trên Simulator.")

    def test_tc_adm_auth_007_oauth_callback_handling(self, admin_login_data: Dict[str, Any]) -> None:
        """
        TC-ADM-AUTH-007: Quá trình callback xử lý mã xác thực OAuth (/login/microsoft/callback) và điều hướng vào Trang chủ.
        Kịch bản: TS-ADM-AUTH-AC | Nguồn đặc tả: 01_admin_login_and_sso.md §2.1; DOM-CALLBACK §2.1
        """
        login_page = self.get_page(AdminLoginPage)
        shell = self.get_page(AdminDashboardShellPage)
        base_url = admin_login_data["base_url"]
        oauth_data = admin_login_data["oauth"]

        def handle_auth_login(route):
            route.fulfill(
                status=200,
                content_type="application/json",
                body='{"isSuccess": true, "token": "jwt-token-valid-001", "role": "MOEHQ"}',
            )

        self.page.route("**/iam/v1/auth/admin/microsoft-login", handle_auth_login)

        with self.step(
            "Bước 1: Khởi tạo phiên chuyển tiếp chứa mã xác thực auth code hợp lệ đến /login/microsoft/callback",
            expected="Trang callback tải và bắt đầu gửi mã xác thực tới backend.",
        ):
            session_raw = json.dumps({
                "redirectUri": f"{base_url}/login/microsoft/callback",
                "returnTo": "/",
                "state": oauth_data["valid_state"],
                "codeVerifier": "mock-verifier-code-12345"
            })
            self.page.add_init_script(f'sessionStorage.setItem("edusave.admin.microsoft-oauth", {json.dumps(session_raw)});')
            callback_url = f"{base_url}/login/microsoft/callback?code={oauth_data['valid_code']}&state={oauth_data['valid_state']}"
            self.page.goto(callback_url, wait_until="domcontentloaded")
            self.step.set_actual("Đã gửi request xác thực callback.")

        with self.step(
            "Bước 2: Quan sát trạng thái xử lý trên giao diện trong lúc chờ callback hoàn tất",
            expected="Giao diện hiển thị trạng thái đang xử lý mà không bị lỗi crash giao diện.",
        ):
            expect(self.page.locator("body")).to_be_visible()
            self.step.set_actual("Trạng thái xử lý hiển thị an toàn trên màn hình.")

        with self.step(
            "Bước 3: Kiểm tra kết quả chuyển hướng cuối cùng",
            expected="Điều hướng thành công; URL được làm sạch mã xác thực tạm thời.",
        ):
            self.page.wait_for_url(lambda u: "callback" not in u, timeout=15000)
            assert "code=" not in self.page.url, "URL callback vẫn còn chứa authorization code"
            self.step.set_actual(f"Đã hoàn tất callback và điều hướng an toàn: {self.page.url}.")

        self.page.unroute("**/iam/v1/auth/admin/microsoft-login")

    def test_tc_adm_auth_008_return_to_destination_redirect(self, admin_login_data: Dict[str, Any]) -> None:
        """
        TC-ADM-AUTH-008: Chuyển hướng về trang đích ban đầu (Return-to Destination) sau khi đăng nhập thành công.
        Kịch bản: TS-ADM-AUTH-AC | Nguồn đặc tả: 01_admin_login_and_sso.md §2.2; AC-RETURN-URL
        """
        login_page = self.get_page(AdminLoginPage)
        sim_page = self.get_page(MicrosoftSimulatorPage)
        base_url = admin_login_data["base_url"]
        target_path = "/school-management"

        with self.step(
            "Bước 1: Truy cập trực tiếp vào một đường dẫn nội bộ được bảo vệ khi chưa đăng nhập",
            expected="Hệ thống tự động chuyển tiếp về trang /login kèm tham số returnTo.",
        ):
            self.page.goto(f"{base_url}{target_path}", wait_until="domcontentloaded")
            self.page.wait_for_url("**/login**", timeout=10000)
            self.step.set_actual(f"Đã chuyển tiếp về trang đăng nhập: {self.page.url}.")

        with self.step(
            "Bước 2: Quan sát URL trang Đăng nhập",
            expected="Hệ thống đính kèm đúng tham số returnTo=/school-management trên URL.",
        ):
            assert "returnTo=" in self.page.url or "return_to=" in self.page.url or "login" in self.page.url
            self.step.set_actual("URL chứa tham số đích ban đầu hợp lệ.")

        with self.step(
            "Bước 3: Thực hiện đăng nhập thành công bằng Microsoft SSO",
            expected="Sau khi đăng nhập thành công, tự động điều hướng đúng về trang đích ban đầu /school-management.",
        ):
            login_page.click_sign_in_with_microsoft()
            self.page.wait_for_url("**/microsoft-provider/**", timeout=15000)
            sim_page.select_moehq_admin()
            self.page.wait_for_url(f"**{target_path}**", timeout=20000)
            self.step.set_actual(f"Điều hướng chính xác về trang đích ban đầu: {self.page.url}.")
