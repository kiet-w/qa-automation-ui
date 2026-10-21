# FS-08: Parent Portal – SingPass, Education Account, Profile (Requirement 8)

# FS-08: Parent Portal – SingPass, Education Account, Profile

FR-08 cho phép Parent đăng nhập e-Service bằng SingPass, xem Education Account (EA) của con và cập nhật thông tin liên lạc của mình. Link Mockup: https://claude.ai/artifact/FnU1iDrqnTkhLmdcKyV1X2

## 1. Thông tin tài liệu

| Mục | Nội dung |
| --- | --- |
| Tên tài liệu | FS-08: Parent Portal – SingPass, Education Account, Profile |
| Function | FR-08 (R8), Epic EP-08 |
| Dự án | Education Account & FAS System (MOE Singapore) |
| Người soạn | Nguyễn Quốc Huy (PM) |
| Đối tượng đọc | Dev, QA |
| Tài liệu ưu tiên khi mâu thuẫn | Decision Log > Story tickets > FRD > BRD |

Lịch sử chỉnh sửa

| Phiên bản | Ngày | Người thực hiện | Nội dung thay đổi |
| --- | --- | --- | --- |
| 0.1 | 13/10/2026 | Nguyễn Quốc Huy | Tạo mới theo 3 nhánh: SingPass, xem EA, cập nhật thông tin |
| 0.2 | 13/10/2026 | Nguyễn Quốc Huy | Residential address chỉ đọc (D-20). Chuẩn hóa theo template FS, thêm phân quyền, giao diện, nghiệm thu |
| 0.3 | 14/10/2026 | Nguyễn Quốc Huy | Thêm tạo tài khoản lần đầu, Parent không có con vẫn đăng nhập, MSG-0808. Bỏ chuông thông báo và AI assistant khỏi phạm vi |
| 0.4 | 14/10/2026 | Nguyễn Quốc Huy | Bỏ quét đồng bộ hằng đêm. Sau khi đăng nhập SingPass thành công, hệ thống gọi API dữ liệu theo NRIC để lấy Parent và các con, rồi cập nhật dữ liệu mới nhất của Parent đó. Thêm MSG-0809 (D-31) |

## 2. Giới thiệu

### 2.1 Mục đích. Mô tả chi tiết FR-08 để Dev xây dựng và QA kiểm thử: Parent đăng nhập e-Service bằng SingPass, xem Education Account (EA) của con và cập nhật thông tin liên lạc của mình.

### 2.2 Phạm vi

| Trong phạm vi | Ngoài phạm vi |
| --- | --- |
| (1) Access via SingPass (kèm tra cứu API và cập nhật dữ liệu Parent, con khi đăng nhập), (2) View EA details, (3) Update basic personal details, Home | Thanh toán phí (FS-09), nộp đơn FAS (FS-10), AI assistant (US-08.3) |

### 2.3 Tài liệu tham chiếu: Decision Log (D-03, D-19 đến D-22, D-28, D-31), FRD mục FR-08, ticket EP-08 (US-08.1, US-08.2), mockup e-Service Portal, bảng Parent_Profile.

### 2.4 Thuật ngữ

| Thuật ngữ | Ý nghĩa |
| --- | --- |
| SingPass | Dịch vụ đăng nhập quốc gia của Singapore. Dự án dùng bản mô phỏng (mock) |
| NRIC | Mã định danh của Parent, dùng để liên kết với học sinh |
| EA | Education Account: tài khoản giáo dục của học sinh là công dân, từ 7 đến 16 tuổi |
| Parent | Cha hoặc mẹ của học sinh, người dùng của e-Service Portal |
| Residential address | Địa chỉ cư trú, lấy từ SingPass, chỉ đọc |
| Mailing address | Địa chỉ nhận thư do Parent tự nhập, sửa được |
| Pending | Giao dịch thanh toán online chưa được ngân hàng xác nhận |
| API dữ liệu | Nguồn dữ liệu Parent và học sinh (mock trong dự án). Hệ thống gọi bằng NRIC khi Parent đăng nhập để lấy thông tin Parent và tìm các con |

## 3. Quy trình đề xuất (To-Be)

Hệ thống mới nên không có quy trình cũ (As-Is). Luồng tổng quát của Parent:

1.      Parent chọn Log in with SingPass. SingPass lỗi hoặc Parent hủy: báo MSG-0802, quay lại trang đăng nhập.

