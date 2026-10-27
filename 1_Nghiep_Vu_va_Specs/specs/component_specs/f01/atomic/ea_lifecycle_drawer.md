# Component Spec: EA Lifecycle Event Log Drawer (`ea_lifecycle_drawer`)

## 1. Metadata & Selector
- **Component ID**: `F01-COMP-LIFECYCLE-DRAWER`
- **Component Name**: EA Lifecycle Event Log Drawer / Slide-Over Panel
- **Module**: `f01` (Education Account Lifecycle)
- **Target Route**: `/admin/ea-lifecycle` (SCR-ADM-01)
- **Target Role**: `MOE HQ User`
- **Element Tag**: `<aside role="dialog" aria-modal="true" aria-label="EA Lifecycle Event Log">`

### Playwright Locators (BSK Live DOM Standard)
```typescript
export const eaDrawerLocators = {
  overlay: 'div[data-testid="drawer-overlay"]',
  container: 'aside[aria-label="EA Lifecycle Event Log"]',
  closeButton: 'button[data-testid="ea-drawer-close-btn"]',
  header: {
    accountNumber: 'h2[data-testid="drawer-account-number"]',
    studentName: 'span[data-testid="drawer-student-name"]',
    studentNricMasked: 'span[data-testid="drawer-student-nric"]',
    accountStatusBadge: 'span[data-testid="drawer-status-badge"]',
    currentBalance: 'div[data-testid="drawer-current-balance"]',
  },
  timeline: {
    container: 'ol[data-testid="ea-lifecycle-timeline"]',
    items: 'li[data-testid="ea-timeline-item"]',
    itemTimestamp: (index: number) => `li[data-testid="ea-timeline-item"]:nth-child(${index}) time`,
    itemTitle: (index: number) => `li[data-testid="ea-timeline-item"]:nth-child(${index}) h4`,
    itemDescription: (index: number) => `li[data-testid="ea-timeline-item"]:nth-child(${index}) p[data-testid="timeline-desc"]`,
    itemBadge: (index: number) => `li[data-testid="ea-timeline-item"]:nth-child(${index}) span[data-testid="timeline-badge"]`,
  },
  auditMetadata: {
    accountCreationDate: 'span[data-testid="meta-created-date"]',
    actualClosureDate: 'span[data-testid="meta-closed-date"]',
    lastSyncJobReference: 'span[data-testid="meta-sync-ref"]',
  },
  loadingState: 'div[data-testid="drawer-loading-spinner"]',
};
```

---

## 2. BR / AC Traceability
- **Business Rules (BR)**:
  - `F01-BR02`: Account created on 7th birthday with initial balance `$0.00 SGD`.
  - `F02-BR01`: Account closes when holder turns 16.
  - `F02-BR02`: Every backend access performs the closure check first before returning data.
  - `F02-BR08`: Closed accounts and complete transaction history retained for audit and view (read-only).
  - `F02-BR09`: Repeated access does not duplicate closure event or change closure date.
  - `1.2.7 (WA)`: If holder is $\ge 16$ and balance $> 0.00$ while CPF transfer is deferred, marked `Closure Deferred`.
- **Acceptance Criteria (AC)**:
  - `F01-AC01`: Timeline contains opening event: `Auto-created via Daily Sync (7th Birthday). Initial Balance: $0.00 SGD`.
  - `F02-AC06`: Closed account displays static `Actual Account Closure Date` without duplicate events.
  - `F02-AC07`: Authorized user can view transaction history without triggering new transactions.
  - `F02-AC10`: Holder $\ge 16$ with positive balance displays `Closure Deferred` event.
- **Architecture Decisions (ADR / Decision Codes)**:
  - `TD`: Transaction history permanently immutable.
  - `Audit F3`: PII in audit events must mask NRIC (`T*****345A`).

---

## 3. Ma Trận 12 Lớp Validation (Drawer & Lifecycle Timeline Matrix)

