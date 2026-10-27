# AGENTS.md - UI Automation Architecture & Master Constitution

## 1. Architectural Philosophy & Repository Structure
This repository implements an Enterprise UI Automation Framework using **Playwright** and **pytest**.
The architecture is designed for high reliability, zero flakiness, minimal boilerplate, and strict verification gates.

```text
automation-ui/
├── 1_Nghiep_Vu_va_Specs/       # 📋 Nhóm 1: Nghiệp vụ, FS Specs, Test Cases & UAT
│   ├── copy/                   # ⛔ [READ-ONLY] Company codebase - Nghiêm cấm chỉnh sửa
│   ├── specs/                  # Đặc tả hệ thống (component_specs, ui_bsk, md, validation_rules)
│   ├── testcases/              # Kho Test Cases Single Source of Truth (TC_*.md, TC_*.xlsx)
│   ├── test_specs/             # Lean Markdown Test Specs (4-tier architecture)
│   └── uat/                    # Kịch bản UAT phân rã theo phân hệ (r01, r02, r08, master)
├── 2_Code_Automation/          # ⚙️ Nhóm 2: Mã nguồn kiểm thử tự động (Playwright + Pytest)
│   ├── components/             # Reusable UI widgets
│   ├── core/                   # Evidence annotator, SketchVLM, custom hooks
│   ├── data/                   # Parameterized datasets & fixtures JSON
│   ├── pages/                  # Modular Page Objects Lego (< 200 dòng, Zero Assertions)
│   ├── tests/                  # Pytest test suites (test_atomic_*.py, test_integration_*.py)
│   ├── tools/                  # Recon BSK, break_it, environment scripts
│   ├── conftest.py             # Fixtures & Pytest hooks
│   ├── pytest.ini              # Pytest configuration
│   ├── requirements.txt        # Python dependencies
│   ├── run_tests.py            # Test execution orchestrator
│   └── md_runner.py            # Markdown test runner
├── 3_Bao_Cao_va_Ket_Qua/       # 📊 Nhóm 3: Báo cáo, Kết quả thực thi & Tài liệu kỹ thuật
│   ├── archive/                # Historical deliverables
│   ├── docs/                   # Framework docs, diagrams, defects
│   ├── generate_enterprise_report.py
│   ├── generate_report.py
│   ├── reporting/              # Offline ExtentReports generator
│   └── reports/                # Báo cáo kết quả UAT & technical test reports
├── .agent/                     # 📜 Intent router & modular rules
│   ├── README.md               # Precedence, path contract & maintenance checklist
│   └── rules/
│       ├── 01-two-stage-workflow.md         # Design TCs -> AI Coding & 5 Pillars
│       ├── 02-field-test-matrix.md          # Ma trận 12 lớp & 8 nhóm controls
│       ├── 03-failure-triage-adversarial.md # 9-Tier Failure & disciplined break-it
│       └── 04-automation-coding-standards.md# POM, evidence & spec lookup
├── AGENTS.md                   # 📜 Master Constitution & Architecture Guidelines
├── README.md                   # 📖 Main Project Documentation
└── .gitignore                  # 🔒 Git ignore rules
```

### 1.1 Kiến Trúc 3 Nhóm Vật Lý Thống Nhất (Unified 3-Group Architecture)

> [!IMPORTANT]
> Cấu trúc repository được phân bổ trực tiếp và vật lý thành **3 nhóm thư mục lớn**, đảm bảo tính thẩm mỹ, trực quan và đồng bộ 100% giữa giao diện GitHub và File Manager trên máy cục bộ (Nautilus).

| Thư mục nhóm | Phạm vi sở hữu vật lý | Mục đích & Quy tắc |
| :--- | :--- | :--- |
| `1_Nghiep_Vu_va_Specs/` | `copy/`, `specs/`, `testcases/`, `test_specs/`, `uat/` | Nghiệp vụ, đặc tả phân hệ, thiết kế test case và UAT. `copy/` vẫn read-only tuyệt đối. |
| `2_Code_Automation/` | `components/`, `core/`, `data/`, `pages/`, `tests/`, `tools/`, runners & configs | Toàn bộ mã nguồn automation, POMs, fixtures, pytest config và công cụ thực thi. |
| `3_Bao_Cao_va_Ket_Qua/` | `archive/`, `docs/`, `reporting/`, `reports/`, report generators | Toàn bộ báo cáo HTML/Excel, evidence runs, defect logs và tài liệu kỹ thuật. |

- **Thư mục gốc (Root)**: Chỉ hiển thị đúng 3 thư mục nhóm lớn cùng `AGENTS.md`, `README.md` và `.gitignore`. Không để bất kỳ file hay thư mục rời rạc nào trôi nổi tại root.
- **Thực thi lệnh kiểm thử**: Có thể chạy từ thư mục gốc hoặc chuyển vào `2_Code_Automation/`:
  - Từ root: `.venv/bin/pytest 2_Code_Automation/tests/fs08/... -v`
  - Từ nhóm 2: `cd 2_Code_Automation && ../.venv/bin/pytest tests/fs08/... -v`

