# Component Spec: Individual Top-Up EA Lookup (`ea_search_lookup`)

## 1. Metadata & Selector
- **Component ID**: `F02-COMP-EA-SEARCH`
- **Component Name**: Individual Top-Up: Find Education Account (`SCR-01`)
- **Module**: `f02` (Top-Up Management)
- **Target Route**: `/admin/top-up/individual` (Tab 1: SCR-01)
- **Target Role**: `MOE HQ User` (Role check enforced via `BR-F2-01`; School Admin and Parents receive 403 Forbidden with `MSG-0003`)
- **Element Tag**: `<form role="search" aria-label="Find Education Account for Top-Up">`

### Playwright Locators (BSK Live DOM Standard)
```typescript
export const eaSearchLocators = {
  container: 'form[aria-label="Find Education Account for Top-Up"]',
  searchByRadioGroup: 'div[data-testid="topup-search-by-group"]',
  searchByAccountNumberRadio: 'input[data-testid="radio-search-account-number"]',
  searchByNricRadio: 'input[data-testid="radio-search-nric"]',
  searchInput: 'input[data-testid="topup-search-input"]',
  searchButton: 'button[data-testid="topup-search-submit-btn"]',
  loadingSpinner: 'div[data-testid="topup-search-spinner"]',
  errorMessage: 'div[data-testid="topup-search-error-msg"][role="alert"]',
  emptyResultBanner: 'div[data-testid="topup-no-account-found"]',
};
```

---

## 2. BR / AC Traceability
- **Business Rules (BR)**:
  - `BR-F2-01`: Only MOE HQ users perform top-ups; API validates permissions server-side.
  - `BR-F2-02`: Search matches an exact full Account Number or a full student NRIC (9 characters) only.
    - Partial, extra, or wrong input returns nothing and triggers `MSG-0201`.
    - No autocomplete suggestions, no fuzzy matching, at most one EA per search.
    - Displayed NRIC is masked (`T****345A`).
- **Acceptance Criteria (AC)**:
  - `SCR-01 AC01`: Selecting `Account Number` and entering exact valid EA number navigates to `SCR-02`.
  - `SCR-01 AC02`: Selecting `NRIC` and entering exact valid 9-char NRIC navigates to `SCR-02`.
  - `SCR-01 AC03`: Partial search (e.g. 5 digits) or non-existent EA shows `MSG-0201` and remains on `SCR-01`.
- **System Messages**:
  - `MSG-0201`: *"No Education Account found. Check the Account Number or NRIC and try again."*
  - `MSG-0001`: *"Enter your <field>"* (when input is left blank upon submission).
  - `MSG-0003`: *"You do not have permission to perform this action."*

---

## 3. Ma Trận 12 Lớp Validation (Universal Field-Level Matrix)

