# Phân Hệ: Ngân Sách & Thống Kê MOE / Trường (Budget and statistics)

Tổng số: **8** test cases.

| STT | Mã UAT | Tên Kịch Bản | Vai Trò | Người Phụ Trách | Trạng Thái | Kết Quả Thực Tế |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- |
| 1 | **UAT-038** | Set and reopen MOEFAS and school budgets within permissions | HQ / School user | Josh | 🟢 **Pass** | Pass. The case asks for three things: set and reopen a budget, keep each school's budget separate, and deny cross-school... |
| 2 | **UAT-039** | Reconcile granted subsidy statistics and role-scoped totals | HQ / School user | Josh | 🟢 **Pass** | Pass. Two real grants of $30 and $70 were approved and activated. The MOEFAS statistics showed used $100 and remaining $... |
| 3 | **UAT-040** | Track remaining budget and warnings without guessing grant policy | HQ / School user | Josh | 🟢 **Pass** | Pass. The normal scope showed $100 used and $900 remaining from $1000, with pending demand shown separately. In a separa... |
| 4 | **UAT-MOE-04** | Set the MOEFAS budget | HQ | Josh | 🟢 **Pass** | Pass. The case asks for two things: set a MOEFAS budget and reopen it without overwriting a school budget. Both worked.<br>... |
| 5 | **UAT-MOE-05** | Track MOEFAS statistics and budget usage | HQ | Josh | 🟢 **Pass** | Pass. The MOEFAS tracking view showed budget $1000, used $100 and remaining $900 after real grants of $30 and $70. The u... |
| 6 | **UAT-MOE-05-E1** | MOEFAS exhaustion and next grant under the agreed policy | HQ | Josh | 🟢 **Pass** | Pass under your blocking assumption. In a separately reset copy, an actual $500 subsidy exhausted the $500 budget. Previ... |
| 7 | **UAT-SCH-04** | Set and track the SBFAS budget | School user | Josh | 🟢 **Pass** | Pass. The case asks for two things: set and track a school's SBFAS budget, and keep it separate from another school. Bot... |
| 8 | **UAT-SCH-04-E1** | SBFAS exhaustion and next grant under the agreed policy | School user | Josh | 🟢 **Pass** | Pass under your blocking assumption. In a separately reset school copy, an actual $500 school-authorised subsidy exhaust... |

## Chi Tiết Từng Kịch Bản

### UAT-038 — Set and reopen MOEFAS and school budgets within permissions

- **Phân hệ:** `Budget and statistics`
- **Phụ trách:** Josh
- **Vai trò:** HQ / School user
- **Trạng thái:** 🟢 **Pass**

#### 1. Setup, Data & Gate
```
Setup: Budget period and edit behavior to be confirmed against the explicitly agreed R6 rule. The budget assumption warns rather than blocks and is unapproved; record the explicitly agreed rule before scoring.
Data: DATA-BUDGET, DATA-ROLES.
Covers: R6-01, R6-02, R6-03, R6-04.
D05 unapproved: period, edit rights, counting basis, remaining formula and warn/block policy require a recorded decision. Do not score observed behavior as an agreed rule.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. Set MOEFAS budget 1000 as authorized HQ.
   Expected: Correct type/period budget persists and reopens as 1000.
2. Set independent School A/B SBFAS budgets as permitted school users.
   Expected: Each amount belongs to intended school and period.
3. Attempt cross-school or unauthorized budget access/edit.
   Expected: No disclosure/change outside permissions; original budgets unchanged.

Watch for: R6 labels come from the draft requirement register, not invented Sprint story IDs.
```

#### 3. Kết Quả Thực Tế (Actual Result)
```
Pass. The case asks for three things: set and reopen a budget, keep each school's budget separate, and deny cross-school access. All three worked.

A MOEFAS budget of $1000 persisted and reopened as $1000. School A and School B each created and reopened their own SBFAS budget ($500 in the second pass, $1000 in the first), and each amount stayed with its own school and period. A school user asking for the other school's scheme got 404, and neither budget changed.

Separate defect: a saved budget cannot be edited at all. PUT and PATCH to the scheme resource return 405, and existing schemes are view-only. That is a real gap against your edit assumption, but the case does not ask for an edit, so the set, reopen and permission result stands.
```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```
First pass: uat-038/new-scheme-statistics.txt. Second pass: moe-statistics.json, school-A-statistics.json, school-B-statistics-after.json, school-A-cross-denied.json, school-B-cross-denied.json. Edit attempts: moe-edit-PUT.json, moe-edit-PATCH.json, school-edit-PUT.json, school-edit-PATCH.json.
```

---

### UAT-039 — Reconcile granted subsidy statistics and role-scoped totals

