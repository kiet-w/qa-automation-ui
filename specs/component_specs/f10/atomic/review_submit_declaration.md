# Component Specification: Review, Submit & Declaration - Step 5 (`f10-review-submit`)

> **Module**: `f10` - FAS Online Family Application Portal (Cổng Nộp Đơn FAS Phụ Huynh)  
> **Component**: `review_submit_declaration` (Wizard Step 5: Review Summary, What Happens Next & Declaration)  
> **Source Spec**: `specs/md/FS document/FS-10_FAS_Family_Application_Portal.md` (Mục 8 Bước 5, Mục 11 BR4, BR5, BR7, Mục 12 T6, T7, T8) & `specs/validation_rules/md/FS10_R10_FAS_Application_Validation (Draft).md`  
> **Target Audience**: Parent / Legal Guardian (Đăng nhập Singpass)  

---

## 1. Metadata & Selector

- **Route URL / Access Path**: e-Service Portal $\rightarrow$ Financial assistance $\rightarrow$ Apply for FAS $\rightarrow$ Step 5 (`/parent/fas/apply/step-5`)
- **Container Element Tag**: `<section id="fas-wizard-step-5" data-testid="wizard-step-5-review">`
- **Playwright Locators (BSK Standardized Convention)**:

| Element Name | HTML Tag / Type | Playwright Locator (BSK Convention) | Description / Notes |
| :--- | :--- | :--- | :--- |
| **Step 5 Container** | `div` | `page.locator("div[data-testid='step-container-review']")` | Step 5 wrapper |
| **Applicant Summary Block** | `section` | `page.locator("section[data-testid='review-applicant-summary']")` | Applicant profile review |
| **Children Summary Block** | `section` | `page.locator("section[data-testid='review-children-summary']")` | Selected children review |
| **Household Summary Block** | `section` | `page.locator("section[data-testid='review-household-summary']")` | Size, GHI, PCI review |
| **What Happens Next Block** | `div.callout` | `page.locator("div[data-testid='review-what-happens-next']")` | Routing explanation card |
| **Context Review Block** | `section` | `page.locator("section[data-testid='review-context-summary']")` | Context display |
| **Edit Context Link** | `a` | `page.locator("a[data-testid='link-edit-context'], a:has-text('Edit context')")` | Returns to Step 4 |
| **Confirmation Checkbox** | `input[type="checkbox"]` | `page.locator("input[data-testid='cb-declaration-confirmation'], input[name='confirm_declaration']")` | Required confirmation |
| **Submit Application Button** | `button` | `page.locator("button[data-testid='btn-submit-fas-application'], button:has-text('Submit application')")` | Disabled until confirmed |
| **Submission Toast** | `div[role="status"]` | `page.locator("div[role='status']:has-text('submitted')")` | Toast upon successful submit |

---

## 2. BR / AC Traceability

- **Functional Requirements**: `FS-10` Section 8 Step 5, Section 11 BR4, BR5, BR7, Section 12 Scenarios T6, T7, T8.
- **Business Rules (BR)**:
  - `BR-10-SUB-01`: Bước 5 tổng hợp toàn bộ thông tin đã điền qua 4 khối chính: `Applicant`, `Children`, `Household`, và `Context` (Scenario T6).
  - `BR-10-SUB-02`: Khối `"What happens next"` giải thích rõ ràng lộ trình phân luồng dự kiến cho từng con:
    - **MOEFAS**: `"reviewed by the system automatically after the form closes on DD/MM/YYYY"`. Nếu có tick SBFAS thì ghi thêm: `"if not eligible, {trường} reviews it under SBFAS"`.
    - **SBFAS**: `"reviewed by {trường}"` kèm lý do (ví dụ không đủ điều kiện quốc tịch MOEFAS).
    - Ghi chú định hướng: `"Indicative only, based on the figures above. MOEFAS is assessed automatically after the application form closes (lowest per capita income first); SBFAS is decided by the school."`
  - `BR-10-SUB-03`: Cam kết bắt buộc (`BR7`): Checkbox `"I confirm the information is true, and I agree to MOE verifying it with Government agencies."` **bắt buộc phải tick**. Nút `Submit application` **bị khóa hoàn toàn cho đến khi tick** (Scenario T7).
  - `BR-10-SUB-04`: Khi nộp thành công (`BR4`):
    - Hệ thống tạo **một đơn cho mỗi con được chọn** (nguồn `Online`, nguồn thu nhập `API`).
    - Nhiều con dùng chung một mã gia đình `FAM-YYYY-NNNNN`.
    - Bản nháp (`Draft`) của phụ huynh bị xóa sạch khỏi hệ thống.
    - Hiển thị Toast thông báo (Scenario T8):
      - 1 con: `"Application submitted for assessment."`
      - Từ 2 con trở lên: `"Applications submitted."`
  - `BR-10-SUB-05`: Chống gửi trùng lặp (Anti-Double Submit): Nút `Submit application` tự động chuyển sang disabled ngay sau click đầu tiên và hiện trạng thái loading.
- **User Story Traceability**: `US-F10-06` (Xem lại tổng thể, xác nhận cam kết và nộp đơn FAS trực tuyến).
- **Access Control (RBAC)**: Chỉ phụ huynh của học sinh.

---

## 3. Ma trận 12 lớp Validation

