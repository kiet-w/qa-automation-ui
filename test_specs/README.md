# Hướng Dẫn Vận Hành Hệ Thống UI Automation Markdown Tinh Gọn

Hệ thống kết hợp **4 Tầng Kiểm Thử Toàn Diện (4-Tier UI Testing Architecture)**:
1. ⚡ **Atomic Test Cases (UI Unit Test)**: Kiểm tra **ĐƠN COMPONENT** độc lập trên UI (1 input, 1 dropdown, 1 button, validate rỗng/biên/regex) (`test_specs/atomic/` - `@smoke`, `@p0`, `@atomic`).
2. 🔗 **Integration Test Cases (UI Integration Test)**: Kiểm tra **TƯƠNG TÁC GIỮA CÁC COMPONENT** (1 Component ➔ 1 Component khác, 1 Component ➔ Nhiều Component, hoặc Form 🔁 API mock status 200/400/500) (`test_specs/integration/` - `@integration`, `@api`).
3. 🚀 **UAT User Journeys**: Luồng người dùng hoàn chỉnh xuyên trang, giữ session liên tục (`test_specs/uat/` - `@uat`, `@journey`).
4. 💥 **Break_It Resilience**: Phá có kỷ luật, gỡ ràng buộc client, double click, 500 chaos (`test_specs/break_it/` - `@break_it`, `@adversarial`).

---

## 1. Trinh Sát DOM Trước Khi Viết Test (Chống Bịa Locator)

> [!WARNING]
> **VAI TRÒ DUY NHẤT CỦA BSK LÀ SCAN LOCATOR**:
> BSK **KHÔNG PHẢI LÀ TEST RUNNER**. BSK chỉ dùng để mở web thật, quét cây DOM và trích xuất selector chuẩn 100%. Toàn bộ việc thực thi test là do Playwright Python (`md_runner.py`) đảm nhiệm!

Trước khi viết bất kỳ file `.md` nào, hãy dùng công cụ trinh sát DOM tự động:

```bash
# Trinh sát trang web thật hoặc mock page
python3 tools/recon_bsk.py --url curricula_trainer_account.html

# Xuất thẳng bảng locator vào file markdown mới
python3 tools/recon_bsk.py --url curricula_trainer_account.html --output test_specs/my_feature.md
```

Kết quả sinh ra bảng tra cứu chính xác 100% để paste vào đầu file `.md`:
```markdown
## 🔍 Locators đã xác minh qua BSK (Browser-Skill Reconnaissance)
| Tên Phần Tử | Nhãn Hiển Thị | Selector / ID Thực Tế | Loại Phần Tử |
| :--- | :--- | :--- | :--- |
| preferredName | preferredName | `#preferredName` | `<input type="text">` |
| Save Button | Save | `#saveBtn` | `<button>` |
```

---

## 2. Cú Pháp Viết Kịch Bản

### A. Dạng Danh Sách Tự Nhiên (Natural Steps - Phù hợp UAT & Happy Path)
```markdown
# Feature: UAT End-to-End User Journeys

## Scenario: UAT-01 Trainer Full Onboarding Flow @uat @journey
- Open: curricula_trainer_account.html
- Assert: Title contains "Curricula"
- Fill: #preferredName with "Dr. Alexandra Tan"
- Click: #cancelBtn
- Assert: Title contains "Curricula"
```

### B. Dạng Bảng Dữ Liệu (Data Table - Phù hợp Atomic & Break_It)
```markdown
# Feature: Curricula Adversarial & Resilience Testing (Break_It)

