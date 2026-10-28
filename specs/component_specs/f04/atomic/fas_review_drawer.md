# Component Spec: FAS Application Review Drawer (`fas_review_drawer`)

## 1. Metadata & Selector
- **Component ID**: `F04-COMP-REVIEW-DRAWER`
- **Component Name**: FAS Review Drawer & Household Assessment Panel (`Screen C & D`)
- **Module**: `f04` (Assess FAS & Apply Subsidies)
- **Target Route**: `/admin/fas/applications` (Opens overlay drawer: Screen C for SBFAS, Screen D for MOEFAS)
- **Target Roles**:
  - `School Admin`: Reviews SBFAS applications for own school students.
  - `MOE HQ User`: Reviews MOEFAS applications nationally; views SBFAS read-only.
- **Element Tag**: `<aside role="dialog" aria-modal="true" aria-label="FAS Application Review">`

### Playwright Locators (BSK Live DOM Standard)
```typescript
export const fasDrawerLocators = {
  container: 'aside[aria-label="FAS Application Review"]',
  closeBtn: 'button[data-testid="fas-drawer-close-btn"]',
  header: {
    appId: 'h2[data-testid="drawer-app-id"]',
    applicantName: 'span[data-testid="drawer-applicant-name"]',
    submittedDate: 'time[data-testid="drawer-submitted-date"]',
    statusBadge: 'span[data-testid="drawer-app-status"]',
  },
  householdFinancials: {
    ghiValue: 'span[data-testid="financial-ghi-amount"]',
    householdSize: 'span[data-testid="financial-household-size"]',
    pciValue: 'span[data-testid="financial-pci-amount"]',
    ruleEngineEvaluation: 'div[data-testid="rule-engine-result-card"]',
    moefasResultBadge: 'span[data-testid="badge-moefas-criteria"]',
    pciCriteriaBadge: 'span[data-testid="badge-pci-criteria"]',
  },
  studentSection: {
    container: 'div[data-testid="drawer-students-list"]',
    studentItem: 'div[data-testid="drawer-student-item"]',
    studentName: 'h4[data-testid="student-card-name"]',
    schoolAndClass: 'p[data-testid="student-school-class"]',
  },
  attachedDocuments: {
    container: 'div[data-testid="drawer-documents-list"]',
    docItem: 'div[data-testid="drawer-document-card"]',
    viewOnlineBtn: (docId: string) => `button[data-testid="btn-view-doc-${docId}"]`,
    modalViewer: 'dialog[data-testid="modal-pdf-document-viewer"]',
  },
  mlScoreWidgetContainer: 'div[data-testid="drawer-ml-widget-container"]',
  decisionActions: {
    container: 'div[data-testid="drawer-actions-bar"]',
    approveBtn: 'button[data-testid="btn-drawer-approve-fas"]',
    rejectBtn: 'button[data-testid="btn-drawer-reject-fas"]',
    requestInfoBtn: 'button[data-testid="btn-drawer-request-info"]',
    readOnlyDecidedBanner: 'div[data-testid="banner-already-decided"]',
  },
};
```

---

## 2. BR / AC Traceability
- **Business Rules (BR)**:
  - `FS 3.1 & 3.5`: Drawer opens over the application list from the right margin.
  - `FS 4.1 & 4.2`: Displays comprehensive household declaration: Gross Household Income (GHI), Household Size (adults + children), and Per Capita Income (PCI = GHI / Household Size).
  - `Rule Engine Evaluation`: Checks MOEFAS criteria ($\text{GHI} \le \$3,000$ or $\text{PCI} \le \$750$). If MOEFAS fails but household demonstrates distress, suggests routing to SBFAS.
  - `Document Viewer`: School Admin must be able to view payslips and medical receipts online without downloading insecure files to disk.
  - `Decision State Lock`: If application status is `Approved` or `Rejected`, action buttons are hidden and the decider's name and decision timestamp are shown read-only.
- **Acceptance Criteria (AC)**:
  - `Screen C AC01`: Clicking `[Review]` on a Pending SBFAS opens drawer with `Approve` and `Reject` buttons.
  - `Screen C AC02`: Clicking `[View]` on an Approved or Rejected application opens drawer in Read-Only mode.
  - `Screen C AC03`: GHI and PCI are formatted in SGD with exactly 2 decimal places (`$X,XXX.XX`).
  - `Screen C AC04`: Clicking document `[View online]` launches the in-browser PDF modal viewer.

---

## 3. Ma Trận 12 Lớp Validation (Universal Drawer & Document Matrix)

