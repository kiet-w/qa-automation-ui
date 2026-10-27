#!/usr/bin/env python3
"""
Generate the fully expanded, 67-case TC_FS08_Parent_Profile.md
incorporating the Universal Input Field Testing Matrix and Anti-i18n Key Leakage rules.
"""
import sys
from pathlib import Path

def generate_markdown():
    output_path = Path("testcases/fs08/fs08-parent-profile/TC_FS08_Parent_Profile.md")
    
    header = """# BỘ ĐẶC TẢ TEST CASE CHUẨN GOOGLE SHEET (19 CỘT) — FS08: MY DETAILS / PARENT PROFILE
## MOE SINGAPORE EDUSAVE E-SERVICE PORTAL (`http://localhost:5174/profile`)

> **Quy chuẩn Format**: Bám sát 100% định dạng bảng tính Google Sheet Tender AvePoint (19 Cột):  
> [Google Sheet Reference (gid=1612531667)](https://docs.google.com/spreadsheets/d/1ViSPLgggDsBI13SCPjfO_i0QoyUXy35A/edit?gid=1612531667#gid=1612531667)
> 
> **File Excel Đi Kèm**: [`TC_FS08_Parent_Profile.xlsx`](TC_FS08_Parent_Profile.xlsx)  
> **Nguyên tắc Invariant 6**: Zero Assumptions — 100% kịch bản, quy tắc biên, mã lỗi đối soát trực tiếp từ FSD `FR-08.3`, Bảng trường Mục 6, Quyết định `D-20`/`D-28` và DOM thật từ BSK.  
> **Kiến trúc Test Suite Granular & Universal Input Field Matrix**: Áp dụng triệt để Bộ Ma Trận Kiểm Thử Mọi Ô Nhập Liệu (12 Lớp Kiểm Thử Chung + 4 Phân Nhóm Ô Nhập + Anti-i18n Key Leakage Rule) cho toàn bộ 8 input fields và controls giao diện thành 12 Test Suites chuyên biệt với **67 Test Cases** độc lập.

---

## 1. TỔNG QUAN PHÂN BỔ TEST SUITES & CÁC INPUT COMPONENT

| STT | Scenario ID | Tên Test Suite / Component Phụ Trách | Loại Phần Tử / Trường Dữ Liệu | Kỹ Thuật QA Kiểm Thử | Số Lượng TC | Mức Ưu Tiên |
| :-: | :---: | :--- | :--- | :--- | :-: | :---: |
| 1 | `TS-010-ID` | **SingPass Identity & PII** | Full Name, Residential Address, NRIC | Read-only check, DOM inspection, Toggle masking, API tampering | 4 | P0 / Smoke |
| 2 | `TS-010-TEL` | **Mobile Number Component** | `phoneNumber` (Input Tel) | EP (6/8/9), BVA (7/8/9), Trim space, Full-width, MSG-0805, MSG-0001, Anti-i18n Key Leak, Viền đỏ | 10 | P0 / Smoke |
| 3 | `TS-010-EML` | **Email Address Component** | `email` (Input Email) | RFC 5322 syntax, BVA (150/151 chars), Space, 1000 chars paste, MSG-0806, MSG-0001, Anti-i18n Leak | 8 | P0 / Smoke |
| 4 | `TS-010-BLK` | **Mailing Block Component** | `mailingBlock` (Input Text) | Optional check, BVA (20/21 chars), Alphanumeric, Address symbols vs Forbidden chars | 4 | P1 |
| 5 | `TS-010-UNT` | **Mailing Unit Component** | `mailingUnit` (Input Text) | Optional check, BVA (20/21 chars), SG unit notation (#12-34), Forbidden chars, Multiline | 4 | P1 |
| 6 | `TS-010-STR` | **Mailing Street Component** | `mailingStreet` (Input Text) | Mandatory check, BVA (100/101 chars), Whitespace ASM-15, Punctuation, Forbidden chars, 1000 chars, XSS | 7 | P0 / P1 |
| 7 | `TS-010-POS` | **Mailing Postal Code Component** | `mailingPostalCode` (Input Text) | Exact 6 digits, Leading zero (018956), BVA (5/6/7), Full-width, MSG-0001, Anti-i18n Key Leak, Viền đỏ | 8 | P0 / Smoke |
| 8 | `TS-010-CTY` | **Mailing Country Component** | `mailingCountry` (Input Text) | Default 'Singapore', Text-only (reject digits), BVA (100/101), Diacritics, Whitespace ASM-15 | 6 | P1 |
| 9 | `TS-010-STA` | **Form State & Mode Transitions** | Update button, Cancel, Save button | View $\\leftrightarrow$ Edit mode, Pristine disabled, Dirty enabled, Restore baseline | 4 | P0 / Smoke |
| 10 | `TS-010-SUB` | **Submission & Confirm Dialog** | Alertdialog modal, Save trigger | Modal Keep editing vs Save, Debounce, MSG-0807 toast, MSG-0808 500 fault injection | 5 | P0 / P1 |
| 11 | `TS-010-AGE` | **Child Age Access & Isolation** | Phân quyền theo tuổi con & phụ huynh | Con $\\ge 16$ lock view-only, Con $< 16$ editable, BOLA/IDOR MSG-0003, Record isolation | 4 | P0 / P1 |
| 12 | `TS-010-NFR` | **Security & UI Health** | Toàn bộ trang `/profile` | Invariant 7: 0 console errors, 0 overflow, WCAG 2.1 AA, PII protection | 3 | P0 / Smoke |
| | **TỔNG** | **12 TEST SUITES ĐỘC LẬP** | **Toàn bộ 8 input fields & UI controls** | **Universal Input Field Matrix (EP, BVA, Anti-i18n, Security, A11y)** | **67** | **P0 - P2** |

---

## 2. MA TRẬN TEST CASE ĐẦY ĐỦ 19 CỘT CHUẨN GOOGLE SHEET AVEPOINT

| ID | Scenario ID | Title | Test Suite | Page | Severity | Priority | Execution Status | Test Type | Environment | Preconditions | Test Data | Test Steps | Expected Result | Actual Result | Assumption Ref | Defect ID | Traceability | Note |
| :-: | :-: | :--- | :--- | :--- | :-: | :-: | :-: | :-: | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
"""

    rows = [
        # =========================================================================
        # 1. TS-010-ID - SingPass Identity & PII (4 TCs)
        # =========================================================================
        (
            "TC-R8-094", "TS-010-ID",
            "Verify SingPass verified identity displays Full Name, NRIC and Residential Address as strictly read-only",
            "SingPass Identity & PII", "Parent Portal > Profile", "S2", "High", "Passed", "UI",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; on /profile page (View Mode)",
            "Parent FA (Tan Wei Ming); NRIC: S1234123F; Residential: Blk 123 Ang Mo Kio Ave 3 #08-1234 S560123",
            "1. Navigate to /profile<br>2. Inspect Full Name, NRIC, and Residential Address elements<br>3. Verify absence of <input> tags for these identity fields",
            "Full Name, NRIC, and Residential Address are rendered as static text/read-only tags<br>No input fields exist for Full Name or Residential Address<br>Edit button [Update details] is visible",
            "Verified: Full Name and Residential Address are static text without editable inputs.",
            "TD: BSK Live DOM verified locator dt:has-text('Residential') + dd", "",
            "FR-08.3; FS R8 sec. 6 field table; D-20; AC #18",
            "Read-only SingPass identity fields cannot be modified by user."
        ),
        (
            "TC-R8-095", "TS-010-ID",
            "Verify residential address cannot be edited and is immutable in Edit Mode",
            "SingPass Identity & PII", "Parent Portal > Profile", "S2", "High", "Passed", "Functional",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; enter Edit Mode via [Update details]",
            "Parent FA; Residential: Blk 123 Ang Mo Kio Ave 3 #08-1234 S560123",
            "1. Click [Update details] to switch to Edit Mode<br>2. Attempt to locate an input field for Residential Address<br>3. Check legal notice text",
            "No editable input exists for Residential Address in Edit Mode<br>Legal notice displayed: 'Residential address is maintained via Government Digital Services and cannot be edited in this portal.'<br>Value remains unchanged",
            "Verified: Residential address remains static and locked during Edit Mode.",
            "CR: D-20 decision confirms residential address is strictly read-only from Singpass", "",
            "FR-08.3 rules (D-20); R8-AC18",
            "Prevents unauthorized address modification."
        ),
        (
            "TC-R8-096", "TS-010-ID",
            "Verify API rejects or ignores any tampering attempt to update read-only SingPass identity fields",
            "SingPass Identity & PII", "API Service", "S1 (highest)", "Critical", "Not Run", "Security",
            "SIT<br>API client (Postman/Playwright API) + DevTools<br>Mock SingPass + mock data API",
            "FA logged in with valid bearer token",
            'Payload tampering: {"fullName": "HACKED NAME", "nric": "T9999999Z", "residentialStreet": "Malicious Street"}',
            "1. Intercept PUT/PATCH profile update request<br>2. Inject read-only identity fields into JSON payload<br>3. Send request to backend<br>4. Inspect backend response and reload profile",
            "API ignores injected read-only fields or rejects request with HTTP 400 Bad Request<br>Parent profile in DB retains original Full Name, NRIC, and Residential Address",
            "Server-side schema validation strips unauthorized fields.",
            "TD: Server-side schema validation strips unauthorized fields", "",
            "FR-08.3 rules; NFR Security; Invariant 8",
            "Guarantees server-side defense against parameter tampering."
        ),
        (
            "TC-R8-ATM-01", "TS-010-ID",
            "Verify NRIC masking and reveal toggle button switches between Show and Hide state",
            "SingPass Identity & PII", "Parent Portal > Profile", "S2", "High", "Passed", "UI",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; on /profile page (View Mode)",
            "NRIC: '*****123F' <-> 'S1234123F'",
            "1. Check initial state: NRIC masked ('*****123F'), button label 'Show NRIC'<br>2. Click 'Show NRIC' button<br>3. Verify unmasked NRIC ('S1234123F') and button label switches to 'Hide NRIC'<br>4. Click 'Hide NRIC' button<br>5. Verify NRIC re-masks to '*****123F' and button returns to 'Show NRIC'",
            "NRIC toggles accurately between masked and unmasked representation<br>Button text dynamically updates ('Show NRIC' <-> 'Hide NRIC')<br>Zero layout shift (CLS = 0)",
            "NRIC toggles correctly between masked and unmasked state with zero layout shift.",
            "TD: BSK Live DOM verified locator button:has-text('Show NRIC')", "",
            "FR-08.3; BR-08-09.1; AC #10; NFR Security",
            "Protects PII against shoulder surfing in public spaces."
        ),

        # =========================================================================
        # 2. TS-010-TEL - Mobile Number Component (10 TCs)
        # =========================================================================
        (
            "TC-R8-098", "TS-010-TEL",
            "Verify Singapore mobile numbers starting with valid prefixes 6, 8, and 9 are accepted",
            "Mobile Number Component", "Parent Portal > Profile", "S3", "Medium", "Passed", "Functional",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; Edit Mode open",
            "EP Valid: 61234567, 81234567, 91234567",
            "1. In Edit Mode, enter mobile number '61234567' and save<br>2. Enter mobile number '81234567' and save<br>3. Enter mobile number '91234567' and save",
            "All 3 numbers starting with 6, 8, and 9 pass validation without inline errors<br>Profile updates successfully with success toast MSG-0807",
            "All 3 valid Singapore prefixes accepted and saved with MSG-0807.",
            "CR: Singapore National Numbering Plan standard 8-digit mobile prefixes 6, 8, 9", "",
            "FR-08.3; FS R8 field table (Mobile); R8-AC14",
            "Covers Equivalence Partitioning for valid SG phone prefixes."
        ),
        (
            "TC-R8-099", "TS-010-TEL",
            "Verify invalid mobile numbers containing letters or mixed alphanumeric are rejected with MSG-0805",
            "Mobile Number Component", "Parent Portal > Profile", "S2", "High", "Passed", "Functional",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; Edit Mode open",
            "EP Invalid: '12345qqqq', '9123abcd', 'abcdefgh'",
            "1. Enter '12345qqqq' into Mobile Number input<br>2. Blur the field or click Save changes<br>3. Inspect inline validation error message and input border",
            "System rejects submission and displays MSG-0805: 'Enter a mobile number in the correct format, like 9123 4567'<br>Input field highlights with red glowing border (aria-invalid='true')<br>Confirm Dialog is blocked",
            "Invalid alphanumeric phone rejected; displays inline error and marks field invalid.",
            "TD: Regex /^[689]\\d{7}$/ enforced on blur and submit", "",
            "FR-08.3 errors; R8-AC15; MSG-0805",
            "Prevents malformed phone records in database."
        ),
        (
            "TC-R8-TEL-01", "TS-010-TEL",
            "Verify mobile numbers starting with invalid prefixes (1, 2, 3, 4, 5, 7) are rejected with MSG-0805",
            "Mobile Number Component", "Parent Portal > Profile", "S2", "High", "Passed", "Functional",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; Edit Mode open",
            "Invalid prefixes: '71234567', '51234567', '11234567', '21234567'",
            "1. Enter '71234567' and blur<br>2. Enter '51234567' and blur<br>3. Verify error message on each attempt",
            "Validation fails on each invalid prefix<br>Displays MSG-0805: 'Enter a mobile number in the correct format, like 9123 4567'<br>Save button blocked from dispatching mutation",
            "Displays MSG-0805 for non-6/8/9 starting digits.",
            "CR: Singapore telecom standard restricts mobile services to 8/9 (and 6 for fixed-line/unified)", "",
            "FR-08.3 errors; R8-AC15; MSG-0805",
            "Negative testing of Singapore phone prefix boundary."
        ),
        (
            "TC-R8-TEL-02", "TS-010-TEL",
            "Verify mobile number length boundary: 7 digits and 9 digits are rejected with MSG-0805 (BVA Length)",
            "Mobile Number Component", "Parent Portal > Profile", "S3", "High", "Passed", "BVA",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; Edit Mode open",
            "BVA Length: 7 digits ('9123456' - underflow), 9 digits ('912345678' - overflow)",
            "1. Enter 7-digit number '9123456' and trigger validation<br>2. Enter 9-digit number '912345678' and trigger validation",
            "Both 7-digit and 9-digit inputs are rejected<br>Displays MSG-0805: 'Enter a mobile number in the correct format, like 9123 4567'<br>No data is committed to DB",
            "Rejected with MSG-0805 for length != 8 digits.",
            "TD: BVA 2-point test on exact 8-digit Singapore phone length constraint", "",
            "FS R8 sec. 6 field table; R8-AC15; MSG-0805",
            "Boundary Value Analysis (N-1 = 7, N+1 = 9)."
        ),
        (
            "TC-R8-TEL-03", "TS-010-TEL",
            "Verify clearing mandatory Mobile Number input triggers required validation error MSG-0001",
            "Mobile Number Component", "Parent Portal > Profile", "S2", "High", "Passed", "Functional",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; Edit Mode open",
            "Mobile number = '' (empty string)",
            "1. Clear the Mobile Number input field completely<br>2. Blur the field or click [Save changes]",
            "Displays required field error MSG-0001: 'Enter your mobile number' (or 'This field is required')<br>Input marked with aria-invalid='true' and red border<br>Save button is disabled",
            "MSG-0001 displayed under Mobile Number field; save action blocked.",
            "CR: Mandatory field rule per FSD section 6 table", "BUG-R8-005",
            "FR-08.3 errors; R8-AC16; MSG-0001",
            "Mandatory field check for contact phone."
        ),
        (
            "TC-R8-TEL-04", "TS-010-TEL",
            "Verify whitespace-only Mobile Number input is treated as empty and triggers MSG-0001 (ASM-15)",
            "Mobile Number Component", "Parent Portal > Profile", "S4 (lowest)", "Medium", "Passed", "Functional",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; Edit Mode open",
            "Mobile number = '        ' (8 blank spaces)",
            "1. Enter multiple spaces into Mobile Number input<br>2. Trigger validation by blurring or clicking Save",
            "Whitespace is trimmed and treated as empty input<br>Displays required field error MSG-0001<br>Nothing is saved to database",
            "Whitespace trimmed; required field validation triggered.",
            "ASM-15: Whitespace-only input in a required field is treated as blank.", "",
            "FR-08.3 errors; ASM-15; MSG-0001",
            "Prevents bypassing mandatory checks with spaces."
        ),
        (
            "TC-R8-100", "TS-010-TEL",
            "Verify mobile number entered with space is accepted and trimmed upon saving (ASM-08)",
            "Mobile Number Component", "Parent Portal > Profile", "S4 (lowest)", "Low", "Passed", "Functional",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; Edit Mode open",
            "Input: '9123 4567' -> Stored value: '91234567'",
            "1. Enter '9123 4567' (with middle space) in Mobile Number<br>2. Click [Save changes] and confirm in dialog<br>3. Verify UI toast and check stored value upon reload",
            "Input is accepted without error<br>Saved successfully with MSG-0807<br>Stored and rendered as '91234567' (space stripped cleanly)",
            "Saved with MSG-0807; stored value normalized to 91234567.",
            "ASM-08: Mobile number entered with a space ('9123 4567') is accepted and stored without the space.", "",
            "FS R8 field table (example format '9123 4567')",
            "User-friendly auto-trimming of typical phone formatting spaces."
        ),
        (
            "TC-R8-TEL-05", "TS-010-TEL",
            "Verify mobile numbers with decimals, negative signs, or symbols (+, -) are rejected with MSG-0805",
            "Mobile Number Component", "Parent Portal > Profile", "S3", "Medium", "Passed", "Functional",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; Edit Mode open",
            "Symbols & math: '91.234567', '-9123456', '+6591234567', '9123-4567'",
            "1. Enter '91.234567' and blur<br>2. Enter '-9123456' and blur<br>3. Enter '+6591234567' and blur",
            "All non-digit formatted strings are rejected<br>Displays MSG-0805: 'Enter a mobile number in the correct format, like 9123 4567'<br>Save action is blocked",
            "Mathematical notations and symbols rejected per MSG-0805.",
            "TD: Strict 8-digit regex without international + or separators", "",
            "FR-08.3; FS R8 field table; MSG-0805",
            "Singapore local mobile numbers are strictly 8 digits."
        ),
        (
            "TC-R8-TEL-06", "TS-010-TEL",
            "Verify full-width Unicode digits ('９１２３４５６７') are handled safely and rejected or normalized",
            "Mobile Number Component", "Parent Portal > Profile", "S4 (lowest)", "Low", "Passed", "Functional",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; Edit Mode open",
            "Full-width digits: '９１２３４５６７'",
            "1. Enter full-width digits '９１２３４５６７' into Mobile Number<br>2. Trigger blur or click Save changes<br>3. Inspect UI response",
            "System safely rejects non-ASCII digits with MSG-0805 or normalizes to ASCII '91234567'<br>Zero JavaScript crashes or uncaught exceptions",
            "Full-width digits handled safely without crash.",
            "TD: Unicode full-width numeric block handling", "",
            "Invariant 7; NFR Usability",
            "Ensures system stability when pasting East Asian input."
        ),
        (
            "TC-R8-TEL-07", "TS-010-TEL",
            "Verify invalid mobile number displays human-readable error MSG-0805, red border, and strictly NO raw i18n key leakage",
            "Mobile Number Component", "Parent Portal > Profile", "S1 (highest)", "Critical", "Failed", "UI",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; Edit Mode open",
            "Invalid input: '12345qqqq'",
            "1. Enter '12345qqqq' into Mobile Number input<br>2. Trigger blur event on the input<br>3. Inspect the rendered validation error message text and input class/attributes<br>4. Verify error text does NOT match raw key 'features.parentProfile.validation.mobileInvalid'",
            "Input field receives red glowing border and aria-invalid='true'<br>Validation message renders human-readable text matching MSG-0805 ('Enter a mobile number in the correct format, like 9123 4567')<br>NO raw i18n translation key (e.g. 'features.parentProfile.validation.mobileInvalid') is leaked on the DOM",
            "DEFECT: UI currently displays raw un-translated i18n key 'features.parentProfile.validation.mobileInvalid' instead of localized MSG-0805.",
            "Mandate: Zero Raw i18n Key Leakage across UI surface", "BUG-R8-I18N-01",
            "FR-08.3 errors; MSG-0805; Invariant 7 UI Health",
            "Direct verification of image defect reported by user."
        ),

        # =========================================================================
        # 3. TS-010-EML - Email Address Component (8 TCs)
        # =========================================================================
        (
            "TC-R8-EML-01", "TS-010-EML",
            "Verify valid email formats including subdomains, plus-addressing, dots, and uppercase are accepted",
            "Email Address Component", "Parent Portal > Profile", "S3", "Medium", "Passed", "Functional",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; Edit Mode open",
            "EP Valid: 'weiming.tan@example.sg', 'parent+moe@gmail.com', 'ABC@GMAIL.COM', ' abc@gmail.com '",
            "1. Enter each valid email format and save<br>2. Verify successful persistence and lowercase normalization",
            "All valid email variants pass validation cleanly<br>Profile updates successfully with MSG-0807 toast<br>Leading/trailing spaces trimmed cleanly",
            "Valid emails with dots, hyphens, plus-signs, and subdomains accepted.",
            "TD: Standard email RFC compliance", "",
            "FR-08.3; FS R8 sec. 6 field table; R8-AC14",
            "Ensures legitimate government and corporate emails are supported."
        ),
        (
            "TC-R8-101", "TS-010-EML",
            "Verify invalid email formats are rejected with error MSG-0806 (RFC 5322 Syntax Permutations)",
            "Email Address Component", "Parent Portal > Profile", "S2", "High", "Passed", "Functional",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; Edit Mode open",
            "EP Invalid: 'nameexample.com' (no @), 'name@' (no domain), '@example.com' (no local), 'abc@@gmail.com', 'abc@gmail..com', 'abc@gmail,com', 'abc@gmail.c'",
            "1. For each invalid email format, enter into Email input and blur<br>2. Verify inline error presentation and red border",
            "Validation rejects each invalid syntax<br>Displays MSG-0806: 'Enter an email address in the correct format, like name@example.com'<br>Input highlights with aria-invalid='true'<br>Submission blocked",
            "Displays inline validation error for malformed email strings.",
            "CR: Standard RFC 5322 regex validation", "BUG-R8-004",
            "FR-08.3 errors; R8-AC15; MSG-0806",
            "Covers equivalence partitions for invalid email syntax."
        ),
        (
            "TC-R8-102", "TS-010-EML",
            "Verify email maximum length limit boundary of 150 characters (BVA Length)",
            "Email Address Component", "Parent Portal > Profile", "S3", "Medium", "Passed", "BVA",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; Edit Mode open",
            "BVA: 150 chars ('a'*138 + '@example.com') vs 151 chars ('a'*139 + '@example.com')",
            "1. Enter valid 150-char email address, click [Save changes] and confirm<br>2. Enter 151-char email address and attempt save",
            "150 chars: Accepted and saved successfully with MSG-0807<br>151 chars: Input truncated by maxlength='150' or rejected with inline validation error",
            "150 chars saved with MSG-0807; 151 chars prevented by field length constraint.",
            "ASM-09: No message code is defined for max-length; field-level validation blocks Save.", "",
            "FS R8 field table (Email max 150) - BVA; Appendix A Parent_Profile.Email NVARCHAR(150)",
            "Protects against database column buffer overflow."
        ),
        (
            "TC-R8-EML-02", "TS-010-EML",
            "Verify email address containing space is rejected with MSG-0806",
            "Email Address Component", "Parent Portal > Profile", "S3", "Medium", "Passed", "Functional",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; Edit Mode open",
            "Input: 'name @example.com', 'name@ example.com', 'a b@gmail.com'",
            "1. Enter 'name @example.com' into Email input<br>2. Attempt to save form",
            "Validation detects illegal whitespace within email address<br>Displays MSG-0806: 'Enter an email address in the correct format, like name@example.com'<br>Save action blocked",
            "Rejected with MSG-0806 due to embedded whitespace.",
            "CR: RFC 5322 forbids unquoted spaces in email addresses", "",
            "FR-08.3 errors; R8-AC15; MSG-0806",
            "Prevents broken email addresses from entering mail queue."
        ),
        (
            "TC-R8-EML-03", "TS-010-EML",
            "Verify clearing mandatory Email Address input triggers required error MSG-0001",
            "Email Address Component", "Parent Portal > Profile", "S2", "High", "Passed", "Functional",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; Edit Mode open",
            "Email = '' (empty string)",
            "1. Clear the Email input field completely<br>2. Blur field or click [Save changes]",
            "Displays required field error MSG-0001: 'Enter your email' (or 'This field is required')<br>Input marked with aria-invalid='true'<br>Save button disabled",
            "MSG-0001 displayed under Email field; save blocked.",
            "CR: Email is mandatory field per FSD section 6 table", "BUG-R8-005",
            "FR-08.3 errors; R8-AC16; MSG-0001",
            "Mandatory email field validation."
        ),
        (
            "TC-R8-EML-04", "TS-010-EML",
            "Verify whitespace-only Email input is treated as empty and triggers MSG-0001 (ASM-15)",
            "Email Address Component", "Parent Portal > Profile", "S4 (lowest)", "Low", "Passed", "Functional",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; Edit Mode open",
            "Email = '       ' (blank spaces)",
            "1. Enter multiple spaces into Email input<br>2. Trigger validation by blurring or clicking Save",
            "Whitespace is trimmed and treated as empty input<br>Displays required field error MSG-0001<br>Nothing is saved to database",
            "Whitespace trimmed; required field validation MSG-0001 displayed.",
            "ASM-15: Whitespace-only input in a required field is treated as blank.", "",
            "FR-08.3 errors; ASM-15; MSG-0001",
            "Prevents space injection bypassing mandatory check."
        ),
        (
            "TC-R8-EML-05", "TS-010-EML",
            "Verify pasting 1000-character string into Email input is handled safely without browser freeze or layout break",
            "Email Address Component", "Parent Portal > Profile", "S3", "Medium", "Passed", "Stress",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; Edit Mode open",
            "Paste stress: 'A'*1000",
            "1. Paste 1000-character alphanumeric string into Email input<br>2. Inspect UI response and layout<br>3. Attempt save",
            "Browser does not freeze<br>Input is truncated to maxlength='150' or rejected with MSG-0806<br>No horizontal layout overflow occurs",
            "Paste handled safely; input truncated to max length without layout break.",
            "TD: Browser DOM event clipboard paste stress testing", "",
            "Invariant 7; NFR Usability",
            "Ensures resilience against long paste buffers."
        ),
        (
            "TC-R8-EML-06", "TS-010-EML",
            "Verify invalid email displays localized error, red border, and strictly NO raw i18n translation key",
            "Email Address Component", "Parent Portal > Profile", "S2", "High", "Passed", "UI",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; Edit Mode open",
            "Invalid email: 'invalid-email-format'",
            "1. Enter 'invalid-email-format' into Email input<br>2. Blur the input<br>3. Inspect the error alert text and aria-invalid attribute",
            "Input field highlights with red border and aria-invalid='true'<br>Displays readable message matching MSG-0806 ('Enter an email address in the correct format, like name@example.com')<br>NO raw key (e.g. 'features.parentProfile.validation.emailInvalid') is leaked",
            "Displays human-readable error text; no raw i18n translation key leaked.",
            "Mandate: Zero Raw i18n Key Leakage across UI surface", "",
            "FR-08.3 errors; MSG-0806; Invariant 7 UI Health",
            "Guarantees professional localized UI error presentation."
        ),

        # =========================================================================
        # 4. TS-010-BLK - Mailing Block Component (4 TCs)
        # =========================================================================
        (
            "TC-R8-105", "TS-010-BLK",
            "Verify optional Mailing Block can be left blank and saved successfully",
            "Mailing Block Component", "Parent Portal > Profile", "S4 (lowest)", "Low", "Passed", "Functional",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; Edit Mode open",
            "MailingBlock = '' (empty); other required fields valid",
            "1. Clear Mailing Block input field<br>2. Fill all other required fields with valid values<br>3. Click [Save changes] and confirm in dialog",
            "Form passes validation without error<br>Profile updates successfully with MSG-0807<br>Reloading shows empty Mailing Block",
            "Blank Mailing Block saved successfully with MSG-0807.",
            "CR: FSD section 6 table defines Mailing Block as optional (Bắt buộc: Không)", "",
            "FS R8 sec. 6 field table (Mailing block optional); Appendix A Parent_Profile.MailingBlock",
            "Landed properties and private estates often do not have block numbers."
        ),
        (
            "TC-R8-BLK-01", "TS-010-BLK",
            "Verify alphanumeric Mailing Block values (e.g. 'Blk 123A', 'Tower 2', '123', 'A') are saved accurately",
            "Mailing Block Component", "Parent Portal > Profile", "S3", "Medium", "Passed", "Functional",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; Edit Mode open",
            "Valid blocks: 'Blk 123A', 'Tower 2', 'Block 9B', '123', 'A'",
            "1. Enter 'Blk 123A' into Mailing Block<br>2. Save and reload profile",
            "Block value persists accurately and renders 'Blk 123A' on view screen<br>Saved with MSG-0807",
            "Alphanumeric block string saved and reloaded accurately.",
            "TD: Standard alphanumeric address text field", "",
            "FS R8 sec. 6 field table; Appendix A",
            "Supports common HDB and Condo block naming schemes."
        ),
        (
            "TC-R8-106", "TS-010-BLK",
            "Verify Mailing Block maximum length boundary of 20 characters (BVA Length)",
            "Mailing Block Component", "Parent Portal > Profile", "S4 (lowest)", "Low", "Passed", "BVA",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; Edit Mode open",
            "BVA: 20 chars ('B'*20) vs 21 chars ('B'*21)",
            "1. Enter 20-character string into Mailing Block, save and verify<br>2. Enter 21-character string into Mailing Block and attempt save",
            "20 chars: Successfully saved with MSG-0807<br>21 chars: Truncated by maxlength='20' attribute or blocked with field length error",
            "20 chars accepted and saved; 21 chars prevented by input length constraint.",
            "ASM-09: No message code defined for max-length; field-level validation blocks Save.", "",
            "FS R8 field table (Block max 20) - BVA; Appendix A Parent_Profile.MailingBlock NVARCHAR(20)",
            "Prevents database truncation error in Parent_Profile table."
        ),
        (
            "TC-R8-BLK-02", "TS-010-BLK",
            "Verify Mailing Block allows address symbols (/ , . - #) and rejects forbidden symbols (< > { } ;) or 1000-char paste",
            "Mailing Block Component", "Parent Portal > Profile", "S3", "Medium", "Passed", "Functional",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; Edit Mode open",
            "Allowed: 'Blk 12-A/B #01'; Forbidden: '<script>', '{blk}'",
            "1. Enter 'Blk 12-A/B #01' and verify save<br>2. Enter '<script>' and verify rejection or sanitization<br>3. Paste 1000 characters",
            "Legitimate punctuation saved accurately<br>Dangerous HTML symbols sanitized or blocked<br>1000 chars truncated to maxlength='20'",
            "Address punctuation accepted; dangerous symbols sanitized; length bounded.",
            "TD: Address field character whitelist and boundary protection", "",
            "NFR Security; Invariant 8",
            "Protects input integrity across address components."
        ),

        # =========================================================================
        # 5. TS-010-UNT - Mailing Unit Component (4 TCs)
        # =========================================================================
        (
            "TC-R8-UNT-01", "TS-010-UNT",
            "Verify optional Mailing Unit can be left blank and saved successfully",
            "Mailing Unit Component", "Parent Portal > Profile", "S4 (lowest)", "Low", "Passed", "Functional",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; Edit Mode open",
            "MailingUnit = '' (empty); other required fields valid",
            "1. Clear Mailing Unit input field<br>2. Save form and confirm in dialog",
            "Form passes validation without error<br>Profile updates successfully with MSG-0807<br>Reloading shows empty Mailing Unit",
            "Blank Mailing Unit saved successfully with MSG-0807.",
            "CR: FSD section 6 table defines Mailing Unit as optional (Bắt buộc: Không)", "",
            "FS R8 sec. 6 field table (Mailing unit optional); Appendix A Parent_Profile.MailingUnit",
            "Landed houses (bungalows, terraces) do not possess unit numbers."
        ),
        (
            "TC-R8-UNT-03", "TS-010-UNT",
            "Verify standard Singapore apartment unit notation (e.g. '#02-01', '#12-345', '12-34A', 'Level 2') is saved accurately",
            "Mailing Unit Component", "Parent Portal > Profile", "S3", "Medium", "Passed", "Functional",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; Edit Mode open",
            "Unit inputs: '#02-01', '#12-345', '12-34A', 'Level 2'",
            "1. Enter '#02-01' into Mailing Unit<br>2. Save and reload profile",
            "Unit string persists accurately and renders '#02-01' on view screen<br>Saved with MSG-0807",
            "Standard unit format saved and displayed correctly.",
            "TD: Standard Singapore address unit notation with '#' and hyphen", "",
            "FS R8 sec. 6 field table; Appendix A",
            "Typical HDB/condo floor-and-unit format."
        ),
        (
            "TC-R8-UNT-02", "TS-010-UNT",
            "Verify Mailing Unit maximum length boundary of 20 characters (BVA Length)",
            "Mailing Unit Component", "Parent Portal > Profile", "S4 (lowest)", "Low", "Passed", "BVA",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; Edit Mode open",
            "BVA: 20 chars ('#12-123456789012345') vs 21 chars ('#12-1234567890123456')",
            "1. Enter 20-character string into Mailing Unit, save and verify<br>2. Enter 21-character string into Mailing Unit and attempt save",
            "20 chars: Successfully saved with MSG-0807<br>21 chars: Truncated by maxlength='20' attribute or blocked with field length error",
            "20 chars accepted; 21 chars blocked by field constraint.",
            "ASM-09: No message code defined for max-length; field-level validation blocks Save.", "",
            "FS R8 field table (Unit max 20) - BVA; Appendix A Parent_Profile.MailingUnit NVARCHAR(20)",
            "Protects against database column buffer overflow."
        ),
        (
            "TC-R8-UNT-04", "TS-010-UNT",
            "Verify forbidden symbols (< > { } ;) in Mailing Unit are rejected and multiline paste handles newlines gracefully",
            "Mailing Unit Component", "Parent Portal > Profile", "S3", "Medium", "Passed", "Functional",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; Edit Mode open",
            "Forbidden: '<script>', '{01-02}'; Multiline: '#02-01\\nTower A'",
            "1. Enter '<script>' in Mailing Unit and blur<br>2. Paste multiline string '#02-01\\nTower A'<br>3. Inspect input state",
            "HTML script tags are sanitized or rejected<br>Newlines in multiline paste are stripped/collapsed into single space without crashing layout",
            "Forbidden characters blocked; multiline newlines stripped cleanly.",
            "TD: Input sanitization and newline normalization", "",
            "NFR Security; Invariant 8",
            "Prevents malformed addresses and UI disruption."
        ),

        # =========================================================================
        # 6. TS-010-STR - Mailing Street Component (7 TCs)
        # =========================================================================
        (
            "TC-R8-STR-01", "TS-010-STR",
            "Verify clearing mandatory Mailing Street input triggers required validation error MSG-0001",
            "Mailing Street Component", "Parent Portal > Profile", "S2", "High", "Passed", "Functional",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; Edit Mode open",
            "MailingStreet = '' (empty string)",
            "1. Clear Mailing Street input field<br>2. Blur field or click [Save changes]",
            "Displays required error MSG-0001: 'Enter your street' (or 'This field is required')<br>Input marked with aria-invalid='true'<br>Save button disabled",
            "MSG-0001 displayed under Mailing Street; submission blocked.",
            "CR: Mailing Street is mandatory per FSD section 6 table", "BUG-R8-005",
            "FR-08.3 errors; R8-AC16; MSG-0001",
            "Mandatory address street validation."
        ),
        (
            "TC-R8-104", "TS-010-STR",
            "Verify whitespace-only Mailing Street input is treated as blank and displays MSG-0001 (ASM-15)",
            "Mailing Street Component", "Parent Portal > Profile", "S4 (lowest)", "Low", "Passed", "Functional",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; Edit Mode open",
            "MailingStreet = '          ' (10 blank spaces)",
            "1. Enter spaces only in Mailing Street<br>2. Click [Save changes] or blur field",
            "System detects empty content and displays required field error MSG-0001 under Mailing Street<br>Input highlights red with aria-invalid='true'<br>Save action blocked",
            "Whitespace detected as empty; MSG-0001 error displayed.",
            "ASM-15: Whitespace-only input in a required field is treated as blank.", "",
            "FR-08.3 errors; ASM-15; MSG-0001",
            "Ensures user cannot submit street with just spaces."
        ),
        (
            "TC-R8-107", "TS-010-STR",
            "Verify Mailing Street maximum length boundary of 100 characters (BVA Length)",
            "Mailing Street Component", "Parent Portal > Profile", "S4 (lowest)", "Low", "Passed", "BVA",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; Edit Mode open",
            "BVA: 100 chars ('S'*100) vs 101 chars ('S'*101)",
            "1. Enter 100-character string into Mailing Street, save and verify<br>2. Enter 101-character string into Mailing Street and attempt save",
            "100 chars: Successfully saved with MSG-0807<br>101 chars: Truncated by maxlength='100' or blocked with field length error",
            "100 chars saved; 101 chars blocked by maxlength constraint.",
            "ASM-09: No message code defined for max-length; field-level validation blocks Save.", "",
            "FS R8 field table (Street max 100) - BVA; Appendix A Parent_Profile.MailingStreet NVARCHAR(100)",
            "Prevents database column overflow in Parent_Profile table."
        ),
        (
            "TC-R8-STR-02", "TS-010-STR",
            "Verify valid Singapore street names with punctuation (hyphens, dots, apostrophes) are saved accurately",
            "Mailing Street Component", "Parent Portal > Profile", "S3", "Medium", "Passed", "Functional",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; Edit Mode open",
            "Streets: 'St. George\\'s Lane', 'Jalan Jurong Kechil', 'Ang Mo Kio Ave 3'",
            "1. Enter 'St. George\\'s Lane' into Mailing Street<br>2. Save and reload profile",
            "Street persists accurately and renders 'St. George\\'s Lane' on view screen<br>Saved with MSG-0807",
            "Street name with apostrophe and period saved and reloaded accurately.",
            "TD: Standard address string allowing legitimate punctuation", "",
            "FS R8 sec. 6 field table; Appendix A",
            "Ensures special characters in Singapore street names are preserved."
        ),
        (
            "TC-R8-STR-03", "TS-010-STR",
            "Verify forbidden symbols (< > { } ;) in Mailing Street are blocked or sanitized",
            "Mailing Street Component", "Parent Portal > Profile", "S3", "Medium", "Passed", "Functional",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; Edit Mode open",
            "Forbidden: 'Ang Mo Kio Ave 3 <script>', '{Street 52};'",
            "1. Enter 'Ang Mo Kio Ave 3 <script>' into Mailing Street<br>2. Attempt to save form",
            "HTML script injection characters blocked or sanitized<br>No raw tags committed to database",
            "Dangerous symbols blocked and sanitized.",
            "TD: Input sanitization whitelist", "",
            "NFR Security; Invariant 8",
            "Prevents address injection attacks."
        ),
        (
            "TC-R8-STR-04", "TS-010-STR",
            "Verify pasting 1000-character string or multiline text into Mailing Street is handled safely without UI breakage",
            "Mailing Street Component", "Parent Portal > Profile", "S3", "Medium", "Passed", "Stress",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; Edit Mode open",
            "Paste stress: 'S'*1000; Multiline: 'Line 1\\nLine 2'",
            "1. Paste 1000 characters into Mailing Street<br>2. Inspect input value and viewport overflow<br>3. Paste multiline address",
            "Input truncated to maxlength='100'<br>Document scrollWidth === clientWidth (zero overflow)<br>Newlines stripped/collapsed to single space",
            "Paste stress handled cleanly; 0 overflow; newlines normalized.",
            "TD: Viewport layout stress & boundary truncation", "",
            "Invariant 7; NFR Usability",
            "Ensures robust handling of large clipboard data."
        ),
        (
            "TC-R8-114", "TS-010-STR",
            "Verify malicious script input in Mailing Street is sanitized and rendered as plain text without XSS execution",
            "Mailing Street Component", "Parent Portal > Profile", "S2", "Medium", "Passed", "Security",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; Edit Mode open",
            "XSS vector: <script>alert(1)</script>",
            "1. Enter '<script>alert(1)</script>' in Mailing Street<br>2. Click [Save changes] and confirm in dialog<br>3. Reload profile page and inspect rendered text and console",
            "No alert popup is triggered<br>Zero JavaScript errors on console<br>Script tags are rendered safely as escaped plain text or sanitized in DB",
            "Script tag escaped safely as plain text, no execution detected.",
            "TD: Invariant 8 - HTML entity encoding and DOMPurify on output", "",
            "NFR Security; Invariant 8",
            "Prevents Stored Cross-Site Scripting (XSS) attacks."
        ),

        # =========================================================================
        # 7. TS-010-POS - Mailing Postal Code Component (8 TCs)
        # =========================================================================
        (
            "TC-R8-108", "TS-010-POS",
            "Verify Singapore Mailing Postal Code must be exactly 6 numeric digits (EP Valid vs Invalid)",
            "Mailing Postal Code Component", "Parent Portal > Profile", "S3", "Medium", "Passed", "Functional",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; Edit Mode open",
            "EP Valid: 650009, 238888, 560123; EP Invalid: 65000 (5 digits), 6500091 (7 digits), 65A009",
            "1. Enter '650009' and verify successful save<br>2. Enter '65000' and attempt save<br>3. Enter '6500091' and attempt save<br>4. Enter '65A009' and attempt save",
            "'650009' passes and saves with MSG-0807<br>'65000', '6500091', and '65A009' are rejected with inline validation error and red border<br>Nothing invalid saved to DB",
            "Only exact 6-digit postal code 650009 is accepted; others rejected.",
            "ASM-09: No message code is defined for postal-code errors; field-level validation blocks Save.", "",
            "FS R8 field table (Postal code 6 digits); Appendix A Parent_Profile.MailingPostalCode VARCHAR(10)",
            "Singapore postal code format verification."
        ),
        (
            "TC-R8-POS-01", "TS-010-POS",
            "Verify Singapore postal code with leading zero (e.g. '018956', '000000') is preserved as 6 digits across save and reload",
            "Mailing Postal Code Component", "Parent Portal > Profile", "S3", "Medium", "Passed", "Functional",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; Edit Mode open",
            "Input: '018956' (Downtown Singapore sector with leading zero)",
            "1. Enter '018956' in Postal Code input<br>2. Click [Save changes] and confirm<br>3. Verify displayed postal code upon reload",
            "Postal code is preserved as text '018956' with leading zero intact<br>Leading zero is NOT stripped by numeric conversion<br>Saved with MSG-0807",
            "Leading zero preserved as '018956' across save and reload.",
            "TD: Postal code stored as VARCHAR, preventing numeric casting zero-drop", "",
            "FS R8 sec. 6 field table; Appendix A Parent_Profile.MailingPostalCode",
            "Crucial for central Singapore districts (Marina Bay 01xxxx, Tanjong Pagar 07xxxx)."
        ),
        (
            "TC-R8-POS-02", "TS-010-POS",
            "Verify postal code length boundary: 5 digits and 7 digits are rejected (BVA Length)",
            "Mailing Postal Code Component", "Parent Portal > Profile", "S3", "Medium", "Passed", "BVA",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; Edit Mode open",
            "BVA: 5 digits ('56012' - underflow) vs 7 digits ('5601234' - overflow)",
            "1. Enter 5-digit postal code '56012' and attempt save<br>2. Enter 7-digit postal code '5601234' and attempt save",
            "Both 5-digit and 7-digit inputs fail validation<br>Inline error displayed below Postal Code input<br>Save action blocked",
            "Rejected: postal code must be exactly 6 digits.",
            "TD: BVA 2-point test on exact 6-digit Singapore postal format constraint", "",
            "FS R8 sec. 6 field table; Appendix A",
            "Enforces strict length boundary."
        ),
        (
            "TC-R8-POS-03", "TS-010-POS",
            "Verify postal code containing non-digits, special symbols, or hyphens (e.g. '23888a', '650-009') is rejected",
            "Mailing Postal Code Component", "Parent Portal > Profile", "S3", "Low", "Passed", "Functional",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; Edit Mode open",
            "Input: '23888a', 'ABCDEF', '650-009', '650 09', '65000.'",
            "1. Enter '23888a' into Postal Code<br>2. Attempt to save form",
            "Validation rejects non-digit characters<br>Displays inline validation error<br>Submission blocked",
            "Rejected: only numeric digits permitted.",
            "TD: Regex /^\\d{6}$/ enforced on postal code", "",
            "FS R8 sec. 6 field table; Appendix A",
            "Prevents malformed postal codes."
        ),
        (
            "TC-R8-POS-04", "TS-010-POS",
            "Verify clearing mandatory Mailing Postal Code triggers required error MSG-0001",
            "Mailing Postal Code Component", "Parent Portal > Profile", "S2", "High", "Passed", "Functional",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; Edit Mode open",
            "MailingPostalCode = '' (empty string)",
            "1. Clear Postal Code input field<br>2. Blur field or click [Save changes]",
            "Displays required field error MSG-0001: 'Enter your postal code' (or 'This field is required')<br>Input marked with aria-invalid='true'<br>Save button disabled",
            "MSG-0001 displayed under Postal Code field; submission blocked.",
            "CR: Postal Code is mandatory per FSD section 6 table", "BUG-R8-005",
            "FR-08.3 errors; R8-AC16; MSG-0001",
            "Mandatory postal code validation."
        ),
        (
            "TC-R8-POS-05", "TS-010-POS",
            "Verify whitespace-only Mailing Postal Code is treated as blank with MSG-0001 (ASM-15)",
            "Mailing Postal Code Component", "Parent Portal > Profile", "S4 (lowest)", "Low", "Passed", "Functional",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; Edit Mode open",
            "MailingPostalCode = '      ' (6 blank spaces)",
            "1. Enter spaces only in Postal Code<br>2. Click [Save changes] or blur field",
            "Whitespace is treated as empty input<br>Displays required field error MSG-0001<br>Nothing saved to DB",
            "Whitespace detected as empty; MSG-0001 error displayed.",
            "ASM-15: Whitespace-only input in a required field is treated as blank.", "",
            "FR-08.3 errors; ASM-15; MSG-0001",
            "Prevents space injection in postal code."
        ),
        (
            "TC-R8-POS-06", "TS-010-POS",
            "Verify invalid postal code displays localized error, red border, and strictly NO raw i18n key leakage",
            "Mailing Postal Code Component", "Parent Portal > Profile", "S1 (highest)", "Critical", "Failed", "UI",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; Edit Mode open",
            "Invalid postal code: '12345'",
            "1. Enter '12345' into Postal Code input<br>2. Trigger blur event<br>3. Inspect the error alert text and aria-invalid attribute<br>4. Verify text does NOT contain 'features.parentProfile.validation.postalCodeInvalid'",
            "Postal Code input highlights with red glowing border (aria-invalid='true')<br>Validation message renders human-readable text (e.g. 'Postal code must be exactly 6 digits')<br>NO raw i18n translation key ('features.parentProfile.validation.postalCodeInvalid') is leaked",
            "DEFECT: UI currently displays raw un-translated key 'features.parentProfile.validation.postalCodeInvalid' instead of localized message.",
            "Mandate: Zero Raw i18n Key Leakage across UI surface", "BUG-R8-I18N-02",
            "FS R8 sec. 6 field table; Invariant 7 UI Health",
            "Catches raw translation key defect in Postal Code component."
        ),
        (
            "TC-R8-POS-07", "TS-010-POS",
            "Verify full-width Unicode digits ('２３８８８８') and negative/decimal postal codes are rejected",
            "Mailing Postal Code Component", "Parent Portal > Profile", "S3", "Low", "Passed", "Functional",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; Edit Mode open",
            "Inputs: '２３８８８８', '238.88', '-23888'",
            "1. Enter '２３８８８８' and blur<br>2. Enter '238.88' and blur<br>3. Enter '-23888' and blur",
            "Full-width digits, decimals, and negative numbers fail 6-digit regex validation<br>Inline error displayed; save action blocked",
            "Full-width, decimal, and negative postal codes rejected cleanly.",
            "TD: Strict ASCII 6-digit validation", "",
            "FS R8 sec. 6 field table; Appendix A",
            "Guarantees data cleanliness for postal logistics integration."
        ),

        # =========================================================================
        # 8. TS-010-CTY - Mailing Country Component (6 TCs)
        # =========================================================================
        (
            "TC-R8-CTY-01", "TS-010-CTY",
            "Verify Mailing Country default value is 'Singapore' and can be modified for overseas address",
            "Mailing Country Component", "Parent Portal > Profile", "S3", "Medium", "Passed", "Functional",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; Edit Mode open",
            "Default: 'Singapore'; Modified: 'Malaysia'",
            "1. Check default value in Mailing Country input<br>2. Change country to 'Malaysia'<br>3. Click [Save changes] and confirm in dialog<br>4. Reload profile page",
            "Default value is 'Singapore'<br>Updated value 'Malaysia' saves successfully with MSG-0807<br>Reloading shows 'Malaysia' rendered on profile",
            "Default 'Singapore' verified; updated to 'Malaysia' and persisted accurately.",
            "CR: Default country is Singapore, supports overseas mailing", "",
            "FS R8 sec. 6 field table; Appendix A Parent_Profile.MailingCountry",
            "Allows parents residing or posting overseas to receive correspondence."
        ),
        (
            "TC-R8-CTY-05", "TS-010-CTY",
            "Verify text-only Mailing Country rejects numeric digits (e.g. 'Singapore1', '123')",
            "Mailing Country Component", "Parent Portal > Profile", "S3", "Low", "Passed", "Functional",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; Edit Mode open",
            "Numeric inputs: 'Singapore1', '123', 'Country 404'",
            "1. Enter 'Singapore1' in Mailing Country<br>2. Attempt to save form",
            "System rejects numeric digits in Country name<br>Displays field error or blocks save",
            "Numeric country strings rejected.",
            "TD: Text-only country name validation", "",
            "FS R8 sec. 6 field table",
            "Prevents numeric corruption in country name."
        ),
        (
            "TC-R8-CTY-06", "TS-010-CTY",
            "Verify legitimate country names with diacritics and hyphens (e.g. 'Côte d\\'Ivoire') are accepted",
            "Mailing Country Component", "Parent Portal > Profile", "S3", "Low", "Passed", "Functional",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; Edit Mode open",
            "Valid: 'Côte d\\'Ivoire', 'Timor-Leste'",
            "1. Enter 'Côte d\\'Ivoire' into Mailing Country<br>2. Save and reload profile",
            "Country persists accurately with diacritics and apostrophe intact<br>Saved with MSG-0807",
            "Country with diacritics and apostrophe saved accurately.",
            "TD: Unicode text support in Country NVARCHAR(100)", "",
            "FS R8 sec. 6 field table; Appendix A",
            "Supports legitimate sovereign country names."
        ),
        (
            "TC-R8-CTY-02", "TS-010-CTY",
            "Verify Mailing Country maximum length boundary of 100 characters (BVA Length)",
            "Mailing Country Component", "Parent Portal > Profile", "S4 (lowest)", "Low", "Passed", "BVA",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; Edit Mode open",
            "BVA: 100 chars ('C'*100) vs 101 chars ('C'*101)",
            "1. Enter 100-character country name, save and verify<br>2. Enter 101-character string and attempt save",
            "100 chars: Successfully saved with MSG-0807<br>101 chars: Truncated by maxlength='100' or blocked with field length error",
            "100 chars saved; 101 chars blocked by maxlength constraint.",
            "ASM-09: No message code defined for max-length; field-level validation blocks Save.", "",
            "FS R8 field table (Country max 100) - BVA; Appendix A Parent_Profile.MailingCountry NVARCHAR(100)",
            "Prevents database column overflow in Parent_Profile table."
        ),
        (
            "TC-R8-CTY-03", "TS-010-CTY",
            "Verify clearing mandatory Mailing Country triggers required validation error MSG-0001",
            "Mailing Country Component", "Parent Portal > Profile", "S2", "High", "Passed", "Functional",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; Edit Mode open",
            "MailingCountry = '' (empty string)",
            "1. Clear Mailing Country input field<br>2. Blur field or click [Save changes]",
            "Displays required error MSG-0001: 'Enter your country' (or 'This field is required')<br>Input marked with aria-invalid='true'<br>Save button disabled",
            "MSG-0001 displayed under Mailing Country; submission blocked.",
            "CR: Mailing Country is mandatory per FSD section 6 table", "BUG-R8-005",
            "FR-08.3 errors; R8-AC16; MSG-0001",
            "Mandatory country field validation."
        ),
        (
            "TC-R8-CTY-04", "TS-010-CTY",
            "Verify whitespace-only Mailing Country is treated as blank with MSG-0001 (ASM-15)",
            "Mailing Country Component", "Parent Portal > Profile", "S4 (lowest)", "Low", "Passed", "Functional",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; Edit Mode open",
            "MailingCountry = '     ' (spaces)",
            "1. Enter spaces only in Mailing Country<br>2. Click [Save changes] or blur field",
            "Whitespace is treated as empty input<br>Displays required field error MSG-0001<br>Nothing saved to DB",
            "Whitespace detected as empty; MSG-0001 error displayed.",
            "ASM-15: Whitespace-only input in a required field is treated as blank.", "",
            "FR-08.3 errors; ASM-15; MSG-0001",
            "Prevents space injection in country field."
        ),

        # =========================================================================
        # 9. TS-010-STA - Form State & Mode Transitions (4 TCs)
        # =========================================================================
        (
            "TC-R8-ATM-02", "TS-010-STA",
            "Verify Save changes button pristine and dirty state gatekeeper (disabled when pristine, enabled when dirty)",
            "Form State & Mode Transitions", "Parent Portal > Profile", "S2", "High", "Passed", "UI",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; enter Edit Mode via [Update details]",
            "Pristine form vs 1 char edit ('91234567' -> '91234568')",
            "1. Open Edit Mode<br>2. Inspect Save changes button state and hint text<br>3. Type 1 character into phone number<br>4. Inspect Save changes button state and hint text<br>5. Revert character back to original baseline",
            "Pristine state: Save changes button is disabled (disabled=true); hint 'Make a change to enable saving.' is visible<br>Dirty state: Save changes button enables (disabled=false); hint is hidden<br>Reverting to original baseline: Save changes button re-disables; hint reappears",
            "Button disabled with hint when pristine; enables upon change; re-disables when reverted.",
            "CR: UI interaction design confirmed to prevent redundant mutation dispatches", "",
            "FR-08.3; AC #14; US-08.2",
            "Prevents redundant PUT mutation dispatches when no changes exist."
        ),
        (
            "TC-R8-STA-01", "TS-010-STA",
            "Verify clicking 'Update details' button transitions page from View Mode to Edit Mode",
            "Form State & Mode Transitions", "Parent Portal > Profile", "S2", "High", "Passed", "UI",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; on /profile page (View Mode)",
            "N/A",
            "1. Open /profile page in View Mode<br>2. Click 'Update details' button<br>3. Verify presence of editable form inputs and action buttons",
            "Page switches smoothly to Edit Mode<br>Editable inputs appear: phoneNumber, email, mailingBlock, mailingStreet, mailingUnit, mailingPostalCode, mailingCountry<br>Action buttons [Save changes] and [Cancel] appear<br>[Update details] button is replaced",
            "Page transitions to Edit Mode; inputs and action buttons revealed.",
            "TD: React component state transition (isEditing: false -> true)", "",
            "FR-08.3; FS R8 sec. 6; AC #14",
            "Core mode transition entry point."
        ),
        (
            "TC-R8-STA-02", "TS-010-STA",
            "Verify clicking 'Cancel' button discards uncommitted modifications and restores baseline in View Mode",
            "Form State & Mode Transitions", "Parent Portal > Profile", "S2", "High", "Passed", "Functional",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; Edit Mode open",
            "Original phone: '91234567'; Modified phone: '98887777'",
            "1. Change Mobile Number to '98887777'<br>2. Change Email to 'uncommitted@example.sg'<br>3. Click [Cancel] button<br>4. Inspect View Mode profile values",
            "Edit Mode exits immediately without confirmation modal<br>Page returns to View Mode<br>Profile displays original phone ('91234567') and email<br>Uncommitted modifications are completely discarded",
            "Cancel button restores original baseline; zero uncommitted data saved.",
            "TD: Local state reset without backend mutation", "",
            "FR-08.3; AC #14; US-08.2",
            "Ensures clean escape from dirty form."
        ),
        (
            "TC-R8-STA-03", "TS-010-STA",
            "Verify each blank required field individually prevents submission with inline error MSG-0001",
            "Form State & Mode Transitions", "Parent Portal > Profile", "S2", "High", "Passed", "Functional",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; Edit Mode open",
            "5 mandatory fields: phoneNumber, email, mailingStreet, mailingPostalCode, mailingCountry",
            "1. Clear phoneNumber, attempt save -> verify MSG-0001<br>2. Restore phoneNumber, clear email, attempt save -> verify MSG-0001<br>3. Restore email, clear mailingStreet, attempt save -> verify MSG-0001<br>4. Restore street, clear mailingPostalCode, attempt save -> verify MSG-0001<br>5. Restore postal, clear mailingCountry, attempt save -> verify MSG-0001",
            "Each blank mandatory field individually triggers MSG-0001 inline error<br>Save action is blocked on every iteration<br>Nothing is saved to DB",
            "Each individual mandatory field triggers MSG-0001 when left blank.",
            "CR: FSD section 6 table and AC #16 require MSG-0001 per required field", "",
            "FR-08.3 errors; R8-AC16; MSG-0001",
            "Granular mandatory validation across all 5 required fields."
        ),

        # =========================================================================
        # 10. TS-010-SUB - Submission & Confirm Dialog (5 TCs)
        # =========================================================================
        (
            "TC-R8-097", "TS-010-SUB",
            "Verify saving valid phone, email and mailing address shows MSG-0807, persists data, creates audit log, and sends zero email",
            "Submission & Confirm Dialog", "Parent Portal > Profile", "S1 (highest)", "Critical", "Passed", "Functional",
            "SIT<br>Chrome (latest) + DB read access<br>Mock SingPass + mock data API",
            "FA logged in; Edit Mode open",
            "Phone: '98887777'; Email: 'fa.new@example.sg'; Mailing: Blk 9 Verde Walk #02-01 S650009 Singapore",
            "1. Enter valid new values for all contact and mailing fields<br>2. Click [Save changes]<br>3. In Confirm Dialog, click [Save changes]<br>4. Verify success toast and reload page<br>5. Inspect DB Parent_Profile table, audit log, and email outbox",
            "Success toast MSG-0807 'Your details have been updated.' is displayed in green<br>Values persist accurately after page reload<br>Audit log records 1 entry per changed field (field, old, new, user, timestamp)<br>ZERO notification email is sent (Decision D-28)",
            "Success toast MSG-0807 displayed; DB updated; audit log created; no email dispatched.",
            "CR: Decision D-28 explicitly prohibits sending email for profile updates", "",
            "FR-08.3; R8-AC14; US-08.2; D-28; PB-15",
            "Golden path end-to-end profile update."
        ),
        (
            "TC-R8-SUB-01", "TS-010-SUB",
            "Verify clicking 'Save changes' in dirty state triggers confirmation modal (role='alertdialog')",
            "Submission & Confirm Dialog", "Parent Portal > Profile", "S2", "High", "Passed", "UI",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; Edit Mode open with valid modifications",
            "Phone: '98887777'",
            "1. Modify phone number<br>2. Click [Save changes] button<br>3. Verify appearance and accessibility of modal dialog",
            "Modal appears with role='alertdialog'<br>Displays title 'Confirm Changes' and confirmation message<br>Contains action buttons: [Keep editing] and [Save changes]<br>Background backdrop blocks background interaction",
            "Modal alertdialog displayed with expected buttons and backdrop.",
            "TD: WCAG 2.1 alertdialog pattern", "",
            "FR-08.3; AC #14; US-08.2",
            "Prevents accidental profile overwrites."
        ),
        (
            "TC-R8-INT-01", "TS-010-SUB",
            "Verify Confirm Dialog 'Keep editing' button retains uncommitted dirty form data without API dispatch",
            "Submission & Confirm Dialog", "Parent Portal > Profile", "S2", "Medium", "Passed", "Integration",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "FA logged in; Edit Mode open",
            "New phone: '98887777'",
            "1. Enter valid new phone '98887777'<br>2. Click [Save changes] -> opens Confirmation Dialog (role='alertdialog')<br>3. Click [Keep editing] button on dialog",
            "Confirmation Dialog closes immediately<br>Form remains in Edit Mode with '98887777' preserved in Mobile Number input<br>Zero HTTP PUT/PATCH mutation requests dispatched to backend<br>No toast displayed",
            "Keep editing button closes dialog and retains dirty form inputs without API dispatch.",
            "TD: Dialog role='alertdialog' integration pattern", "",
            "FR-08.3; AC #14; US-08.2",
            "Multi-component interaction test between Form and Alertdialog."
        ),
        (
            "TC-R8-SUB-02", "TS-010-SUB",
            "Verify Confirm Dialog rapid double-click debounce dispatches only one single mutation request",
            "Submission & Confirm Dialog", "Parent Portal > Profile", "S2", "Medium", "Passed", "Concurrency",
            "SIT<br>Chrome (latest) + Network interceptor<br>Mock SingPass + mock data API",
            "FA logged in; Confirmation Dialog open",
            "Double-click within 50ms interval",
            "1. Open Confirmation Dialog with modified form data<br>2. Intercept outgoing PUT/PATCH /api/parent/profile requests<br>3. Rapidly double-click [Save changes] button on dialog<br>4. Count dispatched requests",
            "Button immediately enters loading state and disables further clicks (isSubmitting=true)<br>Exactly ONE mutation request is dispatched to server<br>No duplicate audit records or race conditions generated",
            "Debounce verified: exactly 1 HTTP mutation request sent.",
            "TD: Invariant 8 - UI debounce and API idempotency", "",
            "FR-08.3; NFR Concurrency; Invariant 8",
            "Prevents race conditions on slow network connections."
        ),
        (
            "TC-R8-109", "TS-010-SUB",
            "Verify backend system error (HTTP 500) displays MSG-0808 and preserves dirty form data without loss",
            "Submission & Confirm Dialog", "Parent Portal > Profile", "S2", "High", "Passed", "Functional",
            "SIT<br>Chrome (latest) + Route mock / fault injection<br>Mock SingPass + mock data API",
            "FA logged in; mock profile update API forced to return HTTP 500 Internal Server Error",
            "Phone: '98887777'",
            "1. Enter new phone '98887777'<br>2. Click [Save changes] and confirm in dialog<br>3. Intercept API and return HTTP 500<br>4. Inspect UI response and form state",
            "Displays error toast/banner MSG-0808: 'We could not update your details. Please try again.'<br>Page does NOT crash (No White Screen of Death)<br>Form remains in Edit Mode with '98887777' preserved so user does not lose typed data<br>Database retains original phone '91234567'",
            "MSG-0808 displayed; form inputs preserved; DB retains original values.",
            "CR: FSD section 6 table and AC #17 error handling", "",
            "FR-08.3 errors; R8-AC17; MSG-0808",
            "Fault injection resilience test."
        ),

        # =========================================================================
        # 11. TS-010-AGE - Child Age Access & Isolation (4 TCs)
        # =========================================================================
        (
            "TC-R8-110", "TS-010-AGE",
            "Verify My details is strictly view-only when all linked children are 16+ years old",
            "Child Age Access & Isolation", "Parent Portal > Profile", "S2", "High", "Passed", "Functional",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "Parent PE logged in (all linked children E1 age 16, E2 age 17)",
            "Parent PE (S7000007G); Children >= 16",
            "1. Log in as Parent PE<br>2. Navigate to /profile<br>3. Inspect profile screen for edit controls<br>4. Attempt to call PUT /api/parent/profile directly via API",
            "All fields rendered as read-only<br>No [Update details] button exists on UI<br>Direct API update attempt is rejected with HTTP 403 Forbidden<br>Banner displays: 'Profile editing is unavailable when all children have reached 16.'",
            "Profile is strictly view-only; edit button hidden; API rejects update.",
            "CR: Business rule BR-08-06.4 and R8-AC09 - view-only when all children 16+", "",
            "FR-08.3 precondition; R8-AC09; BR-08-06.4",
            "Child adulthood transition lifecycle rule."
        ),
        (
            "TC-R8-111", "TS-010-AGE",
            "Verify My details is editable when at least one child is under 16 years old",
            "Child Age Access & Isolation", "Parent Portal > Profile", "S3", "Medium", "Passed", "Functional",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "Parent PB logged in (Child B1 age 16, Child B2 age 14)",
            "Parent PB (S7000002B); Child B2 under 16",
            "1. Log in as Parent PB<br>2. Navigate to /profile<br>3. Inspect profile screen",
            "[Update details] button is visible and active<br>Clicking enters Edit Mode with editable contact and mailing fields<br>Save action is permitted",
            "[Update details] button is available and functional.",
            "CR: FSD section 6 precondition: parent with at least one child < 16 can edit", "",
            "FR-08.3 precondition; R8-AC09",
            "Per-family mixed age rule."
        ),
        (
            "TC-R8-112", "TS-010-AGE",
            "Verify a parent cannot update another parent's profile via API IDOR tampering (BOLA/IDOR Protection)",
            "Child Age Access & Isolation", "API Service", "S1 (highest)", "Critical", "Not Run", "Security",
            "SIT<br>API client (Postman/Playwright API)<br>Mock SingPass + mock data API",
            "Father FA logged in; Mother MA's Parent_Profile ID known",
            "Target ID: MA's Profile ID; Token: FA's auth bearer token",
            "1. Send PUT /api/parent/profile/{MA_ID} using FA's session token<br>2. Check HTTP status code and response payload<br>3. Inspect MA's profile in DB",
            "API rejects request with HTTP 403 Forbidden and MSG-0003: 'You do not have permission to perform this action.'<br>Mother MA's profile remains completely unchanged",
            "Server-side tenancy & ownership verification on user claims.",
            "TD: Server-side tenancy & ownership verification on user claims", "",
            "FR-08.3 rules (own data only); NFR Security; MSG-0003",
            "OWASP Top 10 API1: Broken Object Level Authorization (BOLA/IDOR)."
        ),
        (
            "TC-R8-113", "TS-010-AGE",
            "Verify father's profile update does not alter mother's personal details (Independent Records)",
            "Child Age Access & Isolation", "Parent Portal > Profile", "S2", "Medium", "Passed", "Functional",
            "SIT<br>Chrome (latest), Windows 11<br>Mock SingPass + mock data API",
            "Father FA and Mother MA both registered in system for same children",
            "FA new phone: '98887777'; MA original phone: '81112222'",
            "1. Log in as Father FA and update phone number to '98887777'<br>2. Confirm update and log out<br>3. Log in as Mother MA and navigate to /profile",
            "Mother MA's phone number remains '81112222' (unchanged)<br>Each parent maintains an independent Parent_Profile entity in DB",
            "Father update is isolated; mother profile remains unchanged.",
            "CR: FSD Appendix A shows separate Parent_Profile row per NRIC", "",
            "FR-08.3 rules; Appendix A Parent_Profile",
            "Ensures parent profiles are strictly de-coupled."
        ),

        # =========================================================================
        # 12. TS-010-NFR - Security & UI Health (3 TCs)
        # =========================================================================
        (
            "TC-R8-NFR-01", "TS-010-NFR",
            "Verify Non-Functional UI Health, Zero Console Uncaught JS Exceptions & WCAG AA Contrast >= 4.5:1",
            "Security & UI Health", "Parent Portal > Profile", "S2", "High", "Passed", "Non-Functional",
            "SIT<br>Chrome (latest) + DevTools Protocol<br>Mock SingPass + mock data API",
            "FA logged in; /profile page loaded",
            "Desktop (1280x720) viewport",
            "1. Attach page.on('pageerror') and page.on('console') listeners<br>2. Perform multiple View <-> Edit mode toggles<br>3. Trigger validation alerts and modal dialog<br>4. Run WCAG 2.1 color contrast check on text and alert banners",
            "0 Uncaught JavaScript Exceptions in browser console<br>0 Failed network chunk assets (HTTP 404)<br>WCAG 2.1 AA text color contrast ratio >= 4.5:1 across all labels and alerts",
            "0 console exceptions; 0 failed assets; WCAG 2.1 AA compliant.",
            "TD: Invariant 7 - 9-Tier Failure Evaluation Framework", "",
            "NFR Usability; WCAG 2.1 AA; Invariant 7",
            "Guarantees technical baseline stability and accessibility."
        ),
        (
            "TC-R8-NFR-02", "TS-010-NFR",
            "Verify responsive layout integrity with zero horizontal scrollbar (scrollWidth === clientWidth) on desktop and mobile viewports",
            "Security & UI Health", "Parent Portal > Profile", "S2", "High", "Passed", "Non-Functional",
            "SIT<br>Chrome (latest) + Viewport emulation<br>Mock SingPass + mock data API",
            "FA logged in; on /profile page",
            "Desktop: 1280x720; Mobile: 375x667 (iPhone SE)",
            "1. Load /profile on Desktop viewport (1280x720) and measure document.documentElement.scrollWidth vs clientWidth<br>2. Resize viewport to Mobile (375x667)<br>3. Measure scrollWidth vs clientWidth in both View and Edit modes",
            "In all viewports and modes: document.documentElement.scrollWidth === clientWidth<br>No accidental horizontal scrollbar appears<br>Form inputs stack cleanly on mobile with full tap targets",
            "Verified: 0 horizontal overflow across desktop and mobile viewports.",
            "TD: Invariant 7 Visual & Layout Integrity tier", "",
            "FS R8 sec. 7; Invariant 7",
            "Responsive layout verification."
        ),
        (
            "TC-R8-NFR-03", "TS-010-NFR",
            "Verify PII protection: NRIC is masked by default and never leaked in plain text in URL query params or data attributes",
            "Security & UI Health", "Parent Portal > Profile", "S1 (highest)", "Critical", "Passed", "Security",
            "SIT<br>Chrome (latest) + DOM Inspector<br>Mock SingPass + mock data API",
            "FA logged in; on /profile page",
            "NRIC: S1234123F",
            "1. Check current URL: ensure full NRIC does not appear in query parameters or hash<br>2. Inspect DOM tree before clicking 'Show NRIC'<br>3. Verify unmasked NRIC does not exist in data-* attributes or hidden inputs",
            "URL does not contain NRIC string<br>Unmasked NRIC is NOT present in plain text in DOM attributes before user interaction<br>Compliance with Singapore PDPA & GovTech security standards",
            "NRIC not leaked in URL or DOM attributes; compliant with PDPA.",
            "CR: FSD section 7: Không đưa NRIC đầy đủ vào URL", "",
            "FS R8 sec. 7 Yêu cầu phi chức năng (Bảo mật); NFR Security; Invariant 8",
            "Prevents PII leakage in analytics logs and referrers."
        ),
    ]

    table_lines = []
    for r in rows:
        row_str = "| " + " | ".join(r) + " |"
        table_lines.append(row_str)

    footer = """

---

## 3. BẢNG LOCATOR BSK ĐÃ XÁC MINH TRÊN LIVE DOM (BSK RECON LOCATORS)

AI Coding Agent BẮT BUỘC sử dụng các locator đã trinh sát thực tế này từ `tools/recon_bsk.py` và [`ParentProfilePage`](file:///home/baudui/automation-ui/pages/fs08/parent_profile_page.py):

| Tên Phần Tử | Selector Playwright Chuẩn | Loại Element | Ràng Buộc / Ghi Chú Kỹ Thuật |
| :--- | :--- | :--- | :--- |
| **Tiêu đề trang** | `h1:has-text('My Profile'), h2:has-text('My Profile')` | `<h1> / <h2>` | Hiển thị tiêu đề trang profile |
| **Full Name** | `dt:has-text('Full Name') + dd, [data-testid='full-name']` | `<dd> / <span>` | Read-only tĩnh, lấy từ SingPass MyInfo |
| **Residential Address** | `dt:has-text('Residential') + dd, [data-testid='residential-address']` | `<dd> / <span>` | Read-only tĩnh theo Quyết định `D-20` (Không có thẻ input) |
| **NRIC Display** | `dt:has-text('NRIC') + dd, [data-testid='nric']` | `<dd> / <span>` | Mặc định che mặt nạ dạng `*****123F` |
| **Show NRIC Button** | `button:has-text("Show NRIC")` | `<button>` | Bấm để hiện đầy đủ số NRIC |
| **Hide NRIC Button** | `button:has-text("Hide NRIC")` | `<button>` | Bấm để che lại số NRIC |
| **Update Details Button** | `button:has-text("Update details")` | `<button>` | Chuyển View Mode -> Edit Mode |
| **Mobile Number Input** | `input[name="phoneNumber"]` | `<input type="tel">` | Bắt buộc, 8 chữ số đầu 6, 8, 9, inputmode numeric |
| **Email Address Input** | `input[name="email"]` | `<input type="email">` | Bắt buộc, RFC 5322, <= 150 ký tự |
| **Mailing Block Input** | `input[name="mailingBlock"]` | `<input type="text">` | Tùy chọn, tối đa 20 ký tự |
| **Mailing Street Input** | `input[name="mailingStreet"]` | `<input type="text">` | Bắt buộc, tối đa 100 ký tự |
| **Mailing Unit Input** | `input[name="mailingUnit"]` | `<input type="text">` | Tùy chọn, tối đa 20 ký tự |
| **Mailing Postal Code** | `input[name="mailingPostalCode"]` | `<input type="text">` | Bắt buộc, đúng 6 chữ số Singapore |
| **Mailing Country Input**| `input[name="mailingCountry"]` | `<input type="text">` | Bắt buộc, tối đa 100 ký tự |
| **Pristine State Hint** | `p:has-text("Make a change to enable saving.")` | `<p>` | Hiển thị khi form chưa có thay đổi |
| **Save Changes Button** | `button[type="submit"]:has-text("Save changes")` | `<button>` | `disabled=true` khi chưa sửa (Pristine) |
| **Cancel Button** | `button:has-text("Cancel")` | `<button>` | Hủy thay đổi, hoàn nguyên View Mode |
| **Confirm Dialog** | `div[role="alertdialog"]` | `<div>` | Modal xác nhận trước khi gọi mutation API |
| **Dialog Keep Editing** | `div[role="alertdialog"] button:has-text("Keep editing")` | `<button>` | Đóng modal, giữ nguyên form dirty |
| **Dialog Confirm Save** | `div[role="alertdialog"] button:has-text("Save changes")` | `<button>` | Gửi mutation lưu dữ liệu vào DB |
| **Inline Error Alert** | `p[role="alert"], p[class*="error"], p[id$="-error"]` | `<p>` | Hiển thị mã lỗi validation (`MSG-0805`, `MSG-0806`, `MSG-0001`) |
| **Field Invalid Indicator**| `input[aria-invalid="true"]` | `<input>` | Viền đỏ cảnh báo khi trường nhập bị lỗi |
| **Success Toast** | `p[role="status"]:has-text('Your details have been updated.')` | `<p>` | Hiển thị thông báo `MSG-0807` màu xanh |

---

## 4. FIXTURE DỮ LIỆU KIỂM THỬ (TEST DATA FIXTURES)

```json
{
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
    "email_max_150": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa@example.com",
    "email_overflow_151": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa@example.com",
    "email_invalid": ["nameexample.com", "name@", "@example.com", "name@example", "name @example.com", "abc@@gmail.com", "abc@gmail..com", "abc@gmail,com", "abc@gmail.c"],
    "block_20": "BBBBBBBBBBBBBBBBBBBB",
    "block_21": "BBBBBBBBBBBBBBBBBBBBB",
    "unit_20": "UUUUUUUUUUUUUUUUUUUU",
    "unit_21": "UUUUUUUUUUUUUUUUUUUUU",
    "street_100": "SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
    "street_101": "SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
    "postal_valid_6": ["650009", "560123", "018956", "000000"],
    "postal_invalid": ["65000", "6500091", "65A009", "650-009", "23888a"],
    "country_100": "CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC",
    "country_101": "CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC",
    "xss_vector": "<script>alert(1)</script>"
  }
}
```

---

## 5. MAPPING TRACEABILITY FSD, AC & ERROR CATALOG

| Yêu Cầu / Ràng Buộc | FSD Section / Mã AC | Mã Lỗi Hệ Thống | Kịch Bản Kiểm Thử Bao Phủ |
| :--- | :--- | :--- | :--- |
| **SingPass Read-Only** | FR-08.3; D-20; AC #18 | - | `TC-R8-094`, `TC-R8-095`, `TC-R8-096` |
| **NRIC Masking** | FR-08.3; BR-08-09.1; AC #10 | - | `TC-R8-ATM-01`, `TC-R8-NFR-03` |
| **Số điện thoại hợp lệ (6/8/9)** | FS R8 Bảng mục 6 (Mobile); AC #14 | - | `TC-R8-098`, `TC-R8-100` |
| **Số điện thoại sai định dạng** | FR-08.3 errors; AC #15 | `MSG-0805` | `TC-R8-099`, `TC-R8-TEL-01`, `TC-R8-TEL-02`, `TC-R8-TEL-05`, `TC-R8-TEL-06` |
| **Chống lộ translation key Phone** | FR-08.3; Invariant 7 UI Health | `BUG-R8-I18N-01` | `TC-R8-TEL-07` |
| **Email sai định dạng** | FR-08.3 errors; AC #15 | `MSG-0806` | `TC-R8-101`, `TC-R8-EML-02` |
| **Chống lộ translation key Email** | FR-08.3; Invariant 7 UI Health | - | `TC-R8-EML-06` |
| **Email độ dài 150 ký tự** | FS R8 Bảng mục 6; Appendix A | - | `TC-R8-102`, `TC-R8-EML-01` |
| **Stress paste 1000 ký tự** | Invariant 7; NFR Usability | - | `TC-R8-EML-05`, `TC-R8-STR-04`, `TC-R8-BLK-02` |
| **Trường bắt buộc để trống** | FR-08.3 errors; AC #16 | `MSG-0001` | `TC-R8-TEL-03`, `TC-R8-EML-03`, `TC-R8-STR-01`, `TC-R8-POS-04`, `TC-R8-CTY-03`, `TC-R8-STA-03` |
| **Nhập toàn khoảng trắng** | FR-08.3; ASM-15 | `MSG-0001` | `TC-R8-104`, `TC-R8-TEL-04`, `TC-R8-EML-04`, `TC-R8-POS-05`, `TC-R8-CTY-04` |
| **Block & Unit tùy chọn** | FS R8 Bảng mục 6 | - | `TC-R8-105`, `TC-R8-UNT-01`, `TC-R8-BLK-01`, `TC-R8-UNT-03` |
| **Giới hạn 20 ký tự Block/Unit**| FS R8 Bảng mục 6; Appendix A | - | `TC-R8-106`, `TC-R8-UNT-02` |
| **Giới hạn 100 ký tự Street/Country**| FS R8 Bảng mục 6; Appendix A | - | `TC-R8-107`, `TC-R8-CTY-02`, `TC-R8-STR-02` |
| **Mã bưu chính đúng 6 chữ số** | FS R8 Bảng mục 6; Appendix A | - | `TC-R8-108`, `TC-R8-POS-01`, `TC-R8-POS-02`, `TC-R8-POS-03`, `TC-R8-POS-07` |
| **Chống lộ translation key Postal** | FS R8 Bảng mục 6; Invariant 7 | `BUG-R8-I18N-02` | `TC-R8-POS-06` |
| **Bảo toàn số 0 ở đầu Postal Code**| FS R8 Bảng mục 6; Appendix A | - | `TC-R8-POS-01` |
| **Lưu thành công & không gửi email** | FR-08.3; AC #14; US-08.2; D-28 | `MSG-0807` | `TC-R8-097`, `TC-R8-SUB-01` |
| **Hộp thoại xác nhận Keep editing** | FR-08.3; AC #14; US-08.2 | - | `TC-R8-INT-01`, `TC-R8-SUB-02` |
| **Lỗi hệ thống 500 khi lưu** | FR-08.3 errors; AC #17 | `MSG-0808` | `TC-R8-109` |
| **Tất cả các con >= 16 tuổi** | FR-08.3 precondition; AC #09; BR-08-06.4 | - | `TC-R8-110` |
| **Có con < 16 tuổi** | FR-08.3 precondition | - | `TC-R8-111` |
| **Bảo mật BOLA/IDOR** | FR-08.3 rules; NFR Security | `MSG-0003` | `TC-R8-112` |
| **Độc lập hồ sơ Cha - Mẹ** | FR-08.3 rules; Appendix A | - | `TC-R8-113` |
| **Chống XSS địa chỉ nhận thư** | NFR Security; Invariant 8 | - | `TC-R8-114` |
| **Invariant 7 (0 Console, Layout, A11y)**| Invariant 7; WCAG 2.1 AA | - | `TC-R8-NFR-01`, `TC-R8-NFR-02` |
"""

    full_md = header + "\n".join(table_lines) + footer
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_md)
    print(f"Successfully generated expanded test case spec: {output_path} ({len(rows)} test cases)")

if __name__ == "__main__":
    generate_markdown()
