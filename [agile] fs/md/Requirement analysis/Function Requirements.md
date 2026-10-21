# **Requirements**

# **R1 – Education Account Creation & Closure**

English

Education account is available to Singapore Citizen for education-related spending purposes. It should be automatically created and activated when the child turns 7, and automatically closes when the child reaches 16\.

Tiếng Việt

Tài khoản giáo dục được cung cấp cho công dân Singapore nhằm phục vụ các mục đích chi tiêu liên quan đến giáo dục. Tài khoản phải được tự động tạo và kích hoạt khi trẻ đủ 7 tuổi, đồng thời tự động đóng khi trẻ đủ 16 tuổi.

Portal: Admin Portal

# **R2 – Education Account Top-Up**

English

MOE HQ users can perform "Top-Up" to the education accounts. The Top-Up can be done in batches or to specific account holders. For batch top-up, MOE HQ users should be able to configure rules based on account holders' age, account balance, and schooling status, etc. The Top-up can be done either regularly or on an ad-hoc basis.

Tiếng Việt

Người dùng thuộc Trụ sở chính Bộ Giáo dục (MOE HQ) có thể thực hiện "Nạp tiền" (Top-Up) vào các tài khoản giáo dục. Việc nạp tiền có thể được thực hiện theo lô hoặc cho các chủ tài khoản cụ thể. Đối với việc nạp tiền theo lô, người dùng MOE HQ phải có khả năng cấu hình các quy tắc dựa trên độ tuổi, số dư tài khoản và tình trạng đi học của chủ tài khoản, v.v. Việc nạp tiền có thể được thực hiện định kỳ hoặc đột xuất.

Portal: Admin Portal

# **R3 – School, Student & Fee Management**

English

MOE HQ users and School users need to maintain the list of schools, levels/cohorts, classes, and students in each class, and types of fees and fee components payable by students.

Singaporean students can use the balance in Education Account to pay for the fees.

Tiếng Việt

Người dùng MOE HQ và người dùng nhà trường cần quản lý danh sách các trường học, cấp học/khóa học (levels/cohorts), lớp học và học sinh trong từng lớp, cũng như các loại phí và thành phần phí mà học sinh phải thanh toán.

Học sinh Singapore có thể sử dụng số dư trong Tài khoản Giáo dục để thanh toán các khoản phí này.

Portal: Admin Portal

# **R4 – Financial Assistance Scheme (FAS)**

## **Function**

English

Students with financial needs may apply for Financial Assistance Scheme (FAS).

The system should allow configuration on multiple schemes, each with different eligibility criteria based on student's nationality, household income band, and per-capita income band, and with different tiers and the corresponding subsidy amount on different fee components.

Income information comes from another third-party system via API.

MOEFAS (nationwide standard FAS) should be automatically granted if students meet certain predefined criteria.

If MOEFAS is not granted, School users may decide if they wish to grant School-based FAS (SBFAS).

The outcome of the FAS application should be reflected correctly in the fees payable.

Tiếng Việt

Học sinh có nhu cầu hỗ trợ tài chính có thể đăng ký Chương trình Hỗ trợ Tài chính (Financial Assistance Scheme – FAS).

Hệ thống phải cho phép cấu hình nhiều chương trình hỗ trợ, mỗi chương trình có các tiêu chí đủ điều kiện khác nhau dựa trên quốc tịch của học sinh, nhóm thu nhập hộ gia đình và nhóm thu nhập bình quân đầu người; đồng thời có các mức hỗ trợ khác nhau và số tiền trợ cấp tương ứng cho từng thành phần phí.

Thông tin thu nhập được lấy từ một hệ thống bên thứ ba khác thông qua API.

MOEFAS (chương trình FAS tiêu chuẩn áp dụng trên toàn quốc) phải được tự động cấp nếu học sinh đáp ứng các tiêu chí đã được xác định trước.

Nếu MOEFAS không được cấp, người dùng nhà trường có thể quyết định có cấp FAS của nhà trường (SBFAS) hay không.

Kết quả đơn đăng ký FAS phải được phản ánh chính xác vào các khoản phí phải thanh toán.

## **AI Feature**

English

Rule-based logic determines eligibility; Machine Learning predicts the remaining financial difficulty and recommends an appropriate assistance tier.

