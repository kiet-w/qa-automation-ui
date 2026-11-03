# Phân Hệ: Nạp Tiền Vào Tài Khoản Giáo Dục (Top-Up) (Top-up)

Tổng số: **6** test cases.

| STT | Mã UAT | Tên Kịch Bản | Vai Trò | Người Phụ Trách | Trạng Thái | Kết Quả Thực Tế |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- |
| 1 | **UAT-022** | Credit an individual account after review and confirmation | HQ | Josh | 🟢 **Pass** | Pass. Real browser run. The search found the right child at $30.00. Review showed current $30.00, top-up $5.00 and proje... |
| 2 | **UAT-023** | Configure a bulk top-up and verify the exact preview set | HQ | Josh | 🔴 **Fail** | Fail. The campaign saves and the preview itself is correct: 3 eligible accounts and a $60.00 forecast, with no balance o... |
| 3 | **UAT-024** | Execute bulk top-up once and reconcile results | HQ | Josh | 🔴 **Fail** | Fail. A clean three-account campaign at $1.00 each ran correctly the first time: 3 targeted, 3 success, $3.00 paid, each... |
| 4 | **UAT-025** | Recover a partially failed bulk top-up without re-crediting successes | HQ | Josh | 🔴 **Fail** | Fail. A clean three-account campaign at $1.00 each previewed 3 accounts and $3.00. One wallet was closed after the previ... |
| 5 | **UAT-026** | Schedule a top-up for an agreed future date and time | HQ / system | Josh | 🟢 **Pass** | Pass on the scheduling behaviour, with a separate timestamp defect. A campaign was saved for a future time and stayed Sc... |
| 6 | **UAT-027** | Correct a mistaken individual top-up with preserved history | Authorized HQ | Josh | 🔴 **Fail** | Fail. The product has a reversal endpoint, but it is registered as an internal route. Through the gateway it returns 404... |

## Chi Tiết Từng Kịch Bản

### UAT-022 — Credit an individual account after review and confirmation

- **Phân hệ:** `Top-up`
- **Phụ trách:** Josh
- **Vai trò:** HQ
- **Trạng thái:** 🟢 **Pass**

#### 1. Setup, Data & Gate
```
Setup: Use the top-up gate contract for search, amount and reason; reset the EA at 10.
Data: DATA-ROLES, DATA-TOPUP.
Gate: top-up; lifecycle.
Covers: US-028, US-032.
Owner checks: UAT-HOWARD-007.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. Search exact intended account, enter top-up 20 and reason, then review.
   Expected: Correct recipient, current 10, amount 20 and projected 30 are visible before consent.
2. Cancel once and inspect balance; then confirm a fresh valid attempt.
   Expected: Cancel changes nothing; confirmed success creates exactly one 20 credit and balance 30.
3. Inspect HQ history and parent history; query/retry the same known result per contract.
   Expected: One attributable movement and matching balance; no duplicate credit on replay.

Watch for: Use top-up, not campaign, in user-facing wording. Money precision and Closed-account regressions remain linked functional checks.
```

#### 3. Kết Quả Thực Tế (Actual Result)
```
Pass. Real browser run. The search found the right child at $30.00. Review showed current $30.00, top-up $5.00 and projected $35.00. Back left the wallet at $30.00 with the same ledger. A fresh attempt confirmed once and produced exactly one $5.00 credit to $35.00.

HQ history listed the single reference, and parent history returned the same reference at $35.00. Replaying the reference returned the existing transaction and changed neither the balance nor the ledger.
```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```
Second pass: topup-second-review.txt, topup-second-review.png, topup-second-confirmed.txt, topup-second-result.png, topup-second-after-back.json, topup-second-history-hq.json, topup-second-history-parent.json, topup-second-reconcile.json. First pass: topup-review.txt, topup-result.png, topup-hq-history.png.
```

---

### UAT-023 — Configure a bulk top-up and verify the exact preview set

- **Phân hệ:** `Top-up`
- **Phụ trách:** Josh
- **Vai trò:** HQ
- **Trạng thái:** 🔴 **Fail**

