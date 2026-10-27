# Test Specification: UAT-001 — Complete Education Account Provisioning, Idempotency & Full Coverage

> **Module**: F01 (Education Account Lifecycle)  
> **Ticket / Feature**: `f01-education-accounts`  
> **Target Route**: `http://localhost:5173/education-accounts` (SCR-ADM-01)  
> **Target Persona**: MOE HQ Admin (`admin@IAM.edu.vn`)  
> **Traceability**: US-001, UAT-001, F01-BR01~BR05, F01-AC01~AC12, AF01~AF04, EF01~EF03, D-20, ASM-15
> **Total Test Cases**: 32 (5 Suites + E2E)

---

## Section 1: The 5 Core Pillars of Test Design

### 1.1 Business Rules (BR) — From FS-01 v1.2
- **F01-BR01 (Singapore Citizenship Mandate)**: Only Singapore Citizens are eligible for Education Accounts. Non-citizens (PR/Foreigner) are excluded.
- **F01-BR02 (Age 7 to Under-16 Window)**: Eligible age from 7th birthday until before 16th birthday.
- **F01-BR03 (DOB Identity Source)**: Age calculated strictly from DOB in Government Dataset.
- **F01-BR04 (Parental NRIC Independence)**: Missing Father/Mother NRIC does NOT block EA creation.
- **F01-BR05 (NRIC De-duplication & Idempotency)**: Each citizen has max 1 EA; re-sync creates 0 duplicates.

### 1.2 Acceptance Criteria (AC) — From FS-01 v1.2 & component_specs/f01
- **F01-AC01**: Initial sync provisions SC age 7-15 with Active status, SGD 0.00.
- **F01-AC03**: Non-citizen (PR/Foreigner) not provisioned EA.
- **F01-AC04**: Child < 7 years excluded from EA.
- **F01-AC05**: Citizen ≥ 16 years excluded or marked Deactive.
- **F01-AC06**: Existing Active account not re-created.
- **F01-AC07**: Existing Closed account not re-created.
- **F01-AC08**: Missing required field → record skipped.
- **F01-AC09**: Missing Father/Mother NRIC → EA still created if eligible.
- **F01-AC12**: Re-sync produces 0 duplicate accounts (Idempotency).

### 1.3 Validation Rules — From component_specs/f01/atomic/
- **12-Layer Matrix (ASM-15 Standard)**:
  - L01 Empty: Default list shown
  - L02 Reset: Clear filters, restore defaults
  - L03 Whitespace (ASM-15): Auto-trim to empty, no whitespace queries sent
  - L04 Leading/Trailing: Auto-trim both ends
  - L05-L06 BVA Min/Max Length: NRIC 9-char format, Name ≤100
  - L07 Stress Paste: >1000 chars truncated, no crash
  - L08 Injection Symbols: Safe plain-text handling
  - L09 Unicode/UTF-8: Full support Vietnamese, Chinese, etc.
  - L10 XSS Vectors: HTML-escaped, no script execution
  - L11 i18n: Zero raw keys (features.ea.*, validation.*)
  - L12 Persistence: State preserved via Query Params

### 1.4 Functional Flow & State Machine
**Account Creation Flow** (F01-INT-FLOW-01):
1. Government Citizen API → Extract required fields (NRIC, Name, DOB, Citizenship)
2. Eligibility Validator → Check SC + Age 7-16
3. Duplicate Prevention → Check existing EA via NRIC
4. EA Creation → Generate Account#, Balance 0.00, Status Active
5. UI Refresh → sync_job_status_card increments, ea_account_table_pagination updates

**Account Closure Flow** (F02-INT-FLOW-02) — **Deferred scope for UAT-001 E2E**:
- Backend-triggered closure on access when Age ≥ 16

### 1.5 Error Handling & Visual Feedback
- **EF01 (Source Auth Failure)**: Job marked FAILED, no corrupt accounts
- **EF02 (Required Field Missing)**: Skip record only, continue batch
- **EF03 (Data Conflict)**: Abort creation, log reason for manual review
- **Dialog Safety**: Cancel button closes without POST mutation
- **API 500 Error**: Error banner + Retry button, no crash
- **i18n Guard**: Zero unrendered keys; exact localized strings
- **XSS Protection**: HTML-escaped, safe plain-text
- **Console Health**: Zero uncaught JS exceptions

