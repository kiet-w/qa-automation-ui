# Component Specification: Documents Upload - Step 3 (`f10-documents-upload`)

> **Module**: `f10` - FAS Online Family Application Portal (Cổng Nộp Đơn FAS Phụ Huynh)  
> **Component**: `documents_upload` (Wizard Step 3: Supporting Documents & SBFAS Consideration)  
> **Source Spec**: `specs/md/FS document/FS-10_FAS_Family_Application_Portal.md` (Mục 6 Bước 3, Mục 11 BR5) & `specs/validation_rules/md/FS10_R10_FAS_Application_Validation (Draft).md`  
> **Target Audience**: Parent / Legal Guardian (Đăng nhập Singpass)  

---

## 1. Metadata & Selector

- **Route URL / Access Path**: e-Service Portal $\rightarrow$ Financial assistance $\rightarrow$ Apply for FAS $\rightarrow$ Step 3 (`/parent/fas/apply/step-3`)
- **Container Element Tag**: `<section id="fas-wizard-step-3" data-testid="wizard-step-3-documents">`
- **Playwright Locators (BSK Standardized Convention)**:

| Element Name | HTML Tag / Type | Playwright Locator (BSK Convention) | Description / Notes |
| :--- | :--- | :--- | :--- |
| **Step 3 Container** | `div` | `page.locator("div[data-testid='step-container-documents']")` | Step 3 wrapper |
| **Optional Notice Banner** | `div.alert-info` | `page.locator("div:has-text('Your income is verified with Government records')")` | Documents are optional |
| **Document File Input** | `input[type="file"]` | `page.locator("input[data-testid='input-supporting-doc'], input[type='file']")` | Accepts `.pdf, .jpg, .jpeg, .png` |
| **File Item in Staging** | `li / div` | `page.locator("li[data-testid^='doc-file-item-']")` | Uploaded document row |
| **Remove File Button** | `button` | `page.locator("button[data-testid^='btn-remove-doc-']")` | Deletes selected document |
| **Consider SBFAS Checkbox** | `input[type="checkbox"]` | `page.locator("input[data-testid='cb-consider-sbfas'], input[name='consider_sbfas']")` | Default checked; SBFAS consent |
| **Step 3 Back Button** | `button` | `page.locator("button[data-testid='btn-step3-back'], button:has-text('Back')")` | Navigates to Step 2 |
| **Step 3 Continue Button** | `button` | `page.locator("button[data-testid='btn-step3-continue'], button:has-text('Continue')")` | Always enabled (optional step) |

---

## 2. BR / AC Traceability

- **Functional Requirements**: `FS-10` Section 6 Step 3, Section 11 BR5.
- **Business Rules (BR)**:
  - `BR-10-DOC-01`: Việc tải tài liệu đính kèm là **hoàn toàn tùy chọn (optional)** vì thu nhập đã được xác thực tự động qua dữ liệu Chính phủ (CPF). Phụ huynh không bắt buộc phải tải bất kỳ tài liệu nào để tiếp tục.
  - `BR-10-DOC-02`: Định dạng tài liệu được chấp nhận: PDF hoặc ảnh (JPG, PNG).
  - `BR-10-DOC-03`: Giới hạn dung lượng tối đa **$5\text{ MB}$ mỗi file** ($5 \times 1024 \times 1024\text{ bytes} = 5,242,880\text{ bytes}$). File vượt quá $5\text{ MB}$ bị chặn tại client.
  - `BR-10-DOC-04`: Checkbox `"If my child is not eligible for MOEFAS, also consider them for the school's SBFAS"`:
    - **Mặc định được tick (Checked = true)**.
    - Cho phép con tự động chuyển tiếp hồ sơ sang trường xét duyệt SBFAS nếu không đủ điều kiện MOEFAS.
  - `BR-10-DOC-05`: Nút `Continue` luôn ở trạng thái bật (enabled) vì bước này là tùy chọn.
- **User Story Traceability**: `US-F10-04` (Tải giấy tờ hỗ trợ tùy chọn và đăng ký nguyện vọng SBFAS).
- **Access Control (RBAC)**: Phụ huynh học sinh.

---

## 3. Ma trận 12 lớp Validation

