# Acceptance Criteria - US-03 Curricula Trainer Account

Tài liệu này là nguồn tham chiếu cố định (Source of Truth) về các tiêu chí chấp nhận và yêu cầu nghiệp vụ cho tính năng **Create Trainer Account (Curricula)**. Mọi test case và đánh giá kỳ vọng nghiệp vụ (Exceptor) phải căn cứ trực tiếp vào các mã AC dưới đây.

---

## 1. Thông tin cá nhân (Personal Information)

- **AC-01 (Preferred Name)**: Trường bắt buộc nhập. Độ dài tối đa 255 ký tự. Hỗ trợ đầy đủ ký tự chữ cái, số, khoảng trắng và ký tự Unicode đa ngôn ngữ (tiếng Việt có dấu).
- **AC-02 (Gender)**: Trường bắt buộc. Người dùng phải chọn một trong hai giá trị radio button: "Male" hoặc "Female".
- **AC-03 (ID Type)**: Trường bắt buộc. Người dùng phải chọn một loại giấy tờ từ danh sách: "NRIC", "FIN", "EP", "S-Pass", "Passport".
- **AC-04 (ID Number)**: Trường bắt buộc. Độ dài tối đa 255 ký tự. Hỗ trợ định dạng giấy tờ tùy thân hợp lệ tương ứng với loại ID Type đã chọn.
- **AC-05 (ID Document Upload)**: Trường bắt buộc đính kèm tệp.
  - Chỉ chấp nhận các định dạng tệp: JPG, JPEG, PNG, PDF.
  - Dung lượng tệp tối đa không vượt quá 10MB.
  - Bắt buộc chặn các tệp thực thi độc hại hoặc không đúng định dạng (ví dụ: `.exe`, `.bat`, `.txt`, `.sh`).
- **AC-06 (Nationality)**: Trường bắt buộc. Người dùng phải chọn quốc tịch từ danh sách: "Singaporean", "Chinese", "Malaysian", "Indian", "Indonesian", "Filipino", "Vietnamese", "Others".
- **AC-07 (Date of Birth)**: Trường bắt buộc. Định dạng ngày hợp lệ (YYYY-MM-DD). Ngày sinh phải nhỏ hơn hoặc bằng ngày hiện tại (không được chọn ngày trong tương lai).
- **AC-08 (Race)**: Trường bắt buộc. Người dùng phải chọn sắc tộc từ danh sách: "Chinese", "Malay", "Indian", "Others".
- **AC-09 (Country/Region of Birth)**: Trường bắt buộc. Người dùng phải chọn quốc gia/vùng lãnh thổ nơi sinh từ danh sách định sẵn.
- **AC-10 (Singapore Tax Resident Status)**: Trường bắt buộc. Người dùng phải chọn một trong hai giá trị radio button: "Yes" hoặc "No".

---

## 2. Thông tin liên hệ (Contact Information)

- **AC-11 (Primary Email Address)**: Trường bắt buộc. Độ dài tối đa 100 ký tự. Bắt buộc tuân thủ định dạng email chuẩn quốc tế (`prefix@domain.tld`). Không chấp nhận chuỗi thiếu `@`, thiếu tên miền, hoặc chứa khoảng trắng.
- **AC-12 (Primary Contact Number)**: Trường bắt buộc nhập số điện thoại chính:
  - Nếu chọn mã vùng Singapore (`+65`): Bắt buộc gồm đúng 8 chữ số và phải bắt đầu bằng chữ số `8` hoặc `9` (quy tắc viễn thông Singapore).
  - Nếu chọn mã vùng quốc tế khác (`+60`, `+84`, `+86`, `+91`): Bắt buộc chỉ chứa chữ số, độ dài từ 8 đến 15 ký tự.
- **AC-13 (Secondary Contact Number)**: Trường liên hệ phụ (không bắt buộc / optional):
  - Nếu để trống: Hệ thống không báo lỗi.
  - Nếu có nhập dữ liệu: Bắt buộc tuân thủ quy tắc kiểm tra định dạng tương ứng với mã vùng đã chọn như AC-12.

---

## 3. Thông tin liên hệ khẩn cấp (Emergency Contact Information)

- **AC-14 (Emergency Contact Name)**: Trường bắt buộc. Nhập tên người liên hệ khẩn cấp, độ dài tối đa 255 ký tự.
- **AC-15 (Emergency Contact Relationship)**: Trường bắt buộc. Người dùng phải chọn mối quan hệ từ danh sách: "Father", "Mother", "Spouse", "Sibling", "Relative", "Friend", "Others".
- **AC-16 (Emergency Contact Number)**: Trường bắt buộc. Bắt buộc chọn mã quốc gia và nhập số điện thoại hợp lệ theo quy tắc kiểm tra số điện thoại (tương tự AC-12).

---

## 4. Địa chỉ cư trú (Residential Address)

