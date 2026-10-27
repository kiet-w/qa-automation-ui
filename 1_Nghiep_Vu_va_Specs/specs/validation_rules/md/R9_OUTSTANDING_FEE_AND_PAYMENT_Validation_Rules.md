# R9_OUTSTANDING FEE AND PAYMENT_Validation_Rules


TÀI LIỆU QUY TẮC VALIDATION

Requirement R9, Function 9: Phí còn nợ và thanh toán (Outstanding Fees and Payment)

Dành cho Dev. Dựa trên FS Function 9 (FS09.md và [Agile] FS 09.docx).

| Mục | Nội dung |
| :--- | :--- |
| Dự án | Agileproject, hệ thống tài chính MOE, EAFAMS |
| Phiên bản | Bản nháp 0.2, 25/10/2026 |
| Tác giả | QA |
| Nguồn chính | FS Function 9, mục 3.1.1, 3.1.2, 4.1, 4.2, 5.1, 5.3, Appendix A, B, C |
| Nguồn khác | R9_Test_Cases_final_FS09.xlsx (153 case, BUG-R9-001 đến BUG-R9-023)<br>F9_Dev_Local_Run_Results.md<br>README và data/ui_text.py của r9_automation |
| Tệp đi kèm | R9_Seed_Data.xlsx<br>R9_seed.sql |
| Hình | Màn A đến D là ảnh chụp thật từ e-service localhost:5174 ngày 25/10/2026, QA đánh dấu mã trường<br>Màn E đến G là sơ đồ QA vẽ từ FS 4.1 và Appendix C, vì cần giao dịch thật để chụp<br>FS 09 không có hình màn hình |
| Trạng thái | Chờ BA xác nhận các điểm mở |


# 1. Phạm vi


| Màn | Nội dung | Màn trong FS |
| :--- | :--- | :--- |
| A | Chọn con | SCR-01 |
| B | Phí chưa thanh toán và trạng thái rỗng | SCR-02, SCR-03 |
| C | Chọn cách thanh toán | SCR-04 |
| D | Xem lại và xác nhận | SCR-05 |
| E | Đang chờ xử lý | SCR-06 |
| F | Xác nhận thanh toán | SCR-07 |
| G | Thanh toán thất bại | SCR-08 |
| Mục 10 | Quy tắc máy chủ và API (không có màn hình) | BR-F9, EX, FS 4.2 |


# 2. Quy ước


| Mục | Quy tắc |
| :--- | :--- |
| Số đỏ trong hình | Bằng mã trường ở tiêu đề bên dưới, ví dụ khung C3 là mục C3 |
| Nguồn trong FS | Mục, quy tắc nghiệp vụ (BR), ngoại lệ (EX) hoặc tiêu chí chấp nhận (AC) đứng sau quy tắc |
| Thông báo | Nguyên văn FS mục 5.1 |
| Đề xuất QA | Không có trong FS. BA xác nhận trước khi Dev xây |
| Mọi ô nhập | Là dữ liệu, không bao giờ là mã<br>Truy vấn có tham số<br>Đầu ra mã hóa HTML<br>Không phân tích như JSON, XML, template hay lệnh<br>Bỏ ký tự điều khiển<br>Lưu Unicode |
| Ngôn ngữ giao diện | Chỉ tiếng Anh |
| Vai trò | Parent hoặc Guardian đăng nhập qua Singpass<br>Chỉ xem và trả invoice của con đã liên kết<br>Máy chủ kiểm tra liên kết ở mọi API |
| Tiền tệ | SGD, Decimal(18,2), hiển thị dạng 1,590.00 (đề xuất QA) |
| Ngày giờ | DD/MM/YYYY, giờ Singapore SGT, lưu UTC (đề xuất QA, theo BR16 của FS F4) |
| FS mục 5.2 | Không có, đánh số nhảy từ 5.1 sang 5.3. VAL-18 ở NQ-13 không có mô tả |


# 3. Màn A. Chọn con (SCR-01)


Mở sau khi Parent đăng nhập Singpass. Chỉ liệt kê con đã liên kết. Nguồn: FS 3.1.2 bước 1, FS 4.1 SCR-01, Appendix C.

Hình A. Ảnh chụp e-service tại localhost:5174 ngày 25/10/2026, persona MockPass S7890123F, QA đánh dấu mã trường

Bản build chưa hiển thị A3 và A4 (BUG-R9-001). Bốn trong sáu thẻ (Test Child One, Two, Three và Tan Wei Ming) có liên kết /billing/null, mở ra lỗi Unable to load education account.

## 3.1. Tóm tắt trường


| Mã | Trường | Loại |
| :--- | :--- | :--- |
| A1 | Thẻ con | Nút |
| A2 | Tên học sinh | Chỉ hiển thị |
| A3 | Trường, Level, Lớp | Chỉ hiển thị |
| A4 | Nhãn có hay không có phí chưa thanh toán | Chỉ hiển thị |
| A5 | Trạng thái rỗng, lỗi, đang tải | Chỉ hiển thị |


## 3.2. Quy tắc trường


### A1. Thẻ con


| Mục | Quy tắc |
| :--- | :--- |
| Chức năng | Mở phí chưa thanh toán của con (SCR-02) |
| Hiển thị khi | Mỗi con đã liên kết một thẻ |
| Vô hiệu khi | Không |
| Khi bấm | Máy chủ kiểm tra liên kết Parent và Student<br>Có liên kết: mở SCR-02<br>Không còn liên kết: FORBIDDEN_CHILD, về SCR-01 |
| Khi bấm đúp | Mở một lần |
| Khi lỗi | Something went wrong. Please try again later. |
| Nguồn trong FS | FS 3.1.2 bước 1 và 2, BR-F9-01, EX-01, AC-01, AC-12 |


| Mã | Trường | Hiển thị | Quy tắc | Nguồn trong FS |
| :--- | :--- | :--- | :--- | :--- |
| A2 | Tên học sinh | Họ tên | Chỉ con của Parent đang đăng nhập<br>Thứ tự A đến Z (đề xuất QA) | FS 4.1 SCR-01, BR-F9-01, AC-01 |
| A3 | Trường, Level, Lớp | Tên trường, Level (còn gọi Cohort), Lớp | Bắt buộc có | FS 4.1 SCR-01, FS 1.4 |
| A4 | Nhãn nợ | Has outstanding invoices hoặc No outstanding invoices (đề xuất QA) | Tính từ invoice Issued<br>Con chỉ có invoice PaymentPending, Paid hoặc Cancelled thì không có nợ | FS 4.1 SCR-01, Appendix C |
| A5 | Trạng thái rỗng, lỗi, đang tải | Loading / Empty / Error | Empty: không có thẻ, hướng dẫn liên hệ trường (You have no linked student. Please contact your school., đề xuất QA)<br>Error: Something went wrong. Please try again later., cho thử lại<br>Đăng nhập thất bại hoặc hủy: không có session, hiển thị lỗi | FS 3.1.2 bước 1 luồng thay thế, mục 5.1 |


## 3.3. Điểm mở của màn A


| Trường | Điểm mở |
| :--- | :--- |
| A1 | Parent chỉ có một con: FS nói có thể chuyển thẳng SCR-02. Chưa chốt. Xem O10 |
| A3, A4 | Build local chưa hiển thị trường, level, lớp và nhãn nợ (BUG-R9-001). Xem O9 |


# 4. Màn B. Phí chưa thanh toán (SCR-02, SCR-03)


Mở sau khi chọn con. Parent trả cả invoice, không trả từng dòng, không trả một phần. Không có invoice Issued thì hiển thị trạng thái rỗng SCR-03. Nguồn: FS 3.1.2 bước 2 và 3, FS 4.1 SCR-02, DA-05, BR-F9-13, Appendix C.

Hình B. Ảnh chụp e-service tại localhost:5174 ngày 25/10/2026, persona MockPass S7890123F, QA đánh dấu mã trường

Bản build hiển thị danh sách khoản phí phẳng (BUG-R9-003). Chưa thấy B3, B4, B5, B7, B12 và B15. Cột trạng thái bị cắt, phải cuộn ngang. Dữ liệu: con Lucas Lim (STU-005), hai khoản 19.50 và 25.00, tổng 44.50, số dư EA 650.00.

## 4.1. Tóm tắt trường


| Mã | Trường | Loại |
| :--- | :--- | :--- |
| B1 | Chọn con | Chọn |
| B2 | Số dư EA | Chỉ hiển thị |
| B3 | Trạng thái EA | Chỉ hiển thị |
| B4 | Số invoice | Chỉ hiển thị |
| B5 | Fee type | Chỉ hiển thị |
| B6 | Mô tả dòng | Chỉ hiển thị |
| B7 | Fee component (kể cả GST) | Chỉ hiển thị |
| B8 | Gross amount | Chỉ hiển thị |
| B9 | Subsidy amount | Chỉ hiển thị |
| B10 | Net amount | Chỉ hiển thị |
| B11 | Trạng thái invoice | Chỉ hiển thị |
| B12 | Hạn nộp | Chỉ hiển thị |
| B13 | Tổng còn nợ | Chỉ hiển thị |
| B14 | Nút Pay | Nút |
| B15 | Nút quay lại danh sách con | Nút |
| B16 | Trạng thái rỗng (SCR-03), lỗi, đang tải | Chỉ hiển thị |


