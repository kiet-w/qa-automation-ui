# FS-04: Financial Assistance Scheme - FAS & AI Scoring (Requirement 4)

> **Phân hệ**: Admin Portal (MOE HQ & School Users)  
> **Requirement**: R4 – Financial Assistance Scheme (FAS)  
> **Product Backlog**: PB-17, PB-19, PB-25 (Sprint 3) | **User Story**: US-05, US-AI1  
> **Phiên bản baseline**: Official FSD Baseline (Agile FS.docx - Version 1.1 @Huy)  
> **Trạng thái**: Production Ready / Fully Aligned  

---

Oct 18, 2026 · Version 1.1 · @Huy

Function 4 lets School Admin and MOE HQ view FAS applications (MOEFAS and SBFAS), review them and make the final decision. An approved subsidy is applied to the student's EA fees. A rule-based scoring engine (FAS Scoring & Decision Engine) gives each application a Need Score, a suggested tier and a risk level to help the reviewer. It does not decide.

Highlight: yellow = changed from v1.0, green = new in v1.1.

| Item | Detail |
| :--- | :--- |
| Function | F4 – FAS applications |
| Project | Education Account (EA) and FAS website |
| Portal | Admin Portal |
| Users | School Admin, MOE HQ |
| Version | 1.1 |
| Related functions | F5 Upload applications, FAS schemes (scheme setup), F6 Budget & statistics (MOEFAS budget), FAS Scoring & Decision Engine (FASScoreEngine, README 2026-10-14) |

## 1. Introduction

### 1.1 Scope

| In scope | Out of scope |
| :--- | :--- |
| Application list, filters, tabs, summary cards | Uploading paper applications (F5) |
| Review drawer | Creating and editing schemes (FAS schemes) |
| Approve and reject | Parent e-Service Portal screens |
| System updates after a decision | Setting the budget (F6) |
| ML assessment shown to the reviewer (Need Score, suggested tier, risk) | Training a machine-learning model (the engine is rule-based and deterministic) |

### 1.2 Users and access

| Role | What they can do |
| :--- | :--- |
| School Admin | See SBFAS applications of their own school only. Approve or reject them. Only School Admin decides SBFAS. |
| MOE HQ | See all applications of all schools. Give the final decision on MOEFAS. SBFAS applications are view only for MOE HQ. |

MOEFAS applications and income details are visible to MOE HQ only.

### 1.3 Terms

| Term | Meaning |
| :--- | :--- |
| EA | Education Account |
| FAS | Financial Assistance Scheme |
| MOEFAS | FAS for Singapore Citizens. Final decision by MOE HQ. |
| SBFAS | School-based FAS for Citizens and PRs. Decided by School Admin of the student's school. |
| GHI | Gross household income per month |
| PCI | Per capita income = GHI / household size |
| Tier | Level of subsidy: Tier 1 (High need, full), Tier 2 (Medium need, partial), Tier 3 (Low need, partial) |
| System check | Pass or Fail of the MOEFAS eligibility criteria from the active scheme. Information only. |
| Need Score | 0–100 score from the FAS Scoring Engine. Higher = more need. See section 5. |
| Base Tier / Adjusted Tier | Base Tier: from statutory GHI/PCI thresholds. Adjusted Tier: from the Need Score. |
| ML risk | Low, Medium or High: how likely the family is to have difficulty paying the remaining fees. |
| Fast-track | The household received public support in the last 3 months. |

## 2. Process flow and statuses

### 2.1 Flow

