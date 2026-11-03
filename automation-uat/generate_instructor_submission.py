#!/usr/bin/env python3
"""
=============================================================================
Generate Teacher Submission Packages & Individual Single-Tab Workbooks
=============================================================================
This script exports:
1. 4 Thematic Domain Packages (Core UAT, Admin Portal, Parent Portal, GovTech)
2. 23 Dedicated Standalone 1-Tab Workbooks (One file per test suite)
3. ECMA-376 Standard Relative Rels Patch on EVERY generated workbook so that
   the teacher/instructor experiences zero repair alerts or missing images.
=============================================================================
"""

import os
import io
import time
import zipfile
import shutil
from copy import copy
from pathlib import Path
import openpyxl
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image
from PIL import Image as PILImage

BASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = BASE_DIR.parent
MASTER_FILE = BASE_DIR / "MASTER_TEST_EXECUTION_EVIDENCE_ALL_MODULES.xlsx"

SUBMISSION_DIR = BASE_DIR / "submission_for_instructor"
THEMATIC_DIR = SUBMISSION_DIR / "01_Thematic_Packages"
INDIVIDUAL_DIR = SUBMISSION_DIR / "02_Individual_Modules"

THEMATIC_PACKAGES = [
    (
        "PACKAGE_1_CORE_UAT_AND_ADVANCED_QUALITY_SUITE.xlsx",
        "Bộ Kiểm Thử Nghiệp Vụ Cốt Lõi, E2E, Destructive, Security & Bugs",
        [
            "Executive UAT Summary",
            "E2E UI Automation Flow",
            "8 Forms Destructive Tests",
            "Security & Perf Automation",
            "Date & Temporal Automation",
            "Defect UI Dossier",
        ],
    ),
    (
        "PACKAGE_2_ADMIN_PORTAL_AUTOMATION_5173.xlsx",
        "Bộ Kiểm Thử Toàn Diện Cổng Quản Trị Trường Học (localhost:5173)",
        [
            "FS03 School Create Evidence",
            "FS03 School User Evidence",
            "Drive 01 Admin Login",
            "Drive 02 Admin Dashboard",
            "Drive 03 School Mgmt",
            "Drive 04 School User Mgmt",
            "Drive 06 Class Mgmt",
            "5173_07_Student_Management",
            "5173_08_School_Config",
        ],
    ),
    (
        "PACKAGE_3_PARENT_CITIZEN_PORTAL_AUTOMATION_5174.xlsx",
        "Bộ Kiểm Thử Toàn Diện Cổng Dịch Vụ Công Phụ Huynh (localhost:5174)",
        [
            "FS08 Child Auth Evidence",
            "5174_01_Parent_Login",
            "5174_02_Citizen_Dashboard",
            "5174_03_Parent_Profile",
            "5174_06_Payment_Simulator",
            "FS08_Profile_104_Specs",
        ],
    ),
    (
        "PACKAGE_4_GOVTECH_PLAN_AND_CODE_INVARIANTS.xlsx",
        "Kế Hoạch Kiểm Thử UAT GovTech & Kiểm Định Bất Biến Kiến Trúc",
        [
            "GovTech_UAT_Test_Plan",
            "Automation_Unit_Invariants",
        ],
    ),
]