## 4.2. Quy tắc trường


### B1. Chọn con


| Mục | Quy tắc |
| :--- | :--- |
| Lựa chọn | Các con đã liên kết |
| Mặc định | Con đã chọn ở SCR-01 |
| Bắt buộc | Có, luôn một con |
| Phụ thuộc | Không |
| Khi đổi | Tải lại invoice và số dư EA<br>Bỏ chọn invoice cũ<br>Máy chủ kiểm tra lại liên kết |
| Thông báo | Không còn liên kết: You do not have access to this student's records. (FORBIDDEN_CHILD), về SCR-01 |
| Nguồn trong FS | FS 3.1.2 bước 2, EX-01, AC-12, Appendix C |


### B14. Nút Pay


| Mục | Quy tắc |
| :--- | :--- |
| Chức năng | Chọn invoice để sang SCR-04 |
| Hiển thị khi | Invoice Issued và không có transaction đang mở |
| Vô hiệu khi | Invoice PaymentPending (đề xuất QA)<br>Con từ 16 tuổi (xem O22) |
| Khi bấm | Sang SCR-04 với một invoice<br>Máy chủ kiểm tra lại trạng thái<br>Đã Paid: INVOICE_ALREADY_PAID, làm mới danh sách<br>Bị hủy: INVOICE_NOT_PAYABLE, làm mới danh sách<br>Đang xử lý: PAYMENT_PENDING, sang SCR-06 |
| Khi bấm đúp | Mở một lần |
| Khi lỗi | Something went wrong. Please try again later. |
| Nguồn trong FS | FS 4.1 Selected invoice, BR-F9-04, BR-F9-09, EX-03, EX-04, EX-14, AC-11, AC-21 |


### B15. Nút quay lại danh sách con


| Mục | Quy tắc |
| :--- | :--- |
| Chức năng | Về SCR-01 |
| Hiển thị khi | Luôn, kể cả ở SCR-03 |
| Vô hiệu khi | Không |
| Khi bấm | Về SCR-01<br>Không đổi dữ liệu |
| Khi bấm đúp | Một lần |
| Khi lỗi | Không |
| Nguồn trong FS | FS 3.1.2 bước 3, Appendix C |


| Mã | Trường | Hiển thị | Quy tắc | Nguồn trong FS |
| :--- | :--- | :--- | :--- | :--- |
| B2 | Số dư EA | Số dư khả dụng, SGD | Chỉ khi con có EA<br>Không có EA (PR, học sinh nước ngoài): ghi chú không có Education Account, không báo lỗi<br>Hai chữ số thập phân, không âm | FS 3.1.2 bước 2, FS 4.1, DA-03, BR-F9-07, AC-14 |
| B3 | Trạng thái EA | Active hoặc Closed | Chỉ Active mới dùng để trả<br>Closed: EA và chia đôi bị vô hiệu, EA_NOT_ACTIVE | FS 4.1, BR-F9-02, DA-06, OOS 8 |
| B4 | Số invoice | Mã duy nhất | Bắt buộc, tối đa 50 ký tự, một dòng | FS 4.1, FS 4.2 |
| B5 | Fee type | School fee, miscellaneous, extracurricular, ad hoc | Dòng nhóm theo fee type | FS 4.1, DA-05 |
| B6 | Mô tả dòng | Tên khoản phí | Bắt buộc, mã hóa HTML | FS 4.1 |
| B7 | Fee component | Tên và số tiền từng thành phần, kể cả GST | Tổng bằng Gross của dòng<br>GST là một fee component | FS 4.1, DA-10, NQ-17 |
| B8 | Gross amount | Số tiền trước trợ cấp | Lớn hơn 0, snapshot khi phát hành | FS 4.1, BR-F9-12 |
| B9 | Subsidy amount | Số trợ cấp | Mặc định 0 ở Sprint 1, hiển thị 0.00<br>0 nhỏ hơn hoặc bằng Subsidy nhỏ hơn Gross | FS 4.1, BR-F9-08, BR-F9-12 |
| B10 | Net amount | Số phải trả | Bằng Gross trừ Subsidy, lớn hơn 0<br>Net invoice là tổng Net các dòng | FS 4.1, BR-F9-12, BR-F9-13 |
| B11 | Trạng thái invoice | Issued, PaymentPending, Paid, Cancelled | Không có Partially Paid<br>Draft không hiển thị<br>Nhãn chữ chưa có trong FS (O11) | FS 4.1, DA-05, Appendix A |
| B12 | Hạn nộp | Ngày hạn nộp | Bắt buộc sau khi phát hành, là hạn sớm nhất của các dòng<br>Hiển thị quá hạn chưa chốt (O7) | FS 4.1, OQ-04, NQ-03 |
| B13 | Tổng còn nợ | Tổng Net các invoice Issued (đề xuất QA) | Bằng tổng các dòng đang hiển thị<br>Hai chữ số thập phân | Appendix C SCR-02 |
| B16 | Trạng thái rỗng (SCR-03), lỗi, đang tải | Loading / Empty / Error | Empty: There are no outstanding fees for this child. (đề xuất QA) và liên kết về SCR-01<br>Error: Something went wrong. Please try again later., cho thử lại | FS 3.1.2 bước 3, AC-02 |


## 4.3. Điểm mở của màn B


| Trường | Điểm mở |
| :--- | :--- |
| B11, B14 | Invoice PaymentPending có nút hay không, SCR-02 có liệt kê Paid và Cancelled không (O9, O11). Build local ẩn khoản thuộc invoice PaymentPending (BUG-R9-004) |
| B12 | Hiển thị quá hạn chưa chốt. Case TC-026 đã bị bỏ (O7) |
| B7 | Build local hiển thị bảng phẳng, không mở rộng theo fee type (BUG-R9-003). FS chưa chốt nguồn fee component (O16) |
| B9 | Seed lấy trợ cấp FAS từ R4, khác BR-F9-08 (O19) |
| B15, B16 | Build local thiếu liên kết quay lại ở trạng thái rỗng (BUG-R9-007) |


# 5. Màn C. Chọn cách thanh toán (SCR-04)


Mở sau khi chọn một invoice Issued. Hiển thị tóm tắt invoice và ba cách: EA, trực tuyến, chia đôi. Chưa tạo dữ liệu nào ở màn này. Nguồn: FS 3.1.2 bước 4 và 5, BR-F9-02, BR-F9-07, BR-F9-10, BR-F9-11, Appendix C.

Hình C. Ảnh chụp e-service tại localhost:5174 ngày 25/10/2026, persona MockPass S7890123F, QA đánh dấu mã trường

Số dư EA 650.00 lớn hơn Net 44.50 nên chỉ có hai lựa chọn EA và Online Gateway, không có chia đôi, khớp FS 3.1.2 bước 4. Vì vậy C3, C4 và C5 chưa chụp được trên bản build này.

## 5.1. Tóm tắt trường


| Mã | Trường | Loại |
| :--- | :--- | :--- |
| C1 | Tóm tắt invoice | Chỉ hiển thị |
| C2 | Cách thanh toán (EA, trực tuyến, chia đôi) | Chọn |
| C3 | Số tiền phần EA (khi chia đôi) | Ô nhập số |
| C4 | Số tiền phần trực tuyến | Chỉ hiển thị |
| C5 | Lý do không đủ điều kiện | Chỉ hiển thị |
| C6 | Nút Tiếp tục | Nút |
| C7 | Nút Quay lại | Nút |


## 5.2. Quy tắc trường


### C6. Nút Tiếp tục


| Mục | Quy tắc |
| :--- | :--- |
| Chức năng | Sang xem lại và xác nhận (SCR-05) |
| Hiển thị khi | Luôn |
| Vô hiệu khi | Chưa chọn cách thanh toán (đề xuất QA) |
| Khi bấm | Máy chủ kiểm tra EA: tồn tại, Active, số dư khả dụng ≥ phần EA<br>Chia đôi: hai phần > 0, tổng bằng đúng Net, phần trực tuyến ≥ mức tối thiểu provider (TBC)<br>Đạt: sang SCR-05<br>Không đạt: ở lại SCR-04, hiển thị C5 kèm gợi ý<br>Không tạo transaction, không đổi invoice hay số dư |
| Khi bấm đúp | Mở một lần |
| Khi lỗi | EA_NOT_AVAILABLE, EA_NOT_ACTIVE, EA_INSUFFICIENT_BALANCE, SPLIT_AMOUNT_INVALID |
| Nguồn trong FS | FS 3.1.2 bước 5, BR-F9-02, BR-F9-11, AC-04, AC-19 |


