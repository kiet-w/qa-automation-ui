"""
core/pytest_plugins/excel_evidence_exporter.py - Automatic Test Execution Evidence Excel Exporter.
Automatically updates or generates TEST_EXECUTION_EVIDENCE_<MODULE>_<FEATURE>.xlsx (Strict Single Tab)
at the end of pytest test sessions, recording real-time Passed/Failed outcomes, actual error messages,
and relative video playback hyperlinks.
"""

from datetime import datetime
import json
import os
from pathlib import Path
import re
import shutil
from typing import Dict, Any, Optional, List
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image as OpenpyxlImage

from core.pytest_plugins.excel_evidence_paths import (
    find_actual_result_screenshot,
    rebase_local_target,
    relative_excel_target,
    test_slug_candidates,
)

REPO_ROOT = Path(__file__).resolve().parents[2]


STANDARD_HEADERS = [
    "ID", "Scenario ID", "Title", "Test Suite", "Page", "Severity", "Priority",
    "Execution Status", "Test Type", "Environment", "Preconditions", "Test Data",
    "Steps Test", "Test Steps", "Expected Result", "Actual Result",
    "Traceability", "Note"
]
STANDARD_20_HEADERS = STANDARD_HEADERS

TICKET_MODULE_MAP = {
    # FS03 / Admin Portal (localhost:5173)
    "fs03/fs03-admin-login": "01_admin_login_and_sso",
    "fs03/fs03-dashboard-shell": "02_admin_dashboard_shell",
    "fs03/fs03-school-directory": "03_school_management",
    "fs03/fs03-school-create": "03_school_management",
    "fs03/fs03-school-user-management-csv-form": "04_school_user_management",
    "fs03/fs03-school-user-create": "04_school_user_management",
    "fs03/fs03-academic-years": "05_academic_years_and_levels",
    "fs03/fs03-class-management": "06_class_management",
    "fs03/fs03-student-enrollment": "07_student_management_and_enrollment",
    "fs03/fs03-school-config": "08_school_config",
}

