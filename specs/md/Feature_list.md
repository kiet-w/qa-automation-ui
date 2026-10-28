# DANH MỤC TÍNH NĂNG CHỨC NĂNG HỆ THỐNG (FEATURE LIST)

> **Dự án**: MOE Education Account & Fee Management System  
> **Nguồn gốc**: Trích xuất từ Feature list.docx (Google Drive Baseline)  
> **Phiên bản**: 2.0 (Updated 19/10/2026)  
> **Phạm vi**: Toàn diện R1, R2, R3, R4, R8, R9  

---

# Quản lý vòng đời EA (Mở và đóng)

Initial Synchronization: Truy xuất dữ liệu Singapore Citizens từ đủ 7 đến dưới 16 tuổi thông qua Mock Government Citizen API.

Daily Incremental Synchronization: Truy xuất những công dân vừa đủ 7 tuổi trong ngày xử lý.

Citizen Data Validation: Kiểm tra NRIC, Full Name, DOB, Citizenship và các required fields theo Data Contract.

#### Student Profile Creation: Lưu thông tin công dân hợp lệ vào internal Student Profile(?).

Education Account Creation: Tạo tài khoản liên kết với Student Profile, với Account Number duy nhất, Status = Active, Balance = SGD 0.00 (wallet).

Duplicate Prevention: Mỗi Singapore Citizen chỉ có một Education Account, kể cả khi tài khoản cũ đã Closed.

Invalid Record Handling: Bỏ qua Citizen Records thiếu required information; Father/Mother NRIC là optional.

Student Data Synchronization Boundary: Daily Sync không tự động cập nhật các Student Profiles đã tồn tại.

# Tự động đóng TK EA

Backend-Triggered Eligibility Check: Trước khi truy cập hoặc xử lý Education Account, backend thực hiện kiểm tra điều kiện đóng (Citizenship/tuổi dựa trên DoB).

Real-Time Government Verification: Gọi Mock Government Citizen API để lấy Current DOB và Citizenship của Account Holder.

Age-Based Closure: Nếu Account Holder đã đủ 16 tuổi, kích hoạt Account Closure Processing.

Citizenship-Based Closure: Nếu Account Holder không còn là Singapore Citizen, kích hoạt Closure Processing.

Active Account Handling: Nếu chưa đủ 16 tuổi và vẫn là Singapore Citizen, tài khoản tiếp tục Active.

#### Closure Processing: Kiểm tra điều kiện hoàn tất, cập nhật Status = Closed và Actual Closure Date khi đủ điều kiện (?).

Financial Action Protection: Các yêu cầu Top-Up hoặc Payment phải được kiểm tra trước khi thực hiện.

Closed Account Handling: Không đóng lặp lại; giữ thông tin lịch sử và áp dụng quyền xem phù hợp.

Student Profile Boundary: Không tự động refresh toàn bộ Student Profile từ Government API.

Chuyển tiền dư sau khi đóng qua cpf (chưa làm)

# R8 - Parent Portal: SingPass, Education Account & Profile

Parent chọn Log in with SingPass.

SingPass xác thực và cung cấp Parent NRIC cùng thông tin định danh.

System gọi Mock Data API bằng Parent NRIC để tìm Parent và các con có liên kết.

Lần đầu đăng nhập, tạo Parent Account và liên kết các con; lần sau tái sử dụng tài khoản.

Đồng bộ dữ liệu của Parent và những người con liên quan tại thời điểm đăng nhập, không thực hiện nightly bulk synchronization.

Tạo Session và điều hướng Parent vào Home.

Chỉ cho phép Parent xem các con được liên kết với mình; cha và mẹ có quyền như nhau.

Xử lý lỗi authentication, API timeout, dữ liệu không tìm thấy và Session Expiry.

## View Education Account

Parent Home: Hiển thị card của từng con (EA), tên con, mã EA, Nric của con, balance, phí cần phải trả, trạng thái account

Có chức năng xem thông tin education entolment trường, cấp, level, năm học, lớp, trạng thái enrolement.

Balance Overview: Hiển thị số dư khả dụng, giao dịch Pending và tổng tiền vào/ra.

Transaction History: Xem giao dịch, lọc theo thời gian, loại giao dịch và chiều tiền.

FAS Information Display: Hiển thị thông tin hỗ trợ tài chính khi có dữ liệu (chưa làm).

Age-Based Access Restrictions: Parent vẫn xem được thông tin của con đủ 16 tuổi, nhưng không thực hiện Payment hoặc FAS Application cho con đó.

## Update Basic Personal Details

Cho phép parent chỉnh sủa thông tin liên lạc (qua chức năng view my details)

Chỉnh sửa Phone Number, Email và Mailing Address.

Không cho sửa NRIC, Full Name hoặc Residential Address (dữ liệu đồng bộ từ singpass).

Validate dữ liệu trước khi lưu.

Không ghi đè thông tin liên lạc Parent đã tự chỉnh sửa khi đăng nhập lại.

Chuyển My details sang read-only khi tất cả các con đã đủ 16 tuổi.

# R9 Outstanding Fees & Payment

Cho phép xem hoặc thanh toán các fee của EA liên kết với parent

Các invoice chưa thanh toán bao gồm fee type, fee component, invoice items tương ứng với số tiền, subsidy, net amount, ngày tới hạn, status và Account balance

Hiển thị transaction history

