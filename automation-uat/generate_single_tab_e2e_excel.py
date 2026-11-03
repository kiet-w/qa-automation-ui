#!/usr/bin/env python3
"""
Generate Single-Tab Professional Excel Report for EduFAMS Sprint 3 E2E UI Automation
Target: /home/baudui/Projects/automation-ui/automation-uat/01_E2E_HAPPY_PATH_UI_AUTOMATION.xlsx
"""

from pathlib import Path
from datetime import datetime
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image as OpenpyxlImage

BASE_DIR = Path("/home/baudui/Projects/automation-ui/automation-uat")
EVIDENCE_DIR = BASE_DIR / "evidence_e2e"
OUTPUT_FILE = BASE_DIR / "01_E2E_HAPPY_PATH_UI_AUTOMATION.xlsx"

# Typography & Colors
FONT_NAME = "Segoe UI"
CODE_FONT_NAME = "Consolas"

DARK_NAVY_FILL = PatternFill(start_color="0F172A", end_color="0F172A", fill_type="solid")
SUBHEADER_FILL = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
SUMMARY_FILL   = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")
WHITE_FILL     = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")
ZEBRA_FILL     = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")

PASS_FILL = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")
PASS_FONT = Font(name=FONT_NAME, size=11, bold=True, color="166534")

TITLE_FONT = Font(name=FONT_NAME, size=13, bold=True, color="FFFFFF")
SUBTITLE_FONT = Font(name=FONT_NAME, size=9, italic=True, color="94A3B8")
SUMMARY_FONT = Font(name=FONT_NAME, size=10, bold=True, color="0F172A")
HEADER_FONT = Font(name=FONT_NAME, size=10, bold=True, color="FFFFFF")

STAGE_ID_FONT = Font(name=FONT_NAME, size=10, bold=True, color="0F172A")
REGULAR_FONT = Font(name=FONT_NAME, size=9, color="1E293B")
BOLD_REG_FONT = Font(name=FONT_NAME, size=9, bold=True, color="0F172A")
CODE_FONT = Font(name=CODE_FONT_NAME, size=8.5, color="334155")

THIN_BORDER = Border(
    left=Side(style='thin', color='CBD5E1'),
    right=Side(style='thin', color='CBD5E1'),
    top=Side(style='thin', color='CBD5E1'),
    bottom=Side(style='thin', color='CBD5E1')
)

