      **MINUTES OF AGILE PROJECT SPRINT REVIEW MEETING**

**16 OCT (FRIDAY) AT 2:05 PM VIA TEAMS**

**Reference Document:**

| Meeting’s Transcript | [Transcript](https://docs.google.com/document/d/1RwS1SpU2ijyZeWdEQtNsEGvtceFMAAM6/edit?usp=sharing&ouid=110638749521986844672&rtpof=true&sd=true)  |
| :---- | :---- |

**Agenda**

| S/N | Agenda | Action By |
| :---- | :---- | ----- |
| **1** | **Tổng quan và phạm vi demo Sprint 1**  |  |
|  | Nhóm giới thiệu hai portal: Admin Portal dành cho MOE HQ và School User; e-Service Portal dành cho phụ huynh. MOE HQ quản lý school, level, class và student; School User cấu hình các lớp trường cung cấp, đăng ký học sinh và quản lý enrolment. Phụ huynh có thể xem Education Account, kiểm tra phí, cập nhật profile và thanh toán. Sprint tập trung demo các chức năng được nêu là Functions 1, 3, 8 và 9; số thứ tự/chức năng tương ứng cần được xác nhận.  | **For Info** |
| **2** | **Education Account (EA) và đồng bộ dữ liệu**  |  |
|  | Hệ thống được demo với chức năng tự động đồng bộ dữ liệu học sinh Singapore trong độ tuổi 7–16 và chức năng manual sync để MOE lấy dữ liệu mới ngay khi cần.  Phần trao đổi cho thấy initial/bootstrap sync có thể lấy dữ liệu nhóm tuổi 7–16, còn các lần chạy hằng ngày có thể dùng incremental sync để cập nhật thay đổi và xử lý học sinh vừa đủ 7 tuổi.  MOE có thể chạy manual sync lại khi dữ liệu cần cập nhật chưa được lấy ở job tự động. Tuy nhiên, phần giải thích về cơ chế sync chưa r; giờ chạy tự động cũng chưa xác nhận chắc chắn (có thể là 12:00 AM).  **\[Action Item\] Xác nhận chính thức quy tắc bootstrap/full sync và incremental sync, cách ghi đè dữ liệu và giờ chạy job tự động.**   |  **For Info**   |
| **3** | **Quản lý School User và tạo School**  |  |
|  | MOE HQ có thể tạo School User riêng lẻ hoặc tạo hàng loạt bằng cách upload CSV. Reviewer yêu cầu không lưu password trong hệ thống; School User cần đăng nhập bằng tài khoản MOE Active Directory (AD), không dùng username/password riêng. Nhóm ghi nhận sẽ cập nhật phương án và trình bày lại ở demo tiếp theo.  Danh sách chọn School User hiện tại bị Reviewer từ chối vì không hiệu quả khi một trường có hàng trăm người dùng; cần thiết kế giải pháp khác. Phạm vi hiện tại: một School User thuộc một school, và một school có thể có nhiều School User. Khi tạo school, các trường thông tin được demo gồm school code, school name và school type: Government, Government-aided, Autonomous, Independent, Specialised. Reviewer cũng nhắc nhóm chuẩn bị demo data trước cuộc họp.     **\[Action Item\] Thiết kế lại cách tìm/chọn/quản lý School User; cập nhật xác thực qua MOE AD và không lưu password**  |  **For Info**  |
| **4** | **Academic Level, Class và Student Enrolment**  |  |
|  | School User cần cấu hình class trước, sau đó tạo student và gán student vào class. Thông tin class gồm code, name và school level. Reviewer yêu cầu đổi nhãn “Student Category” thành “Citizenship”; dù nhóm nêu băn khoăn với học sinh quốc tế, Reviewer khẳng định đây là thuật ngữ cần dùng và nhóm ghi nhận sẽ đổi.  Enrolment status được demo gồm “Enrolled”, “Transferred to another school” và “Closed” khi học sinh tốt nghiệp. Reviewer yêu cầu ngày “Enrolled from” và “Enrolled to” phải chính xác, không điền ngày tốt nghiệp giả định tùy ý; nhóm cho biết có thể để null và school user bổ sung  **\[Action Item\] Đổi nhãn “Student Category” thành “Citizenship”; xác định nguồn/quy tắc cho enrolment dates và không tự đặt ngày tốt nghiệp khi chưa có dữ liệu xác thực**  |  **For Info**  |
| **5** | **Parent Portal và Parent Profile**  |  |
|  | Phụ huynh đăng nhập e-Service Portal bằng Singpass và xem các thẻ thông tin của con, hiện có thông tin cơ bản và EA balance.  Reviewer góp ý trang chủ đang dành quá nhiều diện tích cho ngày sinh, giới tính, chủng tộc, citizenship và địa chỉ—những thông tin phụ huynh đã biết. Nhóm thống nhất cân nhắc ưu tiên thông tin hữu ích hơn như phí cần thanh toán và chuyển thông tin cơ bản sang Student Profile.  Parent Profile được demo với thông tin tích hợp từ Singpass; một số trường như số điện thoại và email có thể được chỉnh sửa, nhưng danh sách field được phép sửa cần xác nhận đầy đủ.  **\[Action Item\] Thiết kế lại student cards để ưu tiên EA balance/phí còn nợ; chuyển thông tin cơ bản sang Student Profile; xác nhận các field Parent Profile có thể chỉnh sửa.**  |  **For Info**  |
| **6** | **Transaction History, Fee Management và Payment Flow**  |  |
|  | Phụ huynh có thể xem Transaction History và các khoản phí còn phải trả của từng con. Reviewer hỏi cách xử lý giao dịch “Not successful”; nhóm hiện mới demo happy path và sẽ rà soát các tình huống lỗi hệ thống/mạng cho QA. Chưa có quyết định cuối cùng về việc có hiển thị giao dịch thất bại cho phụ huynh hay không.  Payment có hai phương thức: dùng EA balance hoặc online payment gateway. Luồng gateway hiện mới ở mức cơ bản; nhóm sẽ bổ sung chi tiết ở demo tuần sau.  Khi tổng phí vượt EA balance, hệ thống demo split payment kết hợp EA balance và gateway. Reviewer yêu cầu phụ huynh được chọn số tiền EA muốn sử dụng thay vì bắt buộc dùng toàn bộ số dư Reviewer cũng yêu cầu hiển thị tên học sinh rõ hơn trên trang phí, điều chỉnh độ rộng cột, không hiển thị EA balance lặp lại và thống nhất định dạng ngày, gồm cả due date. Nhóm xác nhận EA balance và outstanding fees được cập nhật real time sau thanh toán. Các số tiền minh họa trong demo chưa được xác nhận chính thức.  **\[Action Item\] Bổ sung kịch bản lỗi/QA và đề xuất cách hiển thị giao dịch thất bại; hoàn thiện online gateway; cho phép chọn phần EA balance sử dụng; hiển thị rõ tên học sinh, chỉnh độ rộng cột, bỏ thông tin EA balance lặp và thống nhất định dạng ngày.**  |  **For Info** |
| **7** | **Kết luận và bước tiếp theo**  |  |
|  | Reviewer nhận xét giải pháp nhìn chung ổn ở mức tổng quan nhưng nhóm cần đi sâu vào các tình huống chưa được xem xét, đặc biệt các trường hợp ngoại lệ/không thành công, đồng thời đánh giá nội dung nào thực sự hữu ích với phụ huynh. Nhóm sẽ ghi nhận phản hồi, cải thiện solution và trình bày phương án tốt hơn trong demo tuần sau.  |  **For Info**  |

**(The meeting ended at 2:36PM)**

Prepared By: Daniel Tran

