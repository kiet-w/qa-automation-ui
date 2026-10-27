# **R3 v3**

# **FUNCTIONAL SPECIFICATION – R3**

## **School, Student & Fee Management**

**Phiên bản:** Revised Draft – MVP  
**Trạng thái:** Chờ Dev/QA/PO rà soát  
**Dependencies:** R1 – Education Account; R4 – Financial Assistance; R8 – Parent Portal; R9 – Payment & Outstanding Fees.

---

# **1\. Giới thiệu**

## **1.1. Mục tiêu**

R3 cho phép MOE HQ Admin và School User quản lý thông tin School, Student, Enrolment, cấu hình các khoản phí và phát hành Student Charges.

Hệ thống cần đảm bảo:

* Student Profile, Enrolment Profile và Education Account (EA) là các đối tượng dữ liệu độc lập.  
* Student có thể được Enrol và phát hành Student Charges dù không có EA.  
* Mức phí được xác định dựa trên Student Category, Enrolment và Fee Configuration.  
* Student Charges được lưu riêng và không tự động trừ EA Balance khi phát hành.  
* R4 có thể áp dụng FAS Subsidy vào Student Charges.  
* Parent có EA liên kết hợp lệ có thể xem Outstanding Fees qua Parent Portal.

## **1.2. Actors & Permissions**

| Actor | Trách nhiệm |
| ----- | ----- |
| MOE HQ Admin | Quản lý Schools, cấp quyền School Users, cấu hình HQ Shared Fee Types/Components và Fee Rates |
| School User (SU) | Quản lý Academic Structure, Students, Enrolments, School-specific Fees và Fee Publications thuộc School |
| System | Xác thực và phân quyền, kiểm tra dữ liệu, liên kết EA, xác định đối tượng chịu phí, tính phí và tạo Charges |
| Parent | Xem Enrolment và Outstanding Fees của Children được phép truy cập qua Parent Portal |

### **Authentication & Authorization**

* MOE HQ Admin và School Users đăng nhập bằng Microsoft Account.  
* **Working Assumption:** HQ Admin đã có Microsoft Account do Chính phủ cấp và được cấu hình sẵn quyền Admin.  
* HQ Admin đăng ký School Users bằng cách import CSV chứa Email, Full Name và School ID.  
* Microsoft thực hiện Authentication; hệ thống kiểm tra User có được đăng ký và phân quyền truy cập hay không.  
* Microsoft Login thành công không đồng nghĩa với việc User được phép truy cập hệ thống.  
* MVP không phát triển chức năng đăng ký tài khoản hoặc quản lý mật khẩu riêng.

## **1.3. Các đối tượng dữ liệu chính**

| Entity | Mô tả |
| ----- | ----- |
| School | Thông tin trường học |
| School User & Assignment | Thông tin User và School được phân quyền |
| Academic Structure | Academic Year, Education Stage, Academic Level, School Offering, Class |
| Student Profile | Thông tin định danh Student |
| Enrolment Profile | Thông tin School, Academic Year, Stage, Level, Class và trạng thái theo học |
| Education Account | Tài khoản EA do R1 quản lý; không bắt buộc đối với mọi Student |
| Fee Type | Nhóm khoản phí |
| Fee Component | Khoản phí cụ thể |
| Fee Eligibility | Nhóm Student có thể phải đóng Fee Component |
| Fee Rate | Mức phí áp dụng theo đối tượng và thời gian hiệu lực |
| Fee Publication | Đợt phát hành phí |
| Student Charge | Khoản phải thu cụ thể của Student |

---

# **2\. Chi tiết các chức năng**

## **A. School & Student Management**

### **F01 – School Management**

**Actor:** MOE HQ Admin

**Function:** Quản lý danh sách School, phục vụ School User Assignment, Academic Configuration và Fee Management.

**System Capabilities:**

1. Hệ thống cho phép HQ Admin tạo mới, xem, chỉnh sửa và Deactivate School.  
2. Thông tin School bao gồm:  
   * School ID (School Code).  
   * School Name.  
   * School Type.  
   * Status.  
3. Hệ thống kiểm tra các trường bắt buộc và School ID không trùng.  
4. Hệ thống lưu School để sử dụng trong School User CSV Import, Academic Configuration và Fee Publication.  
5. Hệ thống cho phép HQ Admin xem danh sách Schools và trạng thái tương ứng.

**Business Rules:**

* School ID phải duy nhất trong hệ thống.  
* School phải tồn tại và đang Active trước khi được sử dụng để assign School User.  
* School ID trong CSV phải khớp với School hợp lệ đã được cấu hình.  
* School đã có School User Assignment, Enrolment hoặc Student Charges không được xóa vĩnh viễn.  
* Inactive School không được dùng để tạo School User Assignment, Academic Configuration hoặc Fee Publication mới.  
* MVP sử dụng 10 Schools mẫu theo Feature List.

### **F02 – School User Provisioning & Microsoft Login**

**Actors:** MOE HQ Admin, School User, System

**Function:** Đăng ký School Users qua CSV, xác thực bằng Microsoft Account và phân quyền truy cập theo School Assignment.

**System Capabilities:**

1. Hệ thống cho phép HQ Admin upload CSV chứa:  
   * School User Email.  
   * Full Name.  
   * School ID.  
2. Hệ thống kiểm tra định dạng CSV, các trường bắt buộc, Email và School ID.  
3. Hệ thống kiểm tra School ID tồn tại và School đang Active.  
4. Với dữ liệu hợp lệ, hệ thống tạo School User Record và liên kết với School tương ứng.  
5. Hệ thống hiển thị kết quả Import gồm các Records thành công, thất bại và lý do lỗi.  
6. Hệ thống hỗ trợ MOE HQ Admin và School User đăng nhập bằng Microsoft Account.  
7. Sau khi Microsoft xác thực thành công, hệ thống đối chiếu thông tin định danh với User Records đã đăng ký.  
8. Với HQ Admin, hệ thống kiểm tra tài khoản có quyền Admin đã được cấu hình trước.  
9. Với School User, hệ thống kiểm tra User đã có trong danh sách import và có School Assignment hợp lệ.  
10. Hệ thống cho phép truy cập theo Role/School Assignment hoặc từ chối nếu không đủ điều kiện.

**Business Rules:**

* Chỉ HQ Admin được import School User CSV.  
* School User phải có School Assignment hợp lệ với một School đang Active.  
* Microsoft Account chưa được đăng ký trong hệ thống không được phép truy cập.  
* School User không được tự đăng ký để nhận quyền truy cập.  
* School User chỉ được truy cập dữ liệu thuộc School được phân quyền.  
* Hệ thống không lưu mật khẩu Microsoft Account.  
* Sau khi import, thông tin School User phải được lưu trong database để kiểm tra khi đăng nhập; không đọc lại CSV mỗi lần Login.

### **F03 – School Academic Configuration**

**Actor:** School User

**Function:** Cấu hình Education Stages mà School giảng dạy theo từng Academic Year và tự động tạo các Academic Levels tương ứng.

**System Capabilities:**

1. Hệ thống cho phép School User truy cập chức năng School Academic Configuration.  
2. School User chọn Academic Year cần cấu hình.  
3. School User chọn các Education Stages mà School giảng dạy trong năm học đó:  
   * Primary.  
   * Secondary.  
   * Pre-University.  
4. Sau khi School User lưu cấu hình, hệ thống tự động tạo các Academic Levels tương ứng:  
   * **Primary:** P1–P6 (6 khối).  
   * **Secondary:** S1–S4 (4 khối).  
   * **Pre-University:** PU1–PU3 (3 khối).  
5. Hệ thống hiển thị danh sách Academic Levels đã được tạo để School User tiếp tục cấu hình Classes tại F04.  
6. Khi School User cấu hình Education Stage cho Academic Year mới, hệ thống tự động tạo các Academic Levels tương ứng và sử dụng những Levels đó để thực hiện Annual Class Progression. 

**Business Rules:**

* School User chỉ được cấu hình Academic Structure thuộc School mình.  
* Mỗi Education Stage chỉ được cấu hình một lần trong cùng School và Academic Year.  
* Academic Levels được tự động tạo theo Education Stage, không yêu cầu School User thêm từng Level thủ công.  
* Không tạo trùng Academic Levels khi School User lưu hoặc cập nhật cấu hình.  
* Academic Structure được quản lý riêng theo từng Academic Year.

### **F04 – Class Management**

**Actor:** School User

**Function:** Tạo và quản lý Classes trong từng Academic Level.

**System Capabilities:**

1. Hệ thống hiển thị các Academic Levels đã được cấu hình tại F03.  
2. School User có thể chọn một Academic Level và tạo Class mới bằng cách nhập Class Code và Class Name.  
3. Đối với Academic Year đầu tiên được cấu hình, School User tạo các Classes ban đầu.  
4. Khi chuyển sang Academic Year mới, hệ thống tự động tạo Classes cho Academic Level tiếp theo dựa trên Classes của năm học trước.  
5. Hệ thống tự động cập nhật Academic Level trong Class mới, ví dụ P1A (2026) → P2A (2027).  
6. Hệ thống giữ lại Classes của Academic Year trước để phục vụ tra cứu lịch sử.  
7. Đối với Academic Level đầu vào của School, School User tạo danh sách Classes mới mỗi Academic Year để tiếp nhận Students mới.

**Business Rules:**

* Classes được quản lý theo School, Academic Year và Academic Level.  
* Khi chuyển Academic Year, Classes được tự động chuyển lên Academic Level tiếp theo trong cùng School.  
* Chỉ Academic Level đầu vào của School yêu cầu School User tạo Classes mới hằng năm.  
* Không tự động tạo Class cho Academic Level vượt quá Level cuối cùng của Education Stage mà School giảng dạy.  
* Class Code phải duy nhất trong cùng School, Academic Year và Academic Level.  
* Classes của các Academic Years trước không được xóa hoặc ghi đè.  
* Hệ thống không tự động chuyển Class sang School khác.

### **F05 – Student Profile Management**

**Actor:** School User

**Function:** Quản lý thông tin định danh và hồ sơ Student.

**System Capabilities:**

1. Hệ thống cho phép School User tạo mới, xem, tìm kiếm và chỉnh sửa Student Record.  
2. Thông tin Student bao gồm:  
   * Student ID – do School cấp.  
   * Full Name.  
   * NRIC.  
   * Date of Birth.  
   * Citizenship:  
     * Singapore Citizen (SC).  
     * Singapore Permanent Resident (PR).  
     * International Student – ASEAN (IS\_ASEAN).  
     * International Student – Non-ASEAN (IS\_NON\_ASEAN).  
3. Hệ thống kiểm tra các trường bắt buộc và dữ liệu Student trùng lặp.  
4. Hệ thống sử dụng NRIC để tìm kiếm và đối chiếu Student đã tồn tại.  
5. Hệ thống kiểm tra EA Linkage theo F08.  
6. Hệ thống vẫn cho phép tạo và lưu Student Record khi Student không có EA.

**Business Rules:**

* Student ID do School cấp, phải duy nhất trong phạm vi School và có thể thay đổi khi Student chuyển School.  
* NRIC được sử dụng để nhận diện cùng một Student khi Student chuyển School.  
* Khi Student chuyển School, School mới có thể cấp Student ID mới mà không tạo Student Identity trùng lặp.  
* Student Profile độc lập với Enrolment Profile và EA.  
* Student không cần có EA để được Enrol, nhận Student Charges hoặc xét FAS.  
* Không được xóa Student Record đã có Enrolment hoặc Student Charges liên quan làm mất dữ liệu lịch sử.

### **F06 – Student Enrolment & Class Assignment**

**Actor:** School User, System

**Function:** Quản lý Student Enrolment, Class Assignment và tự động chuyển Student lên Academic Level tiếp theo khi sang Academic Year mới.

**System Capabilities:**

1. Hệ thống cho phép School User chọn Student Record đã tồn tại và assign vào Class thuộc School được phân quyền.  
2. Khi Student được assign vào Class lần đầu, hệ thống tạo Enrolment Profile, bao gồm:  
   * Student Reference.  
   * School.  
   * Academic Year.  
   * Education Stage.  
   * Academic Level.  
   * Class.  
   * Enrolment Status.  
   * Effective Date.  
3. Hệ thống xác định School, Academic Year, Education Stage và Academic Level dựa trên Class được chọn.  
4. Khi chuyển sang Academic Year mới, hệ thống tự động chuyển những Student đang có Enrolment Active sang Academic Level và Class tiếp theo đã được tạo theo F04.  
5. Hệ thống tự động ghi nhận Enrolment và Class Assignment của Academic Year mới mà không yêu cầu School User thao tác lại.  
6. School User có thể xem Enrolment hiện tại và Enrolment History của Student.

**Business Rules:**

* Student Record phải tồn tại trước khi tạo Enrolment ban đầu.  
* Class phải thuộc School mà School User được phân quyền.  
* Student tiếp tục theo học tại cùng School được tự động chuyển Academic Year, Academic Level và Class theo Annual Progression.  
* School User không cần tạo lại Enrolment hoặc Class Assignment cho Student khi lên khối hằng năm.  
* Chỉ Student có Enrolment Active mới được xử lý Annual Progression.  
* Không được tạo Enrolment trùng hoặc xung đột cho cùng Student trong Academic Year.  
* Hệ thống phải giữ Enrolment History và Class Assignment History của các năm học trước.  
* Enrolment là nguồn dữ liệu để xác định School, Education Stage và Academic Level khi phát hành Fee hoặc đánh giá FAS.  
* Annual Progression không tự động tạo Student Charges.  
* Student chuyển School được xử lý riêng tại F07, không thuộc Automatic Annual Progression.

