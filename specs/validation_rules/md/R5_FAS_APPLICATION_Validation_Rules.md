# R5_FAS_APPLICATION_Validation_Rules


QUY TẮC KIỂM TRA HỢP LỆ

Requirement R5, Function 5: Đơn giấy (Paper Applications)

Dành cho Dev. Dựa trên FS F5 Paper Applications v1.2 ngày 21/10/2026, đối chiếu với các hình trong FS.

| Mục | Nội dung |
| :--- | :--- |
| Dự án | Agileproject, hệ thống tài chính MOE, EAFAMS |
| Phiên bản | Bản nháp 0.1, 26/10/2026 |
| Tác giả | QA |
| Nguồn chính | FS05.md của requirement R5 (FS F5 Paper Applications v1.2, 21/10/2026), 5 hình trong FS |
| Nguồn tham khảo định dạng | R4_FAS_Validation_Rules_EN.docx, R9_FAS_Validation_Rules.docx |
| Nguồn đối chiếu | FS01.md, quy tắc độ tuổi F01-BR02 và đóng tài khoản F02 |
| Hình | Năm hình lấy từ FS F5: danh sách, Upload scans, Review application, trạng thái bị chặn, Review before submitting. QA đánh dấu mã trường màu đỏ. FS không có hình cho màn Xem và sửa đơn đã nộp |
| Trạng thái | Chờ BA xác nhận các điểm mở ở mục 11. Các quy tắc ghi Đề xuất QA chưa có trong FS |


# 1. Phạm vi


| Màn | Nội dung | Mục trong FS |
| :--- | :--- | :--- |
| A | Danh sách Upload applications | FS 3 |
| B | Hộp thoại Upload scans | FS 4 |
| C | Màn Review application, Part 1 đến Part 5 | FS 5 |
| D | Kiểm tra hợp lệ khi bấm Review and submit | FS 6 |
| E | Hộp thoại Review before submitting | FS 7 |
| F | Xem và sửa đơn đã nộp | FS 8 |
| G | Quy tắc máy chủ, API và dữ liệu dùng chung, không có màn hình | FS 1.2, FS 2, FS 9 (BR1 đến BR9) |


# 2. Quy ước


| Mục | Quy tắc |
| :--- | :--- |
| Số đỏ trong hình | Trùng mã trường ở tiêu đề bên dưới, ví dụ khung C5 là mục C5 |
| Nguồn trong FS | Mục, quy tắc nghiệp vụ BR hoặc kịch bản T làm căn cứ cho quy tắc |
| Thông báo | Nguyên văn trong FS mục 4 (hộp thoại Upload scans) và mục 6 (kiểm tra hợp lệ) |
| Đề xuất QA | Không có trong FS. BA phải xác nhận trước khi Dev làm |
| Hình | Giá trị đọc từ hình của FS |
| Nhãn tùy chọn có dấu gạch trong FS | Viết ở đây không có dấu gạch, ví dụ International ASEAN. Nhãn gốc nằm ở FS 5, Part 1 |
| Mọi ô nhập văn bản | Được xem là dữ liệu, không bao giờ là mã<br>Truy vấn tham số hóa<br>Đầu ra được mã hóa HTML<br>Không bao giờ phân tích như JSON, XML, template hay lệnh<br>Ký tự điều khiển bị loại bỏ<br>Lưu bằng Unicode |
| Ngôn ngữ giao diện | Tiếng Anh. Tài liệu này viết tiếng Việt, các thông báo giữ nguyên văn tiếng Anh |
| Vai trò School user | Chỉ thấy và nhập đơn giấy của học sinh đang học tại trường của mình. Tên vai trò trong FS F5 là School user, trong ngoặc School Admin |
| Vai trò MOE HQ | Không có quyền truy cập các màn hình này |
| Trạng thái đơn | Draft, Pending, Approved MOEFAS, Approved SBFAS, Rejected |
| Định dạng chuẩn | Ngày DD/MM/YYYY<br>Giờ HH:mm theo giờ Singapore UTC+8<br>Tiền S$ #,##0.00<br>Theo quy tắc chung của F4, nhắc lại ở mục 10 |


# 3. Màn A. Danh sách Upload applications


Menu Financial assistance, Upload applications. Dành cho School user. Danh sách gồm đơn giấy đã nộp và các bản Draft của trường. Nguồn: FS 3.

Hình A, hình Upload applications của FS có một dòng Draft

## 3.1. Tóm tắt trường


| Mã | Trường | Loại |
| :--- | :--- | :--- |
| A1 | Nút Upload scans | Nút |
| A2 | Thẻ thống kê PENDING, MOEFAS, SBFAS | Chọn để lọc |
| A3 | Ô Search | Ô nhập văn bản |
| A4 | Bộ lọc Status | Chọn |
| A5 | Bộ lọc Tier | Chọn |
| A6 | Bộ lọc Uploaded | Chọn |
| A7 | Bảng đơn | Chỉ hiển thị |
| A8 | Dòng Draft, nút Continue và Delete | Nút |
| A9 | Dòng đã nộp | Chọn dòng |
| A10 | Ghi chú cuối trang | Chỉ hiển thị |


## 3.2. Quy tắc trường


### A1. Nút Upload scans


| Mục | Quy tắc |
| :--- | :--- |
| Chức năng | Mở hộp thoại Upload scans của màn B |
| Hiển thị khi | Luôn luôn. Việc có form FAS đang mở chỉ được kiểm tra khi nộp (mục 6), không chặn nút này |
| Khi bấm | Hộp thoại mở, danh sách file trống |
| Khi bấm đúp | Chỉ mở một hộp thoại |
| Nguồn trong FS | FS 3 mục 1, FS 2 bước 1 |


### A2. Thẻ thống kê


| Mã | Trường | Hiển thị | Quy tắc | Nguồn trong FS |
| :--- | :--- | :--- | :--- | :--- |
| A2 | Thẻ thống kê | PENDING, ghi chú Waiting for assessment<br>MOEFAS, ghi chú Approved automatically<br>SBFAS, ghi chú Decided by school | Đếm số đơn giấy của trường<br>Bấm thẻ để lọc danh sách, bấm lần nữa để bỏ lọc<br>Bản Draft không được tính vào thẻ nào, suy luận từ hình: PENDING 1 trong khi có 1 Draft và 1 Pending<br>Thẻ có theo ô Search và bộ lọc Uploaded hay không là điểm mở O22 | FS 3 mục 2 |


### A3. Ô Search


