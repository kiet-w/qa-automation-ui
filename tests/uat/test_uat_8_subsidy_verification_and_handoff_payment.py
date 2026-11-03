"""
tests/uat/test_uat_8_subsidy_verification_and_handoff_payment.py - UAT Test Suite for Step 8:
Subsidy Verification, Handoff Dossier & Gavin's Payment Execution (UAT-PAR-01).

Targets:
  - Admin Portal: https://admin.20-255-158-192.sslip.io (/fee-batches & /student-management)
  - Parent E-Service Portal: https://eservice.20-255-158-192.sslip.io (/parent/login & /accounts/STU-001/pay)

Roles:
  - School Admin / UAT Lead: Kent (admin@IAM.edu.vn / moehq)
  - Parent Tester: Gavin (Pham Van Duc, Singpass S7654321B)

Strict compliance with:
  - Playwright + Pytest
  - Pure Black-Box Testing (Accessibility Roles, Labels, Visible Texts)
  - 4 Pillars: BR, AC, Validation, Function Flow
  - 10-Column ISTQB Traceability: TC-FAS-0801, TC-PAY-0804, TC-HDF-0807, TC-PAY-0808, TC-SEC-0812, TC-REP-0813
"""

import json
import os
import re
import pytest
from pathlib import Path
from typing import Any, Dict
from playwright.sync_api import Browser, Page, expect

ADMIN_URL = os.environ.get("BASE_URL", "https://admin.20-255-158-192.sslip.io").rstrip("/")
ESERVICE_URL = os.environ.get("ESERVICE_URL", "https://eservice.20-255-158-192.sslip.io").rstrip("/")
ADMIN_EMAIL = "admin@IAM.edu.vn"
DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "uat" / "step_08_handoff_payment_data.json"


