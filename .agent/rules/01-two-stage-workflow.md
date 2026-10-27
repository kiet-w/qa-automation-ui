# RULE MODULE 01: QUY TRÌNH 2 GIAI ĐOẠN BẮT BUỘC & BỘ NGŨ NGUYÊN LIỆU KIỂM THỬ (5 PILLARS)
> **Mục đích**: Áp dụng khi nhận lệnh thiết kế test case, kiểm thử màn hình/URL, hoặc chuyển hóa test case sang code automation.
> **Trọng tâm**: Giai đoạn 1 (Thiết kế test case) -> Giai đoạn 2 (AI Coding), Bộ ngũ nguyên liệu (BR + AC + Validation + Functional Flow + Error Handling), phân tách Test Suite, cấu trúc 5 phần file `.md`, và xuất Excel/Dashboard.

> [!IMPORTANT]
> **Path contract**: Luôn đọc/ghi bằng canonical paths ở repository root (`specs/`, `testcases/`, `pages/`, `data/`, `tests/`, `reports/`). Ba folder `1_Nghiep_Vu_va_Specs/`, `2_Code_Automation/`, `3_Bao_Cao_va_Ket_Qua/` chỉ là navigation views bằng symlink; không dùng chúng làm output path và không xóa canonical targets.

## 1.1 QUY TRÌNH 2 GIAI ĐOẠN BẮT BUỘC: THIẾT KẾ TEST CASE (5 NGUYÊN LIỆU CỐT LÕI) ➔ AI CODING AUTOMATION
> [!IMPORTANT]
> **MANDATE BẮT BUỘC TUÂN THỦ 100% (KHÔNG ĐƯỢC PHÉP LÀM KHÁC)**:
> Khi nhận lệnh kiểm thử bất kỳ màn hình / URL nào (Ví dụ: `đơn component cho trang http://localhost:5174/profile /combo-qa` hoặc `integration test phân hệ fs08`):
> Toàn bộ quá trình phải diễn ra theo **2 Giai Đoạn Liền Mạch** với **Bộ Ngũ Nguyên Liệu Bắt Buộc (5 Pillars)** kết hợp với **Live DOM**:
> 
> ```text
> ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
> 💎 GIAI ĐOẠN 1: THIẾT KẾ TEST CASE DỰA TRÊN BỘ NGŨ NGUYÊN LIỆU CỐT LÕI (5 PILLARS) & LIVE DOM
> ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
> 
>   [1. Business Rules (BR)]      [2. Acceptance Criteria (AC)]   [3. Validation Rules]          [4. Functional Flow]          [5. Error Handling & Feedback]
>   • Ràng buộc logic nghiệp vụ   • Tiêu chí nghiệm thu User Story• Ma trận 12 lớp (Empty, BVA)   • Luồng State Machine, dirty   • Catalog mã lỗi (MSG-xxxx)
>   • Phân quyền theo tuổi, vai trò• Given - When - Then cụ thể   • Định dạng regex, min/max len • View 🔁 Edit 🔁 Confirm Dialog• Viền đỏ aria-invalid, toasts
>   • Quyết định bất biến D-xx    • Kế thừa mã AC (R8-ACxx)       • Bảng tra cứu BVA biên        • Transition states, mutations • Banner cảnh báo, modals
>   (specs/md/FS doc, DECISIONS)  (specs/md/Test Cases/, Backlog) (specs/component_specs/*/atomic)(specs/component_specs/*/integ)(specs/component_specs/*/README)
>                 │                             │                               │                              │                               │
>                 └─────────────────────────────┴───────────────┬───────────────┴──────────────────────────────┴───────────────────────────────┘
>                                                               ▼
>                                           [+ BSK Live DOM Recond Reconnaissance]
>                                           • python3 tools/recon_bsk.py --url <URL>
>                                           • Selectors, roles, tags, inputs từ DOM sống thật
>                                                               │
>                                                               ▼
>                               🎯 TỔNG HỢP VÀO KHO TEST CASES CHUẨN (SINGLE SOURCE OF TRUTH):
>                                  `testcases/<fs_module>/<fs_module>-<tên-component>/`
>                                  ├── `TC_<MODULE>_<FEATURE>.md`   (Ma trận 20 cột kèm Steps Test, BSK Locators, JSON Fixtures)
>                                  └── `TC_<MODULE>_<FEATURE>.xlsx` (Excel 20 cột chuẩn Google Sheet có cột Steps Test)
> 
> ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
> 🚀 GIAI ĐOẠN 2: AI CODING DỰA TRÊN TEST CASE ĐỂ SINH CODE AUTOMATION TESTING
> ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
>                                                         │
>                                                         ▼
>               📋 BƯỚC 2.1: ĐỐI SOÁT & KẾ THỪA TRỰC TIẾP TỪ FILE TEST CASE (`TC_*.md`)
>               • CẤM MỞ SOURCE CODE: Tuyệt đối không mở `copy/` hoặc đoán code React/Vue!
>               • Đọc file `testcases/<fs_module>/<fs_module>-<tên-component>/TC_<MODULE>_<FEATURE>.md`:
>                 - Lấy danh sách Test Cases (ID, Title, Steps, Expected Result, Traceability).
>                 - Lấy BSK Live DOM Locators từ Phần 3.
>                 - Lấy JSON Fixtures từ Phần 4 (baseline, mutation, BVA boundaries, XSS vectors).
>               • Nếu `testcases/` chưa có: Bắt buộc thực hiện Giai Đoạn 1 trước khi bắt đầu code!
>                                                         │
>                                                         ▼
>               🔨 BƯỚC 2.2: TRIỂN KHAI MÃ NGUỒN KIỂM THỬ (PAGE OBJECTS, FIXTURES & TESTS)
>               1. `pages/<fs_module>/<tên-component>_page.py`:
>                  - Đóng gói toàn bộ locators từ Live DOM BSK và các action methods (`open`, `fill`, `click`).
>                  - TUYỆT ĐỐI TUÂN THỦ INVARIANT 1: Zero Assertions in Page Objects!
>               2. `data/<fs_module>/<fs_module>_data.json`:
>                  - Lưu trữ fixtures dữ liệu kiểm thử độc lập, không hardcode trong test (Invariant 2).
>               3. `tests/<fs_module>/<fs_module>-<tên-component>/`:
>                  ├── `__init__.py`
>                  ├── `conftest.py` (Fixtures setup/teardown rollback dữ liệu như `restore_profile_...`)
>                  ├── `test_atomic_<feature>_components.py` (Kiểm thử ĐƠN COMPONENT cô lập)
>                  └── `test_integration_<feature>.py`      (Kiểm thử GIỮA NHIỀU COMPONENT & Form 🔁 Dialog/API)
>                                                         │
>                                                         ▼
>               ⚙️ BƯỚC 2.3: BÀN GIAO MÃ NGUỒN VÀ HƯỚNG DẪN CÂU LỆNH CHO USER THỰC THI (TUÂN THỦ INVARIANT 11)
>               • ⛔ CẤM TUYỆT ĐỐI AI TỰ CHẠY TEST: AI không được tự ý thực thi `pytest` hay `run_tests.py`. User sẽ toàn quyền tự chạy code test.
>               • AI chỉ code Python dựa trên tài liệu đặc tả (specs, component_specs, testcases), sau đó bàn giao mã nguồn và cung cấp sẵn câu lệnh mẫu để User tự chạy.
>               • Vị trí chạy lệnh của User: BẮT BUỘC đứng tại thư mục gốc `/home/baudui/Projects/automation-ui` (KHÔNG ĐƯỢC đứng trong `copy/` hoặc folder navigation).
>               • Cú pháp câu lệnh chuẩn cung cấp cho User tự thực thi:
>                 - Đơn Component: `.venv/bin/pytest tests/<fs_module>/<fs_module>-<component>/test_atomic_<feature>_components.py -v`
>                 - Nhiều Component: `.venv/bin/pytest tests/<fs_module>/<fs_module>-<component>/test_integration_<feature>.py -v`
>                 - Toàn bộ Component: `.venv/bin/pytest tests/<fs_module>/<fs_module>-<component>/ -v`
>               • User chạy test sẽ thu ảnh step/actual-result và xuất báo cáo HTML; video mặc định tắt, chỉ có khi User chủ động dùng `--video=retain-on-failure` hoặc `--video=on`:
>                 `reports/<fs_module>/<fs_module>-<tên-component>/execution_report.html`
> ```
> 
> ### ⚠️ BẢNG ĐỐI CHIẾU 5 SAI LẦM PHỔ BIẾN CẦN TRÁNH TUYỆT ĐỐI:
> | Hành vi Sai Trái (BỊ CẤM) | Hành vi Đúng Chuẩn Của Dự Án |
> | :--- | :--- |
> | ❌ AI tự ý chạy lệnh thực thi test (`pytest`, `run_tests.py`) sau khi code xong. | ✅ Tuân thủ Invariant 11: AI chỉ code Python dựa trên tài liệu và bàn giao file kèm câu lệnh để User tự chạy. |
> | ❌ Tự bịa test case hoặc kịch bản mới khi trong `specs/md/Test Cases/` đã có sẵn. | ✅ Tra cứu `specs/md/Test Cases/TC_Rxx...md` và `tests/<fs_module>/...`, kế thừa 100% test case đã có. |
> | ❌ Mở mã nguồn trong `copy/` hoặc file `.tsx`, `.jsx` để đọc component và đoán tên selector / ID. | ✅ Chạy `python3 tools/recon_bsk.py --url <URL>` để BSK mở web thật và nhặt đúng selector từ DOM sống. |
> | ❌ Đặt tên file chung chung, không phân biệt đơn component (`atomic`) và nhiều component (`integration`). | ✅ Đặt tên file chuẩn hóa: `test_atomic_<feature>_components.py` (đơn) vs `test_integration_<feature>.py` (nhiều component). |
> | ❌ Gom phẳng Test Suite thành 1 nhóm chung chung ("My Details", "My Profile") hoặc gộp nhiều input vào 1 test case. | ✅ Phân rã Test Suite theo từng ô Input/Component cụ thể (Phone, Email, Street, Postal, State, Dialog) và thiết kế đầy đủ ca kiểm thử biên (BVA), rỗng (`MSG-0001`), cú pháp (`MSG-0805`/`MSG-0806`), khoảng trắng (`ASM-15`) cho từng trường. |
> | ❌ Đứng trong `copy/` hoặc folder navigation để gõ lệnh chạy pytest/python. | ✅ Luôn đứng tại `/home/baudui/Projects/automation-ui` và dùng canonical test path. |
> 
> ---
> 
> ### 1.2 BA TRỤC TRUY VẾT TRONG BỘ 5 PILLARS (BR + AC + UI Evidence)
> Khi tạo hoặc cập nhật Test Case, AI vẫn phải thu thập đủ 5 pillars. Ba trục BR, AC và UI Evidence dưới đây chỉ là cách nhóm traceability để trình bày; Validation Rules, Functional Flow và Error Handling không được phép bị lược bỏ và phải được dẫn nguồn riêng.
> 
> #### 1. Tam Giác Nguyên Liệu Bắt Buộc (The 3 Core Ingredients)
> Mỗi ca kiểm thử (Test Case) sinh ra đều phải là giao thoa của đủ 3 nguyên liệu:
> 1. **Nguyên Liệu 1 - Business Rules (BR - Luật Nghiệp Vụ Cốt Lõi)**:
>    - Các điều kiện tiên quyết, phân quyền truy cập, ràng buộc bất biến và vòng đời dữ liệu.
>    - *Ví dụ*: Phụ huynh có con $\ge 16$ tuổi thì khóa sửa hồ sơ (`BR-08-01`); Họ tên/NRIC/Residential Address bất biến từ Singpass (`BR-08-03` / `D-20`); Tuyệt đối không gửi email thông báo khi đổi thông tin (`BR-08-04` / `D-28`); Chỉ sửa hồ sơ của chính mình, độc lập cha/mẹ (`BR-08-02`).
>    - *Nguồn khai thác*: `specs/md/FS document/` (các mục FR, Bảng thuộc tính, Bảng mã lỗi), [`specs/md/FS_SPECIFICATIONS_SUMMARY.md`](specs/md/FS_SPECIFICATIONS_SUMMARY.md), [`specs/md/MEETINGS_AND_DECISIONS_SUMMARY.md`](specs/md/MEETINGS_AND_DECISIONS_SUMMARY.md).
> 2. **Nguyên Liệu 2 - Acceptance Criteria (AC - Tiêu Chuẩn Nghiệm Thu Cụ Thể)**:
>    - Các kịch bản hành vi Given - When - Then chi tiết của từng User Story (`US-xxx`).
>    - Bắt buộc kế thừa 100% ID gốc (ví dụ `R8-AC01` đến `R8-AC28`) và mã thông báo lỗi hệ thống chuẩn (`MSG-0001`, `MSG-0805`, `MSG-0806`, `MSG-0807`, `MSG-0808`).
>    - *Nguồn khai thác*: `specs/md/Test Cases/TC_Rxx...md`, [`specs/md/REQUIREMENTS_AND_BACKLOG_SUMMARY.md`](specs/md/REQUIREMENTS_AND_BACKLOG_SUMMARY.md#L254), [`specs/md/Product Backlog V2.md`](specs/md/Product%20Backlog%20V2.md).
> 3. **Nguyên Liệu 3 - UI Specification & Live DOM Recon (UI - Giao Diện & Selector Sống)**:
>    - Đặc tả trạng thái giao diện: cơ chế dirty/pristine, debounce chống double-click, hộp thoại xác nhận modal `alertdialog`, inline validation alerts, toasts.
>    - **Bắt buộc chạy trinh sát Live DOM**: Chạy `python3 tools/recon_bsk.py --url <URL>` để lấy chính xác 100% CSS selectors, tag types, input attributes từ DOM sống. TUYỆT ĐỐI CẤM đoán mò selector hay mở source code trong `copy/`.
>    - *Nguồn khai thác*: [`specs/md/EAFAMS_UI_SPECIFICATION_AND_INTERACTION_GUIDE.md`](specs/md/EAFAMS_UI_SPECIFICATION_AND_INTERACTION_GUIDE.md) và kết quả quét từ `tools/recon_bsk.py`.
> 
> ---
> 
> #### 2. Quy Chuẩn AI Coding Chuyển Hóa Test Case Thành Code Tự Động (Code Generation Flow)
> Sau khi file `TC_<MODULE>_<FEATURE>.md` được tạo đầy đủ từ 3 nguyên liệu trên, **AI Coding Agent** sẽ sử dụng file này làm **Kim Chỉ Nam Duy Nhất** để triển khai mã nguồn kiểm thử tự động mà không cần đọc lại FSD hay mã nguồn sản phẩm:
> - **Bước 1 - Sinh Page Object (`pages/<fs_module>/<component>_page.py`)**:
>   - Nhặt danh sách Selector từ Phần 3 của `TC_*.md` (BSK Live DOM Locators).
>   - Viết các action methods tương tác (`open`, `fill`, `click`, `toggle`, `wait`).
>   - Tuân thủ nghiêm ngặt **Invariant 1**: Tuyệt đối không đưa lệnh `assert` vào Page Object!
> - **Bước 2 - Sinh Test Data Fixture (`data/<fs_module>/<fs_module>_data.json`)**:
>   - Nhặt bộ dữ liệu kiểm thử từ Phần 4 của `TC_*.md` (JSON Fixtures: baseline, valid payload, invalid payload, boundary values, XSS payload).
>   - Không hardcode dữ liệu trong file test (Invariant 2).
> - **Bước 3 - Sinh Test Suites (Phân Tách Đơn vs Nhiều Component)**:
>   - `tests/<fs_module>/<fs_module>-<component>/test_atomic_<feature>_components.py`: Chuyển hóa toàn bộ ca test Đơn Component (Validate từng trường, BVA biên, regex, empty `MSG-0001`, Invariant 7 UI health).
>   - `tests/<fs_module>/<fs_module>-<component>/test_integration_<feature>.py`: Chuyển hóa toàn bộ ca test Multi-Component (Form $\leftrightarrow$ Confirm Dialog, Keep editing, Save mutation, Mock API 500 `MSG-0808`, Phân quyền tuổi con).
> - **Bước 4 - Bàn Giao Mã Nguồn & Cung Cấp Cú Pháp Lệnh Cho User (Tuân thủ Invariant 11)**:
>   - AI bàn giao toàn bộ mã nguồn Python (`pages/`, `data/`, `tests/`) chuẩn xác dựa trên tài liệu đặc tả, **TUYỆT ĐỐI KHÔNG TỰ CHẠY TEST**.
>   - Cung cấp sẵn cú pháp câu lệnh để User tự sao chép và thực thi từ thư mục gốc: `.venv/bin/pytest tests/<fs_module>/<fs_module>-<component>/ -v`
>   - Khi User thực thi, hệ thống xuất JSON/HTML report và screenshot evidence tại `reports/<fs_module>/<fs_module>-<component>/`; video chỉ được tạo khi User bật explicit video mode.
> 
> ---
> 
> #### 3. Nguyên Tắc Phân Tách Test Suite Theo Từng Ô Input (Field-Level Decomposition)
> - **CẤM gom phẳng Test Suite**: Tuyệt đối không đặt tên Test Suite chung chung cho cả trang (ví dụ: `My Details` hay `My Profile`) hoặc dùng chung 1 Scenario ID cho toàn bộ các dòng.
> - **Tách Test Suite & Scenario ID độc lập cho từng Component/Input**:
>   - Trường định danh SingPass: `TS-<SEQ>-ID` (Full Name, NRIC masking, Residential Address immutability).
>   - Từng trường nhập liệu độc lập: `TS-<SEQ>-TEL` (Phone), `TS-<SEQ>-EML` (Email), `TS-<SEQ>-BLK` (Block), `TS-<SEQ>-UNT` (Unit), `TS-<SEQ>-STR` (Street), `TS-<SEQ>-POS` (Postal Code), `TS-<SEQ>-CTY` (Country).
>   - Trạng thái giao diện & chuyển mode: `TS-<SEQ>-STA` (View $\leftrightarrow$ Edit, Pristine disabled, Dirty enabled).
>   - Hộp thoại xác nhận & Lưu: `TS-<SEQ>-SUB` (Modal alertdialog, Keep editing, Confirm Save mutation, Debounce, Toast `MSG-xxxx`).
>   - Quy tắc nghiệp vụ & Vòng đời: `TS-<SEQ>-AGE` (Phân quyền theo tuổi, BOLA/IDOR `MSG-0003`, Độc lập hồ sơ).
>   - Phi chức năng & Sức khỏe UI: `TS-<SEQ>-NFR` (Invariant 7: 0 Console Errors, Zero Horizontal Scrollbar, WCAG 2.1 AA Contrast).
> 

> #### 4. Nguyên Tắc Ép Bao Phủ Toàn Bộ & Chống Sinh Thiếu Test Case (Full-Coverage Enforcement & Minimum Density)
> - **Nguyên nhân cốt lõi gây sinh thiếu Test Case**:
>   - Bẫy "Happy Path": Chỉ nhìn kịch bản UAT lướt qua màn hình (User POV) mà bỏ quên góc nhìn kỹ thuật phần mềm (Defensive Engineering & Edge Cases).
>   - Bỏ sót Thẻ động (Dynamic Sub-forms) & Ràng buộc chéo (Cross-field dependencies).
>   - Bỏ sót Ma trận 12 lớp validation cho từng ô input và bỏ quên khả năng chịu lỗi (Error resilience HTTP 500 & UI Health).
> - **Cơ chế Ép Bao Phủ Bắt Buộc (Mandatory Full Coverage Gates)**:
>   - Mọi form/màn hình khi thiết kế test case bắt buộc phải vượt qua ngưỡng mật độ tối thiểu (Minimum Density Formula):
>     1. *Form Đơn Giản (1-3 fields)*: Tối thiểu $\ge 15 - 25$ TCs.
>     2. *Form Nghiệp Vụ Chuẩn (4-8 fields)*: Tối thiểu $\ge 30 - 45$ TCs.
>     3. *Form Phức Tạp / Dynamic Sub-forms ($\ge 9$ fields như FAS, Profile, Registration)*: Tối thiểu $\ge 50 - 70$ TCs.
>   - **5 Nhóm Kiểm Thử Bắt Buộc Phải Có Đủ**:
>     1. *Validation 12 Lớp Từng Trường*: Empty, Whitespace trim, Min/Max BVA biên dưới/trong/trên, Regex cú pháp, Ký tự đặc biệt, XSS, Visual `aria-invalid`.
>     2. *Cross-field & Duplicate Checking*: Kiểm tra trùng lặp NRIC/ID chéo giữa các đối tượng (ví dụ: cha-con, anh-em, người thân), ràng buộc rẽ nhánh logic.
>     3. *BVA Biên Tuổi & Ngày Sinh*: Test đủ biên trong, biên ngoài, mầm non, quá tuổi, và ngày sinh tương lai.
>     4. *Vòng Đời Thẻ Động (State Machine)*: Thêm, xóa, re-index, reset form sạch nguyên thủy ("Start a new application").
>     5. *Error Resilience & UI Health*: Giả lập HTTP 500 sập mạng bảo toàn dữ liệu, 0 rò rỉ mã dịch `features.*`, 0 uncaught console error.
> 
> #### 5. Cấu Trúc 5 Phần Bắt Buộc Trong File Markdown Đặc Tả (`.md`)
> Mỗi file đặc tả test case Markdown phải chứa đủ 5 phần rõ ràng:
> 1. **Phần 1: Bảng tổng quan phân bổ Test Suites & Input Components**:
>    - Bảng 1.1: **Bảng Tổng Quan Ma Trận Phân Định 3 Trụ Cột (BR vs AC vs Tech & UI Matrix)**.
>    - Bảng 1.2: **Bảng Phân Bổ Theo 12 Test Suites Của Từng Input Component**.
> 2. **Phần 2: Ma trận Test Case chi tiết đủ 20 cột chuẩn Google Sheet (Phân Chia Theo 3 Trụ Cột, Có Cột Steps Test)**:
>    - `2.1 Trụ Cột 1: Các Ca Kiểm Thử Luật Nghiệp Vụ Cốt Lõi (Business Rules)`
>    - `2.2 Trụ Cột 2: Các Ca Kiểm Thử Tiêu Chuẩn Nghiệm Thu User Story (Acceptance Criteria)`
>    - `2.3 Trụ Cột 3: Các Ca Kiểm Thử Kỹ Thuật Biên, Ma Trận Ô Nhập & Sức Khỏe UI NFR (Tech & UI Matrix)` *(Bắt buộc tra cứu & kế thừa thư viện case sẵn có tại [`.agent/rules/02-field-test-matrix.md Mục G`](file:///.agent/rules/02-field-test-matrix.md) gồm: Controls mở rộng 7, Vòng đời Form 8, Sức khỏe UI 9, và Bảo mật PII 10)*.
>    Đủ 20 cột chuẩn: `ID` \| `Scenario ID` \| `Title` \| `Test Suite` \| `Page` \| `Severity` \| `Priority` \| `Execution Status` \| `Test Type` \| `Environment` \| `Preconditions` \| `Test Data` \| `Steps Test` \| `Test Steps` \| `Expected Result` \| `Actual Result` \| `Assumption Ref` \| `Defect ID` \| `Traceability` \| `Note`.
> 3. **Phần 3: Bảng tra cứu Locator Live DOM từ BSK**: Trích xuất selector thật từ `python3 tools/recon_bsk.py --url <URL>`.
> 4. **Phần 4: Fixture dữ liệu kiểm thử (JSON Fixtures)**: Bộ dữ liệu mẫu gồm baseline, mutation, các vector biên (BVA) và XSS payload.
> 5. **Phần 5: Bảng Traceability đối soát FSD, AC & Error Catalog**: Ma trận truy vết 2 chiều giữa kịch bản kiểm thử và FSD Section ID, AC ID, Quyết định họp (`D-xx`), Mã lỗi hệ thống (`MSG-xxxx`).
> 
> #### 6. Quy Chuẩn Tinh Gọn Báo Cáo: CHỈ TẬP TRUNG VÀO EVIDENCE EXCEL & EXECUTION REPORT
> - **Chính sách Tối Giản (Zero Bloat Reports)**:
>   - **KHÔNG sinh hoặc lưu trữ biến thể báo cáo tùy tiện**. `bao_cao_tinh_gon.html` chỉ được phép tồn tại khi do report engine hiện hành sinh tự động; không tạo thêm `executive_v2.html`, workbook rời hoặc bản sao không có ownership.
>   - **2 TÀI SẢN BÀN GIAO BẮT BUỘC**:
>     1. `execution_report.html`: Báo cáo thực thi chuẩn ExtentReports (đầy đủ timeline, log, step tracking, video modal).
>     2. `TEST_EXECUTION_EVIDENCE_<MODULE>_<FEATURE>.xlsx`: File Excel bằng chứng thực thi duy nhất (Single-Tab Enforced).
>   - **Tuyệt đối cấm tạo thư mục rác**: Cấu hình runner không bao giờ được tạo thư mục chứa tên test function hay ký tự `::` bên trong thư mục `reports/`.
> 
> - **Quy chuẩn Báo Cáo Thực Thi & Bằng Chứng Video (Execution Evidence Excel & Video Handling)**:
>   - **Vị trí và ownership bắt buộc**: Testcase thiết kế nằm tại `testcases/<fs_module>/<component>/TC_*.md|xlsx`; execution evidence nằm tại `reports/<fs_module>/<component>/TEST_EXECUTION_EVIDENCE_*.xlsx`. Không copy trạng thái chạy ngược vào testcase gốc; nếu cần liên kết, dùng traceability ID/hyperlink.
>   - **Số Lượng Sheet (BẮT BUỘC 1 TAB DUY NHẤT - STRICT SINGLE TAB MANDATE)**:
>     - File Excel bằng chứng thực thi video (`TEST_EXECUTION_EVIDENCE_*.xlsx`) **BẮT BUỘC CHỈ ĐƯỢC PHÉP CÓ ĐÚNG 1 TAB DUY NHẤT** (ví dụ: `Execution Evidence (<N> TCs)`).
>     - **TUYỆT ĐỐI CẤM** tách thành nhiều tabs riêng biệt (như Tab Business Rules, Tab Acceptance Criteria, Tab Tech...) làm phân tán dữ liệu và bắt người dùng phải bấm chuyển tab qua lại.
>     - Toàn bộ ca kiểm thử từ tất cả các Trụ Cột (BR, AC, Tech & UI) phải gom chung vào 1 bảng duy nhất trên Tab này. Việc phân biệt Trụ Cột được thể hiện trực quan qua cột `Pillar` (BR, AC, Tech) kèm màu sắc nhận diện rõ ràng.
>     - Hàng 1 & 2 bắt buộc là Executive Banner (Total Tests, Pass Rate, Defect Count, Video Count, Target URL).
>     - Pinned Freeze Panes tại ô `E5` (cố định các cột định danh No, ID, Pillar, Scenario ID và 4 hàng header).
>   - **Quy chuẩn gán Hyperlink Video (CHỐNG LỖI Ô TRỐNG TRÊN WPS OFFICE / LIBREOFFICE)**:
>     - **CẤM TUYỆT ĐỐI** dùng công thức chuỗi `=HYPERLINK(...)` vì các trình đọc bảng tính như WPS Office, LibreOffice Calc, Excel Online thường không render kịp giá trị tính toán và làm hiển thị ô trắng.
>     - **BẮT BUỘC** gán Native Hyperlink bằng openpyxl:
>       ```python
>       cell.value = "▶ Play in Browser"
>       cell.hyperlink = video_url
>       ```
>   - **Cơ chế Phát Video Trên Trình Duyệt (Opt-in, Offline-first)**:
>     - Mặc định không có video vì `pytest.ini` dùng `--video=off`.
>     - Khi User bật video để debug, native hyperlink phải trỏ tới media cục bộ trong `reports/<fs_module>/<component>/test-results/` hoặc một URL đã được User cung cấp/xác nhận.
>     - Không tự động upload/deploy evidence lên Cloudflare hoặc dịch vụ bên ngoài. Việc publish cần yêu cầu và quyền hạn riêng của User.
> 
> #### 7. Quy chuẩn Lưu Trữ UAT Theo Từng Phân Hệ R & Báo Cáo Thống Nhất Master (Per-Module UAT Segregation)
> - **Cấu Trúc Thư Mục Theo Phân Hệ**:
>   - Mọi tài liệu, kịch bản UAT (`.md`, `.xlsx`) và artifacts phải được phân chia rạch ròi theo thư mục:
>     `uat/r01/`, `uat/r02/`, `uat/r03/`, `uat/r08/`, `uat/r09/`, `uat/r10/`...
>   - Báo cáo kết quả UAT lưu tại `reports/uat/r<xx>/`.
> - **Cấm Tuyệt Đối**:
>   1. Lưu file UAT trôi nổi tự do tại thư mục gốc `uat/` hay `reports/`.
>   2. Đặt tên thư mục chứa dấu cách (whitespace) như `uat r8`, `r08 uat`. Bắt buộc dùng kebab-case: `r08`, `fs08`.
>   3. Tách nhỏ lẻ nhiều file excel kết quả khi hoàn thành cả phân hệ: Khi một phân hệ (như R8) hoàn thành toàn bộ các UAT modules, BẮT BUỘC phải gom toàn bộ test cases về **1 File Excel Thống Nhất Duy Nhất** (`TEST_EXECUTION_EVIDENCE_R<XX>_UAT_MASTER.xlsx` - Single Tab) và 1 Master Dashboard HTML (`R<XX>_UAT_MASTER_DASHBOARD.html`).
> 
> ---
> 
> ## 2. Core Invariants for AI & Developers

