# Component Specification: Upload Scans Dialog (`f05-upload-scans-dialog`)

> **Module**: `f05` - FAS Paper Applications (Đơn giấy / Hardcopy Applications Offline)  
> **Component**: `upload_scans_dialog`  
> **Source Spec**: `specs/md/FS document/FS-05_Hardcopy_Applications_Offline.md` (Mục 4) & `specs/validation_rules/md/R5_FAS_APPLICATION_Validation_Rules.md` (Màn B: B1 - B4)  
> **Target Audience**: School User (School Admin)  

---

## 1. Metadata & Selector

- **Route URL / Access Path**: Admin Portal $\rightarrow$ Financial assistance $\rightarrow$ Upload applications $\rightarrow$ Click `Upload scans` button (`/admin/fas/paper-applications` modal `#upload-scans-dialog`)
- **Container Element Tag**: `<dialog role="dialog" aria-labelledby="upload-dialog-title" id="upload-scans-dialog">`
- **Playwright Locators (BSK Standardized Convention)**:

| Element Name | HTML Tag / Type | Playwright Locator (BSK Convention) | Description / Notes |
| :--- | :--- | :--- | :--- |
| **Modal Container** | `div[role="dialog"]` | `page.locator("div[role='dialog']:has-text('Upload scans')")` | Root dialog container |
| **Dialog Title** | `h2` | `page.locator("#upload-dialog-title, h2:has-text('Upload scans')")` | Header "Upload scans" |
| **Dropzone Area** | `div[role="button"]` | `page.locator("div[data-testid='file-dropzone'], .dropzone-area")` | Drag-and-drop file target area |
| **Hidden File Input** | `input[type="file"]` | `page.locator("input[data-testid='scan-file-input'], input[type='file']")` | Accepts `.pdf, .jpg, .jpeg, .png` |
| **Uploaded File Item** | `li / div` | `page.locator("li[data-testid^='uploaded-file-item-']")` | Row displaying file name & size |
| **File Remove Button** | `button` | `page.locator("button[data-testid='btn-remove-file']")` | Removes selected file from staging list |
| **Cancel Button** | `button` | `page.locator("button[data-testid='btn-cancel-upload'], button:has-text('Cancel')")` | Dismisses modal and clears queue |
| **Upload and Read Button** | `button` | `page.locator("button[data-testid='btn-upload-and-read'], button:has-text('Upload and read')")` | Starts OCR reading; disabled when 0 files |
| **Inline File Error Alert** | `div[role="alert"]` | `page.locator("div[data-testid='upload-error-alert'], .file-error-msg")` | Per-file rejection message |

---

## 2. BR / AC Traceability

- **Functional Requirements**: `FS-05` Section 1.1, Section 2 Step 1, Section 4 (Rules & Messages), Section 10 Scenario T1.
- **Business Rules (BR)**:
  - `BR-05-01`: Mỗi mẫu đơn in = một gia đình = một đơn cho mỗi con (lời nhắc hộp thoại: "One application per child").
  - `BR-05-FILE-01`: Chỉ chấp nhận các định dạng file scan tài liệu: PDF, JPG, PNG (không phân biệt hoa/thường).
  - `BR-05-FILE-02`: Giới hạn dung lượng tối đa $10\text{ MB}$ ($10 \times 1024 \times 1024\text{ bytes} = 10,485,760\text{ bytes}$) mỗi file. File lớn hơn $10\text{ MB}$ bị chặn ngay lập tức.
  - `BR-05-FILE-03`: Giới hạn số lượng tối đa 5 file scan cho một lần upload hồ sơ. File thứ 6 trở đi bị từ chối với thông báo "Up to 5 files per application."
- **User Story Traceability**: `US-F5-01` (School Admin tải scan đơn giấy FAS lên hệ thống để trích xuất OCR).
- **Access Control (RBAC)**: Chỉ dành cho `School User` (School Admin). `MOE HQ` và `Parent` không có quyền truy cập.

---

