# FS-01: Education Account Lifecycle Management (Requirement 1)


# R1 – Education Account Lifecycle Management


## Updated Functional Specification – Sprint 1 MVP

Version: 1.2 – BA/Dev/QA Refinement Draft.


### Decision Classification

[CR] Client Confirmed Requirement: Nội dung đã được client xác nhận.

[TD] Team Decision: Phương án implementation bạn đã trao đổi và thống nhất với Dev.

[WA] Working Assumption: Quy tắc BA đề xuất để Dev/QA có expected behavior rõ ràng; cần team chấp nhận trước khi xem là baseline.

[Deferred]: Yêu cầu đã biết nhưng chưa triển khai trong MVP hiện tại.


# 1. Detailed Functions


## 1.1. F01 – Automatic Education Account Creation & Activation


### 1.1.1. Function Description

Hệ thống tự động truy xuất Citizen Information từ Government Citizen Dataset nhằm xác định những Singapore Citizens đủ điều kiện và tạo Education Account.

[CR] Education Account là tài khoản tài chính dành cho Singapore Citizens. Account được tạo và kích hoạt khi công dân đạt 7 tuổi. Mỗi Singapore Citizen chỉ có một Education Account.

[TD] Citizen Information được đồng bộ từ Mock Government Citizen API và lưu vào internal Student Profile khi thực hiện Account Creation.

Sau khi Education Account được tạo thành công, Daily Incremental Sync không tự động đồng bộ lại các thay đổi của Existing Student Profiles.

[Deferred] Những thay đổi về Student Information sau Account Creation có thể được xử lý thông qua Manual Data Update, Bulk Re-synchronization hoặc Student Details Maintenance Function theo scope được team thống nhất.

[TD] Account Creation được triển khai theo hai cơ chế:

A. Initial Synchronization

Trong lần synchronization đầu tiên, hệ thống truy vấn Government Citizen Dataset để lấy Singapore Citizens từ đủ 7 tuổi đến dưới 16 tuổi.

Hệ thống kiểm tra required information, age eligibility và existing Education Account trước khi tạo Account.

Father/Mother NRIC không bắt buộc để tạo Education Account.

B. Daily Incremental Synchronization

Sau Initial Synchronization, hệ thống chạy Daily Scheduled Job để truy vấn những Citizens vừa đạt 7 tuổi trong ngày xử lý.

Daily Job không quét lại toàn bộ Citizen Dataset từ 7 đến dưới 16 tuổi, nhằm giảm lượng dữ liệu cần xử lý hằng ngày.

[TD – Deferred] Additional Citizen Records Handling

Đối với Citizen Records được Government Dataset bổ sung muộn nhưng không thuộc phạm vi Daily Incremental Sync, team dự kiến hỗ trợ hai cơ chế trong Sprint sau:

Manual Account Creation: Authorized Admin chủ động tạo Education Account cho từng Citizen sau khi hệ thống kiểm tra eligibility. (Next sprint)

Bulk Re-synchronization: Authorized Admin kích hoạt việc truy vấn lại Government Citizen Dataset trong nhóm tuổi từ đủ 7 đến dưới 16 để xác định và tạo những Education Accounts còn thiếu.

Cross-Function Dependency – R8

Việc Government cập nhật Father/Mother NRIC sau Account Creation không yêu cầu R1 quét lại Student.

R8 sẽ kiểm tra Parent–Student Relationship thông qua Government API khi Parent đăng nhập bằng Singpass, trước khi cho phép truy cập Education Account theo quyền.


### 1.1.2. Trigger, Schedule & Data Source



| Item | Specification |
| --- | --- |
| Primary Actor | System |
| Data Source | Government Citizen Dataset |
| Sprint 1 Integration | Mock Government Citizen API [TD] |
| Data Access | System gửi API request có kèm API credential [TD] |
| Initial Trigger | Initial Synchronization |
| Recurring Trigger | Daily Scheduled Job |
| Execution Frequency | Một lần mỗi ngày [TD] |
| Execution Time | 00:00 AM Singapore Time (SGT, UTC+8) [WA] |
| Weekends & Public Holidays | Job tiếp tục chạy |
| User Interaction | Không yêu cầu người dùng thao tác thủ công |


Data Source Clarification

Trong Sprint 1, Government Citizen Dataset là nguồn dữ liệu mô phỏng. Chưa xác nhận tích hợp trực tiếp với ICA, Myinfo hoặc một Government API thực tế.

Singpass Authentication dành cho Parent Login là một chức năng riêng, không được xem là cơ chế Daily Citizen Data Synchronization.


### 1.1.3. Citizen Data Extraction

Hệ thống truy xuất các thông tin sau từ Government Citizen Dataset:



| Field Name | Required for MVP | Business Purpose |
| --- | --- | --- |
| NRIC | Yes | Xác định Citizen duy nhất và kiểm tra Existing Education Account |
| Full Name | Yes | Nhận diện Citizen / Student |
| Date of Birth | Yes | Xác định Age Eligibility |
| Citizenship | Yes | Xác định công dân có phải Singapore Citizen |
| Gender | Yes [WA] | Thông tin cá nhân theo dataset hiện tại |
| Race | No | Thông tin cá nhân bổ sung |
| Residential Address | No | Thông tin địa chỉ nếu được cung cấp |
| Father NRIC | No | Hỗ trợ Parent–Student Relationship |
| Mother NRIC | No | Hỗ trợ Parent–Student Relationship |


Required Data Validation

NRIC không được trống và phải đáp ứng định dạng định danh được hỗ trợ.

Full Name không được trống.

