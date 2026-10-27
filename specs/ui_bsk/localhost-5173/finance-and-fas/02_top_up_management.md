# 📋 BSK Locator & Functional Flow Spec: Top-Up Management (Chiến Dịch Nạp Tiền Edusave)

| Trường Thông Tin | Chi Tiết |
| :--- | :--- |
| **Portal / Cổng Dịch Vụ** | Admin Portal (`localhost:5173`) |
| **Các Đường Dẫn Thực Tế (URLs)** | • `/top-up` (Danh sách tabs: Individual, Bulk Campaigns, Top-Up History)<br>• `/top-up/campaigns/new` (Tạo mới chiến dịch nạp tiền)<br>• `/top-up/campaigns/:id` (Chỉnh sửa chiến dịch)<br>• `/top-up/campaigns/:id/preview` (Xem trước danh sách học sinh thụ hưởng & dự toán ngân sách)<br>• `/top-up/runs/:id` (Nhật ký thực thi & kết quả giải ngân) |
| **Tiêu Đề Trang (Title)** | `EduFAMS \| Admin Portal` |
| **Heading Chính (H1)** | `Education Account Top-Up Management` (`#top-up-page-heading`) |
| **Phân Nhóm Điều Hướng** | `EDUSAVE` (Menu order: 20) |
| **Phân Quyền Truy Cập (RBAC)** | `MOEHQ` (`admin@IAM.edu.vn`) |
| **API Endpoints** | • `GET /education-account/v1/top-ups/campaigns`<br>• `POST /education-account/v1/top-ups/campaigns`<br>• `GET /education-account/v1/top-ups/campaigns/{id}`<br>• `PUT /education-account/v1/top-ups/campaigns/{id}`<br>• `POST /education-account/v1/top-ups/campaigns/preview`<br>• `POST /education-account/v1/top-ups/campaigns/execute`<br>• `GET /education-account/v1/top-ups/batches/{id}`<br>• `GET /education-account/v1/top-ups/batches/{id}/items`<br>• `GET /education-account/v1/top-ups/history`<br>• `POST /education-account/v1/top-ups/individual` |
| **Trạng Thái Khảo Sát (BSK)** | 🟢 Live DOM Verified (Playwright Chromium) |

---

## 🔍 1. Bảng Locators Chi Tiết (BSK Verified Live DOM)

### 1.1 Tab Navigation & Quản Lý Chiến Dịch (`/top-up`)
| Tên Phần Tử | Loại | Selector Tối Ưu (Playwright) | Trạng Thái / Ghi Chú |
| :--- | :--- | :--- | :--- |
| **Tab List** | `tablist` | `div[role="tablist"][aria-label="Top-Up Management Tabs"]` | Danh sách các tab điều hướng |
| **Individual Top-Up Tab** | `tab` | `button[role="tab"]:has-text("Individual Top-Up")` | Chuyển sang form nạp đơn lẻ |
| **Bulk Campaigns Tab** | `tab` | `button[role="tab"]:has-text("Bulk Campaigns")` | Màn hình quản lý chiến dịch đợt nạp |
| **Top-Up History Tab** | `tab` | `button[role="tab"]:has-text("Top-Up History")` | Lịch sử nạp và log giao dịch |
| **Search Campaigns Input** | `search` | `form[role="search"] input[type="search"]` | Placeholder: `CMP-00009` |
| **Campaign Status Filter** | `select` | `#campaign-status-filter` | Options: `all` (All), `0` (Draft), `1` (Active), `2` (Inactive) |
| **Create Campaign Button** | `button` | `button:has-text("Create Campaign")` | Điều hướng sang `/top-up/campaigns/new` |
| **Campaigns Table** | `table` | `table` | Headers: Code, Name, Amount, Batches Run, Status, Actions |
| **Row Preview Button** | `button` | `tbody tr >> button:has-text("Preview")` | Mở màn hình `/top-up/campaigns/:id/preview` |
| **Row Edit Button** | `button` | `tbody tr >> button:has-text("Edit")` | Mở màn hình `/top-up/campaigns/:id` |
| **Row Run Campaign Button** | `button` | `tbody tr >> button:has-text("Run Campaign")` | Kích hoạt ConfirmDialog thực thi chiến dịch |