---

## Section 2: Test Suite Allocation Overview

| Test Suite ID | Pillar / Focus | Test Objective | Total TCs | Severity |
| :--- | :--- | :--- | :--- | :--- |
| **TS-UAT001-01** | **Pillar 1: Initial Sync & Eligible Provisioning** | Sync execution, Active status, SGD 0.00, missing parent tolerance | 5 | S1 (Critical) |
| **TS-UAT001-02** | **Pillar 2: Ineligibility Gate & BVA** | Non-citizen exclusion, age boundaries, required field validation | 6 | S1 (Critical) |
| **TS-UAT001-03** | **Pillar 3: Idempotency & Duplicate Prevention** | Re-sync zero duplicates, dialog cancel safety | 5 | S1 (Critical) |
| **TS-UAT001-04** | **Pillar 4: Search, Filter & Table** | NRIC search, status filter, modal, table pagination, NRIC masking, currency format | 8 | S2 (High) |
| **TS-UAT001-05** | **Pillar 5: Error Handling & UI Health** | API 500, i18n guard, console health, auth guard, XSS, missing fields, dialog safety | 7 | S2 (High) |
| **TS-UAT001-E2E** | **Full End-to-End Workflow** | 3-phase journey: Sync#1 → Validate → Sync#2 zero duplicates | 1 | S1 (Critical) |

---

## Section 3: Master Test Case Matrix (20-Column AvePoint Format)

