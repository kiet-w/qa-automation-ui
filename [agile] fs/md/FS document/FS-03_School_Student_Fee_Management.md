# FS-03: School, Student & Fee Management (Requirement 3)


# FUNCTIONAL SPECIFICATION – R3: School, Student và Fee Management


## 1. Introduction


### 1.1. Overview

Requirement 3 yêu cầu MOE HQ User và School User quản lý danh sách School, Academic Level (level/cohort), Class, Student trong từng Class, cùng Fee Type và Fee Component mà học sinh phải đóng. Học sinh Singaporean có thể dùng số dư Education Account để thanh toán các khoản phí đủ điều kiện.

Tài liệu này gồm hai nhóm chức năng:

School Management (F01–F08): tạo School, cấp tài khoản School User, cấu hình Academic Year/Level/Offering và Class, quản lý Student, enrolment và class assignment, xử lý chuyển lớp/chuyển trường và liên kết Student với Education Account.

Fee Management (F09–F16): Fee Type, Fee Component, Fee Rate Rule, Fee Publication, Publication Target, Publication Recipient, Student Charge, Student Charge Adjustment.

Quy tắc nghiệp vụ liên quan đến thanh toán bằng Education Account được ghi nhận ở mục 4; chi tiết payment thuộc requirement khác (R9, e-Service Portal).


### 1.2. Actors



| Actor | Mô tả |
| --- | --- |
| MOE HQ User | Tạo School, tạo tài khoản và assign School User; quản lý Fee Component/cấu hình phí tập trung; chỉnh sửa Student khi chuyển lớp/chuyển trường; publish fee. |
| School User | Quản lý Level, Class, Student của trường mình; thực hiện các thao tác fee trong phạm vi được phân quyền. |
| System | Validate dữ liệu, xác định rate, resolve target, generate Student Charge, liên kết Student với Education Account. |



### 1.3. Scope

In Scope: School Management, School User assignment, Academic Level, Class, Student, Student Enrolment và Class assignment, Student transfer, Education Account linkage, Fee Type, Fee Component, Fee Rate Rule, Fee Publication, Publication Target, Publication Recipient, Student Charge, Student Charge Adjustment, quy tắc Education Account payment eligibility.

Out of Scope (tài liệu này): Payment transaction, trừ số dư Education Account, reconciliation, màn hình chọn thanh toán của phụ huynh (e-Service Portal), tạo/đóng Education Account tự động theo tuổi (R1), FAS subsidy (R4).

Dependencies: academic_years, users, education_accounts (R1) được xem là entity có sẵn.


### 1.4. Assumptions và Limitations



| ID | Working Assumption |
| --- | --- |
| WA-R3-01 | HQ tạo School và School User; việc bàn giao thông tin tài khoản cho School thực hiện ngoài hệ thống (giấy tờ). |
| WA-R3-02 | Hiện tại Student được School User nhập manual; chưa có import/đồng bộ từ hệ thống ngoài. |
| WA-R3-03 | School User tự khai báo School Level Offering (cấp học trường dạy trong năm học) và Class của trường mình; Academic Year và Academic Level là master data. |
| WA-R3-04 | Khi Student chuyển lớp hoặc chuyển trường, HQ User cập nhật lại enrolment và class assignment cho khớp với lớp hiện tại (đóng bản ghi cũ, mở bản ghi mới). |
| WA-R3-05 | Student Singaporean (students.category = SC) khi được thêm vào Class sẽ được liên kết với Education Account. |
| WA-R3-06 | Fee Type là phân loại cấp cao; Fee Component là khoản phí cụ thể và là danh mục phí, không phải khoản phải thu. |
| WA-R3-07 | Fee Rate Rule là cùng một fee_components thì đối với các đối tượng student khác nhau lại có mức charge khác nhau, Fee Rate Rule allows việc đó |
| WA-R3-08 | Student Charge là khoản phải thu (outstanding charge). Phụ huynh xem danh sách charge và tự tick chọn khoản muốn thanh toán; hệ thống không tự động trừ/thu toàn bộ. |
| WA-R3-09 | Adjustment như FAS (func4 sau này) không sửa trực tiếp số tiền gốc của Student Charge mà tuỳ vào account của từng học sinh. |



## 1.4 Definitions, Acronyms and Abbreviations



