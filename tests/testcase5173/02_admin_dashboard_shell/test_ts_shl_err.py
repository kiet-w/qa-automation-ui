"""
tests/testcase5173/02_admin_dashboard_shell/test_ts_shl_err.py - Error Handling & Network/Auth Resilience.
Pillar: Error (Xử lý ngoại lệ & Phục hồi lỗi)
Test Cases: TC-SHL-014, TC-SHL-015, TC-SHL-016.
Scenario ID: TS-SHL-ERR
Traceability: ERR-SHELL-404; ERR-SHELL-OFFLINE; ERR-AUTH-ME-500; RESILIENCE;
              02_admin_dashboard_shell.md §1.4, §4.2; recon_02_admin_dashboard_shell.md §8
Complies with Invariants 1, 2, 3, 4, 7, 8, 9 (<250 lines), 13 (100% Tiếng Việt step evidence).
"""
import re
from typing import Any, Dict
import pytest
from playwright.sync_api import expect

from tests.base_test import BaseTest
from pages.fs03.admin_dashboard_shell_page import AdminDashboardShellPage


@pytest.mark.error
@pytest.mark.resilience
class TestAdminShellErrorHandling(BaseTest):
    """Error handling and network/auth resilience test suite for EduFAMS Admin Dashboard Shell."""

    def test_tc_ts_shl_err_014_not_found_404_routing(
        self, shell_data: Dict[str, Any], auth_mock
    ) -> None:
        """
        TC-SHL-014: Hiển thị thông báo trang không tìm thấy khi truy cập đường dẫn sai kèm nút về Trang chủ.
        Scenario ID: TS-SHL-ERR | Traceability: ERR-SHELL-404; NOT-FOUND
        """
        auth_mock("moehq")
        shell = self.get_page(AdminDashboardShellPage)
        base_url = shell_data["environments"]["base_url"]
        err_data = shell_data["error_routes"]

        with self.step(
            "Step 1: Nhập đường dẫn không tồn tại vào thanh URL",
            expected="Giao diện hiển thị thông báo không tìm thấy trang yêu cầu kèm nút Quay về Trang chủ.",
        ):
            shell.open(base_url=base_url, path=err_data["not_found_path"])
            expect(shell.not_found_container).to_be_visible()
            expect(shell.page_heading).to_have_text("404 - Page Not Found")
            expect(self.page.get_by_text(err_data["expected_404_text"], exact=True)).to_be_visible()
            expect(shell.back_to_home_link).to_be_visible()
            self.step.set_actual(f"Màn hình 404 hiển thị thành công tại {self.page.url}.")

        with self.step(
            "Step 2: Nhấn nút Quay về Trang chủ (Back to Home)",
            expected="Hệ thống điều hướng an toàn về màn hình Trang chủ Dashboard (/).",
        ):
            shell.click_back_to_home()
            expect(self.page).to_have_url(f"{base_url}/")
            expect(shell.nav).to_be_visible()

            self.highlight_actual_result(
                locator=shell.main_content,
                text="Xử lý 404 trang không tồn tại an toàn, quay về Dashboard thành công",
            )
            self.step.set_actual(f"Đã quay về Trang chủ thành công tại {self.page.url}.")

    def test_tc_ts_shl_err_015_offline_navigation_recovery(
        self, shell_data: Dict[str, Any], auth_mock
    ) -> None:
        """
        TC-SHL-015: Khôi phục Dashboard sau khi thao tác điều hướng bị mất mạng.
        Scenario ID: TS-SHL-ERR | Traceability: ERR-SHELL-OFFLINE; RESILIENCE
        """
        auth_mock("moehq")
        shell = self.get_page(AdminDashboardShellPage)
        base_url = shell_data["environments"]["base_url"]
        target_href = shell_data["offline_recovery"]["navigation_href"]

        shell.open(base_url=base_url, path="/")
        expect(shell.header.first).to_be_visible()

        try:
            with self.step(
                "Step 1: Ngắt mạng và chọn mục điều hướng từ shell đã tải",
                expected="URL chuyển sang route được chọn trong khi trình duyệt offline.",
            ):
                self.page.context.set_offline(True)
                shell.click_nav_link_by_href(target_href)
                expect(self.page).to_have_url(f"{base_url}{target_href}")
                self.step.set_actual(f"URL đã chuyển sang {target_href} khi offline.")

            with self.step(
                "Step 2: Bật lại mạng và tải lại Dashboard",
                expected="Trang chủ tải lại được; header, sidebar và nội dung Dashboard hiển thị.",
            ):
                self.page.context.set_offline(False)
                shell.open(base_url=base_url, path="/")
                expect(self.page).to_have_url(f"{base_url}/")
                expect(shell.header.first).to_be_visible()
                expect(shell.nav).to_be_visible()
                expect(shell.main_content).to_be_visible()

                self.highlight_actual_result(
                    locator=shell.header,
                    text="Kết nối lại mạng và trở về Dashboard thành công",
                )
                self.step.set_actual("Đã quay về Dashboard khi kết nối mạng được khôi phục.")
        finally:
            self.page.context.set_offline(False)

    def test_tc_ts_shl_err_016_auth_server_failure_500(
        self, shell_data: Dict[str, Any]
    ) -> None:
        """
        TC-SHL-016: Xử lý khi máy chủ xác thực gặp sự cố gián đoạn: Hiển thị thông báo lỗi hệ thống và đưa về trang đăng nhập.
        Scenario ID: TS-SHL-ERR | Traceability: ERR-AUTH-ME-500; RESILIENCE
        """
        base_url = shell_data["environments"]["base_url"]
        shell = self.get_page(AdminDashboardShellPage)

        def handle_auth_500(route):
            route.fulfill(
                status=500,
                content_type="application/json",
                body='{"isSuccess": false, "statusCode": 500, "message": "Auth service unavailable"}',
            )

        self.page.route(shell_data["environments"]["auth_me_api"], handle_auth_500)

        try:
            with self.step(
                "Step 1: Giả lập tình huống máy chủ xác thực gặp sự cố gián đoạn (500)",
                expected="Hệ thống bắt lỗi từ chối phiên và không làm lộ dữ liệu quản trị.",
            ):
                shell.open(base_url=base_url, path="/")
                self.step.set_actual("Đã mô phỏng sự cố máy chủ xác thực phản hồi 500.")

            with self.step(
                "Step 2: Quan sát phản ứng bảo vệ an toàn của giao diện Shell",
                expected="Hệ thống đưa người dùng về trang Đăng nhập hoặc hiển thị cảnh báo lỗi dịch vụ.",
            ):
                self.page.wait_for_url("**/login*", timeout=10000)
                expect(self.page).to_have_url(re.compile(r".*/login.*"))
                expect(shell.nav).to_have_count(0)
                expect(shell.sidebar_container).to_have_count(0)

                self.highlight_actual_result(
                    locator=shell.page_body,
                    text="Máy chủ xác thực 500 được xử lý an toàn: chuyển hướng về /login",
                )
                self.step.set_actual(f"Hệ thống tự động bảo vệ và chuyển hướng an toàn về {self.page.url}.")
        finally:
            self.page.unroute(shell_data["environments"]["auth_me_api"])
