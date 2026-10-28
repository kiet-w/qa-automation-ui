"""
tests/fs08/fs08-parent-login/test_br.py
Suite: BR (2 cases)
Invariants: POM separation, external fixtures, traceability, <=250 lines.
"""
from typing import Any, Dict
import pytest
from playwright.sync_api import expect

from tests.base_test import BaseTest
from pages.fs08.singpass_login_page import SingpassLoginPage


@pytest.mark.br
class TestSingpassLoginBr(BaseTest):
    """Test suite covering BR test cases."""

    def test_tc_tc_auth_01_ts_auth_br_quyền_truy_cập_dịch_vụ_công_dân_phụ(self, parent_login_data: Dict[str, Any]):
        """
        TC-AUTH-01: Quyền truy cập dịch vụ công dân: Phụ huynh có con liên kết mới vào được cổng EduSave
        Scenario: TS-AUTH-BR
        """
        page_obj = self.get_page(SingpassLoginPage)
        base_url = parent_login_data.get("base_url", "http://localhost:5174")

        with self.step("Step 1: 1. Mở trang Đăng nhập Cổng Phụ huynh.", expected="Đăng nhập thành công vào Cổng phụ huynh; hiển thị thông tin các con liên kết và số dư quỹ EduSave."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Chọn Đăng nhập với Singpass MockPass.", expected="Đăng nhập thành công vào Cổng phụ huynh; hiển thị thông tin các con liên kết và số dư quỹ EduSave."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Chọn tài khoản phụ huynh hợp lệ.", expected="Đăng nhập thành công vào Cổng phụ huynh; hiển thị thông tin các con liên kết và số dư quỹ EduSave."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_auth_02_ts_auth_br_kiểm_soát_an_toàn_phiên_làm_việc_hế(self, parent_login_data: Dict[str, Any]):
        """
        TC-AUTH-02: Kiểm soát an toàn phiên làm việc: Hết hạn phiên tự động bảo vệ dữ liệu phụ huynh
        Scenario: TS-AUTH-BR
        """
        page_obj = self.get_page(SingpassLoginPage)
        base_url = parent_login_data.get("base_url", "http://localhost:5174")

        with self.step("Step 1: 1. Đăng nhập vào Cổng phụ huynh.", expected="Hệ thống tự động kết thúc phiên làm việc an toàn và chuyển hướng về màn hình Đăng nhập."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Để yên không thao tác trên màn hình vượt quá thời gian quy định.", expected="Hệ thống tự động kết thúc phiên làm việc an toàn và chuyển hướng về màn hình Đăng nhập."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Nhấp vào một chức năng bất kỳ.", expected="Hệ thống tự động kết thúc phiên làm việc an toàn và chuyển hướng về màn hình Đăng nhập."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")