---

## 2. The 12 Golden Invariants (Master Constitution)
> [!IMPORTANT]
> **12 NGUYÊN TẮC BẤT BIẾN TUÂN THỦ 100% (VI PHẠM = TASK THẤT BẠI)**:
1. **Invariant 0 (Strict Read-Only Boundary for `copy/`)**: Thư mục `copy/` là mã nguồn sản phẩm của công ty, **TUYỆT ĐỐI KHÔNG ĐƯỢC CHỈNH SỬA, THÊM, BỚT, FORMAT, DI CHUYỂN HOẶC XÓA BẤT KỲ FILE NÀO TRONG `copy/`**. Shortcut `1_Nghiep_Vu_va_Specs/copy` cũng trỏ tới cùng vùng read-only này. Phạm vi làm việc nằm ở automation testing (`specs/`, `testcases/`, `test_specs/`, `uat/`, `pages/`, `components/`, `core/`, `data/`, `tests/`, `tools/`, `reporting/`, `reports/`, `docs/`).
2. **Invariant 1 (Zero Assertions in Page Objects)**: Page Objects (`pages/`) và Components (`components/`) CHỈ tương tác UI và lấy snapshot state. **CẤM TUYỆT ĐỐI đưa lệnh `assert` hoặc validation logic vào Page Objects**. Mọi assertion phải nằm trong `tests/`.
3. **Invariant 2 (Zero Hardcoded Test Data)**: Không hardcode chuỗi dữ liệu trong code test. Toàn bộ input, biên BVA, XSS vector phải lưu tại `data/<fs_module>/<fs_module>_data.json` hoặc fixtures độc lập và deep-copy trước khi dùng (`copy.deepcopy(...)`).
4. **Invariant 3 (Test Case Traceability)**: Mọi test function phải bắt đầu bằng `test_tc_<scenario_id>_...` và truy vết 1-1 về User Story, AC ID (`R8-ACxx`), hoặc Business Rule ID (`BR-xx`).
5. **Invariant 4 (Zero `time.sleep()`)**: Tuyệt đối không dùng `time.sleep()`. Chỉ sử dụng auto-waiting của Playwright (`wait_for_selector`, `expect(locator)`, `wait_for_load_state`).
6. **Invariant 5 (Verification-First & Hook-Based Classification)**: Mọi bug sản phẩm phải được bắt qua `Exceptor.expect_bug_if_accepted(...)` hoặc `@pytest.mark.xfail(strict=True)`. Lỗi hạ tầng (timeout, crash) được hook `pytest_runtest_makereport` tự phân loại trong `conftest.py`.
7. **Invariant 6 (ZERO ASSUMPTIONS - BSK Live DOM First)**: Tuyệt đối không tự suy diễn selector, message lỗi, hay rule nghiệp vụ. Bắt buộc đối chiếu kho recon đã thu thập tại `specs/ui_bsk/`; nếu màn hình/phiên bản chưa có hoặc đã stale thì chạy `python3 tools/recon_bsk.py --url <URL>` để nhặt selector từ DOM sống thật trước khi viết Page Object. Kết quả recon lưu vào `specs/ui_bsk/`, không lưu trong `tools/`.
8. **Invariant 7 (Mandatory 5-Pillar Test Inputs & Full-Coverage Enforcement - Bộ Ngũ Nguyên Liệu & Chống Sinh Thiếu Test Case)**:
   - Trước khi thiết kế test case hoặc code automation, BẮT BUỘC phải đối soát và thu thập đủ **5 Thông Tin Cốt Lõi**:
     - `[1] Business Rules (BR)`: Ràng buộc nghiệp vụ, tuổi, phân quyền (`specs/md/FS document/`, `MEETINGS_AND_DECISIONS`).
     - `[2] Acceptance Criteria (AC)`: Tiêu chí nghiệm thu chuẩn Gherkin (`specs/md/Test Cases/`, `Product Backlog V2.md`).
     - `[3] Validation Rules`: Ma trận 12 lớp, biên BVA, regex, lengths (`specs/component_specs/<module>/atomic/*.md`).
     - `[4] Functional Flow`: Luồng tương tác, State Machine, step-by-step, modal/toast (`specs/component_specs/<module>/integration/*.md`).
     - `[5] Error Handling`: Catalog mã thông báo (`MSG-xxxx`), visual feedback viền đỏ `aria-invalid` (`specs/component_specs/<module>/README.md`).
   - **Chống Sinh Thiếu Test Case (Zero-Shallow Testing Mandate)**:
     - **CẤM TUYỆT ĐỐI** tư duy kiểm thử hời hợt (chỉ sinh 10-20 test cases happy-path rồi dừng). Bất kỳ form hay màn hình nghiệp vụ nào cũng phải áp dụng triệt để ma trận 12 lớp cho **TỪNG Ô NHẬP LIỆU** và **CÁC THẺ ĐỘNG (Dynamic Cards)**.
     - Với mỗi ô của ma trận, ghi rõ `Applicable` hoặc `N/A` kèm lý do dựa trên đặc tả; không sinh ca vô nghĩa cho lớp không áp dụng. Số lượng TC chỉ là ngưỡng phụ, không thay thế việc chứng minh độ phủ theo từng field/rule.
     - **Ngưỡng Bao Phủ Tối Thiểu (Minimum Coverage Gates)**:
       * Form đơn giản (1-3 fields): Tối thiểu $\ge 15 - 25$ TCs.
       * Form nghiệp vụ chuẩn (4-8 fields): Tối thiểu $\ge 30 - 45$ TCs.
       * Form phức tạp / Dynamic Sub-forms ($\ge 9$ fields như FAS, Hồ sơ, Đăng ký): Tối thiểu $\ge 50 - 70$ TCs.
     - **4 Nhóm Ràng Buộc Bắt Buộc Không Được Bỏ Sót**:
       1. *Kiểm tra chéo 3 chiều (Cross-field Validation)*: Trùng lặp NRIC/ID giữa các đối tượng (cha-con, anh-em, người thân), ràng buộc phụ thuộc (nếu chọn có thu nhập thì phải nhập số tiền).
       2. *Biên BVA đầy đủ (Boundary Value Analysis)*: Biên hợp lệ trong khoảng, biên chạm ngưỡng dưới/trên, biên từ chối ngoài khoảng (ví dụ tuổi 7-16 thì phải test đủ 6, 7, 10, 16, 17 và ngày sinh tương lai).
       3. *Vòng đời thẻ động & State Machine*: Thêm thẻ, xóa thẻ, re-index dữ liệu, nút Reset trắng form ("Start a new application").
       4. *Khả năng chịu lỗi (Error Resilience & UI Health)*: Giả lập HTTP 500 bảo toàn dữ liệu form, phản hồi viền đỏ `aria-invalid="true"`, 0 rò rỉ mã dịch `features.*`, 0 lỗi uncaught console.