### 1.2 Form Tạo Mới & Chỉnh Sửa Chiến Dịch (`/top-up/campaigns/new` & `/:id`)
| Tên Trường / Nhãn | Loại | Name / ID | Selector Tối Ưu (Playwright) | Ràng Buộc & Validation |
| :--- | :--- | :--- | :--- | :--- |
| **Campaign Name** | `text` | `#campaign-name` | `input#campaign-name` | Bắt buộc, max 150 ký tự |
| **Amount per Student** | `currency` | `#campaign-amount` | `input#campaign-amount` | Bắt buộc, số dương `> 0`, SGD |
| **Operational Status** | `select` | `#campaign-status` | `select#campaign-status` | Chỉ hiện khi Edit (`Draft`, `Active`, `Inactive`) |
| **Description** | `textarea`| `#campaign-desc` | `textarea#campaign-desc` | Tùy chọn, tối đa 500 ký tự |
| **Minimum Age** | `number` | `#min-age` | `input#min-age` | Ranh giới 6 - 16, $\le$ Maximum Age |
| **Maximum Age** | `number` | `#max-age` | `input#max-age` | Ranh giới 6 - 16, $\ge$ Minimum Age |
| **Min Balance Threshold**| `currency` | `#min-balance` | `input#min-balance` | Ngưỡng số dư tài khoản tối thiểu |
| **Max Balance Threshold**| `currency` | `#max-balance` | `input#max-balance` | Ngưỡng số dư tài khoản tối đa |
| **Cancel Button** | `button` | `-` | `button:has-text("Cancel")` | Quay lại danh sách chiến dịch |
| **Save and Preview Button**| `button` | `-` | `button:has-text("Save and Preview")` | Lưu và chuyển sang màn hình Preview |
| **Back Link** | `button` | `-` | `button:has-text("Back")` | Quay lại `/top-up?tab=campaigns` |

### 1.3 Màn Hình Xem Trước & Dự Báo Ngân Sách (`/top-up/campaigns/:id/preview`)
| Tên Phần Tử | Loại | Selector Tối Ưu (Playwright) | Nội Dung / Chức Năng |
| :--- | :--- | :--- | :--- |
| **Eligible Count Metric** | `tile` | `div[class*="tilePrimary"] div[class*="tileValue"]` | Tổng số học sinh đủ điều kiện nhận cấp tiền |
| **Forecast Total Metric** | `tile` | `div[class*="tileSuccess"] div[class*="tileValue"]` | Tổng ngân sách dự kiến giải ngân (SGD) |
| **Run Now / Execute** | `button` | `button:has-text("Run Now")` | Kích hoạt ConfirmDialog thực thi batch |
| **Sample Accounts Search** | `search` | `form[role="search"] input[type="search"]` | Lọc danh sách mẫu học sinh thụ hưởng |
| **Sample Accounts Table** | `table` | `table` | Columns: Student Name, Wallet Code, Age, Current Balance, Projected Balance |
| **Confirm Run Dialog** | `dialog` | `[role="dialog"]:has-text("Execute Top-Up Campaign")` | Modal xác nhận cấp ngân sách thực tế |
| **Dialog Confirm Run** | `button` | `[role="dialog"] button:has-text("Run Now")` | Xác nhận gửi lệnh chạy batch đồng bộ |
| **Dialog Cancel** | `button` | `[role="dialog"] button:has-text("Cancel")` | Hủy thao tác |

### 1.4 Nhật Ký Thực Thi & Báo Cáo Giải Ngân (`/top-up/runs/:id`)
| Tên Phần Tử | Loại | Selector Tối Ưu (Playwright) | Nội Dung / Chức Năng |
| :--- | :--- | :--- | :--- |
| **Total Disbursed Metric** | `tile` | `div[class*="tilePrimary"] div[class*="tileValue"]` | Tổng số tiền đã giải ngân thành công |
| **Success Count Metric** | `tile` | `div[class*="tileSuccess"] div[class*="tileValue"]` | Số lượng tài khoản giao dịch thành công |
| **Failed Count Metric** | `tile` | `div[class*="tileError"] div[class*="tileValue"]` | Số lượng tài khoản bị thất bại/bỏ qua |
| **Batch Item Search** | `search` | `form[role="search"] input[type="search"]` | Tìm kiếm NRIC / Mã giao dịch |
| **Outcome Status Filter** | `select` | `#item-status-filter` | Options: `all`, `Success`, `Failed` |
| **Export CSV Button** | `button` | `button:has-text("Export CSV")` | Tải xuống file CSV chi tiết các bản ghi |
| **Batch Items Table** | `table` | `table` | Columns: Student Name, Amount, Status, Reason / Error, Transaction ID, Processed At |

