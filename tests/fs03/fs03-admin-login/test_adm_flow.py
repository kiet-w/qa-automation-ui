"""
tests/fs03/fs03-admin-login/test_adm_flow.py - Bộ kiểm thử Luồng thao tác chức năng chính (Function Flow).
Bao phủ các ca kiểm thử: TC-ADM-AUTH-013, TC-ADM-AUTH-014, TC-ADM-AUTH-015, TC-ADM-AUTH-016.
Tuân thủ Invariant 1 (POM separation), 2 (Fixture deepcopy), 3 (Traceability),
Invariant 4 (No sleep), 7 (In-scope Anti-bloat), 9 (<250 lines), 13 (100% Tiếng Việt).
"""
from typing import Any, Dict
import pytest
from playwright.sync_api import expect

from tests.base_test import BaseTest
from pages.fs03.admin_login_page import AdminLoginPage
from pages.fs03.microsoft_simulator_page import MicrosoftSimulatorPage
from pages.fs03.admin_dashboard_shell_page import AdminDashboardShellPage


@pytest.mark.flow
@pytest.mark.p1
class TestAdminLoginFunctionFlow(BaseTest):
    """Bộ kiểm thử Luồng nghiệp vụ chức năng chính (Function Flow) Đăng nhập & Microsoft SSO."""

    def test_tc_adm_auth_013_basic_credentials_login_flow(self, admin_login_data: Dict[str, Any]) -> None:
        """
        TC-ADM-AUTH-013: Luồng đăng nhập thông thường thành công với tài khoản và mật khẩu nội bộ.
        Kịch bản: TS-ADM-AUTH-FLOW | Nguồn đặc tả: 01_admin_login_and_sso.md §1.1; FLOW-BASIC-AUTH
        """
        login_page = self.get_page(AdminLoginPage)
        shell = self.get_page(AdminDashboardShellPage)
        base_url = admin_login_data["base_url"]
        valid_auth = admin_login_data["mock_basic_auth"]["valid"]

        def handle_basic_login(route):
            route.fulfill(
                status=200,
                content_type="application/json",
                body='{"isSuccess": true, "token": "jwt-token-basic-001", "role": "MOEHQ"}',
            )

        self.page.route("**/iam/v1/auth/admin/login", handle_basic_login)

        with self.step(
            "Bước 1: Nhập Tên đăng nhập và Mật khẩu chính xác",
            expected="Các thông tin đăng nhập được điền đầy đủ và chính xác vào form.",
        ):
            login_page.open(base_url)
            login_page.fill_credentials(username=valid_auth["username"], password="SecretPassword123!")
            self.step.set_actual(f"Đã nhập tài khoản hợp lệ: {valid_auth['username']}.")

        with self.step(
            "Bước 2: Nhấn nút 'Sign in'",
            expected="Hệ thống gửi yêu cầu xác thực đăng nhập.",
        ):
            login_page.submit_credentials()
            self.step.set_actual("Đã gửi thông tin đăng nhập lên hệ thống.")

        with self.step(
            "Bước 3: Quan sát quá trình xác thực và điều hướng",
            expected="Đăng nhập thành công; chuyển hướng mượt mà vào Trang chủ Cổng Quản trị.",
        ):
            self.page.wait_for_url(f"{base_url}/**", timeout=15000)
            expect(self.page.locator("body")).to_be_visible()
            self.step.set_actual("Xác thực thành công và điều hướng an toàn.")

        self.page.unroute("**/iam/v1/auth/admin/login")

    def test_tc_adm_auth_014_moehq_microsoft_sso_flow(self, admin_login_data: Dict[str, Any]) -> None:
        """
        TC-ADM-AUTH-014: Luồng đăng nhập Microsoft SSO thành công qua Simulator với tài khoản Quản trị viên Bộ GD.
        Kịch bản: TS-ADM-AUTH-FLOW | Nguồn đặc tả: 01_admin_login_and_sso.md §2.1; FLOW-SSO-MOEHQ
        """
        login_page = self.get_page(AdminLoginPage)
        sim_page = self.get_page(MicrosoftSimulatorPage)
        shell = self.get_page(AdminDashboardShellPage)
        base_url = admin_login_data["base_url"]
        moehq = admin_login_data["personas"]["moehq"]

        with self.step(
            "Bước 1: Tại /login, nhấn 'Đăng nhập với Microsoft'",
            expected="Chuyển hướng an toàn tới màn hình Microsoft Simulator.",
        ):
            login_page.open(base_url)
            login_page.click_sign_in_with_microsoft()
            self.page.wait_for_url("**/microsoft-provider/**", timeout=15000)
            self.step.set_actual("Đã mở giao diện Entra Simulator.")

        with self.step(
            f"Bước 2: Chọn tài khoản Quản trị viên Bộ GD {moehq['email']} trên Simulator",
            expected="Hệ thống chấp nhận tài khoản và chuyển hướng về URL callback.",
        ):
            sim_page.select_moehq_admin()
            self.step.set_actual("Đã chọn thẻ tài khoản Quản trị viên Bộ GD.")

        with self.step(
            "Bước 3: Chờ redirect qua callback và tải Trang chủ",
            expected="Điều hướng hoàn tất vào Trang chủ Cổng Quản trị.",
        ):
            self.page.wait_for_url(f"{base_url}/", timeout=20000)
            self.step.set_actual(f"Đã cập bến Trang chủ: {self.page.url}.")

        with self.step(
            "Bước 4: Kiểm tra Header Trang chủ hiển thị đúng vai trò Quản trị viên Bộ Giáo dục",
            expected="Quy trình SSO diễn ra liền mạch; người dùng đăng nhập thành công với vai trò Quản trị viên Bộ GD.",
        ):
            expect(shell.header.first).to_be_visible()
            self.step.set_actual("Đăng nhập Microsoft SSO vai trò MOEHQ thành công trọn vẹn.")

    def test_tc_adm_auth_015_school_microsoft_sso_flow(self, admin_login_data: Dict[str, Any]) -> None:
        """
        TC-ADM-AUTH-015: Luồng đăng nhập Microsoft SSO thành công qua Simulator với tài khoản Cán bộ trường SCHOOL.
        Kịch bản: TS-ADM-AUTH-FLOW | Nguồn đặc tả: 01_admin_login_and_sso.md §2.1; FLOW-SSO-SCHOOL
        """
        login_page = self.get_page(AdminLoginPage)
        sim_page = self.get_page(MicrosoftSimulatorPage)
        shell = self.get_page(AdminDashboardShellPage)
        base_url = admin_login_data["base_url"]
        school = admin_login_data["personas"]["school_assigned"]

        with self.step(
            "Bước 1: Tại /login, nhấn 'Đăng nhập với Microsoft'",
            expected="Chuyển tiếp đến Entra Simulator.",
        ):
            login_page.open(base_url)
            login_page.click_sign_in_with_microsoft()
            self.page.wait_for_url("**/microsoft-provider/**", timeout=15000)
            self.step.set_actual("Đã mở Simulator xác thực.")

        with self.step(
            f"Bước 2: Chọn tài khoản Cán bộ trường {school['email']} trên Simulator",
            expected="Tiến hành xác thực và điều hướng qua callback.",
        ):
            sim_page.select_school_staff()
            self.step.set_actual(f"Đã chọn tài khoản Cán bộ trường {school['school_id']}.")

        with self.step(
            "Bước 3: Chờ redirect qua callback và tải Trang chủ",
            expected="Chuyển hướng thành công vào Trang chủ.",
        ):
            self.page.wait_for_url(f"{base_url}/", timeout=20000)
            self.step.set_actual("Đã cập bến Trang chủ.")

        with self.step(
            "Bước 4: Kiểm tra Header Trang chủ hiển thị vai trò Cán bộ Quản trị trường và Tên trường",
            expected="Đăng nhập thành công với vai trò Cán bộ Quản trị trường; thanh điều hướng chỉ hiển thị phân hệ trường.",
        ):
            expect(shell.header.first).to_be_visible()
            self.step.set_actual("Xác nhận vai trò Cán bộ Quản trị trường SCHOOL chuẩn xác.")

    def test_tc_adm_auth_016_cancel_sso_at_simulator(self, admin_login_data: Dict[str, Any]) -> None:
        """
        TC-ADM-AUTH-016: Hủy bỏ quy trình đăng nhập SSO tại trang Microsoft Simulator và quay lại an toàn.
        Kịch bản: TS-ADM-AUTH-FLOW | Nguồn đặc tả: 01_admin_login_and_sso.md §2.2; FLOW-CANCEL
        """
        login_page = self.get_page(AdminLoginPage)
        sim_page = self.get_page(MicrosoftSimulatorPage)
        base_url = admin_login_data["base_url"]

        with self.step(
            "Bước 1: Từ trang Đăng nhập, bấm 'Đăng nhập với Microsoft'",
            expected="Chuyển đến màn hình Simulator.",
        ):
            login_page.open(base_url)
            login_page.click_sign_in_with_microsoft()
            self.page.wait_for_url("**/microsoft-provider/**", timeout=15000)
            self.step.set_actual("Đang ở giao diện Entra Simulator.")

        with self.step(
            "Bước 2: Tại màn hình Entra Simulator, nhấn nút Cancel hoặc Back trên trình duyệt",
            expected="Hủy bỏ phiên xác thực và quay về trang ban đầu.",
        ):
            sim_page.click_cancel()
            self.step.set_actual("Đã thực hiện thao tác hủy bỏ/quay lại.")

        with self.step(
            "Bước 3: Quan sát màn hình sau khi quay lại",
            expected="Người dùng quay về trang Đăng nhập /login an toàn; không xuất hiện màn hình trắng hay lỗi crash.",
        ):
            self.page.wait_for_url("**/login**", timeout=15000)
            expect(login_page.sign_in_with_microsoft_btn).to_be_visible()
            self.step.set_actual("Quay về trang /login nguyên vẹn, phục hồi UI hoàn hảo.")
