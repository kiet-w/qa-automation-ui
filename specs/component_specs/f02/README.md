# F02: Top-Up Management Specification Summary

## 1. Overview & Architectural Role
Function 2 (`f02`) governs all Education Account credit operations within EAFAMS, comprising Individual Top-Up credits (`SCR-01` to `SCR-04`), Top-Up History and Spending Audit (`SCR-05`), and Bulk Campaign Lifecycle Management (`SCR-07` to `SCR-12`). All operations are strictly restricted to the `MOE HQ User` role (`BR-F2-01`), with idempotent execution guarantees (`BR-F2-05`, `BR-F2-27`).

---

## 2. Directory Structure & Spec Manifest

```text
specs/component_specs/f02/
├── README.md
├── atomic/
│   ├── ea_search_lookup.md         # F02-COMP-EA-SEARCH: SCR-01 Find EA by exact Number or NRIC
│   ├── topup_amount_reason_form.md # F02-COMP-AMOUNT-REASON: SCR-02 Verify owner & Amount/Reason
│   ├── topup_confirm_dialog.md     # F02-COMP-CONFIRM-DIALOG: SCR-03 Review & Idempotent Confirm
│   ├── topup_history_table.md      # F02-COMP-HISTORY-TABLE: SCR-05 History table & Summary metrics
│   ├── campaign_criteria_config.md # F02-COMP-CAMPAIGN-CONFIG: SCR-08 6 OR-criteria configuration
│   ├── campaign_preview_confirm.md # F02-COMP-CAMPAIGN-PREVIEW: SCR-09 Preview table & Confirm
│   └── run_summary_item_grid.md    # F02-COMP-RUN-GRID: SCR-11/12 Runs list, items & Stop/Retry
└── integration/
    ├── individual_topup_flow.md     # F02-INT-FLOW-01: End-to-end individual credit lifecycle
    └── bulk_campaign_dispatch_flow.md# F02-INT-FLOW-02: End-to-end bulk campaign batch execution
```

---

## 3. Component & Flow Mapping

| Spec File | Screen Code | Route / Endpoint | Primary Function | Traceable Rules |
| :--- | :--- | :--- | :--- | :--- |
| `atomic/ea_search_lookup.md` | `SCR-01` | `/admin/top-up/individual` | Exact EA / NRIC search | `BR-F2-01`, `BR-F2-02`, `MSG-0201` |
| `atomic/topup_amount_reason_form.md` | `SCR-02` | `/admin/top-up/individual/verify` | Amount ($>0.00$) & Reason input | `BR-F2-03`, `BR-F2-04`, `MSG-0202`, `MSG-0204`, `MSG-0206` |
| `atomic/topup_confirm_dialog.md` | `SCR-03` | Modal Dialog | Single-click confirm & Idempotency | `BR-F2-05`, `EX-02`, `EX-04`, `MSG-0002` |
| `atomic/topup_history_table.md` | `SCR-05` | `/admin/top-up/history` | Audit log & Total spending summary | `BR-F2-07`, `BR-F2-30`, `EX-05` |
| `atomic/campaign_criteria_config.md` | `SCR-08` | `/admin/top-up/campaigns/new` | 6 OR-criteria configuration | `BR-F2-14` to `BR-F2-18`, `MSG-0215`, `MSG-0217`, `MSG-0221` |
| `atomic/campaign_preview_confirm.md` | `SCR-09` | `/admin/top-up/campaigns/:id/preview` | Forecast table & Confirm dispatch | `BR-F2-19` to `BR-F2-22`, `MSG-0214`, `MSG-0216`, `MSG-0222` |
| `atomic/run_summary_item_grid.md` | `SCR-11/12`| `/admin/top-up/runs/:id` | Batch monitoring, Stop & Retry | `BR-F2-23`, `BR-F2-26` to `BR-F2-29` |
| `integration/individual_topup_flow.md` | `SCR-01..05` | Full User Journey | Individual credit from search to ledger | `BR-F2-01..07`, `EX-01..06` |
| `integration/bulk_campaign_dispatch_flow.md` | `SCR-07..12` | Batch Pipeline | Wizard setup, chunked run, stop/retry | `BR-F2-13..29`, `EX-07..11` |

---

## 4. Key Business Rules & Quality Gates
1. **Zero Over-crediting via Idempotency (`BR-F2-05`, `BR-F2-27`)**:
   - Every individual top-up and run item possesses a unique, client-generated `FundingReference`. Retries strictly reuse the existing reference, ensuring Function 1 rejects duplicates.
2. **6 OR-Criteria Combination Model (`BR-F2-14`)**:
   - Bulk campaign targets are selected using 6 modular criteria (Age Range, Balance, Schooling Status, School, Academic Level, Class) combining with logical OR. If an account matches multiple criteria, it receives exactly one credit.
3. **Ascending Chunk Execution (`BR-F2-24`)**:
   - Accounts are processed in ascending order of Account Number in small chunks. The Closure Eligibility check runs immediately before crediting each chunk.
4. **Resilience & Stop Governance (`BR-F2-23`)**:
   - Stopping a running batch gracefully allows the active slot to complete while cleanly marking all pending queue items with code `RUN_STOPPED`.
