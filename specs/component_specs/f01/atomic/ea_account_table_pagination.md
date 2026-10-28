# Component Spec: EA Account Table & Pagination (`ea_account_table_pagination`)

## 1. Metadata & Selector
- **Component ID**: `F01-COMP-TABLE-PAGINATION`
- **Component Name**: Education Account Master Table & Server-Side Pagination
- **Module**: `f01` (Education Account Lifecycle)
- **Target Route**: `/admin/ea-lifecycle` (SCR-ADM-01)
- **Target Role**: `MOE HQ User`
- **Element Tag**: `<table role="table" aria-label="Education Accounts List">`

### Playwright Locators (BSK Live DOM Standard)
```typescript
export const eaTableLocators = {
  tableContainer: 'div[data-testid="ea-table-container"]',
  table: 'table[aria-label="Education Accounts List"]',
  tableHeader: 'thead tr',
  tableRows: 'tbody tr[data-testid="ea-table-row"]',
  headerSortButtons: {
    accountNumber: 'th[data-testid="th-ea-number"] button',
    studentName: 'th[data-testid="th-student-name"] button',
    age: 'th[data-testid="th-age"] button',
    balance: 'th[data-testid="th-balance"] button',
    status: 'th[data-testid="th-status"] button',
    createdDate: 'th[data-testid="th-created-date"] button',
  },
  cells: {
    stt: 'td[data-testid="cell-stt"]',
    eaNumber: 'td[data-testid="cell-ea-number"]',
    studentNricMasked: 'td[data-testid="cell-nric-masked"]',
    studentName: 'td[data-testid="cell-student-name"]',
    age: 'td[data-testid="cell-age"]',
    balance: 'td[data-testid="cell-balance"]',
    statusBadge: 'td[data-testid="cell-status"] span[data-testid="status-badge"]',
    actionButton: 'td[data-testid="cell-actions"] button[data-testid="btn-view-ea-detail"]',
  },
  pagination: {
    container: 'nav[data-testid="ea-pagination"]',
    pageSizeSelect: 'select[data-testid="ea-page-size-select"]',
    currentPageDisplay: 'span[data-testid="ea-current-page-text"]',
    prevPageBtn: 'button[data-testid="ea-prev-page-btn"]',
    nextPageBtn: 'button[data-testid="ea-next-page-btn"]',
    firstPageBtn: 'button[data-testid="ea-first-page-btn"]',
    lastPageBtn: 'button[data-testid="ea-last-page-btn"]',
    pageNumberBtn: (num: number) => `button[data-testid="ea-page-btn-${num}"]`,
  },
  emptyState: 'div[data-testid="ea-empty-state"]',
  loadingSkeleton: 'div[data-testid="ea-table-skeleton"]',
};
```

---

## 2. BR / AC Traceability
- **Business Rules (BR)**:
  - `F01-BR01`: Display accounts only for Singapore Citizens.
  - `F01-BR02`: Account creation at age 7, balance starts at `SGD 0.00`.
  - `F02-BR01`: Account status transforms to `Closed` when holder reaches 16.
  - `F02-BR08`: Closed accounts and full transaction history must remain accessible for lookup and audit (read-only, no deletion).
  - `2.2`: Education Account Number is unique and follows format `EA-YYYY-NNNNN`.
  - `2.3`: Balance is formatted in `SGD` with exactly two decimals (`$X,XXX.XX SGD`), never negative.
- **Acceptance Criteria (AC)**:
  - `F01-AC01`: Newly synced account shows status `Active` and balance `$0.00 SGD`.
  - `F01-AC06`: One citizen holds at most one account; no duplicate rows for the same NRIC.
  - `F02-AC01`: Account of student aged 7-15 displayed with badge `Active`.
  - `F02-AC02`: Account of student turned 16 displayed with badge `Closed - 16y`.
  - `F02-AC06`: Accessing closed account does not alter closure date or duplicate close action.