### C7. Nút Quay lại


| Mục | Quy tắc |
| :--- | :--- |
| Chức năng | Rời màn mà không tạo dữ liệu |
| Hiển thị khi | Luôn |
| Vô hiệu khi | Không |
| Khi bấm | Về SCR-02 (đề xuất QA, FS không nêu đích)<br>Không tạo transaction, invoice vẫn Issued, số dư EA không đổi |
| Khi bấm đúp | Mở một lần |
| Khi lỗi | Không |
| Nguồn trong FS | Appendix C dòng SCR-04 |


### C2. Cách thanh toán


| Mục | Quy tắc |
| :--- | :--- |
| Lựa chọn | EA (kèm số dư), ONLINE, SPLIT (EA cộng trực tuyến) |
| Mặc định | FS không nêu (O3). Đề xuất QA: chỉ chọn sẵn, không trừ tiền trước khi xác nhận ở SCR-05. Số dư nhỏ hơn Net thì chọn sẵn chia đôi |
| Bắt buộc | Có, chọn một cách trước khi bấm Tiếp tục |
| Phụ thuộc | EA: con có EA Active và số dư ≥ Net<br>SPLIT: EA Active và số dư > 0<br>Số dư ≥ Net thì chỉ EA hoặc ONLINE (FS 3.1.2 bước 4, xem O2)<br>Không có EA: chỉ ONLINE (BR-F9-07)<br>ONLINE: luôn bật |
| Khi đổi | EA hoặc ONLINE: một phần bằng Net, ẩn C3 và C4<br>SPLIT: hiện C3 và C4<br>Mỗi lần đổi kiểm tra lại điều kiện EA |
| Thông báo | EA_NOT_AVAILABLE: This student does not have an Education Account. Please pay online.<br>EA_NOT_ACTIVE: The Education Account is not active. Please pay online.<br>EA_INSUFFICIENT_BALANCE: Your Education Account balance is not enough for this amount. You can pay the rest online. |
| Nguồn trong FS | FS 3.1.2 bước 4 và 5, BR-F9-02, BR-F9-07, BR-F9-10, DA-06, DA-08, AC-04, AC-14, AC-22 |


### C3. Số tiền phần EA (khi chia đôi)


| Quy tắc | Hợp lệ | Không hợp lệ | Thông báo |
| :--- | :--- | :--- | :--- |
| Kiểu và đơn vị | Số thập phân SGD, Decimal(18,2)<br>Chỉ hiện và nhập được khi SPLIT<br>Mặc định là số dư khả dụng, tối đa Net trừ 0.01 | Rỗng, chữ, S$20, dấu âm, 1e2, dấu phẩy thập phân | SPLIT_AMOUNT_INVALID: The two amounts must be more than zero and add up to the total. |
| Bắt buộc | Có khi SPLIT<br>Khi EA hoặc ONLINE thì ẩn và không gửi | Rỗng hoặc chỉ khoảng trắng | SPLIT_AMOUNT_INVALID |
| Độ dài và chữ số | Tối đa 12 ký tự<br>Tối đa 2 chữ số thập phân (đề xuất QA) | 20.001, giá trị dán quá 12 ký tự | SPLIT_AMOUNT_INVALID |
| Khoảng trắng | Bỏ khoảng trắng đầu và cuối | Khoảng trắng giữa số | SPLIT_AMOUNT_INVALID |
| Giá trị | 0 < phần EA < Net<br>Phần EA ≤ số dư khả dụng<br>Ví dụ với Net 70.63, số dư 20.00: 20, 20.00, 20.5 | 0, 0.00, -5, 70.63 (phần trực tuyến bằng 0), 70.64, 25.00 khi số dư 20.00 | 0, âm, tổng sai: SPLIT_AMOUNT_INVALID<br>Vượt số dư: EA_INSUFFICIENT_BALANCE: Your Education Account balance is not enough for this amount. You can pay the rest online. |
| Ký tự đặc biệt, script, JSON | Coi là văn bản, bị từ chối vì không phải số<br>Truy vấn có tham số | ' OR 1=1 --, <script>alert(1)</script>, {"a":1}, ${7*7}, ../../etc/passwd | SPLIT_AMOUNT_INVALID<br>Không thực thi, không hiển thị thành HTML |
| Ký tự điều khiển | Bỏ U+0000 đến U+001F và U+007F | Byte null, emoji | SPLIT_AMOUNT_INVALID |
| Liên quan C4 | C4 = Net trừ C3, dùng số thập phân, tổng hai phần bằng đúng Net<br>Đổi cách thanh toán hoặc invoice thì đặt lại C3<br>Số dư đổi trước khi xác nhận: EA_INSUFFICIENT_BALANCE, không tạo phiên trực tuyến (EX-05, AC-16) | Parent nhập tay C4 | Không |


Nguồn trong FS: FS 3.1.2 bước 4 và 5, FS 4.1 dòng EA amount và Online amount, BR-F9-02, BR-F9-10, BR-F9-11, AC-15, AC-16, AC-19, AC-22.

### Điểm mở của C3


| Trường | Điểm mở |
| :--- | :--- |
| C3 | FS mâu thuẫn: phần EA sửa được hay không (O1). Tài liệu viết theo cách đọc sửa được. Build local để chỉ đọc (BUG-R9-010) |
| C3 | Kiểu số và 2 chữ số thập phân là đề xuất QA vì FS không có mục 5.2 (O5) |


| Mã | Trường | Hiển thị | Quy tắc | Nguồn trong FS |
| :--- | :--- | :--- | :--- | :--- |
| C1 | Tóm tắt invoice | Con, số invoice, mô tả, Net, hạn nộp | Net = Net của invoice, 2 chữ số thập phân, không sửa được<br>Chỉ invoice Issued không có giao dịch đang mở | FS 3.1.2 bước 4, Appendix C |
| C4 | Phần trực tuyến | Net trừ C3 | Chỉ đọc, > 0, ≥ mức tối thiểu provider (TBC, O4)<br>Cập nhật ngay khi C3 đổi<br>Ví dụ 70.63 − 20.00 = 50.63 | FS 3.1.2 bước 4, BR-F9-11 |
| C5 | Lý do không đủ điều kiện | Mã lỗi và câu thông báo | Bốn mã: EA_NOT_AVAILABLE, EA_NOT_ACTIVE, EA_INSUFFICIENT_BALANCE, SPLIT_AMOUNT_INVALID<br>Câu nguyên văn FS 5.1 (mục 11)<br>Không đổi dữ liệu | FS 4.1, mục 5.1, AC-04, AC-19 |


## 5.3. Điểm mở của màn C


| Trường | Điểm mở |
| :--- | :--- |
| C2 | Chia đôi khi số dư đủ trả (O2), mặc định hay đề xuất tự động (O3), loại phí nào trả bằng EA (O8). Build local vô hiệu EA khi số dư thấp mà không hiện lý do (BUG-R9-009), EA Closed vẫn chọn được (BUG-R9-008) |
| C6 | Mức tối thiểu phần trực tuyến chưa chốt (O4) |
| C7 | FS không nêu đích nút Quay lại (O6) |


# 6. Màn D. Xem lại và xác nhận (SCR-05)


Màn cuối trước khi tạo giao dịch. Khi Parent xác nhận, hệ thống tạo transaction Pending cùng các funding leg và chuyển invoice sang PaymentPending. Nguồn: FS 3.1.2 bước 6, BR-F9-04, BR-F9-09, BR-F9-11, BR-F9-13, Appendix C.

Hình D. Ảnh chụp e-service tại localhost:5174 ngày 25/10/2026, persona MockPass S7890123F, QA đánh dấu mã trường

QA dừng trước nút Authorize and pay, không tạo giao dịch. Màn hiển thị số dư hiện tại 650.00, chưa có số dư sau thanh toán D4 (BUG-R9-012). Chưa thấy D5, vì key do client sinh và không hiển thị.

## 6.1. Tóm tắt trường


| Mã | Trường | Loại |
| :--- | :--- | :--- |
| D1 | Con và invoice | Chỉ hiển thị |
| D2 | Tổng phải trả | Chỉ hiển thị |
| D3 | Số tiền từng phần | Chỉ hiển thị |
| D4 | Số dư EA sau thanh toán | Chỉ hiển thị |
| D5 | Idempotency key | Giá trị ẩn do client sinh |
| D6 | Nút Xác nhận thanh toán | Nút |
| D7 | Nút Hủy | Nút |


## 6.2. Quy tắc trường


### D6. Nút Xác nhận thanh toán