Chọn một invoice → chọn hình thức thanh toán: 
Education Account: Thanh toán toàn bộ bằng số dư EA nếu đủ điều kiện.

Online Payment: Thanh toán bằng cổng thanh toán trực tuyến.

Split Payment: Sử dụng một phần từ EA và phần còn lại từ Online Payment.

Gọi dịch vụ Education Account để kiểm tra số dư, trừ tiền và ghi nhận ledger transaction, sử dụng FundingReference để tránh trừ tiền trùng.

Tạo Payment Session với sandbox gateway, chuyển Parent sang bước thanh toán trực tuyến và chờ kết quả từ provider. (mới chỉ mô phỏng)

Ghi nhận invoice = Paid khi thanh toán thành công; hiển thị Payment Reference và Receipt. Nếu Split Payment thất bại ở nhánh online sau khi EA đã bị trừ, hệ thống phải hoàn lại phần EA hoặc chuyển sang ReconciliationRequired nếu không thể hoàn an toàn.

# R3 - School & student management

## F01 – School Management

Actor: MOE HQ User

HQ User có thể tạo, xem và chỉnh sửa thông tin School.

Thông tin School bao gồm School Code, School Name, School Type và Status (chuẩn bị sẵn list test 10 trường cố định).

HQ User có thể xem danh sách School đã được tạo.

School mới được tạo phải được lưu trong hệ thống để sử dụng cho School User Assignment và Academic Setup.

School có dữ liệu liên quan không bị xóa vĩnh viễn; sử dụng Deactivate theo business rules của FS.

## F02 – School User Account & School Assignment

Admin tạo danh sách các trường

School user đăng nhập bằng school ID của họ (Assume do nhà trường cấp), lần đầu đăng nhập phải tự nhập các thông tin cá nhân: tên, trường. (làm sprint sau)

## F03 – Academic Year, Education Stage & Academic Level Configuration

Actor: School User

SU truy cập School Configuration.

SU lựa chọn Academic Year từ danh sách có sẵn.

SU lựa chọn Education Stage/School Level mà trường giảng dạy, ví dụ Primary, Secondary hoặc Pre-University.

Hệ thống hiển thị các Academic Levels phù hợp để SU lựa chọn từ danh sách có sẵn.

SU chọn các Levels được giảng dạy tại School trong Academic Year đó.

SU add các tên lớp trong từng academic level

Hệ thống lưu cấu hình School – Academic Year – Academic Level Offering – Class name.

Hệ thống không cho tạo trùng một Level trong cùng School và Academic Year.

Một Level có thể có nhiều Classes.

SU có thể xem danh sách Classes theo School, Academic Year và Level.

Hệ thống không cho phép tạo trùng Class Code trong cùng School Level Offering.

Class đã có Student Assignment không được xóa làm mất dữ liệu lịch sử.

## F05 – Student Record Creation & Management

Actor: School User

SU truy cập Student Management và có thể tạo Student Record mới.

Thông tin Student bao gồm:

Student ID

Full Name

NRIC

Date of Birth

Student Category (SC / PR / IS)

Hệ thống validate các trường bắt buộc và kiểm tra Student Record trùng.

Hệ thống sử dụng NRIC để tìm Education Account tương ứng nếu có.

Nếu tìm thấy EA, hệ thống kiểm tra các thông tin định danh cần đối chiếu.

Nếu thông tin phù hợp, Student Record được liên kết với EA.

Nếu thông tin không khớp, hệ thống hiển thị cảnh báo hoặc chặn lưu theo quy tắc được xác nhận. [TBC]

Nếu không có EA, hệ thống vẫn tạo student record (STUDENT RECORD không phải EDUCATION ACCOUNT).

SU có thể xem và chỉnh sửa những Student Details được phép sửa.

## F06 – Student Enrolment

School User (SU) truy cập cấu trúc trường theo School → Academic Year → Academic Level → Class.

SU chọn một Class đã được cấu hình và assign một hoặc nhiều Student Records vào Class đó.

Student Record phải được tạo trước khi thực hiện Class Assignment.

SU chỉ được assign Student vào Class thuộc School mình được phân quyền.

Sau khi assign thành công, hệ thống tự động tạo Enrolment Profile cho từng Student.

Enrolment Profile bao gồm: Student ID, Student Information, School, Academic Year, Academic Level, Class, Enrolment Status và Effective Date.

Thông tin School, Academic Year và Academic Level được tự động xác định từ Class đã chọn.

SU có thể xem danh sách Students thuộc từng Class và Enrolment Profile của từng Student.

Hệ thống không cho phép tạo các Active Enrolment Profiles bị trùng hoặc xung đột.

## F07– Student Transfer & Class Change

Khi Student chuyển Class, Academic Level hoặc Academic Year trong cùng School, SU thực hiện thay đổi Enrolment; hệ thống chuyển profile cũ sang Inactive và tạo profile mới với thông tin cập nhật.

Khi Student chuyển School, SU trường cũ Deactivate Enrolment Profile; SU trường mới nhập Student Information với Student ID do trường mới cấp và assign vào Class để tạo Enrolment Profile mới.

Student ID được cấp và quản lý theo từng School, không bắt buộc giữ nguyên khi chuyển School.

Các Enrolment Profiles cũ được giữ lại để tra cứu lịch sử, không bị xóa hoặc ghi đè.

Hệ thống ghi nhận người thực hiện, thời điểm và lý do thay đổi Enrolment. [Đề xuất]

