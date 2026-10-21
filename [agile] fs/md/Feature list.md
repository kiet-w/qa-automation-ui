# **Quản lý vòng đời EA (Mở và đóng)**

1. Initial Synchronization: Truy xuất dữ liệu Singapore Citizens từ đủ 7 đến dưới 16 tuổi thông qua Mock Government Citizen API.

2. Daily Incremental Synchronization: Truy xuất những công dân vừa đủ 7 tuổi trong ngày xử lý.

3. Citizen Data Validation: Kiểm tra NRIC, Full Name, DOB, Citizenship và các required fields theo Data Contract.

4. #### ***Student Profile Creation: Lưu thông tin công dân hợp lệ vào internal Student Profile(?).***

5. Education Account Creation: Tạo tài khoản liên kết với Student Profile, với Account Number duy nhất, Status \= Active, Balance \= SGD 0.00 (wallet).

6. Duplicate Prevention: Mỗi Singapore Citizen chỉ có một Education Account, kể cả khi tài khoản cũ đã Closed.

7. Invalid Record Handling: Bỏ qua Citizen Records thiếu required information; Father/Mother NRIC là optional.

8. Student Data Synchronization Boundary: Daily Sync không tự động cập nhật các Student Profiles đã tồn tại.

# **Tự động đóng TK EA**

1. Backend-Triggered Eligibility Check: Trước khi truy cập hoặc xử lý Education Account, backend thực hiện kiểm tra điều kiện đóng (Citizenship/tuổi dựa trên DoB).

2. Real-Time Government Verification: Gọi Mock Government Citizen API để lấy Current DOB và Citizenship của Account Holder.

3. Age-Based Closure: Nếu Account Holder đã đủ 16 tuổi, kích hoạt Account Closure Processing.

4. Citizenship-Based Closure: Nếu Account Holder không còn là Singapore Citizen, kích hoạt Closure Processing. 

5. Active Account Handling: Nếu chưa đủ 16 tuổi và vẫn là Singapore Citizen, tài khoản tiếp tục Active.

6. #### ***Closure Processing: Kiểm tra điều kiện hoàn tất, cập nhật Status \= Closed và Actual Closure Date khi đủ điều kiện (?).***

7. Financial Action Protection: Các yêu cầu Top-Up hoặc Payment phải được kiểm tra trước khi thực hiện.

8. Closed Account Handling: Không đóng lặp lại; giữ thông tin lịch sử và áp dụng quyền xem phù hợp.

9. Student Profile Boundary: Không tự động refresh toàn bộ Student Profile từ Government API.

10. Chuyển tiền dư sau khi đóng qua cpf (chưa làm)

# **R8 \- Parent Portal: SingPass, Education Account & Profile** 

1. Parent chọn Log in with SingPass. 

2. SingPass xác thực và cung cấp Parent NRIC cùng thông tin định danh.

3. System gọi Mock Data API bằng Parent NRIC để tìm Parent và các con có liên kết.

4. Lần đầu đăng nhập, tạo Parent Account và liên kết các con; lần sau tái sử dụng tài khoản.

5. Đồng bộ dữ liệu của Parent và những người con liên quan tại thời điểm đăng nhập, không thực hiện nightly bulk synchronization.

6. Tạo Session và điều hướng Parent vào Home.

7. Chỉ cho phép Parent xem các con được liên kết với mình; cha và mẹ có quyền như nhau.

8. Xử lý lỗi authentication, API timeout, dữ liệu không tìm thấy và Session Expiry.

## **View Education Account** 

1. Parent Home: Hiển thị card của từng con (EA), tên con, mã EA, Nric của con, balance, phí cần phải trả, trạng thái account

2. Có chức năng xem thông tin education entolment trường, cấp, level, năm học, lớp, trạng thái enrolement.

3. Balance Overview: Hiển thị số dư khả dụng, giao dịch Pending và tổng tiền vào/ra.

4. Transaction History: Xem giao dịch, lọc theo thời gian, loại giao dịch và chiều tiền.

5. FAS Information Display: Hiển thị thông tin hỗ trợ tài chính khi có dữ liệu (chưa làm).

6. Age-Based Access Restrictions: Parent vẫn xem được thông tin của con đủ 16 tuổi, nhưng không thực hiện Payment hoặc FAS Application cho con đó.

## **Update Basic Personal Details** 

1. Cho phép parent chỉnh sủa thông tin liên lạc (qua chức năng view my details)

2. Chỉnh sửa Phone Number, Email và Mailing Address. 

3. Không cho sửa NRIC, Full Name hoặc Residential Address (dữ liệu đồng bộ từ singpass).

4. Validate dữ liệu trước khi lưu.

5. Không ghi đè thông tin liên lạc Parent đã tự chỉnh sửa khi đăng nhập lại.

6. Chuyển My details sang read-only khi tất cả các con đã đủ 16 tuổi.

# **R9 Outstanding Fees & Payment** 

1. Cho phép xem hoặc thanh toán các fee của EA liên kết với parent

2. Các invoice chưa thanh toán bao gồm fee type, fee component, invoice items tương ứng với số tiền, subsidy, net amount, ngày tới hạn, status và Account balance

3. Hiển thị transaction history

4. Chọn một invoice → chọn hình thức thanh toán:   
   Education Account: Thanh toán toàn bộ bằng số dư EA nếu đủ điều kiện.

   Online Payment: Thanh toán bằng cổng thanh toán trực tuyến.

   Split Payment: Sử dụng một phần từ EA và phần còn lại từ Online Payment.

5. Gọi dịch vụ Education Account để kiểm tra số dư, trừ tiền và ghi nhận ledger transaction, sử dụng FundingReference để tránh trừ tiền trùng. 

6. Tạo Payment Session với sandbox gateway, chuyển Parent sang bước thanh toán trực tuyến và chờ kết quả từ provider. (mới chỉ mô phỏng)

7. Ghi nhận invoice \= Paid khi thanh toán thành công; hiển thị Payment Reference và Receipt. Nếu Split Payment thất bại ở nhánh online sau khi EA đã bị trừ, hệ thống phải hoàn lại phần EA hoặc chuyển sang ReconciliationRequired nếu không thể hoàn an toàn. 

# **R3 \- School & student management**

## **F01 – School Management**

Actor: MOE HQ User

1. HQ User có thể tạo, xem và chỉnh sửa thông tin School.

2. Thông tin School bao gồm School Code, School Name, School Type và Status (chuẩn bị sẵn list test 10 trường cố định).

3. HQ User có thể xem danh sách School đã được tạo.

4. School mới được tạo phải được lưu trong hệ thống để sử dụng cho School User Assignment và Academic Setup.

5. School có dữ liệu liên quan không bị xóa vĩnh viễn; sử dụng Deactivate theo business rules của FS.

## **F02 – School User Account & School Assignment**

1. Admin tạo danh sách các trường 

2. School user đăng nhập bằng school ID của họ (Assume do nhà trường cấp), lần đầu đăng nhập phải tự nhập các thông tin cá nhân: tên, trường. (làm sprint sau)

## **F03 – Academic Year, Education Stage & Academic Level Configuration** 

Actor: School User

1. SU truy cập School Configuration.

2. SU lựa chọn Academic Year từ danh sách có sẵn.

3. SU lựa chọn Education Stage/School Level mà trường giảng dạy, ví dụ Primary, Secondary hoặc Pre-University.

4. Hệ thống hiển thị các Academic Levels phù hợp để SU lựa chọn từ danh sách có sẵn.

5. SU chọn các Levels được giảng dạy tại School trong Academic Year đó.

6. SU add các tên lớp trong từng academic level

