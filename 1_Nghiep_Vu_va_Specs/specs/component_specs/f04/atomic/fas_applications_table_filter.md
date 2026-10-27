# Component Spec: FAS Applications List & Filters (`fas_applications_table_filter`)

## 1. Metadata & Selector
- **Component ID**: `F04-COMP-APP-LIST`
- **Component Name**: FAS Applications Master List & Multi-Filter (`Screen A & B`)
- **Module**: `f04` (Assess FAS & Apply Subsidies)
- **Target Route**: `/admin/fas/applications` (Screen A: School Admin view; Screen B: MOE HQ view)
- **Target Roles**:
  - `School Admin`: Sees SBFAS applications of their own school only (`FS 3.1`).
  - `MOE HQ User`: Sees all applications nationally; decides MOEFAS; views SBFAS read-only.
- **Element Tag**: `<section role="region" aria-label="FAS Applications Management">`

### Playwright Locators (BSK Live DOM Standard)
```typescript
export const fasAppListLocators = {
  container: 'section[aria-label="FAS Applications Management"]',
  summaryCards: {
    pendingCard: 'div[data-testid="summary-card-pending"]',
    pendingCount: 'div[data-testid="summary-card-pending"] span[data-testid="card-count"]',
    approvedCard: 'div[data-testid="summary-card-approved"]',
    approvedCount: 'div[data-testid="summary-card-approved"] span[data-testid="card-count"]',
    rejectedCard: 'div[data-testid="summary-card-rejected"]',
    rejectedCount: 'div[data-testid="summary-card-rejected"] span[data-testid="card-count"]',
  },
  statusTabs: {
    container: 'div[role="tablist"][data-testid="fas-status-tabs"]',
    pendingTab: 'button[role="tab"][data-testid="tab-pending"]',
    allTab: 'button[role="tab"][data-testid="tab-all"]',
    approvedTab: 'button[role="tab"][data-testid="tab-approved"]',
    rejectedTab: 'button[role="tab"][data-testid="tab-rejected"]',
  },
  filters: {
    searchBox: 'input[data-testid="fas-search-input"]',
    levelSelect: 'select[data-testid="fas-filter-level"]',
    classSelect: 'select[data-testid="fas-filter-class"]',
    sourceSelect: 'select[data-testid="fas-filter-source"]',
    tierSelect: 'select[data-testid="fas-filter-tier"]',
    statusSelect: 'select[data-testid="fas-filter-status"]',
    mlRiskSelect: 'select[data-testid="fas-filter-ml-risk"]',
    submittedSelect: 'select[data-testid="fas-filter-submitted"]',
    exportCsvBtn: 'button[data-testid="fas-btn-export-csv"]',
  },
  table: {
    container: 'table[aria-label="FAS Applications Register"]',
    rows: 'tbody tr[data-testid="fas-app-row"]',
    cellAppId: 'td[data-testid="cell-app-id"]',
    cellStudent: 'td[data-testid="cell-student"]',
    cellClass: 'td[data-testid="cell-class"]',
    cellSource: 'td[data-testid="cell-source"]',
    cellSubmitted: 'td[data-testid="cell-submitted"]',
    cellMlSuggestion: 'td[data-testid="cell-ml-suggestion"]',
    cellMlRiskBadge: 'td[data-testid="cell-ml-risk"] span[data-testid="risk-badge"]',
    cellTier: 'td[data-testid="cell-tier"]',
    cellStatusBadge: 'td[data-testid="cell-status"] span[data-testid="app-status-badge"]',
    cellActionBtn: 'td[data-testid="cell-action"] button[data-testid="btn-review-app"]',
  },
  pagination: {
    footer: 'div[data-testid="fas-table-pagination"]',
    showingText: 'span[data-testid="fas-pagination-info"]',
    prevBtn: 'button[data-testid="fas-prev-btn"]',
    nextBtn: 'button[data-testid="fas-next-btn"]',
  },
  emptyState: 'div[data-testid="fas-empty-state"]',
};
```

---

## 2. BR / AC Traceability
- **Business Rules (BR)**:
  - `BR13`: Applications table columns: Application ID, Student (Name + NRIC/FIN), School/Class, Scheme, Source, Submitted Date, ML Suggestion, ML Risk, Tier, Status.
  - `BR14`: Role segregation: School Admin views/decides only SBFAS of their own school. Accessing another school's application returns: *"You do not have access to this application."*
  - `BR16`: Sorting default is `Submitted Date DESC` (newest first), 10 rows per page.
  - `FS 3.1 & 3.3`: Summary cards are not affected by search/filters; refresh immediately after any approval or rejection.
  - `FS 3.5`: Search box matches Student Name, NRIC/FIN, or Application ID (case-insensitive substring).
- **Acceptance Criteria (AC)**:
  - `T24`: Status tabs filter rows by Pending, All, Approved, Rejected with real-time count badges.
  - `T26`: Search input trims whitespace; supports alphanumeric substrings.
  - `T27`: Searching non-existent keyword displays empty message *"No applications found."*
  - `T29`: Export CSV respects currently active status tab, filters, and search query.
  - `T32`: Permanent Resident (PR) and Citizen students correctly display their NRIC/FIN masked.

---

## 3. Ma Trận 12 Lớp Validation (Universal Field & Table Matrix)

