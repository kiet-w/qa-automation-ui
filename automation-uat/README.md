# 🧪 EduFAMS Automation UAT & Destructive Testing Suite

Kho lưu trữ toàn bộ kịch bản, dữ liệu mẫu, công cụ thực thi tự động và báo cáo bằng chứng kiểm thử cho các bước nghiệp vụ UAT của hệ thống **EduFAMS**.

---

## 📂 Cấu Trúc Các Bước Thực Thi (Step-by-Step Architecture)

| Thư Mục | Bước Nghiệp Vụ | Màn Hình / URL | Vai Trò Thực Hiện | Trạng Thái | Số Lỗi Phát Hiện |
| :--- | :--- | :--- | :--- | :---: | :---: |
| [`step_01_create_school_user/`](step_01_create_school_user/STEP_01_REPORT.md) | **Bước 1: Tạo Cán Bộ Nhà Trường** | `/school-user-management/new` | Quản trị viên Bộ (`moehq`) | **HOÀN TẤT** | 💥 **2 Bugs** |
| [`step_02_view_as_support_console/`](step_02_view_as_support_console/STEP_02_REPORT.md) | **Bước 2: Giả Lập Vai Trò Trường "View As"** | `/support-console` | Quản trị viên Bộ (`moehq`) | **HOÀN TẤT** | ✅ **Sẵn sàng (8/8 Checkpoints)** |
| [`step_03_1_class_management/`](step_03_1_class_management/STEP_03_1_REPORT.md) | **Mục 3.1: Kiểm tra / Tạo Lớp học** | `/class-management` | Cán bộ trường (`SCHOOL`) | **HOÀN TẤT** | ✅ **Sẵn sàng (Lớp P1-A đã có)** |
| [`step_04_fee_management_and_rate_rules/`](step_04_fee_management_and_rate_rules/README.md) | **Bước 4: Quản Lý Thành Phần Phí & Biểu Phí** | `/fee-management` | Quản trị viên Bộ (`moehq`) | **HOÀN TẤT** | ✅ **Sẵn sàng (9/9 Checkpoints)** |
| [`step_05_fee_batches_and_publication/`](step_05_fee_batches_and_publication/STEP_05_REPORT.md) | **Bước 5: Tạo Đợt Phí & Xuất Bản Nợ Học Phí** | `/fee-batches` | Quản trị viên Bộ (`moehq`) | **HOÀN TẤT** | ✅ **Sẵn sàng (8/8 Checkpoints)** |
| [`step_06_sbfas_scheme_configuration/`](step_06_sbfas_scheme_configuration/STEP_06_REPORT.md) | **Bước 6: Cấu hình Gói Trợ cấp Trường SBFAS** | `/sbfas-schemes` | Cán bộ trường (`staff1@IAM.edu.vn`) | **HOÀN TẤT** | ✅ **Sẵn sàng (9/9 Checkpoints)** |
| [`step_07_fas_assessment/`](step_07_fas_assessment/STEP_07_REPORT.md) | **Bước 7: Thẩm Định & Phê Duyệt Đơn Trợ Cấp SBFAS** | `/fas-applications` | Cán bộ trường (`staff1@IAM.edu.vn`) | **HOÀN TẤT** | ✅ **Sẵn sàng (9/9 Checkpoints)** |
| [`step_08_subsidy_verification_and_handoff_payment/`](step_08_subsidy_verification_and_handoff_payment/STEP_08_REPORT.md) | **Bước 8: Kiểm Tra Giảm Trừ & Bàn Giao Thanh Toán** | `/fee-batches` & `/accounts/STU-001/pay` | Kent & Gavin | **HOÀN TẤT** | ✅ **Sẵn sàng (8/8 Checkpoints)** |

---

## 📌 Nội Dung Chi Tiết Bước 1: Tạo Cán Bộ Nhà Trường

Xem báo cáo đầy đủ tại: **[`step_01_create_school_user/STEP_01_REPORT.md`](step_01_create_school_user/STEP_01_REPORT.md)**

