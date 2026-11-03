"""
tests/fs08/fs08-parent-login/test_plog_ac.py - Acceptance Criteria for Parent Login & Singpass MockPass.
Pillar: AC (Tiêu chí nghiệm thu chức năng)
Test Cases: TC-AUTH-03, TC-AUTH-04.
Scenario ID: TS-AUTH-AC
Traceability: AC-AUTH-01; DOM-LOGIN; AC-AUTH-SUCCESS; REDIRECT-HOME;
Complies with Invariants 1, 2, 3, 4, 7, 8, 9 (<250 lines), 13 (100% Tiếng Việt step evidence).
"""
from typing import Any, Dict
import pytest
from playwright.sync_api import expect

from tests.base_test import BaseTest
from pages.fs08.singpass_login_page import SingpassLoginPage


@pytest.mark.ac
class TestSingpassLoginAc(BaseTest):
    """Test suite covering Acceptance Criteria for Parent Login."""

    def test_tc_tc_auth_03_ts_auth_ac_hiển_thị_giao_diện_đăng_nhập_đầy_đủ(
        self, parent_login_data: Dict[str, Any]
    ) -> None:
        """
        TC-AUTH-03: Hiển thị giao diện Đăng nhập đầy đủ logo, tiêu đề và nút Đăng nhập Singpass MockPass.
        Scenario: TS-AUTH-AC | Traceability: AC-AUTH-01; DOM-LOGIN
        """
        login = self.get_page(SingpassLoginPage)
        base_url = parent_login_data.get("base_url", "http://localhost:5174")

        with self.step(
            "Step 1: Mở trình duyệt và truy cập trang Đăng nhập Phụ huynh",
            expected="Trang đăng nhập tải thành công và hiển thị khung nội dung chính.",
        ):
            login.open(base_url=base_url)
            expect(login.page.locator(login.LOGIN_CONTAINER)).to_be_visible()
            self.step.set_actual(f"Mở thành công URL {login.page.url}.")

        with self.step(
            "Step 2: Quan sát khung hiển thị và tiêu đề trang",
            expected="Tiêu đề 'Parent portal login' hiển thị rõ ràng; nút Đăng nhập Singpass sẵn sàng thao tác.",
        ):
            expect(login.page.locator(login.HEADING)).to_be_visible()
            expect(login.page.locator(login.LOGIN_WITH_SINGPASS_BTN)).to_be_visible()
            expect(login.page.locator(login.LOGIN_WITH_SINGPASS_BTN)).to_be_enabled()
            self.step.set_actual("Giao diện đăng nhập phụ huynh hiển thị đầy đủ và chuẩn xác.")

    def test_tc_tc_auth_04_ts_auth_ac_đăng_nhập_thành_công_với_tài_khoản(
        self, parent_login_data: Dict[str, Any]
    ) -> None:
        """
        TC-AUTH-04: Đăng nhập thành công với tài khoản mẫu Singpass chuyển hướng ngay vào Trang chủ.
        Scenario: TS-AUTH-AC | Traceability: AC-AUTH-SUCCESS; REDIRECT-HOME
        """
        login = self.get_page(SingpassLoginPage)
        base_url = parent_login_data.get("base_url", "http://localhost:5174")

        with self.step(
            "Step 1: Nhấp nút Đăng nhập với Singpass MockPass",
            expected="Chuyển hướng đến màn hình MockPass simulator.",
        ):
            login.open(base_url=base_url)
            login.click_sign_in_with_singpass()
            login.page.wait_for_selector(login.MOCKPASS_CITIZEN_SELECT, timeout=10000)
            self.step.set_actual("Chuyển hướng sang màn hình MockPass thành công.")

        with self.step(
            "Step 2: Chọn tài khoản phụ huynh Tan Ah Teck (S1234567A)",
            expected="Lựa chọn được danh tính phụ huynh Tan Ah Teck từ dropdown.",
        ):
            login.select_mockpass_persona("Tan Ah Teck")
            self.step.set_actual("Đã chọn nhân vật Tan Ah Teck trên danh sách.")

        with self.step(
            "Step 3: Nhấn Xác nhận đăng nhập và kiểm tra điều hướng",
            expected="Đăng nhập thành công; chuyển hướng mượt mà vào Trang chủ Cổng dịch vụ công dân EduSave.",
        ):
            login.submit_mockpass_login()
            expect(login.page.locator(login.BRAND_LOGO)).to_be_visible(timeout=15000)
            self.step.set_actual(f"Chuyển hướng thành công vào Trang chủ tại {login.page.url}.")