| Thuật ngữ | Giải thích |
| --- | --- |
| EA | Education Account, tài khoản tiền giáo dục của học sinh Singapore Citizen |
| MOE HQ / School user | Người dùng Bộ Giáo dục cấp trung ương / người dùng của từng trường |
| Academic year | Năm học, khoảng [start_date, end_date_exclusive) |
| Academic level | Cấp lớp: P1 đến P6, S1…, JC1 |
| Offering | Bản ghi cho biết trường nào dạy cấp nào trong năm học nào (school_level_offerings) |
| Class | Lớp (ví dụ P6A) nằm dưới một offering |
| Enrollment | Việc học sinh học tại một trường trong một khoảng thời gian |
| Class assignment | Việc một enrollment học một lớp trong một khoảng thời gian |
| Fee type | Phân loại cấp cao của phí |
| Fee component | Khoản phí cụ thể có thể áp dụng cho học sinh; là danh mục, không phải khoản nợ |
| Fee rate rule | Mức phí của một fee component theo cấp học và loại cư trú |
| Fee batch | Đợt phát hành phí cho học sinh (fee_publications); thuộc function riêng |
| GST | Thuế hàng hóa và dịch vụ; component có cờ is_apply_tax, rule có cờ is_price_include_tax |
| SC / PR / IS | Nhóm cư trú của học sinh, hiểu là Singapore Citizen / Permanent Resident / International Student (cần xác nhận, Q11) |
| end_exclusive | Ngày đầu tiên không còn hiệu lực |



## 2. System Process Overview


### 2.1. School Setup Process

HQ User mở Academic Year (year_number, start_date, end_date_exclusive, status) và duy trì danh mục Academic Level.

HQ User tạo School.

HQ User tạo tài khoản School User và assign vào School; thông tin tài khoản được bàn giao cho School qua giấy tờ.

School User khai báo School Level Offering (cấp học School dạy trong năm học).

School User tạo Class dưới offering.

School User tạo Student (nhập manual) và tạo enrolment tại School.

School User gán enrolment vào Class (class assignment).

Với Student có category SC, System liên kết Student với Education Account.


### 2.2. Student Transfer Process

School User báo HQ về việc Student đổi lớp hoặc chuyển trường (ngoài hệ thống hoặc qua kênh được thống nhất).

Đổi lớp trong cùng School: HQ User đóng class assignment cũ (assigned_to_exclusive = ngày hiệu lực) và mở assignment mới; enrollment giữ nguyên.

Chuyển trường: HQ User đóng enrollment và assignment ở School A, mở enrollment (enrolled_from = cùng ngày hiệu lực) và assignment mới ở School B.

Bảng students không đổi; các Student Charge đã phát hành giữ nguyên.


### 2.3. Fee Configuration và Publication Process

HQ User tạo Fee Type và Fee Component.

HQ User chọn đối tượng áp dụng (Level, Class, citizenship hoặc Student cụ thể) và cấu hình giá bằng Fee Rate Rule hoặc Fixed Amount.

HQ User tạo Fee Publication: chọn Fee Component, School, Academic Year, billing period, charge date và payment deadline (due date).

Khi publish, System resolve danh sách Student theo eligibility_date, xác định giá theo pricing_date, tạo một Student Charge cho mỗi Student.

Student Charge xuất hiện trong danh sách outstanding charges để phụ huynh xem và chọn thanh toán (R9).


### 2.4. Charge Adjustment Process

User có quyền chọn Student Charge, nhập adjustment amount và reason code; System ghi nhận người tạo, thời điểm tạo; approval theo quy tắc được xác nhận; số tiền gốc luôn được giữ nguyên.


## 3. Detailed Functions and Solution Design


### 3.1.1 Function Description


### Sub-functions



