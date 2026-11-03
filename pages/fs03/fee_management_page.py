"""
pages/fs03/fee_management_page.py - Page Object Model cho Quy trình Quản lý Phí & Biểu phí qua 4 màn hình.
Tuân thủ tuyệt đối Nguyên tắc Vàng: KHÔNG CHỨA BẤT KỲ CÂU LỆNH ASSERT NÀO.
Khảo sát và đối chiếu trực tiếp từ Live DOM (:5173).
"""
from typing import List, Optional, Dict
from playwright.sync_api import Locator, Page
from pages.base_page import BasePage


class FeeManagementPage(BasePage):
    """Page Object đại diện cho cụm tính năng Fee Management (4 Màn hình)."""

    def __init__(self, page: Page):
        super().__init__(page)

        # --- Màn 1: Overview (/fee-management) ---
        self.overview_heading = self.page.locator("h1:has-text('Fee management')")
        self.fee_types_table = self.page.locator("table")
        self.fee_type_view_btn = self.page.locator("tbody tr >> button:has-text('View')")
        self.create_fee_component_link = self.page.locator("button:has-text('Create fee component'), a:has-text('Create fee component')")

        # --- Màn 2: Wizard Bước 1 - Tạo Component (/fee-management/components/new) ---
        self.step1_heading = self.page.locator("h1:has-text('Create fee component')")
        self.component_name_input = self.page.locator("#fee-component-name")
        self.fee_type_combobox = self.page.locator("#fee-type")
        self.student_categories_input = self.page.locator("#fee-categories")
        self.education_stages_input = self.page.locator("#fee-stages")
        self.tax_checkbox = self.page.locator("#fee-tax")
        self.continue_to_rates_btn = self.page.locator('button[type="submit"]:has-text("Continue to rates")')
        self.name_inline_error = self.page.locator("#fee-component-name ~ p[class*='text-destructive'], #fee-component-name ~ p[class*='error'], p[id*='fee-component-name-error']")

        # --- Màn 3: Wizard Bước 2 - Thiết lập Biểu phí (/rate-rules/new) ---
        self.step2_heading = self.page.locator("h2:has-text('Rate configuration mode'), h1:has-text('Configure fee rates'), div:has-text('Rate configuration mode')")
        self.fixed_amount_radio = self.page.locator('input[type="radio"][value="fixed-amount"]')
        self.matrix_mode_radio = self.page.locator('input[type="radio"][value="config-fee-rate-rules"]')
        self.fixed_amount_input = self.page.locator("input#fixed-amount")
        self.currency_input = self.page.locator("input#fixed-currency")
        self.effective_from_input = self.page.locator("input#fixed-from")
        self.effective_to_input = self.page.locator("input#fixed-to")
        self.save_rates_btn = self.page.locator('button[type="submit"]:has-text("Save rates")')
        self.date_inline_error = self.page.locator("input#fixed-to ~ p[class*='text-destructive'], [role='alert']:has-text('date'), p[class*='error']")

        # --- Màn 4: Chi tiết Component (/components/:feeComponentId) ---
        self.detail_component_name = self.page.locator("main h2, main [class*='title'], h1")
        self.detail_component_code = self.page.locator("text=FC-")
        self.fee_rates_table = self.page.locator("table")
        self.publish_batch_btn = self.page.locator('button:has-text("Publish batch from this Fee Component"), a:has-text("Publish batch from this Fee Component")')
        self.toast_status = self.page.locator("[role='status']")

    # -------------------------------------------------------------
    # 📍 Điều Hướng (Navigation)
    # -------------------------------------------------------------
    def open_overview(self, base_url: str = "https://localhost:5173") -> None:
        """Truy cập Màn 1: Danh mục loại phí."""
        self.page.goto(f"{base_url}/fee-management", wait_until="networkidle")

    def open_new_component(self, base_url: str = "https://localhost:5173") -> None:
        """Truy cập Màn 2: Wizard Bước 1 Tạo Component mới."""
        self.page.goto(f"{base_url}/fee-management/components/new", wait_until="networkidle")

    def open_component_detail(self, base_url: str, component_id: str) -> None:
        """Truy cập Màn 4: Chi tiết Component."""
        self.page.goto(f"{base_url}/fee-management/components/{component_id}", wait_until="networkidle")

    # -------------------------------------------------------------
    # 📍 Thao Tác Màn 1: Khởi động tại /fee-management
    # -------------------------------------------------------------
    def click_first_fee_type_view(self) -> None:
        """Bấm nút View tại dòng đầu tiên trong bảng Fee Types."""
        self.fee_type_view_btn.first.click()
        self.page.wait_for_load_state("networkidle")

    def click_create_fee_component(self) -> None:
        """Bấm nút Create fee component."""
        self.create_fee_component_link.first.click()
        self.page.wait_for_load_state("networkidle")

    # -------------------------------------------------------------
    # 📍 Thao Tác Màn 2: Wizard Bước 1 (/components/new)
    # -------------------------------------------------------------
    def fill_component_name(self, name: str) -> None:
        """Điền tên khoản phí."""
        self.component_name_input.fill(name)

    def select_fee_type(self, fee_type_text: Optional[str] = None) -> None:
        """Chọn loại phí cha từ combobox."""
        self.fee_type_combobox.click()
        self.page.wait_for_timeout(300)
        if fee_type_text:
            opt = self.page.locator(f'[role="option"]:has-text("{fee_type_text}")').first
            if opt.is_visible():
                opt.click()
                return
        # Fallback chọn option đầu tiên nếu không truyền hoặc không khớp
        self.page.locator('[role="option"]').first.click()

    def select_student_categories(self, categories: List[str]) -> None:
        """Chọn danh sách nhóm học sinh áp dụng."""
        self.student_categories_input.click()
        self.page.wait_for_timeout(300)
        for cat in categories:
            opt = self.page.locator(f'[role="option"]:has-text("{cat}")').first
            if opt.is_visible():
                opt.click()
                self.page.wait_for_timeout(200)
        self.page.keyboard.press("Escape")

    def select_education_stages(self, stages: List[str]) -> None:
        """Chọn cấp bậc học áp dụng."""
        self.education_stages_input.click()
        self.page.wait_for_timeout(300)
        for stage in stages:
            opt = self.page.locator(f'[role="option"]:has-text("{stage}")').first
            if opt.is_visible():
                opt.click()
                self.page.wait_for_timeout(200)
        self.page.keyboard.press("Escape")

    def set_tax_applies(self, applies: bool) -> None:
        """Bật/tắt cờ áp dụng thuế GST/VAT."""
        if applies:
            self.tax_checkbox.check()
        else:
            self.tax_checkbox.uncheck()

    def click_continue_to_rates(self) -> None:
        """Bấm nút Continue to rates để hoàn tất Bước 1."""
        self.continue_to_rates_btn.click()
        self.page.wait_for_load_state("networkidle")

    # -------------------------------------------------------------
    # 📍 Thao Tác Màn 3: Wizard Bước 2 (/rate-rules/new)
    # -------------------------------------------------------------
    def select_rate_mode(self, mode: str = "fixed-amount") -> None:
        """Chọn chế độ áp giá: 'fixed-amount' hoặc 'config-fee-rate-rules'."""
        if mode == "fixed-amount":
            self.fixed_amount_radio.check()
        else:
            self.matrix_mode_radio.check()
        self.page.wait_for_timeout(300)

    def fill_fixed_amount(self, amount: str) -> None:
        """Điền số tiền mức phí cố định."""
        self.fixed_amount_input.fill(amount)

    def fill_effective_dates(self, from_date: str, to_date: str) -> None:
        """Điền khoảng thời gian hiệu lực của biểu giá."""
        self.effective_from_input.fill(from_date)
        self.effective_to_input.fill(to_date)

    def fill_matrix_rate(self, stage_code: str, category_code: str, amount: str) -> None:
        """Điền số tiền cho ô ma trận trong Chế độ B."""
        cell = self.page.locator(f"#rate-amount-{stage_code}:{category_code}, input[name*='{stage_code}'][name*='{category_code}']")
        if cell.is_visible():
            cell.fill(amount)

    def click_save_rates(self) -> None:
        """Bấm nút Save rates để lưu biểu phí."""
        self.save_rates_btn.click()
        self.page.wait_for_load_state("networkidle")

    # -------------------------------------------------------------
    # 📍 Thao Tác Màn 4 & Cầu Nối Bước 5
    # -------------------------------------------------------------
    def click_publish_batch(self) -> None:
        """Bấm nút 'Publish batch from this Fee Component'."""
        self.publish_batch_btn.first.click()
        self.page.wait_for_load_state("networkidle")

    # -------------------------------------------------------------
    # 📍 Đọc Trạng Thái UI (State Retrieval - KHÔNG ASSERT)
    # -------------------------------------------------------------
    def get_current_url(self) -> str:
        return self.page.url

    def is_step1_visible(self) -> bool:
        return self.component_name_input.is_visible()

    def is_step2_visible(self) -> bool:
        return self.fixed_amount_radio.is_visible() or self.matrix_mode_radio.is_visible()

    def is_publish_batch_visible(self) -> bool:
        return self.publish_batch_btn.first.is_visible()

    def get_currency_value(self) -> str:
        return self.currency_input.input_value()

    def is_currency_disabled(self) -> bool:
        return self.currency_input.is_disabled() or bool(self.currency_input.get_attribute("readonly"))

    def get_component_name_error(self) -> str:
        if self.name_inline_error.count() > 0 and self.name_inline_error.first.is_visible():
            return self.name_inline_error.first.inner_text().strip()
        return ""

    def is_component_name_invalid(self) -> bool:
        return self.component_name_input.get_attribute("aria-invalid") == "true"
