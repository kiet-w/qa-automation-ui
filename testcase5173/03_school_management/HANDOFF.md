# BÀN GIAO ĐẶC TẢ KIỂM THỬ: Cổng Quản trị viên EduFAMS — Quản lý Danh bạ & Tạo mới Trường học ()

## 1. Thông Tin Tổng Quan
- **Phân hệ**: `03_school_management` | **Chức năng**: `Cổng Quản trị viên EduFAMS — Quản lý Danh bạ & Tạo mới Trường học ()`
- **Nguồn đặc tả (Source of Truth)**: `1_Nghiep_Vu_va_Specs/specs/ui_bsk/localhost-5173/academic-and-users/03_school_management.md`
- **Bộ hồ sơ Test Cases**: `TC_ADMIN_SCHOOL_MANAGEMENT.md` & `TC_ADMIN_SCHOOL_MANAGEMENT.xlsx` — **20 Test Cases**, Trạng thái: `Not Run`
- **Phân bố 5 Trụ Cột Trong Scope (Linh hoạt, bao phủ toàn diện)**:
  - **BR (Business Rules)**: 5 ca (Quy tắc nghiệp vụ, phân quyền vai trò MOEHQ/SCHOOL, ràng buộc dữ liệu, vòng đời).
  - **AC (Acceptance Criteria)**: 5 ca (Tiêu chí nghiệm thu giao diện, hiển thị cấu trúc trang, bảng dữ liệu, toolbar).
  - **Validation (Error Validation)**: 5 ca (Kiểm tra bắt buộc nhập, định dạng NRIC/Date/Code, kiểm tra trùng lặp, trim khoảng trắng).
  - **Flow (Function Flow)**: 4 ca (Luồng thao tác chính, submit thành công, điều hướng hoặc lọc tìm kiếm nâng cao).
  - **Error (Error Handling)**: 1 ca (Xử lý lỗi hệ thống, hủy bỏ an toàn, phục hồi khi gián đoạn mạng, empty state).
- **Bộ Locators Live DOM**: Trích xuất tối ưu trực tiếp từ DOM thực tế theo đặc tả UI BSK.

## 2. Tiêu Chuẩn Tuân Thủ AGENTS.md
- **Invariant 7 (Anti-Bloat & In-Scope Focus)**: Bao phủ linh hoạt và đầy đủ nghiệp vụ; loại bỏ triệt để test i18n, đa ngôn ngữ, stress test 10,000 ký tự hay tấn công mã độc ngoài lề.
- **Invariant 12 (Dual-Artifact Sync)**: Đồng bộ song song Markdown (`TC_ADMIN_SCHOOL_MANAGEMENT.md`), Excel 20 cột chuẩn tender (`TC_ADMIN_SCHOOL_MANAGEMENT.xlsx`) và ma trận JSON (`test_matrix.json`).
- **Invariant 13 (Language Standard)**: 100% Tiếng Việt rõ ràng, mạch lạc, dễ đối soát cho toàn bộ hồ sơ nghiệp vụ.
