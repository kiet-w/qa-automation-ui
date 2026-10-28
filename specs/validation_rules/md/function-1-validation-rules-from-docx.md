# function-1-validation-rules


Function 1. Education Account Lifecycle Validation Rules

# 1. Document control


| Field | Value |
| :--- | :--- |
| Project | EAFAMS (MOE education account and financial assistance platform) |
| Theme | Function 1. Education account lifecycle: creation, closure and balance handling |
| Deliverable | Validation rules, EN edition |
| Version and date | Draft 0.1, 26/10/2026 |
| Author | QA (generated locally from captured sources) |
| Main sources | R1 specification v1.2, captured 14 October 2026 (Team sources/fs/agile-fs-r1-2026-10-14.txt, second revision in that export); Function 1 test plan v1.2, 15 October 2026, for the decision register and the data contract checks; Function 1 implementation audit, 15 October 2026, for observed deviations only. |
| Source standing | R1 v1.2 is a proposed implementation, not an approved specification. Only items marked CR trace to the tender or a dated client statement. This document grants no approval. |
| Revision caution | The same export contains v1.0 and v1.2, and both reuse the F01-BR and F02-BR identifiers with different meanings. v1.2 controls. v1.0 is cited only in sections 5.5 and 6.6 as history. |
| Companion documents | Function 1 test plan and case register. This document explains the rules; it does not replace the cases, results or defect register. |


F1 has no screens of its own. Parent and HQ presentation belongs to F08, so this document stops at the backend checks and the data they return.

# 2. Scope


In scope: citizen data extraction and required-field validation, initial and daily synchronization, age eligibility at 7 and 16 including the 29 February rule, duplicate prevention, account creation values, the backend-triggered closure check, the closure-deferred safety rule, citizenship changes, synchronization logging and recovery, and the transaction and ledger rules that F1 owns.

Out of scope: F08 screens, authentication and relationship display; top-up campaigns and batch credits (R2); fee configuration (R3); invoices, payment processing and split payment (R9); FAS and chatbot functions. CPF transfer is deferred by v1.2 and appears only as a deferred rule.

This edition states 14 business rules, 8 exception flows, 8 alternative flows and 24 acceptance criteria.

# 3. Conventions


| Marker | Meaning | How it is treated |
| :--- | :--- | :--- |
| CR | Client-confirmed through the tender or a dated client statement. | A mismatch is a build failure. |
| TD | Team decision recorded in v1.2. | A mismatch is a build failure, but the rule is not client-approved. |
| WA | Working assumption. | Record the observed result. Acceptance waits for approval. |
| - | No marker in the source. | Treat as a proposal from the v1.2 draft. |
| Open | No agreed answer exists. | Record behaviour only; never mark the check passed. |

- Rule text is an English paraphrase of the captured Vietnamese source. Source identifiers and section numbers are preserved.
- Where a rule carries two markers, the note separates the confirmed part from the assumption. F01-BR02 is the only one here.
- Money is SGD with exactly two decimals. Dates in examples use DD/MM/YYYY and Singapore time (UTC+8).
- F1 has no user-facing message catalogue in the capture. Section 9 lists the outcome vocabulary QA uses in evidence, not product copy.
- Rules the test plan left conditional stay conditional here. Nothing is tightened or relaxed silently.

# 4. Entry points and validation order


The order matters. A record is checked for required data before citizenship, before age and before the duplicate check, and every backend read runs the closure check before returning data.

| Entry point | Trigger | Validation order | Result |
| :--- | :--- | :--- | :--- |
| Initial synchronization | First run against the mock citizen API | Authenticate, validate required fields, check citizenship, check age 7 to under 16, check for an existing account, create. | An invalid record is skipped with a reason and the job result is logged. |
| Daily incremental synchronization | Daily job, 00:00 SGT (WA) | Same order for citizens turning 7. A missed date joins the next run (WA). | Same as initial sync. |
| Account read for Parent or HQ | Any backend read, including F08 and HQ lookup | If Closed, skip closure. Otherwise fetch current citizen data, check age 16, run closure, then return the current status. | The caller sees the status after the check. An API failure does not change the status (WA). |
| Top-up or payment request | Financial request from the owning function | Run the closure check before any money moves. Refuse when the holder is 16 or over, or the account is Closed. | No money moves. The refusal belongs to the closure check, not to the payment rule. |
| Retry or re-run | Manual or scheduled retry | Use the same dataset, check for existing accounts and recover missed dates. | No duplicate account, closure or transfer. |


