# Phân Hệ: Đánh Giá & Phê Duyệt Hồ Sơ Trợ Cấp (FAS Assessment) (FAS assessment)

Tổng số: **9** test cases.

| STT | Mã UAT | Tên Kịch Bản | Vai Trò | Người Phụ Trách | Trạng Thái | Kết Quả Thực Tế |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- |
| 1 | **UAT-031** | Create and activate valid MOEFAS and school SBFAS schemes | HQ / School user | Gavin | ⚪ **Not Run** |  |
| 2 | **UAT-033** | Configure stage/component subsidies and apply the correct capped amount | HQ / School user | GAvin | ⚪ **Not Run** |  |
| 3 | **UAT-035** | School grants or rejects SBFAS under human control | School reviewer / HQ observer | Kent | ⚪ **Not Run** |  |
| 4 | **UAT-MOE-06** | Create a MOEFAS scheme and view FAS applications | HQ | Kent | ⚪ **Not Run** |  |
| 5 | **UAT-MOE-06-N1** | Invalid scheme | HQ | Kent | ⚪ **Not Run** |  |
| 6 | **UAT-SCH-02** | Create an SBFAS scheme and add a fee | School user | Kent | ⚪ **Not Run** |  |
| 7 | **UAT-SCH-02-N1** | Invalid SBFAS scheme | School user | Kent | ⚪ **Not Run** |  |
| 8 | **UAT-SCH-03** | Approve an SBFAS application | School user (reviewer) | Kent | ⚪ **Not Run** |  |
| 9 | **UAT-SCH-03-N1** | Reject an SBFAS application | School user (reviewer) | Kent | ⚪ **Not Run** |  |

## Chi Tiết Từng Kịch Bản

### UAT-031 — Create and activate valid MOEFAS and school SBFAS schemes

- **Phân hệ:** `FAS assessment`
- **Phụ trách:** Gavin
- **Vai trò:** HQ / School user
- **Trạng thái:** ⚪ **Not Run**

#### 1. Setup, Data & Gate
```
Setup: Current scheme lifecycle and permissions follow the FAS gate; sample config independently reviewed.
Data: DATA-SCHEME, DATA-ROLES.
Gate: FAS access.
Covers: US-044, US-045.
Data: DATA-FAS and Gavin supply separate eligibility-boundary applications. Existing precise date/budget validation claims remain conditional on G3/D05; the merged draft is not approval.
Replaces definition UAT-032: US-046, US-049. Required variants remain separate; no old result is reused.
D05: any grant affected by available budget follows the explicitly agreed policy, not an assumed warning-only or blocking rule.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. As School A User, launch 'Create SBFAS Scheme' 4-Step Wizard:
   - Step 1 General: Enter Scheme Name, Open From/To, Effective From/To, Total Budget.
     Rule: Applications Open From >= Today; Open To > Open From; Effective From > Open To (effective strictly after applications close); Total Budget >= 0.
   - Step 2 Eligibility: Select Nationalities, configure GHI/PCI income bands and operator.
   - Step 3 Subsidy: Select fee components and assign percentage per academic offering.
   - Step 4 Review: Verify summary; save as Draft then reopen.
   Expected: Wizard persists all 4 steps; School A ownership enforced; School B cannot view or edit draft.
2. Validate date boundaries and timeline rules:
   - Negative test: Set Effective From <= Applications Open To.
     Expected: System blocks transition with validation error 'Effective from must be after applications close'.
   - Negative test: Save with Total Budget = 0 on Publish.
     Expected: System enforces Total Budget > 0 for publication.
3. Publish and inspect scheme lifecycle:
   - Review and click 'Publish' for the valid SBFAS scheme.
   - Verify application availability during Open From - Open To, and subsidy applicability during Effective Period.
   Expected: Scheme transitions to Active; available for parent/school applications during window; School B cannot modify School A scheme.
4. With Gavin, write an independent expected table for GHI-only, PCI-only, neither and exact-limit households, plus nationality/wrong-school controls; submit separate applications and run the agreed trigger.
   Expected: Each result/reason is reproducible from the recorded scheme inputs and G3/D06 rule; no guessed threshold, wrong-scope bypass or presumed immediate grant. Preserve waiting and assessed observations separately.

Watch for: Effective From must strictly succeed Applications Open To; budget must be non-negative and positive on publish.
```