### **F07 – Student Transfer & Class Change**

**Actor:** School User

**Function:** Quản lý việc Student chuyển Class trong cùng School hoặc chuyển sang School khác, ngoài quy trình Annual Progression tự động tại F06.

**System Capabilities:**

1. Hệ thống cho phép School User thay đổi Class Assignment của Student trong phạm vi School được phân quyền.  
2. Khi Student chuyển Class trong cùng School, hệ thống cập nhật Class Assignment theo Effective Date và lưu lịch sử Class cũ.  
3. Khi Student chuyển School:  
   * School User của School cũ Deactivate Enrolment hiện tại.  
   * School User của School mới tìm kiếm Student bằng NRIC để đối chiếu hồ sơ đã tồn tại.  
   * School User của School mới tạo Enrolment và Class Assignment tại School mới.  
   * School mới có thể cấp Student ID mới cho Student.  
4. Hệ thống ghi nhận Effective Date của việc chuyển Class hoặc chuyển School.  
5. Hệ thống cho phép School User xem Enrolment History và Class Assignment History theo quyền.

**Business Rules:**

* Việc chuyển Academic Year và Academic Level hằng năm trong cùng School được xử lý tự động tại F06, không yêu cầu School User thao tác tại F07.  
* Khi chuyển Class trong cùng School, hệ thống giữ nguyên Enrolment tại School và chỉ cập nhật Class Assignment.  
* Khi chuyển School, Enrolment tại School cũ được kết thúc và Enrolment mới được tạo tại School mới.  
* Student ID do School cấp có thể thay đổi khi Student chuyển School.  
* NRIC được sử dụng để đối chiếu Student Identity giữa các Schools.  
* Không được tạo Enrolment Active bị chồng lấn cho cùng Student.  
* Hệ thống phải giữ Enrolment History và Class Assignment History.  
* Student Charges đã POSTED phải giữ nguyên Original Amount và thông tin School/Enrolment tại thời điểm phát hành.  
* Student chuyển School không tự động tạo EA mới.  
* School User chỉ được thao tác với Enrolment và Class Assignment thuộc School được phân quyền.

### 

### **F08 – Student–Education Account Linkage**

**Actor:** System

**Function:** Liên kết Student Profile với EA hợp lệ đã tồn tại trong R1.

**System Capabilities:**

1. Khi Student Record được tạo hoặc liên kết, hệ thống kiểm tra EA tương ứng bằng NRIC.  
2. Hệ thống đối chiếu thông tin Student Identity với EA tìm được.  
3. Nếu thông tin hợp lệ, hệ thống tạo Student–EA Linkage.  
4. Hệ thống ghi nhận EA Linkage Status.  
5. Nếu không có EA phù hợp, hệ thống vẫn giữ Student Record.

**Business Rules:**

* EA được quản lý bởi R1, R3 không tự tạo EA.  
* Student–EA Linkage không làm thay đổi EA Balance.  
* EA liên kết với Student Identity, không trực tiếp thuộc Enrolment.  
* PR/IS Students không được tự động liên kết với EA dành cho Singapore Citizens.  
* Không tạo Duplicate EA Linkage khi Student chuyển School.  
* EA Closed và Identity Mismatch phải được xử lý mà không tạo liên kết sai.

---

## **B. Fee Management**

### **F09 – Fee Type Management**

**Actors:** MOE HQ Admin, School User

**Function:** Quản lý các nhóm khoản phí.

**System Capabilities:**

1. Hệ thống cho phép User được phân quyền tạo mới, xem, chỉnh sửa và Deactivate Fee Type.  
2. Hệ thống hỗ trợ HQ Shared Fee Types và School-specific Fee Types.  
3. Hệ thống lưu Fee Type Name, Description, Ownership Scope và Status.  
4. Hệ thống cho phép liên kết nhiều Fee Components với cùng một Fee Type.

**Business Rules:**

* Một Fee Type có thể chứa nhiều Fee Components.  
* HQ Admin quản lý HQ Shared Fee Types.  
* School User chỉ được quản lý School-specific Fee Types thuộc School mình.  
* School User không được sửa HQ Shared Fee Types.  
* Fee Type đã được sử dụng không được xóa làm mất dữ liệu lịch sử.  
* Inactive Fee Type không được sử dụng để cấu hình mới.

### 

### **F10 – Fee Component & Eligibility Configuration**

**Actors:** MOE HQ Admin, School User

**Function:** Định nghĩa Fee Components và nhóm Students có thể phải đóng từng khoản phí.

**System Capabilities:**

1. Hệ thống cho phép User được phân quyền tạo mới, xem, chỉnh sửa và Deactivate Fee Components.  
2. Mỗi Fee Component được liên kết với một Fee Type.  
3. Hệ thống hỗ trợ HQ Shared Components và School-specific Components.  
4. Khi cấu hình HQ Shared Fee Component, hệ thống cung cấp tab **Fee Eligibility**.  
5. HQ Admin có thể chọn đối tượng áp dụng theo:  
   * Education Stage.  
   * Student Category.  
6. Theo UI Dev hiện tại, Student Categories bao gồm:  
   * Singapore Citizen.  
   * Permanent Resident.  
   * International ASEAN.  
   * International non-ASEAN.  
7. Hệ thống lưu Fee Eligibility và cho phép tiếp tục cấu hình Fee Rates tại F11.  
8. School User có thể cấu hình School-specific Fee Components thuộc School mình.

**Business Rules:**

* Fee Component là định nghĩa khoản phí, không phải Student Charge.  
* Mỗi Fee Component thuộc một Fee Type.  
* HQ Shared Components có thể được sử dụng bởi Schools theo quyền.  
* School User không được sửa HQ Shared Components.  
* Fee Eligibility xác định nhóm Students *có thể* chịu khoản phí, không trực tiếp phát hành Student Charges.  
* Fee Eligibility không thay thế Publication Target.  
* Inactive Component không được sử dụng trong Fee Publication mới.

**Implementation Alignment:** Fee Component, Fee Eligibility và Fee Rates được cấu hình trong cùng Create/Edit workflow

### **F11 – Fee Rate Configuration**

**Actors:** MOE HQ Admin, School User

**Function:** Cấu hình Amount áp dụng cho từng nhóm Student thuộc Fee Eligibility.

**System Capabilities:**

1. Sau khi cấu hình Fee Eligibility, hệ thống hiển thị các nhóm Student cần cấu hình Rate.  
2. Hệ thống cho phép User nhập Fee Rates với các thông tin:  
   * Education Stage.  
   * Student Category.  
   * Amount.  
   * Currency (SGD).  
   * Effective From.  
   * Effective To.  
3. Một Fee Component có thể có nhiều Fee Rates.  
4. Hệ thống kiểm tra Rate Configuration và Effective Period.  
5. User được phân quyền có thể xem và cập nhật Fee Rates.  
6. Với School-specific Components, School User có thể cấu hình Amount và Effective Period theo chính sách School.

**Business Rules:**

* HQ Fee Rate được xác định theo Fee Component \+ Education Stage \+ Student Category \+ Effective Period.  
* Không cho phép các Fee Rates có cùng điều kiện bị chồng lấn Effective Period.  
* `Effective To` được hiểu là exclusive end date theo FS hiện tại.  
* Khi Publish Fee, hệ thống chọn Rate hợp lệ tại Pricing Date.  
* Nếu không tìm thấy Fee Rate phù hợp, hệ thống không tự suy ra Amount.  
* Việc cập nhật Fee Rate không làm thay đổi Original Amount của Student Charges đã POSTED.  
* School User không được chỉnh sửa HQ Shared Fee Rates.

**Lưu ý:** Fee Rate Effective Period và Fee Publication Billing Period là hai khái niệm khác nhau.

### **F12 – Fee Publication Management**

**Actor:** School User

**Function:** Phát hành các khoản phí cho Students thuộc School theo Academic Year và Billing Period.

**System Capabilities:**

1. Hệ thống cho phép School User tạo mới và xem Fee Publications.  
2. School User có thể lựa chọn một hoặc nhiều Fee Components đang Active.  
3. Fee Publication bao gồm:  
   * Publication Name.  
   * School.  
   * Academic Year.  
   * Billing Period.  
   * Selected Fee Components.  
   * Target Academic Levels.  
   * Due Date.  
4. Hệ thống xác định Students và Fee Rates dự kiến được áp dụng.  
5. Hệ thống cung cấp Preview danh sách Students và Amount trước khi Publish.  
6. School User có thể xác nhận Publish.  
7. Sau khi Publish thành công, hệ thống tạo Student Charges tương ứng.

**Business Rules:**

* Fee Publication là một nghiệp vụ riêng với Fee Component Configuration.  
* Fee Component Eligibility không tự động tạo Student Charges.  
* Một Fee Component có thể được sử dụng trong nhiều Fee Publications thuộc các Billing Period khác nhau.  
* Hệ thống phải ngăn tạo Duplicate Charges khi cùng một Publication được xử lý lại.  
* School User không được chỉnh sửa HQ Fee Rates trong quá trình Publish.  
* Fee Publication không phụ thuộc Student có EA hoặc FAS Grant hay chưa.  
* Fee Rate Effective Period không tự động quyết định Billing Period.

### **F13 – Publication Target Configuration**

**Actor:** School User

**Function:** Xác định nhóm Students thực tế sẽ nhận phí trong một Fee Publication.

**System Capabilities:**

1. Hệ thống cho phép School User cấu hình Publication Target trong phạm vi School được phân quyền.  
2. Hệ thống hỗ trợ lựa chọn Target Academic Levels theo flow MVP hiện tại.  
3. Hệ thống tìm các Student Enrolments phù hợp với School, Academic Year và Eligibility Date.  
4. Hệ thống lọc Students dựa trên Fee Eligibility của từng Fee Component.  
5. Hệ thống tạo danh sách Target Students phục vụ Preview và Publish.

**Business Rules:**

* Target Students phải thuộc School và Academic Year của Fee Publication.  
* Student phải đáp ứng đồng thời Publication Target và Fee Component Eligibility.  
* Không tạo Student Charges cho Student không có Enrolment phù hợp.  
* Student không có EA vẫn có thể nằm trong Publication Target.

### **F14 – Publication Recipient Resolution**

**Actor:** System

**Function:** Xác định danh sách Students nhận Charges từ Fee Publication.

**System Capabilities:**

1. Hệ thống lấy thông tin Fee Publication, Selected Fee Components và Publication Targets.  
2. Hệ thống tìm các Enrolment Profiles hợp lệ tại Eligibility Date.  
3. Hệ thống kiểm tra Fee Eligibility của từng Student đối với từng Fee Component.  
4. Hệ thống xác định Fee Rate phù hợp theo Student Category, Education Stage và Pricing Date.  
5. Hệ thống tính Amount dự kiến cho từng Student và Fee Component.  
6. Hệ thống lưu hoặc chuẩn bị danh sách Recipients để tạo Student Charges.

**Business Rules:**

* Không tạo Duplicate Recipient cho cùng Student \+ Fee Component \+ Publication.  
* Mỗi Recipient phải tham chiếu Student và Enrolment hợp lệ.  
* Không tạo Student Charges cho Student nằm ngoài Publication Target.  
* Nếu không có Student phù hợp, hệ thống thông báo và không tạo Charges.  
* Nếu thiếu Fee Rate hợp lệ, hệ thống thông báo lỗi và không tự chọn Rate khác.

### **F15 – Student Charge Generation & Management**

**Actors:** System, MOE HQ Admin, School User (xem theo quyền)

**Function:** Tạo và quản lý Student Charges được phát hành từ Fee Publication.

**System Capabilities:**

1. Sau khi Fee Publication thành công, hệ thống tạo Student Charges cho các Recipients phù hợp.  
2. Hệ thống xác định Fee Rate hoặc School-specific Amount tương ứng.  
3. Hệ thống tạo một Student Charge cho mỗi Student và Fee Component được phát hành.  
4. Student Charge lưu tối thiểu:  
   * Charge ID.  
   * Student Reference.  
   * Enrolment Reference.  
   * School.  
   * Academic Year.  
   * Fee Component.  
   * Fee Publication Reference.  
   * Original Amount.  
   * Due Date.  
   * Status.  
5. Student Charges phát hành thành công được ghi nhận với Status \= POSTED.  
6. Hệ thống cho phép HQ Admin và School User xem danh sách, chi tiết Charges theo quyền.  
7. Hệ thống cung cấp thông tin Charges cho R4 Subsidy Application và R9 Outstanding Fees.

**Business Rules:**

* Student Charges thuộc Student và tham chiếu Enrolment tại thời điểm phát hành.  
* Student không có EA vẫn được tạo Charges.  
* Không tạo Duplicate Charges cho cùng Student \+ Fee Component \+ Publication.  
* Original Amount của Charges đã POSTED không thay đổi khi Fee Rate hoặc Enrolment thay đổi.  
* Chỉ Charges đã POSTED mới được đưa vào Outstanding Fee Processing.  
* Original Amount, Subsidy Amount và Net Payable được quản lý riêng.  
* Publish Fee không tự động trừ EA Balance.

**R4 – FAS Integration:**