9. **Invariant 8 (High-Speed & RAM-Optimized Lean Media Execution - Tối Ưu Tốc Độ & RAM)**:
   - **Concurrency chuẩn**: Chạy song song `-n 3` (3 workers là tỷ lệ vàng tối ưu cho 7.5GB RAM, tăng tốc độ 3-4x mà không gây quá tải OOM hoặc swap thrashing).
   - **Chính sách Media tinh gọn (Tắt Video Mặc Định)**: Cấu hình mặc định `--video=off` trong `pytest.ini` để triệt tiêu hoàn toàn CPU mã hóa WebM nền và giải phóng > 50% RAM. Chỉ bật lại `--video=retain-on-failure` khi người dùng yêu cầu điều tra defect trực quan sâu.
   - **Chuẩn Bằng Chứng Hình Ảnh Đa Bước & Kết Quả Thực Tế Có Highlight (Step Actions & Highlighted Actual Result)**:
     * *Ảnh các bước thao tác (`screenshots/<test_slug>/step_X_<action>.png`)*: Chụp tự động ở mỗi bước thao tác hoặc theo `with self.step(...)`, tự động highlight ô nhập/nút bấm với viền xanh/cam và smart badge hiển thị nội dung nhập liệu (vd: `Input: "..."` hoặc `Click: [Nút]`).
     * *Ảnh kết quả thực tế (`screenshots/<test_slug>/actual_result.png`)*: Chụp tại bước kiểm chứng assertions/teardown, tự động highlight vùng Actual Result (thông báo lỗi/thành công, badge, toast, trạng thái form) bằng viền xanh lá (Pass) hoặc đỏ (Defect/Error) kèm badge `Actual Result: ...`.
     * File Excel bằng chứng (`TEST_EXECUTION_EVIDENCE_*.xlsx`) liên kết trực tiếp tới `📷 Actual Result (+X steps)`.
   - **Triệt tiêu nghẽn Hang 30s & Setup Chậm**: Dùng `wait_until="domcontentloaded"`, không dùng `wait_for_timeout` cứng; tuyệt đối không dùng `page.click()` trần trụi với các nút hủy/modal đóng khi form có khả năng đã ở View Mode hoặc đã submit. Luôn bọc kiểm tra `if self.is_visible(selector, timeout=2000)` hoặc timeout ngắn để tránh lãng phí 30 giây của Playwright.
   - **Mocking chính xác & Unroute**: Mock đúng regex endpoint backend (ví dụ profile mutation là `/iam/v1/parent/update/profile`, không dùng endpoint giả định); luôn gọi `page.unroute_all()` sau khi kiểm thử xong.
   - **Cô lập nhiều tab (Multi-tab)**: Vì `sessionStorage` độc lập giữa các tab, khi mở `new_page()` bắt buộc inject auth storage (ví dụ `edusave.parent-auth.user`) vào tab mới trước khi điều hướng.