DOB phải là ngày hợp lệ và không nằm trong tương lai.

Citizenship phải thuộc danh sách giá trị được hệ thống nhận diện.

Gender phải thuộc danh sách giá trị hợp lệ nếu được giữ là required field trong MVP.

Thiếu required information: không tạo Account cho Citizen Record đó, ghi nhận exception.

Thiếu optional information: không ngăn Account Creation.

Việc một field có trong Government Dataset không đồng nghĩa phải lưu trùng field đó vào Education Account.


### 1.1.4. Initial Synchronization – Main Flow



| Step | System Behavior |
| --- | --- |
| 1 | Initial Synchronization được kích hoạt khi hệ thống thực hiện lần đồng bộ đầu tiên. |
| 2 | System gửi authenticated request đến Mock Government Citizen API để truy xuất Singapore Citizens từ đủ 7 tuổi đến dưới 16 tuổi. |
| 3 | Government API trả về Citizen Records đáp ứng điều kiện truy vấn. |
| 4 | System kiểm tra required information của từng Citizen Record theo agreed data contract. Father/Mother NRIC không bắt buộc. |
| 5 | Nếu Citizen Record thiếu hoặc có required information không hợp lệ, System bỏ qua Record đó và không tạo Education Account. |
| 6 | Nếu Citizen Record hợp lệ, System tạo Student Profile và lưu Citizen Information vào internal database. |
| 7 | System tạo Education Account mới và liên kết với Student Profile vừa được tạo. |
| 8 | System khởi tạo Education Account Number duy nhất, Status = Active, Balance = SGD 0.00 và Currency = SGD. |
| 9 | System ghi nhận Account Creation Date. |
| 10 | System tiếp tục xử lý các Citizen Records còn lại cho đến khi hoàn tất Initial Synchronization. |


Implementation Notes

[TD] Initial Sync được thực hiện trên database nội bộ chưa có Student Profiles hoặc Education Accounts từ các lần đồng bộ trước.

[TD] Hệ thống chỉ lưu Student Profile và Education Account đối với Citizen Records được xử lý thành công.

[TD] Không yêu cầu lưu Processing History hoặc Processing Result cho từng Citizen Record trong Initial Sync.

[Deferred] Citizen Records không được tạo Account trong Initial Sync sẽ được xem xét xử lý thông qua Manual Account Creation hoặc Bulk Re-synchronization trong Sprint sau.

[TD] Parent–Student Relationship không phải điều kiện tạo Education Account. Việc xác minh relationship thuộc R8 khi Parent đăng nhập thông qua Singpass.


### 1.1.5. Daily Incremental Synchronization – Main Flow (Revised)



| Step | System Behavior |
| --- | --- |
| 1 | Daily Scheduled Job được tự động kích hoạt theo thời gian đã cấu hình (Singapore Time). |
| 2 | System gửi authenticated request đến Mock Government Citizen API để truy xuất Singapore Citizens vừa đạt 7 tuổi trong ngày xử lý. |
| 3 | Government API trả về Citizen Records đáp ứng điều kiện truy vấn. |
| 4 | System kiểm tra required information của từng Citizen Record theo agreed data contract. Father/Mother NRIC không bắt buộc. |
| 5 | Nếu Citizen Record thiếu hoặc có required information không hợp lệ, System bỏ qua Record đó và không tạo Education Account. |
| 6 | Nếu Citizen Record hợp lệ, System kiểm tra Citizen đã có Education Account trong internal database hay chưa bằng NRIC. |
| 7 | Nếu Education Account đã tồn tại, System bỏ qua Record và không tạo Account mới. |
| 8 | Nếu chưa có Education Account, System tạo Student Profile từ Citizen Information và lưu vào internal database. |
| 9 | System tạo Education Account mới và liên kết với Student Profile tương ứng. |
| 10 | System khởi tạo Education Account Number duy nhất, Status = Active, Balance = SGD 0.00 và Currency = SGD. |
| 11 | System ghi nhận Account Creation Date. |
| 12 | System tiếp tục xử lý các Citizen Records còn lại cho đến khi hoàn tất Daily Synchronization. |


Notes

[TD] Daily Sync chỉ truy xuất Singapore Citizens vừa đủ 7 tuổi, không quét lại toàn bộ Citizen Dataset.

[TD] Father/Mother NRIC không phải mandatory fields để tạo Education Account.

[TD] Daily Sync không tự động cập nhật Student Personal Information của các Existing Accounts.

[TD] Không yêu cầu lưu processing history của từng Citizen Record; chỉ lưu Student Profile và Education Account được tạo thành công.

[Deferred] Citizen Records được Government bổ sung muộn hoặc bị bỏ qua do thiếu required information sẽ được xử lý thông qua Manual Account Creation hoặc Bulk Re-synchronization trong Sprint sau.

[TD] Parent–Student Relationship được xác minh riêng trong R8 khi Parent đăng nhập bằng Singpass.


### 1.1.6. Age Eligibility Business Rules



| ID | Business Rule |
| --- | --- |
| F01-BR01 | Chỉ Singapore Citizens được tạo Education Account. [CR] |
| F01-BR02 | Eligible Age từ đủ 7 tuổi đến trước sinh nhật 16 tuổi. |
| F01-BR03 | Age được xác định từ DOB của Citizen, không dựa trên School Level hoặc Schooling Status. |
| F01-BR04 | Account Creation không phụ thuộc School Enrolment. |
| F01-BR05 | Citizen từ đủ 16 tuổi chưa có Account không được tạo Account mới. |


Age Calculation Examples