The closure check is shared. F08, top-up and payment must call the same backend rule rather than reimplement it, or the status they show and the status they enforce will drift.

# 5. Field rules


## 5.1 Student information


Source: v1.2 sections 1.1.3 and 2.1. The Student Profile can exist without an Education Account, for example for a permanent resident or a foreign student.

| Field | Required | Validation rule | On failure | Source |
| :--- | :--- | :--- | :--- | :--- |
| NRIC | Yes | Not empty and in the supported identifier format | No account; exception recorded | 1.1.3, 2.1 |
| Full Name | Yes | Not empty | No account; exception recorded | 1.1.3, 2.1 |
| Date of Birth | Yes | A valid date and not in the future | No account; exception recorded | 1.1.3, 2.1 |
| Citizenship | Yes | One of the recognised values | No account; exception recorded | 1.1.3, 2.1 |
| Gender | Yes (TD) | One of the valid values while the field stays required (WA) | No account; exception recorded | 1.1.3, 2.1 |
| Student Profile Status | System-managed | Not an eligibility condition and not an account status | Not applicable | 2.1 |
| Race | No | Stored if the source supplies it | Creation is not blocked | 2.1 |
| Block, Street, Unit, Postal Code, Country | No | Stored if the source supplies them | Creation is not blocked | 2.1 |
| Father NRIC, Mother NRIC | No | A link is created only when the relationship data is valid | Creation is not blocked; linking is skipped | 2.1, 1.1.10 |


Missing required data fails only that record. The run continues, and the reason is written to the processing result.

## 5.2 Education account


Source: v1.2 section 2.2. One citizen holds at most one account, and the account links to exactly one Student Profile.

| Field | Required | Validation rule | On failure | Source |
| :--- | :--- | :--- | :--- | :--- |
| Education Account Number | Yes | Unique and generated by the system | Creation fails; no partial account | 2.2 |
| Account Holder Reference | Yes | Exactly one Student Profile | Creation fails | 2.2 |
| Account Balance | Yes | SGD 0.00 at creation, two decimals, never negative (WA) | Creation or transaction is rejected | 2.2, 2.3 |
| Account Status | Yes | Active at creation; Closed after closure; no delete (WA) | Inconsistent state; defect | 2.2, 1.1.7 |
| Currency | Yes | SGD | Creation fails | 2.2 |
| Account Creation Date | Yes | The actual creation timestamp | Audit record incomplete | 2.2 |
| Account Last Updated Date | System-managed | Set when the account changes, if the system records it | Not applicable | 2.2 |
| Actual Account Closure Date | Required when Closed (WA) | Set when closure completes | Closure result cannot be asserted or ordered | 2.2 |


v1.2 removes the scheduled closure date. Do not validate against a stored due date; the backend decides from the current citizen record when the account is accessed.

## 5.3 Transaction and ledger


Source: v1.2 section 2.3. F1 records the account-side contract. R2 and R9 own the business transaction rules, and the shared ledger contract must match.

| Field | Required | Validation rule | On failure | Source |
| :--- | :--- | :--- | :--- | :--- |
| Transaction Reference Number | Yes | Unique for the transaction | Reject; duplicate risk recorded | 2.3 |
| Related Education Account | Yes | The account exists | Reject | 2.3 |
| Transaction Direction | Yes | Incoming or outgoing | Reject | 2.3 |
| Transaction Amount | Yes | SGD with two decimals | Reject | 2.3 |
| Transaction Status | Yes | Success or Failed | Reject | 2.3 |
| Transaction Description | No | Stored if supplied; must not carry a national identifier | Record; privacy review | 2.3, audit F3 and F9 |
| Transaction Date | Yes | The recorded timestamp | Reject | 2.3 |
| Transaction Type | Proposed | Top-up, payment or CPF transfer once those functions exist | Needs agreement | 2.3 |

- A successful incoming transaction increases the balance. A successful outgoing transaction decreases it.
- A failed transaction does not change the balance (WA).
- Transaction history is retained after closure (TD).
- Money is exact to two decimals. A negative balance is not supported (WA).
- F01 does not create an opening transaction unless the team decides to (WA).

