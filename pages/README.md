# 🏛️ Tiêu Chuẩn Phân Bổ Code POM, Locators, Function Flows & Error Handling (Zero-Token-Waste Architecture)

> [!IMPORTANT]
> **Mục tiêu cốt lõi**: Phân bổ cấu trúc mã nguồn tự động hóa theo mô hình 3 tầng (3-Tier Clean Architecture) để bất kỳ Kỹ sư Kiểm thử hay AI Agent nào khi tham gia coding đều có thể:
> 1. **Lấy đúng và đủ thông tin (Zero Bloat)**: Chỉ nạp đúng file locator hoặc step component cần dùng (< 100-150 dòng), không bao giờ phải đọc cả file khổng lồ hay toàn bộ DOM.
> 2. **Tiết kiệm token tối đa (Token Optimization)**: Sử dụng metadata RAG và cấu trúc file module hóa để cắt giảm tới 80-90% token ngữ cảnh.
> 3. **Bắt lỗi chính xác 100%**: Chuẩn hóa hợp đồng `get_state_snapshot()` kết nối trực tiếp với `Exceptor`, bắt lỗi chi tiết từng trường (`aria-invalid`) và banner máy chủ mà không gây flake.

---

## 🗺️ 1. Bản Đồ Phân Bổ Thư Mục Chuẩn (Per-Module Distribution)

Mỗi phân hệ (feature/ticket) trong `pages/` được tổ chức độc lập theo quy tắc phân rã:

```
2_Code_Automation/
├── components/                       # Shared UI Pieces & Reusable Automation Engines
│   ├── form_helper.py                # Generic Form interactions & field error extractor (<150L)
│   ├── transaction_helper.py         # Data table, row disclosure accordion & pagination (<150L)
│   └── search_box.py                 # Shared searchbox component
│
├── core/
│   ├── error_diagnostics.py          # Detailed Error Inspection Engine (ARIA, alerts, toasts, console)
│   ├── exceptor.py                   # Central Business Assertion Gatekeeper (Exceptor)
│   └── exceptions.py                 # Custom BusinessAssertionError & InfrastructureError
│
└── pages/<module>/                   # Ví dụ: fs08, fs09, fs03, f10
    ├── locators.py                   # DUY NHẤT: Bảng tập trung mọi CSS/XPath selectors (<100L)
    ├── components/                   # Các bước riêng lẻ của Wizard hoặc Modal con (<150L/file)
    │   ├── charges_step.py           # Bước 1: Chọn khoản phí
    │   ├── payment_methods_step.py   # Bước 2: Chọn phương thức & Split
    │   └── review_step.py            # Bước 3: Xem lại & Authorize
    └── <module>_page.py              # Page Orchestrator điều hướng luồng chính (<200L)
```

---

## 📏 2. Định Mức Dung Lượng & Phân Định Trách Nhiệm (Invariant 9 Enforcements)

| Thành phần | Đường dẫn mẫu | Giới hạn dòng | Trách nhiệm | Những điều NGHIÊM CẤM |
| :--- | :--- | :---: | :--- | :--- |
| **Locators** | `pages/<module>/locators.py` | `< 100 dòng` | Khai báo hằng số selector viết hoa, gom nhóm theo Card/Section. | ❌ Không chứa logic click/fill.<br>❌ Không selector động khó hiểu. |
| **Atomic Step Component** | `pages/<module>/components/*.py` | `< 150 dòng` | Thực hiện hành động trong 1 modal/bước, kiểm tra trạng thái nút/trường. | ❌ Không chứa `assert`.<br>❌ Không điều hướng URL trang khác. |
| **Page Orchestrator** | `pages/<module>/<page>_page.py` | `< 200 dòng` | Mở trang, điều phối chuyển bước (Step 1 -> 2 -> 3), xuất snapshot tổng thể. | ❌ Không nhồi nhét locators trực tiếp.<br>❌ Không chứa validation logic. |
| **Form Helper** | `components/form_helper.py` | `< 150 dòng` | Điền form tự động, quét `aria-invalid`, bóc tách `FormErrorSummary`. | ❌ Không hardcode tên trường cụ thể. |
| **Transaction Helper**| `components/transaction_helper.py` | `< 150 dòng` | Đọc dữ liệu bảng, toggle mở rộng dòng `InvoiceDisclosure`, phân trang. | ❌ Không xử lý nghiệp vụ thanh toán. |