Việc tạo Enrolment Profile không đồng nghĩa với việc tạo Education Account; EA được quản lý riêng theo R1.

## F08 – Student–Education Account Linkage

Actor: System

Hệ thống kiểm tra NRIC và Student Category khi Student Record được tạo hoặc liên kết.

Với Student có EA hợp lệ, hệ thống liên kết Student Record với EA tương ứng.

Liên kết không tạo ra một EA mới và không thay đổi Account Balance.

Hệ thống phải xử lý trường hợp EA không tồn tại, EA đã Closed hoặc dữ liệu định danh không khớp.

HQ User và SU có thể xem trạng thái EA Linkage theo quyền truy cập.

## F10 – Student Enrolment Overview

Actors: School User, MOE HQ User, Parent (read-only)

SU có thể xem Student Records và Enrolments thuộc School mình.

HQ User có thể xem Student Enrolment theo School, Academic Year, Level và Class.

Người dùng có thể mở Student Detail để xem enrolment hiện tại và lịch sử phù hợp với quyền.

Parent đã được xác minh quan hệ và liên kết với Student có thể xem thông tin học tập/enrolment được phép hiển thị qua e-Service Portal.

Không cho phép School User truy cập Student Records của School khác nếu không có quyền.

Làm trong sprint sau

# R1:Education Account Lifecycle Management

CPF Transfer khi tài khoản đóng ở tuổi 16

# R3

## F09 – Bulk CSV Import for Academic Setup & Student Management

Actor: School User

SU có thể upload CSV để cấu hình School Academic Structure.

CSV có thể chứa Academic Year, Academic Level và Class Information.

SU có thể upload CSV để tạo nhiều Student Records cùng lúc.

CSV Student có thể bao gồm thông tin Class Assignment tương ứng.

Hệ thống kiểm tra file format, required fields, duplicate records và tính hợp lệ của School/Class.

Hệ thống hiển thị Import Preview trước khi thực hiện. [Proposed UX]

Sau khi xác nhận, hệ thống tạo các records hợp lệ và thực hiện Class Assignment theo dữ liệu CSV.

Hệ thống hiển thị Import Result, bao gồm Successful, Skipped và Failed Records. [Proposed UX]

Các records lỗi cần có lý do để SU chỉnh sửa và import lại.

# R2 – Education Account Top-Up

## Individual Top-Up

[CR] MOE HQ User có thể Top-Up tiền vào một Education Account cụ thể.

[PD] MOE HQ User truy cập Top-Up → Individual Top-Up.

[PD] MOE HQ User tìm kiếm Education Account theo Account Number hoặc Student NRIC.

[PD] Hệ thống hiển thị thông tin Account Holder, Account Status và Current Balance để Admin xác minh trước khi thực hiện.

[PD] MOE HQ User nhập Top-Up Amount và xác nhận giao dịch.

[PD] Hệ thống cộng tiền vào Education Account Balance và ghi nhận Top-Up Transaction khi thực hiện thành công.

[PD] Hệ thống hiển thị kết quả thành công hoặc thất bại.

## Bulk Top-Up Rule Configuration

[CR] MOE HQ User có thể thực hiện Batch Top-Up dựa trên các criteria như Age, Account Balance và Schooling Status.

[PD] MOE HQ User truy cập Top-Up → Bulk Top-Up.

[PD] MOE HQ User tạo một Bulk Top-Up Campaign cho Academic Year và Round cụ thể.

[PD] MOE HQ User cấu hình các điều kiện:
Age Range: Nhập Minimum Age và Maximum Age.
Account Balance: Nhập điều kiện so sánh và ngưỡng số dư, ví dụ Balance < SGD 100.
Schooling Status: Chọn Actively Enrolled trong Academic Year.
Top-Up Amount: Nhập số tiền cố định được cấp cho mỗi eligible Account.

[PD] MOE HQ User có thể lưu cấu hình để chuẩn bị thực hiện Bulk Top-Up.

[PD] Mỗi Campaign trong MVP áp dụng một bộ criteria và một Top-Up Amount.

Một kỳ có thể thực hiện nhiều scheme bulk top up khác nhau với amount khác nhau dựa trên criteria khác nhau

Business Rules / Constraints

[PD] Student phải đáp ứng tất cả configured criteria (AND logic).

[PD] Age được xác định từ DOB tại Eligibility Date của Campaign.

[PD] Schooling Status được xác định từ Student Enrolment của R3, không suy ra từ tuổi.

[PD] Hệ thống chỉ xét những Education Accounts tồn tại và đang Active.

[TBC] Balance Criteria được xét tại Eligibility Date

[TBC] Student không có Enrolment Record bị loại khỏi campaign auto

Cần có limit cho top-up budget.

## Bulk Top-Up Preview & Confirmation

[PD] MOE HQ User có thể Preview danh sách Education Accounts đủ điều kiện dựa trên configured criteria.

[PD] Hệ thống hiển thị các thông tin cơ bản của từng eligible Account: Student, Age, Current Balance, Schooling Status và Top-Up Amount.

[PD] Hệ thống hiển thị tổng số eligible Accounts và tổng Top-Up Amount dự kiến.

[PD] MOE HQ User kiểm tra kết quả và xác nhận trước khi xác nhận Bulk Top-Up.

[PD] Nếu criteria thay đổi, MOE HQ User phải Preview lại trước khi xác nhận.

### Business Rules / Constraints

