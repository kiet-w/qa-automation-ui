# Ma Trận Test Case: Đợt Thu Phí & Xuất Bản Công Nợ (Fee Batches & Student Charge Publication)

> **Mô đun**: `Financial Management` / `Fee Batches & Student Charges`  
> **Kịch bản UAT tương ứng**: `UAT-021` (Preview and publish fees once, then expose correct charges) & `UAT-MOE-01` (Prepare EA, school, student and publish fees)  
> **User Stories liên quan**: `US-037`, `US-038`, `US-039`, `US-040`  
> **Phạm vi giao diện**: `/support-console` (View As), `/fee-batches/new`, `/fee-batches/:batchId`, Cổng Phụ huynh E-Service Singpass  
> **Tiêu chuẩn**: ISTQB Foundation / ISO/IEC/IEEE 29119-3 / `combo-qa` Specification Standard  
> **Nguyên tắc cốt lõi**: Pure Black-Box Testing (Bám sát Live DOM và Đặc tả UAT, không đọc mã nguồn nội bộ)

---

## 1. Bóc Tách Thực Thể & Kiến Trúc Nghiệp Vụ

### 1.1 Bảng Từ Điển Dữ Liệu & Ràng Buộc Biểu Mẫu (Data Dictionary & Constraints)

| Thực Thể | Trường Dữ Liệu | Kiểu / Format | Bắt Buộc | Ràng Buộc Nghiệp Vụ & Kỹ Thuật | Ý Nghĩa Nghiệp Vụ |
| :--- | :--- | :--- | :---: | :--- | :--- |
| **Support Console (View As)** | `reason` (`textarea`) | String (10..500 ký tự) | Có | Bắt buộc $\ge 10$ ký tự; nút Submit bị mờ xám (`disabled`) nếu $<10$ ký tự | Lý do kiểm toán khi tài khoản MOE HQ đóng vai cán bộ trường |
| | `ticket_ref` (`input`) | String (1..50 ký tự) | Có | Không được để trống; định dạng ticket hỗ trợ (vd: `UAT-KENT-01`) | Mã ticket phê duyệt phiên hỗ trợ |
| | `target_school` | Select / Search | Có | Trường áp dụng phiên đóng vai (vd: `Rosyth Primary School`) | Ngữ cảnh trường học mục tiêu |
| | `target_role` | Select / Radio | Có | `School Admin` hoặc `School Reviewer` | Vai trò đóng vai tại trường |
| **Fee Publication Batch** | `fee_component_id` | UUID / Query Param | Có | Tham số bắt buộc trên URL (`?feeComponentId=<id>`); nếu thiếu hệ thống hiển thị banner cảnh báo | Liên kết đợt thu với biểu phí gốc |
| | `title` (`#fee-publication-title`) | String (1..150 ký tự) | Có | Không để trống; loại bỏ khoảng trắng thừa | Tiêu đề định danh đợt thu phí |
| | `period_start` (`#fee-publication-period-start`) | Date (`YYYY-MM-DD`) | Có | Ngày bắt đầu chu kỳ tính phí; nằm trong khoảng hiệu lực của Component | Mốc bắt đầu kỳ học vụ |
| | `period_end` (`#fee-publication-period-end`) | Date (`YYYY-MM-DD`) | Không | Mang tính loại trừ (`exclusive`); nếu nhập phải thỏa mãn: `period_end > period_start` | Mốc kết thúc kỳ học vụ |
| | `schedule_publish_at` (`#fee-publication-schedule-at`) | DateTime | Không | Để trống để xuất bản thủ công ngay lập tức; nếu nhập phải ở thời điểm tương lai | Lịch hẹn xuất bản tự động |
| | `due_date` (`#fee-publication-due-date`) | Date (`YYYY-MM-DD`) | Có | Hạn chót thanh toán; bắt buộc `due_date >= period_start` | Hạn cuối phụ huynh phải thanh toán |
| | `schools_target` | Radio | Có | `Specific schools` (chọn Rosyth Primary School) hoặc bị khóa theo trường của user | Phạm vi trường học áp dụng |
| | `students_target` | Radio | Có | `All eligible students` hoặc `Specific students` | Danh sách đối tượng học sinh áp dụng |
| **Student Charge** | `charge_id` | UUID / Text | Hệ thống sinh | Định danh duy nhất cho từng khoản công nợ của học sinh | Mã khoản nợ bàn giao cho luồng thanh toán |
| | `status` | Enum | Hệ thống gán | Chuyển từ không tồn tại (ở preview) sang `POSTED` (sau khi publish) | Trạng thái ghi nhận nợ chính thức |
| | `amount` | Decimal (10,2) | Hệ thống tính | Phải khớp chính xác với biểu phí cấu hình theo Stage $\times$ Category (vd: `100.00 SGD`) | Số tiền nợ thực tế phải trả |

