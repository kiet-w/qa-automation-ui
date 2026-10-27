# Component Spec: Run Summary & Run Items Grid (`run_summary_item_grid`)

## 1. Metadata & Selector
- **Component ID**: `F02-COMP-RUN-GRID`
- **Component Name**: Run Summary & Run Item Grid (`SCR-11` & `SCR-12`)
- **Module**: `f02` (Top-Up Management)
- **Target Route**: `/admin/top-up/runs/:id` (SCR-12) and `/admin/top-up/runs` (SCR-11)
- **Target Role**: `MOE HQ User`
- **Element Tag**: `<section role="region" aria-label="Top-Up Run Execution Summary and Items">`

### Playwright Locators (BSK Live DOM Standard)
```typescript
export const runGridLocators = {
  container: 'section[aria-label="Top-Up Run Execution Summary and Items"]',
  runHeader: {
    campaignCode: 'span[data-testid="run-campaign-code"]',
    runStatusBadge: 'span[data-testid="run-status-badge"]',
    startedAt: 'time[data-testid="run-started-at"]',
    completedAt: 'time[data-testid="run-completed-at"]',
    stopRunBtn: 'button[data-testid="btn-run-stop-execution"]',
  },
  summaryMetrics: {
    container: 'div[data-testid="run-summary-metrics-card"]',
    totalCreditedSpending: 'span[data-testid="metric-total-credited"]',
    successfulCount: 'span[data-testid="metric-successful-count"]',
    failedCount: 'span[data-testid="metric-failed-count"]',
    failedAmount: 'span[data-testid="metric-failed-amount"]',
    reconciliationCount: 'span[data-testid="metric-reconciliation-count"]',
  },
  filters: {
    outcomeSelect: 'select[data-testid="select-item-outcome-filter"]',
    exportCsvBtn: 'button[data-testid="btn-run-export-csv"]',
    retryFailedBtn: 'button[data-testid="btn-run-retry-failed"]',
  },
  itemsTable: {
    table: 'table[aria-label="Run Items List"]',
    rows: 'tbody tr[data-testid="run-item-row"]',
    cellStudent: 'td[data-testid="item-student-name"]',
    cellAccountNumber: 'td[data-testid="item-ea-number"]',
    cellAmount: 'td[data-testid="item-amount"]',
    cellOutcomeBadge: 'td[data-testid="item-outcome"] span[data-testid="outcome-badge"]',
    cellFailureCode: 'td[data-testid="item-failure-code"]',
    cellTxRef: 'td[data-testid="item-tx-ref"]',
  },
  stopRunConfirmModal: {
    dialog: 'dialog[data-testid="dialog-confirm-stop-run"]',
    confirmStopBtn: 'button[data-testid="btn-confirm-stop-run-action"]',
  },
};
```

---

## 2. BR / AC Traceability
- **Business Rules (BR)**:
  - `BR-F2-23`: Stop Run Action: A Running run can be Stopped. The current in-flight slot completes, and all remaining queued items become `Failed` with code `RUN_STOPPED`. Already-credited accounts remain credited.
  - `BR-F2-24`: Ascending Account Number processing in small batches/chunks.
  - `BR-F2-26`: Item outcomes are strictly `Successful` or `Failed`.
    - Failure Codes: `EA_NOT_ACTIVE`, `ELIGIBILITY_REVIEW_REQUIRED`, `CRITERIA_NOT_MATCH`, `RUN_STOPPED`, `ELIGIBILITY_CHECK_UNAVAILABLE`, `CREDIT_FAILED`.
    - `ReconciliationRequired` counts inside the Failed group with its own flag.
  - `BR-F2-27`: Each run item has one permanent `FundingReference` created once. Retries reuse it, preventing double-credit in Function 1.
  - `BR-F2-28`: Only `Failed` run items can be retried (not `ReconciliationRequired`); retries must pass all checks again.
  - `BR-F2-29`: Run transitions to `Completed` when no Failed items remain, or `CompletedWithErrors` otherwise.
- **Acceptance Criteria (AC)**:
  - `SCR-12 AC01`: Live counters update in chunks during run execution.
  - `SCR-12 AC02`: Clicking `Stop` halts queue, marks remaining items `RUN_STOPPED`, run status becomes `Stopped`.
  - `SCR-12 AC03`: Clicking `Retry failed` triggers retries using original `FundingReference`.
  - `SCR-12 AC04`: `ReconciliationRequired` items are flagged for operational review and excluded from automated button retry.

---

## 3. Ma Trận 12 Lớp Validation (Universal Table & Execution Matrix)