2.      SingPass xác thực thành công, trả NRIC, họ tên, địa chỉ cư trú.

3.      Hệ thống gọi API dữ liệu bằng NRIC để lấy thông tin Parent, rồi tìm các con theo NRIC (NRIC của cha hoặc mẹ). Không tìm thấy Parent hoặc Parent không có con nào: báo MSG-0801, không vào được. API lỗi hoặc quá 10 giây: báo MSG-0809, không vào được.

### 4.      Lần đầu đăng nhập: hệ thống tạo tài khoản và liên kết các con. Các lần sau dùng lại tài khoản.

5.      Hệ thống cập nhật thông tin mới nhất của Parent và các con của Parent đó vào dữ liệu hệ thống. Chỉ cập nhật cho Parent vừa đăng nhập, không có tiến trình cập nhật toàn bộ hằng đêm.

6.      Parent vào Home (mỗi con một card, xếp theo thứ tự ở mục 6.1), chọn một con và xem Education Account: số dư, giao dịch, lọc.

7.      Con đủ 16 tuổi: Parent chỉ xem thông tin của con đó (EA, phí, lịch sử giao dịch, My details), không thanh toán, không nộp FAS. Con chưa đủ 16 tuổi: dùng đầy đủ chức năng.

8.      Tùy chọn: Parent sửa My details. Lưu thành công: MSG-0807. Lưu lỗi hệ thống: MSG-0808.

9.      Parent đăng xuất, hoặc hệ thống tự đăng xuất sau 15 phút không thao tác.

Luồng function 8 · SingPass, tài khoản, Home, sửa thông tin

## 04. Phân quyền

| Vai trò | Đăng nhập e-Service | Xem EA | Sửa thông tin liên lạc | Ghi chú |
| --- | --- | --- | --- | --- |
| Parent (cha hoặc mẹ) | Có, bằng SingPass | Có, chỉ con liên kết qua NRIC | Có, chỉ của chính mình | Cả bố và mẹ đều có quyền như nhau (D-19) |
| Student | Không | Không | Không | Học sinh không đăng nhập (A-01) |
| School Admin, Staff | Không (dùng Admin Portal) | Không | Không | Chỉ xem lại giao diện Parent qua Simulate, chỉ đọc (FR-07) |
| MOE HQ Admin | Không (dùng Admin Portal) | Không | Không | Như trên |

## 5. Yêu cầu chức năng

US-08.1 Là Parent, tôi muốn đăng nhập bằng SingPass để xem EA của con. US-08.2 Là Parent, tôi muốn cập nhật thông tin liên lạc để nhà trường và MOE liên hệ được.

FR-08.1 Đăng nhập bằng SingPass

| Mục | Nội dung |
| --- | --- |
| Kích hoạt | Parent chọn Log in with SingPass ở Landing page |
| Điều kiện trước | API dữ liệu Parent và học sinh sẵn sàng (mock trong dự án) |
| Luồng chính | 1. SingPass xác thực, trả NRIC, họ tên, địa chỉ cư trú. 2. Hệ thống gọi API dữ liệu bằng NRIC, lấy thông tin Parent và tìm các con theo NRIC. 3. Lần đầu: tạo tài khoản (UserId), kích hoạt (IsActivate = true), liên kết các con. Các lần sau: dùng lại tài khoản, không tạo thêm. 4. Cập nhật thông tin mới nhất của Parent và các con vào dữ liệu hệ thống. 5. Tạo session, vào Home |
| Quy tắc | Cha và mẹ có quyền như nhau (D-19). Chỉ Parent mà API dữ liệu tìm thấy và có ít nhất một con mới đăng nhập được. Cập nhật dữ liệu chỉ chạy sau khi đăng nhập thành công, chỉ cho Parent đó và các con của họ, không có cập nhật hằng đêm. Với Parent: cập nhật họ tên, residential address; phone, email, mailing address lấy từ nguồn ở lần đầu, các lần sau không ghi đè giá trị Parent đã sửa trong My details. Với con: cập nhật họ tên, trường, lớp, ngày sinh, quốc tịch; con không còn liên kết với NRIC này thì bỏ liên kết. Cập nhật lỗi: MSG-0809, dữ liệu giữ nguyên, không vào được. Ghi audit log mỗi lần cập nhật. Session hết hạn sau 15 phút không thao tác (D-22) |
| Đầu vào | NRIC, họ tên, residential address từ SingPass; dữ liệu Parent và con từ API dữ liệu |
| Đầu ra | Tài khoản Parent, dữ liệu Parent và con đã cập nhật, session, Home |
| Lỗi | SingPass lỗi hoặc hủy: MSG-0802, quay lại trang đăng nhập. Không tìm thấy Parent hoặc Parent không có con: MSG-0801, không vào được. API lỗi hoặc quá 10 giây: MSG-0809, không vào được. Hết session: MSG-0002 |

