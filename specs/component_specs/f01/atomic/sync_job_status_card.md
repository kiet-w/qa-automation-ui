# Component Spec: EA Metric Cards & Sync Job Status (`sync_job_status_card`)

## 1. Metadata & Selector
- **Component ID**: `F01-COMP-SYNC-METRICS`
- **Component Name**: EA Lifecycle Metric Cards & Citizen Sync Job Status Banner
- **Module**: `f01` (Education Account Lifecycle)
- **Target Route**: `/admin/ea-lifecycle` (SCR-ADM-01)
- **Target Role**: `MOE HQ User`
- **Element Tag**: `<section role="region" aria-label="EA Lifecycle Metrics and Job Status">`

### Playwright Locators (BSK Live DOM Standard)
```typescript
export const syncMetricsLocators = {
  container: 'section[aria-label="EA Lifecycle Metrics and Job Status"]',
  cards: {
    totalActive: 'div[data-testid="metric-total-active"]',
    totalActiveCount: 'div[data-testid="metric-total-active"] span[data-testid="metric-count"]',
    newlyOpenedMonth: 'div[data-testid="metric-newly-opened"]',
    newlyOpenedCount: 'div[data-testid="metric-newly-opened"] span[data-testid="metric-count"]',
    closedAge16: 'div[data-testid="metric-closed-age16"]',
    closedAge16Count: 'div[data-testid="metric-closed-age16"] span[data-testid="metric-count"]',
    closedNonCitizen: 'div[data-testid="metric-closed-noncitizen"]',
    closedNonCitizenCount: 'div[data-testid="metric-closed-noncitizen"] span[data-testid="metric-count"]',
  },
  syncJobBanner: {
    container: 'div[data-testid="sync-job-banner"]',
    lastSyncTimestamp: 'span[data-testid="last-sync-timestamp"]',
    syncStatusBadge: 'span[data-testid="sync-status-badge"]',
    syncJobRef: 'span[data-testid="sync-job-ref"]',
    processedCount: 'span[data-testid="sync-processed-count"]',
    successCount: 'span[data-testid="sync-success-count"]',
    skippedCount: 'span[data-testid="sync-skipped-count"]',
    failedCount: 'span[data-testid="sync-failed-count"]',
    triggerManualSyncBtn: 'button[data-testid="btn-trigger-manual-sync"]',
  },
};
```

---

## 2. BR / AC Traceability
- **Business Rules (BR)**:
  - `F01-BR01`: Non-citizens are skipped and tallied in skipped/closed metrics.
  - `F01-BR02`: Citizens turning 7 join the newly opened count.
  - `F02-BR01`: Accounts closed upon turning 16 update the closed metric.
  - `2.4`: Every synchronization records a `Processing Reference`, start time, completion time, total records, success count, skipped count, and failed count for reconciliation.
  - `1.1.2`: Daily sync runs at 00:00 SGT (UTC+8); weekend/holiday runs continue.
- **Acceptance Criteria (AC)**:
  - `F01-AC01`: Metric cards update after Initial Sync run.
  - `F01-AC02`: Daily sync run increments newly opened count.
  - `F01-AC11`: Recovered jobs update last successful processing coverage.
  - `F01-AC13`: Weekend execution updates timestamp correctly.
- **Architecture Decisions (ADR / Decision Codes)**:
  - `B6`: Daily sync job schedule 00:00 SGT.
  - `V10`: Reconciliation counters (total, success, failed, skipped) displayed clearly.

---

## 3. Ma Trận 12 Lớp Validation (Metric Cards & Sync Job Status Matrix)

