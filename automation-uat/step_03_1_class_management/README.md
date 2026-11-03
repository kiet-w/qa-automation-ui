# Phân Hệ UAT: 3.1. Kiểm tra hoặc Tạo Lớp học (Classes)

Tài liệu ghi nhận chi tiết quá trình thực thi kiểm thử tự động trực quan (Visual Headed Automation) cho **Mục 3.1: Kiểm tra hoặc Tạo Lớp học** trong quy trình UAT Cổng Quản trị EduFAMS.

---

## 📌 1. Thông Tin Môi Trường & Phiên Kiểm Thử

| Thông Tin | Giá Trị Chi Tiết |
| :--- | :--- |
| **Hạng Mục UAT** | **Mục 3.1: Kiểm tra hoặc Tạo Lớp học (Classes)** |
| **Môi Trường Target** | `https://admin.20-255-158-192.sslip.io` (hoặc `http://localhost:5173`) |
| **Vai Trò Đăng Nhập** | **Cán bộ trường (SCHOOL)** |
| **Tài Khoản Test** | `staff1@IAM.edu.vn` (Rosyth Primary School - `SCH-003` / `RPS-0201`) |
| **Chế Độ Chạy** | Headed Browser (Hiển thị trực tiếp trên màn hình với Live HUD & Pacing `slow_mo=400ms`) |
| **Thời Điểm Hoàn Thành**| 2026-10-31 |
| **Trạng Thái Chung** | ✅ **HOÀN THÀNH TOÀN BỘ (5/5 Bước PASS)** |

---

## 📋 2. Nhật Ký Chi Tiết Từng Bước Đã Thực Hiện

### Bước 1 & 2: Truy cập Menu Classes & Kiểm tra lớp P1-A
- **Thao tác**:
  1. Đăng nhập SSO qua Microsoft Simulator bằng tài khoản `staff1@IAM.edu.vn`.
  2. Tại Sidebar menu bên trái, click chọn **Classes** (URL: `/class-management`).
  3. Nhập từ khóa `"P1-A"` vào ô tìm kiếm và bấm nút **Search**.
- **Kết quả thực tế ghi nhận**:
  - Bảng dữ liệu hiển thị dòng lớp học:
    - **Class code**: `P1-A`
    - **Class name**: `Primary 1-A (Courage)`
    - **Academic level**: `PRI-1 - Primary 1`
    - **Academic year**: `2026`
    - **Sĩ số**: `0` Enrolled students / `0` Active students
    - **ID hệ thống**: `CLS-RPS-P1A`
  - Ngoài ra, khối Primary 1 còn có các lớp `1A1` (10 học sinh), `1A2` (5 học sinh).
- **Kết luận quy trình UAT**:
  > [!TIP]
  > Theo đúng chỉ dẫn tại Mục 3.1: *"Nếu đã có: Bạn có thể dùng luôn lớp đó, chuyển ngay sang mục 3.2."*
  > Lớp **`P1-A` đã sẵn sàng** với sĩ số 0 học sinh, có thể dùng ngay cho các bước phân lớp / gán học sinh tại mục 3.2.
- **Minh chứng**: [`evidence/01_check_p1a_in_classes_table.png`](evidence/01_check_p1a_in_classes_table.png)

---

### Bước 3a: Diễn tập Form Tạo Lớp — Kiểm tra Validation bắt buộc
- **Thao tác**:
  1. Bấm nút màu xanh **Create class** tại góc phải trên cùng của màn hình `/class-management`.
  2. Hệ thống điều hướng sang form tạo lớp mới: `/class-management/new`.
  3. Để trống toàn bộ các trường và bấm nút **Create class** (`button[type="submit"]`).
- **Kết quả thực tế ghi nhận**:
  - Form chặn gửi dữ liệu lên server.
  - Cả 3 trường bắt buộc đều kích hoạt viền đỏ cảnh báo `aria-invalid="true"`.
  - Hiển thị đầy đủ Accessible Error Summary và Inline Error text:
    - `Class code`: `"Class code is required."`
    - `Class name`: `"Class name is required."`
    - `Level offering`: `"Select a school level offering."`
