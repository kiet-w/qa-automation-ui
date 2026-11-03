#!/usr/bin/env python3
"""
=============================================================================
Consolidate Option A Packages & Master Workbook
Rebuilds:
- 01_Thematic_Packages/ (PACKAGE 1, 2, 3, 4)
- 00_EDUFAMS_MASTER_ALL_IN_ONE_TEST_REPORT.xlsx
- Patches all drawing rels to ECMA-376 Part 2
=============================================================================
"""

import os
import re
import io
import zipfile
import shutil
from pathlib import Path
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image as OpenpyxlImage

REPO_ROOT = Path("/home/baudui/Projects/automation-ui")
SUBMISSION_DIR = REPO_ROOT / "automation-uat/submission_for_instructor"
TESTING_DIR = SUBMISSION_DIR / "automation-testing"
INDIVIDUAL_DIR = TESTING_DIR / "02_Individual_Modules"
THEMATIC_DIR = TESTING_DIR / "01_Thematic_Packages"

CORE_DIR = INDIVIDUAL_DIR / "00_Core_and_Executive"
ADMIN_DIR = INDIVIDUAL_DIR / "01_Admin_Portal_5173"
PARENT_DIR = INDIVIDUAL_DIR / "02_Parent_Citizen_Portal_5174"
ADVANCED_DIR = INDIVIDUAL_DIR / "03_Advanced_Quality_Suite"

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
    'M': 72,   # 📷 BSK Visual Evidence
    'N': 26    # Traceability / Spec Ref
}

def copy_sheet_with_images(src_ws, dest_ws, temp_prefix=""):
    dest_ws.views.sheetView[0].showGridLines = True
    if dest_ws.title != "Executive Summary":
        dest_ws.freeze_panes = "C2"
        dest_ws.auto_filter.ref = f"A1:N{src_ws.max_row}"
    if src_ws.sheet_properties and src_ws.sheet_properties.tabColor:
        dest_ws.sheet_properties.tabColor = src_ws.sheet_properties.tabColor
    
    # 1. Copy row dimensions & cell contents
    for r_idx in range(1, src_ws.max_row + 1):
        h = src_ws.row_dimensions[r_idx].height
        if h:
            dest_ws.row_dimensions[r_idx].height = h
        for c_idx in range(1, src_ws.max_column + 1):
            src_cell = src_ws.cell(r_idx, c_idx)
            dest_cell = dest_ws.cell(r_idx, c_idx, src_cell.value)
            if src_cell.has_style:
                dest_cell.font = Font(
                    name=src_cell.font.name,
                    size=src_cell.font.size,
                    bold=src_cell.font.bold,
                    italic=src_cell.font.italic,
                    color=src_cell.font.color
                )
                if src_cell.fill and src_cell.fill.fill_type:
                    dest_cell.fill = PatternFill(
                        fill_type=src_cell.fill.fill_type,
                        start_color=src_cell.fill.start_color,
                        end_color=src_cell.fill.end_color
                    )
                if src_cell.border:
                    dest_cell.border = Border(
                        left=Side(style=src_cell.border.left.style, color=src_cell.border.left.color) if src_cell.border.left else None,
                        right=Side(style=src_cell.border.right.style, color=src_cell.border.right.color) if src_cell.border.right else None,
                        top=Side(style=src_cell.border.top.style, color=src_cell.border.top.color) if src_cell.border.top else None,
                        bottom=Side(style=src_cell.border.bottom.style, color=src_cell.border.bottom.color) if src_cell.border.bottom else None,
                    )
                if src_cell.alignment:
                    dest_cell.alignment = Alignment(
                        horizontal=src_cell.alignment.horizontal,
                        vertical=src_cell.alignment.vertical,
                        wrap_text=src_cell.alignment.wrap_text
                    )

    # 2. Set column widths
    if dest_ws.title == "Executive Summary":
        exec_widths = {'A': 16, 'B': 50, 'C': 22, 'D': 22, 'E': 22, 'F': 20, 'G': 20, 'H': 20}
        for col_letter, width in exec_widths.items():
            dest_ws.column_dimensions[col_letter].width = width
    else:
        for col_letter, width in POLISHED_COLUMN_WIDTHS.items():
            dest_ws.column_dimensions[col_letter].width = width

    # 3. Copy Images
    temp_files = []
    for idx, img in enumerate(src_ws._images):
        try:
            row_num = None
            if isinstance(img.anchor, str):
                nums = re.findall(r'\d+', img.anchor)
                if nums:
                    row_num = int(nums[0])
            elif hasattr(img.anchor, '_from') and hasattr(img.anchor._from, 'row'):
                row_num = img.anchor._from.row + 1

            if row_num:
                t_path = REPO_ROOT / f"/tmp/{temp_prefix}_img_{idx}_{row_num}.png"
                with open(t_path, "wb") as f_out:
                    f_out.write(img._data())
                temp_files.append(t_path)
                
                img_obj = OpenpyxlImage(str(t_path))
                img_obj.width = 380
                img_obj.height = 214
                dest_ws.add_image(img_obj, f"M{row_num}")
                dest_ws.row_dimensions[row_num].height = 190.0
        except Exception as e:
            pass
            
    return temp_files

