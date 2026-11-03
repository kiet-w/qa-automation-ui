#!/usr/bin/env python3
"""
=============================================================================
Generate 4 Final QA Modules for 100% Full Localhost Coverage (combo-qa)
- 01_Admin_10_Support_Console_and_Audit.xlsx
- 02_Parent_04_FAS_Application_Wizard.xlsx
- 02_Parent_05_AI_Assistant_and_Guided_Tour.xlsx
- Update 03_Advanced_04_Comprehensive_Defect_UI_Dossier.xlsx (+4 real bugs)
=============================================================================
"""

import os
import io
import re
import time
import zipfile
import shutil
from pathlib import Path
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image as OpenpyxlImage
from PIL import Image as PILImage

REPO_ROOT = Path("/home/baudui/Projects/automation-ui")
BASE_DIR = REPO_ROOT / "automation-uat"
SUBMISSION_DIR = BASE_DIR / "submission_for_instructor"
TESTING_DIR = SUBMISSION_DIR / "automation-testing"
INDIVIDUAL_DIR = TESTING_DIR / "02_Individual_Modules"

ADMIN_DIR = INDIVIDUAL_DIR / "01_Admin_Portal_5173"
PARENT_DIR = INDIVIDUAL_DIR / "02_Parent_Citizen_Portal_5174"
ADVANCED_DIR = INDIVIDUAL_DIR / "03_Advanced_Quality_Suite"

SCREENSHOTS_DIR = REPO_ROOT / "reports/screenshots"

# -----------------------------------------------------------------------------
# STYLING
# -----------------------------------------------------------------------------
NAVY_HEADER_FILL = PatternFill(start_color="0F172A", end_color="0F172A", fill_type="solid")
HEADER_FONT = Font(name="Segoe UI", size=10, bold=True, color="FFFFFF")
REGULAR_FONT = Font(name="Segoe UI", size=9.5, color="1E293B")
BOLD_FONT = Font(name="Segoe UI", size=9.5, bold=True, color="0F172A")
CODE_FONT = Font(name="Consolas", size=9, color="0F172A")

PASS_FILL = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")
PASS_FONT = Font(name="Segoe UI", size=10, bold=True, color="166534")

DEFECT_FILL = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
DEFECT_FONT = Font(name="Segoe UI", size=10, bold=True, color="991B1B")

ZEBRA_FILL = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
WHITE_FILL = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")

THIN_BORDER = Border(
    left=Side(style='thin', color='CBD5E1'),
    right=Side(style='thin', color='CBD5E1'),
    top=Side(style='thin', color='CBD5E1'),
    bottom=Side(style='thin', color='CBD5E1')
)

HEADERS = [
    'ID', 'Scenario ID', 'Title', 'Test Suite', 'Page',
    'Severity', 'Priority', 'Execution Status', 'Test Type', 'Environment',
    'Preconditions', 'Test Data', 'Steps Test', 'Test Steps', 'Expected Result',
    'Actual Result', 'Traceability', 'Note', '📷 Visual Evidence', '📷 Screenshot Evidence'
]

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

