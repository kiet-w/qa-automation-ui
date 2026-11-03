#!/usr/bin/env python3
"""
=============================================================================
EduFAMS Non-Tech Defect Report Generator (Excel XLSX with Embedded Images)
Creates a beautifully formatted, executive-ready Excel workbook documenting
the 3 verified bugs found during UAT testing.
=============================================================================
"""

import os
from pathlib import Path
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image
from PIL import Image as PILImage

WORKSPACE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_FILE = WORKSPACE_DIR / "automation-uat" / "BAO_CAO_3_BUG_EDUFAMS_UAT.xlsx"
FALLBACK_FILE = Path("/tmp/BAO_CAO_3_BUG_EDUFAMS_UAT.xlsx")

IMG_BUG1 = Path("/tmp/evidence_dest/dest08_budget_cap_exceeded.png")
IMG_BUG2 = Path("/tmp/evidence_dest/dest22_view_as_active_in_class.png")
IMG_BUG3 = Path("/tmp/evidence_date/tc_date_019_year_5digits_overflow.png")

# -------------------------------------------------------------------------
# PALETTE & STYLES (Professional Executive Theme)
# -------------------------------------------------------------------------
COLOR_PRIMARY_NAVY = "0F172A"       # Slate 900
COLOR_HEADER_BLUE = "1E3A8A"        # Blue 900
COLOR_ACCENT_BLUE = "2563EB"        # Blue 600
COLOR_BG_LIGHT_BLUE = "EFF6FF"      # Blue 50
COLOR_BG_LIGHT_GRAY = "F8FAFC"      # Slate 50
COLOR_BORDER_GRAY = "CBD5E1"        # Slate 300
COLOR_BORDER_DARK = "94A3B8"        # Slate 400

COLOR_TAG_RED_BG = "FEE2E2"         # Red 100
COLOR_TAG_RED_TXT = "991B1B"        # Red 800
COLOR_TAG_YELLOW_BG = "FEF3C7"      # Amber 100
COLOR_TAG_YELLOW_TXT = "92400E"     # Amber 800
COLOR_TAG_GREEN_BG = "DCFCE7"       # Green 100
COLOR_TAG_GREEN_TXT = "166534"      # Green 800

FONT_NAME = "Segoe UI"

FONT_MAIN_TITLE = Font(name=FONT_NAME, size=16, bold=True, color="FFFFFF")
FONT_SUB_TITLE = Font(name=FONT_NAME, size=10, italic=True, color="E2E8F0")
FONT_SHEET_TITLE = Font(name=FONT_NAME, size=14, bold=True, color=COLOR_HEADER_BLUE)
FONT_SECTION_HEADER = Font(name=FONT_NAME, size=11, bold=True, color="FFFFFF")
FONT_TBL_HEADER = Font(name=FONT_NAME, size=11, bold=True, color="FFFFFF")
FONT_BOLD = Font(name=FONT_NAME, size=10, bold=True, color="1E293B")
FONT_REGULAR = Font(name=FONT_NAME, size=10, color="334155")
FONT_ITALIC = Font(name=FONT_NAME, size=9, italic=True, color="64748B")
FONT_CODE = Font(name="Consolas", size=9.5, color="0F172A")

FILL_TITLE = PatternFill(start_color=COLOR_HEADER_BLUE, end_color=COLOR_HEADER_BLUE, fill_type="solid")
FILL_SECTION = PatternFill(start_color=COLOR_ACCENT_BLUE, end_color=COLOR_ACCENT_BLUE, fill_type="solid")
FILL_TBL_HEADER = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
FILL_ZEBRA = PatternFill(start_color=COLOR_BG_LIGHT_GRAY, end_color=COLOR_BG_LIGHT_GRAY, fill_type="solid")
FILL_CARD_BG = PatternFill(start_color=COLOR_BG_LIGHT_BLUE, end_color=COLOR_BG_LIGHT_BLUE, fill_type="solid")
FILL_HIGHLIGHT = PatternFill(start_color="FEF9C3", end_color="FEF9C3", fill_type="solid")  # Yellow 100

