# Phân Hệ: Cổng Phụ Huynh & Tra Cứu Kết Quả (Parent access and results)

Tổng số: **4** test cases.

| STT | Mã UAT | Tên Kịch Bản | Vai Trò | Người Phụ Trách | Trạng Thái | Kết Quả Thực Tế |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- |
| 1 | **UAT-005** | Parent signs in and sees only verified children | Parent A / Parent B | Howard | 🟢 **Pass** | QA check pass on 29/10/2026. Actual result as expected. The message may be not exactly the same as mentioned in expected... |
| 2 | **UAT-006** | Parent reads correct balances, enrolment and filtered history | Parent | Howard | 🟢 **Pass** | QA check pass on 29/10/2026. Actual result as expected. The message may be not exactly the same as mentioned in expected... |
| 3 | **UAT-007** | Parent updates permitted contact fields without changing identity | Parent | Howard | 🟢 **Pass** | QA check pass on 29/10/2026. Actual result as expected. The message may be not exactly the same as mentioned in expected... |
| 4 | **UAT-008** | Parent sees the correct grant decision and application details | Parent | Howard | 🟡 **In Progress** |  |

## Chi Tiết Từng Kịch Bản

### UAT-005 — Parent signs in and sees only verified children

- **Phân hệ:** `Parent access and results`
- **Phụ trách:** Howard
- **Vai trò:** Parent A / Parent B
- **Trạng thái:** 🟢 **Pass**

#### 1. Setup, Data & Gate
```
Setup: Named Singpass mock and Parent/child data API mock with relationship data; account lifecycle fixture prepared by Josh. Parent A signs in; the other parent of the same children and an unrelated Parent B are also mapped.
Data: DATA-ROLES, DATA-LIFE.
Source: FS-08 FR-08.1, FR-08.2, AC 1–5, 13, 23.
Covers: US-005.
Owner checks: UAT-HOWARD-001, UAT-HOWARD-002, UAT-HOWARD-003, CHAN-UAT-15.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. Sign in as Parent A and inspect linked children.
   Expected: Home shows one card per child linked by father or mother NRIC; identity source and mock are labelled.
2. Sign out, sign in again as Parent A, then sign in as the other parent of the same children.
   Expected: The same account is reused, no new account; both parents see the same children with the same rights.
3. Try to reach an unrelated child using the delivered navigation and a known direct link in authorized QA.
   Expected: Access is refused with "You do not have permission to perform this action."; no unrelated child data is shown
4. Sign out and sign in as Parent B.
   Expected: No prior family data or session context is reused.
5. Parent with no child;
   Expected: "We could not find any student linked to your account", no access

Watch for: No logged-in identity is fabricated by the test. Record each negative variant as a separate result.
```

#### 3. Kết Quả Thực Tế (Actual Result)
```
QA check pass on 29/10/2026. Actual result as expected. The message may be not exactly the same as mentioned in expected result but it is acceptable
```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```

```

---

### UAT-006 — Parent reads correct balances, enrolment and filtered history

- **Phân hệ:** `Parent access and results`
- **Phụ trách:** Howard
- **Vai trò:** Parent
- **Trạng thái:** 🟢 **Pass**

#### 1. Setup, Data & Gate
```
Setup: Two linked children with distinct school/balance/history: one Active EA and one in another status; one Pending online payment. Josh (EA, top-up), Chan (school) and Gavin (payment) supply before-state receipts. Use a completed seeded top-up, not a live top-up run, because the top-up gate is still open.
Data: DATA-ROLES, DATA-SCHOOL, DATA-LIFE, DATA-TOPUP, DATA-PAY.
Gate: lifecycle.
Source: FS-08 FR-08.2, sections 6.1–6.2, AC 6–8, 10–12, 25–28.
Covers: US-006, US-007, US-008.
G2 controls the exact age-16 status, closure date and permitted actions. Draft labels below are conditional observations until the decision is recorded.
Owner checks: UAT-HOWARD-004, UAT-HOWARD-005, UAT-HOWARD-006, UAT-HOWARD-007, CHAN-UAT-15.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. Open Home and each linked child's Education Account.
   Expected: Card order follows FS-08 6.1. EA number, status, open and planned close dates, school/year/level/class match the fixture. Available balance counts Completed transactions only; the Pending amount is shown separately and not deducted.
2. Open a child aged 16.
   Expected: The 16-year-old shows Deactive and is view only (no payment, no FAS).
3. Use the Student filters, including one with no matches; then switch to All mode.
   Expected: Correct matching transactions, newest first, 20 per page. No match shows "No transactions found.". All mode adds the Student column and never shows an unrelated child.
4. Change child and return after the seeded top-up and the payment handoff.
   Expected: Updated balance and history agree with the ledger; a Fee payment row has a View fee link to that child's Fees page; no stale child context or lost history.

Watch for: Compare values, not screen navigation alone.
```

#### 3. Kết Quả Thực Tế (Actual Result)
```
QA check pass on 29/10/2026. Actual result as expected. The message may be not exactly the same as mentioned in expected result but it is acceptable
```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```

```

---

### UAT-007 — Parent updates permitted contact fields without changing identity

- **Phân hệ:** `Parent access and results`
- **Phụ trách:** Howard
- **Vai trò:** Parent
- **Trạng thái:** 🟢 **Pass**

#### 1. Setup, Data & Gate
```
Setup: Editable-field list confirmed against delivered parent specification; synthetic contact values only
Data: DATA-ROLES.
Covers: US-009.
Source checks: UAT-HOWARD-008, UAT-HOWARD-009, UAT-HOWARD-010. Supply valid/invalid contacts and a controlled failed save. Exact rules need a recorded source before scoring.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. Save a valid permitted contact change; sign out and back in.
   Expected: The correct parent retains the saved value under the agreed government/local precedence.
2. On separate copies try blank required fields, malformed mobile/email and an invalid postal code, then save.
   Expected: Confirmed field rules reject invalid values; saved details remain unchanged. Record each variant and actual message.

Watch for: Howard 008-010. Exact field limits/messages, audit/email policy and the all-children-16 profile lock remain rule follow-ups; do not infer approval from the owner file.
```

#### 3. Kết Quả Thực Tế (Actual Result)
```
QA check pass on 29/10/2026. Actual result as expected. The message may be not exactly the same as mentioned in expected result but it is acceptable
```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```

```

---

### UAT-008 — Parent sees the correct grant decision and application details

- **Phân hệ:** `Parent access and results`
- **Phụ trách:** Howard
- **Vai trò:** Parent
- **Trạng thái:** 🟡 **In Progress**

#### 1. Setup, Data & Gate
```
Setup: Kent/Gavin supply approved/rejected/pending applications and result receipts
Data: DATA-ROLES, DATA-FAS, DATA-SCHEME.
Gate: FAS access.
Covers: US-010, US-041.
Owner checks: UAT-HOWARD-011, UAT-HOWARD-012, UAT-HOWARD-013.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. Open the submitted application and its details.
   Expected: Previously submitted identity, income, documents and child remain accessible to the authorized parent.
2. Inspect pending, granted and rejected examples.
   Expected: Displayed scheme/child/result/reason reflect actual assessment; pending is not falsely shown as approved.
3. Compare a grant with the affected charge and another family.
   Expected: Grant and payable result reconcile; other-family application cannot be viewed.

Watch for: Missing grant display stays an in-scope blocker, not an optional story.
```

#### 3. Kết Quả Thực Tế (Actual Result)
```

```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```

```

---