The model should classify students into different financial difficulty levels, for example:

* Low Risk – The student is likely able to pay the remaining fees.  
* Medium Risk – The student may experience some payment difficulty.  
* High Risk – The student is likely to experience significant payment difficulty.

Tiếng Việt

Logic dựa trên quy tắc (Rule-based logic) xác định điều kiện đủ tiêu chuẩn; Machine Learning dự đoán mức độ khó khăn tài chính còn lại và đề xuất mức hỗ trợ phù hợp.

Mô hình phải phân loại học sinh thành các mức độ khó khăn tài chính khác nhau, ví dụ:

* Rủi ro thấp (Low Risk): Học sinh có khả năng thanh toán các khoản phí còn lại.  
* Rủi ro trung bình (Medium Risk): Học sinh có thể gặp một số khó khăn khi thanh toán.  
* Rủi ro cao (High Risk): Học sinh có khả năng gặp khó khăn đáng kể trong việc thanh toán.

Portal: Admin Portal

# **R5 – Hardcopy Application Processing**

English

The system should support capturing and processing of hardcopy applications filled in by parents offline and collected by School users, for those parents who cannot access the e-Service Portal.

Tiếng Việt

Hệ thống phải hỗ trợ ghi nhận và xử lý các đơn đăng ký bản giấy do phụ huynh điền ngoại tuyến và được người dùng nhà trường thu thập, dành cho những phụ huynh không thể truy cập Cổng Dịch vụ Điện tử (e-Service Portal).

Portal: Admin Portal

# **R6 – FAS Budget & Statistics**

English

MOE HQ users should be able to set a budget and track on the statistics of MOEFAS subsidies granted.

School users should be able to set a budget and track on the statistics of SBFAS subsidies granted. 

Tiếng Việt

Người dùng MOE HQ phải có khả năng thiết lập ngân sách và theo dõi số liệu thống kê về các khoản trợ cấp MOEFAS đã được cấp.

Người dùng nhà trường phải có khả năng thiết lập ngân sách và theo dõi số liệu thống kê về các khoản trợ cấp SBFAS đã được cấp.

Portal: Admin Portal

# **R7 – User View Simulation**

English

MOE HQ users should be able to simulate how School users and Parents access and see the system, in order to address their queries better.

Tiếng Việt

Người dùng MOE HQ phải có khả năng mô phỏng cách người dùng nhà trường và phụ huynh truy cập và nhìn thấy hệ thống, nhằm giải đáp các thắc mắc của họ tốt hơn.

Portal: Admin Portal

# **R8 – Parent Access & Education Account Details**

## **Function**

English

Parents should be able to access e-Service portal via SingPass to view education account details, balance, transactions, and update basic personal details such as residential address, mailing address, contact number, etc. where applicable.

Tiếng Việt

Phụ huynh phải có khả năng truy cập Cổng Dịch vụ Điện tử (e-Service Portal) thông qua SingPass để xem thông tin chi tiết tài khoản giáo dục, số dư, các giao dịch và cập nhật thông tin cá nhân cơ bản như địa chỉ cư trú, địa chỉ nhận thư, số điện thoại liên hệ, v.v., khi áp dụng.

## **AI Feature (Shared across R8–R10)**

English

1\. To have AI solution to allow users ask questions related to the functionalities in the e-Service portal, and dynamically ask follow-up questions to better understand the context and provide more relevant answers.

2\. Automatically fill in the FAS Application form based on the profile as well as answers gathered from above.

Tiếng Việt

1\. Có giải pháp AI cho phép người dùng đặt câu hỏi liên quan đến các chức năng trong Cổng Dịch vụ Điện tử, đồng thời linh hoạt đặt các câu hỏi tiếp theo để hiểu rõ hơn ngữ cảnh và cung cấp câu trả lời phù hợp hơn.

2\. Tự động điền biểu mẫu đăng ký FAS dựa trên thông tin hồ sơ và các câu trả lời đã thu thập ở trên.

Portal: e-Service Portal

# **R9 – Outstanding Charges & Payment**

English

Parents should be able to view outstanding charges. They can choose to pay for fees using the balance from the education accounts, or via online payment methods.

Tiếng Việt