#### 3. Kết Quả Thực Tế (Actual Result)
```

```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```

```

---

### UAT-033 — Configure stage/component subsidies and apply the correct capped amount

- **Phân hệ:** `FAS assessment`
- **Phụ trách:** GAvin
- **Vai trò:** HQ / School user
- **Trạng thái:** ⚪ **Not Run**

#### 1. Setup, Data & Gate
```
Setup: Gavin independently checks sample arithmetic; due dates/effective periods/rounding contract agreed
Data: DATA-SCHEME, DATA-FEES.
Covers: US-047, US-051.
Replaces definition UAT-037: US-051, US-040. Required variants remain separate; no old result is reused.
D05: any grant affected by available budget follows the explicitly agreed policy, not an assumed warning-only or blocking rule.
Gate: FAS access.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. As School A User, configure Subsidy Matrix in SBFAS Scheme (Step 3):
   - Map fee components: configure 50% subsidy for supported Component A (amount SGD 80.00); leave Component B unsupported (0%, amount SGD 20.00). Total bill SGD 100.00.
   Expected: Percentage matrix saved per Education Stage/Level; unselected components remain 0% subsidy.
2. Simulate subsidy application on unpaid Student Charge:
   - Link approved SBFAS grant to student charge with SGD 100.00 original total.
   - Inspect breakdown: Component A (80.00) subsidy = SGD 40.00; Component B (20.00) subsidy = SGD 0.00.
   Expected: Original Amount remains SGD 100.00; Total Subsidy = SGD 40.00; Net Payable = SGD 60.00; audit trail links grant to charge.
3. Validate cap enforcement and negative payable prevention:
   - Test capped scenario: apply fixed SGD 100.00 subsidy against supported Component A (cap = SGD 80.00).
   Expected: Subsidy capped at SGD 80.00; Net Payable = SGD 20.00; net payable NEVER negative (< 0); other components and stages unaffected.
4. Replay the grant/application trigger and compare separate paid, unsupported and date-ineligible charge controls.
   Expected: No duplicate subsidy or negative payable. Original amounts remain; controls change only under an explicitly agreed adjustment rule, with grant/charge/invoice evidence.

Watch for: Original Amount remains immutable; subsidy applied to eligible components only; Net Payable floor is SGD 0.00.
```

#### 3. Kết Quả Thực Tế (Actual Result)
```

```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```

```

---

### UAT-035 — School grants or rejects SBFAS under human control

- **Phân hệ:** `FAS assessment`
- **Phụ trách:** Kent
- **Vai trò:** School reviewer / HQ observer
- **Trạng thái:** ⚪ **Not Run**

#### 1. Setup, Data & Gate
```
Setup: Correct school routing and final-decision or role permissions follow the FAS gate.
Data: DATA-ROLES, DATA-FAS, DATA-SCHEME.
Gate: FAS access.
Covers: US-045, US-050.
Replaces definition UAT-036: US-052. Required variants remain separate; no old result is reused.
D05: any grant affected by available budget follows the explicitly agreed policy, not an assumed warning-only or blocking rule.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. As School A Reviewer, navigate to FAS Management > School Applications:
   - Filter Pending SBFAS applications; open Application 1 (student enrolled at School A).
   - Review household income, GHI/PCI calculation, and optional ML Recommendation tier.
   Expected: Only School A applications display actionable 'Review' button; ML recommendation displays clearly as Advisory (non-binding).
2. Execute Grant (Approve) and Reject workflows under human authorization:
   - Case A (Grant): Click 'Review', select eligible SBFAS Scheme/Tier, confirm Grant.
     Expected: Application transitions to 'Approved' with awarded tier; reviewer ID and timestamp recorded.
   - Case B (Reject): Open Application 2, click 'Reject'; verify mandatory 'Reason for Rejection' field. Enter reason and confirm.
     Expected: Mandatory reason enforced (cannot submit empty); status transitions to 'Rejected' with reason preserved.
3. Verify role security, finality, and cross-school boundary:
   - Reopen finalized application: verify decision is locked (no arbitrary re-grant / re-decision).
   - Log in as School B User: verify School A applications cannot be viewed or approved.
   - Log in as MOE HQ Admin: verify HQ has read-only view (no Approve/Reject buttons per F4 v1.3).
4. Inspect the advisory recommendation, choose a different permitted tier or reject, then exercise unavailable/no-match recommendation on a separate application.
   Expected: Authorized human decision prevails with no recommendation auto-grant; source/inputs are inspectable under the agreed rule and manual review remains usable under its confirmed fallback. No model/accuracy claim is inferred.

Watch for: Human review retains final authority over ML suggestions; HQ is read-only for school decisions; mandatory rejection reasons.
```

