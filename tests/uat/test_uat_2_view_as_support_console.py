"""
tests/uat/test_uat_2_view_as_support_console.py - UAT Test Suite for View As Support Console.
Target: https://admin.20-255-158-192.sslip.io (/support-console)
Strict compliance with:
  - Playwright + Pytest
  - Pure Black-Box Testing (Accessibility Roles, Labels, Visible Texts)
  - Page Object Model (ViewAsPage with NO assertions in POM)
  - 4 Pillars: BR, AC, BVA/Validation, Function Flow
"""
import copy
import json
import os
from pathlib import Path
import pytest
from playwright.sync_api import Browser, Page, expect

from pages.fs03.view_as_page import ViewAsPage

BASE_URL = os.environ.get("BASE_URL", "https://admin.20-255-158-192.sslip.io").rstrip("/")
ADMIN_EMAIL = "admin@IAM.edu.vn"
DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "uat" / "step_02_view_as_data.json"


@pytest.fixture(scope="session")
def uat_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def admin_session_state(browser: Browser, tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Authenticate once as MOE HQ Admin via Microsoft Simulator and store session state."""
    state_file = tmp_path_factory.mktemp("auth") / "moehq_session.json"
    
    temp_auth = Path("/tmp/moehq_auth.json")
    if temp_auth.exists() and temp_auth.stat().st_size > 50:
        return temp_auth

    context = browser.new_context(ignore_https_errors=True)
    try:
        page = context.new_page()
        page.goto(f"{BASE_URL}/login", wait_until="domcontentloaded")
        page.get_by_role("button", name="Sign in with Microsoft").click()
        page.wait_for_url("**/microsoft-provider/**", timeout=25000)
        
        # Select MOE HQ Admin
        account_tile = page.locator(f".account-tile:has-text('{ADMIN_EMAIL}'), [data-email='{ADMIN_EMAIL}']").first
        if account_tile.count() > 0:
            account_tile.click()
        else:
            page.get_by_text(ADMIN_EMAIL, exact=False).first.click()

        page.wait_for_url(f"{BASE_URL}/**", timeout=25000)
        page.wait_for_load_state("networkidle")
        context.storage_state(path=str(state_file))
        return state_file
    finally:
        context.close()


@pytest.fixture
def admin_page(browser: Browser, admin_session_state: Path) -> Page:
    """Create fresh Page with authenticated MOE HQ session."""
    context = browser.new_context(
        storage_state=str(admin_session_state),
        ignore_https_errors=True,
        viewport={"width": 1440, "height": 900},
    )
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture
def view_as_pom(admin_page: Page) -> ViewAsPage:
    return ViewAsPage(admin_page)


# ---------------------------------------------------------------------------
# NHÓM 1: ĐIỀU HƯỚNG & GIAO DIỆN KHỞI TẠO (AC-01 / BR-VA-01)
# ---------------------------------------------------------------------------

@pytest.mark.smoke
@pytest.mark.p1
def test_tc_va_001_sidebar_navigation_to_support_console(admin_page: Page, view_as_pom: ViewAsPage):
    """
    TC-VA-001: Quản trị viên MOE HQ bấm vào mục 'View As' trên Sidebar.
    Kỳ vọng: Điều hướng tới /support-console, hiển thị tiêu đề 'View As' và các Tab.
    """
    admin_page.goto(f"{BASE_URL}/", wait_until="domcontentloaded")
    expect(view_as_pom.sidebar_link_view_as).to_be_visible()
    
    view_as_pom.click_sidebar_view_as()
    admin_page.wait_for_url("**/support-console", timeout=15000)
    
    expect(view_as_pom.page_heading).to_be_visible()
    expect(view_as_pom.tab_school_users).to_be_visible()
    expect(view_as_pom.tab_persona).to_be_visible()


# ---------------------------------------------------------------------------
# NHÓM 2: CHỌN ĐỐI TƯỢNG VÀ KHÓA NÚT MẶC ĐỊNH (AC-02 / BR-VA-03)
# ---------------------------------------------------------------------------

@pytest.mark.flow
@pytest.mark.p1
def test_tc_va_002_persona_selection_form_lock(admin_page: Page, view_as_pom: ViewAsPage, uat_data: dict):
    """
    TC-VA-002: Chọn đối tượng theo Tab 'School role (persona)' (Cách A).
    Kỳ vọng: Form xuất hiện, nút 'Start View As' mặc định bị Disabled (khóa mờ).
    """
    view_as_pom.open(BASE_URL)
    persona = uat_data["persona_mode"]
    
    view_as_pom.search_and_select_persona(
        school_code_or_name=persona["school_code"],
        role_name=persona["role_name"]
    )
    
    expect(view_as_pom.start_view_as_button).to_be_visible()
    expect(view_as_pom.start_view_as_button).to_be_disabled()


@pytest.mark.flow
@pytest.mark.p1
def test_tc_va_003_school_user_selection_form_lock(admin_page: Page, view_as_pom: ViewAsPage, uat_data: dict):
    """
    TC-VA-003: Chọn đối tượng theo Tab 'School users' (Cách B).
    Kỳ vọng: Form xuất hiện, nút 'Start View As' mặc định bị Disabled (khóa mờ).
    """
    view_as_pom.open(BASE_URL)
    user_data = uat_data["user_mode"]
    
    view_as_pom.search_and_select_school_user(search_query=user_data["search_keyword"])
    
    expect(view_as_pom.start_view_as_button).to_be_visible()
    expect(view_as_pom.start_view_as_button).to_be_disabled()


# ---------------------------------------------------------------------------
# NHÓM 3: PHÂN TÍCH GIÁ TRỊ BIÊN (BVA) & VALIDATION FORM KIỂM TOÁN (AC-03 / BR-VA-02)
# ---------------------------------------------------------------------------

@pytest.mark.bva
@pytest.mark.p2
def test_tc_va_004_reason_boundary_under_10_chars(admin_page: Page, view_as_pom: ViewAsPage, uat_data: dict):
    """
    TC-VA-004: Kiểm tra giá trị biên dưới (A - 1): Reason chỉ có 9 ký tự.
    Kỳ vọng: Nút 'Start View As' bắt buộc vẫn bị Disabled (chưa đủ 10 ký tự).
    """
    view_as_pom.open(BASE_URL)
    view_as_pom.search_and_select_school_user("staff1")
    
    boundary = uat_data["audit_form"]["boundary_reason"]
    ticket = uat_data["audit_form"]["boundary_ticket"]["valid"]
    
    view_as_pom.fill_audit_reason(boundary["below_min_9_chars"])
    view_as_pom.fill_ticket_reference(ticket)
    
    expect(view_as_pom.start_view_as_button).to_be_disabled()


@pytest.mark.bva
@pytest.mark.p1
def test_tc_va_005_reason_boundary_exact_10_chars(admin_page: Page, view_as_pom: ViewAsPage, uat_data: dict):
    """
    TC-VA-005: Kiểm tra đúng biên dưới (A): Reason đạt chính xác 10 ký tự.
    Kỳ vọng: Nút 'Start View As' chuyển sang Enabled (sáng xanh dương).
    """
    view_as_pom.open(BASE_URL)
    view_as_pom.search_and_select_school_user("staff1")
    
    boundary = uat_data["audit_form"]["boundary_reason"]
    ticket = uat_data["audit_form"]["boundary_ticket"]["valid"]
    
    view_as_pom.fill_audit_reason(boundary["exact_min_10_chars"])
    view_as_pom.fill_ticket_reference(ticket)
    
    expect(view_as_pom.start_view_as_button).to_be_enabled()


@pytest.mark.validation
@pytest.mark.p2
def test_tc_va_006_ticket_reference_required_validation(admin_page: Page, view_as_pom: ViewAsPage, uat_data: dict):
    """
    TC-VA-006: Reason đạt độ dài hợp lệ (>10 ký tự) nhưng để trống Ticket reference.
    Kỳ vọng: Nút 'Start View As' vẫn bị Disabled cho đến khi có mã ticket.
    """
    view_as_pom.open(BASE_URL)
    view_as_pom.search_and_select_school_user("staff1")
    
    valid_reason = uat_data["audit_form"]["valid_payload"]["reason"]
    
    view_as_pom.fill_audit_reason(valid_reason)
    view_as_pom.fill_ticket_reference("")
    
    expect(view_as_pom.start_view_as_button).to_be_disabled()


# ---------------------------------------------------------------------------
# NHÓM 4: CHUYỂN ĐỔI NGỮ CẢNH & PHÂN QUYỀN TRƯỜNG HỌC (AC-04 / AC-05 / BR-VA-04)
# ---------------------------------------------------------------------------

@pytest.mark.flow
@pytest.mark.p1
def test_tc_va_007_start_view_as_and_verify_school_context(admin_page: Page, view_as_pom: ViewAsPage, uat_data: dict):
    """
    TC-VA-007: Điền đủ Reason (>=10 ký tự) & Ticket reference, bấm 'Start View As'.
    Kỳ vọng:
      1. Header đổi thành thông tin Cán bộ trường (chứa 'Thi H Bui' hoặc 'school').
      2. Sidebar lập tức chuyển sang các menu cấp trường: Classes, School config, Students...
    """
    view_as_pom.open(BASE_URL)
    view_as_pom.search_and_select_school_user("staff1")
    
    payload = uat_data["audit_form"]["valid_payload"]
    view_as_pom.fill_audit_form(reason=payload["reason"], ticket=payload["ticket_reference"])
    
    expect(view_as_pom.start_view_as_button).to_be_enabled()
    view_as_pom.click_start_view_as()
    
    admin_page.wait_for_timeout(1500)
    
    # Assert 1: Header chuyển sang ngữ cảnh trường học
    expect(view_as_pom.header_element).to_contain_text("school")
    
    # Assert 2: Menu trường học xuất hiện trên Sidebar
    expect(view_as_pom.menu_classes).to_be_visible()
    expect(view_as_pom.menu_school_config).to_be_visible()


@pytest.mark.flow
@pytest.mark.p1
def test_tc_va_008_verify_school_action_permissions(admin_page: Page, view_as_pom: ViewAsPage, uat_data: dict):
    """
    TC-VA-008: Trong ngữ cảnh View As trường học, truy cập /class-management và kiểm tra nút Create class.
    Kỳ vọng: Nút 'Create class' mở và có thể bấm được bình thường.
    """
    view_as_pom.open(BASE_URL)
    view_as_pom.search_and_select_school_user("staff1")
    
    payload = uat_data["audit_form"]["valid_payload"]
    view_as_pom.fill_audit_form(reason=payload["reason"], ticket=payload["ticket_reference"])
    view_as_pom.click_start_view_as()
    admin_page.wait_for_timeout(1500)
    
    # Điều hướng sang /class-management
    view_as_pom.menu_classes.click()
    admin_page.wait_for_url("**/class-management", timeout=15000)
    
    create_class_btn = admin_page.get_by_role("button", name="Create class")
    expect(create_class_btn).to_be_visible()
    expect(create_class_btn).to_be_enabled()
