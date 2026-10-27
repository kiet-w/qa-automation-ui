# RULE MODULE 04: AUTOMATION CODING STANDARDS, EVIDENCE & SPEC LOOKUP MATRIX
> **Mục đích**: Áp dụng khi viết mã nguồn Page Objects (`pages/`), Fixtures (`data/`), Test suites (`tests/`), Step Tracking, ExtentReports, và tra cứu đặc tả hệ thống trong `specs/md/`.
> **Trọng tâm**: Step tracking, screenshot/video evidence, 17 chỉ thị đặc biệt cho AI coding, quản lý concurrency, và ma trận tra cứu specs toàn diện.

> [!IMPORTANT]
> **Canonical path contract**: Code, imports, commands và outputs luôn dùng root paths (`core/`, `pages/`, `data/`, `tests/`, `tools/`, `reports/`). Ba folder đánh số chỉ là navigation views bằng symlink; không dùng chúng làm namespace/output path và không xóa canonical targets.

## 3. Step Tracking, Visual Overlays & Video Evidence
Tests use the `self.step()` context manager to structure execution timelines and capture step metadata/screenshot evidence. SketchVLM-style overlays are burned into WebM only when the User explicitly enables video:
```python
with self.step("Step 1: Open form and submit valid data"):
    self.curricula.open()
    self.curricula.fill_full_form(data)
    self.curricula.save()

with self.step("Step 2: Verify success confirmation"):
    snapshot = self.curricula.get_state_snapshot()
    Exceptor.expect_success(snapshot, step=self.step)
    # Or optionally attach dynamic runtime details:
    self.step.set_actual(f"Trainer ID created successfully.")
```
- **Live Step HUD Bar**: Every `with self.step(...)` block can project a floating HUD bar. It is captured in WebM only under `--video=retain-on-failure` or `--video=on`; default execution uses `--video=off`.
- **Action Radar & Spotlight**: Page Object interactions (`click_element`, `fill_text`, `save`) emit a localized radar pulse and action badge (`👆 CLICK`, `✏️ TYPE`) over the target element.
- **SketchVLM Defect Highlight**: On assertion failure, `SketchAnnotator.highlight_defect()` automatically targets the failing field, injects a multi-stroke red sketch circle and SVG arrow pointing to the bug, and displays a top `DEFECT CAPTURE` evidence banner for 1.4s before teardown.
- **AI Visual Oracle**: For complex visual layout or accessibility triage, engineers and AI assistants can run `python3 tools/sketch_vlm_oracle.py <screenshot.png>` to produce Gemini-powered `.sketch.svg` overlays.
- `actual=` is recorded automatically at runtime: on pass it confirms success; on failure it records the exception stack trace.
- **Video Delivery & Excel Integration Standard**:
  - Khi xuất báo cáo thực thi Excel (`TEST_EXECUTION_EVIDENCE_*.xlsx`), file phải đặt tại `reports/<fs_module>/<component>/`. Testcase thiết kế gốc tiếp tục nằm tại `testcases/<fs_module>/<component>/`; không đồng bộ runtime status ngược vào source thiết kế. **BẮT BUỘC CHỈ DÙNG ĐÚNG 1 TAB DUY NHẤT**.
  - Sử dụng Native Hyperlink (`cell.value = "▶ Play in Browser"`, `cell.hyperlink = url`) thay cho công thức `=HYPERLINK()` để chống lỗi ô trắng trong WPS Office/LibreOffice.
  - Offline/local evidence là mặc định. Không tự động chạy deploy hoặc upload media lên Cloudflare/dịch vụ ngoài; publishing cần yêu cầu và quyền hạn riêng của User.

---

## 4. Special Directives for AI Coding Assistants (UI Automation Standards)
When generating or modifying automated tests from Acceptance Criteria (AC), User Stories, or Test Case matrices:
1. **Zero Assumptions on Requirements (BẢN CHẤT DỰ ÁN LÀ UI AUTOMATION TESTING - ZERO ASSUMPTIONS)**:
   - AI coding agents **TUYỆT ĐỐI KHÔNG ĐƯỢC GIẢ ĐỊNH** bất kỳ giá trị nào: giá trị input biên, selector, thông báo lỗi, mã lỗi (`MSG-xxxx`), trạng thái nút bấm, hay công thức tính toán.
   - **CHỈ NHẬN THÔNG TIN** từ `specs/md/`, `specs/component_specs/`, UI/BSK inventory tại `specs/ui_bsk/`, testcase đã được phê duyệt, live DOM evidence hoặc xác nhận trực tiếp của User/PO/BA. Mọi logic kiểm thử và assertion phải có file/section/rule/AC reference.