| Quy tắc | Hợp lệ | Không hợp lệ | Thông báo |
| :--- | :--- | :--- | :--- |
| Bắt buộc | Để trống hoặc có giá trị | Không có | Không có |
| Độ dài | 0 đến 100 ký tự | 101 ký tự trở lên | Trường vượt quá 100 ký tự.<br>Đề xuất QA. |
| Khoảng trắng đầu và cuối | Được cắt bỏ trước khi kiểm tra và lưu | Không có | Không có |
| Chỉ có khoảng trắng | Coi như để trống | Không có | Không có thông báo riêng, áp dụng quy tắc Bắt buộc |
| Xuống dòng và tab | Thay bằng một khoảng trắng | Không có | Không có |
| Ký tự điều khiển U+0000 đến U+001F, U+007F | Bị loại bỏ, trừ xuống dòng và tab khi ô nhiều dòng | Không có | Không có |
| Ký tự null | Bị loại bỏ, không bao giờ tới cơ sở dữ liệu | Không có | Không có |
| Ký tự cho phép | Mọi ký tự in được của Unicode | Không có | Không có |
| Ký tự đặc biệt ' " % \ ; & < > | Lưu đúng như đã nhập | Không có | Hiển thị là văn bản thường |
| Chuỗi SQL, ví dụ ' OR '1'='1 | Lưu hoặc tìm như văn bản, truy vấn tham số hóa | Không có | Không đổi dữ liệu nào ngoài trường này |
| Script và HTML, ví dụ <script>alert(1)</script>, <img onerror>, javascript: | Lưu như đã nhập | Không có | Hiển thị là văn bản thường, không bao giờ chạy hay dựng thành HTML<br>Được mã hóa ở màn hình, hộp thoại, History, CSV và thư điện tử |
| JSON, XML, template, lệnh, ví dụ {"a":1}, ${jndi:ldap://x}, {{7*7}}, $(whoami), ../../etc/passwd | Lưu như văn bản thường, không bao giờ được phân tích hay thực thi | Không có | Dấu nháy và dấu gạch ngược được escape trong dữ liệu gửi qua API |
| Xuất CSV | Giá trị bắt đầu bằng dấu bằng, dấu cộng, dấu trừ hoặc @ được thêm dấu nháy đơn phía trước | Không có | Không có |
| Emoji và chữ của mọi hệ chữ viết | Được chấp nhận như văn bản | Không có | Không có |
| Phạm vi tìm | Application ID, tên người tải lên, số EA hoặc tên học sinh | Không có | Không có |
| So khớp | Chứa chuỗi, không phân biệt hoa thường | Không có | Không có thông báo, danh sách rỗng khi không khớp. Dùng thông báo chung No applications found. của F4. Đề xuất QA |
| Ký tự đại diện | % và _ là văn bản thường, không phải ký tự đại diện, không dùng biểu thức chính quy | Không có | Không có |
| Kích hoạt | Phím Enter hoặc 300 ms sau phím cuối. Đề xuất QA | Không có | Không có |
| Kết hợp | Kết hợp với thẻ thống kê và các bộ lọc bằng AND, quay về trang 1 | Không có | Không có |
| Phạm vi dữ liệu | Chỉ đơn giấy và Draft của trường người dùng | Không có | Không có |
| Lưu thất bại | Không có | Không có | Something went wrong. Please try again.<br>Dữ liệu đã nhập được giữ lại<br>Đề xuất QA, lấy từ thông báo chung của F4 |
| Ví dụ hợp lệ | aisha<br>AISHA<br>APP-2026-00412<br>00412<br>t1412345b<br>zzzz, không khớp, danh sách rỗng | Không có | Không có |
| Ví dụ không hợp lệ | Không có | 101 ký tự trở lên, bị cắt còn 100 | Không có |
| Placeholder | Search Application ID, uploaded by or EA number, nhìn thấy trong hình |  |  |
| Nguồn trong FS | FS 3 mục 3 |  |  |


Ghi chú: giới hạn 100 ký tự, thông báo Search is limited to 100 characters. và cách cắt chuỗi là Đề xuất QA lấy theo R4 (điểm mở O28).

### A4. Bộ lọc Status


| Mục | Quy tắc |
| :--- | :--- |
| Tùy chọn | All<br>Draft<br>Pending<br>Approved · MOEFAS<br>Approved · SBFAS<br>Rejected |
| Mặc định | All |
| Bắt buộc | Không |
| Phụ thuộc | Không có |
| Khi đổi | Bảng tải lại ở trang 1<br>Kết hợp với Search, Tier, Uploaded bằng AND<br>Quan hệ với thẻ thống kê A2 là điểm mở O22 |
| Thông báo | No applications found. khi rỗng. Đề xuất QA |
| Nguồn trong FS | FS 3 mục 4 |


### A5. Bộ lọc Tier


| Mục | Quy tắc |
| :--- | :--- |
| Tùy chọn | All<br>Các tier SBFAS của trường, theo thứ tự tăng dần |
| Mặc định | All |
| Bắt buộc | Không |
| Phụ thuộc | Các scheme SBFAS của trường |
| Khi đổi | Bảng tải lại ở trang 1<br>Cột Tier hiện trong bảng khi lọc SBFAS hoặc lọc theo tier |
| Nguồn trong FS | FS 3 mục 4, mục 5 |


### A6. Bộ lọc Uploaded


| Mục | Quy tắc |
| :--- | :--- |
| Tùy chọn | Last 7 days<br>Last 30 days<br>Any time |
| Mặc định | Last 7 days |
| Bắt buộc | Có, luôn có một giá trị |
| Phụ thuộc | Thời điểm tải lên của đơn |
| Khi đổi | Bảng tải lại ở trang 1<br>Bản Draft cũ hơn 7 ngày có bị ẩn hay không là điểm mở O13 |
| Nguồn trong FS | FS 3 mục 4 |


### A7. Bảng đơn


| Mã | Trường | Hiển thị | Quy tắc | Nguồn trong FS |
| :--- | :--- | :--- | :--- | :--- |
| A7 | Bảng đơn | File<br>Uploaded by<br>Uploaded at<br>Student, tên và số EA, lớp<br>Application ID<br>Status, kèm scheme và tier khi đã duyệt<br>Tier, khi lọc SBFAS hoặc lọc theo tier | Bản Draft được liệt kê trước<br>Application ID của Draft là Not submitted<br>Uploaded at định dạng DD/MM/YYYY HH:mm giờ Singapore. Đề xuất QA, theo quy tắc chung F4<br>Dữ liệu chỉ gồm học sinh của trường người dùng<br>Thứ tự các dòng đã nộp và phân trang là điểm mở O24 | FS 3 mục 5, 6 |


### A8. Dòng Draft, nút Continue và Delete


| Mục | Quy tắc |
| :--- | :--- |
| Chức năng | Continue mở lại bản nháp ở màn Review application. Delete xóa bản nháp |
| Hiển thị khi | Dòng có trạng thái Draft |
| Khi bấm Continue | Mẫu đơn được khôi phục đúng như lúc Save draft, theo từng trường<br>Bấm vào cả dòng cũng tiếp tục bản nháp |
| Khi bấm Delete | Bản nháp bị xóa, dòng biến mất, scan đi kèm bị xóa (BR6)<br>Không có hộp thoại xác nhận trong FS, đề xuất QA có xác nhận, điểm mở O13 |
| Khi bấm đúp | Thực hiện một lần |
| Hình | Hình không hiển thị nút Continue và Delete trên dòng Draft, điểm mở O23 |
| Nguồn trong FS | FS 3 mục 6, BR6, T9 |


### A9. Dòng đã nộp


| Mục | Quy tắc |
| :--- | :--- |
| Chức năng | Mở View application của màn F |
| Khi bấm | Mở mẫu đơn ở chế độ chỉ đọc, có nút Back to list |
| Nguồn trong FS | FS 3 mục 7, FS 8 |


### A10. Ghi chú cuối trang


| Mục | Quy tắc |
| :--- | :--- |
| Nội dung | Student is matched by NRIC/FIN against the school's enrolment (Function 3). Applications can be submitted only while a FAS application form is open. A student who already has an application this year is blocked at submit. Drafts appear in the list with status Draft until they are submitted. |
| Quy tắc | Chỉ hiển thị, nguyên văn như trên |
| Nguồn trong FS | FS 3 mục 8 |


# 4. Màn B. Hộp thoại Upload scans


Mở từ nút Upload scans của màn A. Nguồn: FS 4, FS 2 bước 1.

Hình B, hộp thoại Upload scans có một file

## 4.1. Tóm tắt trường


| Mã | Trường | Loại |
| :--- | :--- | :--- |
| B1 | Vùng kéo thả và chọn file | Chọn file |
| B2 | Danh sách file và nút Remove | Danh sách, nút |
| B3 | Nút Cancel | Nút |
| B4 | Nút Upload and read | Nút |


## 4.2. Quy tắc trường


### B1. Vùng kéo thả và chọn file


| Quy tắc | Hợp lệ | Không hợp lệ | Thông báo |
| :--- | :--- | :--- | :--- |
| Bắt buộc | Cần ít nhất một file để nút Upload and read bật | Không có file | Nút Upload and read tắt |
| Loại file | Phần mở rộng pdf, jpg, png, không phân biệt hoa thường | Mọi phần mở rộng khác, ví dụ docx, gif, tiff, exe | {file}: only PDF, JPG or PNG files. |
| Phần mở rộng jpeg | Điểm mở O26 | Điểm mở O26 | Điểm mở O26 |
| Nội dung thật của file | Phần đầu file khớp với phần mở rộng. Đề xuất QA | Phần mở rộng pdf nhưng nội dung là loại khác | {file}: only PDF, JPG or PNG files. Đề xuất QA |
| Hai phần mở rộng | Không có | form.pdf.exe, form.exe.pdf coi theo phần mở rộng cuối và kiểm nội dung thật | {file}: only PDF, JPG or PNG files. nếu nội dung không phải PDF, JPG, PNG |
| Dung lượng | Từ 1 byte đến đúng 10 MB | Trên 10 MB, ví dụ 10 MB cộng 1 byte | {file} is larger than 10 MB. |
| Đơn vị MB | Điểm mở O26, đề xuất QA 10 x 1024 x 1024 byte | Không có | Không có |
| File rỗng 0 byte | Không có | File rỗng | {file}: the file is empty. Đề xuất QA |
| Số file | 1 đến 5 file mỗi lần tải | File thứ 6 trở đi | Up to 5 files per application. |
| Chọn hoặc kéo nhiều file một lần | File hợp lệ được thêm, file không hợp lệ bị bỏ và có thông báo riêng từng file. Đề xuất QA | Không có | Mỗi file lỗi một thông báo |
| File thêm hai lần | Lần thứ hai bị bỏ qua. Đề xuất QA | Không có | {file} is already added. Đề xuất QA |
| Tên file | 1 đến 255 ký tự, có dấu cách, chữ Unicode, ký tự đặc biệt | Tên chứa ../ hoặc ký tự null: phần đường dẫn bị loại bỏ. Máy chủ tự đặt tên lưu trữ | Không có |
| Tên file chứa mã | Hiển thị là văn bản thường, ví dụ <img onerror=alert(1)>.pdf | Không có | Không bao giờ chạy hay dựng thành HTML |
| Nội dung PDF chủ động | Không bao giờ chạy hay mở JavaScript, hành động khởi chạy trong PDF | Không có | Đề xuất QA, xem mục G |
| File mã hóa mật khẩu, hỏng, trắng, sai mẫu đơn | Điểm mở O27, FS không nói | Điểm mở O27 | Điểm mở O27 |
| Ví dụ hợp lệ | scan_bvp_0667.pdf 812 KB | Không có | Không có |
| Ví dụ hợp lệ | page1.JPG, page2.png | Không có | Không có |
| Ví dụ hợp lệ | File PNG đúng 10 MB, 5 file mỗi file 1 MB | Không có | Không có |
| Ví dụ không hợp lệ | Không có | form.docx, photo.gif, scan.pdf 10 MB cộng 1 byte, file thứ 6 | Theo từng dòng quy tắc ở trên |
| Nguồn trong FS | FS 4, T1 |  |  |


### B2. Danh sách file và nút Remove


| Mục | Quy tắc |
| :--- | :--- |
| Hiển thị | Mỗi file một dòng, tên file và dung lượng, ví dụ scan_bvp_0667.pdf · 812 KB<br>Mỗi dòng có nút Remove |
| Khi bấm Remove | File bị bỏ khỏi danh sách<br>Số file giảm, có thể thêm file khác<br>Khi bỏ file cuối cùng, nút Upload and read tắt |
| Nguồn trong FS | FS 4, hình B |


### B3. Nút Cancel


| Mục | Quy tắc |
| :--- | :--- |
| Chức năng | Đóng hộp thoại, không tải gì |
| Khi bấm | Hộp thoại đóng<br>Các file đã chọn bị bỏ<br>Danh sách đơn không đổi |
| Nguồn trong FS | Hình B |


### B4. Nút Upload and read


| Mục | Quy tắc |
| :--- | :--- |
| Chức năng | Tải các scan lên, đọc mẫu đơn và mở màn Review application |
| Tắt khi | Chưa có file nào<br>Đang tải hoặc đang đọc |
| Khi bấm | Đọc mẫu đơn, mở màn C với các giá trị tìm được<br>Trường không chắc chắn được tô vàng<br>Engine OCR thật nằm ngoài phạm vi, prototype mô phỏng việc đọc |
| Khi bấm đúp | Chỉ tải và đọc một lần |
| Khi lỗi | Không có thông báo trong FS. Đề xuất QA: Something went wrong. Please try again., hộp thoại mở, file giữ nguyên |
| Đóng hộp thoại khi đang đọc | Điểm mở O27 |
| Lời nhắc của hộp thoại | Hình ghi One application is one student, trong khi một mẫu có thể có nhiều con. Điểm mở O2 |
| Nguồn trong FS | FS 4, FS 2 bước 1, FS 1.1 |


# 5. Màn C. Review application


Mở sau Upload and read hoặc Continue. Bản scan nằm bên trái, năm phần Part 1 đến Part 5 của Mẫu đơn FAS nằm bên phải. Ô xám là tự điền và khóa, ô vàng là chỗ trình đọc không chắc chắn. Nguồn: FS 5, FS 2 bước 2 đến 4.

Hình C, hình Review application của FS

## 5.1. Tóm tắt trường


| Mã | Trường | Loại |
| :--- | :--- | :--- |
| C1 | Nút Discard | Nút |
| C2 | Nút Save draft | Nút |
| C3 | Nút Review and submit | Nút |
| C4 | Khung xem bản scan | Chỉ hiển thị |
| C5 | Part 1, NRIC của người khai | Ô nhập văn bản |
| C6 | Part 1, Full name | Tự điền, khóa |
| C7 | Part 1, Date of birth | Tự điền, khóa |
| C8 | Part 1, Gender | Chọn |
| C9 | Part 1, Category | Chọn |
| C10 | Part 1, Nationality | Chọn |
| C11 | Part 1, Relationship to child | Chọn |
| C12 | Part 1, Phone number | Ô nhập văn bản |
| C13 | Part 1, Email | Ô nhập văn bản |
| C14 | Part 1, Address | Ô nhập văn bản |
| C15 | Part 1, School-based FAS | Hộp chọn |
| C16 | Part 2, NRIC của con | Ô nhập văn bản |
| C17 | Part 2, thông tin con tự điền | Tự điền, khóa |
| C18 | Part 2, Add child | Nút |
| C19 | Part 3, dòng thành viên gia đình | Ô nhập văn bản, chọn |
| C20 | Part 3, Add member và tóm tắt hộ | Nút, chỉ hiển thị |
| C21 | Part 4, Context | Ô nhập văn bản |
| C22 | Part 5, Declaration ticked | Hộp chọn |
| C23 | Part 5, Applicant's signature checked | Hộp chọn |
| C24 | Part 5, Received by | Chỉ hiển thị |
| C25 | Part 5, Date received | Chỉ hiển thị |
| C26 | Part 5, Date signed | Ô nhập ngày |


## 5.2. Quy tắc trường


### C1. Nút Discard


| Mục | Quy tắc |
| :--- | :--- |
| Chức năng | Xóa bản scan hoặc bản nháp đang mở |
| Hiển thị khi | Luôn luôn |
| Khi bấm | Bản scan vừa tải hoặc bản nháp bị xóa (BR6)<br>Về danh sách Upload applications<br>Dữ liệu đã nhập bị bỏ |
| Xác nhận | FS không có hộp thoại xác nhận. Đề xuất QA có hộp thoại xác nhận. Điểm mở O13 |
| Khi bấm đúp | Thực hiện một lần |
| Nguồn trong FS | FS 5 đoạn nút ở đầu trang, BR6 |


### C2. Nút Save draft


| Mục | Quy tắc |
| :--- | :--- |
| Chức năng | Lưu mẫu đơn đang nhập thành bản nháp |
| Hiển thị khi | Luôn luôn |
| Điều kiện | FS 2 bước 4a không có bước kiểm tra hợp lệ, nên suy luận Save draft không cần đủ trường bắt buộc. Dữ liệu sai định dạng có được lưu hay không là điểm mở O13 |
| Khi bấm | Lưu theo từng trường kèm người lưu và thời gian lưu (BR6)<br>Danh sách hiển thị dòng với trạng thái Draft, Application ID Not submitted<br>Mẫu đơn được khôi phục khi Continue (T9) |
| Khi bấm đúp | Lưu một bản nháp |
| Khi lỗi | Something went wrong. Please try again. Dữ liệu giữ nguyên. Đề xuất QA |
| Nguồn trong FS | FS 2 bước 4a, BR6, T9 |


### C3. Nút Review and submit


| Mục | Quy tắc |
| :--- | :--- |
| Chức năng | Kiểm tra hợp lệ rồi mở hộp thoại Review before submitting |
| Hiển thị khi | Luôn luôn |
| Khi bấm | Chạy toàn bộ kiểm tra của màn D<br>Nếu hợp lệ, mở hộp thoại của màn E<br>Nếu không hợp lệ, hiện các ghi chú đỏ ở đầu trang và không mở hộp thoại |
| Khi bấm đúp | Chỉ chạy kiểm tra một lần |
| Nguồn trong FS | FS 2 bước 4b, FS 6, BR7 |


### C4. Khung xem bản scan


| Mục | Quy tắc |
| :--- | :--- |
| Chức năng | Hiển thị các trang scan để đối chiếu với các trường bên phải |
| Quy tắc | Chỉ hiển thị<br>Dòng tô vàng cho biết trình đọc không chắc chắn về trường tương ứng |
| Điểm mở | Xem nhiều trang, phóng to, và việc ô vàng mất khi người dùng sửa trường: O27 |
| Nguồn trong FS | FS 1.1, FS 5 chú thích hình |


### C5. Part 1, NRIC của người khai


| Quy tắc | Hợp lệ | Không hợp lệ | Thông báo |
| :--- | :--- | :--- | :--- |
| Bắt buộc | Bắt buộc, không để trống | Để trống | Complete: Applicant NRIC. |
| Độ dài | Đúng 9 ký tự | Dưới 9 hoặc trên 9 ký tự | Enter a valid NRIC/FIN. Đề xuất QA. |
| Cấu trúc | 1 chữ cái đầu S, T, F hoặc G, 7 chữ số, 1 chữ cái cuối | Chữ cái đầu khác S, T, F, G. Chữ số ở vị trí chữ cái. Chữ cái cuối là số | Enter a valid NRIC/FIN. Đề xuất QA. Chữ cái đầu M của FIN mới là điểm mở O6 |
| Chữ hoa và chữ thường | Nhập chữ thường được tự đổi thành chữ hoa | Không có | Không có |
| Khoảng trắng | Khoảng trắng đầu và cuối bị cắt | Khoảng trắng ở giữa | Enter a valid NRIC/FIN. Đề xuất QA |
| Chữ cái kiểm tra cuối | Điểm mở O6. Phụ lục A mô tả thuật toán công khai. Ba NRIC mẫu trong hình FS đều không đạt | Chữ cái cuối sai theo thuật toán, nếu BA chọn kiểm tra | Enter a valid NRIC/FIN. Đề xuất QA |
| Ký tự đặc biệt, SQL, script, JSON, template | Không có | Mọi chuỗi ngoài cấu trúc trên, ví dụ S1234567A' OR '1'='1, <script>, {"a":1}, ../../etc/passwd | Enter a valid NRIC/FIN. Đề xuất QA. Giá trị không bao giờ ghép vào câu truy vấn, không bao giờ được hiển thị dưới dạng HTML |
| Ký tự điều khiển và null | Bị loại bỏ trước khi kiểm tra | Không có | Không có |
| Trùng NRIC trong cùng mẫu | Mỗi NRIC xuất hiện một lần trong người khai, các con và thành viên | Cùng một NRIC xuất hiện hai lần | The same NRIC/FIN appears twice. The applicant, each child and each family member must have a different NRIC/FIN. |
| Tra cứu | Khi đủ 9 ký tự hợp lệ, tra hồ sơ phụ huynh và dữ liệu Chính phủ. Kích hoạt khi rời ô hoặc Enter. Đề xuất QA | Không có | Không có |
| Tìm thấy | Điền C6 đến C10, C12, C13, C14 từ hồ sơ rồi khóa (BR3) | Không có | Không có |
| Không tìm thấy | FS không nói. Điểm mở O3 | Điểm mở O3 | Điểm mở O3 |
| Đổi NRIC sau khi đã điền | Giá trị tự điền được thay bằng giá trị của NRIC mới. C11 và C15 giữ nguyên. Đề xuất QA | Không có | Không có |
| Ví dụ hợp lệ trong FS | S7612345A | Không có | Không có |
| Nguồn trong FS | FS 5 Part 1, FS 6, BR3, T2, T7 |  |  |


### C6. Part 1, Full name


| Mục | Quy tắc |
| :--- | :--- |
| Chức năng | Hiển thị họ tên người khai lấy từ hồ sơ |
| Nguồn giá trị | Hồ sơ phụ huynh và dữ liệu Chính phủ, sau khi NRIC khớp |
| Khóa | Có, người dùng không sửa được (BR3) |
| Bắt buộc | Có |
| Thông báo | Complete: Applicant full name. |
| Khi không tự điền được | Điểm mở O3 và O4 |
| Nguồn trong FS | FS 5 Part 1, FS 6, BR3, T2 |


### C7. Part 1, Date of birth


| Mục | Quy tắc |
| :--- | :--- |
| Chức năng | Hiển thị ngày sinh người khai |
| Định dạng | DD/MM/YYYY, ngày hợp lệ theo lịch |
| Khóa | Có |
| Bắt buộc | Có |
| Thông báo | Complete: Applicant date of birth. |
| Giới hạn tuổi người khai | FS không nói, không kiểm tra |
| Nguồn trong FS | FS 5 Part 1, FS 6, T2 |


### C8. Part 1, Gender


| Mục | Quy tắc |
| :--- | :--- |
| Tùy chọn | Male<br>Female<br>Other |
| Mặc định | Giá trị tự điền khi NRIC khớp, nếu không thì chưa chọn |
| Bắt buộc | Có |
| Khóa | Có khi đã tự điền |
| Phụ thuộc | C5 |
| Thông báo | Complete: Gender. |
| Nguồn trong FS | FS 5 Part 1, FS 6 |


### C9. Part 1, Category


| Mục | Quy tắc |
| :--- | :--- |
| Tùy chọn | Singapore Citizen<br>Singapore PR<br>International ASEAN<br>International non ASEAN |
| Mặc định | Giá trị tự điền khi NRIC khớp, nếu không thì chưa chọn |
| Bắt buộc | Có |
| Khóa | Có khi đã tự điền |
| Phụ thuộc | C5 |
| Thông báo | Complete: Category. |
| Nguồn trong FS | FS 5 Part 1, FS 6 |


### C10. Part 1, Nationality


| Mục | Quy tắc |
| :--- | :--- |
| Tùy chọn | Chinese<br>Malay<br>Indian<br>Eurasian<br>Others |
| Mặc định | Giá trị tự điền khi NRIC khớp, nếu không thì chưa chọn |
| Bắt buộc | Có |
| Khóa | Có khi đã tự điền |
| Phụ thuộc | C5 |
| Thông báo | Complete: Nationality. |
| Ghi chú | Các giá trị là nhóm dân tộc, không phải quốc tịch. Điểm mở O7 |
| Nguồn trong FS | FS 5 Part 1, FS 6 |


### C11. Part 1, Relationship to child


| Mục | Quy tắc |
| :--- | :--- |
| Tùy chọn | Father<br>Mother<br>Legal guardian<br>Grandfather<br>Grandmother<br>Sibling<br>Uncle<br>Aunt<br>Cousin<br>Other |
| Mặc định | Giá trị đọc từ mẫu đơn, nếu không đọc được thì chưa chọn |
| Bắt buộc | Có |
| Khóa | Không, lấy từ mẫu đơn nên người dùng sửa được |
| Khi đổi | Không ảnh hưởng trường khác |
| Thông báo | Complete: Relationship to child. |
| Nguồn trong FS | FS 5 Part 1, FS 6 |


### C12. Part 1, Phone number


| Quy tắc | Hợp lệ | Không hợp lệ | Thông báo |
| :--- | :--- | :--- | :--- |
| Bắt buộc | Bắt buộc | Để trống | Complete: Phone number (up to 10 digits). |
| Ký tự cho phép | Chỉ chữ số 0 đến 9 | Chữ cái, dấu cộng, khoảng trắng, dấu gạch, ngoặc, ký tự đặc biệt | Ký tự không phải chữ số không được nhận khi gõ. Dán chuỗi có ký tự lạ: các ký tự này bị loại bỏ. Đề xuất QA. Hình hiển thị +65 9123 4567, điểm mở O5 |
| Độ dài | 1 đến 10 chữ số | 11 chữ số trở lên | Complete: Phone number (up to 10 digits). |
| Độ dài tối thiểu | FS không nói. Đề xuất QA tối thiểu 8 chữ số. Điểm mở O5 | Dưới mức tối thiểu | Complete: Phone number (up to 10 digits). Đề xuất QA |
| Khoảng trắng đầu cuối, tab, xuống dòng | Bị loại bỏ | Không có | Không có |
| Ký tự điều khiển và null | Bị loại bỏ | Không có | Không có |
| SQL, script, JSON | Không có | Chuỗi chứa chữ cái hoặc ký tự đặc biệt | Bị loại bỏ như ký tự không phải chữ số, không bao giờ tới cơ sở dữ liệu |
| Khóa | FS nói khóa sau khi tự điền, hình hiển thị ô vàng có thể sửa. Điểm mở O4 | Điểm mở O4 | Điểm mở O4 |
| Ví dụ hợp lệ | 91234567 | Không có | Không có |
| Ví dụ hợp lệ | 6591234567, đúng 10 chữ số | Không có | Không có |
| Ví dụ không hợp lệ | Không có | 65912345678, 11 chữ số | Complete: Phone number (up to 10 digits). |
| Nguồn trong FS | FS 5 Part 1, FS 6 |  |  |


### C13. Part 1, Email


| Quy tắc | Hợp lệ | Không hợp lệ | Thông báo |
| :--- | :--- | :--- | :--- |
| Bắt buộc | Bắt buộc | Để trống | Complete: Email. |
| Cấu trúc | Phần trước @, một dấu @, miền có ít nhất một dấu chấm, ví dụ wm.tan@example.com | Thiếu @, hai dấu @, thiếu miền, có khoảng trắng, dấu chấm đầu hoặc cuối phần trước @, hai dấu chấm liền nhau | Enter a valid email address. Đề xuất QA |
| Độ dài | Tối đa 254 ký tự, phần trước @ tối đa 64 ký tự. Đề xuất QA | Vượt giới hạn | Enter a valid email address. Đề xuất QA |
| Khoảng trắng đầu cuối | Được cắt bỏ | Khoảng trắng ở giữa | Enter a valid email address. Đề xuất QA |
| Chữ hoa chữ thường | Chấp nhận, so sánh không phân biệt hoa thường | Không có | Không có |
| Ký tự điều khiển và null | Bị loại bỏ, xuống dòng trong giá trị làm giá trị không hợp lệ | Chuỗi có xuống dòng, ví dụ a@b.com%0ABcc: x@y.com | Enter a valid email address. Chống chèn tiêu đề thư. Đề xuất QA |
| SQL, script, JSON, template | Không có | Mọi chuỗi ngoài cấu trúc trên, ví dụ '><script>@x.com | Enter a valid email address. Không bao giờ hiển thị dưới dạng HTML |
| Khóa | Giống C12, điểm mở O4 |  |  |
| Ví dụ hợp lệ | wm.tan@example.com, a.b+c@mail.example.sg | Không có | Không có |
| Ví dụ không hợp lệ | Không có | wm.tan@, @example.com, wm tan@example.com, wm.tan@@example.com | Enter a valid email address. |
| Nguồn trong FS | FS 5 Part 1, FS 6 |  |  |


### C14. Part 1, Address


| Quy tắc | Hợp lệ | Không hợp lệ | Thông báo |
| :--- | :--- | :--- | :--- |
| Bắt buộc | Bắt buộc, không để trống | Để trống | Complete: Address. |
| Độ dài | 1 đến 255 ký tự | 256 ký tự trở lên | Address must be 255 characters or fewer.<br>Đề xuất QA. |
| Khoảng trắng đầu và cuối | Được cắt bỏ trước khi kiểm tra và lưu | Không có | Không có |
| Chỉ có khoảng trắng | Coi như để trống | Không có | Không có thông báo riêng, áp dụng quy tắc Bắt buộc |
| Xuống dòng và tab | Thay bằng một khoảng trắng | Không có | Không có |
| Ký tự điều khiển U+0000 đến U+001F, U+007F | Bị loại bỏ, trừ xuống dòng và tab khi ô nhiều dòng | Không có | Không có |
| Ký tự null | Bị loại bỏ, không bao giờ tới cơ sở dữ liệu | Không có | Không có |
| Ký tự cho phép | Mọi ký tự in được của Unicode | Không có | Không có |
| Ký tự đặc biệt ' " % \ ; & < > | Lưu đúng như đã nhập | Không có | Hiển thị là văn bản thường |
| Chuỗi SQL, ví dụ ' OR '1'='1 | Lưu hoặc tìm như văn bản, truy vấn tham số hóa | Không có | Không đổi dữ liệu nào ngoài trường này |
| Script và HTML, ví dụ <script>alert(1)</script>, <img onerror>, javascript: | Lưu như đã nhập | Không có | Hiển thị là văn bản thường, không bao giờ chạy hay dựng thành HTML<br>Được mã hóa ở màn hình, hộp thoại, History, CSV và thư điện tử |
| JSON, XML, template, lệnh, ví dụ {"a":1}, ${jndi:ldap://x}, {{7*7}}, $(whoami), ../../etc/passwd | Lưu như văn bản thường, không bao giờ được phân tích hay thực thi | Không có | Dấu nháy và dấu gạch ngược được escape trong dữ liệu gửi qua API |
| Xuất CSV | Giá trị bắt đầu bằng dấu bằng, dấu cộng, dấu trừ hoặc @ được thêm dấu nháy đơn phía trước | Không có | Không có |
| Emoji và chữ của mọi hệ chữ viết | Được chấp nhận như văn bản | Không có | Không có |
| Khóa | Giống C12, điểm mở O4 | Không có | Không có |
| Giới hạn độ dài | FS không nói. 255 ký tự là Đề xuất QA, điểm mở O28 | Không có | Không có |
| Lưu thất bại | Không có | Không có | Something went wrong. Please try again.<br>Dữ liệu đã nhập được giữ lại<br>Đề xuất QA, lấy từ thông báo chung của F4 |
| Ví dụ hợp lệ | Blk 123 Bukit Batok St 21, Singapore 650123<br>Địa chỉ có dấu nháy, dấu phẩy, dấu thăng # | Không có | Không có |
| Ví dụ không hợp lệ | Không có | 256 ký tự trở lên | Không có |
| Nguồn trong FS | FS 5 Part 1, FS 6, T2 |  |  |


### C15. Part 1, School-based FAS


| Mục | Quy tắc |
| :--- | :--- |
| Nhãn | Also consider for SBFAS. Hình: School-based FAS, If not eligible for MOE FAS, the applicant agrees that the child's school considers this application |
| Giá trị | Chọn là Yes, bỏ chọn là No |
| Mặc định | Chọn, tức Yes |
| Bắt buộc | Không |
| Ảnh hưởng | Yes: đơn không được MOEFAS duyệt thì chuyển sang SBFAS của trường con<br>No: đơn không được MOEFAS duyệt thì Rejected (BR8)<br>Trường hợp con không đủ điều kiện quốc tịch MOEFAS với No là điểm mở O20 |
| Hiển thị lại | Giá trị hiện ở hộp thoại E1 và lưu cùng đơn, sửa được khi Pending |
| Nguồn trong FS | FS 5 Part 1, BR8, mục 7 |


### C16. Part 2, NRIC của con


| Quy tắc | Hợp lệ | Không hợp lệ | Thông báo |
| :--- | :--- | :--- | :--- |
| Bắt buộc | Bắt buộc, không để trống | Để trống | Child {n}: enter the NRIC/FIN. |
| Độ dài | Đúng 9 ký tự | Dưới 9 hoặc trên 9 ký tự | Enter a valid NRIC/FIN. Đề xuất QA. |
| Cấu trúc | 1 chữ cái đầu S, T, F hoặc G, 7 chữ số, 1 chữ cái cuối | Chữ cái đầu khác S, T, F, G. Chữ số ở vị trí chữ cái. Chữ cái cuối là số | Enter a valid NRIC/FIN. Đề xuất QA. Chữ cái đầu M của FIN mới là điểm mở O6 |
| Chữ hoa và chữ thường | Nhập chữ thường được tự đổi thành chữ hoa | Không có | Không có |
| Khoảng trắng | Khoảng trắng đầu và cuối bị cắt | Khoảng trắng ở giữa | Enter a valid NRIC/FIN. Đề xuất QA |
| Chữ cái kiểm tra cuối | Điểm mở O6. Phụ lục A mô tả thuật toán công khai. Ba NRIC mẫu trong hình FS đều không đạt | Chữ cái cuối sai theo thuật toán, nếu BA chọn kiểm tra | Enter a valid NRIC/FIN. Đề xuất QA |
| Ký tự đặc biệt, SQL, script, JSON, template | Không có | Mọi chuỗi ngoài cấu trúc trên, ví dụ S1234567A' OR '1'='1, <script>, {"a":1}, ../../etc/passwd | Enter a valid NRIC/FIN. Đề xuất QA. Giá trị không bao giờ ghép vào câu truy vấn, không bao giờ được hiển thị dưới dạng HTML |
| Ký tự điều khiển và null | Bị loại bỏ trước khi kiểm tra | Không có | Không có |
| Trùng NRIC trong cùng mẫu | Mỗi NRIC xuất hiện một lần trong người khai, các con và thành viên | Cùng một NRIC xuất hiện hai lần | The same NRIC/FIN appears twice. The applicant, each child and each family member must have a different NRIC/FIN. |
| Tra cứu hồ sơ MOE | Khi đủ 9 ký tự hợp lệ, tra hồ sơ học sinh và ghi danh hiện tại. Kích hoạt khi rời ô hoặc Enter. Đề xuất QA | Không có | Không có |
| Tìm thấy | Điền C17 rồi khóa (BR3) | Không có | Không có |
| Không tìm thấy | Không có | NRIC hợp lệ về cấu trúc nhưng không có trong hồ sơ MOE | Child {n}: no student with NRIC/FIN {nric} in MOE records. |
| Số con | Ít nhất 1 con. Số con tối đa là điểm mở O10 | Không có con nào | Complete: At least one child. |
| Tuổi | Từ đủ 7 đến 16 tuổi, xem VR-F5-04 | Ngoài khoảng | {tên} must be 7 to 16 years old (now {tuổi}). |
| Đã có đơn trong năm nay | Không có đơn nào của con trong năm hiện tại | Có đơn ở mọi trạng thái | {tên} already has an application this year ({id}, {status}). |
| Con học trường khác | Điểm mở O9 | Điểm mở O9 | Điểm mở O9 |
| Ví dụ hợp lệ trong FS | T1412345B, T1012345A | Không có | Không có |
| Nguồn trong FS | FS 5 Part 2, FS 6, BR2, BR3, T3, T4, T5 |  |  |


### C17. Part 2, thông tin con tự điền


| Mã | Trường | Hiển thị | Quy tắc | Nguồn trong FS |
| :--- | :--- | :--- | :--- | :--- |
| C17 | Thông tin con | Full name<br>Date of birth<br>Gender<br>School<br>Level<br>Grade<br>Class | Tự điền từ hồ sơ MOE, ghi danh hiện tại và lớp, rồi khóa, không sửa được (BR3)<br>Date of birth DD/MM/YYYY, Gender hiển thị F hoặc M như trong hình<br>School, Grade, Class lấy từ ghi danh hiện tại<br>Level suy ra từ Grade, bảng bên dưới<br>Nếu tên của con khác dữ liệu Chính phủ: có ghi chú cho biết MOE sẽ thấy cảnh báo sai lệch dữ liệu, người dùng vẫn nộp được. Nội dung ghi chú là điểm mở O17<br>Không có hàng nào khi chưa tra cứu được NRIC | FS 5 Part 2, BR3, T3 |


| Grade | Level suy ra |
| :--- | :--- |
| P1 đến P6 | Primary |
| S1 đến S5 | Secondary |
| PU1 đến PU3 | Pre-University |
| Giá trị khác | FS không nói, điểm mở O8 |


### C18. Part 2, Add child


| Mục | Quy tắc |
| :--- | :--- |
| Chức năng | Thêm một dòng con mới |
| Khi bấm | Hiện thêm dòng với NRIC trống |
| Giới hạn | Số con tối đa và nút xóa dòng không có trong FS, điểm mở O10 |
| Nguồn trong FS | FS 5 Part 2, ghi chú Add child trong hình |


### C19. Part 3, dòng thành viên gia đình


| Quy tắc | Hợp lệ | Không hợp lệ | Thông báo |
| :--- | :--- | :--- | :--- |
| Tính chất | Cả phần là tùy chọn | Không có | Không có |
| Dòng nhập dở | Không có | Có họ tên mà thiếu NRIC, hoặc ngược lại | Complete: Family members (name and NRIC). |
| Full name, độ dài | 1 đến 100 ký tự. Đề xuất QA | 101 ký tự trở lên | Full name must be 100 characters or fewer. Đề xuất QA |
| Full name, ký tự | Chữ của mọi hệ chữ viết, khoảng trắng, dấu nháy đơn, dấu chấm, dấu gạch nối trong tên | Chữ số, ký tự đặc biệt <, >, ;, {, } | Full name contains invalid characters. Đề xuất QA |
| Full name, mã | Không có | Script, SQL, JSON, template | Bị từ chối như ký tự không hợp lệ, không bao giờ chạy |
| NRIC | Theo C5, không tra hồ sơ, không khóa | Theo C5 | Theo C5. Trùng người khai hoặc con: The same NRIC/FIN appears twice. The applicant, each child and each family member must have a different NRIC/FIN. |
| Gender | Male, Female, Other. Tùy chọn của thành viên là Đề xuất QA, điểm mở O11 | Không có | Không có |
| Số thành viên | Số tối đa và xóa dòng là điểm mở O10 | Không có | Không có |
| Ví dụ hợp lệ | Lim Hui Min, NRIC S7812345F là ví dụ về cấu trúc | Không có | Không có |
| Nguồn trong FS | FS 5 Part 3, FS 6, BR4, T7 |  |  |


### C20. Part 3, Add member và tóm tắt hộ gia đình


| Mã | Trường | Hiển thị | Quy tắc | Nguồn trong FS |
| :--- | :--- | :--- | :--- | :--- |
| C20 | Add member | Nút | Thêm một dòng thành viên trống | FS 5 Part 3 |
| C20 | Tóm tắt hộ | Gross household income, GHI<br>Household size<br>Per capita income, PCI | Chỉ hiển thị, không có ô thu nhập (BR4)<br>Thu nhập lấy từ dữ liệu Chính phủ cho người khai và từng thành viên<br>Household size bằng 1 người khai cộng số con cộng số thành viên. Hình: 1 + 2 + 1 = 4<br>PCI bằng GHI chia Household size. Hình: 4,300.00 chia 4 bằng 1,075.00. Suy luận từ hình<br>Tiền định dạng S$ #,##0.00 mỗi tháng<br>Tính lại khi thêm, bỏ, đổi NRIC thành viên<br>Trẻ em có tính vào GHI, thiếu dữ liệu thu nhập, làm tròn PCI: điểm mở O12 | FS 5 Part 3, FS 7, BR4 |


### C21. Part 4, Context


| Quy tắc | Hợp lệ | Không hợp lệ | Thông báo |
| :--- | :--- | :--- | :--- |
| Bắt buộc | Để trống hoặc có giá trị | Không có | Không có |
| Độ dài | 0 đến 2000 ký tự | 2001 ký tự trở lên | Context must be 2000 characters or fewer.<br>Đề xuất QA. |
| Bộ đếm | Hiển thị n/2000 | Không có | Dòng mới tính 1 ký tự<br>Emoji tính 1 ký tự<br>Đề xuất QA. |
| Khoảng trắng đầu và cuối | Được cắt bỏ trước khi kiểm tra và lưu | Không có | Không có |
| Chỉ có khoảng trắng | Coi như để trống | Không có | Không có thông báo riêng, áp dụng quy tắc Bắt buộc |
| Xuống dòng và tab | Được giữ, xuống dòng tính 1 ký tự | Không có | Không có |
| Ký tự điều khiển U+0000 đến U+001F, U+007F | Bị loại bỏ, trừ xuống dòng và tab khi ô nhiều dòng | Không có | Không có |
| Ký tự null | Bị loại bỏ, không bao giờ tới cơ sở dữ liệu | Không có | Không có |
| Ký tự cho phép | Mọi ký tự in được của Unicode | Không có | Không có |
| Ký tự đặc biệt ' " % \ ; & < > | Lưu đúng như đã nhập | Không có | Hiển thị là văn bản thường |
| Chuỗi SQL, ví dụ ' OR '1'='1 | Lưu hoặc tìm như văn bản, truy vấn tham số hóa | Không có | Không đổi dữ liệu nào ngoài trường này |
| Script và HTML, ví dụ <script>alert(1)</script>, <img onerror>, javascript: | Lưu như đã nhập | Không có | Hiển thị là văn bản thường, không bao giờ chạy hay dựng thành HTML<br>Được mã hóa ở màn hình, hộp thoại, History, CSV và thư điện tử |
| JSON, XML, template, lệnh, ví dụ {"a":1}, ${jndi:ldap://x}, {{7*7}}, $(whoami), ../../etc/passwd | Lưu như văn bản thường, không bao giờ được phân tích hay thực thi | Không có | Dấu nháy và dấu gạch ngược được escape trong dữ liệu gửi qua API |
| Xuất CSV | Giá trị bắt đầu bằng dấu bằng, dấu cộng, dấu trừ hoặc @ được thêm dấu nháy đơn phía trước | Không có | Không có |
| Emoji và chữ của mọi hệ chữ viết | Được chấp nhận như văn bản | Không có | Không có |
| Dán quá 2000 | Văn bản được giữ nguyên, không cắt, bộ đếm đỏ, ví dụ 2100/2000 | Không có | Review and submit và Save draft bị chặn với thông báo ở dòng Độ dài. Đề xuất QA |
| Định dạng | Văn bản thuần, đúng như viết trên mẫu đơn (BR5) | Không có | Không có |
| Hiển thị | Hiện ở hộp thoại Review before submitting và ở drawer F4 | Không có | Không có |
| Lưu thất bại | Không có | Không có | Something went wrong. Please try again.<br>Dữ liệu đã nhập được giữ lại<br>Đề xuất QA, lấy từ thông báo chung của F4 |
| Ví dụ hợp lệ | Father works shifts; the family hopes for help with transport.<br>Đúng 2000 ký tự<br>Hai dòng cách nhau bởi xuống dòng<br><b>ok</b> hiển thị đúng như vậy | Không có | Không có |
| Ví dụ không hợp lệ | Không có | 2001 ký tự trở lên | Không có |
| Nguồn trong FS | FS 5 Part 4, BR5, T11 |  |  |


### C22. Part 5, Declaration ticked


| Mục | Quy tắc |
| :--- | :--- |
| Nhãn | The applicant ticked the declaration (information is true, legal responsibility) |
| Giá trị | Chọn hoặc bỏ chọn |
| Mặc định | Bỏ chọn. Đề xuất QA, nếu trình đọc nhận ra ô đã đánh dấu trên mẫu thì có thể tô sẵn, điểm mở O27 |
| Bắt buộc | Có |
| Thông báo | Complete: Declaration. |
| Nguồn trong FS | FS 5 Part 5, FS 6 |


### C23. Part 5, Applicant's signature checked


| Mục | Quy tắc |
| :--- | :--- |
| Nhãn | Applicant's signature checked |
| Giá trị | Chọn khi người dùng đã kiểm tra chữ ký trên bản scan |
| Mặc định | Bỏ chọn. Đề xuất QA |
| Bắt buộc | Có |
| Thông báo | Complete: Applicant signature checked. |
| Nguồn trong FS | FS 5 Part 5, FS 6, T8 |


### C24. Part 5, Received by


| Mục | Quy tắc |
| :--- | :--- |
| Giá trị | Tên School user đang đăng nhập, ví dụ Lan Nguyen |
| Quy tắc | Chỉ đọc, không sửa được |
| Nguồn trong FS | FS 5 Part 5 |


### C25. Part 5, Date received


| Mục | Quy tắc |
| :--- | :--- |
| Giá trị | Ngày hôm nay theo giờ Singapore, định dạng DD/MM/YYYY |
| Quy tắc | Chỉ đọc<br>Khi tiếp tục một bản nháp ở ngày khác, hiển thị ngày của hôm nay. Đề xuất QA |
| Nguồn trong FS | FS 5 Part 5 |


### C26. Part 5, Date signed


| Quy tắc | Hợp lệ | Không hợp lệ | Thông báo |
| :--- | :--- | :--- | :--- |
| Bắt buộc | Bắt buộc | Để trống | Complete: Date signed. |
| Định dạng | DD/MM/YYYY, ngày và tháng đủ 2 chữ số, năm 4 chữ số, dấu gạch chéo | Dùng dấu khác, năm 2 chữ số, ví dụ 15-10-2026, 15/10/26 | Enter a valid date (DD/MM/YYYY). Đề xuất QA |
| Ngày theo lịch | 15/10/2026, 29/02/2028 là năm nhuận | 31/04/2026, 29/02/2027, 00/10/2026, 15/13/2026 | Enter a valid date (DD/MM/YYYY). Đề xuất QA |
| Ngày trong tương lai | Không sau Date received. Đề xuất QA | Sau Date received | Date signed cannot be after the date received. Đề xuất QA |
| Giới hạn dưới | FS không nói, điểm mở O15 | Điểm mở O15 | Điểm mở O15 |
| Chữ, SQL, script, JSON | Không có | Mọi chuỗi không phải ngày | Enter a valid date (DD/MM/YYYY). |
| Ví dụ hợp lệ | 15/10/2026 trong hình, ngày hôm nay | Không có | Không có |
| Nguồn trong FS | FS 5 Part 5, FS 6, T8 |  |  |


# 6. Màn D. Kiểm tra hợp lệ khi bấm Review and submit


Chạy khi bấm C3. Kết quả hiện thành các ghi chú đỏ ở đầu trang Review application, hộp thoại E không mở. Hình D cho thấy hai ghi chú cùng lúc: một ghi chú Complete và một ghi chú form đã đóng. Suy luận từ hình: mọi kiểm tra không đạt được hiển thị cùng một lần, mỗi loại một ghi chú. Nguồn: FS 6.

Hình D, trạng thái bị chặn khi nộp, thiếu trường bắt buộc và form nộp đơn đã đóng

| Mã | Trường | Loại |
| :--- | :--- | :--- |
| D1 | Ghi chú Complete | Chỉ hiển thị |
| D2 | Ghi chú form đã đóng và các ghi chú theo con | Chỉ hiển thị |
| D3 | Nút Review and submit (mã C3) | Nút |


| ID | Quy tắc | Điều kiện | Thông báo và phản ứng | Nguồn |
| :--- | :--- | :--- | :--- | :--- |
| VR-F5-01 | Thiếu trường bắt buộc | Một hay nhiều trường bắt buộc còn trống | Complete: {danh sách}.<br>Danh sách theo thứ tự: Applicant NRIC, Applicant full name, Applicant date of birth, Gender, Category, Nationality, Relationship to child, Phone number (up to 10 digits), Email, Address, At least one child, Family members (name and NRIC), Declaration, Applicant signature checked, Date signed<br>Ngăn cách bằng dấu phẩy, kết thúc bằng dấu chấm, ví dụ Complete: Applicant signature checked, Date signed. | FS 6, T8 |
| VR-F5-02 | NRIC của con trống | Dòng con có NRIC trống | Child {n}: enter the NRIC/FIN. | FS 6 |
| VR-F5-03 | NRIC của con không có trong hồ sơ MOE | NRIC không tra ra học sinh | Child {n}: no student with NRIC/FIN {nric} in MOE records. | FS 6, T4 |
| VR-F5-04 | Con ngoài độ tuổi 7 đến 16 | Tuổi tính tại ngày nộp, ngoài khoảng | {tên} must be 7 to 16 years old (now {tuổi}).<br>Biên: đúng ngày sinh nhật thứ 7 hợp lệ, một ngày trước đó không hợp lệ<br>Một ngày trước sinh nhật thứ 17 hợp lệ, đúng ngày sinh nhật thứ 17 không hợp lệ, theo T5. Đề xuất QA<br>Mâu thuẫn với FS01: điểm mở O1 | FS 6, BR2, T5 |
| VR-F5-05 | Con đã có đơn trong năm nay | Có đơn của con trong năm hiện tại, mọi trạng thái, Draft không tính | {tên} already has an application this year ({id}, {status}). | FS 6, BR2, FS 3 mục 8 |
| VR-F5-06 | Không có con nào học tại trường người dùng | Không con nào có ghi danh tại trường của School user | At least one child must be enrolled at {trường}. | FS 6, BR2, T6 |
| VR-F5-07 | Form FAS đang đóng | Ngày nộp ngoài khoảng Form opens đến Form closes của MOEFAS và của SBFAS của trường con | {tên}: the FAS application form is closed (next opens DD/MM/YYYY).<br>Bỏ phần ngày khi chưa có form kế tiếp được publish: {tên}: the FAS application form is closed.<br>Biên hai đầu khoảng, form áp dụng cho con không phải công dân, một con đóng một con mở: điểm mở O16 | FS 6, BR9, T13 |
| VR-F5-08 | NRIC trùng | Cùng một NRIC xuất hiện từ hai lần trong người khai, các con, các thành viên | The same NRIC/FIN appears twice. The applicant, each child and each family member must have a different NRIC/FIN. | FS 6, BR4, T7 |
| VR-F5-09 | Hiển thị ghi chú | Có ít nhất một kiểm tra không đạt | Ghi chú đỏ ở đầu trang, hộp thoại E không mở<br>Một ghi chú cho mỗi loại, ghi chú theo con lặp cho từng con<br>Trang cuộn lên đầu. Đề xuất QA<br>Ghi chú biến mất khi bấm lại Review and submit rồi chạy lại kiểm tra. Đề xuất QA<br>Cảnh báo sai lệch tên của con không chặn nộp | FS 6, FS 5, hình D |
| VR-F5-10 | Kiểm tra lại khi Confirm and submit | Giữa lúc mở hộp thoại E và lúc bấm Confirm, form đóng hoặc con đã có đơn do người khác nộp | Chạy lại VR-F5-02 đến VR-F5-08 ở máy chủ, nếu không đạt thì không tạo đơn nào và hiện thông báo tương ứng. Đề xuất QA<br>Tạo đơn của mọi con trong cùng một giao dịch, hoặc tạo hết hoặc không tạo gì. Đề xuất QA, điểm mở O18 | FS 2 bước 5 |


# 7. Màn E. Hộp thoại Review before submitting


Mở khi các kiểm tra của màn D đạt. Tiêu đề phụ: One application per child. MOEFAS is assessed automatically after the application form closes. Nguồn: FS 7, FS 2 bước 5.

Hình E, hộp thoại Review before submitting của mẫu có hai con

## 7.1. Tóm tắt trường


| Mã | Trường | Loại |
| :--- | :--- | :--- |
| E1 | Part 1, Applicant | Chỉ hiển thị |
| E2 | Part 2, Children | Chỉ hiển thị |
| E3 | Part 3, Household | Chỉ hiển thị |
| E4 | Part 4, Context | Chỉ hiển thị |
| E5 | Nút Back to edit | Nút |
| E6 | Nút Confirm and submit | Nút |


## 7.2. Quy tắc trường


| Mã | Trường | Hiển thị | Quy tắc | Nguồn trong FS |
| :--- | :--- | :--- | :--- | :--- |
| E1 | Part 1, Applicant | Applicant: tên, NRIC, quan hệ<br>Category và Nationality<br>Contact: điện thoại, email<br>School-based FAS: Yes hoặc No | Chỉ đọc<br>Hiển thị đúng giá trị đang có ở màn C<br>Địa chỉ không hiển thị trong hình, điểm mở O25 | FS 7 |
| E2 | Part 2, Children | Mỗi con một dòng: tên, NRIC<br>Trường, khối, lớp, số EA | Chỉ đọc<br>Tiêu đề hiển thị số con, ví dụ Children (2)<br>Số EA lấy từ tài khoản giáo dục của con, con chưa có EA hiển thị thế nào là điểm mở O25 | FS 7 |
| E3 | Part 3, Household | Other family members<br>Household size<br>Gross household income, kèm Government records<br>Per capita income | Chỉ đọc, giá trị bằng C20<br>Tiền S$ #,##0.00 | FS 7, BR4 |
| E4 | Part 4, Context | Nội dung Context | Chỉ đọc, hiển thị là văn bản thuần<br>Không có Context thì phần này để trống hoặc ẩn, điểm mở O25 | FS 7, T11 |


### E5. Nút Back to edit


| Mục | Quy tắc |
| :--- | :--- |
| Chức năng | Đóng hộp thoại và quay về màn Review application |
| Khi bấm | Hộp thoại đóng<br>Không lưu gì, không tạo đơn<br>Dữ liệu ở màn C giữ nguyên |
| Nguồn trong FS | FS 7 |


### E6. Nút Confirm and submit


| Mục | Quy tắc |
| :--- | :--- |
| Chức năng | Nộp đơn |
| Tắt khi | Đang xử lý lần bấm trước |
| Khi bấm | Tạo một đơn cho mỗi con, nguồn Paper<br>Nhiều con dùng chung một mã gia đình (BR1)<br>Phân luồng từng đơn theo quy tắc F4 (BR8)<br>Con đủ điều kiện quốc tịch MOEFAS: MOEFAS Pending cho đến khi form MOEFAS đóng, sau đó xếp hạng và quyết định tự động<br>Con không đủ điều kiện MOEFAS về quốc tịch: SBFAS Pending, gửi trường của con<br>Bản nháp bị xóa (BR6)<br>Hộp thoại đóng. Chuyển về danh sách. Suy luận, FS không nói, điểm mở O19 |
| Khi thành công | Toast Application submitted for assessment. cho một đơn, Applications submitted. cho nhiều đơn. Cách ghép toast với số đơn là suy luận từ cách đặt tên |
| Khi bấm đúp | Chỉ tạo một bộ đơn, không trùng |
| Khi hai người cùng nộp một con | Người đầu thành công, người sau bị chặn với {tên} already has an application this year ({id}, {status}). Đề xuất QA |
| Khi form đóng hoặc đã có đơn trong lúc mở hộp thoại | VR-F5-10 |
| Khi lỗi | Something went wrong. Please try again. Hộp thoại giữ mở, không tạo đơn nào. Đề xuất QA |
| Nguồn trong FS | FS 2 bước 5, FS 7, BR1, BR6, BR7, BR8, T10 |


# 8. Màn F. Xem và sửa đơn đã nộp


FS không có hình cho màn này. Màn là chính mẫu đơn của màn C ở chế độ chỉ đọc, mở từ dòng đã nộp của danh sách. Nguồn: FS 8, BR9.

| Mã | Trường | Loại |
| :--- | :--- | :--- |
| F1 | Mẫu đơn đã nộp | Chỉ đọc hoặc nhập khi sửa |
| F2 | Nút Back to list | Nút |
| F3 | Nút Edit | Nút |
| F4 | Nút Save changes | Nút |
| F5 | History | Chỉ hiển thị |


### F1. Mẫu đơn đã nộp


| Mục | Quy tắc |
| :--- | :--- |
| Chế độ xem | Cùng mẫu đơn, mọi trường chỉ đọc |
| Chế độ sửa | Chỉ khi đơn còn Pending<br>Các trường có thể sửa: mẫu đơn, hộ gia đình, thu nhập, quan hệ, Also consider SBFAS, Context<br>Trường nào của mẫu đơn được sửa, NRIC của con có sửa không: điểm mở O21 |
| Kiểm tra khi lưu | Áp dụng VR-F5-01, VR-F5-02, VR-F5-03, VR-F5-04, VR-F5-06 và VR-F5-08<br>Không áp dụng VR-F5-07, vì BR9 cho sửa đơn Pending sau khi form đóng<br>VR-F5-05 không tính chính đơn đang sửa. Suy luận, FS không nói |
| Nguồn trong FS | FS 8, BR9 |


### F2. Nút Back to list


| Mục | Quy tắc |
| :--- | :--- |
| Chức năng | Về danh sách Upload applications |
| Khi bấm | Về danh sách, giữ tab và bộ lọc. Đề xuất QA |
| Nguồn trong FS | FS 8 |


### F3. Nút Edit


| Mục | Quy tắc |
| :--- | :--- |
| Hiển thị khi | Đơn có trạng thái Pending |
| Ẩn khi | Đơn đã Approved MOEFAS, Approved SBFAS hoặc Rejected. Truy cập chỉnh sửa bằng API cũng bị từ chối |
| Khi bấm | Mẫu đơn chuyển sang chế độ sửa |
| Nguồn trong FS | FS 8 |


### F4. Nút Save changes


| Mục | Quy tắc |
| :--- | :--- |
| Chức năng | Lưu thay đổi của đơn Pending |
| Khi bấm | Cập nhật mẫu đơn, hộ gia đình, thu nhập, quan hệ, Also consider SBFAS và Context của đơn đó<br>Thêm History: Paper application edited<br>Luồng quyết định không chạy lại |
| Đơn đã đổi trạng thái trong lúc sửa | Không lưu gì<br>Thông báo: This application was already decided by {user} on {DD/MM/YYYY}. Đề xuất QA, lấy từ thông báo chung của F4, điểm mở O21 |
| Khi bấm đúp | Lưu một lần, một mục History |
| Khi lỗi | Something went wrong. Please try again. Đề xuất QA |
| Nguồn trong FS | FS 8, T12 |


### F5. History


| Mục | Quy tắc |
| :--- | :--- |
| Nội dung | Mỗi lần Save changes thêm một dòng Paper application edited, kèm người sửa và thời gian. Người và thời gian là Đề xuất QA |
| Nguồn trong FS | FS 8, T12 |


# 9. Màn G. Quy tắc máy chủ, API và dữ liệu dùng chung


Không có màn hình. Các quy tắc phải do máy chủ thực thi, dù giao diện đã chặn. Nguồn: FS 1.2, FS 2, FS 9 và Đề xuất QA.

| ID | Quy tắc | Điều kiện | Phản ứng của hệ thống | Nguồn |
| :--- | :--- | :--- | :--- | :--- |
| VR-F5-S01 | Cách ly dữ liệu theo trường | School user truy cập đơn hoặc Draft của trường khác, bằng giao diện hay API | Không trả dữ liệu, thông báo You do not have access to this application. Thông báo là Đề xuất QA, lấy từ F4 | FS 1.2 |
| VR-F5-S02 | MOE HQ không truy cập | Tài khoản MOE HQ gọi màn hoặc API của F5 | Bị từ chối, không có dữ liệu | FS 1.2 |
| VR-F5-S03 | Kiểm tra lại mọi quy tắc ở máy chủ | Yêu cầu nộp bỏ qua giao diện | Chạy lại VR-F5-01 đến VR-F5-08, không tin dữ liệu của trình duyệt. Trường tự điền và khóa lấy lại từ hồ sơ, không nhận giá trị gửi lên | BR3 |
| VR-F5-S04 | Một đơn mỗi con mỗi năm | Hai yêu cầu nộp cùng một con gần như đồng thời | Chỉ một đơn được tạo, ràng buộc duy nhất ở cơ sở dữ liệu, yêu cầu sau nhận thông báo VR-F5-05. Đề xuất QA | BR2 |
| VR-F5-S05 | Mã gia đình | Mẫu có nhiều con | Các đơn dùng chung một mã gia đình, mẫu một con có mã gia đình riêng. Đề xuất QA về mẫu một con | BR1, T10 |
| VR-F5-S06 | Nguồn đơn | Đơn tạo từ F5 | Nguồn là Paper, phân biệt với đơn online của F10 | FS 2 bước 5 |
| VR-F5-S07 | Application ID | Tạo đơn | Duy nhất, định dạng như hình, APP, năm, số thứ tự. Suy luận từ hình, ví dụ APP-2026-00412 | Hình A |
| VR-F5-S08 | Bản nháp | Save draft | Lưu theo từng trường kèm người lưu và thời gian, thuộc trường, hiển thị trạng thái Draft, bị xóa khi nộp, Discard hoặc Delete | BR6 |
| VR-F5-S09 | Lưu file scan | Upload and read | File lưu ngoài thư mục web, tên do máy chủ đặt, chỉ School user của trường tải xuống được, gửi với tiêu đề tải xuống và loại nội dung đúng. Quét mã độc. Đề xuất QA | FS 4 |
| VR-F5-S10 | Nguồn dữ liệu ngoài không sẵn sàng | Hồ sơ MOE, hồ sơ phụ huynh hoặc API Chính phủ lỗi | FS không nói. Đề xuất QA: Something went wrong. Please try again., không tự điền, không cho nộp khi thiếu thu nhập. Điểm mở O3, O12 | FS 2 |
| VR-F5-S11 | Quyết định sau khi nộp | Đơn MOEFAS đã nộp | Pending cho đến khi form MOEFAS đóng, sau đó xếp hạng theo mức cần hỗ trợ và duyệt nếu đủ điều kiện, nếu không thì SBFAS của trường khi Also consider SBFAS là Yes, hoặc Rejected. Quy tắc quyết định thuộc F4 | BR8 |
| VR-F5-S12 | Sửa đơn | Gọi API sửa đơn | Chỉ khi đơn Pending, kể cả sau khi form đóng. Mọi trạng thái khác bị từ chối, ghi History | BR9, FS 8 |
| VR-F5-S13 | Định dạng | Mọi giá trị hiển thị | Ngày DD/MM/YYYY, giờ HH:mm giờ Singapore UTC+8, tiền S$ #,##0.00. Đề xuất QA, theo quy tắc F4 | F4 8.1 |


# 10. Thông báo dùng chung


| Tình huống | Thông báo hoặc hiển thị | Hành vi | Trường | Nguồn |
| :--- | :--- | :--- | :--- | :--- |
| File sai loại | {file}: only PDF, JPG or PNG files. | File bị từ chối, file khác giữ nguyên | B1 | FS 4, T1 |
| File quá lớn | {file} is larger than 10 MB. | File bị từ chối | B1 | FS 4 |
| Quá 5 file | Up to 5 files per application. | File từ thứ 6 bị từ chối | B1 | FS 4 |
| Thiếu trường bắt buộc | Complete: {danh sách}. | Ghi chú đỏ đầu trang, hộp thoại E không mở | C5 đến C26 | FS 6, T8 |
| NRIC của con trống | Child {n}: enter the NRIC/FIN. | Ghi chú đỏ | C16 | FS 6 |
| NRIC của con không có trong hồ sơ MOE | Child {n}: no student with NRIC/FIN {nric} in MOE records. | Ghi chú đỏ | C16 | FS 6, T4 |
| Con ngoài độ tuổi | {tên} must be 7 to 16 years old (now {tuổi}). | Ghi chú đỏ | C16 | FS 6, T5 |
| Con đã có đơn | {tên} already has an application this year ({id}, {status}). | Ghi chú đỏ | C16, E6 | FS 6 |
| Không con nào học tại trường | At least one child must be enrolled at {trường}. | Ghi chú đỏ | C16 | FS 6, T6 |
| Form FAS đóng | {tên}: the FAS application form is closed (next opens DD/MM/YYYY). | Ghi chú đỏ. Bỏ phần ngày khi chưa có form kế tiếp | C3, E6 | FS 6, T13 |
| NRIC trùng | The same NRIC/FIN appears twice. The applicant, each child and each family member must have a different NRIC/FIN. | Ghi chú đỏ | C5, C16, C19 | FS 6, T7 |
| Nộp thành công | Application submitted for assessment. cho một đơn | Toast, danh sách tải lại | E6 | FS 2 bước 5 |
| Nộp thành công nhiều đơn | Applications submitted. | Toast | E6 | FS 2 bước 5 |
| Sửa thành công | History: Paper application edited | Không có toast trong FS | F4 | FS 8 |
| Danh sách rỗng hoặc tìm không có kết quả | No applications found. | Bảng rỗng. Đề xuất QA, lấy từ F4 | A3, A4, A5, A6 | Đề xuất QA |
| Lỗi hệ thống | Something went wrong. Please try again. | Không lưu gì, hộp thoại giữ mở. Đề xuất QA, lấy từ F4 | B4, C2, E6, F4 | Đề xuất QA |
| Truy cập đơn của trường khác | You do not have access to this application. | Không có dữ liệu. Đề xuất QA, lấy từ F4 | A7, A9, VR-F5-S01 | Đề xuất QA |
| Đơn đã được quyết định trong lúc sửa | This application was already decided by {user} on {DD/MM/YYYY}. | Không lưu. Đề xuất QA, lấy từ F4 | F4 | Đề xuất QA |
| Lỗi định dạng của trường | Enter a valid NRIC/FIN. | Lỗi ở trường, Review and submit chặn | C5, C16, C19 | Đề xuất QA |
|  | Enter a valid email address. |  | C13 | Đề xuất QA |
|  | Enter a valid date (DD/MM/YYYY). |  | C26 | Đề xuất QA |
|  | Date signed cannot be after the date received. |  | C26 | Đề xuất QA |
|  | Context must be 2000 characters or fewer. |  | C21 | Đề xuất QA |
|  | Address must be 255 characters or fewer. |  | C14 | Đề xuất QA |
|  | Full name must be 100 characters or fewer. |  | C19 | Đề xuất QA |
|  | Full name contains invalid characters. |  | C19 | Đề xuất QA |
|  | {file}: the file is empty. |  | B1 | Đề xuất QA |
|  | {file} is already added. |  | B1 | Đề xuất QA |
|  | Search is limited to 100 characters. | Văn bản bị cắt còn 100 | A3 | Đề xuất QA |


# 11. Điểm mở cho BA


| Mã | Chủ đề | Chi tiết | Trường |
| :--- | :--- | :--- | :--- |
| O1 | Độ tuổi 7 đến 16 | FS05 mục 6, BR2, T5 chặn con 17 tuổi và cho phép con đủ 16 tuổi. FS01 F01-BR02 ghi tuổi đủ điều kiện từ đủ 7 tuổi đến trước sinh nhật 16 tuổi, và F02 đóng Education Account khi đủ 16 tuổi. Hình Review application có một con học S4 sinh năm 2010, ngày sinh không đọc rõ nên QA đọc là khoảng 16 tuổi tại ngày nhận 18/10/2026, và hộp thoại vẫn hiển thị số EA của con này. Cần BA nói chặn từ 16 tuổi hay từ 17 tuổi, và đơn của con 16 tuổi đã đóng EA áp dụng vào đâu. | C16, VR-F5-04 |
| O2 | Lời nhắc One application is one student | Hình Upload scans ghi One application is one student. Add all pages of the signed form and its attachments. Phụ đề danh sách ghi One form is one student. FS 2 bước 5, BR1, T10 và hình Review application cho một mẫu có nhiều con, mỗi con một đơn. Cần thống nhất mỗi lần tải là một mẫu gia đình hay một con, và giới hạn 5 file tính cho mẫu hay cho từng con. | B1, B4, A (phụ đề), E6 |
| O3 | NRIC người khai không tra ra | FS 2 bước 2 chỉ mô tả trường hợp khớp. Không nói khi hồ sơ phụ huynh hoặc dữ liệu Chính phủ không có NRIC: các trường C6 đến C14 để trống và nhập tay được, hoặc bị chặn, và thông báo là gì. | C5 đến C14 |
| O4 | Trường nào khóa, trường nào sửa được | FS 5 Part 1 nói tên, ngày sinh, giới tính, category, nationality, điện thoại, email, địa chỉ được điền và khóa. Hình Review application cho ô Phone number màu vàng và trông sửa được, trong khi FS còn có quy tắc chữ số tối đa 10 cho ô này. Cần BA nói trường nào khóa hẳn, trường nào sửa được khi dữ liệu hồ sơ sai hoặc cũ. | C12, C13, C14 |
| O5 | Định dạng số điện thoại | FS: chỉ chữ số, tối đa 10, thông báo Phone number (up to 10 digits). Hình hiển thị +65 9123 4567, có dấu cộng và khoảng trắng, tương ứng 10 chữ số kể cả mã nước 65. Cần BA nói có nhận mã nước 65 không, số chữ số tối thiểu, và có tự bỏ dấu cộng, khoảng trắng không. | C12 |
| O6 | Định dạng và chữ cái kiểm tra của NRIC/FIN | FS không nêu định dạng. QA đề xuất cấu trúc S, T, F, G, 7 chữ số, 1 chữ cái. Ba NRIC đọc rõ trong hình là S7612345A, T1412345B, T1012345A đều không đạt thuật toán kiểm tra công khai ở Phụ lục A, chữ cái cuối đúng là D, D, Z. Nếu máy chủ kiểm tra chữ cái cuối thì dữ liệu mẫu của FS bị chặn. Cần BA chọn chỉ kiểm cấu trúc hay cả chữ cái cuối, và có nhận chữ cái đầu M của FIN mới không. | C5, C16, C19 |
| O7 | Nhãn Nationality | FS 5 Part 1 đặt nhãn Nationality với giá trị Chinese, Malay, Indian, Eurasian, Others. Đây là nhóm dân tộc. Quốc tịch và tình trạng cư trú nằm ở Category. Cần BA xác nhận nhãn và danh sách giá trị. | C10 |
| O8 | Grade ngoài danh sách | Level suy ra từ P1 đến P6, S1 đến S5, PU1 đến PU3. FS không nói Level hiển thị gì khi Grade nằm ngoài các giá trị này. | C17 |
| O9 | Con học trường khác | FS 1.2 nói School user chỉ thấy và nhập đơn của học sinh đang học tại trường của mình. FS 6 và BR2 chỉ cần ít nhất một con học tại trường, BR8 gửi SBFAS cho trường của con. Cần BA nói đơn của con học trường khác có được tạo không, ai xem, và suy luận từ BR8 là trường của con đó quyết định SBFAS. | C16, E6 |
| O10 | Số con, số thành viên và xóa dòng | Có nút Add child và Add member. FS không nêu số tối đa, cũng không có nút xóa một dòng đã thêm. | C18, C19, C20 |
| O11 | Gender của thành viên | Part 3 chỉ ghi cột Gender, hình hiển thị F. Cần BA nói danh sách giá trị có giống Part 1 là Male, Female, Other không. | C19 |
| O12 | Cách tính thu nhập | FS: thu nhập lấy từ dữ liệu Chính phủ cho người khai và từng thành viên. Chưa rõ thu nhập của con có tính không, GHI là tổng thu nhập hằng tháng, thành viên không có dữ liệu thu nhập tính 0 hay chặn nộp, và làm tròn PCI thế nào. Hình 4,300.00 chia 4 chẵn, giống điểm mở O10 của R4. | C20, E3 |
| O13 | Bản nháp | Chưa rõ: Save draft có kiểm tra định dạng không, ví dụ Context quá 2000 ký tự. Nhiều người của trường cùng mở một Draft thì sao, BR6 lưu theo trường. Discard và Delete có hộp thoại xác nhận không. Bộ lọc Uploaded có ẩn Draft cũ không. Draft có hết hạn không. Draft của một con mà người khác đã nộp đơn cho con đó. | A6, A8, C1, C2 |
| O14 | Thông báo lỗi định dạng | FS chỉ định nghĩa thông báo ở mục 4 và mục 6. Các thông báo định dạng và độ dài trong tài liệu này, ví dụ Enter a valid NRIC/FIN., là Đề xuất QA. | Mục 10 |
| O15 | Date signed và Date received | FS không có giới hạn dưới cho Date signed và không nói Date signed có được sau Date received không. Date received đổi ngày khi tiếp tục Draft hôm sau hay giữ ngày cũ. | C25, C26 |
| O16 | Thế nào là form đang mở | FS 6 nói ngoài khoảng Form opens đến Form closes của MOEFAS và SBFAS của trường. Chưa rõ hai đầu khoảng có tính là mở không, con không đủ điều kiện MOEFAS về quốc tịch chỉ xét form SBFAS (suy luận từ BR8 và BR9), một con có form mở và một con form đóng thì chặn cả mẫu hay chỉ con đó, và ngày so sánh theo giờ Singapore. | VR-F5-07 |
| O17 | Hiển thị ghi chú chặn và cảnh báo sai lệch tên | Hình D cho hai ghi chú cùng lúc. FS không nói thứ tự, có cuộn lên đầu trang, có đánh dấu ô lỗi. Cảnh báo sai lệch tên của con: FS không nêu nội dung và vị trí. | VR-F5-09, C17 |
| O18 | Nộp nhiều con | Nếu lúc Confirm một con vừa có đơn hoặc form vừa đóng, tạo đơn cho các con còn lại hay không tạo gì. QA đề xuất tất cả hoặc không có đơn nào. | VR-F5-10, E6 |
| O19 | Sau khi nộp | FS không nói màn hình sau toast, scan được gắn thế nào cho đơn của từng con, và có gửi thư cho phụ huynh khi nộp không. | E6 |
| O20 | School-based FAS là No và con không đủ điều kiện MOEFAS về quốc tịch | BR8: không đủ điều kiện về quốc tịch thì SBFAS ngay lúc nộp. BR8 cũng nói SBFAS chỉ khi Also consider SBFAS là Yes, không thì Rejected. Với No và con không đủ điều kiện về quốc tịch, kết quả là SBFAS hay Rejected. | C15, E6 |
| O21 | Sửa đơn Pending | FS 8 liệt kê các nội dung được cập nhật. Chưa rõ con và NRIC của con có sửa được không, thu nhập có tra lại khi đổi NRIC thành viên không, đơn đổi trạng thái trong lúc sửa thì sao, và với MOEFAS Pending chờ đóng form thì xếp hạng dùng dữ liệu lúc đóng form hay lúc nộp. | F1, F4 |
| O22 | Thẻ thống kê và bộ lọc | Hình có PENDING 1, MOEFAS 1, SBFAS 2 trong khi danh sách Last 7 days có 1 Draft, 1 Pending, 1 Approved SBFAS. Chưa rõ thẻ có theo Uploaded và Search không, thẻ đồng bộ với bộ lọc Status thế nào, và Draft có được đếm không. | A2, A4 |
| O23 | Nút trên dòng Draft | FS 3 mục 6 có Continue và Delete. Hình không hiển thị hai nút này. Dòng Draft trong hình chỉ có một tên học sinh trong khi mẫu có thể có nhiều con. | A8 |
| O24 | Phân trang và thứ tự | Hình có dòng chân bảng Showing 1 to 3 of 3, chữ mờ. FS không nêu kích thước trang, thứ tự các dòng đã nộp và sắp xếp cột. | A7 |
| O25 | Hộp thoại Review before submitting | Hình không hiển thị địa chỉ người khai. Chưa rõ số EA hiển thị thế nào khi con chưa có EA, và Context trống thì phần Part 4 hiển thị thế nào. | E1, E2, E4 |
| O26 | Quy tắc file | FS chỉ nhận PDF, JPG, PNG. Chưa rõ phần mở rộng jpeg có nhận không, 10 MB là 10 x 1024 x 1024 byte hay 10 triệu byte, và file trùng tên. | B1 |
| O27 | Đọc scan và khung xem | FS không nói khi file đọc không được, mã hóa mật khẩu, hỏng, trắng, sai mẫu đơn, hết thời gian. Cũng không nói đóng hộp thoại khi đang đọc, xem nhiều trang, ô vàng mất khi người dùng sửa, và trình đọc nhận ô Declaration và chữ ký đã đánh dấu thì có tô sẵn không. | B1, B4, C4, C22 |
| O28 | Giới hạn độ dài và tìm kiếm là đề xuất | Search 100 ký tự và kích hoạt sau 300 ms, Address 255, Full name 100, email 254 và 64 là Đề xuất QA, theo cách R4 xử lý ô tìm kiếm và Comment. | A3, C13, C14, C19 |


# 12. Phụ lục


## Phụ lục A. Chữ cái kiểm tra NRIC/FIN, Đề xuất QA


Thuật toán công khai, dùng khi BA chọn kiểm tra chữ cái cuối ở điểm mở O6. Nhân 7 chữ số với trọng số 2, 7, 6, 5, 4, 3, 2 rồi cộng lại. Chữ cái đầu T hoặc G thì cộng thêm 4. Lấy tổng chia 11 lấy số dư. Với S và T, chữ cái cuối là ký tự ở vị trí số dư (đếm từ 0) trong chuỗi JZIHGFEDCBA. Với F và G, trong chuỗi XWUTRQPNMLK. FIN bắt đầu bằng M không nằm trong phạm vi này.

| NRIC trong hình FS | Tổng sau cộng | Số dư | Chữ cái đúng | Chữ cái trong hình | Kết quả |
| :--- | :--- | :--- | :--- | :--- | :--- |
| S7612345A | 106 | 7 | D | A | Không đạt |
| T1412345B | 84 | 7 | D | B | Không đạt |
| T1012345A | 56 | 1 | Z | A | Không đạt |


## Phụ lục B. Kịch bản của FS ứng với quy tắc


| Kịch bản FS | Nội dung | Quy tắc trong tài liệu này |
| :--- | :--- | :--- |
| T1 | Tải file .docx | B1 |
| T2 | Nhập NRIC của người khai | C5 đến C14 |
| T3 | Nhập NRIC của con | C16, C17 |
| T4 | NRIC của con không có trong hồ sơ MOE | VR-F5-03 |
| T5 | Con 17 tuổi | VR-F5-04, điểm mở O1 |
| T6 | Không con nào của trường người dùng | VR-F5-06 |
| T7 | Thành viên trùng NRIC với người khai | VR-F5-08, C19 |
| T8 | Chưa kiểm tra chữ ký | VR-F5-01, C23 |
| T9 | Save draft rồi Continue | C2, A8, VR-F5-S08 |
| T10 | Mẫu 2 con, Confirm and submit | E6, VR-F5-S05, VR-F5-S11 |
| T11 | Có nhập context | C21, E4 |
| T12 | Sửa đơn Pending | F1 đến F5, VR-F5-S12 |
| T13 | Nộp khi không có form FAS mở | VR-F5-07 |


| Quy tắc FS | Nội dung rút gọn | Quy tắc trong tài liệu này |
| :--- | :--- | :--- |
| BR1 | Một mẫu, một gia đình, một đơn mỗi con | E6, VR-F5-S05 |
| BR2 | Con có trong MOE, 7 đến 16 tuổi, chưa có đơn, ít nhất một con của trường | VR-F5-02 đến VR-F5-06, VR-F5-S04 |
| BR3 | Thông tin từ hồ sơ khi NRIC khớp, không sửa được | C5, C6 đến C10, C16, C17, VR-F5-S03 |
| BR4 | Thu nhập từ dữ liệu Chính phủ, NRIC khác nhau | C19, C20, VR-F5-08 |
| BR5 | Context tùy chọn, văn bản thuần, tối đa 2000 ký tự | C21 |
| BR6 | Bản nháp lưu theo trường, xóa khi nộp, Discard, Delete | C1, C2, A8, VR-F5-S08 |
| BR7 | Nộp luôn qua Review before submitting | C3, E6 |
| BR8 | Phân luồng sau khi nộp theo F4 | C15, E6, VR-F5-S11 |
| BR9 | Chỉ nộp khi form mở, vẫn sửa được đơn Pending sau khi đóng | VR-F5-07, F1, VR-F5-S12 |


## Phụ lục C. Hình của FS ứng với tài liệu này


| Hình trong tài liệu | Hình trong FS | Màn |
| :--- | :--- | :--- |
| Hình A | Upload applications, một dòng Draft | A |
| Hình B | Upload scans | B |
| Hình C | Review application, bản scan bên trái, Part 1 đến 5 bên phải | C |
| Hình D | Bị chặn khi nộp, thiếu trường bắt buộc và form đã đóng | D |
| Hình E | Review before submitting | E |
| Không có hình | Xem và sửa đơn đã nộp | F |
