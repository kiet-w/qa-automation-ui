# Ma Trận Test Case: Quản Lý Thành Phần Phí & Biểu Phí (Fee Management & Rate Rules)

> **Mô đun**: `Fee Management` / `R03 Fee Configuration & Publication`  
> **Phạm vi giao diện**: 4 Màn hình (`/fee-management`, `/components/new`, `/rate-rules/new`, `/components/:feeComponentId`) & Cầu nối Sang Đợt Thu (`/fee-batches/new`)  
> **Tiêu chuẩn**: ISTQB Foundation / ISO/IEC/IEEE 29119-3 / combo-qa Standard  
> **Quy chuẩn**: Black-box Testing (Cấm đọc source code, bám sát Live DOM & Đặc tả nghiệp vụ)

---

## 1. Bóc Tách Thực Thể & Kiến Trúc Nghiệp Vụ

### 1.1 Bảng Phân Tích Thực Thể & Ràng Buộc Dữ Liệu (Data Dictionary & Constraints)

| Thực Thể | Trường Dữ Liệu | Kiểu / Format | Bắt Buộc | Ràng Buộc Kỹ Thuật | Ý Nghĩa Nghiệp Vụ |
| :--- | :--- | :--- | :---: | :--- | :--- |
| **Fee Component** | `name` (`#fee-component-name`) | String (1..150 chars) | Có | Trim whitespace; Không để trống | Tên định danh khoản thu (vd: Tuition Fee 2026) |
| | `fee_type` (`#fee-type`) | Combobox Value | Có | Phải tồn tại trong bảng Fee Types | Loại phí cha (vd: School Tuition Fee, Misc, Enrichment) |
| | `student_categories` (`#fee-categories`) | Multi-select Array | Có | Tối thiểu 1 phần tử (SC, PR, IS) | Nhóm học sinh áp dụng biểu phí |
| | `education_stages` (`#fee-stages`) | Multi-select Array | Có | Tối thiểu 1 phần tử (Primary, Secondary...) | Cấp bậc học áp dụng |
| | `tax_applies` (`#fee-tax`) | Boolean Checkbox | Không | Mặc định unchecked (`false`) | Cờ áp dụng thuế GST/VAT |
| **Fee Rate Rule** | `rate_mode` | Radio Button | Có | `fixed-amount` hoặc `config-fee-rate-rules` | Chế độ áp giá đồng loạt hoặc ma trận phân cấp |
| | `fixed_amount` (`input#fixed-amount`) | Decimal (10,2) | Có (khi Mode A) | $\ge 0.00$; Chấp nhận 0.00 (Miễn phí) | Số tiền đồng loạt cho tất cả các nhóm |
| | `matrix_rate` (`#rate-amount-<STAGE>:<CAT>`) | Decimal (10,2) | Có (khi Mode B) | $\ge 0.00$ cho từng ô ma trận tương ứng | Số tiền riêng cho từng cặp Cấp học $\times$ Đối tượng |
| | `currency` (`input#fixed-currency`) | String (ISO 4217) | Có | Mặc định `SGD`; Read-only/Disabled | Đơn vị tiền tệ thanh toán |
| | `effective_from` (`input#fixed-from`) | Date (`YYYY-MM-DD`) | Có | Ngày bắt đầu có hiệu lực | Mốc bắt đầu biểu giá được phép sử dụng |
| | `effective_to` (`input#fixed-to`) | Date (`YYYY-MM-DD`) | Có | `effective_to > effective_from` (Exclusive) | Mốc kết thúc (không tính ngày này) của biểu giá |

---

### 1.2 Ma Trận Chuyển Trạng Thái (State Transition Table)