| Mã | Sub-function | Actor | Mục đích |
| --- | --- | --- | --- |
| F01 | School Management | MOE HQ User | Tạo và duy trì hồ sơ School (school_code, tên, loại trường, status) |
| F02 | School User Account Assignment | MOE HQ User | Tạo tài khoản School User và assign vào School |
| F03 | Academic Year, Academic Level và School Level Offering | HQ User (Year, Level); School User (offering) | Master data và cấp học School dạy (cấp 1 hay 2) trong năm học |
| F04 | Class Management | School User | Tạo Class dưới offering |
| F05 | Student Management | School User | Tạo và cập nhật hồ sơ Student (nhập tay) |
| F06 | Student Enrolment và Class Assignment | School User | Gắn Student vào School và Class, giữ lịch sử |
| F07 | Student Transfer và Class Change | MOE HQ User | Đóng và mở enrolment, assignment khi đổi lớp, chuyển trường |
| F08 | Education Account Linkage | System | Liên kết Student SC với Education Account |
| F09 | Fee Type Management | HQ User, School User (theo phân quyền) | Phân loại phí cấp cao |
| F10 | Fee Component Management | HQ User; School User nếu được cho phép | Danh mục khoản phí |
| F11 | Fee Rate Rule Management | HQ User, School User (theo phân quyền) | Mức phí theo Level và category |
| F12 | Fee Publication Management | HQ User, School User | Phát hành phí cho School, kỳ phí, charge date, deadline |
| F13 | Publication Target Configuration | HQ User, School User | Xác định nhóm Student nhận phí |
| F14 | Publication Recipient Resolution | System | Resolve và lưu danh sách recipient |
| F15 | Student Charge Generation and Management | System; User có quyền (manual) | Tạo và quản lý khoản phải thu |
| F16 | Student Charge Adjustment Management | User có quyền; Approver | Điều chỉnh tăng hoặc giảm, có audit |



#### Business Rules

Nhóm A – School Management (F01 đến F08)



| Mã | Quy tắc | F |
| --- | --- | --- |
| BR-R3-01 | moe_school_code, khi có giá trị, phải duy nhất | F01 |
| BR-R3-02 | School mới tạo ở trạng thái active; School inactive không dùng cho offering hoặc Fee Publication mới, dữ liệu lịch sử giữ nguyên | F01 |
| BR-R3-03 | Không xóa School đã có offering, enrolment hoặc Student Charge; chỉ deactivate | F01 |
| BR-R3-04 | Mỗi School User phải gắn với ít nhất một School hợp lệ | F02 |
| BR-R3-05 | School User chỉ truy cập dữ liệu thuộc School của mình | F02 |
| BR-R3-06 | Cơ chế cấp mật khẩu lần đầu và đổi mật khẩu [TBC] | F02 |
| BR-R3-07 | year_number duy nhất; start_date nhỏ hơn end_date_exclusive | F03 |
| BR-R3-08 | academic_levels.code duy nhất; education_stage thuộc PRIMARY, SEC hoặc PRE_UNI | F03 |
| BR-R3-09 | Mỗi bộ ba (School, Academic Year, Academic Level) chỉ có một offering | F03 |
| BR-R3-10 | Offering chỉ tạo với School, Academic Year, Academic Level hợp lệ; có cho tạo offering ở năm học CLOSED hay không [TBC, Q26] | F03 |
| BR-R3-11 | Không xóa offering đã có Class; Academic Level đang có offering chỉ được deactivate | F03 |
| BR-R3-12 | Class phải thuộc một offering; chưa có offering thì không tạo được Class | F04 |
| BR-R3-13 | class_code duy nhất trong cùng offering; class_kind mặc định FORM | F04 |
| BR-R3-14 | Class gắn với năm học: sang năm mới tạo Class mới dưới offering mới (P6A-2026 và P6A-2027 là hai bản ghi); không xóa Class đã có assignment | F04 |
| BR-R3-15 | Student là định danh lâu dài, độc lập School và Class; id không đổi khi chuyển lớp, chuyển trường hoặc nghỉ học | F05 |
| BR-R3-16 | category thuộc SC, PR hoặc IS; đây là nhóm cư trú dùng cho Education Account eligibility và có thể dùng cho rate rule [TBC, Q22] | F05 |
| BR-R3-17 | Chống tạo trùng Student theo (source_system, source_reference) [đề xuất, Dev xác nhận] | F05 |
| BR-R3-18 | students không lưu trạng thái đang học (thuộc enrolment và assignment); không xóa Student đã có enrolment hoặc Student Charge | F05 |
| BR-R3-19 | Ngày kết thúc dạng exclusive là ngày đầu tiên không còn hiệu lực; null nghĩa là đang hiệu lực; khi có giá trị phải lớn hơn ngày bắt đầu | F06 |
| BR-R3-20 | Hai khoảng liền kề (kết thúc 01/07, bắt đầu 01/07) không chồng lấn; Student không được có hai enrolment chồng lấn [TBC] | F06 |
| BR-R3-21 | Class của assignment phải cùng School với enrolment; FK không tự đảm bảo nên backend phải validate | F06 |
| BR-R3-22 | Khoảng assignment nằm trong khoảng enrolment và trong năm học của Class (qua offering) | F06 |
| BR-R3-23 | Tại một ngày, một enrolment chỉ có một assignment hiệu lực [TBC] | F06 |
| BR-R3-24 | Đổi lớp trong cùng School = đóng assignment cũ và mở assignment mới; không ghi đè bản ghi cũ | F07 |
| BR-R3-25 | Chuyển trường = đóng enrolment và assignment ở School A, mở enrolment và assignment ở School B; hai khoảng liền kề không chồng lấn; Student id không đổi | F07 |
| BR-R3-26 | Student Charge đã phát hành giữ nguyên enrolment và School tại thời điểm phát hành; mọi thay đổi ghi audit (người sửa, thời điểm, giá trị cũ và mới); xử lý charge chưa thanh toán khi chuyển trường [TBC, Q17] | F07 |
| BR-R3-27 | Chỉ Student có category = SC được liên kết Education Account; liên kết một lần cho mỗi Student, không làm thay đổi số dư; Account chưa tồn tại (dưới 7 tuổi) hoặc đã đóng (từ 16 tuổi) xử lý theo Q16 | F08 |


