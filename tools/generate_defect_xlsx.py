import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image as OpenpyxlImage
from PIL import Image as PILImage
import os

def create_defect_excel_with_images(output_path):
    wb = openpyxl.Workbook()
    font_family = "Segoe UI"
    
    # -------------------------------------------------------------
    # Palette & Styles
    # -------------------------------------------------------------
    navy_fill = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
    dark_slate_fill = PatternFill(start_color="2F5597", end_color="2F5597", fill_type="solid")
    subtle_gray_fill = PatternFill(start_color="F2F4F7", end_color="F2F4F7", fill_type="solid")
    zebra_fill = PatternFill(start_color="F9FAFB", end_color="F9FAFB", fill_type="solid")
    white_fill = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")
    
    # Severity Fills & Fonts
    s1_fill = PatternFill(start_color="FCE8E6", end_color="FCE8E6", fill_type="solid")
    s1_font = Font(name=font_family, size=10, bold=True, color="C5221F")
    
    s2_fill = PatternFill(start_color="FEF3D6", end_color="FEF3D6", fill_type="solid")
    s2_font = Font(name=font_family, size=10, bold=True, color="B06000")
    
    s3_fill = PatternFill(start_color="FEF7E0", end_color="FEF7E0", fill_type="solid")
    s3_font = Font(name=font_family, size=10, bold=True, color="7A5800")
    
    s4_fill = PatternFill(start_color="F1F3F4", end_color="F1F3F4", fill_type="solid")
    s4_font = Font(name=font_family, size=10, color="5F6368")

    # Priority Fonts
    p1_font = Font(name=font_family, size=10, bold=True, color="B31B1B")
    p2_font = Font(name=font_family, size=10, bold=True, color="D97706")
    p3_font = Font(name=font_family, size=10, color="2563EB")
    
    # Text Fonts
    title_font = Font(name=font_family, size=16, bold=True, color="1F4E79")
    subtitle_font = Font(name=font_family, size=10, italic=True, color="4B5563")
    header_font = Font(name=font_family, size=10, bold=True, color="FFFFFF")
    section_banner_font = Font(name=font_family, size=11, bold=True, color="FFFFFF")
    kpi_label_font = Font(name=font_family, size=9, bold=True, color="4B5563")
    data_font = Font(name=font_family, size=10, color="111827")
    data_font_bold = Font(name=font_family, size=10, bold=True, color="111827")
    code_font = Font(name="Consolas", size=9, color="1E3A8A")
    link_font = Font(name=font_family, size=10, underline="single", color="1D4ED8")
    
    # Borders
    thin_border_side = Side(style='thin', color='D1D5DB')
    thin_border = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)

    # Alignments
    center_align = Alignment(horizontal='center', vertical='center')
    left_align = Alignment(horizontal='left', vertical='center')
    left_top_wrap = Alignment(horizontal='left', vertical='top', wrap_text=True)
    center_top = Alignment(horizontal='center', vertical='top')

    # =============================================================
    # SHEET 1: EXECUTIVE SUMMARY & TRIAGE
    # =============================================================
    ws1 = wb.active
    ws1.title = "Executive Summary & Triage"
    ws1.views.sheetView[0].showGridLines = True
    
    # Title Block
    ws1.merge_cells("A1:I1")
    ws1["A1"] = "EDUFAMS PLATFORM DEFECT AUDIT REPORT (PRE-DEMO)"
    ws1["A1"].font = title_font
    ws1["A1"].alignment = Alignment(horizontal='left', vertical='center')
    ws1.row_dimensions[1].height = 28

    ws1.merge_cells("A2:I2")
    ws1["A2"] = "Environment: Localhost Integration (:5173 Admin / :5174 Parent) | Scope: R3, R4 FAS, R9 Parent Portal | Date: October 23, 2026"
    ws1["A2"].font = subtitle_font
    ws1["A2"].alignment = Alignment(horizontal='left', vertical='center')
    ws1.row_dimensions[2].height = 18

    # KPI Summary Cards Block (Row 4-5)
    kpis = [
        ("TOTAL DEFECTS", "8", "A", "B", "1F4E79"),
        ("S1 BLOCKERS", "1", "C", "D", "C5221F"),
        ("S2 MAJOR", "3", "E", "F", "B06000"),
        ("S3 MODERATE", "3", "G", "H", "7A5800"),
        ("S4 MINOR", "1", "I", "I", "5F6368")
    ]
    
    ws1.row_dimensions[4].height = 16
    ws1.row_dimensions[5].height = 28

    for label, count, start_col, end_col, color in kpis:
        cell_range_label = f"{start_col}4:{end_col}4"
        cell_range_num = f"{start_col}5:{end_col}5"
        if start_col != end_col:
            ws1.merge_cells(cell_range_label)
            ws1.merge_cells(cell_range_num)
        
        top_cell = ws1[f"{start_col}4"]
        top_cell.value = label
        top_cell.font = kpi_label_font
        top_cell.fill = subtle_gray_fill
        top_cell.alignment = center_align

        num_cell = ws1[f"{start_col}5"]
        num_cell.value = count
        num_cell.font = Font(name=font_family, size=18, bold=True, color=color)
        num_cell.fill = subtle_gray_fill
        num_cell.alignment = center_align
        
        cols_to_border = [start_col] if start_col == end_col else [start_col, end_col]
        for c in cols_to_border:
            ws1[f"{c}4"].border = thin_border
            ws1[f"{c}5"].border = thin_border

    # Table Header (Row 7)
    headers_ws1 = [
        "Bug ID", "Severity", "Priority", "Status", "Module / Area",
        "Defect Summary", "Assigned Team", "Client Demo Risk", "Target Sprint"
    ]
    
    ws1.row_dimensions[7].height = 26
    for col_idx, h in enumerate(headers_ws1, start=1):
        cell = ws1.cell(row=7, column=col_idx, value=h)
        cell.font = header_font
        cell.fill = navy_fill
        cell.alignment = center_align
        cell.border = thin_border

    triage_data = [
        ("BUG-EDUFAMS-001", "S1 - Blocker", "P1 - High", "OPEN", "Admin / MOEFAS", 
         "GET /api/fas/v1/fas/moe-schemes returns HTTP 404, triggering red 'Unable to load data' banner", 
         "Backend (FasService)", "FATAL - Broken API on click", "Sprint 1 Hotfix"),
        ("BUG-EDUFAMS-002", "S2 - Major", "P2 - High", "OPEN", "Admin / Navigation", 
         "Sidebar exposes unbuilt scaffold placeholder pages (/top-up, /fas) & 'Fanancial' header typo", 
         "Frontend (admin-portal)", "HIGH - Exposes unfinished work", "Sprint 1 Hotfix"),
        ("BUG-EDUFAMS-003", "S2 - Major", "P2 - Medium", "OPEN", "Admin / RBAC Guard", 
         "MOE HQ role accessing /class-management redirected to empty dashboard with 'Access restricted'", 
         "Frontend (Router Guard)", "MEDIUM - Confusing role boundary", "Sprint 2"),
        ("BUG-EDUFAMS-004", "S3 - Moderate", "P2 - Medium", "OPEN", "Admin / Fee Batches", 
         "Raw GUIDs (ffff0001-...) rendered in Fee Component & Created By columns instead of names", 
         "Frontend & API Loader", "HIGH - Unprofessional UI appearance", "Sprint 1 Hotfix"),
        ("BUG-EDUFAMS-005", "S3 - Moderate", "P3 - Low", "OPEN", "Admin / Students", 
         "Newly enrolled students render raw database UUID string instead of standardized format (STU-xxx)", 
         "Backend (StudentSchoolService)", "MEDIUM - Visual inconsistency", "Sprint 2"),
        ("BUG-EDUFAMS-006", "S3 - Moderate", "P3 - Low", "OPEN", "Database / Seed Data", 
         "Corrupted test mock student ('Trần Tuấn Kiệt', Age 25 in Primary 2, Class 111111) persisted in Rosyth", 
         "Database Admin / Seeder", "HIGH - Embarrassing test artifact", "Sprint 1 Hotfix"),
        ("BUG-EDUFAMS-007", "S4 - Minor", "P3 - Low", "OPEN", "Parent Portal / E-Service", 
         "Child profile card displays truncated label 'EDU-00172 · Age Active' (missing numerical age value)", 
         "Frontend (parent-portal)", "LOW - Minor visual glitch", "Sprint 2"),
        ("BUG-EDUFAMS-008", "S2 - Major", "P2 - High", "OPEN", "FAS End-to-End Workflow", 
         "Workflow disconnect: Parents submit FAS application via Portal, but Admin Portal has zero review UI", 
         "Product Owner / Fullstack", "HIGH - Disconnected core user story", "Sprint 2")
    ]

    for row_idx, row_data in enumerate(triage_data, start=8):
        ws1.row_dimensions[row_idx].height = 24
        bg_fill = zebra_fill if row_idx % 2 == 0 else white_fill
        
        for col_idx, val in enumerate(row_data, start=1):
            cell = ws1.cell(row=row_idx, column=col_idx, value=val)
            cell.font = data_font
            cell.fill = bg_fill
            cell.border = thin_border
            cell.alignment = left_align
            
            if col_idx == 1:
                cell.font = code_font
                cell.alignment = center_align
            elif col_idx == 2:
                cell.alignment = center_align
                if "S1" in val: cell.fill, cell.font = s1_fill, s1_font
                elif "S2" in val: cell.fill, cell.font = s2_fill, s2_font
                elif "S3" in val: cell.fill, cell.font = s3_fill, s3_font
                elif "S4" in val: cell.fill, cell.font = s4_fill, s4_font
            elif col_idx == 3:
                cell.alignment = center_align
                if "P1" in val: cell.font = p1_font
                elif "P2" in val: cell.font = p2_font
                elif "P3" in val: cell.font = p3_font
            elif col_idx == 4:
                cell.alignment = center_align
                cell.font = data_font_bold
            elif col_idx == 8:
                if "FATAL" in val: cell.font = s1_font
                elif "HIGH" in val: cell.font = s2_font

    ws1.freeze_panes = "A8"
    ws1.auto_filter.ref = f"A7:I{7 + len(triage_data)}"

    col_widths_ws1 = {1: 18, 2: 15, 3: 13, 4: 12, 5: 22, 6: 48, 7: 24, 8: 30, 9: 15}
    for col_idx, width in col_widths_ws1.items():
        ws1.column_dimensions[get_column_letter(col_idx)].width = width


    # =============================================================
    # SHEET 2: DETAILED DEFECT SPECIFICATIONS (JIRA-READY)
    # =============================================================
    ws2 = wb.create_sheet(title="Defect Details (Full Spec)")
    ws2.views.sheetView[0].showGridLines = True
    
    headers_ws2 = [
        "Bug ID", "Summary / Title", "Severity", "Priority", "Status",
        "Component", "Affected URL / Endpoint", "Persona",
        "Steps to Reproduce", "Expected Behavior", "Actual Behavior",
        "Console / Network Evidence", "Screenshot Evidence Path",
        "Suggested Remediation / Technical Fix", "Demo Workaround Strategy"
    ]

    ws2.row_dimensions[1].height = 28
    for col_idx, h in enumerate(headers_ws2, start=1):
        cell = ws2.cell(row=1, column=col_idx, value=h)
        cell.font = header_font
        cell.fill = navy_fill
        cell.alignment = center_align
        cell.border = thin_border

    detailed_defects = [
        (
            "BUG-EDUFAMS-001",
            "MOEFAS Scheme Management API Returns HTTP 404 & Displays Unhandled Error Banner",
            "S1 - Blocker", "P1 - High", "OPEN",
            "FasService / Admin Portal",
            "http://localhost:5173/moefas\nGET /api/fas/v1/fas/moe-schemes?PageNumber=1&PageSize=100",
            "MOE HQ Administrator (admin@IAM.edu.vn)",
            "1. Log in to Admin Portal as admin@IAM.edu.vn.\n2. In sidebar under FINANCIAL, click 'MOEFAS' (/moefas).\n3. Observe UI response and DevTools Network tab.",
            "Backend returns HTTP 200 OK with schemes list or clean empty state with 'New scheme' action button.",
            "Backend returns HTTP 404 Not Found. UI renders prominent red alert: 'Unable to load data: The MOEFAS schemes could not be loaded. Please try again.'",
            "Failed to load resource: the server responded with a status of 404 (Not Found) - /api/fas/v1/fas/moe-schemes",
            "docs/screenshots/defect_01_moefas_api_404_error.png",
            "1. Verify controller route [Route('api/fas/v1/fas/moe-schemes')] in FasService.\n2. Ensure Vite proxy forwards /api/fas requests to FasService container port.\n3. If unreleased, set visible: false in moefas manifest.ts.",
            "CRITICAL: Do NOT click on MOEFAS under the Financial menu during customer presentation."
        ),
        (
            "BUG-EDUFAMS-002",
            "Navigation Sidebar Exposes Unbuilt Scaffold Placeholder Pages (/top-up, /fas) & Typo on Main Dashboard",
            "S2 - Major", "P2 - High", "OPEN",
            "apps/admin-portal (Layout & i18n)",
            "http://localhost:5173/\nhttp://localhost:5173/top-up\nhttp://localhost:5173/fas",
            "All Admin Roles (MOE HQ & School User)",
            "1. Log in to Admin Portal.\n2. Read root dashboard header.\n3. Click 'EDUSAVE -> Top-up' in sidebar.\n4. Click 'FINANCIAL -> FAS' in sidebar.",
            "Dashboard renders production summary cards. Unreleased modules hidden behind feature flags until functional.",
            "1. Dashboard header has spelling error: 'Education Fanancial Account Management System'.\n2. Body reads: 'This feature is scaffolded and ready for its business workflow.'\n3. /top-up and /fas render blank scaffold cards.",
            "N/A (Static template defect)",
            "docs/screenshots/defect_02_topup_empty_scaffold.png",
            "1. Fix 'Fanancial' -> 'Financial' in locales/en-US/translation.json.\n2. In top-up and fas manifest.ts, set visible: false or disable menu navigation.",
            "Navigate directly to functional modules (School Management or Students) immediately after login. Avoid clicking Top-up or FAS."
        ),
        (
            "BUG-EDUFAMS-003",
            "MOE HQ Role Bounced with Red Error Toast Upon Accessing /class-management",
            "S2 - Major", "P2 - Medium", "OPEN",
            "apps/admin-portal/src/features/class-management",
            "http://localhost:5173/class-management",
            "MOE HQ Administrator (admin@IAM.edu.vn)",
            "1. Log in as MOE HQ Administrator.\n2. Navigate directly to /class-management (or via browser history/bookmark).",
            "Render clean 403 page or allow MOE HQ read-only access to view classes across schools.",
            "Router guard redirects user to root dashboard and flashes red toast: 'Access restricted: Your account does not have permission to view this area of the admin portal.'",
            "Manifest guard triggers route redirect to fallback.",
            "docs/screenshots/defect_03_moehq_access_restricted_class_mgmt.png",
            "Update allowedRoles: ['SCHOOL', 'MOEHQ'] in class-management/manifest.ts with read-only mode for MOE HQ (hide 'Create class' button), or provide clear role switcher.",
            "Always demonstrate class creation under the School Clerk persona (staff1@IAM.edu.vn)."
        ),
        (
            "BUG-EDUFAMS-004",
            "Raw Technical GUIDs Rendered in Fee Publication Batches Table and Details",
            "S3 - Moderate", "P2 - Medium", "OPEN",
            "apps/admin-portal/src/features/fee-publication",
            "http://localhost:5173/fee-batches\nhttp://localhost:5173/fee-batches/:id",
            "MOE HQ & School User",
            "1. Navigate to FINANCIAL -> Fee Batches.\n2. Observe Fee Component column.\n3. Click 'View details' on completed batch.\n4. Observe Fee Component and Created by fields.",
            "Display resolved business names: 'Standard Miscellaneous Fee (COMP_MISC_STD)' and 'System Administrator (admin@IAM.edu.vn)'.",
            "Table and details view display raw technical GUIDs: 'ffff0001-0000-0000-0000-000000000002' and '01A159A5-0F27-7718-82E1-695C2F4642AA'. Batch details also lacks student charge table.",
            "N/A (Presentation mapping defect)",
            "docs/screenshots/flow_12_f12_f15_fee_batch_completed_charges_generated.png",
            "Perform entity lookup/join against fee components and users state/cache in batch list/detail loader to display friendly names.",
            "Explain to clients that technical GUID tracking is active during microservice integration phase."
        ),
        (
            "BUG-EDUFAMS-005",
            "Newly Created Students Display Raw UUID String Instead of Standard ID Format (STU-xxx)",
            "S3 - Moderate", "P3 - Low", "OPEN",
            "StudentSchoolService / Student Management",
            "http://localhost:5173/student-management\nhttp://localhost:5173/students/:id",
            "School Clerk / MOE HQ",
            "1. Create a new student (e.g. Lucas Tan Wei Jie).\n2. View Student management table and student profile.",
            "Newly created student receives business identifier (e.g. STU-00005) matching existing format (STU-001, STU-003).",
            "Table and profile header display full internal database UUID: 'Lucas Tan Wei Jie f73e9aa4-0143-4826-9e48-93e184200d07'.",
            "N/A (Entity ID formatting defect)",
            "docs/screenshots/happycase_02_student_created_in_table.png",
            "Implement sequential student code generation ('STU-xxxxx') in StudentSchoolService on record persistence and bind this to UI display.",
            "Highlight student's name and enrollment status rather than zooming in on ID column."
        ),
        (
            "BUG-EDUFAMS-006",
            "Corrupted / Invalid Test Mock Data Persisted in Database (Age 25 in Primary 2)",
            "S3 - Moderate", "P3 - Low", "OPEN",
            "StudentSchoolDatabase.dbo.students",
            "http://localhost:5173/student-management",
            "School User (Rosyth Primary)",
            "1. Log in as staff1@IAM.edu.vn.\n2. Open Student management table for Rosyth Primary.\n3. Inspect bottom row.",
            "Mock database contains realistic primary school student profiles (Ages 6-12) with standard class codes.",
            "Table contains record: 'Trần Tuấn Kiệt' | DOB: May 18, 2001 (Age 25 in Primary school) | Class: '111111111111111111 · P2-X'.",
            "Database seed data contamination.",
            "docs/screenshots/defect_04_student_age25_mock_data.png",
            "1. Execute SQL script to purge record ce169581-8e09-4255-8377-131718749154.\n2. Add age-stage boundary constraint in StudentSchoolService preventing age > 14 in Primary.",
            "Avoid scrolling to the bottom row of student table during demo. Focus on Lucas Tan Wei Jie and Tan Jun Wei."
        ),
        (
            "BUG-EDUFAMS-007",
            "Parent Portal Child Profile Card Renders Truncated Age Label (EDU-00172 · Age Active)",
            "S4 - Minor", "P3 - Low", "OPEN",
            "apps/parent-portal (E-Service Dashboard)",
            "http://localhost:5174/",
            "Parent (S7890123F - NGUYEN VAN MINH)",
            "1. Log in to Parent Portal via SingPass Simulator as NGUYEN VAN MINH.\n2. Inspect child Education Account card header.",
            "Displays parsed numerical age: 'EDU-00172 · Age 11 · Active'.",
            "Displays literal truncated string 'EDU-00172 · Age Active' (numerical age omitted).",
            "N/A (React JSX template interpolation defect)",
            "docs/screenshots/defect_05_parent_portal_age_label.png",
            "Fix JSX string template interpolation in child account card component to compute age integer from date_of_birth.",
            "Minor cosmetic issue; can be passed over quickly without drawing attention."
        ),
        (
            "BUG-EDUFAMS-008",
            "End-to-End Workflow Disconnect: FAS Application Submitted by Parent Has No Review Queue in Admin Portal",
            "S2 - Major", "P2 - High", "OPEN",
            "FasService / Admin Portal & Parent Portal",
            "http://localhost:5174/fas/apply\nhttp://localhost:5173/fas",
            "Parent & School Clerk / MOE HQ",
            "1. Parent completes and submits FAS application on Parent Portal.\n2. School clerk or MOE admin attempts to locate incoming application in Admin Portal.",
            "Submitted applications populate an administrative inbox for verification and approval.",
            "Admin Portal /fas is a blank placeholder card and /moefas returns 404. Submitted applications cannot be reviewed or actioned via UI.",
            "API endpoint gap / Missing admin UI view for application triage.",
            "docs/screenshots/defect_06_fas_application_form_parent.png",
            "Implement FAS Application Review inbox in Admin Portal connected to FasService query API.",
            "Explain that intake form is functional on citizen portal and admin automated processing workflow is scheduled for Sprint 2."
        )
    ]

    for row_idx, row_data in enumerate(detailed_defects, start=2):
        ws2.row_dimensions[row_idx].height = 65
        bg_fill = zebra_fill if row_idx % 2 == 0 else white_fill
        
        for col_idx, val in enumerate(row_data, start=1):
            cell = ws2.cell(row=row_idx, column=col_idx, value=val)
            cell.font = data_font
            cell.fill = bg_fill
            cell.border = thin_border
            cell.alignment = left_top_wrap
            
            if col_idx == 1:
                cell.font = code_font
                cell.alignment = center_top
            elif col_idx == 3:
                cell.alignment = center_top
                if "S1" in val: cell.fill, cell.font = s1_fill, s1_font
                elif "S2" in val: cell.fill, cell.font = s2_fill, s2_font
                elif "S3" in val: cell.fill, cell.font = s3_fill, s3_font
                elif "S4" in val: cell.fill, cell.font = s4_fill, s4_font
            elif col_idx == 4:
                cell.alignment = center_top
                if "P1" in val: cell.font = p1_font
                elif "P2" in val: cell.font = p2_font
                elif "P3" in val: cell.font = p3_font
            elif col_idx == 5:
                cell.alignment = center_top
                cell.font = data_font_bold
            elif col_idx in (7, 12, 13):
                cell.font = code_font

    ws2.freeze_panes = "A2"
    ws2.auto_filter.ref = f"A1:O{1 + len(detailed_defects)}"

    col_widths_ws2 = {
        1: 18, 2: 32, 3: 15, 4: 12, 5: 12, 6: 22, 7: 32, 8: 24,
        9: 38, 10: 32, 11: 38, 12: 35, 13: 35, 14: 42, 15: 35
    }
    for col_idx, width in col_widths_ws2.items():
        ws2.column_dimensions[get_column_letter(col_idx)].width = width


    # =============================================================
    # SHEET 3: VISUAL DEFECT EVIDENCE GALLERY (EMBEDDED IMAGES)
    # =============================================================
    ws3 = wb.create_sheet(title="Visual Defect Gallery")
    ws3.views.sheetView[0].showGridLines = True
    
    # Title Block
    ws3.merge_cells("A1:G1")
    ws3["A1"] = "VISUAL DEFECT EVIDENCE GALLERY (REAL SCREENSHOTS)"
    ws3["A1"].font = title_font
    ws3["A1"].alignment = Alignment(horizontal='left', vertical='center')
    ws3.row_dimensions[1].height = 28

    ws3.merge_cells("A2:G2")
    ws3["A2"] = "Empirical visual evidence captured during automated bsk exploratory testing on localhost:5173 & localhost:5174"
    ws3["A2"].font = subtitle_font
    ws3["A2"].alignment = Alignment(horizontal='left', vertical='center')
    ws3.row_dimensions[2].height = 18

    # Set column widths for Sheet 3
    ws3.column_dimensions["A"].width = 6
    ws3.column_dimensions["B"].width = 24
    ws3.column_dimensions["C"].width = 30
    ws3.column_dimensions["D"].width = 30
    ws3.column_dimensions["E"].width = 25
    ws3.column_dimensions["F"].width = 25
    ws3.column_dimensions["G"].width = 15

    # Gallery Cards Data
    gallery_items = [
        {
            "id": "BUG-EDUFAMS-001",
            "title": "MOEFAS Scheme Management API Returns HTTP 404 & Displays Unhandled Error Banner",
            "severity": "S1 - Blocker",
            "priority": "P1 - High",
            "component": "FasService / Admin Portal (/moefas)",
            "key_flaw": "API GET /api/fas/v1/fas/moe-schemes fails with HTTP 404; renders prominent red error alert banner.",
            "image_path": "docs/screenshots/defect_01_moefas_api_404_error.png"
        },
        {
            "id": "BUG-EDUFAMS-002",
            "title": "Navigation Sidebar Exposes Unbuilt Scaffold Placeholders (/top-up, /fas) & Typo on Main Dashboard",
            "severity": "S2 - Major",
            "priority": "P2 - High",
            "component": "apps/admin-portal (Layout & i18n)",
            "key_flaw": "Header misspells 'Fanancial' and body says 'This feature is scaffolded...'. Both /top-up and /fas show blank placeholder cards.",
            "image_path": "docs/screenshots/defect_02_topup_empty_scaffold.png"
        },
        {
            "id": "BUG-EDUFAMS-003",
            "title": "MOE HQ Role Bounced with Red Error Toast Upon Accessing /class-management",
            "severity": "S2 - Major",
            "priority": "P2 - Medium",
            "component": "apps/admin-portal/src/features/class-management",
            "key_flaw": "Router guard bounces MOE HQ to root dashboard with red toast 'Access restricted'.",
            "image_path": "docs/screenshots/defect_03_moehq_access_restricted_class_mgmt.png"
        },
        {
            "id": "BUG-EDUFAMS-004",
            "title": "Raw Technical GUIDs Rendered in Fee Publication Batches Table and Details",
            "severity": "S3 - Moderate",
            "priority": "P2 - Medium",
            "component": "apps/admin-portal/src/features/fee-publication",
            "key_flaw": "Raw GUIDs ffff0001-... and 01A159A5-... rendered instead of fee component and user names.",
            "image_path": "docs/screenshots/flow_12_f12_f15_fee_batch_completed_charges_generated.png"
        },
        {
            "id": "BUG-EDUFAMS-005",
            "title": "Newly Created Students Display Raw UUID String Instead of Standard ID Format (STU-xxx)",
            "severity": "S3 - Moderate",
            "priority": "P3 - Low",
            "component": "StudentSchoolService / Student Management",
            "key_flaw": "New student Lucas Tan Wei Jie displays raw DB UUID f73e9aa4-0143-4826-9e48-93e184200d07 instead of STU-xxxxx.",
            "image_path": "docs/screenshots/happycase_02_student_created_in_table.png"
        },
        {
            "id": "BUG-EDUFAMS-006",
            "title": "Corrupted / Invalid Test Mock Data Persisted in Database (Age 25 in Primary 2)",
            "severity": "S3 - Moderate",
            "priority": "P3 - Low",
            "component": "StudentSchoolDatabase.dbo.students",
            "key_flaw": "Row 4 contains student 'Trần Tuấn Kiệt' born in 2001 (Age 25) enrolled in Primary 2 with corrupted class code '111111111111111111 · P2-X'.",
            "image_path": "docs/screenshots/defect_04_student_age25_mock_data.png"
        },
        {
            "id": "BUG-EDUFAMS-007",
            "title": "Parent Portal Child Profile Card Renders Truncated Age Label (EDU-00172 · Age Active)",
            "severity": "S4 - Minor",
            "priority": "P3 - Low",
            "component": "apps/parent-portal (E-Service Dashboard)",
            "key_flaw": "Child Education Account card literally displays 'EDU-00172 · Age Active' missing calculated numerical age integer.",
            "image_path": "docs/screenshots/defect_05_parent_portal_age_label.png"
        },
        {
            "id": "BUG-EDUFAMS-008",
            "title": "End-to-End Workflow Disconnect: FAS Application Submitted by Parent Has No Review Queue in Admin Portal",
            "severity": "S2 - Major",
            "priority": "P2 - High",
            "component": "FasService / Admin Portal & Parent Portal",
            "key_flaw": "Parent Portal has complete intake form (/fas/apply), but Admin Portal /fas is a blank scaffold and /moefas is 404.",
            "image_path": "docs/screenshots/defect_06_fas_application_form_parent.png"
        }
    ]

    current_row = 4
    
    for item in gallery_items:
        # Card Header Banner
        banner_cell = f"B{current_row}"
        banner_range = f"B{current_row}:G{current_row}"
        ws3.merge_cells(banner_range)
        header_text = f"[{item['id']}] {item['title']}"
        ws3[banner_cell] = header_text
        ws3[banner_cell].font = section_banner_font
        ws3[banner_cell].fill = dark_slate_fill
        ws3[banner_cell].alignment = Alignment(horizontal='left', vertical='center', indent=1)
        ws3.row_dimensions[current_row].height = 24
        current_row += 1

        # Metadata Row
        meta_cell_1 = f"B{current_row}"
        ws3[meta_cell_1] = f"Severity: {item['severity']}   |   Priority: {item['priority']}   |   Component: {item['component']}"
        ws3[meta_cell_1].font = Font(name=font_family, size=9, bold=True, color="374151")
        ws3[meta_cell_1].fill = subtle_gray_fill
        ws3.merge_cells(f"B{current_row}:G{current_row}")
        ws3.row_dimensions[current_row].height = 18
        current_row += 1

        # Key Defect Callout Row
        flaw_cell = f"B{current_row}"
        ws3[flaw_cell] = f"Defect Observation: {item['key_flaw']}"
        ws3[flaw_cell].font = Font(name=font_family, size=9, italic=True, color="B91C1C")
        ws3[flaw_cell].fill = white_fill
        ws3.merge_cells(f"B{current_row}:G{current_row}")
        ws3.row_dimensions[current_row].height = 20
        current_row += 1

        # Insert Image if file exists
        img_path = item["image_path"]
        if os.path.exists(img_path):
            with PILImage.open(img_path) as pil_img:
                orig_w, orig_h = pil_img.size
            
            # Target display width: 620px
            target_w = 620
            target_h = int(orig_h * (target_w / orig_w))

            excel_img = OpenpyxlImage(img_path)
            excel_img.width = target_w
            excel_img.height = target_h
            
            anchor_cell = f"B{current_row}"
            ws3.add_image(excel_img, anchor_cell)

            # Approximate row heights (1 point ~ 1.33 pixels)
            # Allocate rows for image height
            rows_needed = int(target_h / 20) + 1
            for r in range(current_row, current_row + rows_needed):
                ws3.row_dimensions[r].height = 20
            current_row += rows_needed + 2
        else:
            ws3[f"B{current_row}"] = f"[Screenshot file not found: {img_path}]"
            ws3.row_dimensions[current_row].height = 24
            current_row += 2

    # Save complete workbook
    wb.save(output_path)
    print(f"Successfully generated Excel with embedded images: {output_path}")

if __name__ == "__main__":
    create_defect_excel_with_images("docs/BUG_REPORT_R3_EDUFAMS_PRE_DEMO.xlsx")