Phụ huynh phải có khả năng xem các khoản phí còn chưa thanh toán (outstanding charges). Họ có thể lựa chọn thanh toán các khoản phí bằng số dư trong tài khoản giáo dục hoặc thông qua các phương thức thanh toán trực tuyến.

AI Feature: Shared across R8–R10 (được ghi tại R8).

Portal: e-Service Portal

# **R10 – Financial Assistance Application**

English

Parents should be able to apply for financial assistance schemes as a family unit.

Tiếng Việt

Phụ huynh phải có khả năng đăng ký các chương trình hỗ trợ tài chính theo đơn vị hộ gia đình (family unit).

AI Feature: Shared across R8–R10 (được ghi tại R8).

Portal: e-Service Portal

| Requirements | Website nên xem |
| :---- | :---- |
| R1 – Education Account Lifecycle | SFS / Edusave |
| R2 – Account Top-up | SFS / Edusave Government Top-up |
| R3 – School & Fee Management | SFS (một phần) |
| R4–R5 – FAS Processing | MOE Financial Assistance |
| R6–R7 – Budget & User Simulation | Chưa xác định được trang công khai tương ứng |
| R8 – Account Inquiry | SFS |
| R9 – Fee Payment | SFS / Parents Gateway (một phần) |
| R10 – FAS Application | SFS / MOE FAS |

# **A.Brief requirement**

## **I. Admin Portal (R1–R7)**

| ID | Requirement | Brief Description |
| :---- | :---- | :---- |
| R1 | Education Account Lifecycle | Education Account dành cho Singapore Citizens để chi tiêu giáo dục. Tài khoản tự động được tạo và kích hoạt khi trẻ đủ 7 tuổi, tự động đóng khi đủ 16 tuổi. |
| R2 | Education Account Top-up | MOE HQ Users có thể nạp tiền cho từng tài khoản hoặc hàng loạt, định kỳ hoặc ad-hoc. Hỗ trợ cấu hình rules theo độ tuổi, số dư tài khoản, tình trạng đi học, v.v. |
| R3 | School, Student & Fee Management | MOE HQ và School Users quản lý danh sách trường, levels/cohorts, classes, students, fee types và fee components. Học sinh Singapore có thể sử dụng Education Account để thanh toán các khoản phí. |
| R4 | Financial Assistance Scheme (FAS) Management | Cấu hình nhiều FAS schemes với eligibility criteria, tiers và subsidy amounts khác nhau. Thu nhập được lấy từ third-party API. MOEFAS có thể tự động được cấp khi đủ điều kiện; School Users quyết định cấp SBFAS nếu MOEFAS không được cấp. Kết quả FAS phải được phản ánh vào fees payable. |
| R5 | Offline FAS Application Processing | School Users có thể nhập và xử lý hồ sơ FAS giấy được phụ huynh nộp offline khi không thể truy cập e-Service Portal. |
| R6 | FAS Budget & Statistics | MOE HQ Users thiết lập ngân sách và theo dõi thống kê trợ cấp MOEFAS; School Users thực hiện tương tự đối với SBFAS. |
| R7 | User Access Simulation | MOE HQ Users có thể mô phỏng cách School Users và Parents truy cập, nhìn thấy hệ thống nhằm hỗ trợ giải đáp thắc mắc. |

## **II. e-Service Portal (R8–R10)**

| ID | Requirement | Brief Description |
| :---- | :---- | :---- |
| R8 | Education Account Inquiry & Profile Management | Parents đăng nhập qua SingPass để xem thông tin Education Account, số dư, giao dịch và cập nhật một số thông tin cá nhân như địa chỉ, số điện thoại khi được phép. |
| R9 | Outstanding Fees & Payment | Parents xem các khoản phí chưa thanh toán và lựa chọn thanh toán bằng số dư Education Account hoặc các phương thức thanh toán online. |
| R10 | FAS Application Submission | Parents có thể đăng ký Financial Assistance Schemes theo đơn vị gia đình (family unit). |

## **III. AI Features**

