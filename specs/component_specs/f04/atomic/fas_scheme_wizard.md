# Component Spec: FAS Scheme Management Wizard (`fas_scheme_wizard`)

## 1. Metadata & Selector
- **Component ID**: `F04-COMP-SCHEME-WIZARD`
- **Component Name**: FAS Scheme Wizard & Fee Component Dialogs (`Screen H, I, J, K`)
- **Module**: `f04` (Assess FAS & Apply Subsidies)
- **Target Route**: `/admin/fas/schemes` (Screen H) and `/admin/fas/schemes/new` (Screen I)
- **Target Roles**:
  - `MOE HQ User`: Creates and publishes national MOEFAS schemes.
  - `School Admin`: Creates and publishes school-specific SBFAS schemes.
- **Element Tag**: `<section role="region" aria-label="FAS Scheme Configuration Wizard">`

### Playwright Locators (BSK Live DOM Standard)
```typescript
export const fasSchemeLocators = {
  // Screen H: Schemes List
  schemesList: {
    container: 'table[aria-label="FAS Schemes Registry"]',
    createSchemeBtn: 'button[data-testid="btn-create-new-scheme"]',
    schemeRow: 'tbody tr[data-testid="scheme-registry-row"]',
    publishBtn: (schemeId: string) => `button[data-testid="btn-publish-scheme-${schemeId}"]`,
    addFeeBtn: (schemeId: string) => `button[data-testid="btn-add-fee-${schemeId}"]`,
  },
  // Screen I: New Scheme Wizard (Steps: General -> Eligibility -> Subsidy -> Review)
  wizard: {
    stepper: 'nav[data-testid="scheme-wizard-stepper"]',
    step1General: {
      schemeNameInput: 'input[data-testid="scheme-name-input"]',
      schemeTypeSelect: 'select[data-testid="scheme-type-select"]',
      academicYearSelect: 'select[data-testid="scheme-academic-year-select"]',
    },
    step2Eligibility: {
      ghiThresholdInput: 'input[data-testid="scheme-ghi-threshold-input"]',
      pciThresholdInput: 'input[data-testid="scheme-pci-threshold-input"]',
    },
    step3Subsidy: {
      tierNameInput: 'input[data-testid="scheme-tier-name-input"]',
      subsidyRateInput: 'input[data-testid="scheme-subsidy-rate-input"]',
      cellError: 'p[data-testid="scheme-subsidy-rate-error"]',
    },
    nextStepBtn: 'button[data-testid="btn-wizard-next-step"]',
    prevStepBtn: 'button[data-testid="btn-wizard-prev-step"]',
    submitSaveDraftBtn: 'button[data-testid="btn-wizard-save-draft"]',
  },
  // Screen J: Review & Publish Scheme Dialog (Overlap Prevention)
  publishDialog: {
    dialog: 'dialog[data-testid="dialog-publish-scheme"]',
    overlapWarningBanner: 'div[data-testid="alert-scheme-overlap-detected"]',
    confirmPublishBtn: 'button[data-testid="btn-confirm-publish-scheme"]',
    cancelBtn: 'button[data-testid="btn-cancel-publish-scheme"]',
  },
  // Screen K: Add Fee Component Dialog
  addFeeDialog: {
    dialog: 'dialog[data-testid="dialog-add-fee-component"]',
    feeComponentSelect: 'select[data-testid="select-fee-component"]',
    waiverRateInput: 'input[data-testid="input-fee-waiver-rate"]',
    confirmAddFeeBtn: 'button[data-testid="btn-confirm-add-fee"]',
  },
  retroactiveToast: 'div[data-testid="toast-retroactive-subsidy-applied"]',
};
```

---

## 2. BR / AC Traceability
- **Business Rules (BR)**:
  - `FS 6.4 & F4.13 to F4.16`: Scheme Creation and Lifecycle (Draft, Active/Published, Archived).
  - `VR-PUB-01 to VR-PUB-04`: **Overlap Prevention Rules**:
    - A school can have at most one active SBFAS scheme for a given Academic Year and student cohort.
    - Attempting to publish an overlapping scheme triggers blocking error `VR-PUB-02`.
  - `VR-FEE-04`: Cell Validation: Fee waiver percentage must be within $0.00\% \le \text{Rate} \le 100.00\%$. Negative, $>100\%$, non-numeric, or blank entries keep button **DISABLED**.
  - `VR-FEE-05`: Existing components in published schemes are locked; cannot be modified or deleted.
  - `VR-FEE-06`: Immediate Retroactive Application: Adding a new fee component to an active scheme automatically recalculates unpaid charges for enrolled beneficiaries.
- **Acceptance Criteria (AC)**:
  - `TC-234`: Negative subsidy rate or $>100\%$ triggers cell error and disables Add button.
  - `TC-236`: Adding a new fee component triggers toast: *"New component added. Retroactive subsidies recalculated for enrolled students."*
  - `TC-238`: Published scheme fee components cannot be deleted.

---

## 3. Ma Trận 12 Lớp Validation (Universal Wizard & Fee Matrix)

