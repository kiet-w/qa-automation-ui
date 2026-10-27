# Component Spec: Campaign Preview & Confirm Table (`campaign_preview_confirm`)

## 1. Metadata & Selector
- **Component ID**: `F02-COMP-CAMPAIGN-PREVIEW`
- **Component Name**: Bulk Top-Up Campaign Preview & Confirm (`SCR-09`)
- **Module**: `f02` (Top-Up Management)
- **Target Route**: `/admin/top-up/campaigns/:id/preview` (SCR-09)
- **Target Role**: `MOE HQ User`
- **Element Tag**: `<section role="region" aria-label="Campaign Eligible Accounts Preview">`

### Playwright Locators (BSK Live DOM Standard)
```typescript
export const campaignPreviewLocators = {
  container: 'section[aria-label="Campaign Eligible Accounts Preview"]',
  summaryBanner: {
    container: 'div[data-testid="preview-summary-card"]',
    totalAccounts: 'span[data-testid="preview-total-accounts"]',
    totalForecastAmount: 'span[data-testid="preview-forecast-amount"]',
    previewedAtTimestamp: 'time[data-testid="preview-computed-at"]',
    budgetWarningBanner: 'div[data-testid="preview-budget-warning"]',
  },
  previewTable: {
    container: 'table[aria-label="Eligible Accounts Preview List"]',
    rows: 'tbody tr[data-testid="preview-table-row"]',
    cellStudentName: 'td[data-testid="preview-cell-student-name"]',
    cellAge: 'td[data-testid="preview-cell-age"]',
    cellBalance: 'td[data-testid="preview-cell-balance"]',
    cellSchoolingStatus: 'td[data-testid="preview-cell-schooling-status"]',
    cellSchool: 'td[data-testid="preview-cell-school"]',
    cellAcademicLevel: 'td[data-testid="preview-cell-level"]',
    cellClass: 'td[data-testid="preview-cell-class"]',
    cellMatchedCriteria: 'td[data-testid="preview-cell-matched-criteria"]',
    cellTopupAmount: 'td[data-testid="preview-cell-amount"]',
  },
  pagination: {
    container: 'nav[data-testid="preview-pagination"]',
    pageInfo: 'span[data-testid="preview-page-info"]',
    prevBtn: 'button[data-testid="preview-prev-btn"]',
    nextBtn: 'button[data-testid="preview-next-btn"]',
  },
  messages: {
    noMatchingAccountsAlert: 'div[data-testid="alert-no-accounts-matched"][role="alert"]',
    campaignChangedAlert: 'div[data-testid="alert-campaign-changed"][role="alert"]',
    conflictChangedAlert: 'div[data-testid="alert-campaign-conflict-user"][role="alert"]',
  },
  actions: {
    confirmRunBtn: 'button[data-testid="btn-preview-confirm-run"]',
    backToEditBtn: 'button[data-testid="btn-preview-back-edit"]',
  },
  confirmModal: {
    dialog: 'dialog[data-testid="dialog-confirm-campaign-run"]',
    typeConfirmInput: 'input[data-testid="input-type-confirm-text"]',
    finalSubmitBtn: 'button[data-testid="btn-modal-final-dispatch"]',
  },
};
```

---

## 2. BR / AC Traceability
- **Business Rules (BR)**:
  - `BR-F2-19`: Preview displays per account: student name, age, balance, schooling status, school, academic level, class, matched criteria, and expected top-up amount; alongside total accounts, forecast budget, and computed timestamp (read-only).
  - `BR-F2-20`: Confirm is allowed **only** when preview was computed on the current campaign version and at least one eligible account exists. Modifying criteria or amount invalidates the preview (`EX-07`).
  - `BR-F2-21`: Confirm immediately transitions campaign to `Running` and spawns the execution run (no schedule / recurrence options in MVP).
  - `BR-F2-22`: Each campaign has exactly one run. Double clicks or concurrent confirms produce only one run via row-version check (`EX-08`).
  - `BR-F2-25`: Preview warns when an account already received a top-up from another campaign in the same period.
- **System Messages**:
  - `MSG-0214`: *"No accounts match these criteria."*
  - `MSG-0216`: *"The campaign has changed. Preview again before confirming."*
  - `MSG-0222`: *"This campaign was changed by another user. Refresh and try again."*

---

## 3. Ma Trận 12 Lớp Validation (Universal Table & Confirmation Matrix)