| Mục | Quy tắc |
| :--- | :--- |
| Chức năng | Tạo giao dịch và bắt đầu xử lý theo cách đã chọn |
| Hiển thị khi | Luôn |
| Vô hiệu khi | Ngay sau lần bấm đầu, hiển thị Processing |
| Khi bấm | Gửi kèm idempotency key<br>Tạo transaction Pending và funding leg (mỗi leg có FundingReference riêng), invoice sang PaymentPending<br>EA: gọi Function 1 ghi nợ Net, thành công thì Paid, lỗi thì Failed, invoice về Issued, EA không đổi<br>Trực tuyến: tạo phiên provider, chuyển sang trang provider<br>Chia đôi: ghi nợ EA trước, chỉ khi thành công mới tạo phiên trực tuyến<br>Session hết hạn: AUTH_REQUIRED, chưa có transaction |
| Khi bấm đúp | Cùng key, một transaction và một lần trừ (AC-05)<br>Hai yêu cầu đồng thời: một thành công, một nhận PAYMENT_PENDING (409) |
| Khi lỗi | INVOICE_ALREADY_PAID, INVOICE_NOT_PAYABLE (làm mới danh sách), PAYMENT_PENDING (sang SCR-06), AUTH_REQUIRED |
| Nguồn trong FS | FS 3.1.2 bước 6, BR-F9-03, BR-F9-04, BR-F9-05, BR-F9-09, BR-F9-11, EX-02 đến EX-05, EX-10, AC-03, AC-05 đến AC-07, AC-16 |


### D7. Nút Hủy


| Mục | Quy tắc |
| :--- | :--- |
| Chức năng | Rời màn xem lại mà không thanh toán |
| Hiển thị khi | Luôn trước khi xác nhận |
| Vô hiệu khi | Sau khi đã xác nhận |
| Khi bấm | Về SCR-04 (đề xuất QA, FS không nêu đích)<br>Không tạo transaction, invoice vẫn Issued, số dư EA không đổi |
| Khi bấm đúp | Mở một lần |
| Khi lỗi | Không |
| Nguồn trong FS | Appendix C dòng SCR-05 |


### D5. Idempotency key


| Quy tắc | Hợp lệ | Không hợp lệ | Thông báo |
| :--- | :--- | :--- | :--- |
| Kiểu | Giá trị ẩn do client sinh mỗi lần xác nhận, gửi trong header Idempotency-Key | Thiếu key | 400 SYSTEM_ERROR (đề xuất QA) |
| Bắt buộc | Có (FS 4.1) | Rỗng | Từ chối, không tạo transaction |
| Độ dài | 1 đến 100 ký tự (tối đa theo FS 4.1 và 4.2, tối thiểu là đề xuất QA) | 101 ký tự: từ chối ở bước kiểm tra đầu vào, trước khi tra invoice | 400, không phải 404 |
| Ký tự cho phép | Chữ, số, gạch ngang, gạch dưới (đề xuất QA). Ví dụ UUID 36 ký tự | Khoảng trắng, dấu nháy, chấm phẩy, HTML, JSON, ký tự điều khiển, emoji | Từ chối, không sửa im lặng |
| Khoảng trắng | Không cắt tự động | Có khoảng trắng đầu hoặc cuối | Từ chối |
| Tính duy nhất | Duy nhất theo (Parent, key), chỉ mục duy nhất ở cơ sở dữ liệu<br>Gửi lại cùng key và cùng nội dung trả cùng kết quả, không tạo transaction thứ hai, không trừ EA lần hai<br>Thử lại sau thất bại dùng key mới (NQ-11) | Cùng key nhưng đổi invoice, số tiền hoặc cách thanh toán | Từ chối với mã xung đột (đề xuất QA) |


Nguồn trong FS: FS 4.1 dòng Idempotency key, FS 4.2 Transaction, BR-F9-04, DA-12, AC-05, NQ-11.

### Điểm mở của D5


| Trường | Điểm mở |
| :--- | :--- |
| D5 | FS chỉ nêu tối đa 100 và duy nhất theo Parent. Phần còn lại là đề xuất QA (O13). Build local trả 404 cho key 101 ký tự (BUG-R9-016) |


| Mã | Trường | Hiển thị | Quy tắc | Nguồn trong FS |
| :--- | :--- | :--- | :--- | :--- |
| D1 | Con và invoice | Tên con, số invoice, mô tả | Chỉ con đã liên kết và invoice Issued<br>Máy chủ kiểm tra lại khi xác nhận, không tin dữ liệu màn trước | FS 3.1.2 bước 6, BR-F9-01 |
| D2 | Tổng phải trả | Net của invoice, SGD | Bằng đúng Net, không trả một phần<br>2 chữ số thập phân | FS 4.1, BR-F9-13 |
| D3 | Số tiền từng phần | Một phần (EA hoặc trực tuyến) hoặc hai phần | Mỗi phần > 0, tổng bằng Net<br>Thứ tự EA trước, trực tuyến sau<br>Ví dụ 20.00 cộng 50.63 | FS 3.1.2 bước 6, BR-F9-11, AC-15 |
| D4 | Số dư EA sau thanh toán | Số dư dự kiến sau khi trừ phần EA | Chỉ khi EA hoặc chia đôi, chỉ để tham khảo<br>= số dư khả dụng trừ phần EA, không âm<br>Không hiển thị khi trả trực tuyến hoàn toàn | FS 4.1, FS 3.1.2 bước 6 |


## 6.3. Điểm mở của màn D


| Trường | Điểm mở |
| :--- | :--- |
| D4 | Build local chưa hiển thị số dư sau thanh toán cho thanh toán EA (BUG-R9-012) |
| D6 | Build local tạo giao dịch nhưng chưa hoàn EA khi trực tuyến thất bại (BUG-R9-014, BUG-R9-019) |
| D7 | FS không nêu đích nút Hủy (O6) |


# 7. Màn E. Đang chờ xử lý (SCR-06)


Hiển thị khi transaction còn Pending hoặc ReconciliationRequired. Kết quả trực tuyến đến qua webhook và truy vấn định kỳ provider. Nguồn: FS 3.1.2 bước 7, BR-F9-06, BR-F9-09, EX-08, EX-09, EX-13, Appendix A, Appendix C.

Hình E. Sơ đồ QA vẽ từ FS 4.1 và Appendix C, không phải ảnh chụp. Cần một giao dịch thật để chụp

## 7.1. Tóm tắt trường


| Mã | Trường | Loại |
| :--- | :--- | :--- |
| E1 | Thông báo đang xử lý hoặc đang xác minh | Chỉ hiển thị |
| E2 | Trạng thái transaction | Chỉ hiển thị |
| E3 | Trạng thái từng leg | Chỉ hiển thị |
| E4 | Mã tham chiếu tạm | Chỉ hiển thị |
| E5 | Nút Làm mới trạng thái | Nút |
| E6 | Nút Quay về danh sách phí | Nút |


## 7.2. Quy tắc trường


### E5. Nút Làm mới trạng thái


| Mục | Quy tắc |
| :--- | :--- |
| Chức năng | Đọc lại trạng thái từ máy chủ |
| Hiển thị khi | Luôn |
| Vô hiệu khi | Vài giây sau mỗi lần bấm (đề xuất QA) |
| Khi bấm | Chỉ đọc, không tạo transaction, không gọi provider thu tiền, không trừ EA<br>Đã Succeeded: sang SCR-07<br>Failed hoặc Cancelled: sang SCR-08<br>ReconciliationRequired: ở lại SCR-06 |
| Khi bấm đúp | Vô hại |
| Khi lỗi | Something went wrong. Please try again later. |
| Nguồn trong FS | FS 3.1.2 bước 7, Appendix C dòng SCR-06 |


### E6. Nút Quay về danh sách phí


| Mục | Quy tắc |
| :--- | :--- |
| Chức năng | Về SCR-02 |
| Hiển thị khi | Luôn |
| Vô hiệu khi | Không |
| Khi bấm | Không đổi dữ liệu, transaction xử lý nền<br>SCR-02 hiển thị invoice đang xử lý và không cho tạo thêm<br>Đóng trình duyệt ở trang provider không hủy transaction |
| Khi bấm đúp | Mở một lần |
| Khi lỗi | Không |
| Nguồn trong FS | FS 3.1.2 bước 7, EX-09, BR-F9-09, AC-11 |


| Mã | Trường | Hiển thị | Quy tắc | Nguồn trong FS |
| :--- | :--- | :--- | :--- | :--- |
| E1 | Thông báo | Đang xử lý hoặc đang xác minh | Pending: đang xử lý. ReconciliationRequired: đang xác minh, không hiển thị như thất bại<br>Chia đôi phải nói bằng chữ rằng phần EA đã bị trừ<br>Không lộ chi tiết kỹ thuật<br>Câu chữ không có trong FS | FS 4.1, EX-13, AC-18 |
| E2 | Trạng thái transaction | Pending hoặc ReconciliationRequired | Chỉ hai giá trị này ở màn này<br>Chỉ chuyển sang giá trị cuối khi có webhook hợp lệ hoặc đối soát, lỗi mạng hay timeout không tự đánh dấu Failed (EX-08)<br>Ngưỡng do Dev cấu hình (NQ-10) | FS 4.1, Appendix A, EX-08 |
| E3 | Trạng thái leg | EA và trực tuyến, kèm số tiền | Pending, Succeeded, Failed, Reversed, ReconciliationRequired, Cancelled<br>Reversed chỉ cho leg EA | FS 4.1, Appendix A |
| E4 | Mã tham chiếu tạm | Mã của transaction | Duy nhất, tối đa 50 ký tự<br>Đề xuất PAY-YYYYMMDD-XXXXXX (TBC, O15)<br>Máy chủ sinh, không sửa | FS 4.1, NQ-12 |


