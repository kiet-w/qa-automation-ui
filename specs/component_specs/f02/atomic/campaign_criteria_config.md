# Component Spec: Bulk Top-Up Campaign Configuration (`campaign_criteria_config`)

## 1. Metadata & Selector
- **Component ID**: `F02-COMP-CAMPAIGN-CONFIG`
- **Component Name**: Bulk Campaign Configuration Form (`SCR-08`)
- **Module**: `f02` (Top-Up Management)
- **Target Route**: `/admin/top-up/campaigns/new` or `/admin/top-up/campaigns/:id/edit` (SCR-08)
- **Target Role**: `MOE HQ User`
- **Element Tag**: `<form role="form" aria-label="Bulk Top-Up Campaign Configuration">`

### Playwright Locators (BSK Live DOM Standard)
```typescript
export const campaignConfigLocators = {
  form: 'form[aria-label="Bulk Top-Up Campaign Configuration"]',
  campaignNameInput: 'input[data-testid="campaign-name-input"]',
  academicYearSelect: 'select[data-testid="campaign-academic-year-select"]',
  eligibilityDatePicker: 'input[data-testid="campaign-eligibility-date-input"]',
  topupAmountInput: 'input[data-testid="campaign-amount-input"]',
  criteriaSection: 'fieldset[data-testid="campaign-criteria-fieldset"]',
  criteria: {
    ageRange: {
      enableCheckbox: 'input[data-testid="cb-criterion-age-range"]',
      minAgeInput: 'input[data-testid="input-age-range-min"]',
      maxAgeInput: 'input[data-testid="input-age-range-max"]',
      errorMsg: 'p[data-testid="error-age-range"][role="alert"]',
    },
    accountBalance: {
      enableCheckbox: 'input[data-testid="cb-criterion-balance"]',
      operatorSelect: 'select[data-testid="select-balance-operator"]',
      thresholdInput: 'input[data-testid="input-balance-threshold"]',
      errorMsg: 'p[data-testid="error-balance"][role="alert"]',
    },
    schoolingStatus: {
      enableCheckbox: 'input[data-testid="cb-criterion-schooling-status"]',
      activelyEnrolledCheckbox: 'input[data-testid="cb-actively-enrolled"]',
    },
    school: {
      enableCheckbox: 'input[data-testid="cb-criterion-school"]',
      multiSelectTrigger: 'button[data-testid="trigger-select-schools"]',
      optionsList: 'div[data-testid="list-schools-options"]',
      selectedTags: 'span[data-testid="tag-selected-school"]',
      errorMsg: 'p[data-testid="error-school"][role="alert"]',
    },
    academicLevel: {
      enableCheckbox: 'input[data-testid="cb-criterion-academic-level"]',
      primaryCheckbox: 'input[data-testid="cb-level-primary"]',
      secondaryCheckbox: 'input[data-testid="cb-level-secondary"]',
      errorMsg: 'p[data-testid="error-academic-level"][role="alert"]',
    },
    classGroup: {
      enableCheckbox: 'input[data-testid="cb-criterion-class"]',
      multiSelectTrigger: 'button[data-testid="trigger-select-classes"]',
      errorMsg: 'p[data-testid="error-class"][role="alert"]',
    },
  },
  errors: {
    generalCriteriaError: 'div[data-testid="error-no-criteria"][role="alert"]',
    academicYearClosedError: 'p[data-testid="error-academic-year-closed"][role="alert"]',
    runningCampaignLockMsg: 'div[data-testid="alert-campaign-running-locked"]',
  },
  actions: {
    saveDraftBtn: 'button[data-testid="btn-campaign-save-draft"]',
    previewBtn: 'button[data-testid="btn-campaign-preview"]',
    cancelBtn: 'button[data-testid="btn-campaign-cancel"]',
  },
};
```

---

## 2. BR / AC Traceability
- **Business Rules (BR)**:
  - `BR-F2-13`: A campaign belongs to one Academic Year; code is unique within the year.
  - `BR-F2-14`: Criteria combine via logical **OR**; at least one criterion is strictly mandatory.
    - Baseline preconditions (not criteria): student is Singapore Citizen, has linked Active EA, passes Closure Eligibility Check.
    - 6 Criteria Types (at most once per campaign): Age Range, Account Balance, Schooling Status, School, Academic Level, Class.
    - Multi-select value lists must have at least 1 value selected (`MSG-0224`).
    - An account matching multiple criteria receives **exactly one credit**.
  - `BR-F2-15`: Age Range is inclusive ($7 \le \text{Min} \le \text{Max} \le 15$) measured at the Campaign Eligibility Date.
  - `BR-F2-16`: Eligibility Date defaults to current date; run uses this exact anchor date.
  - `BR-F2-17`: Function 2 sets no campaign budget or cap; spending is tracked in Top-Up Summary figures only.
  - `BR-F2-18`: Only `Draft` campaigns can be edited. Confirm locks campaign into `Running` (`MSG-0215`). Editing invalidates any prior preview (`EX-07`).
- **System Messages**:
  - `MSG-0215`: *"This campaign is running and cannot be changed."*
  - `MSG-0217`: *"Enter an age range from 7 to 15, with the minimum not more than the maximum."*
  - `MSG-0218`: *"Enter a balance operator and an amount of 0 or more."*
  - `MSG-0220`: *"This Academic Year is closed. Choose another Academic Year."*
  - `MSG-0221`: *"Add at least one criterion."*
  - `MSG-0224`: *"Select at least one value for {criterion}, or remove the criterion."*

---

