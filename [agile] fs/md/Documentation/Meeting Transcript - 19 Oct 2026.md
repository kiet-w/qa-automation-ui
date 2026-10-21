# Meeting Transcript - 19 Oct 2026


# MEETING TRANSCRIPT


Meeting: Agile Project, Monday 19 Oct 2026, 1:00 PM – 1:30 PM, via Teams

## Transcript


Người nói 1: Đối với chức năng nạp tiền (top-up), yêu cầu liên quan đến việc cấu hình phí. Người dùng cấp trường (school user) hoặc người dùng quản trị (admin user) có thể tự định nghĩa các loại phí và thành phần phí theo hai cấp độ. Quản trị viên (người dùng MOE HQ) có thể cấu hình các loại phí và thành phần phí áp dụng cho toàn bộ trường học trong cả nước. Người dùng cấp trường có thể cấu hình các loại phí và thành phần phí riêng biệt, hoàn toàn độc lập với những gì đã được MOE HQ thiết lập. Chúng tôi cũng đề xuất sử dụng các quy tắc về mức phí, trong đó cùng một thành phần có thể có các mức phí khác nhau tùy thuộc vào cấp học của học sinh và thông tin cư trú.

Tiếp theo là việc công bố phí (fee publication). Khi phí đã được định cấu hình, một người dùng có thẩm quyền có thể tạo bảng công bố phí cho bất kỳ trường học và kỳ lập hóa đơn cụ thể nào. Họ có thể chỉ định những học sinh nào phải nhận khoản phí này (ở bất kỳ cấp độ, lớp học hoặc nhóm cụ thể nào). Sau khi người dùng cấp trường quyết định công bố các khoản phí đó, hệ thống sẽ tạo ra khoản thanh toán cho học sinh. Phụ huynh có thể xem các khoản phí này thông qua cổng dịch vụ điện tử (e-service portal). Chúng tôi cũng đề xuất giữ nguyên số tiền gốc không thay đổi ngay cả khi có bất kỳ khoản hỗ trợ tài chính hay điều chỉnh nào được áp dụng vào tài khoản giáo dục. Đó là phương pháp tổng thể mà chúng tôi dự kiến cho việc quản lý phí. Điều này có phù hợp với mong đợi của bạn không?

Người nói 2: Có.

Người nói 1: Tiếp theo là việc đăng ký chương trình Hỗ trợ Tài chính (FAS). Có hai cách để nộp đơn: qua bản cứng hoặc phụ huynh có thể tạo đơn đăng ký trên cổng dịch vụ điện tử. Sau khi đơn được nộp, hệ thống sẽ truy xuất thông tin của học sinh và các thông tin liên quan đến hộ gia đình. Hệ thống có thể trích xuất thông tin thu nhập thông qua nguồn dữ liệu chính phủ bên ngoài bằng API. Hệ thống sẽ đánh giá đơn dựa trên các tiêu chí như quốc tịch học sinh, thu nhập bình quân đầu người, thu nhập hộ gia đình và áp dụng cho các trường công lập do chính phủ quản lý. Học sinh tại trường tư thục sẽ không thể đăng ký chương trình này. Đó là cách tôi diễn giải, như vậy có ổn không?

Người nói 2: Vâng, ổn. Nhưng bạn có bản thiết kế mẫu (mockup) nào để tôi xem không?

Người nói 1: Hiện tại tôi chỉ đang trình bày quy trình tổng thể. Tôi sẽ hoàn thiện các chức năng này để có một bản demo rõ ràng hơn vào thứ Sáu tới.

Thứ hai là việc đánh giá FAS của Bộ Giáo dục (MOE FAS assessment). Hệ thống sẽ có khả năng đánh giá xem học sinh có đủ điều kiện nhận MOE FAS hay không trước khi chuyển hồ sơ xuống cấp trường. Nếu đủ điều kiện, người dùng MOE HQ sẽ cấu hình một chương trình áp dụng các mức trợ cấp khác nhau cho các cấp học khác nhau (như Tiểu học, Trung học, và Tiền đại học).

Người nói 2: Quy trình đối với cấp học là gì?

Người nói 1: Các cấp học khác nhau sẽ nhận mức trợ cấp khác nhau. Tôi có thể cho bạn xem bảng ma trận trợ cấp ngay tại đây. Nếu việc đánh giá MOE FAS không đạt tiêu chuẩn, hệ thống sẽ chuyển đơn xuống cấp trường. Người dùng cấp trường có thể đánh giá hồ sơ dựa trên bối cảnh hoàn cảnh học sinh thay vì chỉ dựa vào tiêu chí cứng về thu nhập. Kết hợp với đề xuất từ AI, họ sẽ quyết định đơn này có phù hợp với chương trình hỗ trợ nào không.

Người nói 2: Lần sau nếu bạn có thêm các màn hình để tôi xem thì sẽ tốt hơn.

Người nói 1: Tôi có thể cho bạn xem một vài màn hình dự thảo ban đầu (draft prototype) ngay bây giờ, dù chưa hoàn thiện. (Trao đổi về việc hiển thị giao diện OCR để xử lý hồ sơ bản cứng.) Phụ huynh nộp bản cứng, quản trị viên trường sẽ tải bản cứng lên, hệ thống OCR sẽ trích xuất nội dung văn bản. Bạn muốn sử dụng hệ thống OCR hay muốn người dùng tự nhập toàn bộ file?

Người nói 2: Tôi thích phương án OCR hơn.

Người nói 1: Kế tiếp là phần ngân sách (budget). Hệ thống sẽ cảnh báo nếu ngân sách bị vượt quá, nhưng sẽ không có hạn chế cứng (hard restriction) để không chặn quy trình phê duyệt hồ sơ. Về phần mô phỏng (simulation), MOE HQ có thể chạy mô phỏng chế độ chỉ xem (read-only) để hướng dẫn người dùng trường học theo thời gian thực hoặc đại diện họ thực hiện các hành động.

Người nói 2: Liệu chatbot AI có thể truy cập thông tin tài khoản cá nhân của phụ huynh và trả lời các câu hỏi về số dư còn lại hay không?

Người nói 1: Có, AI có thể truy xuất thông tin từ hệ thống để trả lời các câu hỏi dựa trên ngữ cảnh đó.

Người nói 2: (Đề cập đến thời gian áp dụng hiệu lực của chương trình FAS vào tháng 10-11 cho năm học tiếp theo.) Phụ huynh thường nộp đơn cho năm học tới từ tháng 10-11 năm trước, quy trình này không thể đợi đến ngày 1 tháng 1 mới bắt đầu.

Người nói 1: Đồng ý, chúng tôi sẽ điều chỉnh lại thời hạn nộp đơn để có hai chu kỳ hiển thị phù hợp. Đối với AI Machine Learning gợi ý chương trình hỗ trợ, hệ thống sẽ đề xuất dựa trên các tiêu chí để giúp các cấp trường quyết định nếu học sinh bị loại khỏi tiêu chí cứng. Quản trị viên trường vẫn phải kiểm tra lại (manual check) tính chính xác của tài liệu tải lên nếu sử dụng OCR.

Cảm ơn bạn đã đánh giá trong buổi hôm nay. Chúng tôi sẽ mang đến sản phẩm chi tiết hơn trong buổi demo vào giai đoạn tới.

(The meeting ended at 1:30PM)