[TBC] Có cho phép Admin loại một số Accounts khỏi danh sách Preview theo cách thủ công

## Bulk Top-Up ExecutionActor: MOE HQ User / System

[CR] MOE HQ User có thể thực hiện Top-Up hàng loạt.

[PD] MOE HQ User xác nhận Execute Bulk Top-Up.

[PD] Hệ thống xác định danh sách eligible Accounts theo Campaign.

[PD] Hệ thống kiểm tra Account Status và eligibility trước khi ghi tiền.

[PD] Hệ thống cộng Top-Up Amount tương ứng vào từng eligible Education Account.

[PD] Hệ thống ghi nhận Top-Up Transaction cho từng Account được nạp thành công.

[PD] Hệ thống hiển thị kết quả xử lý: Successful, Skipped và Failed.

## Top-Up History & ResultsActor: MOE HQ User

[PD] MOE HQ User có thể xem danh sách các Individual Top-Up Transactions và Bulk Top-Up Campaigns đã thực hiện.

[PD] MOE HQ User xem chi tiết kết quả của một Bulk Campaign, bao gồm danh sách Accounts được nạp, không được nạp và xử lý thất bại.

[PD] Hệ thống ghi nhận Transaction Reference, Top-Up Amount, thời điểm thực hiện và người thực hiện.

[PD] Các Top-Up Transactions thành công được phản ánh trong Education Account Transaction History của R1/R8.

Business Rules / Constraints

[PD] Failed Top-Up không làm tăng Account Balance.

[PD] Không chỉnh sửa trực tiếp một Top-Up Transaction đã thành công.

Khi nạp nhầm tiền admin có thể chọn tài khoản AE trong danh sách thành công để chỉnh sửa và cập nhật lại (trường hợp top up manually)

# R3 – Fee Management (MVP Functional Feature List)

Proposed MVP Fee Master Data

| Fee Type | Fee Component | Created By |
| :--- | :--- | :--- |
| 1. Academic Fees | School Fee | HQ |
|  | Miscellaneous Fee | HQ |
| 2. Examination Fees | Examination Fee | HQ |
|  | Supplementary Examination Fee | HQ |
| 3. Programme Fees | Enrichment Programme Fee | School A |
|  | Educational Excursion Fee | School A |
| 4. Student Services Fees | School Transport Fee | School A |
|  | School Meal Fee | School A |

## Fee Type & Fee Component Management

MOE HQ User có thể Create, View, Edit và Deactivate các Fee Types và Fee Components dùng chung cho toàn hệ thống. (có thời gian áp dụng)

School User (SU) có thể sử dụng các HQ Shared Fee Types/Components và tự tạo thêm School-specific Fee Types/Components theo nhu cầu thu phí của School mình.

Khi tạo Fee Type mới, người dùng nhập Fee Type Name, Description (nếu cần) và có thể thêm một hoặc nhiều Fee Components ngay trong cùng màn hình cấu hình.

Mỗi Fee Component có Component Name và Description (nếu cần).

Khi lưu, hệ thống tạo Fee Type cùng các Fee Components đã cấu hình bên trong.

Người dùng có thể xem danh sách các Fee Types đã tạo và mở từng Fee Type để xem các Components tương ứng.

Khi cần bổ sung khoản phí, người dùng mở Fee Type đã tồn tại và chọn Add Component; không cần chức năng tạo Component độc lập rồi gán vào Fee Type.

Một Fee Type có thể chứa nhiều Fee Components, nhưng mỗi Fee Component chỉ thuộc một Fee Type (quan hệ 1).

SU có thể xem và sử dụng các Fee Types/Components dùng chung của HQ cùng với danh mục phí riêng của School mình.

SU không được Edit hoặc Deactivate Fee Types và Fee Components do HQ quản lý.

SU được phép thêm Fee Component riêng của School vào Fee Type dùng chung của HQ. Component mới chỉ thuộc School đó, không ảnh hưởng đến danh mục chung hoặc các School khác.

SU chỉ được chỉnh sửa hoặc Deactivate các Fee Types/Components do School mình tạo.

Hệ thống kiểm tra trùng Fee Type Name và Component Name trong cùng phạm vi quản lý. [Đề xuất MVP]

Các Fee Types/Components đã được sử dụng trong Fee Publications hoặc Student Charges không được xóa vĩnh viễn; chỉ được Deactivate để giữ lịch sử.

Fee Types/Components đã Deactivate không được lựa chọn cho Fee Publications mới.

Đối với Fee Components do HQ quản lý: Amount được cấu hình riêng tại Fee Rate Configuration, dựa trên Education Stage, Student Category và thời gian hiệu lực. SU chỉ được xem, không được thay đổi.

Đối với Fee Components riêng của School: Không áp dụng Fee Rate Configuration của HQ. SU tự cấu hình Amount và thời gian áp dụng theo chính sách của School.

Các Fee Types và Components mẫu cho MVP:

Academic Fees: School Fee, Miscellaneous Fee.

Programme Fees: Enrichment Programme Fee, Educational Excursion Fee.

Student Services Fees: School Transport Fee, School Meal Fee.

SU có thể tạo thêm Fee Types và Components ngoài danh mục mẫu để đáp ứng nhu cầu thu phí riêng của School.

## Fee Rate Configuration

MOE HQ User có thể Create, View và Edit Fee Rates cho các Fee Components dùng chung do HQ quản lý.

Fee Rate được cấu hình chủ yếu theo Education Stage (Primary, Secondary, Pre-University) và Student Category (SC/PR/IS).

