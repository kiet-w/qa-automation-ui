# ADR-0005: 19-Column Test Case Matrix Ingestion & AI Generation Specification

## Trạng thái
Accepted (Confirmed via /grill-me Alignment)

## Bối cảnh
Người dùng định nghĩa một cấu trúc Test Case chuẩn mực gồm 19 cột từ Google Sheets (Template QA Enterprise) làm đầu vào để giao cho AI coding (Cursor, Claude, Copilot, Antigravity) tự động sinh mã kiểm thử trên framework `automation-ui`.
Để tránh hiện tượng AI ảo giác locator, gãy framework, vi phạm các Invariants hoặc làm mất tính truy vết (traceability), cần thiết lập quy chuẩn kỹ thuật ánh xạ 1:1 từ 19 trường này sang code Python Pytest.

## Cấu trúc 19 Cột & Quy Tắc Ánh Xạ Chuẩn Hóa

| # | Cột Đầu Vào | Kiểu Dữ Liệu & Ví Dụ | Quy Tắc Ánh Xạ Kỹ Thuật Vào Code Python |
|---|---|---|---|
| 1 | **ID** | `TC-001` | Tiền tố hàm test: `def test_tc_001_<slug>(self):` & gắn `json_metadata["tc_id"] = "TC-001"`. |
| 2 | **Scenario ID** | `TS-001` | Tên file test: `tests/<traceability>/test_ts01_<suite_slug>.py`. |
| 3 | **Title** | `Verify user can log in with valid credentials` | Hậu tố hàm test & tiêu đề chính trong docstring mô tả. |
| 4 | **Test Suite** | `Login, User Management` | Phân nhóm file test (mỗi Test Suite = 1 file test độc lập). |
| 5 | **Page** | `Login Page` | Page Object trong `pages/`. AI phải tạo/bổ sung Page Object kế thừa `BasePage` trước khi viết test. |
| 6 | **Severity** | `P0 (highest)`, `P1`, `P2` | Pytest Marker: `@pytest.mark.p0`, `@pytest.mark.p1`. |
| 7 | **Priority** | `High`, `Medium`, `Low` | Pytest Marker: `@pytest.mark.priority_high`, ghi vào docstring & `json_metadata["priority"]`. |
| 8 | **Execution Status** | `Passed`, `Failed` | Quyết định có gắn `@pytest.mark.xfail` hay không (nếu Failed kèm Defect ID). |
| 9 | **Test Type** | `Functional`, `UI`, `Regression` | Pytest Marker: `@pytest.mark.functional`, `@pytest.mark.regression`, `@pytest.mark.ui`. |
| 10 | **Environment** | `DEV Chrome 129 Build 1.0.3` | Ghi nhận trong docstring & gán vào `json_metadata["target_env"]`. |
| 11 | **Preconditions** | `User account exists and is active` | Ghi nhận trong docstring; khởi tạo trạng thái trong `Step 0: Setup / Preconditions`. |
| 12 | **Test Data** | `Email: user01@test.com; Password: ...` | Trích xuất vào `data/<traceability>_data.json`; test chỉ gọi `copy.deepcopy(...)` tuân thủ Invariant 2. |
| 13 | **Test Steps** | `1. Open... 2. Enter... 3. Click...` | Ánh xạ 1:1 mỗi bước thành `with self.step("Step X: ..."):` kèm `self.step.set_actual(...)`. |
| 14 | **Expected Result** | `User redirected to Dashboard...` | Logic phán quyết kiểm thử ở bước cuối qua `Exceptor` hoặc `assert` chuẩn. |
| 15 | **Actual Result** | `As expected` / `Error 500 shown` | Đưa vào tham số lý do `reason` của `@pytest.mark.xfail` nếu test có bug. |
| 16 | **Assumption Ref** | Giả định nghiệp vụ khi spec chưa rõ | Ghi nhận vào docstring & lưu vào `json_metadata["assumptions"]`. |
| 17 | **Defect ID** | `BUG-012` | Gắn `@pytest.mark.xfail(strict=True, reason="<Defect_ID>: <Actual_Result>")` & `json_metadata["defect_id"]`. |
| 18 | **Traceability** | `US-05`, `BR-03` | Thư mục ticket `tests/<traceability>/`, `data/<traceability>_data.json` & `json_metadata["story"]`. |
| 19 | **Note** | Ghi chú thêm | Ghi nhận trong docstring của hàm test. |

## Mẫu Code Chuẩn Mực Sau Ánh Xạ (Canonical Implementation)

```python
import copy
import pytest
from core.exceptor import Exceptor
from tests.base_test import BaseTest


@pytest.mark.p0
@pytest.mark.priority_high
@pytest.mark.functional
@pytest.mark.ui
@pytest.mark.xfail(strict=True, reason="BUG-012: Error 500 is shown instead of Dashboard redirect")
def test_tc_001_verify_user_can_login_with_valid_credentials(self, trainer_data):
    """
    TC-001 — Verify user can log in with valid credentials
    Scenario ID: TS-001 | Test Suite: Login
    Page: Login Page | Test Type: Functional / UI
    Severity: P0 | Priority: High | Traceability: US-05, BR-03
    Environment: DEV Chrome 129 Build 1.0.3
    Preconditions: User account exists and is active.
    Test Data: trainer_data["login_valid_credentials"]
    Expected Result: User is redirected to Dashboard; welcome message is shown.
    Actual Result: Error 500 is shown (Tracked under BUG-012).
    Assumption Ref: Assuming default language is English.
    Note: Release blocker defect.
    """
    data = copy.deepcopy(trainer_data["login_valid_credentials"])

    with self.step("Step 1: Open the login page"):
        login_page = self.get_page(LoginPage)
        login_page.open()
        self.step.set_actual("Login page loaded successfully.")

    with self.step("Step 2: Enter valid email and password"):
        login_page.enter_credentials(email=data["email"], password=data["password"])
        self.step.set_actual("Credentials entered into input fields.")

    with self.step("Step 3: Click [Login]"):
        login_page.click_login()
        self.step.set_actual("Login button clicked; waiting for redirect.")

    with self.step("Step 4: Verify user redirected to Dashboard and welcome message shown"):
        assert "/dashboard" in self.page.url, "User must be redirected to /dashboard"
        assert login_page.is_welcome_message_visible(), "Welcome message must be visible"
        self.step.set_actual("Dashboard verified with welcome message.")
```

## Hệ Quả & Lợi Ích
1. **Zero Hallucination**: AI có một ma trận ánh xạ cơ học, không tự ý sáng tạo hay làm lệch chuẩn.
2. **Full Traceability**: Báo cáo ExtentReports tự động hiển thị đầy đủ TC-ID, Story, Priority, Defect Badge và đồng bộ video timeline từng bước.
3. **Pipeline Protection**: Sử dụng `@pytest.mark.xfail(strict=True)` giúp CI/CD không bị chặn bởi các bug đã biết, nhưng vẫn cảnh báo khi bug được lập trình viên sửa xong (XPASS).
