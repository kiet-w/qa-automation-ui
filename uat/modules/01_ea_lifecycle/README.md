# Phân Hệ: Vòng Đời Tài Khoản Giáo Dục (Education Account) (EA lifecycle)

Tổng số: **4** test cases.

| STT | Mã UAT | Tên Kịch Bản | Vai Trò | Người Phụ Trách | Trạng Thái | Kết Quả Thực Tế |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- |
| 1 | **UAT-001** | Provision eligible education accounts without duplicates | HQ / system | Josh | 🟢 **Pass** | Pass. A fresh set of six children went through the delivered simulator and sync.<br><br>Eligible and provisioned: a 7-year-old... |
| 2 | **UAT-002** | Run the daily newly-seven provision and repeat safely | System / HQ observer | Josh | 🟢 **Pass** | Pass. The delivered daily job method ran twice for the 29 October 2019 birthday cohort on a copied database.<br><br>One new se... |
| 3 | **UAT-003** | Close an eligible account before viewing or financial activity | Parent / HQ | Josh | 🔴 **Fail** | Fail. In a clean copy, a 16-year-old citizen account was Active at $40.00. The top-up search showed age 16, status Activ... |
| 4 | **UAT-004** | Settle residual funds to the CPF simulator exactly once | System / HQ observer | Josh | 🔴 **Fail** | Fail. The closure attempt for the 16-year-old with $40.00 returned 400: 'Cannot perform transaction on a wallet with sta... |

## Chi Tiết Từng Kịch Bản

### UAT-001 — Provision eligible education accounts without duplicates

- **Phân hệ:** `EA lifecycle`
- **Phụ trách:** Josh
- **Vai trò:** HQ / system
- **Trạng thái:** 🟢 **Pass**

#### 1. Setup, Data & Gate
```
Setup: Authorized isolated initial-sync trigger and agreed identity contract; fresh fixture partition
Data: DATA-ROLES, DATA-LIFE.
Gate: lifecycle.
Covers: US-001.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. Run initial synchronization for the known citizen set.
   Expected: Only eligible valid SC records aged 7 to below 16 receive one EA linked to the correct student.
2. Compare age/noncitizen/missing optional-parent controls.
   Expected: Ineligible records do not get EAs; absent parent NRIC alone does not reject an otherwise valid citizen.
3. Rerun the agreed provisioning flow and inspect identities/balances.
   Expected: No duplicate EA, no opening money movement; new accounts Active with SGD 0.00 under R1 draft.

Watch for: One correct EA per eligible citizen; school enrolment is not an account-creation prerequisite.
```

#### 3. Kết Quả Thực Tế (Actual Result)
```
Pass. A fresh set of six children went through the delivered simulator and sync.

Eligible and provisioned: a 7-year-old citizen with no school record, a 15-year-old citizen with no school record, and a citizen one day short of 16 with a school record. Each got one Active account at $0.00 with a single opening entry.

Not provisioned: a 7-year-old permanent resident with a school record, a citizen one month short of 7 with a school record, and a citizen who turned 16 that day with a school record. None got an account.

Repeating the same runs changed nothing. The no-school 7-year-old also covers the case note that school enrolment is not a prerequisite.
```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```
Second pass: uat001-fixtures.json, uat001-state-first.json, uat001-state-second.json, uat001-sync-first.json, uat001-sync-second.json. First pass: initial-controls-state.json. The state files list each NRIC, whether a wallet exists, its status, balance and ledger count.
```

---

### UAT-002 — Run the daily newly-seven provision and repeat safely

- **Phân hệ:** `EA lifecycle`
- **Phụ trách:** Josh
- **Vai trò:** System / HQ observer
- **Trạng thái:** 🟢 **Pass**

#### 1. Setup, Data & Gate
```
Setup: Owned controllable business date; existing student with changed government address
Data: DATA-LIFE.
Gate: lifecycle.
Covers: US-002.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. Advance to the recorded seventh birthday and invoke the delivered daily trigger.
   Expected: Newly-seven eligible citizen is processed on the agreed date.
2. Inspect the older existing student profile and daily query set.
   Expected: Daily incremental flow does not refresh all older profiles under R1 v1.2.
3. Repeat the job for the same date.
   Expected: Exactly one EA remains; no additional financial entry.

Watch for: Record the clock and scheduler evidence; do not substitute parent login for a scheduled-job demonstration.
```