| Lớp | Loại Kiểm Thử | Dữ Liệu Input / Thao Tác | Kỳ Vọng Hệ Thống (Expected Behavior) | Mã Lỗi / UI Indicator |
| :--- | :--- | :--- | :--- | :--- |
| **L01** | Empty Required Field | Để trống ô search và bấm `Search` | Báo lỗi bắt buộc; ô nhập viền đỏ `aria-invalid="true"`. | `MSG-0001` ("Enter your Account Number or NRIC") |
| **L02** | Radio Toggle Pristine State | Chuyển đổi giữa `Account Number` và `NRIC` | Xóa sạch text trong ô input, reset trạng thái lỗi, đổi placeholder tương ứng. | Input cleared & pristine |
| **L03** | All Whitespace (ASM-15) | Nhập toàn dấu cách `"         "` và bấm `Search` | Hệ thống tự động trim về rỗng, kích hoạt thông báo rỗng bắt buộc `MSG-0001`. | `MSG-0001` / `aria-invalid` |
| **L04** | Leading / Trailing Whitespaces | Nhập `"  EA-2026-00001  "` hoặc `"  T0912345A  "` | Tự động trim khoảng trắng ở 2 đầu trước khi gửi query; tìm thấy tài khoản chính xác. | Auto-trimmed success |
| **L05** | BVA Min Length (NRIC Mode) | Nhập 8 ký tự `"T0912345"` (thiếu chữ cái cuối) | Không tìm kiếm fuzzy, không gợi ý; báo `MSG-0201` trên UI. | `MSG-0201` |
| **L06** | BVA Max Length (NRIC Mode) | Nhập 10 ký tự `"T09123456A"` | Thuộc tính `maxlength="9"` chặn ký tự thứ 10; hoặc nếu dán vào sẽ báo `MSG-0201`. | Maxlength truncation / `MSG-0201` |
| **L07** | Stress Paste (1000+ chars) | Dán chuỗi 1000 ký tự vào ô Search | Thuộc tính input cắt ngắn an toàn tại giới hạn (maxlength 50 đối với EA number, 9 đối với NRIC); trình duyệt không crash. | Buffer-safe paste |
| **L08** | Ký tự cấm & Injection Symbols | Nhập `' OR 1=1 --`, `< > { } ;` | Xử lý an toàn dưới dạng chuỗi thuần; tham số hóa truy vấn an toàn; trả về không tìm thấy. | `MSG-0201` |
| **L09** | Lowercase NRIC Normalization | Nhập `t0912345a` (chữ thường) | Tự động chuẩn hóa thành chữ hoa `T0912345A` trước khi truy vấn API. | Auto-uppercase NRIC |
| **L10** | Security / XSS Vector Injection | Bơm `<script>alert(1)</script>` | Không thực thi script; sanitize an toàn; hiển thị `MSG-0201`. | Escaped & Safe |
| **L11** | i18n & Error Feedback Integrity | Kiểm tra khi tìm không ra bản ghi | Hiển thị chính xác câu từ của `MSG-0201`; **CẤM TUYỆT ĐỐI** lộ key như `features.topup.noAccountFound`. | Exact `MSG-0201` text |
| **L12** | Non-Existent Account Query | Nhập NRIC hoặc EA hợp lệ cú pháp nhưng không tồn tại | Trả về `MSG-0201`, giữ nguyên người dùng tại `SCR-01`, không điều hướng sang `SCR-02`. | `MSG-0201` on SCR-01 |

---

## 4. Error Handling & Visual Feedback
- **Field Error Cue**:
  - `input[data-testid="topup-search-input"][aria-invalid="true"]` với viền đỏ `#DC2626`.
- **Alert Container**:
  - `div[data-testid="topup-search-error-msg"][role="alert"]`:
  - Text: *"No Education Account found. Check the Account Number or NRIC and try again."*
- **Auto-Dismissal**:
  - Ngay khi người dùng bắt đầu gõ ký tự mới vào ô search, thông báo lỗi `MSG-0201` và cờ `aria-invalid` biến mất ngay lập tức.
- **Search Button Debounce**:
  - Nút `Search` bị disable trong khi API đang gọi (Loading state: spinner hiển thị, text "Searching...").

---

## 5. JSON Fixtures Data Payload

```json
{
  "ea_search_lookup_fixtures": {
    "valid_account_number_query": {
      "search_by": "ACCOUNT_NUMBER",
      "search_value": "EA-2026-00001",
      "expected_redirect": "/admin/top-up/individual/verify",
      "mock_response": {
        "account_number": "EA-2026-00001",
        "student_name": "John Tan",
        "nric_masked": "T*****345A",
        "age": 7,
        "status": "ACTIVE",
        "current_balance": 0.00
      }
    },
    "valid_nric_query": {
      "search_by": "NRIC",
      "search_value": "T0912345A",
      "expected_redirect": "/admin/top-up/individual/verify",
      "mock_response": {
        "account_number": "EA-2026-00001",
        "student_name": "John Tan",
        "nric_masked": "T*****345A",
        "age": 7,
        "status": "ACTIVE",
        "current_balance": 0.00
      }
    },
    "not_found_queries": [
      {
        "search_by": "ACCOUNT_NUMBER",
        "search_value": "EA-9999-99999",
        "expected_message_code": "MSG-0201",
        "expected_message_text": "No Education Account found. Check the Account Number or NRIC and try again."
      },
      {
        "search_by": "NRIC",
        "search_value": "T9999999Z",
        "expected_message_code": "MSG-0201",
        "expected_message_text": "No Education Account found. Check the Account Number or NRIC and try again."
      }
    ]
  }
}
```
