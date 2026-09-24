# US-03 Curricula Trainer Account — Full 68 Test Cases (from Deliverable 3)


## TS-01 Personal Information

| TC ID | Test Case Name | Test Data | Execution Steps | Expected Result (FSD Standard) | Priority | Technique |
|---|---|---|---|---|---|---|
| TC_PI_001 | Preferred Name - Valid string entry | Preferred Name = "Bob Wang" | Enter "Bob Wang" into Preferred name field. | Value accepted without error. | P1 | EP Valid |
| TC_PI_002 | Preferred Name - Boundary Max 100 characters | String of 100 characters ("A"*100) | Enter exactly 100 characters into Preferred name. | All 100 characters accepted successfully. | P2 | BVA Max |
| TC_PI_003 | Preferred Name - Exceeds 100 chars (BVA Max+1) | String of 101 characters ("A"*101) | Enter/paste 101 characters into Preferred name. | System does not accept Preferred Name exceeding 100 characters. Trainer Account is not created until data complies with maximum limit. [Mock App Deviation: allows 101 characters -> BUG-007.] | P2 | BVA Max+1 |
| TC_PI_004 | Preferred Name - Auto-trim whitespace | "  Bob Wang  " | Enter name with leading/trailing spaces, click Save. | System trims whitespace and stores "Bob Wang". | P3 | Error Guessing |
| TC_PI_005 | Gender - Select Male / Female | Click Radio Male, then Female | 1. Click Male. 2. Switch to Female. | Radio button switches smoothly, single value selected. | P1 | EP Valid |
| TC_PI_006 | ID Type - 4 Document types per FSD 4.1 | Open ID Type dropdown | Click ID Type dropdown and verify options. | Exactly 4 document types: NRIC, FIN, Employment Pass, Passport. [Mock App Deviation: shows extra "S-Pass" -> BUG-009 / FSD Table 4.1 vs narrative section mismatch; clarification required.] | P1 | EP Valid |
| TC_PI_007 | ID Number - Valid NRIC format | ID Type = "NRIC", ID Number = "G7666564N" | Enter valid Singapore NRIC number. | Value accepted and stored accurately. | P1 | EP Valid |
| TC_PI_008 | ID Number - ID Checksum validation | ID Type = "NRIC", ID Number = "S1234567A" | Enter NRIC with invalid Checksum, click Save. | System validates ID Checksum per FSD Section 5d and blocks save. (FSD checksum requirement; test data provisional pending BA/PO confirmation; Mock App does not implement any checksum logic -> BUG-010). | P1 | EP Invalid |
| TC_PI_009 | ID Number - Exceeds 20 chars (BVA Max+1) | String of 21 characters ("A"*21) | Enter 21 characters into ID Number. | System does not accept ID Number exceeding 20 characters. Trainer Account is not created until data complies with maximum limit. [Mock App Deviation: allows exceeding 20 characters -> BUG-007.] | P2 | BVA Max+1 |
| TC_PI_010 | Date of Birth - Valid past date | DOB = "1990-05-15" | Select valid past date of birth. | System accepts date successfully. | P1 | EP Valid |
| TC_PI_011 | Date of Birth - Future date rejection | DOB = "2030-01-01" | Select future date, click Save. | System rejects future date of birth, displays inline validation at Date of Birth field, and does not create Trainer Account. Specific error message is TBD pending BA/PO confirmation. | P1 | EP / BVA |
| TC_PI_012 | File Upload - PDF/PNG/JPG/JPEG <= 10MB | PDF file of 5MB | Upload 5MB PDF file to ID Document. | File uploaded successfully, file name displayed. | P1 | EP / BVA |
| TC_PI_013 | File Upload - Exceeds 10MB limit | PDF file of 11MB | Upload 11MB file to ID Document. | System rejects file and displays: "File size must not exceed 10 MB." | P1 | BVA Max+1 |
| TC_PI_014 | File Upload - Invalid file format (.docx) | File document.docx (500KB) | Upload .docx file. | System rejects file and displays: "Unsupported file format." | P1 | EP Invalid |
| TC_PI_015 | Nationality - Select from Dropdown | Select Singaporean | Open Nationality dropdown and select "Singaporean". | Dropdown correctly registers selected value. | P1 | EP Valid |
| TC_PI_016 | Country of Birth - Select from Dropdown | Select Singapore | Open Country of Birth dropdown and select "Singapore". | Dropdown correctly registers selected value. | P1 | EP Valid |
| TC_PI_017 | Preferred Name - Empty mandatory check | Preferred Name = "" | Leave Preferred name empty, click Save. | Displays inline error: "This field is required." | P1 | EP Negative |
| TC_PI_018 | ID Number - Empty mandatory check | ID Number = "" | Leave ID Number empty, click Save. | Displays inline error: "This field is required." | P1 | EP Negative |
| TC_PI_019 | Date of Birth - Empty mandatory check | DOB = "" | Leave Date of birth empty, click Save. | Displays standard mandatory error: "This field is required." [Mock App Deviation: shows "Enter a valid date of birth." -> BUG-008.] | P1 | EP Negative |
| TC_PI_020 | Nationality - Unselected mandatory check | No selection made | Leave Nationality at default prompt, click Save. | Displays inline error: "This field is required." | P1 | EP Negative |
| TC_PI_021 | Country of Birth - Unselected mandatory check | No selection made | Leave Country of birth at default prompt, click Save. | Displays inline error: "This field is required." | P1 | EP Negative |
| TC_PI_022 | Gender, Race & Tax Resident - Unselected check | Leave all 3 unselected | Leave Gender, Race, Tax Resident unselected, click Save. | Displays "This field is required." error for all 3 fields. | P1 | EP Negative |
| TC_PI_023 | Race Dropdown - Ethnic groups options (CQ-07) | Open Race dropdown | Open Race dropdown and inspect options. | Displays 4 standard groups: Chinese, Malay, Indian, Others. | P2 | EP Valid |

