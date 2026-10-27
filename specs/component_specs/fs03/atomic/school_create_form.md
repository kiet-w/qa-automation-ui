# Component Specification: School Creation Form (School Management)

## 1. Metadata & Selector

| Attribute | Specification |
| :--- | :--- |
| **Component Name** | `SchoolCreateFormComponent` |
| **Target Page / Route** | `/school-management/new` (`SchoolCreatePage`) |
| **Element Hierarchy** | Form `<form>`, Section headings `<h2>`, Input fields `<input>`, Select dropdown `<select>`, Multi-select chips `<div>`, Action buttons `<button>`, Feedback alerts `<div>` |
| **Visual State** | Màn hình tạo trường học mới trong EduFAMS Admin Portal |
| **Component Scope** | Nhập thông tin trường học: Mã MOE, Tên trường, Loại hình trường, Gán người dùng quản lý, và Chọn các khối lớp học thuật |

### Playwright Live DOM Locators
```python
# Extracted from pages/fs03/school_create_page.py
PAGE_HEADING = "h1, h2:has-text('Create a school')"
MOE_SCHOOL_CODE_INPUT = "#school-moeSchoolCode"
SCHOOL_NAME_INPUT = "#school-name"
SCHOOL_TYPE_SELECT = "#school-schoolType"
SCHOOL_USERS_INPUT = "#school-schoolUsers"
ACADEMIC_LEVELS_INPUT = "#school-academicLevels"

USERS_COUNTER = "#school-schoolUsers-selected"
LEVELS_COUNTER = "#school-academicLevels-selected"

CREATE_SCHOOL_BTN = "button:has-text('Create school')"
CANCEL_BTN = "button:has-text('Cancel')"

SUMMARY_ERROR_BANNER = "div:has-text('Please correct the errors below.')"
MOE_CODE_INLINE_ERROR = "p:has-text('MOE school code is required.')"
NAME_INLINE_ERROR = "p:has-text('School name is required.')"
TYPE_INLINE_ERROR = "p:has-text('Select a school type.')"
LEVELS_INLINE_ERROR = "p:has-text('Select at least one academic level.')"
SUCCESS_TOAST = "div:has-text('School created')"
```

---

## 2. Business Rules & Acceptance Criteria Traceability

| ID | Type | Description | Source Reference |
| :--- | :--- | :--- | :--- |
| **R3-F01** | Functional Req | School Entity Creation: MOE Admin creates an Active School with unique MOE School Code, School Name, School Type, and Academic Levels. | `specs/md/FS document/FS-03_School_Student_Fee_Management.md` |
| **BR-03-05** | Business Rule | MOE School Code Constraint: Must be 3–20 characters, alphanumeric and hyphens only, and unique across all schools. | `specs/validation_rules/md/R3_Validation_Rules.md` |
| **AC-08** | Acceptance Criteria | Mandatory Fields Validation: MOE School code, School name, School type, and at least one Academic Level are mandatory. Summary error banner appears when any are missing. | `specs/validation_rules/md/R3_Validation_Rules.md` |
| **AC-09** | Acceptance Criteria | Duplicate Prevention: Submitting a school code that already exists displays `"A school with MOE code '{code}' already exists."`. | `specs/validation_rules/md/R3_Validation_Rules.md` |

---

## 3. Ma trận 12 lớp Validation & UI Integrity