| Lớp | Loại Kiểm Thử | Dữ Liệu Input / Thao Tác | Kỳ Vọng Hệ Thống (Expected Behavior) | Mã Lỗi / UI Indicator |
| :--- | :--- | :--- | :--- | :--- |
| **L01** | Empty Required Scheme Name | Bỏ trống tên chương trình và bấm Next | Báo lỗi bắt buộc; ô nhập viền đỏ `aria-invalid="true"`. | `MSG-0001` |
| **L02** | BVA Subsidy Rate Min ($0.00\%$) | Nhập tỷ lệ giảm trừ `0.00%` | Hợp lệ (cho phép miễn giảm 0% nếu có hỗ trợ khác); không báo lỗi. | Valid 0% rate |
| **L03** | BVA Subsidy Rate Max ($100.00\%$) | Nhập tỷ lệ giảm trừ `100.00%` | Hợp lệ (miễn phí 100%); tính toán số tiền được xóa nợ toàn bộ. | Valid 100% rate |
| **L04** | Subsidy Rate Overflow ($100.01\%$) | Nhập `101%` hoặc `100.01%` | Báo lỗi ô nhập: *"Tỷ lệ hỗ trợ phải từ 0% đến 100%"*; nút Add bị disabled. | `VR-FEE-04` error |
| **L05** | Negative Subsidy Rate ($-15\%$) | Nhập `-15%` | Báo lỗi ô nhập; từ chối số âm; nút Submit bị khóa. | `VR-FEE-04` error |
| **L06** | Overlapping Scheme Publishing | Xuất bản SBFAS 2026 khi trường đã có 1 scheme SBFAS 2026 đang Active | Dialog hiển thị cảnh báo đỏ trùng lặp `VR-PUB-02`; nút Publish bị khóa. | `VR-PUB-02` overlap |
| **L07** | Locked Existing Components (`VR-FEE-05`) | Mở dialog Add Fee trên Scheme đã Publish | Các khoản phí cũ hiển thị icon ổ khóa, không có nút Delete hay ô sửa số tiền. | Locked icon & read-only |
| **L08** | Decimal Precision Rate | Nhập `75.5%` vs `75.55%` vs `75.555%` | Cho phép tối đa 2 chữ số thập phân (`75.50%`, `75.55%`); 3 số thập phân bị từ chối. | Decimal(5,2) limit |
| **L09** | Retroactive Recalculation Toast | Thêm thành công `Second-Tier Misc Fee` vào Scheme Active | Toast thông báo xuất hiện góc trên: *"New component added. Retroactive subsidies recalculated..."*. | `VR-FEE-06` Toast |
| **L10** | Security / XSS in Scheme Name | Nhập `<script>alert('scheme')</script>` | Chuỗi được escape an toàn trong danh sách scheme; không sinh mã độc. | Sanitized plain text |
| **L11** | i18n & Wizard Step Integrity | Kiểm tra tên 4 bước của Wizard và các nút bấm | Không xuất hiện `wizard.step.subsidy`, `buttons.publish`. | Clean English copy |
| **L12** | Form Dirty Wizard Navigation | Đang nhập dở bước 3 bấm quay lại bước 1 | Dữ liệu các bước trước được bảo toàn trong state; không bị mất dữ liệu. | Wizard state retained |

---

## 4. Error Handling & Visual Feedback
- **Cell-Level Error Indicator (`VR-FEE-04`)**:
  - `p[data-testid="scheme-subsidy-rate-error"]`:
  - Hiển thị trực tiếp ngay dưới ô nhập rate khi người dùng gõ giá trị không hợp lệ.
  - Nút `[Add to scheme]` chuyển sang màu xám mờ và có thuộc tính `disabled="true"`.
- **Overlap Prevention Callout**:
  - `div[data-testid="alert-scheme-overlap-detected"]`:
  - Text: *"An active scheme already exists for this Academic Year and cohort. You must archive the existing scheme before publishing a new one."*

---

## 5. JSON Fixtures Data Payload

```json
{
  "fas_scheme_fixtures": {
    "valid_new_scheme": {
      "scheme_name": "Tampines SBFAS 2026 Special Tier",
      "scheme_type": "SBFAS",
      "academic_year": "AY2026",
      "eligibility": {
        "max_ghi": 4500.00,
        "max_pci": 900.00
      },
      "tiers": [
        { "tier_name": "Tier 1", "subsidy_rate_percent": 100.00 },
        { "tier_name": "Tier 2", "subsidy_rate_percent": 75.00 }
      ]
    },
    "invalid_rate_inputs": [
      { "rate": -5.00, "expected_error": "Subsidy rate must be between 0.00% and 100.00%" },
      { "rate": 105.00, "expected_error": "Subsidy rate must be between 0.00% and 100.00%" },
      { "rate": "abc", "expected_error": "Please enter a valid numeric percentage" }
    ],
    "retroactive_fee_component": {
      "scheme_id": "SCHEME-SBFAS-2026-01",
      "fee_component_code": "MISC_FEE_TIER2",
      "waiver_percent": 100.00,
      "expected_toast": "New component added. Retroactive subsidies recalculated for enrolled students."
    }
  }
}
```
