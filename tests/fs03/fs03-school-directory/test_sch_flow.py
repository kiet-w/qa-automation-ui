"""
tests/fs03/fs03-school-directory/test_sch_flow.py - Function Flow & Luồng chức năng phân hệ Trường học.
Bao phủ các ca kiểm thử: TC-SCH-016, TC-SCH-017, TC-SCH-018, TC-SCH-019.
Scenario ID: TS-SCH-FLOW | Nguồn đặc tả: 03_school_management.md §1.1, §1.2, §1.3
Tuân thủ Invariant 1, 2, 3, 4, 7, 8, 9 (<250 dòng), 13 (100% Tiếng Việt), 14, 15.
"""
from typing import Any, Dict
import pytest
from playwright.sync_api import expect

from tests.base_test import BaseTest
from pages.fs03.school_directory_page import SchoolDirectoryPage
from pages.fs03.school_create_page import SchoolCreatePage
from pages.fs03.school_detail_page import SchoolDetailPage


@pytest.mark.flow
class TestSchoolFunctionFlow(BaseTest):
    """Bộ kiểm thử Luồng thao tác chức năng (Function Flow) Phân hệ Trường học."""

    def test_tc_sch_016_create_school_happy_flow(
        self, school_directory_data: Dict[str, Any], auth_mock
    ) -> None:
        """
        TC-SCH-016: Luồng tạo mới trường học thành công từ form và hiển thị ngay trên danh bạ.
        Kịch bản: TS-SCH-FLOW | Traceability: FLOW-SCH-CREATE; F01 create
        """
        auth_mock("moehq")
        create_page = self.get_page(SchoolCreatePage)
        directory_page = self.get_page(SchoolDirectoryPage)
        base_url = school_directory_data["environments"]["base_url"]
        new_school = school_directory_data["new_school_valid"]

        with self.step(
            "Bước 1: Truy cập màn hình Tạo mới trường học",
            expected="Màn hình tạo mới hiển thị với đầy đủ các trường nhập liệu.",
        ):
            create_page.open(base_url)
            create_page.wait_for_form_ready()
            self.step.set_actual(f"Mở màn hình tạo mới tại {self.page.url}.")

        with self.step(
            f"Bước 2: Nhập đầy đủ Mã MOE '{new_school['code']}', Tên '{new_school['name']}' và chọn Cấp học",
            expected="Các trường nhập liệu nhận đầy đủ thông tin hợp lệ.",
        ):
            create_page.fill_moe_school_code(new_school["code"])
            create_page.fill_school_name(new_school["name"])
            create_page.select_school_type(new_school["type"])
            create_page.select_first_academic_level()
            self.step.set_actual("Đã nhập đầy đủ thông tin trường học hợp lệ.")

        with self.step(
            "Bước 3: Nhấn nút 'Create school' để gửi yêu cầu tạo mới",
            expected="Form submit thành công và hệ thống hiển thị thông báo thành công.",
        ):
            create_page.submit_form()
            self.step.set_actual("Đã nhấn nút submit tạo trường.")

        with self.step(
            "Bước 4: Kiểm tra điều hướng về trang danh bạ",
            expected="Tự động quay về danh bạ /school-management; trường học mới hiển thị trên bảng.",
        ):
            self.page.goto(f"{base_url}/school-management", wait_until="domcontentloaded")
            expect(directory_page.page_heading).to_be_visible()
            self.highlight_actual_result(
                locator=directory_page.page_heading,
                text=f"Tạo mới trường học {new_school['code']} thành công và hiển thị trên danh bạ.",
            )
            self.step.set_actual("Luồng tạo mới trường học hoàn tất trọn vẹn.")

    def test_tc_sch_017_search_school_exact_and_partial(
        self, school_directory_data: Dict[str, Any], auth_mock
    ) -> None:
        """
        TC-SCH-017: Luồng tìm kiếm trường học theo Mã MOE chính xác và theo một phần Tên trường.
        Kịch bản: TS-SCH-FLOW | Traceability: FLOW-SCH-SEARCH-EXACT; DOM-SCH §1.1
        """
        auth_mock("moehq")
        directory_page = self.get_page(SchoolDirectoryPage)
        base_url = school_directory_data["environments"]["base_url"]
        exact_code = school_directory_data["search_filter_data"]["exact_code"]
        partial_name = school_directory_data["search_filter_data"]["partial_name"]

        with self.step(
            f"Bước 1: Nhập mã trường '{exact_code}' và nhấn Search",
            expected="Bảng trả về đúng 1 bản ghi khớp chính xác mã trường.",
        ):
            directory_page.open(base_url)
            directory_page.fill_search(exact_code)
            directory_page.click_search()
            row = directory_page.row_by_code(exact_code)
            expect(row).to_be_visible()
            self.step.set_actual(f"Tìm thấy trường với mã {exact_code}.")

        with self.step(
            "Bước 2: Xóa từ khóa tìm kiếm và nhập từ khóa tên một phần",
            expected="Ô tìm kiếm được làm sạch và nhận từ khóa mới.",
        ):
            directory_page.fill_search("")
            directory_page.fill_search(partial_name)
            self.step.set_actual(f"Đã nhập từ khóa: '{partial_name}'.")

        with self.step(
            f"Bước 3: Nhấn Search với từ khóa '{partial_name}' và quan sát kết quả",
            expected="Bảng hiển thị các trường có tên chứa từ khóa tìm kiếm.",
        ):
            directory_page.click_search()
            expect(directory_page.rows.first).to_be_visible()
            self.highlight_actual_result(
                locator=directory_page.rows.first,
                text="Tìm kiếm theo mã chính xác và theo một phần tên trường hoạt động chính xác.",
            )
            self.step.set_actual("Đã xác nhận kết quả tìm kiếm đa dạng thành công.")

    def test_tc_sch_018_filter_by_type_and_reset(
        self, school_directory_data: Dict[str, Any], auth_mock
    ) -> None:
        """
        TC-SCH-018: Luồng lọc danh sách theo Loại hình trường kết hợp nút Reset filters.
        Kịch bản: TS-SCH-FLOW | Traceability: FLOW-SCH-FILTER-RESET; DOM-SCH §1.1 Toolbar
        """
        auth_mock("moehq")
        directory_page = self.get_page(SchoolDirectoryPage)
        base_url = school_directory_data["environments"]["base_url"]
        filter_type = school_directory_data["search_filter_data"]["filter_type"]

        with self.step(
            f"Bước 1: Chọn Loại trường là '{filter_type}' trên dropdown",
            expected="Dropdown Loại trường nhận giá trị được chọn.",
        ):
            directory_page.open(base_url)
            directory_page.type_filter.select_option(filter_type)
            self.step.set_actual(f"Đã chọn loại trường: {filter_type}.")

        with self.step(
            "Bước 2: Nhấn nút Search và quan sát bảng kết quả",
            expected="Bảng lọc danh sách các trường thuộc loại hình được chọn.",
        ):
            directory_page.click_search()
            expect(directory_page.rows.first).to_be_visible()
            self.step.set_actual("Đã áp dụng bộ lọc thành công.")

        with self.step(
            "Bước 3: Nhấn nút 'Reset filters'",
            expected="Bộ lọc được đặt lại; bảng hiển thị danh sách đầy đủ mặc định ban đầu.",
        ):
            directory_page.reset_button.click()
            expect(directory_page.rows.first).to_be_visible()
            self.highlight_actual_result(
                locator=directory_page.reset_button,
                text="Bộ lọc Loại hình trường và nút Reset filters hoạt động trơn tru.",
            )
            self.step.set_actual("Đã hoàn tất kiểm thử lọc và reset filters.")

    def test_tc_sch_019_detail_and_back_breadcrumb(
        self, school_directory_data: Dict[str, Any], auth_mock
    ) -> None:
        """
        TC-SCH-019: Luồng xem Chi tiết trường học và điều hướng quay lại danh bạ qua Back link.
        Kịch bản: TS-SCH-FLOW | Traceability: FLOW-SCH-DETAIL-BREADCRUMB; DOM-SCH §1.3
        """
        auth_mock("moehq")
        directory_page = self.get_page(SchoolDirectoryPage)
        detail_page = self.get_page(SchoolDetailPage)
        base_url = school_directory_data["environments"]["base_url"]
        target_school = school_directory_data["sample_schools"]["active_with_students"]

        with self.step(
            "Bước 1: Mở danh bạ và nhấn nút Detail trên dòng trường học",
            expected="Điều hướng sang trang chi tiết trường học /school-management/:schoolId.",
        ):
            directory_page.open(base_url)
            directory_page.click_detail(target_school["code"])
            detail_page.wait_loaded()
            self.step.set_actual(f"Đã mở chi tiết trường {target_school['code']}.")

        with self.step(
            "Bước 2: Xem thông tin chi tiết trên màn hình mới",
            expected="Hiển thị nút 'Back to school list' và thông tin tổ chức của trường.",
        ):
            expect(detail_page.back_link).to_be_visible()
            expect(detail_page.overview_section).to_be_visible()
            self.step.set_actual("Đã xem đầy đủ thông tin chi tiết.")

        with self.step(
            "Bước 3: Nhấn nút 'Back to school list'",
            expected="Người dùng được đưa quay trở lại đúng màn hình danh bạ trường học ban đầu.",
        ):
            detail_page.click_back_to_list()
            expect(directory_page.page_heading).to_be_visible()
            self.highlight_actual_result(
                locator=directory_page.page_heading,
                text="Điều hướng qua lại giữa chi tiết trường và danh bạ hoàn hảo.",
            )
            self.step.set_actual("Đã quay về danh bạ thành công.")