- **Phân hệ:** `Budget and statistics`
- **Phụ trách:** Josh
- **Vai trò:** HQ / School user
- **Trạng thái:** 🟢 **Pass**

#### 1. Setup, Data & Gate
```
Setup: Counting basis and period or filter interpretation to be confirmed against the explicitly agreed R6 rule; independent grant receipt list. The budget assumption warns rather than blocks and is unapproved; record the explicitly agreed rule before scoring.
Data: DATA-BUDGET, DATA-SCHEME.
Covers: R6-05, R6-06, R6-07, R6-09.
D05 unapproved: period, edit rights, counting basis, remaining formula and warn/block policy require a recorded decision. Do not score observed behavior as an agreed rule.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. View MOEFAS and School A SBFAS granted statistics.
   Expected: Correct FAS type, authorized school and period displayed.
2. Compare totals with two counted grants 40 and 60.
   Expected: Total 100 under agreed definition; no pending/rejected/other-school amount included.
3. Change filters/school role and repeat the same query.
   Expected: Totals stable/reproducible for selected scope; no cross-school leakage or duplicate counting.

Watch for: Do not count a percentage setting itself as spent funds; confirm actual monetary basis.
```

#### 3. Kết Quả Thực Tế (Actual Result)
```
Pass. Two real grants of $30 and $70 were approved and activated. The MOEFAS statistics showed used $100 and remaining $900 from a $1000 budget. A pending $20 grant was shown separately as pending demand, a rejected $50 grant was counted as cancelled, and another school's $25 grant stayed out of the MOEFAS totals. Repeating the query gave identical totals, and independent Billing adjustments for the counted grants total $100.

The level breakdown also includes the pending $20; the used total itself is $100.
```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```
Second pass: moe-statistics.json, moe-confirm-30-70.json, moe-statistics-repeat.json, moe-receipts.json. First pass: moe-statistics-matrix.json, moe-confirm-40-60.json. The receipts file lists the independent Billing adjustments.
```

---

### UAT-040 — Track remaining budget and warnings without guessing grant policy

- **Phân hệ:** `Budget and statistics`
- **Phụ trách:** Josh
- **Vai trò:** HQ / School user
- **Trạng thái:** 🟢 **Pass**

#### 1. Setup, Data & Gate
```
Setup: Utilized amount, remaining calculation and warning thresholds follow the explicitly agreed R6 rule; record any missing basis as a gap. The budget assumption warns rather than blocks and is unapproved; boundary cases use the same rule.
Data: DATA-BUDGET, DATA-FAS.
Gate: FAS access.
Covers: R6-08, R6-10, R6-11.
Replaces definition UAT-034: US-048, US-049. Required variants remain separate; no old result is reused.
D05 unapproved: period, edit rights, counting basis, remaining formula and warn/block policy require a recorded decision. Do not score observed behavior as an agreed rule.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. Open configured 1000 budget with counted use 100.
   Expected: Used 100 and remaining 900 under agreed basis, tied to same scope/period.
2. On reset boundary fixtures reach and exceed available budget.
   Expected: Warnings/remaining presentation follow agreed policy; no hidden count or accidental corruption.
3. Assess another valid application and inspect grant outcome and statistics.
   Expected: Warning-only or blocking behavior matches recorded decision; accounting and displayed totals remain consistent.

Watch for: R6 draft says warn, not block; old backlog says budget-constrained grant. Neither is silently declared authoritative.
```

#### 3. Kết Quả Thực Tế (Actual Result)
```
Pass. The normal scope showed $100 used and $900 remaining from $1000, with pending demand shown separately. In a separate clean copy, an actual $500 subsidy reached used $500 and remaining $0. The next eligible $30 was denied as INSUFFICIENT_BUDGET, and the totals stayed at used $500, remaining $0, pending $30. The stored allocation amounts were exactly 500 and 30, so the pending display and the denial agree. No over-budget grant or Billing subsidy was created.
```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```
Second pass: moe-statistics.json, boundary-pending.json, boundary-confirm-500.json, boundary-at-exhaustion.json, boundary-deny-30.json, boundary-after-block.json, boundary-stored-allocations.json. First pass: moe-boundary-*.json.
```

---

### UAT-MOE-04 — Set the MOEFAS budget

- **Phân hệ:** `Budget and statistics`
- **Phụ trách:** Josh
- **Vai trò:** HQ
- **Trạng thái:** 🟢 **Pass**

