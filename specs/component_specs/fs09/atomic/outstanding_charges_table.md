# Component Specification: Outstanding Charges Table (Billing & Payment)

## 1. Metadata & Selector

| Attribute | Specification |
| :--- | :--- |
| **Component Name** | `OutstandingChargesTableComponent` |
| **Target Page / Route** | `/billing/{studentId}` (`BillingPaymentPage`, SCR-02 & SCR-03) |
| **Element Hierarchy** | Summary cards container `<div>`, Charges table `<table>`, Filter dropdown `<select>`, Select-all checkbox `<input>`, Continue button `<button>` |
| **Visual State** | Step 1 của quy trình thanh toán hóa đơn |
| **Component Scope** | Hiển thị bảng danh sách các khoản phí nợ của học sinh, cho phép tích chọn và tính tổng tức thì |

### Playwright Live DOM Locators
```python
# Extracted from pages/fs09/billing_payment_page.py
CHARGES_HEADING = "h2#billing-charges-heading, article[class*='tableCard'] h2"
SUMMARY_CARDS_CONTAINER = "div[class*='selectionSummaryCards']"
OUTSTANDING_FEES_SUMMARY = "[class*='summaryCard']:has-text('Outstanding fees') strong"
EA_BALANCE_SUMMARY = "[class*='summaryCard']:has-text('Education Account balance') strong"
SELECTED_TOTAL_SUMMARY = "[class*='summaryCard']:has-text('Selected total') strong"

STATUS_FILTER_SELECT = "select:has(option[value='All']), [class*='filterField'] select"
CHARGES_TABLE = "table"
CHARGES_ROWS = "table tbody tr"
SELECT_ALL_CHECKBOX = "input[type='checkbox'][aria-label*='Select all'], div[class*='selectAll'] input[type='checkbox']"
ROW_CHECKBOX = "input[type='checkbox']"
SELECTED_COUNTER = "span[class*='selectionSummary']"
STEP1_CONTINUE_BTN = "button:has-text('Continue')"
EMPTY_CHARGES_NOTICE = "div[class*='emptyState'][role='status'], td:has-text('No outstanding charges')"
```

---

## 2. Business Rules & Acceptance Criteria Traceability

| ID | Type | Description | Source Reference |
| :--- | :--- | :--- | :--- |
| **BR-F9-04** | Business Rule | Parent pays invoice in full. Cannot pay individual line items or make partial payments against an invoice line. | `specs/md/FS document/FS-09_Outstanding_Fees_and_Payment.md` |
| **BR-F9-07** | Business Rule | Non-Singapore Citizen students do not have an Education Account. EA balance is not shown, and payment must proceed via Online Gateway. | `specs/md/FS document/FS-09_Outstanding_Fees_and_Payment.md` |
| **BR-F9-12** | Business Rule | Gross amount, Subsidy amount, and Net amount calculation: $Net = Gross - Subsidy$. All values are SGD Decimal(18,2). | `specs/md/FS document/FS-09_Outstanding_Fees_and_Payment.md` |
| **BR-F9-13** | Business Rule | Selected total is the exact mathematical sum of Net amounts for all checked rows. | `specs/md/FS document/FS-09_Outstanding_Fees_and_Payment.md` |
| **AC-02** | Acceptance Criteria | View outstanding charges: Display fee type, description, due date, gross, subsidy, and net amount. If no charges exist, display empty state SCR-03. | `specs/md/Test Cases/TC_R9_Outstanding_Fees_and_Payment.md` |
| **AC-03** | Acceptance Criteria | Select charges: Parent can select one or more outstanding charges. Summary card dynamically updates "Selected total". | `specs/md/Test Cases/TC_R9_Outstanding_Fees_and_Payment.md` |
| **AC-11** | Acceptance Criteria | Continue button is disabled when 0 charges are selected, and enabled when $\ge 1$ charge is checked. | `specs/md/Test Cases/TC_R9_Outstanding_Fees_and_Payment.md` |

---

## 3. Ma trận 12 lớp Validation & UI Integrity

