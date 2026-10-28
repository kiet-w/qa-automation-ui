# Component Specification: Upload Applications List (`f05-paper-application-list`)

> **Module**: `f05` - FAS Paper Applications (Đơn giấy / Hardcopy Applications Offline)  
> **Component**: `paper_application_list` (Screen A: Upload applications list, Filters & Draft Table)  
> **Source Spec**: `specs/md/FS document/FS-05_Hardcopy_Applications_Offline.md` (Mục 3, Mục 8, Mục 9 BR6) & `specs/validation_rules/md/R5_FAS_APPLICATION_Validation_Rules.md` (Màn A: A1 - A10)  
> **Target Audience**: School User (School Admin)  

---

## 1. Metadata & Selector

- **Route URL / Access Path**: Admin Portal $\rightarrow$ Financial assistance $\rightarrow$ Upload applications (`/admin/fas/paper-applications`)
- **Container Element Tag**: `<div id="paper-applications-container" data-testid="page-paper-applications">`
- **Playwright Locators (BSK Standardized Convention)**:

| Element Name | HTML Tag / Type | Playwright Locator (BSK Convention) | Description / Notes |
| :--- | :--- | :--- | :--- |
| **Upload Scans Button** | `button` | `page.locator("button[data-testid='btn-open-upload-scans'], button:has-text('Upload scans')")` | Field A1; opens Upload dialog |
| **Stat Card PENDING** | `div[role="button"]` | `page.locator("div[data-testid='stat-card-pending'], .stat-card:has-text('PENDING')")` | Field A2; filter toggle |
| **Stat Card MOEFAS** | `div[role="button"]` | `page.locator("div[data-testid='stat-card-moefas'], .stat-card:has-text('MOEFAS')")` | Field A2; filter toggle |
| **Stat Card SBFAS** | `div[role="button"]` | `page.locator("div[data-testid='stat-card-sbfas'], .stat-card:has-text('SBFAS')")` | Field A2; filter toggle |
| **Search Input** | `input[type="search"]` | `page.locator("input[data-testid='input-search-applications'], input[placeholder*='Search Application ID']")` | Field A3; max 100 chars, debounced |
| **Status Filter Dropdown** | `select` | `page.locator("select[data-testid='select-status-filter'], select[name='status']")` | Field A4; All, Draft, Pending, Approved, Rejected |
| **Tier Filter Dropdown** | `select` | `page.locator("select[data-testid='select-tier-filter'], select[name='tier']")` | Field A5; school's SBFAS tiers |
| **Date Range Filter** | `select` | `page.locator("select[data-testid='select-uploaded-filter'], select[name='uploaded_range']")` | Field A6; Last 7 days, 30 days, Any time |
| **Applications Table** | `table` | `page.locator("table[data-testid='table-paper-applications']")` | Field A7; data grid |
| **Draft Row** | `tr` | `page.locator("tr[data-testid^='row-draft-'], tr:has-text('Draft')")` | Field A8; Draft items listed at top |
| **Continue Draft Button** | `button` | `page.locator("button[data-testid^='btn-continue-draft-'], button:has-text('Continue')")` | Resumes Review application screen |
| **Delete Draft Button** | `button` | `page.locator("button[data-testid^='btn-delete-draft-'], button:has-text('Delete')")` | Discards draft after confirm |
| **Submitted Row** | `tr` | `page.locator("tr[data-testid^='row-submitted-']")` | Field A9; clickable to View application |
| **Footer Note** | `div.footer-note` | `page.locator("div[data-testid='footer-enrolment-note']")` | Field A10; statutory rules note |

---

## 2. BR / AC Traceability

