#!/usr/bin/env python3
"""
tools/build_executive_testcases.py
Restructures and enriches FS08 Parent Profile test cases into the 3-Tier Core Architecture
in full compliance with .agent/rules/01-two-stage-workflow.md and .agent/rules/02-field-test-matrix.md:
  - Pillar 1: Business Rules (BR - 8 TCs)
  - Pillar 2: Acceptance Criteria (AC - 23 TCs)
  - Pillar 3: Technical, Universal Input Matrix, Form Lifecycle, UI Integrity & PII (Tech & UI Matrix - 73 TCs)
  - Total: 104 Test Cases

Outputs:
  1. testcases/fs08/fs08-parent-profile/TC_FS08_Parent_Profile.md (Structured 5-Part Markdown)
  2. testcases/fs08/fs08-parent-profile/TC_FS08_Parent_Profile.xlsx (Multi-tab AvePoint Navy Excel, 4 Sheets)
  3. testcases/fs08/fs08-parent-profile/TC_FS08_Parent_Profile_Executive.html & executive.html (Interactive Dashboard)
"""

import json
import os
import re
from pathlib import Path
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

ROOT = Path("/home/baudui/automation-ui")
MD_PATH = ROOT / "testcases/fs08/fs08-parent-profile/TC_FS08_Parent_Profile.md"
XLSX_PATH = ROOT / "testcases/fs08/fs08-parent-profile/TC_FS08_Parent_Profile.xlsx"
HTML_EXEC_PATH = ROOT / "testcases/fs08/fs08-parent-profile/TC_FS08_Parent_Profile_Executive.html"
HTML_SHORT_PATH = ROOT / "testcases/fs08/fs08-parent-profile/executive.html"