| Lớp (Layer) | Phân Loại Kiểm Thử | Dữ Liệu Đầu Vào (Input Vector) | Trạng Thái / Hành Vi UI Kỳ Vọng | Tiêu Chí Đạt (Pass Criteria) |
| :--- | :--- | :--- | :--- | :--- |
| **1. Initial Pristine State** | Trạng thái tải ban đầu | Mở `/billing/{student_id}` | Chưa có checkbox nào được chọn mặc định. Selected total = `0.00` SGD. Nút Continue bị **DISABLED**. | Continue button disabled. |
| **2. Single Row Selection** | Chọn 1 dòng đơn lẻ | Tích chọn checkbox dòng 1 ($10.00) | Selected total cập nhật ngay thành `$10.00`. Counter hiển thị `1 selected`. Nút Continue trở nên **ENABLED**. | Selected total = `$10.00`. |
| **3. Multi-Row Selection** | Chọn nhiều dòng | Tích chọn dòng 1 ($10.00) và dòng 2 ($15.00) | Selected total cộng dồn chính xác thành `$25.00`. Counter hiển thị `2 selected`. | Phép tính cộng dồn số học chính xác. |
| **4. Select All Checkbox** | Chọn toàn bộ bảng | Click checkbox "Select all" trên Header | Toàn bộ checkbox của các hàng trong bảng đồng loạt được check. Selected total = Tổng toàn bộ hóa đơn Issued. | Tất cả checkbox `checked=true`. |
| **5. Deselect All** | Hủy chọn toàn bộ | Click lại "Select all" đang checked | Toàn bộ checkbox bị bỏ chọn. Selected total trở về `$0.00`. Nút Continue bị **DISABLED**. | Nút Continue bị disable lại. |
| **6. Partial Uncheck (Indeterminate)**| Bỏ chọn một phần | Đang Select All -> Bỏ tích 1 dòng | Checkbox "Select all" chuyển sang trạng thái `indeterminate` (gạch ngang). Total giảm trừ đúng dòng đã bỏ. | Trạng thái tri-state hoạt động đúng. |
| **7. Currency 2-Decimal Precision** | Định dạng tiền tệ | Giá trị tiền bất kỳ | Luôn hiển thị 2 chữ số thập phân và dấu phân cách hàng nghìn (ví dụ `$1,500.00`, `$10.00`). Không bị làm tròn sai số thực. | Regex `^\$\d{1,3}(,\d{3})*\.\d{2}$`. |
| **8. Status Filter Dropdown** | Lọc theo trạng thái | Chọn filter "Issued" vs "Paid" vs "All" | Bảng tự động lọc các dòng tương ứng mà không cần reload trang. | Số lượng dòng hiển thị thay đổi tương ứng. |
| **9. Zero State (SCR-03)** | Trạng thái không có nợ | Học sinh đã thanh toán hết nợ | Bảng ẩn đi; hiển thị card trạng thái rỗng: *"There are no outstanding fees for this child."* kèm liên kết quay lại SCR-01. | Notice rỗng hiển thị rõ ràng. |
| **10. Non-Citizen EA Notice** | Học sinh không có EA | Học sinh mang quốc tịch nước ngoài / PR | Cột/Card EA Balance hiển thị *"Not eligible"* hoặc *"No Education Account"*. Không hiển thị lỗi giả tạo. | Hiển thị thông báo thân thiện. |
| **11. Inactive/PaymentPending Locked**| Hóa đơn đang chờ xử lý | Invoice có trạng thái `PaymentPending` | Checkbox của dòng bị vô hiệu hóa (`disabled="true"`), nhãn trạng thái màu vàng, không cho phép chọn trùng lặp. | Không thể tích chọn invoice pending. |
| **12. Double-Click Continue** | Chống click đúp | Bấm liên tục nút Continue | Chỉ chuyển sang Step 2 duy nhất một lần, không phát sinh duplicate state transition. | Chỉ có 1 lần chuyển bước. |

---

## 4. Error Handling & Visual Feedback

| Tình Huống Kích Hoạt | Mã Lỗi Chuẩn | Nội Dung Thông Báo Bắt Buộc | Trạng Thái DOM & Style |
| :--- | :--- | :--- | :--- |
| Không có khoản phí nào còn nợ | `SCR-03` | *"There are no outstanding fees for this child."* hoặc *"No outstanding charges"* | Trạng thái rỗng màu xanh/xám nhẹ, nút quay lại danh sách con. |
| Hóa đơn đã bị phụ huynh khác thanh toán trong lúc đang mở | `INVOICE_ALREADY_PAID` | *"This invoice has already been paid."* | Alert banner đỏ `div[role='alert']`, tự động làm mới danh sách phí. |
| Dữ liệu hóa đơn đã bị thay đổi (Stale) | `STALE_FEES` | *"The fees have changed. Please review the updated charges."* | Alert banner vàng/cam, bảng tự động re-fetch dữ liệu mới nhất. |

---

## 5. JSON Fixtures Data Payload

```json
{
  "charges_table_fixtures": {
    "student_with_charges": {
      "student_id": "01a15a22-dddf-750e-ac12-6d155e779d11",
      "ea_balance": 50.00,
      "items": [
        { "id": "bbbb0009-0000-0000-0000-000000000001", "desc": "Term 4 Stationery Fee", "gross": 10.00, "subsidy": 0.00, "net": 10.00, "status": "Issued" },
        { "id": "bbbb0009-0000-0000-0000-000000000002", "desc": "Field Trip - Science Centre", "gross": 15.00, "subsidy": 0.00, "net": 15.00, "status": "Issued" },
        { "id": "bbbb0009-0000-0000-0000-000000000003", "desc": "Sports Fee", "gross": 25.00, "subsidy": 0.00, "net": 25.00, "status": "Issued" }
      ],
      "total_outstanding": 50.00
    },
    "student_zero_charges": {
      "student_id": "01a15a22-f573-7ba6-93d2-71ac9a4ce40b",
      "ea_balance": 40.00,
      "items": [],
      "total_outstanding": 0.00
    },
    "student_non_citizen": {
      "student_id": "01a15a22-9999-7ba6-93d2-71ac9a4ce40b",
      "ea_balance": null,
      "citizenship": "Foreigner",
      "expected_ea_status": "No Education Account"
    }
  }
}
```
