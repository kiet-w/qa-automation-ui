# Component Specification: Payment Result & Official Receipt (Billing & Payment)

## 1. Metadata & Selector

| Attribute | Specification |
| :--- | :--- |
| **Component Name** | `PaymentResultReceiptComponent` |
| **Target Page / Route** | `/payment-result` (`PaymentResultPage`, SCR-07 & SCR-08) |
| **Element Hierarchy** | Status banner `<div>`, Receipt card `<article>`, Description list `<dl>`, Line items `<ul>`, Action buttons `<div>` |
| **Visual State** | Màn hình kết quả giao dịch và biên lai chính thức |
| **Component Scope** | Hiển thị trạng thái giao dịch (Thành công / Thất bại), biên lai thanh toán điện tử, thông báo hoàn tiền EA tự động khi xảy ra sự cố Split payment |

### Playwright Live DOM Locators
```python
# Extracted from pages/fs09/payment_result_page.py
PAGE_HEADING = "h1#payment-result-heading"
RESULT_STATUS_BANNER = "div[class*='resultStatus']"
STATUS_HEADING = "div[class*='resultStatus'] h2"
STATUS_DESCRIPTION = "div[class*='resultStatus'] p:first-of-type"
EA_REVERSAL_NOTICE = "div[class*='resultStatus'] p:has-text('returned'), div[class*='resultStatus'] p:has-text('refunded')"

TRANSACTION_ID_VALUE = "dt:has-text('Transaction ID') + dd, dt:has-text('Transaction') + dd"
INVOICE_NUMBER_VALUE = "dt:has-text('Invoice number') + dd, dt:has-text('Invoice') + dd"
INVOICE_STATUS_VALUE = "dt:has-text('Invoice status') + dd"
COMPLETED_AT_VALUE = "dt:has-text('Completed at') + dd"
REQUESTED_AMOUNT_VALUE = "dt:has-text('Requested amount') + dd"
SETTLED_AMOUNT_VALUE = "dt:has-text('Settled amount') + dd"
INVOICE_ITEMS_LIST = "ul[class*='invoiceItems'] > li"

PRINT_RECEIPT_BTN = "button:has-text('Print receipt'), button:has-text('Print')"
HOME_LINK = "a[class*='homeLink'], a:has-text('Home'), a[href='/']"
BILLING_LINK = "a:has-text('Billing'), a[href='/billing']"
RETRY_BTN = "button:has-text('Retry')"
```

---

## 2. Business Rules & Acceptance Criteria Traceability

| ID | Type | Description | Source Reference |
| :--- | :--- | :--- | :--- |
| **BR-F9-05** | Business Rule | Invoice status transition to `Paid`: Once all funding legs settle successfully, invoice status transitions to `Paid`. Official receipt is issued. | `specs/md/FS document/FS-09_Outstanding_Fees_and_Payment.md` |
| **BR-F9-06** | Business Rule | Split payment automated reversal: If the Online Gateway leg fails during Split payment, the previously deducted Education Account amount **MUST BE AUTOMATICALLY REFUNDED/REVERSED** back to the child's EA balance. | `specs/md/FS document/FS-09_Outstanding_Fees_and_Payment.md` |
| **BR-F9-14** | Business Rule | Invoice reversion on failure: When payment fails (or split fails and reverses), the invoice status **MUST REVERT TO `Issued`** so the parent can retry. | `specs/md/FS document/FS-09_Outstanding_Fees_and_Payment.md` |
| **AC-06** | Acceptance Criteria | Receipt presentation: Display Transaction ID, invoice number, items, settled amount, date/time, and Print button. | `specs/md/Test Cases/TC_R9_Outstanding_Fees_and_Payment.md` |
| **AC-08** | Acceptance Criteria | Failed Payment Presentation: Show clear failure status banner and reason; provide Retry and Billing navigation links. | `specs/md/Test Cases/TC_R9_Outstanding_Fees_and_Payment.md` |
| **AC-20** | Acceptance Criteria | Reversal Notification: When Split online leg fails, display clear prominent notice that the EA deducted portion has been returned. | `specs/md/Test Cases/TC_R9_Outstanding_Fees_and_Payment.md` |

---

## 3. Ma trận 12 lớp Validation & UI Integrity