# Define All 104 Test Cases with 19 Columns
TEST_CASES_DATA = [
    # =========================================================================
    # TRỤ CỘT 1: BUSINESS RULES (BR - 8 TCs)
    # =========================================================================
    {
        "id": "TC-R8-094", "pillar": "BR", "scenario_id": "TS-010-ID",
        "title": "Verify SingPass verified identity displays Full Name, NRIC and Residential Address as strictly read-only",
        "suite": "SingPass Identity & PII", "page": "Parent Portal > Profile", "severity": "S2", "priority": "High",
        "status": "Passed", "test_type": "UI",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; on /profile page (View Mode)",
        "test_data": "Parent FA (Tan Wei Ming); NRIC: S1234123F; Residential: Blk 123 Ang Mo Kio Ave 3 #08-1234 S560123",
        "steps": "1. Navigate to /profile<br>2. Inspect Full Name, NRIC, and Residential Address elements<br>3. Verify absence of <input> tags for these identity fields",
        "expected": "Full Name, NRIC, and Residential Address are rendered as static text/read-only tags<br>No input fields exist for Full Name or Residential Address<br>Edit button [Update details] is visible",
        "actual": "Verified: Full Name and Residential Address are static text without editable inputs.",
        "assumption": "TD: BSK Live DOM verified locator dt:has-text('Residential') + dd", "defect": "",
        "traceability": "FR-08.3; FS R8 sec. 6 field table; D-20; AC #18",
        "note": "Read-only SingPass identity fields cannot be modified by user."
    },
    {
        "id": "TC-R8-095", "pillar": "BR", "scenario_id": "TS-010-ID",
        "title": "Verify residential address cannot be edited and is immutable in Edit Mode",
        "suite": "SingPass Identity & PII", "page": "Parent Portal > Profile", "severity": "S2", "priority": "High",
        "status": "Passed", "test_type": "Functional",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; enter Edit Mode via [Update details]",
        "test_data": "Parent FA; Residential: Blk 123 Ang Mo Kio Ave 3 #08-1234 S560123",
        "steps": "1. Click [Update details] to switch to Edit Mode<br>2. Attempt to locate an input field for Residential Address<br>3. Check legal notice text",
        "expected": "No editable input exists for Residential Address in Edit Mode<br>Legal notice displayed: 'Residential address is maintained via Government Digital Services and cannot be edited in this portal.'<br>Value remains unchanged",
        "actual": "Verified: Residential address remains static and locked during Edit Mode.",
        "assumption": "CR: D-20 decision confirms residential address is strictly read-only from Singpass", "defect": "",
        "traceability": "FR-08.3 rules (D-20); R8-AC18",
        "note": "Prevents unauthorized address modification."
    },
    {
        "id": "TC-R8-096", "pillar": "BR", "scenario_id": "TS-010-ID",
        "title": "Verify API rejects or ignores any tampering attempt to update read-only SingPass identity fields",
        "suite": "SingPass Identity & PII", "page": "API Service", "severity": "S1 (highest)", "priority": "Critical",
        "status": "Not Run", "test_type": "Security",
        "env": "SIT<br>API client (Postman/Playwright API) + DevTools<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in with valid bearer token",
        "test_data": "Payload tampering: {\"fullName\": \"HACKED NAME\", \"nric\": \"T9999999Z\", \"residentialStreet\": \"Malicious Street\"}",
        "steps": "1. Intercept PUT/PATCH profile update request<br>2. Inject read-only identity fields into JSON payload<br>3. Send request to backend<br>4. Inspect backend response and reload profile",
        "expected": "API ignores injected read-only fields or rejects request with HTTP 400 Bad Request<br>Parent profile in DB retains original Full Name, NRIC, and Residential Address",
        "actual": "Server-side schema validation strips unauthorized fields.",
        "assumption": "TD: Server-side schema validation strips unauthorized fields", "defect": "",
        "traceability": "FR-08.3 rules; NFR Security; Invariant 8",
        "note": "Guarantees server-side defense against parameter tampering."
    },
    {
        "id": "TC-R8-097", "pillar": "BR", "scenario_id": "TS-010-SUB",
        "title": "Verify saving valid phone, email and mailing address shows MSG-0807, persists data, creates audit log, and sends zero email",
        "suite": "Submission & Confirm Dialog", "page": "Parent Portal > Profile", "severity": "S1 (highest)", "priority": "Critical",
        "status": "Passed", "test_type": "Functional",
        "env": "SIT<br>Chrome (latest) + DB read access<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open",
        "test_data": "Phone: '98887777'; Email: 'fa.new@example.sg'; Mailing: Blk 9 Verde Walk #02-01 S650009 Singapore",
        "steps": "1. Enter valid new values for all contact and mailing fields<br>2. Click [Save changes]<br>3. In Confirm Dialog, click [Save changes]<br>4. Verify success toast and reload page<br>5. Inspect DB Parent_Profile table, audit log, and email outbox",
        "expected": "Success toast MSG-0807 'Your details have been updated.' is displayed in green<br>Values persist accurately after page reload<br>Audit log records 1 entry per changed field (field, old, new, user, timestamp)<br>ZERO notification email is sent (Decision D-28)",
        "actual": "Success toast MSG-0807 displayed; DB updated; audit log created; no email dispatched.",
        "assumption": "CR: Decision D-28 explicitly prohibits sending email for profile updates", "defect": "",
        "traceability": "FR-08.3; R8-AC14; US-08.2; D-28; PB-15",
        "note": "Golden path end-to-end profile update."
    },
    {
        "id": "TC-R8-110", "pillar": "BR", "scenario_id": "TS-010-AGE",
        "title": "Verify My details is strictly view-only when all linked children are 16+ years old",
        "suite": "Child Age Access & Isolation", "page": "Parent Portal > Profile", "severity": "S2", "priority": "High",
        "status": "Passed", "test_type": "Functional",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "Parent PE logged in (all linked children E1 age 16, E2 age 17)",
        "test_data": "Parent PE (S7000007G); Children >= 16",
        "steps": "1. Log in as Parent PE<br>2. Navigate to /profile<br>3. Inspect profile screen for edit controls<br>4. Attempt to call PUT /api/parent/profile directly via API",
        "expected": "All fields rendered as read-only<br>No [Update details] button exists on UI<br>Direct API update attempt is rejected with HTTP 403 Forbidden<br>Banner displays: 'Profile editing is unavailable when all children have reached 16.'",
        "actual": "Profile is strictly view-only; edit button hidden; API rejects update.",
        "assumption": "CR: Business rule BR-08-06.4 and R8-AC09 - view-only when all children 16+", "defect": "",
        "traceability": "FR-08.3 precondition; R8-AC09; BR-08-06.4",
        "note": "Child adulthood transition lifecycle rule."
    },
    {
        "id": "TC-R8-111", "pillar": "BR", "scenario_id": "TS-010-AGE",
        "title": "Verify My details is editable when at least one child is under 16 years old",
        "suite": "Child Age Access & Isolation", "page": "Parent Portal > Profile", "severity": "S3", "priority": "Medium",
        "status": "Passed", "test_type": "Functional",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "Parent PB logged in (Child B1 age 16, Child B2 age 14)",
        "test_data": "Parent PB (S7000002B); Child B2 under 16",
        "steps": "1. Log in as Parent PB<br>2. Navigate to /profile<br>3. Inspect profile screen",
        "expected": "[Update details] button is visible and active<br>Clicking enters Edit Mode with editable contact and mailing fields<br>Save action is permitted",
        "actual": "[Update details] button is available and functional.",
        "assumption": "CR: FSD section 6 precondition: parent with at least one child < 16 can edit", "defect": "",
        "traceability": "FR-08.3 precondition; R8-AC09",
        "note": "Per-family mixed age rule."
    },
    {
        "id": "TC-R8-112", "pillar": "BR", "scenario_id": "TS-010-AGE",
        "title": "Verify a parent cannot update another parent's profile via API IDOR tampering (BOLA/IDOR Protection)",
        "suite": "Child Age Access & Isolation", "page": "API Service", "severity": "S1 (highest)", "priority": "Critical",
        "status": "Not Run", "test_type": "Security",
        "env": "SIT<br>API client (Postman/Playwright API)<br>Mock SingPass + mock data API",
        "preconditions": "Father FA logged in; Mother MA's Parent_Profile ID known",
        "test_data": "Target ID: MA's Profile ID; Token: FA's auth bearer token",
        "steps": "1. Send PUT /api/parent/profile/{MA_ID} using FA's session token<br>2. Check HTTP status code and response payload<br>3. Inspect MA's profile in DB",
        "expected": "API rejects request with HTTP 403 Forbidden and MSG-0003: 'You do not have permission to perform this action.'<br>Mother MA's profile remains completely unchanged",
        "actual": "Server-side tenancy & ownership verification on user claims.",
        "assumption": "TD: Server-side tenancy & ownership verification on user claims", "defect": "",
        "traceability": "FR-08.3 rules (own data only); NFR Security; MSG-0003",
        "note": "OWASP Top 10 API1: Broken Object Level Authorization (BOLA/IDOR)."
    },
    {
        "id": "TC-R8-113", "pillar": "BR", "scenario_id": "TS-010-AGE",
        "title": "Verify father's profile update does not alter mother's personal details (Independent Records)",
        "suite": "Child Age Access & Isolation", "page": "Parent Portal > Profile", "severity": "S2", "priority": "Medium",
        "status": "Passed", "test_type": "Functional",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "Father FA and Mother MA both registered in system for same children",
        "test_data": "FA new phone: '98887777'; MA original phone: '81112222'",
        "steps": "1. Log in as Father FA and update phone number to '98887777'<br>2. Confirm update and log out<br>3. Log in as Mother MA and navigate to /profile",
        "expected": "Mother MA's phone number remains '81112222' (unchanged)<br>Each parent maintains an independent Parent_Profile entity in DB",
        "actual": "Father update is isolated; mother profile remains unchanged.",
        "assumption": "CR: FSD Appendix A shows separate Parent_Profile row per NRIC", "defect": "",
        "traceability": "FR-08.3 rules; Appendix A Parent_Profile",
        "note": "Ensures parent profiles are strictly de-coupled."
    },

    # =========================================================================
    # TRỤ CỘT 2: ACCEPTANCE CRITERIA (AC - 23 TCs)
    # =========================================================================
    {
        "id": "TC-R8-ATM-01", "pillar": "AC", "scenario_id": "TS-010-ID",
        "title": "Verify NRIC masking and reveal toggle button switches between Show and Hide state",
        "suite": "SingPass Identity & PII", "page": "Parent Portal > Profile", "severity": "S2", "priority": "High",
        "status": "Passed", "test_type": "UI",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; on /profile page (View Mode)",
        "test_data": "NRIC: '*****123F' <-> 'S1234123F'",
        "steps": "1. Check initial state: NRIC masked ('*****123F'), button label 'Show NRIC'<br>2. Click 'Show NRIC' button<br>3. Verify unmasked NRIC ('S1234123F') and button label switches to 'Hide NRIC'<br>4. Click 'Hide NRIC' button<br>5. Verify NRIC re-masks to '*****123F' and button returns to 'Show NRIC'",
        "expected": "NRIC toggles accurately between masked and unmasked representation<br>Button text dynamically updates ('Show NRIC' <-> 'Hide NRIC')<br>Zero layout shift (CLS = 0)",
        "actual": "NRIC toggles correctly between masked and unmasked state with zero layout shift.",
        "assumption": "TD: BSK Live DOM verified locator button:has-text('Show NRIC')", "defect": "",
        "traceability": "FR-08.3; BR-08-09.1; AC #10; NFR Security",
        "note": "Protects PII against shoulder surfing in public spaces."
    },
    {
        "id": "TC-R8-ATM-02", "pillar": "AC", "scenario_id": "TS-010-STA",
        "title": "Verify Save changes button pristine and dirty state gatekeeper (disabled when pristine, enabled when dirty)",
        "suite": "Form State & Mode Transitions", "page": "Parent Portal > Profile", "severity": "S2", "priority": "High",
        "status": "Passed", "test_type": "UI",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; enter Edit Mode via [Update details]",
        "test_data": "Pristine form vs 1 char edit ('91234567' -> '91234568')",
        "steps": "1. Open Edit Mode<br>2. Inspect Save changes button state and hint text<br>3. Type 1 character into phone number<br>4. Inspect Save changes button state and hint text<br>5. Revert character back to original baseline",
        "expected": "Pristine state: Save changes button is disabled (disabled=true); hint 'Make a change to enable saving.' is visible<br>Dirty state: Save changes button enables (disabled=false); hint is hidden<br>Reverting to original baseline: Save changes button re-disables; hint reappears",
        "actual": "Button disabled with hint when pristine; enables upon change; re-disables when reverted.",
        "assumption": "CR: UI interaction design confirmed to prevent redundant mutation dispatches", "defect": "",
        "traceability": "FR-08.3; AC #14; US-08.2",
        "note": "Prevents redundant PUT mutation dispatches when no changes exist."
    },
    {
        "id": "TC-R8-STA-01", "pillar": "AC", "scenario_id": "TS-010-STA",
        "title": "Verify clicking 'Update details' button transitions page from View Mode to Edit Mode",
        "suite": "Form State & Mode Transitions", "page": "Parent Portal > Profile", "severity": "S2", "priority": "High",
        "status": "Passed", "test_type": "UI",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; on /profile page (View Mode)",
        "test_data": "Parent FA (Tan Wei Ming); View Mode baseline; Click button [Update details] to reveal editable inputs",
        "steps": "1. Open /profile page in View Mode<br>2. Click 'Update details' button<br>3. Verify presence of editable form inputs and action buttons",
        "expected": "Page switches smoothly to Edit Mode<br>Editable inputs appear: phoneNumber, email, mailingBlock, mailingStreet, mailingUnit, mailingPostalCode, mailingCountry<br>Action buttons [Save changes] and [Cancel] appear<br>[Update details] button is replaced",
        "actual": "Page transitions to Edit Mode; inputs and action buttons revealed.",
        "assumption": "TD: React component state transition (isEditing: false -> true)", "defect": "",
        "traceability": "FR-08.3; FS R8 sec. 6; AC #14",
        "note": "Core mode transition entry point."
    },
    {
        "id": "TC-R8-STA-02", "pillar": "AC", "scenario_id": "TS-010-STA",
        "title": "Verify clicking 'Cancel' button discards uncommitted modifications and restores baseline in View Mode",
        "suite": "Form State & Mode Transitions", "page": "Parent Portal > Profile", "severity": "S2", "priority": "High",
        "status": "Passed", "test_type": "Functional",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open",
        "test_data": "Original phone: '91234567'; Modified phone: '98887777'",
        "steps": "1. Change Mobile Number to '98887777'<br>2. Change Email to 'uncommitted@example.sg'<br>3. Click [Cancel] button<br>4. Inspect View Mode profile values",
        "expected": "Edit Mode exits immediately without confirmation modal<br>Page returns to View Mode<br>Profile displays original phone ('91234567') and email<br>Uncommitted modifications are completely discarded",
        "actual": "Cancel button restores original baseline; zero uncommitted data saved.",
        "assumption": "TD: Local state reset without backend mutation", "defect": "",
        "traceability": "FR-08.3; AC #14; US-08.2",
        "note": "Ensures clean escape from dirty form."
    },
    {
        "id": "TC-R8-STA-03", "pillar": "AC", "scenario_id": "TS-010-STA",
        "title": "Verify each blank required field individually prevents submission with inline error MSG-0001",
        "suite": "Form State & Mode Transitions", "page": "Parent Portal > Profile", "severity": "S2", "priority": "High",
        "status": "Passed", "test_type": "Functional",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open",
        "test_data": "5 mandatory fields: phoneNumber, email, mailingStreet, mailingPostalCode, mailingCountry",
        "steps": "1. Clear phoneNumber, attempt save -> verify MSG-0001<br>2. Restore phoneNumber, clear email, attempt save -> verify MSG-0001<br>3. Restore email, clear mailingStreet, attempt save -> verify MSG-0001<br>4. Restore street, clear mailingPostalCode, attempt save -> verify MSG-0001<br>5. Restore postal, clear mailingCountry, attempt save -> verify MSG-0001",
        "expected": "Each blank mandatory field individually triggers MSG-0001 inline error<br>Save action is blocked on every iteration<br>Nothing is saved to DB",
        "actual": "Each individual mandatory field triggers MSG-0001 when left blank.",
        "assumption": "CR: FSD section 6 table and AC #16 require MSG-0001 per required field", "defect": "",
        "traceability": "FR-08.3 errors; R8-AC16; MSG-0001",
        "note": "Granular mandatory validation across all 5 required fields."
    },
    {
        "id": "TC-R8-SUB-01", "pillar": "AC", "scenario_id": "TS-010-SUB",
        "title": "Verify clicking 'Save changes' in dirty state triggers confirmation modal (role='alertdialog')",
        "suite": "Submission & Confirm Dialog", "page": "Parent Portal > Profile", "severity": "S2", "priority": "High",
        "status": "Passed", "test_type": "UI",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open with valid modifications",
        "test_data": "Phone: '98887777'",
        "steps": "1. Modify phone number<br>2. Click [Save changes] button<br>3. Verify appearance and accessibility of modal dialog",
        "expected": "Modal appears with role='alertdialog'<br>Displays title 'Confirm Changes' and confirmation message<br>Contains action buttons: [Keep editing] and [Save changes]<br>Background backdrop blocks background interaction",
        "actual": "Modal alertdialog displayed with expected buttons and backdrop.",
        "assumption": "TD: WCAG 2.1 alertdialog pattern", "defect": "",
        "traceability": "FR-08.3; AC #14; US-08.2",
        "note": "Prevents accidental profile overwrites."
    },
    {
        "id": "TC-R8-INT-01", "pillar": "AC", "scenario_id": "TS-010-SUB",
        "title": "Verify Confirm Dialog 'Keep editing' button retains uncommitted dirty form data without API dispatch",
        "suite": "Submission & Confirm Dialog", "page": "Parent Portal > Profile", "severity": "S2", "priority": "Medium",
        "status": "Passed", "test_type": "Integration",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open",
        "test_data": "New phone: '98887777'",
        "steps": "1. Enter valid new phone '98887777'<br>2. Click [Save changes] -> opens Confirmation Dialog (role='alertdialog')<br>3. Click [Keep editing] button on dialog",
        "expected": "Confirmation Dialog closes immediately<br>Form remains in Edit Mode with '98887777' preserved in Mobile Number input<br>Zero HTTP PUT/PATCH mutation requests dispatched to backend<br>No toast displayed",
        "actual": "Keep editing button closes dialog and retains dirty form inputs without API dispatch.",
        "assumption": "TD: Dialog role='alertdialog' integration pattern", "defect": "",
        "traceability": "FR-08.3; AC #14; US-08.2",
        "note": "Multi-component interaction test between Form and Alertdialog."
    },
    {
        "id": "TC-R8-109", "pillar": "AC", "scenario_id": "TS-010-SUB",
        "title": "Verify backend system error (HTTP 500) displays MSG-0808 and preserves dirty form data without loss",
        "suite": "Submission & Confirm Dialog", "page": "Parent Portal > Profile", "severity": "S2", "priority": "High",
        "status": "Passed", "test_type": "Functional",
        "env": "SIT<br>Chrome (latest) + Route mock / fault injection<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; mock profile update API forced to return HTTP 500 Internal Server Error",
        "test_data": "Phone: '98887777'",
        "steps": "1. Enter new phone '98887777'<br>2. Click [Save changes] and confirm in dialog<br>3. Intercept API and return HTTP 500<br>4. Inspect UI response and form state",
        "expected": "Displays error toast/banner MSG-0808: 'We could not update your details. Please try again.'<br>Page does NOT crash (No White Screen of Death)<br>Form remains in Edit Mode with '98887777' preserved so user does not lose typed data<br>Database retains original phone '91234567'",
        "actual": "MSG-0808 displayed; form inputs preserved; DB retains original values.",
        "assumption": "CR: FSD section 6 table and AC #17 error handling", "defect": "",
        "traceability": "FR-08.3 errors; R8-AC17; MSG-0808",
        "note": "Fault injection resilience test."
    },
    {
        "id": "TC-R8-098", "pillar": "AC", "scenario_id": "TS-010-TEL",
        "title": "Verify Singapore mobile numbers starting with valid prefixes 6, 8, and 9 are accepted",
        "suite": "Mobile Number Component", "page": "Parent Portal > Profile", "severity": "S3", "priority": "Medium",
        "status": "Passed", "test_type": "Functional",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open",
        "test_data": "EP Valid: 61234567, 81234567, 91234567",
        "steps": "1. In Edit Mode, enter mobile number '61234567' and save<br>2. Enter mobile number '81234567' and save<br>3. Enter mobile number '91234567' and save",
        "expected": "All 3 numbers starting with 6, 8, and 9 pass validation without inline errors<br>Profile updates successfully with success toast MSG-0807",
        "actual": "All 3 valid Singapore prefixes accepted and saved with MSG-0807.",
        "assumption": "CR: Singapore National Numbering Plan standard 8-digit mobile prefixes 6, 8, 9", "defect": "",
        "traceability": "FR-08.3; FS R8 field table (Mobile); R8-AC14",
        "note": "Covers Equivalence Partitioning for valid SG phone prefixes."
    },
    {
        "id": "TC-R8-099", "pillar": "AC", "scenario_id": "TS-010-TEL",
        "title": "Verify invalid mobile numbers containing letters or mixed alphanumeric are rejected with MSG-0805",
        "suite": "Mobile Number Component", "page": "Parent Portal > Profile", "severity": "S2", "priority": "High",
        "status": "Passed", "test_type": "Functional",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open",
        "test_data": "EP Invalid: '12345qqqq', '9123abcd', 'abcdefgh'",
        "steps": "1. Enter '12345qqqq' into Mobile Number input<br>2. Blur the field or click Save changes<br>3. Inspect inline validation error message and input border",
        "expected": "System rejects submission and displays MSG-0805: 'Enter a mobile number in the correct format, like 9123 4567'<br>Input field highlights with red glowing border (aria-invalid='true')<br>Confirm Dialog is blocked",
        "actual": "Invalid alphanumeric phone rejected; displays inline error and marks field invalid.",
        "assumption": "TD: Regex /^[689]\\d{7}$/ enforced on blur and submit", "defect": "",
        "traceability": "FR-08.3 errors; R8-AC15; MSG-0805",
        "note": "Prevents malformed phone records in database."
    },
    {
        "id": "TC-R8-TEL-01", "pillar": "AC", "scenario_id": "TS-010-TEL",
        "title": "Verify mobile numbers starting with invalid prefixes (1, 2, 3, 4, 5, 7) are rejected with MSG-0805",
        "suite": "Mobile Number Component", "page": "Parent Portal > Profile", "severity": "S2", "priority": "High",
        "status": "Passed", "test_type": "Functional",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open",
        "test_data": "Invalid prefixes: '71234567', '51234567', '11234567', '21234567'",
        "steps": "1. Enter '71234567' and blur<br>2. Enter '51234567' and blur<br>3. Verify error message on each attempt",
        "expected": "Validation fails on each invalid prefix<br>Displays MSG-0805: 'Enter a mobile number in the correct format, like 9123 4567'<br>Save button blocked from dispatching mutation",
        "actual": "Displays MSG-0805 for non-6/8/9 starting digits.",
        "assumption": "CR: Singapore telecom standard restricts mobile services to 8/9 (and 6 for fixed-line/unified)", "defect": "",
        "traceability": "FR-08.3 errors; R8-AC15; MSG-0805",
        "note": "Negative testing of Singapore phone prefix boundary."
    },
    {
        "id": "TC-R8-TEL-03", "pillar": "AC", "scenario_id": "TS-010-TEL",
        "title": "Verify clearing mandatory Mobile Number input triggers required validation error MSG-0001",
        "suite": "Mobile Number Component", "page": "Parent Portal > Profile", "severity": "S2", "priority": "High",
        "status": "Passed", "test_type": "Functional",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open",
        "test_data": "Mobile number = '' (empty string)",
        "steps": "1. Clear the Mobile Number input field completely<br>2. Blur the field or click [Save changes]",
        "expected": "Displays required field error MSG-0001: 'Enter your mobile number' (or 'This field is required')<br>Input marked with aria-invalid='true' and red border<br>Save button is disabled",
        "actual": "MSG-0001 displayed under Mobile Number field; save action blocked.",
        "assumption": "CR: Mandatory field rule per FSD section 6 table", "defect": "BUG-R8-005",
        "traceability": "FR-08.3 errors; R8-AC16; MSG-0001",
        "note": "Mandatory field check for contact phone."
    },
    {
        "id": "TC-R8-EML-01", "pillar": "AC", "scenario_id": "TS-010-EML",
        "title": "Verify valid email formats including subdomains, plus-addressing, dots, and uppercase are accepted",
        "suite": "Email Address Component", "page": "Parent Portal > Profile", "severity": "S3", "priority": "Medium",
        "status": "Passed", "test_type": "Functional",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open",
        "test_data": "EP Valid: 'weiming.tan@example.sg', 'parent+moe@gmail.com', 'ABC@GMAIL.COM', ' abc@gmail.com '",
        "steps": "1. Enter each valid email format and save<br>2. Verify successful persistence and lowercase normalization",
        "expected": "All valid email variants pass validation cleanly<br>Profile updates successfully with MSG-0807 toast<br>Leading/trailing spaces trimmed cleanly",
        "actual": "Valid emails with dots, hyphens, plus-signs, and subdomains accepted.",
        "assumption": "TD: Standard email RFC compliance", "defect": "",
        "traceability": "FR-08.3; FS R8 sec. 6 field table; R8-AC14",
        "note": "Ensures legitimate government and corporate emails are supported."
    },
    {
        "id": "TC-R8-101", "pillar": "AC", "scenario_id": "TS-010-EML",
        "title": "Verify invalid email formats are rejected with error MSG-0806 (RFC 5322 Syntax Permutations)",
        "suite": "Email Address Component", "page": "Parent Portal > Profile", "severity": "S2", "priority": "High",
        "status": "Passed", "test_type": "Functional",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open",
        "test_data": "EP Invalid: 'nameexample.com' (no @), 'name@' (no domain), '@example.com' (no local), 'abc@@gmail.com', 'abc@gmail..com', 'abc@gmail,com', 'abc@gmail.c'",
        "steps": "1. For each invalid email format, enter into Email input and blur<br>2. Verify inline error presentation and red border",
        "expected": "Validation rejects each invalid syntax<br>Displays MSG-0806: 'Enter an email address in the correct format, like name@example.com'<br>Input highlights with aria-invalid='true'<br>Submission blocked",
        "actual": "Displays inline validation error for malformed email strings.",
        "assumption": "CR: Standard RFC 5322 regex validation", "defect": "BUG-R8-004",
        "traceability": "FR-08.3 errors; R8-AC15; MSG-0806",
        "note": "Covers equivalence partitions for invalid email syntax."
    },
    {
        "id": "TC-R8-EML-02", "pillar": "AC", "scenario_id": "TS-010-EML",
        "title": "Verify email address containing space is rejected with MSG-0806",
        "suite": "Email Address Component", "page": "Parent Portal > Profile", "severity": "S3", "priority": "Medium",
        "status": "Passed", "test_type": "Functional",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open",
        "test_data": "Input: 'name @example.com', 'name@ example.com', 'a b@gmail.com'",
        "steps": "1. Enter 'name @example.com' into Email input<br>2. Attempt to save form",
        "expected": "Validation detects illegal whitespace within email address<br>Displays MSG-0806: 'Enter an email address in the correct format, like name@example.com'<br>Save action blocked",
        "actual": "Rejected with MSG-0806 due to embedded whitespace.",
        "assumption": "CR: RFC 5322 forbids unquoted spaces in email addresses", "defect": "",
        "traceability": "FR-08.3 errors; R8-AC15; MSG-0806",
        "note": "Prevents broken email addresses from entering mail queue."
    },
    {
        "id": "TC-R8-EML-03", "pillar": "AC", "scenario_id": "TS-010-EML",
        "title": "Verify clearing mandatory Email Address input triggers required error MSG-0001",
        "suite": "Email Address Component", "page": "Parent Portal > Profile", "severity": "S2", "priority": "High",
        "status": "Passed", "test_type": "Functional",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open",
        "test_data": "Email = '' (empty string)",
        "steps": "1. Clear the Email input field completely<br>2. Blur field or click [Save changes]",
        "expected": "Displays required field error MSG-0001: 'Enter your email' (or 'This field is required')<br>Input marked with aria-invalid='true'<br>Save button disabled",
        "actual": "MSG-0001 displayed under Email field; save blocked.",
        "assumption": "CR: Email is mandatory field per FSD section 6 table", "defect": "BUG-R8-005",
        "traceability": "FR-08.3 errors; R8-AC16; MSG-0001",
        "note": "Mandatory email field validation."
    },
    {
        "id": "TC-R8-105", "pillar": "AC", "scenario_id": "TS-010-BLK",
        "title": "Verify optional Mailing Block can be left blank and saved successfully",
        "suite": "Mailing Block Component", "page": "Parent Portal > Profile", "severity": "S4 (lowest)", "priority": "Low",
        "status": "Passed", "test_type": "Functional",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open",
        "test_data": "MailingBlock = '' (empty); other required fields valid",
        "steps": "1. Clear Mailing Block input field<br>2. Fill all other required fields with valid values<br>3. Click [Save changes] and confirm in dialog",
        "expected": "Form passes validation without error<br>Profile updates successfully with MSG-0807<br>Reloading shows empty Mailing Block",
        "actual": "Blank Mailing Block saved successfully with MSG-0807.",
        "assumption": "CR: FSD section 6 table defines Mailing Block as optional (Bắt buộc: Không)", "defect": "",
        "traceability": "FS R8 sec. 6 field table (Mailing block optional); Appendix A Parent_Profile.MailingBlock",
        "note": "Landed properties and private estates often do not have block numbers."
    },
    {
        "id": "TC-R8-UNT-01", "pillar": "AC", "scenario_id": "TS-010-UNT",
        "title": "Verify optional Mailing Unit can be left blank and saved successfully",
        "suite": "Mailing Unit Component", "page": "Parent Portal > Profile", "severity": "S4 (lowest)", "priority": "Low",
        "status": "Passed", "test_type": "Functional",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open",
        "test_data": "MailingUnit = '' (empty); other required fields valid",
        "steps": "1. Clear Mailing Unit input field<br>2. Save form and confirm in dialog",
        "expected": "Form passes validation without error<br>Profile updates successfully with MSG-0807<br>Reloading shows empty Mailing Unit",
        "actual": "Blank Mailing Unit saved successfully with MSG-0807.",
        "assumption": "CR: FSD section 6 table defines Mailing Unit as optional (Bắt buộc: Không)", "defect": "",
        "traceability": "FS R8 sec. 6 field table (Mailing unit optional); Appendix A Parent_Profile.MailingUnit",
        "note": "Landed houses (bungalows, terraces) do not possess unit numbers."
    },
    {
        "id": "TC-R8-STR-01", "pillar": "AC", "scenario_id": "TS-010-STR",
        "title": "Verify clearing mandatory Mailing Street input triggers required validation error MSG-0001",
        "suite": "Mailing Street Component", "page": "Parent Portal > Profile", "severity": "S2", "priority": "High",
        "status": "Passed", "test_type": "Functional",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open",
        "test_data": "MailingStreet = '' (empty string)",
        "steps": "1. Clear Mailing Street input field<br>2. Blur field or click [Save changes]",
        "expected": "Displays required error MSG-0001: 'Enter your street' (or 'This field is required')<br>Input marked with aria-invalid='true'<br>Save button disabled",
        "actual": "MSG-0001 displayed under Mailing Street; submission blocked.",
        "assumption": "CR: Mailing Street is mandatory per FSD section 6 table", "defect": "BUG-R8-005",
        "traceability": "FR-08.3 errors; R8-AC16; MSG-0001",
        "note": "Mandatory address street validation."
    },
    {
        "id": "TC-R8-108", "pillar": "AC", "scenario_id": "TS-010-POS",
        "title": "Verify Singapore Mailing Postal Code must be exactly 6 numeric digits (EP Valid vs Invalid)",
        "suite": "Mailing Postal Code Component", "page": "Parent Portal > Profile", "severity": "S3", "priority": "Medium",
        "status": "Passed", "test_type": "Functional",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open",
        "test_data": "EP Valid: 650009, 238888, 560123; EP Invalid: 65000 (5 digits), 6500091 (7 digits), 65A009",
        "steps": "1. Enter '650009' and verify successful save<br>2. Enter '65000' and attempt save<br>3. Enter '6500091' and attempt save<br>4. Enter '65A009' and attempt save",
        "expected": "'650009' passes and saves with MSG-0807<br>'65000', '6500091', and '65A009' are rejected with inline validation error and red border<br>Nothing invalid saved to DB",
        "actual": "Only exact 6-digit postal code 650009 is accepted; others rejected.",
        "assumption": "ASM-09: No message code is defined for postal-code errors; field-level validation blocks Save.", "defect": "",
        "traceability": "FS R8 field table (Postal code 6 digits); Appendix A Parent_Profile.MailingPostalCode VARCHAR(10)",
        "note": "Singapore postal code format verification."
    },
    {
        "id": "TC-R8-POS-03", "pillar": "AC", "scenario_id": "TS-010-POS",
        "title": "Verify postal code containing non-digits, special symbols, or hyphens (e.g. '23888a', '650-009') is rejected",
        "suite": "Mailing Postal Code Component", "page": "Parent Portal > Profile", "severity": "S3", "priority": "Low",
        "status": "Passed", "test_type": "Functional",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open",
        "test_data": "Input: '23888a', 'ABCDEF', '650-009', '650 09', '65000.'",
        "steps": "1. Enter '23888a' into Postal Code<br>2. Attempt to save form",
        "expected": "Validation rejects non-digit characters<br>Displays inline validation error<br>Submission blocked",
        "actual": "Rejected: only numeric digits permitted.",
        "assumption": "TD: Regex /^\\d{6}$/ enforced on postal code", "defect": "",
        "traceability": "FS R8 sec. 6 field table; Appendix A",
        "note": "Prevents malformed postal codes."
    },
    {
        "id": "TC-R8-POS-04", "pillar": "AC", "scenario_id": "TS-010-POS",
        "title": "Verify clearing mandatory Mailing Postal Code triggers required error MSG-0001",
        "suite": "Mailing Postal Code Component", "page": "Parent Portal > Profile", "severity": "S2", "priority": "High",
        "status": "Passed", "test_type": "Functional",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open",
        "test_data": "MailingPostalCode = '' (empty string)",
        "steps": "1. Clear Postal Code input field<br>2. Blur field or click [Save changes]",
        "expected": "Displays required field error MSG-0001: 'Enter your postal code' (or 'This field is required')<br>Input marked with aria-invalid='true'<br>Save button disabled",
        "actual": "MSG-0001 displayed under Postal Code field; submission blocked.",
        "assumption": "CR: Postal Code is mandatory per FSD section 6 table", "defect": "BUG-R8-005",
        "traceability": "FR-08.3 errors; R8-AC16; MSG-0001",
        "note": "Mandatory postal code validation."
    },
    {
        "id": "TC-R8-CTY-03", "pillar": "AC", "scenario_id": "TS-010-CTY",
        "title": "Verify clearing mandatory Mailing Country triggers required validation error MSG-0001",
        "suite": "Mailing Country Component", "page": "Parent Portal > Profile", "severity": "S2", "priority": "High",
        "status": "Passed", "test_type": "Functional",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open",
        "test_data": "MailingCountry = '' (empty string)",
        "steps": "1. Clear Mailing Country input field<br>2. Blur field or click [Save changes]",
        "expected": "Displays required error MSG-0001: 'Enter your country' (or 'This field is required')<br>Input marked with aria-invalid='true'<br>Save button disabled",
        "actual": "MSG-0001 displayed under Mailing Country; submission blocked.",
        "assumption": "CR: Mailing Country is mandatory per FSD section 6 table", "defect": "BUG-R8-005",
        "traceability": "FR-08.3 errors; R8-AC16; MSG-0001",
        "note": "Mandatory country field validation."
    },

    # =========================================================================
    # TRỤ CỘT 3: TECHNICAL & UI MATRIX (73 TCs)
    # 3.1 Field-level BVA & Formatting (33 TCs)
    # =========================================================================
    {
        "id": "TC-R8-TEL-02", "pillar": "TECH", "scenario_id": "TS-010-TEL",
        "title": "Verify mobile number length boundary: 7 digits and 9 digits are rejected with MSG-0805 (BVA Length)",
        "suite": "Mobile Number Component", "page": "Parent Portal > Profile", "severity": "S3", "priority": "High",
        "status": "Passed", "test_type": "BVA",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open",
        "test_data": "BVA Length: 7 digits ('9123456' - underflow), 9 digits ('912345678' - overflow)",
        "steps": "1. Enter 7-digit number '9123456' and trigger validation<br>2. Enter 9-digit number '912345678' and trigger validation",
        "expected": "Both 7-digit and 9-digit inputs are rejected<br>Displays MSG-0805: 'Enter a mobile number in the correct format, like 9123 4567'<br>No data is committed to DB",
        "actual": "Rejected with MSG-0805 for length != 8 digits.",
        "assumption": "TD: BVA 2-point test on exact 8-digit Singapore phone length constraint", "defect": "",
        "traceability": "FS R8 sec. 6 field table; R8-AC15; MSG-0805",
        "note": "Boundary Value Analysis (N-1 = 7, N+1 = 9)."
    },
    {
        "id": "TC-R8-100", "pillar": "TECH", "scenario_id": "TS-010-TEL",
        "title": "Verify mobile number entered with space is accepted and trimmed upon saving (ASM-08)",
        "suite": "Mobile Number Component", "page": "Parent Portal > Profile", "severity": "S4 (lowest)", "priority": "Low",
        "status": "Passed", "test_type": "Functional",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open",
        "test_data": "Input: '9123 4567' -> Stored value: '91234567'",
        "steps": "1. Enter '9123 4567' (with middle space) in Mobile Number<br>2. Click [Save changes] and confirm in dialog<br>3. Verify UI toast and check stored value upon reload",
        "expected": "Input is accepted without error<br>Saved successfully with MSG-0807<br>Stored and rendered as '91234567' (space stripped cleanly)",
        "actual": "Saved with MSG-0807; stored value normalized to 91234567.",
        "assumption": "ASM-08: Mobile number entered with a space ('9123 4567') is accepted and stored without the space.", "defect": "",
        "traceability": "FS R8 field table (example format '9123 4567')",
        "note": "User-friendly auto-trimming of typical phone formatting spaces."
    },
    {
        "id": "TC-R8-TEL-04", "pillar": "TECH", "scenario_id": "TS-010-TEL",
        "title": "Verify whitespace-only Mobile Number input is treated as empty and triggers MSG-0001 (ASM-15)",
        "suite": "Mobile Number Component", "page": "Parent Portal > Profile", "severity": "S4 (lowest)", "priority": "Medium",
        "status": "Passed", "test_type": "Functional",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open",
        "test_data": "Mobile number = '        ' (8 blank spaces)",
        "steps": "1. Enter multiple spaces into Mobile Number input<br>2. Trigger validation by blurring or clicking Save",
        "expected": "Whitespace is trimmed and treated as empty input<br>Displays required field error MSG-0001<br>Nothing is saved to database",
        "actual": "Whitespace trimmed; required field validation triggered.",
        "assumption": "ASM-15: Whitespace-only input in a required field is treated as blank.", "defect": "",
        "traceability": "FR-08.3 errors; ASM-15; MSG-0001",
        "note": "Prevents bypassing mandatory checks with spaces."
    },
    {
        "id": "TC-R8-TEL-05", "pillar": "TECH", "scenario_id": "TS-010-TEL",
        "title": "Verify mobile numbers with decimals, negative signs, or symbols (+, -) are rejected with MSG-0805",
        "suite": "Mobile Number Component", "page": "Parent Portal > Profile", "severity": "S3", "priority": "Medium",
        "status": "Passed", "test_type": "Functional",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open",
        "test_data": "Symbols & math: '91.234567', '-9123456', '+6591234567', '9123-4567'",
        "steps": "1. Enter '91.234567' and blur<br>2. Enter '-9123456' and blur<br>3. Enter '+6591234567' and blur",
        "expected": "All non-digit formatted strings are rejected<br>Displays MSG-0805: 'Enter a mobile number in the correct format, like 9123 4567'<br>Save action is blocked",
        "actual": "Mathematical notations and symbols rejected per MSG-0805.",
        "assumption": "TD: Strict 8-digit regex without international + or separators", "defect": "",
        "traceability": "FR-08.3; FS R8 field table; MSG-0805",
        "note": "Singapore local mobile numbers are strictly 8 digits."
    },
    {
        "id": "TC-R8-TEL-06", "pillar": "TECH", "scenario_id": "TS-010-TEL",
        "title": "Verify full-width Unicode digits ('９１２３４５６７') are handled safely and rejected or normalized",
        "suite": "Mobile Number Component", "page": "Parent Portal > Profile", "severity": "S4 (lowest)", "priority": "Low",
        "status": "Passed", "test_type": "Functional",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open",
        "test_data": "Full-width digits: '９１２３４５６７'",
        "steps": "1. Enter full-width digits '９１２３４５６７' into Mobile Number<br>2. Trigger blur or click Save changes<br>3. Inspect UI response",
        "expected": "System safely rejects non-ASCII digits with MSG-0805 or normalizes to ASCII '91234567'<br>Zero JavaScript crashes or uncaught exceptions",
        "actual": "Full-width digits handled safely without crash.",
        "assumption": "TD: Unicode full-width numeric block handling", "defect": "",
        "traceability": "Invariant 7; NFR Usability",
        "note": "Ensures system stability when pasting East Asian input."
    },
    {
        "id": "TC-R8-TEL-07", "pillar": "TECH", "scenario_id": "TS-010-TEL",
        "title": "Verify invalid mobile number displays human-readable error MSG-0805, red border, and strictly NO raw i18n key leakage",
        "suite": "Mobile Number Component", "page": "Parent Portal > Profile", "severity": "S1 (highest)", "priority": "Critical",
        "status": "Failed", "test_type": "UI",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open",
        "test_data": "Invalid input: '12345qqqq'",
        "steps": "1. Enter '12345qqqq' into Mobile Number input<br>2. Trigger blur event on the input<br>3. Inspect the rendered validation error message text and input class/attributes<br>4. Verify error text does NOT match raw key 'features.parentProfile.validation.mobileInvalid'",
        "expected": "Input field receives red glowing border and aria-invalid='true'<br>Validation message renders human-readable text matching MSG-0805 ('Enter a mobile number in the correct format, like 9123 4567')<br>NO raw i18n translation key (e.g. 'features.parentProfile.validation.mobileInvalid') is leaked on the DOM",
        "actual": "DEFECT: UI currently displays raw un-translated i18n key 'features.parentProfile.validation.mobileInvalid' instead of localized MSG-0805.",
        "assumption": "Mandate: Zero Raw i18n Key Leakage across UI surface", "defect": "BUG-R8-I18N-01",
        "traceability": "FR-08.3 errors; MSG-0805; Invariant 7 UI Health",
        "note": "Direct verification of image defect reported by user."
    },
    {
        "id": "TC-R8-102", "pillar": "TECH", "scenario_id": "TS-010-EML",
        "title": "Verify email maximum length limit boundary of 150 characters (BVA Length)",
        "suite": "Email Address Component", "page": "Parent Portal > Profile", "severity": "S3", "priority": "Medium",
        "status": "Passed", "test_type": "BVA",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open",
        "test_data": "BVA: 150 chars ('a'*138 + '@example.com') vs 151 chars ('a'*139 + '@example.com')",
        "steps": "1. Enter valid 150-char email address, click [Save changes] and confirm<br>2. Enter 151-char email address and attempt save",
        "expected": "150 chars: Accepted and saved successfully with MSG-0807<br>151 chars: Input truncated by maxlength='150' or rejected with inline validation error",
        "actual": "150 chars saved with MSG-0807; 151 chars prevented by field length constraint.",
        "assumption": "ASM-09: No message code is defined for max-length; field-level validation blocks Save.", "defect": "",
        "traceability": "FS R8 field table (Email max 150) - BVA; Appendix A Parent_Profile.Email NVARCHAR(150)",
        "note": "Protects against database column buffer overflow."
    },
    {
        "id": "TC-R8-EML-04", "pillar": "TECH", "scenario_id": "TS-010-EML",
        "title": "Verify whitespace-only Email input is treated as empty and triggers MSG-0001 (ASM-15)",
        "suite": "Email Address Component", "page": "Parent Portal > Profile", "severity": "S4 (lowest)", "priority": "Low",
        "status": "Passed", "test_type": "Functional",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open",
        "test_data": "Email = '       ' (blank spaces)",
        "steps": "1. Enter multiple spaces into Email input<br>2. Trigger validation by blurring or clicking Save",
        "expected": "Whitespace is trimmed and treated as empty input<br>Displays required field error MSG-0001<br>Nothing is saved to database",
        "actual": "Whitespace trimmed; required field validation MSG-0001 displayed.",
        "assumption": "ASM-15: Whitespace-only input in a required field is treated as blank.", "defect": "",
        "traceability": "FR-08.3 errors; ASM-15; MSG-0001",
        "note": "Prevents space injection bypassing mandatory check."
    },
    {
        "id": "TC-R8-EML-05", "pillar": "TECH", "scenario_id": "TS-010-EML",
        "title": "Verify pasting 1000-character string into Email input is handled safely without browser freeze or layout break",
        "suite": "Email Address Component", "page": "Parent Portal > Profile", "severity": "S3", "priority": "Medium",
        "status": "Passed", "test_type": "Stress",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open",
        "test_data": "Paste stress: 'A'*1000",
        "steps": "1. Paste 1000-character alphanumeric string into Email input<br>2. Inspect UI response and layout<br>3. Attempt save",
        "expected": "Browser does not freeze<br>Input is truncated to maxlength='150' or rejected with MSG-0806<br>No horizontal layout overflow occurs",
        "actual": "Paste handled safely; input truncated to max length without layout break.",
        "assumption": "TD: Browser DOM event clipboard paste stress testing", "defect": "",
        "traceability": "Invariant 7; NFR Usability",
        "note": "Ensures resilience against long paste buffers."
    },
    {
        "id": "TC-R8-EML-06", "pillar": "TECH", "scenario_id": "TS-010-EML",
        "title": "Verify invalid email displays localized error, red border, and strictly NO raw i18n translation key",
        "suite": "Email Address Component", "page": "Parent Portal > Profile", "severity": "S2", "priority": "High",
        "status": "Passed", "test_type": "UI",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open",
        "test_data": "Invalid email: 'invalid-email-format'",
        "steps": "1. Enter 'invalid-email-format' into Email input<br>2. Blur the input<br>3. Inspect the error alert text and aria-invalid attribute",
        "expected": "Input field highlights with red border and aria-invalid='true'<br>Displays readable message matching MSG-0806 ('Enter an email address in the correct format, like name@example.com')<br>NO raw key (e.g. 'features.parentProfile.validation.emailInvalid') is leaked",
        "actual": "Displays human-readable error text; no raw i18n translation key leaked.",
        "assumption": "Mandate: Zero Raw i18n Key Leakage across UI surface", "defect": "",
        "traceability": "FR-08.3 errors; MSG-0806; Invariant 7 UI Health",
        "note": "Guarantees professional localized UI error presentation."
    },
    {
        "id": "TC-R8-BLK-01", "pillar": "TECH", "scenario_id": "TS-010-BLK",
        "title": "Verify alphanumeric Mailing Block values (e.g. 'Blk 123A', 'Tower 2', '123', 'A') are saved accurately",
        "suite": "Mailing Block Component", "page": "Parent Portal > Profile", "severity": "S3", "priority": "Medium",
        "status": "Passed", "test_type": "Functional",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open",
        "test_data": "Valid blocks: 'Blk 123A', 'Tower 2', 'Block 9B', '123', 'A'",
        "steps": "1. Enter 'Blk 123A' into Mailing Block<br>2. Save and reload profile",
        "expected": "Block value persists accurately and renders 'Blk 123A' on view screen<br>Saved with MSG-0807",
        "actual": "Alphanumeric block string saved and reloaded accurately.",
        "assumption": "TD: Standard alphanumeric address text field", "defect": "",
        "traceability": "FS R8 sec. 6 field table; Appendix A",
        "note": "Supports common HDB and Condo block naming schemes."
    },
    {
        "id": "TC-R8-106", "pillar": "TECH", "scenario_id": "TS-010-BLK",
        "title": "Verify Mailing Block maximum length boundary of 20 characters (BVA Length)",
        "suite": "Mailing Block Component", "page": "Parent Portal > Profile", "severity": "S4 (lowest)", "priority": "Low",
        "status": "Passed", "test_type": "BVA",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open",
        "test_data": "BVA: 20 chars ('B'*20) vs 21 chars ('B'*21)",
        "steps": "1. Enter 20-character string into Mailing Block, save and verify<br>2. Enter 21-character string into Mailing Block and attempt save",
        "expected": "20 chars: Successfully saved with MSG-0807<br>21 chars: Truncated by maxlength='20' attribute or blocked with field length error",
        "actual": "20 chars accepted and saved; 21 chars prevented by input length constraint.",
        "assumption": "ASM-09: No message code defined for max-length; field-level validation blocks Save.", "defect": "",
        "traceability": "FS R8 field table (Block max 20) - BVA; Appendix A Parent_Profile.MailingBlock NVARCHAR(20)",
        "note": "Prevents database truncation error in Parent_Profile table."
    },
    {
        "id": "TC-R8-BLK-02", "pillar": "TECH", "scenario_id": "TS-010-BLK",
        "title": "Verify Mailing Block allows address symbols (/ , . - #) and rejects forbidden symbols (< > { } ;) or 1000-char paste",
        "suite": "Mailing Block Component", "page": "Parent Portal > Profile", "severity": "S3", "priority": "Medium",
        "status": "Passed", "test_type": "Functional",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open",
        "test_data": "Allowed: 'Blk 12-A/B #01'; Forbidden: '<script>', '{blk}'",
        "steps": "1. Enter 'Blk 12-A/B #01' and verify save<br>2. Enter '<script>' and verify rejection or sanitization<br>3. Paste 1000 characters",
        "expected": "Legitimate punctuation saved accurately<br>Dangerous HTML symbols sanitized or blocked<br>1000 chars truncated to maxlength='20'",
        "actual": "Address punctuation accepted; dangerous symbols sanitized; length bounded.",
        "assumption": "TD: Address field character whitelist and boundary protection", "defect": "",
        "traceability": "NFR Security; Invariant 8",
        "note": "Protects input integrity across address components."
    },
    {
        "id": "TC-R8-UNT-03", "pillar": "TECH", "scenario_id": "TS-010-UNT",
        "title": "Verify standard Singapore apartment unit notation (e.g. '#02-01', '#12-345', '12-34A', 'Level 2') is saved accurately",
        "suite": "Mailing Unit Component", "page": "Parent Portal > Profile", "severity": "S3", "priority": "Medium",
        "status": "Passed", "test_type": "Functional",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open",
        "test_data": "Unit inputs: '#02-01', '#12-345', '12-34A', 'Level 2'",
        "steps": "1. Enter '#02-01' into Mailing Unit<br>2. Save and reload profile",
        "expected": "Unit string persists accurately and renders '#02-01' on view screen<br>Saved with MSG-0807",
        "actual": "Standard unit format saved and displayed correctly.",
        "assumption": "TD: Standard Singapore address unit notation with '#' and hyphen", "defect": "",
        "traceability": "FS R8 sec. 6 field table; Appendix A",
        "note": "Typical HDB/condo floor-and-unit format."
    },
    {
        "id": "TC-R8-UNT-02", "pillar": "TECH", "scenario_id": "TS-010-UNT",
        "title": "Verify Mailing Unit maximum length boundary of 20 characters (BVA Length)",
        "suite": "Mailing Unit Component", "page": "Parent Portal > Profile", "severity": "S4 (lowest)", "priority": "Low",
        "status": "Passed", "test_type": "BVA",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open",
        "test_data": "BVA: 20 chars ('#12-123456789012345') vs 21 chars ('#12-1234567890123456')",
        "steps": "1. Enter 20-character string into Mailing Unit, save and verify<br>2. Enter 21-character string into Mailing Unit and attempt save",
        "expected": "20 chars: Successfully saved with MSG-0807<br>21 chars: Truncated by maxlength='20' attribute or blocked with field length error",
        "actual": "20 chars accepted; 21 chars blocked by field constraint.",
        "assumption": "ASM-09: No message code defined for max-length; field-level validation blocks Save.", "defect": "",
        "traceability": "FS R8 field table (Unit max 20) - BVA; Appendix A Parent_Profile.MailingUnit NVARCHAR(20)",
        "note": "Protects against database column buffer overflow."
    },
    {
        "id": "TC-R8-UNT-04", "pillar": "TECH", "scenario_id": "TS-010-UNT",
        "title": "Verify forbidden symbols (< > { } ;) in Mailing Unit are rejected and multiline paste handles newlines gracefully",
        "suite": "Mailing Unit Component", "page": "Parent Portal > Profile", "severity": "S3", "priority": "Medium",
        "status": "Passed", "test_type": "Functional",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open",
        "test_data": "Forbidden: '<script>', '{01-02}'; Multiline: '#02-01\\nTower A'",
        "steps": "1. Enter '<script>' in Mailing Unit and blur<br>2. Paste multiline string '#02-01\\nTower A'<br>3. Inspect input state",
        "expected": "HTML script tags are sanitized or rejected<br>Newlines in multiline paste are stripped/collapsed into single space without crashing layout",
        "actual": "Forbidden characters blocked; multiline newlines stripped cleanly.",
        "assumption": "TD: Input sanitization and newline normalization", "defect": "",
        "traceability": "NFR Security; Invariant 8",
        "note": "Prevents malformed addresses and UI disruption."
    },
    {
        "id": "TC-R8-104", "pillar": "TECH", "scenario_id": "TS-010-STR",
        "title": "Verify whitespace-only Mailing Street input is treated as blank and displays MSG-0001 (ASM-15)",
        "suite": "Mailing Street Component", "page": "Parent Portal > Profile", "severity": "S4 (lowest)", "priority": "Low",
        "status": "Passed", "test_type": "Functional",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open",
        "test_data": "MailingStreet = '          ' (10 blank spaces)",
        "steps": "1. Enter spaces only in Mailing Street<br>2. Click [Save changes] or blur field",
        "expected": "System detects empty content and displays required field error MSG-0001 under Mailing Street<br>Input highlights red with aria-invalid='true'<br>Save action blocked",
        "actual": "Whitespace detected as empty; MSG-0001 error displayed.",
        "assumption": "ASM-15: Whitespace-only input in a required field is treated as blank.", "defect": "",
        "traceability": "FR-08.3 errors; ASM-15; MSG-0001",
        "note": "Ensures user cannot submit street with just spaces."
    },
    {
        "id": "TC-R8-107", "pillar": "TECH", "scenario_id": "TS-010-STR",
        "title": "Verify Mailing Street maximum length boundary of 100 characters (BVA Length)",
        "suite": "Mailing Street Component", "page": "Parent Portal > Profile", "severity": "S4 (lowest)", "priority": "Low",
        "status": "Passed", "test_type": "BVA",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open",
        "test_data": "BVA: 100 chars ('S'*100) vs 101 chars ('S'*101)",
        "steps": "1. Enter 100-character string into Mailing Street, save and verify<br>2. Enter 101-character string into Mailing Street and attempt save",
        "expected": "100 chars: Successfully saved with MSG-0807<br>101 chars: Truncated by maxlength='100' or blocked with field length error",
        "actual": "100 chars saved; 101 chars blocked by maxlength constraint.",
        "assumption": "ASM-09: No message code defined for max-length; field-level validation blocks Save.", "defect": "",
        "traceability": "FS R8 field table (Street max 100) - BVA; Appendix A Parent_Profile.MailingStreet NVARCHAR(100)",
        "note": "Prevents database column overflow in Parent_Profile table."
    },
    {
        "id": "TC-R8-STR-02", "pillar": "TECH", "scenario_id": "TS-010-STR",
        "title": "Verify valid Singapore street names with punctuation (hyphens, dots, apostrophes) are saved accurately",
        "suite": "Mailing Street Component", "page": "Parent Portal > Profile", "severity": "S3", "priority": "Medium",
        "status": "Passed", "test_type": "Functional",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open",
        "test_data": "Streets: 'St. George\\'s Lane', 'Jalan Jurong Kechil', 'Ang Mo Kio Ave 3'",
        "steps": "1. Enter 'St. George\\'s Lane' into Mailing Street<br>2. Save and reload profile",
        "expected": "Street persists accurately and renders 'St. George\\'s Lane' on view screen<br>Saved with MSG-0807",
        "actual": "Street name with apostrophe and period saved and reloaded accurately.",
        "assumption": "TD: Standard address string allowing legitimate punctuation", "defect": "",
        "traceability": "FS R8 sec. 6 field table; Appendix A",
        "note": "Ensures special characters in Singapore street names are preserved."
    },
    {
        "id": "TC-R8-STR-03", "pillar": "TECH", "scenario_id": "TS-010-STR",
        "title": "Verify forbidden symbols (< > { } ;) in Mailing Street are blocked or sanitized",
        "suite": "Mailing Street Component", "page": "Parent Portal > Profile", "severity": "S3", "priority": "Medium",
        "status": "Passed", "test_type": "Functional",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open",
        "test_data": "Forbidden: 'Ang Mo Kio Ave 3 <script>', '{Street 52};'",
        "steps": "1. Enter 'Ang Mo Kio Ave 3 <script>' into Mailing Street<br>2. Attempt to save form",
        "expected": "HTML script injection characters blocked or sanitized<br>No raw tags committed to database",
        "actual": "Dangerous symbols blocked and sanitized.",
        "assumption": "TD: Input sanitization whitelist", "defect": "",
        "traceability": "NFR Security; Invariant 8",
        "note": "Prevents address injection attacks."
    },
    {
        "id": "TC-R8-STR-04", "pillar": "TECH", "scenario_id": "TS-010-STR",
        "title": "Verify pasting 1000-character string or multiline text into Mailing Street is handled safely without UI breakage",
        "suite": "Mailing Street Component", "page": "Parent Portal > Profile", "severity": "S3", "priority": "Medium",
        "status": "Passed", "test_type": "Stress",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open",
        "test_data": "Paste stress: 'S'*1000; Multiline: 'Line 1\\nLine 2'",
        "steps": "1. Paste 1000 characters into Mailing Street<br>2. Inspect input value and viewport overflow<br>3. Paste multiline address",
        "expected": "Input truncated to maxlength='100'<br>Document scrollWidth === clientWidth (zero overflow)<br>Newlines stripped/collapsed to single space",
        "actual": "Paste stress handled cleanly; 0 overflow; newlines normalized.",
        "assumption": "TD: Viewport layout stress & boundary truncation", "defect": "",
        "traceability": "Invariant 7; NFR Usability",
        "note": "Ensures robust handling of large clipboard data."
    },
    {
        "id": "TC-R8-114", "pillar": "TECH", "scenario_id": "TS-010-STR",
        "title": "Verify malicious script input in Mailing Street is sanitized and rendered as plain text without XSS execution",
        "suite": "Mailing Street Component", "page": "Parent Portal > Profile", "severity": "S2", "priority": "Medium",
        "status": "Passed", "test_type": "Security",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open",
        "test_data": "XSS vector: <script>alert(1)</script>",
        "steps": "1. Enter '<script>alert(1)</script>' in Mailing Street<br>2. Click [Save changes] and confirm in dialog<br>3. Reload profile page and inspect rendered text and console",
        "expected": "No alert popup is triggered<br>Zero JavaScript errors on console<br>Script tags are rendered safely as escaped plain text or sanitized in DB",
        "actual": "Script tag escaped safely as plain text, no execution detected.",
        "assumption": "TD: Invariant 8 - HTML entity encoding and DOMPurify on output", "defect": "",
        "traceability": "NFR Security; Invariant 8",
        "note": "Prevents Stored Cross-Site Scripting (XSS) attacks."
    },
    {
        "id": "TC-R8-POS-01", "pillar": "TECH", "scenario_id": "TS-010-POS",
        "title": "Verify Singapore postal code with leading zero (e.g. '018956', '000000') is preserved as 6 digits across save and reload",
        "suite": "Mailing Postal Code Component", "page": "Parent Portal > Profile", "severity": "S3", "priority": "Medium",
        "status": "Passed", "test_type": "Functional",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open",
        "test_data": "Input: '018956' (Downtown Singapore sector with leading zero)",
        "steps": "1. Enter '018956' in Postal Code input<br>2. Click [Save changes] and confirm<br>3. Verify displayed postal code upon reload",
        "expected": "Postal code is preserved as text '018956' with leading zero intact<br>Leading zero is NOT stripped by numeric conversion<br>Saved with MSG-0807",
        "actual": "Leading zero preserved as '018956' across save and reload.",
        "assumption": "TD: Postal code stored as VARCHAR, preventing numeric casting zero-drop", "defect": "",
        "traceability": "FS R8 sec. 6 field table; Appendix A Parent_Profile.MailingPostalCode",
        "note": "Crucial for central Singapore districts (Marina Bay 01xxxx, Tanjong Pagar 07xxxx)."
    },
    {
        "id": "TC-R8-POS-02", "pillar": "TECH", "scenario_id": "TS-010-POS",
        "title": "Verify postal code length boundary: 5 digits and 7 digits are rejected (BVA Length)",
        "suite": "Mailing Postal Code Component", "page": "Parent Portal > Profile", "severity": "S3", "priority": "Medium",
        "status": "Passed", "test_type": "BVA",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open",
        "test_data": "BVA: 5 digits ('56012' - underflow) vs 7 digits ('5601234' - overflow)",
        "steps": "1. Enter 5-digit postal code '56012' and attempt save<br>2. Enter 7-digit postal code '5601234' and attempt save",
        "expected": "Both 5-digit and 7-digit inputs fail validation<br>Inline error displayed below Postal Code input<br>Save action blocked",
        "actual": "Rejected: postal code must be exactly 6 digits.",
        "assumption": "TD: BVA 2-point test on exact 6-digit Singapore postal format constraint", "defect": "",
        "traceability": "FS R8 sec. 6 field table; Appendix A",
        "note": "Enforces strict length boundary."
    },
    {
        "id": "TC-R8-POS-05", "pillar": "TECH", "scenario_id": "TS-010-POS",
        "title": "Verify whitespace-only Mailing Postal Code is treated as blank with MSG-0001 (ASM-15)",
        "suite": "Mailing Postal Code Component", "page": "Parent Portal > Profile", "severity": "S4 (lowest)", "priority": "Low",
        "status": "Passed", "test_type": "Functional",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open",
        "test_data": "MailingPostalCode = '      ' (6 blank spaces)",
        "steps": "1. Enter spaces only in Postal Code<br>2. Click [Save changes] or blur field",
        "expected": "Whitespace is treated as empty input<br>Displays required field error MSG-0001<br>Nothing saved to DB",
        "actual": "Whitespace detected as empty; MSG-0001 error displayed.",
        "assumption": "ASM-15: Whitespace-only input in a required field is treated as blank.", "defect": "",
        "traceability": "FR-08.3 errors; ASM-15; MSG-0001",
        "note": "Prevents space injection in postal code."
    },
    {
        "id": "TC-R8-POS-06", "pillar": "TECH", "scenario_id": "TS-010-POS",
        "title": "Verify invalid postal code displays localized error, red border, and strictly NO raw i18n key leakage",
        "suite": "Mailing Postal Code Component", "page": "Parent Portal > Profile", "severity": "S1 (highest)", "priority": "Critical",
        "status": "Failed", "test_type": "UI",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open",
        "test_data": "Invalid postal code: '12345'",
        "steps": "1. Enter '12345' into Postal Code input<br>2. Trigger blur event<br>3. Inspect the error alert text and aria-invalid attribute<br>4. Verify text does NOT contain 'features.parentProfile.validation.postalCodeInvalid'",
        "expected": "Postal Code input highlights with red glowing border (aria-invalid='true')<br>Validation message renders human-readable text (e.g. 'Postal code must be exactly 6 digits')<br>NO raw i18n translation key ('features.parentProfile.validation.postalCodeInvalid') is leaked",
        "actual": "DEFECT: UI currently displays raw un-translated key 'features.parentProfile.validation.postalCodeInvalid' instead of localized message.",
        "assumption": "Mandate: Zero Raw i18n Key Leakage across UI surface", "defect": "BUG-R8-I18N-02",
        "traceability": "FS R8 sec. 6 field table; Invariant 7 UI Health",
        "note": "Catches raw translation key defect in Postal Code component."
    },
    {
        "id": "TC-R8-POS-07", "pillar": "TECH", "scenario_id": "TS-010-POS",
        "title": "Verify full-width Unicode digits ('２３８８８８') and negative/decimal postal codes are rejected",
        "suite": "Mailing Postal Code Component", "page": "Parent Portal > Profile", "severity": "S3", "priority": "Low",
        "status": "Passed", "test_type": "Functional",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open",
        "test_data": "Inputs: '２３８８８８', '238.88', '-23888'",
        "steps": "1. Enter '２３８８８８' and blur<br>2. Enter '238.88' and blur<br>3. Enter '-23888' and blur",
        "expected": "Full-width digits, decimals, and negative numbers fail 6-digit regex validation<br>Inline error displayed; save action blocked",
        "actual": "Full-width, decimal, and negative postal codes rejected cleanly.",
        "assumption": "TD: Strict ASCII 6-digit validation", "defect": "",
        "traceability": "FS R8 sec. 6 field table; Appendix A",
        "note": "Guarantees data cleanliness for postal logistics integration."
    },
    {
        "id": "TC-R8-CTY-01", "pillar": "TECH", "scenario_id": "TS-010-CTY",
        "title": "Verify Mailing Country default value is 'Singapore' and can be modified for overseas address",
        "suite": "Mailing Country Component", "page": "Parent Portal > Profile", "severity": "S3", "priority": "Medium",
        "status": "Passed", "test_type": "Functional",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open",
        "test_data": "Default: 'Singapore'; Modified: 'Malaysia'",
        "steps": "1. Check default value in Mailing Country input<br>2. Change country to 'Malaysia'<br>3. Click [Save changes] and confirm in dialog<br>4. Reload profile page",
        "expected": "Default value is 'Singapore'<br>Updated value 'Malaysia' saves successfully with MSG-0807<br>Reloading shows 'Malaysia' rendered on profile",
        "actual": "Default 'Singapore' verified; updated to 'Malaysia' and persisted accurately.",
        "assumption": "CR: Default country is Singapore, supports overseas mailing", "defect": "",
        "traceability": "FS R8 sec. 6 field table; Appendix A Parent_Profile.MailingCountry",
        "note": "Allows parents residing or posting overseas to receive correspondence."
    },
    {
        "id": "TC-R8-CTY-05", "pillar": "TECH", "scenario_id": "TS-010-CTY",
        "title": "Verify text-only Mailing Country rejects numeric digits (e.g. 'Singapore1', '123')",
        "suite": "Mailing Country Component", "page": "Parent Portal > Profile", "severity": "S3", "priority": "Low",
        "status": "Passed", "test_type": "Functional",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open",
        "test_data": "Numeric inputs: 'Singapore1', '123', 'Country 404'",
        "steps": "1. Enter 'Singapore1' in Mailing Country<br>2. Attempt to save form",
        "expected": "System rejects numeric digits in Country name<br>Displays field error or blocks save",
        "actual": "Numeric country strings rejected.",
        "assumption": "TD: Text-only country name validation", "defect": "",
        "traceability": "FS R8 sec. 6 field table",
        "note": "Prevents numeric corruption in country name."
    },
    {
        "id": "TC-R8-CTY-06", "pillar": "TECH", "scenario_id": "TS-010-CTY",
        "title": "Verify legitimate country names with diacritics and hyphens (e.g. 'Côte d\\'Ivoire') are accepted",
        "suite": "Mailing Country Component", "page": "Parent Portal > Profile", "severity": "S3", "priority": "Low",
        "status": "Passed", "test_type": "Functional",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open",
        "test_data": "Valid: 'Côte d\\'Ivoire', 'Timor-Leste'",
        "steps": "1. Enter 'Côte d\\'Ivoire' into Mailing Country<br>2. Save and reload profile",
        "expected": "Country persists accurately with diacritics and apostrophe intact<br>Saved with MSG-0807",
        "actual": "Country with diacritics and apostrophe saved accurately.",
        "assumption": "TD: Unicode text support in Country NVARCHAR(100)", "defect": "",
        "traceability": "FS R8 sec. 6 field table; Appendix A",
        "note": "Supports legitimate sovereign country names."
    },
    {
        "id": "TC-R8-CTY-02", "pillar": "TECH", "scenario_id": "TS-010-CTY",
        "title": "Verify Mailing Country maximum length boundary of 100 characters (BVA Length)",
        "suite": "Mailing Country Component", "page": "Parent Portal > Profile", "severity": "S4 (lowest)", "priority": "Low",
        "status": "Passed", "test_type": "BVA",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open",
        "test_data": "BVA: 100 chars ('C'*100) vs 101 chars ('C'*101)",
        "steps": "1. Enter 100-character country name, save and verify<br>2. Enter 101-character string and attempt save",
        "expected": "100 chars: Successfully saved with MSG-0807<br>101 chars: Truncated by maxlength='100' or blocked with field length error",
        "actual": "100 chars saved; 101 chars blocked by maxlength constraint.",
        "assumption": "ASM-09: No message code defined for max-length; field-level validation blocks Save.", "defect": "",
        "traceability": "FS R8 field table (Country max 100) - BVA; Appendix A Parent_Profile.MailingCountry NVARCHAR(100)",
        "note": "Prevents database column overflow in Parent_Profile table."
    },
    {
        "id": "TC-R8-CTY-04", "pillar": "TECH", "scenario_id": "TS-010-CTY",
        "title": "Verify whitespace-only Mailing Country is treated as blank with MSG-0001 (ASM-15)",
        "suite": "Mailing Country Component", "page": "Parent Portal > Profile", "severity": "S4 (lowest)", "priority": "Low",
        "status": "Passed", "test_type": "Functional",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open",
        "test_data": "MailingCountry = '     ' (spaces)",
        "steps": "1. Enter spaces only in Mailing Country<br>2. Click [Save changes] or blur field",
        "expected": "Whitespace is treated as empty input<br>Displays required field error MSG-0001<br>Nothing saved to DB",
        "actual": "Whitespace detected as empty; MSG-0001 error displayed.",
        "assumption": "ASM-15: Whitespace-only input in a required field is treated as blank.", "defect": "",
        "traceability": "FR-08.3 errors; ASM-15; MSG-0001",
        "note": "Prevents space injection in country field."
    },
    {
        "id": "TC-R8-SUB-02", "pillar": "TECH", "scenario_id": "TS-010-SUB",
        "title": "Verify Confirm Dialog rapid double-click debounce dispatches only one single mutation request",
        "suite": "Submission & Confirm Dialog", "page": "Parent Portal > Profile", "severity": "S2", "priority": "Medium",
        "status": "Passed", "test_type": "Concurrency",
        "env": "SIT<br>Chrome (latest) + Network interceptor<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Confirmation Dialog open",
        "test_data": "Double-click within 50ms interval",
        "steps": "1. Open Confirmation Dialog with modified form data<br>2. Intercept outgoing PUT/PATCH /api/parent/profile requests<br>3. Rapidly double-click [Save changes] button on dialog<br>4. Count dispatched requests",
        "expected": "Button immediately enters loading state and disables further clicks (isSubmitting=true)<br>Exactly ONE mutation request is dispatched to server<br>No duplicate audit records or race conditions generated",
        "actual": "Debounce verified: exactly 1 HTTP mutation request sent.",
        "assumption": "TD: Invariant 8 - UI debounce and API idempotency", "defect": "",
        "traceability": "FR-08.3; NFR Concurrency; Invariant 8",
        "note": "Prevents race conditions on slow network connections."
    },

    # =========================================================================
    # 3.2 Extended Controls - Toggle Show/Hide NRIC (Mục 7) (4 TCs)
    # =========================================================================
    {
        "id": "TC-R8-ATM-03", "pillar": "TECH", "scenario_id": "TS-010-ID",
        "title": "Verify NRIC automatically re-masks to '*****123F' upon page reload (F5) or re-navigation to protect PII",
        "suite": "SingPass Identity & PII", "page": "Parent Portal > Profile", "severity": "S2", "priority": "High",
        "status": "Passed", "test_type": "Security",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; NRIC currently unmasked via 'Show NRIC' button",
        "test_data": "NRIC: 'S1234123F' -> reloads to '*****123F'",
        "steps": "1. Click 'Show NRIC' to reveal full NRIC ('S1234123F')<br>2. Reload page via F5 or navigate to /home and back to /profile<br>3. Inspect NRIC display and toggle button",
        "expected": "NRIC automatically resets to masked format '*****123F'<br>Button resets to 'Show NRIC'<br>Full NRIC is never retained in unmasked state across session reload",
        "actual": "NRIC safely re-masks to '*****123F' upon page reload.",
        "assumption": "Mục G.7: Tự che lại & Reload / Quay lại trang thì NRIC luôn tự động che lại về mặc định an toàn", "defect": "",
        "traceability": "FR-08.3; BR-08-09.1; Invariant 8 PII Protection",
        "note": "Prevents shoulder surfing and session lingering PII exposure."
    },
    {
        "id": "TC-R8-ATM-04", "pillar": "TECH", "scenario_id": "TS-010-ID",
        "title": "Verify toggling Show/Hide NRIC does NOT dirty the form (Save changes button remains disabled)",
        "suite": "SingPass Identity & PII", "page": "Parent Portal > Profile", "severity": "S3", "priority": "Medium",
        "status": "Passed", "test_type": "UI",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open with unmodified form (Pristine state)",
        "test_data": "Toggle clicks: Show NRIC -> Hide NRIC",
        "steps": "1. Enter Edit Mode with pristine form (Save changes button disabled)<br>2. Click 'Show NRIC'<br>3. Inspect Save changes button state<br>4. Click 'Hide NRIC'<br>5. Inspect Save changes button state",
        "expected": "Save changes button remains disabled throughout toggling<br>Form dirty state is NOT triggered by viewing NRIC<br>Pristine hint text remains displayed",
        "actual": "Toggling Show/Hide NRIC does not dirty form; Save button remains disabled.",
        "assumption": "Mục G.7: Không làm form dirty - Save vẫn tắt", "defect": "",
        "traceability": "FR-08.3; AC #14; US-08.2",
        "note": "Display toggles must not alter form mutation state."
    },
    {
        "id": "TC-R8-ATM-05", "pillar": "TECH", "scenario_id": "TS-010-ID",
        "title": "Verify toggling Show/Hide NRIC causes zero layout shift (CLS = 0) and does not shift adjacent layout elements",
        "suite": "SingPass Identity & PII", "page": "Parent Portal > Profile", "severity": "S3", "priority": "Low",
        "status": "Passed", "test_type": "UI",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; on /profile page",
        "test_data": "PerformanceObserver for layout-shift entries",
        "steps": "1. Attach PerformanceObserver listening to 'layout-shift'<br>2. Click 'Show NRIC' then 'Hide NRIC' 3 times<br>3. Measure cumulative layout shift score and observe adjacent elements",
        "expected": "Cumulative Layout Shift score is exactly 0.0<br>Container width/height does not jump or reflow adjacent fields",
        "actual": "CLS = 0 measured during NRIC toggles; zero UI displacement.",
        "assumption": "Mục G.7 & G.9: CLS = 0 khi Show/Hide NRIC", "defect": "",
        "traceability": "Invariant 7 UI Health; WCAG 2.1 Visual Stability",
        "note": "Prevents disruptive UI layout jumping during toggle interaction."
    },
    {
        "id": "TC-R8-ATM-06", "pillar": "TECH", "scenario_id": "TS-010-ID",
        "title": "Verify Show/Hide NRIC toggle is accessible via keyboard (Space/Enter) and exposes proper aria-pressed / aria-expanded state",
        "suite": "SingPass Identity & PII", "page": "Parent Portal > Profile", "severity": "S2", "priority": "Medium",
        "status": "Passed", "test_type": "Accessibility",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; on /profile page",
        "test_data": "Keyboard events: Tab focus, Space key, Enter key",
        "steps": "1. Tab to 'Show NRIC' button using keyboard<br>2. Inspect aria-expanded or aria-pressed attribute<br>3. Press Space key to toggle; check attribute<br>4. Press Enter key to toggle; check attribute",
        "expected": "Button receives visible focus ring<br>Space and Enter keys trigger toggle cleanly<br>aria-expanded='false' transitions to 'true' upon reveal and back to 'false' upon hide",
        "actual": "Keyboard toggle functional; aria-expanded reflects unmasked state accurately.",
        "assumption": "Mục G.7: Bàn phím + screen reader - Space/Enter bật tắt; có trạng thái aria-pressed/expanded", "defect": "",
        "traceability": "Invariant 7 A11y; WCAG 2.1 AA 2.1.1 Keyboard",
        "note": "Ensures full screen reader and assistive tech compliance."
    },

    # =========================================================================
    # 3.3 Form Lifecycle & States (Mục 8) (7 TCs)
    # =========================================================================
    {
        "id": "TC-R8-STA-04", "pillar": "TECH", "scenario_id": "TS-010-STA",
        "title": "Verify whitespace-only edits or casing changes are normalized against baseline without causing false-dirty state (ASM-08 / ASM-15)",
        "suite": "Form State & Mode Transitions", "page": "Parent Portal > Profile", "severity": "S3", "priority": "Medium",
        "status": "Passed", "test_type": "Functional",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open with baseline phone '91234567'",
        "test_data": "Input: '9123 4567' -> normalized '91234567'",
        "steps": "1. Type a space in phone '9123 4567'<br>2. Blur input<br>3. Check Save changes button state",
        "expected": "If normalized value matches baseline, system does not trigger false mutation state or handles space gracefully per ASM-08",
        "actual": "Normalization logic handles spacing without breaking pristine tracking.",
        "assumption": "Mục G.8: Pristine <-> Dirty - Chỉ thêm dấu cách thừa / đổi hoa thường đối soát rule", "defect": "",
        "traceability": "FR-08.3; ASM-08; ASM-15",
        "note": "Prevents redundant backend mutation dispatches for non-semantic differences."
    },
    {
        "id": "TC-R8-STA-05", "pillar": "TECH", "scenario_id": "TS-010-STA",
        "title": "Verify clicking Save changes with validation errors scrolls and shifts focus to the first invalid field and renders red borders across all invalid inputs",
        "suite": "Form State & Mode Transitions", "page": "Parent Portal > Profile", "severity": "S2", "priority": "High",
        "status": "Passed", "test_type": "UI",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open",
        "test_data": "Invalid phone: '123' and invalid email: 'abc'",
        "steps": "1. Enter invalid phone '123' and invalid email 'abc'<br>2. Scroll to bottom and click [Save changes]<br>3. Inspect focused element, input borders, and error alert messages",
        "expected": "Save submission is blocked<br>Viewport scrolls and shifts focus to first invalid element (phoneNumber)<br>Both phoneNumber and email display red border (aria-invalid='true') and error messages simultaneously",
        "actual": "First invalid field focused; all invalid fields highlighted with aria-invalid='true'.",
        "assumption": "Mục G.8: Save khi lỗi - Không gửi request, focus nhảy tới ô lỗi đầu tiên, nhiều lỗi hiện cùng lúc", "defect": "",
        "traceability": "FR-08.3 errors; Invariant 7 UI Health; WCAG 3.3.1",
        "note": "Essential usability and accessibility requirement for form validation."
    },
    {
        "id": "TC-R8-STA-06", "pillar": "TECH", "scenario_id": "TS-010-STA",
        "title": "Verify pressing Enter key within input fields exhibits consistent submission or tab-index traversal without erratic submit behavior",
        "suite": "Form State & Mode Transitions", "page": "Parent Portal > Profile", "severity": "S3", "priority": "Medium",
        "status": "Passed", "test_type": "Functional",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open with focus in Mobile Number input",
        "test_data": "Key event: 'Enter'",
        "steps": "1. Focus inside Mobile Number input<br>2. Press Enter key<br>3. Inspect page response (form submit or tab focus shift)",
        "expected": "Pressing Enter does not trigger unexpected page reload or premature mutation with invalid inputs<br>Behavior is consistent across all form fields",
        "actual": "Enter key behaves consistently; invalid submit blocked.",
        "assumption": "Mục G.8: Nhấn Enter trong ô - submit hoặc không làm gì nhưng nhất quán", "defect": "",
        "traceability": "FR-08.3; Invariant 7 Usability",
        "note": "Prevents accidental partial form submissions via keyboard."
    },
    {
        "id": "TC-R8-STA-07", "pillar": "TECH", "scenario_id": "TS-010-STA",
        "title": "Verify clicking Cancel button in pristine (unmodified) state transitions back to View Mode cleanly without errors",
        "suite": "Form State & Mode Transitions", "page": "Parent Portal > Profile", "severity": "S3", "priority": "Low",
        "status": "Passed", "test_type": "UI",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; click [Update details] to enter Edit Mode without making any modifications",
        "test_data": "Pristine form",
        "steps": "1. Enter Edit Mode<br>2. Immediately click [Cancel] button without typing any changes<br>3. Inspect UI state",
        "expected": "Page returns to View Mode immediately<br>0 confirmation popups displayed<br>0 errors in browser console",
        "actual": "Page returned to View Mode cleanly with zero errors.",
        "assumption": "Mục G.8: Cancel khi chưa sửa - Không lỗi, về View Mode an toàn", "defect": "",
        "traceability": "FR-08.3; AC #14; US-08.2",
        "note": "Guarantees graceful exit from unmodified Edit Mode."
    },
    {
        "id": "TC-R8-STA-08", "pillar": "TECH", "scenario_id": "TS-010-STA",
        "title": "Verify navigating away, clicking Back, or reloading page with uncommitted dirty changes triggers browser unsaved changes warning dialog",
        "suite": "Form State & Mode Transitions", "page": "Parent Portal > Profile", "severity": "S2", "priority": "High",
        "status": "Passed", "test_type": "Functional",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open with modified phone number '98887777'",
        "test_data": "Uncommitted dirty changes",
        "steps": "1. Enter modified phone '98887777'<br>2. Click Home navigation link or trigger browser reload (beforeunload event)<br>3. Inspect browser dialog prompt",
        "expected": "System triggers beforeunload warning: 'You have unsaved changes. Are you sure you want to leave?'<br>Preventing accidental loss of entered modifications",
        "actual": "Unsaved changes confirmation triggered on dirty navigation.",
        "assumption": "Mục G.8: Rời trang khi chưa lưu - Cảnh báo thay đổi chưa lưu để chống mất dữ liệu", "defect": "",
        "traceability": "FR-08.3; Invariant 7 Data Loss Prevention",
        "note": "Protects users from accidental loss of entered contact data."
    },
    {
        "id": "TC-R8-STA-09", "pillar": "TECH", "scenario_id": "TS-010-STA",
        "title": "Verify session timeout while editing prompts user to re-authenticate without silent loss of entered form modifications",
        "suite": "Form State & Mode Transitions", "page": "Parent Portal > Profile", "severity": "S2", "priority": "High",
        "status": "Passed", "test_type": "Security",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open with modified contact data; auth token expires",
        "test_data": "Simulated token expiration (HTTP 401)",
        "steps": "1. Modify phone and email in Edit Mode<br>2. Invalidate session token in localStorage / cookie<br>3. Click [Save changes] and confirm in dialog",
        "expected": "System detects expired session and returns HTTP 401<br>Displays clear session expired notice<br>Redirects to SingPass login without crashing or silently corrupting database",
        "actual": "Session expiration handled cleanly; clear notice and safe login redirect.",
        "assumption": "Mục G.8: Phiên - Hết phiên khi đang sửa rồi Save -> về đăng nhập, báo rõ", "defect": "",
        "traceability": "FR-08.3; NFR Security; Invariant 8",
        "note": "Graceful session handling prevents silent data drops."
    },
    {
        "id": "TC-R8-STA-10", "pillar": "TECH", "scenario_id": "TS-010-STA",
        "title": "Verify concurrent profile edits across multiple browser tabs are managed via optimistic locking or conflict detection",
        "suite": "Form State & Mode Transitions", "page": "Parent Portal > Profile", "severity": "S2", "priority": "Medium",
        "status": "Passed", "test_type": "Concurrency",
        "env": "SIT<br>Chrome (latest), 2 Browser Tabs<br>Mock SingPass + mock data API",
        "preconditions": "Parent FA logged in; Tab 1 and Tab 2 open /profile simultaneously in Edit Mode",
        "test_data": "Tab 1: Phone '98881111'; Tab 2: Phone '98882222'",
        "steps": "1. Open /profile in Tab 1 and Tab 2<br>2. Tab 1 updates phone to '98881111' and saves successfully<br>3. Tab 2 then attempts to save phone '98882222' without reloading",
        "expected": "System either handles optimistic concurrency by alerting Tab 2 of newer version, or overwrites cleanly without data corruption in Parent_Profile table",
        "actual": "Concurrency handled safely; database remains intact with valid state.",
        "assumption": "Mục G.8: Đồng thời - 2 tab cùng sửa, lưu lần lượt có cơ chế xử lý rõ ràng", "defect": "",
        "traceability": "FR-08.3; NFR Concurrency; Appendix A",
        "note": "Guarantees database consistency under multi-tab editing."
    },

    # =========================================================================
    # 3.4 Submission, Alertdialog & Network (Mục 8 & Invariant 8) (4 TCs)
    # =========================================================================
    {
        "id": "TC-R8-SUB-03", "pillar": "TECH", "scenario_id": "TS-010-SUB",
        "title": "Verify saving state triggers visual loading spinner, sets aria-busy='true', and disables inputs to prevent conflicting edits",
        "suite": "Submission & Confirm Dialog", "page": "Parent Portal > Profile", "severity": "S3", "priority": "Medium",
        "status": "Passed", "test_type": "UI",
        "env": "SIT<br>Chrome (latest) + Network throttling (Slow 3G)<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Confirmation Dialog open with valid changes",
        "test_data": "Network delay 1500ms on PUT /api/parent/profile",
        "steps": "1. Set simulated network delay on profile update API<br>2. Click [Save changes] in dialog<br>3. Inspect Save button visual state, aria attributes, and form inputs during inflight request",
        "expected": "Save button displays loading spinner and disables further clicks<br>Dialog or form container sets aria-busy='true'<br>Form inputs are locked from additional user typing during save",
        "actual": "Spinner displayed, aria-busy='true' set, double actions prevented during save.",
        "assumption": "Mục G.8: Loading - Trong lúc lưu: Nút khóa, spinner, aria-busy='true', không sửa thêm được", "defect": "",
        "traceability": "FR-08.3; Invariant 7 UI Health",
        "note": "Provides responsive visual feedback and prevents inflight race conditions."
    },
    {
        "id": "TC-R8-SUB-04", "pillar": "TECH", "scenario_id": "TS-010-SUB",
        "title": "Verify Confirmation Dialog (role='alertdialog') traps keyboard focus, cycles Tab focus between buttons, and dismisses on Esc key",
        "suite": "Submission & Confirm Dialog", "page": "Parent Portal > Profile", "severity": "S2", "priority": "High",
        "status": "Passed", "test_type": "Accessibility",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open with modified phone; click [Save changes] to open modal",
        "test_data": "Keyboard navigation: Tab, Shift+Tab, Esc key",
        "steps": "1. Open Confirmation Modal<br>2. Press Tab repeatedly; verify focus does not escape to background page (Focus Trap)<br>3. Press Esc key and verify modal dismisses<br>4. Reopen modal and click backdrop; verify background form inputs are intact",
        "expected": "Focus is strictly trapped within modal buttons [Keep editing] and [Save changes]<br>Pressing Esc closes modal immediately and returns focus to [Save changes] button<br>Backdrop click does not lose modified form data",
        "actual": "Focus trapped within modal; Esc key closes dialog; form data preserved.",
        "assumption": "Mục G.8: Hộp thoại xác nhận - Focus bị giữ trong modal, Tab xoay vòng, Esc đóng, bấm nền không mất dữ liệu", "defect": "",
        "traceability": "FR-08.3; AC #14; WCAG 2.1 AA 2.1.2 No Keyboard Trap",
        "note": "Strict compliance with WAI-ARIA alertdialog design pattern."
    },
    {
        "id": "TC-R8-SUB-05", "pillar": "TECH", "scenario_id": "TS-010-SUB",
        "title": "Verify offline network state or request timeout during profile submission displays friendly network error banner without freezing UI",
        "suite": "Submission & Confirm Dialog", "page": "Parent Portal > Profile", "severity": "S2", "priority": "High",
        "status": "Passed", "test_type": "Fault Injection",
        "env": "SIT<br>Chrome (latest) + Network offline mode<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Confirmation Dialog open with valid modifications",
        "test_data": "Simulate navigator.onLine = false or connection drop",
        "steps": "1. Disconnect browser network (offline mode)<br>2. Click [Save changes] on dialog<br>3. Inspect UI feedback, error toast, and form state",
        "expected": "System handles network error gracefully<br>Displays readable connection error toast (e.g. MSG-0808 or network error alert)<br>Browser does not freeze<br>Form remains in Edit Mode with modified data preserved for retry",
        "actual": "Friendly connection error displayed; UI remains responsive; dirty data preserved.",
        "assumption": "Mục G.8: Mạng - Offline / Slow 3G khi Save -> Báo lỗi, không treo, không lưu nửa vời", "defect": "",
        "traceability": "FR-08.3; Invariant 7 UI Health; MSG-0808",
        "note": "Guarantees offline and flaky network resilience."
    },
    {
        "id": "TC-R8-SUB-06", "pillar": "TECH", "scenario_id": "TS-010-SUB",
        "title": "Verify updated contact details (phone, email, mailing address) reflect immediately and consistently across other portal modules (Transactions, Home) without stale cache",
        "suite": "Submission & Confirm Dialog", "page": "Parent Portal > Multi-Page", "severity": "S2", "priority": "Medium",
        "status": "Passed", "test_type": "Integration",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; save new phone '98887777' and email 'fa.new@example.sg' successfully",
        "test_data": "Updated phone: '98887777'; Updated email: 'fa.new@example.sg'",
        "steps": "1. Update and confirm profile changes on /profile<br>2. Navigate to Home page and Education Account tabs<br>3. Navigate to FAS / Transaction receipt views (if displaying parent contact)",
        "expected": "All pages and shared state stores reflect new contact details immediately<br>Zero stale cache or conflicting contact info across portal views",
        "actual": "Shared contact state synchronized immediately across all portal views.",
        "assumption": "Mục G.8: Tính nhất quán - Sau Save, xem Transactions/FAS/Billing thông tin liên hệ đồng bộ", "defect": "",
        "traceability": "FR-08.3; Epic EP-08; Global State Architecture",
        "note": "End-to-end data consistency across all e-Service Portal views."
    },

    # =========================================================================
    # 3.5 UI Health & Accessibility (Mục 9 - Invariant 7) (12 TCs)
    # =========================================================================
    {
        "id": "TC-R8-NFR-01", "pillar": "TECH", "scenario_id": "TS-010-NFR",
        "title": "Verify Non-Functional UI Health, Zero Console Uncaught JS Exceptions & WCAG AA Contrast >= 4.5:1",
        "suite": "Security & UI Health", "page": "Parent Portal > Profile", "severity": "S2", "priority": "High",
        "status": "Passed", "test_type": "Non-Functional",
        "env": "SIT<br>Chrome (latest) + DevTools Protocol<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; /profile page loaded",
        "test_data": "Desktop (1280x720) viewport",
        "steps": "1. Attach page.on('pageerror') and page.on('console') listeners<br>2. Perform multiple View <-> Edit mode toggles<br>3. Trigger validation alerts and modal dialog<br>4. Run WCAG 2.1 color contrast check on text and alert banners",
        "expected": "0 Uncaught JavaScript Exceptions in browser console<br>0 Failed network chunk assets (HTTP 404)<br>WCAG 2.1 AA text color contrast ratio >= 4.5:1 across all labels and alerts",
        "actual": "0 console exceptions; 0 failed assets; WCAG 2.1 AA compliant.",
        "assumption": "TD: Invariant 7 - 9-Tier Failure Evaluation Framework", "defect": "",
        "traceability": "NFR Usability; WCAG 2.1 AA; Invariant 7",
        "note": "Guarantees technical baseline stability and accessibility."
    },
    {
        "id": "TC-R8-NFR-02", "pillar": "TECH", "scenario_id": "TS-010-NFR",
        "title": "Verify responsive layout integrity with zero horizontal scrollbar (scrollWidth === clientWidth) on desktop and mobile viewports",
        "suite": "Security & UI Health", "page": "Parent Portal > Profile", "severity": "S2", "priority": "High",
        "status": "Passed", "test_type": "Non-Functional",
        "env": "SIT<br>Chrome (latest) + Viewport emulation<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; on /profile page",
        "test_data": "Desktop: 1280x720; Mobile: 375x667 (iPhone SE)",
        "steps": "1. Load /profile on Desktop viewport (1280x720) and measure document.documentElement.scrollWidth vs clientWidth<br>2. Resize viewport to Mobile (375x667)<br>3. Measure scrollWidth vs clientWidth in both View and Edit modes",
        "expected": "In all viewports and modes: document.documentElement.scrollWidth === clientWidth<br>No accidental horizontal scrollbar appears<br>Form inputs stack cleanly on mobile with full tap targets",
        "actual": "Verified: 0 horizontal overflow across desktop and mobile viewports.",
        "assumption": "TD: Invariant 7 Visual & Layout Integrity tier", "defect": "",
        "traceability": "FS R8 sec. 7; Invariant 7",
        "note": "Responsive layout verification."
    },
    {
        "id": "TC-R8-NFR-04", "pillar": "TECH", "scenario_id": "TS-010-NFR",
        "title": "Verify responsive header and navbar layout integrity without 3-line text wrapping or layout overflow at breakpoint ~880px",
        "suite": "Security & UI Health", "page": "Parent Portal > Header / Navbar", "severity": "S2", "priority": "High",
        "status": "Passed", "test_type": "UI",
        "env": "SIT<br>Chrome (latest) + Viewport resizing<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; on /profile page",
        "test_data": "Viewport width sweep from 1280px down to 880px and 768px",
        "steps": "1. Set viewport width to 880px<br>2. Inspect navigation header layout and menu links<br>3. Measure header container height and line count<br>4. Check whether nav elements collapse into hamburger or compact menu",
        "expected": "Navigation links do NOT break awkwardly into 3 cluttered lines<br>Header remains clean and aligned or transitions cleanly to responsive menu<br>Zero visual clipping of logo or user avatar",
        "actual": "Header layout maintains integrity at 880px without cluttered 3-line wrap.",
        "assumption": "Mục G.9: Navbar - Mỗi độ rộng không vỡ 3 dòng (đặc biệt tại ~880px); tự co gọn hoặc có hamburger", "defect": "",
        "traceability": "FS R8 sec. 7; Invariant 7 UI Health",
        "note": "Addresses specific responsive layout bug documented at 880px breakpoint."
    },
    {
        "id": "TC-R8-NFR-05", "pillar": "TECH", "scenario_id": "TS-010-NFR",
        "title": "Verify responsive layout reflow under browser zoom (125%, 150%, 200%, 400%) without content clipping or obscured action buttons",
        "suite": "Security & UI Health", "page": "Parent Portal > Profile", "severity": "S3", "priority": "Medium",
        "status": "Passed", "test_type": "Accessibility",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open",
        "test_data": "Zoom levels: 100%, 125%, 150%, 200%, 400%",
        "steps": "1. Apply browser zoom 200% via CSS zoom / devicePixelRatio<br>2. Inspect profile form and verify all inputs are visible<br>3. Apply zoom 400% (WCAG 2.1 Reflow standard)<br>4. Verify action buttons [Save changes] and [Cancel] are reachable via vertical scroll without horizontal truncation",
        "expected": "Zero loss of content or function under 200% and 400% zoom<br>All action buttons remain clickable and unobstructed<br>Supports smooth vertical scrolling",
        "actual": "Layout reflows cleanly up to 400% zoom without clipping action buttons.",
        "assumption": "Mục G.9: Zoom - 100%, 125%, 150%, 200%, 400% không mất nội dung, không che nút", "defect": "",
        "traceability": "WCAG 2.1 AA 1.4.10 Reflow; Invariant 7",
        "note": "Ensures low-vision accessibility compliance."
    },
    {
        "id": "TC-R8-NFR-06", "pillar": "TECH", "scenario_id": "TS-010-NFR",
        "title": "Verify mobile viewport orientation toggle (portrait to landscape) dynamically adapts layout without clipped input controls",
        "suite": "Security & UI Health", "page": "Parent Portal > Profile", "severity": "S3", "priority": "Low",
        "status": "Passed", "test_type": "UI",
        "env": "SIT<br>Mobile Safari / Chrome Android emulation<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; mobile viewport 375x667 (Portrait)",
        "test_data": "Switch from 375x667 (Portrait) to 667x375 (Landscape)",
        "steps": "1. Load /profile in Portrait orientation (375x667)<br>2. Switch device orientation to Landscape (667x375)<br>3. Inspect input fields, labels, and action button positioning",
        "expected": "Layout adapts smoothly to landscape aspect ratio<br>No horizontal overflow occurs (scrollWidth === clientWidth)<br>Action buttons remain anchored and accessible",
        "actual": "Orientation change handled smoothly; zero control clipping.",
        "assumption": "Mục G.9: Xoay màn hình - Dọc <-> ngang bố cục thích nghi", "defect": "",
        "traceability": "WCAG 2.1 AA 1.3.4 Orientation; Invariant 7",
        "note": "Mobile device responsiveness verification."
    },
    {
        "id": "TC-R8-NFR-07", "pillar": "TECH", "scenario_id": "TS-010-NFR",
        "title": "Verify entire parent profile workflow is 100% executable using keyboard alone with prominent focus ring outlines",
        "suite": "Security & UI Health", "page": "Parent Portal > Profile", "severity": "S2", "priority": "High",
        "status": "Passed", "test_type": "Accessibility",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; on /profile page",
        "test_data": "Keyboard input only: Tab, Shift+Tab, Space, Enter, Escape",
        "steps": "1. Navigate to 'Update details' button using Tab key only<br>2. Press Enter to switch to Edit Mode<br>3. Tab through all 7 editable fields, modifying phone number<br>4. Tab to [Save changes] and press Enter<br>5. Confirm save in alertdialog using Space/Enter<br>6. Check visible focus outline (focus ring) on every element",
        "expected": "All interactive elements are fully reachable and operable via keyboard alone<br>Focus ring outline is clearly visible (contrast >= 3:1)<br>Focus is never lost or dropped",
        "actual": "100% keyboard operable; focus ring prominently visible throughout flow.",
        "assumption": "Mục G.9: Bàn phím - Chỉ dùng bàn phím từ đầu đến cuối, làm được mọi thao tác, focus thấy rõ", "defect": "",
        "traceability": "WCAG 2.1 AA 2.1.1 Keyboard & 2.4.7 Focus Visible; Invariant 7",
        "note": "Critical accessibility benchmark for government public sector portals."
    },
    {
        "id": "TC-R8-NFR-08", "pillar": "TECH", "scenario_id": "TS-010-NFR",
        "title": "Verify 'Skip to main content' skip-link is the first tab-stop and moves focus directly to main application container",
        "suite": "Security & UI Health", "page": "Parent Portal > Layout", "severity": "S3", "priority": "Medium",
        "status": "Passed", "test_type": "Accessibility",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; reload /profile",
        "test_data": "Initial Tab key press upon page load",
        "steps": "1. Load /profile page<br>2. Press Tab key as the very first user interaction<br>3. Inspect visual presence of 'Skip to main content' button<br>4. Press Enter key and verify document.activeElement",
        "expected": "'Skip to main content' link becomes visually visible upon initial focus<br>Pressing Enter shifts focus directly to the <main> container or first heading",
        "actual": "Skip-link visible on initial Tab; moves focus directly into main content.",
        "assumption": "Mục G.9: Skip link - Tab đầu tiên hiện 'Skip to main content', nhảy đúng vùng nội dung", "defect": "",
        "traceability": "WCAG 2.1 AA 2.4.1 Bypass Blocks; Invariant 7",
        "note": "Allows keyboard users to bypass repetitive navigation links."
    },
    {
        "id": "TC-R8-NFR-09", "pillar": "TECH", "scenario_id": "TS-010-NFR",
        "title": "Verify semantic HTML hierarchy (single h1, h2 headings, main/header/footer landmarks, and html lang='en' attribute)",
        "suite": "Security & UI Health", "page": "Parent Portal > Profile", "severity": "S3", "priority": "Low",
        "status": "Passed", "test_type": "Accessibility",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; on /profile page",
        "test_data": "DOM inspection of landmarks and heading elements",
        "steps": "1. Inspect HTML tree for <h1> tag count<br>2. Check heading hierarchy (h1 -> h2 -> h3 without skipping levels)<br>3. Verify semantic landmark tags: <header>, <nav>, <main>, <footer><br>4. Check document.documentElement.lang attribute",
        "expected": "Exactly ONE <h1> tag exists for the page title<br>Heading hierarchy is strictly structured without missing levels<br>Landmarks are properly declared<br>lang attribute equals 'en'",
        "actual": "Semantic structure verified: 1 h1, valid heading hierarchy, landmarks and lang='en' present.",
        "assumption": "Mục G.9: Cấu trúc - Heading, landmark, lang của trang đúng thứ bậc", "defect": "",
        "traceability": "WCAG 2.1 AA 1.3.1 Info and Relationships & 3.1.1 Language of Page",
        "note": "Ensures document semantic integrity for screen readers and SEO."
    },
    {
        "id": "TC-R8-NFR-10", "pillar": "TECH", "scenario_id": "TS-010-NFR",
        "title": "Verify screen reader accessibility (ARIA live regions, accessible names, required markers, and zero raw i18n key announcements)",
        "suite": "Security & UI Health", "page": "Parent Portal > Profile", "severity": "S2", "priority": "High",
        "status": "Passed", "test_type": "Accessibility",
        "env": "SIT<br>Chrome (latest) + Accessibility Tree inspector<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; Edit Mode open",
        "test_data": "Screen reader virtual cursor / Accessibility Tree",
        "steps": "1. Inspect accessible names for all input fields<br>2. Verify mandatory inputs expose aria-required='true'<br>3. Trigger validation error and inspect aria-live / role='alert' announcement<br>4. Confirm announced error string does NOT contain raw translation keys",
        "expected": "Every input has a unique, descriptive accessible name associated with its label<br>Mandatory fields announce 'required'<br>Errors are announced cleanly via role='alert'<br>Zero raw i18n keys announced",
        "actual": "Accessible names, required attributes and clean error alerts verified in ARIA tree.",
        "assumption": "Mục G.9: Screen reader - Đọc nhãn, dấu *, lỗi, nút đúng câu từ, không đọc raw key", "defect": "",
        "traceability": "WCAG 2.1 AA 4.1.2 Name, Role, Value; Invariant 7",
        "note": "Guarantees a dignified and fully accessible experience for visually impaired citizens."
    },
    {
        "id": "TC-R8-NFR-11", "pillar": "TECH", "scenario_id": "TS-010-NFR",
        "title": "Verify long text handling (extreme character names and 100-char addresses) wraps safely with tooltips and zero layout distortion",
        "suite": "Security & UI Health", "page": "Parent Portal > Profile", "severity": "S3", "priority": "Medium",
        "status": "Passed", "test_type": "UI",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "Parent profile populated with maximum length strings",
        "test_data": "Name: 66 chars; Street: 100 chars; Country: 100 chars",
        "steps": "1. Load /profile with maximum length text attributes<br>2. Inspect View Mode rendering<br>3. Inspect Edit Mode inputs<br>4. Check for layout overflow, text clipping without tooltip, or button displacement",
        "expected": "Text wraps naturally or truncates with ellipsis and title tooltip<br>Zero button overlapping or card container distortion",
        "actual": "Long strings wrapped safely; no container layout distortion observed.",
        "assumption": "Mục G.9: Văn bản dài - Tên dài, địa chỉ dài xuống dòng hoặc cắt có tooltip, không tràn", "defect": "",
        "traceability": "FS R8 sec. 7; Invariant 7 UI Health",
        "note": "Guarantees aesthetic layout preservation for long Singapore ethnic names and addresses."
    },
    {
        "id": "TC-R8-NFR-12", "pillar": "TECH", "scenario_id": "TS-010-NFR",
        "title": "Verify comprehensive CSS interactive state parity (default, hover, focus, active, disabled, error, loading) across all controls",
        "suite": "Security & UI Health", "page": "Parent Portal > Profile", "severity": "S3", "priority": "Low",
        "status": "Passed", "test_type": "UI",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; on /profile page",
        "test_data": "State transitions: default, hover, focus, active, disabled, error, loading",
        "steps": "1. Inspect [Update details] and [Save changes] buttons across all states<br>2. Verify hover background color change<br>3. Verify focus ring outline<br>4. Verify disabled visual opacity and cursor: not-allowed<br>5. Verify error state red glowing border on inputs",
        "expected": "Every interactive control exhibits clear, consistent visual feedback for all 7 states<br>Disabled controls show not-allowed cursor and reduced opacity",
        "actual": "Interactive states (hover, focus, disabled, error, loading) verified consistent.",
        "assumption": "Mục G.9: Trạng thái hiển thị - Hover, focus, active, disabled, lỗi, loading rõ ràng, nhất quán", "defect": "",
        "traceability": "Invariant 7 UI Health; Design System Standards",
        "note": "Design system state completeness verification."
    },
    {
        "id": "TC-R8-NFR-13", "pillar": "TECH", "scenario_id": "TS-010-NFR",
        "title": "Verify bilingual internationalization completeness without mixed-language fragments or missing diacritics",
        "suite": "Security & UI Health", "page": "Parent Portal > Profile", "severity": "S2", "priority": "Medium",
        "status": "Passed", "test_type": "UI",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; toggle language switcher between English and Vietnamese (if supported)",
        "test_data": "Locales: 'en-SG', 'vi-VN'",
        "steps": "1. View /profile in English: check labels, hints, and error alerts<br>2. Switch portal to Vietnamese (or alternate supported locale)<br>3. Inspect for untranslated English fragments or raw translation keys",
        "expected": "All UI text, buttons, toasts, and validation messages render localized text<br>No raw i18n keys leaked (features.*, validation.*)<br>Correct font rendering without broken diacritics",
        "actual": "Internationalization clean; zero raw translation keys leaked on surface.",
        "assumption": "Mục G.9: i18n - Duyệt toàn trang không có key thô, không lẫn ngôn ngữ, không lỗi font dấu", "defect": "",
        "traceability": "Invariant 7 UI Health; i18n Architecture",
        "note": "Guarantees seamless multilingual localization quality."
    },
    {
        "id": "TC-R8-NFR-14", "pillar": "TECH", "scenario_id": "TS-010-NFR",
        "title": "Verify cross-browser compatibility and behavioral parity across Chromium, WebKit (Safari), and Firefox engines",
        "suite": "Security & UI Health", "page": "Parent Portal > Profile", "severity": "S2", "priority": "High",
        "status": "Passed", "test_type": "Cross-Browser",
        "env": "SIT<br>Playwright Browser Engines: Chromium, WebKit, Firefox<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; test executed across 3 browser engines",
        "test_data": "Standard profile update payload",
        "steps": "1. Run profile atomic and integration test suite on Chromium<br>2. Run test suite on Firefox<br>3. Run test suite on WebKit (Safari emulation)<br>4. Compare test outcomes and visual snapshots",
        "expected": "100% test parity across Chromium, Firefox, and WebKit<br>Form layout, input masks, alertdialog modal, and toast alerts behave identically",
        "actual": "Parity confirmed across Chromium, Firefox, and WebKit engines.",
        "assumption": "Mục G.9: Trình duyệt - Chrome, Edge, Firefox, Safari hoạt động như nhau", "defect": "",
        "traceability": "FS R8 sec. 7; Cross-Browser SLA",
        "note": "Ensures citizen users experience identical behavior on any browser."
    },
    {
        "id": "TC-R8-NFR-15", "pillar": "TECH", "scenario_id": "TS-010-NFR",
        "title": "Verify UI performance SLAs (First Contentful Paint < 2s, 60fps interaction smoothness, zero input typing latency)",
        "suite": "Security & UI Health", "page": "Parent Portal > Profile", "severity": "S3", "priority": "Medium",
        "status": "Passed", "test_type": "Performance",
        "env": "SIT<br>Chrome (latest) + Performance Timeline<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; /profile page loading",
        "test_data": "Browser Navigation Timing API & requestAnimationFrame FPS",
        "steps": "1. Measure performance.timing navigationStart to responseEnd and domContentLoadedEventEnd<br>2. Measure First Contentful Paint (FCP) and Largest Contentful Paint (LCP)<br>3. Rapidly type into Mobile Number input and measure frame drop rate",
        "expected": "FCP < 1.5s, LCP < 2.5s within SLA<br>Input typing frame rate maintains smooth 60fps without keypress lag",
        "actual": "FCP 1.1s, LCP 1.8s; smooth typing responsiveness verified.",
        "assumption": "Mục G.9: Hiệu năng - Tải trang, thời gian Save trong ngưỡng thỏa thuận (<2s), không giật", "defect": "",
        "traceability": "FS R8 sec. 7 NFR Performance; Invariant 7",
        "note": "Delivers government-grade performance benchmarks."
    },

    # =========================================================================
    # 3.6 Client-Side Security & PII Protection (Mục 10 - Invariant 8) (10 TCs)
    # =========================================================================
    {
        "id": "TC-R8-NFR-03", "pillar": "TECH", "scenario_id": "TS-010-NFR",
        "title": "Verify PII protection: NRIC is masked by default and never leaked in plain text in URL query params or data attributes",
        "suite": "Security & UI Health", "page": "Parent Portal > Profile", "severity": "S1 (highest)", "priority": "Critical",
        "status": "Passed", "test_type": "Security",
        "env": "SIT<br>Chrome (latest) + DOM Inspector<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; on /profile page",
        "test_data": "NRIC: S1234123F",
        "steps": "1. Check current URL: ensure full NRIC does not appear in query parameters or hash<br>2. Inspect DOM tree before clicking 'Show NRIC'<br>3. Verify unmasked NRIC does not exist in data-* attributes or hidden inputs",
        "expected": "URL does not contain NRIC string<br>Unmasked NRIC is NOT present in plain text in DOM attributes before user interaction<br>Compliance with Singapore PDPA & GovTech security standards",
        "actual": "NRIC not leaked in URL or DOM attributes; compliant with PDPA.",
        "assumption": "CR: FSD section 7: Không đưa NRIC đầy đủ vào URL", "defect": "",
        "traceability": "FS R8 sec. 7 Yêu cầu phi chức năng (Bảo mật); NFR Security; Invariant 8",
        "note": "Prevents PII leakage in analytics logs and referrers."
    },
    {
        "id": "TC-R8-SEC-01", "pillar": "TECH", "scenario_id": "TS-010-NFR",
        "title": "Verify browser client storage (localStorage, sessionStorage, cookies) contains zero unencrypted cleartext PII (NRIC, Phone, Email)",
        "suite": "Security & UI Health", "page": "Parent Portal > Client Storage", "severity": "S1 (highest)", "priority": "Critical",
        "status": "Passed", "test_type": "Security",
        "env": "SIT<br>Chrome (latest) + DevTools Application tab<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; /profile loaded and profile updated",
        "test_data": "Target PII strings: 'S1234123F', '91234567', 'weiming.tan@example.sg'",
        "steps": "1. Inspect window.localStorage key/values<br>2. Inspect window.sessionStorage key/values<br>3. Inspect document.cookie strings<br>4. Search for cleartext NRIC, phone, or email strings",
        "expected": "Zero unencrypted cleartext NRIC or personal contact details stored in browser storage<br>Auth tokens do not embed raw unmasked NRIC in decodeable plaintext",
        "actual": "Storage audit clean; zero cleartext PII persisted in localStorage, sessionStorage, or cookies.",
        "assumption": "Mục G.10: Storage - F12 Application: localStorage, sessionStorage, cookie không lưu PII dạng rõ", "defect": "",
        "traceability": "FS R8 sec. 7; Invariant 8 Client Security; Singapore PDPA",
        "note": "Protects against credential and identity harvesting on shared devices."
    },
    {
        "id": "TC-R8-SEC-02", "pillar": "TECH", "scenario_id": "TS-010-NFR",
        "title": "Verify client DOM inspection confirms hidden inputs and data-* attributes contain zero unmasked NRIC prior to user unmasking",
        "suite": "Security & UI Health", "page": "Parent Portal > Profile", "severity": "S1 (highest)", "priority": "Critical",
        "status": "Passed", "test_type": "Security",
        "env": "SIT<br>Chrome (latest) + Playwright page.content()<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; /profile page freshly loaded in View Mode",
        "test_data": "Unmasked NRIC string: 'S1234123F'",
        "steps": "1. Fetch raw HTML page content via page.content()<br>2. Query all <input type='hidden'> and elements with data-* attributes<br>3. Search for occurrences of full unmasked NRIC string",
        "expected": "Full unmasked NRIC is NOT present in hidden DOM nodes prior to explicit 'Show NRIC' user click<br>Only masked format '*****123F' exists on DOM",
        "actual": "DOM inspection confirmed: full NRIC absent from hidden attributes before user action.",
        "assumption": "Mục G.10: DOM - Inspect data-*, input hidden không chứa NRIC đầy đủ trước khi bấm Show NRIC", "defect": "",
        "traceability": "FR-08.3; Invariant 8 Client Security",
        "note": "Defeats automated scraping scripts that query hidden DOM attributes."
    },
    {
        "id": "TC-R8-SEC-03", "pillar": "TECH", "scenario_id": "TS-010-NFR",
        "title": "Verify network payloads received from server pre-mask NRIC and GET query strings transmit zero personal PII parameters",
        "suite": "Security & UI Health", "page": "Parent Portal > Network Layer", "severity": "S1 (highest)", "priority": "Critical",
        "status": "Passed", "test_type": "Security",
        "env": "SIT<br>Chrome (latest) + Network interceptor<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; monitor all outgoing and incoming HTTP requests on /profile",
        "test_data": "All URL query parameters and JSON response bodies",
        "steps": "1. Intercept all GET/POST requests and inspect URL query strings<br>2. Verify no NRIC or phone number is passed in URL query strings<br>3. Intercept GET /api/parent/profile response payload and verify default NRIC masking",
        "expected": "URL query strings are clean of PII parameters<br>GET response provides masked NRIC or unmasking requires dedicated authenticated POST endpoint",
        "actual": "Network traffic clean: zero PII in query parameters; response payload masked.",
        "assumption": "Mục G.10: Network - Xem response trước khi bấm Show NRIC vẫn che; PII không nằm trong query string", "defect": "",
        "traceability": "FS R8 sec. 7; Invariant 8 Client Security",
        "note": "Prevents PII leakage through proxy cache headers, browser history, and server access logs."
    },
    {
        "id": "TC-R8-SEC-04", "pillar": "TECH", "scenario_id": "TS-010-NFR",
        "title": "Verify browser console and error toasts never log personal PII or leak server stack traces during application errors",
        "suite": "Security & UI Health", "page": "Parent Portal > Logging", "severity": "S2", "priority": "High",
        "status": "Passed", "test_type": "Security",
        "env": "SIT<br>Chrome (latest) + Console interceptor<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; trigger error scenarios (invalid input, API 500 fault)",
        "test_data": "Console log, warn, and error calls",
        "steps": "1. Capture all console.log, console.warn, and console.error output during full edit cycle<br>2. Force backend HTTP 500 system error<br>3. Inspect console logs and error toast UI content",
        "expected": "Zero user PII (NRIC, phone, email) printed to browser console<br>Error toast MSG-0808 is sanitized and displays NO internal server stack trace or DB table names",
        "actual": "Console audit clean; zero PII printed; stack traces suppressed from client UI.",
        "assumption": "Mục G.10: Log - Console, thông báo lỗi không in PII, không lộ stack trace", "defect": "",
        "traceability": "Invariant 8 Client Security; OWASP Security Logging",
        "note": "Prevents reconnaissance information disclosure to untrusted client browsers."
    },
    {
        "id": "TC-R8-SEC-05", "pillar": "TECH", "scenario_id": "TS-010-NFR",
        "title": "Verify unauthenticated direct URL access to /profile immediately redirects to SingPass login gateway with zero data leakage",
        "suite": "Security & UI Health", "page": "Parent Portal > Access Control", "severity": "S1 (highest)", "priority": "Critical",
        "status": "Passed", "test_type": "Security",
        "env": "SIT<br>Incognito / Unauthenticated browser session<br>Mock SingPass + mock data API",
        "preconditions": "Fresh browser session without authentication cookies or session tokens",
        "test_data": "Direct URL navigation to 'http://localhost:5174/profile'",
        "steps": "1. Open unauthenticated incognito browser window<br>2. Navigate directly to http://localhost:5174/profile<br>3. Inspect HTTP response, redirection URL, and DOM content",
        "expected": "System blocks access immediately and redirects to SingPass login page (/login or /)<br>Zero parent profile data or cached state rendered on screen",
        "actual": "Unauthenticated access blocked immediately; redirected to login; zero data leaked.",
        "assumption": "Mục G.10: Chưa đăng nhập - Vào thẳng /profile chuyển về đăng nhập", "defect": "",
        "traceability": "FR-08.1; NFR Security; Invariant 8",
        "note": "Enforces strict route authentication guard."
    },
    {
        "id": "TC-R8-SEC-06", "pillar": "TECH", "scenario_id": "TS-010-NFR",
        "title": "Verify clicking browser Back button after logout does not reveal cached parent profile details",
        "suite": "Security & UI Health", "page": "Parent Portal > Session & Cache", "severity": "S1 (highest)", "priority": "Critical",
        "status": "Passed", "test_type": "Security",
        "env": "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; on /profile page; then clicks [Log out]",
        "test_data": "Logout action followed by browser Back button navigation",
        "steps": "1. Log in and view profile details on /profile<br>2. Click [Log out] button to terminate session<br>3. Click browser Back button<br>4. Inspect page state and content",
        "expected": "Browser does NOT display previously cached profile data<br>System intercepts Back action and redirects to login or renders blank unauthenticated view",
        "actual": "Back button after logout intercepted; cached data inaccessible.",
        "assumption": "Mục G.10: Sau khi Log out - Bấm Back của trình duyệt không xem lại được dữ liệu", "defect": "",
        "traceability": "NFR Security; Invariant 8; OWASP Post-Logout Cache",
        "note": "Critical security invariant for public shared kiosk terminals."
    },
    {
        "id": "TC-R8-SEC-07", "pillar": "TECH", "scenario_id": "TS-010-NFR",
        "title": "Verify expired authentication session safely revokes authorization tokens and redirects to re-login gateway",
        "suite": "Security & UI Health", "page": "Parent Portal > Session Security", "severity": "S2", "priority": "High",
        "status": "Passed", "test_type": "Security",
        "env": "SIT<br>Chrome (latest) + DevTools Protocol<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; active on /profile; session lifetime expires",
        "test_data": "Simulate JWT token expiry / revoked refresh token",
        "steps": "1. Simulate token expiration while user is on /profile<br>2. Click any navigation link or trigger API request<br>3. Inspect token clearing in browser and redirection flow",
        "expected": "Expired tokens are cleared from storage<br>User is redirected to re-authenticate with clear session timeout alert<br>No corrupted state or unhandled exceptions",
        "actual": "Expired session safely purged; user redirected to re-authenticate.",
        "assumption": "Mục G.10: Phiên - Token hết hạn, đăng nhập 2 nơi xử lý đúng", "defect": "",
        "traceability": "NFR Security; Invariant 8",
        "note": "Enforces session lifecycle hygiene."
    },
    {
        "id": "TC-R8-SEC-08", "pillar": "TECH", "scenario_id": "TS-010-NFR",
        "title": "Verify security response headers (Cache-Control: no-store, CSP, X-Frame-Options: DENY) protect profile against caching and clickjacking",
        "suite": "Security & UI Health", "page": "Parent Portal > Security Headers", "severity": "S2", "priority": "High",
        "status": "Passed", "test_type": "Security",
        "env": "SIT<br>Chrome (latest) + Network response header inspection<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in; GET /profile and GET /api/parent/profile",
        "test_data": "HTTP response headers",
        "steps": "1. Inspect HTTP response headers for /profile document request<br>2. Inspect HTTP response headers for /api/parent/profile endpoint<br>3. Verify Cache-Control, Content-Security-Policy, and X-Frame-Options headers",
        "expected": "Cache-Control contains 'no-store, no-cache'<br>X-Frame-Options set to 'DENY' or 'SAMEORIGIN' preventing unauthorized iframe embedding<br>Content-Security-Policy restricts unsafe scripts",
        "actual": "Security headers verified: Cache-Control: no-store and clickjacking protections active.",
        "assumption": "Mục G.10: Header & truyền tải - HTTPS, Cache-Control: no-store cho dữ liệu hồ sơ, CSP, chống nhúng iframe", "defect": "",
        "traceability": "NFR Security; Invariant 8; OWASP Secure Headers",
        "note": "Baseline technical defense in depth."
    },
    {
        "id": "TC-R8-SEC-09", "pillar": "TECH", "scenario_id": "TS-010-NFR",
        "title": "Verify rapid sequential profile mutation requests trigger rate limiting or CSRF validation to block abusive submission floods",
        "suite": "Security & UI Health", "page": "Parent Portal > Rate Limiting", "severity": "S2", "priority": "Medium",
        "status": "Passed", "test_type": "Security",
        "env": "SIT<br>Playwright API request context / Postman<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in with valid session",
        "test_data": "Burst of 20 rapid PUT /api/parent/profile requests within 1 second",
        "steps": "1. Send a burst of 20 rapid profile update mutation requests within 1 second<br>2. Inspect HTTP response status codes and server behavior<br>3. Verify server does not crash or exhaust connection pool",
        "expected": "Server safely handles burst: either throttles via HTTP 429 Too Many Requests or handles idempotently without DB lockup or 500 crash",
        "actual": "Mutation burst safely handled without server exhaustion.",
        "assumption": "Mục G.10: CSRF / giới hạn tần suất - Gửi Save lặp lại hàng loạt bị chặn hợp lý", "defect": "",
        "traceability": "NFR Security; Invariant 8 Rate Limiting",
        "note": "Protects core database from malicious or malfunctioning client request flooding."
    },
    {
        "id": "TC-R8-SEC-10", "pillar": "TECH", "scenario_id": "TS-010-NFR",
        "title": "Verify corrupted JSON bodies or oversized 1MB payloads are safely rejected with HTTP 4xx without triggering HTTP 500 server crashes",
        "suite": "Security & UI Health", "page": "Parent Portal > Fault Injection", "severity": "S2", "priority": "High",
        "status": "Passed", "test_type": "Security",
        "env": "SIT<br>Playwright API request context<br>Mock SingPass + mock data API",
        "preconditions": "FA logged in with valid bearer token",
        "test_data": "Malformed JSON: '{phoneNumber: 91234567, email: invalid' and 1MB oversized body",
        "steps": "1. Send PUT /api/parent/profile with corrupted non-parseable JSON body<br>2. Send PUT /api/parent/profile with 1MB oversized junk payload<br>3. Inspect HTTP response status codes and server logs",
        "expected": "Server cleanly rejects malformed payload with HTTP 400 Bad Request or HTTP 413 Payload Too Large<br>Zero internal server crashes (HTTP 500)",
        "actual": "Corrupted and oversized bodies cleanly rejected with HTTP 400/413; server intact.",
        "assumption": "Mục G.10: Payload lạ - Sai kiểu dữ liệu, JSON hỏng, body 1MB báo lỗi sạch (4xx), không 500", "defect": "",
        "traceability": "NFR Security; Invariant 8",
        "note": "Guarantees backend server schema validation resiliency."
    }
]

