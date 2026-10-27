# **R3 – School, Student & Fee Structure Management**

## **1\. Overview**

Hệ thống cho phép **MOE HQ Users và School Users** quản lý dữ liệu về Schools, Levels/Cohorts, Classes, Students và Fee Structures thông qua Admin Portal.

Các dữ liệu này tạo nền tảng cho việc xác định thông tin học sinh, tổ chức lớp học, quản lý các khoản phí giáo dục và hỗ trợ các chức năng liên quan như Top-Up, Fee Payment và Financial Assistance.

Singaporean Students có thể sử dụng số dư trong Education Account để thanh toán các khoản phí giáo dục.

Education Account lifecycle độc lập với School Enrolment. Việc học sinh chuyển trường, đổi lớp hoặc thay đổi schooling status không tự động làm thay đổi Education Account Status.

## **2\. Confirmed Requirements**

| Confirmed Requirement |
| ----- |
| MOE HQ Users và School Users cần có khả năng maintain thông tin Schools, Levels/Cohorts, Classes và Students in each class. |
| Hệ thống cần hỗ trợ quản lý Fee Types và Fee Components payable by students. |
| Singaporean Students có thể sử dụng Education Account Balance để thanh toán education-related fees. |
| Level và Cohort được xem là cùng một khái niệm; cách gọi có thể khác nhau giữa các trường. Ví dụ: Primary 1, Primary 2\. |
| MOE HQ Users có thể manage toàn bộ các records thuộc phạm vi quản lý được thảo luận. |
| School Users chỉ được edit dữ liệu từ Level trở xuống. Chi tiết quyền với từng entity, đặc biệt Fee Types và Fee Components, cần tiếp tục làm rõ. |
| Schooling Status, School Enrolment và Education Account Status là các khái niệm độc lập. Thay đổi enrolment không tự động thay đổi Education Account Status. |

**Additional Client Clarification – Fee Structure**

Client đã đưa ra các ví dụ về những khoản phí có thể phát sinh:

* School Fees và Miscellaneous Fees.  
* Extracurricular Activities, ví dụ Music Classes hoặc School Trips.  
* Ad-hoc Charges, ví dụ phí phát sinh do học sinh làm hư hỏng tài sản.

Client cũng thể hiện mong muốn Fee Components có thể reusable giữa nhiều Fee Types, ví dụ GST. Tuy nhiên, đây là **preferred capability / nice-to-have**, chưa phải mandatory requirement.

**Meeting references:**

* Client yêu cầu giải thích use case thực tế cho Fee Assignment.  
* Clarify Level \= Cohort.  
* Clarify MOE HQ và School User permissions.  
* Clarify School Enrolment độc lập với Education Account Status.  
* Discuss reusable Fee Components, ví dụ GST.  
* Client cung cấp ví dụ Fee Categories và Ad-hoc Charges.

## **3\. Requirement Gaps \+ Proposed Solutions**

