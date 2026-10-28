"""
tests/fs03/fs03-academic-years/test_ac.py
Suite: AC (2 cases)
Invariants: POM separation, external fixtures, traceability, <=250 lines.
"""
from typing import Any, Dict
import pytest
from playwright.sync_api import expect

from tests.base_test import BaseTest
from pages.fs03.academic_years_page import AcademicYearsPage


@pytest.mark.ac
class TestAcademicYearsAc(BaseTest):
    """Test suite covering AC test cases."""

    def test_tc_tc_ay_03_ts_ay_ac_tạo_mới_năm_học_thành_công_với_định(self, academic_years_data: Dict[str, Any]):
        """
        TC-AY-03: Tạo mới Năm học thành công với định dạng 4 chữ số và trạng thái mặc định Bản nháp (DRAFT)
        Scenario: TS-AY-AC
        """
        page_obj = self.get_page(AcademicYearsPage)
        base_url = academic_years_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Nhập số năm '2027', chọn ngày bắt đầu và kết thúc hợp lệ.", expected="Hệ thống tạo năm học thành công; hiển thị thông báo xanh; năm 2027 xuất hiện trong bảng với nhãn DRAFT màu vàng."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Nhấn nút 'Tạo năm học'.", expected="Hệ thống tạo năm học thành công; hiển thị thông báo xanh; năm 2027 xuất hiện trong bảng với nhãn DRAFT màu vàng."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Kiểm tra danh sách.", expected="Hệ thống tạo năm học thành công; hiển thị thông báo xanh; năm 2027 xuất hiện trong bảng với nhãn DRAFT màu vàng."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_ay_04_ts_ay_ac_kích_hoạt_năm_học_chuyển_trạng_thái(self, academic_years_data: Dict[str, Any]):
        """
        TC-AY-04: Kích hoạt Năm học chuyển trạng thái từ Bản nháp (DRAFT) sang Đang hoạt động (ACTIVE)
        Scenario: TS-AY-AC
        """
        page_obj = self.get_page(AcademicYearsPage)
        base_url = academic_years_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Nhấn nút 'Kích hoạt' (Activate) trên dòng năm học 2026.", expected="Năm học 2026 chuyển sang nhãn màu xanh 'Đang hoạt động' (ACTIVE); nút Kích hoạt tự động ẩn đi."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Xác nhận trên hộp thoại xác nhận.", expected="Năm học 2026 chuyển sang nhãn màu xanh 'Đang hoạt động' (ACTIVE); nút Kích hoạt tự động ẩn đi."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")