---

### 1.2 Ma Trận Chuyển Trạng Thái Đợt Phí (State Transition Table)

| Trạng Thái Ban Đầu | Sự Kiện / Hành Động Trigger | Điều Kiện Guard | Trạng Thái Đích | Tác Động Phụ & Biểu Hiện UI / DB |
| :--- | :--- | :--- | :--- | :--- |
| `[None]` | Mở `/fee-batches/new` không có query param | Thiếu tham số `feeComponentId` | `[Form: Blocked]` | Hiển thị Warning Alert: "Fee component is required. Open this page from a fee component before creating a publication."; form bị khóa |
| `[None]` | Mở `/fee-batches/new?feeComponentId=<id>` | Có `feeComponentId` hợp lệ | `[Batch: Pristine Draft]` | Form nhập liệu hiển thị đầy đủ các trường, nút `Create draft` ở trạng thái sẵn sàng |
| `[Batch: Pristine Draft]` | Nhấn nút `Create draft` | Vi phạm validation (rỗng Title, Dates không hợp lệ) | `[Batch: Invalid Form]` | Kích hoạt `aria-invalid="true"` trên các input vi phạm; hiển thị inline error text |
| `[Batch: Pristine Draft]` | Điền đủ trường và nhấn `Create draft` | Title hợp lệ, `period_end > period_start`, `due_date >= period_start` | `[Batch: Draft Saved]` | Gửi `POST /v1/fees/fee-publication-batches`; trả về HTTP 201; chuyển hướng sang `/fee-batches/:batchId`; Badge trạng thái hiển thị `Draft` |
| `[Batch: Draft Saved]` | Mở mục "Student charge preview" và lọc học sinh | Batch ở trạng thái `Draft` | `[Batch: Draft Preview]` | Bảng hiển thị học sinh đủ điều kiện (Liam Pham - SGD 100.00); **Tuyệt đối 0 bản ghi Student Charge được tạo trong DB; Số dư ví Edusave giữ nguyên; Cổng Phụ huynh hiển thị 0 khoản nợ** |
| `[Batch: Draft Saved]` | Nhấn nút `Publish` | Component có biểu phí hợp lệ; có ít nhất 1 học sinh đủ điều kiện | `[Batch: Published]` | Gửi yêu cầu publish; Badge trạng thái đổi sang `Published` hoặc `Completed`; Bản ghi Student Charge được tạo ở trạng thái `POSTED`; Nút `Publish` bị ẩn hoặc vô hiệu hóa |
| `[Batch: Published]` | Thực hiện lại hành động Publish (Click lại / Gửi lại request) | Batch đã ở trạng thái `Published` | `[Batch: Published]` | Hệ thống chặn lặp lại (Idempotency); không tạo thêm bất kỳ khoản nợ trùng lặp nào; số lượng bản ghi Student Charge giữ nguyên |

---

### 1.3 Bảng Quyết Định: Đối Tượng Tính Phí & Xuất Bản (Decision Table)

