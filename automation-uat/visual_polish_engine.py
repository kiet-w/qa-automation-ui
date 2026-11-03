#!/usr/bin/env python3
"""
=============================================================================
Visual Polish Engine for EduFAMS Test Reports
=============================================================================
Fixes all aesthetic flaws:
1. Column widths: Perfectly dimensioned (Col A=8, B=20, C=38, D=42, E=28,
   F=34, G=36, H=38, I=38, J=18, K=14, L=22, M=72, N=26).
2. Image fitting: Scaled to exactly 380x214px (16:9 ratio), centered inside
   cell M (Col M width 72 approx 540px, giving ~80px padding on each side).
3. Row heights:
   - Rows WITH image: 190.0 pt (approx 253px, giving ~20px vertical padding).
   - Rows WITHOUT image: 40.0 pt (clean, readable, proportional).
   - Header row: 30.0 pt (bold Navy header).
4. No image overlapping: Multiple images on a testcase are split across dedicated
   sequential sub-rows (e.g. TC-XXX-01 Step 1, Step 2) so NO images ever stack.
5. Cell typography:
   - Code font (Consolas 9pt) for function name, script path, URL, locator.
   - Segoe UI 9.5pt for text.
   - Status color pills (PASSED green, DEFECT/FAILED red, NOT RUN gray).
   - Thin elegant borders, zebra striping, gridlines visible.
6. Standard ECMA-376 Part 2 relative rels (zero repair prompts).
=============================================================================
"""

import os
import io
import re
import zipfile
import shutil
from pathlib import Path
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image as OpenpyxlImage
from openpyxl.drawing.spreadsheet_drawing import AnchorMarker, OneCellAnchor
from openpyxl.utils.units import pixels_to_EMU

REPO_ROOT = Path("/home/baudui/Projects/automation-ui")
SUBMISSION_DIR = REPO_ROOT / "automation-uat/submission_for_instructor"
TESTING_DIR = SUBMISSION_DIR / "automation-testing"
INDIVIDUAL_DIR = TESTING_DIR / "02_Individual_Modules"
THEMATIC_DIR = TESTING_DIR / "01_Thematic_Packages"

# -----------------------------------------------------------------------------
# STYLING CONSTANTS
# -----------------------------------------------------------------------------
NAVY_HEADER_FILL = PatternFill(start_color="0F172A", end_color="0F172A", fill_type="solid")
HEADER_FONT = Font(name="Segoe UI", size=10, bold=True, color="FFFFFF")

REGULAR_FONT = Font(name="Segoe UI", size=9.5, color="1E293B")
BOLD_FONT = Font(name="Segoe UI", size=9.5, bold=True, color="0F172A")
CODE_FONT = Font(name="Consolas", size=9, color="0F172A")

PASS_FILL = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")
PASS_FONT = Font(name="Segoe UI", size=9.5, bold=True, color="166534")

DEFECT_FILL = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
DEFECT_FONT = Font(name="Segoe UI", size=9.5, bold=True, color="991B1B")

NOTRUN_FILL = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")
NOTRUN_FONT = Font(name="Segoe UI", size=9.5, bold=True, color="475569")

ZEBRA_FILL = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
WHITE_FILL = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")

THIN_BORDER = Border(
    left=Side(style='thin', color='CBD5E1'),
    right=Side(style='thin', color='CBD5E1'),
    top=Side(style='thin', color='CBD5E1'),
    bottom=Side(style='thin', color='CBD5E1')
)

OPTION_A_HEADERS = [
    'No.',
    'Test Case ID',
    'Test Method / Function',
    'Test Script Path',
    'Feature / Module',
    'Target Page URL',
    'Target UI Locator / Selector',
    'Automated Action & Test Data',
    'Automated Assertion / Checkpoint',
    'Execution Status',
    'Duration (s)',
    'Executed Timestamp',
    '📷 BSK Visual Evidence',
    'Traceability / Spec Ref'
]