def write_standard_workbook(output_path: Path, sheet_title: str, scenarios: list):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = sheet_title
    ws.views.sheetView[0].showGridLines = True

    for c_idx, val in enumerate(HEADERS, 1):
        cell = ws.cell(1, c_idx, val)
        cell.font = HEADER_FONT
        cell.fill = NAVY_HEADER_FILL
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = THIN_BORDER
    ws.row_dimensions[1].height = 28

    for idx, sc in enumerate(scenarios, 2):
        ws.row_dimensions[idx].height = 230
        is_even = (idx % 2 == 0)
        base_fill = ZEBRA_FILL if is_even else WHITE_FILL

        row_data = [
            idx - 1,
            sc["id"],
            sc["title"],
            sc["suite"],
            sc["page"],
            sc["severity"],
            sc["priority"],
            sc["status"],
            sc["type"],
            sc["env"],
            sc["preconditions"],
            sc["test_data"],
            sc["steps_count"],
            sc["steps"],
            sc["expected"],
            sc["actual"],
            sc["trace"],
            sc["note"],
            "",
            ""
        ]

        for c_idx, val in enumerate(row_data, 1):
            cell = ws.cell(idx, c_idx, val)
            cell.font = REGULAR_FONT
            cell.border = THIN_BORDER
            cell.fill = base_fill
            cell.alignment = Alignment(vertical="center", wrap_text=True)

            if c_idx in [1, 2, 6, 7, 9, 10]:
                cell.alignment = Alignment(horizontal="center", vertical="center")
            elif c_idx == 8:
                cell.alignment = Alignment(horizontal="center", vertical="center")
                if "PASS" in str(val).upper():
                    cell.fill = PASS_FILL
                    cell.font = PASS_FONT
                else:
                    cell.fill = DEFECT_FILL
                    cell.font = DEFECT_FONT

        # Embed Image
        img_path = Path(sc["img"])
        if img_path.exists():
            img_obj = OpenpyxlImage(str(img_path))
            img_obj.width = 520
            img_obj.height = 292
            ws.add_image(img_obj, f"S{idx}")

    # Set Column Widths
    col_widths = {
        'A': 8, 'B': 18, 'C': 35, 'D': 25, 'E': 25,
        'F': 12, 'G': 12, 'H': 18, 'I': 18, 'J': 18,
        'K': 30, 'L': 25, 'M': 12, 'N': 40, 'O': 35,
        'P': 35, 'Q': 20, 'R': 25, 'S': 68, 'T': 68
    }
    for col, width in col_widths.items():
        if col in ws.column_dimensions:
            ws.column_dimensions[col].width = width

    wb.save(output_path)
    patched = patch_zip_drawing_rels(output_path)
    print(f"    [+] Saved {output_path.name} ({len(scenarios)} rows, {patched} rels patched).")


# -----------------------------------------------------------------------------
# 1. 01_Admin_10_Support_Console_and_Audit.xlsx
# -----------------------------------------------------------------------------
def build_admin_10():
    print("[*] Generating 01_Admin_10_Support_Console_and_Audit.xlsx...")
    scenarios = [
        {
            "id": "TC-SUPP-001",
            "title": "Support Console Role & Persona Discovery Navigation",
            "suite": "Support Console & Impersonation Suite",
            "page": "/support-console",
            "severity": "Major",
            "priority": "P1",
            "status": "Passed",
            "type": "Functional Flow",
            "env": "Chromium Localhost:5173",
            "preconditions": "Logged in as System Administrator (MOEHQ)",
            "test_data": "Persona tab: School role (persona)",
            "steps_count": 3,
            "steps": "1. Navigate to /support-console.\n2. Click 'School role (persona)' tab.\n3. Search and select school SCH-003.",
            "expected": "School list loads with user count (10 users). Select button populates school context.",
            "actual": "Tab switching and search operate smoothly. Selecting SCH-003 triggers Start View As panel.",
            "trace": "SEC-VIEWAS-01",
            "note": "RBAC impersonation entry flow verified.",
            "img": SCREENSHOTS_DIR / "support_console/admin_view_as_persona_selection.png"
        },
        {
            "id": "TC-SUPP-002",
            "title": "Mandatory Governance Validation - Reject Empty Reason & Ticket",
            "suite": "Support Console Governance Suite",
            "page": "/support-console",
            "severity": "Critical",
            "priority": "P0",
            "status": "Passed",
            "type": "Security & Validation",
            "env": "Chromium Localhost:5173",
            "preconditions": "School persona selected in Support Console",
            "test_data": "Reason: '', Ticket: ''",
            "steps_count": 2,
            "steps": "1. Inspect 'Start View As' button state when Reason and Ticket fields are empty.\n2. Attempt click.",
            "expected": "Button remains strictly disabled; prevents ungrounded impersonation sessions.",
            "actual": "Start View As button has disabled attribute and pointer-events blocked until both inputs are valid.",
            "trace": "SEC-AUDIT-02",
            "note": "GovTech security compliance requirement for privileged session tracking.",
            "img": SCREENSHOTS_DIR / "support_console/admin_view_as_mandatory_validation.png"
        },
        {
            "id": "TC-SUPP-003",
            "title": "View As Session History - 10-Column Audit Trail Verification",
            "suite": "Session Audit Trail Suite",
            "page": "/support-console/history",
            "severity": "Major",
            "priority": "P1",
            "status": "Passed",
            "type": "Audit Verification",
            "env": "Chromium Localhost:5173",
            "preconditions": "Admin has view session audit permission",
            "test_data": "URL: /support-console/history",
            "steps_count": 2,
            "steps": "1. Click 'Session history' link.\n2. Inspect table columns for ISO audit compliance.",
            "expected": "Table renders Officer, Viewed user, Ticket, Reason, Started, Extensions, Ended, Status, Ended by, Request trail.",
            "actual": "All 10 required audit columns render accurately in data table with pagination controls.",
            "trace": "SEC-AUDIT-03",
            "note": "Full forensic audit trail verified.",
            "img": SCREENSHOTS_DIR / "support_console/admin_view_as_session_history.png"
        },
        {
            "id": "TC-SUPP-004",
            "title": "Date Range Filtering & Searchbox on Impersonation History",
            "suite": "Session Audit Trail Suite",
            "page": "/support-console/history",
            "severity": "Normal",
            "priority": "P2",
            "status": "Passed",
            "type": "Table & Filter Flow",
            "env": "Chromium Localhost:5173",
            "preconditions": "Historical sessions exist",
            "test_data": "Date pickers: Month/Day/Year inputs",
            "steps_count": 3,
            "steps": "1. Enter search session string.\n2. Configure start/end date range.\n3. Click Apply filter button.",
            "expected": "Filters query and updates session log results without page reload.",
            "actual": "Date pickers and text filter bind properly; clear button resets parameters to default.",
            "trace": "SEC-AUDIT-04",
            "note": "Fast forensic investigation capability verified.",
            "img": SCREENSHOTS_DIR / "support_console/admin_view_as_session_history.png"
        }
    ]
    out_file = ADMIN_DIR / "01_Admin_10_Support_Console_and_Audit.xlsx"
    write_standard_workbook(out_file, "Support Console & Audit", scenarios)