| Date of Birth | Processing Date | Expected Result |
| --- | --- | --- |
| 15/06/2019 | 14/06/2026 | Chưa đủ 7 tuổi, không tạo Account |
| 15/06/2019 | 15/06/2026 | Đủ 7 tuổi, eligible nếu đáp ứng các điều kiện khác |
| 15/06/2019 | 15/06/2035 | Đủ 16 tuổi, không tạo Account mới |


Leap Year Handling [WA] (cần confirm)

Đối với Citizen sinh ngày 29/02, trong năm không nhuận, sử dụng ngày 28/02 làm ngày đánh dấu đạt tuổi tương ứng để đánh giá eligibility.

Ví dụ: Citizen sinh ngày 29/02/2020 được đánh giá đạt 7 tuổi vào ngày 28/02/2027.

F01 và F02 phải dùng cùng một rule này.

1.1.7. Duplicate Account Prevention

[CR] Mỗi Singapore Citizen chỉ được có một Education Account.

[TD] NRIC được sử dụng làm Business Identifier để nhận diện Citizen/Student.

System sử dụng NRIC để tìm Student Profile và xác định Education Account đã liên kết với Student đó.



| Existing Account Condition | Expected Behavior |
| --- | --- |
| Chưa tồn tại Education Account | Tạo Account mới nếu Citizen đủ điều kiện |
| Account đang Active | Không tạo Account mới |
| Account đã Closed | Không tạo Account mới |
| Closed Account bị ẩn khỏi UI | Không tạo Account mới |
| Daily Sync xử lý lại cùng Citizen | Không tạo duplicate |


[WA] Education Account không hỗ trợ Hard Delete hoặc Soft Delete trong Sprint 1. Closed Accounts vẫn được lưu trong hệ thống.


### 1.1.8. Education Account Creation Result

Student Profile và Education Account là hai đối tượng nghiệp vụ riêng biệt.

Student Profile lưu thông tin cá nhân được truy xuất từ Government Citizen Dataset.

Education Account lưu thông tin phục vụ quản lý tài khoản tài chính và được liên kết với Student Profile tương ứng.

Khi tạo thành công:



| Account Information | Expected Result |
| --- | --- |
| Education Account Number | Mã tài khoản duy nhất do hệ thống tạo |
| Account Holder Reference | Liên kết với đúng Student Profile (Student id) |
| Account Status | Active |
| Account Balance | SGD 0.00 |


Hệ thống không bắt buộc lưu lại Full Name, DOB, Citizenship hoặc Address vào Education Account nếu các thông tin đó đã có trong Student Profile và có thể truy xuất thông qua Account Holder Reference.

Function Ownership: F01 tạo Account và relationship với Student. F08 chịu trách nhiệm lấy và hiển thị Account Details cho Parent.


### 1.1.9. Job Failure & Recovery (next sprint)

Proposed Operational Rules [WA]



| Scenario | Expected Behavior |
| --- | --- |
| Government API Authentication Failure | Không tiếp tục xử lý dữ liệu; ghi nhận Job Failure |
| Government API Timeout | Ghi nhận lỗi và retry |
| First Job Failure | Retry một lần sau 15 phút |
| Retry Failure | Ghi nhận Failed; chờ scheduled job tiếp theo |
| Missed Processing Date | Lần chạy tiếp theo phải xử lý các ngày bị bỏ lỡ |
| Individual Citizen Record Invalid | Skip Record, ghi nhận lý do, tiếp tục xử lý các Records còn lại |
| Account Creation Failure | Ghi nhận failure; không lưu Account incomplete |
| Job chạy lại | Không tạo duplicate Account |


Recovery Principle

Hệ thống cần xác định dữ liệu đã xử lý thành công và dữ liệu còn thiếu để retry an toàn. Một Job hoàn tất một phần không được khiến các Citizen Records chưa xử lý bị bỏ sót vĩnh viễn.


### 1.1.10. Alternative & Exception Flows



| ID | Description |
| --- | --- |
| AF01 | Scenario: Citizen không phải Singapore Citizen. System Behavior: Không tạo Education Account. |
| AF02 | Scenario: Citizen chưa đủ 7 tuổi hoặc đã đủ 16 tuổi. System Behavior: Không tạo Education Account. |
| AF03 | Scenario: Citizen đã có Education Account, kể cả Closed. System Behavior: Bỏ qua Account Creation. |
| AF04 | Scenario: Citizen không có Father/Mother NRIC. System Behavior: Vẫn tạo Account nếu đủ eligibility. |
| EF01 | Scenario: Government API Authentication Failure. System Behavior: Ghi nhận Job Failure và thực hiện failure handling. |
| EF02 | Scenario: Missing or Invalid Required Data. System Behavior: Không tạo Account cho Record đó; ghi nhận exception. |
| EF03 | Scenario: Duplicate Citizen Records có dữ liệu mâu thuẫn. System Behavior: Không tạo duplicate; ghi nhận Data Conflict. [WA] |



### 1.1.11. Acceptance Criteria