#### 3. Kết Quả Thực Tế (Actual Result)
```

```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```

```

---

### UAT-MOE-06 — Create a MOEFAS scheme and view FAS applications

- **Phân hệ:** `FAS assessment`
- **Phụ trách:** Kent
- **Vai trò:** HQ
- **Trạng thái:** ⚪ **Not Run**

#### 1. Setup, Data & Gate
```
Setup: MOE HQ User is logged in; At least one Fee Component is Active
Data: DATA-SCHEME, DATA-ROLES. Values: Name: MOEFAS 2028; Form: 1 Aug 2028 to 31 Dec 2028; Effective from: 1 Jan 2029; Nationality: Singapore Citizen; Subsidy: Primary 100%, Secondary 70%, Pre-University 50%.
Gate: FAS access.
Covers: FS04 §3.1, §7, BR2, BR5, BR9.
Replaces definition UAT-034: US-048, US-049. Required variants remain separate; no old result is reused.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. Open MOEFAS schemes and create a new scheme. General step: enter name, Form opens, Form closes, Effective from. Eligibility step: choose nationality and GHI, PCI bands. Subsidy step: enter the rate for each level. Review and Publish.
   Expected: The scheme is published and becomes read only. The scheme list shows the form status label and Approved automatically.
2. Open FAS applications.
   Expected: FAS applications lists applications from all schools, with no Approve or Reject button.
3. Using independent copies and the owned clock, submit just before, exactly at and after the agreed application cutoff.
   Expected: Acceptance/rejection matches the recorded timezone/cutoff. Effective period remains separate; repeated assessment adds no duplicate grant. G3 and D05 must settle required outcomes.

Watch for: Severity 1, must Pass before go live (proposed).
```

#### 3. Kết Quả Thực Tế (Actual Result)
```

```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```

```

---

### UAT-MOE-06-N1 — Invalid scheme

- **Phân hệ:** `FAS assessment`
- **Phụ trách:** Kent
- **Vai trò:** HQ
- **Trạng thái:** ⚪ **Not Run**

#### 1. Setup, Data & Gate
```
Setup: MOE HQ User is logged in
Data: DATA-SCHEME, DATA-ROLES. Values: Form closes: 31 Dec 2028; Effective from: 31 Dec 2028.
Gate: FAS access.
Covers: FS04 §7.3, T9.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. Create a new scheme and enter the Form closes date as Effective from.
   Expected: The system shows Effective from must be after Form closes.
2. Go to the Review step and click Publish.
   Expected: The scheme is not published.

Watch for: Severity 2 (proposed).
```

#### 3. Kết Quả Thực Tế (Actual Result)
```

```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```

```

---

### UAT-SCH-02 — Create an SBFAS scheme and add a fee

- **Phân hệ:** `FAS assessment`
- **Phụ trách:** Kent
- **Vai trò:** School user
- **Trạng thái:** ⚪ **Not Run**