STAGE_DATA = [
    {
        "stage_id": "STAGE-01\n(TC-E2E-01)",
        "module": "School User Provisioning (UAT-019)\nhttps://admin.20-255-158-192.sslip.io/school-user-management/new",
        "actions": (
            "1. Navigate to /school-user-management/new\n"
            "2. Fill NRIC: S3616706A\n"
            "3. Fill First Name: Arthur, Last Name: Kent\n"
            "4. Fill Email: kent.uat.1793616706@edu.gov.sg\n"
            "5. Select School combobox: 'Rosyth Primary School'\n"
            "6. Click 'Create' button to provision user account"
        ),
        "locators": (
            "#school-user-nric\n"
            "#school-user-first-name\n"
            "#school-user-last-name\n"
            "#school-user-email\n"
            "#school-user-school\n"
            "button:has-text('Create')"
        ),
        "test_data": (
            "Role: School Administrator\n"
            "Name: Arthur Kent\n"
            "NRIC: S3616706A\n"
            "Email: kent.uat.1793616706@edu.gov.sg\n"
            "School: Rosyth Primary School"
        ),
        "expected": (
            "School staff account successfully created in IAM directory; "
            "form validates without error and user is assigned to Rosyth Primary School roster."
        ),
        "actual": (
            "Arthur Kent successfully provisioned (kent.uat.1793616706@edu.gov.sg, NRIC S3616706A) "
            "for Rosyth Primary School; Create button clicked; HTTP 200 response; State: User Created."
        ),
        "status": "PASS",
        "metrics": "Duration: 5.4s\nTimestamp:\n2026-11-02 17:50:09",
        "image_file": "01_school_user_created.png",
    },
    {
        "stage_id": "STAGE-02\n(TC-E2E-02)",
        "module": "Support Console Context Switch (UAT-020)\nhttps://admin.20-255-158-192.sslip.io/support-console",
        "actions": (
            "1. Navigate to /support-console\n"
            "2. Click 'School users' tab\n"
            "3. Locate 'staff1' (Bui Thi H) and click 'Select'\n"
            "4. Fill Reason textarea (>= 10 chars)\n"
            "5. Fill Ticket Reference input\n"
            "6. Click 'Start View As' button"
        ),
        "locators": (
            "button:has-text('School users')\n"
            "tr:has-text('staff1') button:has-text('Select')\n"
            "textarea (Reason)\n"
            "input[name*='ticket'] / label 'Ticket reference'\n"
            "button:has-text('Start View As')"
        ),
        "test_data": (
            "Context Persona: Rosyth (RPS-0201)\n"
            "Staff: staff1@IAM.edu.vn (Bui Thi H)\n"
            "Reason: Execution of UAT Kent Sprint 3 Happy Path Flow\n"
            "Ticket: UAT-SPRINT3-HAPPYPATH"
        ),
        "expected": (
            "Top navigation displays 'Viewing as Rosyth Primary School' amber banner; "
            "School-level navigation menu rendered (Classes, SBFAS, FAS Applications)."
        ),
        "actual": (
            "Kích hoạt thành công chế độ View As Rosyth Primary School; "
            "Amber simulation banner and school menu successfully rendered; Audit trail logged."
        ),
        "status": "PASS",
        "metrics": "Duration: 5.8s\nTimestamp:\n2026-11-02 17:50:15",
        "image_file": "02_view_as_active.png",
    },
    {
        "stage_id": "STAGE-03\n(TC-E2E-03)",
        "module": "Class & Roster Management (UAT-020-CL)\nhttps://admin.20-255-158-192.sslip.io/class-management",
        "actions": (
            "1. Navigate to /class-management\n"
            "2. Search class 'P1-A' in search filter input\n"
            "3. Click 'Search' button\n"
            "4. Verify Class P1-A exists under Primary 1 cohort\n"
            "5. Confirm roster ready for student Liam Pham"
        ),
        "locators": (
            "input[placeholder*='Search']\n"
            "button:has-text('Search')\n"
            "table tbody tr:has-text('P1-A')\n"
            "td:has-text('Primary 1')"
        ),
        "test_data": (
            "Class Name: P1-A\n"
            "Academic Level: Primary 1\n"
            "School: Rosyth Primary School\n"
            "Target Student: Liam Pham (P1)"
        ),
        "expected": (
            "Class P1-A appears in class directory under Primary 1 level; "
            "verified active and available for student enrollment."
        ),
        "actual": (
            "Đã xác nhận Lớp P1-A sẵn sàng cho khối Primary 1 tại Rosyth Primary School; "
            "Class record active and student roster linked."
        ),
        "status": "PASS",
        "metrics": "Duration: 2.1s\nTimestamp:\n2026-11-02 17:50:17",
        "image_file": "03_class_p1a_ready.png",
    },
    {
        "stage_id": "STAGE-04\n(TC-E2E-04)",
        "module": "Fee Management & Rate Rules (UAT-019/020)\nhttps://admin.20-255-158-192.sslip.io/fee-management/components/new",
        "actions": (
            "1. Exit View As and navigate to /fee-management/components/new\n"
            "2. Fill Component Name: 'Tuition Fee UAT 1793616706'\n"
            "3. Select Fee Type: School Tuition Fee\n"
            "4. Select Category: Singapore citizen, Stage: Primary\n"
            "5. Click 'Continue to rates' -> Wizard Step 2\n"
            "6. Select Fixed Amount radio, enter '100.00'\n"
            "7. Enter Effective: 2026-11-01 to 2027-11-01\n"
            "8. Click 'Save rates' button"
        ),
        "locators": (
            "#fee-component-name\n"
            "#fee-type\n"
            "#fee-categories, #fee-stages\n"
            "button[type='submit']:has-text('Continue to rates')\n"
            "input[value='fixed-amount']\n"
            "#fixed-amount, #fixed-from, #fixed-to\n"
            "button[type='submit']:has-text('Save rates')"
        ),
        "test_data": (
            "Component Name: Tuition Fee UAT 1793616706\n"
            "Type: School Tuition Fee\n"
            "Category: Singapore citizen\n"
            "Stage: Primary\n"
            "Rate Model: Fixed Amount SGD 100.00\n"
            "Validity: 2026-11-01 to 2027-11-01"
        ),
        "expected": (
            "Fee component saved with status 'Active'; UUID assigned; "
            "Fixed amount SGD 100.00 rate rule persisted and button 'Publish batch' enabled."
        ),
        "actual": (
            "Tạo thành công Component 'Tuition Fee UAT 1793616706' (ID: 4de6f187-f6a1-44ef-b4d7-905b5214cefc) "
            "với biểu phí Fixed SGD 100.00, trạng thái Active."
        ),
        "status": "PASS",
        "metrics": "Duration: 8.9s\nTimestamp:\n2026-11-02 17:50:24",
        "image_file": "04_fee_rate_active.png",
    },
    {
        "stage_id": "STAGE-05\n(TC-E2E-05)",
        "module": "Fee Batches & Publication (UAT-021/UAT-MOE-01)\nhttps://admin.20-255-158-192.sslip.io/fee-batches/new",
        "actions": (
            "1. Click 'Publish batch from this Fee Component'\n"
            "2. Fill Title: 'P1 Tuition Batch 1793616706'\n"
            "3. Fill Period: 2026-11-15 to 2026-12-15, Due: 2026-12-31\n"
            "4. Select 'All eligible schools' & 'All eligible students'\n"
            "5. Click 'Create draft' button\n"
            "6. Inspect Preview table: verify Liam Pham SGD 100.00\n"
            "7. Click 'Publish' button to post charges"
        ),
        "locators": (
            "#fee-publication-title\n"
            "#fee-publication-period-start, end, due-date\n"
            "label:has-text('All eligible schools')\n"
            "label:has-text('All eligible students')\n"
            "button[type='submit']:has-text('Create draft')\n"
            "tr:has-text('Liam Pham')\n"
            "button:has-text('Publish')"
        ),
        "test_data": (
            "Batch Title: P1 Tuition Batch 1793616706\n"
            "Component ID: 4de6f187-f6a1-44ef-b4d7-905b5214cefc\n"
            "Period: 2026-11-15 to 2026-12-15 | Due: 2026-12-31\n"
            "Cohort: Primary 1 (Rosyth Primary School)\n"
            "Preview Target: Liam Pham (SGD 100.00)"
        ),
        "expected": (
            "Preview accurately displays Liam Pham with gross SGD 100.00; "
            "Publish action transitions batch status to Completed and posts debt to ledger (POSTED status)."
        ),
        "actual": (
            "Xuất bản thành công Đợt phí 'P1 Tuition Batch 1793616706'; "
            "Preview xác nhận Liam Pham SGD 100.00; Nợ sinh ở trạng thái POSTED trong sổ công nợ."
        ),
        "status": "PASS",
        "metrics": "Duration: 6.6s\nTimestamp:\n2026-11-02 17:50:30",
        "image_file": "05_batch_published.png",
    },
    {
        "stage_id": "STAGE-06\n(TC-E2E-06)",
        "module": "SBFAS Scheme Configuration (UAT-SCH-02)\nhttps://admin.20-255-158-192.sslip.io/sbfas-schemes/new",
        "actions": (
            "1. Authenticate as School Staff (staff1@IAM.edu.vn)\n"
            "2. Navigate to /sbfas-schemes/new\n"
            "3. Step 1: Fill Name, Open/Close dates, Effective dates, Budget 50000, click 'Next'\n"
            "4. Step 2: Tick Singapore citizen, GHI <= 3000, PCI <= 1000, click 'Next'\n"
            "5. Step 3: Click 'Add fee components', select Tuition Fee, set 100% subsidy, click 'Review'\n"
            "6. Step 4: Click 'Publish' to activate scheme"
        ),
        "locators": (
            "#sbfas-name, #sbfas-open-from, #sbfas-open-to\n"
            "#sbfas-effective-from, #sbfas-budget\n"
            "#sbfas-nationality-SC, #sbfas-ghi-to, #sbfas-pci-to\n"
            "button:has-text('Add fee components')\n"
            "[role='dialog'] input[type='checkbox']\n"
            "table input (100% rate)\n"
            "button:has-text('Publish')"
        ),
        "test_data": (
            "Scheme Name: SBFAS Tier 1 UAT 1793616706\n"
            "Budget: SGD 50,000\n"
            "Open: 2026-11-02 to 2026-11-30 | Eff: 2026-12-01 to 2027-11-30\n"
            "Eligibility: Singapore Citizen, GHI <= SGD 3,000, PCI <= SGD 1,000\n"
            "Subsidy Matrix: 100% Fee Waiver on Tuition Fee"
        ),
        "expected": (
            "Scheme is validated and published; status badge updates to 'Published'; "
            "Subsidy matrix is linked to school tuition component."
        ),
        "actual": (
            "Xuất bản thành công Đề án 'SBFAS Tier 1 UAT 1793616706' "
            "(Ngân sách SGD 50,000, Trợ cấp 100% Học phí); Status: Published."
        ),
        "status": "PASS",
        "metrics": "Duration: 12.2s\nTimestamp:\n2026-11-02 17:50:43",
        "image_file": "06_sbfas_published.png",
    },
    {
        "stage_id": "STAGE-07\n(TC-E2E-07)",
        "module": "FAS Assessment & Approval (UAT-SCH-03/035)\nhttps://admin.20-255-158-192.sslip.io/fas-applications",
        "actions": (
            "1. Navigate to /fas-applications as School Staff\n"
            "2. Locate pending application and click 'View details'\n"
            "3. Review Household Financials & Rule Engine status\n"
            "4. Click 'Approve' action button\n"
            "5. Confirm approval with Tier 1 (100% Fee Waiver)\n"
            "6. Verify status transitions from Pending to Approved"
        ),
        "locators": (
            "table tbody tr button:has-text('View details')\n"
            "button:has-text('Approve')\n"
            "[role='dialog'] button:has-text('Approve'), button:has-text('Confirm')\n"
            "badge / pill:has-text('Approved')"
        ),
        "test_data": (
            "Application Code: APP-01004 / Liam Pham\n"
            "Applicant: Ethan Rahman / Liam Pham\n"
            "Assigned Tier: Tier 1 (100% Fee Waiver)\n"
            "School: Rosyth Primary School\n"
            "Remarks: Eligible for Tier 1 Full Support"
        ),
        "expected": (
            "Application status transitions to 'Approved'; subsidy structure Tier 1 applied; "
            "student billing account reflects 100% fee waiver for tuition."
        ),
        "actual": (
            "Thẩm định thành công hồ sơ trợ cấp; "
            "Cấu trúc hỗ trợ Tier 1 (100% Fee Waiver) áp dụng vào sổ nợ học sinh; Status: Approved."
        ),
        "status": "PASS",
        "metrics": "Duration: 2.6s\nTimestamp:\n2026-11-02 17:52:35",
        "image_file": "07_fas_approved.png",
    },
    {
        "stage_id": "STAGE-08\n(TC-E2E-08)",
        "module": "Parent Settlement & Handoff (UAT-PAR-01)\nhttps://eservice.20-255-158-192.sslip.io/accounts/STU-001/pay",
        "actions": (
            "1. Navigate to Parent E-Service /parent/login\n"
            "2. Sign in via Singpass Mock (Pham Van Duc / S7654321B)\n"
            "3. Navigate to Outstanding Charges /accounts/STU-001/pay\n"
            "4. Verify Gross Fee, SBFAS Subsidy waiver, and Net Amount Due\n"
            "5. Select fee checkbox and click 'Continue'\n"
            "6. Select payment method: 'Education Account' (Edusave EA)\n"
            "7. Click 'Continue' to Authorization screen\n"
            "8. Click 'Authorize & pay' to execute real-time deduction\n"
            "9. Verify official transaction receipt & status 'PAID'"
        ),
        "locators": (
            "button:has-text('Sign in with Singpass')\n"
            "#btn-login-selected\n"
            "tbody tr input[type='checkbox']\n"
            "button:has-text('Continue')\n"
            "input[value='EducationAccount']\n"
            "button:has-text('Authorize & pay')"
        ),
        "test_data": (
            "Parent Singpass: S7654321B (Pham Van Duc)\n"
            "Student Account: STU-001 (Liam Pham)\n"
            "Payment Method: Education Account (Edusave EA)\n"
            "Original Fee: SGD 100.00 Gross (Tuition) / SGD 19.50 (Misc Fee)\n"
            "Subsidy Offset: -SGD 100.00 (100% Waiver)"
        ),
        "expected": (
            "Subsidy waiver accurately deducted from Gross Fee; Net balance paid via Edusave EA wallet; "
            "Payment receipt generated and charge status transitioned to PAID."
        ),
        "actual": (
            "Đối soát giảm trừ trợ cấp chính xác; Gavin thanh toán thành công qua ví Edusave EA; "
            "Trạng thái khoản thu chuyển sang PAID; Official receipt issued."
        ),
        "status": "PASS",
        "metrics": "Duration: 16.4s\nTimestamp:\n2026-11-02 17:52:51",
        "image_file": "08_payment_settled.png",
    },
]

