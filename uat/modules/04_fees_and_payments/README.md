# Phân Hệ: Học Phí, Biểu Phí & Thanh Toán (Fees and payments)

Tổng số: **9** test cases.

| STT | Mã UAT | Tên Kịch Bản | Vai Trò | Người Phụ Trách | Trạng Thái | Kết Quả Thực Tế |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- |
| 1 | **UAT-019** | Maintain shared and school fee catalogues with ownership | HQ / School user | Kent | ⚪ **Not Run** |  |
| 2 | **UAT-020** | Apply correct fee rates at effective-date and category boundaries | HQ / School user | Kent | ⚪ **Not Run** |  |
| 3 | **UAT-021** | Preview and publish fees once, then expose correct charges | School user / Parent observer | Kent | ⚪ **Not Run** |  |
| 4 | **UAT-MOE-01** | Prepare EA, school, student and publish fees | HQ / School user | Kent | ⚪ **Not Run** |  |
| 5 | **UAT-PAR-01** | Log in, view the EA and pay fees with the EA | Parent | Gavin | ⚪ **Not Run** |  |
| 6 | **UAT-PAR-01-A1** | Pay online or split EA and online safely | Parent | Gavin | ⚪ **Not Run** |  |
| 7 | **UAT-PAR-01-E2** | EA refund fails | Parent | Gavin | ⚪ **Not Run** |  |
| 8 | **UAT-PAR-01-N3** | Balance too low for the EA only option | Parent | Gavin | ⚪ **Not Run** |  |
| 9 | **UAT-PAR-01-N4** | Recover failed or uncertain online payment without duplicate money movement | Parent | Gavin | ⚪ **Not Run** |  |

## Chi Tiết Từng Kịch Bản

### UAT-019 — Maintain shared and school fee catalogues with ownership

- **Phân hệ:** `Fees and payments`
- **Phụ trách:** Kent
- **Vai trò:** HQ / School user
- **Trạng thái:** ⚪ **Not Run**

#### 1. Setup, Data & Gate
```
Setup: Known shared and school-owned fee/component records
Data: DATA-ROLES, DATA-FEES.
Covers: US-034, US-035.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. Create/update shared type/components as HQ.
   Expected: Allowed shared definitions persist and are visible in permitted school workflows.
2. Create school-specific fee/component and permitted extension as School A.
   Expected: A local values do not overwrite shared definitions or B catalogue.
3. Deactivate a historical component and attempt unauthorized edit.
   Expected: Billing history remains intact; unauthorized/shared edits are prevented.

Watch for: Record catalogue ownership and component IDs for scheme/subsidy handoffs.
```

#### 3. Kết Quả Thực Tế (Actual Result)
```

```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```

```

---

### UAT-020 — Apply correct fee rates at effective-date and category boundaries

- **Phân hệ:** `Fees and payments`
- **Phụ trách:** Kent
- **Vai trò:** HQ / School user
- **Trạng thái:** ⚪ **Not Run**

#### 1. Setup, Data & Gate
```
Setup: Agreed stage, category, rate and effective-date rules under the school dates gate.
Data: DATA-FEES, DATA-SCHOOL.
Gate: school dates.
Covers: US-036.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. Configure known category/stage rates for adjacent valid periods.
   Expected: Configuration persists with intended ownership and date ranges.
2. Preview just before/on the change date for SC and PR controls.
   Expected: Independent expected rate selected for each category/stage/date, with no ambiguous overlap.
3. Try an invalid overlap or missing applicable rate.
   Expected: No silently wrong charge; delivered validation/exception follows agreed rule.

Watch for: Record calculation date separately from system clock; no production rates are invented.
```

#### 3. Kết Quả Thực Tế (Actual Result)
```

```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```

```

---

### UAT-021 — Preview and publish fees once, then expose correct charges

- **Phân hệ:** `Fees and payments`
- **Phụ trách:** Kent
- **Vai trò:** School user / Parent observer
- **Trạng thái:** ⚪ **Not Run**
- **Đặc tả Test Case chi tiết:** [`TC_FEE_PUBLICATION_BATCHES_UAT021.md`](../../../specs/md/TC_FEE_PUBLICATION_BATCHES_UAT021.md) (Chuẩn 10 cột ISTQB / `combo-qa`)