Khi cấu hình Fee Rate, HQ chọn Fee Component đã tồn tại và nhập các thông tin:

Education Stage

Student Category

Amount (SGD)

Effective From

Effective To

Một Fee Component có thể có nhiều Fee Rates khác nhau theo Education Stage và Student Category.

HQ có thể mở một Fee Component để xem danh sách các Fee Rates đã cấu hình và thêm mức phí mới nếu cần.

Hệ thống không cho phép các Fee Rates có cùng Fee Component + Education Stage + Student Category bị chồng lấn thời gian hiệu lực.

School User có thể xem các Fee Components và Fee Rates của HQ, bao gồm Amount và thời gian áp dụng, nhưng không được chỉnh sửa.

Khi SU tạo Fee Publication sử dụng Component của HQ, hệ thống xác định mức phí phù hợp dựa trên Education Stage, Student Category và thời gian hiệu lực.

Education Stage của Student được xác định thông qua Academic Level trong Enrolment Profile (ví dụ P3 thuộc Primary, S2 thuộc Secondary).

Nếu không có Fee Rate phù hợp, hệ thống thông báo khoản phí chưa được cấu hình đầy đủ và không tự xác định Amount.

Fee Rate Configuration không áp dụng cho các Fee Components riêng của School, kể cả khi nằm trong Fee Type dùng chung của HQ.

Đối với Fee Components riêng, School User tự cấu hình Amount và thời gian áp dụng theo chính sách của trường.

Fee Rates chỉ xác định mức tiền phải thu, không tự động tạo Student Charges. Student Charges chỉ được tạo khi Fee Publication được Publish.

Student Charges đã phát hành giữ nguyên Amount tại thời điểm phát hành, không tự động thay đổi khi HQ cập nhật Fee Rate.

## Fee Publication & Target Configuration – Các quy tắc cập nhật

School User có thể lựa chọn các HQ Shared Fee Components hoặc School-specific Fee Components đã được cấu hình trước đó trong R3 và đang Active để tạo Fee Publication. SU vẫn có thể tự tạo thêm School-specific Components thông qua Fee Type & Fee Component Management khi có nhu cầu.

Việc Publish Fee và tạo Student Charges không phụ thuộc vào việc Fee Component đã được cấu hình trong Subsidy Matrix của R4 hay chưa.

HQ Fee Components không bắt buộc phải được phát hành toàn bộ; SU lựa chọn các khoản cần thu theo nhu cầu và chính sách áp dụng.

SU không được thay đổi Fee Rates đã được HQ cấu hình.

SU có thể tạo nhiều Fee Publications cho cùng một Fee Component ở các Billing Period hoặc đợt thu khác nhau.

Mỗi Fee Publication ghi nhận tối thiểu: Publication Name, School, Academic Year, Billing Period, Fee Components, Target Students Level (khối) và Due Date.

Trước khi Publish, hệ thống cho SU Preview danh sách Students, Components và Amount dự kiến.

Hệ thống kiểm tra các Student Charges đã phát hành để phát hiện khoản thu có khả năng bị trùng cho cùng Student, Fee Component và kỳ/đợt thu.

Hệ thống không được tạo Student Charges trùng do Publish lại cùng một Publication.

Với trường hợp cùng Fee Component được thu nhiều lần, các đợt thu phải có thông tin phân biệt rõ ràng.

MVP chưa tự động kiểm soát số lần tối đa một Fee Component được phép thu trong năm. Việc tuân thủ chính sách về tần suất thu phí thuộc trách nhiệm quản lý nghiệp vụ ngoài hệ thống. [Working Assumption – cần client xác nhận]

## Student Charge GenerationActor: System

[FS] Khi Fee Publication được Publish, hệ thống xác định danh sách Students phù hợp với Target thông qua Enrolment và Class Assignment tại Eligibility Date.

[FS] Hệ thống lấy Fee Rate phù hợp hoặc Fixed Amount đã cấu hình để tính khoản phí cho từng Student.

[FS] Hệ thống tạo Student Charge cho mỗi Student đủ điều kiện, bao gồm Fee Component, Amount, Tax (nếu có), Due Date và Status.

[FS] Chỉ Student Charge ở trạng thái POSTED mới được hiển thị cho Parent.

[FS] Một Student không được tạo hai Student Charges từ cùng một Fee Publication.

[PD] MVP chỉ cần hỗ trợ tính khoản phí cơ bản và Tax theo cấu hình sẵn có; không xây dựng Tax Rule Engine nâng cao. [TBC]

## Student Charge Viewing & ManagementActor:

MOE HQ User / School User

Khi School User xác nhận Publish Fee Publication, hệ thống tự động xác định danh sách Students cần thu phí dựa trên Target Students đã chọn.

Hệ thống sử dụng Enrolment Profile để xác định School, Academic Year, Education Stage, Academic Level và Class của từng Student tại thời điểm áp dụng.

Hệ thống xác định Amount cho từng Fee Component:

HQ Components: Lấy Amount từ Fee Rate đã cấu hình theo Education Stage, Student Category và thời gian hiệu lực.

School-specific Components: Lấy Amount do SU cấu hình trong Fee Publication.

Hệ thống tạo một Student Charge cho mỗi Student và mỗi Fee Component được phát hành.

Mỗi Student Charge ghi nhận tối thiểu: Student, School, Fee Component, Original Amount, Due Date, Status và Fee Publication Reference.