| Lớp (Layer) | Phân Loại Kiểm Thử | Dữ Liệu Đầu Vào (Input Vector) | Trạng Thái / Hành Vi UI Kỳ Vọng | Tiêu Chí Đạt (Pass Criteria) |
| :--- | :--- | :--- | :--- | :--- |
| **1. Submit All Blank** | Submit form rỗng | Click "Create school" khi chưa nhập gì | Hiển thị Banner tổng quát: `"Please correct the errors below."` và đồng thời 4 lỗi inline bên dưới từng trường. | Banner + 4 inline errors xuất hiện. |
| **2. MOE Code Required** | Để trống mã trường | Bỏ trống `#school-moeSchoolCode` | Báo lỗi inline: `"MOE school code is required."`. | Inline error code hiển thị. |
| **3. MOE Code Length BVA** | Độ dài mã trường (2 vs 3 vs 20 vs 21) | `"SC"` (2 chars) vs `"ABC"` (3 chars) vs 21 chars | 2 ký tự và 21 ký tự bị từ chối: `"MOE school code must be between 3 and 20 characters."`. 3 và 20 ký tự hợp lệ. | BVA 3-20 characters hoạt động. |
| **4. MOE Code Disallowed Chars**| Ký tự cấm trong mã trường | Nhập `"SCH_01"`, `"SCH@01"`, `"SCH 01"` | Bị từ chối: `"MOE school code must contain only alphanumeric characters and hyphens."`. | Chặn ký tự lạ. |
| **5. Duplicate MOE Code** | Trùng mã trường đã có | Nhập mã trường đã có sẵn trong DB (`"RPS-0201"`) | Máy chủ trả về lỗi: `"School with MOE code 'RPS-0201' already exists."`. | Banner lỗi trùng lặp. |
| **6. School Name Required & Max** | Tên trường rỗng & BVA 150/151 | Tên rỗng hoặc 151 ký tự | Rỗng: `"School name is required."`; 151 ký tự: `"School name cannot exceed 150 characters."`. | Validate tên trường. |
| **7. School Type Required** | Chưa chọn loại hình trường | Dropdown ở trạng thái mặc định (chưa chọn) | Báo lỗi inline: `"Select a school type."`. | Inline error type hiển thị. |
| **8. Academic Levels Required** | Chưa chọn khối lớp | Bỏ trống không chọn khối lớp nào | Báo lỗi inline: `"Select at least one academic level."`. | Inline error levels hiển thị. |
| **9. Multi-Select Chips Selection**| Chọn và bỏ chọn khối lớp | Chọn `"Primary 1"`, `"Primary 2"` | Hiển thị 2 chip đã chọn; counter cập nhật `#school-academicLevels-selected` thành `"2 selected"`. Bấm icon `x` xóa bớt 1 chip. | Chip & counter phản hồi đúng. |
| **10. Optional School Users Assignment**| Gán người dùng quản lý | Không chọn School User nào | Form vẫn hợp lệ; tạo trường thành công mà chưa cần gán user ngay. | Gán user là tùy chọn. |
| **11. Cancel Navigation** | Hủy bỏ tạo trường | Click nút `"Cancel"` | Hủy các giá trị đang nhập, điều hướng quay lại trang danh sách `/school-management`. | Quay về danh sách an toàn. |
| **12. Success Notification** | Tạo trường thành công | Nhập đầy đủ thông tin hợp lệ -> Bấm Create | Hiển thị toast thông báo: `"School created"`; form đóng lại hoặc điều hướng về danh sách trường. | Toast xanh lá xuất hiện. |

---

## 4. Error Handling & Visual Feedback

| Vị Trí Lỗi | Tiêu Đề / Mã Lỗi | Nội Dung Thông Báo Chuẩn | Visual Feedback |
| :--- | :--- | :--- | :--- |
| **Form Summary** | Banner tổng | `"Please correct the errors below."` | Alert banner màu đỏ đầu trang form |
| **MOE School Code** | Inline field | `"MOE school code is required."` | Viền đỏ, text đỏ dưới input |
| **MOE School Code** | Length error | `"MOE school code must be between 3 and 20 characters."` | Viền đỏ, text đỏ dưới input |
| **MOE School Code** | Duplicate error | `"School with MOE code '{code}' already exists."` | Banner alert đỏ |
| **School Name** | Inline field | `"School name is required."` | Viền đỏ, text đỏ dưới input |
| **School Type** | Inline dropdown | `"Select a school type."` | Viền đỏ bao quanh dropdown select |
| **Academic Levels** | Inline chips | `"Select at least one academic level."` | Text đỏ cảnh báo dưới container chips |

---

## 5. JSON Fixtures Data Payload

```json
{
  "school_create_fixtures": {
    "valid_payload": {
      "moe_school_code": "NEW-SCH-2026",
      "school_name": "New Horizon Primary School",
      "school_type": "Government",
      "academic_levels": ["Primary 1", "Primary 2", "Primary 3"],
      "school_users": []
    },
    "duplicate_payload": {
      "moe_school_code": "RPS-0201",
      "school_name": "Rosyth Clone School",
      "school_type": "Government",
      "academic_levels": ["Primary 1"]
    },
    "boundary_school_codes": {
      "min_valid_3": "ABC",
      "max_valid_20": "A1234567890123456789",
      "too_short_2": "AB",
      "too_long_21": "A12345678901234567890"
    }
  }
}
```
