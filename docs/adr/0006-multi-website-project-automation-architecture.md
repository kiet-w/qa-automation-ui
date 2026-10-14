# ADR-0006: Multi-Website & Multi-Project Automation Architecture

## Trạng thái
Accepted (Confirmed via /grill-me Alignment)

## Bối cảnh
Người dùng muốn xác nhận khả năng mở rộng của framework `automation-ui` để thực hiện kiểm thử tự động cho nhiều dự án website khác nhau (khác cả về domain, backend cơ sở dữ liệu, môi trường và cơ chế xác thực) ngay bên trong thư mục `tests/`.

## Các Quyết Định Kiến Trúc Đã Thống Nhất

### 1. Phân Tách Thư Mục Theo Dự Án (Multi-Project Directory Isolation)
Mỗi website hoặc dự án mới được tổ chức thành một phân khu khép kín:
- **Test Suites**: `tests/<project_name>/` (chứa các file `test_ts01_*.py`).
- **Page Objects**: `pages/<project_name>/` (chứa các Page Object kế thừa `BasePage`).
- **Test Data**: `data/<project_name>/` (chứa file JSON fixture và file upload mẫu).
- **Reports & Artifacts**: `reports/<project_name>/` (ExtentReports HTML, video 1080p, screenshots).
- **Thực thi**: Điều phối độc lập qua lệnh `python3 run_tests.py --ticket <project_name>`.

### 2. Quản Lý Base URL & Đa Môi Trường
- Tận dụng plugin `pytest-base-url` hoặc biến môi trường `BASE_URL`.
- Phương thức `BasePage.navigate(url)` tự động ghép nối nếu truyền đường dẫn tương đối (ví dụ `self.navigate("/checkout")` -> `https://staging.domain.com/checkout`).

### 3. Tối Ưu Phiên Đăng Nhập Bằng `storage_state`
- 1 test case duy nhất thực hiện đăng nhập qua UI và lưu trạng thái vào `reports/<project_name>/auth.json`.
- Các test case nghiệp vụ còn lại nạp sẵn context với `storage_state="reports/<project_name>/auth.json"` để vào thẳng trang chức năng, tiết kiệm 80% thời gian thực thi của cả bộ test suite.

### 4. Vượt Rào Cản Anti-Bot, Captcha & 2FA
- Đề xuất Dev team cung cấp mock header hoặc fixed test bypass key trên môi trường QA/Staging cho Captcha/OTP.
- Tận dụng `playwright-stealth` và kênh trình duyệt Brave có sẵn trong `core/pytest_plugins/browser_engine.py` để vượt Cloudflare/Akamai bot detection.

### 5. Dữ Liệu Động & Teardown Dọn Dẹp
- Sinh chuỗi ngẫu nhiên bằng `uuid.uuid4().hex[:6]` cho các trường unique (Email, SĐT, Mã đơn hàng).
- Sử dụng pytest fixture với `yield` để gọi API dọn dẹp (cleanup) dữ liệu rác sau khi test hoàn tất.