| ID | AI Feature | Description |
| :---- | :---- | :---- |
| AI-01 | FAS Eligibility & Risk Prediction | Rule-based logic xác định eligibility. Machine Learning dự đoán khó khăn tài chính còn lại, phân nhóm Low/Medium/High Risk và đề xuất assistance tier phù hợp. |
| AI-02 | AI Conversational Assistant | Cho phép người dùng hỏi về các chức năng của e-Service Portal; hệ thống đặt follow-up questions linh hoạt để hiểu ngữ cảnh và đưa ra câu trả lời phù hợp. |
| AI-03 | AI-assisted FAS Application | Tự động điền thông tin vào FAS Application Form dựa trên profile và các câu trả lời được thu thập qua AI assistant. |

* Khi phân tích hãy đi theo luồng: **Business Objective → Actor → Trigger → Main Flow → Business Rules → Requirement Gaps → Dependencies.**  
* Để quyết định nên làm chức năng nào trong mỗi sprint thì cần xác định business values/goals  
* Khi phân tích high-level requirement nên lập bảng gồm các cột:

| Requirement | Business Value | Main Actor | Dependency cần kiểm tra |
| :---- | :---- | :---- | :---- |

# **R1**

# **R1 – Education Account Lifecycle Management**

**Version:** 1.3  
**Status:** Partially Clarified – Pending Open Questions  
**Sources:** Initial Client Brief (R1), First Client Clarification Meeting

## **1\. Overview**

Education Account là tài khoản có tính chất tài chính, tương tự một bank account, được Chính phủ Singapore cấp vốn cho Singapore Citizens để chi trả các khoản education-related expenses.

Hệ thống chịu trách nhiệm tự động tạo, kích hoạt và đóng Education Account theo eligibility và age-based lifecycle rules.

Singapore Citizens có thể sử dụng Education Account để thanh toán các khoản phí giáo dục. Permanent Residents và Foreign Students vẫn có thể theo học tại Singapore nhưng không được cấp Education Account và phải sử dụng phương thức thanh toán khác.

## **2\. Confirmed Requirements**

| Confirmed Requirement |
| :---- |
| Education Account chỉ dành cho Singapore Citizens để phục vụ education-related spending. |
| Hệ thống tự động tạo và kích hoạt Education Account khi trẻ đủ 7 tuổi. |
| Hệ thống tự động đóng Education Account khi trẻ đủ 16 tuổi. |
| Mỗi Singapore Citizen chỉ có một Education Account. |
| Education Account là tài khoản tài chính được Chính phủ cấp tiền, không phải tài khoản đăng nhập hệ thống. |
| Education Account lifecycle độc lập với schooling status, school enrolment hoặc school transfer. |
| Khi đóng Education Account ở tuổi 16, remaining balance phải được chuyển sang CPF. |
| Client kỳ vọng không còn pending transactions tại thời điểm đóng tài khoản. Cách xử lý nếu thực tế vẫn tồn tại pending transactions chưa được xác nhận. |
| Thông tin student được client đề cập để phục vụ account provisioning gồm Name, DOB, Citizenship và Address (nếu có thể lấy được). |

**Clarification references:**

* Remaining balance → CPF; không nên còn pending transactions.  
* Client làm rõ các student data fields.  
* Education Account là financial account; mỗi citizen có một account; phân biệt Singapore Citizens với các nhóm học sinh khác.  
* Education Account status không phụ thuộc schooling/enrolment status.

## **3\. Requirement Gaps \+ Proposed Solutions**

