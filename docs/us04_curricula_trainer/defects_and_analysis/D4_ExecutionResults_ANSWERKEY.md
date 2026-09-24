# ANSWER KEY (Deliverable 4 execution results) — DO NOT hand to coding AI upfront

| TC ID | Suite | Test Case Name | Priority | Test Technique | Execution Status | Actual Result / Empirical Evidence | Bug ID / Linked CQ |
|---|---|---|---|---|---|---|---|
| TC_PI_001 | TS-01 | Preferred Name - Valid string entry | P1 | EP Valid | [PASSED] | Entered "Bob Wang" successfully; accepted without error. | - |
| TC_PI_002 | TS-01 | Preferred Name - Boundary Max 100 chars | P2 | BVA Max | [PASSED] | Exactly 100 characters accepted and stored completely. | - |
| TC_PI_003 | TS-01 | Preferred Name - Exceeds 100 chars (Max+1) | P2 | BVA Max+1 | [FAILED] | HTML attribute has maxlength="255", allowing 101 characters (FSD Table 4.1 specifies max 100 chars). | BUG-007 |
| TC_PI_004 | TS-01 | Preferred Name - Auto-trim whitespace | P3 | Error Guessing | [PASSED] | Entered "  Bob Wang  ", script trimmed whitespace storing "Bob Wang". | - |
| TC_PI_005 | TS-01 | Gender - Select Male / Female | P1 | EP Valid | [PASSED] | Radio button switches between Male and Female smoothly. | - |
| TC_PI_006 | TS-01 | ID Type - 4 Document types per FSD 4.1 | P1 | EP Valid | [BLOCKED] | Dropdown displays 5 options including "S-Pass". FSD Table 4.1 and narrative text are inconsistent; pending BA clarification. | BUG-009 (Pending CQ) |
| TC_PI_007 | TS-01 | ID Number - Valid NRIC format | P1 | EP Valid | [PASSED] | Entered G7666564N, accepted and stored accurately. | - |
| TC_PI_008 | TS-01 | ID Number - ID Checksum validation | P1 | EP Invalid | [FAILED] | Mock App accepted ID Number without executing any Checksum validation algorithm. Script inspection confirms missing checksum logic. | BUG-010 |
| TC_PI_009 | TS-01 | ID Number - Exceeds 20 chars (Max+1) | P2 | BVA Max+1 | [FAILED] | HTML attribute has maxlength="255", allowing 21 characters (FSD Table 4.1 limit is 20 chars). | BUG-007 |
| TC_PI_010 | TS-01 | Date of Birth - Valid past date | P1 | EP Valid | [PASSED] | Selected 1990-05-15, accepted successfully. | - |
| TC_PI_011 | TS-01 | Date of Birth - Future date rejection | P1 | EP Invalid | [PASSED] | Selected future date 2030-01-01, save blocked with valid error message. | - |
| TC_PI_012 | TS-01 | File Upload - PDF/PNG/JPG/JPEG <= 10MB | P1 | EP Valid | [PASSED] | Uploaded 5MB PDF file successfully; attachment filename displayed. | - |
| TC_PI_013 | TS-01 | File Upload - Exceeds 10MB limit | P1 | BVA Max+1 | [PASSED] | Uploaded 11MB PDF file, rejected with size limit error message. | - |
| TC_PI_014 | TS-01 | File Upload - Invalid file format (.docx) | P1 | EP Invalid | [FAILED] | .docx file rejected, but Mock App displayed "Please upload a valid document." instead of FSD standard "Unsupported file format." | BUG-008 |
| TC_PI_015 | TS-01 | Nationality - Select from Dropdown | P1 | EP Valid | [PASSED] | Selected Singaporean from dropdown successfully. | - |
| TC_PI_016 | TS-01 | Country of Birth - Select from Dropdown | P1 | EP Valid | [PASSED] | Selected Singapore from dropdown successfully. | - |
| TC_PI_017 | TS-01 | Preferred Name - Empty mandatory check | P1 | EP Negative | [PASSED] | Empty Preferred Name displayed standard error: "This field is required." | - |
| TC_PI_018 | TS-01 | ID Number - Empty mandatory check | P1 | EP Negative | [PASSED] | Empty ID Number displayed standard error: "This field is required." | - |
| TC_PI_019 | TS-01 | Date of Birth - Empty mandatory check | P1 | EP Negative | [FAILED] | Empty DOB displayed non-standard message "Enter a valid date of birth." instead of mandatory error "This field is required." (FSD 5.2). | BUG-008 |
| TC_PI_020 | TS-01 | Nationality - Unselected mandatory check | P1 | EP Negative | [PASSED] | Unselected Nationality displayed standard error: "This field is required." | - |
| TC_PI_021 | TS-01 | Country of Birth - Unselected mandatory check | P1 | EP Negative | [PASSED] | Unselected Country of Birth displayed standard error: "This field is required." | - |
| TC_PI_022 | TS-01 | Gender, Race & Tax Resident - Unselected check | P1 | EP Negative | [PASSED] | Leaving all 3 unselected triggered "This field is required." for each field. | - |
| TC_PI_023 | TS-01 | Race Dropdown - Ethnic groups options (CQ-07) | P2 | EP Valid | [PASSED] | Dropdown displays 4 standard options: Chinese, Malay, Indian, Others. | - |
| TC_CI_001 | TS-02 | Primary Email - Valid email format | P1 | EP Valid | [PASSED] | Entered trainer.bob@curricula.edu.sg successfully without error. | - |
| TC_CI_002 | TS-02 | Primary Email - Invalid format rejection | P1 | EP Invalid | [PASSED] | Entered plainaddress, displayed error "Enter a valid email address." | - |
| TC_CI_003 | TS-02 | Primary Email - Boundary Max 100 chars | P2 | BVA Max | [PASSED] | 100-character valid email accepted successfully. | - |
| TC_CI_004 | TS-02 | Primary Phone - Valid Singapore 8 digits (+65) | P1 | BVA Valid | [PASSED] | Selected +65 and entered 91234567 (8 digits) successfully. | - |
| TC_CI_005 | TS-02 | Primary Phone - 7 digits rejection (Min-1) | P2 | BVA Min-1 | [PASSED] | Entered 7 digits, displayed error "Enter a valid contact number." | - |
| TC_CI_006 | TS-02 | Primary Phone - 9 digits with code +65 | P2 | BVA / Observed | [FAILED] | Mock App rejected 9-digit phone number when +65 was selected, although FSD Table 4.2 allows 8–15 digits. Logged under CQ-09. | CQ-09 Finding |
| TC_CI_007 | TS-02 | Phone Numbers - Reject alphabetic characters | P2 | EP Invalid | [PASSED] | Non-digit input prevented in Contact Number input field. | - |
| TC_CI_008 | TS-02 | Primary Email - Empty mandatory check | P1 | EP Negative | [PASSED] | Empty Primary Email displayed standard error: "This field is required." | - |
| TC_CI_009 | TS-02 | Primary Phone - Empty mandatory check | P1 | EP Negative | [FAILED] | Empty Primary Phone displayed non-standard message "Enter a valid contact number." instead of "This field is required." (FSD 5.2). | BUG-008 |
| TC_EC_001 | TS-03 | Emergency Contact - Valid complete data | P1 | EP Valid | [PASSED] | Entered Name: "David Wang", Relation: "Father", Number: "98765432" successfully. | - |
| TC_EC_002 | TS-03 | Emergency Name - Exceeds 100 chars (Max+1) | P2 | BVA Max+1 | [FAILED] | HTML attribute has maxlength="255", allowing 101 characters (FSD Table 4.3 limit is 100 chars). | BUG-007 |
| TC_EC_003 | TS-03 | Emergency Relationship - Enum per FSD 4.3 | P2 | EP Valid | [FAILED] | Dropdown displays Father, Mother instead of standard enum Parent per FSD Table 4.3. | BUG-005 |
| TC_EC_004 | TS-03 | Emergency Name - Empty mandatory check | P1 | EP Negative | [PASSED] | Empty Emergency Name displayed standard error: "This field is required." | - |
| TC_EC_005 | TS-03 | Emergency Number - Empty mandatory check | P1 | EP Negative | [FAILED] | Empty Emergency Phone displayed non-standard error "Enter a valid contact number." instead of "This field is required." (FSD 5.2). | BUG-008 |
| TC_EC_006 | TS-03 | Emergency Number - 8-15 digits length | P2 | BVA Valid | [PASSED] | 8-digit emergency number accepted and saved successfully. | - |
| TC_SG_001 | TS-04 | Singapore Address - Default selection | P1 | Decision Table | [PASSED] | Singapore radio pre-selected by default; Country dropdown disabled. | - |
| TC_SG_002 | TS-04 | Postal Code 6 digits - Auto-fill (569933) | P1 | EP / BVA | [PASSED] | Entered 569933, auto-filled Block: "10" and Street: "Ang Mo Kio Avenue 5". | - |
| TC_SG_003 | TS-04 | Postal Code - Malformed 5 digits rejection | P1 | BVA / EP | [PASSED] | Entered 12345 (5 digits), rejected with error "Enter a valid postal code." | - |
| TC_SG_004 | TS-04 | Floor/Unit N/A - Checking disables inputs | P1 | Decision Table | [PASSED] | Checked N/A: Floor and Unit disabled and marked non-mandatory; existing data retained in disabled state per CQ-04. | - |
| TC_SG_005 | TS-04 | Floor/Unit N/A - Unchecking restores required | P1 | Decision Table | [PASSED] | Unchecked N/A: Floor and Unit re-enabled and restored to mandatory state. | - |
| TC_SG_006 | TS-04 | Postal Code Lookup Failure - Manual Entry | P2 | Error Guessing | [BLOCKED] | Entered 999999 not in addressMap, Block/Street remained editable allowing manual entry. Pending CQ-03 clarification. | CQ-03 Finding |
| TC_SG_007 | TS-04 | Block Number - Max 10 chars (FSD 4.4.1) | P2 | BVA Max | [FAILED] | HTML attribute has maxlength="9", truncating 10th character (FSD Section 4.4.1 specifies max 10 chars). | BUG-007 |
| TC_SG_008 | TS-04 | Street Name - Exceeds 100 chars (Max+1) | P2 | BVA Max+1 | [FAILED] | HTML attribute has maxlength="255", allowing 101 characters (FSD Section 4.4.1 limit is 100 chars). | BUG-007 |
| TC_SG_009 | TS-04 | Building Name - Optional field check | P3 | EP Valid | [PASSED] | Empty Building Name saved successfully without error. | - |
| TC_SG_010 | TS-04 | Singapore Address - Empty Postal Code | P1 | EP Negative | [FAILED] | Empty Postal Code displayed non-standard message "Enter a valid postal code." instead of "This field is required." (FSD 5.2). | BUG-008 |
| TC_SG_011 | TS-04 | Floor/Unit - Empty when N/A is unchecked | P1 | EP Negative | [FAILED] | Empty Floor and Unit with N/A unchecked displayed combined banner "Floor and unit number are required." instead of "This field is required." for each field (FSD 5.2). | BUG-008 |
| TC_NSG_001 | TS-05 | Non-SG Address - Switch to international form | P1 | Decision Table | [PASSED] | Selected Non-Singapore radio, international fields displayed and Country dropdown enabled. | - |
| TC_NSG_002 | TS-05 | Non-SG Address - Country dropdown excludes SG | P1 | Decision Table | [FAILED] | Country dropdown in Non-Singapore mode contains <option>Singapore</option> on HTML line 382. | BUG-003 |
| TC_NSG_003 | TS-05 | Non-SG Address - Complete valid address | P1 | EP Valid | [PASSED] | Entered Country: "Malaysia", Addr1: "123 Jalan Ampang", City: "KL" successfully. | - |
| TC_NSG_004 | TS-05 | Address Line 1 - Empty mandatory check | P1 | EP Negative | [PASSED] | Empty Address line 1 displayed standard error: "This field is required." | - |
| TC_NSG_005 | TS-05 | City - Empty mandatory check | P1 | EP Negative | [PASSED] | Empty City displayed standard error: "This field is required." | - |
| TC_NSG_006 | TS-05 | Address Line 1 & 2 - Boundary Max 255 chars | P2 | BVA Max | [PASSED] | 255 characters accepted in Address line 1 successfully. | - |
| TC_NSG_007 | TS-05 | Non-Singapore Postal Code - Optional field | P2 | EP Valid | [PASSED] | Empty Postal Code in Non-SG mode saved successfully without error. | - |
| TC_SAV_001 | TS-06 | Save - Success & Auto Trainer ID Gen | P1 | State Transition | [PASSED] | Created account successfully, displayed random ID TRNXXXXXX and Status Active in successBox banner (Mock App stays on page without redirecting). | - |
| TC_SAV_002 | TS-06 | Save - Submit form completely blank | P1 | EP Negative | [PASSED] | Clicked Save on empty form, validation errors triggered on all mandatory fields. | - |
| TC_SAV_003 | TS-06 | Duplicate Email - Exact match check | P1 | EP Invalid | [FAILED] | Entered duplicate email bob.wang@curricula.edu.sg, Mock App created account without duplicate checking. | BUG-001 |
| TC_SAV_004 | TS-06 | Duplicate Email - Case-insensitive match | P1 | EP Invalid | [FAILED] | Entered BOB.WANG@CURRICULA.EDU.SG, Mock App created account without duplicate checking. | BUG-001 |
| TC_SAV_005 | TS-06 | Duplicate ID Number - Exact match check | P1 | EP Invalid | [FAILED] | Entered duplicate ID G7666564N, Mock App created account without duplicate checking. | BUG-002 |
| TC_SAV_006 | TS-06 | Concurrency - Save button Double-Click | P1 | Error Guessing | [FAILED] | Save button not disabled during click; double-clicking executes handler twice and generates 2 distinct random Trainer IDs. | BUG-004 |
| TC_SAV_007 | TS-06 | Trainer ID - Sequential increment rule | P2 | State Transition | [FAILED] | Mock App generates IDs using Math.random() (e.g. TRN842914, TRN104928) instead of sequential increment starting from TRN000001 (FSD Section 7). | CQ-06 Finding |
| TC_SAV_008 | TS-06 | Data Hygiene - Automatic whitespace trim | P2 | Error Guessing | [PASSED] | Surrounding whitespace on Name and Email trimmed automatically before saving. | - |
| TC_CAN_001 | TS-07 | Cancel - Clean form discard without prompt | P2 | State Transition | [PASSED] | Clicked Cancel on clean form, page reloaded immediately without warning. | - |
| TC_CAN_002 | TS-07 | Cancel - Unsaved changes -> Select "Stay" | P1 | Decision Table | [PASSED] | Clicked Cancel on populated form, selected "Stay" (or Cancel on dialog), data retained. | - |
| TC_CAN_003 | TS-07 | Cancel - Unsaved changes -> Select "Leave" | P1 | Decision Table | [PASSED] | Clicked Cancel on populated form, selected "Leave" (or OK on dialog), form reset. | - |
| TC_CAN_004 | TS-07 | Cancel - Detect Dirty State on Radio/Select | P2 | Error Guessing | [FAILED] | Modified Radio Gender or Dropdown Nationality and clicked Cancel, Mock App reloaded without Unsaved Changes warning. | BUG-006 |