#### 1. Setup, Data & Gate
```
Setup: MOE HQ User is logged in and may manage the MOEFAS budget
Data: DATA-BUDGET, DATA-ROLES, DATA-SCHEME. Values: Budget Amount: 1000.00.
Covers: FS06 AC-R6.1.1, AC-R6.1.3.
D05 unapproved: period, edit rights, counting basis, remaining formula and warn/block policy require a recorded decision. Do not score observed behavior as an agreed rule.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. As authorized HQ set MOEFAS budget 1000 and save.
   Expected: The authorized value persists under the agreed period/edit rule.
2. Reopen and compare the saved budget and scope.
   Expected: MOEFAS shows 1000; no school budget was overwritten.

Watch for: D05 remains unapproved. No edit or period rule is inferred from the delivered screen.
```

#### 3. Kết Quả Thực Tế (Actual Result)
```
Pass. The case asks for two things: set a MOEFAS budget and reopen it without overwriting a school budget. Both worked.

An authorised HQ user set a MOEFAS budget of $1000, reopened it and saw $1000, and no school budget was overwritten. The second pass reopened the same scheme at $1000 after the grants.

Separate defect: a saved budget cannot be edited. PUT and PATCH return 405 and the scheme screens are view-only. That is a gap against your edit assumption, recorded separately; it does not change the set-and-reopen result.
```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```
First pass: uat-038/new-scheme-statistics.txt. Second pass: moe-statistics.json. No-overwrite: school-A-statistics.json, school-B-statistics-after.json. Edit attempts: moe-edit-PUT.json, moe-edit-PATCH.json.
```

---

### UAT-MOE-05 — Track MOEFAS statistics and budget usage

- **Phân hệ:** `Budget and statistics`
- **Phụ trách:** Josh
- **Vai trò:** HQ
- **Trạng thái:** 🟢 **Pass**

#### 1. Setup, Data & Gate
```
Setup: MOEFAS budget is set; Some MOEFAS subsidies are already granted
Data: DATA-BUDGET, DATA-ROLES, DATA-SCHEME. Values: Budget Amount: 1000.00.
Covers: FS06 AC-R6.2.1, AC-R6.2.3, AC-R6.3.1, AC-R6.3.3.
D05 unapproved: period, edit rights, counting basis, remaining formula and warn/block policy require a recorded decision. Do not score observed behavior as an agreed rule.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. Open MOEFAS statistics with counted grants 40 and 60 plus excluded controls.
   Expected: Total is 100 only if the stated D05 basis confirms those records count; exclusions and scope hold.
2. Open tracking for budget 1000.
   Expected: Budget 1000, used 100; remaining 900 only if its formula and scope are confirmed. Compare grant IDs, not screen arithmetic alone.

Watch for: D05 is unapproved. Preseeded grant observations do not establish a grant-processing Pass.
```

#### 3. Kết Quả Thực Tế (Actual Result)
```
Pass. The MOEFAS tracking view showed budget $1000, used $100 and remaining $900 after real grants of $30 and $70. The used figure reconciled to the two grant IDs and to independent Billing adjustments totalling $100. A pending $20, a rejected $50 and another school's $25 were excluded from used. Repeating the confirmation did not increase used or the granted count.
```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```
Second pass: moe-statistics.json, moe-confirm-30-70.json, moe-statistics-repeat.json, moe-receipts.json. First pass: moe-statistics-matrix.json, moe-confirm-40-60.json.
```

---

### UAT-MOE-05-E1 — MOEFAS exhaustion and next grant under the agreed policy

- **Phân hệ:** `Budget and statistics`
- **Phụ trách:** Josh
- **Vai trò:** HQ
- **Trạng thái:** 🟢 **Pass**

#### 1. Setup, Data & Gate
```
Setup: Subsidy Amount Used equals or exceeds the MOEFAS Budget Amount
Data: DATA-BUDGET, DATA-ROLES, DATA-SCHEME. Values: Budget Amount: 1000.00; Subsidy Amount Used: 1000.00.
Covers: FS06 R6-11, BR6.06.
Replaces definition UAT-034: US-048, US-049. Required variants remain separate; no old result is reused.
D05 unapproved: period, edit rights, counting basis, remaining formula and warn/block policy require a recorded decision. Do not score observed behavior as an agreed rule.
Gate: FAS access.
Data: DATA-FAS provides one eligible application for 40; use a separately reset scope, not the baseline 100-used copy.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. Open the separate exact-exhaustion copy: budget 1000, counted use 1000.
   Expected: Display matches those amounts under the D05 counting basis; exhaustion presentation follows the recorded rule.
2. Assess one eligible application for 40 through the authorized route.
   Expected: If D05 confirms warning-only, one new grant yields use 1040 and remaining -40 where remaining is in scope. If blocking is confirmed, no grant and use remains 1000. No confirmed policy means Blocked, not Pass.

Watch for: D05 and G3 are unresolved. Warn-only is a draft assumption; capture grant IDs and independent totals. Use a separate reset copy from UAT-040 and the other FAS scope.
```