| Gap / Open Question | Proposed Solution |
| :---- | :---- |
| Hệ thống lấy student records từ nguồn nào? Identifier nào bảo đảm nhận diện duy nhất mỗi student? | Dùng mock data source cho Sprint 1\. Đề xuất Person ID làm unique identifier, kèm Name, DOB, Citizenship, optional Address và metadata phục vụ đồng bộ. |
| Khi student thay đổi Citizenship, account lifecycle xử lý thế nào? Đặc biệt khi nhập quốc tịch sau tuổi 7 hoặc mất quốc tịch trước tuổi 16? | Đề xuất re-evaluate eligibility khi nhận Citizenship Update; tạo account cho newly eligible student và xử lý account không còn eligible. Cần client xác nhận closure, reopening và effective-date rules trước khi triển khai đầy đủ. |
| Nếu tại thời điểm closure vẫn có pending transactions, hệ thống phải xử lý thế nào để vừa đáp ứng age-based closure vừa bảo đảm financial settlement? | Đề xuất dừng new spending khi đến thời điểm closure, flag các pending transactions để reconciliation và chỉ hoàn tất chuyển số dư sau khi xác định số dư cuối cùng. Cần xác nhận account status trong giai đoạn này. |
| CPF transfer được thực hiện qua integration nào? Làm sao xác định tài khoản CPF, xử lý transfer failure và ghi nhận kết quả? | Sprint 1 có thể mô phỏng CPF transfer và lưu transfer status. Chưa triển khai hoặc cam kết real CPF integration nếu chưa có interface và business rules được xác nhận. |
| Hệ thống xác định Parent–Child relationship từ nguồn nào để hỗ trợ R8? | Đề xuất lưu Parent/Guardian–Child mapping từ authorized source hoặc mock dataset. Relationship data phục vụ authorization, tách khỏi Education Account eligibility. |
| Citizenship và DOB được đồng bộ với tần suất nào? Xử lý dữ liệu đến trễ hoặc processing failure ra sao? | Đề xuất daily age-based evaluation, re-evaluation khi nhận updated records, logging và retry. Cần xác nhận data freshness và late-update handling. |
| Những student personal data nào được phép lưu, thời gian lưu bao lâu và trường nào chỉ được truy xuất từ external source? | Áp dụng data minimization và sử dụng synthetic data trong Sprint 1\. Production data storage/retention cần được làm rõ trước khi tích hợp dữ liệu thật. |
| Sau khi account đóng, parent có thể xem account details, balance và transaction history trong bao lâu? | Đề xuất lưu closed-account record và transaction history ở chế độ read-only, subject to access và retention rules cần được xác nhận cùng R8. |

## **4\. Working Assumptions**

| Working Assumption |
| :---- |
| Age được tính theo DOB chính xác, với eligibility age range từ sinh nhật 7 tuổi đến trước sinh nhật 16 tuổi. |
| Hệ thống sử dụng một stable Person ID để xác định student và ngăn duplicate Education Account creation. |
| Age-based lifecycle được đánh giá hằng ngày; citizenship updates được xử lý khi hệ thống nhận dữ liệu mới. |
| Nếu hệ thống nhận student record muộn và student hiện đủ điều kiện trong khoảng 7 đến dưới 16 tuổi, hệ thống có thể tạo và kích hoạt account mà không cần chờ sự kiện sinh nhật tiếp theo. |
| Nếu DOB, Citizenship hoặc identifier cần thiết bị thiếu/không hợp lệ, hệ thống không tự tạo account và ghi nhận exception để xử lý. |
| Sprint 1 sử dụng synthetic student data và mock lifecycle processing; không mặc định có kết nối thật với Government Data Source hoặc CPF. |
| Tạm thiết kế eligibility evaluation dựa trên Citizenship và Age. |
| Dùng mock data source cho Sprint 1\. Đề xuất Person ID làm unique identifier, kèm Name, DOB, Citizenship, optional Address và metadata phục vụ đồng bộ. |

# **R3**

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

## **5\. Functional Breakdown** 

| Function ID | Function | Descriptio |
| ----- | ----- | ----- |
| R3-F01 | Quản lý Trường học | Xem/tìm kiếm hồ sơ trường; tạo/cập nhật thông tin trường; kích hoạt/ngừng kích hoạt (quyền và trường dữ liệu cần xác nhận). |
| R3-F02 | Quản lý Level/Cohort | Xem, tạo và cập nhật Level/Cohort; liên kết với School (quyền sở hữu và phân cấp cần xác nhận). |
| R3-F03 | Quản lý Lớp học | Xem, tạo và cập nhật Class; liên kết Class với Level/Cohort. |
| R3-F04 | Quản lý Học sinh | Xem/tìm kiếm hồ sơ học sinh và duy trì các trường dữ liệu được phép chỉnh sửa. |
| R3-F05 | Gán học sinh vào lớp | Gán Student vào Class và liên kết học sinh với School/Class tương ứng; kiểm tra phạm vi quyền và tính hợp lệ của liên kết. |
| R3-F06 | Quản lý Fee Type | Xem và duy trì Fee Type; liên kết Fee Component theo quyền được cấp. |
| R3-F07 | Quản lý Fee Component | Xem và duy trì Fee Component, cấu hình thuộc tính; các trường và quy tắc tính phí cần xác nhận. |
| R3-F08 | Kiểm soát truy cập dữ liệu danh mục | Giới hạn thao tác và phạm vi bản ghi theo vai trò và trường học. |
| R3-F09 | Tái sử dụng Fee Component | Tùy chọn/cần xác nhận: cho phép dùng một component, ví dụ GST, trong nhiều Fee Type. |
| R3-F10 | Chuyển lớp, chuyển trường và lên lớp | Cần xác nhận: hỗ trợ chuyển lớp/trường và lên lớp theo năm học. |
| R3-F11 | Lịch sử và nhật ký thay đổi dữ liệu | Cần xác nhận: ghi nhận thay đổi và lưu lịch sử khi cần. |
| R3-F12 | Cấu hình phạm vi áp dụng phí | Cần xác nhận: xác định phí áp dụng theo School, Level/Cohort, Class hoặc Student. |

