# Component Specification: Bulk CSV School User Import (School User Management)

## 1. Metadata & Selector

| Attribute | Specification |
| :--- | :--- |
| **Component Name** | `SchoolUserBulkCsvUploadComponent` |
| **Target Page / Route** | `/school-user-management/new` (`SchoolUserCreatePage`, Bulk CSV Tab) |
| **Element Hierarchy** | Tab group `<div role='tablist'>`, File input `<input type='file'>`, Buttons `<button>`, Batch progress & report table `<div>` |
| **Visual State** | Tab "Bulk CSV" active trên màn hình tạo School User |
| **Component Scope** | Tải lên danh sách người dùng hàng loạt qua tệp CSV (tối đa 1,000 dòng), kiểm tra cấu trúc header, validate từng dòng và báo cáo chi tiết |

### Playwright Live DOM Locators
```python
# Extracted from pages/fs03/school_user_create_page.py
BULK_TAB = "button[role='tab']:has-text('Bulk CSV')"
GET_TEMPLATE_BTN = "button:has-text('Get Template')"
FILE_INPUT = "#school-users-csv"
IMPORT_BTN = "button:has-text('Import')"
RESET_BTN = "button:has-text('Reset')"
BACK_TO_LIST_BTN = "button:has-text('Back to list')"

ALERTS = "[role='alert']"
RESULT_CARD = "div[aria-live='polite']"
REPORT_TABLE = "div[aria-live='polite'] table"
SUCCESS_SUMMARY = "text='School users imported successfully'"
```

---

## 2. Business Rules & Acceptance Criteria Traceability

| ID | Type | Description | Source Reference |
| :--- | :--- | :--- | :--- |
| **R3-F02** | Functional Req | Bulk School User Provisioning: MOE Admin uploads CSV to create up to 1,000 school users in a batch. | `specs/md/FS document/FS-03_School_Student_Fee_Management.md` |
| **BR-03-04** | Business Rule | CSV Batch Resilience & Partial Success: Process continues across valid rows even when individual rows fail. Detailed row-by-row status reported. | `specs/validation_rules/md/R3_Validation_Rules.md` |
| **AC-06** | Acceptance Criteria | File and Header Validation: Accept only `.csv`, reject empty file or $>1,000$ rows. Verify case-insensitive headers. | `specs/validation_rules/md/R3_Validation_Rules.md` |
| **AC-07** | Acceptance Criteria | Row-Level Reporting: Each failed row reports row number and explicit error reason (duplicate NRIC/email, invalid format, inactive school). | `specs/validation_rules/md/R3_Validation_Rules.md` |

---

## 3. Ma trận 12 lớp Validation & UI Integrity

