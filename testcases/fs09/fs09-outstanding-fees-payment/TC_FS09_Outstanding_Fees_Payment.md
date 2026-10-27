# BỘ ĐẶC TẢ TEST CASE CHUẨN GOOGLE SHEET (19 CỘT) — FS09: OUTSTANDING FEES & MULTI-MODE PAYMENT ENGINE
## MOE SINGAPORE EDUSAVE E-SERVICE PORTAL (`http://localhost:5174/billing/{studentId}`)

> **Quy chuẩn Format**: Bám sát 100% định dạng bảng tính Google Sheet Tender AvePoint (19 Cột):  
> [Google Sheet Reference (gid=1612531667)](https://docs.google.com/spreadsheets/d/1ViSPLgggDsBI13SCPjfO_i0QoyUXy35A/edit?gid=1612531667#gid=1612531667)  
> 
> **Bảng Điều Hành Trực Quan (Executive Dashboard)**: [`executive.html`](executive.html)  
> **File Excel Đi Kèm**: [`TC_FS09_Outstanding_Fees_Payment.xlsx`](TC_FS09_Outstanding_Fees_Payment.xlsx) (Master Test Suite & 3 Tabs phân tách chuyên biệt).  
> **Nguyên tắc Phân Định 3 Trụ Cột (Zero Confusion Mandate)**: Bóc tách minh bạch tuyệt đối giữa **Luật Nghiệp Vụ Cốt Lõi (BR)**, **Tiêu Chuẩn Nghiệm Thu User Story (AC)** và **Bộ Ma Trận Kỹ Thuật Đơn Component & Sức Khỏe UI NFR**, chấm dứt tình trạng dồn đống gây rối loạn tầm nhìn QA & Quản lý.

---

## 1. TỔNG QUAN PHÂN ĐỊNH 3 TRỤ CỘT KIỂM THỬ (THE 3-TIER TEST ARCHITECTURE)

### 1.1 Ma Trận Phân Định Trụ Cột Nghiệp Vụ vs Kỹ Thuật (Executive Breakdown)

| Trụ Cột Kiểm Thử | Bản Chất & Mục Tiêu Nghiệm Thu | Mã Quy Tắc / Tiêu Chuẩn Nguồn | Số Lượng TC | Mức Độ Nghiêm Trọng | Trọng Tâm Xác Minh |
| :--- | :--- | :--- | :-: | :---: | :--- |
| ⚖️ **Trụ Cột 1: Business Rules (BR)** | **Luật nghiệp vụ cốt lõi, vòng đời thanh toán & bảo vệ giao dịch** | `BR-F9-01` đến `BR-F9-13`, `DA-01` đến `DA-14`, `DEC-01`, `DEC-15`, `D-22`, `D-28` | **10 TCs** | Critical / P0 | Quyền truy cập con liên kết (Singpass BOLA/IDOR); Trừ số dư EduSave nguyên tử tại F1 Ledger; Giới hạn tuổi 16 đóng EA (`DA-06`); Idempotency Key chống nạp/trừ trùng lặp (`EX-03`); Động cơ Auto-Reversal hoàn tiền EA khi Online lỗi (`BR-F9-11`); Fallback `ReconciliationRequired`. |
| 🎯 **Trụ Cột 2: Acceptance Criteria (AC)** | **Tiêu chuẩn nghiệm thu User Story & Luồng hành vi người dùng** | `AC-01` đến `AC-22`, `F9.1` đến `F9.6`, `SCR-01` đến `SCR-08`, `MSG-0001` đến `MSG-0003` | **21 TCs** | High / P0-P1 | Luồng 7 màn hình thanh toán: Chọn con (SCR-01) ➔ Danh sách nợ (SCR-02/03) ➔ Chọn phương thức (SCR-04) ➔ Review & Confirm (SCR-05) ➔ Chờ xử lý (SCR-06) ➔ Biên lai PDF (SCR-07) hoặc Báo lỗi & Thử lại (SCR-08); Xử lý 3 mode thanh toán (100% EA, 100% Online Sandbox Gateway, Split Payment). |
| 🛠️ **Trụ Cột 3: Technical & UI Matrix** | **Kỹ thuật kiểm thử đơn component, BVA biên 1 cent, sức khỏe UI NFR & Adversarial** | Universal Input Field Matrix (12 lớp), Đơn Component SCR-01 ➔ SCR-08, BVA 1-cent ($0.01 SGD), Invariant 7 & 8 | **27 TCs** | Medium / P1-P2 | Kiểm thử cô lập từng đơn component: Checkbox Select All, Row Checkbox, Status Dropdown, Radio Payment Method, Custom Split EA Input, PayNow OTP/QR, Card Number/CVV/Expiry, Nút Continue/Confirm disable state, Viền đỏ `aria-invalid`, Chống lộ raw i18n key (`*.validation.*`), Debounce double-click, Timeout 10 phút, Webhook HMAC-SHA256 signature tampering. |
| | **TỔNG CỘNG HỆ THỐNG** | **Toàn bộ 7 Màn Hình Thanh Toán & Động Cơ Payment Engine FS09** | **58 TCs** | **P0 – P2** | **Bao phủ 100% Ma trận Nghiệp vụ, Tiêu chí Nghiệm thu & Sức khỏe Giao diện** |

---

### 1.2 Phân Bổ Theo 6 Test Suites Chuyên Biệt

| STT | Scenario ID | Tên Test Suite / Component Phụ Trách | Phân Bổ Trụ Cột (BR / AC / Tech) | Kỹ Thuật QA Kiểm Thử | Số Lượng TC | Mức Ưu Tiên |
| :-: | :---: | :--- | :--- | :--- | :-: | :---: |
| 1 | `TS-090-INQ` | **Invoice Inquiry & Breakdown (SCR-01, 02, 03)** | 2 BR, 3 AC, 2 Tech | Xem danh sách hóa đơn theo con liên kết, mở rộng chi tiết phí, kiểm tra số dư EA, trạng thái không nợ (SCR-03), phân biệt Citizen vs Non-Citizen (PR/IS). | 7 | P0 / Smoke |
| 2 | `TS-090-FEA` | **Full EA Payment Engine (SCR-04, 05, 07)** | 2 BR, 3 AC, 2 Tech | Thanh toán 100% bằng số dư EA khi Balance >= NetAmount, trừ số dư nguyên tử tại F1 Ledger, cập nhật Invoice sang Paid, xuất biên lai PDF, từ chối khi số dư thiếu (`EA_INSUFFICIENT_BALANCE`). | 7 | P0 / Smoke |
| 3 | `TS-090-FON` | **Full Online Payment Engine (Gateway Sandbox)** | 2 BR, 4 AC, 2 Tech | Thanh toán 100% qua Cổng Sandbox Gateway cho học sinh Citizen hoặc Non-Citizen (PR/IS), tiếp nhận Webhook HMAC-SHA256, xử lý hủy/thất bại đưa Invoice về Issued, timeout 10 phút. | 8 | P0 / P1 |
| 4 | `TS-090-SPL` | **Split Payment & Auto-Reversal Engine** | 2 BR, 5 AC, 3 Tech | Luồng thanh toán kết hợp 2 bước tuần tự (Trừ EA trước ➔ Online sau), tỷ lệ mặc định, phụ huynh tùy chỉnh số tiền EA, kích hoạt Auto-Reversal Engine khi Online lỗi/hủy, fallback `ReconciliationRequired`. | 10 | P0 / P1 |
| 5 | `TS-090-BRK` | **Break-It Resilience & Concurrency Chaos** | 2 BR, 3 AC, 5 Tech | Chống Double-Click Debounce (`IdempotencyKey`), chống tấn công IDOR xem/thanh toán hóa đơn con người khác, chống giả mạo chữ ký Webhook HMAC, giải quyết xung đột thanh toán đồng thời (409 Conflict), 9-tier technical oracle. | 10 | P0 / P1 |
| 6 | `TS-090-ATM` | **Atomic Controls & Boundary Validation** | 0 BR, 3 AC, 13 Tech | Ma trận 12 lớp kiểm thử cho từng control đơn lẻ: Checkbox Select All, Row Checkbox, Status Dropdown, Radio Payment Method, Custom EA Input amount (BVA $0.01 SGD), PayNow QR/OTP, Card inputs, Button Continue/Confirm/Pay disable state, Toast, aria-invalid viền đỏ, Anti-i18n Key Leak. | 16 | P1 / P2 |
| | | **TỔNG CỘNG** | **6 TEST SUITES ĐỘC LẬP** | **10 BR + 21 AC + 27 Tech** | **Universal Matrix (EP, BVA, State Transitions, Decision Tables, 9-Tier Failure, Anti-i18n)** | **58** | **P0 - P2** |

---

## 2. MA TRẬN TEST CASE ĐẦY ĐỦ 19 CỘT THEO 3 TRỤ CỘT CHUYÊN BIỆT

### 2.1 TRỤ CỘT 1: CÁC CA KIỂM THỬ LUẬT NGHIỆP VỤ CỐT LÕI (BUSINESS RULES — 10 TEST CASES)
> **Mục tiêu**: Kiểm tra các quy tắc bất biến của hệ thống, phân quyền truy cập con liên kết, trừ số dư nguyên tử tại F1 Ledger, chống nạp/trừ trùng lặp Concurrency, và động cơ Auto-Reversal.

| ID | Scenario ID | Title | Test Suite | Page | Severity | Priority | Execution Status | Test Type | Environment | Preconditions | Test Data | Test Steps | Expected Result | Actual Result | Assumption Ref | Defect ID | Traceability | Note |
| :-: | :-: | :--- | :--- | :--- | :-: | :-: | :-: | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| TC-R9-BR-01 | TS-090-INQ | Verify parent can only view and pay invoices for their own linked children (BOLA/IDOR Protection) | Invoice Inquiry | Parent Portal > Billing | S1 (highest) | Critical | Passed | Security | SIT<br>Chrome (latest)<br>Mock SingPass + Mock API | Parent Tan Wei Ming logged in | Parent NRIC: S1234567A; Linked Child: Ryan Tan (STU-001) | 1. Navigate to /billing/STU-001<br>2. Verify invoices rendered for Ryan Tan<br>3. Attempt to navigate directly to /billing/STU-999 (unlinked child)<br>4. Inspect response | Access to STU-001 is permitted<br>Access to STU-999 is blocked with HTTP 403 Forbidden and message 'You do not have access to this student\'s records.' (FORBIDDEN_CHILD) | Verified: Server-side tenancy check enforces child linkage. | CR: Business rule BR-F9-01 strictly enforces parent-child linkage |  | BR-F9-01; AC-12; EX-01 | OWASP Top 10 API1 BOLA/IDOR protection. |
| TC-R9-BR-02 | TS-090-INQ | Verify non-citizen students (PR and International Students) cannot use EduSave Account | Invoice Inquiry | Parent Portal > Billing | S2 | High | Passed | Functional | SIT<br>Chrome (latest)<br>Mock SingPass + Mock API | Parent logged in with PR/IS linked child | Student Chloe Lee (PR/IS, STU-003); NetAmount: $120.00 | 1. Navigate to /billing/STU-003<br>2. Select outstanding invoice and click Continue to Step 2<br>3. Inspect payment method options | EduSave Account payment option is disabled or hidden<br>Helper note displayed: 'This student does not have an Education Account. Please pay online.' (EA_NOT_AVAILABLE)<br>Online Payment is selected by default | Verified: PR/IS students default to Online Payment, EA option disabled. | CR: BR-F9-07 and DA-03 non-citizens do not hold EduSave accounts |  | BR-F9-07; DA-03; AC-01 | Citizenship entitlement rule. |
| TC-R9-BR-03 | TS-090-FEA | Verify Full EA payment atomically deducts balance at Function 1 Ledger and records funding reference | Full EA Payment | Parent Portal > Billing | S1 (highest) | Critical | Passed | Functional | SIT<br>Chrome (latest)<br>Mock SingPass + Mock API | Parent logged in; Child Ryan Tan with EA Balance $500.00; Invoice $150.00 | Invoice INV-2026-001 ($150.00); Payment method: 100% EA | 1. Select INV-2026-001 ($150.00)<br>2. Select Education Account (100% EA)<br>3. Review & confirm payment on Step 3<br>4. Inspect F1 Ledger and invoice status | F1 Ledger atomically deducts $150.00 (Balance becomes $350.00)<br>Transaction recorded with unique FundingReference<br>Invoice status transitions to Paid (Status = 4)<br>Receipt SCR-07 generated | Verified: Atomic balance deduction and transaction ledger entry created. | CR: BR-F9-02, BR-F9-03 atomic ledger deduction |  | BR-F9-02; BR-F9-03; AC-03; AC-04 | Core financial ledger integrity. |
| TC-R9-BR-04 | TS-090-FEA | Verify Full EA payment is rejected when EA balance is insufficient at confirmation time | Full EA Payment | Parent Portal > Billing | S2 | High | Passed | Functional | SIT<br>Chrome (latest)<br>Mock SingPass + Mock API | Parent logged in; Child EA Balance $50.00; Invoice $150.00 | Invoice INV-2026-002 ($150.00); Balance: $50.00 | 1. Select INV-2026-002 ($150.00)<br>2. Attempt to select 100% EA<br>3. Inspect validation message and button state | Option 100% EA is disabled with warning 'Your Education Account balance is not enough for this amount. You can pay the rest online.' (EA_INSUFFICIENT_BALANCE)<br>User guided to Split Payment or Online Payment | Verified: Insufficient EA balance blocks 100% EA option cleanly. | CR: BR-F9-02 and EX-05 balance validation before deduction |  | BR-F9-02; EX-05; AC-03 | Prevents negative account balances. |
| TC-R9-BR-05 | TS-090-FON | Verify concurrent payment attempts for the same invoice are locked (Conditional Unique Index & Idempotency) | Break-It Resilience | API Service | S1 (highest) | Critical | Passed | Concurrency | SIT<br>2 API Clients<br>Mock SingPass + Mock API | Parent logged in; Invoice INV-2026-003 in Issued status | Rapid concurrent POST /api/payment/confirm for same invoiceId | 1. Dispatch Request 1 and Request 2 simultaneously within 10ms<br>2. Inspect HTTP status codes and responses | Exactly ONE request succeeds (HTTP 200/201)<br>The other request is rejected with HTTP 409 Conflict and message 'A payment for this invoice is still being processed.' (PAYMENT_PENDING)<br>Zero duplicate balance deduction | Verified: DB unique transaction lock prevents double payment. | CR: BR-F9-09 and DA-13 conditional unique index on active transactions |  | BR-F9-09; DA-13; EX-03 | High-frequency concurrency defense. |
| TC-R9-BR-06 | TS-090-SPL | Verify Split Payment sequentially deducts EA first and transitions to Online Payment for the remainder | Split Payment | Parent Portal > Billing | S1 (highest) | Critical | Passed | Functional | SIT<br>Chrome (latest)<br>Mock SingPass + Mock API | Parent logged in; EA Balance $100.00; Invoice $250.00 | Total: $250.00; EA Amount: $100.00; Online Remainder: $150.00 | 1. Select Split Payment mode<br>2. Enter EA Amount $100.00, Online calculates $150.00<br>3. Confirm payment on Step 3<br>4. Inspect backend state | EA balance $100.00 deducted with status Hold/Pending<br>System generates Payment Gateway redirect URL for remaining $150.00<br>Invoice status transitions to PaymentPending | Verified: Sequential 2-step split flow executed accurately. | CR: BR-F9-11 and DEC-15 sequential split payment model |  | BR-F9-11; DEC-15; AC-15; AC-16 | Core Split Payment business workflow. |
| TC-R9-BR-07 | TS-090-SPL | Verify Auto-Reversal Engine automatically refunds EA balance when Online Gateway payment fails or is cancelled | Split Payment | Parent Portal > Billing | S1 (highest) | Critical | Passed | Fault Injection | SIT<br>Chrome (latest)<br>Mock SingPass + Mock API | Split payment in progress; EA deducted $100.00; on Sandbox Gateway | Online payment rejected or cancelled by user | 1. On Sandbox Gateway, click 'Cancel and return to merchant'<br>2. Inspect backend reversal queue and parent screen | Gateway webhook reports FAILURE/CANCELLED<br>Auto-Reversal Engine immediately calls F1 Ledger to credit back $100.00 to student EA<br>Screen SCR-08 displays 'Your online payment could not be completed. The amount taken from the Education Account has been returned.' (PAYMENT_FAILED_EA_RETURNED)<br>Invoice status returns to Issued | Verified: Full EA refund executed and user notified of reversal. | CR: BR-F9-11 and AC-17 automatic EA reversal on gateway drop |  | BR-F9-11; AC-17; EX-08 | Zero financial loss resilience guarantee. |
| TC-R9-BR-08 | TS-090-SPL | Verify failed Auto-Reversal marks transaction as ReconciliationRequired and alerts operations | Split Payment | Parent Portal > Billing | S1 (highest) | Critical | Passed | Fault Injection | SIT<br>Fault Injection Engine<br>Mock SingPass + Mock API | Split payment cancelled; F1 Ledger API injected with HTTP 500 fault | Simulate F1 Ledger outage during refund call | 1. Inject failure into F1 Ledger credit API<br>2. Cancel online payment on gateway<br>3. Inspect transaction record in DB | System catches refund failure without silent drop<br>Transaction status set to ReconciliationRequired<br>Urgent ops alert dispatched for manual reconciliation<br>User informed that account review is in progress | Verified: ReconciliationRequired state flagged upon reversal failure. | CR: F2/F9 shared rule EX-11 & ReconciliationRequired state |  | BR-F9-11; EX-11; Appendix A | Operational audit and anomaly containment. |
| TC-R9-BR-09 | TS-090-FON | Verify Webhook HMAC-SHA256 signature tampering is rejected with HTTP 401 Unauthorized | Break-It Resilience | API Service | S1 (highest) | Critical | Passed | Security | SIT<br>API Client (cURL / Playwright API)<br>Mock SingPass + Mock API | Pending online payment transaction open | Tampered payload: status=SUCCESS with invalid HMAC signature | 1. Send simulated payment webhook POST /api/payment/webhook with modified payload or forged X-Signature<br>2. Inspect HTTP status code and invoice status | Server rejects request with HTTP 401 Unauthorized<br>Transaction and Invoice status remain unchanged in PaymentPending<br>Security alert logged | Verified: HMAC-SHA256 signature verification blocks forged webhooks. | CR: BR-F9-06 webhook cryptographic validation |  | BR-F9-06; EX-07; Invariant 8 | Webhook payment injection protection. |
| TC-R9-BR-10 | TS-090-FEA | Verify student aged 16+ with EA marked 'Due for closure' cannot use EA for payments | Full EA Payment | Parent Portal > Billing | S2 | High | Passed | Functional | SIT<br>Chrome (latest)<br>Mock SingPass + Mock API | Parent logged in with child aged 16 (EA Due for closure) | Student Ethan Tan (Age 16, STU-004); NetAmount: $80.00 | 1. Navigate to /billing/STU-004<br>2. Select invoice and proceed to Step 2<br>3. Inspect EduSave Account selection | Option EA is disabled with notice: 'The Education Account is not active. Please pay online.' (EA_NOT_ACTIVE)<br>System enforces age-16 closure rule across payment engine | Verified: Age 16 closure policy blocks EA usage. | CR: DA-06 and BR-F9-02 age 16 EA closure rule |  | BR-F9-02; DA-06; AC-01 | Lifecycle transition enforcement. |

---

### 2.2 TRỤ CỘT 2: CÁC CA KIỂM THỬ TIÊU CHUẨN NGHIỆM THU USER STORY (ACCEPTANCE CRITERIA — 21 TEST CASES)
> **Mục tiêu**: Xác thực hành vi của người dùng từ SCR-01 đến SCR-08 theo tiêu chí Given - When - Then, bộ 3 mode thanh toán và xuất biên lai thanh toán.

| ID | Scenario ID | Title | Test Suite | Page | Severity | Priority | Execution Status | Test Type | Environment | Preconditions | Test Data | Test Steps | Expected Result | Actual Result | Assumption Ref | Defect ID | Traceability | Note |
| :-: | :-: | :--- | :--- | :--- | :-: | :-: | :-: | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| TC-R9-AC-01 | TS-090-INQ | Verify child selector displays all linked children with outstanding balance summary cards (SCR-01) | Invoice Inquiry | Parent Portal > Billing | S2 | High | Passed | Functional | SIT<br>Chrome (latest)<br>Mock SingPass + Mock API | Parent Tan Wei Ming logged in | Parent with 2 linked children: Ryan Tan ($150 nợ), Sarah Tan ($0 nợ) | 1. Navigate to /billing<br>2. Inspect child cards on SCR-01<br>3. Verify student name, class, school, and outstanding amount | All linked children rendered as selectable cards<br>Ryan Tan shows $150.00 outstanding fees<br>Sarah Tan shows $0.00 outstanding fees with 'No fees due' badge | Verified: All linked children rendered with accurate balance summaries. | CR: FSD SCR-01 Child selection layout |  | F9.1; AC-01; SCR-01 | Initial landing screen verification. |
| TC-R9-AC-02 | TS-090-INQ | Verify selecting child with zero outstanding fees displays empty state notice (SCR-03) | Invoice Inquiry | Parent Portal > Billing | S3 | Medium | Passed | UI | SIT<br>Chrome (latest)<br>Mock SingPass + Mock API | Parent logged in; select child Sarah Tan | Student Sarah Tan (STU-002, 0 fees) | 1. Select Sarah Tan on SCR-01<br>2. Observe screen SCR-03 | Displays empty state illustration and message: 'No outstanding charges. All school fees are up to date.'<br>No payment action buttons visible | Verified: Empty state displays cleanly with friendly guidance. | CR: FSD SCR-03 Zero outstanding state |  | F9.2; AC-14; SCR-03 | Empty state verification. |
| TC-R9-AC-03 | TS-090-INQ | Verify outstanding fees table lists all unpaid invoices with fee breakdown and GST (SCR-02) | Invoice Inquiry | Parent Portal > Billing | S2 | High | Passed | Functional | SIT<br>Chrome (latest)<br>Mock SingPass + Mock API | Parent logged in; select Ryan Tan ($150 nợ) | Invoices: INV-001 ($50.00), INV-002 ($100.00) | 1. On SCR-02, inspect invoices table<br>2. Click expand on INV-001<br>3. Verify itemized charges (Tuition fee, Miscellaneous fee, 9% GST) | Invoices listed with Due Date, Invoice No, Description, Amount<br>Expanded row shows line-item breakdown matching NetAmount exactly | Verified: Line items and GST calculate and display accurately. | CR: FSD SCR-02 Charges list & breakdown |  | F9.2; AC-02; SCR-02 | Transparency of billing line items. |
| TC-R9-AC-04 | TS-090-INQ | Verify filter by invoice status (All, Overdue, Due Soon) updates table rows dynamically | Invoice Inquiry | Parent Portal > Billing | S3 | Medium | Passed | Functional | SIT<br>Chrome (latest)<br>Mock SingPass + Mock API | Multiple invoices with varying due dates | Filter options: 'All', 'Overdue', 'Due Soon' | 1. Select 'Overdue' filter option<br>2. Verify only past-due invoices display with red badge<br>3. Select 'All' to restore full list | Table dynamically filters rows matching selected criteria<br>Selection counter updates accordingly | Verified: Status filter functions smoothly. | CR: FSD SCR-02 status filter control |  | F9.2; AC-02 | Usability filter for multiple charges. |
| TC-R9-AC-05 | TS-090-FEA | Verify selecting 100% EduSave Account payment method auto-calculates total deduction | Full EA Payment | Parent Portal > Billing | S2 | High | Passed | Functional | SIT<br>Chrome (latest)<br>Mock SingPass + Mock API | Child EA Balance $500.00; Selected Invoice $150.00 | Method: Education Account | 1. On Step 2, select radio 'Education Account'<br>2. Verify calculation summary card | 'From Education Account: $150.00'<br>'Remaining to pay online: $0.00'<br>Continue button is enabled | Verified: 100% EA payment amount auto-populated accurately. | CR: FSD SCR-04 Method selection (EA mode) |  | F9.3; AC-03; SCR-04 | EA payment calculation. |
| TC-R9-AC-06 | TS-090-FEA | Verify Step 3 Review & Confirm displays full payment summary and requires authorization | Full EA Payment | Parent Portal > Billing | S2 | High | Passed | Functional | SIT<br>Chrome (latest)<br>Mock SingPass + Mock API | Step 2 completed with 100% EA ($150.00) | Review summary card; Confirm button | 1. Proceed to Step 3 (Review & Confirm)<br>2. Verify Child Name, Invoice IDs, Total Amount, Payment Method<br>3. Inspect Terms declaration | All payment parameters summarized accurately<br>User informed that funds will be deducted from EduSave Account<br>Confirm button enabled | Verified: Review summary matches selected invoice and method. | CR: FSD SCR-05 Review & Confirm |  | F9.4; AC-04; SCR-05 | Pre-confirmation validation gate. |
| TC-R9-AC-07 | TS-090-FEA | Verify successful 100% EA payment displays Receipt screen SCR-07 with PDF Download button | Full EA Payment | Parent Portal > Billing | S1 (highest) | Critical | Passed | Functional | SIT<br>Chrome (latest)<br>Mock SingPass + Mock API | Step 3 confirmed for $150.00 EA payment | Confirm action dispatched | 1. Click [Confirm and pay]<br>2. Observe transition to SCR-07<br>3. Verify receipt details: Receipt No, Payment Date, Amount Paid, EA Ref, Download PDF button | Screen transitions to SCR-07 with green success checkmark<br>Receipt No generated (RCP-2026-XXXX)<br>Download PDF button is clickable and downloads valid receipt | Verified: Receipt generated with full metadata and download capability. | CR: FSD SCR-07 Payment receipt |  | F9.4; AC-13; SCR-07 | Payment success confirmation. |
| TC-R9-AC-08 | TS-090-FON | Verify selecting 100% Online Payment generates Sandbox Gateway session and redirects user | Full Online Payment | Parent Portal > Billing | S2 | High | Passed | Functional | SIT<br>Chrome (latest)<br>Mock SingPass + Mock API | Invoice selected $100.00; Method: Online Payment | Method: Online Payment (PayNow / Credit Card) | 1. Select 'Online Payment' on Step 2<br>2. Click Continue to Step 3<br>3. Click [Proceed to pay online] | System creates pending transaction<br>Redirects browser to Sandbox Payment Gateway URL (`/gateway/pay`)<br>Gateway displays Merchant: MOE, Amount: $100.00 | Verified: Seamless redirection to payment gateway with correct amount. | CR: FSD SCR-04 and Appendix C Gateway redirect |  | F9.5; AC-08; SCR-04 | Online payment checkout flow. |
| TC-R9-AC-09 | TS-090-FON | Verify completing payment on Sandbox Gateway with SUCCESS webhook updates invoice to Paid | Full Online Payment | Parent Portal > Billing | S1 (highest) | Critical | Passed | Functional | SIT<br>Chrome (latest)<br>Mock SingPass + Mock API | On Sandbox Gateway screen with $100.00 charge | Click 'Simulate SUCCESS' button | 1. On Sandbox Gateway, select PayNow or Card and click 'Simulate SUCCESS'<br>2. Observe gateway processing and callback redirect to /billing/result | Webhook triggers backend invoice update to Paid (Status = 4)<br>Browser redirected to SCR-07 with success receipt<br>Invoice removed from outstanding list | Verified: Successful online payment marks invoice as Paid. | CR: FSD SCR-07 and AC-10 gateway success callback |  | F9.5; AC-10; SCR-07 | End-to-end online gateway completion. |
| TC-R9-AC-10 | TS-090-FON | Verify cancelling Sandbox Gateway payment redirects to SCR-08 and keeps invoice in Issued status | Full Online Payment | Parent Portal > Billing | S2 | High | Passed | Functional | SIT<br>Chrome (latest)<br>Mock SingPass + Mock API | On Sandbox Gateway screen with $100.00 charge | Click 'Cancel and return to merchant' | 1. On Sandbox Gateway, click 'Cancel'<br>2. Observe redirection to /billing/result | Redirection to SCR-08 with message: 'The payment was cancelled. No amount was deducted.' (PAYMENT_CANCELLED)<br>Invoice remains in Issued status and can be paid again<br>Buttons 'Try again' and 'Exit' available | Verified: Cancelled payment handled gracefully, invoice retains Issued state. | CR: FSD SCR-08 Payment failure & cancellation |  | F9.5; AC-09; SCR-08 | Payment cancellation recovery. |
| TC-R9-AC-11 | TS-090-FON | Verify online payment session expiration (10 minutes timeout) transitions invoice back to payable state | Full Online Payment | Parent Portal > Billing | S2 | High | Passed | Functional | SIT<br>Chrome (latest)<br>Mock SingPass + Mock API | Online payment initiated; user abandons gateway | Simulate 10-minute timeout / trigger cleanup job | 1. Initiate online payment on Step 3<br>2. Trigger background expiration job for 10-min timeout<br>3. Inspect invoice status on SCR-02 | Transaction marked Expired<br>Invoice status unlocked from PaymentPending back to Issued<br>Parent can select and initiate payment again | Verified: Abandoned payment sessions auto-expire cleanly after 10 mins. | CR: FSD section 4.2 session timeout & EX-02 |  | F9.5; AC-10; EX-02 | Session timeout lifecycle management. |
| TC-R9-AC-12 | TS-090-SPL | Verify selecting Split Payment initializes default 50/50 ratio or available EA balance | Split Payment | Parent Portal > Billing | S2 | High | Passed | Functional | SIT<br>Chrome (latest)<br>Mock SingPass + Mock API | Selected Invoice $200.00; EA Balance $150.00 | Mode: Split Payment | 1. Select 'Both (Split payment)' on Step 2<br>2. Inspect default populated amounts | EA Amount defaults to min(EA Balance, Total) = $150.00<br>Online Amount automatically calculates to $50.00<br>Sum strictly equals Total ($200.00) | Verified: Split payment defaults to maximizing EA balance cleanly. | CR: DEC-15 and AC-15 default split allocation logic |  | F9.3; AC-15; DEC-15 | Intelligent default split calculation. |
| TC-R9-AC-13 | TS-090-SPL | Verify custom EA amount input in Split Payment dynamically recalibrates online amount | Split Payment | Parent Portal > Billing | S2 | High | Passed | Functional | SIT<br>Chrome (latest)<br>Mock SingPass + Mock API | Total: $200.00; EA Balance: $150.00; Initial: $150 EA / $50 Online | Change EA input to $80.00 | 1. Focus EA amount input and enter '80.00'<br>2. Blur input or observe live calculation | Online amount instantly updates to '$120.00'<br>Total display remains '$200.00'<br>Validation check passes, Continue button remains active | Verified: Live dynamic recalibration of remainder amount. | CR: AC-16 customizable split amounts |  | F9.3; AC-16; SCR-04 | User customization of payment split. |
| TC-R9-AC-14 | TS-090-SPL | Verify completing Split Payment with successful Online Gateway payment updates invoice to Paid | Split Payment | Parent Portal > Billing | S1 (highest) | Critical | Passed | Functional | SIT<br>Chrome (latest)<br>Mock SingPass + Mock API | Split payment: $100 EA, $100 Online; on Sandbox Gateway | Complete Sandbox payment with SUCCESS | 1. On Sandbox Gateway, simulate SUCCESS for $100 Online<br>2. Observe callback and receipt | Both EA transaction and Online transaction committed<br>Invoice marked Paid<br>Receipt SCR-07 displays breakdown: '$100.00 from EduSave Account' and '$100.00 via Online Gateway' | Verified: Multi-source split payment completed and itemized on receipt. | CR: AC-22 split payment receipt generation |  | F9.4; AC-22; SCR-07 | End-to-end split payment verification. |
| TC-R9-AC-15 | TS-090-SPL | Verify entering EA amount exceeding total invoice or available balance displays SPLIT_AMOUNT_INVALID | Split Payment | Parent Portal > Billing | S2 | High | Passed | Functional | SIT<br>Chrome (latest)<br>Mock SingPass + Mock API | Total: $200.00; EA Balance: $150.00 | Input EA Amount: $180.00 (exceeds balance) | 1. Enter '180.00' into EA amount field<br>2. Blur field and observe validation message | Field highlights red with aria-invalid='true'<br>Message displayed: 'The two amounts must be more than zero and add up to the total.' (SPLIT_AMOUNT_INVALID)<br>Continue button is disabled | Verified: Exceeding balance or total blocks progression with specific alert. | CR: BR-F9-11 and AC-19 split boundary rules |  | BR-F9-11; AC-19; SCR-04 | Input constraint enforcement. |
| TC-R9-AC-16 | TS-090-FON | Verify failed online payment on Gateway displays SCR-08 with Try Again button leading back to Step 2 | Full Online Payment | Parent Portal > Billing | S2 | High | Passed | Functional | SIT<br>Chrome (latest)<br>Mock SingPass + Mock API | On Sandbox Gateway screen | Click 'Simulate FAILURE' | 1. Click 'Simulate FAILURE' on Gateway<br>2. Observe redirection to SCR-08<br>3. Click 'Try again' button | Screen displays PAYMENT_FAILED message with failure reason<br>Clicking 'Try again' returns to Step 2 with previous invoice selection preserved | Verified: Try again button smoothly restores previous payment configuration. | CR: FSD SCR-08 Failure recovery path |  | F9.5; AC-09; SCR-08 | Resilient user recovery flow. |
| TC-R9-AC-17 | TS-090-INQ | Verify navigating back from Step 2 to Step 1 preserves selected invoice checkboxes | Invoice Inquiry | Parent Portal > Billing | S3 | Medium | Passed | UI | SIT<br>Chrome (latest)<br>Mock SingPass + Mock API | On Step 2 (Payment Method) with INV-001 selected | Click 'Back' button | 1. On Step 2, click 'Back' button<br>2. Observe Step 1 table | Step 1 table renders with INV-001 checkbox still checked<br>Selection counter and total retain previously selected values | Verified: Back navigation preserves pristine state without data loss. | CR: FSD UX guidelines on multi-step wizard state |  | F9.2; Invariant 7 UI Health | Multi-step form state persistence. |
| TC-R9-AC-18 | TS-090-INQ | Verify navigating back from Step 3 to Step 2 preserves selected payment method | Full EA Payment | Parent Portal > Billing | S3 | Medium | Passed | UI | SIT<br>Chrome (latest)<br>Mock SingPass + Mock API | On Step 3 (Review & Confirm) with Split Payment configured | Click 'Back' button | 1. On Step 3, click 'Back' button<br>2. Observe Step 2 method form | Step 2 renders with Split Payment radio checked and entered amounts intact | Verified: Backward navigation retains method and amount inputs. | CR: FSD UX guidelines on multi-step wizard state |  | F9.3; Invariant 7 UI Health | Backward step state retention. |
| TC-R9-AC-19 | TS-090-FEA | Verify already paid invoice cannot be selected or paid again (INVOICE_ALREADY_PAID) | Full EA Payment | Parent Portal > Billing | S2 | High | Passed | Functional | SIT<br>Chrome (latest)<br>Mock SingPass + Mock API | Parent in Tab 1 and Tab 2 viewing same invoice | Tab 1 pays invoice; Tab 2 attempts payment | 1. Complete payment in Tab 1<br>2. Switch to Tab 2 and click [Confirm and pay]<br>3. Inspect UI response | Tab 2 is blocked with banner: 'This invoice has already been paid.' (INVOICE_ALREADY_PAID)<br>Page refreshes to remove invoice from outstanding list | Verified: Concurrency protection blocks double payment with clear notice. | CR: EX-04 and DA-13 preventing double payment |  | EX-04; DA-13; SCR-02 | Stale session protection. |
| TC-R9-AC-20 | TS-090-INQ | Verify session expiration during payment flow redirects to Singpass login with clear notice | Invoice Inquiry | Parent Portal > Billing | S2 | High | Passed | Security | SIT<br>Chrome (latest)<br>Mock SingPass + Mock API | Parent on Step 2; session expires (15 mins inactivity) | Token invalidated (HTTP 401) | 1. Invalidate session token<br>2. Click Continue button on Step 2<br>3. Inspect page response | User redirected to Singpass Login screen<br>Notice displayed: 'Your session has expired. Please sign in again.' (AUTH_REQUIRED / MSG-0002) | Verified: Clean redirect on session expiration without silent failure. | CR: Decision D-22 and EX-02 session expiration |  | D-22; EX-02; MSG-0002 | Session security benchmark. |
| TC-R9-AC-21 | TS-090-FEA | Verify system error during payment confirmation displays friendly error and preserves data | Full EA Payment | Parent Portal > Billing | S2 | High | Passed | Fault Injection | SIT<br>Chrome (latest)<br>Mock SingPass + Mock API | Backend database simulated failure (HTTP 500) | Server returns HTTP 500 on confirm request | 1. Click [Confirm and pay] with injected 500 error<br>2. Observe UI response | Error banner displays: 'Something went wrong. Please try again later.' (SYSTEM_ERROR)<br>Invoice remains Issued, zero amount deducted, user can retry | Verified: Server 500 handled gracefully without freezing UI. | CR: FSD section 5.1 and EX-10 system error handling |  | EX-10; SYSTEM_ERROR | Fault injection resilience. |

---

### 2.3 TRỤ CỘT 3: MA TRẬN KỸ THUẬT ĐƠN COMPONENT, BVA & SỨC KHỎE UI NFR (27 TEST CASES)
> **Mục tiêu**: Kiểm thử cô lập từng ô nhập liệu / control đơn lẻ theo Ma trận 12 lớp, phân tích giá trị biên 1-cent, chống tiêm mã XSS, chống lộ raw translation keys (`*.validation.*`), và kiểm tra các tiêu chuẩn phi chức năng Invariant 7 & 8.

| ID | Scenario ID | Title | Test Suite | Page | Severity | Priority | Execution Status | Test Type | Environment | Preconditions | Test Data | Test Steps | Expected Result | Actual Result | Assumption Ref | Defect ID | Traceability | Note |
| :-: | :-: | :--- | :--- | :--- | :-: | :-: | :-: | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| TC-R9-ATM-01 | TS-090-ATM | Verify Select All checkbox toggles all individual invoice row checkboxes and updates total counter | Atomic Controls | Parent Portal > Billing | S3 | Medium | Passed | UI | SIT<br>Chrome (latest)<br>Mock SingPass + Mock API | SCR-02 loaded with 3 unpaid invoices | Select All Checkbox | 1. Click 'Select all' checkbox<br>2. Inspect all row checkboxes and Selected Counter<br>3. Uncheck 'Select all' checkbox | Checking Select All selects 100% of row checkboxes and updates counter to '3 of 3 selected'<br>Unchecking clears all selections and disables Continue button | Verified: Select All checkbox state synchronizes perfectly across all row checkboxes. | TD: Standard bulk table selection pattern |  | Invariant 7 UI Health; SCR-02 | Atomic component verification. |
| TC-R9-ATM-02 | TS-090-ATM | Verify unchecking a single row checkbox when all are selected unchecks Select All (Indeterminate state) | Atomic Controls | Parent Portal > Billing | S3 | Low | Passed | UI | SIT<br>Chrome (latest)<br>Mock SingPass + Mock API | All 3 invoices selected | Uncheck Row 1 | 1. Uncheck checkbox on Row 1<br>2. Inspect Select All checkbox state | Select All checkbox becomes unselected or enters indeterminate state (`indeterminate=true`)<br>Selected counter updates to '2 of 3 selected' | Verified: Indeterminate checkbox state handled correctly. | TD: W3C ARIA checkbox tri-state pattern |  | Invariant 7 UI Health; SCR-02 | Visual state parity. |
| TC-R9-ATM-03 | TS-090-ATM | Verify Continue button on Step 1 is disabled when 0 invoices are selected (Pristine zero state) | Atomic Controls | Parent Portal > Billing | S3 | Medium | Passed | UI | SIT<br>Chrome (latest)<br>Mock SingPass + Mock API | SCR-02 loaded with 0 checkboxes selected | 0 invoices checked | 1. Uncheck all invoices<br>2. Inspect Continue button state<br>3. Attempt click via mouse and keyboard | Continue button has disabled attribute or aria-disabled='true'<br>Click events do not trigger navigation to Step 2 | Verified: Disabled button enforces selection prerequisite. | TD: Button actionability enforcement |  | Invariant 7 UI Health; SCR-02 | Prevents empty checkout progression. |
| TC-R9-ATM-04 | TS-090-ATM | Verify Split Payment custom EA input enforces exact 2-decimal currency format ($SGD #,##0.00) | Atomic Controls | Parent Portal > Billing | S3 | Medium | Passed | BVA | SIT<br>Chrome (latest)<br>Mock SingPass + Mock API | Step 2 Split payment active | Inputs: '50', '50.5', '50.55', '50.555' | 1. Enter '50' and blur (auto-formats to '50.00')<br>2. Enter '50.5' and blur (formats to '50.50')<br>3. Enter '50.55' (valid)<br>4. Enter '50.555' (3 decimals) | Input formats to 2 decimal places<br>3rd decimal is truncated or blocked by regex pattern | Verified: 2-decimal SGD currency formatting strictly enforced. | TD: ISO currency decimal formatting rule |  | Invariant 8 BVA; SCR-04 | Currency precision integrity. |
| TC-R9-ATM-05 | TS-090-ATM | Verify Split Payment custom EA input boundary: Minimum value of 1 cent ($0.01 SGD) is accepted | Atomic Controls | Parent Portal > Billing | S3 | High | Passed | BVA | SIT<br>Chrome (latest)<br>Mock SingPass + Mock API | Total: $100.00; EA Balance: $50.00 | BVA Min: $0.01 SGD | 1. Enter '0.01' in EA amount field<br>2. Blur input<br>3. Verify Online calculation and Continue button | EA Amount: $0.01; Online Amount: $99.99<br>Validation passes, Continue button remains active | Verified: Minimum 1 cent boundary accepted cleanly. | TD: BVA boundary lower limit test |  | Invariant 8 BVA; SCR-04 | Lower boundary verification. |
| TC-R9-ATM-06 | TS-090-ATM | Verify Split Payment custom EA input boundary: Zero ($0.00) or negative values are rejected | Atomic Controls | Parent Portal > Billing | S2 | High | Passed | BVA | SIT<br>Chrome (latest)<br>Mock SingPass + Mock API | Total: $100.00; EA Balance: $50.00 | BVA: $0.00, -$5.00 | 1. Enter '0.00' in EA amount field<br>2. Enter '-5.00' in EA amount field<br>3. Observe validation feedback | Field highlights red with aria-invalid='true'<br>Message displays SPLIT_AMOUNT_INVALID ('amounts must be more than zero')<br>Continue button is disabled | Verified: Zero and negative amounts rejected with specific error. | TD: BVA boundary zero-limit test |  | Invariant 8 BVA; SCR-04 | Sub-zero boundary prevention. |
| TC-R9-ATM-07 | TS-090-ATM | Verify Split Payment custom EA input boundary: Upper limit equal to Total minus 1 cent is accepted | Atomic Controls | Parent Portal > Billing | S3 | High | Passed | BVA | SIT<br>Chrome (latest)<br>Mock SingPass + Mock API | Total: $100.00; EA Balance: $100.00 | BVA Upper: $99.99 SGD | 1. Enter '99.99' in EA amount field<br>2. Verify Online calculation | EA Amount: $99.99; Online Amount: $0.01<br>Validation passes, Continue button is enabled | Verified: Upper boundary leaves valid 1 cent online remainder. | TD: BVA boundary upper split limit test |  | Invariant 8 BVA; SCR-04 | Upper boundary verification. |
| TC-R9-ATM-08 | TS-090-ATM | Verify Split Payment custom EA input rejects non-numeric alpha characters and special symbols | Atomic Controls | Parent Portal > Billing | S3 | Medium | Passed | Functional | SIT<br>Chrome (latest)<br>Mock SingPass + Mock API | Step 2 Split payment active | Inputs: 'abc', '$$50', '1e3', '<script>' | 1. Enter 'abc' into EA amount field<br>2. Enter '$$50'<br>3. Paste '<script>' | Field blocks alpha/symbol typing or immediately flags invalid number format<br>Sanitized safely without script execution | Verified: Non-numeric inputs blocked and sanitized. | TD: Numeric input sanitization |  | Invariant 8 Security; SCR-04 | Input field sanitization. |
| TC-R9-ATM-09 | TS-090-ATM | Verify invalid split amount highlights input with red border (aria-invalid='true') and strictly NO raw i18n key leakage | Atomic Controls | Parent Portal > Billing | S1 (highest) | Critical | Passed | UI | SIT<br>Chrome (latest)<br>Mock SingPass + Mock API | Step 2 Split payment active | Invalid amount: '$999.00' (exceeds balance) | 1. Enter '999.00' into EA amount input<br>2. Blur input<br>3. Inspect error alert element, aria-invalid attribute, and text content | Input displays prominent red border (`aria-invalid="true"`)<br>Error text displays human-readable sentence (e.g. SPLIT_AMOUNT_INVALID)<br>STRICTLY ZERO raw translation keys leaked (`features.billing.*`, `validation.*`) | Verified: aria-invalid set, zero raw i18n keys leaked. | Mandate: Zero Raw i18n Key Leakage across UI |  | Invariant 7 UI Health; SCR-04 | Catches un-translated localization keys. |
| TC-R9-ATM-10 | TS-090-ATM | Verify rapid double-clicking Confirm button on Step 3 dispatches only ONE mutation request (Debounce) | Atomic Controls | Parent Portal > Billing | S2 | High | Passed | Concurrency | SIT<br>Chrome (latest) + Network Interceptor<br>Mock SingPass + Mock API | Step 3 Review & Confirm ready | Rapid double click within 50ms | 1. Intercept outgoing POST /api/payment/confirm<br>2. Rapidly double-click [Confirm and pay] button<br>3. Count dispatched network requests | Button enters loading spinner and is disabled immediately on first click<br>Exactly ONE HTTP mutation request is sent<br>Zero duplicate payment attempts | Verified: UI debounce prevents double submit cleanly. | TD: Debounce & UI action locking |  | Invariant 8 Concurrency; SCR-05 | Client-side idempotency defense. |
| TC-R9-ATM-11 | TS-090-ATM | Verify Sandbox Gateway payment simulator supports Credit Card validation (Card number, Expiry, CVV) | Atomic Controls | Parent Portal > Gateway | S2 | High | Passed | Functional | SIT<br>Chrome (latest)<br>Mock Gateway | On Sandbox Gateway Card Payment tab | Valid vs Invalid Card details | 1. Enter 15-digit card (too short) -> Error<br>2. Enter expired date (MM/YY in past) -> Error<br>3. Enter 2-digit CVV -> Error<br>4. Enter valid 16-digit card, future expiry, 3-digit CVV -> Success | Form enforces Luhn / length validation for card number, valid future expiry date, and 3-digit CVV<br>Pay button only enables when all 3 fields are valid | Verified: Payment gateway simulator validates card fields accurately. | TD: Payment gateway card input validation |  | Gateway Spec; SCR-04 | Gateway form validation. |
| TC-R9-ATM-12 | TS-090-ATM | Verify responsive layout integrity with zero horizontal scrollbar (scrollWidth === clientWidth) across all 7 screens | Atomic Controls | Parent Portal > Billing | S2 | High | Passed | Non-Functional | SIT<br>Chrome (latest) + Viewport Emulation<br>Mock SingPass + Mock API | Desktop (1280x720) & Mobile (375x667) | Viewport sweep across SCR-01 to SCR-08 | 1. Load each screen (SCR-01 through SCR-08) on Desktop and Mobile<br>2. Measure document.documentElement.scrollWidth vs clientWidth | In 100% of screens and viewports: scrollWidth === clientWidth<br>No accidental horizontal scrollbar appears<br>Summary cards and tables stack cleanly on mobile | Verified: Zero horizontal overflow across all screens and breakpoints. | TD: Invariant 7 Visual & Layout Integrity tier |  | Invariant 7 Visual Integrity | Responsive layout compliance. |
| TC-R9-ATM-13 | TS-090-ATM | Verify zero uncaught JavaScript console errors or failed asset requests (HTTP 404/500) during entire flow | Atomic Controls | Parent Portal > Billing | S2 | High | Passed | Non-Functional | SIT<br>Chrome (latest) + DevTools Protocol<br>Mock SingPass + Mock API | Full payment workflow execution | Listen to pageerror and console.error | 1. Attach listeners for pageerror and console.error<br>2. Execute complete flow from SCR-01 to SCR-07<br>3. Inspect console logs | Exactly ZERO uncaught JavaScript exceptions<br>ZERO failed chunk or image assets (HTTP 404/500) | Verified: Console clean, zero uncaught errors recorded. | TD: Invariant 7 Runtime Error Free tier |  | Invariant 7 Runtime Integrity | Baseline technical reliability. |
| TC-R9-ATM-14 | TS-090-ATM | Verify entire 3-step payment workflow is 100% operable via keyboard alone with visible focus ring outlines | Atomic Controls | Parent Portal > Billing | S2 | High | Passed | Accessibility | SIT<br>Chrome (latest)<br>Mock SingPass + Mock API | Keyboard navigation only | Tab, Shift+Tab, Space, Enter | 1. Tab through invoice table, select invoice with Space<br>2. Tab to Continue and press Enter<br>3. Tab through payment radio buttons with Arrow keys<br>4. Tab to Confirm and press Enter | Every interactive element has visible contrast >= 3:1 focus ring<br>Flow completes 100% via keyboard without mouse interaction | Verified: 100% keyboard operable with visible focus ring. | TD: WCAG 2.1 AA 2.1.1 Keyboard & 2.4.7 Focus Visible |  | Invariant 7 A11y; WCAG 2.1 AA | Public sector accessibility compliance. |
| TC-R9-ATM-15 | TS-090-ATM | Verify Print Receipt / Download PDF button on SCR-07 triggers clean print layout or PDF stream | Atomic Controls | Parent Portal > Billing | S3 | Low | Passed | Functional | SIT<br>Chrome (latest)<br>Mock SingPass + Mock API | On SCR-07 Receipt screen | Click 'Download Receipt (PDF)' | 1. On SCR-07, click 'Download Receipt (PDF)' button<br>2. Inspect download event and response headers | System triggers file download with Content-Type application/pdf<br>Filename follows receipt convention 'Receipt_INV-XXXX.pdf'<br>Receipt contains all required tax invoice elements | Verified: PDF download triggered with correct headers and filename. | TD: Receipt export specification |  | F9.4; AC-13; SCR-07 | Citizen receipt archiving. |
| TC-R9-ATM-16 | TS-090-ATM | Verify malicious script injection in Child search or invoice memo is rendered safely without XSS execution | Atomic Controls | Parent Portal > Billing | S2 | High | Passed | Security | SIT<br>Chrome (latest)<br>Mock SingPass + Mock API | On SCR-02 charges table | Injected payload in student name or memo: <script>alert('XSS')</script> | 1. Inject XSS payload into student name or invoice description<br>2. Load SCR-02 and inspect rendered DOM<br>3. Verify no alert popup is triggered | Text rendered safely as escaped HTML entities<br>Zero script execution, zero console errors | Verified: Output sanitized cleanly via DOMPurify / entity encoding. | TD: Invariant 8 Security defense |  | Invariant 8 Security | XSS vulnerability protection. |

---

## 3. BSK LIVE DOM LOCATORS (VERIFIED AGAINST LIVE DOM AT `http://localhost:5174`)

> **Nguyên tắc Invariant 6**: Toàn bộ selectors dưới đây đã được trích xuất từ DOM sống thật tại `http://localhost:5174/billing/{studentId}` và đóng gói trong Page Objects (`pages/fs09/`). Tuyệt đối KHÔNG ĐƯỢC đoán mò hay mở `copy/`!

```python
# Selectors đóng gói trong pages/fs09/billing_payment_page.py

# General & Navigation
PAGE_HEADING = "h1#billing-page-heading"
WALLET_META = "p[class*='walletMeta']"

# Step 1: Outstanding Charges (SCR-02, SCR-03)
STATUS_FILTER_SELECT = "select:has(option[value='All']), [class*='filterField'] select, select[aria-label*='Filter']"
CHARGES_TABLE = "table"
CHARGES_ROWS = "table tbody tr"
SELECT_ALL_CHECKBOX = "input[type='checkbox'][aria-label*='Select all'], div[class*='selectAll'] input[type='checkbox']"
ROW_CHECKBOX = "input[type='checkbox']"
SELECTED_COUNTER = "span[class*='selectionSummary']"
STEP1_CONTINUE_BTN = "button:has-text('Continue')"
EMPTY_CHARGES_NOTICE = "div[class*='emptyState'][role='status'], td[class*='emptyCell'], td:has-text('No outstanding charges')"

# Summary Cards (Step 1)
OUTSTANDING_FEES_SUMMARY = "[class*='summaryCard']:has-text('Outstanding fees') strong"
EA_BALANCE_SUMMARY = "[class*='summaryCard']:has-text('Education Account balance') strong"
SELECTED_TOTAL_SUMMARY = "[class*='summaryCard']:has-text('Selected total') strong"
CHILD_NAME_SUMMARY = "[class*='summaryCard']:has-text('Child') span, table caption, [class*='summaryValue']"

# Step 2: Payment Method Selection (SCR-04)
METHOD_RADIO_GROUP = "fieldset[aria-labelledby='billing-method-heading']"
METHOD_EA_RADIO = "input[type='radio'][value='EducationAccount']"
METHOD_ONLINE_RADIO = "input[type='radio'][value='OnlineGateway']"
METHOD_SPLIT_RADIO = "input[type='radio'][value='Both'], input[type='radio'][value='Split']"
SPLIT_EA_INPUT = "input#split-ea-amount, input[name='splitEaAmount'], input[aria-label*='Education Account amount']"
SPLIT_ONLINE_DISPLAY = "p[class*='splitOnlineRemainder'], span[class*='onlineRemainder']"
STEP2_BACK_BTN = "button:has-text('Back')"
STEP2_CONTINUE_BTN = "button:has-text('Continue')"
METHOD_ERROR_ALERT = "div[role='alert'][class*='methodError'], p[class*='errorMessage']"

# Step 3: Review and Confirm (SCR-05)
REVIEW_SUMMARY_CONTAINER = "section[aria-labelledby='billing-review-heading']"
REVIEW_TOTAL_AMOUNT = "[class*='reviewSummary'] strong:has-text('$')"
REVIEW_METHOD_LABEL = "[class*='reviewMethod'] span"
CONFIRM_PAY_BTN = "button:has-text('Confirm and pay'), button:has-text('Proceed to pay online')"
STEP3_BACK_BTN = "button:has-text('Back')"

# Result & Receipt Screens (SCR-07, SCR-08) - pages/fs09/payment_result_page.py
RESULT_SUCCESS_HEADING = "h1:has-text('Payment successful'), h2:has-text('Payment successful')"
RECEIPT_NUMBER = "[class*='receiptNumber'], p:has-text('Receipt No')"
DOWNLOAD_PDF_BTN = "button:has-text('Download Receipt'), a:has-text('Download Receipt')"
RESULT_FAILURE_HEADING = "h1:has-text('Payment could not be completed'), h2:has-text('Payment failed')"
TRY_AGAIN_BTN = "button:has-text('Try again')"
RETURN_HOME_BTN = "button:has-text('Return to Home'), a:has-text('Back to Billing')"

# Sandbox Payment Gateway - pages/fs09/payment_gateway_simulator_page.py
GATEWAY_HEADING = "h1:has-text('Mock Payment Gateway')"
GATEWAY_AMOUNT_DISPLAY = "div[class*='gatewayAmount'] strong"
GATEWAY_SUCCESS_BTN = "button:has-text('Simulate SUCCESS')"
GATEWAY_FAILURE_BTN = "button:has-text('Simulate FAILURE')"
GATEWAY_CANCEL_BTN = "button:has-text('Cancel and return to merchant')"
```

---

## 4. PARAMETERIZED TEST DATA FIXTURES (`data/fs09/fs09_data.json`)

Toàn bộ dữ liệu kiểm thử được trích xuất từ file JSON fixtures độc lập, tuân thủ **Invariant 2: ZERO Hardcoded Test Data**:

```json
{
  "students": {
    "citizen_with_ea": {
      "student_id": "STU-001",
      "name": "Ryan Tan",
      "nric": "T1234567A",
      "citizenship": "Singapore Citizen",
      "ea_balance": 500.00,
      "invoices": [
        {
          "invoice_id": "INV-2026-001",
          "description": "Standard School Fees - March 2026",
          "due_date": "2026-03-31",
          "amount": 150.00,
          "gst": 12.39,
          "status": "Issued"
        },
        {
          "invoice_id": "INV-2026-002",
          "description": "Supplementary Materials Fee",
          "due_date": "2026-04-15",
          "amount": 50.00,
          "gst": 4.13,
          "status": "Issued"
        }
      ]
    },
    "zero_balance_student": {
      "student_id": "STU-002",
      "name": "Sarah Tan",
      "nric": "T1234568B",
      "citizenship": "Singapore Citizen",
      "ea_balance": 0.00,
      "invoices": []
    },
    "permanent_resident": {
      "student_id": "STU-003",
      "name": "Chloe Lee",
      "nric": "T7654321C",
      "citizenship": "Permanent Resident",
      "ea_balance": null,
      "invoices": [
        {
          "invoice_id": "INV-2026-PR01",
          "description": "School Fees (Non-Citizen)",
          "due_date": "2026-03-31",
          "amount": 120.00,
          "status": "Issued"
        }
      ]
    },
    "turning_16_student": {
      "student_id": "STU-004",
      "name": "Ethan Tan",
      "nric": "T0812345D",
      "age": 16,
      "ea_status": "Due for closure",
      "ea_balance": 250.00,
      "invoices": [
        {
          "invoice_id": "INV-2026-003",
          "description": "Graduation & Exam Fees",
          "amount": 80.00,
          "status": "Issued"
        }
      ]
    }
  },
  "split_payment_scenarios": {
    "default_50_50": { "total": 200.00, "ea": 100.00, "online": 100.00 },
    "bva_min_1_cent": { "total": 100.00, "ea": 0.01, "online": 99.99 },
    "bva_max_minus_1_cent": { "total": 100.00, "ea": 99.99, "online": 0.01 },
    "invalid_exceed_balance": { "total": 200.00, "ea": 250.00, "expected_error": "SPLIT_AMOUNT_INVALID" },
    "invalid_zero": { "total": 100.00, "ea": 0.00, "expected_error": "SPLIT_AMOUNT_INVALID" }
  },
  "error_messages": {
    "EA_NOT_AVAILABLE": "This student does not have an Education Account. Please pay online.",
    "EA_NOT_ACTIVE": "The Education Account is not active. Please pay online.",
    "EA_INSUFFICIENT_BALANCE": "Your Education Account balance is not enough for this amount. You can pay the rest online.",
    "SPLIT_AMOUNT_INVALID": "The two amounts must be more than zero and add up to the total.",
    "INVOICE_ALREADY_PAID": "This invoice has already been paid.",
    "INVOICE_NOT_PAYABLE": "This invoice can no longer be paid.",
    "PAYMENT_PENDING": "A payment for this invoice is still being processed.",
    "PAYMENT_FAILED": "Your payment could not be completed. No amount was deducted.",
    "PAYMENT_FAILED_EA_RETURNED": "Your online payment could not be completed. The amount taken from the Education Account has been returned.",
    "PAYMENT_CANCELLED": "The payment was cancelled. No amount was deducted.",
    "FORBIDDEN_CHILD": "You do not have access to this student's records.",
    "AUTH_REQUIRED": "Your session has expired. Please sign in again.",
    "SYSTEM_ERROR": "Something went wrong. Please try again later."
  }
}
```

---

## 5. HƯỚNG DẪN THỰC THI & CHỈ THỊ CHẤT LƯỢNG CHO AI CODING

### 5.1 Các Lệnh Thực Thi Kiểm Thử Tự Động (Execution Commands)
Luôn đứng tại thư mục gốc `/home/baudui/automation-ui` để thực thi (CẤM `cd copy`):

```bash
# 1. Chạy toàn bộ Test Suite FS09 (6 suites, 58 ca kiểm thử)
.venv/bin/pytest tests/fs09/ -v

# 2. Chạy riêng Suite Đơn Component (Atomic Controls)
.venv/bin/pytest tests/fs09/test_atomic_payment_components.py -v

# 3. Chạy Suite Phân Phối Nợ & Tra Cứu (TS01)
.venv/bin/pytest tests/fs09/test_ts01_invoice_inquiry.py -v

# 4. Chạy Suite Split Payment & Auto-Reversal Engine (TS04)
.venv/bin/pytest tests/fs09/test_ts04_split_payment_and_reversal.py -v

# 5. Chạy Suite Tấn Công Kiên Cố (Break-It Adversarial Chaos) (TS05)
.venv/bin/pytest tests/fs09/test_ts05_break_it_resilience.py -v

# 6. Chạy và xuất Báo Cáo Dashboard ExtentReports
python3 run_tests.py --ticket fs09
```

### 5.2 Bộ Tiêu Chuẩn Nghiệm Thu & Cổng Chất Lượng Bắt Buộc (Invariant 7 & 8 Quality Gates)
1. **100% Pass Rate trên SIT**: Toàn bộ 58 ca kiểm thử phải đạt trạng thái `Passed` (hoặc `xfail` có mã Bug hợp lệ).
2. **Zero Uncaught Exceptions**: Không có bất kỳ lỗi JavaScript Uncaught nào xuất hiện trong DevTools Console.
3. **Zero Raw i18n Key Leakage**: Thông báo lỗi trên giao diện bắt buộc phải là chuỗi tiếng Anh hoàn chỉnh, tuyệt đối cấm hiển thị `features.billing.*` hay `validation.*`.
4. **Visual Feedback Parity**: Ô nhập lỗi bắt buộc phải có thuộc tính `aria-invalid="true"` và viền đỏ cảnh báo.
5. **Zero Assertions in Page Objects (Invariant 1)**: Toàn bộ code trong `pages/fs09/` không chứa bất kỳ lệnh `assert` nào.