Các Student Charges được tạo thành công có trạng thái POSTED và được chuyển sang danh sách Outstanding Fees để Parent xem trên e-Service Portal (R9).

Hệ thống không tạo Student Charges trùng lặp khi cùng một Fee Publication được Publish lại.

Student Charges được tạo với Original Amount độc lập với trạng thái FAS Grant của Student. Subsidy Amount và Net Payable có thể được cập nhật sau khi Student được Grant FAS hợp lệ theo business rules của R4.

SU có thể tạo nhiều Fee Publications cho cùng một Fee Component ở các kỳ hoặc đợt thu khác nhau.

Trước khi tạo Charges, hệ thống kiểm tra các khoản đã phát hành để phát hiện trường hợp cùng Student bị thu trùng Fee Component trong cùng kỳ/đợt thu.

Nếu thiếu Fee Rate, Amount không hợp lệ hoặc Student không có Enrolment phù hợp, hệ thống phải thông báo lỗi và không tạo Charge sai.

Student Charges đã POSTED giữ nguyên Original Amount và thông tin School/Enrolment tại thời điểm phát hành, kể cả khi Student chuyển lớp, chuyển trường hoặc Fee Rate thay đổi.

## Outstanding Fee Integration with R9

Các Student Charges được tạo thành công và có trạng thái POSTED sẽ được cung cấp cho Parent Portal (R9) để hiển thị các khoản phí cần thanh toán.

Hệ thống sử dụng các Student Charges để hiển thị Outstanding Fees / Invoice cho từng Student.

Mỗi khoản phí hiển thị tối thiểu: Fee Component, Original Amount, Subsidy Amount (nếu có), Net Payable, Due Date và Payment Status.

Parent chỉ được xem và thanh toán các khoản phí của Students đã được xác minh quan hệ và liên kết với tài khoản Parent.

Parent có thể xem danh sách các khoản phí chưa thanh toán và chọn khoản muốn thanh toán.

R9 chịu trách nhiệm xử lý thanh toán bằng Education Account Balance, Online Payment hoặc Split Payment theo các phương thức được hỗ trợ.

Sau khi thanh toán thành công, hệ thống cập nhật trạng thái thanh toán và số tiền còn phải trả, tránh hiển thị khoản đã thanh toán đầy đủ như Outstanding Fee.

Các khoản phí đã thanh toán vẫn được giữ lại để Parent xem lịch sử.

R3 chịu trách nhiệm tạo và quản lý Student Charges; R9 chịu trách nhiệm Payment Processing và cập nhật kết quả thanh toán.

## Fee Integration with R4

R4 sử dụng các Fee Components đã tồn tại trong R3 để cấu hình Subsidy Matrix theo từng FAS Scheme, Education Stage/Academic Level và Fee Component.

HQ Admin có thể chọn HQ Shared Fee Components cho MOEFAS; SU có thể chọn HQ Shared Components và School-specific Components thuộc trường mình cho SBFAS.

HQ/SU quyết định Fee Components nào được hỗ trợ. Khi có Component mới, SU có thể bổ sung vào Subsidy Matrix nếu cần; hệ thống không bắt buộc mọi Component phải được trợ cấp.

Fee Publication hoạt động độc lập với FAS. SU có thể Publish Fee dù chưa có Subsidy Rule hoặc FAS Grant.

Khi FAS Grant được Finalize/Published trước Due Date và Student Charge chưa thanh toán, System áp dụng Subsidy theo Matrix của Scheme đã Grant.

System giữ riêng Original Amount, Subsidy Amount và Net Payable. Net Payable = Original Amount − Subsidy Amount; Subsidy không vượt Original Amount và không làm thay đổi Original Amount.

Nếu không có FAS Grant hợp lệ hoặc Fee Component không được hỗ trợ, Subsidy Amount = 0. R9 sử dụng Net Payable để hiển thị Outstanding Fees và xử lý Payment.

# R4

## FAS Application Submission

Actors: Parent / School User (SU)

System hỗ trợ hai phương thức nộp FAS Application:

Online Application: Parent nộp trên Parent Portal.

Paper Application: Parent nộp đơn giấy tại School; SU nhập Application vào hệ thống.

Online Application:

Parent chỉ có thể chọn Student đã có Education Account (EA) liên kết và được xác minh quan hệ.

System tự động điền Student Information từ dữ liệu có sẵn.

Parent nhập Household Information, Income Details và các thông tin cần thiết, xác nhận Declaration và Submit Application.

Paper Application:

SU có thể tiếp nhận và tạo Application cho tất cả Students thuộc School mình, bao gồm cả Students chưa có EA.

SU chọn Student Record trong R3 để liên kết với Application.

SU có thể nhập thông tin thủ công hoặc Upload bản scan/photo của đơn giấy.

MVP hỗ trợ Simulated OCR để prefill một số fields từ file mẫu; SU có thể kiểm tra và chỉnh sửa trước khi Submit.

Cả hai phương thức sử dụng chung các nhóm dữ liệu:

Student Information: Student, NRIC, Citizenship, School, Academic Level.

Parent/Guardian Information: Name, NRIC/FIN, Relationship, Contact Number.

Household Information: GHI, Household Size và PCI do System tính.

Assistance Details: SBFAS Consideration và Family Circumstances/Notes (optional).

Declaration & Supporting Documents: Thông tin xác nhận phù hợp với từng phương thức nộp.

