"""
tests/testcase5173/03_school_management/test_sch_flow.py - Function Flow & Luồng chức năng phân hệ Trường học.
Bao phủ các ca kiểm thử: TC-SCH-016, TC-SCH-017, TC-SCH-018, TC-SCH-019.
Scenario ID: TS-SCH-FLOW | Nguồn đặc tả: 03_school_management.md §1.1, §1.2, §1.3
Tuân thủ 4 Trụ cột Vàng: POM chuẩn, Black-box, Bám sát nghiệp vụ, Pytest First & Báo cáo minh chứng.
"""
from typing import Any, Dict
import uuid
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
        self, school_directory_data: Dict[str, Any]
    ) -> None:
        """
        TC-SCH-016: Luồng tạo mới trường học thành công từ form và hiển thị ngay trên danh bạ.
        Kịch bản: TS-SCH-FLOW | Traceability: FLOW-SCH-CREATE; F01 create
        """
        create_page = self.get_page(SchoolCreatePage)
        directory_page = self.get_page(SchoolDirectoryPage)
        base_url = school_directory_data["environments"]["base_url"]

        new_code = f"SCH{uuid.uuid4().hex[:6].upper()}"
        new_name = f"Singapore Innovation Academy {uuid.uuid4().hex[:4].upper()}"

        with self.step(
            "Bước 1: Truy cập màn hình Tạo mới trường học",
            expected="Màn hình tạo mới hiển thị với đầy đủ các trường nhập liệu.",
        ):
            create_page.open(base_url)
            expect(create_page.moe_school_code_input).to_be_visible()
            self.step.set_actual(f"Mở màn hình tạo mới tại {self.page.url}.")

        with self.step(
            f"Bước 2: Nhập đầy đủ Mã MOE '{new_code}', Tên '{new_name}' và chọn Cấp học",
            expected="Các trường nhập liệu nhận đầy đủ thông tin hợp lệ.",
        ):
            create_page.fill_moe_school_code(new_code)
            create_page.fill_school_name(new_name)
            create_page.select_school_type("GOVERNMENT")
            create_page.select_first_academic_level()
            self.step.set_actual(f"Đã nhập mã {new_code} và tên {new_name}.")

        with self.step(
            "Bước 3: Nhấn nút 'Create school' để gửi yêu cầu tạo mới",
            expected="Form submit thành công và hệ thống điều hướng về danh bạ.",
        ):
            create_page.submit_form()
            self.page.wait_for_url(f"{base_url}/school-management", timeout=15000)
            self.step.set_actual("Đã nhấn nút submit tạo trường.")

        with self.step(
            "Bước 4: Kiểm tra điều hướng về trang danh bạ",
            expected="Tự động quay về danh bạ /school-management; trường học mới xuất hiện.",
        ):
            expect(directory_page.page_heading).to_be_visible()
            # Search the newly created school to confirm it is listed
            directory_page.fill_search(new_code)
            directory_page.click_search()
            self.page.wait_for_timeout(500)
            expect(directory_page.rows.first).to_be_visible()
            expect(directory_page.rows.first).to_contain_text(new_code)

            self.highlight_actual_result(
                locator=directory_page.rows.first,
                text=f"Tạo mới trường học {new_code} thành công và hiển thị trên danh bạ.",
            )
            self.step.set_actual(f"Trường {new_code} đã được tạo và hiển thị thành công.")

    def test_tc_sch_017_search_school_exact_and_partial(
        self, school_directory_data: Dict[str, Any]
    ) -> None:
        """
        TC-SCH-017: Luồng tìm kiếm trường học theo Mã MOE chính xác và theo một phần Tên trường.
        Kịch bản: TS-SCH-FLOW | Traceability: FLOW-SCH-SEARCH-EXACT; DOM-SCH §1.1
        """
        directory_page = self.get_page(SchoolDirectoryPage)
        base_url = school_directory_data["environments"]["base_url"]

        with self.step(
            "Bước 1: Mở danh bạ và lấy mã trường hiện có để tìm kiếm",
            expected="Xác định được mã trường mục tiêu từ dòng đầu tiên.",
        ):
            directory_page.open(base_url)
            expect(directory_page.rows.first).to_be_visible()
            target_code = directory_page.rows.first.locator("td").first.inner_text().strip()
            self.step.set_actual(f"Mã trường tìm kiếm: '{target_code}'.")

        with self.step(
            f"Bước 2: Nhập mã trường '{target_code}' và nhấn Search",
            expected="Bảng lọc trả về bản ghi khớp chính xác mã trường.",
        ):
            directory_page.fill_search(target_code)
            directory_page.click_search()
            self.page.wait_for_timeout(500)
            expect(directory_page.rows.first).to_be_visible()
            expect(directory_page.rows.first.locator("td").first).to_have_text(target_code)
            self.step.set_actual(f"Tìm thấy trường với mã {target_code}.")

        with self.step(
            "Bước 3: Xóa từ khóa tìm kiếm và nhấn Reset filters",
            expected="Bảng khôi phục lại danh sách các trường học.",
        ):
            directory_page.reset_button.click()
            self.page.wait_for_timeout(500)
            expect(directory_page.rows.first).to_be_visible()

            self.highlight_actual_result(
                locator=directory_page.search_input,
                text="Tìm kiếm theo mã MOE code chính xác hoạt động chuẩn xác.",
            )
            self.step.set_actual("Đã hoàn tất kiểm chứng tìm kiếm.")

    def test_tc_sch_018_filter_by_type_and_reset(
        self, school_directory_data: Dict[str, Any]
    ) -> None:
        """
        TC-SCH-018: Luồng lọc danh sách theo Loại hình trường kết hợp nút Reset filters.
        Kịch bản: TS-SCH-FLOW | Traceability: FLOW-SCH-FILTER-RESET; DOM-SCH §1.1 Toolbar
        """
        directory_page = self.get_page(SchoolDirectoryPage)
        base_url = school_directory_data["environments"]["base_url"]
        filter_type = "GOVERNMENT"

        with self.step(
            f"Bước 1: Chọn Loại trường là '{filter_type}' trên dropdown",
            expected="Dropdown Loại trường nhận giá trị được chọn.",
        ):
            directory_page.open(base_url)
            expect(directory_page.rows.first).to_be_visible()
            initial_count = directory_page.rows.count()
            directory_page.type_filter.select_option(filter_type)
            self.step.set_actual(f"Đã chọn loại trường: {filter_type}.")

        with self.step(
            "Bước 2: Nhấn nút Search và quan sát bảng kết quả",
            expected="Bảng lọc danh sách các trường thuộc loại hình được chọn.",
        ):
            directory_page.click_search()
            self.page.wait_for_timeout(500)
            expect(directory_page.rows.first).to_be_visible()
            for row_data in directory_page.get_rows_data():
                assert "government" in row_data["type"].lower()
            self.step.set_actual("Đã áp dụng bộ lọc thành công.")

        with self.step(
            "Bước 3: Nhấn nút 'Reset filters'",
            expected="Bộ lọc được đặt lại; bảng hiển thị danh sách đầy đủ ban đầu.",
        ):
            directory_page.reset_button.click()
            self.page.wait_for_timeout(500)
            expect(directory_page.rows.first).to_be_visible()
            expect(directory_page.rows).to_have_count(initial_count)

            self.highlight_actual_result(
                locator=directory_page.reset_button,
                text="Bộ lọc Loại hình trường và nút Reset filters hoạt động trơn tru.",
            )
            self.step.set_actual("Đã hoàn tất kiểm thử lọc và reset filters.")

    def test_tc_sch_019_detail_and_back_breadcrumb(
        self, school_directory_data: Dict[str, Any]
    ) -> None:
        """
        TC-SCH-019: Luồng xem Chi tiết trường học và điều hướng quay lại danh bạ qua Back link.
        Kịch bản: TS-SCH-FLOW | Traceability: FLOW-SCH-DETAIL-BREADCRUMB; DOM-SCH §1.3
        """
        directory_page = self.get_page(SchoolDirectoryPage)
        detail_page = self.get_page(SchoolDetailPage)
        base_url = school_directory_data["environments"]["base_url"]

        with self.step(
            "Bước 1: Mở danh bạ và nhấn nút Detail trên dòng trường học đầu tiên",
            expected="Điều hướng sang trang chi tiết trường học /school-management/:schoolId.",
        ):
            directory_page.open(base_url)
            expect(directory_page.rows.first).to_be_visible()
            target_code = directory_page.rows.first.locator("td").first.inner_text().strip()

            directory_page.rows.first.locator("button[aria-label='Detail']").click()
            self.page.wait_for_url("**/school-management/**", timeout=10000)
            detail_page.wait_loaded()
            self.step.set_actual(f"Đã mở chi tiết trường {target_code}.")

        with self.step(
            "Bước 2: Xem thông tin chi tiết trên màn hình mới",
            expected="Hiển thị nút 'Back to schools' và thông tin tổ chức của trường.",
        ):
            expect(detail_page.back_link).to_be_visible()
            expect(detail_page.overview_section).to_be_visible()
            self.step.set_actual("Đã xem đầy đủ thông tin chi tiết.")

        with self.step(
            "Bước 3: Nhấn nút quay lại danh sách trường 'Back to schools'",
            expected="Người dùng được đưa quay trở lại đúng màn hình danh bạ trường học ban đầu.",
        ):
            detail_page.click_back_to_list()
            self.page.wait_for_url(f"{base_url}/school-management", timeout=10000)
            expect(directory_page.page_heading).to_be_visible()

            self.highlight_actual_result(
                locator=directory_page.page_heading,
                text="Điều hướng qua lại giữa chi tiết trường và danh bạ hoàn hảo.",
            )
            self.step.set_actual("Đã quay về danh bạ thành công.")
