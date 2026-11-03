# Automation cho testcase5173

Các suite ánh xạ theo test matrix của 8 phân hệ. Assertions ở test; selector lấy từ BSK và mô tả module tương ứng. Module 03 dùng lại suite danh bạ trường đã có ở `tests/fs03/fs03-school-directory/`.

| Phân hệ | Suite | Mã testcase |
| --- | --- | --- |
| 01 Đăng nhập và SSO | `01_admin_login_and_sso/` | `TC-ADM-AUTH-001`–`022` |
| 02 Dashboard shell | `02_admin_dashboard_shell/` | `TC-SHL-001`–`016` |
| 03 Quản lý trường | `../fs03/fs03-school-directory/` | `TC-SCH-001`–`020` |
| 04 Quản lý người dùng trường | `04_school_user_management/` | `TC-USR-001`–`018` |
| 05 Niên khóa và cấp học | `05_academic_years_and_levels/` | `TC-AYL-001`–`018` |
| 06 Quản lý lớp | `06_class_management/` | `TC-CLS-001`–`018` |
| 07 Hồ sơ và nhập học học sinh | `07_student_management_and_enrollment/` | `TC-STU-001`–`020` |
| 08 Cấu hình trường | `08_school_config/` | `TC-CFG-001`–`018` |

Chạy riêng từng suite:

```bash
pytest tests/testcase5173/01_admin_login_and_sso/ -v
pytest tests/testcase5173/02_admin_dashboard_shell/ -v
pytest tests/fs03/fs03-school-directory/ -v
pytest tests/testcase5173/04_school_user_management/ -v
pytest tests/testcase5173/05_academic_years_and_levels/ -v
pytest tests/testcase5173/06_class_management/ -v
pytest tests/testcase5173/07_student_management_and_enrollment/ -v
pytest tests/testcase5173/08_school_config/ -v
```

Một số luồng phụ thuộc dữ liệu đã seed và trạng thái phiên đăng nhập, đặc biệt các case học sinh đã nhập học/rút hồ sơ và role SCHOOL. Khi matrix không khớp BSK chi tiết hoặc BSK không định nghĩa locator, test dùng hành vi/selector có căn cứ và tránh tự suy đoán selector mới; ghi chú cụ thể nằm trong test module tương ứng.
