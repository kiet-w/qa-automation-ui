# Component Specification: Single School User Creation Form (School User Management)

## 1. Metadata & Selector

| Attribute | Specification |
| :--- | :--- |
| **Component Name** | `SchoolUserSingleCreateFormComponent` |
| **Target Page / Route** | `/school-user-management/new` (`SchoolUserCreatePage`, Single Tab) |
| **Element Hierarchy** | Tab group `<div role='tablist'>`, Form `<form>`, Inputs `<input>`, Action buttons `<button>`, Result card `<div>` |
| **Visual State** | Tab "Single" active trên màn hình tạo School User |
| **Component Scope** | Form tạo thủ công từng tài khoản nhân viên trường học, kiểm tra tính duy nhất NRIC và Email |

### Playwright Live DOM Locators
```python
# Extracted from pages/fs03/school_user_create_page.py
SINGLE_TAB = "button[role='tab']:has-text('Single')"
NRIC_INPUT = "#school-user-nric"
FIRST_NAME_INPUT = "#school-user-first-name"
LAST_NAME_INPUT = "#school-user-last-name"
EMAIL_INPUT = "#school-user-email"
MOE_SCHOOL_CODE_INPUT = "#school-user-moe-school-code"

CREATE_BTN = "button:has-text('Create')"
RESET_BTN = "button:has-text('Reset')"
BACK_TO_LIST_BTN = "button:has-text('Back to list')"

ALERTS = "[role='alert']"
SUCCESS_TOAST = "[role='status']:has-text('School user created')"
RESULT_CARD = "div[aria-live='polite']"
```

---

## 2. Business Rules & Acceptance Criteria Traceability

| ID | Type | Description | Source Reference |
| :--- | :--- | :--- | :--- |
| **R3-F02** | Functional Req | School User creation: Admin creates School User with NRIC, First Name, Last Name, Email, and optional School Code. | `specs/md/FS document/FS-03_School_Student_Fee_Management.md` |
| **BR-03-02** | Business Rule | NRIC Format & Uniqueness: NRIC must be exactly 9 characters (1 letter, 7 digits, 1 letter) and unique across all system users. | `specs/validation_rules/md/R3_Validation_Rules.md` |
| **BR-03-03** | Business Rule | Email Uniqueness & Domain: Email must be valid RFC 5322 format, maximum 100 characters, and unique in database. | `specs/validation_rules/md/R3_Validation_Rules.md` |
| **AC-03** | Acceptance Criteria | Single Form Validation: Disable "Create" button while any required field is blank. Validate lengths and formats. | `specs/validation_rules/md/R3_Validation_Rules.md` |
| **AC-04** | Acceptance Criteria | Success & Reset: On success show `"School user created"`. Reset button clears all fields and output cards. | `specs/validation_rules/md/R3_Validation_Rules.md` |

---

## 3. Ma trận 12 lớp Validation & UI Integrity