* Student Charges được tạo độc lập với FAS Grant.  
* Nếu Student đã có Grant hợp lệ, R4 áp dụng Subsidy khi Charges tương ứng được POSTED.  
* Nếu Grant được duyệt sau khi Charges đã tồn tại, R4 áp dụng Subsidy cho các Charges chưa thanh toán và còn đáp ứng điều kiện.  
* Subsidy Amount không được vượt Original Amount.  
* Net Payable \= Original Amount − Subsidy Amount.  
* FAS Subsidy không phải Charge Adjustment.

**R9 – Outstanding Fees & Payment Integration:**

* R9 nhận thông tin POSTED Charges, Subsidy Amount, Net Payable, Due Date và Payment Status.  
* Parent có EA liên kết hợp lệ và được xác minh quyền truy cập có thể xem Outstanding Fees qua Parent Portal.  
* Student không có EA vẫn có Charges trong R3 nhưng không sử dụng Parent EA Payment Flow.  
* Payment Processing, EA Balance Deduction và Reconciliation thuộc R9, không thuộc R3.

---

# **3\. Cross-Requirement Integration**

| Nguồn | Đích | Nội dung |
| ----- | ----- | ----- |
| Microsoft Account | R3 User Access | Authentication và Authorization |
| R3 School Records | R3 School User Assignment | Kiểm tra School ID từ CSV |
| R1 EA | R3 Student Profile | Student–EA Linkage |
| R3 Student/Enrolment | R3 Fee Publication | Xác định Students nhận phí |
| R3 Fee Components | R4 FAS | Cấu hình Subsidy Matrix |
| R3 Enrolment | R4 FAS | Xác minh School và xác định Education Stage |
| R4 FAS Grant | R3 Student Charges | Áp dụng Subsidy |
| R3 Student Charges | R8/R9 Parent Portal | Hiển thị Outstanding Fees |
| R9 Payment | R3 Student Charges | Cập nhật Payment Status và Remaining Outstanding |

---

# **4\. Main Exception Handling**

| Tình huống | Xử lý |
| ----- | ----- |
| School ID bị trùng | Không cho tạo School trùng |
| CSV chứa School ID không hợp lệ | Từ chối Record lỗi và hiển thị lý do |
| CSV thiếu Email, Name hoặc School ID | Từ chối Record lỗi và hiển thị lý do |
| Microsoft Login thành công nhưng User chưa được đăng ký | Từ chối truy cập |
| School User không có School Assignment hợp lệ | Từ chối truy cập |
| Student Identity bị trùng | Cảnh báo hoặc chặn tạo trùng theo Validation Rules |
| Không tìm thấy EA | Vẫn giữ Student Record |
| EA Identity không khớp | Không tạo Linkage sai; yêu cầu kiểm tra |
| Enrolment trùng hoặc xung đột | Không cho lưu Enrolment xung đột |
| Student chuyển School | Giữ Enrolment và Charges lịch sử |
| Không tìm thấy Fee Rate hợp lệ | Thông báo lỗi; không tạo Charge với Amount sai |
| Publication Target không hợp lệ | Không tạo Charges cho Students ngoài Target |
| Publish bị thực hiện lại | Không tạo Duplicate Charges |
| Student chưa có FAS Grant | Subsidy Amount \= 0 |
| Fee Component không nằm trong Subsidy Matrix | Subsidy Amount \= 0 |
| Student không có EA | Charges vẫn tồn tại nhưng không hiển thị qua EA Detail |
| Payment thất bại | R9 không đánh dấu Charge/Invoice là Paid |

---

# **5\. Các chức năng bổ sung theo Feature List**

### **FL-R3-F09 – Bulk CSV Import for Academic Setup & Student Management**

**Actor:** School User  
**Trạng thái:** Deferred / Later Sprint

**System Capabilities:**

1. Hệ thống cho phép School User upload CSV để tạo Academic Structure, Student Records và Class Assignments.  
2. Hệ thống kiểm tra định dạng CSV, các trường bắt buộc, dữ liệu trùng và School/Class References.  
3. Hệ thống hiển thị Import Preview, Import Results và lý do lỗi.

**Business Rules:**

* School User chỉ được import dữ liệu thuộc School được phân quyền.  
* Import không được tạo Duplicate Students hoặc Enrolments xung đột.

**Lưu ý:** Chức năng này khác với F02, nơi HQ Admin import CSV để đăng ký School Users.

### **FL-R3-F10 – Student Enrolment Overview**

**Actors:** MOE HQ Admin, School User, Parent (Read-only theo quyền)

**System Capabilities:**

1. Hệ thống cho phép School User xem Students và Enrolments thuộc School mình.  
2. Hệ thống cho phép HQ Admin xem Enrolments theo School, Academic Year, Academic Level và Class.  
3. Hệ thống hỗ trợ xem Enrolment hiện tại và Enrolment History.  
4. Parent có thể xem Enrolment Information của Children được liên kết hợp lệ qua Parent Portal.

**Business Rules:**

* School User không được xem dữ liệu của School khác nếu không có quyền.  
* Parent chỉ được xem thông tin Children mà mình có quyền truy cập.

---

# **6\. Open Questions & Implementation Decisions**

| Priority | Nội dung cần làm rõ |
| ----- | ----- |
| P1 | Fee Publication UI có hỗ trợ Academic Year, Billing Period, Target Levels, Due Date và Preview trước khi Publish không? |
| P1 | Fee Rate phân biệt International ASEAN và non-ASEAN dựa trên Student Data nào? |
| P1 | Fee Publication hỗ trợ nhiều Fee Components hay chỉ một Component mỗi lần Publish? |
| P1 | Microsoft Identity được đối chiếu với Email trong CSV bằng trường thông tin nào? |
| P1 | Hệ thống duy trì cùng một Student Identity khi Student chuyển giữa hai Schools như thế nào? |
| P2 | Khi Admin import lại CSV, hệ thống Add, Update hay Replace School User Records? |
| P2 | Nếu School cũ chưa Deactivate Enrolment, School mới tiếp nhận Student như thế nào? |
| P2 | R9 sử dụng Student Charge trực tiếp hay có Invoice Entity riêng? |
| P3 | Admin Export Charges/Manual Invoice cho Student không có EA có thuộc scope MVP không? |

---

# **7\. MVP Delivery Notes**

**Các chức năng chính:**

* **F01–F02:** School Management, Microsoft Login, CSV Import để đăng ký School Users.  
* **F03–F08:** Academic Structure, Student Management, Enrolment, Transfer và EA Linkage.  
* **F09–F11:** Fee Type, Fee Component, Fee Eligibility và Fee Rate Configuration.  
* **F12–F15:** Fee Publication, Targeting, Recipient Resolution và Student Charge Generation.  
* **FL-R3-F10:** Student Enrolment Overview theo quyền.

**Chức năng Deferred hoặc thuộc Requirement khác:**

* FL-R3-F09: Bulk CSV Import cho Academic/Student Data.  
* R1: EA Creation/Closure và Wallet Ledger.  
* R4: FAS Eligibility Assessment, Grant và Subsidy Rules.  
* R9: Payment Gateway, Wallet Debit và Reconciliation.

# **R3 v2**

# **FUNCTIONAL SPECIFICATION – R3: School, Student và Fee Management**

## **1\. Introduction**

### **1.1. Overview**

Requirement 3 yêu cầu MOE HQ User và School User quản lý danh sách **School, Academic Level (level/cohort), Class, Student trong từng Class**, cùng **Fee Type và Fee Component** mà học sinh phải đóng. Học sinh Singaporean có thể dùng số dư Education Account để thanh toán các khoản phí đủ điều kiện.  
Tài liệu này gồm hai nhóm chức năng:

* **School Management (F01–F08):** tạo School, cấp tài khoản School User, cấu hình Academic Year/Level/Offering và Class, quản lý Student, enrolment và class assignment, xử lý chuyển lớp/chuyển trường và liên kết Student với Education Account.  
* **Fee Management (F09–F16):** Fee Type, Fee Component, Fee Rate Rule, Fee Publication, Publication Target, Publication Recipient, Student Charge, Student Charge Adjustment.

Quy tắc nghiệp vụ liên quan đến thanh toán bằng Education Account được ghi nhận ở mục 4; chi tiết payment thuộc requirement khác (R9, e-Service Portal).

### **1.2. Actors**

| Actor | Mô tả |
| :---- | :---- |
| MOE HQ User | Tạo School, tạo tài khoản và assign School User; quản lý Fee Component/cấu hình phí tập trung; chỉnh sửa Student khi chuyển lớp/chuyển trường; publish fee. |
| School User | Quản lý Level, Class, Student của trường mình; thực hiện các thao tác fee trong phạm vi được phân quyền. |
| System | Validate dữ liệu, xác định rate, resolve target, generate Student Charge, liên kết Student với Education Account. |

### **1.3. Scope**

**In Scope:** School Management, School User assignment, Academic Level, Class, Student, Student Enrolment và Class assignment, Student transfer, Education Account linkage, Fee Type, Fee Component, Fee Rate Rule, Fee Publication, Publication Target, Publication Recipient, Student Charge, Student Charge Adjustment, quy tắc Education Account payment eligibility.  
**Out of Scope (tài liệu này):** Payment transaction, trừ số dư Education Account, reconciliation, màn hình chọn thanh toán của phụ huynh (e-Service Portal), tạo/đóng Education Account tự động theo tuổi (R1), FAS subsidy (R4).  
**Dependencies:** academic\_years, users, education\_accounts (R1) được xem là entity có sẵn.

### **1.4. Assumptions và Limitations**

| ID | Working Assumption |
| :---- | :---- |
| WA-R3-01 | HQ tạo School và School User; việc bàn giao thông tin tài khoản cho School thực hiện ngoài hệ thống (giấy tờ). |
| WA-R3-02 | Hiện tại Student được School User nhập **manual**; chưa có import/đồng bộ từ hệ thống ngoài. |
| WA-R3-03 | School User tự khai báo School Level Offering (cấp học trường dạy trong năm học) và Class của trường mình; Academic Year và Academic Level là master data. |
| WA-R3-04 | Khi Student chuyển lớp hoặc chuyển trường, HQ User cập nhật lại enrolment và class assignment cho khớp với lớp hiện tại (đóng bản ghi cũ, mở bản ghi mới). |
| WA-R3-05 | Student Singaporean (students.category \= SC) khi được thêm vào Class sẽ được liên kết với Education Account. |
| WA-R3-06 | Fee Type là phân loại cấp cao; Fee Component là khoản phí cụ thể và là danh mục phí, không phải khoản phải thu. |
| WA-R3-07 | Fee Rate Rule là cùng một fee\_components thì đối với các đối tượng student khác nhau lại có mức charge khác nhau, Fee Rate Rule allows việc đó |
| WA-R3-08 | Student Charge là khoản phải thu (outstanding charge). **Phụ huynh xem danh sách charge và tự tick chọn khoản muốn thanh toán**; hệ thống không tự động trừ/thu toàn bộ. |
| WA-R3-09 | Adjustment như FAS (func4 sau này) không sửa trực tiếp số tiền gốc của Student Charge mà tuỳ vào account của từng học sinh. |

## **1.4 Definitions, Acronyms and Abbreviations**

| Thuật ngữ | Giải thích |
| ----- | ----- |
| EA | Education Account, tài khoản tiền giáo dục của học sinh Singapore Citizen |
| MOE HQ / School user | Người dùng Bộ Giáo dục cấp trung ương / người dùng của từng trường |
| Academic year | Năm học, khoảng \[start\_date, end\_date\_exclusive) |
| Academic level | Cấp lớp: P1 đến P6, S1…, JC1 |
| Offering | Bản ghi cho biết trường nào dạy cấp nào trong năm học nào (school\_level\_offerings) |
| Class | Lớp (ví dụ P6A) nằm dưới một offering |
| Enrollment | Việc học sinh học tại một trường trong một khoảng thời gian |
| Class assignment | Việc một enrollment học một lớp trong một khoảng thời gian |
| Fee type | Phân loại cấp cao của phí |
| Fee component | Khoản phí cụ thể có thể áp dụng cho học sinh; là danh mục, không phải khoản nợ |
| Fee rate rule | Mức phí của một fee component theo cấp học và loại cư trú |
| Fee batch | Đợt phát hành phí cho học sinh (fee\_publications); thuộc function riêng |
| GST | Thuế hàng hóa và dịch vụ; component có cờ is\_apply\_tax, rule có cờ is\_price\_include\_tax |
| SC / PR / IS | Nhóm cư trú của học sinh, hiểu là Singapore Citizen / Permanent Resident / International Student (cần xác nhận, Q11) |
| end\_exclusive | Ngày đầu tiên không còn hiệu lực |

## **2\. System Process Overview**

![][image7]

### **2.1. School Setup Process**

1. HQ User mở Academic Year (year\_number, start\_date, end\_date\_exclusive, status) và duy trì danh mục Academic Level.  
2. HQ User tạo School.  
3. HQ User tạo tài khoản School User và assign vào School; thông tin tài khoản được bàn giao cho School qua giấy tờ.  
4. School User khai báo School Level Offering (cấp học School dạy trong năm học).  
5. School User tạo Class dưới offering.  
6. School User tạo Student (nhập manual) và tạo enrolment tại School.  
7. School User gán enrolment vào Class (class assignment).  
8. Với Student có category SC, System liên kết Student với Education Account.

### **2.2. Student Transfer Process**

1. School User báo HQ về việc Student đổi lớp hoặc chuyển trường (ngoài hệ thống hoặc qua kênh được thống nhất).  
2. Đổi lớp trong cùng School: HQ User đóng class assignment cũ (assigned\_to\_exclusive \= ngày hiệu lực) và mở assignment mới; enrollment giữ nguyên.  
3. Chuyển trường: HQ User đóng enrollment và assignment ở School A, mở enrollment (enrolled\_from \= cùng ngày hiệu lực) và assignment mới ở School B.  
4. Bảng students không đổi; các Student Charge đã phát hành giữ nguyên.