| Lớp | Loại Kiểm Thử | Dữ Liệu Input / Thao Tác | Kỳ Vọng Hệ Thống (Expected Behavior) | Mã Lỗi / UI Indicator |
| :--- | :--- | :--- | :--- | :--- |
| **L01** | Empty Items State | Run mới khởi tạo chưa có item | Hiển thị bảng trống với spinner `Loading items...`. | Loading state |
| **L02** | Stop Action Execution (`BR-F2-23`) | Click `Stop` khi run đang ở 50% tiến độ | In-flight items hoàn tất; 50% item còn lại chuyển thành `Failed` với `Failure Reason = RUN_STOPPED`. | Status -> `Stopped` |
| **L03** | Retry Failed Button Activation | Run có 15 items `Failed` và 2 `ReconciliationRequired` | Nút `Retry failed` được enable; click vào chỉ retry 15 items `Failed`; 2 item kia giữ nguyên. | Selective retry count |
| **L04** | Failure Code Formatting | Render cột Failure Reason cho các lỗi khác nhau | Hiển thị mã rõ ràng: `EA_NOT_ACTIVE`, `CRITERIA_NOT_MATCH`, `RUN_STOPPED`, `ELIGIBILITY_CHECK_UNAVAILABLE`. | Standard enum labels |
| **L05** | Status Badge CSS | Cột Outcome badge | `Successful` (Green), `Failed` (Red), `ReconciliationRequired` (Purple badge "Needs Reconciliation"). | Distinct visual cues |
| **L06** | Chunk Progress Calculation | Run đang xử lý theo batch 50 tài khoản | Metrics card cập nhật tăng dần sau mỗi batch; không làm treo trang. | Incremental counter sync |
| **L07** | Export CSV of Run Items | Click `Export CSV` | Tải về file `run_{id}_items.csv` chứa đầy đủ cột: Student, EA, Amount, Outcome, Failure Code, TxRef. | CSV Download verified |
| **L08** | Idempotent Retry Key Check | Kiểm tra payload của lần Retry | Giá trị `FundingReference` của từng item trùng khớp 100% với lần chạy đầu tiên (`BR-F2-27`). | Exact funding ref reuse |
| **L09** | PII Masking in Items | Kiểm tra thông tin học sinh trong bảng item | NRIC luôn masked `T****345A`. | Masked NRIC |
| **L10** | XSS in Failure Message | Lý do lỗi từ gateway chứa chuỗi `<script>` | Render text an toàn, HTML entities encoded. | Safe HTML |
| **L11** | i18n & Metric Text Integrity | Toàn bộ tiêu đề summary, nút bấm | Không xuất hiện `run.metrics.failedCount`. Toàn bộ hiển thị nhãn chuẩn. | Clean i18n copy |
| **L12** | State Upgrade on Successful Retry | Retry toàn bộ 15 item lỗi thành công | Run Status tự động chuyển từ `CompletedWithErrors` sang `Completed`. | Status upgraded |

---

## 4. Error Handling & Visual Feedback
- **Stop Run Confirmation Modal**:
  - Khi click `[Dừng chạy chiến dịch]`:
  - Modal cảnh báo xuất hiện: *"Bạn có chắc chắn muốn dừng chiến dịch? Các tài khoản chưa được nạp sẽ chuyển sang trạng thái Thất bại (RUN_STOPPED)."*
- **Reconciliation Alert**:
  - Nếu có item `ReconciliationRequired`:
  - Hiển thị callout cảnh báo tím: *"Có {N} giao dịch chưa rõ kết quả ghi nợ/ghi có. Vui lòng chuyển bộ phận Vận hành đối soát."*

---

## 5. JSON Fixtures Data Payload

```json
{
  "run_grid_fixtures": {
    "run_summary": {
      "run_id": "RUN-20261026-001",
      "campaign_code": "CAMP-2026-Q1",
      "status": "COMPLETED_WITH_ERRORS",
      "started_at": "2026-10-26T02:00:00+08:00",
      "completed_at": "2026-10-26T02:35:12+08:00",
      "total_items": 215400,
      "successful_count": 215385,
      "failed_count": 15,
      "reconciliation_count": 2,
      "total_credited": 43077000.00
    },
    "sample_items": [
      {
        "student_name": "John Tan",
        "account_number": "EA-2026-00001",
        "amount": 200.00,
        "outcome": "SUCCESSFUL",
        "failure_code": null,
        "transaction_reference": "TUP-20261026-00012"
      },
      {
        "student_name": "Siti Nurhaliza",
        "account_number": "EA-2018-09920",
        "amount": 200.00,
        "outcome": "FAILED",
        "failure_code": "EA_NOT_ACTIVE",
        "transaction_reference": null
      },
      {
        "student_name": "Grace Lee",
        "account_number": "EA-2017-00341",
        "amount": 200.00,
        "outcome": "FAILED",
        "failure_code": "RUN_STOPPED",
        "transaction_reference": null
      }
    ]
  }
}
```
