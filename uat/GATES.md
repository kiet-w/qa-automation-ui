# Sprint 3 UAT — Cổng Kiểm Soát & Giả Định (Gates & Working Assumptions)

> Only a listed test is blocked by its gate. Other tests use the latest explicitly agreed rule and record it; where no rule is agreed, the observation is conditional. Build, accounts and acceptance authority sit in Readiness.

## 1. Bốn Cổng Kiểm Soát (4 Gates)

| Cổng (Gate) | Nội Dung Cần Quyết Định | Nguồn (From) | Phụ Trách | Các Ca Bị Ảnh Hưởng | Trạng Thái | Nghị Quyết (Resolution) |
| :---: | :--- | :---: | :--- | :--- | :---: | :--- |
| **G1** | Top-up contract and recovery. Settle search, amount, retry versus repeat, correction, scheduling and failed-only recovery. | D01, D02 | Josh with BA, Hugh, Kevin and business representative | `UAT-022, UAT-023, UAT-024, UAT-025, UAT-026, UAT-027` | `Open` |  |
| **G2** | Lifecycle and CPF. Settle age and citizenship, closure, pending transactions, Government failure and simulator outcomes. | D03 | Josh with BA and Kevin/Hugh | `UAT-001, UAT-002, UAT-003, UAT-004, UAT-006, UAT-PAR-01-E1, UAT-MOE-01, UAT-PAR-01, UAT-022` | `Open` |  |
| **G3** | FAS routing and decision rights. Settle timing, HQ versus school decisions, scheme routing, duplicate and finality rules, and cross-school siblings. | D04 | Gavin with Kent, Howard and BA | `UAT-008, UAT-028, UAT-029, UAT-047, UAT-049, UAT-SCH-01, UAT-SCH-01-N1, UAT-SCH-01-E1, UAT-PAR-02, UAT-PAR-02-N1, UAT-PAR-02-N2, UAT-PAR-02-E1, UAT-PAR-02-E2, UAT-PAR-02-A1, UAT-PAR-02-N3, UAT-PAR-02-A2, UAT-PAR-02-N4, UAT-031, UAT-033, UAT-035, UAT-MOE-06, UAT-MOE-06-N1, UAT-SCH-02, UAT-SCH-02-N1, UAT-SCH-03, UAT-SCH-03-N1, UAT-040, UAT-MOE-05-E1, UAT-SCH-04-E1, UAT-045, UAT-046, UAT-048` | `Open` |  |
| **G4** | School and fee dates. Settle transfer and enrolment dates, rate periods, publication replay, CSV row behavior and optional classes. | D10 | Kent and Chan with BA and Nito/Tyson | `UAT-016, UAT-017, UAT-018, UAT-020, UAT-021, UAT-MOE-01, UAT-045` | `Open` |  |

## 2. Giả Định Đang Áp Dụng (Working Assumptions - Chưa Phê Duyệt Chính Thức)

- Working assumptions, not approved
- Baseline: the latest explicitly agreed rule is used for every ungated test. Record the decision, approver, date and source in Evidence or defect. A newer draft does not replace an agreement.
- D05 Budget unapproved: period, editing, counting, remaining and warn/block policy require an explicitly agreed decision. Warning-only is a draft assumption, not approval. Affected: UAT-028, UAT-049, UAT-PAR-02, UAT-PAR-02-A1, UAT-PAR-02-A2, UAT-031, UAT-033, UAT-035, UAT-SCH-02, UAT-SCH-03, UAT-038, UAT-039, UAT-040, UAT-MOE-04, UAT-MOE-05, UAT-MOE-05-E1, UAT-SCH-04, UAT-SCH-04-E1, UAT-045, UAT-046.
- D06 FAS unapproved: household membership, income sources, document limits/optionality, caps and rounding require a recorded rule. Government GHI 2400 / four people is baseline data only; a separate 2000 + declared 400 variant runs only if approved.
- D07 View As: read-only is a working assumption. The source still calls it a draft proposal.
- D08 FAQ: use the draft answer bank once approved. If it is missing, block the test.
- Delivery and acceptance facts (D09) sit in Readiness.