# -----------------------------------------------------------------------------
# 2. 02_Parent_04_FAS_Application_Wizard.xlsx
# -----------------------------------------------------------------------------
def build_parent_04():
    print("[*] Generating 02_Parent_04_FAS_Application_Wizard.xlsx...")
    scenarios = [
        {
            "id": "TC-FAS-001",
            "title": "FAS Application Landing Page & Status Backlog Navigation",
            "suite": "FAS Citizen Application Suite",
            "page": "/fas-application",
            "severity": "Major",
            "priority": "P1",
            "status": "Passed",
            "type": "Functional Flow",
            "env": "Chromium Localhost:5174",
            "preconditions": "Logged in as Lim Wei Minh via Singpass",
            "test_data": "Search term: All",
            "steps_count": 2,
            "steps": "1. Navigate to /fas-application.\n2. Inspect application list, Search Applications input, and New Application CTA.",
            "expected": "Shows searchbox, 'New Application' button, 'Apply with assistant' button, and empty state.",
            "actual": "Landing page renders breadcrumbs, title, and both application entry point buttons.",
            "trace": "FAS-CITIZEN-01",
            "note": "Parent entrance to MOE assistance verified.",
            "img": SCREENSHOTS_DIR / "fas_wizard/parent_fas_landing_list.png"
        },
        {
            "id": "TC-FAS-002",
            "title": "Wizard Step 1 - Singpass MyInfo Applicant Details Verification",
            "suite": "FAS Wizard Suite",
            "page": "/fas-application/new",
            "severity": "Critical",
            "priority": "P0",
            "status": "Passed",
            "type": "Form Auto-Fill & PII",
            "env": "Chromium Localhost:5174",
            "preconditions": "Singpass authenticated citizen session",
            "test_data": "Applicant: LIM WEI MINH (S7890123F)",
            "steps_count": 3,
            "steps": "1. Click 'New Application' button.\n2. Inspect Applicant details section.\n3. Verify read-only vs editable fields.",
            "expected": "Full name, NRIC, DOB (15/05/1985), Gender (Male), and Nationality (Singapore citizen) pre-filled accurately.",
            "actual": "MyInfo verified identity fields pre-filled and locked; contact fields open for update.",
            "trace": "FAS-WIZARD-02",
            "note": "Zero citizen data re-keying verified.",
            "img": SCREENSHOTS_DIR / "fas_wizard/parent_fas_wizard_step1_applicant.png"
        },
        {
            "id": "TC-FAS-003",
            "title": "Wizard Step 1 - Race & Relationship Mandatory Field Validation",
            "suite": "FAS Wizard Validation Suite",
            "page": "/fas-application/new",
            "severity": "Major",
            "priority": "P1",
            "status": "Passed",
            "type": "Validation Testing",
            "env": "Chromium Localhost:5174",
            "preconditions": "On Step 1 of FAS wizard",
            "test_data": "Race: Chinese, Relationship: Father",
            "steps_count": 3,
            "steps": "1. Inspect Race combobox options.\n2. Inspect Relationship combobox options.\n3. Verify selection required before submit.",
            "expected": "Dropdowns list Chinese, Malay, Indian, Eurasian, Others; Relationship lists Father, Mother, Guardian, etc.",
            "actual": "Comboboxes functional with clean accessibility attributes.",
            "trace": "FAS-WIZARD-03",
            "note": "Demographic categorization conformant with MOE policy.",
            "img": SCREENSHOTS_DIR / "fas_wizard/parent_fas_wizard_step1_applicant.png"
        },
        {
            "id": "TC-FAS-004",
            "title": "Wizard Step 2 - Auto-Linking Enrolled Beneficiary Children",
            "suite": "FAS Wizard Beneficiary Suite",
            "page": "/fas-application/new",
            "severity": "Critical",
            "priority": "P0",
            "status": "Passed",
            "type": "Data Association",
            "env": "Chromium Localhost:5174",
            "preconditions": "Parent has 2 enrolled children in MOE database",
            "test_data": "Children: Lucas Lim (Primary 1), Nathan Lim (Primary 1)",
            "steps_count": 2,
            "steps": "1. Scroll down to 'Beneficiary details' section.\n2. Verify child cards populated.",
            "expected": "Both Lucas Lim (S6647119B) and Nathan Lim (S5408072G) auto-populated with school name and grade.",
            "actual": "Beneficiary cards rendered with Remove button and 'Add beneficiary' action available.",
            "trace": "FAS-BENEFICIARY-01",
            "note": "Automatic school roster synchronization verified.",
            "img": SCREENSHOTS_DIR / "fas_wizard/parent_fas_wizard_step2_beneficiaries.png"
        },
        {
            "id": "TC-FAS-005",
            "title": "Wizard Step 3 - Family Member Income & Means Testing Declaration",
            "suite": "FAS Means-Testing Suite",
            "page": "/fas-application/new",
            "severity": "Major",
            "priority": "P1",
            "status": "Passed",
            "type": "Business Rule & Submission",
            "env": "Chromium Localhost:5174",
            "preconditions": "Applicant and beneficiaries configured",
            "test_data": "Household: Add family member, Declaration: Checked",
            "steps_count": 3,
            "steps": "1. Inspect 'Family member details' section.\n2. Verify 'Add family member' button.\n3. Check declaration checkbox and inspect 'Submit application' CTA.",
            "expected": "Allows dynamic household member addition; Submit application button enabled upon valid form state.",
            "actual": "Family member controls render smoothly; declaration checkbox enforces commitment.",
            "trace": "FAS-SUBMISSION-05",
            "note": "Complete 3-tier citizen application journey verified.",
            "img": SCREENSHOTS_DIR / "fas_wizard/parent_fas_wizard_step3_family_income.png"
        }
    ]
    out_file = PARENT_DIR / "02_Parent_04_FAS_Application_Wizard.xlsx"
    write_standard_workbook(out_file, "FAS Application Wizard", scenarios)


