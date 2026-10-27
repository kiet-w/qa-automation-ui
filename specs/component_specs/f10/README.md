# Module Specification: F10 - FAS Family Application Portal (Cổng Nộp Đơn FAS Trực Tuyến)

> **Module Code**: `f10` / `R10` / `FS-10`  
> **Module Name**: FAS Family Application Portal (Parent FAS Application / Phụ huynh nộp đơn FAS)  
> **Source Documents**:
> - `specs/md/FS document/FS-10_FAS_Family_Application_Portal.md` (Phiên bản 1.2, 21/10/2026)
> - `specs/validation_rules/md/FS10_R10_FAS_Application_Validation (Draft).md` (Bản thảo 26/10/2026)
> - `specs/md/FS document/FS-04_Financial_Assistance_Scheme_FAS.md` (Phiên bản 1.3)
> **Target Audience & RBAC**: Phụ huynh / Người giám hộ hợp pháp (Xác thực qua Singpass trên e-Service Portal).

---

## 1. Module Overview & Architectural Philosophy

Phân hệ `f10` (Function 10) cung cấp cho **Phụ huynh (cha hoặc mẹ được liên kết với học sinh)** cổng thông tin nộp đơn xin hỗ trợ tài chính trực tuyến theo mô hình đơn gia đình hợp nhất (Unified Family Application):
1. **Một đơn cho cả gia đình**: Nộp đồng thời cho nhiều con trong 1 lần làm việc; hệ thống cấp chung mã gia đình `FAM-YYYY-NNNNN` và sinh đơn con độc lập cho từng học sinh.
2. **Wizard 5 bước trực quan**:
   - **Bước 1 (Children)**: Tự điền thông tin phụ huynh (chỉ đọc), chọn quan hệ, chọn các con đủ điều kiện (khóa các con $\ge 16$ tuổi, đã có đơn chờ hoặc form đóng).
   - **Bước 2 (Household & income)**: Thu nhập tự động lấy từ dữ liệu Chính phủ qua CPF/IRAS (không cần nhập số tiền hay nộp bảng lương), tự động tính GHI và PCI, thu thập hoàn cảnh cho engine F4 chấm điểm.
   - **Bước 3 (Documents)**: Đính kèm tài liệu tùy chọn (PDF/ảnh $\le 5\text{ MB}$), mặc định tick chọn nguyện vọng chuyển tiếp SBFAS.
   - **Bước 4 (Context)**: Nhập văn bản hoàn cảnh & nguyện vọng (tối đa 2000 ký tự).
   - **Bước 5 (Review & submit)**: Xem tóm tắt 4 khối, đọc giải thích lộ trình What happens next, tick cam kết xác nhận và nộp đơn.
3. **Quản lý bản nháp (Draft)**: Tự động lưu khi chuyển bước, hỗ trợ `Save draft & exit`, mỗi phụ huynh 1 bản nháp duy nhất, mở lại đúng bước đã lưu.
4. **Theo dõi tiến trình 4 giai đoạn (Timeline Tracking)**: Theo dõi tiến độ từ lúc nộp (`Submitted`), qua kiểm tra hệ thống (`System check`), thẩm định (`Review`) đến quyết định (`Decision`), nhận thông báo email tự động.

---

## 2. Component Specifications Sitemap

### 2.1. Atomic Components (`specs/component_specs/f10/atomic/`)

