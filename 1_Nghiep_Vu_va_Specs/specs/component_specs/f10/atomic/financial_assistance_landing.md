# Component Specification: Financial Assistance Landing (`f10-landing`)

> **Module**: `f10` - FAS Online Family Application Portal (Cổng Nộp Đơn FAS Phụ Huynh)  
> **Component**: `financial_assistance_landing`  
> **Source Spec**: `specs/md/FS document/FS-10_FAS_Family_Application_Portal.md` (Mục 3 Màn hình Financial assistance, Mục 10 Bản nháp) & `specs/validation_rules/md/FS10_R10_FAS_Application_Validation (Draft).md`  
> **Target Audience**: Parent / Legal Guardian (Đăng nhập Singpass qua e-Service Portal)  

---

## 1. Metadata & Selector

- **Route URL / Access Path**: e-Service Portal $\rightarrow$ Financial assistance (`/parent/fas` hoặc `/eservice/financial-assistance`)
- **Container Element Tag**: `<main id="financial-assistance-portal" data-testid="page-fas-landing">`
- **Playwright Locators (BSK Standardized Convention)**:

| Element Name | HTML Tag / Type | Playwright Locator (BSK Convention) | Description / Notes |
| :--- | :--- | :--- | :--- |
| **Page Title** | `h1` | `page.locator("h1:has-text('Financial assistance')")` | Portal section header |
| **Apply for FAS Button** | `button / a` | `page.locator("button[data-testid='btn-apply-fas'], a:has-text('Apply for FAS')")` | Primary CTA; visible when no active draft |
| **Ineligible Help Notice** | `p.help-text` | `page.locator("p:has-text('All eligible children already have an application under review, or have turned 16')")` | Shown when Apply button is disabled |
| **Resume Draft Button** | `button / a` | `page.locator("button[data-testid='btn-resume-draft'], a:has-text('Resume draft')")` | Primary CTA when draft exists |
| **Discard Draft Button** | `button` | `page.locator("button[data-testid='btn-discard-draft'], button:has-text('Discard draft')")` | Discard action button |
| **Draft Summary Card** | `div.card` | `page.locator("div[data-testid='card-draft-application'], .draft-card")` | Displays step n of 5, saved timestamp |
| **My Applications Section** | `section` | `page.locator("section[data-testid='section-my-applications'], #my-applications")` | Container of submitted family applications |
| **Empty Applications State** | `p` | `page.locator("p:has-text('You have not applied yet.')")` | Empty state notice when 0 applications |

---

## 2. BR / AC Traceability

- **Functional Requirements**: `FS-10` Section 1.1, Section 2 Step 1, Section 3 Components 1-4, Section 10 Draft.
- **Business Rules (BR)**:
  - `BR-10-LAND-01`: Nút `Apply for FAS` hiển thị khi phụ huynh chưa có bản nháp nào đang dở dang.
  - `BR-10-LAND-02`: Nút `Apply for FAS` **bị khóa (disabled)** khi không có đứa con nào đủ điều kiện nộp đơn:
    1. Mọi con từ đủ 16 tuổi trở lên (`turned 16`).
    2. Đã có đơn đang chờ xét (`already has an application under review`).
    3. Không có form FAS nào (cả MOEFAS lẫn SBFAS của trường con) đang mở (`form is closed`).
    - Kèm thông báo: `"All eligible children already have an application under review, or have turned 16."`
  - `BR-10-LAND-03`: Mỗi phụ huynh chỉ có **tối đa một bản nháp duy nhất** (`One draft per parent`). Khi đã có bản nháp, nút `Resume draft` và `Discard draft` sẽ hiển thị thay thế cho `Apply for FAS`.
  - `BR-10-LAND-04`: Thẻ Draft hiển thị rõ: thời gian lưu gần nhất (`Saved DD/MM/YYYY HH:mm`), bước đang dở (`step n of 5 (tên bước)`), các con đã chọn (`· not submitted`).
- **User Story Traceability**: `US-F10-01` (Phụ huynh truy cập cổng FAS, khởi tạo đơn mới hoặc khôi phục bản nháp).
- **Access Control (RBAC)**: Chỉ phụ huynh/người giám hộ hợp pháp đã xác thực qua Singpass.

---

## 3. Ma trận 12 lớp Validation