| Trạng Thái Ban Đầu | Sự Kiện / Hành Động Trigger | Điều Kiện Guard | Trạng Thái Đích | Tác Động Phụ & Biểu Hiện UI |
| :--- | :--- | :--- | :--- | :--- |
| `[None]` | Truy cập `/fee-management/components/new` | Đã đăng nhập MOEHQ hoặc School User | `[Component Form: Pristine]` | Hiển thị Wizard Bước 1, các trường rỗng |
| `[Component Form: Pristine]` | Nhấn "Continue to rates" | Các trường bắt buộc bị bỏ trống | `[Component Form: Invalid]` | Kích hoạt `aria-invalid="true"`, hiển thị inline error |
| `[Component Form: Pristine]` | Điền đủ trường và nhấn "Continue to rates" | Name hợp lệ, chọn Fee Type, $\ge 1$ Category, $\ge 1$ Stage | `[Component: Draft / Pending Rates]` | Gửi `POST /v1/fees/fee-components`; trả về 201; redirect sang `/rate-rules/new?feeComponentId=<id>` |
| `[Component: Draft / Pending Rates]` | Chọn Mode A, điền Amount, điền Dates, nhấn "Save rates" | Amount $\ge 0.00$; `effective_to > effective_from` | `[Component: Active]` | Gửi `POST /v1/fees/fee-components/fee-rate-rules`; trả về 200; redirect sang `/components/:id`; Toast thành công |
| `[Component: Draft / Pending Rates]` | Chọn Mode B, điền đủ ô ma trận, điền Dates, nhấn "Save rates" | Mọi ô ma trận $\ge 0.00$; Dates hợp lệ | `[Component: Active]` | Tạo các bản ghi rate rules tương ứng từng cặp; redirect sang `/components/:id`; Badge status = Active |
| `[Component: Active]` | Nhấn "Publish batch from this Fee Component" | Component có status `Active` và có $\ge 1$ Rate Rule | `[Fee Batch: Create Flow]` | Điều hướng sang `/fee-batches/new?feeComponentId=<id>`; tự động điền Component tương ứng |

---

### 1.3 Bảng Quyết Định (Decision Table: Biểu Phí & Cấu Hình)

| Điều Kiện / Quy Tắc Nghiệp Vụ | R1 (Mode A - Standard) | R2 (Mode A - Zero Fee) | R3 (Mode B - Multi Tier) | R4 (Mode A - Inverted Dates) | R5 (Step 1 - Missing Field) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Tên Component & Fee Type hợp lệ | Có | Có | Có | Có | **Không (Bỏ trống)** |
| Nhóm Category & Stage được chọn | Có | Có | Có | Có | Không |
| Chế độ Biểu phí (Rate Mode) | Fixed Amount | Fixed Amount | Matrix Config | Fixed Amount | N/A |
| Mức phí Amount | $100.00 SGD | $0.00 SGD | $100 (SC) / $150 (PR) | $100.00 SGD | N/A |
| Hiệu lực Dates (`To > From`) | Hợp lệ (2026-01-01 -> 2026-12-31) | Hợp lệ (2026-01-01 -> 2026-12-31) | Hợp lệ (2026-01-01 -> 2026-12-31) | **Không (From > To)** | N/A |
| **Hành Động & Kết Quả Kỳ Vọng** | | | | | |
| Chuyển hướng sang Wizard Bước 2 | Có | Có | Có | Có | **Bị chặn lại Bước 1** |
| Hiển thị lỗi Validation trên Form | Không | Không | Không | **Lỗi Date Range** | **Lỗi Required Field** |
| Bản ghi Rate Rules được lưu | 1 rate áp cho mọi cặp | 1 rate 0đ áp cho mọi cặp | N rates theo từng ô ma trận | Không lưu DB | Không lưu DB |
| Trạng thái Component cuối cùng | `Active` | `Active` | `Active` | `Pending Rates` | `Chưa khởi tạo` |

---

### 1.4 Quy Tắc Phân Định 3 Cặp Ngày Tháng (Date Invariants & Boundary Matrix)

