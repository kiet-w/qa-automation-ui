# R1: Education Account Lifecycle & Closure — Sprint 1 Test Cases

> **Module**: R1 - Education Account Lifecycle
> **Specification Reference**: [FS-01_Education_Account_Lifecycle.md](file:////home/baudui/Projects/automation-ui/[agile] fs/md/FS document/FS-01_Education_Account_Lifecycle.md)
> **Source Spreadsheet**: `Test Cases + Defect sprint 1.xlsx` (Sheet `R1 TC`)
> **Total Test Cases**: 73

## Executive Test Suite Summary

| Test Suite | Scenario Count | Test Cases | Priorities | Severities |
| :--- | :--- | :--- | :--- | :--- |
| Eligibility and age boundary | 1 (TS-R1-01) | 17 | High, Low, Medium | S2, S3 |
| Data validation and duplicate prevention | 1 (TS-R1-02) | 12 | High, Low, Medium | S2, S3 |
| Job failure, recovery and audit | 1 (TS-R1-03) | 9 | Critical, High, Low, Medium | S1 (highest), S2, S3 |
| Closure and balance handling | 1 (TS-R1-04) | 12 | Critical, High | S1 (highest), S2 |
| Wallet and ledger contracts | 1 (TS-R1-05) | 7 | Critical, High, Low | S1 (highest), S2, S3 |
| Cross-function seams | 1 (TS-R1-06) | 4 | High | S2 |
| Performance, concurrency and volume | 1 (TS-R1-08) | 6 | Critical, High, Medium | S1 (highest), S2, S3 |
| Security and privacy | 1 (TS-R1-07) | 5 | Critical, High | S1 (highest), S2 |
| Wallet precision and financial safety | 1 (TS-R1-05) | 1 | Critical | S1 (highest) |

---

## Quick Reference Index Table

| Test Case ID | Scenario ID | Title | Page / Area | Priority | Severity | Type | Defect ID | Traceability |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| [`TC-R1-001`](#tc-r1-001) | `TS-R1-01` | Create an account on the seventh birthday | Backend job / API | High | S2 | Functional |  | R1 FS v1.2 §1.1.4, §1.1.6 and §1.1.8; tender R1. |
| [`TC-R1-002`](#tc-r1-002) | `TS-R1-01` | Do not create an account before age 7 | Backend job / API | Medium | S3 | Functional |  | R1 FS v1.2 F01-AC04, F01-BR02 and F01 AF02; §2.4. |
| [`TC-R1-003`](#tc-r1-003) | `TS-R1-01` | Initial sync creates an account one day before age 16 | Backend job / API | Medium | S3 | Functional |  | R1 FS v1.2 F01-BR02; §1.1.4. |
| [`TC-R1-004`](#tc-r1-004) | `TS-R1-01` | Do not create an account at age 16 | Backend job / API | High | S2 | Functional |  | R1 FS v1.2 F01-AC05, F01-BR05 and F01 AF02. |
| [`TC-R1-005`](#tc-r1-005) | `TS-R1-01` | Do not create an account above age 16 | Backend job / API | Medium | S3 | Functional |  | R1 FS v1.2 F01-AC05, F01-BR05 and F01 AF02. |
| [`TC-R1-006`](#tc-r1-006) | `TS-R1-01` | Do not create an account for a permanent resident | Backend job / API | High | S2 | Functional |  | R1 FS v1.2 F01-AC03, F01-BR01 and F01 AF01; §2.1; CD-01. |
| [`TC-R1-007`](#tc-r1-007) | `TS-R1-01` | Do not create an account for a foreign student | Backend job / API | High | S2 | Functional |  | R1 FS v1.2 F01-AC03, F01-BR01 and F01 AF01; CD-01. |
| [`TC-R1-008`](#tc-r1-008) | `TS-R1-01` | Evaluate a 29 February DOB on 28 February | Backend job / API | Medium | S3 | Functional |  | R1 FS v1.2 F01-AC14; §1.1.6. |
| [`TC-R1-009`](#tc-r1-009) | `TS-R1-01` | Do not create the leap-year account on 27 February | Backend job / API | Low | S3 | Functional |  | R1 FS v1.2 F01-AC04, F01-AC14; §1.1.6. |
| [`TC-R1-010`](#tc-r1-010) | `TS-R1-01` | Daily sync uses the Singapore processing date | Backend job / API | High | S2 | Functional |  | R1 FS v1.2 F01-AC02; §1.1.2 and §1.1.5. |
| [`TC-R1-011`](#tc-r1-011) | `TS-R1-01` | School enrolment is not required for account creation | Backend job / API | Medium | S3 | Functional |  | R1 FS v1.2 F01-BR02, F01-BR03 and F01-BR04; §2.1; CD-06. |
| [`TC-R1-015`](#tc-r1-015) | `TS-R1-01` | Create an account when no parent identifier is supplied | Backend job / API | Medium | S3 | Functional |  | R1 FS v1.2 F01-AC09 and F01 AF04; §2.1. |
| [`TC-R1-017`](#tc-r1-017) | `TS-R1-02` | Reject a record with no NRIC | Backend job / API | High | S2 | Functional |  | R1 FS v1.2 F01-AC08 and F01 EF02; §1.1.3 and §1.1.9; local security draft SYNC-02. |
| [`TC-R1-018`](#tc-r1-018) | `TS-R1-02` | Reject a record with no full name | Backend job / API | Medium | S3 | Functional |  | R1 FS v1.2 F01-AC08 and F01 EF02; §1.1.3 and §1.1.9. |
| [`TC-R1-019`](#tc-r1-019) | `TS-R1-02` | Reject a future DOB | Backend job / API | High | S2 | Functional |  | R1 FS v1.2 F01-AC08 and F01 EF02; §1.1.3. |
| [`TC-R1-021`](#tc-r1-021) | `TS-R1-02` | Reject an unknown citizenship value | Backend job / API | Medium | S3 | Functional |  | R1 FS v1.2 F01-AC08, F01-BR01 and F01 EF02; §1.1.3. |
| [`TC-R1-022`](#tc-r1-022) | `TS-R1-02` | Reject missing gender when the field is required | Backend job / API | Low | S3 | Functional |  | R1 FS v1.2 F01-AC08 and F01 EF02; §1.1.3 and §2.1. |
| [`TC-R1-023`](#tc-r1-023) | `TS-R1-02` | Create an account when optional fields are absent | Backend job / API | Medium | S3 | Functional |  | R1 FS v1.2 F01-AC09 and F01 AF04; §1.1.3 and §2.1. |
| [`TC-R1-024`](#tc-r1-024) | `TS-R1-02` | Do not recreate an existing Active account | Backend job / API | High | S2 | Functional |  | R1 FS v1.2 F01-AC06, F01-AC12 and F01 AF03; §1.1.7. |
| [`TC-R1-025`](#tc-r1-025) | `TS-R1-02` | Do not recreate a Closed account hidden from the view | Backend job / API | High | S2 | Functional |  | R1 FS v1.2 F01-AC07 and F01 AF03; §1.1.7. |
| [`TC-R1-026`](#tc-r1-026) | `TS-R1-02` | Create only one account for identical duplicate records | Backend job / API | Medium | S3 | Functional |  | R1 FS v1.2 F01-AC12; §1.1.7. |
| [`TC-R1-027`](#tc-r1-027) | `TS-R1-02` | Handle conflicting DOB values for one NRIC | Backend job / API | High | S2 | Functional |  | R1 FS v1.2 F01 EF03; §1.1.7 and §1.1.10. |
| [`TC-R1-028`](#tc-r1-028) | `TS-R1-03` | Rerunning initial sync preserves existing accounts | Backend job / API | High | S2 | Functional |  | R1 FS v1.2 F01-AC12; §1.1.7 and §2.4; local SYNC-04; received performance X1.3. |
| [`TC-R1-029`](#tc-r1-029) | `TS-R1-03` | Rerunning daily sync does not duplicate accounts | Backend job / API | High | S2 | Functional |  | R1 FS v1.2 F01-AC12; §2.4; received security SR-1.6; received performance X1.3. |
| [`TC-R1-036`](#tc-r1-036) | `TS-R1-03` | Report the outcome of every record in a mixed run | Backend job / API | Medium | S2 | Functional |  | R1 FS v1.2 §2.4; local SYNC-05; received security SE1.3. |
| [`TC-R1-037`](#tc-r1-037) | `TS-R1-04` | Keep the account Active one day before age 16 | Account eligibility API | High | S2 | Functional |  | R1 FS v1.2 F02-AC01 and F02-BR02; §1.2.5. |
| [`TC-R1-038`](#tc-r1-038) | `TS-R1-04` | Close a zero-balance account on access at age 16 | Account eligibility API | Critical | S1 (highest) | Functional |  | R1 FS v1.2 F02-AC02, F02-BR01 and F02-BR02; §2.2. |
| [`TC-R1-042`](#tc-r1-042) | `TS-R1-04` | Repeated access does not close the account again | Account eligibility API | High | S2 | Functional |  | R1 FS v1.2 F02-AC06, F02-BR09; §2.2. |
| [`TC-R1-052`](#tc-r1-052) | `TS-R1-05` | Check the opening wallet and any opening transaction | Wallet API / ledger | Low | S3 | Functional |  | R1 FS v1.2 §1.1.8, §2.2 and §2.3 Scope Note. |
| [`TC-R1-053`](#tc-r1-053) | `TS-R1-05` | Keep cent-level precision across credits | Wallet API / ledger | Critical | S1 (highest) | Functional |  | R1 FS v1.2 §2.3 Monetary values rule. |
| [`TC-R1-054`](#tc-r1-054) | `TS-R1-05` | Refuse a debit larger than the balance | Wallet API / ledger | Critical | S1 (highest) | Functional |  | R1 FS v1.2 §2.3 Negative Account Balance rule. |
| [`TC-R1-056`](#tc-r1-056) | `TS-R1-05` | Refuse credit and debit on Closed or Closure Deferred accounts | Wallet API / ledger | Critical | S1 (highest) | Functional |  | R1 FS v1.2 F02-BR07; §1.2.7; received security SR-1.4, SE1.4. |
| [`TC-R1-058`](#tc-r1-058) | `TS-R1-05` | Reject wallet requests without authentication | Wallet API / ledger | High | S2 | Functional |  | R1 FS v1.2 §1.2.2; local SEC-01. |
| [`TC-R1-012`](#tc-r1-012) | `TS-R1-01` | School level does not determine creation or closure eligibility | Backend job / API | High | S2 | Integration |  | R1 FS v1.2 F01-AC10, F01-BR02, F01-BR03, F02-AC08 and F02-BR04; CD-06. |
| [`TC-R1-013`](#tc-r1-013) | `TS-R1-01` | Link the account to a student with both parent identifiers | Backend job / API | Medium | S3 | Integration |  | R1 FS v1.2 F01-AC01; §1.1.4, §2.1 and §3; FS-08 v0.4 §4.1. |
| [`TC-R1-014`](#tc-r1-014) | `TS-R1-01` | Link only the supplied parent identifier | Backend job / API | Medium | S3 | Integration |  | R1 FS v1.2 F01-AC09; §2.1 and §3; FS-08 v0.4 §4.1. |
| [`TC-R1-016`](#tc-r1-016) | `TS-R1-01` | Adding a parent link does not recreate the account | Backend job / API | Medium | S3 | Integration |  | R1 FS v1.2 §1.1.7, §2.1 and §3; FS-08 v0.4 §4.1. |
| [`TC-R1-020`](#tc-r1-020) | `TS-R1-02` | Reject an unparseable DOB without losing valid records | Backend job / API | Medium | S3 | Integration |  | R1 FS v1.2 F01-AC08 and F01 EF02; §1.1.3 and §1.1.9. |
| [`TC-R1-030`](#tc-r1-030) | `TS-R1-03` | Record a government API authentication failure | Backend job / API | High | S2 | Integration |  | R1 FS v1.2 F01 EF01; §1.1.2, §1.1.9 and §2.4; local SYNC-03. |
| [`TC-R1-031`](#tc-r1-031) | `TS-R1-03` | Retry once after a government API timeout | Backend job / API | High | S2 | Integration |  | R1 FS v1.2 §1.1.9; local SYNC-03. |
| [`TC-R1-032`](#tc-r1-032) | `TS-R1-03` | Recover missed dates after the retry also fails | Backend job / API | High | S2 | Integration |  | R1 FS v1.2 F01-AC11 and F01 EF04; §1.1.5, §1.1.9 and §2.4. |
| [`TC-R1-033`](#tc-r1-033) | `TS-R1-03` | Recover a completely missed daily run | Backend job / API | High | S2 | Integration |  | R1 FS v1.2 F01-AC11 and F01 EF04; §1.1.5; local SYNC-07. |
| [`TC-R1-034`](#tc-r1-034) | `TS-R1-03` | Interrupting a job does not leave partial accounts | Backend job / API | Critical | S1 (highest) | Integration |  | R1 FS v1.2 §1.1.9 and §2.4; received security SR-1.6, SE1.6; local SYNC-03. |
| [`TC-R1-035`](#tc-r1-035) | `TS-R1-03` | The scheduler runs on weekends and public holidays | Backend job / API | Low | S3 | Integration |  | R1 FS v1.2 F01-AC13; §1.1.2. |
| [`TC-R1-039`](#tc-r1-039) | `TS-R1-04` | Close an overdue zero-balance account when HQ retrieves it | Account eligibility API | High | S2 | Integration |  | R1 FS v1.2 F02-AC03; §1.2.5 and §2.2. |
| [`TC-R1-040`](#tc-r1-040) | `TS-R1-04` | Refuse a top-up when the holder has reached 16 | Account eligibility API | Critical | S1 (highest) | Integration |  | R1 FS v1.2 F02-AC04 and F02 AF04. |
| [`TC-R1-041`](#tc-r1-041) | `TS-R1-04` | Refuse payment when the holder has reached 16 | Account eligibility API | Critical | S1 (highest) | Integration |  | R1 FS v1.2 F02-AC05 and F02 AF04; received security SR-1.4, SE1.4. |
| [`TC-R1-043`](#tc-r1-043) | `TS-R1-04` | Keep Closed account history readable to its authorised parent | Account eligibility API | High | S2 | Integration |  | R1 FS v1.2 F02-AC07, F02-BR07 and F02-BR08; FS-08 v0.4 §4.2. |
| [`TC-R1-044`](#tc-r1-044) | `TS-R1-04` | Defer closure when a positive balance cannot transfer to CPF | Account eligibility API | Critical | S1 (highest) | Integration |  | R1 FS v1.2 F02-AC10 and F02 EF04; §1.2.7. |
| [`TC-R1-045`](#tc-r1-045) | `TS-R1-04` | Handle a government-source failure during eligibility checking | Account eligibility API | Critical | S1 (highest) | Integration |  | R1 FS v1.2 F02-AC09 and F02 EF01; §1.2.3 and §1.2.8. |
| [`TC-R1-051`](#tc-r1-051) | `TS-R1-04` | Review a citizenship change before age 16 | Account eligibility API | Critical | S1 (highest) | Integration |  | R1 FS v1.2 F02 EF02; §1.2.6; local SYNC-06. |
| [`TC-R1-055`](#tc-r1-055) | `TS-R1-05` | A failed credit does not change the balance | Wallet API / ledger | High | S2 | Integration |  | R1 FS v1.2 §2.3 Failed Transaction rule. |
| [`TC-R1-057`](#tc-r1-057) | `TS-R1-05` | Debit and reversal are idempotent by FundingReference | Wallet API / ledger | Critical | S1 (highest) | Integration |  | FS Function 9 dated 2026-10-14: EA ledger contract and §2.1 business rules; R1 FS v1.2 §2.3. |
| [`TC-R1-059`](#tc-r1-059) | `TS-R1-06` | Display the agreed portal state for each account condition | Parent / school / payment integration | High | S2 | Integration |  | FS-08 v0.4 §4.2 and §6.2; R1 FS v1.2 §1.2.7 and §3. |
| [`TC-R1-060`](#tc-r1-060) | `TS-R1-06` | Parent sign-in reuses an account already created by R1 | Parent / school / payment integration | High | S2 | Integration |  | R1 FS v1.2 §1.1.7 and §3; FS-08 v0.4 §4.1. |
| [`TC-R1-061`](#tc-r1-061) | `TS-R1-06` | School transfer or withdrawal leaves the account unchanged | Parent / school / payment integration | High | S2 | Integration |  | R1 FS v1.2 F01-BR04 and F02-BR04; §2.1; CD-06. |
| [`TC-R1-062`](#tc-r1-062) | `TS-R1-06` | A student without an account cannot pay from its balance | Parent / school / payment integration | High | S2 | Integration |  | R1 FS v1.2 F01-AC03; FS Function 9 no-EA payment rule; received performance X9.6, CS-9.7. |
| [`TC-R1-070`](#tc-r1-070) | `TS-R1-08` | Overlapping sync runs do not create duplicate accounts | Backend job / API | Critical | S1 (highest) | Integration |  | R1 FS v1.2 §1.1.7; received performance PR-1.5, X1.7, CS-1.3. |
| [`TC-R1-073`](#tc-r1-073) | `TS-R1-01` | Record the daily-sync limitation for a late-arriving citizen | Backend job / API | High | S2 | Integration |  | R1 FS v1.2 F01-AC02; §1.1.5, §1.1.9 Limitation and §4. |
| [`TC-R1-074`](#tc-r1-074) | `TS-R1-08` | Check eligibility while a payment is in progress | Backend job / API | High | S2 | Integration |  | R1 FS v1.2 §1.2.7; received performance X1.8, X1.9, PR-1.8, CS-1.5; client CD-02. |
| [`TC-R1-075`](#tc-r1-075) | `TS-R1-04` | Closure uses the Singapore date when UTC is still yesterday | Account eligibility API | High | S2 | Integration |  | R1 FS v1.2 F02-BR01, F02-BR02, F02-AC02, F02-AC06; QA SGT assumption; §2.2. |
| [`TC-R1-068`](#tc-r1-068) | `TS-R1-08` | Measure creation and access-triggered closure separately | Backend job / API | High | S2 | Performance |  | Received performance CS-1.1, PR-1.1 to PR-1.4, PR-1.6, X1.1, X1.2, X1.6; R1 FS v1.2 §1.2.7. |
| [`TC-R1-069`](#tc-r1-069) | `TS-R1-08` | Parallel processing matches sequential processing | Backend job / API | Medium | S3 | Performance |  | Received performance PR-1.7, X1.4, CS-1.2. |
| [`TC-R1-071`](#tc-r1-071) | `TS-R1-08` | Account reads remain correct while sync runs | Backend job / API | High | S2 | Performance |  | Received performance X1.5, CS-1.4, CS-8.4, X8.1; local SYNC-07. |
| [`TC-R1-072`](#tc-r1-072) | `TS-R1-08` | Measure sync under the agreed peak parent load | Backend job / API | Medium | S3 | Performance |  | Received performance XS.3, CS-P.3; local PERF-07. |
| [`TC-R1-063`](#tc-r1-063) | `TS-R1-07` | Unauthorised identities cannot start or configure the job | Backend job / API | Critical | S1 (highest) | Security |  | Received security SR-1.1, SE1.1; local SEC-01. |
| [`TC-R1-064`](#tc-r1-064) | `TS-R1-07` | Out-of-source changes do not drive account decisions | Backend job / API | Critical | S1 (highest) | Security |  | Received security SR-1.2, SE1.2; R1 FS v1.2 §1.1.4 and §1.2.3. |
| [`TC-R1-065`](#tc-r1-065) | `TS-R1-07` | Record creation and access-triggered closure for audit | Backend job / API | High | S2 | Security |  | R1 FS v1.2 §2.2 and §2.4; received security SR-1.3, SR-1.8, SE1.3, SE1.8. |
| [`TC-R1-066`](#tc-r1-066) | `TS-R1-07` | Keep sensitive data out of logs, errors and descriptions | Backend job / API | Critical | S1 (highest) | Security |  | Received security draft 0.3 SR-1.5, SE1.5; local security draft 0.4 SEC-05, SYNC-01; implementation audit F3. |
| [`TC-R1-067`](#tc-r1-067) | `TS-R1-07` | Future CPF transfer cannot be started or altered without authority | Backend job / API | Critical | S1 (highest) | Security |  | Received security SR-1.7, SE1.7, SE1.8; R1 FS v1.2 §1.2.7. |
| [`TC-R1-076`](#tc-r1-076) | `TS-R1-02` | Daily sync includes leap-day birthdays under the proposed rule | Backend job / API | High | S2 | Integration |  | R1 FS v1.2 F01-AC02, F01-AC14; §1.1.5 and §1.1.6. |
| [`TC-R1-077`](#tc-r1-077) | `TS-R1-05` | Concurrent duplicate debit and reversal have one financial effect | Wallet API / ledger | Critical | S1 (highest) | Integration |  | FS Function 9 dated 2026-10-14 §2.1, EA ledger contract; R1 FS v1.2 §2.3. |
| [`TC-R1-078`](#tc-r1-078) | `TS-R1-04` | Closure persistence failure leaves a consistent account | Account eligibility API | High | S2 | Integration |  | R1 FS v1.2 F02 EF03; §1.2.3 and §2.2. |

---

## Detailed Test Case Specifications


### Test Suite: Eligibility and age boundary

#### `TC-R1-001`: Create an account on the seventh birthday

- **Scenario ID**: `TS-R1-01`
- **Test Suite**: Eligibility and age boundary
- **Page / Target**: `Backend job / API`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R1 FS v1.2 §1.1.4, §1.1.6 and §1.1.8; tender R1.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: CR: creation at 7. TD: initial-sync flow and account setup.

**Preconditions:**
```text
Set the service clock to 15 October 2026, 12:00 SGT. No student or wallet exists for STU-R1-02. The initial-sync mock returns only this record. Use only a test HTTP source and isolated database; synthetic NRIC acceptance by the mock contract is pending.
```

**Test Data:**
```text
STU-R1-02: Singapore Citizen; DOB 2019-10-15; no account.
Base source records, overridden by the case variants above: STU-R1-02: NRIC="T9900002A"; FullName="R1 Mock Student 02"; DOB=2019-10-15; CitizenshipStatus=SingaporeCitizen; Gender=Female.
```

**Test Steps:**
1. Run the real initial synchronisation.
2. Read the student and wallet rows.
3. Read the processing result for this record.

**Expected Result:**
> Exactly one Active wallet is linked to the correct student. Balance is SGD 0.00, currency is SGD, and Account Creation Date records this run.

---

#### `TC-R1-002`: Do not create an account before age 7

- **Scenario ID**: `TS-R1-01`
- **Test Suite**: Eligibility and age boundary
- **Page / Target**: `Backend job / API`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R1 FS v1.2 F01-AC04, F01-BR02 and F01 AF02; §2.4.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: CR: creation starts at 7. WA: detailed per-record skip reporting.

**Preconditions:**
```text
Service clock: 15 October 2026, 12:00 SGT; no student or wallet exists for STU-R1-01. Return this record in the initial-sync mock. Use only a test HTTP source and isolated database; synthetic NRIC acceptance by the mock contract is pending.
```

**Test Data:**
```text
STU-R1-01: DOB 2019-10-16; Singapore Citizen; no account.
Base source records, overridden by the case variants above: STU-R1-01: NRIC="T9900001A"; FullName="R1 Mock Student 01"; DOB=2019-10-16; CitizenshipStatus=SingaporeCitizen; Gender=Female.
```

**Test Steps:**
1. Run the initial synchronisation.
2. Check for a wallet linked to this NRIC.
3. Read the record processing result.

**Expected Result:**
> No wallet is created. The processing result identifies the record as below the eligible age.

---

#### `TC-R1-003`: Initial sync creates an account one day before age 16

- **Scenario ID**: `TS-R1-01`
- **Test Suite**: Eligibility and age boundary
- **Page / Target**: `Backend job / API`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R1 FS v1.2 F01-BR02; §1.1.4.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: WA: initial backfill for citizens aged 7 to under 16.
- **Note**: Initial backfill is marked WA in v1.2, not an agreed daily-sync rule.

**Preconditions:**
```text
Service clock: 15 October 2026, 12:00 SGT; STU-R1-04 has no account. Initial-sync coverage of eligible citizens older than 7 is agreed or reported as an observation. Use only a test HTTP source and isolated database; synthetic NRIC acceptance by the mock contract is pending.
```

**Test Data:**
```text
STU-R1-04: DOB 2010-10-16; Singapore Citizen; no account.
Base source records, overridden by the case variants above: STU-R1-04: NRIC="T9900004A"; FullName="R1 Mock Student 04"; DOB=2010-10-16; CitizenshipStatus=SingaporeCitizen; Gender=Female.
```

**Test Steps:**
1. Return only STU-R1-04 from the initial-sync mock.
2. Run the initial synchronisation.
3. Read the wallet row.

**Expected Result:**
> Under the proposed initial-backfill rule, one Active wallet is created with balance SGD 0.00. Do not apply the daily birthday-only query to this initial-sync case.

---

#### `TC-R1-004`: Do not create an account at age 16

- **Scenario ID**: `TS-R1-01`
- **Test Suite**: Eligibility and age boundary
- **Page / Target**: `Backend job / API`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R1 FS v1.2 F01-AC05, F01-BR05 and F01 AF02.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: CR: account age limit. TD: no new account at or above 16.

**Preconditions:**
```text
Service clock: 15 October 2026, 12:00 SGT; STU-R1-05 has no student or wallet. Return this record in the initial-sync mock. Use only a test HTTP source and isolated database; synthetic NRIC acceptance by the mock contract is pending.
```

**Test Data:**
```text
STU-R1-05: DOB 2010-10-15; Singapore Citizen; no account.
Base source records, overridden by the case variants above: STU-R1-05: NRIC="T9900005A"; FullName="R1 Mock Student 05"; DOB=2010-10-15; CitizenshipStatus=SingaporeCitizen; Gender=Female.
```

**Test Steps:**
1. Run the initial synchronisation.
2. Check for a wallet linked to this NRIC.
3. Read the record processing result.

**Expected Result:**
> No wallet is created because the holder has reached 16.

---

#### `TC-R1-005`: Do not create an account above age 16

- **Scenario ID**: `TS-R1-01`
- **Test Suite**: Eligibility and age boundary
- **Page / Target**: `Backend job / API`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R1 FS v1.2 F01-AC05, F01-BR05 and F01 AF02.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: TD: no account creation at or above 16.

**Preconditions:**
```text
Service clock: 15 October 2026, 12:00 SGT; seed STU-R1-07 with no wallet for this independent test. The initial-sync mock returns this record. Use only a test HTTP source and isolated database; synthetic NRIC acceptance by the mock contract is pending.
```

**Test Data:**
```text
STU-R1-07 variant: DOB 2009-03-01; Singapore Citizen; no account.
Base source records, overridden by the case variants above: STU-R1-07: NRIC="T9900007A"; FullName="R1 Mock Student 07"; DOB=2009-03-01; CitizenshipStatus=SingaporeCitizen; Gender=Female.
```

**Test Steps:**
1. Run the initial synchronisation.
2. Check for a wallet linked to this NRIC.

**Expected Result:**
> No wallet is created for the 17-year-old citizen.

---

#### `TC-R1-006`: Do not create an account for a permanent resident

- **Scenario ID**: `TS-R1-01`
- **Test Suite**: Eligibility and age boundary
- **Page / Target**: `Backend job / API`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R1 FS v1.2 F01-AC03, F01-BR01 and F01 AF01; §2.1; CD-01.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: CR: Education Accounts are for Singapore Citizens only.

**Preconditions:**
```text
Service clock: 15 October 2026, 12:00 SGT; no account exists for STU-R1-09. Return this record in the initial-sync mock. Use only a test HTTP source and isolated database; synthetic NRIC acceptance by the mock contract is pending.
```

**Test Data:**
```text
STU-R1-09: DOB 2019-10-15; Permanent Resident; no account.
Base source records, overridden by the case variants above: STU-R1-09: NRIC="T9900009A"; FullName="R1 Mock Student 09"; DOB=2019-10-15; CitizenshipStatus=PermanentResident; Gender=Female.
```

**Test Steps:**
1. Run the initial synchronisation.
2. Check for a wallet linked to this NRIC.
3. Record whether a Student Profile exists.

**Expected Result:**
> No wallet is created. Student Profile presence is recorded; this case does not require the sync to create a non-citizen profile.

---

#### `TC-R1-007`: Do not create an account for a foreign student

- **Scenario ID**: `TS-R1-01`
- **Test Suite**: Eligibility and age boundary
- **Page / Target**: `Backend job / API`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R1 FS v1.2 F01-AC03, F01-BR01 and F01 AF01; CD-01.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: CR: Education Accounts are for Singapore Citizens only.

**Preconditions:**
```text
Service clock: 15 October 2026, 12:00 SGT; no account exists for STU-R1-10. Return this record in the initial-sync mock. Use only a test HTTP source and isolated database; synthetic NRIC acceptance by the mock contract is pending.
```

**Test Data:**
```text
STU-R1-10: DOB 2015-08-10; foreign student, aged 11; no account.
Base source records, overridden by the case variants above: STU-R1-10: NRIC="T9900010A"; FullName="R1 Mock Student 10"; DOB=2015-08-10; CitizenshipStatus=ForeignStudent; Gender=Female.
```

**Test Steps:**
1. Run the initial synchronisation.
2. Check for a wallet linked to this NRIC.

**Expected Result:**
> No wallet is created because the student is not a Singapore Citizen.

---

#### `TC-R1-008`: Evaluate a 29 February DOB on 28 February

- **Scenario ID**: `TS-R1-01`
- **Test Suite**: Eligibility and age boundary
- **Page / Target**: `Backend job / API`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R1 FS v1.2 F01-AC14; §1.1.6.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: WA: 28 February is the birthday boundary in a non-leap year.

**Preconditions:**
```text
Fresh database; no account for STU-R1-08. Set the service clock to 2027-02-28 12:00 SGT. The initial-sync mock returns this record. Use only a test HTTP source and isolated database; synthetic NRIC acceptance by the mock contract is pending.
```

**Test Data:**
```text
STU-R1-08: DOB 2020-02-29; Singapore Citizen.
Base source records, overridden by the case variants above: STU-R1-08: NRIC="T9900008A"; FullName="R1 Mock Student 08"; DOB=2020-02-29; CitizenshipStatus=SingaporeCitizen; Gender=Female.
```

**Test Steps:**
1. Run the initial synchronisation at the fixed time.
2. Read the wallet row.

**Expected Result:**
> Under the proposed leap-year rule, the citizen reaches 7 on 28 February and receives one Active wallet with balance SGD 0.00.

---

#### `TC-R1-009`: Do not create the leap-year account on 27 February

- **Scenario ID**: `TS-R1-01`
- **Test Suite**: Eligibility and age boundary
- **Page / Target**: `Backend job / API`
- **Severity / Priority**: `S3` / `Low`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R1 FS v1.2 F01-AC04, F01-AC14; §1.1.6.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: WA: 28 February is the birthday boundary in a non-leap year.

**Preconditions:**
```text
Fresh database; no account for STU-R1-08. Set the service clock to 2027-02-27 12:00 SGT. The initial-sync mock returns this record. Use only a test HTTP source and isolated database; synthetic NRIC acceptance by the mock contract is pending.
```

**Test Data:**
```text
STU-R1-08: DOB 2020-02-29; Singapore Citizen.
Base source records, overridden by the case variants above: STU-R1-08: NRIC="T9900008A"; FullName="R1 Mock Student 08"; DOB=2020-02-29; CitizenshipStatus=SingaporeCitizen; Gender=Female.
```

**Test Steps:**
1. Run the initial synchronisation at the fixed time.
2. Check for a wallet linked to this NRIC.

**Expected Result:**
> No wallet is created; the citizen is one day short of the proposed seventh-birthday boundary.

---

#### `TC-R1-010`: Daily sync uses the Singapore processing date

- **Scenario ID**: `TS-R1-01`
- **Test Suite**: Eligibility and age boundary
- **Page / Target**: `Backend job / API`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R1 FS v1.2 F01-AC02; §1.1.2 and §1.1.5.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: WA: SGT processing. TD: daily query targets the seventh birthday.
- **Note**: This tests a sync cycle, not the scheduler. TC-R1-035 tests automatic triggering; TC-R1-075 tests closure time.

**Preconditions:**
```text
Fresh database; no account for STU-R1-02. Set the service clock to 2026-10-14T17:00:00Z, which is 15 October 01:00 SGT. Use only a test HTTP source and isolated database; synthetic NRIC acceptance by the mock contract is pending.
```

**Test Data:**
```text
STU-R1-02: SingaporeCitizen; DOB 2019-10-15. Mock API returns it only for the matching DOB query.
Base source records, overridden by the case variants above: STU-R1-02: NRIC="T9900002A"; FullName="R1 Mock Student 02"; DOB=2019-10-15; CitizenshipStatus=SingaporeCitizen; Gender=Female.
```

**Test Steps:**
1. Run one real daily sync cycle without overriding the target DOB.
2. Capture the outgoing DOB query and processing date.
3. Read the wallet row.

**Expected Result:**
> The processing date is 15 October SGT, the DOB query is 2019-10-15, and one Active wallet is created.

---

#### `TC-R1-011`: School enrolment is not required for account creation

- **Scenario ID**: `TS-R1-01`
- **Test Suite**: Eligibility and age boundary
- **Page / Target**: `Backend job / API`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R1 FS v1.2 F01-BR02, F01-BR03 and F01-BR04; §2.1; CD-06.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: CR: schooling independence. WA: initial backfill.

**Preconditions:**
```text
Service clock: 15 October 2026, 12:00 SGT; no account for STU-R1-11. No school, class or enrolment record exists. Initial backfill is agreed or reported as an observation. Use only a test HTTP source and isolated database; synthetic NRIC acceptance by the mock contract is pending.
```

**Test Data:**
```text
STU-R1-11: DOB 2018-04-12; Singapore Citizen; no school, class or enrolment.
Base source records, overridden by the case variants above: STU-R1-11: NRIC="T9900011A"; FullName="R1 Mock Student 11"; DOB=2018-04-12; CitizenshipStatus=SingaporeCitizen; Gender=Female.
```

**Test Steps:**
1. Return STU-R1-11 from the initial-sync mock.
2. Run the initial synchronisation.
3. Read the wallet row.

**Expected Result:**
> Under the initial-backfill rule, the eligible citizen receives an Active wallet. Missing school, class or enrolment data does not block creation.

---

#### `TC-R1-015`: Create an account when no parent identifier is supplied

- **Scenario ID**: `TS-R1-01`
- **Test Suite**: Eligibility and age boundary
- **Page / Target**: `Backend job / API`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R1 FS v1.2 F01-AC09 and F01 AF04; §2.1.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: TD: parent identifiers are optional for creation.

**Preconditions:**
```text
Service clock: 15 October 2026, 12:00 SGT; STU-R1-12 has no account. FatherNric and MotherNric are null. Use only a test HTTP source and isolated database; synthetic NRIC acceptance by the mock contract is pending.
```

**Test Data:**
```text
STU-R1-12: DOB 2019-10-15; Singapore Citizen; no parent identifiers.
Base source records, overridden by the case variants above: STU-R1-12: NRIC="T9900012A"; FullName="R1 Mock Student 12"; DOB=2019-10-15; CitizenshipStatus=SingaporeCitizen; Gender=Female.
```

**Test Steps:**
1. Run the initial synchronisation for this record.
2. Read the wallet and its student link.
3. Check for parent links.

**Expected Result:**
> One Active wallet is created and links to the correct student. No parent link is invented.

---

#### `TC-R1-012`: School level does not determine creation or closure eligibility

- **Scenario ID**: `TS-R1-01`
- **Test Suite**: Eligibility and age boundary
- **Page / Target**: `Backend job / API`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: R1 FS v1.2 F01-AC10, F01-BR02, F01-BR03, F02-AC08 and F02-BR04; CD-06.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: CR: schooling independence. TD: backend-triggered closure. WA: initial backfill.

**Preconditions:**
```text
Service clock: 15 October 2026, 12:00 SGT; use separate clean fixtures for creation and closure. Both students have a retained/lower school level. Initial backfill is agreed or observed. Use only a test HTTP source and isolated database; synthetic NRIC acceptance by the mock contract is pending.
```

**Test Data:**
```text
Creation: STU-R1-13, DOB 2015-01-10, no wallet. Closure: after reset, the same mock identity with DOB 2010-10-15, Active wallet and balance SGD 0.00.
Base source records, overridden by the case variants above: STU-R1-13: NRIC="T9900013A"; FullName="R1 Mock Student 13"; DOB=2015-01-10; CitizenshipStatus=SingaporeCitizen; Gender=Female.
```

**Test Steps:**
1. Run initial sync for the creation fixture.
2. Read the created wallet and student link.
3. Reset to the independent age-16 closure fixture.
4. Access the account through the real eligibility path.
5. Read status and balance and compare the age decision with DOB, not school level.

**Expected Result:**
> Under the initial-backfill rule, the first fixture receives one Active wallet with SGD 0.00. The zero-balance age-16 fixture closes on access despite its lower school level. School level does not determine either age decision.

---

#### `TC-R1-013`: Link the account to a student with both parent identifiers

- **Scenario ID**: `TS-R1-01`
- **Test Suite**: Eligibility and age boundary
- **Page / Target**: `Backend job / API`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: R1 FS v1.2 F01-AC01; §1.1.4, §2.1 and §3; FS-08 v0.4 §4.1.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: TD: account-to-student link. WA: initial backfill. Parent authorisation follows the R8 contract.
- **Note**: Guardian linking belongs to R8; this is an integration check, not F01-AC07.

**Preconditions:**
```text
Service clock: 15 October 2026, 12:00 SGT; STU-R1-03 has no account. Both synthetic parent profiles exist. The R8 relationship contract is available. Use only a test HTTP source and isolated database; synthetic NRIC acceptance by the mock contract is pending.
```

**Test Data:**
```text
STU-R1-03: DOB 2016-05-20; Singapore Citizen; FatherNric=T9901001A; MotherNric=T9901002A.
Base source records, overridden by the case variants above: STU-R1-03: NRIC="T9900003A"; FullName="R1 Mock Student 03"; DOB=2016-05-20; CitizenshipStatus=SingaporeCitizen; Gender=Female.
```

**Test Steps:**
1. Run initial synchronisation for this citizen.
2. Read the wallet and its link to the correct student.
3. Sign in through R8 as the synthetic father, then as the synthetic mother, allowing each data refresh to finish.
4. Read parent-to-student links and check that both supplied parents, and no unrelated parent, link to this student.

**Expected Result:**
> One Active wallet with balance SGD 0.00 links to the correct student. Under the agreed R8 relationship rule, both parent identifiers link to that student and no unrelated parent is linked.

---

#### `TC-R1-014`: Link only the supplied parent identifier

- **Scenario ID**: `TS-R1-01`
- **Test Suite**: Eligibility and age boundary
- **Page / Target**: `Backend job / API`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: R1 FS v1.2 F01-AC09; §2.1 and §3; FS-08 v0.4 §4.1.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: TD: student link. WA: initial backfill. Parent linking follows the R8 contract.

**Preconditions:**
```text
Service clock: 15 October 2026, 12:00 SGT; use STU-R1-03 with Father NRIC only, no Mother NRIC and no account. The R8 relationship contract is available. Use only a test HTTP source and isolated database; synthetic NRIC acceptance by the mock contract is pending.
```

**Test Data:**
```text
STU-R1-03: DOB 2016-05-20; SingaporeCitizen; no account; FatherNric=T9901001A; MotherNric=null.
Base source records, overridden by the case variants above: STU-R1-03: NRIC="T9900003A"; FullName="R1 Mock Student 03"; DOB=2016-05-20; CitizenshipStatus=SingaporeCitizen; Gender=Female.
```

**Test Steps:**
1. Run initial synchronisation for this citizen.
2. Read the wallet and its link to the correct student.
3. Sign in through R8 as the supplied father and allow the data refresh to finish.
4. Read parent-to-student links and check that no mother or blank parent link was invented.

**Expected Result:**
> The eligible account links to the correct student. Under the R8 rule, only the supplied parent is linked; no blank or invented parent link is added.

---

#### `TC-R1-016`: Adding a parent link does not recreate the account

- **Scenario ID**: `TS-R1-01`
- **Test Suite**: Eligibility and age boundary
- **Page / Target**: `Backend job / API`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: R1 FS v1.2 §1.1.7, §2.1 and §3; FS-08 v0.4 §4.1.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: OPEN: confirm the refresh path and parent-link rule. CR: one account per citizen.
- **Note**: Do not expect the daily seventh-birthday query to retrieve this existing nine-year-old holder.

**Preconditions:**
```text
Service clock: 15 October 2026, 12:00 SGT; STU-R1-16 has an Active wallet with balance SGD 100.00. An agreed parent-data refresh path is available. Use only a test HTTP source and isolated database; synthetic NRIC acceptance by the mock contract is pending.
```

**Test Data:**
```text
STU-R1-16: DOB 2017-03-05. Add one valid synthetic parent identifier in the mock source; leave local links unchanged.
Base source records, overridden by the case variants above: STU-R1-16: NRIC="T9900016A"; FullName="R1 Mock Student 16"; DOB=2017-03-05; CitizenshipStatus=SingaporeCitizen; Gender=Female. Use FatherNric=T9901001A as the newly added synthetic parent.
```

**Test Steps:**
1. Record wallet ID, balance, status and creation timestamp.
2. Add the parent identifier to the source.
3. Trigger the agreed R8 sign-in/data-refresh path.
4. Read the links and compare the wallet with the snapshot.

**Expected Result:**
> The authorised parent link is added without creating a second account or changing balance, status or creation timestamp.

---

#### `TC-R1-073`: Record the daily-sync limitation for a late-arriving citizen

- **Scenario ID**: `TS-R1-01`
- **Test Suite**: Eligibility and age boundary
- **Page / Target**: `Backend job / API`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: R1 FS v1.2 F01-AC02; §1.1.5, §1.1.9 Limitation and §4.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: TD: birthday-based daily query. OPEN: late-arrival recovery beyond that query.
- **Note**: This preserves a coverage gap for decision; it does not claim all older late arrivals must be created by the daily job.

**Preconditions:**
```text
Service clock: 15 October 2026, 12:00 SGT; initial sync ran before STU-R1-03 existed in the source. The daily contract queries only the current seventh-birthday DOB. Use only a test HTTP source and isolated database; synthetic NRIC acceptance by the mock contract is pending. Successful coverage ends on 14 October; no missed-day recovery is due.
```

**Test Data:**
```text
Late arrival: STU-R1-03, DOB 2016-05-20, age 10. Current birthday: STU-R1-02, DOB 2019-10-15. Neither has an account.
Base source records, overridden by the case variants above: STU-R1-03: NRIC="T9900003A"; FullName="R1 Mock Student 03"; DOB=2016-05-20; CitizenshipStatus=SingaporeCitizen; Gender=Female | STU-R1-02: NRIC="T9900002A"; FullName="R1 Mock Student 02"; DOB=2019-10-15; CitizenshipStatus=SingaporeCitizen; Gender=Female.
```

**Test Steps:**
1. Add both records to the mock source.
2. Run the real daily cycle without widening its DOB query.
3. Capture source queries and returned records.
4. Read wallets for both citizens.
5. Record the late-arrival result and any proposed backfill path.

**Expected Result:**
> The birthday record follows the normal daily creation rule. Record whether the ten-year-old is retrieved or created. v1.2 identifies late arrivals as a limitation; automatic daily backfill is not an agreed pass requirement.

---


### Test Suite: Data validation and duplicate prevention

#### `TC-R1-017`: Reject a record with no NRIC

- **Scenario ID**: `TS-R1-02`
- **Test Suite**: Data validation and duplicate prevention
- **Page / Target**: `Backend job / API`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R1 FS v1.2 F01-AC08 and F01 EF02; §1.1.3 and §1.1.9; local security draft SYNC-02.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: TD: NRIC is required. WA: invalid-record isolation and detailed reporting.

**Preconditions:**
```text
Service clock: 15 October 2026, 12:00 SGT; fresh database. The initial-sync mock returns one valid record and one record with a blank NRIC. Return the invalid record first and the valid STU-R1-02 record second. Use only a test HTTP source and isolated database; synthetic NRIC acceptance by the mock contract is pending.
```

**Test Data:**
```text
Valid: STU-R1-02. Invalid: STU-R1-17 with Nric=""; all other required fields valid.
Base source records, overridden by the case variants above: STU-R1-02: NRIC="T9900002A"; FullName="R1 Mock Student 02"; DOB=2019-10-15; CitizenshipStatus=SingaporeCitizen; Gender=Female | STU-R1-17: NRIC=""; FullName="R1 Mock Student 17"; DOB=2016-09-09; CitizenshipStatus=SingaporeCitizen; Gender=Female.
```

**Test Steps:**
1. Run initial synchronisation in that order.
2. Check for the valid record's wallet.
3. Check for any wallet created from the invalid record.
4. Read the validation result using the mock record key.
5. Check that the valid record after the error receives exactly one Active wallet.

**Expected Result:**
> The invalid record creates no wallet and has a missing-NRIC error. Under the proposed record-isolation rule, the later valid record receives exactly one Active wallet.

---

#### `TC-R1-018`: Reject a record with no full name

- **Scenario ID**: `TS-R1-02`
- **Test Suite**: Data validation and duplicate prevention
- **Page / Target**: `Backend job / API`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R1 FS v1.2 F01-AC08 and F01 EF02; §1.1.3 and §1.1.9.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: TD: Full Name is required. WA: invalid-record isolation.

**Preconditions:**
```text
Service clock: 15 October 2026, 12:00 SGT; fresh database. Return one valid record and one record with a blank full name. Return the invalid record first and the valid STU-R1-02 record second. Use only a test HTTP source and isolated database; synthetic NRIC acceptance by the mock contract is pending.
```

**Test Data:**
```text
Valid: STU-R1-02. Invalid: STU-R1-18 with FullName=""; other required fields valid.
Base source records, overridden by the case variants above: STU-R1-02: NRIC="T9900002A"; FullName="R1 Mock Student 02"; DOB=2019-10-15; CitizenshipStatus=SingaporeCitizen; Gender=Female | STU-R1-18: NRIC="T9900018A"; FullName=""; DOB=2016-09-09; CitizenshipStatus=SingaporeCitizen; Gender=Female.
```

**Test Steps:**
1. Run initial synchronisation in that order.
2. Check for both records' wallets.
3. Read the missing-name error and valid-record result.
4. Check that the valid record after the error receives exactly one Active wallet.

**Expected Result:**
> No wallet is created for the record with no name. Under the proposed isolation rule, the later valid record receives exactly one Active wallet.

---

#### `TC-R1-019`: Reject a future DOB

- **Scenario ID**: `TS-R1-02`
- **Test Suite**: Data validation and duplicate prevention
- **Page / Target**: `Backend job / API`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R1 FS v1.2 F01-AC08 and F01 EF02; §1.1.3.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: TD: DOB must be valid and not in the future.
- **Note**: Exercise the sync path. The lack of a DOB check in one validator does not establish the whole-path outcome.

**Preconditions:**
```text
Service clock: 15 October 2026, 12:00 SGT; fresh database. Return STU-R1-19 and one valid citizen from the initial-sync mock. Use only a test HTTP source and isolated database; synthetic NRIC acceptance by the mock contract is pending.
```

**Test Data:**
```text
Invalid: STU-R1-19 with DOB 2028-01-01. Valid: STU-R1-02.
Base source records, overridden by the case variants above: STU-R1-19: NRIC="T9900019A"; FullName="R1 Mock Student 19"; DOB=2028-01-01; CitizenshipStatus=SingaporeCitizen; Gender=Female | STU-R1-02: NRIC="T9900002A"; FullName="R1 Mock Student 02"; DOB=2019-10-15; CitizenshipStatus=SingaporeCitizen; Gender=Female.
```

**Test Steps:**
1. Run the initial synchronisation through the real validation path.
2. Check for a wallet for STU-R1-19.
3. Read the validation reason.

**Expected Result:**
> No wallet is created for the future DOB, and the result identifies an invalid future date rather than only an age-based skip.

---

#### `TC-R1-021`: Reject an unknown citizenship value

- **Scenario ID**: `TS-R1-02`
- **Test Suite**: Data validation and duplicate prevention
- **Page / Target**: `Backend job / API`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R1 FS v1.2 F01-AC08, F01-BR01 and F01 EF02; §1.1.3.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: TD: citizenship must be recognised. CR: only Singapore Citizens are eligible.

**Preconditions:**
```text
Service clock: 15 October 2026, 12:00 SGT; fresh database. The initial-sync mock can return an unknown raw citizenship value. Use only a test HTTP source and isolated database; synthetic NRIC acceptance by the mock contract is pending.
```

**Test Data:**
```text
STU-R1-24 variant: CitizenshipStatus="Unknown-QA", not SingaporeCitizen. Other required fields valid.
Base source records, overridden by the case variants above: STU-R1-24: NRIC="T9900024A"; FullName="R1 Mock Student 24"; DOB=2016-09-09; CitizenshipStatus=Unknown-QA; Gender=Female.
```

**Test Steps:**
1. Run the initial synchronisation.
2. Check for a wallet for this NRIC.
3. Read the rejection reason.

**Expected Result:**
> No wallet is created. The value is reported as unrecognised, not treated as eligible.

---

#### `TC-R1-022`: Reject missing gender when the field is required

- **Scenario ID**: `TS-R1-02`
- **Test Suite**: Data validation and duplicate prevention
- **Page / Target**: `Backend job / API`
- **Severity / Priority**: `S3` / `Low`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R1 FS v1.2 F01-AC08 and F01 EF02; §1.1.3 and §2.1.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: WA: gender is required in the input. TD: current student data design includes gender.
- **Note**: The current sync maps every non-Female value to Male. Accepted gender values still need agreement.

**Preconditions:**
```text
Service clock: 15 October 2026, 12:00 SGT; fresh database. Confirm that gender remains required under the current input contract. Use only a test HTTP source and isolated database; synthetic NRIC acceptance by the mock contract is pending.
```

**Test Data:**
```text
STU-R1-25 variant: Gender=null; DOB 2019-10-15; SingaporeCitizen; other required fields valid.
Base source records, overridden by the case variants above: STU-R1-25: NRIC="T9900025A"; FullName="R1 Mock Student 25"; DOB=2016-09-09; CitizenshipStatus=SingaporeCitizen; Gender=null.
```

**Test Steps:**
1. Run the initial synchronisation.
2. Check for a wallet.
3. Read the validation or mapping result.

**Expected Result:**
> If gender is required, no wallet is created and missing gender is reported. If the contract changes, record the decision and do not judge against the retired rule.

---

#### `TC-R1-023`: Create an account when optional fields are absent

- **Scenario ID**: `TS-R1-02`
- **Test Suite**: Data validation and duplicate prevention
- **Page / Target**: `Backend job / API`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R1 FS v1.2 F01-AC09 and F01 AF04; §1.1.3 and §2.1.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: TD: optional fields do not block creation.

**Preconditions:**
```text
Service clock: 15 October 2026, 12:00 SGT; fresh database. All required fields are valid; optional fields are absent. Use only a test HTTP source and isolated database; synthetic NRIC acceptance by the mock contract is pending.
```

**Test Data:**
```text
STU-R1-02 variant: Race=null, RegisteredAddress=null, FatherNric=null and MotherNric=null.
Base source records, overridden by the case variants above: STU-R1-02: NRIC="T9900002A"; FullName="R1 Mock Student 02"; DOB=2019-10-15; CitizenshipStatus=SingaporeCitizen; Gender=Female.
```

**Test Steps:**
1. Run the initial synchronisation.
2. Read the wallet and its student link.

**Expected Result:**
> One Active wallet is created with balance SGD 0.00. Missing optional fields do not block creation.

---

#### `TC-R1-024`: Do not recreate an existing Active account

- **Scenario ID**: `TS-R1-02`
- **Test Suite**: Data validation and duplicate prevention
- **Page / Target**: `Backend job / API`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R1 FS v1.2 F01-AC06, F01-AC12 and F01 AF03; §1.1.7.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: CR: one account per citizen. TD: existing-account duplicate prevention.

**Preconditions:**
```text
Service clock: 15 October 2026, 12:00 SGT; STU-R1-13 has an Active wallet with balance SGD 250.00. Return the same citizen in the initial-sync mock. Use only a test HTTP source and isolated database; synthetic NRIC acceptance by the mock contract is pending.
```

**Test Data:**
```text
STU-R1-13: DOB 2015-01-10; SingaporeCitizen; Active wallet; balance SGD 250.00.
Base source records, overridden by the case variants above: STU-R1-13: NRIC="T9900013A"; FullName="R1 Mock Student 13"; DOB=2015-01-10; CitizenshipStatus=SingaporeCitizen; Gender=Female.
```

**Test Steps:**
1. Record wallet ID, account number, balance, status, creation timestamp and transaction count.
2. Run the initial synchronisation again.
3. Compare the wallet and transaction count with the snapshot.

**Expected Result:**
> No second wallet or extra opening transaction is created. Account number, balance, status and creation timestamp stay unchanged.

---

#### `TC-R1-025`: Do not recreate a Closed account hidden from the view

- **Scenario ID**: `TS-R1-02`
- **Test Suite**: Data validation and duplicate prevention
- **Page / Target**: `Backend job / API`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R1 FS v1.2 F01-AC07 and F01 AF03; §1.1.7.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: TD: duplicate prevention also covers Closed accounts. WA: account retention/deletion policy.
- **Note**: The under-16 variant prevents an age rejection from hiding a broken duplicate check. The hidden-view subcheck depends on R8.

**Preconditions:**
```text
Service clock: 15 October 2026, 12:00 SGT; seed the Closed-account variant of STU-R1-14 while its DOB is still within the creation age range. Hide it from the tested view if that view exists. Use only a test HTTP source and isolated database; synthetic NRIC acceptance by the mock contract is pending.
```

**Test Data:**
```text
STU-R1-14 variant: DOB 2015-06-01; Closed wallet; balance SGD 0.00; existing wallet ID and closure timestamp.
Base source records, overridden by the case variants above: STU-R1-14: NRIC="T9900014A"; FullName="R1 Mock Student 14"; DOB=2009-06-01; CitizenshipStatus=SingaporeCitizen; Gender=Female.
```

**Test Steps:**
1. Record the stored Closed wallet.
2. Confirm the view hides it, if the view is available.
3. Run initial sync for the same NRIC.
4. Compare stored wallets and status.

**Expected Result:**
> The existing wallet remains Closed and no replacement is created. Not appearing in the view does not mean the account was deleted.

---

#### `TC-R1-026`: Create only one account for identical duplicate records

- **Scenario ID**: `TS-R1-02`
- **Test Suite**: Data validation and duplicate prevention
- **Page / Target**: `Backend job / API`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R1 FS v1.2 F01-AC12; §1.1.7.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: CR: one account per citizen. TD: reprocessing does not create duplicates.

**Preconditions:**
```text
Service clock: 15 October 2026, 12:00 SGT; fresh database. Return two copies of the same valid record. Use only a test HTTP source and isolated database; synthetic NRIC acceptance by the mock contract is pending.
```

**Test Data:**
```text
STU-R1-20 variant: DOB 2019-10-15; SingaporeCitizen; identical NRIC, name, DOB and other fields in both copies.
Base source records, overridden by the case variants above: STU-R1-20: NRIC="T9900020A"; FullName="R1 Mock Student 20"; DOB=2016-09-09; CitizenshipStatus=SingaporeCitizen; Gender=Female.
```

**Test Steps:**
1. Run the initial synchronisation.
2. Count wallets and opening transactions for the NRIC.

**Expected Result:**
> Exactly one wallet exists. The duplicate record does not create another wallet or another opening transaction.

---

#### `TC-R1-027`: Handle conflicting DOB values for one NRIC

- **Scenario ID**: `TS-R1-02`
- **Test Suite**: Data validation and duplicate prevention
- **Page / Target**: `Backend job / API`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R1 FS v1.2 F01 EF03; §1.1.7 and §1.1.10.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: CR: no duplicate account. WA: report conflicts. OPEN: conflict resolution and input-order behaviour.
- **Note**: v1.2 does not require both conflicting records to produce no wallet.

**Preconditions:**
```text
Service clock: 15 October 2026, 12:00 SGT; fresh database for each input order. The mock can return conflicting rows and an unrelated valid citizen. Use only a test HTTP source and isolated database; synthetic NRIC acceptance by the mock contract is pending.
```

**Test Data:**
```text
Two STU-R1-20 variants share one NRIC: DOB 2019-10-15 and 2019-10-16. STU-R1-02 is the unrelated valid record.
Base source records, overridden by the case variants above: STU-R1-20: NRIC="T9900020A"; FullName="R1 Mock Student 20"; DOB=2016-09-09; CitizenshipStatus=SingaporeCitizen; Gender=Female | STU-R1-02: NRIC="T9900002A"; FullName="R1 Mock Student 02"; DOB=2019-10-15; CitizenshipStatus=SingaporeCitizen; Gender=Female.
```

**Test Steps:**
1. Run the initial sync with the conflicting pair in one order.
2. Count wallets and read the conflict result.
3. Reset the database and run the pair in reverse order.
4. Compare wallet counts, selected DOB and conflict handling.

**Expected Result:**
> At most one wallet is created for the shared NRIC. Under the proposed rule, a data conflict is reported and unrelated valid processing continues. Record whether the pair is rejected or one row is selected; that choice is not agreed.

---

#### `TC-R1-020`: Reject an unparseable DOB without losing valid records

- **Scenario ID**: `TS-R1-02`
- **Test Suite**: Data validation and duplicate prevention
- **Page / Target**: `Backend job / API`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: R1 FS v1.2 F01-AC08 and F01 EF02; §1.1.3 and §1.1.9.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: TD: valid DOB is required. WA: per-record handling of a malformed response.
- **Note**: The current client deserialises the whole page. Agree how a malformed item is isolated; a typed DTO cannot represent this input.

**Preconditions:**
```text
Service clock: 15 October 2026, 12:00 SGT; fresh database. Use the real GovernmentCitizenClient with an HTTP mock, not a typed DateOnly fixture. Return the invalid record first and the valid STU-R1-02 record second. Use only a test HTTP source and isolated database; synthetic NRIC acceptance by the mock contract is pending.
```

**Test Data:**
```text
One raw response page contains a valid STU-R1-02 record and STU-R1-23 with "dateOfBirth":"not-a-date".
Base source records, overridden by the case variants above: STU-R1-02: NRIC="T9900002A"; FullName="R1 Mock Student 02"; DOB=2019-10-15; CitizenshipStatus=SingaporeCitizen; Gender=Female | STU-R1-23: NRIC="T9900023A"; FullName="R1 Mock Student 23"; DOB=not-a-date; CitizenshipStatus=SingaporeCitizen; Gender=Female.
```

**Test Steps:**
1. Return the raw response from the HTTP mock.
2. Run the initial synchronisation through the real client.
3. Check wallets for both records.
4. Read the parsing error and job result.
5. Check that the valid record after the error receives exactly one Active wallet.

**Expected Result:**
> The malformed record creates no wallet. Under the proposed isolation rule, the later valid record receives exactly one Active wallet and the parsing failure is reported.

---

#### `TC-R1-076`: Daily sync includes leap-day birthdays under the proposed rule

- **Scenario ID**: `TS-R1-02`
- **Test Suite**: Data validation and duplicate prevention
- **Page / Target**: `Backend job / API`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: R1 FS v1.2 F01-AC02, F01-AC14; §1.1.5 and §1.1.6.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: WA: leap-year boundary and SGT processing. TD: seventh-birthday daily query.

**Preconditions:**
```text
Use the real daily client and an isolated SQL Server database. Control business time. Reset before each date; neither citizen has an account. Mock source filters by the actual query, not a forced return list.
```

**Test Data:**
```text
Synthetic citizen A: NRIC T9900076A, FullName R1 Mock Leap Citizen, DOB 2020-02-29, SingaporeCitizen, Gender=Female. Citizen B: NRIC T9900176A, FullName R1 Mock February Citizen, DOB 2020-02-28, SingaporeCitizen, Gender=Female. Mock NRIC acceptance pending.
```

**Test Steps:**
1. Run daily sync at 27 February 2027, 12:00 SGT without overriding the DOB query.
2. Capture query conditions and check wallets for A and B.
3. Reset the database and run daily sync at 28 February 2027, 12:00 SGT.
4. Capture query conditions and returned citizens; read both wallets.

**Expected Result:**
> Neither receives an account on 27 February. Under the proposed leap-year rule, the 28 February query retrieves both citizens and creates exactly one Active wallet per citizen with SGD 0.00. No test-only widening of the query is used.

---


### Test Suite: Job failure, recovery and audit

#### `TC-R1-028`: Rerunning initial sync preserves existing accounts

- **Scenario ID**: `TS-R1-03`
- **Test Suite**: Job failure, recovery and audit
- **Page / Target**: `Backend job / API`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R1 FS v1.2 F01-AC12; §1.1.7 and §2.4; local SYNC-04; received performance X1.3.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: TD: safe reprocessing and sync audit. WA: initial backfill of the older citizen.

**Preconditions:**
```text
Service clock: 15 October 2026, 12:00 SGT. Use an isolated database. The initial mock contains only STU-R1-02 and STU-R1-13; neither has an account before the first run. Use only a test HTTP source and isolated database; synthetic NRIC acceptance by the mock contract is pending.
```

**Test Data:**
```text
STU-R1-02: DOB 2019-10-15. STU-R1-13: DOB 2015-01-10. Both SingaporeCitizen; source values stay unchanged between runs.
Base source records, overridden by the case variants above: STU-R1-02: NRIC="T9900002A"; FullName="R1 Mock Student 02"; DOB=2019-10-15; CitizenshipStatus=SingaporeCitizen; Gender=Female | STU-R1-13: NRIC="T9900013A"; FullName="R1 Mock Student 13"; DOB=2015-01-10; CitizenshipStatus=SingaporeCitizen; Gender=Female.
```

**Test Steps:**
1. Run initial synchronisation once over these two records.
2. Record wallet IDs, balances, statuses, creation timestamps and transaction counts.
3. Run initial synchronisation again with the identical source response.
4. Compare accounts and transactions with the snapshot.
5. Check for a separate processing record for the rerun.

**Expected Result:**
> No additional account or opening transaction is created. Existing account fields and balances stay unchanged. The rerun has its own processing record.

---

#### `TC-R1-029`: Rerunning daily sync does not duplicate accounts

- **Scenario ID**: `TS-R1-03`
- **Test Suite**: Job failure, recovery and audit
- **Page / Target**: `Backend job / API`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R1 FS v1.2 F01-AC12; §2.4; received security SR-1.6; received performance X1.3.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: TD: safe reprocessing and sync audit.

**Preconditions:**
```text
Service clock: 15 October 2026, 12:00 SGT; a daily cycle has created the birthday account. Keep the clock and source data unchanged. Use only a test HTTP source and isolated database; synthetic NRIC acceptance by the mock contract is pending.
```

**Test Data:**
```text
STU-R1-02; the same DOB query and response as the first daily cycle.
Base source records, overridden by the case variants above: STU-R1-02: NRIC="T9900002A"; FullName="R1 Mock Student 02"; DOB=2019-10-15; CitizenshipStatus=SingaporeCitizen; Gender=Female. DOB 2019-10-15; SingaporeCitizen; the existing wallet is Active with SGD 0.00.
```

**Test Steps:**
1. Record account fields and transaction count.
2. Run the same daily cycle again.
3. Compare accounts and transactions.
4. Read the new processing record.

**Expected Result:**
> No duplicate account or opening transaction is created. Existing balance, status and creation timestamp stay unchanged; the second run is recorded.

---

#### `TC-R1-036`: Report the outcome of every record in a mixed run

- **Scenario ID**: `TS-R1-03`
- **Test Suite**: Job failure, recovery and audit
- **Page / Target**: `Backend job / API`
- **Severity / Priority**: `S2` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R1 FS v1.2 §2.4; local SYNC-05; received security SE1.3.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: TD: processing audit. Proposed: outcome counts. WA: category meanings and coverage marker.
- **Note**: The schema stores only total_records. The current cron also counts an idempotent enrolment response as enrolled; agree the meaning of success.

**Preconditions:**
```text
Service clock: 15 October 2026, 12:00 SGT. Use an isolated database and initial synchronisation. Agree the proposed count categories before acceptance. Use only a test HTTP source and isolated database; synthetic NRIC acceptance by the mock contract is pending.
```

**Test Data:**
```text
Exactly four source records: STU-R1-02, DOB 2019-10-15, SingaporeCitizen, no account; STU-R1-03, DOB 2016-05-20, SingaporeCitizen, existing Active wallet with SGD 100.00; STU-R1-17, DOB 2016-09-09, blank NRIC; STU-R1-09, DOB 2019-10-15, PermanentResident, no account.
Base source records, overridden by the case variants above: STU-R1-02: NRIC="T9900002A"; FullName="R1 Mock Student 02"; DOB=2019-10-15; CitizenshipStatus=SingaporeCitizen; Gender=Female | STU-R1-03: NRIC="T9900003A"; FullName="R1 Mock Student 03"; DOB=2016-05-20; CitizenshipStatus=SingaporeCitizen; Gender=Female | STU-R1-17: NRIC=""; FullName="R1 Mock Student 17"; DOB=2016-09-09; CitizenshipStatus=SingaporeCitizen; Gender=Female | STU-R1-09: NRIC="T9900009A"; FullName="R1 Mock Student 09"; DOB=2019-10-15; CitizenshipStatus=PermanentResident; Gender=Female.
```

**Test Steps:**
1. Run initial synchronisation with the mock returning exactly these four records.
2. Read the persisted job row and record results.
3. Compare totals with the fixture outcomes.
4. Check start/end timestamps and the invalid-record reason.
5. Record the coverage marker if agreed.

**Expected Result:**
> Under the proposed categories: total 4, newly created 1, failed 1 and skipped 2; counts sum to 4. Start/end and the applicable failure reason are recorded. Coverage reflects only dates actually processed.

---

#### `TC-R1-030`: Record a government API authentication failure

- **Scenario ID**: `TS-R1-03`
- **Test Suite**: Job failure, recovery and audit
- **Page / Target**: `Backend job / API`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: R1 FS v1.2 F01 EF01; §1.1.2, §1.1.9 and §2.4; local SYNC-03.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: TD: authenticated source access. WA: operational failure policy.
- **Note**: The current client returns an empty list for a non-success HTTP response. Test the real client, not a substitute that throws instead.

**Preconditions:**
```text
Service clock: 15 October 2026, 12:00 SGT; fresh database. Keep the real GovernmentCitizenClient and configure the HTTP mock to reject the first page.
```

**Test Data:**
```text
HTTP 401 from the government mock; no citizen data returned.
```

**Test Steps:**
1. Run one real sync cycle through the HTTP client.
2. Read job status and failure reason.
3. Check whether any wallet was created.

**Expected Result:**
> Under the proposed failure policy, the run is Failed with an authentication reason, and no wallet is created. An empty response must not be mistaken for a successful fetch.

---

#### `TC-R1-031`: Retry once after a government API timeout

- **Scenario ID**: `TS-R1-03`
- **Test Suite**: Job failure, recovery and audit
- **Page / Target**: `Backend job / API`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: R1 FS v1.2 §1.1.9; local SYNC-03.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: WA: one retry after 15 minutes.
- **Note**: Control the retry delay as well as date reads. The current job has no retry mechanism.

**Preconditions:**
```text
Fresh database; service clock and retry timer are controllable. The proposed retry policy is agreed or observed. Use only a test HTTP source and isolated database; synthetic NRIC acceptance by the mock contract is pending. Set the service clock to 15 October 2026, 12:00 SGT for both attempts.
```

**Test Data:**
```text
First HTTP request times out; the retry returns STU-R1-02. Proposed delay: 15 minutes.
Base source records, overridden by the case variants above: STU-R1-02: NRIC="T9900002A"; FullName="R1 Mock Student 02"; DOB=2019-10-15; CitizenshipStatus=SingaporeCitizen; Gender=Female. STU-R1-02 has no account before the timeout.
```

**Test Steps:**
1. Start the real job with the timeout configured.
2. Advance the fake clock to just before the retry deadline.
3. Check that no early retry occurs.
4. Advance to the deadline and capture the next request.
5. Read the wallet and processing result.

**Expected Result:**
> Under the proposed policy, exactly one retry occurs after 15 minutes, creates the eligible account once, and records the timeout and final outcome.

---

#### `TC-R1-032`: Recover missed dates after the retry also fails

- **Scenario ID**: `TS-R1-03`
- **Test Suite**: Job failure, recovery and audit
- **Page / Target**: `Backend job / API`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: R1 FS v1.2 F01-AC11 and F01 EF04; §1.1.5, §1.1.9 and §2.4.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: WA: retry policy, missed-day recovery and coverage marker.
- **Note**: The current job lacks retry and catch-up logic. Record the gap without inventing a recovery result.

**Preconditions:**
```text
An isolated run last succeeded for 14 October. Fix time to 15 October 2026 SGT; the service clock and retry timer are controllable. Use only a test HTTP source and isolated database; synthetic NRIC acceptance by the mock contract is pending.
```

**Test Data:**
```text
Both 15 October attempts time out. On 16 October the source contains STU-R1-02, DOB 2019-10-15, and STU-R1-01, DOB 2019-10-16.
Base source records, overridden by the case variants above: STU-R1-02: NRIC="T9900002A"; FullName="R1 Mock Student 02"; DOB=2019-10-15; CitizenshipStatus=SingaporeCitizen; Gender=Female | STU-R1-01: NRIC="T9900001A"; FullName="R1 Mock Student 01"; DOB=2019-10-16; CitizenshipStatus=SingaporeCitizen; Gender=Female.
```

**Test Steps:**
1. Trigger the first failed attempt and advance through the proposed retry.
2. Read failure status, reason and coverage.
3. Restore the source and advance to the next scheduled run.
4. Capture all DOB queries.
5. Check accounts for both missed and current birthdays.

**Expected Result:**
> Under the proposed recovery policy, the failed run does not advance successful coverage. The next run processes 15 and 16 October and creates each eligible account once.

---

#### `TC-R1-033`: Recover a completely missed daily run

- **Scenario ID**: `TS-R1-03`
- **Test Suite**: Job failure, recovery and audit
- **Page / Target**: `Backend job / API`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: R1 FS v1.2 F01-AC11 and F01 EF04; §1.1.5; local SYNC-07.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: WA: missed-day recovery.

**Preconditions:**
```text
Successful coverage ends on 14 October. Pause the owned scheduler before 15 October midnight SGT; use an isolated clock. Use only a test HTTP source and isolated database; synthetic NRIC acceptance by the mock contract is pending.
```

**Test Data:**
```text
STU-R1-02 has its birthday on 15 October; STU-R1-01 has its birthday on 16 October.
Base source records, overridden by the case variants above: STU-R1-02: NRIC="T9900002A"; FullName="R1 Mock Student 02"; DOB=2019-10-15; CitizenshipStatus=SingaporeCitizen; Gender=Female | STU-R1-01: NRIC="T9900001A"; FullName="R1 Mock Student 01"; DOB=2019-10-16; CitizenshipStatus=SingaporeCitizen; Gender=Female.
```

**Test Steps:**
1. Keep the scheduler stopped for the entire 15 October run.
2. Advance the fake clock to the next scheduled run on 16 October.
3. Resume the real scheduler.
4. Capture DOB queries and read both accounts.

**Expected Result:**
> Under the proposed recovery policy, both the missed and current birthday are processed with one wallet per citizen.

---

#### `TC-R1-034`: Interrupting a job does not leave partial accounts

- **Scenario ID**: `TS-R1-03`
- **Test Suite**: Job failure, recovery and audit
- **Page / Target**: `Backend job / API`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: R1 FS v1.2 §1.1.9 and §2.4; received security SR-1.6, SE1.6; local SYNC-03.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: TD: no incomplete account and no duplicate after reprocessing. Derived security check; approval pending.

**Preconditions:**
```text
Use an owned disposable service instance, isolated SQL Server and an agreed interruption point. Some records can commit before interruption.
```

**Test Data:**
```text
Three distinct synthetic citizens turning 7 on 15 October, with otherwise valid fields; record all NRICs before the test.
```

**Test Steps:**
1. Start the real job.
2. Interrupt the owned instance after one record commits and while another is processing.
3. Inspect persisted wallets, student links and balances.
4. Restart the instance and rerun the same data.
5. Compare wallets with the eligible source records.

**Expected Result:**
> No partially created wallet remains. After rerun, each eligible citizen has exactly one complete wallet; committed balances are not reset.

---

#### `TC-R1-035`: The scheduler runs on weekends and public holidays

- **Scenario ID**: `TS-R1-03`
- **Test Suite**: Job failure, recovery and audit
- **Page / Target**: `Backend job / API`
- **Severity / Priority**: `S3` / `Low`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: R1 FS v1.2 F01-AC13; §1.1.2.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: WA: midnight SGT schedule and weekend/holiday operation.
- **Note**: The existing Task.Delay is not clock-aware. Date injection alone cannot prove scheduler behaviour.

**Preconditions:**
```text
Use the real hosted scheduler with provider-aware delays. Agree the weekend/holiday policy and confirm the holiday fixture date.
```

**Test Data:**
```text
Weekend fixture: 17 October 2026 SGT, DOB 2019-10-17. Holiday fixture: 25 December 2026 SGT, DOB 2019-12-25. Reset before each fixture.
```

**Test Steps:**
1. Start the scheduler just before each fixture's Singapore midnight.
2. Advance the fake clock across midnight without calling the cycle method.
3. Capture the automatic source request and job log.
4. Check the birthday account.

**Expected Result:**
> Under the proposed schedule, one automatic run occurs at each midnight and creates the eligible account. No manual sync call is used to prove triggering.

---


### Test Suite: Closure and balance handling

#### `TC-R1-037`: Keep the account Active one day before age 16

- **Scenario ID**: `TS-R1-04`
- **Test Suite**: Closure and balance handling
- **Page / Target**: `Account eligibility API`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R1 FS v1.2 F02-AC01 and F02-BR02; §1.2.5.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: TD: backend-triggered eligibility check. CR: closure age is 16.

**Preconditions:**
```text
Service clock: 15 October 2026, 12:00 SGT; STU-R1-21 has an Active wallet. The real backend eligibility path is available. Use only a test HTTP source and isolated database; synthetic NRIC acceptance by the mock contract is pending.
```

**Test Data:**
```text
STU-R1-21: DOB 2010-10-16; Singapore Citizen; balance SGD 100.00.
Base source records, overridden by the case variants above: STU-R1-21: NRIC="T9900021A"; FullName="R1 Mock Student 21"; DOB=2010-10-16; CitizenshipStatus=SingaporeCitizen; Gender=Female.
```

**Test Steps:**
1. Read the account through the backend eligibility path.
2. Read stored status, balance and Actual Account Closure Date.

**Expected Result:**
> The wallet remains Active with balance SGD 100.00. No closure is performed or recorded.

---

#### `TC-R1-038`: Close a zero-balance account on access at age 16

- **Scenario ID**: `TS-R1-04`
- **Test Suite**: Closure and balance handling
- **Page / Target**: `Account eligibility API`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R1 FS v1.2 F02-AC02, F02-BR01 and F02-BR02; §2.2.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: CR: close at 16. TD: closure on backend access. WA: storing Actual Account Closure Date.
- **Note**: Check the missing closure timestamp separately; it must not prevent testing the status transition.

**Preconditions:**
```text
Service clock: 15 October 2026, 12:00 SGT; STU-R1-22 is Active with zero balance. The backend account read triggers eligibility checking. Use only a test HTTP source and isolated database; synthetic NRIC acceptance by the mock contract is pending.
```

**Test Data:**
```text
STU-R1-22: DOB 2010-10-15; Singapore Citizen; balance SGD 0.00.
Base source records, overridden by the case variants above: STU-R1-22: NRIC="T9900022A"; FullName="R1 Mock Student 22"; DOB=2010-10-15; CitizenshipStatus=SingaporeCitizen; Gender=Female.
```

**Test Steps:**
1. Read the account through the real backend path.
2. Inspect the returned account state.
3. Read stored status, balance and closure evidence.

**Expected Result:**
> Closure finishes before the response is returned. Wallet status is Closed and balance is SGD 0.00. Under the closure-date rule, Actual Account Closure Date records this access.

---

#### `TC-R1-042`: Repeated access does not close the account again

- **Scenario ID**: `TS-R1-04`
- **Test Suite**: Closure and balance handling
- **Page / Target**: `Account eligibility API`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R1 FS v1.2 F02-AC06, F02-BR09; §2.2.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: WA: duplicate-closure safeguard and timestamp storage; F02-AC06 states the repeated-access outcome.
- **Note**: If the closure timestamp is absent, report that gap separately from repeated-access behaviour.

**Preconditions:**
```text
Service clock: 15 October 2026, 12:00 SGT; STU-R1-14 is already Closed with zero balance. Record existing closure evidence before access. Use only a test HTTP source and isolated database; synthetic NRIC acceptance by the mock contract is pending.
```

**Test Data:**
```text
STU-R1-14; original closure timestamp and closure-record count, if available.
Base source records, overridden by the case variants above: STU-R1-14: NRIC="T9900014A"; FullName="R1 Mock Student 14"; DOB=2009-06-01; CitizenshipStatus=SingaporeCitizen; Gender=Female. DOB 2009-06-01; SingaporeCitizen; Closed wallet with SGD 0.00; preserve its stored closure timestamp.
```

**Test Steps:**
1. Record wallet status and closure evidence.
2. Read the account twice through the eligibility path.
3. Compare status, closure-record count and Actual Account Closure Date.

**Expected Result:**
> The wallet remains Closed. No additional closure is performed. Under the timestamp rule, Actual Account Closure Date is unchanged.

---

#### `TC-R1-039`: Close an overdue zero-balance account when HQ retrieves it

- **Scenario ID**: `TS-R1-04`
- **Test Suite**: Closure and balance handling
- **Page / Target**: `Account eligibility API`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: R1 FS v1.2 F02-AC03; §1.2.5 and §2.2.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: TD: overdue closure on access. WA: actual closure timestamp.

**Preconditions:**
```text
Service clock: 15 October 2026, 12:00 SGT; STU-R1-07 is Active with zero balance and has not been accessed since its sixteenth birthday. Use an authorised HQ identity. Use only a test HTTP source and isolated database; synthetic NRIC acceptance by the mock contract is pending.
```

**Test Data:**
```text
STU-R1-07 variant: DOB 2009-03-01; Active; balance SGD 0.00.
Base source records, overridden by the case variants above: STU-R1-07: NRIC="T9900007A"; FullName="R1 Mock Student 07"; DOB=2009-03-01; CitizenshipStatus=SingaporeCitizen; Gender=Female.
```

**Test Steps:**
1. Confirm the stored account is Active before backend access.
2. Retrieve it through the real HQ/backend account path.
3. Read status, balance and closure evidence.

**Expected Result:**
> The overdue account closes on this access, not retroactively on the birthday. Balance stays SGD 0.00. Under the closure-date rule, the actual timestamp is this access time.

---

#### `TC-R1-040`: Refuse a top-up when the holder has reached 16

- **Scenario ID**: `TS-R1-04`
- **Test Suite**: Closure and balance handling
- **Page / Target**: `Account eligibility API`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: R1 FS v1.2 F02-AC04 and F02 AF04.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: TD: top-up invokes closure eligibility. CR: close at 16.
- **Note**: ProcessTopUp uses EducationAccount while lifecycle uses Wallet. Confirm deployed tables and mapping; a missing-table error is not an eligibility pass.

**Preconditions:**
```text
Service clock: 15 October 2026, 12:00 SGT; STU-R1-22 is Active with zero balance. Use a valid authorised top-up request and confirm the deployed top-up/account schema. Use only a test HTTP source and isolated database; synthetic NRIC acceptance by the mock contract is pending.
```

**Test Data:**
```text
STU-R1-22; top-up SGD 10.00; new reference R1-040-TOPUP.
Base source records, overridden by the case variants above: STU-R1-22: NRIC="T9900022A"; FullName="R1 Mock Student 22"; DOB=2010-10-15; CitizenshipStatus=SingaporeCitizen; Gender=Female. DOB 2010-10-15; SingaporeCitizen; Active wallet; SGD 0.00.
```

**Test Steps:**
1. Record account state and ledger count.
2. Submit the request through the real top-up path.
3. Read the response and eligibility result.
4. Compare stored balances, account states and transactions.

**Expected Result:**
> Eligibility is checked before funds are added. The request is refused because the holder is 16; no successful top-up is stored. The zero-balance account follows the closure path.

---

#### `TC-R1-041`: Refuse payment when the holder has reached 16

- **Scenario ID**: `TS-R1-04`
- **Test Suite**: Closure and balance handling
- **Page / Target**: `Account eligibility API`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: R1 FS v1.2 F02-AC05 and F02 AF04; received security SR-1.4, SE1.4.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: TD: payment invokes closure eligibility. WA: handling the positive balance without CPF.
- **Note**: The payment-service call into eligibility is untraced. Calling debit on an already Closed wallet does not prove this integration.

**Preconditions:**
```text
Service clock: 15 October 2026, 12:00 SGT; STU-R1-06 is Active with sufficient funds. Parent authorisation, the charge and payment request are otherwise valid. Use only a test HTTP source and isolated database; synthetic NRIC acceptance by the mock contract is pending.
```

**Test Data:**
```text
STU-R1-06: balance SGD 150.00; payable charge SGD 10.00; new FundingReference R1-041-PAY.
Base source records, overridden by the case variants above: STU-R1-06: NRIC="T9900006A"; FullName="R1 Mock Student 06"; DOB=2010-10-15; CitizenshipStatus=SingaporeCitizen; Gender=Female. DOB 2010-10-15; SingaporeCitizen; Active wallet.
```

**Test Steps:**
1. Record balance, account state and ledger count.
2. Submit an education-balance payment through the real payment service.
3. Read the eligibility result and payment response.
4. Compare balance and ledger entries.

**Expected Result:**
> Payment is refused because the holder has reached 16, not because funds or authorisation are missing. Balance stays SGD 150.00 and no successful debit is recorded.

---

#### `TC-R1-043`: Keep Closed account history readable to its authorised parent

- **Scenario ID**: `TS-R1-04`
- **Test Suite**: Closure and balance handling
- **Page / Target**: `Account eligibility API`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: R1 FS v1.2 F02-AC07, F02-BR07 and F02-BR08; FS-08 v0.4 §4.2.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: TD: history retention and authorised viewing. WA: closed-account financial controls.

**Preconditions:**
```text
An authorised parent is linked to a Closed account. A second family has separate history. Top-up and payment interfaces are available.
```

**Test Data:**
```text
Closed account with prior credit SGD 150.00 and debit SGD 150.00; balance SGD 0.00. Another family has a distinct SGD 87.75 marker transaction.
```

**Test Steps:**
1. Read the Closed account history as its linked parent.
2. Check account and transaction identifiers in the response.
3. Attempt a top-up and a payment using otherwise valid requests.
4. Check for any accepted financial operation or foreign-family data.

**Expected Result:**
> The authorised parent can read retained history. No other family's data is returned. Top-up and payment are refused because the account is Closed.

---

#### `TC-R1-044`: Defer closure when a positive balance cannot transfer to CPF

- **Scenario ID**: `TS-R1-04`
- **Test Suite**: Closure and balance handling
- **Page / Target**: `Account eligibility API`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: R1 FS v1.2 F02-AC10 and F02 EF04; §1.2.7.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: WA: Closure Deferred safety rule. CPF transfer is deferred from the MVP.
- **Note**: Static code inspection found no balance guard before Wallet.Close. That is not an executed test result.

**Preconditions:**
```text
Service clock: 15 October 2026, 12:00 SGT; STU-R1-06 is Active and reaches 16. No CPF transfer path exists. Agree or observe the proposed Closure Deferred rule. Use only a test HTTP source and isolated database; synthetic NRIC acceptance by the mock contract is pending.
```

**Test Data:**
```text
STU-R1-06: balance SGD 150.00; payment SGD 10.00; top-up SGD 10.00; unique references for both requests.
Base source records, overridden by the case variants above: STU-R1-06: NRIC="T9900006A"; FullName="R1 Mock Student 06"; DOB=2010-10-15; CitizenshipStatus=SingaporeCitizen; Gender=Female. DOB 2010-10-15; SingaporeCitizen; the wallet starts Active.
```

**Test Steps:**
1. Read the account through the real eligibility path.
2. Read status, balance and transfer evidence.
3. Attempt the payment.
4. Attempt the top-up.
5. Compare account state, balance and ledger entries.

**Expected Result:**
> Under the proposed safety rule, closure is deferred rather than completed. Balance stays SGD 150.00, no CPF transfer is reported successful, and no new financial operation succeeds.

---

#### `TC-R1-045`: Handle a government-source failure during eligibility checking

- **Scenario ID**: `TS-R1-04`
- **Test Suite**: Closure and balance handling
- **Page / Target**: `Account eligibility API`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: R1 FS v1.2 F02-AC09 and F02 EF01; §1.2.3 and §1.2.8.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: TD: use current citizen data. WA: source-failure handling.
- **Note**: If no source lookup occurs, report missing integration. Do not claim that an unavailable source was exercised by a local-only check.

**Preconditions:**
```text
Service clock: 15 October 2026, 12:00 SGT; STU-R1-07 is Active with zero balance. Keep the real lookup client and configure its HTTP mock to fail. Use only a test HTTP source and isolated database; synthetic NRIC acceptance by the mock contract is pending.
```

**Test Data:**
```text
STU-R1-07 zero-balance variant; government lookup returns HTTP 503; otherwise valid account read and top-up SGD 10.00.
Base source records, overridden by the case variants above: STU-R1-07: NRIC="T9900007A"; FullName="R1 Mock Student 07"; DOB=2009-03-01; CitizenshipStatus=SingaporeCitizen; Gender=Female.
```

**Test Steps:**
1. Read the account through the real eligibility path.
2. Capture government requests and the failure response.
3. Submit the otherwise valid financial request.
4. Read account state and failure evidence.

**Expected Result:**
> Under the proposed failure rule, the source error is recorded, the account is not automatically closed, and financial actions requiring eligibility verification are blocked.

---

#### `TC-R1-051`: Review a citizenship change before age 16

- **Scenario ID**: `TS-R1-04`
- **Test Suite**: Closure and balance handling
- **Page / Target**: `Account eligibility API`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: R1 FS v1.2 F02 EF02; §1.2.6; local SYNC-06.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: WA: citizenship-change handling before 16.
- **Note**: A daily seventh-birthday query alone will not retrieve this existing holder. Exported status is not an agreed substitute for this rule.

**Preconditions:**
```text
Service clock: 15 October 2026, 12:00 SGT; STU-R1-15 is locally Singapore Citizen with an Active wallet and sufficient funds. The source now reports Permanent Resident. Use only a test HTTP source and isolated database; synthetic NRIC acceptance by the mock contract is pending.
```

**Test Data:**
```text
STU-R1-15: DOB 2014-07-07; balance SGD 100.00; payment SGD 10.00. Change only the source citizenship, not local data.
Base source records, overridden by the case variants above: STU-R1-15: NRIC="T9900015A"; FullName="R1 Mock Student 15"; DOB=2014-07-07; CitizenshipStatus=SingaporeCitizen; Gender=Female.
```

**Test Steps:**
1. Access the account through the real eligibility/data-refresh path.
2. Capture the current citizen lookup.
3. Read account state and any Eligibility Review Required record.
4. Attempt the otherwise valid payment.
5. Check for a replacement account.

**Expected Result:**
> Under the proposed rule, Eligibility Review Required is recorded, no age-based closure occurs, financial operations are blocked while eligibility is unverified, and no replacement account is created.

---

#### `TC-R1-075`: Closure uses the Singapore date when UTC is still yesterday

- **Scenario ID**: `TS-R1-04`
- **Test Suite**: Closure and balance handling
- **Page / Target**: `Account eligibility API`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: R1 FS v1.2 F02-BR01, F02-BR02, F02-AC02, F02-AC06; QA SGT assumption; §2.2.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: WA: SGT date for closure and actual closure timestamp. TD: backend-triggered check. CR: close at 16.
- **Note**: UTC date lag can delay closure, not make it early. Do not use UpdatedAt as proof of a dedicated Actual Account Closure Date.

**Preconditions:**
```text
Use the real eligibility path, isolated SQL Server and an injected TimeProvider. Pause the scheduler. Two independent Active Singapore Citizen accounts have zero balance.
```

**Test Data:**
```text
A DOB 2010-10-15; B DOB 2010-10-16. Times: 2026-10-14T15:59:59Z, 2026-10-14T16:00:00Z and 2026-10-15T00:00:00Z; SGT is UTC+8.
```

**Test Steps:**
1. Set the fake clock to 14 October 23:59:59 SGT and access A.
2. Advance to 15 October 00:00 SGT without backend access.
3. Read persisted A state directly to check that time alone did not close it.
4. Access A through the real eligibility path.
5. Access B at the same instant.
6. Advance to 15 October 08:00 SGT and access A again.
7. Compare status, balance and closure evidence.

**Expected Result:**
> Under the proposed SGT rule, A is Active before midnight and until backend access occurs; the first access after midnight closes A with zero balance. B stays Active because its birthday is tomorrow. Repeated access does not duplicate closure; the proposed actual closure timestamp stays unchanged.

---

#### `TC-R1-078`: Closure persistence failure leaves a consistent account

- **Scenario ID**: `TS-R1-04`
- **Test Suite**: Closure and balance handling
- **Page / Target**: `Account eligibility API`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: R1 FS v1.2 F02 EF03; §1.2.3 and §2.2.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: R1 F02 EF03: failure reporting and consistent state. TD: access-triggered closure. WA: actual closure timestamp storage.

**Preconditions:**
```text
Use isolated SQL Server and the real account-access path. A SingaporeCitizen holder, DOB 2010-10-15, has an Active wallet with SGD 0.00. Service clock: 15 October 2026, 12:00 SGT. Agree a deterministic fault before closure commit.
```

**Test Data:**
```text
One controlled closure commit failure; authorised parent account read. Record initial status, balance and any closure timestamp before injecting the fault.
```

**Test Steps:**
1. Enable the fault and access the account to trigger closure.
2. Capture the failure response and failure evidence.
3. Read persisted state directly through SQL so inspection cannot trigger another closure.
4. Disable the fault and access the account again.
5. Read persisted status, balance and closure evidence.

**Expected Result:**
> The failed attempt records failure and leaves the wallet Active with SGD 0.00, without a committed completed-closure result or timestamp. The later successful access closes it once with SGD 0.00. No partial or contradictory state remains.

---


### Test Suite: Wallet and ledger contracts

#### `TC-R1-052`: Check the opening wallet and any opening transaction

- **Scenario ID**: `TS-R1-05`
- **Test Suite**: Wallet and ledger contracts
- **Page / Target**: `Wallet API / ledger`
- **Severity / Priority**: `S3` / `Low`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R1 FS v1.2 §1.1.8, §2.2 and §2.3 Scope Note.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: WA: opening transaction only by team decision. TD: creation flow and zero initial balance in acceptance criteria.
- **Note**: Opening-row policy is pending. TC-R1-066 checks identifiers in free-text descriptions.

**Preconditions:**
```text
Service clock: 15 October 2026, 12:00 SGT; fresh database; one valid birthday citizen. Record the team decision on opening transactions if one exists. Use only a test HTTP source and isolated database; synthetic NRIC acceptance by the mock contract is pending.
```

**Test Data:**
```text
STU-R1-02; one creation run; no prior transactions.
Base source records, overridden by the case variants above: STU-R1-02: NRIC="T9900002A"; FullName="R1 Mock Student 02"; DOB=2019-10-15; CitizenshipStatus=SingaporeCitizen; Gender=Female.
```

**Test Steps:**
1. Run the real creation flow.
2. Read balance, currency and opening transaction rows.
3. Record each opening row's amount, direction, status and description.

**Expected Result:**
> The wallet starts at SGD 0.00 with currency SGD. R1 v1.2 does not require F01 to create an opening transaction unless the team decides otherwise. Record any opening row; judge its presence, amount and fields only against a documented team decision.

---

#### `TC-R1-053`: Keep cent-level precision across credits

- **Scenario ID**: `TS-R1-05`
- **Test Suite**: Wallet and ledger contracts
- **Page / Target**: `Wallet API / ledger`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R1 FS v1.2 §2.3 Monetary values rule.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: TD: two-decimal SGD monetary precision.

**Preconditions:**
```text
Service clock: 15 October 2026, 12:00 SGT; Active under-16 wallet with balance SGD 0.00. Credit requests are authorised and otherwise valid.
```

**Test Data:**
```text
Credit SGD 0.10 with R1-053-A; credit SGD 0.20 with R1-053-B.
```

**Test Steps:**
1. Submit the first credit.
2. Submit the second credit.
3. Read balance and transaction amounts as decimals.
4. Inspect the stored money types and decimal scale.

**Expected Result:**
> Balance is exactly SGD 0.30, with separate SGD 0.10 and SGD 0.20 entries. Money retains two-decimal SGD precision without integer truncation or floating-point drift.

---

#### `TC-R1-054`: Refuse a debit larger than the balance

- **Scenario ID**: `TS-R1-05`
- **Test Suite**: Wallet and ledger contracts
- **Page / Target**: `Wallet API / ledger`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R1 FS v1.2 §2.3 Negative Account Balance rule.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: WA: negative balance is not supported.

**Preconditions:**
```text
Service clock: 15 October 2026, 12:00 SGT; an Active under-16 wallet has SGD 50.00. The request is authorised and otherwise valid.
```

**Test Data:**
```text
Debit SGD 50.01; fresh FundingReference R1-054-DEBIT.
```

**Test Steps:**
1. Record balance and ledger state.
2. Submit the debit.
3. Read the refusal and stored balance.
4. Check for any successful debit entry.

**Expected Result:**
> Under the no-negative-balance rule, the debit is refused for insufficient funds. Balance remains SGD 50.00 and no successful or partial debit is committed.

---

#### `TC-R1-056`: Refuse credit and debit on Closed or Closure Deferred accounts

- **Scenario ID**: `TS-R1-05`
- **Test Suite**: Wallet and ledger contracts
- **Page / Target**: `Wallet API / ledger`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R1 FS v1.2 F02-BR07; §1.2.7; received security SR-1.4, SE1.4.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: WA: closed-account financial controls and Closure Deferred representation/safety.
- **Note**: Confirm how Closure Deferred is represented. Do not invent an enum value or mistake insufficient funds for a state-based refusal.

**Preconditions:**
```text
Two isolated fixtures exist: a legacy Closed wallet and a wallet in the agreed Closure Deferred state. Both have enough balance for the debit; requests are authorised.
```

**Test Data:**
```text
Closed wallet balance SGD 100.00; Closure Deferred balance SGD 150.00. Credit and debit SGD 10.00 each with four fresh references.
```

**Test Steps:**
1. Record balances, states and ledger counts.
2. Submit a credit to each account.
3. Submit a debit to each account.
4. Read refusals and compare all stored values.

**Expected Result:**
> Under the agreed state rules, all four requests are refused because of account state. No balance changes, successful transactions or reopening occur.

---

#### `TC-R1-058`: Reject wallet requests without authentication

- **Scenario ID**: `TS-R1-05`
- **Test Suite**: Wallet and ledger contracts
- **Page / Target**: `Wallet API / ledger`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R1 FS v1.2 §1.2.2; local SEC-01.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: WA: server-side authentication policy; local security draft.

**Preconditions:**
```text
An existing Active under-16 wallet has SGD 100.00. Use valid wallet IDs and request bodies, but no token, session cookie or process credential.
```

**Test Data:**
```text
Wallet read and debit SGD 1.00 with R1-058-DEBIT; no authentication.
```

**Test Steps:**
1. Send the wallet read request without credentials.
2. Send the debit request without credentials.
3. Read both responses.
4. Check the stored balance and ledger.

**Expected Result:**
> Both requests receive the agreed authentication refusal, not a missing-route/account error. No holder or balance data is returned and no debit occurs.

---

#### `TC-R1-055`: A failed credit does not change the balance

- **Scenario ID**: `TS-R1-05`
- **Test Suite**: Wallet and ledger contracts
- **Page / Target**: `Wallet API / ledger`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: R1 FS v1.2 §2.3 Failed Transaction rule.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: WA: failed transactions leave balances unchanged. OPEN: failed-row and reason retention.
- **Note**: Use a real commit failure, not just a validation rejection. Do not require a failed row that the contract has not agreed.

**Preconditions:**
```text
Use isolated SQL Server and an Active under-16 wallet with SGD 100.00. Inject a failure after request validation but before the unit-of-work commit completes.
```

**Test Data:**
```text
Credit SGD 10.00; reference R1-055-CREDIT; one controlled commit failure.
```

**Test Steps:**
1. Record the wallet and transaction rows.
2. Submit the credit with the commit failure enabled.
3. Read the failure result.
4. Compare balance and committed ledger entries.
5. Record whether a separate failure audit exists.

**Expected Result:**
> No successful credit is committed and balance remains SGD 100.00. The failed transaction does not affect the balance. Retention of a failed ledger row and its reason is recorded until the policy is agreed.

---

#### `TC-R1-057`: Debit and reversal are idempotent by FundingReference

- **Scenario ID**: `TS-R1-05`
- **Test Suite**: Wallet and ledger contracts
- **Page / Target**: `Wallet API / ledger`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: FS Function 9 dated 2026-10-14: EA ledger contract and §2.1 business rules; R1 FS v1.2 §2.3.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: R9 contract: atomic, idempotent debit and reversal by FundingReference. API field mapping remains an integration dependency.
- **Note**: This is sequential idempotency coverage. A controlled concurrent-reference SQL Server test is still needed; application lookups alone do not prove it.

**Preconditions:**
```text
An Active under-16 wallet has SGD 100.00. Agree the R9 FundingReference mapping to the wallet and reversal API fields.
```

**Test Data:**
```text
Debit SGD 40.00 with R1-057-DEBIT. Repeat the same body. Reverse the returned original transaction using R1-057-REV, if the reversal contract requires a reference.
```

**Test Steps:**
1. Submit the debit and record its transaction ID.
2. Repeat the identical debit.
3. Read balance and effective debit count.
4. Reverse the original debit through the agreed API.
5. Repeat the identical reversal request.
6. Read balance and effective reversal count.

**Expected Result:**
> The debit reduces balance to SGD 60.00 once. The reversal restores SGD 100.00 once. Repeats have no additional financial effect; the ledger shows one effective debit and one effective reversal.

---


### Test Suite: Cross-function seams

#### `TC-R1-059`: Display the agreed portal state for each account condition

- **Scenario ID**: `TS-R1-06`
- **Test Suite**: Cross-function seams
- **Page / Target**: `Parent / school / payment integration`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: FS-08 v0.4 §4.2 and §6.2; R1 FS v1.2 §1.2.7 and §3.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: R8 draft state mapping. OPEN: mapping Closure Deferred to Due for closure and resolving displayed-date conflicts with R1.
- **Note**: R1 does not store Scheduled Closure Date. Do not accept R8 date wording as an agreed R1 persistence requirement.

**Preconditions:**
```text
R8 is available and its state mapping is agreed. Each test parent is authorised for the tested child; no parent is assumed to own unrelated fixtures. Use only a test HTTP source and isolated database; synthetic NRIC acceptance by the mock contract is pending. Fix the service clock to 15 October 2026, 12:00 SGT.
```

**Test Data:**
```text
Six separate conditions: Active STU-R1-13; due at 16 with balance STU-R1-06; Closed STU-R1-14; age-7/no-account STU-R1-02; under-7 STU-R1-01; non-citizen/no-account STU-R1-10.
Base source records, overridden by the case variants above: STU-R1-13: NRIC="T9900013A"; FullName="R1 Mock Student 13"; DOB=2015-01-10; CitizenshipStatus=SingaporeCitizen; Gender=Female | STU-R1-06: NRIC="T9900006A"; FullName="R1 Mock Student 06"; DOB=2010-10-15; CitizenshipStatus=SingaporeCitizen; Gender=Female | STU-R1-14: NRIC="T9900014A"; FullName="R1 Mock Student 14"; DOB=2009-06-01; CitizenshipStatus=SingaporeCitizen; Gender=Female | STU-R1-02: NRIC="T9900002A"; FullName="R1 Mock Student 02"; DOB=2019-10-15; CitizenshipStatus=SingaporeCitizen; Gender=Female | STU-R1-01: NRIC="T9900001A"; FullName="R1 Mock Student 01"; DOB=2019-10-16; CitizenshipStatus=SingaporeCitizen; Gender=Female | STU-R1-10: NRIC="T9900010A"; FullName="R1 Mock Student 10"; DOB=2015-08-10; CitizenshipStatus=ForeignStudent; Gender=Female. Active: DOB 2015-01-10, SGD 250.00; due: DOB 2010-10-15, SGD 150.00; Closed: DOB 2009-06-01, SGD 0.00; no-account/age-7: DOB 2019-10-15; under-7: DOB 2019-10-16; non-citizen: DOB 2015-08-10, ForeignStudent.
```

**Test Steps:**
1. Sign in as the authorised parent for each condition.
2. Open the child's account view.
3. Compare the display and available actions with backend state.
4. Check that children with no wallet do not show a fabricated balance.

**Expected Result:**
> Under the R8 contract, the view distinguishes Active, Due for closure, Closed, To be created, Not yet 7 and Not eligible. No nonexistent wallet balance is displayed. Closed/due holders have no financial actions.

---

#### `TC-R1-060`: Parent sign-in reuses an account already created by R1

- **Scenario ID**: `TS-R1-06`
- **Test Suite**: Cross-function seams
- **Page / Target**: `Parent / school / payment integration`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: R1 FS v1.2 §1.1.7 and §3; FS-08 v0.4 §4.1.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: TD: shared identity and no duplicate account. R8 refresh behaviour follows its contract.

**Preconditions:**
```text
R8 sign-in refresh is available. STU-R1-03 has an existing wallet and the synthetic parent is authorised for that child. Use only a test HTTP source and isolated database; synthetic NRIC acceptance by the mock contract is pending. The existing wallet is Active; DOB 2016-05-20; FatherNric=T9901001A; MotherNric=T9901002A.
```

**Test Data:**
```text
STU-R1-03 with the same source NRIC and parent identifiers in both services; balance SGD 100.00.
Base source records, overridden by the case variants above: STU-R1-03: NRIC="T9900003A"; FullName="R1 Mock Student 03"; DOB=2016-05-20; CitizenshipStatus=SingaporeCitizen; Gender=Female.
```

**Test Steps:**
1. Record student, wallet and relationship IDs.
2. Sign in as the linked parent through R8.
3. Read refreshed student data and relationships.
4. Compare IDs, counts and balance with the snapshot.

**Expected Result:**
> Sign-in reuses the existing student, wallet and links. No duplicate account or relationship is created and balance stays SGD 100.00.

---

#### `TC-R1-061`: School transfer or withdrawal leaves the account unchanged

- **Scenario ID**: `TS-R1-06`
- **Test Suite**: Cross-function seams
- **Page / Target**: `Parent / school / payment integration`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: R1 FS v1.2 F01-BR04 and F02-BR04; §2.1; CD-06.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: CR: school enrolment is independent of Education Account eligibility.

**Preconditions:**
```text
Service clock: 15 October 2026, 12:00 SGT; STU-R1-13 has an Active wallet, SGD 250.00 and a school record. An authorised school-admin path is available. Use only a test HTTP source and isolated database; synthetic NRIC acceptance by the mock contract is pending.
```

**Test Data:**
```text
STU-R1-13; school transfer in one clean run and withdrawal in another.
Base source records, overridden by the case variants above: STU-R1-13: NRIC="T9900013A"; FullName="R1 Mock Student 13"; DOB=2015-01-10; CitizenshipStatus=SingaporeCitizen; Gender=Female.
```

**Test Steps:**
1. Record account ID, status, balance and DOB.
2. Transfer the student through the school-admin path.
3. Compare account values.
4. Reset the fixture and repeat with withdrawal.

**Expected Result:**
> Account ID, Active status, balance and DOB remain unchanged in both runs. School enrolment changes do not create, close or replace the wallet.

---

#### `TC-R1-062`: A student without an account cannot pay from its balance

- **Scenario ID**: `TS-R1-06`
- **Test Suite**: Cross-function seams
- **Page / Target**: `Parent / school / payment integration`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: R1 FS v1.2 F01-AC03; FS Function 9 no-EA payment rule; received performance X9.6, CS-9.7.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: CR: non-citizens have no Education Account. R9 contract: online and education-balance payment options.
- **Note**: Pending-transaction handling is tested in TC-R1-074, not this case.

**Preconditions:**
```text
R9 and authorised-parent journeys are available. Both students have a valid SGD 10.00 charge. The account holder has sufficient balance. Use only a test HTTP source and isolated database; synthetic NRIC acceptance by the mock contract is pending.
```

**Test Data:**
```text
No-account student: STU-R1-10. Account holder: STU-R1-13 with SGD 250.00. Online provider is a controlled simulation.
Base source records, overridden by the case variants above: STU-R1-10: NRIC="T9900010A"; FullName="R1 Mock Student 10"; DOB=2015-08-10; CitizenshipStatus=ForeignStudent; Gender=Female | STU-R1-13: NRIC="T9900013A"; FullName="R1 Mock Student 13"; DOB=2015-01-10; CitizenshipStatus=SingaporeCitizen; Gender=Female. No-account DOB 2015-08-10, ForeignStudent; account-holder DOB 2015-01-10, SingaporeCitizen, Active wallet.
```

**Test Steps:**
1. Attempt an education-balance payment for STU-R1-10.
2. Pay that charge online through the simulation.
3. Use another valid charge to pay from STU-R1-13's balance.
4. Read payment results and wallet entries.

**Expected Result:**
> STU-R1-10 cannot pay from education balance but can complete the valid online payment. STU-R1-13's balance payment succeeds once and reduces balance by SGD 10.00.

---


### Test Suite: Performance, concurrency and volume

#### `TC-R1-070`: Overlapping sync runs do not create duplicate accounts

- **Scenario ID**: `TS-R1-08`
- **Test Suite**: Performance, concurrency and volume
- **Page / Target**: `Backend job / API`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: R1 FS v1.2 §1.1.7; received performance PR-1.5, X1.7, CS-1.3.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: CR: one account per citizen. WA: overlapping triggers and conflict handling.

**Preconditions:**
```text
The real scheduled and manual triggers are available. Use isolated SQL Server and a source barrier so two owned runs overlap before account creation.
```

**Test Data:**
```text
The same valid birthday citizen set returned to both runs; distinct run IDs; identical NRICs and source data.
```

**Test Steps:**
1. Start a scheduled run and hold it at the source barrier.
2. Start the manual run while the first is still active.
3. Release the barrier so both process the same records.
4. Read both run outcomes and persisted accounts.

**Expected Result:**
> The final account set equals one successful run, with one wallet per citizen and unchanged balances. Record any refused duplicate run or constraint conflict under the agreed error policy.

---

#### `TC-R1-074`: Check eligibility while a payment is in progress

- **Scenario ID**: `TS-R1-08`
- **Test Suite**: Performance, concurrency and volume
- **Page / Target**: `Backend job / API`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: R1 FS v1.2 §1.2.7; received performance X1.8, X1.9, PR-1.8, CS-1.5; client CD-02.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: OPEN: in-progress payment resolution. CR: client expects no pending transaction on completed closure. WA: Closure Deferred safety. WA: SGT birthday boundary.
- **Note**: Correctness/concurrency case, not a timing benchmark. Do not force Closed when the remaining balance should defer it.

**Preconditions:**
```text
Use an isolated payment dependency and SQL Server. Agree a pause point after the payment eligibility check but before wallet debit. Start just before the sixteenth birthday; payment-resolution policy remains open.
```

**Test Data:**
```text
SingaporeCitizen holder, DOB 2010-10-15; Active wallet with SGD 150.00; valid payable charge SGD 10.00; FundingReference R1-074-PAY. Start at 2026-10-14T15:59:59Z, advance to 2026-10-14T16:00:00Z. Parent ownership and all other request checks are valid.
```

**Test Steps:**
1. Set the service clock to 14 October 2026, 23:59:59 SGT.
2. Start the payment and hold it after its initial eligibility check but before wallet debit.
3. Advance to 15 October 2026, 00:00 SGT while the payment is held.
4. Access the account through the real eligibility path.
5. Record state, balance and closure/deferral evidence.
6. Release the payment and read its final result.
7. Check pending transactions and all committed ledger effects.

**Expected Result:**
> Record payment resolution and account state without presuming completed closure. Funds must not be lost or debited twice. If the account completes closure, check the client expectation of no pending transaction. Positive-balance Closure Deferred behaviour remains a WA.

---

#### `TC-R1-068`: Measure creation and access-triggered closure separately

- **Scenario ID**: `TS-R1-08`
- **Test Suite**: Performance, concurrency and volume
- **Page / Target**: `Backend job / API`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Performance`
- **Traceability**: Received performance CS-1.1, PR-1.1 to PR-1.4, PR-1.6, X1.1, X1.2, X1.6; R1 FS v1.2 §1.2.7.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: WA: N, M and time targets. The received 10-minute batch proposal has not been adopted for access-triggered closure.
- **Note**: Advancing time alone is not a closure load. Do not combine the two phase times into an unapproved batch target.

**Preconditions:**
```text
Record the build, environment, workload size N and worker count. Reset the database. Approve timing targets before judging performance.
```

**Test Data:**
```text
Creation workload: N valid synthetic citizen records with recorded eligibility mix. Separate closure workload: M due accounts with recorded zero/positive balances. The 25-row catalogue is not a capacity workload by itself.
```

**Test Steps:**
1. Run creation alone and record duration, errors, CPU and memory.
2. Compare created wallets with creation-eligible records.
3. Prepare the independent closure workload.
4. Access each due account through the real eligibility path and measure that phase separately.
5. Compare final states and balances with closure rules.

**Expected Result:**
> Creation and closure have separate measurements and counts. No eligible account is missing or duplicated. Under the proposed safety rule, positive balances remain in Closure Deferred. No transfer runs. Report against approved phase-specific targets only.

---

#### `TC-R1-069`: Parallel processing matches sequential processing

- **Scenario ID**: `TS-R1-08`
- **Test Suite**: Performance, concurrency and volume
- **Page / Target**: `Backend job / API`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Performance`
- **Traceability**: Received performance PR-1.7, X1.4, CS-1.2.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: Conditional: worker support. Derived performance correctness criterion; workload approval pending.
- **Note**: If worker configuration is unavailable, record the unsupported capability; do not manufacture a parallel run.

**Preconditions:**
```text
The real job supports configurable workers. Use identical empty databases and source snapshots for both runs; record worker counts. Prepare the expected eligible NRIC set independently from the implementation before either run.
```

**Test Data:**
```text
One approved synthetic workload of N records; identical DOB, citizenship, duplicate and invalid-record mix in both runs.
```

**Test Steps:**
1. Run with one worker and record account IDs by NRIC, counts and balances.
2. Reset to the identical starting state.
3. Run with the agreed multi-worker count.
4. Compare account existence, eligibility outcomes and balances by NRIC.

**Expected Result:**
> Each run separately matches the independently prepared expected eligible NRIC set and balances, with no missing or duplicate accounts. The runs also match each other. Generated IDs may differ; compare business identity, not random IDs.

---

#### `TC-R1-071`: Account reads remain correct while sync runs

- **Scenario ID**: `TS-R1-08`
- **Test Suite**: Performance, concurrency and volume
- **Page / Target**: `Backend job / API`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Performance`
- **Traceability**: Received performance X1.5, CS-1.4, CS-8.4, X8.1; local SYNC-07.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: WA: 20-parent load and thresholds. R8 data-access contract applies.

**Preconditions:**
```text
R8 reads are available. Agree the concurrency level and read thresholds; record the build and workload. Parents have authorised links to existing accounts.
```

**Test Data:**
```text
Proposed load: 20 parent journeys. Separate synthetic records are eligible for creation; parent-read accounts and expected values are recorded.
```

**Test Steps:**
1. Start the parent read workload.
2. Run creation sync while reads continue.
3. Record response time, errors and returned account values.
4. Compare created accounts and balances after the run.

**Expected Result:**
> Reads show complete authorised account data, not partially created records or another family's information. No account is missing or duplicated. Report timing against approved read thresholds only.

---

#### `TC-R1-072`: Measure sync under the agreed peak parent load

- **Scenario ID**: `TS-R1-08`
- **Test Suite**: Performance, concurrency and volume
- **Page / Target**: `Backend job / API`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Performance`
- **Traceability**: Received performance XS.3, CS-P.3; local PERF-07.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: WA: peak load, K and timing targets.

**Preconditions:**
```text
Agree base load, peak factor K, environment capacity and timing targets. Record all values before the run.
```

**Test Data:**
```text
Approved peak parent workload and N-record creation workload; no CPF transfer or scheduled closure batch.
```

**Test Steps:**
1. Apply the agreed peak parent workload.
2. Run the real creation job.
3. Measure job duration, parent response times and errors.
4. Compare account counts and balances with the source.

**Expected Result:**
> No eligible account is missing or duplicated and balances remain correct. Compare timing with approved targets. If the environment cannot sustain the agreed load, report the achieved level without claiming larger-scale capacity.

---


### Test Suite: Security and privacy

#### `TC-R1-063`: Unauthorised identities cannot start or configure the job

- **Scenario ID**: `TS-R1-07`
- **Test Suite**: Security and privacy
- **Page / Target**: `Backend job / API`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Security`
- **Traceability**: Received security SR-1.1, SE1.1; local SEC-01.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: Derived security criterion; permitted-role and logging rules require approval.
- **Note**: If no configuration interface is exposed, record that subcheck as not applicable rather than an authorisation pass.

**Preconditions:**
```text
The deployed trigger/configuration interfaces and permitted roles are agreed. Use an isolated deployment and valid request bodies.
```

**Test Data:**
```text
One permitted operator, one authenticated but forbidden user, one uncredentialed process; unique request markers.
```

**Test Steps:**
1. Confirm the permitted operator can use the agreed interface.
2. Try to start the job as each forbidden identity.
3. Try to change job configuration as each forbidden identity.
4. Read refusals, audit evidence and job-run counts.

**Expected Result:**
> No forbidden request starts a run or changes configuration. Refusals are attributable to authorisation, not missing routes or invalid bodies. Record audit evidence under the agreed logging policy.

---

#### `TC-R1-064`: Out-of-source changes do not drive account decisions

- **Scenario ID**: `TS-R1-07`
- **Test Suite**: Security and privacy
- **Page / Target**: `Backend job / API`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Security`
- **Traceability**: Received security SR-1.2, SE1.2; R1 FS v1.2 §1.1.4 and §1.2.3.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: Derived security criterion; authoritative-source and tampering response need approval.
- **Note**: Creation sync alone cannot prove closure behaviour. Do not alter any shared or production database.

**Preconditions:**
```text
An isolated database and government mock are available. Agree the authoritative-source policy; use a supported test-only mutation method. Use only a test HTTP source and isolated database; synthetic NRIC acceptance by the mock contract is pending.
```

**Test Data:**
```text
Run A: STU-R1-13 has an Active wallet with SGD 0.00. Change only local DOB to 2010-10-15; source DOB stays 2015-01-10 and source citizenship stays SingaporeCitizen. Run B after reset: a local-only citizen has DOB 2019-10-15, no account, and is absent from the source.
Base source records, overridden by the case variants above: STU-R1-13: NRIC="T9900013A"; FullName="R1 Mock Student 13"; DOB=2015-01-10; CitizenshipStatus=SingaporeCitizen; Gender=Female.
```

**Test Steps:**
1. Keep the source unchanged and apply the local-only DOB change.
2. Access the existing account through the real eligibility path.
3. Reset and add the local-only creation candidate.
4. Run the real sync.
5. Compare accounts and captured source requests.

**Expected Result:**
> Under the proposed authoritative-source rule, Run A stays Active with SGD 0.00, without age-based closure or deferral, after checking the unchanged upstream DOB. Run B creates no account for the local-only record. Discrepancies are reported without raw identifiers.

---

#### `TC-R1-065`: Record creation and access-triggered closure for audit

- **Scenario ID**: `TS-R1-07`
- **Test Suite**: Security and privacy
- **Page / Target**: `Backend job / API`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Security`
- **Traceability**: R1 FS v1.2 §2.2 and §2.4; received security SR-1.3, SR-1.8, SE1.3, SE1.8.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: TD: processing audit. WA: actual closure timestamp. Derived security audit/tamper criteria require approval.
- **Note**: Do not make existing audit storage a prerequisite that hides a missing required audit record.

**Preconditions:**
```text
Service clock: 15 October 2026, 12:00 SGT; creation and account-access paths are available. Prepare one new citizen and one Active zero-balance holder at 16. Use only a test HTTP source and isolated database; synthetic NRIC acceptance by the mock contract is pending.
```

**Test Data:**
```text
Create STU-R1-02; close STU-R1-22 on access. Use a user that lacks audit-edit permission for the tampering check.
Base source records, overridden by the case variants above: STU-R1-02: NRIC="T9900002A"; FullName="R1 Mock Student 02"; DOB=2019-10-15; CitizenshipStatus=SingaporeCitizen; Gender=Female | STU-R1-22: NRIC="T9900022A"; FullName="R1 Mock Student 22"; DOB=2010-10-15; CitizenshipStatus=SingaporeCitizen; Gender=Female.
```

**Test Steps:**
1. Run the creation flow and collect its audit evidence.
2. Access STU-R1-22 and collect closure evidence.
3. Check action, account reference, timestamp and outcome.
4. Attempt an unauthorised alteration of one audit record.

**Expected Result:**
> Each action has attributable audit evidence under the agreed audit contract. Unauthorised modification is refused. CPF-transfer audit is deferred until a transfer path exists.

---

#### `TC-R1-066`: Keep sensitive data out of logs, errors and descriptions

- **Scenario ID**: `TS-R1-07`
- **Test Suite**: Security and privacy
- **Page / Target**: `Backend job / API`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Security`
- **Traceability**: Received security draft 0.3 SR-1.5, SE1.5; local security draft 0.4 SEC-05, SYNC-01; implementation audit F3.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: WA/derived security rules; approved logging and audit-field permissions are pending.
- **Note**: Use full-output scans, not only sampled known messages. Include Information, Warning, Error and exception text.

**Preconditions:**
```text
Capture all log levels and error responses in an isolated run. Use only synthetic identifiers and known sensitive marker values.
```

**Test Data:**
```text
Success, duplicate, non-citizen, validation-failure, exception, invalid-NRIC, missing-profile and deactivation fixtures. Exact markers are recorded before the run.
```

**Test Steps:**
1. Run creation, duplicate and failure paths through the real job and handlers.
2. Exercise invalid-NRIC, missing-profile and ineligible account requests.
3. Close a zero-balance account through lifecycle access.
4. Capture complete output for success, duplicate, non-citizen, validation, exception, missing-profile and deactivation paths, including all log levels.
5. Scan the complete log and error output for raw marker values.
6. Read opening transaction descriptions and scan them too.
7. Confirm required protected identity fields are evaluated under their separate storage contract.

**Expected Result:**
> Under the draft privacy rules, general logs, errors and free-text descriptions contain no unapproved raw NRIC, DOB, citizenship or financial values. All test inputs are synthetic; necessary protected identity storage is not mistaken for a log leak.

---

#### `TC-R1-067`: Future CPF transfer cannot be started or altered without authority

- **Scenario ID**: `TS-R1-07`
- **Test Suite**: Security and privacy
- **Page / Target**: `Backend job / API`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Security`
- **Traceability**: Received security SR-1.7, SE1.7, SE1.8; R1 FS v1.2 §1.2.7.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: Deferred under B4; no current MVP transfer path.
- **Note**: Keep Not Run. This is future coverage, not a passed security control.

**Preconditions:**
```text
Deferred in v1.2. Run only after a transfer path, permitted trigger and reversal/reconciliation rules are agreed.
```

**Test Data:**
```text
Future fixture: Closed account, known balance-at-closure and unauthorised caller; amount changes and repeated requests.
```

**Test Steps:**
1. Attempt to start a transfer outside the permitted path.
2. Attempt to change its amount or repeat it.
3. Read transfer and account records.

**Expected Result:**
> Future acceptance: unauthorised requests produce no transfer or altered amount; repeated processing does not transfer funds twice. No result is judged before the transfer contract exists.

---


### Test Suite: Wallet precision and financial safety

#### `TC-R1-077`: Concurrent duplicate debit and reversal have one financial effect

- **Scenario ID**: `TS-R1-05`
- **Test Suite**: Wallet precision and financial safety
- **Page / Target**: `Wallet API / ledger`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: FS Function 9 dated 2026-10-14 §2.1, EA ledger contract; R1 FS v1.2 §2.3.
- **Environment**: Planned DEV/SIT; build TBD.
- **Assumption Reference**: R9 contract: atomic and idempotent debit/reversal by FundingReference. OPEN: response policy and API mapping.

**Preconditions:**
```text
Use isolated SQL Server and the real wallet APIs. One SingaporeCitizen holder, DOB 2015-01-10, has an Active wallet with SGD 100.00. Authorisation, charge and reference-field mapping are valid. Release pairs of requests together; record their overlap.
```

**Test Data:**
```text
Two identical SGD 40.00 debit requests with FundingReference R1-077-DEBIT. Then two identical reversals of that original debit using the same agreed reversal reference R1-077-REV. Service clock: 15 October 2026, 12:00 SGT.
```

**Test Steps:**
1. Dispatch both debit requests concurrently and wait for both outcomes.
2. Read persisted balance, effective debit count and original transaction ID.
3. Dispatch both reversal requests concurrently for that original debit and wait for both outcomes.
4. Read persisted balance and effective reversal count; record any duplicate/conflict responses.

**Expected Result:**
> The duplicate debits have one effective SGD 40.00 debit, leaving SGD 60.00. Duplicate reversals have one effective SGD 40.00 credit, restoring SGD 100.00. Balance and ledger effects agree; no funds are lost or applied twice. Response handling is judged against the agreed API contract.

---
