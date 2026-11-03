#!/usr/bin/env python3
"""
=============================================================================
EduFAMS Single-Tab Retest Defect Report Generator (Excel XLSX)
Includes:
  - Header & Executive KPI Summary Card
  - Detailed Retest Verdict for 3 Defects (BUG-01, BUG-02, BUG-03)
  - Full Visual Evidence for BUG-02 and BUG-03
  - EXPANDED SECTION: 6 Detailed Live Screenshots for BUG-01 (DEST-08)
=============================================================================
"""

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_FILE = BASE_DIR / "BAO_CAO_RETEST_3_BUG_EDUFAMS.xlsx"
EVIDENCE_DIR = BASE_DIR / "evidence_bugs"
BUG01_DIR = EVIDENCE_DIR / "bug01_detail"

# Images for 3 Bugs Table
IMG_BUG1_BEFORE = EVIDENCE_DIR / "bug01_input_negative_budget.png"
IMG_BUG1_AFTER = BUG01_DIR / "03_step1_extreme_budget_input.png"

IMG_BUG2_BEFORE = EVIDENCE_DIR / "bug02_result_missing_exit.png"
IMG_BUG2_AFTER = EVIDENCE_DIR / "retest_bug02_fixed_exit_button.png"

IMG_BUG3_BEFORE = EVIDENCE_DIR / "bug03_input_year_20266.png"
IMG_BUG3_AFTER = EVIDENCE_DIR / "retest_bug03_fixed_year_constraint.png"

# Detailed 6 Screenshots for BUG-01
BUG01_STEPS = [
    {
        "stt": "1.1",
        "stage": "BƯỚC 1: XỬ LÝ SỐ ÂM\n(Dev đã sửa 1 phần)",
        "desc": (
            "• Thao tác: Gõ hoặc dán số âm '-50000' vào ô 'Total budget (SGD)'.\n\n"
            "• Ghi nhận: Dev đã thêm hàm sanitize tự động lọc bỏ dấu trừ '-', giá trị trong ô trở thành '50000'.\n\n"
            "• Đánh giá: Đã chặn được dấu âm, nhưng chưa có validation kiểm tra biên trên (50,000 SGD) và cận dưới (0.01 SGD)."
        ),
        "img": BUG01_DIR / "01_typing_negative_sanitized.png"
    },
    {
        "stt": "1.2",
        "stage": "BƯỚC 1: THỬ NGÂN SÁCH = 0\n(Lỗi tồn đọng)",
        "desc": (
            "• Thao tác: Xóa ô budget và gõ ngân sách bằng '0' SGD rồi bấm nút 'Next'.\n\n"
            "• Ghi nhận: Hệ thống HOÀN TOÀN KHÔNG báo lỗi, không có viền đỏ, và chuyển thẳng sang Bước 2 (Eligibility).\n\n"
            "• Hậu quả: Cho phép tạo đề án hỗ trợ tài chính nhưng ngân sách bằng 0 đồng, vô hiệu hóa việc chi trả trợ cấp cho học sinh."
        ),
        "img": BUG01_DIR / "02_zero_budget_accepted_step2.png"
    },
    {
        "stt": "1.3",
        "stage": "BƯỚC 1: NHẬP SỐ CỰC LỚN\n(999 Triệu SGD)",
        "desc": (
            "• Thao tác: Nhập số tiền cực lớn '999999999' SGD (999 triệu SGD, gấp 20,000 lần hạn mức trần 50,000 SGD quy định).\n\n"
            "• Ghi nhận: Ô input nhận toàn bộ 9 chữ số mà không bị giới hạn độ dài hay giá trị. Không có viền đỏ cảnh báo vượt trần."
        ),
        "img": BUG01_DIR / "03_step1_extreme_budget_input.png"
    },
    {
        "stt": "1.4",
        "stage": "BƯỚC 2: CHUYỂN BƯỚC\n(Bypass thành công)",
        "desc": (
            "• Thao tác: Bấm nút 'Next' sau khi nhập 999,999,999 SGD.\n\n"
            "• Ghi nhận: Hệ thống KHÔNG CHẶN, không kích hoạt validation và cho phép chuyển tiếp sang Bước 2 để nhập tiêu chí thu nhập.\n\n"
            "• Nguyên nhân: Thẻ <input type='text'> không kích hoạt kiểm tra HTML5 min/max nếu thiếu schema validation bằng JavaScript."
        ),
        "img": BUG01_DIR / "04_step2_bypassed_without_error.png"
    },
    {
        "stt": "1.5",
        "stage": "BƯỚC 4: MÀN HÌNH REVIEW\n(Hiển thị $999M SGD)",
        "desc": (
            "• Thao tác: Hoàn tất Bước 2 & 3 rồi bấm 'Review' để tới màn hình tổng quan Bước 4 trước khi xuất bản.\n\n"
            "• Ghi nhận: Mục Total budget hiển thị chính thức: '$999,999,999.00 SGD'. Toàn bộ luồng wizard đều hợp thức hóa số tiền bất thường này."
        ),
        "img": BUG01_DIR / "05_step4_review_extreme_budget.png"
    },
    {
        "stt": "1.6",
        "stage": "HẬU QUẢ: XUẤT BẢN CSDL\n(Lưu thành công vào bảng)",
        "desc": (
            "• Thao tác: Bấm nút 'Publish' tại màn hình Review.\n\n"
            "• Ghi nhận: Đề án được lưu thành công vào CSDL với mã SBF-01038, trạng thái PUBLISHED và hiển thị công khai trên danh sách trường.\n\n"
            "• Rủi ro nghiêm trọng: Gây sai lệch ngân sách tài chính của trường và vượt ngân sách tài khóa nhà nước."
        ),
        "img": BUG01_DIR / "06_published_scheme_in_table_999m.png"
    }
]

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