### Thành phần lưu trữ:
- **`STEP_01_REPORT.md`**: Báo cáo tổng hợp kết quả, phân tích 8 ca test và 2 bug chi tiết.
- **`run_step_01_tests.py`**: File Python chạy độc lập mở trình duyệt trực quan và banner HUD.
- **`data/step_01_test_data.json`**: Tập dữ liệu mẫu (Happy path, XSS, SQLi, Buffer overflow, Ghost school).
- **`evidence/`**: 8 ảnh chụp màn hình bằng chứng thực tế khi chạy trên production.

---

## 📌 Nội Dung Chi Tiết Bước 2: Giả Lập Vai Trò Trường "View As"

Xem báo cáo đầy đủ tại: **[`step_02_view_as_support_console/STEP_02_REPORT.md`](step_02_view_as_support_console/STEP_02_REPORT.md)**

### Thành phần lưu trữ:
- **`STEP_02_REPORT.md`**: Báo cáo tổng hợp kết quả chi tiết cho 8 checkpoint kiểm toán và chuyển đổi ngữ cảnh.
- **`run_step_02_tests.py`** / **`run_step_02.py`**: File Python chạy độc lập mở trình duyệt trực quan và banner HUD (slow-mo 500ms).
- **`data/step_02_test_data.json`**: Tập dữ liệu test mẫu (Persona RPS-0201, User staff1, BVA Reason 9/10/500 ký tự, Ticket).
- **`evidence/`**: 8 ảnh chụp màn hình bằng chứng thực tế từng bước thực hiện trên production.

---

## 📌 Nội Dung Chi Tiết Mục 3.1: Kiểm tra hoặc Tạo Lớp học (Classes)

Xem báo cáo đầy đủ tại: **[`step_03_1_class_management/STEP_03_1_REPORT.md`](step_03_1_class_management/STEP_03_1_REPORT.md)**

### Thành phần lưu trữ:
- **`STEP_03_1_REPORT.md`**: Báo cáo tổng hợp kết quả chi tiết cho 5 bước kiểm tra.
- **`run_step_03_1_tests.py`**: File Python chạy độc lập mở trình duyệt trực quan và banner HUD (slow-mo 400ms).
- **`data/step_03_1_test_data.json`**: Tập dữ liệu test mẫu (Lớp P1-A, trùng lặp, validation rỗng, happy path).
- **`evidence/`**: 5 ảnh chụp màn hình bằng chứng thực tế tại từng checkpoint.

---

## 📌 Nội Dung Chi Tiết Bước 4: Quản Lý Thành Phần Phí & Biểu Phí Qua 4 Màn Hình Cụ Thể

Xem báo cáo đầy đủ tại: **[`step_04_fee_management_and_rate_rules/STEP_04_REPORT.md`](step_04_fee_management_and_rate_rules/STEP_04_REPORT.md)**

### Thành phần lưu trữ:
- **`STEP_04_REPORT.md`**: Báo cáo tổng hợp kết quả chi tiết cho 9 checkpoint (4 Màn hình & Cầu nối Bước 5).
- **`run_step_04_tests.py`** / **`run_step_04.py`**: File Python chạy độc lập mở trình duyệt trực quan và banner HUD (slow-mo 500ms).
- **`data/step_04_test_data.json`**: Tập dữ liệu test mẫu (Component Name, School Tuition Fee, Primary, Citizen & PR, Fixed Amount 100 SGD, Date Range BVA).
- **`evidence/`**: 11 ảnh chụp màn hình bằng chứng thực tế từng bước thực hiện trên production/local.

---

## 📌 Nội Dung Chi Tiết Bước 5: Đợt Thu Phí & Xuất Bản Công Nợ (Fee Batches & Publication)

Xem báo cáo đầy đủ tại: **[`step_05_fee_batches_and_publication/STEP_05_REPORT.md`](step_05_fee_batches_and_publication/STEP_05_REPORT.md)**