#### 1. Setup, Data & Gate
```
Setup: Known recipient set, effective date/rates and original amounts calculated independently
Data: DATA-FEES, DATA-SCHOOL.
Gate: school dates.
Covers: US-037, US-038, US-039, US-040.
Owner checks: CHAN-UAT-22.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. Configure publication period/targets/components and preview, including an otherwise eligible no-EA student and an ineligible category control.
   Expected: Exact agreed recipients, component amounts and total; eligible no-EA student is not omitted solely for lacking an EA. Ineligible control excluded; preview creates no charges.
2. Resolve a missing-rate control and publish the valid publication.
   Expected: One correct charge per intended recipient/component, including the eligible no-EA student; correct source links, no FAS dependency and no EA creation or balance change.
3. Repeat the agreed publish action and inspect Admin/Parent views.
   Expected: No duplicate billing; both views agree on issued charge state and amounts.

Watch for: Hand charge IDs and amount receipt to Gavin; retain invalid preview as separate evidence.
```

#### 3. Kết Quả Thực Tế (Actual Result)
```

```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```

```

---

### UAT-MOE-01 — Prepare EA, school, student and publish fees

- **Phân hệ:** `Fees and payments`
- **Phụ trách:** Kent
- **Vai trò:** HQ / School user
- **Trạng thái:** ⚪ **Not Run**

#### 1. Setup, Data & Gate
```
Setup: Government API mock has a Singapore citizen who has just turned 7; MOE HQ User account exists; Fee Type, Fee Component and Rate are configured
Data: DATA-ROLES, DATA-SCHOOL, DATA-FEES. Values: Student: student.test01, NRIC S0000001A; School: School Test 01; Class: P1A; Fee: Tuition fee 100.00 SGD.
Gate: school dates; lifecycle.
Covers: FS01 §1.1, FS03 F08, F12, F15.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. Run the daily sync job.
   Expected: An Active EA is created for the student with balance 0.00.
2. Log in to the Admin Portal as MOE HQ User, create a School and a School User. Log in as the School User, create the class, enter the student and assign the student to the class.
   Expected: The student is linked to the EA after class assignment.
3. Log in as MOE HQ User, create a Fee Publication for that school and publish it. Open the student's Student Charge.
   Expected: Student Charge is POSTED and visible to the parent.

Watch for: Severity 1, must Pass before go live (proposed).
```

#### 3. Kết Quả Thực Tế (Actual Result)
```

```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```

```

---

### UAT-PAR-01 — Log in, view the EA and pay fees with the EA

- **Phân hệ:** `Fees and payments`
- **Phụ trách:** Gavin
- **Vai trò:** Parent
- **Trạng thái:** ⚪ **Not Run**

#### 1. Setup, Data & Gate
```
Setup: Parent has a SingPass mock account and a child under 16 linked to an EA; The Active EA has balance 100.00; The child has one Issued invoice of 50.00
Data: DATA-ROLES, DATA-FEES, DATA-PAY. Values: Parent: parent.test01, NRIC S0000100A; Child: student.test01, EA code EA-001; Invoice: 50.00.
Gate: lifecycle.
Covers: FS08 FR-08.1, FR-08.2, FS09 AC-03, AC-13, userflow e-Service 24/10/2026.
Replaces definition UAT-009: US-011, US-040. Required variants remain separate; no old result is reused.
Replaces definition UAT-010: US-012, US-015. Required variants remain separate; no old result is reused.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. Open e-Service and click Log in with SingPass. On Home choose the child Edu Account card.
   Expected: Home shows a card with the child name, EA code and balance.
2. On Edu Account Detail choose Pay fees. Choose the invoice.
   Expected: The fee list belongs to the selected child, with no need to choose the student again.
3. Choose to pay with the EA and confirm.
   Expected: The EA is debited 50.00 exactly once, leaving 50.00.
4. Open the receipt.
   Expected: The invoice becomes Paid and the receipt shows invoice code, total, method and amount per source. The receipt has a way back to the correct child.
5. Before paying, compare charge component/original/subsidy/net amounts and the selected invoice; try paid and cancelled controls separately.
   Expected: Correct selected child/school/period only; invoice items reconcile. Paid charges are not payable again; cancelled/unpaid recovery follows the agreed state rule.
6. Revisit the settled payment and compare invoice, receipt and history.
   Expected: One 50 debit and one settled invoice/receipt, balance 50 from opening 100; no repeat debit or settlement.

Watch for: Severity 1, must Pass before go live (proposed).
```

#### 3. Kết Quả Thực Tế (Actual Result)
```

```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```

```

---

### UAT-PAR-01-A1 — Pay online or split EA and online safely

- **Phân hệ:** `Fees and payments`
- **Phụ trách:** Gavin
- **Vai trò:** Parent
- **Trạng thái:** ⚪ **Not Run**