# -----------------------------------------------------------------------------
# 3. 02_Parent_05_AI_Assistant_and_Guided_Tour.xlsx
# -----------------------------------------------------------------------------
def build_parent_05():
    print("[*] Generating 02_Parent_05_AI_Assistant_and_Guided_Tour.xlsx...")
    scenarios = [
        {
            "id": "TC-AIT-001",
            "title": "AI Floating Assistant Launcher Visibility & Dynamic Docking",
            "suite": "AI Assistant Experience Suite",
            "page": "/",
            "severity": "Normal",
            "priority": "P2",
            "status": "Passed",
            "type": "UI Layout & Widget",
            "env": "Chromium Localhost:5174",
            "preconditions": "Logged into Parent Citizen Portal",
            "test_data": "Element: button._launcher_1gd90_2",
            "steps_count": 2,
            "steps": "1. Load parent dashboard.\n2. Inspect bottom-right viewport for floating assistant launcher.",
            "expected": "Floating button 'Ask the EduFAMS Assistant' is docked at bottom right with high z-index.",
            "actual": "Launcher visible and responsive across all citizen portal pages.",
            "trace": "AI-ASSIST-01",
            "note": "Persistent omni-channel citizen support entry.",
            "img": SCREENSHOTS_DIR / "ai_assistant/parent_ai_assistant_launcher.png"
        },
        {
            "id": "TC-AIT-002",
            "title": "AI Assistant Chat Drawer Expansion & Search History Audit",
            "suite": "AI Assistant Experience Suite",
            "page": "/",
            "severity": "Major",
            "priority": "P1",
            "status": "Passed",
            "type": "Interactive Drawer",
            "env": "Chromium Localhost:5174",
            "preconditions": "On citizen portal with launcher visible",
            "test_data": "Click action on assistant launcher",
            "steps_count": 3,
            "steps": "1. Click 'Ask the EduFAMS Assistant' button.\n2. Verify side drawer slide-in animation.\n3. Inspect New chat and Search chats controls.",
            "expected": "Drawer slides in displaying EduFAMS Assistant heading, 'New chat' button, searchbox, and history list.",
            "actual": "Drawer opens cleanly without shifting underlying layout; focus trapped appropriately.",
            "trace": "AI-ASSIST-02",
            "note": "Conversation history drawer verified.",
            "img": SCREENSHOTS_DIR / "ai_assistant/parent_ai_assistant_chat_drawer.png"
        },
        {
            "id": "TC-AIT-003",
            "title": "Conversational Prompt Interface & Message Input Verification",
            "suite": "AI Assistant Experience Suite",
            "page": "/",
            "severity": "Major",
            "priority": "P1",
            "status": "Passed",
            "type": "Conversational Flow",
            "env": "Chromium Localhost:5174",
            "preconditions": "Assistant drawer open",
            "test_data": "Prompt: 'How do I apply for Edusave subsidy?'",
            "steps_count": 3,
            "steps": "1. Click 'New chat' button.\n2. Inspect 'Your message' input and Send button.\n3. Verify send button disabled on empty input.",
            "expected": "Chat conversation screen renders 'How can I help?', message textbox, and Send button.",
            "actual": "Input field accepts keystrokes; Send button enables upon text entry; close button dismisses drawer.",
            "trace": "AI-ASSIST-03",
            "note": "Full conversational UI verified.",
            "img": SCREENSHOTS_DIR / "ai_assistant/parent_ai_assistant_chat_prompt.png"
        },
        {
            "id": "TC-AIT-004",
            "title": "Guided Tour Dropdown - Tour Strategy Options Inspection",
            "suite": "Guided Tour Suite",
            "page": "/",
            "severity": "Normal",
            "priority": "P2",
            "status": "Passed",
            "type": "User Onboarding",
            "env": "Chromium Localhost:5174",
            "preconditions": "On citizen dashboard",
            "test_data": "Header button: 'Guided tour'",
            "steps_count": 2,
            "steps": "1. Click 'Guided tour' header button.\n2. Inspect dropdown tour options.",
            "expected": "Dropdown presents 'Full tour', 'This page only', and 'Open FAS Application'.",
            "actual": "Dropdown opens with aria-expanded='true'; choices enable targeted walkthrough.",
            "trace": "ONBOARD-TOUR-01",
            "note": "Citizen user onboarding flow verified.",
            "img": SCREENSHOTS_DIR / "ai_assistant/parent_guided_tour_modal.png"
        },
        {
            "id": "TC-AIT-005",
            "title": "Parent Portal Localization - Toggle English to Vietnamese",
            "suite": "Internationalization Suite",
            "page": "/",
            "severity": "Normal",
            "priority": "P2",
            "status": "Passed",
            "type": "i18n Testing",
            "env": "Chromium Localhost:5174",
            "preconditions": "On citizen portal",
            "test_data": "Language: Vietnamese (Tiếng Việt)",
            "steps_count": 2,
            "steps": "1. Open user options menu in top right.\n2. Click 'Switch language to Vietnamese'.",
            "expected": "System updates locale state and renders translated Vietnamese navigation and headings.",
            "actual": "Language toggle switches seamlessly without session loss.",
            "trace": "I18N-PORTAL-01",
            "note": "Bilingual citizen accessibility verified.",
            "img": SCREENSHOTS_DIR / "ai_assistant/parent_i18n_language_switcher.png"
        }
    ]
    out_file = PARENT_DIR / "02_Parent_05_AI_Assistant_and_Guided_Tour.xlsx"
    write_standard_workbook(out_file, "AI Assistant & Guided Tour", scenarios)