| Lớp | Loại Kiểm Thử | Dữ Liệu Input / Thao Tác | Kỳ Vọng Hệ Thống (Expected Behavior) | Mã Lỗi / UI Indicator |
| :--- | :--- | :--- | :--- | :--- |
| **L01** | Empty / Zero State Metrics | Hệ thống mới khởi tạo chưa có dữ liệu đồng bộ | Hiển thị các chỉ số `0 TK`, badge sync trạng thái `NOT_STARTED` hoặc `IDLE`. | Zero counts rendered |
| **L02** | Default View with Live Counts | Vào trang sau ca chạy Daily Sync thành công | Hiển thị chính xác các thẻ: `342,150 TK Active`, `+1,240 TK (7 tuổi)`, `2,105 TK (16 tuổi)`, `12 TK (Mất QT)`. | Valid formatted integers |
| **L03** | Number Formatting & Localization | Render các số nguyên lớn (`342150`, `1240`) | Format có dấu phẩy ngăn cách hàng nghìn (`342,150`, `1,240`), không hiển thị `342150` trơn. | Thousand-separated format |
| **L04** | Status Badge Colors (Job Status) | Job Status nhận các giá trị: `SUCCESS`, `RUNNING`, `FAILED`, `PARTIAL_SUCCESS` | `SUCCESS` (Green badge), `RUNNING` (Blue badge kèm spinner), `FAILED` (Red badge), `PARTIAL_SUCCESS` (Amber badge). | Dynamic Tailwind badge |
| **L05** | Reconciliation Count Integrity | Kiểm tra phép cộng: $Total = Success + Skipped + Failed$ | Tổng số bản ghi xử lý phải khớp chính xác: $Total = 1250$, $Success = 1240$, $Skipped = 8$, $Failed = 2$. | Mathematical integrity |
| **L06** | BVA Negative / Overflow Count | Backend trả về số lượng âm hoặc giá trị `null` | Hệ thống fallback về `0` hoặc `-`, không crash giao diện, ghi nhận lỗi log. | Fallback safeguard |
| **L07** | Manual Sync Trigger Button | Click `[Kích hoạt đồng bộ]` (nếu tài khoản Admin có quyền) | Nút chuyển sang trạng thái `disabled`, hiển thị icon xoay vòng `Processing...`, mở toast thông báo "Job synchronization queued". | Debounced action trigger |
| **L08** | Unauthorized Role Access | Role School Admin hoặc Read-Only truy cập trang | Nút `[Kích hoạt đồng bộ]` bị ẩn hoàn toàn hoặc disable; hiển thị tooltip không có quyền. | RBAC permission guard |
| **L09** | Timezone Accuracy (SGT UTC+8) | Kiểm tra `last_sync_timestamp` | Hiển thị theo múi giờ Singapore (`DD/MM/YYYY HH:mm:ss SGT`), không hiển thị giờ UTC lệch 8 tiếng. | SGT UTC+8 time format |
| **L10** | XSS in Job Reference or Log Reason | `Processing Reference` chứa `<script>alert(1)</script>` | Chuỗi được escape an toàn, render dưới dạng text thuần trong banner. | HTML Escaped |
| **L11** | i18n & Metric Label Integrity | Kiểm tra tiêu đề 4 thẻ và các mục trong sync banner | Không xuất hiện `dashboard.metrics.total_active`, `job.status.success`. Toàn bộ hiển thị câu từ chuẩn. | No raw i18n keys |
| **L12** | Real-Time Sync Polling / WebSocket | Job sync đang chạy nền (`status = RUNNING`) | Banner cập nhật tiến độ (Progress bar hoặc số đếm tăng dần); khi kết thúc tự động chuyển sang `SUCCESS` mà không cần F5. | Reactive state update |

---

## 4. Error Handling & Visual Feedback
- **Job Failure Alert Banner**:
  - Khi job đồng bộ gặp lỗi (ví dụ: `Job failed: source authentication` hoặc `Job failed: source timeout`):
  - Banner chuyển sang màu đỏ nhạt (Red-50 border Red-500):
    *"Đồng bộ thất bại: Không thể kết nối với Government Citizen Dataset (Timeout). Hệ thống sẽ tự động thử lại sau 15 phút."*
- **Metric Loading State**:
  - Khi đang fetch dữ liệu metrics:
  - 4 thẻ hiển thị Skeleton box `height: 80px` màu xám nhấp nháy, ngăn chặn Cumulative Layout Shift (CLS = 0).

---

## 5. JSON Fixtures Data Payload

```json
{
  "sync_metrics_fixtures": {
    "successful_sync_metrics": {
      "metrics": {
        "total_active_accounts": 342150,
        "newly_opened_this_month": 1240,
        "closed_age_16_this_month": 2105,
        "closed_non_citizen_this_month": 12
      },
      "last_job": {
        "job_reference": "SYNC-20261026-0001",
        "job_name": "Daily Incremental Synchronization",
        "trigger_type": "SCHEDULED",
        "status": "SUCCESS",
        "started_at": "2026-10-26T00:00:00+08:00",
        "completed_at": "2026-10-26T00:04:12+08:00",
        "total_records": 1250,
        "successful_records": 1240,
        "skipped_records": 8,
        "failed_records": 2,
        "failure_reason": null
      }
    },
    "failed_sync_metrics": {
      "last_job": {
        "job_reference": "SYNC-20261025-0002",
        "job_name": "Daily Incremental Synchronization",
        "trigger_type": "SCHEDULED",
        "status": "FAILED",
        "started_at": "2026-10-25T00:00:00+08:00",
        "completed_at": "2026-10-25T00:01:10+08:00",
        "total_records": 1245,
        "successful_records": 0,
        "skipped_records": 0,
        "failed_records": 1245,
        "failure_reason": "Government API source timeout after 3 retries."
      }
    }
  }
}
```
