# Automation UI — Quy Chuẩn Kiểm Thử Tự Động (Playwright + Pytest)

Dự án kiểm thử tự động giao diện tinh gọn, chuẩn mực sử dụng **Playwright** và **Pytest**.
Mọi thành phần code, kịch bản test và dữ liệu được tối ưu hóa để vận hành nhanh, đơn giản và dễ bảo trì.

---

## 1. Cấu Trúc Dự Án (Flat & Standard Layout)

```
automation-ui/
├── pages/             # Page Object Models: Thao tác UI, tương tác phần tử, đọc state (KHÔNG assert)
├── components/        # UI Components tái sử dụng (Header, Sidebar, Modals...)
├── core/              # Hạ tầng chạy test: Browser engine, plugins, error catalog, sanitizers
├── data/              # Dữ liệu test (JSON, fixtures), test data tách biệt với code logic
├── specs/             # Đặc tả màn hình, UI BSK JSONs (SSOT cho locators & error messages)
├── tests/             # Bộ kiểm thử Pytest (BR, AC, Validation, Function Flow)
├── reports/           # Kết quả thực thi: report.html, report.json, screenshots khi fail
├── _legacy_archive/   # Lưu trữ tài liệu, scripts sinh code cũ để tra cứu khi cần
├── pytest.ini         # Cấu hình Pytest tập trung
└── conftest.py        # Master fixtures & plugin setup
```

---

## 2. Bốn Nguyên Tắc Vàng (Core Pillars)

### ① Page Object Model (POM) Chuẩn
- `pages/` và `components/` chỉ thực hiện hành động trên UI (`click`, `fill`, `navigate`) và trả về trạng thái/dữ liệu (`get_text`, `is_visible`).
- **Tuyệt đối KHÔNG viết câu lệnh `assert` bên trong `pages/` hoặc `components/`.** Mọi assertions thuộc về file test trong `tests/`.

### ② Dữ Liệu & Locators Chuẩn Xác — CẤM ĐỌC SOURCE CODE (Strict Black-Box)
- **TUYỆT ĐỐI KHÔNG ĐỌC SOURCE CODE ĐỂ LÀM TESTCASE HAY LẤY LOCATOR:**
  - Nghiêm cấm Agent đọc mã nguồn triển khai (Frontend React `.tsx`/`.ts`, Backend C# `.cs`, API controllers, handlers trong `copy/` hoặc repos liên quan) để "nhìn trộm" logic, suy diễn kịch bản, hay bóc tách selector/mã lỗi.
  - Testcase phải tuân thủ chuẩn **Kiểm thử Hộp Đen (Pure Black-Box Testing)** đứng từ góc nhìn người dùng cuối và tài liệu yêu cầu.
  - Mọi kịch bản test và bộ định vị BẮT BUỘC chỉ được lấy từ 2 nguồn duy nhất:
    1. **Tài liệu Đặc tả Nghiệp vụ / UAT Specs** (`specs/`, tài liệu BA/FSD, Acceptance Criteria).
    2. **Quét trực tiếp Màn hình Đang Chạy Thực tế (Live DOM Scan qua `bsk`)**: Dùng `bsk` hoặc công cụ browser để quan sát trực quan giao diện, bắt sự kiện và lấy accessibility selectors (Role, Label, Placeholder, Text). Tuyệt đối không dùng class CSS Module nội bộ (như class băm `_input_...`).
- Tất cả dữ liệu test, input biên và payload nằm trong `data/**/*.json` hoặc Pytest fixtures. Sử dụng `copy.deepcopy` trước khi thay đổi dữ liệu.
- Tuyệt đối không tự bịa đặt selector hay chuỗi thông báo lỗi; mọi assertion phải đối soát trực tiếp với UI thực tế đang chạy.

### ③ Test Cases Rõ Ràng & Bám Sát Nghiệp Vụ
- Đặt tên hàm test chuẩn: `test_tc_<scenario_id>_<action>`.
- Mỗi ca test tập trung vào 4 thành phần cốt lõi: **BR** (Quy tắc nghiệp vụ), **AC** (Tiêu chí nghiệm thu), **Validation** (Báo lỗi & kích hoạt viền đỏ `aria-invalid`), và **Function Flow** (Luồng thao tác chính).
- Tránh sinh testcase lan man ngoài lề (không test i18n/đa ngôn ngữ hay đếm từng khoảng trắng trừ khi có yêu cầu cụ thể).
- Assertions cụ thể: Kiểm tra chính xác thông báo hiển thị (Toast/Inline text), trạng thái phần tử (`disabled`, `aria-invalid`), và điều hướng URL. Không assert dựa trên biến code hay log nội bộ của backend/frontend.

### ④ Vận Hành Chuẩn & Báo Cáo Tinh Gọn (Pytest First)
- Không dùng `time.sleep()`; sử dụng cơ chế auto-waiting của Playwright.
- Bằng chứng thực thi: Mỗi ca test **PASS** chỉ chụp **duy nhất 1 hình ảnh** minh chứng kết quả giao diện (`actual_result.png`), tự động nhúng vào báo cáo HTML (`report.html`) và liên kết vào workbook Excel. Ca test **FAIL** chụp ảnh trạng thái lỗi kèm overlay chẩn đoán.
- Xuất báo cáo kép: Khi tạo `report.html`, hệ thống tự động xuất song song file `report.xlsx` trong cùng thư mục (ví dụ `reports/testcase5173/01_admin_login_and_sso/report.xlsx`), cập nhật trạng thái các ca test PASS và nhúng/liên kết ảnh minh chứng trực tiếp vào Excel. `report.json` và ảnh minh chứng nằm cạnh report.

---

## 3. Lệnh Chạy Test Thường Dùng

```bash
# Chạy 1 file test cụ thể
pytest tests/us01_bing_search/test_bing_search.py -v

# Chạy toàn bộ test thuộc một module (chạy song song 3 workers)
pytest tests/fs03/ -n 3 -v

# Chạy test; report.html và report.json tự lưu trong thư mục module tương ứng dưới reports/
pytest tests/fs03/

# Chạy chế độ có giao diện trình duyệt để debug trực quan
pytest tests/us01_bing_search/ --headed -v
```