| Lớp | Loại Kiểm Thử | Dữ Liệu Input / Thao Tác | Kỳ Vọng Hệ Thống (Expected Behavior) | Mã Lỗi / UI Indicator |
| :--- | :--- | :--- | :--- | :--- |
| **L01** | Open & Focus Trapping | Click `[Review]` tại đơn `APP-2026-00412` | Drawer trượt vào từ bên phải; focus rơi vào tiêu đề hoặc nút Close; `aria-modal="true"`. | Focus management |
| **L02** | Dismiss via ESC Key | Nhấn phím `Escape` khi đang mở Drawer | Drawer đóng ngay lập tức; quay lại màn hình danh sách với focus tại nút vừa click. | ESC key dismissal |
| **L03** | Currency Formatting (GHI/PCI) | Dữ liệu backend: `GHI = 4200`, `PCI = 840` | Format hiển thị chuẩn: `$4,200.00 /month` và `$840.00 /month`. | Formatted Currency |
| **L04** | Rule Engine Badge Colors | `MOEFAS: Not Met`, `PCI Criteria: Met` | MOEFAS: Badge xám/đỏ nhạt `[Ineligible]`; PCI: Badge xanh lá `[Eligible]`. | Dual-badge criteria |
| **L05** | Document Online Viewer Modal | Click `[View online]` tại `Payslip_Sep2026.pdf` | Mở Modal PDF viewer; hỗ trợ zoom in/out, xoay trang; không kích hoạt direct download executable. | Secure inline PDF |
| **L06** | Read-Only State for Decided Application | Mở đơn có `Status = APPROVED` | Ẩn các nút `Approve`, `Reject`; hiển thị banner: *"Approved by Siti Aminah on 16/10/2026 (Tier 1)"*. | Read-only decider banner |
| **L07** | BVA Household Size Zero Check | Đơn có khai `Household Size = 0` | Rule engine kích hoạt Deny rule `DENY-INVALID-SIZE`; hiển thị cảnh báo đỏ dữ liệu mâu thuẫn. | Inconsistent size flag |
| **L08** | Multi-Student List Rendering | Đơn xin hỗ trợ cho 3 người con cùng lúc | Liệt kê đủ 3 cards học sinh với đầy đủ cấp lớp (P1, P3, S2); thông tin rõ ràng. | Multi-child listing |
| **L09** | PII Masking of Family Members | Xem thông tin CCCD phụ huynh và các con | Toàn bộ NRIC/FIN che dạng `S****456A`. | PII Masking |
| **L10** | XSS in Document Filename | Tên file đính kèm: `<script>alert(1).pdf` | Tên file được encode an toàn trên UI; không sinh mã thực thi độc hại. | Sanitized filename |
| **L11** | i18n & Financial Label Integrity | Kiểm tra các nhãn GHI, PCI, Rule Engine | Không xuất hiện `drawer.financials.ghi`, `labels.householdSize`. | Clean localized text |
| **L12** | Layout Responsive Integrity | Thu nhỏ màn hình xuống 1024px | 2 cột trong Drawer tự động xếp dọc (stack) mượt mà; không vỡ layout, không tràn chữ. | Responsive layout |

---

## 4. Error Handling & Visual Feedback
- **Document Loading Error**:
  - Khi file PDF đính kèm bị hỏng hoặc mất liên kết trên server S3:
  - Viewer hiển thị thông báo lỗi: *"Unable to preview document. The file may be damaged or unavailable."* kèm nút đóng.
- **Concurrent Update Alert**:
  - Nếu School Admin bấm `Approve` nhưng trong tích tắc đó một Admin khác đã Reject đơn:
  - Hệ thống hiển thị Modal lỗi: *"This application was already decided by {user} on {date}. Your action was cancelled."* và chuyển Drawer sang Read-Only.

---

## 5. JSON Fixtures Data Payload

```json
{
  "fas_review_drawer_fixtures": {
    "sample_sbfas_application": {
      "application_id": "APP-2026-00412",
      "applicant_name": "Tan Ah Teck",
      "applicant_relationship": "Father",
      "submitted_date": "2026-10-15T09:30:00+08:00",
      "status": "PENDING",
      "financial_profile": {
        "gross_household_income": 4200.00,
        "household_size": 5,
        "per_capita_income": 840.00,
        "moefas_result": "INELIGIBLE",
        "pci_result": "ELIGIBLE",
        "routing_recommendation": "SBFAS"
      },
      "students": [
        { "name": "Tan Xiao Ming", "school": "Tampines Primary School", "class": "Primary 3A" },
        { "name": "Tan Xiao Hua", "school": "Tampines Primary School", "class": "Primary 1B" }
      ],
      "documents": [
        { "doc_id": "DOC-001", "name": "Payslip_Sep2026.pdf", "size_kb": 450 },
        { "doc_id": "DOC-002", "name": "Medical_Bill.pdf", "size_kb": 1200 }
      ]
    }
  }
}
```