## 7.3. Điểm mở của màn E


| Trường | Điểm mở |
| :--- | :--- |
| E1 | Build local chưa nói phần EA đã bị trừ (BUG-R9-018) |
| E2 | Ngưỡng thời gian chưa chốt (O18) |


# 8. Màn F. Xác nhận thanh toán (SCR-07)


Hiển thị khi mọi leg Succeeded: transaction Succeeded, invoice Paid. Nguồn: FS 3.1.2 bước 7, BR-F9-13, AC-03, AC-08, AC-13, AC-15, Appendix C.

Hình F. Sơ đồ QA vẽ từ FS 4.1 và Appendix C, không phải ảnh chụp. Cần một giao dịch thật để chụp

## 8.1. Tóm tắt trường


| Mã | Trường | Loại |
| :--- | :--- | :--- |
| F1 | Trạng thái thành công | Chỉ hiển thị |
| F2 | Mã tham chiếu | Chỉ hiển thị |
| F3 | Thời gian thanh toán | Chỉ hiển thị |
| F4 | Số tiền quyết toán từng phần | Chỉ hiển thị |
| F5 | Tổng đã trả | Chỉ hiển thị |
| F6 | Nút Tải hoặc in biên lai | Nút |
| F7 | Nút Quay về danh sách phí | Nút |


## 8.2. Quy tắc trường


### F6. Nút Tải hoặc in biên lai


| Mục | Quy tắc |
| :--- | :--- |
| Chức năng | Mở biên lai PDF để tải hoặc in |
| Hiển thị khi | Chỉ khi transaction Succeeded |
| Vô hiệu khi | Không |
| Khi bấm | Biên lai gồm mã tham chiếu, con, invoice, giờ SGT, từng phần và tổng<br>Chỉ xem được biên lai của con đã liên kết (kiểm tra ở máy chủ)<br>Tên tệp đề xuất receipt_{mã}.pdf<br>Gửi email nằm ngoài phạm vi (OOS 9) |
| Khi bấm đúp | Mở một lần |
| Khi lỗi | Something went wrong. Please try again later. |
| Nguồn trong FS | FS 3.1.2 bước 7, AC-13, OOS 9 |


### F7. Nút Quay về danh sách phí


| Mục | Quy tắc |
| :--- | :--- |
| Chức năng | Về SCR-02 |
| Hiển thị khi | Luôn |
| Vô hiệu khi | Không |
| Khi bấm | Không đổi dữ liệu<br>Invoice đã Paid nên không còn trong danh sách<br>Hết phí thì sang SCR-03 |
| Khi bấm đúp | Mở một lần |
| Khi lỗi | Không |
| Nguồn trong FS | Appendix C dòng SCR-07, AC-02 |


| Mã | Trường | Hiển thị | Quy tắc | Nguồn trong FS |
| :--- | :--- | :--- | :--- | :--- |
| F1 | Trạng thái thành công | Succeeded, invoice Paid | Chỉ khi mọi leg Succeeded<br>Mỗi leg EA có bút toán ghi nợ ở Function 1, số dư giảm đúng một lần<br>Trực tuyến cần webhook hợp lệ hoặc đối soát báo thành công | FS 3.1.1, BR-F9-03, AC-03, AC-08 |
| F2 | Mã tham chiếu | Mã của transaction | Duy nhất, tối đa 50 ký tự, PAY-YYYYMMDD-XXXXXX (TBC) | FS 4.1, NQ-12 |
| F3 | Thời gian thanh toán | CompletedAt | Giờ SGT, DD/MM/YYYY 24 giờ (đề xuất QA, O12)<br>Lưu UTC | FS 4.1, FS 4.2 |
| F4 | Số tiền quyết toán từng phần | EA và trực tuyến | Decimal(18,2)<br>Tổng các phần bằng Net<br>Chia đôi: mỗi leg > 0 | FS 4.1, BR-F9-11, AC-15 |
| F5 | Tổng đã trả | Tổng quyết toán | Bằng Net của invoice<br>Succeeded thì Settled = Requested | FS 4.2, BR-F9-13 |


## 8.3. Điểm mở của màn F


| Trường | Điểm mở |
| :--- | :--- |
| F6 | Nội dung biên lai chưa chốt (NQ-12). Build local chỉ có Print receipt (BUG-R9-020, O14) |
| F3 | Định dạng ngày giờ (O12) |


# 9. Màn G. Thanh toán thất bại (SCR-08)


Hiển thị khi transaction Failed hoặc Cancelled. Nguồn: FS 3.1.2 bước 7 và bước thử lại, BR-F9-05, AC-09, AC-17, mục 5.1, Appendix C.

Hình G. Sơ đồ QA vẽ từ FS 4.1 và Appendix C, không phải ảnh chụp. Cần một giao dịch thật để chụp

## 9.1. Tóm tắt trường


| Mã | Trường | Loại |
| :--- | :--- | :--- |
| G1 | Trạng thái giao dịch | Chỉ hiển thị |
| G2 | Lý do thất bại | Chỉ hiển thị |
| G3 | Mã tham chiếu | Chỉ hiển thị |
| G4 | Thông báo hoàn phần EA | Chỉ hiển thị |
| G5 | Nút Thử lại | Nút |
| G6 | Nút Thoát | Nút |


## 9.2. Quy tắc trường


### G5. Nút Thử lại


| Mục | Quy tắc |
| :--- | :--- |
| Chức năng | Về SCR-04 chọn lại cách thanh toán cho cùng invoice |
| Hiển thị khi | Khi giao dịch cũ đã đóng, phần EA (nếu có) đã hoàn, invoice về Issued |
| Vô hiệu khi | ReconciliationRequired (không có nút) |
| Khi bấm | Tạo transaction mới với idempotency key mới (NQ-11) |
| Khi bấm đúp | Mở một lần |
| Khi lỗi | Không |
| Nguồn trong FS | FS 3.1.2 bước thử lại, BR-F9-05, BR-F9-09, NQ-11 |


### G6. Nút Thoát


| Mục | Quy tắc |
| :--- | :--- |
| Chức năng | Về SCR-02 |
| Hiển thị khi | Luôn |
| Vô hiệu khi | Không |
| Khi bấm | Không đổi dữ liệu<br>Invoice đã về Issued nên vẫn trong danh sách |
| Khi bấm đúp | Mở một lần |
| Khi lỗi | Không |
| Nguồn trong FS | FS 3.1.2 bước 7, Appendix C dòng SCR-08 |


| Mã | Trường | Hiển thị | Quy tắc | Nguồn trong FS |
| :--- | :--- | :--- | :--- | :--- |
| G1 | Trạng thái giao dịch | Failed hoặc Cancelled | Chỉ hai giá trị này<br>Invoice về Issued, leg EA đã trừ là Reversed, số dư EA về như trước<br>ReconciliationRequired hiển thị ở SCR-06, không ở đây | FS 3.1.1, FS 4.1, Appendix A |
| G2 | Lý do thất bại | Thông điệp từ FailureCode đã làm sạch | Không lộ SqlException, đường dẫn, mã nội bộ<br>Dùng câu FS 5.1: PAYMENT_FAILED, PAYMENT_FAILED_EA_RETURNED, PAYMENT_CANCELLED, SYSTEM_ERROR (mục 11) | FS 4.1, mục 5.1, AC-09, AC-17 |
| G3 | Mã tham chiếu | Mã của transaction thất bại | Duy nhất, tối đa 50 ký tự, cùng định dạng F2 | FS 4.1, Appendix C |
| G4 | Thông báo hoàn phần EA | Phần EA đã trừ được trả lại | Chỉ khi leg EA Reversed<br>Chia đôi mà trực tuyến Failed, Cancelled hoặc hết hạn: PAYMENT_FAILED_EA_RETURNED, kể cả khi Parent hủy<br>Không hiển thị khi EA chưa bị trừ<br>Hoàn tiền online ngoài phạm vi (OOS 3) | FS 3.1.2 bước 7, mục 5.1, AC-17 |


## 9.3. Điểm mở của màn G


| Trường | Điểm mở |
| :--- | :--- |
| G2, G4, G5 | Build local thiếu lý do, thông báo hoàn EA và nút Thử lại, invoice kẹt PaymentPending (BUG-R9-017, BUG-R9-021), hiện lỗi 5xx thô (BUG-R9-022) |


