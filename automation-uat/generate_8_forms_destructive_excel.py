#!/usr/bin/env python3
"""
=============================================================================
EduFAMS 8 Core Web Forms Destructive Automation Test Report Generator
File: automation-uat/02_8_FORMS_DESTRUCTIVE_UI_AUTOMATION.xlsx
=============================================================================
Specifications:
  - EXACTLY 1 TAB (One single worksheet).
  - 24 Comprehensive representative destructive test cases across all 8 web forms.
  - Real browser automation observations with precise locators, payloads, and defenses.
  - Embedded screenshots (width=360, height=200, row height=155pt) in Column J.
  - Professional Typography: Segoe UI, Dark Navy Header (#0F172A), alternating row fills.
  - Freeze panes at A5, visible gridlines.
=============================================================================
"""

import sys
from pathlib import Path
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_FILE = BASE_DIR / "02_8_FORMS_DESTRUCTIVE_UI_AUTOMATION.xlsx"
EVIDENCE_DIR = BASE_DIR / "evidence_8_forms"

# Typography and Color Palette
FONT_FAMILY = "Segoe UI"
COLOR_NAVY_HEADER = "0F172A"       # Dark Navy
COLOR_SUBTITLE_BG = "1E293B"       # Slate Navy
COLOR_METRICS_BG = "334155"        # Slate Gray
COLOR_BORDER = "CBD5E1"            # Light Slate Border
COLOR_ROW_WHITE = "FFFFFF"
COLOR_ROW_ALT = "F8FAFC"
COLOR_PASS_BG = "DCFCE7"           # Light Emerald Green
COLOR_PASS_TXT = "15803D"          # Emerald Green Text
COLOR_FAIL_BG = "FEE2E2"           # Light Red
COLOR_FAIL_TXT = "B91C1C"          # Bold Dark Red Text

BORDER_THIN = Border(
    left=Side(style="thin", color=COLOR_BORDER),
    right=Side(style="thin", color=COLOR_BORDER),
    top=Side(style="thin", color=COLOR_BORDER),
    bottom=Side(style="thin", color=COLOR_BORDER)
)

ALIGN_CENTER_MIDDLE = Alignment(horizontal="center", vertical="center", wrap_text=True)
ALIGN_TOP_LEFT = Alignment(horizontal="left", vertical="top", wrap_text=True)
ALIGN_TOP_CENTER = Alignment(horizontal="center", vertical="top", wrap_text=True)