### Thành phần lưu trữ:
- **`STEP_05_REPORT.md`**: Báo cáo tổng hợp kết quả chi tiết cho 8 checkpoint (UAT-021 & UAT-MOE-01).
- **`run_step_05.py`**: File Python chạy độc lập mở trình duyệt trực quan và banner HUD (slow-mo 600ms).
- **`data/step_05_data.json`**: Tập dữ liệu mẫu (Component Name, Fixed Amount $100.00 SGD, BVA Dates, Student Liam Pham).
- **`evidence/`**: 8 ảnh chụp màn hình bằng chứng thực tế tại từng checkpoint.

---

## 📌 Nội Dung Chi Tiết Bước 6: Cấu Hình Gói Trợ Cấp Trường SBFAS

Xem báo cáo đầy đủ tại: **[`step_06_sbfas_scheme_configuration/STEP_06_REPORT.md`](step_06_sbfas_scheme_configuration/STEP_06_REPORT.md)**

### Thành phần lưu trữ:
- **`STEP_06_REPORT.md`**: Báo cáo tổng hợp kết quả chi tiết cho 9 checkpoint (UAT-SCH-02 & UAT-SCH-02-N1).
- **`run_step_06.py`**: File Python chạy độc lập mở trình duyệt trực quan và banner HUD (slow-mo 600ms).
- **`data/step_06_data.json`**: Tập dữ liệu mẫu (Tier 1, Dates, Budget, GHI/PCI, Add fee, N1 Conflict).
- **`evidence/`**: 9 ảnh chụp màn hình bằng chứng thực tế tại từng checkpoint.

---

## 📌 Nội Dung Chi Tiết Bước 7: Thẩm Định & Phê Duyệt Đơn Trợ Cấp SBFAS

Xem báo cáo đầy đủ tại: **[`step_07_fas_assessment/STEP_07_REPORT.md`](step_07_fas_assessment/STEP_07_REPORT.md)**

### Thành phần lưu trữ:
- **`STEP_07_REPORT.md`**: Báo cáo tổng hợp kết quả chi tiết cho 9 checkpoint (UAT-SCH-03, UAT-SCH-03-N1 & UAT-035).
- **`run_step_07.py`**: File Python chạy độc lập mở trình duyệt trực quan và banner HUD (slow-mo 700ms).
- **`data/step_07_data.json`**: Tập dữ liệu tài khoản, hồ sơ học sinh Ethan Rahman và tham số validation.
- **`evidence/`**: 9 ảnh chụp màn hình bằng chứng thực tế tại từng checkpoint.

---

## 📌 Nội Dung Chi Tiết Bước 8: Kiểm Tra Giảm Trừ & Bàn Giao Thanh Toán

Xem báo cáo đầy đủ tại: **[`step_08_subsidy_verification_and_handoff_payment/STEP_08_REPORT.md`](step_08_subsidy_verification_and_handoff_payment/STEP_08_REPORT.md)**

### Thành phần lưu trữ:
- **`STEP_08_REPORT.md`**: Báo cáo tổng hợp kết quả chi tiết cho 8 checkpoint (Kent ➔ Gavin / UAT-PAR-01, Gates G1-G3).
- **`run_step_08.py`**: File Python chạy độc lập mở trình duyệt trực quan và banner HUD (slow-mo 800ms).
- **`data/step_08_data.json`**: Tập dữ liệu mẫu (Student Liam Pham, Parent Pham Van Duc, EA Wallet EDU-01001, Net amount).
- **`evidence/`**: 11 ảnh chụp màn hình bằng chứng thực tế tại từng checkpoint.

---

## 🌟 Master End-to-End Happy Path (Bước 1 ➔ Bước 8)

Xem đặc tả chi tiết tại: **[`E2E_HAPPY_PATH_QA_SPEC.md`](E2E_HAPPY_PATH_QA_SPEC.md)**