7. Hệ thống lưu cấu hình School – Academic Year – Academic Level Offering – Class name.

8. Hệ thống không cho tạo trùng một Level trong cùng School và Academic Year.

9. Một Level có thể có nhiều Classes.

10. SU có thể xem danh sách Classes theo School, Academic Year và Level.

11. Hệ thống không cho phép tạo trùng Class Code trong cùng School Level Offering.

12. Class đã có Student Assignment không được xóa làm mất dữ liệu lịch sử.

## **F05 – Student Record Creation & Management**

Actor: School User

1. SU truy cập Student Management và có thể tạo Student Record mới.

2. Thông tin Student bao gồm:

   * Student ID

   * Full Name

   * NRIC

   * Date of Birth

   * Student Category (SC / PR / IS)

3. Hệ thống validate các trường bắt buộc và kiểm tra Student Record trùng.

4. Hệ thống sử dụng NRIC để tìm Education Account tương ứng nếu có.

5. Nếu tìm thấy EA, hệ thống kiểm tra các thông tin định danh cần đối chiếu.

6. Nếu thông tin phù hợp, Student Record được liên kết với EA.

7. Nếu thông tin không khớp, hệ thống hiển thị cảnh báo hoặc chặn lưu theo quy tắc được xác nhận. \[TBC\]

8. Nếu không có EA, hệ thống vẫn tạo student record (STUDENT RECORD không phải EDUCATION ACCOUNT).

9. SU có thể xem và chỉnh sửa những Student Details được phép sửa.

## **F06 – Student Enrolment** 

1. School User (SU) truy cập cấu trúc trường theo School → Academic Year → Academic Level → Class.

2. SU chọn một Class đã được cấu hình và assign một hoặc nhiều Student Records vào Class đó.

3. Student Record phải được tạo trước khi thực hiện Class Assignment.

4. SU chỉ được assign Student vào Class thuộc School mình được phân quyền.

5. Sau khi assign thành công, hệ thống tự động tạo **Enrolment Profile** cho từng Student.

6. Enrolment Profile bao gồm: Student ID, Student Information, School, Academic Year, Academic Level, Class, Enrolment Status và Effective Date.

7. Thông tin School, Academic Year và Academic Level được tự động xác định từ Class đã chọn.

8. SU có thể xem danh sách Students thuộc từng Class và Enrolment Profile của từng Student.

9. Hệ thống không cho phép tạo các Active Enrolment Profiles bị trùng hoặc xung đột.

## **F07– Student Transfer & Class Change** 

10. Khi Student chuyển Class, Academic Level hoặc Academic Year trong cùng School, SU thực hiện thay đổi Enrolment; hệ thống chuyển profile cũ sang **Inactive** và tạo profile mới với thông tin cập nhật.

11. Khi Student chuyển School, SU trường cũ Deactivate Enrolment Profile; SU trường mới nhập Student Information với Student ID do trường mới cấp và assign vào Class để tạo Enrolment Profile mới.

12. Student ID được cấp và quản lý theo từng School, không bắt buộc giữ nguyên khi chuyển School.

13. Các Enrolment Profiles cũ được giữ lại để tra cứu lịch sử, không bị xóa hoặc ghi đè.

14. Hệ thống ghi nhận người thực hiện, thời điểm và lý do thay đổi Enrolment. **\[Đề xuất\]**

15. Việc tạo Enrolment Profile không đồng nghĩa với việc tạo Education Account; EA được quản lý riêng theo R1.

## **F08 – Student–Education Account Linkage**

Actor: System

1. Hệ thống kiểm tra NRIC và Student Category khi Student Record được tạo hoặc liên kết.

2. Với Student có EA hợp lệ, hệ thống liên kết Student Record với EA tương ứng.

3. Liên kết không tạo ra một EA mới và không thay đổi Account Balance.

4. Hệ thống phải xử lý trường hợp EA không tồn tại, EA đã Closed hoặc dữ liệu định danh không khớp.

5. HQ User và SU có thể xem trạng thái EA Linkage theo quyền truy cập.

## **F10 – Student Enrolment Overview**

Actors: School User, MOE HQ User, Parent (read-only)

1. SU có thể xem Student Records và Enrolments thuộc School mình.

2. HQ User có thể xem Student Enrolment theo School, Academic Year, Level và Class.

3. Người dùng có thể mở Student Detail để xem enrolment hiện tại và lịch sử phù hợp với quyền.

4. Parent đã được xác minh quan hệ và liên kết với Student có thể xem thông tin học tập/enrolment được phép hiển thị qua e-Service Portal.

5. Không cho phép School User truy cập Student Records của School khác nếu không có quyền.

# 

# **Làm trong sprint sau**

# **R1:Education Account Lifecycle Management**  

1. CPF Transfer khi tài khoản đóng ở tuổi 16 

# **R3**

## **F09 – Bulk CSV Import for Academic Setup & Student Management**

Actor: School User

1. SU có thể upload CSV để cấu hình School Academic Structure.

2. CSV có thể chứa Academic Year, Academic Level và Class Information.

3. SU có thể upload CSV để tạo nhiều Student Records cùng lúc.

4. CSV Student có thể bao gồm thông tin Class Assignment tương ứng.

5. Hệ thống kiểm tra file format, required fields, duplicate records và tính hợp lệ của School/Class.

6. Hệ thống hiển thị Import Preview trước khi thực hiện. \[Proposed UX\]

7. Sau khi xác nhận, hệ thống tạo các records hợp lệ và thực hiện Class Assignment theo dữ liệu CSV.

8. Hệ thống hiển thị Import Result, bao gồm Successful, Skipped và Failed Records. \[Proposed UX\]

9. Các records lỗi cần có lý do để SU chỉnh sửa và import lại.

# **R2 – Education Account Top-Up** 

## **Individual Top-Up** 

1. \[CR\] MOE HQ User có thể Top-Up tiền vào một Education Account cụ thể.

2. \[PD\] MOE HQ User truy cập Top-Up → Individual Top-Up.

3. \[PD\] MOE HQ User tìm kiếm Education Account theo Account Number hoặc Student NRIC.

4. \[PD\] Hệ thống hiển thị thông tin Account Holder, Account Status và Current Balance để Admin xác minh trước khi thực hiện.

5. \[PD\] MOE HQ User nhập Top-Up Amount và xác nhận giao dịch.

6. \[PD\] Hệ thống cộng tiền vào Education Account Balance và ghi nhận Top-Up Transaction khi thực hiện thành công.

7. \[PD\] Hệ thống hiển thị kết quả thành công hoặc thất bại.

## **Bulk Top-Up Rule Configuration** 

1. \[CR\] MOE HQ User có thể thực hiện Batch Top-Up dựa trên các criteria như Age, Account Balance và Schooling Status.

2. \[PD\] MOE HQ User truy cập Top-Up → Bulk Top-Up.

3. \[PD\] MOE HQ User tạo một Bulk Top-Up Campaign cho Academic Year và Round cụ thể.

4. \[PD\] MOE HQ User cấu hình các điều kiện:  
   Age Range: Nhập Minimum Age và Maximum Age.  
   Account Balance: Nhập điều kiện so sánh và ngưỡng số dư, ví dụ Balance \< SGD 100\.  
   Schooling Status: Chọn Actively Enrolled trong Academic Year.  
   Top-Up Amount: Nhập số tiền cố định được cấp cho mỗi eligible Account.

5. \[PD\] MOE HQ User có thể lưu cấu hình để chuẩn bị thực hiện Bulk Top-Up.

6. \[PD\] Mỗi Campaign trong MVP áp dụng một bộ criteria và một Top-Up Amount.