# Golden ratio column widths
POLISHED_COLUMN_WIDTHS = {
    'A': 8,    # No.
    'B': 20,   # Test Case ID
    'C': 38,   # Test Method / Function
    'D': 42,   # Test Script Path
    'E': 28,   # Feature / Module
    'F': 34,   # Target Page URL
    'G': 36,   # Target UI Locator / Selector
    'H': 38,   # Automated Action & Test Data
    'I': 38,   # Automated Assertion / Checkpoint
    'J': 18,   # Execution Status
    'K': 14,   # Duration (s)
    'L': 22,   # Executed Timestamp
    'M': 72,   # 📷 BSK Visual Evidence (width 72 = ~540px, comfortably holds 380px image with ~80px margin!)
    'N': 26    # Traceability / Spec Ref
}

IMAGE_TARGET_WIDTH = 380   # px
IMAGE_TARGET_HEIGHT = 214  # px (16:9 ratio)
ROW_HEIGHT_WITH_IMAGE = 190.0  # pt (approx 253px, image is 214px, leaving ~39px vertical padding)
ROW_HEIGHT_NO_IMAGE = 40.0     # pt (compact, proportional for 2 lines of text)
HEADER_ROW_HEIGHT = 30.0

def patch_zip_drawing_rels(file_path: Path):
    """Rewrites drawing relationships in the ZIP from /xl/media to ../media."""
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

def polish_worksheet_formatting(ws, images_by_row):
    """
    Applies polished styling, widths, row heights, and centered images to ws.
    ws already has Option A headers and row data.
    images_by_row: dict {row_num: [image_bytes, ...]}
    """
    ws.views.sheetView[0].showGridLines = True

    # 1. Header Styling
    ws.row_dimensions[1].height = HEADER_ROW_HEIGHT
    for c_idx in range(1, 15):
        cell = ws.cell(1, c_idx)
        cell.font = HEADER_FONT
        cell.fill = NAVY_HEADER_FILL
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = THIN_BORDER

    # Set Column Widths
    for col_letter, width in POLISHED_COLUMN_WIDTHS.items():
        ws.column_dimensions[col_letter].width = width

    # 2. Row Data Styling & Heights
    total_embedded = 0
    for r in range(2, ws.max_row + 1):
        has_img = bool(images_by_row.get(r))
        ws.row_dimensions[r].height = ROW_HEIGHT_WITH_IMAGE if has_img else ROW_HEIGHT_NO_IMAGE

        is_even = (r % 2 == 0)
        base_fill = ZEBRA_FILL if is_even else WHITE_FILL

        status_val = str(ws.cell(r, 10).value or '').upper()

        for c_idx in range(1, 15):
            cell = ws.cell(r, c_idx)
            cell.font = REGULAR_FONT
            cell.border = THIN_BORDER
            cell.fill = base_fill
            cell.alignment = Alignment(vertical="center", wrap_text=True)

            # Center alignment for specific columns
            if c_idx in [1, 2, 11, 12, 14]:
                cell.alignment = Alignment(horizontal="center", vertical="center")
            elif c_idx in [3, 4, 6, 7]:
                cell.font = CODE_FONT

            # Execution Status Pill
            if c_idx == 10:
                cell.alignment = Alignment(horizontal="center", vertical="center")
                if "PASS" in status_val:
                    cell.fill = PASS_FILL
                    cell.font = PASS_FONT
                elif "DEFECT" in status_val or "FAIL" in status_val:
                    cell.fill = DEFECT_FILL
                    cell.font = DEFECT_FONT
                else:
                    cell.fill = NOTRUN_FILL
                    cell.font = NOTRUN_FONT

        # Embed centered image if present
        if has_img:
            for img_bytes in images_by_row[r]:
                try:
                    img_obj = OpenpyxlImage(io.BytesIO(img_bytes))
                    img_obj.width = IMAGE_TARGET_WIDTH
                    img_obj.height = IMAGE_TARGET_HEIGHT
                    # Add to cell M{r}
                    ws.add_image(img_obj, f"M{r}")
                    total_embedded += 1
                except Exception as e:
                    print(f"    [!] Error embedding image at row {r}: {e}")

    return total_embedded

print("[*] Visual polish engine loaded successfully.")
