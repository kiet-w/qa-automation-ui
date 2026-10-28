# Component Spec: Top-Up History & Spending Summary (`topup_history_table`)

## 1. Metadata & Selector
- **Component ID**: `F02-COMP-HISTORY-TABLE`
- **Component Name**: Top-Up History & Spending Summary Table (`SCR-05`)
- **Module**: `f02` (Top-Up Management)
- **Target Route**: `/admin/top-up/history` (Tab 3: SCR-05)
- **Target Role**: `MOE HQ User`
- **Element Tag**: `<section role="region" aria-label="Top-Up History and Summary">`

### Playwright Locators (BSK Live DOM Standard)
```typescript
export const topupHistoryLocators = {
  container: 'section[aria-label="Top-Up History and Summary"]',
  summaryBanner: {
    container: 'div[data-testid="topup-summary-banner"]',
    totalSpending: 'span[data-testid="summary-total-spending"]',
    successfulCount: 'span[data-testid="summary-successful-count"]',
    failedCount: 'span[data-testid="summary-failed-count"]',
    failedAmount: 'span[data-testid="summary-failed-uncredited-amount"]',
    reconciliationCount: 'span[data-testid="summary-reconciliation-count"]',
  },
  filters: {
    accountOrNricInput: 'input[data-testid="history-filter-account-nric"]',
    dateFromInput: 'input[data-testid="history-filter-date-from"]',
    dateToInput: 'input[data-testid="history-filter-date-to"]',
    sourceDropdown: 'select[data-testid="history-filter-source"]',
    statusDropdown: 'select[data-testid="history-filter-status"]',
    applyBtn: 'button[data-testid="history-filter-apply-btn"]',
    resetBtn: 'button[data-testid="history-filter-reset-btn"]',
  },
  table: {
    container: 'table[aria-label="Top-Up History Records"]',
    rows: 'tbody tr[data-testid="history-table-row"]',
    cellDate: 'td[data-testid="cell-tx-date"]',
    cellTxRef: 'td[data-testid="cell-tx-ref"]',
    cellStudent: 'td[data-testid="cell-student"]',
    cellAccountNumber: 'td[data-testid="cell-ea-number"]',
    cellSource: 'td[data-testid="cell-source"]',
    cellCampaign: 'td[data-testid="cell-campaign"]',
    cellAmount: 'td[data-testid="cell-amount"]',
    cellStatus: 'td[data-testid="cell-status"] span[data-testid="tx-status-badge"]',
    cellActor: 'td[data-testid="cell-actor"]',
  },
  pagination: {
    container: 'nav[data-testid="history-pagination"]',
    pageSize: 'select[data-testid="history-page-size"]',
    pageText: 'span[data-testid="history-page-info"]',
    prevBtn: 'button[data-testid="history-prev-btn"]',
    nextBtn: 'button[data-testid="history-next-btn"]',
  },
  exportCsvBtn: 'button[data-testid="history-btn-export-csv"]',
  emptyState: 'div[data-testid="history-empty-state"]',
};
```

---

## 2. BR / AC Traceability
- **Business Rules (BR)**:
  - `BR-F2-07`: Top-Up History lists all individual and bulk top-ups; its filter-scoped Top-Up Summary shows:
    - `Total Spending`: sum of Success amounts matching current filters.
    - `Successful count`: count of successful transactions.
    - `Failed count`: count of failed transactions, accompanied by the expected uncredited amount.
    - `ReconciliationRequired count`: explicitly identified and tallied within the failed group.
  - `BR-F2-30`: Audit permanently retains transaction reference, amount, timestamp, actor (HQ User, or "System" with the HQ user who launched campaign), campaign code, and run reference. Hard deletions are strictly forbidden.
- **Acceptance Criteria (AC)**:
  - `SCR-05 AC01`: Dynamic Top-Up Summary counters update in real-time when filters are applied.
  - `SCR-05 AC02`: Rows are sorted newest first (`Transaction Date DESC`), 20 rows per page.
  - `SCR-05 AC03`: `ReconciliationRequired` items display distinct badge status "Verifying / Cần đối soát".
  - `SCR-05 AC04`: Date filters enforce Singapore Time (`DD/MM/YYYY`, SGT UTC+8).
  - `SCR-05 AC05`: Clicking `Export CSV` downloads the filtered dataset.

---

## 3. Ma Trận 12 Lớp Validation (Universal Table & Filter Matrix)

