# Component Specification: Children Selection - Step 1 (`f10-children-selection`)

> **Module**: `f10` - FAS Online Family Application Portal (Cổng Nộp Đơn FAS Phụ Huynh)  
> **Component**: `children_selection` (Wizard Step 1: Your Details & Children Selection)  
> **Source Spec**: `specs/md/FS document/FS-10_FAS_Family_Application_Portal.md` (Mục 4 Bước 1, Mục 11 BR1, BR2, Mục 12 T1, T2, T12) & `specs/validation_rules/md/FS10_R10_FAS_Application_Validation (Draft).md`  
> **Target Audience**: Parent / Legal Guardian (Đăng nhập Singpass)  

---

## 1. Metadata & Selector

- **Route URL / Access Path**: e-Service Portal $\rightarrow$ Financial assistance $\rightarrow$ Apply for FAS (`/parent/fas/apply/step-1` hoặc `/eservice/fas/wizard/step-1`)
- **Container Element Tag**: `<section id="fas-wizard-step-1" data-testid="wizard-step-1-children">`
- **Playwright Locators (BSK Standardized Convention)**:

| Element Name | HTML Tag / Type | Playwright Locator (BSK Convention) | Description / Notes |
| :--- | :--- | :--- | :--- |
| **Step 1 Container** | `div` | `page.locator("div[data-testid='step-container-children']")` | Step 1 wrapper |
| **Applicant Details Block** | `fieldset` | `page.locator("fieldset[data-testid='section-your-details']")` | Read-only auto-filled profile |
| **Edit Profile Link** | `a` | `page.locator("a:has-text('Change them in My details')")` | Link to F8 My details screen |
| **Relationship Select** | `select` | `page.locator("select[data-testid='select-relationship-children'], select[name='relationship']")` | Required; Father, Mother, Legal guardian, etc. |
| **Child Checkbox Item** | `input[type="checkbox"]` | `page.locator("input[data-testid^='cb-child-select-']")` | Selects child for application |
| **Child Locked Notice** | `span.badge` | `page.locator("span[data-testid^='child-lock-reason-']")` | Ineligible reason badge |
| **SBFAS Only Tag** | `span.badge` | `page.locator("span:has-text('school SBFAS only')")` | Displayed for Singapore PR students |
| **Step 1 Continue Button** | `button` | `page.locator("button[data-testid='btn-step1-continue'], button:has-text('Continue')")` | Active only when $\ge 1$ child & relationship selected |
| **Save Draft & Exit Button** | `button` | `page.locator("button[data-testid='btn-save-draft-exit'], button:has-text('Save draft & exit')")` | Saves state and navigates to landing |

---

## 2. BR / AC Traceability

- **Functional Requirements**: `FS-10` Section 4 Step 1, Section 11 BR1, BR2, Section 12 Scenarios T1, T2, T12.
- **Business Rules (BR)**:
  - `BR-10-CHILD-01`: Thông tin phụ huynh (`Your details`) gồm Họ tên, NRIC, Ngày sinh, Giới tính, Category, Nationality, Số điện thoại, Email và Địa chỉ được tự động điền từ Singpass và hồ sơ F8 (My details), hoàn toàn **chỉ đọc (read-only)** trong wizard này (`BR2`). Phụ huynh muốn sửa phải qua màn hình F8 My details.
  - `BR-10-CHILD-02`: Quan hệ với con (`Your relationship to the children`) là **trường bắt buộc**. Danh sách tùy chọn: `Father`, `Mother`, `Legal guardian`, `Grandfather`, `Grandmother`, `Sibling`, `Uncle`, `Aunt`, `Cousin`, `Other`.
  - `BR-10-CHILD-03`: Danh sách con hiển thị toàn bộ các học sinh được liên kết với tài khoản phụ huynh trong CSDL MOE.
  - `BR-10-CHILD-04`: Điều kiện khóa con (Ineligibility Locks - `BR1`):
    1. **Đã từ 16 tuổi trở lên**: Bị khóa với lý do `"turned 16, cannot apply"` (Scenario T2).
    2. **Đã có đơn đang chờ duyệt**: Bị khóa với lý do `"already has an application under review"`.
    3. **Form nộp đơn đang đóng**: Bị khóa với lý do `"application form is closed (opens DD/MM/YYYY)"` nếu hôm nay không có form MOEFAS và cũng không có form SBFAS của trường con đang mở (Scenario T12).
  - `BR-10-CHILD-05`: Nút `Continue` chỉ được kích hoạt (enabled) khi:
    $$\text{Đã chọn ít nhất 1 con} \quad \text{VÀ} \quad \text{Đã chọn quan hệ với con}$$
- **User Story Traceability**: `US-F10-02` (Phụ huynh chọn danh sách các con cần nộp đơn FAS trực tuyến).
- **Access Control (RBAC)**: Chỉ phụ huynh của học sinh.

---

## 3. Ma trận 12 lớp Validation