| Gap / Open Question | Proposed Solution |
| ----- | ----- |
| Student và School Records được tạo thủ công hay lấy từ external data source? Nguồn nào là source of truth? | Đề xuất sử dụng mock student/school dataset trong Sprint 1, với stable identifiers để hỗ trợ R1, R8 và R9. Cần thống nhất source of truth và ownership trước khi thiết kế data synchronization. |
| Relationship và cardinality giữa School, Level/Cohort, Class và Student như thế nào? | Đề xuất hierarchy School → Level/Cohort → Class → Student. Mỗi Student có một current class assignment tại một thời điểm trong mock-up. Cần làm rõ trường hợp transfer, multiple enrolments và historical records. |
| School Users được phép Create, View, Update và Delete những records nào? Có được quản lý Fee Types/Components hay chỉ Level, Class và Student? | Đề xuất Role-Based Access Control, với MOE HQ có phạm vi quản lý toàn hệ thống và School Users chỉ quản lý dữ liệu thuộc trường được phân quyền. Cần xác nhận permission matrix theo entity và action. |
| "Maintain Fee Types and Components" chỉ bao gồm cấu hình fee structure hay còn bao gồm Assign/Charge Fees cho Student? Nếu có Fee Assignment, business flow thực tế là gì? | Đề xuất tách Fee Structure Configuration khỏi Student Billing/Charge Assignment. Không mặc định triển khai Fee Assignment trước khi xác định use case, actor, trigger và relationship với R9. |
| Các Fee Types và Fee Components cụ thể là gì? Mỗi loại có những required attributes nào? | Đề xuất Fee Type gồm Code, Name, Description, Status; Fee Component gồm Code, Name, Calculation Type, Amount/Rate, Effective Period. Danh sách fields và calculation rules cần xác nhận. |
| Một Fee Component có thể được sử dụng ở nhiều Fee Types hay không? Nếu thay đổi common component thì các Fee Types liên quan bị ảnh hưởng thế nào? | Đề xuất reusable Fee Components, nhưng chỉ triển khai sau khi đánh giá business value và effort với Dev. Nếu chọn triển khai, cần rule về shared changes, effective dates và versioning. |
| Quy trình Student Enrolment, Class Assignment, Class Transfer, School Transfer và Progression hoạt động như thế nào? | Đề xuất quản lý current enrolment và lưu enrolment history. Không tự động progression hoặc transfer trước khi client xác nhận business rules. |
| Fees được áp dụng theo School, Level/Cohort, Class, Student hay kết hợp nhiều đối tượng? Có hỗ trợ recurring và ad-hoc charges không? | Đề xuất cấu hình fee applicability theo từng scope, nhưng cần xác nhận trigger, charging frequency và exceptions trước khi triển khai billing logic. |
| Khi Fee Structure thay đổi, thay đổi đó áp dụng cho charges hiện tại, tương lai hay cả outstanding charges? | Đề xuất effective-dated Fee Configuration, giữ nguyên historical charges. Cần xác nhận chính sách retrospective changes và adjustments. |
| Những Student Fields nào cần được lưu và quản lý? Field nào được phép edit, field nào phải lấy từ authoritative source? | Đề xuất dùng Student ID, Name, DOB, Citizenship, School, Level, Class và Enrolment Status làm preliminary model. Phân tách authoritative fields với editable school records. |
| Khi một School, Level, Class hoặc Fee Component không còn sử dụng, hệ thống nên Delete hay Deactivate? | Đề xuất sử dụng Inactive/Archived Status với các records đã có dependencies để bảo toàn historical records và referential integrity. |

**Priority interpretation**

* **P1:** Cần được giải quyết sớm vì ảnh hưởng trực tiếp đến Sprint 1 data model, authorization hoặc scope.  
* **P2:** Cần clarify trước khi các related features được triển khai, nhưng có thể defer nếu không ảnh hưởng Sprint 1\.  
* **P3:** Có thể refinement sau, khi core management flow đã rõ.

## **4\. Working Assumptions**

| ID | Working Assumption |
| ----- | ----- |
| R3-A01 | Mô hình tổ chức dữ liệu ban đầu là School → Level/Cohort → Class → Student. |
| R3-A02 | Mỗi School, Level, Class và Student có unique identifier để quản lý và liên kết dữ liệu. |
| R3-A03 | Một Student có một current class assignment tại một thời điểm; historical enrolment được quản lý riêng nếu cần. |
| R3-A04 | MOE HQ Users có quyền quản lý records toàn hệ thống; School Users chỉ được thao tác trên records thuộc trường được phân quyền và trong phạm vi entity cho phép. |
| R3-A05 | Student Records tồn tại độc lập với Education Accounts. Non-Singaporean Students vẫn có Student Records nhưng không có Education Account. |
| R3-A06 | Fee Type đại diện cho nhóm hoặc loại phí; Fee Component đại diện cho thành phần cấu thành khoản phí. Relationship và calculation logic cần được xác nhận. |
| R3-A07 | Fee Structure Management không tự động đồng nghĩa với tạo payable charges hoặc thực hiện payments; các processing capabilities này cần được phân định với R9. |
| R3-A08 | Sprint 1 có thể sử dụng mock Schools, Levels, Classes, Students và Fee Records; không mặc định tích hợp với external school management systems. |

Các Working Assumptions chỉ hỗ trợ preliminary analysis và solution design, chưa được xem là client-approved business rules.

