# Component Specification: Payment Review and Authorization (Billing & Payment)

## 1. Metadata & Selector

| Attribute | Specification |
| :--- | :--- |
| **Component Name** | `PaymentReviewAndConfirmComponent` |
| **Target Page / Route** | `/billing/{studentId}` (`BillingPaymentPage`, SCR-05) |
| **Element Hierarchy** | Review container `<section>`, Review charges table `<table>`, Funding summary list `<dl>`, Action buttons `<div>` |
| **Visual State** | Step 3 (Màn hình cuối cùng trước khi ghi nợ hoặc chuyển sang cổng thanh toán) |
| **Component Scope** | Hiển thị tóm tắt cuối cùng về các khoản phí, nguồn trích tiền, số dư sau giao dịch và gửi yêu cầu Authorize kèm Idempotency Key |

### Playwright Live DOM Locators
```python
# Extracted from pages/fs09/billing_payment_page.py
REVIEW_HEADING = "h2#billing-review-heading"
REVIEW_TABLE = "table[class*='reviewTable'], [class*='reviewTable'] table, table"
REVIEW_CHARGES_ROWS = "table[class*='reviewTable'] tbody tr"
STEP3_BACK_BTN = "[class*='reviewActions'] button:has-text('Back')"
CONFIRM_PAY_BTN = "button:has-text('Authorize & pay'), button:has-text('Authorize and pay'), button:has-text('Pay')"
PROCESSING_SPINNER = "button[disabled]:has-text('Processing'), [role='status']:has-text('Authorizing')"
ALERT = "div[role='alert']"
```

---

## 2. Business Rules & Acceptance Criteria Traceability

| ID | Type | Description | Source Reference |
| :--- | :--- | :--- | :--- |
| **BR-F9-04** | Business Rule | Invoice state changes to `PaymentPending` upon authorization click. No concurrent payment can be initiated for this invoice. | `specs/md/FS document/FS-09_Outstanding_Fees_and_Payment.md` |
| **BR-F9-09** | Business Rule | Idempotency Protection: Client generates a unique Idempotency Key for every payment authorization to prevent duplicate charges upon rapid clicks or network retries. | `specs/md/FS document/FS-09_Outstanding_Fees_and_Payment.md` |
| **BR-F9-13** | Business Rule | Balance snapshot: Display remaining balance in Education Account after deduction: $\text{Projected Balance} = \text{Current Balance} - \text{EA Deduction Leg}$. | `specs/md/FS document/FS-09_Outstanding_Fees_and_Payment.md` |
| **AC-05** | Acceptance Criteria | Review and Authorize: Parent reviews invoice details, payment breakdown, and clicks "Authorize & pay". Form enters processing state. | `specs/md/Test Cases/TC_R9_Outstanding_Fees_and_Payment.md` |
| **AC-17** | Acceptance Criteria | Double-submit prevention: Authorize button is immediately disabled after first click to prevent duplicate transaction requests. | `specs/md/Test Cases/TC_R9_Outstanding_Fees_and_Payment.md` |

---

## 3. Ma trận 12 lớp Validation & UI Integrity

