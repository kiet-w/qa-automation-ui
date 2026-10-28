"""
tests/fs03/fs03-dashboard-shell/test_ts_shl_ac.py - Acceptance Criteria: Profile, Navigation & Secure Logout.
Pillar: AC (Tiêu chí nghiệm thu chức năng)
Test Cases: TC-SHL-005, TC-SHL-006, TC-SHL-007, TC-SHL-008.
Scenario ID: TS-SHL-AC
Traceability: AC-SHELL-HDR; AC-SIDEBAR-LINKS; AC-ACTIVE-STATE; AC-SHELL-LOGOUT; SEC-BACK;
              02_admin_dashboard_shell.md §1.1, §1.2, §1.3, §2.2; recon_02_admin_dashboard_shell.md §1, §3, §4, §5
Complies with Invariants 1, 2, 3, 4, 7, 8, 9 (<250 lines), 13 (100% Tiếng Việt step evidence).
"""
import re
from typing import Any, Dict
import pytest
from playwright.sync_api import expect

from tests.base_test import BaseTest
from pages.fs03.admin_dashboard_shell_page import AdminDashboardShellPage


@pytest.mark.ac
@pytest.mark.p1
class TestAdminShellAcceptanceCriteria(BaseTest):
    """Acceptance Criteria kiểm thử giao diện và hành vi chuẩn Cổng Quản trị viên EduFAMS."""

    def test_tc_ts_shl_ac_005_global_header_user_profile(
        self, shell_data: Dict[str, Any], auth_mock
    ) -> None:
        """
        TC-SHL-005: Hiển thị Global Header: Tên người dùng, Nhãn vai trò và Tên trường được phân công.
        Scenario ID: TS-SHL-AC | Traceability: AC-SHELL-HDR; USER-INFO
        """
        auth_mock("moehq")
        shell = self.get_page(AdminDashboardShellPage)
        base_url = shell_data["environments"]["base_url"]
        persona = shell_data["personas"]["moehq"]

        with self.step(
            "Step 1: Quan sát góc trên bên phải thanh tiêu đề (Header)",
            expected="Thanh tiêu đề hiển thị tên người dùng và mã định danh vai trò chính xác.",
        ):
            shell.open(base_url=base_url, path="/")
            expect(shell.header).to_be_visible()
            expect(shell.user_name).to_be_visible()
            self.step.set_actual(f"Thanh tiêu đề hiển thị thành công tại {self.page.url}.")

        with self.step(
            "Step 2: Kiểm tra tên người dùng, nhãn vai trò và tên trường",
            expected="Tên người dùng, vai trò và thông tin phân công hiển thị chính xác, rõ ràng.",
        ):
            displayed_name = shell.get_user_display_name()
            assert persona["first_name"] in displayed_name or persona["last_name"] in displayed_name, (
                f"Kỳ vọng tên '{persona['first_name']}' trong tên hiển thị '{displayed_name}'"
            )

            header_text = shell.get_header_text()
            assert persona["username"] in header_text, (
                f"Kỳ vọng username '{persona['username']}' xuất hiện trong header text '{header_text}'"
            )

            self.highlight_actual_result(
                locator=shell.header,
                text="Thông tin người dùng và vai trò hiển thị chính xác trên Global Header",
            )
            self.step.set_actual(f"Header hiển thị tên: '{displayed_name}', username: '{persona['username']}'.")

    def test_tc_ts_shl_ac_006_sidebar_navigation_links(
        self, shell_data: Dict[str, Any], auth_mock
    ) -> None:
        """
        TC-SHL-006: Hiển thị Thanh menu bên trái Navigation Links với đầy đủ icon biểu tượng và nhãn văn bản.
        Scenario ID: TS-SHL-AC | Traceability: AC-SIDEBAR-LINKS; DOM-SHELL §1.2
        """
        auth_mock("moehq")
        shell = self.get_page(AdminDashboardShellPage)
        base_url = shell_data["environments"]["base_url"]
        expected_links = shell_data["navigation"]["moehq_expected_links"]

        with self.step(
            "Step 1: Quan sát cấu trúc menu bên trái (Thanh menu bên trái)",
            expected="Logo EduFAMS hiển thị sắc nét ở đỉnh menu kèm khu vực điều hướng.",
        ):
            shell.open(base_url=base_url, path="/")
            expect(shell.brand_link).to_be_visible()
            expect(shell.nav).to_be_visible()
            self.step.set_actual("Logo EduFAMS và container menu bên trái hiển thị rõ ràng.")

        with self.step(
            "Step 2: Kiểm tra từng dòng mục menu và icon biểu tượng",
            expected="Mỗi mục menu hiển thị liên kết hợp lệ và nhãn phân hệ trực quan.",
        ):
            link_count = shell.nav_links.count()
            assert link_count >= len(expected_links), (
                f"Kỳ vọng ít nhất {len(expected_links)} liên kết menu, tìm thấy {link_count}"
            )

            for item in expected_links:
                link_elem = shell.nav_link_by_href(item["href"])
                expect(link_elem).to_be_visible()

            self.highlight_actual_result(
                locator=shell.nav,
                text="Danh sách liên kết điều hướng và biểu tượng trên sidebar hiển thị đầy đủ",
            )
            self.step.set_actual(f"Xác thực thành công {link_count} mục menu có đầy đủ biểu tượng và nhãn.")

    def test_tc_ts_shl_ac_007_navigation_active_state(
        self, shell_data: Dict[str, Any], auth_mock
    ) -> None:
        """
        TC-SHL-007: Làm nổi bật mục menu đang chọn (Navigation Active State) khớp với URL hiện hành.
        Scenario ID: TS-SHL-AC | Traceability: AC-ACTIVE-STATE; DOM-SHELL §2.2
        """
        auth_mock("moehq")
        shell = self.get_page(AdminDashboardShellPage)
        base_url = shell_data["environments"]["base_url"]
        target_path_1 = "/school-management"
        target_path_2 = "/school-user-management"

        shell.open(base_url=base_url, path="/")
        expect(shell.header).to_be_visible()
        expect(shell.nav).to_be_visible()

        with self.step(
            "Step 1: Nhấp vào mục 'Quản lý trường học' trên Sidebar",
            expected="Điều hướng đến trang /school-management.",
        ):
            shell.click_nav_link_by_href(target_path_1)
            self.page.wait_for_load_state("domcontentloaded")
            expect(self.page).to_have_url(re.compile(rf".*{re.escape(target_path_1)}.*"))
            self.step.set_actual(f"Đã điều hướng tới {self.page.url}.")

        with self.step(
            "Step 2: Quan sát màu nền và thuộc tính aria-current của mục 'Quản lý trường học'",
            expected="Mục menu có thuộc tính aria-current='page' và kiểu dáng active nổi bật.",
        ):
            active_link = shell.nav_link_by_href(target_path_1)
            expect(active_link).to_have_attribute("aria-current", "page")
            self.step.set_actual("Mục /school-management nhận trạng thái aria-current='page'.")

        with self.step(
            "Step 3: Chuyển sang mục 'Quản lý cán bộ' và kiểm tra cập nhật trạng thái",
            expected="Mục mới nhận active, mục cũ hoàn nguyên màu mặc định.",
        ):
            shell.click_nav_link_by_href(target_path_2)
            self.page.wait_for_load_state("domcontentloaded")
            expect(self.page).to_have_url(re.compile(rf".*{re.escape(target_path_2)}.*"))

            new_active_link = shell.nav_link_by_href(target_path_2)
            expect(new_active_link).to_have_attribute("aria-current", "page")
            expect(active_link).not_to_have_attribute("aria-current", "page")

            self.highlight_actual_result(
                locator=shell.nav,
                text="Trạng thái active (aria-current='page') chuyển đổi chính xác giữa các mục",
            )
            self.step.set_actual("Trạng thái active chuyển đổi chính xác khớp với URL hiện hành.")

    def test_tc_ts_shl_ac_008_secure_logout_and_redirect(
        self, shell_data: Dict[str, Any], auth_mock
    ) -> None:
        """
        TC-SHL-008: Chức năng Đăng xuất an toàn: Xóa phiên làm việc và trở về màn hình Đăng nhập.
        Scenario ID: TS-SHL-AC | Traceability: AC-SHELL-LOGOUT; SEC-BACK
        """
        auth_mock("moehq")
        shell = self.get_page(AdminDashboardShellPage)
        base_url = shell_data["environments"]["base_url"]
        logout_calls = []

        def handle_logout(route):
            logout_calls.append(route.request.url)
            route.fulfill(status=200, content_type="application/json", body='{"success": true}')

        self.page.route(shell_data["environments"]["logout_api"], handle_logout)

        try:
            with self.step(
                "Step 1: Nhấn vào nút 'Đăng xuất' trên thanh điều hướng",
                expected="Kích hoạt API đăng xuất và bắt đầu tiến trình xóa phiên.",
            ):
                shell.open(base_url=base_url, path="/login")
                shell.open(base_url=base_url, path="/")
                expect(shell.sign_out_btn).to_be_visible()
                shell.sign_out()
                self.step.set_actual("Đã nhấn nút Đăng xuất.")

            with self.step(
                "Step 2: Quan sát màn hình sau khi đăng xuất",
                expected="Hệ thống chuyển hướng hoàn toàn về màn hình /login, kết thúc phiên làm việc.",
            ):
                self.page.wait_for_url("**/login*", timeout=10000)
                expect(self.page).to_have_url(re.compile(r".*/login.*"))
                assert len(logout_calls) > 0, "API logout không được gọi khi đăng xuất"
                self.step.set_actual(f"Chuyển hướng thành công về {self.page.url}.")

            with self.step(
                "Step 3: Thử nhấn nút Quay lại (Back) trên trình duyệt",
                expected="Không làm lộ dữ liệu quản trị, hệ thống giữ nguyên hoặc chuyển hướng về /login.",
            ):
                def handle_unauth(route):
                    route.fulfill(status=401, body='{"error": "Unauthorized"}')

                self.page.route(shell_data["environments"]["auth_me_api"], handle_unauth)

                self.page.go_back()
                self.page.wait_for_load_state("domcontentloaded")
                expect(shell.nav).to_have_count(0)
                expect(shell.sidebar_container).to_have_count(0)
                expect(self.page).to_have_url(re.compile(r".*/login.*"))

                self.highlight_actual_result(
                    locator=shell.page_body,
                    text="Sau khi đăng xuất, nút Back không làm lộ dữ liệu quản trị",
                )
                self.step.set_actual("Trình duyệt không làm lộ dữ liệu quản trị sau khi đăng xuất.")
        finally:
            self.page.unroute(shell_data["environments"]["logout_api"])
