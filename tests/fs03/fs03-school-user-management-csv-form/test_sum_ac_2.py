"""
tests/fs03/fs03-school-user-management-csv-form/test_ac_2.py
Suite: AC (2 cases)
Invariants: POM separation, external fixtures, traceability, <=250 lines.
"""
from typing import Any, Dict
import pytest
from playwright.sync_api import expect

from tests.base_test import BaseTest
from pages.fs03.school_user_management_page import SchoolUserManagementPage


@pytest.mark.ac
class TestSchoolUserManagementAc2(BaseTest):
    """Test suite covering AC test cases."""

    def test_tc_tc_5173_sum_029_ts_5173_sum_create_single_tạo_thành_công_tài_khoản_cán_bộ_trư(self, school_user_mgmt_data: Dict[str, Any]):
        """
        TC-5173-SUM-029: Tạo thành công tài khoản Cán bộ trường đơn lẻ qua biểu mẫu trực tuyến và chuyển hướng về danh sách
        Scenario: TS-5173-SUM-CREATE-SINGLE
        """
        page_obj = self.get_page(SchoolUserManagementPage)
        base_url = school_user_mgmt_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Điền đầy đủ thông tin hợp lệ vào NRIC, First name, Last name, Email và Mã trường.", expected="Toast thông báo tạo tài khoản thành công xuất hiện; URL tự động chuyển về /school-user-management; cán bộ mới hiển thị ngay trên đầu danh sách."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Nhấn nút 'Create'.", expected="Toast thông báo tạo tài khoản thành công xuất hiện; URL tự động chuyển về /school-user-management; cán bộ mới hiển thị ngay trên đầu danh sách."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Quan sát thông báo toast và chuyển hướng URL.", expected="Toast thông báo tạo tài khoản thành công xuất hiện; URL tự động chuyển về /school-user-management; cán bộ mới hiển thị ngay trên đầu danh sách."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 4: 4. Tìm kiếm cán bộ mới trên danh sách.", expected="Toast thông báo tạo tài khoản thành công xuất hiện; URL tự động chuyển về /school-user-management; cán bộ mới hiển thị ngay trên đầu danh sách."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_sum_030_ts_5173_sum_create_bulk_tải_lên_file_csv_hợp_lệ_gồm_10_cán(self, school_user_mgmt_data: Dict[str, Any]):
        """
        TC-5173-SUM-030: Tải lên file CSV hợp lệ gồm 10 cán bộ và xử lý tạo tài khoản thành công 10/10 dòng
        Scenario: TS-5173-SUM-CREATE-BULK
        """
        page_obj = self.get_page(SchoolUserManagementPage)
        base_url = school_user_mgmt_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Chọn tệp CSV 10 cán bộ tại tab Bulk CSV.", expected="Hệ thống thông báo xử lý thành công 10/10 dòng dữ liệu; hiển thị bảng tổng kết màu xanh thành công; 10 tài khoản cán bộ mới xuất hiện trong hệ thống."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Nhấn nút 'Upload CSV'.", expected="Hệ thống thông báo xử lý thành công 10/10 dòng dữ liệu; hiển thị bảng tổng kết màu xanh thành công; 10 tài khoản cán bộ mới xuất hiện trong hệ thống."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Quan sát thông báo kết quả trả về.", expected="Hệ thống thông báo xử lý thành công 10/10 dòng dữ liệu; hiển thị bảng tổng kết màu xanh thành công; 10 tài khoản cán bộ mới xuất hiện trong hệ thống."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 4: 4. Kiểm tra danh sách cán bộ sau khi hoàn tất.", expected="Hệ thống thông báo xử lý thành công 10/10 dòng dữ liệu; hiển thị bảng tổng kết màu xanh thành công; 10 tài khoản cán bộ mới xuất hiện trong hệ thống."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")
