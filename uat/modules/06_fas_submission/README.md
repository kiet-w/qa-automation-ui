# Phân Hệ: Nộp Hồ Sơ Trợ Cấp Tài Chính (FAS Submission) (FAS submission)

Tổng số: **8** test cases.

| STT | Mã UAT | Tên Kịch Bản | Vai Trò | Người Phụ Trách | Trạng Thái | Kết Quả Thực Tế |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- |
| 1 | **UAT-028** | Parent submits FAS with retrieved identity and confirmed household income | Parent | Howard | 🟡 **In Progress** |  |
| 2 | **UAT-029** | School enters a paper application including a student without an EA | School user | Chan | ⚪ **Not Run** |  |
| 3 | **UAT-030** | Review and correct OCR-prefilled paper data before submission | School user | Chan | ⚪ **Not Run** |  |
| 4 | **UAT-047** | Handle FAS retrieval, document and submission failures visibly | Parent | Howard | 🟡 **In Progress** |  |
| 5 | **UAT-049** | Submit a family application for two children with independent outcomes | Parent, then paper-entry School user on a separate reset copy | Howard | 🟡 **In Progress** |  |
| 6 | **UAT-SCH-01** | Enter a parent's paper application | School user | Chan | ⚪ **Not Run** |  |
| 7 | **UAT-SCH-01-N1** | Blocked when submitting a paper application | School user | Chan | ⚪ **Not Run** |  |
| 8 | **UAT-SCH-01-E1** | Save a draft when entry is incomplete | School user | Chan | ⚪ **Not Run** |  |

## Chi Tiết Từng Kịch Bản

### UAT-028 — Parent submits FAS with retrieved identity and confirmed household income

- **Phân hệ:** `FAS submission`
- **Phụ trách:** Howard
- **Vai trò:** Parent
- **Trạng thái:** 🟡 **In Progress**

#### 1. Setup, Data & Gate
```
Setup: Open application form and verified child; government or mock profile and income known. The FAS gate must settle form selection; calculation follows the FAS assumption.
Data: DATA-ROLES, DATA-FAS, DATA-SCHEME.
Gate: FAS access.
Covers: US-041.
D06: Government-only GHI 2400 is the baseline data, not approval of an income-entry rule. If a declared 400 variant is approved, use a separate Government 2000 copy; never add 400 to the 2400 baseline.
D05: any grant affected by available budget follows the explicitly agreed policy, not an assumed warning-only or blocking rule.
Owner checks: UAT-HOWARD-014, UAT-HOWARD-015, UAT-HOWARD-016, UAT-HOWARD-017.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. Open the form, select a verified child and inspect retrieved parent/child details.
   Expected: Correct linked identities and permitted field editability under the recorded rule; no invented data or unrelated child.
2. Review four distinct people and Government GHI 2400 on the baseline copy; inspect documents, SBFAS option, context and declaration.
   Expected: If D06 confirms the counting basis, GHI 2400 and PCI 600. Required controls follow the agreed rule; manual extra-income behavior is a separate conditional variant.
3. Submit once; reopen the same application as parent and authorized reviewer.
   Expected: One application retains confirmed values/documents; routing, visibility and decision timing follow G3, with no premature grant or unrelated-family access.

Watch for: UAT-HOWARD-014 to 017. Source-specific editability, SBFAS default, context limit and declaration details remain follow-ups until confirmed. Government retrieval is not called AI.
```

#### 3. Kết Quả Thực Tế (Actual Result)
```

```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```

```

---

### UAT-029 — School enters a paper application including a student without an EA

- **Phân hệ:** `FAS submission`
- **Phụ trách:** Chan
- **Vai trò:** School user
- **Trạng thái:** ⚪ **Not Run**

#### 1. Setup, Data & Gate
```
Setup: Open form; authorized school student without EA; duplicate online application control on separate fixture
Data: DATA-SCHOOL, DATA-FAS, DATA-CSV, DATA-SCHEME.
Gate: FAS access.
Covers: US-042.
Owner checks: CHAN-UAT-12.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. Enter paper application with school/student/household data and attach scan.
   Expected: No-EA student is handled per agreed paper eligibility. A control with no child at the submitting school is blocked; cross-school siblings follow the FAS gate rather than a blanket selection ban.
2. Review/save/submit, then open reviewer details.
   Expected: Correct paper provenance, document and application data retained in common review flow.
3. Attempt a known duplicate online/paper application under agreed duplicate rule.
   Expected: No silent duplicate assessment/grant; user receives actionable outcome.

Watch for: Do not require an EA merely because online submission uses an EA-linked child. Multi-child and cross-school variants are explicit in UAT-049.
```