#### 1. Setup, Data & Gate
```
Setup: Decision records identify criteria, AND/OR, eligibility date, budget and schooling behavior; expected ID set is written before preview
Data: DATA-TOPUP, DATA-SCHOOL.
Gate: top-up.
Covers: US-029, US-030.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. Configure chosen age/balance/enrolment criteria and per-account 20.
   Expected: Saved values reopen exactly as configured; criteria meaning is explicit.
2. Preview boundary/multiple-match/ineligible controls.
   Expected: Returned ID set, exclusion reasons, count and forecast match agreed rules; no duplicates or ledger movements.
3. Change criteria/amount and cancel confirmation.
   Expected: Obsolete preview cannot authorize an unintended run; cancellation changes no balance.

Watch for: For three eligible accounts forecast is 60. Formula/control support must match chosen contract, not implementation guesswork.
```

#### 3. Kết Quả Thực Tế (Actual Result)
```
Fail. The campaign saves and the preview itself is correct: 3 eligible accounts and a $60.00 forecast, with no balance or ledger movement. But the product's own Save and Preview button sends the browser to /top-up/campaigns/{id}/preview, which shows 404 Page Not Found. The registered route is /top-up/bulks/{id}/preview, and the same preview loads there.

A user following the normal button cannot reach the preview. The reopen-exact-values and changed-criteria-cancel variants were not completed; the routing failure is enough for a Fail.
```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```
Second pass: topup-second-save-preview.txt, topup-second-save-preview-404.png. First pass: uat-023/defect-404-after-save.png, uat-023/defect-route-grep.txt, uat-023/before-preview.txt, uat-023/after-preview.txt.
```

---

### UAT-024 — Execute bulk top-up once and reconcile results

- **Phân hệ:** `Top-up`
- **Phụ trách:** Josh
- **Vai trò:** HQ
- **Trạng thái:** 🔴 **Fail**

#### 1. Setup, Data & Gate
```
Setup: Confirmed 3-account preview, each at 10, amount 20; current delivery fixes build blockers
Data: DATA-TOPUP.
Gate: top-up.
Covers: US-031, US-032.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. Review current recipients/total and confirm the run.
   Expected: Explicit consent relates to this definition and forecast, with no accidental execution.
2. Read completed result and independent balances/items.
   Expected: Three successful items, total 60; each balance 30; individual movements and run totals reconcile.
3. Cancel a repeat prompt and exercise same-request replay separately.
   Expected: Cancel adds nothing; replay follows agreed one-run/repeat policy without unintended extra credit.

Watch for: A new deliberately authorized distribution is different from retrying the same operation; the top-up gate must define the distinction.
```

#### 3. Kết Quả Thực Tế (Actual Result)
```
Fail. A clean three-account campaign at $1.00 each ran correctly the first time: 3 targeted, 3 success, $3.00 paid, each balance $7.77 to $8.77. Running the same completed campaign again created a second batch and paid the same three accounts again: 3 targeted, 3 success, another $3.00, balances $9.77. The campaign stayed Active.

A completed immediate campaign therefore re-credits instead of following a one-run or idempotent repeat policy. A separate defect also records every batch start seven hours late.
```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```
Second pass: uat024-preview.json, uat024-execution.json. First pass: uat-024/after-run-sql.txt, uat-024/after-replay-attempt.txt, uat-024/replay-batch-detail.txt.
```

---

### UAT-025 — Recover a partially failed bulk top-up without re-crediting successes

- **Phân hệ:** `Top-up`
- **Phụ trách:** Josh
- **Vai trò:** HQ
- **Trạng thái:** 🔴 **Fail**

#### 1. Setup, Data & Gate
```
Setup: Known per-item definitive fault, outcome query and chosen recovery workflow under the top-up gate.
Data: DATA-TOPUP.
Gate: top-up.
Covers: US-031, US-032.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. Execute 3-account top-up with one controlled definitive failure.
   Expected: Two successes credit 40; failed account stays at 10 and has an identifiable result/reason.
2. Inspect results and select the agreed failed-record recovery.
   Expected: Recovery uses actual failed outcomes, not a fresh broad profile rule or 20 separate manual credits.
3. Clear the fault, retry and compare all balances/references.
   Expected: Only failed account receives 20; each closes at 30, total intended distribution 60, prior successes unchanged.

Watch for: Unresolved outcome is queried before retry. Record request/run/item linkage and recovery evidence; absent recovery remains a blocker.
```

