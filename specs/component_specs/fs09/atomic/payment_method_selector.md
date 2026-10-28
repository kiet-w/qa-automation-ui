# Component Specification: Payment Method Selector (Billing & Payment)

## 1. Metadata & Selector

| Attribute | Specification |
| :--- | :--- |
| **Component Name** | `PaymentMethodSelectorComponent` |
| **Target Page / Route** | `/billing/{studentId}` (`BillingPaymentPage`, SCR-04) |
| **Element Hierarchy** | Fieldset `<fieldset>`, Radio options `<input type='radio'>`, Guidance labels `<label>`, Breakdown container `<div>`, Action buttons `<button>` |
| **Visual State** | Step 2 của quy trình thanh toán sau khi đã chọn ít nhất 1 khoản phí ở Step 1 |
| **Component Scope** | Cho phép lựa chọn phương thức thanh toán: Tài khoản Giáo dục (EA), Trực tuyến (Online Gateway), hoặc Chia đôi (Split) |

### Playwright Live DOM Locators
```python
# Extracted from pages/fs09/billing_payment_page.py
METHOD_HEADING = "h2#billing-method-heading"
METHOD_RADIO_GROUP = "fieldset, div[class*='method']"
RADIO_EA = "input[type='radio'][value='EducationAccount']"
RADIO_SPLIT = "input[type='radio'][value='Both']"
RADIO_ONLINE = "input[type='radio'][value='OnlineGateway']"
FUNDING_BREAKDOWN = "div[class*='fundingBreakdown'], div[class*='splitBreakdown']"
STEP2_BACK_BTN = "div[class*='method'] button:has-text('Back')"
STEP2_CONTINUE_BTN = "div[class*='method'] button:has-text('Continue')"
ALERT = "div[role='alert']"
```

---

## 2. Business Rules & Acceptance Criteria Traceability

| ID | Type | Description | Source Reference |
| :--- | :--- | :--- | :--- |
| **BR-F9-02** | Business Rule | Education Account must exist and be in Active status to be used as payment source. Closed or suspended accounts cannot be debited. | `specs/md/FS document/FS-09_Outstanding_Fees_and_Payment.md` |
| **BR-F9-07** | Business Rule | Non-Singapore Citizen students do not have an Education Account. Only Online Gateway payment method is available. | `specs/md/FS document/FS-09_Outstanding_Fees_and_Payment.md` |
| **BR-F9-10** | Business Rule | Split payment eligibility: Available only if Education Account is Active and has a balance $> 0$. | `specs/md/FS document/FS-09_Outstanding_Fees_and_Payment.md` |
| **AC-04** | Acceptance Criteria | Method selection: If EA balance $\ge$ Net amount, allow Full EA or Online. If $0 < \text{EA balance} < \text{Net}$, allow Split or Online. If $\text{EA} = 0$ or not eligible, allow only Online. | `specs/md/Test Cases/TC_R9_Outstanding_Fees_and_Payment.md` |
| **AC-14** | Acceptance Criteria | Verify dynamic disablement of payment options with explanatory text when balance is insufficient or account is inactive. | `specs/md/Test Cases/TC_R9_Outstanding_Fees_and_Payment.md` |
| **AC-22** | Acceptance Criteria | Radio option mutual exclusivity: Selecting one method deselects any previously selected method. | `specs/md/Test Cases/TC_R9_Outstanding_Fees_and_Payment.md` |

---

## 3. Ma trận 12 lớp Validation & UI Integrity