| Cặp Ngày Tháng | Vị Trí Xuất Hiện | Bản Chất Kỹ Thuật | Ràng Buộc Nghiệp Vụ Bất Biến | Hậu Quả Vi Phạm |
| :--- | :--- | :--- | :--- | :--- |
| **`Effective from` & `Effective to`** | Wizard Bước 2 (`/rate-rules/new`) | Vòng đời hiệu lực của Biểu giá (Price Catalog Validity) | • `Effective to` mang tính chất loại trừ (Exclusive).<br>• Bắt buộc: `Effective to > Effective from`. | Báo lỗi validation trên UI; không cho phép lưu biểu phí. |
| **`Period Start` & `Period End`** | Bước 5 (`/fee-batches/new`) | Khoảng thời gian tính học phí (Billing Period / Academic Term) | • Toàn bộ khoảng thời gian `[Period Start, Period End]` **bắt buộc phải nằm trọn vẹn** trong `[Effective from, Effective to)`. | Hệ thống từ chối phát hành Batch vì không tìm thấy biểu giá có hiệu lực bảo đảm. |
| **`Charge Date` & `Due Date`** | Bước 5 (`/fee-batches/new`) | Lịch biểu công nợ & Hạn thanh toán (Invoice & Payment Deadline) | • `Due Date >= Charge Date`.<br>• `Charge Date` là ngày sinh công nợ; `Due Date` là hạn chót trước khi tính quá hạn. | Báo lỗi kỳ hạn thanh toán không hợp lệ. |

---

## 2. Ma Trận Test Case 10 Cột Chuẩn (combo-qa / ISTQB Enforced)