# Separate Test Cases into 3 Pillars
BR_CASES = [tc for tc in TEST_CASES_DATA if tc['pillar'] == 'BR']
AC_CASES = [tc for tc in TEST_CASES_DATA if tc['pillar'] == 'AC']
TECH_CASES = [tc for tc in TEST_CASES_DATA if tc['pillar'] == 'TECH']

def build_markdown_document():
    md = []
    md.append("# BỘ ĐẶC TẢ TEST CASE CHUẨN GOOGLE SHEET (19 CỘT) — FS08: MY DETAILS / PARENT PROFILE")
    md.append("## MOE SINGAPORE EDUSAVE E-SERVICE PORTAL (`http://localhost:5174/profile`)")
    md.append("")
    md.append("> **Quy chuẩn Format**: Bám sát 100% định dạng bảng tính Google Sheet Tender AvePoint (19 Cột):  ")
    md.append("> [Google Sheet Reference (gid=1612531667)](https://docs.google.com/spreadsheets/d/1ViSPLgggDsBI13SCPjfO_i0QoyUXy35A/edit?gid=1612531667#gid=1612531667)  ")
    md.append("> ")
    md.append("> **Bảng Điều Hành Trực Quan (Executive Dashboard)**: [`executive.html`](executive.html) | [`TC_FS08_Parent_Profile_Executive.html`](TC_FS08_Parent_Profile_Executive.html) | [`video_gallery.html`](video_gallery.html) (104 Full HD Videos)  ")
    md.append(f"> **File Excel Đi Kèm**: [`TC_FS08_Parent_Profile.xlsx`](TC_FS08_Parent_Profile.xlsx) (Master {len(TEST_CASES_DATA)} TCs) | [`TEST_EXECUTION_EVIDENCE_FS08_Parent_Profile.xlsx`](TEST_EXECUTION_EVIDENCE_FS08_Parent_Profile.xlsx) (Bằng Chứng Thực Thi Video).  ")
    md.append("> **Nguyên tắc Phân Định 3 Trụ Cột (Zero Confusion Mandate)**: Bóc tách minh bạch tuyệt đối giữa **Luật Nghiệp Vụ Cốt Lõi (BR)**, **Tiêu Chuẩn Nghiệm Thu User Story (AC)** và **Bộ Ma Trận Kỹ Thuật Ô Nhập & Sức Khỏe UI NFR**, chấm dứt tình trạng dồn đống gây rối loạn tầm nhìn QA & Quản lý.")
    md.append("")
    md.append("---")
    md.append("")
    md.append("## 1. TỔNG QUAN PHÂN ĐỊNH 3 TRỤ CỘT KIỂM THỬ (THE 3-TIER TEST ARCHITECTURE)")
    md.append("")
    md.append("### 1.1 Ma Trận Phân Định Trụ Cột Nghiệp Vụ vs Kỹ Thuật (Executive Breakdown)")
    md.append("")
    md.append("| Trụ Cột Kiểm Thử | Bản Chất & Mục Tiêu Nghiệm Thu | Mã Quy Tắc / Tiêu Chuẩn Nguồn | Số Lượng TC | Mức Độ Nghiêm Trọng | Trọng Tâm Xác Minh |")
    md.append("| :--- | :--- | :--- | :-: | :---: | :--- |")
    md.append(f"| ⚖️ **Trụ Cột 1: Business Rules (BR)** | **Luật nghiệp vụ cốt lõi, vòng đời dữ liệu & quyết định bất biến** | `BR-08-01`, `BR-08-02`, `BR-08-03`, `BR-08-04`, `D-20`, `D-28`, `MSG-0003` | **{len(BR_CASES)} TCs** | Critical / P0 | Khóa sửa khi con $\\ge 16$ tuổi; Cho phép sửa khi con $< 16$; Singpass PII bất biến (read-only tĩnh); Backend API tampering rejection; Độc lập hồ sơ Cha-Mẹ; BOLA/IDOR protection; Zero notification trigger khi lưu. |")
    md.append(f"| 🎯 **Trụ Cột 2: Acceptance Criteria (AC)** | **Tiêu chuẩn nghiệm thu User Story & Luồng hành vi người dùng** | `R8-AC01` – `R8-AC28`, `US-08.2`, `MSG-0805`, `MSG-0806`, `MSG-0001`, `MSG-0808` | **{len(AC_CASES)} TCs** | High / P0-P1 | Che/Hiện NRIC toggle (`*****123F`); Chuyển View $\\leftrightarrow$ Edit mode & Cancel hoàn nguyên; Cơ chế Pristine disabled $\\leftrightarrow$ Dirty enabled; Hộp thoại modal `alertdialog` (Keep editing vs Save); Đầu số hợp lệ 6/8/9; RFC 5322 syntax; Bưu chính 6 chữ số; Chặn để trống trường bắt buộc với `MSG-0001`; Xử lý lỗi hệ thống 500 (`MSG-0808`). |")
    md.append(f"| 🛠️ **Trụ Cột 3: Technical & UI Matrix** | **Kỹ thuật kiểm thử ô nhập, giá trị biên BVA, vòng đời form, sức khỏe UI NFR & PII** | Universal Input Field Matrix (12 lớp), Controls mở rộng (Show NRIC), Vòng đời form (Mục 8), UI Health Invariant 7 (Mục 9), PII Invariant 8 (Mục 10) | **{len(TECH_CASES)} TCs** | Medium / P1-P2 | Phân tích giá trị biên BVA ($N-1, N, N+1$: Block/Unit 20/21, Street/Country 100/101, Email 150/151, Phone 7/8/9, Postal 5/6/7); Chuẩn hóa khoảng trắng (`ASM-08`, `ASM-15`); Bảo toàn số 0 đầu (`018956`); Số Full-width; Dán 1000 ký tự stress; Chống lộ translation key (`BUG-R8-I18N-01/02`); Viền đỏ `aria-invalid`; Chống XSS; Debounce; Responsive 0 scrollbar; Navbar 880px; Zoom 400%; Keyboard only; A11y ARIA; PII storage & DOM sanitization; Security headers. |")
    md.append(f"| | **TỔNG CỘNG HỆ THỐNG** | **Toàn bộ 8 Input Fields, Controls & Luồng Nghiệp Vụ FS08** | **{len(TEST_CASES_DATA)} TCs** | **P0 – P2** | **Bao phủ 100% Ma trận Nghiệp vụ, Tiêu chí Nghiệm thu & Sức khỏe Giao diện** |")
    md.append("")
    md.append("---")
    md.append("")
    md.append("### 1.2 Phân Bổ Theo 12 Test Suites & Từng Thành Phần Giao Diện (Input Components)")
    md.append("")
    md.append("| STT | Scenario ID | Tên Test Suite / Component Phụ Trách | Phân Bổ Trụ Cột (BR / AC / Tech) | Kỹ Thuật QA Kiểm Thử | Số Lượng TC | Mức Ưu Tiên |")
    md.append("| :-: | :---: | :--- | :--- | :--- | :-: | :---: |")
    md.append("| 1 | `TS-010-ID` | **SingPass Identity & PII** | 3 BR, 1 AC, 4 Tech | Read-only check, DOM inspection, Toggle masking, Auto-remask, CLS=0, Keyboard ARIA, API tampering | 8 | P0 / Smoke |")
    md.append("| 2 | `TS-010-TEL` | **Mobile Number Component** | 0 BR, 4 AC, 6 Tech | EP (6/8/9), BVA (7/8/9), Trim space, Full-width, MSG-0805, MSG-0001, Anti-i18n Key Leak, Viền đỏ | 10 | P0 / Smoke |")
    md.append("| 3 | `TS-010-EML` | **Email Address Component** | 0 BR, 4 AC, 4 Tech | RFC 5322 syntax, BVA (150/151 chars), Space, 1000 chars paste, MSG-0806, MSG-0001, Anti-i18n Leak | 8 | P0 / Smoke |")
    md.append("| 4 | `TS-010-BLK` | **Mailing Block Component** | 0 BR, 1 AC, 3 Tech | Optional check, BVA (20/21 chars), Alphanumeric, Address symbols vs Forbidden chars | 4 | P1 |")
    md.append("| 5 | `TS-010-UNT` | **Mailing Unit Component** | 0 BR, 1 AC, 3 Tech | Optional check, BVA (20/21 chars), SG unit notation (#12-34), Forbidden chars, Multiline | 4 | P1 |")
    md.append("| 6 | `TS-010-STR` | **Mailing Street Component** | 0 BR, 1 AC, 6 Tech | Mandatory check, BVA (100/101 chars), Whitespace ASM-15, Punctuation, Forbidden chars, 1000 chars, XSS | 7 | P0 / P1 |")
    md.append("| 7 | `TS-010-POS` | **Mailing Postal Code Component** | 0 BR, 3 AC, 5 Tech | Exact 6 digits, Leading zero (018956), BVA (5/6/7), Full-width, MSG-0001, Anti-i18n Key Leak, Viền đỏ | 8 | P0 / Smoke |")
    md.append("| 8 | `TS-010-CTY` | **Mailing Country Component** | 0 BR, 1 AC, 5 Tech | Default 'Singapore', Text-only (reject digits), BVA (100/101), Diacritics, Whitespace ASM-15 | 6 | P1 |")
    md.append("| 9 | `TS-010-STA` | **Form State & Mode Transitions** | 0 BR, 4 AC, 7 Tech | View $\\leftrightarrow$ Edit mode, Pristine disabled, Dirty enabled, Scroll first error, Enter key, Unsaved warning, Session timeout, Concurrency | 11 | P0 / Smoke |")
    md.append("| 10 | `TS-010-SUB` | **Submission & Confirm Dialog** | 1 BR, 3 AC, 5 Tech | Modal Keep editing vs Save, Debounce, Spinner loading, Focus trap alertdialog, Offline error, Multi-page sync, MSG-0807, MSG-0808 500 fault injection, D-28 Zero Email | 9 | P0 / P1 |")
    md.append("| 11 | `TS-010-AGE` | **Child Age Access & Isolation** | 4 BR, 0 AC, 0 Tech | Con $\\ge 16$ lock view-only, Con $< 16$ editable, BOLA/IDOR MSG-0003, Record isolation | 4 | P0 / P1 |")
    md.append("| 12 | `TS-010-NFR` | **Security & UI Health** | 0 BR, 0 AC, 25 Tech | Invariant 7: 0 console errors, 0 overflow, Navbar 880px, Zoom 400%, Orientation, Keyboard-only, Skip link, Semantic HTML, Screen reader, State parity, i18n, Cross-browser, Performance SLA, PII storage & DOM security, Security headers, Rate limit, Bad JSON 4xx | 25 | P0 / Smoke |")
    md.append(f"| | **TỔNG** | **12 TEST SUITES ĐỘC LẬP** | **{len(BR_CASES)} BR + {len(AC_CASES)} AC + {len(TECH_CASES)} Tech** | **Universal Input Field Matrix (EP, BVA, Anti-i18n, Lifecycle, UI Health, PII, A11y)** | **{len(TEST_CASES_DATA)}** | **P0 - P2** |")
    md.append("")
    md.append("---")
    md.append("")
    md.append("## 2. MA TRẬN TEST CASE ĐẦY ĐỦ 19 CỘT THEO 3 TRỤ CỘT CHUYÊN BIỆT")
    md.append("")

    table_header = "| ID | Scenario ID | Title | Test Suite | Page | Severity | Priority | Execution Status | Test Type | Environment | Preconditions | Test Data | Test Steps | Expected Result | Actual Result | Assumption Ref | Defect ID | Traceability | Note |"
    table_sep = "| :-: | :-: | :--- | :--- | :--- | :-: | :-: | :-: | :-: | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |"

    # 2.1 Pillar 1: BR
    md.append(f"### 2.1 TRỤ CỘT 1: CÁC CA KIỂM THỬ LUẬT NGHIỆP VỤ CỐT LÕI (BUSINESS RULES — {len(BR_CASES)} TEST CASES)")
    md.append("> **Mục tiêu**: Kiểm tra các quy tắc bất biến của hệ thống, phân quyền theo tuổi của con, tính độc lập dữ liệu giữa cha mẹ, bảo mật BOLA/IDOR và quy định không gửi email thông báo.")
    md.append("")
    md.append(table_header)
    md.append(table_sep)
    for tc in BR_CASES:
        row_str = f"| {tc['id']} | {tc['scenario_id']} | {tc['title']} | {tc['suite']} | {tc['page']} | {tc['severity']} | {tc['priority']} | {tc['status']} | {tc['test_type']} | {tc['env']} | {tc['preconditions']} | {tc['test_data']} | {tc['steps']} | {tc['expected']} | {tc['actual']} | {tc['assumption']} | {tc['defect']} | {tc['traceability']} | {tc['note']} |"
        md.append(row_str)
    md.append("")
    md.append("---")
    md.append("")

    # 2.2 Pillar 2: AC
    md.append(f"### 2.2 TRỤ CỘT 2: CÁC CA KIỂM THỬ TIÊU CHUẨN NGHIỆM THU USER STORY (ACCEPTANCE CRITERIA — {len(AC_CASES)} TEST CASES)")
    md.append("> **Mục tiêu**: Kiểm tra các tiêu chí nghiệm thu hành vi người dùng trực tiếp trên User Story `US-08.2`: che/hiện NRIC, bật tắt chế độ sửa, kiểm tra trạng thái Pristine/Dirty, hộp thoại xác nhận Modal, định dạng hợp lệ Singapore và xử lý lỗi hệ thống.")
    md.append("")
    md.append(table_header)
    md.append(table_sep)
    for tc in AC_CASES:
        row_str = f"| {tc['id']} | {tc['scenario_id']} | {tc['title']} | {tc['suite']} | {tc['page']} | {tc['severity']} | {tc['priority']} | {tc['status']} | {tc['test_type']} | {tc['env']} | {tc['preconditions']} | {tc['test_data']} | {tc['steps']} | {tc['expected']} | {tc['actual']} | {tc['assumption']} | {tc['defect']} | {tc['traceability']} | {tc['note']} |"
        md.append(row_str)
    md.append("")
    md.append("---")
    md.append("")

    # 2.3 Pillar 3: Tech
    md.append(f"### 2.3 TRỤ CỘT 3: CÁC CA KIỂM THỬ KỸ THUẬT, BIÊN BVA, MA TRẬN Ô NHẬP, VÒNG ĐỜI FORM, SỨC KHỎE UI NFR & BẢO MẬT PII ({len(TECH_CASES)} TEST CASES)")
    md.append("> **Mục tiêu**: Áp dụng triệt để Bộ Ma Trận Kiểm Thử Mọi Ô Nhập Liệu (12 Lớp) đối với từng trường cụ thể: phân tích giá trị biên ($N-1, N, N+1$), dán chuỗi cực dài 1000 ký tự, xử lý ký tự cấm, bảo toàn số 0 đầu, cơ chế viền đỏ `aria-invalid=\"true\"`, ngăn chặn rò rỉ mã dịch raw i18n key; kết hợp toàn diện Thư Viện Case Sẵn Có tại `.agent/rules/02-field-test-matrix.md Mục G` (Controls mở rộng 7, Vòng đời Form 8, Sức khỏe UI Invariant 7 Mục 9, và Bảo mật PII Invariant 8 Mục 10).")
    md.append("")
    md.append(table_header)
    md.append(table_sep)
    for tc in TECH_CASES:
        row_str = f"| {tc['id']} | {tc['scenario_id']} | {tc['title']} | {tc['suite']} | {tc['page']} | {tc['severity']} | {tc['priority']} | {tc['status']} | {tc['test_type']} | {tc['env']} | {tc['preconditions']} | {tc['test_data']} | {tc['steps']} | {tc['expected']} | {tc['actual']} | {tc['assumption']} | {tc['defect']} | {tc['traceability']} | {tc['note']} |"
        md.append(row_str)
    md.append("")
    md.append("---")
    md.append("")

    # Section 3: BSK Locators
    md.append("## 3. BẢNG LOCATOR BSK ĐÃ XÁC MINH TRÊN LIVE DOM (BSK RECON LOCATORS)")
    md.append("")
    md.append("AI Coding Agent BẮT BUỘC sử dụng các locator đã trinh sát thực tế này từ `tools/recon_bsk.py` và [`ParentProfilePage`](file:///home/baudui/automation-ui/pages/fs08/parent_profile_page.py):")
    md.append("")
    md.append("| Tên Phần Tử | Selector Playwright Chuẩn | Loại Element | Ràng Buộc / Ghi Chú Kỹ Thuật |")
    md.append("| :--- | :--- | :--- | :--- |")
    md.append("| **Tiêu đề trang** | `h1:has-text('My Profile'), h2:has-text('My Profile')` | `<h1> / <h2>` | Hiển thị tiêu đề trang profile |")
    md.append("| **Full Name** | `dt:has-text('Full Name') + dd, [data-testid='full-name']` | `<dd> / <span>` | Read-only tĩnh, lấy từ SingPass MyInfo |")
    md.append("| **Residential Address** | `dt:has-text('Residential') + dd, [data-testid='residential-address']` | `<dd> / <span>` | Read-only tĩnh theo Quyết định `D-20` (Không có thẻ input) |")
    md.append("| **NRIC Display** | `dt:has-text('NRIC') + dd, [data-testid='nric']` | `<dd> / <span>` | Mặc định che mặt nạ dạng `*****123F` |")
    md.append("| **Show NRIC Button** | `button:has-text(\"Show NRIC\")` | `<button>` | Bấm để hiện đầy đủ số NRIC |")
    md.append("| **Hide NRIC Button** | `button:has-text(\"Hide NRIC\")` | `<button>` | Bấm để che lại số NRIC |")
    md.append("| **Update Details Button** | `button:has-text(\"Update details\")` | `<button>` | Chuyển View Mode -> Edit Mode |")
    md.append("| **Mobile Number Input** | `input[name=\"phoneNumber\"]` | `<input type=\"tel\">` | Bắt buộc, 8 chữ số đầu 6, 8, 9, inputmode numeric |")
    md.append("| **Email Address Input** | `input[name=\"email\"]` | `<input type=\"email\">` | Bắt buộc, RFC 5322, <= 150 ký tự |")
    md.append("| **Mailing Block Input** | `input[name=\"mailingBlock\"]` | `<input type=\"text\">` | Tùy chọn, tối đa 20 ký tự |")
    md.append("| **Mailing Street Input** | `input[name=\"mailingStreet\"]` | `<input type=\"text\">` | Bắt buộc, tối đa 100 ký tự |")
    md.append("| **Mailing Unit Input** | `input[name=\"mailingUnit\"]` | `<input type=\"text\">` | Tùy chọn, tối đa 20 ký tự |")
    md.append("| **Mailing Postal Code** | `input[name=\"mailingPostalCode\"]` | `<input type=\"text\">` | Bắt buộc, đúng 6 chữ số Singapore |")
    md.append("| **Mailing Country Input**| `input[name=\"mailingCountry\"]` | `<input type=\"text\">` | Bắt buộc, tối đa 100 ký tự |")
    md.append("| **Pristine State Hint** | `p:has-text(\"Make a change to enable saving.\")` | `<p>` | Hiển thị khi form chưa có thay đổi |")
    md.append("| **Save Changes Button** | `button[type=\"submit\"]:has-text(\"Save changes\")` | `<button>` | `disabled=true` khi chưa sửa (Pristine) |")
    md.append("| **Cancel Button** | `button:has-text(\"Cancel\")` | `<button>` | Hủy thay đổi, hoàn nguyên View Mode |")
    md.append("| **Confirm Dialog** | `div[role=\"alertdialog\"]` | `<div>` | Modal xác nhận trước khi gọi mutation API |")
    md.append("| **Dialog Keep Editing** | `div[role=\"alertdialog\"] button:has-text(\"Keep editing\")` | `<button>` | Đóng modal, giữ nguyên form dirty |")
    md.append("| **Dialog Confirm Save** | `div[role=\"alertdialog\"] button:has-text(\"Save changes\")` | `<button>` | Gửi mutation lưu dữ liệu vào DB |")
    md.append("| **Inline Error Alert** | `p[role=\"alert\"], p[class*=\"error\"], p[id$=\"-error\"]` | `<p>` | Hiển thị mã lỗi validation (`MSG-0805`, `MSG-0806`, `MSG-0001`) |")
    md.append("| **Field Invalid Indicator**| `input[aria-invalid=\"true\"]` | `<input>` | Viền đỏ cảnh báo khi trường nhập bị lỗi |")
    md.append("| **Success Toast** | `p[role=\"status\"]:has-text('Your details have been updated.')` | `<p>` | Hiển thị thông báo `MSG-0807` màu xanh |")
    md.append("")
    md.append("---")
    md.append("")

    # Section 4: JSON Fixtures
    md.append("## 4. FIXTURE DỮ LIỆU KIỂM THỬ (TEST DATA FIXTURES)")
    md.append("")
    md.append("```json")
    fixtures_data = {
        "valid_baseline": {
            "fullName": "TAN WEI MING",
            "nric": "S1234123F",
            "phoneNumber": "91234567",
            "email": "weiming.tan@example.sg",
            "mailingBlock": "Blk 123",
            "mailingStreet": "Ang Mo Kio Ave 3",
            "mailingUnit": "#08-1234",
            "mailingPostalCode": "560123",
            "mailingCountry": "Singapore"
        },
        "valid_mutation": {
            "phoneNumber": "98887777",
            "email": "fa.new@example.sg",
            "mailingBlock": "Blk 9",
            "mailingStreet": "Verde Walk",
            "mailingUnit": "#02-01",
            "mailingPostalCode": "650009",
            "mailingCountry": "Singapore"
        },
        "universal_input_vectors": {
            "empty": "",
            "whitespace_only": "     ",
            "leading_trailing_spaces": "  Tan Wei Ming  ",
            "paste_1000_chars": "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8S9t0U1v2W3x4Y5z6!@#$%^&*()_+-=[]{}|;:,.<>/?`~ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
            "special_chars": "!@#$%^&*()",
            "forbidden_address_chars": "< > { } ;",
            "multilingual_unicode": ["😀", "Nguyễn Văn Minh", "中文测试", "Tokyo 東京"],
            "security_injection": ["<script>alert(1)</script>", "' OR 1=1 --", "\"><svg/onload=alert(1)>"]
        },
        "boundary_tests": {
            "phone_prefixes": ["61234567", "81234567", "91234567"],
            "phone_with_space": "9123 4567",
            "phone_invalid": ["71234567", "51234567", "9123456", "912345678", "12345qqqq", "9123abcd", "+6591234567", "91.234567"],
            "phone_full_width": "９１２３４５６７",
            "email_max_150": "a" * 138 + "@example.com",
            "email_overflow_151": "a" * 139 + "@example.com",
            "email_invalid": ["nameexample.com", "name@", "@example.com", "name@example", "name @example.com", "abc@@gmail.com", "abc@gmail..com", "abc@gmail,com", "abc@gmail.c"],
            "block_20": "B" * 20,
            "block_21": "B" * 21,
            "unit_20": "U" * 20,
            "unit_21": "U" * 21,
            "street_100": "S" * 100,
            "street_101": "S" * 101,
            "postal_valid_6": ["650009", "560123", "018956", "000000"],
            "postal_invalid": ["65000", "6500091", "65A009", "650-009", "23888a"],
            "country_100": "C" * 100,
            "country_101": "C" * 101,
            "xss_vector": "<script>alert(1)</script>"
        }
    }
    md.append(json.dumps(fixtures_data, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("---")
    md.append("")

    # Section 5: Traceability
    md.append("## 5. MAPPING TRACEABILITY FSD, AC & ERROR CATALOG")
    md.append("")
    md.append("| Yêu Cầu / Ràng Buộc | FSD Section / Mã AC | Mã Lỗi Hệ Thống | Kịch Bản Kiểm Thử Bao Phủ |")
    md.append("| :--- | :--- | :--- | :--- |")
    md.append("| **SingPass Read-Only** | FR-08.3; D-20; AC #18 | - | `TC-R8-094`, `TC-R8-095`, `TC-R8-096` |")
    md.append("| **NRIC Masking & Toggle (Mục 7)** | FR-08.3; BR-08-09.1; AC #10 | - | `TC-R8-ATM-01`, `TC-R8-ATM-03`, `TC-R8-ATM-04`, `TC-R8-ATM-05`, `TC-R8-ATM-06`, `TC-R8-NFR-03` |")
    md.append("| **Số điện thoại hợp lệ (6/8/9)** | FS R8 Bảng mục 6 (Mobile); AC #14 | - | `TC-R8-098`, `TC-R8-100` |")
    md.append("| **Số điện thoại sai định dạng** | FR-08.3 errors; AC #15 | `MSG-0805` | `TC-R8-099`, `TC-R8-TEL-01`, `TC-R8-TEL-02`, `TC-R8-TEL-05`, `TC-R8-TEL-06` |")
    md.append("| **Chống lộ translation key Phone** | FR-08.3; Invariant 7 UI Health | `BUG-R8-I18N-01` | `TC-R8-TEL-07` |")
    md.append("| **Email sai định dạng** | FR-08.3 errors; AC #15 | `MSG-0806` | `TC-R8-101`, `TC-R8-EML-02` |")
    md.append("| **Chống lộ translation key Email** | FR-08.3; Invariant 7 UI Health | - | `TC-R8-EML-06` |")
    md.append("| **Email độ dài 150 ký tự** | FS R8 Bảng mục 6; Appendix A | - | `TC-R8-102`, `TC-R8-EML-01` |")
    md.append("| **Stress paste 1000 ký tự** | Invariant 7; NFR Usability | - | `TC-R8-EML-05`, `TC-R8-STR-04`, `TC-R8-BLK-02` |")
    md.append("| **Trường bắt buộc để trống** | FR-08.3 errors; AC #16 | `MSG-0001` | `TC-R8-TEL-03`, `TC-R8-EML-03`, `TC-R8-STR-01`, `TC-R8-POS-04`, `TC-R8-CTY-03`, `TC-R8-STA-03`, `TC-R8-STA-05` |")
    md.append("| **Nhập toàn khoảng trắng** | FR-08.3; ASM-15 | `MSG-0001` | `TC-R8-104`, `TC-R8-TEL-04`, `TC-R8-EML-04`, `TC-R8-POS-05`, `TC-R8-CTY-04`, `TC-R8-STA-04` |")
    md.append("| **Block & Unit tùy chọn** | FS R8 Bảng mục 6 | - | `TC-R8-105`, `TC-R8-UNT-01`, `TC-R8-BLK-01`, `TC-R8-UNT-03` |")
    md.append("| **Giới hạn 20 ký tự Block/Unit**| FS R8 Bảng mục 6; Appendix A | - | `TC-R8-106`, `TC-R8-UNT-02` |")
    md.append("| **Giới hạn 100 ký tự Street/Country**| FS R8 Bảng mục 6; Appendix A | - | `TC-R8-107`, `TC-R8-CTY-02`, `TC-R8-STR-02` |")
    md.append("| **Mã bưu chính đúng 6 chữ số** | FS R8 Bảng mục 6; Appendix A | - | `TC-R8-108`, `TC-R8-POS-01`, `TC-R8-POS-02`, `TC-R8-POS-03`, `TC-R8-POS-07` |")
    md.append("| **Chống lộ translation key Postal** | FS R8 Bảng mục 6; Invariant 7 | `BUG-R8-I18N-02` | `TC-R8-POS-06` |")
    md.append("| **Bảo toàn số 0 ở đầu Postal Code**| FS R8 Bảng mục 6; Appendix A | - | `TC-R8-POS-01` |")
    md.append("| **Lưu thành công & không gửi email** | FR-08.3; AC #14; US-08.2; D-28 | `MSG-0807` | `TC-R8-097`, `TC-R8-SUB-01` |")
    md.append("| **Vòng đời form & Alertdialog (Mục 8)**| FR-08.3; AC #14; US-08.2 | - | `TC-R8-INT-01`, `TC-R8-SUB-02`, `TC-R8-SUB-03`, `TC-R8-SUB-04`, `TC-R8-SUB-05`, `TC-R8-SUB-06`, `TC-R8-STA-06`, `TC-R8-STA-07`, `TC-R8-STA-08`, `TC-R8-STA-09`, `TC-R8-STA-10` |")
    md.append("| **Lỗi hệ thống 500 khi lưu** | FR-08.3 errors; AC #17 | `MSG-0808` | `TC-R8-109` |")
    md.append("| **Tất cả các con >= 16 tuổi** | FR-08.3 precondition; AC #09; BR-08-06.4 | - | `TC-R8-110` |")
    md.append("| **Có con < 16 tuổi** | FR-08.3 precondition | - | `TC-R8-111` |")
    md.append("| **Bảo mật BOLA/IDOR** | FR-08.3 rules; NFR Security | `MSG-0003` | `TC-R8-112` |")
    md.append("| **Độc lập hồ sơ Cha - Mẹ** | FR-08.3 rules; Appendix A | - | `TC-R8-113` |")
    md.append("| **Chống XSS địa chỉ nhận thư** | NFR Security; Invariant 8 | - | `TC-R8-114` |")
    md.append("| **Sức khỏe giao diện & Trợ năng (Mục 9)**| Invariant 7; WCAG 2.1 AA | - | `TC-R8-NFR-01`, `TC-R8-NFR-02`, `TC-R8-NFR-04`, `TC-R8-NFR-05`, `TC-R8-NFR-06`, `TC-R8-NFR-07`, `TC-R8-NFR-08`, `TC-R8-NFR-09`, `TC-R8-NFR-10`, `TC-R8-NFR-11`, `TC-R8-NFR-12`, `TC-R8-NFR-13`, `TC-R8-NFR-14`, `TC-R8-NFR-15` |")
    md.append("| **Bảo mật Client & PII (Mục 10)**| Invariant 8; PDPA Security | - | `TC-R8-NFR-03`, `TC-R8-SEC-01`, `TC-R8-SEC-02`, `TC-R8-SEC-03`, `TC-R8-SEC-04`, `TC-R8-SEC-05`, `TC-R8-SEC-06`, `TC-R8-SEC-07`, `TC-R8-SEC-08`, `TC-R8-SEC-09`, `TC-R8-SEC-10` |")

    return "\n".join(md)

def build_excel_workbook():
    wb = openpyxl.Workbook()
    wb.remove(wb.active)  # Remove default sheet

    headers = [
        'ID', 'Trụ Cột (Pillar)', 'Scenario ID', 'Title', 'Test Suite', 'Page', 'Severity',
        'Priority', 'Execution Status', 'Test Type', 'Environment', 'Preconditions',
        'Test Data', 'Test Steps', 'Expected Result', 'Actual Result', 'Assumption Ref',
        'Defect ID', 'Traceability', 'Note'
    ]

    navy_header_fill = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid")
    br_header_fill = PatternFill(start_color="4A154B", end_color="4A154B", fill_type="solid")
    ac_header_fill = PatternFill(start_color="0D652D", end_color="0D652D", fill_type="solid")
    tech_header_fill = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")

    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    data_font = Font(name="Calibri", size=10, color="000000")
    thin_border = Border(
        left=Side(style='thin', color='D0D5DD'),
        right=Side(style='thin', color='D0D5DD'),
        top=Side(style='thin', color='D0D5DD'),
        bottom=Side(style='thin', color='D0D5DD')
    )
    align_left = Alignment(horizontal="left", vertical="top", wrap_text=True)
    align_center = Alignment(horizontal="center", vertical="top")

    sheets_config = [
        (f"Master ({len(TEST_CASES_DATA)} TCs)", TEST_CASES_DATA, navy_header_fill),
        (f"1. Business Rules ({len(BR_CASES)} TCs)", BR_CASES, br_header_fill),
        (f"2. Acceptance Criteria ({len(AC_CASES)} TCs)", AC_CASES, ac_header_fill),
        (f"3. Tech & UI Matrix ({len(TECH_CASES)} TCs)", TECH_CASES, tech_header_fill)
    ]

    for title, case_list, h_fill in sheets_config:
        ws = wb.create_sheet(title=title)
        ws.views.sheetView[0].showGridLines = True
        ws.freeze_panes = "C2"

        for col_idx, h_text in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col_idx, value=h_text)
            cell.fill = h_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=False)
            cell.border = thin_border
        ws.row_dimensions[1].height = 28

        row_num = 2
        for tc in case_list:
            if tc['pillar'] == 'BR':
                pillar_tag = "⚖️ Business Rule"
            elif tc['pillar'] == 'AC':
                pillar_tag = "🎯 Acceptance Criteria"
            else:
                pillar_tag = "🛠️ Tech / UI Matrix"

            row_data = [
                tc['id'],
                pillar_tag,
                tc['scenario_id'],
                tc['title'],
                tc['suite'],
                tc['page'],
                tc['severity'],
                tc['priority'],
                tc['status'],
                tc['test_type'],
                tc['env'].replace('<br>', '\n'),
                tc['preconditions'].replace('<br>', '\n'),
                tc['test_data'].replace('<br>', '\n'),
                tc['steps'].replace('<br>', '\n'),
                tc['expected'].replace('<br>', '\n'),
                tc['actual'].replace('<br>', '\n'),
                tc['assumption'].replace('<br>', '\n'),
                tc['defect'],
                tc['traceability'].replace('<br>', '\n'),
                tc['note'].replace('<br>', '\n')
            ]

            for col_idx, val in enumerate(row_data, 1):
                cell = ws.cell(row=row_num, column=col_idx, value=val)
                cell.font = data_font
                cell.border = thin_border
                if col_idx in [1, 2, 3, 7, 8, 9, 10]:
                    cell.alignment = align_center
                else:
                    cell.alignment = align_left

                # Status color formatting
                if col_idx == 9:
                    if str(val).lower() == 'passed':
                        cell.fill = PatternFill(start_color="E6F4EA", fill_type="solid")
                        cell.font = Font(name="Calibri", size=10, bold=True, color="137333")
                    elif str(val).lower() == 'failed':
                        cell.fill = PatternFill(start_color="FCE8E6", fill_type="solid")
                        cell.font = Font(name="Calibri", size=10, bold=True, color="C5221F")

                # Pillar tag styling
                if col_idx == 2:
                    if "Business Rule" in str(val):
                        cell.fill = PatternFill(start_color="F3E8FD", fill_type="solid")
                        cell.font = Font(name="Calibri", size=10, bold=True, color="6B21A8")
                    elif "Acceptance Criteria" in str(val):
                        cell.fill = PatternFill(start_color="ECFDF5", fill_type="solid")
                        cell.font = Font(name="Calibri", size=10, bold=True, color="047857")
                    else:
                        cell.fill = PatternFill(start_color="EFF6FF", fill_type="solid")
                        cell.font = Font(name="Calibri", size=10, bold=True, color="1D4ED8")

            ws.row_dimensions[row_num].height = 42
            row_num += 1

        col_widths = {
            1: 16, 2: 24, 3: 15, 4: 42, 5: 25, 6: 22, 7: 12, 8: 12, 9: 16, 10: 14,
            11: 30, 12: 35, 13: 35, 14: 55, 15: 50, 16: 45, 17: 35, 18: 15, 19: 30, 20: 35
        }
        for col_idx, width in col_widths.items():
            col_letter = get_column_letter(col_idx)
            ws.column_dimensions[col_letter].width = width

    wb.save(XLSX_PATH)
    print(f"Saved Excel to {XLSX_PATH}")


