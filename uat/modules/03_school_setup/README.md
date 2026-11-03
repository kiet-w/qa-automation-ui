# Phân Hệ: Thiết Lập Dữ Liệu Trường & Học Sinh (School setup)

Tổng số: **6** test cases.

| STT | Mã UAT | Tên Kịch Bản | Vai Trò | Người Phụ Trách | Trạng Thái | Kết Quả Thực Tế |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- |
| 1 | **UAT-013** | Create and deactivate school master data without losing history | HQ / School user | Chan | ⚪ **Not Run** |  |
| 2 | **UAT-014** | School user signs in with AAD and receives correct school scope | Admin / School user | Chan | ⚪ **Not Run** |  |
| 3 | **UAT-015** | Maintain academic structure, students and EA identity links | School user | Chan | ⚪ **Not Run** |  |
| 4 | **UAT-016** | Enrol and move a student while preserving history | School user / HQ observer | Chan | ⚪ **Not Run** |  |
| 5 | **UAT-017** | Transfer between schools without losing identity or placement history | Authorized sending/receiving school users | Chan | ⚪ **Not Run** |  |
| 6 | **UAT-018** | Import academic and student data with per-row outcomes | School user | Chan | ⚪ **Not Run** |  |

## Chi Tiết Từng Kịch Bản

### UAT-013 — Create and deactivate school master data without losing history

- **Phân hệ:** `School setup`
- **Phụ trách:** Chan
- **Vai trò:** HQ / School user
- **Trạng thái:** ⚪ **Not Run**

#### 1. Setup, Data & Gate
```
Setup: Delivered master-data actions and synthetic unique school code
Data: DATA-ROLES, DATA-SCHOOL.
Covers: US-016.
Owner checks: CHAN-UAT-01, CHAN-UAT-02.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. Create School A with a unique code; reopen and edit permitted details.
   Expected: Correct code/name/type persist; linked historical student and charge records remain identifiable.
2. Attempt the same school code again.
   Expected: The confirmed uniqueness rule prevents a second school with that code; record the actual validation.
3. Deactivate a separate historical school; inspect history and try new school assignment/publication.
   Expected: History remains; new actions follow the recorded inactive-school rule, with no cross-school leakage. Unagreed restrictions stay conditional.

Watch for: CHAN-UAT-01, CHAN-UAT-02. Do not deactivate shared journey fixtures.
```

#### 3. Kết Quả Thực Tế (Actual Result)
```

```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```

```

---

### UAT-014 — School user signs in with AAD and receives correct school scope

- **Phân hệ:** `School setup`
- **Phụ trách:** Chan
- **Vai trò:** Admin / School user
- **Trạng thái:** ⚪ **Not Run**

#### 1. Setup, Data & Gate
```
Setup: Named Microsoft/AAD test integration or explicit mock; school assignment and first-login fields mapped
Data: DATA-ROLES, DATA-SCHOOL, DATA-CSV.
Covers: US-017, US-018.
Source checks: CHAN-UAT-03, CHAN-UAT-04, CHAN-UAT-16. DATA-CSV supplies a delivered school-user template and valid/unknown-school rows if CSV is the provisioning route.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. Use delivered authorized school-user setup. If CSV is the route, download its template, import a valid School A row and an unknown-school row separately.
   Expected: Only the valid assignment is created; unknown school has a row-specific error and no assignment. Record the route and import receipt.
2. Sign in through Microsoft/AAD and complete permitted first-login details.
   Expected: The assigned user reaches School A; permitted details persist. Label a mock instead of claiming real AAD integration.
3. Try an unassigned Microsoft user, School B links and HQ-only school/user-management links as School A.
   Expected: Authentication alone grants no assignment; school/HQ boundaries hold and no unauthorized data or changes occur.

Watch for: CHAN-UAT-03, CHAN-UAT-04, CHAN-UAT-16. If setup uses another authorized route, record CSV import as Not Run follow-up, not a passed import.
```

#### 3. Kết Quả Thực Tế (Actual Result)
```

```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```

```

---

### UAT-015 — Maintain academic structure, students and EA identity links

- **Phân hệ:** `School setup`
- **Phụ trách:** Chan
- **Vai trò:** School user
- **Trạng thái:** ⚪ **Not Run**

#### 1. Setup, Data & Gate
```
Setup: School user authorized for A; independent SC, PR and international student fixtures
Data: DATA-SCHOOL, DATA-LIFE.
Covers: US-019, US-020, US-021.
Source checks: CHAN-UAT-05, CHAN-UAT-06, CHAN-UAT-07, CHAN-UAT-17, CHAN-UAT-18, CHAN-UAT-19. Include duplicate class/NRIC and mismatched EA controls; preserve original IDs and balances.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. Create current-year levels/class and student records, including a valid PR/no-EA student; reopen them.
   Expected: Values persist within School A; no EA is required merely to keep a student/enrolment record.
2. Try the same class code in the same level/year and an existing NRIC as a new student.
   Expected: Confirmed uniqueness rules leave one class and one student identity; originals and history remain unchanged.
3. Link an SC student to its matching existing EA, then repeat; compare balance.
   Expected: Exactly one matching link, no second EA/student and no money movement.
4. Try a mismatched EA and the ineligible PR/international linking controls.
   Expected: No unrelated EA link or balance change; valid student/enrolment records remain.

Watch for: CHAN-UAT-05 to 09, CHAN-UAT-17 to 19. Enrolment and assignment are completed in UAT-016. Missing exact uniqueness/link rules remain conditional.
```