# **R8**

# **R8 – Parent e-Service Portal & AI Assistant**

**Version:** 1.0  
**Status:** Draft – Pending Client Clarification  
**Sources:** Initial Client Brief (R8)

## **1\. Overview**

Parents truy cập e-Service Portal bằng SingPass để xem Education Account của con, gồm account details, balance và transactions.

Parents tự cập nhật basic personal details của mình như residential address, mailing address và contact number. Students không đăng nhập; mọi thao tác trên portal do Parent thực hiện.

Portal có AI assistant trả lời câu hỏi về các functionalities của e-Service Portal và chủ động hỏi lại (follow-up questions) để hiểu đúng ngữ cảnh trước khi trả lời.

## **2\. Confirmed Requirements**

| Confirmed Requirement |
| :---- |
| Parent đăng nhập e-Service Portal bằng SingPass. |
| Parent xem được Education Account details, balance và transactions của con. |
| Parent cập nhật được basic personal details: residential address, mailing address, contact number ("etc., where applicable"). |
| AI assistant trả lời câu hỏi liên quan đến functionalities của e-Service Portal. |
| AI assistant chủ động hỏi follow-up questions khi cần để đưa ra câu trả lời sát ngữ cảnh. |

## **3\. Requirement Gaps \+ Proposed Solutions**

| Gap / Open Question | Proposed Solution |
| :---- | :---- |
| Parent xem transactions trong khoảng thời gian bao lâu? Có cần filter và download statement không? | Hiển thị toàn bộ lịch sử giao dịch, filter theo date range và transaction type, cho export PDF statement. Cần client xác nhận. |
| "etc., where applicable": field nào Parent được sửa, field nào chỉ xem? | Editable: residential address, mailing address, mobile number, email. Read-only: Name, NRIC, relationship với student. |
| Có nên cho sửa residential address trên portal? Thực tế công dân Singapore cập nhật địa chỉ tại ICA, các dịch vụ dùng SingPass/Myinfo chỉ đọc. | Mock phase cho sửa trực tiếp. Khi tích hợp SingPass thật, chuyển residential address sang read-only lấy từ Myinfo. Cần client xác nhận. |
| Mobile number và email mới có cần OTP verification không? | Cần client xác nhận. Nếu có, phải bổ sung SMS/email service. |
| Parent có nhiều con, và cả father lẫn mother cùng xem thì xử lý thế nào? | Home page liệt kê tất cả linked children; cả hai parents đều xem được Education Account của con; contact details của mỗi parent lưu riêng. |
| AI assistant có được trả lời về personal data (balance, application status) không? | Đề xuất không. AI chỉ hướng dẫn cách dùng chức năng và điều hướng Parent tới đúng trang khi hỏi về dữ liệu cá nhân. Cần client xác nhận. |
| Khi AI không trả lời được, chuyển Parent sang kênh hỗ trợ nào? | Hiển thị help page và contact của trường. Cần client xác nhận. |
| AI solution cụ thể là gì? | LLM trả lời dựa trên nội dung hướng dẫn của portal, không truy cập personal data. Nếu chưa kịp, dùng tạm chatbot theo kịch bản trên cùng giao diện chat. |
| Làm sao đo AI trả lời đúng trước khi demo? | Client cung cấp hoặc duyệt bộ câu hỏi test trước 21/10; target trả lời đúng tối thiểu 90% và không lộ personal data. |

## **4\. Working Assumptions**