FR-08.2 Xem Education Account

| Mục | Nội dung |
| --- | --- |
| Kích hoạt | Parent chọn một con ở Home và mở Education Account |
| Điều kiện trước | Đã đăng nhập, con thuộc Parent |
| Luồng chính | Hiển thị: (1) Thông tin tài khoản: mã EA, trạng thái và lý do, ngày mở, ngày đóng dự kiến, thời điểm cập nhật dữ liệu lần cuối (lần đăng nhập gần nhất), thông tin học sinh (tên, trường, lớp, ngày sinh). (2) Số dư khả dụng, số tiền đang chờ xử lý (Pending), tổng tiền vào và tiền ra trong năm. (3) Hỗ trợ FAS đang áp dụng cho con (nếu có). (4) Danh sách giao dịch, mới nhất trước. Parent lọc theo thời gian, loại, chiều tiền |
| Quy tắc | Chỉ EA của con liên kết. Số tiền định dạng SGD, ngày DD/MM/YYYY. Con đủ 16 tuổi: vẫn xem EA, phí, lịch sử giao dịch, nhưng không thanh toán, không nộp FAS. Con chưa đủ 16 tuổi: dùng đầy đủ (FS-09, FS-10). Quy tắc áp dụng riêng cho từng con: ví dụ một con 14 tuổi và một con 16 tuổi thì chỉ con 16 tuổi bị chuyển sang chỉ xem. Mã EA dạng EA + số của học sinh. Ngày mở = sinh nhật thứ 7, ngày đóng = sinh nhật thứ 16. Trạng thái: Active (còn dùng, ghi rõ ngày đóng), Due for closure (đã đủ 16 tuổi, chỉ xem, sẽ đóng), Closed. Số dư khả dụng chỉ tính giao dịch Completed. Giao dịch Pending hiện riêng ở khung màu vàng, chưa trừ vào số dư. Tiền vào, tiền ra tính theo năm hiện tại, chỉ giao dịch Completed. Khối FAS: Granted hiện màu xanh kèm khoản phí được giảm, đang xét hiện nhãn Under review, không có thì ẩn. Giao dịch gồm: ngày giờ, mã tham chiếu (TXN-xxxxxx), loại (Top-up, Fee payment, Refund, Closure transfer; mỗi loại một màu), mô tả, số tiền (tiền vào xanh, tiền ra đen), số dư sau giao dịch (giao dịch Pending không có), trạng thái. Giao dịch Fee payment có liên kết View fee mở trang Fees của con đó (FS-09) |
| Đầu vào | Student, bộ lọc (từ ngày, đến ngày, loại) |
| Đầu ra | Thông tin tài khoản, số dư khả dụng, số tiền Pending, tiền vào/ra trong năm, khối FAS, danh sách giao dịch |
| Lỗi | Con không có EA: MSG-0804. Lọc không có kết quả: MSG-0803. Truy cập con không thuộc mình: MSG-0003 |

FR-08.3 Cập nhật thông tin cá nhân cơ bản

| Mục | Nội dung |
| --- | --- |
| Kích hoạt | Parent mở My details và chọn Save (bước tùy chọn) |
| Điều kiện trước | Đã đăng nhập. Parent còn ít nhất một con chưa đủ 16 tuổi. Khi tất cả các con đã đủ 16 tuổi, My details chỉ xem |
| Luồng chính | Parent sửa số điện thoại, email, mailing address. Hệ thống kiểm tra, lưu, ghi audit log, báo MSG-0807 |
| Quy tắc | Chỉ sửa thông tin của chính mình. Residential address, NRIC, họ tên chỉ đọc, lấy từ SingPass (D-20). Không gửi email khi đổi thông tin (D-28 chỉ áp dụng cho top-up, thanh toán, kết quả FAS) |
| Đầu vào | PhoneNumber, Email, Mailing (Block, Street, Unit, PostalCode, Country) |
| Đầu ra | Parent_Profile đã cập nhật, audit log |
| Lỗi | Bỏ trống trường bắt buộc: MSG-0001. Phone sai: MSG-0805. Email sai: MSG-0806. Lưu lỗi hệ thống: MSG-0808, dữ liệu giữ nguyên. Hết session: MSG-0002 |

