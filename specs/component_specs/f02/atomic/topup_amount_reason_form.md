# Component Spec: Top-Up Amount & Reason Form (`topup_amount_reason_form`)

## 1. Metadata & Selector
- **Component ID**: `F02-COMP-AMOUNT-REASON`
- **Component Name**: Verify Owner & Enter Amount (`SCR-02`)
- **Module**: `f02` (Top-Up Management)
- **Target Route**: `/admin/top-up/individual/verify` (SCR-02)
- **Target Role**: `MOE HQ User`
- **Element Tag**: `<section role="region" aria-label="Verify Account and Enter Amount">`

### Playwright Locators (BSK Live DOM Standard)
```typescript
export const topupAmountReasonLocators = {
  container: 'section[aria-label="Verify Account and Enter Amount"]',
  readOnlyInfo: {
    studentName: 'div[data-testid="verify-student-name"]',
    nricMasked: 'div[data-testid="verify-student-nric"]',
    age: 'div[data-testid="verify-student-age"]',
    accountNumber: 'div[data-testid="verify-account-number"]',
    accountStatus: 'div[data-testid="verify-account-status"]',
    accountStatusBadge: 'span[data-testid="verify-status-badge"]',
    currentBalance: 'div[data-testid="verify-current-balance"]',
  },
  form: {
    amountInput: 'input[data-testid="topup-amount-input"]',
    amountCurrencyPrefix: 'span[data-testid="topup-currency-prefix"]',
    amountError: 'p[data-testid="topup-amount-error"][role="alert"]',
    reasonInput: 'textarea[data-testid="topup-reason-input"]',
    reasonCharCounter: 'span[data-testid="topup-reason-char-count"]',
    reasonError: 'p[data-testid="topup-reason-error"][role="alert"]',
    inactiveAccountBanner: 'div[data-testid="topup-account-inactive-banner"]',
    continueBtn: 'button[data-testid="topup-btn-continue"]',
    backBtn: 'button[data-testid="topup-btn-back"]',
  },
};
```

---

## 2. BR / AC Traceability
- **Business Rules (BR)**:
  - `BR-F2-03`: The top-up amount must be strictly greater than 0, formatted to at most two decimal places, and within the per-credit limit. The reason is mandatory and cannot exceed 200 characters.
  - `BR-F2-04`: Only `Active` Education Accounts can accept a top-up. Before crediting, system triggers the F02 Closure Eligibility Check. If Closed, Closure Deferred, or Eligibility Review Required, input is disabled and transaction is blocked with `MSG-0204`.
  - PII Protection: Student NRIC displayed must be partially masked (`T****345A`). The full NRIC is **NEVER** exposed in browser URL parameters.
- **Acceptance Criteria (AC)**:
  - `SCR-02 AC01`: If account is `Active`, amount and reason fields are enabled.
  - `SCR-02 AC02`: If account is `Closed`, amount and reason inputs are disabled; `MSG-0204` is displayed.
  - `SCR-02 AC03`: Submitting amount `<= 0` or more than 2 decimal places triggers `MSG-0202`.
  - `SCR-02 AC04`: Submitting amount exceeding limit triggers `MSG-0203`.
  - `SCR-02 AC05`: Submitting empty reason or $> 200$ chars triggers `MSG-0206`.
  - `SCR-02 AC06`: Valid amount and reason enables `Continue` button navigating to `SCR-03`.
- **System Messages**:
  - `MSG-0202`: *"Enter an amount greater than 0, with up to 2 decimal places."*
  - `MSG-0203`: *"The amount is more than the limit for one top-up."*
  - `MSG-0204`: *"This Education Account is not active. Top-up is not allowed."*
  - `MSG-0206`: *"Enter a reason (up to 200 characters)."*

---

## 3. Ma Trận 12 Lớp Validation (Universal Field-Level Matrix)

