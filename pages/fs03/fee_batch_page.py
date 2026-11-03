"""
pages/fs03/fee_batch_page.py - Page Object Model cho Quy trình Đợt Thu Phí & Xuất Bản Công Nợ (Fee Batches).
Tuân thủ tuyệt đối 4 Nguyên tắc Vàng (AGENTS.md):
- Tách biệt hoàn toàn hành động và assertion (KHÔNG chứa bất kỳ câu lệnh assert nào trong POM).
- Strict Black-box Testing (dựa trên Live DOM thực tế).
"""
import re
from typing import Dict, List, Optional
from playwright.sync_api import Locator, Page
from pages.base_page import BasePage


class FeeBatchPage(BasePage):
    """Page Object đại diện cho các màn hình Đợt Thu Phí (/fee-batches/new và /fee-batches/:batchId)."""

    def __init__(self, page: Page):
        super().__init__(page)

        # --- Màn hình Tạo Mới Đợt Phí (/fee-batches/new) ---
        self.heading = self.page.locator("h1:has-text('Create fee publication batch'), h1:has-text('Fee publication')")
        self.warning_banner = self.page.locator(
            "[role='alert'], [class*='alert'], [class*='warning'], div:has-text('Fee component is required')"
        )
        self.title_input = self.page.locator("#fee-publication-title")
        self.period_start_input = self.page.locator("#fee-publication-period-start")
        self.period_end_input = self.page.locator("#fee-publication-period-end")
        self.schedule_at_input = self.page.locator("#fee-publication-schedule-at")
        self.due_date_input = self.page.locator("#fee-publication-due-date")

        # Publication targets
        self.schools_all_radio = self.page.locator("input[type='radio'][value='all-schools'], input[name='schools'][value='all']")
        self.schools_specific_radio = self.page.locator(
            "input[type='radio'][value='specific-schools'], input[name='schools'][value='specific'], label:has-text('Specific schools')"
        )
        self.school_select = self.page.locator("#fee-publication-schools, select[name='schools'], select[id*='school']")
        self.students_all_radio = self.page.locator(
            "input[type='radio'][value='all-students'], input[name='students'][value='all'], label:has-text('All eligible students')"
        )
        self.students_specific_radio = self.page.locator(
            "input[type='radio'][value='specific-students'], input[name='students'][value='specific'], label:has-text('Specific students')"
        )
        self.create_draft_btn = self.page.locator(
            'button[type="submit"]:has-text("Create draft"), button:has-text("Create draft")'
        )

        # Inline validation errors
        self.title_error = self.page.locator("#fee-publication-title ~ p[class*='text-destructive'], #fee-publication-title ~ p[class*='error']")
        self.period_end_error = self.page.locator("#fee-publication-period-end ~ p[class*='text-destructive'], #fee-publication-period-end ~ p[class*='error']")
        self.due_date_error = self.page.locator("#fee-publication-due-date ~ p[class*='text-destructive'], #fee-publication-due-date ~ p[class*='error']")

        # --- Màn hình Chi tiết Đợt Phí (/fee-batches/:batchId) ---
        self.detail_heading = self.page.locator("main h1, main h2, [class*='title']").first
        self.batch_status_badge = self.page.locator("[class*='badge'], [data-status], span:has-text('Draft'), span:has-text('Published')").first
        self.publish_btn = self.page.locator(
            'button:has-text("Publish"), button:has-text("Xuất bản"), button[id*="publish"]'
        )
        self.confirm_publish_dialog = self.page.locator("div[role='dialog'], [class*='modal']")
        self.confirm_publish_btn = self.page.locator("div[role='dialog'] button:has-text('Publish'), button:has-text('Confirm')")

        # --- Mục Student Charge Preview ---
        self.preview_section = self.page.locator(
            "section:has-text('Student charge preview'), section:has-text('preview'), div:has-text('Student charge preview')"
        )
        self.preview_school_filter = self.page.locator(
            "select[name='preview-school'], #preview-school, select:has(option:has-text('Rosyth'))"
        )
        self.preview_search_input = self.page.locator(
            "input[placeholder*='Search student'], input[placeholder*='search'], input[type='search']"
        )
        self.preview_table = self.page.locator("table:has-text('Expected'), table:has-text('Student')")
        self.preview_disclaimer = self.page.locator("text='Amounts shown are estimates'")

    # -------------------------------------------------------------
    # 📍 Điều Hướng & Thao Tác (Actions)
    # -------------------------------------------------------------
    def open_new_batch(self, base_url: str, fee_component_id: Optional[str] = None) -> None:
        """Mở màn hình tạo mới đợt phí."""
        url = f"{base_url}/fee-batches/new"
        if fee_component_id:
            url += f"?feeComponentId={fee_component_id}"
        self.page.goto(url, wait_until="networkidle")

    def open_batch_detail(self, base_url: str, batch_id: str) -> None:
        """Mở trực tiếp màn hình chi tiết đợt phí."""
        self.page.goto(f"{base_url}/fee-batches/{batch_id}", wait_until="networkidle")

    def fill_batch_form(
        self,
        title: str,
        period_start: str,
        due_date: str,
        period_end: Optional[str] = None,
        schedule_at: Optional[str] = None,
        target_school: Optional[str] = None,
        target_students: str = "all",
    ) -> None:
        """Điền thông tin vào form tạo đợt phí."""
        if title is not None:
            self.title_input.fill(title)
        if period_start is not None:
            self.period_start_input.fill(period_start)
        if period_end is not None:
            self.period_end_input.fill(period_end)
        if due_date is not None:
            self.due_date_input.fill(due_date)
        if schedule_at is not None:
            self.schedule_at_input.fill(schedule_at)

        # Chọn trường mục tiêu nếu radio khả dụng
        if target_school and self.schools_specific_radio.count() > 0 and self.schools_specific_radio.is_visible():
            self.schools_specific_radio.click()
            if self.school_select.count() > 0:
                self.school_select.select_option(label=target_school)

        # Chọn học sinh mục tiêu
        if target_students == "all" and self.students_all_radio.count() > 0:
            self.students_all_radio.click()

    def click_create_draft(self) -> None:
        """Bấm nút Create draft."""
        self.create_draft_btn.click()

    def filter_student_preview(self, student_name: str, school_name: Optional[str] = None) -> None:
        """Tìm kiếm học sinh trong mục Preview."""
        if school_name and self.preview_school_filter.count() > 0 and self.preview_school_filter.is_visible():
            self.preview_school_filter.select_option(label=school_name)
        if self.preview_search_input.count() > 0 and self.preview_search_input.is_visible():
            self.preview_search_input.fill(student_name)
            self.page.wait_for_timeout(500)

    def click_publish_batch(self) -> None:
        """Bấm nút Publish trên thanh công cụ của Batch."""
        self.publish_btn.first.click()
        self.page.wait_for_timeout(1000)
        if self.confirm_publish_dialog.count() > 0 and self.confirm_publish_dialog.is_visible():
            if self.confirm_publish_btn.count() > 0:
                self.confirm_publish_btn.click()
                self.page.wait_for_load_state("networkidle")