# 10. Quy tắc phía máy chủ và API


Quy tắc người dùng không thấy trên màn hình nhưng Dev phải xây và QA phải kiểm tra. Nguồn: FS 3.1.1 (BR-F9-01 đến 13), 3.1.2 (EX-01 đến 14), 4.2.

## 10.1. Quyền theo con và invoice (H1)


| Quy tắc | Hợp lệ | Không hợp lệ | Thông báo |
| :--- | :--- | :--- | :--- |
| Mã trong yêu cầu | Mã học sinh đúng GUID<br>Mã invoice tối đa 50 ký tự<br>Mã tham chiếu tối đa 50 ký tự<br>Chỉ của con đã liên kết với Parent | Đổi /students/101 thành /students/102 khi không liên kết<br>Mã invoice của con khác<br>Mã tham chiếu của Parent khác<br>GUID sai định dạng, quá dài | 403 FORBIDDEN_CHILD: You do not have access to this student's records.<br>Giao diện về SCR-01 |
| Ký tự | Chữ, số, gạch ngang theo định dạng từng mã<br>Không cắt tự động | Khoảng trắng, ' OR 1=1 --, HTML, JSON, ký tự điều khiển, byte null | Từ chối, không lỗi 5xx, không đổi dữ liệu |
| Cách kiểm tra | Kiểm tra liên kết Parent và Student ở máy chủ cho mọi API: danh sách, số dư EA, tạo thanh toán, kết quả, biên lai<br>Mọi lần từ chối ghi log bảo mật<br>Không lộ mã có tồn tại hay không | Chỉ kiểm tra ở giao diện | Không |


Nguồn trong FS: BR-F9-01, EX-01, mục 5.1, AC-01, AC-12. Áp cho mã invoice và mã tham chiếu là đề xuất QA. Build local trả 200 với danh sách rỗng thay vì 403 (BUG-R9-002).

## 10.2. Yêu cầu tạo thanh toán (H2 đến H8)


| Mã | Trường hoặc điều kiện | Quy tắc | Lỗi | Nguồn trong FS |
| :--- | :--- | :--- | :--- | :--- |
| H2 | Header Idempotency-Key | Như D5 | 400. Cùng key khác nội dung: mã xung đột | BR-F9-04, DA-12, AC-05 |
| H3 | RequestedAmount | Decimal(18,2), bằng đúng Net, không trả một phần<br>0 ≤ Settled ≤ Requested; Succeeded thì Settled = Requested<br>Máy chủ tính lại Net, không tin số client gửi | Từ chối, không tạo transaction | BR-F9-13, FS 4.2 |
| H4 | Cách thanh toán và số leg | EA hoặc ONLINE: một leg<br>SPLIT: hai leg, leg 1 EA, leg 2 trực tuyến<br>Method: 1 (EA) hoặc 2 (OnlineGateway) | Từ chối | BR-F9-11, FS 4.2 |
| H5 | Số tiền từng leg | Mỗi leg > 0<br>Tổng bằng RequestedAmount<br>Leg EA ≤ số dư khả dụng<br>Leg trực tuyến ≥ mức tối thiểu provider (TBC) | SPLIT_AMOUNT_INVALID hoặc EA_INSUFFICIENT_BALANCE, không đổi dữ liệu | BR-F9-11, AC-19, NQ-13 |
| H6 | Ví và provider theo leg | Leg EA: có WalletId, không ProviderCode<br>Leg trực tuyến: có ProviderCode (tối đa 40), không WalletId<br>ProviderTransactionId (tối đa 128) bắt buộc khi thành công, duy nhất theo cặp với ProviderCode | Leg không được tạo | FS 4.2 FundingLeg |
| H7 | Trạng thái invoice | Chỉ Issued và không có transaction đang mở<br>Tối đa một transaction đang mở và một transaction thành công cho mỗi invoice | INVOICE_ALREADY_PAID, INVOICE_NOT_PAYABLE, PAYMENT_PENDING (409) | BR-F9-09, EX-03, EX-04, EX-14, AC-21 |
| H8 | FundingReference | Duy nhất, tối đa 50 ký tự<br>Gửi lại cùng giá trị chỉ trừ EA một lần | Trùng thì cơ sở dữ liệu từ chối | BR-F9-03, FS 4.2 |


Build local bỏ qua onlineAmount và không từ chối tổng nhỏ hơn Net (BUG-R9-011). Chỉ chạy yêu cầu thay đổi dữ liệu trên khoản phí seed.

## 10.3. Webhook của provider (H9 đến H14)


| Mã | Điều kiện | Quy tắc | Xử lý khi vi phạm | Nguồn trong FS |
| :--- | :--- | :--- | :--- | :--- |
| H9 | Chữ ký HMAC | Chỉ xử lý khi chữ ký hợp lệ, kiểm tra trước mọi xử lý | Từ chối, log bảo mật, không lưu receipt, không đổi trạng thái | BR-F9-06, EX-06, AC-10 |
| H10 | ProviderCode, ProviderEventId | Tối đa 40 và 128 ký tự, duy nhất theo cặp | Sự kiện gửi lại chỉ áp dụng một lần | BR-F9-06, EX-07, AC-10 |
| H11 | ProviderTransactionId, FundingReference, EventType | Tối đa 128, 50, 50 ký tự | Không khớp leg nào: Ignored, không đổi trạng thái<br>Số tiền khác leg: ReconciliationRequired (đề xuất QA) | FS 4.2 WebhookReceipt |
| H12 | Nội dung gốc | Chỉ lưu PayloadHash SHA-256, không lưu payload thô hay dữ liệu thẻ<br>Lỗi lưu đã làm sạch, tối đa 500 ký tự | Lỗi bảo mật dữ liệu | BR-F9-06, DA-01 |
| H13 | Ghi nhận và xử lý | Ghi ngay Received rồi xử lý bất đồng bộ (Processed, Ignored, Failed) | Lỗi xử lý giữ Pending, job đối soát hỏi lại provider | BR-F9-06, EX-08, AC-10 |
| H14 | Thành công muộn | Sau khi leg EA đã hoàn | Leg trực tuyến ReconciliationRequired, invoice không tự Paid. Chưa có hoàn online | EX-12, AC-20, NQ-14, OOS 3 |


Build local bỏ qua webhook thành công muộn sau Failed và chưa có audit_logs (BUG-R9-013).

## 10.4. Phiên và thời gian chờ (H15 đến H18)


| Mã | Tình huống | Quy tắc | Nguồn trong FS |
| :--- | :--- | :--- | :--- |
| H15 | Session portal hết hạn (10 phút, TBC) | Trước khi xác nhận: AUTH_REQUIRED: Your session has expired. Please sign in again., chưa có transaction<br>Sau khi xác nhận: transaction vẫn xử lý, đăng nhập lại thấy trạng thái hiện tại | EX-02, NQ-18 |
| H16 | Phiên provider hết hạn (10 phút, TBC) | Leg trực tuyến Failed, leg EA (nếu có) Reversed<br>Đóng trình duyệt: transaction vẫn Pending | EX-02, EX-09, NQ-18 |
| H17 | Provider timeout hoặc lỗi mạng | Không tự Failed<br>Job đối soát hỏi lại, quá ngưỡng thì ReconciliationRequired (NQ-10) | EX-08, NQ-10 |
| H18 | Lỗi sau khi leg EA thành công | Không có leg trực tuyến sau X phút (Dev chốt) thì hoàn EA<br>Hoàn lỗi: ReconciliationRequired và cảnh báo vận hành | EX-11, EX-13, NQ-18 |


## 10.5. Ràng buộc dữ liệu (H19 đến H23)


| Mã | Đối tượng | Ràng buộc | Nguồn trong FS |
| :--- | :--- | :--- | :--- |
| H19 | Invoice | Mọi dòng cùng SchoolId<br>Gross, Subsidy, Net ≥ 0; Net = Gross trừ Subsidy; Net > 0 khi không Draft<br>InvoiceNumber duy nhất<br>IssuedAt và DueDate bắt buộc sau khi phát hành; PaidAt chỉ khi Paid; CancelledAt chỉ khi Cancelled | BR-F9-12, FS 4.2 |
| H20 | Invoice item | LineNumber > 0, duy nhất trong invoice<br>StudentChargeId duy nhất<br>Gross > 0; 0 ≤ Subsidy < Gross; Net = Gross trừ Subsidy > 0 | BR-F9-12, FS 4.2 |
| H21 | Transaction | IdempotencyKey duy nhất theo (InitiatedByUserId, key)<br>TransactionReference duy nhất<br>Chỉ mục duy nhất trên InvoiceId khi CompletedAt rỗng và khi Succeeded<br>Status 1 đến 5 | BR-F9-09, FS 4.2 |
| H22 | Funding leg | SequenceNumber > 0, duy nhất trong transaction<br>FundingReference duy nhất<br>Tổng leg bằng RequestedAmount cha<br>EducationAccountTransactionId bắt buộc sau ghi nợ; ReversalTransactionId bắt buộc khi Reversed | BR-F9-11, FS 4.2 |
| H23 | Webhook receipt | Duy nhất theo (ProviderCode, ProviderEventId)<br>PayloadHash SHA-256<br>Chỉ lưu callback đã qua HMAC | BR-F9-06, FS 4.2 |