| Step | MOEFAS | SBFAS |
| :--- | :--- | :--- |
| 0 | Application is submitted (Online by parent, or Paper uploaded by school). A student who is not a Singapore Citizen cannot get MOEFAS: the application is created as SBFAS for the school directly. All other applications start as MOEFAS. | Application is submitted (Online by parent, or Paper uploaded by school). A student who is not a Singapore Citizen cannot get MOEFAS: the application is created as SBFAS for the school directly. All other applications start as MOEFAS. |
| 1 | System runs the eligibility check and saves Pass or Fail for each criterion. The scoring engine computes the Need Score, suggested tier and risk. | Same |
| 2 | Status is Pending. Waits for MOE HQ. Pass and Fail both wait (no automatic approval or rejection). | Status is Pending. Waits for School Admin of the student's school. |
| 3 | MOE HQ approves or rejects. This is the final decision. Approve checks the MOEFAS budget left (BR17). | School Admin approves or rejects. This is the final decision. |
| 4 | If rejected and "Also consider for SBFAS" is Yes: a new SBFAS application is created (Pending) and goes to the school. If No: the application closes as Rejected and the parent gets an email. | End |

### 2.2 Statuses

| Status | Meaning | Next status |
| :--- | :--- | :--- |
| Pending | Waiting for a decision | Approved, Rejected |
| Approved | Subsidy granted with a Tier | None (final) |
| Rejected | Subsidy not granted, with a Reason | None (final) |

No other status is shown on screen (no "Auto-granted", "Pending MOE" or "Pending school").

## 3. Screen: FAS applications list

Menu path: Financial assistance > FAS applications. The page opens on the Pending tab.

### 3.1 School Admin view

Figure: School Admin – FAS applications list (Pending tab)

| # | Element | Type | Behaviour |
| :--- | :--- | :--- | :--- |
| 1 | Export | Button | Downloads a CSV of the filtered list (see 3.4). |
| 2 | Summary cards | Cards | Pending (SBFAS waiting for the school), SBFAS approved (this year), SBFAS rejected (this year). Counts for the user's school. Not affected by filters. |
| 3 | Tabs | Tabs | Pending (default), All, Approved, Rejected. Each tab shows its count when above 0. |
| 4 | Search | Text box | Matches student name, NRIC/FIN or Application ID. Contains, not case sensitive. |
| 5 | Filters | Dropdowns | Level, Class, Source, Tier, Status, ML risk, Submitted. See 3.3. |
| 6 | Table header | Columns | Application, Student, Class, Source, Submitted, ML suggestion, ML risk, Tier, Status. See 3.4. |
| 7 | Review / View | Button | Opens the review drawer (section 4). Review for Pending, View for other statuses. |
| 8 | Footer | Text and pages | Shows "Showing X–Y of Z" and page numbers. 10 rows per page. |

### 3.2 MOE HQ view

Figure: MOE HQ – FAS applications list (Pending tab)

| # | Element | Type | Behaviour |
| :--- | :--- | :--- | :--- |
| 1 | Export | Button | Downloads a CSV of the filtered list (see 3.4). |
| 2 | Summary cards | Cards | Total applications, Pending MOEFAS, Pending SBFAS, Approved, Rejected. All schools. Not affected by filters. |
| 3 | Tabs | Tabs | Pending (default), All, Approved, Rejected. Each tab shows its count when above 0. Pending shows MOEFAS and SBFAS waiting for a decision. |
| 4 | Search | Text box | Same as School Admin. |
| 5 | Filters | Dropdowns | School, Scheme, Level, Source, Tier, Status, ML risk, Submitted. See 3.3. |
| 6 | Table header | Columns | Application, Student, School, Scheme, Source, Submitted, System check, ML recommendation, ML risk, Tier, Status. See 3.4. |
| 7 | Review / View | Button | Review for Pending MOEFAS. View for SBFAS (any status) and decided MOEFAS. |
| 8 | Footer | Text and pages | Same as School Admin. |

### 3.3 Filters

Filters combine with AND. Changing a filter goes back to page 1.

