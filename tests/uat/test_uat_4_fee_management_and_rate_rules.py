"""
tests/uat/test_uat_4_fee_management_and_rate_rules.py - UAT Test Suite for Step 4 Fee Management & Rate Rules.
Target: https://admin.20-255-158-192.sslip.io (or https://localhost:5173) (/fee-management)
Strict compliance with:
  - Playwright + Pytest
  - Pure Black-Box Testing (Accessibility Roles, Labels, Visible Texts)
  - Page Object Model (FeeManagementPage with NO assertions in POM)
  - 4 Pillars: BR, AC, BVA/Validation, Function Flow
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

from pages.fs03.fee_management_page import FeeManagementPage

BASE_URL = os.environ.get("BASE_URL", "https://localhost:5173").rstrip("/")
ADMIN_EMAIL = "admin@IAM.edu.vn"
DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "uat" / "step_04_fee_management_data.json"


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
        page.wait_for_url("**/microsoft-provider/**", timeout=20000)
        page.locator(f"text={ADMIN_EMAIL}").first.click()
        page.wait_for_url(f"{BASE_URL}/", wait_until="domcontentloaded", timeout=30000)
        page.wait_for_load_state("networkidle")
        page.locator("text=System Admin").first.wait_for(state="visible", timeout=15000)

        # Clear active View As session banner if present
        exit_btn = page.get_by_role("button", name="Exit", exact=True)
        if exit_btn.count() > 0 and exit_btn.is_visible():
            exit_btn.click()
            page.wait_for_timeout(1000)

        state_path = tmp_path_factory.mktemp("auth") / "moehq_state.json"
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
        viewport={"width": 1440, "height": 900}
    )
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture
def fee_page(auth_page: Page) -> FeeManagementPage:
    return FeeManagementPage(auth_page)


class TestUatStep04FeeManagement:
    """Bộ kiểm thử UAT 4 Màn hình Quản lý Phí và Cầu nối Bước 5."""

    def test_tc_uat_04_01_screen1_overview_and_entry_paths(self, auth_page: Page, fee_page: FeeManagementPage):
        """Màn 1: Kiểm tra Danh mục Phí tại /fee-management & Thao tác View -> Create Component."""
        fee_page.open_overview(BASE_URL)

        # BR: Bảng danh mục loại phí phải hiển thị
        expect(fee_page.fee_types_table).to_be_visible()
        expect(fee_page.fee_type_view_btn.first).to_be_visible()

        # AC: Bấm View tại dòng loại phí đầu tiên
        fee_page.click_first_fee_type_view()
        expect(auth_page).to_have_url(re.compile(r".*/fee-types/.*"))

        # Bấm Create fee component -> Điều hướng sang /components/new
        fee_page.click_create_fee_component()
        expect(auth_page).to_have_url(re.compile(r".*/components/new.*"))
        expect(fee_page.step1_heading).to_be_visible()
        expect(fee_page.component_name_input).to_be_visible()

    def test_tc_uat_04_02_screen2_mandatory_name_validation(self, auth_page: Page, fee_page: FeeManagementPage):
        """Màn 2: Validation bắt buộc nhập Tên thành phần phí khi để trống Name."""
        fee_page.open_new_component(BASE_URL)

        # Để trống Name và bấm Continue to rates
        fee_page.click_continue_to_rates()

        # Form phải bị chặn không được chuyển sang /rate-rules/new
        expect(auth_page).to_have_url(re.compile(r".*/components/new.*"))
        is_invalid = fee_page.component_name_input.evaluate("el => el.getAttribute('aria-invalid') === 'true' || !el.checkValidity()")
        assert is_invalid, "Trường #fee-component-name phải kích hoạt trạng thái không hợp lệ khi rỗng"

    def test_tc_uat_04_03_screen3_date_range_bva_validation(self, auth_page: Page, fee_page: FeeManagementPage, uat_data):
        """Màn 3: BVA Validation ngày hiệu lực đảo ngược (From > To) tại /rate-rules/new."""
        fee_page.open_new_component(BASE_URL)

        unique_name = f"Validation Component {int(time.time())}"
        fee_page.fill_component_name(unique_name)
        fee_page.select_fee_type()
        fee_page.select_student_categories(uat_data["component_data"]["categories"])
        fee_page.select_education_stages(uat_data["component_data"]["stages"])
        fee_page.set_tax_applies(True)
        fee_page.click_continue_to_rates()

        expect(auth_page).to_have_url(re.compile(r".*/rate-rules/new.*"), timeout=15000)

        # Nhập From: 2026-12-31 > To: 2026-01-01
        fee_page.select_rate_mode("fixed-amount")
        fee_page.fill_fixed_amount("100.00")
        fee_page.fill_effective_dates("2026-12-31", "2026-01-01")
        fee_page.click_save_rates()

        # Hệ thống phải chặn submit và giữ nguyên tại form /rate-rules/new
        expect(auth_page).to_have_url(re.compile(r".*/rate-rules/new.*"))

    def test_tc_uat_04_04_end_to_end_4_screens_and_step5_bridge(self, auth_page: Page, fee_page: FeeManagementPage, uat_data):
        """Luồng hoàn chỉnh qua trọn vẹn 4 màn hình & Cầu nối sang Bước 5 (/fee-batches/new)."""
        unique_name = f"UAT Tuition Fee 2026 {int(time.time())}"
        cfg = uat_data["rate_rules_mode_a"]

        # 1. Màn 2: Khai báo thành phần phí
        fee_page.open_new_component(BASE_URL)
        fee_page.fill_component_name(unique_name)
        fee_page.select_fee_type()
        fee_page.select_student_categories(uat_data["component_data"]["categories"])
        fee_page.select_education_stages(uat_data["component_data"]["stages"])
        fee_page.set_tax_applies(True)
        fee_page.click_continue_to_rates()

        # 2. Màn 3: Tự động chuyển hướng sang /rate-rules/new
        expect(auth_page).to_have_url(re.compile(r".*/rate-rules/new.*"), timeout=15000)

        # 3. Màn 3: Thiết lập Chế độ A Fixed Amount (100.00 SGD, 2026-01-01 đến 2026-12-31)
        fee_page.select_rate_mode(cfg["mode"])
        expect(fee_page.currency_input).to_have_value(cfg["currency"])
        fee_page.fill_fixed_amount(cfg["amount"])
        fee_page.fill_effective_dates(cfg["effective_from"], cfg["effective_to"])
        fee_page.click_save_rates()

        # 4. Màn 4: Màn hình Chi tiết Thành phần Phí (/components/:id)
        expect(auth_page).to_have_url(re.compile(r".*/fee-management/components/[^/]+$"), timeout=15000)
        expect(auth_page.locator(f"text={unique_name}").first).to_be_visible()
        expect(auth_page.locator("text=$100.00").first).to_be_visible()
        expect(fee_page.publish_batch_btn.first).to_be_visible()

        # 5. Bước 5 Bridge: Bấm nút Publish batch from this Fee Component
        fee_page.click_publish_batch()

        # Điều hướng sang /fee-batches/new?feeComponentId=...
        expect(auth_page).to_have_url(re.compile(r".*/fee-batches/new\?feeComponentId=.*"), timeout=15000)
