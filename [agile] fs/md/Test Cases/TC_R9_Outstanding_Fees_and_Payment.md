# R9: Outstanding Fees and Payment Engine — Sprint 1 Test Cases

> **Module**: R9 - Outstanding Fees and Payment
> **Specification Reference**: [FS-09_Outstanding_Fees_and_Payment.md](file:////home/baudui/Projects/automation-ui/[agile] fs/md/FS document/FS-09_Outstanding_Fees_and_Payment.md)
> **Source Spreadsheet**: `Test Cases + Defect sprint 1.xlsx` (Sheet `R9 TC`)
> **Total Test Cases**: 162

## Executive Test Suite Summary

| Test Suite | Scenario Count | Test Cases | Priorities | Severities |
| :--- | :--- | :--- | :--- | :--- |
| F9.1 Access and child list | 3 (TS-001, TS-002, TS-003) | 17 | Critical, High, Medium | S1 (highest), S2, S3 |
| F9.2 Outstanding invoices and EA balance | 3 (TS-004, TS-005, TS-006) | 17 | High, Low, Medium | S2, S3, S4 (lowest) |
| F9.3 Payment method and eligibility | 3 (TS-007, TS-008, TS-009) | 28 | Critical, High, Low, Medium | S1 (highest), S2, S3, S4 (lowest) |
| F9.4 Pay with Education Account | 3 (TS-010, TS-011, TS-012) | 14 | Critical, High, Medium | S1 (highest), S2, S3 |
| F9.4 and F9.5 Idempotency and concurrency | 2 (TS-013, TS-014) | 10 | Critical, High, Medium | S1 (highest), S2, S3 |
| F9.5 Pay online | 2 (TS-015, TS-016) | 10 | Critical, High, Medium | S1 (highest), S2, S3 |
| F9.4 and F9.5 Split payment | 2 (TS-017, TS-018) | 14 | Critical, High, Medium | S1 (highest), S2, S3 |
| F9.6 Webhook and reconciliation | 2 (TS-019, TS-020) | 14 | Critical, High, Medium | S1 (highest), S2, S3 |
| F9.7 Result, receipt and retry | 4 (TS-021, TS-022, TS-023, TS-024) | 20 | Critical, High, Medium | S1 (highest), S2, S3 |
| Data rules and constraints | 2 (TS-025, TS-026) | 18 | Critical, High, Low, Medium | S1 (highest), S2, S3, S4 (lowest) |

---

## Quick Reference Index Table

| Test Case ID | Scenario ID | Title | Page / Area | Priority | Severity | Type | Defect ID | Traceability |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| [`TC-001`](#tc-001) | `TS-001` | Parent signs in with Singpass and reaches the child list | SCR-01 Choose child | High | S2 | Functional |  | Tender R9; PB-09; FS F9: AC-01; Step 1; SCR-01 |
| [`TC-002`](#tc-002) | `TS-001` | Failed Singpass sign in creates no session | SCR-01 Choose child | High | S2 | Functional |  | Tender R9; PB-09; FS F9: Step 1 alternative flow; 5.1 AUTH_REQUIRED; SCR-01 |
| [`TC-003`](#tc-003) | `TS-001` | Cancelled Singpass sign in creates no session | SCR-01 Choose child | Medium | S3 | Functional |  | Tender R9; PB-09; FS F9: Step 1 alternative flow; SCR-01 |
| [`TC-004`](#tc-004) | `TS-002` | Child list shows name, school, level, class and outstanding label | SCR-01 Choose child | Medium | S3 | Functional |  | Tender R9; PB-09; FS F9: 4.1 SCR-01 (Student name, School Level Class, Has outstanding invoices); SCR-01; AC-01 |
| [`TC-005`](#tc-005) | `TS-002` | Label shows no outstanding invoices for a child without any | SCR-01 Choose child | Medium | S3 | Functional |  | Tender R9; PB-09; FS F9: 4.1 SCR-01 Has outstanding invoices; SCR-01 |
| [`TC-006`](#tc-006) | `TS-002` | Child list contains only the children linked to the Parent | SCR-01 Choose child | Critical | S1 (highest) | Functional |  | Tender R9; PB-09; FS F9: AC-01; BR-F9-01; DA-04; SCR-01 |
| [`TC-007`](#tc-007) | `TS-002` | Parent without any linked child sees the empty state | SCR-01 Choose child | Medium | S3 | Functional |  | Tender R9; PB-09; FS F9: Step 1 alternative flow; SCR-01 Empty |
| [`TC-008`](#tc-008) | `TS-002` | Parent with one child reaches that child | SCR-01 Choose child | Medium | S3 | Functional |  | Tender R9; PB-09; FS F9: Step 1 alternative flow; SCR-01; SCR-02 |
| [`TC-009`](#tc-009) | `TS-002` | Second guardian linked to the same child sees the same child and invoices | SCR-02 Outstanding fees | High | S2 | Functional |  | Tender R9; PB-09; FS F9: DA-04; AC-01; BR-F9-01; SCR-02 |
| [`TC-010`](#tc-010) | `TS-002` | System error while loading the child list shows a safe message | SCR-01 Choose child | Medium | S3 | Non-functional |  | Tender R9; PB-09; FS F9: 5.1 SYSTEM_ERROR; SCR-01 Error |
| [`TC-011`](#tc-011) | `TS-003` | Changing the student ID in the address is refused | SCR-02 Outstanding fees | Critical | S1 (highest) | Security |  | Tender R9; PB-09; FS F9: EX-01; AC-12; BR-F9-01; 5.1 FORBIDDEN_CHILD; SCR-02 |
| [`TC-012`](#tc-012) | `TS-003` | API call for the invoices of an unlinked student is refused | API: list invoices | Critical | S1 (highest) | Security |  | Tender R9; PB-09; FS F9: EX-01; AC-12; BR-F9-01 |
| [`TC-013`](#tc-013) | `TS-003` | API call to read an invoice of another family is refused | API: invoice detail | Critical | S1 (highest) | Security |  | Tender R9; PB-09; FS F9: BR-F9-01; EX-01; 5.1 FORBIDDEN_CHILD |
| [`TC-014`](#tc-014) | `TS-003` | API call to pay an invoice of another family is refused and nothing is debited | API: create payment | Critical | S1 (highest) | Security |  | Tender R9; PB-09; FS F9: BR-F9-01; EX-01; AC-12; 5.1 FORBIDDEN_CHILD |
| [`TC-015`](#tc-015) | `TS-003` | API call for the status or receipt of another family's payment is refused | API: transaction status and receipt | Critical | S1 (highest) | Security |  | Tender R9; PB-09; FS F9: BR-F9-01; AC-13; AC-12 |
| [`TC-016`](#tc-016) | `TS-003` | A guardian cannot open a child who is linked only to another Parent | SCR-02 Outstanding fees | Critical | S1 (highest) | Security |  | Tender R9; PB-09; FS F9: BR-F9-01; DA-04; EX-01 |
| [`TC-017`](#tc-017) | `TS-003` | Request without a session is sent to the sign in | API: list invoices | Critical | S1 (highest) | Security |  | Tender R9; PB-09; FS F9: 5.1 AUTH_REQUIRED; BR-F9-01 |
| [`TC-018`](#tc-018) | `TS-004` | Open invoices of the chosen child are listed with number, due date, status and amount | SCR-02 Outstanding fees | High | S2 | Functional |  | Tender R9; PB-09; FS F9: AC-01; Step 2; 4.1 SCR-02; SCR-02 |
| [`TC-019`](#tc-019) | `TS-004` | An invoice opens to its lines grouped by fee type with fee components and GST | SCR-02 Outstanding fees | High | S2 | Functional |  | Tender R9; PB-09; FS F9: Step 2; 4.1 SCR-02 (Fee type, Line description, Fee components); DA-05; SCR-02 |
| [`TC-020`](#tc-020) | `TS-004` | Invoice totals show Gross, Subsidy 0.00 and Net equal to Gross | SCR-02 Outstanding fees | High | S2 | Functional |  | Tender R9; PB-09; FS F9: BR-F9-08; DA-09; NQ-04; 4.1 SCR-02 (Gross, Subsidy, Net) |
| [`TC-021`](#tc-021) | `TS-004` | Amounts are shown in SGD with two decimals | SCR-02 Outstanding fees | Low | S4 (lowest) | UI |  | Tender R9; PB-09; FS F9: DA-10; 4.1 SCR-02 (Decimal(18,2), SGD) |
| [`TC-022`](#tc-022) | `TS-004` | Invoice due date is the earliest due date of its lines | SCR-02 Outstanding fees | Medium | S3 | Functional |  | Tender R9; PB-09; FS F9: 4.1 SCR-02 Due date |
| [`TC-023`](#tc-023) | `TS-004` | Switching to another child changes the invoice list | SCR-02 Outstanding fees | High | S2 | Functional |  | Tender R9; PB-09; FS F9: AC-01; SCR-02 action change child |
| [`TC-024`](#tc-024) | `TS-004` | Paid, Cancelled and Draft invoices are not in the list | SCR-02 Outstanding fees | High | S2 | Functional |  | Tender R9; PB-09; FS F9: AC-01; 4.1 SCR-02 Invoice status note (Draft does not show); Step 3 |
| [`TC-025`](#tc-025) | `TS-004` | An invoice waiting for payment is shown as Pending and cannot be selected | SCR-02 Outstanding fees | High | S2 | Functional |  | Tender R9; PB-09; FS F9: AC-11; DA-05; 4.1 SCR-02 Selected invoice (only Issued, no open transaction); BR-F9-09 |
| [`TC-026`](#tc-026) | `TS-004` | An invoice past its due date is listed and can be paid | SCR-02 Outstanding fees | Medium | S3 | Functional |  | Tender R9; PB-09; FS F9: 4.1 SCR-02 Due date; NQ-03; OQ-04 |
| [`TC-027`](#tc-027) | `TS-004` | Demo data is labelled as sample data | SCR-02 Outstanding fees | Medium | S3 | UI |  | Tender R9; PB-09; FS F9: DA-11; OQ-04; OQ-08 |
| [`TC-028`](#tc-028) | `TS-005` | A child with an Active EA shows balance and status | SCR-02 Outstanding fees | High | S2 | Functional |  | Tender R9; PB-09; FS F9: Step 2; 4.1 SCR-02 (EA balance, EA status); SCR-02 |
| [`TC-029`](#tc-029) | `TS-005` | A child without an EA shows no balance and a note | SCR-02 Outstanding fees | High | S2 | Functional |  | Tender R9; PB-09; FS F9: Step 2 alternative flow; DA-03; 4.1 SCR-02 EA balance |
| [`TC-030`](#tc-030) | `TS-005` | A child with a Closed EA shows the status Closed | SCR-02 Outstanding fees | Medium | S3 | Functional |  | Tender R9; PB-09; FS F9: 4.1 SCR-02 EA status (only Active can pay); DA-06 |
| [`TC-031`](#tc-031) | `TS-005` | A zero EA balance is shown as 0.00 | SCR-02 Outstanding fees | Low | S4 (lowest) | UI |  | Tender R9; PB-09; FS F9: 4.1 SCR-02 EA balance |
| [`TC-032`](#tc-032) | `TS-006` | A child with no Issued invoice shows the empty state | SCR-03 No outstanding fees | High | S2 | Functional |  | Tender R9; PB-09; FS F9: AC-02; Step 3; SCR-03 |
| [`TC-033`](#tc-033) | `TS-006` | The empty state links back to the child list and another child can be chosen | SCR-03 No outstanding fees | Medium | S3 | Functional |  | Tender R9; PB-09; FS F9: Step 3; SCR-03 action back to SCR-01 |
| [`TC-034`](#tc-034) | `TS-006` | A child whose only open invoice is waiting for payment is not shown the empty state | SCR-02 Outstanding fees | High | S2 | Functional |  | Tender R9; PB-09; FS F9: AC-11; AC-02; Step 3; SCR-02; SCR-03 |
| [`TC-035`](#tc-035) | `TS-007` | Selecting an Issued invoice opens the payment method screen with its summary | SCR-04 Choose payment method | High | S2 | Functional |  | Tender R9; PB-10, PB-11; FS F9: Step 4; SCR-04; DA-07 |
| [`TC-036`](#tc-036) | `TS-007` | Only one whole invoice can be selected and lines cannot be paid separately | SCR-02 Outstanding fees | High | S2 | Functional |  | Tender R9; PB-10, PB-11; FS F9: DA-05; DA-07; BR-F9-13; OOS 1 and 2; NQ-09 |
| [`TC-037`](#tc-037) | `TS-007` | Back from the payment method screen returns to the invoice list and creates nothing | SCR-04 Choose payment method | Medium | S3 | Functional |  | Tender R9; PB-10, PB-11; FS F9: Appendix C SCR-04 actions; BR-F9-10 |
| [`TC-038`](#tc-038) | `TS-008` | Student without an EA can pay online only | SCR-04 Choose payment method | High | S2 | Functional |  | Tender R9; PB-10, PB-11; FS F9: AC-14; BR-F9-07; DA-03; 5.1 EA_NOT_AVAILABLE; SCR-04 |
| [`TC-039`](#tc-039) | `TS-008` | Student with a Closed EA can pay online only | SCR-04 Choose payment method | High | S2 | Functional |  | Tender R9; PB-10, PB-11; FS F9: DA-06; BR-F9-02; 5.1 EA_NOT_ACTIVE; SCR-04 |
| [`TC-040`](#tc-040) | `TS-008` | Active EA with zero balance offers online payment only | SCR-04 Choose payment method | High | S2 | Functional |  | Tender R9; PB-10, PB-11; FS F9: BR-F9-02; Step 4; 5.1 EA_INSUFFICIENT_BALANCE; SCR-04 |
| [`TC-041`](#tc-041) | `TS-008` | Balance below the amount to pay disables EA and suggests split | SCR-04 Choose payment method | Critical | S1 (highest) | Functional |  | Tender R9; PB-10, PB-11; FS F9: AC-04; AC-22; BR-F9-02; Step 4; 5.1 EA_INSUFFICIENT_BALANCE; SCR-04 |
| [`TC-042`](#tc-042) | `TS-008` | Balance equal to the amount to pay allows EA and online but not split | SCR-04 Choose payment method | High | S2 | Functional |  | Tender R9; PB-10, PB-11; FS F9: BR-F9-02; Step 4 (balance equal to or higher than the amount); SCR-04 |
| [`TC-043`](#tc-043) | `TS-008` | Balance above the amount to pay allows EA and online but not split | SCR-04 Choose payment method | High | S2 | Functional |  | Tender R9; PB-10, PB-11; FS F9: Step 4; BR-F9-02; DA-07; SCR-04 |
| [`TC-044`](#tc-044) | `TS-008` | Balance one cent below the amount to pay offers split with an online part of 0.01 | SCR-04 Choose payment method | Medium | S3 | Functional |  | Tender R9; PB-10, PB-11; FS F9: BR-F9-02; Step 4; Step 5.2; 4.1 SCR-04 Online amount |
| [`TC-045`](#tc-045) | `TS-008` | The EA is suggested when the balance is enough but nothing is debited until the Parent confirms | SCR-04 Choose payment method | Critical | S1 (highest) | Functional |  | Tender R9; PB-10, PB-11; FS F9: BR-F9-10; DA-08; Step 4 |
| [`TC-046`](#tc-046) | `TS-008` | Selecting EA with a low balance is refused with the reason and nothing changes | SCR-04 Choose payment method | Critical | S1 (highest) | Functional |  | Tender R9; PB-10, PB-11; FS F9: AC-04; Step 5.3; 5.1 EA_INSUFFICIENT_BALANCE |
| [`TC-047`](#tc-047) | `TS-008` | API refuses the EA method when the balance is too low | API: create payment | Critical | S1 (highest) | API |  | Tender R9; PB-10, PB-11; FS F9: AC-04; BR-F9-02; Step 5.1; 5.1 EA_INSUFFICIENT_BALANCE |
| [`TC-048`](#tc-048) | `TS-008` | API refuses EA and split for a student without an EA | API: create payment | Critical | S1 (highest) | API |  | Tender R9; PB-10, PB-11; FS F9: BR-F9-07; DA-03; BR-F9-02; 5.1 EA_NOT_AVAILABLE |
| [`TC-049`](#tc-049) | `TS-008` | API refuses EA and split when the EA is Closed | API: create payment | Critical | S1 (highest) | API |  | Tender R9; PB-10, PB-11; FS F9: DA-06; BR-F9-02; Step 5.1; 5.1 EA_NOT_ACTIVE |
| [`TC-050`](#tc-050) | `TS-009` | Default split proposes the whole balance as the EA part and calculates the online part | SCR-04 Choose payment method | Critical | S1 (highest) | Functional |  | Tender R9; PB-10, PB-11; FS F9: AC-22; Step 4; BR-F9-02; BR-F9-10; 4.1 SCR-04 EA amount and Online amount |
| [`TC-051`](#tc-051) | `TS-009` | The Parent can lower the EA part and the online part updates | SCR-04 Choose payment method | High | S2 | Functional |  | Tender R9; PB-10, PB-11; FS F9: AC-22; DA-08; BR-F9-10; 4.1 SCR-04 |
| [`TC-052`](#tc-052) | `TS-009` | The online part cannot be typed by the Parent | SCR-04 Choose payment method | Medium | S3 | UI |  | Tender R9; PB-10, PB-11; FS F9: 4.1 SCR-04 Online amount (input: No); Step 4 |
| [`TC-053`](#tc-053) | `TS-009` | An EA part of zero is refused and the Parent stays on the screen | SCR-04 Choose payment method | High | S2 | Functional |  | Tender R9; PB-10, PB-11; FS F9: AC-19; BR-F9-11; 5.1 SPLIT_AMOUNT_INVALID |
| [`TC-054`](#tc-054) | `TS-009` | API refuses a split with an online part of zero | API: create payment | Critical | S1 (highest) | API |  | Tender R9; PB-10, PB-11; FS F9: AC-19; BR-F9-11; 5.1 SPLIT_AMOUNT_INVALID |
| [`TC-055`](#tc-055) | `TS-009` | API refuses a split whose parts add up to less than the amount to pay | API: create payment | Critical | S1 (highest) | API |  | Tender R9; PB-10, PB-11; FS F9: AC-19; BR-F9-11; BR-F9-13; 5.1 SPLIT_AMOUNT_INVALID |
| [`TC-056`](#tc-056) | `TS-009` | API refuses a split whose parts add up to more than the amount to pay | API: create payment | Critical | S1 (highest) | API |  | Tender R9; PB-10, PB-11; FS F9: AC-19; BR-F9-11; BR-F9-13; 5.1 SPLIT_AMOUNT_INVALID |
| [`TC-057`](#tc-057) | `TS-009` | API refuses an EA part above the available balance | API: create payment | Critical | S1 (highest) | API |  | Tender R9; PB-10, PB-11; FS F9: Step 5.1; 4.1 SCR-04 EA amount (not above the available balance); 5.1 EA_INSUFFICIENT_BALANCE |
| [`TC-058`](#tc-058) | `TS-009` | API refuses a negative EA part | API: create payment | High | S2 | API |  | Tender R9; PB-10, PB-11; FS F9: AC-19; BR-F9-11; 4.1 SCR-04 EA amount (more than 0) |
| [`TC-059`](#tc-059) | `TS-009` | An EA part with more than two decimals or with text is refused | SCR-04 Choose payment method | Medium | S3 | Functional |  | Tender R9; PB-10, PB-11; FS F9: 4.1 SCR-04 EA amount (Decimal(18,2)); VAL-18 |
| [`TC-060`](#tc-060) | `TS-009` | Online part exactly at the provider minimum is accepted | API: create payment | Medium | S3 | Functional |  | Tender R9; PB-10, PB-11; FS F9: Step 5.2; 4.1 SCR-04 Online amount; NQ-13 |
| [`TC-061`](#tc-061) | `TS-009` | Online part just below the provider minimum is refused | API: create payment | Medium | S3 | API |  | Tender R9; PB-10, PB-11; FS F9: Step 5.2; 4.1 SCR-04 Online amount; NQ-13 |
| [`TC-062`](#tc-062) | `TS-009` | A very small EA part is accepted because the EA part has no minimum | SCR-04 Choose payment method | Low | S4 (lowest) | Functional |  | Tender R9; PB-10, PB-11; FS F9: NQ-13 (no minimum for the EA part); BR-F9-11; 4.1 SCR-04 |
| [`TC-063`](#tc-063) | `TS-010` | Review screen for an EA payment shows the amounts and the balance after payment | SCR-05 Review and confirm | High | S2 | Functional |  | Tender R9; PB-10; FS F9: Step 6.1; 4.1 SCR-05 (Amount to pay, EA balance after payment); SCR-05 |
| [`TC-064`](#tc-064) | `TS-010` | Cancel on the review screen returns to the payment method screen and creates nothing | SCR-05 Review and confirm | Medium | S3 | Functional |  | Tender R9; PB-10; FS F9: Appendix C SCR-05 actions; BR-F9-10 |
| [`TC-065`](#tc-065) | `TS-011` | Paying a 50.00 invoice with the EA debits the balance once and marks the invoice Paid | SCR-07 Payment confirmation | Critical | S1 (highest) | Functional |  | Tender R9; PB-10; FS F9: AC-03; BR-F9-03; BR-F9-13; DA-02; Step 6.3; 4.2 FundingLeg; SCR-07 |
| [`TC-066`](#tc-066) | `TS-011` | Status changes of an EA payment follow Appendix A and are written to the audit log | Audit log | High | S2 | Integration |  | Tender R9; PB-10; FS F9: Appendix A; 4.2 AuditLog; DA-12; Step 6.3 |
| [`TC-067`](#tc-067) | `TS-011` | Paying a two line invoice of 130.00 debits the full Net amount | SCR-07 Payment confirmation | High | S2 | Functional |  | Tender R9; PB-10; FS F9: BR-F9-13; DA-05; AC-03; 4.2 Transaction RequestedAmount |
| [`TC-068`](#tc-068) | `TS-011` | Balance equal to the amount to pay is paid and the balance becomes 0.00 | SCR-07 Payment confirmation | Critical | S1 (highest) | Functional |  | Tender R9; PB-10; FS F9: AC-03; AC-06 (balance not negative); BR-F9-02 |
| [`TC-069`](#tc-069) | `TS-011` | The EA pays each of the four fee types | SCR-07 Payment confirmation | Medium | S3 | Functional |  | Tender R9; PB-10; FS F9: OQ-11; 4.1 SCR-02 Fee type; BR-F9-02 |
| [`TC-070`](#tc-070) | `TS-011` | After an EA payment the list shows the new balance and no longer shows the invoice | SCR-02 Outstanding fees | High | S2 | Functional |  | Tender R9; PB-10; FS F9: AC-03; SCR-07 action back to SCR-02 |
| [`TC-071`](#tc-071) | `TS-012` | Balance falling below the amount before confirm fails the EA leg and changes nothing | SCR-08 Payment failed | Critical | S1 (highest) | Functional |  | Tender R9; PB-10; FS F9: EX-05; AC-04; Step 6.3; 5.1 EA_INSUFFICIENT_BALANCE; Appendix A |
| [`TC-072`](#tc-072) | `TS-012` | Function 1 error during the debit fails the payment and the invoice is not Paid | SCR-08 Payment failed | Critical | S1 (highest) | Functional |  | Tender R9; PB-10; FS F9: EX-10; AC-07; Step 6.3; 5.1 PAYMENT_FAILED; SCR-08 |
| [`TC-073`](#tc-073) | `TS-012` | Unclear debit result with Function 1 confirming nothing was debited fails the leg | SCR-08 Payment failed | Critical | S1 (highest) | Functional |  | Tender R9; PB-10; FS F9: BR-F9-03; AC-07; EX-10 |
| [`TC-074`](#tc-074) | `TS-012` | Unclear debit result with Function 1 confirming the debit leads to a reversal | SCR-08 Payment failed | Critical | S1 (highest) | Functional |  | Tender R9; PB-10; FS F9: BR-F9-03; AC-07; EX-10; Appendix A |
| [`TC-075`](#tc-075) | `TS-012` | Unclear debit result that stays unclear moves to ReconciliationRequired | SCR-06 Pending | Critical | S1 (highest) | Functional |  | Tender R9; PB-10; FS F9: BR-F9-03; EX-10; AC-07; Step 7.6; Appendix A; SCR-06 Verifying |
| [`TC-076`](#tc-076) | `TS-012` | Function 1 treats the same FundingReference as one debit | Function 1 debit API | Critical | S1 (highest) | Integration |  | Tender R9; PB-10; FS F9: BR-F9-03; DA-12; NQ-15 |
| [`TC-077`](#tc-077) | `TS-013` | Double click on Confirm creates one transaction and debits once | SCR-05 Review and confirm | Critical | S1 (highest) | Functional |  | Tender R9; PB-10, PB-11; FS F9: AC-05; BR-F9-04; Step 6.2; SCR-05 Processing |
| [`TC-078`](#tc-078) | `TS-013` | The same request sent again with the same key returns the first result | API: create payment | Critical | S1 (highest) | API |  | Tender R9; PB-10, PB-11; FS F9: BR-F9-04; AC-05; Step 7 Retry |
| [`TC-079`](#tc-079) | `TS-013` | The same key can be used by two different Parents | API: create payment | High | S2 | API |  | Tender R9; PB-10, PB-11; FS F9: 4.2 Transaction IdempotencyKey (unique per InitiatedByUserId and key); SCR-05 Idempotency key |
| [`TC-080`](#tc-080) | `TS-013` | A key of 100 characters is accepted | API: create payment | Medium | S3 | API |  | Tender R9; PB-10, PB-11; FS F9: 4.1 SCR-05 Idempotency key (up to 100 characters); 4.2 Transaction IdempotencyKey VARCHAR(100) |
| [`TC-081`](#tc-081) | `TS-013` | A key that is missing, empty or 101 characters long is refused | API: create payment | Medium | S3 | API |  | Tender R9; PB-10, PB-11; FS F9: 4.1 SCR-05 Idempotency key (required, up to 100 characters); BR-F9-04 |
| [`TC-082`](#tc-082) | `TS-014` | Two requests at the same time for one invoice give one payment and one refusal | API: create payment | Critical | S1 (highest) | API |  | Tender R9; PB-10, PB-11; FS F9: EX-03; AC-06; BR-F9-09; DA-13; 5.1 PAYMENT_PENDING |
| [`TC-083`](#tc-083) | `TS-014` | Two guardians confirming the same invoice at the same time give one payment | SCR-05 Review and confirm | Critical | S1 (highest) | Functional |  | Tender R9; PB-10, PB-11; FS F9: EX-03; AC-06; DA-04; BR-F9-04; BR-F9-09 |
| [`TC-084`](#tc-084) | `TS-014` | Confirming an invoice that was paid meanwhile is refused | SCR-05 Review and confirm | Critical | S1 (highest) | Functional |  | Tender R9; PB-10, PB-11; FS F9: EX-04; BR-F9-04; DA-13; 5.1 INVOICE_ALREADY_PAID |
| [`TC-085`](#tc-085) | `TS-014` | Confirming an invoice that is waiting for another payment is refused | SCR-06 Pending | Critical | S1 (highest) | Functional |  | Tender R9; PB-10, PB-11; FS F9: EX-04; BR-F9-09; AC-11; 5.1 PAYMENT_PENDING |
| [`TC-086`](#tc-086) | `TS-014` | Confirming an invoice that was cancelled meanwhile is refused | SCR-05 Review and confirm | Critical | S1 (highest) | Functional |  | Tender R9; PB-10, PB-11; FS F9: AC-21; EX-14; EX-04; 5.1 INVOICE_NOT_PAYABLE |
| [`TC-087`](#tc-087) | `TS-015` | Review screen for an online payment has no EA part | SCR-05 Review and confirm | Medium | S3 | Functional |  | Tender R9; PB-11; FS F9: Step 6.1; 4.1 SCR-05; SCR-05 |
| [`TC-088`](#tc-088) | `TS-015` | A student without an EA pays online and the invoice becomes Paid | SCR-07 Payment confirmation | Critical | S1 (highest) | Functional |  | Tender R9; PB-11; FS F9: AC-08; AC-14; BR-F9-07; DA-01; Step 6.3 online; Step 7.3; BR-F9-13 |
| [`TC-089`](#tc-089) | `TS-015` | A student with an EA who pays online keeps the EA balance | SCR-07 Payment confirmation | Critical | S1 (highest) | Functional |  | Tender R9; PB-11; FS F9: BR-F9-10; DA-08; AC-08; DA-02 |
| [`TC-090`](#tc-090) | `TS-016` | Provider failure returns the invoice to Issued and nothing is charged | SCR-08 Payment failed | Critical | S1 (highest) | Functional |  | Tender R9; PB-11; FS F9: AC-09; BR-F9-05; Step 7.5; 5.1 PAYMENT_FAILED; SCR-08 |
| [`TC-091`](#tc-091) | `TS-016` | Cancel on the provider page returns the invoice to Issued | SCR-08 Payment failed | Critical | S1 (highest) | Functional |  | Tender R9; PB-11; FS F9: AC-09; Step 7.5; Appendix A; 5.1 PAYMENT_CANCELLED; SCR-08 |
| [`TC-092`](#tc-092) | `TS-016` | An expired provider payment session fails the online leg | SCR-08 Payment failed | High | S2 | Functional |  | Tender R9; PB-11; FS F9: EX-02; Appendix A; Step 7.5 |
| [`TC-093`](#tc-093) | `TS-016` | A provider that refuses to open the payment session fails the payment | SCR-08 Payment failed | High | S2 | Functional |  | Tender R9; PB-11; FS F9: Step 6.3 online; BR-F9-05; EX-08 |
| [`TC-094`](#tc-094) | `TS-016` | Closing the browser on the provider page keeps the payment Pending until the result arrives | SCR-06 Pending | High | S2 | Functional |  | Tender R9; PB-11; FS F9: EX-09; AC-11; BR-F9-09; Step 7.2 |
| [`TC-095`](#tc-095) | `TS-016` | A provider timeout keeps the leg Pending and does not mark it Failed | SCR-06 Pending | High | S2 | Functional |  | Tender R9; PB-11; FS F9: EX-08; Step 7.1 |
| [`TC-096`](#tc-096) | `TS-016` | No card data is stored after an online payment | Database and logs | Critical | S1 (highest) | Security |  | Tender R9; PB-11; FS F9: DA-01; BR-F9-06; 4.2 WebhookReceipt PayloadHash |
| [`TC-097`](#tc-097) | `TS-017` | Split of EA 20.00 and online 30.00 pays a 50.00 invoice | SCR-07 Payment confirmation | Critical | S1 (highest) | Functional |  | Tender R9; PB-10, PB-11; FS F9: AC-15; AC-22; BR-F9-11; BR-F9-13; DA-12; Step 7.3; SCR-07 |
| [`TC-098`](#tc-098) | `TS-017` | The EA is debited before the online payment session is created | Function 1 and provider calls | Critical | S1 (highest) | Integration |  | Tender R9; PB-10, PB-11; FS F9: BR-F9-11; Step 6.3 split; DA-14; Appendix A |
| [`TC-099`](#tc-099) | `TS-017` | Split with a lowered EA part of 10.00 and an online part of 40.00 pays the invoice | SCR-07 Payment confirmation | High | S2 | Functional |  | Tender R9; PB-10, PB-11; FS F9: AC-22; DA-08; BR-F9-11 |
| [`TC-100`](#tc-100) | `TS-017` | Review screen for a split shows both parts and the balance after payment | SCR-05 Review and confirm | High | S2 | Functional |  | Tender R9; PB-10, PB-11; FS F9: Step 6.1; 4.1 SCR-05; AC-22 |
| [`TC-101`](#tc-101) | `TS-017` | While the online part is pending the waiting screen says the EA part is already taken | SCR-06 Pending | High | S2 | Functional |  | Tender R9; PB-10, PB-11; FS F9: Appendix C SCR-06; EX-09; AC-11; Step 7.2 |
| [`TC-102`](#tc-102) | `TS-018` | EA debit fails before the online part: no payment session and no online charge | SCR-04 Choose payment method | Critical | S1 (highest) | Functional |  | Tender R9; PB-10, PB-11; FS F9: AC-16; EX-05; Step 6.3 split; 5.1 EA_INSUFFICIENT_BALANCE |
| [`TC-103`](#tc-103) | `TS-018` | Online failure after the EA debit returns the EA part | SCR-08 Payment failed | Critical | S1 (highest) | Functional |  | Tender R9; PB-10, PB-11; FS F9: AC-17; BR-F9-05; BR-F9-11; Step 7.4; Appendix A; 5.1 PAYMENT_FAILED_EA_RETURNED |
| [`TC-104`](#tc-104) | `TS-018` | Cancel at the provider after the EA debit returns the EA part | SCR-08 Payment failed | Critical | S1 (highest) | Functional |  | Tender R9; PB-10, PB-11; FS F9: AC-17; Appendix A; 5.1 PAYMENT_CANCELLED note; Step 7.4 |
| [`TC-105`](#tc-105) | `TS-018` | An expired provider session after the EA debit returns the EA part | SCR-08 Payment failed | Critical | S1 (highest) | Functional |  | Tender R9; PB-10, PB-11; FS F9: EX-02; AC-17; Step 7.4 |
| [`TC-106`](#tc-106) | `TS-018` | A provider that refuses the payment session after the EA debit returns the EA part | SCR-08 Payment failed | High | S2 | Functional |  | Tender R9; PB-10, PB-11; FS F9: BR-F9-05; BR-F9-11; Step 7.4 |
| [`TC-107`](#tc-107) | `TS-018` | A failed reversal moves the payment to ReconciliationRequired | SCR-06 Pending | Critical | S1 (highest) | Functional |  | Tender R9; PB-10, PB-11; FS F9: AC-18; EX-13; Step 7.6; Appendix A; SCR-06 Verifying |
| [`TC-108`](#tc-108) | `TS-018` | A failure after the EA debit and before the online session is cleaned up by the sweep | Orphan sweep job | High | S2 | Integration |  | Tender R9; PB-10, PB-11; FS F9: EX-11; BR-F9-05; DA-14 |
| [`TC-109`](#tc-109) | `TS-018` | The sweep leaves a split payment alone when the online leg exists | Orphan sweep job | Medium | S3 | Integration |  | Tender R9; PB-10, PB-11; FS F9: EX-11; BR-F9-11 |
| [`TC-110`](#tc-110) | `TS-018` | A late provider success after the EA was returned is not paid and goes to manual handling | SCR-06 Pending | Critical | S1 (highest) | Functional |  | Tender R9; PB-10, PB-11; FS F9: AC-20; EX-12; Appendix A; OOS 3; NQ-14 |
| [`TC-111`](#tc-111) | `TS-019` | A valid callback is recorded at once and processed later | Webhook endpoint | Critical | S1 (highest) | Integration |  | Tender R9; PB-11; FS F9: BR-F9-06; AC-10; AC-08; 4.2 WebhookReceipt (ProcessingStatus, ProcessedAt) |
| [`TC-112`](#tc-112) | `TS-019` | A callback with a wrong signature is rejected and changes nothing | Webhook endpoint | Critical | S1 (highest) | Security |  | Tender R9; PB-11; FS F9: EX-06; AC-10; BR-F9-06; 4.2 WebhookReceipt (only authenticated callbacks are stored) |
| [`TC-113`](#tc-113) | `TS-019` | A callback without a signature is rejected | Webhook endpoint | Critical | S1 (highest) | Security |  | Tender R9; PB-11; FS F9: BR-F9-06; EX-06; AC-10 |
| [`TC-114`](#tc-114) | `TS-019` | A callback whose content was changed after signing is rejected | Webhook endpoint | Critical | S1 (highest) | Security |  | Tender R9; PB-11; FS F9: BR-F9-06; EX-06 |
| [`TC-115`](#tc-115) | `TS-019` | The same event sent twice is applied once | Webhook endpoint | Critical | S1 (highest) | Integration |  | Tender R9; PB-11; FS F9: EX-07; AC-10; BR-F9-06; 4.2 WebhookReceipt (unique pair) |
| [`TC-116`](#tc-116) | `TS-019` | A new event for a payment that is already finished changes nothing | Webhook endpoint | High | S2 | Integration |  | Tender R9; PB-11; FS F9: Appendix A (no transition out of a final state); 4.2 WebhookReceipt ProcessingStatus |
| [`TC-117`](#tc-117) | `TS-019` | A valid callback that matches no payment is ignored | Webhook endpoint | Medium | S3 | Integration |  | Tender R9; PB-11; FS F9: 4.2 WebhookReceipt (FundingTransactionId after matching, ProcessingStatus) |
| [`TC-118`](#tc-118) | `TS-019` | A success callback with a different amount does not pay the invoice | Webhook endpoint | Critical | S1 (highest) | Integration |  | Tender R9; PB-11; FS F9: BR-F9-13; 4.2 Transaction (Settled equals Requested when Succeeded) |
| [`TC-119`](#tc-119) | `TS-019` | Only a hash of the callback is stored | Database and logs | High | S2 | Security |  | Tender R9; PB-11; FS F9: BR-F9-06; DA-01; 4.2 WebhookReceipt PayloadHash |
| [`TC-120`](#tc-120) | `TS-020` | A lost webhook is replaced by the provider status query: success | Reconciliation job | Critical | S1 (highest) | Integration |  | Tender R9; PB-11; FS F9: Step 7.1; Appendix A (online leg Pending to Succeeded: webhook or reconciliation) |
| [`TC-121`](#tc-121) | `TS-020` | A lost webhook is replaced by the provider status query: failure | Reconciliation job | High | S2 | Integration |  | Tender R9; PB-11; FS F9: Step 7.1; Step 7.5; Appendix A |
| [`TC-122`](#tc-122) | `TS-020` | A Pending leg that stays unclear beyond the threshold moves to ReconciliationRequired | SCR-06 Pending | Critical | S1 (highest) | Integration |  | Tender R9; PB-11; FS F9: EX-08; Step 7.6; NQ-10; Appendix A; SCR-06 Verifying |
| [`TC-123`](#tc-123) | `TS-020` | A webhook and a status query that arrive together are applied once | Reconciliation job | High | S2 | Integration |  | Tender R9; PB-11; FS F9: BR-F9-06; EX-07; Step 7.1 |
| [`TC-124`](#tc-124) | `TS-020` | Operations resolves a payment in ReconciliationRequired | Operations | High | S2 | Functional |  | Tender R9; PB-11; FS F9: Appendix A; AC-18; EX-13 |
| [`TC-125`](#tc-125) | `TS-021` | The waiting screen shows the pending notice, a temporary reference and the actions | SCR-06 Pending | High | S2 | Functional |  | Tender R9; PB-09, PB-10, PB-11; FS F9: Step 7.2; Appendix C SCR-06; 4.1 SCR-06 |
| [`TC-126`](#tc-126) | `TS-021` | Refreshing the waiting screen shows the success screen after the result arrives | SCR-06 Pending | High | S2 | Functional |  | Tender R9; PB-09, PB-10, PB-11; FS F9: Step 7.2; Step 7.3; SCR-06 action refresh |
| [`TC-127`](#tc-127) | `TS-021` | A Parent who comes back to a pending invoice cannot start a second payment | SCR-02 Outstanding fees | Critical | S1 (highest) | Functional |  | Tender R9; PB-09, PB-10, PB-11; FS F9: AC-11; BR-F9-09; EX-09; 5.1 PAYMENT_PENDING |
| [`TC-128`](#tc-128) | `TS-021` | The verifying state does not say the payment failed and offers no retry | SCR-06 Pending | High | S2 | UI |  | Tender R9; PB-09, PB-10, PB-11; FS F9: Step 7.6; 4.1 SCR-06 (ReconciliationRequired shown as verifying); Appendix C SCR-06 |
| [`TC-129`](#tc-129) | `TS-022` | The success screen of an EA payment shows reference, time, part and total | SCR-07 Payment confirmation | High | S2 | Functional |  | Tender R9; PB-09, PB-10, PB-11; FS F9: Step 7.3; 4.1 SCR-07; Appendix C SCR-07 |
| [`TC-130`](#tc-130) | `TS-022` | The success screen of a split payment shows both parts | SCR-07 Payment confirmation | High | S2 | Functional |  | Tender R9; PB-09, PB-10, PB-11; FS F9: AC-15; Step 7.3; 4.1 SCR-07 Settled amount |
| [`TC-131`](#tc-131) | `TS-022` | The receipt PDF of an EA payment can be downloaded | SCR-07 Payment confirmation | High | S2 | Functional |  | Tender R9; PB-09, PB-10, PB-11; FS F9: AC-13; SCR-07 action download |
| [`TC-132`](#tc-132) | `TS-022` | The receipt PDF of a split payment shows two parts | SCR-07 Payment confirmation | High | S2 | Functional |  | Tender R9; PB-09, PB-10, PB-11; FS F9: AC-13; AC-15 (receipt shows two parts) |
| [`TC-133`](#tc-133) | `TS-022` | The receipt can be printed | SCR-07 Payment confirmation | Medium | S3 | Functional |  | Tender R9; PB-09, PB-10, PB-11; FS F9: AC-13; SCR-07 action print |
| [`TC-134`](#tc-134) | `TS-022` | Transaction references are unique and follow the proposed format | SCR-07 Payment confirmation | Medium | S3 | Functional |  | Tender R9; PB-09, PB-10, PB-11; FS F9: 4.1 SCR-07 Transaction reference; 4.2 Transaction TransactionReference (unique); NQ-12 |
| [`TC-135`](#tc-135) | `TS-022` | The paid at time is shown in Singapore time | SCR-07 Payment confirmation | Medium | S3 | Functional |  | Tender R9; PB-09, PB-10, PB-11; FS F9: 4.1 SCR-07 Paid at (SGT); 4.2 Transaction CompletedAt (UTC) |
| [`TC-136`](#tc-136) | `TS-023` | The failure screen of an online payment shows the message, the reason and the actions | SCR-08 Payment failed | High | S2 | Functional |  | Tender R9; PB-09, PB-10, PB-11; FS F9: Step 7.5; 4.1 SCR-08; Appendix C SCR-08 |
| [`TC-137`](#tc-137) | `TS-023` | The failure screen of a split payment says the EA part was returned | SCR-08 Payment failed | High | S2 | Functional |  | Tender R9; PB-09, PB-10, PB-11; FS F9: Step 7.4; 5.1 PAYMENT_FAILED_EA_RETURNED; 4.1 SCR-08 Failure reason |
| [`TC-138`](#tc-138) | `TS-023` | The failure message hides technical details | SCR-08 Payment failed | High | S2 | Security |  | Tender R9; PB-09, PB-10, PB-11; FS F9: 4.1 SCR-08 Failure reason (no technical detail); 4.2 FundingLeg FailureReason; 5.1 |
| [`TC-139`](#tc-139) | `TS-023` | Exit on the failure screen returns to the invoice list with the invoice still Issued | SCR-02 Outstanding fees | Medium | S3 | Functional |  | Tender R9; PB-09, PB-10, PB-11; FS F9: Appendix C SCR-08 action exit; BR-F9-05 |
| [`TC-140`](#tc-140) | `TS-023` | Try again after a failure creates a new transaction with a new key and can succeed | SCR-07 Payment confirmation | Critical | S1 (highest) | Functional |  | Tender R9; PB-09, PB-10, PB-11; FS F9: Step 7 Retry; NQ-11; BR-F9-04; BR-F9-09; SCR-08 action Try again |
| [`TC-141`](#tc-141) | `TS-023` | No retry is possible while the EA part has not been returned | SCR-06 Pending | Critical | S1 (highest) | Functional |  | Tender R9; PB-09, PB-10, PB-11; FS F9: Step 7 Retry (only when the old transaction is closed and the EA part is returned); BR-F9-09 |
| [`TC-142`](#tc-142) | `TS-024` | A session that ends before the confirm creates no transaction | SCR-05 Review and confirm | High | S2 | Functional |  | Tender R9; PB-09, PB-10, PB-11; FS F9: EX-02; 5.1 AUTH_REQUIRED |
| [`TC-143`](#tc-143) | `TS-024` | A session that ends after the confirm does not stop the payment | SCR-06 Pending | High | S2 | Functional |  | Tender R9; PB-09, PB-10, PB-11; FS F9: EX-02 |
| [`TC-144`](#tc-144) | `TS-024` | A system error on confirm shows a safe message and changes no data | SCR-05 Review and confirm | High | S2 | Non-functional |  | Tender R9; PB-09, PB-10, PB-11; FS F9: 5.1 SYSTEM_ERROR (no data change) |
| [`TC-145`](#tc-145) | `TS-025` | The seed data follows every invoice rule of BR-F9-12 | Database | High | S2 | Integration |  | Tender R9; PB-09, PB-10; FS F9: BR-F9-12; DA-11; 4.2 InvoiceItem |
| [`TC-146`](#tc-146) | `TS-025` | An Issued invoice with Net 0.00 is refused and a Draft with Net 0.00 is accepted | Database | Medium | S3 | Integration |  | Tender R9; PB-09, PB-10; FS F9: BR-F9-12; 4.2 Invoice NetAmount (Net above 0 when not Draft); NQ-16 |
| [`TC-147`](#tc-147) | `TS-025` | A line with Subsidy equal to Gross is refused and Subsidy just below Gross is accepted | Database | Medium | S3 | Integration |  | Tender R9; PB-09, PB-10; FS F9: BR-F9-12; 4.2 InvoiceItem (0 <= Subsidy < Gross) |
| [`TC-148`](#tc-148) | `TS-025` | A student charge cannot be placed on two invoices | Database | High | S2 | Integration |  | Tender R9; PB-09, PB-10; FS F9: BR-F9-12; 4.2 InvoiceItem StudentChargeId (unique) |
| [`TC-149`](#tc-149) | `TS-025` | A line from another school than the invoice is refused | Database | Medium | S3 | Integration |  | Tender R9; PB-09, PB-10; FS F9: BR-F9-12; 4.2 Invoice SchoolId |
| [`TC-150`](#tc-150) | `TS-025` | Negative amounts are refused | Database | Medium | S3 | Integration |  | Tender R9; PB-09, PB-10; FS F9: BR-F9-12; 4.2 Invoice (amounts not negative) |
| [`TC-151`](#tc-151) | `TS-025` | Date fields follow the invoice status | Database | Medium | S3 | Integration |  | Tender R9; PB-09, PB-10; FS F9: 4.2 Invoice (IssuedAt and DueDate required after issue; PaidAt only when Paid; CancelledAt only when Cancelled) |
| [`TC-152`](#tc-152) | `TS-025` | The currency defaults to SGD | Database | Low | S4 (lowest) | Integration |  | Tender R9; PB-09, PB-10; FS F9: DA-10; 4.2 Invoice CurrencyCode |
| [`TC-153`](#tc-153) | `TS-026` | A second open transaction for an invoice is refused by the database | Database | Critical | S1 (highest) | Integration |  | Tender R9; PB-09, PB-10; FS F9: DA-13; BR-F9-09; 4.2 Transaction (unique index on InvoiceId when CompletedAt is empty) |
| [`TC-154`](#tc-154) | `TS-026` | A second Succeeded transaction for an invoice is refused | Database | Critical | S1 (highest) | Integration |  | Tender R9; PB-09, PB-10; FS F9: DA-13; BR-F9-04; 4.2 Transaction (unique index on InvoiceId when Status = Succeeded) |
| [`TC-155`](#tc-155) | `TS-026` | An idempotency key is unique for a Parent and can repeat across Parents | Database | High | S2 | Integration |  | Tender R9; PB-09, PB-10; FS F9: BR-F9-04; 4.2 Transaction IdempotencyKey (unique per InitiatedByUserId and key) |
| [`TC-156`](#tc-156) | `TS-026` | A FundingReference is unique and a split uses two different references | Database | High | S2 | Integration |  | Tender R9; PB-09, PB-10; FS F9: DA-12; 4.2 FundingLeg FundingReference (unique); Glossary Funding leg |
| [`TC-157`](#tc-157) | `TS-026` | Wallet and provider fields depend on the leg method | Database | Medium | S3 | Integration |  | Tender R9; PB-09, PB-10; FS F9: 4.2 FundingLeg WalletId (required for method 1, forbidden for 2), ProviderCode (required for method 2) |
| [`TC-158`](#tc-158) | `TS-026` | Ledger and provider IDs are stored when they must be and are unique | Database | High | S2 | Integration |  | Tender R9; PB-09, PB-10; FS F9: 4.2 FundingLeg (EducationAccountTransactionId, EducationAccountReversalTransactionId, ProviderTransactionId) |
| [`TC-159`](#tc-159) | `TS-026` | Leg amounts add up to the transaction and the transaction equals the invoice Net | Database | Critical | S1 (highest) | Integration |  | Tender R9; PB-09, PB-10; FS F9: BR-F9-13; BR-F9-11; 4.2 Transaction and FundingLeg amounts |
| [`TC-160`](#tc-160) | `TS-026` | An amount other than the invoice Net cannot be requested | API: create payment | Critical | S1 (highest) | API |  | Tender R9; PB-09, PB-10; FS F9: BR-F9-13; DA-07; OOS 2; 4.2 Invoice Status (1 to 5) |
| [`TC-161`](#tc-161) | `TS-026` | Settled above Requested and a leg amount of zero are refused | Database | Medium | S3 | Integration |  | Tender R9; PB-09, PB-10; FS F9: 4.2 Transaction (0 <= Settled <= Requested), FundingLeg (Requested above 0) |
| [`TC-162`](#tc-162) | `TS-026` | CompletedAt is empty while processing and filled when the transaction is final | Database | Medium | S3 | Integration |  | Tender R9; PB-09, PB-10; FS F9: 4.2 Transaction CompletedAt; DA-13 |

---

## Detailed Test Case Specifications


### Test Suite: F9.1 Access and child list

#### `TC-001`: Parent signs in with Singpass and reaches the child list

- **Scenario ID**: `TS-001`
- **Test Suite**: F9.1 Access and child list
- **Page / Target**: `SCR-01 Choose child`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-09; FS F9: AC-01; Step 1; SCR-01
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01
- **Assumption Reference**: N/A
- **Note**: xác nhận

**Preconditions:**
```text
1. The portal is open on the sign in page.
 2. Parent PAR-A exists in the Singpass mock and is linked to STU-101, STU-102 and STU-103.
```

**Test Data:**
```text
Parent: PAR-A
 Linked children: STU-101, STU-102, STU-103
```

**Test Steps:**
1. Start the Singpass sign in.
2. Sign in as PAR-A in the Singpass mock.
3. Look at the screen that opens.

**Expected Result:**
> 1. A session is created for PAR-A.
>  2. SCR-01 opens and lists the children linked to PAR-A: STU-101 Ethan Tan, STU-102 Chloe Tan and STU-103 Marcus Tan.

---

#### `TC-002`: Failed Singpass sign in creates no session

- **Scenario ID**: `TS-001`
- **Test Suite**: F9.1 Access and child list
- **Page / Target**: `SCR-01 Choose child`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-09; FS F9: Step 1 alternative flow; 5.1 AUTH_REQUIRED; SCR-01
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01
- **Assumption Reference**: N/A
- **Note**: ui mock test hiển thị message khác với message của lỗi auth

**Preconditions:**
```text
1. The portal is open on the sign in page.
 2. The Singpass mock is set to fail the sign in.
```

**Test Data:**
```text
Parent: PAR-A
```

**Test Steps:**
1. Start the Singpass sign in.
2. Let the Singpass mock fail the sign in.
3. Try to open the SCR-01 address of the portal directly.

**Expected Result:**
> 1. An error is shown after the failed sign in and no session is created.
>  2. Opening the SCR-01 address shows the message "Your session has expired. Please sign in again." and moves to the Singpass sign in.
>  3. No child data is shown.

---

#### `TC-003`: Cancelled Singpass sign in creates no session

- **Scenario ID**: `TS-001`
- **Test Suite**: F9.1 Access and child list
- **Page / Target**: `SCR-01 Choose child`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-09; FS F9: Step 1 alternative flow; SCR-01
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01
- **Assumption Reference**: N/A
- **Note**: xác nhận

**Preconditions:**
```text
1. The portal is open on the sign in page.
```

**Test Data:**
```text
Parent: PAR-A
```

**Test Steps:**
1. Start the Singpass sign in.
2. Cancel the sign in on the Singpass mock page.
3. Return to the portal.

**Expected Result:**
> 1. No session is created.
>  2. The portal shows an error or the sign in page and no child data.
>  3. The Parent can start the sign in again.

---

#### `TC-004`: Child list shows name, school, level, class and outstanding label

- **Scenario ID**: `TS-002`
- **Test Suite**: F9.1 Access and child list
- **Page / Target**: `SCR-01 Choose child`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-09; FS F9: 4.1 SCR-01 (Student name, School Level Class, Has outstanding invoices); SCR-01; AC-01
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01
- **Assumption Reference**: N/A
- **Note**: không thấy tài liệu liên quan để check khi xem child lít thì show những gì

**Preconditions:**
```text
1. PAR-A is signed in.
 2. Seed data is loaded: STU-101, STU-102, STU-103 each have an Issued invoice.
```

**Test Data:**
```text
Parent: PAR-A
```

**Test Steps:**
1. Open SCR-01.
2. Read the entry of each child.

**Expected Result:**
> 1. Each entry shows the student name, the school (SCH-01 Greenfield Primary School), the level (also called cohort) and the class.
>  2. Each entry shows the label that the child has outstanding invoices.

---

#### `TC-005`: Label shows no outstanding invoices for a child without any

- **Scenario ID**: `TS-002`
- **Test Suite**: F9.1 Access and child list
- **Page / Target**: `SCR-01 Choose child`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-09; FS F9: 4.1 SCR-01 Has outstanding invoices; SCR-01
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01
- **Assumption Reference**: N/A
- **Note**: xác nhận

**Preconditions:**
```text
1. PAR-E is signed in.
 2. STU-109 has only Paid and Cancelled invoices. STU-104 has one Issued invoice.
```

**Test Data:**
```text
Parent: PAR-E
 Children: STU-104, STU-105, STU-106, STU-108, STU-109
```

**Test Steps:**
1. Open SCR-01.
2. Compare the labels of STU-109 and STU-104.

**Expected Result:**
> 1. STU-109 Zoe Wong shows the label that there are no outstanding invoices.
>  2. STU-104 Noah Wong shows the label that there are outstanding invoices.

---

#### `TC-006`: Child list contains only the children linked to the Parent

- **Scenario ID**: `TS-002`
- **Test Suite**: F9.1 Access and child list
- **Page / Target**: `SCR-01 Choose child`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-09; FS F9: AC-01; BR-F9-01; DA-04; SCR-01
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01
- **Assumption Reference**: N/A
- **Note**: xác nhận

**Preconditions:**
```text
1. PAR-A is signed in.
 2. Students STU-104, STU-105, STU-106, STU-108, STU-109 and STU-201 exist but are not linked to PAR-A.
```

**Test Data:**
```text
Parent: PAR-A
```

**Test Steps:**
1. Open SCR-01.
2. Count the children and read their names.

**Expected Result:**
> 1. Exactly three children are listed: STU-101, STU-102 and STU-103.
>  2. No other student appears and no invoice of another family is shown.

---

#### `TC-007`: Parent without any linked child sees the empty state

- **Scenario ID**: `TS-002`
- **Test Suite**: F9.1 Access and child list
- **Page / Target**: `SCR-01 Choose child`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-09; FS F9: Step 1 alternative flow; SCR-01 Empty
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01
- **Assumption Reference**: N/A
- **Note**: xác nhận

**Preconditions:**
```text
1. PAR-C is signed in. PAR-C has no linked student.
```

**Test Data:**
```text
Parent: PAR-C
```

**Test Steps:**
1. Open SCR-01.

**Expected Result:**
> 1. SCR-01 shows the empty state: no children are linked.
>  2. The screen tells the Parent to contact the school.
>  3. No student and no invoice is shown.

---

#### `TC-008`: Parent with one child reaches that child

- **Scenario ID**: `TS-002`
- **Test Suite**: F9.1 Access and child list
- **Page / Target**: `SCR-01 Choose child`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-09; FS F9: Step 1 alternative flow; SCR-01; SCR-02
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01
- **Assumption Reference**: N/A
- **Note**: The FS says the system may go straight to SCR-02. Both outcomes pass.
 xác nhận. UI mock có kịch bản một con: Home chỉ liệt kê con đó và All fees vào thẳng Fees, khớp trường hợp thứ hai của Expected.

**Preconditions:**
```text
1. PAR-B is signed in. PAR-B has one linked child, STU-201 Daniel Lim.
```

**Test Data:**
```text
Parent: PAR-B
 Student: STU-201
```

**Test Steps:**
1. Sign in as PAR-B.
2. Look at the screen that opens.

**Expected Result:**
> 1. Either SCR-01 lists only STU-201, or the system goes straight to SCR-02 of STU-201.
>  2. No other student is shown.

---

#### `TC-009`: Second guardian linked to the same child sees the same child and invoices

- **Scenario ID**: `TS-002`
- **Test Suite**: F9.1 Access and child list
- **Page / Target**: `SCR-02 Outstanding fees`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-09; FS F9: DA-04; AC-01; BR-F9-01; SCR-02
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01
- **Assumption Reference**: N/A
- **Note**: xác nhận theo FS 09 (DA-04, AC-01, BR-F9-01). UI mock có kịch bản Returning user dùng chung con với guardian khác; chưa đối chiếu danh sách invoice của hai bên.

**Preconditions:**
```text
1. PAR-A and PAR-D are both linked to STU-101.
 2. Seed data is loaded.
```

**Test Data:**
```text
Parents: PAR-A and PAR-D
 Student: STU-101
```

**Test Steps:**
1. Sign in as PAR-A, open STU-101 and note the invoice list.
2. Sign out. Sign in as PAR-D, open STU-101 and note the invoice list.

**Expected Result:**
> 1. PAR-D sees STU-101 on SCR-01.
>  2. Both Parents see the same invoices with the same amounts and statuses.
>  3. PAR-D can select an Issued invoice and open SCR-04.

---

#### `TC-010`: System error while loading the child list shows a safe message

- **Scenario ID**: `TS-002`
- **Test Suite**: F9.1 Access and child list
- **Page / Target**: `SCR-01 Choose child`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Non-functional`
- **Traceability**: Tender R9; PB-09; FS F9: 5.1 SYSTEM_ERROR; SCR-01 Error
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-05
- **Assumption Reference**: N/A
- **Note**: Needs a fault switch from Dev (ENV-R9-05).
 xác nhận. UI mock không có công tắc lỗi nên chưa kiểm được trên UI.

**Preconditions:**
```text
1. PAR-A has a valid session.
 2. A Function 9 service is set to return an error for the child list.
```

**Test Data:**
```text
Parent: PAR-A
```

**Test Steps:**
1. Open SCR-01 while the service returns an error.

**Expected Result:**
> 1. SCR-01 shows the Error state with the message "Something went wrong. Please try again later."
>  2. The Parent can try again.
>  3. No data is changed and no technical detail is shown.

---

#### `TC-011`: Changing the student ID in the address is refused

- **Scenario ID**: `TS-003`
- **Test Suite**: F9.1 Access and child list
- **Page / Target**: `SCR-02 Outstanding fees`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Security`
- **Traceability**: Tender R9; PB-09; FS F9: EX-01; AC-12; BR-F9-01; 5.1 FORBIDDEN_CHILD; SCR-02
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-05
- **Assumption Reference**: N/A
- **Note**: xác nhận theo FS 09 (EX-01, AC-12, 5.1 FORBIDDEN_CHILD). UI mock chỉ có một địa chỉ gốc, không có mã student trên URL (đường dẫn sâu trả trang 404 của Vercel), nên không đổi ID được trên mock.

**Preconditions:**
```text
1. PAR-A is signed in and has opened SCR-02 of STU-101.
 2. STU-201 exists and is not linked to PAR-A.
```

**Test Data:**
```text
Parent: PAR-A
 Own child: STU-101
 Other family child: STU-201 (invoice INV-2101)
```

**Test Steps:**
1. Copy the address of SCR-02.
2. Replace the student ID of STU-101 with the ID of STU-201.
3. Open the changed address.

**Expected Result:**
> 1. The server answers 403.
>  2. The screen shows "You do not have access to this student's records." and returns to SCR-01.
>  3. No invoice, amount or EA balance of STU-201 is shown.
>  4. A security log entry is written.

---

#### `TC-012`: API call for the invoices of an unlinked student is refused

- **Scenario ID**: `TS-003`
- **Test Suite**: F9.1 Access and child list
- **Page / Target**: `API: list invoices`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Security`
- **Traceability**: Tender R9; PB-09; FS F9: EX-01; AC-12; BR-F9-01
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-05, ENV-R9-06
- **Assumption Reference**: N/A
- **Note**: xác nhận

**Preconditions:**
```text
1. PAR-A has a valid session.
```

**Test Data:**
```text
Parent: PAR-A
 Student: STU-201
```

**Test Steps:**
1. Send the list invoices request for STU-201 with the session of PAR-A.
2. Send the same request for STU-101.

**Expected Result:**
> 1. The request for STU-201 returns 403 and no invoice data. A security log entry is written.
>  2. The request for STU-101 returns the invoices of STU-101.

---

#### `TC-013`: API call to read an invoice of another family is refused

- **Scenario ID**: `TS-003`
- **Test Suite**: F9.1 Access and child list
- **Page / Target**: `API: invoice detail`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Security`
- **Traceability**: Tender R9; PB-09; FS F9: BR-F9-01; EX-01; 5.1 FORBIDDEN_CHILD
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-05, ENV-R9-06
- **Assumption Reference**: ASM-R9-23: An invoice, transaction or receipt of a student who is not linked to the Parent is rejected like EX-01: 403, the FORBIDDEN_CHILD message in the screen, no data returned and a security log entry.
- **Note**: xác nhận

**Preconditions:**
```text
1. PAR-A has a valid session.
 2. Invoice INV-2101 belongs to STU-201.
```

**Test Data:**
```text
Parent: PAR-A
 Invoice: INV-2101 (STU-201)
```

**Test Steps:**
1. Send the invoice detail request for INV-2101 with the session of PAR-A.

**Expected Result:**
> 1. The request is refused with 403 and returns no invoice data.
>  2. The screen message is "You do not have access to this student's records."
>  3. A security log entry is written.

---

#### `TC-014`: API call to pay an invoice of another family is refused and nothing is debited

- **Scenario ID**: `TS-003`
- **Test Suite**: F9.1 Access and child list
- **Page / Target**: `API: create payment`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Security`
- **Traceability**: Tender R9; PB-09; FS F9: BR-F9-01; EX-01; AC-12; 5.1 FORBIDDEN_CHILD
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-05, ENV-R9-06
- **Assumption Reference**: ASM-R9-23: An invoice, transaction or receipt of a student who is not linked to the Parent is rejected like EX-01: 403, the FORBIDDEN_CHILD message in the screen, no data returned and a security log entry.
- **Note**: xác nhận

**Preconditions:**
```text
1. PAR-A has a valid session.
 2. Invoice INV-2101 (90.00 SGD) is Issued and belongs to STU-201. STU-201 EA balance is 500.00.
```

**Test Data:**
```text
Parent: PAR-A
 Invoice: INV-2101
 Method: EA
 Idempotency key: SEC-KEY-001
```

**Test Steps:**
1. Send the create payment request for INV-2101 with method EA, using the session of PAR-A.
2. Look at the transactions of INV-2101 and the EA balance of STU-201.

**Expected Result:**
> 1. The request is refused with 403.
>  2. No transaction exists for INV-2101. Invoice INV-2101 is still Issued.
>  3. The EA balance of STU-201 is still 500.00.
>  4. A security log entry is written.

---

#### `TC-015`: API call for the status or receipt of another family's payment is refused

- **Scenario ID**: `TS-003`
- **Test Suite**: F9.1 Access and child list
- **Page / Target**: `API: transaction status and receipt`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Security`
- **Traceability**: Tender R9; PB-09; FS F9: BR-F9-01; AC-13; AC-12
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-05, ENV-R9-06
- **Assumption Reference**: ASM-R9-23: An invoice, transaction or receipt of a student who is not linked to the Parent is rejected like EX-01: 403, the FORBIDDEN_CHILD message in the screen, no data returned and a security log entry.
- **Note**: xác nhận

**Preconditions:**
```text
1. PAR-B has paid a fresh invoice of STU-201 and has transaction TXN-B1 with a receipt.
 2. PAR-A has a valid session.
```

**Test Data:**
```text
Parent: PAR-A
 Transaction: TXN-B1 (PAR-B)
```

**Test Steps:**
1. Send the transaction status request for TXN-B1 with the session of PAR-A.
2. Send the receipt download request for TXN-B1 with the session of PAR-A.

**Expected Result:**
> 1. Both requests are refused with 403 and return no data.
>  2. No receipt file is returned.
>  3. A security log entry is written.

---

#### `TC-016`: A guardian cannot open a child who is linked only to another Parent

- **Scenario ID**: `TS-003`
- **Test Suite**: F9.1 Access and child list
- **Page / Target**: `SCR-02 Outstanding fees`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Security`
- **Traceability**: Tender R9; PB-09; FS F9: BR-F9-01; DA-04; EX-01
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01
- **Assumption Reference**: N/A
- **Note**: xác nhận theo FS 09 (BR-F9-01, DA-04, EX-01). UI mock không có mã student trên URL nên chưa kiểm được trên UI.

**Preconditions:**
```text
1. PAR-D is signed in. PAR-D is linked only to STU-101.
 2. STU-102 is linked to PAR-A only.
```

**Test Data:**
```text
Parent: PAR-D
 Student: STU-102
```

**Test Steps:**
1. Open SCR-02 of STU-101.
2. Change the student ID in the address to the ID of STU-102.

**Expected Result:**
> 1. STU-101 opens normally.
>  2. The changed address returns 403 and the message "You do not have access to this student's records."
>  3. No data of STU-102 is shown.

---

#### `TC-017`: Request without a session is sent to the sign in

- **Scenario ID**: `TS-003`
- **Test Suite**: F9.1 Access and child list
- **Page / Target**: `API: list invoices`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Security`
- **Traceability**: Tender R9; PB-09; FS F9: 5.1 AUTH_REQUIRED; BR-F9-01
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-06
- **Assumption Reference**: N/A
- **Note**: xác nhận theo FS 09 (5.1 AUTH_REQUIRED). UI mock không có địa chỉ riêng của màn Fees để mở khi chưa đăng nhập; câu hiển thị của mock xem ghi chú ở TC-002.

**Preconditions:**
```text
1. No Parent is signed in.
```

**Test Data:**
```text
Student: STU-101
```

**Test Steps:**
1. Send the list invoices request for STU-101 without a session.
2. Open the address of SCR-02 in a new browser with no session.

**Expected Result:**
> 1. Both attempts return no data.
>  2. The portal shows "Your session has expired. Please sign in again." and moves to the Singpass sign in.

---


### Test Suite: F9.2 Outstanding invoices and EA balance

#### `TC-018`: Open invoices of the chosen child are listed with number, due date, status and amount

- **Scenario ID**: `TS-004`
- **Test Suite**: F9.2 Outstanding invoices and EA balance
- **Page / Target**: `SCR-02 Outstanding fees`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-09; FS F9: AC-01; Step 2; 4.1 SCR-02; SCR-02
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01
- **Assumption Reference**: ASM-R9-03: SCR-02 lists invoices in Issued (payable) and PaymentPending (shown as Pending, not selectable). Paid, Cancelled and Draft are not listed. The total owed is the sum of Net of the listed invoices. SCR-03 appears only when the child has no listed invoice.
- **Note**: xác nhận trace (AC-01, Step 2, 4.1 SCR-02). UI mock: mỗi invoice có số, hạn nộp, số tiền SGD và có tổng còn nợ ở đầu trang. Trạng thái hiện bằng nhãn theo hạn nộp (OVERDUE, DUE SOON, NOT DUE YET) thay vì Issued. FS 4.1 để cách hiển thị quá hạn là TBC (OQ-04) nhưng DA-05 liệt kê Issued, Pending, Paid, Cancelled, cần BA chốt nhãn.

**Preconditions:**
```text
1. PAR-A is signed in.
 2. Base seed data is loaded for STU-101: INV-1001 (Issued, 180.00), INV-1002 (Issued, 50.00), INV-1003 (Issued, 130.00), INV-1006 (PaymentPending, 60.00).
```

**Test Data:**
```text
Parent: PAR-A
 Student: STU-101
```

**Test Steps:**
1. On SCR-01 choose STU-101 Ethan Tan.
2. Read the invoice list.

**Expected Result:**
> 1. The list shows INV-1001, INV-1002, INV-1003 and INV-1006.
>  2. Each invoice shows its number, due date, status and the amount to pay in SGD.
>  3. INV-1001 shows 180.00, INV-1002 50.00, INV-1003 130.00 and INV-1006 60.00.
>  4. The total owed is 420.00.
>  5. No invoice of STU-102 or STU-103 is shown.

---

#### `TC-019`: An invoice opens to its lines grouped by fee type with fee components and GST

- **Scenario ID**: `TS-004`
- **Test Suite**: F9.2 Outstanding invoices and EA balance
- **Page / Target**: `SCR-02 Outstanding fees`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-09; FS F9: Step 2; 4.1 SCR-02 (Fee type, Line description, Fee components); DA-05; SCR-02
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01
- **Assumption Reference**: N/A
- **Note**: xác nhận. UI mock mở invoice ra từng dòng có fee type, fee component, GST 9% (ví dụ 22.00 cộng GST 1.98 bằng 23.98), Gross, Subsidy 0.00 và Net. Mock hiện nhãn fee type trên từng dòng, không có tiêu đề gom nhóm theo fee type.

**Preconditions:**
```text
1. PAR-A is signed in and has opened SCR-02 of STU-101.
```

**Test Data:**
```text
Invoice: INV-1001
 L1 School fee: Tuition 55.05 + GST 4.95 = 60.00
 L2 Miscellaneous fee: Stationery 36.70 + GST 3.30 = 40.00
 L3 Extracurricular: Club fee 27.52 + GST 2.48 = 30.00
 L4 Ad hoc: Replacement fee 45.87 + GST 4.13 = 50.00
```

**Test Steps:**
1. Expand INV-1001.
2. Read each line and its components.

**Expected Result:**
> 1. The four lines are shown grouped by fee type: school fee, miscellaneous, extracurricular and ad hoc.
>  2. Each line shows its description, its fee components including GST, its subsidy and its amount.
>  3. For each line the components add up to the line Gross: 60.00, 40.00, 30.00 and 50.00.

---

#### `TC-020`: Invoice totals show Gross, Subsidy 0.00 and Net equal to Gross

- **Scenario ID**: `TS-004`
- **Test Suite**: F9.2 Outstanding invoices and EA balance
- **Page / Target**: `SCR-02 Outstanding fees`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-09; FS F9: BR-F9-08; DA-09; NQ-04; 4.1 SCR-02 (Gross, Subsidy, Net)
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01
- **Assumption Reference**: N/A
- **Note**: Inference: the FS does not say the invoice amount is the sum of its lines. DA-05 describes an invoice made of lines.
 xác nhận trên UI mock: từng dòng có Subsidy (FAS) 0.00 và Net bằng Gross; số phải trả của invoice bằng tổng các dòng (38.00 cộng 23.98 bằng 61.98).

**Preconditions:**
```text
1. PAR-A is signed in and has expanded INV-1001 of STU-101.
```

**Test Data:**
```text
Invoice: INV-1001
 Gross 180.00, Subsidy 0.00, Net 180.00
```

**Test Steps:**
1. Read the Gross, Subsidy and Net amounts of each line.
2. Read the amount to pay of the invoice.
3. Add the lines by hand.

**Expected Result:**
> 1. Every line shows Subsidy 0.00 and Net equal to Gross.
>  2. The invoice shows Subsidy 0.00 and an amount to pay of 180.00, equal to the sum of the line amounts 60.00 + 40.00 + 30.00 + 50.00.
>  3. The Parent sees the Gross amount, not a reduced amount.

---

#### `TC-021`: Amounts are shown in SGD with two decimals

- **Scenario ID**: `TS-004`
- **Test Suite**: F9.2 Outstanding invoices and EA balance
- **Page / Target**: `SCR-02 Outstanding fees`
- **Severity / Priority**: `S4 (lowest)` / `Low`
- **Execution Status**: `Not Run` | **Test Type**: `UI`
- **Traceability**: Tender R9; PB-09; FS F9: DA-10; 4.1 SCR-02 (Decimal(18,2), SGD)
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01
- **Assumption Reference**: N/A
- **Note**: xác nhận. UI mock hiển thị SGD với hai số thập phân cho số phải trả, số dư EA, Gross, Subsidy và Net.

**Preconditions:**
```text
1. PAR-A is signed in and has opened SCR-02 of STU-101.
```

**Test Data:**
```text
Invoices: INV-1001 (180.00), INV-1002 (50.00), INV-1003 (130.00)
```

**Test Steps:**
1. Read the currency and the format of every amount on the screen, including the EA balance.

**Expected Result:**
> 1. Every amount is in SGD and has two decimals, for example 50.00 and not 50.
>  2. The EA balance is shown as 200.00.

---

#### `TC-022`: Invoice due date is the earliest due date of its lines

- **Scenario ID**: `TS-004`
- **Test Suite**: F9.2 Outstanding invoices and EA balance
- **Page / Target**: `SCR-02 Outstanding fees`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-09; FS F9: 4.1 SCR-02 Due date
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01
- **Assumption Reference**: N/A
- **Note**: xác nhận trace (4.1 SCR-02 Due date). UI mock chỉ hiện một hạn nộp cho cả invoice, không hiện hạn nộp từng dòng, nên chưa kiểm được việc đó là hạn sớm nhất của các dòng.

**Preconditions:**
```text
1. PAR-A is signed in and has opened SCR-02 of STU-101.
 2. INV-1003 has two lines: the school fee line is due 15 Dec 2026 and the miscellaneous line is due 1 Dec 2026.
```

**Test Data:**
```text
Invoice: INV-1003
```

**Test Steps:**
1. Read the due date of INV-1003.

**Expected Result:**
> 1. INV-1003 shows the due date 1 Dec 2026, the earliest due date of its lines.

---

#### `TC-023`: Switching to another child changes the invoice list

- **Scenario ID**: `TS-004`
- **Test Suite**: F9.2 Outstanding invoices and EA balance
- **Page / Target**: `SCR-02 Outstanding fees`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-09; FS F9: AC-01; SCR-02 action change child
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01
- **Assumption Reference**: N/A
- **Note**: xác nhận. UI mock đổi con bằng thẻ tên con trên trang Fees, danh sách invoice và số dư EA đổi theo.

**Preconditions:**
```text
1. PAR-A is signed in and has opened SCR-02 of STU-101.
```

**Test Data:**
```text
Parent: PAR-A
 Students: STU-101, STU-102
```

**Test Steps:**
1. Use the change child action and choose STU-102 Chloe Tan.
2. Read the invoice list.
3. Go back and choose STU-101 again.

**Expected Result:**
> 1. For STU-102 only INV-2001 (75.00) is shown and no invoice of STU-101.
>  2. For STU-101 the invoices of STU-101 are shown again.

---

#### `TC-024`: Paid, Cancelled and Draft invoices are not in the list

- **Scenario ID**: `TS-004`
- **Test Suite**: F9.2 Outstanding invoices and EA balance
- **Page / Target**: `SCR-02 Outstanding fees`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-09; FS F9: AC-01; 4.1 SCR-02 Invoice status note (Draft does not show); Step 3
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01
- **Assumption Reference**: ASM-R9-03: SCR-02 lists invoices in Issued (payable) and PaymentPending (shown as Pending, not selectable). Paid, Cancelled and Draft are not listed. The total owed is the sum of Net of the listed invoices. SCR-03 appears only when the child has no listed invoice.
- **Note**: xác nhận trace (AC-01, 4.1 SCR-02 Invoice status). UI mock: invoice Paid không nằm trong OUTSTANDING INVOICES nhưng hiện ở mục riêng RECENT PAYMENTS. Draft và Cancelled chưa kiểm được trên mock.

**Preconditions:**
```text
1. PAR-A is signed in.
 2. STU-101 also has INV-1004 (Paid), INV-1005 (Cancelled) and INV-1007 (Draft).
```

**Test Data:**
```text
Student: STU-101
 Invoices not expected: INV-1004, INV-1005, INV-1007
```

**Test Steps:**
1. Open SCR-02 of STU-101.
2. Look for INV-1004, INV-1005 and INV-1007.

**Expected Result:**
> 1. INV-1004, INV-1005 and INV-1007 are not in the list.
>  2. The Draft invoice INV-1007 is never shown to the Parent.

---

#### `TC-025`: An invoice waiting for payment is shown as Pending and cannot be selected

- **Scenario ID**: `TS-004`
- **Test Suite**: F9.2 Outstanding invoices and EA balance
- **Page / Target**: `SCR-02 Outstanding fees`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-09; FS F9: AC-11; DA-05; 4.1 SCR-02 Selected invoice (only Issued, no open transaction); BR-F9-09
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01
- **Assumption Reference**: ASM-R9-03: SCR-02 lists invoices in Issued (payable) and PaymentPending (shown as Pending, not selectable). Paid, Cancelled and Draft are not listed. The total owed is the sum of Net of the listed invoices. SCR-03 appears only when the child has no listed invoice.
- **Note**: xác nhận. UI mock sau Close Browser: invoice hiện nhãn AWAITING PAYMENT, nút Pay now đổi thành View status mở màn Payment In Progress, không chọn thanh toán mới được. Nhãn là AWAITING PAYMENT, không phải Pending như Expected.

**Preconditions:**
```text
1. PAR-A is signed in.
 2. INV-1006 of STU-101 is PaymentPending with an open transaction.
```

**Test Data:**
```text
Invoice: INV-1006 (60.00)
```

**Test Steps:**
1. Open SCR-02 of STU-101.
2. Look at INV-1006.
3. Try to select INV-1006.

**Expected Result:**
> 1. INV-1006 shows the status Pending.
>  2. INV-1006 cannot be selected for payment.
>  3. SCR-04 does not open for INV-1006.

---

#### `TC-026`: An invoice past its due date is listed and can be paid

- **Scenario ID**: `TS-004`
- **Test Suite**: F9.2 Outstanding invoices and EA balance
- **Page / Target**: `SCR-02 Outstanding fees`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-09; FS F9: 4.1 SCR-02 Due date; NQ-03; OQ-04
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01
- **Assumption Reference**: ASM-R9-04: An invoice past its due date is listed like any other, keeps status Issued, shows its due date and can be paid. No overdue label, penalty or block is required.
- **Note**: xác nhận trace (4.1 SCR-02 Due date, NQ-03, OQ-04). UI mock: invoice quá hạn có nhãn OVERDUE, vẫn có Pay now và trả được (đã trả INV-2026-1001 quá hạn). ASM-R9-04 nói không cần nhãn quá hạn, trong khi FS 4.1 để cách hiển thị là TBC, nên nhãn của mock cần BA xác nhận.

**Preconditions:**
```text
1. PAR-A is signed in.
 2. The system date is after 1 Oct 2026.
 3. INV-1002 of STU-101 is Issued with the due date 1 Oct 2026.
```

**Test Data:**
```text
Invoice: INV-1002 (50.00, due 1 Oct 2026)
```

**Test Steps:**
1. Open SCR-02 of STU-101.
2. Read INV-1002.
3. Select INV-1002.

**Expected Result:**
> 1. INV-1002 is listed with its due date and the status Issued.
>  2. SCR-04 opens for INV-1002.

---

#### `TC-027`: Demo data is labelled as sample data

- **Scenario ID**: `TS-004`
- **Test Suite**: F9.2 Outstanding invoices and EA balance
- **Page / Target**: `SCR-02 Outstanding fees`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `UI`
- **Traceability**: Tender R9; PB-09; FS F9: DA-11; OQ-04; OQ-08
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01
- **Assumption Reference**: ASM-R9-26: A label that says the data is sample data is visible on SCR-02 where the invoices and the EA balance are shown. A portal wide banner also passes.
- **Note**: xác nhận trace (DA-11, OQ-04, OQ-08). UI mock không có nhãn dữ liệu mẫu trên trang Fees; chỉ có nút Reset mock data và cửa sổ Singpass ghi Simulated Environment. Chưa đạt Expected 1 và 2 trên mock.

**Preconditions:**
```text
1. PAR-A is signed in and has opened SCR-02 of STU-101.
```

**Test Data:**
```text
Student: STU-101
```

**Test Steps:**
1. Look for a label that says the data is sample data.

**Expected Result:**
> 1. A label shows clearly that the invoices and the EA balance are sample data.
>  2. The page does not present the data as real billing.

---

#### `TC-028`: A child with an Active EA shows balance and status

- **Scenario ID**: `TS-005`
- **Test Suite**: F9.2 Outstanding invoices and EA balance
- **Page / Target**: `SCR-02 Outstanding fees`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-09; FS F9: Step 2; 4.1 SCR-02 (EA balance, EA status); SCR-02
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01
- **Assumption Reference**: N/A
- **Note**: xác nhận. UI mock hiện EDUCATION ACCOUNT BALANCE và Status: Active.

**Preconditions:**
```text
1. PAR-A is signed in.
```

**Test Data:**
```text
Student: STU-101, EA Active, balance 200.00
```

**Test Steps:**
1. Open SCR-02 of STU-101.
2. Read the EA widget.

**Expected Result:**
> 1. The widget shows the EA balance 200.00 SGD and the EA status Active.

---

#### `TC-029`: A child without an EA shows no balance and a note

- **Scenario ID**: `TS-005`
- **Test Suite**: F9.2 Outstanding invoices and EA balance
- **Page / Target**: `SCR-02 Outstanding fees`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-09; FS F9: Step 2 alternative flow; DA-03; 4.1 SCR-02 EA balance
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01
- **Assumption Reference**: N/A
- **Note**: xác nhận trace (Step 2 alternative flow, DA-03). UI mock với student không phải công dân: không hiện số dư, ghi 'Education Accounts are for Singapore Citizens' và Status: Not eligible. Câu chữ khác FS ('không có Education Account') nhưng cùng ý.

**Preconditions:**
```text
1. PAR-A is signed in.
 2. STU-102 Chloe Tan is a Permanent Resident and has no EA.
```

**Test Data:**
```text
Student: STU-102
```

**Test Steps:**
1. Open SCR-02 of STU-102.
2. Look for the EA widget.

**Expected Result:**
> 1. No EA balance is shown.
>  2. A note says that the student has no Education Account.

---

#### `TC-030`: A child with a Closed EA shows the status Closed

- **Scenario ID**: `TS-005`
- **Test Suite**: F9.2 Outstanding invoices and EA balance
- **Page / Target**: `SCR-02 Outstanding fees`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-09; FS F9: 4.1 SCR-02 EA status (only Active can pay); DA-06
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01
- **Assumption Reference**: N/A
- **Note**: xác nhận trace (4.1 SCR-02 EA status, DA-06). UI mock hiện Status: Closed và 'Closed on' kèm ngày. Student 16 tuổi trở lên trên mock chỉ xem, không có Pay now, nên Expected 2 đúng nhưng không đi tiếp để trả online được; FS 09 không nêu quy tắc chỉ xem cho 16 tuổi trở lên.

**Preconditions:**
```text
1. PAR-E is signed in.
 2. STU-104 has an EA with the status Closed and balance 0.00.
```

**Test Data:**
```text
Student: STU-104
```

**Test Steps:**
1. Open SCR-02 of STU-104.
2. Read the EA widget.

**Expected Result:**
> 1. The EA status is shown as Closed.
>  2. The widget does not offer the EA as a way to pay.

---

#### `TC-031`: A zero EA balance is shown as 0.00

- **Scenario ID**: `TS-005`
- **Test Suite**: F9.2 Outstanding invoices and EA balance
- **Page / Target**: `SCR-02 Outstanding fees`
- **Severity / Priority**: `S4 (lowest)` / `Low`
- **Execution Status**: `Not Run` | **Test Type**: `UI`
- **Traceability**: Tender R9; PB-09; FS F9: 4.1 SCR-02 EA balance
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01
- **Assumption Reference**: N/A
- **Note**: xác nhận. UI mock hiện SGD 0.00 và Status: Active sau khi EA đã dùng hết.

**Preconditions:**
```text
1. PAR-E is signed in.
 2. STU-105 has an Active EA with balance 0.00.
```

**Test Data:**
```text
Student: STU-105
```

**Test Steps:**
1. Open SCR-02 of STU-105.
2. Read the EA widget.

**Expected Result:**
> 1. The balance is shown as 0.00 SGD and the status as Active.

---

#### `TC-032`: A child with no Issued invoice shows the empty state

- **Scenario ID**: `TS-006`
- **Test Suite**: F9.2 Outstanding invoices and EA balance
- **Page / Target**: `SCR-03 No outstanding fees`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-09; FS F9: AC-02; Step 3; SCR-03
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01
- **Assumption Reference**: ASM-R9-03: SCR-02 lists invoices in Issued (payable) and PaymentPending (shown as Pending, not selectable). Paid, Cancelled and Draft are not listed. The total owed is the sum of Net of the listed invoices. SCR-03 appears only when the child has no listed invoice.
- **Note**: xác nhận. UI mock (con không có phí): 'No outstanding fees', nút Back to Home, không có lựa chọn thanh toán. Link quay về là Home (danh sách con).

**Preconditions:**
```text
1. PAR-E is signed in.
 2. STU-109 has only INV-9001 (Paid) and INV-9002 (Cancelled).
```

**Test Data:**
```text
Student: STU-109
```

**Test Steps:**
1. On SCR-01 choose STU-109 Zoe Wong.

**Expected Result:**
> 1. SCR-03 opens with a message that there are no outstanding fees.
>  2. A link back to SCR-01 is shown.
>  3. No payment option is shown.

---

#### `TC-033`: The empty state links back to the child list and another child can be chosen

- **Scenario ID**: `TS-006`
- **Test Suite**: F9.2 Outstanding invoices and EA balance
- **Page / Target**: `SCR-03 No outstanding fees`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-09; FS F9: Step 3; SCR-03 action back to SCR-01
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01
- **Assumption Reference**: N/A
- **Note**: xác nhận trace (Step 3, SCR-03). UI mock: Back to Home mở lại danh sách con; có thể đổi con bằng thẻ tên con trên trang Fees.

**Preconditions:**
```text
1. PAR-E is signed in and is on SCR-03 of STU-109.
```

**Test Data:**
```text
Students: STU-109, STU-104
```

**Test Steps:**
1. Use the link back on SCR-03.
2. Choose STU-104 Noah Wong.

**Expected Result:**
> 1. SCR-01 opens with the children of PAR-E.
>  2. SCR-02 of STU-104 opens with its invoice.

---

#### `TC-034`: A child whose only open invoice is waiting for payment is not shown the empty state

- **Scenario ID**: `TS-006`
- **Test Suite**: F9.2 Outstanding invoices and EA balance
- **Page / Target**: `SCR-02 Outstanding fees`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-09; FS F9: AC-11; AC-02; Step 3; SCR-02; SCR-03
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-05
- **Assumption Reference**: ASM-R9-03: SCR-02 lists invoices in Issued (payable) and PaymentPending (shown as Pending, not selectable). Paid, Cancelled and Draft are not listed. The total owed is the sum of Net of the listed invoices. SCR-03 appears only when the child has no listed invoice.
- **Note**: Step 3 says the empty state applies when there is no Issued invoice. AC-11 says the Parent must see the waiting state. The case follows AC-11.
 xác nhận trên UI mock: khi invoice duy nhất đang chờ, trang Fees vẫn hiện invoice nhãn AWAITING PAYMENT và tổng 54.00, không hiện trạng thái rỗng.

**Preconditions:**
```text
1. PAR-E is signed in.
 2. The only open invoice of STU-105, INV-5001, is set to PaymentPending with an open transaction.
```

**Test Data:**
```text
Student: STU-105
 Invoice: INV-5001 (PaymentPending)
```

**Test Steps:**
1. On SCR-01 choose STU-105 Ava Wong.

**Expected Result:**
> 1. SCR-02 opens and shows INV-5001 with the status Pending.
>  2. SCR-03 is not shown.

---


### Test Suite: F9.3 Payment method and eligibility

#### `TC-035`: Selecting an Issued invoice opens the payment method screen with its summary

- **Scenario ID**: `TS-007`
- **Test Suite**: F9.3 Payment method and eligibility
- **Page / Target**: `SCR-04 Choose payment method`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-10, PB-11; FS F9: Step 4; SCR-04; DA-07
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01
- **Assumption Reference**: N/A
- **Note**: Step 4 names two options. Appendix C and the field table of SCR-04 list three (THREEOPT, resolved).
 xác nhận trên UI mock: màn Step 1 of 2 hiện con, số invoice, tổng 50.00, EA 20.00 Available, Online Payment và Split Payment. Mock có ba lựa chọn khớp Appendix C.

**Preconditions:**
```text
1. PAR-A is signed in and has opened SCR-02 of STU-103.
 2. INV-3001 (50.00) is Issued.
```

**Test Data:**
```text
Student: STU-103 Marcus Tan, Singapore Citizen, EA Active, balance 20.00 SGD
 Invoice: INV-3001 (50.00)
```

**Test Steps:**
1. Select INV-3001.

**Expected Result:**
> 1. SCR-04 opens.
>  2. It shows a summary of the invoice: the child, the invoice number and the amount to pay 50.00 SGD.
>  3. It shows the options EA (with the balance 20.00), online payment and split (EA plus online).

---

#### `TC-036`: Only one whole invoice can be selected and lines cannot be paid separately

- **Scenario ID**: `TS-007`
- **Test Suite**: F9.3 Payment method and eligibility
- **Page / Target**: `SCR-02 Outstanding fees`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-10, PB-11; FS F9: DA-05; DA-07; BR-F9-13; OOS 1 and 2; NQ-09
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01
- **Assumption Reference**: N/A
- **Note**: xác nhận. UI mock mở thanh toán theo cả invoice (Pay now), không có chọn nhiều invoice và không có trả từng dòng.

**Preconditions:**
```text
1. PAR-A is signed in and has opened SCR-02 of STU-101.
 2. INV-1001 and INV-1003 are Issued.
```

**Test Data:**
```text
Invoices: INV-1001 (four lines), INV-1003 (two lines)
```

**Test Steps:**
1. Look for a way to select two invoices at once.
2. Look for a way to pay one line of INV-1001.
3. Select INV-1001.

**Expected Result:**
> 1. No control selects two invoices in one payment.
>  2. No control pays a single line or a part of an invoice.
>  3. SCR-04 opens for the whole INV-1001 with the amount 180.00.

---

#### `TC-037`: Back from the payment method screen returns to the invoice list and creates nothing

- **Scenario ID**: `TS-007`
- **Test Suite**: F9.3 Payment method and eligibility
- **Page / Target**: `SCR-04 Choose payment method`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-10, PB-11; FS F9: Appendix C SCR-04 actions; BR-F9-10
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-05
- **Assumption Reference**: ASM-R9-11: Back on SCR-04 returns to SCR-02. Cancel on SCR-05 returns to SCR-04. Neither action creates a transaction or changes an invoice.
- **Note**: xác nhận. UI mock: nút Back ở bước chọn phương thức quay về danh sách Fees, số dư EA không đổi.

**Preconditions:**
```text
1. PAR-A is signed in and is on SCR-04 for INV-3001 of STU-103.
```

**Test Data:**
```text
Student: STU-103 Marcus Tan, Singapore Citizen, EA Active, balance 20.00 SGD
 Invoice: INV-3001
```

**Test Steps:**
1. Use the back action of SCR-04.
2. Look at the transactions and the status of INV-3001.

**Expected Result:**
> 1. SCR-02 opens.
>  2. No transaction exists for INV-3001. INV-3001 is still Issued. The EA balance is still 20.00.

---

#### `TC-038`: Student without an EA can pay online only

- **Scenario ID**: `TS-008`
- **Test Suite**: F9.3 Payment method and eligibility
- **Page / Target**: `SCR-04 Choose payment method`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-10, PB-11; FS F9: AC-14; BR-F9-07; DA-03; 5.1 EA_NOT_AVAILABLE; SCR-04
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01
- **Assumption Reference**: ASM-R9-13: For a student without EA, the EA and split options are disabled and the EA_NOT_AVAILABLE text is shown as guidance, not as an error banner or error state.
- **Note**: xác nhận trace. UI mock: nút EA bị vô hiệu, Online được chọn sẵn, không có Split. Câu 'This student does not have an Education Account. Please pay online.' đúng chữ nhưng nằm trong khung nền hồng giống kiểu báo lỗi, trong khi ASM-R9-13 yêu cầu hiện như hướng dẫn, không như banner lỗi. Cần xác nhận kiểu hiển thị.

**Preconditions:**
```text
1. PAR-A is signed in.
 2. STU-102 has no EA.
```

**Test Data:**
```text
Student: STU-102 Chloe Tan, Permanent Resident, no Education Account
 Invoice: INV-2001 (75.00)
```

**Test Steps:**
1. Select INV-2001 on SCR-02 of STU-102.
2. Read the options and any text on SCR-04.

**Expected Result:**
> 1. The EA option and the split option are disabled.
>  2. The online payment option is available.
>  3. The text "This student does not have an Education Account. Please pay online." is shown as guidance and no error state or error banner is shown.
>  4. The Parent can continue with the online payment.

---

#### `TC-039`: Student with a Closed EA can pay online only

- **Scenario ID**: `TS-008`
- **Test Suite**: F9.3 Payment method and eligibility
- **Page / Target**: `SCR-04 Choose payment method`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-10, PB-11; FS F9: DA-06; BR-F9-02; 5.1 EA_NOT_ACTIVE; SCR-04
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01
- **Assumption Reference**: N/A
- **Note**: xác nhận trace (DA-06, BR-F9-02, EA_NOT_ACTIVE). Chưa kiểm được trên mock: student có EA Closed trên mock là 16 tuổi trở lên chỉ xem, không vào được màn chọn phương thức nên không thấy câu 'The Education Account is not active. Please pay online.'

**Preconditions:**
```text
1. PAR-E is signed in.
 2. STU-104 has an EA with the status Closed.
```

**Test Data:**
```text
Student: STU-104 Noah Wong, Singapore Citizen, EA status Closed, balance 0.00 SGD
 Invoice: INV-4001 (50.00)
```

**Test Steps:**
1. Select INV-4001 on SCR-02 of STU-104.
2. Read the options and any text on SCR-04.

**Expected Result:**
> 1. The EA option and the split option are disabled.
>  2. The online payment option is available.
>  3. The text "The Education Account is not active. Please pay online." is shown.

---

#### `TC-040`: Active EA with zero balance offers online payment only

- **Scenario ID**: `TS-008`
- **Test Suite**: F9.3 Payment method and eligibility
- **Page / Target**: `SCR-04 Choose payment method`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-10, PB-11; FS F9: BR-F9-02; Step 4; 5.1 EA_INSUFFICIENT_BALANCE; SCR-04
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01
- **Assumption Reference**: N/A
- **Note**: Inference: EA_INSUFFICIENT_BALANCE is the only reason in the SCR-04 list that fits a balance that is too low.
 xác nhận trên UI mock với EA 0.00: nút EA vô hiệu kèm câu EA_INSUFFICIENT_BALANCE, Online dùng được. Mock ẩn hẳn lựa chọn Split chứ không hiện ở dạng vô hiệu như Expected 2.

**Preconditions:**
```text
1. PAR-E is signed in.
 2. STU-105 has an Active EA with balance 0.00.
```

**Test Data:**
```text
Student: STU-105 Ava Wong, Singapore Citizen, EA Active, balance 0.00 SGD
 Invoice: INV-5001 (50.00)
```

**Test Steps:**
1. Select INV-5001 on SCR-02 of STU-105.
2. Read the options and any text on SCR-04.

**Expected Result:**
> 1. The EA option is disabled.
>  2. The split option is disabled because split needs a balance above 0.
>  3. The online payment option is available.
>  4. The text "Your Education Account balance is not enough for this amount. You can pay the rest online." is shown.

---

#### `TC-041`: Balance below the amount to pay disables EA and suggests split

- **Scenario ID**: `TS-008`
- **Test Suite**: F9.3 Payment method and eligibility
- **Page / Target**: `SCR-04 Choose payment method`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-10, PB-11; FS F9: AC-04; AC-22; BR-F9-02; Step 4; 5.1 EA_INSUFFICIENT_BALANCE; SCR-04
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01
- **Assumption Reference**: N/A
- **Note**: xác nhận. UI mock với EA 20.00 và invoice 50.00: nút EA vô hiệu, Split đề xuất EA 20.00 và Online 30.00, Online dùng được, câu EA_INSUFFICIENT_BALANCE hiện dưới ô EA.

**Preconditions:**
```text
1. PAR-A is signed in.
 2. STU-103 EA is Active with balance 20.00.
```

**Test Data:**
```text
Student: STU-103 Marcus Tan, Singapore Citizen, EA Active, balance 20.00 SGD
 Invoice: INV-3001 (50.00)
```

**Test Steps:**
1. Select INV-3001 on SCR-02 of STU-103.
2. Read the options on SCR-04.

**Expected Result:**
> 1. The EA only option is disabled.
>  2. The split option is offered with the EA part 20.00 and the online part 30.00.
>  3. The online payment option is available.
>  4. The text "Your Education Account balance is not enough for this amount. You can pay the rest online." is shown with the suggestion to pay the rest online.

---

#### `TC-042`: Balance equal to the amount to pay allows EA and online but not split

- **Scenario ID**: `TS-008`
- **Test Suite**: F9.3 Payment method and eligibility
- **Page / Target**: `SCR-04 Choose payment method`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-10, PB-11; FS F9: BR-F9-02; Step 4 (balance equal to or higher than the amount); SCR-04
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01
- **Assumption Reference**: ASM-R9-02: When the available balance is equal to or higher than the payable amount, the split option is not offered.
- **Note**: xác nhận trace (BR-F9-02, Step 4). Chưa kiểm trên UI mock vì cần số dư đúng bằng số phải trả; với số dư lớn hơn thì Split không hiện (xem TC-043).

**Preconditions:**
```text
1. PAR-E is signed in.
 2. STU-106 EA is Active with balance 50.00.
```

**Test Data:**
```text
Student: STU-106 Lily Wong, Singapore Citizen, EA Active, balance 50.00 SGD
 Invoice: INV-6001 (50.00)
```

**Test Steps:**
1. Select INV-6001 on SCR-02 of STU-106.
2. Read the options on SCR-04.

**Expected Result:**
> 1. The EA option is enabled.
>  2. The online payment option is enabled.
>  3. The split option is not offered.

---

#### `TC-043`: Balance above the amount to pay allows EA and online but not split

- **Scenario ID**: `TS-008`
- **Test Suite**: F9.3 Payment method and eligibility
- **Page / Target**: `SCR-04 Choose payment method`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-10, PB-11; FS F9: Step 4; BR-F9-02; DA-07; SCR-04
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01
- **Assumption Reference**: ASM-R9-02: When the available balance is equal to or higher than the payable amount, the split option is not offered.
- **Note**: xác nhận. UI mock với EA 440.07 và invoice 15.00: chỉ có EA và Online, không có Split.

**Preconditions:**
```text
1. PAR-A is signed in.
 2. STU-101 EA is Active with balance 200.00.
```

**Test Data:**
```text
Student: STU-101 Ethan Tan, Singapore Citizen, EA Active, balance 200.00 SGD
 Invoice: INV-1002 (50.00)
```

**Test Steps:**
1. Select INV-1002 on SCR-02 of STU-101.
2. Read the options on SCR-04.

**Expected Result:**
> 1. The EA option is enabled and the balance 200.00 is shown.
>  2. The online payment option is enabled.
>  3. The split option is not offered.

---

#### `TC-044`: Balance one cent below the amount to pay offers split with an online part of 0.01

- **Scenario ID**: `TS-008`
- **Test Suite**: F9.3 Payment method and eligibility
- **Page / Target**: `SCR-04 Choose payment method`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-10, PB-11; FS F9: BR-F9-02; Step 4; Step 5.2; 4.1 SCR-04 Online amount
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01
- **Assumption Reference**: ASM-R9-09: The sandbox provider has a minimum of M SGD given by Dev. An online part below M is rejected before any transaction is created and the Parent stays on SCR-04 with the amount marked. M and above is accepted. The EA part has no minimum.
- **Note**: xác nhận trace. Chưa kiểm trên UI mock vì cần dữ liệu có số dư kém số phải trả 0.01; mức tối thiểu của provider (ASM-R9-09) chưa có giá trị.

**Preconditions:**
```text
1. PAR-E is signed in.
 2. STU-108 EA is Active with balance 49.99.
```

**Test Data:**
```text
Student: STU-108 Owen Wong, Singapore Citizen, EA Active, balance 49.99 SGD
 Invoice: INV-8001 (50.00)
```

**Test Steps:**
1. Select INV-8001 on SCR-02 of STU-108.
2. Read the options on SCR-04.

**Expected Result:**
> 1. The EA only option is disabled.
>  2. The split option is offered with the EA part 49.99 and the online part 0.01.
>  3. If the provider minimum is above 0.01, the split cannot go on, the Parent stays on SCR-04 with the amount marked and can choose online payment.

---

#### `TC-045`: The EA is suggested when the balance is enough but nothing is debited until the Parent confirms

- **Scenario ID**: `TS-008`
- **Test Suite**: F9.3 Payment method and eligibility
- **Page / Target**: `SCR-04 Choose payment method`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-10, PB-11; FS F9: BR-F9-10; DA-08; Step 4
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-05
- **Assumption Reference**: N/A
- **Note**: xác nhận. UI mock: Education Account được chọn sẵn ở Step 1 nhưng chưa trừ gì cho đến khi bấm Authorize & Pay ở bước review; số dư sau thanh toán chỉ hiện dạng 'Estimated balance after (reference only)'.

**Preconditions:**
```text
1. PAR-A is signed in.
 2. STU-101 EA is Active with balance 200.00.
```

**Test Data:**
```text
Student: STU-101 Ethan Tan, Singapore Citizen, EA Active, balance 200.00 SGD
 Invoice: INV-1002 (50.00)
```

**Test Steps:**
1. Select INV-1002 on SCR-02.
2. Read SCR-04 without choosing a method.
3. Look at the EA balance and the transactions of INV-1002.
4. Use the back action.

**Expected Result:**
> 1. The EA may be suggested as the method.
>  2. No method is applied until the Parent chooses it and confirms on SCR-05.
>  3. The EA balance is still 200.00 and no transaction exists.

**Actual Result:**
> Chạy trên bản Dev local function9_14-10-26, Chrome, 2026-10-15; dữ liệu mẫu khác R9 nên không xét. Education Account được chọn sẵn ở bước Payment method. Request mạng chặn được trong lượt chạy cho thấy POST checkout chỉ xuất hiện sau khi bấm Authorize & pay, chọn khoản và qua các bước không tạo invoice hay transaction. Số dư EA trên UI không đổi.

---

#### `TC-046`: Selecting EA with a low balance is refused with the reason and nothing changes

- **Scenario ID**: `TS-008`
- **Test Suite**: F9.3 Payment method and eligibility
- **Page / Target**: `SCR-04 Choose payment method`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-10, PB-11; FS F9: AC-04; Step 5.3; 5.1 EA_INSUFFICIENT_BALANCE
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-05
- **Assumption Reference**: N/A
- **Note**: xác nhận. UI mock: khi EA không đủ, lựa chọn EA bị vô hiệu nên không chọn được, câu EA_INSUFFICIENT_BALANCE hiện dưới ô EA, chưa tạo giao dịch.

**Preconditions:**
```text
1. PAR-A is signed in and is on SCR-04 for INV-3001 of STU-103.
 2. STU-103 EA balance is 20.00.
```

**Test Data:**
```text
Student: STU-103 Marcus Tan, Singapore Citizen, EA Active, balance 20.00 SGD
 Invoice: INV-3001 (50.00)
```

**Test Steps:**
1. Try to choose the EA only option.
2. Look at the screen, the transactions of INV-3001 and the EA balance.

**Expected Result:**
> 1. The EA only option cannot be chosen.
>  2. The reason "Your Education Account balance is not enough for this amount. You can pay the rest online." is shown with the advice to pay online or to split.
>  3. No transaction is created. INV-3001 is still Issued. The EA balance is still 20.00.

---

#### `TC-047`: API refuses the EA method when the balance is too low

- **Scenario ID**: `TS-008`
- **Test Suite**: F9.3 Payment method and eligibility
- **Page / Target**: `API: create payment`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `API`
- **Traceability**: Tender R9; PB-10, PB-11; FS F9: AC-04; BR-F9-02; Step 5.1; 5.1 EA_INSUFFICIENT_BALANCE
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-05, ENV-R9-06
- **Assumption Reference**: N/A
- **Note**: xác nhận

**Preconditions:**
```text
1. PAR-A has a valid session.
 2. STU-103 EA balance is 20.00.
```

**Test Data:**
```text
Student: STU-103 Marcus Tan, Singapore Citizen, EA Active, balance 20.00 SGD
 Invoice: INV-3001 (50.00)
 Method: EA
 Idempotency key: SEL-KEY-001
```

**Test Steps:**
1. Send the create payment request with method EA for INV-3001.
2. Look at the answer, the transactions of INV-3001 and the EA balance.

**Expected Result:**
> 1. The request is refused with the reason EA_INSUFFICIENT_BALANCE.
>  2. No transaction is created. INV-3001 is still Issued. The EA balance is still 20.00.

---

#### `TC-048`: API refuses EA and split for a student without an EA

- **Scenario ID**: `TS-008`
- **Test Suite**: F9.3 Payment method and eligibility
- **Page / Target**: `API: create payment`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `API`
- **Traceability**: Tender R9; PB-10, PB-11; FS F9: BR-F9-07; DA-03; BR-F9-02; 5.1 EA_NOT_AVAILABLE
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-05, ENV-R9-06
- **Assumption Reference**: N/A
- **Note**: xác nhận

**Preconditions:**
```text
1. PAR-A has a valid session.
 2. STU-102 has no EA.
```

**Test Data:**
```text
Student: STU-102 Chloe Tan, Permanent Resident, no Education Account
 Invoice: INV-2001 (75.00)
 Methods tried: EA, then SPLIT with EA 25.00 and online 50.00
```

**Test Steps:**
1. Send the create payment request with method EA for INV-2001.
2. Send the create payment request with method SPLIT (EA 25.00, online 50.00) for INV-2001.
3. Look at the transactions of INV-2001.

**Expected Result:**
> 1. Both requests are refused with the reason EA_NOT_AVAILABLE.
>  2. No transaction is created and INV-2001 is still Issued.

---

#### `TC-049`: API refuses EA and split when the EA is Closed

- **Scenario ID**: `TS-008`
- **Test Suite**: F9.3 Payment method and eligibility
- **Page / Target**: `API: create payment`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `API`
- **Traceability**: Tender R9; PB-10, PB-11; FS F9: DA-06; BR-F9-02; Step 5.1; 5.1 EA_NOT_ACTIVE
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-05, ENV-R9-06
- **Assumption Reference**: N/A
- **Note**: xác nhận

**Preconditions:**
```text
1. PAR-E has a valid session.
 2. STU-104 EA status is Closed.
```

**Test Data:**
```text
Student: STU-104 Noah Wong, Singapore Citizen, EA status Closed, balance 0.00 SGD
 Invoice: INV-4001 (50.00)
 Methods tried: EA, then SPLIT with EA 10.00 and online 40.00
```

**Test Steps:**
1. Send the create payment request with method EA for INV-4001.
2. Send the create payment request with method SPLIT (EA 10.00, online 40.00) for INV-4001.
3. Look at the transactions of INV-4001.

**Expected Result:**
> 1. Both requests are refused with the reason EA_NOT_ACTIVE.
>  2. No transaction is created and INV-4001 is still Issued.

---

#### `TC-050`: Default split proposes the whole balance as the EA part and calculates the online part

- **Scenario ID**: `TS-009`
- **Test Suite**: F9.3 Payment method and eligibility
- **Page / Target**: `SCR-04 Choose payment method`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-10, PB-11; FS F9: AC-22; Step 4; BR-F9-02; BR-F9-10; 4.1 SCR-04 EA amount and Online amount
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01
- **Assumption Reference**: N/A
- **Note**: xác nhận. UI mock: chọn Split thì phần EA mặc định 20.00, phần Online 30.00 do hệ thống tính, EA only vô hiệu. Lưu ý FS 09 có hai chỗ khác nhau về ô EA: Step 4 nói Parent không được nhập, còn AC-22 và 4.1 SCR-04 (EA amount, Nhập: Có) cho đổi; mock cho nhập.

**Preconditions:**
```text
1. PAR-A is signed in and is on SCR-04 for INV-3001 of STU-103.
 2. STU-103 EA balance is 20.00.
```

**Test Data:**
```text
Student: STU-103 Marcus Tan, Singapore Citizen, EA Active, balance 20.00 SGD
 Invoice: INV-3001 (50.00)
```

**Test Steps:**
1. Choose the split option.
2. Read the two amounts.

**Expected Result:**
> 1. The EA part is 20.00, the whole available balance.
>  2. The online part is 30.00, calculated by the system, and the Parent does not type it.
>  3. The EA only option is disabled.

---

#### `TC-051`: The Parent can lower the EA part and the online part updates

- **Scenario ID**: `TS-009`
- **Test Suite**: F9.3 Payment method and eligibility
- **Page / Target**: `SCR-04 Choose payment method`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-10, PB-11; FS F9: AC-22; DA-08; BR-F9-10; 4.1 SCR-04
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01
- **Assumption Reference**: ASM-R9-01: The EA part starts at the whole available balance. The Parent can lower it to any amount above 0 and below the payable amount, and the online part is then Net minus the EA part. AC-22 is followed because it gives a worked example.
- **Note**: xác nhận. UI mock: nhập EA 10 thì phần Online tự cập nhật 40.00, tổng 50.00.

**Preconditions:**
```text
1. PAR-A is signed in and is on SCR-04 for INV-3001 of STU-103, with the split option chosen.
```

**Test Data:**
```text
Student: STU-103 Marcus Tan, Singapore Citizen, EA Active, balance 20.00 SGD
 Invoice: INV-3001 (50.00)
 EA part changed from 20.00 to 10.00
```

**Test Steps:**
1. Change the EA part from 20.00 to 10.00.
2. Read the online part.

**Expected Result:**
> 1. The online part updates to 40.00.
>  2. The two parts add up to 50.00.
>  3. The Parent can continue to SCR-05.

---

#### `TC-052`: The online part cannot be typed by the Parent

- **Scenario ID**: `TS-009`
- **Test Suite**: F9.3 Payment method and eligibility
- **Page / Target**: `SCR-04 Choose payment method`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `UI`
- **Traceability**: Tender R9; PB-10, PB-11; FS F9: 4.1 SCR-04 Online amount (input: No); Step 4
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01
- **Assumption Reference**: N/A
- **Note**: xác nhận. UI mock: ô Remaining via Online chỉ đọc (read only).

**Preconditions:**
```text
1. PAR-A is signed in and is on SCR-04 for INV-3001 of STU-103, with the split option chosen.
```

**Test Data:**
```text
Student: STU-103 Marcus Tan, Singapore Citizen, EA Active, balance 20.00 SGD
 Invoice: INV-3001
```

**Test Steps:**
1. Try to type a value in the online amount.

**Expected Result:**
> 1. The online amount is calculated and read only.
>  2. Typing is not possible.

---

#### `TC-053`: An EA part of zero is refused and the Parent stays on the screen

- **Scenario ID**: `TS-009`
- **Test Suite**: F9.3 Payment method and eligibility
- **Page / Target**: `SCR-04 Choose payment method`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-10, PB-11; FS F9: AC-19; BR-F9-11; 5.1 SPLIT_AMOUNT_INVALID
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-05
- **Assumption Reference**: ASM-R9-01: The EA part starts at the whole available balance. The Parent can lower it to any amount above 0 and below the payable amount, and the online part is then Net minus the EA part. AC-22 is followed because it gives a worked example.
- **Note**: xác nhận. UI mock: EA bằng 0 hoặc để trống hiện đúng câu SPLIT_AMOUNT_INVALID, ô nhập viền đỏ, Continue to Review không đi tiếp, ở lại bước chọn phương thức.

**Preconditions:**
```text
1. PAR-A is signed in and is on SCR-04 for INV-3001 of STU-103, with the split option chosen.
```

**Test Data:**
```text
Student: STU-103 Marcus Tan, Singapore Citizen, EA Active, balance 20.00 SGD
 Invoice: INV-3001 (50.00)
 EA part: 0.00
```

**Test Steps:**
1. Change the EA part to 0.00.
2. Try to continue.

**Expected Result:**
> 1. The message "The two amounts must be more than zero and add up to the total." is shown.
>  2. The Parent stays on SCR-04 and the amount field is marked.
>  3. No transaction is created.

---

#### `TC-054`: API refuses a split with an online part of zero

- **Scenario ID**: `TS-009`
- **Test Suite**: F9.3 Payment method and eligibility
- **Page / Target**: `API: create payment`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `API`
- **Traceability**: Tender R9; PB-10, PB-11; FS F9: AC-19; BR-F9-11; 5.1 SPLIT_AMOUNT_INVALID
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-05, ENV-R9-06
- **Assumption Reference**: N/A
- **Note**: xác nhận

**Preconditions:**
```text
1. PAR-E has a valid session.
 2. STU-106 EA balance is 50.00.
```

**Test Data:**
```text
Student: STU-106 Lily Wong, Singapore Citizen, EA Active, balance 50.00 SGD
 Invoice: INV-6001 (50.00)
 Method: SPLIT, EA 50.00, online 0.00
```

**Test Steps:**
1. Send the create payment request with the split amounts EA 50.00 and online 0.00.
2. Look at the answer and the transactions of INV-6001.

**Expected Result:**
> 1. The request is refused with SPLIT_AMOUNT_INVALID.
>  2. No transaction is created. INV-6001 is still Issued. The EA balance is still 50.00.

---

#### `TC-055`: API refuses a split whose parts add up to less than the amount to pay

- **Scenario ID**: `TS-009`
- **Test Suite**: F9.3 Payment method and eligibility
- **Page / Target**: `API: create payment`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `API`
- **Traceability**: Tender R9; PB-10, PB-11; FS F9: AC-19; BR-F9-11; BR-F9-13; 5.1 SPLIT_AMOUNT_INVALID
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-05, ENV-R9-06
- **Assumption Reference**: N/A
- **Note**: xác nhận

**Preconditions:**
```text
1. PAR-A has a valid session.
 2. STU-103 EA balance is 20.00.
```

**Test Data:**
```text
Student: STU-103 Marcus Tan, Singapore Citizen, EA Active, balance 20.00 SGD
 Invoice: INV-3001 (50.00)
 Method: SPLIT, EA 20.00, online 20.00 (sum 40.00)
```

**Test Steps:**
1. Send the create payment request with the split amounts EA 20.00 and online 20.00.
2. Look at the answer and the transactions of INV-3001.

**Expected Result:**
> 1. The request is refused with SPLIT_AMOUNT_INVALID.
>  2. No transaction is created and nothing changes.

---

#### `TC-056`: API refuses a split whose parts add up to more than the amount to pay

- **Scenario ID**: `TS-009`
- **Test Suite**: F9.3 Payment method and eligibility
- **Page / Target**: `API: create payment`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `API`
- **Traceability**: Tender R9; PB-10, PB-11; FS F9: AC-19; BR-F9-11; BR-F9-13; 5.1 SPLIT_AMOUNT_INVALID
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-05, ENV-R9-06
- **Assumption Reference**: N/A
- **Note**: xác nhận

**Preconditions:**
```text
1. PAR-A has a valid session.
 2. STU-103 EA balance is 20.00.
```

**Test Data:**
```text
Student: STU-103 Marcus Tan, Singapore Citizen, EA Active, balance 20.00 SGD
 Invoice: INV-3001 (50.00)
 Method: SPLIT, EA 20.00, online 35.00 (sum 55.00)
```

**Test Steps:**
1. Send the create payment request with the split amounts EA 20.00 and online 35.00.
2. Look at the answer and the transactions of INV-3001.

**Expected Result:**
> 1. The request is refused with SPLIT_AMOUNT_INVALID.
>  2. No transaction is created and the EA balance is still 20.00.

---

#### `TC-057`: API refuses an EA part above the available balance

- **Scenario ID**: `TS-009`
- **Test Suite**: F9.3 Payment method and eligibility
- **Page / Target**: `API: create payment`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `API`
- **Traceability**: Tender R9; PB-10, PB-11; FS F9: Step 5.1; 4.1 SCR-04 EA amount (not above the available balance); 5.1 EA_INSUFFICIENT_BALANCE
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-05, ENV-R9-06
- **Assumption Reference**: N/A
- **Note**: xác nhận trace. UI mock: nhập EA 25 (vượt số dư 20.00) hiện câu 'EA portion cannot exceed available balance (SGD 20.00)', không phải câu EA_INSUFFICIENT_BALANCE của FS 5.1.

**Preconditions:**
```text
1. PAR-A has a valid session.
 2. STU-103 EA balance is 20.00.
```

**Test Data:**
```text
Student: STU-103 Marcus Tan, Singapore Citizen, EA Active, balance 20.00 SGD
 Invoice: INV-3001 (50.00)
 Method: SPLIT, EA 25.00, online 25.00
```

**Test Steps:**
1. Send the create payment request with the split amounts EA 25.00 and online 25.00.
2. Look at the answer, the transactions and the EA balance.

**Expected Result:**
> 1. The request is refused with the reason EA_INSUFFICIENT_BALANCE.
>  2. No transaction is created and the EA balance is still 20.00.

---

#### `TC-058`: API refuses a negative EA part

- **Scenario ID**: `TS-009`
- **Test Suite**: F9.3 Payment method and eligibility
- **Page / Target**: `API: create payment`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `API`
- **Traceability**: Tender R9; PB-10, PB-11; FS F9: AC-19; BR-F9-11; 4.1 SCR-04 EA amount (more than 0)
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-05, ENV-R9-06
- **Assumption Reference**: ASM-R9-24: An amount that is not a number, is empty, is negative or has more than two decimals is rejected on SCR-04 with the field marked, no transaction is created and nothing changes. Zero or a negative amount shows SPLIT_AMOUNT_INVALID.
- **Note**: xác nhận trace. UI mock: nhập số âm hiện đúng câu SPLIT_AMOUNT_INVALID và ô nhập viền đỏ.

**Preconditions:**
```text
1. PAR-A has a valid session.
 2. STU-103 EA balance is 20.00.
```

**Test Data:**
```text
Student: STU-103 Marcus Tan, Singapore Citizen, EA Active, balance 20.00 SGD
 Invoice: INV-3001 (50.00)
 Method: SPLIT, EA -5.00, online 55.00
```

**Test Steps:**
1. Send the create payment request with the split amounts EA -5.00 and online 55.00.
2. Look at the answer and the EA balance.

**Expected Result:**
> 1. The request is refused. The message "The two amounts must be more than zero and add up to the total." is shown.
>  2. No transaction is created and the EA balance is still 20.00.

---

#### `TC-059`: An EA part with more than two decimals or with text is refused

- **Scenario ID**: `TS-009`
- **Test Suite**: F9.3 Payment method and eligibility
- **Page / Target**: `SCR-04 Choose payment method`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-10, PB-11; FS F9: 4.1 SCR-04 EA amount (Decimal(18,2)); VAL-18
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-05
- **Assumption Reference**: ASM-R9-01: The EA part starts at the whole available balance. The Parent can lower it to any amount above 0 and below the payable amount, and the online part is then Net minus the EA part. AC-22 is followed because it gives a worked example.
 ASM-R9-24: An amount that is not a number, is empty, is negative or has more than two decimals is rejected on SCR-04 with the field marked, no transaction is created and nothing changes. Zero or a negative amount shows SPLIT_AMOUNT_INVALID.
- **Note**: Traceability có VAL-18 nhưng FS 09 không có bảng validation (không có mục 5.2; VAL-18 chỉ được nhắc ở NQ-13 trong Appendix B); phần 4.1 SCR-04 EA amount Decimal(18,2) có trong FS. UI mock: nhập 10.123 bị tự làm tròn thành 10.12 và không báo lỗi (khác Expected 1); ô number không cho gõ chữ, giá trị chữ thành 0.00 và hiện SPLIT_AMOUNT_INVALID.

**Preconditions:**
```text
1. PAR-A is signed in and is on SCR-04 for INV-3001 of STU-103, with the split option chosen.
```

**Test Data:**
```text
Student: STU-103 Marcus Tan, Singapore Citizen, EA Active, balance 20.00 SGD
 Values tried: 10.005, abc, empty
```

**Test Steps:**
1. Type 10.005 as the EA part and try to continue.
2. Type abc and try to continue.
3. Clear the field and try to continue.

**Expected Result:**
> 1. Each value is refused and the amount field is marked.
>  2. The Parent stays on SCR-04.
>  3. No transaction is created.

---

#### `TC-060`: Online part exactly at the provider minimum is accepted

- **Scenario ID**: `TS-009`
- **Test Suite**: F9.3 Payment method and eligibility
- **Page / Target**: `API: create payment`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-10, PB-11; FS F9: Step 5.2; 4.1 SCR-04 Online amount; NQ-13
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-02, ENV-R9-05, ENV-R9-06
- **Assumption Reference**: ASM-R9-09: The sandbox provider has a minimum of M SGD given by Dev. An online part below M is rejected before any transaction is created and the Parent stays on SCR-04 with the amount marked. M and above is accepted. The EA part has no minimum.
- **Note**: xác nhận trace (Step 5.2, 4.1 SCR-04 Online amount, NQ-13). Giá trị M của provider chưa có (ASM-R9-09).

**Preconditions:**
```text
1. PAR-E has a valid session.
 2. The provider minimum is M SGD (value from Dev).
 3. STU-108 EA balance is 49.99.
```

**Test Data:**
```text
Student: STU-108 Owen Wong, Singapore Citizen, EA Active, balance 49.99 SGD
 Invoice: fresh Issued invoice for STU-108 with Net = 49.99 + M
 Method: SPLIT, EA 49.99, online M
```

**Test Steps:**
1. Send the create payment request with the split amounts EA 49.99 and online M.
2. Look at the answer.

**Expected Result:**
> 1. The request is accepted and a transaction is created with an EA leg of 49.99 and an online leg of M.

---

#### `TC-061`: Online part just below the provider minimum is refused

- **Scenario ID**: `TS-009`
- **Test Suite**: F9.3 Payment method and eligibility
- **Page / Target**: `API: create payment`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `API`
- **Traceability**: Tender R9; PB-10, PB-11; FS F9: Step 5.2; 4.1 SCR-04 Online amount; NQ-13
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-05, ENV-R9-06
- **Assumption Reference**: ASM-R9-09: The sandbox provider has a minimum of M SGD given by Dev. An online part below M is rejected before any transaction is created and the Parent stays on SCR-04 with the amount marked. M and above is accepted. The EA part has no minimum.
- **Note**: xác nhận trace (Step 5.2, 4.1 SCR-04 Online amount, NQ-13). Giá trị M của provider chưa có (ASM-R9-09).

**Preconditions:**
```text
1. PAR-E has a valid session.
 2. The provider minimum is M SGD (value from Dev).
 3. STU-108 EA balance is 49.99.
```

**Test Data:**
```text
Student: STU-108 Owen Wong, Singapore Citizen, EA Active, balance 49.99 SGD
 Invoice: fresh Issued invoice for STU-108 with Net = 49.99 + M minus 0.01
 Method: SPLIT, EA 49.99, online M minus 0.01
```

**Test Steps:**
1. Send the create payment request with the split amounts EA 49.99 and online M minus 0.01.
2. Look at the answer, the transactions and the EA balance.

**Expected Result:**
> 1. The request is refused before any transaction is created.
>  2. The EA balance is still 49.99 and the invoice is still Issued.

---

#### `TC-062`: A very small EA part is accepted because the EA part has no minimum

- **Scenario ID**: `TS-009`
- **Test Suite**: F9.3 Payment method and eligibility
- **Page / Target**: `SCR-04 Choose payment method`
- **Severity / Priority**: `S4 (lowest)` / `Low`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-10, PB-11; FS F9: NQ-13 (no minimum for the EA part); BR-F9-11; 4.1 SCR-04
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01
- **Assumption Reference**: ASM-R9-01: The EA part starts at the whole available balance. The Parent can lower it to any amount above 0 and below the payable amount, and the online part is then Net minus the EA part. AC-22 is followed because it gives a worked example.
 ASM-R9-09: The sandbox provider has a minimum of M SGD given by Dev. An online part below M is rejected before any transaction is created and the Parent stays on SCR-04 with the amount marked. M and above is accepted. The EA part has no minimum.
- **Note**: xác nhận. UI mock: EA 0.01 được nhận, phần Online hiện 49.99, không báo lỗi. Chưa đi tiếp đến SCR-05 với giá trị này.

**Preconditions:**
```text
1. PAR-A is signed in and is on SCR-04 for INV-3001 of STU-103, with the split option chosen.
```

**Test Data:**
```text
Student: STU-103 Marcus Tan, Singapore Citizen, EA Active, balance 20.00 SGD
 EA part changed to 0.01, online part 49.99
```

**Test Steps:**
1. Change the EA part to 0.01.
2. Read the online part.
3. Continue to SCR-05.

**Expected Result:**
> 1. The online part is 49.99.
>  2. SCR-05 opens with the EA part 0.01 and the online part 49.99.

---


### Test Suite: F9.4 Pay with Education Account

#### `TC-063`: Review screen for an EA payment shows the amounts and the balance after payment

- **Scenario ID**: `TS-010`
- **Test Suite**: F9.4 Pay with Education Account
- **Page / Target**: `SCR-05 Review and confirm`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-10; FS F9: Step 6.1; 4.1 SCR-05 (Amount to pay, EA balance after payment); SCR-05
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01
- **Assumption Reference**: N/A
- **Note**: xác nhận. UI mock bước review hiện con, invoice, trường, Total Amount to Pay, Education Account Deduction và 'Estimated balance after (reference only)', không có dòng Online.

**Preconditions:**
```text
1. PAR-A is signed in and is on SCR-04 for a fresh 50.00 invoice of STU-101.
 2. STU-101 EA balance is 200.00.
```

**Test Data:**
```text
Student: STU-101 Ethan Tan, Singapore Citizen, EA Active, balance 200.00 SGD
 Invoice: a fresh Issued invoice for STU-101, Net 50.00 SGD, created by the seed script just before the case
 Method: EA
```

**Test Steps:**
1. Choose the EA option and continue.
2. Read SCR-05.

**Expected Result:**
> 1. SCR-05 shows the child STU-101 Ethan Tan, the invoice number and the amount to pay 50.00 SGD.
>  2. It shows the method EA and the EA amount 50.00.
>  3. It shows the EA balance after payment 150.00 as information only.
>  4. No online part is shown.

**Actual Result:**
> Chạy trên bản Dev local function9_14-10-26, Chrome, 2026-10-15; dữ liệu mẫu khác R9 nên không xét. Chưa chạy review của EA only trong lượt này. Màn review của online và split chỉ hiện số dư EA hiện tại (250), không có dòng số dư sau thanh toán; nếu màn review EA dùng cùng bố cục thì Expected 3 sẽ không đạt. Cần chạy lại để kết luận.

---

#### `TC-064`: Cancel on the review screen returns to the payment method screen and creates nothing

- **Scenario ID**: `TS-010`
- **Test Suite**: F9.4 Pay with Education Account
- **Page / Target**: `SCR-05 Review and confirm`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-10; FS F9: Appendix C SCR-05 actions; BR-F9-10
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-05
- **Assumption Reference**: ASM-R9-11: Back on SCR-04 returns to SCR-02. Cancel on SCR-05 returns to SCR-04. Neither action creates a transaction or changes an invoice.
- **Note**: xác nhận. UI mock: Cancel ở bước review quay về chọn phương thức, chưa tạo giao dịch.

**Preconditions:**
```text
1. PAR-A is signed in and is on SCR-05 for a fresh 50.00 invoice of STU-101 with the EA method.
```

**Test Data:**
```text
Student: STU-101 Ethan Tan, Singapore Citizen, EA Active, balance 200.00 SGD
 Invoice: a fresh Issued invoice for STU-101, Net 50.00 SGD, created by the seed script just before the case
```

**Test Steps:**
1. Use the cancel action of SCR-05.
2. Look at the transactions of the invoice and the EA balance.

**Expected Result:**
> 1. SCR-04 opens.
>  2. No transaction exists for the invoice. The invoice is still Issued. The EA balance is still 200.00.

---

#### `TC-065`: Paying a 50.00 invoice with the EA debits the balance once and marks the invoice Paid

- **Scenario ID**: `TS-011`
- **Test Suite**: F9.4 Pay with Education Account
- **Page / Target**: `SCR-07 Payment confirmation`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-10; FS F9: AC-03; BR-F9-03; BR-F9-13; DA-02; Step 6.3; 4.2 FundingLeg; SCR-07
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-03, ENV-R9-05
- **Assumption Reference**: N/A
- **Note**: xác nhận. UI mock EA only thành công: biên lai hiện Payment Succeeded, mã tham chiếu dạng PAY, giờ SGT, dòng Education Account kèm Ref dạng FND, Total Settled; số dư EA giảm đúng một lần (455.07 còn 440.07) và sao kê EA có dòng Fee payment kèm FundingReference. Ledger ID và số Requested, Settled không xem được trên mock.

**Preconditions:**
```text
1. PAR-A is signed in and is on SCR-05 for a fresh 50.00 invoice of STU-101 with the EA method.
 2. STU-101 EA balance is 200.00. STU-103 EA balance is 20.00.
```

**Test Data:**
```text
Student: STU-101 Ethan Tan, Singapore Citizen, EA Active, balance 200.00 SGD
 Invoice: a fresh Issued invoice for STU-101, Net 50.00 SGD, created by the seed script just before the case
 Method: EA
 Idempotency key: client generated
```

**Test Steps:**
1. Confirm the payment.
2. Read SCR-07.
3. Look at the transaction, the EA leg, the invoice and the Function 1 ledger by the FundingReference.
4. Read the EA balance of STU-101 and of STU-103.

**Expected Result:**
> 1. SCR-07 shows success, a transaction reference, the time, the EA part 50.00 and the total 50.00.
>  2. The transaction is Succeeded and the EA leg is Succeeded. Requested and Settled amounts are 50.00.
>  3. The invoice is Paid.
>  4. The ledger has one debit of 50.00 for the FundingReference and its ledger ID is stored in the EA leg.
>  5. The EA balance of STU-101 is 150.00. The balance of STU-103 is still 20.00.

**Actual Result:**
> Chạy trên bản Dev local function9_14-10-26, Chrome, 2026-10-15; dữ liệu mẫu khác R9 nên không xét. EA only thành công: trang kết quả Payment successful, có Transaction ID, invoice INV000001, Completed at, dòng Education Account Succeeded requested 120 settled 120, tổng 120. DB: transaction Succeeded, một lượt EA Succeeded có EducationAccountTransactionId, invoice Paid. Chưa kiểm được Expected 4 và 5 (sổ cái Function 1 và số dư của hai học sinh) vì số dư EA trên UI gắn cứng 250 trong bản dev.

---

#### `TC-066`: Status changes of an EA payment follow Appendix A and are written to the audit log

- **Scenario ID**: `TS-011`
- **Test Suite**: F9.4 Pay with Education Account
- **Page / Target**: `Audit log`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: Tender R9; PB-10; FS F9: Appendix A; 4.2 AuditLog; DA-12; Step 6.3
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-05
- **Assumption Reference**: N/A
- **Note**: The owner of the audit log is still open (D5).
 xác nhận trace (Appendix A, 4.2 AuditLog). UI mock không có audit log.

**Preconditions:**
```text
1. A fresh 50.00 invoice of STU-101 is paid with the EA by PAR-A.
```

**Test Data:**
```text
Student: STU-101 Ethan Tan, Singapore Citizen, EA Active, balance 200.00 SGD
 Invoice: a fresh Issued invoice for STU-101, Net 50.00 SGD, created by the seed script just before the case
```

**Test Steps:**
1. Pay the invoice with the EA.
2. Read the audit log entries of the transaction, the EA leg and the invoice in time order.

**Expected Result:**
> 1. The entries show: transaction created Pending and invoice Issued to PaymentPending; EA leg Pending to Succeeded; transaction Pending to Succeeded; invoice PaymentPending to Paid.
>  2. Each entry has the actor, the action, the entity, the old and new value and a time.

---

#### `TC-067`: Paying a two line invoice of 130.00 debits the full Net amount

- **Scenario ID**: `TS-011`
- **Test Suite**: F9.4 Pay with Education Account
- **Page / Target**: `SCR-07 Payment confirmation`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-10; FS F9: BR-F9-13; DA-05; AC-03; 4.2 Transaction RequestedAmount
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-03, ENV-R9-05
- **Assumption Reference**: N/A
- **Note**: xác nhận. UI mock: EA only trừ đủ số phải trả của invoice một lần (15.00).

**Preconditions:**
```text
1. PAR-A is signed in and is on SCR-05 for a fresh two line invoice of STU-101 with the EA method.
 2. STU-101 EA balance is 200.00.
```

**Test Data:**
```text
Student: STU-101 Ethan Tan, Singapore Citizen, EA Active, balance 200.00 SGD
 Invoice: a fresh Issued invoice for STU-101 with two lines, Net 130.00 SGD (same as INV-1003), created by the seed script just before the case
 Method: EA
```

**Test Steps:**
1. Confirm the payment.
2. Read SCR-07 and the EA balance.
3. Look at the Requested amount of the transaction and of the EA leg.

**Expected Result:**
> 1. The EA is debited 130.00 once and the balance is 70.00.
>  2. The Requested amount of the transaction and of the EA leg is 130.00, equal to the Net amount of the invoice.
>  3. The invoice is Paid.

---

#### `TC-068`: Balance equal to the amount to pay is paid and the balance becomes 0.00

- **Scenario ID**: `TS-011`
- **Test Suite**: F9.4 Pay with Education Account
- **Page / Target**: `SCR-07 Payment confirmation`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-10; FS F9: AC-03; AC-06 (balance not negative); BR-F9-02
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-03, ENV-R9-05
- **Assumption Reference**: N/A
- **Note**: xác nhận trace (AC-03, AC-06, BR-F9-02). Chưa kiểm trên UI mock vì cần EA đúng bằng số phải trả; sau split số dư EA hiện 0.00, không âm.

**Preconditions:**
```text
1. PAR-E is signed in and is on SCR-05 for INV-6001 of STU-106 with the EA method.
 2. STU-106 EA balance is 50.00.
```

**Test Data:**
```text
Student: STU-106 Lily Wong, Singapore Citizen, EA Active, balance 50.00 SGD
 Invoice: INV-6001 (50.00)
 Method: EA
```

**Test Steps:**
1. Confirm the payment.
2. Read SCR-07 and the EA balance.

**Expected Result:**
> 1. The payment succeeds and the invoice is Paid.
>  2. The EA balance is 0.00 and is never negative.

---

#### `TC-069`: The EA pays each of the four fee types

- **Scenario ID**: `TS-011`
- **Test Suite**: F9.4 Pay with Education Account
- **Page / Target**: `SCR-07 Payment confirmation`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-10; FS F9: OQ-11; 4.1 SCR-02 Fee type; BR-F9-02
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-03, ENV-R9-05
- **Assumption Reference**: ASM-R9-12: The EA can pay all four fee types: school fee, miscellaneous, extracurricular and ad hoc.
- **Note**: xác nhận trace (OQ-11, 4.1 SCR-02 Fee type). UI mock có đủ bốn loại phí (School fee, Extracurricular, Ad hoc, Miscellaneous); mới trả bằng EA một invoice Ad hoc (Library book replacement), chưa chạy từng loại.

**Preconditions:**
```text
1. PAR-A is signed in.
 2. STU-101 EA balance is 200.00.
 3. Four fresh invoices exist for STU-101: school fee 60.00, miscellaneous 40.00, extracurricular 30.00, ad hoc 50.00.
```

**Test Data:**
```text
Student: STU-101 Ethan Tan, Singapore Citizen, EA Active, balance 200.00 SGD
 Invoices: one per fee type (60.00, 40.00, 30.00, 50.00)
```

**Test Steps:**
1. Pay the school fee invoice with the EA.
2. Pay the miscellaneous invoice with the EA.
3. Pay the extracurricular invoice with the EA.
4. Pay the ad hoc invoice with the EA.
5. Read the EA balance.

**Expected Result:**
> 1. Each payment succeeds and each invoice is Paid.
>  2. The EA balance is 20.00 (200.00 minus 180.00).

---

#### `TC-070`: After an EA payment the list shows the new balance and no longer shows the invoice

- **Scenario ID**: `TS-011`
- **Test Suite**: F9.4 Pay with Education Account
- **Page / Target**: `SCR-02 Outstanding fees`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-10; FS F9: AC-03; SCR-07 action back to SCR-02
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01
- **Assumption Reference**: ASM-R9-03: SCR-02 lists invoices in Issued (payable) and PaymentPending (shown as Pending, not selectable). Paid, Cancelled and Draft are not listed. The total owed is the sum of Net of the listed invoices. SCR-03 appears only when the child has no listed invoice.
- **Note**: xác nhận. UI mock sau khi trả: số dư EA mới, invoice đã trả rời OUTSTANDING INVOICES và sang RECENT PAYMENTS, invoice khác giữ nguyên.

**Preconditions:**
```text
1. PAR-A has just paid a fresh 50.00 invoice of STU-101 with the EA.
```

**Test Data:**
```text
Student: STU-101 Ethan Tan, Singapore Citizen, EA Active, balance 200.00 SGD
 Invoice: a fresh Issued invoice for STU-101, Net 50.00 SGD, created by the seed script just before the case
```

**Test Steps:**
1. On SCR-07 go back to SCR-02 of STU-101.
2. Read the EA widget and the invoice list.

**Expected Result:**
> 1. The EA balance is 150.00.
>  2. The paid invoice is not in the list of outstanding invoices.
>  3. The other invoices of STU-101 are unchanged.

**Actual Result:**
> Chạy trên bản Dev local function9_14-10-26, Chrome, 2026-10-15; dữ liệu mẫu khác R9 nên không xét. Sau khi trả, khoản đã trả không còn trong danh sách phí chưa thanh toán, các khoản khác giữ nguyên (còn 210 và 140, tổng 350). Số dư EA trên UI vẫn 250 vì gắn cứng trong bản dev nên chưa kiểm được Expected 1.

---

#### `TC-071`: Balance falling below the amount before confirm fails the EA leg and changes nothing

- **Scenario ID**: `TS-012`
- **Test Suite**: F9.4 Pay with Education Account
- **Page / Target**: `SCR-08 Payment failed`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-10; FS F9: EX-05; AC-04; Step 6.3; 5.1 EA_INSUFFICIENT_BALANCE; Appendix A
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-03, ENV-R9-05
- **Assumption Reference**: N/A
- **Note**: xác nhận trace. UI mock không có cách đổi số dư giữa lúc xem và lúc xác nhận.

**Preconditions:**
```text
1. PAR-A is signed in and is on SCR-05 for a fresh 50.00 invoice of STU-101 with the EA method.
 2. STU-101 EA balance is 200.00 when SCR-05 opens.
```

**Test Data:**
```text
Student: STU-101 Ethan Tan, Singapore Citizen, EA Active, balance 200.00 SGD
 Invoice: a fresh Issued invoice for STU-101, Net 50.00 SGD, created by the seed script just before the case
 Balance changed to 30.00 before the confirm
```

**Test Steps:**
1. Without leaving SCR-05, set the EA balance of STU-101 to 30.00 in Function 1.
2. Confirm the payment.
3. Look at the screen, the transaction, the EA leg, the invoice and the balance.

**Expected Result:**
> 1. The EA leg is Failed and the transaction is Failed.
>  2. The invoice is back to Issued.
>  3. The EA balance is still 30.00 and no debit is in the ledger.
>  4. The message "Your Education Account balance is not enough for this amount. You can pay the rest online." is shown with the advice to choose another method or to split.

---

#### `TC-072`: Function 1 error during the debit fails the payment and the invoice is not Paid

- **Scenario ID**: `TS-012`
- **Test Suite**: F9.4 Pay with Education Account
- **Page / Target**: `SCR-08 Payment failed`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-10; FS F9: EX-10; AC-07; Step 6.3; 5.1 PAYMENT_FAILED; SCR-08
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-03, ENV-R9-05
- **Assumption Reference**: N/A
- **Note**: xác nhận trace. UI mock không có công tắc lỗi Function 1.

**Preconditions:**
```text
1. PAR-A is signed in and is on SCR-05 for a fresh 50.00 invoice of STU-101 with the EA method.
 2. Function 1 is set to fail the debit and roll it back.
```

**Test Data:**
```text
Student: STU-101 Ethan Tan, Singapore Citizen, EA Active, balance 200.00 SGD
 Invoice: a fresh Issued invoice for STU-101, Net 50.00 SGD, created by the seed script just before the case
```

**Test Steps:**
1. Confirm the payment.
2. Look at SCR-08, the transaction, the EA leg, the invoice and the balance.

**Expected Result:**
> 1. The EA leg is Failed, the transaction is Failed and the invoice is back to Issued.
>  2. The EA balance is still 200.00 and no debit is in the ledger.
>  3. SCR-08 shows "Your payment could not be completed. No amount was deducted." with the buttons Try again and Exit.

---

#### `TC-073`: Unclear debit result with Function 1 confirming nothing was debited fails the leg

- **Scenario ID**: `TS-012`
- **Test Suite**: F9.4 Pay with Education Account
- **Page / Target**: `SCR-08 Payment failed`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-10; FS F9: BR-F9-03; AC-07; EX-10
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-03, ENV-R9-05
- **Assumption Reference**: N/A
- **Note**: xác nhận trace. UI mock không có công tắc lỗi Function 1.

**Preconditions:**
```text
1. PAR-A is signed in and is on SCR-05 for a fresh 50.00 invoice of STU-101 with the EA method.
 2. Function 1 times out on the debit and, when asked with the same FundingReference, answers that nothing was debited.
```

**Test Data:**
```text
Student: STU-101 Ethan Tan, Singapore Citizen, EA Active, balance 200.00 SGD
 Invoice: a fresh Issued invoice for STU-101, Net 50.00 SGD, created by the seed script just before the case
```

**Test Steps:**
1. Confirm the payment.
2. Look at the calls to Function 1 and at the leg, the transaction, the invoice and the balance.

**Expected Result:**
> 1. The system asks Function 1 again with the same FundingReference.
>  2. The EA leg is Failed, the transaction is Failed and the invoice is Issued.
>  3. The balance is still 200.00. The Parent sees "Your payment could not be completed. No amount was deducted."

---

#### `TC-074`: Unclear debit result with Function 1 confirming the debit leads to a reversal

- **Scenario ID**: `TS-012`
- **Test Suite**: F9.4 Pay with Education Account
- **Page / Target**: `SCR-08 Payment failed`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-10; FS F9: BR-F9-03; AC-07; EX-10; Appendix A
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-03, ENV-R9-05
- **Assumption Reference**: ASM-R9-16: If Function 1 confirms the debit after an unclear result, the system reverses it as BR-F9-03 says: the EA leg ends Reversed, the transaction Failed, the invoice Issued, the balance unchanged and the Parent sees PAYMENT_FAILED. If Function 1 says nothing was debited, the leg is Failed. If Function 1 cannot say, the leg and the transaction are ReconciliationRequired.
- **Note**: xác nhận trace. UI mock không có công tắc lỗi Function 1.

**Preconditions:**
```text
1. PAR-A is signed in and is on SCR-05 for a fresh 50.00 invoice of STU-101 with the EA method.
 2. Function 1 debits 50.00, then times out before it answers. When asked with the same FundingReference it answers that the debit was made.
```

**Test Data:**
```text
Student: STU-101 Ethan Tan, Singapore Citizen, EA Active, balance 200.00 SGD
 Invoice: a fresh Issued invoice for STU-101, Net 50.00 SGD, created by the seed script just before the case
```

**Test Steps:**
1. Confirm the payment.
2. Look at the ledger, the EA leg, the transaction, the invoice and the balance.

**Expected Result:**
> 1. The ledger shows exactly one debit and one reversal of 50.00 for the payment.
>  2. The EA leg is Reversed, the transaction is Failed and the invoice is Issued.
>  3. The EA balance is back to 200.00. The Parent sees "Your payment could not be completed. No amount was deducted."

---

#### `TC-075`: Unclear debit result that stays unclear moves to ReconciliationRequired

- **Scenario ID**: `TS-012`
- **Test Suite**: F9.4 Pay with Education Account
- **Page / Target**: `SCR-06 Pending`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-10; FS F9: BR-F9-03; EX-10; AC-07; Step 7.6; Appendix A; SCR-06 Verifying
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-03, ENV-R9-05
- **Assumption Reference**: N/A
- **Note**: xác nhận trace. UI mock không có công tắc lỗi Function 1.

**Preconditions:**
```text
1. PAR-A is signed in and is on SCR-05 for a fresh 50.00 invoice of STU-101 with the EA method.
 2. Function 1 times out on the debit and also on every question about the FundingReference.
```

**Test Data:**
```text
Student: STU-101 Ethan Tan, Singapore Citizen, EA Active, balance 200.00 SGD
 Invoice: a fresh Issued invoice for STU-101, Net 50.00 SGD, created by the seed script just before the case
```

**Test Steps:**
1. Confirm the payment.
2. Read the screen that opens.
3. Look at the leg, the transaction, the invoice and the operations alerts.

**Expected Result:**
> 1. The EA leg and the transaction are ReconciliationRequired.
>  2. The invoice stays PaymentPending and is not Paid.
>  3. SCR-06 shows the verifying state.
>  4. An operations alert is raised.
>  5. The system does not guess that the money was or was not debited, and it does not debit again.

---

#### `TC-076`: Function 1 treats the same FundingReference as one debit

- **Scenario ID**: `TS-012`
- **Test Suite**: F9.4 Pay with Education Account
- **Page / Target**: `Function 1 debit API`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: Tender R9; PB-10; FS F9: BR-F9-03; DA-12; NQ-15
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-03
- **Assumption Reference**: ASM-R9-15: Function 1 debits and reverses once per FundingReference. Function 9 may send the same FundingReference again after an error.
- **Note**: Các ID trong Traceability (BR-F9-03, DA-12, NQ-15) đều có trong FS 09. Lưu ý FS 09 mục 1.5 loại trừ phần triển khai API ghi nợ và hoàn của Function 1, NQ-15 chỉ giả định Function 1 có API idempotent theo FundingReference. Case này kiểm hành vi của Function 1 nên cần BA hoặc Dev xác nhận có thuộc phạm vi kiểm của F9 hay không.

**Preconditions:**
```text
1. A FundingReference FR-TEST-01 for STU-101 and 50.00 is prepared.
 2. STU-101 EA balance is 200.00.
```

**Test Data:**
```text
Student: STU-101
 FundingReference: FR-TEST-01
 Amount: 50.00
```

**Test Steps:**
1. Send the debit call for FR-TEST-01 to Function 1.
2. Send the same debit call again with the same FundingReference.
3. Read the ledger and the balance.

**Expected Result:**
> 1. The second call returns the result of the first call.
>  2. The ledger has one debit for FR-TEST-01.
>  3. The EA balance is 150.00.

---


### Test Suite: F9.4 and F9.5 Idempotency and concurrency

#### `TC-077`: Double click on Confirm creates one transaction and debits once

- **Scenario ID**: `TS-013`
- **Test Suite**: F9.4 and F9.5 Idempotency and concurrency
- **Page / Target**: `SCR-05 Review and confirm`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-10, PB-11; FS F9: AC-05; BR-F9-04; Step 6.2; SCR-05 Processing
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-03, ENV-R9-05
- **Assumption Reference**: N/A
- **Note**: xác nhận trace. UI mock: bấm đúp Authorize & Pay chỉ mở một phiên sandbox (một Ref FND). Chưa quan sát được trạng thái Processing và nút bị vô hiệu.

**Preconditions:**
```text
1. PAR-A is signed in and is on SCR-05 for a fresh 50.00 invoice of STU-101 with the EA method.
 2. STU-101 EA balance is 200.00.
```

**Test Data:**
```text
Student: STU-101 Ethan Tan, Singapore Citizen, EA Active, balance 200.00 SGD
 Invoice: a fresh Issued invoice for STU-101, Net 50.00 SGD, created by the seed script just before the case
```

**Test Steps:**
1. Double click the Confirm button quickly.
2. Look at the button right after the first click.
3. Look at the transactions of the invoice, the ledger and the balance.

**Expected Result:**
> 1. The Confirm button is disabled after the first click and the screen shows the Processing state.
>  2. Exactly one transaction exists for the invoice.
>  3. The ledger has one debit of 50.00 and the EA balance is 150.00.
>  4. The invoice is Paid.

---

#### `TC-078`: The same request sent again with the same key returns the first result

- **Scenario ID**: `TS-013`
- **Test Suite**: F9.4 and F9.5 Idempotency and concurrency
- **Page / Target**: `API: create payment`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `API`
- **Traceability**: Tender R9; PB-10, PB-11; FS F9: BR-F9-04; AC-05; Step 7 Retry
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-03, ENV-R9-05, ENV-R9-06
- **Assumption Reference**: ASM-R9-17: A repeat of the same key by the same Parent returns the result of the first transaction. No new transaction is created, no second debit is made and no error is shown.
- **Note**: xác nhận

**Preconditions:**
```text
1. PAR-A has a valid session.
 2. STU-101 EA balance is 200.00.
```

**Test Data:**
```text
Student: STU-101 Ethan Tan, Singapore Citizen, EA Active, balance 200.00 SGD
 Invoice: a fresh Issued invoice for STU-101, Net 50.00 SGD, created by the seed script just before the case
 Idempotency key: IDM-KEY-001
```

**Test Steps:**
1. Send the create payment request with the key IDM-KEY-001.
2. Send exactly the same request again with the same key.
3. Look at both answers, the transactions, the ledger and the balance.

**Expected Result:**
> 1. Both answers refer to the same transaction.
>  2. Only one transaction exists and the ledger has one debit of 50.00.
>  3. The second answer is not an error.
>  4. The balance is 150.00.

---

#### `TC-079`: The same key can be used by two different Parents

- **Scenario ID**: `TS-013`
- **Test Suite**: F9.4 and F9.5 Idempotency and concurrency
- **Page / Target**: `API: create payment`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `API`
- **Traceability**: Tender R9; PB-10, PB-11; FS F9: 4.2 Transaction IdempotencyKey (unique per InitiatedByUserId and key); SCR-05 Idempotency key
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-03, ENV-R9-05, ENV-R9-06
- **Assumption Reference**: N/A
- **Note**: xác nhận

**Preconditions:**
```text
1. PAR-A and PAR-D have valid sessions.
 2. Two fresh 50.00 invoices of STU-101 exist, invoice X and invoice Y.
 3. STU-101 EA balance is 200.00.
```

**Test Data:**
```text
Student: STU-101 Ethan Tan, Singapore Citizen, EA Active, balance 200.00 SGD
 Invoices: X and Y, 50.00 each
 Idempotency key: SHARED-KEY-001 for both
```

**Test Steps:**
1. As PAR-A pay invoice X with the key SHARED-KEY-001.
2. As PAR-D pay invoice Y with the key SHARED-KEY-001.
3. Look at the transactions.

**Expected Result:**
> 1. Both payments are accepted and two transactions exist.
>  2. Both invoices are Paid and the EA balance is 100.00.

---

#### `TC-080`: A key of 100 characters is accepted

- **Scenario ID**: `TS-013`
- **Test Suite**: F9.4 and F9.5 Idempotency and concurrency
- **Page / Target**: `API: create payment`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `API`
- **Traceability**: Tender R9; PB-10, PB-11; FS F9: 4.1 SCR-05 Idempotency key (up to 100 characters); 4.2 Transaction IdempotencyKey VARCHAR(100)
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-05, ENV-R9-06
- **Assumption Reference**: ASM-R9-18: A request with a missing, empty or 101 character key is rejected and creates no transaction. A 100 character key is accepted. The error text is not defined, so the cases check that nothing is created.
- **Note**: xác nhận

**Preconditions:**
```text
1. PAR-A has a valid session.
```

**Test Data:**
```text
Student: STU-101 Ethan Tan, Singapore Citizen, EA Active, balance 200.00 SGD
 Invoice: a fresh Issued invoice for STU-101, Net 50.00 SGD, created by the seed script just before the case
 Idempotency key: 100 characters
```

**Test Steps:**
1. Send the create payment request with a key of exactly 100 characters.

**Expected Result:**
> 1. The request is accepted and one transaction is created.

---

#### `TC-081`: A key that is missing, empty or 101 characters long is refused

- **Scenario ID**: `TS-013`
- **Test Suite**: F9.4 and F9.5 Idempotency and concurrency
- **Page / Target**: `API: create payment`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `API`
- **Traceability**: Tender R9; PB-10, PB-11; FS F9: 4.1 SCR-05 Idempotency key (required, up to 100 characters); BR-F9-04
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-05, ENV-R9-06
- **Assumption Reference**: ASM-R9-18: A request with a missing, empty or 101 character key is rejected and creates no transaction. A 100 character key is accepted. The error text is not defined, so the cases check that nothing is created.
- **Note**: xác nhận

**Preconditions:**
```text
1. PAR-A has a valid session.
```

**Test Data:**
```text
Student: STU-101 Ethan Tan, Singapore Citizen, EA Active, balance 200.00 SGD
 Invoice: a fresh Issued invoice for STU-101, Net 50.00 SGD, created by the seed script just before the case
 Keys tried: none, empty, 101 characters
```

**Test Steps:**
1. Send the create payment request with no key.
2. Send it with an empty key.
3. Send it with a key of 101 characters.
4. Look at the transactions and the balance.

**Expected Result:**
> 1. Each request is refused.
>  2. No transaction is created, no debit is made and the invoice is still Issued.

---

#### `TC-082`: Two requests at the same time for one invoice give one payment and one refusal

- **Scenario ID**: `TS-014`
- **Test Suite**: F9.4 and F9.5 Idempotency and concurrency
- **Page / Target**: `API: create payment`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `API`
- **Traceability**: Tender R9; PB-10, PB-11; FS F9: EX-03; AC-06; BR-F9-09; DA-13; 5.1 PAYMENT_PENDING
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-03, ENV-R9-05, ENV-R9-06
- **Assumption Reference**: N/A
- **Note**: xác nhận

**Preconditions:**
```text
1. PAR-A has a valid session.
 2. STU-101 EA balance is 200.00.
```

**Test Data:**
```text
Student: STU-101 Ethan Tan, Singapore Citizen, EA Active, balance 200.00 SGD
 Invoice: a fresh Issued invoice for STU-101, Net 50.00 SGD, created by the seed script just before the case
 Two requests with different keys: IDM-KEY-A and IDM-KEY-B, method EA
```

**Test Steps:**
1. Send both create payment requests at the same moment.
2. Look at both answers, the transactions, the ledger, the invoice and the balance.

**Expected Result:**
> 1. One request succeeds and creates one transaction.
>  2. The other request is refused with 409 and the message "A payment for this invoice is still being processed."
>  3. The ledger has one debit of 50.00, the balance is 150.00 and it is never negative.
>  4. The invoice is Paid once. No money is taken without the invoice being updated.

---

#### `TC-083`: Two guardians confirming the same invoice at the same time give one payment

- **Scenario ID**: `TS-014`
- **Test Suite**: F9.4 and F9.5 Idempotency and concurrency
- **Page / Target**: `SCR-05 Review and confirm`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-10, PB-11; FS F9: EX-03; AC-06; DA-04; BR-F9-04; BR-F9-09
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-03, ENV-R9-05
- **Assumption Reference**: N/A
- **Note**: xác nhận

**Preconditions:**
```text
1. PAR-A and PAR-D are signed in in two browsers, both on SCR-05 for the same fresh 50.00 invoice of STU-101 with the EA method.
 2. STU-101 EA balance is 200.00.
```

**Test Data:**
```text
Student: STU-101 Ethan Tan, Singapore Citizen, EA Active, balance 200.00 SGD
 Invoice: a fresh Issued invoice for STU-101, Net 50.00 SGD, created by the seed script just before the case
```

**Test Steps:**
1. Confirm in both browsers at the same moment.
2. Look at both screens, the transactions, the ledger and the balance.

**Expected Result:**
> 1. One Parent sees the success screen SCR-07.
>  2. The other Parent is refused with PAYMENT_PENDING or INVOICE_ALREADY_PAID and is sent to SCR-06 or the refreshed list.
>  3. One transaction exists, the ledger has one debit and the balance is 150.00.

---

#### `TC-084`: Confirming an invoice that was paid meanwhile is refused

- **Scenario ID**: `TS-014`
- **Test Suite**: F9.4 and F9.5 Idempotency and concurrency
- **Page / Target**: `SCR-05 Review and confirm`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-10, PB-11; FS F9: EX-04; BR-F9-04; DA-13; 5.1 INVOICE_ALREADY_PAID
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-03, ENV-R9-05
- **Assumption Reference**: N/A
- **Note**: xác nhận

**Preconditions:**
```text
1. PAR-A is signed in and is on SCR-05 for a fresh 50.00 invoice of STU-101.
 2. PAR-D has paid the same invoice with the EA after PAR-A opened SCR-05.
```

**Test Data:**
```text
Student: STU-101 Ethan Tan, Singapore Citizen, EA Active, balance 200.00 SGD
 Invoice: a fresh Issued invoice for STU-101, Net 50.00 SGD, created by the seed script just before the case
```

**Test Steps:**
1. Confirm the payment as PAR-A.
2. Look at the screen, the transactions and the balance.

**Expected Result:**
> 1. The message "This invoice has already been paid." is shown and the list is refreshed.
>  2. No second transaction is created and no second debit is made. The balance is 150.00.

---

#### `TC-085`: Confirming an invoice that is waiting for another payment is refused

- **Scenario ID**: `TS-014`
- **Test Suite**: F9.4 and F9.5 Idempotency and concurrency
- **Page / Target**: `SCR-06 Pending`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-10, PB-11; FS F9: EX-04; BR-F9-09; AC-11; 5.1 PAYMENT_PENDING
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-02, ENV-R9-05
- **Assumption Reference**: N/A
- **Note**: xác nhận. UI mock: màn Payment In Progress hiện đúng câu 'A payment for this invoice is still being processed.' kèm Transaction Ref, Invoice và Amount.

**Preconditions:**
```text
1. PAR-A is signed in and is on SCR-05 for a fresh 50.00 invoice of STU-101.
 2. PAR-D has started an online payment for the same invoice and it is PaymentPending.
```

**Test Data:**
```text
Student: STU-101 Ethan Tan, Singapore Citizen, EA Active, balance 200.00 SGD
 Invoice: a fresh Issued invoice for STU-101, Net 50.00 SGD, created by the seed script just before the case
```

**Test Steps:**
1. Confirm the payment as PAR-A with the EA method.
2. Look at the screen, the transactions and the balance.

**Expected Result:**
> 1. The message "A payment for this invoice is still being processed." is shown and the Parent moves to SCR-06.
>  2. No new transaction is created and the EA balance is still 200.00.
>  3. The invoice is still PaymentPending.

---

#### `TC-086`: Confirming an invoice that was cancelled meanwhile is refused

- **Scenario ID**: `TS-014`
- **Test Suite**: F9.4 and F9.5 Idempotency and concurrency
- **Page / Target**: `SCR-05 Review and confirm`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-10, PB-11; FS F9: AC-21; EX-14; EX-04; 5.1 INVOICE_NOT_PAYABLE
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-05
- **Assumption Reference**: N/A
- **Note**: xác nhận trace. UI mock không có cách hủy invoice khi Parent đang xem.

**Preconditions:**
```text
1. PAR-A is signed in and is on SCR-05 for a fresh 50.00 invoice of STU-101 with the EA method.
 2. The invoice is set to Cancelled after SCR-05 opened.
```

**Test Data:**
```text
Student: STU-101 Ethan Tan, Singapore Citizen, EA Active, balance 200.00 SGD
 Invoice: a fresh Issued invoice for STU-101, Net 50.00 SGD, created by the seed script just before the case
```

**Test Steps:**
1. Cancel the invoice in the data.
2. Confirm the payment.
3. Look at the screen, the transactions and the balance.

**Expected Result:**
> 1. The message "This invoice can no longer be paid." is shown and the list is refreshed.
>  2. No transaction is created and the EA balance is still 200.00.
>  3. The invoice stays Cancelled.

**Actual Result:**
> Chạy trên bản Dev local function9_14-10-26, Chrome, 2026-10-15; dữ liệu mẫu khác R9 nên không xét. Chưa chạy đúng tình huống invoice bị hủy. Tình huống gần nhất là khoản phí đã bị trả ở tab khác: Authorize ở màn cũ hiện cảnh báo The selected fees are no longer available (không phải câu This invoice can no longer be paid), lựa chọn bị xóa, danh sách tải lại, DB vẫn 1 invoice 1 item, không có transaction thứ hai.

---


### Test Suite: F9.5 Pay online

#### `TC-087`: Review screen for an online payment has no EA part

- **Scenario ID**: `TS-015`
- **Test Suite**: F9.5 Pay online
- **Page / Target**: `SCR-05 Review and confirm`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-11; FS F9: Step 6.1; 4.1 SCR-05; SCR-05
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01
- **Assumption Reference**: N/A
- **Note**: xác nhận. UI mock online only: bước review chỉ có dòng Online Gateway (54.00), không có dòng EA và không có số dư sau thanh toán.

**Preconditions:**
```text
1. PAR-A is signed in and is on SCR-04 for a fresh 75.00 invoice of STU-102.
```

**Test Data:**
```text
Student: STU-102 Chloe Tan, Permanent Resident, no Education Account
 Invoice: a fresh Issued invoice for STU-102, Net 75.00 SGD, created by the seed script just before the case
 Method: online
```

**Test Steps:**
1. Choose online payment and continue.
2. Read SCR-05.

**Expected Result:**
> 1. SCR-05 shows the child STU-102 Chloe Tan, the invoice number, the amount to pay 75.00 SGD and the method online.
>  2. No EA amount and no EA balance after payment are shown.

**Actual Result:**
> Chạy trên bản Dev local function9_14-10-26, Chrome, 2026-10-15; dữ liệu mẫu khác R9 nên không xét. Review online hiện Payment method Online Gateway, Education Account SGD 0.00, Online Gateway SGD 120.00, và số dư EA hiện tại 250 bên cạnh. Khác Expected 2 ở chỗ vẫn có dòng EA 0.00 và số dư EA, nhưng học sinh demo có EA nên chưa kết luận.

---

#### `TC-088`: A student without an EA pays online and the invoice becomes Paid

- **Scenario ID**: `TS-015`
- **Test Suite**: F9.5 Pay online
- **Page / Target**: `SCR-07 Payment confirmation`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-11; FS F9: AC-08; AC-14; BR-F9-07; DA-01; Step 6.3 online; Step 7.3; BR-F9-13
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-02, ENV-R9-05
- **Assumption Reference**: N/A
- **Note**: xác nhận trace. Chưa chạy Pay Successfully cho thanh toán online only trên UI mock; luồng sandbox thành công đã thấy ở split (ra biên lai).

**Preconditions:**
```text
1. PAR-A is signed in and is on SCR-05 for a fresh 75.00 invoice of STU-102 with the online method.
 2. The sandbox provider is ready and can send a valid webhook.
```

**Test Data:**
```text
Student: STU-102 Chloe Tan, Permanent Resident, no Education Account
 Invoice: a fresh Issued invoice for STU-102, Net 75.00 SGD, created by the seed script just before the case
 Method: online
```

**Test Steps:**
1. Confirm the payment.
2. Look at the transaction, the online leg and the invoice before paying.
3. On the provider page choose a payment method and finish with the success outcome.
4. Wait for the webhook and return to the portal.
5. Read SCR-07 and the data.

**Expected Result:**
> 1. After the confirm, the transaction is Pending, the online leg is Pending and the invoice is PaymentPending. The Parent is sent to the provider page for 75.00 SGD.
>  2. A valid webhook is recorded. The online leg is Succeeded with the ProviderTransactionId, the transaction is Succeeded and the invoice is Paid.
>  3. SCR-07 shows success, a transaction reference, the time, the online part 75.00 and the total 75.00.
>  4. Requested and Settled amounts are 75.00. No EA is used and the student has no EA.

**Actual Result:**
> Chạy trên bản Dev local function9_14-10-26, Chrome, 2026-10-15; dữ liệu mẫu khác R9 nên không xét. Sau khi Authorize: invoice PaymentPending, transaction Pending, lượt online Pending, trang tự chuyển sang simulator với số tiền 120. Pay successful: webhook payment.succeeded được ghi và Processed, lượt online Succeeded có ProviderTransactionId, transaction Succeeded, invoice Paid. Trang kết quả hiện Payment successful, Transaction ID, thời gian, Online Gateway Succeeded requested 120 settled 120. Không dùng EA.

---

#### `TC-089`: A student with an EA who pays online keeps the EA balance

- **Scenario ID**: `TS-015`
- **Test Suite**: F9.5 Pay online
- **Page / Target**: `SCR-07 Payment confirmation`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-11; FS F9: BR-F9-10; DA-08; AC-08; DA-02
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-02, ENV-R9-03, ENV-R9-05
- **Assumption Reference**: N/A
- **Note**: xác nhận trace. Chưa chạy online only thành công trên UI mock; online only thất bại không làm đổi số dư EA.

**Preconditions:**
```text
1. PAR-A is signed in and is on SCR-05 for a fresh 50.00 invoice of STU-101 with the online method.
 2. STU-101 EA balance is 200.00.
```

**Test Data:**
```text
Student: STU-101 Ethan Tan, Singapore Citizen, EA Active, balance 200.00 SGD
 Invoice: a fresh Issued invoice for STU-101, Net 50.00 SGD, created by the seed script just before the case
 Method: online
```

**Test Steps:**
1. Confirm the payment and finish with the success outcome at the provider.
2. Read the EA balance and the ledger.

**Expected Result:**
> 1. The invoice is Paid by the online leg only.
>  2. The EA balance is still 200.00 and the ledger has no entry for the payment.

**Actual Result:**
> Chạy trên bản Dev local function9_14-10-26, Chrome, 2026-10-15; dữ liệu mẫu khác R9 nên không xét. Online only cho học sinh có EA: lượt funding chỉ có Online, không có EducationAccountTransactionId, invoice Paid. Số dư EA trên UI luôn 250 (gắn cứng) và sổ cái không xem được nên chưa xác nhận Expected 2.

---

#### `TC-090`: Provider failure returns the invoice to Issued and nothing is charged

- **Scenario ID**: `TS-016`
- **Test Suite**: F9.5 Pay online
- **Page / Target**: `SCR-08 Payment failed`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-11; FS F9: AC-09; BR-F9-05; Step 7.5; 5.1 PAYMENT_FAILED; SCR-08
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-02, ENV-R9-05
- **Assumption Reference**: N/A
- **Note**: xác nhận. UI mock Payment Fails với online only: 'Your payment could not be completed. No amount was deducted.', Transaction Reference, Try Again và Exit to Fees.

**Preconditions:**
```text
1. PAR-A is signed in and is on SCR-05 for a fresh 75.00 invoice of STU-102 with the online method.
```

**Test Data:**
```text
Student: STU-102 Chloe Tan, Permanent Resident, no Education Account
 Invoice: a fresh Issued invoice for STU-102, Net 75.00 SGD, created by the seed script just before the case
```

**Test Steps:**
1. Confirm the payment.
2. At the provider choose the failure outcome.
3. Return to the portal.
4. Look at SCR-08, the leg, the transaction and the invoice.

**Expected Result:**
> 1. The online leg is Failed, the transaction is Failed and the invoice is Issued.
>  2. SCR-08 shows "Your payment could not be completed. No amount was deducted." with the buttons Try again and Exit.
>  3. No amount is collected.

**Actual Result:**
> Chạy trên bản Dev local function9_14-10-26, Chrome, 2026-10-15; dữ liệu mẫu khác R9 nên không xét. Online thất bại (Pay failed): lượt online Failed, transaction Failed, nhưng invoice vẫn PaymentPending, không về Issued. Màn kết quả hiện Payment failed, Your payment could not be completed. Return to Fees & Payments to review the latest outstanding fees; không có câu No amount was deducted, không có nút Try again và Exit (chỉ có Back to home). Khoản phí biến khỏi danh sách phí chưa thanh toán nên không thanh toán lại được. Chưa tạo Defect.

---

#### `TC-091`: Cancel on the provider page returns the invoice to Issued

- **Scenario ID**: `TS-016`
- **Test Suite**: F9.5 Pay online
- **Page / Target**: `SCR-08 Payment failed`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-11; FS F9: AC-09; Step 7.5; Appendix A; 5.1 PAYMENT_CANCELLED; SCR-08
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-02, ENV-R9-05
- **Assumption Reference**: N/A
- **Note**: xác nhận trace. UI mock: Cancel Payment trên sandbox với online only hiện câu của PAYMENT_FAILED ('Your payment could not be completed. No amount was deducted.') thay vì câu PAYMENT_CANCELLED ('The payment was cancelled. No amount was deducted.') theo FS 5.1.

**Preconditions:**
```text
1. PAR-A is signed in and is on SCR-05 for a fresh 75.00 invoice of STU-102 with the online method.
```

**Test Data:**
```text
Student: STU-102 Chloe Tan, Permanent Resident, no Education Account
 Invoice: a fresh Issued invoice for STU-102, Net 75.00 SGD, created by the seed script just before the case
```

**Test Steps:**
1. Confirm the payment.
2. On the provider page cancel the payment.
3. Return to the portal.
4. Look at SCR-08, the leg, the transaction and the invoice.

**Expected Result:**
> 1. The online leg is Cancelled, the transaction is Cancelled and the invoice is Issued.
>  2. SCR-08 shows "The payment was cancelled. No amount was deducted."
>  3. No amount is collected.

---

#### `TC-092`: An expired provider payment session fails the online leg

- **Scenario ID**: `TS-016`
- **Test Suite**: F9.5 Pay online
- **Page / Target**: `SCR-08 Payment failed`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-11; FS F9: EX-02; Appendix A; Step 7.5
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-02, ENV-R9-05
- **Assumption Reference**: ASM-R9-06: The provider payment session expires after 10 minutes, or after the value Dev gives, or when the sandbox expires it on demand.
- **Note**: xác nhận trace (EX-02, ASM-R9-06). Sandbox của mock không có nút làm hết hạn phiên.

**Preconditions:**
```text
1. PAR-A is signed in and is on SCR-05 for a fresh 75.00 invoice of STU-102 with the online method.
```

**Test Data:**
```text
Student: STU-102 Chloe Tan, Permanent Resident, no Education Account
 Invoice: a fresh Issued invoice for STU-102, Net 75.00 SGD, created by the seed script just before the case
```

**Test Steps:**
1. Confirm the payment.
2. Stay on the provider page without paying until the payment session expires.
3. Return to the portal.
4. Look at the leg, the transaction, the invoice and SCR-08.

**Expected Result:**
> 1. The online leg is Failed and the transaction is Failed.
>  2. The invoice is Issued and nothing is collected.
>  3. SCR-08 shows "Your payment could not be completed. No amount was deducted."

---

#### `TC-093`: A provider that refuses to open the payment session fails the payment

- **Scenario ID**: `TS-016`
- **Test Suite**: F9.5 Pay online
- **Page / Target**: `SCR-08 Payment failed`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-11; FS F9: Step 6.3 online; BR-F9-05; EX-08
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-02, ENV-R9-05
- **Assumption Reference**: ASM-R9-25: The online leg is Failed, any EA part is reversed first, the invoice returns to Issued and the Parent sees PAYMENT_FAILED (PAYMENT_FAILED_EA_RETURNED when an EA part was reversed).
- **Note**: xác nhận trace. Sandbox của mock không có tình huống provider từ chối mở phiên.

**Preconditions:**
```text
1. PAR-A is signed in and is on SCR-05 for a fresh 75.00 invoice of STU-102 with the online method.
 2. The sandbox is set to refuse the creation of the payment session.
```

**Test Data:**
```text
Student: STU-102 Chloe Tan, Permanent Resident, no Education Account
 Invoice: a fresh Issued invoice for STU-102, Net 75.00 SGD, created by the seed script just before the case
```

**Test Steps:**
1. Confirm the payment.
2. Look at the screen, the leg, the transaction and the invoice.

**Expected Result:**
> 1. The online leg is Failed, the transaction is Failed and the invoice is Issued.
>  2. The Parent sees "Your payment could not be completed. No amount was deducted." and can try again.
>  3. Nothing is collected.

---

#### `TC-094`: Closing the browser on the provider page keeps the payment Pending until the result arrives

- **Scenario ID**: `TS-016`
- **Test Suite**: F9.5 Pay online
- **Page / Target**: `SCR-06 Pending`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-11; FS F9: EX-09; AC-11; BR-F9-09; Step 7.2
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-02, ENV-R9-04, ENV-R9-05
- **Assumption Reference**: N/A
- **Note**: xác nhận. UI mock Close Browser: hiện màn Payment In Progress, invoice sang AWAITING PAYMENT và không thanh toán thêm được. Lưu ý: bấm Refresh Status trên màn này đưa về trang chủ chưa đăng nhập (lặp lại 2 lần), và sau một lần đăng nhập lại invoice thanh toán lại được, không còn trạng thái chờ, trong khi EX-09 và AC-11 yêu cầu Parent thấy trạng thái khi vào lại.

**Preconditions:**
```text
1. PAR-A is signed in and is on SCR-05 for a fresh 75.00 invoice of STU-102 with the online method.
```

**Test Data:**
```text
Student: STU-102 Chloe Tan, Permanent Resident, no Education Account
 Invoice: a fresh Issued invoice for STU-102, Net 75.00 SGD, created by the seed script just before the case
```

**Test Steps:**
1. Confirm the payment.
2. On the provider page close the browser without paying.
3. Sign in again as PAR-A and open SCR-02 of STU-102.
4. Let the provider send the success result and look again.

**Expected Result:**
> 1. Before the result arrives the transaction stays Pending, the invoice is PaymentPending and the Parent sees the waiting state SCR-06.
>  2. No second payment can be started.
>  3. After the valid success webhook the invoice is Paid.

---

#### `TC-095`: A provider timeout keeps the leg Pending and does not mark it Failed

- **Scenario ID**: `TS-016`
- **Test Suite**: F9.5 Pay online
- **Page / Target**: `SCR-06 Pending`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-11; FS F9: EX-08; Step 7.1
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-02, ENV-R9-05
- **Assumption Reference**: N/A
- **Note**: xác nhận trace. Sandbox của mock không có tình huống provider timeout.

**Preconditions:**
```text
1. PAR-A has started an online payment for a fresh 75.00 invoice of STU-102 and the leg is Pending.
 2. The sandbox is set to time out on every status question.
```

**Test Data:**
```text
Student: STU-102 Chloe Tan, Permanent Resident, no Education Account
 Invoice: a fresh Issued invoice for STU-102, Net 75.00 SGD, created by the seed script just before the case
```

**Test Steps:**
1. Run the reconciliation job once while the provider times out.
2. Look at the leg, the transaction and the invoice.

**Expected Result:**
> 1. The online leg stays Pending and the transaction stays Pending.
>  2. The invoice stays PaymentPending.
>  3. Nothing is marked Failed.

---

#### `TC-096`: No card data is stored after an online payment

- **Scenario ID**: `TS-016`
- **Test Suite**: F9.5 Pay online
- **Page / Target**: `Database and logs`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Security`
- **Traceability**: Tender R9; PB-11; FS F9: DA-01; BR-F9-06; 4.2 WebhookReceipt PayloadHash
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-02, ENV-R9-05
- **Assumption Reference**: N/A
- **Note**: xác nhận

**Preconditions:**
```text
1. An online payment of a fresh 75.00 invoice of STU-102 has finished with the success outcome.
```

**Test Data:**
```text
Student: STU-102 Chloe Tan, Permanent Resident, no Education Account
 Sandbox test card or account used on the provider page
```

**Test Steps:**
1. Search the payment tables for the test card number or account number.
2. Search the application and webhook logs for the same value.

**Expected Result:**
> 1. No card number or account number is stored in the payment tables.
>  2. No card number or account number is in the logs.
>  3. Only the provider references and the hash of the callback are stored.

---


### Test Suite: F9.4 and F9.5 Split payment

#### `TC-097`: Split of EA 20.00 and online 30.00 pays a 50.00 invoice

- **Scenario ID**: `TS-017`
- **Test Suite**: F9.4 and F9.5 Split payment
- **Page / Target**: `SCR-07 Payment confirmation`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-10, PB-11; FS F9: AC-15; AC-22; BR-F9-11; BR-F9-13; DA-12; Step 7.3; SCR-07
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-02, ENV-R9-03, ENV-R9-05
- **Assumption Reference**: N/A
- **Note**: xác nhận. UI mock split 20.00 và 30.00: biên lai hai dòng Education Account 20.00 và Online Payment 30.00 mỗi dòng một Ref dạng FND khác nhau, Total Settled 50.00, số dư EA 0.00, invoice sang RECENT PAYMENTS.

**Preconditions:**
```text
1. PAR-A is signed in and is on SCR-05 for INV-3001 (50.00) of STU-103 with the split option and the default parts EA 20.00 and online 30.00.
 2. STU-103 EA balance is 20.00.
```

**Test Data:**
```text
Student: STU-103 Marcus Tan, Singapore Citizen, EA Active, balance 20.00 SGD
 Invoice: INV-3001 (50.00)
 Method: SPLIT, EA 20.00, online 30.00
```

**Test Steps:**
1. Confirm the payment.
2. On the provider page finish with the success outcome.
3. Wait for the valid webhook and return to the portal.
4. Read SCR-07, the legs, the transaction, the invoice, the ledger and the balance.

**Expected Result:**
> 1. The EA balance falls by 20.00 to 0.00 and the EA leg is Succeeded.
>  2. The online leg of 30.00 is Succeeded after a valid webhook.
>  3. The transaction is Succeeded and the invoice is Paid.
>  4. SCR-07 shows two parts, EA 20.00 and online 30.00, and the total 50.00.
>  5. The two legs have different FundingReferences and their amounts add up to 50.00.

**Actual Result:**
> Chạy trên bản Dev local function9_14-10-26, Chrome, 2026-10-15; dữ liệu mẫu khác R9 nên không xét. Chia EA 250 và Online 100: lượt EA Succeeded có EducationAccountTransactionId, lượt online Succeeded sau webhook Processed, transaction Succeeded, invoice Paid, trang kết quả hiện hai phần (EA 250, Online 100) và tổng 350, hai FundingReference khác nhau. Chưa kiểm Expected 1 (số dư EA giảm) vì số dư trên UI gắn cứng 250.

---

#### `TC-098`: The EA is debited before the online payment session is created

- **Scenario ID**: `TS-017`
- **Test Suite**: F9.4 and F9.5 Split payment
- **Page / Target**: `Function 1 and provider calls`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: Tender R9; PB-10, PB-11; FS F9: BR-F9-11; Step 6.3 split; DA-14; Appendix A
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-02, ENV-R9-03, ENV-R9-05
- **Assumption Reference**: N/A
- **Note**: xác nhận

**Preconditions:**
```text
1. A split payment of EA 20.00 and online 30.00 is confirmed for a fresh 50.00 invoice of STU-103.
```

**Test Data:**
```text
Student: STU-103 Marcus Tan, Singapore Citizen, EA Active, balance 20.00 SGD
 Invoice: a fresh Issued invoice for STU-103, Net 50.00 SGD (same as INV-3001), created by the seed script just before the case
```

**Test Steps:**
1. Confirm the payment.
2. Read the time of the EA debit call, of the EA leg result and of the creation of the payment session.

**Expected Result:**
> 1. The EA debit is called first and the EA leg is Succeeded.
>  2. The payment session at the provider is created only after the EA leg is Succeeded.
>  3. The online leg is created Pending after the EA result.

**Actual Result:**
> Chạy trên bản Dev local function9_14-10-26, Chrome, 2026-10-15; dữ liệu mẫu khác R9 nên không xét. Phản hồi checkout trả lượt EA Succeeded cùng lượt online Pending và checkoutUrl, nên EA được xử lý trước khi có phiên thanh toán online. Thứ tự gọi nhà cung cấp không xem được qua UI hay DB nên chưa xác nhận Expected 2.

---

#### `TC-099`: Split with a lowered EA part of 10.00 and an online part of 40.00 pays the invoice

- **Scenario ID**: `TS-017`
- **Test Suite**: F9.4 and F9.5 Split payment
- **Page / Target**: `SCR-07 Payment confirmation`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-10, PB-11; FS F9: AC-22; DA-08; BR-F9-11
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-02, ENV-R9-03, ENV-R9-05
- **Assumption Reference**: ASM-R9-01: The EA part starts at the whole available balance. The Parent can lower it to any amount above 0 and below the payable amount, and the online part is then Net minus the EA part. AC-22 is followed because it gives a worked example.
- **Note**: xác nhận trace. UI mock: nhập EA 10 cho phần Online 40.00; chưa chạy thanh toán xong với giá trị này (đã chạy với 20 và 30).

**Preconditions:**
```text
1. PAR-A is signed in and is on SCR-04 for a fresh 50.00 invoice of STU-103.
 2. STU-103 EA balance is 20.00.
```

**Test Data:**
```text
Student: STU-103 Marcus Tan, Singapore Citizen, EA Active, balance 20.00 SGD
 Invoice: a fresh Issued invoice for STU-103, Net 50.00 SGD (same as INV-3001), created by the seed script just before the case
 Method: SPLIT, EA 10.00, online 40.00
```

**Test Steps:**
1. Choose the split option and change the EA part to 10.00.
2. Continue and confirm.
3. Finish with the success outcome at the provider.
4. Read SCR-07 and the EA balance.

**Expected Result:**
> 1. The EA is debited 10.00 and the balance is 10.00.
>  2. The online part is 40.00 and is Succeeded.
>  3. The invoice is Paid and SCR-07 shows EA 10.00 and online 40.00.

---

#### `TC-100`: Review screen for a split shows both parts and the balance after payment

- **Scenario ID**: `TS-017`
- **Test Suite**: F9.4 and F9.5 Split payment
- **Page / Target**: `SCR-05 Review and confirm`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-10, PB-11; FS F9: Step 6.1; 4.1 SCR-05; AC-22
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01
- **Assumption Reference**: N/A
- **Note**: xác nhận. UI mock review split: EA 20.00, Online 30.00, 'Estimated balance after: SGD 0.00 (reference only)'.

**Preconditions:**
```text
1. PAR-A is signed in and is on SCR-04 for INV-3001 of STU-103 with the split option and the default parts.
```

**Test Data:**
```text
Student: STU-103 Marcus Tan, Singapore Citizen, EA Active, balance 20.00 SGD
 Invoice: INV-3001 (50.00)
```

**Test Steps:**
1. Continue to SCR-05.
2. Read SCR-05.

**Expected Result:**
> 1. SCR-05 shows the amount to pay 50.00 and the two parts EA 20.00 and online 30.00.
>  2. It shows the EA balance after payment 0.00 as information only.

**Actual Result:**
> Chạy trên bản Dev local function9_14-10-26, Chrome, 2026-10-15; dữ liệu mẫu khác R9 nên không xét. Review của split hiện Payment method Both, Education Account SGD 250.00, Online Gateway SGD 100.00, tổng 350. Không có dòng số dư EA sau thanh toán (chỉ có số dư hiện tại 250), nên không đạt Expected 2. Chưa tạo Defect.

---

#### `TC-101`: While the online part is pending the waiting screen says the EA part is already taken

- **Scenario ID**: `TS-017`
- **Test Suite**: F9.4 and F9.5 Split payment
- **Page / Target**: `SCR-06 Pending`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-10, PB-11; FS F9: Appendix C SCR-06; EX-09; AC-11; Step 7.2
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-02, ENV-R9-05
- **Assumption Reference**: N/A
- **Note**: xác nhận trace (Appendix C SCR-06: với chia đôi nêu rõ phần EA đã được trừ). UI mock Close Browser với split: màn Payment In Progress chỉ có Transaction Ref, Invoice và Amount 50.00, không nói phần EA 20.00 đã bị trừ. Chưa đạt Expected 2.

**Preconditions:**
```text
1. A split payment of EA 20.00 and online 30.00 is confirmed for a fresh 50.00 invoice of STU-103.
 2. The EA leg is Succeeded and the online leg is Pending at the provider.
```

**Test Data:**
```text
Student: STU-103 Marcus Tan, Singapore Citizen, EA Active, balance 20.00 SGD
 Invoice: a fresh Issued invoice for STU-103, Net 50.00 SGD (same as INV-3001), created by the seed script just before the case
```

**Test Steps:**
1. Close the browser on the provider page.
2. Sign in again as PAR-A and open the invoice.
3. Read SCR-06.

**Expected Result:**
> 1. SCR-06 shows the waiting state with a temporary reference.
>  2. It states that the EA part 20.00 has already been taken.
>  3. The Parent cannot start another payment for the invoice.

---

#### `TC-102`: EA debit fails before the online part: no payment session and no online charge

- **Scenario ID**: `TS-018`
- **Test Suite**: F9.4 and F9.5 Split payment
- **Page / Target**: `SCR-04 Choose payment method`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-10, PB-11; FS F9: AC-16; EX-05; Step 6.3 split; 5.1 EA_INSUFFICIENT_BALANCE
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-02, ENV-R9-03, ENV-R9-05
- **Assumption Reference**: N/A
- **Note**: xác nhận trace. UI mock không có cách đổi số dư giữa lúc xem và lúc xác nhận.

**Preconditions:**
```text
1. PAR-A is signed in and is on SCR-05 for INV-3001 of STU-103 with the split option (EA 20.00, online 30.00).
 2. STU-103 EA balance is 20.00 when SCR-05 opens.
```

**Test Data:**
```text
Student: STU-103 Marcus Tan, Singapore Citizen, EA Active, balance 20.00 SGD
 Invoice: INV-3001 (50.00)
 Balance changed to 10.00 before the confirm
```

**Test Steps:**
1. Without leaving SCR-05 set the EA balance of STU-103 to 10.00 in Function 1.
2. Confirm the payment.
3. Look at the legs, the transaction, the invoice, the provider calls and the screen.

**Expected Result:**
> 1. The EA leg is Failed and the transaction is Failed.
>  2. No payment session is created at the provider and nothing is collected online.
>  3. The invoice is Issued and the EA balance is 10.00.
>  4. The Parent sees "Your Education Account balance is not enough for this amount. You can pay the rest online." and goes back to the choice of method.

---

#### `TC-103`: Online failure after the EA debit returns the EA part

- **Scenario ID**: `TS-018`
- **Test Suite**: F9.4 and F9.5 Split payment
- **Page / Target**: `SCR-08 Payment failed`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-10, PB-11; FS F9: AC-17; BR-F9-05; BR-F9-11; Step 7.4; Appendix A; 5.1 PAYMENT_FAILED_EA_RETURNED
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-02, ENV-R9-03, ENV-R9-05
- **Assumption Reference**: N/A
- **Note**: xác nhận. UI mock split rồi Payment Fails: đúng câu 'Your online payment could not be completed. The amount taken from the Education Account has been returned.', có Try Again và Exit to Fees; sau khi thoát số dư EA về lại 20.00 và invoice trả lại được. Reversal ID trong DB không xem được.

**Preconditions:**
```text
1. A split payment of EA 20.00 and online 30.00 is confirmed for INV-3001 of STU-103.
 2. The EA leg is Succeeded and the EA balance is 0.00.
```

**Test Data:**
```text
Student: STU-103 Marcus Tan, Singapore Citizen, EA Active, balance 20.00 SGD
 Invoice: INV-3001 (50.00)
```

**Test Steps:**
1. At the provider choose the failure outcome.
2. Return to the portal.
3. Look at SCR-08, the legs, the transaction, the invoice, the ledger and the balance.

**Expected Result:**
> 1. The online leg is Failed. The EA leg is Reversed and the reversal ID is stored.
>  2. The transaction is Failed and the invoice is Issued.
>  3. The ledger shows the debit of 20.00 and the reversal of 20.00. The EA balance is 20.00 again.
>  4. SCR-08 shows "Your online payment could not be completed. The amount taken from the Education Account has been returned." with the buttons Try again and Exit.

**Actual Result:**
> Chạy trên bản Dev local function9_14-10-26, Chrome, 2026-10-15; dữ liệu mẫu khác R9 nên không xét. Online thất bại sau khi EA đã trừ (EA 250 Succeeded, online 100 Failed): không có trạng thái Reversed, EducationAccountReversalTransactionId là NULL nên EA không được hoàn, transaction là ReconciliationRequired (không phải Failed), invoice còn PaymentPending (không về Issued). Màn hiện Payment needs review và Your Education Account may still have been deducted, không có câu The amount taken from the Education Account has been returned, không có Try again và Exit. Chưa tạo Defect.

---

#### `TC-104`: Cancel at the provider after the EA debit returns the EA part

- **Scenario ID**: `TS-018`
- **Test Suite**: F9.4 and F9.5 Split payment
- **Page / Target**: `SCR-08 Payment failed`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-10, PB-11; FS F9: AC-17; Appendix A; 5.1 PAYMENT_CANCELLED note; Step 7.4
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-02, ENV-R9-03, ENV-R9-05
- **Assumption Reference**: ASM-R9-14: When the Parent cancels at the provider, the transaction and the online leg are Cancelled. When the online part fails or expires, the transaction is Failed. In both cases the EA leg is Reversed, the invoice returns to Issued and the Parent sees PAYMENT_FAILED_EA_RETURNED.
- **Note**: xác nhận. UI mock split rồi Cancel Payment: hiện câu PAYMENT_FAILED_EA_RETURNED như ASM-R9-14 và ghi chú PAYMENT_CANCELLED trong FS 5.1.

**Preconditions:**
```text
1. A split payment of EA 20.00 and online 30.00 is confirmed for INV-3001 of STU-103.
 2. The EA leg is Succeeded.
```

**Test Data:**
```text
Student: STU-103 Marcus Tan, Singapore Citizen, EA Active, balance 20.00 SGD
 Invoice: INV-3001 (50.00)
```

**Test Steps:**
1. On the provider page cancel the payment.
2. Return to the portal.
3. Look at SCR-08, the legs, the transaction, the invoice, the ledger and the balance.

**Expected Result:**
> 1. The online leg is Cancelled and the EA leg is Reversed.
>  2. The transaction is Cancelled and the invoice is Issued.
>  3. The EA balance is 20.00 again.
>  4. SCR-08 shows "Your online payment could not be completed. The amount taken from the Education Account has been returned.", the message for a split where the EA was taken.

---

#### `TC-105`: An expired provider session after the EA debit returns the EA part

- **Scenario ID**: `TS-018`
- **Test Suite**: F9.4 and F9.5 Split payment
- **Page / Target**: `SCR-08 Payment failed`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-10, PB-11; FS F9: EX-02; AC-17; Step 7.4
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-02, ENV-R9-03, ENV-R9-05
- **Assumption Reference**: ASM-R9-06: The provider payment session expires after 10 minutes, or after the value Dev gives, or when the sandbox expires it on demand.
- **Note**: xác nhận trace. Sandbox của mock không có nút làm hết hạn phiên.

**Preconditions:**
```text
1. A split payment of EA 20.00 and online 30.00 is confirmed for INV-3001 of STU-103.
 2. The EA leg is Succeeded.
```

**Test Data:**
```text
Student: STU-103 Marcus Tan, Singapore Citizen, EA Active, balance 20.00 SGD
 Invoice: INV-3001 (50.00)
```

**Test Steps:**
1. Stay on the provider page without paying until the payment session expires.
2. Return to the portal.
3. Look at SCR-08, the legs, the transaction, the invoice and the balance.

**Expected Result:**
> 1. The online leg is Failed and the EA leg is Reversed.
>  2. The transaction is Failed and the invoice is Issued.
>  3. The EA balance is 20.00 again and SCR-08 shows "Your online payment could not be completed. The amount taken from the Education Account has been returned."

---

#### `TC-106`: A provider that refuses the payment session after the EA debit returns the EA part

- **Scenario ID**: `TS-018`
- **Test Suite**: F9.4 and F9.5 Split payment
- **Page / Target**: `SCR-08 Payment failed`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-10, PB-11; FS F9: BR-F9-05; BR-F9-11; Step 7.4
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-02, ENV-R9-03, ENV-R9-05
- **Assumption Reference**: ASM-R9-25: The online leg is Failed, any EA part is reversed first, the invoice returns to Issued and the Parent sees PAYMENT_FAILED (PAYMENT_FAILED_EA_RETURNED when an EA part was reversed).
- **Note**: xác nhận trace. Sandbox của mock không có tình huống provider từ chối mở phiên.

**Preconditions:**
```text
1. PAR-A is signed in and is on SCR-05 for a fresh 50.00 invoice of STU-103 with the split option.
 2. The sandbox is set to refuse the creation of the payment session.
```

**Test Data:**
```text
Student: STU-103 Marcus Tan, Singapore Citizen, EA Active, balance 20.00 SGD
 Invoice: a fresh Issued invoice for STU-103, Net 50.00 SGD (same as INV-3001), created by the seed script just before the case
```

**Test Steps:**
1. Confirm the payment.
2. Look at the legs, the transaction, the invoice, the ledger and the balance.

**Expected Result:**
> 1. The EA leg is Reversed and the online leg is Failed.
>  2. The transaction is Failed and the invoice is Issued.
>  3. The EA balance is 20.00 and the Parent sees "Your online payment could not be completed. The amount taken from the Education Account has been returned."

---

#### `TC-107`: A failed reversal moves the payment to ReconciliationRequired

- **Scenario ID**: `TS-018`
- **Test Suite**: F9.4 and F9.5 Split payment
- **Page / Target**: `SCR-06 Pending`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-10, PB-11; FS F9: AC-18; EX-13; Step 7.6; Appendix A; SCR-06 Verifying
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-02, ENV-R9-03, ENV-R9-05
- **Assumption Reference**: ASM-R9-28: The system retries a failed reversal up to a limit N set by Dev, then sets the leg and transaction to ReconciliationRequired. QA checks that retries stop.
- **Note**: xác nhận trace (AC-18, EX-13, Step 7.6). UI mock không có cách làm hoàn EA lỗi nên chưa thấy trạng thái verifying.

**Preconditions:**
```text
1. A split payment of EA 20.00 and online 30.00 is confirmed for INV-3001 of STU-103.
 2. The EA leg is Succeeded.
 3. Function 1 is set to fail every reversal.
```

**Test Data:**
```text
Student: STU-103 Marcus Tan, Singapore Citizen, EA Active, balance 20.00 SGD
 Invoice: INV-3001 (50.00)
```

**Test Steps:**
1. At the provider choose the failure outcome.
2. Return to the portal.
3. Wait until the system stops trying.
4. Look at the screen, the legs, the transaction, the invoice, the alerts and the number of reversal attempts.

**Expected Result:**
> 1. The EA leg and the transaction are ReconciliationRequired.
>  2. The invoice stays PaymentPending and is not Paid.
>  3. SCR-06 shows the verifying state.
>  4. An operations alert is raised.
>  5. The system stops retrying after a limited number of attempts.

**Actual Result:**
> Chạy trên bản Dev local function9_14-10-26, Chrome, 2026-10-15; dữ liệu mẫu khác R9 nên không xét. Bản dev chưa có hoàn EA nên không dựng được tình huống hoàn EA lỗi. Khi online thất bại sau khi EA đã trừ, transaction là ReconciliationRequired (status 5), invoice còn PaymentPending, màn hiện Payment needs review, nhưng lượt EA vẫn Succeeded (không phải ReconciliationRequired). Chưa có bằng chứng cho cảnh báo vận hành và giới hạn số lần thử lại.

---

#### `TC-108`: A failure after the EA debit and before the online session is cleaned up by the sweep

- **Scenario ID**: `TS-018`
- **Test Suite**: F9.4 and F9.5 Split payment
- **Page / Target**: `Orphan sweep job`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: Tender R9; PB-10, PB-11; FS F9: EX-11; BR-F9-05; DA-14
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-03, ENV-R9-05
- **Assumption Reference**: ASM-R9-08: The sweep finds a Pending transaction with an EA leg Succeeded and no online leg after X minutes and reverses the EA part. QA can run the sweep on demand.
- **Note**: xác nhận

**Preconditions:**
```text
1. A split payment is confirmed for a fresh 50.00 invoice of STU-103.
 2. The system is stopped right after the EA leg is Succeeded, so no online leg exists.
```

**Test Data:**
```text
Student: STU-103 Marcus Tan, Singapore Citizen, EA Active, balance 20.00 SGD
 Invoice: a fresh Issued invoice for STU-103, Net 50.00 SGD (same as INV-3001), created by the seed script just before the case
```

**Test Steps:**
1. Wait X minutes (or run the sweep on demand).
2. Look at the EA leg, the transaction, the invoice, the ledger and the balance.

**Expected Result:**
> 1. The sweep finds the Pending transaction with an EA leg Succeeded and no online leg.
>  2. The EA part is reversed. The EA leg is Reversed, the transaction is Failed and the invoice is Issued.
>  3. The EA balance is 20.00 again.

---

#### `TC-109`: The sweep leaves a split payment alone when the online leg exists

- **Scenario ID**: `TS-018`
- **Test Suite**: F9.4 and F9.5 Split payment
- **Page / Target**: `Orphan sweep job`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: Tender R9; PB-10, PB-11; FS F9: EX-11; BR-F9-11
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-02, ENV-R9-03, ENV-R9-05
- **Assumption Reference**: ASM-R9-08: The sweep finds a Pending transaction with an EA leg Succeeded and no online leg after X minutes and reverses the EA part. QA can run the sweep on demand.
- **Note**: xác nhận

**Preconditions:**
```text
1. A split payment is confirmed for a fresh 50.00 invoice of STU-103.
 2. The EA leg is Succeeded and the online leg is Pending at the provider.
```

**Test Data:**
```text
Student: STU-103 Marcus Tan, Singapore Citizen, EA Active, balance 20.00 SGD
 Invoice: a fresh Issued invoice for STU-103, Net 50.00 SGD (same as INV-3001), created by the seed script just before the case
```

**Test Steps:**
1. Wait X minutes (or run the sweep on demand).
2. Look at the EA leg, the online leg and the ledger.

**Expected Result:**
> 1. The EA leg is still Succeeded and no reversal is made.
>  2. The online leg is still Pending.

---

#### `TC-110`: A late provider success after the EA was returned is not paid and goes to manual handling

- **Scenario ID**: `TS-018`
- **Test Suite**: F9.4 and F9.5 Split payment
- **Page / Target**: `SCR-06 Pending`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-10, PB-11; FS F9: AC-20; EX-12; Appendix A; OOS 3; NQ-14
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-02, ENV-R9-03, ENV-R9-04, ENV-R9-05
- **Assumption Reference**: N/A
- **Note**: The FS does not give the status of the transaction and of the invoice after the late success. The case checks only what the FS states.
 xác nhận trace (AC-20, EX-12, NQ-14). Sandbox của mock không có nút báo thành công muộn.

**Preconditions:**
```text
1. A split payment was confirmed for INV-3001 of STU-103, the online part failed and the EA part was reversed. The invoice is Issued.
 2. The sandbox can send a late success for the online payment.
```

**Test Data:**
```text
Student: STU-103 Marcus Tan, Singapore Citizen, EA Active, balance 20.00 SGD
 Invoice: INV-3001 (50.00)
```

**Test Steps:**
1. Send a valid success webhook for the online payment.
2. Look at the online leg, the invoice, the alerts and the balance.

**Expected Result:**
> 1. The online leg is ReconciliationRequired.
>  2. The invoice does not become Paid by itself.
>  3. An operations alert is raised.
>  4. The EA part stays reversed and no online refund is made.

---


### Test Suite: F9.6 Webhook and reconciliation

#### `TC-111`: A valid callback is recorded at once and processed later

- **Scenario ID**: `TS-019`
- **Test Suite**: F9.6 Webhook and reconciliation
- **Page / Target**: `Webhook endpoint`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: Tender R9; PB-11; FS F9: BR-F9-06; AC-10; AC-08; 4.2 WebhookReceipt (ProcessingStatus, ProcessedAt)
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-02, ENV-R9-04, ENV-R9-05
- **Assumption Reference**: ASM-R9-19: A callback with a wrong or missing signature is rejected with a 4xx response, a security log entry is written and nothing is stored in the webhook receipt. A valid callback gets a 2xx response at once.
- **Note**: xác nhận trace. UI mock sandbox gửi webhook (dòng 'Dispatching webhook event') rồi đổi màn sau vài giây; không xem được mã 2xx hay receipt.

**Preconditions:**
```text
1. An online payment is started for a fresh 75.00 invoice of STU-102. The online leg is Pending with the FundingReference FR-ONL-01.
 2. The processing job can be paused so the order of steps can be seen.
```

**Test Data:**
```text
Student: STU-102 Chloe Tan, Permanent Resident, no Education Account
 Callback: success, valid signature, ProviderCode SANDBOX, ProviderEventId EVT-001, FundingReference FR-ONL-01
```

**Test Steps:**
1. Pause the processing job.
2. Send the valid callback to the webhook.
3. Read the response and the webhook receipt.
4. Resume the processing job.
5. Read the receipt, the online leg, the transaction and the invoice.

**Expected Result:**
> 1. The webhook answers with a 2xx response at once and does not wait for the processing.
>  2. The receipt exists with ProcessingStatus Received and an empty ProcessedAt.
>  3. After the job runs the receipt is Processed with ProcessedAt set and linked to the online leg.
>  4. The online leg is Succeeded, the transaction is Succeeded and the invoice is Paid.

---

#### `TC-112`: A callback with a wrong signature is rejected and changes nothing

- **Scenario ID**: `TS-019`
- **Test Suite**: F9.6 Webhook and reconciliation
- **Page / Target**: `Webhook endpoint`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Security`
- **Traceability**: Tender R9; PB-11; FS F9: EX-06; AC-10; BR-F9-06; 4.2 WebhookReceipt (only authenticated callbacks are stored)
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-02, ENV-R9-04, ENV-R9-05
- **Assumption Reference**: ASM-R9-19: A callback with a wrong or missing signature is rejected with a 4xx response, a security log entry is written and nothing is stored in the webhook receipt. A valid callback gets a 2xx response at once.
- **Note**: xác nhận trace. UI mock: tick Tamper HMAC rồi Pay Successfully hiện 'Webhook Rejected by Portal: Invalid HMAC signature' và ở lại trang sandbox, không chuyển sang màn kết quả. Mã 4xx, log bảo mật và receipt không xem được trên mock.

**Preconditions:**
```text
1. An online payment is started for a fresh 75.00 invoice of STU-102. The online leg is Pending with the FundingReference FR-ONL-01.
```

**Test Data:**
```text
Student: STU-102 Chloe Tan, Permanent Resident, no Education Account
 Callback: success, signature made with a wrong secret
```

**Test Steps:**
1. Send the callback with the wrong signature.
2. Read the response, the webhook receipts, the security log, the online leg and the invoice.

**Expected Result:**
> 1. The callback is rejected with a 4xx response.
>  2. A security log entry is written.
>  3. No receipt is stored for it.
>  4. The online leg is still Pending and the invoice is still PaymentPending.

---

#### `TC-113`: A callback without a signature is rejected

- **Scenario ID**: `TS-019`
- **Test Suite**: F9.6 Webhook and reconciliation
- **Page / Target**: `Webhook endpoint`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Security`
- **Traceability**: Tender R9; PB-11; FS F9: BR-F9-06; EX-06; AC-10
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-02, ENV-R9-04, ENV-R9-05
- **Assumption Reference**: ASM-R9-19: A callback with a wrong or missing signature is rejected with a 4xx response, a security log entry is written and nothing is stored in the webhook receipt. A valid callback gets a 2xx response at once.
- **Note**: xác nhận trace. Mock chỉ có một kiểu sai chữ ký (Tamper HMAC), không có kiểu thiếu chữ ký.

**Preconditions:**
```text
1. An online payment is started for a fresh 75.00 invoice of STU-102. The online leg is Pending with the FundingReference FR-ONL-01.
```

**Test Data:**
```text
Student: STU-102 Chloe Tan, Permanent Resident, no Education Account
 Callback: success, no signature header
```

**Test Steps:**
1. Send the callback without the signature.
2. Read the response, the receipts, the security log and the online leg.

**Expected Result:**
> 1. The callback is rejected with a 4xx response and a security log entry is written.
>  2. No receipt is stored and the online leg is still Pending.

---

#### `TC-114`: A callback whose content was changed after signing is rejected

- **Scenario ID**: `TS-019`
- **Test Suite**: F9.6 Webhook and reconciliation
- **Page / Target**: `Webhook endpoint`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Security`
- **Traceability**: Tender R9; PB-11; FS F9: BR-F9-06; EX-06
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-02, ENV-R9-04, ENV-R9-05
- **Assumption Reference**: ASM-R9-19: A callback with a wrong or missing signature is rejected with a 4xx response, a security log entry is written and nothing is stored in the webhook receipt. A valid callback gets a 2xx response at once.
- **Note**: xác nhận trace. Mock chỉ có Tamper HMAC, không phân biệt kiểu nội dung bị sửa sau khi ký.

**Preconditions:**
```text
1. An online payment is started for a fresh 75.00 invoice of STU-102. The online leg is Pending with the FundingReference FR-ONL-01.
```

**Test Data:**
```text
Student: STU-102 Chloe Tan, Permanent Resident, no Education Account
 Callback: valid signature of a failure payload, body changed to success
```

**Test Steps:**
1. Sign a failure payload.
2. Change the body to a success payload and keep the signature.
3. Send the callback.
4. Read the response and the online leg.

**Expected Result:**
> 1. The callback is rejected with a 4xx response and a security log entry is written.
>  2. The online leg is still Pending and the invoice is not Paid.

---

#### `TC-115`: The same event sent twice is applied once

- **Scenario ID**: `TS-019`
- **Test Suite**: F9.6 Webhook and reconciliation
- **Page / Target**: `Webhook endpoint`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: Tender R9; PB-11; FS F9: EX-07; AC-10; BR-F9-06; 4.2 WebhookReceipt (unique pair)
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-02, ENV-R9-04, ENV-R9-05
- **Assumption Reference**: N/A
- **Note**: xác nhận

**Preconditions:**
```text
1. An online payment is started for a fresh 75.00 invoice of STU-102. The online leg is Pending with the FundingReference FR-ONL-01.
```

**Test Data:**
```text
Student: STU-102 Chloe Tan, Permanent Resident, no Education Account
 Callback: success, valid signature, ProviderCode SANDBOX, ProviderEventId EVT-002
```

**Test Steps:**
1. Send the valid callback.
2. Let it be processed.
3. Send exactly the same callback again.
4. Read the receipts, the online leg, the transaction and the audit log.

**Expected Result:**
> 1. Only one receipt exists for ProviderCode SANDBOX and ProviderEventId EVT-002.
>  2. The online leg changed to Succeeded once and the invoice changed to Paid once.
>  3. The second callback has no further effect and no extra audit entry.

---

#### `TC-116`: A new event for a payment that is already finished changes nothing

- **Scenario ID**: `TS-019`
- **Test Suite**: F9.6 Webhook and reconciliation
- **Page / Target**: `Webhook endpoint`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: Tender R9; PB-11; FS F9: Appendix A (no transition out of a final state); 4.2 WebhookReceipt ProcessingStatus
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-02, ENV-R9-04, ENV-R9-05
- **Assumption Reference**: ASM-R9-20: Such a callback is stored (its signature is valid), marked Ignored, and changes no state.
- **Note**: xác nhận

**Preconditions:**
```text
1. An online payment of a fresh 75.00 invoice of STU-102 is finished: the online leg is Succeeded and the invoice is Paid.
```

**Test Data:**
```text
Student: STU-102 Chloe Tan, Permanent Resident, no Education Account
 Callback: failure, valid signature, new ProviderEventId EVT-003
```

**Test Steps:**
1. Send the valid failure callback for the finished payment.
2. Read the receipt, the online leg, the transaction and the invoice.

**Expected Result:**
> 1. The online leg stays Succeeded, the transaction stays Succeeded and the invoice stays Paid.
>  2. The receipt is stored with the status Ignored.

---

#### `TC-117`: A valid callback that matches no payment is ignored

- **Scenario ID**: `TS-019`
- **Test Suite**: F9.6 Webhook and reconciliation
- **Page / Target**: `Webhook endpoint`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: Tender R9; PB-11; FS F9: 4.2 WebhookReceipt (FundingTransactionId after matching, ProcessingStatus)
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-02, ENV-R9-04, ENV-R9-05
- **Assumption Reference**: ASM-R9-20: Such a callback is stored (its signature is valid), marked Ignored, and changes no state.
- **Note**: xác nhận

**Preconditions:**
```text
1. An online payment is started for a fresh 75.00 invoice of STU-102. The online leg is Pending with the FundingReference FR-ONL-01.
```

**Test Data:**
```text
Callback: success, valid signature, FundingReference FR-UNKNOWN-99
```

**Test Steps:**
1. Send the valid callback with an unknown FundingReference.
2. Read the receipt and the online leg of FR-ONL-01.

**Expected Result:**
> 1. The receipt is stored with the status Ignored.
>  2. No leg, transaction or invoice changes. FR-ONL-01 is still Pending.

---

#### `TC-118`: A success callback with a different amount does not pay the invoice

- **Scenario ID**: `TS-019`
- **Test Suite**: F9.6 Webhook and reconciliation
- **Page / Target**: `Webhook endpoint`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: Tender R9; PB-11; FS F9: BR-F9-13; 4.2 Transaction (Settled equals Requested when Succeeded)
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-02, ENV-R9-04, ENV-R9-05
- **Assumption Reference**: ASM-R9-21: A success callback with an amount different from the leg amount does not make the leg Succeeded. The leg becomes ReconciliationRequired and the invoice is not Paid.
- **Note**: xác nhận

**Preconditions:**
```text
1. An online payment is started for a fresh 75.00 invoice of STU-102. The online leg is Pending with the FundingReference FR-ONL-01.
```

**Test Data:**
```text
Student: STU-102 Chloe Tan, Permanent Resident, no Education Account
 Callback: success for 25.00 while the leg amount is 75.00
```

**Test Steps:**
1. Send the valid success callback with the amount 25.00.
2. Read the online leg, the transaction, the invoice and the alerts.

**Expected Result:**
> 1. The online leg is not Succeeded. It is ReconciliationRequired.
>  2. The invoice is not Paid and an operations alert is raised.

---

#### `TC-119`: Only a hash of the callback is stored

- **Scenario ID**: `TS-019`
- **Test Suite**: F9.6 Webhook and reconciliation
- **Page / Target**: `Database and logs`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Security`
- **Traceability**: Tender R9; PB-11; FS F9: BR-F9-06; DA-01; 4.2 WebhookReceipt PayloadHash
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-02, ENV-R9-04, ENV-R9-05
- **Assumption Reference**: N/A
- **Note**: xác nhận

**Preconditions:**
```text
1. An online payment is started for a fresh 75.00 invoice of STU-102. The online leg is Pending with the FundingReference FR-ONL-01.
```

**Test Data:**
```text
Callback: success, valid signature, with an extra field 'note' = ZZ-RAW-PAYLOAD-MARKER
```

**Test Steps:**
1. Send the valid callback and let it be processed.
2. Search the webhook receipt table and the logs for the marker text.
3. Read the PayloadHash of the receipt.

**Expected Result:**
> 1. The marker text is not stored in the receipt table and not in the logs.
>  2. PayloadHash holds a SHA-256 value of 32 bytes.
>  3. No card data is stored.

---

#### `TC-120`: A lost webhook is replaced by the provider status query: success

- **Scenario ID**: `TS-020`
- **Test Suite**: F9.6 Webhook and reconciliation
- **Page / Target**: `Reconciliation job`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: Tender R9; PB-11; FS F9: Step 7.1; Appendix A (online leg Pending to Succeeded: webhook or reconciliation)
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-02, ENV-R9-05
- **Assumption Reference**: ASM-R9-07: SIT has a threshold of T minutes and a polling interval of P minutes set by Dev. QA can run the reconciliation job on demand. The cases use T and P.
- **Note**: xác nhận

**Preconditions:**
```text
1. An online payment is started for a fresh 75.00 invoice of STU-102. The online leg is Pending with the FundingReference FR-ONL-01.
 2. The provider has the payment as successful but no callback is sent.
```

**Test Data:**
```text
Student: STU-102 Chloe Tan, Permanent Resident, no Education Account
```

**Test Steps:**
1. Run the reconciliation job (or wait for the polling interval).
2. Read the online leg, the transaction and the invoice.

**Expected Result:**
> 1. The system asks the provider about the Pending leg.
>  2. The online leg is Succeeded, the transaction is Succeeded and the invoice is Paid.

---

#### `TC-121`: A lost webhook is replaced by the provider status query: failure

- **Scenario ID**: `TS-020`
- **Test Suite**: F9.6 Webhook and reconciliation
- **Page / Target**: `Reconciliation job`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: Tender R9; PB-11; FS F9: Step 7.1; Step 7.5; Appendix A
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-02, ENV-R9-05
- **Assumption Reference**: ASM-R9-07: SIT has a threshold of T minutes and a polling interval of P minutes set by Dev. QA can run the reconciliation job on demand. The cases use T and P.
- **Note**: xác nhận

**Preconditions:**
```text
1. An online payment is started for a fresh 75.00 invoice of STU-102. The online leg is Pending with the FundingReference FR-ONL-01.
 2. The provider has the payment as failed but no callback is sent.
```

**Test Data:**
```text
Student: STU-102 Chloe Tan, Permanent Resident, no Education Account
```

**Test Steps:**
1. Run the reconciliation job (or wait for the polling interval).
2. Read the online leg, the transaction and the invoice.

**Expected Result:**
> 1. The online leg is Failed and the transaction is Failed.
>  2. The invoice is Issued and nothing is collected.

---

#### `TC-122`: A Pending leg that stays unclear beyond the threshold moves to ReconciliationRequired

- **Scenario ID**: `TS-020`
- **Test Suite**: F9.6 Webhook and reconciliation
- **Page / Target**: `SCR-06 Pending`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: Tender R9; PB-11; FS F9: EX-08; Step 7.6; NQ-10; Appendix A; SCR-06 Verifying
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-02, ENV-R9-05
- **Assumption Reference**: ASM-R9-07: SIT has a threshold of T minutes and a polling interval of P minutes set by Dev. QA can run the reconciliation job on demand. The cases use T and P.
- **Note**: xác nhận

**Preconditions:**
```text
1. An online payment is started for a fresh 75.00 invoice of STU-102. The online leg is Pending with the FundingReference FR-ONL-01.
 2. The provider does not answer status questions and sends no callback.
```

**Test Data:**
```text
Student: STU-102 Chloe Tan, Permanent Resident, no Education Account
 Threshold: T minutes
```

**Test Steps:**
1. Wait longer than T minutes while the reconciliation job runs.
2. Read the online leg, the transaction, the invoice and the alerts.
3. Open the invoice as PAR-A.

**Expected Result:**
> 1. Before T minutes the leg stays Pending and is never set to Failed.
>  2. After T minutes the leg and the transaction are ReconciliationRequired.
>  3. The invoice stays PaymentPending and an operations alert is raised.
>  4. The Parent sees the verifying state on SCR-06.

---

#### `TC-123`: A webhook and a status query that arrive together are applied once

- **Scenario ID**: `TS-020`
- **Test Suite**: F9.6 Webhook and reconciliation
- **Page / Target**: `Reconciliation job`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: Tender R9; PB-11; FS F9: BR-F9-06; EX-07; Step 7.1
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-02, ENV-R9-04, ENV-R9-05
- **Assumption Reference**: N/A
- **Note**: xác nhận

**Preconditions:**
```text
1. An online payment is started for a fresh 75.00 invoice of STU-102. The online leg is Pending with the FundingReference FR-ONL-01.
```

**Test Data:**
```text
Student: STU-102 Chloe Tan, Permanent Resident, no Education Account
 Webhook success and status query success at the same moment
```

**Test Steps:**
1. Send the valid success callback and run the reconciliation job at the same moment.
2. Read the online leg, the transaction, the invoice and the audit log.

**Expected Result:**
> 1. The online leg changes to Succeeded once and the invoice changes to Paid once.
>  2. There is no second state change in the audit log.

---

#### `TC-124`: Operations resolves a payment in ReconciliationRequired

- **Scenario ID**: `TS-020`
- **Test Suite**: F9.6 Webhook and reconciliation
- **Page / Target**: `Operations`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-11; FS F9: Appendix A; AC-18; EX-13
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
- **Assumption Reference**: ASM-R9-22: None. No assumption is possible without a description of the Operations action.
- **Note**: Blocked until the BA describes how Operations resolves a ReconciliationRequired payment.
 xác nhận lý do Block: FS 09 Appendix A chỉ nêu trạng thái đích khi Operations xử lý ReconciliationRequired, AC-18 và EX-13 chỉ nêu cảnh báo vận hành; không có mô tả thao tác của Operations (màn hình, quyền, các bước).

**Preconditions:**
```text
1. A transaction is ReconciliationRequired.
```

**Test Data:**
```text
Transaction in ReconciliationRequired
```

**Test Steps:**
1. Not defined: the FS has no screen, API or procedure for the Operations action.

**Expected Result:**
> 1. Not defined. Appendix A says the transaction moves to Succeeded, Failed or Cancelled and the invoice to Paid or Issued.

---


### Test Suite: F9.7 Result, receipt and retry

#### `TC-125`: The waiting screen shows the pending notice, a temporary reference and the actions

- **Scenario ID**: `TS-021`
- **Test Suite**: F9.7 Result, receipt and retry
- **Page / Target**: `SCR-06 Pending`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-09, PB-10, PB-11; FS F9: Step 7.2; Appendix C SCR-06; 4.1 SCR-06
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-02, ENV-R9-05
- **Assumption Reference**: N/A
- **Note**: xác nhận. UI mock màn Payment In Progress: thông báo đang xử lý, Transaction Ref, Refresh Status và Back to Fees. Mã hiện là mã giao dịch dạng PAY, không ghi là mã tạm.

**Preconditions:**
```text
1. PAR-A has started an online payment for a fresh 75.00 invoice of STU-102 and the leg is Pending.
```

**Test Data:**
```text
Student: STU-102 Chloe Tan, Permanent Resident, no Education Account
 Invoice: a fresh Issued invoice for STU-102, Net 75.00 SGD, created by the seed script just before the case
```

**Test Steps:**
1. Return to the portal after the provider page.
2. Read SCR-06.

**Expected Result:**
> 1. SCR-06 shows that the payment is pending.
>  2. It shows a temporary reference.
>  3. It has the actions to refresh the status and to go back to SCR-02.

---

#### `TC-126`: Refreshing the waiting screen shows the success screen after the result arrives

- **Scenario ID**: `TS-021`
- **Test Suite**: F9.7 Result, receipt and retry
- **Page / Target**: `SCR-06 Pending`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-09, PB-10, PB-11; FS F9: Step 7.2; Step 7.3; SCR-06 action refresh
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-02, ENV-R9-04
- **Assumption Reference**: N/A
- **Note**: xác nhận trace. UI mock: bấm Refresh Status đưa về trang chủ chưa đăng nhập (đã thử 2 lần), không hiện được màn thành công; mock cũng không có cách báo kết quả sau Close Browser.

**Preconditions:**
```text
1. PAR-A is on SCR-06 for a Pending online payment of a fresh 75.00 invoice of STU-102.
```

**Test Data:**
```text
Student: STU-102 Chloe Tan, Permanent Resident, no Education Account
```

**Test Steps:**
1. Send the valid success callback.
2. Use the refresh action of SCR-06.

**Expected Result:**
> 1. SCR-07 opens with the success result, the reference and the online part 75.00.
>  2. The invoice is Paid.

---

#### `TC-127`: A Parent who comes back to a pending invoice cannot start a second payment

- **Scenario ID**: `TS-021`
- **Test Suite**: F9.7 Result, receipt and retry
- **Page / Target**: `SCR-02 Outstanding fees`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-09, PB-10, PB-11; FS F9: AC-11; BR-F9-09; EX-09; 5.1 PAYMENT_PENDING
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-02, ENV-R9-05, ENV-R9-06
- **Assumption Reference**: ASM-R9-03: SCR-02 lists invoices in Issued (payable) and PaymentPending (shown as Pending, not selectable). Paid, Cancelled and Draft are not listed. The total owed is the sum of Net of the listed invoices. SCR-03 appears only when the child has no listed invoice.
- **Note**: xác nhận. UI mock: invoice AWAITING PAYMENT chỉ có View status, không chọn thanh toán mới được. Mã 409 là phản hồi API, không xem được trên mock.

**Preconditions:**
```text
1. PAR-A has started an online payment for a fresh 50.00 invoice of STU-101 and the transaction is Pending.
```

**Test Data:**
```text
Student: STU-101 Ethan Tan, Singapore Citizen, EA Active, balance 200.00 SGD
 Invoice: pending invoice with an open transaction
```

**Test Steps:**
1. Sign out and sign in again as PAR-A.
2. Open SCR-02 of STU-101 and try to select the pending invoice.
3. Send a create payment request for the same invoice with a new key.

**Expected Result:**
> 1. The invoice shows the status Pending and the waiting state can be opened.
>  2. The invoice cannot be selected for a new payment.
>  3. The request is refused with 409 and the message "A payment for this invoice is still being processed."; no new transaction exists.

---

#### `TC-128`: The verifying state does not say the payment failed and offers no retry

- **Scenario ID**: `TS-021`
- **Test Suite**: F9.7 Result, receipt and retry
- **Page / Target**: `SCR-06 Pending`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `UI`
- **Traceability**: Tender R9; PB-09, PB-10, PB-11; FS F9: Step 7.6; 4.1 SCR-06 (ReconciliationRequired shown as verifying); Appendix C SCR-06
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-02, ENV-R9-03, ENV-R9-05
- **Assumption Reference**: N/A
- **Note**: xác nhận trace (Step 7.6, 4.1 SCR-06, Appendix C SCR-06). UI mock chưa có trạng thái verifying riêng; màn Payment In Progress không có Try again nhưng cũng không nêu phần EA đã trừ.

**Preconditions:**
```text
1. A split payment of a fresh 50.00 invoice of STU-103 is ReconciliationRequired because the reversal failed.
```

**Test Data:**
```text
Student: STU-103 Marcus Tan, Singapore Citizen, EA Active, balance 20.00 SGD
```

**Test Steps:**
1. Open SCR-06 as PAR-A.
2. Read the text and the actions.

**Expected Result:**
> 1. SCR-06 shows the verifying state, not a failure.
>  2. It names the EA part that was taken.
>  3. No Try again action is offered.

**Actual Result:**
> Chạy trên bản Dev local function9_14-10-26, Chrome, 2026-10-15; dữ liệu mẫu khác R9 nên không xét. Trạng thái cần xem lại (ReconciliationRequired) hiện Payment needs review, We are reviewing this payment, và dòng Your Education Account may still have been deducted; liệt kê Education Account Succeeded 250 và Online Gateway Failed 100; không hiện nút Try again (chỉ có Back to home). Không nói thanh toán thất bại.

---

#### `TC-129`: The success screen of an EA payment shows reference, time, part and total

- **Scenario ID**: `TS-022`
- **Test Suite**: F9.7 Result, receipt and retry
- **Page / Target**: `SCR-07 Payment confirmation`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-09, PB-10, PB-11; FS F9: Step 7.3; 4.1 SCR-07; Appendix C SCR-07
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-03
- **Assumption Reference**: N/A
- **Note**: xác nhận. UI mock EA only: biên lai hiện Payment Succeeded, Transaction Reference, Paid At (SGT), Education Account 15.00, Total Settled 15.00, nút Print Receipt và Back to Fees. Không có nút tải PDF, trong khi AC-13 và SCR-07 nói tải hoặc in.

**Preconditions:**
```text
1. PAR-A has just paid a fresh 50.00 invoice of STU-101 with the EA.
```

**Test Data:**
```text
Student: STU-101 Ethan Tan, Singapore Citizen, EA Active, balance 200.00 SGD
 Invoice: a fresh Issued invoice for STU-101, Net 50.00 SGD, created by the seed script just before the case
```

**Test Steps:**
1. Read SCR-07.
2. Use the action to go back to SCR-02.

**Expected Result:**
> 1. SCR-07 shows the success status, the transaction reference, the time of payment, the EA part 50.00 and the total 50.00.
>  2. It offers to download or print the receipt and to go back to SCR-02.

**Actual Result:**
> Chạy trên bản Dev local function9_14-10-26, Chrome, 2026-10-15; dữ liệu mẫu khác R9 nên không xét. Màn kết quả EA only hiện Payment successful, Transaction ID, invoice INV000001, Completed at, dòng Education Account Succeeded, tổng; có Print receipt và Back to home (không về danh sách phí). Chưa kiểm Back to home dẫn đến đâu, và mã hiển thị là Transaction ID chứ chưa thấy transaction reference TRX.

---

#### `TC-130`: The success screen of a split payment shows both parts

- **Scenario ID**: `TS-022`
- **Test Suite**: F9.7 Result, receipt and retry
- **Page / Target**: `SCR-07 Payment confirmation`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-09, PB-10, PB-11; FS F9: AC-15; Step 7.3; 4.1 SCR-07 Settled amount
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-02, ENV-R9-03
- **Assumption Reference**: N/A
- **Note**: xác nhận. UI mock split: biên lai hai dòng Education Account 20.00 và Online Payment 30.00, tổng 50.00.

**Preconditions:**
```text
1. PAR-A has just paid INV-3001 of STU-103 with a split of EA 20.00 and online 30.00.
```

**Test Data:**
```text
Student: STU-103 Marcus Tan, Singapore Citizen, EA Active, balance 20.00 SGD
```

**Test Steps:**
1. Read SCR-07.

**Expected Result:**
> 1. SCR-07 shows the EA part 20.00 and the online part 30.00, each with its settled amount.
>  2. The settled amounts add up to the total 50.00.

**Actual Result:**
> Chạy trên bản Dev local function9_14-10-26, Chrome, 2026-10-15; dữ liệu mẫu khác R9 nên không xét. Màn kết quả của chia đôi hiện hai dòng: Education Account Succeeded requested 250 settled 250 và Online Gateway Succeeded requested 100 settled 100, tổng settled 350.

---

#### `TC-131`: The receipt PDF of an EA payment can be downloaded

- **Scenario ID**: `TS-022`
- **Test Suite**: F9.7 Result, receipt and retry
- **Page / Target**: `SCR-07 Payment confirmation`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-09, PB-10, PB-11; FS F9: AC-13; SCR-07 action download
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-03
- **Assumption Reference**: ASM-R9-10: The transaction reference is unique, at most 50 characters and follows PAY-YYYYMMDD-XXXXXX, where YYYYMMDD is the payment date in SGT. The receipt PDF shows the reference, the paid at time in SGT, the child, the invoice number, each paid part with its method and the total.
- **Note**: xác nhận trace (AC-13). UI mock biên lai chỉ có Print Receipt, không có nút tải PDF nên chưa thực hiện được Expected 1 và 2.

**Preconditions:**
```text
1. PAR-A has just paid a fresh 50.00 invoice of STU-101 with the EA.
```

**Test Data:**
```text
Student: STU-101 Ethan Tan, Singapore Citizen, EA Active, balance 200.00 SGD
 Invoice: a fresh Issued invoice for STU-101, Net 50.00 SGD, created by the seed script just before the case
```

**Test Steps:**
1. Use the download receipt action.
2. Open the PDF.

**Expected Result:**
> 1. A PDF file is downloaded and opens.
>  2. It shows the transaction reference and the EA part 50.00 with the total 50.00.

**Actual Result:**
> Chạy trên bản Dev local function9_14-10-26, Chrome, 2026-10-15; dữ liệu mẫu khác R9 nên không xét. Phần receipt trên trang kết quả chỉ có nút Print receipt và Back to home, không có nút tải PDF nên không thực hiện được Expected 1 và 2. Chưa tạo Defect.

---

#### `TC-132`: The receipt PDF of a split payment shows two parts

- **Scenario ID**: `TS-022`
- **Test Suite**: F9.7 Result, receipt and retry
- **Page / Target**: `SCR-07 Payment confirmation`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-09, PB-10, PB-11; FS F9: AC-13; AC-15 (receipt shows two parts)
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-02, ENV-R9-03
- **Assumption Reference**: ASM-R9-10: The transaction reference is unique, at most 50 characters and follows PAY-YYYYMMDD-XXXXXX, where YYYYMMDD is the payment date in SGT. The receipt PDF shows the reference, the paid at time in SGT, the child, the invoice number, each paid part with its method and the total.
- **Note**: xác nhận trace (AC-13, AC-15). UI mock không có nút tải PDF; nội dung hai phần có trên màn biên lai.

**Preconditions:**
```text
1. PAR-A has just paid INV-3001 of STU-103 with a split of EA 20.00 and online 30.00.
```

**Test Data:**
```text
Student: STU-103 Marcus Tan, Singapore Citizen, EA Active, balance 20.00 SGD
```

**Test Steps:**
1. Use the download receipt action.
2. Open the PDF.

**Expected Result:**
> 1. The PDF shows the transaction reference.
>  2. It shows two parts, EA 20.00 and online 30.00, and the total 50.00.

---

#### `TC-133`: The receipt can be printed

- **Scenario ID**: `TS-022`
- **Test Suite**: F9.7 Result, receipt and retry
- **Page / Target**: `SCR-07 Payment confirmation`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-09, PB-10, PB-11; FS F9: AC-13; SCR-07 action print
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-03
- **Assumption Reference**: N/A
- **Note**: xác nhận trace. UI mock có nút Print Receipt; chưa bấm vì sẽ mở hộp thoại in của trình duyệt.

**Preconditions:**
```text
1. PAR-A has just paid a fresh 50.00 invoice of STU-101 with the EA.
```

**Test Data:**
```text
Student: STU-101 Ethan Tan, Singapore Citizen, EA Active, balance 200.00 SGD
```

**Test Steps:**
1. Use the print receipt action.
2. Look at the print preview.

**Expected Result:**
> 1. The print preview shows the same content as the receipt: reference, parts and total.

---

#### `TC-134`: Transaction references are unique and follow the proposed format

- **Scenario ID**: `TS-022`
- **Test Suite**: F9.7 Result, receipt and retry
- **Page / Target**: `SCR-07 Payment confirmation`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-09, PB-10, PB-11; FS F9: 4.1 SCR-07 Transaction reference; 4.2 Transaction TransactionReference (unique); NQ-12
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-03
- **Assumption Reference**: ASM-R9-10: The transaction reference is unique, at most 50 characters and follows PAY-YYYYMMDD-XXXXXX, where YYYYMMDD is the payment date in SGT. The receipt PDF shows the reference, the paid at time in SGT, the child, the invoice number, each paid part with its method and the total.
- **Note**: xác nhận. UI mock mã có dạng PAY-YYYYMMDD-XXXXXX (ví dụ PAY-20261014 kèm 6 ký tự) và khác nhau giữa các lần trả (6B3KMG, 25UC42). Khi thử lại sau thất bại cùng invoice, màn thất bại và màn chờ vẫn dùng lại mã của lần đầu.

**Preconditions:**
```text
1. PAR-A pays two fresh 50.00 invoices of STU-101 with the EA, one after the other.
```

**Test Data:**
```text
Student: STU-101 Ethan Tan, Singapore Citizen, EA Active, balance 200.00 SGD
```

**Test Steps:**
1. Read the reference on SCR-07 of the first payment.
2. Read the reference on SCR-07 of the second payment.
3. Count the characters.

**Expected Result:**
> 1. The two references are different.
>  2. Each reference has at most 50 characters and follows PAY-YYYYMMDD-XXXXXX with the payment date.

---

#### `TC-135`: The paid at time is shown in Singapore time

- **Scenario ID**: `TS-022`
- **Test Suite**: F9.7 Result, receipt and retry
- **Page / Target**: `SCR-07 Payment confirmation`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-09, PB-10, PB-11; FS F9: 4.1 SCR-07 Paid at (SGT); 4.2 Transaction CompletedAt (UTC)
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-03, ENV-R9-05
- **Assumption Reference**: N/A
- **Note**: xác nhận trace. UI mock biên lai ghi giờ SGT; giá trị UTC trong DB không xem được. Biên lai invoice có sẵn INV-2026-2000 (trả 20/07/2026, mã PAY-20260720) lại ghi Paid At 00:28:38 SGT ngày 14/10/2026, trùng lúc mở biên lai chứ không phải ngày trả 20/07/2026.

**Preconditions:**
```text
1. PAR-A pays a fresh 50.00 invoice of STU-101 with the EA.
```

**Test Data:**
```text
Student: STU-101 Ethan Tan, Singapore Citizen, EA Active, balance 200.00 SGD
 CompletedAt stored in UTC, for example 06:00
```

**Test Steps:**
1. Read the CompletedAt value in the database.
2. Read the Paid at time on SCR-07.

**Expected Result:**
> 1. The database value is in UTC.
>  2. SCR-07 shows the same moment in SGT, eight hours later (14:00 for 06:00 UTC).

---

#### `TC-136`: The failure screen of an online payment shows the message, the reason and the actions

- **Scenario ID**: `TS-023`
- **Test Suite**: F9.7 Result, receipt and retry
- **Page / Target**: `SCR-08 Payment failed`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-09, PB-10, PB-11; FS F9: Step 7.5; 4.1 SCR-08; Appendix C SCR-08
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-02
- **Assumption Reference**: N/A
- **Note**: xác nhận. UI mock online only thất bại: đúng câu PAYMENT_FAILED, Transaction Reference, Try Again và Exit to Fees, không nhắc hoàn EA. Chỉ có câu thông báo, không có dòng lý do riêng.

**Preconditions:**
```text
1. PAR-A is signed in. An online payment of a fresh 75.00 invoice of STU-102 has failed at the provider.
```

**Test Data:**
```text
Student: STU-102 Chloe Tan, Permanent Resident, no Education Account
 Invoice: a fresh Issued invoice for STU-102, Net 75.00 SGD, created by the seed script just before the case
```

**Test Steps:**
1. Read SCR-08.

**Expected Result:**
> 1. SCR-08 shows "Your payment could not be completed. No amount was deducted."
>  2. It shows a short friendly reason and the transaction reference.
>  3. It has the actions Try again and Exit.
>  4. It does not mention an EA return because no EA part was taken.

**Actual Result:**
> Chạy trên bản Dev local function9_14-10-26, Chrome, 2026-10-15; dữ liệu mẫu khác R9 nên không xét. Online thất bại: màn hiện Payment failed, Your payment could not be completed. Return to Fees & Payments to review the latest outstanding fees; không có câu No amount was deducted, không có dòng lý do ngắn, chỉ có nút Back to home (không có Try again và Exit). Có Transaction ID và không nhắc hoàn EA (đúng Expected 4). Chưa tạo Defect.

---

#### `TC-137`: The failure screen of a split payment says the EA part was returned

- **Scenario ID**: `TS-023`
- **Test Suite**: F9.7 Result, receipt and retry
- **Page / Target**: `SCR-08 Payment failed`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-09, PB-10, PB-11; FS F9: Step 7.4; 5.1 PAYMENT_FAILED_EA_RETURNED; 4.1 SCR-08 Failure reason
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-02, ENV-R9-03
- **Assumption Reference**: N/A
- **Note**: xác nhận. UI mock split thất bại: đúng câu PAYMENT_FAILED_EA_RETURNED, mã tham chiếu, Try Again và Exit to Fees.

**Preconditions:**
```text
1. A split payment of a fresh 50.00 invoice of STU-103 has failed at the provider and the EA part was reversed.
```

**Test Data:**
```text
Student: STU-103 Marcus Tan, Singapore Citizen, EA Active, balance 20.00 SGD
```

**Test Steps:**
1. Read SCR-08.

**Expected Result:**
> 1. SCR-08 shows "Your online payment could not be completed. The amount taken from the Education Account has been returned."
>  2. It shows the transaction reference and the actions Try again and Exit.

**Actual Result:**
> Chạy trên bản Dev local function9_14-10-26, Chrome, 2026-10-15; dữ liệu mẫu khác R9 nên không xét. Split thất bại: màn hiện Payment needs review, We are reviewing this payment, Your Education Account may still have been deducted; EA không được hoàn (reversal id NULL), không có câu The amount taken from the Education Account has been returned, không có Try again và Exit. Chưa tạo Defect.

---

#### `TC-138`: The failure message hides technical details

- **Scenario ID**: `TS-023`
- **Test Suite**: F9.7 Result, receipt and retry
- **Page / Target**: `SCR-08 Payment failed`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Security`
- **Traceability**: Tender R9; PB-09, PB-10, PB-11; FS F9: 4.1 SCR-08 Failure reason (no technical detail); 4.2 FundingLeg FailureReason; 5.1
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-02, ENV-R9-03
- **Assumption Reference**: N/A
- **Note**: xác nhận. UI mock các màn thất bại chỉ hiện câu thân thiện, không có mã kỹ thuật hay chi tiết lỗi.

**Preconditions:**
```text
1. A payment fails for each of these reasons: Function 1 error, provider failure, provider session refused.
```

**Test Data:**
```text
Three failed payments of fresh invoices
```

**Test Steps:**
1. Read SCR-08 for each failed payment.
2. Look at the page text and the response of the status request.

**Expected Result:**
> 1. Each screen shows only the friendly message of section 5.1.
>  2. No stack trace, SQL text, HTTP code, internal failure code or provider raw message is shown.

**Actual Result:**
> Chạy trên bản Dev local function9_14-10-26, Chrome, 2026-10-15; dữ liệu mẫu khác R9 nên không xét. Các màn thất bại (online only và split) chỉ hiện câu thân thiện, không có stack trace, SQL, mã HTTP, failure code hay thông điệp gốc của nhà cung cấp (Gateway reported payment.failed chỉ có trong DB).

---

#### `TC-139`: Exit on the failure screen returns to the invoice list with the invoice still Issued

- **Scenario ID**: `TS-023`
- **Test Suite**: F9.7 Result, receipt and retry
- **Page / Target**: `SCR-02 Outstanding fees`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-09, PB-10, PB-11; FS F9: Appendix C SCR-08 action exit; BR-F9-05
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-02
- **Assumption Reference**: N/A
- **Note**: xác nhận. UI mock: Exit to Fees về danh sách, invoice vẫn có Pay now, số dư EA về như cũ.

**Preconditions:**
```text
1. PAR-A is on SCR-08 after a failed online payment of a fresh 75.00 invoice of STU-102.
```

**Test Data:**
```text
Student: STU-102 Chloe Tan, Permanent Resident, no Education Account
```

**Test Steps:**
1. Use the Exit action.
2. Read the invoice list.

**Expected Result:**
> 1. SCR-02 opens and the invoice is listed as Issued and can be selected again.
>  2. No amount was collected.

**Actual Result:**
> Chạy trên bản Dev local function9_14-10-26, Chrome, 2026-10-15; dữ liệu mẫu khác R9 nên không xét. Sau thất bại online only, mở lại danh sách phí: khoản đã thất bại không còn trong danh sách (chỉ còn 210 và 140, tổng 350) nên không chọn lại được; invoice vẫn PaymentPending trong DB. Chưa tạo Defect.

---

#### `TC-140`: Try again after a failure creates a new transaction with a new key and can succeed

- **Scenario ID**: `TS-023`
- **Test Suite**: F9.7 Result, receipt and retry
- **Page / Target**: `SCR-07 Payment confirmation`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-09, PB-10, PB-11; FS F9: Step 7 Retry; NQ-11; BR-F9-04; BR-F9-09; SCR-08 action Try again
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-02, ENV-R9-03, ENV-R9-05
- **Assumption Reference**: N/A
- **Note**: xác nhận trace. UI mock: Try Again về bước chọn phương thức. Mã giao dịch dạng PAY của lần thử sau giống lần đầu (Ref của sandbox thì khác), nên chưa thấy giao dịch mới như Expected 2. Idempotency key và lịch sử giao dịch không xem được trên mock.

**Preconditions:**
```text
1. A split payment of INV-3001 of STU-103 failed at the provider and the EA part was reversed. The EA balance is 20.00 and the invoice is Issued.
 2. PAR-A is on SCR-08.
```

**Test Data:**
```text
Student: STU-103 Marcus Tan, Singapore Citizen, EA Active, balance 20.00 SGD
 Invoice: INV-3001 (50.00)
```

**Test Steps:**
1. Use Try again.
2. Choose the split option and confirm.
3. Finish with the success outcome at the provider.
4. Read the transactions of the invoice, the ledger and SCR-07.

**Expected Result:**
> 1. Try again opens SCR-04.
>  2. A second transaction is created with a new idempotency key. The first transaction stays Failed in the history.
>  3. The second payment succeeds and the invoice is Paid.
>  4. The ledger shows the first debit, its reversal and one new debit of 20.00. The balance is 0.00.

**Actual Result:**
> Chạy trên bản Dev local function9_14-10-26, Chrome, 2026-10-15; dữ liệu mẫu khác R9 nên không xét. Không có Try again trên màn kết quả thất bại và khoản phí đã thất bại không chọn lại được, nên không tạo được transaction thứ hai. Chưa tạo Defect.

---

#### `TC-141`: No retry is possible while the EA part has not been returned

- **Scenario ID**: `TS-023`
- **Test Suite**: F9.7 Result, receipt and retry
- **Page / Target**: `SCR-06 Pending`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-09, PB-10, PB-11; FS F9: Step 7 Retry (only when the old transaction is closed and the EA part is returned); BR-F9-09
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-02, ENV-R9-03, ENV-R9-05, ENV-R9-06
- **Assumption Reference**: N/A
- **Note**: xác nhận. UI mock: khi chờ không có Pay now, chỉ có View status. Mã 409 và sổ cái không xem được trên mock.

**Preconditions:**
```text
1. A split payment of a fresh 50.00 invoice of STU-103 is ReconciliationRequired because the reversal failed. The invoice is PaymentPending.
```

**Test Data:**
```text
Student: STU-103 Marcus Tan, Singapore Citizen, EA Active, balance 20.00 SGD
```

**Test Steps:**
1. Open the invoice list as PAR-A.
2. Try to start a new payment for the invoice.
3. Send a create payment request with a new key.

**Expected Result:**
> 1. The invoice cannot be selected for a new payment.
>  2. The request is refused with 409 and the message "A payment for this invoice is still being processed."
>  3. No new transaction exists and no second EA debit is made.

**Actual Result:**
> Chạy trên bản Dev local function9_14-10-26, Chrome, 2026-10-15; dữ liệu mẫu khác R9 nên không xét. Khi ReconciliationRequired, invoice còn PaymentPending, màn kết quả không có nút thanh toán lại. Chưa mở lại danh sách phí sau tình huống này (ở tình huống online thất bại, khoản phí bị loại khỏi danh sách). Chưa thử gọi API checkout lại nên chưa xác nhận Expected 2 (409) và Expected 3.

---

#### `TC-142`: A session that ends before the confirm creates no transaction

- **Scenario ID**: `TS-024`
- **Test Suite**: F9.7 Result, receipt and retry
- **Page / Target**: `SCR-05 Review and confirm`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-09, PB-10, PB-11; FS F9: EX-02; 5.1 AUTH_REQUIRED
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-05
- **Assumption Reference**: ASM-R9-05: The portal session ends after 10 minutes of inactivity in SIT, or after the value Dev gives. The cases use the value that is configured.
- **Note**: xác nhận trace (EX-02, 5.1 AUTH_REQUIRED, ASM-R9-05). Chưa thử hết hạn session trên mock.

**Preconditions:**
```text
1. PAR-A is signed in and is on SCR-05 for a fresh 50.00 invoice of STU-101.
 2. The idle session timeout is known (value from Dev).
```

**Test Data:**
```text
Student: STU-101 Ethan Tan, Singapore Citizen, EA Active, balance 200.00 SGD
 Invoice: a fresh Issued invoice for STU-101, Net 50.00 SGD, created by the seed script just before the case
```

**Test Steps:**
1. Wait without activity until the session times out.
2. Confirm the payment.
3. Look at the screen, the transactions and the balance.

**Expected Result:**
> 1. The Parent sees "Your session has expired. Please sign in again." and is sent to the Singpass sign in.
>  2. No transaction is created and the EA balance is 200.00.

---

#### `TC-143`: A session that ends after the confirm does not stop the payment

- **Scenario ID**: `TS-024`
- **Test Suite**: F9.7 Result, receipt and retry
- **Page / Target**: `SCR-06 Pending`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Functional`
- **Traceability**: Tender R9; PB-09, PB-10, PB-11; FS F9: EX-02
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-02, ENV-R9-04, ENV-R9-05
- **Assumption Reference**: ASM-R9-05: The portal session ends after 10 minutes of inactivity in SIT, or after the value Dev gives. The cases use the value that is configured.
- **Note**: xác nhận trace (EX-02). UI mock: sau Close Browser, Refresh Status đưa về trang chủ chưa đăng nhập; đăng nhập lại thì invoice trả lại được và không thấy trạng thái hiện tại của payment (Expected 2).

**Preconditions:**
```text
1. PAR-A has confirmed an online payment of a fresh 75.00 invoice of STU-102 and is on the provider page.
```

**Test Data:**
```text
Student: STU-102 Chloe Tan, Permanent Resident, no Education Account
 Invoice: a fresh Issued invoice for STU-102, Net 75.00 SGD, created by the seed script just before the case
```

**Test Steps:**
1. Wait until the portal session times out while the provider page is open.
2. Finish the payment with the success outcome at the provider.
3. Sign in again as PAR-A and open the invoice.

**Expected Result:**
> 1. The transaction is still processed by the provider result: the leg is Succeeded and the invoice is Paid.
>  2. After the new sign in, the Parent sees the current state of the payment.

---

#### `TC-144`: A system error on confirm shows a safe message and changes no data

- **Scenario ID**: `TS-024`
- **Test Suite**: F9.7 Result, receipt and retry
- **Page / Target**: `SCR-05 Review and confirm`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Non-functional`
- **Traceability**: Tender R9; PB-09, PB-10, PB-11; FS F9: 5.1 SYSTEM_ERROR (no data change)
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-03, ENV-R9-05
- **Assumption Reference**: N/A
- **Note**: Needs a fault switch from Dev (ENV-R9-05).
 xác nhận trace. UI mock không có công tắc lỗi.

**Preconditions:**
```text
1. PAR-A is signed in and is on SCR-05 for a fresh 50.00 invoice of STU-101 with the EA method.
 2. A Function 9 service is set to return an error when the transaction is created.
```

**Test Data:**
```text
Student: STU-101 Ethan Tan, Singapore Citizen, EA Active, balance 200.00 SGD
 Invoice: a fresh Issued invoice for STU-101, Net 50.00 SGD, created by the seed script just before the case
```

**Test Steps:**
1. Confirm the payment.
2. Look at the screen, the transactions, the ledger and the invoice.

**Expected Result:**
> 1. The Parent sees "Something went wrong. Please try again later." and can try again.
>  2. No transaction is created, no debit is made and the invoice is still Issued.

---


### Test Suite: Data rules and constraints

#### `TC-145`: The seed data follows every invoice rule of BR-F9-12

- **Scenario ID**: `TS-025`
- **Test Suite**: Data rules and constraints
- **Page / Target**: `Database`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: Tender R9; PB-09, PB-10; FS F9: BR-F9-12; DA-11; 4.2 InvoiceItem
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-05
- **Assumption Reference**: N/A
- **Note**: Inference: the FS does not say the invoice amount is the sum of its lines. DA-05 describes an invoice made of lines.
 xác nhận trace (BR-F9-12, DA-11, 4.2 InvoiceItem). UI mock: tổng các dòng bằng số phải trả (38.00 cộng 23.98 bằng 61.98).

**Preconditions:**
```text
1. The Seed Data sheet is loaded in SIT.
```

**Test Data:**
```text
Seed Data sheet: invoices and invoice lines
```

**Test Steps:**
1. Run a check for lines whose school differs from the invoice school.
2. Run a check for repeated StudentChargeId.
3. Run a check for Net different from Gross minus Subsidy on invoices and lines.
4. Run a check for Net not above 0 on invoices that are not Draft.
5. Run a check for negative amounts, and for lines where Gross is not above 0 or Subsidy is not in the range 0 up to below Gross.

**Expected Result:**
> 1. Each check returns no rows.
>  2. The invoice amount equals the sum of its line amounts.

---

#### `TC-146`: An Issued invoice with Net 0.00 is refused and a Draft with Net 0.00 is accepted

- **Scenario ID**: `TS-025`
- **Test Suite**: Data rules and constraints
- **Page / Target**: `Database`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: Tender R9; PB-09, PB-10; FS F9: BR-F9-12; 4.2 Invoice NetAmount (Net above 0 when not Draft); NQ-16
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-05
- **Assumption Reference**: N/A
- **Note**: xác nhận

**Preconditions:**
```text
1. QA can write test rows in SIT.
```

**Test Data:**
```text
Invoice rows: status Issued with Net 0.00; status Draft with Net 0.00; status Issued with Net 0.01
```

**Test Steps:**
1. Insert the Issued invoice with Net 0.00.
2. Insert the Draft invoice with Net 0.00.
3. Insert the Issued invoice with Net 0.01.

**Expected Result:**
> 1. The Issued invoice with Net 0.00 is refused by the database.
>  2. The Draft invoice with Net 0.00 is accepted.
>  3. The Issued invoice with Net 0.01 is accepted.

---

#### `TC-147`: A line with Subsidy equal to Gross is refused and Subsidy just below Gross is accepted

- **Scenario ID**: `TS-025`
- **Test Suite**: Data rules and constraints
- **Page / Target**: `Database`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: Tender R9; PB-09, PB-10; FS F9: BR-F9-12; 4.2 InvoiceItem (0 <= Subsidy < Gross)
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-05
- **Assumption Reference**: N/A
- **Note**: xác nhận

**Preconditions:**
```text
1. QA can write test rows in SIT.
```

**Test Data:**
```text
Line rows: Gross 50.00 with Subsidy 50.00; Gross 50.00 with Subsidy 49.99; Gross 50.00 with Subsidy 0.00
```

**Test Steps:**
1. Insert the line with Subsidy 50.00.
2. Insert the line with Subsidy 49.99.
3. Insert the line with Subsidy 0.00.

**Expected Result:**
> 1. The line with Subsidy 50.00 is refused (Net would be 0.00).
>  2. The lines with Subsidy 49.99 and 0.00 are accepted with Net 0.01 and 50.00.

---

#### `TC-148`: A student charge cannot be placed on two invoices

- **Scenario ID**: `TS-025`
- **Test Suite**: Data rules and constraints
- **Page / Target**: `Database`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: Tender R9; PB-09, PB-10; FS F9: BR-F9-12; 4.2 InvoiceItem StudentChargeId (unique)
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-05
- **Assumption Reference**: ASM-R9-27: StudentChargeId stays unique across all invoices, including Cancelled ones.
- **Note**: xác nhận

**Preconditions:**
```text
1. QA can write test rows in SIT.
 2. Charge SC-TEST-01 is on a line of an Issued invoice. Charge SC-TEST-02 is on a line of a Cancelled invoice.
```

**Test Data:**
```text
StudentChargeId: SC-TEST-01, SC-TEST-02
```

**Test Steps:**
1. Insert a line of a new invoice with StudentChargeId SC-TEST-01.
2. Insert a line of a new invoice with StudentChargeId SC-TEST-02.

**Expected Result:**
> 1. Both inserts are refused as duplicates of StudentChargeId.

---

#### `TC-149`: A line from another school than the invoice is refused

- **Scenario ID**: `TS-025`
- **Test Suite**: Data rules and constraints
- **Page / Target**: `Database`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: Tender R9; PB-09, PB-10; FS F9: BR-F9-12; 4.2 Invoice SchoolId
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-05
- **Assumption Reference**: N/A
- **Note**: xác nhận

**Preconditions:**
```text
1. QA can write test rows in SIT.
```

**Test Data:**
```text
Invoice of SCH-01; line whose charge belongs to SCH-02
```

**Test Steps:**
1. Insert the line of SCH-02 into the invoice of SCH-01.

**Expected Result:**
> 1. The insert is refused because every line must belong to the school of the invoice.

---

#### `TC-150`: Negative amounts are refused

- **Scenario ID**: `TS-025`
- **Test Suite**: Data rules and constraints
- **Page / Target**: `Database`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: Tender R9; PB-09, PB-10; FS F9: BR-F9-12; 4.2 Invoice (amounts not negative)
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-05
- **Assumption Reference**: N/A
- **Note**: xác nhận

**Preconditions:**
```text
1. QA can write test rows in SIT.
```

**Test Data:**
```text
Rows with Gross -1.00, Subsidy -1.00 or Net -1.00
```

**Test Steps:**
1. Insert an invoice with a negative Gross.
2. Insert a line with a negative Subsidy.
3. Insert an invoice with a negative Net.

**Expected Result:**
> 1. Each insert is refused.

---

#### `TC-151`: Date fields follow the invoice status

- **Scenario ID**: `TS-025`
- **Test Suite**: Data rules and constraints
- **Page / Target**: `Database`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: Tender R9; PB-09, PB-10; FS F9: 4.2 Invoice (IssuedAt and DueDate required after issue; PaidAt only when Paid; CancelledAt only when Cancelled)
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-05
- **Assumption Reference**: N/A
- **Note**: xác nhận

**Preconditions:**
```text
1. QA can write test rows in SIT.
```

**Test Data:**
```text
Invoice rows: Issued without DueDate; Issued without IssuedAt; Issued with PaidAt; Paid with PaidAt; Cancelled with CancelledAt
```

**Test Steps:**
1. Insert the Issued invoice without a DueDate.
2. Insert the Issued invoice without an IssuedAt.
3. Insert the Issued invoice with a PaidAt.
4. Insert the Paid invoice with a PaidAt.
5. Insert the Cancelled invoice with a CancelledAt.

**Expected Result:**
> 1. The first three inserts are refused.
>  2. The last two inserts are accepted.

---

#### `TC-152`: The currency defaults to SGD

- **Scenario ID**: `TS-025`
- **Test Suite**: Data rules and constraints
- **Page / Target**: `Database`
- **Severity / Priority**: `S4 (lowest)` / `Low`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: Tender R9; PB-09, PB-10; FS F9: DA-10; 4.2 Invoice CurrencyCode
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-05
- **Assumption Reference**: N/A
- **Note**: xác nhận. UI mock hiển thị số tiền theo SGD.

**Preconditions:**
```text
1. QA can write test rows in SIT.
```

**Test Data:**
```text
Invoice row without CurrencyCode
```

**Test Steps:**
1. Insert an invoice without a CurrencyCode.
2. Read the saved row and the amounts on SCR-02.

**Expected Result:**
> 1. The saved CurrencyCode is SGD.
>  2. SCR-02 shows the amounts in SGD.

---

#### `TC-153`: A second open transaction for an invoice is refused by the database

- **Scenario ID**: `TS-026`
- **Test Suite**: Data rules and constraints
- **Page / Target**: `Database`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: Tender R9; PB-09, PB-10; FS F9: DA-13; BR-F9-09; 4.2 Transaction (unique index on InvoiceId when CompletedAt is empty)
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-05
- **Assumption Reference**: N/A
- **Note**: xác nhận

**Preconditions:**
```text
1. A fresh Issued invoice has one Pending transaction (CompletedAt empty).
```

**Test Data:**
```text
Invoice with one open transaction
```

**Test Steps:**
1. Insert a second transaction for the same invoice with CompletedAt empty.

**Expected Result:**
> 1. The insert is refused by the unique index for one open transaction per invoice.

---

#### `TC-154`: A second Succeeded transaction for an invoice is refused

- **Scenario ID**: `TS-026`
- **Test Suite**: Data rules and constraints
- **Page / Target**: `Database`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: Tender R9; PB-09, PB-10; FS F9: DA-13; BR-F9-04; 4.2 Transaction (unique index on InvoiceId when Status = Succeeded)
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-05
- **Assumption Reference**: N/A
- **Note**: xác nhận

**Preconditions:**
```text
1. A fresh invoice has one Succeeded transaction.
```

**Test Data:**
```text
Invoice with one Succeeded transaction
```

**Test Steps:**
1. Insert a second transaction for the same invoice with the status Succeeded.

**Expected Result:**
> 1. The insert is refused by the unique index for one successful transaction per invoice.

---

#### `TC-155`: An idempotency key is unique for a Parent and can repeat across Parents

- **Scenario ID**: `TS-026`
- **Test Suite**: Data rules and constraints
- **Page / Target**: `Database`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: Tender R9; PB-09, PB-10; FS F9: BR-F9-04; 4.2 Transaction IdempotencyKey (unique per InitiatedByUserId and key)
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-05
- **Assumption Reference**: N/A
- **Note**: xác nhận

**Preconditions:**
```text
1. Transaction T1 exists for Parent PAR-A with the key KEY-DB-01.
```

**Test Data:**
```text
Keys: KEY-DB-01 for PAR-A twice; KEY-DB-01 for PAR-D
```

**Test Steps:**
1. Insert a transaction for PAR-A with KEY-DB-01.
2. Insert a transaction for PAR-D with KEY-DB-01.

**Expected Result:**
> 1. The insert for PAR-A is refused.
>  2. The insert for PAR-D is accepted.

---

#### `TC-156`: A FundingReference is unique and a split uses two different references

- **Scenario ID**: `TS-026`
- **Test Suite**: Data rules and constraints
- **Page / Target**: `Database`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: Tender R9; PB-09, PB-10; FS F9: DA-12; 4.2 FundingLeg FundingReference (unique); Glossary Funding leg
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-02, ENV-R9-03, ENV-R9-05
- **Assumption Reference**: N/A
- **Note**: xác nhận trace. UI mock biên lai split hiện hai Ref dạng FND khác nhau, một cho EA và một cho Online.

**Preconditions:**
```text
1. A split payment of a fresh 50.00 invoice of STU-103 is finished.
```

**Test Data:**
```text
Student: STU-103 Marcus Tan, Singapore Citizen, EA Active, balance 20.00 SGD
```

**Test Steps:**
1. Read the FundingReference of the EA leg and of the online leg.
2. Insert a leg with the FundingReference of the EA leg.

**Expected Result:**
> 1. The two legs have different FundingReferences.
>  2. The EA reference is the one in the Function 1 ledger and the online reference is the one at the provider.
>  3. The duplicate insert is refused.

---

#### `TC-157`: Wallet and provider fields depend on the leg method

- **Scenario ID**: `TS-026`
- **Test Suite**: Data rules and constraints
- **Page / Target**: `Database`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: Tender R9; PB-09, PB-10; FS F9: 4.2 FundingLeg WalletId (required for method 1, forbidden for 2), ProviderCode (required for method 2)
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-05
- **Assumption Reference**: N/A
- **Note**: xác nhận

**Preconditions:**
```text
1. QA can write test rows in SIT.
```

**Test Data:**
```text
Leg rows: EA leg without WalletId; correct EA leg with WalletId; online leg with WalletId; online leg without ProviderCode; correct online leg with ProviderCode
```

**Test Steps:**
1. Insert each leg row.

**Expected Result:**
> 1. An EA leg without a WalletId is refused. An online leg with a WalletId is refused. An online leg without a ProviderCode is refused.
>  2. A correct EA leg with a WalletId and a correct online leg with a ProviderCode are accepted.

---

#### `TC-158`: Ledger and provider IDs are stored when they must be and are unique

- **Scenario ID**: `TS-026`
- **Test Suite**: Data rules and constraints
- **Page / Target**: `Database`
- **Severity / Priority**: `S2` / `High`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: Tender R9; PB-09, PB-10; FS F9: 4.2 FundingLeg (EducationAccountTransactionId, EducationAccountReversalTransactionId, ProviderTransactionId)
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-02, ENV-R9-03, ENV-R9-05
- **Assumption Reference**: N/A
- **Note**: xác nhận

**Preconditions:**
```text
1. A split payment finished with a failure of the online part and a reversed EA leg, and a separate successful online payment, are available.
```

**Test Data:**
```text
Legs: EA leg Succeeded; EA leg Reversed; online leg Succeeded
```

**Test Steps:**
1. Read EducationAccountTransactionId on the Succeeded EA leg.
2. Read EducationAccountReversalTransactionId on the Reversed EA leg.
3. Read ProviderTransactionId on the Succeeded online leg.
4. Insert a leg that repeats one of these IDs.

**Expected Result:**
> 1. The Succeeded EA leg has a ledger ID. The Reversed EA leg has a reversal ID. The Succeeded online leg has a ProviderTransactionId.
>  2. The duplicate IDs are refused.

---

#### `TC-159`: Leg amounts add up to the transaction and the transaction equals the invoice Net

- **Scenario ID**: `TS-026`
- **Test Suite**: Data rules and constraints
- **Page / Target**: `Database`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: Tender R9; PB-09, PB-10; FS F9: BR-F9-13; BR-F9-11; 4.2 Transaction and FundingLeg amounts
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-02, ENV-R9-03, ENV-R9-05
- **Assumption Reference**: N/A
- **Note**: xác nhận

**Preconditions:**
```text
1. A split payment of EA 20.00 and online 30.00 for a fresh 50.00 invoice of STU-103 has Succeeded.
```

**Test Data:**
```text
Student: STU-103 Marcus Tan, Singapore Citizen, EA Active, balance 20.00 SGD
```

**Test Steps:**
1. Read the Requested and Settled amounts of the invoice, the transaction and the two legs.

**Expected Result:**
> 1. The leg Requested amounts are 20.00 and 30.00 and add up to the transaction Requested amount 50.00.
>  2. The transaction Requested amount equals the invoice Net 50.00.
>  3. For the Succeeded transaction Settled equals Requested.

---

#### `TC-160`: An amount other than the invoice Net cannot be requested

- **Scenario ID**: `TS-026`
- **Test Suite**: Data rules and constraints
- **Page / Target**: `API: create payment`
- **Severity / Priority**: `S1 (highest)` / `Critical`
- **Execution Status**: `Not Run` | **Test Type**: `API`
- **Traceability**: Tender R9; PB-09, PB-10; FS F9: BR-F9-13; DA-07; OOS 2; 4.2 Invoice Status (1 to 5)
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-05, ENV-R9-06
- **Assumption Reference**: N/A
- **Note**: xác nhận

**Preconditions:**
```text
1. PAR-A has a valid session.
 2. A fresh 50.00 invoice of STU-101 is Issued.
```

**Test Data:**
```text
Student: STU-101 Ethan Tan, Singapore Citizen, EA Active, balance 200.00 SGD
 Invoice: a fresh Issued invoice for STU-101, Net 50.00 SGD, created by the seed script just before the case
 Requested amount sent: 25.00
```

**Test Steps:**
1. Send the create payment request with the amount 25.00.
2. Look at the answer and the transactions.
3. Look for a PartiallyPaid status or a PaidAmount in the invoice data.

**Expected Result:**
> 1. No transaction is created with a Requested amount other than 50.00.
>  2. The invoice has no PartiallyPaid status and no PaidAmount.
>  3. The invoice is Paid only when a payment of the full 50.00 succeeds.

---

#### `TC-161`: Settled above Requested and a leg amount of zero are refused

- **Scenario ID**: `TS-026`
- **Test Suite**: Data rules and constraints
- **Page / Target**: `Database`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: Tender R9; PB-09, PB-10; FS F9: 4.2 Transaction (0 <= Settled <= Requested), FundingLeg (Requested above 0)
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-05
- **Assumption Reference**: N/A
- **Note**: xác nhận

**Preconditions:**
```text
1. QA can write test rows in SIT.
```

**Test Data:**
```text
Transaction rows: Requested 50.00 with Settled 50.01; leg row with Requested 0.00
```

**Test Steps:**
1. Insert the transaction with Settled 50.01.
2. Insert the leg with Requested 0.00.

**Expected Result:**
> 1. Both inserts are refused.

---

#### `TC-162`: CompletedAt is empty while processing and filled when the transaction is final

- **Scenario ID**: `TS-026`
- **Test Suite**: Data rules and constraints
- **Page / Target**: `Database`
- **Severity / Priority**: `S3` / `Medium`
- **Execution Status**: `Not Run` | **Test Type**: `Integration`
- **Traceability**: Tender R9; PB-09, PB-10; FS F9: 4.2 Transaction CompletedAt; DA-13
- **Environment**: SIT
 Chrome (latest)
 Build: to be recorded at execution
 Needs: ENV-R9-01, ENV-R9-02, ENV-R9-03, ENV-R9-05
- **Assumption Reference**: N/A
- **Note**: xác nhận

**Preconditions:**
```text
1. A split payment is in progress with the online leg Pending.
```

**Test Data:**
```text
Student: STU-103 Marcus Tan, Singapore Citizen, EA Active, balance 20.00 SGD
```

**Test Steps:**
1. Read CompletedAt of the transaction and of the legs while the online leg is Pending.
2. Finish the payment with the success outcome.
3. Read CompletedAt again.

**Expected Result:**
> 1. While processing, CompletedAt of the transaction is empty.
>  2. After the success, CompletedAt of the transaction and of each leg is filled.

---