## TS-02 Contact Information

| TC ID | Test Case Name | Test Data | Execution Steps | Expected Result (FSD Standard) | Priority | Technique |
|---|---|---|---|---|---|---|
| TC_CI_001 | Primary Email - Valid email format | Primary Email = "trainer.bob@curricula.edu.sg" | Enter valid email into Primary email address. | Email accepted without error. | P1 | EP Valid |
| TC_CI_002 | Primary Email - Invalid format rejection | "plainaddress", "@missinguser.com" | Enter malformed email, click Save. | Displays inline error: "Enter a valid email address." | P1 | EP Invalid |
| TC_CI_003 | Primary Email - Boundary Max 100 characters | Valid email of exactly 100 chars | Enter 100-character email into Primary Email. | 100-character email accepted successfully. | P2 | BVA Max |
| TC_CI_004 | Primary Phone - Valid Singapore 8 digits (+65) | Code = "+65", Number = "91234567" | Select +65 and enter 8-digit phone number. | Phone number accepted without error. | P1 | BVA Valid |
| TC_CI_005 | Primary Phone - 7 digits rejection (BVA Min-1) | Code = "+65", Number = "9123456" | Select +65 and enter 7 digits, click Save. | System rejects 7-digit phone number, displays inline validation, and does not create Trainer Account. | P2 | BVA Min-1 |
| TC_CI_006 | Primary Phone - 9 digits with code +65 | Code = "+65", Number = "912345678" | Select +65 and enter 9 digits. | Under general FSD rule of 8–15 digits, 9-digit number is accepted. (Mock App rejects when country code is +65 -> Fail / Requirement inconsistency tracked under CQ-09). | P2 | BVA / Observed |
| TC_CI_007 | Phone Numbers - Reject alphabetic characters | Number = "9123ABCD" | Attempt to type letters into Contact Number. | System prevents non-digit input or displays format error. | P2 | EP Invalid |
| TC_CI_008 | Primary Email - Empty mandatory check | Primary Email = "" | Leave Primary Email empty, click Save. | Displays inline error: "This field is required." | P1 | EP Negative |
| TC_CI_009 | Primary Phone - Empty mandatory check | Primary Phone = "" | Leave Primary Phone empty, click Save. | Displays standard mandatory error: "This field is required." [Mock App Deviation: shows "Enter a valid contact number." -> BUG-008.] | P1 | EP Negative |

## TS-03 Emergency Contact

| TC ID | Test Case Name | Test Data | Execution Steps | Expected Result (FSD Standard) | Priority | Technique |
|---|---|---|---|---|---|---|
| TC_EC_001 | Emergency Contact - Valid complete data | Name: "David Wang", Relationship: "Parent", Number: "98765432" | Enter complete valid emergency contact details. | Emergency contact information recorded successfully. | P1 | EP Valid |
| TC_EC_002 | Emergency Name - Exceeds 100 chars (BVA Max+1) | String of 101 characters ("A"*101) | Enter 101 characters into Emergency contact name. | System does not accept Emergency Contact Name exceeding 100 characters. Trainer Account is not created until data complies with maximum limit. [Mock App Deviation: allows exceeding 100 characters -> BUG-007.] | P2 | BVA Max+1 |
| TC_EC_003 | Emergency Relationship - Enum per FSD 4.3 | Open Relationship dropdown | Open dropdown and inspect options. | Displays exact FSD Table 4.3 enum: Parent, Spouse, Sibling, Relative, Friend, Others. [Mock App Deviation: shows Father, Mother -> BUG-005.] | P2 | EP Valid |
| TC_EC_004 | Emergency Name - Empty mandatory check | Emergency Name = "" | Leave Emergency name empty, click Save. | Displays inline error: "This field is required." | P1 | EP Negative |
| TC_EC_005 | Emergency Number - Empty mandatory check | Emergency Number = "" | Leave Emergency number empty, click Save. | Displays standard mandatory error: "This field is required." [Mock App Deviation: shows "Enter a valid contact number." -> BUG-008.] | P1 | EP Negative |
| TC_EC_006 | Emergency Number - Length 8-15 digits | Code = "+65", Number = "98765432" | Enter 8-digit emergency contact number. | Validated and saved successfully. | P2 | BVA Valid |