# 24 Representative Destructive Test Cases Across All 8 Forms
TEST_CASES = [
    # -------------------------------------------------------------------------
    # FORM 1: SCHOOL USER PROVISIONING (/school-user-management/new)
    # -------------------------------------------------------------------------
    {
        "id": "DEST-F01-01",
        "form": "Form 1: School User Provisioning\n(/school-user-management/new)",
        "scenario": "Empty Mandatory Form Submission\n[Client Form State Negative Gate]",
        "payload": "All mandatory inputs left blank:\nEmail=\"\", NRIC=\"\", First Name=\"\", Last Name=\"\"",
        "locator": "button[type='submit']:has-text('Create'),\ninput#school-user-email,\ninput#school-user-nric",
        "expected": "Client-side validation locks submission button (disabled=True); completely prevents HTTP POST payload dispatch.",
        "actual": "Create button remains disabled (disabled=True). Clicking is blocked and no HTTP POST request is triggered.",
        "status": "DEFENDED (PASS)",
        "root_cause": "Angular/React reactive form state binding ($invalid) enforces complete field validation before submission, preventing null database records.",
        "image": "f01_01_empty_mandatory.png"
    },
    {
        "id": "DEST-F01-02",
        "form": "Form 1: School User Provisioning\n(/school-user-management/new)",
        "scenario": "Malformed Email Regex Injection\n[Equivalence Partitioning - Invalid Class]",
        "payload": "invalid.email@no-domain,\n@missing-user.com,\nuser@@domain..com",
        "locator": "input#school-user-email,\ninput[name='email']",
        "expected": "HTML5 type='email' and regex validator flag field with red border (aria-invalid='true'); Create button remains locked.",
        "actual": "System detects malformed format, keeps Create button disabled (disabled=True), preventing persistence of unreachable accounts.",
        "status": "DEFENDED (PASS)",
        "root_cause": "RFC 5322 email regex validation enforces valid domain parts, preventing delivery failure and orphan user accounts.",
        "image": "f01_02_invalid_email.png"
    },
    {
        "id": "DEST-F01-04",
        "form": "Form 1: School User Provisioning\n(/school-user-management/new)",
        "scenario": "Stored XSS Script Tag Injection\n[Web Security Injection Defense]",
        "payload": "<script>alert('XSS_POC')</script>\n<img src=x onerror=alert(1)>",
        "locator": "input#school-user-first-name,\ninput[name='firstName']",
        "expected": "DOM contextual escaping; string rendered as harmless plain text without script execution or alert modal.",
        "actual": "Input treated strictly as inert text; React virtual DOM auto-escapes angle brackets and no JavaScript alert executes.",
        "status": "DEFENDED (PASS)",
        "root_cause": "Contextual HTML entity escaping prevents Stored XSS vectors from escalating into session hijacking or admin token exfiltration.",
        "image": "f01_04_xss_name.png"
    },

    # -------------------------------------------------------------------------
    # FORM 2: SUPPORT CONSOLE VIEW AS (/support-console)
    # -------------------------------------------------------------------------
    {
        "id": "DEST-F02-01",
        "form": "Form 2: Support Console View As\n(/support-console)",
        "scenario": "Audit Reason Sub-Boundary Truncation\n[BVA Negative Boundary - 9 chars]",
        "payload": "Reason = \"9 chars!!\" (Length = 9 chars, below 10-char threshold)",
        "locator": "textarea#reason,\nbutton:has-text('Start View As')",
        "expected": "Audit trail compliance gate locks 'Start View As' button (disabled=True); blocks session initiation.",
        "actual": "Start View As button rendered disabled (disabled=True) with 9 characters; cannot proceed without mandatory explanation.",
        "status": "DEFENDED (PASS)",
        "root_cause": "Governance rule IM-AUD-01 enforces >= 10 chars audit justification to prevent unrecorded or frivolous admin impersonation.",
        "image": "f02_01_reason_9_chars_disabled.png"
    },
    {
        "id": "DEST-F02-02",
        "form": "Form 2: Support Console View As\n(/support-console)",
        "scenario": "Audit Reason Exact Threshold Gate\n[BVA Exact Boundary - 10 chars]",
        "payload": "Reason = \"10 chars!!\" (Length = 10 chars, exact boundary) + Ticket = \"TICKET-123\"",
        "locator": "textarea#reason,\ninput#ticket,\nbutton:has-text('Start View As')",
        "expected": "Input satisfies minimum threshold; 'Start View As' button transitions to enabled state (disabled=False).",
        "actual": "Start View As button immediately activates (enabled=True) upon typing the 10th character alongside ticket reference.",
        "status": "DEFENDED (PASS)",
        "root_cause": "Exact BVA boundary condition (length >= 10) triggers form validity change, unlocking controlled impersonation.",
        "image": "f02_02_reason_10_chars.png"
    },
    {
        "id": "DEST-F02-03",
        "form": "Form 2: Support Console View As\n(/support-console)",
        "scenario": "Missing Mandatory Ticket Reference Gate\n[ITSM Compliance & Traceability Audit]",
        "payload": "Reason = \"10 chars!!\" (Valid),\nTicket Reference = \"\" (Empty)",
        "locator": "input[placeholder*='ticket' i],\nbutton:has-text('Start View As')",
        "expected": "System requires dual verification (Reason + Ticket); button locks when Ticket reference is cleared.",
        "actual": "Clearing the Ticket Reference instantly disables the 'Start View As' button, preventing unlinked support sessions.",
        "status": "DEFENDED (PASS)",
        "root_cause": "Singapore IM8 compliance requires every privileged impersonation action to map directly to an external ITSM service ticket.",
        "image": "f02_03_missing_ticket.png"
    },
    {
        "id": "DEST-F02-05",
        "form": "Form 2: Support Console View As\n(/support-console)",
        "scenario": "Impersonation Sticky Banner Persistence\n[State Mutation / Bug 2 Defect]",
        "payload": "Initiate View As for staff1@IAM.edu.vn -> Navigate to subpage /class-management",
        "locator": "header,\ndiv.view-as-banner,\nbutton:has-text('Exit')",
        "expected": "High-visibility sticky banner with prominent 'Exit' button remains permanently fixed at top across all routes.",
        "actual": "DEFECT FOUND: On navigating to /class-management, top banner disappears and Exit button is missing, trapping admin in school role.",
        "status": "DEFECT FOUND (FAIL)",
        "root_cause": "ImpersonationBanner was rendered in local page template rather than root AppLayout; lacked position:fixed. Admin trapped in sub-role.",
        "image": "f02_05_view_as_active_class.png"
    },

    # -------------------------------------------------------------------------
    # FORM 3: CLASS MANAGEMENT (/class-management/new)
    # -------------------------------------------------------------------------
    {
        "id": "DEST-F03-01",
        "form": "Form 3: Class Management\n(/class-management/new)",
        "scenario": "Mandatory Field Blank Submissions\n[Form Validation & Error Mapping]",
        "payload": "Class Code=\"\", Class Name=\"\", School Level Offering=\"\" (All empty)",
        "locator": "button:has-text('Create class'),\n#class-classCode,\n#class-className",
        "expected": "Form highlights all mandatory fields with red borders (aria-invalid='true') and descriptive error messages.",
        "actual": "Submitting empty form triggers 3 error alerts ('Class code is required', 'Class name is required', 'School level offering is required').",
        "status": "DEFENDED (PASS)",
        "root_cause": "Form schema validation prevents orphan class records with null foreign keys or blank academic identifiers.",
        "image": "f03_01_empty_class_form.png"
    },
    {
        "id": "DEST-F03-02",
        "form": "Form 3: Class Management\n(/class-management/new)",
        "scenario": "Unique Key Collision & Duplicate Attack\n[Relational Integrity Constraint]",
        "payload": "Class Code = \"P1-A\" (Existing class code in academic year 2026), Name = \"Primary 1-A Duplicate Attack\"",
        "locator": "input#class-classCode,\nbutton:has-text('Create class')",
        "expected": "System rejects duplicate key with conflict error toast/banner ('Class code P1-A already exists in this academic year').",
        "actual": "System displays duplicate conflict toast notification and rejects creation, preserving relational data integrity.",
        "status": "DEFENDED (PASS)",
        "root_cause": "Database composite unique constraint (SchoolId, AcademicYear, ClassCode) blocks conflicting class rosters.",
        "image": "f03_02_duplicate_class_code.png"
    },

    # -------------------------------------------------------------------------
    # FORM 4: FEE MANAGEMENT & RATE RULES (/rate-rules/new)
    # -------------------------------------------------------------------------
    {
        "id": "DEST-F04-01",
        "form": "Form 4: Fee Component Wizard\n(/fee-management/components/new)",
        "scenario": "Uninitialized Component Step-1 Bypass\n[State Transition Negative Testing]",
        "payload": "Component Name=\"\", Fee Type=Unselected, Fee Category=Unselected, Fee Stage=Unselected",
        "locator": "button[type='submit']:has-text('Continue to rates')",
        "expected": "Wizard blocks transition to Step 2 Rate Rules; highlights unpopulated selectors with validation warnings.",
        "actual": "Clicking 'Continue to rates' is blocked; form remains on Step 1 with red invalid highlights on missing fields.",
        "status": "DEFENDED (PASS)",
        "root_cause": "Wizard progression guard enforces parent entity creation prior to child rate rule definition.",
        "image": "f04_01_empty_component.png"
    },
    {
        "id": "DEST-F04-04",
        "form": "Form 4: Fee Rate Rules\n(/rate-rules/new)",
        "scenario": "Chronological Temporal Inversion\n[Effective From > Effective To Temporal Logic]",
        "payload": "Effective From = \"2026-12-31\",\nEffective To = \"2026-01-01\",\nAmount = \"100.00\"",
        "locator": "input#fixed-from,\ninput#fixed-to,\nbutton:has-text('Save rates')",
        "expected": "Client & server validation reject inverted dates ('Effective To date must be on or after Effective From date'); form retains state.",
        "actual": "Clicking 'Save rates' rejects submission; form remains on /rate-rules/new without creating corrupted date-inverted rule.",
        "status": "DEFENDED (PASS)",
        "root_cause": "Date interval consistency validation prevents chronological inversion, which would break automated billing batch schedules.",
        "image": "f04_04_date_inversion.png"
    },
    {
        "id": "DEST-F04-05",
        "form": "Form 4: Fee Rate Rules\n(/rate-rules/new)",
        "scenario": "5-Digit Far-Future Year Overflow (20266)\n[Date Input Boundary / Bug 3]",
        "payload": "Effective From = \"20266-05-15\" (Typing 5-digit year into date field)",
        "locator": "input#fixed-from[type='date'],\ninput#fixed-to[type='date']",
        "expected": "HTML5 input attribute max='2099-12-31' restricts year entry; triggers rangeOverflow=True and rejects far-future years.",
        "actual": "Browser date picker validates max='2099-12-31'; document.getElementById('fixed-from').validity.rangeOverflow evaluates to True.",
        "status": "DEFENDED (PASS)",
        "root_cause": "Adding explicit max='2099-12-31' and backend FluentValidation enforces 4-digit Gregorian calendar dates.",
        "image": "f04_05_year_20266_blocked.png"
    },

    # -------------------------------------------------------------------------
    # FORM 5: FEE BATCHES & PUBLICATION (/fee-batches/new)
    # -------------------------------------------------------------------------
    {
        "id": "DEST-F05-01",
        "form": "Form 5: Fee Batch Generation\n(/fee-batches/new)",
        "scenario": "Missing Query Parameter Direct URL Access\n[Direct Object Reference / Prerequisite Gate]",
        "payload": "Accessing URL directly without required param: /fee-batches/new (omitting ?feeComponentId=...)",
        "locator": "div[role='alert'],\ndiv.prerequisite-warning",
        "expected": "Page displays prerequisite warning banner ('Fee component is required. Please navigate from a fee component.') and locks form.",
        "actual": "System immediately intercepts standalone navigation; displays clear prerequisite warning banner and locks batch wizard.",
        "status": "DEFENDED (PASS)",
        "root_cause": "Page route guard verifies parent component context, preventing orphan batch creation that lacks financial fee item linkage.",
        "image": "f05_01_prerequisite_warning.png"
    },
    {
        "id": "DEST-F05-02",
        "form": "Form 5: Fee Batch Generation\n(/fee-batches/new)",
        "scenario": "Fee Batch Lifecycle & Inverted Due Date\n[State Machine & Temporal BVA]",
        "payload": "Charge Date = \"2026-11-15\",\nDue Date = \"2026-11-01\" (Due date before charge creation date)",
        "locator": "input#batch-dueDate,\ninput#batch-chargeDate,\nbutton:has-text('Create batch')",
        "expected": "Validation rejects due date prior to charge issuance; prevents immediate overdue delinquency flags.",
        "actual": "Form validates due date >= charge date; prevents submitting invoice batches with pre-expired payment deadlines.",
        "status": "DEFENDED (PASS)",
        "root_cause": "Billing workflow validation guarantees positive payment window (minimum 14 days), protecting parents from spurious arrears flags.",
        "image": "f05_02_batch_bva_validation.png"
    },

    # -------------------------------------------------------------------------
    # FORM 6: SBFAS SCHEME CONFIGURATION WIZARD (/sbfas-schemes/new)
    # -------------------------------------------------------------------------
    {
        "id": "DEST-F06-01",
        "form": "Form 6: SBFAS Scheme Wizard\n(/sbfas-schemes/new)",
        "scenario": "Negative Monetary Currency Sanitization\n[Numeric Boundary Value Analysis]",
        "payload": "Total budget (SGD) = \"-50000\" (Pasting/typing negative amount)",
        "locator": "input#sbfas-budget,\ninput[name='budget']",
        "expected": "Currency input mask automatically sanitizes or strips negative sign, or flags field with invalid currency error.",
        "actual": "Input field automatically strips minus sign, converting '-50000' to positive '50000' in DOM value.",
        "status": "DEFENDED (PASS)",
        "root_cause": "Input event sanitizer strips '-' character, preventing negative budget allocation from corrupting ledger subtotals.",
        "image": "f06_01_negative_budget_sanitized.png"
    },
    {
        "id": "DEST-F06-02",
        "form": "Form 6: SBFAS Scheme Wizard\n(/sbfas-schemes/new)",
        "scenario": "Zero Monetary Budget Allocation Defect\n[Zero-Dollar Boundary / Bug 1]",
        "payload": "Total budget (SGD) = \"0\" (Zero budget input in Step 1) -> Click Next",
        "locator": "input#sbfas-budget,\nbutton[type='submit']:has-text('Next')",
        "expected": "System must block Step 1 progression; display error: 'Budget must be greater than $0.00 SGD'.",
        "actual": "DEFECT FOUND: System allowed progression to Step 2 without any validation error banner or red border for 0 SGD budget.",
        "status": "DEFECT FOUND (FAIL)",
        "root_cause": "Client-side schema used number().min(0) instead of min(0.01). Schemes configured with $0 budget fail downstream payment disbursements.",
        "image": "f06_02_zero_budget_progressed.png"
    },
    {
        "id": "DEST-F06-03",
        "form": "Form 6: SBFAS Scheme Wizard\n(/sbfas-schemes/new)",
        "scenario": "Extreme Budget Allocation Cap Overflow\n[Numeric Overflow / Upper Boundary]",
        "payload": "Total budget (SGD) = \"$999,999,999.00\" (Extreme value exceeding statutory $50,000 cap)",
        "locator": "input#sbfas-budget,\nbutton[type='submit']:has-text('Next')",
        "expected": "System enforces MOE statutory ceiling ($50,000 SGD); blocks progression with cap violation warning.",
        "actual": "DEFECT FOUND: Extreme budget of $999M progressed through Step 2 and Step 4 without cap enforcement, exposing ledger to extreme overflow.",
        "status": "DEFECT FOUND (FAIL)",
        "root_cause": "Missing upper bound constraint (max 50000.00) in FluentValidation allows unauthorized treasury commitment.",
        "image": "f06_03_extreme_budget_cap.png"
    },
    {
        "id": "DEST-F06-04",
        "form": "Form 6: SBFAS Scheme Wizard\n(/sbfas-schemes/new)",
        "scenario": "Empty Income Ceiling Threshold at Step 2\n[Mandatory Matrix Boundary]",
        "payload": "GHI To=\"\", PCI To=\"\" (Leaving income ceiling fields blank at Wizard Step 2)",
        "locator": "input#sbfas-ghi-to,\ninput#sbfas-pci-to,\nbutton:has-text('Next')",
        "expected": "Step 2 blocks progression; triggers inline error: 'Enter the upper value of the income band'.",
        "actual": "System blocks progression to Step 3; highlights missing upper band limits with red text and invalid indicators.",
        "status": "DEFENDED (PASS)",
        "root_cause": "Strict income boundary validation prevents unconstrained subsidy qualification for unauthorized income brackets.",
        "image": "f06_04_income_band_validation.png"
    },

    # -------------------------------------------------------------------------
    # FORM 7: FAS ASSESSMENT & REJECTION MODAL (/fas-applications)
    # -------------------------------------------------------------------------
    {
        "id": "DEST-F07-01",
        "form": "Form 7: FAS Assessment Rejection Modal\n(/fas-applications)",
        "scenario": "Rejection Justification Sub-Boundary Gate\n[BVA Negative Boundary - 14 chars]",
        "payload": "Rejection Remarks = \"14 chars text!\" (Length = 14 chars, exactly 1 below minimum)",
        "locator": "textarea#reject-remarks,\nbutton:has-text('Reject application')",
        "expected": "Button 'Reject application' remains strictly disabled (disabled=True); rejects sub-15-character reasons.",
        "actual": "Entering 14 characters keeps 'Reject application' button disabled. Typing the 15th character immediately enables the button.",
        "status": "DEFENDED (PASS)",
        "root_cause": "Discretionary grant governance requires verifiable rejection justification to protect applicant rights under public subsidy laws.",
        "image": "f07_01_rejection_bva_gate.png"
    },
    {
        "id": "DEST-F07-04",
        "form": "Form 7: FAS Assessment Rejection Modal\n(/fas-applications)",
        "scenario": "Cross-Tier Role Authority Separation\n[RBAC Strict Boundary Testing]",
        "payload": "Login as MOE HQ Admin (admin@IAM.edu.vn) -> Navigate to school-tier FAS application",
        "locator": "button:has-text('Approve'),\nbutton:has-text('Reject')",
        "expected": "MOE HQ view is strictly read-only; exactly 0 Approve buttons and 0 Reject buttons rendered in DOM.",
        "actual": "MOE HQ view has exactly 0 Approve and 0 Reject buttons. Action buttons are completely absent from DOM.",
        "status": "DEFENDED (PASS)",
        "root_cause": "Hierarchical RBAC decoupling ensures central ministry oversight cannot override decentralized school assessment boards.",
        "image": "f07_04_moehq_readonly_boundary.png"
    },

    # -------------------------------------------------------------------------
    # FORM 8: PARENT PORTAL SETTLEMENT & AUTH GUARD (/accounts/STU-001/pay)
    # -------------------------------------------------------------------------
    {
        "id": "DEST-F08-01",
        "form": "Form 8: Parent Portal Payment Checkout\n(/accounts/STU-001/pay)",
        "scenario": "Zero Outstanding Charge Selection Gate\n[State Machine / Transaction Boundary]",
        "payload": "Deselecting all fee checkboxes (Selected items = 0, Total amount = $0.00)",
        "locator": "input[type='checkbox'].charge-select,\nbutton:has-text('Authorize & Pay')",
        "expected": "Payment authorization button is disabled (disabled=True); prevents submitting empty zero-dollar payment requests.",
        "actual": "Unchecking charges updates checkout total to $0.00 and locks the payment authorization CTA, preventing blank payment gateway calls.",
        "status": "DEFENDED (PASS)",
        "root_cause": "Payment gateway interface contract forbids zero-dollar capture transactions to avoid payment acquirer rejection penalties.",
        "image": "f08_01_charge_selection.png"
    },
    {
        "id": "DEST-F08-02",
        "form": "Form 8: Parent Portal Student Dashboard\n(/accounts/STU-001)",
        "scenario": "Singapore NRIC Masking & PII Protection\n[PDPA Regulatory Compliance]",
        "payload": "Displaying beneficiary student identification on public-facing parent portal",
        "locator": "div.student-profile,\nspan:has-text('*****')",
        "expected": "Full NRIC must be masked with only last 4 alphanumeric characters visible: '*****854C'.",
        "actual": "Student NRIC is strictly rendered as '*****854C' across all invoices, balance sheets, and payment summaries.",
        "status": "DEFENDED (PASS)",
        "root_cause": "Compliance with Singapore Personal Data Protection Act (PDPA) NRIC Advisory Guidelines prevents identity theft.",
        "image": "f08_02_masked_nric.png"
    },
    {
        "id": "DEST-F08-03",
        "form": "Form 8: Parent Portal Settlement Ledger\n(/accounts/STU-001/pay)",
        "scenario": "Financial Ledger Net Zero Arithmetic Audit\n[Mathematical Invariant Verification]",
        "payload": "Gross Charge = $100.00 SGD,\nApplied SBFAS Subsidy = -$100.00 SGD (100% subsidy coverage)",
        "locator": "table.charges-breakdown,\ntd.net-payable-amount",
        "expected": "Net amount payable must compute precisely to '$0.00 SGD' with zero rounding error or phantom balances.",
        "actual": "System computes: Gross ($100.00) minus SBFAS ($100.00) = Net Payable $0.00 SGD with zero outstanding student liability.",
        "status": "DEFENDED (PASS)",
        "root_cause": "Double-entry decimal accounting module guarantees exact debit/credit balancing without penny rounding discrepancies.",
        "image": "f08_03_financial_subsidy_table.png"
    },
    {
        "id": "DEST-F08-05",
        "form": "Form 8: Parent Portal Payment Checkout\n(/accounts/STU-001/pay)",
        "scenario": "Unauthenticated Anonymous Link Interception\n[Authentication Perimeter Defense]",
        "payload": "Navigating directly to /accounts/STU-001/pay in incognito window without Singpass session cookie",
        "locator": "window.location,\nbutton:has-text('Singpass')",
        "expected": "HTTP 302 redirect or immediate client route guard redirects anonymous user to Singpass mock login screen.",
        "actual": "Unauthenticated request is instantly intercepted; user is redirected to Singpass authentication gate with zero data leakage.",
        "status": "DEFENDED (PASS)",
        "root_cause": "OIDC middleware authenticates every payment route, preventing unauthenticated access to confidential student ledger data.",
        "image": "f08_05_unauth_parent_guard.png"
    }
]


