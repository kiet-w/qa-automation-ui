# Component Spec: Student Citizen Search & Lifecycle Filter (`student_citizen_search_filter`)

## 1. Metadata & Selector
- **Component ID**: `F01-COMP-SEARCH-FILTER`
- **Component Name**: Student Citizen Search & Lifecycle Status Filter
- **Module**: `f01` (Education Account Lifecycle)
- **Target Route**: `/admin/ea-lifecycle` (SCR-ADM-01)
- **Target Role**: `MOE HQ User` (System Administrator / Finance Officer)
- **Element Tag**: `<section role="search" aria-label="EA Lifecycle Filters">`

### Playwright Locators (BSK Live DOM Standard)
```typescript
export const searchFilterLocators = {
  container: 'section[aria-label="EA Lifecycle Filters"]',
  searchInput: 'input[data-testid="ea-search-student-input"]',
  statusDropdown: 'select[data-testid="ea-status-filter-select"]',
  statusDropdownTrigger: 'button[data-testid="ea-status-filter-trigger"]', // If Radix/Shadcn Combobox
  ageMinSelect: 'select[data-testid="ea-age-min-select"]',
  ageMaxSelect: 'select[data-testid="ea-age-max-select"]',
  searchButton: 'button[data-testid="ea-search-submit-btn"]',
  resetButton: 'button[data-testid="ea-search-reset-btn"]',
  errorMessage: 'p[data-testid="ea-search-error-msg"]',
  activeFiltersBadges: 'div[data-testid="active-filter-chips"]',
};
```

---

## 2. BR / AC Traceability
- **Business Rules (BR)**:
  - `F01-BR01`: Only Singapore Citizens (SC) are eligible for Education Accounts.
  - `F01-BR02`: Eligible age is from 7th birthday to before 16th birthday ($7 \le \text{Age} < 16$).
  - `F01-BR03`: Age is derived strictly from Date of Birth (DOB), not schooling status or grade level.
  - `F02-BR01`: Account closes upon reaching 16th birthday.
  - `F02-BR03`: Closure age is computed using current DOB from citizen dataset.
- **Acceptance Criteria (AC)**:
  - `F01-AC01`: Filter displays Active accounts for eligible citizens.
  - `F01-AC03`: Search by PR/Foreigner returns no education account (or shows Profile without EA).
  - `F01-AC04`: Age filter bounds between 7 and 16 years.
  - `F02-AC01`: Viewing account of 15-year-old reflects `Active` status.
  - `F02-AC02`: Filtering for 16-year-old reflects `Closed` status.
- **Architecture Decisions (ADR / Decision Codes)**:
  - `D-20`: Citizen identity (NRIC, Full Name) immutable from Government Citizen Dataset; NRIC masked in search results (`*****123A`).
  - `B2`: Closure boundary at 16th birthday in SGT (UTC+8).
  - `ASM-15`: Search inputs auto-trimmed; whitespace-only queries treated as clear filter.

---

## 3. Ma Trận 12 Lớp Validation (Universal Field-Level Matrix)

| Lớp | Loại Kiểm Thử | Dữ Liệu Input / Thao Tác | Kỳ Vọng Hệ Thống (Expected Behavior) | Mã Lỗi / UI Indicator |
| :--- | :--- | :--- | :--- | :--- |
| **L01** | Empty Required (Search value when submitting search) | Click `Search` khi ô search rỗng, bộ lọc `Status=All` | Hiển thị toàn bộ danh sách tài khoản theo mặc định (không báo lỗi). | Không có lỗi (Default list) |
| **L02** | Empty Optional Filter (Reset state) | Click `Reset` khi đang có text và filter | Xóa sạch text trong search bar, đưa Dropdown về `All`, Age về `7-16`, kích hoạt tải lại danh sách gốc. | Filter pristine state |
| **L03** | All Whitespace (ASM-15) | Nhập toàn dấu cách `"     "` vào ô search | Hệ thống tự động trim về rỗng, coi như tìm kiếm không có từ khóa, không gửi chuỗi whitespace lên backend. | Trimmed clean |
| **L04** | Leading / Trailing Whitespaces | Nhập `"   S1234567A   "` hoặc `"  John Tan  "` | Tự động trim khoảng trắng thừa ở 2 đầu thành `"S1234567A"` và `"John Tan"` trước khi thực hiện query. | Query normalized |
| **L05** | BVA Min Length (NRIC Search) | Nhập chuỗi 8 ký tự `"S1234567"` (thiếu checksum letter) | Báo lỗi định dạng NRIC không hợp lệ nếu người dùng tìm theo định dạng NRIC. | `MSG-0001` / Inline warning |
| **L06** | BVA Max Length (NRIC & Name) | Nhập NRIC 10 ký tự (`S12345678A`) hoặc Name > 100 ký tự | Thuộc tính `maxlength="100"` trên input ngăn nhập ký tự thứ 101; với NRIC format chặn tại ký tự thứ 10. | `maxlength` truncation |
| **L07** | Stress Paste (1000+ chars) | Dán chuỗi 1500 ký tự Lorem Ipsum vào ô Search | Input tự động truncate tại 100 ký tự hoặc từ chối chuỗi quá dài, không gây crash trình duyệt, không giật lag. | Browser stability preserved |
| **L08** | Ký tự cấm & Injection Symbols | Nhập `< > { } ; " ' % _ --` vào Search input | Xử lý an toàn như plain text; `%` và `_` không hoạt động như SQL wildcards; không phá vỡ UI table. | Sanitized plain text |
| **L09** | Unicode / Tiếng Việt / Chữ Trung | Nhập `"Nguyễn Văn A"`, `"陈小明"`, `"Siti Nurhaliza"` | Hỗ trợ tìm kiếm UTF-8 đầy đủ, không gây lỗi serialization JSON hoặc encode URL lỗi. | UTF-8 compliant query |
| **L10** | Security / XSS Vector Injection | Nhập `<script>alert(1)</script>` hoặc `<img src=x onerror=alert('xss')>` | Không thực thi script; mã hóa HTML entities `&lt;script&gt;`; hiển thị thông báo "No accounts found". | Safe HTML Escaped |
| **L11** | i18n & Error Feedback Integrity | Gõ sai định dạng NRIC hoặc tìm kiếm thất bại | Hiển thị câu thông báo lỗi hoàn chỉnh; **CẤM TUYỆT ĐỐI** hiển thị raw translation keys như `features.ea.searchError` hay `*.undefined`. | Exact localized string |
| **L12** | Persistence Integrity | Chọn `Status=Closed - Age 16`, `Age=16`, F5 reload | Bảo toàn trạng thái bộ lọc qua Query Params (`?status=CLOSED_AGE_16&age=16`), khôi phục chính xác UI filter. | URL State Sync preserved |

