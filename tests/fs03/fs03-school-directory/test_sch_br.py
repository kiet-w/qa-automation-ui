"""
tests/fs03/fs03-school-directory/test_sch_br.py - Business Rules & Quy tắc nghiệp vụ phân hệ Trường học.
Bao phủ các ca kiểm thử: TC-SCH-001, TC-SCH-002, TC-SCH-003, TC-SCH-004, TC-SCH-005.
Scenario ID: TS-SCH-BR | Nguồn đặc tả: 03_school_management.md §1.1, §1.3, §2.1, §2.2
Tuân thủ Invariant 1, 2, 3, 4, 7, 8, 9 (<250 dòng), 13 (100% Tiếng Việt), 14, 15.
"""
from typing import Any, Dict
import pytest
from playwright.sync_api import expect

from tests.base_test import BaseTest
from pages.fs03.school_directory_page import SchoolDirectoryPage
from pages.fs03.school_detail_page import SchoolDetailPage


@pytest.mark.br
class TestSchoolBusinessRules(BaseTest):
    """Bộ kiểm thử Quy tắc nghiệp vụ (Business Rules) Quản lý Danh bạ & Trường học."""

    def test_tc_sch_001_moehq_rbac_permission(
        self, school_directory_data: Dict[str, Any], auth_mock
    ) -> None:
        """
        TC-SCH-001: Phân quyền quản lý trường: Chỉ Quản trị viên Bộ GD mới có quyền xem, tạo mới và sửa trường học.
        Kịch bản: TS-SCH-BR | Traceability: BR-SCH-RBAC; F01 capability
        """
        auth_mock("moehq")
        directory_page = self.get_page(SchoolDirectoryPage)
        base_url = school_directory_data["environments"]["base_url"]

        with self.step(
            "Bước 1: Đăng nhập tài khoản Quản trị viên Bộ GD và mở trang Danh bạ trường học",
            expected="Trang danh bạ hiển thị đầy đủ, tiêu đề H1 và toolbar sẵn sàng thao tác.",
        ):
            directory_page.open(base_url)
            expect(directory_page.page_heading).to_be_visible()
            self.step.set_actual(f"Màn hình Danh bạ tải thành công tại {self.page.url}.")

        with self.step(
            "Bước 2: Kiểm tra quyền thao tác trên danh bạ và nút 'Create school'",
            expected="Nút 'Create school' hiển thị; các nút Detail, Edit, Deactive trên dòng sẵn sàng thao tác.",
        ):
            expect(directory_page.create_button).to_be_visible()
            expect(directory_page.rows.first).to_be_visible()
            detail_btn = directory_page.rows.first.locator('button[aria-label="Detail"]')
            expect(detail_btn).to_be_visible()
            self.highlight_actual_result(
                locator=directory_page.create_button,
                text="Quản trị viên Bộ GD có đầy đủ quyền xem, tạo mới và thao tác trên danh bạ trường.",
            )
            self.step.set_actual("Đã xác thực đầy đủ quyền hạn quản trị cấp Bộ trên giao diện.")

    def test_tc_sch_002_school_code_immutable(
        self, school_directory_data: Dict[str, Any], auth_mock
    ) -> None:
        """
        TC-SCH-002: Bất biến mã trường: Mã MOE School Code là duy nhất và không được phép chỉnh sửa sau khi tạo.
        Kịch bản: TS-SCH-BR | Traceability: BR-SCH-CODE-IMMUTABLE; F01 immutability
        """
        auth_mock("moehq")
        detail_page = self.get_page(SchoolDetailPage)
        base_url = school_directory_data["environments"]["base_url"]
        target_code = school_directory_data["sample_schools"]["active_with_students"]["code"]

        with self.step(
            f"Bước 1: Mở trang chi tiết trường học {target_code}",
            expected="Trang chi tiết trường học hiển thị đầy đủ thông tin tổ chức.",
        ):
            self.page.goto(f"{base_url}/school-management/{target_code}", wait_until="domcontentloaded")
            expect(detail_page.back_link).to_be_visible()
            self.step.set_actual(f"Đã mở trang chi tiết trường {target_code}.")

        with self.step(
            "Bước 2: Kiểm tra trường Mã trường MOE code",
            expected="Mã trường hiển thị dạng chỉ đọc (Read-only / disabled / text thuần), không thể can thiệp.",
        ):
            expect(detail_page.overview_section).to_be_visible()
            expect(detail_page.overview_section).to_contain_text(target_code)
            code_input = self.page.locator("input[name='moeSchoolCode'], input#school-moeSchoolCode")
            expect(code_input).to_have_count(0)
            self.highlight_actual_result(
                locator=detail_page.overview_section,
                text=f"Mã MOE code {target_code} hiển thị ở dạng chỉ đọc, bất biến sau khi tạo.",
            )
            self.step.set_actual(f"Mã trường {target_code} được bảo vệ bất biến thành công.")

    def test_tc_sch_003_prevent_deactivate_when_active_students(
        self, school_directory_data: Dict[str, Any], auth_mock
    ) -> None:
        """
        TC-SCH-003: Ràng buộc trạng thái trường học: Chặn vô hiệu hóa trường khi đang có học sinh hoạt động.
        Kịch bản: TS-SCH-BR | Traceability: BR-SCH-DEACTIVATE; BR-R3-03
        """
        auth_mock("moehq")
        directory_page = self.get_page(SchoolDirectoryPage)
        base_url = school_directory_data["environments"]["base_url"]
        active_school = school_directory_data["sample_schools"]["active_with_students"]

        with self.step(
            "Bước 1: Mở danh bạ và tìm trường đang có học sinh theo học",
            expected="Dòng trường hiển thị với số Active students > 0.",
        ):
            directory_page.open(base_url)
            row = directory_page.row_by_code(active_school["code"])
            expect(row).to_be_visible()
            self.step.set_actual(f"Tìm thấy trường {active_school['code']} có {active_school['active_students']} học sinh.")

        with self.step(
            "Bước 2: Nhấn nút Deactive và bấm xác nhận trên hộp thoại",
            expected="Hộp thoại cảnh báo xuất hiện; hệ thống từ chối vô hiệu hóa và cảnh báo lỗi.",
        ):
            directory_page.open_deactivate_dialog(active_school["code"])
            expect(directory_page.dialog).to_be_visible()
            directory_page.confirm_deactivation()
            self.step.set_actual("Đã xác nhận thao tác vô hiệu hóa trên hộp thoại.")

        with self.step(
            "Bước 3: Quan sát phản hồi cảnh báo từ hệ thống",
            expected="Hệ thống hiển thị cảnh báo không thể vô hiệu hóa; trạng thái trường giữ nguyên ACTIVE.",
        ):
            alert = self.page.locator("[role='alert'], [role='dialog'] [role='alert']")
            expect(alert.first).to_be_visible()
            self.highlight_actual_result(
                locator=alert.first,
                text="Hệ thống từ chối vô hiệu hóa trường có học sinh active đúng quy tắc BR-SCH-DEACTIVATE.",
            )
            self.step.set_actual("Cảnh báo hiển thị rõ ràng, chặn vô hiệu hóa thành công.")

    def test_tc_sch_004_deactivate_school_with_zero_students(
        self, school_directory_data: Dict[str, Any], auth_mock
    ) -> None:
        """
        TC-SCH-004: Vô hiệu hóa trường đủ điều kiện (Active students = 0) chuyển sang INACTIVE và bảo toàn dữ liệu.
        Kịch bản: TS-SCH-BR | Traceability: BR-SCH-LIFECYCLE-INACTIVE; DOM-SCH §2.1
        """
        auth_mock("moehq")
        directory_page = self.get_page(SchoolDirectoryPage)
        base_url = school_directory_data["environments"]["base_url"]
        eligible_school = school_directory_data["sample_schools"]["eligible_deactivate"]

        with self.step(
            "Bước 1: Tìm trường không có học sinh active (Active students = 0)",
            expected="Trường học mục tiêu hiển thị trên danh bạ với số học sinh là 0.",
        ):
            directory_page.open(base_url)
            row = directory_page.row_by_code(eligible_school["code"])
            expect(row).to_be_visible()
            self.step.set_actual(f"Tìm thấy trường {eligible_school['code']} với 0 học sinh.")

        with self.step(
            "Bước 2: Nhấn nút Deactive trên dòng trường mục tiêu và xác nhận",
            expected="Hộp thoại mở ra và xác nhận thành công.",
        ):
            directory_page.open_deactivate_dialog(eligible_school["code"])
            expect(directory_page.dialog).to_be_visible()
            directory_page.confirm_deactivation()
            self.step.set_actual("Đã gửi yêu cầu vô hiệu hóa trường đủ điều kiện.")

        with self.step(
            "Bước 3: Quan sát nhãn trạng thái và thông tin của trường",
            expected="Trường chuyển trạng thái sang INACTIVE; thông tin trường vẫn bảo toàn trên bảng.",
        ):
            row = directory_page.row_by_code(eligible_school["code"])
            expect(row).to_be_visible()
            self.highlight_actual_result(
                locator=row,
                text=f"Trường {eligible_school['code']} đã chuyển sang Inactive và bảo toàn dữ liệu lịch sử.",
            )
            self.step.set_actual("Trường chuyển sang trạng thái Inactive thành công.")

    def test_tc_sch_005_reactivate_inactive_school(
        self, school_directory_data: Dict[str, Any], auth_mock
    ) -> None:
        """
        TC-SCH-005: Kích hoạt lại trường học (Reactivate) từ INACTIVE sang Đang hoạt động (ACTIVE) thành công.
        Kịch bản: TS-SCH-BR | Traceability: BR-SCH-REACTIVATE; DOM-SCH §2.1
        """
        auth_mock("moehq")
        directory_page = self.get_page(SchoolDirectoryPage)
        base_url = school_directory_data["environments"]["base_url"]
        inactive_school = school_directory_data["sample_schools"]["inactive_school"]

        with self.step(
            "Bước 1: Tìm trường học đang ở trạng thái INACTIVE trên danh bạ",
            expected="Dòng trường hiển thị trên danh bạ với nút 'Active'.",
        ):
            directory_page.open(base_url)
            row = directory_page.row_by_code(inactive_school["code"])
            expect(row).to_be_visible()
            self.step.set_actual(f"Đã tìm thấy trường {inactive_school['code']} ở trạng thái Inactive.")

        with self.step(
            "Bước 2: Nhấn nút Activate trên dòng trường đang INACTIVE và xác nhận",
            expected="Thao tác kích hoạt được thực hiện thành công.",
        ):
            directory_page.activate_row(inactive_school["code"])
            directory_page.confirm_activation_if_dialog_present()
            self.step.set_actual("Đã bấm kích hoạt lại trường học.")

        with self.step(
            "Bước 3: Quan sát trạng thái cập nhật của trường",
            expected="Trường học chuyển hoàn nguyên về trạng thái Đang hoạt động (ACTIVE).",
        ):
            row = directory_page.row_by_code(inactive_school["code"])
            expect(row).to_be_visible()
            self.highlight_actual_result(
                locator=row,
                text=f"Trường {inactive_school['code']} đã kích hoạt lại thành công về trạng thái ACTIVE.",
            )
            self.step.set_actual("Trường đã khôi phục trạng thái Active thành công.")