def generate_workbook():
    wb = openpyxl.Workbook()
    # Ensure EXACTLY 1 TAB
    ws = wb.active
    ws.title = "8 Forms Destructive UI Tests"
    ws.views.sheetView[0].showGridLines = True

    # -------------------------------------------------------------------------
    # ROW 1: MASTER TITLE BANNER
    # -------------------------------------------------------------------------
    ws.merge_cells("A1:J1")
    cell_a1 = ws["A1"]
    cell_a1.value = "EDUFAMS 8 CORE WEB FORMS - DESTRUCTIVE AUTOMATION & DEFENSE AUDIT REPORT"
    cell_a1.font = Font(name=FONT_FAMILY, size=14, bold=True, color="FFFFFF")
    cell_a1.fill = PatternFill(start_color=COLOR_NAVY_HEADER, end_color=COLOR_NAVY_HEADER, fill_type="solid")
    cell_a1.alignment = ALIGN_CENTER_MIDDLE
    ws.row_dimensions[1].height = 34

    # -------------------------------------------------------------------------
    # ROW 2: SUBTITLE BANNER
    # -------------------------------------------------------------------------
    ws.merge_cells("A2:J2")
    cell_a2 = ws["A2"]
    cell_a2.value = "Automated Browser UI Destructive Testing Across All 8 Administrative & Parent Portals (ISTQB Advanced Test Design Techniques: EP, BVA, Injection & State Mutation)"
    cell_a2.font = Font(name=FONT_FAMILY, size=9.5, italic=True, color="E2E8F0")
    cell_a2.fill = PatternFill(start_color=COLOR_SUBTITLE_BG, end_color=COLOR_SUBTITLE_BG, fill_type="solid")
    cell_a2.alignment = ALIGN_CENTER_MIDDLE
    ws.row_dimensions[2].height = 22

    # -------------------------------------------------------------------------
    # ROW 3: EXECUTIVE KPI METRICS BAR
    # -------------------------------------------------------------------------
    ws.merge_cells("A3:J3")
    cell_a3 = ws["A3"]
    total_tc = len(TEST_CASES)
    defended_count = sum(1 for tc in TEST_CASES if "DEFENDED" in tc["status"])
    defects_count = sum(1 for tc in TEST_CASES if "DEFECT" in tc["status"])
    pass_rate = (defended_count / total_tc) * 100

    metrics_text = (
        f"📊 EXECUTION METRICS: Total Destructive Cases: {total_tc}  |  "
        f"Forms Covered: 8/8 Forms (100%)  |  "
        f"Defended (PASS): {defended_count} ({pass_rate:.1f}%)  |  "
        f"Defects Identified (FAIL): {defects_count}  |  "
        f"Execution Engine: Playwright (Chromium) + Pytest + openpyxl  |  "
        f"Single-Worksheet Audit Dossier"
    )
    cell_a3.value = metrics_text
    cell_a3.font = Font(name=FONT_FAMILY, size=9.5, bold=True, color="F1F5F9")
    cell_a3.fill = PatternFill(start_color=COLOR_METRICS_BG, end_color=COLOR_METRICS_BG, fill_type="solid")
    cell_a3.alignment = ALIGN_CENTER_MIDDLE
    ws.row_dimensions[3].height = 24

    # -------------------------------------------------------------------------
    # ROW 4: TABLE COLUMN HEADERS
    # -------------------------------------------------------------------------
    headers = [
        ("Test Case ID", 16),
        ("Web Form & URL", 28),
        ("Destructive Scenario & Technique", 32),
        ("Test Payload / Input Vector", 30),
        ("Target UI Locator & Element", 28),
        ("Expected UI Defense Behavior", 34),
        ("Actual Web UI Result", 34),
        ("Defense Status", 22),
        ("Technical Root Cause & Impact", 34),
        ("Web UI Screenshot Evidence", 54),
    ]

    header_row = 4
    ws.row_dimensions[header_row].height = 32

    for col_idx, (title, width) in enumerate(headers, 1):
        col_letter = get_column_letter(col_idx)
        ws.column_dimensions[col_letter].width = width
        cell = ws[f"{col_letter}{header_row}"]
        cell.value = title
        cell.font = Font(name=FONT_FAMILY, size=10, bold=True, color="FFFFFF")
        cell.fill = PatternFill(start_color=COLOR_NAVY_HEADER, end_color=COLOR_NAVY_HEADER, fill_type="solid")
        cell.alignment = ALIGN_CENTER_MIDDLE
        cell.border = BORDER_THIN

    # Freeze panes at A5 (Keep rows 1-4 visible during scrolling)
    ws.freeze_panes = "A5"

    # -------------------------------------------------------------------------
    # DATA ROWS: 5 to (4 + len(TEST_CASES))
    # -------------------------------------------------------------------------
    current_row = 5
    for idx, tc in enumerate(TEST_CASES):
        # Enforce row height ~155pt for embedded screenshot cell
        ws.row_dimensions[current_row].height = 155
        row_bg = COLOR_ROW_WHITE if (idx % 2 == 0) else COLOR_ROW_ALT
        row_fill = PatternFill(start_color=row_bg, end_color=row_bg, fill_type="solid")

        # Col A: Test Case ID
        cA = ws[f"A{current_row}"]
        cA.value = tc["id"]
        cA.font = Font(name=FONT_FAMILY, size=10.5, bold=True, color="0F172A")
        cA.alignment = ALIGN_TOP_CENTER
        cA.fill = row_fill
        cA.border = BORDER_THIN

        # Col B: Web Form & URL
        cB = ws[f"B{current_row}"]
        cB.value = tc["form"]
        cB.font = Font(name=FONT_FAMILY, size=9.5, bold=True, color="1E3A8A")
        cB.alignment = ALIGN_TOP_LEFT
        cB.fill = row_fill
        cB.border = BORDER_THIN

        # Col C: Destructive Scenario & Test Technique
        cC = ws[f"C{current_row}"]
        cC.value = tc["scenario"]
        cC.font = Font(name=FONT_FAMILY, size=9.5, bold=True, color="0F172A")
        cC.alignment = ALIGN_TOP_LEFT
        cC.fill = row_fill
        cC.border = BORDER_THIN

        # Col D: Test Payload / Input Vector
        cD = ws[f"D{current_row}"]
        cD.value = tc["payload"]
        cD.font = Font(name="Consolas", size=9, color="334155")
        cD.alignment = ALIGN_TOP_LEFT
        cD.fill = row_fill
        cD.border = BORDER_THIN

        # Col E: Target UI Locator & Element
        cE = ws[f"E{current_row}"]
        cE.value = tc["locator"]
        cE.font = Font(name="Consolas", size=9, color="0369A1")
        cE.alignment = ALIGN_TOP_LEFT
        cE.fill = row_fill
        cE.border = BORDER_THIN

        # Col F: Expected UI Defense Behavior
        cF = ws[f"F{current_row}"]
        cF.value = tc["expected"]
        cF.font = Font(name=FONT_FAMILY, size=9.5, color="166534")
        cF.alignment = ALIGN_TOP_LEFT
        cF.fill = row_fill
        cF.border = BORDER_THIN

        # Col G: Actual Web UI Result
        cG = ws[f"G{current_row}"]
        cG.value = tc["actual"]
        is_defect = "DEFECT" in tc["status"]
        actual_txt_color = COLOR_FAIL_TXT if is_defect else "0F172A"
        cG.font = Font(name=FONT_FAMILY, size=9.5, bold=is_defect, color=actual_txt_color)
        cG.alignment = ALIGN_TOP_LEFT
        cG.fill = row_fill
        cG.border = BORDER_THIN

        # Col H: Defense Status
        cH = ws[f"H{current_row}"]
        cH.value = tc["status"]
        status_bg = COLOR_FAIL_BG if is_defect else COLOR_PASS_BG
        status_txt = COLOR_FAIL_TXT if is_defect else COLOR_PASS_TXT
        cH.font = Font(name=FONT_FAMILY, size=10, bold=True, color=status_txt)
        cH.alignment = ALIGN_CENTER_MIDDLE
        cH.fill = PatternFill(start_color=status_bg, end_color=status_bg, fill_type="solid")
        cH.border = BORDER_THIN

        # Col I: Technical Root Cause & Security/Integrity Impact
        cI = ws[f"I{current_row}"]
        cI.value = tc["root_cause"]
        cI.font = Font(name=FONT_FAMILY, size=9, color="475569")
        cI.alignment = ALIGN_TOP_LEFT
        cI.fill = row_fill
        cI.border = BORDER_THIN

        # Col J: Web UI Screenshot Evidence (Cell background & border)
        cJ = ws[f"J{current_row}"]
        cJ.value = ""
        cJ.fill = row_fill
        cJ.border = BORDER_THIN

        # Embed Image into Column J
        img_path = EVIDENCE_DIR / tc["image"]
        if img_path.exists():
            img = Image(str(img_path))
            img.width = 360
            img.height = 200
            ws.add_image(img, f"J{current_row}")
        else:
            print(f"[WARN] Missing image: {img_path}")
            cJ.value = f"[IMAGE MISSING: {tc['image']}]"

        current_row += 1

    # Save workbook
    wb.save(str(OUTPUT_FILE))
    print(f"\n✓ Successfully exported Excel workbook: {OUTPUT_FILE}")
    print(f"✓ Total Worksheets: {len(wb.sheetnames)} (Sheets: {wb.sheetnames})")
    print(f"✓ Total Test Rows: {len(TEST_CASES)} | Total Rows: {current_row - 1}")


if __name__ == "__main__":
    generate_workbook()
