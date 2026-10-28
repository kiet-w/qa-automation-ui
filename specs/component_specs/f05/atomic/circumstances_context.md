# Component Specification: Circumstances & Context - Part 4 (`f05-circumstances-context`)

> **Module**: `f05` - FAS Paper Applications (Đơn giấy / Hardcopy Applications Offline)  
> **Component**: `circumstances_context` (Review Application Screen - Part 4: Circumstances and wishes)  
> **Source Spec**: `specs/md/FS document/FS-05_Hardcopy_Applications_Offline.md` (Mục 5, Mục 9 BR5, Mục 10 T11) & `specs/validation_rules/md/R5_FAS_APPLICATION_Validation_Rules.md` (Màn C: C21)  
> **Target Audience**: School User (School Admin)  

---

## 1. Metadata & Selector

- **Route URL / Access Path**: Admin Portal $\rightarrow$ Financial assistance $\rightarrow$ Upload applications $\rightarrow$ Review application (`/admin/fas/paper-applications/review/:id` or `#part-4-context`)
- **Container Element Tag**: `<fieldset id="part-4-context" data-testid="section-part-4-context" aria-labelledby="heading-part-4">`
- **Playwright Locators (BSK Standardized Convention)**:

| Element Name | HTML Tag / Type | Playwright Locator (BSK Convention) | Description / Notes |
| :--- | :--- | :--- | :--- |
| **Section Header** | `h3` | `page.locator("h3:has-text('Part 4 · Circumstances and wishes')")` | Section 4 Title |
| **Context Textarea** | `textarea` | `page.locator("textarea[data-testid='input-application-context'], textarea[name='application_context']")` | Field C21; up to 2000 characters |
| **Character Counter** | `span / div` | `page.locator("[data-testid='context-char-counter'], .char-counter")` | Live counter "n / 2000" |
| **Placeholder Text** | `textarea[placeholder]` | `page.locator("textarea[placeholder*='circumstances']")` | Guide prompt matching paper form |

---

## 2. BR / AC Traceability

- **Functional Requirements**: `FS-05` Section 5 Part 4, Section 7 Part 4 Context, Section 9 BR5, Section 10 Scenario T11.
- **Business Rules (BR)**:
  - `BR-05-CTX-01`: Trường Context là **tùy chọn (optional)**, văn bản thuần (plain text), tối đa $2000$ ký tự.
  - `BR-05-CTX-02`: Được nhập đúng y nguyên như phụ huynh viết trên mẫu đơn in giấy.
  - `BR-05-CTX-03`: Nội dung Context được lưu trữ vĩnh viễn kèm theo hồ sơ của từng con và hiển thị tại:
    1. Hộp thoại `Review before submitting` (Màn E).
    2. Chi tiết đơn FAS của người xét đơn tại Chức năng 4 (`Function 4 Drawer -> Context`).
- **User Story Traceability**: `US-F5-05` (Ghi nhận hoàn cảnh đặc biệt và nguyện vọng trợ cấp từ mẫu đơn giấy).
- **Access Control (RBAC)**: School User nhập liệu; School Admin và MOE HQ có quyền đọc tại F4.

---

## 3. Ma trận 12 lớp Validation