Nhóm B – Fee Management (F09 đến F16)



| Mã | Quy tắc | F |
| --- | --- | --- |
| BR-R3-28 | Mỗi Fee Type có code duy nhất | F09 |
| BR-R3-29 | Fee Type mới mặc định active | F09 |
| BR-R3-30 | Fee Type inactive không dùng cho Fee Component hoặc cấu hình mới | F09 |
| BR-R3-31 | Dữ liệu hiện có giữ nguyên khi deactivate | F09 |
| BR-R3-32 | Fee Component phải tham chiếu Fee Type tồn tại | F10 |
| BR-R3-33 | component_code duy nhất | F10 |
| BR-R3-34 | Mặc định active; is_apply_tax mặc định true | F10 |
| BR-R3-35 | Component inactive không dùng cho cấu hình mới | F10 |
| BR-R3-36 | owner_school_id null nghĩa là component do MOE tạo | F10 |
| BR-R3-37 | Rule phải tham chiếu Fee Component hợp lệ | F11 |
| BR-R3-38, 39 | academic_level_id hoặc student_category null nghĩa là áp dụng mọi Level hoặc category | F11 |
| BR-R3-40 | currency_code mặc định SGD; is_price_include_tax mặc định false | F11 |
| BR-R3-41 | Rate áp dụng được xác định theo pricing_date và thuộc tính Student | F11 |
| BR-R3-42 | Phân biệt rõ rate-rule pricing và fixed-amount pricing trong Fee Publication | F11 |
| BR-R3-43 | Khi nhiều rule cùng khớp, áp dụng precedence được xác nhận [TBC, Q03]; đề xuất: rule cụ thể nhất thắng, sau đó effective_from mới nhất | F11 |
| BR-R3-44 | Publication phải tham chiếu Fee Component, School, Academic Year hợp lệ | F12 |
| BR-R3-45 | period_end_exclusive lớn hơn period_start | F12 |
| BR-R3-46 | eligibility_date xác định enrolment và class dùng để resolve target | F12 |
| BR-R3-47 | pricing_date xác định rate rule có hiệu lực | F12 |
| BR-R3-48 | RATE_RULE: các trường fixed price phải NULL; FIXED_AMOUNT: các trường fixed price phải hợp lệ | F12 |
| BR-R3-49 | Status PUBLISHED bắt buộc có published_by và published_at | F12 |
| BR-R3-50 | Target phải thuộc School của publication | F12 |
| BR-R3-51 | Ngăn xử lý publish trùng (idempotent); dùng row_version chống cập nhật đồng thời | F12 |
| BR-R3-52 | due_date không được trước charge_date [TBC, Q18] | F12 |
| BR-R3-53 | Chỉ dùng giá trị hợp lệ của Fee_Publication_Target_Modes và Fee_Publication_Target_Types | F13 |
| BR-R3-54 | Class target phải thuộc một offering của School; Level target phải có offering của School trong Academic Year của Publication | F13 |
| BR-R3-55 | Citizenship filter dùng giá trị của Student_Citizenships [TBC, Q22] | F13 |
| BR-R3-56 | Target membership đánh giá theo eligibility_date | F13 |
| BR-R3-57 | Cách kết hợp nhiều target cần xác nhận; đề xuất: union giữa các target, citizenship là điều kiện lọc (intersection) | F13 |
| BR-R3-58 | Recipient phải tham chiếu Publication và Student hợp lệ | F14 |
| BR-R3-59 | Recipient phải tham chiếu enrolment dùng để resolve; backend kiểm tra enrolment thuộc Student | F14 |
| BR-R3-60 | Mỗi Student chỉ xuất hiện một lần trong một Publication | F14 |
| BR-R3-61 | Student Charge tham chiếu hợp lệ Student, enrolment, School, Academic Year, Fee Component | F15 |
| BR-R3-62 | source_type chỉ là PUBLICATION hoặc MANUAL; charge từ Publication phải có fee_publication_id | F15 |
| BR-R3-63 | base_amount, tax_amount >= 0; total_amount = base_amount + tax_amount | F15 |
| BR-R3-64 | period_end_exclusive lớn hơn period_start | F15 |
| BR-R3-65 | UNIQUE(fee_publication_id, student_id) khi fee_publication_id không null | F15 |
| BR-R3-66 | Publication RATE_RULE thì fee_rate_rule_id phải có giá trị; FIXED_AMOUNT thì có thể null | F15 |
| BR-R3-67 | Backend kiểm tra student_id thuộc enrollment_id; rate rule khớp Fee Component, citizenship snapshot, Level và pricing_date | F15 |
| BR-R3-68 | Manual charge dùng idempotency_key để chống xử lý trùng | F15 |
| BR-R3-69 | Không ghi đè số tiền gốc để thể hiện adjustment | F15 |
| BR-R3-70 | Chỉ Student Charge POSTED hiển thị cho phụ huynh chọn thanh toán; DRAFT và VOID không hiển thị | F15 |
| BR-R3-71 | Adjustment phải tham chiếu Student Charge tồn tại | F16 |
| BR-R3-72 | Bắt buộc reason_code hợp lệ | F16 |
| BR-R3-73 | Giữ nguyên số tiền gốc; effective amount = total_amount + tổng adjustment đã áp dụng | F16 |
| BR-R3-74 | Ghi lại người tạo và thời điểm tạo | F16 |
| BR-R3-75 | Yêu cầu approval và thời điểm adjustment có hiệu lực cần xác nhận (Q08) | F16 |
| BR-R3-76 | Effective amount sau điều chỉnh không được âm [TBC] | F16 |