#### 3. Kết Quả Thực Tế (Actual Result)
```

```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```

```

---

### UAT-016 — Enrol and move a student while preserving history

- **Phân hệ:** `School setup`
- **Phụ trách:** Chan
- **Vai trò:** School user / HQ observer
- **Trạng thái:** ⚪ **Not Run**

#### 1. Setup, Data & Gate
```
Setup: Agreed academic effective dates; independent student with known prior placement
Data: DATA-SCHOOL.
Gate: school dates.
Covers: US-022, US-023, US-025.
Source checks: CHAN-UAT-08, CHAN-UAT-09, CHAN-UAT-10, CHAN-UAT-20, CHAN-UAT-21, CHAN-UAT-26, CHAN-UAT-27. Supply prior/current years, overlap copies, inactive and final-level students; G4 settles progression rules.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. Enrol an existing un-enrolled student and assign a class at the agreed dates.
   Expected: One correct school/year/level/class placement, with the existing student identity reused.
2. Try duplicate/overlapping enrolment and the same class assignment again.
   Expected: The agreed rule rejects or reuses the original; exactly one current placement, with no extra history row.
3. Move class at the agreed boundary; preview/confirm annual progression, including final-level controls; repeat.
   Expected: Current placement changes at the agreed date, history remains, no duplicate progression, invalid next level or new charge.
4. Compare current/history as School A and HQ, then try School B and the linked parent.
   Expected: Permitted placement/history match; another school/family cannot view or alter protected records.

Watch for: CHAN-UAT-08 to 10, CHAN-UAT-20, CHAN-UAT-21, CHAN-UAT-26, CHAN-UAT-27. Progression and terminal-level outcomes follow G4; use isolated copies.
```

#### 3. Kết Quả Thực Tế (Actual Result)
```

```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```

```

---

### UAT-017 — Transfer between schools without losing identity or placement history

- **Phân hệ:** `School setup`
- **Phụ trách:** Chan
- **Vai trò:** Authorized sending/receiving school users
- **Trạng thái:** ⚪ **Not Run**

#### 1. Setup, Data & Gate
```
Setup: Transfer permissions and effective dates agreed; separate sending/receiving school identities
Data: DATA-SCHOOL, DATA-FEES.
Gate: school dates.
Covers: US-024, US-025.
Source checks: CHAN-UAT-11, CHAN-UAT-23. Kent supplies an original posted SGD 100 charge and a separate future-rate fixture under DATA-FEES.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. Record transfer out of A and into B using authorized actors and agreed effective dates.
   Expected: The same identity is reused; no overlapping current placement or unauthorized school privilege.
2. Inspect school IDs, current placement and history in authorized school/HQ/parent views.
   Expected: Correct receiving-school ID; old placement remains and unauthorized school access is refused.
3. Reopen the original posted A charge after transfer and a future rate change; preview a later B publication.
   Expected: Original A charge ID, enrolment and amount stay unchanged. Future B recipients/rates follow the agreed date, without duplicating old charges.

Watch for: CHAN-UAT-11, CHAN-UAT-23. Kent supplies original charge and future-rate receipts; do not reuse payment fixtures for transfer.
```

#### 3. Kết Quả Thực Tế (Actual Result)
```

```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```

```

---

### UAT-018 — Import academic and student data with per-row outcomes

- **Phân hệ:** `School setup`
- **Phụ trách:** Chan
- **Vai trò:** School user
- **Trạng thái:** ⚪ **Not Run**

#### 1. Setup, Data & Gate
```
Setup: Approved small CSVs using delivered templates; expected row outcomes documented
Data: DATA-CSV, DATA-SCHOOL.
Gate: school dates.
Covers: US-026, US-027.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. Preview academic structure CSV containing valid/invalid references.
   Expected: Rows, validation issues and intended changes are visible before commit.
2. Import student CSV including optional empty class, duplicate and invalid reference.
   Expected: Accepted/rejected rows follow agreed contract and identify row-specific outcomes; no cross-school insertion.
3. Reconcile lists, enrolments and row totals, then retry only as permitted.
   Expected: Every row accounted for; no unexplained partial creation or silent duplicate on retry.

Watch for: Capture original file and row-result export; do not claim all-or-nothing unless the selected contract requires it.
```

#### 3. Kết Quả Thực Tế (Actual Result)
```

```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```

```

---

