# Component Specification: Declaration & Signature - Part 5 (`f05-declaration-signature`)

> **Module**: `f05` - FAS Paper Applications (Đơn giấy / Hardcopy Applications Offline)  
> **Component**: `declaration_signature` (Review Application Screen - Part 5: Declaration)  
> **Source Spec**: `specs/md/FS document/FS-05_Hardcopy_Applications_Offline.md` (Mục 5, Mục 6, Mục 10 T8) & `specs/validation_rules/md/R5_FAS_APPLICATION_Validation_Rules.md` (Màn C: C22 - C26, Màn D: VR-F5-01)  
> **Target Audience**: School User (School Admin)  

---

## 1. Metadata & Selector

- **Route URL / Access Path**: Admin Portal $\rightarrow$ Financial assistance $\rightarrow$ Upload applications $\rightarrow$ Review application (`/admin/fas/paper-applications/review/:id` or `#part-5-declaration`)
- **Container Element Tag**: `<fieldset id="part-5-declaration" data-testid="section-part-5-declaration" aria-labelledby="heading-part-5">`
- **Playwright Locators (BSK Standardized Convention)**:

| Element Name | HTML Tag / Type | Playwright Locator (BSK Convention) | Description / Notes |
| :--- | :--- | :--- | :--- |
| **Section Header** | `h3` | `page.locator("h3:has-text('Part 5 · Declaration')")` | Section 5 Header |
| **Declaration Checkbox** | `input[type="checkbox"]` | `page.locator("input[data-testid='cb-declaration-agreement'], input[name='declaration_agreement']")` | Field C22; required tick |
| **Signature Checked Checkbox** | `input[type="checkbox"]` | `page.locator("input[data-testid='cb-applicant-signature'], input[name='signature_checked']")` | Field C23; required tick |
| **Date Signed Input** | `input[type="text"]` | `page.locator("input[data-testid='input-date-signed'], input[name='date_signed']")` | Field C25; required date `DD/MM/YYYY` |
| **Received By Display** | `input[type="text"]` | `page.locator("input[data-testid='display-received-by'], [data-testid='field-received-by']")` | Field C24; read-only (School User name) |
| **Date Received Display** | `input[type="text"]` | `page.locator("input[data-testid='display-date-received'], [data-testid='field-date-received']")` | Field C26; read-only (Today's date) |
| **Top Error Alert** | `div[role="alert"]` | `page.locator("div[data-testid='submit-blocked-alert']")` | Banner displaying missing items |

---

## 2. BR / AC Traceability

- **Functional Requirements**: `FS-05` Section 5 Part 5, Section 6 Validation, Section 10 Scenario T8.
- **Business Rules (BR)**:
  - `BR-05-DEC-01`: Ô xác nhận cam kết (`Declaration ticked`) là **bắt buộc** phải tick.
  - `BR-05-DEC-02`: Ô xác nhận chữ ký của phụ huynh (`Applicant's signature checked`) là **bắt buộc** phải tick để chứng nhận School User đã kiểm tra thấy chữ ký thật của phụ huynh trên bản scan.
  - `BR-05-DEC-03`: Ngày ký (`Date signed`) là bắt buộc, định dạng chuẩn `DD/MM/YYYY`, không được là ngày trong tương lai so với ngày tiếp nhận.
  - `BR-05-DEC-04`: Người tiếp nhận (`Received by`) tự động gán theo tài khoản School User đang đăng nhập, ở chế độ chỉ đọc (read-only).
  - `BR-05-DEC-05`: Ngày tiếp nhận (`Date received`) tự động lấy ngày hiện tại của hệ thống (today), ở chế độ chỉ đọc (read-only).
- **User Story Traceability**: `US-F5-06` (Xác thực chữ ký đơn giấy và hoàn tất cam kết pháp lý).
- **Access Control (RBAC)**: Chỉ School User của trường học sinh.

---

## 3. Ma trận 12 lớp Validation

| Lớp Kiểm Thử (12 Tầng) | Điều Kiện / Dữ Liệu Đầu Vào | Kỳ Vọng Giao Diện & Hành Vi Hệ Thống | Mã Lỗi / Phản Hồi Trực Quan |
| :--- | :--- | :--- | :--- |
| **1. Empty / Required All** | Chưa tick Declaration, chưa tick Signature, để trống Date signed. | Bị chặn mở dialog Review; hiện thông báo đỏ ở đầu trang liệt kê cả 3 trường. | `Complete: Declaration, Applicant signature checked, Date signed.` |
| **2. Single Missing Checkbox (Signature)** | Đã tick Declaration, nhập Date signed hợp lệ, nhưng **chưa tick Signature checked** (Scenario T8). | Bị chặn nộp đơn; thông báo chính xác trường chữ ký chưa được kiểm tra. | `Complete: Applicant signature checked.` |
| **3. Single Missing Checkbox (Declaration)** | Đã tick Signature, nhập Date signed, nhưng chưa tick Declaration. | Bị chặn nộp đơn. | `Complete: Declaration.` |
| **4. Date Format Validation** | Nhập ngày ký sai cấu trúc (ví dụ: `31-02-2026`, `2026/12/01`, `text`, `32/01/2026`). | Bị từ chối; yêu cầu nhập đúng ngày thực tế hợp lệ theo chuẩn `DD/MM/YYYY`. | Báo lỗi ngày không hợp lệ. |
| **5. BVA Date Limits (Future Date)** | • Ngày ký = Hôm nay (`Date received`): Hợp lệ.<br>• Ngày ký = Hôm qua: Hợp lệ.<br>• Ngày ký = Ngày mai (Tương lai): Bị chặn. | Ngày ký của phụ huynh trên giấy phải nhỏ hơn hoặc bằng ngày tiếp nhận đơn của trường. | `Date signed cannot be in the future.` |
| **6. Read-Only Immutability (Received by)** | Cố gắng can thiệp sửa trường `Received by` qua DevTools hoặc DOM script. | Trường có thuộc tính `readonly="true"` và `disabled="true"`; backend chỉ chấp nhận user session ID từ token xác thực. | Giá trị không thể bị giả mạo. |
| **7. Read-Only Immutability (Date received)** | Cố gắng sửa ngày tiếp nhận đơn `Date received`. | Giá trị được khóa chặt bởi hệ thống; luôn hiển thị ngày hiện tại của máy chủ (Singapore UTC+8). | Không thể sửa đổi. |
| **8. Extended Controls (Keyboard Toggle)** | Dùng phím `Space` hoặc `Enter` khi focus vào các checkbox Declaration và Signature. | Checkbox chuyển đổi trạng thái `checked` $\leftrightarrow$ `unchecked` mượt mà, hỗ trợ chuẩn accessibility WCAG 2.1. | Toggle chính xác, visual focus outline rõ. |
| **9. Draft State Persistence** | Tick cả 2 checkbox, nhập Date signed, rồi bấm `Save draft`. Mở lại đơn từ danh sách bằng `Continue`. | Trạng thái của cả 2 checkbox và ngày ký được phục hồi nguyên vẹn từ bản nháp. | Khôi phục 100% state đã lưu. |
| **10. UI Health & Visual Alignment** | Kiểm tra hiển thị của Part 5 ở cuối trang Review application. | Checkbox có nhãn (label) bấm được; khoảng cách đồng đều; không bị che khuất bởi thanh công cụ cố định (sticky bottom bar). | Giao diện rõ ràng, đạt chuẩn Invariant 7. |
| **11. Pristine / Dirty Detection** | Bấm tick vào ô Declaration trên form vừa mở. | Chuyển form sang trạng thái dirty; bật nút `Save draft`. | Dirty state được kích hoạt. |
| **12. Submission Synchronization** | Khi tất cả Part 1 đến Part 5 đều hợp lệ và người dùng bấm `Review and submit`. | Các ghi chú đỏ biến mất hoàn toàn; mở ngay lập tức hộp thoại Màn E (`Review before submitting`). | Chuyển tiếp mượt sang Màn E. |

---

## 4. Error Handling & Visual Feedback

- **Standard Messages**:
  - Chưa tick cam kết: `"Complete: Declaration."`
  - Chưa kiểm tra chữ ký: `"Complete: Applicant signature checked."`
  - Chưa nhập ngày ký: `"Complete: Date signed."`
  - Ngày ký trong tương lai: `"Date signed cannot be in the future."`
- **Visual Cues**:
  - Hộp thông báo màu đỏ ở đỉnh trang Review (`bg-red-50 text-red-800 border-red-500`).
  - Ô checkbox hoặc input bị thiếu có `aria-invalid="true"` và viền đỏ bao quanh.

---

## 5. JSON Fixtures Data Payload

```json
{
  "valid_declaration_payload": {
    "declarationChecked": true,
    "signatureChecked": true,
    "dateSigned": "25/10/2026",
    "receivedBy": "Mdm Tan Siew Ling (Bedok Green Primary School)",
    "dateReceived": "26/10/2026"
  },
  "invalid_missing_signature_payload": {
    "declarationChecked": true,
    "signatureChecked": false,
    "dateSigned": "25/10/2026",
    "expectedErrorMessage": "Complete: Applicant signature checked."
  },
  "invalid_missing_all_payload": {
    "declarationChecked": false,
    "signatureChecked": false,
    "dateSigned": "",
    "expectedErrorMessage": "Complete: Declaration, Applicant signature checked, Date signed."
  },
  "invalid_future_date_payload": {
    "declarationChecked": true,
    "signatureChecked": true,
    "dateSigned": "30/12/2026",
    "expectedErrorMessage": "Date signed cannot be in the future."
  }
}
```
