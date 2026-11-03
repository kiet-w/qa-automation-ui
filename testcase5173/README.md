# Bộ Đặc Tả Kiểm Thử Cổng Quản Trị EduFAMS (localhost:5173) — Toàn Diện In-Scope

Bộ test case bao phủ toàn diện 100% nghiệp vụ In-Scope của Cổng Quản trị EduFAMS, tuân thủ nghiêm ngặt Invariant 7, 12, 13:
- **Bao phủ đầy đủ 4 thành phần In-Scope cốt lõi (Không gò bó số lượng nhân tạo, linh hoạt theo yêu cầu nghiệp vụ):**
  1. **BR (Business Rules):** Phân quyền vai trò (MOEHQ, SCHOOL), kiểm soát truy cập phân hệ, các ràng buộc học vụ, vòng đời trường/lớp/học sinh.
  2. **AC (Acceptance Criteria):** Tiêu chí nghiệm thu chức năng, cấu trúc bảng dữ liệu, toolbar, thanh điều hướng, modal và trạng thái hiển thị.
  3. **Validation & Function Flow:**
     - Error Validation: Kiểm tra bắt buộc nhập (mandatory), định dạng NRIC/Email/Date/Code, kiểm tra trùng lặp và phản hồi viền đỏ `aria-invalid='true'`.
     - Function Flow: Luồng thao tác chính (Happy path, Tạo mới, Gán trường, Phân lớp, Nhập học, Sao chép niên khóa, Tìm kiếm/Lọc nâng cao, Điều hướng qua lại).
  4. **UI BSK Locators:** Bộ selector bám sát Live DOM thực tế từ đặc tả `1_Nghiep_Vu_va_Specs/specs/ui_bsk/localhost-5173/`.
- **Loại bỏ triệt để ngoài lề (Anti-Bloat):**
  - Tuyệt đối KHÔNG sinh test i18n / đa ngôn ngữ / rò rỉ translation key.
  - Tuyệt đối KHÔNG sinh test non-functional lan man (stress paste 10,000 ký tự, tấn công SQLi/XSS, ARIA tree sâu).

## Danh sách 8 Phân hệ Quản trị (Tổng số: 150 test cases)

| STT | Phân hệ (Module) | Đường dẫn (URL) | File Đặc tả MD | File Excel 20 cột | Số ca |
| :---: | :--- | :--- | :--- | :--- | :---: |
| 1 | `01_admin_login_and_sso` | `Đăng nhập Cổng Quản trị` | `TC_ADMIN_LOGIN_MICROSOFT_SSO.md` | `TC_ADMIN_LOGIN_MICROSOFT_SSO.xlsx` | 22 |
| 2 | `02_admin_dashboard_shell` | `Trang chủ Quản trị` | `TC_ADMIN_SHELL_SIDEBAR_RBAC_HEADER.md` | `TC_ADMIN_SHELL_SIDEBAR_RBAC_HEADER.xlsx` | 16 |
| 3 | `03_school_management` | `Danh bạ Trường học` | `TC_ADMIN_SCHOOL_MANAGEMENT.md` | `TC_ADMIN_SCHOOL_MANAGEMENT.xlsx` | 20 |
| 4 | `04_school_user_management` | `Quản lý Cán bộ trường` | `TC_ADMIN_SCHOOL_USER_MANAGEMENT.md` | `TC_ADMIN_SCHOOL_USER_MANAGEMENT.xlsx` | 18 |
| 5 | `05_academic_years_and_levels` | `Quản lý Niên khóa` | `TC_ADMIN_ACADEMIC_YEARS_AND_LEVELS.md` | `TC_ADMIN_ACADEMIC_YEARS_AND_LEVELS.xlsx` | 18 |
| 6 | `06_class_management` | `Quản lý Lớp học` | `TC_ADMIN_CLASS_MANAGEMENT.md` | `TC_ADMIN_CLASS_MANAGEMENT.xlsx` | 18 |
| 7 | `07_student_management_and_enrollment` | `Hồ sơ Học sinh` | `TC_ADMIN_STUDENT_MANAGEMENT_ENROLLMENT.md` | `TC_ADMIN_STUDENT_MANAGEMENT_ENROLLMENT.xlsx` | 20 |
| 8 | `08_school_config` | `Cấu hình Học vụ Trường` | `TC_ADMIN_SCHOOL_CONFIG.md` | `TC_ADMIN_SCHOOL_CONFIG.xlsx` | 18 |

- **Master Workbook Tổng Hợp:** [`MASTER_TESTCASES_CONG_QUAN_TRI_5173.xlsx`](MASTER_TESTCASES_CONG_QUAN_TRI_5173.xlsx) (150 test cases)