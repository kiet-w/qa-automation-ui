# Enterprise QA Automation UI Framework — Ngữ Cảnh Hệ Thống Hiện Tại (Current System Context)

> **Mục tiêu:** Cung cấp bức tranh toàn cảnh, chi tiết và đầy đủ nhất về hiện trạng mã nguồn, kiến trúc kiểm thử, các User Story đã/đang triển khai, công cụ trinh sát (Reconnaissance Tools), cùng quy tắc phát triển cho AI Coding Assistants và QA/Automation Engineers.  
> **Repository:** `automation-ui` (`kiet-w/qa-automation-ui`)  
> **Ngôn ngữ & Runtime:** Python 3.10+ (Playwright Sync API) • Shell (Bash)  
> **Testing Core:** `pytest` • `pytest-xdist` • `pytest-json-report`  
> **Reporting Engine:** 100% Offline ExtentReports Engine (Zero External CDN, Pure SVG Math, Base64 Media)  
> **Trạng thái Git:** Branch `main` (Ahead `origin/main` 2 commits: `86af9de`, `88d99d7`)  
> **Cập nhật gần nhất:** Tháng 10/2026  

---

## 1. Tổng Quan Dự Án & Mục Đích (Executive Summary)

Dự án `automation-ui` là một Framework kiểm thử tự động hóa giao diện (UI Automation Framework) cấp độ doanh nghiệp (Enterprise-grade), được thiết kế xoay quanh tiêu chuẩn:
- **Độ tin cậy tối đa & Zero Flakiness**: Tuyệt đối không dùng `time.sleep()`, tận dụng 100% auto-waiting của Playwright.
- **Giám sát lỗi 2 cổng (Dual-Gate Error Supervision)**: Tách bạch triệt để lỗi kỹ thuật hạ tầng (Network timeout, Browser crash) khỏi lỗi nghiệp vụ ứng dụng (Bug / Validation error).
- **Cách ly tuyệt đối theo Ticket (Ticket-Driven Isolation)**: Chạy song song độc lập, có khóa xử lý xung đột (`fcntl.flock`), báo cáo và lưu trữ lịch sử video/HTML theo từng User Story riêng biệt.
- **Báo cáo Offline 100%**: Tạo file HTML tự đóng gói hoàn chỉnh (monolithic) chứa video WebM Base64, ảnh chụp màn hình Base64, biểu đồ SVG vẽ bằng toán Python thuần túy, và tính năng đồng bộ bấm bước trên sơ đồ để nhảy đúng timestamp video.

---

## 2. 5 Nguyên Tắc Kiến Trúc Bất Biến (5 Core Architectural Invariants)

Framework bắt buộc tuân thủ 5 nguyên tắc bất biến (được giám sát bằng cả Unit Tests AST tại `tests/unit/test_architecture_invariants.py`):

| Invariant | Nguyên tắc | Chi tiết thực thi |
|---|---|---|
| **Invariant 1** | **Zero Assertions in Page Objects** | Tuyệt đối không đặt `assert` hoặc logic kiểm tra kết quả trong `pages/` và `components/`. Page Object chỉ thực hiện hành động (click, fill, toggle) và trả về trạng thái UI snapshot (`get_state_snapshot()`). Mọi assertion thuộc về `tests/`. |
| **Invariant 2** | **Zero Hardcoded Test Data** | Toàn bộ dữ liệu biểu mẫu, thông tin định danh, tài khoản, email, địa chỉ phải đọc từ `data/*.json` hoặc fixtures. Test suite bắt buộc phải deep-copy payload (`copy.deepcopy(...)`) trước khi biến tấu để tránh xung đột dữ liệu song song. |
| **Invariant 3** | **Traceability & Đặt Tên Test Case** | Mỗi test function phải đặt tên dạng `test_tc_<scenario_id>_...` và tương ứng 1:1 với Acceptance Criteria (AC). Phải có docstring chuẩn gồm 3 mục: `Scenario`, `Test Data`, `Expected Behavior`. |
| **Invariant 4** | **Zero `time.sleep()`** | Cấm dùng `time.sleep()`. Dùng Playwright built-in waiting, `wait_for_selector()`, `wait_for_load_state()`, hoặc `page.wait_for_timeout()` khi cần mô phỏng độ trễ tự nhiên của người dùng. |
| **Invariant 5** | **Xử Lý Lỗi Hai Cổng & Hook Phân Loại** | **Business Gate**: Dùng `Exceptor` (`core/exceptor.py`) hoặc `@pytest.mark.xfail(strict=True)`.<br>**Infrastructure Gate**: Lỗi kỹ thuật hạ tầng (Timeout, TargetClosed, Net disconnect) được tự động phân loại thông qua hook `pytest_runtest_makereport` tại `conftest.py` tra cứu vào `ErrorCatalog` (`core/catalog.py`). |

