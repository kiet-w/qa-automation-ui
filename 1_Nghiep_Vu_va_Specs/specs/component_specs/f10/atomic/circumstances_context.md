# Component Specification: Circumstances & Wishes - Step 4 (`f10-circumstances-context`)

> **Module**: `f10` - FAS Online Family Application Portal (Cổng Nộp Đơn FAS Phụ Huynh)  
> **Component**: `circumstances_context` (Wizard Step 4: Your Circumstances and Wishes)  
> **Source Spec**: `specs/md/FS document/FS-10_FAS_Family_Application_Portal.md` (Mục 7 Bước 4, Mục 11 BR6, Mục 12 T4, T5) & `specs/validation_rules/md/FS10_R10_FAS_Application_Validation (Draft).md`  
> **Target Audience**: Parent / Legal Guardian (Đăng nhập Singpass)  

---

## 1. Metadata & Selector

- **Route URL / Access Path**: e-Service Portal $\rightarrow$ Financial assistance $\rightarrow$ Apply for FAS $\rightarrow$ Step 4 (`/parent/fas/apply/step-4`)
- **Container Element Tag**: `<section id="fas-wizard-step-4" data-testid="wizard-step-4-context">`
- **Playwright Locators (BSK Standardized Convention)**:

| Element Name | HTML Tag / Type | Playwright Locator (BSK Convention) | Description / Notes |
| :--- | :--- | :--- | :--- |
| **Step 4 Container** | `div` | `page.locator("div[data-testid='step-container-context']")` | Step 4 wrapper |
| **Section Header** | `h2` | `page.locator("h2:has-text('Your circumstances and wishes')")` | Step 4 Title |
| **Context Textarea** | `textarea` | `page.locator("textarea[data-testid='input-fas-context'], textarea[name='parent_context']")` | Optional; max 2000 chars |
| **Character Counter** | `span / div` | `page.locator("[data-testid='context-live-counter'], .char-counter")` | Live counter "n / 2000" |
| **Step 4 Back Button** | `button` | `page.locator("button[data-testid='btn-step4-back'], button:has-text('Back')")` | Navigates to Step 3 |
| **Step 4 Continue Button** | `button` | `page.locator("button[data-testid='btn-step4-continue'], button:has-text('Continue')")` | Always enabled; goes to Step 5 |
| **Save Draft & Exit Button** | `button` | `page.locator("button[data-testid='btn-step4-save-draft'], button:has-text('Save draft & exit')")` | Scenario T4; saves draft |

---

## 2. BR / AC Traceability

- **Functional Requirements**: `FS-10` Section 7 Step 4, Section 11 BR6, Section 12 Scenarios T4, T5.
- **Business Rules (BR)**:
  - `BR-10-CTX-01`: Tiêu đề hiển thị chuẩn: `"Your circumstances and wishes"`.
  - `BR-10-CTX-02`: Ô nhập liệu là **tùy chọn (optional)**, văn bản thuần (plain text), giới hạn tối đa $2000$ ký tự.
  - `BR-10-CTX-03`: Nội dung này được chuyển tiếp trực tiếp và hiển thị đầy đủ cho người xét duyệt đơn tại Chức năng 4 (`Function 4 Drawer -> Context`).
  - `BR-10-CTX-04`: Khi bấm `Save draft & exit` tại Bước 4, hệ thống lưu bản nháp với trạng thái `"step 4 of 5 (Context)"` và hiển thị thẻ Draft card tương ứng tại trang chủ (Scenario T4).
  - `BR-10-CTX-05`: Khi bấm `Resume` từ trang chủ, hệ thống mở đúng Bước 4 và giữ nguyên vẹn nội dung context đã nhập (Scenario T5).
- **User Story Traceability**: `US-F10-05` (Phụ huynh trình bày hoàn cảnh khó khăn và nguyện vọng trợ cấp).
- **Access Control (RBAC)**: Phụ huynh học sinh.

---

## 3. Ma trận 12 lớp Validation

