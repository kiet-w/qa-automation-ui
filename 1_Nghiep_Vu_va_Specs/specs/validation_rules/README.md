# EAFAMS Validation Rules & Error Handling Catalog

Tài liệu đặc tả toàn bộ quy tắc kiểm thực dữ liệu (Validation Rules) và xử lý lỗi (Error Handling) được đồng bộ từ Google Drive:
- **Thư mục nguồn Drive**: [Validation Rules Folder](https://drive.google.com/drive/folders/1X4fBlIgi6ilL6yCP4NBJSZVFTAB0iuaU)
- **Đường dẫn cục bộ**: [`specs/validation_rules/`](file:///home/baudui/automation-ui/specs/validation_rules/) (Symlink: [`validation_rules/`](file:///home/baudui/automation-ui/validation_rules/))

---

## 1. Cấu Trúc Thư Mục

```text
specs/validation_rules/
├── README.md                                          # Mục lục & ma trận phân loại (file này)
├── raw/                                               # File gốc tải trực tiếp từ Drive (.docx, .md)
│   ├── F2_Validation_Rules_EN.docx
│   ├── FS08_R8_Profile_Validation_Rule.md
│   ├── FS10_R10_FAS_Application_Validation (Draft).md
│   ├── function-1-validation-rules.docx
│   ├── function-1-validation-rules.md
│   ├── R3_Validation_Rules.md
│   ├── R4_FAS_Validation_Rules_EN.docx
│   ├── R5_FAS_APPLICATION_Validation_Rules.docx
│   └── R9_OUTSTANDING FEE AND PAYMENT_Validation_Rules.docx
└── md/                                                # Toàn bộ nội dung đã chuẩn hóa Markdown cho AI & QA
    ├── F2_Validation_Rules_EN.md
    ├── FS08_R8_Profile_Validation_Rule.md
    ├── FS10_R10_FAS_Application_Validation (Draft).md
    ├── function-1-validation-rules.md
    ├── function-1-validation-rules-from-docx.md
    ├── R3_Validation_Rules.md
    ├── R4_FAS_Validation_Rules_EN.md
    ├── R5_FAS_APPLICATION_Validation_Rules.md
    └── R9_OUTSTANDING_FEE_AND_PAYMENT_Validation_Rules.md
```

---

## 2. Bảng Danh Mục Chi Tiết 9 Bộ Validation Rules

| STT | Tên Tài Liệu (Markdown) | Module / Requirement | Đối Tượng Sử Dụng / Role | Trọng Tâm Validation & Error Handling |
| :---: | :--- | :--- | :--- | :--- |
| 1 | [`F2_Validation_Rules_EN.md`](file:///home/baudui/automation-ui/specs/validation_rules/md/F2_Validation_Rules_EN.md) | **F2 / R2: Top-Up Management** | MOE HQ, Finance Admin | Quy tắc nạp tiền tài khoản học sinh, giới hạn hạn mức (Cap rules), kiểm tra số dư, xác thực phương thức thanh toán, rollback khi thất bại. |
| 2 | [`FS08_R8_Profile_Validation_Rule.md`](file:///home/baudui/automation-ui/specs/validation_rules/md/FS08_R8_Profile_Validation_Rule.md) | **FS08 / R8: Profile Management** | Parent Portal (Singpass) | Kiểm thực các trường thông tin cá nhân (`/profile`): Mobile number (8 chữ số, tiền tố 6, 8, 9), Email (tối đa 150 ký tự, format chuẩn), Postal code (6 chữ số), Address, các trường chỉ đọc (Full Name, NRIC). |
| 3 | [`FS10_R10_FAS_Application_Validation (Draft).md`](file:///home/baudui/automation-ui/specs/validation_rules/md/FS10_R10_FAS_Application_Validation%20(Draft).md) | **FS10 / R10: Online FAS Application** | Parents / Guardians | Kiểm thực đơn xin trợ cấp tài chính trực tuyến: NRIC/FIN người nộp đơn và thành viên gia đình, thu nhập PCI/GHI, tệp đính kèm chứng minh thu nhập, trạng thái lưu Draft. |
| 4 | [`function-1-validation-rules.md`](file:///home/baudui/automation-ui/specs/validation_rules/md/function-1-validation-rules.md) | **Function 1: Education Account Lifecycle** | Backend / Batch Jobs | Vòng đời tài khoản học sinh EAFAMS: Khởi tạo, đóng tài khoản, chuyển giao số dư, kiểm tra độ tuổi hợp lệ (7 & 16 tuổi, xử lý năm nhuận 29/02), chống trùng lặp, đồng bộ dữ liệu công dân (Singpass/MyInfo). |
| 5 | [`R3_Validation_Rules.md`](file:///home/baudui/automation-ui/specs/validation_rules/md/R3_Validation_Rules.md) | **R3: School User Management** | MOE Admin, School Admin | Phân quyền vai trò người dùng trường học (`/school-users`): Tạo mới, gán trường, chỉnh sửa, thu hồi quyền, các trường tìm kiếm và thông báo lỗi tương ứng. |
| 6 | [`R4_FAS_Validation_Rules_EN.md`](file:///home/baudui/automation-ui/specs/validation_rules/md/R4_FAS_Validation_Rules_EN.md) | **R4: Assess FAS and Apply Subsidies** | School Admin, MOE HQ | Thẩm định và xét duyệt trợ cấp tài chính (SBFAS & MOEFAS) trên 12 màn hình/dialog: Chống trùng lặp trợ cấp (Overlap Prevention), công cụ tính AI/ML Need Score và bộ quy tắc từ chối tự động (Deny Rules engine). |
| 7 | [`R5_FAS_APPLICATION_Validation_Rules.md`](file:///home/baudui/automation-ui/specs/validation_rules/md/R5_FAS_APPLICATION_Validation_Rules.md) | **R5: Paper Applications (Đơn Giấy)** | School User / School Admin | Quy trình xử lý đơn giấy FAS từ Màn A đến G: Tải tệp scan (Upload scans), rà soát đơn qua 5 phần (Parts 1–5), các điều kiện kiểm thực trước khi submit và quy tắc nghiệp vụ BR1–BR9. |
| 8 | [`R9_OUTSTANDING_FEE_AND_PAYMENT_Validation_Rules.md`](file:///home/baudui/automation-ui/specs/validation_rules/md/R9_OUTSTANDING_FEE_AND_PAYMENT_Validation_Rules.md) | **R9 / Function 9: Outstanding Fees and Payment** | Parents / Guardians (Singpass) | 7 màn hình thanh toán nợ học phí (SCR-01 đến SCR-08): Chọn con liên kết, tra cứu hoá đơn, chọn phương thức thanh toán, xem lại xác nhận, xử lý giao dịch đang chờ, biên lai thanh toán thành công, xử lý lỗi thanh toán thất bại. |