## TS-04 Singapore Residential Address

| TC ID | Test Case Name | Test Data | Execution Steps | Expected Result (FSD Standard) | Priority | Technique |
|---|---|---|---|---|---|---|
| TC_SG_001 | Singapore Address - Default selection | Open Create Trainer page | Observe Residential Address section. | Singapore radio selected by default; Country/Region automatically set to Singapore and disabled. | P1 | Decision Table |
| TC_SG_002 | Postal Code 6 digits - Auto-fill (569933) | Postal Code = "569933" | Enter 569933 and blur the input field. | Auto-populates Block: "10" and Street: "Ang Mo Kio Avenue 5". | P1 | EP / BVA |
| TC_SG_003 | Postal Code - Malformed 5 digits rejection | Postal Code = "12345" | Enter 5 digits into Postal Code, click Save. | System rejects postal code without exactly 6 digits, displays inline validation, and does not create Trainer Account. | P1 | BVA / EP |
| TC_SG_004 | Floor/Unit N/A - Checking disables inputs | Check Floor/Unit number is not applicable | Check the N/A checkbox. | Floor and Unit disabled and no longer mandatory per FSD. Pre-existing values retained under Working Assumption CQ-04, pending BA/PO confirmation. | P1 | Decision Table |
| TC_SG_005 | Floor/Unit N/A - Unchecking restores required | Uncheck N/A checkbox | Uncheck the N/A checkbox. | Floor and Unit inputs enabled and marked mandatory. | P1 | Decision Table |
| TC_SG_006 | Postal Code Fallback - Manual Block & Street | Postal = "999999", Block: "888", Street: "Custom St" | Enter unmapped postal code, manually type Block/Street. | Block and Street remain editable under Working Assumption CQ-03. Expected behavior on lookup failure pending BA/PO confirmation. | P2 | Error Guessing |
| TC_SG_007 | Block Number - Max 10 chars (FSD 4.4.1) | String of 10 characters ("1234567890") | Enter exactly 10 characters into Block Number. | System accepts Block Number up to 10 characters per FSD Section 4.4.1. [Mock App Deviation: only allows 9 characters -> BUG-007.] | P2 | BVA Max |
| TC_SG_008 | Street Name - Exceeds 100 chars (BVA Max+1) | String of 101 characters ("A"*101) | Enter 101 characters into Street Name. | System does not accept Street Name exceeding 100 characters. Trainer Account is not created until data complies with maximum limit. [Mock App Deviation: allows exceeding 100 characters -> BUG-007.] | P2 | BVA Max+1 |
| TC_SG_009 | Building Name - Optional field check | Building Name = "" | Leave Building name empty, populate other fields. | Address saved successfully without error. | P3 | EP Valid |
| TC_SG_010 | Singapore Address - Empty Postal Code | Postal Code = "" | Leave Postal Code empty, click Save. | Displays standard mandatory error: "This field is required." [Mock App Deviation: shows "Enter a valid postal code." -> BUG-008.] | P1 | EP Negative |
| TC_SG_011 | Floor/Unit - Empty when N/A is unchecked | Floor = "", Unit = "", N/A = Unchecked | Leave Floor and Unit empty with N/A unchecked, click Save. | Displays "This field is required." beneath Floor Number and Unit Number; Trainer Account is not created. | P1 | EP Negative |

## TS-05 Non-Singapore Residential Address

