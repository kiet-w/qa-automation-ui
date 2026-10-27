# Component Specification: School User Search & Data Table (School User Management)

## 1. Metadata & Selector

| Attribute | Specification |
| :--- | :--- |
| **Component Name** | `SchoolUserSearchAndTableComponent` |
| **Target Page / Route** | `/school-user-management` (`SchoolUserManagementPage`) |
| **Element Hierarchy** | Page header `<header>`, Search input `<input>`, Action button `<button>`, Data table `<table>`, Pagination `<nav>` |
| **Visual State** | Màn hình danh sách người dùng trường học (EduFAMS Admin Portal) |
| **Component Scope** | Hiển thị danh sách tài khoản nhân viên trường, tìm kiếm thời gian thực, phân trang và trạng thái chưa phân trường |

### Playwright Live DOM Locators
```python
# Extracted from pages/fs03/school_user_management_page.py
PAGE_HEADING = "h1:has-text('School user management')"
PAGE_SUBTITLE = "text=Manage users assigned to schools."
CREATE_USER_BTN = "button:has-text('Create School User')"
SEARCH_INPUT = "input[type='search'], input[placeholder*='Search']"
TABLE = "table"
TABLE_HEADERS = "table thead th"
TABLE_ROWS = "table tbody tr"
UNASSIGNED_BADGE = "text='Unassigned in any school', span:has-text('Unassigned')"
PAGINATION = "nav[aria-label*='pagination' i], [class*='pagination']"
EMPTY_STATE_NOTICE = "text='No school users found'"
EMPTY_STATE_HINT = "text='Try changing the search.'"
LOAD_ERROR_HEADING = "text='Unable to load school users'"
RETRY_BTN = "button:has-text('Retry')"
```

---

## 2. Business Rules & Acceptance Criteria Traceability

| ID | Type | Description | Source Reference |
| :--- | :--- | :--- | :--- |
| **R3-F02** | Functional Req | School User Provisioning: MOE Admin views, searches, and manages School Users. School Users must have an assignment to an Active School. | `specs/md/FS document/FS-03_School_Student_Fee_Management.md` |
| **BR-03-01** | Business Rule | Access Boundary: A School User can access only data belonging to their assigned Active School. If unassigned, user cannot manage student fees. | `specs/validation_rules/md/R3_Validation_Rules.md` |
| **AC-01** | Acceptance Criteria | School User List: Display Code, Username, Full Name, School, and Actions. If no school assigned, display `"Unassigned in any school"`. | `specs/validation_rules/md/R3_Validation_Rules.md` |
| **AC-02** | Acceptance Criteria | Search filtering: Search by Code, Username, Full name, or School. Reset pagination to page 1 on search change. | `specs/validation_rules/md/R3_Validation_Rules.md` |
| **AC-05** | Acceptance Criteria | Pagination & Empty state: Default page size is 10 (options: 5, 10, 25). If 0 results, show `"No school users found"`. | `specs/validation_rules/md/R3_Validation_Rules.md` |

---

## 3. Ma trận 12 lớp Validation & UI Integrity

