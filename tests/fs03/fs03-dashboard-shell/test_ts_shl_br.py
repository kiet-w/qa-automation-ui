"""
tests/fs03/fs03-dashboard-shell/test_ts_shl_br.py - Business Rules & RBAC Navigation Matrix.
Pillar: BR (Business Rules & Phân quyền)
Test Cases: TC-SHL-001, TC-SHL-002, TC-SHL-003, TC-SHL-004.
Scenario ID: TS-SHL-BR
Traceability: BR-SHELL-RBAC (MOEHQ, SCHOOL); BR-ROUTE-GUARD; FLOW-SHELL-GUARD;
              02_admin_dashboard_shell.md §1.2, §1.4, §2.1; recon_02_admin_dashboard_shell.md §3, §8, §10
Complies with Invariants 1, 2, 3, 4, 7, 8, 9 (<250 lines), 13 (100% Tiếng Việt step evidence).
"""
import re
from typing import Any, Dict
import pytest
from playwright.sync_api import expect

from tests.base_test import BaseTest
from pages.fs03.admin_dashboard_shell_page import AdminDashboardShellPage


@pytest.mark.br
@pytest.mark.rbac
class TestAdminShellBusinessRules(BaseTest):
    """Business Rules & Phân quyền kiểm thử Cổng Quản trị viên EduFAMS."""

    def test_tc_ts_shl_br_001_moehq_menu_rbac(
        self, shell_data: Dict[str, Any], auth_mock
    ) -> None:
        """
        TC-SHL-001: Phân quyền Menu Thanh menu bên trái cho Quản trị viên Bộ GD: Hiển thị toàn bộ các phân hệ cấp Bộ.
        Scenario ID: TS-SHL-BR | Traceability: BR-SHELL-RBAC; MOEHQ
        """
        auth_mock("moehq")
        shell = self.get_page(AdminDashboardShellPage)
        base_url = shell_data["environments"]["base_url"]
        expected_links = shell_data["navigation"]["moehq_expected_links"]
        forbidden_hrefs = shell_data["navigation"]["moehq_forbidden_hrefs"]

        with self.step(
            "Step 1: Đăng nhập với tài khoản Quản trị viên Bộ GD",
            expected="Đăng nhập thành công và truy cập màn hình Dashboard.",
        ):
            shell.open(base_url=base_url, path="/")
            expect(shell.header).to_be_visible()
            expect(shell.brand_link).to_be_visible()
            self.step.set_actual(f"Màn hình Dashboard tải thành công tại {self.page.url}.")

        with self.step(
            "Step 2: Quan sát thanh menu điều hướng bên trái (Thanh menu bên trái)",
            expected="Hiển thị đầy đủ các phân hệ cấp Bộ và ẩn các menu chỉ dành cho School.",
        ):
            expect(shell.nav).to_be_visible()

            for item in expected_links:
                nav_item = shell.nav_link_by_href(item["href"])
                expect(nav_item).to_be_visible()

            for f_href in forbidden_hrefs:
                forbidden_item = shell.nav_link_by_href(f_href)
                expect(forbidden_item).to_have_count(0)

            self.highlight_actual_result(
                locator=shell.nav,
                text="MOEHQ navigation menu hiển thị đầy đủ các phân hệ cấp Bộ và ẩn menu trường học",
            )
            self.step.set_actual(f"Thanh menu MOEHQ hiển thị đúng {len(expected_links)} mục phân hệ cấp Bộ.")

    def test_tc_ts_shl_br_002_school_menu_rbac(
        self, shell_data: Dict[str, Any], auth_mock
    ) -> None:
        """
        TC-SHL-002: Phân quyền Menu Thanh menu bên trái cho Cán bộ trường SCHOOL: Ẩn các menu cấp Bộ, chỉ hiển thị menu trường.
        Scenario ID: TS-SHL-BR | Traceability: BR-SHELL-RBAC; SCHOOL
        """
        auth_mock("school")
        shell = self.get_page(AdminDashboardShellPage)
        base_url = shell_data["environments"]["base_url"]
        expected_links = shell_data["navigation"]["school_expected_links"]
        forbidden_hrefs = shell_data["navigation"]["school_forbidden_hrefs"]

        with self.step(
            "Step 1: Đăng nhập với tài khoản Cán bộ trường",
            expected="Đăng nhập thành công với vai trò Cán bộ Quản trị trường.",
        ):
            shell.open(base_url=base_url, path="/")
            expect(shell.header).to_be_visible()
            self.step.set_actual(f"Đăng nhập thành công vai trò Cán bộ trường tại {self.page.url}.")

        with self.step(
            "Step 2: Quan sát thanh menu điều hướng bên trái",
            expected="Chỉ hiển thị các phân hệ quản lý trường; các menu quản lý cấp Bộ hoàn toàn bị ẩn.",
        ):
            expect(shell.nav).to_be_visible()

            for item in expected_links:
                nav_item = shell.nav_link_by_href(item["href"])
                expect(nav_item).to_be_visible()

            for f_href in forbidden_hrefs:
                forbidden_item = shell.nav_link_by_href(f_href)
                expect(forbidden_item).to_have_count(0)

            self.highlight_actual_result(
                locator=shell.nav,
                text="SCHOOL navigation menu chỉ hiển thị menu cấp trường, ẩn toàn bộ menu cấp Bộ",
            )
            self.step.set_actual(f"Thanh menu SCHOOL hiển thị đúng {len(expected_links)} mục trường học.")

    def test_tc_ts_shl_br_003_school_url_access_denial(
        self, shell_data: Dict[str, Any], auth_mock
    ) -> None:
        """
        TC-SHL-003: Chặn truy cập URL quản trị cấp Bộ đối với vai trò Cán bộ trường (Access Control Guard).
        Scenario ID: TS-SHL-BR | Traceability: BR-ROUTE-GUARD; RBAC-SCHOOL
        """
        auth_mock("school")
        shell = self.get_page(AdminDashboardShellPage)
        base_url = shell_data["environments"]["base_url"]
        target_url = shell_data["rbac_denial"]["target_url"]

        with self.step(
            "Step 1: Cán bộ trường nhập trực tiếp URL quản trị cấp Bộ vào thanh địa chỉ",
            expected="Hệ thống tiếp nhận yêu cầu và áp dụng bộ lọc phân quyền tuyến đường (Route Guard).",
        ):
            shell.open(base_url=base_url, path=target_url)
            self.step.set_actual(f"Đã mở trực tiếp URL cấp Bộ: {target_url}.")

        with self.step(
            "Step 2: Quan sát phản ứng điều hướng và thông báo bảo vệ của hệ thống",
            expected="Hệ thống chặn truy cập; chuyển hướng về trang chủ hoặc hiển thị cảnh báo không có quyền.",
        ):
            expect(self.page).not_to_have_url(re.compile(rf".*{re.escape(target_url)}$"))
            expect(shell.nav_link_by_href(target_url)).to_have_count(0)

            self.highlight_actual_result(
                locator=shell.main_content,
                text="Truy cập URL cấp Bộ bị chặn an toàn đối với vai trò Cán bộ trường",
            )
            self.step.set_actual("Truy cập bị từ chối; hệ thống chuyển hướng an toàn và bảo vệ dữ liệu cấp Bộ.")

    def test_tc_ts_shl_br_004_unauthenticated_access_denial(
        self, shell_data: Dict[str, Any]
    ) -> None:
        """
        TC-SHL-004: Chặn người dùng chưa đăng nhập truy cập trực tiếp các đường dẫn quản trị nội bộ.
        Scenario ID: TS-SHL-BR | Traceability: FLOW-SHELL-GUARD; AUTH-PROTECT
        """
        base_url = shell_data["environments"]["base_url"]
        protected_path = shell_data["rbac_denial"]["target_url"]
        shell = self.get_page(AdminDashboardShellPage)

        def handle_unauthenticated(route):
            route.fulfill(
                status=401,
                content_type="application/json",
                body='{"error": "Unauthorized", "message": "Authentication required"}',
            )

        self.page.route(shell_data["environments"]["auth_me_api"], handle_unauthenticated)

        try:
            with self.step(
                "Step 1: Mở trình duyệt chưa đăng nhập và nhập trực tiếp đường dẫn quản trị nội bộ",
                expected="Hệ thống phát hiện phiên chưa xác thực và kích hoạt bộ lọc bảo vệ.",
            ):
                shell.open(base_url=base_url, path=protected_path)
                self.step.set_actual(f"Đã cố truy cập đường dẫn nội bộ: {protected_path}.")

            with self.step(
                "Step 2: Quan sát phản ứng chuyển hướng an toàn",
                expected="Hệ thống lập tức chuyển hướng về trang Đăng nhập /login; không hiển thị khung quản trị.",
            ):
                self.page.wait_for_url("**/login*", timeout=10000)
                expect(self.page).to_have_url(re.compile(r".*/login.*"))
                expect(shell.nav).to_have_count(0)
                expect(shell.sidebar_container).to_have_count(0)

                self.highlight_actual_result(
                    locator=shell.page_body,
                    text="Chưa đăng nhập bị chặn và tự động chuyển hướng về /login",
                )
                self.step.set_actual(f"Chuyển hướng thành công về {self.page.url}; khung quản trị được bảo vệ tuyệt đối.")
        finally:
            self.page.unroute(shell_data["environments"]["auth_me_api"])