| ID | Scenario ID | Title | Test Suite | Page | Severity | Priority | Execution Status | Test Type | Environment | Preconditions | Test Data | Steps Test | Test Steps | Expected Result | Actual Result | Assumption Ref | Defect ID | Traceability | Note |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| TC-UAT001-01 | TS-UAT001-01 | Verify initial synchronization triggers successfully via confirmation dialog | Sync & Eligible | EA Lifecycle | S1 | Critical | Ready | Functional | localhost:5173 | Authenticated as MOE HQ Admin | data/f01/f01_uat001_data.json | Step 1, 2, 3 | 1. Navigate /education-accounts 2. Click Manual sync 3. Verify dialog title 4. Click Confirm | 1. Dialog "Sync citizen data" appears 2. POST /trigger-citizen-sync fires (200 OK) 3. Table refreshes | Not Run | F01-BR01, F01-AC01 | None | US-001, UAT-001 Step 1 | Initial sync dialog |
| TC-UAT001-02 | TS-UAT001-01 | Verify SC aged 7-15 receives Active EA with SGD 0.00 | Sync & Eligible | EA Lifecycle | S1 | Critical | Ready | Functional | localhost:5173 | Sync completed | data/f01/f01_uat001_data.json (eligible_student: Isaac Teo T0000787X age 10) | Step 1, 2, 3, 4 | 1. Search NRIC T0000787X 2. Inspect table row 3. Verify citizenship 4. Verify balance | 1. Citizenship: Singapore Citizen 2. Age: 10 (within 7-15) 3. Status: Active (green badge) 4. Balance: $0.00 SGD | Not Run | F01-BR01, F01-BR02, F01-AC01 | None | US-001, F01-AC01 | SC eligible provision |
| TC-UAT001-03 | TS-UAT001-01 | Verify BVA: citizen exactly 7 years old receives Active EA | Sync & Eligible | EA Lifecycle | S1 | Critical | Ready | Functional | localhost:5173 | Sync completed | data/f01/f01_uat001_data.json (age_boundary_7: dob = today - 7yrs exactly) | Step 1, 2, 3 | 1. Inspect 7yo student 2. Verify status 3. Verify balance | 1. Status: Active 2. Balance: $0.00 SGD | Not Run | F01-BR02, F01-AC01 | None | US-001, BVA min age | Age 7 boundary |
| TC-UAT001-04 | TS-UAT001-01 | Verify BVA: citizen exactly 15 years old (last eligible) receives Active EA | Sync & Eligible | EA Lifecycle | S1 | Critical | Ready | Functional | localhost:5173 | Sync completed | data/f01/f01_uat001_data.json (age_boundary_15: dob = today - 15yrs) | Step 1, 2, 3 | 1. Inspect 15yo student 2. Verify status 3. Verify balance | 1. Status: Active 2. Balance: $0.00 SGD | Not Run | F01-BR02, F01-AC01 | None | US-001, BVA max age | Age 15 boundary |
| TC-UAT001-05 | TS-UAT001-01 | Verify missing Father/Mother NRIC does NOT block EA (AF04) | Sync & Eligible | EA Lifecycle | S1 | Critical | Ready | Functional | localhost:5173 | Sync completed | data/f01/f01_uat001_data.json (eligible_missing_parent: Adam Wong T0000539X, no parent NRIC) | Step 1, 2, 3, 4 | 1. Search T0000539X 2. Open profile modal 3. Inspect parent NRIC fields 4. Verify account Active | 1. Parent NRIC fields: empty 2. Account Status: Active 3. Balance: $0.00 SGD | Not Run | F01-BR04, F01-AC09 | None | US-001, AF04 | Missing parent NRIC OK |
| TC-UAT001-06 | TS-UAT001-02 | Verify PR (Permanent Resident) does NOT receive EA | Ineligibility Gate | EA Lifecycle | S1 | Critical | Ready | Functional | localhost:5173 | Sync completed | Mock dataset with PR record | Step 1, 2 | 1. Query synced accounts for non-citizens 2. Verify zero EA for PR | 1. Zero EA created for PR | Not Run | F01-BR01, F01-AC03, AF01 | None | US-001, AF01 | Non-citizen PR excluded |
| TC-UAT001-07 | TS-UAT001-02 | Verify Foreigner does NOT receive EA | Ineligibility Gate | EA Lifecycle | S1 | Critical | Ready | Functional | localhost:5173 | Sync completed | Mock dataset with Foreigner record | Step 1, 2 | 1. Query synced accounts for foreigners 2. Verify zero EA | 1. Zero EA created for foreigner | Not Run | F01-BR01, F01-AC03, AF01 | None | US-001, AF01 | Non-citizen foreigner excluded |
| TC-UAT001-08 | TS-UAT001-02 | Verify BVA: child age 6 (below min 7) excluded | Ineligibility Gate | EA Lifecycle | S1 | Critical | Ready | Functional | localhost:5173 | Sync completed | data/f01/f01_uat001_data.json (age_6: dob = today - 6yrs - 1day) | Step 1, 2 | 1. Query accounts for age <7 2. Verify zero EA | 1. Zero EA created for age 6 | Not Run | F01-BR02, F01-AC04, AF02 | None | US-001, BVA under 7 | Age 6 boundary excluded |
| TC-UAT001-09 | TS-UAT001-02 | Verify BVA: citizen exactly 16 years old excluded/Deactive | Ineligibility Gate | EA Lifecycle | S1 | Critical | Ready | Functional | localhost:5173 | Sync completed | data/f01/f01_uat001_data.json (age_16_boundary) | Step 1, 2 | 1. Query 16yo student 2. Verify status | 1. Status: Deactive OR zero EA | Not Run | F01-BR05, F01-AC05, AF02 | None | US-001, BVA 16 boundary | Age 16 excluded |
| TC-UAT001-10 | TS-UAT001-02 | Verify citizen age 17+ excluded/Deactive | Ineligibility Gate | EA Lifecycle | S1 | Critical | Ready | Functional | localhost:5173 | Sync completed | data/f01/f01_uat001_data.json (ineligible_over_age: Ethan Rahman T0000911X age 17) | Step 1, 2, 3 | 1. Search T0000911X 2. Verify age 3. Inspect status | 1. Age: 17 2. Status: Deactive 3. No active wallet | Not Run | F01-BR05, F01-AC05 | None | US-001, Age 17+ | Age 17+ closure |
| TC-UAT001-11 | TS-UAT001-02 | Verify missing required NRIC field → record skipped | Ineligibility Gate | EA Lifecycle | S1 | Critical | Ready | Functional | localhost:5173 | Sync job processing | Mock dataset with missing NRIC | Step 1, 2, 3 | 1. Process citizen record with blank NRIC 2. Verify skip logged 3. Verify other records continue | 1. Record skipped (logged EF02) 2. No EA created 3. Batch continues successfully | Not Run | F01-AC08, EF02 | None | US-001, EF02 | Required field validation |
| TC-UAT001-12 | TS-UAT001-03 | Verify Sync #2 produces ZERO duplicate accounts (Idempotency) | Idempotency | EA Lifecycle | S1 | Critical | Ready | Functional | localhost:5173 | Sync #1 completed, row count recorded | data/f01/f01_uat001_data.json | Step 1, 2, 3, 4, 5 | 1. Record total row count before Sync#2 2. Trigger Manual sync again 3. Click Confirm 4. Wait completion 5. Re-query row count | 1. Sync #2 HTTP 200 2. Total row count unchanged 3. Zero duplicates 4. All balances preserved | Not Run | F01-BR05, F01-AC06, F01-AC12, AF03 | None | US-001, Idempotency | Re-sync #2 no dupes |
| TC-UAT001-13 | TS-UAT001-03 | Verify existing Active account re-sync → NOT recreated | Idempotency | EA Lifecycle | S1 | Critical | Ready | Functional | localhost:5173 | Active account exists | data/f01/f01_uat001_data.json (eligible_student: Isaac T0000787X) | Step 1, 2, 3, 4 | 1. Note account details + balance 2. Trigger Sync #2 3. Click Confirm 4. Re-query same account | 1. Account not duplicated 2. Balance unchanged 3. Created Date same | Not Run | F01-AC06, AF03 | None | US-001, No recreate | Active not re-created |
| TC-UAT001-14 | TS-UAT001-03 | Verify existing Closed account → NOT recreated on re-sync | Idempotency | EA Lifecycle | S1 | Critical | Ready | Functional | localhost:5173 | Closed account exists | Mock Closed EA | Step 1, 2, 3, 4 | 1. Inspect Closed account 2. Trigger Sync #2 3. Confirm 4. Verify Closed account status unchanged | 1. Account not duplicated 2. Status: Closed (not re-opened) 3. Actual Closed Date preserved | Not Run | F01-AC07, AF03 | None | US-001, No recreate closed | Closed not re-created |
| TC-UAT001-15 | TS-UAT001-03 | Verify Cancel sync dialog → dialog closes, zero POST fired | Idempotency | EA Lifecycle | S2 | High | Ready | UI / Functional | localhost:5173 | Admin Portal open | Dialog trigger | Step 1, 2, 3, 4 | 1. Click Manual sync 2. In dialog, click Cancel 3. Monitor network 4. Inspect table | 1. Dialog closes immediately 2. Zero POST to sync endpoint 3. Table unchanged | Not Run | Dialog Cancel Rule | None | US-001, Dialog safety | Cancel sync safe |
| TC-UAT001-16 | TS-UAT001-03 | Verify duplicate identical NRIC records in dataset → only 1 EA created | Idempotency | EA Lifecycle | S1 | Critical | Ready | Functional | localhost:5173 | Sync processing | Mock dataset with 2 identical NRIC records | Step 1, 2, 3 | 1. Dataset contains duplicate NRIC rows 2. Process sync 3. Query final EA count for that NRIC | 1. Only 1 EA created (not 2) 2. Logged data conflict handling | Not Run | F01-AC12, EF03 | None | US-001, Duplicate handling | Dedup identical records |
| TC-UAT001-17 | TS-UAT001-04 | Verify search by NRIC isolates single matching account | Search & Filter | EA Lifecycle | S2 | High | Ready | UI / Functional | localhost:5173 | Accounts table loaded | data/f01/f01_uat001_data.json (search_nric: T0000787X) | Step 1, 2, 3, 4 | 1. Type NRIC T0000787X 2. Click Search 3. Inspect table rows 4. Verify count | 1. Exactly 1 matching row: Isaac Teo | Not Run | F01-COMP-SEARCH-FILTER, ASM-15 | None | US-001, Search NRIC | NRIC search isolation |
| TC-UAT001-18 | TS-UAT001-04 | Verify search by full name returns matching accounts | Search & Filter | EA Lifecycle | S2 | High | Ready | UI / Functional | localhost:5173 | Accounts table loaded | data/f01/f01_uat001_data.json (search_name: Isaac Teo) | Step 1, 2, 3 | 1. Type name Isaac Teo 2. Click Search 3. Verify matching rows | 1. Table filters to matching student(s) | Not Run | F01-COMP-SEARCH-FILTER | None | US-001, Search name | Name search filter |
| TC-UAT001-19 | TS-UAT001-04 | Verify whitespace-only search (ASM-15) treated as empty → all accounts shown | Search & Filter | EA Lifecycle | S2 | High | Ready | UI / Functional | localhost:5173 | Accounts table loaded | Whitespace input "     " | Step 1, 2, 3, 4 | 1. Input only spaces into search 2. Click Search 3. Backend trims 4. Inspect table | 1. Whitespace trimmed (L03 matrix) 2. Default list shown 3. No whitespace query sent | Not Run | ASM-15 | None | US-001, ASM-15 | Whitespace trim L03 |
| TC-UAT001-20 | TS-UAT001-04 | Verify Status filter Active → all visible rows Active | Search & Filter | EA Lifecycle | S2 | High | Ready | UI / Functional | localhost:5173 | Accounts table loaded | Status filter value "1" (Active) | Step 1, 2, 3 | 1. Select Status dropdown Active 2. Click Search 3. Inspect all rows | 1. Every visible row has Status: Active 2. Deactive rows excluded (L04 matrix) | Not Run | F01-COMP-TABLE-PAGINATION | None | US-001, Status filter | Status Active filter |
| TC-UAT001-21 | TS-UAT001-04 | Verify Status filter Deactive → all visible rows Deactive | Search & Filter | EA Lifecycle | S2 | High | Ready | UI / Functional | localhost:5173 | Accounts table loaded | Status filter value "2" (Deactive) | Step 1, 2, 3 | 1. Select Status dropdown Deactive 2. Click Search 3. Inspect all rows | 1. Every visible row has Status: Deactive 2. Active rows excluded | Not Run | F01-COMP-TABLE-PAGINATION | None | US-001, Status filter | Status Deactive filter |
| TC-UAT001-22 | TS-UAT001-04 | Verify Student Profile modal opens, displays demographics, closes cleanly | Search & Filter | EA Lifecycle | S2 | High | Ready | UI / Visual | localhost:5173 | Accounts table loaded, at least 1 row | First student row | Step 1, 2, 3, 4, 5 | 1. Click View details on row 2. Inspect modal heading 3. Verify demographics displayed 4. Click Close 5. Verify modal dismissed | 1. Modal heading: Student Profile 2. Demographics: Code, NRIC (masked), DOB, Age, Gender, Address 3. Close button works 4. Modal hidden (L12 lifecycle) | Not Run | F01-AC01, profile modal BSK | None | US-001, Modal lifecycle | Profile details modal |
| TC-UAT001-23 | TS-UAT001-04 | Verify NRIC in table masked (D-20: no raw NRIC in DOM) | Search & Filter | EA Lifecycle | S2 | High | Ready | Security | localhost:5173 | Accounts table loaded | data/f01/f01_uat001_data.json (all rows) | Step 1, 2, 3 | 1. Inspect table NRIC column 2. Check DOM data-nric attributes 3. Verify masking pattern | 1. NRIC displayed masked: T*****345A 2. Raw NRIC NOT in data-nric (D-20) 3. Zero PII exposure | Not Run | D-20 | None | US-001, NRIC masking | NRIC PII protection |
| TC-UAT001-24 | TS-UAT001-04 | Verify Balance displayed in SGD 2-decimal format | Search & Filter | EA Lifecycle | S2 | High | Ready | Functional | localhost:5173 | Accounts table loaded with varying balances | data/f01/f01_uat001_data.json (balances: 0, 15.5, 1200.75) | Step 1, 2, 3 | 1. Inspect Balance column 2. Verify formatting 3. Check currency symbol | 1. $0.00 SGD 2. $15.50 SGD 3. $1,200.75 SGD (L03 currency matrix) | Not Run | 2.3 Monetary rule | None | US-001, Currency format | SGD format validation |
| TC-UAT001-25 | TS-UAT001-05 | Verify API 500 → Error banner, Retry button, no crash | Error Handling | EA Lifecycle | S2 | High | Ready | Functional | localhost:5173 | Mock API returning 500 | HTTP 500 error trigger | Step 1, 2, 3, 4 | 1. Mock table API 500 2. Trigger table load 3. Inspect error state 4. Verify Retry button | 1. Error banner visible 2. Error text: "Không thể tải..." 3. Retry button present 4. UI stable (no crash) | Not Run | Error handling | None | US-001, API 500 | Error resilience |
| TC-UAT001-26 | TS-UAT001-05 | Verify zero raw i18n keys (features.ea.*) leaked in UI | Error Handling | EA Lifecycle | S2 | High | Ready | Quality / i18n | localhost:5173 | Authenticated session | Regex pattern: features.* | Step 1, 2, 3 | 1. Navigate to /education-accounts 2. Extract all visible DOM text 3. Search for untranslated keys | 1. Zero raw keys (features.ea.*, validation.*) 2. All text localized 3. L11 compliance | Not Run | L11, Zero i18n rule | None | US-001, i18n Guard | i18n leak protection |
| TC-UAT001-27 | TS-UAT001-05 | Verify console UI health: zero uncaught JS errors | Error Handling | EA Lifecycle | S2 | High | Ready | UI / Stability | localhost:5173 | Authenticated session, console listener | Console error listener | Step 1, 2, 3, 4, 5 | 1. Attach console error listener 2. Navigate /education-accounts 3. Execute search 4. Trigger sync 5. Inspect errors | 1. Zero uncaught TypeErrors 2. Zero uncaught ReferenceErrors 3. Console clean 4. Page stable | Not Run | Invariant 8 Console | None | US-001, Console health | Console UI health |
| TC-UAT001-28 | TS-UAT001-05 | Verify auth route guard: unauthenticated → redirect /login | Error Handling | EA Lifecycle | S2 | High | Ready | Security | localhost:5173 | Unauthenticated context (no cookies) | Route /education-accounts | Step 1, 2, 3 | 1. New context, no auth cookies 2. Navigate /education-accounts 3. Inspect final URL | 1. Access blocked 2. Redirect to /login 3. Auth Guard verified | Not Run | Auth Guard | None | US-001, Auth Guard | Route protection |
| TC-UAT001-29 | TS-UAT001-05 | Verify XSS in search input sanitized, not executed | Error Handling | EA Lifecycle | S2 | High | Ready | Security | localhost:5173 | Accounts table loaded | XSS payload: <script>alert('xss')</script> | Step 1, 2, 3, 4 | 1. Input XSS into search 2. Click Search 3. Inspect console 4. Verify no execution | 1. Script not executed 2. Text HTML-escaped 3. Table shows "No accounts" (L10 matrix) 4. UI stable | Not Run | L10, L08 | None | US-001, XSS Guard | XSS protection |
| TC-UAT001-30 | TS-UAT001-05 | Verify missing required field (blank NRIC) in citizen record → skip + continue batch | Error Handling | EA Lifecycle | S2 | High | Ready | Functional | localhost:5173 | Sync job processing | Mock dataset: record with missing NRIC + 1 valid record after it | Step 1, 2, 3, 4 | 1. Process citizen batch with blank NRIC in middle 2. Verify skip logged (EF02) 3. Verify next record processed 4. Verify 1 EA created (not 0, not 2) | 1. EF02 logged 2. Valid record processed 3. Batch continuous (not aborted) 4. Exactly 1 EA from valid record | Not Run | F01-AC08, EF02 | None | US-001, EF02 | Required field resilience |
| TC-UAT001-31 | TS-UAT001-05 | Verify sync dialog Cancel closes safely without POST mutation | Error Handling | EA Lifecycle | S2 | High | Ready | UI / Functional | localhost:5173 | Admin Portal open | Dialog trigger + network monitor | Step 1, 2, 3, 4 | 1. Click Manual sync 2. Dialog appears 3. Click Cancel 4. Monitor network traffic | 1. Dialog closes 2. Zero POST to sync endpoint 3. Network request count unchanged 4. Table untouched | Not Run | Dialog safety | None | US-001, Dialog cancel | Dialog cancel safety |
| TC-UAT001-32 | TS-UAT001-E2E | Full E2E: Initial Sync → Data Validation → Sync #2 Zero Duplicates | Full E2E | EA Lifecycle | S1 | Critical | Ready | E2E Acceptance | localhost:5173 | Authenticated as MOE HQ Admin, virgin dataset | data/f01/f01_uat001_data.json (full E2E set) | Step 1-14 (See test steps) | **Phase 1**: 1. Trigger Sync#1 2. Confirm dialog 3. Verify SC 7-15 Active 4. Verify non-citizens skipped 5. Record row count **Phase 2**: 6. Search Isaac Teo (T0000787X) 7. Verify Active+SGD 0.00 8. Search PR/Foreigner verify excluded 9. Verify 16yo Deactive 10. Verify missing parent still Active **Phase 3**: 11. Trigger Sync#2 12. Confirm 13. Verify same row count 14. Zero duplicates | **Phase 1**: 1. Sync#1 succeeds 2. POST fired 200 OK **Phase 2**: 3. SC 7-15 Active, SGD 0.00 4. Non-citizens not in Active 5. Over-age Deactive 6. Missing parent Active **Phase 3**: 7. Sync#2 succeeds 8. Row count unchanged 9. Idempotency confirmed 10. E2E journey complete | Not Run | UAT-001 Master Spec, F01-BR01~BR05, F01-AC01/03/04/05/06/09/12 | None | US-001, UAT-001 Full | Full acceptance journey |