- **Minh chứng**: [`evidence/02_create_form_mandatory_validation.png`](evidence/02_create_form_mandatory_validation.png)

---

### Bước 3b: Diễn tập Form Tạo Lớp — Ràng buộc duy nhất (Chặn trùng mã lớp)
- **Thao tác**:
  1. Điền thông tin trùng lặp với lớp đã có:
     - **Class code**: `P1-A`
     - **Class name**: `Primary 1-A Duplicate`
     - **Level offering**: `Primary 1 · 2026 · Rosyth Primary School`
  2. Bấm nút **Create class**.
- **Kết quả thực tế ghi nhận**:
  - Backend API từ chối tạo lớp trùng lặp trong cùng niên khóa.
  - Giao diện bật hộp cảnh báo Alert màu đỏ:
    - Tiêu đề: `"Unable to create class"`
    - Nội dung: `"Class code 'P1-A' already exists for this offering."`
  - URL giữ nguyên tại `/class-management/new` để người dùng sửa đổi.
- **Minh chứng**: [`evidence/03_duplicate_p1a_rejected.png`](evidence/03_duplicate_p1a_rejected.png)

---

### Bước 3c: Diễn tập Form Tạo Lớp — Luồng Tạo Mới Thành Công (Happy Path)
- **Thao tác**:
  1. Điền thông tin lớp học với mã lớp duy nhất (ví dụ: `P1-A96981`):
     - **Class code**: `P1-A96981`
     - **Class name**: `Primary 1-A Auto 96981`
     - **Level offering**: `Primary 1 · 2026 · Rosyth Primary School`
  2. Bấm nút **Create class**.
- **Kết quả thực tế ghi nhận**:
  - Gửi thành công request `POST /api/academic-resources/v1/schools/SCH-003/classes`.
  - Hệ thống tạo lớp học thành công và điều hướng an toàn về `/class-management`.
  - Tìm kiếm lớp vừa tạo trên bảng: Dòng dữ liệu mới xuất hiện chính xác với sĩ số ban đầu là `0 / 0`.
- **Minh chứng**: [`evidence/04_created_class_verified_in_list.png`](evidence/04_created_class_verified_in_list.png)

---

### Bước 4: Mở Xem Chi Tiết Lớp Học (Detail & Roster)
- **Thao tác**:
  1. Tìm lại lớp `P1-A` trên bảng danh sách lớp học.
  2. Bấm nút **Detail** trên cột Thao tác Actions.
  3. Kiểm tra màn hình chi tiết lớp học (`/class-management/CLS-RPS-P1A`).
- **Kết quả thực tế ghi nhận**:
  - Tiêu đề hiển thị: `P1-A` - `Primary 1-A (Courage)` - `Primary 1 · Academic year 2026`.
  - Thẻ tóm tắt thông số (Class overview):
    - `Academic year`: **2026**
    - `Academic level`: **Primary 1**
    - `Active students`: **0** (0 students in roster)
  - Bảng danh sách học sinh (Roster Table) hiển thị trạng thái rỗng: *"No students found. This class has no students assigned yet."*.
  - Sẵn sàng 100% để đón nhận học sinh được phân bổ ở Mục 3.2.
- **Minh chứng**: [`evidence/05_class_p1a_detail_view.png`](evidence/05_class_p1a_detail_view.png)

---

## 🚀 3. Hướng Dẫn Chạy Lại Kịch Bản Trực Quan

Kịch bản được đóng gói thành công cụ chạy độc lập có thể xem trực tiếp trên màn hình:

```bash
# Chạy có giao diện trình duyệt (Headed), độ trễ 400ms để quan sát:
.venv/bin/python tools/uat_3_1_class_management.py --url https://admin.20-255-158-192.sslip.io --headed --slow-mo 400
```