10. **Invariant 9 (Strict File Length & Modular Component Architecture - Giới hạn < 250 dòng & Phân Rã Modular)**:
   - **Quy chuẩn kích thước file**: CẤM tuyệt đối mọi file `.py` mới hoặc refactored vượt quá 250 dòng. Mỗi file phải tuân thủ nguyên tắc Đơn nhiệm (Single Responsibility Principle).
   - **Page Object Lego Architecture**: CẤM viết "God Class" gom nhiều bước/màn hình vào 1 Page Object. Bắt buộc tách thành:
     * `pages/<module>/locators.py` (< 100 dòng): Tập trung toàn bộ selectors.
     * `pages/<module>/components/<step_or_subfeature>.py` (< 150 dòng): Mỗi component / step một file độc lập.
     * `pages/<module>/<page_name>_page.py` (< 200 dòng): Orchestrator điều phối, ủy quyền (delegate) vào sub-components để đảm bảo 100% backward compatibility cho existing tests.
   - **Test Suite Scope Slicing & Strict Subdirectory Placement**:
     * **CẤM TUYỆT ĐỐI** viết, sinh hoặc ném file test trôi nổi tự do tại thư mục gốc `tests/`.
     * Khi AI Coding chịu trách nhiệm cho ticket/module nào (`<fs_module>/<component>`), **BẮT BUỘC** phải đặt toàn bộ file test code vào đúng thư mục con: `tests/<fs_module>/<component_or_ticket>/` (ví dụ: `tests/fs08/fs08-uat007-contact-update/` hoặc `tests/f10/f10-fas-submission/`).
     * CẤM gom 20-30 test case của nhiều trường vào 1 file 600 dòng. Bắt buộc tách thành các test file độc lập theo từng ô input (`test_atomic_<field>.py` < 200 dòng) và luồng tích hợp (`test_integration_<flow>.py` < 250 dòng), áp dụng Data-Driven Testing (`@pytest.mark.parametrize`) nạp từ file `data/<module>/*.json`.
   - **Decouple Data & Generators**: CẤM nhồi nhét mảng dữ liệu test case hoặc styling OpenPyXL/HTML dài hàng nghìn dòng vào script Python trong `tools/`. Bắt buộc tách dữ liệu sang `specs/` hoặc `data/*.json/yaml`, file script generator chỉ giữ logic render < 150 dòng.
   - **Chromium Ultra-Lean Execution**: Luôn cấu hình `--disable-gpu`, `--disable-software-rasterizer`, `--renderer-process-limit=2`, `--disk-cache-size=1`, `--media-cache-size=1`, `--disable-features=Translate,BackForwardCache,...` và `--js-flags=--max-old-space-size=256` trong `core/pytest_plugins/browser_engine.py` để tiết kiệm RAM tối đa và duy trì RAM khả dụng > 1.8GB.
11. **Invariant 10 (Per-Module UAT Segregation & Unified Master Report - Phân Tầng UAT Theo Phân Hệ & Báo Cáo Thống Nhất)**:
   - **Cấu Trúc Bắt Buộc Theo Phân Hệ R**: Kịch bản kiểm thử UAT, tài liệu và báo cáo thuộc phân hệ nào (`r01`, `r02`, `r03`, `r08`, `r09`, `r10`...) thì **BẮT BUỘC** phải tạo folder riêng theo mã phân hệ đó (`uat/r<xx>/` và `reports/uat/r<xx>/`).
   - **CẤM TUYỆT ĐỐI**:
     1. Để file UAT trôi nổi tự do tại thư mục gốc `uat/` hay `reports/`.
     2. Đặt tên thư mục chứa dấu cách (whitespace) như `uat r8`, `r08 uat`. Bắt buộc dùng `kebab-case` hoặc snake_case chuẩn (ví dụ `uat/r08/`, `reports/uat/r08/`).
     3. Phân tán nhiều file evidence rời rạc cho cùng 1 phân hệ. Khi một phân hệ (như R8) chạy xong toàn bộ các sub-modules, **BẮT BUỘC** phải tổng hợp thành **1 File Thống Nhất Duy Nhất** (`TEST_EXECUTION_EVIDENCE_R<XX>_UAT_MASTER.xlsx` gom toàn bộ test cases trên 1 Tab duy nhất 20 cột kèm Steps Test) và 1 Master Dashboard HTML (`R<XX>_UAT_MASTER_DASHBOARD.html`).
12. **Invariant 11 (No Autonomous Test Execution - Cấm AI Tự Tiện Thực Thi Code Test Automation)**:
   - **Quy tắc tuyệt đối**: Khi viết/sinh mã Python automation testing (Page Objects, Fixtures, Test Suites), AI **TUYỆT ĐỐI KHÔNG ĐƯỢC TỰ Ý CHẠY/THỰC THI** code đó (không chạy `pytest`, `python run_tests.py`, script chạy test...).
   - **Quyền hạn rõ ràng**: Việc chạy test sẽ do **USER TOÀN QUYỀN TỰ THỰC THI**. AI chỉ đóng vai trò nghiên cứu, phân tích tài liệu đặc tả (`specs/`, `component_specs/`, `testcases/`, live DOM recon) và viết mã nguồn Python chuẩn mực, chính xác dựa trên tài liệu.
   - **Bàn giao chuẩn hóa**: Sau khi viết code xong, AI chỉ bàn giao mã nguồn, giải thích cấu trúc và cung cấp sẵn cú pháp câu lệnh tương ứng để User tự sao chép và thực thi.

