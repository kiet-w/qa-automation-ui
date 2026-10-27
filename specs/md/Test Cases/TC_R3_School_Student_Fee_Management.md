# R3: School, Student & Fee Master Data Management — Sprint 1 Test Cases

> **Module**: R3 - School, Student & Fee Master Data
> **Specification Reference**: [FS-03_School_Student_Fee_Management.md](file:////home/baudui/Projects/automation-ui/[agile] fs/md/FS document/FS-03_School_Student_Fee_Management.md)
> **Source Spreadsheet**: `Test Cases + Defect sprint 1.xlsx` (Sheet `R3 TC`)
> **Total Test Cases**: 105

## Executive Test Suite Summary

| Test Suite | Scenario Count | Test Cases | Priorities | Severities |
| :--- | :--- | :--- | :--- | :--- |
| School Management | 1 (TS-R3-F01) | 5 | High, Medium | S2, S3 |
| User Management & Security | 1 (TS-R3-F02) | 5 | Critical, High, Medium | S1, S2, S3 |
| Academic Structure | 1 (TS-R3-F03) | 4 | High, Medium | S2, S3 |
| Class Management | 1 (TS-R3-F04) | 6 | High, Medium | S2, S3 |
| Student Profile Management | 1 (TS-R3-F05) | 9 | High | S2 |
| Student Enrolment | 1 (TS-R3-F06) | 4 | High | S2 |
| Student Transfer | 1 (TS-R3-F07) | 4 | Critical, High, Medium | S1, S2, S3 |
| Education Account Linkage | 1 (TS-R3-F08) | 5 | High | S2 |
| Fee Type Catalog | 1 (TS-R3-F09) | 4 | Low, Medium | S3, S4 |
| Fee Component Catalog | 1 (TS-R3-F10) | 6 | Critical, High, Low, Medium | S1, S2, S3, S4 |
| Fee Pricing Engine | 1 (TS-R3-F11) | 8 | Critical, High | S1, S2 |
| Fee Publication Lifecycle | 1 (TS-R3-F12) | 9 | Critical, High, Medium | S1, S2, S3 |
| Publication Target Configuration | 1 (TS-R3-F13) | 7 | Critical, High, Medium | S1, S2, S3 |
| Recipient Resolution Engine | 1 (TS-R3-F14) | 4 | High | S2 |
| Student Charge Generation | 1 (TS-R3-F15) | 10 | Critical, High, Medium | S1, S2, S3 |
| Charge Adjustment & Audit | 1 (TS-R3-F16) | 9 | Critical, High, Medium | S1, S2, S3 |
| Edusave Payment & Reconciliation | 1 (TS-R3-PAY) | 5 | Critical | S1 |
| Tender E2E Integration | 1 (TS-R3-TENDER) | 1 | Critical | S1 |

---

## Quick Reference Index Table

| Test Case ID | Scenario ID | Title | Page / Area | Priority | Severity | Type | Defect ID | Traceability |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| [`TC-R3-F01-001`](#tc-r3-f01-001) | `TS-R3-F01` | Verify MOE HQ User successfully creates a new School with unique school_code | Admin Portal > School Setup | High | S2 | Functional |  | R3 FS v1.1 §3.1 F01-AC01; BR-R3-01; BR-R3-02; Tender R3 Item 3 |
| [`TC-R3-F01-002`](#tc-r3-f01-002) | `TS-R3-F01` | Verify system rejects School creation with duplicate school_code | Admin Portal > School Setup | High | S2 | Negative |  | R3 FS v1.1 §3.1 F01-AC02; BR-R3-01 |
| [`TC-R3-F01-003`](#tc-r3-f01-003) | `TS-R3-F01` | Verify deactivating a School preserves existing data but blocks new configurations/publications | Admin Portal > School Setup | High | S2 | StateTransition |  | R3 FS v1.1 §3.1 F01-AC03; BR-R3-03 |
| [`TC-R3-F01-004`](#tc-r3-f01-004) | `TS-R3-F01` | Verify School creation validates and stores Singapore school_type enum | Admin Portal > School Setup | Medium | S3 | Functional |  | R3 FS v1.1 §3.1 F01; WA-R3-10; Q18 |
| [`TC-R3-F01-005`](#tc-r3-f01-005) | `TS-R3-F01` | Verify boundary length validation on school_code and school_name fields | Admin Portal > School Setup | Medium | S3 | BVA |  | R3 FS v1.1 §3.1 F01; BVA boundary rules |
| [`TC-R3-F02-001`](#tc-r3-f02-001) | `TS-R3-F02` | Verify MOE HQ User assigns School User to at least one valid School | Admin Portal > User Management | High | S2 | Functional |  | R3 FS v1.1 §3.2 F02-AC04; BR-R3-04; Tender R3 Item 3 |
| [`TC-R3-F02-002`](#tc-r3-f02-002) | `TS-R3-F02` | Verify multi-tenant isolation: School User of School A cannot access School B data | Admin Portal > Academic Structure | Critical | S1 | Security |  | R3 FS v1.1 §3.2 F02-AC05; BR-R3-05; §5.2 Access Control |
| [`TC-R3-F02-003`](#tc-r3-f02-003) | `TS-R3-F02` | Verify School User first-time login mandates password change and 2FA setup per IM8 | Admin Portal > Authentication | High | S2 | Security |  | R3 FS v1.1 §3.2 F02; BR-R3-06; Q05 |
| [`TC-R3-F02-004`](#tc-r3-f02-004) | `TS-R3-F02` | Verify Segregation of Duties: School Admin, School Finance, and Teacher sub-roles | Admin Portal > RBAC | High | S2 | Security |  | R3 FS v1.1 §1.2 Actors; §3.2 F02; Q01 |
| [`TC-R3-F02-005`](#tc-r3-f02-005) | `TS-R3-F02` | Verify system rejects creating School User without associating to an active School | Admin Portal > User Management | Medium | S3 | Negative |  | R3 FS v1.1 §3.2 F02; BR-R3-04 |
| [`TC-R3-F03-001`](#tc-r3-f03-001) | `TS-R3-F03` | Verify configuration of Academic Level with unique code within School | Admin Portal > Academic Structure | Medium | S3 | Functional |  | R3 FS v1.1 §3.3 F03-AC06; BR-R3-07; Tender R3 Item 3 |
| [`TC-R3-F03-002`](#tc-r3-f03-002) | `TS-R3-F03` | Verify system blocks duplicate Academic Level code within same management scope | Admin Portal > Academic Structure | Medium | S3 | Negative |  | R3 FS v1.1 §3.3 F03-AC07; BR-R3-07 |
| [`TC-R3-F03-003`](#tc-r3-f03-003) | `TS-R3-F03` | Verify Academic Level referenced by active Class/Rate Rule cannot be deleted (Deactivation only) | Admin Portal > Academic Structure | High | S2 | Integrity |  | R3 FS v1.1 §3.3 F03-AC08; BR-R3-08 |
| [`TC-R3-F03-004`](#tc-r3-f03-004) | `TS-R3-F03` | Verify Academic Level is a standardized nationwide catalog centrally managed by MOE HQ | Admin Portal > Central Catalogs | Medium | S3 | Integration |  | R3 FS v1.1 §3.3 F03; Q04; §1.2 Actors |
| [`TC-R3-F04-001`](#tc-r3-f04-001) | `TS-R3-F04` | Verify School User creates Class linked to valid Level and School | Admin Portal > Classes | High | S2 | Functional |  | R3 FS v1.1 §3.4 F04-AC09; BR-R3-09; Tender R3 Item 3 |
| [`TC-R3-F04-002`](#tc-r3-f04-002) | `TS-R3-F04` | Verify system rejects Class creation if Level belongs to another School | Admin Portal > Classes | High | S2 | Integrity |  | R3 FS v1.1 §3.4 F04-AC10; BR-R3-09 |
| [`TC-R3-F04-003`](#tc-r3-f04-003) | `TS-R3-F04` | Verify system blocks duplicate class_code within the same School and Academic Year | Admin Portal > Classes | High | S2 | Negative |  | R3 FS v1.1 §3.4 F04-AC11; BR-R3-10 |
| [`TC-R3-F04-004`](#tc-r3-f04-004) | `TS-R3-F04` | Verify Class deactivation is blocked while active student enrolments exist | Admin Portal > Classes | High | S2 | StateTransition |  | R3 FS v1.1 §3.4 F04; BR-R3-11; Q03 |
| [`TC-R3-F04-005`](#tc-r3-f04-005) | `TS-R3-F04` | Verify Class max_capacity boundary enforcement (30/30) and Bulk Transfer feature upon class merge | Admin Portal > Classes | High | S2 | BVA |  | R3 FS v1.1 §3.4 F04; Q03; BVA |
| [`TC-R3-F04-006`](#tc-r3-f04-006) | `TS-R3-F04` | Verify rejection of Class creation with invalid/negative max_capacity or blank class_code | Admin Portal > Classes | Medium | S3 | Negative |  | R3 FS v1.1 §3.4 F04; BVA validation |
| [`TC-R3-F05-001`](#tc-r3-f05-001) | `TS-R3-F05` | Verify creation of Student with valid Singapore NRIC and valid Date of Birth | Admin Portal > Students | High | S2 | Functional |  | R3 FS v1.1 §3.5 F05-AC12; BR-R3-12; Tender R3 Item 3 |
| [`TC-R3-F05-002`](#tc-r3-f05-002) | `TS-R3-F05` | Verify system rejects duplicate Student national identifier (NRIC/FIN) | Admin Portal > Students | High | S2 | Negative |  | R3 FS v1.1 §3.5 F05-AC13; BR-R3-12 |
| [`TC-R3-F05-003`](#tc-r3-f05-003) | `TS-R3-F05` | Verify Student with existing enrolments or Student Charges cannot be deleted (Deactivation only) | Admin Portal > Students | High | S2 | Integrity |  | R3 FS v1.1 §3.5 F05-AC14; BR-R3-15 |
| [`TC-R3-F05-004`](#tc-r3-f05-004) | `TS-R3-F05` | Verify Singapore Checksum Modulo 11 validation on NRIC / FIN identifiers | Admin Portal > Students | High | S2 | Security |  | R3 FS v1.1 §3.5 F05; Q07; GovTech IM8 |
| [`TC-R3-F05-005`](#tc-r3-f05-005) | `TS-R3-F05` | Verify Data Masking of NRIC/FIN on Admin Portal UI according to PDPA / IM8 guidelines | Admin Portal > Student Roster | High | S2 | Security |  | R3 FS v1.1 §3.5 F05; Q07; PDPA Compliance |
| [`TC-R3-F05-006`](#tc-r3-f05-006) | `TS-R3-F05` | Verify Student Category adheres strictly to 4 MOE Singapore Tiers | Admin Portal > Students | High | S2 | DecisionTable |  | R3 FS v1.1 §3.5 F05; §3.11 F11; Q08; BR-R3-13 |
| [`TC-R3-F05-007`](#tc-r3-f05-007) | `TS-R3-F05` | Verify Student status transitions to WITHDRAWN upon official student withdrawal | Admin Portal > Students | High | S2 | StateTransition |  | R3 FS v1.1 §3.5 F05; BR-R3-15; Q06 |
| [`TC-R3-F05-008`](#tc-r3-f05-008) | `TS-R3-F05` | Verify School User cannot alter Student citizenship/category; restricted to MOE HQ with audit log | Admin Portal > Students | High | S2 | Security |  | R3 FS v1.1 §3.5 F05; BR-R3-14; Q08 |
| [`TC-R3-F05-009`](#tc-r3-f05-009) | `TS-R3-F05` | Verify Batch upload of student roster via CSV/Excel template with row-level error validation | Admin Portal > Students > Batch Upload | High | S2 | Functional |  | R3 FS v1.1 §1.4 WA-R3-02; §3.5 F05; Q02 |
| [`TC-R3-F06-001`](#tc-r3-f06-001) | `TS-R3-F06` | Verify assigning Student to active Class creates active enrolment with start_date | Admin Portal > Enrolment | High | S2 | Functional |  | R3 FS v1.1 §3.6 F06-AC15; BR-R3-16; Tender R3 Item 3 |
| [`TC-R3-F06-002`](#tc-r3-f06-002) | `TS-R3-F06` | Verify system prevents enrolling Student into multiple active classes in the same Academic Year | Admin Portal > Enrolment | High | S2 | Negative |  | R3 FS v1.1 §3.6 F06-AC16; BR-R3-17 |
| [`TC-R3-F06-003`](#tc-r3-f06-003) | `TS-R3-F06` | Verify system rejects assigning Student to Class belonging to a different School | Admin Portal > Enrolment | High | S2 | Integrity |  | R3 FS v1.1 §3.6 F06-AC17; BR-R3-18 |
| [`TC-R3-F06-004`](#tc-r3-f06-004) | `TS-R3-F06` | Verify assigning Singaporean Student to Class automatically initiates F08 Education Account linkage | Admin Portal > Enrolment | High | S2 | Integration |  | R3 FS v1.1 §3.6 F06; BR-R3-20; §3.8 F08-AC21; Tender R3 Item 3 |
| [`TC-R3-F07-001`](#tc-r3-f07-001) | `TS-R3-F07` | Verify Student Transfer closes old enrolment (end_date) and creates new enrolment in target School/Class | Admin Portal > Student Transfer | High | S2 | Functional |  | R3 FS v1.1 §3.7 F07-AC18; BR-R3-21; BR-R3-22 |
| [`TC-R3-F07-002`](#tc-r3-f07-002) | `TS-R3-F07` | Verify historical Student Charges at previous school remain attached to previous school | Admin Portal > Student Transfer | Critical | S1 | Integrity |  | R3 FS v1.1 §3.7 F07-AC19; BR-R3-23; Q10; Tender R3 Item 3 |
| [`TC-R3-F07-003`](#tc-r3-f07-003) | `TS-R3-F07` | Verify full audit log recorded for Student Transfer (actor, timestamp, old and new school/class) | Admin Portal > Student Transfer > Audit Log | Medium | S3 | Audit |  | R3 FS v1.1 §3.7 F07-AC20; BR-R3-24 |
| [`TC-R3-F07-004`](#tc-r3-f07-004) | `TS-R3-F07` | Verify Proration calculation for mid-month school transfer fees | Admin Portal > Fee Calculation | High | S2 | BVA |  | R3 FS v1.1 §3.7 F07; BR-R3-25; Q10 |
| [`TC-R3-F08-001`](#tc-r3-f08-001) | `TS-R3-F08` | Verify Singaporean Citizen student is automatically linked to Education Account created by R1 | Admin Portal > Students | High | S2 | Integration |  | R3 FS v1.1 §3.8 F08-AC21; BR-R3-26; BR-R3-27; Tender R3 Item 3 |
| [`TC-R3-F08-002`](#tc-r3-f08-002) | `TS-R3-F08` | Verify non-Singaporean student (PR, IS) does not receive Education Account linkage | Admin Portal > Students | High | S2 | Functional |  | R3 FS v1.1 §3.8 F08-AC22; BR-R3-28; Tender R3 Item 3 |
| [`TC-R3-F08-003`](#tc-r3-f08-003) | `TS-R3-F08` | Verify Idempotency: System prevents creating duplicate Education Account linkages for same student | Admin Portal > Students | High | S2 | Integrity |  | R3 FS v1.1 §3.8 F08-AC23; BR-R3-29 |
| [`TC-R3-F08-004`](#tc-r3-f08-004) | `TS-R3-F08` | Verify student turning 16 boundary: Edusave closed, account linkage transitions to PSEA / payment blocked | Admin Portal > Students | High | S2 | BVA |  | R3 FS v1.1 §3.8 F08; BR-R3-30; Q11; R1 Boundary |
| [`TC-R3-F08-005`](#tc-r3-f08-005) | `TS-R3-F08` | Verify Student gaining Singapore Citizenship mid-year triggers automatic Education Account creation & linkage | Admin Portal > Students | High | S2 | Integration |  | R3 FS v1.1 §3.8 F08; BR-R3-26; Q11 |
| [`TC-R3-F09-001`](#tc-r3-f09-001) | `TS-R3-F09` | Verify creation of Fee Type with unique fee_type_code | Admin Portal > Fee Types | Medium | S3 | Functional |  | R3 FS v1.1 §3.9 F09-AC24; BR-R3-31; Tender R3 Item 3 |
| [`TC-R3-F09-002`](#tc-r3-f09-002) | `TS-R3-F09` | Verify system rejects Fee Type with duplicate fee_type_code | Admin Portal > Fee Types | Medium | S3 | Negative |  | R3 FS v1.1 §3.9 F09-AC25; BR-R3-31 |
| [`TC-R3-F09-003`](#tc-r3-f09-003) | `TS-R3-F09` | Verify system assigns is_active = true by default upon Fee Type creation | Admin Portal > Fee Types | Low | S4 | Functional |  | R3 FS v1.1 §3.9 F09-AC26; BR-R3-32 |
| [`TC-R3-F09-004`](#tc-r3-f09-004) | `TS-R3-F09` | Verify Standard vs Autonomous Fee Types: MOE HQ catalog vs School-specific ownership | Admin Portal > Fee Types | Medium | S3 | Security |  | R3 FS v1.1 §3.9 F09; BR-R3-33; Q12 |
| [`TC-R3-F10-001`](#tc-r3-f10-001) | `TS-R3-F10` | Verify creation of Fee Component linked to valid parent Fee Type with unique code | Admin Portal > Fee Components | High | S2 | Functional |  | R3 FS v1.1 §3.10 F10-AC27; BR-R3-35; BR-R3-36; Tender R3 Item 3 |
| [`TC-R3-F10-002`](#tc-r3-f10-002) | `TS-R3-F10` | Verify system rejects Fee Component creation if parent Fee Type does not exist or is inactive | Admin Portal > Fee Components | Medium | S3 | Negative |  | R3 FS v1.1 §3.10 F10-AC28; BR-R3-35 |
| [`TC-R3-F10-003`](#tc-r3-f10-003) | `TS-R3-F10` | Verify system assigns is_apply_tax = true by default upon Fee Component creation | Admin Portal > Fee Components | Low | S4 | Functional |  | R3 FS v1.1 §3.10 F10-AC29; BR-R3-37 |
| [`TC-R3-F10-004`](#tc-r3-f10-004) | `TS-R3-F10` | Verify owner_school_id references valid School ID or MOE HQ ID, not arbitrary user ID | Admin Portal > Fee Components | High | S2 | Integrity |  | R3 FS v1.1 §3.10 F10; BR-R3-38; Q12 |
| [`TC-R3-F10-005`](#tc-r3-f10-005) | `TS-R3-F10` | Verify allow_edusave_payment flag governs Education Account payment eligibility | Admin Portal > Fee Components | Critical | S1 | Functional |  | R3 FS v1.1 §3.10 F10; BR-R3-39; §4 Payment Rule; Tender R3 Item 3 |
| [`TC-R3-F10-006`](#tc-r3-f10-006) | `TS-R3-F10` | Verify Fee Component with is_taxable = true applies Singapore GST (9%) correctly | Admin Portal > Fee Components | High | S2 | Calculation |  | R3 FS v1.1 §3.10 F10; §3.15 F15; BR-R3-40; Q13 |
| [`TC-R3-F11-001`](#tc-r3-f11-001) | `TS-R3-F11` | Verify creation of Fee Rate Rule with positive price_amount and valid date range | Admin Portal > Fee Rates | High | S2 | Functional |  | R3 FS v1.1 §3.11 F11-AC30; BR-R3-41; Tender R3 Item 3 |
| [`TC-R3-F11-002`](#tc-r3-f11-002) | `TS-R3-F11` | Verify Academic Level set to null in rate rule applies as wildcard across all levels | Admin Portal > Fee Rates | High | S2 | Functional |  | R3 FS v1.1 §3.11 F11-AC31; BR-R3-42 |
| [`TC-R3-F11-003`](#tc-r3-f11-003) | `TS-R3-F11` | Verify rate rule evaluation matches strictly on student_category (SC vs PR vs IS) | Admin Portal > Fee Rates | Critical | S1 | DecisionTable |  | R3 FS v1.1 §3.11 F11-AC32; BR-R3-43; Tender R3 Item 3 |
| [`TC-R3-F11-004`](#tc-r3-f11-004) | `TS-R3-F11` | Verify if no rate rule matches, system raises explicit missing rule error, never arbitrary charge | Admin Portal > Fee Rates | High | S2 | Negative |  | R3 FS v1.1 §3.11 F11-AC33; BR-R3-44 |
| [`TC-R3-F11-005`](#tc-r3-f11-005) | `TS-R3-F11` | Verify system rejects Fee Rate Rule with negative or zero price_amount | Admin Portal > Fee Rates | High | S2 | BVA |  | R3 FS v1.1 §3.11 F11; BR-R3-41; BVA |
| [`TC-R3-F11-006`](#tc-r3-f11-006) | `TS-R3-F11` | Verify system prevents overlapping effective date ranges for identical Component + Level + Category | Admin Portal > Fee Rates | High | S2 | Integrity |  | R3 FS v1.1 §3.11 F11; BR-R3-45 |
| [`TC-R3-F11-007`](#tc-r3-f11-007) | `TS-R3-F11` | Verify Rule Precedence: Specific Level rule takes precedence over Wildcard Level rule | Admin Portal > Fee Rates | High | S2 | DecisionTable |  | R3 FS v1.1 §3.11 F11; BR-R3-46; Q14 |
| [`TC-R3-F11-008`](#tc-r3-f11-008) | `TS-R3-F11` | Verify currency precision enforcement: Banker's Rounding to 2 decimal places in SGD | Admin Portal > Fee Rates | High | S2 | BVA |  | R3 FS v1.1 §3.11 F11; BR-R3-41; IEEE-754 prevention |
| [`TC-R3-F12-001`](#tc-r3-f12-001) | `TS-R3-F12` | Verify Fee Publication lifecycle transitions from DRAFT to PUBLISHED | Admin Portal > Fee Publication | High | S2 | StateTransition |  | R3 FS v1.1 §3.12 F12-AC34; BR-R3-47; BR-R3-48; Tender R3 Item 3 |
| [`TC-R3-F12-002`](#tc-r3-f12-002) | `TS-R3-F12` | Verify system rejects Fee Publication with invalid billing period (end_date < start_date) | Admin Portal > Fee Publication | High | S2 | Negative |  | R3 FS v1.1 §3.12 F12-AC35; BR-R3-48 |
| [`TC-R3-F12-003`](#tc-r3-f12-003) | `TS-R3-F12` | Verify Fee Publication with pricing_mode = RATE_RULE enforces fixed_amount fields are null | Admin Portal > Fee Publication | Medium | S3 | Validation |  | R3 FS v1.1 §3.12 F12-AC36; BR-R3-47 |
| [`TC-R3-F12-004`](#tc-r3-f12-004) | `TS-R3-F12` | Verify Fee Publication with pricing_mode = FIXED_AMOUNT requires valid fixed price_amount | Admin Portal > Fee Publication | Medium | S3 | Validation |  | R3 FS v1.1 §3.12 F12-AC37; BR-R3-47 |
| [`TC-R3-F12-005`](#tc-r3-f12-005) | `TS-R3-F12` | Verify status PUBLISHED is immutable; cannot be edited or re-published, records published_by/at | Admin Portal > Fee Publication | High | S2 | Integrity |  | R3 FS v1.1 §3.12 F12-AC38; BR-R3-49 |
| [`TC-R3-F12-006`](#tc-r3-f12-006) | `TS-R3-F12` | Verify Optimistic locking / row_version: concurrent edits generate conflict warning | Admin Portal > Fee Publication | High | S2 | Concurrency |  | R3 FS v1.1 §3.12 F12-AC39; BR-R3-51; EF01 |
| [`TC-R3-F12-007`](#tc-r3-f12-007) | `TS-R3-F12` | Verify Date sequence validation: due_date must not be earlier than charge_date | Admin Portal > Fee Publication | High | S2 | BVA |  | R3 FS v1.1 §3.12 F12; BR-R3-52; Q18 |
| [`TC-R3-F12-008`](#tc-r3-f12-008) | `TS-R3-F12` | Verify Maker-Checker Principle (Four-Eyes): Approver must be distinct from Creator | Admin Portal > Fee Publication | Critical | S1 | Security |  | R3 FS v1.1 §3.12 F12; BR-R3-49; Q16 |
| [`TC-R3-F12-009`](#tc-r3-f12-009) | `TS-R3-F12` | Verify asynchronous PROCESSING state prevents duplicate fee publication execution | Admin Portal > Fee Publication | High | S2 | Concurrency |  | R3 FS v1.1 §3.12 F12; BR-R3-51; Q17 |
| [`TC-R3-F13-001`](#tc-r3-f13-001) | `TS-R3-F13` | Verify Target mode ALL_STUDENTS (Component Scope) resolves all active students of the School | Admin Portal > Publication Target | High | S2 | Functional |  | R3 FS v1.1 §3.13 F13-AC40; BR-R3-53; Tender R3 Item 3 |
| [`TC-R3-F13-002`](#tc-r3-f13-002) | `TS-R3-F13` | Verify Target mode BY_LEVEL selects strictly students enrolled in specified Level | Admin Portal > Publication Target | High | S2 | Functional |  | R3 FS v1.1 §3.13 F13-AC41; BR-R3-54 |
| [`TC-R3-F13-003`](#tc-r3-f13-003) | `TS-R3-F13` | Verify Target mode BY_CLASS selects strictly students enrolled in specified Class | Admin Portal > Publication Target | High | S2 | Functional |  | R3 FS v1.1 §3.13 F13-AC42; BR-R3-54 |
| [`TC-R3-F13-004`](#tc-r3-f13-004) | `TS-R3-F13` | Verify Target mode SPECIFIC_STUDENTS validates each individual student eligibility | Admin Portal > Publication Target | Medium | S3 | Functional |  | R3 FS v1.1 §3.13 F13-AC43; BR-R3-53 |
| [`TC-R3-F13-005`](#tc-r3-f13-005) | `TS-R3-F13` | Verify system rejects target configuration if Level, Class, or Student belongs to another School | Admin Portal > Publication Target | Critical | S1 | Negative |  | R3 FS v1.1 §3.13 F13-AC44; BR-R3-54; §5.2 Access Control |
| [`TC-R3-F13-006`](#tc-r3-f13-006) | `TS-R3-F13` | Verify Target combination logic: Target entities UNION combined with Citizenship filter INTERSECTION | Admin Portal > Publication Target | High | S2 | DecisionTable |  | R3 FS v1.1 §3.13 F13; BR-R3-55; BR-R3-57; Q02 |
| [`TC-R3-F13-007`](#tc-r3-f13-007) | `TS-R3-F13` | Verify Target membership evaluated strictly as of eligibility_date | Admin Portal > Publication Target | High | S2 | Functional |  | R3 FS v1.1 §3.13 F13; BR-R3-56 |
| [`TC-R3-F14-001`](#tc-r3-f14-001) | `TS-R3-F14` | Verify Recipient Resolution accurately resolves students with active enrolment on eligibility_date | Admin Portal > Recipient Resolution | High | S2 | Functional |  | R3 FS v1.1 §3.14 F14-AC45; BR-R3-58; BR-R3-59 |
| [`TC-R3-F14-002`](#tc-r3-f14-002) | `TS-R3-F14` | Verify Idempotency: Re-running Recipient Resolution produces identical recipients with zero duplicates | Admin Portal > Recipient Resolution | High | S2 | Integrity |  | R3 FS v1.1 §3.14 F14-AC46; BR-R3-60 |
| [`TC-R3-F14-003`](#tc-r3-f14-003) | `TS-R3-F14` | Verify system rejects recipient resolution if enrolment record belongs to another student | Admin Portal > Recipient Resolution | High | S2 | Integrity |  | R3 FS v1.1 §3.14 F14-AC47; BR-R3-61 |
| [`TC-R3-F14-004`](#tc-r3-f14-004) | `TS-R3-F14` | Verify Recipient resolver excludes students with status WITHDRAWN on eligibility_date | Admin Portal > Recipient Resolution | High | S2 | Functional |  | R3 FS v1.1 §3.14 F14; BR-R3-58; Q06 |
| [`TC-R3-F15-001`](#tc-r3-f15-001) | `TS-R3-F15` | Verify Student Charge generated for each resolved recipient with initial status DRAFT | Admin Portal > Charge Generation | High | S2 | Functional |  | R3 FS v1.1 §3.15 F15-AC48; BR-R3-62; Tender R3 Item 3 |
| [`TC-R3-F15-002`](#tc-r3-f15-002) | `TS-R3-F15` | Verify Student Charge calculates total_amount = base_amount + tax_amount (GST 9%) | Admin Portal > Charge Generation | High | S2 | Calculation |  | R3 FS v1.1 §3.15 F15-AC49; BR-R3-63 |
| [`TC-R3-F15-003`](#tc-r3-f15-003) | `TS-R3-F15` | Verify system rejects Student Charge with negative amount | Admin Portal > Charge Generation | High | S2 | Negative |  | R3 FS v1.1 §3.15 F15-AC50; BR-R3-64 |
| [`TC-R3-F15-004`](#tc-r3-f15-004) | `TS-R3-F15` | Verify unique constraint prevents duplicate charge for same Student, Publication, and Billing Period | Admin Portal > Charge Generation | High | S2 | Integrity |  | R3 FS v1.1 §3.15 F15-AC51; BR-R3-65 |
| [`TC-R3-F15-005`](#tc-r3-f15-005) | `TS-R3-F15` | Verify Manual Student Charge creation sets source_type = MANUAL and requires idempotency_key | Admin Portal > Manual Charges | High | S2 | Functional |  | R3 FS v1.1 §3.15 F15-AC52; BR-R3-66 |
| [`TC-R3-F15-006`](#tc-r3-f15-006) | `TS-R3-F15` | Verify Void Student Charge records status VOID, voided_at, and void_reason | Admin Portal > Charge Management | High | S2 | StateTransition |  | R3 FS v1.1 §3.15 F15-AC53; BR-R3-67 |
| [`TC-R3-F15-007`](#tc-r3-f15-007) | `TS-R3-F15` | Verify only POSTED charges appear in parent outstanding charges on e-Service Portal | e-Service Portal > Outstanding Charges | Critical | S1 | Visibility |  | R3 FS v1.1 §3.15 F15-AC54; BR-R3-68; Tender R3 Item 3 |
| [`TC-R3-F15-008`](#tc-r3-f15-008) | `TS-R3-F15` | Verify Snapshot integrity: student_charges records citizenship_snapshot and pricing_date snapshot | Admin Portal > Charge Management | High | S2 | Audit |  | R3 FS v1.1 §3.15 F15; BR-R3-69; Q19 |
| [`TC-R3-F15-009`](#tc-r3-f15-009) | `TS-R3-F15` | Verify Due Date calculation: due_date = charge_date + 30 days by default | Admin Portal > Charge Generation | Medium | S3 | BVA |  | R3 FS v1.1 §3.15 F15; BR-R3-70; Q18 |
| [`TC-R3-F15-010`](#tc-r3-f15-010) | `TS-R3-F15` | Verify Payment status initialized to UNPAID and paid_amount = 0.00 upon charge generation | Admin Portal > Charge Generation | Medium | S3 | Functional |  | R3 FS v1.1 §3.15 F15; BR-R3-62; Q20 |
| [`TC-R3-F16-001`](#tc-r3-f16-001) | `TS-R3-F16` | Verify Student Charge Adjustment creates valid adjustment record with reason code | Admin Portal > Charge Adjustment | High | S2 | Functional |  | R3 FS v1.1 §3.16 F16-AC55; BR-R3-71; Tender R3 Item 3 |
| [`TC-R3-F16-002`](#tc-r3-f16-002) | `TS-R3-F16` | Verify Positive adjustment increases effective amount due | Admin Portal > Charge Adjustment | High | S2 | Calculation |  | R3 FS v1.1 §3.16 F16-AC56; BR-R3-72 |
| [`TC-R3-F16-003`](#tc-r3-f16-003) | `TS-R3-F16` | Verify Negative adjustment decreases effective amount due | Admin Portal > Charge Adjustment | High | S2 | Calculation |  | R3 FS v1.1 §3.16 F16-AC57; BR-R3-72 |
| [`TC-R3-F16-004`](#tc-r3-f16-004) | `TS-R3-F16` | Verify original charge base_amount and tax_amount remain strictly immutable upon adjustment | Admin Portal > Charge Adjustment | Critical | S1 | Integrity |  | R3 FS v1.1 §3.16 F16-AC58; BR-R3-73; WA-R3-09 |
| [`TC-R3-F16-005`](#tc-r3-f16-005) | `TS-R3-F16` | Verify Audit tracking records created_by, created_at, and reason_code for every adjustment | Admin Portal > Charge Adjustment | Medium | S3 | Audit |  | R3 FS v1.1 §3.16 F16-AC59; BR-R3-74 |
| [`TC-R3-F16-006`](#tc-r3-f16-006) | `TS-R3-F16` | Verify Adjustment in PENDING_APPROVAL status is not applied to effective balance until approved | Admin Portal > Charge Adjustment | High | S2 | StateTransition |  | R3 FS v1.1 §3.16 F16-AC60; BR-R3-75 |
| [`TC-R3-F16-007`](#tc-r3-f16-007) | `TS-R3-F16` | Verify system blocks adjustment that would result in negative effective amount | Admin Portal > Charge Adjustment | High | S2 | Negative |  | R3 FS v1.1 §3.16 F16; BR-R3-76; BVA |
| [`TC-R3-F16-008`](#tc-r3-f16-008) | `TS-R3-F16` | Verify Foreign Key validation: adjustment must link to valid student_charge_id | Admin Portal > Charge Adjustment | Medium | S3 | Integrity |  | R3 FS v1.1 §3.16 F16; BR-R3-77; Q21 |
| [`TC-R3-F16-009`](#tc-r3-f16-009) | `TS-R3-F16` | Verify Tiered Approval Threshold: School approves < $200 SGD, MOE HQ approves >= $200 SGD | Admin Portal > Charge Adjustment | High | S2 | Security |  | R3 FS v1.1 §3.16 F16; BR-R3-78; Q16 |
| [`TC-R3-PAY-001`](#tc-r3-pay-001) | `TS-R3-PAY` | Verify only Singaporean Student charges with eligible Fee Component can be paid via Edusave | e-Service Portal > Payment | Critical | S1 | Functional |  | R3 FS v1.1 §4 Payment Rule; BR-R3-80; Tender R3 Item 3 |
| [`TC-R3-PAY-002`](#tc-r3-pay-002) | `TS-R3-PAY` | Verify system rejects Edusave payment attempt for non-eligible Fee Component (allow_edusave_payment = false) | e-Service Portal > Payment | Critical | S1 | Negative |  | R3 FS v1.1 §4 Payment Rule; BR-R3-81; Tender R3 Item 3 |
| [`TC-R3-PAY-003`](#tc-r3-pay-003) | `TS-R3-PAY` | Verify Full Edusave Payment: Account balance >= charge amount deducts balance and sets status PAID | e-Service Portal > Payment | Critical | S1 | Functional |  | R3 FS v1.1 §4 Payment Rule; BR-R3-82; Tender R3 Item 3 |
| [`TC-R3-PAY-004`](#tc-r3-pay-004) | `TS-R3-PAY` | Verify Split Payment: Insufficient Education Account balance deducts available balance, remaining balance stays UNPAID | e-Service Portal > Payment | Critical | S1 | BVA |  | R3 FS v1.1 §4 Payment Rule; BR-R3-83; Q15; Tender R3 Item 3 |
| [`TC-R3-PAY-005`](#tc-r3-pay-005) | `TS-R3-PAY` | Verify Concurrency: Prevent race condition on simultaneous payment requests against same Education Account | e-Service Portal > Payment | Critical | S1 | Concurrency |  | R3 FS v1.1 §4 Payment Rule; BR-R3-84; Concurrency Isolation |
| [`TC-R3-TENDER-001`](#tc-r3-tender-001) | `TS-R3-TENDER` | End-to-End Workflow: MOE HQ creates school -> School creates roster -> HQ publishes fee -> Student pays via Edusave | Admin Portal & e-Service Portal | Critical | S1 | Integration |  | Tender R3 Item 3; R3 FS v1.1 §2 Process Overview; §3 F01-F16; §4 Payment Rule |

---

## Detailed Test Case Specifications


### Test Suite: School Management

#### `TC-R3-F01-001`: Verify MOE HQ User successfully creates a new School with unique school_code

- **Scenario ID**: `TS-R3-F01`
- **Test Suite**: School Management
- **Page / Target**: `Admin Portal > School Setup`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R3 FS v1.1 §3.1 F01-AC01; BR-R3-01; BR-R3-02; Tender R3 Item 3
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: CR: MOE HQ maintains school list. TD: unique school_code constraint.
- **Note**: Happy path verification for School creation.

**Preconditions:**
```text
MOE HQ User is logged in to Admin Portal. school_code 'SCH-RI-01' does not exist in schools table.
```

**Test Data:**
```text
school_code: 'SCH-RI-01', school_name: 'Raffles Institution', school_type: 'Government'
```

**Test Steps:**
1. Navigate to School Management screen.
2. Click [Add New School].
3. Enter school_code 'SCH-RI-01', school_name 'Raffles Institution', and school_type.
4. Click [Save].

**Expected Result:**
> 1. System displays success message 'School created successfully'.
> 2. New school record is created in schools table with status = 'ACTIVE' (BR-R3-02).
> 3. School appears in the active school list.

---

#### `TC-R3-F01-002`: Verify system rejects School creation with duplicate school_code

- **Scenario ID**: `TS-R3-F01`
- **Test Suite**: School Management
- **Page / Target**: `Admin Portal > School Setup`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Negative`
- **Traceability**: R3 FS v1.1 §3.1 F01-AC02; BR-R3-01
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: TD: unique index on schools(school_code).
- **Note**: Data integrity test: Unique constraint on school_code.

**Preconditions:**
```text
School with school_code 'SCH-RI-01' already exists in schools table with status Active.
```

**Test Data:**
```text
school_code: 'SCH-RI-01', school_name: 'Duplicate Raffles High'
```

**Test Steps:**
1. Navigate to School Management screen.
2. Click [Add New School].
3. Enter existing school_code 'SCH-RI-01' and a different name.
4. Click [Save].

**Expected Result:**
> 1. System blocks creation and displays validation error: 'school_code already exists' (HTTP 409 Conflict).
> 2. No duplicate record is inserted into schools table (BR-R3-01). Database record count remains 1.

---

#### `TC-R3-F01-003`: Verify deactivating a School preserves existing data but blocks new configurations/publications

- **Scenario ID**: `TS-R3-F01`
- **Test Suite**: School Management
- **Page / Target**: `Admin Portal > School Setup`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `StateTransition`
- **Traceability**: R3 FS v1.1 §3.1 F01-AC03; BR-R3-03
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: TD: Soft-deactivation pattern; preserve historical ledger.
- **Note**: Verifies soft-delete / deactivation behavior preserves historical audit trail.

**Preconditions:**
```text
School 'SCH-RI-01' exists with active classes, enrolments, and historical student charges.
```

**Test Data:**
```text
school_code: 'SCH-RI-01', target_status: 'INACTIVE'
```

**Test Steps:**
1. Open School 'SCH-RI-01' profile.
2. Set status to 'INACTIVE' and click [Save].
3. Query database to verify existing classes and charges are untouched.
4. Attempt to create a new Fee Publication targeting 'SCH-RI-01'.

**Expected Result:**
> 1. School status updates to 'INACTIVE' in schools table.
> 2. All existing classes, student enrolments, and student charges are preserved intact.
> 3. Attempt to create new Fee Publication is rejected with error 'Cannot publish fees for inactive school' (HTTP 422 Unprocessable Entity).

---

#### `TC-R3-F01-004`: Verify School creation validates and stores Singapore school_type enum

- **Scenario ID**: `TS-R3-F01`
- **Test Suite**: School Management
- **Page / Target**: `Admin Portal > School Setup`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R3 FS v1.1 §3.1 F01; WA-R3-10; Q18
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: WA: 4 Singapore school types needed for Top-Up (R2) and fee tiering.
- **Note**: School classification enables downstream funding and fee tiering rules.

**Preconditions:**
```text
MOE HQ User is logged in to Admin Portal.
```

**Test Data:**
```text
Valid types: ['Government', 'Government-Aided', 'Independent', 'Specialised']. Invalid: 'Private_Tutoring'
```

**Test Steps:**
1. Attempt to create school with each valid school_type.
2. Attempt to create school with invalid school_type 'Private_Tutoring'.

**Expected Result:**
> 1. Valid school types are accepted and stored correctly in database.
> 2. Invalid school type is rejected with validation error 'Invalid school type enum value' (HTTP 422).

---

#### `TC-R3-F01-005`: Verify boundary length validation on school_code and school_name fields

- **Scenario ID**: `TS-R3-F01`
- **Test Suite**: School Management
- **Page / Target**: `Admin Portal > School Setup`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `BVA`
- **Traceability**: R3 FS v1.1 §3.1 F01; BVA boundary rules
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: TD: Field boundary limits defined per standard database schema.
- **Note**: Boundary value analysis on schema column limits.

**Preconditions:**
```text
MOE HQ User on School Setup page.
```

**Test Data:**
```text
Boundary 1: school_code 1 char ('A'). Boundary 2: 20 chars ('SCH-1234567890123456'). Boundary 3: 21 chars. school_name: 200 chars vs 201 chars.
```

**Test Steps:**
1. Submit school with school_code = 'A' (length 1).
2. Submit school with school_code of length 20.
3. Submit school with school_code of length 21.
4. Submit school with school_name of length 200 vs 201.

**Expected Result:**
> 1. school_code length 1 rejected ('Min length 2 chars').
> 2. school_code length 20 accepted (HTTP 201).
> 3. school_code length 21 rejected ('Max length 20 chars').
> 4. school_name 200 chars accepted; 201 chars rejected ('Max length 200 chars').

---


### Test Suite: User Management & Security

#### `TC-R3-F02-001`: Verify MOE HQ User assigns School User to at least one valid School

- **Scenario ID**: `TS-R3-F02`
- **Test Suite**: User Management & Security
- **Page / Target**: `Admin Portal > User Management`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R3 FS v1.1 §3.2 F02-AC04; BR-R3-04; Tender R3 Item 3
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: CR: MOE HQ maintains school users. TD: user_schools mapping table.
- **Note**: Validates tenant assignment.

**Preconditions:**
```text
Active School 'SCH-RI-01' exists. User 'finance.officer@ri.edu.sg' is provisioned.
```

**Test Data:**
```text
user_id: 'USR-FO-01', school_id: 'SCH-RI-01', role: 'SCHOOL_USER'
```

**Test Steps:**
1. Navigate to User Management screen.
2. Select user 'USR-FO-01'.
3. Assign user to School 'SCH-RI-01' with role 'SCHOOL_USER'.
4. Click [Save].

**Expected Result:**
> 1. System displays 'User assigned to school successfully'.
> 2. Record created in user_schools table linking user_id and school_id.
> 3. User gains access to manage Academic Levels and Classes for 'SCH-RI-01'.

---

#### `TC-R3-F02-002`: Verify multi-tenant isolation: School User of School A cannot access School B data

- **Scenario ID**: `TS-R3-F02`
- **Test Suite**: User Management & Security
- **Page / Target**: `Admin Portal > Academic Structure`
- **Severity / Priority**: `S1` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Security`
- **Traceability**: R3 FS v1.1 §3.2 F02-AC05; BR-R3-05; §5.2 Access Control
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: CR: Multi-tenant data segregation mandatory. TD: Tenant Guard Middleware.
- **Note**: Critical P0 security test: Prevents Broken Object Level Authorization (BOLA/IDOR).

**Preconditions:**
```text
School User A belongs to School 'SCH-RI-01'. School B 'SCH-HCI-02' has classes and students. User A authenticated with valid JWT token.
```

**Test Data:**
```text
User A Bearer Token. Target endpoint: GET /api/v1/schools/SCH-HCI-02/classes
```

**Test Steps:**
1. Log in as School User A.
2. Dispatch API request GET /api/v1/schools/SCH-HCI-02/classes using User A token.
3. Attempt to fetch student list of School B via URL tampering.

**Expected Result:**
> 1. System rejects request with HTTP 403 Forbidden.
> 2. Error payload returns error_code 'ERR_TENANT_ACCESS_DENIED'.
> 3. Security audit log records unauthorized cross-tenant attempt with user_id, IP, and timestamp.

---

#### `TC-R3-F02-003`: Verify School User first-time login mandates password change and 2FA setup per IM8

- **Scenario ID**: `TS-R3-F02`
- **Test Suite**: User Management & Security
- **Page / Target**: `Admin Portal > Authentication`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Security`
- **Traceability**: R3 FS v1.1 §3.2 F02; BR-R3-06; Q05
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: WA: GovTech IM8 security compliance mandates 2FA and initial password rotation.
- **Note**: Enforces Singapore government cybersecurity baseline IM8.

**Preconditions:**
```text
HQ User created School User with temporary password. User has not logged in before.
```

**Test Data:**
```text
temp_password: 'TempPassword!123', new_password: 'NewValidPassword#2026'
```

**Test Steps:**
1. Enter username and temporary password on login screen.
2. Inspect response and redirection.
3. Attempt to navigate directly to /admin/schools without changing password.

**Expected Result:**
> 1. System intercepts login and redirects to /force-change-password.
> 2. Direct URL access to dashboard is blocked (HTTP 403 / Redirect).
> 3. User must successfully change password and bind 2FA authenticator before session token is activated.

---

#### `TC-R3-F02-004`: Verify Segregation of Duties: School Admin, School Finance, and Teacher sub-roles

- **Scenario ID**: `TS-R3-F02`
- **Test Suite**: User Management & Security
- **Page / Target**: `Admin Portal > RBAC`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Security`
- **Traceability**: R3 FS v1.1 §1.2 Actors; §3.2 F02; Q01
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: WA: School User sub-roles required for Segregation of Duties.
- **Note**: Prevents unauthorized operations through strict Role-Based Access Control.

**Preconditions:**
```text
Users provisioned with distinct roles: School Admin (USR-SA), School Finance (USR-SF), Teacher (USR-TCH).
```

**Test Data:**
```text
Endpoints: POST /api/v1/classes (Admin only); POST /api/v1/fee-publications (Finance only); GET /api/v1/classes/mine (Teacher)
```

**Test Steps:**
1. As USR-TCH, attempt to publish fees (POST /api/v1/fee-publications).
2. As USR-TCH, attempt to create a new Class.
3. As USR-SF, attempt to add students to class.
4. As USR-SA, create class and assign students.

**Expected Result:**
> 1. Teacher fee publication attempt returns HTTP 403 Forbidden.
> 2. Teacher class creation returns HTTP 403 Forbidden.
> 3. School Finance class roster modification returns HTTP 403 Forbidden.
> 4. School Admin successfully creates class and assigns students (HTTP 201).

---

#### `TC-R3-F02-005`: Verify system rejects creating School User without associating to an active School

- **Scenario ID**: `TS-R3-F02`
- **Test Suite**: User Management & Security
- **Page / Target**: `Admin Portal > User Management`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Negative`
- **Traceability**: R3 FS v1.1 §3.2 F02; BR-R3-04
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: TD: Foreign key constraint and backend business validation on school_id.
- **Note**: Guarantees every school user belongs to a tenant.

**Preconditions:**
```text
MOE HQ User on User Management screen.
```

**Test Data:**
```text
email: 'orphan.user@moe.edu.sg', full_name: 'Orphan User', school_id: null
```

**Test Steps:**
1. Click [Add School User].
2. Enter name and email, but leave School selection empty.
3. Click [Save].

**Expected Result:**
> 1. System blocks submission and displays error: 'School User must be associated with at least one valid School' (HTTP 422).
> 2. No user record with role 'SCHOOL_USER' is created without school_id (BR-R3-04).

---


### Test Suite: Academic Structure

#### `TC-R3-F03-001`: Verify configuration of Academic Level with unique code within School

- **Scenario ID**: `TS-R3-F03`
- **Test Suite**: Academic Structure
- **Page / Target**: `Admin Portal > Academic Structure`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R3 FS v1.1 §3.3 F03-AC06; BR-R3-07; Tender R3 Item 3
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: CR: School or HQ manages academic levels. TD: sequence_order for sorting.
- **Note**: Standard level setup for cohort tracking.

**Preconditions:**
```text
School User logged in for School 'SCH-RI-01'. level_code 'PRI-1' not yet configured.
```

**Test Data:**
```text
level_code: 'PRI-1', level_name: 'Primary 1', sequence_order: 1
```

**Test Steps:**
1. Navigate to Academic Levels screen.
2. Click [Add Level].
3. Enter level_code 'PRI-1', name 'Primary 1', and sequence_order 1.
4. Click [Save].

**Expected Result:**
> 1. System displays 'Academic Level created successfully'.
> 2. Record created in academic_levels table with school_id = 'SCH-RI-01', level_code = 'PRI-1', is_active = true.
> 3. Level appears in class creation dropdown.

---

#### `TC-R3-F03-002`: Verify system blocks duplicate Academic Level code within same management scope

- **Scenario ID**: `TS-R3-F03`
- **Test Suite**: Academic Structure
- **Page / Target**: `Admin Portal > Academic Structure`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Negative`
- **Traceability**: R3 FS v1.1 §3.3 F03-AC07; BR-R3-07
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: TD: Unique constraint on (school_id, level_code).
- **Note**: Integrity constraint on academic levels.

**Preconditions:**
```text
Level 'PRI-1' already exists for School 'SCH-RI-01'.
```

**Test Data:**
```text
level_code: 'PRI-1', level_name: 'Duplicate Primary 1'
```

**Test Steps:**
1. Click [Add Level].
2. Enter existing level_code 'PRI-1'.
3. Click [Save].

**Expected Result:**
> 1. System rejects creation with validation error: 'Level code already exists for this school' (HTTP 409 Conflict).
> 2. No duplicate row inserted in academic_levels table (BR-R3-07).

---

#### `TC-R3-F03-003`: Verify Academic Level referenced by active Class/Rate Rule cannot be deleted (Deactivation only)

- **Scenario ID**: `TS-R3-F03`
- **Test Suite**: Academic Structure
- **Page / Target**: `Admin Portal > Academic Structure`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Integrity`
- **Traceability**: R3 FS v1.1 §3.3 F03-AC08; BR-R3-08
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: TD: Foreign key RESTRICT rule protects relational integrity.
- **Note**: Prevents orphaned records in fee engine.

**Preconditions:**
```text
Level 'PRI-1' is referenced by active Class 'CLS-P1-A' and Fee Rate Rule 'FRR-001'.
```

**Test Data:**
```text
level_id: 'LVL-PRI-1'
```

**Test Steps:**
1. Attempt to hard-delete Level 'LVL-PRI-1' via UI or DELETE API.
2. Update status to INACTIVE (soft-deactivate).

**Expected Result:**
> 1. Hard-delete is rejected with error: 'Cannot delete Level referenced by active classes or fee rules' (HTTP 409 Conflict).
> 2. Soft-deactivation succeeds (is_active = false); existing classes remain viewable.

---

#### `TC-R3-F03-004`: Verify Academic Level is a standardized nationwide catalog centrally managed by MOE HQ

- **Scenario ID**: `TS-R3-F03`
- **Test Suite**: Academic Structure
- **Page / Target**: `Admin Portal > Central Catalogs`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: R3 FS v1.1 §3.3 F03; Q04; §1.2 Actors
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: WA: Centralized level master catalog prevents fee rule breakage nationwide.
- **Note**: National alignment for fee publication standardization.

**Preconditions:**
```text
MOE HQ User has defined standard Singapore levels (PRI-1 to PRI-6, SEC-1 to SEC-5, JC-1 to JC-2).
```

**Test Data:**
```text
Standard levels catalog in MOE master dictionary.
```

**Test Steps:**
1. Log in as School User of newly created primary school.
2. Open Academic Levels setup.
3. Verify whether standard national levels are auto-populated or available for selection.

**Expected Result:**
> 1. Standard MOE academic levels are available across schools, preventing disparate naming like 'K1' vs 'Grade1'.
> 2. School selects applicable levels (Primary 1-6) without creating divergent codes.

---


### Test Suite: Class Management

#### `TC-R3-F04-001`: Verify School User creates Class linked to valid Level and School

- **Scenario ID**: `TS-R3-F04`
- **Test Suite**: Class Management
- **Page / Target**: `Admin Portal > Classes`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R3 FS v1.1 §3.4 F04-AC09; BR-R3-09; Tender R3 Item 3
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: CR: School User maintains classes. TD: academic_year field required.
- **Note**: Baseline happy path for class creation.

**Preconditions:**
```text
School 'SCH-RI-01' and Level 'PRI-1' exist and are ACTIVE. Academic Year 2026 is configured.
```

**Test Data:**
```text
class_code: 'P1-EMERALD', level_id: 'LVL-PRI-1', academic_year: 2026, max_capacity: 30
```

**Test Steps:**
1. Navigate to Class Management screen.
2. Click [Create Class].
3. Enter class_code 'P1-EMERALD', select Level 'Primary 1', year 2026, capacity 30.
4. Click [Save].

**Expected Result:**
> 1. System displays 'Class created successfully'.
> 2. Record created in classes table with school_id, level_id, academic_year, and status ACTIVE.
> 3. Class appears in student assignment roster.

---

#### `TC-R3-F04-002`: Verify system rejects Class creation if Level belongs to another School

- **Scenario ID**: `TS-R3-F04`
- **Test Suite**: Class Management
- **Page / Target**: `Admin Portal > Classes`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Integrity`
- **Traceability**: R3 FS v1.1 §3.4 F04-AC10; BR-R3-09
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: TD: School-Level foreign key validation constraint.
- **Note**: Prevents cross-school level contamination.

**Preconditions:**
```text
School A ('SCH-RI-01') and School B ('SCH-HCI-02') exist. Level 'LVL-SEC-1-B' belongs to School B.
```

**Test Data:**
```text
class_code: 'S1-A', level_id: 'LVL-SEC-1-B' (School B level), school_id: 'SCH-RI-01'
```

**Test Steps:**
1. As School User of School A, submit API request POST /api/v1/classes with Level ID belonging to School B.
2. Inspect response.

**Expected Result:**
> 1. System rejects request with HTTP 400 Bad Request.
> 2. Error message: 'Academic level does not belong to specified school' (ERR_LEVEL_SCHOOL_MISMATCH).
> 3. Zero class records created in database.

---

#### `TC-R3-F04-003`: Verify system blocks duplicate class_code within the same School and Academic Year

- **Scenario ID**: `TS-R3-F04`
- **Test Suite**: Class Management
- **Page / Target**: `Admin Portal > Classes`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Negative`
- **Traceability**: R3 FS v1.1 §3.4 F04-AC11; BR-R3-10
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: TD: Unique compound constraint on (school_id, academic_year, class_code).
- **Note**: Composite unique constraint validation.

**Preconditions:**
```text
Class 'P1-EMERALD' already exists in School 'SCH-RI-01' for Academic Year 2026.
```

**Test Data:**
```text
class_code: 'P1-EMERALD', academic_year: 2026
```

**Test Steps:**
1. Click [Create Class].
2. Enter class_code 'P1-EMERALD' for Academic Year 2026.
3. Click [Save].

**Expected Result:**
> 1. System blocks creation with validation error: 'class_code already exists for this school and academic year' (HTTP 409 Conflict).
> 2. Note: Same class_code in a different Academic Year (e.g. 2027) is permitted.

---

#### `TC-R3-F04-004`: Verify Class deactivation is blocked while active student enrolments exist

- **Scenario ID**: `TS-R3-F04`
- **Test Suite**: Class Management
- **Page / Target**: `Admin Portal > Classes`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `StateTransition`
- **Traceability**: R3 FS v1.1 §3.4 F04; BR-R3-11; Q03
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: WA: Class deactivation guard prevents orphaned active students.
- **Note**: Lifecycle guard: No active students in closed class.

**Preconditions:**
```text
Class 'P1-EMERALD' has 15 active students currently enrolled.
```

**Test Data:**
```text
class_id: 'CLS-P1-EME', target_status: 'INACTIVE'
```

**Test Steps:**
1. Navigate to Class profile for 'P1-EMERALD'.
2. Select status 'INACTIVE' and click [Save].

**Expected Result:**
> 1. System blocks deactivation and displays error: 'Cannot deactivate class with active student enrolments. Transfer students before closing class' (HTTP 422).
> 2. Class remains in status ACTIVE until all enrolments are ended or transferred.

---

#### `TC-R3-F04-005`: Verify Class max_capacity boundary enforcement (30/30) and Bulk Transfer feature upon class merge

- **Scenario ID**: `TS-R3-F04`
- **Test Suite**: Class Management
- **Page / Target**: `Admin Portal > Classes`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `BVA`
- **Traceability**: R3 FS v1.1 §3.4 F04; Q03; BVA
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: WA: max_capacity prevents overcrowding; bulk transfer handles class merges.
- **Note**: BVA boundary testing on class size limit and bulk transition.

**Preconditions:**
```text
Class 'P1-A' has max_capacity = 30 and currently 29 enrolled students. Eligible students STU-30 and STU-31 available.
```

**Test Data:**
```text
ClassId: 'CLS-P1-A', STU-30 (30th student), STU-31 (31st student)
```

**Test Steps:**
1. Enrol student STU-30 into Class 'P1-A'.
2. Inspect class enrolment count (30/30 reached).
3. Attempt to enrol student STU-31 into Class 'P1-A'.
4. Use [Bulk Transfer] to merge Class 'P1-A' into Class 'P1-MERGED' (capacity 40).

**Expected Result:**
> 1. STU-30 enrolled successfully; class count reaches 30/30.
> 2. STU-31 enrolment rejected with error: 'Class capacity limit reached (max 30)' (HTTP 422).
> 3. Bulk Transfer migrates all 30 students to 'P1-MERGED', closes old class enrolments, and keeps student charges intact.

---

#### `TC-R3-F04-006`: Verify rejection of Class creation with invalid/negative max_capacity or blank class_code

- **Scenario ID**: `TS-R3-F04`
- **Test Suite**: Class Management
- **Page / Target**: `Admin Portal > Classes`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Negative`
- **Traceability**: R3 FS v1.1 §3.4 F04; BVA validation
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: TD: Standard boundary check on integer capacity fields.
- **Note**: Defensive schema validation on class sizing.

**Preconditions:**
```text
School User on Create Class screen.
```

**Test Data:**
```text
Invalid data sets: 1) max_capacity = -5; 2) max_capacity = 0; 3) max_capacity = 500; 4) class_code = ' ' (whitespace)
```

**Test Steps:**
1. Submit class with max_capacity = -5.
2. Submit class with max_capacity = 0.
3. Submit class with max_capacity = 500 (exceeds reasonable limit 100).
4. Submit class with blank class_code.

**Expected Result:**
> 1. Negative capacity rejected with HTTP 422 ('Capacity must be positive integer').
> 2. Zero capacity rejected with HTTP 422.
> 3. Capacity > 100 rejected with HTTP 422 ('Max class capacity cannot exceed 100').
> 4. Blank class_code rejected ('class_code is required').

---


### Test Suite: Student Profile Management

#### `TC-R3-F05-001`: Verify creation of Student with valid Singapore NRIC and valid Date of Birth

- **Scenario ID**: `TS-R3-F05`
- **Test Suite**: Student Profile Management
- **Page / Target**: `Admin Portal > Students`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R3 FS v1.1 §3.5 F05-AC12; BR-R3-12; Tender R3 Item 3
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: CR: School maintains student list. TD: student identity verified.
- **Note**: Standard profile creation flow.

**Preconditions:**
```text
School User logged in for School 'SCH-RI-01'. NRIC 'T0812345A' not yet in students table.
```

**Test Data:**
```text
nric: 'T0812345A', full_name: 'Tan Wei Ming', dob: '2008-05-14', citizenship: 'SINGAPORE_CITIZEN', student_category: 'SINGAPORE_CITIZEN'
```

**Test Steps:**
1. Navigate to Student Management.
2. Click [Add Student].
3. Enter valid NRIC 'T0812345A', Name, DOB 2008-05-14, and citizenship 'SINGAPORE_CITIZEN'.
4. Click [Save].

**Expected Result:**
> 1. System displays 'Student created successfully'.
> 2. Student record inserted into students table with status = 'ACTIVE' and unique student_id.
> 3. Student is ready for class enrolment.

---

#### `TC-R3-F05-002`: Verify system rejects duplicate Student national identifier (NRIC/FIN)

- **Scenario ID**: `TS-R3-F05`
- **Test Suite**: Student Profile Management
- **Page / Target**: `Admin Portal > Students`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Negative`
- **Traceability**: R3 FS v1.1 §3.5 F05-AC13; BR-R3-12
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: TD: Unique index on students(nric_hash/identifier).
- **Note**: Prevents ghost accounts and duplicate student profiles.

**Preconditions:**
```text
Student with NRIC 'T0812345A' already exists in the system.
```

**Test Data:**
```text
nric: 'T0812345A', full_name: 'Duplicate Student Name'
```

**Test Steps:**
1. Click [Add Student].
2. Enter duplicate NRIC 'T0812345A' with different name.
3. Click [Save].

**Expected Result:**
> 1. System blocks creation with validation error: 'National identifier (NRIC/FIN) already exists' (HTTP 409 Conflict).
> 2. No duplicate record is created in database (BR-R3-12).

---

#### `TC-R3-F05-003`: Verify Student with existing enrolments or Student Charges cannot be deleted (Deactivation only)

- **Scenario ID**: `TS-R3-F05`
- **Test Suite**: Student Profile Management
- **Page / Target**: `Admin Portal > Students`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Integrity`
- **Traceability**: R3 FS v1.1 §3.5 F05-AC14; BR-R3-15
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: TD: Foreign key constraint on student_charges.student_id.
- **Note**: Financial audit trail protection.

**Preconditions:**
```text
Student 'STU-001' has historical enrolment in 2025 and 2 outstanding Student Charges.
```

**Test Data:**
```text
student_id: 'STU-001'
```

**Test Steps:**
1. Send DELETE /api/v1/students/STU-001.
2. Verify response status and error body.
3. Send PATCH /api/v1/students/STU-001 with is_active = false.

**Expected Result:**
> 1. Hard DELETE rejected with HTTP 409 Conflict ('Cannot delete student with historical enrolments or charges').
> 2. Soft-deactivation (PATCH) succeeds; historical student ledger preserved intact.

---

#### `TC-R3-F05-004`: Verify Singapore Checksum Modulo 11 validation on NRIC / FIN identifiers

- **Scenario ID**: `TS-R3-F05`
- **Test Suite**: Student Profile Management
- **Page / Target**: `Admin Portal > Students`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Security`
- **Traceability**: R3 FS v1.1 §3.5 F05; Q07; GovTech IM8
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: WA: GovTech IM8 & Singapore National Identity checksum standard.
- **Note**: Algorithmic validation for Singapore identity documents.

**Preconditions:**
```text
School User on Add Student screen.
```

**Test Data:**
```text
Valid NRIC: 'S9823456D', 'T0512345J'. Corrupt Checksum NRIC: 'T0512345Z'. Invalid format: '1234567', 'T123456789'.
```

**Test Steps:**
1. Submit student with valid NRIC 'S9823456D'.
2. Submit student with corrupt checksum NRIC 'T0512345Z'.
3. Submit student with ill-formatted NRIC.

**Expected Result:**
> 1. Valid NRIC passes Modulo 11 checksum algorithm and is accepted.
> 2. Corrupt checksum is rejected with error: 'Invalid Singapore NRIC checksum' (HTTP 422).
> 3. Ill-formatted NRIC rejected with format error (HTTP 422).

---

#### `TC-R3-F05-005`: Verify Data Masking of NRIC/FIN on Admin Portal UI according to PDPA / IM8 guidelines

- **Scenario ID**: `TS-R3-F05`
- **Test Suite**: Student Profile Management
- **Page / Target**: `Admin Portal > Student Roster`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Security`
- **Traceability**: R3 FS v1.1 §3.5 F05; Q07; PDPA Compliance
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: WA: PDPA & GovTech IM8 Data Masking mandates protecting national ID.
- **Note**: PDPA privacy compliance verification.

**Preconditions:**
```text
Student with NRIC 'T0812345A' exists in the database.
```

**Test Data:**
```text
Stored NRIC: 'T0812345A'
```

**Test Steps:**
1. Navigate to Student Roster / Search screen as standard School User.
2. Inspect displayed NRIC column on screen.
3. Inspect HTTP API response JSON in browser DevTools network tab.

**Expected Result:**
> 1. UI renders masked NRIC: 'T****345A' (first letter + 4 asterisks + last 4 characters).
> 2. Full NRIC is not exposed in default search API payload; only unmasked via explicit 'View Full Profile' audit-logged action.

---

#### `TC-R3-F05-006`: Verify Student Category adheres strictly to 4 MOE Singapore Tiers

- **Scenario ID**: `TS-R3-F05`
- **Test Suite**: Student Profile Management
- **Page / Target**: `Admin Portal > Students`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `DecisionTable`
- **Traceability**: R3 FS v1.1 §3.5 F05; §3.11 F11; Q08; BR-R3-13
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: WA: 4 official MOE Singapore residency tiers determine school fees.
- **Note**: Essential tiering for fee calculations.

**Preconditions:**
```text
School User creating student profiles.
```

**Test Data:**
```text
4 valid tiers: ['SINGAPORE_CITIZEN', 'PERMANENT_RESIDENT', 'INTERNATIONAL_STUDENT_ASEAN', 'INTERNATIONAL_STUDENT_NON_ASEAN']. Invalid: 'EXPAT_GUEST'.
```

**Test Steps:**
1. Submit student profiles for each of the 4 valid MOE tiers.
2. Submit student with invalid tier 'EXPAT_GUEST'.

**Expected Result:**
> 1. All 4 standard tiers are accepted and persisted.
> 2. Invalid tier rejected with validation error (HTTP 422).
> 3. Stored tier accurately drives downstream Fee Rate Rule matching.

---

#### `TC-R3-F05-007`: Verify Student status transitions to WITHDRAWN upon official student withdrawal

- **Scenario ID**: `TS-R3-F05`
- **Test Suite**: Student Profile Management
- **Page / Target**: `Admin Portal > Students`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `StateTransition`
- **Traceability**: R3 FS v1.1 §3.5 F05; BR-R3-15; Q06
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: WA: WITHDRAWN status lifecycle prevents billing retired students.
- **Note**: Student lifecycle transition audit.

**Preconditions:**
```text
Student 'STU-WD-01' is actively enrolled in Class 'P1-A'.
```

**Test Data:**
```text
withdrawal_date: '2026-06-30', reason: 'Emigrated overseas'
```

**Test Steps:**
1. Open student profile.
2. Select action [Process Withdrawal].
3. Enter withdrawal_date and reason.
4. Click [Confirm].

**Expected Result:**
> 1. Student status transitions to 'WITHDRAWN'.
> 2. Current class enrolment is automatically ended with end_date = withdrawal_date.
> 3. Student is excluded from subsequent Fee Publication recipient resolutions (F14).

---

#### `TC-R3-F05-008`: Verify School User cannot alter Student citizenship/category; restricted to MOE HQ with audit log

- **Scenario ID**: `TS-R3-F05`
- **Test Suite**: Student Profile Management
- **Page / Target**: `Admin Portal > Students`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Security`
- **Traceability**: R3 FS v1.1 §3.5 F05; BR-R3-14; Q08
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: WA: Fraud prevention: Residency changes restricted to HQ with ICA verification.
- **Note**: Prevents fee evasion by illicit citizenship changes.

**Preconditions:**
```text
Student 'STU-001' has category = 'PERMANENT_RESIDENT'. User A is School User; User B is MOE HQ Admin.
```

**Test Data:**
```text
new_category: 'SINGAPORE_CITIZEN', supporting_doc: 'ICA-CIT-9921'
```

**Test Steps:**
1. As School User, attempt to change student_category to 'SINGAPORE_CITIZEN'.
2. As MOE HQ Admin, perform the update with supporting_doc reference.

**Expected Result:**
> 1. School User update attempt is rejected with HTTP 403 Forbidden ('Only MOE HQ can alter student citizenship').
> 2. MOE HQ Admin update succeeds; audit log records previous value, new value, actor, and ICA doc reference.

---

#### `TC-R3-F05-009`: Verify Batch upload of student roster via CSV/Excel template with row-level error validation

- **Scenario ID**: `TS-R3-F05`
- **Test Suite**: Student Profile Management
- **Page / Target**: `Admin Portal > Students > Batch Upload`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R3 FS v1.1 §1.4 WA-R3-02; §3.5 F05; Q02
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: WA: Bulk roster upload required at beginning of academic year.
- **Note**: Bulk onboarding operational efficiency.

**Preconditions:**
```text
School User on Batch Upload screen. CSV file contains 10 rows: 8 valid students, 1 duplicate NRIC, 1 invalid DOB.
```

**Test Data:**
```text
File: 'student_roster_upload.csv' (10 records)
```

**Test Steps:**
1. Upload 'student_roster_upload.csv'.
2. Click [Validate and Import].
3. Review import summary report.

**Expected Result:**
> 1. System parses file in a single transactional batch.
> 2. Valid 8 students imported with status ACTIVE.
> 3. Failed 2 rows flagged with exact row numbers and errors ('Row 4: Duplicate NRIC', 'Row 7: Invalid DOB').
> 4. Option provided to download error report CSV.

---


### Test Suite: Student Enrolment

#### `TC-R3-F06-001`: Verify assigning Student to active Class creates active enrolment with start_date

- **Scenario ID**: `TS-R3-F06`
- **Test Suite**: Student Enrolment
- **Page / Target**: `Admin Portal > Enrolment`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R3 FS v1.1 §3.6 F06-AC15; BR-R3-16; Tender R3 Item 3
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: CR: Enrolment binds student to class and academic year.
- **Note**: Core enrolment association.

**Preconditions:**
```text
Student 'STU-001' has no active enrolment for Academic Year 2026. Class 'P1-A' is ACTIVE.
```

**Test Data:**
```text
student_id: 'STU-001', class_id: 'CLS-P1-A', academic_year: 2026, start_date: '2026-01-02'
```

**Test Steps:**
1. Navigate to Class 'P1-A'.
2. Click [Add Student].
3. Select 'STU-001', set start_date '2026-01-02'.
4. Click [Enrol].

**Expected Result:**
> 1. System displays 'Student enrolled successfully'.
> 2. Record created in enrolments table with status = 'ACTIVE', start_date = '2026-01-02', end_date = null.
> 3. Class student count increments by 1.

---

#### `TC-R3-F06-002`: Verify system prevents enrolling Student into multiple active classes in the same Academic Year

- **Scenario ID**: `TS-R3-F06`
- **Test Suite**: Student Enrolment
- **Page / Target**: `Admin Portal > Enrolment`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Negative`
- **Traceability**: R3 FS v1.1 §3.6 F06-AC16; BR-R3-17
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: TD: Unique index on (student_id, academic_year) WHERE end_date IS NULL.
- **Note**: Enforces single active enrolment invariant.

**Preconditions:**
```text
Student 'STU-001' already has an active enrolment in Class 'P1-A' for Academic Year 2026.
```

**Test Data:**
```text
target_class: 'P1-B' (same school, same year 2026)
```

**Test Steps:**
1. Attempt to enrol 'STU-001' into Class 'P1-B' without closing enrolment in 'P1-A'.
2. Inspect response.

**Expected Result:**
> 1. System rejects enrolment with error: 'Student already has an active enrolment for Academic Year 2026' (HTTP 409 Conflict).
> 2. No secondary active enrolment created (BR-R3-17).

---

#### `TC-R3-F06-003`: Verify system rejects assigning Student to Class belonging to a different School

- **Scenario ID**: `TS-R3-F06`
- **Test Suite**: Student Enrolment
- **Page / Target**: `Admin Portal > Enrolment`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Integrity`
- **Traceability**: R3 FS v1.1 §3.6 F06-AC17; BR-R3-18
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: TD: School tenant boundary check on enrolment.
- **Note**: Multi-tenant integrity check.

**Preconditions:**
```text
Student belongs to School 'SCH-RI-01'. Class 'CLS-HCI-01' belongs to School 'SCH-HCI-02'.
```

**Test Data:**
```text
student_id: 'STU-RI-01', class_id: 'CLS-HCI-01'
```

**Test Steps:**
1. Submit enrolment request pairing Student from School A with Class of School B.
2. Inspect validation response.

**Expected Result:**
> 1. System blocks submission with error: 'Student cannot be enrolled in a class of a different school' (HTTP 400 Bad Request).
> 2. Cross-school enrolment prevented (BR-R3-18).

---

#### `TC-R3-F06-004`: Verify assigning Singaporean Student to Class automatically initiates F08 Education Account linkage

- **Scenario ID**: `TS-R3-F06`
- **Test Suite**: Student Enrolment
- **Page / Target**: `Admin Portal > Enrolment`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: R3 FS v1.1 §3.6 F06; BR-R3-20; §3.8 F08-AC21; Tender R3 Item 3
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: CR: Singaporean enrolment triggers Edusave link.
- **Note**: Integration seam between School Roster and Edusave Account.

**Preconditions:**
```text
Student 'STU-SC-01' has citizenship = 'SINGAPORE_CITIZEN'. Education Account exists in R1.
```

**Test Data:**
```text
student_id: 'STU-SC-01', class_id: 'CLS-P1-A'
```

**Test Steps:**
1. Complete enrolment of 'STU-SC-01' into Class 'P1-A'.
2. Inspect background event dispatch or database linkage table.

**Expected Result:**
> 1. Enrolment is created successfully.
> 2. System automatically triggers F08: Education Account is linked to student record (BR-R3-20).
> 3. Flag has_education_account set to true.

---


### Test Suite: Student Transfer

#### `TC-R3-F07-001`: Verify Student Transfer closes old enrolment (end_date) and creates new enrolment in target School/Class

- **Scenario ID**: `TS-R3-F07`
- **Test Suite**: Student Transfer
- **Page / Target**: `Admin Portal > Student Transfer`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R3 FS v1.1 §3.7 F07-AC18; BR-R3-21; BR-R3-22
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: CR: HQ performs cross-school transfer. TD: Sequential date chaining.
- **Note**: Core transfer transition.

**Preconditions:**
```text
Student 'STU-001' is enrolled in School A ('SCH-RI-01'), Class 'P1-A'. MOE HQ User logged in.
```

**Test Data:**
```text
target_school: 'SCH-HCI-02', target_class: 'P1-HONOR', effective_date: '2026-07-01'
```

**Test Steps:**
1. HQ User opens Student Transfer module.
2. Select 'STU-001', select target School B and Class 'P1-HONOR'.
3. Set effective_date '2026-07-01' and submit.

**Expected Result:**
> 1. Old enrolment in School A updated with end_date = '2026-06-30' and status = 'TRANSFERRED_OUT'.
> 2. New enrolment created in School B with start_date = '2026-07-01' and status = 'ACTIVE'.
> 3. Student appears on School B roster and disappears from active roster of School A.

---

#### `TC-R3-F07-002`: Verify historical Student Charges at previous school remain attached to previous school

- **Scenario ID**: `TS-R3-F07`
- **Test Suite**: Student Transfer
- **Page / Target**: `Admin Portal > Student Transfer`
- **Severity / Priority**: `S1` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Integrity`
- **Traceability**: R3 FS v1.1 §3.7 F07-AC19; BR-R3-23; Q10; Tender R3 Item 3
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: WA: Debt remains at originating school; no automatic transfer of liability.
- **Note**: Critical accounting integrity: Prevents inter-school ledger leakage.

**Preconditions:**
```text
Student transferred from School A to School B. Prior to transfer, School A issued Student Charge 'CHG-SCHA-001' ($50.00 SGD, UNPAID).
```

**Test Data:**
```text
charge_id: 'CHG-SCHA-001', school_a: 'SCH-RI-01', school_b: 'SCH-HCI-02'
```

**Test Steps:**
1. Execute transfer of student from School A to School B.
2. Query database for 'CHG-SCHA-001'.
3. Check outstanding charges visible to School A Finance User vs School B Finance User.

**Expected Result:**
> 1. Charge 'CHG-SCHA-001' remains attached to School A (school_id does not change to School B).
> 2. Charge status remains UNPAID and owed to School A.
> 3. School B cannot modify or collect School A charge; parent sees debt owed to School A on portal.

---

#### `TC-R3-F07-003`: Verify full audit log recorded for Student Transfer (actor, timestamp, old and new school/class)

- **Scenario ID**: `TS-R3-F07`
- **Test Suite**: Student Transfer
- **Page / Target**: `Admin Portal > Student Transfer > Audit Log`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Audit`
- **Traceability**: R3 FS v1.1 §3.7 F07-AC20; BR-R3-24
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: TD: Comprehensive audit trail for student movements.
- **Note**: Compliance and dispute resolution evidence.

**Preconditions:**
```text
HQ User 'hq.admin01@moe.gov.sg' transfers student 'STU-001'.
```

**Test Data:**
```text
transfer_reason: 'Family relocated to Bukit Timah', reference_doc: 'MOE-TRF-2026-992'
```

**Test Steps:**
1. Submit transfer request with transfer_reason and reference_doc.
2. Query student_transfer_audit table.

**Expected Result:**
> 1. Audit record persisted containing: student_id, from_school_id, to_school_id, from_class_id, to_class_id, effective_date, created_by ('hq.admin01@moe.gov.sg'), and UTC timestamp.
> 2. Record is immutable (no UPDATE/DELETE allowed on audit table).

---

#### `TC-R3-F07-004`: Verify Proration calculation for mid-month school transfer fees

- **Scenario ID**: `TS-R3-F07`
- **Test Suite**: Student Transfer
- **Page / Target**: `Admin Portal > Fee Calculation`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `BVA`
- **Traceability**: R3 FS v1.1 §3.7 F07; BR-R3-25; Q10
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: WA: Proration formula applies daily rate for mid-month school transfer.
- **Note**: Fair billing during mid-cycle transfers.

**Preconditions:**
```text
Monthly miscellaneous fee is $30.00 SGD for 30-day month (June). Student transfers on June 16 (active 15 days in School A, 15 days in School B).
```

**Test Data:**
```text
full_fee: 30.00 SGD, days_in_school_a: 15, days_in_month: 30
```

**Test Steps:**
1. Trigger fee calculation for transfer student in June.
2. Inspect proration formula: (15 / 30) * $30.00.

**Expected Result:**
> 1. School A issues prorated charge of $15.00 SGD.
> 2. School B issues prorated charge for remaining 15 days ($15.00 SGD).
> 3. Total charged to parent equals standard monthly fee ($30.00 SGD).

---


### Test Suite: Education Account Linkage

#### `TC-R3-F08-001`: Verify Singaporean Citizen student is automatically linked to Education Account created by R1

- **Scenario ID**: `TS-R3-F08`
- **Test Suite**: Education Account Linkage
- **Page / Target**: `Admin Portal > Students`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: R3 FS v1.1 §3.8 F08-AC21; BR-R3-26; BR-R3-27; Tender R3 Item 3
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: CR: Singaporean student automatically linked to Edusave.
- **Note**: Core prerequisite for Edusave fee deduction.

**Preconditions:**
```text
Student 'STU-SC-01' is Singapore Citizen. Edusave account exists in education_accounts table.
```

**Test Data:**
```text
student_id: 'STU-SC-01', citizenship: 'SINGAPORE_CITIZEN'
```

**Test Steps:**
1. Enrol student into active class.
2. Query student_education_accounts linkage table.
3. Verify account balance and status.

**Expected Result:**
> 1. System establishes linkage between student_id and account_id.
> 2. Linkage status = 'LINKED', verified_at = current timestamp.
> 3. Student is marked eligible to pay school fees using Edusave balance.

---

#### `TC-R3-F08-002`: Verify non-Singaporean student (PR, IS) does not receive Education Account linkage

- **Scenario ID**: `TS-R3-F08`
- **Test Suite**: Education Account Linkage
- **Page / Target**: `Admin Portal > Students`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R3 FS v1.1 §3.8 F08-AC22; BR-R3-28; Tender R3 Item 3
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: CR: Edusave strictly reserved for Singapore Citizens by law.
- **Note**: Statutory eligibility guard.

**Preconditions:**
```text
Student 'STU-PR-01' is Permanent Resident; Student 'STU-IS-01' is International Student.
```

**Test Data:**
```text
citizenship: ['PERMANENT_RESIDENT', 'INTERNATIONAL_STUDENT_ASEAN']
```

**Test Steps:**
1. Enrol both students into active classes.
2. Inspect student_education_accounts table.

**Expected Result:**
> 1. No Education Account record is linked for either student (count = 0).
> 2. Both students are ineligible for Edusave payment; must pay via online payment methods in R9.

---

#### `TC-R3-F08-003`: Verify Idempotency: System prevents creating duplicate Education Account linkages for same student

- **Scenario ID**: `TS-R3-F08`
- **Test Suite**: Education Account Linkage
- **Page / Target**: `Admin Portal > Students`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Integrity`
- **Traceability**: R3 FS v1.1 §3.8 F08-AC23; BR-R3-29
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: TD: Unique constraint on (student_id, education_account_id).
- **Note**: Idempotent linkage execution.

**Preconditions:**
```text
Student 'STU-SC-01' already linked to Education Account 'EA-9901'.
```

**Test Data:**
```text
student_id: 'STU-SC-01', account_id: 'EA-9901'
```

**Test Steps:**
1. Re-trigger F08 linkage process (e.g. during class transfer or re-enrolment).
2. Query database linkage table count.

**Expected Result:**
> 1. System recognizes existing active link.
> 2. No secondary linkage record created (database count remains exactly 1).
> 3. Operation returns idempotent success (HTTP 200 OK).

---

#### `TC-R3-F08-004`: Verify student turning 16 boundary: Edusave closed, account linkage transitions to PSEA / payment blocked

- **Scenario ID**: `TS-R3-F08`
- **Test Suite**: Education Account Linkage
- **Page / Target**: `Admin Portal > Students`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `BVA`
- **Traceability**: R3 FS v1.1 §3.8 F08; BR-R3-30; Q11; R1 Boundary
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: WA: Age 16 boundary closes Edusave per Singapore statute.
- **Note**: Lifecycle boundary between Edusave and PSEA.

**Preconditions:**
```text
Student turns 16 on 2026-10-15. Service clock advanced to 2026-10-16. Account status in R1 updated to 'CLOSED_AGE_16'.
```

**Test Data:**
```text
student_dob: '2010-10-15', current_date: '2026-10-16'
```

**Test Steps:**
1. School issues fee charge for secondary level student.
2. System checks Edusave payment eligibility for this student.
3. Attempt to select Edusave payment on e-Service portal.

**Expected Result:**
> 1. System detects Edusave account is CLOSED.
> 2. Edusave payment option is disabled / blocked with message: 'Edusave account closed upon turning 16; remaining funds transferred to PSEA'.
> 3. Parent must pay via credit card / PayNow.

---

#### `TC-R3-F08-005`: Verify Student gaining Singapore Citizenship mid-year triggers automatic Education Account creation & linkage

- **Scenario ID**: `TS-R3-F08`
- **Test Suite**: Education Account Linkage
- **Page / Target**: `Admin Portal > Students`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: R3 FS v1.1 §3.8 F08; BR-R3-26; Q11
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: WA: Event-driven citizenship change auto-provisions and links Edusave.
- **Note**: Event-driven asynchronous lifecycle integration.

**Preconditions:**
```text
Student 'STU-PR-02' currently PR without Education Account. MOE HQ updates citizenship to 'SINGAPORE_CITIZEN' with ICA approval.
```

**Test Data:**
```text
student_id: 'STU-PR-02', new_citizenship: 'SINGAPORE_CITIZEN', effective_date: '2026-08-01'
```

**Test Steps:**
1. MOE HQ updates student citizenship to 'SINGAPORE_CITIZEN'.
2. Inspect event bus / listener for 'CITIZENSHIP_UPDATED'.
3. Check R1 account creation and R3 F08 linkage.

**Expected Result:**
> 1. Citizenship update event successfully triggers R1 account creation.
> 2. F08 automatically establishes Education Account linkage in R3.
> 3. Starting from August 1, student becomes eligible for Edusave fee deduction.

---


### Test Suite: Fee Type Catalog

#### `TC-R3-F09-001`: Verify creation of Fee Type with unique fee_type_code

- **Scenario ID**: `TS-R3-F09`
- **Test Suite**: Fee Type Catalog
- **Page / Target**: `Admin Portal > Fee Types`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R3 FS v1.1 §3.9 F09-AC24; BR-R3-31; Tender R3 Item 3
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: CR: High-level classification of fees. TD: unique code constraint.
- **Note**: Fee taxonomy setup.

**Preconditions:**
```text
MOE HQ User on Fee Types setup screen. fee_type_code 'MISC_FEE' does not exist.
```

**Test Data:**
```text
fee_type_code: 'MISC_FEE', name: 'Standard Miscellaneous Fees', description: 'National standard school miscellaneous fees'
```

**Test Steps:**
1. Click [Add Fee Type].
2. Enter code 'MISC_FEE', Name, and Description.
3. Click [Save].

**Expected Result:**
> 1. System displays 'Fee Type created successfully'.
> 2. Record created in fee_types table with code 'MISC_FEE', is_active = true.
> 3. Fee Type appears in parent dropdown when configuring Fee Components (F10).

---

#### `TC-R3-F09-002`: Verify system rejects Fee Type with duplicate fee_type_code

- **Scenario ID**: `TS-R3-F09`
- **Test Suite**: Fee Type Catalog
- **Page / Target**: `Admin Portal > Fee Types`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Negative`
- **Traceability**: R3 FS v1.1 §3.9 F09-AC25; BR-R3-31
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: TD: Unique index on fee_types(fee_type_code).
- **Note**: Uniqueness constraint on fee type codes.

**Preconditions:**
```text
Fee Type 'MISC_FEE' already exists in fee_types table.
```

**Test Data:**
```text
fee_type_code: 'MISC_FEE', name: 'Duplicate Miscellaneous'
```

**Test Steps:**
1. Click [Add Fee Type].
2. Enter existing code 'MISC_FEE'.
3. Click [Save].

**Expected Result:**
> 1. System blocks submission with error: 'fee_type_code already exists' (HTTP 409 Conflict).
> 2. No duplicate row inserted (BR-R3-31).

---

#### `TC-R3-F09-003`: Verify system assigns is_active = true by default upon Fee Type creation

- **Scenario ID**: `TS-R3-F09`
- **Test Suite**: Fee Type Catalog
- **Page / Target**: `Admin Portal > Fee Types`
- **Severity / Priority**: `S4` / `Low`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R3 FS v1.1 §3.9 F09-AC26; BR-R3-32
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: TD: Schema default value BIT DEFAULT 1.
- **Note**: Verifies default boolean configuration.

**Preconditions:**
```text
MOE HQ User creates new Fee Type without specifying is_active flag explicitly.
```

**Test Data:**
```text
fee_type_code: 'AUTO_FEE', name: 'Autonomous School Fee'
```

**Test Steps:**
1. Submit POST /api/v1/fee-types omitting is_active field.
2. Query database for inserted record.

**Expected Result:**
> 1. Record created successfully (HTTP 201).
> 2. Database column is_active is set to true (1) by default (BR-R3-32).
> 3. Status displayed as 'Active' on UI.

---

#### `TC-R3-F09-004`: Verify Standard vs Autonomous Fee Types: MOE HQ catalog vs School-specific ownership

- **Scenario ID**: `TS-R3-F09`
- **Test Suite**: Fee Type Catalog
- **Page / Target**: `Admin Portal > Fee Types`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Security`
- **Traceability**: R3 FS v1.1 §3.9 F09; BR-R3-33; Q12
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: WA: MOE controls national fee framework; autonomous schools manage custom fees.
- **Note**: Ownership scope of fee types.

**Preconditions:**
```text
MOE HQ defines Standard Fee Types. School User of Autonomous school attempts to configure school-specific fee type.
```

**Test Data:**
```text
Standard: 'STD_MISC_FEE' (HQ owned). School-specific: 'RI_BOARDING_FEE' (School owned).
```

**Test Steps:**
1. Verify Standard Fee Types are centrally visible to all schools.
2. School User creates school-specific Fee Type 'RI_BOARDING_FEE' with owner_school_id = 'SCH-RI-01'.
3. Verify School B cannot see or use 'RI_BOARDING_FEE'.

**Expected Result:**
> 1. HQ fee types are shared nationwide.
> 2. School-specific fee types are strictly scoped to the creating school.
> 3. Cross-tenant fee type leakage is prevented.

---


### Test Suite: Fee Component Catalog

#### `TC-R3-F10-001`: Verify creation of Fee Component linked to valid parent Fee Type with unique code

- **Scenario ID**: `TS-R3-F10`
- **Test Suite**: Fee Component Catalog
- **Page / Target**: `Admin Portal > Fee Components`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R3 FS v1.1 §3.10 F10-AC27; BR-R3-35; BR-R3-36; Tender R3 Item 3
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: CR: Fee components represent specific chargeable items. TD: Foreign key to fee_types.
- **Note**: Foundational fee item setup.

**Preconditions:**
```text
Fee Type 'MISC_FEE' exists and is ACTIVE. component_code 'FC-STD-MISC-01' does not exist.
```

**Test Data:**
```text
fee_type_id: 'FT-MISC', component_code: 'FC-STD-MISC-01', name: 'Standard Miscellaneous Fee', is_taxable: false, allow_edusave: true
```

**Test Steps:**
1. Navigate to Fee Components.
2. Click [Add Component].
3. Select Fee Type 'MISC_FEE', enter code 'FC-STD-MISC-01', name, and flags.
4. Click [Save].

**Expected Result:**
> 1. System displays 'Fee Component created successfully'.
> 2. Record created in fee_components table with status ACTIVE.
> 3. Component available for Fee Rate Rule pricing (F11) and Fee Publication (F12).

---

#### `TC-R3-F10-002`: Verify system rejects Fee Component creation if parent Fee Type does not exist or is inactive

- **Scenario ID**: `TS-R3-F10`
- **Test Suite**: Fee Component Catalog
- **Page / Target**: `Admin Portal > Fee Components`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Negative`
- **Traceability**: R3 FS v1.1 §3.10 F10-AC28; BR-R3-35
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: TD: Foreign key constraint and active parent validation.
- **Note**: Relational integrity protection.

**Preconditions:**
```text
Fee Type 'FT-NONEXISTENT' does not exist; Fee Type 'FT-DEACTIVATED' has is_active = false.
```

**Test Data:**
```text
component_code: 'FC-ORPHAN-01'
```

**Test Steps:**
1. Submit POST /api/v1/fee-components with fee_type_id = 'FT-NONEXISTENT'.
2. Submit POST /api/v1/fee-components with fee_type_id = 'FT-DEACTIVATED'.

**Expected Result:**
> 1. Nonexistent fee_type_id returns HTTP 400 Bad Request ('Referenced Fee Type does not exist').
> 2. Deactivated fee_type_id returns HTTP 422 Unprocessable Entity ('Cannot create component under inactive Fee Type').
> 3. Zero records inserted into fee_components.

---

#### `TC-R3-F10-003`: Verify system assigns is_apply_tax = true by default upon Fee Component creation

- **Scenario ID**: `TS-R3-F10`
- **Test Suite**: Fee Component Catalog
- **Page / Target**: `Admin Portal > Fee Components`
- **Severity / Priority**: `S4` / `Low`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R3 FS v1.1 §3.10 F10-AC29; BR-R3-37
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: TD: Schema default value BIT DEFAULT 1.
- **Note**: Default tax applicability verification.

**Preconditions:**
```text
User creates Fee Component without explicitly passing is_apply_tax field.
```

**Test Data:**
```text
component_code: 'FC-DEF-TAX-01', name: 'Default Tax Component'
```

**Test Steps:**
1. Submit POST /api/v1/fee-components omitting is_apply_tax.
2. Query database for inserted component.

**Expected Result:**
> 1. Component created successfully (HTTP 201).
> 2. Column is_apply_tax is set to true (1) by default in fee_components table (BR-R3-37).

---

#### `TC-R3-F10-004`: Verify owner_school_id references valid School ID or MOE HQ ID, not arbitrary user ID

- **Scenario ID**: `TS-R3-F10`
- **Test Suite**: Fee Component Catalog
- **Page / Target**: `Admin Portal > Fee Components`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Integrity`
- **Traceability**: R3 FS v1.1 §3.10 F10; BR-R3-38; Q12
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: WA: Fee Component ownership belongs to School or MOE HQ, not individual persons.
- **Note**: Corrects schema ambiguity: Fees belong to institutions, not individuals.

**Preconditions:**
```text
User attempts to configure fee component with an individual user_id as owner instead of institutional entity.
```

**Test Data:**
```text
Invalid owner: user_id 'USR-101'. Valid owner: school_id 'SCH-RI-01' or 'MOE-HQ-CENTRAL'.
```

**Test Steps:**
1. Submit component creation with owner_id referencing a user UUID.
2. Submit component creation with owner_school_id = 'SCH-RI-01'.

**Expected Result:**
> 1. User UUID rejected with HTTP 400 Bad Request ('Fee Component owner must be School or MOE HQ entity').
> 2. School ID accepted; component correctly owned by the school institution (BR-R3-38).

---

#### `TC-R3-F10-005`: Verify allow_edusave_payment flag governs Education Account payment eligibility

- **Scenario ID**: `TS-R3-F10`
- **Test Suite**: Fee Component Catalog
- **Page / Target**: `Admin Portal > Fee Components`
- **Severity / Priority**: `S1` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R3 FS v1.1 §3.10 F10; BR-R3-39; §4 Payment Rule; Tender R3 Item 3
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: CR: Only approved fee components can be deducted from Edusave per MOE statutory policy.
- **Note**: Critical compliance guard: Prevents unauthorized Edusave usage.

**Preconditions:**
```text
Component A ('FC-STD-MISC') has allow_edusave_payment = true. Component B ('FC-OPT-CAMP') has allow_edusave_payment = false.
```

**Test Data:**
```text
Components A and B published to Singaporean student STU-SC-01.
```

**Test Steps:**
1. Issue charges for Component A and Component B.
2. Check Edusave payment eligibility for Charge A.
3. Check Edusave payment eligibility for Charge B.

**Expected Result:**
> 1. Charge A (allow_edusave_payment = true) is flagged is_edusave_eligible = true; Edusave deduction allowed.
> 2. Charge B (allow_edusave_payment = false) is flagged is_edusave_eligible = false; Edusave deduction strictly blocked on portal.

---

#### `TC-R3-F10-006`: Verify Fee Component with is_taxable = true applies Singapore GST (9%) correctly

- **Scenario ID**: `TS-R3-F10`
- **Test Suite**: Fee Component Catalog
- **Page / Target**: `Admin Portal > Fee Components`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Calculation`
- **Traceability**: R3 FS v1.1 §3.10 F10; §3.15 F15; BR-R3-40; Q13
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: WA: Singapore GST (9%) applied on taxable fee components.
- **Note**: Statutory tax calculation.

**Preconditions:**
```text
Component 'FC-TAX-CAMP' configured with is_taxable = true. Current GST rate is 9.0%.
```

**Test Data:**
```text
base_amount: 100.00 SGD, gst_rate: 9.0%
```

**Test Steps:**
1. Publish fee of $100.00 SGD for Component 'FC-TAX-CAMP'.
2. Inspect generated Student Charge tax_amount and total_amount.

**Expected Result:**
> 1. System calculates tax_amount = $9.00 SGD ($100.00 * 9%).
> 2. Total charge amount = $109.00 SGD ($100.00 base + $9.00 tax).
> 3. Both base_amount and tax_amount stored distinctly in student_charges table.

---


### Test Suite: Fee Pricing Engine

#### `TC-R3-F11-001`: Verify creation of Fee Rate Rule with positive price_amount and valid date range

- **Scenario ID**: `TS-R3-F11`
- **Test Suite**: Fee Pricing Engine
- **Page / Target**: `Admin Portal > Fee Rates`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R3 FS v1.1 §3.11 F11-AC30; BR-R3-41; Tender R3 Item 3
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: CR: Rate rules define pricing per category/level. TD: Date range bounded.
- **Note**: Standard rate rule configuration.

**Preconditions:**
```text
Fee Component 'FC-STD-MISC' exists and is ACTIVE.
```

**Test Data:**
```text
component_id: 'FC-STD-MISC', student_category: 'SINGAPORE_CITIZEN', level_id: 'LVL-PRI-1', price_amount: 13.00, start_date: '2026-01-01', end_date: '2026-12-31'
```

**Test Steps:**
1. Navigate to Fee Rate Rules.
2. Click [Add Rate Rule].
3. Select Component, Category 'SINGAPORE_CITIZEN', Level 'Primary 1', enter price 13.00 SGD and date range.
4. Click [Save].

**Expected Result:**
> 1. System displays 'Fee Rate Rule created successfully'.
> 2. Record persisted in fee_rate_rules table with price_amount = 13.00, status ACTIVE.
> 3. Rule is available for fee pricing evaluation.

---

#### `TC-R3-F11-002`: Verify Academic Level set to null in rate rule applies as wildcard across all levels

- **Scenario ID**: `TS-R3-F11`
- **Test Suite**: Fee Pricing Engine
- **Page / Target**: `Admin Portal > Fee Rates`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R3 FS v1.1 §3.11 F11-AC31; BR-R3-42
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: CR: Level null in rate rule applies across all levels.
- **Note**: Wildcard level matching test.

**Preconditions:**
```text
Fee Component 'FC-AUTONOMOUS' has rate rule with level_id = null and student_category = 'SINGAPORE_CITIZEN', price = $25.00 SGD.
```

**Test Data:**
```text
Students enrolled across different levels: Primary 1, Primary 4, Primary 6.
```

**Test Steps:**
1. Evaluate price for Student in Primary 1.
2. Evaluate price for Student in Primary 4.
3. Evaluate price for Student in Primary 6.

**Expected Result:**
> 1. Primary 1 student resolves to $25.00 SGD.
> 2. Primary 4 student resolves to $25.00 SGD.
> 3. Primary 6 student resolves to $25.00 SGD.
> 4. Level null functions correctly as a wildcard covering all academic levels (BR-R3-42).

---

#### `TC-R3-F11-003`: Verify rate rule evaluation matches strictly on student_category (SC vs PR vs IS)

- **Scenario ID**: `TS-R3-F11`
- **Test Suite**: Fee Pricing Engine
- **Page / Target**: `Admin Portal > Fee Rates`
- **Severity / Priority**: `S1` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `DecisionTable`
- **Traceability**: R3 FS v1.1 §3.11 F11-AC32; BR-R3-43; Tender R3 Item 3
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: CR: Pricing determined by student residency tier.
- **Note**: Decision table testing across residency tiers.

**Preconditions:**
```text
Fee Component has 3 distinct rate rules configured: 1) SC = $13.00 SGD; 2) PR = $43.00 SGD; 3) IS-Non-ASEAN = $150.00 SGD.
```

**Test Data:**
```text
Students: STU-SC (Singapore Citizen), STU-PR (Permanent Resident), STU-IS (International Student)
```

**Test Steps:**
1. Publish fee publication for all students.
2. Inspect generated student charges for STU-SC, STU-PR, and STU-IS.

**Expected Result:**
> 1. STU-SC charged exactly $13.00 SGD base amount.
> 2. STU-PR charged exactly $43.00 SGD base amount.
> 3. STU-IS charged exactly $150.00 SGD base amount.
> 4. Zero cross-category pricing errors (BR-R3-43).

---

#### `TC-R3-F11-004`: Verify if no rate rule matches, system raises explicit missing rule error, never arbitrary charge

- **Scenario ID**: `TS-R3-F11`
- **Test Suite**: Fee Pricing Engine
- **Page / Target**: `Admin Portal > Fee Rates`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Negative`
- **Traceability**: R3 FS v1.1 §3.11 F11-AC33; BR-R3-44
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: CR: Missing rate rule must halt publication for that student, not invent zero fee.
- **Note**: Prevents financial losses caused by silent pricing fallbacks.

**Preconditions:**
```text
Fee Component has rate rules only for SC and PR. Student STU-IS-ASEAN is enrolled.
```

**Test Data:**
```text
student_category: 'INTERNATIONAL_STUDENT_ASEAN', pricing_date: '2026-03-01'
```

**Test Steps:**
1. Attempt to publish fee publication targeting STU-IS-ASEAN using RATE_RULE mode.
2. Inspect resolver and charge generation output.

**Expected Result:**
> 1. System detects no matching rate rule exists for 'INTERNATIONAL_STUDENT_ASEAN'.
> 2. System aborts charge generation for this student with explicit error 'ERR_NO_MATCHING_RATE_RULE'.
> 3. System NEVER defaults to $0.00 or arbitrary price without explicit rule (BR-R3-44).

---

#### `TC-R3-F11-005`: Verify system rejects Fee Rate Rule with negative or zero price_amount

- **Scenario ID**: `TS-R3-F11`
- **Test Suite**: Fee Pricing Engine
- **Page / Target**: `Admin Portal > Fee Rates`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `BVA`
- **Traceability**: R3 FS v1.1 §3.11 F11; BR-R3-41; BVA
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: TD: CHECK constraint (price_amount > 0).
- **Note**: Prevents inverted charges.

**Preconditions:**
```text
MOE HQ User on Fee Rate Rule setup screen.
```

**Test Data:**
```text
Negative test cases: 1) price_amount = -0.01; 2) price_amount = -50.00; 3) price_amount = 0.00 (unless explicit waiver rule).
```

**Test Steps:**
1. Submit rate rule with price_amount = -0.01 SGD.
2. Submit rate rule with price_amount = -50.00 SGD.
3. Submit rate rule with price_amount = 0.00 without waiver flag.

**Expected Result:**
> 1. Negative price rejected with error 'price_amount must be strictly positive' (HTTP 422).
> 2. Zero price rejected unless flagged as 100% scholarship/waiver rule.
> 3. Zero negative price rules inserted into database.

---

#### `TC-R3-F11-006`: Verify system prevents overlapping effective date ranges for identical Component + Level + Category

- **Scenario ID**: `TS-R3-F11`
- **Test Suite**: Fee Pricing Engine
- **Page / Target**: `Admin Portal > Fee Rates`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Integrity`
- **Traceability**: R3 FS v1.1 §3.11 F11; BR-R3-45
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: TD: Temporal range exclusion constraint to guarantee deterministic pricing.
- **Note**: Prevents pricing ambiguity caused by concurrent active rules.

**Preconditions:**
```text
Rule 1 exists: Component 'FC-01', Level 'PRI-1', Category 'SC', effective 2026-01-01 to 2026-06-30 at $13.00 SGD.
```

**Test Data:**
```text
Rule 2: Component 'FC-01', Level 'PRI-1', Category 'SC', effective 2026-05-01 to 2026-12-31 at $15.00 SGD (overlaps May-June).
```

**Test Steps:**
1. Attempt to save Rule 2.
2. Inspect validation response.

**Expected Result:**
> 1. System detects temporal overlap in date ranges for identical criteria.
> 2. Rejects creation with error: 'Overlapping rate rule detected for specified criteria between 2026-05-01 and 2026-06-30' (HTTP 409 Conflict).
> 3. User prompted to adjust start/end dates.

---

#### `TC-R3-F11-007`: Verify Rule Precedence: Specific Level rule takes precedence over Wildcard Level rule

- **Scenario ID**: `TS-R3-F11`
- **Test Suite**: Fee Pricing Engine
- **Page / Target**: `Admin Portal > Fee Rates`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `DecisionTable`
- **Traceability**: R3 FS v1.1 §3.11 F11; BR-R3-46; Q14
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: WA: Specificity-based resolution: Specific Level > Wildcard Level.
- **Note**: Rule resolution precedence hierarchy.

**Preconditions:**
```text
Rule A (Wildcard): Level = null, Category = 'SC', price = $15.00 SGD. Rule B (Specific): Level = 'PRI-1', Category = 'SC', price = $12.00 SGD.
```

**Test Data:**
```text
Student 1 in Primary 1; Student 2 in Primary 2.
```

**Test Steps:**
1. Evaluate price for Student 1 (Primary 1).
2. Evaluate price for Student 2 (Primary 2).

**Expected Result:**
> 1. Student 1 matches both rules; System applies Specific Rule B ($12.00 SGD).
> 2. Student 2 matches only Wildcard Rule A; System applies $15.00 SGD.
> 3. Specificity precedence rule resolves conflict deterministically.

---

#### `TC-R3-F11-008`: Verify currency precision enforcement: Banker's Rounding to 2 decimal places in SGD

- **Scenario ID**: `TS-R3-F11`
- **Test Suite**: Fee Pricing Engine
- **Page / Target**: `Admin Portal > Fee Rates`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `BVA`
- **Traceability**: R3 FS v1.1 §3.11 F11; BR-R3-41; IEEE-754 prevention
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: TD: Arbitrary-precision decimal arithmetic (Java BigDecimal / Python Decimal).
- **Note**: Precision audit for financial transactions.

**Preconditions:**
```text
Rate calculation involves fractional multipliers (e.g. 15% discount or 9% GST).
```

**Test Data:**
```text
Case 1: $14.99 * 0.15 = 2.2485 -> rounds to $2.25. Case 2: $12.505 -> rounds to $12.50 (round half to even).
```

**Test Steps:**
1. Execute calculation quotes with fractional values.
2. Inspect returned numeric decimals and database storage.

**Expected Result:**
> 1. All financial values stored as exact DECIMAL(10, 2) without IEEE-754 floating point drift.
> 2. Banker's rounding (Half to Even) applied consistently across all fee calculations.
> 3. No precision leakage in API JSON responses.

---


### Test Suite: Fee Publication Lifecycle

#### `TC-R3-F12-001`: Verify Fee Publication lifecycle transitions from DRAFT to PUBLISHED

- **Scenario ID**: `TS-R3-F12`
- **Test Suite**: Fee Publication Lifecycle
- **Page / Target**: `Admin Portal > Fee Publication`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `StateTransition`
- **Traceability**: R3 FS v1.1 §3.12 F12-AC34; BR-R3-47; BR-R3-48; Tender R3 Item 3
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: CR: Publication lifecycle: DRAFT -> PUBLISHED. TD: published_at audit timestamp.
- **Note**: Primary fee publication happy path.

**Preconditions:**
```text
Fee Component 'FC-001' and School 'SCH-RI-01' exist. Publication target configured.
```

**Test Data:**
```text
academic_year: 2026, billing_period: '2026-03-01 to 2026-03-31', charge_date: '2026-03-01', due_date: '2026-03-31'
```

**Test Steps:**
1. Create Fee Publication with status 'DRAFT'.
2. Review configured recipients and amounts.
3. Click [Publish].
4. Query fee_publications table status.

**Expected Result:**
> 1. Publication transitions from 'DRAFT' to 'PUBLISHED'.
> 2. published_by and published_at are populated with current user ID and timestamp.
> 3. Student charges generated for all resolved recipients (BR-R3-47, BR-R3-48).

---

#### `TC-R3-F12-002`: Verify system rejects Fee Publication with invalid billing period (end_date < start_date)

- **Scenario ID**: `TS-R3-F12`
- **Test Suite**: Fee Publication Lifecycle
- **Page / Target**: `Admin Portal > Fee Publication`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Negative`
- **Traceability**: R3 FS v1.1 §3.12 F12-AC35; BR-R3-48
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: TD: Chronological date order validation constraint.
- **Note**: Date sequence validation.

**Preconditions:**
```text
School User on Fee Publication setup screen.
```

**Test Data:**
```text
start_date: '2026-04-30', end_date: '2026-04-01' (end before start)
```

**Test Steps:**
1. Enter inverted billing period dates.
2. Click [Save Draft].

**Expected Result:**
> 1. System blocks submission with error: 'Billing period end_date cannot be earlier than start_date' (HTTP 422).
> 2. No publication record is created (BR-R3-48).

---

#### `TC-R3-F12-003`: Verify Fee Publication with pricing_mode = RATE_RULE enforces fixed_amount fields are null

- **Scenario ID**: `TS-R3-F12`
- **Test Suite**: Fee Publication Lifecycle
- **Page / Target**: `Admin Portal > Fee Publication`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Validation`
- **Traceability**: R3 FS v1.1 §3.12 F12-AC36; BR-R3-47
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: TD: Mutually exclusive pricing mode contract.
- **Note**: Contract assertion on pricing mode.

**Preconditions:**
```text
User selects pricing_mode = 'RATE_RULE'.
```

**Test Data:**
```text
pricing_mode: 'RATE_RULE', fixed_price: 50.00 (inconsistent payload)
```

**Test Steps:**
1. Dispatch POST /api/v1/fee-publications with pricing_mode = 'RATE_RULE' and fixed_price = 50.00.
2. Inspect response.

**Expected Result:**
> 1. System sanitizes or rejects payload: fixed_price must be null when pricing_mode is RATE_RULE.
> 2. Publication uses rate engine to evaluate student charges individually (BR-R3-47).

---

#### `TC-R3-F12-004`: Verify Fee Publication with pricing_mode = FIXED_AMOUNT requires valid fixed price_amount

- **Scenario ID**: `TS-R3-F12`
- **Test Suite**: Fee Publication Lifecycle
- **Page / Target**: `Admin Portal > Fee Publication`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Validation`
- **Traceability**: R3 FS v1.1 §3.12 F12-AC37; BR-R3-47
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: TD: Conditional mandatory validation rule.
- **Note**: Validation on fixed pricing mode.

**Preconditions:**
```text
User selects pricing_mode = 'FIXED_AMOUNT'.
```

**Test Data:**
```text
Case 1: fixed_price = 45.00 SGD (valid). Case 2: fixed_price = null (invalid). Case 3: fixed_price = -10.00 (invalid).
```

**Test Steps:**
1. Submit publication with FIXED_AMOUNT and fixed_price = null.
2. Submit publication with FIXED_AMOUNT and fixed_price = -10.00.
3. Submit publication with FIXED_AMOUNT and fixed_price = 45.00.

**Expected Result:**
> 1. Case 1 & 2 rejected with HTTP 422 ('Fixed price amount must be positive number when FIXED_AMOUNT selected').
> 2. Case 3 accepted; all resolved recipients charged identical fixed amount $45.00 SGD.

---

#### `TC-R3-F12-005`: Verify status PUBLISHED is immutable; cannot be edited or re-published, records published_by/at

- **Scenario ID**: `TS-R3-F12`
- **Test Suite**: Fee Publication Lifecycle
- **Page / Target**: `Admin Portal > Fee Publication`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Integrity`
- **Traceability**: R3 FS v1.1 §3.12 F12-AC38; BR-R3-49
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: CR: Published publications are immutable for financial integrity.
- **Note**: Financial immutability guard.

**Preconditions:**
```text
Fee Publication 'PUB-2026-001' is in status 'PUBLISHED'.
```

**Test Data:**
```text
publication_id: 'PUB-2026-001', updated_name: 'Modified Fee Publication'
```

**Test Steps:**
1. Attempt to update billing_period or target configuration of 'PUB-2026-001' via PUT API.
2. Attempt to trigger [Publish] action again.

**Expected Result:**
> 1. Edit attempt rejected with HTTP 422 ('Cannot modify a published Fee Publication; use Charge Adjustment for corrections').
> 2. Re-publish attempt rejected (HTTP 409 Conflict).
> 3. published_by and published_at remain permanent and immutable (BR-R3-49).

---

#### `TC-R3-F12-006`: Verify Optimistic locking / row_version: concurrent edits generate conflict warning

- **Scenario ID**: `TS-R3-F12`
- **Test Suite**: Fee Publication Lifecycle
- **Page / Target**: `Admin Portal > Fee Publication`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Concurrency`
- **Traceability**: R3 FS v1.1 §3.12 F12-AC39; BR-R3-51; EF01
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: TD: Optimistic locking with row_version / ETag.
- **Note**: Concurrency control against lost updates.

**Preconditions:**
```text
Fee Publication 'PUB-DRAFT-01' has row_version = 1. User A and User B open the edit form simultaneously.
```

**Test Data:**
```text
User A updates description; User B updates target class.
```

**Test Steps:**
1. User A submits changes (row_version 1 -> 2). Update succeeds.
2. User B submits changes still presenting row_version = 1.
3. Inspect response to User B.

**Expected Result:**
> 1. System detects stale row_version for User B.
> 2. User B request rejected with HTTP 409 Conflict ('Record has been updated by another user. Please refresh and review changes').
> 3. Overwriting User A's changes without review is prevented.

---

#### `TC-R3-F12-007`: Verify Date sequence validation: due_date must not be earlier than charge_date

- **Scenario ID**: `TS-R3-F12`
- **Test Suite**: Fee Publication Lifecycle
- **Page / Target**: `Admin Portal > Fee Publication`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `BVA`
- **Traceability**: R3 FS v1.1 §3.12 F12; BR-R3-52; Q18
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: CR: Due date must be on or after charge date.
- **Note**: Logical date hierarchy constraint.

**Preconditions:**
```text
School User on Fee Publication configuration screen.
```

**Test Data:**
```text
charge_date: '2026-05-15', due_date: '2026-05-10' (due before charge)
```

**Test Steps:**
1. Set charge_date = '2026-05-15'.
2. Set due_date = '2026-05-10'.
3. Click [Save].

**Expected Result:**
> 1. System blocks submission with validation error: 'due_date cannot be earlier than charge_date' (HTTP 422).
> 2. Date rule enforced: due_date >= charge_date (BR-R3-52).

---

#### `TC-R3-F12-008`: Verify Maker-Checker Principle (Four-Eyes): Approver must be distinct from Creator

- **Scenario ID**: `TS-R3-F12`
- **Test Suite**: Fee Publication Lifecycle
- **Page / Target**: `Admin Portal > Fee Publication`
- **Severity / Priority**: `S1` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Security`
- **Traceability**: R3 FS v1.1 §3.12 F12; BR-R3-49; Q16
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: WA: Four-Eyes Principle / Maker-Checker enforced on financial publications.
- **Note**: Internal financial fraud control.

**Preconditions:**
```text
Publication 'PUB-DRAFT-01' was created by User 'USR-MAKER-01'.
```

**Test Data:**
```text
Approver User: 'USR-MAKER-01' (same) vs 'USR-CHECKER-02' (distinct supervisor)
```

**Test Steps:**
1. User 'USR-MAKER-01' attempts to approve/publish their own publication.
2. User 'USR-CHECKER-02' reviews and approves the publication.

**Expected Result:**
> 1. Self-approval attempt is rejected with error: 'Creator cannot approve their own publication (Maker-Checker violation)' (HTTP 403).
> 2. Distinct approver successfully approves and publishes the fee batch.

---

#### `TC-R3-F12-009`: Verify asynchronous PROCESSING state prevents duplicate fee publication execution

- **Scenario ID**: `TS-R3-F12`
- **Test Suite**: Fee Publication Lifecycle
- **Page / Target**: `Admin Portal > Fee Publication`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Concurrency`
- **Traceability**: R3 FS v1.1 §3.12 F12; BR-R3-51; Q17
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: WA: Distributed lock and PROCESSING state guard idempotent batch execution.
- **Note**: Idempotent batch execution guard.

**Preconditions:**
```text
Large publication targeting 1,200 students. Publication action initiated and currently executing.
```

**Test Data:**
```text
publication_id: 'PUB-LARGE-01', status: 'PROCESSING'
```

**Test Steps:**
1. Click [Publish] to trigger background batch worker.
2. During background execution, rapidly click [Publish] again or send duplicate HTTP POST.
3. Verify database locks and job queue.

**Expected Result:**
> 1. Immediate state transition to 'PROCESSING' with distributed lock (Redis/DB lock).
> 2. Duplicate request rejected with HTTP 409 ('Publication is currently being processed').
> 3. Zero duplicate student charges created in database (BR-R3-51).

---


### Test Suite: Publication Target Configuration

#### `TC-R3-F13-001`: Verify Target mode ALL_STUDENTS (Component Scope) resolves all active students of the School

- **Scenario ID**: `TS-R3-F13`
- **Test Suite**: Publication Target Configuration
- **Page / Target**: `Admin Portal > Publication Target`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R3 FS v1.1 §3.13 F13-AC40; BR-R3-53; Tender R3 Item 3
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: CR: Target mode ALL_STUDENTS selects all school students.
- **Note**: School-wide target resolution.

**Preconditions:**
```text
School 'SCH-RI-01' has 500 active enrolled students across 6 levels.
```

**Test Data:**
```text
target_mode: 'ALL_STUDENTS' (COMPONENT_SCOPE)
```

**Test Steps:**
1. In Fee Publication setup, select target_mode = 'ALL_STUDENTS'.
2. Trigger target preview.
3. Verify returned recipient count.

**Expected Result:**
> 1. Preview resolves exactly all 500 active students enrolled in 'SCH-RI-01'.
> 2. Zero students from other schools are included (AC40, BR-R3-53).

---

#### `TC-R3-F13-002`: Verify Target mode BY_LEVEL selects strictly students enrolled in specified Level

- **Scenario ID**: `TS-R3-F13`
- **Test Suite**: Publication Target Configuration
- **Page / Target**: `Admin Portal > Publication Target`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R3 FS v1.1 §3.13 F13-AC41; BR-R3-54
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: CR: Level targeting selects only students of that level.
- **Note**: Cohort level targeting.

**Preconditions:**
```text
Level 'Primary 1' has 80 students across 3 classes. Level 'Primary 2' has 75 students.
```

**Test Data:**
```text
target_mode: 'BY_LEVEL', target_level_id: 'LVL-PRI-1'
```

**Test Steps:**
1. Select target_mode = 'BY_LEVEL' and pick Level 'Primary 1'.
2. Click [Preview Recipients].

**Expected Result:**
> 1. Preview lists exactly the 80 students enrolled in Primary 1.
> 2. Zero students from Primary 2 or other levels are included (AC41, BR-R3-54).

---

#### `TC-R3-F13-003`: Verify Target mode BY_CLASS selects strictly students enrolled in specified Class

- **Scenario ID**: `TS-R3-F13`
- **Test Suite**: Publication Target Configuration
- **Page / Target**: `Admin Portal > Publication Target`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R3 FS v1.1 §3.13 F13-AC42; BR-R3-54
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: CR: Class targeting isolates specific class roster.
- **Note**: Class-level fee targeting.

**Preconditions:**
```text
Class 'P1-EMERALD' has 28 students; Class 'P1-RUBY' has 30 students.
```

**Test Data:**
```text
target_mode: 'BY_CLASS', target_class_id: 'CLS-P1-EME'
```

**Test Steps:**
1. Select target_mode = 'BY_CLASS' and pick Class 'P1-EMERALD'.
2. Preview recipient list.

**Expected Result:**
> 1. Exactly the 28 students of 'P1-EMERALD' are resolved.
> 2. Zero students from 'P1-RUBY' or other classes are selected (AC42, BR-R3-54).

---

#### `TC-R3-F13-004`: Verify Target mode SPECIFIC_STUDENTS validates each individual student eligibility

- **Scenario ID**: `TS-R3-F13`
- **Test Suite**: Publication Target Configuration
- **Page / Target**: `Admin Portal > Publication Target`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R3 FS v1.1 §3.13 F13-AC43; BR-R3-53
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: CR: Explicit student targeting for ad-hoc/optional fees.
- **Note**: Individual recipient targeting.

**Preconditions:**
```text
Publication configured for optional remedial course targeting 5 specific students.
```

**Test Data:**
```text
target_mode: 'CUSTOM_TARGETS', student_ids: ['STU-01', 'STU-02', 'STU-03', 'STU-04', 'STU-05']
```

**Test Steps:**
1. Add 5 specific student IDs to publication target.
2. Click [Save & Validate].

**Expected Result:**
> 1. System validates all 5 students belong to the school and have active enrolments.
> 2. Exactly those 5 students are assigned as publication recipients (AC43, BR-R3-53).

---

#### `TC-R3-F13-005`: Verify system rejects target configuration if Level, Class, or Student belongs to another School

- **Scenario ID**: `TS-R3-F13`
- **Test Suite**: Publication Target Configuration
- **Page / Target**: `Admin Portal > Publication Target`
- **Severity / Priority**: `S1` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Negative`
- **Traceability**: R3 FS v1.1 §3.13 F13-AC44; BR-R3-54; §5.2 Access Control
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: TD: Target entity tenant validation guard.
- **Note**: Multi-tenant billing isolation.

**Preconditions:**
```text
Publication belongs to School A ('SCH-RI-01'). User attempts to add Class 'CLS-HCI-01' (belongs to School B) into target configuration.
```

**Test Data:**
```text
target_class_id: 'CLS-HCI-01' (School B class)
```

**Test Steps:**
1. Send API request POST /api/v1/fee-publications/PUB-01/targets with School B's class ID.
2. Inspect validation response.

**Expected Result:**
> 1. System blocks submission with HTTP 400 Bad Request.
> 2. Error message: 'Target entity does not belong to the publication school' (ERR_TARGET_SCHOOL_MISMATCH).
> 3. Cross-school billing strictly prevented (AC44, BR-R3-54).

---

#### `TC-R3-F13-006`: Verify Target combination logic: Target entities UNION combined with Citizenship filter INTERSECTION

- **Scenario ID**: `TS-R3-F13`
- **Test Suite**: Publication Target Configuration
- **Page / Target**: `Admin Portal > Publication Target`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `DecisionTable`
- **Traceability**: R3 FS v1.1 §3.13 F13; BR-R3-55; BR-R3-57; Q02
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: WA: Target rules evaluate as (Target_1 OR Target_2) AND (Citizenship_Filter).
- **Note**: Set logic evaluation for compound targets.

**Preconditions:**
```text
Class 1A has 20 SC, 5 PR. Class 1B has 18 SC, 6 PR. Target configured: Classes [1A, 1B] AND citizenship = 'SINGAPORE_CITIZEN'.
```

**Test Data:**
```text
targets: [Class 1A, Class 1B], citizenship_filter: 'SINGAPORE_CITIZEN'
```

**Test Steps:**
1. Configure targets for Class 1A and Class 1B (Union).
2. Apply filter: Singapore Citizens only (Intersection).
3. Resolve recipients.

**Expected Result:**
> 1. System takes Union of Class 1A and Class 1B (total 49 students).
> 2. Applies Citizenship filter (Intersection): selects only Singapore Citizens.
> 3. Exactly 38 SC students resolved (20 + 18); PR students excluded (BR-R3-55, BR-R3-57).

---

#### `TC-R3-F13-007`: Verify Target membership evaluated strictly as of eligibility_date

- **Scenario ID**: `TS-R3-F13`
- **Test Suite**: Publication Target Configuration
- **Page / Target**: `Admin Portal > Publication Target`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R3 FS v1.1 §3.13 F13; BR-R3-56
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: CR: Target membership evaluated as of eligibility_date.
- **Note**: Point-in-time eligibility evaluation.

**Preconditions:**
```text
Student enrolled in School on 2026-03-15. Publication configured with eligibility_date = '2026-03-01'.
```

**Test Data:**
```text
eligibility_date: '2026-03-01', student_enrol_date: '2026-03-15'
```

**Test Steps:**
1. Run recipient resolution with eligibility_date = '2026-03-01'.
2. Run recipient resolution with eligibility_date = '2026-03-20'.

**Expected Result:**
> 1. For eligibility_date 2026-03-01: Student had no active enrolment on that date -> excluded.
> 2. For eligibility_date 2026-03-20: Student has active enrolment -> included.
> 3. Strict temporal evaluation verified (BR-R3-56).

---


### Test Suite: Recipient Resolution Engine

#### `TC-R3-F14-001`: Verify Recipient Resolution accurately resolves students with active enrolment on eligibility_date

- **Scenario ID**: `TS-R3-F14`
- **Test Suite**: Recipient Resolution Engine
- **Page / Target**: `Admin Portal > Recipient Resolution`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R3 FS v1.1 §3.14 F14-AC45; BR-R3-58; BR-R3-59
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: CR: Resolved recipients snapshot with enrollment_id for full traceability.
- **Note**: Primary recipient resolution audit.

**Preconditions:**
```text
Publication 'PUB-001' targets Level 1. 80 students currently enrolled in Level 1 with active status.
```

**Test Data:**
```text
fee_publication_id: 'PUB-001', eligibility_date: '2026-02-01'
```

**Test Steps:**
1. Trigger recipient resolution engine.
2. Query fee_publication_recipients table.

**Expected Result:**
> 1. Exactly 80 rows inserted into fee_publication_recipients table.
> 2. Each record has student_id, enrollment_id, and resolved_at timestamp.
> 3. Recipient list is frozen for charge generation (AC45, BR-R3-58, BR-R3-59).

---

#### `TC-R3-F14-002`: Verify Idempotency: Re-running Recipient Resolution produces identical recipients with zero duplicates

- **Scenario ID**: `TS-R3-F14`
- **Test Suite**: Recipient Resolution Engine
- **Page / Target**: `Admin Portal > Recipient Resolution`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Integrity`
- **Traceability**: R3 FS v1.1 §3.14 F14-AC46; BR-R3-60
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: TD: Unique constraint on (fee_publication_id, student_id).
- **Note**: Idempotent resolution safety.

**Preconditions:**
```text
Recipient resolution already executed for 'PUB-001' with 80 recipients created.
```

**Test Data:**
```text
fee_publication_id: 'PUB-001'
```

**Test Steps:**
1. Re-execute recipient resolution API/batch worker.
2. Query fee_publication_recipients table count for 'PUB-001'.

**Expected Result:**
> 1. System recognizes existing resolved list.
> 2. No duplicate recipient rows created (count remains exactly 80).
> 3. Operation returns idempotent success (AC46, BR-R3-60).

---

#### `TC-R3-F14-003`: Verify system rejects recipient resolution if enrolment record belongs to another student

- **Scenario ID**: `TS-R3-F14`
- **Test Suite**: Recipient Resolution Engine
- **Page / Target**: `Admin Portal > Recipient Resolution`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Integrity`
- **Traceability**: R3 FS v1.1 §3.14 F14-AC47; BR-R3-61
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: TD: Relational integrity check: student_id must match enrolments.student_id.
- **Note**: Relational integrity check.

**Preconditions:**
```text
Data anomaly injection: Attempt to insert recipient pairing student_id 'STU-01' with enrollment_id belonging to 'STU-02'.
```

**Test Data:**
```text
student_id: 'STU-01', enrollment_id: 'ENR-STU-02'
```

**Test Steps:**
1. Dispatch resolver validation with mismatched student and enrolment IDs.
2. Inspect integrity error.

**Expected Result:**
> 1. System rejects record with HTTP 400 Bad Request ('Enrolment does not belong to specified student').
> 2. Zero corrupted recipient rows created (AC47, BR-R3-61).

---

#### `TC-R3-F14-004`: Verify Recipient resolver excludes students with status WITHDRAWN on eligibility_date

- **Scenario ID**: `TS-R3-F14`
- **Test Suite**: Recipient Resolution Engine
- **Page / Target**: `Admin Portal > Recipient Resolution`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R3 FS v1.1 §3.14 F14; BR-R3-58; Q06
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: WA: Withdrawn students excluded from subsequent billing runs.
- **Note**: Prevents wrongful billing of withdrawn students.

**Preconditions:**
```text
Student 'STU-WD-01' officially withdrew on 2026-02-15. Publication eligibility_date is 2026-03-01.
```

**Test Data:**
```text
withdrawn_student: 'STU-WD-01', eligibility_date: '2026-03-01'
```

**Test Steps:**
1. Run publication recipient resolution for March fees.
2. Inspect generated recipient list.

**Expected Result:**
> 1. Withdrawn student 'STU-WD-01' is excluded from resolution.
> 2. No student charge generated for student who already left school (BR-R3-58, Q06).

---


### Test Suite: Student Charge Generation

#### `TC-R3-F15-001`: Verify Student Charge generated for each resolved recipient with initial status DRAFT

- **Scenario ID**: `TS-R3-F15`
- **Test Suite**: Student Charge Generation
- **Page / Target**: `Admin Portal > Charge Generation`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R3 FS v1.1 §3.15 F15-AC48; BR-R3-62; Tender R3 Item 3
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: CR: Charges created as DRAFT, become POSTED upon publication release.
- **Note**: Primary charge generation workflow.

**Preconditions:**
```text
80 recipients resolved in F14 for Publication 'PUB-001'. Pricing evaluates to $20.00 base amount.
```

**Test Data:**
```text
publication_id: 'PUB-001', base_amount: 20.00 SGD
```

**Test Steps:**
1. Trigger charge generation process.
2. Query student_charges table.

**Expected Result:**
> 1. Exactly 80 student charge records created.
> 2. Initial charge status is 'DRAFT'.
> 3. Upon publication approval, charges transition to 'POSTED' and posted_at is set (AC48, BR-R3-62).

---

#### `TC-R3-F15-002`: Verify Student Charge calculates total_amount = base_amount + tax_amount (GST 9%)

- **Scenario ID**: `TS-R3-F15`
- **Test Suite**: Student Charge Generation
- **Page / Target**: `Admin Portal > Charge Generation`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Calculation`
- **Traceability**: R3 FS v1.1 §3.15 F15-AC49; BR-R3-63
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: CR: Total equals base plus tax. TD: Fixed 2 decimal precision.
- **Note**: Mathematical invariant verification.

**Preconditions:**
```text
Taxable Fee Component with 9% GST. Base price evaluated as $50.00 SGD.
```

**Test Data:**
```text
base_amount: 50.00, gst_rate: 0.09
```

**Test Steps:**
1. Generate student charge for taxable component.
2. Inspect columns: base_amount, tax_amount, total_amount.

**Expected Result:**
> 1. base_amount = 50.00 SGD.
> 2. tax_amount = 4.50 SGD ($50.00 * 9%).
> 3. total_amount = 54.50 SGD ($50.00 + $4.50).
> 4. Invariant enforced: total_amount == base_amount + tax_amount (AC49, BR-R3-63).

---

#### `TC-R3-F15-003`: Verify system rejects Student Charge with negative amount

- **Scenario ID**: `TS-R3-F15`
- **Test Suite**: Student Charge Generation
- **Page / Target**: `Admin Portal > Charge Generation`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Negative`
- **Traceability**: R3 FS v1.1 §3.15 F15-AC50; BR-R3-64
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: CR: Negative charges prohibited; waivers must use Adjustment workflow.
- **Note**: Ledger sign integrity.

**Preconditions:**
```text
Attempt to create a manual charge or rate rule resulting in negative charge.
```

**Test Data:**
```text
base_amount: -25.00 SGD
```

**Test Steps:**
1. Submit POST /api/v1/student-charges with negative base_amount.
2. Inspect response.

**Expected Result:**
> 1. System blocks creation with HTTP 422 Unprocessable Entity.
> 2. Error message: 'Charge amount cannot be negative. Use Student Charge Adjustment for waivers/reductions' (AC50, BR-R3-64).
> 3. Zero negative charges created.

---

#### `TC-R3-F15-004`: Verify unique constraint prevents duplicate charge for same Student, Publication, and Billing Period

- **Scenario ID**: `TS-R3-F15`
- **Test Suite**: Student Charge Generation
- **Page / Target**: `Admin Portal > Charge Generation`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Integrity`
- **Traceability**: R3 FS v1.1 §3.15 F15-AC51; BR-R3-65
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: TD: Unique index on (student_id, fee_publication_id, billing_period).
- **Note**: Prevents double billing upon batch restart.

**Preconditions:**
```text
Charge 'CHG-001' already generated for Student 'STU-01' under Publication 'PUB-001'.
```

**Test Data:**
```text
student_id: 'STU-01', publication_id: 'PUB-001'
```

**Test Steps:**
1. Re-run charge generation batch for 'PUB-001'.
2. Query student_charges table count for 'STU-01' and 'PUB-001'.

**Expected Result:**
> 1. System detects existing charge record.
> 2. Re-run skips existing charge without duplication (count remains exactly 1).
> 3. Operation completes idempotently (AC51, BR-R3-65).

---

#### `TC-R3-F15-005`: Verify Manual Student Charge creation sets source_type = MANUAL and requires idempotency_key

- **Scenario ID**: `TS-R3-F15`
- **Test Suite**: Student Charge Generation
- **Page / Target**: `Admin Portal > Manual Charges`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R3 FS v1.1 §3.15 F15-AC52; BR-R3-66
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: CR: Manual charges require explicit audit source and idempotency protection.
- **Note**: Ad-hoc fee generation with API idempotency.

**Preconditions:**
```text
School Finance User issues an ad-hoc charge (e.g. lost badge replacement).
```

**Test Data:**
```text
student_id: 'STU-01', fee_component: 'FC-BADGE-REPLACE', amount: 5.00, idempotency_key: 'uuid-man-9921'
```

**Test Steps:**
1. Submit manual charge request with idempotency_key.
2. Re-send identical request.
3. Query database record.

**Expected Result:**
> 1. First request creates charge with source_type = 'MANUAL' and status = 'POSTED'.
> 2. Second request detects identical idempotency_key and returns existing record without double-charging.
> 3. Zero duplicate charges created (AC52, BR-R3-66).

---

#### `TC-R3-F15-006`: Verify Void Student Charge records status VOID, voided_at, and void_reason

- **Scenario ID**: `TS-R3-F15`
- **Test Suite**: Student Charge Generation
- **Page / Target**: `Admin Portal > Charge Management`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `StateTransition`
- **Traceability**: R3 FS v1.1 §3.15 F15-AC53; BR-R3-67
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: CR: Voiding records immutable audit trail and removes debt from portal.
- **Note**: Void lifecycle state audit.

**Preconditions:**
```text
Student Charge 'CHG-ERR-01' issued by mistake (status POSTED, UNPAID).
```

**Test Data:**
```text
charge_id: 'CHG-ERR-01', void_reason: 'Issued in error to incorrect student'
```

**Test Steps:**
1. Finance Supervisor opens charge and clicks [Void Charge].
2. Enter void_reason and confirm.
3. Inspect database row.

**Expected Result:**
> 1. Charge status transitions to 'VOID'.
> 2. voided_at is populated with current timestamp; void_reason is stored.
> 3. Voided charge is immediately removed from parent outstanding charges on e-Service Portal (AC53, BR-R3-67).

---

#### `TC-R3-F15-007`: Verify only POSTED charges appear in parent outstanding charges on e-Service Portal

- **Scenario ID**: `TS-R3-F15`
- **Test Suite**: Student Charge Generation
- **Page / Target**: `e-Service Portal > Outstanding Charges`
- **Severity / Priority**: `S1` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Visibility`
- **Traceability**: R3 FS v1.1 §3.15 F15-AC54; BR-R3-68; Tender R3 Item 3
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: CR: Only POSTED, UNPAID charges are visible for payment on portal.
- **Note**: Cross-portal visibility verification.

**Preconditions:**
```text
Student has 4 charges in database: 1) Status DRAFT; 2) Status POSTED ($30.00); 3) Status VOID ($20.00); 4) Status PAID ($50.00).
```

**Test Data:**
```text
student_id: 'STU-01'
```

**Test Steps:**
1. Parent logs in to e-Service Portal via SingPass.
2. Navigate to [Outstanding Charges] screen.
3. Inspect listed payable items.

**Expected Result:**
> 1. Parent sees strictly the single POSTED charge ($30.00 SGD).
> 2. DRAFT charges are invisible.
> 3. VOID and PAID charges are not listed as outstanding payable items (AC54, BR-R3-68).
> 4. Total outstanding balance displayed = $30.00 SGD.

---

#### `TC-R3-F15-008`: Verify Snapshot integrity: student_charges records citizenship_snapshot and pricing_date snapshot

- **Scenario ID**: `TS-R3-F15`
- **Test Suite**: Student Charge Generation
- **Page / Target**: `Admin Portal > Charge Management`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Audit`
- **Traceability**: R3 FS v1.1 §3.15 F15; BR-R3-69; Q19
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: WA: Immutable snapshot of citizenship at time of charge generation.
- **Note**: Protects historical financial ledger from retroactive mutation.

**Preconditions:**
```text
Student was PR when fee was charged ($43.00 SGD). Student subsequently naturalizes to SC 3 months later.
```

**Test Data:**
```text
Original charge: citizenship_snapshot = 'PERMANENT_RESIDENT', amount = 43.00 SGD
```

**Test Steps:**
1. Verify stored student_charge record after student becomes SC.
2. Inspect historic charge columns.

**Expected Result:**
> 1. Historic charge preserves citizenship_snapshot = 'PERMANENT_RESIDENT'.
> 2. Historical amount remains $43.00 SGD and does not retroactively mutate to SC rate ($13.00).
> 3. Financial snapshot isolation verified (BR-R3-69, Q19).

---

#### `TC-R3-F15-009`: Verify Due Date calculation: due_date = charge_date + 30 days by default

- **Scenario ID**: `TS-R3-F15`
- **Test Suite**: Student Charge Generation
- **Page / Target**: `Admin Portal > Charge Generation`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `BVA`
- **Traceability**: R3 FS v1.1 §3.15 F15; BR-R3-70; Q18
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: WA: Default payment grace period is 30 calendar days from charge date.
- **Note**: Standard 30-day payment term calculation.

**Preconditions:**
```text
Publication configured with charge_date = '2026-03-01' without custom due date override.
```

**Test Data:**
```text
charge_date: '2026-03-01'
```

**Test Steps:**
1. Generate student charges.
2. Inspect calculated due_date column.

**Expected Result:**
> 1. System calculates due_date = '2026-03-31' (charge_date + 30 calendar days).
> 2. Due date correctly accounts for month boundaries (e.g. February leap year vs non-leap year) (BR-R3-70, Q18).

---

#### `TC-R3-F15-010`: Verify Payment status initialized to UNPAID and paid_amount = 0.00 upon charge generation

- **Scenario ID**: `TS-R3-F15`
- **Test Suite**: Student Charge Generation
- **Page / Target**: `Admin Portal > Charge Generation`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R3 FS v1.1 §3.15 F15; BR-R3-62; Q20
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: TD: Explicit initial state for payment tracking.
- **Note**: Initial ledger state verification.

**Preconditions:**
```text
Fresh Student Charge generated from Publication.
```

**Test Data:**
```text
total_amount: 35.00 SGD
```

**Test Steps:**
1. Query database columns for newly created student_charge.
2. Inspect payment fields.

**Expected Result:**
> 1. payment_status is initialized to 'UNPAID'.
> 2. paid_amount is initialized to 0.00 SGD.
> 3. outstanding_amount equals total_amount ($35.00 SGD) (BR-R3-62, Q20).

---


### Test Suite: Charge Adjustment & Audit

#### `TC-R3-F16-001`: Verify Student Charge Adjustment creates valid adjustment record with reason code

- **Scenario ID**: `TS-R3-F16`
- **Test Suite**: Charge Adjustment & Audit
- **Page / Target**: `Admin Portal > Charge Adjustment`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R3 FS v1.1 §3.16 F16-AC55; BR-R3-71; Tender R3 Item 3
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: CR: Adjustments adjust effective amount without modifying original charge.
- **Note**: Standard charge adjustment flow.

**Preconditions:**
```text
Student Charge 'CHG-001' exists with total_amount = $50.00 SGD.
```

**Test Data:**
```text
adjustment_amount: -10.00, reason_code: 'FAS_PARTIAL_SUBSIDY', note: 'School assistance grant'
```

**Test Steps:**
1. Navigate to Charge Adjustments.
2. Click [Create Adjustment] for 'CHG-001'.
3. Enter amount -10.00 SGD, reason_code, and note.
4. Submit and approve adjustment.

**Expected Result:**
> 1. Record created in student_charge_adjustments table with status 'APPROVED'.
> 2. Effective balance payable updates to $40.00 SGD ($50.00 - $10.00).
> 3. Original base_amount remains untouched at $50.00 (AC55, BR-R3-71).

---

#### `TC-R3-F16-002`: Verify Positive adjustment increases effective amount due

- **Scenario ID**: `TS-R3-F16`
- **Test Suite**: Charge Adjustment & Audit
- **Page / Target**: `Admin Portal > Charge Adjustment`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Calculation`
- **Traceability**: R3 FS v1.1 §3.16 F16-AC56; BR-R3-72
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: CR: Positive adjustment increases effective amount.
- **Note**: Positive adjustment calculation.

**Preconditions:**
```text
Student Charge 'CHG-002' has initial total_amount = $40.00 SGD.
```

**Test Data:**
```text
adjustment_amount: +15.00 SGD, reason_code: 'LATE_ENROLMENT_ADDITIONAL_MODULE'
```

**Test Steps:**
1. Apply positive adjustment of +$15.00 SGD to 'CHG-002'.
2. Approve adjustment.
3. Inspect effective amount.

**Expected Result:**
> 1. System calculates effective_amount = $40.00 + $15.00 = $55.00 SGD.
> 2. Outstanding amount payable on portal updates to $55.00 SGD (AC56, BR-R3-72).

---

#### `TC-R3-F16-003`: Verify Negative adjustment decreases effective amount due

- **Scenario ID**: `TS-R3-F16`
- **Test Suite**: Charge Adjustment & Audit
- **Page / Target**: `Admin Portal > Charge Adjustment`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Calculation`
- **Traceability**: R3 FS v1.1 §3.16 F16-AC57; BR-R3-72
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: CR: Negative adjustment decreases effective amount.
- **Note**: Negative adjustment waiver calculation.

**Preconditions:**
```text
Student Charge 'CHG-003' has initial total_amount = $60.00 SGD.
```

**Test Data:**
```text
adjustment_amount: -25.00 SGD, reason_code: 'PRINCIPAL_DISCRETIONARY_WAIVER'
```

**Test Steps:**
1. Apply negative adjustment of -$25.00 SGD to 'CHG-003'.
2. Approve adjustment.
3. Inspect effective amount.

**Expected Result:**
> 1. System calculates effective_amount = $60.00 - $25.00 = $35.00 SGD.
> 2. Outstanding amount payable on portal updates to $35.00 SGD (AC57, BR-R3-72).

---

#### `TC-R3-F16-004`: Verify original charge base_amount and tax_amount remain strictly immutable upon adjustment

- **Scenario ID**: `TS-R3-F16`
- **Test Suite**: Charge Adjustment & Audit
- **Page / Target**: `Admin Portal > Charge Adjustment`
- **Severity / Priority**: `S1` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Integrity`
- **Traceability**: R3 FS v1.1 §3.16 F16-AC58; BR-R3-73; WA-R3-09
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: CR: Original charge amounts are immutable; adjustment ledger is additive.
- **Note**: Double-entry bookkeeping integrity guard.

**Preconditions:**
```text
Charge 'CHG-001' has base_amount = $100.00, tax_amount = $9.00. Adjustment of -$30.00 applied.
```

**Test Data:**
```text
charge_id: 'CHG-001', adjustment: -30.00 SGD
```

**Test Steps:**
1. Query student_charges row directly in database before and after adjustment.
2. Compare base_amount and tax_amount columns.

**Expected Result:**
> 1. base_amount remains exactly 100.00 SGD; tax_amount remains exactly 9.00 SGD.
> 2. Direct UPDATE on student_charges amounts is prevented (AC58, BR-R3-73).
> 3. Adjustment is stored in separate ledger table student_charge_adjustments.

---

#### `TC-R3-F16-005`: Verify Audit tracking records created_by, created_at, and reason_code for every adjustment

- **Scenario ID**: `TS-R3-F16`
- **Test Suite**: Charge Adjustment & Audit
- **Page / Target**: `Admin Portal > Charge Adjustment`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Audit`
- **Traceability**: R3 FS v1.1 §3.16 F16-AC59; BR-R3-74
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: TD: Comprehensive audit metadata on financial adjustments.
- **Note**: Financial audit compliance.

**Preconditions:**
```text
User 'finance.lead@ri.edu.sg' submits adjustment.
```

**Test Data:**
```text
reason_code: 'FINANCIAL_HARDSHIP_SPECIAL_GRANT'
```

**Test Steps:**
1. Submit adjustment.
2. Query student_charge_adjustments audit columns.

**Expected Result:**
> 1. created_by is populated with 'finance.lead@ri.edu.sg'.
> 2. created_at populated with exact UTC timestamp.
> 3. reason_code correctly stored and mapped to standard enum (AC59, BR-R3-74).

---

#### `TC-R3-F16-006`: Verify Adjustment in PENDING_APPROVAL status is not applied to effective balance until approved

- **Scenario ID**: `TS-R3-F16`
- **Test Suite**: Charge Adjustment & Audit
- **Page / Target**: `Admin Portal > Charge Adjustment`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `StateTransition`
- **Traceability**: R3 FS v1.1 §3.16 F16-AC60; BR-R3-75
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: CR: Unapproved adjustments have zero effect on ledger balances.
- **Note**: Approval workflow state gating.

**Preconditions:**
```text
Charge has total_amount = $100.00 SGD. Adjustment of -$40.00 created with status 'PENDING_APPROVAL'.
```

**Test Data:**
```text
adjustment_status: 'PENDING_APPROVAL'
```

**Test Steps:**
1. Inspect effective amount while adjustment is PENDING_APPROVAL.
2. Check parent portal outstanding charges balance.
3. Approve adjustment and re-check balance.

**Expected Result:**
> 1. While PENDING_APPROVAL, effective balance remains $100.00 SGD.
> 2. Parent portal continues to show $100.00 SGD.
> 3. Upon supervisor approval, status transitions to 'APPROVED' and effective balance reduces to $60.00 SGD (AC60, BR-R3-75).

---

#### `TC-R3-F16-007`: Verify system blocks adjustment that would result in negative effective amount

- **Scenario ID**: `TS-R3-F16`
- **Test Suite**: Charge Adjustment & Audit
- **Page / Target**: `Admin Portal > Charge Adjustment`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Negative`
- **Traceability**: R3 FS v1.1 §3.16 F16; BR-R3-76; BVA
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: TD: Effective charge amount bounded by lower bound 0.00.
- **Note**: Prevents negative payable balances.

**Preconditions:**
```text
Student Charge has total_amount = $50.00 SGD. User attempts to apply waiver of -$60.00 SGD.
```

**Test Data:**
```text
total_amount: 50.00 SGD, requested_adjustment: -60.00 SGD
```

**Test Steps:**
1. Enter adjustment amount = -60.00 SGD.
2. Click [Submit].

**Expected Result:**
> 1. System blocks submission with error: 'Adjustment cannot exceed outstanding charge amount. Effective amount cannot be negative' (HTTP 422).
> 2. Maximum allowable negative adjustment is capped at -$50.00 SGD (BR-R3-76).

---

#### `TC-R3-F16-008`: Verify Foreign Key validation: adjustment must link to valid student_charge_id

- **Scenario ID**: `TS-R3-F16`
- **Test Suite**: Charge Adjustment & Audit
- **Page / Target**: `Admin Portal > Charge Adjustment`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Integrity`
- **Traceability**: R3 FS v1.1 §3.16 F16; BR-R3-77; Q21
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: TD: Foreign key constraint on student_charge_adjustments.student_charge_id.
- **Note**: Database relational constraint.

**Preconditions:**
```text
Attempt to create adjustment with non-existent student_charge_id.
```

**Test Data:**
```text
student_charge_id: 'CHG-NONEXISTENT-999'
```

**Test Steps:**
1. Send POST /api/v1/student-charge-adjustments with invalid student_charge_id.
2. Inspect response.

**Expected Result:**
> 1. System rejects request with HTTP 400 Bad Request ('Referenced Student Charge does not exist').
> 2. Foreign key integrity strictly enforced (BR-R3-77, Q21).

---

#### `TC-R3-F16-009`: Verify Tiered Approval Threshold: School approves < $200 SGD, MOE HQ approves >= $200 SGD

- **Scenario ID**: `TS-R3-F16`
- **Test Suite**: Charge Adjustment & Audit
- **Page / Target**: `Admin Portal > Charge Adjustment`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Security`
- **Traceability**: R3 FS v1.1 §3.16 F16; BR-R3-78; Q16
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: WA: Tiered approval thresholds govern financial risk controls.
- **Note**: Financial governance delegation of authority.

**Preconditions:**
```text
Adjustment A is -$150.00 SGD. Adjustment B is -$250.00 SGD. User is School Principal.
```

**Test Data:**
```text
Case A: -150.00 SGD. Case B: -250.00 SGD.
```

**Test Steps:**
1. School Principal attempts to approve Adjustment A (-$150.00).
2. School Principal attempts to approve Adjustment B (-$250.00).
3. MOE HQ Director reviews Adjustment B.

**Expected Result:**
> 1. Adjustment A approved successfully by School Principal (< $200 threshold).
> 2. School Principal approval of Adjustment B rejected: 'Adjustments >= $200 SGD require MOE HQ approval'.
> 3. MOE HQ Director successfully approves Adjustment B (BR-R3-78, Q16).

---


### Test Suite: Edusave Payment & Reconciliation

#### `TC-R3-PAY-001`: Verify only Singaporean Student charges with eligible Fee Component can be paid via Edusave

- **Scenario ID**: `TS-R3-PAY`
- **Test Suite**: Edusave Payment & Reconciliation
- **Page / Target**: `e-Service Portal > Payment`
- **Severity / Priority**: `S1` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R3 FS v1.1 §4 Payment Rule; BR-R3-80; Tender R3 Item 3
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: CR: Singaporean students can use Edusave balance to pay eligible fees per Tender R3.
- **Note**: Statutory payment method entitlement check.

**Preconditions:**
```text
Student STU-SC-01 is Singaporean with active Education Account (balance $200 SGD). Student STU-PR-01 is PR without Education Account. Fee Component 'FC-STD-MISC' has allow_edusave_payment = true.
```

**Test Data:**
```text
Student STU-SC-01 ($30 charge); Student STU-PR-01 ($30 charge)
```

**Test Steps:**
1. Parent of STU-SC-01 selects charge and views payment options.
2. Parent of STU-PR-01 selects charge and views payment options.

**Expected Result:**
> 1. For STU-SC-01, [Pay using Education Account] button is ENABLED; available balance $200 SGD is displayed.
> 2. For STU-PR-01, [Pay using Education Account] option is HIDDEN/DISABLED; parent is restricted to credit card / PayNow (BR-R3-80, Tender R3 Item 3).

---

#### `TC-R3-PAY-002`: Verify system rejects Edusave payment attempt for non-eligible Fee Component (allow_edusave_payment = false)

- **Scenario ID**: `TS-R3-PAY`
- **Test Suite**: Edusave Payment & Reconciliation
- **Page / Target**: `e-Service Portal > Payment`
- **Severity / Priority**: `S1` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Negative`
- **Traceability**: R3 FS v1.1 §4 Payment Rule; BR-R3-81; Tender R3 Item 3
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: CR: Strict enforcement of statutory fee component eligibility.
- **Note**: Prevents unauthorized use of government education subsidies.

**Preconditions:**
```text
Student STU-SC-01 has active Education Account ($300 SGD). Charge is for Fee Component 'FC-OPTIONAL-TRIP' with allow_edusave_payment = false.
```

**Test Data:**
```text
charge_id: 'CHG-TRIP-01', amount: 80.00 SGD
```

**Test Steps:**
1. Attempt to dispatch API payment payload specifying payment_method = 'EDUCATION_ACCOUNT' for 'CHG-TRIP-01'.
2. Inspect response.

**Expected Result:**
> 1. System rejects transaction with HTTP 422 Unprocessable Entity.
> 2. Error message: 'This fee component is not eligible for payment via Education Account per MOE regulations' (ERR_INELIGIBLE_FEE_COMPONENT).
> 3. Zero funds deducted from Education Account (BR-R3-81).

---

#### `TC-R3-PAY-003`: Verify Full Edusave Payment: Account balance >= charge amount deducts balance and sets status PAID

- **Scenario ID**: `TS-R3-PAY`
- **Test Suite**: Edusave Payment & Reconciliation
- **Page / Target**: `e-Service Portal > Payment`
- **Severity / Priority**: `S1` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: R3 FS v1.1 §4 Payment Rule; BR-R3-82; Tender R3 Item 3
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: CR: Full fee deduction updates account balance and settles charge.
- **Note**: Primary happy path for Edusave fee settlement.

**Preconditions:**
```text
Student STU-SC-01 has Education Account balance = $150.00 SGD. Outstanding charge = $40.00 SGD for eligible miscellaneous fees.
```

**Test Data:**
```text
charge_amount: 40.00 SGD, initial_ea_balance: 150.00 SGD
```

**Test Steps:**
1. Parent selects charge and clicks [Confirm Payment with Education Account].
2. System processes payment transaction.
3. Query student_charges and education_accounts tables.

**Expected Result:**
> 1. Education Account balance decremented to $110.00 SGD ($150.00 - $40.00).
> 2. Student Charge status transitions from 'POSTED' to 'PAID', paid_amount = $40.00, outstanding_amount = $0.00.
> 3. Immutable transaction ledger entry created with transaction_type = 'FEE_PAYMENT' and reference to charge_id (BR-R3-82).

---

#### `TC-R3-PAY-004`: Verify Split Payment: Insufficient Education Account balance deducts available balance, remaining balance stays UNPAID

- **Scenario ID**: `TS-R3-PAY`
- **Test Suite**: Edusave Payment & Reconciliation
- **Page / Target**: `e-Service Portal > Payment`
- **Severity / Priority**: `S1` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `BVA`
- **Traceability**: R3 FS v1.1 §4 Payment Rule; BR-R3-83; Q15; Tender R3 Item 3
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: CR: Function 9 / R9 supports split bill between Edusave and online payment.
- **Note**: Split billing boundary handling.

**Preconditions:**
```text
Student STU-SC-01 has Education Account balance = $25.00 SGD. Outstanding charge = $60.00 SGD. System supports Split Payment (R9).
```

**Test Data:**
```text
charge_amount: 60.00 SGD, available_ea_balance: 25.00 SGD
```

**Test Steps:**
1. Parent initiates payment, selects 'Use full Education Account balance ($25.00)'.
2. System deducts available balance.
3. Inspect updated charge status and remaining balance.

**Expected Result:**
> 1. Education Account balance decremented to $0.00 SGD.
> 2. Student Charge record updated: paid_amount = $25.00, outstanding_amount = $35.00 SGD ($60.00 - $25.00).
> 3. Charge status remains 'PARTIALLY_PAID' (or UNPAID with partial ledger).
> 4. Parent is prompted to pay remaining $35.00 SGD via online payment (PayNow/Credit Card) in R9 (BR-R3-83, Q15).

---

#### `TC-R3-PAY-005`: Verify Concurrency: Prevent race condition on simultaneous payment requests against same Education Account

- **Scenario ID**: `TS-R3-PAY`
- **Test Suite**: Edusave Payment & Reconciliation
- **Page / Target**: `e-Service Portal > Payment`
- **Severity / Priority**: `S1` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Concurrency`
- **Traceability**: R3 FS v1.1 §4 Payment Rule; BR-R3-84; Concurrency Isolation
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: TD: Pessimistic row locking on wallet balance updates prevents double-spending.
- **Note**: Prevents double-spend and overdraft race conditions.

**Preconditions:**
```text
Education Account has balance = $50.00 SGD. Two charges 'CHG-A' ($40) and 'CHG-B' ($40) exist. Total needed = $80 > balance.
```

**Test Data:**
```text
simultaneous_requests: [Pay CHG-A ($40), Pay CHG-B ($40)] at exact same millisecond
```

**Test Steps:**
1. Dispatch concurrent HTTP POST requests for CHG-A and CHG-B using asynchronous thread pool.
2. Inspect database transaction isolation (SELECT FOR UPDATE / SERIALIZABLE).

**Expected Result:**
> 1. First request acquires row lock on education_account, succeeds, and deducts $40.00 (balance becomes $10.00).
> 2. Second request reads updated balance ($10.00), detects insufficient funds for $40 charge.
> 3. Second request fails safely or offers partial payment; account balance NEVER becomes negative ($10.00 >= 0.00) (BR-R3-84).

---


### Test Suite: Tender E2E Integration

#### `TC-R3-TENDER-001`: End-to-End Workflow: MOE HQ creates school -> School creates roster -> HQ publishes fee -> Student pays via Edusave

- **Scenario ID**: `TS-R3-TENDER`
- **Test Suite**: Tender E2E Integration
- **Page / Target**: `Admin Portal & e-Service Portal`
- **Severity / Priority**: `S1` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: Tender R3 Item 3; R3 FS v1.1 §2 Process Overview; §3 F01-F16; §4 Payment Rule
- **Environment**: SIT | Chrome (latest) + DB read access | Build: Sprint 1 MVP
- **Assumption Reference**: CR: Complete lifecycle delivery conforming strictly to Tender Requirement Item 3.
- **Note**: Executive End-to-End Acceptance Test Case demonstrating 100% R3 compliance.

**Preconditions:**
```text
Fresh tenant environment. MOE HQ Admin, School User, and Singaporean Parent accounts provisioned. R1 Education Account active.
```

**Test Data:**
```text
School: 'SCH-RI-01', Level: 'PRI-1', Class: 'P1-A', Student: 'Tan Wei Ming' (SC), Fee: 'Standard Misc' ($13.00)
```

**Test Steps:**
1. MOE HQ creates School 'SCH-RI-01' and assigns School User (F01, F02).
2. School User creates Academic Level 'PRI-1' and Class 'P1-A' (F03, F04).
3. School User creates Student and enrolls into Class 'P1-A' (F05, F06).
4. System auto-links Singaporean student to R1 Education Account (F08).
5. MOE HQ configures Fee Component and Fee Rate Rule ($13.00 for SC) (F09, F10, F11).
6. MOE HQ publishes Fee Publication targeting School 'SCH-RI-01' (F12, F13, F14, F15).
7. System resolves student, generates $13.00 Student Charge in status POSTED.
8. Parent logs in to e-Service Portal, views outstanding charge, and selects Edusave payment.
9. System deducts $13.00 from Education Account, marks charge PAID, and records audit trail.

**Expected Result:**
> 1. All 16 functions execute seamlessly in end-to-end integration.
> 2. RTM traceability verified: Tender Requirement Item 3 is 100% satisfied.
> 3. Student Charge status is PAID; Education Account reflects deduction; financial ledger reconciles with zero discrepancies.

---