---

## 🔄 2. Đặc Tả Luồng Nghiệp Vụ Chi Tiết (Functional Flow & State Machine)

```mermaid
flowchart TD
    Start([Truy cập /top-up]) --> TabCampaigns[Chọn Tab 'Bulk Campaigns']
    TabCampaigns --> CreateClick[Click 'Create Campaign']
    CreateClick --> FormNew[/top-up/campaigns/new: Nhập Tên, Tiền/HS, Tiêu chí Tuổi & Số dư]
    
    FormNew --> ValCheck{Validation Form Hợp Lệ?}
    ValCheck -- Không --> ShowInlineErr[Hiển thị viền đỏ và lỗi trường nameError, amountError, ageError]
    ValCheck -- Có --> ClickSavePreview[Click 'Save and Preview']
    
    ClickSavePreview --> SaveAPI[POST /education-account/v1/top-ups/campaigns]
    SaveAPI --> PreviewPage[/top-up/campaigns/:id/preview: Hiển thị Tổng HS & Dự toán Ngân sách]
    
    PreviewPage --> ReviewData{Kiểm tra Forecasted Total?}
    ReviewData -- Không đạt --> BackEdit[Click 'Back to Campaign' sửa tiêu chí]
    ReviewData -- Đạt --> ClickRun[Click 'Run Now']
    
    ClickRun --> ConfirmModal[Hiển thị ConfirmDialog: Xác nhận nạp tiền]
    ConfirmModal --> ConfirmAction{Xác nhận?}
    ConfirmAction -- Cancel --> PreviewPage
    ConfirmAction -- Confirm --> ExecAPI[POST /education-account/v1/top-ups/campaigns/execute]
    
    ExecAPI --> RunDetail[/top-up/runs/:id: Xem Tiến độ, Success/Failed Counters & Export CSV]
    RunDetail --> End([Hoàn tất đợt nạp])
```

### 2.1 Tiêu Chí Nghiệm Thu (Acceptance Criteria) & Business Rules
1. **Ràng buộc tên chiến dịch (`name`)**: Không được để trống, tự động trim khoảng trắng thừa, giới hạn tối đa 150 ký tự.
2. **Ràng buộc số tiền (`amountPerStudent`)**: Bắt buộc là số dương lớn hơn 0 SGD.
3. **Ma trận BVA Tiêu chí tuổi (`minAge`, `maxAge`)**:
   - Khoảng tuổi hợp lệ: 6 đến 16 tuổi.
   - Biên hợp lệ: `minAge = 6`, `maxAge = 16`.
   - Biên vi phạm: `minAge > maxAge` (ví dụ `min = 12, max = 10`) $\rightarrow$ Kích hoạt lỗi: *"Minimum age cannot be greater than maximum age."*
4. **Ma trận BVA Tiêu chí số dư (`minBalance`, `maxBalance`)**:
   - `minBalance > maxBalance` $\rightarrow$ Kích hoạt lỗi: *"Minimum balance cannot be greater than maximum balance."*
5. **State Transition**:
   - Chiến dịch mới tạo luôn có trạng thái mặc định là `Draft (0)`.
   - Chỉ khi được kích hoạt hoặc hoàn thiện mới chuyển sang `Active (1)`.
   - Khi chiến dịch được kích hoạt `execute`, hệ thống sinh ra `BatchRunId` và tự động điều hướng sang màn hình xem tiến độ `/top-up/runs/:id` hoặc quay lại danh sách với toast thông báo.

---

## 💻 3. Playwright Page Object Snippet Khuyến Nghị