| Điều Kiện Nghiệp Vụ | R1 (Chuẩn UAT-021) | R2 (Học sinh chưa có EA) | R3 (Khác Khối Lớp / Stage) | R4 (Thiếu Biểu Giá Rate Rule) | R5 (Kỳ Phí Vượt Quá Hiệu Lực Component) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Trường học trực thuộc | Rosyth Primary School | Rosyth Primary School | Rosyth Primary School | Rosyth Primary School | Rosyth Primary School |
| Bậc học của học sinh | Primary 1 | Primary 1 | Primary 2 (Ngoài kỳ) | Primary 1 | Primary 1 |
| Quốc tịch học sinh | Singapore Citizen | Singapore Citizen | Singapore Citizen | International Student | Singapore Citizen |
| Trạng thái Tài khoản EA | Đã có tài khoản EA | **Chưa có tài khoản EA** | Đã có tài khoản EA | Đã có tài khoản EA | Đã có tài khoản EA |
| Biểu phí Component tương ứng | Đã cấu hình ($100.00) | Đã cấu hình ($100.00) | Đã cấu hình ($100.00) | **Chưa cấu hình biểu giá** | Đã cấu hình (hết hạn trước kỳ) |
| **Kết Quả Preview & Publish** | | | | | |
| Xuất hiện trong danh sách Preview | **Có (100.00 SGD)** | **Có (100.00 SGD)** | **Không (Bị loại trừ)** | **Báo lỗi thiếu biểu giá** | **Bị chặn từ form tạo** |
| Cho phép Publish đợt phí | **Cho phép** | **Cho phép** | Không áp dụng | **Bị chặn xuất bản** | **Bị chặn khởi tạo** |
| Tạo bản ghi nợ Student Charge | **POSTED (100.00 SGD)**| **POSTED (100.00 SGD)**| Không sinh nợ | Không sinh nợ | Không sinh nợ |
| Tạo mới tài khoản EA ngoài ý muốn | **Không** | **Không (Giữ nguyên)**| Không | Không | Không |

---

### 1.4 Thuật Toán Tuần Tự Kiểm Thử Âm Tính & Bàn Giao (Deterministic Algorithm)