| TC_ID | Module / Feature | Test Title / Objective | Preconditions | Test Data | Steps to Execute | Expected Observable Result | Technique | Suite | Priority |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `TC-FEE-001` | Fee Management | Verify Entry Path 1 direct URL access to Create Fee Component wizard | User logged in with MOEHQ or School Admin role | URL: `/fee-management/components/new` | 1. Navigate directly to `/fee-management/components/new`.<br>2. Observe page heading and form layout. | Page title displays 'EduFAMS - Admin Portal'; H1 heading 'Create fee component' is visible; form displays '#fee-component-name', '#fee-type', '#fee-categories', '#fee-stages', and '#fee-tax'. | EP | Smoke | P1 |
| `TC-FEE-002` | Fee Management | Verify Entry Path 2 navigation from Fee Types overview table to Create Fee Component | User logged in; Fee Types list has at least one active row 'School Tuition Fee' | Fee Type: 'School Tuition Fee' | 1. Navigate to `/fee-management`.<br>2. Locate row 'School Tuition Fee' and click 'View' button.<br>3. On fee type detail view, click 'Create fee component' link/button. | URL navigates to `/fee-management/components/new` or `/fee-management/fee-types/:id/components/new`; H1 heading 'Create fee component' is visible. | EP | Smoke | P1 |
| `TC-FEE-003` | Fee Management | Verify End-to-End Happy Path with Mode A Fixed Amount and publish batch navigation | User logged in; Fee Type 'School Tuition Fee' exists; Student categories and stages configured | Name: 'Tuition Fee 2026', Fee Type: 'School Tuition Fee', Categories: ['Singapore Citizen', 'Permanent Resident'], Stage: ['Primary'], Mode: 'fixed-amount', Amount: '100.00', From: '2026-01-01', To: '2026-12-31' | 1. Navigate to `/fee-management/components/new`.<br>2. Fill Name, select Fee Type, select Categories, select Stage, check Tax applies, click 'Continue to rates'.<br>3. On `/rate-rules/new`, select radio 'Fixed Amount', enter Amount '100.00', enter Effective from '2026-01-01', enter Effective to '2026-12-31', click 'Save rates'.<br>4. Observe detail page `/components/:feeComponentId` and click 'Publish batch from this Fee Component'. | Step 2 redirects to `/rate-rules/new?feeComponentId=<id>`.<br>Step 3 redirects to `/components/:id`; toast message 'Fee rate rules saved successfully' displays; Fee rate rules table shows Primary, Singapore Citizen, Permanent Resident with 100.00 SGD; Component status badge shows 'Active'.<br>Step 4 redirects to `/fee-batches/new?feeComponentId=<id>`. | StateTransition | Smoke | P1 |
| `TC-FEE-004` | Fee Management | Verify End-to-End Happy Path with Mode B Config Fee Rate Rules matrix configuration | User logged in; Category 'Singapore Citizen' and 'Permanent Resident' exist; Stage 'Primary' exists | Name: 'Multi-Rate Tuition 2026', Fee Type: 'School Tuition Fee', Stage: ['Primary'], Categories: ['Singapore Citizen', 'Permanent Resident'], Mode: 'config-fee-rate-rules', SC Rate: '100.00', PR Rate: '150.00', From: '2026-01-01', To: '2026-12-31' | 1. Navigate to `/fee-management/components/new`, fill details, click 'Continue to rates'.<br>2. On `/rate-rules/new`, select radio 'Config Fee Rate Rules'.<br>3. Enter '100.00' into '#rate-amount-PRIMARY:SC' and '150.00' into '#rate-amount-PRIMARY:PR'.<br>4. Enter Effective from '2026-01-01' and Effective to '2026-12-31'.<br>5. Click 'Save rates'. | System creates 2 discrete rate rules; redirects to component detail page; table displays Row 1: Primary x Singapore Citizen with 100.00 SGD and Row 2: Primary x Permanent Resident with 150.00 SGD; status badge is 'Active'. | StateTransition | Sprint | P1 |
| `TC-FEE-005` | Fee Management | Verify Step 1 persists Component and auto-appends generated ID to Step 2 URL query | User on Step 1 form `/fee-management/components/new` | Name: 'Enrichment Fee 2026', Fee Type: 'School Tuition Fee', Categories: ['Singapore Citizen'], Stage: ['Primary'] | 1. Fill valid mandatory fields on Step 1.<br>2. Click 'Continue to rates' button (`button[type="submit"]`).<br>3. Inspect URL and request network response. | API returns HTTP 201 Created with JSON `{ "id": "<generated_id>" }`; browser URL matches pattern `**/rate-rules/new*` containing parameter `feeComponentId=<generated_id>`. | EP | Sprint | P1 |
| `TC-FEE-006` | Fee Management | Verify Tax applies checkbox correctly flags GST/VAT applicability on Component | User on Step 1 form | Name: 'Taxable Enrichment 2026', Tax applies: checked (`true`) | 1. Fill required fields and check '#fee-tax'.<br>2. Submit to Step 2 and complete rate saving.<br>3. Inspect Component details screen. | Component details field 'Tax applies' displays 'Yes' (or checkmark icon); Tax badge is rendered as Active. | DecisionTable | Sprint | P2 |
| `TC-FEE-007` | Fee Management | Verify Currency input defaults to SGD and remains disabled/read-only in Wizard Step 2 | User has completed Step 1 and is on Wizard Step 2 `/rate-rules/new` | Mode: 'fixed-amount' | 1. Select radio 'Fixed Amount'.<br>2. Inspect DOM element `input#fixed-currency`.<br>3. Attempt to type another currency code (e.g. 'USD'). | Input `input#fixed-currency` has value 'SGD'; element has attribute 'disabled' or 'readonly'; typed input is rejected. | EP | Sprint | P2 |
| `TC-FEE-008` | Fee Management | Verify Component details screen renders accurate Fee Rate Rules table columns and values | Component created with 100.00 SGD rate rule valid from 2026-01-01 to 2026-12-31 | Component ID: `<feeComponentId>` | 1. Open `/components/<feeComponentId>`.<br>2. Inspect table headers and data cells in 'Fee rate rules' section. | Table renders columns: 'Education stage', 'Student category', 'Amount', 'Currency', 'Effective from', 'Effective to'; cell values match 'Primary', 'Singapore Citizen', '100.00', 'SGD', '2026-01-01', '2026-12-31'. | EP | Sprint | P1 |
| `TC-FEE-009` | Fee Management | Verify Publish batch button is visible and routes to Fee Batches wizard with feeComponentId | Component exists with 'Active' status and configured rate rules | Component ID: `CMP-2026-001` | 1. Open `/components/CMP-2026-001`.<br>2. Locate button 'Publish batch from this Fee Component' at top of page.<br>3. Click the button. | Browser navigates to `/fee-batches/new?feeComponentId=CMP-2026-001`; Fee Batches wizard displays with 'Tuition Fee 2026' pre-selected in component field. | EP | Sprint | P1 |
| `TC-FEE-010` | Fee Management | Verify Step 1 validation prevents submission when Component Name is empty | User on `/fee-management/components/new` | Name: `""` (empty string) | 1. Leave '#fee-component-name' blank.<br>2. Fill other fields with valid options.<br>3. Click 'Continue to rates'. | Form submission blocked; input '#fee-component-name' receives attribute `aria-invalid="true"`; inline error text 'Name is required' or 'Component name is required' appears below input. | EP | Sprint | P2 |
| `TC-FEE-011` | Fee Management | Verify Step 1 validation prevents submission when Fee Type is not selected | User on `/fee-management/components/new` | Fee Type: unselected | 1. Fill Name with 'Valid Name'.<br>2. Leave '#fee-type' unselected.<br>3. Click 'Continue to rates'. | Form submission blocked; element '#fee-type' receives `aria-invalid="true"`; error message 'Fee type is required' displays. | EP | Sprint | P2 |
| `TC-FEE-012` | Fee Management | Verify Step 1 validation prevents submission when Categories or Stages are empty | User on `/fee-management/components/new` | Categories: `[]`, Stages: `[]` | 1. Fill Name and Fee Type.<br>2. Leave '#fee-categories' and '#fee-stages' with 0 items selected.<br>3. Click 'Continue to rates'. | Submission blocked; focus shifts to first missing multi-select field; validation error 'Select at least one student category' and 'Select at least one education stage' display. | EP | Sprint | P2 |
| `TC-FEE-013` | Fee Management | Verify Step 2 Mode A minimum valid boundary for Amount accepts 0.00 SGD free tier | User on Step 2 `/rate-rules/new` | Mode: 'fixed-amount', Amount: '0.00', Dates: 2026-01-01 to 2026-12-31 | 1. Select 'Fixed Amount' radio.<br>2. Enter '0.00' into `input#fixed-amount`.<br>3. Enter valid dates and click 'Save rates'. | Form submission accepted; rate saved with 0.00 SGD; detail page displays amount '0.00 SGD' representing full fee waiver. | BVA | Regression | P2 |
| `TC-FEE-014` | Fee Management | Verify Step 2 Mode A rejection on negative Amount input | User on Step 2 `/rate-rules/new` | Mode: 'fixed-amount', Amount: '-1.00' | 1. Select 'Fixed Amount'.<br>2. Enter '-1.00' into `input#fixed-amount`.<br>3. Click 'Save rates'. | Form submission blocked; input `input#fixed-amount` has attribute `aria-invalid="true"`; error message 'Amount must be greater than or equal to 0' displays. | BVA | Regression | P2 |
| `TC-FEE-015` | Fee Management | Verify Step 2 Mode A rejection when Effective From is greater than Effective To | User on Step 2 `/rate-rules/new` | Effective From: '2026-12-31', Effective To: '2026-01-01' | 1. Select 'Fixed Amount' and enter valid amount '100.00'.<br>2. Enter Effective from '2026-12-31'.<br>3. Enter Effective to '2026-01-01'.<br>4. Click 'Save rates'. | Form submission blocked; date inputs receive `aria-invalid="true"`; inline error message 'Effective to date must be after Effective from date' displays. | BVA | Regression | P1 |
| `TC-FEE-016` | Fee Management | Verify Step 2 Mode A rejection when Effective From equals Effective To under exclusive rule | User on Step 2 `/rate-rules/new` | Effective From: '2026-06-01', Effective To: '2026-06-01' | 1. Select 'Fixed Amount' and enter valid amount '100.00'.<br>2. Enter Effective from '2026-06-01'.<br>3. Enter Effective to '2026-06-01' (same day).<br>4. Click 'Save rates'. | Form submission blocked; error message 'Effective to date must be strictly after Effective from date' displays due to exclusive end boundary. | BVA | Regression | P2 |
| `TC-FEE-017` | Fee Management | Verify Step 2 Mode B validation blocks submission when any matrix cell is left empty | User on Step 2 with 2 pairs (Primary x Citizen, Primary x PR) | Cell PRIMARY:SC: '100.00', Cell PRIMARY:PR: `""` (blank) | 1. Select radio 'Config Fee Rate Rules'.<br>2. Enter '100.00' into '#rate-amount-PRIMARY:SC'.<br>3. Leave '#rate-amount-PRIMARY:PR' blank.<br>4. Enter valid dates and click 'Save rates'. | Submission blocked; empty input '#rate-amount-PRIMARY:PR' receives focus and `aria-invalid="true"`; error message 'Rate amount is required for all configured pairs' displays. | EP | Regression | P2 |
| `TC-FEE-018` | Fee Management | Verify switching between Mode A and Mode B retains date inputs and resets active mode payload | User on Step 2 `/rate-rules/new` | Dates: 2026-01-01 to 2026-12-31 | 1. Select 'Fixed Amount', enter '100.00', enter dates.<br>2. Switch radio to 'Config Fee Rate Rules'.<br>3. Inspect date inputs and matrix input states. | Effective from and Effective to remain populated with '2026-01-01' and '2026-12-31'; matrix table becomes active; fixed amount input is hidden or disabled. | StateTransition | Regression | P3 |
| `TC-FEE-019` | Fee Management | Verify Component lifecycle status remains Draft when user navigates away before saving rates | User completed Step 1 creating component ID `CMP-ABORT-001` | Component ID: `CMP-ABORT-001` | 1. Complete Step 1 and arrive at `/rate-rules/new?feeComponentId=CMP-ABORT-001`.<br>2. Do not submit rates; click 'Back to list' or navigate to `/fee-management/components`.<br>3. Locate `CMP-ABORT-001` in components table. | Row `CMP-ABORT-001` has Rates count '0'; Status badge displays 'Draft' or 'Pending Rates'; 'Publish batch' action is disabled or hidden. | StateTransition | Regression | P2 |
| `TC-FEE-020` | Fee Management | Verify Date Semantics Invariant rejecting Fee Batch period outside Component effective range | Component effective range: 2026-01-01 to 2026-12-31 (exclusive) | Batch Period: 2026-06-01 to 2027-01-15 (exceeds 2026-12-31) | 1. On Component detail, click 'Publish batch from this Fee Component'.<br>2. In Fee Batch wizard, set Period Start '2026-06-01' and Period End '2027-01-15'.<br>3. Click Submit batch. | System rejects batch creation with error message 'Batch period must fall entirely within the fee component effective dates (2026-01-01 to 2026-12-31)'; no batch published. | DecisionTable | Regression | P1 |