| Lớp | Loại Kiểm Thử | Dữ Liệu Input / Thao Tác | Kỳ Vọng Hệ Thống (Expected Behavior) | Mã Lỗi / UI Indicator |
| :--- | :--- | :--- | :--- | :--- |
| **L01** | Empty Required Amount | Để trống ô Amount và bấm `Continue` | Báo lỗi bắt buộc; ô nhập viền đỏ `aria-invalid="true"`. | `MSG-0202` |
| **L02** | Empty Required Reason | Để trống ô Reason và bấm `Continue` | Báo lỗi lý do bắt buộc; ô textarea viền đỏ. | `MSG-0206` |
| **L03** | All Whitespace Reason | Nhập toàn dấu cách `"        "` vào Reason | Tự động trim về rỗng; báo `MSG-0206`. | `MSG-0206` |
| **L04** | Leading / Trailing Whitespaces | Nhập `"   250.00   "` và lý do `"  Monthly support  "` | Tự động trim sạch khoảng trắng thừa; lưu giá trị chuẩn `250.00` và `"Monthly support"`. | Auto-trimmed clean |
| **L05** | BVA Min Amount ($Min-1, Min, Min+1$) | Thử các giá trị: `0.00`, `-1.00`, `0.01` | `0.00` và `-1.00` bị từ chối với `MSG-0202`; `0.01` hợp lệ và được chấp nhận. | `MSG-0202` on zero/negative |
| **L06** | Decimal Precision Limits | Thử nhập `10.5` vs `10.55` vs `10.555` | `10.5` tự động chuẩn hóa thành `10.50`; `10.55` hợp lệ; `10.555` (3 số thập phân) bị từ chối với `MSG-0202`. | `MSG-0202` on 3+ decimals |
| **L07** | BVA Max Amount Limit ($Limit, Limit+1$) | Thử hạn mức ví dụ `$10,000.00` vs `$10,000.01` | `$10,000.00` hợp lệ; `$10,000.01` bị từ chối và hiển thị `MSG-0203`. | `MSG-0203` |
| **L08** | BVA Max Length Reason ($199, 200, 201$) | Nhập lý do 200 ký tự vs 201 ký tự | 200 ký tự hợp lệ (counter `200/200`); ký tự thứ 201 bị chặn bởi `maxlength="200"` hoặc báo lỗi `MSG-0206`. | Maxlength 200 chars |
| **L09** | Inactive / Closed Account UI State | Truy cập SCR-02 với tài khoản có `status = CLOSED` | Ô Amount và Reason bị `disabled="true"`; Nút `Continue` bị disabled; banner hiện `MSG-0204`. | `MSG-0204` / inputs disabled |
| **L10** | Security / XSS in Reason Field | Bơm `<script>alert(1)</script>` vào ô Reason | Không thực thi script; sanitize HTML an toàn; text lưu trữ dạng Unicode thuần. | Sanitized safe string |
| **L11** | i18n & Error Feedback Integrity | Báo các mã lỗi `MSG-0202`, `MSG-0203`, `MSG-0204`, `MSG-0206` | Câu từ chính xác 100% theo bản đặc tả F2; **CẤM TUYỆT ĐỐI** lộ translation key thô. | Exact spec copy |
| **L12** | Form Dirty & Navigation Guard | Đã nhập Amount `100.00` rồi bấm nút `Quay lại` (Back) | Hiển thị confirm prompt hoặc quay lại SCR-01 mà không làm crash flow. | Clean navigation |

---

## 4. Error Handling & Visual Feedback
- **Disabled State on Inactive Account**:
  - Khi `account_status !== 'ACTIVE'`:
  - Input Amount có thuộc tính `disabled="true"` và class `bg-gray-100 cursor-not-allowed`.
  - Banner cảnh báo `MSG-0204` xuất hiện với background vàng nhạt (Amber-50/Amber-800).
- **Inline Error Feedback**:
  - `p[data-testid="topup-amount-error"][role="alert"]` hiển thị ngay bên dưới ô nhập Amount.
  - Viền đỏ rực `#DC2626` quanh ô nhập.
- **Character Counter**:
  - Bộ đếm ký tự `span[data-testid="topup-reason-char-count"]` cập nhật thời gian thực (`X/200`). Chuyển màu đỏ khi chạm mốc 200.

---

## 5. JSON Fixtures Data Payload

```json
{
  "amount_reason_fixtures": {
    "active_account_valid_input": {
      "account_number": "EA-2026-00001",
      "account_status": "ACTIVE",
      "current_balance": 0.00,
      "input_amount": "250.00",
      "input_reason": "Top-up for school textbooks support",
      "expected_valid": true,
      "expected_next_screen": "/admin/top-up/individual/confirm"
    },
    "boundary_amounts": [
      { "amount": "0.01", "valid": true, "note": "Min valid penny" },
      { "amount": "0.00", "valid": false, "expected_message": "MSG-0202" },
      { "amount": "-50.00", "valid": false, "expected_message": "MSG-0202" },
      { "amount": "100.999", "valid": false, "expected_message": "MSG-0202" },
      { "amount": "10000.01", "valid": false, "expected_message": "MSG-0203" }
    ],
    "boundary_reasons": [
      { "length": 1, "text": "A", "valid": true },
      { "length": 200, "text": "Lorem ipsum dolor sit amet...", "valid": true },
      { "length": 201, "valid": false, "expected_message": "MSG-0206" }
    ],
    "inactive_account_blocked": {
      "account_number": "EA-2018-09920",
      "account_status": "CLOSED",
      "current_balance": 0.00,
      "expected_message_code": "MSG-0204",
      "expected_message_text": "This Education Account is not active. Top-up is not allowed.",
      "expected_inputs_disabled": true
    }
  }
}
```