---

## 🛠️ 3. Mẫu Chuẩn Cho AI / Developer Khi Coding

### 3.1 Mẫu 1: Xử Lý Biểu Mẫu (Forms) Tối Ưu
Khi tạo mới hoặc sửa Page Object cho Form, kế thừa `BasePage` và gắn `FormHelper`:

```python
# pages/fs03/school_create_page.py
from pages.base_page import BasePage
from pages.fs03.locators import SchoolCreateLocators as Loc
from components.form_helper import FormHelper

class SchoolCreatePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.form = FormHelper(page, container=Loc.FORM_CONTAINER)

    def submit_school(self, data: dict):
        self.form.fill_fields(data)
        self.form.click_submit(Loc.SUBMIT_BTN)

    def get_state_snapshot(self) -> dict:
        """Hợp đồng snapshot chuẩn cho Exceptor - Zero Token Bloat"""
        return self.form.get_form_snapshot(
            success_selector=Loc.SUCCESS_TOAST,
            submit_selector=Loc.SUBMIT_BTN
        )
```

### 3.2 Mẫu 2: Xử Lý Bảng Giao Dịch & Accordion (Transactions)
Khi làm việc với bảng dữ liệu hoặc giao dịch có mở rộng chi tiết:

```python
# pages/fs08/transactions_page.py
from pages.base_page import BasePage
from pages.fs08.locators import TransactionsLocators as Loc
from components.transaction_helper import TransactionHelper

class TransactionsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.grid = TransactionHelper(page, table_selector=Loc.TABLE)

    def view_invoice_breakdown(self, invoice_number: str):
        # Mở dòng accordion chi tiết
        self.grid.toggle_disclosure(invoice_number, open=True)
        # Bóc tách bảng phân bổ nguồn tiền con
        return self.grid.get_rows_data()

    def get_state_snapshot(self) -> dict:
        alert = self.grid.get_alert_state()
        return {
            "success_visible": alert is None,
            "visible_errors": {alert["heading"]: alert["message"]} if alert else {},
            "row_count": len(self.grid.get_rows_data())
        }
```

### 3.3 Mẫu 3: Bắt Lỗi Trong Test Case (`tests/`) Không Thừa Thãi
Trong kịch bản kiểm thử, QA chỉ cần assert thông qua `Exceptor`:

```python
# tests/fs03/test_school_creation.py
from core.exceptor import Exceptor

def test_tc_school_create_rejected_missing_name(school_create_page):
    # 1. Hành động điền form thiếu trường bắt buộc
    school_create_page.submit_school({"moeSchoolCode": "SCH9999"})
    
    # 2. Lấy snapshot trạng thái
    snapshot = school_create_page.get_state_snapshot()
    
    # 3. Assert chuẩn xác theo mã lỗi / trường mà không cần chụp toàn bộ DOM
    Exceptor.expect_rejection(
        snapshot=snapshot,
        field="name",
        message_contains="School name is required",
        context="TC-SCH-002: Verify mandatory school name"
    )
```

---

## ⚡ 4. Quy Trình Lấy Thông Tin Nhanh Bằng RAG Cho AI Agent (Zero-Token Retrieval)

Khi AI Agent hoặc Developer cần lấy selector hay quy tắc flow, **TUYỆT ĐỐI KHÔNG** đọc cả file Markdown hàng ngàn dòng. Hãy thực hiện 2 bước truy vấn siêu gọn:

1. **Bước 1: Tra cứu đúng selector / flow cần qua RAG**:
   ```bash
   python3 2_Code_Automation/tools/lean_context/retrieve.py "InvoiceDisclosure" --max-chars 1000
   ```
   *Kết quả trả về*: Chỉ đúng 10 dòng chứa locator và mô tả của thành phần đó. Tiết kiệm 95% token context.

2. **Bước 2: Đọc file `locators.py` của module đó**:
   ```python
   # File pages/<module>/locators.py chỉ vỏn vẹn <100 dòng, đọc trực tiếp 1 lần là đủ toàn bộ selectors.
   from pages.fs08.locators import TransactionsLocators
   ```
