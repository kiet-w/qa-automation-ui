# Phân Hệ UAT: Bước 4: Quản Lý Thành Phần Phí & Biểu Phí Qua 4 Màn Hình Cụ Thể

Tài liệu ghi nhận chi tiết kịch bản, bộ định vị, công cụ thực thi trực quan (**Visual Headed Automation với Live HUD & Wayland Support**) và báo cáo kiểm thử cho **Bước 4: Fee Management & Rate Rules Flow** của Cổng Quản trị EduFAMS.

---

## 📌 1. Thông Tin Phiên Kiểm Thử

| Thông Tin | Giá Trị Chi Tiết |
| :--- | :--- |
| **Hạng Mục UAT** | **Bước 4: Quản Lý Thành Phần Phí & Thiết Lập Biểu Phí (4 Màn Hình & Cầu Nối Bước 5)** |
| **Môi Trường Target** | `https://admin.20-255-158-192.sslip.io` (hoặc `https://localhost:5173`) |
| **Các Màn Hình Kiểm Thử** | 1. `/fee-management` (Tổng quan Danh mục Phí)<br/>2. `/fee-management/components/new` (Wizard Bước 1 - Tạo Khung Pháp Lý)<br/>3. `/fee-management/components/:id/rate-rules/new` (Wizard Bước 2 - Thiết Lập Biểu Phí Chế Độ A)<br/>4. `/fee-management/components/:id` (Chi Tiết & Oracle Xác Nhận Active)<br/>5. `/fee-batches/new?feeComponentId=...` (Cầu Nối Sang Bước 5 - Tạo Đợt Thu Học Phí) |
| **Vai Trò Thực Hiện** | **Quản trị viên Bộ Giáo dục (MOEHQ / System Admin)** |
| **Tài Khoản Test** | `admin@IAM.edu.vn` |
| **Chế Độ Chạy** | Headed Browser (Hiển thị trực tiếp trên màn hình Wayland/Hyprland với Live HUD banner, làm nổi bật viền phần tử DOM, pacing `slow_mo=500ms`, `hold=15s`) |
| **Trạng Thái Chung** | ✅ **HOÀN THÀNH TOÀN BỘ (9/9 Checkpoints PASS - 0 WARNING - 0 FAIL)** |

---

## 🚀 2. Hướng Dẫn Chạy Nhanh

```bash
# 1. Chạy trực quan có giao diện trình duyệt và Live HUD trên Production/Remote:
.venv/bin/python automation-uat/step_04_fee_management_and_rate_rules/run_step_04.py --url https://admin.20-255-158-192.sslip.io --headed --slow-mo 500 --hold 15

# 2. Chạy trực quan có giao diện trình duyệt trên Localhost:
.venv/bin/python automation-uat/step_04_fee_management_and_rate_rules/run_step_04.py --url https://localhost:5173 --headed --slow-mo 500 --hold 15

# 3. Chạy chế độ headless nền:
.venv/bin/python automation-uat/step_04_fee_management_and_rate_rules/run_step_04.py --headless

# 4. Chạy thông qua bộ kiểm thử Pytest UAT:
pytest tests/uat/test_uat_4_fee_management_and_rate_rules.py -v
```

---

## 📋 3. Chi Tiết Thao Tác Qua 4 Màn Hình Cụ Thể

### 📍 Màn 1: Khởi Động Tại `/fee-management`
- **Mục đích**: Xem các loại phí có sẵn (`TUITION`, `MISC`, `ENRICHMENT`).
- **Hành động khảo sát**:
  - **Cách 1**: Truy cập thẳng link `/fee-management/components/new`.
  - **Cách 2**: Bấm nút **View** tại dòng School Tuition Fee $\rightarrow$ Bấm link **Create fee component**.
- **Kết quả thực tế**:
  - Hiển thị bảng Fee Types với đầy đủ các loại phí đang hoạt động.
  - Điều hướng thành công đến form Tạo mới Thành phần Phí.

---

