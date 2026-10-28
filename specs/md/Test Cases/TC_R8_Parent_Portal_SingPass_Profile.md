# R8: Parent Portal (SingPass, Profile & Account Info) — Sprint 1 Test Cases

> **Module**: R8 - Parent Portal & SingPass Profile
> **Specification Reference**: [FS-08_Parent_Portal_SingPass_Profile.md](file:////home/baudui/Projects/automation-ui/[agile] fs/md/FS document/FS-08_Parent_Portal_SingPass_Profile.md)
> **Source Spreadsheet**: `Test Cases + Defect sprint 1.xlsx` (Sheet `R8 TC`)
> **Total Test Cases**: 87

## Executive Test Suite Summary

| Test Suite | Scenario Count | Test Cases | Priorities | Severities |
| :--- | :--- | :--- | :--- | :--- |
| Login / Session | 1 (TS-001) | 9 | Critical, High, Medium | S1 (highest), S2, S3 |
| Home | 1 (TS-002) | 7 | High, Low, Medium | S2, S3, S4 (lowest) |
| My Profile | 1 (TS-003) | 15 | Critical, High, Low, Medium | S1 (highest), S2, S3, S4 (lowest) |
| Profile Validation (R8) | 1 (TS-004) | 36 | High, Low, Medium | S2, S3, S4 (lowest) |
| Transactions | 1 (TS-005) | 11 | High, Low, Medium | S2, S3, S4 (lowest) |
| Fees & Payments (R9) | 1 (TS-006) | 5 | High, Low, Medium | S2, S3, S4 (lowest) |
| Navigation & Language | 1 (TS-007) | 4 | High, Low, Medium | S2, S3, S4 (lowest) |

---

## Quick Reference Index Table

| Test Case ID | Scenario ID | Title | Page / Area | Priority | Severity | Type | Defect ID | Traceability |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| [`TC-001`](#tc-001) | `TS-001` | Verify login page shows title, description and [Sign in with Singpass] button | Parent Login page | Medium | S3 | UI |  | R8 |
| [`TC-002`](#tc-002) | `TS-001` | Verify [Sign in with Singpass] opens Mockpass with correct login parameters | Parent Login page | High | S2 | Integration |  | R8 |
| [`TC-003`](#tc-003) | `TS-001` | Verify parent can log in with a Mockpass persona and lands on Home | Mockpass / Home | Critical | S1 (highest) | Functional |  | R8 |
| [`TC-004`](#tc-004) | `TS-001` | Verify opening / without a session redirects to the login page | Auth guard | High | S2 | Security |  | R8 |
| [`TC-005`](#tc-005) | `TS-001` | Verify opening /profile without a session redirects to the login page | Auth guard | High | S2 | Security |  | R8 |
| [`TC-006`](#tc-006) | `TS-001` | Verify opening /transactions without a session redirects to the login page | Auth guard | High | S2 | Security |  | R8 |
| [`TC-007`](#tc-007) | `TS-001` | Verify opening /billing without a session redirects to the login page | Auth guard | High | S2 | Security |  | R8 |
| [`TC-008`](#tc-008) | `TS-001` | Verify invalid login callback shows an error and returns to login | Login callback page | High | S2 | Security |  | R8 |
| [`TC-009`](#tc-009) | `TS-001` | Verify [Log out] ends the session and protected pages need login again | Header | Critical | S1 (highest) | Security |  | R8 |
| [`TC-010`](#tc-010) | `TS-002` | Verify Home header, menu and page description | Home page | Medium | S3 | UI |  | TBC |
| [`TC-011`](#tc-011) | `TS-002` | Verify one card per linked child with Active badge | Home page | High | S2 | Functional |  | TBC |
| [`TC-012`](#tc-012) | `TS-002` | Verify Nur Aisyah card shows balance and profile details | Home page | High | S2 | Functional |  | TBC |
| [`TC-013`](#tc-013) | `TS-002` | Verify Nur Iman card shows profile details and a balance state | Home page | Medium | S3 | Functional |  | TBC |
| [`TC-014`](#tc-014) | `TS-002` | Verify children NRIC is masked on Home cards | Home page | High | S2 | Security |  | TBC |
| [`TC-015`](#tc-015) | `TS-002` | Verify clicking a child name opens that child's transactions | Home page | Medium | S3 | Functional |  | TBC |
| [`TC-016`](#tc-016) | `TS-002` | Verify card subtitle shows the child's age as a number | Home page | Low | S4 (lowest) | UI | BUG-010 | TBC |
| [`TC-017`](#tc-017) | `TS-003` | Verify My Profile shows Singpass identity, contact and mailing cards | My Profile page | High | S2 | Functional |  | R8 |
| [`TC-018`](#tc-018) | `TS-003` | Verify NRIC is masked and can be shown / hidden | My Profile page | High | S2 | Security |  | R8 |
| [`TC-019`](#tc-019) | `TS-003` | Verify residential address comes from Singpass | My Profile page | Medium | S3 | Functional |  | R8 |
| [`TC-020`](#tc-020) | `TS-003` | Verify residential address shows floor and unit like Singpass | My Profile page | Medium | S3 | Functional | BUG-009 | R8 |
| [`TC-021`](#tc-021) | `TS-003` | Verify [Update details] opens the form with saved values and Save disabled | My Profile – edit | High | S2 | Functional |  | R8 |
| [`TC-022`](#tc-022) | `TS-003` | Verify focus moves to Mobile Number when editing starts | My Profile – edit | Low | S4 (lowest) | UI |  | R8 |
| [`TC-023`](#tc-023) | `TS-003` | Verify edit form shows the Mailing address card only once | My Profile – edit | Medium | S3 | UI | BUG-001 | R8 |
| [`TC-024`](#tc-024) | `TS-003` | Verify [Cancel] leaves edit mode without saving | My Profile – edit | High | S2 | Functional |  | R8 |
| [`TC-025`](#tc-025) | `TS-003` | Verify [Save changes] is enabled after a change and disabled when the change is undone | My Profile – edit | Medium | S3 | Functional |  | R8 |
| [`TC-026`](#tc-026) | `TS-003` | Verify spaces around a value are trimmed when leaving the field | My Profile – edit | Low | S4 (lowest) | Functional |  | R8 |
| [`TC-027`](#tc-027) | `TS-003` | Verify valid change opens the confirm dialog and [Keep editing] keeps the change | My Profile – edit | High | S2 | Functional |  | R8 |
| [`TC-028`](#tc-028) | `TS-003` | Verify save failure shows MSG-0808 | My Profile – edit | High | S2 | Functional | BUG-008 | R8 / FS08 Save behavior |
| [`TC-029`](#tc-029) | `TS-003` | Verify successful save shows MSG-0807 | My Profile – edit | High | S2 | Functional |  | R8 / FS08 Save behavior |
| [`TC-030`](#tc-030) | `TS-003` | Verify mobile number is saved and shown after reload | My Profile – edit | Critical | S1 (highest) | Integration |  | R8 |
| [`TC-031`](#tc-031) | `TS-003` | Verify profile is read-only when all linked children are 16 or older | My Profile page | High | S2 | Functional |  | R8 / FS08 Save behavior |
| [`TC-032`](#tc-032) | `TS-004` | Verify Mobile Number – blank shows an error | My Profile – edit | High | S2 | Functional | BUG-003 | R8 / FS08 Field rules – Mobile Number |
| [`TC-033`](#tc-033) | `TS-004` | Verify Mobile Number – 7 digits shows an error | My Profile – edit | High | S2 | Functional | BUG-002 | R8 / FS08 Field rules – Mobile Number |
| [`TC-034`](#tc-034) | `TS-004` | Verify Mobile Number – 9 digits shows an error | My Profile – edit | High | S2 | Functional | BUG-002 | R8 / FS08 Field rules – Mobile Number |
| [`TC-035`](#tc-035) | `TS-004` | Verify Mobile Number – starts with 7 shows an error | My Profile – edit | High | S2 | Functional | BUG-002 | R8 / FS08 Field rules – Mobile Number |
| [`TC-036`](#tc-036) | `TS-004` | Verify Mobile Number – starts with 1 shows an error | My Profile – edit | High | S2 | Functional | BUG-002 | R8 / FS08 Field rules – Mobile Number |
| [`TC-037`](#tc-037) | `TS-004` | Verify Mobile Number – with letters shows an error | My Profile – edit | High | S2 | Functional | BUG-002 | R8 / FS08 Field rules – Mobile Number |
| [`TC-038`](#tc-038) | `TS-004` | Verify Mobile Number – with symbols shows an error | My Profile – edit | High | S2 | Functional | BUG-002 | R8 / FS08 Field rules – Mobile Number |
| [`TC-039`](#tc-039) | `TS-004` | Verify Mobile Number – valid, starts with 9 is accepted | My Profile – edit | Medium | S3 | Functional |  | R8 / FS08 Field rules – Mobile Number |
| [`TC-040`](#tc-040) | `TS-004` | Verify Mobile Number – valid, starts with 8 is accepted | My Profile – edit | Medium | S3 | Functional |  | R8 / FS08 Field rules – Mobile Number |
| [`TC-041`](#tc-041) | `TS-004` | Verify Mobile Number – valid, starts with 6 is accepted | My Profile – edit | Medium | S3 | Functional |  | R8 / FS08 Field rules – Mobile Number |
| [`TC-042`](#tc-042) | `TS-004` | Verify Email – blank shows an error | My Profile – edit | High | S2 | Functional | BUG-003 | R8 / FS08 Field rules – Email |
| [`TC-043`](#tc-043) | `TS-004` | Verify Email – without @ shows an error | My Profile – edit | High | S2 | Functional | BUG-004 | R8 / FS08 Field rules – Email |
| [`TC-044`](#tc-044) | `TS-004` | Verify Email – without domain shows an error | My Profile – edit | High | S2 | Functional | BUG-004 | R8 / FS08 Field rules – Email |
| [`TC-045`](#tc-045) | `TS-004` | Verify Email – without dot in domain shows an error | My Profile – edit | High | S2 | Functional | BUG-004 | R8 / FS08 Field rules – Email |
| [`TC-046`](#tc-046) | `TS-004` | Verify Email – with space shows an error | My Profile – edit | High | S2 | Functional | BUG-004 | R8 / FS08 Field rules – Email |
| [`TC-047`](#tc-047) | `TS-004` | Verify Email – 151 characters shows an error | My Profile – edit | High | S2 | Functional | BUG-005 | R8 / FS08 Field rules – Email |
| [`TC-048`](#tc-048) | `TS-004` | Verify Email – exactly 150 characters is accepted | My Profile – edit | Medium | S3 | Functional |  | R8 / FS08 Field rules – Email |
| [`TC-049`](#tc-049) | `TS-004` | Verify Email – valid is accepted | My Profile – edit | Medium | S3 | Functional |  | R8 / FS08 Field rules – Email |
| [`TC-050`](#tc-050) | `TS-004` | Verify Mailing Block – 21 characters shows an error | My Profile – edit | High | S2 | Functional | BUG-006 | R8 / FS08 Field rules – Mailing Block |
| [`TC-051`](#tc-051) | `TS-004` | Verify Mailing Block – exactly 20 characters is accepted | My Profile – edit | Medium | S3 | Functional |  | R8 / FS08 Field rules – Mailing Block |
| [`TC-052`](#tc-052) | `TS-004` | Verify Mailing Street – blank shows an error | My Profile – edit | High | S2 | Functional | BUG-003 | R8 / FS08 Field rules – Mailing Street |
| [`TC-053`](#tc-053) | `TS-004` | Verify Mailing Street – 101 characters shows an error | My Profile – edit | High | S2 | Functional | BUG-006 | R8 / FS08 Field rules – Mailing Street |
| [`TC-054`](#tc-054) | `TS-004` | Verify Mailing Street – exactly 100 characters is accepted | My Profile – edit | Medium | S3 | Functional |  | R8 / FS08 Field rules – Mailing Street |
| [`TC-055`](#tc-055) | `TS-004` | Verify Mailing Unit – 21 characters shows an error | My Profile – edit | High | S2 | Functional | BUG-006 | R8 / FS08 Field rules – Mailing Unit |
| [`TC-056`](#tc-056) | `TS-004` | Verify Mailing Unit – exactly 20 characters is accepted | My Profile – edit | Medium | S3 | Functional |  | R8 / FS08 Field rules – Mailing Unit |
| [`TC-057`](#tc-057) | `TS-004` | Verify Mailing Postal Code – blank shows an error | My Profile – edit | High | S2 | Functional | BUG-003 | R8 / FS08 Field rules – Mailing Postal Code |
| [`TC-058`](#tc-058) | `TS-004` | Verify Mailing Postal Code – 5 digits shows an error | My Profile – edit | High | S2 | Functional | BUG-007 | R8 / FS08 Field rules – Mailing Postal Code |
| [`TC-059`](#tc-059) | `TS-004` | Verify Mailing Postal Code – 7 digits shows an error | My Profile – edit | High | S2 | Functional | BUG-007 | R8 / FS08 Field rules – Mailing Postal Code |
| [`TC-060`](#tc-060) | `TS-004` | Verify Mailing Postal Code – with letters shows an error | My Profile – edit | High | S2 | Functional | BUG-007 | R8 / FS08 Field rules – Mailing Postal Code |
| [`TC-061`](#tc-061) | `TS-004` | Verify Mailing Postal Code – valid 6 digits is accepted | My Profile – edit | Medium | S3 | Functional |  | R8 / FS08 Field rules – Mailing Postal Code |
| [`TC-062`](#tc-062) | `TS-004` | Verify Mailing Country – blank shows an error | My Profile – edit | High | S2 | Functional | BUG-003 | R8 / FS08 Field rules – Mailing Country |
| [`TC-063`](#tc-063) | `TS-004` | Verify Mailing Country – 101 characters shows an error | My Profile – edit | High | S2 | Functional | BUG-006 | R8 / FS08 Field rules – Mailing Country |
| [`TC-064`](#tc-064) | `TS-004` | Verify Mailing Country – exactly 100 characters is accepted | My Profile – edit | Medium | S3 | Functional |  | R8 / FS08 Field rules – Mailing Country |
| [`TC-065`](#tc-065) | `TS-004` | Verify several invalid fields show all messages at the same time | My Profile – edit | Medium | S3 | Functional | BUG-002 | R8 / FS08 Save behavior |
| [`TC-066`](#tc-066) | `TS-004` | Verify error message clears when the user types again | My Profile – edit | Low | S4 (lowest) | UI |  | R8 |
| [`TC-067`](#tc-067) | `TS-004` | Verify all valid fields together open the confirm dialog | My Profile – edit | High | S2 | Functional |  | R8 |
| [`TC-068`](#tc-068) | `TS-005` | Verify Transactions page shows title, description and student filter | Transactions page | Medium | S3 | UI |  | TBC |
| [`TC-069`](#tc-069) | `TS-005` | Verify student summary shows account, masked NRIC and available balance | Transactions page | High | S2 | Functional |  | TBC |
| [`TC-070`](#tc-070) | `TS-005` | Verify table columns, 10 rows on page 1 and total count | Transactions page | Medium | S3 | Functional |  | TBC |
| [`TC-071`](#tc-071) | `TS-005` | Verify newest transaction is shown first | Transactions page | Medium | S3 | Functional |  | TBC |
| [`TC-072`](#tc-072) | `TS-005` | Verify [Next] and [Previous] paging | Transactions page | Medium | S3 | Functional |  | TBC |
| [`TC-073`](#tc-073) | `TS-005` | Verify Rows per page 25 shows all transactions on one page | Transactions page | Low | S4 (lowest) | Functional |  | TBC |
| [`TC-074`](#tc-074) | `TS-005` | Verify amount format and status values | Transactions page | Medium | S3 | UI |  | TBC |
| [`TC-075`](#tc-075) | `TS-005` | Verify each row shows a transaction code | Transactions page | Low | S4 (lowest) | UI |  | TBC |
| [`TC-076`](#tc-076) | `TS-005` | Verify All students shows the Account holder column | Transactions page | Medium | S3 | Functional |  | TBC |
| [`TC-077`](#tc-077) | `TS-005` | Verify switching back to All students clears the student from the URL | Transactions page | Low | S4 (lowest) | Functional |  | TBC |
| [`TC-078`](#tc-078) | `TS-005` | Verify unknown student id in the URL falls back to All students | Transactions page | Medium | S3 | Security |  | TBC |
| [`TC-079`](#tc-079) | `TS-006` | Verify account selection lists each child with account code and status | Choose an education account | High | S2 | Functional |  | R9 / F9.1 / SCR-01 |
| [`TC-080`](#tc-080) | `TS-006` | Verify summary cards show outstanding fees, balance and selected total | Pay education charges | High | S2 | Functional |  | R9 / F9.2 / SCR-02 |
| [`TC-081`](#tc-081) | `TS-006` | Verify empty state when there are no outstanding charges | Pay education charges | High | S2 | Functional |  | R9 / AC-02 / SCR-03 |
| [`TC-082`](#tc-082) | `TS-006` | Verify status filter options | Pay education charges | Low | S4 (lowest) | UI |  | R9 / SCR-02 |
| [`TC-083`](#tc-083) | `TS-006` | Verify invalid account id shows 'Payment context is invalid' | Pay education charges | Medium | S3 | Security |  | R9 / EX-01 (partly) |
| [`TC-084`](#tc-084) | `TS-007` | Verify each menu item opens its page and is marked active | Header | High | S2 | Functional |  | TBC |
| [`TC-085`](#tc-085) | `TS-007` | Verify brand name goes back to Home | Header | Low | S4 (lowest) | UI |  | TBC |
| [`TC-086`](#tc-086) | `TS-007` | Verify unknown page shows 404 with a link back to Home | 404 page | Low | S4 (lowest) | UI |  | TBC |
| [`TC-087`](#tc-087) | `TS-007` | Verify logged-in parent opening the login page is sent to Home | Parent Login page | Medium | S3 | Functional |  | R8 |

---

## Detailed Test Case Specifications


### Test Suite: Login / Session

#### `TC-001`: Verify login page shows title, description and [Sign in with Singpass] button

- **Scenario ID**: `TS-001`
- **Test Suite**: Login / Session
- **Page / Target**: `Parent Login page`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Passed` | **Test Type**: `UI`
- **Traceability**: R8
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_AUTH_01
Run: 23/10/2026

**Preconditions:**
```text
No parent session (browser storage is empty).
```

**Test Data:**
```text
-
```

**Test Steps:**
1. Open /parent/login

**Expected Result:**
> Title 'Parent portal login', text 'Use Singpass to access your parent profile.' and 'You will be redirected to Mockpass for secure authentication.' are shown; [Sign in with Singpass] is enabled

**Actual Result:**
> As expected

---

#### `TC-002`: Verify [Sign in with Singpass] opens Mockpass with correct login parameters

- **Scenario ID**: `TS-001`
- **Test Suite**: Login / Session
- **Page / Target**: `Parent Login page`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Passed` | **Test Type**: `Integration`
- **Traceability**: R8
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_AUTH_02
Run: 23/10/2026

**Preconditions:**
```text
No parent session (browser storage is empty).
```

**Test Data:**
```text
-
```

**Test Steps:**
1. Open /parent/login
2. Click [Sign in with Singpass]

**Expected Result:**
> Mockpass page opens; URL has client_id=template-iam-service, response_type=code, scope=openid, state, nonce and redirect_uri ending with /parent/callback

**Actual Result:**
> As expected

---

#### `TC-003`: Verify parent can log in with a Mockpass persona and lands on Home

- **Scenario ID**: `TS-001`
- **Test Suite**: Login / Session
- **Page / Target**: `Mockpass / Home`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Passed` | **Test Type**: `Functional`
- **Traceability**: R8
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_AUTH_03
Run: 23/10/2026

**Preconditions:**
```text
No parent session (browser storage is empty).
```

**Test Data:**
```text
Persona: S8411053A - Parent of Nur Aisyah
```

**Test Steps:**
1. Open /parent/login
2. Click [Sign in with Singpass]
3. Select persona S8411053A in the dropdown
4. Click [Log in with Singpass]

**Expected Result:**
> Home page 'EduSave E-Service Portal' is shown; menu shows My Profile; [Log out] is shown

**Actual Result:**
> As expected

---

#### `TC-004`: Verify opening / without a session redirects to the login page

- **Scenario ID**: `TS-001`
- **Test Suite**: Login / Session
- **Page / Target**: `Auth guard`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Passed` | **Test Type**: `Security`
- **Traceability**: R8
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_AUTH_04
Run: 23/10/2026

**Preconditions:**
```text
No parent session (browser storage is empty).
```

**Test Data:**
```text
URL: /
```

**Test Steps:**
1. Open / directly

**Expected Result:**
> User is redirected to /parent/login; 'Parent portal login' is shown

**Actual Result:**
> As expected

---

#### `TC-005`: Verify opening /profile without a session redirects to the login page

- **Scenario ID**: `TS-001`
- **Test Suite**: Login / Session
- **Page / Target**: `Auth guard`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Passed` | **Test Type**: `Security`
- **Traceability**: R8
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_AUTH_04
Run: 23/10/2026

**Preconditions:**
```text
No parent session (browser storage is empty).
```

**Test Data:**
```text
URL: /profile
```

**Test Steps:**
1. Open /profile directly

**Expected Result:**
> User is redirected to /parent/login; 'Parent portal login' is shown

**Actual Result:**
> As expected

---

#### `TC-006`: Verify opening /transactions without a session redirects to the login page

- **Scenario ID**: `TS-001`
- **Test Suite**: Login / Session
- **Page / Target**: `Auth guard`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Passed` | **Test Type**: `Security`
- **Traceability**: R8
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_AUTH_04
Run: 23/10/2026

**Preconditions:**
```text
No parent session (browser storage is empty).
```

**Test Data:**
```text
URL: /transactions
```

**Test Steps:**
1. Open /transactions directly

**Expected Result:**
> User is redirected to /parent/login; 'Parent portal login' is shown

**Actual Result:**
> As expected

---

#### `TC-007`: Verify opening /billing without a session redirects to the login page

- **Scenario ID**: `TS-001`
- **Test Suite**: Login / Session
- **Page / Target**: `Auth guard`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Passed` | **Test Type**: `Security`
- **Traceability**: R8
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_AUTH_04
Run: 23/10/2026

**Preconditions:**
```text
No parent session (browser storage is empty).
```

**Test Data:**
```text
URL: /billing
```

**Test Steps:**
1. Open /billing directly

**Expected Result:**
> User is redirected to /parent/login; 'Parent portal login' is shown

**Actual Result:**
> As expected

---

#### `TC-008`: Verify invalid login callback shows an error and returns to login

- **Scenario ID**: `TS-001`
- **Test Suite**: Login / Session
- **Page / Target**: `Login callback page`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Passed` | **Test Type**: `Security`
- **Traceability**: R8
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Assumption Reference**: Redirect delay is 3 seconds (from code)
- **Note**: Auto: TC_AUTH_05
Run: 23/10/2026

**Preconditions:**
```text
No parent session (browser storage is empty).
```

**Test Data:**
```text
URL: /parent/callback?code=fake-code&state=wrong-state
```

**Test Steps:**
1. Open the callback URL with a wrong state
2. Wait 3 seconds

**Expected Result:**
> Message 'The authentication link is invalid or has expired.' and 'Returning to the sign-in page in a few seconds…' are shown; after ~3s user is on /parent/login

**Actual Result:**
> As expected

---

#### `TC-009`: Verify [Log out] ends the session and protected pages need login again

- **Scenario ID**: `TS-001`
- **Test Suite**: Login / Session
- **Page / Target**: `Header`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Passed` | **Test Type**: `Security`
- **Traceability**: R8
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_AUTH_06
Run: 23/10/2026

**Preconditions:**
```text
No parent session (browser storage is empty).
```

**Test Data:**
```text
Persona: S8411053A
```

**Test Steps:**
1. Log in with persona S8411053A
2. Click [Log out]
3. Open /profile

**Expected Result:**
> After logout user is on /parent/login; opening /profile redirects to login; session data is removed

---


### Test Suite: Home

#### `TC-010`: Verify Home header, menu and page description

- **Scenario ID**: `TS-002`
- **Test Suite**: Home
- **Page / Target**: `Home page`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Passed` | **Test Type**: `UI`
- **Traceability**: TBC
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_HOME_01
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
```

**Test Data:**
```text
-
```

**Test Steps:**
1. Open Home (/)

**Expected Result:**
> Description 'View your children's education account and transaction history.' is shown; menu has Home, My Profile, Transactions, FAS Application, Fees & Payments; Home is active; Language and [Log out] are shown

**Actual Result:**
> As expected

---

#### `TC-011`: Verify one card per linked child with Active badge

- **Scenario ID**: `TS-002`
- **Test Suite**: Home
- **Page / Target**: `Home page`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Passed` | **Test Type**: `Functional`
- **Traceability**: TBC
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_HOME_02
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
```

**Test Data:**
```text
-
```

**Test Steps:**
1. Open Home (/)

**Expected Result:**
> Exactly one card for Nur Iman (X04) and one for Nur Aisyah (S01); each shows 'Active'

**Actual Result:**
> As expected

---

#### `TC-012`: Verify Nur Aisyah card shows balance and profile details

- **Scenario ID**: `TS-002`
- **Test Suite**: Home
- **Page / Target**: `Home page`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Passed` | **Test Type**: `Functional`
- **Traceability**: TBC
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Assumption Reference**: Values come from current seed data
- **Note**: Auto: TC_HOME_03
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
```

**Test Data:**
```text
Student: Nur Aisyah (S01)
```

**Test Steps:**
1. Open Home (/)
2. Check the Nur Aisyah card

**Expected Result:**
> EA balance SGD 1,590.00; Date of birth Feb 2, 2012; Gender Female; NRIC *****001E; address contains Clementi Avenue 3

**Actual Result:**
> As expected

---

#### `TC-013`: Verify Nur Iman card shows profile details and a balance state

- **Scenario ID**: `TS-002`
- **Test Suite**: Home
- **Page / Target**: `Home page`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Blocked` | **Test Type**: `Functional`
- **Traceability**: TBC
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_HOME_04
Home heading was not found when the test opened '/' (page did not load). Re-run.
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
```

**Test Data:**
```text
Student: Nur Iman (X04)
```

**Test Steps:**
1. Open Home (/)
2. Check the Nur Iman card

**Expected Result:**
> Date of birth Mar 10, 2019; Gender Male; NRIC *****404A; EA balance shows an amount or 'Balance unavailable' (not stuck on loading)

---

#### `TC-014`: Verify children NRIC is masked on Home cards

- **Scenario ID**: `TS-002`
- **Test Suite**: Home
- **Page / Target**: `Home page`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Passed` | **Test Type**: `Security`
- **Traceability**: TBC
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_HOME_05
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
```

**Test Data:**
```text
-
```

**Test Steps:**
1. Open Home (/)
2. Check the NRIC / FIN tile of each card

**Expected Result:**
> NRIC shows ***** + last 4 characters; full NRIC is not visible

**Actual Result:**
> As expected

---

#### `TC-015`: Verify clicking a child name opens that child's transactions

- **Scenario ID**: `TS-002`
- **Test Suite**: Home
- **Page / Target**: `Home page`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Passed` | **Test Type**: `Functional`
- **Traceability**: TBC
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_HOME_06
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
```

**Test Data:**
```text
Student: Nur Aisyah
```

**Test Steps:**
1. Open Home (/)
2. Click the name 'Nur Aisyah'

**Expected Result:**
> Transactions page opens with ?student=<id>; Student filter shows 'Nur Aisyah (S01)'

**Actual Result:**
> As expected

---

#### `TC-016`: Verify card subtitle shows the child's age as a number

- **Scenario ID**: `TS-002`
- **Test Suite**: Home
- **Page / Target**: `Home page`
- **Severity / Priority**: `S4 (lowest)` / `Low`
- **Execution Status**: `Failed` | **Test Type**: `UI`
- **Linked Defect ID**: `BUG-010`
- **Traceability**: TBC
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Assumption Reference**: Age should be shown as a number (key has a placeholder in vi-VN)
- **Note**: Auto: TC_HOME_07
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
```

**Test Data:**
```text
-
```

**Test Steps:**
1. Open Home (/)
2. Check the subtitle under 'Nur Aisyah'

**Expected Result:**
> Subtitle shows code and age, e.g. 'S01 · Age 14'

**Actual Result:**
> Subtitle shows 'S01 · Age' without a number

---


### Test Suite: My Profile

#### `TC-017`: Verify My Profile shows Singpass identity, contact and mailing cards

- **Scenario ID**: `TS-003`
- **Test Suite**: My Profile
- **Page / Target**: `My Profile page`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Passed` | **Test Type**: `Functional`
- **Traceability**: R8
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_PRF_01
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
```

**Test Data:**
```text
-
```

**Test Steps:**
1. Click [My Profile] in the menu

**Expected Result:**
> 3 cards shown: Singpass verified identity (read-only), Contact information, Mailing address. Full Name = Parent of Nur Aisyah; Email = s8411053a@singpass.local; Mobile = 8 digits or 'Not provided'

**Actual Result:**
> As expected

---

#### `TC-018`: Verify NRIC is masked and can be shown / hidden

- **Scenario ID**: `TS-003`
- **Test Suite**: My Profile
- **Page / Target**: `My Profile page`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Passed` | **Test Type**: `Security`
- **Traceability**: R8
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_PRF_02
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
```

**Test Data:**
```text
-
```

**Test Steps:**
1. Open My Profile
2. Click [Show NRIC]
3. Click [Hide NRIC]

**Expected Result:**
> Default shows *****053A; after Show: S8411053A; after Hide: *****053A again

**Actual Result:**
> As expected

---

#### `TC-019`: Verify residential address comes from Singpass

- **Scenario ID**: `TS-003`
- **Test Suite**: My Profile
- **Page / Target**: `My Profile page`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Passed` | **Test Type**: `Functional`
- **Traceability**: R8
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_PRF_03
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
```

**Test Data:**
```text
-
```

**Test Steps:**
1. Open My Profile
2. Check 'Residential address (from Singpass / NRIC)'

**Expected Result:**
> Address contains 101, Clementi Avenue 3, 650013

---

#### `TC-020`: Verify residential address shows floor and unit like Singpass

- **Scenario ID**: `TS-003`
- **Test Suite**: My Profile
- **Page / Target**: `My Profile page`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Failed` | **Test Type**: `Functional`
- **Linked Defect ID**: `BUG-009`
- **Traceability**: R8
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Assumption Reference**: Format follows Home page: #floor-unit
- **Note**: Auto: TC_PRF_04
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
```

**Test Data:**
```text
Singpass regadd: floor 04, unit 11
```

**Test Steps:**
1. Open My Profile
2. Check the residential address

**Expected Result:**
> Address shows '#04-11' (same as Home page)

**Actual Result:**
> Address shows 'Blk 101 Clementi Avenue 3 #11, SINGAPORE 650013' (floor 04 missing)

---

#### `TC-021`: Verify [Update details] opens the form with saved values and Save disabled

- **Scenario ID**: `TS-003`
- **Test Suite**: My Profile
- **Page / Target**: `My Profile – edit`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Passed` | **Test Type**: `Functional`
- **Traceability**: R8
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_PRF_05
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
```

**Test Data:**
```text
-
```

**Test Steps:**
1. Open My Profile
2. Click [Update details]

**Expected Result:**
> Note 'Only your contact details and mailing address can be changed here.' and 'Make a change to enable saving.' shown; [Save changes] disabled; identity has no input; Email is prefilled; Mobile and Email marked required (*)

**Actual Result:**
> As expected

---

#### `TC-022`: Verify focus moves to Mobile Number when editing starts

- **Scenario ID**: `TS-003`
- **Test Suite**: My Profile
- **Page / Target**: `My Profile – edit`
- **Severity / Priority**: `S4 (lowest)` / `Low`
- **Execution Status**: `Passed` | **Test Type**: `UI`
- **Traceability**: R8
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_PRF_06
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
```

**Test Data:**
```text
-
```

**Test Steps:**
1. Open My Profile
2. Click [Update details]

**Expected Result:**
> Cursor is in the Mobile Number field

**Actual Result:**
> As expected

---

#### `TC-023`: Verify edit form shows the Mailing address card only once

- **Scenario ID**: `TS-003`
- **Test Suite**: My Profile
- **Page / Target**: `My Profile – edit`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Failed` | **Test Type**: `UI`
- **Linked Defect ID**: `BUG-001`
- **Traceability**: R8
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_PRF_07
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
```

**Test Data:**
```text
-
```

**Test Steps:**
1. Open My Profile
2. Click [Update details]
3. Count the 'Mailing address' cards

**Expected Result:**
> Only 1 Mailing address card is shown

**Actual Result:**
> 2 'Mailing address' cards are shown in the edit form

---

#### `TC-024`: Verify [Cancel] leaves edit mode without saving

- **Scenario ID**: `TS-003`
- **Test Suite**: My Profile
- **Page / Target**: `My Profile – edit`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Passed` | **Test Type**: `Functional`
- **Traceability**: R8
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_PRF_08
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
Parent is on My Profile and has clicked [Update details].
```

**Test Data:**
```text
Unit: 99
```

**Test Steps:**
1. Change Unit to 99
2. Click [Cancel]
3. Click [Update details] again

**Expected Result:**
> Form closes; focus returns to [Update details]; no update request is sent; Unit is not 99

**Actual Result:**
> As expected

---

#### `TC-025`: Verify [Save changes] is enabled after a change and disabled when the change is undone

- **Scenario ID**: `TS-003`
- **Test Suite**: My Profile
- **Page / Target**: `My Profile – edit`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Passed` | **Test Type**: `Functional`
- **Traceability**: R8
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_PRF_09
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
Parent is on My Profile and has clicked [Update details].
```

**Test Data:**
```text
Unit: 77 then original value
```

**Test Steps:**
1. Change Unit to 77
2. Change Unit back to the original value

**Expected Result:**
> After step 1 [Save changes] is enabled and the 'Make a change' note is hidden; after step 2 [Save changes] is disabled

**Actual Result:**
> As expected

---

#### `TC-026`: Verify spaces around a value are trimmed when leaving the field

- **Scenario ID**: `TS-003`
- **Test Suite**: My Profile
- **Page / Target**: `My Profile – edit`
- **Severity / Priority**: `S4 (lowest)` / `Low`
- **Execution Status**: `Passed` | **Test Type**: `Functional`
- **Traceability**: R8
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_PRF_10
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
Parent is on My Profile and has clicked [Update details].
```

**Test Data:**
```text
Street: ' Clementi Avenue 3 '
```

**Test Steps:**
1. Enter the street with spaces
2. Leave the field

**Expected Result:**
> Value becomes 'Clementi Avenue 3'

**Actual Result:**
> As expected

---

#### `TC-027`: Verify valid change opens the confirm dialog and [Keep editing] keeps the change

- **Scenario ID**: `TS-003`
- **Test Suite**: My Profile
- **Page / Target**: `My Profile – edit`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Passed` | **Test Type**: `Functional`
- **Traceability**: R8
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_PRF_11
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
Parent is on My Profile and has clicked [Update details].
```

**Test Data:**
```text
Unit: 12
```

**Test Steps:**
1. Change Unit to 12
2. Click [Save changes]
3. Click [Keep editing]

**Expected Result:**
> Dialog 'Save your changes?' with 'Your contact details and mailing address will be updated.' is shown; after Keep editing the dialog closes, Unit is still 12, no update request is sent

**Actual Result:**
> As expected

---

#### `TC-028`: Verify save failure shows MSG-0808

- **Scenario ID**: `TS-003`
- **Test Suite**: My Profile
- **Page / Target**: `My Profile – edit`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Failed` | **Test Type**: `Functional`
- **Linked Defect ID**: `BUG-008`
- **Traceability**: R8 / FS08 Save behavior
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Assumption Reference**: API failure is simulated with a mocked 500 response
- **Note**: Auto: TC_PRF_12
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
Parent is on My Profile and has clicked [Update details].
Backend update API returns HTTP 500 (mocked).
```

**Test Data:**
```text
Unit: 13
```

**Test Steps:**
1. Change Unit to 13
2. Click [Save changes]
3. Click [Save changes] in the dialog

**Expected Result:**
> Dialog stays open and shows MSG-0808: 'We could not update your details. Please try again.'

**Actual Result:**
> Dialog shows 'A server error occurred. Please try again later.' instead of MSG-0808

---

#### `TC-029`: Verify successful save shows MSG-0807

- **Scenario ID**: `TS-003`
- **Test Suite**: My Profile
- **Page / Target**: `My Profile – edit`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Blocked` | **Test Type**: `Functional`
- **Traceability**: R8 / FS08 Save behavior
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Assumption Reference**: API success is simulated so test data is not changed
- **Note**: Auto: TC_PRF_13
Script issue: mocked API response used 'success' instead of 'isSuccess', so the app treated it as a failure. Fixed in script – re-run.
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
Parent is on My Profile and has clicked [Update details].
Backend update API returns success (mocked).
```

**Test Data:**
```text
Unit: 14
```

**Test Steps:**
1. Change Unit to 14
2. Click [Save changes]
3. Click [Save changes] in the dialog

**Expected Result:**
> Dialog closes; MSG-0807 'Your details have been updated.' is shown; [Update details] is shown again

---

#### `TC-030`: Verify mobile number is saved and shown after reload

- **Scenario ID**: `TS-003`
- **Test Suite**: My Profile
- **Page / Target**: `My Profile – edit`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: R8
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Assumption Reference**: Changes real test data
- **Note**: Auto: TC_PRF_14
Skipped by config (see README: ALLOW_DATA_CHANGE / PARENT_NRIC_ALL_CHILDREN_16_PLUS)
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
Parent is on My Profile and has clicked [Update details].
Run only with ALLOW_DATA_CHANGE=true.
```

**Test Data:**
```text
Mobile: 91234567 (or 81234567 if already 91234567)
```

**Test Steps:**
1. Enter the new mobile number
2. Click [Save changes]
3. Click [Save changes] in the dialog
4. Reload the page

**Expected Result:**
> Update API returns success; MSG-0807 shown; view mode and page after reload show the new number

---

#### `TC-031`: Verify profile is read-only when all linked children are 16 or older

- **Scenario ID**: `TS-003`
- **Test Suite**: My Profile
- **Page / Target**: `My Profile page`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R8 / FS08 Save behavior
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Assumption Reference**: Read-only = no [Update details] button
- **Note**: Auto: TC_PRF_15
Skipped by config (see README: ALLOW_DATA_CHANGE / PARENT_NRIC_ALL_CHILDREN_16_PLUS)
Run: 23/10/2026

**Preconditions:**
```text
Parent whose linked children are all 16+ is logged in (PARENT_NRIC_ALL_CHILDREN_16_PLUS).
```

**Test Data:**
```text
Persona: TBC
```

**Test Steps:**
1. Log in with the persona
2. Open My Profile

**Expected Result:**
> [Update details] is not shown

---


### Test Suite: Profile Validation (R8)

#### `TC-032`: Verify Mobile Number – blank shows an error

- **Scenario ID**: `TS-004`
- **Test Suite**: Profile Validation (R8)
- **Page / Target**: `My Profile – edit`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Failed` | **Test Type**: `Functional`
- **Linked Defect ID**: `BUG-003`
- **Traceability**: R8 / FS08 Field rules – Mobile Number
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Assumption Reference**: Blank is tested by clearing the field and clicking Save directly
- **Note**: Auto: TC_R8_01
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
Parent is on My Profile and has clicked [Update details].
```

**Test Data:**
```text
Mobile Number: (empty)
```

**Test Steps:**
1. Change Unit to 12 (so Save is enabled)
2. Clear Mobile Number
3. Click [Save changes] (without leaving the field)

**Expected Result:**
> Message 'MSG-0001: Enter your mobile number' is shown under Mobile Number; field is marked invalid; confirm dialog does not open (no update)

**Actual Result:**
> No error message is shown; Save is not blocked by this rule

---

#### `TC-033`: Verify Mobile Number – 7 digits shows an error

- **Scenario ID**: `TS-004`
- **Test Suite**: Profile Validation (R8)
- **Page / Target**: `My Profile – edit`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Failed` | **Test Type**: `Functional`
- **Linked Defect ID**: `BUG-002`
- **Traceability**: R8 / FS08 Field rules – Mobile Number
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_R8_02
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
Parent is on My Profile and has clicked [Update details].
```

**Test Data:**
```text
Mobile Number: 9123456
```

**Test Steps:**
1. Enter the value in Mobile Number
2. Leave the field
3. Click [Save changes]

**Expected Result:**
> Message 'MSG-0805: Enter a mobile number in the correct format, like 9123 4567' is shown under Mobile Number; field is marked invalid; confirm dialog does not open (no update)

**Actual Result:**
> No error message is shown; Save is not blocked by this rule

---

#### `TC-034`: Verify Mobile Number – 9 digits shows an error

- **Scenario ID**: `TS-004`
- **Test Suite**: Profile Validation (R8)
- **Page / Target**: `My Profile – edit`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Failed` | **Test Type**: `Functional`
- **Linked Defect ID**: `BUG-002`
- **Traceability**: R8 / FS08 Field rules – Mobile Number
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_R8_03
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
Parent is on My Profile and has clicked [Update details].
```

**Test Data:**
```text
Mobile Number: 912345678
```

**Test Steps:**
1. Enter the value in Mobile Number
2. Leave the field
3. Click [Save changes]

**Expected Result:**
> Message 'MSG-0805: Enter a mobile number in the correct format, like 9123 4567' is shown under Mobile Number; field is marked invalid; confirm dialog does not open (no update)

**Actual Result:**
> No error message is shown; Save is not blocked by this rule

---

#### `TC-035`: Verify Mobile Number – starts with 7 shows an error

- **Scenario ID**: `TS-004`
- **Test Suite**: Profile Validation (R8)
- **Page / Target**: `My Profile – edit`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Failed` | **Test Type**: `Functional`
- **Linked Defect ID**: `BUG-002`
- **Traceability**: R8 / FS08 Field rules – Mobile Number
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_R8_04
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
Parent is on My Profile and has clicked [Update details].
```

**Test Data:**
```text
Mobile Number: 71234567
```

**Test Steps:**
1. Enter the value in Mobile Number
2. Leave the field
3. Click [Save changes]

**Expected Result:**
> Message 'MSG-0805: Enter a mobile number in the correct format, like 9123 4567' is shown under Mobile Number; field is marked invalid; confirm dialog does not open (no update)

**Actual Result:**
> No error message is shown; Save is not blocked by this rule

---

#### `TC-036`: Verify Mobile Number – starts with 1 shows an error

- **Scenario ID**: `TS-004`
- **Test Suite**: Profile Validation (R8)
- **Page / Target**: `My Profile – edit`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Failed` | **Test Type**: `Functional`
- **Linked Defect ID**: `BUG-002`
- **Traceability**: R8 / FS08 Field rules – Mobile Number
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_R8_05
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
Parent is on My Profile and has clicked [Update details].
```

**Test Data:**
```text
Mobile Number: 11234567
```

**Test Steps:**
1. Enter the value in Mobile Number
2. Leave the field
3. Click [Save changes]

**Expected Result:**
> Message 'MSG-0805: Enter a mobile number in the correct format, like 9123 4567' is shown under Mobile Number; field is marked invalid; confirm dialog does not open (no update)

**Actual Result:**
> No error message is shown; Save is not blocked by this rule

---

#### `TC-037`: Verify Mobile Number – with letters shows an error

- **Scenario ID**: `TS-004`
- **Test Suite**: Profile Validation (R8)
- **Page / Target**: `My Profile – edit`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Failed` | **Test Type**: `Functional`
- **Linked Defect ID**: `BUG-002`
- **Traceability**: R8 / FS08 Field rules – Mobile Number
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_R8_06
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
Parent is on My Profile and has clicked [Update details].
```

**Test Data:**
```text
Mobile Number: 9123abcd
```

**Test Steps:**
1. Enter the value in Mobile Number
2. Leave the field
3. Click [Save changes]

**Expected Result:**
> Message 'MSG-0805: Enter a mobile number in the correct format, like 9123 4567' is shown under Mobile Number; field is marked invalid; confirm dialog does not open (no update)

**Actual Result:**
> No error message is shown; Save is not blocked by this rule

---

#### `TC-038`: Verify Mobile Number – with symbols shows an error

- **Scenario ID**: `TS-004`
- **Test Suite**: Profile Validation (R8)
- **Page / Target**: `My Profile – edit`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Failed` | **Test Type**: `Functional`
- **Linked Defect ID**: `BUG-002`
- **Traceability**: R8 / FS08 Field rules – Mobile Number
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_R8_07
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
Parent is on My Profile and has clicked [Update details].
```

**Test Data:**
```text
Mobile Number: +6591234
```

**Test Steps:**
1. Enter the value in Mobile Number
2. Leave the field
3. Click [Save changes]

**Expected Result:**
> Message 'MSG-0805: Enter a mobile number in the correct format, like 9123 4567' is shown under Mobile Number; field is marked invalid; confirm dialog does not open (no update)

**Actual Result:**
> No error message is shown; Save is not blocked by this rule

---

#### `TC-039`: Verify Mobile Number – valid, starts with 9 is accepted

- **Scenario ID**: `TS-004`
- **Test Suite**: Profile Validation (R8)
- **Page / Target**: `My Profile – edit`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Passed` | **Test Type**: `Functional`
- **Traceability**: R8 / FS08 Field rules – Mobile Number
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_R8_08
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
Parent is on My Profile and has clicked [Update details].
```

**Test Data:**
```text
Mobile Number: 91234567
```

**Test Steps:**
1. Enter the value in Mobile Number
2. Leave the field
3. Click [Save changes]

**Expected Result:**
> No error under Mobile Number; confirm dialog 'Save your changes?' opens

**Actual Result:**
> As expected

---

#### `TC-040`: Verify Mobile Number – valid, starts with 8 is accepted

- **Scenario ID**: `TS-004`
- **Test Suite**: Profile Validation (R8)
- **Page / Target**: `My Profile – edit`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Passed` | **Test Type**: `Functional`
- **Traceability**: R8 / FS08 Field rules – Mobile Number
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_R8_09
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
Parent is on My Profile and has clicked [Update details].
```

**Test Data:**
```text
Mobile Number: 81234567
```

**Test Steps:**
1. Enter the value in Mobile Number
2. Leave the field
3. Click [Save changes]

**Expected Result:**
> No error under Mobile Number; confirm dialog 'Save your changes?' opens

**Actual Result:**
> As expected

---

#### `TC-041`: Verify Mobile Number – valid, starts with 6 is accepted

- **Scenario ID**: `TS-004`
- **Test Suite**: Profile Validation (R8)
- **Page / Target**: `My Profile – edit`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Passed` | **Test Type**: `Functional`
- **Traceability**: R8 / FS08 Field rules – Mobile Number
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_R8_10
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
Parent is on My Profile and has clicked [Update details].
```

**Test Data:**
```text
Mobile Number: 61234567
```

**Test Steps:**
1. Enter the value in Mobile Number
2. Leave the field
3. Click [Save changes]

**Expected Result:**
> No error under Mobile Number; confirm dialog 'Save your changes?' opens

**Actual Result:**
> As expected

---

#### `TC-042`: Verify Email – blank shows an error

- **Scenario ID**: `TS-004`
- **Test Suite**: Profile Validation (R8)
- **Page / Target**: `My Profile – edit`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Failed` | **Test Type**: `Functional`
- **Linked Defect ID**: `BUG-003`
- **Traceability**: R8 / FS08 Field rules – Email
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Assumption Reference**: Blank is tested by clearing the field and clicking Save directly
- **Note**: Auto: TC_R8_11
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
Parent is on My Profile and has clicked [Update details].
```

**Test Data:**
```text
Email: (empty)
```

**Test Steps:**
1. Change Unit to 12 (so Save is enabled)
2. Clear Email
3. Click [Save changes] (without leaving the field)

**Expected Result:**
> Message 'MSG-0001: Enter your email' is shown under Email; field is marked invalid; confirm dialog does not open (no update)

**Actual Result:**
> No error message is shown; Save is not blocked by this rule

---

#### `TC-043`: Verify Email – without @ shows an error

- **Scenario ID**: `TS-004`
- **Test Suite**: Profile Validation (R8)
- **Page / Target**: `My Profile – edit`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Failed` | **Test Type**: `Functional`
- **Linked Defect ID**: `BUG-004`
- **Traceability**: R8 / FS08 Field rules – Email
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_R8_12
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
Parent is on My Profile and has clicked [Update details].
```

**Test Data:**
```text
Email: parent.example.com
```

**Test Steps:**
1. Enter the value in Email
2. Leave the field
3. Click [Save changes]

**Expected Result:**
> Message 'MSG-0806: Enter an email address in the correct format, like name@example.com' is shown under Email; field is marked invalid; confirm dialog does not open (no update)

**Actual Result:**
> Message shown: 'Enter a valid email address.'

---

#### `TC-044`: Verify Email – without domain shows an error

- **Scenario ID**: `TS-004`
- **Test Suite**: Profile Validation (R8)
- **Page / Target**: `My Profile – edit`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Failed` | **Test Type**: `Functional`
- **Linked Defect ID**: `BUG-004`
- **Traceability**: R8 / FS08 Field rules – Email
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_R8_13
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
Parent is on My Profile and has clicked [Update details].
```

**Test Data:**
```text
Email: parent@
```

**Test Steps:**
1. Enter the value in Email
2. Leave the field
3. Click [Save changes]

**Expected Result:**
> Message 'MSG-0806: Enter an email address in the correct format, like name@example.com' is shown under Email; field is marked invalid; confirm dialog does not open (no update)

**Actual Result:**
> Message shown: 'Enter a valid email address.'

---

#### `TC-045`: Verify Email – without dot in domain shows an error

- **Scenario ID**: `TS-004`
- **Test Suite**: Profile Validation (R8)
- **Page / Target**: `My Profile – edit`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Failed` | **Test Type**: `Functional`
- **Linked Defect ID**: `BUG-004`
- **Traceability**: R8 / FS08 Field rules – Email
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_R8_14
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
Parent is on My Profile and has clicked [Update details].
```

**Test Data:**
```text
Email: parent@example
```

**Test Steps:**
1. Enter the value in Email
2. Leave the field
3. Click [Save changes]

**Expected Result:**
> Message 'MSG-0806: Enter an email address in the correct format, like name@example.com' is shown under Email; field is marked invalid; confirm dialog does not open (no update)

**Actual Result:**
> Message shown: 'Enter a valid email address.'

---

#### `TC-046`: Verify Email – with space shows an error

- **Scenario ID**: `TS-004`
- **Test Suite**: Profile Validation (R8)
- **Page / Target**: `My Profile – edit`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Failed` | **Test Type**: `Functional`
- **Linked Defect ID**: `BUG-004`
- **Traceability**: R8 / FS08 Field rules – Email
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_R8_15
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
Parent is on My Profile and has clicked [Update details].
```

**Test Data:**
```text
Email: par ent@example.com
```

**Test Steps:**
1. Enter the value in Email
2. Leave the field
3. Click [Save changes]

**Expected Result:**
> Message 'MSG-0806: Enter an email address in the correct format, like name@example.com' is shown under Email; field is marked invalid; confirm dialog does not open (no update)

**Actual Result:**
> Message shown: 'Enter a valid email address.'

---

#### `TC-047`: Verify Email – 151 characters shows an error

- **Scenario ID**: `TS-004`
- **Test Suite**: Profile Validation (R8)
- **Page / Target**: `My Profile – edit`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Failed` | **Test Type**: `Functional`
- **Linked Defect ID**: `BUG-005`
- **Traceability**: R8 / FS08 Field rules – Email
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_R8_16
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
Parent is on My Profile and has clicked [Update details].
```

**Test Data:**
```text
Email: 'a' x 139 + '@example.com' (151 chars)
```

**Test Steps:**
1. Enter the value in Email
2. Leave the field
3. Click [Save changes]

**Expected Result:**
> Message 'MSG-0806: Enter an email address in the correct format, like name@example.com' is shown under Email; field is marked invalid; confirm dialog does not open (no update)

**Actual Result:**
> No error message is shown; Save is not blocked by this rule

---

#### `TC-048`: Verify Email – exactly 150 characters is accepted

- **Scenario ID**: `TS-004`
- **Test Suite**: Profile Validation (R8)
- **Page / Target**: `My Profile – edit`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Passed` | **Test Type**: `Functional`
- **Traceability**: R8 / FS08 Field rules – Email
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_R8_17
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
Parent is on My Profile and has clicked [Update details].
```

**Test Data:**
```text
Email: 'a' x 138 + '@example.com' (150 chars)
```

**Test Steps:**
1. Enter the value in Email
2. Leave the field
3. Click [Save changes]

**Expected Result:**
> No error under Email; confirm dialog 'Save your changes?' opens

**Actual Result:**
> As expected

---

#### `TC-049`: Verify Email – valid is accepted

- **Scenario ID**: `TS-004`
- **Test Suite**: Profile Validation (R8)
- **Page / Target**: `My Profile – edit`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Passed` | **Test Type**: `Functional`
- **Traceability**: R8 / FS08 Field rules – Email
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_R8_18
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
Parent is on My Profile and has clicked [Update details].
```

**Test Data:**
```text
Email: parent.test@example.com
```

**Test Steps:**
1. Enter the value in Email
2. Leave the field
3. Click [Save changes]

**Expected Result:**
> No error under Email; confirm dialog 'Save your changes?' opens

**Actual Result:**
> As expected

---

#### `TC-050`: Verify Mailing Block – 21 characters shows an error

- **Scenario ID**: `TS-004`
- **Test Suite**: Profile Validation (R8)
- **Page / Target**: `My Profile – edit`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Failed` | **Test Type**: `Functional`
- **Linked Defect ID**: `BUG-006`
- **Traceability**: R8 / FS08 Field rules – Mailing Block
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Assumption Reference**: Message wording is assumed (not defined in message_R8.txt)
- **Note**: Auto: TC_R8_19
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
Parent is on My Profile and has clicked [Update details].
```

**Test Data:**
```text
Mailing Block: '1' x 21
```

**Test Steps:**
1. Enter the value in Mailing Block
2. Leave the field
3. Click [Save changes]

**Expected Result:**
> Message 'Enter no more than 20 characters.' is shown under Mailing Block; field is marked invalid; confirm dialog does not open (no update)

**Actual Result:**
> No error message is shown; Save is not blocked by this rule

---

#### `TC-051`: Verify Mailing Block – exactly 20 characters is accepted

- **Scenario ID**: `TS-004`
- **Test Suite**: Profile Validation (R8)
- **Page / Target**: `My Profile – edit`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Passed` | **Test Type**: `Functional`
- **Traceability**: R8 / FS08 Field rules – Mailing Block
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_R8_20
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
Parent is on My Profile and has clicked [Update details].
```

**Test Data:**
```text
Mailing Block: '1' x 20
```

**Test Steps:**
1. Enter the value in Mailing Block
2. Leave the field
3. Click [Save changes]

**Expected Result:**
> No error under Mailing Block; confirm dialog 'Save your changes?' opens

**Actual Result:**
> As expected

---

#### `TC-052`: Verify Mailing Street – blank shows an error

- **Scenario ID**: `TS-004`
- **Test Suite**: Profile Validation (R8)
- **Page / Target**: `My Profile – edit`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Failed` | **Test Type**: `Functional`
- **Linked Defect ID**: `BUG-003`
- **Traceability**: R8 / FS08 Field rules – Mailing Street
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Assumption Reference**: Blank is tested by clearing the field and clicking Save directly
- **Note**: Auto: TC_R8_21
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
Parent is on My Profile and has clicked [Update details].
```

**Test Data:**
```text
Mailing Street: (empty)
```

**Test Steps:**
1. Change Unit to 12 (so Save is enabled)
2. Clear Mailing Street
3. Click [Save changes] (without leaving the field)

**Expected Result:**
> Message 'MSG-0001: Enter your mailing street' is shown under Mailing Street; field is marked invalid; confirm dialog does not open (no update)

**Actual Result:**
> No error message is shown; Save is not blocked by this rule

---

#### `TC-053`: Verify Mailing Street – 101 characters shows an error

- **Scenario ID**: `TS-004`
- **Test Suite**: Profile Validation (R8)
- **Page / Target**: `My Profile – edit`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Failed` | **Test Type**: `Functional`
- **Linked Defect ID**: `BUG-006`
- **Traceability**: R8 / FS08 Field rules – Mailing Street
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Assumption Reference**: Message wording is assumed (not defined in message_R8.txt)
- **Note**: Auto: TC_R8_22
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
Parent is on My Profile and has clicked [Update details].
```

**Test Data:**
```text
Mailing Street: 'S' x 101
```

**Test Steps:**
1. Enter the value in Mailing Street
2. Leave the field
3. Click [Save changes]

**Expected Result:**
> Message 'Enter no more than 100 characters.' is shown under Mailing Street; field is marked invalid; confirm dialog does not open (no update)

**Actual Result:**
> No error message is shown; Save is not blocked by this rule

---

#### `TC-054`: Verify Mailing Street – exactly 100 characters is accepted

- **Scenario ID**: `TS-004`
- **Test Suite**: Profile Validation (R8)
- **Page / Target**: `My Profile – edit`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Passed` | **Test Type**: `Functional`
- **Traceability**: R8 / FS08 Field rules – Mailing Street
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_R8_23
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
Parent is on My Profile and has clicked [Update details].
```

**Test Data:**
```text
Mailing Street: 'S' x 100
```

**Test Steps:**
1. Enter the value in Mailing Street
2. Leave the field
3. Click [Save changes]

**Expected Result:**
> No error under Mailing Street; confirm dialog 'Save your changes?' opens

**Actual Result:**
> As expected

---

#### `TC-055`: Verify Mailing Unit – 21 characters shows an error

- **Scenario ID**: `TS-004`
- **Test Suite**: Profile Validation (R8)
- **Page / Target**: `My Profile – edit`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Failed` | **Test Type**: `Functional`
- **Linked Defect ID**: `BUG-006`
- **Traceability**: R8 / FS08 Field rules – Mailing Unit
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Assumption Reference**: Message wording is assumed (not defined in message_R8.txt)
- **Note**: Auto: TC_R8_24
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
Parent is on My Profile and has clicked [Update details].
```

**Test Data:**
```text
Mailing Unit: '2' x 21
```

**Test Steps:**
1. Enter the value in Mailing Unit
2. Leave the field
3. Click [Save changes]

**Expected Result:**
> Message 'Enter no more than 20 characters.' is shown under Mailing Unit; field is marked invalid; confirm dialog does not open (no update)

**Actual Result:**
> No error message is shown; Save is not blocked by this rule

---

#### `TC-056`: Verify Mailing Unit – exactly 20 characters is accepted

- **Scenario ID**: `TS-004`
- **Test Suite**: Profile Validation (R8)
- **Page / Target**: `My Profile – edit`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Passed` | **Test Type**: `Functional`
- **Traceability**: R8 / FS08 Field rules – Mailing Unit
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_R8_25
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
Parent is on My Profile and has clicked [Update details].
```

**Test Data:**
```text
Mailing Unit: '2' x 20
```

**Test Steps:**
1. Enter the value in Mailing Unit
2. Leave the field
3. Click [Save changes]

**Expected Result:**
> No error under Mailing Unit; confirm dialog 'Save your changes?' opens

**Actual Result:**
> As expected

---

#### `TC-057`: Verify Mailing Postal Code – blank shows an error

- **Scenario ID**: `TS-004`
- **Test Suite**: Profile Validation (R8)
- **Page / Target**: `My Profile – edit`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Failed` | **Test Type**: `Functional`
- **Linked Defect ID**: `BUG-003`
- **Traceability**: R8 / FS08 Field rules – Mailing Postal Code
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Assumption Reference**: Blank is tested by clearing the field and clicking Save directly
- **Note**: Auto: TC_R8_26
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
Parent is on My Profile and has clicked [Update details].
```

**Test Data:**
```text
Mailing Postal Code: (empty)
```

**Test Steps:**
1. Change Unit to 12 (so Save is enabled)
2. Clear Mailing Postal Code
3. Click [Save changes] (without leaving the field)

**Expected Result:**
> Message 'MSG-0001: Enter your mailing postal code' is shown under Mailing Postal Code; field is marked invalid; confirm dialog does not open (no update)

**Actual Result:**
> No error message is shown; Save is not blocked by this rule

---

#### `TC-058`: Verify Mailing Postal Code – 5 digits shows an error

- **Scenario ID**: `TS-004`
- **Test Suite**: Profile Validation (R8)
- **Page / Target**: `My Profile – edit`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Failed` | **Test Type**: `Functional`
- **Linked Defect ID**: `BUG-007`
- **Traceability**: R8 / FS08 Field rules – Mailing Postal Code
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Assumption Reference**: Message wording is assumed (not defined in message_R8.txt)
- **Note**: Auto: TC_R8_27
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
Parent is on My Profile and has clicked [Update details].
```

**Test Data:**
```text
Mailing Postal Code: 65001
```

**Test Steps:**
1. Enter the value in Mailing Postal Code
2. Leave the field
3. Click [Save changes]

**Expected Result:**
> Message 'Enter a valid 6-digit postal code.' is shown under Mailing Postal Code; field is marked invalid; confirm dialog does not open (no update)

**Actual Result:**
> No error message is shown; Save is not blocked by this rule

---

#### `TC-059`: Verify Mailing Postal Code – 7 digits shows an error

- **Scenario ID**: `TS-004`
- **Test Suite**: Profile Validation (R8)
- **Page / Target**: `My Profile – edit`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Failed` | **Test Type**: `Functional`
- **Linked Defect ID**: `BUG-007`
- **Traceability**: R8 / FS08 Field rules – Mailing Postal Code
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Assumption Reference**: Message wording is assumed (not defined in message_R8.txt)
- **Note**: Auto: TC_R8_28
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
Parent is on My Profile and has clicked [Update details].
```

**Test Data:**
```text
Mailing Postal Code: 6500131
```

**Test Steps:**
1. Enter the value in Mailing Postal Code
2. Leave the field
3. Click [Save changes]

**Expected Result:**
> Message 'Enter a valid 6-digit postal code.' is shown under Mailing Postal Code; field is marked invalid; confirm dialog does not open (no update)

**Actual Result:**
> No error message is shown; Save is not blocked by this rule

---

#### `TC-060`: Verify Mailing Postal Code – with letters shows an error

- **Scenario ID**: `TS-004`
- **Test Suite**: Profile Validation (R8)
- **Page / Target**: `My Profile – edit`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Failed` | **Test Type**: `Functional`
- **Linked Defect ID**: `BUG-007`
- **Traceability**: R8 / FS08 Field rules – Mailing Postal Code
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Assumption Reference**: Message wording is assumed (not defined in message_R8.txt)
- **Note**: Auto: TC_R8_29
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
Parent is on My Profile and has clicked [Update details].
```

**Test Data:**
```text
Mailing Postal Code: 65A013
```

**Test Steps:**
1. Enter the value in Mailing Postal Code
2. Leave the field
3. Click [Save changes]

**Expected Result:**
> Message 'Enter a valid 6-digit postal code.' is shown under Mailing Postal Code; field is marked invalid; confirm dialog does not open (no update)

**Actual Result:**
> No error message is shown; Save is not blocked by this rule

---

#### `TC-061`: Verify Mailing Postal Code – valid 6 digits is accepted

- **Scenario ID**: `TS-004`
- **Test Suite**: Profile Validation (R8)
- **Page / Target**: `My Profile – edit`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Passed` | **Test Type**: `Functional`
- **Traceability**: R8 / FS08 Field rules – Mailing Postal Code
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_R8_30
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
Parent is on My Profile and has clicked [Update details].
```

**Test Data:**
```text
Mailing Postal Code: 650014
```

**Test Steps:**
1. Enter the value in Mailing Postal Code
2. Leave the field
3. Click [Save changes]

**Expected Result:**
> No error under Mailing Postal Code; confirm dialog 'Save your changes?' opens

**Actual Result:**
> As expected

---

#### `TC-062`: Verify Mailing Country – blank shows an error

- **Scenario ID**: `TS-004`
- **Test Suite**: Profile Validation (R8)
- **Page / Target**: `My Profile – edit`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Failed` | **Test Type**: `Functional`
- **Linked Defect ID**: `BUG-003`
- **Traceability**: R8 / FS08 Field rules – Mailing Country
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Assumption Reference**: Blank is tested by clearing the field and clicking Save directly
- **Note**: Auto: TC_R8_31
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
Parent is on My Profile and has clicked [Update details].
```

**Test Data:**
```text
Mailing Country: (empty)
```

**Test Steps:**
1. Change Unit to 12 (so Save is enabled)
2. Clear Mailing Country
3. Click [Save changes] (without leaving the field)

**Expected Result:**
> Message 'MSG-0001: Enter your mailing country' is shown under Mailing Country; field is marked invalid; confirm dialog does not open (no update)

**Actual Result:**
> No error message is shown; Save is not blocked by this rule

---

#### `TC-063`: Verify Mailing Country – 101 characters shows an error

- **Scenario ID**: `TS-004`
- **Test Suite**: Profile Validation (R8)
- **Page / Target**: `My Profile – edit`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Failed` | **Test Type**: `Functional`
- **Linked Defect ID**: `BUG-006`
- **Traceability**: R8 / FS08 Field rules – Mailing Country
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Assumption Reference**: Message wording is assumed (not defined in message_R8.txt)
- **Note**: Auto: TC_R8_32
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
Parent is on My Profile and has clicked [Update details].
```

**Test Data:**
```text
Mailing Country: 'C' x 101
```

**Test Steps:**
1. Enter the value in Mailing Country
2. Leave the field
3. Click [Save changes]

**Expected Result:**
> Message 'Enter no more than 100 characters.' is shown under Mailing Country; field is marked invalid; confirm dialog does not open (no update)

**Actual Result:**
> No error message is shown; Save is not blocked by this rule

---

#### `TC-064`: Verify Mailing Country – exactly 100 characters is accepted

- **Scenario ID**: `TS-004`
- **Test Suite**: Profile Validation (R8)
- **Page / Target**: `My Profile – edit`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Passed` | **Test Type**: `Functional`
- **Traceability**: R8 / FS08 Field rules – Mailing Country
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_R8_33
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
Parent is on My Profile and has clicked [Update details].
```

**Test Data:**
```text
Mailing Country: 'C' x 100
```

**Test Steps:**
1. Enter the value in Mailing Country
2. Leave the field
3. Click [Save changes]

**Expected Result:**
> No error under Mailing Country; confirm dialog 'Save your changes?' opens

**Actual Result:**
> As expected

---

#### `TC-065`: Verify several invalid fields show all messages at the same time

- **Scenario ID**: `TS-004`
- **Test Suite**: Profile Validation (R8)
- **Page / Target**: `My Profile – edit`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Failed` | **Test Type**: `Functional`
- **Linked Defect ID**: `BUG-002`
- **Traceability**: R8 / FS08 Save behavior
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Assumption Reference**: Message wording is assumed (not defined in message_R8.txt)
- **Note**: Auto: TC_R8_34
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
Parent is on My Profile and has clicked [Update details].
```

**Test Data:**
```text
Mobile: 123; Email: wrong-email; Postal code: 12
```

**Test Steps:**
1. Enter the 3 invalid values
2. Click [Save changes]

**Expected Result:**
> MSG-0805 under Mobile, MSG-0806 under Email, 'Enter a valid 6-digit postal code.' under Postal code; dialog does not open

**Actual Result:**
> No message under Mobile Number and Postal code; only Email shows 'Enter a valid email address.'

---

#### `TC-066`: Verify error message clears when the user types again

- **Scenario ID**: `TS-004`
- **Test Suite**: Profile Validation (R8)
- **Page / Target**: `My Profile – edit`
- **Severity / Priority**: `S4 (lowest)` / `Low`
- **Execution Status**: `Passed` | **Test Type**: `UI`
- **Traceability**: R8
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_R8_35
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
Parent is on My Profile and has clicked [Update details].
```

**Test Data:**
```text
Email: wrong-email then parent@example.com
```

**Test Steps:**
1. Enter wrong-email in Email
2. Click [Save changes]
3. Type parent@example.com

**Expected Result:**
> Error shows after step 2 and disappears after step 3

**Actual Result:**
> As expected

---

#### `TC-067`: Verify all valid fields together open the confirm dialog

- **Scenario ID**: `TS-004`
- **Test Suite**: Profile Validation (R8)
- **Page / Target**: `My Profile – edit`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Passed` | **Test Type**: `Functional`
- **Traceability**: R8
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_R8_36
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
Parent is on My Profile and has clicked [Update details].
```

**Test Data:**
```text
Mobile 91234567; Email parent.valid@example.com; Block 101; Street Clementi Avenue 3; Unit 04-11; Postal 650013; Country SINGAPORE
```

**Test Steps:**
1. Enter all values
2. Click [Save changes]

**Expected Result:**
> No error; confirm dialog opens

**Actual Result:**
> As expected

---


### Test Suite: Transactions

#### `TC-068`: Verify Transactions page shows title, description and student filter

- **Scenario ID**: `TS-005`
- **Test Suite**: Transactions
- **Page / Target**: `Transactions page`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Passed` | **Test Type**: `UI`
- **Traceability**: TBC
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_TXN_01
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
```

**Test Data:**
```text
-
```

**Test Steps:**
1. Click [Transactions] in the menu

**Expected Result:**
> Title 'Transactions manage', description 'Official statement of ledger balances and transaction history.'; filter options: All students, Nur Iman (X04), Nur Aisyah (S01); default All students

**Actual Result:**
> As expected

---

#### `TC-069`: Verify student summary shows account, masked NRIC and available balance

- **Scenario ID**: `TS-005`
- **Test Suite**: Transactions
- **Page / Target**: `Transactions page`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Passed` | **Test Type**: `Functional`
- **Traceability**: TBC
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_TXN_02
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
```

**Test Data:**
```text
Student filter: Nur Aisyah (S01)
```

**Test Steps:**
1. Open Transactions
2. Select Nur Aisyah (S01)

**Expected Result:**
> Summary shows Nur Aisyah, Active, A/C: EA260001, *****001E, Available balance SGD 1,590.00

**Actual Result:**
> As expected

---

#### `TC-070`: Verify table columns, 10 rows on page 1 and total count

- **Scenario ID**: `TS-005`
- **Test Suite**: Transactions
- **Page / Target**: `Transactions page`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Passed` | **Test Type**: `Functional`
- **Traceability**: TBC
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Assumption Reference**: Seed has 17 transactions for Nur Aisyah
- **Note**: Auto: TC_TXN_03
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
```

**Test Data:**
```text
Student filter: Nur Aisyah (S01)
```

**Test Steps:**
1. Open Transactions
2. Select Nur Aisyah (S01)

**Expected Result:**
> Columns: Date, Description, Amount, Status; 10 rows; '17 total'; Rows per page = 10

**Actual Result:**
> As expected

---

#### `TC-071`: Verify newest transaction is shown first

- **Scenario ID**: `TS-005`
- **Test Suite**: Transactions
- **Page / Target**: `Transactions page`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Passed` | **Test Type**: `Functional`
- **Traceability**: TBC
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_TXN_04
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
```

**Test Data:**
```text
Student filter: Nur Aisyah (S01)
```

**Test Steps:**
1. Open Transactions
2. Select Nur Aisyah (S01)

**Expected Result:**
> First row is TXN-000017; dates are in descending order

**Actual Result:**
> As expected

---

#### `TC-072`: Verify [Next] and [Previous] paging

- **Scenario ID**: `TS-005`
- **Test Suite**: Transactions
- **Page / Target**: `Transactions page`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Passed` | **Test Type**: `Functional`
- **Traceability**: TBC
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_TXN_05
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
```

**Test Data:**
```text
Student filter: Nur Aisyah (S01)
```

**Test Steps:**
1. Select Nur Aisyah (S01)
2. Click [Next]
3. Click [Previous]

**Expected Result:**
> [Previous] disabled on page 1; page 2 shows 7 rows and [Next] disabled; back on page 1 shows 10 rows starting with TXN-000017

**Actual Result:**
> As expected

---

#### `TC-073`: Verify Rows per page 25 shows all transactions on one page

- **Scenario ID**: `TS-005`
- **Test Suite**: Transactions
- **Page / Target**: `Transactions page`
- **Severity / Priority**: `S4 (lowest)` / `Low`
- **Execution Status**: `Passed` | **Test Type**: `Functional`
- **Traceability**: TBC
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_TXN_06
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
```

**Test Data:**
```text
Student filter: Nur Aisyah (S01); Rows per page: 25
```

**Test Steps:**
1. Select Nur Aisyah (S01)
2. Set Rows per page = 25

**Expected Result:**
> 17 rows shown; [Next] disabled

**Actual Result:**
> As expected

---

#### `TC-074`: Verify amount format and status values

- **Scenario ID**: `TS-005`
- **Test Suite**: Transactions
- **Page / Target**: `Transactions page`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Passed` | **Test Type**: `UI`
- **Traceability**: TBC
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_TXN_07
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
```

**Test Data:**
```text
Student filter: Nur Aisyah (S01)
```

**Test Steps:**
1. Select Nur Aisyah (S01)
2. Check Amount and Status columns

**Expected Result:**
> Amount has +/- and 2 decimals (e.g. +20.00); Status is Pending, Completed or Failed

**Actual Result:**
> As expected

---

#### `TC-075`: Verify each row shows a transaction code

- **Scenario ID**: `TS-005`
- **Test Suite**: Transactions
- **Page / Target**: `Transactions page`
- **Severity / Priority**: `S4 (lowest)` / `Low`
- **Execution Status**: `Passed` | **Test Type**: `UI`
- **Traceability**: TBC
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_TXN_08
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
```

**Test Data:**
```text
Student filter: Nur Aisyah (S01)
```

**Test Steps:**
1. Select Nur Aisyah (S01)
2. Check the Description column

**Expected Result:**
> Each row shows a code TXN-xxxxxx

**Actual Result:**
> As expected

---

#### `TC-076`: Verify All students shows the Account holder column

- **Scenario ID**: `TS-005`
- **Test Suite**: Transactions
- **Page / Target**: `Transactions page`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Blocked` | **Test Type**: `Functional`
- **Traceability**: TBC
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_TXN_09
No rows loaded for 'All students' within 15s. Re-run; if it still fails, check if 'All students' data loads slowly or is empty.
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
```

**Test Data:**
```text
Student filter: All students
```

**Test Steps:**
1. Open Transactions (All students)

**Expected Result:**
> Rows load; columns: Date, Account holder, Description, Amount, Status

---

#### `TC-077`: Verify switching back to All students clears the student from the URL

- **Scenario ID**: `TS-005`
- **Test Suite**: Transactions
- **Page / Target**: `Transactions page`
- **Severity / Priority**: `S4 (lowest)` / `Low`
- **Execution Status**: `Passed` | **Test Type**: `Functional`
- **Traceability**: TBC
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_TXN_10
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
```

**Test Data:**
```text
-
```

**Test Steps:**
1. Select Nur Aisyah (S01)
2. Select All students

**Expected Result:**
> URL has no 'student' parameter; student summary is hidden

**Actual Result:**
> As expected

---

#### `TC-078`: Verify unknown student id in the URL falls back to All students

- **Scenario ID**: `TS-005`
- **Test Suite**: Transactions
- **Page / Target**: `Transactions page`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Passed` | **Test Type**: `Security`
- **Traceability**: TBC
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_TXN_11
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
```

**Test Data:**
```text
URL: /transactions?student=00000000-0000-0000-0000-000000000000
```

**Test Steps:**
1. Open the URL

**Expected Result:**
> Filter shows All students; no data of an unknown student is shown

**Actual Result:**
> As expected

---


### Test Suite: Fees & Payments (R9)

#### `TC-079`: Verify account selection lists each child with account code and status

- **Scenario ID**: `TS-006`
- **Test Suite**: Fees & Payments (R9)
- **Page / Target**: `Choose an education account`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Passed` | **Test Type**: `Functional`
- **Traceability**: R9 / F9.1 / SCR-01
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_BIL_01
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
```

**Test Data:**
```text
-
```

**Test Steps:**
1. Click [Fees & Payments] in the menu

**Expected Result:**
> Text 'Select an account to view outstanding fees.'; Nur Iman: Account X04, Status: Active; Nur Aisyah: Account S01, Status: Active; each has 'View fees for <name>' link

**Actual Result:**
> As expected

---

#### `TC-080`: Verify summary cards show outstanding fees, balance and selected total

- **Scenario ID**: `TS-006`
- **Test Suite**: Fees & Payments (R9)
- **Page / Target**: `Pay education charges`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Passed` | **Test Type**: `Functional`
- **Traceability**: R9 / F9.2 / SCR-02
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_BIL_02
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
```

**Test Data:**
```text
Student: Nur Aisyah
```

**Test Steps:**
1. Open Fees & Payments
2. Click 'View fees for Nur Aisyah'

**Expected Result:**
> Text 'Choose the charges you want to include in this payment.'; Education Account balance 1,590.00; Selected total 0.00

**Actual Result:**
> As expected

---

#### `TC-081`: Verify empty state when there are no outstanding charges

- **Scenario ID**: `TS-006`
- **Test Suite**: Fees & Payments (R9)
- **Page / Target**: `Pay education charges`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Blocked` | **Test Type**: `Functional`
- **Traceability**: R9 / AC-02 / SCR-03
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Assumption Reference**: R9 seed lists INV-2026-000101 (27.25) for Nur Aisyah, but the environment shows none – confirm seed status
- **Note**: Auto: TC_BIL_03
Script issue: text 'No outstanding charges' matched 2 elements. Fixed in script (exact match) – re-run.
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
```

**Test Data:**
```text
Student: Nur Aisyah (no outstanding charge)
```

**Test Steps:**
1. Open Fees & Payments
2. Click 'View fees for Nur Aisyah'

**Expected Result:**
> No outstanding charges' and 'There are no outstanding charges for this child.' shown; Outstanding fees 0.00; '0 charge(s) selected'; [Select all] and [Continue] disabled

---

#### `TC-082`: Verify status filter options

- **Scenario ID**: `TS-006`
- **Test Suite**: Fees & Payments (R9)
- **Page / Target**: `Pay education charges`
- **Severity / Priority**: `S4 (lowest)` / `Low`
- **Execution Status**: `Blocked` | **Test Type**: `UI`
- **Traceability**: R9 / SCR-02
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_BIL_04
Script issue: same as TC_BIL_03. Fixed in script – re-run.
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
```

**Test Data:**
```text
Filter: Overdue, Due soon, All statuses
```

**Test Steps:**
1. Open charges of Nur Aisyah
2. Select each filter value

**Expected Result:**
> Options: All statuses, Overdue, Due soon; empty state shown for each

---

#### `TC-083`: Verify invalid account id shows 'Payment context is invalid'

- **Scenario ID**: `TS-006`
- **Test Suite**: Fees & Payments (R9)
- **Page / Target**: `Pay education charges`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Passed` | **Test Type**: `Security`
- **Traceability**: R9 / EX-01 (partly)
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_BIL_05
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
```

**Test Data:**
```text
URL: /billing/not-a-valid-id
```

**Test Steps:**
1. Open the URL
2. Click [Back to home]

**Expected Result:**
> Payment context is invalid' shown; Back to home opens Home

**Actual Result:**
> As expected

---


### Test Suite: Navigation & Language

#### `TC-084`: Verify each menu item opens its page and is marked active

- **Scenario ID**: `TS-007`
- **Test Suite**: Navigation & Language
- **Page / Target**: `Header`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Passed` | **Test Type**: `Functional`
- **Traceability**: TBC
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_NAV_01
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
```

**Test Data:**
```text
-
```

**Test Steps:**
1. Open Home
2. Click My Profile, Transactions, FAS Application, Fees & Payments, Home one by one

**Expected Result:**
> Each click opens the right page (My Profile, Transactions manage, Financial Assistance Scheme application, Choose an education account, EduSave E-Service Portal) and the item is active

**Actual Result:**
> As expected

---

#### `TC-085`: Verify brand name goes back to Home

- **Scenario ID**: `TS-007`
- **Test Suite**: Navigation & Language
- **Page / Target**: `Header`
- **Severity / Priority**: `S4 (lowest)` / `Low`
- **Execution Status**: `Passed` | **Test Type**: `UI`
- **Traceability**: TBC
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_NAV_02
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
```

**Test Data:**
```text
-
```

**Test Steps:**
1. Open My Profile
2. Click 'EduSave E-Service'

**Expected Result:**
> Home page is shown

**Actual Result:**
> As expected

---

#### `TC-086`: Verify unknown page shows 404 with a link back to Home

- **Scenario ID**: `TS-007`
- **Test Suite**: Navigation & Language
- **Page / Target**: `404 page`
- **Severity / Priority**: `S4 (lowest)` / `Low`
- **Execution Status**: `Passed` | **Test Type**: `UI`
- **Traceability**: TBC
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_NAV_03
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
```

**Test Data:**
```text
URL: /this-page-does-not-exist
```

**Test Steps:**
1. Open the URL
2. Click [Back to Home]

**Expected Result:**
> 404 - Page Not Found' shown; link opens Home

**Actual Result:**
> As expected

---

#### `TC-087`: Verify logged-in parent opening the login page is sent to Home

- **Scenario ID**: `TS-007`
- **Test Suite**: Navigation & Language
- **Page / Target**: `Parent Login page`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Passed` | **Test Type**: `Functional`
- **Traceability**: R8
- **Environment**: DEV (dev tunnel qjrntd59-5174)
Chromium headless (Playwright)
Windows
- **Note**: Auto: TC_NAV_04
Run: 23/10/2026

**Preconditions:**
```text
Parent S8411053A (Parent of Nur Aisyah) is logged in via Mockpass.
Linked children: Nur Iman (X04), Nur Aisyah (S01).
```

**Test Data:**
```text
URL: /parent/login
```

**Test Steps:**
1. Open /parent/login while logged in

**Expected Result:**
> Home page is shown

**Actual Result:**
> As expected

---