## 3. Ma Trận 12 Lớp Validation (Universal Field-Level Matrix)

| Lớp | Loại Kiểm Thử | Dữ Liệu Input / Thao Tác | Kỳ Vọng Hệ Thống (Expected Behavior) | Mã Lỗi / UI Indicator |
| :--- | :--- | :--- | :--- | :--- |
| **L01** | Empty Required Campaign Name | Để trống Tên chiến dịch và bấm Preview | Báo lỗi bắt buộc `MSG-0001` ("Enter your Campaign Name"); viền đỏ `aria-invalid`. | `MSG-0001` |
| **L02** | Zero Criteria Added | Bỏ chọn toàn bộ 6 tiêu chí và bấm Preview | Báo lỗi `MSG-0221`; nút Preview không điều hướng. | `MSG-0221` ("Add at least one criterion.") |
| **L03** | Closed Academic Year Selection | Chọn năm học có trạng thái `CLOSED` | Báo lỗi `MSG-0220`; không cho phép lưu hoặc Preview. | `MSG-0220` |
| **L04** | Age Range BVA Min/Max ($Min > Max$) | Nhập `Min Age = 12`, `Max Age = 10` | Báo lỗi `MSG-0217`; ô nhập đỏ viền. | `MSG-0217` |
| **L05** | Age Range Out of Bounds ($<7$ or $>15$) | Nhập `Min Age = 6` hoặc `Max Age = 16` | Báo lỗi `MSG-0217` ($7 \le \text{Min} \le \text{Max} \le 15$). | `MSG-0217` |
| **L06** | Incomplete Criterion Inputs | Bật checkbox `Age Range` nhưng chỉ nhập `Min Age = 8`, để trống `Max Age` | Báo lỗi `MSG-0217` (yêu cầu nhập cả hai hoặc bỏ tiêu chí). | `MSG-0217` |
| **L07** | Negative Balance Threshold | Chọn toán tử `<`, nhập số tiền `-50.00` | Báo lỗi `MSG-0218` (ngưỡng số dư không âm). | `MSG-0218` |
| **L08** | Multi-Select Empty Value List | Bật tiêu chí `School` hoặc `Academic Level` nhưng không tích trường/cấp học nào | Báo lỗi `MSG-0224` tương ứng cho từng nhóm. | `MSG-0224` |
| **L09** | BVA Max Length Campaign Name ($150, 151$) | Nhập tên chiến dịch 150 ký tự vs 151 ký tự | 150 ký tự hợp lệ; ký tự thứ 151 bị cắt ngắn bởi `maxlength="150"`. | Maxlength truncation |
| **L10** | Running Campaign Locked State | Cố gắng truy cập URL sửa một campaign đang `RUNNING` | Toàn bộ form bị khóa `disabled="true"`; xuất hiện banner `MSG-0215`. | `MSG-0215` lock banner |
| **L11** | i18n & Error Feedback Integrity | Báo các mã lỗi `MSG-0215`, `MSG-0217`, `MSG-0218`, `MSG-0220`, `MSG-0221`, `MSG-0224` | Câu chữ chính xác 100% tài liệu F2; **CẤM TUYỆT ĐỐI** lộ raw keys. | Exact F2 wording |
| **L12** | Form Invalidation on Edit After Preview | Đã Preview thành công, quay lại đổi Số tiền từ `$200` $\rightarrow$ `$250` | Trạng thái Preview cũ bị hủy (`EX-07`), nút Confirm trên Preview bị khóa, bắt buộc bấm Preview lại. | Preview voided (`EX-07`) |

---

## 4. Error Handling & Visual Feedback
- **Criteria Inline Error Markers**:
  - Mỗi cụm tiêu chí khi có lỗi sẽ hiển thị paragraph alert màu đỏ bên dưới:
    `p[data-testid="error-age-range"][role="alert"]` chứa nội dung `MSG-0217`.
- **Top Alert Banner for Running State**:
  - `div[data-testid="alert-campaign-running-locked"]` với màu nền vàng đậm:
    *"This campaign is running and cannot be changed."*
- **Dynamic Class Option Filter**:
  - Khi thay đổi `Academic Year`, danh sách Lớp học tự động làm mới để chỉ giữ các lớp thuộc năm học mới (`BR-F2-14`).

---

## 5. JSON Fixtures Data Payload

```json
{
  "campaign_config_fixtures": {
    "valid_draft_campaign": {
      "name": "Edusave National Top-Up 2026 Q1",
      "academic_year": "AY2026",
      "eligibility_date": "2026-11-01",
      "topup_amount": 200.00,
      "criteria": {
        "age_range": { "enabled": true, "min_age": 7, "max_age": 15 },
        "schooling_status": { "enabled": true, "actively_enrolled": true },
        "academic_level": { "enabled": true, "levels": ["PRIMARY", "SECONDARY"] }
      },
      "expected_valid": true
    },
    "invalid_scenarios": [
      {
        "test_name": "No criteria selected",
        "name": "Test Campaign",
        "academic_year": "AY2026",
        "topup_amount": 200.00,
        "criteria": {},
        "expected_error_code": "MSG-0221"
      },
      {
        "test_name": "Invalid age bounds",
        "criteria": {
          "age_range": { "enabled": true, "min_age": 16, "max_age": 17 }
        },
        "expected_error_code": "MSG-0217"
      },
      {
        "test_name": "Negative balance operator",
        "criteria": {
          "account_balance": { "enabled": true, "operator": "<", "threshold": -10.00 }
        },
        "expected_error_code": "MSG-0218"
      }
    ]
  }
}
```
