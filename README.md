# Automation UI - Playwright & Pytest Framework

Dự án kiểm thử tự động giao diện (UI Automation) xây dựng trên nền tảng **Playwright** và **Pytest**, áp dụng mô hình **Page Object Model (POM)** và thiết kế thành phần UI tái sử dụng (Component-based).

---

## 🚀 Hướng dẫn Cài đặt & Khởi tạo

1. **Chuẩn bị môi trường ảo Python**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   # hoặc: .venv\Scripts\activate  # Windows
   ```

2. **Cài đặt các thư viện phụ thuộc**:
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

---

## 🎯 Hướng dẫn Thực thi Kiểm thử

Script điều phối `run_tests.py` giúp tự động hóa toàn diện quy trình kiểm thử theo 2 pha liên tiếp:
- **Pha 1**: Chạy kiểm thử với Pytest, stream log trực tiếp ra console và lưu kết quả vào `reports/report.json`.
- **Pha 2**: Kích hoạt `generate_report.py` để chuyển đổi dữ liệu JSON thành báo cáo HTML tương tác, tự chứa (self-contained) tại `reports/execution_report.html`.

### 1. Chạy mặc định (Tất cả test case)
```bash
python run_tests.py
```
> Thực thi kiểm thử tuần tự với các cấu hình định sẵn trong `pytest.ini` và tự động sinh báo cáo HTML sau khi hoàn tất.

### 2. Chạy song song đa tiến trình (Parallel Workers)
```bash
python run_tests.py -n 4
```
> Kích hoạt 4 worker chạy đồng thời an toàn bằng `pytest-xdist`. Script `run_tests.py` sẽ đồng bộ và đợi toàn bộ các worker kết thúc trước khi tổng hợp báo cáo.

### 3. Lọc bài test theo Marker hoặc Tên
- Chạy theo Marker:
  ```bash
  python run_tests.py -m search
  ```
- Chạy theo tên bài test hoặc từ khóa:
  ```bash
  python run_tests.py -k test_user_story_1
  ```
- Chạy chế độ Headless / Headed:
  ```bash
  python run_tests.py --headed
  ```

---

## 📊 Chỉ Sinh Lại Báo Cáo (Không chạy lại Test)

Khi đã có file dữ liệu `reports/report.json` từ lần chạy trước, bạn có thể tạo lại file HTML báo cáo bất cứ lúc nào mà không cần chạy lại toàn bộ test suite:

```bash
python generate_report.py
```
Hoặc chỉ định file dữ liệu tùy chỉnh:
```bash
python generate_report.py reports/report.json
```

Báo cáo kết quả sẽ được tạo tại:
- **Đường dẫn**: `reports/execution_report.html`
- **Tính năng nổi bật**:
  - Tự chứa 100% (self-contained), có thể gửi qua email hoặc lưu trữ CI/CD mà không mất dữ liệu.
  - Interactive SVG Step Pipeline (biểu diễn trực quan Step 1 ➔ Step 5 với trạng thái màu sắc).
  - Video WebM và Screenshot được nhúng trực tiếp dạng Base64.
  - Hỗ trợ chuyển đổi song ngữ Anh - Việt (EN / VI).

---

## 📁 Cấu trúc Thư mục

```text
automation-ui/
├── run_tests.py         # Script điều phối thực thi kiểm thử và kích hoạt báo cáo
├── generate_report.py   # Entrypoint tạo báo cáo HTML (gọi package reporting/)
├── reporting/           # Package sinh báo cáo HTML tự chứa (Modular Architecture)
│   ├── core/            # Xử lý dữ liệu và điều phối sinh báo cáo
│   │   ├── parser.py    # Đọc report.json, tính toán timeline từng step
│   │   ├── media.py     # Xử lý Base64 cho Video Full HD và Screenshot
│   │   └── builder.py   # Lắp ráp layout HTML và điều phối tổng thể
│   ├── charts/          # Thuật toán vẽ biểu đồ Pure SVG (Zero CDN/JS)
│   │   ├── donut.py     # Biểu đồ tròn tỷ lệ Pass / Fail
│   │   ├── bar.py       # Biểu đồ cột thời lượng từng step
│   │   └── pipeline.py  # Sơ đồ luồng Interactive Step Pipeline (Step 1 ➔ Step 5)
│   └── assets/          # Giao diện và tương tác người dùng
│       ├── report.css   # Stylesheet CSS Dark theme, responsive 16:9, animation viền
│       └── report.js    # Client JavaScript: cuộn đến video rồi phát, song ngữ EN/VI
├── conftest.py          # Fixtures dùng chung, cấu hình Brave browser, tracker các bước (step)
├── pytest.ini           # Cấu hình Pytest, browser options, json report
├── requirements.txt     # Danh sách thư viện Python
├── AGENTS.md            # Nguyên tắc và kiến trúc cho AI agents
├── components/          # Các thành phần UI dùng chung (SearchBox, v.v.)
├── pages/               # Page Objects (BingHomePage, BingResultsPage, YouTubePage, v.v.)
├── tests/               # Các test case kiểm thử kịch bản nghiệp vụ (User Story 1, v.v.)
├── data/                # Dữ liệu kiểm thử JSON (search_data.json)
└── reports/             # Thư mục chứa báo cáo, screenshot và video kiểm thử
    ├── report.json             # Dữ liệu chi tiết kết quả test dạng JSON
    ├── execution_report.html   # Báo cáo dashboard HTML tổng hợp
    ├── execution_step5.png     # Screenshot bằng chứng hoàn thành kịch bản
    └── test-results/           # Video .webm ghi hình phiên kiểm thử
```
