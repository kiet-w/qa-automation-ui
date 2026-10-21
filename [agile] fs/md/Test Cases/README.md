# Sprint 1 Test Cases & Defect Catalog

Single source of truth for all automated and manual Test Cases and Defect logs executed during Sprint 1 for the MOE Education Account & Fee Management System (EAFAMS).

## 📚 Module Test Suites

| Module | Document | Scope | Total TCs | Defect Count |
| :--- | :--- | :--- | :--- | :--- |
| **R1: Education Account Lifecycle** | [`TC_R1_Education_Account_Lifecycle.md`](file:///home/baudui/Projects/automation-ui/%5Bagile%5D%20fs/md/Test%20Cases/TC_R1_Education_Account_Lifecycle.md) | Age 7 auto-creation, age 16 closure, sync audit, duplicate prevention, wallet & ledger rules | 73 | 1 (Template) |
| **R3: School, Student & Fee Master** | [`TC_R3_School_Student_Fee_Management.md`](file:///home/baudui/Projects/automation-ui/%5Bagile%5D%20fs/md/Test%20Cases/TC_R3_School_Student_Fee_Management.md) | School setup, academic levels, classes, fee catalog, fee pricing, publication & charges | 105 | 5 (Open) |
| **R8: Parent Portal & Profile** | [`TC_R8_Parent_Portal_SingPass_Profile.md`](file:///home/baudui/Projects/automation-ui/%5Bagile%5D%20fs/md/Test%20Cases/TC_R8_Parent_Portal_SingPass_Profile.md) | SingPass authentication, home dashboard, parent details update, child link, audit log | 125 | 5 (Open) |
| **R9: Outstanding Fees & Payment** | [`TC_R9_Outstanding_Fees_and_Payment.md`](file:///home/baudui/Projects/automation-ui/%5Bagile%5D%20fs/md/Test%20Cases/TC_R9_Outstanding_Fees_and_Payment.md) | Invoice access, EA payment, online payment, split payment, idempotency, retry, receipts | 162 | 3 (Open) |
| **Defects Master Log** | [`DEFECTS_Sprint_1_Master.md`](file:///home/baudui/Projects/automation-ui/%5Bagile%5D%20fs/md/Test%20Cases/DEFECTS_Sprint_1_Master.md) | All known defects across R1, R3, R8, R9 with steps to reproduce, expected results & xfail syntax | - | 14 total |
| **Master Workbook Raw Table** | [`Test Cases + Defect sprint 1.md`](file:///home/baudui/Projects/automation-ui/%5Bagile%5D%20fs/md/Test%20Cases%20%2B%20Defect%20sprint%201.md) | Complete unedited multi-sheet tabular view exported directly from Google Sheets | 465 | 14 |

---

## 🎯 Traceability & Invariant Guidelines
Per **`AGENTS.md`**:
- **Invariant 3 (Test Case Identification & Traceability)**: Every test function must be named `test_tc_<scenario_id>_...` matching the corresponding TC or Scenario ID from these documents.
- **Invariant 5 (Verification-First Bug Handling)**: Open bugs listed in `DEFECTS_Sprint_1_Master.md` must be decorated with `@pytest.mark.xfail(strict=True, reason="BUG-xxx: <description>")`.
- **Invariant 6 (Zero Assumptions)**: Assertions and data parameters MUST cite the exact Test Case ID and Expected Result from these markdown files.