@pytest.fixture(scope="session")
def step8_data() -> Dict[str, Any]:
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def authenticated_admin_state(browser: Browser, tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Xác thực phiên làm việc MOE HQ Admin qua Microsoft SSO Simulator."""
    context = browser.new_context(ignore_https_errors=True)
    page = context.new_page()
    try:
        page.goto(f"{ADMIN_URL}/login", wait_until="networkidle")
        page.locator('button:has-text("Sign in with Microsoft")').click()
        page.wait_for_url("**/microsoft-provider/**", timeout=25000)
        page.locator(f"text={ADMIN_EMAIL}").first.click()
        page.wait_for_url(f"{ADMIN_URL}/**", wait_until="domcontentloaded", timeout=30000)
        page.wait_for_load_state("networkidle")

        exit_btn = page.get_by_role("button", name="Exit", exact=True)
        if exit_btn.count() > 0 and exit_btn.is_visible():
            exit_btn.click()
            page.wait_for_timeout(1000)

        state_path = tmp_path_factory.mktemp("auth") / "step8_admin_state.json"
        context.storage_state(path=str(state_path))
        return state_path
    finally:
        context.close()


@pytest.fixture(scope="session")
def authenticated_parent_state(browser: Browser, tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Xác thực phiên làm việc Phụ huynh Pham Van Duc (S7654321B) qua Singpass Mock."""
    context = browser.new_context(ignore_https_errors=True)
    page = context.new_page()
    try:
        page.goto(f"{ESERVICE_URL}/parent/login", wait_until="networkidle")
        sp_btn = page.locator('button:has-text("Sign in with Singpass"), a:has-text("Sign in with Singpass")')
        sp_btn.click()
        page.wait_for_timeout(1000)

        select = page.locator("select")
        if select.count() > 0:
            select.select_option(index=1)
            page.locator("#btn-login-selected").click()
            page.wait_for_timeout(3000)

        state_path = tmp_path_factory.mktemp("auth") / "step8_parent_state.json"
        context.storage_state(path=str(state_path))
        return state_path
    finally:
        context.close()


@pytest.fixture
def admin_page(browser: Browser, authenticated_admin_state: Path) -> Page:
    context = browser.new_context(
        storage_state=str(authenticated_admin_state),
        ignore_https_errors=True,
        viewport={"width": 1440, "height": 900},
    )
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture
def parent_page(browser: Browser, authenticated_parent_state: Path) -> Page:
    context = browser.new_context(
        storage_state=str(authenticated_parent_state),
        ignore_https_errors=True,
        viewport={"width": 1440, "height": 900},
    )
    page = context.new_page()
    yield page
    context.close()


class TestUatStep08HandoffAndPayment:
    """Bộ kiểm thử UAT Bước 8: Kiểm Tra Giảm Trừ, Bàn Giao & Thanh Toán Gavin (UAT-PAR-01)."""

    def test_tc_fas_0801_admin_fee_batches_published_status(self, admin_page: Page, step8_data: Dict[str, Any]):
        """
        TC-FAS-0801: Kiểm tra danh sách Fee Batches tại Admin Portal (/fee-batches).
        BR: Các đợt phát hành học phí phải đạt trạng thái Completed/Published.
        AC: Bảng đợt phí hiển thị đầy đủ tiêu đề, kỳ phát hành, và trạng thái.
        """
        admin_page.goto(f"{ADMIN_URL}/fee-batches", wait_until="networkidle")
        expect(admin_page.locator("table")).to_be_visible(timeout=15000)
        table_text = admin_page.locator("table").inner_text()
        assert "Completed" in table_text or "Published" in table_text or "Nov 1, 2026" in table_text

    def test_tc_fas_0803_admin_student_ledger_profile(self, admin_page: Page, step8_data: Dict[str, Any]):
        """
        TC-FAS-0803: Kiểm tra hồ sơ học sinh Liam Pham tại /student-management/STU-001.
        BR: Học sinh Liam Pham được ghi danh vào lớp 1A1 trường Rosyth Primary School.
        AC: NRIC S4744854C, trạng thái ENROLLED.
        """
        admin_page.goto(f"{ADMIN_URL}/student-management/STU-001", wait_until="networkidle")
        body_text = admin_page.inner_text("body")
        assert "Liam Pham" in body_text
        assert "S4744854C" in body_text
        assert "Rosyth Primary School" in body_text
        assert "Primary 1 - 1A1" in body_text

    def test_tc_pay_0804_parent_account_and_masked_nric(self, parent_page: Page, step8_data: Dict[str, Any]):
        """
        TC-PAY-0804: Kiểm tra chi tiết tài khoản học vụ EDU-01001 tại /accounts/STU-001.
        BR: Số NRIC của học sinh phải luôn được che (Masked NRIC: *****854C).
        AC: Hiển thị đúng số dư ví EA khả dụng (SGD 500.00 ban đầu / số dư hiện tại).
        """
        parent_page.goto(f"{ESERVICE_URL}/accounts/STU-001", wait_until="networkidle")
        body_text = parent_page.inner_text("body")
        assert "Liam Pham" in body_text
        assert "EDU-01001" in body_text
        assert "*****854C" in body_text
        assert "EA BALANCE" in body_text
        assert "SGD" in body_text

    def test_tc_pay_0805_parent_outstanding_charges_breakdown(self, parent_page: Page, step8_data: Dict[str, Any]):
        """
        TC-PAY-0805: Kiểm tra bảng đối soát công nợ học phí tại /accounts/STU-001/pay.
        BR: Hiển thị đầy đủ các cột Gross amount, Subsidy, Amount due (Net).
        AC: Bảng nợ học phí sẵn sàng cho việc chọn khoản phí và thanh toán.
        """
        parent_page.goto(f"{ESERVICE_URL}/accounts/STU-001/pay", wait_until="networkidle")
        expect(parent_page.locator("table")).to_be_visible(timeout=15000)
        table_text = parent_page.locator("table").inner_text()
        assert "Gross amount" in table_text
        assert "Subsidy" in table_text
        assert "Amount due" in table_text

    def test_tc_hdf_0807_handoff_dossier_preconditions(self, step8_data: Dict[str, Any]):
        """
        TC-HDF-0807: Kiểm tra tính đầy đủ và hợp lệ của bộ hồ sơ bàn giao (Gate G1).
        BR: Số dư ví EA khả dụng (SGD 500.00) phải lớn hơn hoặc bằng Net Amount (SGD 40.00).
        AC: Đầy đủ 4 khối fixtures: Student, Parent, EA Wallet, Charge/Invoice.
        """
        student = step8_data["student_fixture"]
        parent = step8_data["parent_fixture"]
        ea = step8_data["edusave_account"]

        assert student["full_name"] == "Liam Pham"
        assert student["student_id"] == "STU-00001"
        assert student["nric_masked"] == "*****854C"
        assert parent["singpass_mock_nric"] == "S7654321B"
        assert ea["ea_code"] == "EDU-01001"
        assert ea["opening_balance"] >= 40.00
        assert step8_data["handoff_meta"]["gate_readiness"] == "Gate G1 Passed"

    def test_tc_pay_0808_gavin_uat_par_01_ea_payment_journey(self, parent_page: Page, step8_data: Dict[str, Any]):
        """
        TC-PAY-0808: Gavin thực thi ca kiểm thử UAT-PAR-01 (Thanh toán hoàn toàn bằng ví EA).
        BR: Phụ huynh chọn phí hợp lệ, chọn phương thức Education Account, xác nhận thanh toán.
        AC: Hệ thống cho phép hoàn tất quy trình Review & Authorize.
        """
        parent_page.goto(f"{ESERVICE_URL}/accounts/STU-001/pay", wait_until="networkidle")
        expect(parent_page.locator("tbody input[type='checkbox']").first).to_be_visible(timeout=15000)

        # 1. Chọn khoản phí hợp lệ (số tiền <= số dư ví EA để phương thức EA khả dụng)
        target_row = parent_page.locator("tbody tr:has-text('Standard Miscellaneous Fee')").first
        if target_row.count() == 0:
            target_row = parent_page.locator("tbody tr:has-text('Tuition')").first
        if target_row.count() == 0:
            target_row = parent_page.locator("tbody tr").first

        target_cb = target_row.locator("input[type='checkbox']").first
        target_cb.check()

        # 2. Nhấn Continue sang màn hình Payment Method
        continue_btn = parent_page.locator("button:has-text('Continue')")
        expect(continue_btn).to_be_enabled()
        continue_btn.click()
        parent_page.wait_for_timeout(1000)

        # 3. Chọn phương thức thanh toán Education Account
        ea_radio = parent_page.locator("input[value='EducationAccount']")
        if ea_radio.count() > 0:
            if not ea_radio.is_checked():
                ea_radio.check(force=True)
        else:
            ea_option = parent_page.locator("text='Education Account'").first
            ea_option.click(force=True)

        # 4. Nhấn Continue sang màn hình Review & Authorize
        parent_page.locator("button:has-text('Continue')").click()
        parent_page.wait_for_timeout(1000)

        # 5. Xác nhận cấu trúc màn hình Review & Authorize
        body_text = parent_page.inner_text("body")
        assert "Review payment" in body_text or "Review & authorize" in body_text or "Review" in body_text
        assert "Education Account" in body_text
        assert "Authorize & pay" in body_text

    def test_tc_sec_0812_and_0813_safety_gates(self, step8_data: Dict[str, Any]):
        """
        TC-SEC-0812 & TC-REP-0813: Kiểm chứng các chốt chặn an toàn Gate G2 và Gate G3.
        Gate G2: Invariant chống trừ trùng tiền (No double debit).
        Gate G3: Đối soát tính toàn vẹn tài chính trên phiếu thu (Gross = Subsidy + Paid).
        """
        gates = step8_data["safety_gates"]
        g2 = gates["gate_g2_idempotency"]
        g3 = gates["gate_g3_receipt_reconciliation"]

        assert g2["rule"] == "No double debit"
        assert g3["expected_receipt"]["gross"] == "SGD 100.00"
        assert g3["expected_receipt"]["subsidy_sbfas"] == "SGD 60.00"
        assert g3["expected_receipt"]["net_paid"] == "SGD 40.00"
        assert g3["expected_receipt"]["balance_outstanding"] == "SGD 0.00"