BORDER_THIN = Border(
    left=Side(style="thin", color=COLOR_BORDER_GRAY),
    right=Side(style="thin", color=COLOR_BORDER_GRAY),
    top=Side(style="thin", color=COLOR_BORDER_GRAY),
    bottom=Side(style="thin", color=COLOR_BORDER_GRAY)
)
BORDER_SECTION = Border(
    left=Side(style="thin", color=COLOR_BORDER_DARK),
    right=Side(style="thin", color=COLOR_BORDER_DARK),
    top=Side(style="medium", color=COLOR_HEADER_BLUE),
    bottom=Side(style="medium", color=COLOR_HEADER_BLUE)
)

ALIGN_LEFT = Alignment(horizontal="left", vertical="center", wrap_text=True)
ALIGN_CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
ALIGN_TOP_LEFT = Alignment(horizontal="left", vertical="top", wrap_text=True)


def create_bug_report_workbook():
    wb = openpyxl.Workbook()
    # Remove default sheet
    wb.remove(wb.active)

    # -------------------------------------------------------------------------
    # SHEET 1: TỔNG HỢP (SUMMARY DASHBOARD)
    # -------------------------------------------------------------------------
    ws_summary = wb.create_sheet(title="📋 TỔNG HỢP (SUMMARY)")
    ws_summary.views.sheetView[0].showGridLines = True

    # Title Banner (Rows 1 to 2)
    ws_summary.merge_cells("A1:G1")
    ws_summary["A1"] = "BÁO CÁO GHI NHẬN 3 LỖI NGHIỆP VỤ CẦN XỬ LÝ TRƯỚC UAT (EDUFAMS)"
    ws_summary["A1"].font = FONT_MAIN_TITLE
    ws_summary["A1"].fill = FILL_TITLE
    ws_summary["A1"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws_summary.row_dimensions[1].height = 34

    ws_summary.merge_cells("A2:G2")
    ws_summary["A2"] = "Dự án: EduFAMS | Phiên bản: Sprint 2 Pre-UAT | Đối tượng: Dành cho Quản trị viên, PO, BA và Đội ngũ Kỹ thuật (Dev Team)"
    ws_summary["A2"].font = FONT_SUB_TITLE
    ws_summary["A2"].fill = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
    ws_summary["A2"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws_summary.row_dimensions[2].height = 20

    # Executive Overview Cards (Rows 4 to 6)
    cards = [
        ("TỔNG SỐ LỖI PHÁT HIỆN", "3 BUG", "Phát hiện qua 57 bài test UAT & Destructive", "A", "B", COLOR_TAG_RED_BG, COLOR_TAG_RED_TXT),
        ("MỨC ĐỘ ẢNH HƯỞNG", "2 VỪA - 1 NHẸ", "Không gây sập hệ thống hay mất dữ liệu", "C", "D", COLOR_TAG_YELLOW_BG, COLOR_TAG_YELLOW_TXT),
        ("TRẠNG THÁI KHUYẾN NGHỊ", "CẦN SỬA SỚM", "Xử lý trước ngày demo bàn giao cho Khách hàng", "E", "G", COLOR_TAG_GREEN_BG, COLOR_TAG_GREEN_TXT),
    ]

    for title, val, sub, col_start, col_end, fill_color, txt_color in cards:
        cell_ref = f"{col_start}4"
        ws_summary.merge_cells(f"{col_start}4:{col_end}4")
        ws_summary[cell_ref] = title
        ws_summary[cell_ref].font = Font(name=FONT_NAME, size=9, bold=True, color="64748B")
        ws_summary[cell_ref].alignment = ALIGN_CENTER

        cell_val = f"{col_start}5"
        ws_summary.merge_cells(f"{col_start}5:{col_end}5")
        ws_summary[cell_val] = val
        ws_summary[cell_val].font = Font(name=FONT_NAME, size=15, bold=True, color=txt_color)
        ws_summary[cell_val].alignment = ALIGN_CENTER
        ws_summary[cell_val].fill = PatternFill(start_color=fill_color, end_color=fill_color, fill_type="solid")

        cell_sub = f"{col_start}6"
        ws_summary.merge_cells(f"{col_start}6:{col_end}6")
        ws_summary[cell_sub] = sub
        ws_summary[cell_sub].font = Font(name=FONT_NAME, size=8.5, italic=True, color="475569")
        ws_summary[cell_sub].alignment = ALIGN_CENTER

        for r in range(4, 7):
            for c in range(openpyxl.utils.column_index_from_string(col_start), openpyxl.utils.column_index_from_string(col_end) + 1):
                col_letter = openpyxl.utils.get_column_letter(c)
                ws_summary[f"{col_letter}{r}"].border = BORDER_THIN

    ws_summary.row_dimensions[4].height = 18
    ws_summary.row_dimensions[5].height = 28
    ws_summary.row_dimensions[6].height = 18

    # Table Header (Row 8)
    headers = [
        ("MÃ LỖI", 14),
        ("TÊN LỖI & HIỆN TƯỢNG (NGÔN TỪ DỄ HIỂU)", 42),
        ("MÀN HÌNH / PHÂN HỆ", 24),
        ("MỨC ĐỘ", 14),
        ("AI SẼ GẶP LỖI NÀY?", 22),
        ("HẬU QUẢ NẾU KHÔNG SỬA", 36),
        ("XEM CHI TIẾT", 16),
    ]

    start_row = 8
    ws_summary.row_dimensions[start_row].height = 26
    for i, (h_title, width) in enumerate(headers, 1):
        c_letter = get_column_letter(i)
        ws_summary.column_dimensions[c_letter].width = width
        cell = ws_summary[f"{c_letter}{start_row}"]
        cell.value = h_title
        cell.font = FONT_TBL_HEADER
        cell.fill = FILL_TBL_HEADER
        cell.alignment = ALIGN_CENTER
        cell.border = BORDER_THIN

    # Data Rows
    bug_rows = [
        (
            "BUG-01",
            "Cho phép nhập số âm hoặc số tiền quá lớn vào Ngân sách gói trợ cấp trường (SBFAS)",
            "Tạo gói trợ cấp trường\n(/financial/sbfas/new)",
            "Vừa (Medium)",
            "Hiệu trưởng / Kế toán trường học",
            "Nếu người dùng gõ nhầm số âm (-50000) hoặc số quá lớn, hệ thống vẫn cho lưu, làm sai lệch quỹ trợ cấp và báo cáo tài chính.",
            "BUG-01",
            COLOR_TAG_YELLOW_BG,
            COLOR_TAG_YELLOW_TXT
        ),
        (
            "BUG-02",
            "Bị kẹt trong phiên giả lập: Mất nút 'Thoát' (Exit) khi mở các trang quản lý của trường",
            "Quản lý lớp học\n(/class-management)",
            "Vừa (Medium)",
            "Cán bộ Bộ Giáo dục (MOE HQ)",
            "Cán bộ Bộ khi đóng vai trường để kiểm tra dữ liệu sẽ không tìm thấy nút để quay về quyền Bộ; tưởng hệ thống bị treo quyền.",
            "BUG-02",
            COLOR_TAG_YELLOW_BG,
            COLOR_TAG_YELLOW_TXT
        ),
        (
            "BUG-03",
            "Ô chọn ngày cho phép gõ nhầm năm có 5 chữ số (Ví dụ: Năm 20266 thay vì 2026)",
            "Cài đặt biểu phí học phí\n(/fee-management/rate-rules/new)",
            "Nhẹ (Low)",
            "Nhân viên quản lý biểu phí",
            "Người dùng lỡ tay gõ thừa 1 số năm thì hệ thống vẫn nhận, dẫn đến biểu phí có hiệu lực kéo dài đến tận năm 20266.",
            "BUG-03",
            COLOR_TAG_GREEN_BG,
            COLOR_TAG_GREEN_TXT
        ),
    ]

    for idx, (b_id, b_title, b_screen, b_sev, b_who, b_impact, target_sheet, sev_bg, sev_txt) in enumerate(bug_rows, start=9):
        ws_summary.row_dimensions[idx].height = 54
        row_cells = [
            (f"A{idx}", b_id, FONT_BOLD, ALIGN_CENTER, None),
            (f"B{idx}", b_title, FONT_REGULAR, ALIGN_LEFT, None),
            (f"C{idx}", b_screen, FONT_CODE, ALIGN_CENTER, None),
            (f"D{idx}", b_sev, Font(name=FONT_NAME, size=10, bold=True, color=sev_txt), ALIGN_CENTER, PatternFill(start_color=sev_bg, end_color=sev_bg, fill_type="solid")),
            (f"E{idx}", b_who, FONT_REGULAR, ALIGN_CENTER, None),
            (f"F{idx}", b_impact, FONT_REGULAR, ALIGN_LEFT, None),
            (f"G{idx}", f"👉 Xem {b_id}", Font(name=FONT_NAME, size=10, bold=True, color="2563EB", underline="single"), ALIGN_CENTER, None),
        ]
        for c_ref, c_val, c_font, c_align, c_fill in row_cells:
            cell = ws_summary[c_ref]
            cell.value = c_val
            cell.font = c_font
            cell.alignment = c_align
            cell.border = BORDER_THIN
            if c_fill:
                cell.fill = c_fill
            elif idx % 2 == 0:
                cell.fill = FILL_ZEBRA

        # Link to sheet
        ws_summary[f"G{idx}"].hyperlink = f"#'{target_sheet}'!A1"

    # Notes section at bottom (Row 13)
    ws_summary.merge_cells("A13:G13")
    ws_summary["A13"] = "💡 LƯU Ý DÀNH CHO ĐỘI NGŨ PHÁT TRIỂN (DEV TEAM):"
    ws_summary["A13"].font = FONT_BOLD
    ws_summary["A13"].fill = FILL_CARD_BG
    ws_summary["A13"].alignment = Alignment(horizontal="left", vertical="center", indent=1)

    ws_summary.merge_cells("A14:G14")
    ws_summary["A14"] = "• Cả 3 lỗi trên đều thuộc nhóm 'Kiểm soát dữ liệu đầu vào' (Validation & UI Guardrails), không liên quan đến lỗi kiến trúc lõi.\n• Vui lòng nhấp vào từng tab bên dưới hoặc bấm 'Xem BUG-01/02/03' ở cột G để xem ảnh chụp màn hình minh chứng và các bước bấm chuột chi tiết."
    ws_summary["A14"].font = FONT_REGULAR
    ws_summary["A14"].alignment = Alignment(horizontal="left", vertical="center", wrap_text=True, indent=1)
    ws_summary.row_dimensions[13].height = 24
    ws_summary.row_dimensions[14].height = 38

    for r in range(13, 15):
        for c in range(1, 8):
            ws_summary[f"{get_column_letter(c)}{r}"].border = BORDER_THIN

    # -------------------------------------------------------------------------
    # DETAIL SHEETS (BUG-01, BUG-02, BUG-03)
    # -------------------------------------------------------------------------
    detail_specs = [
        {
            "sheet_name": "BUG-01",
            "code": "BUG-01 (Mã test: DEST-08)",
            "title": "Cho Phép Nhập Số Âm Hoặc Vượt Trần Ngân Sách Gói Trợ Cấp Trường (SBFAS)",
            "severity": "Vừa (Medium) - Rủi ro sai lệch dữ liệu tài chính",
            "screen": "Tạo gói đề án trợ cấp trường học (Menu Financial > MOEFAS/SBFAS > /financial/sbfas/new)",
            "who": "Cán bộ quản lý trợ cấp / Hiệu trưởng / Kế toán trường học (staff1@IAM.edu.vn)",
            "simple_desc": "Ở Bước 1 của form tạo gói trợ cấp trường (SBFAS Scheme Wizard), ô nhập 'Total budget (SGD)' không có chốt chặn kiểm tra số tiền hợp lệ. Khi người dùng cố tình hoặc vô ý gõ số tiền âm (ví dụ: -50,000 SGD) hoặc số tiền quá lớn (999,999 SGD), form hoàn toàn không bật viền đỏ báo lỗi mà vẫn cho phép bấm nút 'Next' để chuyển tiếp sang Bước 2 (Income Bands).",
            "steps": [
                "1. Đăng nhập hệ thống bằng tài khoản Cán bộ trường: staff1@IAM.edu.vn.",
                "2. Trên thanh menu chính bên trái, chọn 'Financial' -> chọn 'MOEFAS' (hoặc SBFAS Schemes).",
                "3. Nhấn nút 'Create scheme' để bắt đầu tạo gói trợ cấp mới (URL: /financial/sbfas/new).",
                "4. Tại Bước 1 (Scheme Details): Nhập tên đề án 'Test Scheme', sau đó tìm ô 'Total budget (SGD)'.",
                "5. Thử gõ số tiền âm: '-50000' (hoặc số tiền cực lớn vượt hạn mức như 999999).",
                "6. Cuộn xuống cuối trang và nhấn nút 'Next'."
            ],
            "actual": "💥 Màn hình KHÔNG báo lỗi, KHÔNG hiện viền đỏ. Hệ thống tự động chuyển người dùng sang Bước 2 bình thường.",
            "expected": "🎯 Hệ thống phải chặn lại ngay tại Bước 1, hiển thị viền đỏ quanh ô Total Budget và đưa ra câu nhắc dễ hiểu: 'Ngân sách phải lớn hơn 0 và không vượt quá 50,000.00 SGD'. Nút 'Next' phải bị khóa hoặc form không cho chuyển bước.",
            "dev_guide": "• Frontend (React UI): Bổ sung thuộc tính min='0.01' và max='50000.00' vào ô input `#total-budget`. Thêm validation trigger onBlur.\n• Backend (C# API DTO): Bổ sung FluentValidation cho SchemeCreateDto:\n   RuleFor(x => x.TotalBudget).GreaterThanOrEqualTo(0.01m).LessThanOrEqualTo(50000.00m).WithMessage('Budget must be between $0.01 and $50,000.00');",
            "img_path": IMG_BUG1,
            "img_caption": "Hình ảnh minh chứng thực tế: Nhập số âm -50,000 SGD nhưng form vẫn nhận và cho phép bấm Next chuyển bước."
        },
        {
            "sheet_name": "BUG-02",
            "code": "BUG-02 (Mã test: DEST-22)",
            "title": "Bị Kẹt Phiên Giả Lập: Mất Nút 'Thoát' (Exit) Trên Banner Khi Mở Các Trang Quản Lý Con",
            "severity": "Vừa (Medium) - Trải nghiệm người dùng và điều hướng phân quyền",
            "screen": "Màn hình Quản lý lớp học của trường (/class-management) trong phiên View As",
            "who": "Cán bộ Quản trị cấp Bộ MOE HQ (admin@IAM.edu.vn)",
            "simple_desc": "Tính năng 'View As' (Xem với tư cách trường) cho phép cán bộ Bộ MOE đóng vai trường để hỗ trợ người dùng. Khi vào phiên giả lập, hệ thống có một thanh banner màu đen ghi 'Viewing as staff1@...'. Trên banner này cần có nút 'Exit' để thoát. Tuy nhiên, khi cán bộ Bộ bấm vào menu bên trong (như Quản lý lớp học /class-management), thanh banner này bị cuộn mất hoặc không render nút 'Exit', khiến người dùng bị 'mắc kẹt' ở quyền trường và không biết làm sao để quay về quyền Bộ nếu không tự gõ lại đường link /support-console.",
            "steps": [
                "1. Đăng nhập bằng tài khoản Cán bộ Bộ MOE: admin@IAM.edu.vn.",
                "2. Truy cập trang /support-console, tìm cán bộ trường 'staff1', nhập lý do kiểm toán và bấm 'Start View As'.",
                "3. Hệ thống chuyển sang giao diện trường học với banner 'Viewing as staff1@IAM.edu.vn'.",
                "4. Trên menu điều hướng bên trái, bấm vào mục 'Class Management' (URL: /class-management).",
                "5. Quan sát thanh banner trên cùng của trang web để tìm nút quay lại quyền Bộ."
            ],
            "actual": "💥 Trên thanh banner hoặc đầu trang không có nút 'Exit' rõ ràng. Người dùng không có cách bấm chuột nào để thoát khỏi phiên trường.",
            "expected": "🎯 Thanh banner thông báo 'Viewing as staff1@...' phải luôn được ghim cố định ở đầu màn hình (Sticky Header) trên mọi trang con. Nút 'Exit' màu trắng hoặc đỏ phải luôn hiển thị nổi bật để người dùng bấm 1 cái là lập tức khôi phục quyền Quản trị Bộ.",
            "dev_guide": "• Frontend Layout: Cấu hình CSS cho impersonation top banner:\n   position: fixed; top: 0; left: 0; width: 100%; z-index: 99999;\n• Luôn bảo đảm component <ImpersonationBanner /> chứa <button onClick={handleExit}>Exit</button> được bọc ở Root App Layout thay vì chỉ ở một số trang độc lập.",
            "img_path": IMG_BUG2,
            "img_caption": "Hình ảnh minh chứng thực tế: Đang ở trong trang /class-management của trường nhưng không tìm thấy nút 'Exit' để quay về quyền Bộ."
        },
        {
            "sheet_name": "BUG-03",
            "code": "BUG-03 (Mã test: TC-DATE-019)",
            "title": "Ô Chọn Ngày Cho Phép Gõ Nhầm Năm 5 Chữ Số (Ví Dụ: Năm 20266 Thay Vì 2026)",
            "severity": "Nhẹ (Low) - Kiểm tra tính hợp lệ của định dạng ngày tháng",
            "screen": "Màn hình Tạo mức biểu phí học phí (/fee-management/rate-rules/new)",
            "who": "Nhân viên cài đặt biểu phí của Bộ và Nhà trường (admin@IAM.edu.vn)",
            "simple_desc": "Tại màn hình cài đặt ngày hiệu lực của mức học phí (Effective From / Effective To), ô chọn ngày không giới hạn độ dài ký tự năm. Nếu người dùng lỡ tay gõ nhanh bị dính phím thừa 1 con số (ví dụ: gõ '15/05/20266' thay vì '15/05/2026'), ô nhập vẫn chấp nhận và lưu năm 20266 vào hệ thống mà không có cảnh báo nào.",
            "steps": [
                "1. Đăng nhập bằng tài khoản Quản trị: admin@IAM.edu.vn.",
                "2. Mở màn hình tạo mức biểu phí mới: /fee-management/rate-rules/new.",
                "3. Click chuột vào ô 'Effective from (Ngày bắt đầu)'.",
                "4. Sử dụng bàn phím gõ chuỗi ngày có năm 5 chữ số: '15/05/20266'.",
                "5. Nhấn phím Tab hoặc click chuột ra bên ngoài ô nhập."
            ],
            "actual": "💥 Ô ngày chấp nhận hoàn toàn giá trị '20266-05-15', không báo lỗi cú pháp và cho phép submit lưu dữ liệu.",
            "expected": "🎯 Ô ngày phải giới hạn chỉ cho phép nhập tối đa 4 chữ số cho phần năm (trong khoảng hợp lý từ năm 1900 đến 2099). Khi người dùng gõ số thứ 5 thì hệ thống tự động ngắt hoặc báo lỗi viền đỏ: 'Năm không hợp lệ (chỉ được từ 1900 đến 2099)'.",
            "dev_guide": "• Frontend (HTML input): Bổ sung thuộc tính min và max cho thẻ input date:\n   <input type='date' id='fixed-from' min='1900-01-01' max='2099-12-31' />\n• Backend DTO: Thêm validation rule:\n   RuleFor(x => x.EffectiveFrom.Year).InclusiveBetween(1900, 2099).WithMessage('Year must be within 1900 and 2099');",
            "img_path": IMG_BUG3,
            "img_caption": "Hình ảnh minh chứng thực tế: Ô ngày nhận giá trị 20266-05-15 (năm 5 chữ số) do thiếu thuộc tính giới hạn max date."
        }
    ]

    for spec in detail_specs:
        ws = wb.create_sheet(title=spec["sheet_name"])
        ws.views.sheetView[0].showGridLines = True

        # Sheet Header
        ws.merge_cells("A1:H1")
        ws["A1"] = f"CHI TIẾT: {spec['code']} - {spec['title']}"
        ws["A1"].font = FONT_MAIN_TITLE
        ws["A1"].fill = FILL_TITLE
        ws["A1"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
        ws.row_dimensions[1].height = 32

        # Back to summary link
        ws.merge_cells("A2:H2")
        ws["A2"] = "⬅️ Bấm vào đây để quay lại Trang Tổng Hợp (Summary Dashboard)"
        ws["A2"].font = Font(name=FONT_NAME, size=9.5, bold=True, color="2563EB", underline="single")
        ws["A2"].hyperlink = "#'📋 TỔNG HỢP (SUMMARY)'!A1"
        ws["A2"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
        ws.row_dimensions[2].height = 20

        # Info Metadata Box (Rows 4 to 6)
        meta_items = [
            ("Mức độ nghiêm trọng:", spec["severity"], "A", "D"),
            ("Màn hình phát sinh:", spec["screen"], "A", "H"),
            ("Người dùng gặp lỗi:", spec["who"], "A", "H"),
        ]

        curr_r = 4
        # Severity
        ws[f"A{curr_r}"] = "Mức độ nghiêm trọng:"
        ws[f"A{curr_r}"].font = FONT_BOLD
        ws.merge_cells(f"B{curr_r}:H{curr_r}")
        ws[f"B{curr_r}"] = spec["severity"]
        ws[f"B{curr_r}"].font = Font(name=FONT_NAME, size=10, bold=True, color="B45309")
        ws[f"B{curr_r}"].fill = PatternFill(start_color=COLOR_TAG_YELLOW_BG, end_color=COLOR_TAG_YELLOW_BG, fill_type="solid")
        curr_r += 1

        # Screen
        ws[f"A{curr_r}"] = "Màn hình / Vị trí:"
        ws[f"A{curr_r}"].font = FONT_BOLD
        ws.merge_cells(f"B{curr_r}:H{curr_r}")
        ws[f"B{curr_r}"] = spec["screen"]
        ws[f"B{curr_r}"].font = FONT_CODE
        curr_r += 1

        # Who
        ws[f"A{curr_r}"] = "Đối tượng gặp lỗi:"
        ws[f"A{curr_r}"].font = FONT_BOLD
        ws.merge_cells(f"B{curr_r}:H{curr_r}")
        ws[f"B{curr_r}"] = spec["who"]
        ws[f"B{curr_r}"].font = FONT_REGULAR
        curr_r += 2

        # Section 1: Hiện tượng (Non-Tech Summary)
        ws.merge_cells(f"A{curr_r}:H{curr_r}")
        ws[f"A{curr_r}"] = "1. HIỆN TƯỢNG LỖI LÀ GÌ? (TÓM TẮT DỄ HIỂU DÀNH CHO NON-TECH / PO / BA)"
        ws[f"A{curr_r}"].font = FONT_SECTION_HEADER
        ws[f"A{curr_r}"].fill = FILL_SECTION
        ws[f"A{curr_r}"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
        ws.row_dimensions[curr_r].height = 24
        curr_r += 1

        ws.merge_cells(f"A{curr_r}:H{curr_r+1}")
        ws[f"A{curr_r}"] = spec["simple_desc"]
        ws[f"A{curr_r}"].font = FONT_REGULAR
        ws[f"A{curr_r}"].alignment = ALIGN_TOP_LEFT
        ws[f"A{curr_r}"].fill = FILL_CARD_BG
        ws.row_dimensions[curr_r].height = 28
        ws.row_dimensions[curr_r+1].height = 28
        curr_r += 3

        # Section 2: Các bước tái hiện (Steps to Reproduce)
        ws.merge_cells(f"A{curr_r}:H{curr_r}")
        ws[f"A{curr_r}"] = "2. CÁC BƯỚC THỰC HIỆN ĐỂ THẤY LỖI (STEP-BY-STEP)"
        ws[f"A{curr_r}"].font = FONT_SECTION_HEADER
        ws[f"A{curr_r}"].fill = FILL_SECTION
        ws[f"A{curr_r}"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
        ws.row_dimensions[curr_r].height = 24
        curr_r += 1

        for step in spec["steps"]:
            ws.merge_cells(f"A{curr_r}:H{curr_r}")
            ws[f"A{curr_r}"] = step
            ws[f"A{curr_r}"].font = FONT_REGULAR
            ws[f"A{curr_r}"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
            ws.row_dimensions[curr_r].height = 20
            curr_r += 1
        curr_r += 1

        # Section 3: Thực tế vs Kỳ vọng
        ws.merge_cells(f"A{curr_r}:H{curr_r}")
        ws[f"A{curr_r}"] = "3. KẾT QUẢ THỰC TẾ (LỖI) VS KẾT QUẢ KỲ VỌNG (ĐÚNG)"
        ws[f"A{curr_r}"].font = FONT_SECTION_HEADER
        ws[f"A{curr_r}"].fill = FILL_SECTION
        ws[f"A{curr_r}"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
        ws.row_dimensions[curr_r].height = 24
        curr_r += 1

        # Actual
        ws.merge_cells(f"A{curr_r}:H{curr_r}")
        ws[f"A{curr_r}"] = spec["actual"]
        ws[f"A{curr_r}"].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_TAG_RED_TXT)
        ws[f"A{curr_r}"].fill = PatternFill(start_color=COLOR_TAG_RED_BG, end_color=COLOR_TAG_RED_BG, fill_type="solid")
        ws[f"A{curr_r}"].alignment = Alignment(horizontal="left", vertical="center", wrap_text=True, indent=1)
        ws.row_dimensions[curr_r].height = 26
        curr_r += 1

        # Expected
        ws.merge_cells(f"A{curr_r}:H{curr_r+1}")
        ws[f"A{curr_r}"] = spec["expected"]
        ws[f"A{curr_r}"].font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_TAG_GREEN_TXT)
        ws[f"A{curr_r}"].fill = PatternFill(start_color=COLOR_TAG_GREEN_BG, end_color=COLOR_TAG_GREEN_BG, fill_type="solid")
        ws[f"A{curr_r}"].alignment = ALIGN_TOP_LEFT
        ws.row_dimensions[curr_r].height = 24
        ws.row_dimensions[curr_r+1].height = 24
        curr_r += 3

        # Section 4: Hướng dẫn kỹ thuật cho Dev
        ws.merge_cells(f"A{curr_r}:H{curr_r}")
        ws[f"A{curr_r}"] = "4. HƯỚNG DẪN KỸ THUẬT DÀNH CHO DEV TEAM ĐỂ SỬA NHANH (TECHNICAL FIX)"
        ws[f"A{curr_r}"].font = FONT_SECTION_HEADER
        ws[f"A{curr_r}"].fill = PatternFill(start_color="334155", end_color="334155", fill_type="solid")
        ws[f"A{curr_r}"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
        ws.row_dimensions[curr_r].height = 24
        curr_r += 1

        ws.merge_cells(f"A{curr_r}:H{curr_r+1}")
        ws[f"A{curr_r}"] = spec["dev_guide"]
        ws[f"A{curr_r}"].font = FONT_CODE
        ws[f"A{curr_r}"].fill = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")
        ws[f"A{curr_r}"].alignment = ALIGN_TOP_LEFT
        ws.row_dimensions[curr_r].height = 24
        ws.row_dimensions[curr_r+1].height = 24
        curr_r += 3

        # Section 5: Hình ảnh minh chứng thực tế (Embedded Screenshot)
        ws.merge_cells(f"A{curr_r}:H{curr_r}")
        ws[f"A{curr_r}"] = "5. HÌNH ẢNH CHỤP MÀN HÌNH MINH CHỨNG THỰC TẾ (SCREENSHOT EVIDENCE)"
        ws[f"A{curr_r}"].font = FONT_SECTION_HEADER
        ws[f"A{curr_r}"].fill = FILL_SECTION
        ws[f"A{curr_r}"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
        ws.row_dimensions[curr_r].height = 24
        curr_r += 1

        ws.merge_cells(f"A{curr_r}:H{curr_r}")
        ws[f"A{curr_r}"] = f"📸 {spec['img_caption']}"
        ws[f"A{curr_r}"].font = FONT_ITALIC
        ws[f"A{curr_r}"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
        ws.row_dimensions[curr_r].height = 20
        curr_r += 1

        # Embed Image
        if spec["img_path"].exists():
            img = Image(str(spec["img_path"]))
            # Resize image cleanly to 680px x 425px
            img.width = 680
            img.height = 425
            img_anchor = f"A{curr_r}"
            ws.add_image(img, img_anchor)

            # Adjust rows for image height (425px ~= 22 rows of height 20)
            for r_offset in range(curr_r, curr_r + 23):
                ws.row_dimensions[r_offset].height = 19
            curr_r += 24

        # Set column widths
        col_widths = {"A": 16, "B": 18, "C": 18, "D": 18, "E": 18, "F": 18, "G": 18, "H": 18}
        for col_l, w in col_widths.items():
            ws.column_dimensions[col_l].width = w

    # Save to workspace and fallback
    try:
        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
        wb.save(str(OUTPUT_FILE))
        print(f"✓ Successfully saved Excel report: {OUTPUT_FILE}")
    except Exception as e:
        print(f"Note: Workspace save error ({e}), writing to fallback...")

    try:
        FALLBACK_FILE.parent.mkdir(parents=True, exist_ok=True)
        wb.save(str(FALLBACK_FILE))
        print(f"✓ Successfully saved Fallback Excel report: {FALLBACK_FILE}")
    except Exception as e:
        print(f"Error saving fallback: {e}")


if __name__ == "__main__":
    create_bug_report_workbook()