| Lớp Kiểm Thử (12 Tầng) | Điều Kiện / Dữ Liệu Đầu Vào | Kỳ Vọng Giao Diện & Hành Vi Hệ Thống | Mã Lỗi / Phản Hồi Trực Quan |
| :--- | :--- | :--- | :--- |
| **1. Pristine No-Draft State** | Phụ huynh chưa từng nộp đơn và không có bản nháp nào. | Nút `Apply for FAS` sáng bật; phần My applications hiển thị dòng text `"You have not applied yet."`. | Giao diện sạch sẽ, CTA rõ ràng. |
| **2. Draft Detected State** | Phụ huynh đã lưu nháp ở Bước 3. | Nút `Apply for FAS` biến mất; thay bằng nút `Resume draft` và `Discard draft`; thẻ Draft card xuất hiện hiển thị `"step 3 of 5 (Documents)"`. | Thẻ Draft hiển thị nổi bật. |
| **3. Resume Draft Navigation** | Bấm nút `Resume draft` trên landing page. | Hệ thống mở ngay lập tức Wizard nộp đơn tại chính xác bước đã lưu (Bước 3) với dữ liệu đã lưu giữ nguyên vẹn. | Mở đúng Bước 3. |
| **4. Discard Draft Confirmation** | Bấm nút `Discard draft`. | Hiển thị hộp thoại xác nhận hủy nháp: `"Are you sure you want to discard your draft application?"`. Khi xác nhận, bản nháp bị xóa sạch, nút `Apply for FAS` xuất hiện trở lại. | Toast: `"Draft discarded."` |
| **5. Ineligibility Lock (All Turned 16)** | Phụ huynh có 2 con: Con lớn 18 tuổi, con nhỏ 16 tuổi 1 ngày. | Nút `Apply for FAS` bị disabled (`disabled="true"`); hiển thị ghi chú trợ giúp màu xám bên dưới. | `All eligible children already have an application under review, or have turned 16.` |
| **6. Ineligibility Lock (All Pending)** | Phụ huynh có 1 con và đã nộp đơn FAS tuần trước (đơn đang `Under review`). | Nút `Apply for FAS` bị disabled; phụ huynh không thể tạo thêm đơn thứ hai cho cùng đứa trẻ. | Ghi chú giải thích rõ ràng. |
| **7. Ineligibility Lock (All Forms Closed)** | Không có kỳ xét duyệt FAS nào mở hôm nay (ngoài khoảng Form opens - closes). | Nút `Apply for FAS` bị disabled. | Nút bị khóa. |
| **8. Double-Click Resume Prevention** | Bấm đúp nhanh nút `Resume draft`. | Trình duyệt chỉ kích hoạt 1 lần chuyển hướng duy nhất, không nạp trùng lặp API session. | Điều hướng mượt mà. |
| **9. Multi-Child Grouping Display** | Phụ huynh đã nộp đơn cho 2 con trong kỳ trước. | Khối My applications gom 2 con vào cùng 1 thẻ gia đình `Family application FAM-2026-00045`. | Hiển thị thẻ gia đình hợp nhất. |
| **10. UI Health & Responsive Layout** | Mở trang trên thiết bị di động (Mobile Safari / Chrome viewport 390px) và Desktop 1920px. | Thẻ Draft card và timeline tự động co giãn theo cột; các nút bấm có kích thước cảm ứng tối thiểu 44x44px; 0 console errors. | Đạt chuẩn Invariant 7 UI Health. |
| **11. Session Timeout Recovery** | Phiên đăng nhập Singpass hết hạn khi đang xem trang Landing. | Bấm `Resume draft` tự động chuyển hướng an toàn về trang đăng nhập Singpass; sau khi đăng nhập xong tự quay lại `/parent/fas`. | Bảo toàn luồng người dùng. |
| **12. Error Loading Applications** | API lấy danh sách đơn của phụ huynh bị lỗi HTTP 500. | Hiển thị thông báo lỗi nhẹ nhàng và nút thử lại: `"We could not load your applications. Please try again."`, không crash toàn trang. | Fallback state thân thiện. |

---

## 4. Error Handling & Visual Feedback

- **Standard Messages**:
  - Không có con đủ điều kiện: `"All eligible children already have an application under review, or have turned 16."`
  - Chưa từng nộp đơn: `"You have not applied yet."`
  - Hủy nháp thành công: `"Draft discarded."`
- **Visual Cues**:
  - Nút `Apply for FAS` có màu xanh lá nổi bật (`bg-emerald-600 hover:bg-emerald-700 text-white`).
  - Thẻ Draft có viền nét đứt màu xanh dương nhạt (`border-dashed border-blue-400 bg-blue-50/50`).

---

## 5. JSON Fixtures Data Payload

```json
{
  "landing_with_draft_payload": {
    "hasDraft": true,
    "draftDetails": {
      "savedAt": "26/10/2026 10:15",
      "currentStep": 3,
      "stepName": "Documents",
      "selectedChildren": ["Tan Mei Ling (Primary 6)", "Tan Jun Jie (Primary 3)"]
    },
    "eligibleChildrenCount": 2
  },
  "landing_ineligible_payload": {
    "hasDraft": false,
    "children": [
      { "name": "Tan Wei Kang", "age": 17, "ineligibleReason": "turned 16, cannot apply" }
    ],
    "isApplyButtonDisabled": true,
    "expectedHelpText": "All eligible children already have an application under review, or have turned 16."
  },
  "landing_pristine_payload": {
    "hasDraft": false,
    "submittedApplications": [],
    "isApplyButtonEnabled": true
  }
}
```