### Specialized Validation Rules for Input Types:
1. **NRIC Pattern Validation**:
   - Format: `^[STFGstfg]\d{7}[A-Za-z]$` (Singapore NRIC / FIN standard).
   - Case-insensitivity: Nhập `s1234567a` tự động hoa thành `S1234567A`.
2. **Age Range Boundary Rules**:
   - `Age Min`: Giới hạn $7 \le \text{Min} \le 16$.
   - `Age Max`: Giới hạn $7 \le \text{Max} \le 16$.
   - Logical Rule: Nếu `Age Min > Age Max`, hệ thống tự động điều chỉnh hoặc hiển thị cảnh báo đỏ viền `aria-invalid="true"`.
3. **Status Dropdown Enum**:
   - Values: `ALL` (Tất cả), `ACTIVE` (Đang hoạt động), `CLOSED_AGE_16` (Đóng - Tròn 16 tuổi), `CLOSED_NON_CITIZEN` (Đóng - Mất quốc tịch), `CLOSURE_DEFERRED` (Tạm hoãn đóng - Chờ xử lý số dư).

---

## 4. Error Handling & Visual Feedback
- **Field Error State**:
  - CSS Selector: `input[data-testid="ea-search-student-input"][aria-invalid="true"]`.
  - Visual Cue: Viền đỏ `#DC2626` (Red-600), box-shadow phát sáng nhẹ (1px glowing red border).
- **Inline Error Alert**:
  - Selector: `p[data-testid="ea-search-error-msg"][role="alert"]`.
  - Content check: Bắt buộc không chứa regex `(features\..*|validation\..*|.*undefined.*)`.
- **Auto-Dismissal**:
  - Khi người dùng xóa ký tự lỗi hoặc bấm `Reset`, class lỗi và `aria-invalid` biến mất ngay lập tức trong vòng < 50ms.
- **Empty Result State**:
  - Khi tìm NRIC không tồn tại (ví dụ: `T9999999Z`):
  - Hiển thị Empty Illustration kèm thông điệp: *"Không tìm thấy tài khoản EA nào phù hợp với điều kiện tìm kiếm."*

---

## 5. JSON Fixtures Data Payload

```json
{
  "search_filter_fixtures": {
    "valid_nric_searches": [
      { "input": "T0912345A", "expected_count": 1, "description": "Exact 7yo active student" },
      { "input": "t0912345a", "expected_count": 1, "description": "Lowercase NRIC auto-uppercased" },
      { "input": "  T0912345A  ", "expected_count": 1, "description": "Leading and trailing whitespace trimmed" }
    ],
    "valid_name_searches": [
      { "input": "John Tan", "expected_count": 1, "description": "Partial match name query" },
      { "input": "Siti Nur", "expected_count": 1, "description": "Malay name UTF-8" },
      { "input": "陈小明", "expected_count": 1, "description": "Chinese characters UTF-8" }
    ],
    "boundary_age_filters": [
      { "min_age": 7, "max_age": 7, "expected_status": "ACTIVE", "description": "Freshly opened 7yo" },
      { "min_age": 15, "max_age": 15, "expected_status": "ACTIVE", "description": "Final active year 15yo" },
      { "min_age": 16, "max_age": 16, "expected_status": "CLOSED_AGE_16", "description": "Reached 16th birthday" }
    ],
    "invalid_searches": [
      {
        "input": "S12345",
        "expected_error": "Mã NRIC không hợp lệ (cần đúng 9 ký tự).",
        "expected_aria_invalid": true
      },
      {
        "input": "<script>alert(1)</script>",
        "expected_result": "EMPTY_STATE",
        "expected_sanitized_text": "<script>alert(1)</script>"
      }
    ],
    "state_persistence_url": {
      "initial": "/admin/ea-lifecycle",
      "filtered": "/admin/ea-lifecycle?query=T0912345A&status=ACTIVE&min_age=7&max_age=16"
    }
  }
}
```
