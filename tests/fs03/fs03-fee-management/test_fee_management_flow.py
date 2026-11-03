"""
tests/fs03/fs03-fee-management/test_fee_management_flow.py
Bộ kiểm thử tự động quy trình Quản lý Thành phần Phí & Biểu phí qua 4 Màn hình (Playwright + Pytest).
Tuân thủ 4 Nguyên tắc Vàng (AGENTS.md):
- Page Object Model chuẩn (tách biệt thao tác và assertion).
- Strict Black-box Testing (dựa trên Live DOM và Đặc tả nghiệp vụ).
- Test cases rõ ràng bám sát BR, AC, Validation, Function Flow.
- Chụp ảnh minh chứng kết quả giao diện cho từng test case.
"""
import re
import time
from typing import Any, Dict
import pytest
from playwright.sync_api import expect, Page

from tests.base_test import BaseTest
from pages.fs03.fee_management_page import FeeManagementPage


@pytest.mark.flow
@pytest.mark.p1
class TestFeeManagementFlow(BaseTest):
    """Kiểm thử tự động quy trình Quản lý Phí qua 4 Màn hình cụ thể."""

    def test_tc_fee_001_entry_path_direct_url(
        self, auth_page: Page, fee_data: Dict[str, Any]
    ) -> None:
        """
        TC-FEE-001: Khởi động qua Cách 1 - Truy cập thẳng link /fee-management/components/new.
        Pillar: AC / Flow | Priority: P1
        """
        fee_page = FeeManagementPage(auth_page)
        base_url = fee_data["base_url"]

        with self.step(
            "Bước 1: Truy cập trực tiếp URL /fee-management/components/new",
            expected="Màn hình Wizard Bước 1 hiển thị đầy đủ form khai báo.",
        ):
            fee_page.open_new_component(base_url)
            expect(fee_page.step1_heading).to_be_visible()
            expect(fee_page.component_name_input).to_be_visible()
            expect(fee_page.fee_type_combobox).to_be_visible()
            expect(fee_page.student_categories_input).to_be_visible()
            expect(fee_page.education_stages_input).to_be_visible()
            expect(fee_page.tax_checkbox).to_be_visible()
            expect(fee_page.continue_to_rates_btn).to_be_visible()

    def test_tc_fee_002_entry_path_overview_view(
        self, auth_page: Page, fee_data: Dict[str, Any]
    ) -> None:
        """
        TC-FEE-002: Khởi động qua Cách 2 - Bấm nút View tại dòng School Tuition Fee -> Create fee component.
        Pillar: AC / Flow | Priority: P1
        """
        fee_page = FeeManagementPage(auth_page)
        base_url = fee_data["base_url"]

        with self.step(
            "Bước 1: Truy cập /fee-management và xem bảng danh mục loại phí",
            expected="Bảng Fee Types hiển thị các loại phí có sẵn.",
        ):
            fee_page.open_overview(base_url)
            expect(fee_page.overview_heading).to_be_visible()
            expect(fee_page.fee_types_table).to_be_visible()

        with self.step(
            "Bước 2: Bấm nút View tại dòng loại phí",
            expected="Điều hướng sang chi tiết loại phí.",
        ):
            fee_page.click_first_fee_type_view()

        with self.step(
            "Bước 3: Bấm nút Create fee component",
            expected="Điều hướng tới màn hình tạo thành phần phí (/components/new).",
        ):
            fee_page.click_create_fee_component()
            expect(fee_page.step1_heading).to_be_visible()
            expect(fee_page.component_name_input).to_be_visible()

    def test_tc_fee_003_e2e_mode_a_fixed_amount(
        self, auth_page: Page, fee_data: Dict[str, Any]
    ) -> None:
        """
        TC-FEE-003: Luồng Happy Path trọn vẹn qua 4 màn hình với Chế độ A (Fixed Amount) và chuyển sang Bước 5.
        Pillar: Function Flow & State Transition | Priority: P1
        """
        fee_page = FeeManagementPage(auth_page)
        base_url = fee_data["base_url"]
        cfg = fee_data["happy_path_mode_a"]
        unique_name = f"{cfg['name_prefix']} {int(time.time())}"

        # -------------------------------------------------------------
        # 📍 Màn 2: Wizard Bước 1 - Khai báo Thành phần Phí
        # -------------------------------------------------------------
        with self.step(
            "Màn 2: Khai báo Thành phần Phí tại /components/new",
            expected="Điền Name, Fee type, Categories, Stages, Tax applies và bấm Continue to rates.",
        ):
            fee_page.open_new_component(base_url)
            fee_page.fill_component_name(unique_name)
            fee_page.select_fee_type()
            fee_page.select_student_categories(cfg["categories"])
            fee_page.select_education_stages(cfg["stages"])
            fee_page.set_tax_applies(cfg["tax_applies"])
            fee_page.click_continue_to_rates()

        # -------------------------------------------------------------
        # 📍 Màn 3: Wizard Bước 2 - Thiết lập Biểu phí & Thời hạn
        # -------------------------------------------------------------
        with self.step(
            "Màn 3: Thiết lập Biểu phí Chế độ A (Fixed Amount) tại /rate-rules/new",
            expected="URL chuyển sang /rate-rules/new; điền Amount 100.00 SGD và ngày hiệu lực.",
        ):
            expect(auth_page).to_have_url(re.compile(r".*/rate-rules/new.*"), timeout=15000)
            fee_page.select_rate_mode(cfg["mode"])

            # Kiểm tra ô Currency SGD đã mặc định sẵn
            expect(fee_page.currency_input).to_have_value(cfg["currency"])

            fee_page.fill_fixed_amount(cfg["amount"])
            fee_page.fill_effective_dates(cfg["effective_from"], cfg["effective_to"])
            fee_page.click_save_rates()

        # -------------------------------------------------------------
        # 📍 Màn 4: Màn hình Chi tiết Thành phần Phí (/components/:id)
        # -------------------------------------------------------------
        with self.step(
            "Màn 4: Kiểm tra thông tin Thành phần Phí và Biểu phí đã cấu hình",
            expected="Component chuyển sang chi tiết; Bảng biểu phí hiển thị 100.00 SGD; xuất hiện nút Publish batch.",
        ):
            expect(auth_page).to_have_url(re.compile(r".*/fee-management/components/[^/]+$"), timeout=15000)
            expect(auth_page.locator(f"text={unique_name}").first).to_be_visible()
            expect(fee_page.publish_batch_btn.first).to_be_visible()
            expect(auth_page.locator("text=$100.00").first).to_be_visible()

        # -------------------------------------------------------------
        # 📍 Cầu nối sang Bước 5: Tạo Đợt Thu & Chốt Công Nợ
        # -------------------------------------------------------------
        with self.step(
            "Bước 5 Bridge: Bấm 'Publish batch from this Fee Component'",
            expected="Điều hướng sang /fee-batches/new?feeComponentId=...",
        ):
            fee_page.click_publish_batch()
            expect(auth_page).to_have_url(re.compile(r".*/fee-batches/new\?feeComponentId=.*"), timeout=15000)

    def test_tc_fee_010_step1_validation_empty_name(
        self, auth_page: Page, fee_data: Dict[str, Any]
    ) -> None:
        """
        TC-FEE-010: Kiểm tra validation Bước 1 khi để trống trường Name.
        Pillar: Validation | Priority: P2
        """
        fee_page = FeeManagementPage(auth_page)
        base_url = fee_data["base_url"]

        with self.step(
            "Bước 1: Để trống Name và bấm Continue to rates",
            expected="Hệ thống chặn submit, kích hoạt trạng thái không hợp lệ.",
        ):
            fee_page.open_new_component(base_url)
            fee_page.fill_component_name("")
            fee_page.click_continue_to_rates()

            is_invalid = fee_page.component_name_input.evaluate("el => el.getAttribute('aria-invalid') === 'true' || !el.checkValidity()")
            assert is_invalid
            assert "/components/new" in fee_page.get_current_url()

    def test_tc_fee_015_step2_validation_inverted_dates(
        self, auth_page: Page, fee_data: Dict[str, Any]
    ) -> None:
        """
        TC-FEE-015: Kiểm tra validation Bước 2 khi Effective From > Effective To.
        Pillar: Validation & BVA | Priority: P1
        """
        fee_page = FeeManagementPage(auth_page)
        base_url = fee_data["base_url"]
        unique_name = f"Date Validation {int(time.time())}"

        with self.step(
            "Bước 1: Tạo Component để chuyển sang Bước 2",
            expected="Đến màn hình cấu hình biểu phí.",
        ):
            fee_page.open_new_component(base_url)
            fee_page.fill_component_name(unique_name)
            fee_page.select_fee_type()
            fee_page.select_student_categories(["Singapore citizen"])
            fee_page.select_education_stages(["Primary"])
            fee_page.click_continue_to_rates()
            expect(auth_page).to_have_url(re.compile(r".*/rate-rules/new.*"), timeout=15000)

        with self.step(
            "Bước 2: Nhập ngày đảo ngược (From: 2026-12-31 > To: 2026-01-01) và bấm Save rates",
            expected="Bị chặn lại trên giao diện Bước 2; không chuyển hướng sang Màn 4.",
        ):
            fee_page.select_rate_mode("fixed-amount")
            fee_page.fill_fixed_amount("100.00")
            fee_page.fill_effective_dates("2026-12-31", "2026-01-01")
            fee_page.click_save_rates()

            # Kiểm tra vẫn ở lại trang cấu hình biểu phí, không lưu được DB
            assert "/rate-rules/new" in fee_page.get_current_url()
