# Nhóm 2 — Code Automation

Thư mục điều hướng cho framework runtime, Page Objects, test data, test suites và công cụ hỗ trợ.

| Shortcut | Nội dung | Quy tắc |
| :--- | :--- | :--- |
| `core/` | Pytest plugins, browser lifecycle, hooks và error classification | Framework runtime. |
| `pages/` | Page Objects theo module | Không chứa assertion. |
| `components/` | Shared UI widgets | Chỉ tương tác UI và trả state. |
| `data/` | JSON data, fixtures và mock assets | Không hardcode dữ liệu trong test. |
| `tests/` | Atomic/integration automation suites | Đặt dưới `tests/<module>/<ticket>/`. |
| `tools/` | Recon, environment, generator và spec sync | Không chứa test suite nghiệp vụ. |
| `conftest.py` | Pytest entrypoint | Delegates tới `core/pytest_plugins/`. |
| `pytest.ini` | Cấu hình chạy mặc định | `-n 3`, video off và report paths. |
| `requirements.txt` | Python dependencies | Dùng để dựng `.venv`. |
| `run_tests.py` | Test/report orchestrator | Người dùng tự thực thi. |
| `md_runner.py` | Markdown-first runner | Người dùng tự thực thi. |

Các mục trong thư mục này là shortcut tới vị trí chuẩn ở repository root để giữ nguyên Python imports và pytest discovery.
