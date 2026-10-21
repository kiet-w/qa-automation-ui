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
| [`BUG-R8-001`](#bug-r8-001) | `R8` | **Open** | S2 | High | Functional | [My details] No success message after saving valid phone, email and mailing address | `TC-R8-097` |
| [`BUG-R8-002`](#bug-r8-002) | `R8` | **Open** | S2 | High | Functional | [My details] Invalid mobile numbers are accepted and saved | `TC-R8-099` |
| [`BUG-R8-003`](#bug-r8-003) | `R8` | **Open** | S4 (lowest) | Low | Data | [My details] Mobile number entered with a space is saved with the space | `TC-R8-100` |
| [`BUG-R8-004`](#bug-r8-004) | `R8` | **Open** | S4 (lowest) | Low | UI | [My details] Invalid email message does not match MSG-0806 | `TC-R8-101` |
| [`BUG-R8-005`](#bug-r8-005) | `R8` | **Open** | S2 | High | Functional | [My details] Required fields cannot be cleared, so MSG-0001 cannot be triggered | `TC-R8-103` |
| [`BUG-R9-001`](#bug-r9-001) | `R9` | **Open** | S2 | High | Functional | [SCR-08 Payment failed] Failed online payment shows no invoice status, no settled amount and no Try again or Exit action | `TC-090, TC-136` |
| [`BUG-R9-002`](#bug-r9-002) | `R9` | **Open** | S2 | High | Data | [SCR-07 Payment result] Date and time of payment are wrong and shown without a time zone | `TC-135, TC-129, TC-065` |
| [`BUG-R9-003`](#bug-r9-003) | `R9` | **Open** | S3 | Medium | UI | [SCR-07 Receipt] Print preview shows the application header and skip link over the receipt | `TC-133` |

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

### `BUG-R8-001`: [My details] No success message after saving valid phone, email and mailing address

- **Module**: `R8` (R8 Defect)
- **Status**: **Open**
- **Severity / Priority**: `S2` / `High`
- **Defect Type**: `Functional`
- **Linked Test Case(s)**: `TC-R8-097`
- **Environment**: SIT |  Chrome (latest), Windows 11 |  Build: TBC |  Mock SingPass + mock data API
- **Evidence**: No screenshot supplied. Result recorded in TC-R8-097 Actual Result
- **Notes**: The test case severity is S1. Defect severity is set to S2 because the save itself may work. Raise to S1 if the values or the audit log are not saved.

**Preconditions:**
```text
Family Account holder (FA) is logged in.
```

**Steps to Reproduce:**
1. Open My details.
2. Enter phone 98887777, email fa.new@example.sg, mailing Blk 9, Verde Walk, #02-01, 650009, Singapore.
3. Click Save.

**Expected Result:**
> MSG-0807 'Your details have been updated.' is shown. Values persist after reload. The audit log has one entry per changed field. No email is sent.

**Actual Result:**
> No success message is displayed after the profile is updated. Persistence, audit log and email outbox were not recorded in the test case result.

**Pytest Strict XFAIL Directive:**
```python
@pytest.mark.xfail(strict=True, reason="BUG-R8-001: [My details] No success message after saving valid phone, email and mailing address")
```

---

### `BUG-R8-002`: [My details] Invalid mobile numbers are accepted and saved

- **Module**: `R8` (R8 Defect)
- **Status**: **Open**
- **Severity / Priority**: `S2` / `High`
- **Defect Type**: `Functional`
- **Linked Test Case(s)**: `TC-R8-099`
- **Environment**: SIT |  Chrome (latest), Windows 11 |  Build: TBC |  Mock SingPass + mock data API
- **Evidence**: No screenshot supplied. Result recorded in TC-R8-099 Actual Result
- **Notes**: The test case result does not say which of the six values were accepted. Record the value list at retest.

**Preconditions:**
```text
Family Account holder (FA) is logged in.
```

**Steps to Reproduce:**
1. Open My details.
2. For each value, enter it as the mobile number and click Save: 71234567, 51234567, 9123456, 912345678, 9123abcd, +6591234567.

**Expected Result:**
> MSG-0805 'Enter a mobile number in the correct format, like 9123 4567' is shown and nothing is saved.

**Actual Result:**
> The invalid mobile numbers can be saved. MSG-0805 is not shown.

**Pytest Strict XFAIL Directive:**
```python
@pytest.mark.xfail(strict=True, reason="BUG-R8-002: [My details] Invalid mobile numbers are accepted and saved")
```

---

### `BUG-R8-003`: [My details] Mobile number entered with a space is saved with the space

- **Module**: `R8` (R8 Defect)
- **Status**: **Open**
- **Severity / Priority**: `S4 (lowest)` / `Low`
- **Defect Type**: `Data`
- **Linked Test Case(s)**: `TC-R8-100`
- **Environment**: SIT |  Chrome (latest), Windows 11 |  Build: TBC |  Mock SingPass + mock data API
- **Evidence**: No screenshot supplied. Result recorded in TC-R8-100 Actual Result
- **Notes**: Result wording is 'Save with space'. Confirm at retest that the stored value in the database contains the space.

**Preconditions:**
```text
Family Account holder (FA) is logged in.
```

**Steps to Reproduce:**
1. Open My details.
2. Enter mobile number '9123 4567'.
3. Click Save.
4. Check the stored value.

**Expected Result:**
> Saved with MSG-0807 and stored as 91234567 (space removed).

**Actual Result:**
> Saved with the space kept, as typed.

**Pytest Strict XFAIL Directive:**
```python
@pytest.mark.xfail(strict=True, reason="BUG-R8-003: [My details] Mobile number entered with a space is saved with the space")
```

---

### `BUG-R8-004`: [My details] Invalid email message does not match MSG-0806

- **Module**: `R8` (R8 Defect)
- **Status**: **Open**
- **Severity / Priority**: `S4 (lowest)` / `Low`
- **Defect Type**: `UI`
- **Linked Test Case(s)**: `TC-R8-101`
- **Environment**: SIT |  Chrome (latest), Windows 11 |  Build: TBC |  Mock SingPass + mock data API
- **Evidence**: No screenshot supplied. Result recorded in TC-R8-101 Actual Result
- **Notes**: To confirm with the tester: the Actual Result in the test case only contains the message text. This defect assumes the validation works and only the message text differs. Change or reject it if the fault is different.

**Preconditions:**
```text
Family Account holder (FA) is logged in.
```

**Steps to Reproduce:**
1. Open My details.
2. For each value, enter it as the email and click Save: nameexample.com, name@, @example.com, name@example, name @example.com.

**Expected Result:**
> MSG-0806 'Enter an email address in the correct format, like name@example.com' is shown and nothing is saved.

**Actual Result:**
> The message shown is 'Enter an email address in the correct format.' The example 'like name@example.com' is missing.

**Pytest Strict XFAIL Directive:**
```python
@pytest.mark.xfail(strict=True, reason="BUG-R8-004: [My details] Invalid email message does not match MSG-0806")
```

---

### `BUG-R8-005`: [My details] Required fields cannot be cleared, so MSG-0001 cannot be triggered

- **Module**: `R8` (R8 Defect)
- **Status**: **Open**
- **Severity / Priority**: `S2` / `High`
- **Defect Type**: `Functional`
- **Linked Test Case(s)**: `TC-R8-103`
- **Environment**: SIT |  Chrome (latest), Windows 11 |  Build: TBC |  Mock SingPass + mock data API
- **Evidence**: No screenshot supplied. Result recorded in TC-R8-103 Actual Result
- **Notes**: To confirm with the tester: whether the field refuses deletion, is read only, or the old value comes back after the field is emptied.

**Preconditions:**
```text
Family Account holder (FA) is logged in.
```

**Steps to Reproduce:**
1. Open My details.
2. Clear Mobile number, Email, Mailing street, Mailing postal code and Mailing country.
3. Click Save.

**Expected Result:**
> MSG-0001 is shown under each blank field (for example 'Enter your email') and nothing is saved.

**Actual Result:**
> The required fields cannot be cleared, so the blank field validation cannot be reached.

**Pytest Strict XFAIL Directive:**
```python
@pytest.mark.xfail(strict=True, reason="BUG-R8-005: [My details] Required fields cannot be cleared, so MSG-0001 cannot be triggered")
```

---

### `BUG-R9-001`: [SCR-08 Payment failed] Failed online payment shows no invoice status, no settled amount and no Try again or Exit action

- **Module**: `R9` (R9 Defect)
- **Status**: **Open**
- **Severity / Priority**: `S2` / `High`
- **Defect Type**: `Functional`
- **Linked Test Case(s)**: `TC-090, TC-136`
- **Environment**: SIT (per test cases) |  Chrome (latest) |  Build: to be recorded at execution |  E-service opened through a devtunnels.ms host (see footer of Image 8)
- **Evidence**: Image 6 (sheet Evidence)
- **Notes**: Check in the database that the invoice is Issued after the failure, as TC-090 expects. If it is, the '—' is a display problem only.

**Preconditions:**
```text
Parent signed in through Singpass, an invoice of SGD 25.00 is Issued, the payment method is Online only.
 The payment provider is set to fail the payment (simulator: Pay failed).
```

**Steps to Reproduce:**
1. Choose the invoice and pay online only.
2. Fail the payment at the payment provider.
3. Read the Payment result page that opens.

**Expected Result:**
> SCR-08 shows 'Your payment could not be completed. No amount was deducted.', a short reason, the transaction reference and the actions Try again and Exit. The invoice is back to Issued and its status is shown (TC-090, TC-136).

**Actual Result:**
> The page shows 'Payment failed' with the text 'Your payment could not be completed. Return to Fees & Payments to review the latest outstanding fees.' Invoice ID is shown as a GUID with the label '(invoice number unavailable)'. Invoice status is '—'. Settled amount is '—' and the Online Gateway row repeats 'Settled amount: —'. Only a Back to home link is offered. There is no Try again or Exit, no reason and no statement that nothing was deducted.

**Pytest Strict XFAIL Directive:**
```python
@pytest.mark.xfail(strict=True, reason="BUG-R9-001: [SCR-08 Payment failed] Failed online payment shows no invoice status, no settled amount and no Try again or Exit action")
```

---

### `BUG-R9-002`: [SCR-07 Payment result] Date and time of payment are wrong and shown without a time zone

- **Module**: `R9` (R9 Defect)
- **Status**: **Open**
- **Severity / Priority**: `S2` / `High`
- **Defect Type**: `Data`
- **Linked Test Case(s)**: `TC-135, TC-129, TC-065`
- **Environment**: SIT (per test cases) |  Chrome (latest) |  Build: to be recorded at execution |  E-service opened through a devtunnels.ms host (see footer of Image 8)
- **Evidence**: Image 7 (sheet Evidence), also visible in Image 6 and Image 8
- **Notes**: The tester reports this on the whole system. Screens of R1, R3 and R8 that show a date or time still need to be checked. Expected value is SGT per TC-135, confirm the required time zone and display format with the Business Analyst.

**Preconditions:**
```text
Parent signed in through Singpass, an invoice is Issued, the EA balance is enough for the payment.
```

**Steps to Reproduce:**
1. Pay the invoice with the Education Account.
2. On the success screen read 'Completed at'.
3. Compare it with the paid at value in the database and with the Singapore time of the payment.

**Expected Result:**
> The database value is in UTC and the screen shows the same moment in Singapore time (SGT), eight hours later, for example 14:00 for 06:00 UTC (TC-135).

**Actual Result:**
> The success screen of INV000011, SGD 30.00, shows 'Completed at Oct 15, 2026, 6:37 PM', which the tester reports as wrong. The failed payment screen (Completed at 6:36 PM) and the receipt print (Issued at 6:37 PM) show the same kind of value. No time zone is shown. In QA's earlier local run on the Dev package the UI displayed the UTC value from the database without conversion (database 17:16 UTC shown as 5:16 PM).

**Pytest Strict XFAIL Directive:**
```python
@pytest.mark.xfail(strict=True, reason="BUG-R9-002: [SCR-07 Payment result] Date and time of payment are wrong and shown without a time zone")
```

---

### `BUG-R9-003`: [SCR-07 Receipt] Print preview shows the application header and skip link over the receipt

- **Module**: `R9` (R9 Defect)
- **Status**: **Open**
- **Severity / Priority**: `S3` / `Medium`
- **Defect Type**: `UI`
- **Linked Test Case(s)**: `TC-133`
- **Environment**: SIT (per test cases) |  Chrome (latest) |  Build: to be recorded at execution |  E-service opened through a devtunnels.ms host (see footer of Image 8)
- **Evidence**: Image 8 (sheet Evidence)
- **Notes**: Likely fix: a print stylesheet that hides the header, menu and skip link. Check the downloaded PDF receipt separately (TC-131).

**Preconditions:**
```text
Parent signed in through Singpass, an EA payment has succeeded and SCR-07 is open.
```

**Steps to Reproduce:**
1. On SCR-07 click Print (or press Ctrl+P).
2. Look at the print preview.

**Expected Result:**
> The print preview shows only the receipt: reference, parts and total. The application header and navigation are not printed (TC-133).

**Actual Result:**
> The 'EduSave E-Service' header, the language selector, the menu button and the 'Skip to main content' link are drawn over the receipt and cover its first rows. The receipt runs to 2 pages and the footer prints the page URL.

**Pytest Strict XFAIL Directive:**
```python
@pytest.mark.xfail(strict=True, reason="BUG-R9-003: [SCR-07 Receipt] Print preview shows the application header and skip link over the receipt")
```

---
