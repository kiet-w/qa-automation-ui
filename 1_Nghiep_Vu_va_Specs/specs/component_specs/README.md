# EAFAMS Enterprise UI Automation: Master Component Specifications Matrix

> **Repository**: `automation-ui`  
> **Master Index**: `specs/component_specs/README.md`  
> **Target System**: MOE Education Account & Fee Management System (EAFAMS)  
> **Governing Rules**: [`.agent/rules/01-two-stage-workflow.md`](file:///.agent/rules/01-two-stage-workflow.md), [`.agent/rules/02-field-test-matrix.md`](file:///.agent/rules/02-field-test-matrix.md), [`.agent/rules/03-failure-triage-adversarial.md`](file:///.agent/rules/03-failure-triage-adversarial.md), [`.agent/rules/04-automation-coding-standards.md`](file:///.agent/rules/04-automation-coding-standards.md)  
> **Security Boundary**: **Strict Invariant 0 (`copy/` directory is 100% READ-ONLY)**.

---

## 1. Executive Architectural Blueprint

Hệ thống **EAFAMS (Education Account & Fee Management System)** của Bộ Giáo Dục Singapore (MOE) được cấu trúc thành 8 phân hệ nghiệp vụ cốt lõi, phục vụ 3 nhóm đối tượng người dùng qua 2 cổng điện tử chuyên biệt:
- **Admin Portal**: Dành cho `MOE HQ System Administrator` và `School User (School Admin)` để quản trị trường lớp, biểu phí, nạp tiền tài khoản giáo dục, xử lý đơn giấy và ban hành chính sách trợ cấp tài chính.
- **e-Service Portal**: Dành cho `Parent / Legal Guardian` đăng nhập an toàn qua Singpass để quản lý thông tin định danh cá nhân, tra cứu tài khoản giáo dục, thanh toán công nợ học phí và nộp đơn xin trợ cấp tài chính gia đình (FAS) trực tuyến.

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        MOE EAFAMS ENTERPRISE ARCHITECTURE MAP                          │
└───────────────────────────────────────────────────┬────────────────────────────────────┘
                                                    │
             ┌──────────────────────────────────────┴──────────────────────────────────────┐
             ▼                                                                             ▼
┌───────────────────────────────────────────────┐ ┌───────────────────────────────────────────────┐
│        ADMIN PORTAL (MOE HQ & SCHOOL)         │ │            e-SERVICE PARENT PORTAL            │
├───────────────────────────────────────────────┤ ├───────────────────────────────────────────────┤
│ • f01: Education Account Lifecycle (HQ)       │ │ • fs08: Parent SingPass Profile & EA Info     │
│ • f02: EA Top-Up Management (HQ)              │ │ • fs09: Outstanding Fees & Split Payment      │
│ • fs03: School & User Entity Management (HQ)  │ │ • f10: FAS Online Family Application Portal   │
│ • f04: FAS Assessment & Subsidy Schemes (HQ/Sc)│ └───────────────────────────────────────────────┘
│ • f05: FAS Paper Applications Offline (School)│
└───────────────────────────────────────────────┘
```

---

## 2. Master Cross-Module Specification Matrix (Toàn Bộ 8 Phân Hệ)

| Mã Phân Hệ | Tên Nghiệp Vụ Chính Thức | Cổng Ứng Dụng | Đối Tượng Sử Dụng (RBAC) | Số Atomic Specs | Số Integration Flows | Thư Mục Đặc Tả Chi Tiết |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| **`f01`** | **Education Account Lifecycle** (Vòng đời tài khoản EA) | Admin Portal | `MOE HQ System Admin` | 4 components | 2 flows | [`specs/component_specs/f01/`](file:///home/baudui/automation-ui/specs/component_specs/f01/README.md) |
| **`f02`** | **Top-Up Management** (Nạp tiền đơn lẻ & chiến dịch) | Admin Portal | `MOE HQ System Admin` | 7 components | 2 flows | [`specs/component_specs/f02/`](file:///home/baudui/automation-ui/specs/component_specs/f02/README.md) |
| **`fs03`** | **School & User Entity Management** (Trường học & Nhân sự) | Admin Portal | `MOE HQ System Admin` | 4 components | 2 flows | [`specs/component_specs/fs03/`](file:///home/baudui/automation-ui/specs/component_specs/fs03/README.md) |
| **`f04`** | **Assess FAS & Apply Subsidies** (Thẩm định & Trợ cấp FAS) | Admin Portal | `School Admin` & `MOE HQ` | 5 components | 3 flows | [`specs/component_specs/f04/`](file:///home/baudui/automation-ui/specs/component_specs/f04/README.md) |
| **`f05`** | **FAS Paper Applications Offline** (Xử lý đơn giấy) | Admin Portal | `School User (School Admin)` | 8 components | 3 flows | [`specs/component_specs/f05/`](file:///home/baudui/automation-ui/specs/component_specs/f05/README.md) |
| **`fs08`** | **Parent Portal — SingPass, Profile** (Hồ sơ phụ huynh) | e-Service Portal | `Parent / Legal Guardian` | 4 components | 2 flows | [`specs/component_specs/fs08/`](file:///home/baudui/automation-ui/specs/component_specs/fs08/README.md) |
| **`fs09`** | **Outstanding Fees & Payment** (Công nợ & Thanh toán) | e-Service Portal | `Parent / Legal Guardian` | 4 components | 3 flows | [`specs/component_specs/fs09/`](file:///home/baudui/automation-ui/specs/component_specs/fs09/README.md) |
| **`f10`** | **FAS Family Application Portal** (Nộp đơn FAS gia đình) | e-Service Portal | `Parent / Legal Guardian` | 7 components | 3 flows | [`specs/component_specs/f10/`](file:///home/baudui/automation-ui/specs/component_specs/f10/README.md) |

---

## 3. Comprehensive Module Inventory & Link Catalog

### 3.1. Phân Hệ F01: Education Account Lifecycle (R1)
> Quản trị vòng đời tài khoản giáo dục: Khởi tạo tự động khi học sinh tròn 7 tuổi, đồng bộ dữ liệu công dân hàng ngày, tự động đóng tài khoản khi đủ 16 tuổi và xử lý số dư hoãn lại (Deferred Balance).

- **Module Index**: [`specs/component_specs/f01/README.md`](file:///home/baudui/automation-ui/specs/component_specs/f01/README.md)
- **Atomic Components**:
  1. [`student_citizen_search_filter.md`](file:///home/baudui/automation-ui/specs/component_specs/f01/atomic/student_citizen_search_filter.md): Thanh tìm kiếm NRIC/Họ tên, bộ lọc trạng thái và độ tuổi (`SCR-ADM-01`).
  2. [`ea_account_table_pagination.md`](file:///home/baudui/automation-ui/specs/component_specs/f01/atomic/ea_account_table_pagination.md): Bảng tài khoản EA tổng thể, sắp xếp cột và phân trang.
  3. [`ea_lifecycle_drawer.md`](file:///home/baudui/automation-ui/specs/component_specs/f01/atomic/ea_lifecycle_drawer.md): Drawer xem chi tiết dòng thời gian sự kiện, số dư và nhật ký kiểm toán.
  4. [`sync_job_status_card.md`](file:///home/baudui/automation-ui/specs/component_specs/f01/atomic/sync_job_status_card.md): Thẻ KPI chỉ số tiến trình đồng bộ dữ liệu công dân hàng ngày.
- **Integration Flows**:
  1. [`account_lifecycle_creation_flow.md`](file:///home/baudui/automation-ui/specs/component_specs/f01/integration/account_lifecycle_creation_flow.md): Luồng đồng bộ công dân $\rightarrow$ Kích hoạt tài khoản EA tuổi lên 7.
  2. [`account_closure_and_deferred_flow.md`](file:///home/baudui/automation-ui/specs/component_specs/f01/integration/account_closure_and_deferred_flow.md): Luồng đóng tài khoản tuổi 16 và xử lý số dư chuyển tiếp.

---

### 3.2. Phân Hệ F02: Top-Up Management (R2)
> Thực hiện nạp tiền tài khoản giáo dục: Nạp tiền đơn lẻ (Individual Top-Up) và nạp tiền theo chiến dịch hàng loạt (Bulk Campaign) với kiểm soát Idempotency chặt chẽ.

- **Module Index**: [`specs/component_specs/f02/README.md`](file:///home/baudui/automation-ui/specs/component_specs/f02/README.md)
- **Atomic Components**:
  1. [`ea_search_lookup.md`](file:///home/baudui/automation-ui/specs/component_specs/f02/atomic/ea_search_lookup.md): Tra cứu tài khoản EA theo số tài khoản hoặc NRIC (`SCR-01`).
  2. [`topup_amount_reason_form.md`](file:///home/baudui/automation-ui/specs/component_specs/f02/atomic/topup_amount_reason_form.md): Nhập số tiền SGD và lý do nạp tiền (`SCR-02`).
  3. [`topup_confirm_dialog.md`](file:///home/baudui/automation-ui/specs/component_specs/f02/atomic/topup_confirm_dialog.md): Hộp thoại xác nhận giao dịch nạp tiền Idempotent (`SCR-03`).
  4. [`topup_history_table.md`](file:///home/baudui/automation-ui/specs/component_specs/f02/atomic/topup_history_table.md): Bảng lịch sử nạp tiền và chi tiêu kiểm toán (`SCR-05`).
  5. [`campaign_criteria_config.md`](file:///home/baudui/automation-ui/specs/component_specs/f02/atomic/campaign_criteria_config.md): Cấu hình 6 tiêu chí OR cho chiến dịch nạp tiền hàng loạt (`SCR-08`).
  6. [`campaign_preview_confirm.md`](file:///home/baudui/automation-ui/specs/component_specs/f02/atomic/campaign_preview_confirm.md): Bảng xem trước danh sách thụ hưởng chiến dịch và xác nhận chạy (`SCR-09`).
  7. [`run_summary_item_grid.md`](file:///home/baudui/automation-ui/specs/component_specs/f02/atomic/run_summary_item_grid.md): Theo dõi tiến trình chiến dịch, dừng (Stop) và thử lại (Retry) dòng lỗi (`SCR-11/12`).
- **Integration Flows**:
  1. [`individual_topup_flow.md`](file:///home/baudui/automation-ui/specs/component_specs/f02/integration/individual_topup_flow.md): Luồng nạp tiền đơn lẻ toàn trình.
  2. [`bulk_campaign_dispatch_flow.md`](file:///home/baudui/automation-ui/specs/component_specs/f02/integration/bulk_campaign_dispatch_flow.md): Luồng tạo, duyệt và thực thi chiến dịch nạp tiền hàng loạt.

---

### 3.3. Phân Hệ FS03: School & User Entity Management (R3)
> Quản lý thực thể trường học và phân quyền tài khoản: Tạo người dùng trường đơn lẻ hoặc tải file CSV hàng loạt (tối đa 1,000 dòng), quản lý danh mục trường học và cấu hình khối lớp liên kết.

- **Module Index**: [`specs/component_specs/fs03/README.md`](file:///home/baudui/automation-ui/specs/component_specs/fs03/README.md)
- **Atomic Components**:
  1. [`school_user_search_and_table.md`](file:///home/baudui/automation-ui/specs/component_specs/fs03/atomic/school_user_search_and_table.md): Bảng danh sách người dùng trường, tìm kiếm thời gian thực, lọc tài khoản chưa gán trường (`Unassigned`).
  2. [`school_user_single_create_form.md`](file:///home/baudui/automation-ui/specs/component_specs/fs03/atomic/school_user_single_create_form.md): Form tạo tài khoản nhân viên trường đơn lẻ (kiểm tra NRIC, email duy nhất, MOE school code).
  3. [`school_user_bulk_csv_upload.md`](file:///home/baudui/automation-ui/specs/component_specs/fs03/atomic/school_user_bulk_csv_upload.md): Upload danh sách người dùng qua CSV hàng loạt, cơ chế Partial Success.
  4. [`school_create_form.md`](file:///home/baudui/automation-ui/specs/component_specs/fs03/atomic/school_create_form.md): Khởi tạo trường học mới, mã định danh MOE duy nhất và khối lớp liên kết.
- **Integration Flows**:
  1. [`school_user_provisioning_flow.md`](file:///home/baudui/automation-ui/specs/component_specs/fs03/integration/school_user_provisioning_flow.md): Luồng cấp phát tài khoản nhân sự trường học.
  2. [`school_entity_academic_onboarding_flow.md`](file:///home/baudui/automation-ui/specs/component_specs/fs03/integration/school_entity_academic_onboarding_flow.md): Luồng khởi tạo trường và đồng bộ khối lớp đào tạo.

---

### 3.4. Phân Hệ F04: Assess FAS & Apply Subsidies (R4)
> Quản lý chính sách trợ cấp tài chính: Xét duyệt SBFAS (trường), tự động duyệt MOEFAS (hệ thống) theo xếp hạng ưu tiên PCI/GHI, mô hình AI/ML Need Score gợi ý và thiết lập Scheme FAS.

- **Module Index**: [`specs/component_specs/f04/README.md`](file:///home/baudui/automation-ui/specs/component_specs/f04/README.md)
- **Atomic Components**:
  1. [`fas_applications_table_filter.md`](file:///home/baudui/automation-ui/specs/component_specs/f04/atomic/fas_applications_table_filter.md): Danh sách đơn FAS, bộ lọc Status/Tier/Date và thẻ thống kê.
  2. [`fas_review_drawer.md`](file:///home/baudui/automation-ui/specs/component_specs/f04/atomic/fas_review_drawer.md): Drawer chi tiết hồ sơ hộ gia đình, thu nhập CPF và xem tài liệu.
  3. [`ml_need_score_gauge.md`](file:///home/baudui/automation-ui/specs/component_specs/f04/atomic/ml_need_score_gauge.md): Đồng hồ AI Need Score, Hard Deny Rules và Tier gợi ý.
  4. [`fas_decision_dialogs.md`](file:///home/baudui/automation-ui/specs/component_specs/f04/atomic/fas_decision_dialogs.md): Hộp thoại Approve (chọn Tier) và Reject (nhập lý do từ chối).
  5. [`fas_scheme_wizard.md`](file:///home/baudui/automation-ui/specs/component_specs/f04/atomic/fas_scheme_wizard.md): Wizard tạo Scheme FAS 3 bước (General $\rightarrow$ Eligibility $\rightarrow$ Subsidy) và Add Fee.
- **Integration Flows**:
  1. [`fas_application_assessment_flow.md`](file:///home/baudui/automation-ui/specs/component_specs/f04/integration/fas_application_assessment_flow.md): Luồng thẩm định đơn FAS toàn trình tại trường học.
  2. [`ml_need_score_evaluation_flow.md`](file:///home/baudui/automation-ui/specs/component_specs/f04/integration/ml_need_score_evaluation_flow.md): Quy trình tính điểm AI Need Score và Hard Deny Rules.
  3. [`scheme_configuration_subsidy_application_flow.md`](file:///home/baudui/automation-ui/specs/component_specs/f04/integration/scheme_configuration_subsidy_application_flow.md): Luồng ban hành Scheme và áp dụng trợ cấp hồi tố.

---

### 3.5. Phân Hệ F05: FAS Paper Applications Offline (R5)
> Xử lý đơn FAS in giấy: Tải bản scan (.pdf, .jpg, .png $\le 10\text{ MB}$, tối đa 5 file), trích xuất OCR, rà soát 5 phần, kiểm tra độ tuổi 7–16, trường của user, tạo đơn con và phân luồng F4.

- **Module Index**: [`specs/component_specs/f05/README.md`](file:///home/baudui/automation-ui/specs/component_specs/f05/README.md)
- **Atomic Components**:
  1. [`upload_scans_dialog.md`](file:///home/baudui/automation-ui/specs/component_specs/f05/atomic/upload_scans_dialog.md): Hộp thoại upload bản scan đơn giấy (Dropzone, PDF/JPG/PNG, $\le 10\text{ MB}$, tối đa 5 file).
  2. [`applicant_details.md`](file:///home/baudui/automation-ui/specs/component_specs/f05/atomic/applicant_details.md): Part 1: Thông tin người khai (NRIC tự điền họ tên, liên hệ, SBFAS consent).
  3. [`children_applying.md`](file:///home/baudui/automation-ui/specs/component_specs/f05/atomic/children_applying.md): Part 2: Danh sách các con (Tra cứu MOE DB, tuổi 7–16, trường của user, form mở).
  4. [`household_members.md`](file:///home/baudui/automation-ui/specs/component_specs/f05/atomic/household_members.md): Part 3: Thành viên gia đình & Thu nhập CPF (Tính tự động GHI & PCI).
  5. [`circumstances_context.md`](file:///home/baudui/automation-ui/specs/component_specs/f05/atomic/circumstances_context.md): Part 4: Hoàn cảnh & nguyện vọng (Context tối đa 2000 ký tự).
  6. [`declaration_signature.md`](file:///home/baudui/automation-ui/specs/component_specs/f05/atomic/declaration_signature.md): Part 5: Cam kết & chữ ký (Tick declaration, tick signature checked, ngày ký).
  7. [`paper_application_list.md`](file:///home/baudui/automation-ui/specs/component_specs/f05/atomic/paper_application_list.md): Danh sách đơn giấy (Thẻ thống kê, Search, Bộ lọc, Dòng Draft ưu tiên).
  8. [`review_before_submit_dialog.md`](file:///home/baudui/automation-ui/specs/component_specs/f05/atomic/review_before_submit_dialog.md): Hộp thoại xem lại trước khi nộp (Tóm tắt Part 1–4, chống double click, xóa bản nháp).
- **Integration Flows**:
  1. [`paper_application_submission_flow.md`](file:///home/baudui/automation-ui/specs/component_specs/f05/integration/paper_application_submission_flow.md): Luồng nộp đơn giấy toàn trình từ Upload scan đến phân luồng F4.
  2. [`draft_lifecycle_flow.md`](file:///home/baudui/automation-ui/specs/component_specs/f05/integration/draft_lifecycle_flow.md): Vòng đời bản nháp đơn giấy (Lưu nháp $\rightarrow$ Khôi phục $\rightarrow$ Hủy bỏ).
  3. [`edit_pending_application_flow.md`](file:///home/baudui/automation-ui/specs/component_specs/f05/integration/edit_pending_application_flow.md): Xem và sửa đơn đã nộp khi còn ở trạng thái `Pending` (History audit log).

---

### 3.6. Phân Hệ FS08: Parent Portal — SingPass, Profile (R8)
> Quản lý hồ sơ phụ huynh Singpass: Bảo vệ tính bất biến của thông tin công dân (Full name, NRIC che mờ `*****123F`, Residential Address), cho phép tự cập nhật số điện thoại, email và địa chỉ gửi thư.

- **Module Index**: [`specs/component_specs/fs08/README.md`](file:///home/baudui/automation-ui/specs/component_specs/fs08/README.md)
- **Atomic Components**:
  1. [`singpass_identity_component.md`](file:///home/baudui/automation-ui/specs/component_specs/fs08/atomic/singpass_identity_component.md): Thông tin định danh Singpass, che mờ NRIC và nút toggle Show/Hide NRIC (CLS = 0).
  2. [`mobile_input_component.md`](file:///home/baudui/automation-ui/specs/component_specs/fs08/atomic/mobile_input_component.md): Ô nhập số điện thoại Singapore 8 chữ số (đầu 6/8/9), auto-trim.
  3. [`email_input_component.md`](file:///home/baudui/automation-ui/specs/component_specs/fs08/atomic/email_input_component.md): Ô nhập email RFC 5322, tối đa 150 ký tự, kiểm tra biên BVA 149/150/151.
  4. [`mailing_address_component.md`](file:///home/baudui/automation-ui/specs/component_specs/fs08/atomic/mailing_address_component.md): Cụm trường địa chỉ gửi thư: Block, Street, Unit, Postal Code (6 số), Country.
- **Integration Flows**:
  1. [`parent_profile_view_mode_flow.md`](file:///home/baudui/automation-ui/specs/component_specs/fs08/integration/parent_profile_view_mode_flow.md): Luồng xem hồ sơ và che mờ/hiển thị NRIC Singpass.
  2. [`parent_profile_edit_and_save_flow.md`](file:///home/baudui/automation-ui/specs/component_specs/fs08/integration/parent_profile_edit_and_save_flow.md): Luồng chỉnh sửa, xác thực form và lưu thay đổi với hộp thoại Confirm Dialog.

---

### 3.7. Phân Hệ FS09: Outstanding Fees & Payment (R9)
> Tra cứu và thanh toán học phí: Lựa chọn linh hoạt 3 phương thức (100% Tài khoản Giáo dục EA, 100% Cổng trực tuyến, hoặc Chia đôi Split: EA + Online) kèm cơ chế hoàn tiền bù trừ SAGA an toàn tuyệt đối.

- **Module Index**: [`specs/component_specs/fs09/README.md`](file:///home/baudui/automation-ui/specs/component_specs/fs09/README.md)
- **Atomic Components**:
  1. [`account_selection_card.md`](file:///home/baudui/automation-ui/specs/component_specs/fs09/atomic/account_selection_card.md): Danh sách thẻ tài khoản con cái liên kết, trạng thái nợ học phí (`SCR-01`).
  2. [`outstanding_charges_table.md`](file:///home/baudui/automation-ui/specs/component_specs/fs09/atomic/outstanding_charges_table.md): Bảng danh sách các khoản phí nợ, checkbox từng dòng, Select All (`SCR-02`).
  3. [`payment_method_selector.md`](file:///home/baudui/automation-ui/specs/component_specs/fs09/atomic/payment_method_selector.md): Nhóm 3 phương thức thanh toán (EA, Split, Online) theo số dư khả dụng (`SCR-04`).
  4. [`split_payment_amount_input.md`](file:///home/baudui/automation-ui/specs/component_specs/fs09/atomic/split_payment_amount_input.md): Ô nhập số tiền trích từ EA, kiểm tra biên ($0 < EA < Net$), đồng bộ phần trực tuyến.
- **Integration Flows**:
  1. [`fee_settlement_education_account_flow.md`](file:///home/baudui/automation-ui/specs/component_specs/fs09/integration/fee_settlement_education_account_flow.md): Thanh toán 100% qua Tài khoản Giáo dục EA.
  2. [`fee_settlement_split_payment_flow.md`](file:///home/baudui/automation-ui/specs/component_specs/fs09/integration/fee_settlement_split_payment_flow.md): Thanh toán chia đôi (Split Payment: EA + Cổng trực tuyến).
  3. [`payment_failure_and_refund_saga_flow.md`](file:///home/baudui/automation-ui/specs/component_specs/fs09/integration/payment_failure_and_refund_saga_flow.md): Xử lý lỗi cổng thanh toán và cơ chế hoàn tiền tự động SAGA.

---

### 3.8. Phân Hệ F10: FAS Family Application Portal (R10)
> Cổng nộp đơn FAS trực tuyến cho phụ huynh: Wizard 5 bước nộp đơn gia đình (Children $\rightarrow$ Household & income $\rightarrow$ Documents $\rightarrow$ Context $\rightarrow$ Review & submit), tra cứu thu nhập CPF tự động và theo dõi tiến trình 4 giai đoạn.

- **Module Index**: [`specs/component_specs/f10/README.md`](file:///home/baudui/automation-ui/specs/component_specs/f10/README.md)
- **Atomic Components**:
  1. [`financial_assistance_landing.md`](file:///home/baudui/automation-ui/specs/component_specs/f10/atomic/financial_assistance_landing.md): Trang chủ Financial assistance, nút Apply, Resume/Discard nháp, thẻ Draft card.
  2. [`children_selection.md`](file:///home/baudui/automation-ui/specs/component_specs/f10/atomic/children_selection.md): Wizard Bước 1: Chọn con nộp đơn (Khóa con $\ge 16$ tuổi, có đơn chờ, hoặc form đóng).
  3. [`household_income.md`](file:///home/baudui/automation-ui/specs/component_specs/f10/atomic/household_income.md): Wizard Bước 2: Hộ gia đình & Thu nhập CPF (Tra cứu CPF, tính GHI/PCI, cờ hoàn cảnh ML).
  4. [`documents_upload.md`](file:///home/baudui/automation-ui/specs/component_specs/f10/atomic/documents_upload.md): Wizard Bước 3: Tài liệu hỗ trợ tùy chọn $\le 5\text{ MB}$, Checkbox SBFAS mặc định bật.
  5. [`circumstances_context.md`](file:///home/baudui/automation-ui/specs/component_specs/f10/atomic/circumstances_context.md): Wizard Bước 4: Hoàn cảnh & nguyện vọng (Context $\le 2000$ ký tự, lưu nháp tại Bước 4).
  6. [`review_submit_declaration.md`](file:///home/baudui/automation-ui/specs/component_specs/f10/atomic/review_submit_declaration.md): Wizard Bước 5: Xem lại tổng thể, What happens next, Checkbox cam kết, nộp đơn.
  7. [`application_timeline_tracking.md`](file:///home/baudui/automation-ui/specs/component_specs/f10/atomic/application_timeline_tracking.md): Theo dõi tiến trình 4 giai đoạn (Submitted $\rightarrow$ System check $\rightarrow$ Review $\rightarrow$ Decision), email thông báo.
- **Integration Flows**:
  1. [`online_family_application_flow.md`](file:///home/baudui/automation-ui/specs/component_specs/f10/integration/online_family_application_flow.md): Luồng nộp đơn trực tuyến toàn trình 5 bước.
  2. [`parent_draft_lifecycle_flow.md`](file:///home/baudui/automation-ui/specs/component_specs/f10/integration/parent_draft_lifecycle_flow.md): Vòng đời bản nháp phụ huynh (Auto-save $\rightarrow$ Resume đúng bước $\rightarrow$ Discard).
  3. [`application_lifecycle_decision_flow.md`](file:///home/baudui/automation-ui/specs/component_specs/f10/integration/application_lifecycle_decision_flow.md): Vòng đời xét duyệt, xếp hạng PCI, tự động duyệt MOEFAS và thẩm định SBFAS.

---

## 4. Cross-Module Data Lifecycles & Integration Seams

Hệ thống EAFAMS vận hành như một thực thể thống nhất với các dòng chảy dữ liệu liên phân hệ chặt chẽ:

```mermaid
flowchart LR
    F01["f01: EA Account<br>(Age 7: Created<br>Age 16: Closed)"] -->|EA Number & Balance| F02["f02: Top-Up<br>(Credits Added<br>to EA Balance)"]
    F02 -->|Sufficient Balance| FS09["fs09: Payment<br>(Pay via EA or<br>Split Payment)"]
    
    FS03["fs03: School & Classes<br>(Academic Entities)"] -->|Enrolment Check| F05["f05: Paper Apps<br>(Matched against<br>User School)"]
    FS03 -->|Class Fee Schedule| FS09
    
    F05["f05: Paper Apps<br>(Hardcopy Scans)"] -->|Creates Per-Child Apps| F04["f04: FAS Assessment<br>(MOEFAS Ranking &<br>School SBFAS Decision)"]
    F10["f10: Online Portal<br>(Parent Wizard)"] -->|Creates Family Apps| F04
    
    F04 -->|Subsidies Granted<br>(Fees Waived/Reduced)| FS09
    FS08["fs08: Singpass Profile<br>(Verified Contact)"] -->|Auto-fills Parent Profile| F10
```

1. **Vòng đời Tài khoản Giáo dục $\rightarrow$ Biểu phí & Nạp tiền (`f01` $\rightarrow$ `f02` $\rightarrow$ `fs09`)**:
   - `f01` khởi tạo tài khoản EA khi học sinh tròn 7 tuổi.
   - `f02` nạp tiền theo chiến dịch ngân sách vào tài khoản EA.
   - `fs09` trích tiền từ tài khoản EA để thanh toán học phí do trường ban hành (`fs03`).
2. **Quy trình Trợ cấp Tài chính FAS $\rightarrow$ Giảm trừ Học phí (`f05` / `f10` $\rightarrow$ `f04` $\rightarrow$ `fs09`)**:
   - Phụ huynh nộp đơn online (`f10`) hoặc nộp đơn giấy tại trường (`f05`). Cả hai đều đối chiếu hồ sơ học sinh qua CSDL ghi danh (`fs03`).
   - Các đơn được chuyển về Chức năng 4 (`f04`): Học sinh quốc tịch Singapore được xếp hạng tự động duyệt MOEFAS khi form đóng; học sinh PR được chuyển cho trường xét SBFAS.
   - Khi được duyệt trợ cấp (`Approved`), khoản trợ cấp được áp dụng tự động để xóa hoặc giảm các khoản nợ học phí hiển thị trên cổng thanh toán của phụ huynh (`fs09`).
3. **Định danh Singpass $\rightarrow$ Cổng dịch vụ phụ huynh (`fs08` $\rightarrow$ `f10` / `fs09`)**:
   - `fs08` bảo đảm thông tin họ tên, NRIC và địa chỉ thường trú không bị sửa đổi trái phép.
   - Thông tin liên hệ đã chuẩn hóa từ `fs08` tự động điền vào hồ sơ nộp đơn FAS ở `f10` và biên lai thanh toán ở `fs09`.

---

## 5. Standardized 12-Tier Field Test Matrix & Quality Gates

Mọi tài liệu đặc tả thành phần đơn lẻ (`atomic/*.md`) và ca kiểm thử tự động trong kho mã nguồn đều phải tuân thủ nghiêm ngặt **12 Tầng Kiểm Thử Chuẩn Hóa** theo [`.agent/rules/02-field-test-matrix.md`](file:///.agent/rules/02-field-test-matrix.md):

1. **Tầng 1 (Empty / Required)**: Bỏ trống trường bắt buộc $\rightarrow$ Kích hoạt `aria-invalid="true"`, viền đỏ `#D9383A`, mã lỗi chuẩn `MSG-0001` và thông báo `"Enter your <field>"` / `"Select <field>"`.
2. **Tầng 2 (Whitespace / Trim)**: Khoảng trắng đầu/cuối được tự động trim trước khi kiểm tra (`ASM-15`); chuỗi chỉ chứa toàn khoảng trắng được coi là rỗng.
3. **Tầng 3 (Boundary Value Analysis - BVA)**: Kiểm tra 5 điểm biên chuẩn: $\text{Min}-1$, $\text{Min}$, $\text{Normal}$, $\text{Max}$, $\text{Max}+1$.
4. **Tầng 4 (Ký tự cấm & Đặc thù)**: Kiểm tra bảng mã ký tự cho phép; loại bỏ ký tự điều khiển (U+0000 đến U+001F) ngoại trừ tab/newline trong văn bản nhiều dòng.
5. **Tầng 5 (XSS & Injection Security)**: Payload HTML/JS (`<script>`, `<img onerror>`), SQL Injection (`' OR '1'='1'`) được xử lý dạng plain text, escape HTML an toàn; không bao giờ thực thi mã.
6. **Tầng 6 (Format Chuyên Biệt)**: Định dạng NRIC/FIN Singapore (9 ký tự, checksum chuẩn S/T/F/G/M), Số điện thoại (8 số bắt đầu bằng 6/8/9 - `MSG-0805`), Email (RFC 5322 - `MSG-0806`), Tiền tệ (`S$ #,##0.00`), File scan (PDF/JPG/PNG $\le 10\text{ MB}$ ở F05, $\le 5\text{ MB}$ ở F10).
7. **Tầng 7 (Ràng buộc Nghiệp vụ Chéo)**: Giới hạn độ tuổi 7–16 ở F05, dưới 16 ở F10; Kiểm tra form mở/đóng; Chống trùng lặp NRIC trong cùng hồ sơ gia đình; Đối chiếu trường học của người dùng.
8. **Tầng 8 (Extended Controls)**: Dropdown chọn quan hệ, Checkbox cam kết, Radio phương thức thanh toán, Dialog modal xác nhận.
9. **Tầng 9 (UI Health & Layout Integrity)**: 0 lỗi Console Error, 0 thanh cuộn ngang ngoài ý muốn, WCAG 2.1 AA Contrast Ratio $\ge 4.5:1$, bố cục responsive thích ứng mượt mà.
10. **Tầng 10 (Form Lifecycle & Pristine/Dirty)**: Disable nút submit khi form chưa sửa (pristine); enable khi form dirty; cảnh báo rời trang (beforeunload); chống bấm đúp (double-click debouncing).
11. **Tầng 11 (Bảo mật & PII Protection)**: Che mờ CCCD/NRIC mặc định (`*****123F`), không in log nhạy cảm ra client console, truyền tải an toàn qua HTTPS.
12. **Tầng 12 (Khả Năng Phục Hồi - Resilience)**: Mất mạng đột ngột (Offline mode), timeout API 500, cơ chế tự động thử lại (Retry) và khôi phục bản nháp an toàn.

---

## 6. AI Coding Directives & Verification Protocol

Dành cho tất cả các AI Coding Assistants khi sinh mã nguồn Page Objects, Fixtures và Pytest Suites:
1. **Tuân thủ Tuyệt đối Invariant 0**: Thư mục `copy/` là mã nguồn sản phẩm của công ty, **CẤM TUYỆT ĐỐI CHỈNH SỬA, THÊM, BỚT HOẶC XÓA BẤT KỲ FILE NÀO TRONG `copy/`**.
2. **Tuân thủ Invariant 1 (Zero Assertions in Page Objects)**: Page Objects (`pages/`) và Components (`components/`) CHỈ thực hiện tương tác UI và trích xuất snapshot state. Toàn bộ lệnh `assert` phải nằm trong `tests/`.
3. **Tuân thủ Invariant 2 (Zero Hardcoded Data)**: Không hardcode chuỗi dữ liệu trong code test. Toàn bộ input, BVA vectors và mock payload phải nằm trong `data/<fs_module>/` hoặc fixtures.
4. **Kế thừa 1-1 Traceability (Invariant 3)**: Mọi hàm kiểm thử phải có tên chuẩn `test_tc_<scenario_id>_...` và truy vết về AC ID (`R8-ACxx`), BR ID (`BR-xx`), hoặc FSD Section ID tương ứng trong kho specs này.
5. **Auto-Waiting & Zero `time.sleep()` (Invariant 4)**: Cấm dùng `time.sleep()`. Chỉ sử dụng auto-waiting của Playwright (`wait_for_selector`, `expect(locator)`, `wait_for_load_state`).
6. **Thực thi và Xuất Báo Cáo**:
   ```bash
   # Chạy kiểm thử đơn component
   .venv/bin/pytest tests/<fs_module>/<component>/test_atomic_<feature>_components.py -v
   
   # Chạy kiểm thử tích hợp
   .venv/bin/pytest tests/<fs_module>/<component>/test_integration_<feature>.py -v
   
   # Chạy toàn bộ ticket suite và xuất ExtentReports Dashboard
   python3 run_tests.py --ticket <fs_module>
   ```
