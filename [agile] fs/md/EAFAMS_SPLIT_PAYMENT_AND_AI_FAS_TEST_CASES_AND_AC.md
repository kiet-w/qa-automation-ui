# BỘ TEST CASES & ACCEPTANCE CRITERIA (AC) CHI TIẾT
## EAFAMS e-Service Portal: Kịch bản Split Payment (R9) & AI Auto-fill FAS Form (R10)

> **Dự án**: EAFAMS (Education Account, School, Student & Fee Management System)  
> **Phân hệ**: e-Service Portal (Parent Portal)  
> **Module kiểm thử**: R9 (Payment Engine) & R10 (Family FAS Application Engine)  
> **Tiêu chuẩn chất lượng**: Enterprise Banking & GovTech Grade (ISO/IEC/IEEE 29119, OWASP ASVS, Gherkin BDD)  
> **Ngày phê duyệt**: 19/10/2026  

---

## MỤC LỤC
1. [Tổng quan Kiến trúc & Nguyên tắc Kiểm thử](#1-tổng-quan-kiến-trúc--nguyên-tắc-kiểm-thử)
2. [Phân hệ R9: Kịch bản Thanh toán Kết hợp (Split Payment)](#2-phân-hệ-r9-kịch-bản-thanh-toán-kết-hợp-split-payment)
   - 2.1. User Story & Luồng Trực quan Hai bước (Two-Step Sequential Flow)
   - 2.2. Chi tiết Acceptance Criteria (AC-SP-01 đến AC-SP-08)
   - 2.3. Bảng Ma trận Test Cases chi tiết (TC-SP-01 đến TC-SP-12)
3. [Phân hệ R10: Luồng Nộp Đơn FAS Gia đình & AI Auto-fill](#3-phân-hệ-r10-luồng-nộp-đơn-fas-gia-đình--ai-auto-fill)
   - 3.1. User Story & Luồng Trực quan 5-Step Wizard & Timeline
   - 3.2. Chi tiết Acceptance Criteria (AC-FAS-01 đến AC-FAS-08)
   - 3.3. Bảng Ma trận Test Cases chi tiết (TC-FAS-01 đến TC-FAS-14)
4. [Kịch bản Kiểm thử Phi chức năng & Bảo mật (Security & Performance)](#4-kịch-bản-kiểm-thử-phi-chức-năng--bảo-mật)

---

## 1. TỔNG QUAN KIẾN TRÚC & NGUYÊN TẮC KIỂM THỬ

### 1.1. Phạm vi Kiểm thử Trọng yếu
* **Phân hệ R9 (Split Payment)**:
  * Cơ chế kiểm tra số dư khả dụng EA và tính toán tỷ lệ tự động.
  * Tính toàn vẹn giao dịch sổ cái (ACID) qua cơ chế 2 bước tuần tự.
  * Xử lý ngoại lệ mạng, timeout (10 phút), chữ ký số webhook HMAC-SHA256.
  * Động cơ hoàn tiền tự động (`EA Reversal Engine`) và cơ chế chặn treo tiền (`ReconciliationRequired`).
* **Phân hệ R10 (Family FAS & AI Auto-fill)**:
  * Trình hướng dẫn 5 bước (5-Step Wizard) cho phép gom tất cả con cái vào 1 lần nộp.
  * Tự động trích xuất thu nhập từ API Dữ liệu Chính phủ (CPF & IRAS Tax).
  * Kiểm thử công thức tính $PCI = \frac{GHI}{\text{Household Size}}$ và đánh giá điều kiện MOEFAS vs SBFAS.
  * Tính năng AI Auto-fill (US-AI3) tổng hợp dữ liệu Singpass và hội thoại Chatbot.
  * Tiến trình 4 mốc (Timeline tracking) tách đơn về Admin R4 và cơ chế Auto-grant tức thì.

---

## 2. PHÂN HỆ R9: KỊCH BẢN THANH TOÁN KẾT HỢP (SPLIT PAYMENT)

### 2.1. User Story
> **US-R9.3**: Là một Phụ huynh có con đang học tại trường MOE, khi số dư tài khoản EA của con không đủ thanh toán toàn bộ hóa đơn học phí ($0 < \text{EA Balance} < \text{Net Payable}$), tôi muốn có thể trích toàn bộ hoặc một phần số dư EA hiện có và thanh toán phần tiền còn thiếu qua Cổng thanh toán trực tuyến trong cùng một giao dịch an toàn, đảm bảo nếu thanh toán trực tuyến thất bại thì số tiền EA đã trích phải được hoàn lại 100% ngay lập tức.

---

### 2.2. Chi tiết Acceptance Criteria (Gherkin BDD Format)

#### AC-SP-01: Điều kiện Hiển thị & Đề xuất Tỷ lệ Tự động
```gherkin
Scenario: Gợi ý tỷ lệ thanh toán Split Payment tự động khi số dư EA không đủ 100%
  Given Phụ huynh đã đăng nhập vào e-Service Portal và chọn 1 hóa đơn có Net Payable = 150.00 SGD
  And Tài khoản EA của con ở trạng thái "Active" với Available Balance = 60.00 SGD
  When Phụ huynh chọn phương thức thanh toán "Split Payment"
  Then Nút thanh toán "100% Education Account" bị vô hiệu hóa kèm thông báo "EA_INSUFFICIENT_BALANCE"
  And Hệ thống tự động điền giá trị đề xuất:
    | Trường           | Giá trị Đề xuất | Trạng thái Chỉnh sửa |
    | EA Amount        | 60.00 SGD       | Cho phép sửa         |
    | Online Amount    | 90.00 SGD       | Read-only (Tự động)  |
    | Net Payable      | 150.00 SGD      | Read-only            |
  And Quy tắc ràng buộc: 0.01 SGD <= EA Amount <= 60.00 SGD
  And Công thức tự động: Online Amount = Net Payable - EA Amount
```

#### AC-SP-02: Ràng buộc Xác thực Nhập liệu Số tiền EA (Validation Bounds)
```gherkin
Scenario Outline: Xác thực biên giá trị khi Phụ huynh tùy chỉnh EA Amount
  Given Hóa đơn Net Payable = 100.00 SGD, Available EA Balance = 40.00 SGD
  When Phụ huynh nhập <Input_EA_Amount> vào ô EA Amount
  Then Hệ thống phản hồi <Result> và <Error_Message>

  Examples:
    | Input_EA_Amount | Result | Error_Message                                                  |
    | 40.00           | Valid  | N/A (Online Amount = 60.00 SGD)                                |
    | 25.50           | Valid  | N/A (Online Amount = 74.50 SGD)                                |
    | 0.00            | Error  | "EA amount must be greater than 0. Please choose Online Pay."   |
    | -5.00           | Error  | "Invalid amount."                                              |
    | 40.01           | Error  | "EA amount cannot exceed your available balance of 40.00 SGD." |
    | 100.00          | Error  | "EA amount cannot exceed your available balance of 40.00 SGD." |
    | abc             | Error  | "Please enter a valid numeric amount."                         |
```

#### AC-SP-03: Bước 1 - Ghi nợ Sổ cái EA & Idempotency Key
```gherkin
Scenario: Bước 1 - Trừ tiền EA an toàn kèm khóa chống thanh toán trùng
  Given Phụ huynh xác nhận thanh toán Split với EA Amount = 50.00 SGD, Online Amount = 100.00 SGD
  When Phụ huynh bấm nút "Confirm Payment"
  Then Nút bấm lập tức chuyển trạng thái disabled và hiển thị spinner "Processing..."
  And Hệ thống sinh một mã duy nhất IdempotencyKey (UUIDv4) gắn liền với Session này
  And Hệ thống gọi Function 1 Core Ledger API:
    | Tham số            | Giá trị                                                 |
    | AccountId          | Mã EA của con                                           |
    | Amount             | -50.00 SGD                                              |
    | TransactionType    | Fee payment (Split - Step 1)                            |
    | FundingReference   | Mã tham chiếu ghi nợ riêng biệt                          |
    | IdempotencyKey     | UUIDv4 đã sinh                                          |
  And Nếu Function 1 trả về Success:
    | Trạng thái Hóa đơn | Chuyển thành "PaymentPending"                           |
    | Số dư EA khả dụng  | Trừ ngay lập tức 50.00 SGD                              |
    | Chuyển hướng       | Khởi tạo Session và Redirect sang Sandbox Payment Gateway |
```

#### AC-SP-04: Xử lý Ngoại lệ tại Bước 1 (EA Debit Thất bại)
```gherkin
Scenario: Bước 1 thất bại do tài khoản EA vừa bị khóa hoặc không đủ số dư thực tế
  Given Phụ huynh đang ở màn hình Confirm Split Payment
  When Hệ thống gọi Function 1 ghi nợ EA nhưng gặp lỗi (Tài khoản bị đóng/Số dư bị khóa)
  Then Giao dịch dừng lại ngay lập tức
  And Hóa đơn giữ nguyên trạng thái "Issued" (Chưa trừ tiền, chưa chuyển PaymentPending)
  And Hiển thị thông báo lỗi thân thiện: "Unable to deduct Education Account. Please try again or pay 100% online."
  And Tuyệt đối không mở Session thanh toán Online sang Payment Gateway
```

#### AC-SP-05: Bước 2 - Thanh toán Online Thành công qua Webhook HMAC-SHA256
```gherkin
Scenario: Bước 2 - Thanh toán Online thành công và hoàn tất giao dịch
  Given Bước 1 đã hoàn tất thành công, hóa đơn ở trạng thái PaymentPending
  And Phụ huynh đã hoàn thành thao tác thanh toán trên Sandbox Payment Gateway
  When Sandbox Gateway gửi HTTP POST Webhook về endpoint /api/payments/webhook
  Then Hệ thống đối soát chữ ký điện tử HMAC-SHA256 trên header X-Signature bằng Secret Key
  And Chữ ký hợp lệ:
    | Hành động Hệ thống | Kết quả                                                        |
    | Cập nhật Hóa đơn   | Chuyển trạng thái sang "Paid"                                  |
    | Lưu vết Giao dịch  | Lưu đồng thời EA_Txn_Id và Online_Txn_Id vào bản ghi Hóa đơn   |
    | Hiển thị Giao diện | Điều hướng Phụ huynh về màn hình Payment Receipt (Biên lai)    |
    | Biên lai hiển thị  | Chi tiết rõ: Trừ EA (50.00 SGD) + Thanh toán Online (100.00 SGD)|
```

#### AC-SP-06: Bước 2 Thất bại / Hủy / Timeout ➔ Kích hoạt EA Reversal Engine
```gherkin
Scenario Outline: Nhánh Online bị lỗi hoặc hết hạn, kích hoạt tự động hoàn lại tiền EA
  Given Bước 1 đã trừ EA Amount = 50.00 SGD, hóa đơn đang là PaymentPending
  When Xảy ra sự kiện <Event_Trigger> ở Bước 2
  Then Hệ thống lập tức kích hoạt "EA Reversal Engine":
    | Hành vi Reversal Engine | Chi tiết                                                      |
    | Gọi Function 1 Ledger   | Ghi có +50.00 SGD vào tài khoản EA của con                    |
    | Loại giao dịch          | "Refund (Split Payment Auto-Reversal)"                        |
    | Trạng thái Hóa đơn      | Chuyển ngược lại về "Issued"                                  |
    | Trừ tiền Phụ huynh      | 0 SGD (Tài khoản EA phục hồi nguyên trạng)                    |
    | Thông báo Phụ huynh     | Mã "PAYMENT_FAILED_EA_RETURNED": "Your online payment could not be completed. The amount taken from the Education Account has been returned." |

  Examples:
    | Event_Trigger                                                              |
    | Phụ huynh bấm nút "Cancel and Return to Merchant" trên Gateway              |
    | Thẻ bị từ chối / Không đủ hạn mức trên Gateway                             |
    | Timeout 10 phút trôi qua không nhận được Webhook từ Gateway                |
```

#### AC-SP-07: EA Reversal Thất bại ➔ Fallback Trạng thái `ReconciliationRequired`
```gherkin
Scenario: Sự cố nghiêm trọng - Reversal Engine không thể hoàn tiền EA tự động
  Given Bước 2 Online bị thất bại nhưng Core Ledger DB bị mất kết nối khi thực hiện Reversal
  When EA Reversal Engine thử lại 3 lần (Retry with Exponential Backoff) đều thất bại
  Then Hệ thống KHÔNG chuyển hóa đơn về "Issued" (tránh phụ huynh bị trừ tiền 2 lần)
  And Chuyển trạng thái hóa đơn sang "ReconciliationRequired"
  And Tạo bản ghi cảnh báo khẩn cấp trong bảng Audit_Exceptions gửi School/MOE Admin
  And Hiển thị thông báo an tâm cho Phụ huynh: "We are verifying this payment. Please check your account history later." (Mã ReconciliationRequired)
```

#### AC-SP-08: Kiểm soát Concurrency & Ràng buộc Độ tuổi 16
```gherkin
Scenario: Chặn thao tác trùng lặp khi đang có Session thanh toán dở dang
  Given Hóa đơn đang ở trạng thái "PaymentPending" do Phụ huynh đã mở tab thanh toán Online
  When Phụ huynh mở một tab trình duyệt khác hoặc ấn nút Back để thanh toán lại cùng hóa đơn đó
  Then Hệ thống chặn toàn bộ các nút bấm thanh toán
  And Hiển thị thông báo "PAYMENT_PENDING": "A payment for this invoice is still being processed."
  And Con đã tròn 16 tuổi (Due for closure): Nút thanh toán bị vô hiệu hóa hoàn toàn, chỉ cho phép xem lịch sử.
```

---

### 2.3. Bảng Ma trận Test Cases chi tiết (Phân hệ R9 - Split Payment)

| TC ID | Kịch bản Kiểm thử | Phân loại | Điều kiện Tiền đề | Các Bước Thực hiện | Dữ liệu Đầu vào | Kết quả Kỳ vọng | Mức độ |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-SP-01** | Kiểm tra hiển thị Split Payment khi đủ điều kiện | Functional / GUI | Tài khoản EA Active, $0 < \text{Balance} < \text{Net}$ | 1. Mở Fees & Payment<br>2. Chọn hóa đơn nợ<br>3. Kiểm tra các option thanh toán | Net = 200$, EA = 80$ | Hiện 2 option: Split Payment & Online Payment. Option 100% EA bị disabled. Gợi ý EA = 80$, Online = 120$. | **P1** |
| **TC-SP-02** | Điều chỉnh giảm số tiền EA hợp lệ | Functional | Đang ở form Split Payment | 1. Nhập EA Amount nhỏ hơn số dư khả dụng<br>2. Kiểm tra ô Online Amount | EA sửa thành 50.00$ | Ô Online Amount tự động nhảy thành 150.00$. Tổng hiển thị = 200.00$. Nút Confirm active. | **P1** |
| **TC-SP-03** | BVA: Nhập EA Amount bằng 0.01$ (Biên dưới) | Boundary Value | Đang ở form Split Payment | 1. Nhập EA Amount = 0.01$<br>2. Kiểm tra tính toán | Net = 100.00$, EA = 0.01$ | Hợp lệ. Online Amount = 99.99$. Hệ thống cho phép tiếp tục. | **P2** |
| **TC-SP-04** | BVA: Nhập EA Amount bằng đúng số dư khả dụng (Biên trên) | Boundary Value | Đang ở form Split Payment | 1. Nhập EA Amount = Available Balance<br>2. Kiểm tra tính toán | Net = 100.00$, Balance = 45.00$ | Hợp lệ. EA = 45.00$, Online = 55.00$. | **P2** |
| **TC-SP-05** | BVA: Nhập EA Amount vượt quá số dư khả dụng | Negative / Boundary | Đang ở form Split Payment | 1. Nhập EA Amount = Balance + 0.01$<br>2. Bấm Confirm | Balance = 50.00$, Input = 50.01$ | Báo lỗi inline: "EA amount cannot exceed your available balance of 50.00 SGD". Khóa nút Confirm. | **P1** |
| **TC-SP-06** | Nhập EA Amount = 0 hoặc số âm | Negative | Đang ở form Split Payment | 1. Nhập 0 hoặc -10.00$<br>2. Bấm Confirm | Input = 0 hoặc -10 | Báo lỗi inline. Chặn không cho gửi request. | **P2** |
| **TC-SP-07** | Luồng thành công toàn phần (Happy Path) | End-to-End | EA = 60$, Net = 150$ | 1. Confirm Split (EA 60$, Online 90$)<br>2. Nhập thẻ thành công trên Sandbox<br>3. Gateway gửi webhook HMAC hợp lệ | Thẻ test: Pass | EA bị trừ 60$, Online nhận 90$. Hóa đơn đổi `Paid`. Hiển thị Receipt với 2 Transaction ID riêng biệt. | **P1** |
| **TC-SP-08** | Sandbox Gateway: Người dùng bấm Hủy giao dịch (Cancel) | Exception / Flow | Đã trừ EA 50$, đang ở trang Sandbox Gateway | 1. Bấm "Cancel and return"<br>2. Kiểm tra trạng thái hệ thống | N/A | EA Reversal Engine kích hoạt ngay lập tức. Hoàn lại 50$ vào EA. Hóa đơn về `Issued`. Hiện thông báo `PAYMENT_FAILED_EA_RETURNED`. | **P1** |
| **TC-SP-09** | Sandbox Gateway: Giao dịch thất bại (Card Declined) | Exception / Flow | Đã trừ EA 40$, đang ở trang Sandbox Gateway | 1. Chọn mã thẻ bị lỗi/hết hạn<br>2. Nhận kết quả thất bại từ Gateway | Test Card: Declined | Kích hoạt EA Reversal Engine. Hoàn lại 40$ vào EA. Hóa đơn về `Issued`. Phụ huynh không mất tiền. | **P1** |
| **TC-SP-10** | Timeout thanh toán trực tuyến (10 phút) | Timeout / Edge | Đã trừ EA 30$, cổng online mở nhưng treo | 1. Mở trang thanh toán Online<br>2. Không thao tác quá 10 phút<br>3. Chờ Background Timeout Handler | Thời gian > 10m01s | Gateway session hết hạn. Hệ thống tự động Reversal 30$ về EA. Hóa đơn giải phóng khỏi `PaymentPending`, về `Issued`. | **P1** |
| **TC-SP-11** | Chống thanh toán kép (Double-click prevention) | Concurrency | Form Confirm Payment | 1. Double click liên tục vào nút Confirm Payment | 2 click cách nhau 50ms | Nút bị disabled ngay sau click 1. Chỉ duy nhất 1 IdempotencyKey và 1 request trừ tiền được gửi đi. | **P1** |
| **TC-SP-12** | Sự cố EA Reversal Engine bị lỗi kết nối | Fault Tolerance | Đã trừ EA, Online fail, ngắt DB lúc Reversal | 1. Giả lập lỗi Core Ledger khi Reversal<br>2. Kiểm tra retry và fallback | Core Ledger 500 | Retry 3 lần thất bại. Hóa đơn chuyển trạng thái `ReconciliationRequired`. Gửi cảnh báo Admin Portal. Thông báo cho phụ huynh. | **P1** |

---

## 3. PHÂN HỆ R10: LUỒNG NỘP ĐƠN FAS GIA ĐÌNH & AI AUTO-FILL

### 3.1. User Story
> **US-R10.1**: Là một Phụ huynh có nhiều con đang theo học tại các trường công lập, tôi muốn có thể nộp một lá đơn xin trợ cấp tài chính (FAS) duy nhất cho toàn bộ các con trong gia đình thông qua quy trình hướng dẫn trực quan, được hệ thống tự động trích xuất thu nhập từ API Chính phủ và sử dụng tính năng AI Auto-fill để điền sẵn hồ sơ, đồng thời theo dõi tiến độ xét duyệt trực quan qua 4 mốc thời gian.

---

### 3.2. Chi tiết Acceptance Criteria (Gherkin BDD Format)

#### AC-FAS-01: Step 1 - Lọc Danh sách Con Hợp lệ & Phân quyền
```gherkin
Scenario: Bước 1 - Lựa chọn danh sách con cái đủ điều kiện nộp FAS
  Given Phụ huynh truy cập mục "Financial Assistance Scheme (FAS)"
  When Hệ thống tải Step 1 - Children
  Then Thông tin cá nhân Phụ huynh hiển thị ở chế độ Chỉ đọc (Read-only) lấy từ Singpass
  And Dropdown chọn mối quan hệ hiển thị: "Father", "Mother", "Legal Guardian"
  And Danh sách các con được đối soát từ Government Data API:
    | Trạng thái Con                          | Trạng thái Checkbox | Ghi chú Hiển thị                                           |
    | Đang đi học, < 16 tuổi, chưa nộp FAS    | Cho phép tích chọn  | Sẵn sàng nộp đơn                                           |
    | Đã tròn 16 tuổi (Due for closure/Closed)| Bị Disable (Khóa)   | "Not eligible: Student has reached 16 years of age"        |
    | Đang có đơn FAS chờ duyệt (Pending)     | Bị Disable (Khóa)   | "Application already submitted and currently under review"  |
  And Quy tắc: Phụ huynh phải tích chọn ít nhất 1 đứa con hợp lệ mới được bấm "Next: Household"
```

#### AC-FAS-02: Step 2 - Tự động Kéo Thu nhập từ API Chính phủ & Thêm Thành viên
```gherkin
Scenario: Bước 2 - Tự động truy xuất thu nhập CPF/IRAS và bổ sung thành viên hộ gia đình
  Given Phụ huynh chuyển sang Step 2 - Household & Income
  When Hệ thống gọi Government Data API theo NRIC của Cha và Mẹ
  Then Dữ liệu thu nhập tự động hiển thị mà không yêu cầu tải lên bảng lương:
    | Thành viên | Nguồn Dữ liệu   | Thu nhập trích xuất | Trạng thái Chỉnh sửa |
    | Phụ huynh  | IRAS Tax & CPF  | Số tiền chính thức  | Chỉ đọc (Read-only)  |
    | Vợ / Chồng | IRAS Tax & CPF  | Số tiền chính thức  | Chỉ đọc (Read-only)  |
  When Phụ huynh bấm "+ Add member" để thêm thành viên khác (Ông, Bà, Anh, Chị)
  Then Hiển thị modal nhập: Họ tên, NRIC/FIN, Mối quan hệ, Nghề nghiệp, Thu nhập hàng tháng
  And Khi thành viên không có thu nhập (VD: Người cao tuổi/Học sinh): Cho phép tích chọn "Unemployed / Student (0.00 SGD)"
```

#### AC-FAS-03: Step 2 - Tính toán Tự động GHI, Household Size & PCI
```gherkin
Scenario Outline: Tính toán tự động tổng thu nhập GHI và thu nhập bình quân đầu người PCI
  Given Danh sách thành viên hộ gia đình có thu nhập như bảng Examples
  When Hệ thống tổng hợp dữ liệu tại Step 2
  Then Hệ thống tự động tính toán theo đúng công thức:
    | Chỉ số          | Công thức                               |
    | Household Size  | Tổng số thành viên trong danh sách      |
    | GHI             | Tổng Gross Monthly Income của tất cả TV |
    | PCI             | GHI / Household Size (Làm tròn 2 số)    |

  Examples:
    | Household_Size | GHI (SGD) | Expected_PCI (SGD) | MOEFAS_Eligibility_Check (GHI <= 3000 OR PCI <= 750) |
    | 4              | 2,800.00  | 700.00             | Đạt (Thỏa cả GHI và PCI)                             |
    | 5              | 3,500.00  | 700.00             | Đạt (GHI > 3000 nhưng PCI <= 750)                   |
    | 4              | 2,900.00  | 725.00             | Đạt (GHI <= 3000 dù PCI = 725)                       |
    | 3              | 3,600.00  | 1,200.00           | Không đạt MOEFAS (Chuyển xét duyệt SBFAS)            |
```

#### AC-FAS-04: Step 3 & Step 4 - Hồ sơ Đính kèm & Hoàn cảnh Gia đình
```gherkin
Scenario: Bước 3 & Bước 4 - Đính kèm tài liệu và nhập giải trình hoàn cảnh
  Given Phụ huynh đang ở Step 3 - Documents
  When Phụ huynh tải tài liệu đính kèm (Chứng nhận y tế/Khuyết tật/Ly hôn)
  Then Validate file: Định dạng hợp lệ (.pdf, .jpg, .png), kích thước < 5MB/file
  And Cờ cam kết SBFAS: "If not eligible for MOEFAS, I agree to forward my application to the school(s) for School-Based FAS (SBFAS) consideration"
  And Cờ này mặc định được tích chọn "YES"
  When Phụ huynh chuyển sang Step 4 - Context
  Then Cung cấp ô textarea cho phép nhập giải trình hoàn cảnh tối đa 2,000 ký tự
  And Bộ đếm ký tự thời gian thực hiển thị "N / 2000 characters"
  And Hệ thống tự động lọc và mã hóa ký tự (Sanitize HTML) để chống lỗi bảo mật XSS
```

#### AC-FAS-05: Step 5 - Tính năng AI Auto-fill (US-AI3) & Review Đơn
```gherkin
Scenario: Bước 5 - Tổng hợp dữ liệu thông minh qua AI Auto-fill và gửi đơn
  Given Phụ huynh đã cung cấp thông tin hoặc đã trao đổi qua AI Assistant trước đó
  When Phụ huynh mở Step 5 - Review & Submit
  Then Tính năng AI Auto-fill kích hoạt:
    | Nguồn Dữ liệu   | Hành động AI Auto-fill                                       |
    | Singpass Profile| Điền sẵn nhân khẩu học, địa chỉ thường trú                   |
    | CPF / IRAS API  | Chuẩn hóa cơ cấu thu nhập GHI / PCI                          |
    | AI Chat Context | Tóm tắt hoàn cảnh khó khăn thành văn bản súc tích vào form   |
  And Hiển thị thẻ tóm tắt tổng thể (Summary Bento Card) gồm:
    | Danh sách con nộp đơn | Mức GHI & PCI tính toán | Dự báo diện trợ cấp (MOEFAS / SBFAS) |
  And Phụ huynh bắt buộc phải tích chọn cam đoan: "I declare that all information provided is true and complete."
  When Phụ huynh bấm "Submit Application"
  Then Nút bấm disabled chống double-submit và đơn được gửi lên hệ thống
```

#### AC-FAS-06: Tách Đơn Gia đình thành Đơn Con & Đẩy sang Admin Portal (R4)
```gherkin
Scenario: Xử lý sau khi nộp đơn gia đình thành công
  Given Đơn FAS gia đình chứa 2 đứa con (Con A - Tiểu học Trường X, Con B - Trung học Trường Y)
  When Đơn Submit thành công
  Then Hệ thống lưu bản ghi gốc `Family_FAS_Application`
  And Tự động tách thành 2 bản ghi đơn con độc lập:
    | Đơn con | Học sinh | Trường thụ lý     | Trạng thái ban đầu |
    | FAS-01  | Con A    | Trường Tiểu học X | Submitted          |
    | FAS-02  | Con B    | Trường Trung học Y| Submitted          |
  And Đơn lập tức xuất hiện trên giao diện Admin Portal (R4) của từng trường tương ứng
```

#### AC-FAS-07: Tiến trình 4 Mốc (Timeline Tracking) - Nhánh MOEFAS Tự động
```gherkin
Scenario: Đơn đạt chuẩn MOEFAS toàn quốc - Tự động phê duyệt (Auto-Grant)
  Given Đơn gia đình có PCI <= 750 SGD (Đạt chuẩn MOEFAS)
  When Phụ huynh mở màn hình theo dõi Timeline trên e-Service Portal
  Then Tiến trình 4 mốc hiển thị:
    | Mốc Timeline            | Trạng thái Hiển thị | Chi tiết                                                      |
    | 1. Submitted            | Completed (Green)   | Đơn đã nộp thành công                                         |
    | 2. System Check         | Completed (Green)   | Hệ thống kiểm tra điều kiện tự động: "PASSED (MOE Criteria)"  |
    | 3. Review by School     | Skipped (N/A)       | Bỏ qua duyệt trường (Do hệ thống tự động Auto-Grant)          |
    | 4. Decision             | Active (Green)      | "APPROVED - MOEFAS (100% Fee Subsidy)"                        |
  And Hiển thị bảng chi tiết số tiền học phí được miễn giảm cho từng con
```

#### AC-FAS-08: Tiến trình 4 Mốc (Timeline Tracking) - Nhánh Chuyển Xét SBFAS
```gherkin
Scenario: Đơn không đạt MOEFAS nhưng phụ huynh đồng ý xét SBFAS cấp trường
  Given Đơn gia đình có GHI = 3,600 SGD, PCI = 900 SGD (Vượt trần MOEFAS)
  When Phụ huynh mở màn hình theo dõi Timeline
  Then Tiến trình 4 mốc hiển thị:
    | Mốc Timeline            | Trạng thái Hiển thị | Chi tiết                                                      |
    | 1. Submitted            | Completed (Green)   | Đơn đã nộp thành công                                         |
    | 2. System Check         | Completed (Amber)   | "Not eligible for MOEFAS. Forwarded to School for SBFAS."     |
    | 3. Review by School     | In Progress (Blue)  | "Under Review by [Tên Trường] Admin Committee"                |
    | 4. Decision             | Pending (Grey)      | Chờ quyết định từ Ban Giám Hiệu trường                        |
```

---

### 3.3. Bảng Ma trận Test Cases chi tiết (Phân hệ R10 - Family FAS)

| TC ID | Kịch bản Kiểm thử | Phân loại | Điều kiện Tiền đề | Các Bước Thực hiện | Dữ liệu Đầu vào | Kết quả Kỳ vọng | Mức độ |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-FAS-01** | Kiểm tra danh sách con hợp lệ tại Step 1 | Functional | Phụ huynh có 3 con (14 tuổi, 16 tuổi, và 10 tuổi đang có đơn Pending) | 1. Mở FAS Wizard Step 1<br>2. Kiểm tra checkbox từng con | N/A | Con 14 tuổi: Checkbox Active.<br>Con 16 tuổi: Disabled (Đủ 16 tuổi).<br>Con 10 tuổi: Disabled (Đang chờ duyệt). | **P1** |
| **TC-FAS-02** | Chọn mối quan hệ bắt buộc tại Step 1 | Validation | Đang ở Step 1 | 1. Tích chọn con hợp lệ<br>2. Để trống ô Relationship<br>3. Bấm Next | Relationship = None | Báo lỗi inline: "Please select your relationship with the child". Không cho qua Step 2. | **P2** |
| **TC-FAS-03** | Tự động kéo thu nhập từ CPF/IRAS API tại Step 2 | Integration | API Chính phủ hoạt động bình thường | 1. Chuyển sang Step 2<br>2. Kiểm tra bảng thu nhập | NRIC Phụ huynh | Tự động hiển thị chính xác thu nhập Cha/Mẹ từ API. Ô nhập liệu ở trạng thái Read-only. | **P1** |
| **TC-FAS-04** | API Chính phủ bị Timeout (>10s) tại Step 2 | Exception / Network | Giả lập Gov API bị timeout | 1. Chuyển sang Step 2<br>2. Hệ thống gọi API timeout | Timeout > 10s | Hiển thị thông báo `MSG-0809`: "We could not retrieve your information. Please try again later." Cho phép thử lại. | **P1** |
| **TC-FAS-05** | Thêm thành viên thất nghiệp / trẻ em | Functional | Đang ở Step 2 | 1. Bấm "+ Add member"<br>2. Nhập thông tin con dưới 6 tuổi<br>3. Tích chọn "Unemployed / Child" | Thu nhập = 0$ | Thêm thành viên thành công. Household Size tăng 1, GHI giữ nguyên, PCI tự động giảm tương ứng. | **P2** |
| **TC-FAS-06** | Tính toán công thức GHI và PCI chính xác | Functional / Math | Step 2 có 4 thành viên | 1. Nhập thu nhập: Cha 1,800$, Mẹ 1,200$, 2 con 0$ | GHI = 3,000$, Size = 4 | GHI = 3,000.00 SGD. Household Size = 4. PCI = 750.00 SGD. Đánh giá sơ bộ: "Meets MOEFAS Criteria". | **P1** |
| **TC-FAS-07** | Upload tài liệu hợp lệ tại Step 3 | Functional | Đang ở Step 3 | 1. Đính kèm file PDF 2MB<br>2. Kiểm tra danh sách đính kèm | file.pdf (2MB) | Upload thành công. Hiển thị tên file, dung lượng và nút xóa. | **P2** |
| **TC-FAS-08** | Upload file quá dung lượng (>5MB) tại Step 3 | Validation / Security | Đang ở Step 3 | 1. Đính kèm file 6MB<br>2. Kiểm tra validate | file.pdf (6MB) | Báo lỗi ngay lập tức: "File size exceeds the 5MB limit. Please upload a smaller file." Chặn upload. | **P2** |
| **TC-FAS-09** | Upload file sai định dạng (.exe, .zip) tại Step 3 | Security | Đang ở Step 3 | 1. Cố ý đính kèm file malware.exe | malware.exe | Báo lỗi: "Invalid file format. Only PDF, JPG, and PNG are allowed." | **P1** |
| **TC-FAS-10** | Nhập văn bản giải trình vượt 2,000 ký tự tại Step 4 | Boundary Value | Đang ở Step 4 | 1. Nhập chuỗi 2,005 ký tự vào ô Context | Chuỗi 2,005 ký tự | Ô input tự động cắt ngắn ở ký tự 2,000. Bộ đếm hiển thị "2000 / 2000 characters". | **P2** |
| **TC-FAS-11** | Chống tấn công XSS trong ô Context tại Step 4 | Security / XSS | Đang ở Step 4 | 1. Nhập payload script: `<script>alert('xss')</script>`<br>2. Tiếp tục sang Step 5 | Payload XSS | Ký tự được sanitize an toàn thành dạng thực thể text. Không thực thi script trên màn hình Review hoặc Admin Portal. | **P1** |
| **TC-FAS-12** | AI Auto-fill tổng hợp form chính xác tại Step 5 | Functional / AI | Hoàn tất Step 1-4 | 1. Mở Step 5<br>2. Kiểm tra các trường dữ liệu AI điền sẵn | US-AI3 Trigger | Mọi dữ liệu khớp chính xác 100% với các bước trước. Bản tóm tắt Bento Card hiển thị trực quan, mạch lạc. | **P1** |
| **TC-FAS-13** | Tách đơn gộp thành các đơn con tương ứng tại các trường | Integration / E2E | Đơn gia đình cho 2 con học 2 trường khác nhau | 1. Submit đơn tại Step 5<br>2. Đăng nhập Admin Portal trường X & trường Y | Con A (Trường X), Con B (Trường Y) | Đơn được phân tách chính xác: School Admin trường X thấy hồ sơ Con A; School Admin trường Y thấy hồ sơ Con B. | **P1** |
| **TC-FAS-14** | Timeline Tracking: Đạt chuẩn MOEFAS Auto-Grant | End-to-End | Đơn có PCI = 650$ | 1. Submit đơn<br>2. Xem Timeline trên Portal | PCI <= 750$ | Mốc 1: Completed. Mốc 2: Passed. Mốc 3: Skipped. Mốc 4: Approved MOEFAS ngay lập tức. | **P1** |

---

## 4. KỊCH BẢN KIỂM THỬ PHI CHỨC NĂNG & BẢO MẬT

### 4.1. Bảo mật & Xác thực (Security ASVS)
1. **Xác thực Webhook HMAC-SHA256**:
   * Gửi request giả mạo tới `/api/payments/webhook` với chữ ký sai $\rightarrow$ Hệ thống lập tức từ chối với mã HTTP `401 Unauthorized`, không thay đổi trạng thái hóa đơn.
2. **Kiểm soát Truy cập Dọc/Ngang (IDOR Prevention)**:
   * Phụ huynh A cố tình đổi tham số `invoiceId` hoặc `studentId` trên URL sang con của Phụ huynh B $\rightarrow$ Hệ thống đối soát Session Singpass NRIC, chặn truy cập và trả về HTTP `403 Forbidden` kèm ghi nhận Audit Log.
3. **Session Expiry**:
   * Phiên làm việc của Phụ huynh tự động hủy sau **15 phút không thao tác**. Mọi request sau 15 phút đều bị điều hướng về màn hình đăng nhập Singpass.

### 4.2. Hiệu năng & Khả năng Chịu tải (Performance & Resiliency)
1. **Tải đỉnh mùa nộp học phí (Back-to-School Peak)**:
   * Đáp ứng đồng thời 2.000 phụ huynh đăng nhập và thanh toán qua Split Payment trong 1 phút mà không phát sinh lỗi Deadlock trên bảng Ledger.
2. **Khả năng Phục hồi khi Gateway Offline**:
   * Nếu Sandbox Payment Gateway gặp sự cố sập nguồn (503 Service Unavailable), hệ thống tự động giữ hóa đơn ở trạng thái `Issued`, không trừ số dư EA của phụ huynh.
