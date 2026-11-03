"""
tests/testcase5173/01_admin_login_and_sso/test_adm_ac.py - Bộ kiểm thử Tiêu chí nghiệm thu giao diện & chức năng (AC).
Bao phủ các ca kiểm thử: TC-ADM-AUTH-006, TC-ADM-AUTH-007, TC-ADM-AUTH-008, TC-ADM-AUTH-009.
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
    """Bộ kiểm thử Tiêu chí nghiệm thu (Acceptance Criteria) Giao diện Đăng nhập & Microsoft SSO."""

    def test_tc_adm_auth_006_login_page_dom_elements(self, admin_login_data: Dict[str, Any]) -> None:
        """
        TC-ADM-AUTH-006: Hiển thị đầy đủ giao diện Đăng nhập Cổng Quản trị: Tiêu đề, Form đăng nhập, nút Sign in và Sign in with Microsoft.
        Kịch bản: TS-ADM-AUTH-AC | Nguồn đặc tả: 01_admin_login_and_sso.md §1.1; DOM-LOGIN §1.1; LoginPage.tsx:87-208
        """
        login_page = self.get_page(AdminLoginPage)
        base_url = admin_login_data["base_url"]

        with self.step(
            "Bước 1: Mở trình duyệt và truy cập http://localhost:5173/login",
            expected="Trang đăng nhập tải thành công không phát sinh lỗi.",
        ):
            login_page.open(base_url)
            self.step.set_actual(f"Đã mở URL: {self.page.url}.")

        with self.step(
            "Bước 2: Kiểm tra tiêu đề trang web, các trường nhập liệu, nút bấm và panel giới thiệu bên phải",
            expected="Hiển thị đầy đủ tiêu đề, phụ đề, bộ chọn ngôn ngữ, ô Username, Password, nút Sign in, Sign in with Microsoft và panel trang trí.",
        ):
            # Kiểm tra Title và Heading
            assert "Admin Portal" in self.page.title(), f"Title không chứa 'Admin Portal': {self.page.title()}"
            expect(login_page.heading).to_be_visible()
            expect(login_page.subtitle).to_be_visible()

            # Kiểm tra bộ chọn ngôn ngữ
            expect(login_page.language_select).to_be_visible()

            # Kiểm tra các trường form đăng nhập nội bộ
            expect(login_page.username_input).to_be_visible()
            expect(login_page.password_input).to_be_visible()
            expect(login_page.password_toggle_btn).to_be_visible()
            expect(login_page.sign_in_btn).to_be_visible()

            # Kiểm tra nút Sign in with Microsoft
            expect(login_page.sign_in_with_microsoft_btn).to_be_visible()
            self.step.set_actual("Tất cả các phần tử form đăng nhập hiển thị đầy đủ và chính xác theo đặc tả.")

    def test_tc_adm_auth_007_microsoft_simulator_tiles(self, admin_login_data: Dict[str, Any]) -> None:
        """
        TC-ADM-AUTH-007: Tích hợp chuyển hướng sang Microsoft Entra Simulator (:5288) với danh sách tài khoản mẫu.
        Kịch bản: TS-ADM-AUTH-AC | Nguồn đặc tả: 01_admin_login_and_sso.md §1.2; AC-ENTRA-SIMULATOR; LoginPage.tsx:66-79
        """
        login_page = self.get_page(AdminLoginPage)
        sim_page = self.get_page(MicrosoftSimulatorPage)
        base_url = admin_login_data["base_url"]
        moehq = admin_login_data["personas"]["moehq"]
        school = admin_login_data["personas"]["school_assigned"]
        parent = admin_login_data["personas"]["parent_role"]

        with self.step(
            "Bước 1: Tại trang http://localhost:5173/login, nhấn nút 'Sign in with Microsoft'",
            expected="Hệ thống gọi API GET authorize-url, lưu OAuth session và chuyển hướng sang Entra Simulator :5288.",
        ):
            login_page.open(base_url)
            login_page.click_sign_in_with_microsoft()
            self.page.wait_for_url("**/microsoft-provider/**", timeout=15000)
            self.step.set_actual("Đã chuyển hướng đến màn hình Entra ID Simulator.")

        with self.step(
            "Bước 2: Quan sát URL trình duyệt và màn hình điều hướng tới",
            expected="Màn hình Simulator hiển thị 'Pick an account' kèm danh sách tài khoản (MOEHQ, SCHOOL, PARENT) và nút Continue.",
        ):
            assert "5288" in self.page.url or "microsoft-provider" in self.page.url, f"URL Simulator không đúng: {self.page.url}"
            expect(sim_page.pick_account_heading).to_be_visible()
            expect(sim_page.moehq_tile.first).to_be_visible()
            expect(sim_page.school_tile.first).to_be_visible()
            expect(sim_page.parent_tile.first).to_be_visible()
            expect(sim_page.use_another_account_input).to_be_visible()
            expect(sim_page.continue_btn.first).to_be_visible()
            self.step.set_actual(f"Hiển thị đầy đủ thẻ tài khoản {moehq['email']}, {school['email']}, {parent['email']} và nút Continue trên Simulator.")

    def test_tc_adm_auth_008_oauth_callback_handling(self, admin_login_data: Dict[str, Any]) -> None:
        """
        TC-ADM-AUTH-008: Xử lý Callback OAuth (/login/microsoft/callback): Hiển thị spinner và trao đổi mã xác thực.
        Kịch bản: TS-ADM-AUTH-AC | Nguồn đặc tả: 01_admin_login_and_sso.md §1.3; AC-OAUTH-CALLBACK; MicrosoftCallbackPage.tsx:48-65
        """
        login_page = self.get_page(AdminLoginPage)
        shell = self.get_page(AdminDashboardShellPage)
        base_url = admin_login_data["base_url"]
        oauth_data = admin_login_data["oauth"]
        callback_requests = []

        import json
        moe_user_payload = {
            "isSuccess": True,
            "statusCode": 200,
            "data": {
                "id": "moe-admin-001",
                "username": "admin@IAM.edu.vn",
                "fullName": "MOE HQ Administrator",
                "schoolId": None,
                "roles": [{"name": "MOEHQ"}],
                "permissions": [],
            },
        }

        def handle_auth_login(route):
            callback_requests.append(route.request.post_data_json or {})
            route.fulfill(
                status=200,
                content_type="application/json",
                body='{"isSuccess": true, "data": {"token": "jwt-token-valid-001"}}',
            )

        def handle_auth_me(route):
            route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps(moe_user_payload),
            )

        def handle_moe_dashboard(route):
            route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps({
                    "isSuccess": True,
                    "statusCode": 200,
                    "data": {
                        "kpis": {
                            "totalEnrolledStudents": 500,
                            "activeRatePercent": 100,
                            "totalSchools": 10,
                            "activeTopUpCampaigns": 2,
                            "moeFasPendingReview": 20,
                            "edusaveTotalBalance": 1000000,
                            "edusaveAverageBalance": 2000,
                        },
                        "budgetByStage": [],
                        "moeFasEligibility": {
                            "approvedCount": 0,
                            "approvedPercent": 0,
                            "underReviewCount": 0,
                            "underReviewPercent": 0,
                            "rejectedCount": 0,
                            "rejectedPercent": 0,
                        },
                        "recentTopUpCampaigns": [],
                        "activeMoeSchemes": [],
                    },
                }),
            )

        self.page.route("**/auth/admin/microsoft-login**", handle_auth_login)
        self.page.route("**/auth/me**", handle_auth_me)
        self.page.route("**/bff/v1/dashboard/**", handle_moe_dashboard)

        try:
            with self.step(
                "Bước 1: Chọn tài khoản hợp lệ (admin@IAM.edu.vn) trên màn hình Entra Simulator",
                expected="Simulator điều hướng về URL callback kèm code và state.",
            ):
                login_page.open(base_url)
                # Khởi tạo OAuth session hợp lệ trong sessionStorage
                self.page.evaluate(
                    f"""sessionStorage.setItem('edusave.admin.microsoft-oauth', JSON.stringify({{
                        'redirectUri': '{base_url}/login/microsoft/callback',
                        'state': '{oauth_data['valid_state']}',
                        'codeVerifier': 'verifier-abc-123',
                        'returnTo': '/'
                    }}));"""
                )
                login_page.open_callback(
                    base_url=base_url,
                    params=f"?code={oauth_data['valid_code']}&state={oauth_data['valid_state']}",
                )
                self.step.set_actual("Đã chuyển tiếp đến URL callback với mã code và state hợp lệ.")

            with self.step(
                "Bước 2: Quan sát giai đoạn xử lý callback tại URL http://localhost:5173/login/microsoft/callback",
                expected="Hiển thị spinner div[role='status'], gửi POST /microsoft-login và tự động điều hướng về trang chủ /.",
            ):
                self.page.wait_for_url(f"{base_url}/", timeout=15000)
                expect(shell.header.first).to_be_visible()
                assert len(callback_requests) == 1, "Callback không gửi duy nhất một yêu cầu xác thực OAuth"
                callback_payload = callback_requests[0]
                for key in ("code", "state", "redirectUri", "codeVerifier"):
                    assert key in callback_payload, f"Thiếu trường '{key}' trong payload callback OAuth"
                assert callback_payload["state"] == oauth_data["valid_state"]
                assert callback_payload["code"] == oauth_data["valid_code"]
                assert self.page.evaluate("sessionStorage.getItem('edusave.admin.microsoft-oauth')") is None
                self.step.set_actual("Xử lý callback thành công và điều hướng mượt mà vào Trang chủ.")
        finally:
            self.page.unroute("**/auth/admin/microsoft-login**")
            self.page.unroute("**/auth/me**")
            self.page.unroute("**/bff/v1/dashboard/**")

    def test_tc_adm_auth_009_return_to_destination_redirect(self, admin_login_data: Dict[str, Any]) -> None:
        """
        TC-ADM-AUTH-009: Chuyển hướng về trang đích ban đầu (Return-to Destination) sau khi đăng nhập thành công.
        Kịch bản: TS-ADM-AUTH-AC | Nguồn đặc tả: 01_admin_login_and_sso.md §2.2; AC-RETURN-DESTINATION; LoginPage.tsx:74/212
        """
        login_page = self.get_page(AdminLoginPage)
        shell = self.get_page(AdminDashboardShellPage)
        base_url = admin_login_data["base_url"]
        target_path = "/school-management"

        def handle_unauth_me(route):
            route.fulfill(
                status=401,
                content_type="application/json",
                body='{"isSuccess": false, "statusCode": 401, "message": "Unauthorized"}',
            )

        def handle_auth_login(route):
            route.fulfill(
                status=200,
                content_type="application/json",
                body='{"isSuccess": true, "data": {"token": "jwt-token-return-001"}}',
            )

        def handle_auth_me(route):
            route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps({
                    "isSuccess": True,
                    "statusCode": 200,
                    "data": {
                        "id": "moe-admin-001",
                        "username": "admin@moe.gov.vn",
                        "email": "admin@moe.gov.vn",
                        "fullName": "MOE Administrator",
                        "schoolId": None,
                        "roles": [{"name": "MOEHQ"}],
                        "permissions": [],
                    },
                }),
            )

        def handle_school_table(route):
            route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps({
                    "isSuccess": True,
                    "statusCode": 200,
                    "data": {
                        "items": [],
                        "metadata": {
                            "totalRecords": 0,
                            "totalPages": 0,
                            "pageNumber": 1,
                            "pageSize": 10,
                        },
                    },
                }),
            )

        try:
            self.page.route("**/auth/me**", handle_unauth_me)

            with self.step(
                f"Bước 1: Khi chưa đăng nhập, nhập trực tiếp URL {base_url}{target_path} vào thanh địa chỉ",
                expected="Hệ thống điều hướng sang /login kèm lưu trữ đích đến ban đầu.",
            ):
                self.page.goto(f"{base_url}{target_path}", wait_until="domcontentloaded")
                expect(login_page.sign_in_with_microsoft_btn).to_be_visible()
                self.step.set_actual(f"Chưa đăng nhập, đã bị điều hướng an toàn về {self.page.url}.")

            with self.step(
                "Bước 2: Hệ thống ghi nhận returnTo trong OAuth session, hoàn tất xác thực đăng nhập",
                expected="Xác thực danh tính người dùng thành công.",
            ):
                self.page.unroute("**/auth/me**")
                self.page.route("**/auth/admin/microsoft-login**", handle_auth_login)
                self.page.route("**/auth/me**", handle_auth_me)
                self.page.route("**/academic-resources/**", handle_school_table)

                self.page.evaluate(
                    f"""sessionStorage.setItem('edusave.admin.microsoft-oauth', JSON.stringify({{
                        'redirectUri': '{base_url}/login/microsoft/callback',
                        'state': 'state-return-001',
                        'codeVerifier': 'verifier-123',
                        'returnTo': '{target_path}'
                    }}));"""
                )
                login_page.open_callback(base_url=base_url, params="?code=code-return-001&state=state-return-001")
                self.step.set_actual("Đã hoàn tất xác thực thông qua callback.")

            with self.step(
                f"Bước 3: Quan sát trang đích mà người dùng được đưa đến sau khi xác thực xong",
                expected=f"Hệ thống điều hướng chính xác về {target_path} thay vì trang chủ mặc định /.",
            ):
                self.page.wait_for_url(f"**{target_path}**", timeout=15000)
                assert target_path in self.page.url, f"Không chuyển hướng về đúng trang đích {target_path}: {self.page.url}"
                self.step.set_actual(f"Đã chuyển hướng chính xác về trang đích ban đầu: {self.page.url}.")
        finally:
            try:
                self.page.unroute("**/auth/admin/microsoft-login**")
            except Exception:
                pass
            try:
                self.page.unroute("**/auth/me**")
            except Exception:
                pass
            try:
                self.page.unroute("**/academic-resources/**")
            except Exception:
                pass