#### 1. Setup, Data & Gate
```
Setup: School Admin is logged in; An Active Fee Component exists that is not yet in the scheme
Data: DATA-SCHEME, DATA-FEES, DATA-ROLES. Values: Name: Tier 1; Nationality: Singapore Citizen; Subsidy: P1 100%, P2 80%, P3 60%; New fee component: Activity fee.
Gate: FAS access.
Covers: FS04 §7, T13, T14.
D05: any grant affected by available budget follows the explicitly agreed policy, not an assumed warning-only or blocking rule.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. Open SBFAS schemes and create a new scheme named Tier 1. Enter the form period and the effective period. Choose nationality and GHI, PCI bands. Enter the subsidy rate for each level. Review and Publish.
   Expected: Tier 1 is published and becomes read only.
2. When the scheme is Active, click Add fee, choose the new component, enter a value, click Add to scheme.
   Expected: Add fee is available only on Active or Upcoming schemes. The new column is added and the old columns are read only. The subsidy applies to open fees of students already granted the scheme.

Watch for: Severity 2 (proposed).
```

#### 3. Kết Quả Thực Tế (Actual Result)
```

```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```

```

---

### UAT-SCH-02-N1 — Invalid SBFAS scheme

- **Phân hệ:** `FAS assessment`
- **Phụ trách:** Kent
- **Vai trò:** School user
- **Trạng thái:** ⚪ **Not Run**

#### 1. Setup, Data & Gate
```
Setup: The school's Tier 1 scheme is published
Data: DATA-SCHEME, DATA-FEES, DATA-ROLES. Values: Name, first attempt: Tier 1; Name, second attempt: Tier 2.
Gate: FAS access.
Covers: FS04 §7.3, T12.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. Create another scheme also named Tier 1 with an application period overlapping the old Tier 1. Click Publish.
   Expected: The first attempt reports an overlap with an existing scheme and cannot be published.
2. Rename it to Tier 2 and Publish again.
   Expected: The second attempt with a different name can be published.

Watch for: Severity 2 (proposed).
```

#### 3. Kết Quả Thực Tế (Actual Result)
```

```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```

```

---

### UAT-SCH-03 — Approve an SBFAS application

- **Phân hệ:** `FAS assessment`
- **Phụ trách:** Kent
- **Vai trò:** School user (reviewer)
- **Trạng thái:** ⚪ **Not Run**

#### 1. Setup, Data & Gate
```
Setup: School Admin is logged in; A Pending SBFAS application exists for a student of the school; SBFAS scheme Tier 1 is published
Data: DATA-ROLES, DATA-FAS, DATA-SCHEME. Values: Tier: Tier 1; Comment: Eligible.
Gate: FAS access.
Covers: FS04 §2.3, §6.1, §8, T8.
D05: any grant affected by available budget follows the explicitly agreed policy, not an assumed warning-only or blocking rule.
Owner checks: UAT-HOWARD-025.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. Open FAS applications, Pending tab. Click Review on the application. Check income, context and the ML recommendation in the drawer.
   Expected: The tier list shows the school's SBFAS schemes and the ML recommended tier is preselected.
2. Choose a tier, enter a Comment, click Confirm approval.
   Expected: The application becomes Approved with the tier and the scheme Effective from. The message Subsidy applied to the student's EA fees appears. The parent receives an email and the application becomes read only.

Watch for: Severity 1, must Pass before go live (proposed).
```

#### 3. Kết Quả Thực Tế (Actual Result)
```

```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```

```

---

### UAT-SCH-03-N1 — Reject an SBFAS application

- **Phân hệ:** `FAS assessment`
- **Phụ trách:** Kent
- **Vai trò:** School user (reviewer)
- **Trạng thái:** ⚪ **Not Run**

#### 1. Setup, Data & Gate
```
Setup: School Admin is logged in; A Pending SBFAS application exists for a student of the school
Data: DATA-ROLES, DATA-FAS, DATA-SCHEME. Values: Reason: Income above limit; Comment: Income above the Tier 1 limit.
Gate: FAS access.
Covers: FS04 §6.2, BR11.
Owner checks: UAT-HOWARD-025.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. Open the application in FAS applications. Click Reject. Choose a Reason and enter a Comment.
   Expected: The Reject application button stays disabled until both Reason and Comment are filled.
2. Click Reject application.
   Expected: The application becomes Rejected and shows Application rejected. Parent notified by email. The parent receives an email with the reason.

Watch for: Severity 1, must Pass before go live (proposed).
```

#### 3. Kết Quả Thực Tế (Actual Result)
```

```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```

```

---

