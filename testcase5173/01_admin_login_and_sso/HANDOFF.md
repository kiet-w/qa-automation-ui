# Biên Bản Bàn Giao Kiểm Thử: 01_admin_login_and_sso

- **Phân hệ**: `01_admin_login_and_sso` (Đăng nhập Cổng Quản trị & Microsoft SSO)
- **Cổng dịch vụ**: `http://localhost:5173/login` & Microsoft Entra Simulator `http://localhost:5288`
- **Số lượng test cases**: **22 test cases** (Chuẩn 5 Trụ Cột: BR, AC, Validation, Error Handling, Function Flow)
- **Tình trạng Spec**: Grounded 100% vào Live DOM và mã nguồn backend IAM / frontend React. Tuyệt đối không bịa đặt text lỗi hay selector (Invariant 6 & Invariant 14).
- **Trạng thái thực thi**: `Not Run` (Chờ người dùng chạy bulk execution với `-n 3`).

## Phân bổ 5 Trụ Cột In-Scope:
1. **Quy tắc nghiệp vụ & Phân quyền (BR)**: 5 ca (TC-ADM-AUTH-001 đến 005)
2. **Tiêu chí nghiệm thu chức năng (AC)**: 4 ca (TC-ADM-AUTH-006 đến 009)
3. **Kiểm tra hợp lệ dữ liệu (Validation)**: 4 ca (TC-ADM-AUTH-010 đến 013)
4. **Xử lý ngoại lệ & Phục hồi lỗi (Error Handling)**: 5 ca (TC-ADM-AUTH-014 đến 018)
5. **Luồng thao tác chức năng chính (Function Flow)**: 4 ca (TC-ADM-AUTH-019 đến 022)

## Danh mục tài liệu đồng bộ (Dual-artifact sync):
- `TC_ADMIN_LOGIN_MICROSOFT_SSO.md`
- `TC_ADMIN_LOGIN_MICROSOFT_SSO.xlsx` (Chuẩn 20 cột Google Sheet)
- `test_matrix.json` (Dữ liệu máy đọc chuẩn)
- Mirror đồng bộ sang `1_Nghiep_Vu_va_Specs/testcases/academic-and-users/5173-admin-login-and-sso/`
- Tích hợp vào Master Workbook `1_Nghiep_Vu_va_Specs/testcase5173/MASTER_TESTCASES_CONG_QUAN_TRI_5173.xlsx`