| Filter | Values | School Admin | MOE HQ |
| :--- | :--- | :--- | :--- |
| School | List of schools | No | Yes |
| Scheme | MOEFAS, SBFAS | No | Yes |
| Level | Levels of the school (School Admin) or of all schools (MOE HQ) | Yes | Yes |
| Class | Classes of the school (filtered by Level) | Yes | No |
| Source | Online, Paper | Yes | Yes |
| Tier | School Admin: tiers of the school's SBFAS schemes. MOE HQ: MOEFAS, SBFAS – Tier 1/2/3. Decided applications match on their tier; Pending applications match on the ML suggested tier. | Yes | Yes |
| Status | Pending, Approved, Rejected | Yes | Yes |
| ML risk | Low, Medium, High | Yes | Yes |
| Submitted | Last 7 days, Last 30 days (default), Any time | Yes | Yes |

### 3.4 Table columns

| Column | School Admin | MOE HQ | Notes |
| :--- | :--- | :--- | :--- |
| Application | Yes | Yes | Application ID |
| Student | Yes | Yes | Name, with NRIC/FIN under it |
| School | No | Yes |  |
| Class | Yes | No |  |
| Scheme | No | Yes | MOEFAS or SBFAS |
| Source | Yes | Yes | Online or Paper |
| Submitted | Yes | Yes | DD/MM/YYYY |
| System check | No | Yes | MOEFAS: Pass if all criteria pass, otherwise Fail. SBFAS: "—". |
| ML recommendation / ML suggestion | Yes (ML suggestion) | Yes (ML recommendation) | See 5.4. MOEFAS rows: "Grant · Tier X", "Borderline" or "Do not grant". SBFAS rows: "Tier X · High/Medium/Low need" or "Reject". |
| ML risk | Yes | Yes | Low, Medium or High (5.3) |
| Tier | Yes | Yes | Shown when Approved, otherwise empty |
| Status | Yes | Yes | Pending, Approved or Rejected |

CSV export columns: Application, Student, NRIC, School/Class, Scheme, Source, Submitted, System check, ML, ML risk, Tier, Status.

### 3.5 List behaviour

Sort: Submitted, newest first.

Empty result: "No applications found."

Review shows only to users who can decide that application (see 2.1). Others see View.

Note under the MOE HQ list: "System check and ML are information only; MOE HQ decides MOEFAS. SBFAS is decided by each school (view only here)."

## 4. Screen: Review drawer

Review or View opens a side drawer on top of the list. Close it with the X button or by clicking outside. All fields are read-only.

Figure: School Admin – SBFAS review drawer

Figure: MOE HQ – MOEFAS review drawer

### 4.1 Sections by scheme

| # | Section | MOEFAS | SBFAS | Behaviour |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Header | Yes | Yes | Scheme and "REVIEW", Application ID, then student name, class (School Admin) or school (MOE HQ), and Source. X closes the drawer. |
| 2 | Decision | Decided only | Decided only | See 4.3. |
| 3 | Eligibility check | Yes | No | One row per criterion: value, limit (and % over when above) and Pass or Fail. Limits come from the active scheme. Note: "Information only. MOE HQ can approve a Fail or reject a Pass." |
| 4 | Student | No | Yes | Full name, NRIC/FIN, Class, School (MOE HQ only), Citizenship. |
| 5 | Parent | No | Yes | Name and relationship, NRIC/FIN, Mobile, Email. |
| 6 | Household and income | Yes | Yes | GHI (S$ per month), Household size, PCI (S$), Income source (API or Paper). Income cannot be edited. |
| 7 | ML recommendation (MOEFAS) / ML suggestion (SBFAS) | Yes | Yes | Recommendation or suggestion, tag "Recommendation only" / "Suggestion only", Confidence %, Risk, Need Score, Base Tier, Adjusted Tier, Fast-track (if any), deny rule (if any), Factors, and a collapsible "Score breakdown" (one line per feature: value × weight = contribution). SBFAS: warning when the school has no active SBFAS scheme. |
| 8 | Documents | No | Yes | File name with a View link that opens the file. |
| 9 | History | No | Yes | Date and time and action, oldest first (see 4.4). |
| 10 | Reject / Approve buttons | MOE HQ, Pending | School Admin of the school, Pending | Open the dialogs in section 6. Approve label: "Approve MOEFAS" or "Approve". |

### 4.2 Eligibility criteria shown

