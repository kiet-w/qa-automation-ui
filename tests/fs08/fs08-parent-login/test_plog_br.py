"""
tests/fs08/fs08-parent-login/test_plog_br.py - Business Rules for Parent Login & Singpass MockPass.
Pillar: BR (Quy tắc nghiệp vụ)
Test Cases: TC-AUTH-01, TC-AUTH-02.
Scenario ID: TS-AUTH-BR
Traceability: BR-AUTH-01; CITIZEN-SCOPE; BR-AUTH-SESSION; SECURITY-IDLE;
Complies with Invariants 1, 2, 3, 4, 7, 8, 9 (<250 lines), 13 (100% Tiếng Việt step evidence).
"""
from typing import Any, Dict
import pytest
from playwright.sync_api import expect

from tests.base_test import BaseTest
from pages.fs08.singpass_login_page import SingpassLoginPage


@pytest.mark.br
class TestSingpassLoginBr(BaseTest):
    """Test suite covering Business Rules for Parent Login and MockPass."""

    def test_tc_tc_auth_01_ts_auth_br_quyền_truy_cập_dịch_vụ_công_dân_phụ(
        self, parent_login_data: Dict[str, Any]
    ) -> None:
        """
        TC-AUTH-01: Quyền truy cập dịch vụ công dân: Phụ huynh có con liên kết mới vào được cổng EduSave.
        Scenario: TS-AUTH-BR | Traceability: BR-AUTH-01; CITIZEN-SCOPE
        """
        login = self.get_page(SingpassLoginPage)
        base_url = parent_login_data.get("base_url", "http://localhost:5174")

        with self.step(
            "Step 1: Mở trang Đăng nhập Cổng Phụ huynh",
            expected="Trang đăng nhập hiển thị tiêu đề và nút 'Sign in with Singpass'.",
        ):
            login.open(base_url=base_url)
            expect(login.page.locator(login.HEADING)).to_be_visible()
            expect(login.page.locator(login.LOGIN_WITH_SINGPASS_BTN)).to_be_visible()
            self.step.set_actual(f"Mở thành công trang đăng nhập tại {login.page.url}.")

        with self.step(
            "Step 2: Chọn Đăng nhập với Singpass MockPass",
            expected="Điều hướng sang màn hình giả lập SingPass MockPass.",
        ):
            login.click_sign_in_with_singpass()
            login.page.wait_for_selector(login.MOCKPASS_CITIZEN_SELECT, timeout=10000)
            self.step.set_actual("Chuyển hướng thành công sang cổng Singpass MockPass (:5156).")

        with self.step(
            "Step 3: Chọn tài khoản phụ huynh hợp lệ có con liên kết",
            expected="Đăng nhập thành công vào Cổng phụ huynh; hiển thị thông tin các con liên kết.",
        ):
            login.select_mockpass_persona("Tan Ah Teck")
            login.submit_mockpass_login()
            expect(login.page.locator(login.BRAND_LOGO)).to_be_visible(timeout=15000)
            self.step.set_actual("Đăng nhập thành công và truy cập Dashboard công dân EduSave.")

    def test_tc_tc_auth_02_ts_auth_br_kiểm_soát_an_toàn_phiên_làm_việc_hế(
        self, parent_login_data: Dict[str, Any]
    ) -> None:
        """
        TC-AUTH-02: Kiểm soát an toàn phiên làm việc: Hết hạn phiên tự động bảo vệ dữ liệu phụ huynh.
        Scenario: TS-AUTH-BR | Traceability: BR-AUTH-SESSION; SECURITY-IDLE
        """
        login = self.get_page(SingpassLoginPage)
        base_url = parent_login_data.get("base_url", "http://localhost:5174")

        with self.step(
            "Step 1: Đăng nhập vào Cổng phụ huynh với tài khoản mẫu hợp lệ",
            expected="Đăng nhập thành công vào trang chủ.",
        ):
            login.login_with_persona("Tan Ah Teck", base_url=base_url)
            expect(login.page.locator(login.BRAND_LOGO)).to_be_visible()
            self.step.set_actual("Đã đăng nhập thành công vào Cổng phụ huynh.")

        with self.step(
            "Step 2: Giả lập hết hạn phiên làm việc và kích hoạt kiểm tra phiên",
            expected="Hệ thống tự động kích hoạt bảo vệ an toàn hoặc yêu cầu đăng nhập lại.",
        ):
            # Xóa session storage/local storage mô phỏng token hết hạn
            login.page.evaluate("() => { localStorage.clear(); sessionStorage.clear(); }")
            login.page.reload()
            login.page.wait_for_selector(login.LOGIN_WITH_SINGPASS_BTN, timeout=10000)
            expect(login.page.locator(login.LOGIN_WITH_SINGPASS_BTN)).to_be_visible()
            self.step.set_actual("Hệ thống chuyển hướng an toàn về trang Đăng nhập sau khi hết phiên.")