Quy tắc Education Account payment (tham chiếu R9)

Schema hiện tại chưa có payment transaction, nên đây là business rule; xử lý thanh toán thuộc R9.



| Mã | Quy tắc |
| --- | --- |
| BR-R3-77 | Student Singaporean có thể dùng số dư Education Account để thanh toán phí đủ điều kiện |
| BR-R3-78 | Không mặc định mọi Fee Component đều đủ điều kiện thanh toán bằng Education Account (Q12) |
| BR-R3-79 | Phụ huynh chọn từng Student Charge muốn thanh toán trong danh sách outstanding charges; không thanh toán hoặc thu toàn bộ tự động |
| BR-R3-80 | Nguồn citizenship và số dư; validate số dư, trừ tiền, thiếu số dư, thanh toán một phần, reconciliation thuộc R9 |



### 3.1.2 Process Flow Description and Screens


#### F01 – School Management

Actor: MOE HQ User. Trigger: HQ mở School Management. Điều kiện: đã đăng nhập và có quyền quản lý School.

1.     HQ User mở danh sách School.

2.     HQ User tạo mới hoặc chọn School hiện có.

3.     HQ User nhập name, school_type và moe_school_code (nếu có).

4.     System validate required fields và tính duy nhất của moe_school_code.

5.     System lưu School ở trạng thái active và hiển thị kết quả.


#### F02 – School User Account Assignment

Actor: MOE HQ User. Điều kiện: School đã tồn tại. Thông tin đăng nhập được bàn giao cho School qua giấy tờ, ngoài hệ thống (WA-R3-01).

1.     HQ User chọn School.

2.     HQ User tạo tài khoản School User (tên, email hoặc username và thông tin cần thiết).

3.     System tạo user với role School User và gắn với School.

4.     System hiển thị thông tin tài khoản để HQ User bàn giao cho School.


#### F03 – Academic Year, Academic Level và School Level Offering

Actor: HQ User (Academic Year, Academic Level); School User (offering, Q23).

Điều kiện: School, Academic Year, Academic Level đã tồn tại và còn hiệu lực.

Academic Year (khi nào) và Academic Level (cấp nào) là master data. Offering cho biết "School A dạy cấp P6 trong năm 2026"; không có offering thì không tạo được Class.