| Lớp Kiểm Thử (12 Tầng) | Điều Kiện / Dữ Liệu Đầu Vào | Kỳ Vọng Giao Diện & Hành Vi Hệ Thống | Mã Lỗi / Phản Hồi Trực Quan |
| :--- | :--- | :--- | :--- |
| **1. Empty / Optional Step** | Không tải bất kỳ tài liệu nào (0 file đính kèm), bấm `Continue`. | Hợp lệ hoàn toàn! Hệ thống cho phép chuyển tiếp sang Bước 4 mà không yêu cầu tài liệu. | Chuyển tiếp mượt sang Bước 4. |
| **2. BVA File Size Limits** | • File 1 byte: Hợp lệ.<br>• File $5\text{ MB}$ ($5,242,880\text{ bytes}$): Hợp lệ.<br>• File $5\text{ MB} + 1\text{ byte}$: Bị từ chối. | Hiển thị lỗi dung lượng; không thêm file vào danh sách đính kèm. | `{file} is larger than 5 MB.` |
| **3. Banned Extensions** | Kéo thả file `.docx`, `.xlsx`, `.zip`, `.exe`. | Từ chối ngay tại giao diện; chỉ chấp nhận PDF hoặc ảnh JPG/PNG. | `{file}: only PDF, JPG or PNG files.` |
| **4. Default SBFAS Checkbox** | Mở Bước 3 lần đầu tiên từ đơn mới. | Checkbox `Also consider for SBFAS` hiển thị trạng thái đã được tick (`checked="true"`). | Checkbox được bật mặc định. |
| **5. Uncheck SBFAS Intentional** | Phụ huynh cố tình bỏ tick checkbox SBFAS. | Hệ thống lưu giá trị `consider_sbfas = false`. Nếu sau này con không đạt chuẩn MOEFAS, đơn sẽ bị `Rejected` ngay chứ không chuyển tiếp sang trường. | Ghi nhận đúng ý định phụ huynh. |
| **6. Remove Uploaded Document** | Tải lên 2 file PDF, sau đó bấm nút `Remove` ở file thứ nhất. | File thứ nhất bị xóa khỏi danh sách; bộ đếm tài liệu cập nhật giảm tương ứng. | File biến mất khỏi DOM. |
| **7. Multi-File Selection** | Chọn cùng lúc 3 file ảnh hóa đơn y tế (mỗi file 1 MB). | Cả 3 file được thêm vào danh sách đính kèm hiển thị tên và dung lượng đầy đủ. | Danh sách hiển thị 3 file. |
| **8. XSS Payload in Document Name** | Tên file: `<script>alert('doc_xss')</script>.pdf`. | Tên file được escape an toàn thành chuỗi ký tự thường trong DOM; không thực thi script. | Render dạng text an toàn. |
| **9. Auto-Save on Navigation** | Tải 1 file PDF, bấm nút `Back` về Bước 2 rồi bấm `Continue` quay lại Bước 3. | File đã tải vẫn được giữ nguyên trong phiên làm việc, không bị mất dữ liệu. | State được bảo toàn. |
| **10. UI Health & Mobile Upload** | Bấm upload file từ trình duyệt di động iOS / Android. | Mở hộp thoại chọn camera / thư viện ảnh chuẩn; thanh tiến trình upload hiển thị trực quan; 0 console errors. | Đạt chuẩn Invariant 7 UI Health. |
| **11. Pristine / Dirty Detection** | Bỏ tick checkbox SBFAS hoặc thêm 1 file tài liệu mới. | Chuyển form sang dirty, cho phép lưu nháp qua nút `Save draft & exit`. | Kích hoạt dirty state. |
| **12. Corrupted File Handling** | Tải file PDF bị hỏng hoặc 0 byte. | Hệ thống phát hiện file rỗng hoặc hỏng và từ chối tải lên. | `{file}: the file is empty.` |

---

## 4. Error Handling & Visual Feedback

- **Standard Messages**:
  - Dung lượng quá lớn: `"{file} is larger than 5 MB."`
  - Sai định dạng: `"{file}: only PDF, JPG or PNG files."`
  - File rỗng: `"{file}: the file is empty."`
- **Visual Cues**:
  - File lỗi có viền đỏ nhạt và thông báo lỗi hiển thị ngay dưới khu vực dropzone.
  - File hợp lệ hiển thị thanh progress bar ngắn và icon thành công màu xanh lá.

---

## 5. JSON Fixtures Data Payload

```json
{
  "step3_valid_with_files": {
    "uploadedDocuments": [
      { "fileName": "medical_report_child.pdf", "fileSize": 1500000, "mimeType": "application/pdf" },
      { "fileName": "retrenchment_letter.png", "fileSize": 850000, "mimeType": "image/png" }
    ],
    "alsoConsiderSbfas": true
  },
  "step3_valid_no_files_default_sbfas": {
    "uploadedDocuments": [],
    "alsoConsiderSbfas": true
  },
  "step3_invalid_oversized_file": {
    "fileName": "large_scan.pdf",
    "fileSize": 5242881,
    "expectedErrorMessage": "large_scan.pdf is larger than 5 MB."
  }
}
```