| ID | Test Scenario | Expected Result |
| --- | --- | --- |
| F01-AC01 | Initial Sync – Singapore Citizen 10 tuổi chưa có Account | Tạo một Active Account, Balance = SGD 0.00 |
| F01-AC02 | Daily Sync – Singapore Citizen vừa đủ 7 tuổi | Tạo Account nếu chưa tồn tại |
| F01-AC03 | Non-Singapore Citizen / Permanent Resident | Không tạo Account |
| F01-AC04 | Citizen dưới 7 tuổi | Không tạo Account |
| F01-AC05 | Citizen đã đủ 16 tuổi | Không tạo Account mới |
| F01-AC06 | Citizen đã có Active Account | Không tạo duplicate |
| F01-AC07 | Citizen đã có Closed Account | Không tạo Account mới |
| F01-AC08 | Missing Required Information | Không tạo Account |
| F01-AC09 | Missing Father/Mother NRIC | Account vẫn được tạo nếu các điều kiện khác hợp lệ |
| F01-AC10 | Student lưu ban hoặc học muộn | Eligibility vẫn dựa trên DOB |
| F01-AC12 | Job chạy lại trên Records đã thành công | Không tạo duplicate Education Account |
| F01-AC13 | Job chạy cuối tuần hoặc ngày lễ | Vẫn thực hiện theo daily schedule |
| F01-AC14 | Citizen sinh 29/02 | Eligibility xử lý theo Leap Year Rule [WA] |
| F01-AC15 | Eligible Citizen với required data đầy đủ, Father/Mother NRIC trống | Tạo Student Profile và một Active Education Account liên kết đúng Student; lưu Citizen Information được cung cấp. |
| F01-AC16 | Government cập nhật Address của Student 10 tuổi đã có Account | Daily Sync không truy xuất lại Student này và không tự động cập nhật Address. |



## 1.2. F02 – Automatic Education Account Closure


# 1.2. F02 – Automatic Education Account Closure


## 1.2.1. Function Description

[CR] Education Account được đóng khi Account Holder đạt 16 tuổi.

[TD] Hệ thống áp dụng Backend-Triggered Closure Eligibility Check và không lưu Scheduled Closure Date.

Bất kỳ backend action nào cần truy xuất hoặc xử lý Education Account đều phải thực hiện Closure Eligibility Check trước khi tiếp tục xử lý yêu cầu.

Trong quá trình kiểm tra, hệ thống gọi Mock Government Citizen API để lấy Citizen Information hiện tại của Account Holder, tập trung vào hai điều kiện:

Age: Account Holder đã đạt 16 tuổi.

Citizenship: Account Holder không còn là Singapore Citizen.

Nếu ít nhất một trong hai điều kiện trên xảy ra, hệ thống thực hiện Account Closure Processing theo các business rules tương ứng.

Nếu Account Holder chưa đủ 16 tuổi và vẫn là Singapore Citizen, Account tiếp tục Active.

Closure Eligibility Check chỉ sử dụng Government Data để đánh giá điều kiện đóng Account. Những thay đổi khác trong Citizen Information không được F02 tự động đồng bộ vào Student Profile nội bộ.


## 1.2.2. Trigger & Data Source



| Item | Specification |
| --- | --- |
| Primary Actor | System |
| Trigger | Bất kỳ backend action nào cần truy xuất hoặc xử lý Education Account |
| Data Source | Education Account, linked Student Profile và Mock Government Citizen API |
| Citizen Identification | NRIC của Account Holder |
| Closure Eligibility | Age >= 16 OR Citizenship không còn là Singapore Citizen |
| Age Evaluation | Dựa trên Current DOB lấy từ Government API |
| Citizenship Evaluation | Dựa trên Current Citizenship lấy từ Government API |
| Closure Check Timing | Trước khi backend action tiếp tục xử lý |
| Scheduled Closure Date | Không lưu [TD] |
| Student Data Synchronization | Không cập nhật toàn bộ Student Profile trong F02 [TD] |
| Pending Transactions | Giả định không có tại thời điểm closure [TD] |


Backend Actions requiring Closure Eligibility Check

Bao gồm nhưng không giới hạn:

Parent xem Education Account Details.

Parent xem Account Balance hoặc Transaction History.

MOE HQ User truy xuất Education Account.

Top-Up request, bao gồm Batch Top-Up nếu function đó truy cập Account.

Payment request.

Các backend actions khác truy xuất hoặc xử lý Education Account.

Đối với Account đã Closed, hệ thống không thực hiện closure lần nữa và áp dụng các quy tắc truy cập dành cho Closed Account.

Đối với Financial Actions, Closure Eligibility Check phải hoàn tất trước khi hệ thống quyết định cho phép giao dịch.


## 1.2.3. Main Flow



| Step | System Behavior |
| --- | --- |
| 1 | Backend nhận action cần truy xuất hoặc xử lý Education Account. |
| 2 | System xác định Education Account liên quan. |
| 3 | System kiểm tra Account Status. Nếu Account đã Closed, không thực hiện closure lần nữa và xử lý action theo quyền read-only hoặc từ chối financial operation. |
| 4 | Nếu Account chưa Closed, System xác định NRIC của Account Holder thông qua linked Student Profile. |
| 5 | System gọi Mock Government Citizen API để lấy Current DOB và Citizenship của Account Holder. |
| 6 | System xác định Account Holder đã đủ 16 tuổi hay chưa dựa trên Current DOB. |
| 7 | System kiểm tra Account Holder còn là Singapore Citizen hay không. |
| 8 | Nếu Account Holder chưa đủ 16 tuổi và vẫn là Singapore Citizen, Account tiếp tục Active; backend action tiếp tục theo các business rules của function tương ứng. |
| 9 | Nếu Account Holder đã đủ 16 tuổi hoặc không còn là Singapore Citizen, System bắt đầu Account Closure Processing. |
| 10 | System không cho phép financial transaction mới tiếp tục trong khi xử lý closure. |
| 11 | System kiểm tra các điều kiện cần thiết để hoàn tất closure, bao gồm Pending Transaction assumption và Remaining Balance Handling. |
| 12 | Nếu closure có thể hoàn tất, System cập nhật Account Status = Closed và ghi nhận Actual Closure Date. |
| 13 | System tiếp tục hoặc từ chối backend action theo kết quả Closure Processing và Account Status mới nhất. |


