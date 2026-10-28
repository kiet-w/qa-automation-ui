"""
tests/fs03/fs03-dashboard-shell/test_ts_shl_err.py - Error Handling & Network/Auth Resilience.
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
            content_text = shell.get_main_content_text()
            assert (
                err_data["expected_404_text"] in content_text
                or "404" in content_text
                or "Not Found" in content_text
            ), f"Kỳ vọng thông báo 404 trong nội dung: '{content_text}'"
            expect(shell.action_by_label(err_data["back_to_home_text"])).to_be_visible()
            self.step.set_actual(f"Màn hình 404 hiển thị thành công tại {self.page.url}.")

        with self.step(
            "Step 2: Nhấn nút Quay về Trang chủ (Back to Home)",
            expected="Hệ thống điều hướng an toàn về màn hình Trang chủ Dashboard (/).",
        ):
            shell.click_action_by_label(err_data["back_to_home_text"])
            self.page.wait_for_load_state("domcontentloaded")
            expect(self.page).to_have_url(re.compile(r".*/?$"))
            expect(shell.nav).to_be_visible()

            self.highlight_actual_result(
                locator=shell.main_content,
                text="Xử lý 404 trang không tồn tại an toàn, quay về Dashboard thành công",
            )
            self.step.set_actual(f"Đã quay về Trang chủ thành công tại {self.page.url}.")

    def test_tc_ts_shl_err_015_network_offline_recovery(
        self, shell_data: Dict[str, Any], auth_mock
    ) -> None:
        """
        TC-SHL-015: Khôi phục và hiển thị thông báo nhắc nhở khi mất kết nối mạng trên giao diện Quản trị.
        Scenario ID: TS-SHL-ERR | Traceability: ERR-SHELL-OFFLINE; RESILIENCE
        """
        auth_mock("moehq")
        shell = self.get_page(AdminDashboardShellPage)
        base_url = shell_data["environments"]["base_url"]

        shell.open(base_url=base_url, path="/")
        expect(shell.header).to_be_visible()

        try:
            with self.step(
                "Step 1: Ngắt kết nối mạng mô phỏng (Offline mode) và thao tác trên giao diện",
                expected="Giao diện không bị crash trắng trang; thanh điều hướng và header vẫn ổn định.",
            ):
                self.page.context.set_offline(True)
                expect(shell.header).to_be_visible()
                expect(shell.nav).to_be_visible()
                self.step.set_actual("Giao diện duy trì cấu trúc khung shell ổn định khi ngắt mạng.")

            with self.step(
                "Step 2: Bật lại kết nối mạng và phục hồi trạng thái hoạt động",
                expected="Khôi phục kết nối thành công; giao diện hoạt động bình thường.",
            ):
                self.page.context.set_offline(False)
                expect(shell.header).to_be_visible()
                expect(shell.nav).to_be_visible()
                expect(shell.main_content).to_be_visible()

                self.highlight_actual_result(
                    locator=shell.header,
                    text="Khôi phục kết nối mạng thành công, giao diện hoạt động bình thường",
                )
                self.step.set_actual("Phục hồi thành công khi mạng kết nối lại bình thường.")
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