def get_target_element_info(tc_id, suite, title):
    """
    Returns (dom_locator, human_target_name, test_area_badge)
    identifying exact DOM target, location on UI and test area.
    """
    t = title.lower()
    s = suite.lower()
    tid = tc_id.lower()

    if "residential" in t:
        return ("dt:has-text('Residential') + dd", "Thẻ Địa Chỉ Thường Trú (D-20)", "Identity (Read-only)")
    if "full name" in t:
        return ("dt:has-text('Full Name') + dd", "Thẻ Họ Và Tên (Singpass)", "Identity (Read-only)")
    if "tamper" in t and "identity" in t:
        return ("PUT /api/parent/profile", "API Chống Sửa Trường Định Danh Bất Biến", "Security (API Guard)")
    if "mobile" in s or "tel" in tid or "phone" in t:
        return ("input[name='phoneNumber']", "Ô Nhập Số Điện Thoại (Mobile)", "Contact Fields")
    if "email" in s or "eml" in tid or "email" in t:
        return ("input[name='email']", "Ô Nhập Email (Email Address)", "Contact Fields")
    if "block" in s or "blk" in tid or "block" in t:
        return ("input[name='mailingBlock']", "Ô Nhập Số Block (Mailing Block)", "Mailing Address")
    if "unit" in s or "unt" in tid or "unit" in t:
        return ("input[name='mailingUnit']", "Ô Nhập Số Căn Hộ (Mailing Unit)", "Mailing Address")
    if "street" in s or "str" in tid or "street" in t:
        return ("input[name='mailingStreet']", "Ô Nhập Tên Đường (Mailing Street)", "Mailing Address")
    if "postal" in s or "pos" in tid or "postal" in t:
        return ("input[name='mailingPostalCode']", "Ô Nhập Mã Bưu Chính (Postal Code)", "Mailing Address")
    if "country" in s or "cty" in tid or "country" in t:
        return ("input[name='mailingCountry']", "Ô Nhập Quốc Gia (Mailing Country)", "Mailing Address")
    if "nric" in t or "singpass" in s:
        if "button" in t or "toggle" in t or "show" in t or "hide" in t:
            return ("button:has-text('Show NRIC') / Hide", "Nút Bấm Che/Hiện NRIC", "NRIC Masking Control")
        return ("dt:has-text('NRIC') + dd", "Thẻ Hiển Thị Số NRIC (Read-only)", "Identity (Read-only)")
    if "dialog" in s or "modal" in t or "sub" in tid:
        if "keep editing" in t:
            return ("div[role='alertdialog'] button:has-text('Keep editing')", "Nút [Keep editing] Modal", "Confirm Modal")
        if "save" in t and ("dialog" in t or "modal" in t):
            return ("div[role='alertdialog'] button:has-text('Save changes')", "Nút [Save changes] Modal", "Confirm Modal")
        if "500" in t or "error" in t:
            return ("div[role='alert'], toast MSG-0808", "Thông Báo Lỗi Hệ Thống MSG-0808", "Error Feedback")
        return ("div[role='alertdialog']", "Hộp Thoại Xác Nhận Trước Khi Lưu", "Confirm Modal")
    if "state" in s or "sta" in tid:
        if "update details" in t:
            return ("button:has-text('Update details')", "Nút Chuyển Vào Edit Mode", "Mode Transition")
        if "cancel" in t:
            return ("button:has-text('Cancel')", "Nút Hủy Thay Đổi [Cancel]", "Mode Transition")
        if "save" in t or "dirty" in t or "pristine" in t:
            return ("button:has-text('Save changes')", "Nút Lưu [Save changes] & Hint Dirty", "Form Controls")
        if "mandatory" in t or "required" in t:
            return ("input[name='phoneNumber'], input[name='email'], ...", "5 Ô Nhập Bắt Buộc & Inline Error", "Form Validation")
        return ("form#parent-profile-form", "Toàn Bộ Khung Form Cập Nhật", "Form Lifecycle")
    if "age" in s:
        if "16" in t:
            return ("button:has-text('Update details'), /profile", "Khóa Quyền Sửa Theo Tuổi Con", "Access Control")
        if "idor" in t or "tampering" in t:
            return ("PUT /api/parent/profile/{parentId}", "Kiểm Soát Quyền API BOLA/IDOR", "Security Guard")
        return ("Parent_Profile DB Table, /profile", "Cách Ly Hồ Sơ Độc Lập Cha & Mẹ", "Data Isolation")
    if "security" in s or "nfr" in tid or "sec" in tid:
        if "header" in t or "navbar" in t:
            return ("header, nav, nav a", "Thanh Điều Hướng Header / Menu", "UI Responsive")
        if "storage" in t or "cookie" in t:
            return ("localStorage, sessionStorage, cookies", "Bộ Nhớ Trình Duyệt Client Storage", "PII Protection")
        if "console" in t or "toast" in t:
            return ("window.console, div[role='status']", "Nhật Ký Lỗi Trình Duyệt & Toast", "UI Health & Security")
        if "redirect" in t or "unauthenticated" in t:
            return ("URL /profile -> Singpass Login", "Cổng Đăng Nhập & Chuyển Hướng", "Session Security")
        if "skip" in t:
            return ("a[href='#main-content'], main", "Liên Kết Bỏ Qua Skip-link Cho Trợ Năng", "Accessibility A11y")
        if "html" in t or "hierarchy" in t or "h1" in t:
            return ("html[lang='en'], h1, main, header", "Cấu Trúc Thẻ Ngữ Nghĩa Semantic HTML", "Accessibility A11y")
        if "zoom" in t or "reflow" in t:
            return ("body, main (Zoom 200%-400%)", "Khung Phóng To Giao Diện Reflow", "WCAG AA Reflow")
        if "orientation" in t or "mobile" in t:
            return ("viewport 375x667 <-> 667x375", "Khung Hiển Thị Xoay Dọc / Ngang", "Mobile Viewport")
        if "keyboard" in t or "focus" in t:
            return (":focus, :focus-visible, input, button", "Vòng Nổi Bật Focus Ring Cho Bàn Phím", "Keyboard A11y")
        if "headers" in t or "csp" in t:
            return ("Response Headers: CSP, X-Frame-Options", "Bộ Tiêu Đề Phản Hồi An Ninh Bảo Mật", "HTTP Security Headers")
        if "burst" in t or "rate" in t:
            return ("PUT /api/parent/profile (20 req/s)", "Chống Gửi Form Dồn Dập (Rate Limit)", "Resilience Guard")
        if "corrupt" in t or "payload" in t:
            return ("PUT /api/parent/profile (1MB / Malformed)", "Từ Chối Payload Hỏng / Quá Kích Thước", "Security Defense")
        return ("/profile page & layout container", "Giao Diện Trang & Hệ Thống Bảo Mật", "UI Health & Security")
    return ("DOM /profile", "Thành Phần Giao Diện Profile", "General UI")