def build_package(dest_path: Path, src_files: list):
    print(f"[*] Building package {dest_path.name} from {len(src_files)} modules...")
    dest_wb = openpyxl.Workbook()
    # remove default sheet
    default_sheet = dest_wb.active

    all_temp_files = []
    for idx, (title, src_file) in enumerate(src_files):
        if not src_file.exists():
            print(f"    [!] Skipping missing: {src_file.name}")
            continue
        src_wb = openpyxl.load_workbook(src_file)
        src_ws = src_wb.active
        clean_title = title[:31]
        dest_ws = dest_wb.create_sheet(title=clean_title)
        t_files = copy_sheet_with_images(src_ws, dest_ws, f"pkg_{dest_path.stem}_{idx}")
        all_temp_files.extend(t_files)
        src_wb.close()
        print(f"    + Sheet: {clean_title} ({src_ws.max_row} rows, {len(t_files)} images)")

    # remove default sheet if other sheets exist
    if len(dest_wb.sheetnames) > 1:
        dest_wb.remove(default_sheet)

    dest_wb.save(dest_path)
    dest_wb.close()

    for t in all_temp_files:
        if t.exists():
            t.unlink()

    patched = patch_zip_drawing_rels(dest_path)
    print(f"  [✓] Saved {dest_path.name} ({len(dest_wb.sheetnames)} sheets, {patched} rels patched).")