| Lớp Kiểm Thử (12 Tầng) | Điều Kiện / Dữ Liệu Đầu Vào | Kỳ Vọng Giao Diện & Hành Vi Hệ Thống | Mã Lỗi / Phản Hồi Trực Quan |
| :--- | :--- | :--- | :--- |
| **1. Empty / Optional** | Bỏ trống ô Context (0 ký tự) và bấm `Continue`. | Hợp lệ hoàn toàn! Hệ thống cho phép đi thẳng sang Bước 5 Review mà không bị chặn. | Chuyển tiếp mượt sang Bước 5. |
| **2. BVA Min/Max Limits** | • 1 ký tự: Hợp lệ.<br>• 2,000 ký tự: Hợp lệ, đạt ngưỡng tối đa.<br>• Cố gõ ký tự thứ 2,001: Trình duyệt chặn nhập (`maxlength="2000"`). | Bộ đếm ký tự hiển thị chính xác `2000 / 2000`. Không làm tràn bộ nhớ client. | Bộ đếm cập nhật real-time. |
| **3. Placeholder Prompt Check** | Textarea ở trạng thái rỗng chưa nhập liệu. | Hiển thị văn bản gợi ý đúng mẫu FS10: `"e.g. I lost my job in June. We hope to get help with school fees and transport for both children."`. | Placeholder hiển thị đúng mẫu. |
| **4. Save Draft & Exit Flow (T4)** | Nhập 300 ký tự context rồi bấm `Save draft & exit`. | Dữ liệu được lưu vào CSDL; Toast: `"Draft saved. You can continue later."`; chuyển về landing page; thẻ nháp hiện `"step 4 of 5 (Context)"`. | Hoàn tất Scenario T4. |
| **5. Resume Draft Flow (T5)** | Từ landing page, bấm `Resume draft`. | Hệ thống mở ngay lập tức Bước 4 (`/parent/fas/apply/step-4`); toàn bộ 300 ký tự context được hiển thị nguyên vẹn trong textarea. | Hoàn tất Scenario T5. |
| **6. XSS & Code Injection Security** | Dán payload mã độc: `<script>alert('xss')</script>`, `<img src=x onerror=alert(1)>`. | Hệ thống xử lý dạng plain text thuần túy; khi render ở Bước 5 hoặc F4 drawer, các thẻ HTML được mã hóa an toàn (escaped HTML); không execute script. | Render an toàn dưới dạng text. |
| **7. Multi-language & Emoji Input** | Nhập tiếng Anh kèm tiếng Trung, tiếng Mã Lai, tiếng Tamil và emoji: `"Family in hardship. 需助学金. Terima kasih. 🙏"`. | Chuỗi UTF-8 được lưu trữ và hiển thị chính xác 100%, không bị lỗi font (tofu character). | Hiển thị đa ngôn ngữ chuẩn xác. |
| **8. Real-time Counter Sync** | Gõ từng ký tự hoặc copy-paste đoạn văn dài vào textarea. | Bộ đếm `n / 2000` nhảy số đồng bộ tức thời sau mỗi sự kiện `input`. | Counter phản hồi không độ trễ. |
| **9. Whitespace Only Handling** | Nhập toàn bộ là dấu cách và xuống dòng trống. | Khi sang Bước 5 sẽ được chuẩn hóa thành chuỗi rỗng và hiển thị fallback `"No context given."`. | Hiển thị fallback hợp lý. |
| **10. UI Health & Responsive Layout** | Mở trên màn hình điện thoại di động (chiều rộng 375px). | Textarea co giãn vừa vặn màn hình; hỗ trợ cuộn dọc tự nhiên; các nút Back / Save / Continue cố định dễ bấm; 0 console errors. | Đạt chuẩn Invariant 7 UI Health. |
| **11. Pristine / Dirty Transition** | Gõ 1 chữ cái đầu tiên vào textarea. | Form kích hoạt trạng thái dirty; nếu người dùng cố bấm reload trang hoặc đóng tab, trình duyệt hiển thị cảnh báo rời trang (beforeunload). | Bảo vệ dữ liệu chưa lưu. |
| **12. Step Navigation State Retention** | Bấm `Back` về Bước 3 rồi bấm `Continue` quay lại Bước 4. | Nội dung context đã nhập vẫn được giữ nguyên trong session client. | Không bị mất dữ liệu khi qua lại. |

---

## 4. Error Handling & Visual Feedback

- **Standard Messages**:
  - Không có context (khi xem lại ở Bước 5): `"No context given."`
  - Vượt quá $2000$ ký tự: `"Enter no more than 2000 characters."`
  - Lưu nháp thành công: `"Draft saved. You can continue later."`
- **Visual Cues**:
  - Bộ đếm ký tự chuyển màu đỏ cảnh báo khi chạm mốc 2,000 ký tự (`text-red-600 font-bold`).

---

## 5. JSON Fixtures Data Payload

```json
{
  "valid_context_payload": {
    "contextText": "Single-income household with elderly grandmother and 2 school-going children. Mother is currently seeking employment after retrenchment. Appreciate financial support for school fees and textbooks.",
    "characterCount": 204
  },
  "boundary_exact_2000_chars": {
    "contextText": "Circumstance statement ".repeat(86).slice(0, 2000),
    "characterCount": 2000
  },
  "empty_context_fallback": {
    "contextText": "",
    "characterCount": 0,
    "expectedReviewText": "No context given."
  }
}
```