Kịch bản Happy Path kết nối trọn vẹn toàn bộ 8 bước nghiệp vụ trong một lần thực thi duy nhất:
1. **Bước 1:** Quản trị viên Bộ MOE HQ tạo cán bộ nhà trường mới (`/school-user-management/new`).
2. **Bước 2:** Chuyển ngữ cảnh sang trường Rosyth Primary School qua Support Console (`/support-console`).
3. **Bước 3:** Kiểm tra và xác nhận Lớp `P1-A` sẵn sàng (`/class-management`).
4. **Bước 4:** Cấu hình Thành phần phí `Tuition Fee UAT` và Biểu phí Cố định `SGD 100.00` (`/fee-management`).
5. **Bước 5:** Khởi tạo Đợt thu phí, kiểm tra Preview không sinh nợ thật, và Publish công nợ `POSTED` (`/fee-batches`).
6. **Bước 6:** Cán bộ trường tạo Gói trợ cấp `SBFAS Tier 1` miễn giảm 100% học phí và Publish (`/sbfas-schemes`).
7. **Bước 7:** Cán bộ trường thẩm định và phê duyệt Đơn trợ cấp của học sinh (`/fas-applications`).
8. **Bước 8:** Đối soát công nợ đã giảm trừ (Net Amount) và Phụ huynh thanh toán thành công qua ví Edusave EA (`/accounts/STU-001/pay`).

### Thành phần Master Runner:
- **`run_e2e_happy_path.py`**: Trình điều khiển trực quan có HUD và Highlight từng thao tác.
- **`data/e2e_happy_path_data.json`**: Tập dữ liệu mẫu thống nhất cho cả 8 bước.
- **`tests/uat/test_e2e_happy_path.py`**: Bộ test chuẩn Pytest + Playwright phục vụ CI/CD.

---

## 🚀 Hướng Dẫn Chạy Nhanh

```bash
# 🌟 Chạy toàn bộ luồng Happy Path (Từ Bước 1 đến Bước 8 liên tục có giao diện HUD):
.venv/bin/python automation-uat/run_e2e_happy_path.py --headed --slow-mo 400 --hold 10

# Chạy Happy Path ở chế độ không giao diện (Headless):
.venv/bin/python automation-uat/run_e2e_happy_path.py --headless

# Chạy thông qua Pytest Suite UAT End-to-End:
pytest tests/uat/test_e2e_happy_path.py -v

# Chạy từng bước độc lập:
# Bước 1:
.venv/bin/python automation-uat/step_01_create_school_user/run_step_01_tests.py --url https://admin.20-255-158-192.sslip.io --slow-mo 500
# Bước 2:
.venv/bin/python automation-uat/step_02_view_as_support_console/run_step_02_tests.py --url https://admin.20-255-158-192.sslip.io --headed --slow-mo 500
# Bước 3.1:
.venv/bin/python automation-uat/step_03_1_class_management/run_step_03_1_tests.py --url https://admin.20-255-158-192.sslip.io --headed --slow-mo 400
# Bước 4:
.venv/bin/python automation-uat/step_04_fee_management_and_rate_rules/run_step_04.py --url https://admin.20-255-158-192.sslip.io --headed --slow-mo 500 --hold 15
# Bước 5:
.venv/bin/python automation-uat/step_05_fee_batches_and_publication/run_step_05.py --headed --slow-mo 600 --hold 15
# Bước 6:
.venv/bin/python automation-uat/step_06_sbfas_scheme_configuration/run_step_06.py --headed --slow-mo 600 --hold 15
# Bước 7:
.venv/bin/python automation-uat/step_07_fas_assessment/run_step_07.py --headed --slow-mo 700 --hold 15
# Bước 8:
.venv/bin/python automation-uat/step_08_subsidy_verification_and_handoff_payment/run_step_08.py --headed --slow-mo 800 --hold 15

# Chạy toàn bộ thư mục tests/uat/ qua Pytest:
pytest tests/uat/ -v
```