| Lớp (Layer) | Phân Loại Kiểm Thử | Dữ Liệu Đầu Vào (Input Vector) | Trạng Thái / Hành Vi UI Kỳ Vọng | Tiêu Chí Đạt (Pass Criteria) |
| :--- | :--- | :--- | :--- | :--- |
| **1. Default List Display** | Tải danh sách mặc định | Mở `/school-user-management` | Bảng hiển thị tối đa 10 dòng đầu tiên; đủ các cột: Code, Username, Full Name, School, Actions. | Số dòng $\le 10$, có phân trang. |
| **2. Search by Full Name** | Tìm kiếm theo họ tên | Nhập `"Bui Thi H"` vào ô search | Bảng tự động lọc hiển thị các tài khoản có tên chứa `"Bui Thi H"`. | Hàng hiển thị khớp từ khóa. |
| **3. Search by Username** | Tìm theo tài khoản | Nhập `"staff1"` | Bảng lọc đúng dòng có Username `"staff1"`. | Khớp chính xác username. |
| **4. Search by School Code** | Tìm theo trường | Nhập `"RPS-0201"` | Bảng lọc tất cả người dùng thuộc trường Rosyth Primary School. | Cột School hiển thị mã/tên trường. |
| **5. Unassigned School Badge**| Trạng thái chưa gán trường | Tài khoản mới tạo chưa gán trường | Cột School hiển thị nhãn nổi bật: `"Unassigned in any school"` (hoặc badge màu xám/vàng). | Nhãn Unassigned hiển thị đúng. |
| **6. Empty Search Result** | Tìm kiếm không có kết quả | Nhập chuỗi ngẫu nhiên `"NON_EXISTENT_XYZ_999"` | Bảng hiển thị thông báo: `"No school users found"` kèm gợi ý `"Try changing the search."`. | Thấy dòng empty state. |
| **7. Whitespace Search Trim** | Khoảng trắng trong ô tìm kiếm | Nhập `"   staff1   "` | Tự động trim khoảng trắng và lọc ra user `"staff1"`. | Tìm kiếm chính xác không lỗi. |
| **8. Search Resets Pagination** | Reset trang khi tìm kiếm | Đang ở trang 3 -> Gõ từ khóa tìm kiếm | Hệ thống tự động chuyển trang hiện tại về Trang 1 (`page = 1`). | Phân trang hiển thị Page 1. |
| **9. Page Size Switch** | Đổi số dòng hiển thị | Chọn page size 5 vs 10 vs 25 | Bảng cập nhật hiển thị đúng số dòng tối đa đã chọn (5 dòng, 10 dòng, 25 dòng). | Số dòng tbody khớp page size. |
| **10. SQLi / Script in Search** | Bảo mật ô tìm kiếm | Nhập `' OR '1'='1`, `<script>alert(1)</script>` | Hệ thống mã hóa an toàn, coi như chuỗi text tìm kiếm thông thường; không crash SQL. | Trả về empty state an toàn. |
| **11. Load Error Fallback** | Xử lý lỗi API máy chủ | API danh sách user trả về 500 | Hiển thị alert: `"Unable to load school users."` kèm nút `"Retry"`. | Nút Retry khả dụng. |
| **12. Create Button Navigation** | Điều hướng tạo người dùng | Click nút `"Create School User"` | Điều hướng sang URL `/school-user-management/new`. | URL chuyển sang `/new`. |

---

## 4. Error Handling & Visual Feedback

| Tình Huống Kích Hoạt | Tiêu Đề / Mã Lỗi | Nội Dung Thông Báo | Hành Động Khả Dụng |
| :--- | :--- | :--- | :--- |
| Không tìm thấy người dùng khớp từ khóa | Thông báo trạng thái rỗng | `"No school users found. Try changing the search."` | Xóa ô tìm kiếm, nhập từ khóa khác |
| Lỗi mạng hoặc máy chủ không tải được danh sách | Lỗi hệ thống 500 | `"Unable to load school users. Please try again."` | Nút `"Retry"` |
| Tài khoản chưa gán trường | Cảnh báo nghiệp vụ | `"Unassigned in any school"` | Hiển thị badge màu trung tính để nhắc nhở Admin gán trường |

---

## 5. JSON Fixtures Data Payload

```json
{
  "school_user_table_fixtures": {
    "existing_users": [
      {
        "code": "USR-0001",
        "username": "staff1",
        "full_name": "Bui Thi H",
        "email": "staff1@IAM.edu.vn",
        "school": "Rosyth Primary School (RPS-0201)",
        "role": "SCHOOL"
      },
      {
        "code": "USR-0002",
        "username": "unassigned_staff",
        "full_name": "Alan Turing",
        "email": "alan.turing@IAM.edu.vn",
        "school": "Unassigned in any school",
        "role": "SCHOOL"
      }
    ],
    "search_queries": {
      "by_username": "staff1",
      "by_name": "Bui Thi",
      "by_school": "RPS-0201",
      "non_existent": "NON_EXISTENT_XYZ_999"
    }
  }
}
```
