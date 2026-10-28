# F01: Education Account Lifecycle Specification Summary

## 1. Overview & Architectural Role
Function 1 (`f01`) governs the automated lifecycle of the Singapore Education Account within EAFAMS, covering citizen data ingestion, account initialization upon turning 7 years old, daily incremental synchronization, age-based closure upon turning 16, deferred balance handling, and lifecycle monitoring via the MOE HQ Admin Portal (`SCR-ADM-01`).

---

## 2. Directory Structure & Spec Manifest

```text
specs/component_specs/f01/
├── README.md
├── atomic/
│   ├── student_citizen_search_filter.md  # F01-COMP-SEARCH-FILTER: Search Bar, Status & Age Filters
│   ├── ea_account_table_pagination.md    # F01-COMP-TABLE-PAGINATION: Master Accounts Table & Paging
│   ├── ea_lifecycle_drawer.md            # F01-COMP-LIFECYCLE-DRAWER: Timeline Event Log & History
│   └── sync_job_status_card.md           # F01-COMP-SYNC-METRICS: Metric KPI Cards & Sync Banner
└── integration/
    ├── account_lifecycle_creation_flow.md   # F01-INT-FLOW-01: Auto-Creation & Citizen Sync
    └── account_closure_and_deferred_flow.md # F01-INT-FLOW-02: Age 16 Closure & Deferred Balance
```

---

## 3. Component & Flow Mapping

| Spec File | Type | Target Screen / Route | Primary Actor | Traceable Rules & ACs |
| :--- | :--- | :--- | :--- | :--- |
| `atomic/student_citizen_search_filter.md` | Atomic | `/admin/ea-lifecycle` (SCR-ADM-01) | MOE HQ User | `F01-BR01`, `F01-BR02`, `F01-AC01`, `F01-AC03`, `ASM-15` |
| `atomic/ea_account_table_pagination.md` | Atomic | `/admin/ea-lifecycle` (SCR-ADM-01) | MOE HQ User | `F01-AC01`, `F01-AC06`, `F02-BR01`, `F02-BR08`, `D-20` |
| `atomic/ea_lifecycle_drawer.md` | Atomic | `/admin/ea-lifecycle` (SCR-ADM-01) | MOE HQ User | `F01-BR02`, `F02-BR01`, `F02-BR08`, `F02-BR09`, `F02-AC06` |
| `atomic/sync_job_status_card.md` | Atomic | `/admin/ea-lifecycle` (SCR-ADM-01) | MOE HQ User | `F01-AC02`, `F01-AC11`, `F01-AC13`, `2.4 (Audit)` |
| `integration/account_lifecycle_creation_flow.md` | Integration | Cron Job & API `/api/sync/citizen` | System / Cron | `F01-BR01` to `F01-BR05`, `F01-AC01` to `F01-AC14`, `F01 EF01-EF04` |
| `integration/account_closure_and_deferred_flow.md`| Integration | Read Backend `/api/accounts/{id}` | System / Parent | `F02-BR01` to `F02-BR09`, `F02-AC01` to `F02-AC10`, `F02 EF01-EF04` |

---

## 4. Key Business Rules & Quality Gates
1. **Age 7 to Under-16 Rule (`F01-BR02`)**:
   - Accounts are created strictly for Singapore Citizens starting on their 7th birthday until before their 16th birthday.
2. **Backend-Triggered Closure on Access (`F02-BR02`)**:
   - Accounts are not closed by a timer; closure is evaluated synchronously upon any backend access or transaction attempt once the student is 16.
3. **Closure-Deferred Balance Rule (`1.2.7 WA`)**:
   - Accounts with a balance $> 0.00$ SGD cannot be closed without a valid CPF transfer destination; they transition to `Closure Deferred` and block all further transactions.
4. **Zero Tolerance for Raw i18n Keys**:
   - No untranslated UI strings (`features.ea.*`) or unhandled nulls are permitted in UI automation tests.
