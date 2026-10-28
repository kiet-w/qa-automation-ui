# Component Spec: Top-Up Review & Confirm Dialog (`topup_confirm_dialog`)

## 1. Metadata & Selector
- **Component ID**: `F02-COMP-CONFIRM-DIALOG`
- **Component Name**: Review & Confirm Individual Top-Up (`SCR-03`)
- **Module**: `f02` (Top-Up Management)
- **Target Route**: `/admin/top-up/individual/confirm` (SCR-03)
- **Target Role**: `MOE HQ User`
- **Element Tag**: `<dialog role="alertdialog" aria-modal="true" aria-labelledby="confirm-topup-title">`

### Playwright Locators (BSK Live DOM Standard)
```typescript
export const topupConfirmLocators = {
  dialog: 'dialog[aria-labelledby="confirm-topup-title"]',
  overlay: 'div[data-testid="confirm-dialog-overlay"]',
  title: 'h3[id="confirm-topup-title"]',
  reviewSummary: {
    studentName: 'span[data-testid="summary-student-name"]',
    nricMasked: 'span[data-testid="summary-student-nric"]',
    accountNumber: 'span[data-testid="summary-account-number"]',
    currentBalance: 'span[data-testid="summary-current-balance"]',
    topupAmount: 'span[data-testid="summary-topup-amount"]',
    balanceAfterTopup: 'span[data-testid="summary-balance-after"]',
    reason: 'p[data-testid="summary-reason-text"]',
  },
  idempotencyTokenInput: 'input[data-testid="topup-idempotency-key"]', // Hidden input
  actions: {
    confirmBtn: 'button[data-testid="topup-btn-confirm-submit"]',
    cancelBtn: 'button[data-testid="topup-btn-cancel"]',
    processingIndicator: 'span[data-testid="topup-processing-spinner"]',
  },
  lateClosureAlert: 'div[data-testid="late-closure-alert"][role="alert"]',
};
```

---

## 2. BR / AC Traceability
- **Business Rules (BR)**:
  - `BR-F2-05`: Each credit happens **exactly once**:
    - An idempotency key unique per HQ user action.
    - Confirm button is strictly **disabled** immediately after the first click.
    - Generates a distinct `FundingReference` per credit.
  - `EX-02`: Late Closure Check: If the EA closes or student turns 16 between viewing and confirming, the closure eligibility check runs at confirm, rejects the top-up with `MSG-0204`, and leaves the balance unchanged.
  - `EX-04`: Double confirm click or resubmitted idempotency key produces exactly one transaction and one credit; resend returns original transaction outcome.
- **Acceptance Criteria (AC)**:
  - `SCR-03 AC01`: Displays correct calculation: $\text{Balance After} = \text{Current Balance} + \text{Top-Up Amount}$.
  - `SCR-03 AC02`: Clicking `Confirm` disables the button immediately and transitions UI to `Processing`.
  - `SCR-03 AC03`: Rapid double-clicking confirm button only issues a single network payload.
  - `SCR-03 AC04`: If account closed in background before confirm, transaction aborts with `MSG-0204`.
  - `SCR-03 AC05`: Clicking `Cancel` returns to SCR-02 with amount and reason preserved.
- **System Messages**:
  - `MSG-0204`: *"This Education Account is not active. Top-up is not allowed."*
  - `MSG-0002`: *"Your session has expired. Please log in again."*

---

## 3. Ma Trận 12 Lớp Validation (Confirmation Dialog & Idempotency Matrix)

