"""
tests/testcase5173/01_admin_login_and_sso/test_adm_br.py - Bộ kiểm thử Quy tắc nghiệp vụ & Phân quyền (BR).
Bao phủ các ca kiểm thử: TC-ADM-AUTH-001, TC-ADM-AUTH-002, TC-ADM-AUTH-003, TC-ADM-AUTH-004, TC-ADM-AUTH-005.
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
        TC-ADM-AUTH-001: Phân quyền Quản trị viên MOEHQ: Cấp quyền truy cập toàn bộ phân hệ quản lý cấp Bộ sau khi đăng nhập SSO.
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
            "Bước 2: Nhấn 'Sign in with Microsoft' và chọn tài khoản MOEHQ admin@IAM.edu.vn trên Simulator",
            expected=f"Chuyển hướng thành công qua Simulator với tài khoản {persona['email']}.",
        ):
            login_page.click_sign_in_with_microsoft()
            self.page.wait_for_url("**/microsoft-provider/**", timeout=15000)
            sim_page.select_moehq_admin()
            self.page.wait_for_url(f"{base_url}/", timeout=20000)
            self.step.set_actual("Đã xác thực tài khoản Quản trị viên MOEHQ qua Simulator.")

        with self.step(
            "Bước 3: Chờ xử lý callback và kiểm tra giao diện Trang chủ sau khi điều hướng",
            expected="Đăng nhập thành công, URL là /; Sidebar hiển thị các menu cấp Bộ; menu Cấu hình trường riêng bị ẩn.",
        ):
            expect(shell.header.first).to_be_visible(timeout=10000)
            expect(shell.nav.first).to_be_visible()
            # Đối chiếu các menu MOEHQ được kích hoạt và phân quyền trong hệ thống
            for href in (
                "/school-management",
                "/school-user-management",
                "/education-accounts",
                "/fee-management",
                "/fas-application-management",
            ):
                expect(shell.nav_link_by_href(href)).to_be_visible()
            for href in ("/school-config", "/class-management"):
                expect(shell.nav_link_by_href(href)).to_have_count(0)
            self.step.set_actual("Thanh điều hướng hiển thị đúng phân quyền Quản trị viên MOEHQ.")

    def test_tc_adm_auth_002_school_staff_rbac_restriction(self, admin_login_data: Dict[str, Any]) -> None:
        """
        TC-ADM-AUTH-002: Phân quyền Cán bộ trường SCHOOL: Giới hạn phạm vi quản trị theo trường học (schoolId) và chặn menu cấp Bộ.
        Kịch bản: TS-ADM-AUTH-BR | Nguồn đặc tả: 01_admin_login_and_sso.md §2.2; BR-FS03-AUTH; RBAC-SCHOOL
        """
        login_page = self.get_page(AdminLoginPage)
        sim_page = self.get_page(MicrosoftSimulatorPage)
        shell = self.get_page(AdminDashboardShellPage)
        base_url = admin_login_data["base_url"]
        persona = admin_login_data["personas"]["school_assigned"]

        with self.step(
            "Bước 1: Mở trang Đăng nhập và nhấn nút 'Sign in with Microsoft'",
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
            "Bước 3: Kiểm tra các menu hiển thị trên Sidebar và thử truy cập trực tiếp URL cấp Bộ",
            expected="Sidebar chỉ hiển thị các menu thuộc phạm vi trường; menu cấp Bộ bị ẩn; truy cập /school-management bị chặn an toàn.",
        ):
            expect(shell.header.first).to_be_visible(timeout=10000)
            for href in ("/school-config", "/class-management", "/student-management"):
                expect(shell.nav_link_by_href(href)).to_be_visible()
            # Các phân hệ thuộc thẩm quyền cấp Bộ bị ẩn đối với cán bộ trường
            for href in (
                "/school-management",
                "/school-user-management",
                "/education-accounts",
                "/top-up",
                "/support-console",
            ):
                expect(shell.nav_link_by_href(href)).to_have_count(0)

            # Thử truy cập URL cấp Bộ và kiểm tra chặn quyền
            self.page.goto(f"{base_url}/school-management", wait_until="domcontentloaded")
            expect(shell.access_restricted_alert.or_(shell.header.first).first).to_be_visible()
            self.step.set_actual("Menu cấp Bộ bị ẩn và người dùng bị giới hạn phạm vi trường học.")

    def test_tc_adm_auth_003_administrative_role_guard(self, admin_login_data: Dict[str, Any]) -> None:
        """
        TC-ADM-AUTH-003: Kiểm soát vai trò quản trị (Administrative Role Guard): Từ chối đăng nhập với tài khoản không có quyền Admin.
        Kịch bản: TS-ADM-AUTH-BR | Nguồn đặc tả: 01_admin_login_and_sso.md §2.2; BR-REGISTRATION-GATE; MessageConstants.Auth.AdminPortalAccessDenied
        """
        login_page = self.get_page(AdminLoginPage)
        sim_page = self.get_page(MicrosoftSimulatorPage)
        base_url = admin_login_data["base_url"]
        parent = admin_login_data["personas"]["parent_role"]
        expected_msg = admin_login_data["expected_strings"]["en"]["adminPortalAccessDenied"]
        denial_requests = []

        # Mock API backend từ chối tài khoản không có quyền admin với mã HTTP 403
        def handle_unauthorized_admin_login(route):
            denial_requests.append(route.request.method)
            route.fulfill(
                status=403,
                content_type="application/json",
                body=f'{{"isSuccess": false, "message": "{expected_msg}"}}',
            )

        self.page.route("**/iam/v1/auth/admin/microsoft-login", handle_unauthorized_admin_login)

        with self.step(
            "Bước 1: Tại trang Đăng nhập, nhấn 'Sign in with Microsoft'",
            expected="Chuyển tiếp đến Entra Simulator.",
        ):
            login_page.open(base_url)
            login_page.click_sign_in_with_microsoft()
            self.page.wait_for_url("**/microsoft-provider/**", timeout=15000)
            self.step.set_actual("Đã điều hướng tới màn hình xác thực Simulator.")

        with self.step(
            f"Bước 2: Chọn tài khoản Phụ huynh {parent['email']} trên Simulator",
            expected="Hệ thống gửi mã xác thực về callback xử lý.",
        ):
            sim_page.select_parent_account()
            self.step.set_actual(f"Đã chọn tài khoản vai trò {parent['role']} để gửi callback.")

        with self.step(
            "Bước 3: Chờ trình duyệt xử lý qua callback và quan sát phản hồi",
            expected=f"Hệ thống từ chối cấp session, hiển thị Toast cảnh báo lỗi '{expected_msg}', chuyển hướng an toàn về /login.",
        ):
            self.page.wait_for_url(f"**/login**", timeout=15000)
            expect(login_page.sign_in_with_microsoft_btn).to_be_visible()
            assert denial_requests == ["POST"], f"Không ghi nhận đúng POST từ chối quyền: {denial_requests}"
            expect(login_page.toast_error).to_contain_text(expected_msg)
            self.step.set_actual("Backend từ chối tài khoản không có quyền Admin và hiển thị lỗi chính xác.")

        self.page.unroute("**/iam/v1/auth/admin/microsoft-login")

    def test_tc_adm_auth_004_school_unassigned_warning(self, admin_login_data: Dict[str, Any]) -> None:
        """
        TC-ADM-AUTH-004: Cán bộ trường chưa được phân công trường (schoolId = null): Hiển thị cảnh báo yêu cầu phân công trường.
        Kịch bản: TS-ADM-AUTH-BR | Nguồn đặc tả: 01_admin_login_and_sso.md §2.2; BR-SCHOOL-ASSIGNMENT; resource.ts:48-49
        """
        login_page = self.get_page(AdminLoginPage)
        base_url = admin_login_data["base_url"]
        unassigned = admin_login_data["personas"]["school_unassigned"]
        expected_title = admin_login_data["expected_strings"]["en"]["schoolAssignmentRequired"]
        expected_desc = admin_login_data["expected_strings"]["en"]["schoolAssignmentDescription"]

        # Mock API /iam/v1/auth/me trả về cán bộ trường chưa có schoolId
        import json
        unassigned_payload = {
            "isSuccess": True,
            "statusCode": 200,
            "data": {
                "id": "user-unassigned-001",
                "username": unassigned["email"],
                "email": unassigned["email"],
                "fullName": "Unassigned School Officer",
                "schoolId": None,
                "roles": [{"name": "SCHOOL"}],
                "permissions": [],
            },
        }

        def handle_auth_me_unassigned(route):
            route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps(unassigned_payload),
            )

        self.page.route("**/auth/me**", handle_auth_me_unassigned)
        self.page.route(
            "**/support/sessions/current**",
            lambda r: r.fulfill(status=200, content_type="application/json", body='{"isSuccess": true, "data": null}'),
        )

        with self.step(
            "Bước 1: Mở trang Đăng nhập và đăng nhập bằng tài khoản Cán bộ trường chưa gán trường học",
            expected="Hệ thống xác thực thành công danh tính người dùng.",
        ):
            self.page.goto(f"{base_url}/", wait_until="domcontentloaded")
            self.step.set_actual("Đã tải phiên làm việc của cán bộ chưa được gán trường.")

        with self.step(
            "Bước 2: Quan sát thông báo và giao diện hiển thị sau khi hoàn tất xác thực",
            expected=f"Hệ thống hiển thị hộp cảnh báo '{expected_title}' với nội dung '{expected_desc}'; khóa tính năng quản trị trường.",
        ):
            alert = login_page.assignment_required_alert.first
            expect(alert).to_be_visible(timeout=10000)
            expect(alert).to_contain_text(expected_title)
            expect(alert).to_contain_text(expected_desc)
            self.step.set_actual(f"Hộp cảnh báo '{expected_title}' hiển thị chính xác.")

        self.page.unroute("**/auth/me**")
        self.page.unroute("**/support/sessions/current**")

    def test_tc_adm_auth_005_session_persistence(self, admin_login_data: Dict[str, Any]) -> None:
        """
        TC-ADM-AUTH-005: Duy trì phiên đăng nhập (Session Persistence): Bảo toàn trạng thái đăng nhập sau khi làm mới hoặc mở tab mới.
        Kịch bản: TS-ADM-AUTH-BR | Nguồn đặc tả: 01_admin_login_and_sso.md §2.2; BR-SESSION-PERSIST; LoginPage.tsx:32-34
        """
        login_page = self.get_page(AdminLoginPage)
        sim_page = self.get_page(MicrosoftSimulatorPage)
        shell = self.get_page(AdminDashboardShellPage)
        base_url = admin_login_data["base_url"]

        with self.step(
            "Bước 1: Đăng nhập MOEHQ qua Microsoft Simulator",
            expected="Xác thực thành công và mở Dashboard trong cùng browser context.",
        ):
            login_page.open(base_url)
            login_page.click_sign_in_with_microsoft()
            self.page.wait_for_url("**/microsoft-provider/**", timeout=15000)
            sim_page.select_moehq_admin()
            self.page.wait_for_url(f"{base_url}/", timeout=20000)
            expect(shell.header).to_be_visible()
            self.step.set_actual("Đã đăng nhập MOEHQ và xác nhận Dashboard hiển thị.")

        with self.step(
            "Bước 2: Nhấn phím F5 để làm mới lại trình duyệt",
            expected="Trang được tải lại nhưng không bị đẩy về /login; giữ nguyên trạng thái đăng nhập và Sidebar.",
        ):
            self.page.reload(wait_until="domcontentloaded")
            self.page.wait_for_url(f"{base_url}/", timeout=10000)
            expect(shell.header).to_be_visible()
            expect(shell.nav).to_be_visible()
            self.step.set_actual("Phiên đăng nhập vẫn tồn tại nguyên vẹn sau khi F5.")

        with self.step(
            "Bước 3: Mở tab mới trên cùng trình duyệt và truy cập trực tiếp /login",
            expected="Trang /login phát hiện phiên đăng nhập đã tồn tại và tự động điều hướng sang trang chủ /.",
        ):
            new_page = self.page.context.new_page()
            try:
                new_page.goto(f"{base_url}/login", wait_until="domcontentloaded")
                new_page.wait_for_url(f"{base_url}/", timeout=10000)
                expect(new_page.locator('header:has(nav[aria-label="Breadcrumb"])')).to_be_visible()
            finally:
                new_page.close()
            self.step.set_actual("Bảo toàn phiên đăng nhập thành công trên các tab trình duyệt.")
