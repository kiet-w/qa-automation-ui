# F04: Assess FAS & Apply Subsidies Specification Summary

## 1. Overview & Architectural Role
Function 4 (`f04`) manages the Financial Assistance Scheme (FAS) assessment and subsidy allocation within EAFAMS, comprising School-Based FAS (`SBFAS`) administered by School Admins, national MOE FAS (`MOEFAS`) administered by MOE HQ Users, an automated AI/ML Need Score Recommendation Engine, and Scheme Configuration with Overlap Prevention and Retroactive Fee Subsidies.

---

## 2. Directory Structure & Spec Manifest

```text
specs/component_specs/f04/
├── README.md
├── atomic/
│   ├── fas_applications_table_filter.md  # F04-COMP-APP-LIST: Screen A/B List, summary KPI cards & filters
│   ├── fas_review_drawer.md              # F04-COMP-REVIEW-DRAWER: Screen C/D Household profile & PDF viewer
│   ├── ml_need_score_gauge.md            # F04-COMP-ML-GAUGE: Screen L AI Need Score & Hard Deny Rules
│   ├── fas_decision_dialogs.md           # F04-COMP-DECISION-DIALOGS: Screen E/F Approve & Screen G Reject
│   └── fas_scheme_wizard.md              # F04-COMP-SCHEME-WIZARD: Screen H-K Scheme wizard & Add Fee dialog
└── integration/
    ├── fas_application_assessment_flow.md # F04-INT-FLOW-01: End-to-end review & approval journey
    ├── ml_need_score_evaluation_flow.md   # F04-INT-FLOW-02: AI scoring & Deny rules execution pipeline
    └── scheme_configuration_subsidy_application_flow.md # F04-INT-FLOW-03: Scheme publish & retroactive fees
```

---

## 3. Component & Flow Mapping

| Spec File | Screen Code | Route / Endpoint | Primary Function | Traceable Rules |
| :--- | :--- | :--- | :--- | :--- |
| `atomic/fas_applications_table_filter.md` | `Screen A & B` | `/admin/fas/applications` | Applications list & filters | `BR13`, `BR14`, `BR16`, `T24..29` |
| `atomic/fas_review_drawer.md` | `Screen C & D` | Drawer overlay | Household GHI/PCI & PDF docs | `FS 3.1`, `FS 3.5`, `FS 4.1`, `T32` |
| `atomic/ml_need_score_gauge.md` | `Screen L / C5`| Embedded Widget | Score 0-100 & Hard Deny Rules | `FS 7.2`, `FS 14.1..2`, `TC-249..263` |
| `atomic/fas_decision_dialogs.md` | `Screen E, F, G`| Modal Dialogs | Approve Tier 1/2 & Reject | `VR-REJ-01`, `T30`, `T31` |
| `atomic/fas_scheme_wizard.md` | `Screen H, I, J, K`| `/admin/fas/schemes` | Scheme setup & Fee waivers | `VR-PUB-01..04`, `VR-FEE-01..06` |
| `integration/fas_application_assessment_flow.md` | `Screen A..G` | Review Flow | Review, AI evaluation & decision | `FS 3.1..4.2`, `TC-24` to `TC-32` |
| `integration/ml_need_score_evaluation_flow.md` | `Screen L` | Scoring Engine | Deny rules & weighted calculation | `FS 7.2`, `TC-256..263` |
| `integration/scheme_configuration_subsidy_application_flow.md` | `Screen H..K` | Scheme Pipeline | Overlap check & Retroactive fee | `VR-PUB-01..04`, `VR-FEE-04..06` |

---

## 4. Key Business Rules & Quality Gates
1. **School Admin Role Boundary (`BR14`)**:
   - A School Admin can only view and decide SBFAS applications belonging to students actively enrolled in their own school. Attempting to view applications from another school returns: *"You do not have access to this application."*
2. **Hard Deny Rules Pre-screen (`FS 14.1`)**:
   - Applications with inconsistent household data (e.g. 0 school-age children, workers exceeding household members, negative months) immediately yield a Need Score of `0.00`, both tiers Ineligible, and display an explicit audit flag banner.
3. **Mandatory Rejection Remarks (`VR-REJ-01`)**:
   - When rejecting an application, entering rejection remarks with a minimum of 15 characters is strictly mandatory before the confirmation button unlocks.
4. **Immediate Retroactive Fee Waivers (`VR-FEE-06`)**:
   - Adding a fee component to an active scheme immediately triggers a batch recalculation across all enrolled student charges without requiring manual recalculation runs.