| Lớp | Loại Kiểm Thử | Dữ Liệu Input / Thao Tác | Kỳ Vọng Hệ Thống (Expected Behavior) | Mã Lỗi / UI Indicator |
| :--- | :--- | :--- | :--- | :--- |
| **L01** | Accurate Math Summary | Balance `$0.00` + Top-Up `$250.00` | Cột `Balance After Top-Up` hiển thị đúng `$250.00 SGD` (read-only tham khảo). | Accurate sum display |
| **L02** | Cancel Action Navigation | Bấm nút `Hủy` (Cancel) | Dialog đóng, quay về `SCR-02`, giữ nguyên giá trị đã nhập ở Amount và Reason. | Form state retained |
| **L03** | Rapid Double-Click Debounce | Bấm nút `Xác nhận` (Confirm) 2 lần liên tiếp thật nhanh (<100ms) | Nút bị vô hiệu hóa ngay ở lần click 1 (`disabled="true"`); chỉ 1 request POST gửi đi. | Single network request |
| **L04** | Idempotency Key Generation | Kiểm tra payload của request Confirm | Mang header `X-Idempotency-Key` dạng UUIDv4 duy nhất theo phiên người dùng. | Unique idempotency header |
| **L05** | Late Account Closure Race (`EX-02`) | Student tròn 16 tuổi trong lúc đang ở màn hình SCR-03 | API backend từ chối credit; hiển thị `MSG-0204`; số dư giữ nguyên; đóng dialog. | `MSG-0204` late reject |
| **L06** | Session Expiry Race (`EX-06`) | Admin session hết hạn trước khi bấm Confirm | Bấm confirm bị từ chối; redirect sang màn hình đăng nhập với `MSG-0002`. | `MSG-0002` session expiry |
| **L07** | Network Timeout during Credit (`EX-05`) | Mất kết nối khi đang xử lý credit | Giao diện hiển thị trạng thái `Verifying` (đang xác minh); chuyển sang `SCR-04` với `MSG-0209`. | `MSG-0209` verifying |
| **L08** | Keyboard Accessibility | Phím `Tab`, `Shift+Tab`, `Escape` | Phím `Escape` đóng dialog (hủy); phím `Tab` chỉ luân chuyển giữa nút `Cancel` và `Confirm`. | Focus trap standard |
| **L09** | PII Masking Verification | Cột NRIC trong bảng tóm tắt | Che theo quy chuẩn `T****345A`; không in NRIC trần ra DOM. | PII Masked |
| **L10** | HTML Entities Escaped in Reason | Xem text hiển thị tại mục Reason | Text có ký tự `<script>` hiển thị text thuần đã escape, không sinh modal XSS. | Sanitized text |
| **L11** | i18n & Modal Copy Integrity | Tiêu đề modal, nút bấm, nhãn trường | Đảm bảo không chứa `modal.topup.confirm.*`. | Clean localized copy |
| **L12** | FundingReference Uniqueness | Kiểm tra transaction audit sinh ra | Tạo một `FundingReference` duy nhất gắn liền với lượt credit này. | Unique funding ref |

---

## 4. Error Handling & Visual Feedback
- **Processing Spinner**:
  - Khi click `Confirm`:
  - Nút chuyển text sang: `Processing top-up...` kèm spinner icon quay đều; nút Cancel bị disable.
- **Race Condition Alert**:
  - Khi dính lỗi `EX-02` (tài khoản vừa đóng):
  - Modal hiển thị thông báo đỏ: *"Tài khoản này vừa được đóng do học sinh đã tròn 16 tuổi. Giao dịch nạp tiền đã bị hủy."*

---

## 5. JSON Fixtures Data Payload

```json
{
  "topup_confirm_fixtures": {
    "standard_confirm_payload": {
      "account_number": "EA-2026-00001",
      "amount": 250.00,
      "reason": "Top-up for school textbooks support",
      "idempotency_key": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
      "expected_outcome": "SUCCESS",
      "mock_response": {
        "transaction_reference": "TUP-20261026-00129",
        "status": "SUCCESS",
        "new_balance": 250.00,
        "credited_at": "2026-10-26T14:00:00+08:00"
      }
    },
    "late_closure_rejection": {
      "account_number": "EA-2018-09920",
      "amount": 100.00,
      "reason": "Test late closure",
      "idempotency_key": "8a0cea3c-2a6c-3abc-8acc-1a0c6a2cba5c",
      "expected_outcome": "REJECTED_INACTIVE",
      "expected_message_code": "MSG-0204",
      "expected_message_text": "This Education Account is not active. Top-up is not allowed."
    }
  }
}
```