| Lớp | Loại Kiểm Thử | Dữ Liệu Input / Thao Tác | Kỳ Vọng Hệ Thống (Expected Behavior) | Mã Lỗi / UI Indicator |
| :--- | :--- | :--- | :--- | :--- |
| **L01** | Open & Focus Management | Click `[Chi tiết]` tại dòng `EA-2026-00001` | Drawer trượt vào từ cạnh phải; focus tự động chuyển vào Close Button hoặc Tiêu đề Drawer (`aria-modal="true"`). | Focus trapped inside drawer |
| **L02** | Dismiss via ESC Key | Nhấn phím `Escape` khi Drawer đang mở | Drawer đóng ngay lập tức; focus trả lại nút `[Chi tiết]` vừa bấm trước đó. | ESC key dismissal |
| **L03** | Dismiss via Backdrop Click | Click vào lớp phủ mờ đen (Overlay backdrop) bên ngoài Drawer | Drawer đóng an toàn; không gây reload trang hoặc mất trạng thái bảng. | Backdrop dismissal |
| **L04** | Chronological Event Sorting | Xem các sự kiện trong Timeline | Các sự kiện hiển thị theo thứ tự thời gian rõ ràng (Mới nhất ở trên cùng hoặc tuần tự theo mốc vòng đời). | Sorted timeline items |
| **L05** | BVA Initial Balance Event | Kiểm tra sự kiện mở tài khoản (`Account Created`) | Hiển thị chính xác balance ban đầu: `$0.00 SGD`; ghi rõ ngày tháng năm trùng với sinh nhật 7 tuổi. | Initial $0.00 verified |
| **L06** | BVA 16th Birthday Closure Event | Kiểm tra sự kiện đóng tài khoản của học sinh 16 tuổi | Hiển thị sự kiện: `Backend Closure Check (Age 16 reached) -> Status changed to Closed`; ghi nhận `Actual Closure Date`. | Closure event verified |
| **L07** | Positive Balance at Age 16 (Deferred) | Học sinh tròn 16 tuổi nhưng số dư còn `$120.00 SGD` | Hiển thị sự kiện: `Closure Deferred (Balance remaining: $120.00 SGD, CPF Transfer deferred)`. Trạng thái: `Closure Deferred`. | Deferred event banner |
| **L08** | Non-Citizen Revocation Event | Học sinh mất quốc tịch Singapore trước 16 tuổi | Hiển thị sự kiện: `Citizenship Revocation / Change -> Eligibility Review Required / Closed - Non-Citizen`. | Citizenship event log |
| **L09** | PII Masking in Audit Notes | Kiểm tra các đoạn text ghi chú trong timeline | Không chứa NRIC đầy đủ trong mô tả sự kiện (Audit F3 compliant); NRIC phải được che `T*****345A`. | Clean masked timeline |
| **L10** | XSS in Event Description | Mô tả sự kiện hoặc Transaction Description chứa `<script>` | Mã hóa HTML an toàn, hiển thị plain text, không pop-up alert dialog. | Sanitized event text |
| **L11** | i18n & Label Integrity | Toàn bộ tiêu đề, nhãn thời gian, trạng thái badge | Không hiển thị `drawer.timeline.created_at`, `status.closed_16y`. Hiển thị nhãn song ngữ hoặc tiếng Anh/Việt chuẩn hóa. | No raw i18n leaks |
| **L12** | Read-Only Immutability | Kiểm tra các element bên trong Drawer | Không có ô input nào cho phép sửa đổi dữ liệu; toàn bộ là read-only snapshot. | Strict Read-only state |

---

## 4. Error Handling & Visual Feedback
- **Drawer Loading Skeleton**:
  - Khi bấm `[Chi tiết]`, trong khi backend trả về timeline events:
  - Hiển thị spinner hoặc timeline skeleton với 3 node đang nhấp nháy (`animate-pulse`).
- **Data Load Error State**:
  - Nếu API lấy chi tiết sự kiện lỗi (ví dụ 404 hoặc 500):
  - Hiển thị thông báo bên trong Drawer: *"Không thể tải lịch sử sự kiện của tài khoản này. Vui lòng thử lại."*
- **Animation Performance**:
  - Slide-in transition mượt mà (CSS `transform: translateX(0)` trong vòng 200ms), không giật layout trang chính.

---

## 5. JSON Fixtures Data Payload

```json
{
  "ea_drawer_fixtures": {
    "active_account_events": {
      "account_number": "EA-2026-00001",
      "student_name": "John Tan",
      "student_nric_masked": "T*****345A",
      "current_balance": "$200.00 SGD",
      "status": "ACTIVE",
      "events": [
        {
          "event_id": "EVT-001",
          "timestamp": "2026-01-02T00:00:00+08:00",
          "title": "Account Created via Daily Sync",
          "description": "Citizen reached 7th birthday. Education Account initialized with balance $0.00 SGD.",
          "badge": "INITIALIZATION",
          "actor": "System"
        },
        {
          "event_id": "EVT-002",
          "timestamp": "2026-03-15T10:30:00+08:00",
          "title": "Top-Up Credited (Edusave National 2026-Q1)",
          "description": "Amount credited: +$200.00 SGD. New balance: $200.00 SGD. Ref: TUP-20260315-00129",
          "badge": "TOP_UP",
          "actor": "HQ Admin"
        }
      ]
    },
    "closed_account_events": {
      "account_number": "EA-2018-09920",
      "student_name": "Siti Nurhaliza",
      "student_nric_masked": "T*****765B",
      "current_balance": "$0.00 SGD",
      "status": "CLOSED_AGE_16",
      "actual_closure_date": "2026-10-18T23:59:00+08:00",
      "events": [
        {
          "event_id": "EVT-101",
          "timestamp": "2018-03-12T00:00:00+08:00",
          "title": "Account Created",
          "description": "Auto-created on 7th birthday.",
          "badge": "INITIALIZATION",
          "actor": "System"
        },
        {
          "event_id": "EVT-102",
          "timestamp": "2026-10-18T23:59:00+08:00",
          "title": "Account Closed (Age 16 Reached)",
          "description": "Backend closure check triggered upon access. Balance was $0.00 SGD. Account permanently closed.",
          "badge": "CLOSURE",
          "actor": "System"
        }
      ]
    }
  }
}
```
