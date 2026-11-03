"""
tests/uat/test_uat_6_sbfas_scheme_configuration.py - UAT Test Suite for Step 6 SBFAS Scheme Configuration.
Scenarios:
  - UAT-SCH-02: Create an SBFAS scheme and add a fee (Parts 1 & 2)
  - UAT-SCH-02-N1: Invalid SBFAS scheme: Duplicate name conflict & recovery (Part 3)
  - Date & Income Band Validation tests (Boundary & Error handling)

Target: https://admin.20-255-158-192.sslip.io (/sbfas-schemes)
Role: School Admin / School User (staff1@IAM.edu.vn - Rosyth Primary School)

Strict compliance with:
  - Playwright + Pytest
  - Pure Black-Box Testing (Accessibility Roles, Labels, Visible Texts)
  - Page Object Model (SbfasSchemesPage with ZERO assertions in POM)
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

from pages.fs04.sbfas_schemes_page import SbfasSchemesPage

BASE_URL = os.environ.get("BASE_URL", "https://admin.20-255-158-192.sslip.io").rstrip("/")
SCHOOL_EMAIL = "staff1@IAM.edu.vn"
DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "uat" / "step_06_sbfas_scheme_data.json"


@pytest.fixture(scope="session")
def uat_data() -> Dict[str, Any]:
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def authenticated_school_state(browser: Browser, tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Xác thực một lần duy nhất với tài khoản School Admin (staff1@IAM.edu.vn) qua SSO Simulator."""
    context = browser.new_context(ignore_https_errors=True)
    page = context.new_page()
    try:
        page.goto(f"{BASE_URL}/login", wait_until="networkidle")
        page.locator('button:has-text("Sign in with Microsoft")').click()
        page.wait_for_url("**/microsoft-provider/**", timeout=25000)
        page.locator(f"text={SCHOOL_EMAIL}").first.click()
        page.wait_for_url(f"{BASE_URL}/**", wait_until="domcontentloaded", timeout=30000)
        page.wait_for_load_state("networkidle")

        # Clear active View As session banner if present
        exit_btn = page.get_by_role("button", name="Exit", exact=True)
        if exit_btn.count() > 0 and exit_btn.is_visible():
            exit_btn.click()
            page.wait_for_timeout(1000)

        state_path = tmp_path_factory.mktemp("auth") / "school_sbfas_state.json"
        context.storage_state(path=str(state_path))
        return state_path
    finally:
        context.close()


@pytest.fixture
def auth_page(browser: Browser, authenticated_school_state: Path) -> Page:
    """Page fixture đã có phiên đăng nhập sẵn của School Admin."""
    context = browser.new_context(
        storage_state=str(authenticated_school_state),
        ignore_https_errors=True,
        viewport={"width": 1440, "height": 900},
    )
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture
def sbfas_page(auth_page: Page) -> SbfasSchemesPage:
    return SbfasSchemesPage(auth_page)


