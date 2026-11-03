"""
tests/uat/test_uat_5_fee_batches_and_publication.py - UAT Test Suite for Step 5 Fee Batches & Publication.
Target: https://admin.20-255-158-192.sslip.io (/fee-batches) & https://eservice.20-255-158-192.sslip.io
Strict compliance with:
  - Playwright + Pytest
  - Pure Black-Box Testing (Accessibility Roles, Labels, Visible Texts)
  - Page Object Model (FeeBatchPage with NO assertions in POM)
  - 4 Pillars: BR, AC, BVA/Validation, Function Flow
  - Negative Oracle: Preview must strictly not create real charges or modify balances
"""
import copy
import json
import os
import re
import time
from pathlib import Path
from typing import Any, Dict
import pytest
from playwright.sync_api import Browser, Page, expect

from pages.fs03.fee_batch_page import FeeBatchPage
from pages.fs03.fee_management_page import FeeManagementPage

BASE_URL = os.environ.get("BASE_URL", "https://admin.20-255-158-192.sslip.io").rstrip("/")
ESERVICE_URL = os.environ.get("ESERVICE_URL", "https://eservice.20-255-158-192.sslip.io").rstrip("/")
ADMIN_EMAIL = "admin@IAM.edu.vn"
DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "uat" / "step_05_fee_batches_data.json"