---

## 3. Cấu Trúc Thư Mục Toàn Diện (Directory Topology)

```text
automation-ui/
├── core/                                    # 🛡️ Tầng Giám sát & Phân loại lỗi
│   ├── __init__.py                          # Export Exceptor, Interceptor, Exceptions
│   ├── catalog.py                           # 8 biểu thức regex phân loại lỗi kỹ thuật (TIMEOUT, CRASH, NET...)
│   ├── exceptions.py                        # BusinessAssertionError vs InfrastructureError
│   ├── exceptor.py                          # Cổng thẩm định nghiệp vụ (expect_success, expect_rejection, bug hunters)
│   └── interceptor.py                       # Giám sát tương tác Playwright trực tiếp
│
├── pages/                                   # 📄 Page Object Model (Không chứa assert)
│   ├── __init__.py                          # Export BasePage, BingHomePage, CurriculaTrainerPage...
│   ├── base_page.py                         # Thao tác nền tảng: click, fill, wait_for_visible, screenshot, dialog
│   ├── bing_home_page.py                    # Locators & luồng tìm kiếm Bing
│   ├── bing_results_page.py                 # Giải mã redirect link & xử lý kết quả Bing
│   ├── curricula_trainer_page.py            # Form tạo Trainer Account (fill form, toggles, get_state_snapshot)
│   └── youtube_page.py                      # Trang YouTube: tìm kiếm kênh, lọc video cũ nhất, phát video
│
├── components/                              # 🧩 UI Widgets tái sử dụng
│   ├── __init__.py
│   └── search_box.py                        # Ô tìm kiếm gõ phím giả lập người thật (press_sequentially)
│
├── data/                                    # 🗄️ Dữ liệu kiểm thử tham số hóa
│   ├── curricula_trainer_data.json          # Bộ hồ sơ mẫu hợp lệ, ranh giới, ngoại lệ cho US04
│   ├── search_data.json                     # Từ khóa tìm kiếm, cấu hình video cho US01
│   └── fixtures/                            # Tệp đính kèm kiểm thử upload ID
│       ├── valid_id.pdf                     # File PDF hợp lệ 2MB
│       ├── valid_id.png                     # File ảnh PNG hợp lệ
│       ├── oversized_11mb.pdf               # File >10MB kiểm tra bắt lỗi dung lượng
│       ├── invalid_document.txt             # File .txt kiểm tra MIME filter
│       ├── malicious.exe                    # File thực thi kiểm tra bảo mật
│       └── document.docx                    # File Word không thuộc định dạng cho phép
│
├── tests/                                   # 🧪 Các bộ kiểm thử tự động
│   ├── __init__.py
│   ├── base_test.py                         # Lớp cha BaseTest (inject page, curricula, step tracker, fixture helper)
│   │
│   ├── unit/                                # Kiểm thử đơn vị nội bộ framework (26 tests)
│   │   ├── test_architecture_invariants.py  # Dùng AST kiểm tra cấm assert trong POM, cấm time.sleep, cấm CDN
│   │   ├── test_catalog.py                  # Kiểm tra độ chính xác của regex phân loại lỗi hạ tầng
│   │   ├── test_exceptor.py                 # Kiểm tra logic 4 cổng phán quyết của Exceptor
│   │   └── test_interceptor.py              # Kiểm tra bọc lệnh và chuyển dịch exception của Interceptor
│   │
│   ├── us01_bing_search/                    # US01: E2E Bing -> YouTube -> VTV Video cũ nhất
│   │   └── test_bing_search.py              # Luồng E2E 5 bước kèm bot evasion & chụp ảnh bằng chứng
│   │
│   └── us04_curricula_trainer/              # US04: Curricula Trainer Account (68 Test Cases, 7 Suites)
│       ├── requirements/                    # Đặc tả AC gốc và Ma trận truy vết
│       │   ├── us04_curricula_trainer_AC.md
│       │   └── us04_curricula_trainer_traceability_matrix.md
│       ├── test_ts01_personal_info.py       # TS01: Thông tin cá nhân, NRIC/FIN, ngày sinh, thuế, upload ID
│       ├── test_ts02_contact_info.py        # TS02: Email, mã vùng, số điện thoại chính / phụ
│       ├── test_ts03_emergency_contact.py   # TS03: Thông tin người liên hệ khẩn cấp
│       ├── test_ts04_singapore_address.py   # TS04: Địa chỉ Singapore (Postal code, Block, Unit)
│       ├── test_ts05_non_singapore_address.py # TS05: Địa chỉ ngoài Singapore (Country, State, City)
│       ├── test_ts06_save_action.py         # TS06: Lưu biểu mẫu, kiểm tra trùng lặp, chống double-click
│       └── test_ts07_cancel_action.py       # TS07: Hủy biểu mẫu, dialog confirm, dirty state detection
│
├── tools/                                   # 🛠️ Bộ công cụ trinh sát, phá có kỷ luật & môi trường
│   ├── env/                                 # Quản lý microservices backend, proxy xác thực, seed DB
│   ├── specs_sync/                          # Đồng bộ Google Drive và bóc tách bảng tính test cases sang markdown
│   └── recon_and_resilience/                # Trinh sát thụ động DOM (`recon.sh`) & toolkit phá ("break_it")
│
├── specs/                                   # 📋 Nguồn Sự Thật Duy Nhất (Single Source of Truth)
│   ├── raw/                                 # File gốc Word/Excel từ Google Drive (.docx, .xlsx, .xlsm)
│   ├── md/                                  # 100% Markdown đặc tả FS-01 đến FS-10, Business Rules, ACs
│   └── [agile] fs -> specs                  # Symlink tương thích ngược cho các bài test và script cũ
│
├── copy/                                    # 🏢 Ứng dụng mục tiêu đang test (BẤT KHẢ XÂM PHẠM - Invariant 0)
│   ├── edufams-backend/                     # Microservices backend (.NET)
│   └── edugovernment-frontend/              # Cổng web e-Service (React / Vite)
│
├── docs/                                    # 📚 Đặc tả, kiến trúc, quyết định kỹ thuật
│   ├── framework/                           # Tài liệu kỹ thuật của tool (adr, context, guidelines, eval)
│   └── test-specs/                          # Ma trận test cases chi tiết theo module (fs08, us08, us04, us01)
│
├── archive/                                 # 📦 Lưu trữ file nặng (Edu_Project_S2_Oct22.zip) & assets cũ
│
├── reporting/                               # 📊 Engine Báo Cáo HTML ExtentReports 100% Offline
│   ├── core/                                # Parser JSON, Media Base64 encoder, Document Builder
│   ├── charts/                              # Pure SVG (Donut chart, Bar chart, Pipeline timeline, Diagram)
│   └── assets/                              # CSS dark mode hiện đại và JS xử lý 2-way sync
│
├── reports/                                 # 📂 Thư mục Artifacts kết quả (Cô lập theo từng Ticket)
│   ├── us01_bing_search/
│   ├── us04_curricula_trainer/              # execution_report.html, history/, test-results/ (WebM videos)
│   ├── fs08/
│   ├── fs09/
│   └── unit/
│
├── conftest.py                              # Central fixtures: browser setup, video recording, makereport hook
├── run_tests.py                             # Bộ điều phối chạy test: Concurrency lock, Pytest, HTML Generator
├── generate_report.py                       # CLI độc lập sinh lại báo cáo HTML từ file report.json có sẵn
├── curricula_trainer_account.html -> data/fixtures/mock_pages/curricula_trainer_account.html # Symlink mock web
└── pytest.ini, requirements.txt, README.md, AGENTS.md
```

