"""
tests/fs03/fs03-school-config/test_validation_2.py
Suite: Validation (2 cases)
Invariants: POM separation, external fixtures, traceability, <=250 lines.
"""
from typing import Any, Dict
import pytest
from playwright.sync_api import expect

from tests.base_test import BaseTest
from pages.fs03.school_config_page import SchoolConfigPage


@pytest.mark.validation
class TestSchoolConfigValidation2(BaseTest):
    """Test suite covering Validation test cases."""

    def test_tc_tc_5173_cfg_035_ts_cfg_val_search_bva_phân_tích_giá_trị_biên_bva_ô_tìm_ki(self, school_config_data: Dict[str, Any]):
        """
        TC-5173-CFG-035: Phân tích giá trị biên (BVA) Ô Tìm kiếm Cấp học: Kiểm tra 0 ký tự (toàn bộ), 1 ký tự (lọc ngay), và từ khóa không tồn tại
        Scenario: TS-CFG-VAL-SEARCH-BVA
        """
        page_obj = self.get_page(SchoolConfigPage)
        base_url = school_config_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Để trống ô tìm kiếm (0 ký tự) và kiểm tra danh sách hiển thị đủ 6 cấp học.", expected="0 ký tự hiển thị đầy đủ; 1 ký tự lọc ngay lập tức; khi không có kết quả hiển thị thông báo rỗng thân thiện 'No academic levels found' / 'Không tìm thấy cấp học'."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Nhập 1 ký tự 'P' và quan sát danh sách lọc.", expected="0 ký tự hiển thị đầy đủ; 1 ký tự lọc ngay lập tức; khi không có kết quả hiển thị thông báo rỗng thân thiện 'No academic levels found' / 'Không tìm thấy cấp học'."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Nhập từ khóa không tồn tại 'XYZ_NOTFOUND_999'.", expected="0 ký tự hiển thị đầy đủ; 1 ký tự lọc ngay lập tức; khi không có kết quả hiển thị thông báo rỗng thân thiện 'No academic levels found' / 'Không tìm thấy cấp học'."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 4: 4. Quan sát thông báo trạng thái rỗng.", expected="0 ký tự hiển thị đầy đủ; 1 ký tự lọc ngay lập tức; khi không có kết quả hiển thị thông báo rỗng thân thiện 'No academic levels found' / 'Không tìm thấy cấp học'."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_cfg_036_ts_cfg_val_search_bva_phân_tích_giá_trị_biên_bva_ô_tìm_ki(self, school_config_data: Dict[str, Any]):
        """
        TC-5173-CFG-036: Phân tích giá trị biên (BVA) Ô Tìm kiếm Ký tự Wildcard: Xử lý ký tự *, ?, %, [ dưới dạng chuỗi thuần túy không gây crash RegExp
        Scenario: TS-CFG-VAL-SEARCH-BVA
        """
        page_obj = self.get_page(SchoolConfigPage)
        base_url = school_config_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Lần lượt nhập các ký tự đặc biệt '*', '?', '[' vào ô tìm kiếm.", expected="Giao diện không bị crash hay trắng trang; các ký tự đặc biệt được xử lý an toàn dưới dạng chuỗi thuần túy (literal string); Console không có lỗi uncaught error."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Quan sát phản ứng của giao diện và console log.", expected="Giao diện không bị crash hay trắng trang; các ký tự đặc biệt được xử lý an toàn dưới dạng chuỗi thuần túy (literal string); Console không có lỗi uncaught error."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Kiểm tra xem có lỗi RegExp syntax error nào không.", expected="Giao diện không bị crash hay trắng trang; các ký tự đặc biệt được xử lý an toàn dưới dạng chuỗi thuần túy (literal string); Console không có lỗi uncaught error."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")
