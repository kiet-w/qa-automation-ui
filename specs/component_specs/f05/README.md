# Module Specification: F05 - FAS Paper Applications (Đơn Giấy Offline)

> **Module Code**: `f05` / `R5` / `FS-05`  
> **Module Name**: FAS Paper Applications (Hardcopy Applications Offline / Đơn giấy)  
> **Source Documents**:
> - `specs/md/FS document/FS-05_Hardcopy_Applications_Offline.md` (Phiên bản 1.2, 21/10/2026)
> - `specs/validation_rules/md/R5_FAS_APPLICATION_Validation_Rules.md` (Bản nháp 0.1, 26/10/2026)
> **Target Audience & RBAC**: School User (School Admin). MOE HQ không có quyền truy cập.

---

## 1. Module Overview & Architectural Philosophy

Phân hệ `f05` (Function 5) cho phép **School User (School Admin)** nhập liệu các mẫu đơn Financial Assistance Scheme (FAS) in sẵn (hardcopy) do phụ huynh điền tay và nộp trực tiếp tại trường:
1. **Upload bản scan**: Tải lên từ 1 đến 5 trang scan (.pdf, .jpg, .png $\le 10\text{ MB}$).
2. **Review application**: Hệ thống mô phỏng trích xuất OCR, chia làm 5 phần chuẩn hóa (Part 1 Người khai $\rightarrow$ Part 2 Các con $\rightarrow$ Part 3 Thành viên gia đình & Thu nhập CPF $\rightarrow$ Part 4 Hoàn cảnh Context $\rightarrow$ Part 5 Cam kết chữ ký).
3. **Quy tắc phân luồng Chức năng 4 (F4)**:
   - Một mẫu đơn = Một đơn cho mỗi con (dùng chung mã gia đình `FAM-YYYY-NNNNN`).
   - Con có quốc tịch Singapore Citizen: `MOEFAS Pending` (chờ form đóng để hệ thống xếp hạng và tự động duyệt).
   - Con không phải công dân Singapore: `SBFAS Pending` (gửi về trường học của con tự xét duyệt).
4. **Bản nháp & Sửa đơn**: Hỗ trợ lưu nháp (`Draft`), xem lại đơn đã nộp và chỉnh sửa đơn khi còn ở trạng thái `Pending` (kể cả sau khi form nộp đơn đã đóng).

---

## 2. Component Specifications Sitemap

### 2.1. Atomic Components (`specs/component_specs/f05/atomic/`)