| Scheme | Criteria |
| :--- | :--- |
| MOEFAS | Nationality is Singapore Citizen. GHI up to S$ 4,000. PCI up to S$ 1,000. GHI and PCI are separate rows. Pass if nationality passes and at least one of GHI or PCI passes (match rule of the active scheme). |
| SBFAS | Not shown as a section. The SBFAS scheme criteria (Citizen or PR, PCI within the SBFAS band) are used for the ML suggestion. |

### 4.3 Decided application

When the status is Approved or Rejected, the Reject and Approve buttons are hidden and a Decision section shows at the top of the drawer: Result, Tier and Effective from (or Reason), Comment, decided by, and date and time.

### 4.4 History actions

Uploaded, Submitted, SBFAS application (not a Singapore Citizen), Eligibility check: Pass/Fail · waits for MOE HQ, Approved · Tier X · n fee(s) reduced by S$…, Rejected · Reason, Email with result/reason sent to parent, Moved to SBFAS, Moved to SBFAS from APP-…, Paper application edited.

## 5. ML assessment (FAS Scoring & Decision Engine)

The engine is rule-based and deterministic. It runs for every application and is shown to the reviewer as information only. It never approves or rejects (BR6, BR19). Weights and cut-offs are configuration, not fixed in the screen.

### 5.1 Deny rules (checked first)

| Rule | Condition |
| :--- | :--- |
| DENY-NO-CHILDREN | No household member under 21 |
| DENY-ONLY-CHILDREN | All household members under 21 (no adult) |
| DENY-INVALID-SIZE | Household size ≤ 0 |
| DENY-WORKERS-EXCEED-SIZE | Workers > household size |
| DENY-NEGATIVE-MONTHS | Months since last support < 0 |

If a deny rule is hit, Need Score = 0 and both tiers are Ineligible. The rule ID is shown in the ML box.

### 5.2 Need Score

Need Score = 100 × Σ (weight × feature), each feature in [0, 1], weights add up to 1.0.

| Feature | Weight | How it is computed |
| :--- | :--- | :--- |
| Income | 0.70 | max(x_ghi, x_pci). x_ghi = clamp(1 − GHI/12,000). x_pci = clamp(1 − PCI/3,000). The path used (GHI-driven, PCI-driven, Equal) is logged. |
| Dependency | 0.05 | (household size − workers) / household size |
| Stability | 0.10 | Stable 0.20 (3-month / 12-month average 0.70–1.30), Interrupted 0.50 (ratio < 0.70), Unemployed short 0.80 (1–5 zero months), Unemployed long 1.00 (≥ 6 zero months) |
| Recency | 0.10 | Last support ≤ 3 months 0.90 (Fast-track), 4–12 months 0.50, 13–24 months 0.30, never or > 24 months 0.30 |
| Vulnerability | 0.05 | Sum of: single parent +0.15, elderly member (65+) +0.10, disabled member +0.20, young child (< 6) +0.10. Max 1.0. |

### 5.3 Tiers and risk

| Base Tier (statutory, GHI OR PCI) | Adjusted Tier (Need Score) | ML risk |
| :--- | :--- | :--- |
| Tier 1: GHI ≤ S$ 4,000 or PCI ≤ S$ 1,000 | Tier 1: 75.00–100 | High |
| Tier 2: GHI ≤ S$ 5,500 or PCI ≤ S$ 1,375 | Tier 2: 50.00–74.99 | Medium |
| Tier 3: GHI ≤ S$ 9,000 or PCI ≤ S$ 2,250 | Tier 3: 25.00–49.99 | Low |
| Tier 4: GHI ≤ S$ 12,000 or PCI ≤ S$ 3,000 | Tier 4: 1.00–24.99 | Low |
| Ineligible: GHI > S$ 12,000 and PCI > S$ 3,000 | Ineligible: 0 | Low |

When the Adjusted Tier shows more need than the Base Tier, the ML box flags it as non-income hardship (evidence for a discretionary decision).

### 5.4 Recommendation, suggested tier and confidence