def build_retest_excel():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "KẾT QUẢ RETEST 3 BUG"
    ws.views.sheetView[0].showGridLines = True

    # 1. Title Banner (Rows 1-2)
    ws.merge_cells("A1:H1")
    ws["A1"] = "BÁO CÁO KẾT QUẢ RETEST 3 LỖI NGHIỆP VỤ SAU KHI DEV SỬA (EDUFAMS UAT)"
    ws["A1"].font = Font(name=FONT_NAME, size=15, bold=True, color="FFFFFF")
    ws["A1"].fill = PatternFill(start_color=COLOR_HEADER_BG, end_color=COLOR_HEADER_BG, fill_type="solid")
    ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 34

    ws.merge_cells("A2:H2")
    ws["A2"] = "Môi trường: Live Admin & Parent Portal (https://admin.20-255-158-192.sslip.io) | Thực thi: QA Automation Suite | Ngày retest: 01/11/2026"
    ws["A2"].font = Font(name=FONT_NAME, size=9.5, italic=True, color="E2E8F0")
    ws["A2"].fill = PatternFill(start_color=COLOR_NAVY, end_color=COLOR_NAVY, fill_type="solid")
    ws["A2"].alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[2].height = 22

    # 2. Executive KPI Cards (Row 4)
    ws.merge_cells("A4:B4")
    ws["A4"] = "TỔNG SỐ BUG RETEST: 3"
    ws["A4"].font = Font(name=FONT_NAME, size=10, bold=True, color="0F172A")
    ws["A4"].fill = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")
    ws["A4"].alignment = ALIGN_CENTER

    ws.merge_cells("C4:D4")
    ws["C4"] = "✅ ĐÃ SỬA XONG (PASS): 2/3 (67%)"
    ws["C4"].font = Font(name=FONT_NAME, size=10, bold=True, color="166534")
    ws["C4"].fill = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")
    ws["C4"].alignment = ALIGN_CENTER

    ws.merge_cells("E4:F4")
    ws["E4"] = "⚠️ CÒN TỒN ĐỌNG (RESIDUAL): 1/3 (BUG-01)"
    ws["E4"].font = Font(name=FONT_NAME, size=10, bold=True, color="991B1B")
    ws["E4"].fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
    ws["E4"].alignment = ALIGN_CENTER

    ws.merge_cells("G4:H4")
    ws["G4"] = "HỆ THỐNG REGRESSION: 100% E2E PASS | 32/32 DATE PASS"
    ws["G4"].font = Font(name=FONT_NAME, size=9.5, bold=True, color="1E3A8A")
    ws["G4"].fill = PatternFill(start_color="DBEAFE", end_color="DBEAFE", fill_type="solid")
    ws["G4"].alignment = ALIGN_CENTER
    ws.row_dimensions[4].height = 26

    # 3. Table Column Headers (Row 6)
    headers = [
        ("STT", 6),
        ("MÃ BUG & VỊ TRÍ", 22),
        ("TÊN LỖI & PHẠM VI", 26),
        ("TRẠNG THÁI RETEST", 20),
        ("KẾT QUẢ KIỂM THỬ THỰC TẾ (VERDICT)", 38),
        ("ĐÁNH GIÁ KỸ THUẬT & HƯỚNG DẪN DEV", 32),
        ("HÌNH ẢNH TRƯỚC SỬA (LỖI CŨ)", 50),
        ("HÌNH ẢNH SAU SỬA (KẾT QUẢ RETEST)", 50),
    ]

    header_row = 6
    ws.row_dimensions[header_row].height = 32

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
    ws.freeze_panes = "A7"

    # 4. Retest Data (Rows 7, 8, 9)
    bugs = [
        {
            "stt": "1",
            "code": "BUG-01 (DEST-08)\n\nMàn hình:\nTạo gói trợ cấp trường\n(/sbfas-schemes/new)",
            "title": "Chặn số âm và giới hạn trần ngân sách ($50,000 SGD) gói trợ cấp SBFAS",
            "status": "⚠️ MỚI SỬA 1 PHẦN\n(CÒN TỒN ĐỌNG LỖI)",
            "status_color": "991B1B",
            "status_bg": "FEE2E2",
            "verdict": (
                "• ĐIỂM ĐÃ SỬA ĐƯỢC: Dev đã loại bỏ dấu trừ '-', người dùng gõ phím hoặc paste số âm '-50000' thì hệ thống tự động lọc bỏ dấu trừ thành '50000'.\n\n"
                "• LỖI TỒN ĐỌNG (CHƯA ĐẠT):\n"
                "1. Ô nhập liệu vẫn cho phép nhập ngân sách bằng 0 SGD mà vẫn bấm được 'Next' sang bước 2.\n"
                "2. Khi nhập số tiền vượt trần $50,000 SGD (test với số '999,999,999 SGD'), form KHÔNG bật viền đỏ, KHÔNG hiển thị câu thông báo lỗi nào và VẪN CHO BẤM 'Next' chuyển sang bước 2, cho phép tạo và ban hành gói trợ cấp vượt quá ngân sách nhà nước!"
            ),
            "dev_guidance": (
                "🔍 NGUYÊN NHÂN:\n"
                "Dev mới chỉ thêm thuộc tính min='0' vào ô <input type='text'>. Trình duyệt KHÔNG tự kích hoạt form validation HTML5 cho input kiểu text nếu không có logic JS hoặc type='number'.\n\n"
                "🛠️ CÁCH KHẮC PHỤC TRIỆT ĐỂ:\n"
                "1. Thêm validation schema tại Bước 1 (Zod/Yup/Regex) khi bấm 'Next':\n"
                "   Bắt buộc: 0.01 <= Budget <= 50,000.00 SGD.\n"
                "2. Nếu giá trị = 0 hoặc > 50,000, lập tức bật viền đỏ, hiển thị: 'Budget must be between $0.01 and $50,000.00 SGD' và chặn không cho chuyển bước.\n"
                "3. Backend: Áp dụng FluentValidation InclusiveBetween(0.01m, 50000.00m)."
            ),
            "img_before": IMG_BUG1_BEFORE,
            "img_after": IMG_BUG1_AFTER,
            "img_w": 350,
            "img_h": 218
        },
        {
            "stt": "2",
            "code": "BUG-02 (DEST-22)\n\nMàn hình:\nQuản lý lớp học\n(/class-management)\ntrong phiên View As",
            "title": "Hiển thị nút 'Thoát' (Exit) trên thanh Banner khi cán bộ Bộ mở các trang con của trường",
            "status": "✅ ĐÃ SỬA HOÀN TOÀN\n(PASS / DEFENDED)",
            "status_color": "166534",
            "status_bg": "DCFCE7",
            "verdict": (
                "• KẾT QUẢ KIỂM THỬ: XUẤT SẮC (100% ĐẠT).\n\n"
                "1. Khi cán bộ MOE HQ kích hoạt phiên View As trường 'Rosyth Primary School' và truy cập vào trang con '/class-management', thanh Banner màu đen và nút 'Exit' vẫn hiển thị cố định ở đầu màn hình.\n"
                "2. Bấm nút 'Exit': Hệ thống lập tức gửi lệnh hủy phiên giả lập, tự động chuyển hướng an toàn về '/support-console' và xóa hoàn toàn trạng thái View As, khôi phục quyền cán bộ Bộ bình thường.\n"
                "3. Toàn bộ 6/6 kịch bản kiểm thử bảo mật & RBAC đều được bảo vệ thành công."
            ),
            "dev_guidance": (
                "👍 ĐÁNH GIÁ:\n"
                "Dev đã tích hợp ImpersonationBanner vào AppLayout bao ngoài với nút `<button class='_action_1437o_38'>Exit</button>` hiển thị nhất quán trên mọi trang con.\n\n"
                "📌 DUY TRÌ:\n"
                "Giữ nguyên kiến trúc Layout toàn cục này cho tất cả các trang/submodules mới phát triển trong tương lai."
            ),
            "img_before": IMG_BUG2_BEFORE,
            "img_after": IMG_BUG2_AFTER,
            "img_w": 350,
            "img_h": 218
        },
        {
            "stt": "3",
            "code": "BUG-03 (TC-DATE-019)\n\nMàn hình:\nCài đặt biểu phí\n(/fee-management/\nrate-rules/new)",
            "title": "Chặn nhập nhầm năm có 5 chữ số (ví dụ năm 20266) tại các ô ngày tháng",
            "status": "✅ ĐÃ SỬA HOÀN TOÀN\n(PASS / DEFENDED)",
            "status_color": "166534",
            "status_bg": "DCFCE7",
            "verdict": (
                "• KẾT QUẢ KIỂM THỬ: XUẤT SẮC (100% ĐẠT).\n\n"
                "1. Khi gõ ngày '15/05/20266' vào ô 'Effective From' hoặc 'Effective To', thuộc tính max='2099-12-31' kích hoạt ngay lập tức.\n"
                "2. Trình duyệt đánh dấu ô dữ liệu là không hợp lệ (rangeOverflow=True, checkValidity=False) và bật thông báo cảnh báo chuẩn: 'Value must be 12/31/2099 or earlier'.\n"
                "3. Nút submit bị chặn hoàn toàn, ngăn chặn 100% nguy cơ lọt dữ liệu rác làm hỏng CSDL.\n"
                "4. Toàn bộ 32/32 ca kiểm thử ngày tháng đều vượt qua (100% Pass)."
            ),
            "dev_guidance": (
                "👍 ĐÁNH GIÁ:\n"
                "Dev đã thêm đầy đủ thuộc tính chuẩn HTML5 min='1900-01-01' và max='2099-12-31' vào các thẻ <input type='date'>.\n\n"
                "📌 KHUYẾN NGHỊ BỔ SUNG:\n"
                "Đồng bộ thuộc tính max='2099-12-31' này trên toàn bộ các form nhập ngày còn lại của hệ thống (như ngày sinh học sinh, ngày đánh giá FAS)."
            ),
            "img_before": IMG_BUG3_BEFORE,
            "img_after": IMG_BUG3_AFTER,
            "img_w": 350,
            "img_h": 218
        }
    ]

    current_row = 7
    for b in bugs:
        ws.row_dimensions[current_row].height = 205

        # Col A: STT
        ws[f"A{current_row}"] = b["stt"]
        ws[f"A{current_row}"].font = Font(name=FONT_NAME, size=11, bold=True, color="0F172A")
        ws[f"A{current_row}"].alignment = ALIGN_TOP_CENTER

        # Col B: Code & Location
        ws[f"B{current_row}"] = b["code"]
        ws[f"B{current_row}"].font = Font(name=FONT_NAME, size=9.5, bold=True, color="1E3A8A")
        ws[f"B{current_row}"].alignment = ALIGN_TOP_LEFT

        # Col C: Title
        ws[f"C{current_row}"] = b["title"]
        ws[f"C{current_row}"].font = Font(name=FONT_NAME, size=9.5, bold=True, color="0F172A")
        ws[f"C{current_row}"].alignment = ALIGN_TOP_LEFT

        # Col D: Retest Status
        ws[f"D{current_row}"] = b["status"]
        ws[f"D{current_row}"].font = Font(name=FONT_NAME, size=10, bold=True, color=b["status_color"])
        ws[f"D{current_row}"].fill = PatternFill(start_color=b["status_bg"], end_color=b["status_bg"], fill_type="solid")
        ws[f"D{current_row}"].alignment = ALIGN_TOP_CENTER

        # Col E: Verdict
        ws[f"E{current_row}"] = b["verdict"]
        ws[f"E{current_row}"].font = Font(name=FONT_NAME, size=9, color="0F172A")
        ws[f"E{current_row}"].alignment = ALIGN_TOP_LEFT

        # Col F: Guidance for Dev
        ws[f"F{current_row}"] = b["dev_guidance"]
        ws[f"F{current_row}"].font = Font(name=FONT_NAME, size=9, color="334155")
        ws[f"F{current_row}"].fill = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
        ws[f"F{current_row}"].alignment = ALIGN_TOP_LEFT

        # Apply borders
        for c_idx in range(1, 9):
            col_l = get_column_letter(c_idx)
            ws[f"{col_l}{current_row}"].border = BORDER_THIN

        # Col G: Photo Before
        if b["img_before"].exists():
            img_b = Image(str(b["img_before"]))
            img_b.width = b["img_w"]
            img_b.height = b["img_h"]
            ws.add_image(img_b, f"G{current_row}")

        # Col H: Photo After
        if b["img_after"].exists():
            img_a = Image(str(b["img_after"]))
            img_a.width = b["img_w"]
            img_a.height = b["img_h"]
            ws.add_image(img_a, f"H{current_row}")

        current_row += 1

    # -------------------------------------------------------------------------
    # 5. EXPANDED SECTION: 6 DETAILED LIVE SCREENSHOTS FOR BUG-01 (DEST-08)
    # -------------------------------------------------------------------------
    section_row = current_row + 1
    ws.merge_cells(f"A{section_row}:H{section_row}")
    ws[f"A{section_row}"] = "PHỤ LỤC: TOÀN BỘ 6 HÌNH ẢNH MINH CHỨNG CHI TIẾT CHO BUG-01 (DEST-08) VỪA CHỤP TRỰC TIẾP TRÊN HỆ THỐNG"
    ws[f"A{section_row}"].font = Font(name=FONT_NAME, size=12, bold=True, color="FFFFFF")
    ws[f"A{section_row}"].fill = PatternFill(start_color="991B1B", end_color="991B1B", fill_type="solid")
    ws[f"A{section_row}"].alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[section_row].height = 30

    section_sub = section_row + 1
    ws.merge_cells(f"A{section_sub}:H{section_sub}")
    ws[f"A{section_sub}"] = "Quy trình thực tế từ lúc gõ số âm, số 0, số cực lớn 999M SGD -> Bấm Next vượt qua -> Màn hình Review -> Xuất bản thành công vào CSDL"
    ws[f"A{section_sub}"].font = Font(name=FONT_NAME, size=9.5, italic=True, color="FFFFFF")
    ws[f"A{section_sub}"].fill = PatternFill(start_color="B91C1C", end_color="B91C1C", fill_type="solid")
    ws[f"A{section_sub}"].alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[section_sub].height = 20

    detail_header = section_sub + 1
    d_headers = [
        ("STT", 6),
        ("GIAI ĐOẠN / THAO TÁC", 22),
        ("DIỄN GIẢI HÀNH VI HỆ THỐNG & ĐÁNH GIÁ NGHIỆP VỤ", 45),
        ("HÌNH ẢNH CHỤP MINH CHỨNG THỰC TẾ (CHI TIẾT MÀN HÌNH)", 85),
    ]
    ws.row_dimensions[detail_header].height = 28

    ws[f"A{detail_header}"] = d_headers[0][0]
    ws[f"B{detail_header}"] = d_headers[1][0]
    ws.merge_cells(f"C{detail_header}:D{detail_header}")
    ws[f"C{detail_header}"] = d_headers[2][0]
    ws.merge_cells(f"E{detail_header}:H{detail_header}")
    ws[f"E{detail_header}"] = d_headers[3][0]

    for col in ["A", "B", "C", "D", "E", "F", "G", "H"]:
        cell = ws[f"{col}{detail_header}"]
        cell.font = Font(name=FONT_NAME, size=10, bold=True, color="FFFFFF")
        cell.fill = PatternFill(start_color="475569", end_color="475569", fill_type="solid")
        cell.alignment = ALIGN_CENTER
        cell.border = BORDER_THIN

    detail_row = detail_header + 1
    for step in BUG01_STEPS:
        ws.row_dimensions[detail_row].height = 240

        # Col A
        ws[f"A{detail_row}"] = step["stt"]
        ws[f"A{detail_row}"].font = Font(name=FONT_NAME, size=11, bold=True, color="0F172A")
        ws[f"A{detail_row}"].alignment = ALIGN_TOP_CENTER

        # Col B
        ws[f"B{detail_row}"] = step["stage"]
        ws[f"B{detail_row}"].font = Font(name=FONT_NAME, size=10, bold=True, color="1E3A8A")
        ws[f"B{detail_row}"].alignment = ALIGN_TOP_LEFT

        # Col C & D merged
        ws.merge_cells(f"C{detail_row}:D{detail_row}")
        ws[f"C{detail_row}"] = step["desc"]
        ws[f"C{detail_row}"].font = Font(name=FONT_NAME, size=9.5, color="0F172A")
        ws[f"C{detail_row}"].alignment = ALIGN_TOP_LEFT

        # Col E to H merged for Image
        ws.merge_cells(f"E{detail_row}:H{detail_row}")

        # Borders
        for c in ["A", "B", "C", "D", "E", "F", "G", "H"]:
            ws[f"{c}{detail_row}"].border = BORDER_THIN

        # Add image
        if step["img"].exists():
            img = Image(str(step["img"]))
            img.width = 540
            img.height = 310
            ws.add_image(img, f"E{detail_row}")

        detail_row += 1

    # 6. Save workbook
    wb.save(str(OUTPUT_FILE))
    # Also save fallback to /tmp
    wb.save("/tmp/BAO_CAO_RETEST_3_BUG_EDUFAMS.xlsx")
    print(f"✓ Successfully exported comprehensive retest report to: {OUTPUT_FILE}")


if __name__ == "__main__":
    build_retest_excel()