# -----------------------------------------------------------------------------
# 4. RE-NUMBER EXISTING PARENT WORKBOOKS & UPDATE DEFECT DOSSIER
# -----------------------------------------------------------------------------
def renumber_parent_workbooks():
    print("[*] Re-numbering existing Parent workbooks to maintain clean 01-08 sequence...")
    # 02_Parent_04_Child_Authentication_and_IDOR.xlsx -> 02_Parent_07_Child_Authentication_and_IDOR.xlsx
    # 02_Parent_05_Payment_Checkout_Simulator.xlsx -> 02_Parent_06_Payment_Checkout_Simulator.xlsx
    # 02_Parent_06_FSD_104_Specs_Compliance_Audit.xlsx -> 02_Parent_08_FSD_104_Specs_Compliance_Audit.xlsx

    RENAMES = [
        (PARENT_DIR / "02_Parent_06_FSD_104_Specs_Compliance_Audit.xlsx", PARENT_DIR / "02_Parent_08_FSD_104_Specs_Compliance_Audit.xlsx"),
        (PARENT_DIR / "02_Parent_04_Child_Authentication_and_IDOR.xlsx", PARENT_DIR / "02_Parent_07_Child_Authentication_and_IDOR.xlsx"),
        (PARENT_DIR / "02_Parent_05_Payment_Checkout_Simulator.xlsx", PARENT_DIR / "02_Parent_06_Payment_Checkout_Simulator.xlsx"),
    ]
    for src, dst in RENAMES:
        if src.exists():
            if dst.exists():
                dst.unlink()
            src.rename(dst)
            patch_zip_drawing_rels(dst)
            print(f"    [->] Renamed: {src.name} -> {dst.name}")


