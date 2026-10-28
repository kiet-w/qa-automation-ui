# FS09: Outstanding Fees & Payment

## 1. Phân Hệ Tổng Quan
- **Mã phân hệ**: `FS09` (Requirement R9, Function 9)
- **Tên nghiệp vụ**: Outstanding Fees and Payment (Phí còn nợ và thanh toán)
- **Đường dẫn ứng dụng**:
  - Chọn con: `http://localhost:5174/billing` (SCR-01)
  - Thanh toán phí: `http://localhost:5174/billing/{studentId}` (SCR-02 đến SCR-05)
  - Cổng thanh toán Sandbox: `http://localhost:5286/checkout/{token}`
  - Biên lai & Kết quả: `http://localhost:5174/payment-result` (SCR-07 & SCR-08)
- **Đối tượng sử dụng**: Phụ huynh / Người giám hộ học sinh (đăng nhập qua Singpass)
- **Mục tiêu**: Cho phép phụ huynh tra cứu toàn bộ các khoản phí còn nợ của con cái, lựa chọn thanh toán linh hoạt qua 3 phương thức: 100% Tài khoản Giáo dục (Education Account - EA), 100% Cổng thanh toán trực tuyến (Online Gateway), hoặc Chia đôi (Split: EA + Online), đi kèm cơ chế bù trừ hoàn tiền tự động (SAGA Compensation Reversal) đảm bảo an toàn tuyệt đối.

---

## 2. Mục Lục Đặc Tả Thành Phần Đơn Lẻ (Atomic Component Specs)

Tất cả các tài liệu thành phần đơn lẻ tuân thủ đầy đủ cấu trúc 5 phần chuẩn hóa:

| Component File | Tên Thành Phần & Chức Năng | Route & Selector Chính | BR / AC Traceability |
| :--- | :--- | :--- | :--- |
| [`account_selection_card.md`](./atomic/account_selection_card.md) | **Account Selection Card**: Hiển thị danh sách thẻ tài khoản con cái liên kết, tên học sinh, trường lớp, nhãn trạng thái nợ, trạng thái rỗng SCR-03, và phân trang. | `/billing`<br>`h1#billing-account-selection-heading`<br>`ul.accountGrid > li` | `BR-F9-01`<br>`AC-01`, `AC-12`<br>`EX-01` |
| [`outstanding_charges_table.md`](./atomic/outstanding_charges_table.md) | **Outstanding Charges Table**: Bảng danh sách các khoản phí nợ, checkbox từng dòng, checkbox Select All, bộ lọc trạng thái, 3 thẻ tóm tắt (Phí nợ, Số dư EA, Tổng chọn). | `/billing/{studentId}` (SCR-02)<br>`h2#billing-charges-heading`<br>`table tbody tr` | `BR-F9-04`, `BR-F9-07`<br>`BR-F9-12`, `BR-F9-13`<br>`AC-02`, `AC-03`, `AC-11` |
| [`payment_method_selector.md`](./atomic/payment_method_selector.md) | **Payment Method Selector**: Nhóm radio 3 phương thức thanh toán (EA, Split, Online), kiểm tra tính khả dụng động dựa trên số dư EA so với Net, thông báo lý do không đủ điều kiện. | `/billing/{studentId}` (SCR-04)<br>`h2#billing-method-heading`<br>`input[value='EducationAccount']` | `BR-F9-02`, `BR-F9-07`<br>`BR-F9-10`<br>`AC-04`, `AC-14`, `AC-22` |
| [`split_payment_amount_input.md`](./atomic/split_payment_amount_input.md) | **Split Payment Amount Input**: Ô nhập số tiền trích từ EA với 2 chữ số thập phân SGD, kiểm tra biên BVA ($0 < EA < Net$), đồng bộ thời gian thực phần trực tuyến $Online = Net - EA$. | `/billing/{studentId}` (SCR-04)<br>`input[inputmode='decimal']`<br>`div.fundingBreakdown` | `BR-F9-10`, `BR-F9-11`<br>`AC-15`, `AC-16`, `AC-19` |
| [`payment_review_and_confirm.md`](./atomic/payment_review_and_confirm.md) | **Payment Review & Authorization**: Bảng xem lại các khoản phí, cơ cấu nguồn tiền, dự báo số dư EA sau thanh toán, khóa nút chống click đúp, gắn `Idempotency-Key`. | `/billing/{studentId}` (SCR-05)<br>`h2#billing-review-heading`<br>`button:has-text('Authorize & pay')` | `BR-F9-04`, `BR-F9-09`<br>`BR-F9-13`<br>`AC-05`, `AC-17` |
| [`payment_gateway_simulator.md`](./atomic/payment_gateway_simulator.md) | **Payment Gateway Simulator**: Cổng checkout sandbox mô phỏng thanh toán thẻ/PayNow, hiển thị mã tham chiếu, nút "Pay successful" và "Pay failed", chống replay token đã hoàn tất. | `:5286/checkout/{token}`<br>`h1#checkout-title`<br>`button:has-text('Pay successful')` | `BR-F9-09`<br>`AC-07`, `AC-08`<br>`AC-18`, `AC-20` |
| [`payment_result_receipt.md`](./atomic/payment_result_receipt.md) | **Payment Result & Receipt**: Banner trạng thái Thành công / Thất bại, biên lai điện tử chuẩn MOE, thông báo hoàn tiền EA tự động (`EA_REVERSAL_NOTICE`) khi thanh toán trực tuyến trong gói Split bị lỗi. | `/payment-result` (SCR-07, 08)<br>`h1#payment-result-heading`<br>`div.resultStatus` | `BR-F9-05`, `BR-F9-06`<br>`BR-F9-14`<br>`AC-06`, `AC-08`, `AC-20` |

