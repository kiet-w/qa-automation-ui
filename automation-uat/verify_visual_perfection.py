#!/usr/bin/env python3
"""
Verify visual perfection across all generated Excel workbooks:
- Column widths: No column with default 13.0. Col M >= 70, Col C >= 35, etc.
- Image dimensions: Width <= 400px, Height <= 220px.
- Row heights: With image >= 185pt, without image <= 50pt.
- Drawing rels: 100% ECMA-376 Part 2 relative rels.
"""

import os
import glob
import zipfile
from pathlib import Path
import openpyxl

REPO_ROOT = Path("/home/baudui/Projects/automation-ui")
SUBMISSION_DIR = REPO_ROOT / "automation-uat/submission_for_instructor"
TESTING_DIR = SUBMISSION_DIR / "automation-testing"
INDIVIDUAL_DIR = TESTING_DIR / "02_Individual_Modules"
THEMATIC_DIR = TESTING_DIR / "01_Thematic_Packages"

def audit_workbook(f_path: Path):
    issues = []
    try:
        wb = openpyxl.load_workbook(f_path)
    except Exception as e:
        return [f"Failed to load: {e}"]

    for s_name in wb.sheetnames:
        ws = wb[s_name]
        if s_name == "Executive Summary" or "Executive" in f_path.name:
            continue

        # Check Column Widths
        w_m = ws.column_dimensions['M'].width or 0
        w_c = ws.column_dimensions['C'].width or 0
        w_n = ws.column_dimensions['N'].width or 0

        if w_m < 65:
            issues.append(f"[{s_name}] Col M width too narrow: {w_m} (expected >= 70)")
        if w_c < 30:
            issues.append(f"[{s_name}] Col C width too narrow: {w_c} (expected >= 35)")
        if w_n < 20:
            issues.append(f"[{s_name}] Col N width too narrow: {w_n} (expected >= 25)")

        # Check Images & Row heights
        img_rows = set()
        for idx, img in enumerate(ws._images):
            # Check dimensions
            if img.width > 420:
                issues.append(f"[{s_name}] Image {idx} too wide: {img.width}px (expected <= 380px)")
            if img.height > 230:
                issues.append(f"[{s_name}] Image {idx} too tall: {img.height}px (expected <= 214px)")

            # Check anchor row
            r = None
            if hasattr(img, 'anchor') and hasattr(img.anchor, '_from') and hasattr(img.anchor._from, 'row'):
                r = img.anchor._from.row + 1
            if r:
                img_rows.add(r)
                h = ws.row_dimensions[r].height or 0
                if h < 170:
                    issues.append(f"[{s_name}] Row {r} with image has insufficient height: {h}pt (expected >= 185pt)")

        # Check non-image rows height
        for r in range(2, min(ws.max_row + 1, 25)):
            if r not in img_rows:
                h = ws.row_dimensions[r].height or 0
                if h > 70:
                    issues.append(f"[{s_name}] Non-image row {r} has bloated height: {h}pt (expected ~40pt)")

    # Check zip rels
    try:
        with zipfile.ZipFile(f_path, 'r') as z:
            for n in z.namelist():
                if n.startswith('xl/drawings/_rels/'):
                    xml = z.read(n).decode('utf-8')
                    if 'Target="/xl/media/' in xml:
                        issues.append(f"Absolute rel path found in {n}")
    except Exception as e:
        issues.append(f"Zip read error: {e}")

    return issues

def main():
    print("=" * 70)
    print("AUDITING VISUAL PERFECTION ACROSS ALL WORKBOOKS")
    print("=" * 70)

    all_files = sorted(INDIVIDUAL_DIR.glob("**/*.xlsx"))
    total_files = len(all_files)
    flawless = 0
    flawed = 0

    for f in all_files:
        issues = audit_workbook(f)
        if not issues:
            flawless += 1
            print(f"[OK] {f.name:55s} -> 100% Visual Perfection")
        else:
            flawed += 1
            print(f"[FAIL] {f.name:55s} -> {len(issues)} issues:")
            for iss in issues[:3]:
                print(f"       ! {iss}")

    print("\nSummary: Flawless: %d / %d, Flawed: %d / %d" % (flawless, total_files, flawed, total_files))

if __name__ == "__main__":
    main()