7. Một kỳ có thể thực hiện nhiều scheme bulk top up khác nhau với amount khác nhau dựa trên criteria khác nhau

Business Rules / Constraints

* \[PD\] Student phải đáp ứng tất cả configured criteria (AND logic).

* \[PD\] Age được xác định từ DOB tại Eligibility Date của Campaign.

* \[PD\] Schooling Status được xác định từ Student Enrolment của R3, không suy ra từ tuổi.

* \[PD\] Hệ thống chỉ xét những Education Accounts tồn tại và đang Active.

* \[TBC\] Balance Criteria được xét tại Eligibility Date

* \[TBC\] Student không có Enrolment Record bị loại khỏi campaign auto

* Cần có limit cho top-up budget.

## **Bulk Top-Up Preview & Confirmation** 

1. \[PD\] MOE HQ User có thể Preview danh sách Education Accounts đủ điều kiện dựa trên configured criteria.

2. \[PD\] Hệ thống hiển thị các thông tin cơ bản của từng eligible Account: Student, Age, Current Balance, Schooling Status và Top-Up Amount.

3. \[PD\] Hệ thống hiển thị tổng số eligible Accounts và tổng Top-Up Amount dự kiến.

4. \[PD\] MOE HQ User kiểm tra kết quả và xác nhận trước khi xác nhận Bulk Top-Up.

5. \[PD\] Nếu criteria thay đổi, MOE HQ User phải Preview lại trước khi xác nhận.

### **Business Rules / Constraints** 

* \[TBC\] Có cho phép Admin loại một số Accounts khỏi danh sách Preview theo cách thủ công

## **Bulk Top-Up ExecutionActor: MOE HQ User / System**

1. \[CR\] MOE HQ User có thể thực hiện Top-Up hàng loạt.

2. \[PD\] MOE HQ User xác nhận Execute Bulk Top-Up.

3. \[PD\] Hệ thống xác định danh sách eligible Accounts theo Campaign.

4. \[PD\] Hệ thống kiểm tra Account Status và eligibility trước khi ghi tiền.

5. \[PD\] Hệ thống cộng Top-Up Amount tương ứng vào từng eligible Education Account.

6. \[PD\] Hệ thống ghi nhận Top-Up Transaction cho từng Account được nạp thành công.

7. \[PD\] Hệ thống hiển thị kết quả xử lý: Successful, Skipped và Failed.

## **Top-Up History & ResultsActor: MOE HQ User**

1. \[PD\] MOE HQ User có thể xem danh sách các Individual Top-Up Transactions và Bulk Top-Up Campaigns đã thực hiện.

2. \[PD\] MOE HQ User xem chi tiết kết quả của một Bulk Campaign, bao gồm danh sách Accounts được nạp, không được nạp và xử lý thất bại.

3. \[PD\] Hệ thống ghi nhận Transaction Reference, Top-Up Amount, thời điểm thực hiện và người thực hiện.

4. \[PD\] Các Top-Up Transactions thành công được phản ánh trong Education Account Transaction History của R1/R8.

Business Rules / Constraints

* \[PD\] Failed Top-Up không làm tăng Account Balance.

* \[PD\] Không chỉnh sửa trực tiếp một Top-Up Transaction đã thành công.

* Khi nạp nhầm tiền admin có thể chọn tài khoản AE trong danh sách thành công để chỉnh sửa và cập nhật lại (trường hợp top up manually)

# 

# **R3 – Fee Management (MVP Functional Feature List)** 

Proposed MVP Fee Master Data

| Fee Type | Fee Component | Created By |
| :---- | :---- | :---- |
| 1\. Academic Fees | School Fee | HQ |
|  | Miscellaneous Fee | HQ |
| 2\. Examination Fees | Examination Fee | HQ |
|  | Supplementary Examination Fee | HQ |
| 3\. Programme Fees | Enrichment Programme Fee | School A |
|  | Educational Excursion Fee | School A |
| 4\. Student Services Fees | School Transport Fee | School A |
|  | School Meal Fee | School A |

## **Fee Type & Fee Component Management**

1. **MOE HQ User** có thể Create, View, Edit và Deactivate các Fee Types và Fee Components dùng chung cho toàn hệ thống. (có thời gian áp dụng)

2. School User (SU) có thể sử dụng các HQ Shared Fee Types/Components và tự tạo thêm School-specific Fee Types/Components theo nhu cầu thu phí của School mình.

3. Khi tạo Fee Type mới, người dùng nhập **Fee Type Name**, Description (nếu cần) và có thể thêm một hoặc nhiều Fee Components ngay trong cùng màn hình cấu hình.

4. Mỗi Fee Component có **Component Name** và Description (nếu cần).

5. Khi lưu, hệ thống tạo Fee Type cùng các Fee Components đã cấu hình bên trong.

6. Người dùng có thể xem danh sách các Fee Types đã tạo và mở từng Fee Type để xem các Components tương ứng.

7. Khi cần bổ sung khoản phí, người dùng mở Fee Type đã tồn tại và chọn **Add Component**; không cần chức năng tạo Component độc lập rồi gán vào Fee Type.

8. Một Fee Type có thể chứa nhiều Fee Components, nhưng mỗi Fee Component chỉ thuộc một Fee Type (**quan hệ 1**).

9. SU có thể xem và sử dụng các Fee Types/Components dùng chung của HQ cùng với danh mục phí riêng của School mình.

10. SU không được Edit hoặc Deactivate Fee Types và Fee Components do HQ quản lý.

11. SU được phép thêm **Fee Component riêng của School vào Fee Type dùng chung của HQ**. Component mới chỉ thuộc School đó, không ảnh hưởng đến danh mục chung hoặc các School khác.

12. SU chỉ được chỉnh sửa hoặc Deactivate các Fee Types/Components do School mình tạo.

13. Hệ thống kiểm tra trùng Fee Type Name và Component Name trong cùng phạm vi quản lý. **\[Đề xuất MVP\]**

14. Các Fee Types/Components đã được sử dụng trong Fee Publications hoặc Student Charges không được xóa vĩnh viễn; chỉ được Deactivate để giữ lịch sử.

15. Fee Types/Components đã Deactivate không được lựa chọn cho Fee Publications mới.

16. Đối với Fee Components do HQ quản lý: Amount được cấu hình riêng tại Fee Rate Configuration, dựa trên **Education Stage, Student Category và thời gian hiệu lực**. SU chỉ được xem, không được thay đổi.

17. **Đối với Fee Components riêng của School:** Không áp dụng Fee Rate Configuration của HQ. SU tự cấu hình Amount và thời gian áp dụng theo chính sách của School.

18. Các Fee Types và Components mẫu cho MVP:

    * **Academic Fees:** School Fee, Miscellaneous Fee.

    * **Programme Fees:** Enrichment Programme Fee, Educational Excursion Fee.

    * **Student Services Fees:** School Transport Fee, School Meal Fee.

19. SU có thể tạo thêm Fee Types và Components ngoài danh mục mẫu để đáp ứng nhu cầu thu phí riêng của School.

## 

## **Fee Rate Configuration**

1. **MOE HQ User** có thể Create, View và Edit Fee Rates cho các **Fee Components dùng chung do HQ quản lý**.

2. Fee Rate được cấu hình chủ yếu theo **Education Stage (Primary, Secondary, Pre-University)** và **Student Category (SC/PR/IS)**.

3. Khi cấu hình Fee Rate, HQ chọn Fee Component đã tồn tại và nhập các thông tin:

   * Education Stage

   * Student Category

   * Amount (SGD)

   * Effective From

   * Effective To

4. Một Fee Component có thể có nhiều Fee Rates khác nhau theo Education Stage và Student Category.