| Lớp | Loại Kiểm Thử | Dữ Liệu Input / Thao Tác | Kỳ Vọng Hệ Thống (Expected Behavior) | Mã Lỗi / UI Indicator |
| :--- | :--- | :--- | :--- | :--- |
| **L01** | Empty Table Search | Tìm từ khóa không tồn tại `"ZZZZ999"` | Bảng trống; footer ẩn; hiển thị thông điệp *"No applications found."*. | `No applications found.` |
| **L02** | Default View (Pristine) | Mở trang lần đầu | Mặc định mở Tab `Pending`; hiển thị 10 hồ sơ mới nộp nhất; summary cards hiển thị đúng số đếm thực tế. | Tab Pending active |
| **L03** | Search Input Whitespace (ASM-15) | Nhập toàn dấu cách `"      "` vào ô tìm kiếm | Tự động trim về rỗng, coi như không tìm kiếm, không làm mất kết quả lọc. | Clean trim |
| **L04** | Search BVA Max Length (100, 101) | Nhập chuỗi 100 ký tự vs 101 ký tự | Chuỗi 100 ký tự hợp lệ; ký tự thứ 101 bị cắt ngắn với helper text: *"Search is limited to 100 characters."* | Maxlength 100 limit |
| **L05** | Special Characters in Search | Nhập `' " % _ \ ; -- * ? ( ) [ ]` | Ký tự `%` và `_` không hoạt động như SQL wildcards; xử lý an toàn dạng plain text. | Plain text parameter |
| **L06** | SQL Injection in Search | Nhập `' OR 1=1 --` | Không gây lỗi cú pháp SQL, không rò rỉ dữ liệu ngoài trường; trả về *"No applications found."* | Parameterized query |
| **L07** | XSS Script Vector in Search | Bơm `<script>alert(1)</script>` | Không execute script, HTML entities được escape an toàn trên input và kết quả. | Escaped HTML |
| **L08** | Inter-Filter Dependency (Level $\rightarrow$ Class) | Chọn `Level = Primary 3` | Dropdown Class tự động giới hạn chỉ hiển thị các lớp thuộc Khối 3 (`3A`, `3B`, `3C`); chọn Level khác reset Class về `All`. | Dynamic cascade filter |
| **L09** | ML Risk Badge CSS & Labels | Render các mức rủi ro: `Low`, `Medium`, `High` | `Low` (Xanh lá `Need Score < 50`), `Medium` (Vàng cam `50 - 74.99`), `High` (Đỏ `#DC2626` `Need Score >= 75`). | Dynamic Risk Badges |
| **L10** | PII Masking Compliance | Hiển thị NRIC/FIN trong bảng | Luôn hiển thị dạng `T****177H`; không để lộ số CCCD/NRIC trần. | Masked NRIC |
| **L11** | i18n & Empty Copy Integrity | Kiểm tra bảng rỗng, tab counts, export | Không chứa raw keys như `fas.applications.empty`, `risk.high.label`. | Exact English copy |
| **L12** | CSV Export Content Integrity | Click `Export` khi đang lọc `ML Risk = High` | Xuất file `fas-applications_YYYYMMDD.csv` chỉ chứa các đơn có rủi ro cao; header chuẩn; định dạng ngày `DD/MM/YYYY`. | Filter-scoped CSV |

---

## 4. Error Handling & Visual Feedback
- **Cross-School Unauthorized Error**:
  - Khi School Admin mở URL của đơn thuộc trường khác:
  - Hiển thị Toast lỗi đỏ: *"You do not have access to this application."* và giữ nguyên ở màn hình danh sách.
- **Concurrent Decision Warning**:
  - Nếu đơn đã được duyệt bởi đồng nghiệp khác trong khi danh sách đang mở:
  - Click `[Review]` sẽ mở drawer ở chế độ Read-Only với banner:
    *"This application was already decided by {user} on {DD/MM/YYYY}."*

---

## 5. JSON Fixtures Data Payload

```json
{
  "fas_applications_fixtures": {
    "summary_metrics": {
      "pending_count": 3,
      "approved_this_year": 34,
      "rejected_this_year": 9
    },
    "sample_applications": [
      {
        "application_id": "APP-2026-00412",
        "student_name": "Aisha Binte Roslan",
        "student_nric_masked": "T*****177H",
        "school_code": "SCH-101",
        "class_name": "Primary 3A",
        "scheme": "SBFAS",
        "source": "ONLINE",
        "submitted_date": "2026-10-15T09:30:00+08:00",
        "ml_suggestion": "Tier 1 · High need",
        "ml_need_score": 78.50,
        "ml_risk_level": "HIGH",
        "tier_granted": null,
        "status": "PENDING"
      },
      {
        "application_id": "APP-2026-00398",
        "student_name": "Tan Wei Ming",
        "student_nric_masked": "T*****889A",
        "school_code": "SCH-101",
        "class_name": "Primary 5C",
        "scheme": "SBFAS",
        "source": "PAPER",
        "submitted_date": "2026-10-10T14:20:00+08:00",
        "ml_suggestion": "Tier 2 · Medium need",
        "ml_need_score": 62.00,
        "ml_risk_level": "MEDIUM",
        "tier_granted": "Tier 2",
        "status": "APPROVED"
      }
    ]
  }
}
```