System lưu Application với các thông tin: Application ID, Student, Submission Method (Online/Paper), Submitted Date và Status.

Sau khi Submit, System sử dụng cùng quy trình MOEFAS Eligibility Assessment, Auto Grant hoặc SBFAS Manual Review, không phân biệt phương thức nộp.

Application được liên kết với Student Record và các Student Charges phù hợp từ R3 để phục vụ Subsidy Calculation.

MVP chưa cần triển khai OCR thật; việc xử lý Student chưa có EA được tách khỏi chức năng EA Payment trên R9.

## FAS Scheme Management

System hỗ trợ 2 Scheme Types: MOEFAS và SBFAS.

MOE HQ Admin quản lý MOEFAS Schemes; School User quản lý SBFAS Schemes thuộc trường mình.

Admin có thể Create, View, Edit, Activate/Deactivate Schemes theo quyền được cấp.

Mỗi Scheme bao gồm: Scheme Code, Name, Type, Description, Effective Date, Expiry Date và Status.

Một MOEFAS Scheme có thể áp dụng cho nhiều trường đủ điều kiện; mỗi SBFAS Scheme được liên kết với một School.

Trước khi Activate, MOEFAS Scheme phải có Eligibility Criteria và Subsidy Matrix; SBFAS Scheme phải có Subsidy Matrix.

Mỗi Scheme có thể được sử dụng trong các đợt xét duyệt với Budget và Application Deadline tương ứng. Chi tiết được quy định trong FAS Application & Batch Processing.

## MOEFAS Eligibility Configuration

Actor: MOE HQ Admin

HQ Admin có thể Create, View và Edit Eligibility Criteria riêng cho từng MOEFAS Scheme. MVP chỉ cần cấu hình sẵn một Scheme mẫu.

MVP hỗ trợ ba nhóm Eligibility Criteria:

Citizenship: Quốc tịch đủ điều kiện.

Household Income: GHI Threshold và PCI Threshold.

Eligible Schools: Chọn Schools từ danh sách R3.

System đánh giá Income theo logic GHI ≤ Threshold OR PCI ≤ Threshold.

Student được đánh giá MOEFAS Eligible khi đáp ứng Citizenship AND (GHI OR PCI) AND Eligible School, dựa trên Active Enrolment Profile.

Khi Application được Submit, System tự động đánh giá Eligibility và tính Subsidy Amount theo Subsidy Matrix.

Nếu Eligible và Remaining Budget đủ, System Auto Grant FAS, cập nhật Application Status và trừ Subsidy Amount khỏi Remaining Budget.

Nếu Not Eligible, System ghi nhận MOEFAS Not Eligible và chuyển sang SBFAS Review theo quy trình áp dụng.

Subsidy chỉ được áp dụng cho Student Charges chưa thanh toán và có Due Date chưa đến hạn; R9 cập nhật Net Payable tương ứng.

MVP chưa cần Batch Processing, Financial Priority Ranking hoặc các Eligibility Criteria nâng cao.

## SBFAS Eligibility

Actor: School User (SU)

Mỗi SBFAS Scheme bao gồm Scheme Information, Eligibility Description và Subsidy Matrix.

Eligibility Description là đoạn free-text ngắn mô tả hoàn cảnh hoặc nhóm học sinh mà Scheme hướng tới, dùng làm cơ sở cho School User đánh giá và AI Recommendation.

MVP không yêu cầu cấu hình hard income thresholds hoặc Eligibility Rule Engine cho SBFAS.

School User có thể Create/Edit Eligibility Description và Subsidy Matrix của các SBFAS Schemes thuộc School mình.

Scheme phải có Eligibility Description và Subsidy Matrix hợp lệ trước khi Activate.

Khi review FAS Application, System có thể hiển thị AI Recommendation về SBFAS Scheme phù hợp; School User là người quyết định Grant hoặc Reject.

## SBFAS Manual Review & Decision

Mỗi SBFAS Scheme bao gồm Scheme Information, Eligibility Description và Subsidy Matrix.

Eligibility Description là đoạn free-text ngắn mô tả hoàn cảnh hoặc nhóm học sinh mà Scheme hướng tới, dùng làm cơ sở cho School User đánh giá và AI Recommendation.

MVP không yêu cầu cấu hình hard income thresholds hoặc Eligibility Rule Engine cho SBFAS.

School User có thể Create/Edit Eligibility Description và Subsidy Matrix của các SBFAS Schemes thuộc School mình.

Scheme phải có Eligibility Description và Subsidy Matrix hợp lệ trước khi Activate.

Khi review FAS Application, System có thể hiển thị AI Recommendation về SBFAS Scheme phù hợp; School User là người quyết định Grant hoặc Reject.

## Subsidy Matrix Configuration

Actor: MOE HQ Admin / School User

Mỗi FAS Scheme có một Subsidy Matrix riêng.

Subsidy Matrix được cấu hình theo Education Stage × Fee Component (Primary, Secondary, Pre-University).

Fee Components được lấy từ danh mục đã cấu hình trong R3, theo quyền quản lý của HQ/SU.

User cấu hình Subsidy Type (Percentage / Fixed Amount) và Subsidy Value cho từng Education Stage và Fee Component.

Một Scheme có thể hỗ trợ nhiều Fee Components với các mức trợ cấp khác nhau; Fee Components không có trong Matrix sẽ không được hỗ trợ.