## 6. Yêu cầu giao diện

| Màn hình | Nội dung chính |
| --- | --- |
| Landing page | Nút Log in with SingPass |
| Home | Mỗi con một card: tên, trường, lớp, trạng thái EA, số dư, phí cần trả |
| Education Account | Thông tin tài khoản, số dư, khối FAS, bộ lọc, bảng giao dịch |
| My details | Form thông tin cá nhân (bảng dưới), nút Save |

| Trường | Kiểu | Bắt buộc | Sửa được | Kiểm tra |
| --- | --- | --- | --- | --- |
| Full name, NRIC | Text | - | Không | Lấy từ SingPass |
| Residential address | Text | - | Không | Lấy từ SingPass |
| Mobile number | Text | Có | Có | 8 chữ số, bắt đầu 6, 8 hoặc 9, ví dụ 9123 4567 |
| Email | Text | Có | Có | Đúng định dạng email, tối đa 150 ký tự |
| Mailing block, unit | Text | Không | Có | Tối đa 20 ký tự |
| Mailing street | Text | Có | Có | Tối đa 100 ký tự |
| Mailing postal code | Text | Có | Có | 6 chữ số |
| Mailing country | Text | Có | Có | Tối đa 100 ký tự |

### 6.1 Màn hình Home

Mỗi con một card. Bấm vào card để mở Education Account của con đó. Phía trên có nút Apply for FAS (FS-10). Thứ tự card: (1) con có EA Active xếp trước, con đã đủ 16 tuổi (chỉ xem) xếp cuối; (2) trong mỗi nhóm, con lớn tuổi hơn xếp trước; (3) cùng tuổi thì con chưa có đơn FAS xếp trước con đã có hoặc đang chờ FAS. Thứ tự này cũng dùng cho các nút chọn con ở màn Education Account.

| Thành phần | Quy tắc hiển thị |
| --- | --- |
| Đầu card | Tên học sinh, nhãn trạng thái EA, trường và lớp |
| EA balance | Chỉ hiện khi EA là Active hoặc Due for closure. Trạng thái khác hiện câu thay thế (xem 6.2) |
| Need to pay | Tổng phí đang Outstanding của con, tính sau trợ cấp |
| Nhãn FAS | Hiện khi con có FAS đang Granted, ví dụ MOEFAS Tier 2 |
| Danh sách phí | Tối đa 3 khoản còn phải trả, xếp theo hạn trả gần nhất: tên phí, trạng thái (Due soon, Not due yet, Overdue), số tiền. Nhiều hơn 3 khoản hiện thêm dòng "+N more". Không có khoản nào hiện "Nothing to pay right now." |
| Nút All fees | Mở danh sách phí của con (FS-09) |

### 6.2 Màn hình Education Account

| Trạng thái | Điều kiện | Hiển thị |
| --- | --- | --- |
| Active | Công dân, từ 7 đến dưới 16 tuổi, đã có EA | Số dư và giao dịch |
| Due for closure | Đã đủ 16 tuổi, EA chưa đóng | Số dư và giao dịch |
| Closed | EA đã đóng | Giao dịch |
| To be created | Công dân, đủ 7 tuổi, chưa có EA | Câu "Education Account not active yet." |
| Not yet 7 | Công dân, chưa đủ 7 tuổi | Câu cho biết ngày EA được mở (sinh nhật 7 tuổi) |
| Not eligible | Không phải công dân | Câu "Education Accounts are for Singapore Citizens". Vẫn xem được phí và nộp FAS |

•       Nhiều con: có nút lọc All và từng con. Chế độ All hiện card số dư của từng con và bảng giao dịch có thêm cột Student.

•       Bộ lọc: From, To (ngày), Type (All, Top-up, Fee payment, Refund, Closure transfer), Money flow (All, Money in, Money out). Bấm Apply filter để áp dụng.

•       Bảng giao dịch: cột Date & time, Student (chỉ ở chế độ All), Type, Description (kèm mã TXN), Amount, Balance after, Status. Mới nhất trước, 20 dòng mỗi trang, có Previous và Next, hiện tổng số giao dịch.

•       Amount: tiền vào có dấu + và màu xanh, tiền ra có dấu -. Giao dịch thanh toán online chỉ ghi số tiền và "online", không làm đổi số dư EA.