class TestUatStep06SbfasSchemeConfiguration:
    """Bộ kiểm thử UAT 6: Cấu hình Gói Trợ cấp Trường SBFAS (UAT-SCH-02 & UAT-SCH-02-N1)."""

    def test_tc_uat_sch_02_01_create_and_publish_sbfas_tier1(
        self, auth_page: Page, sbfas_page: SbfasSchemesPage, uat_data: Dict[str, Any]
    ):
        """
        UAT-SCH-02 Phần 1: Tạo & Xuất bản Gói Trợ cấp SBFAS Tier 1 qua Wizard 4 bước.
        BR: Chỉ School User tạo được gói cho trường mình; Tổng ngân sách > 0;
            Ngày hiệu lực sau ngày đóng đơn; GHI & PCI được cấu hình trần.
        AC: Xuất bản thành công, cấp mã SBF-xxxxx tự động, chuyển trạng thái Published/Active.
        """
        cfg = uat_data["tier1_scheme"]
        timestamp = int(time.time())
        scheme_name = f"{cfg['name_prefix']} UAT {timestamp}"

        # 1. Mở danh sách đề án /sbfas-schemes
        sbfas_page.open_list(BASE_URL)
        expect(sbfas_page.schemes_table).to_be_visible()

        # 2. Bấm New scheme -> Điều hướng sang /sbfas-schemes/new
        sbfas_page.click_new_scheme()
        expect(auth_page).to_have_url(re.compile(r".*/sbfas-schemes/new"))

        # 3. Wizard Bước 1: General (Tên, Ngày nhận đơn, Ngày hiệu lực, Ngân sách)
        sbfas_page.fill_step1_general(
            name=scheme_name,
            open_from=cfg["open_from"],
            open_to=cfg["open_to"],
            effective_from=cfg["effective_from"],
            effective_to=cfg["effective_to"],
            budget=cfg["budget"],
            description=cfg["description"],
        )
        sbfas_page.submit_step1()

        # 4. Wizard Bước 2: Eligibility (Quốc tịch, Trần thu nhập GHI/PCI)
        expect(sbfas_page.nationality_sc_checkbox).to_be_visible()
        sbfas_page.fill_step2_eligibility(
            nationality_sc=True,
            ghi_to=cfg["ghi_to"],
            pci_to=cfg["pci_to"],
        )
        sbfas_page.submit_step2()

        # 5. Wizard Bước 3: Subsidy (Chọn khoản phí & cấu hình tỷ lệ trợ cấp %)
        expect(sbfas_page.add_fee_components_btn).to_be_visible()
        sbfas_page.pick_fee_component_by_index(0)
        sbfas_page.fill_subsidy_rates_all_inputs("100")
        sbfas_page.submit_step3()

        # 6. Wizard Bước 4: Review & Finalize (Kiểm tra tóm tắt & Xuất bản)
        expect(sbfas_page.review_heading).to_be_visible()
        expect(auth_page.locator(f"text={scheme_name}").first).to_be_visible()
        expect(auth_page.locator("text=$50,000.00").first).to_be_visible()

        # Thao tác Publish
        sbfas_page.click_publish()

        # 7. Kết quả kỳ vọng: Tự động chuyển về danh sách /sbfas-schemes
        expect(auth_page).to_have_url(re.compile(r".*/sbfas-schemes$"), timeout=15000)

        # Đề án hiển thị trên bảng với tên, mã SBF tự động và trạng thái Published
        scheme_row = auth_page.locator(f"table tbody tr:has-text('{scheme_name}')")
        expect(scheme_row).to_be_visible()
        expect(scheme_row).to_contain_text(re.compile(r"SBF-\d+"))
        expect(scheme_row).to_contain_text(re.compile(r"Published|Active|Upcoming", re.IGNORECASE))

    def test_tc_uat_sch_02_02_add_fee_component_to_published_scheme(
        self, auth_page: Page, sbfas_page: SbfasSchemesPage, uat_data: Dict[str, Any]
    ):
        """
        UAT-SCH-02 Phần 2: Thêm Thành phần Phí vào Đề án đã Xuất bản.
        BR: Nút Add fee chỉ có hiệu lực trên đề án Active/Upcoming/Published.
        AC: Bổ sung thành phần phí mới vào ma trận, các cột phí cũ giữ nguyên thuộc tính read-only.
        """
        fee_data = uat_data["add_fee_data"]

        # 1. Truy cập danh sách /sbfas-schemes
        sbfas_page.open_list(BASE_URL)
        expect(sbfas_page.schemes_table).to_be_visible()

        # Lấy dòng đề án đầu tiên trên bảng
        first_row = sbfas_page.table_rows.first
        expect(first_row).to_be_visible()
        scheme_text = first_row.locator("td").first.inner_text().split("\n")[0].strip()

        # 2. Bấm vào menu 3 chấm Actions -> Chọn Add fee
        sbfas_page.open_add_fee_dialog_for_scheme(scheme_text)
        expect(sbfas_page.add_fee_dialog).to_be_visible()

        # 3. Chọn khoản phí và nhập % trợ cấp cho các khối lớp
        sbfas_page.submit_add_fee_component(
            component_name=fee_data["component_name"],
            rates_per_grade=["100", "80", "60", "60"],
        )

        # 4. Kỳ vọng: Dialog đóng lại sau khi lưu thành công
        expect(sbfas_page.add_fee_dialog).to_be_hidden(timeout=10000)

    def test_tc_uat_sch_02_n1_duplicate_name_conflict_and_recovery(
        self, auth_page: Page, sbfas_page: SbfasSchemesPage, uat_data: Dict[str, Any]
    ):
        """
        UAT-SCH-02-N1: Kiểm thử Tiêu Cực — Trùng Tên Đề án trong cùng Trường & Khôi phục Hợp lệ.
        Lần 1: Nhập trùng tên đã xuất bản -> Hệ thống chặn và bật Alert:
               'Unable to create scheme: A scheme with this name already exists for this school.'
        Lần 2: Bấm Back quay lại Bước 1, đổi tên thành Tier 2 -> Xuất bản thành công.
        """
        cfg = uat_data["tier1_scheme"]
        n1_data = uat_data["n1_conflict_data"]
        timestamp = int(time.time())
        original_name = f"TierConflict_{timestamp}"
        recovery_name = f"TierRecovered_{timestamp}"

        # Setup: Tạo một đề án hợp lệ trước để làm mốc trùng lặp
        sbfas_page.open_create_wizard(BASE_URL)
        sbfas_page.fill_step1_general(
            name=original_name,
            open_from=cfg["open_from"],
            open_to=cfg["open_to"],
            effective_from=cfg["effective_from"],
            budget=cfg["budget"],
        )
        sbfas_page.submit_step1()
        sbfas_page.fill_step2_eligibility(nationality_sc=True, ghi_to="3000", pci_to="1000")
        sbfas_page.submit_step2()
        sbfas_page.pick_fee_component_by_index(0)
        sbfas_page.fill_subsidy_rates_all_inputs("100")
        sbfas_page.submit_step3()
        sbfas_page.click_publish()
        expect(auth_page).to_have_url(re.compile(r".*/sbfas-schemes$"), timeout=15000)

        # --- LẦN 1: Thử tạo đề án trùng lặp tên vừa tạo ---
        sbfas_page.click_new_scheme()
        sbfas_page.fill_step1_general(
            name=original_name,  # Trùng lặp tên
            open_from=cfg["open_from"],
            open_to=cfg["open_to"],
            effective_from=cfg["effective_from"],
            budget=cfg["budget"],
        )
        sbfas_page.submit_step1()
        sbfas_page.fill_step2_eligibility(nationality_sc=True, ghi_to="3000", pci_to="1000")
        sbfas_page.submit_step2()
        sbfas_page.pick_fee_component_by_index(0)
        sbfas_page.fill_subsidy_rates_all_inputs("100")
        sbfas_page.submit_step3()

        # Tại Bước 4: Nhấn Publish và kiểm tra lỗi chặn
        sbfas_page.click_publish()

        # Kỳ vọng Lần 1: Chặn xuất bản, giữ nguyên ở bước Review, hiển thị Alert lỗi chính xác
        expect(auth_page).to_have_url(re.compile(r".*/sbfas-schemes/new"))
        expect(sbfas_page.alert_error).to_be_visible()
        expect(sbfas_page.alert_error).to_contain_text("Unable to create scheme")
        expect(sbfas_page.alert_error).to_contain_text(n1_data["expected_error"])

        # --- LẦN 2: Sửa tên hợp lệ và hoàn tất xuất bản ---
        sbfas_page.navigate_back_to_step1()
        expect(sbfas_page.name_input).to_be_visible()

        # Đổi tên thành tên mới duy nhất
        sbfas_page.name_input.fill(recovery_name)
        sbfas_page.submit_step1()
        sbfas_page.submit_step2()
        sbfas_page.submit_step3()

        # Nhấn Publish lại
        sbfas_page.click_publish()

        # Kỳ vọng Lần 2: Hệ thống chấp thuận, xuất bản thành công và chuyển hướng về /sbfas-schemes
        expect(auth_page).to_have_url(re.compile(r".*/sbfas-schemes$"), timeout=15000)
        expect(auth_page.locator(f"table tbody tr:has-text('{recovery_name}')")).to_be_visible()

    def test_tc_uat_sch_02_bva_date_ordering_validation(
        self, auth_page: Page, sbfas_page: SbfasSchemesPage
    ):
        """
        BVA Validation: Kiểm tra ràng buộc ngày hiệu lực Effective From phải sau ngày đóng nhận đơn Open To.
        Input: Open To: 2026-11-30, Effective From: 2026-11-30 (trùng ngày).
        Kỳ vọng: Hệ thống chặn chuyển tiếp Bước 2 và kích hoạt cờ validation.
        """
        sbfas_page.open_create_wizard(BASE_URL)
        sbfas_page.fill_step1_general(
            name=f"DateBVA_{int(time.time())}",
            open_from="2026-11-01",
            open_to="2026-11-30",
            effective_from="2026-11-30",  # Trùng ngày đóng nhận đơn (vi phạm Effective From > Open To)
            budget="50000",
        )
        sbfas_page.submit_step1()

        # Kiểm tra form bị chặn không được chuyển sang Bước 2
        is_step1_still_visible = sbfas_page.name_input.is_visible()
        assert is_step1_still_visible, "Form phải chặn chuyển sang Bước 2 khi ngày hiệu lực không hợp lệ"

    def test_tc_uat_sch_02_validation_income_band_missing_upper_bound(
        self, auth_page: Page, sbfas_page: SbfasSchemesPage, uat_data: Dict[str, Any]
    ):
        """
        Validation Bước 2: Bật tiêu chí thu nhập (Enable income band) nhưng bỏ trống ô trần To *.
        Kỳ vọng: Hệ thống hiển thị thông báo lỗi 'Enter the upper value of the income band'.
        """
        sbfas_page.open_create_wizard(BASE_URL)
        sbfas_page.fill_step1_general(
            name=f"IncomeBVA_{int(time.time())}",
            open_from="2026-11-01",
            open_to="2026-11-30",
            effective_from="2026-12-01",
            budget="50000",
        )
        sbfas_page.submit_step1()

        # Bước 2: Để trống ô GHI To và PCI To
        expect(sbfas_page.ghi_to_input).to_be_visible()
        sbfas_page.ghi_to_input.fill("")
        sbfas_page.pci_to_input.fill("")
        sbfas_page.submit_step2()

        # Kỳ vọng: Form bị chặn không chuyển sang Bước 3, hiển thị lỗi trần thu nhập
        error_msg = uat_data["validation_cases"]["missing_income_band_error"]
        expect(auth_page.locator(f"text={error_msg}").first).to_be_visible()