```python
"""
pages/f02/top_up_page.py
Page Object đại diện cho cụm tính năng Top-Up Management (Admin Portal)
Verified via BSK Live DOM Reconnaissance.
"""
from typing import Optional
from playwright.sync_api import Locator, Page
from pages.base_page import BasePage


class TopUpPage(BasePage):
    """Main Orchestrator for Top-Up Management (/top-up and wizard flows)."""
    URL = "http://localhost:5173/top-up"

    def __init__(self, page: Page):
        super().__init__(page)

    # --- Tabs ---
    @property
    def individual_tab(self) -> Locator:
        return self.page.locator('button[role="tab"]:has-text("Individual Top-Up")')

    @property
    def campaigns_tab(self) -> Locator:
        return self.page.locator('button[role="tab"]:has-text("Bulk Campaigns")')

    @property
    def history_tab(self) -> Locator:
        return self.page.locator('button[role="tab"]:has-text("Top-Up History")')

    # --- Campaigns List Tab ---
    @property
    def create_campaign_btn(self) -> Locator:
        return self.page.locator('button:has-text("Create Campaign")')

    @property
    def campaign_search_input(self) -> Locator:
        return self.page.locator('form[role="search"] input[type="search"]')

    @property
    def campaign_status_filter(self) -> Locator:
        return self.page.locator("#campaign-status-filter")

    @property
    def campaigns_table(self) -> Locator:
        return self.page.locator("table")

    # --- Campaign Create/Edit Form Fields ---
    @property
    def campaign_name_input(self) -> Locator:
        return self.page.locator("#campaign-name")

    @property
    def campaign_amount_input(self) -> Locator:
        return self.page.locator("#campaign-amount")

    @property
    def campaign_status_select(self) -> Locator:
        return self.page.locator("#campaign-status")

    @property
    def campaign_desc_textarea(self) -> Locator:
        return self.page.locator("#campaign-desc")

    @property
    def min_age_input(self) -> Locator:
        return self.page.locator("#min-age")

    @property
    def max_age_input(self) -> Locator:
        return self.page.locator("#max-age")

    @property
    def min_balance_input(self) -> Locator:
        return self.page.locator("#min-balance")

    @property
    def max_balance_input(self) -> Locator:
        return self.page.locator("#max-balance")

    @property
    def save_and_preview_btn(self) -> Locator:
        return self.page.locator('button:has-text("Save and Preview")')

    @property
    def cancel_btn(self) -> Locator:
        return self.page.locator('button:has-text("Cancel")')

    # --- Preview & Execute Screen ---
    @property
    def preview_eligible_count(self) -> Locator:
        return self.page.locator('div[class*="tilePrimary"] div[class*="tileValue"]')

    @property
    def preview_total_amount(self) -> Locator:
        return self.page.locator('div[class*="tileSuccess"] div[class*="tileValue"]')

    @property
    def run_now_btn(self) -> Locator:
        return self.page.locator('button:has-text("Run Now")')

    @property
    def confirm_run_dialog(self) -> Locator:
        return self.page.locator('[role="dialog"]:has-text("Execute Top-Up Campaign")')

    @property
    def confirm_run_dialog_confirm_btn(self) -> Locator:
        return self.confirm_run_dialog.locator('button:has-text("Run Now")')

    # --- Actions / Workflows ---
    def navigate(self) -> None:
        self.page.goto(self.URL, wait_until="networkidle")

    def open_campaigns_tab(self) -> None:
        self.campaigns_tab.click()
        self.page.wait_for_load_state("networkidle")

    def fill_campaign_form(
        self,
        name: str,
        amount: str,
        min_age: Optional[str] = None,
        max_age: Optional[str] = None,
        min_balance: Optional[str] = None,
        max_balance: Optional[str] = None,
        description: str = "",
    ) -> None:
        self.campaign_name_input.fill(name)
        self.campaign_amount_input.fill(amount)
        if min_age:
            self.min_age_input.fill(min_age)
        if max_age:
            self.max_age_input.fill(max_age)
        if min_balance:
            self.min_balance_input.fill(min_balance)
        if max_balance:
            self.max_balance_input.fill(max_balance)
        if description:
            self.campaign_desc_textarea.fill(description)

    def submit_and_preview(self) -> None:
        self.save_and_preview_btn.click()
        self.page.wait_for_load_state("networkidle")

    def execute_campaign(self) -> None:
        self.run_now_btn.click()
        self.confirm_run_dialog.wait_for(state="visible", timeout=5000)
        self.confirm_run_dialog_confirm_btn.click()
```