## Scenario: TC-BRK-001 Strip Client Constraints and Verify Defense @break_it @p0
| Step | Action | Target / Selector | Value | Expected / Assertion |
| :--- | :--- | :--- | :--- | :--- |
| 1 | open | curricula_trainer_account.html | | Mở trang thành công |
| 2 | strip_constraints | | | Gỡ sạch required, maxlength, disabled |
| 3 | click | #saveBtn | | Submit khi client validation đã bị xóa |
| 4 | assert_visible | .error[data-for="preferredName"] | | Backend vẫn phải từ chối an toàn |
| 5 | assert_not_visible | #successBox | | Không tạo dữ liệu rác |
```

---

## 3. Danh Mục Lệnh Thực Thi & Thao Tác Phá

| Nhóm | Lệnh (`Action`) | Tham số (`Target / Value`) | Ý nghĩa hành vi |
| :--- | :--- | :--- | :--- |
| **Cơ bản** | `open` / `goto` | `url` | Mở trang web hoặc mock HTML |
| | `fill` | `selector` \| `value` | Nhập văn bản với auto-wait |
| | `click` | `selector` | Click vào phần tử |
| | `dblclick` | `selector` | Double-click (kiểm tra race condition) |
| | `select` | `selector` \| `option` | Chọn dropdown theo label hoặc value |
| | `check` / `uncheck` | `selector` | Đánh dấu hoặc bỏ chọn checkbox/radio |
| | `press` | `key` (Enter, Escape, Tab) | Thao tác bàn phím |
| | `wait` | `1s`, `500ms` | Tạm dừng thời gian ngắn |
| **💥 Break_It** | `strip_constraints` | *(trống)* | Xóa sạch `required`, `disabled`, `maxlength` |
| | `force_fill` | `selector` \| `payload` | Bơm chuỗi qua prototype setter (vượt client) |
| | `enable` | `selector` | Gỡ disabled của nút và ép thao tác |
| | `mock_status` | `url_pattern` \| `500` | Giả lập máy chủ sập HTTP 500 / 502 |
| | `set_viewport` | `375x667` | Chuyển đổi kích thước Mobile / Desktop |
| **Kiểm tra** | `assert_visible` | `selector` | Phần tử hiển thị trên màn hình |
| | `assert_not_visible` | `selector` | Phần tử không hiển thị |
| | `assert_contains` | `selector` \| `text` | Chứa đoạn văn bản kỳ vọng |
| | `assert_disabled` | `selector` | Phần tử đang bị khóa (disabled) |
| | `assert_no_overflow` | *(trống)* | Không có thanh cuộn ngang vỡ layout |
| | `assert_no_console_errors`| *(trống)* | 0 lỗi đỏ Uncaught JS trong console |

---

## 4. Lệnh Vận Hành CLI

```bash
# 1. Chạy toàn bộ 4 tầng test suites (Atomic, Integration, UAT, Break_It)
python3 md_runner.py

# 2. Chạy riêng nhánh Integration (Tích hợp UI 🔁 API)
python3 md_runner.py --tags @integration

# 3. Chạy riêng nhánh Break_It (Vợt lỗi ngầm, bảo mật, validate)
python3 md_runner.py --tags @break_it

# 4. Chạy riêng luồng UAT
python3 md_runner.py --tags @uat

# 5. Chạy riêng Smoke / UI Unit Test nhanh
python3 md_runner.py --tags @smoke

# 5. Mở trình duyệt xem trực tiếp
python3 md_runner.py --headed --slowmo 200

