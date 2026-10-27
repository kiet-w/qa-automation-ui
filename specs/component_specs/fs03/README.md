# FS03: School User Management & School Management

## 1. Phân Hệ Tổng Quan
- **Mã phân hệ**: `FS03` (Requirement R3, Function 3)
- **Tên nghiệp vụ**: School User Management & School Entity Management
- **Đường dẫn ứng dụng**:
  - Danh sách người dùng trường: `http://localhost:5173/school-user-management`
  - Tạo người dùng trường (Single & Bulk CSV): `http://localhost:5173/school-user-management/new`
  - Danh sách trường học: `http://localhost:5173/school-management`
  - Tạo trường học mới: `http://localhost:5173/school-management/new`
- **Đối tượng sử dụng**: MOE HQ System Administrator (xác thực qua Microsoft Entra ID SSO)
- **Mục tiêu**: Cung cấp công cụ quản trị tập trung cho MOE HQ để khởi tạo, quản lý và phân quyền cho nhân viên các trường học trên toàn quốc (qua hình thức tạo đơn lẻ hoặc tải lên danh sách hàng loạt CSV tối đa 1,000 dòng), đồng thời quản lý danh mục các trường học Active và các khối lớp học thuật liên kết.

---

## 2. Mục Lục Đặc Tả Thành Phần Đơn Lẻ (Atomic Component Specs)

Tất cả các tài liệu thành phần đơn lẻ tuân thủ đầy đủ cấu trúc 5 phần chuẩn hóa:

| Component File | Tên Thành Phần & Chức Năng | Route & Selector Chính | BR / AC Traceability |
| :--- | :--- | :--- | :--- |
| [`school_user_search_and_table.md`](./atomic/school_user_search_and_table.md) | **School User Search & Table**: Bảng danh sách người dùng trường học, tìm kiếm thời gian thực theo mã/tên/trường, nhãn người dùng chưa gán trường (`Unassigned in any school`), phân trang (5/10/25). | `/school-user-management`<br>`input[type='search']`<br>`table tbody tr` | `R3-F02`<br>`BR-03-01`<br>`AC-01`, `AC-02`, `AC-05` |
| [`school_user_single_create_form.md`](./atomic/school_user_single_create_form.md) | **Single School User Create Form**: Form tạo thủ công từng tài khoản trường học, kiểm tra định dạng NRIC (1 chữ cái, 7 số, 1 chữ cái), First/Last name max 100, Email duy nhất, và mã trường MOE hợp lệ. | `/school-user-management/new`<br>`#school-user-nric`<br>`button:has-text('Create')` | `R3-F02`<br>`BR-03-02`, `BR-03-03`<br>`AC-03`, `AC-04` |
| [`school_user_bulk_csv_upload.md`](./atomic/school_user_bulk_csv_upload.md) | **Bulk CSV School User Import**: Tải lên danh sách hàng loạt qua file CSV (tối đa 1,000 dòng), kiểm tra header bắt buộc, tải file template, cơ chế Partial Success tiếp tục xử lý các dòng hợp lệ khi có dòng lỗi. | `/school-user-management/new`<br>`#school-users-csv`<br>`button:has-text('Import')` | `R3-F02`<br>`BR-03-04`<br>`AC-06`, `AC-07` |
| [`school_create_form.md`](./atomic/school_create_form.md) | **School Creation Form**: Khởi tạo thực thể trường học mới, mã MOE code duy nhất (3-20 ký tự chữ số/gạch nối), tên trường max 150, loại hình trường, và chọn các khối lớp học thuật qua multi-select chips. | `/school-management/new`<br>`#school-moeSchoolCode`<br>`#school-name` | `R3-F01`<br>`BR-03-05`<br>`AC-08`, `AC-09` |

---

## 3. Mục Lục Đặc Tả Luồng Tích Hợp (Integration Flow Specs)

Các tài liệu luồng tích hợp tuân thủ cấu trúc 5 phần chuẩn hóa:

| Integration Flow File | Tên Luồng Nghiệp Vụ & Quy Trình | Vai Trò & Điểm Nổi Bật | Trạng Thái Chuyển Đổi Chính |
| :--- | :--- | :--- | :--- |
| [`school_user_provisioning_flow.md`](./integration/school_user_provisioning_flow.md) | **School User Provisioning & SSO Integration**: Quy trình khởi tạo tài khoản nhân viên trường (qua Single Form hoặc Bulk CSV), lưu vào cơ sở dữ liệu TemplateIAM, phản ánh lên bảng danh sách và kích hoạt liên kết SSO Microsoft Entra ID. | MOE HQ Admin ➔ School User | `EMPTY_FORM`<br>➔ `READY_TO_SUBMIT`<br>➔ `PROVISIONING`<br>➔ `USER_ASSIGNED` / `UNASSIGNED` |
| [`school_creation_and_assignment_flow.md`](./integration/school_creation_and_assignment_flow.md) | **School Entity Creation & User Assignment**: Vòng đời tạo thực thể trường học Active, liên kết các khối lớp học thuật, và ràng buộc phạm vi truy cập dữ liệu của nhân viên (School User chỉ được truy cập dữ liệu thuộc trường Active đã gán). | MOE HQ Admin ➔ School Entity | `DRAFT`<br>➔ `VALIDATED`<br>➔ `ACTIVE`<br>➔ (User Access Allowed) |

---

## 4. Bảng Tra Cứu Thông Báo & Mã Lỗi Hệ Thống (Error Catalog)

| Ngữ Cảnh Kích Hoạt | Thông Báo Chuẩn Trên Giao Diện | Loại Lỗi | Visual Indicator |
| :--- | :--- | :--- | :--- |
| Để trống NRIC | `"NRIC is required."` | Validation Error | `aria-invalid="true"`, viền đỏ input |
| Sai định dạng NRIC | `"NRIC must be 1 letter, 7 digits and 1 letter (e.g. S1234567A)."` | Format Error | `aria-invalid="true"`, viền đỏ input |
| NRIC đã tồn tại trong DB | `"User with NRIC '{nric}' already exists."` | Conflict Error 409 | Banner alert đỏ đầu form |
| Email đã tồn tại trong DB | `"User with email '{email}' already exists."` | Conflict Error 409 | Banner alert đỏ đầu form |
| Tệp CSV chưa được chọn | `"Please choose a CSV file."` | File Validation | Inline alert màu đỏ |
| Tệp CSV rỗng | `"The CSV file is empty."` | File Validation | Banner alert màu đỏ |
| Tệp CSV vượt quá 1,000 dòng | `"The CSV file may contain at most 1000 rows."` | Limit Exceeded | Banner alert màu đỏ |
| Thiếu cột header trong CSV | `"Missing CSV column: {header}"` | Schema Error | Banner alert màu đỏ |
| Trùng mã MOE School Code | `"School with MOE code '{code}' already exists."` | Conflict Error 409 | Banner alert đỏ đầu form |
| Trường đang Inactive | `"School '{code}' is inactive."` | Business Rule Error | Banner alert đỏ đầu form |
| Tạo user thành công | `"School user created. The school user was created successfully."` | Success Feedback | Toast xanh lá + Result card |
| Tạo trường thành công | `"School created"` | Success Feedback | Toast xanh lá |