Build local cho gắn student charge của trường khác vào invoice (BUG-R9-023) và ánh xạ sai kiểu student_id, school_id gây lỗi 500 (BUG-R9-015).

# 11. Thông báo chung


Nguyên văn FS mục 5.1. Hai dòng cuối là đề xuất QA.

| Mã | Nội dung hiển thị | Hành vi UI | Trường | Nguồn |
| :--- | :--- | :--- | :--- | :--- |
| EA_NOT_AVAILABLE | This student does not have an Education Account. Please pay online. | Vô hiệu tùy chọn EA, gợi ý Online | C2, C5 | FS 5.1 |
| EA_NOT_ACTIVE | The Education Account is not active. Please pay online. | Như trên | B3, C2, C5 | FS 5.1 |
| EA_INSUFFICIENT_BALANCE | Your Education Account balance is not enough for this amount. You can pay the rest online. | Quay lại chọn phương thức, gợi ý chia đôi | C2, C3, C5 | FS 5.1 |
| SPLIT_AMOUNT_INVALID | The two amounts must be more than zero and add up to the total. | Giữ ở SCR-04, đánh dấu ô nhập | C3, C5, C6, H5 | FS 5.1 |
| INVOICE_ALREADY_PAID | This invoice has already been paid. | Làm mới danh sách | B14, D6, H7 | FS 5.1 |
| INVOICE_NOT_PAYABLE | This invoice can no longer be paid. | Làm mới danh sách | B14, D6, H7 | FS 5.1 |
| PAYMENT_PENDING | A payment for this invoice is still being processed. | Chuyển đến SCR-06 | B14, D6, E1, H2 | FS 5.1 |
| PAYMENT_FAILED | Your payment could not be completed. No amount was deducted. | SCR-08, nút Try again, Exit | G2 | FS 5.1 |
| PAYMENT_FAILED_EA_RETURNED | Your online payment could not be completed. The amount taken from the Education Account has been returned. | SCR-08, nút Try again, Exit | G2, G4 | FS 5.1 |
| PAYMENT_CANCELLED | The payment was cancelled. No amount was deducted. | SCR-08; với chia đôi mà EA đã trừ thì dùng PAYMENT_FAILED_EA_RETURNED | G2 | FS 5.1 |
| FORBIDDEN_CHILD | You do not have access to this student's records. | Quay về SCR-01 | A1, B1, H1 | FS 5.1 |
| AUTH_REQUIRED | Your session has expired. Please sign in again. | Chuyển đến đăng nhập Singpass | H15 | FS 5.1 |
| SYSTEM_ERROR | Something went wrong. Please try again later. | Cho thử lại; không đổi dữ liệu | A5, B16, D5, G2 | FS 5.1 |
| Không có liên kết nào | You have no linked student. Please contact your school. | Trạng thái rỗng ở SCR-01 | A5 | Đề xuất QA, FS nêu có hướng dẫn liên hệ trường nhưng không nêu câu chữ |
| Không có phí chưa thanh toán | There are no outstanding fees for this child. | Trạng thái rỗng SCR-03, có liên kết quay lại SCR-01 | B16 | Đề xuất QA, lấy câu chữ từ giao diện build local |


# 12. Điểm mở cần BA xác nhận


Mọi đề xuất trên các dòng này là suy luận của QA, chưa được xác nhận.

| Mã | Chủ đề | Chi tiết | Trường |
| :--- | :--- | :--- | :--- |
| O1 | Phần EA khi chia đôi có sửa được không | FS 3.1.2 bước 4 và BR-F9-02: phần EA là toàn bộ số dư, Parent không nhập. FS 4.1, BR-F9-10 và AC-22: Parent chọn số tiền từng phần. Build local để chỉ đọc (BUG-R9-010) | C3, C4 |
| O2 | Chia đôi khi số dư đủ trả | BR-F9-02 cho chia đôi khi số dư > 0. FS 3.1.2 bước 4: số dư ≥ Net thì chỉ EA hoặc trực tuyến | C2 |
| O3 | Mặc định hay đề xuất tự động | DA-08: tự động đề xuất EA. BR-F9-10: không tự động trừ EA | C2 |
| O4 | Mức tối thiểu phần trực tuyến | NQ-13 (TBC). Case biên TC-044, TC-060, TC-061 đã bị bỏ | C3, C4, C6, H5 |
| O5 | Kiểu số và số chữ số thập phân | FS không có mục 5.2, NQ-13 nhắc VAL-18 nhưng không có mô tả. TC-059 đã bị bỏ | C3, H3, H5 |
| O6 | Đích của nút Quay lại và Hủy | Appendix C không nêu. TC-037 và TC-064 đã bị bỏ | C7, D7 |
| O7 | Hiển thị quá hạn | OQ-04, NQ-03. TC-026 đã bị bỏ | B12 |
| O8 | Loại phí nào trả bằng EA | OQ-11. TC-069 đã bị bỏ | C2 |
| O9 | Invoice PaymentPending và tổng còn nợ | DA-05 liệt kê Pending, FS 4.1 tính nhãn nợ từ Issued. Build local ẩn khoản thuộc invoice PaymentPending (BUG-R9-004) | A4, B11, B13, B14 |
| O10 | Con duy nhất có bỏ qua SCR-01 không | FS 3.1.2 bước 1 chỉ nói có thể | A1 |
| O11 | Nhãn trạng thái và invoice được liệt kê | DA-05 viết Pending, FS 4.1 viết PaymentPending. Không rõ SCR-02 có liệt kê Paid và Cancelled | B11 |
| O12 | Định dạng ngày, giờ, tiền | FS F9 chỉ nêu SGT. FS F4 BR16: DD/MM/YYYY. Phân cách nghìn lấy từ seed | B2, B12, F3 |
| O13 | Quy tắc idempotency key | FS chỉ nêu tối đa 100 và duy nhất theo Parent. Phần còn lại là đề xuất QA (BUG-R9-016) | D5, H2 |
| O14 | Nội dung và định dạng biên lai | AC-13, NQ-12, OOS 9. Build local chỉ có Print receipt (BUG-R9-020) | F6 |
| O15 | Định dạng mã tham chiếu | NQ-12: PAY-YYYYMMDD-XXXXXX là đề xuất (TBC) | E4, F2, G3 |
| O16 | Nguồn fee component và GST | FS 4.1 TBC, NQ-17: Sprint 1 seed gắn sẵn | B7 |
| O17 | Hoàn tiền online | OOS 3, NQ-05, NQ-14: chưa có, thành công muộn thì ReconciliationRequired | G4, H14 |
| O18 | Ngưỡng thời gian | NQ-10, NQ-18: do Dev cấu hình, session và phiên provider đề xuất 10 phút | E2, H15 đến H18 |
| O19 | Trợ cấp trong seed | BR-F9-08: Sprint 1 Subsidy bằng 0. Seed lấy trợ cấp FAS từ R4, đặt @ApplyFasSubsidy bằng 0 để đúng quy tắc. NQ-04, NQ-16: Net bằng 0 không biểu diễn được vì Net phải > 0 | B9, B10 |
| O20 | Mô hình invoice của FS khác build | FS: chọn invoice, trả cả invoice. Build local: chọn charge rồi gom vào invoice, danh sách phẳng (BUG-R9-003) | B4 đến B14, D1 |
| O21 | Quy tắc và câu chữ không có trong FS | Câu trạng thái rỗng, tên tệp biên lai, mã 400 và 409, quy tắc ký tự của C3, D5, H1, H2 là đề xuất QA | A5, B16, C3, D5, F6 |
| O23 | Liên kết /billing/null ở danh sách con | Quan sát 25/10/2026: thẻ Test Child One, Two, Three và Tan Wei Ming có liên kết /billing/null, mở ra Unable to load education account. Hai thẻ Lucas Lim (STU-005) và Nathan Lim (STU-014) có mã đúng. Chưa có trong danh sách defect | A1 |
| O22 | Con từ 16 tuổi | Seed (sheet Scenarios, dòng Extra): không có nút Pay theo quy tắc R8. FS 9 không nhắc | B14 |


# Phụ lục A. Chuyển trạng thái (FS Appendix A)