---

## Section 4: Live DOM Locators Extracted via BSK (Browser-Skill Reconnaissance)

| Element Name | Display Label | Actual Selector | Element Type |
| :--- | :--- | :--- | :--- |
| Page Heading | Education Accounts | `h1#education-accounts-heading, h1:has-text("Education Accounts")` | `<h1>` |
| Search Input | Search | `form[role="search"] input[type="search"]` | `<input type="search">` |
| Status Select | Status | `form[role="search"] select:has(option[value="1"])` | `<select>` |
| Citizenship Select | Citizenship | `form[role="search"] select:has(option[value="5"])` | `<select>` |
| Apply Search | Search | `form[role="search"] button[type="submit"]:has-text("Search")` | `<button type="submit">` |
| Manual Sync Button | Manual sync | `button:has-text("Manual sync")` | `<button type="button">` |
| Sync Dialog | Sync citizen data | `[role="dialog"]:has-text("Sync citizen data"), [role="alertdialog"]` | `<div>` |
| Dialog Confirm | Confirm | `button:has-text("Confirm")` | `<button type="button">` |
| Dialog Cancel | Cancel | `button:has-text("Cancel")` | `<button type="button">` |
| Accounts Table | Student profiles table | `table` | `<table>` |
| Table Rows | Student rows | `table tbody tr` | `<tr>` |
| View Details Button | View details | `button:has-text("View details")` | `<button type="button">` |
| Student Profile Dialog | Student Profile | `[role="dialog"]:has-text("Student Profile")` | `<div>` |
| Dialog Close Button | Close | `[role="dialog"] button:has-text("Close")` | `<button>` |
| Pagination Next | Next | `button:has-text("Next")` | `<button>` |
| Pagination Previous | Previous | `button:has-text("Previous")` | `<button>` |