---

## 3. Bảng Truy Vết Phân Hạng Rủi Ro & CIR Items (Clarification & Assurance Tags)

| Mã CIR / Tag | Phân Loại | Vị Trí Tham Chiếu | Nội Dung Làm Rõ / Giả Định Kỹ Thuật | Tác Động Kiểm Thử |
| :--- | :--- | :--- | :--- | :--- |
| `[ASSUMPTION: ASM-01]` | `[ASSUMPTION]` | Step 2 Currency Input | Tiền tệ mặc định là `SGD` và ở chế độ Read-only không cho phép sửa đổi vì hệ thống áp dụng cho các trường thuộc MOE Singapore. | `TC-FEE-007` kiểm tra thuộc tính `disabled` hoặc `readonly` của ô nhập `#fixed-currency`. |
| `[ASSUMPTION: ASM-02]` | `[ASSUMPTION]` | Step 2 Amount Precision | Định dạng số tiền biểu phí áp dụng chuẩn 2 chữ số thập phân (e.g. `100.00`). Giá trị `0.00` là hợp lệ để phục vụ học sinh diện học bổng / miễn giảm FAS 100%. | `TC-FEE-013` kiểm tra chấp nhận `0.00 SGD`. |
| `[CONFERENCE: CIR-01]` | `[CONFERENCE]` | Step 2 Effective To Semantics | FSD ghi nhận `Effective to (exclusive)`. Cần PO xác nhận: Nếu nhập `2026-12-31`, hệ thống hiểu ngày có hiệu lực cuối cùng là ngày `2026-12-30 23:59:59` hay bao gồm cả ngày `2026-12-31` khi đối chiếu với Batch Period? | Tạm thời kiểm thử theo chuẩn Exclusive: `Effective to` phải lớn hơn `Effective from` ít nhất 1 ngày (`TC-FEE-016`). |
| `[GENERAL: STD-01]` | `[GENERAL]` | Step 1 & Step 2 Form Validation | Toàn bộ các trường nhập liệu vi phạm validation bắt buộc phải kích hoạt thuộc tính trợ năng `aria-invalid="true"` và hiển thị inline error text theo chuẩn WAI-ARIA & ISTQB. | Áp dụng cho toàn bộ các ca kiểm thử từ `TC-FEE-010` đến `TC-FEE-017`. |