- **Architecture Decisions (ADR / Decision Codes)**:
  - `D-20`: NRIC masking in UI table (`T****345A` or `*****345A`).
  - `Contract Check 1`: Money precision exact to two decimal places (Decimal 18,2).
  - `B10`: Actual closure date recorded, scheduled closure date is not stored.

---

## 3. Ma Trận 12 Lớp Validation (Universal Table & Pagination Matrix)

| Lớp | Loại Kiểm Thử | Dữ Liệu Input / Thao Tác | Kỳ Vọng Hệ Thống (Expected Behavior) | Mã Lỗi / UI Indicator |
| :--- | :--- | :--- | :--- | :--- |
| **L01** | Empty Table (Zero records) | Filter query không khớp bất kỳ bản ghi nào | Ẩn toàn bộ `tbody`, hiển thị Empty State Illustration; phân trang ẩn hoặc disable; text *"Không tìm thấy tài khoản EA nào phù hợp."* | Empty container visible |
| **L02** | Default View (Pristine load) | Truy cập trang lần đầu tiên | Tải 10 dòng đầu tiên (Page 1), sắp xếp `Created Date` giảm dần hoặc `Account Number` tăng dần; pagination hiển thị `1 to 10 of 342,150`. | Full data table loaded |
| **L03** | Currency Formatting (SGD) | Render cột Balance với các giá trị: `0`, `15.5`, `1200.75` | Format chính xác 2 chữ số thập phân: `$0.00 SGD`, `$15.50 SGD`, `$1,200.75 SGD`; có dấu phân cách hàng nghìn. | Strict Currency Check |
| **L04** | Status Badge Color Coding | Cột Status với các giá trị: `Active`, `Closed - 16y`, `Closed - Citizenship`, `Closure Deferred` | Badge hiển thị đúng CSS: `Active` (Green-100/Green-800), `Closed - 16y` (Gray-100/Gray-800), `Closed - Non-Citizen` (Red-100/Red-800), `Closure Deferred` (Amber-100/Amber-800). | Correct Tailwind / CSS badge |
| **L05** | BVA Pagination Min Boundary | Đang ở Page 1 -> Kiểm tra nút `Previous` và `First` | Nút `Previous` và `First Page` có thuộc tính `disabled="true"`, cursor `not-allowed`. | Disabled boundary buttons |
| **L06** | BVA Pagination Max Boundary | Đang ở trang cuối cùng (Page N) -> Kiểm tra nút `Next` và `Last` | Nút `Next` và `Last Page` có thuộc tính `disabled="true"`, cursor `not-allowed`. | Disabled boundary buttons |
| **L07** | Page Size Changing (Stress/Density) | Thay đổi Dropdown page size từ `10` -> `25` -> `50` bản ghi/trang | Bảng tự động tải lại đúng số dòng tương ứng; tính toán lại tổng số trang; giữ nguyên trang 1. | Re-rendered table size |
| **L08** | Column Sorting Toggle | Click header `Số dư` lần 1 (Ascending), lần 2 (Descending) | Lần 1: Icon mũi tên hướng lên, số dư xếp từ nhỏ nhất đến lớn nhất; Lần 2: Icon mũi tên xuống, số dư xếp từ lớn đến nhỏ; không crash pagination. | Sorting query params sync |
| **L09** | NRIC Masking & PII Protection | Kiểm tra hiển thị cột `NRIC Học sinh` | 100% dòng trong bảng hiển thị NRIC dạng masked: `T*****345A` (giữ ký tự đầu và 4 ký tự cuối); không render raw NRIC trong DOM attributes (`data-nric`). | PII Compliant Masking |
| **L10** | XSS in Student Name & Sanitization | Học sinh có tên chứa XSS: `<script>alert('hack')</script>` | Trình duyệt hiển thị nguyên văn dạng string text, không execute script, text sanitized an toàn. | Encoded cell text |
| **L11** | i18n & Translation Integrity | Kiểm tra toàn bộ Header, Cột, Badge và Pagination footer | Không chứa raw keys như `ea.table.headers.*`, `common.pagination.total`, `status.active.label`. Toàn bộ hiển thị ngôn ngữ chuẩn. | No raw i18n leaks |
| **L12** | Deep Linking & Navigation Persistence | Truy cập trực tiếp URL: `/admin/ea-lifecycle?page=3&size=25&sort=balance_desc` | Bảng tự động nhảy tới Page 3, hiển thị 25 dòng, áp dụng sort Balance descending; nút bấm Page 3 active. | URL Deep Link State |