### **2.3. Fee Configuration và Publication Process**

1. HQ User tạo Fee Type và Fee Component.  
2. HQ User chọn đối tượng áp dụng (Level, Class, citizenship hoặc Student cụ thể) và cấu hình giá bằng Fee Rate Rule hoặc Fixed Amount.  
3. HQ User tạo Fee Publication: chọn Fee Component, School, Academic Year, billing period, **charge date** và **payment deadline (due date)**.  
4. Khi publish, System resolve danh sách Student theo eligibility\_date, xác định giá theo pricing\_date, tạo một Student Charge cho mỗi Student.  
5. Student Charge xuất hiện trong danh sách outstanding charges để phụ huynh xem và chọn thanh toán (R9).

### **2.4. Charge Adjustment Process**

User có quyền chọn Student Charge, nhập adjustment amount và reason code; System ghi nhận người tạo, thời điểm tạo; approval theo quy tắc được xác nhận; số tiền gốc luôn được giữ nguyên.

## **3\. Detailed Functions and Solution Design**

### **3.1.1 Function Description**

### **Sub-functions**

| Mã | Sub-function | Actor | Mục đích |
| :---- | :---- | :---- | :---- |
| F01 | School Management | MOE HQ User | Tạo và duy trì hồ sơ School (school\_code, tên, loại trường, status) |
| F02 | School User Account Assignment | MOE HQ User | Tạo tài khoản School User và assign vào School |
| F03 | Academic Year, Academic Level và School Level Offering | HQ User (Year, Level); School User (offering) | Master data và cấp học School dạy (cấp 1 hay 2\) trong năm học |
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

#### **Business Rules**

**Nhóm A – School Management (F01 đến F08)**

| Mã | Quy tắc | F |
| :---- | :---- | :---- |
| BR-R3-01 | moe\_school\_code, khi có giá trị, phải duy nhất | F01 |
| BR-R3-02 | School mới tạo ở trạng thái active; School inactive không dùng cho offering hoặc Fee Publication mới, dữ liệu lịch sử giữ nguyên | F01 |
| BR-R3-03 | Không xóa School đã có offering, enrolment hoặc Student Charge; chỉ deactivate | F01 |
| BR-R3-04 | Mỗi School User phải gắn với ít nhất một School hợp lệ | F02 |
| BR-R3-05 | School User chỉ truy cập dữ liệu thuộc School của mình | F02 |
| BR-R3-06 | Cơ chế cấp mật khẩu lần đầu và đổi mật khẩu \[TBC\] | F02 |
| BR-R3-07 | year\_number duy nhất; start\_date nhỏ hơn end\_date\_exclusive | F03 |
| BR-R3-08 | academic\_levels.code duy nhất; education\_stage thuộc PRIMARY, SEC hoặc PRE\_UNI | F03 |
| BR-R3-09 | Mỗi bộ ba (School, Academic Year, Academic Level) chỉ có một offering | F03 |
| BR-R3-10 | Offering chỉ tạo với School, Academic Year, Academic Level hợp lệ; có cho tạo offering ở năm học CLOSED hay không \[TBC, Q26\] | F03 |
| BR-R3-11 | Không xóa offering đã có Class; Academic Level đang có offering chỉ được deactivate | F03 |
| BR-R3-12 | Class phải thuộc một offering; chưa có offering thì không tạo được Class | F04 |
| BR-R3-13 | class\_code duy nhất trong cùng offering; class\_kind mặc định FORM | F04 |
| BR-R3-14 | Class gắn với năm học: sang năm mới tạo Class mới dưới offering mới (P6A-2026 và P6A-2027 là hai bản ghi); không xóa Class đã có assignment | F04 |
| BR-R3-15 | Student là định danh lâu dài, độc lập School và Class; id không đổi khi chuyển lớp, chuyển trường hoặc nghỉ học | F05 |
| BR-R3-16 | category thuộc SC, PR hoặc IS; đây là nhóm cư trú dùng cho Education Account eligibility và có thể dùng cho rate rule \[TBC, Q22\] | F05 |
| BR-R3-17 | Chống tạo trùng Student theo (source\_system, source\_reference) \[đề xuất, Dev xác nhận\] | F05 |
| BR-R3-18 | students không lưu trạng thái đang học (thuộc enrolment và assignment); không xóa Student đã có enrolment hoặc Student Charge | F05 |
| BR-R3-19 | Ngày kết thúc dạng exclusive là ngày đầu tiên không còn hiệu lực; null nghĩa là đang hiệu lực; khi có giá trị phải lớn hơn ngày bắt đầu | F06 |
| BR-R3-20 | Hai khoảng liền kề (kết thúc 01/07, bắt đầu 01/07) không chồng lấn; Student không được có hai enrolment chồng lấn \[TBC\] | F06 |
| BR-R3-21 | Class của assignment phải cùng School với enrolment; FK không tự đảm bảo nên backend phải validate | F06 |
| BR-R3-22 | Khoảng assignment nằm trong khoảng enrolment và trong năm học của Class (qua offering) | F06 |
| BR-R3-23 | Tại một ngày, một enrolment chỉ có một assignment hiệu lực \[TBC\] | F06 |
| BR-R3-24 | Đổi lớp trong cùng School \= đóng assignment cũ và mở assignment mới; không ghi đè bản ghi cũ | F07 |
| BR-R3-25 | Chuyển trường \= đóng enrolment và assignment ở School A, mở enrolment và assignment ở School B; hai khoảng liền kề không chồng lấn; Student id không đổi | F07 |
| BR-R3-26 | Student Charge đã phát hành giữ nguyên enrolment và School tại thời điểm phát hành; mọi thay đổi ghi audit (người sửa, thời điểm, giá trị cũ và mới); xử lý charge chưa thanh toán khi chuyển trường \[TBC, Q17\] | F07 |
| BR-R3-27 | Chỉ Student có category \= SC được liên kết Education Account; liên kết một lần cho mỗi Student, không làm thay đổi số dư; Account chưa tồn tại (dưới 7 tuổi) hoặc đã đóng (từ 16 tuổi) xử lý theo Q16 | F08 |

**Nhóm B – Fee Management (F09 đến F16)**

| Mã | Quy tắc | F |
| :---- | :---- | :---- |
| BR-R3-28 | Mỗi Fee Type có code duy nhất | F09 |
| BR-R3-29 | Fee Type mới mặc định active | F09 |
| BR-R3-30 | Fee Type inactive không dùng cho Fee Component hoặc cấu hình mới | F09 |
| BR-R3-31 | Dữ liệu hiện có giữ nguyên khi deactivate | F09 |
| BR-R3-32 | Fee Component phải tham chiếu Fee Type tồn tại | F10 |
| BR-R3-33 | component\_code duy nhất | F10 |
| BR-R3-34 | Mặc định active; is\_apply\_tax mặc định true | F10 |
| BR-R3-35 | Component inactive không dùng cho cấu hình mới | F10 |
| BR-R3-36 | owner\_school\_id null nghĩa là component do MOE tạo | F10 |
| BR-R3-37 | Rule phải tham chiếu Fee Component hợp lệ | F11 |
| BR-R3-38, 39 | academic\_level\_id hoặc student\_category null nghĩa là áp dụng mọi Level hoặc category | F11 |
| BR-R3-40 | currency\_code mặc định SGD; is\_price\_include\_tax mặc định false | F11 |
| BR-R3-41 | Rate áp dụng được xác định theo pricing\_date và thuộc tính Student | F11 |
| BR-R3-42 | Phân biệt rõ rate-rule pricing và fixed-amount pricing trong Fee Publication | F11 |
| BR-R3-43 | Khi nhiều rule cùng khớp, áp dụng precedence được xác nhận \[TBC, Q03\]; đề xuất: rule cụ thể nhất thắng, sau đó effective\_from mới nhất | F11 |
| BR-R3-44 | Publication phải tham chiếu Fee Component, School, Academic Year hợp lệ | F12 |
| BR-R3-45 | period\_end\_exclusive lớn hơn period\_start | F12 |
| BR-R3-46 | eligibility\_date xác định enrolment và class dùng để resolve target | F12 |
| BR-R3-47 | pricing\_date xác định rate rule có hiệu lực | F12 |
| BR-R3-48 | RATE\_RULE: các trường fixed price phải NULL; FIXED\_AMOUNT: các trường fixed price phải hợp lệ | F12 |
| BR-R3-49 | Status PUBLISHED bắt buộc có published\_by và published\_at | F12 |
| BR-R3-50 | Target phải thuộc School của publication | F12 |
| BR-R3-51 | Ngăn xử lý publish trùng (idempotent); dùng row\_version chống cập nhật đồng thời | F12 |
| BR-R3-52 | due\_date không được trước charge\_date \[TBC, Q18\] | F12 |
| BR-R3-53 | Chỉ dùng giá trị hợp lệ của Fee\_Publication\_Target\_Modes và Fee\_Publication\_Target\_Types | F13 |
| BR-R3-54 | Class target phải thuộc một offering của School; Level target phải có offering của School trong Academic Year của Publication | F13 |
| BR-R3-55 | Citizenship filter dùng giá trị của Student\_Citizenships \[TBC, Q22\] | F13 |
| BR-R3-56 | Target membership đánh giá theo eligibility\_date | F13 |
| BR-R3-57 | Cách kết hợp nhiều target cần xác nhận; đề xuất: union giữa các target, citizenship là điều kiện lọc (intersection) | F13 |
| BR-R3-58 | Recipient phải tham chiếu Publication và Student hợp lệ | F14 |
| BR-R3-59 | Recipient phải tham chiếu enrolment dùng để resolve; backend kiểm tra enrolment thuộc Student | F14 |
| BR-R3-60 | Mỗi Student chỉ xuất hiện một lần trong một Publication | F14 |
| BR-R3-61 | Student Charge tham chiếu hợp lệ Student, enrolment, School, Academic Year, Fee Component | F15 |
| BR-R3-62 | source\_type chỉ là PUBLICATION hoặc MANUAL; charge từ Publication phải có fee\_publication\_id | F15 |
| BR-R3-63 | base\_amount, tax\_amount \>= 0; total\_amount \= base\_amount \+ tax\_amount | F15 |
| BR-R3-64 | period\_end\_exclusive lớn hơn period\_start | F15 |
| BR-R3-65 | UNIQUE(fee\_publication\_id, student\_id) khi fee\_publication\_id không null | F15 |
| BR-R3-66 | Publication RATE\_RULE thì fee\_rate\_rule\_id phải có giá trị; FIXED\_AMOUNT thì có thể null | F15 |
| BR-R3-67 | Backend kiểm tra student\_id thuộc enrollment\_id; rate rule khớp Fee Component, citizenship snapshot, Level và pricing\_date | F15 |
| BR-R3-68 | Manual charge dùng idempotency\_key để chống xử lý trùng | F15 |
| BR-R3-69 | Không ghi đè số tiền gốc để thể hiện adjustment | F15 |
| BR-R3-70 | Chỉ Student Charge POSTED hiển thị cho phụ huynh chọn thanh toán; DRAFT và VOID không hiển thị | F15 |
| BR-R3-71 | Adjustment phải tham chiếu Student Charge tồn tại | F16 |
| BR-R3-72 | Bắt buộc reason\_code hợp lệ | F16 |
| BR-R3-73 | Giữ nguyên số tiền gốc; effective amount \= total\_amount \+ tổng adjustment đã áp dụng | F16 |
| BR-R3-74 | Ghi lại người tạo và thời điểm tạo | F16 |
| BR-R3-75 | Yêu cầu approval và thời điểm adjustment có hiệu lực cần xác nhận (Q08) | F16 |
| BR-R3-76 | Effective amount sau điều chỉnh không được âm \[TBC\] | F16 |

**Quy tắc Education Account payment (tham chiếu R9)**  
Schema hiện tại chưa có payment transaction, nên đây là business rule; xử lý thanh toán thuộc R9.

| Mã | Quy tắc |
| :---- | :---- |
| BR-R3-77 | Student Singaporean có thể dùng số dư Education Account để thanh toán phí đủ điều kiện |
| BR-R3-78 | Không mặc định mọi Fee Component đều đủ điều kiện thanh toán bằng Education Account (Q12) |
| BR-R3-79 | Phụ huynh chọn từng Student Charge muốn thanh toán trong danh sách outstanding charges; không thanh toán hoặc thu toàn bộ tự động |
| BR-R3-80 | Nguồn citizenship và số dư; validate số dư, trừ tiền, thiếu số dư, thanh toán một phần, reconciliation thuộc R9 |

### **3.1.2 Process Flow Description and Screens**

#### **F01 – School Management**

**Actor:** MOE HQ User. **Trigger:** HQ mở School Management. **Điều kiện:** đã đăng nhập và có quyền quản lý School.  
1\.     HQ User mở danh sách School.  
2\.     HQ User tạo mới hoặc chọn School hiện có.  
3\.     HQ User nhập name, school\_type và moe\_school\_code (nếu có).  
4\.     System validate required fields và tính duy nhất của moe\_school\_code.  
5\.     System lưu School ở trạng thái active và hiển thị kết quả.

#### **F02 – School User Account Assignment**