Notes

[TD] F02 sử dụng Current Government DOB và Citizenship, không chỉ sử dụng thông tin đã lưu tại Account Creation.

[TD] F02 không tự động cập nhật các Student Personal Information khác như Full Name, Address, Gender, Race hoặc Parent NRIC.

[TD] Existing Closed Account không được thực hiện duplicate closure.

[WA] Nếu không thể xác minh eligibility hoặc hoàn tất closure, system không được coi Account là đã đóng thành công. Financial operations cần xử lý theo agreed failure rules.


## 1.2.4. Closure Business Rules



| ID | Business Rule |
| --- | --- |
| F02-BR01 | Education Account phải được đóng khi Account Holder đạt 16 tuổi. [CR] |
| F02-BR02 | Bất kỳ backend action nào truy xuất hoặc xử lý Education Account đều phải đi qua Closure Eligibility Check. [TD] |
| F02-BR03 | Hệ thống sử dụng Current DOB và Citizenship từ Government Citizen API để đánh giá Closure Eligibility. [TD] |
| F02-BR04 | Nếu Account Holder đã đủ 16 tuổi, System thực hiện closure processing. [CR về điều kiện tuổi] |
| F02-BR05 | Nếu Account Holder không còn là Singapore Citizen, System thực hiện closure processing. [TD – cần business/client confirmation] |
| F02-BR06 | Nếu Account Holder dưới 16 tuổi và vẫn là Singapore Citizen, Account tiếp tục Active. [TD] |
| F02-BR07 | Age được xác định theo DOB, không dựa vào School Level, Cohort, Class hoặc Schooling Status. |
| F02-BR08 | Không lưu Scheduled Closure Date. [TD] |
| F02-BR09 | Giả định không có Pending Transactions tại thời điểm closure. [TD] |
| F02-BR10 | Closed Account không được thực hiện Financial Transactions mới. [WA] |
| F02-BR11 | Closed Account và Transaction History được giữ lại để phục vụ authorized viewing và audit. [TD] |
| F02-BR12 | Repeated Account Access không được thực hiện duplicate closure. [TD] |
| F02-BR13 | Closure Eligibility Check không tự động cập nhật Student Personal Information trong internal Student Profile. [TD] |
| F02-BR14 | Nếu Government API không trả về thông tin hợp lệ để xác minh eligibility, hệ thống không được tự kết luận Account đủ điều kiện đóng. [WA] |


Account Closure Processing – MVP Implementation

Mọi backend action liên quan đến Education Account phải áp dụng cùng một Closure Eligibility Check.

System sử dụng dữ liệu mới nhất từ Government API để xác định Age và Citizenship Eligibility trước khi tiếp tục Account Action.

Account có thể được xác định là đủ điều kiện đóng do đạt 16 tuổi hoặc không còn Singapore Citizen.

Account Status chỉ được cập nhật thành Closed khi các điều kiện hoàn tất closure đã được đáp ứng.

Account Status được cập nhật khi có backend action liên quan đến Account, không nhất thiết ngay tại thời điểm Government Data thay đổi nếu không có backend activity.


## 1.2.5. Closure Date Examples



| Current Government DOB | Backend Access Date | Current Citizenship | Expected Result |
| --- | --- | --- | --- |
| 10/10/2018 | 09/10/2034 | Singapore Citizen | Chưa đủ 16 tuổi, Account tiếp tục Active |
| 10/10/2018 | 10/10/2034 | Singapore Citizen | Đủ 16 tuổi, thực hiện closure processing |
| 10/10/2018 | 15/12/2034 | Singapore Citizen | Đã quá 16 tuổi, thực hiện closure processing khi Account được truy cập |
| 10/10/2018 | 10/10/2030 | Không còn Singapore Citizen | Thực hiện citizenship-based closure processing [TD] |
| 10/10/2018 | Sau khi Account đã Closed | Bất kỳ | Không thực hiện closure lần nữa |


Leap Year Handling [WA]

Đối với Citizen sinh ngày 29/02, trong năm không nhuận, sử dụng ngày 28/02 để đánh giá mốc tuổi tương ứng. F01 và F02 phải sử dụng cùng một rule.


## 1.2.6. Citizenship Changes & Student Data Updates

[TD] Citizenship-Based Closure Eligibility

Khi backend action liên quan đến Education Account được thực hiện, F02 truy vấn Government Citizen API để lấy Citizenship Status hiện tại của Account Holder.

Nếu Government Data cho thấy Account Holder không còn là Singapore Citizen, System thực hiện Account Closure Processing theo Team Decision hiện tại.

Điều kiện đóng Account do mất Singapore Citizenship chưa được xác nhận rõ trong Client Requirement ban đầu và cần được business/client confirmation.

[TD] Student Data Synchronization Boundary

F02 sử dụng Government Citizen Information cho mục đích Closure Eligibility Check, không thực hiện full synchronization của Student Profile.

Các thay đổi Government Data không liên quan trực tiếp đến Closure Eligibility, ví dụ Full Name, Address, Gender, Race hoặc Parent/Guardian Information, không được F02 tự động cập nhật vào internal Student Profile.

Việc xác minh Parent–Student Relationship thuộc R8 khi Parent đăng nhập bằng Singpass.

[Deferred] Việc cập nhật các Student Details khác sau Account Creation có thể được xử lý thông qua Student Details Maintenance hoặc Manual/Bulk Data Update khi các chức năng tương ứng được triển khai.


