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

### ② Dữ Liệu & Locators Chuẩn Xác (Zero Guesswork)
- Tất cả dữ liệu test, input biên và payload nằm trong `data/**/*.json` hoặc Pytest fixtures. Sử dụng `copy.deepcopy` trước khi thay đổi dữ liệu.
- Bộ định vị (selectors) và thông báo lỗi BẮT BUỘC đối soát từ file đặc tả `specs/ui_bsk/` hoặc DOM thực tế. Tuyệt đối không tự bịa đặt selector hay chuỗi thông báo lỗi.

### ③ Test Cases Rõ Ràng & Bám Sát Nghiệp Vụ
- Đặt tên hàm test chuẩn: `test_tc_<scenario_id>_<action>`.
- Mỗi ca test tập trung vào 4 thành phần cốt lõi: **BR** (Quy tắc nghiệp vụ), **AC** (Tiêu chí nghiệm thu), **Validation** (Báo lỗi & kích hoạt viền đỏ `aria-invalid`), và **Function Flow** (Luồng thao tác chính).
- Tránh sinh testcase lan man ngoài lề (không test i18n/đa ngôn ngữ hay đếm từng khoảng trắng trừ khi có yêu cầu cụ thể).
- Assertions cụ thể: Kiểm tra chính xác thông báo hiển thị (Toast/Inline text), trạng thái phần tử (`disabled`, `aria-invalid`), và điều hướng URL.

### ④ Vận Hành Chuẩn & Báo Cáo Tinh Gọn (Pytest First)
- Không dùng `time.sleep()`; sử dụng cơ chế auto-waiting của Playwright.
- Bằng chứng thực thi: Chỉ tự động chụp ảnh màn hình khi test **FAIL** (`--screenshot=only-on-failure`), tiết kiệm tài nguyên và tăng tốc độ chạy test.
- Xuất báo cáo trực quan 1 file duy nhất qua `pytest-html` tại `reports/report.html`.

---

## 3. Lệnh Chạy Test Thường Dùng

```bash
# Chạy 1 file test cụ thể
pytest tests/us01_bing_search/test_bing_search.py -v

# Chạy toàn bộ test thuộc một module (chạy song song 3 workers)
pytest tests/fs03/ -n 3 -v

# Chạy test và xuất file báo cáo HTML
pytest tests/fs03/ --html=reports/report.html --self-contained-html

# Chạy chế độ có giao diện trình duyệt để debug trực quan
pytest tests/us01_bing_search/ --headed -v
```
