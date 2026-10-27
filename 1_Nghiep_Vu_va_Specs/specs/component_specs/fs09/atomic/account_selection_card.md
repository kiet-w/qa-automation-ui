# Component Specification: Account Selection Card (Billing & Payment)

## 1. Metadata & Selector

| Attribute | Specification |
| :--- | :--- |
| **Component Name** | `AccountSelectionCardComponent` |
| **Target Page / Route** | `/billing` (`BillingAccountSelectionPage`, SCR-01) |
| **Element Hierarchy** | Account list `<ul>`, Card item `<li>`, Card container `<article>`, Student link `<a>` |
| **Visual State** | Màn hình đầu tiên sau khi Parent đăng nhập để chọn con thanh toán |
| **Component Scope** | Hiển thị danh sách các tài khoản giáo dục của từng con liên kết với phụ huynh |

### Playwright Live DOM Locators
```python
# Extracted from pages/fs09/billing_account_selection_page.py
HEADING = "h1#billing-account-selection-heading"
ACCOUNT_GRID = "ul[aria-label='Education accounts'], ul[class*='accountGrid']"
ACCOUNT_CARDS = "ul[class*='accountGrid'] > li, ul[aria-label='Education accounts'] > li"
ACCOUNT_CARD_ARTICLES = "ul[class*='accountGrid'] li article, article[class*='accountCard']"
ACCOUNT_LINK = "a:has-text('View fees for'), a:has-text('Select account'), a[class*='accountLink']"
EMPTY_STATE = "div[class*='accountState'][role='status'], div[role='status']:has-text('No education accounts')"
LOADING_STATE = "p[class*='accountState'][role='status'], p[role='status']:has-text('Loading education accounts')"
ERROR_ALERT = "div[role='alert'], [class*='alert']"
RETRY_BUTTON = "button:has-text('Retry'), button:has-text('Try again')"
```

---

## 2. Business Rules & Acceptance Criteria Traceability

| ID | Type | Description | Source Reference |
| :--- | :--- | :--- | :--- |
| **BR-F9-01** | Business Rule | Parent can only view and pay outstanding fees for students linked to their Singpass account. The server validates the link on every request. | `specs/md/FS document/FS-09_Outstanding_Fees_and_Payment.md` |
| **AC-01** | Acceptance Criteria | Student Selection: View all linked children with student name, school, cohort/level, and class. Clicking a child card opens outstanding charges. | `specs/md/Test Cases/TC_R9_Outstanding_Fees_and_Payment.md` |
| **AC-12** | Acceptance Criteria | Access Control: Accessing charges for an unlinked student returns `FORBIDDEN_CHILD` error and redirects to SCR-01. | `specs/md/Test Cases/TC_R9_Outstanding_Fees_and_Payment.md` |
| **EX-01** | Exception Rule | Student not linked or relationship removed: Prompt error *"You do not have access to this student's records."* and redirect to SCR-01. | `specs/validation_rules/md/R9_OUTSTANDING_FEE_AND_PAYMENT_Validation_Rules.md` |

---

## 3. Ma trận 12 lớp Validation & UI Integrity

