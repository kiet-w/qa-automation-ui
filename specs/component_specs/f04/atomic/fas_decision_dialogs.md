# Component Spec: FAS Approval & Rejection Dialogs (`fas_decision_dialogs`)

## 1. Metadata & Selector
- **Component ID**: `F04-COMP-DECISION-DIALOGS`
- **Component Name**: FAS Approval & Rejection Confirmation Dialogs (`Screen E, F, G`)
- **Module**: `f04` (Assess FAS & Apply Subsidies)
- **Target Route**: Triggered from FAS Review Drawer (`/admin/fas/applications`)
- **Target Roles**:
  - `School Admin`: Approves / Rejects SBFAS (Screen E & G).
  - `MOE HQ User`: Approves / Rejects MOEFAS (Screen F & G).
- **Element Tag**: `<dialog role="alertdialog" aria-modal="true" aria-labelledby="fas-decision-dialog-title">`

### Playwright Locators (BSK Live DOM Standard)
```typescript
export const fasDecisionLocators = {
  // Screen E & F: Approve FAS Dialog
  approveDialog: {
    dialog: 'dialog[data-testid="dialog-approve-fas"]',
    title: 'h3[id="fas-approve-dialog-title"]',
    tierRadioGroup: 'div[data-testid="group-select-tier"]',
    tier1Radio: 'input[data-testid="radio-tier-1"]',
    tier2Radio: 'input[data-testid="radio-tier-2"]',
    subsidizedFeesTable: 'table[data-testid="table-subsidized-fees-breakdown"]',
    totalSubsidyAmount: 'span[data-testid="total-subsidized-amount"]',
    effectiveFromDate: 'span[data-testid="effective-from-date"]',
    confirmApproveBtn: 'button[data-testid="btn-confirm-approve-fas"]',
    cancelBtn: 'button[data-testid="btn-cancel-approve-fas"]',
  },
  // Screen G: Reject FAS Dialog
  rejectDialog: {
    dialog: 'dialog[data-testid="dialog-reject-fas"]',
    title: 'h3[id="fas-reject-dialog-title"]',
    warningBanner: 'div[data-testid="reject-warning-banner"]',
    remarksTextarea: 'textarea[data-testid="textarea-rejection-remarks"]',
    charCounter: 'span[data-testid="reject-remarks-char-counter"]',
    remarksErrorMsg: 'p[data-testid="error-rejection-remarks"][role="alert"]',
    confirmRejectBtn: 'button[data-testid="btn-confirm-reject-fas"]',
    cancelBtn: 'button[data-testid="btn-cancel-reject-fas"]',
  },
  processingSpinner: 'span[data-testid="decision-processing-spinner"]',
};
```

---

## 2. BR / AC Traceability
- **Business Rules (BR)**:
  - `FS Section 8 & 9`: Approval must confirm the Tier granted (`Tier 1` vs `Tier 2`).
  - `FS 6.4 & T31`: Approval computes and displays the breakdown of subsidized school fees (School Fee, Standard Misc Fee, Second-Tier Misc Fee).
  - `Screen G Mandatory Remarks`: When rejecting an application, **Rejection Remarks are strictly mandatory** (minimum 15 characters, maximum 500 characters) to provide transparent feedback to parents (`VR-REJ-01`).
  - `T30`: Double-click prevention: Confirm button is disabled immediately upon first click. If a save error occurs, displays: *"Something went wrong. Please try again."*
- **Acceptance Criteria (AC)**:
  - `Screen E AC01`: Selecting Tier 1 updates subsidized fee calculation to 100% waiver.
  - `Screen G AC01`: Submitting empty rejection remarks triggers inline validation error.
  - `Screen G AC02`: Submitting remarks with $<15$ characters keeps Confirm button disabled or triggers error: *"Please enter rejection remarks (at least 15 characters) to inform the parent."*
  - `Screen G AC03`: Valid rejection updates application status to `REJECTED`, refreshes summary cards.

---

## 3. Ma Trận 12 Lớp Validation (Universal Modal & Decision Matrix)

