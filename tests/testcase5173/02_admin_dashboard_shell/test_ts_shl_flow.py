"""
tests/testcase5173/02_admin_dashboard_shell/test_ts_shl_flow.py - Function Flow & Navigation State Machine.
Pillar: Flow (Luồng thao tác chức năng & Chuyển trạng thái)
Test Cases: TC-SHL-012, TC-SHL-013.
Scenario ID: TS-SHL-FLOW
Traceability: FLOW-SHELL-NAV; FLOW-SIGN-OUT;
              02_admin_dashboard_shell.md §1.2, §1.3, §2.2, §4.2; recon_02_admin_dashboard_shell.md §4, §5, §8
Complies with Invariants 1, 2, 3, 4, 7, 8, 9 (<250 lines), 13 (100% Tiếng Việt step evidence).
"""
import re
from typing import Any, Dict
import pytest
from playwright.sync_api import expect

from tests.base_test import BaseTest
from pages.fs03.admin_dashboard_shell_page import AdminDashboardShellPage


@pytest.mark.flow
@pytest.mark.p1
class TestAdminShellFunctionFlow(BaseTest):
    """Function flow and navigation transitions for EduFAMS Admin Dashboard Shell."""

    def test_tc_ts_shl_flow_012_sequential_navigation(
        self, shell_data: Dict[str, Any], auth_mock
    ) -> None:
        """
        TC-SHL-012: Luồng điều hướng tuần tự qua các phân hệ quản lý và cập nhật nội dung tương ứng.
        Scenario ID: TS-SHL-FLOW | Traceability: FLOW-SHELL-NAV; DOM-SHELL §1.2
        """
        auth_mock("moehq")
        shell = self.get_page(AdminDashboardShellPage)
        base_url = shell_data["environments"]["base_url"]
        routes = shell_data["navigation"]["sequential_test_routes"]

        shell.open(base_url=base_url, path="/")
        expect(shell.header.first).to_be_visible()
        expect(shell.nav).to_be_visible()

        with self.step(
            "Step 1: Lần lượt nhấn vào từng mục menu điều hướng trong danh sách phân hệ",
            expected="Chuyển trang mượt mà không tải lại toàn bộ trang (SPA routing); URL cập nhật chính xác.",
        ):
            for route_info in routes:
                shell.click_nav_link_by_href(route_info["href"])
                self.page.wait_for_load_state("domcontentloaded")
                expect(self.page).to_have_url(re.compile(rf".*{re.escape(route_info['href'])}.*"))
                expect(shell.page_heading).to_be_visible()

                active_info = shell.get_active_nav_info()
                assert active_info["aria_current"] == "page", (
                    f"Mục {route_info['href']} thiếu aria-current='page', nhận được: {active_info}"
                )
                self.step.set_actual(f"Điều hướng thành công đến {route_info['href']} với active state = page.")

        with self.step(
            "Step 2: Quan sát sự chuyển đổi trạng thái nổi bật của thanh menu",
            expected="Chỉ duy nhất mục menu hiện tại được đánh dấu active (aria-current='page').",
        ):
            active_count = shell.active_nav_link.count()
            assert active_count == 1, f"Kỳ vọng duy nhất 1 mục active, tìm thấy {active_count}"

            self.highlight_actual_result(
                locator=shell.active_nav_link,
                text="Luồng điều hướng tuần tự giữa các phân hệ chuyển tiếp mượt mà, active state chính xác",
            )
            self.step.set_actual("Trạng thái nổi bật của thanh menu cập nhật chính xác qua các lần chuyển trang.")

    def test_tc_ts_shl_flow_013_sign_out_from_sidebar(
        self, shell_data: Dict[str, Any], auth_mock
    ) -> None:
        """
        TC-SHL-013: Đăng xuất từ nút Sign out cố định trên sidebar.
        Scenario ID: TS-SHL-FLOW | Traceability: FLOW-SIGN-OUT; DOM-SHELL §1.3
        """
        auth_mock("moehq")
        shell = self.get_page(AdminDashboardShellPage)
        base_url = shell_data["environments"]["base_url"]
        def handle_logout(route):
            route.fulfill(status=200, content_type="application/json", body='{"success": true}')

        self.page.route(shell_data["environments"]["logout_api"], handle_logout)

        try:
            with self.step(
                "Step 1: Kiểm tra nút Sign out trên sidebar",
                expected="Thông tin tài khoản hiển thị ở header và nút Sign out hiển thị trực tiếp trên sidebar.",
            ):
                shell.open(base_url=base_url, path="/")
                expect(shell.header.first).to_be_visible()
                expect(shell.nav).to_be_visible()
                expect(shell.user_name.first).to_be_visible()
                expect(shell.sign_out_btn).to_be_visible()
                self.step.set_actual(f"Giao diện sẵn sàng tại {self.page.url}.")

            with self.step(
                "Step 2: Nhấn nút 'Sign out' để kết thúc phiên",
                expected="Kích hoạt API POST /iam/v1/auth/logout và khởi động chuyển hướng an toàn.",
            ):
                shell.sign_out()
                self.step.set_actual("Đã kích hoạt hành động Đăng xuất.")

            with self.step(
                "Step 3: Kiểm tra chuyển hướng an toàn về màn hình Đăng nhập",
                expected="Phiên đăng nhập kết thúc ngay lập tức; điều hướng an toàn về màn hình /login.",
            ):
                self.page.wait_for_url("**/login*", timeout=10000)
                expect(self.page).to_have_url(re.compile(r".*/login.*"))

                self.highlight_actual_result(
                    locator=shell.page_body,
                    text="Thực hiện đăng xuất thành công, chuyển hướng an toàn về /login",
                )
                self.step.set_actual(f"Điều hướng về /login thành công tại {self.page.url}.")
        finally:
            self.page.unroute(shell_data["environments"]["logout_api"])
