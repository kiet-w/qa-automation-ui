# Traceability Matrix - US-03 Curricula Trainer Account

Bảng đối chiếu giữa **Acceptance Criteria (AC.md)** và **Hành vi thực tế của hệ thống (curricula_trainer_account.html)**.
Được sử dụng làm căn cứ duy nhất để triển khai test suite và lựa chọn chính xác hàm Exceptor (`expect_success`, `expect_rejection`, `expect_bug_if_rejected`, `expect_bug_if_accepted`).

---

| AC ref | Test case ID (dự kiến) | Input / Điều kiện | Hành vi thực tế của hệ thống | Khớp AC? | Nhãn Exceptor áp dụng |
|:---|:---|:---|:---|:---:|:---|
| **AC-01** | TC01, TC28 | Preferred Name hợp lệ, độ dài tối đa 255 ký tự | Hệ thống chấp nhận giá trị hợp lệ và cho phép submit khi các trường khác thỏa mãn | ✅ Khớp | `expect_success` |
| **AC-01** | TC29 | Preferred Name chứa ký tự Unicode tiếng Việt có dấu ("Nguyễn Đặng Hoàng Ánh") | Hệ thống lưu giữ nguyên vẹn chuỗi tiếng Việt có dấu, không bị méo font/lỗi mã hóa | ✅ Khớp | `expect_success` |
| **AC-01** | TC08, TC09 | Để trống trường Preferred Name rồi nhấn Save | Hệ thống hiển thị thông báo lỗi "This field is required." tại `preferredName` | ✅ Khớp | `expect_rejection` |
| **AC-02** | TC01 | Chọn giới tính "Male" hoặc "Female" | Hệ thống ghi nhận lựa chọn radio button, không báo lỗi | ✅ Khớp | `expect_success` |
| **AC-02** | TC08, TC09 | Không chọn bất kỳ giới tính nào rồi nhấn Save | Hệ thống hiển thị lỗi "This field is required." tại `gender` | ✅ Khớp | `expect_rejection` |
| **AC-03** | TC01 | Chọn ID Type từ danh sách ("NRIC", "FIN", "EP", "S-Pass", "Passport") | Hệ thống ghi nhận giá trị đã chọn hợp lệ | ✅ Khớp | `expect_success` |
| **AC-03** | TC08, TC09 | Để trống dropdown ID Type rồi nhấn Save | Hệ thống hiển thị lỗi "This field is required." tại `idType` | ✅ Khớp | `expect_rejection` |
| **AC-04** | TC01 | Nhập ID Number hợp lệ (ví dụ: "S1234567A") | Hệ thống chấp nhận ID Number | ✅ Khớp | `expect_success` |
| **AC-04** | TC08, TC09 | Để trống trường ID Number rồi nhấn Save | Hệ thống hiển thị lỗi "This field is required." tại `idNumber` | ✅ Khớp | `expect_rejection` |
| **AC-05** | TC01, TC02 | Đính kèm file ID hợp lệ (.png, .pdf, .jpg <= 10MB) | Hệ thống chấp nhận file đính kèm, không báo lỗi | ✅ Khớp | `expect_success` |
| **AC-05** | TC08 | Không đính kèm bất kỳ file ID nào rồi nhấn Save | Hệ thống hiển thị lỗi "Please upload a valid document." tại `idDocument` | ✅ Khớp | `expect_rejection` |
| **AC-05** | TC20, UP05 | Đính kèm file sai định dạng hoặc độc hại (.txt, .exe) | Hệ thống chặn submit, hiển thị lỗi "Please upload a valid document." tại `idDocument` | ✅ Khớp | `expect_rejection` |
| **AC-06** | TC01 | Chọn Quốc tịch hợp lệ từ dropdown (ví dụ: "Singaporean", "Vietnamese") | Hệ thống ghi nhận quốc tịch đã chọn | ✅ Khớp | `expect_success` |
| **AC-06** | TC08 | Để trống dropdown Quốc tịch rồi nhấn Save | Hệ thống hiển thị lỗi "This field is required." tại `nationality` | ✅ Khớp | `expect_rejection` |
| **AC-07** | TC01 | Nhập Ngày sinh trong quá khứ (ví dụ: "1992-08-15") | Hệ thống chấp nhận ngày sinh hợp lệ | ✅ Khớp | `expect_success` |
| **AC-07** | TC08 | Để trống trường Ngày sinh rồi nhấn Save | Hệ thống hiển thị lỗi "Enter a valid date of birth." tại `dob` | ✅ Khớp | `expect_rejection` |
| **AC-07** | TC10, UP02 | Nhập Ngày sinh trong tương lai (ví dụ: năm sau) rồi nhấn Save | Hệ thống phát hiện ngày tương lai, hiển thị lỗi "Enter a valid date of birth." tại `dob` | ✅ Khớp | `expect_rejection` |
| **AC-08** | TC01 | Chọn Sắc tộc hợp lệ từ dropdown (ví dụ: "Chinese", "Malay") | Hệ thống ghi nhận sắc tộc đã chọn | ✅ Khớp | `expect_success` |
| **AC-08** | TC08 | Để trống dropdown Sắc tộc rồi nhấn Save | Hệ thống hiển thị lỗi "This field is required." tại `race` | ✅ Khớp | `expect_rejection` |
| **AC-09** | TC01 | Chọn Quốc gia sinh hợp lệ từ dropdown (ví dụ: "Singapore", "Vietnam") | Hệ thống ghi nhận nơi sinh đã chọn | ✅ Khớp | `expect_success` |
| **AC-09** | TC08 | Để trống dropdown Nơi sinh rồi nhấn Save | Hệ thống hiển thị lỗi "This field is required." tại `birthCountry` | ✅ Khớp | `expect_rejection` |
| **AC-10** | TC01 | Chọn trạng thái đối tượng nộp thuế ("Yes" hoặc "No") | Hệ thống ghi nhận lựa chọn, không báo lỗi | ✅ Khớp | `expect_success` |
| **AC-10** | TC08 | Không chọn tình trạng nộp thuế rồi nhấn Save | Hệ thống hiển thị lỗi "This field is required." tại `taxResident` | ✅ Khớp | `expect_rejection` |
| **AC-11** | TC01, TC30 | Nhập email hợp lệ chuẩn RFC (độ dài <= 100 ký tự) | Hệ thống chấp nhận email hợp lệ | ✅ Khớp | `expect_success` |
| **AC-11** | TC08 | Để trống trường Email rồi nhấn Save | Hệ thống hiển thị lỗi "Enter a valid email address." tại `primaryEmail` | ✅ Khớp | `expect_rejection` |
| **AC-11** | TC11, UP03 | Nhập email sai định dạng (thiếu @, thiếu domain, có khoảng trắng) | Hệ thống hiển thị lỗi "Enter a valid email address." tại `primaryEmail` | ✅ Khớp | `expect_rejection` |
| **AC-12** | TC01 | Nhập số điện thoại Singapore (+65) gồm 8 chữ số bắt đầu bằng 8 hoặc 9 (ví dụ: "91234567") | Hệ thống chấp nhận số điện thoại hợp lệ | ✅ Khớp | `expect_success` |
| **AC-12** | TC12, UP04 | Nhập số điện thoại Singapore (+65) có độ dài không đủ 8 chữ số (ví dụ: "123456") | Hệ thống chặn submit, hiển thị lỗi "Enter a valid contact number." tại `primaryPhone` | ✅ Khớp | `expect_rejection` |
| **AC-12** | TC12 | Nhập số điện thoại Singapore (+65) chứa chữ cái hoặc ký tự đặc biệt (ví dụ: "9123abcd") | Hệ thống chặn submit, hiển thị lỗi "Enter a valid contact number." tại `primaryPhone` | ✅ Khớp | `expect_rejection` |
| **AC-12** | TC12_BUG | Nhập số điện thoại Singapore (+65) 8 chữ số nhưng bắt đầu bằng đầu số không hợp lệ (ví dụ: "12345678", "23456789") | Hệ thống chỉ kiểm tra `value.length === 8` và chấp nhận submit thành công. *(Lý do không khớp: Hệ thống thiếu kiểm tra đầu số 8 hoặc 9 theo AC-12, dẫn đến lỗ hổng validate)* | ❌ Không khớp | `expect_bug_if_accepted` |
| **AC-12** | TC03, TC13 | Nhập số điện thoại quốc tế (+84) từ 8-15 chữ số hợp lệ | Hệ thống chấp nhận số điện thoại quốc tế hợp lệ | ✅ Khớp | `expect_success` |
| **AC-12** | TC13 | Nhập số điện thoại quốc tế (+84) dưới 8 chữ số hoặc trên 15 chữ số | Hệ thống hiển thị lỗi "Enter a valid contact number." tại `primaryPhone` | ✅ Khớp | `expect_rejection` |
| **AC-13** | TC01 | Để trống trường Secondary Phone rồi nhấn Save | Hệ thống không báo lỗi tại `secondaryPhone` (trường là tùy chọn) | ✅ Khớp | `expect_success` |
| **AC-13** | TC14 | Nhập Secondary Phone sai định dạng (ví dụ: +65 nhưng chỉ 3 chữ số) | Hệ thống kích hoạt kiểm tra định dạng và hiển thị lỗi tại `secondaryPhone` | ✅ Khớp | `expect_rejection` |
| **AC-14** | TC01 | Nhập Tên người liên hệ khẩn cấp hợp lệ | Hệ thống chấp nhận giá trị hợp lệ | ✅ Khớp | `expect_success` |
| **AC-14** | TC08, TC15 | Để trống Tên người liên hệ khẩn cấp rồi nhấn Save | Hệ thống hiển thị lỗi "This field is required." tại `emergencyName` | ✅ Khớp | `expect_rejection` |
| **AC-15** | TC01 | Chọn Mối quan hệ khẩn cấp từ dropdown | Hệ thống ghi nhận lựa chọn hợp lệ | ✅ Khớp | `expect_success` |
| **AC-15** | TC08, TC15 | Để trống dropdown Mối quan hệ khẩn cấp rồi nhấn Save | Hệ thống hiển thị lỗi "This field is required." tại `emergencyRelationship` | ✅ Khớp | `expect_rejection` |
| **AC-16** | TC01 | Nhập Số điện thoại khẩn cấp hợp lệ | Hệ thống chấp nhận giá trị hợp lệ | ✅ Khớp | `expect_success` |
| **AC-16** | TC08, TC15 | Để trống hoặc nhập sai định dạng Số điện thoại khẩn cấp | Hệ thống hiển thị lỗi tương ứng tại `emergencyPhone` | ✅ Khớp | `expect_rejection` |
| **AC-17** | TC21 | Chuyển đổi Residential Type sang "Non-Singapore" | Hệ thống tự động ẩn khối địa chỉ SG, hiển thị khối quốc tế và mở dropdown Country | ✅ Khớp | `expect_success` |
| **AC-17** | TC22 | Chuyển đổi Residential Type trở lại "Singapore" | Hệ thống khôi phục các ô địa chỉ SG và khóa Country dropdown về "Singapore" | ✅ Khớp | `expect_success` |
| **AC-18** | TC01 | Nhập Postal Code 6 chữ số hợp lệ của Singapore (ví dụ: "120047") | Hệ thống chấp nhận mã bưu chính | ✅ Khớp | `expect_success` |
| **AC-18** | TC16 | Nhập Postal Code Singapore sai quy cách (chứa chữ, hoặc khác 6 chữ số) | Hệ thống hiển thị lỗi "Enter a valid postal code." tại `postalCode` | ✅ Khớp | `expect_rejection` |
| **AC-18** | TC05-07 | Nhập Postal Code Singapore đã có trong dữ liệu (120047, 238801, 569933) rồi blur | Hệ thống tự động điền Block Number và Street Name tương ứng | ✅ Khớp | `expect_success` |
| **AC-18** | TC08 | Để trống Block Number hoặc Street Name trong chế độ SG rồi nhấn Save | Hệ thống hiển thị lỗi bắt buộc tại `blockNumber` và `streetName` | ✅ Khớp | `expect_rejection` |
| **AC-18** | TC01 | Nhập Floor và Unit Number dạng số thuần túy (ví dụ: Floor "08", Unit "205") | Hệ thống chấp nhận cụm Floor/Unit | ✅ Khớp | `expect_success` |
| **AC-18** | TC17, UP01 | Nhập Unit Number chứa ký tự chữ và số hợp lệ tại Singapore (ví dụ: "#04-12A", "#B1-02") | Hệ thống chặn submit và hiển thị lỗi "Floor and unit number are required." *(Lý do không khớp: Regex `/^\d{1,9}$/` chỉ cho phép số, từ chối số căn hộ Alphanumeric hợp lệ theo AC-18)* | ❌ Không khớp | `expect_bug_if_rejected` |
| **AC-19** | TC02, TC23 | Tích chọn "Floor/Unit number is not applicable" | Hai ô Floor và Unit bị disabled, giá trị bị xóa trắng và lỗi `floorUnit` bị ẩn | ✅ Khớp | `expect_success` |
| **AC-19** | TC23 | Bỏ tích chọn "Floor/Unit number is not applicable" | Hai ô Floor và Unit được kích hoạt trở lại (enabled) cho phép nhập dữ liệu | ✅ Khớp | `expect_success` |
| **AC-20** | TC03, TC19 | Ở chế độ Non-Singapore, chọn quốc gia và nhập đủ Address 1, City | Hệ thống chấp nhận thông tin địa chỉ quốc tế hợp lệ | ✅ Khớp | `expect_success` |
| **AC-20** | TC18 | Ở chế độ Non-Singapore nhưng lại chọn Country là "Singapore" | Hệ thống hiển thị lỗi "This field is required." tại `countryRegion` | ✅ Khớp | `expect_rejection` |
| **AC-20** | TC19 | Ở chế độ Non-Singapore, để trống Address Line 1 hoặc City | Hệ thống hiển thị lỗi bắt buộc tại `address1` và `city` | ✅ Khớp | `expect_rejection` |
| **AC-21** | TC01, TC27 | Điền đầy đủ thông tin hợp lệ và nhấn Save | Hệ thống hiển thị banner `#successBox` có thông báo thành công, Trainer ID dạng `TRN\d{6}` và Status Active, đồng thời cuộn lên đầu trang | ✅ Khớp | `expect_success` |
| **AC-22** | TC08 | Gửi form rỗng hoặc chứa dữ liệu không hợp lệ | Hệ thống chặn submit (`#successBox` không xuất hiện), hiển thị các dòng lỗi màu đỏ và cuộn lên đầu | ✅ Khớp | `expect_rejection` |
| **AC-23** | TC26 | Nhấn "Cancel" khi form chưa có dữ liệu (Clean form) | Trang được reload trực tiếp mà không kích hoạt popup xác nhận | ✅ Khớp | `expect_success` |
| **AC-23** | TC24 | Nhấn "Cancel" khi form đã nhập liệu (Dirty form), sau đó chọn Dismiss | Hộp thoại cảnh báo xuất hiện, chọn Dismiss thì form giữ nguyên dữ liệu đã nhập | ✅ Khớp | `expect_success` |
| **AC-23** | TC25 | Nhấn "Cancel" khi form đã nhập liệu (Dirty form), sau đó chọn Accept | Hộp thoại cảnh báo xuất hiện, chọn Accept thì trang reload và làm sạch form | ✅ Khớp | `expect_success` |
| **AC-24** | TC31 | Nhập chuỗi Script Injection (`<script>window._xss_executed=true;</script>`) vào Preferred Name và lưu | Dữ liệu được xử lý an toàn dưới dạng chuỗi thuần túy (escaped), biến `_xss_executed` không bị kích hoạt | ✅ Khớp | `expect_success` |
| **AC-25** | TC32 | Nhập chuỗi SQL Injection (`admin' OR '1'='1' --`) vào ID Number | Hệ thống giữ nguyên chuỗi an toàn, không gây crash ứng dụng hay lỗi cú pháp | ✅ Khớp | `expect_success` |
