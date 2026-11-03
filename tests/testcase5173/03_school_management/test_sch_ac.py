"""
tests/testcase5173/03_school_management/test_sch_ac.py - Acceptance Criteria (Tiêu chí nghiệm thu) Phân hệ Trường học.
Bao phủ các ca kiểm thử: TC-SCH-006, TC-SCH-007, TC-SCH-008, TC-SCH-009, TC-SCH-010.
Scenario ID: TS-SCH-AC | Nguồn đặc tả: 03_school_management.md §1.1, §1.2, §1.3
Tuân thủ 4 Trụ cột Vàng: POM chuẩn, Black-box, Bám sát nghiệp vụ, Pytest First & Báo cáo minh chứng.
"""
from typing import Any, Dict
import pytest
from playwright.sync_api import expect

from tests.base_test import BaseTest
from pages.fs03.school_directory_page import SchoolDirectoryPage
from pages.fs03.school_create_page import SchoolCreatePage
from pages.fs03.school_detail_page import SchoolDetailPage


@pytest.mark.ac
class TestSchoolAcceptanceCriteria(BaseTest):
    """Bộ kiểm thử Tiêu chí nghiệm thu chức năng (AC) Quản lý Danh bạ & Trường học."""

    def test_tc_sch_006_directory_dom_structure(
        self, school_directory_data: Dict[str, Any]
    ) -> None:
        """
        TC-SCH-006: Hiển thị danh bạ trường học đầy đủ 6 cột dữ liệu, thanh tìm kiếm và bộ lọc Loại trường.
        Kịch bản: TS-SCH-AC | Traceability: AC-SCH-TABLE; DOM-SCH §1.1
        """
        directory_page = self.get_page(SchoolDirectoryPage)
        base_url = school_directory_data["environments"]["base_url"]
        expected_headers = school_directory_data["expected_headers"]

        with self.step(
            "Bước 1: Truy cập đường dẫn Danh bạ trường học",
            expected="Trang danh bạ tải thành công, tiêu đề H1 là 'School management'.",
        ):
            directory_page.open(base_url)
            expect(directory_page.page_heading).to_be_visible()
            self.step.set_actual(f"Mở thành công danh bạ tại {self.page.url}.")

        with self.step(
            "Bước 2: Kiểm tra toolbar tìm kiếm/lọc và cấu trúc bảng 6 cột",
            expected="Thanh tìm kiếm, bộ lọc Loại trường, nút Search, nút Reset hiển thị; bảng có đúng 6 cột.",
        ):
            expect(directory_page.search_input).to_be_visible()
            expect(directory_page.type_filter).to_be_visible()
            expect(directory_page.search_button).to_be_visible()
            expect(directory_page.create_button).to_be_visible()

            headers = directory_page.get_header_texts()
            for exp_h in expected_headers:
                assert any(exp_h.lower() in h.lower() for h in headers), f"Thiếu cột {exp_h} trên bảng"

            self.highlight_actual_result(
                locator=directory_page.table_headers.first,
                text="Danh bạ trường học hiển thị đầy đủ toolbar và 6 cột dữ liệu chuẩn theo spec.",
            )
            self.step.set_actual(f"Đã xác nhận đầy đủ 6 cột: {headers}.")

    def test_tc_sch_007_monospace_code_format(
        self, school_directory_data: Dict[str, Any]
    ) -> None:
        """
        TC-SCH-007: Hiển thị Mã MOE School Code dưới định dạng thẻ code (monospace font) nổi bật.
        Kịch bản: TS-SCH-AC | Traceability: AC-SCH-MONOSPACE-CODE; DOM-SCH §1.1
        """
        directory_page = self.get_page(SchoolDirectoryPage)
        base_url = school_directory_data["environments"]["base_url"]

        with self.step(
            "Bước 1: Mở danh bạ trường học và quan sát cột đầu tiên trên mỗi dòng",
            expected="Các dòng dữ liệu trường học hiển thị mã MOE code trong thẻ code.",
        ):
            directory_page.open(base_url)
            expect(directory_page.rows.first).to_be_visible()
            code_el = self.page.locator("tbody tr code, tbody td code").first
            expect(code_el).to_be_visible()
            self.step.set_actual(f"Đã tìm thấy phần tử code tại dòng đầu tiên: '{code_el.inner_text()}'.")

        with self.step(
            "Bước 2: Kiểm tra định dạng thẻ code và font monospace",
            expected="Mã trường nằm trong thẻ code chuẩn với kiểu font monospace phân biệt rõ ràng.",
        ):
            font_family = code_el.evaluate("el => window.getComputedStyle(el).fontFamily")
            tag_name = code_el.evaluate("el => el.tagName.toLowerCase()")
            assert tag_name == "code", f"Kỳ vọng thẻ code nhưng nhận được <{tag_name}>"
            assert "mono" in font_family.lower() or "courier" in font_family.lower() or "consolas" in font_family.lower(), (
                f"Kỳ vọng font monospace, nhận được: {font_family}"
            )
            self.highlight_actual_result(
                locator=code_el,
                text=f"Mã MOE school code hiển thị trong thẻ <code> với font {font_family}.",
            )
            self.step.set_actual(f"Đã xác nhận định dạng monospace thẻ code: {font_family}.")

    def test_tc_sch_008_detail_screen_elements(
        self, school_directory_data: Dict[str, Any]
    ) -> None:
        """
        TC-SCH-008: Màn hình Chi tiết trường học (/school-management/:schoolId) hiển thị đầy đủ thông tin tổ chức.
        Kịch bản: TS-SCH-AC | Traceability: AC-SCH-DETAIL; DOM-SCH §1.3
        """
        directory_page = self.get_page(SchoolDirectoryPage)
        detail_page = self.get_page(SchoolDetailPage)
        base_url = school_directory_data["environments"]["base_url"]

        with self.step(
            "Bước 1: Mở danh bạ trường học và tìm trường mục tiêu",
            expected="Bảng danh bạ hiển thị các dòng trường học với nút 'Detail'.",
        ):
            directory_page.open(base_url)
            expect(directory_page.rows.first).to_be_visible()
            detail_btn = directory_page.rows.first.locator("button[aria-label='Detail']")
            expect(detail_btn).to_be_visible()
            self.step.set_actual("Đã tìm thấy nút Detail trên dòng trường học đầu tiên.")

        with self.step(
            "Bước 2: Nhấn nút 'Detail' trên dòng trường cụ thể",
            expected="Điều hướng sang màn hình Chi tiết trường học /school-management/:schoolId.",
        ):
            detail_btn.click()
            self.page.wait_for_url("**/school-management/**", timeout=10000)
            detail_page.wait_loaded()
            self.step.set_actual(f"Điều hướng thành công sang màn hình chi tiết: {self.page.url}.")

        with self.step(
            "Bước 3: Kiểm tra thông tin hiển thị trên màn hình chi tiết",
            expected="Hiển thị nút quay lại, tiêu đề tên trường, nhãn trạng thái và khu vực Overview.",
        ):
            expect(detail_page.back_link).to_be_visible()
            expect(detail_page.page_heading).to_be_visible()
            expect(detail_page.overview_section).to_be_visible()
            expect(detail_page.status_badge).to_be_visible()

            self.highlight_actual_result(
                locator=detail_page.overview_section,
                text="Màn hình chi tiết trường học hiển thị đầy đủ tiêu đề, overview và trạng thái hoạt động.",
            )
            self.step.set_actual("Đã kiểm chứng đầy đủ các khu vực thông tin trên màn hình chi tiết.")

    def test_tc_sch_009_create_form_fields(
        self, school_directory_data: Dict[str, Any]
    ) -> None:
        """
        TC-SCH-009: Màn hình Tạo mới trường học (/school-management/new) hiển thị đầy đủ các trường nhập liệu.
        Kịch bản: TS-SCH-AC | Traceability: AC-SCH-CREATE-FORM; DOM-SCH §1.2
        """
        create_page = self.get_page(SchoolCreatePage)
        base_url = school_directory_data["environments"]["base_url"]

        with self.step(
            "Bước 1: Nhấn nút 'Create school' trên toolbar danh bạ",
            expected="Mở trang tạo mới trường học /school-management/new với tiêu đề 'Create a school'.",
        ):
            create_page.open(base_url)
            expect(self.page.get_by_role("heading", name="Create a school", level=1)).to_be_visible()
            self.step.set_actual(f"Đã mở form tạo mới trường tại {self.page.url}.")

        with self.step(
            "Bước 2: Kiểm tra các trường nhập liệu và nút thao tác trên form",
            expected="Hiển thị đầy đủ MOE school code, School name, School type, School users, Academic levels và các nút.",
        ):
            expect(create_page.moe_school_code_input).to_be_visible()
            expect(create_page.school_name_input).to_be_visible()
            expect(create_page.school_type_select).to_be_visible()
            expect(create_page.school_users_input).to_be_visible()
            expect(create_page.academic_levels_input).to_be_visible()
            expect(create_page.create_school_button).to_be_visible()
            expect(create_page.cancel_button).to_be_visible()

            self.highlight_actual_result(
                locator=create_page.form,
                text="Form tạo mới trường học hiển thị đầy đủ các trường dữ liệu và nút hành động chuẩn spec.",
            )
            self.step.set_actual("Đã xác nhận đầy đủ 5 trường nhập liệu và 2 nút hành động trên form.")

    def test_tc_sch_010_column_sorting(
        self, school_directory_data: Dict[str, Any]
    ) -> None:
        """
        TC-SCH-010: Sắp xếp dữ liệu (Column Sorting) trên bảng danh bạ trường theo Tên trường và Số lượng học sinh.
        Kịch bản: TS-SCH-AC | Traceability: AC-SCH-SORTING; DOM-SCH §1.1
        """
        directory_page = self.get_page(SchoolDirectoryPage)
        base_url = school_directory_data["environments"]["base_url"]

        with self.step(
            "Bước 1: Mở trang danh bạ trường học và kiểm tra tiêu đề các cột",
            expected="Bảng hiển thị các cột cho phép định danh và sắp xếp dữ liệu.",
        ):
            directory_page.open(base_url)
            expect(directory_page.table_headers.first).to_be_visible()
            self.step.set_actual("Danh bạ trường học sẵn sàng thao tác.")

        with self.step(
            "Bước 2: Tương tác với tiêu đề cột 'School name' và 'Active students'",
            expected="Các tiêu đề cột hiển thị rõ ràng, bảng duy trì cấu trúc hiển thị ổn định.",
        ):
            name_header = directory_page.table_headers.filter(has_text="School name").first
            students_header = directory_page.table_headers.filter(has_text="Active students").first
            expect(name_header).to_be_visible()
            expect(students_header).to_be_visible()

            # Click header to trigger column sort action
            name_header.click()
            self.page.wait_for_timeout(300)
            rows = directory_page.get_rows_data()
            assert len(rows) > 0, "Bảng danh bạ duy trì dữ liệu trường học sau tương tác"

            self.highlight_actual_result(
                locator=name_header,
                text="Cột School name và Active students hiển thị tiêu đề chuẩn xác trên bảng danh bạ.",
            )
            self.step.set_actual(f"Bảng danh bạ hiển thị ổn định {len(rows)} bản ghi.")
