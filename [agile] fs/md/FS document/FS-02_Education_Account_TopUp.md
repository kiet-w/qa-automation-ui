# FS-02: Education Account Top-Up Management (Requirement 2)

> **Phân hệ**: Admin Portal (MOE HQ Users & System Background Jobs)  
> **Requirement**: R2 – Education Account Top-Up Management  
> **Product Backlog**: PB-14 (Sprint 2) | **User Story**: US-02 (FR2)  
> **Phiên bản baseline**: Official FSD Baseline (FS R2 – Top-Up Management.docx)  
> **Trạng thái**: Production Ready / Fully Aligned  

---

## 1. Introduction

### 1.1. Preface

Tài liệu này là Functional Specification (FS) cho Function 2 (R2) – Top-Up Management trên Admin Portal của hệ thống Education Account & FAS (MOE Singapore). Function 2 cho phép MOE HQ User nạp tiền vào Education Account (EA) theo hai cách: nạp lẻ cho từng chủ tài khoản (Individual Top-Up), hoặc nạp hàng loạt theo campaign với rule cấu hình theo độ tuổi, số dư và tình trạng đi học (Bulk Top-Up). Campaign chạy ad-hoc hoặc định kỳ. Top-up nhầm được sửa bằng bút toán hiệu chỉnh.

Function 2 chỉ ra lệnh ghi có (credit). Số dư và sổ cái EA thuộc Function 1; mục 2.2 nêu các điểm nối với R1, R3, R8, R9.

### 1.2. Personas

| Persona | Loại | Vai trò trong Function 2 |
| :--- | :--- | :--- |
| MOE HQ User | Primary actor | Nạp lẻ; tạo và cấu hình campaign; xem preview; xác nhận chạy; xem kết quả run; sửa top-up nhầm |
| School User | Không phải actor | Không có quyền Top-Up, không thấy menu Top-Up |
| Parent | Gián tiếp | Thấy giao dịch Top-up trong Transaction History (R8); có thể nhận thông báo (xem F2.8) |
| Admin Portal System | Hệ thống | Kiểm tra điều kiện, tính danh sách eligible, lập lịch, chạy batch, ghi log và audit |

### 1.3. Design Assumptions and Limitations

### Design Assumptions:

| ID | Assumption |
| :--- | :--- |
| DA-01 | Top-up là ghi có vào EA trong sổ cái Function 1. |
| DA-02 | Function 2 ghi có và ghi nợ hiệu chỉnh trực tiếp vào số dư EA, đồng thời thêm một bút toán vào sổ cái, trong cùng một database transaction. |
| DA-03 | Chỉ MOE HQ User dùng được Function 2. School User và Parent không có quyền |
| DA-04 | Chỉ EA có trạng thái Active mới nhận top-up. |
| DA-05 | Mọi lần ghi có (top-up lẻ, từng dòng trong batch, hiệu chỉnh) đều chạy Closure Eligibility Check của F02 trước khi thực hiện |
| DA-06 | Preview chỉ mang tính tham khảo. Khi chạy, hệ thống đánh giá lại từng tài khoản bằng dữ liệu tại thời điểm đó |
| DA-07 | Các criterion của campaign kết hợp bằng AND. Mỗi tài khoản eligible nhận một số tiền cố định |
| DA-08 | Một campaign thuộc một Academic Year và một Round. Cùng một kỳ có thể chạy nhiều campaign với criterion và số tiền khác nhau |
| DA-09 | Campaign chạy theo một trong hai chế độ: ad-hoc (chạy ngay hoặc vào một thời điểm HQ User chọn) hoặc định kỳ (hệ thống tự chạy theo lịch) |
| DA-10 | Sổ cái chỉ thêm mới. "Sửa" một top-up nhầm nghĩa là ghi một bút toán hiệu chỉnh mới; bút toán gốc không bị sửa hay xóa |
| DA-11 | Mỗi lần ghi có tạo một top-up transaction với FundingReference riêng, và kiểm tra idempotency key để không phát sinh hai giao dịch trùng |
| DA-12 | Tiền tệ SGD, 2 chữ số thập phân. Ngày hiển thị DD/MM/YYYY theo giờ Singapore (SGT, UTC+8); lưu UTC |

#### Limitations:

Sửa top-up nhầm chỉ áp dụng cho top-up lẻ. Sửa từng giao dịch trong batch chưa nằm trong phạm vi.

Function 2 chỉ được coi là đạt khi cả nạp lẻ, nạp hàng loạt (ad-hoc và định kỳ) và sửa top-up nhầm chạy đúng tiêu chí chấp nhận.

### 1.4. Definitions, Acronyms and Abbreviations

| Thuật ngữ | Giải thích |
| :--- | :--- |
| EA | Education Account. Tài khoản chi tiêu cho giáo dục của Singapore Citizen từ 7 đến dưới 16 tuổi. Số dư và sổ cái ở Function 1 |
| Top-Up | Giao dịch ghi có một số tiền SGD vào EA |
| Individual Top-Up | Top-up lẻ cho một EA do HQ User tìm và nhập số tiền |
| Bulk Top-Up | Top-up cho nhiều EA cùng lúc theo criterion của một campaign |
| Campaign | Định nghĩa một đợt bulk top-up: Academic Year, Round, criterion, số tiền, ngân sách, chế độ chạy |
| Round | Số thứ tự đợt top-up trong một Academic Year (1, 2, 3...) |
| Criterion | Một điều kiện lọc của campaign: tuổi, số dư, tình trạng đi học. Các criterion kết hợp bằng AND |
| Campaign Eligibility Date | Ngày dùng làm mốc tính tuổi và tình trạng đi học |
| Run | Một lần thực thi campaign. Campaign ad-hoc có một run; campaign định kỳ có nhiều run |
| Run Item | Kết quả xử lý của một EA trong một run |
| Preview | Danh sách tài khoản dự kiến eligible, kèm tổng số và tổng tiền, xem trước khi chạy |
| Budget Limit | Tổng số tiền tối đa một run được phép ghi có |
| Actively Enrolled | Học sinh có enrollment còn hiệu lực trong Academic Year mục tiêu |
| Successful / Skipped / Failed | Ba nhóm kết quả của Run Item: nạp thành công / bỏ qua do không đủ điều kiện / lỗi xử lý |
| Funding reference | Mã tham chiếu duy nhất của một lần ghi có, gửi sang Function 1 để chống ghi trùng và đối soát |
| Idempotency key | Khóa đảm bảo một yêu cầu chỉ được xử lý một lần dù bị gửi lại; duy nhất theo HQ User |
| Correction | Bút toán ghi nợ hiệu chỉnh dùng để sửa một top-up lẻ nạp nhầm |
| Reconciliation | Đối soát khi kết quả ghi có chưa rõ. ReconciliationRequired là trạng thái cần bộ phận vận hành xử lý |
| Ledger | Sổ ghi giao dịch EA, chỉ thêm mới, thuộc Function 1 |
| SGD | Singapore dollar |

### 1.5. Exclusions

FS này không đặc tả:

Nguồn ngân sách, phê duyệt tài chính nội bộ MOE và hạch toán kế toán.

Tạo và đóng EA, Closure Eligibility Check (R1). Function 2 chỉ gọi.

Số dư, sổ cái và việc triển khai API ghi có, ghi nợ của Function 1. FS chỉ mô tả cách Function 2 gọi các API này.

Enrollment, Academic Year, liên kết Student–EA (R3). Function 2 chỉ đọc.

Hiển thị Transaction History cho Parent (R8) và thanh toán phí bằng EA (R9). Chỉ mô tả điểm nối ở mục 2.2.

Áp trợ cấp FAS (R4).

Xác thực và phân quyền Admin Portal.

### 1.6. OOS List

| # | Hạng mục ngoài phạm vi | Lý do / nguồn | Dự kiến |
| :--- | :--- | :--- | :--- |
| 1 | Số tiền khác nhau theo từng tài khoản (theo bậc tuổi, cấp học) | Requirement chỉ nêu số tiền cố định mỗi tài khoản; muốn nhiều mức thì tạo nhiều campaign | Chưa xếp lịch |
| 2 | Criterion bổ sung (School, Academic Level, FAS tier) | Requirement ghi "etc."; mô hình criterion được thiết kế mở rộng nhưng bản này chỉ có tuổi, số dư, tình trạng đi học | Chưa xếp lịch |
| 3 | Nhập danh sách tài khoản bằng file CSV | Không có trong requirement | Chưa xếp lịch |
| 4 | Sửa từng giao dịch trong batch, hoặc hoàn tác cả một run | Feature list chỉ nêu sửa top-up thủ công (OQ-07) | Sau khi client chốt |
| 5 | Top-up cho EA Closed, chuyển số dư sang CPF | CPF Transfer chưa triển khai ở R1 | Cùng CPF Transfer |
| 6 | Phê duyệt hai bước (maker-checker) | Chưa có trong requirement (OQ-04) | Chưa xếp lịch |
| 7 | Dashboard phân tích mức dùng ngân sách nhiều campaign | Không có trong requirement; bản này chỉ có tổng kết từng run và export | Chưa xếp lịch |
| 8 | SMS và thông báo trong ứng dụng cho Parent | FS-08 đã bỏ chuông thông báo khỏi phạm vi | Chưa xếp lịch |