## 5.4 Synchronization and audit


Source: v1.2 section 2.4. Every run records a result, and a partial run must not lose the records it did not process.

| Field | Required | Validation rule | On failure | Source |
| :--- | :--- | :--- | :--- | :--- |
| Processing Reference | Yes | One reference per synchronization | Run cannot be traced | 2.4 |
| Job Name | Yes | Initial Synchronization or Daily Synchronization | Run cannot be classified | 2.4 |
| Trigger Type | Yes | Scheduled or Manual, where manual is supported | Run cannot be classified | 2.4 |
| Processing Status | Yes | Success or Failed | Run result is unknown | 2.4 |
| Processing Start Time | Yes | Recorded at start | Timing cannot be checked | 2.4 |
| Processing Completion Time | When completed | Recorded at the end | Partial run looks complete | 2.4 |
| Total Records | Yes | Count of citizen records processed | Reconciliation fails | 2.4 |
| Successful, Failed, Skipped Records | Proposed | Counts that add up to the total | Reconciliation fails | 2.4 |
| Failure Reason | When applicable | Names the job or record failure | Failure cannot be triaged | 2.4 |
| Last Successful Processing Coverage | Proposed (WA) | The date range already processed | Recovery cannot pick a start date | 2.4 |


## 5.5 CPF transfer record (deferred)


v1.0 defined a CPF Transfer Record with a transfer ID, account ID, amount, status and date. v1.2 removes that section and defers the transfer, so none of those fields is a current validation rule. Keep the record design available for B4, and apply the closure-deferred rule until a transfer path exists.

# 6. Business rules


## 6.1 Creation


| Rule | Rule (EN paraphrase) | Marker | What the validation does |
| :--- | :--- | :--- | :--- |
| F01-BR01 | Only Singapore Citizens are given an Education Account. | CR | A non-citizen record creates no account and is recorded as skipped. |
| F01-BR02 | Eligible age runs from the 7th birthday to before the 16th birthday. | CR / WA | The age range is client-confirmed. How initial sync treats citizens already past 7 is a working assumption. |
| F01-BR03 | Age is determined from the citizen's DOB, not from school level or schooling status. | - | School, level, cohort and class are not required to create an account. |
| F01-BR04 | Account creation does not depend on school enrolment. | - | A citizen with no enrolment record still gets an account. |
| F01-BR05 | A citizen aged 16 or over without an account is not given a new one. | - | An overdue record is skipped, not backfilled. |


The age examples make the boundary testable. A citizen born 15/06/2019 is under 7 on 14/06/2026, eligible on 15/06/2026, and 16 on 15/06/2035. The leap-year rule evaluates a 29 February birth on 28 February in a non-leap year, and F01 and F02 use the same rule (WA).

The 7 to under-16 range is client-confirmed. The WA on F01-BR02 covers initial-sync handling for citizens already past 7, not the range itself.

## 6.2 Duplicate prevention


| Situation | Expected behaviour | Source |
| :--- | :--- | :--- |
| No account exists | Create an account if the citizen is eligible. | 1.1.7 |
| Account is Active | Do not create a new account. | 1.1.7 |
| Account is Closed | Do not create a new account. | 1.1.7 |
| Closed account is hidden from a screen | Do not create a new account. Hidden does not mean deleted. | 1.1.7 |
| Daily sync processes the same citizen again | Do not create a duplicate. | 1.1.7 |
| Any account | No hard delete or soft delete in Sprint 1. | 1.1.7 (WA) |


Hiding an account from a screen does not remove it. The duplicate check looks at the stored account, not at what the current screen shows.

## 6.3 Closure


| Rule | Rule (EN paraphrase) | Marker | What the validation does |
| :--- | :--- | :--- | :--- |
| F02-BR01 | The account must close when the holder turns 16. | CR | A due account is closed on the next backend access, not on a timer. |
| F02-BR02 | Every backend action that reads or processes the account triggers the closure check first. | TD | A read or financial request returns the status after the check. |
| F02-BR03 | Closure age is determined from the holder's current DOB. | TD | A stale copy of the DOB cannot decide closure. |
| F02-BR04 | Creation date or school level does not affect the closure age. | CR | A late-created or retained account still closes at 16. |
| F02-BR05 | No scheduled closure date is stored in the MVP. | TD | No row exists to select accounts by date. |
| F02-BR06 | No pending transactions exist at closure. | TD | A pending transaction is an exception, not an expected state. |
| F02-BR07 | A closed account cannot receive new financial transactions. | WA | A top-up or payment is refused before money moves. |
| F02-BR08 | Closed accounts and their transaction history are retained for lookup and audit. | TD | History stays readable after closure. |
| F02-BR09 | Repeated backend access must not close the account twice. | WA | The closure date and balance do not change on a repeat. |