---

## 3. The Intent-First Dynamic Router (BẢNG ĐỊNH TUYẾN BẮT BUỘC)
> [!NOTE]
> Để tránh quá tải token và mất ngữ cảnh, tài liệu chi tiết được module hóa tại `.agent/rules/`.
> **Khi nhận task thuộc phạm vi nào, AI Agent BẮT BUỘC gọi `read_file` đọc đúng file rule tương ứng TRƯỚC KHI hành động**:

| Nhiệm Vụ Của User / Intent | File Rule Bắt Buộc Phải Đọc Trước | Trọng Tâm Quy Chuẩn Cần Bám Theo |
| :--- | :--- | :--- |
| **Thiết kế Test Case / `/combo-qa` / Test màn hình mới** | [`.agent/rules/01-two-stage-workflow.md`](file:///.agent/rules/01-two-stage-workflow.md) | • Quy trình 2 giai đoạn: Giai đoạn 1 (BR-AC-UI) ➔ Giai đoạn 2 (AI Coding)<br>• Cấu trúc 5 phần file `.md` và xuất `TEST_EXECUTION_EVIDENCE_*.xlsx` 20 cột (1 Tab duy nhất, có cột Steps Test)<br>• Tránh 5 sai lầm phổ biến, phân rã Test Suite theo từng ô input |
| **Kiểm thử chi tiết ô Input / Validation / Form / PII** | [`.agent/rules/02-field-test-matrix.md`](file:///.agent/rules/02-field-test-matrix.md) | • Bộ ma trận 12 lớp kiểm thử chung (Empty, Whitespace, BVA, XSS...)<br>• Quy chuẩn chuyên biệt cho 8 nhóm Input (Số, Chữ, Email, Dropdown...)<br>• Thư viện đối chiếu nhanh Controls mở rộng (Dropdown, DatePicker, Checkbox, FileUpload, Vòng đời form, UI Health, PII)<br>• Chống rò rỉ translation key thô (`features.*`), viền đỏ `aria-invalid` |
| **Phân tích Test Fail (Triage) / Test Phá / Resilience** | [`.agent/rules/03-failure-triage-adversarial.md`](file:///.agent/rules/03-failure-triage-adversarial.md) | • 9 Tầng tiêu chí kích hoạt test FAIL (Runtime, Network, Visual, SLA...)<br>• Bảng Triage Matrix phân loại lỗi (Product vs Frontend vs Script)<br>• 6 Nhóm kỹ thuật "Phá có kỷ luật" (`@pytest.mark.break_it`) |
| **Viết Code Page Object / Test Suite / Tra cứu Specs** | [`.agent/rules/04-automation-coding-standards.md`](file:///.agent/rules/04-automation-coding-standards.md) | • Step tracking HUD bar & SketchVLM defect overlays trong video<br>• 11 Chỉ thị đặc biệt cho AI Coding Assistants<br>• Bản đồ tra cứu đặc tả FSD/AC/Decisions trong `specs/md/` |

---

## 3.1 Nơi Lưu Trữ Đặc Tả Cốt Lõi: Functional Flow, Error Handling & Component Specs (BẮT BUỘC ĐỌC ĐỂ LẤY THÔNG TIN TEST CASE)
> [!IMPORTANT]
> **Nguyên tắc "Đọc đúng nguồn - Lấy đủ thông tin"**:
> Khi thiết kế test case (`TC_*.md`, `TC_*.xlsx`) hoặc lập kịch bản automation, AI Agent **BẮT BUỘC** phải tra cứu các tài liệu đặc tả thành phần tại `specs/component_specs/<module>/` để lấy trọn vẹn **Functional Flow**, **Error Handling**, và **Ma trận Validation 12 lớp**. Tuyệt đối không tự suy diễn kịch bản hay mã lỗi.

### Cấu Trúc Lưu Trữ 5 Trụ Cột (5 Pillars) Trong Kho Specs:
1. **`[1] Business Rules (BR)`**: Nằm tại `specs/md/FS document/` và `specs/md/MEETINGS_AND_DECISIONS_SUMMARY.md` (31 quyết định `D-01` đến `D-31`).
2. **`[2] Acceptance Criteria (AC)`**: Nằm tại `specs/md/Test Cases/` và `specs/md/Product Backlog V2.md`.
3. **`[3] Validation Rules (Atomic)`**: Nằm tại `specs/component_specs/<module>/atomic/*.md` (Quy định chi tiết BVA, regex, empty, whitespace ASM-15 cho từng ô nhập).
4. **`[4] Functional Flow (Integration)`**: Nằm tại `specs/component_specs/<module>/integration/*.md` (Sơ đồ State Machine, quy tắc Pristine/Dirty, bẫy focus modal dialog, các luồng Given-When-Then).
5. **`[5] Error Handling (Error Catalog & Visual Feedback)`**: Nằm tại `specs/component_specs/<module>/README.md` (Bảng danh mục mã lỗi `MSG-xxxx`, quy chuẩn viền đỏ `aria-invalid`, alert modal, và toast).

### Bảng Tra Cứu Đặc Tả Mẫu Chuẩn Cho UAT-007 (Parent Contact Update — US-009 / FS08):
Khi nhận task kiểm thử, cập nhật hoặc đối soát test case cho **UAT-007**, đọc trực tiếp các file sau:

| Trụ Cột / Thành Phần | File Đặc Tả Bắt Buộc Đọc | Nội Dung Cung Cấp Cho Test Case |
| :--- | :--- | :--- |
| **Functional Flow & State Machine** | [`specs/component_specs/fs08/integration/parent_profile_update_flow.md`](file:///home/baudui/Projects/automation-ui/specs/component_specs/fs08/integration/parent_profile_update_flow.md) | • Luồng chuyển đổi 6 bước: View Mode ➔ Pristine ➔ Dirty ➔ Confirm Dialog ➔ Submitting ➔ Toast/View<br>• Hành vi nút Cancel (discard dirty state)<br>• Hành vi modal alertdialog và nút "Keep editing"<br>• Cơ chế chống double-click khi submit |
| **Error Handling & Catalog** | [`specs/component_specs/fs08/README.md`](file:///home/baudui/Projects/automation-ui/specs/component_specs/fs08/README.md#L37-L46) | • Danh mục mã lỗi: `MSG-0001` (trống bắt buộc), `MSG-0805` (sai SĐT SG), `MSG-0806` (sai email RFC 5322), `MSG-0807` (toast thành công), `MSG-0808` (lỗi API 500 / mạng)<br>• Quy định UI feedback: viền đỏ `border-red-500`, cờ `aria-invalid="true"`, modal giữ nguyên khi lỗi 500 |
| **Validation: Mobile Input** | [`specs/component_specs/fs08/atomic/mobile_input_component.md`](file:///home/baudui/Projects/automation-ui/specs/component_specs/fs08/atomic/mobile_input_component.md) | • Ma trận 12 lớp cho SĐT: 8 số bắt đầu bằng 6, 8, 9; tự động trim khoảng trắng (ASM-15); BVA 7/8/9 số; vector XSS/SQLi |
| **Validation: Email Input** | [`specs/component_specs/fs08/atomic/email_input_component.md`](file:///home/baudui/Projects/automation-ui/specs/component_specs/fs08/atomic/email_input_component.md) | • Ma trận 12 lớp cho Email: chuẩn RFC 5322; BVA độ dài 149/150/151 ký tự; trim khoảng trắng; chống rò rỉ key i18n |
| **Validation: Mailing Address** | [`specs/component_specs/fs08/atomic/mailing_address_component.md`](file:///home/baudui/Projects/automation-ui/specs/component_specs/fs08/atomic/mailing_address_component.md) | • Cụm địa chỉ: Street, Postal Code (6 số), Country là bắt buộc (`MSG-0001`); Block, Unit là tùy chọn |
| **Security: Singpass Identity** | [`specs/component_specs/fs08/atomic/singpass_identity_component.md`](file:///home/baudui/Projects/automation-ui/specs/component_specs/fs08/atomic/singpass_identity_component.md) | • Tính bất biến của Họ tên, NRIC/FIN, Địa chỉ thường trú (chỉ dùng thẻ `<dd>`, 0 thẻ `<input>`)<br>• Masking NRIC mặc định (`*****321B`) và nút Show/Hide không kích hoạt dirty state |
| **Master Test Case Matrix** | [`testcases/fs08/fs08-uat007-contact-update/TC_FS08_UAT007_Contact_Update.md`](file:///home/baudui/Projects/automation-ui/testcases/fs08/fs08-uat007-contact-update/TC_FS08_UAT007_Contact_Update.md) | • Single Source of Truth cho 10 TCs UAT-007 kèm ma trận 20 cột (có Steps Test), BSK live locators, và test data payload |
| **Automation Test Suites** | [`tests/fs08/fs08-uat007-contact-update/`](file:///home/baudui/Projects/automation-ui/tests/fs08/fs08-uat007-contact-update/) | • `test_atomic_contact_fields.py`: kiểm thử từng ô input<br>• `test_integration_contact_update.py`: kiểm thử flow, confirm dialog, API 500 error & E2E acceptance |

---

## 4. Mandatory Pre-Flight Protocol & Self-Verification Checklist
### Giao thức Pre-Flight (Trước khi viết Code / Test Case):
1. Xác định rõ Intent công việc từ yêu cầu của User.
2. Tra cứu Bảng Định Tuyến ở Mục 3 và đọc toàn bộ file rule tương ứng trong `.agent/rules/` trước khi hành động.
3. Xác nhận đang thao tác trên canonical path ở root, không ghi dữ liệu độc lập vào ba navigation groups.
4. Nếu làm việc với màn hình web: Chạy `python3 tools/recon_bsk.py --url <URL>` để lấy selectors sống thật.

### Giao thức sinh Test Case có thể kiểm chứng độ phủ (bắt buộc trước khi xuất `TC_*.md` / `TC_*.xlsx`):
1. **Lập sổ yêu cầu có nguồn**: Trích từng BR, AC, validation rule, bước flow/state và error/feedback thành một mục có ID, file nguồn, section và phiên bản nếu có. Đối chiếu các nguồn; chỗ thiếu hoặc mâu thuẫn đánh dấu `SPEC GAP` để xác nhận, không tự bịa rule, selector hay thông báo lỗi.
2. **Lập inventory từ DOM sống**: Ghi từng field, loại control, trạng thái required/optional, điều kiện hiển thị, quyền truy cập, nút thao tác và dynamic card. Đối chiếu hai chiều với sổ yêu cầu để phát hiện field thiếu rule hoặc rule chưa có vị trí kiểm thử trên UI.
3. **Dựng ma trận coverage trước khi gen ca**: Mỗi hàng là field/control hoặc BR/AC/transition; mỗi cột là lớp kiểm thử áp dụng. Bao gồm 12 lớp validation theo `.agent/rules/02-field-test-matrix.md`, BVA, cross-field/duplicate, nhánh điều kiện, vòng đời thẻ động, lỗi API/mạng, UI health và PII. Mỗi ô phải có TC ID, `N/A` kèm lý do, hoặc `SPEC GAP` nếu rule chưa xác định. Với BVA theo tuổi/ngày, dùng ngày sinh tương đối với ngày chạy hoặc đồng hồ test cố định; kiểm tra ngay dưới, đúng và ngay trên ngưỡng.
4. **Sinh ca theo tầng và rủi ro**: Tạo ca Atomic cho từng field, Integration cho tương tác nhiều component/API mock, UAT cho hành trình xuyên màn hình (và kiểm tra backend thật khi Expected Result kết luận về lưu trữ), Break-It cho hành vi đối kháng. Dùng pairwise để giảm tổ hợp độc lập, nhưng không thay thế biên BVA, BR/AC quan trọng, phân quyền hoặc các chuyển trạng thái bắt buộc.
5. **Ràng buộc oracle và traceability**: Mỗi TC có ID duy nhất, nguồn BR/AC/rule, precondition, dữ liệu từ fixture, bước thao tác, Expected Result quan sát/đo được và cách thu bằng chứng. Mỗi mệnh đề trong Expected Result phải có assertion hoặc evidence tương ứng khi chuyển sang code. Test dùng response mock chỉ được kết luận về hợp đồng và hành vi UI; kết luận "đã lưu vào backend/DB" cần ca UAT/API kiểm tra dữ liệu thật.
6. **Tách thiết kế khỏi kết quả chạy**: TC mới có `Execution Status = Not Run`; để trống `Actual Result`, timestamp và evidence cho đến khi thực thi. Chỉ ghi `Passed`/`Failed` từ một run xác định, có run ID, môi trường/build, thời điểm, kết quả quan sát và link evidence. Không dùng "As expected" làm Actual Result. Duy trì một bản testcase gốc cho mỗi phạm vi; bản Markdown/Excel và bản dẫn chiếu ở module khác phải đồng bộ từ nguồn đó.
7. **Coverage gate trước bàn giao**: 100% BR/AC trong phạm vi có TC ID hoặc `SPEC GAP` được nêu rõ; 100% ô `Applicable` đã rõ rule có TC ID; 100% TC có nguồn và oracle kiểm chứng được; 100% test function đã code ánh xạ về TC ID và các mệnh đề Expected Result; không có ID trùng hoặc rule mâu thuẫn chưa xử lý. `SPEC GAP` chưa được xác nhận không tính là đã phủ: đánh dấu phạm vi đó `Blocked/Partial`, không công bố full coverage hoặc tạo expected result phỏng đoán. Báo cáo danh sách ô thiếu, `N/A`, `SPEC GAP` và tỷ lệ phủ theo từng field/nhóm. Chỉ xét ngưỡng số lượng TC sau khi các gate này đạt.

### Bảng Self-Verification Checklist (11 Cổng Kiểm Soát Chất Lượng):
Trước khi bàn giao kết quả cho User, AI Agent phải tự đối soát:
- [ ] **Cổng 1 (Zero `copy/` Modification & Navigation Integrity)**: 100% không chạm vào bất kỳ file nào trong `copy/`; không xóa canonical target của các shortcut trong ba navigation groups; không ghi file nghiệp vụ/code/report trực tiếp dưới navigation groups.
- [ ] **Cổng 2 (Zero Assertions in Page Objects)**: Toàn bộ assertions nằm ở `tests/`, không nằm trong `pages/`.
- [ ] **Cổng 3 (Zero Hardcoded Data)**: Test data nằm ở `data/<module>/` hoặc fixtures, không viết cứng chuỗi trong test.
- [ ] **Cổng 4 (BSK Live Recon Evidence)**: Locators được trích xuất từ DOM sống thật, không đoán mò selector React.
- [ ] **Cổng 5 (Naming & Structure Convention)**: File test phân rã rõ `test_atomic_*` (đơn component) vs `test_integration_*` (nhiều component/form), test function có tiền tố `test_tc_<scenario_id>_...`.
- [ ] **Cổng 6 (5-Pillar Coverage & Minimum Density Check)**: Thu thập đủ 5 thông tin (BR, AC, Validation, Flow, Error Handling); hoàn thành ma trận coverage và 7 bước giao thức ở trên (mọi ô `Applicable` đã rõ rule có TC ID, `N/A` có lý do, `SPEC GAP` được nêu rõ và không tính là đã phủ, Expected Result có oracle/evidence); sau đó đối chiếu ngưỡng số lượng tối thiểu theo độ phức tạp form (15-25 TCs đơn giản, 30-45 TCs chuẩn, 50-70 TCs form động/phức tạp). Bắt buộc phủ kiểm tra chéo NRIC, BVA biên tuổi, Vòng đời thẻ động, HTTP 500 data preservation, và UI Health.
- [ ] **Cổng 7 (Single-Tab Execution Evidence Excel)**: File Excel bằng chứng video (`TEST_EXECUTION_EVIDENCE_*.xlsx`) BẮT BUỘC chỉ dùng ĐÚNG 1 TAB DUY NHẤT gom toàn bộ ca kiểm thử (không tách sheet), dùng native openpyxl hyperlink `▶ Play in Browser` (hoặc `📷 Screenshot (Pass)` cho ca pass).
- [ ] **Cổng 8 (High-Speed & Lean Media Execution)**: Tuân thủ `-n 3` song song, `--video=off` mặc định (triệt tiêu 100% overhead mã hóa WebM nền). Bằng chứng thu giữ chuẩn: ảnh từng step thao tác có highlight input (`step_X_*.png`) và ảnh `actual_result.png` có highlight kết quả thực tế. Tuyệt đối không để xảy ra hang 30s do click không điều kiện vào Cancel/Modal.
- [ ] **Cổng 9 (Max 250 Lines & Modular Component Standards)**: Tuyệt đối không để bất kỳ file Python nào vượt quá 250 dòng. Page Objects phải bóc tách thành `locators.py` (< 100 dòng), `components/` (< 150 dòng) và Page Orchestrator (< 200 dòng). Test suites phải phân tách theo từng trường (`test_atomic_<field>.py` < 200 dòng) và Data-Driven Testing; Tools phải tách Data (JSON/YAML) ra khỏi script logic.
- [ ] **Cổng 10 (Per-Module UAT Segregation & Unified Master Report)**: Toàn bộ kịch bản và báo cáo UAT phải nằm trong folder riêng theo phân hệ (`uat/r<xx>/`, `reports/uat/r<xx>/`), tuyệt đối không có folder chứa dấu cách (`uat r8`), và phải có 1 file Excel Master duy nhất (Single Tab) tổng hợp toàn bộ test cases của phân hệ.
- [ ] **Cổng 11 (No Autonomous Test Execution - Cấm AI Tự Chạy Test)**: AI 100% không tự ý thực thi các lệnh chạy test (`pytest`, `run_tests.py`); chỉ viết mã Python hoàn chỉnh dựa trên tài liệu đặc tả và cung cấp câu lệnh mẫu để User tự chạy.

---

## 5. Execution Commands & Quick Start
> [!IMPORTANT]
> **CÁC LỆNH DÀNH CHO USER TỰ CHẠY (AI TUYỆT ĐỐI KHÔNG TỰ CHẠY THEO INVARIANT 11)**:
> Theo Invariant 11, AI chỉ viết code dựa trên tài liệu và bàn giao file. User sẽ sao chép và tự thực thi các lệnh dưới đây từ thư mục gốc `/home/baudui/Projects/automation-ui` (CẤM `cd copy` và không chạy từ folder navigation):

```bash
# 1. Trinh sát DOM sống của màn hình mục tiêu (Bắt buộc chạy trước khi code)
python3 tools/recon_bsk.py --url http://localhost:5174/profile

# 2. Chạy kiểm thử đơn component cô lập (Atomic)
.venv/bin/pytest tests/<fs_module>/<component>/test_atomic_<feature>_components.py -v

# 3. Chạy kiểm thử tích hợp liên component / Form (Integration)
.venv/bin/pytest tests/<fs_module>/<component>/test_integration_<feature>.py -v

# 4. Chạy toàn bộ ticket suite và xuất HTML Dashboard
# run_tests.py chuyển đường dẫn và options trực tiếp cho pytest; hiện chưa có --ticket parser.
python3 run_tests.py tests/<fs_module>/<component>/
```