| Lớp (Layer) | Phân Loại Kiểm Thử | Dữ Liệu Đầu Vào (Input Vector) | Trạng Thái / Hành Vi UI Kỳ Vọng | Tiêu Chí Đạt (Pass Criteria) |
| :--- | :--- | :--- | :--- | :--- |
| **1. No File Selected** | Chưa chọn tệp khi bấm Import | Bấm nút "Import" khi chưa chọn tệp CSV | Báo lỗi ngay lập tức: `"Please choose a CSV file."`. Nút Import không gửi request rỗng. | Alert chọn file xuất hiện. |
| **2. Template Download** | Tải template mẫu | Click `"Get Template"` | Trình duyệt kích hoạt tải tệp mẫu hợp lệ (`school_users_template.csv` hoặc `.xlsx`). | Event download được trigger. |
| **3. Empty CSV File** | Tệp rỗng 0 bytes | Upload tệp `empty.csv` (dung lượng 0 bytes) | Báo lỗi: `"The CSV file is empty."`. | Alert file rỗng. |
| **4. Max Rows Boundary (1,000 vs 1,001)** | Biên số lượng dòng tối đa | Tệp có 1,000 dòng vs 1,001 dòng dữ liệu | 1,000 dòng được chấp nhận xử lý; 1,001 dòng bị từ chối với: `"The CSV file may contain at most 1000 rows."`. | Giới hạn 1,000 dòng thực thi đúng. |
| **5. Missing Header Column** | Thiếu cột bắt buộc | Thiếu cột `School User Email` trong header | Từ chối tệp với thông báo: `"Missing CSV column: School User Email"`. | Báo rõ tên cột bị thiếu. |
| **6. Case-Insensitive Headers** | Chữ hoa/thường trong header | Header dùng `school user nric`, `FIRST NAME` | Chấp nhận hợp lệ, parse chính xác các trường dữ liệu. | Parser khớp không phân biệt hoa thường. |
| **7. Row Invalid NRIC** | Lỗi NRIC tại dòng 3 | Dòng 3 có NRIC `"12345678"` (không có chữ cái) | Dòng 3 được đánh dấu Failed: `"NRIC must contain 1 letter, 7 digits, and 1 letter."`. Các dòng khác tiếp tục xử lý. | Báo cáo dòng 3 thất bại. |
| **8. Row Duplicate Email Conflict**| Lỗi trùng email tại dòng 5 | Dòng 5 có email đã tồn tại trong DB | Dòng 5 thất bại: `"User with email '{email}' already exists."`. | Báo cáo chi tiết dòng 5. |
| **9. Malformed Row (Too Many Columns)**| Thừa cột dữ liệu | Dòng 7 có 8 cột thay vì 6 cột | Báo lỗi: `"CSV row 7 contains too many columns."`. | Bắt lỗi phân tách dấu phẩy. |
| **10. Inactive School Code in Row**| Gán trường đã đóng | Dòng 8 gán mã trường `"SCH-INACTIVE-999"` | Báo lỗi: `"School 'SCH-INACTIVE-999' is inactive."`. | Chặn gán trường đóng. |
| **11. Blank Rows Handling** | Dòng trống giữa tệp | Dòng có toàn dấu phẩy `,,,,,` | Hệ thống tự động bỏ qua (skip), không tính vào lỗi và không lưu bản ghi rác. | Bỏ qua dòng trắng. |
| **12. Reset Button Clears State** | Reset sau khi upload | Bấm nút `"Reset"` sau khi import | Tệp đã chọn bị gỡ bỏ, bảng báo cáo kết quả bị xóa, form sẵn sàng cho mẻ upload mới. | Trở về trạng thái sạch ban đầu. |

---

## 4. Error Handling & Visual Feedback

| Cấp Độ Lỗi | Thông Báo Lỗi Chuẩn | Nguyên Nhân Kích Hoạt | Xử Lý Giao Diện |
| :--- | :--- | :--- | :--- |
| **File Level** | `"Please choose a CSV file."` | Chưa đính kèm file | Inline alert màu đỏ |
| **File Level** | `"The CSV file is empty."` | Tệp 0 byte hoặc không có dòng data | Banner alert màu đỏ |
| **File Level** | `"The CSV file may contain at most 1000 rows."` | Vượt quá 1,000 dòng | Banner alert màu đỏ |
| **File Level** | `"Missing CSV column: {header}"` | Thiếu cột header bắt buộc | Banner alert màu đỏ kèm tên cột |
| **Row Level** | `"Row {N}: NRIC must contain 1 letter, 7 digits, and 1 letter."` | Sai cú pháp NRIC dòng N | Hiển thị trong bảng kết quả chi tiết dòng N |
| **Row Level** | `"Row {N}: User with email '{email}' already exists."` | Trùng email tại dòng N | Hiển thị trong bảng kết quả chi tiết dòng N |
| **Row Level** | `"Row {N}: School code '{code}' does not exist."` | Mã trường không có thật | Hiển thị trong bảng kết quả chi tiết dòng N |

---

## 5. JSON Fixtures Data Payload & CSV Samples

```json
{
  "bulk_csv_fixtures": {
    "valid_csv_sample": "No,School User NRIC,School User Email,First Name,Last Name,School Code (optional)\n1,S9123451A,john.doe@IAM.edu.vn,John,Doe,RPS-0201\n2,S9123452B,jane.smith@IAM.edu.vn,Jane,Smith,HCI-0102\n3,S9123453C,unassigned.user@IAM.edu.vn,Bob,Lee,",
    "missing_header_sample": "No,NRIC,First Name,Last Name\n1,S9123451A,John,Doe",
    "mixed_errors_sample": "No,School User NRIC,School User Email,First Name,Last Name,School Code (optional)\n1,S9123451A,valid.user@IAM.edu.vn,Valid,User,RPS-0201\n2,INVALID_NRIC,test2@IAM.edu.vn,Invalid,Nric,RPS-0201\n3,S9123453C,admin@IAM.edu.vn,Duplicate,Email,RPS-0201\n4,S9123454D,inactive@IAM.edu.vn,Inactive,School,SCH-INACTIVE-999"
  }
}
```