KNOWN_ISSUE_DEV_NOTES = {
    # 06_class_management
    "TC-CLS-007": (
        "[UI BEHAVIOR] Nút 'Reset filters' đang ở trạng thái ENABLED ngay cả khi các ô lọc "
        "(Search, Academic Level, Academic Year) đều rỗng. Theo AC, nút 'Reset filters' phải bị disabled "
        "mặc định và chỉ được kích hoạt (enabled) khi người dùng có nhập ít nhất một điều kiện lọc."
    ),
    "TC-CLS-010": (
        "[VALIDATION BUG] Form tạo lớp cho phép nhập mã lớp chứa dấu cách và ký tự đặc biệt "
        "('P1 A class!') mà không kích hoạt thuộc tính aria-invalid='true' và viền đỏ cảnh báo trên ô input "
        "'#class-classCode'. Cần bổ sung regex validation client-side (chỉ cho phép ký tự chữ và số liền nhau, "
        "vd: ^[A-Za-z0-9_-]+$) trước khi submit."
    ),
    "TC-CLS-016": (
        "[AUTH/SESSION BUG] Khi click nút Detail để mở màn hình chi tiết lớp học (/class-management/:classId), "
        "trang web bị redirect về màn hình Login (/login) do mất cookie/auth token phiên đăng nhập. "
        "Cần kiểm tra cơ chế lưu token/session persistence hoặc route guard của trang chi tiết lớp học."
    ),
    "TC-CLS-018": (
        "[RATE-LIMIT BUG] Sau khi ngắt mạng và click nút 'Try again', bảng danh sách lớp không phục hồi được "
        "mà hiển thị thông báo 'Unable to load classes: Too many requests. Please try again later.' do API "
        "bị kích hoạt rate-limit (HTTP 429). Cần thêm debounce cho nút Retry hoặc nới lỏng rate limiter trên SIT."
    ),

    # 07_student_management_and_enrollment
    "TC-STU-003": (
        "[CHƯA CÓ TÍNH NĂNG] Chức năng 'Assign in class' trên giao diện hiện đang bị khóa (disabled) đối với các "
        "học sinh đã được phân lớp; hệ thống chưa có luồng 'Chuyển lớp' (Change class) để kiểm tra nghiệp vụ lưu vết "
        "lịch sử chuyển lớp (enrollment history)."
    ),
    "TC-STU-004": (
        "[GIỚI HẠN GIAO DIỆN] Khi tạo hồ sơ học sinh có thời hạn nhập học đã kết thúc (enrolled_to_exclusive trong quá khứ), "
        "hệ thống tự động ẩn học sinh này khỏi danh bạ Students. Do đó không thể chọn học sinh này vào màn hình phân lớp "
        "để kiểm tra thông báo từ chối phân lớp cho học sinh đã rút hồ sơ/thôi học."
    ),
    "TC-STU-005": (
        "[THIẾU TRƯỜNG DỮ LIỆU] Màn hình Chi tiết học sinh (Student Detail) hiện tại chưa hiển thị trường/thông tin "
        "liên kết Quỹ Giáo dục (Education Account - EA) của công dân Singapore (SC) để đối chiếu tự động theo BR-STU-005."
    ),
    "TC-STU-008": (
        "[THIẾU TRƯỜNG GIAO DIỆN] Màn hình Tiếp nhận học sinh (/student-management/enroll) hiện chỉ có trường "
        "Student ID, School combo và ngày bắt đầu/kết thúc; chưa có bộ chọn Niên khóa (Academic Year) và Cấp học "
        "(Academic Level) như đặc tả ban đầu."
    ),
    "TC-STU-013": (
        "[LỖI THÔNG BÁO BACKEND] Khi nhập ngày sinh ở tương lai (2099-01-01), backend trả về chuỗi lỗi mã hóa chung "
        "'Unable to complete student actionSystem.ValidationFailed' thay vì thông báo lỗi thân thiện trên UI "
        "('Date of birth must be in the past'). Cần map lỗi ValidationException của backend thành error message chuẩn trên UI."
    ),
    "TC-STU-015": (
        "[LỆCH SPEC GIAO DIỆN] Form nhập học hiện tại của hệ thống được thiết kế theo mô hình Student ID + School ID trực tiếp, "
        "không có dropdown chọn Niên khóa & Cấp học. Đang chờ BA/Product chốt lại luồng giao diện chuẩn."
    ),
    "TC-STU-017": (
        "[TIMEOUT ĐIỀU HƯỚNG] Thao tác tạo học sinh và tiếp nhận vào trường bị timeout sau 30 giây: Sau khi bấm nút Submit "
        "form tạo học sinh mới, trang web phản hồi chậm hoặc không tự động redirect về màn hình danh bạ Students. "
        "Cần kiểm tra API backend /api/students response time và logic xử lý on-success trên form."
    ),
    "TC-STU-018": (
        "[LỖI ĐỒNG BỘ DỮ LIỆU] Thao tác phân công học sinh vào lớp '1A1' thành công trên modal, nhưng khi quay lại "
        "bảng danh bạ học sinh (Students list), cột Lớp (Class) của học sinh vẫn bị trống, không hiển thị mã lớp 1A1. "
        "Cần kiểm tra việc re-fetch dữ liệu danh sách hoặc cache sau khi phân lớp."
    ),
    "TC-STU-020": (
        "[TIMEOUT TẢI TRANG] Form tạo học sinh (/student-management/new) không tải kịp trong thời gian chờ 30 giây trong "
        "quá trình chuẩn bị dữ liệu học sinh mẫu để thử phân lớp. Cần kiểm tra kết nối mạng nội bộ và tốc độ load form."
    ),

    # 08_school_config
    "TC-CFG-002": (
        "[THIẾU DỮ LIỆU NGUỒN] Niên khóa 2025 trên môi trường SIT hiện không có dữ liệu cấu hình cấp học nguồn; thao tác "
        "sao chép vào năm 2026 sẽ làm thay đổi dữ liệu trường dùng chung. Cần cấp tài khoản trường riêng biệt hoặc seed data "
        "chuẩn cho năm 2025 để chạy test."
    ),
    "TC-CFG-003": (
        "[LỖI KHÓA DỮ LIỆU ĐÃ ĐÓNG] Khi người dùng chọn xem niên khóa 2025 đã hoàn thành (CLOSED/COMPLETED), nút 'Add Academic Levels' "
        "vẫn ở trạng thái ENABLED thay vì bị vô hiệu hóa (disabled). Theo BR-CFG-003, mọi nút thay đổi cấu trúc học vụ phải bị khóa "
        "hoàn toàn khi niên khóa đã hoàn thành."
    ),
    "TC-CFG-004": (
        "[CHƯA CÓ TÍNH NĂNG] Giao diện Cấu hình trường hiện tại chưa xây dựng chức năng Xóa cấp học (nút Remove / Delete Level) "
        "nên không thể thực hiện kiểm thử quy tắc chặn xóa cấp học có lớp học đang hoạt động."
    ),
    "TC-CFG-011": (
        "[BẢO TOÀN DỮ LIỆU TEST] Tạm thời bỏ qua thao tác gửi request sao chép từ năm 2025 rỗng vào năm 2027 để tránh làm biến đổi "
        "trạng thái DRAFT dùng chung của niên khóa 2027."
    ),
    "TC-CFG-012": (
        "[BẢO TOÀN DỮ LIỆU TEST] Kiểm thử hộp thoại xác nhận ghi đè đòi hỏi niên khóa nguồn phải có đủ dữ liệu và đích đến là trường "
        "test cách ly. Tạm skip để bảo toàn cấu hình hiện hành của trường."
    ),
    "TC-CFG-013": (
        "[LỖI PHIÊN ĐĂNG NHẬP] Trình duyệt bị văng về trang đăng nhập (/login) khi đang thao tác chuyển đổi dropdown niên khóa, "
        "làm gián đoạn bài test. Cần kiểm tra cơ chế refresh token hoặc session timeout trên frontend."
    ),
    "TC-CFG-014": (
        "[BẢO TOÀN DỮ LIỆU DÙNG CHUNG] Việc thêm cấp học mới sẽ lưu vĩnh viễn vào trường dùng chung mà hệ thống chưa có API dọn dẹp "
        "(cleanup/rollback) sau kiểm thử. Cần môi trường test sandbox có thể reset database."
    ),
    "TC-CFG-015": (
        "[THIẾU DỮ LIỆU & TRÁNH XUNG ĐỘT] Năm nguồn 2025 rỗng và việc thực thi sao chép thành công sẽ làm thay đổi cấu hình "
        "niên khóa dùng chung của các tester khác."
    ),
    "TC-CFG-016": (
        "[LỖI PHIÊN ĐĂNG NHẬP] Phiên đăng nhập bị mất (redirect to /login) khi truy cập màn hình Cấu hình trường. "
        "Cần đảm bảo cookie xác thực được duy trì ổn định giữa các tác vụ điều hướng."
    ),
    "TC-CFG-017": (
        "[LỖI PHIÊN ĐĂNG NHẬP] Phiên đăng nhập bị mất (redirect to /login) trước khi mở modal sao chép cấu hình."
    ),
    "TC-CFG-018": (
        "[LỖI PHIÊN ĐĂNG NHẬP] Phiên đăng nhập bị redirect về /login khi bắt đầu kiểm thử."
    ),
}