Closure is checked when the account is accessed, not by a nightly batch. If nobody touches the account, it can stay Active past the 16th birthday; the first backend access then closes it before returning data. That delay is a known MVP limitation, not a validation failure.

A citizenship change before 16 does not trigger age-based closure. The account is flagged Eligibility Review Required, new financial operations are blocked, and no second account is created (WA).

## 6.4 Balance handling at closure


| Condition | Expected behaviour | Source |
| :--- | :--- | :--- |
| Due to close, balance SGD 0.00 | Complete the closure. | 1.2.7 |
| Due to close, balance above SGD 0.00, CPF transfer not available | Do not record a successful transfer. Mark Closure Deferred, keep the balance and block new financial operations. | 1.2.7 (WA) |
| CPF transfer implemented and successful | Complete the closure under the confirmed financial rule. | 1.2.7 |


The rule exists to stop an account closing with money that has nowhere to go. A zero balance closes normally. A positive balance without a transfer path stays deferred and blocked.

## 6.5 Transaction, sync and audit rules

- A successful debit or credit changes the balance by exactly its amount. A failed transaction changes nothing (2.3).
- The balance never goes below zero in the MVP (2.3, WA).
- Every synchronization records its result for audit (2.4, TD).
- A government API failure is recorded, and a retry or re-run must not create a duplicate account (2.4).
- One invalid record does not stop the run; the reason is recorded and the next record is processed (2.4, WA).
- A missed daily run must be detectable so the next run can recover the unprocessed dates (2.4, WA).

## 6.6 v1.0 rules and their status


These rules come from the first revision in the same export. Some survived in v1.2, some were retired or deferred. None should be validated from the v1.0 wording, because the identifiers were reused with different meanings.

| v1.0 rule | What it said | Status now |
| :--- | :--- | :--- |
| F01-BR06 | Scheduled Closure Date = DOB + 16 years. | Retired by v1.2 F02-BR05. |
| F01-BR07 | Creation is independent of school, class or schooling status. | Kept, restated as v1.2 F01-BR03 and F01-BR04. |
| F01-BR08 | A rerun must not duplicate or reset financial data. | Kept in the duplicate table and the job-rerun row. |
| F01-BR09 | A late-added eligible student still gets an account. | Kept as a working assumption, limited by v1.2 section 4. |
| F01-BR10 | A missing parent relationship does not block creation. | Kept as F01 AF04. |
| F03-BR01 to F03-BR07 | Simulated CPF transfer amount, success, retry and zero-balance rules. | Deferred. v1.2 has no F03 section. |


# 7. Exception and alternative flows


Each function numbers its flows from 01, so the function prefix is part of the reference here. F01 EF01 and F02 EF01 are different rules.

## 7.1 Creation


| Flow | Scenario | Expected behaviour | Source |
| :--- | :--- | :--- | :--- |
| F01 AF01 | The citizen is not a Singapore Citizen. | No account is created. | 1.1.10 |
| F01 AF02 | The citizen is under 7 or has turned 16. | No account is created. | 1.1.10 |
| F01 AF03 | The citizen already has an account, including a closed one. | Creation is skipped. | 1.1.10 |
| F01 AF04 | The citizen has no father or mother NRIC. | An account is created if the other conditions hold. | 1.1.10 |
| F01 EF01 | The government API rejects the credentials. | Record a job failure and apply failure handling. | 1.1.10 |
| F01 EF02 | Required data is missing or invalid. | No account for that record; record the exception. | 1.1.3, 1.1.10 |
| F01 EF03 | Duplicate citizen records hold conflicting data. | No duplicate account; record a data conflict. | 1.1.10 |
| F01 EF04 | The daily job fails or misses a processing day. | Run recovery for the unprocessed dates. | 1.1.10 |


## 7.2 Closure