#### 3. Kết Quả Thực Tế (Actual Result)
```

```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```

```

---

### UAT-030 — Review and correct OCR-prefilled paper data before submission

- **Phân hệ:** `FAS submission`
- **Phụ trách:** Chan
- **Vai trò:** School user
- **Trạng thái:** ⚪ **Not Run**

#### 1. Setup, Data & Gate
```
Setup: Delivered simulated OCR mapping and known imperfect scan; no claim of real OCR accuracy
Data: DATA-CSV, DATA-FAS, DATA-SCHEME.
Covers: US-043.
Owner checks: CHAN-UAT-13.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. Upload known paper sample to OCR/prefill.
   Expected: Supported fields prefilled and source remains identifiable; no automatic submission or grant.
2. Compare to paper and correct the deliberately wrong income/identity field.
   Expected: Operator can review/correct values and validation runs on corrected data.
3. Submit and reopen reviewer details.
   Expected: Only confirmed corrected data reaches assessment; scan retained and simulator labelled.

Watch for: Unsupported scan/failure variant leaves a usable manual-entry route if the agreed contract supplies one.
```

#### 3. Kết Quả Thực Tế (Actual Result)
```

```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```

```

---

### UAT-047 — Handle FAS retrieval, document and submission failures visibly

- **Phân hệ:** `FAS submission`
- **Phụ trách:** Howard
- **Vai trò:** Parent
- **Trạng thái:** 🟡 **In Progress**

#### 1. Setup, Data & Gate
```
Setup: Agreed government retrieval outage, document validation and submission-outcome controls; separate reset copy per failure variant
Data: DATA-ROLES, DATA-FAS, DATA-SCHEME.
Gate: FAS access.
Covers: US-041.
D06: confirm upload types, size and optionality before scoring; use known file metadata, a failed submission control and independent application-count evidence.
Owner checks: UAT-HOWARD-018, UAT-HOWARD-019, UAT-HOWARD-021.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. Force government-income retrieval outage, then restore it and retry.
   Expected: Visible failure; no invented or other-family income. Recovered values come from the recorded source and earlier inputs remain per contract.
2. On separate copies try invalid type/oversize and valid documents, remove one, then inspect a no-document submission.
   Expected: Confirmed type/size/required rules hold, removed files stay removed and counts match. No-document eligibility and exact limits remain D06-dependent.
3. Force a submission failure; query the outcome, then retry/double-click only through the authorized isolated control.
   Expected: Confirmed retained inputs and outcome are visible; exactly one application, no duplicate or premature grant. No fault control means that variant is Blocked.

Watch for: UAT-HOWARD-018, UAT-HOWARD-019, UAT-HOWARD-021. Do not invent exact failure messages, document limits or recovery routes.
```

#### 3. Kết Quả Thực Tế (Actual Result)
```

```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```

```

---

### UAT-049 — Submit a family application for two children with independent outcomes

- **Phân hệ:** `FAS submission`
- **Phụ trách:** Howard
- **Vai trò:** Parent, then paper-entry School user on a separate reset copy
- **Trạng thái:** 🟡 **In Progress**

#### 1. Setup, Data & Gate
```
Setup: Use two eligible applying siblings with one shared household. Run online and paper variants separately; baseline both siblings at School A. The FAS gate must settle cross-school submission and routing before the School A/B variant is scored. Map one family ID, two child IDs, two application IDs and separate child charge IDs. Income and member inclusion follow the FAS assumption. Source locators: F10 section 1.2/BR4-BR5 and F5 section 2/BR1-BR2.
Data: DATA-ROLES, DATA-FAS, DATA-SCHOOL, DATA-SCHEME, DATA-FEES.
Gate: FAS access.
Covers: US-041, US-042, US-049, US-050, US-051, US-010.
D05: any grant affected by available budget follows the explicitly agreed policy, not an assumed warning-only or blocking rule.
Owner checks: UAT-HOWARD-023, UAT-HOWARD-024, UAT-HOWARD-025.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. Select both verified siblings, enter/retrieve shared household inputs once, review and submit the family online application.
   Expected: Exactly two different child application IDs share one family ID. Both carry the same confirmed household inputs; household count includes each person once, not two copies of shared adults or applying children.
2. Open both child applications and the parent family summary.
   Expected: Correct child, school, form/scheme route and charge links are retained separately, with shared context/documents handled under the confirmed contract; no merged or overwritten child result.
3. On a separate reset copy enter the same two-child family through paper submission, then repeat with one child at A and one at B after the FAS gate is resolved.
   Expected: Paper submission also produces one application per child with shared family identity and Paper provenance. Baseline and cross-school selection/routing follow the chosen rule; if cross-school behavior is unresolved this variant stays blocked, not automatically forbidden.
4. Have the authorized reviewer/system decide Child A while Child B remains pending; inspect both, then apply the documented independent decision to B.
   Expected: A decision does not propagate to B. Each application records its own authorized reviewer, scheme, result/reason and effective date; any school review is routed to that child school under the FAS gate.
5. Inspect each parent result, child charge and grant/subsidy record, and a paper control with no child at the submitting school.
   Expected: Each result and subsidy belongs only to its child/charge, with no household-wide double grant or accidental subsidy to pending/rejected sibling. The no-child-at-school control is rejected under the selected F5 rule, without silently rejecting a permitted sibling variant.

Watch for: Keep two source-specific execution variants and per-child before/after evidence. Family grouping is not one shared acceptance decision. Same-school baseline is mandatory; cross-school variant remains an explicit FAS gate.
```