## 2. System Process and Function Overview

### 2.1. Process Flow Diagrams

#### Individual Top-Up Flow

HQ User tìm một EA, kiểm tra thông tin chủ tài khoản, nhập số tiền và xác nhận. Hệ thống chạy Closure Eligibility Check trước khi ghi có. Chỉ EA Active mới nhận tiền; thất bại không làm đổi số dư.

#### Bulk Top-Up Flow – Campaign Setup, Preview and Launch

HQ User cấu hình campaign, xem preview, sửa cho đến khi nằm trong ngân sách, rồi chọn chạy ngay, chạy vào một thời điểm hoặc kích hoạt chạy định kỳ. Sửa criterion, số tiền hoặc ngân sách sau khi preview thì campaign quay về Draft và phải preview lại.

#### Top-Up Correction Flow

HQ User chọn một top-up lẻ đã thành công và sửa bằng bút toán ghi nợ hiệu chỉnh: giảm số tiền hoặc rút lại hoàn toàn bộ. Bút toán gốc giữ nguyên; thất bại thì không có gì thay đổi.

### 2.2. Liên kết với các requirement khác

| Requirement | Function 2 dùng / cung cấp | Quy tắc nối |
| :--- | :--- | :--- |
| R1 – F02 (đóng EA) | Gọi: Closure Eligibility Check trước mỗi lần ghi có | EA Closed, Closure Deferred, Eligibility Review Required, hoặc Government API không phản hồi: không ghi có (F02-AC04, EF01). EA đủ 16 tuổi chưa Closed: F02 chạy closure trước, rồi top-up bị từ chối |
| R3 – Enrollment | Dùng: student_school_enrollments (enrolled_from, enrolled_to_exclusive, status) để xác định Actively Enrolled | Học sinh Actively Enrolled khi có enrollment ENROLLED còn hiệu lực tại Eligibility Date và giao với Academic Year của campaign |
| R3 – Academic Year | Dùng: academic_years (year_number, start_date, end_date_exclusive, status) | Campaign chỉ gắn với Academic Year có status DRAFT hoặc ACTIVE, không gắn với CLOSED (OQ-06) |
| R3 – F08 (liên kết Student–EA) | Dùng: liên kết giữa Student của R3 và EA | Chỉ Student SC có EA; Student PR hoặc IS không có EA nên không bao giờ eligible. Từ EA tìm Student của R3 qua liên kết này để lấy enrollment |
| R4 – FAS | Không có phụ thuộc trực tiếp | Số tiền top-up không phụ thuộc FAS. Mô hình criterion cho phép thêm criterion FAS sau này |
| R8 – Parent Portal | Cung cấp: giao dịch Top-up trong Transaction History (FR-08.2) | Top-up thành công hiện Type Top-up, Money in, Status Completed, Amount có dấu cộng. Sửa top-up hiện Type Top-up, Money out. Description chỉ ghi "MOE Top-up" hoặc tên campaign; không hiện lý do hoặc ghi chú nội bộ của HQ User. Số dư Home và Education Account tăng ngay sau khi ghi có thành công |
| R9 – thanh toán bằng EA | Dùng chung Function 1 | Số dư khả dụng dùng cho thanh toán là số dư sau top-up. Top-up (ghi có), thanh toán (ghi nợ) và sửa top-up (ghi nợ) đều đi qua sổ cái Function 1, nên được tuần tự hóa ở đó; Function 2 không khóa số dư. Sửa top-up không được làm số dư âm, nên có thể bị từ chối nếu tiền đã dùng để trả phí. Function 1 cần API ghi có và ghi nợ idempotent theo FundingReference, cùng nhu cầu với NQ-15 của R9 |

## 3. Detailed Functions and Solution Design

### 3.1.1. Function Description

Function 2 cho MOE HQ User nạp tiền vào EA theo hai cách: nạp lẻ cho một chủ tài khoản, hoặc nạp hàng loạt theo campaign. Campaign gồm Academic Year, Round, các criterion (tuổi, số dư, tình trạng đi học), số tiền cố định mỗi tài khoản và ngân sách; campaign chạy ad-hoc hoặc định kỳ. Mỗi lần ghi có đi qua Closure Eligibility Check và API ghi có của Function 1. Top-up lẻ nạp nhầm được sửa bằng bút toán ghi nợ hiệu chỉnh.

| Mục | Nội dung |
| :--- | :--- |
| Function ID | F2 (R2) |
| Portal | Admin Portal |
| Actor chính | MOE HQ User |
| Precondition | HQ User đã đăng nhập Admin Portal và có quyền Top-Up; EA đã được tạo (R1). Với bulk: Academic Year đã tồn tại (R3) |
| Postcondition (thành công) | Mỗi lần ghi có thành công có một bút toán ghi có ở Function 1, số dư EA tăng đúng một lần; có top-up transaction với Transaction Reference; có audit log. Với bulk: có run summary Successful, Skipped, Failed |
| Postcondition (thất bại) | Top-up transaction = Failed; số dư EA không đổi; lý do được ghi log. Với bulk: các tài khoản khác trong run vẫn được xử lý |
| Postcondition (đang chạy) | Run = Running; campaign không sửa được; không mở thêm run cho cùng campaign |
| Postcondition (cần xử lý tay) | Giao dịch hoặc run item = ReconciliationRequired khi không xác định được kết quả ghi có; bộ phận vận hành xử lý; hệ thống không tự đoán là đã ghi hay chưa |

#### Sub-functions:

| ID | Sub-function | Mục đích |
| :--- | :--- | :--- |
| F2.1 | Search and Verify EA Account Holder | Tìm kiếm tài khoản EA theo Account Number hoặc Student NRIC; hiển thị thông tin chủ tài khoản, trạng thái tài khoản và số dư hiện tại để xác minh trước khi nạp tiền. |
| F2.2 | Individual Top-Up | Thực hiện nạp tiền cho một tài khoản EA cụ thể; nhập số tiền, xác nhận giao dịch, kiểm tra điều kiện hợp lệ, ghi có vào EA thông qua Function 1 và hiển thị kết quả. |
| F2.3 | Top-Up History and Correction | Tra cứu lịch sử top-up và xử lý các giao dịch nạp nhầm bằng bút toán điều chỉnh ghi nợ, có kiểm tra điều kiện và lưu vết kiểm toán. |
| F2.4 | Top-Up Campaign Configuration | Tạo và cấu hình chiến dịch top-up theo Academic Year, Round, tiêu chí đối tượng thụ hưởng, số tiền nạp, ngân sách và chế độ thực thi. |
| F2.5 | Eligibility Preview and Budget Validation | Xác định danh sách tài khoản đủ điều kiện theo các tiêu chí đã cấu hình; hiển thị số lượng tài khoản, tổng số tiền dự kiến, kiểm tra giới hạn ngân sách và cho phép xem lại preview khi cấu hình thay đổi. |
| F2.6 | Top-Up Run Scheduling and Control | Thiết lập cách thức và thời điểm chạy top-up: chạy ngay, chạy một lần theo lịch hoặc chạy định kỳ; hỗ trợ tạm dừng, hủy lịch hoặc dừng chiến dịch theo các quy tắc được phép. |
| F2.7 | Top-Up Execution and Run Monitoring | Thực thi top-up theo danh sách đã xác nhận; kiểm tra lại điều kiện từng tài khoản trước khi ghi có; tổng hợp kết quả thành công/thất bại, hỗ trợ thử lại các tài khoản thất bại, xuất báo cáo và lưu audit log. |
| F2.8 | Parent Notification | Gửi thông báo cho Parent/Guardian sau khi giao dịch top-up thành công, không làm gián đoạn quá trình thực thi top-up. |

#### Business Rules:

Nhóm A – Quyền và Individual Top-Up (F2.1, F2.2)

| ID | Rule |
| :--- | :--- |
| BR-F2-01 | Chỉ MOE HQ User có quyền Top-Up. Mọi API kiểm tra quyền ở server; School User và Parent bị từ chối |
| BR-F2-02 | Tìm EA theo khớp chính xác Account Number hoặc NRIC đầy đủ của học sinh; không tìm gần đúng. Kết quả hiển thị NRIC che một phần |
| BR-F2-03 | Số tiền top-up lớn hơn 0, tối đa 2 chữ số thập phân, không vượt hạn mức mỗi lần (TBC, OQ-03). Lý do (reason) bắt buộc, tối đa 200 ký tự |
| BR-F2-04 | Chỉ EA Active nhận top-up. Trước khi ghi có, hệ thống chạy Closure Eligibility Check của F02. EA Closed, Closure Deferred, Eligibility Review Required hoặc Government API không phản hồi: từ chối, không ghi có, số dư không đổi |
| BR-F2-05 | Mỗi lần ghi có chỉ xảy ra một lần: idempotency key duy nhất theo HQ User, nút xác nhận bị vô hiệu sau khi bấm, mỗi lần ghi có có FundingReference riêng |
| BR-F2-06 | Giao dịch thất bại không làm đổi số dư nhưng vẫn được ghi log (thời điểm, người thực hiện, lý do) |