INDIVIDUAL_FILE_NAMES = {
    "Executive UAT Summary": "01_Executive_UAT_Summary.xlsx",
    "E2E UI Automation Flow": "02_E2E_Happy_Path_Automation_Flow.xlsx",
    "8 Forms Destructive Tests": "03_8_Forms_Destructive_Testing_Suite.xlsx",
    "Security & Perf Automation": "04_Security_and_Performance_Benchmark.xlsx",
    "Date & Temporal Automation": "05_Date_Testing_and_Temporal_Audit.xlsx",
    "Defect UI Dossier": "06_Comprehensive_Defect_UI_Dossier.xlsx",
    "FS03 School Create Evidence": "07_FS03_School_Create_Evidence.xlsx",
    "FS03 School User Evidence": "08_FS03_School_User_Create_Evidence.xlsx",
    "FS08 Child Auth Evidence": "09_FS08_Child_Authentication_and_IDOR.xlsx",
    "Drive 01 Admin Login": "10_Admin_Portal_01_Login_and_SSO.xlsx",
    "Drive 02 Admin Dashboard": "11_Admin_Portal_02_Dashboard_Shell.xlsx",
    "Drive 03 School Mgmt": "12_Admin_Portal_03_School_Management.xlsx",
    "Drive 04 School User Mgmt": "13_Admin_Portal_04_School_User_Management.xlsx",
    "Drive 06 Class Mgmt": "14_Admin_Portal_06_Class_Management.xlsx",
    "5173_07_Student_Management": "15_Admin_Portal_07_Student_Management.xlsx",
    "5173_08_School_Config": "16_Admin_Portal_08_School_Configuration.xlsx",
    "5174_01_Parent_Login": "17_Parent_Portal_01_Login_and_Mockpass.xlsx",
    "5174_02_Citizen_Dashboard": "18_Parent_Portal_02_Citizen_Dashboard.xlsx",
    "5174_03_Parent_Profile": "19_Parent_Portal_03_Profile_and_Contact.xlsx",
    "5174_06_Payment_Simulator": "20_Parent_Portal_06_Payment_Checkout_Simulator.xlsx",
    "FS08_Profile_104_Specs": "21_Parent_Portal_FS08_104_Specs_Audit.xlsx",
    "GovTech_UAT_Test_Plan": "22_GovTech_EduSave_UAT_Test_Plan.xlsx",
    "Automation_Unit_Invariants": "23_Automation_Unit_and_Architecture_Invariants.xlsx",
}


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


def copy_sheet(src_ws, dest_ws):
    """Deep-copies cells, styles, merged ranges, dimensions, and scaled images."""
    for col_letter, col_dim in src_ws.column_dimensions.items():
        dest_ws.column_dimensions[col_letter].width = col_dim.width
        dest_ws.column_dimensions[col_letter].hidden = col_dim.hidden

    for row_idx, row_dim in src_ws.row_dimensions.items():
        dest_ws.row_dimensions[row_idx].height = row_dim.height

    for row in src_ws.iter_rows():
        for cell in row:
            dest_cell = dest_ws.cell(row=cell.row, column=cell.column, value=cell.value)
            if cell.has_style:
                dest_cell.font = copy(cell.font)
                dest_cell.border = copy(cell.border)
                dest_cell.fill = copy(cell.fill)
                dest_cell.number_format = copy(cell.number_format)
                dest_cell.alignment = copy(cell.alignment)
            if cell.hyperlink:
                dest_cell.hyperlink = copy(cell.hyperlink)

    for merged_range in src_ws.merged_cells.ranges:
        dest_ws.merge_cells(str(merged_range))

    if src_ws.freeze_panes:
        dest_ws.freeze_panes = src_ws.freeze_panes
    dest_ws.views.sheetView[0].showGridLines = True

    imgs_copied = 0
    for img in src_ws._images:
        try:
            cell_ref = None
            if hasattr(img, "anchor"):
                if isinstance(img.anchor, str):
                    cell_ref = img.anchor
                elif hasattr(img.anchor, "_from"):
                    col = img.anchor._from.col
                    row = img.anchor._from.row
                    cell_ref = f"{get_column_letter(col + 1)}{row + 1}"
                elif hasattr(img.anchor, "from"):
                    col = getattr(img.anchor, "from").col
                    row = getattr(img.anchor, "from").row
                    cell_ref = f"{get_column_letter(col + 1)}{row + 1}"

            if not cell_ref:
                continue

            raw_data = img._data()
            new_img = Image(io.BytesIO(raw_data))
            new_img.width = img.width
            new_img.height = img.height
            dest_ws.add_image(new_img, cell_ref)
            imgs_copied += 1
        except Exception as e:
            print(f"      [WARN] Failed to copy image at {cell_ref}: {e}")

    return imgs_copied


