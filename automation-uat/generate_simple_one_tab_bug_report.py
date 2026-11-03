#!/usr/bin/env python3
"""
=============================================================================
EduFAMS Simple Single-Tab Defect Report Generator (Excel XLSX)
Includes:
  - Root Cause (Nguyên nhân)
  - Actual Result (Kết quả lỗi) & Expected Result (Kỳ vọng)
  - PHOTO 1: The Exact Moment of Input (Hình ảnh lúc nhập dẫn đến lỗi)
  - PHOTO 2: The Resulting Defect (Hình ảnh kết quả lỗi sau đó)
=============================================================================
"""

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
FALLBACK_FILE = Path("/tmp/BAO_CAO_3_BUG_EDUFAMS_UAT.xlsx")

EVIDENCE_DIR = BASE_DIR / "evidence_bugs"

IMG_BUG1_INPUT = EVIDENCE_DIR / "bug01_input_negative_budget.png"
IMG_BUG1_RESULT = EVIDENCE_DIR / "dest08_budget_cap_exceeded.png"

IMG_BUG2_INPUT = EVIDENCE_DIR / "dest22_view_as_active_in_class.png"
IMG_BUG2_RESULT = EVIDENCE_DIR / "bug02_result_missing_exit.png"

IMG_BUG3_INPUT = EVIDENCE_DIR / "bug03_input_year_20266.png"
IMG_BUG3_RESULT = EVIDENCE_DIR / "tc_date_019_year_5digits_overflow.png"

FONT_NAME = "Segoe UI"
COLOR_NAVY = "1E3A8A"
COLOR_HEADER_BG = "0F172A"
COLOR_BORDER = "CBD5E1"

BORDER_THIN = Border(
    left=Side(style="thin", color=COLOR_BORDER),
    right=Side(style="thin", color=COLOR_BORDER),
    top=Side(style="thin", color=COLOR_BORDER),
    bottom=Side(style="thin", color=COLOR_BORDER)
)

ALIGN_CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
ALIGN_TOP_LEFT = Alignment(horizontal="left", vertical="top", wrap_text=True)
ALIGN_TOP_CENTER = Alignment(horizontal="center", vertical="top", wrap_text=True)