## 1.2.7. Pending Transactions & Remaining Balance

Pending Transactions

[TD] Team giả định không có Pending Transactions tại thời điểm Account Closure.

Financial Functions cần thực hiện Closure Eligibility Check trước khi cho phép transaction mới.

F02 không xây dựng Pending Transaction Reconciliation riêng trong Sprint 1.

Remaining Balance

[CR] Khi Education Account đóng ở tuổi 16, remaining balance phải được chuyển sang CPF.

[Deferred] CPF Transfer chưa được triển khai trong MVP hiện tại.



| Account Condition | Proposed MVP Behavior |
| --- | --- |
| Account đủ điều kiện đóng, Balance = SGD 0.00 | Cho phép hoàn tất closure |
| Account đủ điều kiện đóng, Balance > SGD 0.00, CPF Transfer chưa triển khai | Không giả định CPF Transfer đã thành công; Closure Deferred, giữ Balance và ngăn financial operations mới [WA] |
| Account đóng do mất Citizenship trước 16 tuổi | Closure được kích hoạt theo [TD]; cách xử lý Remaining Balance chưa được business xác nhận |
| CPF Transfer được triển khai và thành công theo applicable business rule | Hoàn tất closure theo quy trình tài chính được xác nhận |


Important: Citizenship-Based Closure không được mặc định sử dụng CPF Transfer Rule dành cho Age-Based Closure nếu chưa có business confirmation.


## 1.2.8. Alternative & Exception Flows



| ID | Description |
| --- | --- |
| AF01 | Scenario: Account Holder dưới 16 tuổi và vẫn là Singapore Citizen. System Behavior: Account tiếp tục Active; backend action được xử lý theo function tương ứng. |
| AF02 | Scenario: Account đã Closed. System Behavior: Không thực hiện duplicate closure; authorized viewing được phép, financial actions bị từ chối. |
| AF03 | Scenario: Parent hoặc MOE HQ User truy cập Account của Student đã đủ 16 tuổi. System Behavior: System kiểm tra Government Data và thực hiện closure processing trước khi trả Account Information. |
| AF04 | Scenario: Government Data cho thấy Account Holder không còn Singapore Citizen. System Behavior: System thực hiện citizenship-based closure processing theo Team Decision. |
| AF05 | Scenario: Payment hoặc Top-Up được gọi trên Account đã đủ điều kiện đóng. System Behavior: System thực hiện Closure Eligibility Check và không cho financial transaction mới tiếp tục. |
| EF01 | Scenario: Government API không phản hồi hoặc trả về lỗi. System Behavior: Không kết luận closure eligibility khi chưa xác minh được; ghi nhận technical error và không cho financial operation cần eligibility verification tiếp tục. [WA] |
| EF02 | Scenario: Government API không trả về Citizen Record hợp lệ. System Behavior: Không tự động đánh dấu Account Closed; trả kết quả lỗi phù hợp để backend action xử lý. [WA] |
| EF03 | Scenario: Closure Processing thất bại. System Behavior: Không ghi nhận closure thành công; bảo đảm Account Status và Balance không bị cập nhật sai. |
| EF04 | Scenario: Account đủ điều kiện đóng nhưng Remaining Balance > 0 và CPF Transfer chưa triển khai. System Behavior: Xử lý theo Closure Deferred rule nếu được team chấp nhận. [WA] |
| EF05 | Scenario: Government cập nhật các Student Details không liên quan đến Closure Eligibility. System Behavior: F02 không tự động đồng bộ các fields này vào Student Profile. |



## 1.2.9. Acceptance Criteria



| ID | Test Scenario | Expected Result |
| --- | --- | --- |
| F02-AC01 | Parent xem Account của Student 15 tuổi vẫn là Singapore Citizen | Account tiếp tục Active. |
| F02-AC02 | Parent xem Account của Student vừa đủ 16 tuổi, Balance = SGD 0.00 | Backend kiểm tra Government Data và cập nhật Account thành Closed. |
| F02-AC03 | MOE HQ truy xuất Account đã quá 16 tuổi nhưng vẫn Active, Balance = SGD 0.00 | System thực hiện closure trước khi trả Account Information. |
| F02-AC04 | Top-Up request trên Account đã đủ 16 tuổi | Không thực hiện Top-Up. |
| F02-AC05 | Payment request trên Account đã đủ 16 tuổi | Không thực hiện Payment. |
| F02-AC06 | Closed Account được truy cập lại | Không thực hiện duplicate closure, không thay đổi Actual Closure Date. |
| F02-AC07 | Authorized Parent xem Closed Account | Có thể xem thông tin/lịch sử được phép, không thực hiện giao dịch. |
| F02-AC08 | Student lưu ban hoặc học muộn | Closure Eligibility không phụ thuộc School Level. |
| F02-AC09 | Government API thất bại khi thực hiện Closure Eligibility Check | Không cập nhật Account thành Closed khi chưa xác minh; financial operations xử lý theo failure rule. [WA] |
| F02-AC10 | Account đủ điều kiện đóng, Balance > 0, CPF chưa triển khai | Xử lý theo agreed Remaining Balance Rule; không giả định CPF Transfer đã thành công. |
| F02-AC11 | Government Data thay đổi Citizenship thành Non-Singapore Citizen khi Student dưới 16 tuổi | Backend phát hiện thay đổi và kích hoạt citizenship-based closure processing. [TD] |
| F02-AC12 | Government Data cập nhật DOB khiến Student đủ 16 tuổi | F02 dùng Current Government DOB để xác định Closure Eligibility. |
| F02-AC13 | Government Data cập nhật Address hoặc Gender sau Account Creation | F02 không tự động cập nhật các thông tin này vào internal Student Profile. |
| F02-AC14 | Financial Action truy cập Account đã đến hạn closure nhưng persisted Status vẫn Active | Closure Eligibility Check phải xảy ra trước khi financial transaction được thực hiện. |
| F02-AC15 | Student sinh ngày 29/02 và đạt mốc tuổi 16 theo agreed Leap Year Rule | System đánh giá Closure Eligibility đúng mốc tuổi được thống nhất. [WA] |