•       Status: Completed, Pending, Failed. Giao dịch online Pending có nút Continue payment.

•       Last updated: thời điểm hệ thống cập nhật dữ liệu Parent và con ở lần đăng nhập gần nhất, dạng DD/MM/YYYY HH:mm.

## 7. Yêu cầu phi chức năng

•       Bảo mật: mọi API kiểm tra quyền ở server, Parent chỉ truy cập dữ liệu của mình và con liên kết (MSG-0003). Không đưa NRIC đầy đủ vào URL.

•       Audit: ghi log đăng nhập, mỗi lần cập nhật dữ liệu từ API và mỗi lần sửa thông tin (trường, giá trị cũ, mới, người sửa, thời điểm).

•       Phiên làm việc: tự đăng xuất sau 15 phút không thao tác (D-22).

•       Tích hợp: SingPass và API dữ liệu Parent, học sinh là mock trong dự án; tách lớp tích hợp để thay bằng hệ thống thật. API dữ liệu có timeout 10 giây. Không có tiến trình cập nhật hàng loạt: dữ liệu chỉ cập nhật theo từng Parent khi đăng nhập.

•       Hiệu năng: Home và Education Account tải dưới 3 giây với 1.000 giao dịch.

•       Hiển thị: giao diện tiếng Anh, tiền SGD, ngày DD/MM/YYYY, dùng được trên điện thoại.

## 8. Tiêu chí nghiệm thu

| # | Tình huống | Kết quả mong đợi |
| --- | --- | --- |
| 1 | Parent được API dữ liệu tìm thấy và có con, đăng nhập SingPass lần đầu | Tạo tài khoản, cập nhật dữ liệu Parent và con, vào Home, thấy card của từng con |
| 2 | Parent đăng nhập lần thứ hai | Dùng lại tài khoản, không tạo thêm |
| 3 | NRIC không có trong API dữ liệu, hoặc có Parent nhưng không có con | Báo MSG-0801, không vào được hệ thống |
| 4 | Cha và mẹ cùng đăng nhập | Cùng thấy các con và quyền như nhau |
| 5 | SingPass lỗi hoặc hủy | Báo MSG-0802, quay lại trang đăng nhập |
| 6 | Mở EA của con có EA | Thấy số dư và giao dịch mới nhất trước |
| 7 | Parent có hai con, một con 14 tuổi, một con đạt 16 tuổi hôm nay | Con 14 tuổi dùng bình thường. Con 16 tuổi chỉ xem, không có thanh toán và nộp FAS |
| 8 | Con 16 tuổi | Vẫn xem được EA, phí, lịch sử giao dịch và My details |
| 9 | Tất cả các con đã đủ 16 tuổi | My details chỉ xem, không sửa được |
| 10 | Con không phải công dân | Home và màn EA hiện câu thay thế theo bảng 6.2, không hiện số dư |
| 11 | Lọc không có kết quả | Báo MSG-0803 |
| 12 | Parent có con Active và con đã đủ 16 tuổi | Con đủ 16 tuổi xếp cuối, các con còn lại xếp theo tuổi giảm dần |
| 13 | Mở EA của con không thuộc mình | Báo MSG-0003 |
| 14 | Sửa phone, email, mailing hợp lệ | Lưu, báo MSG-0807, có audit log, không gửi email |
| 15 | Phone hoặc email sai định dạng | Báo MSG-0805 hoặc MSG-0806, không lưu |
| 16 | Bỏ trống trường bắt buộc | Báo MSG-0001 theo từng trường |
| 17 | Lưu bị lỗi hệ thống | Báo MSG-0808, dữ liệu giữ nguyên |
| 18 | Thử sửa residential address | Trường chỉ đọc, không sửa được |
| 19 | Có hơn 3 khoản phí còn phải trả | Card Home hiện 3 khoản gần hạn nhất và dòng "+N more" |
| 20 | Không thao tác 15 phút | Tự đăng xuất, báo MSG-0002 |
| 21 | Thông tin con thay đổi trên API dữ liệu (ví dụ đổi lớp), rồi Parent đăng nhập | Home hiện thông tin mới nhất của con |
| 22 | Parent đã sửa số điện thoại trong My details, rồi đăng nhập lại | Số điện thoại giữ giá trị Parent đã sửa, không bị ghi đè |
| 23 | API dữ liệu lỗi hoặc quá 10 giây khi Parent đăng nhập | Báo MSG-0809, không vào được, dữ liệu giữ nguyên |
| 24 | Parent chưa đăng nhập | Dữ liệu của Parent và các con không bị thay đổi (không có cập nhật hằng đêm) |
| 25 | Con đang có giao dịch Pending (thanh toán online chờ xác nhận) | Số tiền Pending hiện riêng ở khung vàng, số dư khả dụng chưa trừ, giao dịch đó không có số dư sau giao dịch |
| 26 | Con đã đủ 16 tuổi | Trạng thái Due for closure, hiện ngày đủ 16 tuổi và ngày đóng |
| 27 | Con có FAS được duyệt / con chưa có FAS | Có FAS: khối xanh ghi chương trình, tier, khoản phí được giảm. Chưa có: không hiện khối FAS |
| 28 | Xem danh sách giao dịch, lọc loại Refund, bấm View fee | Mỗi giao dịch có ngày giờ, mã TXN, loại (màu riêng), số dư sau giao dịch. Lọc đúng loại. View fee mở trang Fees của con đó |

