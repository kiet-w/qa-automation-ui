# Component Specification: Review Before Submitting Dialog (`f05-review-before-submit-dialog`)

> **Module**: `f05` - FAS Paper Applications (Đơn giấy / Hardcopy Applications Offline)  
> **Component**: `review_before_submit_dialog` (Screen E: Modal Review Before Submitting)  
> **Source Spec**: `specs/md/FS document/FS-05_Hardcopy_Applications_Offline.md` (Mục 7, Mục 9 BR1, BR7, BR8, Mục 10 T10) & `specs/validation_rules/md/R5_FAS_APPLICATION_Validation_Rules.md` (Màn E: E1 - E6, Màn D: VR-F5-10)  
> **Target Audience**: School User (School Admin)  

---

## 1. Metadata & Selector

- **Route URL / Access Path**: Admin Portal $\rightarrow$ Financial assistance $\rightarrow$ Upload applications $\rightarrow$ Review application $\rightarrow$ Click `Review and submit` (`/admin/fas/paper-applications/review/:id` modal `#review-before-submit-dialog`)
- **Container Element Tag**: `<dialog role="dialog" aria-labelledby="review-dialog-title" id="review-before-submit-dialog">`
- **Playwright Locators (BSK Standardized Convention)**:

| Element Name | HTML Tag / Type | Playwright Locator (BSK Convention) | Description / Notes |
| :--- | :--- | :--- | :--- |
| **Modal Container** | `div[role="dialog"]` | `page.locator("div[role='dialog']:has-text('Review before submitting')")` | Root modal dialog element |
| **Dialog Subtitle** | `p.subtitle` | `page.locator("p:has-text('One application per child. MOEFAS is assessed automatically')")` | Mandatory subtitle notice |
| **Applicant Summary Block** | `section` | `page.locator("section[data-testid='review-section-applicant'], #review-applicant")` | Field E1; applicant details summary |
| **Children Summary Block** | `section` | `page.locator("section[data-testid='review-section-children'], #review-children")` | Field E2; lists all children applying |
| **Household Summary Block** | `section` | `page.locator("section[data-testid='review-section-household'], #review-household")` | Field E3; size, GHI, PCI summary |
| **Context Summary Block** | `section` | `page.locator("section[data-testid='review-section-context'], #review-context")` | Field E4; context text or fallback |
| **Back to Edit Button** | `button` | `page.locator("button[data-testid='btn-back-to-edit'], button:has-text('Back to edit')")` | Field E5; returns to Screen C |
| **Confirm and Submit Button** | `button` | `page.locator("button[data-testid='btn-confirm-and-submit'], button:has-text('Confirm and submit')")` | Field E6; triggers final submission |
| **Submission Toast Notification** | `div[role="status"]` | `page.locator("div[role='status']:has-text('submitted')")` | Toast on successful creation |

---

## 2. BR / AC Traceability

- **Functional Requirements**: `FS-05` Section 2 Steps 4-5, Section 7 Summary Details, Section 9 BR1, BR7, BR8, Section 10 Scenario T10.
- **Business Rules (BR)**:
  - `BR-05-SUB-01`: Bắt buộc phải qua bước Review before submitting trước khi tạo đơn chính thức (`BR7`). Không được submit trực tiếp bỏ qua bước này.
  - `BR-05-SUB-02`: Một mẫu đơn in = một gia đình = **tạo một đơn cho mỗi con** (nguồn `Paper`; dùng chung một mã gia đình `FAM-YYYY-NNNNN` khi có từ 2 con trở lên) (`BR1`).
  - `BR-05-SUB-03`: Phân luồng nghiệp vụ theo quy tắc Chức năng 4 (`BR8`):
    - Con có quốc tịch Singapore Citizen: Gắn với scheme MOEFAS đang mở, trạng thái `Pending` (System check `"Waiting"`) cho đến khi form MOEFAS đóng; sau đó tự động xếp hạng và duyệt.
    - Con không đủ điều kiện quốc tịch MOEFAS (ví dụ PR, Quốc tế): Chuyển thành `SBFAS Pending` ngay lúc nộp và gửi về cho trường của con xử lý.
  - `BR-05-SUB-04`: Bản nháp (`Draft`) của hồ sơ này bị **xóa hoàn toàn** khỏi hệ thống sau khi nộp thành công (`BR6`).
  - `BR-05-SUB-05`: Hiển thị Toast thông báo:
    - 1 con: `"Application submitted for assessment."`
    - Từ 2 con trở lên: `"Applications submitted."`
  - `VR-F5-10`: Server-side re-check: Hệ thống tự động kiểm tra lại toàn bộ quy tắc hợp lệ (form mở, trùng NRIC, tuổi) trước khi commit transaction lưu CSDL.