---

## 3. Mục Lục Đặc Tả Luồng Tích Hợp (Integration Flow Specs)

Các tài liệu luồng tích hợp tuân thủ cấu trúc 5 phần chuẩn hóa:

| Integration Flow File | Tên Luồng Nghiệp Vụ & Quy Trình | Vai Trò & Điểm Nổi Bật | Trạng Thái Chuyển Đổi Chính |
| :--- | :--- | :--- | :--- |
| [`full_ea_payment_flow.md`](./integration/full_ea_payment_flow.md) | **Full Education Account Payment**: Luồng thanh toán 100% học phí bằng số dư Tài khoản Giáo dục nội bộ, ghi nợ sổ cái tức thì và xuất biên lai không cần cổng thanh toán ngoài. | Học sinh Citizen có EA Active và số dư $\ge Net$ | `SCR-01` ➔ `SCR-02`<br>➔ `SCR-04` (EA)<br>➔ `SCR-05`<br>➔ `SCR-07` (Paid) |
| [`full_online_payment_flow.md`](./integration/full_online_payment_flow.md) | **Full Online Gateway Payment**: Luồng thanh toán trực tuyến thẻ tín dụng/PayNow qua cổng sandbox ngoài, điều hướng trình duyệt và xác thực chữ ký webhook `HMAC-SHA256`. | Học sinh ngoại quốc, PR, hoặc số dư EA = 0 | `SCR-02` ➔ `SCR-04` (Online)<br>➔ Checkout Sandbox (:5286)<br>➔ Webhook Callback<br>➔ `SCR-07` (Paid) / `SCR-08` (Failed) |
| [`split_payment_and_reversal_flow.md`](./integration/split_payment_and_reversal_flow.md) | **Split Payment & Automated Reversal (SAGA)**: Luồng chia đôi nguồn tiền 2 chân (Leg 1: EA, Leg 2: Online). Nếu Leg 2 thất bại, hệ thống tự động hoàn tiền EA tức thì và hoàn nguyên hóa đơn về `Issued`. | Phụ huynh có số dư EA $> 0$ nhưng $< Net$ | Leg 1 Settled ➔ Leg 2 Fails<br>➔ Auto Reverse Leg 1 (+EA)<br>➔ Invoice `Issued`<br>➔ Banner Reversal Notice |

---

## 4. Bảng Tra Cứu Mã Lỗi Nghiệp Vụ (Error Catalog)

| Mã Lỗi Hệ Thống | Thông Báo Chuẩn Trên Giao Diện | Ngữ Cảnh Kích Hoạt | Xử Lý UI & Trạng Thái |
| :--- | :--- | :--- | :--- |
| `EA_NOT_AVAILABLE` | *"This student does not have an Education Account. Please pay online."* | Học sinh không phải công dân Singapore (PR, Foreigner) | Vô hiệu tùy chọn EA/Split, tự động chọn Online |
| `EA_NOT_ACTIVE` | *"The Education Account is not active. Please pay online."* | Tài khoản EA của học sinh đang ở trạng thái `Closed` hoặc `Suspended` | Vô hiệu tùy chọn EA/Split |
| `EA_INSUFFICIENT_BALANCE`| *"Your Education Account balance is not enough for this amount. You can pay the rest online."* | Số dư EA nhỏ hơn tổng Net khi cố chọn Full EA | Gợi ý sử dụng phương thức Chia đôi (Split) |
| `SPLIT_AMOUNT_INVALID` | *"The two amounts must be more than zero and add up to the total."* | Ô chia tiền EA bị để trống, nhập số $\le 0$, hoặc bằng đúng tổng Net | `aria-invalid="true"`, viền đỏ, chặn Continue |
| `INVOICE_ALREADY_PAID` | *"This invoice has already been paid."* | Hóa đơn đã được thanh toán bởi kênh khác hoặc phụ huynh khác | Banner cảnh báo đỏ, làm mới lại danh sách phí |
| `FORBIDDEN_CHILD` | *"You do not have access to this student's records."* | Phụ huynh cố tình truy cập vào ID của học sinh không liên kết | Chặn truy cập BOLA/IDOR, chuyển về `/billing` |
| `EA_REVERSAL_NOTICE` | *"The amount deducted from your Education Account has been returned to your balance."* | Thanh toán trực tuyến trong giao dịch Split bị thất bại | Khối thông báo hoàn tiền nổi bật trên màn hình kết quả |
