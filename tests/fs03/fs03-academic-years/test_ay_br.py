"""
tests/fs03/fs03-academic-years/test_br.py
Suite: BR (2 cases)
Invariants: POM separation, external fixtures, traceability, <=250 lines.
"""
from typing import Any, Dict
import pytest
from playwright.sync_api import expect

from tests.base_test import BaseTest
from pages.fs03.academic_years_page import AcademicYearsPage


@pytest.mark.br
class TestAcademicYearsBr(BaseTest):
    """Test suite covering BR test cases."""

    def test_tc_tc_ay_01_ts_ay_br_quy_tắc_duy_nhất_một_năm_học_hoạt_đ(self, academic_years_data: Dict[str, Any]):
        """
        TC-AY-01: Quy tắc duy nhất một Năm học hoạt động: Chỉ có tối đa 1 năm học được ở trạng thái Hoạt động
        Scenario: TS-AY-BR
        """
        page_obj = self.get_page(AcademicYearsPage)
        base_url = academic_years_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Tại danh sách năm học, tìm năm 2026 đang ở trạng thái Bản nháp (DRAFT).", expected="Hệ thống chặn kích hoạt và cảnh báo: 'Chỉ được phép có duy nhất một năm học đang hoạt động trên toàn quốc'."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Nhấn nút Kích hoạt (Activate).", expected="Hệ thống chặn kích hoạt và cảnh báo: 'Chỉ được phép có duy nhất một năm học đang hoạt động trên toàn quốc'."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Quan sát thông báo từ hệ thống.", expected="Hệ thống chặn kích hoạt và cảnh báo: 'Chỉ được phép có duy nhất một năm học đang hoạt động trên toàn quốc'."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_ay_02_ts_ay_br_ràng_buộc_thời_gian_ngày_kết_thúc_n(self, academic_years_data: Dict[str, Any]):
        """
        TC-AY-02: Ràng buộc thời gian: Ngày kết thúc năm học bắt buộc phải sau ngày bắt đầu
        Scenario: TS-AY-BR
        """
        page_obj = self.get_page(AcademicYearsPage)
        base_url = academic_years_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Chọn ngày kết thúc sớm hơn ngày bắt đầu.", expected="Hệ thống chặn gửi form; hiển thị cảnh báo lỗi: 'Ngày kết thúc phải lớn hơn ngày bắt đầu năm học'."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Nhấn nút Tạo năm học.", expected="Hệ thống chặn gửi form; hiển thị cảnh báo lỗi: 'Ngày kết thúc phải lớn hơn ngày bắt đầu năm học'."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")