| Lớp Kiểm Thử (12 Tầng) | Điều Kiện / Dữ Liệu Đầu Vào | Kỳ Vọng Giao Diện & Hành Vi Hệ Thống | Mã Lỗi / Phản Hồi Trực Quan |
| :--- | :--- | :--- | :--- |
| **1. Empty / Optional** | Bỏ trống ô Context (0 ký tự). | Hợp lệ hoàn toàn; không kích hoạt lỗi hay chặn nộp đơn. | Không có thông báo lỗi; cho phép submit. |
| **2. Whitespace Only** | Nhập toàn dấu cách hoặc xuống dòng liên tiếp (`"   \n\n   "`). | Coi như để trống hoặc trim lại thành chuỗi rỗng khi lưu; không gây lỗi. | Không có lỗi. |
| **3. BVA Boundary Limits** | • 1 ký tự (Min boundary)<br>• 1,999 ký tự (Normal)<br>• 2,000 ký tự (Max boundary)<br>• 2,001 ký tự (Max + 1 boundary) | • 1 đến 2,000 ký tự: Hợp lệ.<br>• 2,001 ký tự: Trình duyệt chặn nhập tiếp (thuộc tính `maxlength="2000"`) hoặc hiện cảnh báo vượt giới hạn. | Bộ đếm hiện `2000 / 2000`. Cảnh báo nếu vượt quá. |
| **4. Special & Multilingual Characters** | Nhập ký tự có dấu tiếng Việt, chữ Hán, Tamil, Malay, ký hiệu toán học, emoji: `"Mẹ đơn thân 2 con, 需救助, வணக்கம், 👨‍👩‍👧"`. | Lưu trữ và hiển thị chính xác dưới dạng chuỗi UTF-8 Unicode đa ngôn ngữ. | Hiển thị trung thực 100%. |
| **5. Line Breaks & Formatting** | Nhập nhiều đoạn văn có ký tự xuống dòng (`\n`) và thụt đầu dòng (`\t`). | Bảo toàn cấu trúc xuống dòng; loại bỏ các ký tự điều khiển nguy hiểm (U+0000 đến U+001F ngoại trừ tab và newline). | Giữ nguyên format văn bản. |
| **6. XSS & Code Injection Vectors** | Nhập payload HTML/JS: `<script>document.location='http://attacker.com'</script>`, `<img src=x onerror=alert(1)>`, `{{7*7}}`. | Lưu dạng plain text; khi render ra HTML ở màn E hoặc F4 drawer, tất cả thẻ HTML được escape an toàn (thành `&lt;script&gt;...`); không thực thi mã. | Render an toàn dưới dạng văn bản thường. |
| **7. SQL / Query Injection Vectors** | Nhập: `' OR '1'='1' --`, `'; DROP TABLE applications; --`. | Hệ thống xử lý qua Prepared Statements / ORM tham số hóa; không làm sai lệch truy vấn CSDL. | Lưu an toàn như văn bản thường. |
| **8. Real-time Counter Synchronization** | Người dùng gõ hoặc dán (paste) một đoạn văn bản vào ô. | Bộ đếm ký tự (`n / 2000`) tự động cập nhật ngay lập tức theo số lượng ký tự thực tế trong textarea. | Counter nhảy số đồng bộ tức thì. |
| **9. Draft Persistence Across Steps** | Nhập 500 ký tự context rồi bấm `Save draft`. Sau đó bấm `Continue` từ danh sách. | Toàn bộ 500 ký tự context được khôi phục nguyên vẹn, không bị mất ký tự nào (Test T11). | Dữ liệu khôi phục chuẩn xác. |
| **10. UI Health & Textarea Resizing** | Textarea có kích thước tối thiểu 4 dòng; hỗ trợ cuộn dọc tự động khi văn bản dài. | Không tạo thanh cuộn ngang (zero horizontal scrollbar); không làm vỡ bố cục 2 cột (bản scan bên trái, form bên phải). | Đạt chuẩn Invariant 7 UI Health. |
| **11. Read-Only Reflection in Review Modal** | Sau khi nhập context, bấm `Review and submit`. | Nội dung context hiển thị nguyên vẹn tại mục Part 4 của hộp thoại Màn E. Nếu không nhập context, hiển thị `No context given.` | Hiển thị đúng giá trị tại Modal Review. |
| **12. Error Recovery & Auto-Save** | Mất kết nối mạng đột ngột khi đang nhập context. | Văn bản được giữ nguyên trong bộ nhớ client / LocalStorage, không bị xóa trắng khi mạng khôi phục. | Bảo toàn dữ liệu người dùng. |

---

## 4. Error Handling & Visual Feedback

- **Standard Messages**:
  - Vượt quá $2000$ ký tự: `"Context cannot exceed 2000 characters."`
  - Nếu không có context (khi xem lại): `"No context given."`
- **Visual Cues**:
  - Bộ đếm ký tự chuyển màu cam khi đạt từ 1,900 ký tự trở lên (`text-amber-600`) và màu đỏ khi đạt giới hạn 2,000 ký tự (`text-red-600 font-semibold`).

---

## 5. JSON Fixtures Data Payload

```json
{
  "valid_context_sample": {
    "contextText": "Applicant is currently undergoing medical treatment for chronic illness and working part-time. Family relies on irregular freelance income. Seeking assistance for school fees, textbooks, and transport subsidies for both children attending Primary and Secondary school.",
    "characterCount": 268
  },
  "boundary_2000_chars_payload": {
    "contextText": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. ".repeat(35).slice(0, 2000),
    "characterCount": 2000
  },
  "multilingual_and_special_chars": {
    "contextText": "Family circumstance: Single parent family. Mẹ đơn thân nuôi 2 con nhỏ. 父亲因病丧失劳动力。Seeking FAS support for AY2026/2027. Special dietary needs for younger child.",
    "characterCount": 164
  },
  "xss_injection_payload": {
    "contextText": "Testing XSS resistance: <script>alert('FAS_AUDIT')</script><svg onload=alert(1)>' OR '1'='1"
  },
  "empty_optional_payload": {
    "contextText": "",
    "characterCount": 0
  }
}
```