Nhóm B – Sửa top-up nhầm (F2.3)

| ID | Rule |
| :--- | :--- |
| BR-F2-08 | Chỉ top-up lẻ có Status Success mới sửa được. Top-up trong batch và giao dịch hiệu chỉnh không sửa được |
| BR-F2-09 | Có hai kiểu sửa: giảm số tiền, hoặc hoàn toàn bộ. Cả hai là một giao dịch ghi nợ mới loại Top-Up Correction, liên kết với giao dịch gốc. Giao dịch gốc không bị sửa hay xóa; hiển thị thêm Corrected amount và Effective amount (gốc trừ tổng đã sửa) |
| BR-F2-10 | Số tiền ghi nợ hiệu chỉnh lớn hơn 0, không vượt Effective amount còn lại của giao dịch gốc và không vượt số dư khả dụng của EA (không để số dư âm). Cho sửa nhiều lần đến khi Effective amount bằng 0 |
| BR-F2-11 | EA phải Active và qua Closure Eligibility Check. EA Closed: từ chối, vận hành xử lý ngoài hệ thống |
| BR-F2-12 | Lý do sửa bắt buộc. Audit log ghi giao dịch gốc, Effective amount trước và sau, người sửa, thời điểm. Thời hạn cho phép sửa và việc có cần người duyệt: TBC (OQ-04, OQ-05) |

Nhóm C – Cấu hình Campaign (F2.4)

| ID | Rule |
| :--- | :--- |
| BR-F2-13 | Mỗi campaign thuộc một Academic Year và một Round (số nguyên dương). Campaign Code duy nhất trong cặp (Academic Year, Round). Cùng một kỳ chạy được nhiều campaign với criterion và số tiền khác nhau |
| BR-F2-14 | Các criterion kết hợp bằng AND. Có ba loại: Age Range (Minimum Age, Maximum Age, bao gồm cả hai đầu), Account Balance (toán tử và ngưỡng SGD), Schooling Status (Actively Enrolled). Campaign cần ít nhất một criterion; criterion không khai báo thì không lọc |
| BR-F2-15 | Age Range: 7 ≤ Minimum Age ≤ Maximum Age ≤ 15, vì EA chỉ tồn tại từ 7 đến dưới 16 tuổi. Tuổi tính theo số năm tròn tại Campaign Eligibility Date, dùng Leap Year Rule của R1 |
| BR-F2-16 | Campaign Eligibility Date: với ad-hoc do HQ User chọn (mặc định là ngày chạy); với định kỳ là ngày của từng lần chạy |
| BR-F2-17 | Budget Limit bắt buộc, lớn hơn 0, áp dụng cho từng run (OQ-02 hỏi có cần hạn mức cộng dồn theo campaign hay theo kỳ). Hệ thống chặn ở hai chỗ: lúc xác nhận (tổng tiền preview không vượt Budget Limit) và lúc chạy (dừng ghi có khi số còn lại nhỏ hơn số tiền mỗi tài khoản) |
| BR-F2-18 | Trạng thái campaign: Draft, Scheduled, Active, Running, Completed, Ended, Cancelled (Appendix A). Chỉ sửa được khi Draft. Sửa campaign đang Scheduled hoặc Active thì quay về Draft, hủy các lần chạy chưa bắt đầu, và phải preview lại rồi xác nhận lại |

Nhóm D – Preview, lịch chạy và thực thi (F2.5, F2.6, F2.7)

| ID | Rule |
| :--- | :--- |
| BR-F2-19 | Preview hiển thị Student Name, Age, Balance, Schooling Status, Top-Up Amount dự kiến của từng tài khoản, cùng tổng số tài khoản, tổng tiền và thời điểm tính preview. Preview chỉ đọc |
| BR-F2-20 | Chỉ xác nhận được khi preview tính trên đúng phiên bản hiện tại của campaign và tổng tiền không vượt Budget Limit. Sửa criterion, số tiền hoặc ngân sách thì preview cũ mất hiệu lực |
| BR-F2-21 | Có ba cách chạy: chạy ngay; chạy vào một ngày giờ SGT trong tương lai (một lần); chạy định kỳ với tần suất MONTHLY, QUARTERLY hoặc YEARLY, ngày giờ bắt đầu và ngày kết thúc tùy chọn (lịch cụ thể: TBC, OQ-02). Mỗi lần chạy tạo một run |
| BR-F2-22 | Mỗi campaign tối đa một run đang mở. Lần chạy định kỳ đến khi run trước còn Running, hoặc scheduler bị lỡ giờ: không tự chạy bù, đánh dấu Missed, cảnh báo vận hành; HQ User có thể chạy ad-hoc nếu cần |
| BR-F2-23 | Hủy được campaign Scheduled hoặc Active và run Pending. Run đang Running cho phép Stop: hoàn tất đoạn đang xử lý, các tài khoản còn lại ghi Skipped (RUN_STOPPED), các khoản đã ghi có giữ nguyên |
| BR-F2-24 | Khi chạy, hệ thống xử lý từng tài khoản theo thứ tự Account Number tăng dần, theo từng đoạn nhỏ: Closure Eligibility Check, EA còn Active, đánh giá lại criterion bằng dữ liệu tại thời điểm đó, kiểm tra ngân sách còn lại, ghi có. |
| BR-F2-25 | Trong một run, mỗi tài khoản được ghi có tối đa một lần (duy nhất theo RunId và EA). Giữa các campaign khác nhau, một tài khoản có thể nhận nhiều khoản; preview cảnh báo nếu tài khoản đã nhận top-up từ campaign khác cùng kỳ |
| BR-F2-26 | Kết quả từng tài khoản: Successful; Skipped kèm Skip Reason (EA_NOT_ACTIVE, ELIGIBILITY_REVIEW_REQUIRED, AGE_NOT_MATCH, BALANCE_NOT_MATCH, NOT_ENROLLED, BUDGET_EXHAUSTED, RUN_STOPPED); Failed kèm Failure Code (ví dụ ELIGIBILITY_CHECK_UNAVAILABLE, CREDIT_FAILED). ReconciliationRequired tính trong nhóm Failed và có cờ riêng |
| BR-F2-27 | Mỗi run item có FundingReference cố định, sinh một lần. Thử lại dùng đúng FundingReference đó, nên Function 1 không ghi trùng |
| BR-F2-28 | Thử lại: HQ User thử lại các run item Failed (không gồm ReconciliationRequired và Skipped). Thử lại vẫn đi qua mọi kiểm tra và vẫn bị giới hạn bởi ngân sách còn lại |
| BR-F2-29 | Run summary hiển thị tổng Successful, Skipped, Failed (số tài khoản và số tiền), số ReconciliationRequired, ngân sách đã dùng và còn lại; lọc theo kết quả; export CSV. Trạng thái run: Completed khi không có Failed, CompletedWithErrors khi còn Failed |
| BR-F2-30 | Audit lưu vĩnh viễn: Transaction Reference, số tiền, thời điểm, người thực hiện (HQ User, hoặc "System" kèm HQ User đã kích hoạt campaign), campaign, run. Không xóa cứng campaign, run, run item và giao dịch |

Nhóm E – Thông báo (F2.8)

| ID | Rule |
| :--- | :--- |
| BR-F2-31 | Sau mỗi top-up thành công, hệ thống đưa sự kiện vào hàng đợi để gửi cho các Parent liên kết qua Father NRIC hoặc Mother NRIC và đã có email trong Parent_Profile. Nội dung gồm số tiền, ngày và số EA che một phần; không gồm lý do hay ghi chú nội bộ |
| BR-F2-32 | Gửi thông báo lỗi hoặc Parent chưa có hồ sơ thì không ảnh hưởng top-up. |

### 3.1.2. Process Flow Description and Screens

#### Bước 1. Tìm EA và xác minh chủ tài khoản (F2.1)

HQ User vào menu Top-Up, chọn Individual Top-Up (SCR-01).

HQ User nhập Account Number hoặc NRIC đầy đủ của học sinh và chọn Search.

Hệ thống tìm EA theo khớp chính xác (BR-F2-02) và hiển thị SCR-02: tên học sinh, NRIC che một phần, tuổi, Account Number, Account Status, Current Balance.

Luồng thay thế: không tìm thấy thì báo MSG-0201; EA không Active vẫn hiển thị để tra cứu nhưng không cho nhập số tiền, kèm lý do (MSG-0204).

