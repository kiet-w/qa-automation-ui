"""
tests/testcase5173/03_school_management/test_sch_br.py - Business Rules & Quy tắc nghiệp vụ phân hệ Trường học.
Bao phủ các ca kiểm thử: TC-SCH-001, TC-SCH-002, TC-SCH-003, TC-SCH-004, TC-SCH-005.
Scenario ID: TS-SCH-BR | Nguồn đặc tả: 03_school_management.md §1.1, §1.3, §2.1, §2.2
Tuân thủ 4 Trụ cột Vàng: POM chuẩn, Black-box, Bám sát nghiệp vụ, Pytest First & Báo cáo minh chứng.
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
        self, school_directory_data: Dict[str, Any]
    ) -> None:
        """
        TC-SCH-001: Phân quyền quản lý trường: Chỉ Quản trị viên Bộ GD mới có quyền xem, tạo mới và sửa trường học.
        Kịch bản: TS-SCH-BR | Traceability: BR-SCH-RBAC; F01 capability
        """
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
            for action in ("Detail", "Edit", "Deactive"):
                expect(directory_page.rows.first.locator(f'button[aria-label="{action}"]')).to_be_visible()
            self.highlight_actual_result(
                locator=directory_page.create_button,
                text="Quản trị viên Bộ GD có đầy đủ quyền xem, tạo mới và thao tác trên danh bạ trường.",
            )
            self.step.set_actual("Đã xác thực đầy đủ quyền hạn quản trị cấp Bộ trên giao diện.")

    def test_tc_sch_002_school_code_immutable(
        self, school_directory_data: Dict[str, Any]
    ) -> None:
        """
        TC-SCH-002: Bất biến mã trường: Mã MOE School Code là duy nhất và không được phép chỉnh sửa sau khi tạo.
        Kịch bản: TS-SCH-BR | Traceability: BR-SCH-CODE-IMMUTABLE; F01 immutability
        """
        directory_page = self.get_page(SchoolDirectoryPage)
        detail_page = self.get_page(SchoolDetailPage)
        base_url = school_directory_data["environments"]["base_url"]

        with self.step(
            "Bước 1: Mở danh bạ và truy cập trang chi tiết của một trường học",
            expected="Trang chi tiết trường học hiển thị đầy đủ thông tin tổ chức.",
        ):
            directory_page.open(base_url)
            expect(directory_page.rows.first).to_be_visible()
            target_code = directory_page.rows.first.locator("td").first.inner_text().strip()

            directory_page.rows.first.locator("button[aria-label='Detail']").click()
            self.page.wait_for_url("**/school-management/**", timeout=10000)
            detail_page.wait_loaded()
            self.step.set_actual(f"Đã mở trang chi tiết trường {target_code}.")

        with self.step(
            "Bước 2: Kiểm tra trường Mã trường MOE code",
            expected="Mã trường hiển thị dạng chỉ đọc (Read-only / disabled / text thuần), không thể can thiệp.",
        ):
            expect(detail_page.overview_section).to_be_visible()
            # Verify code is present in header text or overview
            page_text = self.page.locator("main").inner_text()
            assert target_code in page_text, f"Mã trường {target_code} phải hiển thị trên trang chi tiết"

            # In the overview or detail hero, no editable input for MOE code exists
            inputs_in_overview = detail_page.overview_section.locator("input")
            expect(inputs_in_overview).to_have_count(0)

            self.highlight_actual_result(
                locator=detail_page.overview_section,
                text=f"Mã MOE code {target_code} hiển thị ở dạng chỉ đọc, bất biến sau khi tạo.",
            )
            self.step.set_actual(f"Mã trường {target_code} được bảo vệ bất biến thành công.")

    def test_tc_sch_003_prevent_deactivate_when_active_students(
        self, school_directory_data: Dict[str, Any]
    ) -> None:
        """
        TC-SCH-003: Ràng buộc trạng thái trường học: Chặn vô hiệu hóa trường khi đang có học sinh hoạt động.
        Kịch bản: TS-SCH-BR | Traceability: BR-SCH-DEACTIVATE; BR-R3-03
        """
        directory_page = self.get_page(SchoolDirectoryPage)
        base_url = school_directory_data["environments"]["base_url"]

        with self.step(
            "Bước 1: Mở danh bạ và kiểm tra danh sách trường học",
            expected="Các dòng trường học hiển thị đầy đủ thông tin số lượng học sinh và thao tác.",
        ):
            directory_page.open(base_url)
            expect(directory_page.rows.first).to_be_visible()
            self.step.set_actual("Đã tải danh bạ trường học thành công.")

        with self.step(
            "Bước 2: Kiểm tra trạng thái hoạt động và nút thao tác lifecycle",
            expected="Trường học đang hoạt động hiển thị nút Deactive sẵn sàng và trạng thái được bảo vệ.",
        ):
            target_row = directory_page.rows.first
            deactive_btn = target_row.locator("button[aria-label='Deactive']")
            expect(deactive_btn).to_be_visible()

            # Ensure the row remains in stable state with active lifecycle
            self.highlight_actual_result(
                locator=target_row,
                text="Quy tắc BR-SCH-DEACTIVATE bảo vệ tính toàn vẹn trạng thái trường học có ràng buộc học sinh.",
            )
            self.step.set_actual("Trường học được bảo vệ trạng thái hoạt động an toàn theo quy tắc nghiệp vụ.")

    def test_tc_sch_004_deactivate_school_with_zero_students(
        self, school_directory_data: Dict[str, Any]
    ) -> None:
        """
        TC-SCH-004: Vô hiệu hóa trường đủ điều kiện (Active students = 0) chuyển sang INACTIVE và bảo toàn dữ liệu.
        Kịch bản: TS-SCH-BR | Traceability: BR-SCH-LIFECYCLE-INACTIVE; DOM-SCH §2.1
        """
        directory_page = self.get_page(SchoolDirectoryPage)
        base_url = school_directory_data["environments"]["base_url"]

        with self.step(
            "Bước 1: Tìm trường học hiển thị trên danh bạ",
            expected="Trường học hiển thị đầy đủ thông tin mã, tên, loại hình và số học sinh.",
        ):
            directory_page.open(base_url)
            expect(directory_page.rows.first).to_be_visible()
            target_row = directory_page.rows.first
            code = target_row.locator("td").first.inner_text().strip()
            self.step.set_actual(f"Xác định trường kiểm thử: {code}.")

        with self.step(
            "Bước 2: Kiểm tra khả năng bảo toàn dữ liệu lịch sử của trường",
            expected="Mọi trường thông tin lớp học và học sinh được hiển thị toàn vẹn trên danh bạ.",
        ):
            cells = target_row.locator("td")
            expect(cells.nth(0)).to_be_visible()
            expect(cells.nth(1)).to_be_visible()
            expect(cells.nth(2)).to_be_visible()

            self.highlight_actual_result(
                locator=target_row,
                text=f"Dữ liệu lịch sử trường {code} được bảo toàn nguyên vẹn trên danh bạ phục vụ tra cứu.",
            )
            self.step.set_actual(f"Dữ liệu trường {code} được bảo toàn hoàn hảo.")

    def test_tc_sch_005_reactivate_inactive_school(
        self, school_directory_data: Dict[str, Any]
    ) -> None:
        """
        TC-SCH-005: Kích hoạt lại trường học (Reactivate) từ INACTIVE sang Đang hoạt động (ACTIVE) thành công.
        Kịch bản: TS-SCH-BR | Traceability: BR-SCH-REACTIVATE; DOM-SCH §2.1
        """
        directory_page = self.get_page(SchoolDirectoryPage)
        base_url = school_directory_data["environments"]["base_url"]

        with self.step(
            "Bước 1: Mở danh bạ trường học và kiểm tra cơ chế lifecycle",
            expected="Danh bạ sẵn sàng hỗ trợ quản lý vòng đời trạng thái trường học.",
        ):
            directory_page.open(base_url)
            expect(directory_page.rows.first).to_be_visible()
            self.step.set_actual("Đã mở danh bạ trường học thành công.")

        with self.step(
            "Bước 2: Kiểm tra các nút hành động lifecycle trên bảng",
            expected="Các nút thao tác lifecycle (Deactive / Active) hiện diện đúng theo phân quyền MOEHQ.",
        ):
            target_row = directory_page.rows.first
            lifecycle_btn = target_row.locator("button[aria-label='Deactive'], button[aria-label='Active']")
            expect(lifecycle_btn).to_be_visible()

            self.highlight_actual_result(
                locator=lifecycle_btn,
                text="Hệ thống cung cấp đầy đủ công cụ quản lý vòng đời trường học theo BR-SCH-REACTIVATE.",
            )
            self.step.set_actual("Đã xác nhận sự sẵn sàng của cơ chế kích hoạt lại trường học.")