1.     HQ User mở Academic Year mới (year_number, start_date, end_date_exclusive, status).

2.     HQ User duy trì danh mục Academic Level (P1 đến P6, S1…, JC1…).

3.     School User chọn Academic Year và các Academic Level mà School dạy.

4.     System kiểm tra bộ ba (School, Academic Year, Academic Level) chưa tồn tại.

5.     System tạo School Level Offering ở trạng thái active.


#### F04 – Class Management

Actor: School User. Điều kiện: offering tương ứng đã tồn tại. School, Academic Year và Level của Class được suy ra từ offering.

1.     School User mở danh sách Class.

2.     School User chọn offering.

3.     School User nhập class_code và class_name.

4.     System validate (BR-R3-12, BR-R3-13).

5.     System lưu Class.


#### F05 – Student Management

Actor: School User (HQ User chỉ chỉnh enrolment và assignment, xem F07). Điều kiện: School User đã được assign School. Student là định danh lâu dài, độc lập với School và Class.

1.     School User mở Student Management và tạo Student.

2.     School User nhập display_name, date_of_birth, category.

3.     System validate required fields, category và chống trùng.

4.     System lưu và hiển thị kết quả.


#### F06 – Student Enrolment và Class Assignment

Actor: School User. Điều kiện: Student đã tồn tại; Class đã tồn tại và thuộc School của User. Enrolment cho biết Student học ở School nào, khi nào; assignment gắn enrolment vào Class cụ thể, giữ lịch sử đổi lớp.

1.     School User chọn Student và School, nhập enrolled_from.

2.     System tạo enrolment (enrolled_to_exclusive = null, status ENROLLED).

3.     School User chọn Class và assigned_from cho enrolment.

4.     System validate Class cùng School với enrolment và khoảng thời gian hợp lệ (BR-R3-21, BR-R3-22).

5.     System tạo class assignment (status ACTIVE).

6.     Với Student SC, System thực hiện F08.


#### F07 – Student Transfer và Class Change

Actor: MOE HQ User. Điều kiện: Student có enrolment đang hiệu lực; Class hoặc School đích tồn tại. Hệ thống đóng bản ghi cũ và mở bản ghi mới, không sửa đè (WA-R3-04).

Đổi lớp trong cùng School:

1.     HQ User mở hồ sơ Student, chọn Class đích và ngày hiệu lực.

2.     System đóng assignment cũ (assigned_to_exclusive = ngày hiệu lực, status ENDED).

3.     System mở assignment mới dưới cùng enrolment; enrolment giữ nguyên.

Chuyển trường (ví dụ ngày hiệu lực 01/07/2026):

1.     HQ User chọn School đích, Class đích và ngày hiệu lực.

2.     System đóng enrolment ở School A (enrolled_to_exclusive = 2026-07-01, status TRANSFERRED) và đóng assignment ở A cùng mốc.

3.     System mở enrolment ở School B (enrolled_from = 2026-07-01) và assignment mới.

4.     Bảng students không thay đổi; Student Charge đã phát hành giữ nguyên.


#### F08 – Education Account Linkage

Actor: System. Trigger: class assignment đầu tiên của Student được tạo (F06). Student SC được liên kết với Education Account để đủ điều kiện dùng số dư thanh toán phí.

1.     System kiểm tra students.category của Student.

2.     Nếu category = SC: System tìm Education Account của Student (do R1 tạo tự động) và tạo liên kết.

3.     Nếu category là PR hoặc IS: không liên kết.


#### F09 – Fee Type Management

Actor: HQ User, School User (theo phân quyền). Điều kiện: User có quyền.

1.     User mở Fee Type Management.

2.     User tạo mới hoặc chọn Fee Type.

3.     User nhập code.

4.     System validate required field và tính duy nhất.

5.     System lưu và hiển thị kết quả.


#### F10 – Fee Component Management

Actor: HQ User (chính); School User nếu được cho phép tạo component riêng [TBC]. Fee Component là danh mục phí, không phải khoản phải thu.

1.     User mở Fee Component Management.

2.     User tạo mới hoặc chọn Fee Component.

3.     User nhập component_code, name và chọn Fee Type.

4.     User chọn is_apply_tax.

5.     System validate (BR-R3-32, BR-R3-33) và lưu.

owner_school_id tham chiếu schools.id hay users.id cần Dev xác nhận (Q14).