Suggested tier: the tier of the application's scheme (MOEFAS active scheme, or the school's SBFAS scheme) whose band and nationality match. If the income is up to 5% above the scheme limit, the lowest tier is suggested.

MOEFAS recommendation: "Grant · Tier X" when a tier matches. Up to 5% above the limit: "Grant · lowest tier" if Need Score ≥ 50, otherwise "Borderline". Else "Do not grant".

SBFAS suggestion: "Tier X · High/Medium/Low need" (need by tier order) or "Reject" when no tier matches.

Confidence (55–95%): starts at 92, minus 18 if up to 5% above the limit, minus 8 if income is not from API, minus 10 if the name differs from Government data, minus 6 if the household profile is assumed, minus 4 if no tier is suggested.

## 6. Screen: Approve and reject dialogs

Both dialogs open from the review drawer. The dialog title shows the scheme: "Approve MOEFAS" or "Approve SBFAS". The Comment box is empty by default.

### 6.1 Approve dialog

Figure: Approve SBFAS (School Admin)

Figure: Approve MOEFAS (MOE HQ) – with Tier and MOEFAS budget note

| # | Element | Type | Required | Behaviour |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Tier | Dropdown | Yes | Tiers of the scheme: Tier 1 · High need, Tier 2 · Medium need, Tier 3 · Low need. Pre-selected with the ML suggested tier (hint "ML suggests Tier X"); the reviewer can change it. Shown for both MOEFAS and SBFAS. |
| 2 | Effective from | — | — | Not shown. The decision date (today) is used. |
| 3 | Comment | Text box | No | Up to 500 characters. Counter "n/500". |
| 4 | Fees that will be subsidised | Read-only list | - | One row per open fee that the scheme covers: fee name and amount, subsidy (S$ and %). Total subsidy at the bottom. Updates when the Tier changes. If there are no open fees: "No open fees right now. Fees issued later are subsidised automatically." |
| 5 | MOEFAS budget | Note | - | MOEFAS only. "MOEFAS budget left: S$ X. After this approval: S$ Y." If the total subsidy is more than the budget left, a red message shows (section 8) and Confirm approval is disabled. |
| 6 | Cancel | Button | - | Closes the dialog. Nothing is saved. |
| 7 | Confirm approval | Button | - | Disabled when no Tier is selected, the comment is over 500 characters, the scheme has no active version, or the MOEFAS budget is not enough. Saves the decision (section 9). |

### 6.2 Reject dialog

Figure: Reject application (MOEFAS, MOE HQ) – parent asked for SBFAS

| # | Element | Type | Required | Behaviour |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Reason | Dropdown | Yes | Income above limit, Not eligible nationality, Incomplete documents, Other. Nothing selected by default. The hint under the field lists the same reasons. |
| 2 | Comment | Text box | Yes | Up to 500 characters. Placeholder: "Explain the decision. Parent receives the reason by email." |
| 3 | SBFAS note | Note | - | MOEFAS only. If "Also consider for SBFAS" is Yes: "…a new SBFAS application goes to {school} for its decision." If No: "The parent did not ask for SBFAS. The application closes as Rejected." |
| 4 | Cancel | Button | - | Closes the dialog. Nothing is saved. |
| 5 | Reject application | Button | - | Disabled until Reason and Comment are filled. Saves the decision (section 9). |

## 7. Business rules