def generate_report():
    print(f"Creating workbook: {OUTPUT_FILE}")
    wb = openpyxl.Workbook()
    
    # CRITICAL RULE: Exactly 1 sheet/tab
    ws = wb.active
    ws.title = "E2E UI Automation Flow"
    
    # Ensure sheet view has gridlines enabled
    ws.views.sheetView[0].showGridLines = True
    
    # Freeze panes at A5 (rows 1-4 frozen)
    ws.freeze_panes = "A5"
    
    # -------------------------------------------------------------------------
    # ROW 1: MASTER TITLE BANNER (A1:J1)
    # -------------------------------------------------------------------------
    ws.merge_cells("A1:J1")
    cell_a1 = ws["A1"]
    cell_a1.value = "EDUFAMS SPRINT 3 — LIVE END-TO-END HAPPY PATH UI AUTOMATION REPORT"
    cell_a1.font = TITLE_FONT
    cell_a1.fill = DARK_NAVY_FILL
    cell_a1.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 32
    
    # Fill remaining merged cells in row 1 for border/fill consistency
    for col_idx in range(1, 11):
        c = ws.cell(row=1, column=col_idx)
        c.fill = DARK_NAVY_FILL
        c.border = THIN_BORDER
        
    # -------------------------------------------------------------------------
    # ROW 2: SUBTITLE / ENVIRONMENT BANNER (A2:J2)
    # -------------------------------------------------------------------------
    ws.merge_cells("A2:J2")
    cell_a2 = ws["A2"]
    cell_a2.value = (
        "Target Environments: Admin Portal (https://admin.20-255-158-192.sslip.io)  |  "
        "Parent E-Service (https://eservice.20-255-158-192.sslip.io)  |  "
        "Engine: Playwright v1.50 (Python) Headless  |  Traceability: UAT-019 to UAT-PAR-01"
    )
    cell_a2.font = SUBTITLE_FONT
    cell_a2.fill = SUBHEADER_FILL
    cell_a2.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[2].height = 22
    
    for col_idx in range(1, 11):
        c = ws.cell(row=2, column=col_idx)
        c.fill = SUBHEADER_FILL
        c.border = THIN_BORDER

    # -------------------------------------------------------------------------
    # ROW 3: KPI SUMMARY STATS BAR (A3:J3)
    # -------------------------------------------------------------------------
    ws.merge_cells("A3:J3")
    cell_a3 = ws["A3"]
    cell_a3.value = (
        "PIPELINE METRICS:  8 of 8 Stages Executed (100.0%)  |  Total Flow Duration: 64.9s  |  "
        "Overall Status: 8 PASS / 0 FAIL  |  Execution Date: 2026-11-02 17:52:51 SGT  |  "
        "Evidence Resolution: 1440 x 900 (High-Fidelity UI Capture)"
    )
    cell_a3.font = SUMMARY_FONT
    cell_a3.fill = SUMMARY_FILL
    cell_a3.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[3].height = 24
    
    for col_idx in range(1, 11):
        c = ws.cell(row=3, column=col_idx)
        c.fill = SUMMARY_FILL
        c.border = THIN_BORDER

    # -------------------------------------------------------------------------
    # ROW 4: TABLE COLUMN HEADERS
    # -------------------------------------------------------------------------
    headers = [
        "Stage / Step ID",
        "Module Name & Web URL",
        "UI Action & Interaction Steps",
        "Target UI Locator & Element",
        "Input Test Data",
        "Expected Web UI Result",
        "Actual Web UI Result",
        "Execution Status",
        "Execution Duration & Timestamp",
        "Web UI Screenshot Evidence"
    ]
    
    ws.row_dimensions[4].height = 32
    for col_idx, header_text in enumerate(headers, 1):
        cell = ws.cell(row=4, column=col_idx, value=header_text)
        cell.fill = DARK_NAVY_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = THIN_BORDER

    # -------------------------------------------------------------------------
    # ROWS 5 to 12: DATA ROWS + EMBEDDED IMAGES
    # -------------------------------------------------------------------------
    start_row = 5
    row_height = 158  # points (≈ 210 px, perfectly enclosing 200px height image)

    for idx, data in enumerate(STAGE_DATA):
        curr_row = start_row + idx
        ws.row_dimensions[curr_row].height = row_height
        
        row_fill = ZEBRA_FILL if (idx % 2 == 1) else WHITE_FILL
        
        # Col A: Stage / Step ID
        cell_a = ws.cell(row=curr_row, column=1, value=data["stage_id"])
        cell_a.font = STAGE_ID_FONT
        cell_a.fill = row_fill
        cell_a.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell_a.border = THIN_BORDER
        
        # Col B: Module Name & Web URL
        cell_b = ws.cell(row=curr_row, column=2, value=data["module"])
        cell_b.font = BOLD_REG_FONT
        cell_b.fill = row_fill
        cell_b.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        cell_b.border = THIN_BORDER

        # Col C: UI Action & Interaction Steps
        cell_c = ws.cell(row=curr_row, column=3, value=data["actions"])
        cell_c.font = REGULAR_FONT
        cell_c.fill = row_fill
        cell_c.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        cell_c.border = THIN_BORDER

        # Col D: Target UI Locator & Element
        cell_d = ws.cell(row=curr_row, column=4, value=data["locators"])
        cell_d.font = CODE_FONT
        cell_d.fill = row_fill
        cell_d.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        cell_d.border = THIN_BORDER

        # Col E: Input Test Data
        cell_e = ws.cell(row=curr_row, column=5, value=data["test_data"])
        cell_e.font = REGULAR_FONT
        cell_e.fill = row_fill
        cell_e.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        cell_e.border = THIN_BORDER

        # Col F: Expected Web UI Result
        cell_f = ws.cell(row=curr_row, column=6, value=data["expected"])
        cell_f.font = REGULAR_FONT
        cell_f.fill = row_fill
        cell_f.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        cell_f.border = THIN_BORDER

        # Col G: Actual Web UI Result
        cell_g = ws.cell(row=curr_row, column=7, value=data["actual"])
        cell_g.font = REGULAR_FONT
        cell_g.fill = row_fill
        cell_g.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        cell_g.border = THIN_BORDER

        # Col H: Execution Status (PASS Badge)
        cell_h = ws.cell(row=curr_row, column=8, value=data["status"])
        cell_h.font = PASS_FONT
        cell_h.fill = PASS_FILL
        cell_h.alignment = Alignment(horizontal="center", vertical="center")
        cell_h.border = Border(
            left=Side(style='thin', color='86EFAC'),
            right=Side(style='thin', color='86EFAC'),
            top=Side(style='thin', color='86EFAC'),
            bottom=Side(style='thin', color='86EFAC')
        )

        # Col I: Execution Duration & Timestamp
        cell_i = ws.cell(row=curr_row, column=9, value=data["metrics"])
        cell_i.font = REGULAR_FONT
        cell_i.fill = row_fill
        cell_i.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell_i.border = THIN_BORDER

        # Col J: Web UI Screenshot Evidence Cell Formatting
        cell_j = ws.cell(row=curr_row, column=10, value="")
        cell_j.fill = row_fill
        cell_j.alignment = Alignment(horizontal="center", vertical="center")
        cell_j.border = THIN_BORDER

        # Embed Image into Col J
        img_path = EVIDENCE_DIR / data["image_file"]
        if img_path.exists():
            img = OpenpyxlImage(str(img_path))
            img.width = 356
            img.height = 200
            ws.add_image(img, f"J{curr_row}")
            print(f"  [+] Embedded {data['image_file']} at cell J{curr_row} (width={img.width}, height={img.height})")
        else:
            print(f"  [!] Missing image: {img_path}")

    # -------------------------------------------------------------------------
    # COLUMN WIDTHS CONFIGURATION
    # -------------------------------------------------------------------------
    col_widths = {
        "A": 16,  # Stage / Step ID
        "B": 32,  # Module Name & Web URL
        "C": 44,  # UI Action & Interaction Steps
        "D": 34,  # Target UI Locator & Element
        "E": 34,  # Input Test Data
        "F": 36,  # Expected Web UI Result
        "G": 36,  # Actual Web UI Result
        "H": 18,  # Execution Status
        "I": 24,  # Duration & Timestamp
        "J": 54,  # Screenshot Evidence (~356px width)
    }

    for col_letter, width in col_widths.items():
        ws.column_dimensions[col_letter].width = width

    # Save Workbook
    wb.save(OUTPUT_FILE)
    print(f"\n✓ Successfully generated single-tab Excel report: {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_report()