| Lớp | Loại Kiểm Thử | Dữ Liệu Input / Thao Tác | Kỳ Vọng Hệ Thống (Expected Behavior) | Mã Lỗi / UI Indicator |
| :--- | :--- | :--- | :--- | :--- |
| **L01** | Empty Required Remarks (Reject) | Để trống ô Remarks và bấm `Confirm Rejection` | Báo lỗi bắt buộc; ô textarea viền đỏ `aria-invalid="true"`. | Inline validation error |
| **L02** | BVA Min Length Remarks ($<15$ chars) | Nhập 14 ký tự `"Gia cảnh chưa rõ"` | Báo lỗi độ dài: yêu cầu tối thiểu 15 ký tự; nút Confirm bị chặn. | Minlength 15 chars |
| **L03** | BVA Min Length Remarks ($15$ chars) | Nhập đúng 15 ký tự `"Gia đình khá giả"` | Hợp lệ; `aria-invalid` biến mất; nút Confirm mở khóa. | Valid minimum |
| **L04** | All Whitespace Remarks (ASM-15) | Nhập 20 dấu cách `"                    "` | Tự động trim về rỗng; báo lỗi bắt buộc; không qua được validation. | Trimmed clean |
| **L05** | BVA Max Length Remarks ($500, 501$) | Nhập 500 ký tự vs 501 ký tự | 500 ký tự hợp lệ (counter `500/500`); ký tự 501 bị chặn bởi `maxlength="500"`. | Maxlength 500 chars |
| **L06** | Tier Radio Selection (Approve) | Chuyển đổi giữa `Tier 1 (100%)` và `Tier 2 (75%)` | Bảng tính toán phí cập nhật số tiền được miễn giảm tương ứng ngay lập tức. | Reactive calculation |
| **L07** | Rapid Double Click Debounce | Bấm nút Xác nhận 2 lần thật nhanh | Nút disable ngay lần bấm đầu tiên; chỉ gửi 1 request duyệt/từ chối lên server. | Single network request |
| **L08** | Escape Key Dismissal | Nhấn phím `Escape` khi dialog đang mở | Dialog đóng; không lưu trạng thái; không thay đổi dữ liệu đơn. | ESC key dismissal |
| **L09** | Focus Trapping Accessibility | Nhấn `Tab` liên tục trong modal | Focus chỉ luân chuyển qua lại giữa Radio, Textarea, Cancel, Confirm; không lọt ra ngoài. | Focus trapped |
| **L10** | Security / XSS in Remarks | Nhập `<script>alert('rejected')</script>` | Textarea lưu trữ an toàn; khi phụ huynh xem thông báo trên Portal hiển thị text đã escape. | Sanitized feedback |
| **L11** | i18n & Error Feedback Integrity | Báo lỗi thiếu lý do từ chối | Hiển thị câu từ hoàn chỉnh; không hiển thị `fas.reject.remarksMinLength`. | Exact English copy |
| **L12** | Database Save Failure (`T30`) | Backend trả về mã lỗi 500 khi lưu quyết định | Dialog giữ nguyên trạng thái; hiển thị alert: *"Something went wrong. Please try again."* | T30 error handled |

---

## 4. Error Handling & Visual Feedback
- **Reject Remarks Error Marker**:
  - `p[data-testid="error-rejection-remarks"][role="alert"]`:
  - Text: *"Please enter rejection remarks (at least 15 characters) to inform the parent."*
  - Viền đỏ `#DC2626` quanh Textarea.
- **Character Counter**:
  - `span[data-testid="reject-remarks-char-counter"]`:
  - Hiển thị tiến trình `X/500`. Đổi màu đỏ khi vi phạm min hoặc chạm max.
- **Processing State**:
  - Khi đang gửi quyết định:
  - Nút chuyển sang `Processing decision...` kèm spinner xoay vòng; nút Cancel bị disable.

---

## 5. JSON Fixtures Data Payload

```json
{
  "fas_decision_fixtures": {
    "approve_tier1_payload": {
      "application_id": "APP-2026-00412",
      "decision": "APPROVED",
      "tier_granted": "Tier 1",
      "subsidies": [
        { "fee_code": "SCH_FEE_STD", "waiver_percent": 100, "waived_amount": 13.00 },
        { "fee_code": "MISC_FEE_STD", "waiver_percent": 100, "waived_amount": 10.00 }
      ],
      "total_monthly_subsidy": 23.00
    },
    "reject_payload": {
      "application_id": "APP-2026-00412",
      "decision": "REJECTED",
      "remarks": "Gross household income and per capita income exceed SBFAS eligibility thresholds."
    },
    "invalid_reject_remarks": [
      { "text": "", "expected_error": "Please enter rejection remarks (at least 15 characters) to inform the parent." },
      { "text": "Too high income", "expected_error": "Please enter rejection remarks (at least 15 characters) to inform the parent." }
    ]
  }
}
```