| Lớp Kiểm Thử (12 Tầng) | Điều Kiện / Dữ Liệu Đầu Vào | Kỳ Vọng Giao Diện & Hành Vi Hệ Thống | Mã Lỗi / Phản Hồi Trực Quan |
| :--- | :--- | :--- | :--- |
| **1. Empty / Required Guards** | Chưa chọn con nào (0 con được tick) hoặc chưa chọn Relationship. | Nút `Continue` bị disable (`disabled="true"` hoặc `aria-disabled="true"`). Không thể chuyển sang Bước 2. | Nút xám mờ; không phát sinh error banner. |
| **2. Relationship Selection Required** | Đã tick chọn 1 con nhưng để trống ô `Relationship to the children`. | Nút `Continue` tiếp tục bị disable cho đến khi chọn một quan hệ hợp lệ trong dropdown. | Yêu cầu chọn quan hệ (`MSG-0001`). |
| **3. Age Limit Lock (16 Years Old)** | Con tròn 16 tuổi vào ngày nộp đơn (ví dụ sinh 26/10/2010). | Checkbox của con bị disable hoàn toàn; hiển thị huy hiệu chữ đỏ/cam bên cạnh tên con (Scenario T2). | `turned 16, cannot apply` |
| **4. Pending Application Lock** | Con đã nộp đơn và đang ở trạng thái `Under review` (Pending). | Checkbox của con bị disable; hiển thị huy hiệu giải thích. | `already has an application under review` |
| **5. Closed Application Period Lock** | Hôm nay nằm ngoài khoảng mở form của MOEFAS và trường con (Scenario T12). | Checkbox của con bị disable; hiển thị ngày mở form tiếp theo đã công bố. | `application form is closed (opens DD/MM/YYYY)` |
| **6. Nationality Display Specifics** | Con có quốc tịch là Singapore PR. | Bên cạnh thông tin con hiển thị huy hiệu nhãn màu tím/xanh nhạt báo trước con chỉ được xét diện SBFAS của trường. | Nhãn: `school SBFAS only` |
| **7. Multi-Child Mixed Selection** | Phụ huynh có 3 con: Con 1 (P3, đủ điều kiện), Con 2 (P6, đủ điều kiện), Con 3 (17 tuổi, bị khóa). | Phụ huynh tick chọn Con 1 và Con 2. Nút `Continue` bật sáng sau khi chọn quan hệ `Father`. | Chuyển tiếp thành công sang Bước 2 với 2 con đã chọn. |
| **8. Profile Immutability Protection** | Cố tình dùng inspect element để sửa trường Họ tên hoặc Email của phụ huynh tại Bước 1. | Các trường bị khóa với thuộc tính `readonly` và `disabled`; dữ liệu phụ huynh trên server được lấy trực tiếp từ session xác thực Singpass. | Ngăn chặn giả mạo thông tin. |
| **9. Save Draft & Exit at Step 1** | Chọn 1 con và quan hệ `Mother`, sau đó bấm `Save draft & exit`. | Bản nháp được lưu tại CSDL với trạng thái: `step 1 of 5 (Children)`; hiển thị Toast: `"Draft saved. You can continue later."`; chuyển về landing page. | Lưu nháp thành công. |
| **10. UI Health & Sticky Summary** | Cuộn trang xem danh sách nhiều con trên màn hình nhỏ. | Bố cục thẻ con hiển thị rõ ràng, checkbox có vùng click rộng; thanh công cụ Back / Continue cố định ở chân trang (sticky footer). | Đạt chuẩn Invariant 7 UI Health. |
| **11. Pristine / Dirty Transition** | Tick chọn hoặc bỏ chọn một đứa con. | Form chuyển trạng thái dirty; cập nhật số lượng con đang chọn trong bộ đếm tổng quan. | State phản hồi tức thì. |
| **12. Error Resiliency on MOE DB Lookup** | CSDL MOE Enrolment tạm thời mất kết nối khi nạp danh sách con. | Hiển thị error alert thân thiện kèm nút `Retry loading children`: `"Unable to load student records. Please refresh or try again later."`. | Chống crash trang web. |

---

## 4. Error Handling & Visual Feedback

- **Standard Messages**:
  - Thiếu quan hệ: `MSG-0001` - `"Select your relationship to the children"`
  - Con quá tuổi: `"turned 16, cannot apply"`
  - Đang có đơn chờ: `"already has an application under review"`
  - Form đóng: `"application form is closed (opens DD/MM/YYYY)"`
- **Visual Cues**:
  - Thẻ học sinh bị khóa có nền xám nhạt (`bg-gray-100 opacity-75 cursor-not-allowed`).
  - Nút `Continue` chuyển màu xanh dương sáng (`bg-blue-600`) khi thỏa mãn đủ 2 điều kiện.

---

## 5. JSON Fixtures Data Payload

```json
{
  "applicant_profile_mock": {
    "name": "Mdm Noor Aisha",
    "nric": "S8212345E",
    "dateOfBirth": "14/06/1982",
    "gender": "Female",
    "category": "Singapore Citizen",
    "nationality": "Malay",
    "phone": "98765432",
    "email": "noor.aisha@example.sg",
    "address": "Blk 888 Tampines St 81 #10-44, Singapore 520888"
  },
  "children_list_mock": [
    {
      "childId": "c1",
      "nric": "T1456789A",
      "name": "Nurul Huda Binte Mohd",
      "eaNumber": "EA-2014-00999",
      "school": "Tampines Primary School",
      "level": "Primary",
      "grade": "P6",
      "nationality": "Singapore Citizen",
      "isEligible": true
    },
    {
      "childId": "c2",
      "nric": "T1856789B",
      "name": "Muhammad Danial Bin Mohd",
      "eaNumber": "EA-2018-00888",
      "school": "Tampines Primary School",
      "level": "Primary",
      "grade": "P2",
      "nationality": "Singapore Citizen",
      "isEligible": true
    },
    {
      "childId": "c3",
      "nric": "T0956789C",
      "name": "Nurul Iman Binte Mohd",
      "eaNumber": "EA-2009-00777",
      "school": "Tampines Secondary School",
      "level": "Secondary",
      "grade": "S4",
      "nationality": "Singapore Citizen",
      "isEligible": false,
      "ineligibleReason": "turned 16, cannot apply"
    }
  ]
}
```