#### Bước 2. Nhập số tiền và xác nhận (F2.2)

Trên SCR-02, HQ User nhập Top-Up Amount và Reason rồi chọn Continue.

Hệ thống kiểm tra định dạng và hạn mức (BR-F2-03), rồi hiển thị SCR-03 để xem lại: chủ tài khoản, Account Number, số dư hiện tại, số tiền, số dư sau top-up (tham khảo), lý do.

HQ User xác nhận. Nút xác nhận bị vô hiệu ngay sau lần bấm đầu; client gửi kèm idempotency key.

#### Bước 3. Kiểm tra và ghi có (F2.2)

Hệ thống tạo top-up transaction (Pending) với Transaction Reference và FundingReference, rồi chạy Closure Eligibility Check của F02.

Không đủ điều kiện (EA Closed, Closure Deferred, Eligibility Review Required, Government API không phản hồi): transaction Failed, số dư không đổi, hiển thị SCR-04 với thông báo tương ứng.

Đủ điều kiện: gọi Function 1 ghi có (nguyên tử, idempotent theo FundingReference).

Thành công: transaction Success, lưu mã bút toán của Function 1, ghi audit log, đưa sự kiện vào hàng đợi email (F2.8), hiển thị SCR-04 kèm Transaction Reference và số dư mới (MSG-0207).

Thất bại: transaction Failed, số dư không đổi (MSG-0208).

Không rõ kết quả: hỏi lại Function 1 bằng cùng FundingReference; vẫn không rõ thì ReconciliationRequired, hiển thị trạng thái đang xác minh (MSG-0209).

#### Bước 4. Xem Top-Up History và sửa top-up nhầm (F2.3)

HQ User mở Top-Up History (SCR-05): danh sách mọi top-up (lẻ và từ batch) theo thời gian mới nhất trước, lọc theo Account Number, NRIC, khoảng ngày, nguồn (Individual, Bulk), trạng thái.

HQ User chọn một top-up lẻ Success và chọn Correct. Hệ thống mở SCR-06: giao dịch gốc, Effective amount còn lại, kiểu sửa (Reduce amount hoặc Reverse in full), số tiền ghi nợ, Reason.

Hệ thống kiểm tra (BR-F2-08 đến BR-F2-12), chạy Closure Eligibility Check rồi gọi Function 1 ghi nợ hiệu chỉnh (idempotent theo FundingReference).

Thành công: tạo giao dịch Top-Up Correction, giao dịch gốc hiện Corrected amount và Effective amount mới (MSG-0210).

Số dư không đủ hoặc lỗi: không có gì thay đổi (MSG-0211, MSG-0208).

#### Bước 5. Tạo và cấu hình Campaign (F2.4)

HQ User vào Top-Up, chọn Bulk Top-Up Campaigns (SCR-07), chọn Create.

Trên SCR-08, HQ User nhập Campaign Name, chọn Academic Year và Round, thêm criterion (Age Range, Account Balance, Schooling Status), nhập Top-Up Amount và Budget Limit, rồi Save. Eligibility Date cho ad-hoc chọn ở bước 7.

Hệ thống kiểm tra theo BR-F2-13 đến BR-F2-20 và lưu campaign ở trạng thái Draft.

#### Bước 6. Preview và xác nhận (F2.5)

HQ User chọn Preview. Hệ thống đánh giá criterion trên các EA Active và hiển thị SCR-09: danh sách eligible (Student Name, Age, Balance, Schooling Status, Top-Up Amount), tổng số tài khoản, tổng tiền, Budget Limit, thời điểm tính preview, cảnh báo tài khoản đã nhận top-up từ campaign khác cùng kỳ.

Tổng tiền vượt Budget Limit: nút Confirm bị vô hiệu, hiển thị số tiền vượt (MSG-0213). HQ User sửa campaign (quay về Draft) rồi preview lại.

Không có tài khoản eligible: hiển thị MSG-0214, không xác nhận được.

Đạt điều kiện: HQ User chọn Confirm và sang bước 7.

#### Bước 7. Chọn chế độ chạy (F2.6)

Trên SCR-10, HQ User chọn một trong ba cách: Run now, Run at date and time (một lần, giờ SGT, trong tương lai), hoặc Recurring (tần suất, ngày giờ bắt đầu, ngày kết thúc tùy chọn).

Với ad-hoc, HQ User chọn Eligibility Date (mặc định là ngày chạy); với định kỳ, mỗi lần chạy dùng ngày chạy làm Eligibility Date.

Hệ thống đổi campaign sang Running (chạy ngay), Scheduled (chạy một lần vào giờ đã chọn) hoặc Active (định kỳ), và ghi audit log người xác nhận.

HQ User có thể Cancel campaign Scheduled hoặc Active, hoặc Stop run đang Running ở SCR-11.

#### Bước 8. Thực thi run và nhận kết quả (F2.7)

Đến giờ (hoặc ngay lập tức), hệ thống tạo run (Pending, rồi Running), khóa campaign, cố định Eligibility Date và criterion cho run này.

Hệ thống xử lý từng tài khoản theo BR-F2-27: kiểm tra, ghi có qua Function 1 với FundingReference của run item, ghi kết quả Successful, Skipped hoặc Failed.

HQ User theo dõi tiến độ ở SCR-11 và SCR-12 (số đã xử lý, ngân sách đã dùng).

Hết danh sách: run = Completed (không có Failed) hoặc CompletedWithErrors (còn Failed); hiển thị run summary (BR-F2-32). Với campaign ad-hoc, campaign = Completed; với định kỳ, campaign về Active chờ lần chạy kế tiếp.

#### Bước 9. Thử lại, export và thông báo (F2.7, F2.8)

Trên SCR-12, HQ User lọc run item theo kết quả, export CSV, và chọn Retry failed để thử lại các run item Failed (BR-F2-31).

Mỗi top-up thành công đưa một sự kiện vào hàng đợi email; Parent thấy giao dịch trong Transaction History của R8 ngay sau khi ghi có.

#### Trường hợp ngoại lệ:

| # | Tình huống | Xử lý |
| :--- | :--- | :--- |
| EX-01 | School User hoặc Parent gọi API Top-Up, hoặc HQ User sửa ID trong request để thao tác trên campaign hay giao dịch không thuộc quyền | Server kiểm tra quyền cho mọi request, trả 403, không lộ dữ liệu, ghi log bảo mật (MSG-0003) |
| EX-02 | EA chuyển sang Closed, hoặc học sinh đủ 16 tuổi, giữa lúc HQ User xem và lúc xác nhận | Closure Eligibility Check chạy khi xác nhận; F02 đóng EA nếu cần; top-up bị từ chối, số dư không đổi (MSG-0204) |
| EX-03 | Government API không phản hồi khi kiểm tra đóng EA | Không ghi có; individual: hiển thị lỗi, cho thử lại; bulk: run item Failed (ELIGIBILITY_CHECK_UNAVAILABLE), có thể thử lại. Không tự đổi Account Status |
| EX-04 | Bấm xác nhận hai lần, hoặc client gửi lại cùng idempotency key | Chỉ tạo một transaction và ghi có một lần; lần gửi lại nhận kết quả của transaction đầu |
| EX-05 | Function 1 timeout hoặc lỗi mạng sau khi gửi lệnh ghi có | Giữ Pending, hỏi lại Function 1 bằng cùng FundingReference; nếu đã ghi thì đánh Success, nếu chưa thì cho Failed; vẫn không xác định thì ReconciliationRequired, cảnh báo vận hành. Không tự thử vô hạn |
| EX-06 | Session Admin Portal hết hạn khi đang thao tác | Hết hạn trước khi xác nhận: yêu cầu đăng nhập lại, chưa có transaction. Hết hạn sau khi xác nhận: transaction vẫn được xử lý; HQ User đăng nhập lại thấy trạng thái hiện tại (MSG-0002) |
| EX-07 | HQ User sửa criterion, số tiền hoặc ngân sách sau khi đã preview hoặc đã Confirm | Campaign về Draft; các lần chạy chưa bắt đầu bị hủy; phải preview và xác nhận lại (BR-F2-21, BR-F2-23) |
| EX-08 | Hai HQ User sửa hoặc hủy cùng một campaign đồng thời; hoặc sửa campaign đang Running | Dùng row version để phát hiện xung đột, người sau nhận yêu cầu làm mới. Campaign đang Running không sửa được (MSG-0215) |
| EX-09 | Giữa preview và lúc chạy, một tài khoản đổi số dư, bị đóng, hoặc học sinh không còn học | Đánh giá lại khi chạy: tài khoản không còn đủ điều kiện bị Skipped với Skip Reason tương ứng; danh sách thực tế có thể khác preview |
| EX-10 | Ngân sách hết giữa chừng | Các tài khoản còn lại Skipped (BUDGET_EXHAUSTED), run vẫn hoàn tất với số liệu đã dùng |
| EX-11 | Job bị dừng đột ngột hoặc server khởi động lại giữa run | Run tiếp tục từ các run item chưa xử lý. Item đã gửi lệnh sang Function 1 mà chưa ghi kết quả được hỏi lại bằng FundingReference; không ghi có hai lần |
| EX-12 | Lần chạy định kỳ đến khi run trước còn Running, hoặc scheduler bị lỡ giờ | Không chạy bù tự động; đánh dấu Missed, cảnh báo vận hành (BR-F2-25) |
| EX-13 | Academic Year của campaign chuyển sang CLOSED hoặc quá ngày kết thúc của campaign định kỳ | Campaign chuyển Ended, không tạo run mới, cảnh báo HQ User |
| EX-14 | Sửa top-up khi số dư EA nhỏ hơn số tiền cần ghi nợ (tiền đã dùng trả phí) | Từ chối, không đổi dữ liệu (MSG-0211); xử lý tiếp do vận hành, ngoài phạm vi (OQ-05) |
| EX-15 | Sửa top-up khi EA đã Closed, hoặc giao dịch đã sửa hết | Từ chối (MSG-0212) |
| EX-16 | Gửi email thất bại, hoặc Parent chưa đăng nhập lần nào nên chưa có email | Bỏ qua hoặc thử lại theo hàng đợi; không ảnh hưởng top-up, ghi log |

