# Phân Hệ: Quyền Truy Cập, View As & Trợ Giúp FAQ (Access and help)

Tổng số: **5** test cases.

| STT | Mã UAT | Tên Kịch Bản | Vai Trò | Người Phụ Trách | Trạng Thái | Kết Quả Thực Tế |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- |
| 1 | **UAT-041** | Enter View As and see the selected role/target without mutation | Authorized HQ viewer | Chan | ⚪ **Not Run** |  |
| 2 | **UAT-042** | View As blocks writes and exits without contaminating sessions | HQ viewer / target observer | Chan | ⚪ **Not Run** |  |
| 3 | **UAT-043** | FAQ answers explain how to use the delivered system | Supported system user | Howard | 🚫 **Blocked** | No AI integration yet |
| 4 | **UAT-044** | FAQ does not look up private data or perform user actions | Supported system user | Howard | 🚫 **Blocked** | No AI integration yet |
| 5 | **UAT-048** | Preserve normal role boundaries across financial and FAS actions | Parent / School / HQ negative controls | Chan | ⚪ **Not Run** |  |

## Chi Tiết Từng Kịch Bản

### UAT-041 — Enter View As and see the selected role/target without mutation

- **Phân hệ:** `Access and help`
- **Phụ trách:** Chan
- **Vai trò:** Authorized HQ viewer
- **Trạng thái:** ⚪ **Not Run**

#### 1. Setup, Data & Gate
```
Setup: View As is read-only per the working assumption. Confirm authority, targets and named view context.
Data: DATA-VIEW, DATA-ROLES.
Covers: ADD-VIEW-AS.
Owner checks: CHAN-UAT-14.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. Enter View As for School A and inspect identity/banner.
   Expected: Mode and target visibly identified; viewer does not silently become a real School A actor.
2. Compare permitted school screen data with same target baseline.
   Expected: Displayed data and actions reflect chosen target scope without unauthorized HQ data.
3. Repeat for permitted Parent A and attempt a prohibited target.
   Expected: Correct family view; unauthorized target denied without leaking its data.

Watch for: Read-only/banners are draft F7 safety proposal, subject to explicit contract confirmation, not general-purpose impersonation.
```

#### 3. Kết Quả Thực Tế (Actual Result)
```

```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```

```

---

### UAT-042 — View As blocks writes and exits without contaminating sessions

- **Phân hệ:** `Access and help`
- **Phụ trách:** Chan
- **Vai trò:** HQ viewer / target observer
- **Trạng thái:** ⚪ **Not Run**

#### 1. Setup, Data & Gate
```
Setup: Approved non-destructive QA probes; API-level write enforcement verification by authorized technical tester complements business UI
Data: DATA-VIEW, DATA-PAY, DATA-FAS.
Covers: ADD-VIEW-AS.
Owner checks: CHAN-UAT-25.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. In View As try profile save, FAS submission/decision, fee publish, payment and top-up using available controls.
   Expected: Read-only proposal prevents every mutation; capture before/after records, not just disabled button screenshots.
2. Have authorized tester attempt corresponding write requests with View As context in isolated QA.
   Expected: Server enforces agreed read-only boundary and preserves balances, records and permissions.
3. Exit View As, reopen original context and inspect real target session/audit.
   Expected: Original actor restored; no stale target access; real user session unaffected per chosen contract; audit distinguishes viewer and target.

Watch for: Every module owner supplies own before/after invariants; no destructive probe on live target data.
```

#### 3. Kết Quả Thực Tế (Actual Result)
```

```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```

```

---

### UAT-043 — FAQ answers explain how to use the delivered system

- **Phân hệ:** `Access and help`
- **Phụ trách:** Howard
- **Vai trò:** Supported system user
- **Trạng thái:** 🚫 **Blocked**

#### 1. Setup, Data & Gate
```
Setup: The draft answer bank, once approved, records the revision, help location and supported user or language scope.
Data: DATA-FAQ.
Covers: ADD-FAQ.
Owner checks: UAT-HOWARD-028.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. Ask the agreed sign-in, balance/history, payment and FAS how-to questions.
   Expected: Answer facts and navigation match the delivered UI and approved answer bank.
2. Ask paraphrases and follow the instructions in a separate normal user session.
   Expected: User can find the described screen/action; no invented buttons, policy or eligibility promises.
3. Ask an unknown/out-of-scope question.
   Expected: Defined honest fallback/support route, not an invented answer.

Watch for: FAQ is simple guidance; no LLM/model/provider, accuracy percentage or conversational engine required.
```

#### 3. Kết Quả Thực Tế (Actual Result)
```
No AI integration yet
```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```

```

---

### UAT-044 — FAQ does not look up private data or perform user actions

- **Phân hệ:** `Access and help`
- **Phụ trách:** Howard
- **Vai trò:** Supported system user
- **Trạng thái:** 🚫 **Blocked**

#### 1. Setup, Data & Gate
```
Setup: Known generic answer bank; record balances/application/payment before-state
Data: DATA-FAQ, DATA-ROLES.
Covers: ADD-FAQ.
Owner checks: UAT-HOWARD-029.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. Ask for another parent balance or a personal payment status.
   Expected: FAQ does not retrieve/disclose private records; may explain how the authorized user can view them normally.
2. Ask the chatbot to pay, top up, submit FAS or alter profile.
   Expected: No state change, transaction, hidden auto-fill or approval; only safe how-to guidance/fallback.
3. Send an instruction to ignore help limits and invent an official assistance rule.
   Expected: No claim of authoritative decision or private action; answer remains within documented system-use help.

Watch for: Security checks are proportionate to actual simple implementation; no unsupported claim that a generative model exists.
```

#### 3. Kết Quả Thực Tế (Actual Result)
```
No AI integration yet
```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```

```

---

### UAT-048 — Preserve normal role boundaries across financial and FAS actions

- **Phân hệ:** `Access and help`
- **Phụ trách:** Chan
- **Vai trò:** Parent / School / HQ negative controls
- **Trạng thái:** ⚪ **Not Run**

#### 1. Setup, Data & Gate
```
Setup: Approved isolated technical controls complement visible menus; BA has confirmed ordinary and View As role rights separately
Data: DATA-ROLES, DATA-TOPUP, DATA-FAS, DATA-SCHEME.
Gate: FAS access.
Covers: US-017, US-028, US-044, US-050.
Owner checks: CHAN-UAT-04.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. As Parent and School user, try the HQ top-up action through delivered entry points.
   Expected: No unauthorized credit, balance change or sensitive recipient disclosure, regardless of hidden menu.
2. As School A user, try School B scheme/application decision via known QA fixture links and authorized request probes.
   Expected: B data is protected and no scheme or grant changes.
3. As HQ inspect permitted MOEFAS configuration and attempt a school decision according to chosen F4 role rule.
   Expected: Only authorized operations succeed; decision actor/audit and unchanged negative-control records are verified.

Watch for: Do not infer access correctness solely from disabled buttons. Retain before/after state; no new production permission change is authorized.
```

#### 3. Kết Quả Thực Tế (Actual Result)
```

```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```

```

---