| File Spec | Tên Component & Phạm Vi | Mã Trường / Rules |
| :--- | :--- | :--- |
| [`financial_assistance_landing.md`](file:///home/baudui/automation-ui/specs/component_specs/f10/atomic/financial_assistance_landing.md) | Trang chủ Financial assistance (Nút Apply for FAS, Resume/Discard draft, Thẻ nháp, Danh sách đơn đã nộp). | FS10 Mục 3, Mục 10 |
| [`children_selection.md`](file:///home/baudui/automation-ui/specs/component_specs/f10/atomic/children_selection.md) | Wizard Bước 1: Chọn con nộp đơn (Tự điền profile Singpass chỉ đọc, Chọn quan hệ bắt buộc, Khóa con $\ge 16$ tuổi hoặc form đóng). | FS10 Mục 4, BR1, BR2, T1, T2, T12 |
| [`household_income.md`](file:///home/baudui/automation-ui/specs/component_specs/f10/atomic/household_income.md) | Wizard Bước 2: Hộ gia đình & Thu nhập CPF (Tra cứu tự động CPF, tính GHI/PCI, Khóa Continue khi thiếu tên/NRIC thành viên, Thu thập hoàn cảnh ML). | FS10 Mục 5, BR3, T3 |
| [`documents_upload.md`](file:///home/baudui/automation-ui/specs/component_specs/f10/atomic/documents_upload.md) | Wizard Bước 3: Tài liệu hỗ trợ & SBFAS (Tài liệu tùy chọn $\le 5\text{ MB}$, Checkbox "Also consider SBFAS" mặc định bật). | FS10 Mục 6, BR5 |
| [`circumstances_context.md`](file:///home/baudui/automation-ui/specs/component_specs/f10/atomic/circumstances_context.md) | Wizard Bước 4: Hoàn cảnh & nguyện vọng (Context tùy chọn $\le 2000$ ký tự, Bộ đếm live, Lưu nháp tại Bước 4). | FS10 Mục 7, BR6, T4, T5 |
| [`review_submit_declaration.md`](file:///home/baudui/automation-ui/specs/component_specs/f10/atomic/review_submit_declaration.md) | Wizard Bước 5: Xem lại, cam kết & nộp đơn (Tóm tắt 4 khối, Lộ trình What happens next, Checkbox cam kết bắt buộc, Chống double click). | FS10 Mục 8, BR4, BR7, T6, T7, T8 |
| [`application_timeline_tracking.md`](file:///home/baudui/automation-ui/specs/component_specs/f10/atomic/application_timeline_tracking.md) | Theo dõi tiến trình đơn & Kết quả (4 Node Timeline: Submitted $\rightarrow$ System check $\rightarrow$ Review $\rightarrow$ Decision, Khung Approved / Rejected, Email notification). | FS10 Mục 9, BR5, BR8, T9, T10, T11 |

### 2.2. Integration Flows (`specs/component_specs/f10/integration/`)

| File Spec | Tên Luồng & Phạm Vi Nghiệp Vụ | Actors & State Transitions |
| :--- | :--- | :--- |
| [`online_family_application_flow.md`](file:///home/baudui/automation-ui/specs/component_specs/f10/integration/online_family_application_flow.md) | Luồng nộp đơn trực tuyến toàn trình 5 bước: Children $\rightarrow$ Household & income $\rightarrow$ Documents $\rightarrow$ Context $\rightarrow$ Review & submit $\rightarrow$ Phân luồng F4. | Parent $\rightarrow$ Wizard Steps 1-5 $\rightarrow$ Under Review (MOEFAS/SBFAS) |
| [`parent_draft_lifecycle_flow.md`](file:///home/baudui/automation-ui/specs/component_specs/f10/integration/parent_draft_lifecycle_flow.md) | Vòng đời bản nháp của phụ huynh: Tự động lưu qua các bước $\rightarrow$ Save draft & exit $\rightarrow$ Hiển thị trên landing $\rightarrow$ Resume đúng bước $\rightarrow$ Discard nháp. | Pristine $\rightarrow$ Step In-Progress $\rightarrow$ Draft Saved $\rightarrow$ Auto-Cleaned |
| [`application_lifecycle_decision_flow.md`](file:///home/baudui/automation-ui/specs/component_specs/f10/integration/application_lifecycle_decision_flow.md) | Vòng đời xét duyệt & ban hành kết quả: Chờ form đóng $\rightarrow$ Xếp hạng ưu tiên theo PCI $\rightarrow$ Tự động duyệt MOEFAS hoặc chuyển trường duyệt SBFAS $\rightarrow$ Email kết quả. | Under Review $\rightarrow$ MOEFAS Waiting $\rightarrow$ Approved / SBFAS / Rejected |

---

## 3. Core Business Rules & Validation Matrix Summary

1. **Điều kiện chọn con (BR1)**: Chỉ chọn được con dưới 16 tuổi (tại ngày nộp; tròn 16 tuổi bị khóa), chưa có đơn Pending, và form MOEFAS hoặc form SBFAS của trường con đang mở.
2. **Thu nhập tự động (BR3)**: Thu nhập hoàn toàn lấy từ dữ liệu Chính phủ (CPF); phụ huynh không tự khai thu nhập và không bắt buộc nộp bảng lương.
3. **Mã gia đình hợp nhất (BR4)**: Mỗi con được chọn thành một đơn với cùng dữ liệu hộ gia đình; các con dùng chung một mã gia đình `FAM-YYYY-NNNNN`.
4. **Phân luồng MOEFAS vs SBFAS (BR5)**:
   - Học sinh công dân Singapore: `MOEFAS Pending` (`"Under review"`), chờ form MOEFAS đóng để xếp hạng PCI từ thấp lên cao rồi tự động duyệt.
   - Học sinh không phải công dân Singapore: Chuyển thẳng sang diện `SBFAS Pending` gửi cho trường của học sinh xét duyệt.
5. **Cam kết bắt buộc (BR7)**: Nút `Submit application` bị khóa chặt cho đến khi phụ huynh tick vào ô cam kết thông tin trung thực và đồng ý xác thực dữ liệu với cơ quan Chính phủ.
6. **Thông báo email (BR8)**: Hệ thống tự động gửi email cho phụ huynh sau mỗi quyết định được ban hành.