## 4. Data Fields Table

### 4.1. Trường hiển thị và nhập trên màn hình

| Màn hình | Trường | Kiểu | Nguồn | Nhập | Bắt buộc | Quy tắc / ghi chú |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| SCR-01 | Search by | Enum ACCOUNT_NUMBER, NRIC | HQ User chọn | Có | Có | Khớp chính xác, không tìm gần đúng |
| SCR-01 | Search value | Text | HQ User nhập | Có | Có | Account Number hoặc NRIC đầy đủ (9 ký tự) |
| SCR-02 | Student name | Text | Student Profile (R1) | Không | Có |  |
| SCR-02 | NRIC | Text | Student Profile (R1) | Không | Có | Che một phần, không đưa NRIC đầy đủ vào URL |
| SCR-02 | Age | Integer | Tính từ DOB | Không | Có | Số năm tròn tại ngày hiện tại |
| SCR-02 | Account Number | Text | Function 1 | Không | Có |  |
| SCR-02 | Account Status | Enum Active, Closed | Function 1 | Không | Có | Chỉ Active mới nhập được số tiền |
| SCR-02 | Current Balance | Decimal(18,2), SGD | Function 1 | Không | Có |  |
| SCR-02 | Top-Up Amount | Decimal(18,2), SGD | HQ User nhập | Có | Có | Lớn hơn 0; tối đa 2 chữ số thập phân; không vượt hạn mức mỗi lần (TBC) |
| SCR-02 | Reason | Text, tối đa 200 ký tự | HQ User nhập | Có | Có | Chỉ dùng nội bộ, không hiển thị cho Parent |
| SCR-03 | Balance after top-up | Decimal(18,2) | Tính | Không | Không | Chỉ để tham khảo |
| SCR-03 | Idempotency key | Text, tối đa 100 ký tự | Client sinh | Không | Có | Duy nhất theo HQ User; bấm đúp giữ cùng key; thao tác mới dùng key mới |
| SCR-04 | Transaction Reference | Text, tối đa 50 ký tự | Hệ thống sinh | Không | Có | Duy nhất; định dạng đề xuất TUP-YYYYMMDD-XXXXXX (TBC) |
| SCR-04 | Transaction Status | Enum Success, Failed, ReconciliationRequired | Transaction | Không | Có | ReconciliationRequired hiển thị là đang xác minh |
| SCR-04 | New balance | Decimal(18,2) | Function 1 | Không | Không | Chỉ khi Success |
| SCR-05 | Filter: Account Number, NRIC | Text | HQ User nhập | Có | Không |  |
| SCR-05 | Filter: From, To | Date | HQ User chọn | Có | Không | DD/MM/YYYY, SGT |
| SCR-05 | Filter: Source | Enum All, Individual, Bulk, Correction | HQ User chọn | Có | Không |  |
| SCR-05 | Filter: Status | Enum All, Success, Failed, ReconciliationRequired | HQ User chọn | Có | Không |  |
| SCR-05 | Cột bảng | Date, Transaction Reference, Student, Account Number, Source, Campaign (nếu bulk), Amount, Corrected amount, Effective amount, Status, Performed by | Transaction | Không | Có | Mới nhất trước, 20 dòng mỗi trang; nút Correct chỉ hiện ở top-up lẻ Success còn Effective amount lớn hơn 0 |
| SCR-06 | Correction type | Enum REDUCE, REVERSE_FULL | HQ User chọn | Có | Có |  |
| SCR-06 | Debit amount | Decimal(18,2) | HQ User nhập; tự điền khi REVERSE_FULL | Có | Có khi REDUCE | Lớn hơn 0; không vượt Effective amount còn lại và số dư khả dụng |
| SCR-06 | Reason | Text, tối đa 200 ký tự | HQ User nhập | Có | Có |  |
| SCR-07 | Cột danh sách | Campaign Code, Name, Academic Year, Round, Amount, Budget Limit, Run mode, Status, Next run | Campaign | Không | Có | Lọc theo Academic Year, Round, Status |
| SCR-08 | Campaign Name | Text, tối đa 150 ký tự | HQ User nhập | Có | Có |  |
| SCR-08 | Academic Year | Dropdown | academic_years (R3) | Có | Có | Chỉ DRAFT hoặc ACTIVE |
| SCR-08 | Round | Integer | HQ User nhập | Có | Có | Dương; Code duy nhất trong (Academic Year, Round) |
| SCR-08 | Age Range: Minimum, Maximum Age | Integer | HQ User nhập | Có | Không | 7 ≤ Min ≤ Max ≤ 15; nhập cả hai hoặc không nhập |
| SCR-08 | Account Balance: operator, threshold | Enum, Decimal(18,2) | HQ User chọn, nhập | Có | Không | Toán tử <, <=, >, >=, =; ngưỡng không âm; nhập cả hai hoặc không |
| SCR-08 | Schooling Status: Actively Enrolled | Checkbox | HQ User chọn | Có | Không | Bật thì chỉ lấy học sinh Actively Enrolled trong Academic Year |
| SCR-08 | Top-Up Amount per account | Decimal(18,2), SGD | HQ User nhập | Có | Có | Lớn hơn 0; không vượt hạn mức mỗi lần (TBC) |
| SCR-08 | Budget Limit | Decimal(18,2), SGD | HQ User nhập | Có | Có | Lớn hơn 0; áp dụng cho từng run |
| SCR-09 | Cột preview | Student Name, Age, Balance, Schooling Status, Top-Up Amount | Tính | Không | Có | 20 dòng mỗi trang |
| SCR-09 | Total accounts, Total amount, Budget Limit, Remaining budget, Previewed at | Integer, Decimal, Datetime | Tính | Không | Có | Total amount vượt Budget Limit thì vô hiệu nút Confirm |
| SCR-10 | Run mode | Enum RUN_NOW, SCHEDULED, RECURRING | HQ User chọn | Có | Có |  |
| SCR-10 | Eligibility Date | Date | HQ User chọn | Có | Có khi ad-hoc | Mặc định ngày chạy; với RECURRING hệ thống tự gán |
| SCR-10 | Scheduled at | Datetime SGT | HQ User chọn | Có | Có khi SCHEDULED | Trong tương lai |
| SCR-10 | Frequency, Start at, End at | Enum, Datetime, Datetime | HQ User chọn | Có | Frequency và Start at bắt buộc khi RECURRING | Frequency: MONTHLY, QUARTERLY, YEARLY (TBC); End at sau Start at |
| SCR-11 | Cột danh sách run | Run No, Trigger, Eligibility Date, Status, Total, Successful, Skipped, Failed, Total credited, Started at, Completed at | Run | Không | Có |  |
| SCR-12 | Cột run item | Student, Account Number, Age, Balance, Schooling Status, Amount, Outcome, Skip Reason hoặc Failure Reason, Transaction Reference | Run item | Không | Có | Lọc theo Outcome; nút Export CSV, Retry failed |

### 4.2. Thực thể dữ liệu liên quan

#### Campaign (topup_campaigns)

Id: VARCHAR(50) - PK

Code: NVARCHAR(50) - Duy nhất trong (AcademicYearId, RoundNo)

Name: NVARCHAR(150)

AcademicYearId: UNIQUEIDENTIFIER - FK logic tới academic_years (R3); RoundNo: SMALLINT - Dương

AmountPerAccount, BudgetLimit, CurrencyCode: DECIMAL(18,2), DECIMAL(18,2), CHAR(3) - Cả hai số tiền lớn hơn 0; mặc định SGD

RunMode: INT - 1 RunNow, 2 Scheduled, 3 Recurring

EligibilityDate: DATE - Bắt buộc khi ad-hoc; rỗng khi Recurring