| ID | Rule |
| :--- | :--- |
| BR1 | MOEFAS always needs the final decision of MOE HQ. The system check and the ML assessment do not approve or reject. |
| BR2 | SBFAS is decided only by School Admin of the student's school. MOE HQ can view SBFAS but not decide. |
| BR3 | One decision per application. After Approved or Rejected, the application is read-only. |
| BR4 | If two users open the same Pending application, the first to confirm wins. The second gets the message in section 8. |
| BR5 | Eligibility criteria and limits come from the active scheme setup (for example MOEFAS: Citizen, GHI up to S$ 4,000 or PCI up to S$ 1,000). They are not fixed in the screen. |
| BR6 | The eligibility check is information only. The approver can approve a Fail or reject a Pass. |
| BR7 | Subsidy % per fee for each Tier comes from the scheme setup. |
| BR8 | Approve needs a Tier. The Tier is pre-selected with the ML suggestion and can be changed. Comment is optional. |
| BR9 | Reject needs a Reason and a Comment. |
| BR10 | Effective from is the decision date (today). The subsidy applies to open fees due on or after it and to new fees. |
| BR11 | Income is read-only. It cannot be edited in the drawer. |
| BR12 | MOEFAS rejected by MOE HQ and "Also consider for SBFAS" is Yes: create an SBFAS application with status Pending for the student's school. If No: the application is Rejected and the process ends. |
| BR13 | School Admin sees only SBFAS applications of their own school. MOEFAS data is never shown to School Admin. |
| BR14 | Application ID format is APP-YYYY-NNNNN and is unique. |
| BR15 | Comment: up to 500 characters, plain text. |
| BR16 | Currency is S$. Date format is DD/MM/YYYY. Time is HH:mm, Singapore time (UTC+8). |
| BR17 | MOEFAS approval checks the MOEFAS budget (F6): budget left = MOEFAS budget − subsidies already granted. If the total subsidy of this approval is more than the budget left, approval is blocked. No budget set = no limit. |
| BR18 | A student who is not a Singapore Citizen is not considered for MOEFAS. The application is created as SBFAS for the school. |
| BR19 | The ML assessment (Need Score, tiers, risk, recommendation, confidence) is information only and is computed by the rule-based engine in section 5. The reviewer always decides. |
| BR20 | The parent gets an email after every decision: with the Tier when approved, with the Reason when rejected. |

## 8. Validation and messages

| Case | Message | Behaviour |
| :--- | :--- | :--- |
| Approve without Tier / Reject without Reason or Comment / Comment over 500 characters | Counter "n/500" | Confirm button disabled until fixed. |
| MOEFAS budget not enough | Not enough MOEFAS budget. This approval needs S$ X but only S$ Y is left. | Confirm approval disabled. Nothing saved. |
| No active scheme | No active {MOEFAS/SBFAS} scheme. | Confirm approval disabled. |
| Already decided by someone else | This application was already decided by {user} on {DD/MM/YYYY}. | Dialog closes. Drawer becomes read-only. List refreshes. |
| School Admin opens an application of another school | You do not have access to this application. | No data shown. |
| Save fails (system error) | Something went wrong. Please try again. | Nothing is saved. Dialog stays open. |
| Approved | Subsidy applied to the student's EA fees. | Toast message. |
| Rejected | Application rejected. Parent notified by email. | Toast message. |

Clicking Confirm twice quickly saves the decision once.

## 9. After a decision

| Event | System updates |
| :--- | :--- |
| Approved | Status = Approved. Save Tier, Effective from (today), Comment, decided by, date and time. Apply the subsidy to the student's EA fees (open fees and new fees). Add History rows "Approved · Tier X · n fee(s) reduced by S$…" and "Email with result sent to parent". The subsidy counts towards the MOEFAS/SBFAS granted amount in F6. |
| Rejected | Status = Rejected. Save Reason, Comment, decided by, date and time. Send an email to the parent with the Reason. Add History rows "Rejected · Reason" and "Email with reason sent to parent". |
| MOEFAS rejected and "Also consider for SBFAS" is Yes | Create an SBFAS application for the same student, status Pending, visible to the school (History "Moved to SBFAS from APP-…"). Add History row "Moved to SBFAS" on the MOEFAS application. |
| Any decision | Update summary cards and tab counts. The row leaves the Pending tab. The application becomes read-only. |

| Where the result shows | What shows |
| :--- | :--- |
| Upload applications list, Status column | Pending, MOEFAS, or SBFAS - Tier 1 / Tier 2 / Tier 3 |
| Parent e-Service Portal, FAS page | Timeline: Submitted, System check, Review by MOE HQ or school, Decision |
| Parent e-Service Portal, fees page | Fees reduced by the subsidy |
| Student EA record | Scheme, Tier, Effective from |