#### 3. Kết Quả Thực Tế (Actual Result)
```

```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```

```

---

### UAT-SCH-01 — Enter a parent's paper application

- **Phân hệ:** `FAS submission`
- **Phụ trách:** Chan
- **Vai trò:** School user
- **Trạng thái:** ⚪ **Not Run**

#### 1. Setup, Data & Gate
```
Setup: School User is logged in; The MOEFAS form is open; A Singapore Citizen parent has a 10 year old child at the school with no application this year; A PDF scan under 10 MB is available
Data: DATA-SCHOOL, DATA-FAS, DATA-CSV, DATA-SCHEME. Values: File: paper-form-test01.pdf; Applicant NRIC: S0000100A; Child NRIC: S0000001A; Relationship: Mother; Context: Household income reduced.
Gate: FAS access.
Covers: FS05 §2, §5 to §7, BR1 to BR9.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. Open Upload applications, click Upload scans, add the file, click Upload and read. Enter the applicant's NRIC and the child's NRIC.
   Expected: Applicant and child details are prefilled and locked.
2. Choose the relationship, declare other members, enter context, tick the declaration.
   Expected: Income comes from Government data and GHI and PCI are shown.
3. Click Review and submit. Check the Review before submitting screen, then click Confirm and submit.
   Expected: The message Application submitted for assessment appears.
4. Open the Upload applications list.
   Expected: Each child has one application with source Paper and status Pending, and the draft is removed.

Watch for: Severity 1, must Pass before go live (proposed).
```

#### 3. Kết Quả Thực Tế (Actual Result)
```

```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```

```

---

### UAT-SCH-01-N1 — Blocked when submitting a paper application

- **Phân hệ:** `FAS submission`
- **Phụ trách:** Chan
- **Vai trò:** School user
- **Trạng thái:** ⚪ **Not Run**

#### 1. Setup, Data & Gate
```
Setup: School User is logged in; A paper application is open on the Review application screen
Data: DATA-SCHOOL, DATA-FAS, DATA-CSV, DATA-SCHEME. Values: Child aged 17: S0000200C; Child with an application: S0000001A.
Gate: FAS access.
Covers: FS05 §6.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. Leave Phone number empty and click Review and submit. Enter a child outside the 7 to 16 age range and click Review and submit. Enter a child who already has an application this year and click Review and submit. Enter the same NRIC for applicant and child and click Review and submit.
   Expected: Each time a red note at the top of the page states what to fix. No application is created.

Watch for: Severity 1, must Pass before go live (proposed).
```

#### 3. Kết Quả Thực Tế (Actual Result)
```

```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```

```

---

### UAT-SCH-01-E1 — Save a draft when entry is incomplete

- **Phân hệ:** `FAS submission`
- **Phụ trách:** Chan
- **Vai trò:** School user
- **Trạng thái:** ⚪ **Not Run**

#### 1. Setup, Data & Gate
```
Setup: School User is logged in; A paper application is open on the Review application screen and partly entered
Data: DATA-SCHOOL, DATA-FAS, DATA-CSV, DATA-SCHEME. Values: Applicant NRIC: S0000100A.
Gate: FAS access.
Covers: FS05 BR6.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. Click Save draft. Return to the Upload applications list.
   Expected: The list shows a Draft row with Application ID Not submitted.
2. Click Continue on the Draft row.
   Expected: Continue reopens the data that was entered.

Watch for: Severity 3 (proposed).
```

#### 3. Kết Quả Thực Tế (Actual Result)
```

```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```

```

---