2. **Never Guess Rejection Error Messages**: Never guess or invent exact validation error strings for edge cases not explicitly defined in the FSD. Always use `Exceptor.expect_bug_if_accepted(snapshot)` or assert rejection on the affected field without hardcoding imaginary error text. Tag unverified message formats with `[SPEC GAP]`.
3. **Never Invent Locators**: Reuse verified Page Object methods. Tra kho đã thu thập tại `specs/ui_bsk/` trước; nếu thiếu hoặc stale thì lấy lại bằng `tools/recon_bsk.py`/live DOM. Selector đã xác minh được thêm vào `pages/<module>/locators.py`, rồi dùng qua Page Object; không viết raw locator trong test.
4. **Inherit from `BaseTest`**: Subclasses use the shared page, step tracker, page factory and fixture helpers; module-specific properties chỉ được dùng khi thực sự tồn tại.
5. **Handle Native Browser Dialogs**: Nếu action kích hoạt `confirm()`/`alert()`, đăng ký dialog handler trên Page Object tương ứng trước khi click trigger.
6. **Deep Copy Data Payloads**: Always use `copy.deepcopy(data["..."])` before modifying payload dictionaries to ensure test isolation during parallel execution.
7. **Never Swallow Exceptions**: Do not wrap test assertions in empty `try...except` blocks. If an error occurs, let it raise so `StepTracker` and `pytest_runtest_makereport` can record diagnostic evidence.
8. **Strict Read-Only Guard on `copy/` (Invariant 0)**: Never touch, edit, format, patch, or delete files in `copy/`. Treat the entire `copy/` directory as 100% read-only and immutable. QA automation tests must adapt to the system under test, never modify the company codebase.
9. **Proactively Generate Disciplined Adversarial Tests (`@pytest.mark.break_it`)**: When generating test suites for any story or ticket, AI agents MUST NOT stop at "happy path" scenarios. Always check [`tools/recon_and_resilience/break_it/README.md`](file:///home/baudui/Projects/automation-ui/tools/recon_and_resilience/break_it/README.md) and consult [`tools/recon_and_resilience/break_it/test_templates.py`](file:///home/baudui/Projects/automation-ui/tools/recon_and_resilience/break_it/test_templates.py) to generate the accompanying adversarial suite covering the 6 dimensions.
10. **Use `tools/recon_and_resilience/break_it/` Scaffolding & Coverage Auditing**:
    - Run `python3 tools/recon_and_resilience/break_it/scaffold_break_it.py` to auto-scaffold a standard `break_it` test file skeleton for any new Page Object or module.
    - Run `python3 tools/recon_and_resilience/break_it/audit_coverage.py` before finalizing test deliverables to verify that test suites are not missing break_it resilience coverage.
11. **Preserve Step Evidence; Preserve Video Quality When Enabled**:
    - Always encapsulate every user action phase inside `with self.step("Step X: ..."):` so reports and screenshots retain a deterministic timeline.
    - Khi User bật video, dùng Page Object helper methods thay vì raw locators để HUD/action spotlight được ghi nhận nhất quán.
12. **Lean Concurrency Standard (`-n 3`) for Fast & RAM-Safe Execution**:
    - Khi cấu hình và chạy test, luôn tuân thủ chuẩn chạy song song `-n 3` workers. Đây là tỷ lệ vàng đã được định lượng cho môi trường hệ thống (~7.5GB RAM, ~3.6GB khả dụng), giúp rút ngắn thời gian toàn bộ test suite từ 16 phút xuống ~2-3 phút mà không vượt ngưỡng RAM hoặc gây swap thrashing.
    - Tuyệt đối không dùng `-n auto` hoặc worker quá lớn gây OOM.
13. **Ultra-Lean Media Standard (`--video=off` & Step Actions + Highlighted Actual Result)**:
    - **Tắt Video WebM Mặc Định (`--video=off`)**: Tắt hoàn toàn việc ghi video WebM nền trong `pytest.ini` cho các lần chạy test thông thường/CI. Điều này triệt tiêu hoàn toàn CPU mã hóa phần mềm, loại bỏ buffer video trong RAM (tiết kiệm ~50% RAM), và loại bỏ độ trễ flush video 2.5s - 3s ở teardown.
    - **Chỉ Bật Video Khi Debug Sâu**: Chỉ sử dụng cờ `--video=retain-on-failure` hoặc `--video=on` khi người dùng chủ động yêu cầu ghi hình video để phân tích lỗi.
    - **Chuẩn Bằng Chứng Hình Ảnh Đa Bước & Kết Quả Thực Tế Có Highlight**:
      * *Ảnh các bước thao tác (`reports/<module>/<ticket>/screenshots/<test_slug>/step_X_<action>.png`)*: Chụp theo step và highlight target/action.
      * *Ảnh kết quả thực tế (`reports/<module>/<ticket>/screenshots/<test_slug>/actual_result.png`)*: Chụp vùng Actual Result với trạng thái Pass/Defect/Error.
      * File Excel bằng chứng (`TEST_EXECUTION_EVIDENCE_*.xlsx`) liên kết trực tiếp tới `📷 Actual Result (+X steps)`.
    - **Cấu Trúc Lưu Trữ Sạch Sẽ**: Lưu ảnh theo `reports/<module>/<ticket>/screenshots/<test_slug>/`; không sinh file evidence trôi nổi ở repository root.
14. **Strict Test Suite Subdirectory Placement (Đúng Thư Mục Phụ Trách)**:
    - **CẤM TUYỆT ĐỐI** tạo, sinh hoặc ném file test trôi nổi tự do tại thư mục gốc `tests/`.
    - Khi AI Coding chịu trách nhiệm cho ticket/module nào (`<fs_module>/<component>`), **BẮT BUỘC** phải đặt toàn bộ file test code vào đúng thư mục con: `tests/<fs_module>/<component_or_ticket>/` (ví dụ: `tests/fs08/fs08-uat007-contact-update/` hoặc `tests/f10/f10-fas-submission/`).
    - Mỗi file test phải tuân thủ chuẩn slicing per-field: `test_atomic_<field>.py` (< 200 dòng) và `test_integration_<flow>.py` (< 250 dòng).
15. **Anti-Hang Directives (Triệt Tiêu Hoàn Toàn Nghẽn 30s Timeout)**:
    - CẤM viết lệnh `page.click()` trần trụi đối với các nút phụ trợ/dọn dẹp (như `cancel_button`, `close_modal`, `dialog_dismiss`) nếu form có khả năng đã tự đóng hoặc đã ở View Mode.
    - Luôn bọc kiểm tra an toàn: `if self.is_visible(selector, timeout=2000):` hoặc truyền `timeout=2000` để tránh Playwright chờ ngâm 30,000ms gây kéo dài thời gian chạy.
16. **Accurate API Mocking & Multi-Tab Isolation**:
    - Khi kiểm thử luồng lỗi mạng hoặc bảo mật (401, 500, injection), bắt buộc mock chính xác regex endpoint backend thật (ví dụ `/iam/v1/parent/update/profile`), không dùng endpoint phỏng đoán khiến mock bị trượt.
    - Luôn gọi `self.page.unroute_all()` ngay sau khi assert xong để tránh rò rỉ mock sang các ca test tiếp theo.
    - Trong kiểm thử đa tab (`context.new_page()`), do `sessionStorage` không tự chia sẻ giữa các tab, bắt buộc copy và inject token/session (ví dụ `window.sessionStorage.setItem('edusave.parent-auth.user', ...)`) vào tab mới trước khi `goto()`.
17. **Strict Ban on Autonomous Test Execution (Invariant 11 - Cấm AI Tự Tiện Chạy Code Test Automation)**:
    - Khi viết mã automation testing (Page Objects, Fixtures, Test Suites bằng Python), AI **TUYỆT ĐỐI KHÔNG ĐƯỢC TỰ Ý CHẠY/THỰC THI** code vừa viết (không chạy `pytest`, `python run_tests.py`, hay bất kỳ command chạy test nào).
    - **Quyền thực thi thuộc 100% về User**: User sẽ tự tay chạy các kịch bản test.
    - **Nhiệm vụ của AI**: AI chỉ đóng vai trò nghiên cứu, phân tích tài liệu đặc tả (`specs/md/`, `specs/component_specs/`, `testcases/`, live DOM recon) để code Python chuẩn mực, chính xác, sạch sẽ, bảo đảm cú pháp và tuân thủ tuyệt đối cấu trúc dự án.
    - Sau khi hoàn thành code, AI chỉ bàn giao file và cung cấp cú pháp lệnh thực thi mẫu để User tự sao chép và chạy.

---

## 5. Execution Commands & Concurrency Control
> [!IMPORTANT]
> **LỆNH DÀNH CHO USER TỰ CHẠY (AI TUYỆT ĐỐI KHÔNG TỰ CHẠY THEO INVARIANT 11)**:
> Khi AI bàn giao code Python, User sẽ tự chạy các lệnh kiểm thử sau từ `/home/baudui/Projects/automation-ui`:
```bash
# Run specific test suite
python3 run_tests.py tests/us04_curricula_trainer/test_ts06_save_action.py -v

# Run an entire ticket suite and auto-generate HTML report.
# run_tests.py currently forwards paths/options to pytest; it has no --ticket parser.
python3 run_tests.py tests/fs08/fs08-uat007-contact-update/
python3 run_tests.py tests/fs09/fs09-outstanding-fees-payment/
python3 run_tests.py tests/us04_curricula_trainer/
```

### Execution Isolation & Artifact Retention:
1. **Concurrency Lock**: `run_tests.py` enforces a ticket-scoped file lock (`fcntl.flock`). Concurrent runs targeting the same ticket will be safely rejected with a `[LOCKED ERROR]` to prevent test data collision and report corruption.
2. **Artifact Retention**: Execution artifacts belong under `reports/<module>/<ticket>/`. Video files exist only when the User enables video; do not promise video artifacts for the default `--video=off` mode.

---

## 6. Agile Project Knowledge Base & Single Source of Truth (`specs/` & `[agile] fs/`)

To support AI coding agents with verified, structured, and diffable project documentation, the project knowledge base is organized in canonical `specs/`. The only supported legacy alias is `[agile] fs -> specs`:

```text
specs/
├── raw/                              # Original source documents from Google Drive (.docx, .xlsx, .xlsm)
└── md/                               # 100% diffable, structured Markdown (.md) for AI coding retrieval
    ├── FS document/                  # 📄 Chuyên biệt từng Functional Specification từ FS-01 đến FS-10
    ├── Test Cases/                   # 🧪 Bộ 465 Test Cases chính thức & Defect Master Log
    ├── Documentation/                # 📝 Biên bản họp, phỏng vấn, từ điển thuật ngữ Agile & GovTech
    └── diagrams/                     # 📊 Sơ đồ kiến trúc & luồng dữ liệu tương tác (SVG / HTML)
```

### 🚨 Strict Directive for AI Coding: TUYỆT ĐỐI KHÔNG ASSUMPTION (ZERO ASSUMPTIONS)
> **MANDATE: ZERO ASSUMPTIONS UNDER ANY CIRCUMSTANCES.**
>
> 1. **BẢN CHẤT DỰ ÁN LÀ UI AUTOMATION TESTING**: AI coding agents **MUST NEVER GUESS** business logic, data models, error codes, UI validation text, button states, or status transitions.
> 2. **CHỈ NHẬN THÔNG TIN TỪ SPECS**: Mọi test case, assertion, mock response, và parameter fixture **BẮT BUỘC** trích dẫn trực tiếp từ các file Markdown trong `specs/md/`.
> 3. **XỬ LÝ KHI THIẾU THÔNG TIN**: Nếu có chi tiết chưa rõ hoặc mâu thuẫn, tra cứu ngay `specs/md/FSD_ALIGNMENT_AND_GAP_AUDIT_REPORT.md` và `specs/md/MEETINGS_AND_DECISIONS_SUMMARY.md`. Nếu vẫn chưa rõ: **DỪNG LẠI VÀ HỎI USER/PO/BA — TUYỆT ĐỐI KHÔNG TỰ ĐOÁN MÒ.**

---

### 🗺️ BẢN ĐỒ TRA CỨU ĐẶC TẢ CHI TIẾT DÀNH CHO AI CODING (SPEC LOOKUP MATRIX)

#### Nhóm 1: Business Rules Cốt Lõi, Kiến Trúc Tổng Thể & Hướng Dẫn Giao Diện
| Nội Dung / Phân Hệ | File Đặc Tả Chính Thức trong `specs/md/` | Mô Tả Chi Tiết & Giá Trị Sử Dụng Cho AI Coding |
| :--- | :--- | :--- |
| **Business Rules & State Machine Toàn Diện** *(BẮT BUỘC ĐỌC)* | [`specs/md/FS_SPECIFICATIONS_SUMMARY.md`](file:///home/baudui/Projects/automation-ui/specs/md/FS_SPECIFICATIONS_SUMMARY.md) | **Tài liệu cốt lõi nhất (993 dòng)**: Phân tích chuyên sâu toàn bộ Business Rules của hệ thống, máy trạng thái giao dịch (State Machine), logic biên tuổi 16, công thức tính toán tài chính, danh mục thông báo lỗi chuẩn (`MSG-0801` đến `MSG-0809`, `MSG-0001` đến `MSG-0003`). |
| **Quy Chuẩn UI/UX & Form Validation** *(BẮT BUỘC ĐỌC TRƯỚC KHI VIẾT PAGE OBJECT)* | [`specs/md/EAFAMS_UI_SPECIFICATION_AND_INTERACTION_GUIDE.md`](file:///home/baudui/Projects/automation-ui/specs/md/EAFAMS_UI_SPECIFICATION_AND_INTERACTION_GUIDE.md) | Đặc tả hành vi giao diện: quy tắc validation form, cơ chế che mờ CCCD/NRIC, định dạng tiền tệ SGD, các trạng thái button/loading, layout các màn hình. |
| **Nhật Ký 31 Quyết Định Nghiệp Vụ Client** | [`specs/md/MEETINGS_AND_DECISIONS_SUMMARY.md`](file:///home/baudui/Projects/automation-ui/specs/md/MEETINGS_AND_DECISIONS_SUMMARY.md) | **31 Quyết định nghiệp vụ chính thức (`D-01` đến `D-31`)** giữa PO, BA và Client: chốt cơ chế On-demand API Sync thay vì quét đêm (D-31), luồng Split Payment, quy tắc hoàn tiền, xử lý đơn FAS. |
| **Yêu Cầu Tổng Thể & Backlog** | [`specs/md/REQUIREMENTS_AND_BACKLOG_SUMMARY.md`](file:///home/baudui/Projects/automation-ui/specs/md/REQUIREMENTS_AND_BACKLOG_SUMMARY.md) | Tóm tắt toàn bộ yêu cầu dự án, user stories, phân chia sprint và các mốc bàn giao. |
| **Giải Pháp Kiến Trúc Mức Cao** | [`specs/md/[Agile] High-level Solution.md`](file:///home/baudui/Projects/automation-ui/specs/md/%5BAgile%5D%20High-level%20Solution.md) | Kiến trúc tổng thể hệ thống EAFAMS, phân tách Admin Portal (F1–F7) và e-Service Parent Portal (F8–F10). |
| **Product Backlog Chi Tiết** | [`specs/md/Product Backlog V2.md`](file:///home/baudui/Projects/automation-ui/specs/md/Product%20Backlog%20V2.md) | Danh sách User Stories từ `US-001` đến `US-058` kèm Acceptance Criteria, độ ưu tiên và dependencies. |

---

#### Nhóm 2: Acceptance Criteria (AC Đầy Đủ) & Test Cases
| Module / Phân Hệ Kiểm Thử | File Đặc Tả Acceptance Criteria & Test Cases trong `specs/md/` | Số Lượng TCs & Nội Dung Kiểm Thử Chi Tiết |
| :--- | :--- | :--- |
| **R9 (Split Payment) & R10 (FAS AI Auto-fill) AC Chuẩn Gherkin** | [`specs/md/EAFAMS_SPLIT_PAYMENT_AND_AI_FAS_TEST_CASES_AND_AC.md`](file:///home/baudui/Projects/automation-ui/specs/md/EAFAMS_SPLIT_PAYMENT_AND_AI_FAS_TEST_CASES_AND_AC.md) | **Acceptance Criteria chuẩn Enterprise Banking**: `AC-SP-01` đến `AC-SP-08` (Split Payment) và `AC-FAS-01` đến `AC-FAS-08` (FAS AI Auto-fill), ma trận test cases Gherkin BDD chi tiết. |
| **R1: Education Account Lifecycle & Closure** | [`specs/md/Test Cases/TC_R1_Education_Account_Lifecycle.md`](file:///home/baudui/Projects/automation-ui/specs/md/Test%20Cases/TC_R1_Education_Account_Lifecycle.md) | **73 Test Cases**: Tự động mở tài khoản khi 7 tuổi, đóng khi 16 tuổi, thừa kế số dư, khóa ledger, chống trùng lặp. |
| **R3: School, Student & Fee Management** | [`specs/md/Test Cases/TC_R3_School_Student_Fee_Management.md`](file:///home/baudui/Projects/automation-ui/specs/md/Test%20Cases/TC_R3_School_Student_Fee_Management.md) | **105 Test Cases**: Thiết lập trường học, khối lớp, danh mục biểu phí, định giá, phát hành hóa đơn học phí. |
| **R8: Parent Portal & SingPass Profile** | [`specs/md/Test Cases/TC_R8_Parent_Portal_SingPass_Profile.md`](file:///home/baudui/Projects/automation-ui/specs/md/Test%20Cases/TC_R8_Parent_Portal_SingPass_Profile.md) | **125 Test Cases**: Đăng nhập SingPass, dashboard phụ huynh, liên kết con cái, xem số dư EA, cập nhật My Details, audit log. |
| **R9: Outstanding Fees & Payment Engine** | [`specs/md/Test Cases/TC_R9_Outstanding_Fees_and_Payment.md`](file:///home/baudui/Projects/automation-ui/specs/md/Test%20Cases/TC_R9_Outstanding_Fees_and_Payment.md) | **162 Test Cases**: Truy cập hóa đơn, thanh toán EA, thanh toán Online Sandbox, Split Payment, Idempotency, tự động hoàn tiền khi lỗi. |
| **Sprint 1 Defect Master Log (Known Bugs)** | [`specs/md/Test Cases/DEFECTS_Sprint_1_Master.md`](file:///home/baudui/Projects/automation-ui/specs/md/Test%20Cases/DEFECTS_Sprint_1_Master.md) | **14 Lỗi đã ghi nhận (BUG-R8-001 đến BUG-R8-005, BUG-R9-001 đến BUG-R9-003...)**: Kèm các bước tái hiện, kết quả mong đợi và cú pháp `@pytest.mark.xfail(strict=True)`. |
| **Master Workbook Test Cases Raw Table** | [`specs/md/Test Cases/Test Cases + Defect sprint 1.md`](file:///home/baudui/Projects/automation-ui/specs/md/Test%20Cases/Test%20Cases%20%2B%20Defect%20sprint%201.md) | **Toàn bộ 465 Test Cases** xuất trực tiếp từ file Google Sheets của Sprint 1. |

---

#### Nhóm 3: Tài Liệu Đặc Tả Từng Phân Hệ Chức Năng (Agile FS Documents)
| Mã FS | File Đặc Tả trong `specs/md/FS document/` | Phạm Vi Chức Năng & Quy Tắc Nghiệp Vụ |
| :--- | :--- | :--- |
| **FS-01** | [`specs/md/FS document/FS-01_Education_Account_Lifecycle.md`](file:///home/baudui/Projects/automation-ui/specs/md/FS%20document/FS-01_Education_Account_Lifecycle.md) | Quản lý vòng đời tài khoản giáo dục (mở khi 7 tuổi, đóng khi 16 tuổi, thừa kế số dư, khóa ledger). |
| **FS-02** | [`specs/md/FS document/FS-02_Education_Account_TopUp.md`](file:///home/baudui/Projects/automation-ui/specs/md/FS%20document/FS-02_Education_Account_TopUp.md) | Quản lý nạp tiền Top-up cá nhân và hàng loạt, ngân sách hàng năm. |
| **FS-03** | [`specs/md/FS document/FS-03_School_Student_Fee_Management.md`](file:///home/baudui/Projects/automation-ui/specs/md/FS%20document/FS-03_School_Student_Fee_Management.md) | Quản lý danh mục biểu phí trường học, cấu hình học phần, đợt phát hành hóa đơn. |
| **FS-04** | [`specs/md/FS document/FS-04_Financial_Assistance_Scheme_FAS.md`](file:///home/baudui/Projects/automation-ui/specs/md/FS%20document/FS-04_Financial_Assistance_Scheme_FAS.md) | Tiêu chí xét duyệt chính sách hỗ trợ tài chính FAS (MOEFAS vs SBFAS, công thức PCI/GHI). |
| **FS-05** | [`specs/md/FS document/FS-05_Hardcopy_Applications_Offline.md`](file:///home/baudui/Projects/automation-ui/specs/md/FS%20document/FS-05_Hardcopy_Applications_Offline.md) | Quy trình tiếp nhận và xử lý đơn giấy FAS ngoại tuyến, scan tài liệu và thẩm định thủ công. |
| **FS-06** | [`specs/md/FS document/FS-06_FAS_Budget_and_Statistics.md`](file:///home/baudui/Projects/automation-ui/specs/md/FS%20document/FS-06_FAS_Budget_and_Statistics.md) | Quản lý, cảnh báo soft-limit và thống kê phân bổ ngân sách FAS cho các trường học. |
| **FS-07** | [`specs/md/FS document/FS-07_User_Simulation_ViewAs.md`](file:///home/baudui/Projects/automation-ui/specs/md/FS%20document/FS-07_User_Simulation_ViewAs.md) | Tính năng giả lập người dùng (View As) của Admin/Clerk để kiểm tra góc nhìn của phụ huynh. |
| **FS-08** | [`specs/md/FS document/FS-08_Parent_Portal_SingPass_Profile.md`](file:///home/baudui/Projects/automation-ui/specs/md/FS%20document/FS-08_Parent_Portal_SingPass_Profile.md) | Cổng phụ huynh: đăng nhập SingPass, xem số dư tài khoản con, cập nhật thông tin cá nhân. |
| **FS-09** | [`specs/md/FS document/FS-09_Outstanding_Fees_and_Payment.md`](file:///home/baudui/Projects/automation-ui/specs/md/FS%20document/FS-09_Outstanding_Fees_and_Payment.md) | Tra cứu nợ học phí, thanh toán EA, thanh toán Online (eNETS/PayNow), thanh toán tách (Split Payment), tự động hoàn tiền khi giao dịch lỗi. |
| **FS-10** | [`specs/md/FS document/FS-10_FAS_Family_Application_Portal.md`](file:///home/baudui/Projects/automation-ui/specs/md/FS%20document/FS-10_FAS_Family_Application_Portal.md) | Cổng nộp đơn FAS trực tuyến cho hộ gia đình, tự động điền form (AI Auto-fill). |
| **Tổng Hợp**| [`specs/md/FS document/Tổng hợp FS.md`](file:///home/baudui/Projects/automation-ui/specs/md/FS%20document/T%E1%BB%95ng%20h%E1%BB%A3p%20FS.md) | Bản gộp tổng thể toàn bộ các phân hệ FS (1.97 MB). |

---

#### Nhóm 4: Biên Bản Cuộc Họp, Phỏng Vấn & Đối Soát Khoảng Trống (Gap Audit)
| Nội Dung | File Đặc Tả trong `specs/md/` | Mục Đích Đối Soát Cho AI Coding |
| :--- | :--- | :--- |
| **Biên Bản Cuộc Họp Mới Nhất (19/10/2026)** | [`specs/md/Documentation/Meeting Transcript - 19 Oct 2026.md`](file:///home/baudui/Projects/automation-ui/specs/md/Documentation/Meeting%20Transcript%20-%2019%20Oct%202026.md) | Biên bản họp giải quyết các mâu thuẫn nghiệp vụ mới nhất: workflow OCR, soft-limit, simulation mode. |
| **Báo Cáo Đối Soát Khoảng Trống FSD vs Tender** | [`specs/md/FSD_ALIGNMENT_AND_GAP_AUDIT_REPORT.md`](file:///home/baudui/Projects/automation-ui/specs/md/FSD_ALIGNMENT_AND_GAP_AUDIT_REPORT.md) | Đối soát toàn diện các điểm thiếu sót, mơ hồ giữa hồ sơ thầu và tài liệu FSD. |
| **Báo Cáo Đối Soát Khoảng Trống Phân Hệ R3** | [`specs/md/FSD_R3_GAP_AUDIT_REPORT.md`](file:///home/baudui/Projects/automation-ui/specs/md/FSD_R3_GAP_AUDIT_REPORT.md) | Đối soát gap chi tiết riêng cho phân hệ Quản lý Biểu phí R3. |
| **Từ Điển Thuật Ngữ Chuẩn GovTech & Agile** | [`specs/md/Documentation/Agile Glossary.md`](file:///home/baudui/Projects/automation-ui/specs/md/Documentation/Agile%20Glossary.md) | Bảng tra cứu thuật ngữ: EA, MOEFAS, SBFAS, PCI, GHI, Tier, NRIC, SingPass... |

---

#### Nhóm 5: File Gốc Word & Excel từ Google Drive (`specs/raw/`)
Toàn bộ file gốc nhị phân chưa qua xử lý được lưu trữ nguyên vẹn tại **[`specs/raw/`](file:///home/baudui/Projects/automation-ui/specs/raw/)**:
- `specs/raw/Test Cases + Defect sprint 1.xlsx`: Bảng tính Excel gốc gồm toàn bộ 465 test cases và 14 defect logs.
- `specs/raw/Product Backlog V2.xlsm`: Bảng tính Excel gốc Product Backlog.
- `specs/raw/FS document/*.docx`: Các file Microsoft Word gốc của từng phân hệ FS.
- `specs/raw/Documentation/*.docx`: Các file Microsoft Word biên bản cuộc họp và phỏng vấn gốc.

---

#### Nhóm 6: Đặc Tả Thành Phần Chuẩn Hóa & Luồng Tích Hợp (`specs/component_specs/`) *(BẮT BUỘC TRA CỨU)*
Nguồn cung cấp **3 trụ cột thiết yếu** (Validation Rules, Functional Flow & Error Handling Catalog):
| Thư Mục / File | Loại Đặc Tả Cung Cấp | Giá Trị Cốt Lõi Cho AI Automation Coding |
| :--- | :--- | :--- |
| `specs/component_specs/<module>/atomic/*.md` | **Validation Rules & Field Matrix** | Ma trận 12 lớp kiểm thử chi tiết từng ô input: Empty, Whitespace, Min/Max BVA biên (149/150/151), regex định dạng (SĐT 8 số đầu 6/8/9, email RFC, postal code 6 số), XSS vectors và BSK Live DOM selectors. |
| `specs/component_specs/<module>/integration/*.md` | **Functional Flow & State Machine** | Luồng tương tác liên component, máy chuyển trạng thái (State Machine): View $\leftrightarrow$ Edit dirty $\leftrightarrow$ Modal confirm $\leftrightarrow$ Toast, logic khóa form khi con $\ge 16$ tuổi. |
| `specs/component_specs/<module>/README.md` | **Error Catalog & Visual Feedback** | Bảng tra cứu toàn bộ mã lỗi chuẩn (`MSG-0001` đến `MSG-0809`), visual feedback tương ứng (`aria-invalid="true"`, viền đỏ, alert modal, toast timing). |

#### Nhóm 7: UI/BSK Live DOM Inventory (`specs/ui_bsk/`) *(BẮT BUỘC TRA TRƯỚC KHI RECON LẠI)*

| Thư Mục | Phạm Vi | Cách Dùng |
| :--- | :--- | :--- |
| `specs/ui_bsk/localhost-5173/` | Admin Portal: login, academic/users, finance, fee, FAS | Lấy route, control inventory, verified selector và raw DOM inspections. |
| `specs/ui_bsk/localhost-5174/` | Parent Portal: Singpass, dashboard, profile, transaction, payment, FAS application | Lấy route, state UI, dynamic-card identifiers, modal/toast và verified selector. |

UI/BSK inventory là bằng chứng giao diện ở thời điểm recon, không tự tạo BR/AC. Khi inventory mâu thuẫn với DOM hiện tại, đánh dấu stale, recon lại và cập nhật `specs/ui_bsk/`; script/công cụ vẫn nằm trong `tools/`.

---

## 7. Modular Component Architecture & File Length Governance (Chuẩn Phân Rã & Giới Hạn < 250 Dòng)

> [!IMPORTANT]
> **QUY CHUẨN THIẾT KẾ MÃ NGUỒN AUTOMATION - CẤM TUYỆT ĐỐI FILE DÀI > 250 DÒNG**:
> Toàn bộ file Python trong dự án được tổ chức nghiêm ngặt thành 2 nhóm với ranh giới rõ ràng. Bất kỳ file nào chạm ngưỡng 250 dòng BẮT BUỘC phải bóc tách ngay theo các mẫu kiến trúc dưới đây.

### 1. Phân chia 2 Nhóm File Trong Toàn Bộ Dự Án
```text
┌───────────────────────────────────────────────────────────────────────────────────┐
│                    2 TRỤ CỘT KIẾN TRÚC AUTOMATION TESTING                         │
├─────────────────────────────────────────┬─────────────────────────────────────────┤
│    NHÓM 1: TẦNG NGHIỆP VỤ & TEST        │     NHÓM 2: HẠ TẦNG & CÔNG CỤ           │
│         (Business & Test Layer)         │       (Platform & Tooling Layer)        │
├─────────────────────────────────────────┼─────────────────────────────────────────┤
│ • pages/ (Page Object Orchestrators)    │ • core/ (Engine, Hooks, Plugins)        │
│ • pages/<module>/locators.py (Selectors)│ • tools/ (Recon DOM, Báo cáo generator) │
│ • pages/<module>/components/ (Sub-steps)│ • reporting/ (Charts, Builders)         │
│ • tests/<module>/ (Sliced Test Suites)  │ • data/ & specs/ (Pure JSON/YAML Data)  │
│ • data/<module>/ (Input Datasets JSON)  │                                         │
└─────────────────────────────────────────┴─────────────────────────────────────────┘
```

---

### 2. Chuẩn Phân Rã Page Objects (Mô hình Lego Component POM)
CẤM viết 1 file Page Object dài ôm toàn bộ mọi màn hình (God Class). Khi một màn hình có từ 2 bước trở lên hoặc vượt quá 200 dòng, bắt buộc phân rã:
```text
pages/<module>/
├── locators.py                     # [Tối đa 100 dòng] Tập trung toàn bộ biến chuỗi selector CSS / XPath
├── components/                     # Thư mục chứa từng bước hoặc từng modal riêng biệt
│   ├── step1_<feature>.py          # [Tối đa 150 dòng] Chỉ chứa hàm thao tác của Step 1
│   ├── step2_<feature>.py          # [Tối đa 150 dòng] Chỉ chứa hàm thao tác của Step 2
│   └── <modal_or_dialog>.py        # [Tối đa 100 dòng] Chỉ xử lý hộp thoại / popup riêng biệt
└── <feature>_page.py               # [Tối đa 250 dòng] Page Orchestrator: khởi tạo các sub-components
                                    # và cung cấp phương thức ủy quyền (delegation) để 100% test cũ không lỗi.
```

**Mẫu Ủy Quyền (Delegation Pattern) trên Page Orchestrator**:
```python
class MyFeaturePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.step1 = Step1Component(page)
        self.step2 = Step2Component(page)

    # Delegation methods để giữ tương thích ngược 100% với code test cũ:
    def select_item(self, item_id: str):
        return self.step1.select_item(item_id)
```

---

### 3. Chuẩn Phân Rã Test Suites (Per-Field Slicing & Data-Driven)
CẤM gộp 30 ca test của toàn bộ màn hình vào 1 file 600 dòng. Bắt buộc:
1. **Chia nhỏ file test theo phạm vi ô nhập liệu hoặc nhóm chức năng**:
   - `test_atomic_<field_name_1>.py` (< 200 dòng).
   - `test_atomic_<field_name_2>.py` (< 200 dòng).
   - `test_atomic_security_nfr.py` (< 150 dòng).
   - `test_integration_<flow_name>.py` (< 200 dòng).
2. **Áp dụng Data-Driven Testing (`@pytest.mark.parametrize`)**:
   - Tách toàn bộ ma trận test input (BVA, regex, XSS) sang `data/<module>/<module>_data.json`.
   - Một hàm test 20 dòng kết hợp `@pytest.mark.parametrize` có thể giải quyết 15–20 ca kiểm thử thay vì copy-paste 20 hàm riêng lẻ.

---

### 4. Chuẩn Phân Rã Tools & Scripts Báo Cáo (Decouple Data from Logic)
- **Tuyệt đối cấm**: Hardcode danh sách hàng trăm test case, từ điển cấu hình, hoặc bảng màu OpenPyXL/CSS trực tiếp trong code Python (`tools/build_*.py`).
- **Quy chuẩn**:
  - Dữ liệu đưa về: `specs/` hoặc `data/*.json` / `.yaml`.
  - Hàm định dạng style đưa về module dùng chung: `tools/utils/` (< 100 dòng).
  - File script generator chỉ chứa logic đọc template và ghi file (< 150 dòng).

---

### 5. Chuẩn Tốc Độ Thực Thi & Tiết Kiệm RAM (Lean Browser & Concurrency)
- **Concurrency**: Cấu hình song song `-n 3` trong `pytest.ini` (3 workers là chuẩn vàng tối ưu cho 7.5GB RAM).
- **Chromium Ultra-Lean Flags**: Bắt buộc duy trì trong `core/pytest_plugins/browser_engine.py`:
  - `--disable-gpu`: Tắt GPU render trong môi trường headless, tiết kiệm 100–150MB RAM/worker.
  - `--disable-software-rasterizer`: Tiết kiệm tải CPU.
  - `--renderer-process-limit=2`: Giới hạn sub-process của Chromium.
  - `--disk-cache-size=1` & `--media-cache-size=1`: Triệt tiêu bộ nhớ đệm cache phình to.
  - `--disable-features=Translate,BackForwardCache,AcceptCHFrame,MediaRouter,OptimizationHints`.
  - `--js-flags=--max-old-space-size=256`: Giới hạn heap V8.





