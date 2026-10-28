# Component Specification: Payment Gateway Simulator Sandbox (Billing & Payment)

## 1. Metadata & Selector

| Attribute | Specification |
| :--- | :--- |
| **Component Name** | `PaymentGatewaySimulatorComponent` |
| **Target Page / Route** | `http://localhost:5286/checkout/{checkoutToken}` (`PaymentGatewaySimulatorPage`) |
| **Element Hierarchy** | Hosted checkout header `<header>`, Summary card `<div>`, Details list `<dl>`, Outcome action cards `<form>`, Action buttons `<button>` |
| **Visual State** | Màn hình cổng thanh toán bên thứ ba (Sandbox Mock Gateway) |
| **Component Scope** | Mô phỏng trải nghiệm thanh toán thẻ tín dụng / PayNow trực tuyến; cung cấp 2 nút kích hoạt kịch bản Thành Công và Thất Bại |

### Playwright Live DOM Locators
```python
# Extracted from pages/fs09/payment_gateway_simulator_page.py
TITLE = "h1#checkout-title"
AMOUNT_DUE = "div.summary-amount strong, .summary-amount strong"
STATUS_BADGE = "div.summary-status [class*='badge'], .summary-status span"
REFERENCE_CODE = ".checkout-details-list code, dt:has-text('Reference') + dd code"
MERCHANT_VALUE = "dt:has-text('Merchant') + dd"
CURRENCY_VALUE = "dt:has-text('Currency') + dd"
METHOD_VALUE = "dt:has-text('Payment method') + dd"
EXPIRES_VALUE = "dt:has-text('Expires') + dd"

PAY_SUCCESSFUL_BTN = "button[type='submit']:has-text('Pay successful')"
PAY_FAILED_BTN = "button[type='submit']:has-text('Pay failed')"
ALERT = "div[role='alert'], .checkout-content div[role='alert']"
EXPIRED_ALERT = "div[role='alert']:has-text('expired')"
COMPLETED_ALERT = "div[role='alert']:has-text('already completed')"
```

---

## 2. Business Rules & Acceptance Criteria Traceability

| ID | Type | Description | Source Reference |
| :--- | :--- | :--- | :--- |
| **BR-F9-09** | Business Rule | Merchant and Checkout session reference binding: Checkout session is cryptographically bound to the invoice transaction ID and requested amount. | `specs/md/FS document/FS-09_Outstanding_Fees_and_Payment.md` |
| **AC-07** | Acceptance Criteria | Successful Online Payment: Clicking "Pay successful" triggers webhook callback and redirects parent to receipt page with status "Paid". | `specs/md/Test Cases/TC_R9_Outstanding_Fees_and_Payment.md` |
| **AC-08** | Acceptance Criteria | Failed Online Payment: Clicking "Pay failed" triggers failure callback and redirects parent to result page with status "Failed". | `specs/md/Test Cases/TC_R9_Outstanding_Fees_and_Payment.md` |
| **AC-18** | Acceptance Criteria | Checkout Expiry: Sessions older than 15 minutes expire automatically; attempting payment returns expired notice and cannot settle. | `specs/md/Test Cases/TC_R9_Outstanding_Fees_and_Payment.md` |
| **AC-20** | Acceptance Criteria | Idempotent Replay Prevention: Submitting payment on an already completed/failed checkout returns `already completed` notice. | `specs/md/Test Cases/TC_R9_Outstanding_Fees_and_Payment.md` |

---

## 3. Ma trận 12 lớp Validation & UI Integrity