* Phase này dùng SingPass giả lập; Parent identity được mapping với student qua metadata.  
* AI assistant hỗ trợ English.  
* Transaction history hiển thị 20 dòng mỗi trang, mới nhất trước.  
* Mobile number gồm 8 chữ số, bắt đầu bằng 8 hoặc 9; postal code gồm 6 chữ số.  
* NRIC hiển thị dạng masked, ví dụ S\*\*\*\*567A.  
* AI hiện typing indicator trong 1 giây và trả lời trong 10 giây

# **R9**

# **R9 – Fee Payment**

1. ## **Overview**

| Item | Details |
| ----- | ----- |
| Requirement | Parents should be able to view outstanding charges. They can choose to pay for fees using the balance from the education accounts, or via online payment methods. |
| Portal | e-Service Portal (for Parents) |
| Primary actor | Parent/Guardian signed in via Singpass |
| Indirect actors | School Users and MOE HQ Users: set up fee types and fee components and assign fees to students through the Admin Portal (R3) |

## **2\. Function**

| ID | Function |
| :---: | ----- |
| R9-01 | Parents access the e-Service Portal through Singpass to view and pay fees. |
| R9-02 | Parents can view the outstanding charges of their child. |
| R9-03 | Parents can choose to pay with the Education Account balance or with an online payment method. |
| R9-04 | Singapore citizen students can use the EA balance to pay fees. |
| R9-05 | An EA is a government-funded account for eligible education expenses, like a bank account for education. It is not a login account. |
| R9-06 | Students without an EA (permanent residents, foreign students) can still attend school and pay fees from their own funds, not from an EA. |
| R9-07 | School enrolment status and EA status are separate; one does not determine the other. |
| R9-08 | Fee categories include school fees, miscellaneous fees, extracurricular activities (music classes, school trips) and ad hoc charges (e.g. damage to classroom property). |
| R9-09 | Some charges apply only to a particular level or class. Level and cohort may be used interchangeably; class is a separate concept. |
| R9-10 | A fee component is reusable across fee types (e.g. GST is configured once, not separately for each fee type). |
| R9-11 | When an EA is closed there must be no pending transactions, and any remaining balance is transferred to CPF. |
| R9-12 | Sprint 1 covers the parent-facing portal, the necessary backend/database work and part of the Administration Portal. |
| R9-13 | The parent portal may be used from 6:00 a.m. to 2:00 a.m.; usage may rise around bill-payment periods, with no fixed peak. About 2 million parents is the potential population, not concurrent users. |

### **Clarification references**

| Ref | Clarification |
| :---: | :---- |
| CM-1 | EA closure: no pending transactions, remaining balance goes to CPF. Student data discussed: name, date of birth, citizenship, address (if available). |
| CM-2 | An EA is an education account, not a login account. Permanent residents and foreign students have no EA and pay fees themselves. |
| CM-3 | Level and cohort are interchangeable; class is separate. HQ manages all records, School manages its own school level and below. Enrolment and EA status are independent. |
| CM-4 | Fee type examples; reusable fee components (GST); some fees apply by level or class. |
| CM-5 | User populations, usage hours, peaks around bill payment; the delivery team must propose concurrent-user targets. |

## 

## **3\. Requirement Gaps \+ Proposed Solutions**