---

## Section 5: Coverage Matrix — BR/AC/AF/EF → TC ID Mapping

| Rule ID | Rule Name | Coverage TCs | Count | Status |
| :--- | :--- | :--- | :--- | :--- |
| **F01-BR01** | Singapore Citizenship Mandate | TC-01, TC-02, TC-06, TC-07, TC-32 | 5 | ✓ Covered |
| **F01-BR02** | Age 7-16 Window | TC-03, TC-04, TC-08, TC-09, TC-10, TC-32 | 6 | ✓ Covered |
| **F01-BR03** | DOB Identity Source | TC-03, TC-04 | 2 | ✓ Covered |
| **F01-BR04** | Parental NRIC Independence | TC-05 | 1 | ✓ Covered |
| **F01-BR05** | NRIC De-duplication | TC-12, TC-13, TC-14, TC-16 | 4 | ✓ Covered |
| **F01-AC01** | Initial sync provisions Active, SGD 0.00 | TC-01, TC-02, TC-03, TC-04, TC-32 | 5 | ✓ Covered |
| **F01-AC03** | Non-citizen excluded | TC-06, TC-07 | 2 | ✓ Covered |
| **F01-AC04** | Age <7 excluded | TC-08 | 1 | ✓ Covered |
| **F01-AC05** | Age ≥16 excluded/Deactive | TC-09, TC-10 | 2 | ✓ Covered |
| **F01-AC06** | Existing Active not re-created | TC-12, TC-13 | 2 | ✓ Covered |
| **F01-AC07** | Existing Closed not re-created | TC-14 | 1 | ✓ Covered |
| **F01-AC08** | Missing required field → skip | TC-11, TC-30 | 2 | ✓ Covered |
| **F01-AC09** | Missing parent NRIC OK | TC-05 | 1 | ✓ Covered |
| **F01-AC12** | Idempotency zero duplicates | TC-12, TC-16 | 2 | ✓ Covered |
| **AF01** | Non-citizen skip | TC-06, TC-07 | 2 | ✓ Covered |
| **AF02** | Age ineligible skip | TC-08, TC-09 | 2 | ✓ Covered |
| **AF03** | Duplicate skip | TC-12, TC-13, TC-14 | 3 | ✓ Covered |
| **AF04** | Missing parent NRIC skip | TC-05 | 1 | ✓ Covered |
| **EF02** | Required field missing skip | TC-11, TC-30 | 2 | ✓ Covered |
| **EF03** | Data conflict skip | TC-16 | 1 | ✓ Covered |
| **ASM-15** | Whitespace trimming | TC-19 | 1 | ✓ Covered |
| **D-20** | NRIC masking | TC-23 | 1 | ✓ Covered |
| **Monetary** | SGD 2-decimal precision | TC-24 | 1 | ✓ Covered |
| **i18n Guard** | Zero raw keys | TC-26 | 1 | ✓ Covered |
| **Console Health** | Zero JS errors | TC-27 | 1 | ✓ Covered |
| **Auth Guard** | Route protection | TC-28 | 1 | ✓ Covered |
| **XSS Protection** | Script injection safe | TC-29 | 1 | ✓ Covered |
| **API 500 Error** | Error handling | TC-25 | 1 | ✓ Covered |
| **Dialog Cancel** | Safe dialog close | TC-15, TC-31 | 2 | ✓ Covered |

---

## Summary

**Total Test Cases**: 32  
**Total Suites**: 6 (5 Suites + 1 E2E)  
**BR Coverage**: 5/5 (F01-BR01~BR05)  
**AC Coverage**: 9/9 (F01-AC01/03/04/05/06/07/08/09/12)  
**AF Coverage**: 4/4 (AF01~AF04)  
**EF Coverage**: 2/3 (EF02, EF03)  
**Additional Coverage**: ASM-15, D-20, Monetary, i18n, Console, Auth, XSS, Error Handling, Dialog Safety  

**All test cases fully traceable to FS-01 Business Rules, Acceptance Criteria, Alternative Flows, Exception Flows, and component_specs/f01 Atomic/Integration specifications.**
