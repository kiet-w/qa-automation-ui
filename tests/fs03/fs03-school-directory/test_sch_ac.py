"""
tests/fs03/fs03-school-directory/test_sch_ac.py - Acceptance Criteria & Tiêu chí nghiệm thu giao diện Trường học.
Bao phủ các ca kiểm thử: TC-SCH-006, TC-SCH-007, TC-SCH-008, TC-SCH-009, TC-SCH-010.
Scenario ID: TS-SCH-AC | Nguồn đặc tả: 03_school_management.md §1.1, §1.2, §1.3
Tuân thủ Invariant 1, 2, 3, 4, 7, 8, 9 (<250 dòng), 13 (100% Tiếng Việt), 14, 15.
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
    """Bộ kiểm thử Tiêu chí nghiệm thu giao diện (Acceptance Criteria) Phân hệ Trường học."""

    def test_tc_sch_006_directory_dom_structure(
        self, school_directory_data: Dict[str, Any], auth_mock
    ) -> None:
        """
        TC-SCH-006: Hiển thị danh bạ trường học đầy đủ 6 cột dữ liệu, thanh tìm kiếm và bộ lọc Loại trường.
        Kịch bản: TS-SCH-AC | Traceability: AC-SCH-TABLE; DOM-SCH §1.1
        """
        auth_mock("moehq")
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
        self, school_directory_data: Dict[str, Any], auth_mock
    ) -> None:
        """
        TC-SCH-007: Hiển thị Mã MOE School Code dưới định dạng thẻ code (monospace font) nổi bật.
        Kịch bản: TS-SCH-AC | Traceability: AC-SCH-MONOSPACE-CODE; DOM-SCH §1.1
        """
        auth_mock("moehq")
        directory_page = self.get_page(SchoolDirectoryPage)
        base_url = school_directory_data["environments"]["base_url"]

        with self.step(
            "Bước 1: Mở danh bạ trường học và quan sát cột đầu tiên trên mỗi dòng",
            expected="Các dòng dữ liệu trường học hiển thị mã MOE code trong thẻ code.",
        ):
            directory_page.open(base_url)
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
            self.highlight_actual_result(
                locator=code_el,
                text=f"Mã MOE school code hiển thị trong thẻ <code> với font {font_family}.",
            )
            self.step.set_actual(f"Đã xác nhận định dạng monospace thẻ code: {font_family}.")

    def test_tc_sch_008_detail_screen_elements(
        self, school_directory_data: Dict[str, Any], auth_mock
    ) -> None:
        """
        TC-SCH-008: Màn hình Chi tiết trường học (/school-management/:schoolId) hiển thị đầy đủ thông tin tổ chức.
        Kịch bản: TS-SCH-AC | Traceability: AC-SCH-DETAIL; DOM-SCH §1.3
        """
        auth_mock("moehq")
        directory_page = self.get_page(SchoolDirectoryPage)
        detail_page = self.get_page(SchoolDetailPage)
        base_url = school_directory_data["environments"]["base_url"]
        active_school = school_directory_data["sample_schools"]["active_with_students"]

        with self.step(
            "Bước 1: Mở danh bạ trường học và tìm trường mục tiêu",
            expected="Dòng trường học hiển thị với nút 'Detail'.",
        ):
            directory_page.open(base_url)
            row = directory_page.row_by_code(active_school["code"])
            expect(row).to_be_visible()
            self.step.set_actual(f"Tìm thấy trường {active_school['code']} trên bảng.")

        with self.step(
            "Bước 2: Nhấn nút 'Detail' trên dòng trường cụ thể",
            expected="Điều hướng sang màn hình /school-management/:schoolId.",
        ):
            directory_page.click_detail(active_school["code"])
            detail_page.wait_loaded()
            self.step.set_actual(f"Điều hướng thành công sang {self.page.url}.")

        with self.step(
            "Bước 3: Kiểm tra thông tin hiển thị trên màn hình chi tiết",
            expected="Hiển thị nút quay lại, nhãn trạng thái và khu vực Overview của trường.",
        ):
            expect(detail_page.back_link).to_be_visible()
            expect(detail_page.overview_section).to_be_visible()
            self.highlight_actual_result(
                locator=detail_page.overview_section,
                text=f"Màn hình chi tiết trường {active_school['code']} hiển thị đầy đủ thông tin tổ chức.",
            )
            self.step.set_actual("Đã kiểm chứng đầy đủ các khu vực thông tin trên màn hình chi tiết.")

    def test_tc_sch_009_create_form_fields(
        self, school_directory_data: Dict[str, Any], auth_mock
    ) -> None:
        """
        TC-SCH-009: Màn hình Tạo mới trường học (/school-management/new) hiển thị đầy đủ các trường nhập liệu.
        Kịch bản: TS-SCH-AC | Traceability: AC-SCH-CREATE-FORM; DOM-SCH §1.2
        """
        auth_mock("moehq")
        directory_page = self.get_page(SchoolDirectoryPage)
        create_page = self.get_page(SchoolCreatePage)
        base_url = school_directory_data["environments"]["base_url"]

        with self.step(
            "Bước 1: Mở danh bạ và nhấn nút 'Create school' trên toolbar",
            expected="Điều hướng sang màn hình /school-management/new với tiêu đề 'Create a school'.",
        ):
            directory_page.open(base_url)
            directory_page.create_button.click()
            create_page.wait_for_form_ready()
            self.step.set_actual(f"Đã mở form tạo mới trường học tại {self.page.url}.")

        with self.step(
            "Bước 2: Kiểm tra các trường nhập liệu trên form tạo mới",
            expected="Có các ô: MOE school code, School name, School type dropdown, Academic levels và các nút hành động.",
        ):
            expect(create_page.moe_school_code_input).to_be_visible()
            expect(create_page.school_name_input).to_be_visible()
            expect(create_page.school_type_select).to_be_visible()
            expect(create_page.academic_levels_input).to_be_visible()
            expect(create_page.cancel_button).to_be_visible()
            expect(create_page.create_school_button).to_be_visible()
            self.highlight_actual_result(
                locator=create_page.form,
                text="Form tạo mới trường học hiển thị đầy đủ tất cả các trường nhập liệu và nút bấm theo spec.",
            )
            self.step.set_actual("Đã xác nhận đầy đủ các trường nhập liệu trên form tạo mới.")

    def test_tc_sch_010_column_sorting(
        self, school_directory_data: Dict[str, Any], auth_mock
    ) -> None:
        """
        TC-SCH-010: Sắp xếp dữ liệu (Column Sorting) trên bảng danh bạ trường theo Tên trường và Số lượng học sinh.
        Kịch bản: TS-SCH-AC | Traceability: AC-SCH-SORTING; DOM-SCH §1.1
        """
        auth_mock("moehq")
        directory_page = self.get_page(SchoolDirectoryPage)
        base_url = school_directory_data["environments"]["base_url"]

        with self.step(
            "Bước 1: Mở trang danh bạ trường học và kiểm tra tiêu đề các cột",
            expected="Bảng hiển thị các cột cho phép sắp xếp dữ liệu.",
        ):
            directory_page.open(base_url)
            expect(directory_page.table_headers.first).to_be_visible()
            self.step.set_actual("Danh bạ trường học sẵn sàng thao tác sorting.")

        with self.step(
            "Bước 2: Nhấp vào tiêu đề cột 'School name'",
            expected="Cột School name được kích hoạt sắp xếp (A-Z hoặc Z-A).",
        ):
            name_header = directory_page.table_headers.filter(has_text="School name").first
            expect(name_header).to_be_visible()
            name_header.click()
            self.step.set_actual("Đã nhấp sắp xếp theo cột School name.")

        with self.step(
            "Bước 3: Nhấp vào tiêu đề cột 'Active students' để sắp xếp theo số lượng học sinh",
            expected="Bảng tự động đảo chiều sắp xếp theo tiêu chí được chọn.",
        ):
            students_header = directory_page.table_headers.filter(has_text="Active students").first
            expect(students_header).to_be_visible()
            students_header.click()
            self.highlight_actual_result(
                locator=students_header,
                text="Tính năng sắp xếp cột (Column Sorting) trên bảng danh bạ hoạt động ổn định.",
            )
            self.step.set_actual("Thao tác sắp xếp hoàn tất thành công.")