| Lớp (Layer) | Phân Loại Kiểm Thử | Dữ Liệu Đầu Vào (Input Vector) | Trạng Thái / Hành Vi UI Kỳ Vọng | Tiêu Chí Đạt (Pass Criteria) |
| :--- | :--- | :--- | :--- | :--- |
| **1. Success Status Banner** | Thanh trạng thái thành công | Thanh toán Full EA hoặc Online thành công | Banner xanh lá (`bg-green-50`), Heading: *"Payment successful"*, nhãn trạng thái *"Paid"*. | Banner xanh lá, text "Payment successful". |
| **2. Failure Status Banner** | Thanh trạng thái thất bại | Gateway báo thẻ bị từ chối / timeout | Banner đỏ (`bg-red-50`), Heading: *"Payment failed"*, nhãn trạng thái *"Failed"*. | Banner đỏ, text "Payment failed". |
| **3. Automated EA Reversal Notice** | Thông báo hoàn tiền EA tự động | Split payment có Online leg thất bại | Hiển thị đoạn văn bản thông báo: *"The amount deducted from your Education Account has been returned to your balance."*. | Selector `EA_REVERSAL_NOTICE` hiển thị. |
| **4. Transaction ID Integrity** | Mã giao dịch duy nhất | Transaction hoàn tất | Hiển thị mã UUID/Reference hợp lệ, không bị rỗng hoặc undefined. | Text khớp UUID hoặc mã tham chiếu. |
| **5. Settled Amount Precision** | Số tiền quyết toán | Giao dịch thành công | Hiển thị đúng 2 chữ số thập phân, khớp với tổng tiền yêu cầu ban đầu (ví dụ: `$25.00`). | Settled amount = Requested amount. |
| **6. Timestamp Format** | Định dạng ngày giờ Singapore | Timestamp hoàn tất | Định dạng ngày tháng giờ Singapore: `DD/MM/YYYY, HH:mm SGT`. | Đúng format ngày giờ MOE. |
| **7. Invoice Line Items List** | Danh sách khoản phí | Hóa đơn có 2 dòng | Liệt kê đầy đủ 2 thẻ `<li>` hiển thị tên từng khoản phí và số tiền tương ứng. | Số lượng dòng khớp với hóa đơn. |
| **8. Print Receipt Action** | Thao tác in biên lai | Click button "Print receipt" | Kích hoạt sự kiện in trình duyệt `window.print()` (trong test xác minh mock call). | Hàm print được gọi. |
| **9. Return to Billing Link** | Điều hướng về trang nợ phí | Click link "Billing" hoặc "Back to billing" | Điều hướng về `/billing`; hóa đơn vừa trả đã biến mất khỏi danh sách Issued. | Hóa đơn đã Paid không còn trong nợ. |
| **10. Retry on Failure Action** | Thử lại khi thất bại | Click button "Retry" tại màn hình thất bại | Điều hướng quay lại SCR-02 hoặc SCR-04 của học sinh đó để thực hiện thanh toán lại. | Cho phép trả lại không bị bế tắc. |
| **11. Direct Access Tampering** | Truy cập trực tiếp không session | Gõ thẳng URL `/payment-result` không query param | Hiển thị heading `h1#payment-result-invalid-heading`: *"No payment transaction found"*; hướng dẫn về Home. | Không crash ứng dụng. |
| **12. Zero Horizontal Scrollbar** | Sức khỏe UI Invariant 7 | Xem biên lai trên màn hình chuẩn 1920x1080 & 1366x768 | Biên lai hiển thị gọn gàng trong container, không xuất hiện thanh cuộn ngang trang. | Không có scrollbar ngang. |

---

## 4. Error Handling & Visual Feedback

| Trạng Thái Giao Dịch | Tiêu Đề Banner | Nội Dung Thông Báo | Hành Động Khả Dụng |
| :--- | :--- | :--- | :--- |
| **Thành công (Paid)** | *"Payment successful"* | *"Thank you. Your payment has been processed and your official receipt is shown below."* | In biên lai, Quay lại Billing, Về trang chủ |
| **Thất bại thường (Failed)** | *"Payment failed"* | *"Your payment could not be completed. No funds were deducted from your accounts."* | Thử lại (Retry), Quay lại Billing |
| **Thất bại Split (Có hoàn EA)** | *"Payment failed"* | *"The online payment was not successful. The amount deducted from your Education Account has been returned to your balance."* | Thử lại (Retry), Quay lại Billing |
| **Không tìm thấy giao dịch** | *"Invalid payment result"* | *"No transaction details could be located for this session."* | Quay về trang chủ |

---

## 5. JSON Fixtures Data Payload

```json
{
  "payment_result_fixtures": {
    "success_receipt": {
      "transaction_id": "TXN-2026-00098234",
      "invoice_number": "INV-2026-0001",
      "invoice_status": "Paid",
      "requested_amount": 25.00,
      "settled_amount": 25.00,
      "completed_at": "26/10/2026, 14:30 SGT",
      "items": [
        { "name": "Term 4 Stationery Fee", "amount": 10.00 },
        { "name": "Field Trip - Science Centre", "amount": 15.00 }
      ]
    },
    "split_failure_with_reversal": {
      "transaction_id": "TXN-2026-00098235",
      "invoice_number": "INV-2026-0004",
      "invoice_status": "Issued",
      "requested_amount": 1500.00,
      "settled_amount": 0.00,
      "ea_reversed_amount": 50.00,
      "expected_reversal_notice": "The amount deducted from your Education Account has been returned to your balance."
    }
  }
}
```