## Phụ lục A. Bảng dữ liệu Parent_Profile

Bảng dùng chung cho nhánh 1 (tra cứu bằng Nric) và nhánh 3 (sửa thông tin). Liên kết với học sinh qua Nric = Student_Profile.FatherNric hoặc MotherNric.

| Trường | Kiểu | Sửa được | Nguồn |
| --- | --- | --- | --- |
| Id | UUID | Không | Hệ thống |
| Code | NVARCHAR(50) | Không | Hệ thống |
| UserId | VARCHAR(50) | Không | Hệ thống |
| Nric | VARCHAR(9) | Không | SingPass |
| FullName | NVARCHAR(150) | Không | SingPass |
| PhoneNumber | VARCHAR(20) | Có | Người dùng nhập |
| Email | NVARCHAR(150) | Có | Người dùng nhập |
| ResidentialBlock | NVARCHAR(20) | Không | SingPass |
| ResidentialStreet | NVARCHAR(100) | Không | SingPass |
| ResidentialUnit | NVARCHAR(20) | Không | SingPass |
| ResidentialPostalCode | VARCHAR(10) | Không | SingPass |
| ResidentialCountry | NVARCHAR(100) | Không | SingPass |
| MailingBlock | NVARCHAR(20) | Có | Người dùng nhập |
| MailingStreet | NVARCHAR(100) | Có | Người dùng nhập |
| MailingUnit | NVARCHAR(20) | Có | Người dùng nhập |
| MailingPostalCode | VARCHAR(10) | Có | Người dùng nhập |
| MailingCountry | NVARCHAR(100) | Có | Người dùng nhập |
| IsActivate | BOOLEAN | Không | Hệ thống |
| CreatedAt, UpdatedAt | TIMESTAMP | Không | Hệ thống |
| CreatedBy, UpdatedBy | VARCHAR(50) | Không | Hệ thống |

Mỗi lần sửa, ghi audit log: trường, giá trị cũ, giá trị mới, người sửa, thời điểm.

## Phụ lục B. Message codes

| Code | Nội dung | Khi nào |
| --- | --- | --- |
| MSG-0801 | We could not find any student linked to your account. Please contact your child's school. | Không tìm thấy Parent hoặc Parent không có con |
| MSG-0802 | Login was not completed. Try again. | SingPass lỗi/hủy |
| MSG-0803 | No transactions found. | Filter không có kết quả |
| MSG-0804 | This student does not have an Education Account. | Con không có EA |
| MSG-0805 | Enter a mobile number in the correct format, like 9123 4567 | Phone sai |
| MSG-0806 | Enter an email address in the correct format, like name@example.com | Email sai |
| MSG-0807 | Your details have been updated. | Lưu thành công |
| MSG-0002 | Your session has expired. Please log in again. | Hết session |
| MSG-0003 | You do not have permission to perform this action. | Truy cập dữ liệu không thuộc về mình |
| MSG-0001 | Enter your <field> (lỗi bắt buộc theo từng trường) | Bỏ trống trường bắt buộc |
| MSG-0808 | We could not update your details. Please try again. | Lưu lỗi hệ thống |
| MSG-0809 | We could not retrieve your information. Please try again later. | API dữ liệu lỗi hoặc quá 10 giây, hoặc cập nhật dữ liệu lỗi khi đăng nhập |