| Lớp (Layer) | Phân Loại Kiểm Thử | Dữ Liệu Đầu Vào (Input Vector) | Trạng Thái / Hành Vi UI Kỳ Vọng | Tiêu Chí Đạt (Pass Criteria) |
| :--- | :--- | :--- | :--- | :--- |
| **1. Required Empty Form** | Mặc định chưa nhập | Để trống NRIC, First Name, Last Name, Email | Nút "Create" bị **DISABLED**. Không gửi request lên máy chủ. | Create button disabled. |
| **2. NRIC Format BVA (8 vs 9 vs 10 chars)** | Cú pháp NRIC Singapore | `"12345678"` (8 số), `"S12345678A"` (10 ký tự) | Bị từ chối với thông báo: `"NRIC must be 1 letter, 7 digits and 1 letter (e.g. S1234567A)."`. | Alert lỗi NRIC hiển thị. |
| **3. Valid NRIC Formats** | NRIC/FIN hợp lệ | `"S1234567A"`, `"T7654321B"`, `"F1234567X"`, `"G9876543Z"` | Chấp nhận hợp lệ, xóa viền đỏ. | NRIC hợp lệ. |
| **4. Duplicate NRIC Conflict** | Trùng NRIC đã tồn tại | Nhập NRIC đã có trong DB (`"S8407384A"`) | Máy chủ trả về lỗi xung đột: `"User with NRIC 'S8407384A' already exists."`. | Banner lỗi trùng lặp xuất hiện. |
| **5. Duplicate Email Conflict**| Trùng Email đã có | Nhập email của Admin (`"admin@IAM.edu.vn"`) | Báo lỗi: `"User with email 'admin@IAM.edu.vn' already exists."`. | Alert trùng email. |
| **6. First/Last Name BVA Max** | Độ dài tên 100 vs 101 | Nhập 100 ký tự chữ vs 101 ký tự | 100 ký tự lưu thành công; 101 ký tự bị từ chối hoặc cắt ngắn an toàn. | Giới hạn 100 ký tự hoạt động. |
| **7. Email Format Validation** | Cú pháp Email | `"plainaddress"`, `"missing@domain"`, `"@no-user.com"` | Báo lỗi định dạng email: `"Enter a valid email address."`. | Alert định dạng email. |
| **8. Optional School Code** | Để trống mã trường | Bỏ trống `MOE school code` | Form vẫn hợp lệ; tạo user ở trạng thái `"Unassigned in any school"`. | Tạo thành công user chưa gán. |
| **9. Invalid School Code Format**| Ký tự cấm trong School Code | Nhập `"SC@#12"`, `"A"`, `"TOOLONGSCHOOLCODETHATEXCEEDS20CHARS"` | Báo lỗi: `"MOE school code must be between 3 and 20 characters."` hoặc `"only alphanumeric characters and hyphens."`. | Lỗi format trường học. |
| **10. Non-Existent School Code**| Mã trường không tồn tại | Nhập `"INVALID_SCH_999"` | Máy chủ trả về lỗi: `"School code 'INVALID_SCH_999' does not exist."`. | Báo không tìm thấy trường. |
| **11. Inactive School Assignment**| Gán vào trường đã đóng | Nhập mã trường Inactive (`"SCH-INACTIVE-999"`) | Báo lỗi: `"School 'SCH-INACTIVE-999' is inactive."`. Chặn gán vào trường không hoạt động. | Chặn gán trường inactive. |
| **12. Reset Button Clears State** | Thao tác xóa trắng form | Điền form đầy đủ -> Bấm nút `"Reset"` | Toàn bộ 5 ô input được xóa sạch giá trị; thẻ kết quả (nếu có) bị ẩn đi; nút Create trở về disabled. | Form sạch như ban đầu. |

---

## 4. Error Handling & Visual Feedback

| Tình Huống Kích Hoạt | Mã Lỗi / Loại Lỗi | Nội Dung Thông Báo Bắt Buộc | Trạng Thái DOM & Style |
| :--- | :--- | :--- | :--- |
| NRIC rỗng khi submit | Validation Error | `"NRIC is required."` | `aria-invalid="true"`, viền đỏ input |
| NRIC sai định dạng | Format Error | `"NRIC must be 1 letter, 7 digits and 1 letter (e.g. S1234567A)."` | `aria-invalid="true"`, viền đỏ input |
| NRIC đã tồn tại trong DB | Conflict Error 409 | `"User with NRIC '{nric}' already exists."` | Banner alert đỏ `[role='alert']` |
| Email đã tồn tại trong DB | Conflict Error 409 | `"User with email '{email}' already exists."` | Banner alert đỏ `[role='alert']` |
| Mã trường không tồn tại | Lookup Error 404 | `"School code '{moeSchoolCode}' does not exist."` | Banner alert đỏ `[role='alert']` |
| Mã trường đang Inactive | Business Rule Error | `"School '{code}' is inactive."` | Banner alert đỏ `[role='alert']` |
| Tạo thành công | Success Toast & Card | `"School user created. The school user was created successfully."` | Toast xanh lá, Result card `aria-live='polite'` |

---

## 5. JSON Fixtures Data Payload

```json
{
  "single_create_fixtures": {
    "valid_payload_assigned": {
      "nric": "S9123456A",
      "first_name": "Alan",
      "last_name": "Turing",
      "email": "alan.turing.test@IAM.edu.vn",
      "moe_school_code": "RPS-0201"
    },
    "valid_payload_unassigned": {
      "nric": "S9123457B",
      "first_name": "Grace",
      "last_name": "Hopper",
      "email": "grace.hopper.test@IAM.edu.vn",
      "moe_school_code": ""
    },
    "duplicate_conflicts": {
      "existing_nric": "S8407384A",
      "existing_email": "admin@IAM.edu.vn"
    },
    "invalid_school_codes": {
      "too_short": "SC",
      "special_chars": "SCH_#01",
      "non_existent": "INVALID_SCH_999",
      "inactive": "SCH-INACTIVE-999"
    }
  }
}
```