```text
BƯỚC 1: XÁC THỰC TIỀN ĐIỀU KIỆN (SETUP CONTEXT)
  1.1 IF thực hiện bằng MOE HQ THEN:
        Truy cập /support-console.
        Chọn Tab "School role (persona)" -> Chọn trường "Rosyth Primary School" -> Role "School Admin".
        Điền Reason = "Testing UAT Sprint 3 for Kent" (độ dài >= 10 ký tự).
        Điền Ticket reference = "UAT-KENT-01".
        Nhấn "Start View As".
        Xác nhận Header hiển thị "Thi H Bui | school" và Sidebar chuyển sang menu trường học.
      ELSE (Đăng nhập trực tiếp):
        Đăng nhập bằng tài khoản staff1@IAM.edu.vn qua Microsoft SSO.

BƯỚC 2: KHỞI TẠO BATCH DRAFT
  2.1 Truy cập /fee-management/components -> Chọn Component "Tuition Fee 2026" -> Nhấn "Publish batch from this Fee Component".
  2.2 Điền Title = "Rosyth P1 Tuition Batch 2026".
  2.3 Điền Period start = "2026-01-01", Period end = "2026-06-30", Due date = "2026-01-31".
  2.4 Để trống ô Schedule publish at.
  2.5 Chọn Targets: Schools = "Rosyth Primary School", Students = "All eligible students".
  2.6 Nhấn nút "Create draft".
  2.7 Xác nhận điều hướng sang /fee-batches/:batchId với nhãn trạng thái "Draft".

BƯỚC 3: KIỂM CHỨNG PREVIEW & NEGATIVE ORACLE (UAT-021 CORE)
  3.1 Tại mục "Student charge preview", chọn School = "Rosyth Primary School", tìm kiếm "Liam Pham".
  3.2 Xác nhận dòng hiển thị: Liam Pham (STU-00001), Primary 1, Singapore citizen, Expected Amount = SGD 100.00.
  3.3 Xác nhận hiển thị disclaimer: "Amounts shown are estimates from each student's saved pricing snapshot. Publishing rechecks eligibility and duplicate charges, so the final charges may differ."
  3.4 THỰC HIỆN NEGATIVE ASSERTIONS:
        a. Kiểm tra bảng Student Charges trong hệ thống: Số lượng bản ghi cho đợt này bằng 0.
        b. Kiểm tra ví Edusave của Liam Pham: Số dư giữ nguyên, không phát sinh giao dịch trừ tiền.
        c. Đăng nhập Cổng E-Service (https://eservice.20-255-158-192.sslip.io) bằng phụ huynh Pham Van Duc (S7654321B): Xác nhận danh sách nợ học phí chưa xuất hiện khoản thu mới này.

BƯỚC 4: XUẤT BẢN ĐỢT PHÍ & CHỐT CÔNG NỢ
  4.1 Tại trang chi tiết đợt phí /fee-batches/:batchId, nhấn nút "Publish".
  4.2 Xác nhận nhãn trạng thái Batch chuyển thành "Published" hoặc "Completed".
  4.3 Xác nhận bản ghi Student Charge chính thức được tạo:
        - Trạng thái: POSTED.
        - Số tiền: 100.00 SGD.
        - Học sinh: Liam Pham.
  4.4 Thực hiện Publish lặp lại (re-click): Xác nhận hệ thống không tạo thêm charge trùng lặp.

BƯỚC 5: KIỂM CHỨNG CỔNG PHỤ HUYNH & BÀN GIAO (HANDOFF)
  5.1 Phụ huynh Pham Van Duc (S7654321B) truy cập Cổng E-Service:
        Xác nhận hiển thị khoản nợ học phí 100.00 SGD của học sinh Liam Pham.
  5.2 Đóng gói biên bản bàn giao cho Gavin (UAT-PAR-01):
        Bao gồm Charge ID, Student Fixture Key (Liam Pham / STU-00001), Component Breakdown (Tuition Fee 100.00 SGD), Batch Publication ID.
```

---

## 2. Ma Trận Test Case 10 Cột Chuẩn (combo-qa / ISTQB Enforced)