| Flow | Scenario | Expected behaviour | Source |
| :--- | :--- | :--- | :--- |
| F02 AF01 | The holder is under 16. | The account stays Active. | 1.2.8 |
| F02 AF02 | The account is already Closed. | Closure is not processed again. | 1.2.8 |
| F02 AF03 | The holder has turned 16 when a parent opens the account. | Closure runs before account information is returned. | 1.2.8 |
| F02 AF04 | The holder has turned 16 when a top-up or payment is requested. | Closure is checked and the financial transaction does not continue. | 1.2.8 |
| F02 EF01 | The government API does not respond. | Do not change the status automatically; record the error and block financial actions that need eligibility verification. | 1.2.8 |
| F02 EF02 | Citizenship changes before age 16. | Record Eligibility Review Required; do not run age-based closure. | 1.2.8 |
| F02 EF03 | Closure processing fails. | Record the failure; never leave the account in an inconsistent state. | 1.2.8 |
| F02 EF04 | Balance is above zero while the CPF transfer is not implemented. | Record Closure Deferred; do not record a successful simulated transfer. | 1.2.7, 1.2.8 |


# 8. State transitions


| Object | From | To | Condition | Source |
| :--- | :--- | :--- | :--- | :--- |
| Education Account | None | Active | Citizen is eligible, required data is valid and no account exists | 1.1.4 |
| Education Account | Active | Active | Holder is under 16 at access | 1.2.3 |
| Education Account | Active | Closed | Holder is 16 or over and the balance is handled successfully | 1.2.3, 1.2.7 |
| Education Account | Active | Closure Deferred | Holder is 16 or over, balance is above zero and no transfer path exists | 1.2.7 (WA) |
| Education Account | Closed | Closed | Any later access; no second closure | 1.2.4 |
| Education Account | Any | Deleted | Not supported in Sprint 1 | 1.1.7 (WA) |
| Student Profile | Exists | No account | Permanent resident or foreign student | 2.1 |
| Synchronization | Running | Success or Failed | Job completes or fails; partial results are recorded | 2.4 |
| Transaction | Recorded | Success or Failed | Processing outcome | 2.3 |


Closure Deferred appears in the specification as behaviour. Whether it is a stored status value is open point V7; do not assert an enum value until Dev confirms it.

# 9. Recorded outcomes


No user-facing message catalogue was captured for F1. This table fixes the vocabulary QA will use in evidence so two testers record the same result the same way. It is not product copy.

| Outcome | What it means | Rule behind it |
| :--- | :--- | :--- |
| Created | Account created with Active status and SGD 0.00. | F01-BR01 to F01-BR05 |
| Skipped: not a citizen | Record left without an account. | F01 AF01 |
| Skipped: outside age range | Record left without an account. | F01 AF02 |
| Skipped: account exists | No second account. | F01 AF03 |
| Failed: required data | No account for that record; reason recorded. | F01 EF02 |
| Failed: data conflict | No account for that record; conflict recorded. | F01 EF03 |
| Job failed: source authentication | Processing stops; job failure recorded. | F01 EF01 |
| Job failed: source timeout | Error recorded; retry applies. | 1.1.9 |
| Closure completed | Status Closed; actual closure date recorded; balance handled. | F02-BR01, F02-BR08 |
| Closure Deferred | Balance kept; new financial operations blocked; no transfer success claimed. | F02 EF04 |
| Eligibility Review Required | No automatic closure; financial operations blocked until review. | F02 EF02 |


# 10. Open questions


B1 to B10 are the decisions the Function 1 test plan already tracks. V1 to V10 are validation gaps found while writing this document. A V reference is a QA reference, not a project identifier.