| Lớp Kiểm Thử (12 Tầng) | Điều Kiện / Dữ Liệu Đầu Vào | Kỳ Vọng Giao Diện & Hành Vi Hệ Thống | Mã Lỗi / Phản Hồi Trực Quan |
| :--- | :--- | :--- | :--- |
| **1. Unchecked Confirmation Lock (T7)** | Mở Bước 5 nhưng chưa tick checkbox cam kết xác nhận. | Nút `Submit application` bị khóa chặt (`disabled="true"` hoặc `aria-disabled="true"`). Không thể nộp đơn. | Nút xám mờ; cursor not-allowed. |
| **2. Checked Confirmation Enable** | Tick vào checkbox cam kết xác nhận. | Nút `Submit application` lập tức sáng bật chuyển sang màu xanh lá (`bg-emerald-600`), sẵn sàng nộp. | Nút bật sáng mượt mà. |
| **3. Edit Context Shortcut Link** | Bấm link `"Edit context"` tại khối Context. | Hệ thống điều hướng quay trở lại Bước 4 (`/parent/fas/apply/step-4`); con trỏ tự động focus vào textarea Context. | Điều hướng quay lại Bước 4. |
| **4. What Happens Next - Citizen Child** | Con là công dân Singapore (SC), GHI/PCI trong ngưỡng dự kiến. | Khối What happens next hiển thị lộ trình MOEFAS kèm ngày đóng form cụ thể. | `MOEFAS: reviewed by the system automatically after the form closes on 31/12/2026.` |
| **5. What Happens Next - PR Child** | Con là thường trú nhân Singapore PR. | Khối What happens next hiển thị rõ đơn sẽ được chuyển thẳng cho trường con xét diện SBFAS. | `SBFAS: reviewed by {school} (not eligible for MOEFAS by nationality).` |
| **6. Single Child Submit Execution** | Phụ huynh nộp đơn cho 1 con duy nhất. Bấm `Submit application`. | Tạo 1 đơn mới, xóa bản nháp, điều hướng về màn hình theo dõi đơn kèm Toast thông báo số ít. | Toast: `Application submitted for assessment.` |
| **7. Multi-Child Submit Execution (T8)** | Phụ huynh nộp đơn cho 2 con. Bấm `Submit application`. | Tạo 2 đơn con dùng chung mã gia đình `FAM-2026-00045`, xóa bản nháp, hiện Toast thông báo số nhiều. | Toast: `Applications submitted.` |
| **8. Double-Click Submit Prevention** | Phụ huynh bấm đúp liên tiếp 2 lần vào nút `Submit application`. | Nút lập tức disabled sau click thứ nhất, hiển thị spinner `"Submitting..."`. Chỉ có duy nhất 1 giao dịch tạo đơn được thực thi. | Chống trùng đơn tuyệt đối. |
| **9. Concurrent Child Application Check** | Một phụ huynh khác nộp đơn cho cùng một đứa con trong lúc phụ huynh này đang xem Bước 5. | Server phát hiện con đã có đơn `Under review`; hủy giao dịch tạo đơn; thông báo lỗi giải thích rõ ràng. | `{Beneficiary name} already has an application under review.` |
| **10. UI Health & Accessibility** | Kiểm tra tương tác bàn phím (phím Tab, phím Space). | Phím Space kích hoạt checkbox cam kết mượt mà; các khối tóm tắt có phân cấp thẻ semantic (`section`, `h3`, `p`); 0 console errors. | Đạt chuẩn Invariant 7 UI Health. |
| **11. Draft Auto-Cleanup Verification** | Sau khi nộp thành công, quay lại trang chủ Financial assistance. | Thẻ Draft card đã biến mất hoàn toàn; thay vào đó là thẻ đơn đã nộp kèm timeline theo dõi. | Bản nháp được dọn sạch 100%. |
| **12. Server Error Resilience** | API submit đơn trả về mã lỗi HTTP 500 hoặc rớt mạng. | Dữ liệu trên trang được giữ nguyên 100%; hiển thị error banner: `"We could not submit your application. Please try again."`; cho phép bấm nộp lại. | Chống mất dữ liệu người dùng. |

---

## 4. Error Handling & Visual Feedback

- **Standard Messages**:
  - Toast nộp 1 con: `"Application submitted for assessment."`
  - Toast nộp nhiều con: `"Applications submitted."`
  - Con đã có đơn: `"{Beneficiary name} already has an application under review."`
  - Lỗi máy chủ: `"We could not submit your application. Please try again."`
- **Visual Cues**:
  - Khối `"What happens next"` có nền xanh dương nhạt (`bg-blue-50 border border-blue-200 text-blue-900`) kèm icon la bàn/lộ trình `🧭`.
  - Nút `Submit application` có kích thước lớn, màu xanh lá đậm nổi bật (`bg-emerald-600 hover:bg-emerald-700 text-white font-medium py-3 px-6 rounded-lg`).

---

## 5. JSON Fixtures Data Payload

```json
{
  "submission_summary_two_children": {
    "applicant": {
      "fullName": "Mdm Noor Aisha",
      "nric": "S8212345E",
      "relationship": "Mother",
      "phone": "98765432",
      "email": "noor.aisha@example.sg"
    },
    "children": [
      {
        "name": "Nurul Huda Binte Mohd",
        "nric": "T1456789A",
        "school": "Tampines Primary School",
        "class": "Primary 6 Compassion",
        "indicativeRoute": "MOEFAS (auto-review after 31/12/2026)"
      },
      {
        "name": "Muhammad Danial Bin Mohd",
        "nric": "T1856789B",
        "school": "Tampines Primary School",
        "class": "Primary 2 Honesty",
        "indicativeRoute": "MOEFAS (auto-review after 31/12/2026)"
      }
    ],
    "household": {
      "size": 4,
      "ghi": "S$ 1,600.00",
      "pci": "S$ 400.00",
      "considerSbfas": true
    },
    "declarationConfirmed": true,
    "expectedToast": "Applications submitted.",
    "expectedFamilyCodePrefix": "FAM-2026-"
  }
}
```
