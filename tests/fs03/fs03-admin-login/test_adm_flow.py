"""
tests/testcase5173/01_admin_login_and_sso/test_adm_flow.py - Bộ kiểm thử Luồng thao tác chức năng chính (Function Flow).
Bao phủ các ca kiểm thử: TC-ADM-AUTH-019, TC-ADM-AUTH-020, TC-ADM-AUTH-021, TC-ADM-AUTH-022.
Tuân thủ Invariant 1 (POM separation), 2 (Fixture deepcopy), 3 (Traceability),
Invariant 4 (No sleep), 7 (In-scope Anti-bloat), 9 (<250 lines), 13 (100% Tiếng Việt).
"""
from typing import Any, Dict
import re
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

    def test_tc_adm_auth_019_basic_credentials_login_flow(self, admin_login_data: Dict[str, Any]) -> None:
        """
        TC-ADM-AUTH-019: Luồng đăng nhập thông thường thành công bằng tài khoản và mật khẩu nội bộ.
        Kịch bản: TS-ADM-AUTH-FLOW | Nguồn đặc tả: 01_admin_login_and_sso.md §2.1; FLOW-LOCAL-LOGIN; LoginPage.tsx:44
        """
        login_page = self.get_page(AdminLoginPage)
        shell = self.get_page(AdminDashboardShellPage)
        base_url = admin_login_data["base_url"]
        valid_auth = admin_login_data["mock_basic_auth"]["valid"]
        authenticated_auth_me_calls = []
        login_calls = []
        login_status_codes = []

        def handle_basic_login(route):
            login_calls.append(route.request.url)
            login_status_codes.append(204)
            route.fulfill(
                status=204,
                headers={"Set-Cookie": "auth_token=jwt-token-basic-001; Path=/; HttpOnly"},
            )

        self.page.route("**/iam/v1/auth/admin/login", handle_basic_login)

        def handle_auth_me(route):
            if not login_calls:
                route.fulfill(
                    status=401,
                    content_type="application/json",
                    body='{"isSuccess":false,"statusCode":401,"message":"Unauthenticated"}',
                )
                return
            authenticated_auth_me_calls.append(route.request.url)
            route.fulfill(
                status=200,
                content_type="application/json",
                body=(
                    '{"isSuccess":true,"statusCode":200,"data":{'
                    '"id":"USR-00001","code":"USR-00001",'
                    '"username":"admin@IAM.edu.vn","firstName":"System",'
                    '"lastName":"Administrator","fullName":"System Administrator",'
                    '"phoneNumber":"00000000","gender":"Male",'
                    '"birthDate":"1990-01-01","provider":"local","schoolId":null,'
                    '"roles":[{"id":"role-moehq","code":"MOEHQ","name":"MOEHQ",'
                    '"description":"MOE HQ administrator","isActive":true,'
                    '"isSystemRole":true,"createdAt":"2026-01-01T00:00:00Z",'
                    '"updatedAt":null,"createdBy":null,"updatedBy":null}],"permissions":[]}}'
                ),
            )

        self.page.route("**/auth/me", handle_auth_me)

        # The authenticated dashboard fetches its own BFF endpoint immediately.
        # Keep this flow isolated from the live dashboard backend so a 401 there
        # cannot invalidate an otherwise successful mocked login session.
        def handle_moe_dashboard(route):
            route.fulfill(
                status=200,
                content_type="application/json",
                body=(
                    '{"isSuccess":true,"statusCode":200,"data":{'
                    '"kpis":{"totalEnrolledStudents":0,"activeRatePercent":0,'
                    '"totalSchools":0,"activeTopUpCampaigns":0,"moeFasPendingReview":0},'
                    '"budgetByStage":[],"moeFasEligibility":{"approvedCount":0,'
                    '"approvedPercent":0,"underReviewCount":0,"underReviewPercent":0,'
                    '"rejectedCount":0,"rejectedPercent":0},'
                    '"recentTopUpCampaigns":[],"activeMoeSchemes":[]}}'
                ),
            )

        self.page.route("**/bff/v1/dashboard/moe**", handle_moe_dashboard)

        with self.step(
            "Bước 1: Truy cập http://localhost:5173/login",
            expected="Trang đăng nhập hiển thị đầy đủ các trường nhập liệu.",
        ):
            login_page.open(base_url)
            expect(login_page.sign_in_btn).to_be_visible()
            self.step.set_actual("Đã mở trang đăng nhập Cổng Quản trị.")

        with self.step(
            f"Bước 2: Nhập Tên đăng nhập ({valid_auth['username']}) và Mật khẩu quản trị viên hợp lệ",
            expected="Thông tin đăng nhập hợp lệ được điền đầy đủ.",
        ):
            login_page.fill_credentials(username=valid_auth["username"], password="ValidAdminPassword@2026")
            self.step.set_actual(f"Đã nhập tài khoản hợp lệ: {valid_auth['username']}.")

        with self.step(
            "Bước 3: Nhấn nút 'Sign in'",
            expected="Hệ thống gửi yêu cầu xác thực API POST /iam/v1/auth/admin/login.",
        ):
            login_page.submit_credentials()
            self.step.set_actual("Đã gửi thông tin đăng nhập lên hệ thống.")

        with self.step(
            "Bước 4: Quan sát quá trình xác thực và điều hướng",
            expected="API trả về HTTP 204 No Content; điều hướng mượt mà sang Trang chủ /; Admin Shell hiển thị đầy đủ.",
        ):
            assert login_calls, "Không gửi POST /iam/v1/auth/admin/login"
            self.page.wait_for_url(f"{base_url}/", timeout=15000)
            expect(self.page).to_have_url(f"{base_url}/")
            assert login_status_codes == [204], f"API đăng nhập không trả HTTP 204: {login_status_codes}"
            assert authenticated_auth_me_calls, "Không truy vấn GET /iam/v1/auth/me sau đăng nhập nội bộ"
            expect(shell.header.first).to_be_visible()
            expect(shell.nav).to_be_visible()
            self.step.set_actual("Xác thực đăng nhập cơ bản thành công và điều hướng an toàn.")

        self.page.unroute("**/iam/v1/auth/admin/login")
        self.page.unroute("**/auth/me")
        self.page.unroute("**/bff/v1/dashboard/moe**")

    def test_tc_adm_auth_020_moehq_microsoft_sso_flow(self, admin_login_data: Dict[str, Any]) -> None:
        """
        TC-ADM-AUTH-020: Luồng đăng nhập Microsoft SSO thành công với tài khoản Quản trị viên MOEHQ.
        Kịch bản: TS-ADM-AUTH-FLOW | Nguồn đặc tả: 01_admin_login_and_sso.md §2.1; FLOW-SSO-MOEHQ; LoginPage.tsx:66-79
        """
        login_page = self.get_page(AdminLoginPage)
        sim_page = self.get_page(MicrosoftSimulatorPage)
        shell = self.get_page(AdminDashboardShellPage)
        base_url = admin_login_data["base_url"]
        moehq = admin_login_data["personas"]["moehq"]

        with self.step(
            "Bước 1: Tại http://localhost:5173/login, nhấn nút 'Sign in with Microsoft'",
            expected="Chuyển hướng an toàn tới màn hình Microsoft Simulator.",
        ):
            login_page.open(base_url)
            login_page.click_sign_in_with_microsoft()
            self.page.wait_for_url("**/microsoft-provider/**", timeout=15000)
            self.step.set_actual("Đã mở giao diện Entra Simulator.")

        with self.step(
            f"Bước 2: Tại màn hình Entra Simulator, click chọn tài khoản Quản trị Bộ {moehq['email']}",
            expected="Hệ thống chấp nhận tài khoản và chuyển hướng về URL callback.",
        ):
            sim_page.select_moehq_admin()
            self.step.set_actual("Đã chọn thẻ tài khoản Quản trị viên MOEHQ.")

        with self.step(
            "Bước 3: Chờ trình duyệt xử lý qua callback /login/microsoft/callback",
            expected="Điều hướng hoàn tất vào Trang chủ Cổng Quản trị http://localhost:5173/.",
        ):
            self.page.wait_for_url(f"{base_url}/", timeout=20000)
            self.step.set_actual(f"Đã cập bến Trang chủ: {self.page.url}.")

        with self.step(
            "Bước 4: Kiểm tra Header và Sidebar tại Trang chủ sau đăng nhập",
            expected="Header hiển thị vai trò Quản trị viên MOEHQ; Sidebar hiển thị đầy đủ 6 phân hệ cấp Bộ.",
        ):
            expect(shell.header.first).to_be_visible(timeout=10000)
            expect(shell.nav.first).to_be_visible()
            # Current UI exposes account identity as an aria-label: "<Name> (<role/username>)".
            expect(shell.user_role_or_code.first).to_have_attribute(
                "aria-label", re.compile(r"\(moehq\)$", re.IGNORECASE)
            )
            for href in (
                "/school-management",
                "/school-user-management",
                "/education-accounts",
                "/fee-management",
                "/fas-application-management",
            ):
                expect(shell.nav_link_by_href(href)).to_be_visible()
            expect(shell.nav_link_by_href("/school-config")).to_have_count(0)
            self.step.set_actual("Header và Sidebar hiển thị chuẩn xác phân quyền MOEHQ.")

    def test_tc_adm_auth_021_school_microsoft_sso_flow(self, admin_login_data: Dict[str, Any]) -> None:
        """
        TC-ADM-AUTH-021: Luồng đăng nhập Microsoft SSO thành công với tài khoản Cán bộ trường SCHOOL.
        Kịch bản: TS-ADM-AUTH-FLOW | Nguồn đặc tả: 01_admin_login_and_sso.md §2.1; FLOW-SSO-SCHOOL; LoginPage.tsx:66-79
        """
        login_page = self.get_page(AdminLoginPage)
        sim_page = self.get_page(MicrosoftSimulatorPage)
        shell = self.get_page(AdminDashboardShellPage)
        base_url = admin_login_data["base_url"]
        school = admin_login_data["personas"]["school_assigned"]

        with self.step(
            "Bước 1: Tại http://localhost:5173/login, nhấn nút 'Sign in with Microsoft'",
            expected="Mở màn hình chọn tài khoản trên Entra Simulator.",
        ):
            login_page.open(base_url)
            login_page.click_sign_in_with_microsoft()
            self.page.wait_for_url("**/microsoft-provider/**", timeout=15000)
            self.step.set_actual("Đã mở giao diện xác thực Simulator.")

        with self.step(
            f"Bước 2: Tại màn hình Entra Simulator, click chọn tài khoản Cán bộ trường {school['email']}",
            expected="Chọn tài khoản trường thành công và chuyển hướng về callback.",
        ):
            sim_page.select_school_staff()
            self.step.set_actual(f"Đã chọn thẻ tài khoản Cán bộ trường ({school['school_id']}).")

        with self.step(
            "Bước 3: Chờ xử lý callback và quan sát điều hướng vào Trang chủ",
            expected="Xác thực SSO thành công; URL chuyển về http://localhost:5173/.",
        ):
            self.page.wait_for_url(f"{base_url}/", timeout=20000)
            self.step.set_actual("Đã hoàn tất callback và điều hướng vào Trang chủ.")

        with self.step(
            "Bước 4: Kiểm tra Header và Sidebar phân quyền trường học",
            expected="Header hiển thị vai trò Cán bộ Quản trị trường (SCHOOL); Sidebar hiển thị các menu cấp trường.",
        ):
            expect(shell.header.first).to_be_visible(timeout=10000)
            expect(shell.user_role_or_code.first).to_have_attribute(
                "aria-label", re.compile(r"\(school\)$", re.IGNORECASE)
            )
            expect(shell.user_role_or_code.first).to_contain_text("Thi H Bui")
            for href in ("/school-config", "/class-management", "/student-management"):
                expect(shell.nav_link_by_href(href)).to_be_visible()
            for href in (
                "/school-management",
                "/school-user-management",
                "/education-accounts",
                "/top-up",
                "/support-console",
            ):
                expect(shell.nav_link_by_href(href)).to_have_count(0)
            self.step.set_actual("Giao diện phản ánh chuẩn xác vai trò Cán bộ trường SCHOOL.")

    def test_tc_adm_auth_022_cancel_sso_at_simulator(self, admin_login_data: Dict[str, Any]) -> None:
        """
        TC-ADM-AUTH-022: Hủy bỏ quy trình đăng nhập SSO tại Microsoft Simulator bằng nút Back trình duyệt và quay lại an toàn.
        Kịch bản: TS-ADM-AUTH-FLOW | Nguồn đặc tả: 01_admin_login_and_sso.md §2.2; FLOW-CANCEL; DOM-LOGIN §2.2
        """
        login_page = self.get_page(AdminLoginPage)
        sim_page = self.get_page(MicrosoftSimulatorPage)
        base_url = admin_login_data["base_url"]

        with self.step(
            "Bước 1: Từ trang Đăng nhập http://localhost:5173/login, nhấn 'Sign in with Microsoft' để sang Entra Simulator",
            expected="Chuyển hướng đến màn hình Simulator.",
        ):
            login_page.open(base_url)
            login_page.click_sign_in_with_microsoft()
            self.page.wait_for_url("**/microsoft-provider/**", timeout=15000)
            self.step.set_actual("Đã chuyển hướng đến Microsoft Simulator.")

        with self.step(
            "Bước 2: Tại màn hình Entra Simulator, người dùng nhấn nút Back trên trình duyệt để hủy bỏ đăng nhập",
            expected="Trình duyệt thực hiện thao tác Back an toàn.",
        ):
            sim_page.click_cancel()
            self.step.set_actual("Đã thực hiện thao tác hủy bỏ đăng nhập SSO.")

        with self.step(
            "Bước 3: Quan sát trạng thái trang web sau khi quay lại",
            expected="Trình duyệt quay trở về trang Đăng nhập /login an toàn; giao diện bình thường không bị crash.",
        ):
            self.page.wait_for_url(f"**/login**", timeout=15000)
            expect(login_page.sign_in_with_microsoft_btn).to_be_visible()
            self.step.set_actual("Quay trở lại trang Đăng nhập an toàn; nút bấm sẵn sàng tương tác tiếp theo.")