#### 3. Kết Quả Thực Tế (Actual Result)
```
Pass under your blocking assumption. In a separately reset copy, an actual $500 subsidy exhausted the $500 budget. Preview and confirmation of a further $30 returned INSUFFICIENT_BUDGET. Statistics stayed at used $500 and remaining $0, pending $30, and the denied child received no Billing subsidy. No over-budget grant was created.
```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```
Second pass: boundary-confirm-500.json, boundary-at-exhaustion.json, boundary-deny-30.json, boundary-after-block.json, boundary-stored-allocations.json. First pass: moe-boundary-*.json. The stored allocations are exactly 500 and 30.
```

---

### UAT-SCH-04 — Set and track the SBFAS budget

- **Phân hệ:** `Budget and statistics`
- **Phụ trách:** Josh
- **Vai trò:** School user
- **Trạng thái:** 🟢 **Pass**

#### 1. Setup, Data & Gate
```
Setup: School User is logged in and may manage the SBFAS budget; The school already has granted SBFAS subsidies
Data: DATA-BUDGET, DATA-ROLES. Values: Budget Amount: 1000.00.
Covers: FS06 AC-R6.1.2, AC-R6.3.2.
D05 unapproved: period, edit rights, counting basis, remaining formula and warn/block policy require a recorded decision. Do not score observed behavior as an agreed rule.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. As School A set its separately reset SBFAS budget to 1000.
   Expected: The authorized school budget persists under the recorded period/edit rule.
2. Inspect tracking with counted grants 40 and 60; attempt School B access.
   Expected: Budget 1000 and used 100 under D05; remaining 900 only if confirmed. No cross-school disclosure or change.

Watch for: D05 remains unapproved; use school-specific grants, independent from MOEFAS.
```

#### 3. Kết Quả Thực Tế (Actual Result)
```
Pass. The case asks for two things: set and track a school's SBFAS budget, and keep it separate from another school. Both worked.

School A set its own SBFAS budget to $500 ($1000 in the first pass), reopened it, and saw the amount stay with School A and its period. Real grants of $30 and $70 produced used $100 and remaining $400, matched to separate billing records of $100. School B could not read School A's scheme and got 404; School A could not read School B's. Neither budget changed.

Separate defect: an authorised edit returns 405, recorded separately; it does not change the set, track and isolation result.
```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```
Second pass: school-A-statistics.json, school-A-confirm.json, school-B-statistics-after.json, school-A-cross-denied.json, school-B-cross-denied.json, school-receipts.json. Edit attempts: school-edit-PUT.json, school-edit-PATCH.json. First pass: school-A-matrix.json, school-B-matrix.json.
```

---

### UAT-SCH-04-E1 — SBFAS exhaustion and next grant under the agreed policy

- **Phân hệ:** `Budget and statistics`
- **Phụ trách:** Josh
- **Vai trò:** School user
- **Trạng thái:** 🟢 **Pass**

#### 1. Setup, Data & Gate
```
Setup: The school's Subsidy Amount Used equals or exceeds the SBFAS Budget Amount
Data: DATA-BUDGET, DATA-ROLES. Values: Budget Amount: 1000.00; Subsidy Amount Used: 1000.00.
Covers: FS06 R6-11, BR6.06.
Replaces definition UAT-034: US-048, US-049. Required variants remain separate; no old result is reused.
D05 unapproved: period, edit rights, counting basis, remaining formula and warn/block policy require a recorded decision. Do not score observed behavior as an agreed rule.
Gate: FAS access.
Data: DATA-FAS provides one eligible application for 40; use a separately reset scope, not the baseline 100-used copy.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. Open the separate exact-exhaustion copy: budget 1000, counted use 1000.
   Expected: Display matches those amounts under the D05 counting basis; exhaustion presentation follows the recorded rule.
2. Assess one eligible application for 40 through the authorized route.
   Expected: If D05 confirms warning-only, one new grant yields use 1040 and remaining -40 where remaining is in scope. If blocking is confirmed, no grant and use remains 1000. No confirmed policy means Blocked, not Pass.

Watch for: D05 and G3 are unresolved. Warn-only is a draft assumption; capture grant IDs and independent totals. Use a separate reset copy from UAT-040 and the other FAS scope.
```

#### 3. Kết Quả Thực Tế (Actual Result)
```
Pass under your blocking assumption. In a separately reset school copy, an actual $500 school-authorised subsidy exhausted the $500 SBFAS budget. Preview and confirmation of a further $30 returned INSUFFICIENT_BUDGET. Statistics stayed at used $500 and remaining $0, pending $30, and the denied child received no Billing subsidy. No over-budget grant was created.
```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```
Second pass: school-boundary-at-exhaustion.json, school-boundary-deny-30.json, school-boundary-after-block.json, school-boundary-receipts.json. First pass: school-boundary-*.json.
```

---