# 2. Business Data & Fields


## 2.1. Student Information

Student Information được truy xuất từ Government Citizen Dataset và lưu vào internal Student Profile khi Education Account được tạo thành công.

Internal Student Profile lưu dữ liệu đã đồng bộ tại thời điểm Account Creation và không được tự động cập nhật mỗi khi Government Dataset thay đổi.

[TD] Government Data Usage

F01 truy xuất Citizen Data phục vụ Account Creation.

F02 truy xuất Current Government DOB và Citizenship phục vụ Closure Eligibility Check.

R8 truy xuất Government Data khi Parent đăng nhập để xác minh Parent–Student Relationship.

Việc F02 hoặc R8 truy vấn Government API không đồng nghĩa toàn bộ Student Information trong internal Student Profile được refresh.

[Deferred] Student Information Updates

Các thay đổi khác của Student Information sau Account Creation được xử lý qua Student Details Maintenance hoặc Manual/Bulk Data Update khi được triển khai.



| Field Name | Required | Business Description |
| --- | --- | --- |
| Citizen Identifier (NRIC) | Yes | Mã định danh duy nhất của Citizen, dùng để nhận diện Student và kiểm tra Education Account đã tồn tại. |
| Full Name | Yes | Họ và tên đầy đủ của Student. |
| Date of Birth | Yes | Ngày sinh của Student, sử dụng để xác định điều kiện tuổi 7 khi tạo Account và tuổi 16 khi đóng Account. |
| Citizenship | Yes | Tình trạng quốc tịch, dùng để xác định Singapore Citizen có đủ điều kiện sở hữu Education Account. |
| Gender | Yes [TD – Data Design] | Giới tính của Student, được lưu trong Student Profile theo data contract hiện tại của Dev. |
| Student Profile Status | System-managed [TD] | Trạng thái của Student Profile, độc lập với Education Account Status. |
| Race | No | Thông tin chủng tộc, được lưu nếu có trong Government Dataset. |
| Block | No | Số Block trong địa chỉ cư trú. |
| Street | No | Tên đường trong địa chỉ cư trú. |
| Unit | No | Số căn hộ hoặc Unit trong địa chỉ cư trú. |
| Postal Code | No | Mã bưu chính. |
| Country | No | Quốc gia cư trú. |
| Father NRIC | No | Mã định danh của cha, hỗ trợ Parent–Student Relationship. |
| Mother NRIC | No | Mã định danh của mẹ, hỗ trợ Parent–Student Relationship. |


Business Rules

NRIC là Business Identifier dùng để nhận diện Citizen/Student.

DOB và Citizenship được dùng để đánh giá Account Eligibility.

Full Name và Gender là required information theo data contract Dev hiện tại; Gender không phải điều kiện để xác định độ tuổi hoặc quốc tịch.

Missing required information: Student Record không được dùng để tạo Education Account và phải ghi nhận exception.

Missing optional information: không ngăn việc tạo Education Account.

Father NRIC và Mother NRIC được sử dụng để hỗ trợ linking trong F08.

Student Profile có thể tồn tại mà không có Education Account, ví dụ Permanent Resident hoặc Foreign Student.

School, Level, Cohort và Class không phải điều kiện bắt buộc để tạo Education Account.

Note: Student Profile Status được hệ thống quản lý riêng. Nó không đại diện cho việc Education Account đang Active hay Closed.


## 2.2. Education Account Information

[TD] Account Closure Eligibility

Education Account được liên kết với Student Profile để nhận diện Account Holder.

Khi có backend action liên quan đến Education Account, hệ thống dùng NRIC của Account Holder để truy vấn Government Citizen API và đánh giá Current DOB và Citizenship.

Education Account không cần lưu Scheduled Closure Date.



| Field Name | Required | Business Description |
| --- | --- | --- |
| Education Account Number | Yes | Số tài khoản giáo dục duy nhất, được tạo tự động khi Account Creation thành công. |
| Account Holder Reference | Yes | Mối liên kết giữa Education Account và Student Profile sở hữu Account. |
| Account Balance | Yes | Số dư hiện tại của Education Account, được khởi tạo bằng SGD 0.00. |
| Account Status | Yes | Trạng thái của Education Account, gồm Active và Closed trong MVP. |


Business Rules

Mỗi Singapore Citizen chỉ được sở hữu một Education Account.

Education Account phải được liên kết với đúng Student Profile.

Account mới được tạo với Status = Active và Balance = SGD 0.00. [WA về initial balance]

Closed Account vẫn được lưu để phục vụ Historical Viewing và Audit. [TD]

Closed Account không được sử dụng cho Financial Transactions mới. [WA]

Account Holder Full Name, DOB, Citizenship và Address có thể được truy xuất từ Student Profile, không cần lưu trùng vào Education Account.

Theo Team Decision hiện tại, Education Account không lưu Scheduled Closure Date; Backend thực hiện Closure Eligibility Check khi có action truy xuất hoặc xử lý Account.

Note: Những thông tin được hiển thị trên Account Details Screen thuộc phạm vi F08. Không mặc định rằng mọi thông tin của Student Profile đều phải hiển thị cho Parent hoặc MOE HQ User.