| Ref | Question | Status | Position | Affects |
| :--- | :--- | :--- | :--- | :--- |
| B1 | Closure mechanism | Baseline | The backend-triggered check controls. The v1.0 batch design is retired. | Every closure case |
| B2 | Closure age rule and exceptions | Open | Tender says the 16th birthday. Earlier local material says the day before, with exceptions after 16. | F01-BR02, F02-BR01, boundary cases |
| B3 | Pending transaction at closure | Open | The client expects none. Handling is undefined. | F02-BR06, F02 EF01 |
| B4 | CPF transfer interface and whether it is simulated | Open | v1.2 removes F03 and defers the transfer. The closure-deferred rule stands in its place. | F02 EF04, balance handling |
| B5 | Nightly scan or sign-in fetch | Open | The R1 specification and the parent portal specification disagree. | F01 entry points |
| B6 | Job schedule and retry policy | Open | The 00:00 SGT start and the 15-minute retry are working assumptions. | Job failure table |
| B7 | Money precision and closure-date column | Open | The data design and the specification disagree. | Contract checks 1 and 2 |
| B8 | Performance thresholds, N and T | Open | Proposals pending approval. No validation rule depends on them. | Performance cases only |
| B9 | Post-16 exceptions | Open | No criteria, approver or duration is recorded. | F02-BR01 |
| B10 | Whether a closure date is stored | Baseline | No scheduled date is stored. The current citizen record decides on access. Storing the actual closure date remains B7. | F01-BR02, F02-BR05 |


| Ref | Question | Status | Position | Affects |
| :--- | :--- | :--- | :--- | :--- |
| V1 | Identifier model | Open | The requirements analysis proposes Person ID. v1.2 makes NRIC the business identifier. Confirm which key Dev persists and validates. | F01-BR01, F01-BR05 |
| V2 | NRIC format | Open | The rule says non-empty and in a supported format. No pattern or checksum is captured. | Student NRIC |
| V3 | Citizenship values | Open | The recognised list is not enumerated. Permanent resident and foreign student appear only as data examples. | Student Citizenship |
| V4 | Gender values and required status | Open | v1.2 keeps Gender required under the Dev contract. The first draft marks it WA. The 15 October build coerces values instead of rejecting them. | Student Gender |
| V5 | DOB input format | Open | The rule says a valid date that is not in the future. The accepted format and parser behaviour are not captured. | Student DOB |
| V6 | Account number format | Open | The number must be unique. No pattern, prefix or length is recorded. | Account Number |
| V7 | Account status values | Open | The MVP uses Active and Closed. Closure Deferred is described as behaviour, not as an enumerated value. | Account Status |
| V8 | Which fields make a duplicate conflict | Open | v1.0 names DOB and citizenship. v1.2 says conflicting data without listing the fields. | F01 EF03 |
| V9 | Zero-amount opening transaction | Open | R1 v1.2 makes an opening transaction conditional on a team decision. | Transaction rules |
| V10 | Sync log fields | Open | The 14 October data design lacks successful, failed and skipped counts, the failure reason and the last successful coverage. | Sync audit rules |


Answer B2 and V4 first. B2 fixes the closure boundary for every closure case, and V4 decides whether a missing gender blocks creation on the current contract.

# 11. Acceptance criteria map


| Criterion | Scenario | Expected result | Rules exercised |
| :--- | :--- | :--- | :--- |
| F01-AC01 | Initial sync, citizen aged 10, no account | One Active account with SGD 0.00 | F01-BR01, F01-BR02 |
| F01-AC02 | Daily sync, citizen turns 7 | Account created if none exists | F01-BR02 |
| F01-AC03 | Non-citizen or permanent resident | No account | F01-BR01 |
| F01-AC04 | Citizen under 7 | No account | F01-BR02 |
| F01-AC05 | Citizen aged 16 or over | No new account | F01-BR05 |
| F01-AC06 | Citizen already has an Active account | No duplicate | Duplicate table |
| F01-AC07 | Citizen already has a Closed account | No new account | Duplicate table |
| F01-AC08 | Required information is missing | No account; error recorded | 1.1.3 validation list |
| F01-AC09 | Father and mother NRIC are missing | Account created if other conditions hold | F01 AF04 |
| F01-AC10 | Student repeated a year or started school late | Eligibility still follows DOB | F01-BR03, F01-BR04 |
| F01-AC11 | The job missed one day | Recovery processes the missed date | F01 EF04 |
| F01-AC12 | The job reruns over records already created | No extra account | Duplicate table |
| F01-AC13 | The job runs on a weekend or public holiday | The daily schedule still applies | 1.1.2 |
| F01-AC14 | Citizen born on 29 February | The leap-year rule decides eligibility | 1.1.6 |
| F02-AC01 | Parent views the account of a 15-year-old | Account stays Active | F02-BR01 |
| F02-AC02 | Parent views the account of a holder who just turned 16, balance 0 | Account becomes Closed | F02-BR01 |
| F02-AC03 | HQ reads an overdue account whose holder is over 16, balance 0 | Closure runs before data is returned | F02-BR02 |
| F02-AC04 | Top-up request on an account whose holder has turned 16 | Top-up does not run | F02-BR07, F02 AF04 |
| F02-AC05 | Payment request on an account whose holder has turned 16 | Payment does not run | F02-BR07, F02 AF04 |
| F02-AC06 | A closed account is accessed again | No duplicate closure; closure date unchanged | F02-BR09 |
| F02-AC07 | Authorised parent views a closed account | History is readable; no new transaction | F02-BR08 |
| F02-AC08 | Student repeated a year or started school late | Closure still follows DOB | F02-BR04 |
| F02-AC09 | Government API fails during closure | No automatic closure; error recorded | F02 EF01 |
| F02-AC10 | Holder is 16 or over with balance above zero and no CPF transfer | No assumed transfer success; Closure Deferred | F02 EF04 |


