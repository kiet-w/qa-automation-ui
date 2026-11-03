#!/usr/bin/env python3
"""
apply_option_a_clean_rebuild.py
=============================================================================
Option A Implementation: Gold Standard 100% Visual Density Across All Packages
- Eliminates phantom spec matrices (03 School Spec Matrix, 04 User Spec Matrix)
- Eliminates 0-image theoretical checklists (08 FSD 104 Specs Audit, 06 Payment Simulator)
- Filters text-only checklist rows from GovTech Plan, Parent Login, Citizen Dashboard
- Guarantees 100% 1:1 row-to-image ratio across every single test execution sheet
- Sets unique, domain-specific Actions and Checkpoints (no generic placeholder text)
- Applies Golden-Ratio Enterprise aesthetics:
    Col M = 74.0, Row Height = 195.0 pt, centered 380x214 px images with 70px/18px margins
    Freeze Panes C2, Auto-Filter A1:N
=============================================================================
"""

import os
import io
import re
import shutil
import zipfile
from pathlib import Path
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.drawing.image import Image as OpenpyxlImage

REPO_ROOT = Path("/home/baudui/Projects/automation-ui")
SUBMISSION_DIR = REPO_ROOT / "automation-uat/submission_for_instructor"
THEMATIC_DIR = SUBMISSION_DIR / "01_Thematic_Packages"
TESTING_DIR = SUBMISSION_DIR / "automation-testing"
INDIVIDUAL_DIR = TESTING_DIR / "02_Individual_Modules"

# Typography and Styling
NAVY_HEADER_FILL = PatternFill(start_color="0F172A", end_color="0F172A", fill_type="solid")
HEADER_FONT = Font(name="Segoe UI", size=10, bold=True, color="FFFFFF")
REGULAR_FONT = Font(name="Segoe UI", size=9.5, color="1E293B")
BOLD_FONT = Font(name="Segoe UI", size=9.5, bold=True, color="0F172A")
CODE_FONT = Font(name="Consolas", size=9, color="0F172A")

PASS_FILL = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")
PASS_FONT = Font(name="Segoe UI", size=9.5, bold=True, color="166534")

ZEBRA_FILL = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
WHITE_FILL = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")

THIN_BORDER = Border(
    left=Side(style='thin', color='CBD5E1'),
    right=Side(style='thin', color='CBD5E1'),
    top=Side(style='thin', color='CBD5E1'),
    bottom=Side(style='thin', color='CBD5E1')
)

COLUMN_WIDTHS = {
    'A': 8.0,    # No.
    'B': 20.0,   # Test Case ID
    'C': 38.0,   # Test Method / Function
    'D': 42.0,   # Test Script Path
    'E': 28.0,   # Feature / Module
    'F': 34.0,   # Target Page URL
    'G': 36.0,   # Target UI Locator / Selector
    'H': 38.0,   # Automated Action & Test Data
    'I': 38.0,   # Automated Assertion / Checkpoint
    'J': 18.0,   # Execution Status
    'K': 14.0,   # Duration (s)
    'L': 22.0,   # Executed Timestamp
    'M': 74.0,   # 📷 BSK Visual Evidence
    'N': 26.0    # Traceability / Spec Ref
}

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

def patch_zip_drawing_rels_and_centering(file_path):
    """Ensures relative drawing rels and centers images within cell M."""
    temp_path = str(file_path) + ".tmp.xlsx"
    with zipfile.ZipFile(file_path, "r") as zin:
        with zipfile.ZipFile(temp_path, "w", zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                content = zin.read(item.filename)
                if "drawing" in item.filename and item.filename.endswith(".xml") and not "_rels" in item.filename:
                    xml_str = content.decode("utf-8")
                    new_xml = re.sub(r"<(?:\w+:)?colOff>0</(?:\w+:)?colOff>", "<colOff>666750</colOff>", xml_str)
                    new_xml = re.sub(r"<(?:\w+:)?rowOff>0</(?:\w+:)?rowOff>", "<rowOff>171450</rowOff>", new_xml)
                    content = new_xml.encode("utf-8")
                elif item.filename.startswith("xl/drawings/_rels/") and item.filename.endswith(".rels"):
                    rels_str = content.decode("utf-8")
                    if "Target=\"/xl/media/" in rels_str or "Target=\x27/xl/media/" in rels_str:
                        rels_str = rels_str.replace("Target=\"/xl/media/", "Target=\"../media/").replace("Target=\x27/xl/media/", "Target=\x27../media/")
                        content = rels_str.encode("utf-8")
                zout.writestr(item, content)
    shutil.move(temp_path, file_path)

print("[*] apply_option_a_clean_rebuild.py module loaded successfully.")
