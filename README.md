# Automation UI — Playwright & Pytest Framework

Dự án kiểm thử tự động giao diện tinh gọn, hiệu năng cao xây dựng trên nền tảng **Python 3.10+**, **Playwright (Sync API)** và **Pytest**.
Framework tuân theo mô hình **Page Object Model (POM)** chuẩn mực, phân tách rõ ràng giữa Hành động UI, Dữ liệu kiểm thử và Xác minh nghiệp vụ (Assertions).

---

## 1. Cấu Trúc Dự Án (Flat & Standard Layout)

```
automation-ui/
├── pages/             # Page Object Models: Thao tác UI, đọc DOM (KHÔNG assert)
├── components/        # UI Components tái sử dụng (Header, Sidebar, Modals...)
├── core/              # Hạ tầng chạy test: Browser engine, plugins, error catalog, sanitizer
├── data/              # Dữ liệu test (JSON, fixtures), test data tách biệt với code logic
├── specs/             # Đặc tả màn hình, UI BSK JSONs (SSOT cho locators & error messages)
├── tests/             # Bộ kiểm thử Pytest (BR, AC, Validation, Function Flow)
├── reports/           # Kết quả thực thi: report.html, report.json, screenshots khi fail
├── _legacy_archive/   # Lưu trữ tài liệu, scripts sinh code cũ để tra cứu khi cần
├── pytest.ini         # Cấu hình Pytest tập trung tại root
├── conftest.py        # Master fixtures & plugin delegation
├── requirements.txt   # Các thư viện phụ thuộc
└── AGENTS.md          # Bộ quy chuẩn vàng cho AI và Developers
```

---

## 2. Bốn Nguyên Tắc Vàng (Core Pillars)

1. **Page Object Model (POM) Chuẩn:**
   - `pages/` và `components/` chỉ thực hiện hành động trên UI (`click`, `fill`, `navigate`) và trả về dữ liệu/trạng thái.
   - **Tuyệt đối không viết `assert` trong `pages/` hay `components/`.** Mọi assertions thuộc về file test trong `tests/`.

2. **Dữ Liệu & Locators Chuẩn Xác — CẤM ĐỌC SOURCE CODE (Strict Black-Box):**
   - **Tuyệt đối không đọc mã nguồn code (React `.tsx`, C# `.cs`, API controllers/handlers)** để làm testcase hay lấy selector/thông báo lỗi.
   - Mọi testcase và locators bắt buộc tuân theo kiểm thử hộp đen chuẩn mực: lấy từ **Tài liệu Đặc tả Nghiệp vụ / UAT specs** và **Quét trực tiếp màn hình thực tế (Live DOM Scan qua `bsk`)**.
   - Dữ liệu test nằm trong `data/**/*.json` hoặc Pytest fixtures. Sử dụng `copy.deepcopy` trước khi chỉnh sửa.
   - Selectors và chuỗi thông báo lỗi đối soát trực tiếp từ `specs/ui_bsk/` hoặc Live DOM thực tế. Tuyệt đối không tự suy diễn.

3. **Tập Trung 4 Thành Phần Cốt Lõi (In-Scope Coverage):**
   - **BR (Business Rules):** Logic nghiệp vụ, điều kiện dữ liệu và ràng buộc tính toán.
   - **AC (Acceptance Criteria):** Tiêu chí nghiệm thu của user story.
   - **Validation:** Bắt buộc kiểm tra 3 trạng thái: đúng câu thông báo lỗi, kích hoạt `aria-invalid="true"`/viền đỏ, và tự xóa lỗi khi nhập đúng.
   - **Function Flow:** Luồng thao tác chính (Happy path, Submit, Cancel, Back).

4. **Pytest First & Báo Cáo Minh Chứng:**
   - Chạy test trực tiếp qua lệnh `pytest` tiêu chuẩn.
   - Tự động chụp ảnh màn hình minh chứng giao diện cho cả ca test **PASS** (Actual Result) và **FAIL** (`actual_result.png`).
   - Lưu `report.html` và `report.json` trong thư mục module tương ứng dưới `reports/`, cùng với ảnh minh chứng được nhúng trực tiếp vào báo cáo.

---

## 3. Cài Đặt & Chạy Test

### Cài đặt môi trường

```bash
# Tạo và kích hoạt môi trường ảo Python
python3 -m venv .venv
source .venv/bin/activate

# Cài đặt các thư viện cần thiết
pip install -r requirements.txt

# Cài đặt trình duyệt Playwright
playwright install chromium
```

### Lệnh chạy kiểm thử thường dùng

```bash
# 1. Chạy kiểm tra thu thập test (Verify cú pháp & import không lỗi)
pytest tests --collect-only -q

# 2. Chạy 1 file test cụ thể
pytest tests/unit/test_catalog.py -v

# 3. Chạy toàn bộ test thuộc một module (chạy song song 3 workers)
pytest tests/fs03/ -n 3 -v

# 4. Chạy test và mở trình duyệt trực quan để debug (Headed mode)
pytest tests/fs08/fs08-parent-login/ --headed -v

# 5. Chạy test và tự động lưu báo cáo HTML/JSON trong thư mục module
pytest tests/unit/
```

---

## 4. Báo Cáo & Debug

- Báo cáo thực thi, ảnh/video minh chứng, gói xuất và phiên đăng nhập được giữ cục bộ, không commit lên GitHub. Chỉ commit code, dữ liệu test và tài liệu/testcase nguồn; chạy lại `pytest` để tạo báo cáo.
- Sau mỗi lượt chạy, báo cáo được cập nhật tự động trong thư mục suite tương ứng, ví dụ `reports/testcase5173/01_admin_login_and_sso/`:
  - **HTML Report:** `report.html` (self-contained, mở trực tiếp trên trình duyệt)
  - **JSON Report:** `report.json`
  - **Ảnh lỗi/trace:** `test-results/` dưới cùng thư mục suite; ảnh lỗi cũng được nhúng vào chi tiết test trong HTML.
