# Sprint 1 Defect Log & Known Issues Master

> Source: `[agile] fs/raw/Test Cases + Defect sprint 1.xlsx`
> Covers known defects identified during Sprint 1 test execution across R1, R3, R8, and R9.
> Use with `@pytest.mark.xfail(strict=True, reason="<BUG-ID>: <summary>")` per Invariant 5 in `AGENTS.md`.


## Defect Inventory Matrix

| Defect ID | Module | Status | Severity | Priority | Type | Summary | Linked TCs |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| [`BUG-R1-001`](#bug-r1-001) | `R1` | **Resolved** | S1 (highest) | Medium | Functional / UI / Data / Performance / Security / Compatibility / Usability | [Module] Short problem statement    e.g. [Login] Error 500 when password contains '&' | `Related test case IDs    e.g. TC-004` |
| [`BUG-R3-001`](#bug-r3-001) | `R3` | **Open** | S2 | High | Functional | [School User] Edit and Delete on the School user management list do not work | `TC-R3-F02-001` |
| [`BUG-R3-002`](#bug-r3-002) | `R3` | **Open** | S4 (lowest) | Low | UI | [Navigation] Sidebar highlights Education Accounts instead of the current menu on Create school user and Create school | `TC-R3-F02-001, TC-R3-F01-001` |
| [`BUG-R3-003`](#bug-r3-003) | `R3` | **Open** | S1 (highest) | Critical | Functional | [Academic Level] Create academic level fails and shows a raw database exception message | `TC-R3-F03-001` |
| [`BUG-R3-004`](#bug-r3-004) | `R3` | **Open** | S2 | High | Data | [School] School type dropdown on Create school has no Primary or Secondary option | `TC-R3-F01-001, TC-R3-F01-004` |
| [`BUG-R3-005`](#bug-r3-005) | `R3` | **Open** | S3 | Medium | UI | [School] School type column shows raw translation keys for Primary, Secondary and Pre-University | `TC-R3-F01-001, TC-R3-F01-004` |
| [`BUG-001`](#bug-001) | `R8` | **Resolved** | S3 | Medium | UI | [My Profile] Mailing address card is shown twice in edit mode | `TC-023` |
| [`BUG-002`](#bug-002) | `R8` | **Open** | S2 | High | Functional | [My Profile] Mobile Number format rule is not checked (8 digits, starts with 6/8/9) | `TC-033, TC-034, TC-035, TC-036, TC-037, TC-038, TC-065` |
| [`BUG-003`](#bug-003) | `R8` | **Open** | S2 | High | Functional | [My Profile] Required field message (MSG-0001) never shows when a field is cleared | `TC-032, TC-042, TC-052, TC-057, TC-062` |
| [`BUG-004`](#bug-004) | `R8` | **Open** | S3 | Medium | Functional | [My Profile] Invalid email message text does not match MSG-0806 | `TC-043, TC-044, TC-045, TC-046` |
| [`BUG-005`](#bug-005) | `R8` | **Open** | S3 | Medium | Functional | [My Profile] Email over 150 characters is accepted | `TC-047` |
| [`BUG-006`](#bug-006) | `R8` | **Open** | S3 | Medium | Functional | [My Profile] Max length not checked for Block/Unit (20) and Street/Country (100) | `TC-050, TC-053, TC-055, TC-063` |
| [`BUG-007`](#bug-007) | `R8` | **Open** | S2 | High | Functional | [My Profile] Postal code 6-digit rule is not checked | `TC-058, TC-059, TC-060` |
| [`BUG-008`](#bug-008) | `R8` | **Open** | S3 | Medium | Functional | [My Profile] Save failure message does not match MSG-0808 | `TC-028` |
| [`BUG-009`](#bug-009) | `R8` | **Open** | S3 | Medium | Data | [My Profile] Residential address is missing the floor (#11 instead of #04-11) | `TC-020` |
| [`BUG-010`](#bug-010) | `R8` | **Open** | S4 (lowest) | Low | UI | [Home] Child card does not show the age number | `TC-016` |
| [`BUG-011`](#bug-011) | `R8` | **Open** | S3 | Medium | Functional | [My Profile] Invalid Mobile & Mailing Address info message show incorrectly | `TC-033, TC-034, TC-035, TC-036, TC-037, TC-038, TC-065` |
| [`BUG-R9-001`](#bug-r9-001) | `R9` | **Open** | S3 | Medium | UI | [SCR-01 Choose child] Child cards do not show school, level, class or outstanding invoice label | `TC-004, TC-005` |
| [`BUG-R9-002`](#bug-r9-002) | `R9` | **Open** | S1 (highest) | Critical | Security | [API & SCR-02 Access Control] Unlinked student ID returns HTTP 200 empty list instead of 403 Forbidden and UI does not show access denied message | `TC-012, TC-016` |
| [`BUG-R9-003`](#bug-r9-003) | `R9` | **Open** | S2 | High | UI | [SCR-02 Outstanding fees] Flat charge table is displayed instead of expandable invoices grouped by fee type with GST and earliest due date | `TC-019, TC-022` |
| [`BUG-R9-004`](#bug-r9-004) | `R9` | **Open** | S1 (highest) | Critical | Functional | [SCR-02 Outstanding fees] Charges in a PaymentPending or ReconciliationRequired invoice are hidden instead of shown as Pending and disabled | `TC-025, TC-034, TC-110, TC-127` |
| [`BUG-R9-005`](#bug-r9-005) | `R9` | **Open** | S3 | Medium | UI | [SCR-02 Outstanding fees] Missing sample/demo data notice on the Fees & Payments screen | `TC-027` |
| [`BUG-R9-006`](#bug-r9-006) | `R9` | **Open** | S2 | High | Functional | [SCR-02 & SCR-04 Student without EA] Missing Education Account (404) shows an error banner and blocks online payment | `TC-029, TC-038` |
| [`BUG-R9-007`](#bug-r9-007) | `R9` | **Open** | S2 | High | UI | [SCR-03 No outstanding fees] Empty state has no in-page link back to the child list | `TC-032, TC-033` |
| [`BUG-R9-008`](#bug-r9-008) | `R9` | **Open** | S2 | High | Functional | [SCR-04 Choose payment method] Closed Education Account is still selectable when wallet balance >= amount | `TC-039` |
| [`BUG-R9-009`](#bug-r9-009) | `R9` | **Open** | S1 (highest) | Critical | UI | [SCR-04 Choose payment method] Low EA balance disables Education Account radio without showing the required explanation message | `TC-041, TC-046` |
| [`BUG-R9-010`](#bug-r9-010) | `R9` | **Open** | S1 (highest) | Critical | Functional | [SCR-04 Split payment] EA portion in split payment is read-only and cannot be lowered or validated on the UI | `TC-051, TC-053, TC-057, TC-062` |
| [`BUG-R9-011`](#bug-r9-011) | `R9` | **Open** | S1 (highest) | Critical | Functional | [API Checkout Split] CheckoutRequestDto ignores onlineAmount and does not reject split requests whose parts sum to less than the invoice total | `TC-055` |
| [`BUG-R9-012`](#bug-r9-012) | `R9` | **Open** | S2 | High | UI | [SCR-05 Review and confirm] Review screen for Education Account payment does not show the remaining EA balance after payment | `TC-063` |
| [`BUG-R9-013`](#bug-r9-013) | `R9` | **Open** | S1 (highest) | Critical | Data | [Audit Log & Late Webhook] BillingPaymentService has no audit_logs table for F9 payment events and ignores late payment.succeeded webhooks after Failed | `TC-071, TC-076, TC-098, TC-167` |
| [`BUG-R9-014`](#bug-r9-014) | `R9` | **Open** | S1 (highest) | Critical | Functional | [Checkout EA & Concurrency] CreateCheckoutHandler lacks EA debit compensation/reversal on save error, timeout reconciliation, and Invoice RowVersion concurrency token | `TC-073, TC-074, TC-075, TC-166` |
| [`BUG-R9-015`](#bug-r9-015) | `R9` | **Open** | S1 (highest) | Critical | Data | [EF Core Mapping] dbo.invoices student_id and school_id are uniqueidentifier in SQL Server but mapped as string in C#, throwing HTTP 500 InvalidCastException on GetByIdAsync | `TC-078, TC-080, TC-088, TC-089, TC-096, TC-097, TC-115, TC-119, TC-120, TC-143` |
| [`BUG-R9-016`](#bug-r9-016) | `R9` | **Open** | S3 | Medium | Functional | [API Checkout Validation] Idempotency-Key of 101 characters is not rejected at input validation (returns 404 instead of 400) | `TC-081` |
| [`BUG-R9-017`](#bug-r9-017) | `R9` | **Open** | S1 (highest) | Critical | Functional | [Online Payment Failure / Cancel / Expiry] Failed, cancelled or expired online payment leaves invoice stuck in PaymentPending (3) instead of restoring to Issued (2) | `TC-090, TC-091, TC-092, TC-094, TC-139` |
| [`BUG-R9-018`](#bug-r9-018) | `R9` | **Open** | S2 | High | UI | [SCR-06 Pending & Verifying] Waiting/verifying screen for split payment does not state in prose that the Education Account part was already deducted | `TC-101, TC-128` |
| [`BUG-R9-019`](#bug-r9-019) | `R9` | **Open** | S1 (highest) | Critical | Functional | [Split Payment Failure / Cancel / Timeout] Online failure, cancellation or session failure after EA debit does not automatically reverse the EA deduction | `TC-103, TC-104, TC-105, TC-107, TC-108, TC-109` |
| [`BUG-R9-020`](#bug-r9-020) | `R9` | **Open** | S2 | High | Functional | [SCR-07 Receipt] Payment confirmation screen only offers Print receipt and has no Download PDF button or endpoint | `TC-131, TC-132` |
| [`BUG-R9-021`](#bug-r9-021) | `R9` | **Open** | S1 (highest) | Critical | UI | [SCR-08 Payment failed] Failure screen omits the failure reason, omits the EA-returned notice for refunded splits, and has no Try again button | `TC-136, TC-137, TC-140` |
| [`BUG-R9-022`](#bug-r9-022) | `R9` | **Open** | S2 | High | Security | [Error Handling UI] 5xx API errors on charge list, checkout confirm, and payment result render raw server error strings (SqlException) on screen | `TC-138, TC-144, TC-164` |
| [`BUG-R9-023`](#bug-r9-023) | `R9` | **Open** | S3 | Medium | Data | [Database Constraints] dbo.invoice_items allows attaching a student_charge from a different school_id than dbo.invoices.school_id | `TC-149` |

---

## Detailed Defect Reports

### `BUG-R1-001`: [Module] Short problem statement

- **Module**: `R1` (R1 Defect)
- **Status**: **Resolved**
- **Severity / Priority**: `S1 (highest)` / `Medium`
- **Defect Type**: `Functional / UI / Data / Performance / Security / Compatibility / Usability`
- **Linked Test Case(s)**: `Related test case IDs
 
 e.g. TC-004`
- **Environment**: Environment + browser/device + build |   |  e.g.  |  DEV  |  Chrome 129 |  Build 1.0.3
- **Evidence**: Screenshot, video or log link
 
 e.g. link to file in shared drive
- **Notes**: Root cause, workaround, assignee, fix version

**Preconditions:**
```text
State required before execution
 
 e.g. User account exists and is active
```

**Steps to Reproduce:**
- Numbered steps to trigger the defect
1. Open the login page
2. Enter password 'Abc&123'
3. Click [Login]

**Expected Result:**
> Correct behaviour per requirement
>  
>  e.g. User is logged in and redirected to Dashboard

**Actual Result:**
> What actually happened
>  
>  e.g. Error 500 page is displayed

**Pytest Strict XFAIL Directive:**
```python
@pytest.mark.xfail(strict=True, reason="BUG-R1-001: [Module] Short problem statement")
```

---

### `BUG-R3-001`: [School User] Edit and Delete on the School user management list do not work

- **Module**: `R3` (R3 Defect)
- **Status**: **Open**
- **Severity / Priority**: `S2` / `High`
- **Defect Type**: `Functional`
- **Linked Test Case(s)**: `TC-R3-F02-001`
- **Environment**: SIT |  Chrome (latest) |  Build: Sprint 1 MVP (taken from the test cases, confirm at retest) |  Admin Portal, URL not captured in the evidence
- **Evidence**: Image 1 (sheet Evidence): School user management list
- **Notes**: No test case covers editing or deleting a School User. Suggest adding one. Capture the console and network response at retest so Dev can locate the cause.

**Preconditions:**
```text
Logged in to the Admin Portal as MOE HQ User.
 At least one School User exists in the list.
```

**Steps to Reproduce:**
1. Open School user management.
2. Click Edit on a School User row.
3. Click Delete on a School User row.

**Expected Result:**
> 1. Edit opens the edit form with the current values and the changes can be saved.
>  2. Delete asks for confirmation and then removes or deactivates the School User.

**Actual Result:**
> Edit and Delete do not work: neither action completes. The detail of the failure (no form, no response or an error) was not captured in the evidence.

**Pytest Strict XFAIL Directive:**
```python
@pytest.mark.xfail(strict=True, reason="BUG-R3-001: [School User] Edit and Delete on the School user management list do not work")
```

---

### `BUG-R3-002`: [Navigation] Sidebar highlights Education Accounts instead of the current menu on Create school user and Create school

- **Module**: `R3` (R3 Defect)
- **Status**: **Open**
- **Severity / Priority**: `S4 (lowest)` / `Low`
- **Defect Type**: `UI`
- **Linked Test Case(s)**: `TC-R3-F02-001, TC-R3-F01-001`
- **Environment**: SIT |  Chrome (latest) |  Build: Sprint 1 MVP (taken from the test cases, confirm at retest) |  Admin Portal, URL not captured in the evidence
- **Evidence**: Image 2 and Image 4 (sheet Evidence)
- **Notes**: The active menu seems to be matched by route prefix, so child pages fall under Education Accounts. Check the other create and edit pages for the same behaviour.

**Preconditions:**
```text
Logged in to the Admin Portal as MOE HQ User.
```

**Steps to Reproduce:**
1. Open School user management and click Create school user.
2. Look at the highlighted item in the sidebar.
3. Open School management, click Create school and look at the sidebar again.

**Expected Result:**
> 1. On Create school user the sidebar highlights School user management.
>  2. On Create school the sidebar highlights School management only.

**Actual Result:**
> 1. On Create school user the sidebar highlights Education Accounts (Dashboard is also shaded) and School user management is not highlighted.
>  2. On Create school the sidebar highlights Education Accounts together with School management.

**Pytest Strict XFAIL Directive:**
```python
@pytest.mark.xfail(strict=True, reason="BUG-R3-002: [Navigation] Sidebar highlights Education Accounts instead of the current menu on Create school user and Create school")
```

---

### `BUG-R3-003`: [Academic Level] Create academic level fails and shows a raw database exception message

- **Module**: `R3` (R3 Defect)
- **Status**: **Open**
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Defect Type**: `Functional`
- **Linked Test Case(s)**: `TC-R3-F03-001`
- **Environment**: SIT |  Chrome (latest) |  Build: Sprint 1 MVP (taken from the test cases, confirm at retest) |  Admin Portal, URL not captured in the evidence
- **Evidence**: Image 3 (sheet Evidence)
- **Notes**: Not yet known whether the cause is the data (name, stage or display order already used) or every save fails. Retest with another value. The screen fields (Name, Education stage, Display order) differ from the TC data (level_code, level_name, sequence_order), so update the TC data at retest. Dev to read the inner exception in the server log.

**Preconditions:**
```text
Logged in to the Admin Portal as MOE HQ User.
 Academic Level screen is open.
```

**Steps to Reproduce:**
1. Click create academic level.
2. Enter Name 'Primary7', Education stage 'Primary', Display order 14.
3. Click Save.

**Expected Result:**
> The level is saved, 'Academic Level created successfully' is shown and the level appears in the list and in the class creation dropdown (TC-R3-F03-001).

**Actual Result:**
> The level is not created. The page shows: 'An error occurred while saving the entity changes. See the inner exception for details.' This is an internal framework message and should not be shown to the user.

**Pytest Strict XFAIL Directive:**
```python
@pytest.mark.xfail(strict=True, reason="BUG-R3-003: [Academic Level] Create academic level fails and shows a raw database exception message")
```

---

### `BUG-R3-004`: [School] School type dropdown on Create school has no Primary or Secondary option

- **Module**: `R3` (R3 Defect)
- **Status**: **Open**
- **Severity / Priority**: `S2` / `High`
- **Defect Type**: `Data`
- **Linked Test Case(s)**: `TC-R3-F01-001, TC-R3-F01-004`
- **Environment**: SIT |  Chrome (latest) |  Build: Sprint 1 MVP (taken from the test cases, confirm at retest) |  Admin Portal, URL not captured in the evidence
- **Notes**: Reported by the tester as missing Primary and Secondary. Confirm the full school_type enum against the R3 requirement, Pre-University may also be missing.

**Preconditions:**
```text
Logged in to the Admin Portal as MOE HQ User.
```

**Steps to Reproduce:**
1. Open School management and click Create school.
2. Enter a school code and a school name.
3. Open the School type dropdown.

**Expected Result:**
> The dropdown offers Primary and Secondary, so every school type used by the system can be selected (TC-R3-F01-004).

**Actual Result:**
> The dropdown lists only Government, Government aided, Autonomous, Independent and Specialised. Primary and Secondary are missing, although the School management list already shows schools of type PRIMARY, SECONDARY and PRE_UNIVERSITY.

**Pytest Strict XFAIL Directive:**
```python
@pytest.mark.xfail(strict=True, reason="BUG-R3-004: [School] School type dropdown on Create school has no Primary or Secondary option")
```

---

### `BUG-R3-005`: [School] School type column shows raw translation keys for Primary, Secondary and Pre-University

- **Module**: `R3` (R3 Defect)
- **Status**: **Open**
- **Severity / Priority**: `S3` / `Medium`
- **Defect Type**: `UI`
- **Linked Test Case(s)**: `TC-R3-F01-001, TC-R3-F01-004`
- **Environment**: SIT |  Chrome (latest) |  Build: Sprint 1 MVP (taken from the test cases, confirm at retest) |  Admin Portal, URL not captured in the evidence
- **Evidence**: Image 5 (sheet Evidence)
- **Notes**: Translation entries for these three types look missing. Check the other languages and the school detail and edit pages.

**Preconditions:**
```text
Logged in to the Admin Portal as MOE HQ User.
 Schools of type Primary, Secondary and Pre-University exist.
```

**Steps to Reproduce:**
1. Open School management.
2. Read the School type column.

**Expected Result:**
> Every school type is shown as a readable label, like Government and Government aided.

**Actual Result:**
> The column shows the keys features.schoolManagement.types.PRIMARY, features.schoolManagement.types.SECONDARY and features.schoolManagement.types.PRE_UNIVERSITY. Government and Government aided are shown correctly.

**Pytest Strict XFAIL Directive:**
```python
@pytest.mark.xfail(strict=True, reason="BUG-R3-005: [School] School type column shows raw translation keys for Primary, Secondary and Pre-University")
```

---

### `BUG-001`: [My Profile] Mailing address card is shown twice in edit mode

- **Module**: `R8` (R8 Defect)
- **Status**: **Resolved**
- **Severity / Priority**: `S3` / `Medium`
- **Defect Type**: `UI`
- **Linked Test Case(s)**: `TC-023`
- **Environment**: DEV (dev tunnel qjrntd59-5174) | Chromium headless (Playwright) | Windows
- **Evidence**: playwright-report (screenshot / video / trace of linked cases)
- **Notes**: ParentProfileEditForm.tsx renders ProfileCard id='mailing' twice

**Preconditions:**
```text
Parent S8411053A logged in; My Profile > [Update details]
```

**Steps to Reproduce:**
1. Open My Profile
2. Click [Update details]

**Expected Result:**
> Only one Mailing address card

**Actual Result:**
> Two identical Mailing address cards (duplicate inputs)

**Pytest Strict XFAIL Directive:**
```python
@pytest.mark.xfail(strict=True, reason="BUG-001: [My Profile] Mailing address card is shown twice in edit mode")
```

---

### `BUG-002`: [My Profile] Mobile Number format rule is not checked (8 digits, starts with 6/8/9)

- **Module**: `R8` (R8 Defect)
- **Status**: **Open**
- **Severity / Priority**: `S2` / `High`
- **Defect Type**: `Functional`
- **Linked Test Case(s)**: `TC-033, TC-034, TC-035, TC-036, TC-037, TC-038, TC-065`
- **Environment**: DEV (dev tunnel qjrntd59-5174) | Chromium headless (Playwright) | Windows
- **Evidence**: playwright-report (screenshot / video / trace of linked cases)
- **Notes**: Rule not implemented in ParentProfileEditForm.tsx

**Preconditions:**
```text
Parent S8411053A logged in; My Profile > [Update details]
```

**Steps to Reproduce:**
1. Enter 9123456 in Mobile Number
2. Click [Save changes]

**Expected Result:**
> MSG-0805 under Mobile Number; no update

**Actual Result:**
> No error; confirm dialog opens

**Pytest Strict XFAIL Directive:**
```python
@pytest.mark.xfail(strict=True, reason="BUG-002: [My Profile] Mobile Number format rule is not checked (8 digits, starts with 6/8/9)")
```

---

### `BUG-003`: [My Profile] Required field message (MSG-0001) never shows when a field is cleared

- **Module**: `R8` (R8 Defect)
- **Status**: **Open**
- **Severity / Priority**: `S2` / `High`
- **Defect Type**: `Functional`
- **Linked Test Case(s)**: `TC-032, TC-042, TC-052, TC-057, TC-062`
- **Environment**: DEV (dev tunnel qjrntd59-5174) | Chromium headless (Playwright) | Windows
- **Evidence**: playwright-report (screenshot / video / trace of linked cases)
- **Notes**: handleBlur restores saved value; getChanges skips empty values

**Preconditions:**
```text
Parent S8411053A logged in; My Profile > [Update details]
```

**Steps to Reproduce:**
1. Change Unit to 12
2. Clear Mobile Number (or Email / Street / Postal code / Country)
3. Click [Save changes]

**Expected Result:**
> MSG-0001 'Enter your <field>' under the field; no update

**Actual Result:**
> No message; blank value is ignored (on blur it goes back to the saved value)

**Pytest Strict XFAIL Directive:**
```python
@pytest.mark.xfail(strict=True, reason="BUG-003: [My Profile] Required field message (MSG-0001) never shows when a field is cleared")
```

---

### `BUG-004`: [My Profile] Invalid email message text does not match MSG-0806

- **Module**: `R8` (R8 Defect)
- **Status**: **Open**
- **Severity / Priority**: `S3` / `Medium`
- **Defect Type**: `Functional`
- **Linked Test Case(s)**: `TC-043, TC-044, TC-045, TC-046`
- **Environment**: DEV (dev tunnel qjrntd59-5174) | Chromium headless (Playwright) | Windows
- **Evidence**: playwright-report (screenshot / video / trace of linked cases)
- **Notes**: Update i18n key features.parentProfile.validation.emailInvalid

**Preconditions:**
```text
Parent S8411053A logged in; My Profile > [Update details]
```

**Steps to Reproduce:**
1. Enter parent.example.com in Email
2. Click [Save changes]

**Expected Result:**
> Enter an email address in the correct format, like name@example.com'

**Actual Result:**
> Enter a valid email address.'

**Pytest Strict XFAIL Directive:**
```python
@pytest.mark.xfail(strict=True, reason="BUG-004: [My Profile] Invalid email message text does not match MSG-0806")
```

---

### `BUG-005`: [My Profile] Email over 150 characters is accepted

- **Module**: `R8` (R8 Defect)
- **Status**: **Open**
- **Severity / Priority**: `S3` / `Medium`
- **Defect Type**: `Functional`
- **Linked Test Case(s)**: `TC-047`
- **Environment**: DEV (dev tunnel qjrntd59-5174) | Chromium headless (Playwright) | Windows
- **Evidence**: playwright-report (screenshot / video / trace of linked cases)
- **Notes**: Max length rule not implemented

**Preconditions:**
```text
Parent S8411053A logged in; My Profile > [Update details]
```

**Steps to Reproduce:**
1. Enter an email with 151 characters
2. Click [Save changes]

**Expected Result:**
> MSG-0806; no update

**Actual Result:**
> No error; confirm dialog opens

**Pytest Strict XFAIL Directive:**
```python
@pytest.mark.xfail(strict=True, reason="BUG-005: [My Profile] Email over 150 characters is accepted")
```

---

### `BUG-006`: [My Profile] Max length not checked for Block/Unit (20) and Street/Country (100)

- **Module**: `R8` (R8 Defect)
- **Status**: **Open**
- **Severity / Priority**: `S3` / `Medium`
- **Defect Type**: `Functional`
- **Linked Test Case(s)**: `TC-050, TC-053, TC-055, TC-063`
- **Environment**: DEV (dev tunnel qjrntd59-5174) | Chromium headless (Playwright) | Windows
- **Evidence**: playwright-report (screenshot / video / trace of linked cases)
- **Notes**: Messages are assumed in FS08

**Preconditions:**
```text
Parent S8411053A logged in; My Profile > [Update details]
```

**Steps to Reproduce:**
1. Enter 21 characters in Block
2. Click [Save changes]

**Expected Result:**
> Enter no more than 20 characters.' (Street/Country: 100)

**Actual Result:**
> No error; confirm dialog opens

**Pytest Strict XFAIL Directive:**
```python
@pytest.mark.xfail(strict=True, reason="BUG-006: [My Profile] Max length not checked for Block/Unit (20) and Street/Country (100)")
```

---

### `BUG-007`: [My Profile] Postal code 6-digit rule is not checked

- **Module**: `R8` (R8 Defect)
- **Status**: **Open**
- **Severity / Priority**: `S2` / `High`
- **Defect Type**: `Functional`
- **Linked Test Case(s)**: `TC-058, TC-059, TC-060`
- **Environment**: DEV (dev tunnel qjrntd59-5174) | Chromium headless (Playwright) | Windows
- **Evidence**: playwright-report (screenshot / video / trace of linked cases)
- **Notes**: Message is assumed in FS08

**Preconditions:**
```text
Parent S8411053A logged in; My Profile > [Update details]
```

**Steps to Reproduce:**
1. Enter 65001 in Postal code
2. Click [Save changes]

**Expected Result:**
> Enter a valid 6-digit postal code.'; no update

**Actual Result:**
> No error; confirm dialog opens

**Pytest Strict XFAIL Directive:**
```python
@pytest.mark.xfail(strict=True, reason="BUG-007: [My Profile] Postal code 6-digit rule is not checked")
```

---

### `BUG-008`: [My Profile] Save failure message does not match MSG-0808

- **Module**: `R8` (R8 Defect)
- **Status**: **Open**
- **Severity / Priority**: `S3` / `Medium`
- **Defect Type**: `Functional`
- **Linked Test Case(s)**: `TC-028`
- **Environment**: DEV (dev tunnel qjrntd59-5174) | Chromium headless (Playwright) | Windows
- **Evidence**: playwright-report (screenshot / video / trace of linked cases)
- **Notes**: Generic API error text is shown instead of MSG-0808

**Preconditions:**
```text
Parent S8411053A logged in; My Profile > [Update details]; update API fails (HTTP 500)
```

**Steps to Reproduce:**
1. Change Unit to 13
2. Click [Save changes]
3. Click [Save changes] in the dialog

**Expected Result:**
> We could not update your details. Please try again.' (MSG-0808)

**Actual Result:**
> A server error occurred. Please try again later.'

**Pytest Strict XFAIL Directive:**
```python
@pytest.mark.xfail(strict=True, reason="BUG-008: [My Profile] Save failure message does not match MSG-0808")
```

---

### `BUG-009`: [My Profile] Residential address is missing the floor (#11 instead of #04-11)

- **Module**: `R8` (R8 Defect)
- **Status**: **Open**
- **Severity / Priority**: `S3` / `Medium`
- **Defect Type**: `Data`
- **Linked Test Case(s)**: `TC-020`
- **Environment**: DEV (dev tunnel qjrntd59-5174) | Chromium headless (Playwright) | Windows
- **Evidence**: playwright-report (screenshot / video / trace of linked cases)
- **Notes**: Home page shows #04-11 correctly

**Preconditions:**
```text
Parent S8411053A logged in
```

**Steps to Reproduce:**
1. Open My Profile
2. Check the residential address

**Expected Result:**
> Blk 101 Clementi Avenue 3 #04-11, SINGAPORE 650013' (Singpass: floor 04, unit 11)

**Actual Result:**
> Blk 101 Clementi Avenue 3 #11, SINGAPORE 650013'

**Pytest Strict XFAIL Directive:**
```python
@pytest.mark.xfail(strict=True, reason="BUG-009: [My Profile] Residential address is missing the floor (#11 instead of #04-11)")
```

---

### `BUG-010`: [Home] Child card does not show the age number

- **Module**: `R8` (R8 Defect)
- **Status**: **Open**
- **Severity / Priority**: `S4 (lowest)` / `Low`
- **Defect Type**: `UI`
- **Linked Test Case(s)**: `TC-016`
- **Environment**: DEV (dev tunnel qjrntd59-5174) | Chromium headless (Playwright) | Windows
- **Evidence**: playwright-report (screenshot / video / trace of linked cases)
- **Notes**: en-US key educationAccounts.age has no {{age}} placeholder

**Preconditions:**
```text
Parent S8411053A logged in
```

**Steps to Reproduce:**
1. Open Home
2. Check the subtitle under a child name

**Expected Result:**
> e.g. 'S01 · Age 14'

**Actual Result:**
> S01 · Age'

**Pytest Strict XFAIL Directive:**
```python
@pytest.mark.xfail(strict=True, reason="BUG-010: [Home] Child card does not show the age number")
```

---

### `BUG-011`: [My Profile] Invalid Mobile & Mailing Address info message show incorrectly

- **Module**: `R8` (R8 Defect)
- **Status**: **Open**
- **Severity / Priority**: `S3` / `Medium`
- **Defect Type**: `Functional`
- **Linked Test Case(s)**: `TC-033, TC-034, TC-035, TC-036, TC-037, TC-038, TC-065`
- **Environment**: DEV (dev tunnel qjrntd59-5174) | Windows

**Preconditions:**
```text
Parent S8411053A logged in; My Profile > [Update details]
```

**Steps to Reproduce:**
1. Enter invalid info in Mobile and Mailing Address
2. Click [Save changes]

**Expected Result:**
> Correc message display

**Actual Result:**
> Show raw code message

**Pytest Strict XFAIL Directive:**
```python
@pytest.mark.xfail(strict=True, reason="BUG-011: [My Profile] Invalid Mobile & Mailing Address info message show incorrectly")
```

---

### `BUG-R9-001`: [SCR-01 Choose child] Child cards do not show school, level, class or outstanding invoice label

- **Module**: `R9` (R9 Defect)
- **Status**: **Open**
- **Severity / Priority**: `S3` / `Medium`
- **Defect Type**: `UI`
- **Linked Test Case(s)**: `TC-004, TC-005`
- **Environment**: SIT (Local QA Stack) | e-Service: http://localhost:5174 | API Gateway: http://localhost:5273 | Database: edufams-qa-sqlserver (SQL Server 2022) | Browser: Chrome (latest), Windows 11 | Build: QA_BE / develop (22 Oct 2026)
- **Evidence**: Image 1 (sheet Evidence)
evidence_01_BUG-R9-001.png
- **Notes**: Root cause: AccountsPage in apps/e-service only renders wallet summary fields from EducationAccountService and does not fetch or display school/level/class or billing outstanding summary.

**Preconditions:**
```text
Parent (S7890123F, Tan Ah Kow) is signed in through Singpass and has linked children with and without outstanding charges.
```

**Steps to Reproduce:**
1. Sign in to the e-Service portal as Parent S7890123F.
2. Open the Education Accounts / Choose Child screen (/accounts, SCR-01).
3. Inspect each child card for school name, level/cohort, class, and the outstanding/no-outstanding invoices indicator.

**Expected Result:**
> Each child entry on SCR-01 displays the student name, school, level (cohort), class, and a label indicating whether the child has outstanding invoices or no outstanding invoices (TC-004, TC-005).

**Actual Result:**
> Each card only displays the student name, account number (e.g., 'Account EDU-00502'), status ('Status: Active') and a 'View fees for <Child>' link. School name, level, class and the outstanding/no-outstanding label are not shown.

**Pytest Strict XFAIL Directive:**
```python
@pytest.mark.xfail(strict=True, reason="BUG-R9-001: [SCR-01 Choose child] Child cards do not show school, level, class or outstanding invoice label")
```

---

### `BUG-R9-002`: [API & SCR-02 Access Control] Unlinked student ID returns HTTP 200 empty list instead of 403 Forbidden and UI does not show access denied message

- **Module**: `R9` (R9 Defect)
- **Status**: **Open**
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Defect Type**: `Security`
- **Linked Test Case(s)**: `TC-012, TC-016`
- **Environment**: SIT (Local QA Stack) | e-Service: http://localhost:5174 | API Gateway: http://localhost:5273 | Database: edufams-qa-sqlserver (SQL Server 2022) | Browser: Chrome (latest), Windows 11 | Build: QA_BE / develop (22 Oct 2026)
- **Evidence**: Image 2 (sheet Evidence)
evidence_02_BUG-R9-002.png
- **Notes**: Root cause: StudentChargesController and GetOutstandingChargesHandler do not verify guardian-student linkage against IAM/EducationAccount before querying charges.

**Preconditions:**
```text
Parent (S7890123F) is signed in and requests outstanding charges or opens /billing/{studentId} for a student ID belonging to another family.
```

**Steps to Reproduce:**
1. Sign in as Parent S7890123F.
2. Call GET /api/billing/v1/students/00000000-0000-4000-8000-000000000001/outstanding-charges (TC-012).
3. Navigate directly to http://localhost:5174/billing/00000000-0000-4000-8000-000000000001 in the browser (TC-016).

**Expected Result:**
> 1. The API refuses the request with HTTP 403 Forbidden and writes a security log entry (TC-012).
> 2. Navigating to /billing/{unlinkedStudentId} returns 403 and displays 'You do not have access to this student's records.' without showing wallet or billing controls (TC-016).

**Actual Result:**
> 1. GET /api/billing/v1/students/{unlinkedStudentId}/outstanding-charges returns HTTP 200 OK with {"isSuccess":true,"statusCode":200,"data":[]}.
> 2. Navigating to /billing/{unlinkedStudentId} opens the billing screen with 'Outstanding fees SGD 0.00' instead of showing 'You do not have access to this student's records.'

**Pytest Strict XFAIL Directive:**
```python
@pytest.mark.xfail(strict=True, reason="BUG-R9-002: [API & SCR-02 Access Control] Unlinked student ID returns HTTP 200 empty list instead of 403 Forbidden and UI does not show access denied message")
```

---

### `BUG-R9-003`: [SCR-02 Outstanding fees] Flat charge table is displayed instead of expandable invoices grouped by fee type with GST and earliest due date

- **Module**: `R9` (R9 Defect)
- **Status**: **Open**
- **Severity / Priority**: `S2` / `High`
- **Defect Type**: `UI`
- **Linked Test Case(s)**: `TC-019, TC-022`
- **Environment**: SIT (Local QA Stack) | e-Service: http://localhost:5174 | API Gateway: http://localhost:5273 | Database: edufams-qa-sqlserver (SQL Server 2022) | Browser: Chrome (latest), Windows 11 | Build: QA_BE / develop (22 Oct 2026)
- **Evidence**: Image 3 (sheet Evidence)
evidence_03_BUG-R9-003.png
- **Notes**: Root cause: Architecture/UI mismatch (ASM-R9-UI-01): BillingPaymentPage lists pre-invoice student_charges rather than pre-issued invoices with expandable line groups.

**Preconditions:**
```text
Parent is signed in and opens SCR-02 (/billing/01999001-0000-7000-8000-000000000001) for a child with multiple outstanding fee lines.
```

**Steps to Reproduce:**
1. Open /billing/01999001-0000-7000-8000-000000000001 (SCR-02).
2. Inspect the list of outstanding items for invoice numbers (INV-YYYY-NNNNNN), earliest due date across lines, expandable fee-type groups (Tuition, School, Miscellaneous), and GST breakdown.

**Expected Result:**
> 1. Open invoices are listed with their invoice number and the earliest due date of their lines (TC-022).
> 2. Opening an invoice shows its lines grouped by fee type with fee components and GST (TC-019).

**Actual Result:**
> SCR-02 renders a flat table of individual student_charges rows (Charge description, Gross, Subsidy, Net, Due date). Invoices are only created at checkout, so no INV-YYYY-NNNNNN header, earliest due date aggregation, fee-type grouping, or GST breakdown is shown on SCR-02.

**Pytest Strict XFAIL Directive:**
```python
@pytest.mark.xfail(strict=True, reason="BUG-R9-003: [SCR-02 Outstanding fees] Flat charge table is displayed instead of expandable invoices grouped by fee type with GST and earliest due date")
```

---

### `BUG-R9-004`: [SCR-02 Outstanding fees] Charges in a PaymentPending or ReconciliationRequired invoice are hidden instead of shown as Pending and disabled

- **Module**: `R9` (R9 Defect)
- **Status**: **Open**
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Defect Type**: `Functional`
- **Linked Test Case(s)**: `TC-025, TC-034, TC-110, TC-127`
- **Environment**: SIT (Local QA Stack) | e-Service: http://localhost:5174 | API Gateway: http://localhost:5273 | Database: edufams-qa-sqlserver (SQL Server 2022) | Browser: Chrome (latest), Windows 11 | Build: QA_BE / develop (22 Oct 2026)
- **Evidence**: Image 4 (sheet Evidence)
evidence_04_BUG-R9-004.png
- **Notes**: Root cause: GetOutstandingChargesHandler.cs excludes charges joined to non-cancelled invoices instead of returning them with a Pending status flag for BillingPaymentPage to display as disabled.

**Preconditions:**
```text
A student has an open charge that is currently inside a PaymentPending (status = 3) or ReconciliationRequired (status = 5) invoice/transaction.
```

**Steps to Reproduce:**
1. Start an OnlineGateway checkout for a charge (or set a split payment to ReconciliationRequired) so the invoice is PaymentPending (status = 3).
2. Return to SCR-02 (/billing/{studentId}) and inspect the list of items (TC-025, TC-110, TC-127).
3. Repeat for a child whose only open invoice is in PaymentPending (TC-034).

**Expected Result:**
> 1. The invoice/item waiting for payment is shown on SCR-02 with status 'Pending' (or 'Verifying') and its selection checkbox is disabled so a second payment cannot be started from the UI (TC-025, TC-110, TC-127).
> 2. A child whose only open invoice is waiting for payment sees that Pending item on SCR-02 and is NOT shown the SCR-03 empty state (TC-034).

**Actual Result:**
> GetOutstandingChargesHandler filters out any student_charge already linked to a PaymentPending invoice. As a result, the Pending item disappears completely from SCR-02 (TC-025, TC-110, TC-127), and a child whose only open item is PaymentPending is shown the 'No outstanding charges' empty state SCR-03 (TC-034).

**Pytest Strict XFAIL Directive:**
```python
@pytest.mark.xfail(strict=True, reason="BUG-R9-004: [SCR-02 Outstanding fees] Charges in a PaymentPending or ReconciliationRequired invoice are hidden instead of shown as Pending and disabled")
```

---

### `BUG-R9-005`: [SCR-02 Outstanding fees] Missing sample/demo data notice on the Fees & Payments screen

- **Module**: `R9` (R9 Defect)
- **Status**: **Open**
- **Severity / Priority**: `S3` / `Medium`
- **Defect Type**: `UI`
- **Linked Test Case(s)**: `TC-027`
- **Environment**: SIT (Local QA Stack) | e-Service: http://localhost:5174 | API Gateway: http://localhost:5273 | Database: edufams-qa-sqlserver (SQL Server 2022) | Browser: Chrome (latest), Windows 11 | Build: QA_BE / develop (22 Oct 2026)
- **Evidence**: Image 5 (sheet Evidence)
evidence_05_BUG-R9-005.png
- **Notes**: Root cause: BillingPaymentPage.tsx does not include a sample/demo data disclaimer banner.

**Preconditions:**
```text
Parent is signed in and opens SCR-02 (/billing/{studentId}) in the prototype/SIT environment.
```

**Steps to Reproduce:**
1. Open /billing/01999001-0000-7000-8000-000000000001 (SCR-02).
2. Check the page header, banner, and table footer for a notice stating that the fee and balance figures are sample/demo data.

**Expected Result:**
> SCR-02 displays a visible notice labelling the fee and Education Account figures as sample/demo data (TC-027).

**Actual Result:**
> No sample data, demo data, or prototype notice appears anywhere on SCR-02.

**Pytest Strict XFAIL Directive:**
```python
@pytest.mark.xfail(strict=True, reason="BUG-R9-005: [SCR-02 Outstanding fees] Missing sample/demo data notice on the Fees & Payments screen")
```

---

### `BUG-R9-006`: [SCR-02 & SCR-04 Student without EA] Missing Education Account (404) shows an error banner and blocks online payment

- **Module**: `R9` (R9 Defect)
- **Status**: **Open**
- **Severity / Priority**: `S2` / `High`
- **Defect Type**: `Functional`
- **Linked Test Case(s)**: `TC-029, TC-038`
- **Environment**: SIT (Local QA Stack) | e-Service: http://localhost:5174 | API Gateway: http://localhost:5273 | Database: edufams-qa-sqlserver (SQL Server 2022) | Browser: Chrome (latest), Windows 11 | Build: QA_BE / develop (22 Oct 2026)
- **Evidence**: Image 6 (sheet Evidence)
evidence_06_BUG-R9-006.png
- **Notes**: Root cause: BillingPaymentPage fails the whole page load when the wallet query returns 404 instead of treating 404 as 'no Education Account' with OnlineGateway-only eligibility.

**Preconditions:**
```text
A linked student (e.g., non-citizen or pre-activation student) has outstanding charges in BillingPaymentService but no wallet record in EducationAccountDatabase (wallet API returns 404).
```

**Steps to Reproduce:**
1. Open SCR-02 (/billing/{studentId}) for a student without an Education Account.
2. Observe the balance area and attempt to select a charge and proceed to SCR-04 to pay via Online Gateway.

**Expected Result:**
> 1. SCR-02 shows no EA balance and displays a clear note that the student does not have an Education Account (TC-029).
> 2. The Parent can still select outstanding charges and pay via Online Gateway only on SCR-04 (TC-038).

**Actual Result:**
> When GET /api/v1/accounts/by-student/{studentId} returns HTTP 404, BillingPaymentPage treats it as a fatal load failure, displaying 'Unable to load education account' and hiding the entire charges table and payment flow.

**Pytest Strict XFAIL Directive:**
```python
@pytest.mark.xfail(strict=True, reason="BUG-R9-006: [SCR-02 & SCR-04 Student without EA] Missing Education Account (404) shows an error banner and blocks online payment")
```

---

### `BUG-R9-007`: [SCR-03 No outstanding fees] Empty state has no in-page link back to the child list

- **Module**: `R9` (R9 Defect)
- **Status**: **Open**
- **Severity / Priority**: `S2` / `High`
- **Defect Type**: `UI`
- **Linked Test Case(s)**: `TC-032, TC-033`
- **Environment**: SIT (Local QA Stack) | e-Service: http://localhost:5174 | API Gateway: http://localhost:5273 | Database: edufams-qa-sqlserver (SQL Server 2022) | Browser: Chrome (latest), Windows 11 | Build: QA_BE / develop (22 Oct 2026)
- **Evidence**: Image 7 (sheet Evidence)
evidence_07_BUG-R9-007.png
- **Notes**: Root cause: Empty state block in BillingPaymentPage.tsx omits a 'Back to child list' / 'Choose another child' link.

**Preconditions:**
```text
Parent is signed in and opens /billing/01a15be4-1120-7768-a885-cef71d2a0b8a for Tan Wei Ming (a child with 0 outstanding charges).
```

**Steps to Reproduce:**
1. Open /billing/01a15be4-1120-7768-a885-cef71d2a0b8a (SCR-03).
2. Look inside the main empty-state card ('No outstanding charges') for a button or link to return to the child list (SCR-01).

**Expected Result:**
> SCR-03 displays the empty state and provides an in-page link/button back to the child list so the Parent can choose another child (TC-032, TC-033).

**Actual Result:**
> The empty state only renders the text 'No outstanding charges — This student currently has no outstanding education charges to pay.' There is no link or button inside <main> to return to the child list.

**Pytest Strict XFAIL Directive:**
```python
@pytest.mark.xfail(strict=True, reason="BUG-R9-007: [SCR-03 No outstanding fees] Empty state has no in-page link back to the child list")
```

---

### `BUG-R9-008`: [SCR-04 Choose payment method] Closed Education Account is still selectable when wallet balance >= amount

- **Module**: `R9` (R9 Defect)
- **Status**: **Open**
- **Severity / Priority**: `S2` / `High`
- **Defect Type**: `Functional`
- **Linked Test Case(s)**: `TC-039`
- **Environment**: SIT (Local QA Stack) | e-Service: http://localhost:5174 | API Gateway: http://localhost:5273 | Database: edufams-qa-sqlserver (SQL Server 2022) | Browser: Chrome (latest), Windows 11 | Build: QA_BE / develop (22 Oct 2026)
- **Evidence**: Image 8 (sheet Evidence)
evidence_08_BUG-R9-008.png
- **Notes**: Root cause: Frontend eligibility helper canUseEducationAccount checks balance >= amount without checking account status == 'Active'.

**Preconditions:**
```text
A student has an Education Account with status = 'Closed' and balance = SGD 300.00, and an outstanding charge of SGD 75.00.
```

**Steps to Reproduce:**
1. Open SCR-02 for the student with a Closed EA wallet.
2. Select the SGD 75.00 charge and click Continue to open SCR-04 (Choose payment method).
3. Inspect the Education Account radio option.

**Expected Result:**
> Because the Education Account is Closed, the Education Account and Split (Both) options are disabled/unavailable, and only Online Gateway can be selected (TC-039).

**Actual Result:**
> The Education Account radio button is enabled and checked by default because canUseEducationAccount in BillingPaymentPage only compares wallet.balance >= selectedTotal and ignores wallet.status !== 'Active'.

**Pytest Strict XFAIL Directive:**
```python
@pytest.mark.xfail(strict=True, reason="BUG-R9-008: [SCR-04 Choose payment method] Closed Education Account is still selectable when wallet balance >= amount")
```

---

### `BUG-R9-009`: [SCR-04 Choose payment method] Low EA balance disables Education Account radio without showing the required explanation message

- **Module**: `R9` (R9 Defect)
- **Status**: **Open**
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Defect Type**: `UI`
- **Linked Test Case(s)**: `TC-041, TC-046`
- **Environment**: SIT (Local QA Stack) | e-Service: http://localhost:5174 | API Gateway: http://localhost:5273 | Database: edufams-qa-sqlserver (SQL Server 2022) | Browser: Chrome (latest), Windows 11 | Build: QA_BE / develop (22 Oct 2026)
- **Evidence**: Image 9 (sheet Evidence)
evidence_09_BUG-R9-009.png
- **Notes**: Root cause: BillingPaymentPage disables the EducationAccount radio when balance < totalSelectedNet but does not render the low-balance explanation copy from FS 5.1.

**Preconditions:**
```text
Parent selects charges totalling SGD 470.00 for Test Child Three whose active EA balance is SGD 300.00 (0 < balance < amount to pay).
```

**Steps to Reproduce:**
1. Open /billing/01999001-0000-7000-8000-000000000003 (Test Child Three, EA balance SGD 300.00).
2. Select all charges (SGD 470.00) and click Continue to SCR-04.
3. Inspect the disabled Education Account option for the explanation message.

**Expected Result:**
> Education Account is disabled and the screen displays the reason explaining that the Education Account balance is not enough for this amount and suggesting paying the rest online via split payment (TC-041, TC-046).

**Actual Result:**
> The Education Account radio option is disabled and Both is selected, but no message explains why Education Account is disabled.

**Pytest Strict XFAIL Directive:**
```python
@pytest.mark.xfail(strict=True, reason="BUG-R9-009: [SCR-04 Choose payment method] Low EA balance disables Education Account radio without showing the required explanation message")
```

---

### `BUG-R9-010`: [SCR-04 Split payment] EA portion in split payment is read-only and cannot be lowered or validated on the UI

- **Module**: `R9` (R9 Defect)
- **Status**: **Open**
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Defect Type**: `Functional`
- **Linked Test Case(s)**: `TC-051, TC-053, TC-057, TC-062`
- **Environment**: SIT (Local QA Stack) | e-Service: http://localhost:5174 | API Gateway: http://localhost:5273 | Database: edufams-qa-sqlserver (SQL Server 2022) | Browser: Chrome (latest), Windows 11 | Build: QA_BE / develop (22 Oct 2026)
- **Evidence**: Image 10 (sheet Evidence)
evidence_10_BUG-R9-010.png
- **Notes**: Root cause: Frontend implements split payment as read-only full-balance deduction (i18n 'split.readOnlyDescription') even though backend CheckoutPlanner accepts custom eaAmount.

**Preconditions:**
```text
Parent is on SCR-04 with 'Both (Education Account + Online Gateway)' selected for a charge where 0 < EA balance < total amount.
```

**Steps to Reproduce:**
1. On SCR-04, select 'Both (Education Account + Online Gateway)'.
2. Attempt to edit the Education Account portion (e.g., lower it from 300.00 to 100.00 or 0.01, or test invalid inputs 0.00 and > balance).

**Expected Result:**
> 1. The Parent can lower the EA part (down to 0.01) and the online part updates automatically so both parts add up to the total (TC-051, TC-062).
> 2. Entering 0.00 or an amount above the available balance is refused on SCR-04 with the corresponding validation message (TC-053, TC-057).

**Actual Result:**
> The Payment split box renders static read-only text ('Use the full available balance from the Education Account first, then pay the remainder online. Education Account SGD 300.00 / Online Gateway SGD 170.00') with no input control.

**Pytest Strict XFAIL Directive:**
```python
@pytest.mark.xfail(strict=True, reason="BUG-R9-010: [SCR-04 Split payment] EA portion in split payment is read-only and cannot be lowered or validated on the UI")
```

---

### `BUG-R9-011`: [API Checkout Split] CheckoutRequestDto ignores onlineAmount and does not reject split requests whose parts sum to less than the invoice total

- **Module**: `R9` (R9 Defect)
- **Status**: **Open**
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Defect Type**: `Functional`
- **Linked Test Case(s)**: `TC-055`
- **Environment**: SIT (Local QA Stack) | e-Service: http://localhost:5174 | API Gateway: http://localhost:5273 | Database: edufams-qa-sqlserver (SQL Server 2022) | Browser: Chrome (latest), Windows 11 | Build: QA_BE / develop (22 Oct 2026)
- **Evidence**: Image 11 (sheet Evidence)
evidence_11_BUG-R9-011.png
- **Notes**: Root cause: CheckoutRequestDto has no OnlineAmount property; CheckoutPlanner only validates EaAmount and derives the online leg as Total - EaAmount.

**Preconditions:**
```text
An outstanding charge of SGD 250.00 exists for a student with an active EA balance of SGD 180.00.
```

**Steps to Reproduce:**
1. Send POST /api/billing/v1/checkout with paymentMethod = 'Both', eaAmount = 100.00, and onlineAmount = 100.00 (sum = 200.00 < 250.00).
2. Inspect the HTTP status code and response payload.

**Expected Result:**
> The API refuses the request with HTTP 400 Bad Request (SPLIT_AMOUNT_INVALID) because the two parts (100.00 + 100.00 = 200.00) do not add up to the 250.00 amount to pay, and no transaction is created (TC-055).

**Actual Result:**
> The API returns HTTP 200 OK and creates a transaction with EA leg = 100.00 and Online leg = 150.00 because CheckoutRequestDto ignores onlineAmount and silently calculates onlineAmount = total - eaAmount.

**Pytest Strict XFAIL Directive:**
```python
@pytest.mark.xfail(strict=True, reason="BUG-R9-011: [API Checkout Split] CheckoutRequestDto ignores onlineAmount and does not reject split requests whose parts sum to less than the invoice total")
```

---

### `BUG-R9-012`: [SCR-05 Review and confirm] Review screen for Education Account payment does not show the remaining EA balance after payment

- **Module**: `R9` (R9 Defect)
- **Status**: **Open**
- **Severity / Priority**: `S2` / `High`
- **Defect Type**: `UI`
- **Linked Test Case(s)**: `TC-063`
- **Environment**: SIT (Local QA Stack) | e-Service: http://localhost:5174 | API Gateway: http://localhost:5273 | Database: edufams-qa-sqlserver (SQL Server 2022) | Browser: Chrome (latest), Windows 11 | Build: QA_BE / develop (22 Oct 2026)
- **Evidence**: Image 12 (sheet Evidence)
evidence_12_BUG-R9-012.png
- **Notes**: Root cause: Review step in BillingPaymentPage.tsx does not render (wallet.balance - eaAmount) as 'Balance after payment'.

**Preconditions:**
```text
Parent selects an outstanding charge on SCR-02, chooses Education Account on SCR-04, and continues to SCR-05 (Check your payment details).
```

**Steps to Reproduce:**
1. Open /billing/01999001-0000-7000-8000-000000000001.
2. Select a charge (e.g., SGD 75.00), keep Education Account selected on Step 2, and click Continue to Step 3 (SCR-05).
3. Check the review summary for the remaining Education Account balance after payment.

**Expected Result:**
> SCR-05 shows the child name, invoice/charge details, amount to pay, payment method, and the projected Education Account balance after payment (TC-063).

**Actual Result:**
> Step 3 ('Check your payment details') shows 'Education Account SGD 75.00', 'Online Gateway SGD 0.00', and the 'Authorize & pay' button, but does not display the remaining EA balance after payment.

**Pytest Strict XFAIL Directive:**
```python
@pytest.mark.xfail(strict=True, reason="BUG-R9-012: [SCR-05 Review and confirm] Review screen for Education Account payment does not show the remaining EA balance after payment")
```

---

### `BUG-R9-013`: [Audit Log & Late Webhook] BillingPaymentService has no audit_logs table for F9 payment events and ignores late payment.succeeded webhooks after Failed

- **Module**: `R9` (R9 Defect)
- **Status**: **Open**
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Defect Type**: `Data`
- **Linked Test Case(s)**: `TC-071, TC-076, TC-098, TC-167`
- **Environment**: SIT (Local QA Stack) | e-Service: http://localhost:5174 | API Gateway: http://localhost:5273 | Database: edufams-qa-sqlserver (SQL Server 2022) | Browser: Chrome (latest), Windows 11 | Build: QA_BE / develop (22 Oct 2026)
- **Evidence**: Image 13 (sheet Evidence)
evidence_13_BUG-R9-013.png
- **Notes**: Root cause: Audit logging is not implemented in BillingPaymentService, and ProcessGatewayWebhookHandler exits early with WebhookReceiptStatus.Ignored whenever transaction.Status != Pending.

**Preconditions:**
```text
EA payment, Split payment, or OnlineGateway webhook settlement is executed on BillingPaymentService.
```

**Steps to Reproduce:**
1. Execute an EA payment or Split payment and query BillingPaymentService for audit log records of F9_PAYMENT_INITIATED, F9_PAYMENT_COMPLETED, and EA reversals (TC-071, TC-076, TC-098, TC-167).
2. On a failed OnlineGateway transaction (status = 3 Failed), send a late 'payment.succeeded' webhook with a new eventId and inspect the transaction status.

**Expected Result:**
> 1. Every payment initiation, leg transition, completion, and EA reversal is written to the audit log in chronological order.
> 2. A late 'payment.succeeded' webhook arriving after a transaction was already marked Failed transitions the transaction to ReconciliationRequired (status = 5) and writes an alert/audit entry.

**Actual Result:**
> 1. BillingPaymentService database has 0 audit log tables (SELECT COUNT(*) FROM sys.tables WHERE name LIKE '%audit%' returns 0) and writes no audit log entries.
> 2. ProcessGatewayWebhookHandler marks a late 'payment.succeeded' webhook on a Failed transaction as Ignored (receipt status = 3) and leaves transaction.status = 3 (Failed) instead of 5 (ReconciliationRequired).

**Pytest Strict XFAIL Directive:**
```python
@pytest.mark.xfail(strict=True, reason="BUG-R9-013: [Audit Log & Late Webhook] BillingPaymentService has no audit_logs table for F9 payment events and ignores late payment.succeeded webhooks after Failed")
```

---

### `BUG-R9-014`: [Checkout EA & Concurrency] CreateCheckoutHandler lacks EA debit compensation/reversal on save error, timeout reconciliation, and Invoice RowVersion concurrency token

- **Module**: `R9` (R9 Defect)
- **Status**: **Open**
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Defect Type**: `Functional`
- **Linked Test Case(s)**: `TC-073, TC-074, TC-075, TC-166`
- **Environment**: SIT (Local QA Stack) | e-Service: http://localhost:5174 | API Gateway: http://localhost:5273 | Database: edufams-qa-sqlserver (SQL Server 2022) | Browser: Chrome (latest), Windows 11 | Build: QA_BE / develop (22 Oct 2026)
- **Evidence**: Image 14 (sheet Evidence)
evidence_14_BUG-R9-014.png
- **Notes**: Root cause: CreateCheckoutHandler was implemented as happy-path only without compensating CreditAsync calls, and RowVersion concurrency was commented out in InvoiceModelCreating.cs.

**Preconditions:**
```text
Parent confirms an EA or Split payment in BillingPaymentService.
```

**Steps to Reproduce:**
1. Inspect CreateCheckoutHandler.cs handling when EducationAccountClient.DebitAsync returns an unclear/timeout error or when saving the invoice/transaction to SQL Server fails after DebitAsync succeeded (TC-073, TC-074, TC-075).
2. Inspect InvoiceModelCreating.cs for optimistic concurrency protection on dbo.invoices.row_version (TC-166).

**Expected Result:**
> 1. On unclear EA debit outcome, BillingPaymentService queries Function 1 with the same FundingReference, reverses the debit via CreditAsync if needed, or moves the payment to ReconciliationRequired if reversal fails, showing a safe user message (TC-073, TC-074, TC-075).
> 2. dbo.invoices.row_version is configured as an EF Core concurrency token so concurrent modifications trigger compensation (TC-166).

**Actual Result:**
> 1. CreateCheckoutHandler.cs states 'Happy-path only — no reverse/compensation', propagates raw EA client error messages, and has no compensation block calling CreditAsync if DB persistence fails after wallet debit.
> 2. In InvoiceModelCreating.cs (line 61), '// b.Property(i => i.RowVersion).IsRowVersion();' is commented out.

**Pytest Strict XFAIL Directive:**
```python
@pytest.mark.xfail(strict=True, reason="BUG-R9-014: [Checkout EA & Concurrency] CreateCheckoutHandler lacks EA debit compensation/reversal on save error, timeout reconciliation, and Invoice RowVersion concurrency token")
```

---

### `BUG-R9-015`: [EF Core Mapping] dbo.invoices student_id and school_id are uniqueidentifier in SQL Server but mapped as string in C#, throwing HTTP 500 InvalidCastException on GetByIdAsync

- **Module**: `R9` (R9 Defect)
- **Status**: **Open**
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Defect Type**: `Data`
- **Linked Test Case(s)**: `TC-078, TC-080, TC-088, TC-089, TC-096, TC-097, TC-115, TC-119, TC-120, TC-143`
- **Environment**: SIT (Local QA Stack) | e-Service: http://localhost:5174 | API Gateway: http://localhost:5273 | Database: edufams-qa-sqlserver (SQL Server 2022) | Browser: Chrome (latest), Windows 11 | Build: QA_BE / develop (22 Oct 2026)
- **Evidence**: Image 15 (sheet Evidence)
evidence_15_BUG-R9-015.png
- **Notes**: Root cause: In SQL Server (BillingPaymentService.dbo.invoices), student_id and school_id are uniqueidentifier (Guid), but Invoice.cs and InvoiceModelCreating.cs map StudentId and SchoolId as string (varchar(50)). Fix: add a HasConversion<Guid>() value converter or align the column/property types.

**Preconditions:**
```text
An invoice row exists in BillingPaymentService.dbo.invoices (created by POST /api/billing/v1/checkout).
```

**Steps to Reproduce:**
1. Create an OnlineGateway or Split (Both) checkout via POST /api/billing/v1/checkout.
2. Send a valid signed 'payment.succeeded' webhook to POST /billing/v1/webhooks/payment-gateway (TC-088, TC-089, TC-096, TC-097, TC-115, TC-119, TC-120, TC-143).
3. Or resend POST /api/billing/v1/checkout with the exact same Idempotency-Key (up to 100 chars) to replay the first result (TC-078, TC-080).

**Expected Result:**
> 1. On 'payment.succeeded' webhook, SettleSucceededAsync loads the invoice via _invoiceRepo.GetByIdAsync, marks the online leg and transaction Succeeded, marks the invoice Paid (4), and returns HTTP 200 OK.
> 2. On idempotent checkout replay with the same Idempotency-Key, CreateCheckoutHandler loads the existing invoice and returns HTTP 200 OK with the original transaction details.

**Actual Result:**
> Both flows fail with HTTP 500 Internal Server Error: {"isSuccess":false,"statusCode":500,"message":"Unable to cast object of type 'System.Guid' to type 'System.String'."}. Because SettleSucceededAsync throws before committing, no online or split payment can transition to Succeeded/Paid via webhook.

**Pytest Strict XFAIL Directive:**
```python
@pytest.mark.xfail(strict=True, reason="BUG-R9-015: [EF Core Mapping] dbo.invoices student_id and school_id are uniqueidentifier in SQL Server but mapped as string in C#, throwing HTTP 500 InvalidCastException on GetByIdAsync")
```

---

### `BUG-R9-016`: [API Checkout Validation] Idempotency-Key of 101 characters is not rejected at input validation (returns 404 instead of 400)

- **Module**: `R9` (R9 Defect)
- **Status**: **Open**
- **Severity / Priority**: `S3` / `Medium`
- **Defect Type**: `Functional`
- **Linked Test Case(s)**: `TC-081`
- **Environment**: SIT (Local QA Stack) | e-Service: http://localhost:5174 | API Gateway: http://localhost:5273 | Database: edufams-qa-sqlserver (SQL Server 2022) | Browser: Chrome (latest), Windows 11 | Build: QA_BE / develop (22 Oct 2026)
- **Evidence**: Image 16 (sheet Evidence)
evidence_16_BUG-R9-016.png
- **Notes**: Root cause: CheckoutPlanner.ValidateShape only checks string.IsNullOrWhiteSpace(request.IdempotencyKey) and omits request.IdempotencyKey.Trim().Length > 100.

**Preconditions:**
```text
Parent is authenticated and sends a checkout request to POST /api/billing/v1/checkout.
```

**Steps to Reproduce:**
1. Send POST /api/billing/v1/checkout with idempotencyKey set to a 101-character string ('k' * 101).
2. Observe the HTTP response status code.

**Expected Result:**
> The request is rejected immediately at input validation with HTTP 400 Bad Request because Idempotency-Key exceeds the 100-character maximum (TC-081).

**Actual Result:**
> CheckoutPlanner.ValidateShape does not check IdempotencyKey.Length > 100, so execution proceeds to charge lookup and returns HTTP 404 Not Found ('Charge(s) not found or not outstanding').

**Pytest Strict XFAIL Directive:**
```python
@pytest.mark.xfail(strict=True, reason="BUG-R9-016: [API Checkout Validation] Idempotency-Key of 101 characters is not rejected at input validation (returns 404 instead of 400)")
```

---

### `BUG-R9-017`: [Online Payment Failure / Cancel / Expiry] Failed, cancelled or expired online payment leaves invoice stuck in PaymentPending (3) instead of restoring to Issued (2)

- **Module**: `R9` (R9 Defect)
- **Status**: **Open**
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Defect Type**: `Functional`
- **Linked Test Case(s)**: `TC-090, TC-091, TC-092, TC-094, TC-139`
- **Environment**: SIT (Local QA Stack) | e-Service: http://localhost:5174 | API Gateway: http://localhost:5273 | Database: edufams-qa-sqlserver (SQL Server 2022) | Browser: Chrome (latest), Windows 11 | Build: QA_BE / develop (22 Oct 2026)
- **Evidence**: Image 17 (sheet Evidence)
evidence_17_BUG-R9-017.png
- **Notes**: Root cause: ProcessGatewayWebhookHandler.SettleFailed does not update invoice.Status back to Issued (2) or release invoice_items, and ProcessGatewayWebhookHandler only handles 'payment.succeeded' and 'payment.failed'.

**Preconditions:**
```text
An OnlineGateway payment has been initiated (invoice.status = 3 PaymentPending, transaction.status = 1 Pending).
```

**Steps to Reproduce:**
1. Send a signed 'payment.failed' webhook to POST /billing/v1/webhooks/payment-gateway and inspect dbo.invoices.status and dbo.invoice_items (TC-090, TC-139).
2. Send a signed 'payment.cancelled' (TC-091) or 'payment.expired' (TC-092) webhook and inspect dbo.webhook_receipts, dbo.payment_transactions, and dbo.invoices.
3. Inspect CreateCheckoutHandler when gateway session creation fails on an OnlineGateway checkout (TC-094).

**Expected Result:**
> 1. On 'payment.failed' or 'payment.expired', the online leg and transaction become Failed (3), the invoice returns to Issued (2), and the charge can be selected again on SCR-02 (TC-090, TC-092, TC-139).
> 2. On 'payment.cancelled', the online leg and transaction become Cancelled (4) and the invoice returns to Issued (2) (TC-091).
> 3. When provider session creation fails during checkout, the invoice is not left in PaymentPending (TC-094).

**Actual Result:**
> 1. On 'payment.failed', SettleFailed sets transaction.status = 3 (Failed) but leaves dbo.invoices.status = 3 (PaymentPending) and keeps dbo.invoice_items attached, permanently locking the charge from SCR-02.
> 2. On 'payment.cancelled' and 'payment.expired', ProcessGatewayWebhookHandler marks the webhook receipt as Ignored (status = 3) and leaves transaction = 1 (Pending) and invoice = 3 (PaymentPending).
> 3. When gateway session creation fails in CreateCheckoutHandler, invoice.Status remains PaymentPending (3).

**Pytest Strict XFAIL Directive:**
```python
@pytest.mark.xfail(strict=True, reason="BUG-R9-017: [Online Payment Failure / Cancel / Expiry] Failed, cancelled or expired online payment leaves invoice stuck in PaymentPending (3) instead of restoring to Issued (2)")
```

---

### `BUG-R9-018`: [SCR-06 Pending & Verifying] Waiting/verifying screen for split payment does not state in prose that the Education Account part was already deducted

- **Module**: `R9` (R9 Defect)
- **Status**: **Open**
- **Severity / Priority**: `S2` / `High`
- **Defect Type**: `UI`
- **Linked Test Case(s)**: `TC-101, TC-128`
- **Environment**: SIT (Local QA Stack) | e-Service: http://localhost:5174 | API Gateway: http://localhost:5273 | Database: edufams-qa-sqlserver (SQL Server 2022) | Browser: Chrome (latest), Windows 11 | Build: QA_BE / develop (22 Oct 2026)
- **Evidence**: Image 18 (sheet Evidence)
evidence_18_BUG-R9-018.png
- **Notes**: Root cause: PaymentResultPage.tsx uses the same generic pending banner for single and split payments, and only shows the EA-deducted note in ReconciliationRequired when eaLeg.status === 'Succeeded'.

**Preconditions:**
```text
A Split payment (Both: EA SGD 20.00 + Online SGD 30.00) is in Pending status (TC-101) or ReconciliationRequired verifying status (TC-128) on /payment-result (SCR-06).
```

**Steps to Reproduce:**
1. Open /payment-result?transactionId={txId} for a Pending split payment where the EA leg (SGD 20.00) is Succeeded and the Online leg (SGD 30.00) is Pending (TC-101).
2. Open /payment-result?transactionId={txId} for a ReconciliationRequired split payment where the EA leg is also in ReconciliationRequired (TC-128).
3. Read the status banner message.

**Expected Result:**
> 1. While pending, SCR-06 states in prose that the Education Account portion (SGD 20.00) has already been taken/deducted while the online part is being confirmed (TC-101).
> 2. While verifying (ReconciliationRequired), SCR-06 states the Education Account portion that was taken and offers no retry (TC-128).

**Actual Result:**
> 1. For Pending split, SCR-06 only displays generic text 'Your payment is still being confirmed. This page will update automatically.' without mentioning that the EA part was already deducted.
> 2. For ReconciliationRequired split when EA leg is ReconciliationRequired, SCR-06 only displays 'We are reviewing this payment. Please contact support if the status does not change.' without naming the EA part taken.

**Pytest Strict XFAIL Directive:**
```python
@pytest.mark.xfail(strict=True, reason="BUG-R9-018: [SCR-06 Pending & Verifying] Waiting/verifying screen for split payment does not state in prose that the Education Account part was already deducted")
```

---

### `BUG-R9-019`: [Split Payment Failure / Cancel / Timeout] Online failure, cancellation or session failure after EA debit does not automatically reverse the EA deduction

- **Module**: `R9` (R9 Defect)
- **Status**: **Open**
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Defect Type**: `Functional`
- **Linked Test Case(s)**: `TC-103, TC-104, TC-105, TC-107, TC-108, TC-109`
- **Environment**: SIT (Local QA Stack) | e-Service: http://localhost:5174 | API Gateway: http://localhost:5273 | Database: edufams-qa-sqlserver (SQL Server 2022) | Browser: Chrome (latest), Windows 11 | Build: QA_BE / develop (22 Oct 2026)
- **Evidence**: Image 19 (sheet Evidence)
evidence_19_BUG-R9-019.png
- **Notes**: Root cause: SettleFailed in ProcessGatewayWebhookHandler.cs and the fallback branch in CreateCheckoutHandler.cs do not invoke _eaClient.CreditAsync to refund the EA wallet on split payment failure.

**Preconditions:**
```text
A Split payment (Both) has debited the student's Education Account wallet (EA leg = 2 Succeeded) and created an OnlineGateway leg (status = 1 Pending).
```

**Steps to Reproduce:**
1. Trigger an online failure via 'payment.failed' webhook (TC-103, TC-108, TC-109) or parent cancellation via 'payment.cancelled' webhook (TC-104) on a Split transaction.
2. Query BillingPaymentService (payment_transactions, payment_funding_legs) and EducationAccountDatabase (wallets).
3. Inspect CreateCheckoutHandler.cs when online session creation fails after EA debit (TC-105) or when online session times out (TC-107).

**Expected Result:**
> When the online leg of a Split payment fails, is cancelled, fails session creation, or expires, BillingPaymentService calls Function 1 (CreditAsync) to reverse the EA debit, sets the EA leg to Reversed (4) with a ReversalReference, restores the student's wallet balance, marks the transaction Failed/Cancelled, and restores the invoice to Issued (2) (or sets both the EA leg and transaction to ReconciliationRequired (5) if the reversal call itself fails, TC-109).

**Actual Result:**
> 1. ProcessGatewayWebhookHandler.SettleFailed never calls EducationAccountClient.CreditAsync; it sets transaction.Status = 5 (ReconciliationRequired) while leaving the EA leg at status = 2 (Succeeded), reversal_reference = NULL, and wallet.balance = 0.00 (unrefunded).
> 2. In CreateCheckoutHandler.cs (line 226), online session creation failure logs 'TODO reverse EA leg' without calling CreditAsync.
> 3. 'payment.cancelled' is ignored completely.

**Pytest Strict XFAIL Directive:**
```python
@pytest.mark.xfail(strict=True, reason="BUG-R9-019: [Split Payment Failure / Cancel / Timeout] Online failure, cancellation or session failure after EA debit does not automatically reverse the EA deduction")
```

---

### `BUG-R9-020`: [SCR-07 Receipt] Payment confirmation screen only offers Print receipt and has no Download PDF button or endpoint

- **Module**: `R9` (R9 Defect)
- **Status**: **Open**
- **Severity / Priority**: `S2` / `High`
- **Defect Type**: `Functional`
- **Linked Test Case(s)**: `TC-131, TC-132`
- **Environment**: SIT (Local QA Stack) | e-Service: http://localhost:5174 | API Gateway: http://localhost:5273 | Database: edufams-qa-sqlserver (SQL Server 2022) | Browser: Chrome (latest), Windows 11 | Build: QA_BE / develop (22 Oct 2026)
- **Evidence**: Image 20 (sheet Evidence)
evidence_20_BUG-R9-020.png
- **Notes**: Root cause: PaymentResultPage.tsx only implements window.print() and BillingPaymentService has no PDF receipt generation endpoint.

**Preconditions:**
```text
An Education Account payment (TC-131) or Split payment (TC-132) has succeeded and the Parent is on SCR-07 (/payment-result).
```

**Steps to Reproduce:**
1. Open /payment-result?transactionId={txId} for a Succeeded EA or Split payment.
2. Look for the action to download the receipt as a PDF file.

**Expected Result:**
> SCR-07 provides a 'Download PDF' action that downloads a PDF receipt containing the transaction reference, funding part(s), and total settled amount (TC-131, TC-132).

**Actual Result:**
> SCR-07 only renders a 'Print receipt' button (which calls window.print()) and a 'Back to home' link. Neither a Download PDF button nor a backend PDF receipt endpoint exists.

**Pytest Strict XFAIL Directive:**
```python
@pytest.mark.xfail(strict=True, reason="BUG-R9-020: [SCR-07 Receipt] Payment confirmation screen only offers Print receipt and has no Download PDF button or endpoint")
```

---

### `BUG-R9-021`: [SCR-08 Payment failed] Failure screen omits the failure reason, omits the EA-returned notice for refunded splits, and has no Try again button

- **Module**: `R9` (R9 Defect)
- **Status**: **Open**
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Defect Type**: `UI`
- **Linked Test Case(s)**: `TC-136, TC-137, TC-140`
- **Environment**: SIT (Local QA Stack) | e-Service: http://localhost:5174 | API Gateway: http://localhost:5273 | Database: edufams-qa-sqlserver (SQL Server 2022) | Browser: Chrome (latest), Windows 11 | Build: QA_BE / develop (22 Oct 2026)
- **Evidence**: Image 21 (sheet Evidence)
evidence_21_BUG-R9-021.png
- **Notes**: Root cause: PaymentResultPage.tsx does not render transaction.failureReason, has no 'Try again' button, and only renders refund/deduction copy under ReconciliationRequired instead of Failed + Reversed.

**Preconditions:**
```text
An Online payment or Split payment has failed and the Parent is viewing SCR-08 (/payment-result?transactionId={txId}).
```

**Steps to Reproduce:**
1. Open /payment-result for a Failed online or split payment that includes a failureReason.
2. Check the screen for (a) the short friendly failure reason (TC-136), (b) the statement that the Education Account amount was returned when the EA leg is Reversed (TC-137), and (c) the 'Try again' button to start a new transaction with a new idempotency key (TC-140).

**Expected Result:**
> 1. SCR-08 displays 'Your payment could not be completed. No amount was deducted.', the short failure reason, and the actions 'Try again' and 'Exit' (TC-136, TC-140).
> 2. For a failed split payment whose EA leg was reversed, SCR-08 states 'Your online payment could not be completed. The amount taken from the Education Account has been returned.' (TC-137).

**Actual Result:**
> SCR-08 only displays 'Your payment could not be completed. Return to Fees & Payments to review the latest outstanding fees.' and a 'Back to home' link. It omits the failure reason, omits the EA-returned message when transaction.status === 'Failed' and eaLeg.status === 'Reversed', and provides no 'Try again' button.

**Pytest Strict XFAIL Directive:**
```python
@pytest.mark.xfail(strict=True, reason="BUG-R9-021: [SCR-08 Payment failed] Failure screen omits the failure reason, omits the EA-returned notice for refunded splits, and has no Try again button")
```

---

### `BUG-R9-022`: [Error Handling UI] 5xx API errors on charge list, checkout confirm, and payment result render raw server error strings (SqlException) on screen

- **Module**: `R9` (R9 Defect)
- **Status**: **Open**
- **Severity / Priority**: `S2` / `High`
- **Defect Type**: `Security`
- **Linked Test Case(s)**: `TC-138, TC-144, TC-164`
- **Environment**: SIT (Local QA Stack) | e-Service: http://localhost:5174 | API Gateway: http://localhost:5273 | Database: edufams-qa-sqlserver (SQL Server 2022) | Browser: Chrome (latest), Windows 11 | Build: QA_BE / develop (22 Oct 2026)
- **Evidence**: Image 22 (sheet Evidence)
evidence_22_BUG-R9-022.png
- **Notes**: Root cause: packages/api-client/src/api-error.ts returns server errors[] strings even when statusCode >= 500 instead of masking 5xx errors with a generic user-safe message.

**Preconditions:**
```text
A 500 Internal Server Error with server error details in errors[] occurs when loading outstanding charges (SCR-02), confirming checkout (SCR-05), or loading payment result (SCR-08).
```

**Steps to Reproduce:**
1. Trigger or mock an HTTP 500 response containing internal error text (e.g. 'System.Data.SqlClient.SqlException: Timeout expired...') on GET /outstanding-charges (TC-164), POST /checkout (TC-144), or GET /transactions/{id} (TC-138).
2. Observe the error message rendered to the Parent on the UI.

**Expected Result:**
> The UI hides all technical details (SQL exceptions, stack traces, class names, HTTP codes) and displays only the safe friendly message 'Something went wrong. Please try again later.' (TC-138, TC-144, TC-164).

**Actual Result:**
> getBillingPaymentErrorMessage in packages/api-client/src/api-error.ts concatenates and returns response.errors[] verbatim on 5xx responses, causing the UI to display raw 'System.Data.SqlClient.SqlException...' strings directly to the Parent.

**Pytest Strict XFAIL Directive:**
```python
@pytest.mark.xfail(strict=True, reason="BUG-R9-022: [Error Handling UI] 5xx API errors on charge list, checkout confirm, and payment result render raw server error strings (SqlException) on screen")
```

---

### `BUG-R9-023`: [Database Constraints] dbo.invoice_items allows attaching a student_charge from a different school_id than dbo.invoices.school_id

- **Module**: `R9` (R9 Defect)
- **Status**: **Open**
- **Severity / Priority**: `S3` / `Medium`
- **Defect Type**: `Data`
- **Linked Test Case(s)**: `TC-149`
- **Environment**: SIT (Local QA Stack) | e-Service: http://localhost:5174 | API Gateway: http://localhost:5273 | Database: edufams-qa-sqlserver (SQL Server 2022) | Browser: Chrome (latest), Windows 11 | Build: QA_BE / develop (22 Oct 2026)
- **Evidence**: Image 23 (sheet Evidence)
evidence_23_BUG-R9-023.png
- **Notes**: Root cause: Missing composite FK (invoice_id, school_id) / trigger on dbo.invoice_items and missing multi-school validation in CheckoutPlanner.

**Preconditions:**
```text
An invoice exists for School A in BillingPaymentService.dbo.invoices and a student_charge exists for School B in dbo.student_charges.
```

**Steps to Reproduce:**
1. Insert an invoice with school_id = School A into BillingPaymentService.dbo.invoices.
2. Insert a student_charge with school_id = School B into dbo.student_charges.
3. Insert a line into dbo.invoice_items linking that student_charge to the invoice (TC-149).

**Expected Result:**
> The database (and checkout planner) refuses to attach a student_charge whose school_id differs from the invoice's school_id (TC-149).

**Actual Result:**
> The insert into dbo.invoice_items succeeds ('OK') because neither a composite foreign key / trigger in SQL Server nor a check in CheckoutPlanner verifies that student_charges.school_id matches invoices.school_id.

**Pytest Strict XFAIL Directive:**
```python
@pytest.mark.xfail(strict=True, reason="BUG-R9-023: [Database Constraints] dbo.invoice_items allows attaching a student_charge from a different school_id than dbo.invoices.school_id")
```

---