ScheduledAt: DATETIME2(3) - UTC; bắt buộc khi Scheduled

RecurrenceFrequency, RecurrenceStartAt, RecurrenceEndAt, NextRunAt: INT, DATETIME2(3) - Bắt buộc khi Recurring (End at tùy chọn); UTC

Status: INT - 1 Draft, 2 Scheduled, 3 Active, 4 Running, 5 Completed, 6 Ended, 7 Cancelled

DefinitionVersion, PreviewedVersion, PreviewedAt: INT, INT, DATETIME2(3) - DefinitionVersion tăng mỗi lần sửa; chỉ Confirm được khi PreviewedVersion bằng DefinitionVersion

ConfirmedBy, ConfirmedAt: VARCHAR(50), DATETIME2(3) - IAM ID của HQ User xác nhận

CreatedBy, CreatedAt, UpdatedAt, RowVersion: VARCHAR(50), DATETIME2(3), ROWVERSION - UTC; RowVersion là token kiểm soát đồng thời lạc quan

#### Criterion (topup_campaign_criteria)

Id, CampaignId: VARCHAR(50) - PK, FK Campaign

CriterionType: INT - 1 AGE_RANGE, 2 BALANCE, 3 SCHOOLING_STATUS; duy nhất theo (CampaignId, CriterionType). Thêm loại mới không đổi cấu trúc bảng

MinAge, MaxAge: SMALLINT - Bắt buộc khi AGE_RANGE, cấm ở loại khác; 7 ≤ MinAge ≤ MaxAge ≤ 15

BalanceOperator, BalanceThreshold: INT, DECIMAL(18,2) - Bắt buộc khi BALANCE; 1 LT, 2 LTE, 3 GT, 4 GTE, 5 EQ; ngưỡng không âm

RequireActivelyEnrolled: BIT - Bắt buộc khi SCHOOLING_STATUS

#### Run (topup_campaign_runs)

Id, CampaignId: VARCHAR(50) - PK, FK Campaign

RunNo: INT - Dương, duy nhất trong campaign

TriggerType: INT - 1 Manual, 2 Scheduled, 3 Recurring

TriggeredBy: VARCHAR(50) - IAM ID của HQ User đã xác nhận campaign

EligibilityDate: DATE - Cố định tại lúc bắt đầu run

DefinitionVersion, AmountPerAccount, BudgetLimit: INT, DECIMAL(18,2) - Snapshot tại lúc bắt đầu; sửa campaign không đổi run đã tạo

Status: INT - 1 Pending, 2 Running, 3 Completed, 4 CompletedWithErrors, 5 Cancelled, 6 Stopped, 7 Missed

TotalAccounts, SuccessfulCount, SkippedCount, FailedCount, ReconciliationCount: INT - Không âm; ReconciliationCount là một phần của FailedCount

TotalCredited: DECIMAL(18,2) - Tổng các khoản Successful; không vượt BudgetLimit

StartedAt, CompletedAt, CreatedAt, UpdatedAt, RowVersion: DATETIME2(3), ROWVERSION - UTC. Index duy nhất trên CampaignId khi Status là Pending hoặc Running (một run mở)

#### Run Item (topup_run_items)

Id, RunId: VARCHAR(50) - PK, FK Run; duy nhất theo (RunId, EducationAccountId)

EducationAccountId: UNIQUEIDENTIFIER - FK logic tới EA (Function 1)

AccountNumber, StudentProfileId: VARCHAR(50), UNIQUEIDENTIFIER - Tham chiếu hiển thị; NRIC lấy qua Student Profile, không sao chép

AgeAtEligibility, BalanceSnapshot, SchoolingStatusSnapshot, ExpectedAmount: SMALLINT, DECIMAL(18,2), INT, DECIMAL(18,2) - Giá trị lúc lập danh sách và lúc đánh giá; dùng để hiển thị và audit

Outcome: INT - 1 Pending, 2 Successful, 3 Skipped, 4 Failed, 5 ReconciliationRequired

SkipReason: VARCHAR(40) - Bắt buộc khi Skipped

FailureCode, FailureReason: VARCHAR(50), NVARCHAR(500) - Mã lỗi kỹ thuật và nguyên nhân đã làm sạch

FundingReference: NVARCHAR(50) - Duy nhất; sinh một lần, dùng lại khi thử lại

TopUpTransactionId: VARCHAR(50) - FK Transaction; bắt buộc khi Successful

ProcessedAt, RowVersion: DATETIME2(3), ROWVERSION - UTC

#### Top-Up Transaction (topup_transactions)

Id: VARCHAR(50) - PK

TransactionReference: NVARCHAR(50) - Duy nhất

SourceType: INT - 1 Individual, 2 Bulk, 3 Correction

Direction: INT - 1 In (ghi có), 2 Out (ghi nợ hiệu chỉnh)

EducationAccountId: UNIQUEIDENTIFIER - FK logic tới EA (Function 1)

RunItemId: VARCHAR(50) - FK Run Item; bắt buộc khi Bulk, cấm ở loại khác

OriginalTransactionId: VARCHAR(50) - FK Transaction gốc; bắt buộc khi Correction, trỏ tới giao dịch Individual Success

InitiatedByUserId: VARCHAR(50) - IAM ID của HQ User; với Bulk là HQ User đã xác nhận campaign

IdempotencyKey: VARCHAR(100) - Duy nhất theo (InitiatedByUserId, IdempotencyKey); dùng cho Individual và Correction

FundingReference: NVARCHAR(50) - Duy nhất; gửi sang Function 1 để đối soát

Amount, CurrencyCode: DECIMAL(18,2), CHAR(3) - Lớn hơn 0; SGD

CorrectionType: INT - 1 Reduce, 2 ReverseFull; bắt buộc khi Correction

Reason: NVARCHAR(200) - Bắt buộc khi Individual và Correction; không hiển thị cho Parent

Status: INT - 1 Pending, 2 Success, 3 Failed, 4 ReconciliationRequired

FailureCode, FailureReason: VARCHAR(50), NVARCHAR(500) - Đã làm sạch

EducationAccountTransactionId: BIGINT - ID logic sổ cái Function 1; bắt buộc khi Success; duy nhất

CreatedAt, UpdatedAt, CompletedAt, RowVersion: DATETIME2(3), ROWVERSION - UTC; CompletedAt rỗng khi đang xử lý

Giá trị dẫn xuất (không lưu): Effective amount của giao dịch Individual = Amount trừ tổng Amount của các Correction Success liên kết

#### Tham chiếu ngoài & Audit Log

Function 1: EA, sổ cái, API ghi có và ghi nợ hiệu chỉnh, Closure Eligibility Check (Function 2 chỉ lưu ID logic: EducationAccountId, EducationAccountTransactionId).

R1: Student Profile (họ tên, NRIC, DOB, Citizenship, Father NRIC, Mother NRIC).

R3: academic_years, student_school_enrollments, liên kết Student–EA.

R8: Parent_Profile (Email) cho thông báo email.

AuditLog: actor, action, entity, entity_id, old_value, new_value, timestamp. Ghi: tạo, sửa, xác nhận, hủy campaign; bắt đầu, dừng, kết thúc run; mỗi top-up; mỗi hiệu chỉnh. Chủ sở hữu dịch vụ chung hay bảng riêng chờ Dev xác nhận.

## 5. Validation

### 5.1. Thông báo lỗi hiển thị cho HQ User

| Mã | Nội dung hiển thị | Hành vi UI |
| :--- | :--- | :--- |
| MSG-0201 | No Education Account found. Check the Account Number or NRIC and try again. | Giữ ở SCR-01 |
| MSG-0202 | Enter an amount greater than 0, with up to 2 decimal places. | Giữ ở SCR-02, đánh dấu ô nhập |
| MSG-0203 | The amount is more than the limit for one top-up. (TBC, OQ-03) | Giữ ở SCR-02 hoặc SCR-08 |
| MSG-0204 | This Education Account is not active. Top-up is not allowed. | Vô hiệu ô nhập số tiền |
| MSG-0205 | We could not check the account status. No amount was credited. Please try again later. | SCR-04, cho thử lại; không đổi dữ liệu |
| MSG-0206 | Enter a reason (up to 200 characters). | Giữ ở SCR-02 hoặc SCR-06 |
| MSG-0207 | Top-up completed. Reference: {Transaction Reference}. | SCR-04, hiện số dư mới |
| MSG-0208 | The top-up could not be completed. No amount was credited. | SCR-04, cho thử lại |
| MSG-0209 | We are verifying this top-up. Please check the history later. | SCR-04, trạng thái đang xác minh |
| MSG-0210 | The correction has been completed. | Về SCR-05, hiện Effective amount mới |
| MSG-0211 | The Education Account balance is not enough to correct this top-up. Nothing was changed. | Giữ ở SCR-06 |
| MSG-0212 | This top-up cannot be corrected. | Ẩn hoặc vô hiệu nút Correct |
| MSG-0213 | The total amount is more than the budget limit by SGD {amount}. Change the campaign and preview again. | SCR-09, vô hiệu nút Confirm |
| MSG-0214 | No accounts match these criteria. | SCR-09, vô hiệu nút Confirm |
| MSG-0215 | This campaign is running and cannot be changed. | Mọi nút sửa bị vô hiệu |
| MSG-0216 | The campaign has changed. Preview again before confirming. | Quay về SCR-09, bắt buộc preview lại |
| MSG-0217 | Enter an age range from 7 to 15, with the minimum not more than the maximum. | SCR-08, đánh dấu ô nhập |
| MSG-0218 | Enter a balance operator and an amount of 0 or more. | SCR-08, đánh dấu ô nhập |
| MSG-0219 | Choose a date and time in the future. | SCR-10, đánh dấu ô nhập |
| MSG-0220 | This Academic Year is closed. Choose another Academic Year. | SCR-08 |
| MSG-0221 | Add at least one criterion. | SCR-08 |
| MSG-0222 | This campaign was changed by another user. Refresh and try again. | Làm mới dữ liệu |
| MSG-0001 | Enter your <field> | Bỏ trống trường bắt buộc, báo theo từng trường |
| MSG-0002 | Your session has expired. Please log in again. | Chuyển đến đăng nhập Admin Portal |
| MSG-0003 | You do not have permission to perform this action. | Quay về màn hình chính |