5. HQ có thể mở một Fee Component để xem danh sách các Fee Rates đã cấu hình và thêm mức phí mới nếu cần.

6. Hệ thống không cho phép các Fee Rates có cùng **Fee Component \+ Education Stage \+ Student Category** bị chồng lấn thời gian hiệu lực.

7. School User có thể xem các Fee Components và Fee Rates của HQ, bao gồm Amount và thời gian áp dụng, nhưng không được chỉnh sửa.

8. Khi SU tạo Fee Publication sử dụng Component của HQ, hệ thống xác định mức phí phù hợp dựa trên Education Stage, Student Category và thời gian hiệu lực.

9. Education Stage của Student được xác định thông qua Academic Level trong Enrolment Profile (ví dụ P3 thuộc Primary, S2 thuộc Secondary).

10. Nếu không có Fee Rate phù hợp, hệ thống thông báo khoản phí chưa được cấu hình đầy đủ và không tự xác định Amount.

11. **Fee Rate Configuration không áp dụng cho các Fee Components riêng của School**, kể cả khi nằm trong Fee Type dùng chung của HQ.

12. Đối với Fee Components riêng, School User tự cấu hình Amount và thời gian áp dụng theo chính sách của trường.

13. Fee Rates chỉ xác định mức tiền phải thu, **không tự động tạo Student Charges**. Student Charges chỉ được tạo khi Fee Publication được Publish.

14. Student Charges đã phát hành giữ nguyên Amount tại thời điểm phát hành, không tự động thay đổi khi HQ cập nhật Fee Rate.

![][image1]

## 

## **Fee Publication & Target Configuration – Các quy tắc cập nhật**

1. School User có thể lựa chọn các HQ Shared Fee Components hoặc School-specific Fee Components đã được cấu hình trước đó trong R3 và đang Active để tạo Fee Publication. SU vẫn có thể tự tạo thêm School-specific Components thông qua Fee Type & Fee Component Management khi có nhu cầu.

2. Việc Publish Fee và tạo Student Charges không phụ thuộc vào việc Fee Component đã được cấu hình trong Subsidy Matrix của R4 hay chưa.

3. HQ Fee Components không bắt buộc phải được phát hành toàn bộ; SU lựa chọn các khoản cần thu theo nhu cầu và chính sách áp dụng.

4. SU không được thay đổi Fee Rates đã được HQ cấu hình.

5. SU có thể tạo nhiều Fee Publications cho cùng một Fee Component ở các Billing Period hoặc đợt thu khác nhau.

6. Mỗi Fee Publication ghi nhận tối thiểu: Publication Name, School, Academic Year, Billing Period, Fee Components, Target Students Level (khối) và Due Date.

7. Trước khi Publish, hệ thống cho SU Preview danh sách Students, Components và Amount dự kiến.

8. Hệ thống kiểm tra các Student Charges đã phát hành để phát hiện khoản thu có khả năng bị trùng cho cùng Student, Fee Component và kỳ/đợt thu.

9. Hệ thống không được tạo Student Charges trùng do Publish lại cùng một Publication.

10. Với trường hợp cùng Fee Component được thu nhiều lần, các đợt thu phải có thông tin phân biệt rõ ràng.

11. **MVP chưa tự động kiểm soát số lần tối đa một Fee Component được phép thu trong năm.** Việc tuân thủ chính sách về tần suất thu phí thuộc trách nhiệm quản lý nghiệp vụ ngoài hệ thống. \[Working Assumption – cần client xác nhận\]

## **Student Charge GenerationActor: System**

1. \[FS\] Khi Fee Publication được Publish, hệ thống xác định danh sách Students phù hợp với Target thông qua Enrolment và Class Assignment tại Eligibility Date.

2. \[FS\] Hệ thống lấy Fee Rate phù hợp hoặc Fixed Amount đã cấu hình để tính khoản phí cho từng Student.

3. \[FS\] Hệ thống tạo Student Charge cho mỗi Student đủ điều kiện, bao gồm Fee Component, Amount, Tax (nếu có), Due Date và Status.

4. \[FS\] Chỉ Student Charge ở trạng thái POSTED mới được hiển thị cho Parent.

5. \[FS\] Một Student không được tạo hai Student Charges từ cùng một Fee Publication.

6. \[PD\] MVP chỉ cần hỗ trợ tính khoản phí cơ bản và Tax theo cấu hình sẵn có; không xây dựng Tax Rule Engine nâng cao. \[TBC\]

## **Student Charge Viewing & ManagementActor:** 

MOE HQ User / School User

1. Khi School User xác nhận **Publish Fee Publication**, hệ thống tự động xác định danh sách Students cần thu phí dựa trên Target Students đã chọn.

2. Hệ thống sử dụng **Enrolment Profile** để xác định School, Academic Year, Education Stage, Academic Level và Class của từng Student tại thời điểm áp dụng.

3. Hệ thống xác định Amount cho từng Fee Component:

   1. **HQ Components:** Lấy Amount từ Fee Rate đã cấu hình theo Education Stage, Student Category và thời gian hiệu lực.

   2. **School-specific Components:** Lấy Amount do SU cấu hình trong Fee Publication.

4. Hệ thống tạo một **Student Charge cho mỗi Student và mỗi Fee Component** được phát hành.

5. Mỗi Student Charge ghi nhận tối thiểu: **Student, School, Fee Component, Original Amount, Due Date, Status và Fee Publication Reference**.

6. Các Student Charges được tạo thành công có trạng thái **POSTED** và được chuyển sang danh sách Outstanding Fees để Parent xem trên e-Service Portal (R9).

7. Hệ thống không tạo Student Charges trùng lặp khi cùng một Fee Publication được Publish lại.

8. Student Charges được tạo với Original Amount độc lập với trạng thái FAS Grant của Student. Subsidy Amount và Net Payable có thể được cập nhật sau khi Student được Grant FAS hợp lệ theo business rules của R4.

9. SU có thể tạo nhiều Fee Publications cho cùng một Fee Component ở các kỳ hoặc đợt thu khác nhau.

10. Trước khi tạo Charges, hệ thống kiểm tra các khoản đã phát hành để phát hiện trường hợp cùng Student bị thu trùng Fee Component trong cùng kỳ/đợt thu.

11. Nếu thiếu Fee Rate, Amount không hợp lệ hoặc Student không có Enrolment phù hợp, hệ thống phải thông báo lỗi và không tạo Charge sai.

12. Student Charges đã POSTED giữ nguyên Original Amount và thông tin School/Enrolment tại thời điểm phát hành, kể cả khi Student chuyển lớp, chuyển trường hoặc Fee Rate thay đổi.

## **Outstanding Fee Integration with R9**

1. Các **Student Charges** được tạo thành công và có trạng thái **POSTED** sẽ được cung cấp cho Parent Portal (R9) để hiển thị các khoản phí cần thanh toán.

2. Hệ thống sử dụng các Student Charges để hiển thị **Outstanding Fees / Invoice** cho từng Student.

3. Mỗi khoản phí hiển thị tối thiểu: **Fee Component, Original Amount, Subsidy Amount (nếu có), Net Payable, Due Date và Payment Status**.

4. Parent chỉ được xem và thanh toán các khoản phí của Students đã được xác minh quan hệ và liên kết với tài khoản Parent.

5. Parent có thể xem danh sách các khoản phí chưa thanh toán và chọn khoản muốn thanh toán.

6. R9 chịu trách nhiệm xử lý thanh toán bằng **Education Account Balance, Online Payment hoặc Split Payment** theo các phương thức được hỗ trợ.