| Lớp | Loại Kiểm Thử | Dữ Liệu Input / Thao Tác | Kỳ Vọng Hệ Thống (Expected Behavior) | Mã Lỗi / UI Indicator |
| :--- | :--- | :--- | :--- | :--- |
| **L01** | Empty Table Search | Lọc khoảng ngày không có giao dịch nào | Bảng hiển thị Empty State: *"No top-up transactions found."*; Summary hiển thị `$0.00 SGD`, 0 Success, 0 Failed. | Empty state rendered |
| **L02** | Default View (Pristine) | Truy cập Tab History | Tải 20 giao dịch mới nhất; Summary hiển thị tổng chi tiêu toàn thời gian hoặc mặc định tháng này. | 20 rows per page |
| **L03** | Date Range Validation (BVA) | Chọn `Date From: 25/10/2026`, `Date To: 20/10/2026` ($From > To$) | Báo lỗi inline: *"From Date cannot be later than To Date"*; nút Apply bị disable. | Date order validation |
| **L04** | Status Badge Colors | Các dòng có trạng thái: `Success`, `Failed`, `ReconciliationRequired` | `Success` (Green badge), `Failed` (Red badge), `ReconciliationRequired` (Purple/Amber badge "Verifying"). | Standard status styles |
| **L05** | Top-Up Summary Math Integrity | Lọc 3 giao dịch: $100 (Success), $200 (Success), $150 (Failed) | Total Spending = `$300.00 SGD`; Successful = 2; Failed = 1 (Uncredited: `$150.00 SGD`). | Math check pass |
| **L06** | Currency Format (SGD) | Render cột Amount: `200`, `15.5` | Format chính xác 2 chữ số thập phân: `$200.00 SGD`, `$15.50 SGD`. | Strict Currency format |
| **L07** | BVA Pagination Boundary | Ở Page 1 bấm Previous; ở trang cuối bấm Next | Nút Previous/Next bị disabled ở biên; trang không bị crash. | Disabled boundary buttons |
| **L08** | CSV Export Trigger | Click nút `Export CSV` | Trình duyệt kích hoạt tải file CSV `topup_history_YYYYMMDD.csv`; không chứa ký tự BOM lỗi, mã hóa UTF-8. | Valid CSV download |
| **L09** | PII Masking in History | Kiểm tra cột Student | Tên học sinh hiển thị kèm NRIC masked `T****345A`. | Masked PII in table |
| **L10** | XSS in Campaign / Reason Column | Giao dịch bulk từ campaign có tên `<script>` | Escaped an toàn, render text thuần trong cell, không thực thi script. | Sanitized cell output |
| **L11** | i18n & Table Header Integrity | Toàn bộ header cột và thẻ summary | Không chứa các chuỗi thô như `history.table.headers.*`. | Clean localized headers |
| **L12** | Deep Link Filter Persistence | Truy cập: `/admin/top-up/history?status=FAILED&source=BULK` | Dropdown Status tự chọn `Failed`, Source tự chọn `Bulk`, bảng tự động lọc đúng tập bản ghi. | Filter URL sync |

---

## 4. Error Handling & Visual Feedback
- **Filter Parsing Error**:
  - Nhập sai định dạng ngày: Date Picker tự động sửa hoặc báo viền đỏ `aria-invalid="true"`.
- **Loading Skeleton**:
  - Trong lúc load dữ liệu lọc:
  - 20 dòng Skeleton nhấp nháy, Summary cards mờ nhẹ `opacity-60`.
- **Export Error Handling**:
  - Nếu xuất file thất bại do timeout backend:
  - Hiển thị Toast thông báo: *"Failed to generate export file. Please refine filters and try again."*

---

## 5. JSON Fixtures Data Payload

```json
{
  "topup_history_fixtures": {
    "summary_data": {
      "total_spending": 43080000.00,
      "total_spending_formatted": "$43,080,000.00 SGD",
      "successful_count": 215400,
      "failed_count": 15,
      "failed_uncredited_amount": 3000.00,
      "reconciliation_required_count": 2
    },
    "sample_history_records": [
      {
        "transaction_date": "2026-10-26T10:15:00+08:00",
        "transaction_reference": "TUP-20261026-00129",
        "student_name": "John Tan",
        "student_nric_masked": "T*****345A",
        "account_number": "EA-2026-00001",
        "source": "INDIVIDUAL",
        "campaign_code": null,
        "amount": 250.00,
        "amount_formatted": "$250.00 SGD",
        "status": "SUCCESS",
        "performed_by": "hq_admin_01"
      },
      {
        "transaction_date": "2026-10-26T02:00:15+08:00",
        "transaction_reference": "TUP-20261026-00045",
        "student_name": "Siti Nurhaliza",
        "student_nric_masked": "T*****765B",
        "account_number": "EA-2018-09920",
        "source": "BULK",
        "campaign_code": "CAMP-2026-Q1",
        "amount": 200.00,
        "amount_formatted": "$200.00 SGD",
        "status": "FAILED",
        "failure_reason": "EA_NOT_ACTIVE",
        "performed_by": "System (via hq_admin_02)"
      }
    ]
  }
}
```