| Lớp | Loại Kiểm Thử | Dữ Liệu Input / Thao Tác | Kỳ Vọng Hệ Thống (Expected Behavior) | Mã Lỗi / UI Indicator |
| :--- | :--- | :--- | :--- | :--- |
| **L01** | Zero Matching Accounts | Bộ tiêu chí không khớp với bất kỳ học sinh nào | Bảng trống; Nút `Confirm` bị `disabled="true"`; Banner hiển thị `MSG-0214`. | `MSG-0214` / Disabled Confirm |
| **L02** | Stale Preview Validation | Đổi tiêu chí ở SCR-08 nhưng cố submit Confirm ở SCR-09 | Hệ thống từ chối; hiển thị `MSG-0216`; bắt buộc bấm Preview lại. | `MSG-0216` |
| **L03** | Row Version Conflict (`EX-08`) | Hai admin cùng thao tác confirm 1 campaign | Admin thứ hai nhận thông báo `MSG-0222`; campaign tự động reload trạng thái mới. | `MSG-0222` |
| **L04** | Forecast Math Accuracy | $N$ tài khoản với mức `$200.00 SGD` | `Total Forecast Amount` = $N \times 200.00$ SGD chính xác; format 2 chữ số thập phân. | Strict calculation check |
| **L05** | Pagination Size (20/page) | Preview có 45 tài khoản eligible | Chia làm 3 trang (20, 20, 5); phân trang mượt mà; không duplicate tài khoản giữa các trang. | 20 items per page |
| **L06** | Matched Criteria Tag Rendering | Tài khoản khớp 2 tiêu chí (Age Range và School) | Cột `Matched Criteria` hiển thị đủ 2 tags: `[Age Range 7-15]`, `[School: Sch 101]`. | Multi-tag badge render |
| **L07** | Duplicate Credit Warning (`BR-F2-25`) | Học sinh đã nhận tiền từ campaign khác trong kỳ | Hiển thị icon cảnh báo màu vàng tại dòng học sinh: *"Already received top-up in current period"*. | Duplicate period warning |
| **L08** | Rapid Double Click Confirm | Bấm nút Confirm 2 lần liên tục | Nút disable ngay lập tức; chỉ tạo đúng 1 Run duy nhất trong hệ thống (`BR-F2-22`). | Single Run guarantee |
| **L09** | Text Confirmation Modal Barrier | Mở modal xác nhận chạy chiến dịch | Nút dispatch chỉ mở khóa khi người dùng gõ đúng chữ `CONFIRM` vào ô input. | Safety barrier unlocked |
| **L10** | Security / XSS in School/Class Name | Tên trường hoặc lớp chứa ký tự XSS | Escape an toàn, hiển thị text thuần, không execute script. | Sanitized table cells |
| **L11** | i18n & Alert Copy Integrity | Toàn bộ thông báo lỗi và xác nhận | Không lộ các raw keys như `preview.alerts.noMatch`. Khớp chính xác `MSG-0214`, `MSG-0216`. | Localized strings verified |
| **L12** | Read-Only Immutability | Kiểm tra các trường trong bảng Preview | Toàn bộ dòng là read-only, không thể sửa trực tiếp số tiền trên từng học sinh. | Strict read-only state |

---

## 4. Error Handling & Visual Feedback
- **Disabled Confirm Cue**:
  - `button[data-testid="btn-preview-confirm-run"][disabled]` kèm tooltip giải thích nếu $Total = 0$.
- **Stale Preview Invalidation**:
  - Khi phát hiện `campaign.updated_at > preview.computed_at`:
  - Toàn bộ bảng mờ đi `opacity-50`, banner cảnh báo màu đỏ xuất hiện:
    *"The campaign has changed. Preview again before confirming."*
- **Dispatching Animation**:
  - Khi xác nhận chạy:
  - Hiển thị spinner chuyển hướng sang `SCR-11 Runs list` hoặc `SCR-12 Run summary`.

---

## 5. JSON Fixtures Data Payload

```json
{
  "campaign_preview_fixtures": {
    "valid_preview_response": {
      "campaign_id": "CAMP-2026-001",
      "campaign_name": "Edusave National Top-Up 2026 Q1",
      "total_accounts": 215400,
      "total_amount_forecast": 43080000.00,
      "previewed_at": "2026-10-26T10:00:00+08:00",
      "sample_rows": [
        {
          "student_name": "John Tan",
          "age": 7,
          "balance": 0.00,
          "schooling_status": "Actively Enrolled",
          "school": "Tampines Primary School",
          "academic_level": "PRIMARY",
          "class": "Primary 1A",
          "matched_criteria": ["Age Range (7-15)", "Schooling Status"],
          "topup_amount": 200.00
        }
      ]
    },
    "zero_match_preview": {
      "total_accounts": 0,
      "total_amount_forecast": 0.00,
      "expected_message_code": "MSG-0214",
      "expected_message_text": "No accounts match these criteria."
    }
  }
}
```