#### 3. Kết Quả Thực Tế (Actual Result)
```
Pass. The delivered daily job method ran twice for the 29 October 2019 birthday cohort on a copied database.

One new seven-year-old got exactly one Active account at $0.00 with one opening entry. An older child whose government address had changed kept the old address. An existing account in the same cohort kept the same balance and ledger count. The second run changed nothing, and two COMPLETED single-birthday rows appeared in the job log.

Limit: the midnight timer itself was not observed. The delivered method was called through a small QA adapter, and the published assembly hash is recorded.
```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```
Second pass: uat002-entry-1.json, uat002-entry-2.json, uat002-logs.json. First pass: daily-entry-1.json, daily-entry-2.json, daily-persisted-job-logs.json. The entry files record the assembly SHA-256, target birth date and before/after state.
```

---

### UAT-003 — Close an eligible account before viewing or financial activity

- **Phân hệ:** `EA lifecycle`
- **Phụ trách:** Josh
- **Vai trò:** Parent / HQ
- **Trạng thái:** 🔴 **Fail**

#### 1. Setup, Data & Gate
```
Setup: The lifecycle gate must settle age, citizenship, positive-balance behavior and the current build trigger. Use independent reset copies for each financial action.
Data: DATA-LIFE, DATA-ROLES, DATA-PAY, DATA-TOPUP.
Gate: lifecycle.
Covers: US-003.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. Access a below-16 citizen control and an exactly-16 zero-balance account.
   Expected: Control remains Active; the eligible account shows exactly the status and closure date stated by the recorded G2 answer. No other value is accepted, and until G2 answers, the observed status is recorded as conditional.
2. Attempt top-up and payment on closure-eligible accounts, including one whose persisted state was Active.
   Expected: Eligibility check prevents new ineligible financial activity; no wrong debit/credit.
3. Open the same account again after the closure check and inspect allowed history.
   Expected: No duplicate closure; authorized historical viewing remains available; status/date remain consistent.

Watch for: Student profile state is not used as a substitute for EA state.
```

#### 3. Kết Quả Thực Tế (Actual Result)
```
Fail. In a clean copy, a 16-year-old citizen account was Active at $40.00. The top-up search showed age 16, status Active and 'eligible for top-up'. A $1.00 credit then succeeded, taking the balance to $41.00. No closure date or closed status was applied.

The closure endpoint returned 400 because the wallet was closed inside the transaction before the debit, the same ordering defect as UAT-004. The financial restriction is missing: the account takes new money after the age limit.

The exact status label is still an open lifecycle question, but it does not change the failure.
```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```
Second pass: uat003-search-before-credit.json, uat003-credit-and-state.json, uat004-validate-and-state.json. First pass: uat-004/credit-attempt-on-16yo.txt, uat-004/state-after-validate.txt.
```

---

### UAT-004 — Settle residual funds to the CPF simulator exactly once

- **Phân hệ:** `EA lifecycle`
- **Phụ trách:** Josh
- **Vai trò:** System / HQ observer
- **Trạng thái:** 🔴 **Fail**

#### 1. Setup, Data & Gate
```
Setup: Current CPF mock contract, identity mapping, allowed trigger and failure/query controls supplied. The lifecycle gate must be closed.
Data: DATA-LIFE.
Gate: lifecycle.
Covers: US-004.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. Trigger eligible closure with residual SGD 40.
   Expected: Transfer follows agreed lifecycle; account and CPF result are linked, with exactly 40 settled on success.
2. Query CPF outcome, EA balance and ledger rather than trusting a success banner.
   Expected: No lost or duplicated funds; confirmed success and final account state agree.
3. Repeat access and separately test a definitively failed CPF response.
   Expected: Confirmed transfer is not repeated; failure does not claim settlement or discard the 40.

Watch for: No real CPF integration claim; retain success and failure as separately reset variants.
```

#### 3. Kết Quả Thực Tế (Actual Result)
```
Fail. The closure attempt for the 16-year-old with $40.00 returned 400: 'Cannot perform transaction on a wallet with status Closed'. The student and wallet stayed Active at $40.00, and no settlement or ledger entry was created.

The cause is ordering. The lifecycle code closes the wallet first and only then debits the residual balance, so the debit fails. A CPF outage is swallowed and cannot be distinguished from success. The CPF simulator's own DI error is a second, separate defect.

No funds are lost, but no settlement happens and the account is not closed.
```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```
Second pass: uat004-validate-and-state.json. First pass: uat-004/cpf-accounts.txt, uat-004/cpf-log-lines.txt, uat-004/validate-1.txt. Root cause: Student.EvaluateAndApplyLifecycle -> Deactivate -> Wallet.Close, then StudentLifecycleService debits the closed wallet.
```

---