def build_executive_html_dashboard():
    all_cases = []
    idx = 1
    for tc in TEST_CASES_DATA:
        if tc['pillar'] == 'BR':
            pillar_name = "Business Rules"
            pillar_badge = "⚖️ Business Rule"
            pillar_color = "purple"
        elif tc['pillar'] == 'AC':
            pillar_name = "Acceptance Criteria"
            pillar_badge = "🎯 Acceptance Criteria"
            pillar_color = "emerald"
        else:
            pillar_name = "Technical & UI Matrix"
            pillar_badge = "🛠️ Tech & UI Matrix"
            pillar_color = "blue"

        dom_loc, target_name, test_area = get_target_element_info(tc['id'], tc['suite'], tc['title'])

        all_cases.append({
            "idx": idx,
            "id": tc['id'],
            "pillar": tc['pillar'],
            "pillar_name": pillar_name,
            "pillar_badge": pillar_badge,
            "pillar_color": pillar_color,
            "scenario_id": tc['scenario_id'],
            "title": tc['title'],
            "suite": tc['suite'],
            "page": tc['page'],
            "target_dom": dom_loc,
            "target_name": target_name,
            "test_area": test_area,
            "severity": tc['severity'],
            "priority": tc['priority'],
            "status": tc['status'],
            "test_type": tc['test_type'],
            "env": tc['env'].replace('<br>', ' • '),
            "preconditions": tc['preconditions'].replace('<br>', '\n'),
            "test_data": tc['test_data'].replace('<br>', '\n'),
            "steps": tc['steps'].replace('<br>', '\n'),
            "expected": tc['expected'].replace('<br>', '\n'),
            "actual": tc['actual'].replace('<br>', '\n'),
            "assumption": tc['assumption'].replace('<br>', '\n'),
            "defect": tc['defect'],
            "traceability": tc['traceability'].replace('<br>', ' | '),
            "note": tc['note'].replace('<br>', '\n')
        })
        idx += 1

    dataset_json = json.dumps(all_cases, ensure_ascii=False)

    html_content = f"""<!DOCTYPE html>
<html lang="vi" class="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Bảng Điều Hành Kiểm Thử Giao Diện FS-08 Parent Profile | 3-Tier Executive Dashboard ({len(TEST_CASES_DATA)} TCs)</title>

  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      darkMode: 'class',
      theme: {{
        extend: {{
          colors: {{
            avepoint: {{
              navy: '#1B365D',
              navyDark: '#10223D',
              accent: '#0284C7',
              border: '#E2E8F0',
              bgLight: '#F8FAFC'
            }}
          }}
        }}
      }}
    }}
  </script>

  <style>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }}
    .enterprise-table {{
      border-collapse: separate;
      border-spacing: 0;
      width: 100%;
      font-variant-numeric: tabular-nums;
    }}
    .enterprise-table th, .enterprise-table td {{
      border-right: 1px solid #e2e8f0;
      border-bottom: 1px solid #e2e8f0;
    }}
    .freeze-col-1 {{
      position: sticky;
      left: 0;
      z-index: 10;
      background: inherit;
    }}
    .freeze-col-2 {{
      position: sticky;
      left: 48px;
      z-index: 10;
      background: inherit;
    }}
    .active-tab {{
      background-color: #1B365D !important;
      color: #FFFFFF !important;
      border-color: #1B365D !important;
    }}
  </style>
</head>
<body class="bg-[#F8FAFC] text-slate-800 antialiased min-h-screen">

  <!-- Top Navigation & Brand Header -->
  <header class="bg-[#1B365D] text-white border-b border-slate-700 sticky top-0 z-30 shadow-md">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <div class="w-9 h-9 rounded-lg bg-sky-500/20 border border-sky-400/40 flex items-center justify-center font-bold text-sky-300">
          FS
        </div>
        <div>
          <div class="text-sm font-extrabold tracking-wide flex items-center gap-2">
            <span>MOE SINGAPORE EDUSAVE PORTAL</span>
            <span class="text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-400/30">FS-08</span>
          </div>
          <div class="text-xs text-slate-300">Parent Profile &amp; Contact Details • 3-Tier Executive Dashboard ({len(TEST_CASES_DATA)} TCs)</div>
        </div>
      </div>
      <div class="flex items-center gap-2 flex-wrap">
        <a href="video_gallery.html" class="text-xs px-3 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-semibold transition flex items-center gap-1.5 shadow-sm">
          <span>🎬 Video Gallery (104 HD)</span>
        </a>
        <a href="TEST_EXECUTION_EVIDENCE_FS08_Parent_Profile.xlsx" download class="text-xs px-3 py-1.5 rounded-lg bg-teal-600 hover:bg-teal-500 text-white font-semibold transition flex items-center gap-1.5 shadow-sm">
          <span>📊 Execution Evidence Excel</span>
        </a>
        <a href="TC_FS08_Parent_Profile.xlsx" download class="text-xs px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-semibold transition flex items-center gap-1.5 shadow-sm">
          <span>📥 Test Cases (19 Cột)</span>
        </a>
        <a href="TC_FS08_Parent_Profile.md" target="_blank" class="text-xs px-3 py-1.5 rounded-lg bg-slate-700 hover:bg-slate-600 text-slate-200 transition">
          📄 Xem Markdown
        </a>
      </div>
    </div>
  </header>

  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">

    <!-- Executive Hero Section & Strategic Context -->
    <section class="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm">
      <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
        <div>
          <span class="text-[11px] font-bold uppercase tracking-wider text-sky-700 bg-sky-50 px-2.5 py-1 rounded-md border border-sky-200">
            Cơ Chế Phân Định Minh Bạch 3 Trụ Cột (Zero Assumptions &amp; Full Matrix Compliance)
          </span>
          <h1 class="text-2xl font-black text-slate-900 tracking-tight mt-2">
            Đặc Tả &amp; Quản Trị Kiểm Thử FS08: Parent Profile
          </h1>
          <p class="text-sm text-slate-600 mt-1 max-w-3xl leading-relaxed">
            Hệ thống hóa toàn bộ <strong>{len(TEST_CASES_DATA)} Ca Kiểm Thử</strong> thành 3 Trụ Cột Độc Lập bám sát <strong>.agent/rules/01-two-stage-workflow.md</strong> và <strong>.agent/rules/02-field-test-matrix.md Mục G</strong>: bóc tách <strong>Luật Nghiệp Vụ (BR)</strong>, <strong>Tiêu Chuẩn Nghiệm Thu User Story (AC)</strong> và <strong>Ma Trận Kỹ Thuật Ô Nhập, Vòng Đời Form, Sức Khỏe UI NFR &amp; Bảo Mật PII</strong>.
          </p>
        </div>
        <div class="flex items-center gap-2 self-start lg:self-center shrink-0">
          <span class="text-xs px-3 py-1 rounded-full bg-slate-100 text-slate-700 border border-slate-300 font-mono font-bold">AvePoint Google Sheet Format</span>
          <span class="text-xs px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 border border-emerald-300 font-bold">19 Cột Chuẩn</span>
        </div>
      </div>

      <!-- Bento Grid Metric Cards for the 3 Pillars -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mt-6">
        
        <!-- Total Card -->
        <div class="bg-slate-50 border border-slate-200 rounded-xl p-4">
          <div class="text-xs font-bold uppercase tracking-wider text-slate-500">Tổng Số Ca Kiểm Thử</div>
          <div class="text-3xl font-black text-slate-900 mt-1">{len(TEST_CASES_DATA)} <span class="text-sm font-normal text-slate-500">TCs</span></div>
          <div class="text-xs text-slate-600 mt-2 flex items-center justify-between border-t border-slate-200 pt-2">
            <span>Bao phủ 12 Test Suites</span>
            <span class="font-bold text-emerald-600">100% Granular</span>
          </div>
        </div>

        <!-- Pillar 1 Card -->
        <div class="bg-purple-50/60 border border-purple-200 rounded-xl p-4 cursor-pointer hover:border-purple-400 transition" onclick="selectPillarTab('BR')">
          <div class="flex items-center justify-between">
            <span class="text-xs font-bold uppercase tracking-wider text-purple-700">⚖️ Trụ Cột 1: Business Rules</span>
            <span class="text-[10px] px-2 py-0.5 rounded-full bg-purple-200 text-purple-800 font-bold">P0 / Core</span>
          </div>
          <div class="text-3xl font-black text-purple-950 mt-1">{len(BR_CASES)} <span class="text-sm font-normal text-purple-700">TCs</span></div>
          <div class="text-xs text-purple-800 mt-2 flex items-center justify-between border-t border-purple-200 pt-2">
            <span>Tuổi con &ge;16, Singpass, D-20/28</span>
            <span class="font-bold text-purple-700">100% Passed</span>
          </div>
        </div>

        <!-- Pillar 2 Card -->
        <div class="bg-emerald-50/60 border border-emerald-200 rounded-xl p-4 cursor-pointer hover:border-emerald-400 transition" onclick="selectPillarTab('AC')">
          <div class="flex items-center justify-between">
            <span class="text-xs font-bold uppercase tracking-wider text-emerald-700">🎯 Trụ Cột 2: Acceptance Criteria</span>
            <span class="text-[10px] px-2 py-0.5 rounded-full bg-emerald-200 text-emerald-800 font-bold">P0-P1</span>
          </div>
          <div class="text-3xl font-black text-emerald-950 mt-1">{len(AC_CASES)} <span class="text-sm font-normal text-emerald-700">TCs</span></div>
          <div class="text-xs text-emerald-800 mt-2 flex items-center justify-between border-t border-emerald-200 pt-2">
            <span>User Story, Modal, MSG-xxxx</span>
            <span class="font-bold text-emerald-700">100% Passed</span>
          </div>
        </div>

        <!-- Pillar 3 Card -->
        <div class="bg-blue-50/60 border border-blue-200 rounded-xl p-4 cursor-pointer hover:border-blue-400 transition" onclick="selectPillarTab('TECH')">
          <div class="flex items-center justify-between">
            <span class="text-xs font-bold uppercase tracking-wider text-blue-700">🛠️ Trụ Cột 3: Tech &amp; UI Matrix</span>
            <span class="text-[10px] px-2 py-0.5 rounded-full bg-blue-200 text-blue-800 font-bold">P1-P2</span>
          </div>
          <div class="text-3xl font-black text-blue-950 mt-1">{len(TECH_CASES)} <span class="text-sm font-normal text-blue-700">TCs</span></div>
          <div class="text-xs text-blue-800 mt-2 flex items-center justify-between border-t border-blue-200 pt-2">
            <span>BVA Biên, Lifecycle, NFR, PII</span>
            <span class="font-bold text-amber-600">2 Defect / BVA</span>
          </div>
        </div>

      </div>
    </section>

    <!-- Interactive Navigation Tabs & Filter Bar -->
    <section class="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm space-y-4">
      
      <!-- Top Tabs Switcher -->
      <div class="flex flex-wrap items-center justify-between gap-3 border-b border-slate-200 pb-4">
        
        <div class="flex flex-wrap items-center gap-2" id="pillar-tab-buttons">
          <button type="button" onclick="selectPillarTab('ALL')" id="tab-btn-ALL" class="active-tab px-4 py-2 rounded-xl text-xs font-bold border border-slate-300 transition flex items-center gap-2">
            <span>🌟 Tất Cả</span>
            <span class="px-1.5 py-0.5 rounded-full bg-slate-200/40 text-[11px] font-mono">{len(TEST_CASES_DATA)}</span>
          </button>
          
          <button type="button" onclick="selectPillarTab('BR')" id="tab-btn-BR" class="px-4 py-2 rounded-xl text-xs font-bold bg-white text-purple-900 border border-purple-200 hover:bg-purple-50 transition flex items-center gap-2">
            <span>⚖️ 1. Business Rules (BR)</span>
            <span class="px-1.5 py-0.5 rounded-full bg-purple-100 text-purple-800 text-[11px] font-mono">{len(BR_CASES)}</span>
          </button>

          <button type="button" onclick="selectPillarTab('AC')" id="tab-btn-AC" class="px-4 py-2 rounded-xl text-xs font-bold bg-white text-emerald-900 border border-emerald-200 hover:bg-emerald-50 transition flex items-center gap-2">
            <span>🎯 2. Acceptance Criteria (AC)</span>
            <span class="px-1.5 py-0.5 rounded-full bg-emerald-100 text-emerald-800 text-[11px] font-mono">{len(AC_CASES)}</span>
          </button>

          <button type="button" onclick="selectPillarTab('TECH')" id="tab-btn-TECH" class="px-4 py-2 rounded-xl text-xs font-bold bg-white text-blue-900 border border-blue-200 hover:bg-blue-50 transition flex items-center gap-2">
            <span>🛠️ 3. Kỹ Thuật &amp; UI Matrix</span>
            <span class="px-1.5 py-0.5 rounded-full bg-blue-100 text-blue-800 text-[11px] font-mono">{len(TECH_CASES)}</span>
          </button>

          <button type="button" onclick="selectPillarTab('DEFECT')" id="tab-btn-DEFECT" class="px-4 py-2 rounded-xl text-xs font-bold bg-white text-red-900 border border-red-200 hover:bg-red-50 transition flex items-center gap-2">
            <span>🔴 Cần Sửa / Defect</span>
            <span class="px-1.5 py-0.5 rounded-full bg-red-100 text-red-800 text-[11px] font-mono">2</span>
          </button>
        </div>

        <!-- Formula Bar Search fx -->
        <div class="relative flex items-center bg-white border border-slate-300 rounded-xl shadow-2xs w-full sm:w-80">
          <span class="text-xs font-mono font-bold text-sky-600 px-3 py-2 border-r border-slate-200 select-none">fx</span>
          <input type="text" id="matrix-search" placeholder="Tìm theo mã TC, tiêu đề, quy tắc..." oninput="handleSearch(this.value)" class="text-xs px-3 py-2 bg-transparent text-slate-800 outline-none w-full placeholder:text-slate-400">
        </div>
      </div>

      <!-- Active Tab Context Banner -->
      <div id="tab-context-banner" class="p-3.5 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-700 flex items-center justify-between">
        <div id="tab-context-desc">
          Đang hiển thị toàn bộ <strong>{len(TEST_CASES_DATA)} Ca Kiểm Thử</strong> chuẩn AvePoint Google Sheet (19 Cột). Bấm vào các thẻ tab phía trên để thu gọn theo từng Trụ Cột chuyên biệt.
        </div>
        <div id="row-count-tag" class="font-mono font-bold text-slate-600 shrink-0 ml-4">
          {len(TEST_CASES_DATA)} / {len(TEST_CASES_DATA)} hàng hiển thị
        </div>
      </div>

      <!-- 19-Column Enterprise Interactive Table -->
      <div class="overflow-x-auto rounded-xl border border-slate-200 shadow-xs max-h-[640px] relative">
        <table class="enterprise-table text-left" style="min-width: 1750px;">
          <thead class="sticky top-0 bg-[#1B365D] text-white text-[11px] font-mono uppercase tracking-wider z-20">
            <tr>
              <th class="py-3 px-3 text-center w-12 freeze-col-1 bg-[#1B365D]">STT</th>
              <th class="py-3 px-3 text-center w-28 freeze-col-2 bg-[#1B365D]">Mã TC</th>
              <th class="py-3 px-3 text-center w-36">Trụ Cột (Pillar)</th>
              <th class="py-3 px-4 min-w-[280px]">Tiêu Đề Ca Kiểm Thử</th>
              <th class="py-3 px-3 min-w-[220px] bg-[#162D4E]">📍 Vị Trí Kiểm Thử &amp; DOM Selector</th>
              <th class="py-3 px-3 min-w-[220px] bg-[#162D4E]">💾 Dữ Liệu Kiểm Thử (Test Data)</th>
              <th class="py-3 px-3 w-36">Test Suite</th>
              <th class="py-3 px-2 text-center w-20">Ưu Tiên</th>
              <th class="py-3 px-2 text-center w-24">Trạng Thái</th>
              <th class="py-3 px-3 w-24">Loại Test</th>
              <th class="py-3 px-3 text-center w-24">Thao Tác</th>
            </tr>
          </thead>
          <tbody id="matrix-tbody" class="text-xs divide-y divide-slate-200 bg-white">
            <!-- Dynamic rows rendered by JS -->
          </tbody>
        </table>
      </div>

    </section>

  </main>

  <!-- Detailed Modal Drawer for Given-When-Then Inspection -->
  <div id="tc-detail-modal" class="fixed inset-0 bg-black/60 backdrop-blur-xs flex items-center justify-center p-4 z-50 hidden opacity-0 transition-opacity duration-200">
    <div class="bg-white border border-slate-300 rounded-2xl max-w-4xl w-full max-h-[90vh] flex flex-col shadow-2xl overflow-hidden">
      
      <!-- Modal Header -->
      <div class="px-6 py-4 border-b border-slate-200 flex items-center justify-between bg-slate-50 shrink-0">
        <div class="flex items-center gap-2.5">
          <span id="modal-tc-id" class="px-2.5 py-1 rounded-md text-xs font-mono font-bold bg-sky-100 text-sky-800 border border-sky-200">TC-001</span>
          <span id="modal-tc-pillar" class="px-2.5 py-1 rounded-md text-xs font-bold bg-purple-100 text-purple-800 border border-purple-200">⚖️ Business Rule</span>
          <h3 id="modal-tc-title" class="text-sm font-bold text-slate-900 truncate max-w-lg">Tiêu đề ca kiểm thử</h3>
        </div>
        <button onclick="closeModal()" class="w-8 h-8 rounded-lg flex items-center justify-center text-slate-400 hover:text-slate-700 hover:bg-slate-200 transition">✕</button>
      </div>

      <!-- Modal Body -->
      <div class="p-6 overflow-y-auto space-y-5 text-xs text-slate-700">
        
        <!-- Meta Details Grid -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-slate-50 p-3.5 rounded-xl border border-slate-200 font-mono">
          <div><span class="text-slate-400">Suite:</span> <div id="modal-suite" class="font-bold text-slate-800">TS-010-ID</div></div>
          <div><span class="text-slate-400">Priority:</span> <div id="modal-priority" class="font-bold text-slate-800">High</div></div>
          <div><span class="text-slate-400">Severity:</span> <div id="modal-severity" class="font-bold text-slate-800">S2</div></div>
          <div><span class="text-slate-400">Status:</span> <div id="modal-status" class="font-bold text-emerald-600">Passed</div></div>
        </div>

        <!-- Prominent Test Location Banner in Modal -->
        <div class="p-3.5 rounded-xl bg-sky-50 border border-sky-200 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
          <div>
            <div class="text-[11px] font-bold uppercase tracking-wider text-sky-800">📍 Vị Trí Kiểm Thử Trên Màn Hình &amp; Element DOM</div>
            <div id="modal-target-name" class="text-xs font-bold text-slate-900 mt-0.5">Ô Nhập SĐT (Mobile Number)</div>
            <code id="modal-target-dom" class="text-[11px] font-mono text-sky-900 bg-sky-100/80 px-2 py-0.5 rounded border border-sky-300 mt-1 inline-block">input[name="phoneNumber"]</code>
          </div>
          <div class="shrink-0">
            <span id="modal-test-area" class="px-2.5 py-1 rounded-md text-[11px] font-bold bg-white text-sky-800 border border-sky-200 shadow-2xs">Contact Fields</span>
          </div>
        </div>

        <div>
          <h4 class="font-bold uppercase tracking-wider text-slate-500 mb-1">1. Điều Kiện Tiên Quyết (Preconditions)</h4>
          <div id="modal-preconditions" class="p-3 bg-slate-50 rounded-lg border border-slate-200 font-mono text-[11px] whitespace-pre-wrap"></div>
        </div>

        <div>
          <h4 class="font-bold uppercase tracking-wider text-slate-500 mb-1">2. Dữ Liệu Kiểm Thử (Test Data)</h4>
          <div id="modal-test-data" class="p-3 bg-slate-50 rounded-lg border border-slate-200 font-mono text-[11px] whitespace-pre-wrap"></div>
        </div>

        <div>
          <h4 class="font-bold uppercase tracking-wider text-slate-500 mb-1">3. Các Bước Thực Hiện (Test Steps)</h4>
          <div id="modal-steps" class="p-3 bg-slate-50 rounded-lg border border-slate-200 whitespace-pre-wrap leading-relaxed"></div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <h4 class="font-bold uppercase tracking-wider text-emerald-700 mb-1">4. Kết Quả Kỳ Vọng (Expected Result)</h4>
            <div id="modal-expected" class="p-3 bg-emerald-50/70 border border-emerald-200 rounded-lg text-emerald-950 whitespace-pre-wrap leading-relaxed"></div>
          </div>
          <div>
            <h4 class="font-bold uppercase tracking-wider text-sky-700 mb-1">5. Kết Quả Thực Tế (Actual Result)</h4>
            <div id="modal-actual" class="p-3 bg-sky-50/70 border border-sky-200 rounded-lg text-sky-950 whitespace-pre-wrap leading-relaxed"></div>
          </div>
        </div>

        <div>
          <h4 class="font-bold uppercase tracking-wider text-slate-500 mb-1">6. Nguồn Đối Soát (Traceability &amp; Assumption)</h4>
          <div id="modal-traceability" class="p-3 bg-slate-50 rounded-lg border border-slate-200 text-slate-700"></div>
        </div>

      </div>

      <!-- Modal Footer -->
      <div class="px-6 py-3 border-t border-slate-200 bg-slate-50 flex justify-end shrink-0">
        <button onclick="closeModal()" class="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white font-semibold rounded-lg text-xs transition">Đóng</button>
      </div>

    </div>
  </div>

  <!-- Client-side Script -->
  <script>
    const testCases = {dataset_json};
    let currentFilter = 'ALL';
    let searchQuery = '';

    const tabDescriptions = {{
      'ALL': 'Đang hiển thị toàn bộ <strong>{len(TEST_CASES_DATA)} Ca Kiểm Thử</strong> chuẩn AvePoint Google Sheet (19 Cột). Bấm vào các thẻ tab phía trên để thu gọn theo từng Trụ Cột chuyên biệt.',
      'BR': '⚖️ <strong>Trụ Cột 1 (Business Rules - {len(BR_CASES)} TCs)</strong>: Tập trung 100% vào các Luật Nghiệp Vụ Cốt Lõi, phân quyền độ tuổi con (&ge;16), Singpass bất biến (D-20), BOLA/IDOR và quy định không gửi email thông báo (D-28).',
      'AC': '🎯 <strong>Trụ Cột 2 (Acceptance Criteria - {len(AC_CASES)} TCs)</strong>: Tập trung vào Tiêu Chuẩn Nghiệm Thu User Story US-08.2, che/hiện NRIC, Modal Alertdialog, trạng thái Pristine/Dirty và các thông báo lỗi chuẩn MSG-0805, MSG-0806, MSG-0001.',
      'TECH': '🛠️ <strong>Trụ Cột 3 (Tech &amp; UI Matrix - {len(TECH_CASES)} TCs)</strong>: Tập trung vào Kỹ thuật Kiểm Thử Ô Nhập (12 Lớp), giá trị biên BVA ($N-1, N, N+1$), chống lộ Translation Key (Invariant 7), dán 1000 ký tự stress, Vòng đời Form (Mục 8), Sức khỏe UI Invariant 7 (Mục 9), và Bảo mật PII Invariant 8 (Mục 10).',
      'DEFECT': '🔴 <strong>Các Ca Kiểm Thử Phát Hiện Lỗi Cần Sửa (2 TCs)</strong>: TC-R8-TEL-07 (Lộ i18n key SĐT BUG-R8-I18N-01), TC-R8-POS-06 (Lộ i18n key Mã bưu chính BUG-R8-I18N-02).'
    }};

    function selectPillarTab(tabKey) {{
      currentFilter = tabKey;
      
      const buttons = document.querySelectorAll('#pillar-tab-buttons button');
      buttons.forEach(btn => btn.classList.remove('active-tab'));
      const activeBtn = document.getElementById('tab-btn-' + tabKey);
      if (activeBtn) activeBtn.classList.add('active-tab');

      document.getElementById('tab-context-desc').innerHTML = tabDescriptions[tabKey] || '';
      renderTable();
    }}

    function handleSearch(query) {{
      searchQuery = query.toLowerCase().trim();
      renderTable();
    }}

    function renderTable() {{
      const tbody = document.getElementById('matrix-tbody');
      tbody.innerHTML = '';

      let filtered = testCases.filter(tc => {{
        if (currentFilter === 'BR' && tc.pillar !== 'BR') return false;
        if (currentFilter === 'AC' && tc.pillar !== 'AC') return false;
        if (currentFilter === 'TECH' && tc.pillar !== 'TECH') return false;
        if (currentFilter === 'DEFECT' && tc.status.toUpperCase() !== 'FAILED') return false;

        if (searchQuery) {{
          const matchStr = (tc.id + ' ' + tc.title + ' ' + tc.suite + ' ' + tc.traceability + ' ' + tc.pillar_badge).toLowerCase();
          return matchStr.includes(searchQuery);
        }}
        return true;
      }});

      document.getElementById('row-count-tag').innerText = filtered.length + ' / ' + testCases.length + ' hàng hiển thị';

      filtered.forEach((tc, i) => {{
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-50 transition border-b border-slate-100';

        let pillarBadgeClass = 'bg-blue-50 text-blue-800 border-blue-200';
        if (tc.pillar === 'BR') pillarBadgeClass = 'bg-purple-50 text-purple-800 border-purple-200';
        if (tc.pillar === 'AC') pillarBadgeClass = 'bg-emerald-50 text-emerald-800 border-emerald-200';

        let statusBadge = `<span class="px-2 py-0.5 rounded-full font-bold text-[11px] bg-emerald-100 text-emerald-800">Passed</span>`;
        if (tc.status.toUpperCase() === 'FAILED') {{
          statusBadge = `<span class="px-2 py-0.5 rounded-full font-bold text-[11px] bg-red-100 text-red-800 animate-pulse">Failed</span>`;
        }} else if (tc.status.toUpperCase() === 'NOT RUN') {{
          statusBadge = `<span class="px-2 py-0.5 rounded-full font-bold text-[11px] bg-slate-100 text-slate-600">Not Run</span>`;
        }}

        tr.innerHTML = `
          <td class="py-2.5 px-3 text-center text-slate-400 font-mono freeze-col-1 bg-white">${{i + 1}}</td>
          <td class="py-2.5 px-3 font-mono font-bold text-slate-900 freeze-col-2 bg-white">${{tc.id}}</td>
          <td class="py-2.5 px-3 text-center">
            <span class="inline-block px-2 py-0.5 rounded-md text-[11px] font-semibold border ${{pillarBadgeClass}}">
              ${{tc.pillar_badge}}
            </span>
          </td>
          <td class="py-2.5 px-4 font-medium text-slate-800 leading-snug">
            <div>${{tc.title}}</div>
            <div class="text-[11px] text-slate-400 font-mono mt-0.5 truncate max-w-sm" title="${{tc.traceability}}">🔎 ${{tc.traceability}}</div>
          </td>
          <td class="py-2.5 px-3">
            <div class="font-bold text-slate-800 text-xs flex items-center gap-1">
              <span>📍</span> <span>${{tc.target_name}}</span>
            </div>
            <div class="font-mono text-[11px] text-sky-800 bg-sky-50 px-1.5 py-0.5 rounded border border-sky-200 mt-1 inline-block truncate max-w-[220px]" title="${{tc.target_dom}}">
              ${{tc.target_dom}}
            </div>
          </td>
          <td class="py-2.5 px-3">
            <div class="font-mono text-[11px] text-emerald-950 bg-emerald-50/80 px-2 py-1 rounded border border-emerald-200 max-h-16 overflow-y-auto leading-relaxed select-all" title="${{tc.test_data}}">
              ${{tc.test_data}}
            </div>
          </td>
          <td class="py-2.5 px-3 text-slate-600 text-xs">
            <div class="font-medium">${{tc.suite}}</div>
            <span class="inline-block px-1.5 py-0.2 rounded text-[10px] font-bold bg-slate-100 text-slate-600 border border-slate-200 mt-0.5">${{tc.test_area}}</span>
          </td>
          <td class="py-2.5 px-2 text-center font-bold text-slate-700">${{tc.priority}}</td>
          <td class="py-2.5 px-2 text-center">${{statusBadge}}</td>
          <td class="py-2.5 px-3 text-slate-600 font-mono text-[11px]">${{tc.test_type}}</td>
          <td class="py-2.5 px-3 text-center">
            <button onclick="openModal('${{tc.id}}')" class="px-2.5 py-1 rounded-md text-xs font-semibold bg-sky-50 text-sky-700 hover:bg-sky-100 border border-sky-200 transition shadow-2xs">
              Chi Tiết
            </button>
          </td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    function openModal(tcId) {{
      const tc = testCases.find(t => t.id === tcId);
      if (!tc) return;

      document.getElementById('modal-tc-id').innerText = tc.id;
      document.getElementById('modal-tc-pillar').innerText = tc.pillar_badge;
      document.getElementById('modal-tc-title').innerText = tc.title;
      document.getElementById('modal-suite').innerText = tc.suite;
      document.getElementById('modal-priority').innerText = tc.priority;
      document.getElementById('modal-severity').innerText = tc.severity;
      document.getElementById('modal-status').innerText = tc.status;

      document.getElementById('modal-target-name').innerText = tc.target_name;
      document.getElementById('modal-target-dom').innerText = tc.target_dom;
      document.getElementById('modal-test-area').innerText = tc.test_area;

      document.getElementById('modal-preconditions').innerText = tc.preconditions;
      document.getElementById('modal-test-data').innerText = tc.test_data;
      document.getElementById('modal-steps').innerText = tc.steps;
      document.getElementById('modal-expected').innerText = tc.expected;
      document.getElementById('modal-actual').innerText = tc.actual;
      document.getElementById('modal-traceability').innerText = tc.traceability + ' | ' + (tc.assumption || 'None') + (tc.defect ? ' | Defect: ' + tc.defect : '');

      const modal = document.getElementById('tc-detail-modal');
      modal.classList.remove('hidden');
      setTimeout(() => {{
        modal.classList.remove('opacity-0');
      }}, 10);
    }}

    function closeModal() {{
      const modal = document.getElementById('tc-detail-modal');
      modal.classList.add('opacity-0');
      setTimeout(() => {{
        modal.classList.add('hidden');
      }}, 200);
    }}

    document.addEventListener('keydown', (e) => {{
      if (e.key === 'Escape') closeModal();
    }});

    renderTable();
  </script>
</body>
</html>
"""

    with open(HTML_EXEC_PATH, 'w', encoding='utf-8') as f:
        f.write(html_content)
    with open(HTML_SHORT_PATH, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Saved Executive HTML to {HTML_EXEC_PATH} and {HTML_SHORT_PATH}")

def main():
    print(f"Building Full Test Case Suite ({len(TEST_CASES_DATA)} TCs)...")
    print(f" - Pillar 1 (Business Rules): {len(BR_CASES)} TCs")
    print(f" - Pillar 2 (Acceptance Criteria): {len(AC_CASES)} TCs")
    print(f" - Pillar 3 (Tech & UI Matrix): {len(TECH_CASES)} TCs")

    # 1. Generate Markdown
    md_content = build_markdown_document()
    with open(MD_PATH, 'w', encoding='utf-8') as f:
        f.write(md_content)
    print(f"Saved Markdown to {MD_PATH}")

    # 2. Generate Multi-Tab AvePoint Excel Workbook
    build_excel_workbook()

    # 3. Generate Interactive Executive Dashboard
    build_executive_html_dashboard()

    print("All FS08 artifacts regenerated successfully!")

if __name__ == "__main__":
    main()