**Actor:** MOE HQ User. **Điều kiện:** School đã tồn tại. Thông tin đăng nhập được bàn giao cho School qua giấy tờ, ngoài hệ thống (WA-R3-01).  
1\.     HQ User chọn School.  
2\.     HQ User tạo tài khoản School User (tên, email hoặc username và thông tin cần thiết).  
3\.     System tạo user với role School User và gắn với School.  
4\.     System hiển thị thông tin tài khoản để HQ User bàn giao cho School.

#### **F03 – Academic Year, Academic Level và School Level Offering**

**Actor:** HQ User (Academic Year, Academic Level); School User (offering, Q23).   
**Điều kiện:** School, Academic Year, Academic Level đã tồn tại và còn hiệu lực.  
Academic Year (khi nào) và Academic Level (cấp nào) là master data. Offering cho biết "School A dạy cấp P6 trong năm 2026"; không có offering thì không tạo được Class.  
1\.     HQ User mở Academic Year mới (year\_number, start\_date, end\_date\_exclusive, status).  
2\.     HQ User duy trì danh mục Academic Level (P1 đến P6, S1…, JC1…).  
3\.     School User chọn Academic Year và các Academic Level mà School dạy.  
4\.     System kiểm tra bộ ba (School, Academic Year, Academic Level) chưa tồn tại.  
5\.     System tạo School Level Offering ở trạng thái active.

#### **F04 – Class Management**

**Actor:** School User. **Điều kiện:** offering tương ứng đã tồn tại. School, Academic Year và Level của Class được suy ra từ offering.  
1\.     School User mở danh sách Class.  
2\.     School User chọn offering.  
3\.     School User nhập class\_code và class\_name.  
4\.     System validate (BR-R3-12, BR-R3-13).  
5\.     System lưu Class.

#### **F05 – Student Management**

**Actor:** School User (HQ User chỉ chỉnh enrolment và assignment, xem F07). **Điều kiện:** School User đã được assign School. Student là định danh lâu dài, độc lập với School và Class.  
1\.     School User mở Student Management và tạo Student.  
2\.     School User nhập display\_name, date\_of\_birth, category.  
3\.     System validate required fields, category và chống trùng.  
4\.     System lưu và hiển thị kết quả.

#### **F06 – Student Enrolment và Class Assignment**

**Actor:** School User. **Điều kiện:** Student đã tồn tại; Class đã tồn tại và thuộc School của User. Enrolment cho biết Student học ở School nào, khi nào; assignment gắn enrolment vào Class cụ thể, giữ lịch sử đổi lớp.  
1\.     School User chọn Student và School, nhập enrolled\_from.  
2\.     System tạo enrolment (enrolled\_to\_exclusive \= null, status ENROLLED).  
3\.     School User chọn Class và assigned\_from cho enrolment.  
4\.     System validate Class cùng School với enrolment và khoảng thời gian hợp lệ (BR-R3-21, BR-R3-22).  
5\.     System tạo class assignment (status ACTIVE).  
6\.     Với Student SC, System thực hiện F08.

#### **F07 – Student Transfer và Class Change**

**Actor:** MOE HQ User. **Điều kiện:** Student có enrolment đang hiệu lực; Class hoặc School đích tồn tại. Hệ thống đóng bản ghi cũ và mở bản ghi mới, không sửa đè (WA-R3-04).  
**Đổi lớp trong cùng School:**  
1\.     HQ User mở hồ sơ Student, chọn Class đích và ngày hiệu lực.  
2\.     System đóng assignment cũ (assigned\_to\_exclusive \= ngày hiệu lực, status ENDED).  
3\.     System mở assignment mới dưới cùng enrolment; enrolment giữ nguyên.  
**Chuyển trường (ví dụ ngày hiệu lực 01/07/2026):**  
1\.     HQ User chọn School đích, Class đích và ngày hiệu lực.  
2\.     System đóng enrolment ở School A (enrolled\_to\_exclusive \= 2026-07-01, status TRANSFERRED) và đóng assignment ở A cùng mốc.  
3\.     System mở enrolment ở School B (enrolled\_from \= 2026-07-01) và assignment mới.  
4\.     Bảng students không thay đổi; Student Charge đã phát hành giữ nguyên.

#### **F08 – Education Account Linkage**

**Actor:** System. **Trigger:** class assignment đầu tiên của Student được tạo (F06). Student SC được liên kết với Education Account để đủ điều kiện dùng số dư thanh toán phí.  
1\.     System kiểm tra students.category của Student.  
2\.     Nếu category \= SC: System tìm Education Account của Student (do R1 tạo tự động) và tạo liên kết.  
3\.     Nếu category là PR hoặc IS: không liên kết.

#### **F09 – Fee Type Management**

**Actor:** HQ User, School User (theo phân quyền). **Điều kiện:** User có quyền.  
1\.     User mở Fee Type Management.  
2\.     User tạo mới hoặc chọn Fee Type.  
3\.     User nhập code.  
4\.     System validate required field và tính duy nhất.  
5\.     System lưu và hiển thị kết quả.

#### **F10 – Fee Component Management**

**Actor:** HQ User (chính); School User nếu được cho phép tạo component riêng \[TBC\]. Fee Component là danh mục phí, không phải khoản phải thu.  
1\.     User mở Fee Component Management.  
2\.     User tạo mới hoặc chọn Fee Component.  
3\.     User nhập component\_code, name và chọn Fee Type.  
4\.     User chọn is\_apply\_tax.  
5\.     System validate (BR-R3-32, BR-R3-33) và lưu.  
owner\_school\_id tham chiếu schools.id hay users.id cần Dev xác nhận (Q14).

#### **F11 – Fee Rate Rule Management**

**Actor:** HQ User, School User (theo phân quyền). Với cùng một Fee Component, các nhóm Student khác nhau có thể có mức phí khác nhau. Rate Rule xác định thu bao nhiêu, không xác định học sinh nào bị thu.  
1\.     User chọn Fee Component và xem các rule hiện có.  
2\.     User tạo hoặc sửa rule.  
3\.     User chọn Academic Level và student\_category (nếu cần).  
4\.     User nhập price\_amount, effective\_from và trạng thái.  
5\.     System validate và lưu.

#### **F12 – Fee Publication Management**

**Actor:** HQ User, School User. **Điều kiện:** Fee Component, School, Academic Year tồn tại; user có quyền. Một Fee Publication là một lần phát hành một Fee Component cho một School, một Academic Year và một billing period, với đối tượng xác định, charge date và payment deadline.  
1\.     User tạo Publication, chọn Fee Component, School, Academic Year.  
2\.     User nhập billing period, eligibility\_date, pricing\_date.  
3\.     User chọn pricing mode: RATE\_RULE hoặc FIXED\_AMOUNT.  
4\.     User chọn target mode và cấu hình đối tượng (F13).  
5\.     User cấu hình charge date và due date.  
6\.     User lưu (Draft); System validate.  
7\.     Khi publish, System resolve recipient (F14) và generate Student Charge (F15), ghi published\_by và published\_at.

#### **F13 – Publication Target Configuration**

**Actor:** HQ User, School User. Xác định nhóm Student nhận phí: toàn trường, một hoặc nhiều Level, một hoặc nhiều Class, hoặc Student cụ thể; có thể lọc thêm theo citizenship.  
1\.     User chọn Publication và target mode.  
2\.     Với CUSTOM\_TARGETS, User thêm các target (Level, Class, Student, citizenship).  
3\.     System validate tham chiếu và School scope.  
4\.     System lưu.  
Diễn giải target\_mode (giả định, Q02): COMPONENT\_SCOPE lấy đối tượng theo phạm vi mặc định của Fee Component và School (toàn trường), không cần target chi tiết; CUSTOM\_TARGETS lấy đối tượng từ các dòng trong fee\_publication\_targets.

#### **F14 – Publication Recipient Resolution**

**Actor:** System. Ghi lại danh sách Student được xác định là người nhận của Publication và enrolment dùng để xác định, bảo đảm truy vết.  
1\.     System đọc Publication và target.  
2\.     System lấy enrolment và class assignment có hiệu lực tại eligibility\_date (Class qua offering ra School và Level).  
3\.     System xác định Student đủ điều kiện.  
4\.     System ghi recipient và resolved\_at.  
5\.     System chuyển danh sách sang F15.

#### **F15 – Student Charge Generation and Management**

**Actor:** System (từ Publication); User có quyền (manual). Student Charge là khoản phải thu (outstanding charge); phụ huynh xem danh sách và chọn khoản muốn thanh toán (R9), hệ thống không tự thu toàn bộ.  
1\.     System nhận Student đủ điều kiện từ F14, hoặc nhận yêu cầu manual.  
2\.     System validate Student và enrolment.  
3\.     System xác định giá: Rate Rule (theo Fee Component, citizenship, Level, pricing\_date) hoặc Fixed Amount.  
4\.     System tính tax nếu Fee Component áp dụng GST.  
5\.     System tạo Student Charge status DRAFT, gán charge\_date và due\_date.  
6\.     Khi ghi nhận chính thức, System set POSTED và posted\_at.  
7\.     Charge POSTED xuất hiện trong outstanding charges của phụ huynh.

#### **F16 – Student Charge Adjustment Management**

**Actor:** User có quyền; Approver (nếu cần approval). Ghi nhận điều chỉnh tăng hoặc giảm cho Student Charge đã phát hành, không sửa trực tiếp số tiền gốc.  
1\.     User chọn Student Charge.  
2\.     User nhập adjustment\_amount và chọn reason\_code.  
3\.     System validate, ghi created\_by và created\_at.  
4\.     Nếu cần approval, Approver duyệt; System ghi approved\_by và approved\_at.  
5\.     System áp dụng theo rule đã xác nhận; số tiền gốc không đổi.

#### **Màn hình**

Tài liệu R3 chưa mô tả màn hình; bảng dưới là đề xuất của BA, cần chốt với team UI.

| Màn hình | Function | Actor | Nội dung |
| :---- | :---- | :---- | :---- |
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

#### **Trường hợp ngoại lệ**

| F | Mã | Tình huống | Xử lý |
| :---- | :---- | :---- | :---- |
| F01 | AF01 | Trùng moe\_school\_code | Từ chối (E-03-09) |
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
| F15 | AF05 | Void | User có quyền void kèm lý do; ghi voided\_at và void\_reason (E-03-28) |
| F15 | EF01 | Generate thất bại | Ghi nhận lỗi; không xem charge chưa hoàn chỉnh là thành công (E-03-23) |

*End of Document*

## 

# **R3**

# **FUNCTIONAL SPECIFICATION – R3: School, Student và Fee Management**

Project: Education Account Management System · Portal: Admin Portal · Version: 1.1 (Draft) · Status: Proposed – Pending Business Clarification Reference: Requirement R3, Developer Database Design (Fee), trao đổi với Dev

## **1\. Introduction**

### **1.1. Overview**

Requirement 3 yêu cầu MOE HQ User và School User quản lý danh sách **School, Academic Level (level/cohort), Class, Student trong từng Class**, cùng **Fee Type và Fee Component** mà học sinh phải đóng. Học sinh Singaporean có thể dùng số dư Education Account để thanh toán các khoản phí đủ điều kiện.

Tài liệu này gồm hai nhóm chức năng:

* **School Management (F01–F08):** tạo School, cấp tài khoản School User, cấu hình Level/Class, quản lý Student, gán Student vào Class, xử lý chuyển lớp/chuyển trường và liên kết Student với Education Account.  
* **Fee Management (F09–F16):** Fee Type, Fee Component, Fee Rate Rule, Fee Publication, Publication Target, Publication Recipient, Student Charge, Student Charge Adjustment.

Quy tắc nghiệp vụ liên quan đến thanh toán bằng Education Account được ghi nhận ở mục 4; chi tiết payment thuộc requirement khác (R9, e-Service Portal).

### **1.2. Actors**

| Actor | Mô tả |
| :---- | :---- |
| MOE HQ User | Tạo School, tạo tài khoản và assign School User; quản lý Fee Component/cấu hình phí tập trung; chỉnh sửa Student khi chuyển lớp/chuyển trường; publish fee. |
| School User | Quản lý Level, Class, Student của trường mình; thực hiện các thao tác fee trong phạm vi được phân quyền. |
| System | Validate dữ liệu, xác định rate, resolve target, generate Student Charge, liên kết Student với Education Account. |

\[TBC\] Quyền chi tiết của từng actor cần xác nhận với client (xem mục 5.2).

### **1.3. Scope**

**In Scope:** School Management, School User assignment, Academic Level, Class, Student, Student–Class assignment, Student transfer, Education Account linkage, Fee Type, Fee Component, Fee Rate Rule, Fee Publication, Publication Target, Publication Recipient, Student Charge, Student Charge Adjustment, quy tắc Education Account payment eligibility.

**Out of Scope (tài liệu này):** Payment transaction, trừ số dư Education Account, reconciliation, màn hình chọn thanh toán của phụ huynh (e-Service Portal), tạo/đóng Education Account tự động theo tuổi (R1), FAS subsidy (R4).

**Dependencies:** academic\_years, users, education\_accounts (R1) được xem là entity có sẵn.

### **1.4. Assumptions và Limitations**