- **Functional Requirements**: `FS-05` Section 1.1, Section 3 Components 1-8, Section 8 View/Edit, Section 9 BR6.
- **Business Rules (BR)**:
  - `BR-05-LIST-01`: Phạm vi dữ liệu chỉ hiển thị đơn giấy (nguồn Paper) và các bản Draft của trường của School User đang đăng nhập. MOE HQ không thấy màn hình này.
  - `BR-05-LIST-02`: Bản nháp (`Draft`) được ưu tiên liệt kê lên trên cùng bảng dữ liệu, có mã Application ID là `"Not submitted"`, trạng thái `Draft`, kèm nút `Continue` và `Delete`. Bấm vào dòng cũng tiếp tục bản nháp.
  - `BR-05-LIST-03`: Thẻ thống kê (A2) đếm số đơn giấy của trường theo từng trạng thái: PENDING (chờ xét), MOEFAS (duyệt tự động), SBFAS (trường quyết định). **Bản Draft không được tính vào các thẻ thống kê này**. Bấm thẻ để lọc danh sách, bấm lần nữa để bỏ lọc.
  - `BR-05-LIST-04`: Bộ lọc mặc định thời gian là `Last 7 days`. Có thể chuyển sang `Last 30 days` hoặc `Any time`.
  - `BR-05-LIST-05`: Dòng đơn đã nộp (`Submitted`) có thể bấm vào để mở màn hình xem chi tiết `View application`. Nếu đơn còn ở trạng thái `Pending`, School User có quyền chỉnh sửa (`Edit`). Khi đã `Approved` hoặc `Rejected`, đơn bị khóa chỉ đọc.
- **User Story Traceability**: `US-F5-07` (Quản lý và tra cứu danh sách đơn giấy FAS của trường).
- **Access Control (RBAC)**: Chỉ School User (School Admin).

---

## 3. Ma trận 12 lớp Validation

| Lớp Kiểm Thử (12 Tầng) | Điều Kiện / Dữ Liệu Đầu Vào | Kỳ Vọng Giao Diện & Hành Vi Hệ Thống | Mã Lỗi / Phản Hồi Trực Quan |
| :--- | :--- | :--- | :--- |
| **1. Search Substring Matching** | Nhập chuỗi tìm kiếm: tên học sinh `"Aisha"`, hoặc số EA `"t1412345b"`, hoặc Application ID `"APP-2026-00412"`. | Lọc danh sách không phân biệt hoa/thường (case-insensitive substring match). | Bảng hiển thị các dòng khớp. |
| **2. Search BVA Limits (0 to 100)** | • 0 ký tự: Bỏ lọc, hiện toàn bộ danh sách.<br>• 100 ký tự: Hợp lệ, tìm kiếm bình thường.<br>• 101 ký tự trở lên: Bị cắt ngắn còn 100 ký tự. | Tìm kiếm chuẩn xác; không gây giật lag (áp dụng debounce 300ms sau phím cuối). | Kết quả mượt mà. |
| **3. Empty Search Result** | Nhập từ khóa không tồn tại: `"zzzzzz_non_existent"`. | Hiển thị thông báo bảng rỗng chuẩn; không bị lỗi console. | `No applications found.` |
| **4. Stat Card Filter Toggle** | Click vào thẻ `PENDING (1)`. Click lần thứ hai vào thẻ đó. | Lần 1: Lọc bảng chỉ hiện các đơn có Status = Pending; thẻ có viền xanh active. Lần 2: Bỏ lọc, bảng quay về hiển thị tất cả. | Toggle filter mượt mà. |
| **5. Status Filter Dropdown** | Chọn `Draft` trong dropdown Status filter. | Bảng lọc chỉ hiển thị các bản nháp chưa nộp; ẩn các đơn Pending/Approved. | Cập nhật URL query params hoặc state. |
| **6. Draft Row Priority** | Có 1 đơn Draft và 5 đơn Submitted trong CSDL. | Dòng Draft luôn đứng ở các vị trí đầu tiên của bảng. Application ID hiển thị text `"Not submitted"`. | Draft ở vị trí ưu tiên hàng đầu. |
| **7. Continue Draft Navigation** | Bấm nút `Continue` hoặc click vào dòng Draft. | Điều hướng ngay vào màn hình `Review application` (Màn C) với toàn bộ dữ liệu đã lưu được phục hồi đầy đủ (Scenario T9). | Khôi phục đúng màn hình Review. |
| **8. Delete Draft Confirmation** | Bấm nút `Delete` trên một dòng Draft. | Hiển thị modal xác nhận xóa: "Are you sure you want to delete this draft?". Khi bấm xác nhận, bản nháp bị xóa khỏi CSDL và biến mất khỏi bảng. | Toast: `Draft deleted.` |
| **9. View Submitted Read-Only** | Click vào một dòng đơn đã ở trạng thái `Approved · MOEFAS`. | Mở màn hình `View application` ở chế độ chỉ đọc (read-only); không có nút Edit, chỉ có nút `Back to list`. | Màn hình chỉ đọc an toàn. |
| **10. Edit Pending Application** | Click vào một dòng đơn ở trạng thái `Pending`. | Màn hình mở ra có nút `Edit`. Khi bấm Edit, các trường có thể chỉnh sửa được; sau khi lưu ghi nhận History: `"Paper application edited"` (Scenario T12). | Lưu thành công; audit trail đầy đủ. |
| **11. Combined Filter Multi-Criteria** | Kết hợp: Search `"Lee"` + Status `"Pending"` + Uploaded `"Last 30 days"`. | Áp dụng logic AND giữa các tiêu chí lọc; bảng tự động reset về trang 1. | Danh sách kết hợp chính xác. |
| **12. UI Health & Responsive Table** | Thu nhỏ màn hình hoặc mở trên màn hình độ phân giải 1366x768. | Bảng có thanh cuộn ngang cục bộ trong khối table nếu cần (`overflow-x: auto`), không gây tràn layout toàn trang; 0 console errors. | Đạt chuẩn Invariant 7 UI Health. |