- **User Story Traceability**: `US-F5-08` (Xem lại tổng quan và xác nhận nộp đơn giấy FAS).
- **Access Control (RBAC)**: Chỉ School User (School Admin).

---

## 3. Ma trận 12 lớp Validation

| Lớp Kiểm Thử (12 Tầng) | Điều Kiện / Dữ Liệu Đầu Vào | Kỳ Vọng Giao Diện & Hành Vi Hệ Thống | Mã Lỗi / Phản Hồi Trực Quan |
| :--- | :--- | :--- | :--- |
| **1. Data Integrity Reflection** | Đối chiếu thông tin giữa Form nhập (Màn C) và Hộp thoại Review (Màn E). | Hiển thị chính xác 100% các giá trị đã nhập: Họ tên phụ huynh, NRIC, Category, Nationality, Phone, Email, danh sách con, số EA, quy mô hộ, GHI, PCI, Context. | Khớp hoàn toàn từng trường. |
| **2. Multi-Child Header Count** | Hồ sơ gồm 2 con học sinh. | Tiêu đề danh sách con hiển thị rõ: `Children (2)`. Mỗi con hiển thị một thẻ tóm tắt riêng biệt. | Hiển thị `Children (2)` chuẩn xác. |
| **3. Back to Edit Interaction** | Bấm nút `Back to edit` (E5). | Hộp thoại E đóng lại ngay lập tức. Không lưu dữ liệu mới; không tạo đơn; toàn bộ dữ liệu trên màn hình Review (Màn C) giữ nguyên trạng thái. | Quay về Màn C an toàn. |
| **4. Double-Click Debouncing** | Người dùng bấm đúp nhanh (double click) vào nút `Confirm and submit` (E6). | Nút lập tức chuyển sang trạng thái disabled và hiển thị loading spinner `"Submitting..."`. Chỉ gửi duy nhất 1 request HTTP lên máy chủ; không tạo đơn trùng lặp. | Chống duplicate transaction tuyệt đối. |
| **5. Single Child Submission Flow** | Hồ sơ có 1 con là công dân Singapore (SC). Bấm `Confirm and submit`. | Tạo 1 đơn FAS (nguồn Paper); trạng thái `Pending`; xóa bản nháp; đóng modal; chuyển về danh sách và hiện Toast thông báo 1 đơn. | Toast: `Application submitted for assessment.` |
| **6. Multi-Child Submission Flow** | Hồ sơ có 2 con (1 SC, 1 PR). Bấm `Confirm and submit` (Scenario T10). | Tạo 2 đơn dùng chung mã gia đình `FAM-2026-00088`. Đơn con SC là MOEFAS Pending; đơn con PR là SBFAS Pending gửi về trường con; hiện Toast số nhiều. | Toast: `Applications submitted.` |
| **7. Server Re-Check Collision (Form Closed)** | Form FAS bị đóng bởi Admin MOE ngay trước thời điểm người dùng bấm `Confirm and submit`. | Server phát hiện form đã đóng; hủy transaction; không tạo đơn; modal giữ nguyên và hiện thông báo lỗi đỏ. | `{tên}: the FAS application form is closed.` |
| **8. Concurrent Duplicate Submission** | Một người dùng khác nộp đơn cho cùng một học sinh trong lúc hộp thoại E đang mở. | Server phát hiện trùng đơn trong năm hiện tại; từ chối tạo đơn mới. | `{tên} already has an application this year ({id}, {status}).` |
| **9. Draft Cleanup Verification** | Sau khi nộp thành công, kiểm tra danh sách đơn (Màn A). | Dòng Draft tương ứng biến mất hoàn toàn khỏi bảng dữ liệu; thay vào đó là các dòng đơn mới nộp với mã Application ID chính thức. | Draft đã bị xóa sạch (BR6). |
| **10. UI Health & Modal Contrast** | Modal mở lên trên nền backdrop tối (`backdrop-blur-sm bg-black/50`). | Modal căn giữa màn hình; nội dung có thanh cuộn dọc nếu dài; đáp ứng WCAG 2.1 AA contrast ratio $\ge 4.5:1$; 0 console errors. | Đạt chuẩn Invariant 7 UI Health. |
| **11. Context Presentation** | • Trường hợp có nhập context 300 ký tự.<br>• Trường hợp không nhập context (0 ký tự). | • Có context: Hiển thị nguyên văn bản thuần túy.<br>• Không có context: Hiển thị dòng chữ xám nhạt `No context given.` | Hiển thị đúng ngữ cảnh. |
| **12. Network Failure Resilience** | Bấm `Confirm and submit` nhưng mạng bị rớt (Offline / HTTP 504 Gateway Timeout). | Hộp thoại không đóng; không mất dữ liệu; hiển thị thông báo lỗi để người dùng có thể bấm submit lại khi mạng phục hồi. | `Something went wrong. Please try again.` |