Không cho phép các Subsidy Rules trùng trong cùng Scheme, Education Stage và Fee Component.

Percentage Subsidy phải từ 0–100%; Subsidy Amount không được vượt Original Charge.

System xác định Education Stage của Student thông qua Academic Level trong Active Enrolment Profile để áp dụng Subsidy Rule tương ứng.

#### Ví dụ Subsidy Matrix

1. MOEFAS – Government Financial Assistance 2026

Eligibility: Singapore Citizen, GHI ≤ SGD 4,000 OR PCI ≤ SGD 1,000, thuộc Eligible Schools.

| HQ Fee Component | Primary | Secondary | Pre-University |
| :--- | :--- | :--- | :--- |
| School Fee | N/A | 100% | 100% |
| Miscellaneous Fee | 100% | 100% | 100% |

2. SBFAS – School A

3 Schemes – School User

Cả ba Scheme đều dùng các School-specific Fee Components đã tạo trong R3. Để đơn giản hóa, các tỷ lệ dưới đây áp dụng cho Primary – All Levels (P1–P6) trong demo.

SBFAS – High Support : Khó khăn tài chính nghiêm trọng

| Fee Component | Primary | Secondary | Pre-University |
| :--- | :--- | :--- | :--- |
| Enrichment Programme Fee | 100% | 100% | 100% |
| Educational Excursion Fee | 100% | 100% | 100% |
| School Transport Fee | 75% | 50% | 30% |
| School Meal Fee | 75% | 50% | 30% |

SBFAS – Medium Support : Áp lực tài chính đáng kể

| Fee Component | Primary | Secondary | Pre-University |
| :--- | :--- | :--- | :--- |
| Enrichment Programme Fee | 50% | 50% | 50% |
| Educational Excursion Fee | 50% | 50% | 50% |
| School Transport Fee | 50% | 30% | 20% |
| School Meal Fee | 50% | 30% | 20% |

SBFAS – Basic Support

Cần hỗ trợ một phần chi phí

| Fee Component | Primary | Secondary | Pre-University |
| :--- | :--- | :--- | :--- |
| Enrichment Programme Fee | 25% | 25% | 25% |
| Educational Excursion Fee | 25% | 25% | 25% |
| School Transport Fee | 25% | 15% | 10% |
| School Meal Fee | 25% | 15% | 10% |

## FAS Eligibility Assessment & Grant Processing

Actor: System / School User

System đánh giá MOEFAS Eligibility khi FAS Application được submit.

Nếu Eligible, System tính Subsidy Amount theo Subsidy Matrix và kiểm tra Remaining Budget của Scheme. Nếu đủ Budget, System Auto Grant, trừ Budget và cập nhật Application Status.

Nếu Not Eligible: System chuyển Application sang School User để review SBFAS.

School User có thể chọn SBFAS Scheme phù hợp và Grant hoặc Reject Application.

System lưu Assessment Result, Grant Decision, Scheme Applied và Decision Date.

System phân biệt MOEFAS Not Eligible với FAS Application Rejected.

Nếu MOEFAS Eligible nhưng không đủ Budget, System ghi nhận Eligible – Insufficient Budget, không Auto Grant.

## Subsidy Application to Student Charges

Actor: System

Khi Student được Grant FAS trước Due Date và Student Charge chưa được thanh toán, System áp dụng Subsidy Rules của Scheme đã Grant cho các Student Charges phù hợp từ R3.

Subsidy được tính theo Education Stage và Fee Component của Student Charge.

System lưu riêng Original Amount, Subsidy Amount và Net Payable.

Net Payable = Original Amount − Subsidy Amount.

Subsidy Amount không được vượt Original Amount; Net Payable không được âm.

R9 sử dụng Net Payable để hiển thị Outstanding Fees và xử lý Payment.

MVP không tự động điều chỉnh hồi tố các Student Charges đã thanh toán trước khi Student được Grant FAS.

# R9 – Additional Features: Payment Flow & Gateway Integration

Khi Parent chọn một Outstanding Invoice, System hiển thị Net Payable và Available EA Balance của Student.

Parent có thể bật/tắt checkbox Use EA Balance và nhập số tiền EA muốn sử dụng:

Checkbox OFF: Thanh toán toàn bộ bằng Online Payment.

Checkbox ON: Parent chọn số tiền EA muốn sử dụng, có thể là toàn bộ hoặc một phần.

EA Amount không được vượt Available EA Balance hoặc Net Payable.

System tự động tính Online Payment Amount = Net Payable − EA Amount. Nếu Online Payment Amount = 0, System xử lý EA Payment mà không cần chuyển sang Payment Gateway.

Nếu Online Payment Amount > 0, System tạo Payment Session và redirect Parent sang Mock Third-party Payment Gateway UI để thực hiện giao dịch.

Mock Payment Gateway hỗ trợ mô phỏng Payment Success / Failed và redirect Parent trở lại R9 để hiển thị Payment Result.

Khi Payment thành công, System:

Trừ EA Amount đã sử dụng khỏi EA Balance.

Ghi nhận EA Transaction và Payment Reference.

Cập nhật Invoice/Student Charge thành Paid và cập nhật Outstanding Fees.

Hiển thị Payment Confirmation/Receipt cho Parent.

Nếu Payment thất bại, System không đánh dấu Invoice là Paid và phải đảm bảo EA Balance không bị trừ vĩnh viễn. Hệ thống ngăn xử lý trùng cùng một Payment Transaction.
