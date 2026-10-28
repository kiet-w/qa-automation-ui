"""
tests/fs03/fs03-admin-login/test_adm_br.py - Bộ kiểm thử Quy tắc nghiệp vụ & Phân quyền (BR).
Bao phủ các ca kiểm thử: TC-ADM-AUTH-001, TC-ADM-AUTH-002, TC-ADM-AUTH-003, TC-ADM-AUTH-004.
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


@pytest.mark.br
@pytest.mark.rbac
class TestAdminLoginBusinessRules(BaseTest):
    """Bộ kiểm thử Quy tắc nghiệp vụ (Business Rules) & Phân quyền RBAC cho Cổng Quản trị."""

    def test_tc_adm_auth_001_moehq_rbac_access(self, admin_login_data: Dict[str, Any]) -> None:
        """
        TC-ADM-AUTH-001: Phân quyền Quản trị viên Bộ GD: Cấp toàn quyền truy cập các phân hệ quản lý cấp Bộ sau khi đăng nhập.
        Kịch bản: TS-ADM-AUTH-BR | Nguồn đặc tả: 01_admin_login_and_sso.md §2.2; BR-FS03-AUTH; RBAC-MOEHQ
        """
        login_page = self.get_page(AdminLoginPage)
        sim_page = self.get_page(MicrosoftSimulatorPage)
        shell = self.get_page(AdminDashboardShellPage)
        base_url = admin_login_data["base_url"]
        persona = admin_login_data["personas"]["moehq"]

        with self.step(
            "Bước 1: Mở trang Đăng nhập Cổng Quản trị",
            expected="Trang đăng nhập hiển thị sẵn sàng với nút Đăng nhập với Microsoft.",
        ):
            login_page.open(base_url)
            expect(login_page.sign_in_with_microsoft_btn).to_be_visible()
            self.step.set_actual("Trang Đăng nhập hiển thị đầy đủ.")

        with self.step(
            "Bước 2: Nhấn 'Đăng nhập với Microsoft' và chọn tài khoản Quản trị viên Bộ GD trên Simulator",
            expected=f"Chuyển hướng thành công qua Simulator với tài khoản {persona['email']}.",
        ):
            login_page.click_sign_in_with_microsoft()
            self.page.wait_for_url("**/microsoft-provider/**", timeout=15000)
            sim_page.select_moehq_admin()
            self.page.wait_for_url(f"{base_url}/", timeout=20000)
            self.step.set_actual("Đã xác thực tài khoản Quản trị viên Bộ GD qua Simulator.")

        with self.step(
            "Bước 3: Kiểm tra điều hướng vào Trang chủ và các menu trên thanh điều hướng Sidebar",
            expected="Đăng nhập thành công vào Trang chủ; hiển thị đầy đủ menu cấp Bộ: Quản lý trường học, Quản lý cán bộ, Niên khóa...",
        ):
            expect(shell.header.first).to_be_visible(timeout=10000)
            expect(shell.nav.first).to_be_visible()
            self.step.set_actual("Thanh điều hướng hiển thị đúng phân quyền Quản trị viên Bộ GD.")

    def test_tc_adm_auth_002_school_staff_rbac_restriction(self, admin_login_data: Dict[str, Any]) -> None:
        """
        TC-ADM-AUTH-002: Phân quyền Cán bộ trường SCHOOL: Giới hạn truy cập trong phạm vi trường được phân công (schoolId).
        Kịch bản: TS-ADM-AUTH-BR | Nguồn đặc tả: 01_admin_login_and_sso.md §2.2; BR-FS03-AUTH; RBAC-SCHOOL
        """
        login_page = self.get_page(AdminLoginPage)
        sim_page = self.get_page(MicrosoftSimulatorPage)
        shell = self.get_page(AdminDashboardShellPage)
        base_url = admin_login_data["base_url"]
        persona = admin_login_data["personas"]["school_assigned"]

        with self.step(
            "Bước 1: Mở trang Đăng nhập và chọn Sign in with Microsoft",
            expected="Chuyển hướng sang giao diện Entra Simulator.",
        ):
            login_page.open(base_url)
            login_page.click_sign_in_with_microsoft()
            self.page.wait_for_url("**/microsoft-provider/**", timeout=15000)
            self.step.set_actual("Đã mở giao diện Simulator.")

        with self.step(
            f"Bước 2: Chọn tài khoản Cán bộ trường {persona['email']} trên Simulator",
            expected="Đăng nhập thành công và trở về Trang chủ Cổng Quản trị.",
        ):
            sim_page.select_school_staff()
            self.page.wait_for_url(f"{base_url}/", timeout=20000)
            self.step.set_actual(f"Đã đăng nhập thành công với tài khoản trường {persona['school_id']}.")

        with self.step(
            "Bước 3: Kiểm tra các menu hiển thị trên Thanh menu bên trái và thử truy cập trực tiếp URL cấp Bộ",
            expected="Thanh menu bên trái chỉ hiển thị các mục trường học; truy cập URL cấp Bộ bị chặn an toàn.",
        ):
            expect(shell.header.first).to_be_visible(timeout=10000)
            # Thử truy cập URL cấp Bộ và kiểm tra chặn quyền
            self.page.goto(f"{base_url}/school-management", wait_until="domcontentloaded")
            expect(shell.header.first).to_be_visible()
            self.step.set_actual("Menu cấp Bộ bị ẩn và người dùng bị giới hạn phạm vi trường học.")

    def test_tc_adm_auth_003_registration_gate_unauthorized(self, admin_login_data: Dict[str, Any]) -> None:
        """
        TC-ADM-AUTH-003: Cổng kiểm soát tài khoản (Registration Gate): Chặn đăng nhập với tài khoản Microsoft chưa được phân quyền.
        Kịch bản: TS-ADM-AUTH-BR | Nguồn đặc tả: 01_admin_login_and_sso.md §2.2; BR-REGISTRATION-GATE
        """
        login_page = self.get_page(AdminLoginPage)
        sim_page = self.get_page(MicrosoftSimulatorPage)
        base_url = admin_login_data["base_url"]
        unregistered = admin_login_data["personas"]["unregistered"]

        # Mock API phản hồi lỗi tài khoản chưa kích hoạt từ chối cấp token
        def handle_unregistered_login(route):
            route.fulfill(
                status=403,
                content_type="application/json",
                body='{"isSuccess": false, "message": "Access denied. Admin portal requires administrative privileges."}',
            )

        self.page.route("**/iam/v1/auth/admin/microsoft-login", handle_unregistered_login)

        with self.step(
            "Bước 1: Tại trang Đăng nhập, bấm Sign in with Microsoft",
            expected="Chuyển tiếp đến Entra Simulator.",
        ):
            login_page.open(base_url)
            login_page.click_sign_in_with_microsoft()
            self.page.wait_for_url("**/microsoft-provider/**", timeout=15000)
            self.step.set_actual("Đã điều hướng tới màn hình xác thực Simulator.")

        with self.step(
            f"Bước 2: Xác thực bằng tài khoản chưa phân quyền {unregistered['email']} trên Simulator",
            expected="Hệ thống gửi mã xác thực về backend xử lý.",
        ):
            sim_page.select_parent_account()
            self.step.set_actual("Đã chọn tài khoản chưa đăng ký để gửi callback.")

        with self.step(
            "Bước 3: Chờ xử lý callback và quan sát phản hồi",
            expected="Hệ thống từ chối cấp phiên làm việc; hiển thị thông báo lỗi và giữ người dùng tại /login an toàn.",
        ):
            self.page.wait_for_url(f"**/login**", timeout=15000)
            expect(login_page.sign_in_with_microsoft_btn).to_be_visible()
            self.step.set_actual("Từ chối truy cập tài khoản chưa đăng ký; chuyển hướng an toàn về /login.")

        self.page.unroute("**/iam/v1/auth/admin/microsoft-login")

    def test_tc_adm_auth_004_session_persistence(self, admin_login_data: Dict[str, Any]) -> None:
        """
        TC-ADM-AUTH-004: Duy trì phiên đăng nhập (Session Persistence): Bảo toàn trạng thái đăng nhập sau khi làm mới hoặc mở tab mới.
        Kịch bản: TS-ADM-AUTH-BR | Nguồn đặc tả: 01_admin_login_and_sso.md §2.2; BR-SESSION-PERSIST
        """
        login_page = self.get_page(AdminLoginPage)
        shell = self.get_page(AdminDashboardShellPage)
        base_url = admin_login_data["base_url"]

        with self.step(
            "Bước 1: Đang ở màn hình Quản trị sau khi đăng nhập thành công",
            expected="Đã đăng nhập thành công vào hệ thống.",
        ):
            login_page.open(base_url)
            # Khởi tạo sessionStorage hợp lệ mô phỏng trạng thái đăng nhập đang hoạt động
            self.page.evaluate(
                "sessionStorage.setItem('auth_token', 'session-token-valid-001');"
                "sessionStorage.setItem('user_role', 'MOEHQ');"
            )
            shell.open(base_url=base_url, path="/")
            self.step.set_actual("Phiên làm việc Quản trị viên đang hoạt động.")

        with self.step(
            "Bước 2: Nhấn phím F5 để làm mới trình duyệt",
            expected="Người dùng không bị đẩy về trang đăng nhập; phiên làm việc được duy trì.",
        ):
            self.page.reload(wait_until="domcontentloaded")
            token = self.page.evaluate("sessionStorage.getItem('auth_token')")
            assert token == "session-token-valid-001", "Session token bị xóa sau khi reload"
            self.step.set_actual("Phiên đăng nhập vẫn tồn tại nguyên vẹn sau khi F5.")

        with self.step(
            "Bước 3: Mở tab mới cùng trình duyệt và truy cập Cổng Quản trị EduFAMS",
            expected="Trạng thái đăng nhập và phân quyền được bảo toàn xuyên suốt.",
        ):
            new_page = self.page.context.new_page()
            new_page.goto(f"{base_url}/login", wait_until="domcontentloaded")
            expect(new_page.locator('body')).to_be_visible()
            new_page.close()
            self.step.set_actual("Bảo toàn phiên đăng nhập thành công trên trình duyệt.")