| TC_ID | Module / Feature | Test Title / Objective | Preconditions | Test Data | Steps to Execute | Expected Observable Result | Technique | Suite | Priority |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `TC-VIEWAS-001` | Support Console | Verify successful View As activation as School Admin with valid audit fields [CONFIRMED] | User logged in with MOE HQ account `admin@IAM.edu.vn` | School: `Rosyth Primary School`, Role: `School Admin`, Reason: `Testing UAT Sprint 3 for Kent`, Ticket: `UAT-KENT-01` | 1. Navigate to `/support-console`.<br>2. Click tab 'School role (persona)'.<br>3. Search and select 'Rosyth Primary School', select role 'School Admin', click 'Select'.<br>4. Fill Reason and Ticket reference.<br>5. Click 'Start View As'. | Header updates to display 'Thi H Bui - school'; left sidebar replaces MOE menus with School menus including Classes, School config, Students, Fees, and FAS; URL redirects to `/dashboard` or `/support-console`. | EP | Smoke | P1 |
| `TC-VIEWAS-002` | Support Console | Verify Start View As button remains disabled when Reason has fewer than 10 characters [CONFIRMED] | User on `/support-console` with School and Role selected | Reason: `Short (9c)`, Ticket: `UAT-KENT-01` | 1. Select 'Rosyth Primary School' and 'School Admin' on tab 'School role (persona)'.<br>2. Enter Reason with exactly 9 characters.<br>3. Enter valid Ticket reference.<br>4. Inspect the 'Start View As' button state. | Button 'Start View As' has attribute 'disabled'; clicking the button produces no navigation and no HTTP request; character counter shows 9 characters. | BVA | Sprint | P2 |
| `TC-VIEWAS-003` | Support Console | Verify Start View As button activates immediately upon reaching 10-character boundary [CONFIRMED] | User on `/support-console` with School and Role selected | Reason: `1234567890` (10 chars), Ticket: `UAT-KENT-01` | 1. Select 'Rosyth Primary School' and 'School Admin'.<br>2. Enter Reason with exactly 10 characters.<br>3. Enter valid Ticket reference.<br>4. Inspect the 'Start View As' button state. | Button 'Start View As' removes attribute 'disabled'; button class changes to active blue style; element responds to click events. | BVA | Sprint | P2 |
| `TC-VIEWAS-004` | Support Console | Verify Start View As button remains disabled when Ticket reference is empty [CONFIRMED] | User on `/support-console` with School and Role selected | Reason: `Testing UAT Sprint 3 for Kent` (30 chars), Ticket: `""` (empty) | 1. Enter valid Reason with 30 characters.<br>2. Leave Ticket reference input blank.<br>3. Inspect the 'Start View As' button state. | Button 'Start View As' retains attribute 'disabled'; form submission is prevented. | EP | Sprint | P2 |
| `TC-BATCH-001` | Fee Batches | Verify direct navigation to create batch wizard without feeComponentId displays prerequisite warning [CONFIRMED] | User logged in with School Admin role | URL: `/fee-batches/new` (no query params) | 1. Navigate directly to `/fee-batches/new`.<br>2. Observe page banner and form interactivity. | Warning banner displays message: 'Fee component is required. Open this page from a fee component before creating a publication.'; form inputs and submit button are disabled or hidden. | EP | Smoke | P1 |
| `TC-BATCH-002` | Fee Batches | Verify entry navigation from Fee Component detail view passes component ID to Create Batch form [CONFIRMED] | Fee Component 'Tuition Fee 2026' exists with Active status and rate rules | Component ID: `CMP-2026-001` | 1. Navigate to `/fee-management/components`.<br>2. Open component `CMP-2026-001`.<br>3. Click button 'Publish batch from this Fee Component'. | Browser navigates to `/fee-batches/new?feeComponentId=CMP-2026-001`; page heading displays 'Create fee publication batch'; component selector shows 'Tuition Fee 2026' selected. | EP | Smoke | P1 |
| `TC-BATCH-003` | Fee Batches | Verify successful creation of Fee Publication Batch Draft with valid fields [CONFIRMED] | User on `/fee-batches/new?feeComponentId=CMP-2026-001` | Title: `Rosyth P1 Tuition Batch 2026`, Start: `2026-01-01`, End: `2026-06-30`, Due: `2026-01-31`, Schedule: empty, Targets: Rosyth Primary School / All eligible students | 1. Fill '#fee-publication-title'.<br>2. Fill '#fee-publication-period-start' and '#fee-publication-period-end'.<br>3. Fill '#fee-publication-due-date'.<br>4. Leave '#fee-publication-schedule-at' blank.<br>5. Select target schools and students.<br>6. Click button 'Create draft'. | API returns HTTP 201 Created; browser redirects to `/fee-batches/:batchId`; page renders batch status badge 'Draft'; batch details reflect title 'Rosyth P1 Tuition Batch 2026' and due date '2026-01-31'. | StateTransition | Smoke | P1 |
| `TC-BATCH-004` | Fee Batches | Verify Form validation blocks submission when Title, Period Start, or Due Date is empty [CONFIRMED] | User on `/fee-batches/new?feeComponentId=CMP-2026-001` | Title: `""`, Start: `""`, Due: `""` | 1. Leave mandatory fields blank.<br>2. Click button 'Create draft'. | Form submission blocked; inputs receive attribute `aria-invalid="true"`; validation error messages 'Title is required', 'Period start is required', and 'Due date is required' display below respective fields. | EP | Sprint | P2 |
| `TC-BATCH-005` | Fee Batches | Verify rejection when Period End date is earlier than Period Start date [CONFIRMED] | User on `/fee-batches/new?feeComponentId=CMP-2026-001` | Start: `2026-06-01`, End: `2026-01-01` | 1. Fill Title and valid Due date.<br>2. Set Period start to '2026-06-01'.<br>3. Set Period end to '2026-01-01'.<br>4. Click button 'Create draft'. | Submission blocked; element '#fee-publication-period-end' receives `aria-invalid="true"`; error text 'Period end date must be after period start date' displays. | BVA | Sprint | P1 |
| `TC-BATCH-006` | Fee Batches | Verify rejection when Period End equals Period Start under exclusive boundary rule [CONFIRMED] | User on `/fee-batches/new?feeComponentId=CMP-2026-001` | Start: `2026-01-01`, End: `2026-01-01` | 1. Fill Title and valid Due date.<br>2. Set Period start to '2026-01-01'.<br>3. Set Period end to '2026-01-01' (same day).<br>4. Click button 'Create draft'. | Submission blocked; inline validation error specifies 'Period end date must be strictly after period start date due to exclusive period definition'. | BVA | Sprint | P2 |
| `TC-BATCH-007` | Fee Batches | Verify rejection when Due Date is earlier than Period Start date [CONFIRMED] | User on `/fee-batches/new?feeComponentId=CMP-2026-001` | Start: `2026-02-01`, Due: `2026-01-15` | 1. Fill Title.<br>2. Set Period start to '2026-02-01'.<br>3. Set Due date to '2026-01-15'.<br>4. Click button 'Create draft'. | Submission blocked; input '#fee-publication-due-date' receives `aria-invalid="true"`; error text 'Due date must be on or after period start date' displays. | BVA | Sprint | P2 |
| `TC-BATCH-008` | Fee Batches | Verify acceptance when Due Date equals Period Start date on boundary [CONFIRMED] | User on `/fee-batches/new?feeComponentId=CMP-2026-001` | Start: `2026-01-01`, Due: `2026-01-01` | 1. Fill valid Title.<br>2. Set Period start to '2026-01-01'.<br>3. Set Due date to '2026-01-01'.<br>4. Click button 'Create draft'. | Form submission accepted; batch draft created successfully with Due date matching Period start date. | BVA | Sprint | P2 |
| `TC-BATCH-009` | Fee Batches | Verify Student Charge Preview displays accurate eligible student calculation [CONFIRMED] | Batch draft created for 'Tuition Fee 2026' (100.00 SGD for Primary 1 Citizen); Student Liam Pham enrolled in P1 at Rosyth Primary School | School: `Rosyth Primary School`, Search: `Liam Pham` (STU-00001 / S4744854C) | 1. Open batch details page `/fee-batches/:batchId`.<br>2. Scroll to 'Student charge preview' section.<br>3. Filter School to 'Rosyth Primary School' and search 'Liam Pham'. | Preview table displays row: Name 'Liam Pham', School 'Rosyth Primary School', Category 'Singapore citizen', Stage 'Primary 1', Expected Amount 'SGD 100.00'; disclaimer text 'Amounts shown are estimates from each student\'s saved pricing snapshot' is visible. | EP | Smoke | P1 |
| `TC-BATCH-010` | Fee Batches | Verify Negative Oracle that Preview strictly creates ZERO real charges in database [CONFIRMED] | System on `/fee-batches/:batchId` showing 100.00 SGD preview for Liam Pham; Parent account exists on E-Service | Student: `Liam Pham`, Parent: `Pham Van Duc` (`S7654321B`) | 1. Observe preview amount of 100.00 SGD on batch detail screen.<br>2. Query system Student Charges table for batch ID.<br>3. Inspect Liam Pham Edusave wallet balance.<br>4. Log in to Parent E-Service portal with parent NRIC `S7654321B`. | Database query returns 0 Student Charge records for this draft batch; Edusave wallet balance is unchanged (0.00 SGD); Parent E-Service portal displays 0 pending charges or invoices for Liam Pham. | EP | UAT | P1 |
| `TC-BATCH-011` | Fee Batches | Verify Preview includes eligible student who does not have an active EA account [CONFIRMED] | Student B is Singapore Citizen enrolled in P1 at Rosyth Primary School without an active Education Account (EA) | Student: `Eligible Student No-EA` | 1. Open preview table for the draft batch.<br>2. Search for Student B. | Student B is listed in preview table with Expected Amount 'SGD 100.00'; lack of EA does not exclude student from fee assessment. | EP | UAT | P2 |
| `TC-BATCH-012` | Fee Batches | Verify Preview excludes ineligible control student from another stage [CONFIRMED] | Student C is enrolled in Primary 2 at Rosyth Primary School (Component targets P1 only) | Student: `Student C (Primary 2)` | 1. Open preview table.<br>2. Search for Student C. | Preview table displays 'No students found matching the criteria'; Student C is excluded from preview. | EP | UAT | P2 |
| `TC-BATCH-013` | Fee Batches | Verify Publish Batch transitions state to Published and generates POSTED Student Charge [CONFIRMED] | Batch in 'Draft' state with valid preview of 100.00 SGD for Liam Pham | Batch ID: `<batchId>`, Student: `Liam Pham` | 1. On `/fee-batches/:batchId`, locate top-right action button 'Publish'.<br>2. Click 'Publish' button.<br>3. Confirm modal prompt if requested.<br>4. Inspect batch status badge and charges list. | Batch status badge updates to 'Published'; action button 'Publish' is hidden or disabled; system generates Student Charge record for Liam Pham with Status 'POSTED', Amount 'SGD 100.00', and valid Charge ID. | StateTransition | Smoke | P1 |
| `TC-BATCH-014` | Fee Batches | Verify publishing fees for no-EA student creates charge without generating unwanted EA [CONFIRMED] | Batch published containing Student B (eligible, no active EA) | Student: `Eligible Student No-EA` | 1. Publish batch containing Student B.<br>2. Inspect Student Charges for Student B.<br>3. Inspect Education Account register for Student B. | Student Charge for Student B is generated with status 'POSTED' and amount 'SGD 100.00'; Student B EA register shows 0 active EA accounts; system does not fabricate EA. | StateTransition | UAT | P2 |
| `TC-BATCH-015` | Fee Batches | Verify publish idempotency prevents duplicate charge generation on repeated requests [CONFIRMED] | Batch already published; Student Charge already exists for Liam Pham with amount 100.00 SGD | Batch ID: `<batchId>` | 1. Attempt to trigger publish action again via UI or direct API POST.<br>2. Query total count of Student Charges for Liam Pham under this batch. | System returns HTTP 400 Bad Request or 409 Conflict with message 'Batch is already published'; total count of Student Charges for Liam Pham remains exactly 1; no duplicate invoice created. | StateTransition | Regression | P1 |
| `TC-BATCH-016` | Fee Batches | Verify End-to-End Parent Portal exposure and audit handoff package generation [CONFIRMED] | Batch published; Student Charge POSTED for Liam Pham (STU-00001) | Parent: `Pham Van Duc` (`S7654321B`), Student: `Liam Pham` | 1. Navigate to Parent E-Service portal `https://eservice.20-255-158-192.sslip.io`.<br>2. Log in using mock Singpass with NRIC `S7654321B`.<br>3. Open 'Outstanding Fees / Payment' tab.<br>4. Verify bill amount and details.<br>5. Export Charge ID and audit evidence package for Gavin (UAT-PAR-01). | Parent portal displays outstanding fee of 'SGD 100.00' for child 'Liam Pham' under 'Tuition Fee 2026'; payment status shows 'Pending Payment'; audit receipt contains Charge ID, Student ID, Component breakdown, and Timestamp. | StateTransition | UAT | P1 |
| `TC-BATCH-017` | Fee Batches | Verify school isolation prevents School Admin from targeting other schools in publication [CONFIRMED] | User logged in as School Admin of Rosyth Primary School | School: `Rosyth Primary School` | 1. Navigate to `/fee-batches/new?feeComponentId=CMP-2026-001`.<br>2. Inspect 'Publication targets -> Schools' section. | School selector is locked to 'Rosyth Primary School' with disabled/readonly state; radio option to select other schools is disabled or hidden. | EP | Regression | P2 |