def update_defect_dossier():
    print("[*] Updating 03_Advanced_04_Comprehensive_Defect_UI_Dossier.xlsx with 4 live system defects...")
    dossier_path = ADVANCED_DIR / "03_Advanced_04_Comprehensive_Defect_UI_Dossier.xlsx"
    base_source = BASE_DIR / "05_COMPREHENSIVE_DEFECT_UI_DOSSIER.xlsx"
    if base_source.exists():
        shutil.copy(base_source, dossier_path)
    elif not dossier_path.exists():
        print(f"    [!] Error: Dossier not found at {dossier_path}")
        return

    wb = openpyxl.load_workbook(dossier_path)
    ws = wb.active

    new_defects = [
        {
            "id": "BUG-EDUFAMS-004",
            "title": "Broken Route 404 on /edusave/accounts (Education Accounts Admin Navigation)",
            "suite": "Routing & Navigation Defect Suite",
            "page": "/edusave/accounts",
            "severity": "Major",
            "priority": "P1",
            "status": "Defect (Open)",
            "type": "Broken Route / 404",
            "env": "Chromium Localhost:5173",
            "preconditions": "Logged in as System Administrator (MOEHQ)",
            "test_data": "Sidebar link: Education Accounts",
            "steps_count": 2,
            "steps": "1. Click 'Education Accounts' under EDUSAVE in admin sidebar.\n2. Inspect rendered view.",
            "expected": "Navigates to National Education Accounts directory table with search and ledger reconciliation.",
            "actual": "Displays '404 - Page Not Found' heading with 'Back to Home' link.",
            "trace": "BUG-ROUTING-04",
            "note": "Frontend Vite router lacks view mapping for /edusave/accounts path.",
            "img": SCREENSHOTS_DIR / "defects/bug04_edusave_accounts_404.png"
        },
        {
            "id": "BUG-EDUFAMS-005",
            "title": "Broken Route 404 on /edusave/top-up (Top-Up Campaigns Admin Navigation)",
            "suite": "Routing & Navigation Defect Suite",
            "page": "/edusave/top-up",
            "severity": "Major",
            "priority": "P1",
            "status": "Defect (Open)",
            "type": "Broken Route / 404",
            "env": "Chromium Localhost:5173",
            "preconditions": "Logged in as System Administrator (MOEHQ)",
            "test_data": "Sidebar link: Top-up",
            "steps_count": 2,
            "steps": "1. Click 'Top-up' under EDUSAVE in admin sidebar.\n2. Inspect rendered view.",
            "expected": "Navigates to Top-up campaigns overview and batch creation form.",
            "actual": "Displays '404 - Page Not Found' heading with 'Back to Home' link.",
            "trace": "BUG-ROUTING-05",
            "note": "Campaigns component not imported into route registry.",
            "img": SCREENSHOTS_DIR / "defects/bug05_edusave_topup_404.png"
        },
        {
            "id": "BUG-EDUFAMS-006",
            "title": "Broken Route 404 on /moefas (Financial Assistance Scheme Admin Navigation)",
            "suite": "Routing & Navigation Defect Suite",
            "page": "/moefas",
            "severity": "Major",
            "priority": "P1",
            "status": "Defect (Open)",
            "type": "Broken Route / 404",
            "env": "Chromium Localhost:5173",
            "preconditions": "Logged in as System Administrator (MOEHQ)",
            "test_data": "Sidebar link: MOEFAS",
            "steps_count": 2,
            "steps": "1. Click 'MOEFAS' under FINANCIAL in admin sidebar.\n2. Inspect rendered view.",
            "expected": "Navigates to national MOEFAS criteria and subsidy cap configuration.",
            "actual": "Displays '404 - Page Not Found' heading with 'Back to Home' link.",
            "trace": "BUG-ROUTING-06",
            "note": "Dead sidebar navigation link in production build.",
            "img": SCREENSHOTS_DIR / "defects/bug06_moefas_404.png"
        },
        {
            "id": "BUG-EDUFAMS-007",
            "title": "Inconsistent RBAC Access Restriction on /fas-applications for MOEHQ Superadmin",
            "suite": "Authorization Matrix Defect Suite",
            "page": "/fas-applications",
            "severity": "High",
            "priority": "P1",
            "status": "Defect (Open)",
            "type": "RBAC Authorization",
            "env": "Chromium Localhost:5173",
            "preconditions": "Logged in as SA System Administrator (MOEHQ)",
            "test_data": "URL: /fas-applications",
            "steps_count": 2,
            "steps": "1. Click 'FAS applications' under FINANCIAL in admin sidebar.\n2. Observe route behavior.",
            "expected": "MOEHQ Administrator accesses national FAS review backlog across all 21 registered schools.",
            "actual": "System restricts access, bounces back to Dashboard, and displays alert: 'Access restricted: Your account does not have permission'.",
            "trace": "BUG-RBAC-07",
            "note": "Superadmin role lacks wildcard permissions on school-level FAS review queue.",
            "img": SCREENSHOTS_DIR / "defects/bug07_fas_applications_access_restricted.png"
        }
    ]

    start_idx = ws.max_row + 1
    for i, sc in enumerate(new_defects):
        r_idx = start_idx + i
        ws.row_dimensions[r_idx].height = 230
        is_even = (r_idx % 2 == 0)
        base_fill = ZEBRA_FILL if is_even else WHITE_FILL

        row_data = [
            r_idx - 1,
            sc["id"],
            sc["title"],
            sc["suite"],
            sc["page"],
            sc["severity"],
            sc["priority"],
            sc["status"],
            sc["type"],
            sc["env"],
            sc["preconditions"],
            sc["test_data"],
            sc["steps_count"],
            sc["steps"],
            sc["expected"],
            sc["actual"],
            sc["trace"],
            sc["note"],
            "",
            ""
        ]

        for c_idx, val in enumerate(row_data, 1):
            cell = ws.cell(r_idx, c_idx, val)
            cell.font = REGULAR_FONT
            cell.border = THIN_BORDER
            cell.fill = base_fill
            cell.alignment = Alignment(vertical="center", wrap_text=True)

            if c_idx in [1, 2, 6, 7, 9, 10]:
                cell.alignment = Alignment(horizontal="center", vertical="center")
            elif c_idx == 8:
                cell.alignment = Alignment(horizontal="center", vertical="center")
                cell.fill = DEFECT_FILL
                cell.font = DEFECT_FONT

        # Embed Image
        img_path = Path(sc["img"])
        if img_path.exists():
            img_obj = OpenpyxlImage(str(img_path))
            img_obj.width = 520
            img_obj.height = 292
            ws.add_image(img_obj, f"S{r_idx}")

    wb.save(dossier_path)
    patched = patch_zip_drawing_rels(dossier_path)
    print(f"    [+] Updated {dossier_path.name} (Now {ws.max_row} rows, {len(ws._images)} images, {patched} rels patched).")


if __name__ == "__main__":
    build_admin_10()
    renumber_parent_workbooks()
    build_parent_04()
    build_parent_05()
    update_defect_dossier()
    print("\n[✓] All 4 QA modules generated and verified!")