## 3. Ma trận 12 lớp Validation

| Lớp Kiểm Thử (12 Tầng) | Điều Kiện / Dữ Liệu Đầu Vào | Kỳ Vọng Giao Diện & Hành Vi Hệ Thống | Mã Lỗi / Thông Báo |
| :--- | :--- | :--- | :--- |
| **1. Empty / Required** | Không có file nào trong hàng chờ upload. | Nút `Upload and read` bị disable (`disabled="true"` hoặc `aria-disabled="true"`). Không gửi request. | Không có thông báo lỗi, nút xám mờ. |
| **2. Whitespace / Trim** | Tên file chứa khoảng trắng đầu/cuối hoặc nhiều dấu cách liên tiếp (ví dụ: `"  scan page 1 .pdf  "`). | Hệ thống trim chuẩn hóa tên file hiển thị, bảo toàn định dạng và dung lượng. | Chấp nhận bình thường. |
| **3. BVA Min/Max Size** | • 1 byte<br>• $10\text{ MB}$ ($10,485,760\text{ bytes}$)<br>• $10\text{ MB} + 1\text{ byte}$ ($10,485,761\text{ bytes}$)<br>• 0 byte (Empty file) | • 1 byte: Hợp lệ, thêm vào danh sách.<br>• $10\text{ MB}$: Hợp lệ, thêm vào danh sách.<br>• $10\text{ MB} + 1\text{ byte}$: Từ chối, hiện lỗi.<br>• 0 byte: Từ chối file rỗng. | • `{file} is larger than 10 MB.`<br>• `{file}: the file is empty.` |
| **4. Banned Formats** | Upload file có phần mở rộng `.docx`, `.xlsx`, `.gif`, `.tiff`, `.exe`, `.sh`, `.zip`. | Từ chối ngay tại client khi chọn/thả file, không đưa vào danh sách upload. | `{file}: only PDF, JPG or PNG files.` |
| **5. File Count Boundary** | • 1 file (Min boundary)<br>• 5 files (Max boundary)<br>• 6 files (Max + 1 boundary) | • 1 đến 5 files: Hợp lệ, nút `Upload and read` sáng bật.<br>• File thứ 6 trở đi: Chặn file thứ 6, giữ nguyên 5 files hợp lệ đầu tiên. | `Up to 5 files per application.` |
| **6. XSS / Payload in Filename** | Tên file chứa payload: `<script>alert(1)</script>.pdf`, `form" onerror="alert(1).png`, `../../etc/passwd.pdf`. | Tên file được escape và hiển thị dạng text thuần túy trong DOM; không parse HTML/JS. Loại bỏ directory traversal (`../`). | Hiển thị an toàn dưới dạng text node. |
| **7. Duplicate File Staging** | Chọn cùng 1 file 2 lần trong cùng một phiên upload (cùng tên, cùng checksum). | Bỏ qua lần chọn thứ hai hoặc thông báo file đã tồn tại trong danh sách. | `{file} is already added.` |
| **8. Multi-Extension Masquerading** | File có tên nguy hiểm: `application.pdf.exe`, `scan.php.jpg` nhưng MIME type thực là thực thi hoặc script. | Kiểm tra Magic Bytes / Signature header thực tế của file; từ chối file nếu không phải PDF/JPG/PNG. | `{file}: only PDF, JPG or PNG files.` |
| **9. Extended Controls & Removal** | Bấm nút `Remove` bên cạnh một dòng file đã chọn. | File bị xóa khỏi danh sách; dung lượng tổng và counter file giảm tương ứng. Nếu xóa hết file, nút `Upload and read` tự động chuyển sang disabled. | File biến mất khỏi DOM; `upload-and-read` disabled. |
| **10. UI Health & Responsive Layout** | • Kéo thả file trực tiếp vào dropzone.<br>• Mở trên màn hình chuẩn 1920x1080 và 1366x768. | • Dropzone đổi viền đứt nét highlight xanh lá khi kéo file hover.<br>• Hộp thoại căn giữa, không có thanh cuộn ngang (0 horizontal scrollbar), 0 console errors. | Đạt chuẩn Invariant 7 UI Health. |
| **11. Pristine / Dirty Lifecycle** | Bấm nút `Cancel` hoặc icon `✕` đóng dialog khi đã chọn file. | Modal đóng, danh sách file chờ bị hủy hoàn toàn (reset pristine state); danh sách đơn giấy bên dưới không bị ảnh hưởng. | State reset về pristine. |
| **12. Network / Server Failure Resilience** | Bấm `Upload and read` nhưng API mock hoặc backend trả về timeout / HTTP 500. | Không crash ứng dụng; hiện error banner trong modal, giữ nguyên danh sách file để người dùng bấm thử lại mà không phải chọn file lại từ đầu. | `Something went wrong. Please try again.` |