#### 1. Setup, Data & Gate
```
Setup: Parent is logged in; EA balance is 20.00; The child has an Issued invoice of 50.00; The Online sandbox gateway is set to succeed
Data: DATA-PAY, DATA-ROLES. Values: EA part: 20.00; Online part: 30.00.
Covers: FS09 §3.1.2, userflow e-Service 24/10/2026.
Replaces definition UAT-011: US-013, US-015. Required variants remain separate; no old result is reused.
Replaces definition UAT-012: US-014, US-053. Required variants remain separate; no old result is reused.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. Go to the child's fees and choose the invoice. Choose Both and confirm.
   Expected: The EA part equals the whole balance and the Online part is the remainder. The EA is debited first, then the Online gateway opens.
2. Complete payment on the Online gateway.
   Expected: The invoice is Paid and the receipt lists both sources, total 50.00.
3. Open the receipt.
   Expected: The EA balance is 0.00.
4. On an independent invoice-50 copy choose online only, complete the sandbox payment and reopen the receipt.
   Expected: One online payment of 50, no EA debit; invoice, charge and receipt agree. Record this required variant separately from the split 20 + 30 run.
5. Revisit success and replay a known settled notification through the authorized QA control.
   Expected: No second debit, credit, settlement or receipt. Missing replay control blocks this variant, not a fabricated Pass.

Watch for: Severity 1, must Pass before go live (proposed).
```

#### 3. Kết Quả Thực Tế (Actual Result)
```

```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```

```

---

### UAT-PAR-01-E2 — EA refund fails

- **Phân hệ:** `Fees and payments`
- **Phụ trách:** Gavin
- **Vai trò:** Parent
- **Trạng thái:** ⚪ **Not Run**

#### 1. Setup, Data & Gate
```
Setup: As UAT-PAR-01-N4; The tech team simulates a failed EA refund command
Data: DATA-PAY, DATA-ROLES. Values: EA part: 20.00; Online part: 30.00.
Covers: FS09 AC-18.
Replaces definition UAT-012: US-014, US-053. Required variants remain separate; no old result is reused.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. Choose Both and confirm. At the Online gateway choose failure.
   Expected: The transaction moves to ReconciliationRequired and the invoice stays PaymentPending.
2. Open the invoice after the refund command fails.
   Expected: The parent sees a verifying status. An alert is raised for operations.

Watch for: Severity 1, must Pass before go live (proposed). Needs the tech team to simulate it. The new UX assumes 100% completion.
```

#### 3. Kết Quả Thực Tế (Actual Result)
```

```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```

```

---

### UAT-PAR-01-N3 — Balance too low for the EA only option

- **Phân hệ:** `Fees and payments`
- **Phụ trách:** Gavin
- **Vai trò:** Parent
- **Trạng thái:** ⚪ **Not Run**

#### 1. Setup, Data & Gate
```
Setup: Parent is logged in; EA balance is 20.00; The child has an Issued invoice of 50.00
Data: DATA-PAY, DATA-ROLES. Values: Balance: 20.00; Invoice: 50.00.
Covers: FS09 AC-04.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. Go to the child's fees and choose the invoice. Open the payment method step.
   Expected: The EA only option is disabled and shows the reason. The system suggests Online or Both. No data changes.

Watch for: Severity 1, must Pass before go live (proposed).
```

#### 3. Kết Quả Thực Tế (Actual Result)
```

```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```

```

---

### UAT-PAR-01-N4 — Recover failed or uncertain online payment without duplicate money movement

- **Phân hệ:** `Fees and payments`
- **Phụ trách:** Gavin
- **Vai trò:** Parent
- **Trạng thái:** ⚪ **Not Run**

#### 1. Setup, Data & Gate
```
Setup: As UAT-PAR-01-A1; The Online sandbox gateway is set to fail or cancel
Data: DATA-PAY, DATA-ROLES. Values: EA part: 20.00; Online part: 30.00.
Covers: FS09 AC-09, AC-17.
Replaces definition UAT-011: US-013, US-015. Required variants remain separate; no old result is reused.
Replaces definition UAT-012: US-014, US-053. Required variants remain separate; no old result is reused.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. Choose Both and confirm. At the Online gateway choose failure or cancel.
   Expected: The EA part of 20.00 is refunded.
2. Return to e-Service and open the invoice.
   Expected: The invoice returns to Issued and can be retried. The EA balance returns to 20.00.
3. On separate online-only and split copies force cancellation/definitive failure; then force an ambiguous timeout and query the recorded payment outcome before retry.
   Expected: No paid invoice or receipt on confirmed failure. Split failure has no net EA debit under the agreed recovery rule; online-only never debits EA. Unknown stays unresolved until authoritative query, with no blind duplicate attempt.

Watch for: Severity 1, must Pass before go live (proposed). Failure/cancel/timeout variants remain in scope; do not assume 100% successful completion.
```

#### 3. Kết Quả Thực Tế (Actual Result)
```

```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```

```

---