### 📍 Màn 2: Wizard Bước 1 — Khai Báo Thành Phần Phí (`/components/new`)
- **Mục đích**: Tạo khung pháp lý cho khoản thu (chưa nhập số tiền).
- **Kiểm thử Validation**:
  - Để trống trường Name và bấm submit $\rightarrow$ Hệ thống chặn và kích hoạt ràng buộc bắt buộc nhập.
- **Khai báo Happy Path**:
  1. **Name** (`#fee-component-name`): `Tuition Fee 2026 <timestamp>`
  2. **Fee type** (`#fee-type`): `School Tuition Fee`
  3. **Student categories** (`#fee-categories`): `Singapore Citizen`, `Permanent Resident`
  4. **Education stages** (`#fee-stages`): `Primary`
  5. **Tax applies** (`#fee-tax`): `Yes` (tích chọn)
- **Hành động chuyển bước**: Bấm **Continue to rates** (`button[type="submit"]`).
- **Hệ thống xử lý**: Tạo bản ghi Component trong Database và tự động lấy `id` vừa tạo chuyển hướng sang Wizard Bước 2 (`/rate-rules/new`).

---

### 📍 Màn 3: Wizard Bước 2 — Thiết Lập Biểu Phí & Thời Hạn (`/rate-rules/new`)
- **Mục đích**: Gán số tiền cụ thể và đặt khoảng thời gian bảng giá có hiệu lực.
- **Kiểm thử BVA Validation**:
  - Nhập ngày hiệu lực đảo ngược: `Effective from = 2026-12-31` > `Effective to = 2026-01-01` $\rightarrow$ Hệ thống chặn submit và giữ form hợp lệ.
- **Thiết lập Chế độ A — Fixed Amount (Đồng loạt một mức giá)**:
  1. Chọn radio **Fixed Amount** (`input[value="fixed-amount"]`).
  2. Điền số tiền vào ô **Amount** (`input#fixed-amount`): `100.00`.
  3. Ô **Currency** (`input#fixed-currency`): Mặc định sẵn `SGD`.
  4. Điền ngày hiệu lực của mức giá:
     - **Effective from** (`input#fixed-from`): `2026-01-01`
     - **Effective to (exclusive)** (`input#fixed-to`): `2026-12-31`
- **Hành động kết thúc**: Bấm nút **Save rates** (`button[type="submit"]`).

---

### 📍 Màn 4: Màn Hình Chi Tiết Thành Phần Phí (`/components/:feeComponentId`)
- **Mục đích**: Kiểm tra lại thông tin sau khi cấu hình thành công (Oracle xác nhận PASS).
- **Kết quả quan sát thực tế**:
  - Bảng Fee rate rules hiển thị các dòng tương ứng: Cấp học `Primary`, Đối tượng `Singapore Citizen` & `Permanent Resident`, Mức giá `$100.00 SGD`, Ngày hiệu lực `2026-01-01` đến `2026-12-31`.
  - Trạng thái component hiển thị đầy đủ thông tin biểu phí hoạt động.
  - Trên đỉnh trang hiển thị nút chức năng: **`Publish batch from this Fee Component`**.

---

### 📍 Cầu Nối Sang Bước 5 (`/fee-batches/new`)
- **Hành động**: Bấm nút **Publish batch from this Fee Component**.
- **Kết quả thực tế**:
  - Điều hướng thành công sang `/fee-batches/new?feeComponentId=...` mang theo đúng ID vừa tạo để bắt đầu quy trình tạo đợt thu học phí và chốt công nợ.

---

## 💡 4. Tóm Tắt Khác Biệt Giữa 3 Loại "Ngày Tháng"

| Khái Niệm Ngày | Xuất Hiện Ở Đâu? | Ý Nghĩa Nghiệp Vụ Thực Tế |
| :--- | :--- | :--- |
| **`Effective from` & `Effective to (exclusive)`** | Wizard Bước 2 (`/rate-rules/new`) | **Hiệu lực của Biểu giá**: Mức giá 100 SGD này được phép sử dụng từ ngày nào đến ngày nào. `Effective to` mang tính loại trừ (exclusive). |
| **`Period Start` & `Period End`** | Bước 5 (`/fee-batches/new`) | **Kỳ thu học phí**: Tiền thu cho học kỳ nào (ví dụ: Học kỳ 1 từ 01/01/2026 đến 30/06/2026). Kỳ này phải nằm trong khoảng hiệu lực của Biểu giá ở Bước 4. |
| **`Charge Date` & `Due Date`** | Bước 5 (`/fee-batches/new`) | **Hạn nợ**: Ngày phát hành hóa đơn (`Charge Date`) và Hạn chót phụ huynh phải thanh toán (`Due Date`). |