| TC ID | Test Case Name | Test Data | Execution Steps | Expected Result (FSD Standard) | Priority | Technique |
|---|---|---|---|---|---|---|
| TC_NSG_001 | Non-SG Address - Switch to international form | Click Radio Non-Singapore | Select Non-Singapore radio button. | Country dropdown enabled, international address inputs displayed. | P1 | Decision Table |
| TC_NSG_002 | Non-SG Address - Country dropdown excludes SG | Open Country/region dropdown | Open Country dropdown in Non-Singapore mode. | Country list must NOT include "Singapore" (FSD 4.4.2). [Mock App Deviation: HTML line 382 includes Singapore -> BUG-003.] | P1 | Decision Table |
| TC_NSG_003 | Non-SG Address - Complete valid address | Country: "Malaysia", Addr1: "123 Jalan Ampang", City: "KL" | Enter complete valid international address. | International address saved successfully. | P1 | EP Valid |
| TC_NSG_004 | Address Line 1 - Empty mandatory check | Address Line 1 = "" | Leave Address line 1 empty, click Save. | Displays inline error: "This field is required." | P1 | EP Negative |
| TC_NSG_005 | City - Empty mandatory check | City = "" | Leave City empty, click Save. | Displays inline error: "This field is required." | P1 | EP Negative |
| TC_NSG_006 | Address Line 1 - Boundary Max 255 chars | String of 255 characters ("A"*255) | Enter 255 characters into Address line 1. | System accepts all 255 valid characters on Address Line 1. | P2 | BVA Max |
| TC_NSG_007 | Non-Singapore Postal Code - Optional field | Postal Code = "" | Leave Postal Code empty in Non-SG mode, click Save. | Saved successfully without error. | P2 | EP Valid |

## TS-06 Save Action & System Logic

| TC ID | Test Case Name | Test Data | Execution Steps | Expected Result (FSD Standard) | Priority | Technique |
|---|---|---|---|---|---|---|
| TC_SAV_001 | Save - Success & Auto Trainer ID Generation | Complete valid form data | Fill all mandatory fields validly, click Save. | Trainer Account is created; unique Trainer ID formatted as TRN + 6 sequential digits; Status is Active; system displays "Trainer account has been created successfully." and navigates to Trainer Details page. | P1 | State Transition |
| TC_SAV_002 | Save - Empty mandatory fields submit | Empty form | Click Save on completely blank form. | Inline error messages displayed across all mandatory fields. | P1 | EP Negative |
| TC_SAV_003 | Duplicate Email - Exact match prevention | Existing email: bob.wang@curricula.edu.sg | Enter existing email, click Save. | Creation blocked with error: "An account with this email address already exists." [Mock App Deviation: missing duplicate check -> BUG-001.] | P1 | EP Invalid |
| TC_SAV_004 | Duplicate Email - Case-insensitive match | BOB.WANG@CURRICULA.EDU.SG | Enter uppercase duplicate email, click Save. | Case-insensitive check blocks creation and displays duplicate error. [Mock App Deviation: missing duplicate check -> BUG-001.] | P1 | EP Invalid |
| TC_SAV_005 | Duplicate ID Number - Exact match check | Existing ID: G7666564N | Enter existing ID Number, click Save. | Creation blocked with error: "An account with this ID number already exists." [Mock App Deviation: missing duplicate check -> BUG-002.] | P1 | EP Invalid |
| TC_SAV_006 | Concurrency - Multiple Save clicks handling | Complete valid form | Double-click Save button in rapid succession. | Only one account creation request is processed and exactly one Trainer Account/Trainer ID is generated. The system must not create duplicate records when the user clicks Save multiple times (Error Guessing -> BUG-004). | P1 | Error Guessing |
| TC_SAV_007 | Trainer ID - Sequential increment rule | Valid form | Create consecutive trainer accounts. | Trainer ID follows sequential increment TRN + 6 digits. | P2 | State Transition |
| TC_SAV_008 | Data Hygiene - Automatic whitespace trim | Name & Email with surrounding spaces | Enter name/email with leading/trailing spaces, click Save. | System automatically trims whitespace before database persistence. | P2 | Error Guessing |

## TS-07 Cancel Action & Form State

| TC ID | Test Case Name | Test Data | Execution Steps | Expected Result (FSD Standard) | Priority | Technique |
|---|---|---|---|---|---|---|
| TC_CAN_001 | Cancel - Clean form discard without prompt | Form with zero user inputs | Open Create Trainer page and immediately click Cancel. | User is navigated back to Trainer Listing page without a confirmation popup. | P2 | State Transition |
| TC_CAN_002 | Cancel - Unsaved changes -> Select "Stay" | Partially populated form | Enter name, click Cancel -> Select "Stay" (or Cancel on dialog). | Dialog closes, all entered form data retained. | P1 | Decision Table |
| TC_CAN_003 | Cancel - Unsaved changes -> Select "Leave" | Partially populated form | Enter name, click Cancel -> Select "Leave" (or OK on dialog). | Form changes discarded and user navigated back to Trainer Listing page. | P1 | Decision Table |
| TC_CAN_004 | Cancel - Detect Dirty State on Radio/Select | Modified Gender = Female or Nationality | Modify single Radio button or Dropdown (no text entered), click Cancel. | System recognizes Dirty State and displays Unsaved Changes prompt. [Mock App Deviation: misses radio/select elements -> BUG-006.] | P2 | Error Guessing |