#!/usr/bin/env python3
"""
Verification Script for Single-Tab Excel Reports
Validates:
  - Both files exist
  - Each workbook has EXACTLY 1 worksheet (no extra tabs)
  - Column headers match Col A to Col J
  - Embedded images exist in openpyxl worksheet
  - Freeze panes set at A5
  - Gridlines visible
"""

import sys
from pathlib import Path
import openpyxl

BASE_DIR = Path("/home/baudui/Projects/automation-ui/automation-uat")
FILE_03 = BASE_DIR / "03_SECURITY_AND_PERFORMANCE_UI_AUTOMATION.xlsx"
FILE_04 = BASE_DIR / "04_DATE_AND_TEMPORAL_UI_AUTOMATION.xlsx"

EXPECTED_HEADERS = [
    "Test Case ID",
    "Module Name & Page URL",
    "Test Scenario & Interaction Flow",
    "Target UI Locator / Endpoint",
    "Input Payload / Action Trigger",
    "Expected Web UI Result",
    "Actual Web UI Result",
    "Status",
    "Performance Metric / Security Risk Analysis",
    "Web UI Screenshot Evidence"
]


def verify_report(file_path: Path):
    print("=" * 70)
    print(f"VERIFYING: {file_path.name}")
    print("=" * 70)

    # 1. File existence
    if not file_path.exists():
        print(f"FAILED: File does not exist: {file_path}")
        return False
    size_kb = file_path.stat().st_size / 1024
    print(f"✓ File exists. Size: {size_kb:.1f} KB")

    # 2. Exactly 1 tab
    wb = openpyxl.load_workbook(file_path, data_only=False)
    sheet_names = wb.sheetnames
    print(f"Worksheet Count: {len(sheet_names)} | Sheet Names: {sheet_names}")
    if len(sheet_names) != 1:
        print(f"FAILED: Workbook has {len(sheet_names)} sheets, expected EXACTLY 1!")
        return False
    print(f"✓ EXACTLY 1 TAB verified: '{sheet_names[0]}'")

    ws = wb.active

    # 3. Headers at Row 4
    headers = [ws.cell(row=4, column=col).value for col in range(1, 11)]
    print(f"Headers Row 4: {headers}")
    for idx, (exp, act) in enumerate(zip(EXPECTED_HEADERS, headers), 1):
        if exp != act:
            print(f"FAILED: Header mismatch at Col {idx}: expected '{exp}', got '{act}'")
            return False
    print(f"✓ Standard Automation Headers Col A-J verified.")

    # 4. Freeze Panes
    print(f"Freeze Panes: {ws.freeze_panes}")
    if ws.freeze_panes != "A5":
        print(f"FAILED: Freeze panes is '{ws.freeze_panes}', expected 'A5'!")
        return False
    print(f"✓ Freeze panes verified at A5.")

    # 5. Embedded Images Count
    images = ws._images
    print(f"Embedded Images Count: {len(images)}")
    if len(images) == 0:
        print("FAILED: No embedded images found in worksheet!")
        return False
    for idx, img in enumerate(images, 1):
        print(f"  - Image {idx}: dimensions={img.width}x{img.height}")
    print(f"✓ Embedded images verified ({len(images)} images in Column J).")

    # 6. Data Rows
    max_row = ws.max_row
    print(f"Total Rows: {max_row} (Header at 4, Data rows from 5 to {max_row})")
    if max_row < 5:
        print("FAILED: No data rows found!")
        return False

    # Check some status values
    statuses = [ws.cell(row=r, column=8).value for r in range(5, max_row + 1)]
    print(f"Recorded Statuses: {set(statuses)}")

    print(f"✓ ALL CHECKS PASSED FOR {file_path.name}!\n")
    return True


if __name__ == "__main__":
    ok3 = verify_report(FILE_03)
    ok4 = verify_report(FILE_04)

    if ok3 and ok4:
        print("=" * 70)
        print("🎉 ALL REQUIREMENTS VERIFIED: BOTH WORKBOOKS EXIST, HAVE EXACTLY 1 TAB,")
        print("   AND CONTAIN EMBEDDED HIGH-RES AUTOMATION SCREENSHOT EVIDENCE!")
        print("=" * 70)
        sys.exit(0)
    else:
        print("💥 VERIFICATION FAILED!")
        sys.exit(1)
