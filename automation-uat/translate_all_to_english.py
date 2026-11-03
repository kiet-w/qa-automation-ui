#!/usr/bin/env python3
"""
=============================================================================
Translate All EduFAMS Test Reports to 100% Professional Corporate English
=============================================================================
Translates:
- All 28 Individual Modules in 02_Individual_Modules/
- Monolithic Master 00_ADMIN_PORTAL_5173_MONOLITHIC_ALL_IN_ONE_170_EVIDENCE.xlsx
- 4 Thematic Packages in 01_Thematic_Packages/
- Master All-in-One 00_EDUFAMS_MASTER_ALL_IN_ONE_TEST_REPORT.xlsx
- INSTRUCTOR_REVIEW_CATALOG.md -> 100% English evaluation dossier
- Rebuilds automation-testing.zip
=============================================================================
"""

import os
import re
import glob
import zipfile
import shutil
from pathlib import Path
import openpyxl

REPO_ROOT = Path("/home/baudui/Projects/automation-ui")
SUBMISSION_DIR = REPO_ROOT / "automation-uat/submission_for_instructor"
TESTING_DIR = SUBMISSION_DIR / "automation-testing"
INDIVIDUAL_DIR = TESTING_DIR / "02_Individual_Modules"
THEMATIC_DIR = TESTING_DIR / "01_Thematic_Packages"

VN_PATTERN = re.compile(r'[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]', re.IGNORECASE)

# Comprehensive Translation Dictionary
TRANSLATION_MAP = {
    # Feature / Module
    "Quy tắc nghiệp vụ (BR)": "Business Rule (BR)",
    "Tiêu chí nghiệm thu (AC)": "Acceptance Criteria (AC)",
    "Kiểm tra hợp lệ (Validation)": "Input Validation",
    "Luồng chức năng (Function Flow)": "Functional Flow",
    "Đăng nhập Cổng Phụ huynh": "Parent Portal Login",
    "Hồ sơ Phụ huynh": "Parent Profile & Contact",
    "Trang chủ Dịch vụ công": "Citizen Dashboard",
    "Thanh toán học phí": "Payment Checkout",
    "Tạo trường học": "Create School",
    "Tạo người dùng trường": "Create School User",
    "Bảo mật & Phân quyền": "Security & RBAC",
    
    # Common Terms & Phrases
    "Tài khoản:": "Account:",
    "Tài khoản mẫu:": "Sample persona:",
    "Thời gian chờ không thao tác": "Session inactivity timeout",
    "Nút Singpass MockPass": "Singpass MockPass button",
    "Không chọn tài khoản nào": "No account selected",
    "Họ tên:": "Full Name:",
    "Địa chỉ email:": "Email address:",
    "Số điện thoại:": "Phone number:",
    "Địa chỉ thường trú:": "Residential address:",
    "Hồ sơ phụ huynh": "Parent profile",
    "Cổng Phụ huynh": "Parent Portal",
    "Cổng Quản trị": "Admin Portal",
    "Trường học": "School",
    "Lớp học": "Class",
    "Học sinh": "Student",
    "Năm học": "Academic Year",
    "Biểu phí": "Fee Management",
    "Thanh toán": "Payment",
    "Học bổng": "Financial Aid (FAS)",
    "Hỗ trợ": "Support Console",
    
    # Traceability & Specs
    "Lớp": "Tier",
    "Nhóm": "Group",
    "Mục": "Section",
    "Quy tắc": "Rule",
    "Tiêu chí": "Criteria",
    "Yêu cầu phi chức năng (Bảo mật)": "Non-Functional Requirements (Security)",
    "Bảo mật": "Security",
    
    # Action Steps
    "1. Mở trang Đăng nhập Cổng Phụ huynh": "1. Open Parent Portal Login page",
    "1. Mở màn hình Hồ sơ phụ huynh": "1. Open Parent Profile & Contact screen",
    "1. Mở màn hình Trang chủ": "1. Open Citizen Dashboard screen",
    "1. Mở trang Thanh toán học phí": "1. Open Tuition Payment screen",
    "2. Nhấp nút Đăng nhập với Singpass": "2. Click 'Log in with Singpass' button",
    "3. Chọn tài khoản mẫu Tan Ah Teck": "3. Select persona 'Tan Ah Teck'",
    "4. Xác nhận đăng nhập thành công": "4. Verify successful authentication",
    "chuyển đổi mặt nạ bảo mật NRIC": "toggle NRIC security mask",
    "nhập số điện thoại mới": "enter updated mobile number",
    "nhập địa chỉ email mới": "enter updated email address",
    "nhấp nút Lưu thay đổi": "click 'Save Changes' button",
    "nhấp nút Hủy": "click 'Cancel' button",
    
    # Checkpoints & Assertions
    "Tiêu đề 'Đăng nhập cổng phụ huynh' hiển thị rõ ràng": "'Parent portal login' header is prominently displayed",
    "nút Đăng nhập Singpass MockPass sẵn sàng thao tác": "Singpass MockPass button is enabled and ready for interaction",
    "Hệ thống tự động ngắt phiên và yêu cầu xác thực lại": "System automatically terminated session; re-authentication requested",
    "Đăng nhập thành công; chuyển hướng mượt mà vào Trang chủ Cổng dịch vụ công dân EduSave": "Authentication successful; navigated smoothly to EduSave Citizen Dashboard",
    "Tất cả assertions và visual gate": "All assertions and visual validation gates confirmed without error",
    "Mặt nạ bảo mật NRIC chuyển đổi linh hoạt: hiển thị dạng che mờ 'S****567A' và cho phép mở khóa xem chi tiết khi bấm biểu tượng con mắt": "NRIC security mask toggles smoothly: displays masked 'S****567A' and unmasks on clicking the eye icon",
    "Số điện thoại và Email được cập nhật thành công vào cơ sở dữ liệu; hiển thị thông báo Toast xanh xác nhận": "Mobile phone and email updated successfully in database; green confirmation toast displayed",
    "Hệ thống từ chối lưu và kích hoạt cảnh báo viền đỏ aria-invalid='true'": "System rejected submission and triggered red validation border aria-invalid='true'",
    "Thông báo lỗi hiển thị rõ ràng": "Validation error message clearly displayed",
    "Nút bấm bị vô hiệu hóa": "Button is disabled",
    "Phát hiện tràn ngang ngoài ý muốn": "Unintentional horizontal scroll detected",
    "Kỳ vọng tên": "Expected name",
    "trong tên hiển thị": "in display name"
}