| File Spec | Tên Component & Phạm Vi | Mã Trường / Rules |
| :--- | :--- | :--- |
| [`upload_scans_dialog.md`](file:///home/baudui/automation-ui/specs/component_specs/f05/atomic/upload_scans_dialog.md) | Hộp thoại tải bản scan đơn giấy (Dropzone, PDF/JPG/PNG, $\le 10\text{ MB}$, tối đa 5 file). | B1 – B4, T1 |
| [`applicant_details.md`](file:///home/baudui/automation-ui/specs/component_specs/f05/atomic/applicant_details.md) | Part 1: Thông tin người khai (NRIC tự động tra cứu họ tên, ngày sinh, địa chỉ, liên hệ, SBFAS consent). | C5 – C15, VR-F5-01, BR3 |
| [`children_applying.md`](file:///home/baudui/automation-ui/specs/component_specs/f05/atomic/children_applying.md) | Part 2: Danh sách các con nộp đơn (Tra cứu CSDL MOE, tuổi 7–16, trường của user, kiểm tra form mở). | C16 – C18, VR-F5-01..07, T3..T6 |
| [`household_members.md`](file:///home/baudui/automation-ui/specs/component_specs/f05/atomic/household_members.md) | Part 3: Thành viên gia đình & Thu nhập (Không có ô nhập thu nhập; tra cứu CPF, tính tự động GHI & PCI). | C19 – C20, VR-F5-01, VR-F5-08, BR4 |
| [`circumstances_context.md`](file:///home/baudui/automation-ui/specs/component_specs/f05/atomic/circumstances_context.md) | Part 4: Hoàn cảnh & nguyện vọng (Context tùy chọn, tối đa 2000 ký tự, chuyển tiếp sang drawer F4). | C21, BR5, T11 |
| [`declaration_signature.md`](file:///home/baudui/automation-ui/specs/component_specs/f05/atomic/declaration_signature.md) | Part 5: Cam kết & chữ ký (Tick declaration, tick signature checked, ngày ký không trong tương lai). | C22 – C26, VR-F5-01, T8 |
| [`paper_application_list.md`](file:///home/baudui/automation-ui/specs/component_specs/f05/atomic/paper_application_list.md) | Màn hình danh sách đơn giấy (Thẻ thống kê, Search 100 ký tự, Bộ lọc Status/Tier/Date, Dòng Draft ưu tiên). | A1 – A10, T9 |
| [`review_before_submit_dialog.md`](file:///home/baudui/automation-ui/specs/component_specs/f05/atomic/review_before_submit_dialog.md) | Hộp thoại xem lại trước khi nộp (Tóm tắt Part 1–4, chống double click, tạo đơn con, xóa bản nháp). | E1 – E6, VR-F5-10, T10 |

### 2.2. Integration Flows (`specs/component_specs/f05/integration/`)

| File Spec | Tên Luồng & Phạm Vi Nghiệp Vụ | Actors & State Transitions |
| :--- | :--- | :--- |
| [`paper_application_submission_flow.md`](file:///home/baudui/automation-ui/specs/component_specs/f05/integration/paper_application_submission_flow.md) | Luồng nộp đơn giấy toàn trình: Upload scan $\rightarrow$ Nhập Part 1–5 $\rightarrow$ Validation gate $\rightarrow$ Modal review $\rightarrow$ Phân luồng F4. | School Admin $\rightarrow$ Review Gate $\rightarrow$ MOEFAS/SBFAS Pending |
| [`draft_lifecycle_flow.md`](file:///home/baudui/automation-ui/specs/component_specs/f05/integration/draft_lifecycle_flow.md) | Vòng đời bản nháp đơn giấy: Lưu nháp giữa chừng $\rightarrow$ Hiển thị trên đầu danh sách $\rightarrow$ Khôi phục (`Continue`) $\rightarrow$ Xóa hủy (`Delete`). | Unsaved $\rightarrow$ Draft $\rightarrow$ Staging $\rightarrow$ Cleaned up |
| [`edit_pending_application_flow.md`](file:///home/baudui/automation-ui/specs/component_specs/f05/integration/edit_pending_application_flow.md) | Xem và chỉnh sửa đơn đã nộp: Chỉ sửa khi đơn còn `Pending` (kể cả khi form đã đóng), ghi nhận History `"Paper application edited"`. | Pending $\rightarrow$ Edit Mode $\rightarrow$ Save Changes with Audit Log |

---

## 3. Core Business Rules & Validation Matrix Summary

1. **Điều kiện mở form (BR9 / VR-F5-07)**: Chỉ nộp được khi form MOEFAS hoặc form SBFAS của trường của con đang mở (`"{tên}: the FAS application form is closed (next opens DD/MM/YYYY)."`).
2. **Quyền hạn trường (BR2 / VR-F5-06)**: Ít nhất một con trong đơn phải đang theo học tại trường của School User (`"At least one child must be enrolled at {trường}."`).
3. **Độ tuổi hợp lệ (BR2 / VR-F5-04)**: Con phải từ đủ 7 đến dưới 17 tuổi (7 đến 16 tuổi tại ngày nộp đơn; sinh nhật thứ 17 bị chặn).
4. **Không trùng đơn trong năm (BR2 / VR-F5-05)**: Con chưa từng có đơn FAS nào trong năm hiện tại (`"{tên} already has an application this year ({id}, {status})."`).
5. **Chống trùng lặp NRIC (BR4 / VR-F5-08)**: NRIC của người khai, các con và các thành viên gia đình phải hoàn toàn khác biệt nhau.
6. **Thu nhập không tự khai (BR4)**: Toàn bộ thu nhập lấy tự động từ API Chính phủ (CPF); không có ô nhập thu nhập trên giao diện.