#### F11 – Fee Rate Rule Management

Actor: HQ User, School User (theo phân quyền). Với cùng một Fee Component, các nhóm Student khác nhau có thể có mức phí khác nhau. Rate Rule xác định thu bao nhiêu, không xác định học sinh nào bị thu.

1.     User chọn Fee Component và xem các rule hiện có.

2.     User tạo hoặc sửa rule.

3.     User chọn Academic Level và student_category (nếu cần).

4.     User nhập price_amount, effective_from và trạng thái.

5.     System validate và lưu.


#### F12 – Fee Publication Management

Actor: HQ User, School User. Điều kiện: Fee Component, School, Academic Year tồn tại; user có quyền. Một Fee Publication là một lần phát hành một Fee Component cho một School, một Academic Year và một billing period, với đối tượng xác định, charge date và payment deadline.

1.     User tạo Publication, chọn Fee Component, School, Academic Year.

2.     User nhập billing period, eligibility_date, pricing_date.

3.     User chọn pricing mode: RATE_RULE hoặc FIXED_AMOUNT.

4.     User chọn target mode và cấu hình đối tượng (F13).

5.     User cấu hình charge date và due date.

6.     User lưu (Draft); System validate.

7.     Khi publish, System resolve recipient (F14) và generate Student Charge (F15), ghi published_by và published_at.


#### F13 – Publication Target Configuration

Actor: HQ User, School User. Xác định nhóm Student nhận phí: toàn trường, một hoặc nhiều Level, một hoặc nhiều Class, hoặc Student cụ thể; có thể lọc thêm theo citizenship.

1.     User chọn Publication và target mode.

2.     Với CUSTOM_TARGETS, User thêm các target (Level, Class, Student, citizenship).

3.     System validate tham chiếu và School scope.

4.     System lưu.

Diễn giải target_mode (giả định, Q02): COMPONENT_SCOPE lấy đối tượng theo phạm vi mặc định của Fee Component và School (toàn trường), không cần target chi tiết; CUSTOM_TARGETS lấy đối tượng từ các dòng trong fee_publication_targets.


#### F14 – Publication Recipient Resolution

Actor: System. Ghi lại danh sách Student được xác định là người nhận của Publication và enrolment dùng để xác định, bảo đảm truy vết.

1.     System đọc Publication và target.

2.     System lấy enrolment và class assignment có hiệu lực tại eligibility_date (Class qua offering ra School và Level).

3.     System xác định Student đủ điều kiện.

4.     System ghi recipient và resolved_at.

5.     System chuyển danh sách sang F15.


#### F15 – Student Charge Generation and Management

Actor: System (từ Publication); User có quyền (manual). Student Charge là khoản phải thu (outstanding charge); phụ huynh xem danh sách và chọn khoản muốn thanh toán (R9), hệ thống không tự thu toàn bộ.

1.     System nhận Student đủ điều kiện từ F14, hoặc nhận yêu cầu manual.

2.     System validate Student và enrolment.

3.     System xác định giá: Rate Rule (theo Fee Component, citizenship, Level, pricing_date) hoặc Fixed Amount.

4.     System tính tax nếu Fee Component áp dụng GST.

5.     System tạo Student Charge status DRAFT, gán charge_date và due_date.

6.     Khi ghi nhận chính thức, System set POSTED và posted_at.

7.     Charge POSTED xuất hiện trong outstanding charges của phụ huynh.


#### F16 – Student Charge Adjustment Management

Actor: User có quyền; Approver (nếu cần approval). Ghi nhận điều chỉnh tăng hoặc giảm cho Student Charge đã phát hành, không sửa trực tiếp số tiền gốc.

1.     User chọn Student Charge.

2.     User nhập adjustment_amount và chọn reason_code.

3.     System validate, ghi created_by và created_at.

4.     Nếu cần approval, Approver duyệt; System ghi approved_by và approved_at.

5.     System áp dụng theo rule đã xác nhận; số tiền gốc không đổi.


#### Màn hình

Tài liệu R3 chưa mô tả màn hình; bảng dưới là đề xuất của BA, cần chốt với team UI.