# 6. Tự động mở báo cáo sau khi chạy xong
python3 md_runner.py --open-report
```

---

## 5. Báo Cáo Kết Quả

Hệ thống tự động biên dịch báo cáo đồ họa 1 trang duy nhất:
* 🎯 **Báo cáo Tinh Gọn**: [reports/uat/bao_cao_tinh_gon.html](file:///home/baudui/automation-ui/reports/uat/bao_cao_tinh_gon.html) (Có nhãn `[ATOMIC]`, `[UAT JOURNEY]`, `[BREAK_IT]`, nút nhảy lỗi 1-click).
* 🎬 **Báo cáo ExtentReports chi tiết**: [reports/uat/execution_report.html](file:///home/baudui/automation-ui/reports/uat/execution_report.html) (Nhúng sẵn video WebM quay lại toàn bộ màn hình khi chạy).

---

## 6. Quy Chuẩn Thiết Kế Đặc Tả Test Case Markdown & Đồng Bộ Excel (Granular Input-Specific & 19-Column AvePoint Standard)

Mọi tài liệu test case đặc tả trong `testcases/` và `test_specs/` đều tuân thủ kiến trúc kiểm thử chuyên sâu theo `/combo-qa`:

### A. Nguyên Tắc Phân Tách Test Suite & Scenario ID
* **Tuyệt đối không gom phẳng Test Suite**: Không đặt tên Test Suite chung chung như `My Details` hay `My Profile` cho tất cả các kịch bản của một trang.
* **Phân rã thành từng Test Suite độc lập cho từng Component/Input**:
  * Định danh SingPass: `TS-<SEQ>-ID` (Full Name, NRIC masking, Residential Address).
  * Từng ô Input riêng lẻ: `TS-<SEQ>-TEL` (Phone), `TS-<SEQ>-EML` (Email), `TS-<SEQ>-BLK` (Block), `TS-<SEQ>-UNT` (Unit), `TS-<SEQ>-STR` (Street), `TS-<SEQ>-POS` (Postal Code), `TS-<SEQ>-CTY` (Country).
  * Trạng thái giao diện: `TS-<SEQ>-STA` (View $\leftrightarrow$ Edit mode, Pristine disabled, Dirty enabled).
  * Hộp thoại xác nhận: `TS-<SEQ>-SUB` (Modal alertdialog, Keep editing, Confirm Save, Debounce, Toast `MSG-xxxx`).
  * Phân quyền & Vòng đời: `TS-<SEQ>-AGE` (Theo độ tuổi, BOLA/IDOR `MSG-0003`, Độc lập hồ sơ).
  * Phi chức năng UI: `TS-<SEQ>-NFR` (Invariant 7: 0 Console Errors, Zero Horizontal Scroll, WCAG 2.1 AA).

### B. Bao Phủ Kỹ Thuật Black-Box Cho Từng Trường Nhập Liệu
1. **Phân vùng tương đương (EP)**: Tập dữ liệu hợp lệ (Valid) và không hợp lệ (Invalid).
2. **Phân tích giá trị biên (BVA 2-point/3-point)**: Đo lường độ dài ký tự tối thiểu, tối đa ($N, N-1, N+1$) chống tràn bộ đệm cơ sở dữ liệu.
3. **Validate rỗng trường bắt buộc**: Xóa trắng từng trường kiểm tra lỗi `MSG-0001` độc lập.
4. **Xử lý khoảng trắng (`ASM-15`)**: Nhập toàn khoảng trắng bị tính là rỗng và kích hoạt `MSG-0001`.
5. **Định dạng đặc thù & Regex**: Cú pháp email RFC 5322 (`MSG-0806`), số điện thoại Singapore đầu 6/8/9 (`MSG-0805`), bảo toàn số 0 ở đầu mã bưu chính (`018956`).
6. **Bảo mật bề mặt (Security/XSS)**: Thử nghiệm vector `<script>alert(1)</script>` để kiểm tra mã hóa HTML an toàn.

### C. 5 Khối Nội Dung Bắt Buộc Trong File Markdown Đặc Tả
1. **Khối 1: Bảng tổng quan phân bổ Test Suites & Input Components**: STT, Scenario ID, Tên Suite, Loại phần tử/Input, Kỹ thuật QA, Số lượng TC, Mức ưu tiên.
2. **Khối 2: Ma trận Test Case chi tiết đủ 19 cột chuẩn Google Sheet AvePoint Tender**:
   `ID` | `Scenario ID` | `Title` | `Test Suite` | `Page` | `Severity` | `Priority` | `Execution Status` | `Test Type` | `Environment` | `Preconditions` | `Test Data` | `Test Steps` | `Expected Result` | `Actual Result` | `Assumption Ref` | `Defect ID` | `Traceability` | `Note`.
3. **Khối 3: Bảng tra cứu Locator Live DOM từ BSK**: Trích xuất selector chuẩn từ `recon_bsk.py`.
4. **Khối 4: Fixture dữ liệu kiểm thử (JSON Fixtures)**: Bộ dữ liệu baseline, mutation, boundary và XSS payload.
5. **Khối 5: Bảng Traceability đối soát FSD, AC & Error Catalog**: Đối soát 2 chiều với FSD Section ID, AC ID, Quyết định họp (`D-xx`), Mã thông báo lỗi (`MSG-xxxx`).

### D. Đồng Bộ File Excel Đi Kèm (.xlsx)
* Tự động sinh file Excel cùng tên bằng `tools/generate_19col_xlsx.py` với styling chuẩn AvePoint Tender:
  * Header navy `#001B365D`, font Segoe UI 10pt bold, chữ trắng.
  * Cột ID/Scenario ID font Consolas 9pt bold.
  * Thin border `#00D3D3D3`, wrap_text, pinned freeze panes `A2`, kích hoạt auto-filter toàn bảng.
