# Enterprise QA Automation UI Framework

Framework kiểm thử tự động giao diện (UI Automation) chuẩn doanh nghiệp xây dựng trên nền tảng **Python**, **Playwright** và **Pytest**. Áp dụng mô hình **Page Object Model (POM)** kết hợp kiến trúc thành phần UI tái sử dụng (**Component-based**), kiến trúc kiểm thử phân lập theo Ticket (**Ticket-Isolated Architecture**), cùng hệ sinh thái độc lập gồm **Requirements Traceability**, bộ đôi giám sát lỗi **Exceptor & Interceptor**, và công cụ sinh báo cáo **ExtentReports HTML 100% Offline**.

---

## 📑 Mục lục (Table of Contents)

1. [Điểm nổi bật của Framework](#-điểm-nổi-bật-của-framework)
2. [Kiến trúc & Các Module Cốt lõi](#-kiến-trúc--các-module-cốt-lõi)
   - [Module Exceptor — Cửa khẩu phán quyết nghiệp vụ](#1-module-exceptor--business-assertion-gate)
   - [Module Interceptor — Giám sát lỗi kỹ thuật hạ tầng](#2-module-interceptor--infrastructure-supervisor)
   - [Error Catalog — Danh mục phân loại lỗi & gợi ý debug](#3-error-catalog--danh-mục-phân-loại-lỗi)
   - [Requirements-First & Ma trận đối chiếu (Traceability Matrix)](#4-requirements-first--ma-trận-đối-chiếu-traceability-matrix)
   - [Báo cáo ExtentReports HTML tự chứa (100% Offline)](#5-báo-cáo-extentreports-html-100-offline)
3. [Cấu trúc Thư mục Dự án](#-cấu-trúc-thư-mục-dự-án)
4. [Hướng dẫn Cài đặt & Khởi tạo](#-hướng-dẫn-cài-đặt--khởi-tạo)
5. [Hướng dẫn Thực thi Kiểm thử](#-hướng-dẫn-thực-thi-kiểm-thử)
   - [Chạy theo User Story / Ticket cụ thể](#1-chạy-theo-user-story--ticket-cụ-thể)
   - [Chạy song song đa tiến trình (pytest-xdist)](#2-chạy-song-song-đa-tiến-trình-parallel-workers)
   - [Chạy bộ Unit Test nội bộ của Framework](#3-chạy-bộ-unit-test-của-framework)
   - [Chạy ở chế độ có giao diện (Headed Mode)](#4-chạy-ở-chế-độ-có-giao-diện-headed-mode)
   - [Tái sinh báo cáo HTML không cần chạy lại test](#5-tái-sinh-báo-cáo-html-không-cần-chạy-lại-test)
6. [Quy chuẩn Phát triển Test Case Mới](#-quy-chuẩn-phát-triển-test-case-mới)

---

## 🌟 Điểm nổi bật của Framework

- **Tách bạch lỗi Nghiệp vụ vs Lỗi Hạ tầng**: Không còn gộp chung mọi lỗi thành "Failed". Phân biệt rành mạch giữa **Lỗi sản phẩm thật (Bug)** và **Lỗi môi trường/mạng/timeout (Infrastructure Error)**.
- **Triệt tiêu lỗi Đảo ngược Logic (Reversed Assertion)**: Thay thế hoàn toàn các lệnh `assert x == True/False` thô bằng 4 phương thức khai báo kỳ vọng theo đúng ý định kiểm thử (`expect_success`, `expect_rejection`, `expect_bug_if_rejected`, `expect_bug_if_accepted`).
- **Nguồn tham chiếu cố định (Source of Truth)**: Mọi test case đều bắt nguồn từ tài liệu `AC.md` và bảng `traceability_matrix.md` trước khi code được viết.
- **Báo cáo HTML Tự Chứa 100% (Zero External CDN)**: Toàn bộ video WebM Full HD (1080p), ảnh chụp bằng chứng (Screenshots), các biểu đồ toán học Pure SVG (Donut, Bar, Pipeline, Diagram, Trend) và CSS/JS đều được nhúng trực tiếp (Base64 Data URI) vào một file HTML duy nhất. Không phụ thuộc Internet, Chart.js, Tailwind CDN hay Google Fonts.
- **Đồng bộ Tương tác 2 chiều (Diagram to Video Sync)**: Bấm vào từng bước trên sơ đồ quy trình tương tác sẽ tự động cuộn đến video, tua đến mốc thời gian chính xác và phát lại.
- **Hỗ trợ Song ngữ Thông minh (EN / VI)**: Chuyển đổi ngôn ngữ hiển thị báo cáo tức thì chỉ với một nút bấm.
- **Thực thi Song song Hiệu năng cao**: Tối ưu hóa cho `pytest-xdist` với cơ chế mapping video 1:1 độc lập, tự động chuyển chế độ Headless khi chạy đa luồng (`-n > 1`).

---

## 🏗 Kiến trúc & Các Module Cốt lõi

```text
       ┌────────────────────────────────────────────────────────┐
       │             User Story Requirements (AC.md)            │
       └───────────────────────────┬────────────────────────────┘
                                   │  1. Map Ý định kiểm thử
                                   ▼
       ┌────────────────────────────────────────────────────────┐
       │       Traceability Matrix (traceability_matrix.md)     │
       │   [Gán nhãn: expect_success / expect_rejection / ...]  │
       └───────────────────────────┬────────────────────────────┘
                                   │  2. Chỉ định phương thức
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           TEST CASE EXECUTION                           │
│                                                                         │
│   ┌───────────────────────────┐         ┌───────────────────────────┐   │
│   │    Playwright Actions     │         │     Page Object State     │   │
│   │  (click, fill, save, ...) │         │  (Snapshot: errors, box)  │   │
│   └─────────────┬─────────────┘         └─────────────┬─────────────┘   │
│                 │                                     │                 │
│                 ▼                                     ▼                 │
│   ┌───────────────────────────┐         ┌───────────────────────────┐   │
│   │        Interceptor        │         │         Exceptor          │   │
│   │ (Bắt lỗi kỹ thuật hạ tầng)│         │ (Phán quyết lỗi nghiệp vụ)│   │
│   └─────────────┬─────────────┘         └─────────────┬─────────────┘   │
└─────────────────┼─────────────────────────────────────┼─────────────────┘
                  │                                     │
                  ▼                                     ▼
     ┌────────────────────────┐            ┌────────────────────────┐
     │  InfrastructureError   │            │ BusinessAssertionError │
     │ [TIMEOUT, CRASH, NET]  │            │  [BUG / REJECTION OK]  │
     └────────────────────────┘            └────────────────────────┘
```

### 1. Module `Exceptor` — Business Assertion Gate
Tệp tin: `core/exceptor.py`

Là **cửa khẩu duy nhất** quyết định Pass/Fail về mặt nghiệp vụ. Exceptor hoạt động thuần túy trên `snapshot` trạng thái UI đã thu thập từ Page Object, hoàn toàn không gọi lại Playwright bên trong.

```python
from core import Exceptor

# 1. Happy Path: Kỳ vọng thao tác thành công
Exceptor.expect_success(snapshot, context="Lưu form hợp lệ")

# 2. Unhappy Path: Kỳ vọng bị từ chối đúng trường và đúng nội dung lỗi
Exceptor.expect_rejection(
    snapshot,
    field="primaryPhone",
    message_contains="Enter a valid contact number",
    context="Nhập số điện thoại sai độ dài",
)

# 3. Bug Hunting: Input hợp lệ thực tế nhưng hệ thống lại chặn -> Raise [BUG DETECTED]
Exceptor.expect_bug_if_rejected(
    snapshot,
    field="unitNumber",
    context="Nhập số căn hộ Singapore Alphanumeric #04-12A",
)

# 4. Bug Hunting: Input sai thực tế nhưng hệ thống lại cho qua -> Raise [BUG DETECTED]
Exceptor.expect_bug_if_accepted(
    snapshot,
    context="Nhập số điện thoại Singapore bắt đầu bằng đầu số 1",
)
```

Khi điều kiện kiểm tra không thỏa mãn, Exceptor ném ra ngoại lệ `BusinessAssertionError` (kế thừa từ `AssertionError`), giúp Pytest nhận diện là lỗi kiểm thử chuẩn mà không nhầm lẫn với lỗi code hệ thống.

---

### 2. Module `Interceptor` — Infrastructure Supervisor
Tệp tin: `core/interceptor.py`

Bọc quanh một thao tác Playwright cụ thể (`click`, `fill`, `save`, `navigate`...) một cách tường minh, nhằm bắt các lỗi kỹ thuật phát sinh ngoài ý muốn và ném ra ngoại lệ `InfrastructureError` (kế thừa `Exception`, KHÔNG kế thừa `AssertionError`).

```python
from core import Interceptor

# Bọc hành động Playwright cần giám sát
result = Interceptor.run(
    lambda: curricula_page.save(),
    action_name="save_curricula_form",
    context="Nhấn nút Save để hoàn tất tạo tài khoản",
)
```

**Đặc điểm:**
- Giữ nguyên thông tin và traceback của exception gốc thông qua thuộc tính `original_exception` và cơ chế `raise ... from exc`.
- Thông báo lỗi hiển thị có tiền tố nhận diện chuẩn dạng: `[INFRA ERROR:<CATEGORY>]`.

---

### 3. Error Catalog — Danh mục phân loại lỗi
Tệp tin: `core/catalog.py`

Registry tập trung tra cứu và phân loại lỗi kỹ thuật Playwright/Python thành các danh mục chuẩn:

| Danh mục (Category) | Điều kiện nhận diện (Pattern / Class) | Gợi ý khắc phục (Diagnostic Hint) |
|---|---|---|
| `TIMEOUT` | Class `TimeoutError` hoặc thông điệp chứa `Timeout \d+ms exceeded` | Phần tử không xuất hiện/sẵn sàng kịp thời gian chờ; kiểm tra lại selector hoặc tăng timeout. |
| `BROWSER_CRASH` | Thông điệp chứa `Target closed`, `Target page, context or browser has been closed` | Trình duyệt hoặc tab bị đóng đột ngột giữa lúc thao tác. |
| `STALE_ELEMENT` | Thông điệp chứa `Element is not attached to the DOM`, `stale element` | DOM đã thay đổi do trang re-render, locator cũ không còn hợp lệ. |
| `NETWORK` | Thông điệp chứa `net::ERR_`, `NS_ERROR_CONNECTION_REFUSED` | Lỗi kết nối mạng khi tải trang hoặc tài nguyên từ xa. |
| `UNKNOWN` | Các ngoại lệ không khớp quy tắc nào ở trên | Lỗi hạ tầng chưa được phân loại — cần bổ sung thêm vào catalog. |

> **Khả năng mở rộng:** Để thêm một rule phân loại lỗi mới, chỉ cần thêm 1 phần tử `ErrorRule(...)` vào danh sách `ERROR_RULES` trong `core/catalog.py`.

---

### 4. Requirements-First & Ma trận đối chiếu (Traceability Matrix)
Thư mục: `tests/<ticket_folder>/requirements/`

Trước khi viết bất kỳ dòng code kiểm thử nào, mỗi User Story đều có 2 file tài liệu làm **nguồn tham chiếu cố định (Source of Truth)**:
1. `<ticket>_AC.md`: Liệt kê nguyên văn từng tiêu chí chấp nhận (**AC-01, AC-02, ...**) của nghiệp vụ.
2. `<ticket>_traceability_matrix.md`: Bảng đối chiếu từng AC với hành vi thực tế của hệ thống trên form, đánh giá `✅ Khớp` hoặc `❌ Không khớp`, và **chỉ định chính xác hàm Exceptor cần gọi**.

---

### 5. Báo cáo ExtentReports HTML (100% Offline)
Thư mục: `reporting/`

Công cụ sinh báo cáo HTML độc lập, được đóng gói hoàn toàn:
- **Tự chứa toàn bộ dữ liệu**: Video WebM Full HD và ảnh screenshot được mã hóa Base64 Data URI trực tiếp vào file HTML.
- **Biểu đồ Pure SVG**: Thuật toán vẽ SVG nội tại cho Donut Chart (Pass rate), Bar Chart (Thời lượng từng step), Pipeline (Sơ đồ quy trình), Architecture Diagram và Multi-Run Trend Chart.
- **Phân lập theo Ticket**: Kết quả và bằng chứng của từng ticket được cô lập hoàn toàn tại `reports/<ticket>/`, không ghi đè lẫn nhau.

---

## 📁 Cấu trúc Thư mục Dự án

```text
automation-ui/
├── AGENTS.md                                # Quy chuẩn kiến trúc & hướng dẫn dành cho AI Agents
├── README.md                                # Tài liệu hướng dẫn toàn diện của framework
├── requirements.txt                         # Danh sách thư viện Python
├── pytest.ini                               # Cấu hình Pytest, browser options, json report
├── conftest.py                              # Fixtures dùng chung, ticket router, video/screenshot hooks
├── run_tests.py                             # Script điều phối thực thi kiểm thử 2 pha
├── generate_report.py                       # CLI entrypoint sinh báo cáo HTML độc lập
├── example_usage.py                         # File ví dụ mẫu cách dùng Exceptor & Interceptor
├── curricula_trainer_account.html           # Ứng dụng web mẫu Curricula Trainer Account
│
├── core/                                    # Gói module cốt lõi phân lập lỗi
│   ├── __init__.py                          # Export Exceptor, Interceptor, classify, exceptions
│   ├── exceptions.py                        # BusinessAssertionError, InfrastructureError
│   ├── catalog.py                           # Error Catalog & hàm classify()
│   ├── exceptor.py                          # Exceptor phán quyết nghiệp vụ
│   └── interceptor.py                       # Interceptor giám sát hạ tầng
│
├── components/                              # Các UI widget tái sử dụng giữa nhiều trang
│   ├── __init__.py
│   └── search_box.py                        # Search bar component (gõ phím người dùng tự nhiên)
│
├── pages/                                   # Page Objects (Tương tác giao diện & định vị element)
│   ├── __init__.py
│   ├── base_page.py                         # BasePage cung cấp click, fill, wait, screenshot, highlight
│   ├── bing_home_page.py                    # Trang chủ Bing
│   ├── bing_results_page.py                 # Trang kết quả tìm kiếm Bing
│   ├── youtube_page.py                      # Trang YouTube target
│   └── curricula_trainer_page.py            # Trang tạo tài khoản Curricula Trainer
│
├── data/                                    # Dữ liệu kiểm thử JSON
│   ├── search_data.json                     # Từ khóa tìm kiếm cho US01
│   ├── parallel_20_data.json                # Bộ dữ liệu 20 test song song US02
│   ├── curricula_trainer_data.json          # Bộ hồ sơ kiểm thử US03 (Singapore, Non-SG, Boundary)
│   └── fixtures/                            # Tệp đính kèm kiểm thử (PDF, PNG, file exe độc hại)
│
├── tests/                                   # Các test suite phân lập theo User Story / Ticket
│   ├── __init__.py
│   ├── base_test.py                         # BaseTest: setup autouse, report helpers, step tracking
│   ├── unit/                                # Unit test nội bộ kiểm thử chính framework
│   │   ├── __init__.py
│   │   ├── test_exceptor.py                 # 12 bài test kiểm tra logic của Exceptor
│   │   ├── test_interceptor.py              # 7 bài test kiểm tra cơ chế bắt lỗi của Interceptor
│   │   └── test_catalog.py                  # 7 bài test kiểm tra Error Catalog và tính mở rộng
│   ├── us01_bing_search/                    # Kịch bản kiểm thử User Story 1
│   │   ├── __init__.py
│   │   ├── test_bing_search.py
│   │   └── test_bing_search_parallel.py
│   ├── us02_parallel_20/                    # Kịch bản kiểm thử 20 test song song
│   │   ├── __init__.py
│   │   └── test_parallel_20.py
│   └── us03_curricula_trainer/              # Kịch bản kiểm thử Curricula Trainer Account
│       ├── __init__.py
│       ├── requirements/                    # Nguồn tham chiếu cố định (Source of Truth)
│       │   ├── us03_curricula_trainer_AC.md
│       │   └── us03_curricula_trainer_traceability_matrix.md
│       └── test_curricula_trainer.py
│
├── reporting/                               # HTML Report Engine (100% Offline)
│   ├── __init__.py
│   ├── core/                                # Xử lý dữ liệu JSON, media encoder, document builder
│   ├── charts/                              # Pure SVG Renderers: donut, bar, pipeline, diagram, trend
│   └── assets/                              # report.css, report.js (hỗ trợ lightbox, song ngữ EN/VI)
│
└── reports/                                 # Artifacts sinh ra sau khi chạy (Được cô lập theo ticket)
    ├── .gitkeep
    ├── us01_bing_search/                    # Báo cáo, log, video, ảnh của US01
    ├── us03_curricula_trainer/              # Báo cáo, log, video, ảnh của US03
    └── unit/                                # Báo cáo kết quả của bộ unit tests
```

---

## 🚀 Hướng dẫn Cài đặt & Khởi tạo

1. **Khởi tạo môi trường ảo Python (Python 3.10+)**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate       # Trên Linux / macOS
   # hoặc: .venv\Scripts\activate   # Trên Windows
   ```

2. **Cài đặt các thư viện phụ thuộc**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Cài đặt Browser Driver của Playwright**:
   ```bash
   playwright install chromium
   ```

---

## 🎯 Hướng dẫn Thực thi Kiểm thử

Script điều phối `run_tests.py` quản lý toàn bộ quy trình:
- **Pha 1**: Chạy Pytest, stream log real-time và tạo file `report.json` phân lập theo ticket.
- **Pha 2**: Tự động kích hoạt `generate_report.py` để đóng gói HTML report tự chứa kèm video và ảnh Base64.
- **Pha 3**: In bảng tổng kết ANSI Dashboard trực tiếp trên terminal.

### 1. Chạy theo User Story / Ticket cụ thể
Để chạy một ticket cụ thể và xuất báo cáo riêng biệt vào `reports/<ticket>/`:

```bash
# Chạy User Story 1 (Bing Search)
python run_tests.py tests/us01_bing_search/

# Chạy User Story 3 (Curricula Trainer Account)
python run_tests.py tests/us03_curricula_trainer/
```

### 2. Chạy song song đa tiến trình (Parallel Workers)
Tận dụng sức mạnh đa nhân CPU với `pytest-xdist`:

```bash
# Chạy 4 workers đồng thời
python run_tests.py tests/us02_parallel_20/ -n 4

# Chạy toàn bộ test suite với tối đa số worker tương ứng số core CPU
python run_tests.py -n auto
```

### 3. Chạy bộ Unit Test của Framework
Kiểm tra tính toàn vẹn của các module `Exceptor`, `Interceptor` và `Catalog`:

```bash
python run_tests.py tests/unit/
# Hoặc chạy trực tiếp qua pytest:
pytest tests/unit/
```

### 4. Chạy ở chế độ có giao diện (Headed Mode)
Hữu ích khi cần quan sát trực tiếp trình duyệt trong lúc debug:

```bash
python run_tests.py tests/us01_bing_search/ --headed
```

### 5. Tái sinh báo cáo HTML không cần chạy lại test
Khi đã có file dữ liệu `report.json` trước đó, bạn có thể tái tạo lại file HTML bất cứ lúc nào:

```bash
# Sinh báo cáo cho một ticket cụ thể:
python generate_report.py reports/us03_curricula_trainer/report.json

# Hoặc sinh báo cáo cho thư mục reports mặc định:
python generate_report.py
```

---

## 📝 Quy chuẩn Phát triển Test Case Mới

Khi xây dựng một User Story kiểm thử mới (ví dụ: `us04_payment_gateway`), hãy thực hiện theo đúng 4 bước chuẩn sau:

### Bước 1: Tạo thư mục Requirements
Tạo thư mục `tests/us04_payment_gateway/requirements/` gồm 2 file:
- `us04_payment_gateway_AC.md`: Liệt kê các tiêu chí chấp nhận gốc.
- `us04_payment_gateway_traceability_matrix.md`: Lập bảng đối chiếu giữa AC và hành vi thực tế của hệ thống, gán nhãn Exceptor tương ứng.

### Bước 2: Tạo Page Object (kế thừa `BasePage`)
Tạo `pages/payment_page.py`:
- Kế thừa từ `BasePage`.
- Đóng gói các selector và hàm thao tác (`open()`, `fill_payment_info()`, `submit()`).
- Cung cấp hàm `get_state_snapshot()` trả về dictionary trạng thái trang dạng:
  ```python
  {
      "success_visible": bool,
      "visible_errors": {"field_name": "error_message_text"}
  }
  ```
- **Tuyệt đối KHÔNG viết lệnh `assert` bên trong Page Object.**

### Bước 3: Viết Test Case (kế thừa `BaseTest`)
Tạo `tests/us04_payment_gateway/test_payment.py`:
- Bọc mọi hành động thao tác Playwright bằng `Interceptor.run()`:
  ```python
  Interceptor.run(
      lambda: self.payment_page.submit(),
      action_name="submit_payment",
      context="Thực hiện thanh toán đơn hàng",
  )
  ```
- Lấy `snapshot = self.payment_page.get_state_snapshot()`.
- Gọi hàm của `Exceptor` theo đúng nhãn đã định trong Ma trận đối chiếu:
  ```python
  # Nếu là Happy Path:
  Exceptor.expect_success(snapshot, context="Thanh toán thành công bằng thẻ hợp lệ")

  # Nếu là Unhappy Path:
  Exceptor.expect_rejection(snapshot, field="cardNumber", message_contains="Invalid card number")
  ```

### Bước 4: Thực thi và Xem Báo cáo
```bash
python run_tests.py tests/us04_payment_gateway/
```
Báo cáo HTML tự chứa và video ghi hình sẽ tự động hiển thị tại `reports/us04_payment_gateway/execution_report.html`.