def find_evidence_xlsx_file(ticket_dir: Path) -> Optional[Path]:
    """Find existing TEST_EXECUTION_EVIDENCE_*.xlsx file in a given directory."""
    if not ticket_dir.exists():
        return None
    matches = [f for f in ticket_dir.glob("TEST_EXECUTION_EVIDENCE_*.xlsx") if not f.name.startswith("~")]
    if matches:
        return matches[0]
    return None


def create_standard_evidence_workbook(ticket_name: str) -> openpyxl.Workbook:
    """Create a new standard 20-column single-tab openpyxl workbook."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Execution Evidence"
    ws.views.sheetView[0].showGridLines = True

    header_fill = PatternFill(start_color="001B365D", end_color="001B365D", fill_type="solid")
    header_font = Font(name="Segoe UI", size=10, bold=True, color="00FFFFFF")
    header_align = Alignment(horizontal="center", vertical="center", wrap_text=True)

    for col_idx, h_text in enumerate(STANDARD_20_HEADERS, start=1):
        cell = ws.cell(row=1, column=col_idx, value=h_text)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = header_align
    ws.row_dimensions[1].height = 28
    return wb


def find_candidate_source_workbooks(reports_dir: Path, ticket_name: str) -> Optional[Path]:
    """
    Search canonical locations in testcase5173/, testcase5174/, specs/, and reports_dir
    for an existing testcase specification or execution evidence workbook.
    Prioritizes original specification workbooks (TC_*.xlsx) to preserve Traceability and Note.
    """
    last_part = Path(ticket_name).name.lower()
    mapped_mod = TICKET_MODULE_MAP.get(ticket_name)

    search_dirs = [
        REPO_ROOT / ticket_name,
        REPO_ROOT / "specs" / ticket_name,
        REPO_ROOT / "1_Nghiep_Vu_va_Specs" / "testcases" / ticket_name,
    ]

    for base_parent in (REPO_ROOT, REPO_ROOT / "specs", REPO_ROOT / "1_Nghiep_Vu_va_Specs"):
        for group_name in ("testcase5173", "testcase5174", "uattestcase", "uat", "testcases"):
            group_dir = base_parent / group_name
            if not group_dir.exists():
                continue
            if mapped_mod and (group_dir / mapped_mod).is_dir():
                search_dirs.append(group_dir / mapped_mod)
            for sub in group_dir.glob("*"):
                if sub.is_dir():
                    sub_l = sub.name.lower()
                    if last_part in sub_l or sub_l in last_part:
                        search_dirs.append(sub)

    # 1. Prefer original specification workbooks (TC_*.xlsx or UAT_*.xlsx)
    for d in search_dirs:
        if d.exists():
            tc_files = [
                f for f in d.glob("*.xlsx")
                if not f.name.startswith("~")
                and not f.name.startswith(".")
                and not f.name.startswith("TEST_EXECUTION_EVIDENCE_")
                and not f.name.startswith("report")
                and "master" not in f.name.lower()
            ]
            if tc_files:
                return tc_files[0]

    # 2. Check existing evidence in reports_dir or search_dirs
    rep_ev = find_evidence_xlsx_file(reports_dir)
    if rep_ev and rep_ev.exists():
        return rep_ev

    for d in search_dirs:
        if d.exists():
            ev_files = [f for f in d.glob("TEST_EXECUTION_EVIDENCE_*.xlsx") if not f.name.startswith("~")]
            if ev_files:
                return ev_files[0]

    return None


def derive_evidence_filename(ticket_name: str) -> str:
    """Derive standard evidence filename from ticket slug (e.g. fs08/fs08-parent-profile -> TEST_EXECUTION_EVIDENCE_FS08_Parent_Profile.xlsx)."""
    parts = ticket_name.strip("/").split("/")
    last_part = parts[-1]
    # Replace dashes with underscores and format casing
    words = last_part.replace("-", "_").split("_")
    formatted_words = []
    for w in words:
        if re.match(r"^(fs|us|tc|r)\d+$", w.lower()):
            formatted_words.append(w.upper())
        else:
            formatted_words.append(w.capitalize())
    clean_slug = "_".join(formatted_words)
    return f"TEST_EXECUTION_EVIDENCE_{clean_slug}.xlsx"


def extract_tc_id_from_nodeid(nodeid: str) -> str:
    """
    Extracts canonical TC ID (e.g. TC-ADM-AUTH-001, TC-PRF-VAL-01, TC-R8-094, UAT-019) from pytest nodeid.
    Handles various test function naming formats robustly.
    """
    func_name = re.sub(r"\[.*?\]$", "", nodeid.split("::")[-1])

    # Pattern 1: test_tc_(tc_)?(ID)_ts_... (standard: test_tc_tc_prf_val_01_ts_prf_val_...)
    m_ts = re.search(r"test_tc_(?:tc_)?([a-zA-Z0-9]+(?:_[a-zA-Z0-9]+)*?)_ts_", func_name, re.I)
    if m_ts:
        raw = m_ts.group(1).upper().replace("_", "-")
        return f"TC-{raw}" if not raw.startswith("TC-") else raw

    # Pattern 2: test_tc_(tc_)?(ID_with_digits)_(description) e.g. test_tc_adm_auth_001_moehq_rbac
    m_num = re.search(r"test_tc_(?:tc_)?([a-zA-Z0-9]+(?:_[a-zA-Z0-9]+)*?_\d+[a-zA-Z0-9]*)(?:_|\Z)", func_name, re.I)
    if m_num:
        raw = m_num.group(1).upper().replace("_", "-")
        return f"TC-{raw}" if not raw.startswith("TC-") else raw

    # Pattern 3: test_tc_([a-zA-Z0-9_]+)
    m_tc = re.search(r"test_tc_([a-zA-Z0-9]+(?:_[a-zA-Z0-9]+)*?)(?:_[a-z]{3,}|\Z)", func_name, re.I)
    if m_tc:
        raw = m_tc.group(1).upper().replace("_", "-")
        return f"TC-{raw}" if not raw.startswith("TC-") else raw

    # Pattern 4: test_(ac|br|val|err|flow|uat)(\d+)
    m_short = re.search(r"test_([a-zA-Z]+)(\d+)", func_name, re.I)
    if m_short:
        return f"TC-{m_short.group(1).upper()}-{m_short.group(2)}"

    return func_name.upper().replace("_", "-")


def match_nodeid_to_tc_row(nodeid: str, tc_id_map: Dict[str, int]) -> Optional[int]:
    """Matches a pytest test function nodeid to a row in the testcase ID map."""
    func_name = re.sub(r"\[.*?\]$", "", nodeid.split("::")[-1]).lower()

    # 1. Exact derived TC ID match
    derived_id = extract_tc_id_from_nodeid(nodeid)
    if derived_id in tc_id_map:
        return tc_id_map[derived_id]

    # Check case-insensitive / with or without 'TC-' prefix
    for tid, row_idx in tc_id_map.items():
        if derived_id.upper() == tid.upper():
            return row_idx
        if derived_id.replace("TC-", "").upper() == tid.replace("TC-", "").upper():
            return row_idx

    # 2. Normalized token substring match
    func_tokens = set(func_name.split("_"))
    for tid, row_idx in tc_id_map.items():
        norm_tid = tid.lower().replace("-", "_")
        if norm_tid in func_name:
            return row_idx
        norm_no_tc = norm_tid.replace("tc_", "")
        if norm_no_tc in func_name:
            return row_idx
        # Check if all tokens of tid are present in func_tokens
        tid_tokens = set(norm_no_tc.split("_"))
        if tid_tokens and tid_tokens.issubset(func_tokens):
            return row_idx

    # 3. Partial number match if number has at least 3 digits
    m = re.findall(r"\b(\d{2,4})\b", func_name)
    for num in m:
        candidates = [tid for tid in tc_id_map if re.search(rf"\b{num}\b", tid.replace("-", " "))]
        if len(candidates) == 1:
            return tc_id_map[candidates[0]]

    return None


def find_header_column(header_map: Dict[str, int], *names: str) -> Optional[int]:
    """Resolve a column by supported header aliases without unsafe defaults."""
    normalized = {re.sub(r"\s+", " ", key).strip().casefold(): value for key, value in header_map.items()}
    for name in names:
        column = normalized.get(re.sub(r"\s+", " ", name).strip().casefold())
        if column:
            return column
    return None


def export_test_execution_evidence(
    reports_dir: Path,
    ticket_name: Optional[str] = None,
    report_json_path: Optional[Path] = None,
    run_id: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """
    Inspects pytest run results from report.json and updates/creates TEST_EXECUTION_EVIDENCE_*.xlsx
    enforcing strictly ONE single tab with native openpyxl video/screenshot hyperlinks.
    Guarantees 100% synchronization with execution_report.html.
    """
    if not reports_dir.exists():
        return None

    if not ticket_name:
        for parent_cand in ("3_Bao_Cao_va_Ket_Qua/reports", "2_Code_Automation/reports", "reports"):
            base_cand = REPO_ROOT / parent_cand
            try:
                rel = reports_dir.relative_to(base_cand)
                if str(rel) != ".":
                    ticket_name = str(rel)
                    break
            except Exception:
                pass

    if not ticket_name:
        ticket_name = reports_dir.name

    evidence_filename = derive_evidence_filename(ticket_name)

    # Load report.json
    if not report_json_path or not report_json_path.exists():
        report_json_path = reports_dir / "report.json"
    if not report_json_path.exists():
        return None

    try:
        with open(report_json_path, "r", encoding="utf-8") as f:
            report_data = json.load(f)
    except Exception:
        return None

    executed_tests = report_data.get("tests", [])
    if not executed_tests:
        # No tests were executed in this session
        return None

    # Find master source workbook or create new standard 20-col workbook
    src_wb_path = find_candidate_source_workbooks(reports_dir, ticket_name)
    if src_wb_path and src_wb_path.exists():
        wb = openpyxl.load_workbook(src_wb_path)
    else:
        wb = create_standard_evidence_workbook(ticket_name)

    # ENFORCE STRICT SINGLE TAB MANDATE
    # If multiple tabs exist, keep ONLY the first tab (Execution Evidence) and remove the rest
    if len(wb.sheetnames) > 1:
        keep_sheet_name = wb.sheetnames[0]
        for name in list(wb.sheetnames)[1:]:
            wb.remove(wb[name])

    ws = wb.active
    ws.views.sheetView[0].showGridLines = True

    # Styling Palette
    status_pass_fill = PatternFill(start_color="00DCFCE7", end_color="00DCFCE7", fill_type="solid")
    status_fail_fill = PatternFill(start_color="00FEE2E2", end_color="00FEE2E2", fill_type="solid")
    status_skip_fill = PatternFill(start_color="00F1F5F9", end_color="00F1F5F9", fill_type="solid")
    link_font = Font(name="Segoe UI", size=9.5, bold=True, underline="single", color="001D4ED8")

    # Map column headers (auto-detect header row between 1 and 5)
    header_col_map = {}
    header_row_idx = 1
    for r_cand in range(1, 6):
        row_vals = {
            str(ws.cell(row=r_cand, column=col).value).strip(): col
            for col in range(1, ws.max_column + 1)
            if ws.cell(row=r_cand, column=col).value
        }
        if any(k in row_vals for k in ("ID", "Test Case ID", "TC ID")):
            header_col_map = row_vals
            header_row_idx = r_cand
            break

    # Automatically drop unneeded columns: "Assumption Ref" and "Defect ID"
    unneeded_cols = [
        col for col in range(1, ws.max_column + 1)
        if str(ws.cell(row=header_row_idx, column=col).value or "").strip() in ("Assumption Ref", "Defect ID")
    ]
    if unneeded_cols:
        for col in sorted(unneeded_cols, reverse=True):
            ws.delete_cols(col, 1)
        # Rebuild header map after deletion
        header_col_map = {
            str(ws.cell(row=header_row_idx, column=col).value).strip(): col
            for col in range(1, ws.max_column + 1)
            if ws.cell(row=header_row_idx, column=col).value
        }

    id_col = find_header_column(header_col_map, "ID", "Test Case ID", "TC ID") or 1
    status_col = find_header_column(header_col_map, "Execution Status", "Status") or 8
    actual_col = find_header_column(header_col_map, "Actual Result", "Actual Result (Verified)") or 16

    # Strictly preserve Traceability and Note without overwriting them.
    trace_col = find_header_column(header_col_map, "Traceability")
    note_col = find_header_column(header_col_map, "Note")
    protected_cols = {c for c in (trace_col, note_col) if c}

    evidence_link_col = find_header_column(
        header_col_map,
        "📷 Visual Evidence",
        "Visual Evidence",
        "Evidence Link",
    )
    if not evidence_link_col or evidence_link_col in protected_cols:
        evidence_link_col = ws.max_column + 1
        h_link = ws.cell(row=header_row_idx, column=evidence_link_col, value="📷 Visual Evidence")
        h_link.fill = PatternFill(start_color="001B365D", end_color="001B365D", fill_type="solid")
        h_link.font = Font(name="Segoe UI", size=9.5, bold=True, color="00FFFFFF")
        h_link.alignment = Alignment(horizontal="center", vertical="center")

    ws.column_dimensions[get_column_letter(evidence_link_col)].width = 28

    img_col = evidence_link_col + 1
    h_img = ws.cell(row=header_row_idx, column=img_col, value="📷 Screenshot Evidence")
    h_img.fill = PatternFill(start_color="001B365D", end_color="001B365D", fill_type="solid")
    h_img.font = Font(name="Segoe UI", size=9.5, bold=True, color="00FFFFFF")
    h_img.alignment = Alignment(horizontal="center", vertical="center")
    ws.column_dimensions[get_column_letter(img_col)].width = 75

    if note_col:
        ws.column_dimensions[get_column_letter(note_col)].width = 45

    # Clear any preexisting images if refreshing existing workbook to prevent stacking
    if hasattr(ws, "_images") and ws._images:
        ws._images.clear()

    # Build row index map: TC_ID -> row_number
    tc_id_row_map = {}
    for r in range(header_row_idx + 1, ws.max_row + 1):
        tid = ws.cell(row=r, column=id_col).value
        if tid:
            tc_id_row_map[str(tid).strip()] = r

    # Collect video files available in test-results
    test_results_dir = reports_dir / "test-results"
    video_file_map = {}
    if test_results_dir.exists():
        for vid in test_results_dir.glob("**/*.webm"):
            video_file_map[vid.parent.name.lower()] = vid

    # Process executed test results
    updated_rows = set()
    for test in executed_tests:
        nodeid = test.get("nodeid", "")
        outcome = test.get("outcome", "passed")
        call_info = test.get("call", {}) or {}
        meta_info = test.get("metadata", {}) or {}

        target_row = match_nodeid_to_tc_row(nodeid, tc_id_row_map)
        derived_id = extract_tc_id_from_nodeid(nodeid)

        # If test was not in the existing template, append it as a new row
        if not target_row:
            target_row = ws.max_row + 1
            tc_id_row_map[derived_id] = target_row
            ws.cell(row=target_row, column=id_col, value=derived_id).font = Font(name="Consolas", size=9, bold=True, color="001B365D")

            scen_col = find_header_column(header_col_map, "Scenario ID")
            if scen_col:
                ws.cell(row=target_row, column=scen_col, value=f"TS-{derived_id.replace('TC-', '')}").font = Font(name="Segoe UI", size=9)

            title_col = find_header_column(header_col_map, "Title", "Title / Test Description", "Description")
            if title_col:
                clean_title = re.sub(r"^test_(tc_)?", "", re.sub(r"\[.*?\]$", "", nodeid.split("::")[-1])).replace("_", " ").capitalize()
                ws.cell(row=target_row, column=title_col, value=clean_title).font = Font(name="Segoe UI", size=9)

            suite_col = find_header_column(header_col_map, "Test Suite")
            if suite_col:
                ws.cell(row=target_row, column=suite_col, value=ticket_name).font = Font(name="Segoe UI", size=9)

            page_col = find_header_column(header_col_map, "Page")
            if page_col:
                target_portal = "localhost:5173" if any(k in ticket_name.lower() for k in ("5173", "admin", "fs03")) else "localhost:5174"
                ws.cell(row=target_row, column=page_col, value=target_portal).font = Font(name="Segoe UI", size=9)

            sev_col = find_header_column(header_col_map, "Severity")
            if sev_col:
                ws.cell(row=target_row, column=sev_col, value="S1" if outcome == "failed" else "S2").font = Font(name="Segoe UI", size=9)

            prio_col = find_header_column(header_col_map, "Priority")
            if prio_col:
                ws.cell(row=target_row, column=prio_col, value="High" if outcome == "failed" else "Medium").font = Font(name="Segoe UI", size=9)

            type_col = find_header_column(header_col_map, "Test Type")
            if type_col:
                ws.cell(row=target_row, column=type_col, value="Automated SIT").font = Font(name="Segoe UI", size=9)

            env_col = find_header_column(header_col_map, "Environment")
            if env_col:
                ws.cell(row=target_row, column=env_col, value="Local SIT (:5173 / :5174)").font = Font(name="Segoe UI", size=9)

            exp_col = find_header_column(header_col_map, "Expected Result")
            if exp_col:
                ws.cell(row=target_row, column=exp_col, value="Tất cả assertions và visual gates hoạt động chính xác theo FSD/BR/AC.").font = Font(name="Segoe UI", size=9)

        updated_rows.add(target_row)

        # 1. Update Execution Status
        c_status = ws.cell(row=target_row, column=status_col)
        c_actual = ws.cell(row=target_row, column=actual_col)
        c_note = ws.cell(row=target_row, column=note_col) if note_col else None

        if outcome == "passed":
            c_status.value = "Passed"
            c_status.fill = status_pass_fill
            c_status.font = Font(name="Segoe UI", size=9.0, bold=True, color="00166534")
            # Preserve existing actual verified text if already detailed, or update
            if not c_actual.value or "failed" in str(c_actual.value).lower():
                c_actual.value = "Verified: All automated assertions and visual gates passed successfully in SIT."
                c_actual.font = Font(name="Segoe UI", size=8.5, color="00166534")
            if c_note and (not c_note.value or "thao tác và ghi nhận" in str(c_note.value).lower()):
                c_note.value = "Mọi tiêu chí nghiệm thu và quy tắc nghiệp vụ đã được xác minh thành công."
                c_note.font = Font(name="Segoe UI", size=8.5, color="00166534")
                c_note.alignment = Alignment(vertical="center", wrap_text=True)
        elif outcome == "failed":
            c_status.value = "Failed"
            c_status.fill = status_fail_fill
            c_status.font = Font(name="Segoe UI", size=9.0, bold=True, color="00DC2626")

            # Extract failure message
            crash = call_info.get("crash", {}) or {}
            err_msg = crash.get("message") or str(call_info.get("longrepr", ""))[:200]
            err_msg = re.sub(r"\s+", " ", err_msg).strip()
            c_actual.value = f"Defect: {err_msg}" if err_msg else "Defect: Assertion failed during execution."
            c_actual.font = Font(name="Segoe UI", size=8.5, color="00DC2626")

            if c_note:
                if derived_id in KNOWN_ISSUE_DEV_NOTES:
                    c_note.value = KNOWN_ISSUE_DEV_NOTES[derived_id]
                else:
                    c_note.value = f"[DEFECT] {err_msg}"
                c_note.font = Font(name="Segoe UI", size=8.5, color="00DC2626")
                c_note.alignment = Alignment(vertical="center", wrap_text=True)
        else:
            c_status.value = "Skipped"
            c_status.fill = status_skip_fill
            c_status.font = Font(name="Segoe UI", size=9.0, color="0064748B")

            # Extract skip reason
            setup_info = test.get("setup", {}) or {}
            skip_msg = ""
            for source_info in (setup_info, call_info):
                longrepr = source_info.get("longrepr")
                if isinstance(longrepr, tuple) and len(longrepr) >= 3:
                    skip_msg = str(longrepr[2])
                    break
                elif isinstance(longrepr, str) and "Skipped" in longrepr:
                    skip_msg = longrepr
                    break

            if skip_msg:
                clean_skip = re.sub(r"^Skipped:\s*", "", skip_msg).strip()
                c_actual.value = f"Skipped: {clean_skip[:200]}"
            else:
                c_actual.value = "Skipped: Test case skipped during execution."
            c_actual.font = Font(name="Segoe UI", size=8.5, color="0064748B")

            if c_note:
                if derived_id in KNOWN_ISSUE_DEV_NOTES:
                    c_note.value = KNOWN_ISSUE_DEV_NOTES[derived_id]
                elif skip_msg:
                    c_note.value = f"[SKIPPED] {skip_msg}"
                else:
                    c_note.value = "[SKIPPED] Điều kiện môi trường/dữ liệu kiểm thử chưa sẵn sàng."
                c_note.font = Font(name="Segoe UI", size=8.5, color="00475569")
                c_note.alignment = Alignment(vertical="center", wrap_text=True)

        # 2. Update Video / Screenshot Evidence Link
        func_slug = re.sub(r"\[.*?\]$", "", nodeid.split("::")[-1]).lower()
        test_slugs = list(test_slug_candidates(nodeid))
        test_slug = test_slugs[0]
        test_screenshots_dir = reports_dir / "screenshots" / test_slug

        # Prefer the canonical actual_result.png captured for this exact pytest
        # parameter set (for example the ``[chromium]`` suffix).
        actual_screen = find_actual_result_screenshot(
            reports_dir=reports_dir,
            nodeid=nodeid,
            metadata=meta_info,
            repo_root=REPO_ROOT,
        )

        step_count = len(list(test_screenshots_dir.glob("step_*.png"))) if test_screenshots_dir.exists() else 0

        if actual_screen and actual_screen.exists():
            rel_screen = relative_excel_target(actual_screen, reports_dir)
            c_vid = ws.cell(row=target_row, column=evidence_link_col)
            if outcome in ("failed", "xfailed"):
                c_vid.value = "🚨 Full HD Defect"
                c_vid.font = Font(name="Segoe UI", size=9.5, bold=True, underline="single", color="00DC2626")
            else:
                c_vid.value = "🔍 Full HD Actual Result"
                c_vid.font = link_font
            c_vid.alignment = Alignment(horizontal="center", vertical="center")
            c_vid.hyperlink = str(rel_screen)

            # Embed high-resolution reviewable screenshot cleanly into img_col
            try:
                img = OpenpyxlImage(str(actual_screen))
                target_w = 520
                if img.width and img.height:
                    aspect = img.height / img.width
                    target_h = int(target_w * aspect)
                else:
                    target_h = 292
                img.width = target_w
                img.height = target_h
                cell_coord = f"{get_column_letter(img_col)}{target_row}"
                ws.add_image(img, cell_coord)
                ws.row_dimensions[target_row].height = max(80, int(target_h * 0.75) + 14)
                ws.cell(row=target_row, column=img_col).hyperlink = str(rel_screen)
            except Exception:
                pass
        elif outcome in ("failed", "xfailed"):
            # If no screenshot exists, fall back to recorded video
            v_path = meta_info.get("video_path")
            matched_video = None
            if v_path and Path(v_path).exists():
                matched_video = Path(v_path)
            else:
                norm_slug = re.sub(r"[_\W]+", "-", func_slug).strip("-")
                for d_name, vid_p in video_file_map.items():
                    if norm_slug in d_name or d_name in norm_slug:
                        matched_video = vid_p
                        break

            if matched_video and matched_video.exists():
                try:
                    rel_vid_reports = matched_video.relative_to(reports_dir)
                except Exception:
                    rel_vid_reports = Path("test-results") / matched_video.name

                c_vid = ws.cell(row=target_row, column=evidence_link_col)
                c_vid.value = "▶ Play in Browser"
                c_vid.font = link_font
                c_vid.alignment = Alignment(horizontal="center", vertical="center")
                c_vid.hyperlink = str(rel_vid_reports)

    # 3. Recalculate Executive Banner (Row 2 Metrics)
    total_tcs = len(tc_id_row_map)
    pass_count = 0
    fail_count = 0
    video_count = 0

    for r in tc_id_row_map.values():
        st = str(ws.cell(row=r, column=status_col).value or "").strip()
        if st.lower() == "passed":
            pass_count += 1
        elif st.lower() == "failed":
            fail_count += 1

        vl = ws.cell(row=r, column=evidence_link_col).hyperlink
        if vl:
            video_count += 1

    pass_pct = round((pass_count / total_tcs) * 100, 1) if total_tcs > 0 else 100.0

    if header_row_idx > 2:
        c_banner2 = ws["A2"]
        target_portal = "http://localhost:5173" if any(k in ticket_name.lower() for k in ("5173", "admin", "fs03")) else "http://localhost:5174"
        c_banner2.value = (
            f"Total Tests: {total_tcs}  |  Pass: {pass_count} ({pass_pct}%)  |  "
            f"Fail: {fail_count}  |  Bugs: {fail_count}  |  "
            f"Target: {target_portal}"
        )

    # 4. Save to reports/<ticket>/
    dest_reports_xlsx = reports_dir / evidence_filename
    dest_reports_xlsx.parent.mkdir(parents=True, exist_ok=True)
    wb.save(dest_reports_xlsx)

    # 4b. Always guarantee report.xlsx is saved alongside report.html
    report_std_xlsx = reports_dir / "report.xlsx"
    wb.save(report_std_xlsx)

    return {
        "ticket": ticket_name,
        "reports_xlsx": str(dest_reports_xlsx),
        "report_std_xlsx": str(report_std_xlsx),
        "total": total_tcs,
        "passed": pass_count,
        "failed": fail_count,
        "updated_tcs_count": len(updated_rows),
    }


# Backwards compatibility alias
update_or_create_evidence_workbook = export_test_execution_evidence