def create_simple_report():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "BÁO CÁO 3 BUG EDUFAMS"
    ws.views.sheetView[0].showGridLines = True

    # 1. Main Header Title (Row 1-2)
    ws.merge_cells("A1:I1")
    ws["A1"] = "BÁO CÁO TỔNG HỢP 3 LỖI NGHIỆP VỤ - HỆ THỐNG EDUFAMS (UAT PRE-CHECK)"
    ws["A1"].font = Font(name=FONT_NAME, size=15, bold=True, color="FFFFFF")
    ws["A1"].fill = PatternFill(start_color=COLOR_HEADER_BG, end_color=COLOR_HEADER_BG, fill_type="solid")
    ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 32

    ws.merge_cells("A2:I2")
    ws["A2"] = "Báo cáo 1 Tab duy nhất: Thấy rõ Nguyên nhân, Kết quả thực tế, Ảnh lúc nhập liệu và Ảnh kết quả lỗi (Dành cho PO, BA & Dev Team)"
    ws["A2"].font = Font(name=FONT_NAME, size=9.5, italic=True, color="E2E8F0")
    ws["A2"].fill = PatternFill(start_color=COLOR_NAVY, end_color=COLOR_NAVY, fill_type="solid")
    ws["A2"].alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[2].height = 20

    # 2. Table Column Headers (Row 4)
    headers = [
        ("STT", 6),
        ("MÃ BUG & VỊ TRÍ", 22),
        ("TÊN LỖI (DỄ HIỂU)", 25),
        ("NGUYÊN NHÂN GÂY LỖI", 28),
        ("KẾT QUẢ THỰC TẾ (LỖI)", 32),
        ("KẾT QUẢ KỲ VỌNG (ĐÚNG)", 30),
        ("CÁCH SỬA (CHO DEV)", 28),
        ("HÌNH ẢNH 1: LÚC NHẬP DẪN ĐẾN LỖI", 50),
        ("HÌNH ẢNH 2: KẾT QUẢ HIỂN THỊ SAU ĐÓ", 50),
    ]

    header_row = 4
    ws.row_dimensions[header_row].height = 30

    for col_idx, (title, width) in enumerate(headers, 1):
        col_letter = get_column_letter(col_idx)
        ws.column_dimensions[col_letter].width = width
        cell = ws[f"{col_letter}{header_row}"]
        cell.value = title
        cell.font = Font(name=FONT_NAME, size=10, bold=True, color="FFFFFF")
        cell.fill = PatternFill(start_color="334155", end_color="334155", fill_type="solid")
        cell.alignment = ALIGN_CENTER
        cell.border = BORDER_THIN

    # Freeze Header row
    ws.freeze_panes = "A5"

    # 3. Bug Data (Rows 5, 6, 7)
    bugs = [
        {
            "stt": "1",
            "code": "BUG-01 (DEST-08)\n\nMàn hình:\nTạo gói trợ cấp trường\n(/sbfas-schemes/new)",
            "title": "Nhập được số âm & vượt trần vào ô Ngân sách gói trợ cấp SBFAS",
            "cause": "Ô nhập 'Total budget (SGD)' ở Bước 1 thiếu ràng buộc kiểm tra số tiền hợp lệ (chưa chặn số âm và chưa chặn trần 50,000 SGD ở cả giao diện lẫn API backend).",
            "actual": "💥 Gõ số âm '-50000' hoặc gõ số cực lớn '999999', form KHÔNG báo lỗi viền đỏ mà vẫn cho bấm nút 'Next' chuyển tiếp sang Bước 2 bình thường.",
            "expected": "🎯 Hệ thống phải chặn ngay tại Bước 1, bật viền đỏ và hiện cảnh báo: 'Ngân sách phải nằm trong khoảng $0.01 đến $50,000.00 SGD'. Không cho bấm Next.",
            "fix": "• Frontend: Thêm min='0.01' và max='50000.00' vào ô #sbfas-budget.\n• Backend: Thêm FluentValidation: InclusiveBetween(0.01m, 50000.00m).",
            "img_input": IMG_BUG1_INPUT,
            "img_result": IMG_BUG1_RESULT,
            "img_w": 350,
            "img_h": 218
        },
        {
            "stt": "2",
            "code": "BUG-02 (DEST-22)\n\nMàn hình:\nQuản lý lớp học\n(/class-management)\ntrong phiên View As",
            "title": "Mất nút 'Thoát' (Exit) trên thanh Banner khi mở các trang con của trường",
            "cause": "Thanh banner giả lập 'Viewing as staff1@...' chưa được ghim cố định (thiếu CSS position: fixed) và component nút 'Exit' chưa được đặt ở layout gốc nên khi chuyển sang trang con thì nút bị biến mất.",
            "actual": "💥 Khi cán bộ Bộ đang giả lập trường và bấm vào menu 'Class Management', trên đầu trang không có nút 'Exit'. Người dùng bị 'kẹt' luôn ở quyền trường, không biết cách quay về quyền Bộ.",
            "expected": "🎯 Thanh banner màu đen phải luôn ghim cố định ở đầu màn hình (Sticky Header) với nút 'Exit' màu trắng/đỏ nổi bật để người dùng bấm 1 cái là về lại quyền Bộ ngay.",
            "fix": "• Thêm CSS: position: fixed; top: 0; left: 0; width: 100%; z-index: 99999;\n• Đặt component ImpersonationBanner vào AppLayout bao ngoài toàn bộ trang.",
            "img_input": IMG_BUG2_INPUT,
            "img_result": IMG_BUG2_RESULT,
            "img_w": 350,
            "img_h": 218
        },
        {
            "stt": "3",
            "code": "BUG-03 (TC-DATE-019)\n\nMàn hình:\nCài đặt biểu phí\n(/fee-management/\nrate-rules/new)",
            "title": "Ô chọn ngày cho phép gõ nhầm năm có 5 chữ số (Ví dụ: Năm 20266)",
            "cause": "Thẻ <input type='date'> ở trường Effective From/To chưa được cài đặt thuộc tính max date, nên trình duyệt cho phép người dùng gõ chuỗi năm dài hơn 4 chữ số.",
            "actual": "💥 Gõ bàn phím '15/05/20266', ô input vẫn chấp nhận và lưu chuỗi '20266-05-15' vào hệ thống mà không hề cảnh báo lỗi sai năm.",
            "expected": "🎯 Ô ngày chỉ được cho phép nhập tối đa 4 số năm (từ 1900 đến 2099). Khi gõ số thứ 5 thì tự ngắt hoặc báo lỗi viền đỏ: 'Năm không hợp lệ'.",
            "fix": "• Thêm thuộc tính vào HTML:\n  <input type='date' min='1900-01-01' max='2099-12-31' />\n• Backend: Kiểm tra EffectiveFrom.Year <= 2099.",
            "img_input": IMG_BUG3_INPUT,
            "img_result": IMG_BUG3_RESULT,
            "img_w": 350,
            "img_h": 218
        }
    ]

    current_row = 5
    for b in bugs:
        # Row height for each bug (~178pt)
        ws.row_dimensions[current_row].height = 178

        ws[f"A{current_row}"] = b["stt"]
        ws[f"A{current_row}"].font = Font(name=FONT_NAME, size=11, bold=True, color="0F172A")
        ws[f"A{current_row}"].alignment = ALIGN_TOP_CENTER

        ws[f"B{current_row}"] = b["code"]
        ws[f"B{current_row}"].font = Font(name=FONT_NAME, size=9.5, bold=True, color="1E3A8A")
        ws[f"B{current_row}"].alignment = ALIGN_TOP_LEFT

        ws[f"C{current_row}"] = b["title"]
        ws[f"C{current_row}"].font = Font(name=FONT_NAME, size=10, bold=True, color="0F172A")
        ws[f"C{current_row}"].alignment = ALIGN_TOP_LEFT

        ws[f"D{current_row}"] = b["cause"]
        ws[f"D{current_row}"].font = Font(name=FONT_NAME, size=9.5, color="334155")
        ws[f"D{current_row}"].alignment = ALIGN_TOP_LEFT

        ws[f"E{current_row}"] = b["actual"]
        ws[f"E{current_row}"].font = Font(name=FONT_NAME, size=9.5, color="991B1B")
        ws[f"E{current_row}"].fill = PatternFill(start_color="FEF2F2", end_color="FEF2F2", fill_type="solid")
        ws[f"E{current_row}"].alignment = ALIGN_TOP_LEFT

        ws[f"F{current_row}"] = b["expected"]
        ws[f"F{current_row}"].font = Font(name=FONT_NAME, size=9.5, color="166534")
        ws[f"F{current_row}"].fill = PatternFill(start_color="F0FDF4", end_color="F0FDF4", fill_type="solid")
        ws[f"F{current_row}"].alignment = ALIGN_TOP_LEFT

        ws[f"G{current_row}"] = b["fix"]
        ws[f"G{current_row}"].font = Font(name="Consolas", size=9, color="0F172A")
        ws[f"G{current_row}"].fill = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
        ws[f"G{current_row}"].alignment = ALIGN_TOP_LEFT

        # Border for cells A to I
        for c_idx in range(1, 10):
            col_l = get_column_letter(c_idx)
            ws[f"{col_l}{current_row}"].border = BORDER_THIN

        # Photo 1: Moment of Input (Column H)
        if b["img_input"].exists():
            img1 = Image(str(b["img_input"]))
            img1.width = b["img_w"]
            img1.height = b["img_h"]
            ws.add_image(img1, f"H{current_row}")

        # Photo 2: Resulting Defect (Column I)
        if b["img_result"].exists():
            img2 = Image(str(b["img_result"]))
            img2.width = b["img_w"]
            img2.height = b["img_h"]
            ws.add_image(img2, f"I{current_row}")

        current_row += 1

    # Save workbook
    wb.save(str(FALLBACK_FILE))
    print(f"✓ Successfully exported single-tab report to: {FALLBACK_FILE}")


if __name__ == "__main__":
    create_simple_report()