def main():
    print("=" * 80)
    print("  GENERATING INSTRUCTOR SUBMISSION PACKAGES & INDIVIDUAL WORKBOOKS")
    print(f"  Source Master: {MASTER_FILE.name}")
    print("=" * 80)

    THEMATIC_DIR.mkdir(parents=True, exist_ok=True)
    INDIVIDUAL_DIR.mkdir(parents=True, exist_ok=True)

    print("\nLoading Master Workbook...")
    t0 = time.time()
    master_wb = openpyxl.load_workbook(MASTER_FILE)
    print(f"✓ Master Workbook loaded ({time.time() - t0:.2f}s). Total sheets: {len(master_wb.sheetnames)}")

    # -------------------------------------------------------------------------
    # PART 1: Generate 4 Thematic Domain Packages
    # -------------------------------------------------------------------------
    print("\n--- [PART 1/2] Generating 4 Thematic Domain Packages ---")
    for pkg_filename, pkg_desc, sheet_names in THEMATIC_PACKAGES:
        pkg_path = THEMATIC_DIR / pkg_filename
        print(f"\nBuilding: {pkg_filename}")
        print(f"  Description: {pkg_desc}")
        print(f"  Included Sheets ({len(sheet_names)}): {sheet_names}")

        pkg_wb = openpyxl.Workbook()
        pkg_wb.remove(pkg_wb.active)  # remove default sheet

        pkg_images = 0
        for sname in sheet_names:
            if sname not in master_wb.sheetnames:
                print(f"  [ERROR] Sheet not found in master: {sname}")
                continue
            src_ws = master_wb[sname]
            dest_ws = pkg_wb.create_sheet(title=sname[:31])
            copied_imgs = copy_sheet(src_ws, dest_ws)
            pkg_images += copied_imgs
            print(f"    + {sname:<30} ({dest_ws.max_row} rows, {copied_imgs} images)")

        pkg_wb.save(pkg_path)
        patched = patch_zip_drawing_rels(pkg_path)
        size_mb = os.path.getsize(pkg_path) / (1024 * 1024)
        print(f"  ✓ Saved {pkg_filename} ({size_mb:.2f} MB, {pkg_images} imgs, {patched} drawing rels patched)")

    # -------------------------------------------------------------------------
    # PART 2: Generate 23 Individual Single-Tab Workbooks
    # -------------------------------------------------------------------------
    print("\n--- [PART 2/2] Generating 23 Dedicated Single-Tab Workbooks ---")
    for sheet_name in master_wb.sheetnames:
        filename = INDIVIDUAL_FILE_NAMES.get(sheet_name, f"{sheet_name}.xlsx")
        file_path = INDIVIDUAL_DIR / filename
        print(f"\nExporting Single-Tab: {filename} <- [{sheet_name}]")

        ind_wb = openpyxl.Workbook()
        dest_ws = ind_wb.active
        dest_ws.title = sheet_name[:31]

        src_ws = master_wb[sheet_name]
        copied_imgs = copy_sheet(src_ws, dest_ws)

        ind_wb.save(file_path)
        patched = patch_zip_drawing_rels(file_path)
        size_mb = os.path.getsize(file_path) / (1024 * 1024)
        print(f"  ✓ Saved ({size_mb:.2f} MB, {dest_ws.max_row} rows, {copied_imgs} imgs, {patched} drawing rels patched)")

    # Copy Master Workbook directly into submission root for convenience
    dest_master = SUBMISSION_DIR / "00_EDUFAMS_MASTER_ALL_IN_ONE_TEST_REPORT.xlsx"
    shutil.copyfile(MASTER_FILE, dest_master)
    print(f"\n✓ Master Workbook synchronized to: {dest_master.name}")

    print("\n" + "=" * 80)
    print("  ALL SUBMISSION PACKAGES GENERATED SUCCESSFULLY!")
    print(f"  Output Directory: {SUBMISSION_DIR}")
    print("=" * 80)


if __name__ == "__main__":
    main()