---

## 4. Error Handling & Visual Feedback
- **Network / API Timeout State**:
  - Khi API tải bảng tài khoản gặp lỗi 500 hoặc Gateway Timeout (504):
  - Ẩn skeleton, hiển thị Error Banner: *"Không thể tải danh sách tài khoản. Vui lòng kiểm tra kết nối và thử lại."* kèm nút `[Thử lại]`.
- **Loading Skeleton**:
  - Trong quá trình gọi API (debounce hoặc chuyển trang):
  - Hiển thị Skeleton animation với 10 dòng xám phát sáng mờ (`animate-pulse`). Cấm để bảng giật layout (CLS = 0).
- **Row Click / Action Trigger**:
  - Click nút `[Chi tiết]` tại cột Thao tác:
  - Bật cờ `aria-expanded="true"`, mở Drawer `EA Lifecycle Event Log` (Component `ea_lifecycle_drawer`) tương ứng với `ea_number` của dòng đó.

---

## 5. JSON Fixtures Data Payload

```json
{
  "ea_table_fixtures": {
    "sample_page_response": {
      "page_index": 1,
      "page_size": 10,
      "total_records": 342150,
      "total_pages": 34215,
      "items": [
        {
          "stt": 1,
          "account_number": "EA-2026-00001",
          "student_nric_masked": "T*****345A",
          "student_name": "John Tan",
          "age": 7,
          "balance": 0.00,
          "balance_formatted": "$0.00 SGD",
          "status": "ACTIVE",
          "status_badge_class": "badge-success",
          "created_at": "2026-01-02T00:00:00+08:00"
        },
        {
          "stt": 2,
          "account_number": "EA-2018-09920",
          "student_nric_masked": "T*****765B",
          "student_name": "Siti Nurhaliza",
          "age": 16,
          "balance": 15.50,
          "balance_formatted": "$15.50 SGD",
          "status": "CLOSED_AGE_16",
          "status_badge_class": "badge-secondary",
          "created_at": "2018-03-12T00:00:00+08:00"
        },
        {
          "stt": 3,
          "account_number": "EA-2020-04512",
          "student_nric_masked": "T*****112C",
          "student_name": "Chen Wei Ling",
          "age": 12,
          "balance": 200.00,
          "balance_formatted": "$200.00 SGD",
          "status": "ACTIVE",
          "status_badge_class": "badge-success",
          "created_at": "2020-05-18T00:00:00+08:00"
        },
        {
          "stt": 4,
          "account_number": "EA-2019-01299",
          "student_nric_masked": "T*****901D",
          "student_name": "Arun Kumar",
          "age": 13,
          "balance": 50.00,
          "balance_formatted": "$50.00 SGD",
          "status": "CLOSED_NON_CITIZEN",
          "status_badge_class": "badge-destructive",
          "created_at": "2019-02-14T00:00:00+08:00"
        },
        {
          "stt": 5,
          "account_number": "EA-2017-00341",
          "student_nric_masked": "T*****882E",
          "student_name": "Grace Lee",
          "age": 16,
          "balance": 120.00,
          "balance_formatted": "$120.00 SGD",
          "status": "CLOSURE_DEFERRED",
          "status_badge_class": "badge-warning",
          "created_at": "2017-08-20T00:00:00+08:00"
        }
      ]
    },
    "empty_page_response": {
      "page_index": 1,
      "page_size": 10,
      "total_records": 0,
      "total_pages": 0,
      "items": []
    }
  }
}
```
