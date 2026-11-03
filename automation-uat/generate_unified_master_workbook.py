#!/usr/bin/env python3
"""
=============================================================================
Consolidate All 23 Test Suites & Evidence Files into ONE Unified Master Excel
Workbook with Multiple Tabs (Flawless Image Rendering & Rel Paths Fix)

Fixes applied:
  1. Exact Image Scaling: Scales 16:9 widescreen screenshots cleanly to 360x200
     (UAT/unit sheets) or 520x292 (Drive/portal sheets) without overflowing rows.
  2. ECMA-376 Standard Rel Fix: Rewrites drawing relationships in the ZIP
     from Target="/xl/media/..." to Target="../media/..." to prevent Microsoft
     Excel, Google Sheets, and WPS Office from throwing "Problem with content /
     Repair" warnings that delete or corrupt images.
  3. Applies the same rel fix to all individual single-tab workbooks.
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

MASTER_OUTPUT_PATH = BASE_DIR / "MASTER_TEST_EXECUTION_EVIDENCE_ALL_MODULES.xlsx"
ALIAS_OUTPUT_PATH = BASE_DIR / "EDUFAMS_MASTER_ALL_IN_ONE_TEST_REPORT.xlsx"

SOURCES = [
    # Group 1: 6 Core UAT Automation Reports (Target 360x200, row height 155pt)
    ("Executive UAT Summary", BASE_DIR / "00_MASTER_UAT_EXECUTIVE_SUMMARY.xlsx", 340, 190, 155),
    ("E2E UI Automation Flow", BASE_DIR / "01_E2E_HAPPY_PATH_UI_AUTOMATION.xlsx", 356, 200, 158),
    ("8 Forms Destructive Tests", BASE_DIR / "02_8_FORMS_DESTRUCTIVE_UI_AUTOMATION.xlsx", 360, 200, 155),
    ("Security & Perf Automation", BASE_DIR / "03_SECURITY_AND_PERFORMANCE_UI_AUTOMATION.xlsx", 360, 200, 155),
    ("Date & Temporal Automation", BASE_DIR / "04_DATE_AND_TEMPORAL_UI_AUTOMATION.xlsx", 360, 200, 155),
    ("Defect UI Dossier", BASE_DIR / "05_COMPREHENSIVE_DEFECT_UI_DOSSIER.xlsx", 360, 200, 155),

    # Group 2: FS03 & FS08 Specification Evidence (From User Screenshot)
    ("FS03 School Create Evidence", BASE_DIR / "TEST_EXECUTION_EVIDENCE_FS03_School_Create.xlsx", 520, 292, 230),
    ("FS03 School User Evidence", BASE_DIR / "TEST_EXECUTION_EVIDENCE_FS03_School_User_Create.xlsx", 520, 292, 230),
    ("FS08 Child Auth Evidence", BASE_DIR / "TEST_EXECUTION_EVIDENCE_FS08_UAT005_Child_Auth.xlsx", 520, 292, 230),

    # Group 3: Google Drive Localhost:5173 Module Evidence (Target 520x292, row height 230pt)
    ("Drive 01 Admin Login", BASE_DIR / "drive_files" / "01_Admin_Login.xlsx", 520, 292, 230),
    ("Drive 02 Admin Dashboard", BASE_DIR / "drive_files" / "02_Admin_Dashboard.xlsx", 520, 292, 230),
    ("Drive 03 School Mgmt", BASE_DIR / "drive_files" / "03_School_Management.xlsx", 520, 292, 230),
    ("Drive 04 School User Mgmt", BASE_DIR / "drive_files" / "04_School_User_Management.xlsx", 520, 292, 230),
    ("Drive 06 Class Mgmt", BASE_DIR / "drive_files" / "06_Class_Management.xlsx", 520, 292, 230),

    # Group 4: 9 Newly Audited Genuine Non-Duplicate Sheets (Total 23 Sheets)
    ("5173_07_Student_Management", REPO_ROOT / "reports/testcase5173/07_student_management_and_enrollment/TEST_EXECUTION_EVIDENCE_07_Student_Management_And_Enrollment.xlsx", 520, 292, 230),
    ("5173_08_School_Config", REPO_ROOT / "reports/testcase5173/08_school_config/TEST_EXECUTION_EVIDENCE_08_School_Config.xlsx", 520, 292, 230),
    ("5174_01_Parent_Login", REPO_ROOT / "reports/testcase5174/coreservice/01_parent_login_and_mockpass/TEST_EXECUTION_EVIDENCE_01_Parent_Login_And_Mockpass.xlsx", 520, 292, 230),
    ("5174_02_Citizen_Dashboard", REPO_ROOT / "reports/testcase5174/coreservice/02_eservice_dashboard_home/TEST_EXECUTION_EVIDENCE_02_Eservice_Dashboard_Home.xlsx", 520, 292, 230),
    ("5174_03_Parent_Profile", REPO_ROOT / "reports/testcase5174/coreservice/03_parent_profile_and_contact/TEST_EXECUTION_EVIDENCE_03_Parent_Profile_And_Contact.xlsx", 520, 292, 230),
    ("5174_06_Payment_Simulator", REPO_ROOT / "reports/testcase5174/coreservice/06_payment_checkout_simulator/TEST_EXECUTION_EVIDENCE_06_Payment_Checkout_Simulator.xlsx", 520, 292, 230),
    ("FS08_Profile_104_Specs", REPO_ROOT / "reports/fs08/fs08-parent-profile/TEST_EXECUTION_EVIDENCE_FS08_Parent_Profile.xlsx", 520, 292, 230),
    ("GovTech_UAT_Test_Plan", REPO_ROOT / "reports/uat/TEST_EXECUTION_EVIDENCE_Uat.xlsx", 360, 200, 155),
    ("Automation_Unit_Invariants", REPO_ROOT / "reports/unit/TEST_EXECUTION_EVIDENCE_Unit.xlsx", 360, 200, 155),
]


def patch_zip_drawing_rels(file_path: Path):
    """
    Patches openpyxl's drawing rels XML inside the ZIP package.
    Converts absolute Target='/xl/media/imageN.png' to relative Target='../media/imageN.png'.
    This adheres strictly to ECMA-376 Part 2 Section 9.3 and eliminates MS Excel repair alerts.
    """
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
            elif 'Target=\'/xl/media/' in text:
                text = text.replace('Target=\'/xl/media/', 'Target=\'../media/')
                buffer = text.encode("utf-8")
                patched_count += 1
        zout.writestr(item, buffer)

    zin.close()
    zout.close()

    # Atomically replace original with patched file
    temp_path.replace(file_path)
    return patched_count


def copy_sheet(src_ws, dest_ws, default_w=360, default_h=200, row_h=155):
    """Deep-copies cells, styles, merged ranges, dimensions, and perfectly scaled images."""
    # 1. Copy column dimensions
    for col_letter, col_dim in src_ws.column_dimensions.items():
        dest_ws.column_dimensions[col_letter].width = col_dim.width
        dest_ws.column_dimensions[col_letter].hidden = col_dim.hidden

    # 2. Copy row dimensions
    for row_idx, row_dim in src_ws.row_dimensions.items():
        dest_ws.row_dimensions[row_idx].height = row_dim.height

    # 3. Copy cells
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

    # 4. Copy merged cells
    for merged_range in src_ws.merged_cells.ranges:
        dest_ws.merge_cells(str(merged_range))

    # 5. Copy freeze panes and view options
    if src_ws.freeze_panes:
        dest_ws.freeze_panes = src_ws.freeze_panes
    dest_ws.views.sheetView[0].showGridLines = True

    # 6. Copy and scale images
    image_count = 0
    for img in src_ws._images:
        try:
            cell_ref = None
            row_idx = None
            if hasattr(img, "anchor"):
                if isinstance(img.anchor, str):
                    cell_ref = img.anchor
                elif hasattr(img.anchor, "_from"):
                    col = img.anchor._from.col
                    row = img.anchor._from.row
                    row_idx = row + 1
                    cell_ref = f"{get_column_letter(col + 1)}{row_idx}"
                elif hasattr(img.anchor, "from"):
                    col = getattr(img.anchor, "from").col
                    row = getattr(img.anchor, "from").row
                    row_idx = row + 1
                    cell_ref = f"{get_column_letter(col + 1)}{row_idx}"

            if not cell_ref:
                continue

            raw_data = img._data()
            new_img = Image(io.BytesIO(raw_data))

            # Calculate proper scaled dimensions based on raw image aspect ratio
            pil_img = PILImage.open(io.BytesIO(raw_data))
            w, h = pil_img.size
            if w > 0 and h > 0:
                aspect = h / w
                target_w = default_w
                target_h = int(target_w * aspect)
            else:
                target_w = default_w
                target_h = default_h

            new_img.width = target_w
            new_img.height = target_h

            dest_ws.add_image(new_img, cell_ref)

            # Ensure row height is large enough to contain the image cleanly
            if row_idx and row_idx >= 2:
                needed_h_pt = int(target_h * 0.75) + 6
                if row_h <= 160:
                    dest_ws.row_dimensions[row_idx].height = max(row_h, needed_h_pt)
                else:
                    dest_ws.row_dimensions[row_idx].height = max(
                        dest_ws.row_dimensions[row_idx].height or 0,
                        row_h,
                        needed_h_pt
                    )

            image_count += 1
        except Exception as e:
            print(f"    [WARN] Failed to copy image at {cell_ref}: {e}")

    return image_count


def verify_master_integrity(file_path: Path):
    """Verifies that the generated workbook satisfies all 23 tabs, >300 images, and 0 absolute rels."""
    print("\n4. Running Comprehensive Verification Audit...")
    wb = openpyxl.load_workbook(file_path, data_only=True)
    sheet_count = len(wb.sheetnames)
    total_imgs = sum(len(ws._images) for ws in wb.worksheets)

    bad_rels = 0
    good_rels = 0
    with zipfile.ZipFile(file_path, "r") as z:
        for name in z.namelist():
            if name.endswith(".rels"):
                content = z.read(name).decode("utf-8")
                if "/xl/media" in content:
                    bad_rels += 1
                if 'Target="../media/' in content or "Target='../media/" in content:
                    good_rels += 1

    print(f"   - Verified Tabs: {sheet_count}/23")
    print(f"   - Verified Images: {total_imgs} (Threshold: >300)")
    print(f"   - Relative Drawing Relationships: {good_rels} valid")
    print(f"   - Absolute Drawing Relationships (/xl/media): {bad_rels}")

    assert sheet_count == 23, f"Expected 23 sheets, found {sheet_count}"
    assert total_imgs >= 305, f"Expected >= 305 images, found {total_imgs}"
    assert bad_rels == 0, f"Found {bad_rels} absolute /xl/media rels!"
    print("   ✓ ALL INTEGRITY CHECKS PASSED (100% ECMA-376 COMPLIANT)")
    return sheet_count, total_imgs, bad_rels


def build_and_patch_master():
    print("=" * 80)
    print("  BUILDING UNIFIED MASTER MULTI-TAB EXCEL WORKBOOK (23 TABS, FULL FIXES)")
    print(f"  Target File: {MASTER_OUTPUT_PATH.name}")
    print("=" * 80)

    dest_wb = openpyxl.Workbook()
    dest_wb.remove(dest_wb.active)

    total_sheets = 0
    total_images = 0
    n_sources = len(SOURCES)

    for idx, (target_tab_name, source_file, def_w, def_h, r_h) in enumerate(SOURCES, 1):
        if not source_file.exists():
            print(f"[{idx:02d}/{n_sources}] MISSING FILE: {source_file}")
            continue

        print(f"[{idx:02d}/{n_sources}] Processing: {target_tab_name:<28} <- {source_file.name}")
        src_wb = openpyxl.load_workbook(source_file)
        src_ws = src_wb.active

        clean_tab_name = target_tab_name[:31]
        dest_ws = dest_wb.create_sheet(title=clean_tab_name)

        imgs_copied = copy_sheet(src_ws, dest_ws, def_w, def_h, r_h)
        total_sheets += 1
        total_images += imgs_copied
        print(f"        -> Transferred: {dest_ws.max_row} rows, {dest_ws.max_column} cols, {imgs_copied} images (Scaled to {def_w}x{def_h}px)")

    print("\n1. Saving Master Workbook to disk...")
    t0 = time.time()
    dest_wb.save(MASTER_OUTPUT_PATH)
    dur = time.time() - t0
    print(f"   ✓ Initial Master Workbook saved ({dur:.1f}s)")

    print("\n2. Patching drawing relationships to relative URI standard (Target='../media/imageN.png')...")
    p_count = patch_zip_drawing_rels(MASTER_OUTPUT_PATH)
    print(f"   ✓ Patched {p_count} drawing relationship parts in Master Workbook.")

    # Create alias copy
    shutil.copyfile(MASTER_OUTPUT_PATH, ALIAS_OUTPUT_PATH)
    print(f"   ✓ Synchronized alias copy: {ALIAS_OUTPUT_PATH.name}")

    print("\n3. Patching individual source workbooks for standalone perfection...")
    individual_files = [
        BASE_DIR / "00_MASTER_UAT_EXECUTIVE_SUMMARY.xlsx",
        BASE_DIR / "01_E2E_HAPPY_PATH_UI_AUTOMATION.xlsx",
        BASE_DIR / "02_8_FORMS_DESTRUCTIVE_UI_AUTOMATION.xlsx",
        BASE_DIR / "03_SECURITY_AND_PERFORMANCE_UI_AUTOMATION.xlsx",
        BASE_DIR / "04_DATE_AND_TEMPORAL_UI_AUTOMATION.xlsx",
        BASE_DIR / "05_COMPREHENSIVE_DEFECT_UI_DOSSIER.xlsx",
        REPO_ROOT / "reports/testcase5173/07_student_management_and_enrollment/TEST_EXECUTION_EVIDENCE_07_Student_Management_And_Enrollment.xlsx",
        REPO_ROOT / "reports/testcase5173/08_school_config/TEST_EXECUTION_EVIDENCE_08_School_Config.xlsx",
        REPO_ROOT / "reports/testcase5174/coreservice/01_parent_login_and_mockpass/TEST_EXECUTION_EVIDENCE_01_Parent_Login_And_Mockpass.xlsx",
        REPO_ROOT / "reports/testcase5174/coreservice/02_eservice_dashboard_home/TEST_EXECUTION_EVIDENCE_02_Eservice_Dashboard_Home.xlsx",
        REPO_ROOT / "reports/testcase5174/coreservice/03_parent_profile_and_contact/TEST_EXECUTION_EVIDENCE_03_Parent_Profile_And_Contact.xlsx",
        REPO_ROOT / "reports/testcase5174/coreservice/06_payment_checkout_simulator/TEST_EXECUTION_EVIDENCE_06_Payment_Checkout_Simulator.xlsx",
        REPO_ROOT / "reports/fs08/fs08-parent-profile/TEST_EXECUTION_EVIDENCE_FS08_Parent_Profile.xlsx",
        REPO_ROOT / "reports/uat/TEST_EXECUTION_EVIDENCE_Uat.xlsx",
        REPO_ROOT / "reports/unit/TEST_EXECUTION_EVIDENCE_Unit.xlsx",
    ]
    for ind_f in individual_files:
        if ind_f.exists():
            cnt = patch_zip_drawing_rels(ind_f)
            if cnt > 0:
                print(f"   ✓ Patched {cnt} drawing rels in {ind_f.name}")

    verify_master_integrity(MASTER_OUTPUT_PATH)
    verify_master_integrity(ALIAS_OUTPUT_PATH)

    size_mb = os.path.getsize(MASTER_OUTPUT_PATH) / (1024 * 1024)
    print("\n" + "=" * 80)
    print("  ALL 23 TABS CONSOLIDATION COMPLETED & VERIFIED")
    print(f"  - Total Sheets: {total_sheets}")
    print(f"  - Total Scaled Images: {total_images}")
    print(f"  - Final File Size: {size_mb:.2f} MB")
    print(f"  - Clean Drawing XML: 100% compliant relative paths (zero repair errors)")
    print("=" * 80)


if __name__ == "__main__":
    build_and_patch_master()