| ID | Working Assumption |
| :---- | :---- |
| WA-R3-01 | HQ tạo School và School User; việc bàn giao thông tin tài khoản cho School thực hiện ngoài hệ thống (giấy tờ). |
| WA-R3-02 | Hiện tại Student được School User nhập **manual**; chưa có import/đồng bộ từ hệ thống ngoài. |
| WA-R3-03 | School User tự cấu hình Level và Class của trường mình. |
| WA-R3-04 | Khi Student chuyển lớp hoặc chuyển trường, HQ User cập nhật lại cấu hình Student cho khớp với lớp hiện tại. |
| WA-R3-05 | Student Singaporean khi được thêm vào Class sẽ được liên kết với Education Account. |
| WA-R3-06 | Fee Type là phân loại cấp cao; Fee Component là khoản phí cụ thể và là danh mục phí, không phải khoản phải thu. |
| WA-R3-07 | Fee Rate Rule trả lời câu hỏi “thu bao nhiêu”; Publication Target trả lời “thu của ai”. |
| WA-R3-08 | Student Charge là khoản phải thu (outstanding charge). **Phụ huynh xem danh sách charge và tự tick chọn khoản muốn thanh toán**; hệ thống không tự động trừ/thu toàn bộ. |
| WA-R3-09 | Adjustment không sửa trực tiếp số tiền gốc của Student Charge. |
| WA-R3-10 | Schema School/Student chưa được cung cấp; các field ở F01–F08 là **Proposed** và cần Dev xác nhận. |

## **2\. System Process Overview**

### **2.1. School Setup Process**

1. HQ User tạo School.  
2. HQ User tạo tài khoản School User và assign vào School. Thông tin tài khoản được bàn giao cho School qua giấy tờ.  
3. School User đăng nhập và tạo Academic Level (nếu chưa có) và Class.  
4. School User tạo Student (nhập manual).  
5. School User assign Student vào Class (tạo enrolment cho Academic Year hiện hành).  
6. Với Student Singaporean, System liên kết Student với Education Account.

### **2.2. Student Transfer Process**

1. School User báo HQ về việc Student chuyển lớp/chuyển trường (ngoài hệ thống hoặc qua kênh được thống nhất).  
2. HQ User mở hồ sơ Student và cập nhật enrolment (School/Level/Class) cho khớp với thực tế.  
3. System đóng enrolment cũ, tạo enrolment mới, giữ nguyên lịch sử và các Student Charge đã phát hành.

### **2.3. Fee Configuration và Publication Process**

1. HQ User tạo Fee Type và Fee Component.  
2. HQ User chọn đối tượng áp dụng (Level, Class, citizenship hoặc Student cụ thể) và cấu hình giá bằng Fee Rate Rule hoặc Fixed Amount.  
3. HQ User tạo Fee Publication: chọn Fee Component, School, Academic Year, billing period, **charge date** và **payment deadline (due date)**.  
4. Khi publish, System resolve danh sách Student theo eligibility\_date, xác định giá theo pricing\_date, tạo một Student Charge cho mỗi Student.  
5. Student Charge xuất hiện trong danh sách outstanding charges để phụ huynh xem và chọn thanh toán (R9).

### **2.4. Charge Adjustment Process**

User có quyền chọn Student Charge, nhập adjustment amount và reason code; System ghi nhận người tạo, thời điểm tạo; approval theo quy tắc được xác nhận; số tiền gốc luôn được giữ nguyên.

## **3\. Detailed Functions**

### **PHẦN A – SCHOOL MANAGEMENT**

### **3.1. F01 – School Management**

**Mô tả:** HQ User tạo và duy trì danh sách School. **Actor:** MOE HQ User. **Trigger:** HQ mở School Management. **Preconditions:** User đã đăng nhập và có quyền quản lý School.

**Main Flow:**

1. HQ User mở danh sách School.  
2. HQ User tạo mới hoặc chọn School hiện có.  
3. HQ User nhập school code, tên và thông tin liên quan.  
4. System validate required fields và tính duy nhất của school code.  
5. System lưu School ở trạng thái active và hiển thị kết quả.

**Data Requirements (Proposed):**

| Field | Mô tả | Constraint |
| :---- | :---- | :---- |
| id | School identifier | UUID, PK |
| school\_code | Mã School | Unique, NOT NULL |
| name | Tên School | NOT NULL |
| is\_active | Trạng thái hoạt động | BIT, Default \= true |
| (other) | Địa chỉ, liên hệ, loại trường | \[TBC\] |

**Business Rules:**

* BR-R3-01: school\_code là duy nhất.  
* BR-R3-02: School mới tạo ở trạng thái active.  
* BR-R3-03: School bị deactivate không dùng được cho cấu hình/publication mới; dữ liệu hiện có được giữ nguyên.

**Exception Flows:** AF01 – Duplicate code: reject và yêu cầu giá trị khác. EF01 – Save failure: báo lỗi, không xác nhận đã lưu.

**Acceptance Criteria:**

* AC01: Given school\_code chưa tồn tại, when HQ User lưu, then System tạo School.  
* AC02: Given school\_code đã tồn tại, when HQ User lưu, then System từ chối.  
* AC03: Given School bị deactivate, when tạo Fee Publication mới cho School đó, then System từ chối.

### **3.2. F02 – School User Account Assignment**

**Mô tả:** HQ User tạo tài khoản School User và assign vào School. Thông tin đăng nhập được bàn giao cho School ngoài hệ thống. **Actor:** MOE HQ User. **Preconditions:** School đã tồn tại.

**Main Flow:**

1. HQ User chọn School.  
2. HQ User tạo tài khoản School User (tên, email/username và thông tin cần thiết).  
3. System tạo user với role School User và gắn với School.  
4. System hiển thị thông tin tài khoản để HQ User bàn giao cho School.

**Data Requirements (Proposed):** users (đã có) \+ bảng gán user\_schools (user\_id, school\_id) hoặc cột school\_id trên users \[TBC – Dev xác nhận\].

**Business Rules:**

* BR-R3-04: Mỗi School User phải gắn với ít nhất một School hợp lệ.  
* BR-R3-05: School User chỉ truy cập dữ liệu thuộc School của mình.  
* BR-R3-06: Cơ chế cấp mật khẩu lần đầu/đổi mật khẩu \[TBC\].

**Acceptance Criteria:**

* AC04: Given School hợp lệ, when HQ User tạo School User, then user được tạo và gắn với School.  
* AC05: Given School User của School A, when truy cập dữ liệu School B, then System từ chối.

### **3.3. F03 – Academic Level Management**

**Mô tả:** School User cấu hình Level/Cohort của trường mình. **Actor:** School User (HQ User xem/hỗ trợ). **Preconditions:** School User đã được assign School.

**Main Flow:** Mở danh sách Level → tạo hoặc chọn Level → nhập level code, tên, thứ tự → System validate → lưu.

**Data Requirements (Proposed):**

| Field | Mô tả | Constraint |
| :---- | :---- | :---- |
| id | Level identifier | UUID, PK |
| school\_id | School sở hữu Level | FK → schools.id \[TBC: Level dùng chung toàn hệ thống hay theo School\] |
| level\_code / name | Mã và tên | Unique trong phạm vi School |
| display\_order | Thứ tự | Optional |
| is\_active | Trạng thái | Default \= true |

**Business Rules:**

* BR-R3-07: Level code duy nhất trong phạm vi quản lý.  
* BR-R3-08: Level đang có Class/Student/Fee Rate Rule tham chiếu không được xóa; chỉ deactivate.

**Acceptance Criteria:** AC06 – tạo Level hợp lệ thành công; AC07 – trùng code bị từ chối; AC08 – Level đang được tham chiếu không bị xóa.

### **3.4. F04 – Class Management**

**Mô tả:** School User tạo và duy trì Class của trường theo Academic Year và Level. **Actor:** School User. **Preconditions:** School, Level và Academic Year tồn tại.

**Main Flow:** Mở danh sách Class → tạo hoặc chọn Class → chọn Level, Academic Year, nhập class name/code → System validate → lưu.

**Data Requirements (Proposed):**

| Field | Mô tả | Constraint |
| :---- | :---- | :---- |
| id | Class identifier | UUID, PK |
| school\_id | School | FK, NOT NULL |
| academic\_level\_id | Level | FK, NOT NULL |
| academic\_year\_id | Năm học | FK, NOT NULL |
| class\_name / code | Tên/mã lớp | Unique theo (school, academic\_year, class\_code) |
| is\_active | Trạng thái | Default \= true |

**Business Rules:**

* BR-R3-09: Class phải thuộc School của School User và gắn với một Level hợp lệ của School đó.  
* BR-R3-10: Class code duy nhất theo School và Academic Year.  
* BR-R3-11: Class đang có Student không được xóa; deactivate chỉ khi không còn enrolment active \[TBC\].

**Acceptance Criteria:** AC09 – tạo Class hợp lệ thành công; AC10 – Level không thuộc School bị từ chối; AC11 – trùng class code bị từ chối.

### **3.5. F05 – Student Management**

**Mô tả:** School User tạo và cập nhật hồ sơ Student bằng nhập tay. **Actor:** School User; HQ User (chỉnh sửa theo F07). **Preconditions:** School User được assign School.

**Main Flow:** Mở Student Management → tạo Student → nhập thông tin định danh, ngày sinh, citizenship, student category → System validate (bắt buộc, trùng) → lưu → hiển thị kết quả.

**Data Requirements (Proposed):**

| Field | Mô tả | Constraint |
| :---- | :---- | :---- |
| id | Student identifier | UUID, PK |
| student\_code / national\_id | Định danh học sinh | Unique \[TBC: dùng trường nào làm định danh\] |
| full\_name | Họ tên | NOT NULL |
| date\_of\_birth | Ngày sinh | NOT NULL (cần cho R1 – tuổi 7 đến 16\) |
| citizenship | Quốc tịch | Enum: Student\_Citizenships |
| student\_category | Loại định cư | Enum: Student\_Categories |

**Business Rules:**

* BR-R3-12: Student phải có định danh duy nhất để tránh tạo trùng.  
* BR-R3-13: ; citizenship và student\_category phải thuộc giá trị enum hỗ trợhai thuộc tính này được dùng cho rate rule matching và Education Account eligibility.  
* BR-R3-14: Student chỉ được tạo trong phạm vi School của School User.  
* BR-R3-15: Không xóa Student đã có enrolment hoặc Student Charge; chỉ deactivate.

**Exception Flows:** AF01 – Duplicate Student: cảnh báo/từ chối. AF02 – Thiếu dữ liệu bắt buộc: reject.

**Acceptance Criteria:** AC12 – tạo Student hợp lệ thành công; AC13 – định danh trùng bị từ chối; AC14 – Student đã có Student Charge không thể xóa.

### **3.6. F06 – Student–Class Assignment (Enrolment)**

**Mô tả:** School User thêm Student vào Class, tạo bản ghi enrolment làm cơ sở cho resolve Publication Recipient và Student Charge. **Actor:** School User. **Preconditions:** Student và Class tồn tại, cùng School.

**Main Flow:**

1. User chọn Class và chọn Student cần thêm.  
2. System kiểm tra Student chưa có enrolment active trong cùng Academic Year.  
3. System tạo enrolment (school, class, level, academic year, start\_date).  
4. Nếu Student là Singaporean, System thực hiện F08 (liên kết Education Account).

**Data Requirements (Proposed) – student\_school\_enrollments:**

| Field | Mô tả | Constraint |
| :---- | :---- | :---- |
| id | Enrolment identifier | UUID, PK |
| student\_id | Student | FK, NOT NULL |
| school\_id / academic\_level\_id / school\_class\_id | Vị trí học | FK, NOT NULL |
| academic\_year\_id | Năm học | FK, NOT NULL |
| start\_date / end\_date | Hiệu lực | end\_date nullable |
| status | Active / Ended | Enum |

**Business Rules:**

* BR-R3-16: Một Student chỉ có một enrolment active trong một Academic Year \[TBC\].  
* BR-R3-17: Class phải thuộc School của enrolment; Level của enrolment lấy từ Class.  
* BR-R3-18: Enrolment lưu theo khoảng hiệu lực để tra cứu theo eligibility\_date.

**Acceptance Criteria:** AC15 – thêm Student vào Class thành công; AC16 – Student đã có enrolment active cùng năm bị từ chối; AC17 – Class khác School bị từ chối.

### **3.7. F07 – Student Transfer (HQ cập nhật)**

**Mô tả:** Khi Student chuyển lớp hoặc chuyển trường, HQ User cập nhật cấu hình Student cho khớp với lớp hiện tại. **Actor:** MOE HQ User. **Preconditions:** Student có enrolment active; Class/School đích tồn tại.

**Main Flow:**

1. HQ User tìm Student và mở hồ sơ.  
2. HQ User chọn School/Class đích và ngày hiệu lực.  
3. System validate Class thuộc School đích.  
4. System đặt end\_date cho enrolment cũ, tạo enrolment mới.  
5. System giữ nguyên các Student Charge và Publication Recipient đã có.

**Business Rules:**

* BR-R3-19: Chuyển lớp/chuyển trường không được ghi đè enrolment cũ; phải lưu lịch sử.  
* BR-R3-20: Student Charge đã phát hành vẫn gắn với enrolment/School tại thời điểm phát hành; không tự động chuyển sang School mới.  
* BR-R3-21: Các Publication chưa publish sẽ resolve theo eligibility\_date nên dùng enrolment hiệu lực tại ngày đó.  
* BR-R3-22: Mọi thay đổi phải ghi audit (người sửa, thời điểm, giá trị cũ/mới).  
* BR-R3-23: Charge chưa thanh toán của School cũ xử lý thế nào khi chuyển trường \[TBC – Q17\].

**Acceptance Criteria:** AC18 – chuyển lớp tạo enrolment mới và đóng enrolment cũ; AC19 – Student Charge cũ không thay đổi; AC20 – audit được ghi.