---

## 3.1 NGUYÊN TẮC BẤT DI BẤT DỊCH DÀNH CHO AI CODING: ZERO ASSUMPTIONS
> ⚠️ **ĐÂY LÀ DỰ ÁN UI AUTOMATION TESTING CHUYÊN NGHIỆP — TUYỆT ĐỐI KHÔNG ĐƯỢC GIẢ ĐỊNH (ZERO ASSUMPTIONS)**
>
> 1. **CHỈ NHẬN THÔNG TIN TỪ TÀI LIỆU ĐẶC TẢ**: AI coding tuyệt đối không được tự ý bịa hoặc suy diễn bất kỳ giá trị nào (giá trị input biên, format dữ liệu, thông báo lỗi, mã lỗi `MSG-xxxx`, trạng thái nút bấm, vòng đời status hay công thức tính toán tài chính).
> 2. **NGUỒN THAM CHIẾU BẮT BUỘC TRONG `specs/md/`**:
>    - **Business Rules cốt lõi**: Đọc [`specs/md/FS_SPECIFICATIONS_SUMMARY.md`](file:///home/baudui/automation-ui/specs/md/FS_SPECIFICATIONS_SUMMARY.md) và [`specs/md/EAFAMS_UI_SPECIFICATION_AND_INTERACTION_GUIDE.md`](file:///home/baudui/automation-ui/specs/md/EAFAMS_UI_SPECIFICATION_AND_INTERACTION_GUIDE.md).
>    - **Acceptance Criteria đầy đủ**: Đọc [`specs/md/EAFAMS_SPLIT_PAYMENT_AND_AI_FAS_TEST_CASES_AND_AC.md`](file:///home/baudui/automation-ui/specs/md/EAFAMS_SPLIT_PAYMENT_AND_AI_FAS_TEST_CASES_AND_AC.md) và [`specs/md/Test Cases/`](file:///home/baudui/automation-ui/specs/md/Test%20Cases/).
>    - **31 Quyết định nghiệp vụ client**: Đọc [`specs/md/MEETINGS_AND_DECISIONS_SUMMARY.md`](file:///home/baudui/automation-ui/specs/md/MEETINGS_AND_DECISIONS_SUMMARY.md).
>    - **Từng phân hệ Functional Spec**: Đọc [`specs/md/FS document/`](file:///home/baudui/automation-ui/specs/md/FS%20document/) (`FS-01` đến `FS-10`).
> 3. **KHI THIẾU THÔNG TIN HOẶC GẶP MÂU THUẪN**:
>    - Tra cứu `specs/md/FSD_ALIGNMENT_AND_GAP_AUDIT_REPORT.md`.
>    - Nếu tài liệu chưa có: **DỪNG LẠI VÀ HỎI USER/PO/BA**, tuyệt đối không tự bịa logic hay giả lập hành vi theo cảm tính.
```

---

## 4. Chi Tiết Các Hạng Mục Kiểm Thử & Phạm Vi Nghiệp Vụ

### 4.1 User Story 1: Bing Search -> YouTube Navigation (`tests/us01_bing_search`)
- **Mục tiêu**: Luồng tự động hóa tương tác web bên ngoài với khả năng chống bot, gõ phím giả lập người thật.
- **5 Bước thực thi**:
  1. Điều hướng Bing Search Engine với stealth options.
  2. Tìm kiếm Facebook, xác minh kết quả tự nhiên đầu tiên.
  3. Tìm kiếm YouTube, giải mã redirect URL để tránh `TargetClosedError`.
  4. Điều hướng vào kênh YouTube mục tiêu (`VTV24`).
  5. Chuyển sang tab Videos, lọc video cũ nhất (Earliest/Oldest), click phát video và chụp screenshot độ phân giải cao làm bằng chứng.

### 4.2 User Story 2 & 4: Curricula Trainer Account Form (`tests/us04_curricula_trainer`)
- **Quy mô**: 68 Test Cases chia làm 7 Suites, bám sát từng dòng của `AC.md`.
- **10 Lỗi Nghiệp Vụ Đã Được Catalog & Assert (Bug Matrix)**:

| Bug ID | Phân hệ | Mô tả lỗi trong ứng dụng (`curricula_trainer_account.html`) | Test Case phát hiện | Cổng Exceptor áp dụng |
|---|---|---|---|---|
| **BUG-001** | Save Action | Không chặn trùng lặp Email; hệ thống chấp nhận lưu email đã tồn tại | `TC_SAV_003`, `TC_SAV_004` | `expect_bug_if_accepted` |
| **BUG-002** | Save Action | Không chặn trùng lặp ID Number | `TC_SAV_005` | `expect_bug_if_accepted` |
| **BUG-003** | Non-SG Address | Dropdown quốc gia ngoài SG vẫn hiển thị "Singapore" | `TC_NSG_002` | `expect_bug_if_rejected` |
| **BUG-004** | Save Action | Double-click nhanh nút Save làm gửi duplicate request | `TC_SAV_006` | `expect_bug_if_accepted` |
| **BUG-005** | Emergency Contact | Dropdown quan hệ hiển thị Father/Mother thay vì chuẩn FSD | `TC_EC_003` | `expect_bug_if_rejected` |
| **BUG-006** | Cancel Action | Nút Cancel bỏ qua trạng thái thay đổi (dirty) của radio/dropdown | `TC_CAN_004` | `expect_bug_if_accepted` |
| **BUG-007** | Form Inputs | Không chặn max length tại 5 trường văn bản quan trọng | `TC_PI_003`, `TC_SG_007` | `expect_bug_if_accepted` |
| **BUG-008** | Validation | Câu thông báo lỗi bắt buộc không khớp câu chữ chuẩn FSD | `TC_PI_019`, `TC_CI_009` | `expect_rejection` |
| **BUG-009** | Personal Info | Dropdown ID Type chứa tùy chọn không có trong tài liệu ("S-Pass") | `TC_PI_006` | `expect_bug_if_rejected` |
| **BUG-010** | Personal Info | Bỏ qua thuật toán kiểm tra Checksum của NRIC/FIN | `TC_PI_008` | `expect_bug_if_accepted` |

### 4.3 User Story 8: Parent Portal – SingPass, Education Account & Profile (`docs/us08_parent_portal/`)
- **Tài liệu tham chiếu**: `US08_Parent_Portal_Full_Spec_and_QA_Matrix.md` (422 dòng phân tích chuyên sâu).
- **Phạm vi**:
  - Đăng nhập Mock SingPass, đồng bộ dữ liệu phiên theo NRIC.
  - Bình đẳng quyền phụ huynh (`D-19`): Cha/Mẹ đều xem đầy đủ thông tin các con liên kết.
  - Địa chỉ cư trú bất biến (`D-20`): Trích xuất trực tiếp từ SingPass, chỉ đọc.
  - Sắp xếp Card con ở trang chủ theo thứ tự ưu tiên; hiển thị số dư Education Account (EA), giao dịch pending, lịch sử.
  - Cập nhật thông tin My Details (Phone, Email, Mailing Address). Khóa quyền sửa khi tất cả các con $\ge$ 16 tuổi.
  - Hết hạn phiên tự động sau 15 phút không thao tác (`D-22`, lỗi `MSG-0002`).
- **Phần mềm kiểm thử API kèm theo (`automation-testing/`)**:
  - Đã tích hợp client, mock server, test suite kiểm thử API cho US08 với cơ chế chia pool user cách ly giữa các worker song song.

---

## 5. Bộ Công Cụ Trinh Sát & Thăm Dò Mới (`tools/`)

Gần đây dự án bổ sung công cụ hỗ trợ QA kiểm toán thực địa ứng dụng Web đang chạy:
1. **`tools/recon.sh`**:
   - Tự động hóa trinh sát thụ động (Passive Recon) bằng công cụ `bsk` trên trình duyệt đang mở.
   - Thu thập 4 loại artifact: DOM hoàn chỉnh (`page_dom.html`), Accessibility Tree Snapshot (`accessibility_snapshot.txt`), Console Logs (`console_logs.txt`), Network Requests (`network_logs.txt`), và Ảnh chụp màn hình viewport/full-page (`initial_screen.png`).
   - Lưu trữ có cấu trúc vào `reports/recon_<timestamp>/`.
2. **`tools/templates/active_probe_prompt.txt`**:
   - Mẫu chỉ thị an toàn cho AI khi thăm dò chủ động màn hình staging. Cấm tuyệt đối các hành vi phá hủy (xóa, đổi pass, thanh toán, upload file độc hại), chỉ thao tác đọc và kiểm thử giá trị biên form.
3. **`tools/templates/audit_findings.md`**:
   - Mẫu bảng ghi nhận sự kiện bất thường, bằng chứng ảnh/log, tách bạch giữa sự thật quan sát được và giả thuyết chưa kiểm chứng.

---

## 6. Cơ Chế Khóa Song Song & Lưu Trữ Lịch Sử (`run_tests.py`)

Trong các commit mới nhất, `run_tests.py` đã được nâng cấp mạnh mẽ:
1. **Ticket-Level Concurrency Lock (`fcntl.flock`)**:
   - Khi chạy test cho một ticket (ví dụ: `tests/us04_curricula_trainer`), script tự động tạo và khóa file `.run.lock` bên trong thư mục `reports/<ticket>/`.
   - Nếu có một tiến trình khác đang chạy cùng ticket đó, tiến trình mới sẽ bị từ chối ngay lập tức với mã lỗi `[LOCKED ERROR]`, bảo vệ tuyệt đối dữ liệu test và báo cáo không bị ghi đè hoặc hỏng hóc.
2. **Lưu Trữ Lịch Sử Báo Cáo Vĩnh Viễn (Permanent History Retention)**:
   - Mỗi lần chạy sinh ra một `RUN_ID` duy nhất (VD: `RUN-20261018-ABC123`).
   - Báo cáo HTML được lưu song song: file chính tại `reports/<ticket>/execution_report.html` và bản snapshot lịch sử bất biến tại `reports/<ticket>/history/<RUN_ID>.html`.
   - Toàn bộ video WebM quay lại quá trình chạy cũng được lưu trữ an toàn trong `reports/<ticket>/test-results/<RUN_ID>/`.

---

## 7. Cú Pháp Lệnh & Quy Trình Vận Hành

### Chạy kiểm thử tự động
```bash
# 1. Chạy trọn bộ US04 (giao diện Trainer Account)
python3 run_tests.py tests/us04_curricula_trainer

# 2. Chạy 1 test suite cụ thể
python3 run_tests.py tests/us04_curricula_trainer/test_ts06_save_action.py -v

# 3. Chạy song song tốc độ cao (4 workers)
python3 run_tests.py tests/us04_curricula_trainer -n 4

# 4. Chạy US01 (Bing Search & YouTube E2E)
python3 run_tests.py tests/us01_bing_search/test_bing_search.py

# 5. Chạy bộ Unit Tests kiểm tra kiến trúc và invariants
python3 run_tests.py tests/unit/
```

### Sử dụng công cụ trinh sát (Recon)
```bash
# Trinh sát thụ động một trang web staging qua bsk
./tools/recon.sh https://staging.example.com <BROWSER_ID>
```

---

## 8. Hướng Dẫn Phát Triển Cho AI Coding Assistant

1. **Khi được yêu cầu viết Test Case mới**:
   - Kế thừa lớp `BaseTest` từ `tests.base_test`.
   - Tuyệt đối không dùng `page.locator()` trực tiếp trong file test nếu locator đã có hoặc cần có trong Page Object. Hãy gọi method của Page Object (`self.curricula....`).
   - Bao bọc từng giai đoạn trong `with self.step("Step X: ..."):`.
   - Đọc dữ liệu từ `self.get_fixture_file("data/...")` hoặc fixture, deep copy trước khi sửa.
   - Thẩm định kết quả qua `Exceptor.expect_success()` hoặc `Exceptor.expect_rejection()`. Với các bug đã xác nhận, đánh dấu `@pytest.mark.xfail(strict=True)`.
2. **Khi thêm/sửa Page Object**:
   - Kế thừa từ `BasePage` (`pages.base_page`).
   - Không import hoặc dùng `assert` trong file page object.
   - Viết method snapshot `get_state_snapshot()` trả về dictionary trạng thái tĩnh (`success_visible`, `visible_errors`).
3. **Khi bảo trì Báo Cáo Offline**:
   - Giữ nguyên tắc Zero CDN trong `reporting/`. Mọi biểu đồ dùng toán hình học SVG xuất ra HTML string, mọi media đều mã hóa Base64 Data URI.