### 5.2. Tiêu chí chấp nhận (AC)

Individual Top-Up

| ID | Given / When / Then |
| :--- | :--- |
| AC-01 | Given HQ User, when tìm theo Account Number hoặc NRIC đầy đủ, then thấy đúng một EA với holder, status, balance; NRIC hiển thị che một phần |
| AC-02 | Given Account Number hoặc NRIC không có EA, when tìm, then báo MSG-0201 |
| AC-03 | Given EA Active, when HQ User xác nhận top-up 50.00, then số dư tăng đúng 50.00 một lần, transaction Success, có mã bút toán của Function 1, Transaction Reference và audit log |
| AC-04 | Given EA Closed, when xác nhận top-up, then bị từ chối, số dư không đổi, transaction Failed được ghi log |
| AC-05 | Given học sinh vừa đủ 16 tuổi và EA chưa Closed, when xác nhận top-up, then F02 đóng EA trước, top-up bị từ chối, số dư không đổi |
| AC-06 | Given Government API không phản hồi, when xác nhận top-up, then không ghi có, Account Status không tự đổi, báo MSG-0205 |
| AC-07 | Given HQ User bấm xác nhận hai lần, then chỉ tạo một transaction và chỉ ghi có một lần |
| AC-08 | Given Function 1 timeout sau khi nhận lệnh ghi có, when hỏi lại bằng FundingReference, then đã ghi thì Success đúng một lần; không xác định được thì ReconciliationRequired, và số dư không bị ghi có lần hai |
| AC-09 | Given số tiền bằng 0, âm, hoặc có hơn 2 chữ số thập phân, then bị từ chối MSG-0202, không có dữ liệu nào đổi |
| AC-10 | Given top-up thất bại, then số dư không đổi và lý do được ghi log |
| AC-11 | Given School User hoặc Parent gọi API Top-Up, then bị từ chối 403 và ghi log bảo mật |

Sửa top-up nhầm

| ID | Given / When / Then |
| :--- | :--- |
| AC-12 | Given top-up lẻ Success 100.00, EA Active, số dư 130.00, when HQ User chọn Reduce 40.00 kèm lý do, then số dư thành 90.00, có giao dịch Top-Up Correction, giao dịch gốc không đổi và hiện Corrected 40.00, Effective 60.00 |
| AC-13 | Given top-up lẻ Success 100.00, when Reverse in full, then Effective amount bằng 0 và không sửa tiếp được |
| AC-14 | Given số dư EA nhỏ hơn số tiền cần ghi nợ, when sửa, then bị từ chối MSG-0211, số dư không âm, không đổi dữ liệu |
| AC-15 | Given top-up thuộc batch, hoặc giao dịch Top-Up Correction, then không có nút Correct |
| AC-16 | Given EA Closed, when sửa, then bị từ chối |
| AC-17 | Given sửa không có lý do, then bị từ chối MSG-0206 |

Cấu hình Campaign, Preview

| ID | Given / When / Then |
| :--- | :--- |
| AC-18 | Given Academic Year, Round, ít nhất một criterion, số tiền và ngân sách hợp lệ, when Save, then campaign được tạo ở trạng thái Draft với Code do hệ thống sinh |
| AC-19 | Given Minimum Age lớn hơn Maximum Age, hoặc nằm ngoài 7 đến 15, then bị từ chối MSG-0217 |
| AC-20 | Given criterion tuổi 7 đến 12, số dư dưới SGD 100, Actively Enrolled, when Preview, then danh sách chỉ gồm EA Active thỏa cả ba criterion (AND), kèm Student Name, Age, Balance, Schooling Status, Top-Up Amount; tổng số tài khoản và tổng tiền đúng |
| AC-21 | Given học sinh có enrollment đã kết thúc trước Eligibility Date, hoặc là PR hoặc IS không có EA, then không xuất hiện trong preview |
| AC-22 | Given tổng tiền preview vượt Budget Limit, then nút Confirm bị vô hiệu và báo MSG-0213 |
| AC-23 | Given đã preview, when HQ User sửa criterion, số tiền hoặc ngân sách, then campaign về Draft và phải preview lại mới Confirm được |
| AC-24 | Given hai campaign cùng Academic Year và Round với criterion khác nhau, then cả hai chạy được; tài khoản thuộc cả hai nhận hai khoản và preview cảnh báo |

Chạy và kết quả

| ID | Given / When / Then |
| :--- | :--- |
| AC-25 | Given campaign đã Confirm, when Run now, then mỗi tài khoản eligible được ghi có đúng một lần; run summary có Successful, Skipped, Failed; số tiền tổng khớp tổng các giao dịch Success |
| AC-26 | Given giữa preview và lúc chạy một tài khoản có số dư tăng vượt ngưỡng, then bị Skipped (BALANCE_NOT_MATCH), không ghi có |
| AC-27 | Given tài khoản bị đóng hoặc học sinh không còn học trước lúc chạy, then Skipped (EA_NOT_ACTIVE hoặc NOT_ENROLLED) |
| AC-28 | Given Budget Limit 250.00, số tiền mỗi tài khoản 100.00, 5 tài khoản eligible, then 2 tài khoản Successful, 3 tài khoản Skipped (BUDGET_EXHAUSTED), tổng ghi có 200.00 |
| AC-29 | Given Government API lỗi với một số tài khoản, then các tài khoản đó Failed (ELIGIBILITY_CHECK_UNAVAILABLE), run vẫn xử lý các tài khoản khác, trạng thái CompletedWithErrors |
| AC-30 | Given có run item Failed, when Retry failed, then chỉ các item Failed được thử lại với cùng FundingReference và mỗi tài khoản ghi có tối đa một lần |
| AC-31 | Given server khởi động lại giữa run, then run tiếp tục từ các item chưa xử lý, không ghi có trùng |
| AC-32 | Given run Running, when HQ User Stop, then các tài khoản còn lại Skipped (RUN_STOPPED), các khoản đã ghi có giữ nguyên |
| AC-33 | Given Failed hoặc Skipped, then số dư EA tương ứng không đổi |
| AC-34 | Given campaign Running, when HQ User sửa hoặc hai HQ User thao tác đồng thời, then bị từ chối MSG-0215 hoặc MSG-0222 |

Lịch chạy

| ID | Given / When / Then |
| :--- | :--- |
| AC-35 | Given Run at date and time trong tương lai, then campaign Scheduled và tự chạy đúng giờ SGT; thời điểm trong quá khứ bị từ chối MSG-0219 |
| AC-36 | Given campaign định kỳ MONTHLY, then mỗi tháng tạo một run mới với Eligibility Date là ngày chạy, đánh giá bằng dữ liệu tại thời điểm đó |
| AC-37 | Given lần chạy định kỳ đến khi run trước còn Running, hoặc scheduler bị lỡ, then lần đó ghi Missed, cảnh báo vận hành, không chạy bù tự động |
| AC-38 | Given sửa campaign Active, then các lần chạy chưa bắt đầu bị hủy và campaign về Draft |

Audit, Parent, thông báo

| ID | Given / When / Then |
| :--- | :--- |
| AC-39 | Given mọi giao dịch Top-Up và Correction, then có Transaction Reference, số tiền, thời điểm, người thực hiện, campaign và run (nếu có); không xóa cứng |
| AC-40 | Given top-up thành công, when Parent xem Transaction History (R8), then thấy Type Top-up, Money in, Status Completed; Description không chứa lý do nội bộ |
| AC-41 | Given top-up thành công và Parent có email, then email được gửi bất đồng bộ; gửi lỗi không làm đổi kết quả top-up (nếu OQ-08 chốt trong phạm vi) |