---

## 🎯 4. Tiêu Chí Xác Nhận Pass/Fail & Error Handling (Pass/Fail Oracles & Assertions)

### 4.1 Tiêu Chí Xác Nhận Thành Công (Pass Oracles)
| Hành Động / Kịch Bản Kiểm Thử | Loại UI Feedback | Selector Playwright Tối Ưu | Kỳ Vọng Text / Giá Trị | Playwright Assertion Cú Pháp Mẫu (Dành Cho `tests/`) |
| :--- | :--- | :--- | :--- | :--- |
| **Lưu và Mở Xem trước Chiến dịch (Save & Preview)** | Chuyển tiếp sang màn hình Preview | Tiêu đề hoặc Card giá trị | Hiển thị số lượng học sinh thụ hưởng & Tổng tiền SGD | `expect(page.locator('div[class*="tilePrimary"] div[class*="tileValue"]')).to_be_visible()`<br>`expect(page.locator('button:has-text("Run Now")')).to_be_visible()` |
| **Thực thi giải ngân Chiến dịch (Run Now)** | Hộp thoại xác nhận & Trạng thái chạy | `[role="dialog"]` | Modal xác nhận giải ngân xuất hiện | `expect(page.locator('[role="dialog"]:has-text("Execute")')).to_be_visible()` |
| **Chiến dịch chạy thành công** | Cập nhật Status Badge trên Bảng | `tbody tr [class*="badge"]` | Status chuyển thành `COMPLETED` hoặc `RUNNING` | `expect(page.locator("tbody tr [class*='badge']").first).to_have_text(re.compile(r"COMPLETED|RUNNING"))` |
| **Chiến dịch mới hiển thị trên Danh sách** | Dòng dữ liệu mới trên Bảng | `tbody tr` | Tên chiến dịch và số tiền SGD hiển thị | `expect(page.locator(f"tbody tr:has-text('{campaign_name}')")).to_be_visible()` |

---

### 4.2 Tiêu Chí Bắt Lỗi & Xử Lý Ngoại Lệ (Fail & Error Handling Feedback)
| Tình Huống Lỗi / Trigger | Loại UI Feedback | Selector Playwright Tối Ưu | Mã Lỗi & Text Kỳ Vọng | Playwright Assertion Cú Pháp Mẫu (Dành Cho `tests/`) |
| :--- | :--- | :--- | :--- | :--- |
| **Để trống Tên chiến dịch hoặc Số tiền** | Inline Error Text & viền đỏ | `#campaign-name ~ [class*="error"], #campaign-amount ~ [class*="error"]` | `"Campaign name is required"` / `"Required"` | `expect(page.locator('#campaign-name')).to_have_attribute("aria-invalid", "true")`<br>`expect(page.locator('#campaign-name ~ [class*="error"]')).to_be_visible()` |
| **Số tiền giải ngân mỗi học sinh $\le 0$** | Inline Error Text & viền đỏ | `#campaign-amount ~ [class*="error"]` | `"Amount must be greater than 0"` | `expect(page.locator('#campaign-amount')).to_have_attribute("aria-invalid", "true")` |
| **Độ tuổi tối thiểu lớn hơn độ tuổi tối đa** | Inline Error Text dưới ô Min Age | `#min-age ~ [class*="error"], p` | `"Minimum age cannot exceed maximum age"` | `expect(page.locator('#min-age ~ [class*="error"]')).to_contain_text("exceed")` |
| **Số dư tối thiểu lớn hơn số dư tối đa** | Inline Error Text dưới ô Min Balance | `#min-balance ~ [class*="error"], p` | `"Minimum balance cannot exceed maximum balance"` | `expect(page.locator('#min-balance ~ [class*="error"]')).to_contain_text("exceed")` |

