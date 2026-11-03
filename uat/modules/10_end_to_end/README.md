# Phân Hệ: Hành Trình Nghiệp Vụ Xuyên Suốt (End-to-End Journeys) (End-to-end)

Tổng số: **2** test cases.

| STT | Mã UAT | Tên Kịch Bản | Vai Trò | Người Phụ Trách | Trạng Thái | Kết Quả Thực Tế |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- |
| 1 | **UAT-045** | Rehearse online FAS through school review, subsidy and payment | Parent -> School/System -> Parent | Howard | 🟡 **In Progress** |  |
| 2 | **UAT-046** | Rehearse paper application through assessment and parent result | School -> System/School -> Parent where authorized | Chan | ⚪ **Not Run** |  |

## Chi Tiết Từng Kịch Bản

### UAT-045 — Rehearse online FAS through school review, subsidy and payment

- **Phân hệ:** `End-to-end`
- **Phụ trách:** Howard
- **Vai trò:** Parent -> School/System -> Parent
- **Trạng thái:** 🟡 **In Progress**

#### 1. Setup, Data & Gate
```
Setup: Component owners have current-build readiness evidence; one linked child/charge used throughout; all listed decisions resolved for this route
Data: DATA-ROLES, DATA-SCHOOL, DATA-FAS, DATA-SCHEME, DATA-FEES, DATA-PAY, DATA-BUDGET.
Gate: FAS access; school dates.
Covers: US-041, US-050, US-051, US-010, US-011, US-014, US-015, US-053.
Replaces definition UAT-037: US-051, US-040. Required variants remain separate; no old result is reused.
D05: any grant affected by available budget follows the explicitly agreed policy, not an assumed warning-only or blocking rule.
Owner checks: UAT-HOWARD-013, UAT-HOWARD-026, UAT-HOWARD-027.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. Parent submits known complete application; reviewer opens same application ID.
   Expected: Identity, income, document and child agree across portals; correct school/system reviewer receives it.
2. Run agreed assessment/review and apply 40 subsidy to original 100 charge.
   Expected: Attributable decision, original 100, subsidy 40, net 60; parent result and fee view agree.
3. Parent pays net 60 using independent EA 40 plus online 20 allocation.
   Expected: One invoice settled, EA net debit 40 and gateway 20; receipt total 60 and history agree.
4. Reopen parent/admin/grant/budget views and compare entity links.
   Expected: All views reconcile, no duplicate grant/payment, authorized scope preserved; budget follows chosen accounting.

Watch for: Each owner signs off their handoff evidence. QA rehearsal is not business acceptance.
```

#### 3. Kết Quả Thực Tế (Actual Result)
```

```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```

```

---

### UAT-046 — Rehearse paper application through assessment and parent result

- **Phân hệ:** `End-to-end`
- **Phụ trách:** Chan
- **Vai trò:** School -> System/School -> Parent where authorized
- **Trạng thái:** ⚪ **Not Run**

#### 1. Setup, Data & Gate
```
Setup: Known paper identity and any parent linkage; chosen MOEFAS/SBFAS routing/timing contract. No-EA branch has separately agreed result visibility
Data: DATA-CSV, DATA-FAS, DATA-SCHEME, DATA-SCHOOL, DATA-ROLES.
Gate: FAS access.
Covers: US-042, US-043, US-049, US-050, US-010.
D05: any grant affected by available budget follows the explicitly agreed policy, not an assumed warning-only or blocking rule.
Owner checks: CHAN-UAT-24.
```

#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)
```
1. School scans/types and confirms corrected application.
   Expected: One paper application with correct provenance/household/support reaches review.
2. Run the selected assessment trigger and school-decision branch on independent data.
   Expected: Correct route and final or pending result, with no OCR auto-grant or unauthorized HQ decision.
3. Inspect review/audit and authorized parent result for the linked-child branch.
   Expected: Same decision/details appear; no assumption that a no-EA unlinked parent can access a portal result.

Watch for: Record no-EA paper flow and linked-parent visibility as distinct variants.
```

#### 3. Kết Quả Thực Tế (Actual Result)
```

```

#### 4. Bằng Chứng / Defect (Evidence / Defect)
```

```

---