## 10. Test scenarios

| ID | Scenario | Expected result |
| :--- | :--- | :--- |
| T1 | MOE HQ opens the list | Default tab Pending. MOEFAS and SBFAS from all schools. Review on Pending MOEFAS, View on SBFAS. |
| T2 | School Admin opens the list | Only SBFAS of own school. No School, Scheme or System check column. |
| T3 | School Admin opens a link to another school's application | "You do not have access to this application." |
| T4 | School Admin tries to see a MOEFAS application | Not shown anywhere. |
| T5 | MOE HQ opens a Pending MOEFAS application | Drawer shows eligibility check, income and ML recommendation. Reject and Approve MOEFAS buttons show. |
| T6 | System check is Fail and MOE HQ approves MOEFAS | Allowed. Status Approved. |
| T7 | MOEFAS submitted (Pass or Fail) | Status stays Pending until MOE HQ decides. No automatic approval or rejection. |
| T8 | Open Approve dialog | Tier pre-selected with the ML suggested tier. Fee list shown for that tier. |
| T9 | Select Tier 2, no comment, confirm | Saved. Status Approved. Fee list matches Tier 2. |
| T10 | Change Tier in the Approve dialog | Fee list and Total subsidy change. |
| T11 | Approve MOEFAS when total subsidy is more than the MOEFAS budget left | Red budget message. Confirm approval disabled. Nothing saved. |
| T12 | Reject without Reason or Comment | Reject application disabled. |
| T14 | Comment with 501 characters | Confirm disabled. Counter shows 501/500. |
| T15 | Reject with Reason and Comment | Status Rejected. Parent gets an email with the Reason. Toast "Application rejected. Parent notified by email." |
| T16 | MOE HQ rejects MOEFAS, "Also consider for SBFAS" is Yes | New SBFAS application, Pending, visible to the school. |
| T17 | MOE HQ rejects MOEFAS, "Also consider for SBFAS" is No | No new application. MOEFAS Rejected. |
| T18 | SBFAS decided by School Admin | MOE HQ sees it as Approved or Rejected, read-only. |
| T19 | MOE HQ opens a Pending SBFAS application | View only. No Approve or Reject buttons. |
| T32 | Application for a Singapore PR student | Created as SBFAS, Pending for the school. Not shown as MOEFAS. |
| T20 | Two users confirm the same Pending application | First saves. Second gets the "already decided" message. |
| T21 | Click Confirm twice quickly | One decision saved. |
| T22 | Open a decided application | Drawer is read-only. Decision section shows. No buttons. |
| T23 | Approve an application | Student's EA fees reduced. Parent gets an email. |
| T24 | Approve or reject | Summary cards and tab counts update. Row leaves the Pending tab. |
| T25 | Combine filters (Scheme, Status, ML risk, Submitted) | Only rows matching all filters. Page goes back to 1. |
| T26 | Search by NRIC/FIN, name, Application ID | Matching rows only, not case sensitive. |
| T27 | Filter with no match | "No applications found." |
| T28 | More than 10 results | 10 rows per page, newest Submitted first. |
| T29 | Export with a filter on | CSV has only the filtered rows and the export columns (3.4). |
| T30 | Save fails | "Something went wrong. Please try again." Nothing saved. |
| T31 | Dates, times and money | DD/MM/YYYY, HH:mm Singapore time, S$. |
| T33 | Household with GHI S$ 3,000, size 4, 1 worker, Unemployed short, last support 6 months, elderly member | Need Score 69.75, Adjusted Tier 2, Base Tier 1, ML risk Medium. |
| T34 | Household with workers more than household size | Deny rule DENY-WORKERS-EXCEED-SIZE shown. Need Score 0. Reviewer can still decide. |
| T35 | Support received 2 months ago | Fast-track shown in the ML box. |