# 12. Contract checks and known deviations


## 12.1 Data contract checks


These are checks against the Dev data design, not rules. They pass or fail before a functional case can be judged, and they are QA's reading of the 14 October design capture.

| # | Check | Data design says | Specification says | Effect on validation |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Money type | Wallets.Balance and Transactions.Amount are BIGINT | Decimal(18,2), SGD, two decimals | Cent-level and precision checks cannot pass on an integer column. |
| 2 | Closure date column | Wallets has CreatedAt and UpdatedAt as DATE; no closure date | Actual Closure Date is required when Closed | Closure results cannot be asserted or ordered. |
| 3 | Sync job log fields | total_records and status only | Total, successful, failed, skipped, start, completion, failure reason, last successful coverage | Recovery and audit cases cannot be checked. |
| 4 | Account status values | Enum, values not enumerated | Active and Closed, with Closure Deferred behaviour | Status assertions and display mapping depend on the answer. |
| 5 | Idempotency key | Not present in the capture | Idempotent debit and reversal keyed by a reference | Duplicate-money checks cannot pass without it. |
| 6 | Processing timezone | Not present in the capture | Singapore time, UTC+8 | Age boundary cases are not deterministic. |


## 12.2 Observed against the 15 October build


These observations come from the local implementation audit and the develop-Ver2 defect register. They describe one build, not the current one, and they do not change the rules above.

| Ref | Observation | Effect on validation |
| :--- | :--- | :--- |
| Audit F3 | National identifiers, dates of birth and citizenship appear in plain text. | Logs and responses cannot be treated as masked. |
| Audit F8 | The validator checks identifier, name and citizenship. A future DOB is not rejected, and gender is coerced to Male unless it matches Female. | DOB and gender cases cannot pass on that build. |
| Audit F5 | The sync log discards the record counts and the failure reason. | Sync audit rules cannot be verified from the log. |
| Audit F6 | No retry and no missed-day recovery was found. | F01 EF04 and F01-AC11 cannot pass. |
| Audit F7 | Closure never consults the government source. | F02-BR02 and F02-BR03 are not met. |
| Audit F9 | Creation writes a zero-amount transaction whose description contains the identifier. | The opening-row decision is still open; the privacy impact is separate. |
| R1-V2-DRAFT-01 | The default initial sync created a wallet for a six-year-old. | F01-BR02 fails on that build. |
| R1-DRAFT-01 | A due-age zero-balance account was stored as Inactive instead of Closed. | F02-BR01 and F02-AC02 fail on that build. |


Confirm the build under test before treating any of these as current. A rule that fails on this list is still a rule; the finding only explains why the last run failed.

# 13. Limits

- No product, build or environment test ran for this document. It reads captured sources only.
- R1 v1.2 is a proposed implementation. CR items trace to the tender or a client statement; TD and WA items do not.
- The text is an English paraphrase. The Vietnamese source controls if the two ever differ.
- No user-facing message catalogue exists in the capture. Section 9 is QA vocabulary.
- The v1.0 revision is retired. It is cited only as history, never as a current rule.
- Field formats for NRIC, DOB, citizenship, gender and account number are not captured. They stay open rather than guessed.
- The data contract checks describe the 14 October design capture and may be stale.
- This document grants no approval and does not replace the test plan, case register or defect register.

This edition uses the same table style and marker conventions as the Function 2 validation rules document. Function 1 has no screens, so it keeps its rule-first order. It adds no scenario and no result.