| Lớp (Layer) | Phân Loại Kiểm Thử | Dữ Liệu Đầu Vào (Input Vector) | Trạng Thái / Hành Vi UI Kỳ Vọng | Tiêu Chí Đạt (Pass Criteria) |
| :--- | :--- | :--- | :--- | :--- |
| **1. Snapshot Fidelity** | Tính toàn vẹn dữ liệu | Chuyển từ Step 2 sang Step 3 | Bảng Review hiển thị chính xác 100% các dòng đã chọn ở Step 1 và phương thức đã chọn ở Step 2. | Không mất mát hoặc sai lệch số tiền. |
| **2. Funding Breakdown Display** | Hiển thị nguồn tiền | Full EA vs Full Online vs Split | Hiển thị rõ ràng số tiền trích từ từng nguồn (vd: EA: `$50.00`, Online: `$1,450.00`). | Khớp chính xác với cấu hình Step 2. |
| **3. Projected Balance Math** | Tính số dư sau giao dịch | EA Balance = `$650.00`, Pay = `$44.50` | Hiển thị: Current `$650.00`, Deduction `$44.50`, Projected Balance: `$605.50`. | Phép trừ số học chính xác. |
| **4. Back Navigation to Step 2** | Quay lại bước trước | Click nút "Back" ở Step 3 | Quay lại Step 2; phương thức thanh toán đã chọn trước đó vẫn được giữ nguyên. | Form không bị reset. |
| **5. Single-Click Immediate Lockout**| Khóa nút chống click đúp | Click 1 lần vào "Authorize & pay" | Nút lập tức chuyển sang disabled, hiển thị spinner hoặc nhãn *"Processing..."*. Con trỏ đổi sang `wait`/`not-allowed`. | Thuộc tính `disabled="true"` xuất hiện trong 50ms. |
| **6. Idempotency Key Injection** | Bảo vệ lặp giao dịch | Bấm Authorize | Client sinh UUID v4 gắn vào request payload `idempotency_key`. | Request header/body có key duy nhất. |
| **7. Fast Double-Click Resilience** | Bắn liên tiếp 2 click nhanh | Click đúp với delta < 50ms | Chỉ có duy nhất 1 request `POST /api/billing/authorize` được gửi qua mạng. | 1 network request duy nhất. |
| **8. Session Timeout Handling** | Hết hạn phiên Singpass | Đứng chờ ở Step 3 quá 15 phút rồi click Authorize | Máy chủ trả về `AUTH_REQUIRED`; UI hiển thị modal/alert yêu cầu đăng nhập lại, không trừ tiền. | An toàn, không treo hệ thống. |
| **9. Concurrent Payment Race** | Phụ huynh khác vừa trả xong | Bấm Authorize khi invoice đã Paid | Máy chủ trả về `INVOICE_ALREADY_PAID`. Hệ thống báo lỗi thân thiện và làm mới lại danh sách phí. | Báo lỗi rõ ràng, không double debit. |
| **10. Full EA Transition** | Luồng Full EA | Bấm Authorize cho hóa đơn Full EA | Gọi trực tiếp API ghi nợ EA; khi hoàn tất chuyển thẳng sang trang Kết quả `/payment-result`. | Không chuyển hướng ra ngoài. |
| **11. Online Gateway Redirect** | Luồng Trực tuyến / Split | Bấm Authorize có kèm Online Leg | Hệ thống nhận payment URL từ API và thực hiện redirect trình duyệt sang trang checkout cổng thanh toán. | Chuyển hướng sang `/checkout/...`. |
| **12. Zero Layout Shift** | Sức khỏe UI | Trạng thái chuyển đổi nút submit | Kích thước nút không bị co giãn đột ngột khi chèn biểu tượng spinner. | CLS = 0. |

---

## 4. Error Handling & Visual Feedback

| Tình Huống Kích Hoạt | Mã Lỗi Chuẩn | Nội Dung Thông Báo Bắt Buộc | Trạng Thái DOM & Style |
| :--- | :--- | :--- | :--- |
| Hóa đơn đã được thanh toán bởi kênh khác | `INVOICE_ALREADY_PAID` | *"This invoice has already been paid. Please check your transaction history."* | Alert banner đỏ nổi bật `div[role='alert']`, nút quay về danh sách. |
| Lỗi mạng hoặc máy chủ không phản hồi | `NETWORK_ERROR` | *"Unable to process your payment authorization. Please try again."* | Alert banner đỏ, nút Authorize được mở lại để retry. |
| Phiên làm việc Singpass hết hạn | `AUTH_REQUIRED` | *"Your session has expired. Please log in again to continue."* | Thông báo kèm link điều hướng về Singpass login. |

---

## 5. JSON Fixtures Data Payload

```json
{
  "review_and_confirm_fixtures": {
    "full_ea_review": {
      "student_name": "Chloe Chan",
      "items": [
        { "desc": "Term 4 Stationery Fee", "amount": 10.00 },
        { "desc": "Field Trip - Science Centre", "amount": 15.00 }
      ],
      "total_amount": 25.00,
      "method": "EducationAccount",
      "ea_current_balance": 50.00,
      "ea_deduction": 25.00,
      "ea_projected_balance": 25.00
    },
    "split_review": {
      "student_name": "Chloe Chan",
      "items": [
        { "desc": "Overseas Learning Trip Fee", "amount": 1500.00 }
      ],
      "total_amount": 1500.00,
      "method": "Both",
      "ea_deduction": 50.00,
      "online_deduction": 1450.00,
      "ea_projected_balance": 0.00
    }
  }
}
```