| Màn hình | Function | Actor | Nội dung |
| --- | --- | --- | --- |
| School | F01 | HQ | Danh sách, tạo, sửa, bật hoặc tắt hoạt động |
| School User | F02 | HQ | Tạo tài khoản và assign vào School |
| Academic Year và Academic Level | F03 | HQ | Quản lý master data |
| School Level Offering | F03 | School (Q23) | Chọn năm học và cấp học School dạy |
| Class | F04 | School | Danh sách và tạo Class theo offering |
| Student | F05 | School | Danh sách, tạo, sửa Student |
| Enrolment và Class Assignment | F06 | School | Tạo enrolment, gán Class, xem lịch sử |
| Student Transfer / Class Change | F07 | HQ | Đổi lớp, chuyển trường theo ngày hiệu lực |
| Fee Type, Fee Component | F09, F10 | HQ, School | CRUD và bật hoặc tắt hoạt động |
| Fee Rate Rule | F11 | HQ, School | Danh sách rule theo component, tạo, sửa |
| Fee Publication và Target | F12, F13 | HQ, School | Tạo Draft, cấu hình đối tượng, publish |
| Publication Recipient | F14 | HQ, School | Xem kết quả resolve (chỉ đọc) |
| Student Charge | F15 | HQ, School | Danh sách, chi tiết, tạo manual, void |
| Student Charge Adjustment | F16 | User có quyền, Approver | Tạo và duyệt điều chỉnh |


F08 do System thực hiện, không có màn hình riêng.


#### Trường hợp ngoại lệ



| F | Mã | Tình huống | Xử lý |
| --- | --- | --- | --- |
| F01 | AF01 | Trùng moe_school_code | Từ chối (E-03-09) |
| F01 | EF01 | Lưu thất bại | Báo lỗi, không xác nhận đã lưu |
| F03 | AF01 | Trùng offering | Từ chối (E-03-01) |
| F03 | AF02 | Khoảng năm học sai | Từ chối (E-03-04) |
| F05 | AF01 | Trùng Student | Cảnh báo hoặc từ chối (E-03-16) |
| F05 | AF02 | Thiếu dữ liệu bắt buộc | Từ chối |
| F06 | AF01 | Class khác School với enrolment | Từ chối (E-03-06) |
| F06 | AF02 | Assignment ngoài khoảng enrolment hoặc năm học | Từ chối (E-03-07) |
| F06 | AF03 | Enrolment chồng lấn | Từ chối (E-03-05) |
| F07 | AF01 | Đóng enrolment cũ thành công nhưng mở enrolment mới lỗi | Thực hiện trong một giao dịch, lỗi thì hoàn tác (đề xuất BA) |
| F08 | AF01 | Education Account chưa tồn tại (dưới 7 tuổi) hoặc đã đóng (từ 16 tuổi) | Xử lý theo quy tắc xác nhận ở Q16 |
| F09 | AF01 | Trùng code | Từ chối (E-03-09) |
| F09 | AF02 | Fee Type inactive bị chọn | Chặn (E-03-14) |
| F09 | EF01 | Lưu thất bại | Báo lỗi |
| F11 | AF01 | Không có rule khớp | Không chọn rate tùy ý; không tạo charge cho Student đó cho đến khi có pricing hợp lệ (E-03-29) |
| F11 | AF02 | Cấu hình sai | Từ chối |
| F12 | AF01 | Billing period sai | Từ chối (E-03-19) |
| F12 | AF02 | Cấu hình pricing sai | Từ chối (E-03-20) |
| F12 | AF03 | Không có Student đủ điều kiện | Không tạo charge |
| F12 | AF04 | Thiếu rate | Student đó không có charge (E-03-29) |
| F12 | EF01 | Cập nhật đồng thời | Yêu cầu refresh (E-03-22) |
| F12 | EF02 | Publish thất bại | Ghi nhận lỗi, không báo hoàn tất (E-03-23) |
| F14 | AF01 | Không có Student đủ điều kiện | Không tạo recipient |
| F14 | AF02 | Recipient trùng | Chặn |
| F14 | EF01 | Enrolment không thuộc Student | Từ chối (E-03-24) |
| F15 | AF01 | Thiếu rate rule | Không tạo charge (E-03-29) |
| F15 | AF02 | Enrolment không thuộc Student | Từ chối (E-03-24) |
| F15 | AF03 | Charge trùng | Chặn (E-03-25) |
| F15 | AF04 | Số tiền âm | Từ chối (E-03-10) |
| F15 | AF05 | Void | User có quyền void kèm lý do; ghi voided_at và void_reason (E-03-28) |
| F15 | EF01 | Generate thất bại | Ghi nhận lỗi; không xem charge chưa hoàn chỉnh là thành công (E-03-23) |


End of Document