## 2.3. Education Account Transaction Information

Purpose: Ghi nhận lịch sử các giao dịch tài chính liên quan đến Education Account.



| Field Name | Required | Business Description |
| --- | --- | --- |
| Transaction Reference Number | Yes | Mã tham chiếu duy nhất của giao dịch. |
| Related Education Account | Yes | Education Account phát sinh giao dịch. |
| Transaction Direction | Yes | Xác định giao dịch làm tăng hoặc giảm Account Balance. |
| Transaction Amount | Yes | Số tiền giao dịch bằng SGD. |
| Transaction Status | Yes | Kết quả xử lý giao dịch, ví dụ Success hoặc Failed. |
| Transaction Description | No | Nội dung hoặc mục đích giao dịch. |
| Transaction Date | Yes | Thời điểm giao dịch được ghi nhận. |
| Transaction Type | Proposed | Phân loại nghiệp vụ Top-Up, Payment hoặc CPF Transfer khi các functions liên quan được triển khai. |


Business Rules

Successful incoming transaction làm tăng Account Balance.

Successful outgoing transaction làm giảm Account Balance.

Failed Transaction không làm thay đổi Account Balance. [WA]

Transaction History phải được giữ lại khi Education Account đã Closed. [TD]

Monetary values phải chính xác đến 2 chữ số thập phân theo SGD.

Negative Account Balance không được hỗ trợ trong MVP. [WA]

Transaction Type là field đề xuất để phân biệt mục đích giao dịch; cần thống nhất với nhóm Dev phụ trách Top-Up/Payment nếu chưa có trong design.

Scope Note: F01 không chịu trách nhiệm tạo Transaction khi khởi tạo Account với Balance = SGD 0.00, trừ khi team quyết định có opening transaction. [WA]


# 3. Cross-Function Boundaries



| Function | Responsibility |
| --- | --- |
| F01 – Account Creation | Initial/Daily Government Citizen Data Extraction, Required Data Validation, Student Profile Creation, Education Account Creation |
| F02 – Account Closure | Backend-Triggered Government Closure Eligibility Check dựa trên Current DOB và Citizenship; Account Closure Processing |
| R8 – Parent Authentication & Relationship Verification | Singpass Login, Parent NRIC Identification, Government API Parent–Student Relationship Verification |
| Account Details Viewing | Hiển thị Student Information và Education Account Information từ internal database theo authorization |
| Top-Up / Payment | Financial Transaction Processing và áp dụng F02 Closure Eligibility Check trước financial operations |
| Future Manual Account Creation | Tạo missing Education Account cho từng Citizen theo authorized action |
| Future Bulk Re-synchronization | Truy vấn lại Citizens từ đủ 7 đến dưới 16 tuổi để tạo missing Education Accounts |
| Future Student Details Maintenance | Cập nhật những thay đổi Student Personal Information không được tự động đồng bộ bởi F01/F02 |
| CPF Transfer | Deferred trong MVP hiện tại |


Data Ownership & Synchronization Boundary

F01 chịu trách nhiệm lưu Citizen Information trong quá trình Account Creation.

F02 sử dụng Current Government Data để đánh giá Account Closure Eligibility, nhưng không tự động cập nhật các Student Details khác vào internal Student Profile.

R8 xác minh Parent–Student Relationship khi Parent đăng nhập và không mặc định thực hiện full Student Data Synchronization.

Các chức năng cập nhật Student Details sau Account Creation được quản lý riêng và không thuộc phạm vi F02.


# 4. Delivery Limitations

[TD] Incremental Synchronization Scope

Daily Incremental Synchronization chỉ xử lý Citizen Records vừa đạt 7 tuổi.

Những Citizen Records được Government Dataset bổ sung muộn hoặc thay đổi Citizenship sau Initial Sync không được F01 Daily Job tự động xử lý nếu không thuộc nhóm truy vấn.

Manual Account Creation và Bulk Re-synchronization được dự kiến triển khai trong Sprint sau. [Deferred]

[TD] Backend-Triggered Closure

F02 kiểm tra Government Data hiện tại khi có backend action cần truy xuất hoặc xử lý Education Account.

Account Status được cập nhật thông qua Closure Processing tại thời điểm backend action được thực hiện, không nhất thiết ngay khi Government Data thay đổi nếu không có backend activity.

[TD] Student Data Synchronization Boundary

F02 chỉ sử dụng Government Data để kiểm tra Current Age và Citizenship phục vụ Account Closure Eligibility.

Những thay đổi khác của Student Personal Information không được tự động cập nhật vào internal Student Profile.

Parent–Student Relationship được xác minh thông qua R8 khi Parent đăng nhập Singpass.

[Deferred] Student Details Maintenance

Manual/Bulk Data Update và Student Details Maintenance không thuộc phạm vi Sprint 1 MVP.

[Deferred] CPF Transfer

CPF Transfer chưa được triển khai. Closure Processing khi Account còn Remaining Balance phải tuân theo agreed MVP handling rules; không được coi CPF Transfer là đã thực hiện thành công.

[Open Business Decision] Citizenship-Based Closure Financial Handling

Citizenship Change được Team Decision đưa vào Closure Eligibility. Tuy nhiên, business rule về xử lý Remaining Balance và CPF đối với Account đóng do mất Citizenship cần được xác nhận.

[WA] Other Operational Rules

Leap Year Handling, một số Failure Handling Rules và Remaining Balance Closure Deferred Rule vẫn là Working Assumptions cho đến khi team thống nhất.

