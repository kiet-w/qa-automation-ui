# R8: Parent Portal (SingPass, Profile & Account Info) — Sprint 1 Test Cases

> **Module**: R8 - Parent Portal & SingPass Profile
> **Specification Reference**: [FS-08_Parent_Portal_SingPass_Profile.md](file:////home/baudui/Projects/automation-ui/[agile] fs/md/FS document/FS-08_Parent_Portal_SingPass_Profile.md)
> **Source Spreadsheet**: `Test Cases + Defect sprint 1.xlsx` (Sheet `R8 TC`)
> **Total Test Cases**: 125

## Executive Test Suite Summary

| Test Suite | Scenario Count | Test Cases | Priorities | Severities |
| :--- | :--- | :--- | :--- | :--- |
| SingPass Login | 1 (TS-001) | 17 | Critical, High, Low, Medium | S1 (highest), S2, S3 |
| Login Data Refresh | 1 (TS-002) | 12 | Critical, High, Medium | S1 (highest), S2, S3 |
| Session | 1 (TS-003) | 4 | High, Medium | S2, S3 |
| Home | 1 (TS-004) | 17 | High, Low, Medium | S2, S3, S4 (lowest) |
| Education Account - Account Info | 1 (TS-005) | 13 | Critical, High, Low, Medium | S1 (highest), S2, S3 |
| Education Account - Balance | 1 (TS-006) | 5 | Critical, High, Medium | S1 (highest), S2, S3 |
| Education Account - FAS | 1 (TS-007) | 3 | Low, Medium | S3, S4 (lowest) |
| Education Account - Transactions | 1 (TS-008) | 19 | Critical, High, Low, Medium | S1 (highest), S2, S3, S4 (lowest) |
| Age 16 View-only Rules | 1 (TS-009) | 3 | Critical, High | S1 (highest), S2 |
| My Details | 1 (TS-010) | 21 | Critical, High, Low, Medium | S1 (highest), S2, S3, S4 (lowest) |
| Authorization & Data Protection | 1 (TS-011) | 4 | Critical, High | S1 (highest), S2 |
| Audit Log | 1 (TS-012) | 3 | High | S2 |
| Non-functional | 1 (TS-013) | 4 | Low, Medium | S2, S3, S4 (lowest) |

---

## Quick Reference Index Table

| Test Case ID | Scenario ID | Title | Page / Area | Priority | Severity | Type | Defect ID | Traceability |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| [`TC-R8-001`](#tc-r8-001) | `TS-001` | Verify Landing page shows the 'Log in with SingPass' button | Landing page | Medium | S3 | UI |  | FR-08.1; FS R8 sec. 6; US-08.1; PB-06 |
| [`TC-R8-002`](#tc-r8-002) | `TS-001` | Verify first-time SingPass login creates a parent account and opens Home | Landing page > Home | Critical | S1 (highest) | Functional |  | FR-08.1 steps 1-5; R8-AC01; US-08.1; PB-06; PB-07 |
| [`TC-R8-003`](#tc-r8-003) | `TS-001` | Verify a returning parent reuses the existing account | Landing page > Home | High | S2 | Functional |  | FR-08.1 step 3; R8-AC02; PB-06 |
| [`TC-R8-004`](#tc-r8-004) | `TS-001` | Verify cancelling SingPass returns to Landing with MSG-0802 | Landing page | Medium | S3 | Functional |  | FR-08.1 errors; R8-AC05; PB-06 |
| [`TC-R8-005`](#tc-r8-005) | `TS-001` | Verify a SingPass authentication error returns to Landing with MSG-0802 | Landing page | High | S2 | Integration |  | FR-08.1 errors; R8-AC05; PB-06 |
| [`TC-R8-006`](#tc-r8-006) | `TS-001` | Verify login is refused when the NRIC is not found in the data API | Landing page | High | S2 | Functional |  | FR-08.1 rules; R8-AC03; PB-07 |
| [`TC-R8-007`](#tc-r8-007) | `TS-001` | Verify login is refused when the parent has no linked child | Landing page | High | S2 | Functional |  | FR-08.1 rules; R8-AC03; PB-07 |
| [`TC-R8-008`](#tc-r8-008) | `TS-001` | Verify login is refused when the data API returns an error | Landing page | High | S2 | Integration |  | FR-08.1 errors; R8-AC23 |
| [`TC-R8-009`](#tc-r8-009) | `TS-001` | Verify login is refused when the data API takes longer than 10 seconds | Landing page | High | S2 | Integration |  | FR-08.1 errors; NFR Integration (10 s timeout); R8-AC23 |
| [`TC-R8-010`](#tc-r8-010) | `TS-001` | Verify login succeeds when the data API responds just under 10 seconds | Landing page > Home | Medium | S3 | Integration |  | NFR Integration (10 s timeout) - boundary |
| [`TC-R8-011`](#tc-r8-011) | `TS-001` | Verify login is refused when saving the refreshed data fails | Landing page | High | S2 | Integration |  | FR-08.1 rules ('Cập nhật lỗi: MSG-0809') |
| [`TC-R8-012`](#tc-r8-012) | `TS-001` | Verify father and mother both see the same children with the same rights | Home | High | S2 | Functional |  | FR-08.1 rules (D-19); R8-AC04; PB-07 |
| [`TC-R8-013`](#tc-r8-013) | `TS-001` | Verify each parent sees only children linked to their own NRIC | Home | Critical | S1 (highest) | Security |  | FR-08.1; sec. 4 permissions; PB-07 |
| [`TC-R8-014`](#tc-r8-014) | `TS-001` | Verify a student cannot use the e-Service Portal | Landing page | Medium | S3 | Security |  | Sec. 4 permissions (A-01) |
| [`TC-R8-015`](#tc-r8-015) | `TS-001` | Verify an MOE HQ or School user without children cannot use the e-Service Portal | Landing page | Low | S3 | Security |  | Sec. 4 permissions |
| [`TC-R8-016`](#tc-r8-016) | `TS-001` | Verify a protected page cannot be opened without logging in | Home / Education Account | Critical | S1 (highest) | Security |  | NFR Security; PB-06 AC (unauthenticated access blocked) |
| [`TC-R8-017`](#tc-r8-017) | `TS-001` | Verify protected APIs reject calls without a valid session | API | Critical | S1 (highest) | API |  | NFR Security; PB-06 |
| [`TC-R8-018`](#tc-r8-018) | `TS-002` | Verify parent name and residential address are refreshed from SingPass at login | My details | High | S2 | Functional |  | FR-08.1 rules (parent update); FS R8 Appendix A |
| [`TC-R8-019`](#tc-r8-019) | `TS-002` | Verify phone, email and mailing address are filled from the data API on first login | My details | High | S2 | Functional |  | FR-08.1 rules |
| [`TC-R8-020`](#tc-r8-020) | `TS-002` | Verify a phone number edited in My details is not overwritten at the next login | My details | High | S2 | Functional |  | FR-08.1 rules; R8-AC22 |
| [`TC-R8-021`](#tc-r8-021) | `TS-002` | Verify edited email and mailing address are not overwritten at the next login | My details | High | S2 | Functional |  | FR-08.1 rules; R8-AC22 |
| [`TC-R8-022`](#tc-r8-022) | `TS-002` | Verify contact fields never edited by the parent are not refreshed after first login | My details | Medium | S3 | Functional |  | FR-08.1 rules |
| [`TC-R8-023`](#tc-r8-023) | `TS-002` | Verify a change to a child's class in the data API appears after the parent logs in | Home | High | S2 | Functional |  | FR-08.1 rules (child update); R8-AC21 |
| [`TC-R8-024`](#tc-r8-024) | `TS-002` | Verify child name, DOB and citizenship are refreshed at login | Education Account | High | S2 | Functional |  | FR-08.1 rules (child update) |
| [`TC-R8-025`](#tc-r8-025) | `TS-002` | Verify a child no longer linked to the parent's NRIC is unlinked at login | Home | Critical | S1 (highest) | Security |  | FR-08.1 rules (unlink); NFR Security; PB-07 |
| [`TC-R8-026`](#tc-r8-026) | `TS-002` | Verify a newly linked child appears at the next login | Home | High | S2 | Functional |  | FR-08.1 rules |
| [`TC-R8-027`](#tc-r8-027) | `TS-002` | Verify there is no nightly refresh for a parent who does not log in | Database | Medium | S2 | Functional |  | FR-08.1 rules; NFR Integration; R8-AC24 |
| [`TC-R8-028`](#tc-r8-028) | `TS-002` | Verify the refresh at login only updates the logged-in parent and their children | Database | High | S2 | Functional |  | FR-08.1 rules |
| [`TC-R8-029`](#tc-r8-029) | `TS-002` | Verify 'Last updated' shows the time of the latest login refresh | Education Account | Medium | S3 | Functional |  | FR-08.2; FS R8 6.2 (Last updated) |
| [`TC-R8-030`](#tc-r8-030) | `TS-003` | Verify the session ends after 15 minutes of inactivity | Any page | High | S2 | Security |  | NFR session (D-22); R8-AC20 |
| [`TC-R8-031`](#tc-r8-031) | `TS-003` | Verify the session stays active after 14 minutes of inactivity | Any page | Medium | S3 | Security |  | NFR session (D-22) - boundary |
| [`TC-R8-032`](#tc-r8-032) | `TS-003` | Verify an expired session cannot save My details | My details | High | S2 | Functional |  | FR-08.3 errors; NFR session |
| [`TC-R8-033`](#tc-r8-033) | `TS-003` | Verify logout ends the session | Any page | High | S2 | Security |  | FS R8 sec. 3 step 9; NFR Security |
| [`TC-R8-034`](#tc-r8-034) | `TS-004` | Verify each linked child has a card with name, EA status, school and class | Home | High | S2 | UI |  | FS R8 6.1; R8-AC01 |
| [`TC-R8-035`](#tc-r8-035) | `TS-004` | Verify the EA balance is shown on the card for an Active account | Home | High | S2 | Functional |  | FS R8 6.1 (EA balance) |
| [`TC-R8-036`](#tc-r8-036) | `TS-004` | Verify the EA balance is shown on the card for a Due for closure account | Home | Medium | S3 | Functional |  | FS R8 6.1; 6.2 |
| [`TC-R8-037`](#tc-r8-037) | `TS-004` | Verify the balance is replaced by a status sentence for children without a usable EA | Home | High | S2 | Functional |  | FS R8 6.1; 6.2; R8-AC10 |
| [`TC-R8-038`](#tc-r8-038) | `TS-004` | Verify 'Need to pay' shows total outstanding fees after subsidy | Home | High | S2 | Functional |  | FS R8 6.1 (Need to pay) |
| [`TC-R8-039`](#tc-r8-039) | `TS-004` | Verify the FAS label appears only for a Granted FAS | Home | Medium | S3 | Functional |  | FS R8 6.1 (FAS label) |
| [`TC-R8-040`](#tc-r8-040) | `TS-004` | Verify the card lists at most 3 outstanding fees sorted by nearest due date | Home | Medium | S3 | Functional |  | FS R8 6.1 (fee list) - boundary 3 |
| [`TC-R8-041`](#tc-r8-041) | `TS-004` | Verify '+N more' appears when there are more than 3 outstanding fees | Home | Medium | S3 | Functional |  | FS R8 6.1; R8-AC19 |
| [`TC-R8-042`](#tc-r8-042) | `TS-004` | Verify 'Nothing to pay right now.' when there are no outstanding fees | Home | Low | S4 (lowest) | UI |  | FS R8 6.1 (fee list) |
| [`TC-R8-043`](#tc-r8-043) | `TS-004` | Verify fee status labels Overdue, Due soon and Not due yet | Home | Medium | S3 | Functional |  | FS R8 6.1 (fee status) |
| [`TC-R8-044`](#tc-r8-044) | `TS-004` | Verify clicking a card opens that child's Education Account | Home > Education Account | High | S2 | Functional |  | FS R8 6.1 |
| [`TC-R8-045`](#tc-r8-045) | `TS-004` | Verify [All fees] opens the fee list of that child | Home > Fees | Medium | S3 | Functional |  | FS R8 6.1 (All fees); FS-09 |
| [`TC-R8-046`](#tc-r8-046) | `TS-004` | Verify the [Apply for FAS] button is shown at the top of Home | Home | Low | S4 (lowest) | UI |  | FS R8 6.1 |
| [`TC-R8-047`](#tc-r8-047) | `TS-004` | Verify Active children are shown before children aged 16+ | Home | Medium | S3 | Functional |  | FS R8 6.1 order rules 1-2; R8-AC12 |
| [`TC-R8-048`](#tc-r8-048) | `TS-004` | Verify children of the same age are ordered by FAS application status | Home | Low | S4 (lowest) | Functional |  | FS R8 6.1 order rule 3 |
| [`TC-R8-049`](#tc-r8-049) | `TS-004` | Verify the child selector on the Education Account screen uses the same order as Home | Education Account | Low | S4 (lowest) | UI |  | FS R8 6.1 (same order for selector) |
| [`TC-R8-050`](#tc-r8-050) | `TS-004` | Verify the card position of children with Closed / To be created / Not yet 7 / Not eligible status | Home | Low | S4 (lowest) | Functional |  | FS R8 6.1 |
| [`TC-R8-051`](#tc-r8-051) | `TS-005` | Verify the account information block on the Education Account screen | Education Account | High | S2 | Functional |  | FR-08.2 main flow (1); R8-AC06 |
| [`TC-R8-052`](#tc-r8-052) | `TS-005` | Verify the EA code format | Education Account | Medium | S3 | Functional |  | FR-08.2 rules (EA code) |
| [`TC-R8-053`](#tc-r8-053) | `TS-005` | Verify opening date and expected closure date | Education Account | High | S2 | Functional |  | FR-08.2 rules (dates) |
| [`TC-R8-054`](#tc-r8-054) | `TS-005` | Verify opening and closure dates for a child born on 29/02 | Education Account | Low | S3 | Functional |  | FR-08.2 rules; FS R1 leap-year rule (F01-AC14, F02-AC15) |
| [`TC-R8-055`](#tc-r8-055) | `TS-005` | Verify Active status shows the closure date | Education Account | High | S2 | Functional |  | FS R8 6.2 (Active) |
| [`TC-R8-056`](#tc-r8-056) | `TS-005` | Verify a 16+ child with zero balance is closed when the parent opens the account | Education Account | Critical | S1 (highest) | Integration |  | FR-08.2; FS R1 F02-AC02; R8-AC26 |
| [`TC-R8-057`](#tc-r8-057) | `TS-005` | Verify Due for closure for a 16+ child whose account has a remaining balance | Education Account | High | S2 | Functional |  | FS R8 6.2 (Due for closure); R8-AC26; FS R1 F02-AC10 |
| [`TC-R8-058`](#tc-r8-058) | `TS-005` | Verify a Closed account shows transactions only | Education Account | High | S2 | Functional |  | FS R8 6.2 (Closed); FS R1 F02-AC07 |
| [`TC-R8-059`](#tc-r8-059) | `TS-005` | Verify 'To be created' for a citizen aged 7+ without an EA | Education Account | Medium | S3 | Functional |  | FS R8 6.2 (To be created) |
| [`TC-R8-060`](#tc-r8-060) | `TS-005` | Verify 'Not yet 7' shows the date the EA will open | Education Account | Medium | S3 | Functional |  | FS R8 6.2 (Not yet 7) |
| [`TC-R8-061`](#tc-r8-061) | `TS-005` | Verify 'Not eligible' for a non-citizen child | Education Account | High | S2 | Functional |  | FS R8 6.2 (Not eligible); R8-AC10 |
| [`TC-R8-062`](#tc-r8-062) | `TS-005` | Verify behaviour when the closure check cannot reach the Government API on view | Education Account | Medium | S2 | Integration |  | FS R1 F02-AC09, EF01 |
| [`TC-R8-063`](#tc-r8-063) | `TS-005` | Verify a child turning 16 tomorrow is still Active with full functions | Education Account | High | S2 | Functional |  | FR-08.2 rules (16-year rule) - boundary |
| [`TC-R8-064`](#tc-r8-064) | `TS-006` | Verify available balance counts only Completed transactions | Education Account | Critical | S1 (highest) | Functional |  | FR-08.2 rules (balance) |
| [`TC-R8-065`](#tc-r8-065) | `TS-006` | Verify a Pending transaction is shown separately and not deducted | Education Account | Critical | S1 (highest) | Functional |  | FR-08.2 rules; R8-AC25 |
| [`TC-R8-066`](#tc-r8-066) | `TS-006` | Verify money in and money out for the current year | Education Account | High | S2 | Functional |  | FR-08.2 main flow (2) - boundary year start |
| [`TC-R8-067`](#tc-r8-067) | `TS-006` | Verify amount format is SGD with 2 decimals and thousand separators | Education Account | Medium | S3 | UI |  | FR-08.2 rules; NFR display |
| [`TC-R8-068`](#tc-r8-068) | `TS-006` | Verify an account with zero balance and no transactions | Education Account | Medium | S3 | Functional |  | FR-08.2 |
| [`TC-R8-069`](#tc-r8-069) | `TS-007` | Verify the green FAS block for a Granted scheme | Education Account | Medium | S3 | Functional |  | FR-08.2 main flow (3); R8-AC27 |
| [`TC-R8-070`](#tc-r8-070) | `TS-007` | Verify 'Under review' label for an FAS being assessed | Education Account | Low | S4 (lowest) | Functional |  | FR-08.2 rules (FAS) |
| [`TC-R8-071`](#tc-r8-071) | `TS-007` | Verify the FAS block is hidden when the child has no FAS | Education Account | Low | S4 (lowest) | Functional |  | FR-08.2 rules (FAS); R8-AC27 |
| [`TC-R8-072`](#tc-r8-072) | `TS-008` | Verify the transaction table columns and newest-first order | Education Account | High | S2 | Functional |  | FR-08.2 main flow (4); FS R8 6.2; R8-AC06; R8-AC28 |
| [`TC-R8-073`](#tc-r8-073) | `TS-008` | Verify transaction reference format and type colours | Education Account | Medium | S3 | UI |  | FR-08.2 rules; R8-AC28 |
| [`TC-R8-074`](#tc-r8-074) | `TS-008` | Verify amount signs and colours for money in and money out | Education Account | Medium | S3 | UI |  | FR-08.2 rules; FS R8 6.2 (Amount) |
| [`TC-R8-075`](#tc-r8-075) | `TS-008` | Verify 'Balance after' for Completed and Failed transactions | Education Account | Medium | S3 | Functional |  | FR-08.2 rules; FS R1 2.3 (failed transaction) |
| [`TC-R8-076`](#tc-r8-076) | `TS-008` | Verify an online payment shows amount and 'online' without changing the EA balance | Education Account | Critical | S1 (highest) | Functional |  | FS R8 6.2 (Amount); test plan 3.9 (online payment must not debit EA) |
| [`TC-R8-077`](#tc-r8-077) | `TS-008` | Verify a Pending online payment shows [Continue payment] | Education Account | Medium | S3 | Functional |  | FS R8 6.2 (Status) |
| [`TC-R8-078`](#tc-r8-078) | `TS-008` | Verify [View fee] on a Fee payment opens that child's Fees page | Education Account > Fees | Medium | S3 | Functional |  | FR-08.2 rules; R8-AC28 |
| [`TC-R8-079`](#tc-r8-079) | `TS-008` | Verify pagination with 21 transactions | Education Account | Medium | S3 | Functional |  | FS R8 6.2 (20 rows per page) - boundary |
| [`TC-R8-080`](#tc-r8-080) | `TS-008` | Verify a single page with exactly 20 transactions | Education Account | Low | S4 (lowest) | Functional |  | FS R8 6.2 (pagination) - boundary |
| [`TC-R8-081`](#tc-r8-081) | `TS-008` | Verify filter by type Refund | Education Account | Medium | S3 | Functional |  | FR-08.2 (filter); R8-AC28 |
| [`TC-R8-082`](#tc-r8-082) | `TS-008` | Verify filter by each transaction type | Education Account | Medium | S3 | Functional |  | FS R8 6.2 (filter Type) |
| [`TC-R8-083`](#tc-r8-083) | `TS-008` | Verify filter by money flow | Education Account | Medium | S3 | Functional |  | FS R8 6.2 (filter Money flow) |
| [`TC-R8-084`](#tc-r8-084) | `TS-008` | Verify the date range filter includes the From and To dates | Education Account | Medium | S3 | Functional |  | FS R8 6.2 (filter From/To) - boundary |
| [`TC-R8-085`](#tc-r8-085) | `TS-008` | Verify the filter rejects From later than To | Education Account | Low | S4 (lowest) | Functional |  | FS R8 6.2 (filter) |
| [`TC-R8-086`](#tc-r8-086) | `TS-008` | Verify a filter with no results shows MSG-0803 | Education Account | Medium | S3 | Functional |  | FR-08.2 errors; R8-AC11 |
| [`TC-R8-087`](#tc-r8-087) | `TS-008` | Verify filters apply only after clicking [Apply filter] | Education Account | Low | S4 (lowest) | UI |  | FS R8 6.2 (Apply filter) |
| [`TC-R8-088`](#tc-r8-088) | `TS-008` | Verify combined date, type and money flow filters | Education Account | Medium | S3 | Functional |  | FS R8 6.2 (filter) |
| [`TC-R8-089`](#tc-r8-089) | `TS-008` | Verify the All view for a parent with several children | Education Account | High | S2 | Functional |  | FS R8 6.2 (Nhiều con) |
| [`TC-R8-090`](#tc-r8-090) | `TS-008` | Verify the All view does not include other families' transactions | Education Account | Critical | S1 (highest) | Security |  | NFR Security; PB-07 |
| [`TC-R8-091`](#tc-r8-091) | `TS-009` | Verify only the child who turned 16 becomes view-only | Home / Education Account | Critical | S1 (highest) | Functional |  | FR-08.2 rules (per-child rule); R8-AC07 |
| [`TC-R8-092`](#tc-r8-092) | `TS-009` | Verify a 16-year-old child's information remains viewable | Home / Education Account / Fees / My details | High | S2 | Functional |  | FS R8 sec. 3 step 7; R8-AC08 |
| [`TC-R8-093`](#tc-r8-093) | `TS-009` | Verify payment for a 16+ child is rejected by the API | API | Critical | S1 (highest) | Security |  | FR-08.2 rules; FS R1 F02-AC05 |
| [`TC-R8-094`](#tc-r8-094) | `TS-010` | Verify My details shows the parent's information with read-only fields | My details | High | S2 | UI |  | FR-08.3; FS R8 sec. 6 field table |
| [`TC-R8-095`](#tc-r8-095) | `TS-010` | Verify residential address cannot be edited | My details | High | S2 | Functional |  | FR-08.3 rules (D-20); R8-AC18 |
| [`TC-R8-096`](#tc-r8-096) | `TS-010` | Verify the API ignores or rejects changes to read-only fields | API | High | S1 (highest) | Security |  | FR-08.3 rules; NFR Security |
| [`TC-R8-097`](#tc-r8-097) | `TS-010` | Verify saving valid phone, email and mailing address | My details | Critical | S1 (highest) | Functional |  | FR-08.3; R8-AC14; US-08.2; PB-15 |
| [`TC-R8-098`](#tc-r8-098) | `TS-010` | Verify mobile numbers starting with 6, 8 and 9 are accepted | My details | Medium | S3 | Functional |  | FS R8 field table (Mobile) - equivalence partitioning |
| [`TC-R8-099`](#tc-r8-099) | `TS-010` | Verify invalid mobile numbers are rejected with MSG-0805 | My details | High | S2 | Functional |  | FR-08.3 errors; R8-AC15 |
| [`TC-R8-100`](#tc-r8-100) | `TS-010` | Verify a mobile number entered with a space | My details | Low | S4 (lowest) | Functional |  | FS R8 field table (example format) |
| [`TC-R8-101`](#tc-r8-101) | `TS-010` | Verify invalid email formats are rejected with MSG-0806 | My details | High | S2 | Functional |  | FR-08.3 errors; R8-AC15 |
| [`TC-R8-102`](#tc-r8-102) | `TS-010` | Verify email length limit of 150 characters | My details | Medium | S3 | Functional |  | FS R8 field table (Email max 150) - boundary |
| [`TC-R8-103`](#tc-r8-103) | `TS-010` | Verify each blank required field shows MSG-0001 | My details | High | S2 | Functional |  | FR-08.3 errors; R8-AC16 |
| [`TC-R8-104`](#tc-r8-104) | `TS-010` | Verify whitespace-only input is treated as blank | My details | Low | S4 (lowest) | Functional |  | FR-08.3 errors |
| [`TC-R8-105`](#tc-r8-105) | `TS-010` | Verify optional mailing block and unit can be left blank | My details | Low | S4 (lowest) | Functional |  | FS R8 field table (block, unit optional) |
| [`TC-R8-106`](#tc-r8-106) | `TS-010` | Verify mailing block and unit length limit of 20 characters | My details | Low | S4 (lowest) | Functional |  | FS R8 field table - boundary |
| [`TC-R8-107`](#tc-r8-107) | `TS-010` | Verify mailing street and country length limit of 100 characters | My details | Low | S4 (lowest) | Functional |  | FS R8 field table - boundary |
| [`TC-R8-108`](#tc-r8-108) | `TS-010` | Verify mailing postal code must be exactly 6 digits | My details | Medium | S3 | Functional |  | FS R8 field table (postal code) |
| [`TC-R8-109`](#tc-r8-109) | `TS-010` | Verify a system error on save shows MSG-0808 and keeps the old data | My details | High | S2 | Functional |  | FR-08.3 errors; R8-AC17 |
| [`TC-R8-110`](#tc-r8-110) | `TS-010` | Verify My details is view-only when all children are 16+ | My details | High | S2 | Functional |  | FR-08.3 precondition; R8-AC09 |
| [`TC-R8-111`](#tc-r8-111) | `TS-010` | Verify My details is editable when at least one child is under 16 | My details | Medium | S3 | Functional |  | FR-08.3 precondition |
| [`TC-R8-112`](#tc-r8-112) | `TS-010` | Verify a parent cannot update another parent's profile via the API | API | Critical | S1 (highest) | Security |  | FR-08.3 rules (own data only); NFR Security |
| [`TC-R8-113`](#tc-r8-113) | `TS-010` | Verify father's update does not change mother's details | My details | Medium | S2 | Functional |  | FR-08.3 rules |
| [`TC-R8-114`](#tc-r8-114) | `TS-010` | Verify script input in mailing fields is not executed | My details | Medium | S2 | Security |  | NFR Security |
| [`TC-R8-115`](#tc-r8-115) | `TS-011` | Verify opening the Education Account of a child not linked to the parent | Education Account | Critical | S1 (highest) | Security |  | FR-08.2 errors; NFR Security; R8-AC13; PB-07 |
| [`TC-R8-116`](#tc-r8-116) | `TS-011` | Verify EA and transaction APIs block access to unlinked children | API | Critical | S1 (highest) | Security |  | NFR Security (server-side checks); PB-07 |
| [`TC-R8-117`](#tc-r8-117) | `TS-011` | Verify the full NRIC never appears in URLs | All pages | High | S2 | Security |  | NFR Security |
| [`TC-R8-118`](#tc-r8-118) | `TS-011` | Verify application logs and error messages do not expose personal data | Logs | High | S2 | Security |  | Test plan 3.8 (safe logs); NFR Security |
| [`TC-R8-119`](#tc-r8-119) | `TS-012` | Verify a login is recorded in the audit log | Audit log | High | S2 | Functional |  | NFR Audit |
| [`TC-R8-120`](#tc-r8-120) | `TS-012` | Verify each data update from the API at login is audited | Audit log | High | S2 | Functional |  | FR-08.1 rules; NFR Audit |
| [`TC-R8-121`](#tc-r8-121) | `TS-012` | Verify a My details change is audited with old and new values | Audit log | High | S2 | Functional |  | FR-08.3; FS R8 Appendix A; NFR Audit; R8-AC14 |
| [`TC-R8-122`](#tc-r8-122) | `TS-013` | Verify Home loads within 3 seconds with 1,000 transactions | Home | Medium | S2 | Performance |  | NFR Performance |
| [`TC-R8-123`](#tc-r8-123) | `TS-013` | Verify Education Account loads within 3 seconds with 1,000 transactions | Education Account | Medium | S2 | Performance |  | NFR Performance |
| [`TC-R8-124`](#tc-r8-124) | `TS-013` | Verify Home, Education Account and My details are usable on a phone | Home / Education Account / My details | Medium | S3 | UI |  | NFR Display |
| [`TC-R8-125`](#tc-r8-125) | `TS-013` | Verify interface language and display formats | All pages | Low | S4 (lowest) | UI |  | NFR Display; FR-08.2 rules |

---

## Detailed Test Case Specifications


### Test Suite: SingPass Login

#### `TC-R8-001`: Verify Landing page shows the 'Log in with SingPass' button

- **Scenario ID**: `TS-001`
- **Test Suite**: SingPass Login
- **Page / Target**: `Landing page`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `UI`
- **Traceability**: FR-08.1; FS R8 sec. 6; US-08.1; PB-06
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
User is not logged in
```

**Test Data:**
```text
N/A
```

**Test Steps:**
1. Open the e-Service Portal URL
2. Observe the Landing page

**Expected Result:**
> Landing page is shown with the 'Log in with SingPass' button; no child or account data is shown

---

#### `TC-R8-002`: Verify first-time SingPass login creates a parent account and opens Home

- **Scenario ID**: `TS-001`
- **Test Suite**: SingPass Login
- **Page / Target**: `Landing page > Home`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FR-08.1 steps 1-5; R8-AC01; US-08.1; PB-06; PB-07
- **Environment**: SIT
Chrome (latest) + DB read access
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
Father FA has never logged in (no Parent_Profile row for S7000001A)
Data API returns FA and children A1, A2
```

**Test Data:**
```text
Father FA: NRIC S7000001A, Tan Wei Ming
Mother MA: NRIC S7000002B, Lim Mei Ling
Child A1: Tan Jia Hui, citizen, age 12, EA Active, balance S$250.00, BVP / P6 Integrity
Child A2: Tan Jun Kai, citizen, age 9, EA Active, balance S$80.00, BVP / P3 Harmony
```

**Test Steps:**
1. Open the Landing page
2. Click [Log in with SingPass]
3. Authenticate as FA in mock SingPass
4. Observe the page after redirect
5. Check Parent_Profile for NRIC S7000001A

**Expected Result:**
> Home is shown with one card for A1 and one card for A2
> One Parent_Profile row exists with a UserId and IsActivate = true
> A1 and A2 are linked to FA
> Parent and child data are stored from the data API

---

#### `TC-R8-003`: Verify a returning parent reuses the existing account

- **Scenario ID**: `TS-001`
- **Test Suite**: SingPass Login
- **Page / Target**: `Landing page > Home`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FR-08.1 step 3; R8-AC02; PB-06
- **Environment**: SIT
Chrome (latest) + DB read access
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
FA has logged in before (Parent_Profile exists, UserId recorded)
```

**Test Data:**
```text
Father FA: NRIC S7000001A, Tan Wei Ming
Mother MA: NRIC S7000002B, Lim Mei Ling
Child A1: Tan Jia Hui, citizen, age 12, EA Active, balance S$250.00, BVP / P6 Integrity
Child A2: Tan Jun Kai, citizen, age 9, EA Active, balance S$80.00, BVP / P3 Harmony
```

**Test Steps:**
1. Note FA's UserId and the Parent_Profile row count for S7000001A
2. Log out
3. Log in again via SingPass as FA
4. Re-check Parent_Profile

**Expected Result:**
> Login succeeds and Home is shown
> Same UserId; still exactly one Parent_Profile row for S7000001A; no duplicate child links

---

#### `TC-R8-004`: Verify cancelling SingPass returns to Landing with MSG-0802

- **Scenario ID**: `TS-001`
- **Test Suite**: SingPass Login
- **Page / Target**: `Landing page`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FR-08.1 errors; R8-AC05; PB-06
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
User is not logged in
```

**Test Data:**
```text
Any mock SingPass identity
```

**Test Steps:**
1. Click [Log in with SingPass]
2. Click [Cancel] on the mock SingPass page

**Expected Result:**
> User is returned to the Landing page
> MSG-0802 'Login was not completed. Try again.' is shown
> No session is created

---

#### `TC-R8-005`: Verify a SingPass authentication error returns to Landing with MSG-0802

- **Scenario ID**: `TS-001`
- **Test Suite**: SingPass Login
- **Page / Target**: `Landing page`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: FR-08.1 errors; R8-AC05; PB-06
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
Mock SingPass configured to return an error on callback
```

**Test Data:**
```text
Mock SingPass error response
```

**Test Steps:**
1. Click [Log in with SingPass]
2. Complete login on mock SingPass (mock returns an error)

**Expected Result:**
> User is returned to the Landing page with MSG-0802
> No session; no Parent_Profile created or changed

---

#### `TC-R8-006`: Verify login is refused when the NRIC is not found in the data API

- **Scenario ID**: `TS-001`
- **Test Suite**: SingPass Login
- **Page / Target**: `Landing page`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FR-08.1 rules; R8-AC03; PB-07
- **Environment**: SIT
Chrome (latest) + DB read access
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
NRIC S7999999Z exists in mock SingPass but not in the data API
```

**Test Data:**
```text
NRIC: S7999999Z
```

**Test Steps:**
1. Click [Log in with SingPass]
2. Authenticate as S7999999Z
3. Check Parent_Profile

**Expected Result:**
> MSG-0801 'We could not find any student linked to your account. Please contact your child's school.' is shown
> User cannot enter the portal; no Parent_Profile row created

---

#### `TC-R8-007`: Verify login is refused when the parent has no linked child

- **Scenario ID**: `TS-001`
- **Test Suite**: SingPass Login
- **Page / Target**: `Landing page`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FR-08.1 rules; R8-AC03; PB-07
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
Parent S7000009H exists in the data API; no student has this NRIC as FatherNric/MotherNric
```

**Test Data:**
```text
NRIC: S7000009H
```

**Test Steps:**
1. Log in via SingPass as S7000009H

**Expected Result:**
> MSG-0801 is shown
> User cannot enter the portal; no session is created

---

#### `TC-R8-008`: Verify login is refused when the data API returns an error

- **Scenario ID**: `TS-001`
- **Test Suite**: SingPass Login
- **Page / Target**: `Landing page`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: FR-08.1 errors; R8-AC23
- **Environment**: SIT
Chrome (latest) + DB read access
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
FA has logged in before; mock data API configured to return HTTP 500
```

**Test Data:**
```text
Father FA: NRIC S7000001A, Tan Wei Ming
Mother MA: NRIC S7000002B, Lim Mei Ling
Child A1: Tan Jia Hui, citizen, age 12, EA Active, balance S$250.00, BVP / P6 Integrity
Child A2: Tan Jun Kai, citizen, age 9, EA Active, balance S$80.00, BVP / P3 Harmony
```

**Test Steps:**
1. Note FA's Parent_Profile and A1/A2 data
2. Log in via SingPass as FA
3. Re-check the data

**Expected Result:**
> MSG-0809 'We could not retrieve your information. Please try again later.' is shown
> User cannot enter the portal
> Parent and child data are unchanged

---

#### `TC-R8-009`: Verify login is refused when the data API takes longer than 10 seconds

- **Scenario ID**: `TS-001`
- **Test Suite**: SingPass Login
- **Page / Target**: `Landing page`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: FR-08.1 errors; NFR Integration (10 s timeout); R8-AC23
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
Mock data API configured to respond after 11 seconds
```

**Test Data:**
```text
Father FA: NRIC S7000001A, Tan Wei Ming
Mother MA: NRIC S7000002B, Lim Mei Ling
Child A1: Tan Jia Hui, citizen, age 12, EA Active, balance S$250.00, BVP / P6 Integrity
Child A2: Tan Jun Kai, citizen, age 9, EA Active, balance S$80.00, BVP / P3 Harmony
API delay: 11 s
```

**Test Steps:**
1. Log in via SingPass as FA
2. Measure time until a message is shown

**Expected Result:**
> Request times out at about 10 seconds
> MSG-0809 is shown; user cannot enter; data unchanged

---

#### `TC-R8-010`: Verify login succeeds when the data API responds just under 10 seconds

- **Scenario ID**: `TS-001`
- **Test Suite**: SingPass Login
- **Page / Target**: `Landing page > Home`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: NFR Integration (10 s timeout) - boundary
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API
- **Note**: Boundary pair with the 11 s timeout case

**Preconditions:**
```text
Mock data API configured to respond after 9 seconds
```

**Test Data:**
```text
Father FA: NRIC S7000001A, Tan Wei Ming
Mother MA: NRIC S7000002B, Lim Mei Ling
Child A1: Tan Jia Hui, citizen, age 12, EA Active, balance S$250.00, BVP / P6 Integrity
Child A2: Tan Jun Kai, citizen, age 9, EA Active, balance S$80.00, BVP / P3 Harmony
API delay: 9 s
```

**Test Steps:**
1. Log in via SingPass as FA

**Expected Result:**
> Login completes and Home is shown; no MSG-0809

---

#### `TC-R8-011`: Verify login is refused when saving the refreshed data fails

- **Scenario ID**: `TS-001`
- **Test Suite**: SingPass Login
- **Page / Target**: `Landing page`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: FR-08.1 rules ('Cập nhật lỗi: MSG-0809')
- **Environment**: SIT
Chrome (latest) + DB read access
Build: TBC
Mock SingPass + mock data API
- **Note**: Needs Dev support for fault injection

**Preconditions:**
```text
FA has logged in before; DB write for the login data update is forced to fail (fault injection)
```

**Test Data:**
```text
Father FA: NRIC S7000001A, Tan Wei Ming
Mother MA: NRIC S7000002B, Lim Mei Ling
Child A1: Tan Jia Hui, citizen, age 12, EA Active, balance S$250.00, BVP / P6 Integrity
Child A2: Tan Jun Kai, citizen, age 9, EA Active, balance S$80.00, BVP / P3 Harmony
```

**Test Steps:**
1. Note FA's Parent_Profile and A1/A2 data
2. Log in via SingPass as FA
3. Re-check the data

**Expected Result:**
> MSG-0809 is shown; user cannot enter the portal
> No partial update: parent and child data are unchanged

---

#### `TC-R8-012`: Verify father and mother both see the same children with the same rights

- **Scenario ID**: `TS-001`
- **Test Suite**: SingPass Login
- **Page / Target**: `Home`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FR-08.1 rules (D-19); R8-AC04; PB-07
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
A1 and A2 have FatherNric = S7000001A and MotherNric = S7000002B
```

**Test Data:**
```text
Father FA: NRIC S7000001A, Tan Wei Ming
Mother MA: NRIC S7000002B, Lim Mei Ling
Child A1: Tan Jia Hui, citizen, age 12, EA Active, balance S$250.00, BVP / P6 Integrity
Child A2: Tan Jun Kai, citizen, age 9, EA Active, balance S$80.00, BVP / P3 Harmony
```

**Test Steps:**
1. Log in as FA and note the cards and actions on Home and EA screens
2. Log out
3. Log in as MA and compare

**Expected Result:**
> FA and MA both see A1 and A2 with the same data and the same available actions

---

#### `TC-R8-013`: Verify each parent sees only children linked to their own NRIC

- **Scenario ID**: `TS-001`
- **Test Suite**: SingPass Login
- **Page / Target**: `Home`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Security`
- **Traceability**: FR-08.1; sec. 4 permissions; PB-07
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
Child C3 has FatherNric = S7000001A but a different MotherNric (S7000005E)
```

**Test Data:**
```text
Father FA: NRIC S7000001A, Tan Wei Ming
Mother MA: NRIC S7000002B, Lim Mei Ling
Child A1: Tan Jia Hui, citizen, age 12, EA Active, balance S$250.00, BVP / P6 Integrity
Child A2: Tan Jun Kai, citizen, age 9, EA Active, balance S$80.00, BVP / P3 Harmony
Child C3: Tan Kai Wen, age 10, FatherNric S7000001A, MotherNric S7000005E
```

**Test Steps:**
1. Log in as FA and list the cards
2. Log out
3. Log in as MA and list the cards

**Expected Result:**
> FA sees A1, A2 and C3
> MA sees A1 and A2 only; C3 is not shown to MA

---

#### `TC-R8-014`: Verify a student cannot use the e-Service Portal

- **Scenario ID**: `TS-001`
- **Test Suite**: SingPass Login
- **Page / Target**: `Landing page`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Security`
- **Traceability**: Sec. 4 permissions (A-01)
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
Student A1 has an NRIC in mock SingPass; A1 is not a parent of any student
```

**Test Data:**
```text
NRIC of A1: T1400001A
```

**Test Steps:**
1. Log in via SingPass with A1's NRIC

**Expected Result:**
> MSG-0801 is shown; no access to the portal

---

#### `TC-R8-015`: Verify an MOE HQ or School user without children cannot use the e-Service Portal

- **Scenario ID**: `TS-001`
- **Test Suite**: SingPass Login
- **Page / Target**: `Landing page`
- **Severity / Priority**: `S3` / `Low`
- **Execution Status**: `Not Run` | **Test Type**: `Security`
- **Traceability**: Sec. 4 permissions
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
HQ user identity S7000010K has no linked child in the data API
```

**Test Data:**
```text
NRIC: S7000010K
```

**Test Steps:**
1. Log in via SingPass as S7000010K

**Expected Result:**
> MSG-0801 is shown; no access to the e-Service Portal

---

#### `TC-R8-016`: Verify a protected page cannot be opened without logging in

- **Scenario ID**: `TS-001`
- **Test Suite**: SingPass Login
- **Page / Target**: `Home / Education Account`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Security`
- **Traceability**: NFR Security; PB-06 AC (unauthenticated access blocked)
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API
- **Assumption Reference**: ASM-17: Unauthenticated access to a protected page redirects to the Landing page; protected APIs return 401.

**Preconditions:**
```text
No active session
```

**Test Data:**
```text
URLs of Home, Education Account and My details
```

**Test Steps:**
1. In a new private window, open the Home URL directly
2. Repeat for the Education Account and My details URLs

**Expected Result:**
> Each request redirects to the Landing page; no parent or child data is shown

---

#### `TC-R8-017`: Verify protected APIs reject calls without a valid session

- **Scenario ID**: `TS-001`
- **Test Suite**: SingPass Login
- **Page / Target**: `API`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `API`
- **Traceability**: NFR Security; PB-06
- **Environment**: SIT
API client (Postman) + Chrome DevTools
Build: TBC
Mock SingPass + mock data API
- **Assumption Reference**: ASM-17: Unauthenticated access to a protected page redirects to the Landing page; protected APIs return 401.

**Preconditions:**
```text
No session token
```

**Test Data:**
```text
Endpoints: parent profile, children list, EA details, transactions
```

**Test Steps:**
1. Call each endpoint without a token
2. Call each endpoint with an expired or tampered token

**Expected Result:**
> Every call returns 401 with no data in the response body

---


### Test Suite: Login Data Refresh

#### `TC-R8-018`: Verify parent name and residential address are refreshed from SingPass at login

- **Scenario ID**: `TS-002`
- **Test Suite**: Login Data Refresh
- **Page / Target**: `My details`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FR-08.1 rules (parent update); FS R8 Appendix A
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
FA has logged in before; mock SingPass now returns a new residential address
```

**Test Data:**
```text
Old: Blk 214 Bukit Verde Ave 4, #08-102, 650214
New: Blk 88 Marina Crest Rd, #03-15, 440088
```

**Test Steps:**
1. Log in as FA
2. Open My details

**Expected Result:**
> Residential address shows the new value; full name matches SingPass
> Audit log records the update

---

#### `TC-R8-019`: Verify phone, email and mailing address are filled from the data API on first login

- **Scenario ID**: `TS-002`
- **Test Suite**: Login Data Refresh
- **Page / Target**: `My details`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FR-08.1 rules
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API
- **Assumption Reference**: ASM-02: Phone, email and mailing address are taken from the data API only on first login; later logins never overwrite them (edited or not). FS R8 wording is ambiguous for values the parent never edited; confirm with BA.

**Preconditions:**
```text
FA has never logged in; data API returns phone, email and mailing address
```

**Test Data:**
```text
Phone 91234567; email weiming.tan@example.sg; mailing Blk 214 Bukit Verde Ave 4, #08-102, 650214, Singapore
```

**Test Steps:**
1. Log in as FA for the first time
2. Open My details

**Expected Result:**
> Phone, email and mailing address show the values from the data API

---

#### `TC-R8-020`: Verify a phone number edited in My details is not overwritten at the next login

- **Scenario ID**: `TS-002`
- **Test Suite**: Login Data Refresh
- **Page / Target**: `My details`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FR-08.1 rules; R8-AC22
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
FA changed phone to 98887777 in My details; data API still returns 91234567
```

**Test Data:**
```text
Edited phone: 98887777
API phone: 91234567
```

**Test Steps:**
1. Log out
2. Log in again as FA
3. Open My details

**Expected Result:**
> Phone is still 98887777

---

#### `TC-R8-021`: Verify edited email and mailing address are not overwritten at the next login

- **Scenario ID**: `TS-002`
- **Test Suite**: Login Data Refresh
- **Page / Target**: `My details`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FR-08.1 rules; R8-AC22
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
FA edited email and mailing street in My details; data API returns different values
```

**Test Data:**
```text
Edited email: fa.new@example.sg; edited street: 9 Verde Walk
API values: weiming.tan@example.sg; Bukit Verde Ave 4
```

**Test Steps:**
1. Log out
2. Log in again as FA
3. Open My details

**Expected Result:**
> Email and mailing address keep the edited values

---

#### `TC-R8-022`: Verify contact fields never edited by the parent are not refreshed after first login

- **Scenario ID**: `TS-002`
- **Test Suite**: Login Data Refresh
- **Page / Target**: `My details`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FR-08.1 rules
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API
- **Assumption Reference**: ASM-02: Phone, email and mailing address are taken from the data API only on first login; later logins never overwrite them (edited or not). FS R8 wording is ambiguous for values the parent never edited; confirm with BA.
- **Note**: Expected result depends on BA answer to ASM-02

**Preconditions:**
```text
FA has logged in before and never edited email; data API now returns a different email
```

**Test Data:**
```text
Stored email: weiming.tan@example.sg
New API email: wm.tan@example.sg
```

**Test Steps:**
1. Log in as FA
2. Open My details

**Expected Result:**
> Email remains weiming.tan@example.sg

---

#### `TC-R8-023`: Verify a change to a child's class in the data API appears after the parent logs in

- **Scenario ID**: `TS-002`
- **Test Suite**: Login Data Refresh
- **Page / Target**: `Home`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FR-08.1 rules (child update); R8-AC21
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API
- **Assumption Reference**: ASM-01: FS R8 FR-08.1 refreshes child name, school, class, DOB, citizenship at each login. FS R1 v1.2 (sec. 3) says R8 only verifies the parent-student relationship and does not run a full student sync; the Government dataset has no school/class. Test follows FS R8; confirm with BA.

**Preconditions:**
```text
A1 class changed from P6 Integrity to P6 Harmony in the data API
```

**Test Data:**
```text
Father FA: NRIC S7000001A, Tan Wei Ming
Mother MA: NRIC S7000002B, Lim Mei Ling
Child A1: Tan Jia Hui, citizen, age 12, EA Active, balance S$250.00, BVP / P6 Integrity
Child A2: Tan Jun Kai, citizen, age 9, EA Active, balance S$80.00, BVP / P3 Harmony
```

**Test Steps:**
1. Log in as FA
2. View A1's card on Home and A1's Education Account

**Expected Result:**
> A1 shows class P6 Harmony on Home and on the Education Account screen

---

#### `TC-R8-024`: Verify child name, DOB and citizenship are refreshed at login

- **Scenario ID**: `TS-002`
- **Test Suite**: Login Data Refresh
- **Page / Target**: `Education Account`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FR-08.1 rules (child update)
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API
- **Assumption Reference**: ASM-01: FS R8 FR-08.1 refreshes child name, school, class, DOB, citizenship at each login. FS R1 v1.2 (sec. 3) says R8 only verifies the parent-student relationship and does not run a full student sync; the Government dataset has no school/class. Test follows FS R8; confirm with BA.

**Preconditions:**
```text
Data API has a new full name for A2
```

**Test Data:**
```text
A2 new name: Tan Jun Kai Marcus
```

**Test Steps:**
1. Log in as FA
2. Open A2's Education Account

**Expected Result:**
> Student information shows the new name; DOB and citizenship match the data API
> Audit log records the update

---

#### `TC-R8-025`: Verify a child no longer linked to the parent's NRIC is unlinked at login

- **Scenario ID**: `TS-002`
- **Test Suite**: Login Data Refresh
- **Page / Target**: `Home`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Security`
- **Traceability**: FR-08.1 rules (unlink); NFR Security; PB-07
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
A2's FatherNric changed in the data API to a different NRIC
```

**Test Data:**
```text
Father FA: NRIC S7000001A, Tan Wei Ming
Mother MA: NRIC S7000002B, Lim Mei Ling
Child A1: Tan Jia Hui, citizen, age 12, EA Active, balance S$250.00, BVP / P6 Integrity
Child A2: Tan Jun Kai, citizen, age 9, EA Active, balance S$80.00, BVP / P3 Harmony
```

**Test Steps:**
1. Note A2's EA URL while logged in as FA
2. Log out, apply the API change, log in as FA
3. View Home
4. Open the saved A2 URL

**Expected Result:**
> A2's card is no longer on Home
> Opening A2's URL shows MSG-0003 'You do not have permission to perform this action.' and no data

---

#### `TC-R8-026`: Verify a newly linked child appears at the next login

- **Scenario ID**: `TS-002`
- **Test Suite**: Login Data Refresh
- **Page / Target**: `Home`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FR-08.1 rules
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
New child A3 (age 7, citizen) added in the data API with FatherNric S7000001A
```

**Test Data:**
```text
Father FA: NRIC S7000001A, Tan Wei Ming
Mother MA: NRIC S7000002B, Lim Mei Ling
Child A1: Tan Jia Hui, citizen, age 12, EA Active, balance S$250.00, BVP / P6 Integrity
Child A2: Tan Jun Kai, citizen, age 9, EA Active, balance S$80.00, BVP / P3 Harmony
Child A3: Tan Mei Xin, age 7
```

**Test Steps:**
1. Log in as FA
2. View Home

**Expected Result:**
> A3's card is shown in addition to A1 and A2

---

#### `TC-R8-027`: Verify there is no nightly refresh for a parent who does not log in

- **Scenario ID**: `TS-002`
- **Test Suite**: Login Data Refresh
- **Page / Target**: `Database`
- **Severity / Priority**: `S2` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FR-08.1 rules; NFR Integration; R8-AC24
- **Environment**: SIT
Chrome (latest) + DB read access
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
FA logged in on day D; on day D the data API changes A1's class and FA's name; FA does not log in
```

**Test Data:**
```text
Father FA: NRIC S7000001A, Tan Wei Ming
Mother MA: NRIC S7000002B, Lim Mei Ling
Child A1: Tan Jia Hui, citizen, age 12, EA Active, balance S$250.00, BVP / P6 Integrity
Child A2: Tan Jun Kai, citizen, age 9, EA Active, balance S$80.00, BVP / P3 Harmony
```

**Test Steps:**
1. On day D+1, check A1 and FA data in the database (FA has not logged in)
2. Log in as FA
3. Check the data again

**Expected Result:**
> On D+1 before login the data is unchanged
> After FA logs in the data is updated

---

#### `TC-R8-028`: Verify the refresh at login only updates the logged-in parent and their children

- **Scenario ID**: `TS-002`
- **Test Suite**: Login Data Refresh
- **Page / Target**: `Database`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FR-08.1 rules
- **Environment**: SIT
Chrome (latest) + DB read access
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
Parent PB (S7000003C) with child B2 has newer data in the API; FA logs in
```

**Test Data:**
```text
Parent PB: NRIC S7000003C
Child B2: age 14
```

**Test Steps:**
1. Change PB and B2 data in the API
2. Log in as FA
3. Check PB and B2 rows in the database

**Expected Result:**
> PB and B2 rows are unchanged; only FA, A1 and A2 are refreshed

---

#### `TC-R8-029`: Verify 'Last updated' shows the time of the latest login refresh

- **Scenario ID**: `TS-002`
- **Test Suite**: Login Data Refresh
- **Page / Target**: `Education Account`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FR-08.2; FS R8 6.2 (Last updated)
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API
- **Assumption Reference**: ASM-24: 'Last updated' = time of the latest login data update for this parent (FS R8 6.2). May change if ASM-01 is revised.

**Preconditions:**
```text
FA logs in at a known time
```

**Test Data:**
```text
Father FA: NRIC S7000001A, Tan Wei Ming
Mother MA: NRIC S7000002B, Lim Mei Ling
Child A1: Tan Jia Hui, citizen, age 12, EA Active, balance S$250.00, BVP / P6 Integrity
Child A2: Tan Jun Kai, citizen, age 9, EA Active, balance S$80.00, BVP / P3 Harmony
```

**Test Steps:**
1. Log in as FA at 14/10/2026 09:15
2. Open A1's Education Account
3. Read 'Last updated'

**Expected Result:**
> Last updated' shows 14/10/2026 09:15 (DD/MM/YYYY HH:mm, Singapore time)

---


### Test Suite: Session

#### `TC-R8-030`: Verify the session ends after 15 minutes of inactivity

- **Scenario ID**: `TS-003`
- **Test Suite**: Session
- **Page / Target**: `Any page`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Security`
- **Traceability**: NFR session (D-22); R8-AC20
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
FA logged in on Home
```

**Test Data:**
```text
Father FA: NRIC S7000001A, Tan Wei Ming
Mother MA: NRIC S7000002B, Lim Mei Ling
Child A1: Tan Jia Hui, citizen, age 12, EA Active, balance S$250.00, BVP / P6 Integrity
Child A2: Tan Jun Kai, citizen, age 9, EA Active, balance S$80.00, BVP / P3 Harmony
```

**Test Steps:**
1. Stay idle for 15 minutes
2. Click any link or button

**Expected Result:**
> User is logged out; MSG-0002 'Your session has expired. Please log in again.' is shown; Landing page is displayed

---

#### `TC-R8-031`: Verify the session stays active after 14 minutes of inactivity

- **Scenario ID**: `TS-003`
- **Test Suite**: Session
- **Page / Target**: `Any page`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Security`
- **Traceability**: NFR session (D-22) - boundary
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
FA logged in on Home
```

**Test Data:**
```text
Father FA: NRIC S7000001A, Tan Wei Ming
Mother MA: NRIC S7000002B, Lim Mei Ling
Child A1: Tan Jia Hui, citizen, age 12, EA Active, balance S$250.00, BVP / P6 Integrity
Child A2: Tan Jun Kai, citizen, age 9, EA Active, balance S$80.00, BVP / P3 Harmony
```

**Test Steps:**
1. Stay idle for 14 minutes
2. Open A1's Education Account

**Expected Result:**
> Page opens normally; no MSG-0002

---

#### `TC-R8-032`: Verify an expired session cannot save My details

- **Scenario ID**: `TS-003`
- **Test Suite**: Session
- **Page / Target**: `My details`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FR-08.3 errors; NFR session
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
FA on My details with an edited phone not yet saved
```

**Test Data:**
```text
Phone: 98887777
```

**Test Steps:**
1. Edit phone to 98887777
2. Stay idle 15 minutes
3. Click [Save]

**Expected Result:**
> MSG-0002 is shown; user is sent to Landing page
> Phone in the database is unchanged

---

#### `TC-R8-033`: Verify logout ends the session

- **Scenario ID**: `TS-003`
- **Test Suite**: Session
- **Page / Target**: `Any page`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Security`
- **Traceability**: FS R8 sec. 3 step 9; NFR Security
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
FA logged in
```

**Test Data:**
```text
Father FA: NRIC S7000001A, Tan Wei Ming
Mother MA: NRIC S7000002B, Lim Mei Ling
Child A1: Tan Jia Hui, citizen, age 12, EA Active, balance S$250.00, BVP / P6 Integrity
Child A2: Tan Jun Kai, citizen, age 9, EA Active, balance S$80.00, BVP / P3 Harmony
```

**Test Steps:**
1. Click [Log out]
2. Press the browser Back button
3. Re-use the old token on the EA API

**Expected Result:**
> Landing page is shown; Back does not show child data
> API call with the old token returns 401

---


### Test Suite: Home

#### `TC-R8-034`: Verify each linked child has a card with name, EA status, school and class

- **Scenario ID**: `TS-004`
- **Test Suite**: Home
- **Page / Target**: `Home`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `UI`
- **Traceability**: FS R8 6.1; R8-AC01
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
FA logged in
```

**Test Data:**
```text
Father FA: NRIC S7000001A, Tan Wei Ming
Mother MA: NRIC S7000002B, Lim Mei Ling
Child A1: Tan Jia Hui, citizen, age 12, EA Active, balance S$250.00, BVP / P6 Integrity
Child A2: Tan Jun Kai, citizen, age 9, EA Active, balance S$80.00, BVP / P3 Harmony
```

**Test Steps:**
1. Open Home
2. Check the header of each card

**Expected Result:**
> One card per child; each shows student name, EA status label, school and class

---

#### `TC-R8-035`: Verify the EA balance is shown on the card for an Active account

- **Scenario ID**: `TS-004`
- **Test Suite**: Home
- **Page / Target**: `Home`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FS R8 6.1 (EA balance)
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
A1 EA Active, balance S$250.00
```

**Test Data:**
```text
Father FA: NRIC S7000001A, Tan Wei Ming
Mother MA: NRIC S7000002B, Lim Mei Ling
Child A1: Tan Jia Hui, citizen, age 12, EA Active, balance S$250.00, BVP / P6 Integrity
Child A2: Tan Jun Kai, citizen, age 9, EA Active, balance S$80.00, BVP / P3 Harmony
```

**Test Steps:**
1. Open Home
2. Check A1's card

**Expected Result:**
> A1 card shows status Active and EA balance S$250.00

---

#### `TC-R8-036`: Verify the EA balance is shown on the card for a Due for closure account

- **Scenario ID**: `TS-004`
- **Test Suite**: Home
- **Page / Target**: `Home`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FS R8 6.1; 6.2
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API
- **Assumption Reference**: ASM-03: Per FS R1 v1.2 F02, opening the EA of a child aged 16+ triggers the closure eligibility check. Balance = 0 -> account becomes Closed; 'Due for closure' is expected only when balance > 0 and CPF transfer is deferred. Confirm with BA.

**Preconditions:**
```text
Child B1 is 16+, EA not closed, balance S$40.00
```

**Test Data:**
```text
Parent PB: S7000003C
Child B1: age 16, EA balance S$40.00
```

**Test Steps:**
1. Log in as PB
2. Check B1's card

**Expected Result:**
> B1 card shows status Due for closure and EA balance S$40.00

---

#### `TC-R8-037`: Verify the balance is replaced by a status sentence for children without a usable EA

- **Scenario ID**: `TS-004`
- **Test Suite**: Home
- **Page / Target**: `Home`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FS R8 6.1; 6.2; R8-AC10
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API
- **Assumption Reference**: ASM-07: Card position for Closed / To be created / Not yet 7 / Not eligible children is not defined in FS R8 sec. 6.1. Record the actual order and confirm with BA.

**Preconditions:**
```text
Parent PC has children: C1 Closed EA, C2 citizen age 7 without EA, C3 citizen age 5, C4 non-citizen age 10
```

**Test Data:**
```text
Parent PC: S7000004D
C1 Closed; C2 To be created; C3 Not yet 7 (DOB 20/05/2021); C4 PR
```

**Test Steps:**
1. Log in as PC
2. Check each card

**Expected Result:**
> No balance is shown on any card
> C2: 'Education Account not active yet.'
> C3: sentence with opening date 20/05/2028
> C4: 'Education Accounts are for Singapore Citizens'
> C1: Closed status, no balance

---

#### `TC-R8-038`: Verify 'Need to pay' shows total outstanding fees after subsidy

- **Scenario ID**: `TS-004`
- **Test Suite**: Home
- **Page / Target**: `Home`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FS R8 6.1 (Need to pay)
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API
- **Assumption Reference**: ASM-22: FAS (R4/R10) is not delivered in Sprint 1; FAS status is seeded as mock data.

ASM-23: Fee/charge data (R3/R9) is seeded as POSTED student charges with due dates.

**Preconditions:**
```text
A1 has POSTED charges S$120.00 and S$80.00; FAS subsidy reduces S$80.00 to S$40.00
```

**Test Data:**
```text
A1 charges: Misc fee S$120.00; Textbooks S$80.00 (subsidy -S$40.00)
```

**Test Steps:**
1. Log in as FA
2. Check 'Need to pay' on A1's card

**Expected Result:**
> Need to pay' shows S$160.00

---

#### `TC-R8-039`: Verify the FAS label appears only for a Granted FAS

- **Scenario ID**: `TS-004`
- **Test Suite**: Home
- **Page / Target**: `Home`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FS R8 6.1 (FAS label)
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API
- **Assumption Reference**: ASM-22: FAS (R4/R10) is not delivered in Sprint 1; FAS status is seeded as mock data.

**Preconditions:**
```text
A1 has MOEFAS Tier 2 Granted; A2 has an FAS under review
```

**Test Data:**
```text
Father FA: NRIC S7000001A, Tan Wei Ming
Mother MA: NRIC S7000002B, Lim Mei Ling
Child A1: Tan Jia Hui, citizen, age 12, EA Active, balance S$250.00, BVP / P6 Integrity
Child A2: Tan Jun Kai, citizen, age 9, EA Active, balance S$80.00, BVP / P3 Harmony
```

**Test Steps:**
1. Log in as FA
2. Check the cards of A1 and A2

**Expected Result:**
> A1 card shows 'MOEFAS Tier 2'
> A2 card shows no FAS label

---

#### `TC-R8-040`: Verify the card lists at most 3 outstanding fees sorted by nearest due date

- **Scenario ID**: `TS-004`
- **Test Suite**: Home
- **Page / Target**: `Home`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FS R8 6.1 (fee list) - boundary 3
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API
- **Assumption Reference**: ASM-06: 'Due soon' threshold is not defined; assumed due date within the next 7 days. Overdue = due date before today; Not due yet = otherwise.

ASM-23: Fee/charge data (R3/R9) is seeded as POSTED student charges with due dates.

**Preconditions:**
```text
A1 has 3 outstanding charges with different due dates
```

**Test Data:**
```text
Due 20/10/2026 S$30.00; due 05/11/2026 S$45.00; due 10/10/2026 S$20.00 (overdue)
```

**Test Steps:**
1. Log in as FA
2. Check the fee list on A1's card

**Expected Result:**
> 3 rows in this order: due 10/10, 20/10, 05/11
> Each row shows fee name, status (Overdue / Due soon / Not due yet) and amount
> No '+N more' line

---

#### `TC-R8-041`: Verify '+N more' appears when there are more than 3 outstanding fees

- **Scenario ID**: `TS-004`
- **Test Suite**: Home
- **Page / Target**: `Home`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FS R8 6.1; R8-AC19
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API
- **Assumption Reference**: ASM-23: Fee/charge data (R3/R9) is seeded as POSTED student charges with due dates.

**Preconditions:**
```text
A1 has 5 outstanding charges
```

**Test Data:**
```text
5 POSTED charges with due dates 10/10, 20/10, 05/11, 30/11, 15/12/2026
```

**Test Steps:**
1. Log in as FA
2. Check A1's card

**Expected Result:**
> The 3 nearest-due charges are shown, then '+2 more'

---

#### `TC-R8-042`: Verify 'Nothing to pay right now.' when there are no outstanding fees

- **Scenario ID**: `TS-004`
- **Test Suite**: Home
- **Page / Target**: `Home`
- **Severity / Priority**: `S4 (lowest)` / `Low`
- **Execution Status**: `Not Run` | **Test Type**: `UI`
- **Traceability**: FS R8 6.1 (fee list)
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
A2 has no outstanding charges
```

**Test Data:**
```text
Father FA: NRIC S7000001A, Tan Wei Ming
Mother MA: NRIC S7000002B, Lim Mei Ling
Child A1: Tan Jia Hui, citizen, age 12, EA Active, balance S$250.00, BVP / P6 Integrity
Child A2: Tan Jun Kai, citizen, age 9, EA Active, balance S$80.00, BVP / P3 Harmony
```

**Test Steps:**
1. Log in as FA
2. Check A2's card

**Expected Result:**
> A2 card shows 'Nothing to pay right now.' and 'Need to pay' is S$0.00

---

#### `TC-R8-043`: Verify fee status labels Overdue, Due soon and Not due yet

- **Scenario ID**: `TS-004`
- **Test Suite**: Home
- **Page / Target**: `Home`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FS R8 6.1 (fee status)
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API
- **Assumption Reference**: ASM-06: 'Due soon' threshold is not defined; assumed due date within the next 7 days. Overdue = due date before today; Not due yet = otherwise.

ASM-23: Fee/charge data (R3/R9) is seeded as POSTED student charges with due dates.

**Preconditions:**
```text
A1 has charges due yesterday, in 3 days and in 30 days
```

**Test Data:**
```text
Today = execution date
```

**Test Steps:**
1. Log in as FA
2. Check the status label of each charge on A1's card

**Expected Result:**
> Due yesterday: Overdue
> Due in 3 days: Due soon
> Due in 30 days: Not due yet

---

#### `TC-R8-044`: Verify clicking a card opens that child's Education Account

- **Scenario ID**: `TS-004`
- **Test Suite**: Home
- **Page / Target**: `Home > Education Account`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FS R8 6.1
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
FA logged in
```

**Test Data:**
```text
Father FA: NRIC S7000001A, Tan Wei Ming
Mother MA: NRIC S7000002B, Lim Mei Ling
Child A1: Tan Jia Hui, citizen, age 12, EA Active, balance S$250.00, BVP / P6 Integrity
Child A2: Tan Jun Kai, citizen, age 9, EA Active, balance S$80.00, BVP / P3 Harmony
```

**Test Steps:**
1. Click A2's card

**Expected Result:**
> Education Account screen opens for A2 (name, EA code and balance belong to A2)

---

#### `TC-R8-045`: Verify [All fees] opens the fee list of that child

- **Scenario ID**: `TS-004`
- **Test Suite**: Home
- **Page / Target**: `Home > Fees`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FS R8 6.1 (All fees); FS-09
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API
- **Assumption Reference**: ASM-23: Fee/charge data (R3/R9) is seeded as POSTED student charges with due dates.

**Preconditions:**
```text
A1 has outstanding charges
```

**Test Data:**
```text
Father FA: NRIC S7000001A, Tan Wei Ming
Mother MA: NRIC S7000002B, Lim Mei Ling
Child A1: Tan Jia Hui, citizen, age 12, EA Active, balance S$250.00, BVP / P6 Integrity
Child A2: Tan Jun Kai, citizen, age 9, EA Active, balance S$80.00, BVP / P3 Harmony
```

**Test Steps:**
1. Click [All fees] on A1's card

**Expected Result:**
> Fees page (FS-09) opens filtered to A1

---

#### `TC-R8-046`: Verify the [Apply for FAS] button is shown at the top of Home

- **Scenario ID**: `TS-004`
- **Test Suite**: Home
- **Page / Target**: `Home`
- **Severity / Priority**: `S4 (lowest)` / `Low`
- **Execution Status**: `Not Run` | **Test Type**: `UI`
- **Traceability**: FS R8 6.1
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API
- **Assumption Reference**: ASM-22: FAS (R4/R10) is not delivered in Sprint 1; FAS status is seeded as mock data.
- **Note**: Navigation only; FAS application is out of R8 scope

**Preconditions:**
```text
FA logged in
```

**Test Data:**
```text
Father FA: NRIC S7000001A, Tan Wei Ming
Mother MA: NRIC S7000002B, Lim Mei Ling
Child A1: Tan Jia Hui, citizen, age 12, EA Active, balance S$250.00, BVP / P6 Integrity
Child A2: Tan Jun Kai, citizen, age 9, EA Active, balance S$80.00, BVP / P3 Harmony
```

**Test Steps:**
1. Open Home
2. Click [Apply for FAS]

**Expected Result:**
> Button is shown above the cards and opens the FAS application entry (FS-10)

---

#### `TC-R8-047`: Verify Active children are shown before children aged 16+

- **Scenario ID**: `TS-004`
- **Test Suite**: Home
- **Page / Target**: `Home`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FS R8 6.1 order rules 1-2; R8-AC12
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
Parent PB: B1 age 16 (Due for closure), B2 age 14 Active, B3 age 9 Active
```

**Test Data:**
```text
Parent PB: S7000003C
```

**Test Steps:**
1. Log in as PB
2. Read the card order

**Expected Result:**
> Order: B2 (14), B3 (9), B1 (16) - the 16+ child is last; Active children by age descending

---

#### `TC-R8-048`: Verify children of the same age are ordered by FAS application status

- **Scenario ID**: `TS-004`
- **Test Suite**: Home
- **Page / Target**: `Home`
- **Severity / Priority**: `S4 (lowest)` / `Low`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FS R8 6.1 order rule 3
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API
- **Assumption Reference**: ASM-22: FAS (R4/R10) is not delivered in Sprint 1; FAS status is seeded as mock data.

**Preconditions:**
```text
Twins T1 and T2 (same DOB, Active); T2 has a pending FAS application, T1 has none
```

**Test Data:**
```text
Parent PD: S7000006F
```

**Test Steps:**
1. Log in as PD
2. Read the card order

**Expected Result:**
> T1 (no FAS application) is shown before T2

---

#### `TC-R8-049`: Verify the child selector on the Education Account screen uses the same order as Home

- **Scenario ID**: `TS-004`
- **Test Suite**: Home
- **Page / Target**: `Education Account`
- **Severity / Priority**: `S4 (lowest)` / `Low`
- **Execution Status**: `Not Run` | **Test Type**: `UI`
- **Traceability**: FS R8 6.1 (same order for selector)
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
Parent PB with B1 (16), B2 (14), B3 (9)
```

**Test Data:**
```text
Parent PB: S7000003C
```

**Test Steps:**
1. Log in as PB
2. Open any Education Account
3. Read the order of the child buttons

**Expected Result:**
> Buttons follow the Home order: All, B2, B3, B1

---

#### `TC-R8-050`: Verify the card position of children with Closed / To be created / Not yet 7 / Not eligible status

- **Scenario ID**: `TS-004`
- **Test Suite**: Home
- **Page / Target**: `Home`
- **Severity / Priority**: `S4 (lowest)` / `Low`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FS R8 6.1
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API
- **Assumption Reference**: ASM-07: Card position for Closed / To be created / Not yet 7 / Not eligible children is not defined in FS R8 sec. 6.1. Record the actual order and confirm with BA.
- **Note**: Expected result pending BA answer

**Preconditions:**
```text
Parent PC with C1 Closed, C2 To be created, C3 Not yet 7, C4 Not eligible, C5 Active
```

**Test Data:**
```text
Parent PC: S7000004D
```

**Test Steps:**
1. Log in as PC
2. Record the card order

**Expected Result:**
> Order is consistent and matches the rule confirmed by BA

---


### Test Suite: Education Account - Account Info

#### `TC-R8-051`: Verify the account information block on the Education Account screen

- **Scenario ID**: `TS-005`
- **Test Suite**: Education Account - Account Info
- **Page / Target**: `Education Account`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FR-08.2 main flow (1); R8-AC06
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
FA logged in; A1 EA Active
```

**Test Data:**
```text
Father FA: NRIC S7000001A, Tan Wei Ming
Mother MA: NRIC S7000002B, Lim Mei Ling
Child A1: Tan Jia Hui, citizen, age 12, EA Active, balance S$250.00, BVP / P6 Integrity
Child A2: Tan Jun Kai, citizen, age 9, EA Active, balance S$80.00, BVP / P3 Harmony
```

**Test Steps:**
1. Open A1's Education Account
2. Check the account information block

**Expected Result:**
> Shows EA code, status and reason, opening date, expected closure date, Last updated, student name, school, class, DOB
> Dates in DD/MM/YYYY

---

#### `TC-R8-052`: Verify the EA code format

- **Scenario ID**: `TS-005`
- **Test Suite**: Education Account - Account Info
- **Page / Target**: `Education Account`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FR-08.2 rules (EA code)
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API
- **Assumption Reference**: ASM-05: 'EA + student number' - the student number is assumed NOT to be the NRIC (privacy). Confirm the number source with BA/Dev.

**Preconditions:**
```text
A1 EA exists
```

**Test Data:**
```text
Father FA: NRIC S7000001A, Tan Wei Ming
Mother MA: NRIC S7000002B, Lim Mei Ling
Child A1: Tan Jia Hui, citizen, age 12, EA Active, balance S$250.00, BVP / P6 Integrity
Child A2: Tan Jun Kai, citizen, age 9, EA Active, balance S$80.00, BVP / P3 Harmony
```

**Test Steps:**
1. Open A1's Education Account
2. Read the EA code

**Expected Result:**
> EA code starts with 'EA' followed by the student number; it does not contain the student's NRIC

---

#### `TC-R8-053`: Verify opening date and expected closure date

- **Scenario ID**: `TS-005`
- **Test Suite**: Education Account - Account Info
- **Page / Target**: `Education Account`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FR-08.2 rules (dates)
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API
- **Assumption Reference**: ASM-04: FS R8 says opening date = 7th birthday; FS R1 records the actual creation date (initial sync creates accounts for ages 7-<16). Test follows FS R8; confirm with BA.

**Preconditions:**
```text
A1 DOB 12/03/2014, EA Active
```

**Test Data:**
```text
A1 DOB: 12/03/2014
```

**Test Steps:**
1. Open A1's Education Account
2. Read the opening date and expected closure date

**Expected Result:**
> Opening date 12/03/2021 (7th birthday); expected closure date 12/03/2030 (16th birthday)

---

#### `TC-R8-054`: Verify opening and closure dates for a child born on 29/02

- **Scenario ID**: `TS-005`
- **Test Suite**: Education Account - Account Info
- **Page / Target**: `Education Account`
- **Severity / Priority**: `S3` / `Low`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FR-08.2 rules; FS R1 leap-year rule (F01-AC14, F02-AC15)
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API
- **Assumption Reference**: ASM-04: FS R8 says opening date = 7th birthday; FS R1 records the actual creation date (initial sync creates accounts for ages 7-<16). Test follows FS R8; confirm with BA.

ASM-13: Leap-year rule from FS R1 [WA]: a child born 29/02 reaches an age milestone on 28/02 in non-leap years.

**Preconditions:**
```text
Child A4 DOB 29/02/2016, EA Active
```

**Test Data:**
```text
A4 DOB: 29/02/2016
```

**Test Steps:**
1. Open A4's Education Account
2. Read the dates

**Expected Result:**
> Opening date 28/02/2023; expected closure date 28/02/2032

---

#### `TC-R8-055`: Verify Active status shows the closure date

- **Scenario ID**: `TS-005`
- **Test Suite**: Education Account - Account Info
- **Page / Target**: `Education Account`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FS R8 6.2 (Active)
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
A1 citizen age 12 with EA
```

**Test Data:**
```text
Father FA: NRIC S7000001A, Tan Wei Ming
Mother MA: NRIC S7000002B, Lim Mei Ling
Child A1: Tan Jia Hui, citizen, age 12, EA Active, balance S$250.00, BVP / P6 Integrity
Child A2: Tan Jun Kai, citizen, age 9, EA Active, balance S$80.00, BVP / P3 Harmony
```

**Test Steps:**
1. Open A1's Education Account

**Expected Result:**
> Status Active with the closure date; balance and transactions are shown

---

#### `TC-R8-056`: Verify a 16+ child with zero balance is closed when the parent opens the account

- **Scenario ID**: `TS-005`
- **Test Suite**: Education Account - Account Info
- **Page / Target**: `Education Account`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: FR-08.2; FS R1 F02-AC02; R8-AC26
- **Environment**: SIT
Chrome (latest) + DB read access
Build: TBC
Mock SingPass + mock data API
- **Assumption Reference**: ASM-03: Per FS R1 v1.2 F02, opening the EA of a child aged 16+ triggers the closure eligibility check. Balance = 0 -> account becomes Closed; 'Due for closure' is expected only when balance > 0 and CPF transfer is deferred. Confirm with BA.

**Preconditions:**
```text
Child B1 reached 16 today; EA still Active in DB; balance S$0.00
```

**Test Data:**
```text
Parent PB: S7000003C
B1 DOB = execution date - 16 years
```

**Test Steps:**
1. Log in as PB
2. Open B1's Education Account
3. Check B1's EA status in the database

**Expected Result:**
> Closure check runs before the data is shown
> Status shown and stored is Closed with an actual closure date; no balance block; transactions still viewable

---

#### `TC-R8-057`: Verify Due for closure for a 16+ child whose account has a remaining balance

- **Scenario ID**: `TS-005`
- **Test Suite**: Education Account - Account Info
- **Page / Target**: `Education Account`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FS R8 6.2 (Due for closure); R8-AC26; FS R1 F02-AC10
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API
- **Assumption Reference**: ASM-03: Per FS R1 v1.2 F02, opening the EA of a child aged 16+ triggers the closure eligibility check. Balance = 0 -> account becomes Closed; 'Due for closure' is expected only when balance > 0 and CPF transfer is deferred. Confirm with BA.

**Preconditions:**
```text
B1 reached 16; balance S$40.00; CPF transfer deferred
```

**Test Data:**
```text
B1 DOB = execution date - 16 years; balance S$40.00
```

**Test Steps:**
1. Log in as PB
2. Open B1's Education Account

**Expected Result:**
> Status Due for closure; shows the 16th birthday and closure date; balance and transactions shown; no pay or FAS actions

---

#### `TC-R8-058`: Verify a Closed account shows transactions only

- **Scenario ID**: `TS-005`
- **Test Suite**: Education Account - Account Info
- **Page / Target**: `Education Account`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FS R8 6.2 (Closed); FS R1 F02-AC07
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
C1's EA is Closed with transaction history
```

**Test Data:**
```text
Parent PC: S7000004D; C1 Closed
```

**Test Steps:**
1. Log in as PC
2. Open C1's Education Account

**Expected Result:**
> Status Closed; no balance block; transaction history is shown read-only

---

#### `TC-R8-059`: Verify 'To be created' for a citizen aged 7+ without an EA

- **Scenario ID**: `TS-005`
- **Test Suite**: Education Account - Account Info
- **Page / Target**: `Education Account`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FS R8 6.2 (To be created)
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API
- **Assumption Reference**: ASM-14: MSG-0804 and the FS R8 table 6.2 sentences overlap; assumed the table 6.2 sentence is shown on the EA screen.

**Preconditions:**
```text
C2 citizen aged 7+ with no EA record
```

**Test Data:**
```text
C2 age 7
```

**Test Steps:**
1. Log in as PC
2. Open C2's Education Account

**Expected Result:**
> Sentence 'Education Account not active yet.' is shown; no balance or transactions

---

#### `TC-R8-060`: Verify 'Not yet 7' shows the date the EA will open

- **Scenario ID**: `TS-005`
- **Test Suite**: Education Account - Account Info
- **Page / Target**: `Education Account`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FS R8 6.2 (Not yet 7)
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API
- **Assumption Reference**: ASM-14: MSG-0804 and the FS R8 table 6.2 sentences overlap; assumed the table 6.2 sentence is shown on the EA screen.

**Preconditions:**
```text
C3 citizen DOB 20/05/2021
```

**Test Data:**
```text
C3 DOB: 20/05/2021
```

**Test Steps:**
1. Log in as PC
2. Open C3's Education Account

**Expected Result:**
> Sentence states the EA will open on 20/05/2028; no balance

---

#### `TC-R8-061`: Verify 'Not eligible' for a non-citizen child

- **Scenario ID**: `TS-005`
- **Test Suite**: Education Account - Account Info
- **Page / Target**: `Education Account`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FS R8 6.2 (Not eligible); R8-AC10
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
C4 is a Permanent Resident
```

**Test Data:**
```text
C4 citizenship: PR
```

**Test Steps:**
1. Log in as PC
2. Open C4's Education Account
3. Go back to Home and open C4's fees

**Expected Result:**
> Sentence 'Education Accounts are for Singapore Citizens' shown; no balance
> C4's fees can still be viewed

---

#### `TC-R8-062`: Verify behaviour when the closure check cannot reach the Government API on view

- **Scenario ID**: `TS-005`
- **Test Suite**: Education Account - Account Info
- **Page / Target**: `Education Account`
- **Severity / Priority**: `S2` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: FS R1 F02-AC09, EF01
- **Environment**: SIT
Chrome (latest) + DB read access
Build: TBC
Mock SingPass + mock data API
- **Assumption Reference**: ASM-12: FS R1 v1.2 EF01 covers Government API failure only for financial actions. R8 behaviour when the closure check fails on a view is not defined; record actual behaviour and confirm with BA.
- **Note**: Expected UI behaviour pending BA answer

**Preconditions:**
```text
B1 aged 16+; mock Government API returns HTTP 500 during the closure check
```

**Test Data:**
```text
B1 balance S$0.00
```

**Test Steps:**
1. Log in as PB
2. Open B1's Education Account
3. Check B1's EA status in DB

**Expected Result:**
> Account is not marked Closed; behaviour/message on screen matches the rule confirmed by BA

---

#### `TC-R8-063`: Verify a child turning 16 tomorrow is still Active with full functions

- **Scenario ID**: `TS-005`
- **Test Suite**: Education Account - Account Info
- **Page / Target**: `Education Account`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FR-08.2 rules (16-year rule) - boundary
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
B2 DOB = execution date - 16 years + 1 day
```

**Test Data:**
```text
B2 age 15 (16th birthday tomorrow)
```

**Test Steps:**
1. Log in as PB
2. Open B2's Education Account and Home card

**Expected Result:**
> Status Active; balance shown; pay and FAS actions available

---


### Test Suite: Education Account - Balance

#### `TC-R8-064`: Verify available balance counts only Completed transactions

- **Scenario ID**: `TS-006`
- **Test Suite**: Education Account - Balance
- **Page / Target**: `Education Account`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FR-08.2 rules (balance)
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API
- **Assumption Reference**: ASM-19: FS R1 transactions only have Success/Failed; Pending applies to online payments. 'Completed' in R8 = 'Success' in R1.

**Preconditions:**
```text
A1 transactions: Top-up +S$300.00 Completed; Fee payment -S$50.00 Completed; Top-up +S$100.00 Failed
```

**Test Data:**
```text
Father FA: NRIC S7000001A, Tan Wei Ming
Mother MA: NRIC S7000002B, Lim Mei Ling
Child A1: Tan Jia Hui, citizen, age 12, EA Active, balance S$250.00, BVP / P6 Integrity
Child A2: Tan Jun Kai, citizen, age 9, EA Active, balance S$80.00, BVP / P3 Harmony
```

**Test Steps:**
1. Open A1's Education Account
2. Read available balance

**Expected Result:**
> Available balance = S$250.00 (Failed top-up not counted)

---

#### `TC-R8-065`: Verify a Pending transaction is shown separately and not deducted

- **Scenario ID**: `TS-006`
- **Test Suite**: Education Account - Balance
- **Page / Target**: `Education Account`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FR-08.2 rules; R8-AC25
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API
- **Assumption Reference**: ASM-19: FS R1 transactions only have Success/Failed; Pending applies to online payments. 'Completed' in R8 = 'Success' in R1.

**Preconditions:**
```text
A1 balance S$250.00; one online payment S$60.00 Pending
```

**Test Data:**
```text
Pending: online Fee payment S$60.00
```

**Test Steps:**
1. Open A1's Education Account
2. Check the balance block and transaction table

**Expected Result:**
> Available balance stays S$250.00
> Pending S$60.00 shown in a yellow box
> The Pending row has no 'Balance after' value

---

#### `TC-R8-066`: Verify money in and money out for the current year

- **Scenario ID**: `TS-006`
- **Test Suite**: Education Account - Balance
- **Page / Target**: `Education Account`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FR-08.2 main flow (2) - boundary year start
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API
- **Assumption Reference**: ASM-16: 'Money in / money out this year' = calendar year 01/01-31/12, Singapore time.

**Preconditions:**
```text
A1 Completed transactions: +S$200.00 on 31/12/2025, +S$150.00 on 01/01/2026, -S$70.00 on 15/03/2026, -S$30.00 Failed on 01/04/2026
```

**Test Data:**
```text
Father FA: NRIC S7000001A, Tan Wei Ming
Mother MA: NRIC S7000002B, Lim Mei Ling
Child A1: Tan Jia Hui, citizen, age 12, EA Active, balance S$250.00, BVP / P6 Integrity
Child A2: Tan Jun Kai, citizen, age 9, EA Active, balance S$80.00, BVP / P3 Harmony
```

**Test Steps:**
1. Open A1's Education Account
2. Read money in / money out this year

**Expected Result:**
> Money in = S$150.00; money out = S$70.00 (prior-year and Failed items excluded)

---

#### `TC-R8-067`: Verify amount format is SGD with 2 decimals and thousand separators

- **Scenario ID**: `TS-006`
- **Test Suite**: Education Account - Balance
- **Page / Target**: `Education Account`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `UI`
- **Traceability**: FR-08.2 rules; NFR display
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
A5 balance S$1234.5
```

**Test Data:**
```text
Balance: 1234.5
```

**Test Steps:**
1. Open A5's Education Account
2. Read the balance and amounts in the table

**Expected Result:**
> Shown as S$1,234.50; all amounts in SGD with 2 decimals

---

#### `TC-R8-068`: Verify an account with zero balance and no transactions

- **Scenario ID**: `TS-006`
- **Test Suite**: Education Account - Balance
- **Page / Target**: `Education Account`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FR-08.2
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API
- **Assumption Reference**: ASM-11: Empty-state text for an account with no transactions is not defined; assumed MSG-0803 'No transactions found.'

**Preconditions:**
```text
A3 EA just created; balance S$0.00; no transactions
```

**Test Data:**
```text
A3 age 7
```

**Test Steps:**
1. Open A3's Education Account

**Expected Result:**
> Balance S$0.00; money in/out S$0.00; transaction table shows the empty-state message

---


### Test Suite: Education Account - FAS

#### `TC-R8-069`: Verify the green FAS block for a Granted scheme

- **Scenario ID**: `TS-007`
- **Test Suite**: Education Account - FAS
- **Page / Target**: `Education Account`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FR-08.2 main flow (3); R8-AC27
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API
- **Assumption Reference**: ASM-22: FAS (R4/R10) is not delivered in Sprint 1; FAS status is seeded as mock data.

**Preconditions:**
```text
A1 has MOEFAS Tier 2 Granted reducing Textbooks fee
```

**Test Data:**
```text
FAS: MOEFAS Tier 2; reduced fee: Textbooks
```

**Test Steps:**
1. Open A1's Education Account
2. Check the FAS block

**Expected Result:**
> Green block shows scheme MOEFAS, Tier 2 and the reduced fee(s)

---

#### `TC-R8-070`: Verify 'Under review' label for an FAS being assessed

- **Scenario ID**: `TS-007`
- **Test Suite**: Education Account - FAS
- **Page / Target**: `Education Account`
- **Severity / Priority**: `S4 (lowest)` / `Low`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FR-08.2 rules (FAS)
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API
- **Assumption Reference**: ASM-22: FAS (R4/R10) is not delivered in Sprint 1; FAS status is seeded as mock data.

**Preconditions:**
```text
A2 has an FAS application under review
```

**Test Data:**
```text
Father FA: NRIC S7000001A, Tan Wei Ming
Mother MA: NRIC S7000002B, Lim Mei Ling
Child A1: Tan Jia Hui, citizen, age 12, EA Active, balance S$250.00, BVP / P6 Integrity
Child A2: Tan Jun Kai, citizen, age 9, EA Active, balance S$80.00, BVP / P3 Harmony
```

**Test Steps:**
1. Open A2's Education Account

**Expected Result:**
> FAS area shows the 'Under review' label

---

#### `TC-R8-071`: Verify the FAS block is hidden when the child has no FAS

- **Scenario ID**: `TS-007`
- **Test Suite**: Education Account - FAS
- **Page / Target**: `Education Account`
- **Severity / Priority**: `S4 (lowest)` / `Low`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FR-08.2 rules (FAS); R8-AC27
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
B2 has no FAS record
```

**Test Data:**
```text
Parent PB
```

**Test Steps:**
1. Log in as PB
2. Open B2's Education Account

**Expected Result:**
> No FAS block is shown

---


### Test Suite: Education Account - Transactions

#### `TC-R8-072`: Verify the transaction table columns and newest-first order

- **Scenario ID**: `TS-008`
- **Test Suite**: Education Account - Transactions
- **Page / Target**: `Education Account`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FR-08.2 main flow (4); FS R8 6.2; R8-AC06; R8-AC28
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
A1 has 5 transactions on different dates
```

**Test Data:**
```text
Father FA: NRIC S7000001A, Tan Wei Ming
Mother MA: NRIC S7000002B, Lim Mei Ling
Child A1: Tan Jia Hui, citizen, age 12, EA Active, balance S$250.00, BVP / P6 Integrity
Child A2: Tan Jun Kai, citizen, age 9, EA Active, balance S$80.00, BVP / P3 Harmony
```

**Test Steps:**
1. Open A1's Education Account (single child view)
2. Check the columns and order

**Expected Result:**
> Columns: Date & time, Type, Description (with TXN ref), Amount, Balance after, Status
> Newest transaction first
> No Student column

---

#### `TC-R8-073`: Verify transaction reference format and type colours

- **Scenario ID**: `TS-008`
- **Test Suite**: Education Account - Transactions
- **Page / Target**: `Education Account`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `UI`
- **Traceability**: FR-08.2 rules; R8-AC28
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API
- **Assumption Reference**: ASM-20: Transaction type labels follow FS R8 (Top-up, Fee payment, Refund, Closure transfer). Refund and Closure transfer may not exist in Sprint 1 (CPF transfer deferred in FS R1); use seeded mock transactions.

**Preconditions:**
```text
A1 has at least one transaction of each type
```

**Test Data:**
```text
Types: Top-up, Fee payment, Refund, Closure transfer
```

**Test Steps:**
1. Open A1's Education Account
2. Check each row's description and type badge

**Expected Result:**
> Each reference matches TXN- followed by 6 digits
> Each type has its own distinct colour

---

#### `TC-R8-074`: Verify amount signs and colours for money in and money out

- **Scenario ID**: `TS-008`
- **Test Suite**: Education Account - Transactions
- **Page / Target**: `Education Account`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `UI`
- **Traceability**: FR-08.2 rules; FS R8 6.2 (Amount)
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
A1 has a Top-up and a Fee payment
```

**Test Data:**
```text
Top-up +S$100.00; Fee payment -S$45.00
```

**Test Steps:**
1. Open A1's Education Account
2. Check the Amount column

**Expected Result:**
> Top-up shows +S$100.00 in green; Fee payment shows -S$45.00 in black

---

#### `TC-R8-075`: Verify 'Balance after' for Completed and Failed transactions

- **Scenario ID**: `TS-008`
- **Test Suite**: Education Account - Transactions
- **Page / Target**: `Education Account`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FR-08.2 rules; FS R1 2.3 (failed transaction)
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API
- **Assumption Reference**: ASM-19: FS R1 transactions only have Success/Failed; Pending applies to online payments. 'Completed' in R8 = 'Success' in R1.

**Preconditions:**
```text
A1: Completed top-up +S$100.00 from S$150.00; Failed top-up S$50.00
```

**Test Data:**
```text
Father FA: NRIC S7000001A, Tan Wei Ming
Mother MA: NRIC S7000002B, Lim Mei Ling
Child A1: Tan Jia Hui, citizen, age 12, EA Active, balance S$250.00, BVP / P6 Integrity
Child A2: Tan Jun Kai, citizen, age 9, EA Active, balance S$80.00, BVP / P3 Harmony
```

**Test Steps:**
1. Open A1's Education Account
2. Read 'Balance after' for both rows

**Expected Result:**
> Completed row shows S$250.00
> Failed row does not change the balance

---

#### `TC-R8-076`: Verify an online payment shows amount and 'online' without changing the EA balance

- **Scenario ID**: `TS-008`
- **Test Suite**: Education Account - Transactions
- **Page / Target**: `Education Account`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FS R8 6.2 (Amount); test plan 3.9 (online payment must not debit EA)
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
A1 balance S$250.00; online card payment S$90.00 Completed for a fee
```

**Test Data:**
```text
Online payment S$90.00
```

**Test Steps:**
1. Open A1's Education Account
2. Check the online payment row and the balance

**Expected Result:**
> Row shows S$90.00 with 'online'; available balance stays S$250.00

---

#### `TC-R8-077`: Verify a Pending online payment shows [Continue payment]

- **Scenario ID**: `TS-008`
- **Test Suite**: Education Account - Transactions
- **Page / Target**: `Education Account`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FS R8 6.2 (Status)
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API
- **Assumption Reference**: ASM-19: FS R1 transactions only have Success/Failed; Pending applies to online payments. 'Completed' in R8 = 'Success' in R1.
- **Note**: Payment flow is FS-09 scope

**Preconditions:**
```text
A1 has an online payment in Pending
```

**Test Data:**
```text
Pending online payment S$60.00
```

**Test Steps:**
1. Open A1's Education Account
2. Check the Pending row
3. Click [Continue payment]

**Expected Result:**
> Status Pending with a [Continue payment] button that opens the payment flow (FS-09)

---

#### `TC-R8-078`: Verify [View fee] on a Fee payment opens that child's Fees page

- **Scenario ID**: `TS-008`
- **Test Suite**: Education Account - Transactions
- **Page / Target**: `Education Account > Fees`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FR-08.2 rules; R8-AC28
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
A1 has a Completed Fee payment
```

**Test Data:**
```text
Father FA: NRIC S7000001A, Tan Wei Ming
Mother MA: NRIC S7000002B, Lim Mei Ling
Child A1: Tan Jia Hui, citizen, age 12, EA Active, balance S$250.00, BVP / P6 Integrity
Child A2: Tan Jun Kai, citizen, age 9, EA Active, balance S$80.00, BVP / P3 Harmony
```

**Test Steps:**
1. Open A1's Education Account
2. Click [View fee] on the Fee payment row

**Expected Result:**
> Fees page (FS-09) of A1 opens with the related fee

---

#### `TC-R8-079`: Verify pagination with 21 transactions

- **Scenario ID**: `TS-008`
- **Test Suite**: Education Account - Transactions
- **Page / Target**: `Education Account`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FS R8 6.2 (20 rows per page) - boundary
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
A5 has 21 transactions
```

**Test Data:**
```text
21 transactions
```

**Test Steps:**
1. Open A5's Education Account
2. Check page 1
3. Click [Next]
4. Click [Previous]

**Expected Result:**
> Page 1 shows 20 rows and total '21 transactions'
> Page 2 shows 1 row
> [Previous] returns to page 1

---

#### `TC-R8-080`: Verify a single page with exactly 20 transactions

- **Scenario ID**: `TS-008`
- **Test Suite**: Education Account - Transactions
- **Page / Target**: `Education Account`
- **Severity / Priority**: `S4 (lowest)` / `Low`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FS R8 6.2 (pagination) - boundary
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
A6 has 20 transactions
```

**Test Data:**
```text
20 transactions
```

**Test Steps:**
1. Open A6's Education Account

**Expected Result:**
> 20 rows on one page; [Next] is disabled or hidden; total shows 20

---

#### `TC-R8-081`: Verify filter by type Refund

- **Scenario ID**: `TS-008`
- **Test Suite**: Education Account - Transactions
- **Page / Target**: `Education Account`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FR-08.2 (filter); R8-AC28
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API
- **Assumption Reference**: ASM-20: Transaction type labels follow FS R8 (Top-up, Fee payment, Refund, Closure transfer). Refund and Closure transfer may not exist in Sprint 1 (CPF transfer deferred in FS R1); use seeded mock transactions.

**Preconditions:**
```text
A1 has transactions of all 4 types including 2 Refunds
```

**Test Data:**
```text
Father FA: NRIC S7000001A, Tan Wei Ming
Mother MA: NRIC S7000002B, Lim Mei Ling
Child A1: Tan Jia Hui, citizen, age 12, EA Active, balance S$250.00, BVP / P6 Integrity
Child A2: Tan Jun Kai, citizen, age 9, EA Active, balance S$80.00, BVP / P3 Harmony
```

**Test Steps:**
1. Set Type = Refund
2. Click [Apply filter]

**Expected Result:**
> Only the 2 Refund rows are shown

---

#### `TC-R8-082`: Verify filter by each transaction type

- **Scenario ID**: `TS-008`
- **Test Suite**: Education Account - Transactions
- **Page / Target**: `Education Account`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FS R8 6.2 (filter Type)
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API
- **Assumption Reference**: ASM-20: Transaction type labels follow FS R8 (Top-up, Fee payment, Refund, Closure transfer). Refund and Closure transfer may not exist in Sprint 1 (CPF transfer deferred in FS R1); use seeded mock transactions.

**Preconditions:**
```text
A1 has transactions of all 4 types
```

**Test Data:**
```text
Type values: Top-up, Fee payment, Closure transfer, All
```

**Test Steps:**
1. For each Type value, select it and click [Apply filter]

**Expected Result:**
> Each filter shows only that type; All shows every row

---

#### `TC-R8-083`: Verify filter by money flow

- **Scenario ID**: `TS-008`
- **Test Suite**: Education Account - Transactions
- **Page / Target**: `Education Account`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FS R8 6.2 (filter Money flow)
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
A1 has money-in and money-out transactions
```

**Test Data:**
```text
Father FA: NRIC S7000001A, Tan Wei Ming
Mother MA: NRIC S7000002B, Lim Mei Ling
Child A1: Tan Jia Hui, citizen, age 12, EA Active, balance S$250.00, BVP / P6 Integrity
Child A2: Tan Jun Kai, citizen, age 9, EA Active, balance S$80.00, BVP / P3 Harmony
```

**Test Steps:**
1. Money flow = Money in, click [Apply filter]
2. Money flow = Money out, click [Apply filter]

**Expected Result:**
> Money in shows only positive amounts; Money out shows only negative amounts

---

#### `TC-R8-084`: Verify the date range filter includes the From and To dates

- **Scenario ID**: `TS-008`
- **Test Suite**: Education Account - Transactions
- **Page / Target**: `Education Account`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FS R8 6.2 (filter From/To) - boundary
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
A1 transactions on 31/08, 01/09, 30/09 and 01/10/2026
```

**Test Data:**
```text
From 01/09/2026; To 30/09/2026
```

**Test Steps:**
1. Enter From and To
2. Click [Apply filter]

**Expected Result:**
> Rows dated 01/09 and 30/09 are shown; 31/08 and 01/10 are not

---

#### `TC-R8-085`: Verify the filter rejects From later than To

- **Scenario ID**: `TS-008`
- **Test Suite**: Education Account - Transactions
- **Page / Target**: `Education Account`
- **Severity / Priority**: `S4 (lowest)` / `Low`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FS R8 6.2 (filter)
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API
- **Assumption Reference**: ASM-10: Validation for From date later than To date is not defined; assumed Apply filter is blocked with an inline error.

**Preconditions:**
```text
A1 has transactions
```

**Test Data:**
```text
From 30/09/2026; To 01/09/2026
```

**Test Steps:**
1. Enter From and To
2. Click [Apply filter]

**Expected Result:**
> Filter is not applied and an error is shown

---

#### `TC-R8-086`: Verify a filter with no results shows MSG-0803

- **Scenario ID**: `TS-008`
- **Test Suite**: Education Account - Transactions
- **Page / Target**: `Education Account`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FR-08.2 errors; R8-AC11
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
A2 has no Refund
```

**Test Data:**
```text
Father FA: NRIC S7000001A, Tan Wei Ming
Mother MA: NRIC S7000002B, Lim Mei Ling
Child A1: Tan Jia Hui, citizen, age 12, EA Active, balance S$250.00, BVP / P6 Integrity
Child A2: Tan Jun Kai, citizen, age 9, EA Active, balance S$80.00, BVP / P3 Harmony
```

**Test Steps:**
1. Open A2's Education Account
2. Type = Refund, click [Apply filter]

**Expected Result:**
> MSG-0803 'No transactions found.' is shown

---

#### `TC-R8-087`: Verify filters apply only after clicking [Apply filter]

- **Scenario ID**: `TS-008`
- **Test Suite**: Education Account - Transactions
- **Page / Target**: `Education Account`
- **Severity / Priority**: `S4 (lowest)` / `Low`
- **Execution Status**: `Not Run` | **Test Type**: `UI`
- **Traceability**: FS R8 6.2 (Apply filter)
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
A1 has transactions
```

**Test Data:**
```text
Father FA: NRIC S7000001A, Tan Wei Ming
Mother MA: NRIC S7000002B, Lim Mei Ling
Child A1: Tan Jia Hui, citizen, age 12, EA Active, balance S$250.00, BVP / P6 Integrity
Child A2: Tan Jun Kai, citizen, age 9, EA Active, balance S$80.00, BVP / P3 Harmony
```

**Test Steps:**
1. Change Type to Top-up without clicking [Apply filter]
2. Click [Apply filter]

**Expected Result:**
> Table does not change after step 1; it is filtered after step 2

---

#### `TC-R8-088`: Verify combined date, type and money flow filters

- **Scenario ID**: `TS-008`
- **Test Suite**: Education Account - Transactions
- **Page / Target**: `Education Account`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FS R8 6.2 (filter)
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
A1 has mixed transactions in September and October 2026
```

**Test Data:**
```text
From 01/10/2026; To 31/10/2026; Type Fee payment; Money out
```

**Test Steps:**
1. Set all filters
2. Click [Apply filter]

**Expected Result:**
> Only Fee payment money-out rows dated in October 2026 are shown

---

#### `TC-R8-089`: Verify the All view for a parent with several children

- **Scenario ID**: `TS-008`
- **Test Suite**: Education Account - Transactions
- **Page / Target**: `Education Account`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FS R8 6.2 (Nhiều con)
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
FA has A1 and A2 with transactions
```

**Test Data:**
```text
Father FA: NRIC S7000001A, Tan Wei Ming
Mother MA: NRIC S7000002B, Lim Mei Ling
Child A1: Tan Jia Hui, citizen, age 12, EA Active, balance S$250.00, BVP / P6 Integrity
Child A2: Tan Jun Kai, citizen, age 9, EA Active, balance S$80.00, BVP / P3 Harmony
```

**Test Steps:**
1. Open Education Account
2. Click [All]
3. Click [A1]

**Expected Result:**
> All: one balance card per child and a Student column in the table with rows from A1 and A2 only
> A1: only A1's data; no Student column

---

#### `TC-R8-090`: Verify the All view does not include other families' transactions

- **Scenario ID**: `TS-008`
- **Test Suite**: Education Account - Transactions
- **Page / Target**: `Education Account`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Security`
- **Traceability**: NFR Security; PB-07
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
FA and PB both have children with transactions
```

**Test Data:**
```text
Father FA: NRIC S7000001A, Tan Wei Ming
Mother MA: NRIC S7000002B, Lim Mei Ling
Child A1: Tan Jia Hui, citizen, age 12, EA Active, balance S$250.00, BVP / P6 Integrity
Child A2: Tan Jun Kai, citizen, age 9, EA Active, balance S$80.00, BVP / P3 Harmony
Parent PB children: B1, B2
```

**Test Steps:**
1. Log in as FA
2. Open Education Account > [All]
3. Inspect the API response

**Expected Result:**
> Only A1 and A2 rows; no B1 or B2 data in the UI or API response

---


### Test Suite: Age 16 View-only Rules

#### `TC-R8-091`: Verify only the child who turned 16 becomes view-only

- **Scenario ID**: `TS-009`
- **Test Suite**: Age 16 View-only Rules
- **Page / Target**: `Home / Education Account`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FR-08.2 rules (per-child rule); R8-AC07
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API
- **Assumption Reference**: ASM-03: Per FS R1 v1.2 F02, opening the EA of a child aged 16+ triggers the closure eligibility check. Balance = 0 -> account becomes Closed; 'Due for closure' is expected only when balance > 0 and CPF transfer is deferred. Confirm with BA.

**Preconditions:**
```text
Parent PB: B1 turns 16 today (balance S$40.00); B2 age 14
```

**Test Data:**
```text
B1 DOB = execution date - 16 years
```

**Test Steps:**
1. Log in as PB
2. Check pay and FAS actions for B2
3. Check pay and FAS actions for B1

**Expected Result:**
> B2: pay and FAS actions available
> B1: no pay action and no FAS application action; data remains viewable

---

#### `TC-R8-092`: Verify a 16-year-old child's information remains viewable

- **Scenario ID**: `TS-009`
- **Test Suite**: Age 16 View-only Rules
- **Page / Target**: `Home / Education Account / Fees / My details`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FS R8 sec. 3 step 7; R8-AC08
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
B1 aged 16+
```

**Test Data:**
```text
Parent PB
```

**Test Steps:**
1. Log in as PB
2. Open B1's Education Account, transaction history and Fees
3. Open My details

**Expected Result:**
> All pages open and show B1's data read-only

---

#### `TC-R8-093`: Verify payment for a 16+ child is rejected by the API

- **Scenario ID**: `TS-009`
- **Test Suite**: Age 16 View-only Rules
- **Page / Target**: `API`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Security`
- **Traceability**: FR-08.2 rules; FS R1 F02-AC05
- **Environment**: SIT
API client (Postman) + Chrome DevTools
Build: TBC
Mock SingPass + mock data API
- **Note**: Payment API belongs to FS-09; checks R8 rule server-side

**Preconditions:**
```text
B1 aged 16+ with an outstanding charge
```

**Test Data:**
```text
B1 charge S$20.00
```

**Test Steps:**
1. Log in as PB
2. Call the payment API directly for B1's charge

**Expected Result:**
> Request rejected; no transaction created; balance unchanged

---


### Test Suite: My Details

#### `TC-R8-094`: Verify My details shows the parent's information with read-only fields

- **Scenario ID**: `TS-010`
- **Test Suite**: My Details
- **Page / Target**: `My details`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Passed` | **Test Type**: `UI`
- **Traceability**: FR-08.3; FS R8 sec. 6 field table
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
FA logged in; A1 and A2 under 16
```

**Test Data:**
```text
Parent FA; current phone 91234567; email weiming.tan@example.sg
```

**Test Steps:**
1. Open My details

**Expected Result:**
> Full name, NRIC and residential address are read-only
> Mobile number, email and mailing fields are editable
> [Save] is shown

**Actual Result:**
> Full name, NRIC and residential address are read-only
Mobile number, email and mailing fields are editable
[Save] is shown

---

#### `TC-R8-095`: Verify residential address cannot be edited

- **Scenario ID**: `TS-010`
- **Test Suite**: My Details
- **Page / Target**: `My details`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FR-08.3 rules (D-20); R8-AC18
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
FA logged in
```

**Test Data:**
```text
Parent FA; current phone 91234567; email weiming.tan@example.sg
```

**Test Steps:**
1. Try to type in the residential address field

**Expected Result:**
> Field is read-only; value unchanged

---

#### `TC-R8-096`: Verify the API ignores or rejects changes to read-only fields

- **Scenario ID**: `TS-010`
- **Test Suite**: My Details
- **Page / Target**: `API`
- **Severity / Priority**: `S1 (highest)` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Security`
- **Traceability**: FR-08.3 rules; NFR Security
- **Environment**: SIT
API client (Postman) + Chrome DevTools
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
FA logged in
```

**Test Data:**
```text
Payload adds FullName, Nric and ResidentialStreet values
```

**Test Steps:**
1. Send the profile update API with read-only fields added
2. Check Parent_Profile

**Expected Result:**
> Request rejected or read-only fields ignored; FullName, Nric and residential fields unchanged

---

#### `TC-R8-097`: Verify saving valid phone, email and mailing address

- **Scenario ID**: `TS-010`
- **Test Suite**: My Details
- **Page / Target**: `My details`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Failed` | **Test Type**: `Functional`
- **Traceability**: FR-08.3; R8-AC14; US-08.2; PB-15
- **Environment**: SIT
Chrome (latest) + DB read access
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
FA logged in
```

**Test Data:**
```text
Phone 98887777; email fa.new@example.sg; mailing Blk 9, Verde Walk, #02-01, 650009, Singapore
```

**Test Steps:**
1. Enter the values
2. Click [Save]
3. Reload My details
4. Check the audit log and email outbox

**Expected Result:**
> MSG-0807 'Your details have been updated.' is shown
> Values persist after reload
> Audit log has one entry per changed field (field, old, new, user, time)
> No email is sent

**Actual Result:**
> No success message is displayed after updating the profile.

---

#### `TC-R8-098`: Verify mobile numbers starting with 6, 8 and 9 are accepted

- **Scenario ID**: `TS-010`
- **Test Suite**: My Details
- **Page / Target**: `My details`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Passed` | **Test Type**: `Functional`
- **Traceability**: FS R8 field table (Mobile) - equivalence partitioning
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
FA logged in
```

**Test Data:**
```text
61234567; 81234567; 91234567
```

**Test Steps:**
1. For each value, enter it and click [Save]

**Expected Result:**
> Each value is saved with MSG-0807

**Actual Result:**
> Able to save

---

#### `TC-R8-099`: Verify invalid mobile numbers are rejected with MSG-0805

- **Scenario ID**: `TS-010`
- **Test Suite**: My Details
- **Page / Target**: `My details`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Failed` | **Test Type**: `Functional`
- **Traceability**: FR-08.3 errors; R8-AC15
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
FA logged in
```

**Test Data:**
```text
71234567 (starts 7); 51234567; 9123456 (7 digits); 912345678 (9 digits); 9123abcd; +6591234567
```

**Test Steps:**
1. For each value, enter it and click [Save]

**Expected Result:**
> MSG-0805 'Enter a mobile number in the correct format, like 9123 4567' is shown; nothing is saved

**Actual Result:**
> Able to save

---

#### `TC-R8-100`: Verify a mobile number entered with a space

- **Scenario ID**: `TS-010`
- **Test Suite**: My Details
- **Page / Target**: `My details`
- **Severity / Priority**: `S4 (lowest)` / `Low`
- **Execution Status**: `Failed` | **Test Type**: `Functional`
- **Traceability**: FS R8 field table (example format)
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API
- **Assumption Reference**: ASM-08: Mobile number entered with a space ('9123 4567') is accepted and stored without the space.

**Preconditions:**
```text
FA logged in
```

**Test Data:**
```text
9123 4567
```

**Test Steps:**
1. Enter '9123 4567'
2. Click [Save]
3. Check the stored value

**Expected Result:**
> Saved with MSG-0807; stored as 91234567

**Actual Result:**
> Save with space

---

#### `TC-R8-101`: Verify invalid email formats are rejected with MSG-0806

- **Scenario ID**: `TS-010`
- **Test Suite**: My Details
- **Page / Target**: `My details`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Failed` | **Test Type**: `Functional`
- **Traceability**: FR-08.3 errors; R8-AC15
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
FA logged in
```

**Test Data:**
```text
nameexample.com; name@; @example.com; name@example; name @example.com
```

**Test Steps:**
1. For each value, enter it and click [Save]

**Expected Result:**
> MSG-0806 'Enter an email address in the correct format, like name@example.com' is shown; nothing is saved

**Actual Result:**
> Enter an email address in the correct format.

---

#### `TC-R8-102`: Verify email length limit of 150 characters

- **Scenario ID**: `TS-010`
- **Test Suite**: My Details
- **Page / Target**: `My details`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Passed` | **Test Type**: `Functional`
- **Traceability**: FS R8 field table (Email max 150) - boundary
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API
- **Assumption Reference**: ASM-09: No message code is defined for max-length / postal-code errors; assumed field-level validation blocks Save and shows an inline error.

**Preconditions:**
```text
FA logged in
```

**Test Data:**
```text
Email of 150 chars (a x 138 + '@example.com'); email of 151 chars
```

**Test Steps:**
1. Enter the 150-char email, click [Save]
2. Enter the 151-char email, click [Save]

**Expected Result:**
> 150 chars: saved with MSG-0807
> 151 chars: not saved; error shown

**Actual Result:**
> 150 chars: saved with MSG-0807
151 chars: not saved; error shown

---

#### `TC-R8-103`: Verify each blank required field shows MSG-0001

- **Scenario ID**: `TS-010`
- **Test Suite**: My Details
- **Page / Target**: `My details`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Failed` | **Test Type**: `Functional`
- **Traceability**: FR-08.3 errors; R8-AC16
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
FA logged in
```

**Test Data:**
```text
Clear: Mobile number, Email, Mailing street, Mailing postal code, Mailing country
```

**Test Steps:**
1. Clear all five required fields
2. Click [Save]

**Expected Result:**
> MSG-0001 shown under each blank field (e.g. 'Enter your email'); nothing is saved

**Actual Result:**
> Unable to clear required field

---

#### `TC-R8-104`: Verify whitespace-only input is treated as blank

- **Scenario ID**: `TS-010`
- **Test Suite**: My Details
- **Page / Target**: `My details`
- **Severity / Priority**: `S4 (lowest)` / `Low`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FR-08.3 errors
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API
- **Assumption Reference**: ASM-15: Whitespace-only input in a required field is treated as blank.

**Preconditions:**
```text
FA logged in
```

**Test Data:**
```text
Mailing street = ' '
```

**Test Steps:**
1. Enter spaces only in Mailing street
2. Click [Save]

**Expected Result:**
> MSG-0001 for Mailing street; nothing is saved

---

#### `TC-R8-105`: Verify optional mailing block and unit can be left blank

- **Scenario ID**: `TS-010`
- **Test Suite**: My Details
- **Page / Target**: `My details`
- **Severity / Priority**: `S4 (lowest)` / `Low`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FS R8 field table (block, unit optional)
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
FA logged in
```

**Test Data:**
```text
Mailing block = blank; unit = blank; other fields valid
```

**Test Steps:**
1. Clear block and unit
2. Click [Save]

**Expected Result:**
> Saved with MSG-0807

---

#### `TC-R8-106`: Verify mailing block and unit length limit of 20 characters

- **Scenario ID**: `TS-010`
- **Test Suite**: My Details
- **Page / Target**: `My details`
- **Severity / Priority**: `S4 (lowest)` / `Low`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FS R8 field table - boundary
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API
- **Assumption Reference**: ASM-09: No message code is defined for max-length / postal-code errors; assumed field-level validation blocks Save and shows an inline error.

**Preconditions:**
```text
FA logged in
```

**Test Data:**
```text
Block: 20 chars, then 21 chars; Unit: 20 chars, then 21 chars
```

**Test Steps:**
1. Save with 20-char values
2. Save with 21-char values

**Expected Result:**
> 20 chars saved; 21 chars blocked with an error

---

#### `TC-R8-107`: Verify mailing street and country length limit of 100 characters

- **Scenario ID**: `TS-010`
- **Test Suite**: My Details
- **Page / Target**: `My details`
- **Severity / Priority**: `S4 (lowest)` / `Low`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FS R8 field table - boundary
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API
- **Assumption Reference**: ASM-09: No message code is defined for max-length / postal-code errors; assumed field-level validation blocks Save and shows an inline error.

**Preconditions:**
```text
FA logged in
```

**Test Data:**
```text
Street and country: 100 chars, then 101 chars
```

**Test Steps:**
1. Save with 100-char values
2. Save with 101-char values

**Expected Result:**
> 100 chars saved; 101 chars blocked with an error

---

#### `TC-R8-108`: Verify mailing postal code must be exactly 6 digits

- **Scenario ID**: `TS-010`
- **Test Suite**: My Details
- **Page / Target**: `My details`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FS R8 field table (postal code)
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API
- **Assumption Reference**: ASM-09: No message code is defined for max-length / postal-code errors; assumed field-level validation blocks Save and shows an inline error.

**Preconditions:**
```text
FA logged in
```

**Test Data:**
```text
650009 (valid); 65000 (5 digits); 6500091 (7 digits); 65A009
```

**Test Steps:**
1. For each value, enter it and click [Save]

**Expected Result:**
> Only 650009 is saved; others are blocked with an error

---

#### `TC-R8-109`: Verify a system error on save shows MSG-0808 and keeps the old data

- **Scenario ID**: `TS-010`
- **Test Suite**: My Details
- **Page / Target**: `My details`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FR-08.3 errors; R8-AC17
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API
- **Note**: Needs Dev support for fault injection

**Preconditions:**
```text
FA logged in; profile update API forced to fail (fault injection)
```

**Test Data:**
```text
Phone 98887777
```

**Test Steps:**
1. Change phone to 98887777
2. Click [Save]
3. Reload My details

**Expected Result:**
> MSG-0808 'We could not update your details. Please try again.' is shown
> Phone remains 91234567

---

#### `TC-R8-110`: Verify My details is view-only when all children are 16+

- **Scenario ID**: `TS-010`
- **Test Suite**: My Details
- **Page / Target**: `My details`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FR-08.3 precondition; R8-AC09
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
Parent PE: all children aged 16+
```

**Test Data:**
```text
Parent PE: S7000007G; children E1 age 16, E2 age 17
```

**Test Steps:**
1. Log in as PE
2. Open My details
3. Call the profile update API

**Expected Result:**
> All fields read-only; no [Save] button
> API update is rejected

---

#### `TC-R8-111`: Verify My details is editable when at least one child is under 16

- **Scenario ID**: `TS-010`
- **Test Suite**: My Details
- **Page / Target**: `My details`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FR-08.3 precondition
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
Parent PB: B1 age 16, B2 age 14
```

**Test Data:**
```text
Parent PB
```

**Test Steps:**
1. Log in as PB
2. Open My details

**Expected Result:**
> Contact fields are editable and [Save] is shown

---

#### `TC-R8-112`: Verify a parent cannot update another parent's profile via the API

- **Scenario ID**: `TS-010`
- **Test Suite**: My Details
- **Page / Target**: `API`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Security`
- **Traceability**: FR-08.3 rules (own data only); NFR Security
- **Environment**: SIT
API client (Postman) + Chrome DevTools
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
FA logged in; MA's Parent_Profile Id known
```

**Test Data:**
```text
Target: MA's profile Id
```

**Test Steps:**
1. Send the profile update API with MA's Id using FA's token
2. Check MA's profile

**Expected Result:**
> Request rejected with MSG-0003 / 403; MA's profile unchanged

---

#### `TC-R8-113`: Verify father's update does not change mother's details

- **Scenario ID**: `TS-010`
- **Test Suite**: My Details
- **Page / Target**: `My details`
- **Severity / Priority**: `S2` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FR-08.3 rules
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
FA and MA both logged in before
```

**Test Data:**
```text
FA new phone 98887777
```

**Test Steps:**
1. FA saves a new phone
2. Log in as MA and open My details

**Expected Result:**
> MA's phone is unchanged

---

#### `TC-R8-114`: Verify script input in mailing fields is not executed

- **Scenario ID**: `TS-010`
- **Test Suite**: My Details
- **Page / Target**: `My details`
- **Severity / Priority**: `S2` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Security`
- **Traceability**: NFR Security
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
FA logged in
```

**Test Data:**
```text
Mailing street: <script>alert(1)</script>
```

**Test Steps:**
1. Enter the value and click [Save]
2. Reload My details

**Expected Result:**
> No script runs; text is shown as plain text or rejected

---


### Test Suite: Authorization & Data Protection

#### `TC-R8-115`: Verify opening the Education Account of a child not linked to the parent

- **Scenario ID**: `TS-011`
- **Test Suite**: Authorization & Data Protection
- **Page / Target**: `Education Account`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Security`
- **Traceability**: FR-08.2 errors; NFR Security; R8-AC13; PB-07
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
FA logged in; B2 belongs to PB
```

**Test Data:**
```text
B2 student Id
```

**Test Steps:**
1. Replace the child Id in the Education Account URL with B2's Id

**Expected Result:**
> MSG-0003 'You do not have permission to perform this action.' is shown; no B2 data displayed

---

#### `TC-R8-116`: Verify EA and transaction APIs block access to unlinked children

- **Scenario ID**: `TS-011`
- **Test Suite**: Authorization & Data Protection
- **Page / Target**: `API`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Security`
- **Traceability**: NFR Security (server-side checks); PB-07
- **Environment**: SIT
API client (Postman) + Chrome DevTools
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
FA logged in
```

**Test Data:**
```text
B2 student Id and EA Id
```

**Test Steps:**
1. Call EA details API for B2 with FA's token
2. Call transactions API for B2
3. Call Home children API

**Expected Result:**
> Calls 1-2 return 403 with no B2 data; call 3 returns only A1 and A2

---

#### `TC-R8-117`: Verify the full NRIC never appears in URLs

- **Scenario ID**: `TS-011`
- **Test Suite**: Authorization & Data Protection
- **Page / Target**: `All pages`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Security`
- **Traceability**: NFR Security
- **Environment**: SIT
API client (Postman) + Chrome DevTools
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
FA logged in
```

**Test Data:**
```text
Father FA: NRIC S7000001A, Tan Wei Ming
Mother MA: NRIC S7000002B, Lim Mei Ling
Child A1: Tan Jia Hui, citizen, age 12, EA Active, balance S$250.00, BVP / P6 Integrity
Child A2: Tan Jun Kai, citizen, age 9, EA Active, balance S$80.00, BVP / P3 Harmony
```

**Test Steps:**
1. Go through Landing, SingPass callback, Home, Education Account, My details
2. Check address bar and DevTools Network request URLs

**Expected Result:**
> No full NRIC in any URL or query string

---

#### `TC-R8-118`: Verify application logs and error messages do not expose personal data

- **Scenario ID**: `TS-011`
- **Test Suite**: Authorization & Data Protection
- **Page / Target**: `Logs`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Security`
- **Traceability**: Test plan 3.8 (safe logs); NFR Security
- **Environment**: SIT
Chrome (latest) + DB read access
Build: TBC
Mock SingPass + mock data API
- **Note**: Audit log storage rules to be agreed separately

**Preconditions:**
```text
Run login, EA view, filter and profile save; trigger one validation error and one MSG-0809
```

**Test Data:**
```text
Father FA: NRIC S7000001A, Tan Wei Ming
Mother MA: NRIC S7000002B, Lim Mei Ling
Child A1: Tan Jia Hui, citizen, age 12, EA Active, balance S$250.00, BVP / P6 Integrity
Child A2: Tan Jun Kai, citizen, age 9, EA Active, balance S$80.00, BVP / P3 Harmony
```

**Test Steps:**
1. Perform the actions
2. Review application logs and error responses

**Expected Result:**
> No credentials, tokens, full NRIC, raw birth dates, contact details or balances in general logs or error bodies

---


### Test Suite: Audit Log

#### `TC-R8-119`: Verify a login is recorded in the audit log

- **Scenario ID**: `TS-012`
- **Test Suite**: Audit Log
- **Page / Target**: `Audit log`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: NFR Audit
- **Environment**: SIT
Chrome (latest) + DB read access
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
FA logs in
```

**Test Data:**
```text
Father FA: NRIC S7000001A, Tan Wei Ming
Mother MA: NRIC S7000002B, Lim Mei Ling
Child A1: Tan Jia Hui, citizen, age 12, EA Active, balance S$250.00, BVP / P6 Integrity
Child A2: Tan Jun Kai, citizen, age 9, EA Active, balance S$80.00, BVP / P3 Harmony
```

**Test Steps:**
1. Log in as FA
2. Query the audit log

**Expected Result:**
> Entry for FA's login with user and timestamp

---

#### `TC-R8-120`: Verify each data update from the API at login is audited

- **Scenario ID**: `TS-012`
- **Test Suite**: Audit Log
- **Page / Target**: `Audit log`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FR-08.1 rules; NFR Audit
- **Environment**: SIT
Chrome (latest) + DB read access
Build: TBC
Mock SingPass + mock data API
- **Assumption Reference**: ASM-01: FS R8 FR-08.1 refreshes child name, school, class, DOB, citizenship at each login. FS R1 v1.2 (sec. 3) says R8 only verifies the parent-student relationship and does not run a full student sync; the Government dataset has no school/class. Test follows FS R8; confirm with BA.

**Preconditions:**
```text
Data API has a new residential address for FA and a new class for A1
```

**Test Data:**
```text
Father FA: NRIC S7000001A, Tan Wei Ming
Mother MA: NRIC S7000002B, Lim Mei Ling
Child A1: Tan Jia Hui, citizen, age 12, EA Active, balance S$250.00, BVP / P6 Integrity
Child A2: Tan Jun Kai, citizen, age 9, EA Active, balance S$80.00, BVP / P3 Harmony
```

**Test Steps:**
1. Log in as FA
2. Query the audit log

**Expected Result:**
> Entries for each updated field: field, old value, new value, updated by, time

---

#### `TC-R8-121`: Verify a My details change is audited with old and new values

- **Scenario ID**: `TS-012`
- **Test Suite**: Audit Log
- **Page / Target**: `Audit log`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: FR-08.3; FS R8 Appendix A; NFR Audit; R8-AC14
- **Environment**: SIT
Chrome (latest) + DB read access
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
FA changes phone 91234567 -> 98887777
```

**Test Data:**
```text
Phone 98887777
```

**Test Steps:**
1. Save the new phone
2. Query the audit log

**Expected Result:**
> Entry: field PhoneNumber, old 91234567, new 98887777, user FA, time of save

---


### Test Suite: Non-functional

#### `TC-R8-122`: Verify Home loads within 3 seconds with 1,000 transactions

- **Scenario ID**: `TS-013`
- **Test Suite**: Non-functional
- **Page / Target**: `Home`
- **Severity / Priority**: `S2` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Performance`
- **Traceability**: NFR Performance
- **Environment**: SIT (perf-ready build)
Chrome (latest), DevTools Network
Build: TBC
Seeded 1,000 transactions
- **Note**: Candidate target; needs client approval (test plan 3.9)

**Preconditions:**
```text
A5 has 1,000 transactions; cache cleared
```

**Test Data:**
```text
1,000 seeded transactions
```

**Test Steps:**
1. Log in as A5's parent
2. Measure Home load time (DevTools) 5 times

**Expected Result:**
> Each load completes under 3 seconds

---

#### `TC-R8-123`: Verify Education Account loads within 3 seconds with 1,000 transactions

- **Scenario ID**: `TS-013`
- **Test Suite**: Non-functional
- **Page / Target**: `Education Account`
- **Severity / Priority**: `S2` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Performance`
- **Traceability**: NFR Performance
- **Environment**: SIT (perf-ready build)
Chrome (latest), DevTools Network
Build: TBC
Seeded 1,000 transactions
- **Note**: Candidate target; needs client approval (test plan 3.9)

**Preconditions:**
```text
A5 has 1,000 transactions
```

**Test Data:**
```text
1,000 seeded transactions
```

**Test Steps:**
1. Open A5's Education Account
2. Measure load time 5 times

**Expected Result:**
> Each load completes under 3 seconds (first page of 20 rows)

---

#### `TC-R8-124`: Verify Home, Education Account and My details are usable on a phone

- **Scenario ID**: `TS-013`
- **Test Suite**: Non-functional
- **Page / Target**: `Home / Education Account / My details`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `UI`
- **Traceability**: NFR Display
- **Environment**: SIT
Safari iOS 17 (iPhone 13, 390px) / Chrome Android
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
FA logged in on a phone
```

**Test Data:**
```text
Father FA: NRIC S7000001A, Tan Wei Ming
Mother MA: NRIC S7000002B, Lim Mei Ling
Child A1: Tan Jia Hui, citizen, age 12, EA Active, balance S$250.00, BVP / P6 Integrity
Child A2: Tan Jun Kai, citizen, age 9, EA Active, balance S$80.00, BVP / P3 Harmony
```

**Test Steps:**
1. Open Home, Education Account and My details
2. Use filters, pagination and Save

**Expected Result:**
> No horizontal page scroll; all content and buttons reachable and readable

---

#### `TC-R8-125`: Verify interface language and display formats

- **Scenario ID**: `TS-013`
- **Test Suite**: Non-functional
- **Page / Target**: `All pages`
- **Severity / Priority**: `S4 (lowest)` / `Low`
- **Execution Status**: `Not Run` | **Test Type**: `UI`
- **Traceability**: NFR Display; FR-08.2 rules
- **Environment**: SIT
Chrome (latest), Windows 11
Build: TBC
Mock SingPass + mock data API

**Preconditions:**
```text
FA logged in
```

**Test Data:**
```text
Father FA: NRIC S7000001A, Tan Wei Ming
Mother MA: NRIC S7000002B, Lim Mei Ling
Child A1: Tan Jia Hui, citizen, age 12, EA Active, balance S$250.00, BVP / P6 Integrity
Child A2: Tan Jun Kai, citizen, age 9, EA Active, balance S$80.00, BVP / P3 Harmony
```

**Test Steps:**
1. Review all R8 pages

**Expected Result:**
> Text in English; amounts in SGD; dates DD/MM/YYYY; Last updated DD/MM/YYYY HH:mm

---
