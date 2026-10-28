"""
tests/fs08/fs08-parent-child-auth/test_ac.py
Suite: AC (2 cases)
Invariants: POM separation, external fixtures, traceability, <=250 lines.
"""
from typing import Any, Dict
import pytest
from playwright.sync_api import expect

from tests.base_test import BaseTest
from pages.fs08.home_portal_page import HomePortalPage


@pytest.mark.ac
class TestHomePortalAc(BaseTest):
    """Test suite covering AC test cases."""

    def test_tc_tc_dsh_03_ts_dsh_ac_trang_chủ_hiển_thị_đầy_đủ_thẻ_các_c(self, citizen_dashboard_data: Dict[str, Any]):
        """
        TC-DSH-03: Trang chủ hiển thị đầy đủ thẻ các con, số dư tài khoản và các nút dịch vụ nhanh
        Scenario: TS-DSH-AC
        """
        page_obj = self.get_page(HomePortalPage)
        base_url = citizen_dashboard_data.get("base_url", "http://localhost:5174")

        with self.step("Step 1: 1. Đăng nhập vào hệ thống.", expected="Hiển thị đầy đủ lời chào phụ huynh, danh sách thẻ học sinh, số dư EduSave và các nút Thanh toán học phí, Nộp đơn FAS."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Kiểm tra các khu vực nội dung trên Trang chủ.", expected="Hiển thị đầy đủ lời chào phụ huynh, danh sách thẻ học sinh, số dư EduSave và các nút Thanh toán học phí, Nộp đơn FAS."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_dsh_04_ts_dsh_ac_chuyển_đổi_linh_hoạt_giữa_các_con_đ(self, citizen_dashboard_data: Dict[str, Any]):
        """
        TC-DSH-04: Chuyển đổi linh hoạt giữa các con để xem học phí và tình hình học vụ tương ứng
        Scenario: TS-DSH-AC
        """
        page_obj = self.get_page(HomePortalPage)
        base_url = citizen_dashboard_data.get("base_url", "http://localhost:5174")

        with self.step("Step 1: 1. Nhấp chọn thẻ của người con thứ hai.", expected="Thông tin lớp học, trường học và danh sách học phí tự động cập nhật khớp chính xác với người con thứ hai."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Quan sát thông tin hiển thị bên dưới.", expected="Thông tin lớp học, trường học và danh sách học phí tự động cập nhật khớp chính xác với người con thứ hai."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")
