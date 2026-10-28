"""
tests/fs03/fs03-dashboard-shell/test_ts_shl_val.py - Validation & Responsive Layout Tests.
Pillar: Validation (Kiểm tra hợp lệ & BVA)
Test Cases: TC-SHL-009, TC-SHL-010, TC-SHL-011.
Scenario ID: TS-SHL-VAL
Traceability: VAL-SHELL-SIDEBAR; VAL-SHELL-ZOOM; VAL-LOGOUT-NO-CACHE;
              02_admin_dashboard_shell.md §1.2, §1.3, §2.2; recon_02_admin_dashboard_shell.md §1, §7
Complies with Invariants 1, 2, 3, 4, 7, 8, 9 (<250 lines), 13 (100% Tiếng Việt step evidence).
"""
import re
from typing import Any, Dict
import pytest
from playwright.sync_api import expect

from tests.base_test import BaseTest
from pages.fs03.admin_dashboard_shell_page import AdminDashboardShellPage


@pytest.mark.validation
@pytest.mark.ui
class TestAdminShellValidation(BaseTest):
    """Validation and layout resilience tests for EduFAMS Admin Dashboard Shell."""

    def test_tc_ts_shl_val_009_sidebar_toggle_collapse_expand(
        self, shell_data: Dict[str, Any], auth_mock
    ) -> None:
        """
        TC-SHL-009: Thu gọn và mở rộng thanh menu điều hướng Thanh menu bên trái không làm tràn hoặc vỡ bố cục giao diện.
        Scenario ID: TS-SHL-VAL | Traceability: VAL-SHELL-SIDEBAR; RESPONSIVE
        """
        auth_mock("moehq")
        shell = self.get_page(AdminDashboardShellPage)
        base_url = shell_data["environments"]["base_url"]
        dim = shell_data["sidebar_dimensions"]

        shell.open(base_url=base_url, path="/")
        expect(shell.collapse_sidebar_btn).to_be_visible()

        with self.step(
            "Step 1: Quan sát chiều rộng ban đầu của thanh menu bên trái",
            expected="Thanh menu ở trạng thái mở rộng tiêu chuẩn (~256px).",
        ):
            w_initial = shell.get_sidebar_width()
            assert abs(w_initial - dim["expanded_width"]) <= dim["tolerance"], (
                f"Kỳ vọng chiều rộng ban đầu {dim['expanded_width']}±{dim['tolerance']}, thực tế {w_initial}"
            )
            self.step.set_actual(f"Chiều rộng ban đầu của thanh menu: {w_initial}px.")

        with self.step(
            "Step 2: Nhấn nút thu gọn menu Thanh menu bên trái",
            expected="Thanh menu thu gọn mượt mà hiển thị các biểu tượng thu nhỏ (~72px); nội dung mở rộng tự nhiên.",
        ):
            shell.toggle_sidebar()
            w_collapsed = shell.get_sidebar_width()
            assert abs(w_collapsed - dim["collapsed_width"]) <= dim["tolerance"], (
                f"Kỳ vọng chiều rộng sau khi thu gọn {dim['collapsed_width']}±{dim['tolerance']}, thực tế {w_collapsed}"
            )
            self.highlight_actual_result(
                locator=shell.sidebar_container,
                text="Thanh menu thu gọn mượt mà sang dạng biểu tượng thu nhỏ",
            )
            self.step.set_actual(f"Chiều rộng sau khi thu gọn: {w_collapsed}px.")

        with self.step(
            "Step 3: Nhấn lại nút để mở rộng thanh menu trở lại",
            expected="Thanh menu mở rộng trở lại đầy đủ nhãn mục điều hướng (~256px).",
        ):
            shell.toggle_sidebar()
            w_restored = shell.get_sidebar_width()
            assert abs(w_restored - dim["expanded_width"]) <= dim["tolerance"], (
                f"Kỳ vọng chiều rộng phục hồi {dim['expanded_width']}±{dim['tolerance']}, thực tế {w_restored}"
            )
            self.step.set_actual(f"Chiều rộng sau khi mở rộng lại: {w_restored}px.")

    def test_tc_ts_shl_val_010_zoom_responsive_layout(
        self, shell_data: Dict[str, Any], auth_mock
    ) -> None:
        """
        TC-SHL-010: Tự động thích ứng co giãn giao diện quản trị khi thu phóng trình duyệt 125% - 150%.
        Scenario ID: TS-SHL-VAL | Traceability: VAL-SHELL-ZOOM; ACCESSIBILITY
        """
        auth_mock("moehq")
        shell = self.get_page(AdminDashboardShellPage)
        base_url = shell_data["environments"]["base_url"]

        with self.step(
            "Step 1: Tăng mức thu phóng của trình duyệt lên 150%",
            expected="Giao diện tự động co giãn thích ứng theo kích thước viewport mới.",
        ):
            scale = shell_data["zoom"]["scale"]
            desktop = shell_data["viewports"]["desktop"]
            zoomed_width = int(desktop["width"] / scale)
            zoomed_height = int(desktop["height"] / scale)
            self.page.set_viewport_size({"width": zoomed_width, "height": zoomed_height})
            shell.open(base_url=base_url, path="/")
            expect(shell.header).to_be_visible()
            self.step.set_actual(f"Đã thiết lập viewport thu phóng 150%: {zoomed_width}x{zoomed_height}.")

        with self.step(
            "Step 2: Quan sát thanh menu và tiêu đề, kiểm tra tràn bố cục",
            expected="Thanh menu và nội dung tự động thích ứng; không xuất hiện thanh cuộn ngang ngoài ý muốn.",
        ):
            scroll_width = self.page.evaluate("() => document.documentElement.scrollWidth")
            inner_width = self.page.evaluate("() => window.innerWidth")
            assert scroll_width <= inner_width + 10, (
                f"Phát hiện tràn ngang ngoài ý muốn: scrollWidth={scroll_width} > innerWidth={inner_width}"
            )

            self.highlight_actual_result(
                locator=shell.header,
                text="Bố cục co giãn thích ứng hoàn hảo ở mức thu phóng 150%, không bị vỡ giao diện",
            )
            self.step.set_actual(f"Không có tràn ngang (scrollWidth={scroll_width}, innerWidth={inner_width}).")

    def test_tc_ts_shl_val_011_logout_back_button_security(
        self, shell_data: Dict[str, Any], auth_mock
    ) -> None:
        """
        TC-SHL-011: Bảo vệ bảo mật sau khi Đăng xuất: Bấm nút Back trên trình duyệt không tải lại trang nội bộ từ cache.
        Scenario ID: TS-SHL-VAL | Traceability: VAL-LOGOUT-NO-CACHE; SECURITY
        """
        auth_mock("moehq")
        shell = self.get_page(AdminDashboardShellPage)
        base_url = shell_data["environments"]["base_url"]

        def handle_logout(route):
            route.fulfill(status=200, content_type="application/json", body='{"success": true}')

        self.page.route(shell_data["environments"]["logout_api"], handle_logout)

        try:
            with self.step(
                "Step 1: Đăng nhập và sau đó thực hiện Đăng xuất khỏi hệ thống",
                expected="Đăng xuất thành công và trình duyệt chuyển hướng về trang /login.",
            ):
                shell.open(base_url=base_url, path="/login")
                shell.open(base_url=base_url, path="/")
                expect(shell.sign_out_btn).to_be_visible()
                shell.sign_out()
                self.page.wait_for_url("**/login*", timeout=10000)
                expect(self.page).to_have_url(re.compile(r".*/login.*"))
                self.step.set_actual("Đã đăng xuất và đang ở trang /login.")

            # Now mock auth/me to return 401 unauthenticated so any cache bypass attempt is rejected
            def handle_unauth(route):
                route.fulfill(status=401, body='{"error": "Unauthorized"}')

            self.page.route(shell_data["environments"]["auth_me_api"], handle_unauth)

            with self.step(
                "Step 2: Nhấn nút Back trên trình duyệt để quay lại URL quản trị vừa xem",
                expected="Trình duyệt không tải dữ liệu quản trị từ disk cache; chuyển hướng về /login.",
            ):
                self.page.go_back()
                self.page.wait_for_load_state("domcontentloaded")
                expect(shell.nav).to_have_count(0)
                expect(shell.sidebar_container).to_have_count(0)
                expect(self.page).to_have_url(re.compile(r".*/login.*"))

                self.highlight_actual_result(
                    locator=shell.page_body,
                    text="Dữ liệu quản trị không bị khôi phục từ cache sau khi đăng xuất",
                )
                self.step.set_actual("Bấm Back không làm lộ dữ liệu quản trị; hệ thống chuyển hướng an toàn về /login.")
        finally:
            self.page.unroute(shell_data["environments"]["logout_api"])
            try:
                self.page.unroute(shell_data["environments"]["auth_me_api"])
            except Exception:
                pass