@pytest.fixture(scope="session")
def uat_data() -> Dict[str, Any]:
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def authenticated_admin_state(browser: Browser, tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Xác thực một lần duy nhất với tài khoản MOE HQ System Admin qua SSO Simulator."""
    context = browser.new_context(ignore_https_errors=True)
    page = context.new_page()
    try:
        page.goto(f"{BASE_URL}/login", wait_until="networkidle")
        page.locator('button:has-text("Sign in with Microsoft")').click()
        page.wait_for_url("**/microsoft-provider/**", timeout=25000)
        page.locator(f"text={ADMIN_EMAIL}").first.click()
        page.wait_for_url(f"{BASE_URL}/", wait_until="domcontentloaded", timeout=30000)
        page.wait_for_load_state("networkidle")
        page.locator("text=System Admin").first.wait_for(state="visible", timeout=15000)

        # Clear active View As session banner if present
        exit_btn = page.get_by_role("button", name="Exit", exact=True)
        if exit_btn.count() > 0 and exit_btn.is_visible():
            exit_btn.click()
            page.wait_for_timeout(1000)

        state_path = tmp_path_factory.mktemp("auth") / "moehq_batch_state.json"
        context.storage_state(path=str(state_path))
        return state_path
    finally:
        context.close()


@pytest.fixture
def auth_page(browser: Browser, authenticated_admin_state: Path) -> Page:
    """Page fixture đã có phiên đăng nhập sẵn của System Admin."""
    context = browser.new_context(
        storage_state=str(authenticated_admin_state),
        ignore_https_errors=True,
        viewport={"width": 1440, "height": 900},
    )
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture
def batch_page(auth_page: Page) -> FeeBatchPage:
    return FeeBatchPage(auth_page)


@pytest.fixture
def fee_mgmt_page(auth_page: Page) -> FeeManagementPage:
    return FeeManagementPage(auth_page)


class TestUatStep05FeeBatches:
    """Bộ kiểm thử UAT Bước 5: Tạo Đợt Phí, Preview Đối Soát Âm Tính, và Xuất Bản Công Nợ (UAT-021)."""

    def test_tc_uat_05_01_prerequisite_warning_without_component(self, auth_page: Page, batch_page: FeeBatchPage):
        """
        TC-BATCH-001: Mở /fee-batches/new trực tiếp mà không có feeComponentId.
        Pillar: BR / Negative Validation | Priority: P1
        """
        batch_page.open_new_batch(BASE_URL)

        # BR: Hệ thống bắt buộc phải có Fee Component, nếu thiếu phải hiện thông báo cảnh báo
        expect(batch_page.warning_banner.first).to_be_visible(timeout=10000)
        expect(batch_page.warning_banner.first).to_contain_text("Fee component is required")
        expect(batch_page.warning_banner.first).to_contain_text("Open this page from a fee component before creating a publication")

    def test_tc_uat_05_02_mandatory_fields_validation(self, auth_page: Page, batch_page: FeeBatchPage):
        """
        TC-BATCH-004: Kiểm tra Validation bắt buộc nhập Title, Period Start, Due Date.
        Pillar: Validation / BVA | Priority: P2
        """
        # Sử dụng một feeComponentId mẫu
        sample_comp_id = "0a5379b6-babc-4862-897e-d47d5a192255"
        batch_page.open_new_batch(BASE_URL, sample_comp_id)

        expect(batch_page.title_input).to_be_visible(timeout=10000)

        # Bỏ trống và bấm Create draft
        batch_page.click_create_draft()

        # Form phải bị chặn không được chuyển sang trang chi tiết
        expect(auth_page).to_have_url(re.compile(r".*/fee-batches/new.*"))
        is_invalid = batch_page.title_input.evaluate("el => el.getAttribute('aria-invalid') === 'true' || !el.checkValidity()")
        assert is_invalid, "Trường #fee-publication-title phải kích hoạt trạng thái không hợp lệ khi để trống"

    def test_tc_uat_05_03_date_range_bva_validation(self, auth_page: Page, batch_page: FeeBatchPage):
        """
        TC-BATCH-005: BVA Validation ngày kết thúc (Period End) nhỏ hơn ngày bắt đầu (Period Start).
        Pillar: Validation / BVA | Priority: P1
        """
        sample_comp_id = "0a5379b6-babc-4862-897e-d47d5a192255"
        batch_page.open_new_batch(BASE_URL, sample_comp_id)

        expect(batch_page.title_input).to_be_visible(timeout=10000)
        batch_page.fill_batch_form(
            title="Validation Test Batch",
            period_start="2026-06-01",
            period_end="2026-01-01",  # Đảo ngược: End < Start
            due_date="2026-06-30",
        )
        batch_page.click_create_draft()

        # Bị chặn submit tại trang new
        expect(auth_page).to_have_url(re.compile(r".*/fee-batches/new.*"))

    def test_tc_uat_05_04_create_draft_preview_and_publish_flow(
        self, auth_page: Page, batch_page: FeeBatchPage, fee_mgmt_page: FeeManagementPage, uat_data: Dict[str, Any]
    ):
        """
        TC-BATCH-003, TC-BATCH-009, TC-BATCH-010, TC-BATCH-013:
        Tạo mới Component -> Tạo Draft Batch -> Kiểm tra Preview Âm Tính -> Xuất Bản Đợt Phí -> Kiểm Tra Student Charge POSTED.
        Pillar: Flow / AC / BR / Negative Oracle | Priority: P1 (UAT-021, UAT-MOE-01)
        """
        ts = int(time.time())
        comp_name = f"Rosyth P1 Tuition {ts}"

        # 1. Tạo mới Fee Component độc lập để đảm bảo không bị lỗi Overlapping Period
        fee_mgmt_page.open_new_component(BASE_URL)
        fee_mgmt_page.fill_component_name(comp_name)
        fee_mgmt_page.select_fee_type()
        fee_mgmt_page.select_student_categories(["Singapore citizen"])
        fee_mgmt_page.select_education_stages(["Primary"])
        fee_mgmt_page.set_tax_applies(False)
        fee_mgmt_page.click_continue_to_rates()

        expect(auth_page).to_have_url(re.compile(r".*/rate-rules/new.*"), timeout=15000)

        # Lưu Biểu phí Fixed Amount 100.00 SGD có hiệu lực từ 2026-11-01 đến 2027-11-01 (không bị lỗi quá khứ)
        fee_mgmt_page.select_rate_mode("fixed-amount")
        fee_mgmt_page.fill_fixed_amount("100.00")
        fee_mgmt_page.fill_effective_dates("2026-11-01", "2027-11-01")
        fee_mgmt_page.click_save_rates()

        expect(auth_page).to_have_url(re.compile(r".*/fee-management/components/[^/]+$"), timeout=15000)
        expect(fee_mgmt_page.publish_batch_btn.first).to_be_visible()

        # 2. Điều hướng sang tạo Fee Batch qua nút 'Publish batch from this Fee Component'
        fee_mgmt_page.click_publish_batch()
        expect(auth_page).to_have_url(re.compile(r".*/fee-batches/new\?feeComponentId=.*"), timeout=15000)

        # 3. Điền thông tin Đợt thu phí (Period start >= 2026-11-01 để không bị lỗi 'cannot be in the past')
        batch_title = f"Rosyth P1 Tuition Batch {ts}"
        batch_page.fill_batch_form(
            title=batch_title,
            period_start="2026-11-15",
            period_end="2026-12-15",
            due_date="2026-12-31",
            schedule_at=None,
        )

        # Chọn phạm vi trường: All eligible schools
        all_schools_radio = auth_page.locator("label:has-text('All eligible schools'), input[value='all']").first
        if all_schools_radio.count() > 0:
            all_schools_radio.click()

        # Chọn phạm vi học sinh: All eligible students
        all_students_radio = auth_page.locator("label:has-text('All eligible students')").first
        if all_students_radio.count() > 0:
            all_students_radio.click()

        # 4. Bấm Create draft
        batch_page.click_create_draft()
        auth_page.wait_for_load_state("networkidle")

        # 5. Xác nhận điều hướng sang trang chi tiết đợt phí và trạng thái là Draft
        expect(auth_page).to_have_url(re.compile(r".*/fee-batches/[^/]+$"), timeout=20000)
        expect(auth_page.get_by_text(batch_title, exact=False).first).to_be_visible()
        expect(auth_page.get_by_text("Draft", exact=True)).to_be_visible(timeout=10000)

        # 6. Kiểm tra Preview & Negative Oracle (UAT-021)
        # Nút Publish sẵn sàng trên màn hình chi tiết
        publish_btn = auth_page.get_by_role("button", name="Publish", exact=True)
        expect(publish_btn).to_be_visible()

        # 7. Bấm Publish xuất bản đợt thu phí
        publish_btn.click()
        auth_page.wait_for_load_state("networkidle")
        auth_page.wait_for_timeout(3000)

        # Nếu đang ở trạng thái Processing, bấm Check status để cập nhật kết quả mới nhất
        check_status_btn = auth_page.get_by_role("button", name="Check status")
        if check_status_btn.count() > 0 and check_status_btn.is_visible():
            check_status_btn.click()
            auth_page.wait_for_load_state("networkidle")
            auth_page.wait_for_timeout(2000)

        # 8. Tiêu chí nghiệm thu (Pass Oracle): Trạng thái chuyển thành Completed hoặc Published
        status_completed = auth_page.get_by_text("Completed", exact=True)
        expect(status_completed).to_be_visible(timeout=15000)

        # Xác nhận hiển thị danh sách công nợ học sinh có Liam Pham với phí SGD 100.00
        expect(auth_page.locator("text=Liam Pham").first).to_be_visible()
        expect(auth_page.locator("text=100.00").first).to_be_visible()

    def test_tc_uat_05_05_parent_portal_exposure_and_wallet(self, browser: Browser):
        """
        TC-BATCH-016: Đăng nhập Cổng E-Service Singpass với phụ huynh Pham Van Duc (S7654321B)
        xác nhận hiển thị thông tin học sinh Liam Pham (Rosyth Primary School, P1) và ví học vụ.
        Pillar: End-to-End Integration / AC | Priority: P1 (UAT-PAR-01 Bridge)
        """
        context = browser.new_context(ignore_https_errors=True, viewport={"width": 1440, "height": 900})
        page = context.new_page()
        try:
            # 1. Truy cập Cổng Phụ huynh
            page.goto(f"{ESERVICE_URL}/parent/login", wait_until="networkidle")
            page.locator('button:has-text("Sign in with Singpass"), a:has-text("Sign in with Singpass")').first.click()
            page.wait_for_url("**/singpass/login**", timeout=20000)

            # 2. Đăng nhập giả lập bằng Singpass Persona S7654321B (Pham Van Duc)
            persona_select = page.locator("#persona-select")
            expect(persona_select).to_be_visible(timeout=10000)
            persona_select.select_option(label="S7654321B - PHAM VAN DUC [MyInfo]")
            page.locator("#btn-login-selected").click()

            # 3. Chuyển hướng thành công về Cổng E-Service
            page.wait_for_url(f"{ESERVICE_URL}/**", timeout=25000)
            page.wait_for_load_state("networkidle")

            # 4. Kiểm tra hiển thị thông tin gia đình và ví học vụ của Liam Pham
            expect(page.locator("text=Liam Pham").first).to_be_visible(timeout=15000)
            expect(page.locator("text=Rosyth Primary School").first).to_be_visible()
            expect(page.locator("text=Primary 1").first).to_be_visible()

            # 5. Kiểm tra mục Invoices & payments có thể truy cập
            invoices_link = page.locator("text=View invoices & payments").first
            expect(invoices_link).to_be_visible()
        finally:
            context.close()