- **AC-17 (Residential Type Selection)**: Cho phép chuyển đổi giữa hai chế độ cư trú: "Singapore" (mặc định) và "Non-Singapore".
- **AC-18 (Singapore Residential Address)**:
  - Trường Country/Region bị cố định giá trị là "Singapore" và bị vô hiệu hóa (disabled).
  - Trường Postal code là bắt buộc, phải gồm đúng 6 chữ số (`^\d{6}$`).
  - Hệ thống hỗ trợ cơ chế tự động điền (auto-population) Block Number và Street Name khi người dùng nhập Postal Code hợp lệ đã có trong cơ sở dữ liệu bưu chính (sau sự kiện blur).
  - Block/Building Number và Street Name là các trường bắt buộc nhập.
  - Building Name là trường tùy chọn (optional).
  - Floor Number (độ dài 1-5 ký tự) và Unit Number (độ dài 1-9 ký tự) là bắt buộc.
  - **Quy chuẩn địa chỉ Singapore**: Số phòng/căn hộ (Unit Number) tại Singapore chấp nhận cả chữ và số (Alphanumeric, ví dụ: `#04-12A`, `#B1-02`, `#10-A1`).
- **AC-19 (Floor/Unit Not Applicable Toggle)**:
  - Khi người dùng tích chọn checkbox "Floor/Unit number is not applicable", cả hai ô Floor Number và Unit Number phải bị vô hiệu hóa (disabled), xóa sạch dữ liệu hiện có và ẩn mọi thông báo lỗi của cụm trường này.
  - Khi bỏ tích chọn checkbox, hai trường này phải được mở khóa (enabled) trở lại để người dùng nhập liệu.
- **AC-20 (Non-Singapore Residential Address)**:
  - Khi chuyển sang chế độ "Non-Singapore", hệ thống ẩn các trường địa chỉ đặc thù của Singapore (Block, Building Name, Street, Floor/Unit).
  - Mở khóa dropdown Country/Region cho phép người dùng chọn quốc gia cư trú nước ngoài (không được chọn "Singapore").
  - Hiển thị các trường địa chỉ quốc tế: Address Line 1 (bắt buộc), Address Line 2 (tùy chọn), City (bắt buộc), State/Province (tùy chọn).
  - Trường Postal Code không còn bắt buộc (optional).

---

## 5. Thao tác trên Form & Phản hồi hệ thống (Actions & Feedback)

- **AC-21 (Account Creation Submission & Success Indicator)**:
  - Khi tất cả dữ liệu hợp lệ, nhấn nút "Save" phải tạo tài khoản thành công.
  - Hệ thống hiển thị hộp thông báo màu xanh (`#successBox`) bao gồm:
    - Lời chúc mừng: "Trainer account has been created successfully."
    - Mã định danh Trainer ID sinh ngẫu nhiên theo định dạng chuẩn `TRN` kèm 6 chữ số (ví dụ: `TRN123456`).
    - Trạng thái: "Status: Active".
  - Trang phải tự động cuộn mượt lên trên cùng (scroll to top) để người dùng xem kết quả.
- **AC-22 (Validation Feedback on Empty / Invalid Form)**:
  - Khi gửi form để trống hoặc có dữ liệu không hợp lệ, hệ thống phải chặn tiến trình submit (`successBox` ẩn).
  - Hiển thị thông báo lỗi màu đỏ ngay dưới từng trường dữ liệu không đạt yêu cầu.
  - Viền của ô nhập liệu vi phạm chuyển sang màu đỏ cảnh báo.
  - Trang tự động cuộn lên đầu để hướng dẫn người dùng chỉnh sửa.
- **AC-23 (Cancel Button Navigation & Confirmation)**:
  - Khi form đang sạch (Clean form - chưa nhập liệu): Nhấn "Cancel" sẽ tải lại trang ngay lập tức mà không hiển thị hộp thoại xác nhận.
  - Khi form đã có dữ liệu (Dirty form - người dùng đã nhập ít nhất 1 trường hoặc đính kèm tệp): Nhấn "Cancel" bắt buộc kích hoạt Browser Confirm Dialog với thông điệp: "You have unsaved changes. Are you sure you want to leave this page?".
    - Nếu chọn "Dismiss" (Hủy): Hộp thoại đóng lại, giữ nguyên toàn bộ dữ liệu trên form.
    - Nếu chọn "Accept" (Đồng ý): Tải lại trang và làm mới sạch sẽ form về trạng thái ban đầu.

---

## 6. Bảo mật & Khả năng chống chịu dữ liệu (Security & Resilience)

- **AC-24 (XSS Injection Resilience)**:
  - Các trường nhập liệu văn bản (Preferred Name, Address...) phải xử lý an toàn chuỗi mã độc Cross-Site Scripting (ví dụ: `<script>window._xss_executed=true;</script>`).
  - Hệ thống phải lưu trữ và hiển thị nội dung dạng text thuần túy (HTML-escaped), tuyệt đối không thực thi JavaScript trên trình duyệt.
- **AC-25 (SQL Injection & Special Characters Resilience)**:
  - Hệ thống phải chấp nhận và lưu trữ an toàn các chuỗi ký tự đặc biệt, dấu nháy đơn, nháy kép, payload SQL Injection (ví dụ: `admin' OR '1'='1' --`) mà không gây sập giao diện hay lỗi xử lý dữ liệu.