| Gap / Open Question | Proposed Solution |
| ----- | ----- |
| G1 – "Outstanding charges" is not defined: which charges are included, which statuses exist (unpaid, partially paid, overdue), and whether charges are shown per student or per invoice. | Each fee assigned to a student is a charge with status Unpaid or Paid (Partially Paid if the client agrees). The screen lists charges per child, grouped by fee type, showing fee components (including GST) and the total. Ask the client to confirm the status set. |
| G2 – Fee types, fee components, mandatory attributes, who may set up which fee type, and the use case of school users assigning fees to students have not been provided (client owes the list and use case). | Model: a Fee Type has several reusable Fee Components; charges are assigned to a student, class or level. DEV mocks data from the four fee groups the client gave (school fee, misc fee, extracurricular, ad hoc). Permissions follow the rule: HQ manages everything, School manages its own school level and below. |
| G3 – "Online payment methods" are not listed, and the payment gateway is unknown. | Sprint 1 uses a simulated payment gateway (sandbox) covering success, failure and cancel flows. Ask the client for the list of methods and the real gateway for later sprints. |
| G4 – Paying with EA when the balance is insufficient: block, or allow a partial EA payment with the remainder paid online (split payment)? | Sprint 1: allow the EA option only when the balance is at least the amount to pay; otherwise show a message and suggest online payment. Ask the client whether split payment is allowed. |
| G5 – Conditions for using an EA to pay: citizenship, activation and closure ages (7 and 16 in the requirements list, to be verified), and loss of citizenship or leaving Singapore. The business reason for deactivating on loss of citizenship has not been asked. | Enable the "EA balance" option only when the student has an EA in Active status; otherwise only online payment is offered. Detailed conditions wait for the client to confirm in workshops. |
| G6 – Outstanding charges when an EA is closed, and what counts as a "pending transaction" at closure (the client only said there must be none). | Do not run EA closure while a payment is in Pending status; the closure job reports an error and retries after the payment completes or is cancelled. Charges still owed after EA closure can be paid online only. Ask the client to confirm the definition of pending. |
| G7 – Parent-student linking rules: multiple children, multiple guardians, who may view and who may pay. | Links are created when student data is loaded from the third-party system; after Singpass sign-in the system checks the link and shows only linked children. A parent with several children selects a child to view fees. Any guardian with a link can view and pay, pending client confirmation. |
| G8 – How FAS affects the amount payable. Requirement \#4 says the FAS outcome must be reflected in fees payable, but FAS is not in Sprint 1\. | Sprint 1 shows the original amount. The charge has a subsidy line (default 0\) so R4 can plug in without changing the data structure. The internal understanding is that FAS reduces the school fee invoice directly; the client has not confirmed this. |
| G9 – Payment confirmation, receipt, transaction history, errors/timeouts and duplicate-payment protection have not been discussed. | Each payment creates a payment record (Success, Failed, Pending) shown in the transaction history (Req \#8 lets parents view transactions). Show a confirmation screen with a reference number. Use an idempotency key so money is never deducted twice. A failed payment does not change the charge status and does not debit the EA. |
| G10 – Concurrent-user target for the parent portal: the client asked the delivery team to propose one (action item of KO-7). | QA and DEV propose targets as a share of the 2 million parents online at once, e.g. a low scenario of 1% (20,000 users) and a high scenario of 5% (100,000 users), plus a peak scenario around bill-payment periods. Figures are for discussion only and will be agreed with the client in workshops. |
| G11 – The exact meaning of "level" and "cohort" in the data model, since some fees apply only by level or class. | Use one attribute, Level (alias Cohort); charges are assigned by Level or Class. Ask the client to confirm the definition. |
| G12 – The requirement numbers in the transcript (1, 3, 8, 9\) are not clear enough for formal documentation. | BA verifies them against the requirements list. Until the client confirms, use Functions 1, 3, 8, 9 per the internal MoM. |

## 

## **4\. Working Assumptions**

| ID | Working Assumption |
| :---: | ----- |
| A1 | Online payment in Sprint 1 goes through a simulated payment gateway (sandbox). |
| A2 | The EA balance is stored in the internal database and is debited only when an EA payment succeeds. |
| A3 | Basic student data (date of birth, ID) is stored in the internal database after the first extraction from MyInfo and synchronised periodically at 0:00 daily. This is an internal agreement, not yet discussed with the client. |
| A4 | Parent-student links are created when student data is loaded; after Singpass sign-in the system checks the link and allows access only to the EA of linked children. |
| A5 | Only Singapore citizen students have an EA. Permanent resident and foreign students pay online from their own funds only. |
| A6 | The EA is activated at age 7 and closed at age 16 per requirement \#1; these figures need to be verified against the official requirements list. |
| A7 | Amounts are shown in Singapore dollars (SGD) and GST is a reusable fee component. The meetings did not state the currency. |
| A8 | FAS does not apply in Sprint 1; the amount shown is the original amount, and the charge has a subsidy line defaulting to 0\. |
| A9 | Fee and charge data for the demo is mocked or entered through the Admin Portal part of Sprint 1 (R3), based on the four fee groups the client mentioned. |
| A10 | Whether an EA can be used depends only on EA status, not on school enrolment status. |
| A11 | The parent actively chooses the payment method for each charge; the system never debits the EA automatically. |