7. Sau khi thanh toán thành công, hệ thống cập nhật trạng thái thanh toán và số tiền còn phải trả, tránh hiển thị khoản đã thanh toán đầy đủ như Outstanding Fee.

8. Các khoản phí đã thanh toán vẫn được giữ lại để Parent xem lịch sử.

9. R3 chịu trách nhiệm tạo và quản lý Student Charges; R9 chịu trách nhiệm Payment Processing và cập nhật kết quả thanh toán.

## **Fee Integration with R4** 

1. R4 sử dụng các **Fee Components đã tồn tại trong R3** để cấu hình Subsidy Matrix theo từng FAS Scheme, Education Stage/Academic Level và Fee Component.

2. HQ Admin có thể chọn HQ Shared Fee Components cho MOEFAS; SU có thể chọn HQ Shared Components và School-specific Components thuộc trường mình cho SBFAS.

3. HQ/SU quyết định Fee Components nào được hỗ trợ. Khi có Component mới, SU có thể bổ sung vào Subsidy Matrix nếu cần; hệ thống không bắt buộc mọi Component phải được trợ cấp.

4. **Fee Publication hoạt động độc lập với FAS**. SU có thể Publish Fee dù chưa có Subsidy Rule hoặc FAS Grant.

5. Khi FAS Grant được **Finalize/Published trước Due Date** và Student Charge chưa thanh toán, System áp dụng Subsidy theo Matrix của Scheme đã Grant.

6. System giữ riêng **Original Amount, Subsidy Amount và Net Payable**. Net Payable \= Original Amount − Subsidy Amount; Subsidy không vượt Original Amount và không làm thay đổi Original Amount.

7. Nếu không có FAS Grant hợp lệ hoặc Fee Component không được hỗ trợ, Subsidy Amount \= 0\. **R9 sử dụng Net Payable** để hiển thị Outstanding Fees và xử lý Payment.

# 

# **R4**

## **FAS Application Submission**

**Actors: Parent / School User (SU)**

1. System hỗ trợ hai phương thức nộp FAS Application:

   * **Online Application:** Parent nộp trên Parent Portal.

   * **Paper Application:** Parent nộp đơn giấy tại School; SU nhập Application vào hệ thống.

2. **Online Application:**

   * Parent chỉ có thể chọn Student đã có Education Account (EA) liên kết và được xác minh quan hệ.

   * System tự động điền Student Information từ dữ liệu có sẵn.

   * Parent cung cấp thông tin định danh của Applicant, các Children và Family Members (bao gồm NRIC/FIN), thông tin hoàn cảnh gia đình và Declaration. GHI/PCI được hệ thống truy xuất hoặc tính toán dựa trên Government/Third-party API khi thực hiện Eligibility Assessment; Parent không tự nhập Income Details. 

3. **Paper Application:**

   * SU có thể tiếp nhận và tạo Application cho tất cả Students thuộc School mình, bao gồm cả Students chưa có EA.

   * SU chọn Student Record trong R3 để liên kết với Application.

   * SU có thể nhập thông tin thủ công hoặc Upload bản scan/photo của đơn giấy.

   * MVP hỗ trợ **Simulated OCR** để prefill một số fields từ file mẫu; SU có thể kiểm tra và chỉnh sửa trước khi Submit.

4. Cả hai phương thức sử dụng chung các nhóm dữ liệu:

   * **Student Information:** Student, NRIC, Citizenship, School, Academic Level.

   * **Parent/Guardian Information:** Name, NRIC/FIN, Relationship, Contact Number.

   * **Household Information:** GHI, Household Size và PCI do System tính.

   * **Assistance Details:** SBFAS Consideration và Family Circumstances/Notes (optional).

   * **Declaration & Supporting Documents:** Thông tin xác nhận phù hợp với từng phương thức nộp.

5. Một Family Submission có thể bao gồm nhiều Children và được liên kết bằng Family Reference. School, Academic Level và Class được khai trong đơn được lưu làm Submission Snapshot, không phải dữ liệu chính thức để xác định Eligibility hoặc Subsidy khi Assessment. 

6. Sau khi Submit, System lưu Application ở trạng thái Pending Assessment. System chỉ thực hiện FAS Eligibility Assessment khi FAS Scheme áp dụng và Enrolment Profile hợp lệ của Student cho Target Academic Year đã sẵn sàng. Online và Paper Applications sử dụng cùng quy trình Assessment. 

7. Application được liên kết với Student Record và các Student Charges phù hợp từ R3 để phục vụ Subsidy Calculation.

8. MVP chưa cần triển khai OCR thật; việc xử lý Student chưa có EA được tách khỏi chức năng EA Payment trên R9.

## **FAS Scheme Management**

1. System hỗ trợ 2 Scheme Types: MOEFAS và SBFAS.

2. MOE HQ Admin quản lý MOEFAS Schemes; School User quản lý SBFAS Schemes thuộc trường mình.

3. Admin có thể Create, View, Edit, Activate/Deactivate Schemes theo quyền được cấp.

4. Mỗi Scheme bao gồm: Scheme Code, Name, Type, Description, Effective Date, Expiry Date và Status.  
   Một MOEFAS Scheme có thể áp dụng cho nhiều trường đủ điều kiện; mỗi SBFAS Scheme được liên kết với một School.

5. Trước khi Activate, MOEFAS Scheme phải có Eligibility Criteria và Subsidy Matrix; SBFAS Scheme phải có Subsidy Matrix.

6. Mỗi Scheme có thể được sử dụng trong các đợt xét duyệt với Budget và Application Deadline tương ứng. Chi tiết được quy định trong FAS Application & Batch Processing.

   → **\[Update\]** Nếu Student đáp ứng MOEFAS Eligibility Criteria, System Auto Grant FAS mà không phụ thuộc Remaining Budget. System theo dõi Budget Usage và hiển thị Warning/Notification khi Budget bị vượt. Subsidy Amount thực tế được tính khi có Student Charges phù hợp. 

7. 

## **MOEFAS Eligibility Configuration**

**Actor: MOE HQ Admin**

1. HQ Admin có thể Create, View và Edit Eligibility Criteria riêng cho từng MOEFAS Scheme. MVP chỉ cần cấu hình sẵn một Scheme mẫu.

2. MVP hỗ trợ ba nhóm Eligibility Criteria:

   * **Citizenship:** Quốc tịch đủ điều kiện.

   * **Household Income:** GHI Threshold và PCI Threshold.

   * **Eligible Schools:** Chọn Schools từ danh sách R3.

3. System đánh giá Income theo logic **GHI ≤ Threshold OR PCI ≤ Threshold**.

4. Student được đánh giá MOEFAS Eligible khi đáp ứng **Citizenship AND (GHI OR PCI) AND Eligible School**, dựa trên Active Enrolment Profile.  
   **\[Cập nhật\]** Khi Application đủ điều kiện Processing, System truy xuất Government-verified Citizenship, GHI và PCI, đồng thời xác định School và Enrolment Status từ Enrolment Profile phù hợp với Target Academic Year để đánh giá MOEFAS Eligibility. System không yêu cầu Student Charges phải tồn tại tại thời điểm Eligibility Assessment. 

5. Khi Application được Submit, System tự động đánh giá Eligibility và tính Subsidy Amount theo Subsidy Matrix.

6. Nếu Eligible và Remaining Budget đủ, System **Auto Grant FAS**, cập nhật Application Status và trừ Subsidy Amount khỏi Remaining Budget.

7. Nếu Not Eligible, System ghi nhận MOEFAS Not Eligible và chuyển sang SBFAS Review theo quy trình áp dụng.

