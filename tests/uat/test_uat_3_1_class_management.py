"""
Kịch bản kiểm thử tự động UAT 3.1: Kiểm tra hoặc Tạo Lớp học (Classes)
Target: https://admin.20-255-158-192.sslip.io (Admin Portal)
Tuân thủ tiêu chuẩn:
  - Playwright + Pytest
  - Pure Black-Box Testing (không đọc source code, không dùng CSS băm)
  - Page Object Model chuẩn (không assert trong POM)
  - 5 Trụ cột QA (BR, AC, Validation, Function Flow, Error Handling)
"""
import os
import re
import time
from pathlib import Path
import pytest
from playwright.sync_api import Browser, Page, expect

from pages.fs03.class_management_page import ClassManagementPage

BASE_URL = os.environ.get("BASE_URL", "https://admin.20-255-158-192.sslip.io").rstrip("/")
DEFAULT_SCHOOL_EMAIL = "staff1@IAM.edu.vn"


@pytest.fixture(scope="session")
def school_session_state(browser: Browser, tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Đăng nhập bằng tài khoản Cán bộ trường qua Microsoft Simulator và lưu session state."""
    state_file = tmp_path_factory.mktemp("auth") / "school_session.json"
    
    # Kiểm tra nếu đã có session hợp lệ trong /tmp thì dùng lại
    temp_auth = Path("/tmp/school_auth.json")
    if temp_auth.exists() and temp_auth.stat().st_size > 50:
        return temp_auth

    context = browser.new_context(ignore_https_errors=True)
    try:
        page = context.new_page()
        page.goto(f"{BASE_URL}/login", wait_until="domcontentloaded")
        page.get_by_role("button", name="Sign in with Microsoft").click()
        page.wait_for_url("**/microsoft-provider/**", timeout=20000)
        page.get_by_text(DEFAULT_SCHOOL_EMAIL, exact=False).click()
        page.wait_for_url(f"{BASE_URL}/**", timeout=20000)
        page.wait_for_load_state("networkidle")
        context.storage_state(path=str(state_file))
        return state_file
    finally:
        context.close()


@pytest.fixture
def school_page(browser: Browser, school_session_state: Path) -> Page:
    """Tạo Browser Context với session Cán bộ trường đã đăng nhập và bypass SSL."""
    context = browser.new_context(
        storage_state=str(school_session_state),
        ignore_https_errors=True,
        viewport={"width": 1280, "height": 800},
    )
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture
def pom(school_page: Page) -> ClassManagementPage:
    """Page Object Model cho Class Management."""
    return ClassManagementPage(school_page)


# ---------------------------------------------------------------------------
# NHÓM 1: FUNCTION FLOW & TÁI SỬ DỤNG LỚP HỌC (UAT 3.1 CORE)
# ---------------------------------------------------------------------------

@pytest.mark.flow
@pytest.mark.p0
def test_tc_cls_31_001_verify_existing_primary1_class_for_step_32(school_page: Page, pom: ClassManagementPage):
    """
    Kịch bản 3.1: Kiểm tra xem trong bảng đã có lớp P1-A (hoặc lớp thuộc khối Primary 1) chưa.
    Kỳ vọng: Lớp P1-A đã tồn tại trong danh sách, có thể sử dụng ngay để chuyển sang mục 3.2.
    """
    pom.open(BASE_URL)
    expect(school_page.get_by_role("heading", name="Class Management")).to_be_visible()

    # Tìm kiếm lớp P1-A
    pom.search_input.fill("P1-A")
    pom.search_button.click()
    school_page.wait_for_load_state("networkidle")

    # Kiểm tra dòng kết quả của lớp P1-A
    row = pom.table_rows.filter(has_text="P1-A").first
    expect(row).to_be_visible()
    expect(row).to_contain_text("Primary 1")
    expect(row).to_contain_text("2026")

    # Chụp ảnh minh chứng thực tế
    evidence_dir = Path("/tmp/reports/uat_3_1")
    evidence_dir.mkdir(parents=True, exist_ok=True)
    school_page.screenshot(path=str(evidence_dir / "actual_result_tc_cls_31_001_p1a_found.png"))


# ---------------------------------------------------------------------------
# NHÓM 2: VALIDATION FORM TẠO LỚP HỌC (/class-management/new)
# ---------------------------------------------------------------------------

@pytest.mark.validation
@pytest.mark.p1
def test_tc_cls_31_002_create_form_mandatory_field_validation(school_page: Page, pom: ClassManagementPage):
    """
    Kịch bản 3.1: Mở form tạo lớp và kiểm tra validate bắt buộc khi để trống toàn bộ thông tin.
    Kỳ vọng: Các trường Class code, Class name, Level offering bật viền đỏ aria-invalid và thông báo lỗi.
    """
    pom.open_create(BASE_URL)
    expect(school_page.get_by_role("heading", name="Create a class")).to_be_visible()

    # Nhấn Create class khi form rỗng
    pom.submit_btn.click()

    # Kiểm tra thuộc tính aria-invalid
    expect(pom.class_code_input).to_have_attribute("aria-invalid", "true")
    expect(pom.class_name_input).to_have_attribute("aria-invalid", "true")

    # Kiểm tra text thông báo lỗi inline thực tế
    expect(school_page.locator("#class-classCode-error")).to_contain_text("Class code is required.")
    expect(school_page.locator("#class-className-error")).to_contain_text("Class name is required.")
    expect(school_page.locator("#class-schoolLevelOffering-error")).to_contain_text("Select a school level offering.")


@pytest.mark.validation
@pytest.mark.br
@pytest.mark.p0
def test_tc_cls_31_003_duplicate_class_code_p1a_rejected(school_page: Page, pom: ClassManagementPage):
    """
    Kịch bản 3.1 & BR: Kiểm tra ràng buộc duy nhất - Từ chối tạo trùng mã lớp P1-A đã có.
    Kỳ vọng: Hệ thống hiển thị Alert 'Unable to create class' kèm nội dung 'Class code 'P1-A' already exists for this offering.'
    """
    pom.open_create(BASE_URL)
    expect(school_page.get_by_role("heading", name="Create a class")).to_be_visible()

    # Nhập thông tin trùng lặp với lớp P1-A đã tồn tại
    pom.class_code_input.fill("P1-A")
    pom.class_name_input.fill("Primary 1-A Duplicate")
    
    # Chọn cấp học Primary 1 · 2026
    pom.offering_combobox.click()
    primary_1_option = school_page.get_by_role("option", name=re.compile(r"Primary 1 · 2026", re.IGNORECASE))
    expect(primary_1_option).to_be_visible()
    primary_1_option.click()

    # Gửi form
    pom.submit_btn.click()

    # Xác nhận hiển thị thông báo lỗi trùng lặp
    expect(pom.create_error).to_be_visible()
    expect(school_page.get_by_text("Class code 'P1-A' already exists for this offering.")).to_be_visible()
    expect(school_page).to_have_url(re.compile(r"/class-management/new$"))


# ---------------------------------------------------------------------------
# NHÓM 3: LUỒNG TẠO MỚI THÀNH CÔNG VỚI MÃ DUY NHẤT (HAPPY PATH)
# ---------------------------------------------------------------------------

@pytest.mark.flow
@pytest.mark.p1
def test_tc_cls_31_004_create_unique_primary1_class_success(school_page: Page, pom: ClassManagementPage):
    """
    Kịch bản 3.1 (Khi chưa có): Điền thông tin hợp lệ -> Bấm Create class -> Tạo thành công.
    Kỳ vọng: Tạo thành công, điều hướng về /class-management và lớp mới xuất hiện trên bảng.
    """
    pom.open_create(BASE_URL)
    expect(school_page.get_by_role("heading", name="Create a class")).to_be_visible()

    suffix = str(time.time_ns())[-6:]
    unique_code = f"P1-AUTO{suffix}"
    unique_name = f"Primary 1 Auto {suffix}"

    pom.class_code_input.fill(unique_code)
    pom.class_name_input.fill(unique_name)

    # Chọn Primary 1 · 2026
    pom.offering_combobox.click()
    primary_1_option = school_page.get_by_role("option", name=re.compile(r"Primary 1 · 2026", re.IGNORECASE))
    primary_1_option.click()

    # Gửi form tạo lớp
    pom.submit_btn.click()

    # Chờ điều hướng về danh sách lớp
    school_page.wait_for_url("**/class-management", timeout=15000)
    expect(school_page.get_by_role("heading", name="Class Management")).to_be_visible()

    # Tìm kiếm lớp vừa tạo trên bảng
    pom.search_input.fill(unique_code)
    pom.search_button.click()
    school_page.wait_for_load_state("networkidle")

    # Xác nhận lớp mới hiển thị với sĩ số ban đầu là 0
    new_row = pom.table_rows.filter(has_text=unique_code).first
    expect(new_row).to_be_visible()
    expect(new_row.locator("td:nth-child(5)")).to_have_text("0")
    expect(new_row.locator("td:nth-child(6)")).to_have_text("0")


# ---------------------------------------------------------------------------
# NHÓM 4: CHI TIẾT LỚP HỌC VÀ ROSTER
# ---------------------------------------------------------------------------

@pytest.mark.ac
@pytest.mark.p2
def test_tc_cls_31_005_verify_class_p1a_detail_and_roster(school_page: Page, pom: ClassManagementPage):
    """
    Kịch bản 3.1 & AC: Mở xem chi tiết lớp P1-A để sẵn sàng cho phân bổ học sinh ở mục 3.2.
    Kỳ vọng: Hiển thị đúng mã lớp P1-A, Niên khóa 2026, Cấp học Primary 1, Bảng danh sách học sinh.
    """
    pom.open(BASE_URL)
    pom.search_input.fill("P1-A")
    pom.search_button.click()
    school_page.wait_for_load_state("networkidle")

    # Bấm nút Detail
    detail_btn = pom.table_rows.filter(has_text="P1-A").first.get_by_role("button", name="Detail")
    expect(detail_btn).to_be_visible()
    detail_btn.click()

    # Xác nhận màn hình chi tiết
    school_page.wait_for_url("**/class-management/*", timeout=15000)
    expect(school_page.get_by_role("button", name="Back to classes")).to_be_visible()
    expect(school_page.get_by_text("Primary 1 · Academic year 2026")).to_be_visible()
    expect(school_page.get_by_label("Class overview")).to_be_visible()
    expect(school_page.get_by_text("0 students in roster")).to_be_visible()