| Lớp (Layer) | Phân Loại Kiểm Thử | Dữ Liệu Đầu Vào (Input Vector) | Trạng Thái / Hành Vi UI Kỳ Vọng | Tiêu Chí Đạt (Pass Criteria) |
| :--- | :--- | :--- | :--- | :--- |
| **1. Session Data Binding** | Khớp dữ liệu giao dịch | Chuyển từ Step 3 sang Simulator | Amount Due hiển thị đúng số tiền trực tuyến (ví dụ `$1,450.00`), Reference code hiển thị mã giao dịch hợp lệ. | Số tiền và mã Reference khớp 100%. |
| **2. Merchant & Currency Display** | Nhãn đơn vị và tiền tệ | Merchant info | Merchant: *"Ministry of Education (Singapore)"*, Currency: *"SGD"*. | Thông tin hiển thị rõ ràng. |
| **3. Expiry Countdown Display** | Hạn hiệu lực phiên | Token có TTL 15 phút | Hiển thị thời điểm hết hạn dạng `DD/MM/YYYY HH:mm:ss SGT`. | Trường Expires có định dạng hợp lệ. |
| **4. Trigger Pay Successful** | Kích hoạt thanh toán thành công | Click `button:has-text('Pay successful')` | Gửi POST webhook thành công, redirect trình duyệt về `http://localhost:5174/payment-result?session={token}`. | Chuyển trang về kết quả Paid. |
| **5. Trigger Pay Failed** | Kích hoạt thanh toán thất bại | Click `button:has-text('Pay failed')` | Gửi POST webhook thất bại, redirect trình duyệt về `http://localhost:5174/payment-result` với trạng thái Failed. | Chuyển trang về kết quả Failed. |
| **6. Already Completed Replay** | Chống thực thi lại phiên | F5 lại trang Simulator sau khi đã click Pay | Hiển thị thông báo: *"This checkout session has already completed."*. Các nút bấm bị vô hiệu hóa. | Không thể thanh toán lại lần 2. |
| **7. Expired Session Guard** | Phiên hết hạn | Mở checkout token đã quá 15 phút | Hiển thị thông báo: *"This checkout session has expired."*. Chặn thực hiện thanh toán. | Nút Pay bị ẩn/disabled. |
| **8. Webhook Signature Verification** | Bảo mật truyền thông | Webhook call tới backend MOE | Kèm chữ ký `X-Webhook-Signature` (HMAC SHA-256) sử dụng secret `whsec_f9_demo_shared_secret`. | Backend xác thực chữ ký thành công. |
| **9. Browser Back Button Guard** | Nút Back trên trình duyệt | Bấm Back từ trang kết quả quay lại Simulator | Hiển thị trạng thái completed hoặc redirect trở lại kết quả; không cho phép submit lại. | Giao diện an toàn. |
| **10. Accessibility & Security Badge** | WCAG 2.1 AA | Kiểm tra header simulator | Hiển thị nhãn *"Secure checkout"* với biểu tượng khóa bảo mật, nút submit có độ tương phản cao. | Nhãn bảo mật trực quan. |
| **11. Network Latency Simulation** | Độ trễ mạng khi xử lý | Giả lập mạng chậm 1500ms khi bấm Pay | Nút Pay hiển thị trạng thái loading, chặn tương tác bổ sung trong thời gian chờ redirect. | Con trỏ wait, không click đúp. |
| **12. Error Outcome Context** | Gửi kèm lý do từ chối | Bấm Pay failed | Gửi mã lỗi từ chối tiêu chuẩn (ví dụ: `CARD_DECLINED`, `INSUFFICIENT_FUNDS`) để backend lưu audit log. | Lý do thất bại được ghi nhận. |

---

## 4. Error Handling & Visual Feedback

| Tình Huống Kích Hoạt | Mã Lỗi Chuẩn | Nội Dung Thông Báo Bắt Buộc | Trạng Thái DOM & Style |
| :--- | :--- | :--- | :--- |
| Phiên checkout đã được xử lý trước đó | `ALREADY_COMPLETED` | *"This checkout session has already completed."* hoặc *"already failed"* | Banner alert xám/vàng `div[role='alert']`, nút bấm bị ẩn hoặc disabled. |
| Phiên checkout đã hết hạn 15 phút | `SESSION_EXPIRED` | *"This checkout session has expired. Please return to billing to start a new payment."* | Banner alert đỏ `div[role='alert']`, nút điều hướng về trang chủ. |

---

## 5. JSON Fixtures Data Payload

```json
{
  "gateway_simulator_fixtures": {
    "valid_session_payload": {
      "merchant_name": "Ministry of Education (Singapore)",
      "currency": "SGD",
      "payment_method": "Credit / Debit Card or PayNow",
      "simulated_success_action": "Pay successful",
      "simulated_failure_action": "Pay failed"
    },
    "webhook_signature_config": {
      "shared_secret": "whsec_f9_demo_shared_secret",
      "signature_header": "X-Webhook-Signature",
      "algorithm": "HMAC-SHA256"
    }
  }
}
```