#### 3. Kết Quả Thực Tế (Actual Result)
```
Fail. A clean three-account campaign at $1.00 each previewed 3 accounts and $3.00. One wallet was closed after the preview. The run then reported 2 targeted, 2 success, 0 failed and 0 skipped, and paid $2.00. The closed account stayed at $7.77.

It has no item row and no failure or skip record, so the run cannot name what failed, and the Retry failed control has nothing to act on. The recovery half could not be scored because the product never records the failure.
```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```
Second pass: uat025-execution.json. First pass: uat-025/fixture.txt, uat-025/fault-injected.txt, uat-025/preview.txt, uat-025/after-run.txt.
```

---

### UAT-026 — Schedule a top-up for an agreed future date and time

- **Phân hệ:** `Top-up`
- **Phụ trách:** Josh
- **Vai trò:** HQ / system
- **Trạng thái:** 🟢 **Pass**

#### 1. Setup, Data & Gate
```
Setup: The top-up gate must settle supported scheduling behavior, timezone and safe isolated clock and worker controls.
Data: DATA-TOPUP.
Gate: top-up.
Covers: US-029, US-031.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. Save a future top-up and reopen its schedule.
   Expected: Exact agreed local date/time/timezone retained; no immediate credit.
2. Inspect before due time, then advance the approved business clock/trigger.
   Expected: No early distribution; due execution follows chosen timing and eligibility policy.
3. Inspect run/history and repeat worker wake-up after completion.
   Expected: One intended distribution with attributable scheduled trigger; no duplicate credit.

Watch for: Not assumed delivered. If no scheduling capability is supplied, record blocked against the in-scope customer concern rather than replacing it with manual execution.
```

#### 3. Kết Quả Thực Tế (Actual Result)
```
Pass on the scheduling behaviour, with a separate timestamp defect. A campaign was saved for a future time and stayed Scheduled before the due time. At the due second it produced one batch with 3 targeted and 3 successful credits, $3.00, and no duplicate on the next worker wake-up. The batch is attributable to SYSTEM_SCHEDULER and the correct campaign.

Separate defect: every batch records started_at about seven hours after the real UTC time. This run was scheduled for 11:29 UTC and recorded 18:29. That does not change the schedule, the credits or the duplicate check, but the audit time must be fixed.

The earlier zero-targeted result was a fixture error: the campaign's maximum balance was $10.00 while the cohort had already been topped up to $30.00.
```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```
Second pass: uat026-created.json, uat026-result.json. First pass: uat-026/clock-offset.txt, uat-026/after-due.txt, uat-026/batch-row.txt. The result file shows the scheduled time, the batch counts and the seven-hour gap.
```

---

### UAT-027 — Correct a mistaken individual top-up with preserved history

- **Phân hệ:** `Top-up`
- **Phụ trách:** Josh
- **Vai trò:** Authorized HQ
- **Trạng thái:** 🔴 **Fail**

#### 1. Setup, Data & Gate
```
Setup: The top-up gate must settle correction authority, adjustment and reversal method, limits and insufficient-balance behavior.
Data: DATA-TOPUP.
Gate: top-up.
Covers: US-033.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. Create a known mistaken top-up of 20 on opening 10.
   Expected: Original credit and resulting 30 are attributable and retained.
2. Apply the agreed authorized full correction with reason.
   Expected: Compensating outcome restores intended 10 and links to the original; no destructive history rewrite.
3. Inspect history and repeat the same correction request.
   Expected: Original/correction entries reconcile; no repeated debit or unsupported negative balance.

Watch for: Historical To Do/deferred labels do not remove this story from the completeness register. Missing mechanism is a blocker.
```

#### 3. Kết Quả Thực Tế (Actual Result)
```
Fail. The product has a reversal endpoint, but it is registered as an internal route. Through the gateway it returns 404 'Resource not found'. Direct to the service it returns 403 because the service expects gateway headers, not a user token. The top-up screens have no Correct or Reverse action: the history view offers only search, reset and paging.

An authorised HQ user therefore has no route to correct a mistaken top-up, and the required linked compensating entry cannot be created.
```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```
Second pass: uat027-gateway-reverse.json. First pass: uat-027/8-direct-service.txt, uat-027/4-reverse.txt. UI: the top-up history tab has only search, reset and paging; no Correct or Reverse action.
```

---