8. Subsidy chỉ được áp dụng cho Student Charges chưa thanh toán và có Due Date chưa đến hạn; R9 cập nhật Net Payable tương ứng.

9. MVP chưa cần Batch Processing, Financial Priority Ranking hoặc các Eligibility Criteria nâng cao.

![][image2]

## **SBFAS Eligibility** 

**Actor: School User (SU)**

1. Mỗi SBFAS Scheme bao gồm **Scheme Information, Eligibility Description và Subsidy Matrix**.

2. **Eligibility Description** là đoạn free-text ngắn mô tả hoàn cảnh hoặc nhóm học sinh mà Scheme hướng tới, dùng làm cơ sở cho School User đánh giá và AI Recommendation.

3. MVP không yêu cầu cấu hình hard income thresholds hoặc Eligibility Rule Engine cho SBFAS.

4. School User có thể Create/Edit Eligibility Description và Subsidy Matrix của các SBFAS Schemes thuộc School mình.

5. Scheme phải có Eligibility Description và Subsidy Matrix hợp lệ trước khi Activate.

6. Khi review FAS Application, System có thể hiển thị **AI Recommendation** về SBFAS Scheme phù hợp; School User là người quyết định Grant hoặc Reject.

## **SBFAS Manual Review & Decision** 

1. Mỗi SBFAS Scheme bao gồm **Scheme Information, Eligibility Description và Subsidy Matrix**.

2. **Eligibility Description** là đoạn free-text ngắn mô tả hoàn cảnh hoặc nhóm học sinh mà Scheme hướng tới, dùng làm cơ sở cho School User đánh giá và AI Recommendation.

3. MVP không yêu cầu cấu hình hard income thresholds hoặc Eligibility Rule Engine cho SBFAS.

4. School User có thể Create/Edit Eligibility Description và Subsidy Matrix của các SBFAS Schemes thuộc School mình.

5. Scheme phải có Eligibility Description và Subsidy Matrix hợp lệ trước khi Activate.

6. Khi review FAS Application, System có thể hiển thị **AI Recommendation** về SBFAS Scheme phù hợp; School User là người quyết định Grant hoặc Reject.

## **Subsidy Matrix Configuration**

**Actor: MOE HQ Admin / School User**

1. Mỗi FAS Scheme có một Subsidy Matrix riêng.

2. Subsidy Matrix được cấu hình theo **Education Stage × Fee Component** (Primary, Secondary, Pre-University).

3. Fee Components được lấy từ danh mục đã cấu hình trong R3, theo quyền quản lý của HQ/SU.

4. User cấu hình Subsidy Type (Percentage / Fixed Amount) và Subsidy Value cho từng Education Stage và Fee Component.

5. Một Scheme có thể hỗ trợ nhiều Fee Components với các mức trợ cấp khác nhau; Fee Components không có trong Matrix sẽ không được hỗ trợ.

6. Không cho phép các Subsidy Rules trùng trong cùng Scheme, Education Stage và Fee Component.

7. Percentage Subsidy phải từ 0–100%; Subsidy Amount không được vượt Original Charge.

8. System xác định Education Stage của Student thông qua Academic Level trong Active Enrolment Profile để áp dụng Subsidy Rule tương ứng.

#### ***Ví dụ Subsidy Matrix*** 

**1\. MOEFAS – Government Financial Assistance 2026**

Eligibility: Singapore Citizen, GHI ≤ SGD 4,000 OR PCI ≤ SGD 1,000, thuộc Eligible Schools.

| HQ Fee Component | Primary | Secondary | Pre-University |
| :---- | :---- | :---- | :---- |
| School Fee | N/A | 100% | 100% |
| Miscellaneous Fee | 100% | 100% | 100% |

**2\. SBFAS – School A**

3 Schemes – School User

Cả ba Scheme đều dùng các School-specific Fee Components đã tạo trong R3. Để đơn giản hóa, các tỷ lệ dưới đây áp dụng cho Primary – All Levels (P1–P6) trong demo.

SBFAS – High Support : Khó khăn tài chính nghiêm trọng

PCI, GHI, Coxtext: 

Enrich

| Fee Component | khối 1 | 2 | 3 |
| :---- | :---- | :---- | :---- |
| Enrichment Programme Fee | 100% | 100% | 100% |
| Educational Excursion Fee | 100% | 100% | 100% |
| School Transport Fee | 75% | 50% | 30% |
| School Meal Fee | 75% | 50% | 30% |

SBFAS – Medium Support : Áp lực tài chính đáng kể

| Fee Component | Primary | Secondary | Pre-University |
| :---- | :---- | :---- | :---- |
| Enrichment Programme Fee | 50% | 50% | 50% |
| Educational Excursion Fee | 50% | 50% | 50% |
| School Transport Fee | 50% | 30% | 20% |
| School Meal Fee | 50% | 30% | 20% |

SBFAS – Basic Support

Cần hỗ trợ một phần chi phí

| Fee Component | Primary | Secondary | Pre-University |
| :---- | :---- | :---- | :---- |
| Enrichment Programme Fee | 25% | 25% | 25% |
| Educational Excursion Fee | 25% | 25% | 25% |
| School Transport Fee | 25% | 15% | 10% |
| School Meal Fee | 25% | 15% | 10% |

## **FAS Eligibility Assessment & Grant Processing**

Actor: System / School User

1. System đánh giá MOEFAS Eligibility khi FAS Application được submit.

2. Nếu Eligible, System tính Subsidy Amount theo Subsidy Matrix và kiểm tra Remaining Budget của Scheme. Nếu đủ Budget, System **Auto Grant**, trừ Budget và cập nhật Application Status.

   → **\[Client Confirmed Update\]** Nếu Student đáp ứng Eligibility Criteria, System thực hiện Auto Grant MOEFAS, ghi nhận Approved Scheme và Target Academic Year. Budget không phải điều kiện để Approve/Reject Application. System theo dõi Budget Usage và cảnh báo khi vượt Configured Budget. 

3. Nếu Not Eligible: System chuyển Application sang School User để review SBFAS.

4. School User có thể chọn SBFAS Scheme phù hợp và Grant hoặc Reject Application.

5. System lưu Assessment Result, Grant Decision, Scheme Applied và Decision Date.

6. System phân biệt MOEFAS Not Eligible với FAS Application Rejected.

7. Nếu MOEFAS Eligible nhưng không đủ Budget, System ghi nhận **Eligible – Insufficient Budget**, không Auto Grant.

   → \[**Client Confirmed Update\]** Nếu MOEFAS Eligible nhưng Budget Usage vượt Configured Budget, System vẫn Auto Grant Application và ghi nhận Budget Warning. Không sử dụng trạng thái `Eligible – Insufficient Budget` để chặn Grant. 

## **Subsidy Application to Student Charges**

Actor: System

1. Khi Student được Grant FAS **trước Due Date** và Student Charge chưa được thanh toán, System áp dụng Subsidy Rules của Scheme đã Grant cho các Student Charges phù hợp từ R3.

2. Subsidy được tính theo **Education Stage và Fee Component** của Student Charge.

3. System lưu riêng Original Amount, Subsidy Amount và Net Payable.

4. **Net Payable \= Original Amount − Subsidy Amount.**

5. Subsidy Amount không được vượt Original Amount; Net Payable không được âm.

6. R9 sử dụng Net Payable để hiển thị Outstanding Fees và xử lý Payment.

7. MVP không tự động điều chỉnh hồi tố các Student Charges đã thanh toán trước khi Student được Grant FAS.

# **R9 – Additional Features: Payment Flow & Gateway Integration**

1. Khi Parent chọn một Outstanding Invoice, System hiển thị **Net Payable** và **Available EA Balance** của Student.

