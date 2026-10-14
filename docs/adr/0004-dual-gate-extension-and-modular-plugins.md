# ADR-0004: Dual-Gate Architectural Modernization & Modular Pytest Architecture

## Trạng thái
Accepted

## Bối cảnh
Hệ thống kiểm thử tự động `automation-ui` dựa trên Playwright và Pytest cần mở rộng các năng lực giám sát kỹ thuật (Console/JS Error, Accessibility scanning, Visual Regression, Network Mocking) mà không phá vỡ 8 Bất biến Kiến trúc (Developer Invariants). Đồng thời, cần giải quyết 2 điểm nghẽn kiến trúc lớn:
1. File `conftest.py` (820 dòng) gộp quá nhiều trách nhiệm (trình duyệt, isolation, video, hooks).
2. Hub Node `CurriculaTrainerPage` (478 dòng, 175 liên kết) gánh toàn bộ 5 phân khu biểu mẫu.

## Quyết định Kỹ thuật
1. **Phân định ranh giới Dual-Gate cho Lỗi Kỹ thuật**:
   - Thu thập thụ động `pageerror` và `console.error` thông qua listeners trong `BasePage` (`get_technical_snapshot()`).
   - Đăng ký danh mục `JS_RUNTIME_ERROR` trong `core/catalog.py`.
   - `Exceptor.expect_zero_js_errors(snapshot)` ném ra `InfrastructureError(category="JS_RUNTIME_ERROR")` để hook `pytest_runtest_makereport` phân loại đồng nhất vào nhóm lỗi hạ tầng kỹ thuật.
2. **Kiểm thử Accessibility (A11y)**:
   - Sử dụng `axe-core-python` với cơ chế **Lazy Import** an toàn trong `BasePage.get_a11y_snapshot()`.
   - Cổng phán quyết `Exceptor.expect_accessible(snapshot)` ném `BusinessAssertionError` khi có vi phạm tiêu chuẩn tiếp cận.
3. **Phân tách Modular Pytest Plugins (`conftest.py`)**:
   - Chuyển `conftest.py` thành 3 module độc lập đặt trong `core/pytest_plugins/`:
     - `browser_engine.py`: Quản lý cấu hình 6 trình duyệt, stealth flags, và auto-detection Brave.
     - `ticket_isolation.py`: Cô lập `run_id`, thư mục artifact theo ticket, và điều phối ExtentReports.
     - `step_and_video_hook.py`: Quản lý `StepTracker` context manager và hook phân loại lỗi.
   - File `conftest.py` tại root rút gọn chỉ còn khai báo `pytest_plugins`.
4. **AST Architecture Invariant Guard**:
   - Thêm `tests/unit/test_architecture_invariants.py` dùng `ast` chuẩn để kiểm soát tự động các Invariants trong CI/CD, tự động loại trừ các khối CLI `if __name__ == '__main__':` để tránh false positive.
5. **Component Composition & Facade Pattern cho `CurriculaTrainerPage` (Giai đoạn P2)**:
   - Tách 4 phân khu thành các Section Component trong `components/curricula/`.
   - Giữ `CurriculaTrainerPage` làm Facade duy trì 100% chữ ký hàm hiện có.

## Hệ quả & Rủi ro
- **Tích cực**:
  - `conftest.py` giảm từ 820 dòng xuống còn 12 dòng.
  - Bộ kiểm thử unit tests tăng từ 26 lên 36 tests và chạy 100% PASS.
  - Bảo toàn 100% tính tương thích ngược với 68 test case hiện hành của US04.
- **Lưu ý triển khai**:
  - Đã thêm `Pillow>=10.0.0` và `axe-core-python>=0.1.0` vào `requirements.txt`.