| Lớp (Layer) | Phân Loại Kiểm Thử | Dữ Liệu Đầu Vào (Input Vector) | Trạng Thái / Hành Vi UI Kỳ Vọng | Tiêu Chí Đạt (Pass Criteria) |
| :--- | :--- | :--- | :--- | :--- |
| **1. EA Balance $\ge$ Net Amount** | Đủ số dư trả 100% EA | Net = `$44.50`, EA Balance = `$650.00` | Cả 2 tùy chọn `EducationAccount` và `OnlineGateway` đều ENABLED. Tùy chọn Split bị ẩn hoặc vô hiệu (vì số dư đã đủ trả hết). | Radio EA click được, Radio Online click được. |
| **2. $0 < \text{EA Balance} < \text{Net}$**| Thiếu số dư (Đủ điều kiện Split)| Net = `$1,500.00`, EA Balance = `$50.00` | Radio `EducationAccount` bị **DISABLED** (kèm lý do `EA_INSUFFICIENT_BALANCE`). Radio `Both` (Split) và `OnlineGateway` là **ENABLED**. | Radio EA disabled; Radio Split selectable. |
| **3. EA Balance = $0.00$** | Số dư EA bằng 0 | Net = `$50.00`, EA Balance = `$0.00` | Radio `EducationAccount` và Radio `Both` bị **DISABLED**. Chỉ duy nhất Radio `OnlineGateway` là **ENABLED**. | Chỉ chọn được OnlineGateway. |
| **4. Non-Citizen / No EA** | Không có tài khoản EA | Học sinh ngoại quốc (No EA) | Radio EA và Split bị ẩn hoặc disabled kèm ghi chú: `EA_NOT_AVAILABLE`. Radio `OnlineGateway` tự động chọn sẵn. | Không thể chọn EA. |
| **5. Closed / Suspended EA** | Tài khoản EA đã đóng | EA Status = `"Closed"` | Tùy chọn EA bị disabled với lý do `EA_NOT_ACTIVE`. Không cho phép chia đôi hay trả bằng EA. | Chặn trả qua EA Closed. |
| **6. Radio Mutual Exclusivity** | Tính loại trừ lẫn nhau | Click chọn qua lại giữa EA và Online | Tại một thời điểm chỉ có DUY NHẤT 1 radio button có trạng thái `checked=true`. | Không bao giờ có 2 radio cùng checked. |
| **7. Dynamic Split Fields Reveal** | Bật mở ô chia tiền | Click chọn radio `Both` (Split) | Khối chia tiền `FUNDING_BREAKDOWN` xuất hiện, hiển thị ô nhập số tiền EA và nhãn số tiền trực tuyến tự động tính. | Selector `SPLIT_EA_INPUT` hiển thị. |
| **8. Dynamic Split Fields Hide** | Ẩn khối chia tiền | Đang chọn Split -> Chuyển sang Online | Khối chia tiền lập tức biến mất khỏi DOM; không gửi giá trị split lên server. | Khối split detached hoặc ẩn. |
| **9. Navigation Back to Step 1** | Quay lại bước trước | Click nút "Back" ở Step 2 | Quay lại Step 1 (Bảng phí); các checkbox đã chọn ở Step 1 vẫn được bảo toàn nguyên vẹn. | Quay lại SCR-02 an toàn. |
| **10. Accessibility ARIA Group** | WCAG 2.1 AA Compliance | Kiểm tra ngữ nghĩa radio | Nhóm radio được bọc trong `<fieldset>` với `<legend>` mô tả rõ ràng; hỗ trợ phím mũi tên `Arrow Up`/`Arrow Down` để chuyển chọn. | Chuẩn accessibility form control. |
| **11. Prevent Continue Unselected** | Chưa chọn phương thức | Không tích chọn radio nào | Nút Continue ở Step 2 bị **DISABLED** (hoặc báo lỗi yêu cầu chọn trước khi tiếp tục). | Continue button disabled. |
| **12. Double-Click Continue** | Chống click đúp | Click liên tục nút Continue | Chỉ mở Step 3 một lần duy nhất, không gây flickering hoặc reload lại trạng thái. | Chuyển sang Review mượt mà. |

---

## 4. Error Handling & Visual Feedback

| Mã Lỗi Hệ Thống | Điều Kiện Kích Hoạt | Nội Dung Thông Báo Hiển Thị Chuẩn | Vị Trí & Visual Indicator |
| :--- | :--- | :--- | :--- |
| `EA_NOT_AVAILABLE` | Con không có Education Account (Foreigner/PR) | *"This student does not have an Education Account. Please pay online."* | Nhãn giải thích màu xám/vàng ngay dưới option EA bị mờ. |
| `EA_NOT_ACTIVE` | Tài khoản EA có trạng thái `Closed` hoặc `Suspended` | *"The Education Account is not active. Please pay online."* | Nhãn giải thích dưới option EA, radio bị disabled. |
| `EA_INSUFFICIENT_BALANCE`| Số dư EA nhỏ hơn tổng Net hóa đơn | *"Your Education Account balance is not enough for this amount. You can pay the rest online."* | Text trợ giúp màu cam/xám bên cạnh tùy chọn EA full, hướng dẫn dùng Split. |

---

## 5. JSON Fixtures Data Payload

```json
{
  "payment_method_fixtures": {
    "scenario_sufficient_ea": {
      "student_name": "Chloe Chan",
      "net_amount": 44.50,
      "ea_balance": 650.00,
      "ea_status": "Active",
      "allowed_methods": ["EducationAccount", "OnlineGateway"],
      "recommended_default": "EducationAccount"
    },
    "scenario_insufficient_ea_split_eligible": {
      "student_name": "Tan Wei Ming",
      "net_amount": 1500.00,
      "ea_balance": 50.00,
      "ea_status": "Active",
      "allowed_methods": ["Both", "OnlineGateway"],
      "disabled_methods": ["EducationAccount"],
      "expected_ea_error": "Your Education Account balance is not enough for this amount. You can pay the rest online."
    },
    "scenario_zero_ea_online_only": {
      "student_name": "Student Zero",
      "net_amount": 80.00,
      "ea_balance": 0.00,
      "ea_status": "Active",
      "allowed_methods": ["OnlineGateway"],
      "disabled_methods": ["EducationAccount", "Both"]
    },
    "scenario_non_citizen": {
      "student_name": "K. Shanmugam Child",
      "net_amount": 120.00,
      "ea_balance": null,
      "citizenship": "Foreigner",
      "allowed_methods": ["OnlineGateway"],
      "expected_ea_error": "This student does not have an Education Account. Please pay online."
    }
  }
}
```