---

## 3. Bảng Phân Tích Rủi Ro & CIR Items (Clarification & Assurance Tags)

| Mã Tag | Phân Loại | Vị Trí Tham Chiếu | Nội Dung Giả Định & Quy Chuẩn Kiểm Thử | Tác Động Kiểm Thử |
| :--- | :--- | :--- | :--- | :--- |
| `[CONFIRMED: CF-01]` | `[CONFIRMED]` | Support Console `/support-console` | Ràng buộc Reason có độ dài tối thiểu 10 ký tự và bắt buộc Ticket reference được xác nhận 100% qua live DOM scan trên môi trường thực tế. | `TC-VIEWAS-002` và `TC-VIEWAS-003` kiểm tra ranh giới 9 vs 10 ký tự của Reason. |
| `[CONFIRMED: CF-02]` | `[CONFIRMED]` | Tạo Batch `/fee-batches/new` | Hệ thống bắt buộc phải có `feeComponentId` trên URL; nếu truy cập trực tiếp sẽ hiện cảnh báo yêu cầu mở từ màn hình Component. | `TC-BATCH-001` kiểm tra cảnh báo và trạng thái form bị khóa. |
| `[CONFIRMED: CF-03]` | `[CONFIRMED]` | UAT-021 Negative Oracle | Preview đợt phí chỉ hiển thị ước tính (estimate), tuyệt đối KHÔNG được tạo bản ghi nợ thật, KHÔNG đổi số dư ví Edusave, và KHÔNG hiển thị trên Cổng Phụ huynh trước khi bấm Publish. | `TC-BATCH-010` thực hiện kiểm chứng âm tính độc lập trên DB, Ví Edusave và Cổng E-Service. |
| `[CONFIRMED: CF-04]` | `[CONFIRMED]` | UAT-021 Chống trùng lặp (Anti-duplicate) | Sau khi Publish, việc lặp lại thao tác không được sinh khoản nợ kép cho cùng một học sinh và thành phần phí. | `TC-BATCH-015` kiểm tra tính Idempotent của tiến trình Publish. |
| `[ASSUMPTION: ASM-01]` | `[ASSUMPTION]` | Định dạng hiển thị tiền tệ | Số tiền công nợ học sinh luôn được hiển thị với tiền tệ `SGD` và định dạng 2 chữ số thập phân (e.g., `SGD 100.00`). | Kiểm tra định dạng trong `TC-BATCH-009`, `TC-BATCH-013`, và `TC-BATCH-016`. |
| `[CONFERENCE: CIR-01]` | `[CONFERENCE]` | Xử lý học sinh thiếu Rate Rule | Khi một học sinh đủ điều kiện trường/lớp nhưng rơi vào diện quốc tịch chưa có biểu giá trong Component: FSD quy định hệ thống báo lỗi missing-rate và chặn xuất bản cho đến khi biểu giá được bổ sung. Cần PO xác nhận thông báo lỗi chính xác trên UI. | Ghi nhận câu hỏi làm rõ CIR-01 cho PO/BA; tạm thời kiểm thử chặn xuất bản. |