### **3.8. F08 – Education Account Linkage**

**Mô tả:** Khi Student Singaporean được thêm vào Class, System liên kết Student với Education Account tương ứng để Student đủ điều kiện dùng số dư thanh toán phí. **Actor:** System.

**Main Flow:**

1. Sau khi enrolment được tạo (F06), System kiểm tra citizenship.  
2. Nếu Singaporean: tìm Education Account của Student (do R1 tạo tự động) và tạo liên kết.  
3. Nếu không phải Singaporean: không liên kết.

**Business Rules:**

* BR-R3-24: Chỉ Student Singaporean được liên kết Education Account.  
* BR-R3-25: Liên kết chỉ thực hiện một lần cho mỗi Student; thêm vào Class khác không tạo account mới.  
* BR-R3-26: Nếu Education Account chưa tồn tại (Student chưa đủ 7 tuổi) hoặc đã đóng (từ 16 tuổi), hệ thống xử lý theo quy tắc xác nhận \[TBC – Q16\].  
* BR-R3-27: Liên kết không làm thay đổi số dư; payment thuộc mục 4\.

**Acceptance Criteria:** AC21 – Student Singaporean vào Class thì được liên kết; AC22 – Student non-Singaporean không có liên kết; AC23 – liên kết không bị tạo trùng.

### **PHẦN B – FEE MANAGEMENT**

### **3.9. F09 – Fee Type Management**

**Mô tả:** Duy trì phân loại phí cấp cao dùng để tổ chức Fee Component. **Actor:** MOE HQ User / School User (theo phân quyền). **Preconditions:** User có quyền.

**Main Flow:** Mở Fee Type Management → tạo mới/chọn → nhập code → System validate required field và uniqueness → lưu → hiển thị kết quả.

**Data Requirements:** id (UUID, PK); code (NVARCHAR(100), Unique); is\_active (BIT, Default \= true).

**Business Rules:**

* BR-R3-28: Mỗi Fee Type có code duy nhất.  
* BR-R3-29: Fee Type mới mặc định active.  
* BR-R3-30: Fee Type inactive không dùng cho Fee Component/cấu hình mới.  
* BR-R3-31: Dữ liệu hiện có được giữ nguyên khi deactivate.

**Exception Flows:** AF01 – Duplicate code; AF02 – Fee Type inactive bị chặn; EF01 – Save failure.

**Acceptance Criteria:** AC24 – code hợp lệ tạo được; AC25 – code trùng bị từ chối; AC26 – is\_active mặc định true.

### **3.10. F10 – Fee Component Management**

**Mô tả:** Định nghĩa từng khoản phí cụ thể có thể áp dụng cho học sinh. Fee Component là danh mục phí, không phải khoản phải thu. **Actor:** MOE HQ User (chính); School User nếu được cho phép tạo component riêng \[TBC\].

**Main Flow:** Mở Fee Component Management → tạo/chọn → nhập component\_code, name, Fee Type → chọn is\_apply\_tax → lưu.

**Data Requirements:**

| Field | Mô tả | Constraint |
| :---- | :---- | :---- |
| id | Component ID | UUID, PK |
| fee\_type\_id | Fee Type cha | FK → fee\_types.id |
| component\_code | Mã | Unique |
| name | Tên | NVARCHAR; mandatory \[TBC\] |
| is\_active | Dùng cho cấu hình mới | Default \= true |
| is\_apply\_tax | Áp dụng GST | Default \= true |
| owner\_school\_id | Người/School tạo; null \= MOE tạo | Nullable FK → users.id (theo schema) |

**Data model clarification:** owner\_school\_id đặt tên là School nhưng tham chiếu users.id – Dev cần xác nhận tham chiếu schools.id hay users.id (Q14).

**Business Rules:**

* BR-R3-32: Fee Component phải tham chiếu Fee Type tồn tại.  
* BR-R3-33: component\_code duy nhất.  
* BR-R3-34: Mặc định active; is\_apply\_tax mặc định true.  
* BR-R3-35: Component inactive không dùng cho cấu hình mới.  
* BR-R3-36: owner\_school\_id null nghĩa là component do MOE tạo.

**Acceptance Criteria:** AC27 – tạo thành công với Fee Type hợp lệ và code duy nhất; AC28 – Fee Type không tồn tại bị từ chối; AC29 – is\_apply\_tax mặc định true.

### **3.11. F11 – Fee Rate Rule Management**

**Mô tả:** Với cùng một Fee Component, các nhóm Student khác nhau có thể có mức phí khác nhau. Rate Rule xác định **thu bao nhiêu**, không xác định học sinh nào bị thu. **Actor:** MOE HQ User / School User (theo phân quyền).

**Main Flow:** Chọn Fee Component → xem rule hiện có → tạo/sửa rule → chọn Level và student\_category (nếu cần) → nhập price\_amount, effective\_from, trạng thái → System validate → lưu.

**Data Requirements:**

| Field | Mô tả | Constraint |
| :---- | :---- | :---- |
| id | Rule ID | UUID, PK |
| fee\_component\_id | Component | FK → fee\_components.id |
| academic\_level\_id | Level áp dụng | Nullable; null \= mọi Level |
| student\_category | Loại định cư | Nullable Enum; null \= mọi category |
| price\_amount | Mức giá | NUMERIC(18,2) |
| currency\_code | Tiền tệ | Default \= SGD |
| is\_price\_include\_tax | Giá đã gồm thuế | Default \= false |
| effective\_from | Hiệu lực từ ngày | DATE |
| status | Trạng thái | Enum: Fee\_Rate\_Rule\_Statuses |

**Business Rules:**

* BR-R3-37: Rule phải tham chiếu Fee Component hợp lệ.  
* BR-R3-38/39: academic\_level\_id/student\_category null nghĩa là áp dụng mọi Level/category.  
* BR-R3-40: currency\_code mặc định SGD; is\_price\_include\_tax mặc định false.  
* BR-R3-41: Rate áp dụng được xác định theo pricing\_date và thuộc tính Student.  
* BR-R3-42: Phân biệt rõ rate-rule pricing và fixed-amount pricing trong Fee Publication.  
* BR-R3-43: Khi nhiều rule cùng khớp, áp dụng precedence được xác nhận \[TBC – Q03\] (đề xuất: rule cụ thể nhất thắng, sau đó effective\_from mới nhất).

**Exception Flows:** AF01 – Không có rule khớp: không chọn rate tùy ý, không tạo charge cho Student đó cho đến khi có pricing hợp lệ. AF02 – Cấu hình sai: reject.

**Acceptance Criteria:** AC30 – tạo rule hợp lệ; AC31 – Level null áp dụng mọi Level; AC32 – chỉ xét rule có category khớp; AC33 – không có rule khớp thì không áp giá tùy ý.

### **3.12. F12 – Fee Publication Management**

**Mô tả:** Một Fee Publication là một lần phát hành một Fee Component cho một School, một Academic Year và một billing period, với đối tượng xác định, **charge date** và **payment deadline**. **Actor:** MOE HQ User / School User. **Preconditions:** Fee Component, School, Academic Year tồn tại; user có quyền.

**Main Flow:**

1. User tạo Publication, chọn Fee Component, School, Academic Year.  
2. Nhập billing period, eligibility\_date, pricing\_date.  
3. Chọn pricing mode: RATE\_RULE hoặc FIXED\_AMOUNT.  
4. Chọn target mode và cấu hình đối tượng (F13).  
5. Cấu hình charge date và due date (xem lưu ý bên dưới).  
6. Lưu (Draft); System validate.  
7. Khi publish, System resolve recipient (F14) và generate Student Charge (F15), ghi published\_by, published\_at.

**Data Requirements:**

| Field | Mô tả | Constraint |
| :---- | :---- | :---- |
| id | Publication ID | UUID, PK |
| fee\_component\_id | Component | FK |
| title / description | Tiêu đề / ghi chú | NVARCHAR(200) / nullable |
| school\_id, academic\_year\_id | School, năm học | FK, NOT NULL |
| target\_mode | COMPONENT\_SCOPE hoặc CUSTOM\_TARGETS | Enum: Fee\_Publication\_Target\_Modes |
| period\_start / period\_end\_exclusive | Billing period | DATE; end \> start |
| eligibility\_date / pricing\_date | Ngày xác định đối tượng / rate | DATE |
| fixed\_amount | Giá cố định mỗi Student | DECIMAL(18,2) ≥ 0 khi có |
| status | Trạng thái | Enum: Publication\_Statuses |
| created\_by / created\_at | Người/thời điểm tạo | FK users.id / DATETIME2 |
| published\_by / published\_at | Người/thời điểm publish | Nullable |
| row\_version | Concurrency | ROWVERSION |

**Lưu ý schema:** (1) Fee Publication hiện chưa có charge\_date và due\_date, trong khi flow nghiệp vụ yêu cầu HQ chọn ngày charge và deadline thanh toán; hai giá trị này hiện chỉ có ở Student Charge → đề xuất bổ sung vào fee\_publications (Q18). (2) Tài liệu DB nhắc fixed\_amount\_includes\_tax và fixed\_currency\_code nhưng cột chưa được liệt kê (Q15).

**Business Rules:**

* BR-R3-44: Phải tham chiếu Fee Component, School, Academic Year hợp lệ.  
* BR-R3-45: period\_end\_exclusive \> period\_start.  
* BR-R3-46: eligibility\_date xác định enrolment/class dùng để resolve target.  
* BR-R3-47: pricing\_date xác định rate rule có hiệu lực.  
* BR-R3-48: RATE\_RULE → các trường fixed price phải NULL; FIXED\_AMOUNT → các trường fixed price phải hợp lệ.  
* BR-R3-49: Status PUBLISHED bắt buộc có published\_by và published\_at.  
* BR-R3-50: Target phải thuộc School của publication.  
* BR-R3-51: Ngăn xử lý publish trùng (idempotent); dùng row\_version chống cập nhật đồng thời.  
* BR-R3-52: due\_date không được trước charge\_date \[TBC theo Q18\].

**Exception Flows:** AF01 – Billing period sai; AF02 – Pricing configuration sai; AF03 – Không có Student đủ điều kiện: không tạo charge; AF04 – Thiếu rate: Student đó không có charge; EF01 – Concurrent modification: yêu cầu refresh; EF02 – Publish thất bại: ghi nhận lỗi, không báo hoàn tất.

**Acceptance Criteria:** AC34 – tạo Publication hợp lệ; AC35 – period sai bị từ chối; AC36 – RATE\_RULE thì fixed fields null; AC37 – FIXED\_AMOUNT thì fixed fields hợp lệ; AC38 – publish xong có published\_by/published\_at; AC39 – hai người cùng sửa thì người sau nhận cảnh báo conflict.

### **3.13. F13 – Publication Target Configuration**

**Mô tả:** Xác định nhóm Student nhận phí: toàn trường, một hoặc nhiều Level, một hoặc nhiều Class, hoặc Student cụ thể, có thể lọc thêm theo citizenship.

**Data Requirements:** id; fee\_publication\_id (FK); target\_type (Enum: Fee\_Publication\_Target\_Types); academic\_level\_id, school\_class\_id, student\_id (nullable); citizenship (nullable Enum: Student\_Citizenships).

**Diễn giải target\_mode (Assumption, \[TBC\] – Q02):**

* COMPONENT\_SCOPE: đối tượng lấy theo phạm vi mặc định của Fee Component/School (toàn trường), không cần khai báo target chi tiết.  
* CUSTOM\_TARGETS: đối tượng lấy từ các dòng trong fee\_publication\_targets.

**Main Flow:** Chọn Publication → chọn target mode → với CUSTOM\_TARGETS thêm các target (Level/Class/Student, citizenship) → System validate tham chiếu và School scope → lưu.

**Business Rules:**

* BR-R3-53: Chỉ dùng giá trị hợp lệ của Fee\_Publication\_Target\_Modes và Fee\_Publication\_Target\_Types.  
* BR-R3-54: Level/Class target phải thuộc School của Publication.  
* BR-R3-55: Citizenship filter dùng giá trị của Student\_Citizenships.  
* BR-R3-56: Target membership đánh giá theo eligibility\_date.  
* BR-R3-57: Cách kết hợp nhiều target (union/intersection) cần xác nhận (đề xuất: union giữa các target; citizenship là điều kiện lọc intersection).

**Acceptance Criteria:** AC40 – target toàn trường chọn đúng Student của School; AC41 – target Level chỉ gồm Student thuộc Level; AC42 – target Class chỉ gồm Student thuộc Class; AC43 – target Student cụ thể được kiểm tra theo rule; AC44 – target ngoài School bị từ chối.

### **3.14. F14 – Publication Recipient Resolution**

**Mô tả:** Ghi lại danh sách Student được xác định là người nhận của Publication và enrolment dùng để xác định, đảm bảo truy vết.

**Data Requirements:** id; fee\_publication\_id; student\_id; enrollment\_id; resolved\_at (NOT NULL); UNIQUE(fee\_publication\_id, student\_id).

**Main Flow:** Đọc Publication và target → lấy enrolment có hiệu lực tại eligibility\_date → xác định Student đủ điều kiện → ghi recipient và resolved\_at → chuyển danh sách sang F15.

**Business Rules:**

* BR-R3-58: Recipient tham chiếu Publication và Student hợp lệ.  
* BR-R3-59: Recipient phải tham chiếu enrolment được dùng để resolve; backend kiểm tra enrolment thuộc Student.  
* BR-R3-60: Mỗi Student chỉ xuất hiện một lần trong một Publication.