---

## 4. Error Handling & Visual Feedback

- **Standard Messages**:
  - Sai định dạng file: `"{file}: only PDF, JPG or PNG files."`
  - Dung lượng vượt quá $10\text{ MB}$: `"{file} is larger than 10 MB."`
  - Vượt quá 5 files: `"Up to 5 files per application."`
  - File rỗng 0 byte: `"{file}: the file is empty."`
  - Lỗi máy chủ / OCR thất bại: `"Something went wrong. Please try again."`
- **Visual Cues**:
  - Hàng file bị lỗi hiển thị viền đỏ nhạt (`border-color: #D9383A`) và icon cảnh báo `⚠️`.
  - Nút `Upload and read` hiển thị spinner loading state `"Reading application..."` trong thời gian giả lập OCR và bị khóa chống double-click.

---

## 5. JSON Fixtures Data Payload

```json
{
  "valid_payloads": {
    "single_pdf": {
      "fileName": "FAS_Form_Application_2026_LeeFamily.pdf",
      "fileSize": 1048576,
      "mimeType": "application/pdf"
    },
    "max_allowed_batch_5_files": [
      { "fileName": "page1_applicant.jpg", "fileSize": 850000, "mimeType": "image/jpeg" },
      { "fileName": "page2_children.png", "fileSize": 920000, "mimeType": "image/png" },
      { "fileName": "page3_household.jpg", "fileSize": 810000, "mimeType": "image/jpeg" },
      { "fileName": "page4_context.png", "fileSize": 790000, "mimeType": "image/png" },
      { "fileName": "page5_declaration.pdf", "fileSize": 1200000, "mimeType": "application/pdf" }
    ],
    "exact_boundary_10mb": {
      "fileName": "boundary_exact_10mb.pdf",
      "fileSize": 10485760,
      "mimeType": "application/pdf"
    }
  },
  "invalid_payloads": {
    "unsupported_extensions": [
      { "fileName": "scanned_doc.docx", "fileSize": 500000, "mimeType": "application/vnd.openxmlformats-officedocument.wordprocessingml.document" },
      { "fileName": "malicious_script.sh", "fileSize": 1200, "mimeType": "application/x-sh" },
      { "fileName": "scanned_image.tiff", "fileSize": 2500000, "mimeType": "image/tiff" }
    ],
    "oversized_file_10mb_plus_1b": {
      "fileName": "oversized_application.pdf",
      "fileSize": 10485761,
      "mimeType": "application/pdf",
      "expectedMessage": "oversized_application.pdf is larger than 10 MB."
    },
    "empty_file_0b": {
      "fileName": "corrupted_empty.png",
      "fileSize": 0,
      "mimeType": "image/png",
      "expectedMessage": "corrupted_empty.png: the file is empty."
    },
    "exceed_5_files_attempt": {
      "fileCount": 6,
      "expectedMessage": "Up to 5 files per application."
    },
    "xss_filename": {
      "fileName": "<script>alert(document.cookie)</script>.pdf",
      "fileSize": 512000,
      "mimeType": "application/pdf"
    }
  }
}
```