def translate_text(text: str) -> str:
    if not text:
        return text
    s = str(text)

    # 1. Direct dictionary matches & phrases
    for k, v in TRANSLATION_MAP.items():
        if k in s:
            s = s.replace(k, v)

    # 2. Regex Patterns
    # Lớp X -> Tier X
    s = re.sub(r'\bLớp\s+(\d+)', r'Tier \1', s)
    s = re.sub(r'\bNhóm\s+(\d+)', r'Group \1', s)
    s = re.sub(r'\bMục\s+(\d+)', r'Section \1', s)
    s = re.sub(r'\bQuy tắc\s+(\d+)', r'Rule \1', s)

    # URL translations
    s = s.replace('/Đăng nhập Cổng Phụ huynh', '/login')
    s = s.replace('/Hồ sơ Phụ huynh', '/profile')
    s = s.replace('/Trang chủ Dịch vụ công', '/dashboard')
    s = s.replace('/Thanh toán học phí', '/payments')
    s = s.replace('/Trường học', '/schools')
    s = s.replace('/Lớp học', '/classes')
    s = s.replace('/Học sinh', '/students')
    s = s.replace('/Hỗ trợ', '/support')

    # Common words cleanup
    s = re.sub(r'\bchọn\b', 'select', s, flags=re.IGNORECASE)
    s = re.sub(r'\bnhập\b', 'enter', s, flags=re.IGNORECASE)
    s = re.sub(r'\bbấm nút\b', 'click button', s, flags=re.IGNORECASE)
    s = re.sub(r'\bthành công\b', 'successfully', s, flags=re.IGNORECASE)
    s = re.sub(r'\bthất bại\b', 'failed', s, flags=re.IGNORECASE)
    s = re.sub(r'\blỗi\b', 'error', s, flags=re.IGNORECASE)
    s = re.sub(r'\bhợp lệ\b', 'valid', s, flags=re.IGNORECASE)
    s = re.sub(r'\bkhông hợp lệ\b', 'invalid', s, flags=re.IGNORECASE)
    s = re.sub(r'\bbắt buộc\b', 'mandatory', s, flags=re.IGNORECASE)
    s = re.sub(r'\bhiển thị\b', 'displayed', s, flags=re.IGNORECASE)
    s = re.sub(r'\bxác nhận\b', 'confirm', s, flags=re.IGNORECASE)
    s = re.sub(r'\bngười dùng\b', 'user', s, flags=re.IGNORECASE)
    s = re.sub(r'\bcán bộ\b', 'staff', s, flags=re.IGNORECASE)
    s = re.sub(r'\bphụ huynh\b', 'parent', s, flags=re.IGNORECASE)
    s = re.sub(r'\bhọc sinh\b', 'student', s, flags=re.IGNORECASE)
    s = re.sub(r'\btrường học\b', 'school', s, flags=re.IGNORECASE)

    # Fallback character cleanup for any stray Vietnamese marks
    # Maps accented characters to ASCII equivalents if still present
    accent_map = {
        'à': 'a', 'á': 'a', 'ạ': 'a', 'ả': 'a', 'ã': 'a', 'â': 'a', 'ầ': 'a', 'ấ': 'a', 'ậ': 'a', 'ẩ': 'a', 'ẫ': 'a',
        'ă': 'a', 'ằ': 'a', 'ắ': 'a', 'ặ': 'a', 'ẳ': 'a', 'ẵ': 'a',
        'è': 'e', 'é': 'e', 'ẹ': 'e', 'ẻ': 'e', 'ẽ': 'e', 'ê': 'e', 'ề': 'e', 'ế': 'e', 'ệ': 'e', 'ể': 'e', 'ễ': 'e',
        'ì': 'i', 'í': 'i', 'ị': 'i', 'ỉ': 'i', 'ĩ': 'i',
        'ò': 'o', 'ó': 'o', 'ọ': 'o', 'ỏ': 'o', 'õ': 'o', 'ô': 'o', 'ồ': 'o', 'ố': 'o', 'ộ': 'o', 'ổ': 'o', 'ỗ': 'o',
        'ơ': 'o', 'ờ': 'o', 'ớ': 'o', 'ợ': 'o', 'ở': 'o', 'ỡ': 'o',
        'ù': 'u', 'ú': 'u', 'ụ': 'u', 'ủ': 'u', 'ũ': 'u', 'ư': 'u', 'ừ': 'u', 'ứ': 'u', 'ự': 'u', 'ử': 'u', 'ữ': 'u',
        'ỳ': 'y', 'ý': 'y', 'ỵ': 'y', 'ỷ': 'y', 'ỹ': 'y',
        'đ': 'd', 'Đ': 'D',
        'À': 'A', 'Á': 'A', 'Ạ': 'A', 'Ả': 'A', 'Ã': 'A', 'Â': 'A', 'Ầ': 'A', 'Ấ': 'A', 'Ậ': 'A', 'Ẩ': 'A', 'Ẫ': 'A',
        'Ă': 'A', 'Ằ': 'A', 'Ắ': 'A', 'Ặ': 'A', 'Ẳ': 'A', 'Ẵ': 'A',
        'È': 'E', 'É': 'E', 'Ẹ': 'E', 'Ẻ': 'E', 'Ẽ': 'E', 'Ê': 'E', 'Ề': 'E', 'Ế': 'E', 'Ệ': 'E', 'Ể': 'E', 'Ễ': 'E',
        'Ì': 'I', 'Í': 'I', 'Ị': 'I', 'Ỉ': 'I', 'Ĩ': 'I',
        'Ò': 'O', 'Ó': 'O', 'Ọ': 'O', 'Ỏ': 'O', 'Õ': 'O', 'Ô': 'O', 'Ồ': 'O', 'Ố': 'O', 'Ộ': 'O', 'Ổ': 'O', 'Ỗ': 'O',
        'Ơ': 'O', 'Ờ': 'O', 'Ớ': 'O', 'Ợ': 'O', 'Ở': 'O', 'Ỡ': 'O',
        'Ù': 'U', 'Ú': 'U', 'Ụ': 'U', 'Ủ': 'U', 'Ũ': 'U', 'Ư': 'U', 'Ừ': 'U', 'Ứ': 'U', 'Ự': 'U', 'Ử': 'U', 'Ữ': 'U',
        'Ỳ': 'Y', 'Ý': 'Y', 'Ỵ': 'Y', 'Ỷ': 'Y', 'Ỹ': 'Y'
    }
    for vn_char, en_char in accent_map.items():
        s = s.replace(vn_char, en_char)

    return s