## 6. Appendices

### Appendix A. Trạng thái Campaign, Run, Run Item và Transaction

| Đối tượng | Từ | Sang | Điều kiện | Ghi chú |
| :--- | :--- | :--- | :--- | :--- |
| Campaign | (mới) | Draft | HQ User Save | Sửa được |
| Campaign | Draft | Running | Preview đạt, Confirm, chọn Run now | Tạo run đầu tiên |
| Campaign | Draft | Scheduled | Confirm, chọn Run at date and time | Chờ đến giờ |
| Campaign | Draft | Active | Confirm, chọn Recurring | NextRunAt được tính |
| Campaign | Scheduled hoặc Active | Running | Đến giờ chạy | Mỗi campaign tối đa một run mở |
| Campaign | Running | Completed | Run của campaign ad-hoc kết thúc (Completed, CompletedWithErrors hoặc Stopped) | Không sửa được nữa |
| Campaign | Running | Active | Run của campaign định kỳ kết thúc | Chờ lần chạy kế tiếp |
| Campaign | Active | Ended | Quá End at, hoặc Academic Year chuyển CLOSED | Không tạo run mới |
| Campaign | Scheduled hoặc Active | Draft | HQ User sửa criterion, số tiền, ngân sách | Hủy các run chưa bắt đầu; phải preview và Confirm lại |
| Campaign | Draft, Scheduled hoặc Active | Cancelled | HQ User Cancel | Không còn run nào được tạo |
| Run | (mới) | Pending | Đến giờ hoặc HQ User chạy ngay | Khóa campaign |
| Run | Pending | Running | Bắt đầu lập danh sách và xử lý |  |
| Run | Pending | Cancelled | Hủy trước khi bắt đầu |  |
| Run | Running | Completed | Hết danh sách, không còn run item Failed hoặc ReconciliationRequired |  |
| Run | Running | CompletedWithErrors | Hết danh sách, còn run item Failed hoặc ReconciliationRequired |  |
| Run | Running | Stopped | HQ User Stop | Item còn lại Skipped (RUN_STOPPED) |
| Run | CompletedWithErrors | Completed | Thử lại hoặc vận hành xử lý hết Failed và ReconciliationRequired |  |
| Run | (lần chạy định kỳ) | Missed | Run trước còn Running, hoặc scheduler bị lỡ giờ | Cảnh báo vận hành, không chạy bù |
| Run Item | (mới) | Pending | Lập danh sách khi run bắt đầu |  |
| Run Item | Pending | Successful | Function 1 ghi có thành công | Số dư tăng một lần |
| Run Item | Pending | Skipped | Không đủ điều kiện, hết ngân sách, hoặc run bị Stop | Số dư không đổi; có Skip Reason |
| Run Item | Pending | Failed | Lỗi xử lý hoặc kiểm tra | Số dư không đổi; có Failure Code |
| Run Item | Pending | ReconciliationRequired | Không xác định được kết quả ghi có | Tính trong nhóm Failed |
| Run Item | Failed | Successful, Skipped hoặc Failed | HQ User Retry failed | Dùng lại FundingReference |
| Run Item | ReconciliationRequired | Successful hoặc Failed | Bộ phận vận hành xử lý |  |
| Transaction | (mới) | Pending | HQ User xác nhận, hoặc run item bắt đầu ghi có | Có FundingReference |
| Transaction | Pending | Success | Function 1 ghi sổ cái thành công | Có mã bút toán của Function 1 |
| Transaction | Pending | Failed | Không đủ điều kiện, hoặc Function 1 báo lỗi | Số dư không đổi |
| Transaction | Pending | ReconciliationRequired | Không xác định được kết quả sau khi hỏi lại Function 1 | Cảnh báo vận hành |
| Transaction | ReconciliationRequired | Success hoặc Failed | Bộ phận vận hành xử lý |  |

### Appendix B. Open Questions & Assumptions

| ID | Câu hỏi | Ảnh hưởng | Phương án tạm trong FS |
| :--- | :--- | :--- | :--- |
| OQ-01 | Hạn mức tối đa mỗi lần top-up lẻ và mỗi tài khoản trong bulk | BR-F2-03, BR-F2-19, MSG-0203 | Chưa đặt hạn mức; cấu hình được |
| OQ-02 | Lịch định kỳ gồm những tần suất nào; Budget Limit áp dụng cho từng run hay cộng dồn theo campaign hoặc theo kỳ | BR-F2-20, BR-F2-24 | Từng run; ba tần suất MONTHLY, QUARTERLY, YEARLY |
| OQ-03 | Có cần phê duyệt hai bước (maker-checker) cho campaign, kích hoạt định kỳ hoặc sửa top-up | BR-F2-12, OOS #6 | Không; HQ User xác nhận một bước, có audit |
| OQ-04 | Thời hạn cho phép sửa top-up nhầm; xử lý khi tiền đã dùng trả phí (số dư không đủ) | BR-F2-10, EX-14 | Không giới hạn thời gian; từ chối khi số dư không đủ, vận hành xử lý ngoài hệ thống |
| OQ-05 | Có cần sửa từng giao dịch trong batch, hoặc hoàn tác cả một run | BR-F2-08, OOS #4 | Ngoài phạm vi |
| OQ-6 | Actively Enrolled chỉ dựa trên enrollment hay cần cả class assignment | BR-F2-17 | Chỉ enrollment |
| OQ-7 | Campaign Eligibility Date của ad-hoc dùng ngày chạy hay một ngày cố định (ví dụ đầu năm học) | BR-F2-18 | HQ User chọn, mặc định ngày chạy |
| OQ-8 | Description của top-up hiển thị cho Parent: tên campaign hay "MOE Top-up" chung | Mục 2.2 (R8) | "MOE Top-up" chung |
| OQ-9 | Tài khoản thỏa nhiều campaign cùng kỳ: cho nhận nhiều khoản hay chặn | BR-F2-28 | Cho phép, preview cảnh báo |
| OQ-11 | Ngưỡng thời gian Pending trước khi chuyển ReconciliationRequired; chu kỳ hỏi lại Function 1 | EX-05 | Do Dev cấu hình; không tự Failed |

### Appendix C. Danh sách màn hình

| Mã | Màn hình | Thành phần chính | Hành động | Trạng thái UI |
| :--- | :--- | :--- | :--- | :--- |
| SCR-01 | Individual Top-Up: Tìm EA | Chọn kiểu tìm, ô nhập Account Number hoặc NRIC | Search | Loading, Empty (không có kết quả), Error |
| SCR-02 | Xác minh chủ tài khoản và nhập số tiền | Tên, NRIC che một phần, tuổi, Account Number, Account Status, Current Balance, ô Top-Up Amount, Reason | Continue, quay lại | Ô nhập bị vô hiệu khi EA không Active |
| SCR-03 | Xem lại và xác nhận | Chủ tài khoản, số tiền, số dư sau top-up, lý do | Xác nhận, hủy | Nút xác nhận bị vô hiệu sau khi bấm; Processing |
| SCR-04 | Kết quả top-up | Trạng thái, Transaction Reference, số dư mới, thông báo | Về SCR-01, xem Top-Up History | Success, Failed, Verifying |
| SCR-05 | Top-Up History | Bộ lọc, bảng giao dịch (gồm Corrected và Effective amount), nút Correct | Lọc, Correct, xem chi tiết | Loading, Empty, Error |
| SCR-06 | Sửa top-up | Giao dịch gốc, Effective amount còn lại, kiểu sửa, số tiền ghi nợ, Reason | Xác nhận, hủy | Lỗi từng trường |
| SCR-07 | Danh sách Campaign | Bảng campaign, bộ lọc Academic Year, Round, Status | Create, mở, Cancel | Loading, Empty |
| SCR-08 | Cấu hình Campaign | Name, Academic Year, Round, criterion (Age Range, Account Balance, Schooling Status), Top-Up Amount, Budget Limit | Save, Preview | Draft; lỗi từng trường |
| SCR-09 | Preview | Danh sách eligible, tổng số tài khoản, tổng tiền, Budget Limit, Remaining budget, cảnh báo trùng campaign, thời điểm preview | Confirm, quay lại sửa | Confirm bị vô hiệu khi vượt ngân sách hoặc không có tài khoản |
| SCR-10 | Chọn chế độ chạy | Run now, Run at date and time, Recurring; Eligibility Date; lịch | Xác nhận, hủy | Lỗi từng trường |
| SCR-11 | Danh sách Run | Bảng run: trạng thái, số liệu, Eligibility Date | Mở run, Stop, Cancel | Pending, Running, Completed, CompletedWithErrors, Stopped, Missed |
| SCR-12 | Run summary và Run Item | Tổng Successful, Skipped, Failed (số lượng và tiền), ngân sách đã dùng, bảng run item, bộ lọc Outcome | Export CSV, Retry failed | Loading, Empty, Error |