| Lớp (Layer) | Phân Loại Kiểm Thử | Dữ Liệu Đầu Vào (Input Vector) | Trạng Thái / Hành Vi UI Kỳ Vọng | Tiêu Chí Đạt (Pass Criteria) |
| :--- | :--- | :--- | :--- | :--- |
| **1. Linked Cards Display** | Danh sách con hợp lệ | Phụ huynh có 2 con (`Chloe Chan`, `Tan Wei Ming`) | Hiển thị đúng 2 thẻ học sinh độc lập, đúng tên, mã trường, cấp lớp. | Đủ 2 card, selector count = 2. |
| **2. Sorting Order** | Thứ tự hiển thị | Danh sách nhiều con | Tự động sắp xếp theo thứ tự bảng chữ cái A-Z theo Họ tên học sinh. | Tên hiển thị theo thứ tự từ điển A-Z. |
| **3. Outstanding Status Badge** | Nhãn trạng thái nợ | Con có hóa đơn Issued vs Không nợ | Hiển thị nhãn rõ ràng: *"Has outstanding invoices"* (nếu có nợ) hoặc *"No outstanding invoices"*. | Badge có màu tương ứng (amber/green). |
| **4. Zero Linked Students (Empty State)** | Trạng thái rỗng SCR-03 | Phụ huynh mới chưa có con nào liên kết | Không hiển thị thẻ học sinh, hiển thị thông báo rỗng: *"You have no linked student. Please contact your school."*. | Phần tử `EMPTY_STATE` hiển thị. |
| **5. Card Click Navigation** | Điều hướng khi click | Click vào thẻ của con `Chloe Chan` | Điều hướng sang URL `/billing/{student_id}` (SCR-02), tải danh sách phí. | URL khớp `/billing/<uuid>`. |
| **6. Double-Click Debounce** | Chống click đúp liên tục | Double click nhanh vào link thẻ con | Hệ thống xử lý debounce, chỉ thực hiện điều hướng 1 lần duy nhất, không tạo đa phiên. | Chỉ có 1 navigation request. |
| **7. Single Child Auto-Transition** | Hành vi mở rộng (Open Point O10) | Phụ huynh chỉ có duy nhất 1 con | Tùy chọn chuyển thẳng vào SCR-02 hoặc hiển thị 1 card với nút rõ ràng. | Không treo trang. |
| **8. Accessibility & Card Semantics** | WCAG 2.1 AA Compliance | Định hướng bàn phím `Tab` | Thẻ học sinh dùng thẻ ngữ nghĩa `<article>`, link có `aria-label` đầy đủ (ví dụ: `View fees for Chloe Chan`). | Focus indicator rõ ràng. |
| **9. Unauthorized Student Tampering** | Bảo mật BOLA / IDOR | Cố tình truy cập `/billing/{unauthorized_id}` | Bị chặn bởi máy chủ, hiển thị thông báo lỗi `FORBIDDEN_CHILD`, redirect về `/billing`. | Không lộ thông tin của học sinh khác. |
| **10. Pagination Handling** | Phân trang khi nhiều con | Phụ huynh có > 5 con | Hiển thị phân trang `<nav aria-label='Pagination'>` với nút Previous và Next hoạt động chính xác. | Nút Prev/Next chuyển trang mượt mà. |
| **11. Loading Skeleton / Spinner** | Trạng thái đang tải | Mạng chậm / độ trễ 2000ms | Hiển thị chỉ báo `Loading education accounts` với `role='status'`, không vỡ giao diện. | Skeleton biến mất khi tải xong. |
| **12. Load Error Fallback & Retry** | Xử lý lỗi API máy chủ | API danh sách con trả về 500 | Hiển thị alert *"Unable to load education accounts"* kèm nút **Retry**. Bấm Retry tải lại danh sách. | Nút Retry kích hoạt fetch lại. |

---

## 4. Error Handling & Visual Feedback

| Tình Huống Kích Hoạt | Mã Lỗi Chuẩn | Nội Dung Thông Báo Bắt Buộc | Trạng Thái DOM & Style |
| :--- | :--- | :--- | :--- |
| Không tìm thấy con nào liên kết | `EMPTY_STATE` | *"You have no linked student. Please contact your school."* | Box trạng thái rỗng trung tính, icon info, không có viền đỏ. |
| Cố tình can thiệp xem học sinh không liên kết | `FORBIDDEN_CHILD` | *"You do not have access to this student's records."* | Alert banner đỏ nổi bật `div[role='alert']`, tự động chuyển về `/billing`. |
| Lỗi tải danh sách tài khoản từ máy chủ | `LOAD_ERROR` | *"Something went wrong. Please try again later."* hoặc *"Unable to load education accounts"* | `div[role='alert']`, kèm nút `"Retry"`. |

---

## 5. JSON Fixtures Data Payload

```json
{
  "account_selection_fixtures": {
    "parent_with_multiple_children": {
      "parent_nric": "S7654321B",
      "children": [
        {
          "student_id": "01a15a22-dddf-750e-ac12-6d155e779d11",
          "student_name": "Chloe Chan",
          "school_name": "Rosyth Primary School",
          "level": "Primary 4",
          "class": "4A",
          "has_outstanding": true
        },
        {
          "student_id": "01a15a22-f573-7ba6-93d2-71ac9a4ce40b",
          "student_name": "Tan Wei Ming",
          "school_name": "Rosyth Primary School",
          "level": "Primary 6",
          "class": "6B",
          "has_outstanding": false
        }
      ]
    },
    "parent_zero_children": {
      "parent_nric": "S3456789C",
      "expected_empty_message": "You have no linked student. Please contact your school."
    },
    "unauthorized_access_attempt": {
      "tampered_student_id": "99999999-9999-9999-9999-999999999999",
      "expected_error": "You do not have access to this student's records."
    }
  }
}
```