| Đối tượng | Từ | Sang | Điều kiện | Invoice |
| :--- | :--- | :--- | :--- | :--- |
| Transaction | (mới) | Pending | Parent xác nhận; tạo các nhánh | PaymentPending |
| Transaction | Pending | Succeeded | Mọi nhánh Succeeded | Paid |
| Transaction | Pending | Failed | Một nhánh Failed, hoặc trực tuyến Failed, Cancelled, hết hạn và nhánh EA (nếu có) đã Reversed | Issued |
| Transaction | Pending | Cancelled | Parent hủy trên trang provider và nhánh EA (nếu có) đã Reversed | Issued |
| Transaction | Pending | ReconciliationRequired | Không xác định được kết quả quá ngưỡng, hoặc hoàn EA lỗi | PaymentPending |
| Transaction | ReconciliationRequired | Succeeded, Failed hoặc Cancelled | Bộ phận vận hành xử lý | Paid hoặc Issued |
| Nhánh EA | Pending | Succeeded | Function 1 ghi nợ thành công | Không đổi |
| Nhánh EA | Pending | Failed | Không đủ số dư hoặc lỗi khi ghi nợ | Không đổi |
| Nhánh EA | Succeeded | Reversed | Hoàn khi giao dịch không hoàn tất | Không đổi |
| Nhánh EA | Pending hoặc Succeeded | ReconciliationRequired | Không chắc kết quả ghi nợ hoặc hoàn | Không đổi |
| Nhánh trực tuyến | Pending | Succeeded | Webhook hợp lệ hoặc đối soát báo thành công | Không đổi |
| Nhánh trực tuyến | Pending | Failed hoặc Cancelled | Provider báo thất bại, Parent hủy, hoặc phiên hết hạn | Không đổi |
| Nhánh trực tuyến | Pending | ReconciliationRequired | Không xác định được kết quả, hoặc thành công muộn sau khi EA đã hoàn | Không đổi |


# Phụ lục B. AC và EX ứng với trường


| Mã | Mô tả | Trường liên quan |
| :--- | :--- | :--- |
| AC-01 | Parent chỉ thấy invoice của con đã chọn | A1, A2, B1, B4, B10, B11, B12, H1 |
| AC-02 | Con không có invoice Issued, hiển thị trạng thái rỗng | B16, F7 |
| AC-03 | Trả bằng EA đủ số dư, số dư giảm một lần | C2, D2, D3, D6, F1, F4 |
| AC-04 | Số dư không đủ, thấy lý do và gợi ý, dữ liệu không đổi | C2, C5, C6 |
| AC-05 | Bấm xác nhận hai lần, một transaction và một lần trừ | D5, D6, H2 |
| AC-06 | Hai yêu cầu đồng thời, chỉ một transaction mở | D6, H2, H7 |
| AC-07 | Function 1 lỗi giữa chừng khi ghi nợ | D6, E1, G1, H17 |
| AC-08 | Trực tuyến thành công qua webhook hợp lệ | D6, F1, H9, H13 |
| AC-09 | Trực tuyến thất bại hoặc hủy, invoice về Issued | G1, G2, G5 |
| AC-10 | Webhook sai chữ ký, gửi lại, hợp lệ | H9, H10, H13 |
| AC-11 | Transaction Pending, không tạo thêm | B14, E1, E6 |
| AC-12 | Đổi mã con trong yêu cầu thì bị từ chối | A1, B1, H1 |
| AC-13 | Xem và tải hoặc in biên lai PDF | F6 |
| AC-14 | Con không có EA chỉ có thanh toán trực tuyến | B2, B3, C2 |
| AC-15 | Chia đôi, cả hai phần thành công | C3, C4, D3, F4 |
| AC-16 | Số dư EA giảm trước lúc xác nhận khi chia đôi | C2, C3, D6 |
| AC-17 | Chia đôi, trực tuyến thất bại, hoàn phần EA | E3, G1, G4 |
| AC-18 | Chia đôi, hoàn EA lỗi, ReconciliationRequired | E1, E2, E3 |
| AC-19 | Tổng hai phần sai hoặc một phần bằng 0 | C3, C5, C6, H5 |
| AC-20 | Thành công muộn sau khi EA đã hoàn | H14 |
| AC-21 | Invoice bị hủy giữa lúc xem và lúc xác nhận | B14, H7 |
| AC-22 | Chia đôi, phần EA mặc định và phần trực tuyến tự tính | C2, C3, C4 |
| EX-01 | Sửa mã con trên URL hoặc API | A1, B1, H1 |
| EX-02 | Session hết hạn khi đang thanh toán | H15, H16 |
| EX-03 | Hai yêu cầu đồng thời cho cùng invoice | D6, H2, H7 |
| EX-04 | Invoice Paid, PaymentPending hoặc Cancelled khi xác nhận | B14, D6, H7 |
| EX-05 | Số dư đổi giữa lúc xem và lúc xác nhận | C2, C3, D6 |
| EX-06 | Webhook sai chữ ký | H9 |
| EX-07 | Webhook gửi lại nhiều lần | H10 |
| EX-08 | Provider timeout hoặc lỗi mạng | E2, H17 |
| EX-09 | Parent đóng trình duyệt khi ở trang provider | E6, H16 |
| EX-10 | Lỗi giữa chừng khi ghi nợ EA | D6, E1 |
| EX-11 | Hệ thống lỗi sau khi nhánh EA thành công | H18 |
| EX-12 | Provider báo thành công muộn sau khi EA đã hoàn | H14 |
| EX-13 | Hoàn EA thất bại | E1, H18 |
| EX-14 | Invoice bị hủy trong lúc Parent đang xem | B14, H7 |


# Phụ lục C. Defect của build local theo trường


Nguồn: sheet Defect Reports của R9_Test_Cases_final_FS09.xlsx, tất cả đang Open. Trang của build: /billing (SCR-01), /billing/:studentId (SCR-02 đến SCR-05), /payment-result (SCR-06 đến SCR-08).

| Defect | Trường | Nội dung |
| :--- | :--- | :--- |
| BUG-R9-001 | A2, A3, A4 | Thẻ con không hiển thị trường, level, lớp và nhãn có phí chưa thanh toán. |
| BUG-R9-002 | H1, B1 | Mã con không liên kết trả 200 danh sách rỗng thay vì 403, giao diện không báo từ chối truy cập. |
| BUG-R9-003 | B4 đến B7 | Hiển thị bảng khoản phí phẳng thay vì invoice mở rộng theo fee type kèm GST và hạn nộp sớm nhất. |
| BUG-R9-004 | B11, B14 | Khoản thuộc invoice PaymentPending hoặc ReconciliationRequired bị ẩn thay vì hiển thị Pending và vô hiệu. |
| BUG-R9-005 | DA-11 | Thiếu ghi chú dữ liệu mẫu trên màn Fees and Payments. |
| BUG-R9-006 | B2, C2 | Con không có EA (404) hiện banner lỗi và chặn thanh toán trực tuyến. |
| BUG-R9-007 | B15, B16 | Trạng thái rỗng không có liên kết quay về danh sách con. |
| BUG-R9-008 | B3, C2 | EA đã Closed vẫn chọn được khi số dư đủ. |
| BUG-R9-009 | C2, C5 | Số dư thấp làm vô hiệu EA nhưng không hiện thông báo giải thích. |
| BUG-R9-010 | C3 | Phần EA khi chia đôi chỉ đọc, không giảm được và không kiểm tra được trên giao diện. |
| BUG-R9-011 | H5 | Yêu cầu bỏ qua onlineAmount và không từ chối tổng hai phần nhỏ hơn số phải trả. |
| BUG-R9-012 | D4 | Màn xem lại thanh toán EA không hiển thị số dư EA sau thanh toán. |
| BUG-R9-013 | H13, H14 | Không có bảng audit_logs cho sự kiện thanh toán và bỏ qua webhook payment.succeeded muộn sau Failed. |
| BUG-R9-014 | D6, H18 | Thiếu bù trừ hoặc hoàn khi lỗi lưu, đối soát khi timeout và token đồng thời RowVersion. |
| BUG-R9-015 | H19 | student_id và school_id kiểu uniqueidentifier nhưng ánh xạ chuỗi, gây lỗi 500. |
| BUG-R9-016 | D5, H2 | Idempotency-Key 101 ký tự không bị từ chối ở bước kiểm tra đầu vào, trả 404 thay vì 400. |
| BUG-R9-017 | G5, H7 | Trực tuyến thất bại, hủy hoặc hết hạn làm invoice kẹt PaymentPending thay vì về Issued. |
| BUG-R9-018 | E1 | Màn chờ khi chia đôi không nói bằng chữ rằng phần EA đã bị trừ. |
| BUG-R9-019 | G4, H18 | Trực tuyến thất bại sau khi EA đã trừ không tự hoàn phần EA. |
| BUG-R9-020 | F6 | Chỉ có Print receipt, không có tải PDF. |
| BUG-R9-021 | G2, G4, G5 | Màn thất bại thiếu lý do, thiếu thông báo phần EA đã hoàn và không có nút Try again. |
| BUG-R9-022 | G2 | Lỗi 5xx hiển thị chuỗi lỗi máy chủ thô, ví dụ SqlException. |
| BUG-R9-023 | H20 | invoice_items cho gắn student charge của trường khác với trường của invoice. |
