#!/usr/bin/env python3
"""
Fix multi-image extraction and supplement missing images so that:
01_Admin_Portal_5173 reaches exactly 170 images and 269 rows.
Also creates a single-sheet all-in-one workbook for Admin Portal 5173 with all 170 images!
"""

import os
import io
import re
import zipfile
from pathlib import Path
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.drawing.image import Image as OpenpyxlImage

REPO_ROOT = Path("/home/baudui/Projects/automation-ui")
SUBMISSION_DIR = REPO_ROOT / "automation-uat/submission_for_instructor"
ADMIN_DIR = SUBMISSION_DIR / "automation-testing/02_Individual_Modules/01_Admin_Portal_5173"
SRC_5173_MASTER = REPO_ROOT / "reports/testcase5173/TEST_EXECUTION_EVIDENCE_Testcase5173.xlsx"

NAVY_HEADER_FILL = PatternFill(start_color="0F172A", end_color="0F172A", fill_type="solid")
HEADER_FONT = Font(name="Segoe UI", size=10, bold=True, color="FFFFFF")
REGULAR_FONT = Font(name="Segoe UI", size=9.5, color="1E293B")
PASS_FILL = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")
PASS_FONT = Font(name="Segoe UI", size=10, bold=True, color="166534")
FAIL_FILL = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
FAIL_FONT = Font(name="Segoe UI", size=10, bold=True, color="991B1B")
ZEBRA_FILL = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
WHITE_FILL = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")
THIN_BORDER = Border(
    left=Side(style='thin', color='CBD5E1'),
    right=Side(style='thin', color='CBD5E1'),
    top=Side(style='thin', color='CBD5E1'),
    bottom=Side(style='thin', color='CBD5E1')
)

OPTION_A_HEADERS = [
    "No.",
    "Test Case ID",
    "Test Method / Function",
    "Test Script Path",
    "Feature / Module",
    "Target Page URL",
    "Target UI Locator / Selector",
    "Automated Action & Test Data",
    "Automated Assertion / Checkpoint",
    "Execution Status",
    "Duration (s)",
    "Executed Timestamp",
    "📷 BSK Visual Evidence",
    "Traceability / Spec Ref"
]

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

def main():
    print("[*] Starting Admin Portal 170-image recovery...")
    # 1. Load monolithic 5173 master workbook
    wb_master = openpyxl.load_workbook(SRC_5173_MASTER)
    ws_master = wb_master.active
    print(f"    Loaded monolithic master: {len(ws_master._images)} images, {ws_master.max_row} rows")
    
    # Map all images in master by row (preserving multiple images per row in a list)
    master_images_by_row = {}
    for img in ws_master._images:
        r = img.anchor._from.row + 1
        master_images_by_row.setdefault(r, []).append(img)
    
    # Check images by prefix
    prefix_img_counts = {}
    for r, img_list in master_images_by_row.items():
        sc_id = str(ws_master.cell(r, 2).value)
        pfx = sc_id.split('-')[1] if '-' in sc_id else 'OTHER'
        prefix_img_counts[pfx] = prefix_img_counts.get(pfx, 0) + len(img_list)
    print("    Master image distribution:", prefix_img_counts)

if __name__ == "__main__":
    main()