---

## 4. Error Handling & Visual Feedback

- **Standard Messages**:
  - Không tìm thấy đơn: `"No applications found."`
  - Xóa nháp thành công: `"Draft deleted."`
  - Lỗi tải dữ liệu: `"Something went wrong. Please try again."`
- **Visual Cues**:
  - Huy hiệu trạng thái có màu sắc trực quan:
    - `Draft`: Xám nhạt (`bg-gray-100 text-gray-700`)
    - `Pending`: Vàng cam (`bg-amber-100 text-amber-800`)
    - `Approved · MOEFAS`: Xanh lá đậm (`bg-emerald-100 text-emerald-800`)
    - `Approved · SBFAS`: Xanh dương (`bg-blue-100 text-blue-800`)
    - `Rejected`: Đỏ nhạt (`bg-rose-100 text-rose-800`)

---

## 5. JSON Fixtures Data Payload

```json
{
  "stat_cards_summary": {
    "pendingCount": 1,
    "moefasApprovedCount": 3,
    "sbfasApprovedCount": 2,
    "draftsCountExcluded": 1
  },
  "sample_table_rows": [
    {
      "id": "draft-001",
      "applicationId": "Not submitted",
      "status": "Draft",
      "fileName": "scan_batch_2026_lee.pdf",
      "uploadedBy": "School Admin (Tan S.L.)",
      "uploadedAt": "26/10/2026 09:30",
      "studentName": "Tan Mei Ling, Tan Jun Jie",
      "class": "P6-Compassion, P3-Honesty",
      "isDraft": true
    },
    {
      "id": "app-2026-00412",
      "applicationId": "APP-2026-00412",
      "status": "Pending",
      "scheme": "MOEFAS",
      "fileName": "scan_aisha_mohd.pdf",
      "uploadedBy": "School Admin (Tan S.L.)",
      "uploadedAt": "25/10/2026 14:15",
      "studentName": "Aisha Binte Mohd",
      "class": "P4-Integrity",
      "isDraft": false
    },
    {
      "id": "app-2026-00388",
      "applicationId": "APP-2026-00388",
      "status": "Approved · MOEFAS",
      "scheme": "MOEFAS",
      "fileName": "scan_chen_family.pdf",
      "uploadedBy": "School Admin (Tan S.L.)",
      "uploadedAt": "20/10/2026 11:00",
      "studentName": "Chen Wei Ling",
      "class": "P5-Resilience",
      "isDraft": false
    }
  ]
}
```