def consolidate_all():
    THEMATIC_DIR.mkdir(parents=True, exist_ok=True)

    # 1. PACKAGE 1: Core & Advanced Quality Suite
    pkg1_sources = [
        ("Executive Summary", CORE_DIR / "00_Core_01_Executive_UAT_Summary.xlsx"),
        ("E2E Happy Path", CORE_DIR / "00_Core_02_E2E_Happy_Path_Automation_Flow.xlsx"),
        ("8 Forms Destructive", ADVANCED_DIR / "03_Advanced_01_8_Forms_Destructive_Testing_Suite.xlsx"),
        ("Security & Perf", ADVANCED_DIR / "03_Advanced_02_Security_and_Performance_Benchmark.xlsx"),
        ("Date & Temporal", ADVANCED_DIR / "03_Advanced_03_Date_Testing_and_Temporal_Audit.xlsx"),
        ("Defect UI Dossier", ADVANCED_DIR / "03_Advanced_04_Comprehensive_Defect_UI_Dossier.xlsx"),
    ]
    build_package(THEMATIC_DIR / "PACKAGE_1_CORE_UAT_AND_ADVANCED_QUALITY_SUITE.xlsx", pkg1_sources)

    # 2. PACKAGE 2: Admin Portal 5173
    pkg2_sources = [
        ("01 Admin Login & SSO", ADMIN_DIR / "01_Admin_01_Login_and_SSO.xlsx"),
        ("02 Dashboard Shell", ADMIN_DIR / "01_Admin_02_Dashboard_Shell.xlsx"),
        ("03 School Management", ADMIN_DIR / "01_Admin_03_School_Management.xlsx"),
        ("03 School Spec Matrix", ADMIN_DIR / "01_Admin_03_School_Create_Spec_Matrix.xlsx"),
        ("04 School User Mgmt", ADMIN_DIR / "01_Admin_04_School_User_Management.xlsx"),
        ("04 User Spec Matrix", ADMIN_DIR / "01_Admin_04_School_User_Spec_Matrix.xlsx"),
        ("05 Academic Years", ADMIN_DIR / "01_Admin_05_Academic_Years_and_Levels.xlsx"),
        ("06 Class Management", ADMIN_DIR / "01_Admin_06_Class_Management.xlsx"),
        ("07 Student Management", ADMIN_DIR / "01_Admin_07_Student_Management.xlsx"),
        ("08 School Configuration", ADMIN_DIR / "01_Admin_08_School_Configuration.xlsx"),
        ("09 Fee Batches & Mgmt", ADMIN_DIR / "01_Admin_09_Fee_Batches_and_Fee_Management.xlsx"),
        ("10 Support Console", ADMIN_DIR / "01_Admin_10_Support_Console_and_Audit.xlsx"),
    ]
    build_package(THEMATIC_DIR / "PACKAGE_2_ADMIN_PORTAL_AUTOMATION_5173.xlsx", pkg2_sources)

    # 3. PACKAGE 3: Parent Citizen Portal 5174
    pkg3_sources = [
        ("01 Parent Login", PARENT_DIR / "02_Parent_01_Login_and_Mockpass.xlsx"),
        ("02 Citizen Dashboard", PARENT_DIR / "02_Parent_02_Citizen_Dashboard.xlsx"),
        ("03 Profile & Contact", PARENT_DIR / "02_Parent_03_Profile_and_Contact.xlsx"),
        ("04 FAS Application Wizard", PARENT_DIR / "02_Parent_04_FAS_Application_Wizard.xlsx"),
        ("05 AI Assistant & Tour", PARENT_DIR / "02_Parent_05_AI_Assistant_and_Guided_Tour.xlsx"),
        ("06 Payment Simulator", PARENT_DIR / "02_Parent_06_Payment_Checkout_Simulator.xlsx"),
        ("07 Child Auth & IDOR", PARENT_DIR / "02_Parent_07_Child_Authentication_and_IDOR.xlsx"),
        ("08 FSD 104 Specs Audit", PARENT_DIR / "02_Parent_08_FSD_104_Specs_Compliance_Audit.xlsx"),
    ]
    build_package(THEMATIC_DIR / "PACKAGE_3_PARENT_CITIZEN_PORTAL_AUTOMATION_5174.xlsx", pkg3_sources)

    # 4. PACKAGE 4: GovTech Plan & Code Invariants
    pkg4_sources = [
        ("GovTech UAT Plan", CORE_DIR / "00_Core_03_GovTech_EduSave_UAT_Test_Plan.xlsx"),
        ("Code Invariants", CORE_DIR / "00_Core_04_Automation_Unit_and_Architecture_Invariants.xlsx"),
    ]
    build_package(THEMATIC_DIR / "PACKAGE_4_GOVTECH_PLAN_AND_CODE_INVARIANTS.xlsx", pkg4_sources)

    # 5. MASTER ALL-IN-ONE WORKBOOK
    master_sources = (
        pkg1_sources[:2] +
        pkg2_sources +
        pkg3_sources +
        pkg1_sources[2:] +
        pkg4_sources
    )
    build_package(SUBMISSION_DIR / "00_EDUFAMS_MASTER_ALL_IN_ONE_TEST_REPORT.xlsx", master_sources)

if __name__ == "__main__":
    consolidate_all()