2. Parent có thể bật/tắt checkbox **Use EA Balance** và nhập số tiền EA muốn sử dụng:

   * Checkbox OFF: Thanh toán toàn bộ bằng Online Payment.

   * Checkbox ON: Parent chọn số tiền EA muốn sử dụng, có thể là toàn bộ hoặc một phần.

   * EA Amount không được vượt Available EA Balance hoặc Net Payable.

3. System tự động tính **Online Payment Amount \= Net Payable − EA Amount**. Nếu Online Payment Amount \= 0, System xử lý EA Payment mà không cần chuyển sang Payment Gateway.

4. Nếu Online Payment Amount \> 0, System tạo Payment Session và **redirect Parent sang Mock Third-party Payment Gateway UI** để thực hiện giao dịch.

5. Mock Payment Gateway hỗ trợ mô phỏng **Payment Success / Failed** và redirect Parent trở lại R9 để hiển thị Payment Result.

6. Khi Payment thành công, System:

   * Trừ EA Amount đã sử dụng khỏi EA Balance.

   * Ghi nhận EA Transaction và Payment Reference.

   * Cập nhật Invoice/Student Charge thành Paid và cập nhật Outstanding Fees.

   * Hiển thị Payment Confirmation/Receipt cho Parent.

7. Nếu Payment thất bại, System không đánh dấu Invoice là Paid và phải đảm bảo EA Balance không bị trừ vĩnh viễn. Hệ thống ngăn xử lý trùng cùng một Payment Transaction.

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAqgAAADsCAYAAAC47lQPAAAozUlEQVR4Xu3dW6sk1fnHcV+A8wa89cJrwRuRAREJEQmC6IAoAcVIUFBD8DDxRIxOEjXiiCccY0LiREnE0aAZDJqJp/EcTdwex9N4Gk/zGvrPr/7+mmc/a1V1957uvfbefi8+zO5nrapadVr11KrqnsMOO+ywEQAAALCGFAEAAACgpSIAAAAAtFQEAAAAgJaKAAAAANBSEQDmavPmzaOlpaXR3r17i7JF2b59++jgwYOjAwcOFGXribbZli1bivj3jY6hb7/9dvTCCy+MTjzxxKJ8Vtqu+/fvL+KiZb3//vujU089tSgDAKyaIjBIF0t17Lr4Z0oKcv15O+KII0a33HLL6PXXXx8v94svvhhdd911RV3Mj7f7V199Nd7ur7766uicc84p6mZrNUHdtWtXcQyL2qo25/rz9qtf/Wp0xx13FPFoHgmqz9m+ddI20rbIcZ9n2udKDj/++OPRY489VtRbLVdeeWV3rt98881F2ayGEtTf//73o6uuumr8+cMPPxw99NBDo8MPP7yoCwBYmCIwqHWC+sEHHxTLldoFFvOhEat4Q2BKbLZu3VrUz0hQSyeffPLo3XffHR111FFFWdQqQT399NO7bfH111+P3nnnne5mRMmhYvNIEFfC+0bbLpfNqi9B1Q2XEtKYjCph1TbSDUWuDwBYmCIwyBe7fEFbND1u02M3XTD/9Kc/dSN6uQ6GrTRRVCKl5ED/5rJprHS5h2KWBLWWqCzSaaed1t1o7dmzpyjLVjtBVWL2j3/8o9sufcnzl19+2R0L80gUW+lLUPvcfvvt3XrnOABgYYrAoFYJ6v33399dNHnUtnIrTRQ9Yv7KK68UZdNY6XIPxVpOUG+66abusbn+zWXZaieoGkH85JNPulHEXM+UWOuR/913312UrRezJqi+qaDvAYBVUwQGTZOg+n1FXcSUAOiCd8wxxxTzeeKJJ8aPEV977bViPuYER3V1ocjl2QknnNC9K6d35jTNZ5991i0r1nHyovfa1D591iNMtV1tVSLs2IMPPjieTu1WXOt/1llndW3XeurilUd13Q5vB7UjJhsxidK7iJqH6j711FOjk046adm8NO+33357PK8HHnhgvE2nmY8uyKqTnXnmmd1omBKmuLxI+0Z1J40gqT333nvvuI3adtp3MUHVo+NnnnmmK9d2v+uuu5bNY5p9JxdddNHoxRdf7OpoeRpdj8fYvBJUH6daFx+nWnaso2Pd+0brFPdNjRI8rd8ZZ5yxLH7nnXeO992bb745Ov/884sEVfPV/OP2efzxx4tlRLMkqBop1Hx3795d1LMbbrhh9M0333T7MZeZ9qPape2mY+vJJ58c/fSnP112k6Ll1m5a1Favs48p7V8fUzo3c31tSx372nZano79PN/ICarmr9dXNN9YrkT0ueeeWxbXfjvllFOKeQEAFqIIDPLFLic6fm9v586d3UUiXvSvueaaLqYyfdbFRp+deOgioYtd3zdn9Z6jLmZaTi7LNL2TDl1I9ZhSCYQuNHqXzt8AdrudlF577bXjd+z074033ji65JJLxuv6wx/+sJvOCara/+9//7u7kF166aWjjz76qEsWLrjggvE6uh2av9uhmNvhJEq0PM3L7Y/vd3qbXnHFFeP1VBu9TaedT20k8+yzz56YoGp+t95663gfaLl5NFUXc5f50a9uJiTeYGg6tW3Hjh1dwqfYkUce2dWfdt95Or0Xqc+K+7H0o48+2sVmSVAzv0ut9vg41THq41R1fJxq+6u93jc61r1v8vJM9XMCqNFIzduJrba5EjHNx8matpPW/Y9//ON4JE//6rOSdW/HrO+cjZyg6tjQNovHWub5aZ/mMnE7dfPhdupG6Y033pg5Qb3nnntGv/nNb8bz8bu7MblX+3V86OZHn3U8KMG/+uqri3lbHEH1qHFM4LU/lITHUWJtk9V4zx4A0CkCg/oudk5Q/b6iLpqeRhcXxTT6dPTRR3d/q96PfvSjcR11/rogKDHJy5wlQb3vvvu6kb78hQZ90SHO3+3WqwOuo6ShL3bhhRd2n52g5i/S/PrXv+7iuqB6/rV2KOFwO2JiGev4m/IazVJi7G0a6+jndrxNp5mPPtcS1FloxFjt97KUPLpM66rYww8/XEzn5eqx8Y9//OMu5pErTXP88cd3sWn2XTx+4juQSmYV142BRrnmkaBqX9aOU81TbfG+yce6943ampcpSmDjEwjV037Mv4jg+TtZu/jii0cvv/xy8W6otuXnn38+PkYzn7O6iXj66acL2rbzTFDVjlrCrJvAWRPUGo1kxi/nqf35dQkdSz4Xa2KCqn2mecaEVvtDo9nxiY1uWIeeHAEA5qoIDPLFSSNW+tt0EVdH71HIGid1OV5LDqJZElSNQumi7hFPO/fcc7vp/bhef8fRRVEily/OfuTpek5Q84Uqx/V3rR2ffvrpuB19SZTraF66KE7aptPMR58PNUEVJVFKdJSoql16RUJxLUfL03bO03i5StziO3xKCjSdk5Fp9p0SBv2dRyDdBrVJ26xvm0ROUDV6Fo9lJ5YeLa3R/Cftm6FH6r5pEJ9TtYQ2PuLXMvuSLu2Pvm/Xe/5D7fEx4n1SOw9N+0P7WiOiuUw0rRLEHNfrJCtJUHUjopsUjZIqEVf74nlbS87VhnyORjFBFSWnHn0X7df4WdSmoXkCAOaqCAzyxa6vo3YiGS/Amcrfeuut8cjZJBqJ8fuG+Z3FTBee2ryd5PjCqb9zgqqLWi0WL4g5ETVdfGO8bx2dNKodfUmUR6g1r2mS82nmo8/zSFDNNxrxpkOJnrZDrW5tuU4QnYxMs++8/R955JFiOYo7WenbJrXlx0Ql6muPed8MHes1MSEUJ3z5CzgeWfX20XL6EtS+pw8yS4KqUVolZxo9zPVMiXtt1NLUxto20X6ZlKDqXI8JqkbUNWqsd1pdR/s+nqM5oZVZE1TREweN8vpn1fJ7xGr/0DwBAHNVBAZNSlD95Q1dVHKZqbz2KHeI6moaXTz1nl8ut6HHxIr7MZ6Tl5yM1mKqmxPU/Aiz9gpBrR0a6XI7+pKomFjqXTtv0/xoN7dxaD763JcoTqIvqeQvgGnEXPN2gqp117ppO+Tp+5abE9Rp9t2kR/z5/d68TWrLz4lKLK+1x7xvao/dh2h5cQTYj/LzFwD9bqS3j47BfNyJEinVy68I2CwJquatLxhpu+R9bnq/NL/iEinJ00hsTrj1Pmc8BtQmjcIee+yx45i2QUw41Y44mqv26T3mRSSo2oZ+1F/7hQLeQQWAVVUEBk1KUPVtXV1UlKwcd9xxXUwXKsV9AfZjOn2xyBcxJR61x4LmL4143s8//3w3Wqcv+dx2223jL2DpHUcnHfmLNv/5z3/GoyJOXnIyWoupbk5QdZH+29/+1rVLy9E6xS/y6H1LtyN/Scrt6EuiYmLpbafPeq3C2/S8884bb9Np5qPPThTfe++9cTIzzbf4NR9No2+Za/31aNvf7PdjUL8nq/m4jdoX8UtSkxLUafedkmHVy1+S8pfGFOvbJrXl50TFNJqoch2n+iKcYjpOnYR732i53jeKed/k+ZlGZZVkxURT21HzcKKrf5Uoal29fbT+tS9J6amClpcTQpslQRWdUzp+9SXAOHKp41hfbouvdtRof2iecURX89T7wfEY0DERbwB8jucENb4Trm/qaxssIkFV8q82Pvvss8UvLIhGhofezQUAzFURGDQpQRX/FI6/UKMLmr6JG0dk9FM9SjpUrnpKAqb54W8lVhrl8E9D6WKli2m8QOnLPKrjb1NrlEvtifNx8pKT0VpMdXOCqvW//vrru/n3/UyW2+F1VDviY8O+JConlqLpNL23qR5BepvOMh8lUf7ylLbPNN/i17orWfL8NJ2SrDzC5p8WiuurRGvaBFWm2XdKZPRf2/73v/8dHwNqT0zQ+rZJbfk5UYl8nPq/+9Rxmv+7T//sk8rVbu+bPC/TLyKozfmRvJJM7xttR+0rbbO4fbyN9YsRWp4exWuEOy8jmjVBNd2Q6KYr/pSabsR0vPSN1pq2m75Jr2k1nRJLJX3xGHByrW2nei+99FL3TfyYcF522WXjn/DSdtVPb6mti0hQPZJd+zk1ffFOyWvfTQAAYO6KAAbEBDWXAdOY5X+SWmv8X6AqEY+/4jANnTv5JmUt8X5RIpzL/J8r5DgAYGGKAAaQoGIedPxoNDLH1wONpmtEU/IXiYas9QRV751qneIrBeKfROv7WS0AwEIUAQwgQcW86N1LPfrO8Y1qrSaoevdX7dJrBrX9oVeI+C+WAWDVFQEMIEEFVmatJqj+1QK9skASCgBrRhEAAAAAWioCAAAAQEtFAAAAAGipCAAAAAAtFQEAAACgpSIAAAAAtFQEAAAAgJaKAAAAANBSEQAAAABaKgIAAABAS0UAAAAAaKkIAAAAAC0VAQAAAKClIgAAAAC0VAQAAACAlooAAAAA0FIRAAAAAFoqAgAAAEBLRQAAAABoqQgAAAAALRUBAAAAoKUiAAAAALRUBAAAAICWigAAAADQUhEAAAAAWioCAAAAQEtFAAAAAGipCAAAAAAtFQEAAACgpSIAAAAAtFQEAAAAgJaKwIayffv20QknnFDEAQAAsGYVgblSgnjw4MHR5s2bi7JFO+WUU7pl79mzpygDsPq2bt06OnDgwGj//v1FGQAAQREY5IQzWlpa6k1AVytBPeaYY0Z//etfR2+//fY4dtRRR42+/PLL0e23317Unxct9y9/+cvo/fff79bz66+/Hu3bt29cpjZddtllxXTAWuRj+dtvvx0fy0oqa+fXSiwiQX3xxRdHTz31VBHPTj755NFjjz3WrZvO1a+++mp01VVXFfWyea07APR59NFHu77p1ltvLcrWqhtuuKHrG3N8jorAoFkTzlnrr9SWLVu6i54ufrlskbRuX3zxxejaa6/tPh9xxBGjHTt2dH+7Tboo5+mAtea+++4bH8uHH374+Fjetm3b3M6vRSSoOgf37t1bxCMl26r37rvvduul2NFHH92tc66bzWvdAaDmpptuGn3zzTdd//v555+PLrzwwqLOWqR+d9euXUV8jorAoEkJ5y9/+ctupEF3Ak8++WR3gYv1tTJxxNUXrNj56+LoeWjae++9t4vrXdKPP/54HL/rrru6uirLo7reaPFvOeuss0bPPPPMeLTzzTffXNZ+X+w06qnlqF0PPvhgsZ6x/gsvvDBuh2mZtTbpYvfEE0+MPvvss27+Gq26/vrrx9Np1Fdlqq9/n3/++WIdtB10ICuufzXCk9sFzErnRe1YltqxrHM4H5s+7mP/8Nprr3Xnmo73W265pUhQlTB+8MEH41FbnaMuc92LL754PI+XX365K3PiGNulWG77qaee2pVp/frOFbXhrbfeGiey6ruOO+64rqy27oq7L9FI7CeffNL1dU5+RX2hEmLN031h7PtU98477xw/fdH5/tBDD42n17po/X/72992+0X90D333NPV1etLrueLm+ad1wvA2nbkkUd2T4HUt+lfnd/333//sjqKKS9RrqB66ivUlyoHUt+jcn2OffdQrjNN363PzoXUjzkXUo7ivC32iwvqf4rAoEkJqjprlStx0t+6G8grPZSgagOrk9Y0mlYXIA8ha9nqzJ999tnRe++91210D4erA9fjfHXUTz/99Ojmm2/u4nEn/OIXvxi3R/P133fccce4/fqsJFhlLtcBkdcz1te63njjjcviWr7b9Morr4zbpLao3e+8887oo48+Gk/vddeFzAfgp59+Oj4IvA5nn312tw20/jp4VE/z1kGT2wbMwiOoOpZzklo7v6bp5DQSoM/qC3TOaf6ahxNUHbd6PK/jWMezjusPP/ywO85V7r5B54rOB9+cKtH8wQ9+MHr88cfH56zapVher7vvvrub9rzzzivKTMmg2vDSSy+NXn311W6eapcuHrV11zTqH9Qe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>

[image2]: <data:image/png;base64,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>