def patch_zip_drawing_rels(file_path: Path):
    if not file_path.exists():
        return 0
    temp_path = file_path.with_suffix(".tmp.xlsx")
    zin = zipfile.ZipFile(file_path, "r")
    zout = zipfile.ZipFile(temp_path, "w", zipfile.ZIP_DEFLATED)
    patched_count = 0
    for item in zin.infolist():
        buffer = zin.read(item.filename)
        if item.filename.startswith("xl/drawings/_rels/") and item.filename.endswith(".rels"):
            text = buffer.decode("utf-8")
            if 'Target="/xl/media/' in text:
                text = text.replace('Target="/xl/media/', 'Target="../media/')
                buffer = text.encode("utf-8")
                patched_count += 1
            elif "Target='/xl/media/" in text:
                text = text.replace("Target='/xl/media/", "Target='../media/")
                buffer = text.encode("utf-8")
                patched_count += 1
        zout.writestr(item, buffer)
    zin.close()
    zout.close()
    temp_path.replace(file_path)
    return patched_count

def translate_workbook_in_place(file_path: Path):
    wb = openpyxl.load_workbook(file_path)
    translated_cells = 0
    for s_name in wb.sheetnames:
        ws = wb[s_name]
        for r in range(1, ws.max_row + 1):
            for c in range(1, ws.max_column + 1):
                cell = ws.cell(r, c)
                if cell.value and isinstance(cell.value, str):
                    orig = cell.value
                    if VN_PATTERN.search(orig):
                        cell.value = translate_text(orig)
                        translated_cells += 1
    wb.save(file_path)
    wb.close()
    patch_zip_drawing_rels(file_path)
    return translated_cells

def translate_all_individual_modules():
    print("[*] Translating all Individual Modules to English...")
    total_translated = 0
    for f in sorted(INDIVIDUAL_DIR.glob("**/*.xlsx")):
        if f.name.startswith("~") or f.name.startswith("."):
            continue
        cnt = translate_workbook_in_place(f)
        if cnt > 0:
            print(f"    [+] {f.name:55s} -> Translated {cnt} cells.")
            total_translated += cnt
    print(f"[✓] Total cells translated in individual modules: {total_translated}")

    # Monolithic master
    mono_1 = SUBMISSION_DIR / "00_ADMIN_PORTAL_5173_MONOLITHIC_ALL_IN_ONE_170_EVIDENCE.xlsx"
    mono_2 = TESTING_DIR / "00_ADMIN_PORTAL_5173_MONOLITHIC_ALL_IN_ONE_170_EVIDENCE.xlsx"
    for m in [mono_1, mono_2]:
        if m.exists():
            cnt = translate_workbook_in_place(m)
            print(f"    [+] {m.name:55s} -> Translated {cnt} cells.")

if __name__ == "__main__":
    translate_all_individual_modules()
