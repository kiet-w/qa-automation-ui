# GLOSSARY: Architecture & Testing Domain Terminology

Thuật ngữ kiến trúc và kiểm thử chuẩn hóa của repository `automation-ui`.

## 1. Kiến trúc Dual-Gate & Giám sát Kép
* **Dual-Gate Architecture**: Mô hình kiểm thử giám sát kép, trong đó mọi tương tác UI đều qua `Interceptor` (bảo vệ hạ tầng) và mọi phán quyết trạng thái đều qua `Exceptor` (xác minh nghiệp vụ / snapshot), tuyệt đối không dùng `assert` tự do trong Page Objects.
* **Interceptor (`core/interceptor.py`)**: Tầng giám sát kỹ thuật bọc quanh các thao tác Playwright, tự động bắt và phân loại ngoại lệ thông qua `Error Catalog` (`core/catalog.py`) và ném ra `InfrastructureError`.
* **Exceptor (`core/exceptor.py`)**: Cổng phán quyết nghiệp vụ tập trung, tiếp nhận các snapshot trạng thái UI tĩnh và thực hiện các cổng kiểm tra (`expect_success`, `expect_rejection`, `expect_bug_if_rejected`, `expect_bug_if_accepted`, `expect_zero_js_errors`, `expect_accessible`).

## 2. Dữ liệu Snapshot (UI State Snapshots)
* **UI State Snapshot**: Cấu trúc dữ liệu dạng dictionary phản ánh trạng thái tĩnh của giao diện tại một thời điểm, bao gồm cờ thành công (`success_visible`), từ điển thông báo lỗi (`visible_errors`), và snapshot kỹ thuật.
* **Technical Snapshot**: Tập hợp dữ liệu trạng thái phi chức năng của trang tại một thời điểm (gồm danh sách `js_exceptions`, `console_errors`), tách biệt với trạng thái nghiệp vụ biểu mẫu.
* **A11y Snapshot**: Dữ liệu vi phạm khả năng tiếp cận thu thập qua engine `axe-core` theo các mức độ nghiêm trọng (`critical`, `serious`, `moderate`, `minor`), được chuyển đổi thành cấu trúc JSON độc lập.
* **Visual Diff Ratio**: Tỷ lệ phần trăm pixel khác biệt giữa ảnh chụp thực tế và ảnh chuẩn (baseline), hỗ trợ tính toán sai lệch và xuất chuỗi Base64 Data URI để nhúng vào báo cáo offline.

## 3. Kiến trúc Pytest & Bất biến (Invariants)
* **AST Invariant Guard**: Bộ kiểm thử đơn vị phân tích cây cú pháp trừu tượng (`ast`) của Python nhằm tự động ngăn chặn việc vi phạm các nguyên tắc kiến trúc (như cấm `assert` trong Page Objects, cấm `time.sleep()`, cấm debug `print()` và cấm External CDN).
* **Modular Pytest Plugins**: Mô hình phân tách `conftest.py` thành các plugin chuyên trách (`core/pytest_plugins/`) được nạp khai báo qua mảng `pytest_plugins`, đảm bảo nguyên tắc Single Responsibility.
* **Ticket Isolation**: Cơ chế tự động phát hiện mã User Story / Ticket từ tham số chạy của Pytest để cô lập toàn bộ video, ảnh chụp màn hình, và báo cáo JSON/HTML vào đúng thư mục con `reports/<ticket>/test-results/<run_id>/`.