---

## 📸 5. Bảng Tổng Hợp Kết Quả Thực Thi 9 Checkpoints

| Checkpoint | Hạng Mục Kiểm Thử | Trạng Thái | Chi Tiết Ghi Nhận Thực Tế | Ảnh Minh Chứng |
| :---: | :--- | :---: | :--- | :--- |
| `CP-01` | **Màn 1: Khởi động tại /fee-management** | ✅ **PASS** | Bảng Fee Types hiển thị đầy đủ danh mục loại phí đang hoạt động | [01_fee_management_overview.png](evidence/01_fee_management_overview.png) |
| `CP-02` | **Màn 1 Cách 2: View -> Create Fee Component** | ✅ **PASS** | Điều hướng thành công đến form Tạo mới Thành phần Phí (/components/new) | [02_navigated_to_create_component.png](evidence/02_navigated_to_create_component.png) |
| `CP-03` | **Màn 2: Validation Empty Name** | ✅ **PASS** | Hệ thống chặn submit và kích hoạt trạng thái không hợp lệ (Required field constraint) | [03_step1_empty_name_validation.png](evidence/03_step1_empty_name_validation.png) |
| `CP-04` | **Màn 2: Khai báo Thành phần Phí** | ✅ **PASS** | Khai báo thành công: Name, Cấp học: Primary, Đối tượng: SC & PR, Tax: Yes | [04_step1_form_filled_successfully.png](evidence/04_step1_form_filled_successfully.png) |
| `CP-05` | **Màn 3: Tự động chuyển hướng sang /rate-rules/new** | ✅ **PASS** | URL mang theo ID vừa tạo của component tự động | [05_step2_rate_rules_screen_loaded.png](evidence/05_step2_rate_rules_screen_loaded.png) |
| `CP-06` | **Màn 3: Validation Date Range** | ✅ **PASS** | Hệ thống chặn submit, giữ form tại /rate-rules/new khi From > To | [06_step2_inverted_dates_validation.png](evidence/06_step2_inverted_dates_validation.png) |
| `CP-07` | **Màn 3: Thiết lập Biểu phí Chế độ A** | ✅ **PASS** | Lưu thành công biểu phí 100.00 SGD có hiệu lực 2026-01-01 đến 2026-12-31 (exclusive) | [07_saved_rates_redirected.png](evidence/07_saved_rates_redirected.png) |
| `CP-08` | **Màn 4: Chi tiết Thành phần Phí & Oracle PASS** | ✅ **PASS** | Hiển thị biểu phí $100.00 SGD, ngày hiệu lực và nút 'Publish batch from this Fee Component' | [08_component_detail_active.png](evidence/08_component_detail_active.png) |
| `CP-09` | **Cầu nối sang Bước 5 (Tạo đợt thu học phí)** | ✅ **PASS** | Điều hướng thành công sang: `/fee-batches/new?feeComponentId=...` | [09_navigated_to_fee_batches_new.png](evidence/09_navigated_to_fee_batches_new.png) |

---

## 📂 6. Cấu Trúc Thành Phần

```
automation-uat/step_04_fee_management_and_rate_rules/
├── README.md                  # Hướng dẫn nghiệp vụ, kỹ thuật & vận hành chi tiết
├── STEP_04_REPORT.md          # Báo cáo tổng hợp UAT tự động xuất sau mỗi lần chạy
├── run_step_04.py             # Script thực thi trực quan có Live HUD & Wayland support
├── run_step_04_tests.py       # Alias tiêu chuẩn tương đương
├── data/
│   └── step_04_test_data.json # Dữ liệu mẫu Happy Path, BVA Ngày, Cấp học & Đối tượng
└── evidence/                  # 11 ảnh chụp màn hình minh chứng phân giải cao tại các checkpoints
```