---

## 4. Error Handling & Visual Feedback

- **Standard Messages**:
  - Toast nộp 1 đơn thành công: `"Application submitted for assessment."`
  - Toast nộp nhiều đơn thành công: `"Applications submitted."`
  - Lỗi máy chủ / mạng: `"Something went wrong. Please try again."`
  - Bị chặn do form đóng: `"{tên}: the FAS application form is closed (next opens DD/MM/YYYY)."`
  - Bị chặn do trùng đơn: `"{tên} already has an application this year ({id}, {status})."`
- **Visual Cues**:
  - Nút `Confirm and submit` có màu xanh dương chủ đạo (`bg-blue-600 hover:bg-blue-700 text-white`).
  - Toast thông báo thành công xuất hiện ở góc trên bên phải màn hình (`fixed top-4 right-4 z-50`), tự động ẩn sau 4 giây.

---

## 5. JSON Fixtures Data Payload

```json
{
  "submission_single_child_payload": {
    "applicant": {
      "nric": "S7512345Z",
      "fullName": "Tan Ah Seng",
      "relationship": "Father",
      "contact": "91234567 | ahseng.tan@example.com",
      "alsoConsiderSbfas": true
    },
    "children": [
      {
        "childNric": "T1412345B",
        "fullName": "Tan Mei Ling",
        "school": "Bedok Green Primary School",
        "grade": "P6",
        "className": "Primary 6 Compassion",
        "eaNumber": "EA-2014-00123"
      }
    ],
    "household": {
      "householdSize": 3,
      "grossHouseholdIncome": "S$ 2,400.00",
      "perCapitaIncome": "S$ 800.00"
    },
    "expectedToast": "Application submitted for assessment."
  },
  "submission_two_children_shared_family_payload": {
    "applicant": {
      "nric": "S7512345Z",
      "fullName": "Tan Ah Seng",
      "relationship": "Father",
      "alsoConsiderSbfas": true
    },
    "children": [
      {
        "childNric": "T1412345B",
        "fullName": "Tan Mei Ling",
        "nationality": "Singapore Citizen",
        "expectedRouting": "MOEFAS Pending (Waiting)"
      },
      {
        "childNric": "T1798765C",
        "fullName": "Tan Jun Jie",
        "nationality": "Singapore PR",
        "expectedRouting": "SBFAS Pending (Sent to school)"
      }
    ],
    "expectedFamilyCodePrefix": "FAM-2026-",
    "expectedToast": "Applications submitted."
  }
}
```