**Exception Flows:** AF01 – Không có Student đủ điều kiện: không tạo recipient; AF02 – Duplicate: chặn; EF01 – Enrolment không thuộc Student: reject.

**Acceptance Criteria:** AC45 – resolve thành công ghi đủ recipient; AC46 – xử lý lại không tạo recipient trùng; AC47 – enrolment của Student khác bị từ chối.

### **3.15. F15 – Student Charge Generation và Management**

**Mô tả:** Tạo và quản lý khoản phải thu cho từng Student từ Publication hoặc phát hành manual. Student Charge là **outstanding charge**; phụ huynh xem danh sách và tick chọn khoản muốn thanh toán (R9), hệ thống không tự thu toàn bộ. **Actor:** System (từ Publication); authorized User (manual).

**Main Flow:**

1. Nhận Student đủ điều kiện từ F14 hoặc yêu cầu manual.  
2. Validate Student và enrolment.  
3. Xác định giá: Rate Rule (theo Fee Component, citizenship, Level, pricing\_date) hoặc Fixed Amount.  
4. Tính tax nếu Fee Component áp dụng GST.  
5. Tạo Student Charge với status DRAFT, gán charge\_date và due\_date.  
6. Khi ghi nhận chính thức: set POSTED và posted\_at.  
7. Charge POSTED xuất hiện trong outstanding charges của phụ huynh.

**Data Requirements:**

| Field | Mô tả | Constraint |
| :---- | :---- | :---- |
| id | Charge ID | UUID, PK |
| fee\_publication\_id | Publication nguồn | Nullable FK (null với manual) |
| student\_id, enrollment\_id | Student, enrolment | FK, NOT NULL |
| school\_id, academic\_year\_id, academic\_level\_id | Ngữ cảnh | FK, NOT NULL |
| school\_class\_id | Lớp tại thời điểm xác định | Nullable FK |
| fee\_component\_id | Khoản phí | FK, NOT NULL |
| source\_type | PUBLICATION / MANUAL | NOT NULL |
| pricing\_date | Ngày xác định rate | DATE, NOT NULL |
| period\_start / period\_end\_exclusive | Billing period | DATE, NOT NULL; end \> start |
| charge\_date / due\_date | Ngày phát hành / hạn thanh toán | DATE |
| base\_amount | Trước thuế/trợ cấp/điều chỉnh | DECIMAL(18,2) ≥ 0 |
| tax\_amount | Thuế | DECIMAL(18,2), Default 0, ≥ 0 |
| total\_amount | base \+ tax | DECIMAL(18,2) |
| currency\_code | Tiền tệ | CHAR(3), Default SGD |
| status | DRAFT / POSTED / VOID | NOT NULL |
| posted\_at / voided\_at / void\_reason | Mốc posting, void | Nullable |
| idempotency\_key | Chống tạo trùng manual | NVARCHAR(120), unique khi có |

**Lưu ý schema:** các ràng buộc nhắc fee\_rate\_rule\_id và citizenship\_snapshot nhưng chưa có trong danh sách cột (Q15). Ngoài ra chưa có trạng thái thanh toán (paid/unpaid) – cần xác định nơi lưu (Q19).

**Business Rules:**

* BR-R3-61: Tham chiếu hợp lệ Student, enrolment, School, Academic Year, Fee Component.  
* BR-R3-62: source\_type chỉ PUBLICATION hoặc MANUAL; charge từ Publication phải có fee\_publication\_id.  
* BR-R3-63: base\_amount, tax\_amount ≥ 0; total\_amount \= base\_amount \+ tax\_amount.  
* BR-R3-64: period\_end\_exclusive \> period\_start.  
* BR-R3-65: UNIQUE(fee\_publication\_id, student\_id) khi fee\_publication\_id không null.  
* BR-R3-66: Publication RATE\_RULE thì fee\_rate\_rule\_id phải có giá trị; FIXED\_AMOUNT thì có thể null.  
* BR-R3-67: Backend kiểm tra student\_id thuộc enrollment\_id; rate rule phải khớp Fee Component, citizenship snapshot, Level và pricing\_date.  
* BR-R3-68: Manual charge dùng idempotency\_key để chống xử lý trùng.  
* BR-R3-69: Không ghi đè số tiền gốc để thể hiện adjustment.  
* BR-R3-70: Chỉ Student Charge status POSTED mới hiển thị cho phụ huynh chọn thanh toán; DRAFT/VOID không hiển thị.

**Exception Flows:** AF01 – Thiếu rate rule: không tạo charge; AF02 – Enrolment không thuộc Student: reject; AF03 – Trùng charge: chặn; AF04 – Số tiền âm: reject; AF05 – Void: user có quyền void với lý do, ghi voided\_at và void\_reason; EF01 – Generate thất bại: ghi nhận lỗi, không xem charge chưa hoàn chỉnh là thành công.

**Acceptance Criteria:** AC48 – tạo charge cho Student đủ điều kiện; AC49 – total \= base \+ tax; AC50 – số tiền âm bị từ chối; AC51 – xử lý lại Publication không tạo charge trùng; AC52 – manual charge có source\_type \= MANUAL; AC53 – void ghi status VOID, voided\_at, void\_reason; AC54 – chỉ charge POSTED hiển thị cho phụ huynh.

### **3.16. F16 – Student Charge Adjustment Management**

**Mô tả:** Ghi nhận điều chỉnh tăng/giảm cho Student Charge đã phát hành, không sửa trực tiếp số tiền gốc, có audit trail. **Actor:** Authorized User; Approver (nếu cần approval).

**Main Flow:** Chọn Student Charge → nhập adjustment\_amount → chọn reason\_code → System validate → ghi created\_by, created\_at → (nếu cần) Approver duyệt, ghi approved\_by, approved\_at → áp dụng theo rule đã xác nhận; số tiền gốc không đổi.

**Data Requirements:** id; student\_charge\_id (FK → **student\_charges.id**; tài liệu DB ghi nhầm users.id, cần Dev sửa – Q20); adjustment\_amount DECIMAL(18,2) (dương \= tăng, âm \= giảm); reason\_code (Enum, ví dụ INCORRECT\_RATE, PRORATION, OTHER); created\_by, created\_at, approved\_by, approved\_at.

**Business Rules:**

* BR-R3-71: Phải tham chiếu Student Charge tồn tại.  
* BR-R3-72: Bắt buộc reason\_code hợp lệ.  
* BR-R3-73: Giữ nguyên số tiền gốc; effective amount \= total\_amount \+ tổng adjustment đã áp dụng.  
* BR-R3-74: Ghi lại người tạo và thời điểm tạo.  
* BR-R3-75: Yêu cầu approval và thời điểm adjustment có hiệu lực cần xác nhận (Q08).  
* BR-R3-76: Effective amount sau điều chỉnh không được âm \[TBC\].

**Acceptance Criteria:** AC55 – tạo adjustment hợp lệ; AC56 – số dương làm tăng effective amount; AC57 – số âm làm giảm; AC58 – số tiền gốc không đổi; AC59 – ghi created\_by và created\_at; AC60 – adjustment chờ duyệt chưa được tính là đã duyệt.

## **4\. Education Account Payment Business Rule**

Requirement 3 nêu rằng Student Singaporean có thể dùng số dư Education Account để thanh toán phí. Schema hiện tại chưa có payment transaction entity, nên đây là business rule và phần xử lý thanh toán cần làm rõ scope.

* BR-R3-77: Student Singaporean có thể dùng số dư Education Account để thanh toán phí đủ điều kiện.  
* BR-R3-78: Không mặc định mọi Fee Component đều đủ điều kiện thanh toán bằng Education Account.  
* BR-R3-79: Phụ huynh chọn từng Student Charge muốn thanh toán trong danh sách outstanding charges; không thanh toán/charge toàn bộ tự động.  
* BR-R3-80: Nguồn dữ liệu citizenship và số dư; validate số dư, trừ tiền, insufficient balance, partial payment, reconciliation thuộc requirement payment (R9).

**Open Scope Items:** Payment xử lý ở Admin Portal hay e-Service Portal? Component nào đủ điều kiện? Có validate số dư trước khi thanh toán? Xử lý thiếu số dư/partial payment? Hệ thống nào ghi transaction và cập nhật số dư?

## **5\. Data Integrity và Access Control**

### **5.1. Data Integrity**

Unique code của School, Fee Type, Fee Component; foreign key hợp lệ; billing period hợp lệ; số tiền không âm; total \= base \+ tax; UNIQUE(publication, student) cho recipient và charge; enrolment thuộc Student; rate rule khớp Fee Component, citizenship, Level, pricing\_date; metadata Publication khi PUBLISHED; lịch sử enrolment không bị ghi đè.

### **5.2. Access Control**

System giới hạn thao tác theo phạm vi quyền của user. \[TBC\] Client xác nhận:

* HQ User quản lý tất cả School và Fee Component.  
* School User chỉ quản lý dữ liệu School của mình (Level, Class, Student).  
* School User tự cấu hình rate hay chỉ publish phí do HQ cấu hình.  
* Quyền manual charge, void, adjustment, và việc adjustment cần người duyệt khác.  
* Chỉ HQ User được chuyển lớp/chuyển trường (theo trao đổi với Dev).

## **6\. Non-functional Requirements**

Chưa có yêu cầu định lượng. Cần xác nhận: hiệu năng publish/generate charge cho số lượng Student lớn; xử lý đồng thời; audit (Student transfer, publication, charge, adjustment); bảo vệ dữ liệu cá nhân học sinh; khả năng phục hồi khi publish thất bại; thời gian lưu trữ dữ liệu.

## **7\. Open Questions**

| ID | Câu hỏi | Priority |
| :---- | :---- | :---- |
| Q01 | Quyền chi tiết của MOE HQ User và School User cho từng function? | High |
| Q02 | Ý nghĩa chính xác của target mode (COMPONENT\_SCOPE, CUSTOM\_TARGETS) và target type; cách kết hợp nhiều target? | High |
| Q03 | Precedence khi nhiều rate rule cùng khớp? | High |
| Q04 | Không có rate rule khớp thì xử lý thế nào (bỏ qua Student, báo lỗi, chặn publish)? | High |
| Q05 | Vòng đời status Publication (draft, publish, cancel, republish)? | High |
| Q06 | Charge sinh ngay khi publish? Atomic hay cho phép thành công từng phần? | High |
| Q07 | Quy tắc due date của Publication và Student Charge? | High |
| Q08 | Adjustment có cần approval? Khi nào có hiệu lực? | High |
| Q09 | Charge POSTED có thể void không, hạn chế sau khi đã thanh toán? | High |
| Q10 | Cách tính và làm tròn GST? | High |
| Q11 | Gán Fee Component cho nhóm Student và billing period như thế nào? | High |
| Q12 | Fee Component nào đủ điều kiện thanh toán bằng Education Account? | High |
| Q13 | Payment thuộc Admin Portal hay e-Service Portal? | High |
| Q14 | owner\_school\_id tham chiếu schools.id hay users.id? | High |
| Q15 | Thiếu cột fee\_rate\_rule\_id, citizenship\_snapshot (Student Charge) và fixed\_amount\_includes\_tax, fixed\_currency\_code (Publication)? | High |
| Q16 | Education Account chưa tồn tại (dưới 7 tuổi) hoặc đã đóng (từ 16 tuổi) khi Student được thêm vào Class? | High |
| Q17 | Khi chuyển trường, charge chưa thanh toán của School cũ xử lý ra sao? | High |
| Q18 | Có bổ sung charge\_date và due\_date vào fee\_publications để HQ chọn khi phát hành? | High |
| Q19 | Trạng thái thanh toán (paid/unpaid/partial) của Student Charge lưu ở đâu? | High |
| Q20 | student\_charge\_adjustments.student\_charge\_id đang ghi FK → users.id, cần sửa thành student\_charges.id? | Medium |
| Q21 | School/Level/Class/Student/Enrolment/School User: schema và định danh Student (student code hay national ID)? Level dùng chung hay theo School? | High |
| Q22 | student\_category (Student\_Categories) và citizenship (Student\_Citizenships) khác nhau thế nào, rule dùng trường nào? | Medium |

## **8\. Function Summary**

| ID | Function | Mục đích chính |
| :---- | :---- | :---- |
| F01 | School Management | HQ tạo và duy trì School |
| F02 | School User Account Assignment | HQ tạo School User và assign vào School |
| F03 | Academic Level Management | School User cấu hình Level |
| F04 | Class Management | School User cấu hình Class |
| F05 | Student Management | School User tạo/cập nhật Student |
| F06 | Student–Class Assignment | Thêm Student vào Class (enrolment) |
| F07 | Student Transfer | HQ cập nhật khi Student chuyển lớp/trường |
| F08 | Education Account Linkage | Liên kết Student Singaporean với Education Account |
| F09 | Fee Type Management | Phân loại phí cấp cao |
| F10 | Fee Component Management | Danh mục khoản phí |
| F11 | Fee Rate Rule Management | Mức phí theo Level và category |
| F12 | Fee Publication Management | Phát hành phí cho School, kỳ phí, charge date, deadline |
| F13 | Publication Target Configuration | Xác định nhóm Student nhận phí |
| F14 | Publication Recipient Resolution | Resolve và lưu recipient |
| F15 | Student Charge Generation and Management | Tạo và quản lý khoản phải thu |
| F16 | Student Charge Adjustment Management | Điều chỉnh tăng/giảm có audit |
| Related | Education Account Payment Rule | Thanh toán bằng Education Account (theo R9) |

*End of R3*

