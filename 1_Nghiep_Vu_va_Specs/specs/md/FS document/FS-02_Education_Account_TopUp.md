# **R2 (v3)**

# **Function 2 (R2) – Top-Up Management**

## **1\. Introduction**

### **1.1. Preface**

Tài liệu này là Functional Specification (FS) cho Function 2 (R2) – Top-Up Management trên Admin Portal của hệ thống Education Account & FAS (MOE Singapore). Function 2 cho phép MOE HQ User nạp tiền vào Education Account (EA) theo hai cách: nạp lẻ cho từng chủ tài khoản (Individual Top-Up), hoặc nạp hàng loạt theo campaign (Bulk Campaigns) với criterion tùy chọn theo độ tuổi và số dư. Campaign tạo một lần và dùng lại nhiều lần: HQ User bấm Run Campaign ngay ở danh sách để chạy một batch mới.

### **1.2. Personas**

| Persona | Loại | Vai trò trong Function 2 |
| :---- | :---- | :---- |
| MOE HQ User | Primary actor | Nạp lẻ; tạo và sửa campaign; xem preview; bấm Run Campaign; theo dõi kết quả batch và Top-Up History |
| School User | Không phải actor | Không có quyền Top-Up, không thấy menu Top-up |
| Parent | Gián tiếp | Thấy giao dịch Top-up trong Transaction History (R8) |
| Admin Portal System | Hệ thống | Kiểm tra điều kiện, tính danh sách eligible, chạy batch, ghi log và audit |

### **1.3. Design Assumptions and Limitations**

#### **Design Assumptions**

| ID | Assumption |
| :---- | :---- |
| DA-02 | Function 2 ghi có trực tiếp vào số dư EA, đồng thời thêm một bút toán vào trong cùng một database transaction. |
| DA-03 | Chỉ MOE HQ User dùng được Function 2\. School User và Parent không có quyền. |
| DA-04 | Chỉ EA có trạng thái Active mới nhận top-up. |
| DA-06 | Preview chỉ mang tính tham khảo và không bắt buộc trước khi chạy. Khi chạy, hệ thống đánh giá lại từng tài khoản bằng dữ liệu tại thời điểm đó. |
| DA-07 | Criterion của campaign là tùy chọn (Age Range, Account Balance): tài khoản eligible khi thỏa tất cả criterion đã chọn. Nếu không chọn criterion nào, mặc định lấy hết (mọi EA Active). Mỗi tài khoản eligible nhận một số tiền cố định. |
| DA-09 | Campaign dùng lại được. HQ User bấm Run Campaign ở danh sách Bulk Campaigns để chạy ngay; mỗi lần bấm tạo một batch mới. Không cần Preview hay bước xác nhận riêng, không có chế độ chạy theo lịch hay định kỳ. |
| DA-11 | Mỗi lần ghi có tạo một top-up transaction với Reference ID riêng, và kiểm tra bằng Reference ID để không phát sinh hai giao dịch trùng. |
| DA-12 | Tiền tệ SGD, 2 chữ số thập phân, hiển thị dạng \$1,234.00. Ngày giờ hiển thị dạng 21 Oct 2026, 5:56 pm theo giờ Singapore (SGT, UTC+8); lưu UTC. |
| DA-13 | Function 2 không thiết lập ngân sách hay hạn mức cho campaign. Chi tiêu được theo dõi bằng Top-Up Summary (Total Spending, Successful, Failed) khi xem history, campaign và batch; số liệu chỉ để xem, không chặn ghi có. |
| DA-14 | Mỗi campaign chỉ có tối đa một batch đang Running tại một thời điểm. Khi batch đang Running, nút Run Campaign và Edit của campaign đó bị vô hiệu. |

#### **Limitations**

•      Function 2 không sửa hay hoàn tác top-up đã ghi có; top-up nhầm được xử lý ngoài hệ thống (OOS \#4).  
•      Function 2 chỉ được coi là đạt khi cả nạp lẻ và nạp hàng loạt chạy đúng tiêu chí chấp nhận.

### **1.4. Definitions, Acronyms and Abbreviations**

| Thuật ngữ | Giải thích |
| :---- | :---- |
| EA | Education Account. Tài khoản chi tiêu cho giáo dục của Singapore Citizen từ 7 đến dưới 16 tuổi. |
| Top-Up | Giao dịch ghi có một số tiền SGD vào EA. |
| Individual Top-Up | Top-up lẻ cho một EA do HQ User tìm và nhập số tiền. |
| Bulk Top-Up | Top-up cho nhiều EA cùng lúc theo criterion của một campaign. |
| Campaign | Định nghĩa một đợt bulk top-up: criterion tùy chọn (tuổi, số dư) và số tiền mỗi tài khoản. Tạo một lần, chạy được nhiều lần. Trạng thái: Draft (chưa chạy lần nào), Active (đã chạy ít nhất một lần), Deactive (bị tắt). |
| Criterion | Một điều kiện lọc tùy chọn của campaign: Age Range hoặc Account Balance. Các criterion khác để sprint sau. |
| Run Campaign | Thao tác chạy campaign ngay từ danh sách Bulk Campaigns. Mỗi lần bấm tạo một batch. |
| Batch | Một lần chạy campaign (một lần Run Campaign). Cột Batches Run ở danh sách là số batch đã chạy của campaign. |
| Batch Item | Kết quả xử lý của một EA trong một batch. |
| Preview | Danh sách tài khoản dự kiến eligible tại thời điểm xem, kèm tổng số và tổng tiền. Chỉ tham khảo, không bắt buộc trước khi chạy. |
| Total Spending | Tổng số tiền đã ghi có thành công (tổng Amount các giao dịch Success) trong phạm vi đang xem: theo bộ lọc History, theo campaign hoặc theo batch. |
| Top-Up Summary | Khối số liệu chỉ để xem gồm Total Spending, Successful, Failed. Không thiết lập ngân sách và không chặn top-up. |
| Successful / Failed | Hai nhóm kết quả của Batch Item: nạp thành công / không nạp được (lỗi xử lý, hoặc không còn đủ điều kiện khi chạy). |
| Reference ID | Mã tham chiếu duy nhất của một lần ghi có, dùng để chống ghi trùng và đối soát. |
| SGD | Singapore dollar. |

### **1.5. Exclusions**

FS này không đặc tả:  
•      Nguồn ngân sách, phê duyệt tài chính nội bộ MOE và hạch toán kế toán.  
•      Tạo và đóng EA (R1).  
•      Liên kết Student–EA (R3). Function 2 chỉ đọc.  
•      Hiển thị Transaction History cho Parent (R8) và thanh toán phí bằng EA (R9).  
•      Áp trợ cấp FAS (R4).  
•      Xác thực và phân quyền Admin Portal.

### **1.6. OOS List**

| \# | Hạng mục ngoài phạm vi | Lý do / nguồn | Dự kiến |
| :---- | :---- | :---- | :---- |
| 1 | Số tiền khác nhau theo từng tài khoản (theo bậc tuổi, cấp học) | Requirement chỉ nêu số tiền cố định mỗi tài khoản; muốn nhiều mức thì tạo nhiều campaign | Chưa xếp lịch |
| 2 | Criterion bổ sung (Schooling Status, School, Academic Level, Class, FAS tier) | Requirement ghi "etc."; bản này chỉ có Age Range và Account Balance; Schooling Status, School, Academic Level và Class để sprint sau (khi triển khai, chỉ chọn được Class sau khi đã chọn School) | Chưa xếp lịch |
| 3 | Nhập danh sách tài khoản bằng file CSV | Không có trong requirement | Chưa xếp lịch |
| 4 | Sửa hoặc hoàn tác top-up đã ghi có (top-up lẻ, từng giao dịch trong batch, cả một batch) | Đã bỏ khỏi phạm vi (US-033 Incorrect Manual Top-Up Correction); top-up nhầm được xử lý ngoài hệ thống | Sau khi client chốt |
| 5 | Top-up cho EA Closed, chuyển số dư sang CPF | CPF Transfer chưa triển khai ở R1 | Cùng CPF Transfer |
| 6 | Phê duyệt hai bước (maker-checker) | Chưa có trong requirement (OQ-03) | Chưa xếp lịch |
| 7 | Dashboard phân tích chi tiêu nhiều campaign | Không có trong requirement; bản này chỉ có Top-Up Summary (Total Spending, Successful, Failed) khi xem history, từng campaign và từng batch, và export | Chưa xếp lịch |
| 8 | Mọi thông báo cho Parent (email, SMS, trong ứng dụng) | Đã bỏ khỏi phạm vi (F2.8 Parent Notification); FS-08 cũng đã bỏ chuông thông báo | Chưa xếp lịch |
| 9 | Thiết lập ngân sách hoặc hạn mức cho campaign, cảnh báo vượt ngân sách | Đã bỏ khỏi phạm vi; thay bằng Top-Up Summary khi xem history | Chưa xếp lịch |
| 10 | Chạy campaign theo lịch (một lần hoặc định kỳ), chọn chế độ chạy | Đã bỏ khỏi phạm vi; campaign chỉ chạy khi HQ User bấm Run Campaign | Chưa xếp lịch |

## **2\. System Process and Function Overview**

### **2.1. Process Flow Diagrams**

#### ***2.1.1 Individual Top-Up Flow***

HQ User tìm một EA, kiểm tra thông tin chủ tài khoản, nhập số tiền và xác nhận. Chỉ EA Active mới nhận tiền; thất bại không làm đổi số dư.  
1\.     HQ User mở menu Top-up, tab Individual Top-Up, tìm EA theo Account Number hoặc NRIC.  
2\.     Hệ thống hiển thị thông tin chủ tài khoản, trạng thái và số dư; EA không Active thì không cho nhập số tiền.  
3\.     HQ User nhập số tiền (lý do không bắt buộc), xem lại và xác nhận.  
4\.     Hệ thống tạo giao dịch với Reference ID và ghi có vào EA.  
5\.     Kết quả Success hoặc Failed hiển thị ở màn hình kết quả và trong Top-Up History; thất bại thì số dư không đổi.

#### ***2.1.2 Bulk Campaign Flow – Create, Run and Re-run***

HQ User tạo campaign ở tab Bulk Campaigns với criterion tùy chọn (tuổi, số dư) và số tiền mỗi tài khoản. Từ danh sách, HQ User có thể Preview để xem số tài khoản được Top-up và tổng tiền dự kiến, Edit lại, hoặc bấm Run Campaign luôn. Campaign dùng lại được: mỗi lần Run Campaign tạo một batch mới và Batches Run tăng thêm 1\.  
1\.     HQ User chọn Create Campaign, nhập Campaign Name, cấu hình criterion tùy chọn (Age, Account Balance) và số tiền mỗi tài khoản, rồi Save. Campaign ở trạng thái Draft.  
2\.     (Tùy chọn) HQ User bấm Preview ở danh sách để xem danh sách eligible tại thời điểm hiện tại.  
3\.     (Tùy chọn) HQ User bấm Edit để sửa lại campaign.  
4\.     HQ User bấm Run Campaign ở dòng campaign. Hệ thống tạo batch mới, lập danh sách eligible theo dữ liệu lúc đó và bắt đầu ghi có từng tài khoản; lần chạy đầu tiên chuyển campaign từ Draft sang Active.  
5\.     HQ User theo dõi batch ở Top-Up History (Bulk Batches), kèm Top-Up Summary; xem Batch Item, export CSV.  
6\.     Muốn chạy lại, HQ User bấm Run Campaign lần nữa; Batches Run tăng thêm 1\.

## **3\. Detailed Functions and Solution Design**

### **3.1. Detailed Function Specification**

#### ***3.1.1. Function Description***

Function 2 cho MOE HQ User nạp tiền vào EA theo hai cách: nạp lẻ cho một chủ tài khoản, hoặc nạp hàng loạt theo campaign. Campaign gồm criterion tùy chọn (tuổi, số dư) và số tiền cố định mỗi tài khoản. Campaign dùng lại được: HQ User có thể Preview, Edit lại hoặc bấm Run Campaign ở danh sách để chạy ngay một batch, không cần Preview hay bước xác nhận riêng. Khi xem Top-Up History, campaign và batch, HQ User thấy Total Spending, Successful, Failed.

| Mục | Nội dung |
| :---- | :---- |
| Function ID | F2 (R2) |
| Portal | Admin Portal, menu Top-up, ba tab: Individual Top-Up, Bulk Campaigns, Top-Up History |
| Actor chính | MOE HQ User |
| Precondition | HQ User đã đăng nhập Admin Portal và có quyền Top-Up; EA đã được tạo (R1) |
| Postcondition (thành công) | Mỗi lần ghi có thành công làm số dư EA tăng đúng một lần; có top-up transaction với Reference; có audit log. Với bulk: có batch summary Successful, Failed và Top-Up Summary (Total Spending, Successful, Failed) của campaign |
| Postcondition (thất bại) | Top-up transaction \= Failed; số dư EA không đổi; lý do được ghi log. Với bulk: các tài khoản khác trong batch vẫn được xử lý |
| Postcondition (đang chạy) | Batch \= Running; campaign không sửa được và không chạy thêm batch khác cho đến khi batch kết thúc |

##### **Sub-functions**

| ID | Sub-function | Mục đích |
| :---- | :---- | :---- |
| F2.1 | Search and Verify EA Account Holder | Tìm kiếm tài khoản EA theo Account Number hoặc Student NRIC; hiển thị thông tin chủ tài khoản, trạng thái tài khoản và số dư hiện tại để xác minh trước khi nạp tiền. |
| F2.2 | Individual Top-Up | Thực hiện nạp tiền cho một tài khoản EA cụ thể; nhập số tiền, xác nhận giao dịch, kiểm tra điều kiện hợp lệ, ghi có vào EA và hiển thị kết quả. |
| F2.3 | Top-Up History | Tra cứu lịch sử top-up lẻ (Individual Top-Ups) và top-up từ bulk (Bulk Batches), lọc theo nguồn và trạng thái, tìm theo tên học sinh; xem Top-Up Summary (Total Spending, Successful, Failed) theo bộ lọc, theo campaign và theo batch; lưu vết kiểm toán. |
| F2.4 | Top-Up Campaign Configuration | Tạo và sửa campaign theo tiêu chí đối tượng thụ hưởng và số tiền nạp; tìm và lọc danh sách Bulk Campaigns. |
| F2.5 | Eligibility Preview | Xác định danh sách tài khoản đủ điều kiện theo các tiêu chí đã cấu hình; hiển thị số lượng tài khoản và tổng số tiền dự kiến để kiểm tra criterion. |
| F2.6 | Run Campaign | Khi HQ User bấm Run Campaign ở danh sách, hệ thống tạo ngay một batch và chạy. |
| F2.7 | Top-Up Execution and Batch Monitoring | Thực thi top-up theo danh sách lập lúc chạy; kiểm tra lại điều kiện từng tài khoản trước khi ghi có; tổng hợp kết quả thành công/thất bại, xuất báo cáo và lưu audit log. |

#### ***Business Rules***

**Nhóm A – Quyền và Individual Top-Up (F2.1, F2.2)**  
•      BR-F2-01: Chỉ MOE HQ User có quyền Top-Up.  
•      BR-F2-02: Tìm EA theo khớp chính xác Account Number hoặc NRIC đầy đủ của học sinh; không tìm gần đúng. Chỉ khi nhập đủ và đúng NRIC (hoặc Account Number) mới hiển thị tài khoản; nhập thiếu, thừa ký tự hoặc sai thì không có kết quả, không có danh sách gợi ý, không hiển thị kết quả một phần, và chỉ báo MSG-0201. Mỗi lần tìm trả về tối đa một EA. Kết quả hiển thị NRIC che một phần.  
•      BR-F2-03: Số tiền top-up lớn hơn 0, tối đa 2 chữ số thập phân, không vượt hạn mức mỗi lần (TBC, OQ-01). Lý do (reason) optional, tối đa 200 ký tự.  
•      BR-F2-04: Chỉ EA Active nhận top-up.  
•      BR-F2-06: Giao dịch thất bại không làm đổi số dư nhưng vẫn được ghi log trên MOE (thời điểm, người thực hiện, lý do).  
**Nhóm B – Lịch sử (F2.3)**  
•      BR-F2-07: Tab Top-Up History liệt kê mọi top-up lẻ và top-up từ bulk (SCR-05). Hai nút Filter by Source (Individual Top-Ups, Bulk Batches) chọn nguồn đang xem; ngoài ra có ô Search theo tên học sinh và bộ lọc Status.  
> > > o      Phía trên bảng là ba thẻ Top-Up Summary tính theo đúng bộ lọc đang chọn: Total Spending (tổng Amount các giao dịch Success, ghi chú "Credited successfully only"), Successful (số giao dịch Success, ghi chú "Accounts credited") và Failed (số giao dịch thất bại, ghi chú "Transactions failed").  
> > > o      Bảng sắp xếp mặc định theo Date / Time mới nhất trước; cột Date / Time và Amount sắp xếp được. Campaign bulk đã chạy xem được ở danh sách Bulk Campaigns (SCR-07, cột Batches Run), danh sách batch (SCR-11) và Batch summary (SCR-12), kèm ba chỉ số này theo từng campaign và batch. Số liệu chỉ để xem, không chặn ghi có.  
**Nhóm C – Cấu hình Campaign (F2.4)**  
•      BR-F2-13: Campaign Code duy nhất, hệ thống sinh theo mẫu CMP-YYYY-NNNN.  
•      BR-F2-14: Criterion là tùy chọn. HQ User có thể không chọn criterion nào (mặc định lấy hết mọi EA đủ điều kiện nền) hoặc chọn một hoặc cả hai loại criterion; tài khoản eligible khi thỏa tất cả criterion đã chọn. Điều kiện nền áp dụng cho mọi tài khoản và không phải criterion: Student SC có liên kết EA và EA Active. Bản này có hai loại criterion, mỗi loại thêm tối đa một lần:  
> > > o      Age Range: Minimum Age, Maximum Age (bao gồm cả hai đầu); thỏa khi tuổi của học sinh tại ngày bấm Run Campaign (hoặc Preview) nằm trong khoảng.  
> > > o      Account Balance: toán tử và ngưỡng SGD; thỏa khi số dư hiện tại so với ngưỡng đúng toán tử.  
> > > o      Các criterion Schooling Status, School, Academic Level và Class để sprint sau (OOS \#2). Khi triển khai, chỉ chọn được Class sau khi đã chọn School.  
•      BR-F2-15: Age Range: chỉ nhận giá trị lớn hơn hoặc bằng 7 VÀ bé hơn 16 vì EA chỉ tồn tại từ 7 đến dưới 16 tuổi. Tuổi được tính theo số năm tròn của ngày hôm đó (ngày bấm Run Campaign hoặc Preview).  
•      BR-F2-17: Function 2 không thiết lập ngân sách hay hạn mức cho campaign. Chi tiêu của campaign được theo dõi bằng Top-Up Summary (BR-F2-07); không có bước chặn hay cảnh báo theo ngân sách ở preview hay khi chạy.  
•      BR-F2-18: Trạng thái campaign: Draft, Active, Deactive (Appendix A).  
> > > o      Draft: chưa chạy lần nào (Batches Run \= 0). Active: đã chạy ít nhất một lần (Batches Run lớn hơn hoặc bằng 1).  
> > > o      Deactive: campaign bị tắt, không chạy được (cách bật, tắt TBC, OQ-13).  
**Nhóm D – Preview và thực thi (F2.5, F2.6, F2.7)**  
•      BR-F2-19: Preview hiển thị Student Name, Age, Balance, Top-Up Amount dự kiến của từng tài khoản, cùng tổng số tài khoản, tổng tiền dự kiến và thời điểm tính preview. Preview chỉ đọc, không có nút Confirm.  
•      BR-F2-20: Run Campaign không yêu cầu Preview trước. Điều kiện để chạy: campaign không Deactive, không có batch Running của campaign đó, và có ít nhất một tài khoản eligible tại lúc bắt đầu chạy. Không có tài khoản eligible thì báo không có tài khoản (MSG-0214) và không tạo batch.  
•      BR-F2-21: Khi HQ User bấm Run Campaign ở danh sách, hệ thống tạo batch ngay (Pending rồi Running) và ghi audit log người bấm. Nút Run Campaign bị vô hiệu sau lần bấm đầu. Không có lựa chọn chế độ chạy, lịch chạy hay bước xác nhận riêng.  
•      BR-F2-22: Campaign chạy được nhiều lần; mỗi lần Run Campaign tạo một batch mới và Batches Run tăng 1; lần chạy đầu tiên chuyển campaign từ Draft sang Active. Mỗi campaign chỉ có một batch Running tại một thời điểm; bấm Run Campaign hai lần, hoặc hai HQ User bấm cùng lúc, chỉ tạo một batch (kiểm tra bằng row version).  
•      BR-F2-24: Khi chạy, hệ thống xử lý từng tài khoản theo thứ tự Account Number tăng dần, theo từng đoạn nhỏ: EA còn Active, đánh giá lại các criterion đã chọn bằng dữ liệu tại thời điểm đó, ghi có. Sau mỗi đoạn hệ thống cập nhật số liệu batch (Successful, Failed, Total credited) để theo dõi.  
•      BR-F2-25: Trong một batch, mỗi tài khoản được ghi có tối đa một lần (duy nhất theo Batch và EA). Giữa các batch của cùng campaign hoặc của campaign khác, một tài khoản có thể nhận nhiều khoản.  
•      BR-F2-26: Kết quả từng tài khoản chỉ có hai trạng thái: Successful hoặc Failed. Failed kèm Failure Code: không còn đủ điều kiện khi chạy (EA\_NOT\_ACTIVE, CRITERIA\_NOT\_MATCH khi không còn thỏa criterion đã chọn) hoặc lỗi kỹ thuật (ví dụ CREDIT\_FAILED).  
•      BR-F2-27: Mỗi batch item (mỗi tài khoản được top-up trong batch) có một Reference ID riêng, sinh một lần và duy nhất trong toàn hệ thống; dùng để kiểm tra không ghi trùng. Việc theo dõi theo campaign dùng Campaign Code, batch không có Reference ID riêng.  
•      BR-F2-29: Batch summary hiển thị Total Spending của batch (Total credited), tổng Successful, Failed (số tài khoản và số tiền), lọc theo kết quả; export CSV. Trạng thái batch: Completed khi không có Failed, Failed khi còn Failed kèm lý do.  
•      BR-F2-30: Audit lưu vĩnh viễn: Reference, số tiền, thời điểm, người thực hiện (HQ User, hoặc "System" kèm HQ User đã bấm Run Campaign), campaign, batch. Không xóa cứng campaign, batch, batch item và giao dịch.

#### ***3.1.2. Process Flow Description and Screens***

##### **A. Individual Top-Up Flow**

**Bước 1\. Tìm EA và xác minh chủ tài khoản (F2.1)**  
•      **1.1** HQ User vào menu Top-up, chọn tab Individual Top-Up (SCR-01).  
•      **1.2** HQ User nhập Account Number hoặc NRIC đầy đủ của học sinh và chọn Search. Hệ thống tìm EA theo khớp chính xác (BR-F2-02).  
•      **1.3** Hệ thống hiển thị SCR-02: tên học sinh, NRIC che một phần, tuổi, Account Number, Account Status, Current Balance.  
•      **1.4** Luồng thay thế: không tìm thấy thì báo MSG-0201; EA không Active vẫn hiển thị để tra cứu nhưng không cho nhập số tiền, kèm lý do (MSG-0204).  
**Bước 2\. Nhập số tiền và xác nhận (F2.2)**  
•      **2.1** Trên SCR-02, HQ User nhập Top-Up Amount và Reason (không bắt buộc), rồi chọn Continue.  
•      **2.2** Hệ thống kiểm tra định dạng và hạn mức (BR-F2-03).  
•      **2.3** Hệ thống hiển thị SCR-03 để xem lại: chủ tài khoản, Account Number, số dư hiện tại, số tiền, số dư sau top-up (tham khảo), lý do (nếu có).  
•      **2.4** HQ User xác nhận. Nút xác nhận bị vô hiệu ngay sau lần bấm đầu.  
**Bước 3\. Ghi có (F2.2)**  
•      **3.1** Hệ thống tạo top-up transaction (Pending) với Reference ID.  
•      **3.2** Hệ thống kiểm tra Reference ID chưa được dùng.  
•      **3.3** Hệ thống lưu vào history và cập nhất số dư mới.  
> > > o      Thành công: transaction Success, ghi audit log, hiển thị SCR-04 kèm Reference và số dư mới (MSG-0207).  
> > > o      Thất bại (EA không Active, hoặc lỗi khi ghi có): transaction Failed, số dư không đổi, hiển thị SCR-04 (MSG-0204 hoặc MSG-0208).  
**Bước 4\. Xem lịch sử top-up lẻ (F2.3)**  
•      **4.1** HQ User mở tab Top-Up History (SCR-05), chọn Filter by Source là Individual Top-Ups.  
•      **4.2** Màn hình hiển thị ba thẻ Top-Up Summary (Total Spending, Successful, Failed), tính theo đúng bộ lọc đang chọn (BR-F2-07).  
•      **4.3** HQ User có thể nhập tên học sinh vào ô Search, chọn Status, rồi bấm Search hoặc Reset.  
•      **4.4** Bảng giao dịch hiển thị mới nhất trước: Date / Time, Reference, Student, Account, Amount, Status, Note.  
•      **4.5** Màn hình chỉ để tra cứu; không có thao tác sửa hoặc hoàn tác top-up (OOS \#4). Parent thấy giao dịch trong Transaction History của R8 ngay sau khi ghi có.

##### **B. Batch Top-Up Flow**

**Bước 1\. Tạo và cấu hình Campaign (F2.4)**  
•      **1.1** HQ User vào tab Bulk Campaigns (SCR-07), chọn Create Campaign.  
•      **1.2** Trên SCR-08, HQ User nhập Campaign Name.  
•      **1.3** HQ User cấu hình criterion tùy chọn gồm Minimum & Maximum Age hoặc Minimum & Maximum Account Balance.  
•      **1.4** HQ User nhập Top-Up Amount per account, rồi Save Draft/ Preview.  
•      **1.5** Hệ thống kiểm tra theo BR-F2-13 đến BR-F2-18 và lưu campaign ở trạng thái Draft.  
•      **1.6** Từ danh sách, HQ User có thể Preview, Edit lại hoặc Run Campaign luôn; Edit bị vô hiệu khi campaign có batch Running.  
**Bước 2\. Xem Preview, tùy chọn (F2.5)**  
•      **2.1** HQ User bấm Preview ở dòng campaign.  
•      **2.2** Hệ thống đánh giá các criterion đã chọn trên các EA Active theo dữ liệu hiện tại.  
•      **2.3** Hệ thống hiển thị SCR-09: danh sách eligible (Student Name, Age, Balance, Top-Up Amount), tổng số tài khoản, tổng tiền dự kiến, thời điểm tính preview.  
•      **2.4** Không có tài khoản eligible: hiển thị MSG-0214.  
•      **2.5** Preview chỉ đọc; HQ User quay lại danh sách để chạy.  
**Bước 3\. Run Campaign (F2.6)**  
•      **3.1** HQ User bấm Run Campaign ở dòng campaign ngay trên danh sách SCR-07. Nút bị vô hiệu sau lần bấm đầu.  
•      **3.2** Không có bước Preview bắt buộc, lựa chọn chế độ chạy, lịch chạy hay xác nhận riêng.  
•      **3.3** Hệ thống ghi audit log người bấm và tạo batch ngay.  
•      **3.4** Chưa có tài khoản eligible thì báo MSG-0214, không tạo batch.  
•      **3.5** Batch đã chạy không dừng giữa chừng được.  
**Bước 4\. Thực thi batch và nhận kết quả (F2.7)**  
•      **4.1** Hệ thống tạo batch (Pending, rồi Running) và khóa campaign (không Edit, không Run thêm).  
•      **4.2** Hệ thống cố định criterion và số tiền cho batch này; lần chạy đầu tiên chuyển campaign sang Active.  
•      **4.3** Hệ thống xử lý từng tài khoản theo BR-F2-24: kiểm tra, ghi có vào EA với Reference ID riêng của từng batch item (BR-F2-27), ghi kết quả Successful hoặc Failed.  
•      **4.4** HQ User theo dõi tiến độ ở SCR-11 và SCR-12 (số đã xử lý, Successful, Failed, Total credited).  
•      **4.5** Hết danh sách: batch \= Completed (không có Failed) hoặc Failed (còn Failed, kèm lý do); hiển thị batch summary (BR-F2-29).  
•      **4.6** Campaign được mở lại để Edit hoặc Run Campaign lần nữa; Batches Run tăng 1\.  
**Bước 5\. Xem kết quả, export và chạy lại (F2.3, F2.7)**  
•      **5.1** HQ User mở tab Top-Up History (SCR-05), chọn Filter by Source là Bulk Batches để xem các batch đã chạy kèm Top-Up Summary (BR-F2-07).  
•      **5.2** HQ User mở một batch để xem SCR-12, lọc batch item theo kết quả và export CSV.  
•      **5.3** Batch item Failed không thử lại; cần thì chạy batch mới.  
•      **5.4** Parent thấy giao dịch trong Transaction History của R8 ngay sau khi ghi có.  
•      **5.5** Muốn chạy đợt mới, HQ User bấm Run Campaign lần nữa ở SCR-07 (BR-F2-22).

##### **Trường hợp ngoại lệ**

| \# | Tình huống | Xử lý |
| :---- | :---- | :---- |
| EX-01 | School User hoặc Parent gọi API Top-Up, hoặc HQ User sửa ID trong request để thao tác trên campaign hay giao dịch không thuộc quyền | Server kiểm tra quyền cho mọi request, trả 403, không lộ dữ liệu, ghi log bảo mật (MSG-0003) |
| EX-02 | EA chuyển sang Closed giữa lúc HQ User xem và lúc xác nhận | Top-up bị từ chối, số dư không đổi (MSG-0204) |
| EX-04 | Bấm xác nhận hai lần, hoặc client gửi lại cùng một yêu cầu | Chỉ tạo một transaction (kiểm tra bằng Reference ID) và ghi có một lần; lần gửi lại nhận kết quả của transaction đầu |
| EX-06 | Session Admin Portal hết hạn khi đang thao tác | Hết hạn trước khi xác nhận (top-up lẻ) hoặc trước khi bấm Run Campaign: yêu cầu đăng nhập lại, chưa có transaction hay batch. Hết hạn sau đó: transaction hoặc batch vẫn được xử lý; HQ User đăng nhập lại thấy trạng thái hiện tại (MSG-0002) |
| EX-07 | HQ User sửa criterion hoặc số tiền sau khi đã xem Preview | Preview chỉ tham khảo, không chặn gì. Run Campaign dùng định nghĩa hiện tại và đánh giá lại tại lúc chạy; danh sách thực tế có thể khác Preview cũ |
| EX-08 | Hai HQ User sửa hoặc Run Campaign cùng một campaign đồng thời; hoặc Edit, Run Campaign trên campaign đang có batch Running | Dùng row version để phát hiện xung đột, người sau nhận yêu cầu làm mới (MSG-0222). Campaign có batch Running không Edit hay Run Campaign được (MSG-0215) |
| EX-09 | Giữa preview (hoặc lúc lập danh sách) và lúc xử lý, một tài khoản đổi số dư hoặc bị đóng | Đánh giá lại khi chạy: tài khoản không còn đủ điều kiện (bị đóng, hoặc không còn thỏa criterion đã chọn) bị Failed với Failure Code tương ứng (EA\_NOT\_ACTIVE hoặc CRITERIA\_NOT\_MATCH); danh sách thực tế có thể khác preview |
| EX-11 | Job bị dừng đột ngột hoặc server khởi động lại giữa batch | Batch tiếp tục từ các batch item chưa xử lý. Kiểm tra Reference ID của từng item trước khi ghi có; không ghi có hai lần |

## **4\. Data Fields Table**

### **4.1. Trường hiển thị và nhập trên màn hình**

| Màn hình | Trường | Kiểu | Nguồn | Nhập | Bắt buộc | Quy tắc / ghi chú |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| SCR-01 | Search by | Enum ACCOUNT\_NUMBER, NRIC | HQ User chọn | Có | Có | Khớp chính xác, không tìm gần đúng, không gợi ý khi nhập dở |
| SCR-01 | Search value | Text | HQ User nhập | Có | Có | Account Number hoặc NRIC đầy đủ (9 ký tự) |
| SCR-02 | Student name | Text | Student Profile (R1) | Không | Có |   |
| SCR-02 | NRIC | Text | Student Profile (R1) | Không | Có | Che một phần, không đưa NRIC đầy đủ vào URL |
| SCR-02 | Age | Integer | Tính từ DOB | Không | Có | Số năm tròn tại ngày hiện tại |
| SCR-02 | Account Number | Text | Education Account | Không | Có |   |
| SCR-02 | Account Status | Enum Active, Closed | Education Account | Không | Có | Chỉ Active mới nhập được số tiền |
| SCR-02 | Current Balance | Decimal(18,2), SGD | Education Account | Không | Có |   |
| SCR-02 | Top-Up Amount | Decimal(18,2), SGD | HQ User nhập | Có | Có | Lớn hơn 0; tối đa 2 chữ số thập phân; không vượt hạn mức mỗi lần (TBC) |
| SCR-02 | Reason | Text, tối đa 200 ký tự | HQ User nhập | Có | Không | Chỉ dùng nội bộ, không hiển thị cho Parent. Hiển thị ở cột Note của Top-Up History |
| SCR-03 | Balance after top-up | Decimal(18,2) | Tính | Không | Không | Chỉ để tham khảo |
| SCR-04 | Reference | Text, tối đa 50 ký tự | Hệ thống sinh | Không | Có | Duy nhất; top-up lẻ theo mẫu TUP-IND-{timestamp ms}, ví dụ TUP-IND-1792580216342; tiền tố cho bulk TBC |
| SCR-04 | Transaction Status | Enum Success, Failed | Transaction | Không | Có |   |
| SCR-04 | New balance | Decimal(18,2) | Education Account | Không | Không | Chỉ khi Success |
| SCR-05 | Thẻ Total Spending | Decimal(18,2), SGD | Tính | Không | Có | Tổng Amount các giao dịch Success theo bộ lọc đang chọn; ghi chú "Credited successfully only" |
| SCR-05 | Thẻ Successful | Integer | Tính | Không | Có | Số giao dịch Success theo bộ lọc; ghi chú "Accounts credited" |
| SCR-05 | Thẻ Failed | Integer | Tính | Không | Có | Số giao dịch thất bại theo bộ lọc; ghi chú "Transactions failed" |
| SCR-05 | Filter by Source | Nút chọn Individual Top-Ups, Bulk Batches | HQ User chọn | Có | Không | Chọn nguồn đang xem; thẻ Top-Up Summary và bảng đổi theo |
| SCR-05 | Search | Text | HQ User nhập | Có | Không | Tìm theo tên học sinh (placeholder "Search by student name"); có nút xóa nội dung |
| SCR-05 | Status | Dropdown All Statuses, Success, Failed | HQ User chọn | Có | Không | Mặc định All Statuses |
| SCR-05 | Nút Search, Reset | Button | HQ User bấm | Có | Không | Reset bị vô hiệu khi chưa có bộ lọc nào |
| SCR-05 | Cột bảng | Date / Time, Reference, Student, Account, Amount, Status, Note | Transaction | Không | Có | Date / Time mới nhất trước, dạng 21 Oct 2026, 5:56 pm (SGT); Student hiển thị tên và NRIC (OQ-14); Account là Account Number; Amount có dấu \$ và dấu phẩy; Note là Reason của top-up lẻ; Date / Time và Amount sắp xếp được; 20 dòng mỗi trang |
| SCR-07 | Search | Text | HQ User nhập | Có | Không | Tìm theo Campaign Code hoặc Campaign Name |
| SCR-07 | Status | Dropdown All Statuses, Draft, Active, Deactive | HQ User chọn | Có | Không | Mặc định All Statuses; có nút Search và Reset |
| SCR-07 | Create Campaign | Button | HQ User bấm | Có | Không | Mở SCR-08 ở chế độ tạo mới |
| SCR-07 | Cột danh sách | Campaign Code, Campaign Name, Amount Per Account (SGD), Batches Run, Status, Actions | Campaign | Không | Có | Campaign Name kèm dòng tóm tắt criterion (ví dụ Age: 7–12); Amount Per Account và Batches Run sắp xếp được; Batches Run là số batch đã chạy của campaign; Status: Draft khi Batches Run bằng 0, Active khi lớn hơn hoặc bằng 1, Deactive khi bị tắt |
| SCR-07 | Actions: Preview | Button | HQ User bấm | Có | Không | Mở SCR-09; dùng được ở mọi trạng thái campaign |
| SCR-07 | Actions: Edit | Button | HQ User bấm | Có | Không | Mở SCR-08 ở chế độ sửa; vô hiệu khi campaign có batch Running |
| SCR-07 | Actions: Run Campaign | Button | HQ User bấm | Có | Không | Chạy ngay một batch mới (BR-F2-20, BR-F2-21); bật với campaign Draft hoặc Active không có batch Running (OQ-13) |
| SCR-08 | Campaign Name | Text, tối đa 150 ký tự | HQ User nhập | Có | Có |   |
| SCR-08 | Age Range: Minimum, Maximum Age | Integer | HQ User nhập | Có | Không | 7 ≤ Min ≤ Max ≤ 15; nhập cả hai hoặc không nhập |
| SCR-08 | Account Balance: operator, threshold | Enum, Decimal(18,2) | HQ User chọn, nhập | Có | Không | Toán tử \<, \<=, \>, \>=, \=; ngưỡng không âm; nhập cả hai hoặc không |
| SCR-08 | Top-Up Amount per account | Decimal(18,2), SGD | HQ User nhập | Có | Có | Lớn hơn 0; không vượt hạn mức mỗi lần (TBC); hiển thị ở cột Amount Per Account (SGD) |
| SCR-09 | Cột preview | Student Name, Age, Balance, Top-Up Amount | Tính | Không | Có | 20 dòng mỗi trang; chỉ đọc |
| SCR-09 | Total accounts, Total amount (forecast), Previewed at | Integer, Decimal, Datetime | Tính | Không | Có | Chỉ để xem; không có nút Confirm |
| SCR-11 | Cột danh sách batch | Campaign Code, Status, Total, Successful, Failed, Total credited, Started at, Completed at | Batch | Không | Có | Mở từ Top-Up History, nguồn Bulk Batches (bố cục TBC, OQ-15); Status: Pending, Running, Completed, Failed |
| SCR-12 | Cột batch item | Student, Account Number, Age, Balance, Amount, Outcome, Failure Reason, Reference | Batch item | Không | Có | Lọc theo Outcome; nút Export CSV |
| SCR-12 | Batch summary | Integer, Decimal(18,2) | Tính | Không | Có | Total Spending (Total credited), Successful, Failed (số lượng và tiền) |

### **4.2. Thực thể dữ liệu liên quan**

Batch trong tài liệu này là bảng topup\_campaign\_runs; Batch Item là bảng topup\_run\_items. Tên bảng và cột (RunId, ...) giữ nguyên để khớp thiết kế DB hiện có.

#### **Campaign (topup\_campaigns)**

•      Id: VARCHAR(50) \- PK  
•      Code: NVARCHAR(50) \- Duy nhất; hiển thị dạng CMP-2026-0001  
•      Name: NVARCHAR(150)  
•      AmountPerAccount, CurrencyCode: DECIMAL(18,2), CHAR(3) \- Số tiền lớn hơn 0; mặc định SGD  
•      Status: INT \- 1 Draft, 2 Active, 3 Deactive. Draft chuyển Active khi batch đầu tiên được tạo; Deactive do HQ User đặt (OQ-13)  
•      DefinitionVersion: INT \- Tăng mỗi lần sửa; ghi vào batch lúc chạy  
•      CreatedBy, CreatedAt, UpdatedAt, RowVersion: VARCHAR(50), DATETIME2(3), ROWVERSION \- UTC; RowVersion là token kiểm soát đồng thời lạc quan  
•      Giá trị dẫn xuất (không lưu): Batches Run là số batch của campaign. Top-Up Summary của campaign cộng dồn từ các batch thuộc campaign: Total Spending là tổng TotalCredited; Successful, Failed là tổng SuccessfulCount, FailedCount.

#### **Criterion (topup\_campaign\_criteria)**

•      Id, CampaignId: VARCHAR(50) \- PK, FK Campaign  
•      CriterionType: INT \- 1 AGE\_RANGE, 2 BALANCE; duy nhất theo (CampaignId, CriterionType). Criterion là tùy chọn; campaign không có criterion nào thì lấy hết. Thêm loại mới ở sprint sau không đổi cấu trúc bảng  
•      MinAge, MaxAge: SMALLINT \- Bắt buộc khi AGE\_RANGE, cấm ở loại khác; 7 ≤ MinAge ≤ MaxAge ≤ 15  
•      BalanceOperator, BalanceThreshold: INT, DECIMAL(18,2) \- Bắt buộc khi BALANCE; 1 LT, 2 LTE, 3 GT, 4 GTE, 5 EQ; ngưỡng không âm

#### **Batch (topup\_campaign\_runs)**

•      Id, CampaignId: VARCHAR(50) \- PK, FK Campaign. Một campaign có nhiều batch  
•      BatchNo: INT \- Số thứ tự batch trong campaign (1, 2, ...); duy nhất theo (CampaignId, BatchNo)  
•      TriggeredBy: VARCHAR(50) \- IAM ID của HQ User đã bấm Run Campaign  
•      DefinitionVersion, AmountPerAccount: INT, DECIMAL(18,2) \- Snapshot tại lúc bắt đầu; sửa campaign không đổi batch đã tạo  
•      Status: INT \- 1 Pending, 2 Running, 3 Completed, 4 Failed  
•      TotalAccounts, SuccessfulCount, FailedCount: INT \- Không âm  
•      TotalCredited: DECIMAL(18,2) \- Tổng các khoản Successful của batch; là Total Spending của batch  
•      StartedAt, CompletedAt, CreatedAt, UpdatedAt, RowVersion: DATETIME2(3), ROWVERSION \- UTC  
•      Ràng buộc: tối đa một batch ở trạng thái Pending hoặc Running cho mỗi CampaignId (unique index có điều kiện); đây là cơ sở của DA-14

#### **Batch Item (topup\_run\_items)**

•      Id, RunId: VARCHAR(50) \- PK, FK Batch; duy nhất theo (RunId, EducationAccountId)  
•      EducationAccountId: UNIQUEIDENTIFIER \- FK logic tới EA  
•      AccountNumber, StudentProfileId: VARCHAR(50), UNIQUEIDENTIFIER \- Tham chiếu hiển thị; NRIC lấy qua Student Profile, không sao chép  
•      AgeAtRun, BalanceSnapshot, ExpectedAmount: SMALLINT, DECIMAL(18,2), DECIMAL(18,2) \- Giá trị lúc lập danh sách và lúc đánh giá; dùng để hiển thị và audit  
•      Outcome: INT \- 1 Pending, 2 Successful, 3 Failed  
•      FailureCode, FailureReason: VARCHAR(50), NVARCHAR(500) \- Bắt buộc khi Failed; mã lỗi (EA\_NOT\_ACTIVE, CRITERIA\_NOT\_MATCH, CREDIT\_FAILED) và nguyên nhân đã làm sạch  
•      ReferenceId: NVARCHAR(50) \- Duy nhất; sinh một lần  
•      TopUpTransactionId: VARCHAR(50) \- FK Transaction; bắt buộc khi Successful  
•      ProcessedAt, RowVersion: DATETIME2(3), ROWVERSION \- UTC

#### **Top-Up Transaction (topup\_transactions)**

•      Id: VARCHAR(50) \- PK  
•      TransactionReference: NVARCHAR(50) \- Duy nhất; hiển thị ở cột Reference của Top-Up History và ở SCR-04  
•      SourceType: INT \- 1 Individual, 2 Bulk  
•      EducationAccountId: UNIQUEIDENTIFIER \- FK logic tới EA  
•      RunItemId: VARCHAR(50) \- FK Batch Item; bắt buộc khi Bulk, cấm ở loại khác  
•      InitiatedByUserId: VARCHAR(50) \- IAM ID của HQ User; với Bulk là HQ User đã bấm Run Campaign  
•      ReferenceId: NVARCHAR(50) \- Duy nhất; hệ thống kiểm tra trước khi tạo giao dịch để chống ghi trùng  
•      Amount, CurrencyCode: DECIMAL(18,2), CHAR(3) \- Lớn hơn 0; SGD  
•      Reason: NVARCHAR(200) \- Optional, chỉ dùng cho Individual; không hiển thị cho Parent; hiển thị ở cột Note của Top-Up History  
•      Status: INT \- 1 Pending, 2 Success, 3 Failed  
•      FailureCode, FailureReason: VARCHAR(50), NVARCHAR(500) \- Đã làm sạch  
•      CreatedAt, UpdatedAt, CompletedAt, RowVersion: DATETIME2(3), ROWVERSION \- UTC; CompletedAt rỗng khi đang xử lý  
•      Giá trị dẫn xuất (không lưu): Top-Up Summary ở SCR-05 tính theo bộ lọc. Total Spending là tổng Amount các giao dịch Success. Successful và Failed là số giao dịch theo Status; với nguồn Bulk Batches đếm theo Outcome của batch item.

#### **Tham chiếu ngoài & Audit Log**

•      R1: Student Profile (họ tên, NRIC, DOB, Citizenship).  
•      R3: liên kết Student–EA.  
•      AuditLog: actor, action, entity, entity\_id, old\_value, new\_value, timestamp. Ghi: tạo, sửa, bật hoặc tắt (Deactive) campaign; Run Campaign; bắt đầu và kết thúc batch; mỗi top-up.

## **5\. Validation**

### **5.1. Thông báo lỗi hiển thị cho HQ User**

| Mã | Nội dung hiển thị | Hành vi UI |
| :---- | :---- | :---- |
| MSG-0201 | No Education Account found. Check the Account Number or NRIC and try again. | Giữ ở SCR-01 |
| MSG-0202 | Enter an amount greater than 0, with up to 2 decimal places. | Giữ ở SCR-02, đánh dấu ô nhập |
| MSG-0203 | The amount is more than the limit for one top-up. (TBC, OQ-01) | Giữ ở SCR-02 hoặc SCR-08 |
| MSG-0204 | This Education Account is not active. Top-up is not allowed. | Vô hiệu ô nhập số tiền |
| MSG-0207 | Top-up completed. Reference: {Reference}. | SCR-04, hiện số dư mới |
| MSG-0208 | The top-up could not be completed. No amount was credited. | SCR-04, cho thử lại |
| MSG-0214 | No accounts match these criteria. | Hiện ở SCR-09 (Preview) hoặc ngay khi bấm Run Campaign ở SCR-07; không tạo batch |
| MSG-0215 | This campaign is running and cannot be changed. | Vô hiệu nút Edit và Run Campaign của campaign đó |
| MSG-0217 | Enter an age range from 7 to 15, with the minimum not more than the maximum. | SCR-08, đánh dấu ô nhập |
| MSG-0218 | Enter a balance operator and an amount of 0 or more. | SCR-08, đánh dấu ô nhập |
| MSG-0222 | This campaign was changed by another user. Refresh and try again. | Làm mới dữ liệu |
| MSG-0001 | Enter your \<field\> | Bỏ trống trường bắt buộc, báo theo từng trường |
| MSG-0002 | Your session has expired. Please log in again. | Chuyển đến đăng nhập Admin Portal |
| MSG-0003 | You do not have permission to perform this action. | Quay về màn hình chính |

### **5.2. Tiêu chí chấp nhận (AC)**

#### **Individual Top-Up**

| ID | Given / When / Then |
| :---- | :---- |
| AC-01 | Given HQ User, when tìm theo Account Number hoặc NRIC đầy đủ, then thấy đúng một EA với holder, status, balance; NRIC hiển thị che một phần. |
| AC-02 | Given Account Number hoặc NRIC không có EA, hoặc NRIC nhập thiếu, thừa ký tự hoặc chỉ khớp một phần, when tìm, then báo MSG-0201, không hiển thị tài khoản hay danh sách gợi ý nào. |
| AC-03 | Given EA Active, when HQ User xác nhận top-up 50.00, then số dư tăng đúng 50.00 một lần, transaction Success, có Reference và audit log. |
| AC-04 | Given EA Closed, when xác nhận top-up, then bị từ chối, số dư không đổi, transaction Failed được ghi log. |
| AC-07 | Given HQ User bấm xác nhận hai lần, then chỉ tạo một transaction (kiểm tra bằng Reference ID) và chỉ ghi có một lần. |
| AC-09 | Given số tiền bằng 0, âm, hoặc có hơn 2 chữ số thập phân, then bị từ chối MSG-0202, không có dữ liệu nào đổi. |
| AC-10 | Given top-up thất bại, then số dư không đổi và lý do được ghi log. |
| AC-11 | Given School User hoặc Parent gọi API Top-Up, then bị từ chối 403 và ghi log bảo mật. |

#### **Cấu hình Campaign, Preview**

| ID | Given / When / Then |
| :---- | :---- |
| AC-18 | Given Campaign Name và số tiền hợp lệ (criterion tùy chọn), when Save, then campaign được tạo ở trạng thái Draft với Code do hệ thống sinh và hiện ở danh sách Bulk Campaigns với Batches Run bằng 0\. |
| AC-19 | Given Minimum Age lớn hơn Maximum Age, hoặc nằm ngoài 7 đến 15, then bị từ chối MSG-0217. |
| AC-20 | Given campaign có criterion tuổi 7 đến 12 và số dư dưới SGD 100, when Preview, then danh sách gồm mọi EA Active thỏa cả hai criterion, kèm Student Name, Age, Balance, Top-Up Amount; tổng số tài khoản và tổng tiền đúng. |
| AC-21 | Given campaign không có criterion nào, when Preview, then danh sách gồm mọi EA Active; học sinh PR hoặc IS không có EA không bao giờ xuất hiện. |
| AC-22 | Given campaign đã lưu, when HQ User bấm Preview, then hiển thị tổng số tài khoản và tổng tiền dự kiến (Total amount) để kiểm tra; Preview không có nút Confirm và không bắt buộc trước khi Run Campaign. |
| AC-23 | Given đã xem Preview, when HQ User sửa criterion hoặc số tiền rồi bấm Run Campaign, then batch dùng định nghĩa mới nhất tại lúc bấm; Preview cũ không chặn việc chạy. |
| AC-24 | Given hai campaign với criterion khác nhau, then cả hai chạy được; tài khoản thuộc cả hai nhận hai khoản và Preview không cảnh báo. |

#### **Chạy và kết quả**

| ID | Given / When / Then |
| :---- | :---- |
| AC-25 | Given campaign Draft hoặc Active, when HQ User bấm Run Campaign, then mỗi tài khoản eligible được ghi có đúng một lần; batch summary có Successful, Failed; số tiền tổng khớp tổng các giao dịch Success. |
| AC-26 | Given giữa lúc lập danh sách và lúc xử lý một tài khoản không còn thỏa criterion đã chọn (ví dụ số dư tăng vượt ngưỡng), then bị Failed (CRITERIA\_NOT\_MATCH), không ghi có; nếu vẫn thỏa thì vẫn được ghi có. |
| AC-27 | Given tài khoản bị đóng trước lúc chạy, then Failed (EA\_NOT\_ACTIVE), không ghi có. |
| AC-28 | Given batch có 5 tài khoản eligible, số tiền mỗi tài khoản 100.00, when kết quả là 3 Successful, 2 Failed, then batch summary hiển thị Total Spending 300.00, Successful 3, Failed 2; các số này được cộng vào Top-Up Summary của campaign. |
| AC-29 | Given một số tài khoản Failed, then batch vẫn xử lý các tài khoản khác và kết thúc ở trạng thái Failed kèm lý do. |
| AC-31 | Given server khởi động lại giữa batch, then batch tiếp tục từ các item chưa xử lý, không ghi có trùng. |
| AC-33 | Given batch item Failed, then số dư EA tương ứng không đổi. |
| AC-34 | Given campaign có batch Running, when HQ User bấm Edit hoặc Run Campaign, hoặc hai HQ User thao tác đồng thời, then bị từ chối MSG-0215 hoặc MSG-0222. |

#### **Run Campaign**

| ID | Given / When / Then |
| :---- | :---- |
| AC-35 | Given campaign Draft hoặc Active không có batch Running và có tài khoản eligible, when HQ User bấm Run Campaign ở danh sách, then batch bắt đầu ngay; không có bước Preview bắt buộc, chọn chế độ chạy, lịch chạy hay xác nhận riêng; campaign Draft chuyển Active. |
| AC-36 | Given HQ User bấm Run Campaign hai lần, hoặc hai HQ User bấm cùng lúc, then chỉ tạo một batch; trong lúc batch Running, Run Campaign và Edit của campaign đó bị vô hiệu (MSG-0215). |
| AC-37 | Given campaign đã có batch kết thúc, when HQ User bấm Run Campaign lần nữa, then tạo batch mới (BatchNo tăng, Batches Run tăng 1), batch cũ giữ nguyên, và Top-Up Summary của campaign cộng dồn cả hai batch. |
| AC-38 | Given không có tài khoản eligible lúc bấm Run Campaign, then báo MSG-0214, không tạo batch, Batches Run không đổi. |

#### **Audit và Parent (R8)**

| ID | Given / When / Then |
| :---- | :---- |
| AC-39 | Given mọi giao dịch Top-Up, then có Reference, số tiền, thời điểm, người thực hiện, campaign và batch (nếu có); không xóa cứng. |
| AC-40 | Given top-up thành công, when Parent xem Transaction History (R8), then thấy Type Top-up, Money in, Status Completed; Description không chứa lý do nội bộ. |

#### **Top-Up Summary khi xem history**

| ID | Given / When / Then |
| :---- | :---- |
| AC-42 | Given Top-Up History đang chọn một nguồn (Individual Top-Ups hoặc Bulk Batches), Status hoặc từ khóa Search, when HQ User bấm Search, then ba thẻ Top-Up Summary hiển thị Total Spending bằng tổng Amount các giao dịch Success trong bộ lọc, cùng số lượng Successful, Failed; đổi bộ lọc thì số liệu đổi theo. |
| AC-43 | Given campaign đã chạy một hoặc nhiều batch, when xem Top-Up Summary của campaign, then Total Spending, Successful, Failed bằng tổng các batch tương ứng ở SCR-11. |
| AC-44 | Given batch item Failed, then số tiền đó không được cộng vào Total Spending; chỉ batch item Successful mới được cộng. |
| AC-45 | Given SCR-05 chọn nguồn Individual Top-Ups, then Total Spending chỉ gồm top-up lẻ Success. |

## **6\. Appendices**

### **Appendix A. Trạng thái Campaign, Batch, Batch Item và Transaction**

| Đối tượng | Từ | Sang | Điều kiện | Ghi chú |
| :---- | :---- | :---- | :---- | :---- |
| Campaign | (mới) | Draft | HQ User Save | Chưa chạy lần nào; Preview, Edit, Run Campaign được |
| Campaign | Draft | Active | HQ User bấm Run Campaign, batch đầu tiên được tạo | Batches Run lớn hơn hoặc bằng 1; vẫn Preview, Edit, Run Campaign được |
| Campaign | Active | Active | HQ User bấm Run Campaign | Tạo batch mới; Edit và Run Campaign bị vô hiệu đến khi batch kết thúc |
| Campaign | Draft hoặc Active | Deactive | HQ User tắt campaign (cách thao tác TBC, OQ-13) | Không chạy được |
| Batch | (mới) | Pending | HQ User bấm Run Campaign | Khóa Edit và Run Campaign của campaign |
| Batch | Pending | Running | Bắt đầu lập danh sách và xử lý |   |
| Batch | Running | Completed | Hết danh sách, không còn batch item Failed | Mở lại Edit và Run Campaign |
| Batch | Running | Failed | Hết danh sách, còn batch item Failed | Kèm lý do; mở lại Edit và Run Campaign |
| Batch Item | (mới) | Pending | Lập danh sách khi batch bắt đầu |   |
| Batch Item | Pending | Successful | Ghi có vào EA thành công | Số dư tăng một lần |
| Batch Item | Pending | Failed | Lỗi xử lý hoặc kiểm tra; không còn đủ điều kiện khi chạy | Số dư không đổi; có Failure Code |
| Transaction | (mới) | Pending | HQ User xác nhận, hoặc batch item bắt đầu ghi có | Có Reference ID |
| Transaction | Pending | Success | Ghi có vào EA thành công | Số dư tăng một lần |
| Transaction | Pending | Failed | Không đủ điều kiện, hoặc lỗi khi ghi có | Số dư không đổi |

### **Appendix B. Open Questions & Assumptions**

| ID | Câu hỏi | Ảnh hưởng | Phương án tạm trong FS |
| :---- | :---- | :---- | :---- |
| OQ-01 | Hạn mức tối đa mỗi lần top-up lẻ và mỗi tài khoản trong bulk | BR-F2-03, BR-F2-19, MSG-0203 | Chưa đặt hạn mức; cấu hình được |
| OQ-03 | Có cần phê duyệt hai bước (maker-checker) cho campaign | OOS \#6 | Không; HQ User bấm Run Campaign một bước, có audit |
| OQ-08 | Description của top-up hiển thị cho Parent: tên campaign hay "MOE Top-up" chung | AC-40 | "MOE Top-up" chung |
| OQ-09 | Tài khoản thỏa nhiều campaign, hoặc nhiều batch của cùng campaign: cho nhận nhiều khoản hay chặn | BR-F2-25 | Cho phép; Preview không cảnh báo |
| OQ-13 | Trạng thái Deactive: HQ User tắt và bật lại bằng thao tác nào. UI mockup đang dùng nhãn Archived (Archived, Active, Draft) và hiện nút Run Campaign cả ở dòng Draft, Archived | BR-F2-18, BR-F2-20, SCR-07 | Deactive không chạy được; cần bổ sung thao tác tắt, bật trên UI |
| OQ-14 | Top-Up History trên UI mockup hiện NRIC đầy đủ, trong khi BR-F2-02 yêu cầu che một phần | SCR-05 | FS giữ che một phần; cần chốt với UI hoặc client |
| OQ-15 | Bố cục xem Bulk Batches (danh sách batch, Top-Up Summary theo campaign và batch) chưa có trong UI | BR-F2-07, SCR-11, SCR-12 | Theo mô tả ở 4.1; chờ UI |
| OQ-16 | Có cần hộp thoại xác nhận ngắn trước khi chạy batch (thao tác ghi có hàng loạt) | DA-09, BR-F2-21 | Không; bấm Run Campaign chạy ngay, chỉ có chống bấm đúp |
| OQ-17 | Các criterion đã chọn (Age Range, Account Balance) kết hợp bằng AND hay OR | DA-07, BR-F2-14 | AND: thỏa tất cả criterion đã chọn |

### **Appendix C. Danh sách màn hình**

| Mã | Màn hình | Thành phần chính | Hành động | Trạng thái UI |
| :---- | :---- | :---- | :---- | :---- |
| SCR-01 | Individual Top-Up: Tìm EA (tab Individual Top-Up) | Chọn kiểu tìm, ô nhập Account Number hoặc NRIC | Search | Loading, Empty (không có kết quả), Error |
| SCR-02 | Xác minh chủ tài khoản và nhập số tiền | Tên, NRIC che một phần, tuổi, Account Number, Account Status, Current Balance, ô Top-Up Amount, Reason (không bắt buộc) | Continue, quay lại | Ô nhập bị vô hiệu khi EA không Active |
| SCR-03 | Xem lại và xác nhận | Chủ tài khoản, số tiền, số dư sau top-up, lý do (nếu có) | Xác nhận, hủy | Nút xác nhận bị vô hiệu sau khi bấm; Processing |
| SCR-04 | Kết quả top-up | Trạng thái, Reference, số dư mới, thông báo | Về SCR-01, xem Top-Up History | Success, Failed |
| SCR-05 | Top-Up History (tab Top-Up History) | Ba thẻ Top-Up Summary (Total Spending, Successful, Failed), Filter by Source (Individual Top-Ups, Bulk Batches), Search theo tên học sinh, Status, bảng giao dịch (Date / Time, Reference, Student, Account, Amount, Status, Note) | Search, Reset, sắp xếp Date / Time và Amount | Loading, Empty, Error |
| SCR-07 | Bulk Campaigns (tab Bulk Campaigns) | Search, Status, bảng campaign (Campaign Code, Campaign Name, Amount Per Account (SGD), Batches Run, Status, Actions) | Create Campaign, Search, Reset, Preview, Edit, Run Campaign | Loading, Empty |
| SCR-08 | Cấu hình Campaign (tạo mới và sửa) | Campaign Name, criterion tùy chọn (Age Range, Account Balance), Top-Up Amount per account | Save, hủy | Draft; lỗi từng trường |
| SCR-09 | Preview | Danh sách eligible (Student Name, Age, Balance, Top-Up Amount), tổng số tài khoản, tổng tiền dự kiến, thời điểm preview | Quay lại danh sách | Empty (MSG-0214) |
| SCR-11 | Danh sách Batch (Top-Up History, nguồn Bulk Batches; OQ-15) | Bảng batch: trạng thái, số liệu | Mở batch | Pending, Running, Completed, Failed |
| SCR-12 | Batch summary và Batch Item | Total Spending, Successful, Failed (số lượng và tiền), bảng batch item, bộ lọc Outcome | Export CSV | Loading, Empty, Error |

 

# **R2 (v1)**

# **FS Function 2 \- Top-Up Management**

## **1\. Introduction**

### **1.1. Preface**

Tài liệu này là Functional Specification (FS) cho Function 2 (R2) – Top-Up Management trên Admin Portal của hệ thống Education Account & FAS (MOE Singapore). Function 2 cho phép MOE HQ User nạp tiền vào Education Account (EA) theo hai cách: nạp lẻ cho từng chủ tài khoản (Individual Top-Up), hoặc nạp hàng loạt theo campaign với rule cấu hình theo độ tuổi, số dư và tình trạng đi học (Bulk Top-Up). Campaign chạy ad-hoc hoặc định kỳ. Top-up nhầm được sửa bằng bút toán hiệu chỉnh.  
Function 2 chỉ ra lệnh ghi có (credit). Số dư và sổ cái EA thuộc Function 1; mục 2.2 nêu các điểm nối với R1, R3, R8, R9.

### **1.2. Personas**

| Persona | Loại | Vai trò trong Function 2 |
| :---- | :---- | :---- |
| **MOE HQ User** | Primary actor | Nạp lẻ; tạo và cấu hình campaign; xem preview; xác nhận chạy; xem kết quả run; sửa top-up nhầm |
| **School User** | Không phải actor | Không có quyền Top-Up, không thấy menu Top-Up |
| **Parent** | Gián tiếp | Thấy giao dịch Top-up trong Transaction History (R8); có thể nhận thông báo (xem F2.8) |
| **Admin Portal System** | Hệ thống | Kiểm tra điều kiện, tính danh sách eligible, lập lịch, chạy batch, ghi log và audit |

### **1.3. Design Assumptions and Limitations**

### **Design Assumptions:**

| ID | Assumption |
| :---- | :---- |
| **DA-01** | Top-up là ghi có vào EA trong sổ cái Function 1\.  |
| **DA-02** | Function 2 ghi có và ghi nợ hiệu chỉnh trực tiếp vào số dư EA, đồng thời thêm một bút toán vào sổ cái, trong cùng một database transaction. |
| **DA-03** | Chỉ MOE HQ User dùng được Function 2\. School User và Parent không có quyền |
| **DA-04** | Chỉ EA có trạng thái Active mới nhận top-up.  |
| **DA-05** | Mọi lần ghi có (top-up lẻ, từng dòng trong batch, hiệu chỉnh) đều chạy Closure Eligibility Check của F02 trước khi thực hiện |
| **DA-06** | Preview chỉ mang tính tham khảo. Khi chạy, hệ thống đánh giá lại từng tài khoản bằng dữ liệu tại thời điểm đó |
| **DA-07** | Các criterion của campaign kết hợp bằng AND. Mỗi tài khoản eligible nhận một số tiền cố định |
| **DA-08** | Một campaign thuộc một Academic Year và một Round. Cùng một kỳ có thể chạy nhiều campaign với criterion và số tiền khác nhau |
| **DA-09** | Campaign chạy theo một trong hai chế độ: ad-hoc (chạy ngay hoặc vào một thời điểm HQ User chọn) hoặc định kỳ (hệ thống tự chạy theo lịch) |
| **DA-10** | Sổ cái chỉ thêm mới. "Sửa" một top-up nhầm nghĩa là ghi một bút toán hiệu chỉnh mới; bút toán gốc không bị sửa hay xóa |
| **DA-11** | Mỗi lần ghi có tạo một top-up transaction với FundingReference riêng, và kiểm tra idempotency key để không phát sinh hai giao dịch trùng |
| **DA-12** | Tiền tệ SGD, 2 chữ số thập phân. Ngày hiển thị DD/MM/YYYY theo giờ Singapore (SGT, UTC+8); lưu UTC |

#### **Limitations:**

* Sửa top-up nhầm chỉ áp dụng cho top-up lẻ. Sửa từng giao dịch trong batch chưa nằm trong phạm vi.  
* Function 2 chỉ được coi là đạt khi cả nạp lẻ, nạp hàng loạt (ad-hoc và định kỳ) và sửa top-up nhầm chạy đúng tiêu chí chấp nhận.

### **1.4. Definitions, Acronyms and Abbreviations**

| Thuật ngữ | Giải thích |
| :---- | :---- |
| **EA** | Education Account. Tài khoản chi tiêu cho giáo dục của Singapore Citizen từ 7 đến dưới 16 tuổi. Số dư và sổ cái ở Function 1 |
| **Top-Up** | Giao dịch ghi có một số tiền SGD vào EA |
| **Individual Top-Up** | Top-up lẻ cho một EA do HQ User tìm và nhập số tiền |
| **Bulk Top-Up** | Top-up cho nhiều EA cùng lúc theo criterion của một campaign |
| **Campaign** | Định nghĩa một đợt bulk top-up: Academic Year, Round, criterion, số tiền, ngân sách, chế độ chạy |
| **Round** | Số thứ tự đợt top-up trong một Academic Year (1, 2, 3...) |
| **Criterion** | Một điều kiện lọc của campaign: tuổi, số dư, tình trạng đi học. Các criterion kết hợp bằng AND |
| **Campaign Eligibility Date** | Ngày dùng làm mốc tính tuổi và tình trạng đi học |
| **Run** | Một lần thực thi campaign. Campaign ad-hoc có một run; campaign định kỳ có nhiều run |
| **Run Item** | Kết quả xử lý của một EA trong một run |
| **Preview** | Danh sách tài khoản dự kiến eligible, kèm tổng số và tổng tiền, xem trước khi chạy |
| **Budget Limit** | Tổng số tiền tối đa một run được phép ghi có |
| **Actively Enrolled** | Học sinh có enrollment còn hiệu lực trong Academic Year mục tiêu  |
| **Successful / Skipped / Failed** | Ba nhóm kết quả của Run Item: nạp thành công / bỏ qua do không đủ điều kiện / lỗi xử lý |
| **Funding reference** | Mã tham chiếu duy nhất của một lần ghi có, gửi sang Function 1 để chống ghi trùng và đối soát |
| **Idempotency key** | Khóa đảm bảo một yêu cầu chỉ được xử lý một lần dù bị gửi lại; duy nhất theo HQ User |
| **Correction** | Bút toán ghi nợ hiệu chỉnh dùng để sửa một top-up lẻ nạp nhầm |
| **Reconciliation** | Đối soát khi kết quả ghi có chưa rõ. ReconciliationRequired là trạng thái cần bộ phận vận hành xử lý |
| **Ledger** | Sổ ghi giao dịch EA, chỉ thêm mới, thuộc Function 1 |
| **SGD** | Singapore dollar |

### **1.5. Exclusions**

FS này không đặc tả:

* Nguồn ngân sách, phê duyệt tài chính nội bộ MOE và hạch toán kế toán.  
* Tạo và đóng EA, Closure Eligibility Check (R1). Function 2 chỉ gọi.  
* Số dư, sổ cái và việc triển khai API ghi có, ghi nợ của Function 1\. FS chỉ mô tả cách Function 2 gọi các API này.  
* Enrollment, Academic Year, liên kết Student–EA (R3). Function 2 chỉ đọc.  
* Hiển thị Transaction History cho Parent (R8) và thanh toán phí bằng EA (R9). Chỉ mô tả điểm nối ở mục 2.2.  
* Áp trợ cấp FAS (R4).  
* Xác thực và phân quyền Admin Portal.

### **1.6. OOS List**

| \# | Hạng mục ngoài phạm vi | Lý do / nguồn | Dự kiến |
| :---- | :---- | :---- | :---- |
| **1** | Số tiền khác nhau theo từng tài khoản (theo bậc tuổi, cấp học) | Requirement chỉ nêu số tiền cố định mỗi tài khoản; muốn nhiều mức thì tạo nhiều campaign | Chưa xếp lịch |
| **2** | Criterion bổ sung (School, Academic Level, FAS tier) | Requirement ghi "etc."; mô hình criterion được thiết kế mở rộng nhưng bản này chỉ có tuổi, số dư, tình trạng đi học | Chưa xếp lịch |
| **3** | Nhập danh sách tài khoản bằng file CSV | Không có trong requirement | Chưa xếp lịch |
| **4** | Sửa từng giao dịch trong batch, hoặc hoàn tác cả một run | Feature list chỉ nêu sửa top-up thủ công (OQ-07) | Sau khi client chốt |
| **5** | Top-up cho EA Closed, chuyển số dư sang CPF | CPF Transfer chưa triển khai ở R1 | Cùng CPF Transfer |
| **6** | Phê duyệt hai bước (maker-checker) | Chưa có trong requirement (OQ-04) | Chưa xếp lịch |
| **7** | Dashboard phân tích mức dùng ngân sách nhiều campaign | Không có trong requirement; bản này chỉ có tổng kết từng run và export | Chưa xếp lịch |
| **8** | SMS và thông báo trong ứng dụng cho Parent | FS-08 đã bỏ chuông thông báo khỏi phạm vi | Chưa xếp lịch |

## **2\. System Process and Function Overview**

### **2.1. Process Flow Diagrams**

#### **Individual Top-Up Flow**

HQ User tìm một EA, kiểm tra thông tin chủ tài khoản, nhập số tiền và xác nhận. Hệ thống chạy Closure Eligibility Check trước khi ghi có. Chỉ EA Active mới nhận tiền; thất bại không làm đổi số dư.  
![][image1]

#### 

#### **Bulk Top-Up Flow – Campaign Setup, Preview and Launch**

HQ User cấu hình campaign, xem preview, sửa cho đến khi nằm trong ngân sách, rồi chọn chạy ngay, chạy vào một thời điểm hoặc kích hoạt chạy định kỳ. Sửa criterion, số tiền hoặc ngân sách sau khi preview thì campaign quay về Draft và phải preview lại.  
![][image2]  
![][image3]

#### **Top-Up Correction Flow**

HQ User chọn một top-up lẻ đã thành công và sửa bằng bút toán ghi nợ hiệu chỉnh: giảm số tiền hoặc rút lại hoàn toàn bộ. Bút toán gốc giữ nguyên; thất bại thì không có gì thay đổi.  
![][image4]

### **2.2. Liên kết với các requirement khác**

| Requirement | Function 2 dùng / cung cấp | Quy tắc nối |
| :---- | :---- | :---- |
| **R1 – F02 (đóng EA)** | Gọi: Closure Eligibility Check trước mỗi lần ghi có | EA Closed, Closure Deferred, Eligibility Review Required, hoặc Government API không phản hồi: không ghi có (F02-AC04, EF01). EA đủ 16 tuổi chưa Closed: F02 chạy closure trước, rồi top-up bị từ chối |
| **R3 – Enrollment** | Dùng: student\_school\_enrollments (enrolled\_from, enrolled\_to\_exclusive, status) để xác định Actively Enrolled | Học sinh Actively Enrolled khi có enrollment ENROLLED còn hiệu lực tại Eligibility Date và giao với Academic Year của campaign |
| **R3 – Academic Year** | Dùng: academic\_years (year\_number, start\_date, end\_date\_exclusive, status) | Campaign chỉ gắn với Academic Year có status DRAFT hoặc ACTIVE, không gắn với CLOSED (OQ-06) |
| **R3 – F08 (liên kết Student–EA)** | Dùng: liên kết giữa Student của R3 và EA | Chỉ Student SC có EA; Student PR hoặc IS không có EA nên không bao giờ eligible. Từ EA tìm Student của R3 qua liên kết này để lấy enrollment |
| **R4 – FAS** | Không có phụ thuộc trực tiếp | Số tiền top-up không phụ thuộc FAS. Mô hình criterion cho phép thêm criterion FAS sau này |
| **R8 – Parent Portal** | Cung cấp: giao dịch Top-up trong Transaction History (FR-08.2) | Top-up thành công hiện Type Top-up, Money in, Status Completed, Amount có dấu cộng. Sửa top-up hiện Type Top-up, Money out. Description chỉ ghi "MOE Top-up" hoặc tên campaign; không hiện lý do hoặc ghi chú nội bộ của HQ User. Số dư Home và Education Account tăng ngay sau khi ghi có thành công |
| **R9 – thanh toán bằng EA** | Dùng chung Function 1 | Số dư khả dụng dùng cho thanh toán là số dư sau top-up. Top-up (ghi có), thanh toán (ghi nợ) và sửa top-up (ghi nợ) đều đi qua sổ cái Function 1, nên được tuần tự hóa ở đó; Function 2 không khóa số dư. Sửa top-up không được làm số dư âm, nên có thể bị từ chối nếu tiền đã dùng để trả phí. Function 1 cần API ghi có và ghi nợ idempotent theo FundingReference, cùng nhu cầu với NQ-15 của R9 |

## **3\. Detailed Functions and Solution Design**

### **3.1.1. Function Description**

Function 2 cho MOE HQ User nạp tiền vào EA theo hai cách: nạp lẻ cho một chủ tài khoản, hoặc nạp hàng loạt theo campaign. Campaign gồm Academic Year, Round, các criterion (tuổi, số dư, tình trạng đi học), số tiền cố định mỗi tài khoản và ngân sách; campaign chạy ad-hoc hoặc định kỳ. Mỗi lần ghi có đi qua Closure Eligibility Check và API ghi có của Function 1\. Top-up lẻ nạp nhầm được sửa bằng bút toán ghi nợ hiệu chỉnh.

| Mục | Nội dung |
| :---- | :---- |
| **Function ID** | F2 (R2) |
| **Portal** | Admin Portal |
| **Actor chính** | MOE HQ User |
| **Precondition** | HQ User đã đăng nhập Admin Portal và có quyền Top-Up; EA đã được tạo (R1). Với bulk: Academic Year đã tồn tại (R3) |
| **Postcondition (thành công)** | Mỗi lần ghi có thành công có một bút toán ghi có ở Function 1, số dư EA tăng đúng một lần; có top-up transaction với Transaction Reference; có audit log. Với bulk: có run summary Successful, Skipped, Failed |
| **Postcondition (thất bại)** | Top-up transaction \= Failed; số dư EA không đổi; lý do được ghi log. Với bulk: các tài khoản khác trong run vẫn được xử lý |
| **Postcondition (đang chạy)** | Run \= Running; campaign không sửa được; không mở thêm run cho cùng campaign |
| **Postcondition (cần xử lý tay)** | Giao dịch hoặc run item \= ReconciliationRequired khi không xác định được kết quả ghi có; bộ phận vận hành xử lý; hệ thống không tự đoán là đã ghi hay chưa |

#### **Sub-functions:**

| ID | Sub-function | Mục đích |
| ----- | ----- | ----- |
| F2.1 | Search and Verify EA Account Holder | Tìm kiếm tài khoản EA theo Account Number hoặc Student NRIC; hiển thị thông tin chủ tài khoản, trạng thái tài khoản và số dư hiện tại để xác minh trước khi nạp tiền. |
| F2.2 | Individual Top-Up | Thực hiện nạp tiền cho một tài khoản EA cụ thể; nhập số tiền, xác nhận giao dịch, kiểm tra điều kiện hợp lệ, ghi có vào EA thông qua Function 1 và hiển thị kết quả. |
| F2.3 | Top-Up History and Correction | Tra cứu lịch sử top-up và xử lý các giao dịch nạp nhầm bằng bút toán điều chỉnh ghi nợ, có kiểm tra điều kiện và lưu vết kiểm toán. |
| F2.4 | Top-Up Campaign Configuration | Tạo và cấu hình chiến dịch top-up theo Academic Year, Round, tiêu chí đối tượng thụ hưởng, số tiền nạp, ngân sách và chế độ thực thi. |
| F2.5 | Eligibility Preview and Budget Validation | Xác định danh sách tài khoản đủ điều kiện theo các tiêu chí đã cấu hình; hiển thị số lượng tài khoản, tổng số tiền dự kiến, kiểm tra giới hạn ngân sách và cho phép xem lại preview khi cấu hình thay đổi. |
| F2.6 | Top-Up Run Scheduling and Control | Thiết lập cách thức và thời điểm chạy top-up: chạy ngay, chạy một lần theo lịch hoặc chạy định kỳ; hỗ trợ tạm dừng, hủy lịch hoặc dừng chiến dịch theo các quy tắc được phép. |
| F2.7 | Top-Up Execution and Run Monitoring | Thực thi top-up theo danh sách đã xác nhận; kiểm tra lại điều kiện từng tài khoản trước khi ghi có; tổng hợp kết quả thành công/thất bại, hỗ trợ thử lại các tài khoản thất bại, xuất báo cáo và lưu audit log. |
| F2.8 | Parent Notification | Gửi thông báo cho Parent/Guardian sau khi giao dịch top-up thành công, không làm gián đoạn quá trình thực thi top-up. |

#### **Business Rules:**

**Nhóm A – Quyền và Individual Top-Up (F2.1, F2.2)**

| ID | Rule |
| :---- | :---- |
| **BR-F2-01** | Chỉ MOE HQ User có quyền Top-Up. Mọi API kiểm tra quyền ở server; School User và Parent bị từ chối |
| **BR-F2-02** | Tìm EA theo khớp chính xác Account Number hoặc NRIC đầy đủ của học sinh; không tìm gần đúng. Kết quả hiển thị NRIC che một phần |
| **BR-F2-03** | Số tiền top-up lớn hơn 0, tối đa 2 chữ số thập phân, không vượt hạn mức mỗi lần (TBC, OQ-03). Lý do (reason) bắt buộc, tối đa 200 ký tự |
| **BR-F2-04** | Chỉ EA Active nhận top-up. Trước khi ghi có, hệ thống chạy Closure Eligibility Check của F02. EA Closed, Closure Deferred, Eligibility Review Required hoặc Government API không phản hồi: từ chối, không ghi có, số dư không đổi |
| **BR-F2-05** | Mỗi lần ghi có chỉ xảy ra một lần: idempotency key duy nhất theo HQ User, nút xác nhận bị vô hiệu sau khi bấm, mỗi lần ghi có có FundingReference riêng |
| **BR-F2-06** | Giao dịch thất bại không làm đổi số dư nhưng vẫn được ghi log (thời điểm, người thực hiện, lý do) |

**Nhóm B – Sửa top-up nhầm (F2.3)**

| ID | Rule |
| :---- | :---- |
| **BR-F2-08** | Chỉ top-up lẻ có Status Success mới sửa được. Top-up trong batch và giao dịch hiệu chỉnh không sửa được  |
| **BR-F2-09** | Có hai kiểu sửa: giảm số tiền, hoặc hoàn toàn bộ. Cả hai là một giao dịch ghi nợ mới loại Top-Up Correction, liên kết với giao dịch gốc. Giao dịch gốc không bị sửa hay xóa; hiển thị thêm Corrected amount và Effective amount (gốc trừ tổng đã sửa) |
| **BR-F2-10** | Số tiền ghi nợ hiệu chỉnh lớn hơn 0, không vượt Effective amount còn lại của giao dịch gốc và không vượt số dư khả dụng của EA (không để số dư âm). Cho sửa nhiều lần đến khi Effective amount bằng 0 |
| **BR-F2-11** | EA phải Active và qua Closure Eligibility Check. EA Closed: từ chối, vận hành xử lý ngoài hệ thống |
| **BR-F2-12** | Lý do sửa bắt buộc. Audit log ghi giao dịch gốc, Effective amount trước và sau, người sửa, thời điểm. Thời hạn cho phép sửa và việc có cần người duyệt: TBC (OQ-04, OQ-05) |

**Nhóm C – Cấu hình Campaign (F2.4)**

| ID | Rule |
| :---- | :---- |
| **BR-F2-13** | Mỗi campaign thuộc một Academic Year và một Round (số nguyên dương). Campaign Code duy nhất trong cặp (Academic Year, Round). Cùng một kỳ chạy được nhiều campaign với criterion và số tiền khác nhau |
| **BR-F2-14** | Các criterion kết hợp bằng AND. Có ba loại: Age Range (Minimum Age, Maximum Age, bao gồm cả hai đầu), Account Balance (toán tử và ngưỡng SGD), Schooling Status (Actively Enrolled). Campaign cần ít nhất một criterion; criterion không khai báo thì không lọc |
| **BR-F2-15** | Age Range: 7 ≤ Minimum Age ≤ Maximum Age ≤ 15, vì EA chỉ tồn tại từ 7 đến dưới 16 tuổi. Tuổi tính theo số năm tròn tại Campaign Eligibility Date, dùng Leap Year Rule của R1 |
| **BR-F2-16** | Campaign Eligibility Date: với ad-hoc do HQ User chọn (mặc định là ngày chạy); với định kỳ là ngày của từng lần chạy |
| **BR-F2-17** | Budget Limit bắt buộc, lớn hơn 0, áp dụng cho từng run (OQ-02 hỏi có cần hạn mức độ cộng dồn theo campaign hay theo kỳ). Hệ thống chặn ở hai chỗ: lúc xác nhận (tổng tiền preview không vượt Budget Limit) và lúc chạy (dừng ghi có khi số còn lại nhỏ hơn số tiền mỗi tài khoản) |
| **BR-F2-18** | Trạng thái campaign: Draft, Scheduled, Active, Running, Completed, Ended, Cancelled (Appendix A). Chỉ sửa được khi Draft. Sửa campaign đang Scheduled hoặc Active thì quay về Draft, hủy các lần chạy chưa bắt đầu, và phải preview lại rồi xác nhận lại |

**Nhóm D – Preview, lịch chạy và thực thi (F2.5, F2.6, F2.7)**

| ID | Rule |
| :---- | :---- |
| **BR-F2-19** | Preview hiển thị Student Name, Age, Balance, Schooling Status, Top-Up Amount dự kiến của từng tài khoản, cùng tổng số tài khoản, tổng tiền và thời điểm tính preview. Preview chỉ đọc |
| **BR-F2-20** | Chỉ xác nhận được khi preview tính trên đúng phiên bản hiện tại của campaign và tổng tiền không vượt Budget Limit. Sửa criterion, số tiền hoặc ngân sách thì preview cũ mất hiệu lực |
| **BR-F2-21** | Có ba cách chạy: chạy ngay; chạy vào một ngày giờ SGT trong tương lai (một lần); chạy định kỳ với tần suất MONTHLY, QUARTERLY hoặc YEARLY, ngày giờ bắt đầu và ngày kết thúc tùy chọn (lịch cụ thể: TBC, OQ-02). Mỗi lần chạy tạo một run |
| **BR-F2-22** | Mỗi campaign tối đa một run đang mở. Lần chạy định kỳ đến khi run trước còn Running, hoặc scheduler bị lỡ giờ: không tự chạy bù, đánh dấu Missed, cảnh báo vận hành; HQ User có thể chạy ad-hoc nếu cần |
| **BR-F2-23** | Hủy được campaign Scheduled hoặc Active và run Pending. Run đang Running cho phép Stop: hoàn tất đoạn đang xử lý, các tài khoản còn lại ghi Skipped (RUN\_STOPPED), các khoản đã ghi có giữ nguyên |
| **BR-F2-24** | Khi chạy, hệ thống xử lý từng tài khoản theo thứ tự Account Number tăng dần, theo từng đoạn nhỏ: Closure Eligibility Check, EA còn Active, đánh giá lại criterion bằng dữ liệu tại thời điểm đó, kiểm tra ngân sách còn lại, ghi có.  |
| **BR-F2-25** | Trong một run, mỗi tài khoản được ghi có tối đa một lần (duy nhất theo RunId và EA). Giữa các campaign khác nhau, một tài khoản có thể nhận nhiều khoản; preview cảnh báo nếu tài khoản đã nhận top-up từ campaign khác cùng kỳ |
| **BR-F2-26** | Kết quả từng tài khoản: Successful; Skipped kèm Skip Reason (EA\_NOT\_ACTIVE, ELIGIBILITY\_REVIEW\_REQUIRED, AGE\_NOT\_MATCH, BALANCE\_NOT\_MATCH, NOT\_ENROLLED, BUDGET\_EXHAUSTED, RUN\_STOPPED); Failed kèm Failure Code (ví dụ ELIGIBILITY\_CHECK\_UNAVAILABLE, CREDIT\_FAILED). ReconciliationRequired tính trong nhóm Failed và có cờ riêng |
| **BR-F2-27** | Mỗi run item có FundingReference cố định, sinh một lần. Thử lại dùng đúng FundingReference đó, nên Function 1 không ghi trùng |
| **BR-F2-28** | Thử lại: HQ User thử lại các run item Failed (không gồm ReconciliationRequired và Skipped). Thử lại vẫn đi qua mọi kiểm tra và vẫn bị giới hạn bởi ngân sách còn lại |
| **BR-F2-29** | Run summary hiển thị tổng Successful, Skipped, Failed (số tài khoản và số tiền), số ReconciliationRequired, ngân sách đã dùng và còn lại; lọc theo kết quả; export CSV. Trạng thái run: Completed khi không có Failed, CompletedWithErrors khi còn Failed |
| **BR-F2-30** | Audit lưu vĩnh viễn: Transaction Reference, số tiền, thời điểm, người thực hiện (HQ User, hoặc "System" kèm HQ User đã kích hoạt campaign), campaign, run. Không xóa cứng campaign, run, run item và giao dịch |

**Nhóm E – Thông báo (F2.8)**

| ID | Rule |
| :---- | :---- |
| **BR-F2-31** | Sau mỗi top-up thành công, hệ thống đưa sự kiện vào hàng đợi để gửi cho các Parent liên kết qua Father NRIC hoặc Mother NRIC và đã có email trong Parent\_Profile. Nội dung gồm số tiền, ngày và số EA che một phần; không gồm lý do hay ghi chú nội bộ |
| **BR-F2-32** | Gửi thông báo lỗi hoặc Parent chưa có hồ sơ thì không ảnh hưởng top-up. |

### **3.1.2. Process Flow Description and Screens**

#### **Bước 1\. Tìm EA và xác minh chủ tài khoản (F2.1)**

* HQ User vào menu Top-Up, chọn Individual Top-Up (SCR-01).  
* HQ User nhập Account Number hoặc NRIC đầy đủ của học sinh và chọn Search.  
* Hệ thống tìm EA theo khớp chính xác (BR-F2-02) và hiển thị SCR-02: tên học sinh, NRIC che một phần, tuổi, Account Number, Account Status, Current Balance.

*Luồng thay thế:* không tìm thấy thì báo MSG-0201; EA không Active vẫn hiển thị để tra cứu nhưng không cho nhập số tiền, kèm lý do (MSG-0204).

#### **Bước 2\. Nhập số tiền và xác nhận (F2.2)**

* Trên SCR-02, HQ User nhập Top-Up Amount và Reason rồi chọn Continue.  
* Hệ thống kiểm tra định dạng và hạn mức (BR-F2-03), rồi hiển thị SCR-03 để xem lại: chủ tài khoản, Account Number, số dư hiện tại, số tiền, số dư sau top-up (tham khảo), lý do.  
* HQ User xác nhận. Nút xác nhận bị vô hiệu ngay sau lần bấm đầu; client gửi kèm idempotency key.

#### **Bước 3\. Kiểm tra và ghi có (F2.2)**

* Hệ thống tạo top-up transaction (Pending) với Transaction Reference và FundingReference, rồi chạy Closure Eligibility Check của F02.  
* Không đủ điều kiện (EA Closed, Closure Deferred, Eligibility Review Required, Government API không phản hồi): transaction Failed, số dư không đổi, hiển thị SCR-04 với thông báo tương ứng.  
* Đủ điều kiện: gọi Function 1 ghi có (nguyên tử, idempotent theo FundingReference).  
  * *Thành công:* transaction Success, lưu mã bút toán của Function 1, ghi audit log, đưa sự kiện vào hàng đợi email (F2.8), hiển thị SCR-04 kèm Transaction Reference và số dư mới (MSG-0207).  
  * *Thất bại:* transaction Failed, số dư không đổi (MSG-0208).  
  * *Không rõ kết quả:* hỏi lại Function 1 bằng cùng FundingReference; vẫn không rõ thì ReconciliationRequired, hiển thị trạng thái đang xác minh (MSG-0209).

#### **Bước 4\. Xem Top-Up History và sửa top-up nhầm (F2.3)**

* HQ User mở Top-Up History (SCR-05): danh sách mọi top-up (lẻ và từ batch) theo thời gian mới nhất trước, lọc theo Account Number, NRIC, khoảng ngày, nguồn (Individual, Bulk), trạng thái.  
* HQ User chọn một top-up lẻ Success và chọn Correct. Hệ thống mở SCR-06: giao dịch gốc, Effective amount còn lại, kiểu sửa (Reduce amount hoặc Reverse in full), số tiền ghi nợ, Reason.  
* Hệ thống kiểm tra (BR-F2-08 đến BR-F2-12), chạy Closure Eligibility Check rồi gọi Function 1 ghi nợ hiệu chỉnh (idempotent theo FundingReference).  
  * *Thành công:* tạo giao dịch Top-Up Correction, giao dịch gốc hiện Corrected amount và Effective amount mới (MSG-0210).  
  * *Số dư không đủ hoặc lỗi:* không có gì thay đổi (MSG-0211, MSG-0208).

#### **Bước 5\. Tạo và cấu hình Campaign (F2.4)**

* HQ User vào Top-Up, chọn Bulk Top-Up Campaigns (SCR-07), chọn Create.  
* Trên SCR-08, HQ User nhập Campaign Name, chọn Academic Year và Round, thêm criterion (Age Range, Account Balance, Schooling Status), nhập Top-Up Amount và Budget Limit, rồi Save. Eligibility Date cho ad-hoc chọn ở bước 7\.  
* Hệ thống kiểm tra theo BR-F2-13 đến BR-F2-20 và lưu campaign ở trạng thái Draft.

#### **Bước 6\. Preview và xác nhận (F2.5)**

* HQ User chọn Preview. Hệ thống đánh giá criterion trên các EA Active và hiển thị SCR-09: danh sách eligible (Student Name, Age, Balance, Schooling Status, Top-Up Amount), tổng số tài khoản, tổng tiền, Budget Limit, thời điểm tính preview, cảnh báo tài khoản đã nhận top-up từ campaign khác cùng kỳ.  
* Tổng tiền vượt Budget Limit: nút Confirm bị vô hiệu, hiển thị số tiền vượt (MSG-0213). HQ User sửa campaign (quay về Draft) rồi preview lại.  
* Không có tài khoản eligible: hiển thị MSG-0214, không xác nhận được.  
* Đạt điều kiện: HQ User chọn Confirm và sang bước 7\.

#### **Bước 7\. Chọn chế độ chạy (F2.6)**

* Trên SCR-10, HQ User chọn một trong ba cách: Run now, Run at date and time (một lần, giờ SGT, trong tương lai), hoặc Recurring (tần suất, ngày giờ bắt đầu, ngày kết thúc tùy chọn).  
* Với ad-hoc, HQ User chọn Eligibility Date (mặc định là ngày chạy); với định kỳ, mỗi lần chạy dùng ngày chạy làm Eligibility Date.  
* Hệ thống đổi campaign sang Running (chạy ngay), Scheduled (chạy một lần vào giờ đã chọn) hoặc Active (định kỳ), và ghi audit log người xác nhận.  
* HQ User có thể Cancel campaign Scheduled hoặc Active, hoặc Stop run đang Running ở SCR-11.

#### **Bước 8\. Thực thi run và nhận kết quả (F2.7)**

* Đến giờ (hoặc ngay lập tức), hệ thống tạo run (Pending, rồi Running), khóa campaign, cố định Eligibility Date và criterion cho run này.  
* Hệ thống xử lý từng tài khoản theo BR-F2-27: kiểm tra, ghi có qua Function 1 với FundingReference của run item, ghi kết quả Successful, Skipped hoặc Failed.  
* HQ User theo dõi tiến độ ở SCR-11 và SCR-12 (số đã xử lý, ngân sách đã dùng).  
* Hết danh sách: run \= Completed (không có Failed) hoặc CompletedWithErrors (còn Failed); hiển thị run summary (BR-F2-32). Với campaign ad-hoc, campaign \= Completed; với định kỳ, campaign về Active chờ lần chạy kế tiếp.

#### **Bước 9\. Thử lại, export và thông báo (F2.7, F2.8)**

* Trên SCR-12, HQ User lọc run item theo kết quả, export CSV, và chọn Retry failed để thử lại các run item Failed (BR-F2-31).  
* Mỗi top-up thành công đưa một sự kiện vào hàng đợi email; Parent thấy giao dịch trong Transaction History của R8 ngay sau khi ghi có.

#### **Trường hợp ngoại lệ:**

| \# | Tình huống | Xử lý |
| :---- | :---- | :---- |
| **EX-01** | School User hoặc Parent gọi API Top-Up, hoặc HQ User sửa ID trong request để thao tác trên campaign hay giao dịch không thuộc quyền | Server kiểm tra quyền cho mọi request, trả 403, không lộ dữ liệu, ghi log bảo mật (MSG-0003) |
| **EX-02** | EA chuyển sang Closed, hoặc học sinh đủ 16 tuổi, giữa lúc HQ User xem và lúc xác nhận | Closure Eligibility Check chạy khi xác nhận; F02 đóng EA nếu cần; top-up bị từ chối, số dư không đổi (MSG-0204) |
| **EX-03** | Government API không phản hồi khi kiểm tra đóng EA | Không ghi có; individual: hiển thị lỗi, cho thử lại; bulk: run item Failed (ELIGIBILITY\_CHECK\_UNAVAILABLE), có thể thử lại. Không tự đổi Account Status |
| **EX-04** | Bấm xác nhận hai lần, hoặc client gửi lại cùng idempotency key | Chỉ tạo một transaction và ghi có một lần; lần gửi lại nhận kết quả của transaction đầu |
| **EX-05** | Function 1 timeout hoặc lỗi mạng sau khi gửi lệnh ghi có | Giữ Pending, hỏi lại Function 1 bằng cùng FundingReference; nếu đã ghi thì đánh Success, nếu chưa thì cho Failed; vẫn không xác định thì ReconciliationRequired, cảnh báo vận hành. Không tự thử vô hạn |
| **EX-06** | Session Admin Portal hết hạn khi đang thao tác | Hết hạn trước khi xác nhận: yêu cầu đăng nhập lại, chưa có transaction. Hết hạn sau khi xác nhận: transaction vẫn được xử lý; HQ User đăng nhập lại thấy trạng thái hiện tại (MSG-0002) |
| **EX-07** | HQ User sửa criterion, số tiền hoặc ngân sách sau khi đã preview hoặc đã Confirm | Campaign về Draft; các lần chạy chưa bắt đầu bị hủy; phải preview và xác nhận lại (BR-F2-21, BR-F2-23) |
| **EX-08** | Hai HQ User sửa hoặc hủy cùng một campaign đồng thời; hoặc sửa campaign đang Running | Dùng row version để phát hiện xung đột, người sau nhận yêu cầu làm mới. Campaign đang Running không sửa được (MSG-0215) |
| **EX-09** | Giữa preview và lúc chạy, một tài khoản đổi số dư, bị đóng, hoặc học sinh không còn học | Đánh giá lại khi chạy: tài khoản không còn đủ điều kiện bị Skipped với Skip Reason tương ứng; danh sách thực tế có thể khác preview |
| **EX-10** | Ngân sách hết giữa chừng | Các tài khoản còn lại Skipped (BUDGET\_EXHAUSTED), run vẫn hoàn tất với số liệu đã dùng |
| **EX-11** | Job bị dừng đột ngột hoặc server khởi động lại giữa run | Run tiếp tục từ các run item chưa xử lý. Item đã gửi lệnh sang Function 1 mà chưa ghi kết quả được hỏi lại bằng FundingReference; không ghi có hai lần |
| **EX-12** | Lần chạy định kỳ đến khi run trước còn Running, hoặc scheduler bị lỡ giờ | Không chạy bù tự động; đánh dấu Missed, cảnh báo vận hành (BR-F2-25) |
| **EX-13** | Academic Year của campaign chuyển sang CLOSED hoặc quá ngày kết thúc của campaign định kỳ | Campaign chuyển Ended, không tạo run mới, cảnh báo HQ User |
| **EX-14** | Sửa top-up khi số dư EA nhỏ hơn số tiền cần ghi nợ (tiền đã dùng trả phí) | Từ chối, không đổi dữ liệu (MSG-0211); xử lý tiếp do vận hành, ngoài phạm vi (OQ-05) |
| **EX-15** | Sửa top-up khi EA đã Closed, hoặc giao dịch đã sửa hết | Từ chối (MSG-0212) |
| **EX-16** | Gửi email thất bại, hoặc Parent chưa đăng nhập lần nào nên chưa có email | Bỏ qua hoặc thử lại theo hàng đợi; không ảnh hưởng top-up, ghi log |

## **4\. Data Fields Table**

### **4.1. Trường hiển thị và nhập trên màn hình**

| Màn hình | Trường | Kiểu | Nguồn | Nhập | Bắt buộc | Quy tắc / ghi chú |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **SCR-01** | Search by | Enum ACCOUNT\_NUMBER, NRIC | HQ User chọn | Có | Có | Khớp chính xác, không tìm gần đúng |
| **SCR-01** | Search value | Text | HQ User nhập | Có | Có | Account Number hoặc NRIC đầy đủ (9 ký tự) |
| **SCR-02** | Student name | Text | Student Profile (R1) | Không | Có |  |
| **SCR-02** | NRIC | Text | Student Profile (R1) | Không | Có | Che một phần, không đưa NRIC đầy đủ vào URL |
| **SCR-02** | Age | Integer | Tính từ DOB | Không | Có | Số năm tròn tại ngày hiện tại |
| **SCR-02** | Account Number | Text | Function 1 | Không | Có |  |
| **SCR-02** | Account Status | Enum Active, Closed | Function 1 | Không | Có | Chỉ Active mới nhập được số tiền |
| **SCR-02** | Current Balance | Decimal(18,2), SGD | Function 1 | Không | Có |  |
| **SCR-02** | Top-Up Amount | Decimal(18,2), SGD | HQ User nhập | Có | Có | Lớn hơn 0; tối đa 2 chữ số thập phân; không vượt hạn mức mỗi lần (TBC) |
| **SCR-02** | Reason | Text, tối đa 200 ký tự | HQ User nhập | Có | Có | Chỉ dùng nội bộ, không hiển thị cho Parent |
| **SCR-03** | Balance after top-up | Decimal(18,2) | Tính | Không | Không | Chỉ để tham khảo |
| **SCR-03** | Idempotency key | Text, tối đa 100 ký tự | Client sinh | Không | Có | Duy nhất theo HQ User; bấm đúp giữ cùng key; thao tác mới dùng key mới |
| **SCR-04** | Transaction Reference | Text, tối đa 50 ký tự | Hệ thống sinh | Không | Có | Duy nhất; định dạng đề xuất TUP-YYYYMMDD-XXXXXX (TBC) |
| **SCR-04** | Transaction Status | Enum Success, Failed, ReconciliationRequired | Transaction | Không | Có | ReconciliationRequired hiển thị là đang xác minh |
| **SCR-04** | New balance | Decimal(18,2) | Function 1 | Không | Không | Chỉ khi Success |
| **SCR-05** | Filter: Account Number, NRIC | Text | HQ User nhập | Có | Không |  |
| **SCR-05** | Filter: From, To | Date | HQ User chọn | Có | Không | DD/MM/YYYY, SGT |
| **SCR-05** | Filter: Source | Enum All, Individual, Bulk, Correction | HQ User chọn | Có | Không |  |
| **SCR-05** | Filter: Status | Enum All, Success, Failed, ReconciliationRequired | HQ User chọn | Có | Không |  |
| **SCR-05** | Cột bảng | Date, Transaction Reference, Student, Account Number, Source, Campaign (nếu bulk), Amount, Corrected amount, Effective amount, Status, Performed by | Transaction | Không | Có | Mới nhất trước, 20 dòng mỗi trang; nút Correct chỉ hiện ở top-up lẻ Success còn Effective amount lớn hơn 0 |
| **SCR-06** | Correction type | Enum REDUCE, REVERSE\_FULL | HQ User chọn | Có | Có |  |
| **SCR-06** | Debit amount | Decimal(18,2) | HQ User nhập; tự điền khi REVERSE\_FULL | Có | Có khi REDUCE | Lớn hơn 0; không vượt Effective amount còn lại và số dư khả dụng |
| **SCR-06** | Reason | Text, tối đa 200 ký tự | HQ User nhập | Có | Có |  |
| **SCR-07** | Cột danh sách | Campaign Code, Name, Academic Year, Round, Amount, Budget Limit, Run mode, Status, Next run | Campaign | Không | Có | Lọc theo Academic Year, Round, Status |
| **SCR-08** | Campaign Name | Text, tối đa 150 ký tự | HQ User nhập | Có | Có |  |
| **SCR-08** | Academic Year | Dropdown | academic\_years (R3) | Có | Có | Chỉ DRAFT hoặc ACTIVE |
| **SCR-08** | Round | Integer | HQ User nhập | Có | Có | Dương; Code duy nhất trong (Academic Year, Round) |
| **SCR-08** | Age Range: Minimum, Maximum Age | Integer | HQ User nhập | Có | Không | 7 ≤ Min ≤ Max ≤ 15; nhập cả hai hoặc không nhập |
| **SCR-08** | Account Balance: operator, threshold | Enum, Decimal(18,2) | HQ User chọn, nhập | Có | Không | Toán tử \<, \<=, \>, \>=, \=; ngưỡng không âm; nhập cả hai hoặc không |
| **SCR-08** | Schooling Status: Actively Enrolled | Checkbox | HQ User chọn | Có | Không | Bật thì chỉ lấy học sinh Actively Enrolled trong Academic Year |
| **SCR-08** | Top-Up Amount per account | Decimal(18,2), SGD | HQ User nhập | Có | Có | Lớn hơn 0; không vượt hạn mức mỗi lần (TBC) |
| **SCR-08** | Budget Limit | Decimal(18,2), SGD | HQ User nhập | Có | Có | Lớn hơn 0; áp dụng cho từng run |
| **SCR-09** | Cột preview | Student Name, Age, Balance, Schooling Status, Top-Up Amount | Tính | Không | Có | 20 dòng mỗi trang |
| **SCR-09** | Total accounts, Total amount, Budget Limit, Remaining budget, Previewed at | Integer, Decimal, Datetime | Tính | Không | Có | Total amount vượt Budget Limit thì vô hiệu nút Confirm |
| **SCR-10** | Run mode | Enum RUN\_NOW, SCHEDULED, RECURRING | HQ User chọn | Có | Có |  |
| **SCR-10** | Eligibility Date | Date | HQ User chọn | Có | Có khi ad-hoc | Mặc định ngày chạy; với RECURRING hệ thống tự gán |
| **SCR-10** | Scheduled at | Datetime SGT | HQ User chọn | Có | Có khi SCHEDULED | Trong tương lai |
| **SCR-10** | Frequency, Start at, End at | Enum, Datetime, Datetime | HQ User chọn | Có | Frequency và Start at bắt buộc khi RECURRING | Frequency: MONTHLY, QUARTERLY, YEARLY (TBC); End at sau Start at |
| **SCR-11** | Cột danh sách run | Run No, Trigger, Eligibility Date, Status, Total, Successful, Skipped, Failed, Total credited, Started at, Completed at | Run | Không | Có |  |
| **SCR-12** | Cột run item | Student, Account Number, Age, Balance, Schooling Status, Amount, Outcome, Skip Reason hoặc Failure Reason, Transaction Reference | Run item | Không | Có | Lọc theo Outcome; nút Export CSV, Retry failed |

### **4.2. Thực thể dữ liệu liên quan**

#### **Campaign (topup\_campaigns)**

* Id: VARCHAR(50) \- PK  
* Code: NVARCHAR(50) \- Duy nhất trong (AcademicYearId, RoundNo)  
* Name: NVARCHAR(150)  
* AcademicYearId: UNIQUEIDENTIFIER \- FK logic tới academic\_years (R3); RoundNo: SMALLINT \- Dương  
* AmountPerAccount, BudgetLimit, CurrencyCode: DECIMAL(18,2), DECIMAL(18,2), CHAR(3) \- Cả hai số tiền lớn hơn 0; mặc định SGD  
* RunMode: INT \- 1 RunNow, 2 Scheduled, 3 Recurring  
* EligibilityDate: DATE \- Bắt buộc khi ad-hoc; rỗng khi Recurring  
* ScheduledAt: DATETIME2(3) \- UTC; bắt buộc khi Scheduled  
* RecurrenceFrequency, RecurrenceStartAt, RecurrenceEndAt, NextRunAt: INT, DATETIME2(3) \- Bắt buộc khi Recurring (End at tùy chọn); UTC  
* Status: INT \- 1 Draft, 2 Scheduled, 3 Active, 4 Running, 5 Completed, 6 Ended, 7 Cancelled  
* DefinitionVersion, PreviewedVersion, PreviewedAt: INT, INT, DATETIME2(3) \- DefinitionVersion tăng mỗi lần sửa; chỉ Confirm được khi PreviewedVersion bằng DefinitionVersion  
* ConfirmedBy, ConfirmedAt: VARCHAR(50), DATETIME2(3) \- IAM ID của HQ User xác nhận  
* CreatedBy, CreatedAt, UpdatedAt, RowVersion: VARCHAR(50), DATETIME2(3), ROWVERSION \- UTC; RowVersion là token kiểm soát đồng thời lạc quan

#### **Criterion (topup\_campaign\_criteria)**

* Id, CampaignId: VARCHAR(50) \- PK, FK Campaign  
* CriterionType: INT \- 1 AGE\_RANGE, 2 BALANCE, 3 SCHOOLING\_STATUS; duy nhất theo (CampaignId, CriterionType). Thêm loại mới không đổi cấu trúc bảng  
* MinAge, MaxAge: SMALLINT \- Bắt buộc khi AGE\_RANGE, cấm ở loại khác; 7 ≤ MinAge ≤ MaxAge ≤ 15  
* BalanceOperator, BalanceThreshold: INT, DECIMAL(18,2) \- Bắt buộc khi BALANCE; 1 LT, 2 LTE, 3 GT, 4 GTE, 5 EQ; ngưỡng không âm  
* RequireActivelyEnrolled: BIT \- Bắt buộc khi SCHOOLING\_STATUS

#### **Run (topup\_campaign\_runs)**

* Id, CampaignId: VARCHAR(50) \- PK, FK Campaign  
* RunNo: INT \- Dương, duy nhất trong campaign  
* TriggerType: INT \- 1 Manual, 2 Scheduled, 3 Recurring  
* TriggeredBy: VARCHAR(50) \- IAM ID của HQ User đã xác nhận campaign  
* EligibilityDate: DATE \- Cố định tại lúc bắt đầu run  
* DefinitionVersion, AmountPerAccount, BudgetLimit: INT, DECIMAL(18,2) \- Snapshot tại lúc bắt đầu; sửa campaign không đổi run đã tạo  
* Status: INT \- 1 Pending, 2 Running, 3 Completed, 4 CompletedWithErrors, 5 Cancelled, 6 Stopped, 7 Missed  
* TotalAccounts, SuccessfulCount, SkippedCount, FailedCount, ReconciliationCount: INT \- Không âm; ReconciliationCount là một phần của FailedCount  
* TotalCredited: DECIMAL(18,2) \- Tổng các khoản Successful; không vượt BudgetLimit  
* StartedAt, CompletedAt, CreatedAt, UpdatedAt, RowVersion: DATETIME2(3), ROWVERSION \- UTC. Index duy nhất trên CampaignId khi Status là Pending hoặc Running (một run mở)

#### **Run Item (topup\_run\_items)**

* Id, RunId: VARCHAR(50) \- PK, FK Run; duy nhất theo (RunId, EducationAccountId)  
* EducationAccountId: UNIQUEIDENTIFIER \- FK logic tới EA (Function 1\)  
* AccountNumber, StudentProfileId: VARCHAR(50), UNIQUEIDENTIFIER \- Tham chiếu hiển thị; NRIC lấy qua Student Profile, không sao chép  
* AgeAtEligibility, BalanceSnapshot, SchoolingStatusSnapshot, ExpectedAmount: SMALLINT, DECIMAL(18,2), INT, DECIMAL(18,2) \- Giá trị lúc lập danh sách và lúc đánh giá; dùng để hiển thị và audit  
* Outcome: INT \- 1 Pending, 2 Successful, 3 Skipped, 4 Failed, 5 ReconciliationRequired  
* SkipReason: VARCHAR(40) \- Bắt buộc khi Skipped  
* FailureCode, FailureReason: VARCHAR(50), NVARCHAR(500) \- Mã lỗi kỹ thuật và nguyên nhân đã làm sạch  
* FundingReference: NVARCHAR(50) \- Duy nhất; sinh một lần, dùng lại khi thử lại  
* TopUpTransactionId: VARCHAR(50) \- FK Transaction; bắt buộc khi Successful  
* ProcessedAt, RowVersion: DATETIME2(3), ROWVERSION \- UTC

#### **Top-Up Transaction (topup\_transactions)**

* Id: VARCHAR(50) \- PK  
* TransactionReference: NVARCHAR(50) \- Duy nhất  
* SourceType: INT \- 1 Individual, 2 Bulk, 3 Correction  
* Direction: INT \- 1 In (ghi có), 2 Out (ghi nợ hiệu chỉnh)  
* EducationAccountId: UNIQUEIDENTIFIER \- FK logic tới EA (Function 1\)  
* RunItemId: VARCHAR(50) \- FK Run Item; bắt buộc khi Bulk, cấm ở loại khác  
* OriginalTransactionId: VARCHAR(50) \- FK Transaction gốc; bắt buộc khi Correction, trỏ tới giao dịch Individual Success  
* InitiatedByUserId: VARCHAR(50) \- IAM ID của HQ User; với Bulk là HQ User đã xác nhận campaign  
* IdempotencyKey: VARCHAR(100) \- Duy nhất theo (InitiatedByUserId, IdempotencyKey); dùng cho Individual và Correction  
* FundingReference: NVARCHAR(50) \- Duy nhất; gửi sang Function 1 để đối soát  
* Amount, CurrencyCode: DECIMAL(18,2), CHAR(3) \- Lớn hơn 0; SGD  
* CorrectionType: INT \- 1 Reduce, 2 ReverseFull; bắt buộc khi Correction  
* Reason: NVARCHAR(200) \- Bắt buộc khi Individual và Correction; không hiển thị cho Parent  
* Status: INT \- 1 Pending, 2 Success, 3 Failed, 4 ReconciliationRequired  
* FailureCode, FailureReason: VARCHAR(50), NVARCHAR(500) \- Đã làm sạch  
* EducationAccountTransactionId: BIGINT \- ID logic sổ cái Function 1; bắt buộc khi Success; duy nhất  
* CreatedAt, UpdatedAt, CompletedAt, RowVersion: DATETIME2(3), ROWVERSION \- UTC; CompletedAt rỗng khi đang xử lý  
* *Giá trị dẫn xuất (không lưu):* Effective amount của giao dịch Individual \= Amount trừ tổng Amount của các Correction Success liên kết

#### **Tham chiếu ngoài & Audit Log**

* **Function 1:** EA, sổ cái, API ghi có và ghi nợ hiệu chỉnh, Closure Eligibility Check (Function 2 chỉ lưu ID logic: EducationAccountId, EducationAccountTransactionId).  
* **R1:** Student Profile (họ tên, NRIC, DOB, Citizenship, Father NRIC, Mother NRIC).  
* **R3:** academic\_years, student\_school\_enrollments, liên kết Student–EA.  
* **R8:** Parent\_Profile (Email) cho thông báo email.  
* **AuditLog:** actor, action, entity, entity\_id, old\_value, new\_value, timestamp. Ghi: tạo, sửa, xác nhận, hủy campaign; bắt đầu, dừng, kết thúc run; mỗi top-up; mỗi hiệu chỉnh. Chủ sở hữu dịch vụ chung hay bảng riêng chờ Dev xác nhận.

## **5\. Validation**

### **5.1. Thông báo lỗi hiển thị cho HQ User**

| Mã | Nội dung hiển thị | Hành vi UI |
| :---- | :---- | :---- |
| **MSG-0201** | No Education Account found. Check the Account Number or NRIC and try again. | Giữ ở SCR-01 |
| **MSG-0202** | Enter an amount greater than 0, with up to 2 decimal places. | Giữ ở SCR-02, đánh dấu ô nhập |
| **MSG-0203** | The amount is more than the limit for one top-up. (TBC, OQ-03) | Giữ ở SCR-02 hoặc SCR-08 |
| **MSG-0204** | This Education Account is not active. Top-up is not allowed. | Vô hiệu ô nhập số tiền |
| **MSG-0205** | We could not check the account status. No amount was credited. Please try again later. | SCR-04, cho thử lại; không đổi dữ liệu |
| **MSG-0206** | Enter a reason (up to 200 characters). | Giữ ở SCR-02 hoặc SCR-06 |
| **MSG-0207** | Top-up completed. Reference: {Transaction Reference}. | SCR-04, hiện số dư mới |
| **MSG-0208** | The top-up could not be completed. No amount was credited. | SCR-04, cho thử lại |
| **MSG-0209** | We are verifying this top-up. Please check the history later. | SCR-04, trạng thái đang xác minh |
| **MSG-0210** | The correction has been completed. | Về SCR-05, hiện Effective amount mới |
| **MSG-0211** | The Education Account balance is not enough to correct this top-up. Nothing was changed. | Giữ ở SCR-06 |
| **MSG-0212** | This top-up cannot be corrected. | Ẩn hoặc vô hiệu nút Correct |
| **MSG-0213** | The total amount is more than the budget limit by SGD {amount}. Change the campaign and preview again. | SCR-09, vô hiệu nút Confirm |
| **MSG-0214** | No accounts match these criteria. | SCR-09, vô hiệu nút Confirm |
| **MSG-0215** | This campaign is running and cannot be changed. | Mọi nút sửa bị vô hiệu |
| **MSG-0216** | The campaign has changed. Preview again before confirming. | Quay về SCR-09, bắt buộc preview lại |
| **MSG-0217** | Enter an age range from 7 to 15, with the minimum not more than the maximum. | SCR-08, đánh dấu ô nhập |
| **MSG-0218** | Enter a balance operator and an amount of 0 or more. | SCR-08, đánh dấu ô nhập |
| **MSG-0219** | Choose a date and time in the future. | SCR-10, đánh dấu ô nhập |
| **MSG-0220** | This Academic Year is closed. Choose another Academic Year. | SCR-08 |
| **MSG-0221** | Add at least one criterion. | SCR-08 |
| **MSG-0222** | This campaign was changed by another user. Refresh and try again. | Làm mới dữ liệu |
| **MSG-0001** | Enter your \<field\> | Bỏ trống trường bắt buộc, báo theo từng trường |
| **MSG-0002** | Your session has expired. Please log in again. | Chuyển đến đăng nhập Admin Portal |
| **MSG-0003** | You do not have permission to perform this action. | Quay về màn hình chính |

### **5.2. Tiêu chí chấp nhận (AC)**

**Individual Top-Up**

| ID | Given / When / Then |
| :---- | :---- |
| **AC-01** | Given HQ User, when tìm theo Account Number hoặc NRIC đầy đủ, then thấy đúng một EA với holder, status, balance; NRIC hiển thị che một phần |
| **AC-02** | Given Account Number hoặc NRIC không có EA, when tìm, then báo MSG-0201 |
| **AC-03** | Given EA Active, when HQ User xác nhận top-up 50.00, then số dư tăng đúng 50.00 một lần, transaction Success, có mã bút toán của Function 1, Transaction Reference và audit log |
| **AC-04** | Given EA Closed, when xác nhận top-up, then bị từ chối, số dư không đổi, transaction Failed được ghi log |
| **AC-05** | Given học sinh vừa đủ 16 tuổi và EA chưa Closed, when xác nhận top-up, then F02 đóng EA trước, top-up bị từ chối, số dư không đổi |
| **AC-06** | Given Government API không phản hồi, when xác nhận top-up, then không ghi có, Account Status không tự đổi, báo MSG-0205 |
| **AC-07** | Given HQ User bấm xác nhận hai lần, then chỉ tạo một transaction và chỉ ghi có một lần |
| **AC-08** | Given Function 1 timeout sau khi nhận lệnh ghi có, when hỏi lại bằng FundingReference, then đã ghi thì Success đúng một lần; không xác định được thì ReconciliationRequired, và số dư không bị ghi có lần hai |
| **AC-09** | Given số tiền bằng 0, âm, hoặc có hơn 2 chữ số thập phân, then bị từ chối MSG-0202, không có dữ liệu nào đổi |
| **AC-10** | Given top-up thất bại, then số dư không đổi và lý do được ghi log |
| **AC-11** | Given School User hoặc Parent gọi API Top-Up, then bị từ chối 403 và ghi log bảo mật |

**Sửa top-up nhầm**

| ID | Given / When / Then |
| :---- | :---- |
| **AC-12** | Given top-up lẻ Success 100.00, EA Active, số dư 130.00, when HQ User chọn Reduce 40.00 kèm lý do, then số dư thành 90.00, có giao dịch Top-Up Correction, giao dịch gốc không đổi và hiện Corrected 40.00, Effective 60.00 |
| **AC-13** | Given top-up lẻ Success 100.00, when Reverse in full, then Effective amount bằng 0 và không sửa tiếp được |
| **AC-14** | Given số dư EA nhỏ hơn số tiền cần ghi nợ, when sửa, then bị từ chối MSG-0211, số dư không âm, không đổi dữ liệu |
| **AC-15** | Given top-up thuộc batch, hoặc giao dịch Top-Up Correction, then không có nút Correct |
| **AC-16** | Given EA Closed, when sửa, then bị từ chối |
| **AC-17** | Given sửa không có lý do, then bị từ chối MSG-0206 |

**Cấu hình Campaign, Preview**

| ID | Given / When / Then |
| :---- | :---- |
| **AC-18** | Given Academic Year, Round, ít nhất một criterion, số tiền và ngân sách hợp lệ, when Save, then campaign được tạo ở trạng thái Draft với Code do hệ thống sinh |
| **AC-19** | Given Minimum Age lớn hơn Maximum Age, hoặc nằm ngoài 7 đến 15, then bị từ chối MSG-0217 |
| **AC-20** | Given criterion tuổi 7 đến 12, số dư dưới SGD 100, Actively Enrolled, when Preview, then danh sách chỉ gồm EA Active thỏa cả ba criterion (AND), kèm Student Name, Age, Balance, Schooling Status, Top-Up Amount; tổng số tài khoản và tổng tiền đúng |
| **AC-21** | Given học sinh có enrollment đã kết thúc trước Eligibility Date, hoặc là PR hoặc IS không có EA, then không xuất hiện trong preview |
| **AC-22** | Given tổng tiền preview vượt Budget Limit, then nút Confirm bị vô hiệu và báo MSG-0213 |
| **AC-23** | Given đã preview, when HQ User sửa criterion, số tiền hoặc ngân sách, then campaign về Draft và phải preview lại mới Confirm được |
| **AC-24** | Given hai campaign cùng Academic Year và Round với criterion khác nhau, then cả hai chạy được; tài khoản thuộc cả hai nhận hai khoản và preview cảnh báo |

**Chạy và kết quả**

| ID | Given / When / Then |
| :---- | :---- |
| **AC-25** | Given campaign đã Confirm, when Run now, then mỗi tài khoản eligible được ghi có đúng một lần; run summary có Successful, Skipped, Failed; số tiền tổng khớp tổng các giao dịch Success |
| **AC-26** | Given giữa preview và lúc chạy một tài khoản có số dư tăng vượt ngưỡng, then bị Skipped (BALANCE\_NOT\_MATCH), không ghi có |
| **AC-27** | Given tài khoản bị đóng hoặc học sinh không còn học trước lúc chạy, then Skipped (EA\_NOT\_ACTIVE hoặc NOT\_ENROLLED) |
| **AC-28** | Given Budget Limit 250.00, số tiền mỗi tài khoản 100.00, 5 tài khoản eligible, then 2 tài khoản Successful, 3 tài khoản Skipped (BUDGET\_EXHAUSTED), tổng ghi có 200.00 |
| **AC-29** | Given Government API lỗi với một số tài khoản, then các tài khoản đó Failed (ELIGIBILITY\_CHECK\_UNAVAILABLE), run vẫn xử lý các tài khoản khác, trạng thái CompletedWithErrors |
| **AC-30** | Given có run item Failed, when Retry failed, then chỉ các item Failed được thử lại với cùng FundingReference và mỗi tài khoản ghi có tối đa một lần |
| **AC-31** | Given server khởi động lại giữa run, then run tiếp tục từ các item chưa xử lý, không ghi có trùng |
| **AC-32** | Given run Running, when HQ User Stop, then các tài khoản còn lại Skipped (RUN\_STOPPED), các khoản đã ghi có giữ nguyên |
| **AC-33** | Given Failed hoặc Skipped, then số dư EA tương ứng không đổi |
| **AC-34** | Given campaign Running, when HQ User sửa hoặc hai HQ User thao tác đồng thời, then bị từ chối MSG-0215 hoặc MSG-0222 |

**Lịch chạy**

| ID | Given / When / Then |
| :---- | :---- |
| **AC-35** | Given Run at date and time trong tương lai, then campaign Scheduled và tự chạy đúng giờ SGT; thời điểm trong quá khứ bị từ chối MSG-0219 |
| **AC-36** | Given campaign định kỳ MONTHLY, then mỗi tháng tạo một run mới với Eligibility Date là ngày chạy, đánh giá bằng dữ liệu tại thời điểm đó |
| **AC-37** | Given lần chạy định kỳ đến khi run trước còn Running, hoặc scheduler bị lỡ, then lần đó ghi Missed, cảnh báo vận hành, không chạy bù tự động |
| **AC-38** | Given sửa campaign Active, then các lần chạy chưa bắt đầu bị hủy và campaign về Draft |

**Audit, Parent, thông báo**

| ID | Given / When / Then |
| :---- | :---- |
| **AC-39** | Given mọi giao dịch Top-Up và Correction, then có Transaction Reference, số tiền, thời điểm, người thực hiện, campaign và run (nếu có); không xóa cứng |
| **AC-40** | Given top-up thành công, when Parent xem Transaction History (R8), then thấy Type Top-up, Money in, Status Completed; Description không chứa lý do nội bộ |
| **AC-41** | Given top-up thành công và Parent có email, then email được gửi bất đồng bộ; gửi lỗi không làm đổi kết quả top-up (nếu OQ-08 chốt trong phạm vi) |

## **6\. Appendices**

### **Appendix A. Trạng thái Campaign, Run, Run Item và Transaction**

| Đối tượng | Từ | Sang | Điều kiện | Ghi chú |
| :---- | :---- | :---- | :---- | :---- |
| **Campaign** | (mới) | Draft | HQ User Save | Sửa được |
| **Campaign** | Draft | Running | Preview đạt, Confirm, chọn Run now | Tạo run đầu tiên |
| **Campaign** | Draft | Scheduled | Confirm, chọn Run at date and time | Chờ đến giờ |
| **Campaign** | Draft | Active | Confirm, chọn Recurring | NextRunAt được tính |
| **Campaign** | Scheduled hoặc Active | Running | Đến giờ chạy | Mỗi campaign tối đa một run mở |
| **Campaign** | Running | Completed | Run của campaign ad-hoc kết thúc (Completed, CompletedWithErrors hoặc Stopped) | Không sửa được nữa |
| **Campaign** | Running | Active | Run của campaign định kỳ kết thúc | Chờ lần chạy kế tiếp |
| **Campaign** | Active | Ended | Quá End at, hoặc Academic Year chuyển CLOSED | Không tạo run mới |
| **Campaign** | Scheduled hoặc Active | Draft | HQ User sửa criterion, số tiền, ngân sách | Hủy các run chưa bắt đầu; phải preview và Confirm lại |
| **Campaign** | Draft, Scheduled hoặc Active | Cancelled | HQ User Cancel | Không còn run nào được tạo |
| **Run** | (mới) | Pending | Đến giờ hoặc HQ User chạy ngay | Khóa campaign |
| **Run** | Pending | Running | Bắt đầu lập danh sách và xử lý |  |
| **Run** | Pending | Cancelled | Hủy trước khi bắt đầu |  |
| **Run** | Running | Completed | Hết danh sách, không còn run item Failed hoặc ReconciliationRequired |  |
| **Run** | Running | CompletedWithErrors | Hết danh sách, còn run item Failed hoặc ReconciliationRequired |  |
| **Run** | Running | Stopped | HQ User Stop | Item còn lại Skipped (RUN\_STOPPED) |
| **Run** | CompletedWithErrors | Completed | Thử lại hoặc vận hành xử lý hết Failed và ReconciliationRequired |  |
| **Run** | (lần chạy định kỳ) | Missed | Run trước còn Running, hoặc scheduler bị lỡ giờ | Cảnh báo vận hành, không chạy bù |
| **Run Item** | (mới) | Pending | Lập danh sách khi run bắt đầu |  |
| **Run Item** | Pending | Successful | Function 1 ghi có thành công | Số dư tăng một lần |
| **Run Item** | Pending | Skipped | Không đủ điều kiện, hết ngân sách, hoặc run bị Stop | Số dư không đổi; có Skip Reason |
| **Run Item** | Pending | Failed | Lỗi xử lý hoặc kiểm tra | Số dư không đổi; có Failure Code |
| **Run Item** | Pending | ReconciliationRequired | Không xác định được kết quả ghi có | Tính trong nhóm Failed |
| **Run Item** | Failed | Successful, Skipped hoặc Failed | HQ User Retry failed | Dùng lại FundingReference |
| **Run Item** | ReconciliationRequired | Successful hoặc Failed | Bộ phận vận hành xử lý |  |
| **Transaction** | (mới) | Pending | HQ User xác nhận, hoặc run item bắt đầu ghi có | Có FundingReference |
| **Transaction** | Pending | Success | Function 1 ghi sổ cái thành công | Có mã bút toán của Function 1 |
| **Transaction** | Pending | Failed | Không đủ điều kiện, hoặc Function 1 báo lỗi | Số dư không đổi |
| **Transaction** | Pending | ReconciliationRequired | Không xác định được kết quả sau khi hỏi lại Function 1 | Cảnh báo vận hành |
| **Transaction** | ReconciliationRequired | Success hoặc Failed | Bộ phận vận hành xử lý |  |

### **Appendix B. Open Questions & Assumptions**

| ID | Câu hỏi | Ảnh hưởng | Phương án tạm trong FS |
| :---- | :---- | :---- | :---- |
| **OQ-01** | Hạn mức tối đa mỗi lần top-up lẻ và mỗi tài khoản trong bulk | BR-F2-03, BR-F2-19, MSG-0203 | Chưa đặt hạn mức; cấu hình được |
| **OQ-02** | Lịch định kỳ gồm những tần suất nào; Budget Limit áp dụng cho từng run hay cộng dồn theo campaign hoặc theo kỳ | BR-F2-20, BR-F2-24 | Từng run; ba tần suất MONTHLY, QUARTERLY, YEARLY |
| **OQ-03** | Có cần phê duyệt hai bước (maker-checker) cho campaign, kích hoạt định kỳ hoặc sửa top-up | BR-F2-12, OOS \#6 | Không; HQ User xác nhận một bước, có audit |
| **OQ-04** | Thời hạn cho phép sửa top-up nhầm; xử lý khi tiền đã dùng trả phí (số dư không đủ) | BR-F2-10, EX-14 | Không giới hạn thời gian; từ chối khi số dư không đủ, vận hành xử lý ngoài hệ thống |
| **OQ-05** | Có cần sửa từng giao dịch trong batch, hoặc hoàn tác cả một run | BR-F2-08, OOS \#4 | Ngoài phạm vi |
| **OQ-6** | Actively Enrolled chỉ dựa trên enrollment hay cần cả class assignment | BR-F2-17 | Chỉ enrollment |
| **OQ-7** | Campaign Eligibility Date của ad-hoc dùng ngày chạy hay một ngày cố định (ví dụ đầu năm học) | BR-F2-18 | HQ User chọn, mặc định ngày chạy |
| **OQ-8** | Description của top-up hiển thị cho Parent: tên campaign hay "MOE Top-up" chung | Mục 2.2 (R8) | "MOE Top-up" chung |
| **OQ-9** | Tài khoản thỏa nhiều campaign cùng kỳ: cho nhận nhiều khoản hay chặn | BR-F2-28 | Cho phép, preview cảnh báo |
| **OQ-11** | Ngưỡng thời gian Pending trước khi chuyển ReconciliationRequired; chu kỳ hỏi lại Function 1 | EX-05 | Do Dev cấu hình; không tự Failed |

### **Appendix C. Danh sách màn hình**

| Mã | Màn hình | Thành phần chính | Hành động | Trạng thái UI |
| :---- | :---- | :---- | :---- | :---- |
| **SCR-01** | Individual Top-Up: Tìm EA | Chọn kiểu tìm, ô nhập Account Number hoặc NRIC | Search | Loading, Empty (không có kết quả), Error |
| **SCR-02** | Xác minh chủ tài khoản và nhập số tiền | Tên, NRIC che một phần, tuổi, Account Number, Account Status, Current Balance, ô Top-Up Amount, Reason | Continue, quay lại | Ô nhập bị vô hiệu khi EA không Active |
| **SCR-03** | Xem lại và xác nhận | Chủ tài khoản, số tiền, số dư sau top-up, lý do | Xác nhận, hủy | Nút xác nhận bị vô hiệu sau khi bấm; Processing |
| **SCR-04** | Kết quả top-up | Trạng thái, Transaction Reference, số dư mới, thông báo | Về SCR-01, xem Top-Up History | Success, Failed, Verifying |
| **SCR-05** | Top-Up History | Bộ lọc, bảng giao dịch (gồm Corrected và Effective amount), nút Correct | Lọc, Correct, xem chi tiết | Loading, Empty, Error |
| **SCR-06** | Sửa top-up | Giao dịch gốc, Effective amount còn lại, kiểu sửa, số tiền ghi nợ, Reason | Xác nhận, hủy | Lỗi từng trường |
| **SCR-07** | Danh sách Campaign | Bảng campaign, bộ lọc Academic Year, Round, Status | Create, mở, Cancel | Loading, Empty |
| **SCR-08** | Cấu hình Campaign | Name, Academic Year, Round, criterion (Age Range, Account Balance, Schooling Status), Top-Up Amount, Budget Limit | Save, Preview | Draft; lỗi từng trường |
| **SCR-09** | Preview | Danh sách eligible, tổng số tài khoản, tổng tiền, Budget Limit, Remaining budget, cảnh báo trùng campaign, thời điểm preview | Confirm, quay lại sửa | Confirm bị vô hiệu khi vượt ngân sách hoặc không có tài khoản |
| **SCR-10** | Chọn chế độ chạy | Run now, Run at date and time, Recurring; Eligibility Date; lịch | Xác nhận, hủy | Lỗi từng trường |
| **SCR-11** | Danh sách Run | Bảng run: trạng thái, số liệu, Eligibility Date | Mở run, Stop, Cancel | Pending, Running, Completed, CompletedWithErrors, Stopped, Missed |
| **SCR-12** | Run summary và Run Item | Tổng Successful, Skipped, Failed (số lượng và tiền), ngân sách đã dùng, bảng run item, bộ lọc Outcome | Export CSV, Retry failed | Loading, Empty, Error |

# **R2 (v2)**

1. # **Functional Specification: Function 2 (R2) – Top-Up Management**

   1. ## **1\. Introduction**

      1. ### **1.1. Preface**

Tài liệu này là Functional Specification (FS) cho Function 2 (R2) – Top-Up Management trên Admin Portal của hệ thống Education Account & FAS (MOE Singapore). Function 2 cho phép MOE HQ User nạp tiền vào Education Account (EA) theo hai cách: nạp lẻ cho từng chủ tài khoản (Individual Top-Up), hoặc nạp hàng loạt theo campaign với rule cấu hình theo độ tuổi, số dư và tình trạng đi học (Bulk Top-Up). Campaign chạy ngay sau khi HQ User xác nhận.

2. ### **1.2. Personas**

| Persona | Loại | Vai trò trong Function 2 |
| ----- | ----- | ----- |
| **MOE HQ User** | Primary actor | Nạp lẻ; tạo và cấu hình campaign; xem preview; xác nhận chạy; xem kết quả run |
| **School User** | Không phải actor | Không có quyền Top-Up, không thấy menu Top-Up |
| **Parent** | Gián tiếp | Thấy giao dịch Top-up trong Transaction History (R8) |
| **Admin Portal System** | Hệ thống | Kiểm tra điều kiện, tính danh sách eligible, chạy batch, ghi log và audit |

   3. ### **1.3. Design Assumptions and Limitations**

      1. #### ***Design Assumptions***

| ID | Assumption |
| ----- | ----- |
| **DA-01** | Top-up là ghi có vào EA trong sổ cái Function 1\. |
| **DA-02** | Function 2 ghi có trực tiếp vào số dư EA, đồng thời thêm một bút toán vào sổ cái, trong cùng một database transaction. |
| **DA-03** | Chỉ MOE HQ User dùng được Function 2\. School User và Parent không có quyền. |
| **DA-04** | Chỉ EA có trạng thái Active mới nhận top-up. |
| **DA-05** | Mọi lần ghi có (top-up lẻ, từng dòng trong batch) đều chạy Closure Eligibility Check của F02 trước khi thực hiện. |
| **DA-06** | Preview chỉ mang tính tham khảo. Khi chạy, hệ thống đánh giá lại từng tài khoản bằng dữ liệu tại thời điểm đó. |
| **DA-07** | Các criterion của campaign kết hợp bằng OR: tài khoản eligible khi thỏa ít nhất một criterion đã chọn. Mỗi tài khoản eligible nhận một số tiền cố định, dù thỏa nhiều criterion. |
| **DA-08** | Một campaign thuộc một Academic Year. Cùng một Academic Year có thể chạy nhiều campaign với criterion và số tiền khác nhau. |
| **DA-09** | Campaign chạy ngay sau khi HQ User xác nhận (Confirm); không có chế độ chạy theo lịch hay định kỳ. Mỗi campaign có đúng một run. |
| **DA-10** | Sổ cái chỉ thêm mới. Function 2 không sửa hay xóa giao dịch đã ghi; top-up nhầm được xử lý ngoài hệ thống (OOS \#4). |
| **DA-11** | Mỗi lần ghi có tạo một top-up transaction với FundingReference riêng, và kiểm tra idempotency key để không phát sinh hai giao dịch trùng. |
| **DA-12** | Tiền tệ SGD, 2 chữ số thập phân. Ngày hiển thị DD/MM/YYYY theo giờ Singapore (SGT, UTC+8); lưu UTC. |
| **DA-13** | Function 2 không thiết lập ngân sách hay hạn mức cho campaign. Chi tiêu được theo dõi bằng Top-Up Summary (Total Spending, Successful, Failed) khi xem history, campaign và run; số liệu chỉ để xem, không chặn xác nhận hay ghi có. |

         2. #### ***Limitations***

* Function 2 không sửa hay hoàn tác top-up đã ghi có; top-up nhầm được xử lý ngoài hệ thống (OOS \#4).  
* Function 2 chỉ được coi là đạt khi cả nạp lẻ và nạp hàng loạt chạy đúng tiêu chí chấp nhận.

### **1.4. Definitions, Acronyms and Abbreviations**

| Thuật ngữ | Giải thích |
| ----- | ----- |
| **EA** | Education Account. Tài khoản chi tiêu cho giáo dục của Singapore Citizen từ 7 đến dưới 16 tuổi. Số dư và sổ cái ở Function 1\. |
| **Top-Up** | Giao dịch ghi có một số tiền SGD vào EA. |
| **Individual Top-Up** | Top-up lẻ cho một EA do HQ User tìm và nhập số tiền. |
| **Bulk Top-Up** | Top-up cho nhiều EA cùng lúc theo criterion của một campaign. |
| **Campaign** | Định nghĩa một đợt bulk top-up: Academic Year, criterion, số tiền, Eligibility Date. |
| **Criterion** | Một điều kiện lọc của campaign: tuổi, số dư, tình trạng đi học, trường, cấp học, lớp. HQ User chọn một hoặc nhiều criterion; các criterion kết hợp bằng OR. |
| **Campaign Eligibility Date** | Ngày dùng làm mốc tính tuổi và tình trạng đi học. |
| **Run** | Một lần thực thi campaign. Mỗi campaign có một run, chạy ngay khi HQ User xác nhận. |
| **Run Item** | Kết quả xử lý của một EA trong một run. |
| **Preview** | Danh sách tài khoản dự kiến eligible, kèm tổng số và tổng tiền, xem trước khi chạy. |
| **Total Spending** | Tổng số tiền đã ghi có thành công (tổng Amount các giao dịch Success) trong phạm vi đang xem: theo bộ lọc History, theo campaign hoặc theo run. |
| **Top-Up Summary** | Khối số liệu chỉ để xem gồm Total Spending, Successful, Failed. Không thiết lập ngân sách và không chặn top-up. |
| **Actively Enrolled** | Học sinh có enrollment còn hiệu lực trong Academic Year mục tiêu. |
| **Successful / Failed** | Hai nhóm kết quả của Run Item: nạp thành công / không nạp được (lỗi xử lý, hoặc không còn đủ điều kiện khi chạy). |
| **Funding reference id** | Mã tham chiếu duy nhất của một lần ghi có, gửi sang Function 1 để chống ghi trùng và đối soát. |
| **Idempotency key** | Khóa đảm bảo một yêu cầu chỉ được xử lý một lần dù bị gửi lại; duy nhất theo HQ User. |
| **Reconciliation X** | Đối soát khi kết quả ghi có chưa rõ. ReconciliationRequired là trạng thái cần bộ phận vận hành xử lý. |
| **Ledger X** | Sổ ghi giao dịch EA, chỉ thêm mới, thuộc Function 1\. |
| **SGD** | Singapore dollar. |

4. ### **1.5. Exclusions**

FS này không đặc tả:

* Nguồn ngân sách, phê duyệt tài chính nội bộ MOE và hạch toán kế toán.  
* Tạo và đóng EA, Closure Eligibility Check (R1). Function 2 chỉ gọi.  
* Số dư, sổ cái và việc triển khai API ghi có của Function 1\. FS chỉ mô tả cách Function 2 gọi các API này.  
* Enrollment, Academic Year, liên kết Student–EA (R3). Function 2 chỉ đọc.  
* Hiển thị Transaction History cho Parent (R8) và thanh toán phí bằng EA (R9). Chỉ mô tả điểm nối ở mục 2.2.  
* Áp trợ cấp FAS (R4).  
* Xác thực và phân quyền Admin Portal.

### **1.6. OOS List**

| \# | Hạng mục ngoài phạm vi | Lý do / nguồn | Dự kiến |
| ----- | ----- | ----- | ----- |
| **1** | Số tiền khác nhau theo từng tài khoản (theo bậc tuổi, cấp học) | Requirement chỉ nêu số tiền cố định mỗi tài khoản; muốn nhiều mức thì tạo nhiều campaign | Chưa xếp lịch |
| **2** | Criterion bổ sung (FAS tier) | Requirement ghi "etc."; mô hình criterion được thiết kế mở rộng nhưng bản này có tuổi, số dư, tình trạng đi học, School, Academic Level và Class | Chưa xếp lịch |
| **3** | Nhập danh sách tài khoản bằng file CSV | Không có trong requirement | Chưa xếp lịch |
| **4** | Sửa hoặc hoàn tác top-up đã ghi có (top-up lẻ, từng giao dịch trong batch, cả một run) | Đã bỏ khỏi phạm vi (US-033 Incorrect Manual Top-Up Correction); top-up nhầm được xử lý ngoài hệ thống | Sau khi client chốt |
| **5** | Top-up cho EA Closed, chuyển số dư sang CPF | CPF Transfer chưa triển khai ở R1 | Cùng CPF Transfer |
| **6** | Phê duyệt hai bước (maker-checker) | Chưa có trong requirement (OQ-03) | Chưa xếp lịch |
| **7** | Dashboard phân tích chi tiêu nhiều campaign | Không có trong requirement; bản này chỉ có Top-Up Summary (Total Spending, Successful, Failed) khi xem history, từng campaign và từng run, và export | Chưa xếp lịch |
| **8** | Mọi thông báo cho Parent (email, SMS, trong ứng dụng) | Đã bỏ khỏi phạm vi (F2.8 Parent Notification); FS-08 cũng đã bỏ chuông thông báo | Chưa xếp lịch |
| **9** | Thiết lập ngân sách hoặc hạn mức cho campaign, cảnh báo vượt ngân sách | Đã bỏ khỏi phạm vi; thay bằng Top-Up Summary khi xem history | Chưa xếp lịch |
| **10** | Chạy campaign theo lịch (một lần hoặc định kỳ), chọn chế độ chạy | Đã bỏ khỏi phạm vi; campaign chạy ngay khi xác nhận | Chưa xếp lịch |

5. ### **1.7. Traceability với Product Backlog**

| User Story | Tên | Requirement (backlog) | Sub-function | Business Rule | Acceptance Criteria | Màn hình |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| **US-028** | Individual EA Top-Up | R2 Individual Top-Up, B01–B07 | F2.1, F2.2 | BR-F2-01 đến BR-F2-06 | AC-01 đến AC-11 | SCR-01 đến SCR-04 |
| **US-029** | Bulk Campaign Rules & Funding Limit | R2 Bulk Top-Up Rule Configuration, B01–B18 | F2.4 | BR-F2-13 đến BR-F2-18 | AC-18, AC-19, AC-24, AC-46 đến AC-50 | SCR-07, SCR-08 |
| **US-030** | Bulk Eligibility Preview & Confirmation | R2 Bulk Top-Up Preview & Confirmation, B01–B06 | F2.5 | BR-F2-19, BR-F2-20 | AC-20 đến AC-23 | SCR-09 |
| **US-031** | Bulk Top-Up Execution & Results | R2 Bulk Top-Up Execution, B01–B07; R2 Top-Up History & Results, B05 | F2.6, F2.7 | BR-F2-21 đến BR-F2-30 | AC-25 đến AC-36 | SCR-09 (Confirm), SCR-11, SCR-12 |
| **US-032** | Individual & Bulk Top-Up History | R2 Top-Up History & Results, B01–B06 | F2.3, F2.7 (run summary) | BR-F2-07, BR-F2-29, BR-F2-30 | AC-39, AC-42 đến AC-45 | SCR-05, SCR-07, SCR-11, SCR-12 |
| **US-033** | Incorrect Manual Top-Up Correction | R2 Top-Up History & Results, B06; R2 Incorrect Manual Top-Up Correction, B01 | Ngoài phạm vi (OOS \#4) | Không có | Không có | Không có |

## **2\. System Process and Function Overview**

6. ### **2.1. Process Flow Diagrams**

   1. #### ***Individual Top-Up Flow***

HQ User tìm một EA, kiểm tra thông tin chủ tài khoản, nhập số tiền và xác nhận. Hệ thống chạy Closure Eligibility Check trước khi ghi có. Chỉ EA Active mới nhận tiền; thất bại không làm đổi số dư.  
![][image5]

2. #### ***Bulk Top-Up Flow – Campaign Setup, Preview and Launch***

HQ User cấu hình campaign, xem preview (số tài khoản và tổng tiền dự kiến) để kiểm tra criterion, rồi xác nhận để campaign chạy ngay. Sửa criterion hoặc số tiền sau khi preview thì preview cũ mất hiệu lực và phải làm lại và preview lại.  
![][image6]

7. ### **2.2. Liên kết với các requirement khác**

| Requirement | Function 2 dùng / cung cấp | Quy tắc nối |
| ----- | ----- | ----- |
| **R1 – F02 (đóng EA)** | Gọi: Closure Eligibility Check trước mỗi lần ghi có | EA Closed, Closure Deferred, Eligibility Review Required, hoặc Government API không phản hồi: không ghi có (F02-AC04, EF01). EA đủ 16 tuổi chưa Closed: F02 chạy closure trước, rồi top-up bị từ chối |
| **R3 – Enrollment** | Dùng: student\_school\_enrollments (enrolled\_from, enrolled\_to\_exclusive, status) để xác định Actively Enrolled | Học sinh Actively Enrolled khi có enrollment ENROLLED còn hiệu lực tại Eligibility Date và giao với Academic Year của campaign |
| **R3 – School, Academic Level, Class** | Dùng: master data trường, cấp học (Primary, Secondary), lớp và phân lớp của học sinh (tên bảng TBC, OQ-12) | Criterion School và Academic Level đối chiếu với enrollment ENROLLED hiệu lực tại Eligibility Date; criterion Class đối chiếu với phân lớp của học sinh trong Academic Year của campaign |
| **R3 – Academic Year** | Dùng: academic\_years (year\_number, start\_date, end\_date\_exclusive, status) | Campaign chỉ gắn với Academic Year có status DRAFT hoặc ACTIVE, không gắn với CLOSED (OQ-06) |
| **R3 – F08 (liên kết Student–EA)** | Dùng: liên kết giữa Student của R3 và EA | Chỉ Student SC có EA; Student PR hoặc IS không có EA nên không bao giờ eligible. Từ EA tìm Student của R3 qua liên kết này để lấy enrollment |
| **R8 – Parent Portal** | Cung cấp: giao dịch Top-up trong Transaction History (FR-08.2) | Top-up thành công hiện Type Top-up, Money in, Status Completed, Amount có dấu cộng. Description chỉ ghi "MOE Top-up" hoặc tên campaign; không hiện lý do hoặc ghi chú nội bộ của HQ User. Số dư Home và Education Account tăng ngay sau khi ghi có thành công |
| **R9 – thanh toán bằng EA** | Dùng chung Function 1 | Số dư khả dụng dùng cho thanh toán là số dư sau top-up. Top-up (ghi có) và thanh toán (ghi nợ) đều đi qua sổ cái Function 1, nên được tuần tự hóa ở đó; Function 2 không khóa số dư. Function 1 cần API ghi có idempotent theo FundingReference, cùng nhu cầu với NQ-15 của R9 |

## **3\. Detailed Functions and Solution Design**

8. ### **3.1. Detailed Function Specification**

   1. #### ***3.1.1. Function Description***

Function 2 cho MOE HQ User nạp tiền vào EA theo hai cách: nạp lẻ cho một chủ tài khoản, hoặc nạp hàng loạt theo campaign. Campaign gồm Academic Year, các criterion (tuổi, số dư, tình trạng đi học, trường, cấp học, lớp; thỏa ít nhất một criterion là eligible), số tiền cố định mỗi tài khoản; campaign chạy ngay sau khi HQ User xác nhận. Mỗi lần ghi có đi qua Closure Eligibility Check và API ghi có của Function 1\. Khi xem Top-Up History, campaign và run, HQ User thấy Total Spending, Successful, Failed.

| Mục | Nội dung |
| ----- | ----- |
| **Function ID** | F2 (R2) |
| **Portal** | Admin Portal |
| **Actor chính** | MOE HQ User |
| **Precondition** | HQ User đã đăng nhập Admin Portal và có quyền Top-Up; EA đã được tạo (R1). Với bulk: Academic Year đã tồn tại (R3) |
| **Postcondition (thành công)** | Mỗi lần ghi có thành công có một bút toán ghi có ở Function 1, số dư EA tăng đúng một lần; có top-up transaction với Transaction Reference; có audit log. Với bulk: có run summary Successful, Failed và Top-Up Summary (Total Spending, Successful, Failed) của campaign |
| **Postcondition (thất bại)** | Top-up transaction \= Failed; số dư EA không đổi; lý do được ghi log. Với bulk: các tài khoản khác trong run vẫn được xử lý |
| **Postcondition (đang chạy)** | Run \= Running; campaign không sửa được; không mở thêm run cho cùng campaign |
| **Postcondition (cần xử lý tay)** | Giao dịch hoặc run item \= ReconciliationRequired khi không xác định được kết quả ghi có; bộ phận vận hành xử lý; hệ thống không tự đoán là đã ghi hay chưa |

1. ##### **Sub-functions**

| ID | Sub-function | Mục đích |
| ----- | ----- | ----- |
| **F2.1** | Search and Verify EA Account Holder | Tìm kiếm tài khoản EA theo Account Number hoặc Student NRIC; hiển thị thông tin chủ tài khoản, trạng thái tài khoản và số dư hiện tại để xác minh trước khi nạp tiền. |
| **F2.2** | Individual Top-Up | Thực hiện nạp tiền cho một tài khoản EA cụ thể; nhập số tiền, xác nhận giao dịch, kiểm tra điều kiện hợp lệ, ghi có vào EA thông qua Function 1 và hiển thị kết quả. |
| **F2.3** | Top-Up History | Tra cứu lịch sử các giao dịch top-up lẻ và top-up từ bulk, lọc theo tài khoản, khoảng ngày, nguồn và trạng thái; xem Top-Up Summary (Total Spending, Successful, Failed) theo bộ lọc, theo campaign và theo run; lưu vết kiểm toán. |
| **F2.4** | Top-Up Campaign Configuration | Tạo và cấu hình chiến dịch top-up theo Academic Year, tiêu chí đối tượng thụ hưởng, số tiền nạp và chế độ thực thi. |
| **F2.5** | Eligibility Preview | Xác định danh sách tài khoản đủ điều kiện theo các tiêu chí đã cấu hình; hiển thị số lượng tài khoản và tổng số tiền dự kiến để kiểm tra criterion và chi tiêu trước khi xác nhận, và cho phép xem lại preview khi cấu hình thay đổi. |
| **F2.6** | Top-Up Run Launch and Stop | Khi HQ User xác nhận campaign, hệ thống chạy ngay một run; HQ User có thể dừng (Stop) run đang chạy theo các quy tắc được phép. Không có chế độ chạy theo lịch hay định kỳ. |
| **F2.7** | Top-Up Execution and Run Monitoring | Thực thi top-up theo danh sách đã xác nhận; kiểm tra lại điều kiện từng tài khoản trước khi ghi có; tổng hợp kết quả thành công/thất bại, hỗ trợ thử lại các tài khoản thất bại, xuất báo cáo và lưu audit log. |

##### **Business Rules**

1. ###### ***Nhóm A – Quyền và Individual Top-Up (F2.1, F2.2)***

* **BR-F2-01**: Chỉ MOE HQ User có quyền Top-Up. Mọi API kiểm tra quyền ở server; School User và Parent bị từ chối.  
* **BR-F2-02**: Tìm EA theo khớp chính xác Account Number hoặc NRIC đầy đủ của học sinh; không tìm gần đúng. Chỉ khi nhập đủ và đúng NRIC (hoặc Account Number) mới hiển thị tài khoản; nhập thiếu, thừa ký tự hoặc sai thì không có kết quả, không có danh sách gợi ý, không hiển thị kết quả một phần, và chỉ báo MSG-0201. Mỗi lần tìm trả về tối đa một EA. Kết quả hiển thị NRIC che một phần.  
* **BR-F2-03**: Số tiền top-up lớn hơn 0, tối đa 2 chữ số thập phân, không vượt hạn mức mỗi lần (TBC, OQ-03). Lý do (reason) bắt buộc, tối đa 200 ký tự.  
* **BR-F2-04**: Chỉ EA Active nhận top-up. Trước khi ghi có, hệ thống chạy Closure Eligibility Check của F02. EA Closed, Closure Deferred, Eligibility Review Required hoặc Government API không phản hồi: từ chối, không ghi có, số dư không đổi.  
* **BR-F2-05**: Mỗi lần ghi có chỉ xảy ra một lần: idempotency key duy nhất theo HQ User, nút xác nhận bị vô hiệu sau khi bấm, mỗi lần ghi có có FundingReference riêng.  
* **BR-F2-06**: Giao dịch thất bại không làm đổi số dư nhưng vẫn được ghi log (thời điểm, người thực hiện, lý do).

###### ***Nhóm B – Lịch sử (F2.3)***

* **BR-F2-07**: Top-Up History liệt kê mọi top-up lẻ và top-up từ bulk (SCR-05). Phía trên bảng, hệ thống hiển thị khối Top-Up Summary tính theo đúng bộ lọc đang chọn: Total Spending (tổng Amount các giao dịch Success), Successful (số lượng) và Failed (số lượng và số tiền dự kiến chưa ghi có, kèm số ReconciliationRequired). Campaign bulk đã chạy xem được ở danh sách Campaign (SCR-07), danh sách Run (SCR-11) và Run summary (SCR-12), kèm ba chỉ số này theo từng campaign và run. Số liệu chỉ để xem, không chặn xác nhận hay ghi có.

###### ***Nhóm C – Cấu hình Campaign (F2.4)***

* **BR-F2-13**: Mỗi campaign thuộc một Academic Year. Campaign Code duy nhất trong Academic Year. Cùng một Academic Year chạy được nhiều campaign với criterion và số tiền khác nhau.  
* **BR-F2-14**: Các criterion kết hợp bằng OR: HQ User chọn một hoặc nhiều criterion, tài khoản eligible khi thỏa ít nhất một criterion. Campaign cần ít nhất một criterion. Điều kiện nền áp dụng cho mọi tài khoản và không phải criterion: Student SC có liên kết EA, EA Active, qua Closure Eligibility Check. Có sáu loại criterion, mỗi loại thêm tối đa một lần:  
  * **Age Range**: Minimum Age, Maximum Age (bao gồm cả hai đầu); thỏa khi tuổi tại Eligibility Date nằm trong khoảng.  
  * **Account Balance**: toán tử và ngưỡng SGD; thỏa khi số dư hiện tại so với ngưỡng đúng toán tử.  
  * **Schooling Status**: Actively Enrolled; thỏa khi học sinh Actively Enrolled trong Academic Year.  
  * **School**: chọn một hoặc nhiều trường; thỏa khi enrollment ENROLLED hiệu lực tại Eligibility Date (giao với Academic Year) thuộc một trong các trường đã chọn.  
  * **Academic Level**: chọn Primary và/hoặc Secondary; thỏa khi cấp học của enrollment hiệu lực thuộc một trong các cấp đã chọn.  
  * **Class**: chọn một hoặc nhiều lớp thuộc Academic Year của campaign; thỏa khi học sinh được xếp vào một trong các lớp đã chọn. Đổi Academic Year thì các lớp đã chọn không thuộc năm mới bị bỏ chọn.  
  * Với School, Academic Level và Class, các giá trị trong cùng một criterion cũng kết hợp bằng OR. Mỗi criterion loại này cần ít nhất một giá trị.  
  * Tài khoản thỏa nhiều criterion vẫn chỉ xuất hiện một lần và nhận một khoản (BR-F2-25).  
* **BR-F2-15**: Age Range: chỉ nhận giá trị lớn hơn hoặc bằng 7 VÀ bé hơn 16 vì EA chỉ tồn tại từ 7 đến dưới 16 tuổi. Tuổi được tính theo số năm tròn tại Campaign Eligibility Date.  
* **BR-F2-16**: Campaign Eligibility Date do HQ User chọn ở SCR-08, mặc định là ngày hiện tại; run dùng đúng ngày này làm mốc.  
* **BR-F2-17**: Function 2 không thiết lập ngân sách hay hạn mức cho campaign. Chi tiêu của campaign được theo dõi bằng Top-Up Summary (BR-F2-07); không có bước chặn hay cảnh báo theo ngân sách ở preview, xác nhận hay khi chạy.  
* **BR-F2-18**: Trạng thái campaign: Draft, Running, Completed, Cancelled (Appendix A). Chỉ sửa được khi Draft. Sau khi Confirm, campaign chuyển Running ngay và không sửa được nữa. Sửa criterion, số tiền hoặc Eligibility Date sau khi đã preview thì preview cũ mất hiệu lực và phải preview lại.

###### ***Nhóm D – Preview và thực thi (F2.5, F2.6, F2.7)***

* **BR-F2-19**: Preview hiển thị Student Name, Age, Balance, Schooling Status, School, Academic Level, Class, Matched Criteria (các criterion tài khoản thỏa), Top-Up Amount dự kiến của từng tài khoản, cùng tổng số tài khoản, tổng tiền dự kiến và thời điểm tính preview. Preview chỉ đọc.  
* **BR-F2-20**: Chỉ xác nhận được khi preview tính trên đúng phiên bản hiện tại của campaign và có ít nhất một tài khoản eligible. Sửa criterion hoặc số tiền thì preview cũ mất hiệu lực.  
* **BR-F2-21**: Khi HQ User Confirm, campaign chuyển Running và hệ thống tạo run ngay; không có lựa chọn chế độ chạy, lịch chạy hay chạy định kỳ.  
* **BR-F2-22**: Mỗi campaign chỉ có một run. Chỉ Confirm được khi campaign đang Draft; bấm Confirm lần hai, hoặc hai HQ User Confirm cùng lúc, chỉ tạo một run (kiểm tra bằng row version).  
* **BR-F2-23**: Hủy (Cancel) được campaign Draft. Run đang Running cho phép Stop: hoàn tất đoạn đang xử lý, các tài khoản còn lại ghi Failed (RUN\_STOPPED), các khoản đã ghi có giữ nguyên.  
* **BR-F2-24**: Khi chạy, hệ thống xử lý từng tài khoản theo thứ tự Account Number tăng dần, theo từng đoạn nhỏ: Closure Eligibility Check, EA còn Active, đánh giá lại các criterion (thỏa ít nhất một) bằng dữ liệu tại thời điểm đó, ghi có. Sau mỗi đoạn hệ thống cập nhật số liệu run (Successful, Failed, Total credited) để theo dõi.  
* **BR-F2-25**: Trong một run, mỗi tài khoản được ghi có tối đa một lần (duy nhất theo RunId và EA). Giữa các campaign khác nhau, một tài khoản có thể nhận nhiều khoản; preview cảnh báo nếu tài khoản đã nhận top-up từ campaign khác cùng kỳ.  
* **BR-F2-26**: Kết quả từng tài khoản chỉ có hai trạng thái: Successful hoặc Failed. Failed kèm Failure Code: không còn đủ điều kiện khi chạy (EA\_NOT\_ACTIVE, ELIGIBILITY\_REVIEW\_REQUIRED, CRITERIA\_NOT\_MATCH khi không còn thỏa criterion nào), run bị dừng (RUN\_STOPPED), hoặc lỗi kỹ thuật (ví dụ ELIGIBILITY\_CHECK\_UNAVAILABLE, CREDIT\_FAILED). ReconciliationRequired tính trong nhóm Failed và có cờ riêng.  
* **BR-F2-27**: Mỗi run item có FundingReference cố định, sinh một lần. Thử lại dùng đúng FundingReference đó, nên Function 1 không ghi trùng.  
* **BR-F2-28**: Thử lại: HQ User thử lại các run item Failed (không gồm ReconciliationRequired). Thử lại vẫn đi qua mọi kiểm tra.  
* **BR-F2-29**: Run summary hiển thị Total Spending của run (Total credited), tổng Successful, Failed (số tài khoản và số tiền), số ReconciliationRequired; lọc theo kết quả; export CSV. Trạng thái run: Completed khi không có Failed, CompletedWithErrors khi còn Failed.  
* **BR-F2-30**: Audit lưu vĩnh viễn: Transaction Reference, số tiền, thời điểm, người thực hiện (HQ User, hoặc "System" kèm HQ User đã kích hoạt campaign), campaign, run. Không xóa cứng campaign, run, run item và giao dịch.

#### ***3.1.2. Process Flow Description and Screens***

* **Bước 1\. Tìm EA và xác minh chủ tài khoản (F2.1):** HQ User vào menu Top-Up, chọn Individual Top-Up (SCR-01). HQ User nhập Account Number hoặc NRIC đầy đủ của học sinh và chọn Search. Hệ thống tìm EA theo khớp chính xác (BR-F2-02) và hiển thị SCR-02: tên học sinh, NRIC che một phần, tuổi, Account Number, Account Status, Current Balance. *Luồng thay thế:* không tìm thấy thì báo MSG-0201; EA không Active vẫn hiển thị để tra cứu nhưng không cho nhập số tiền, kèm lý do (MSG-0204).  
* **Bước 2\. Nhập số tiền và xác nhận (F2.2):** Trên SCR-02, HQ User nhập Top-Up Amount và Reason rồi chọn Continue. Hệ thống kiểm tra định dạng và hạn mức (BR-F2-03), rồi hiển thị SCR-03 để xem lại: chủ tài khoản, Account Number, số dư hiện tại, số tiền, số dư sau top-up (tham khảo), lý do. HQ User xác nhận. Nút xác nhận bị vô hiệu ngay sau lần bấm đầu; client gửi kèm idempotency key.  
* **Bước 3\. Kiểm tra và ghi có (F2.2):** Hệ thống tạo top-up transaction (Pending) với Transaction Reference và FundingReference, rồi chạy Closure Eligibility Check của F02.  
  * *Không đủ điều kiện* (EA Closed, Closure Deferred, Eligibility Review Required, Government API không phản hồi): transaction Failed, số dư không đổi, hiển thị SCR-04 với thông báo tương ứng.  
  * *Đủ điều kiện:* gọi Function 1 ghi có (nguyên tử, idempotent theo FundingReference).  
  * *Thành công:* transaction Success, lưu mã bút toán của Function 1, ghi audit log, hiển thị SCR-04 kèm Transaction Reference và số dư mới (MSG-0207).  
  * *Thất bại:* transaction Failed, số dư không đổi (MSG-0208).  
  * *Không rõ kết quả:* hỏi lại Function 1 bằng cùng FundingReference; vẫn không rõ thì ReconciliationRequired, hiển thị trạng thái đang xác minh (MSG-0209).  
* **Bước 4\. Xem Top-Up History (F2.3):** HQ User mở Top-Up History (SCR-05): danh sách mọi top-up (lẻ và từ batch) theo thời gian mới nhất trước, lọc theo Account Number, NRIC, khoảng ngày, nguồn (Individual, Bulk), trạng thái. Phía trên bảng, khối Top-Up Summary hiển thị Total Spending, Successful, Failed tính theo đúng bộ lọc đang chọn (BR-F2-07). Màn hình chỉ để tra cứu; không có thao tác sửa hoặc hoàn tác top-up (OOS \#4).  
* **Bước 5\. Tạo và cấu hình Campaign (F2.4):** HQ User vào Top-Up, chọn Bulk Top-Up Campaigns (SCR-07), chọn Create. Trên SCR-08, HQ User nhập Campaign Name, chọn Academic Year, thêm một hoặc nhiều criterion (Age Range, Account Balance, Schooling Status, School, Academic Level, Class; tài khoản thỏa ít nhất một criterion là eligible), nhập Top-Up Amount và Eligibility Date (mặc định là ngày hiện tại), rồi Save. Hệ thống kiểm tra theo BR-F2-13 đến BR-F2-18 và lưu campaign ở trạng thái Draft.  
* **Bước 6\. Preview và xác nhận (F2.5):** HQ User chọn Preview. Hệ thống đánh giá các criterion (OR) trên các EA Active và hiển thị SCR-09: danh sách eligible (Student Name, Age, Balance, Schooling Status, School, Academic Level, Class, Matched Criteria, Top-Up Amount), tổng số tài khoản, tổng tiền dự kiến, thời điểm tính preview, cảnh báo tài khoản đã nhận top-up từ campaign khác cùng kỳ.  
  * *Không có tài khoản eligible:* hiển thị MSG-0214, không xác nhận được.  
  * *Đạt điều kiện:* HQ User chọn Confirm và campaign chạy ngay (bước 7).  
* **Bước 7\. Xác nhận và chạy ngay (F2.6):** Trên SCR-09, HQ User chọn Confirm và xác nhận trong hộp thoại. Nút Confirm bị vô hiệu sau lần bấm đầu. Không có lựa chọn chế độ chạy hay lịch chạy. Hệ thống đổi campaign sang Running, ghi audit log người xác nhận và tạo run ngay. HQ User có thể Stop run đang Running ở SCR-11.  
* **Bước 8\. Thực thi run và nhận kết quả (F2.7):** Ngay sau khi Confirm, hệ thống tạo run (Pending, rồi Running), khóa campaign, cố định Eligibility Date và criterion cho run này. Hệ thống xử lý từng tài khoản theo BR-F2-24: kiểm tra, ghi có qua Function 1 với FundingReference của run item, ghi kết quả Successful hoặc Failed. HQ User theo dõi tiến độ ở SCR-11 và SCR-12 (số đã xử lý, Successful, Failed, Total credited). Hết danh sách: run \= Completed (không có Failed) hoặc CompletedWithErrors (còn Failed); hiển thị run summary (BR-F2-29). Campaign \= Completed.  
* **Bước 9\. Thử lại, export và xem lại campaign (F2.7):** Trên SCR-12, HQ User lọc run item theo kết quả, export CSV, và chọn Retry failed để thử lại các run item Failed (BR-F2-28). Parent thấy giao dịch trong Transaction History của R8 ngay sau khi ghi có. HQ User xem lại các campaign và run đã chạy ở SCR-07, SCR-11 và SCR-12, kèm Total Spending, Successful, Failed (BR-F2-07).

##### **Trường hợp ngoại lệ**

| \# | Tình huống | Xử lý |
| ----- | ----- | ----- |
| **EX-01** | School User hoặc Parent gọi API Top-Up, hoặc HQ User sửa ID trong request để thao tác trên campaign hay giao dịch không thuộc quyền | Server kiểm tra quyền cho mọi request, trả 403, không lộ dữ liệu, ghi log bảo mật (MSG-0003) |
| **EX-02** | EA chuyển sang Closed, hoặc học sinh đủ 16 tuổi, giữa lúc HQ User xem và lúc xác nhận | Closure Eligibility Check chạy khi xác nhận; F02 đóng EA nếu cần; top-up bị từ chối, số dư không đổi (MSG-0204) |
| **EX-03** | Government API không phản hồi khi kiểm tra đóng EA | Không ghi có; individual: hiển thị lỗi, cho thử lại; bulk: run item Failed (ELIGIBILITY\_CHECK\_UNAVAILABLE), có thể thử lại. Không tự đổi Account Status |
| **EX-04** | Bấm xác nhận hai lần, hoặc client gửi lại cùng idempotency key | Chỉ tạo một transaction và ghi có một lần; lần gửi lại nhận kết quả của transaction đầu |
| **EX-05** | Function 1 timeout hoặc lỗi mạng sau khi gửi lệnh ghi có | Giữ Pending, hỏi lại Function 1 bằng cùng FundingReference; nếu đã ghi thì đánh Success, nếu chưa thì cho Failed; vẫn không xác định thì ReconciliationRequired, cảnh báo vận hành. Không tự thử vô hạn |
| **EX-06** | Session Admin Portal hết hạn khi đang thao tác | Hết hạn trước khi xác nhận: yêu cầu đăng nhập lại, chưa có transaction. Hết hạn sau khi xác nhận: transaction vẫn được xử lý; HQ User đăng nhập lại thấy trạng thái hiện tại (MSG-0002) |
| **EX-07** | HQ User sửa criterion, số tiền hoặc Eligibility Date sau khi đã preview | Campaign vẫn là Draft; preview cũ mất hiệu lực; phải preview lại mới Confirm được (BR-F2-20). Sau khi Confirm, campaign đã Running và không sửa được (MSG-0215) |
| **EX-08** | Hai HQ User sửa, hủy hoặc Confirm cùng một campaign đồng thời; hoặc sửa campaign đang Running | Dùng row version để phát hiện xung đột, người sau nhận yêu cầu làm mới. Campaign đang Running không sửa được (MSG-0215) |
| **EX-09** | Giữa preview và lúc chạy, một tài khoản đổi số dư, bị đóng, hoặc học sinh không còn học | Đánh giá lại khi chạy: tài khoản không còn đủ điều kiện (bị đóng, hoặc không còn thỏa criterion nào) bị Failed với Failure Code tương ứng (EA\_NOT\_ACTIVE, hoặc CRITERIA\_NOT\_MATCH khi không còn thỏa criterion nào); danh sách thực tế có thể khác preview |
| **EX-11** | Job bị dừng đột ngột hoặc server khởi động lại giữa run | Run tiếp tục từ các run item chưa xử lý. Item đã gửi lệnh sang Function 1 mà chưa ghi kết quả được hỏi lại bằng FundingReference; không ghi có hai lần |

## 

## **4\. Data Fields Table**

9. ### **4.1. Trường hiển thị và nhập trên màn hình**

| Màn hình | Trường | Kiểu | Nguồn | Nhập | Bắt buộc | Quy tắc / ghi chú |
| ----- | ----- | ----- | ----- | :---: | :---: | ----- |
| **SCR-01** | Search by | Enum ACCOUNT\_NUMBER, NRIC | HQ User chọn | Có | Có | Khớp chính xác, không tìm gần đúng, không gợi ý khi nhập dở |
| **SCR-01** | Search value | Text | HQ User nhập | Có | Có | Account Number hoặc NRIC đầy đủ (9 ký tự) |
| **SCR-02** | Student name | Text | Student Profile (R1) | Không | Có |  |
| **SCR-02** | NRIC | Text | Student Profile (R1) | Không | Có | Che một phần, không đưa NRIC đầy đủ vào URL |
| **SCR-02** | Age | Integer | Tính từ DOB | Không | Có | Số năm tròn tại ngày hiện tại |
| **SCR-02** | Account Number | Text | Function 1 | Không | Có |  |
| **SCR-02** | Account Status | Enum Active, Closed | Function 1 | Không | Có | Chỉ Active mới nhập được số tiền |
| **SCR-02** | Current Balance | Decimal(18,2), SGD | Function 1 | Không | Có |  |
| **SCR-02** | Top-Up Amount | Decimal(18,2), SGD | HQ User nhập | Có | Có | Lớn hơn 0; tối đa 2 chữ số thập phân; không vượt hạn mức mỗi lần (TBC) |
| **SCR-02** | Reason | Text, tối đa 200 ký tự | HQ User nhập | Có | Có | Chỉ dùng nội bộ, không hiển thị cho Parent |
| **SCR-03** | Balance after top-up | Decimal(18,2) | Tính | Không | Không | Chỉ để tham khảo |
| **SCR-03** | Idempotency key | Text, tối đa 100 ký tự | Client sinh | Không | Có | Duy nhất theo HQ User; bấm đúp giữ cùng key; thao tác mới dùng key mới |
| **SCR-04** | Transaction Reference | Text, tối đa 50 ký tự | Hệ thống sinh | Không | Có | Duy nhất; định dạng đề xuất TUP-YYYYMMDD-XXXXXX (TBC) |
| **SCR-04** | Transaction Status | Enum Success, Failed, ReconciliationRequired | Transaction | Không | Có | ReconciliationRequired hiển thị là đang xác minh |
| **SCR-04** | New balance | Decimal(18,2) | Function 1 | Không | Không | Chỉ khi Success |
| **SCR-05** | Filter: Account Number, NRIC | Text | HQ User nhập | Có | Không |  |
| **SCR-05** | Filter: From, To | Date | HQ User chọn | Có | Không | DD/MM/YYYY, SGT |
| **SCR-05** | Filter: Source | Enum All, Individual, Bulk | HQ User chọn | Có | Không |  |
| **SCR-05** | Filter: Status | Enum All, Success, Failed, ReconciliationRequired | HQ User chọn | Có | Không |  |
| **SCR-05** | Cột bảng | Date, Transaction Reference, Student, Account Number, Source, Campaign (nếu bulk), Amount, Status, Performed by | Transaction | Không | Có | Mới nhất trước, 20 dòng mỗi trang |
| **SCR-05** | Top-Up Summary: Total Spending | Decimal(18,2), SGD | Tính | Không | Có | Tổng Amount các giao dịch Success theo bộ lọc đang chọn |
| **SCR-05** | Top-Up Summary: Successful, Failed | Integer, Decimal(18,2) | Tính | Không | Có | Số lượng theo bộ lọc; Failed gồm cả ReconciliationRequired, hiển thị số riêng; số tiền Failed là số tiền dự kiến chưa ghi có |
| **SCR-07** | Cột danh sách | Campaign Code, Name, Academic Year, Amount, Total Spending, Successful, Failed, Status | Campaign | Không | Có | Lọc theo Academic Year, Status; Total Spending, Successful, Failed của campaign |
| **SCR-08** | Campaign Name | Text, tối đa 150 ký tự | HQ User nhập | Có | Có |  |
| **SCR-08** | Academic Year | Dropdown | academic\_years (R3) | Có | Có | Chỉ DRAFT hoặc ACTIVE |
| **SCR-08** | Age Range: Minimum, Maximum Age | Integer | HQ User nhập | Có | Không | \$7 \\le \\text{Min} \\le \\text{Max} \\le 15\$; nhập cả hai hoặc không nhập |
| **SCR-08** | Account Balance: operator, threshold | Enum, Decimal(18,2) | HQ User chọn, nhập | Có | Không | Toán tử \<, \<=, \>, \>=, \=; ngưỡng không âm; nhập cả hai hoặc không |
| **SCR-08** | Schooling Status: Actively Enrolled | Checkbox | HQ User chọn | Có | Không | Bật thì criterion này thỏa với học sinh Actively Enrolled trong Academic Year |
| **SCR-08** | School | Multi-select | Master data trường (R3, TBC) | Có | Không | Chọn một hoặc nhiều trường; đã thêm criterion thì cần ít nhất một giá trị (MSG-0224) |
| **SCR-08** | Academic Level | Multi-select enum PRIMARY, SECONDARY | HQ User chọn | Có | Không | Chọn một hoặc cả hai; đã thêm criterion thì cần ít nhất một giá trị (MSG-0224) |
| **SCR-08** | Class | Multi-select | Master data lớp của Academic Year (R3, TBC) | Có | Không | Chỉ hiện lớp thuộc Academic Year đã chọn, kèm tên trường; đổi Academic Year thì bỏ các lớp không thuộc năm mới; cần ít nhất một giá trị (MSG-0224) |
| **SCR-08** | Top-Up Amount per account | Decimal(18,2), SGD | HQ User nhập | Có | Có | Lớn hơn 0; không vượt hạn mức mỗi lần (TBC) |
| **SCR-08** | Eligibility Date | Date | HQ User chọn | Có | Có | Mặc định ngày hiện tại; mốc tính tuổi, tình trạng đi học, trường, cấp học và lớp |
| **SCR-09** | Cột preview | Student Name, Age, Balance, Schooling Status, School, Academic Level, Class, Matched Criteria, Top-Up Amount | Tính | Không | Có | 20 dòng mỗi trang |
| **SCR-09** | Total accounts, Total amount (forecast), Previewed at | Integer, Decimal, Datetime | Tính | Không | Có | Chỉ để xem; Confirm chỉ bị vô hiệu khi không có tài khoản eligible |
| **SCR-11** | Cột danh sách run | Campaign Code, Eligibility Date, Status, Total, Successful, Failed, Total credited, Started at, Completed at | Run | Không | Có |  |
| **SCR-12** | Cột run item | Student, Account Number, Age, Balance, Schooling Status, Amount, Outcome, Failure Reason, Transaction Reference | Run item | Không | Có | Lọc theo Outcome; nút Export CSV, Retry failed |
| **SCR-12** | Run summary | Integer, Decimal(18,2) | Tính | Không | Có | Total Spending (Total credited), Successful, Failed (số lượng và số tiền), số ReconciliationRequired |

   10. ### **4.2. Thực thể dữ liệu liên quan**

       1. #### ***Campaign (topup\_campaigns)***

* Id: VARCHAR(50) \- PK  
* Code: NVARCHAR(50) \- Duy nhất trong AcademicYearId  
* Name: NVARCHAR(150)  
* AcademicYearId: UNIQUEIDENTIFIER \- FK logic tới academic\_years (R3)  
* AmountPerAccount, CurrencyCode: DECIMAL(18,2), CHAR(3) \- Số tiền lớn hơn 0; mặc định SGD  
* EligibilityDate: DATE \- Bắt buộc; mặc định ngày hiện tại  
* Status: INT \- 1 Draft, 2 Running, 3 Completed, 4 Cancelled  
* DefinitionVersion, PreviewedVersion, PreviewedAt: INT, INT, DATETIME2(3) \- DefinitionVersion tăng mỗi lần sửa; chỉ Confirm được khi PreviewedVersion bằng DefinitionVersion  
* ConfirmedBy, ConfirmedAt: VARCHAR(50), DATETIME2(3) \- IAM ID của HQ User xác nhận  
* CreatedBy, CreatedAt, UpdatedAt, RowVersion: VARCHAR(50), DATETIME2(3), ROWVERSION \- UTC; RowVersion là token kiểm soát đồng thời lạc quan  
* *Giá trị dẫn xuất (không lưu):* Top-Up Summary của campaign cộng dồn từ các Run thuộc campaign: Total Spending là tổng TotalCredited; Successful, Failed là tổng SuccessfulCount, FailedCount.

#### ***Criterion (topup\_campaign\_criteria)***

* Id, CampaignId: VARCHAR(50) \- PK, FK Campaign  
* CriterionType: INT \- 1 AGE\_RANGE, 2 BALANCE, 3 SCHOOLING\_STATUS, 4 SCHOOL, 5 ACADEMIC\_LEVEL, 6 CLASS; duy nhất theo (CampaignId, CriterionType). Các criterion của một campaign kết hợp bằng OR. Thêm loại mới không đổi cấu trúc bảng  
* MinAge, MaxAge: SMALLINT \- Bắt buộc khi AGE\_RANGE, cấm ở loại khác; \$7 \\le \\text{MinAge} \\le \\text{MaxAge} \\le 15\$  
* BalanceOperator, BalanceThreshold: INT, DECIMAL(18,2) \- Bắt buộc khi BALANCE; 1 LT, 2 LTE, 3 GT, 4 GTE, 5 EQ; ngưỡng không âm  
* RequireActivelyEnrolled: BIT \- Bắt buộc khi SCHOOLING\_STATUS  
* Loại SCHOOL, ACADEMIC\_LEVEL, CLASS lưu giá trị chọn ở bảng topup\_campaign\_criterion\_values bên dưới; cần ít nhất một giá trị

#### ***Criterion Value (topup\_campaign\_criterion\_values)***

* Id, CriterionId: VARCHAR(50) \- PK, FK Criterion  
* SchoolId: UNIQUEIDENTIFIER \- FK logic tới trường (R3, TBC); bắt buộc khi SCHOOL, cấm ở loại khác  
* AcademicLevel: INT \- 1 PRIMARY, 2 SECONDARY; bắt buộc khi ACADEMIC\_LEVEL, cấm ở loại khác  
* ClassId: UNIQUEIDENTIFIER \- FK logic tới lớp (R3, TBC); bắt buộc khi CLASS, cấm ở loại khác; lớp phải thuộc Academic Year của campaign  
* Duy nhất theo (CriterionId, giá trị đã chọn)

#### ***Run (topup\_campaign\_runs)***

* Id, CampaignId: VARCHAR(50) \- PK, FK Campaign  
* TriggeredBy: VARCHAR(50) \- IAM ID của HQ User đã xác nhận campaign  
* EligibilityDate: DATE \- Sao chép từ campaign lúc bắt đầu run, không đổi  
* DefinitionVersion, AmountPerAccount: INT, DECIMAL(18,2) \- Snapshot tại lúc bắt đầu; sửa campaign không đổi run đã tạo  
* Status: INT \- 1 Pending, 2 Running, 3 Completed, 4 CompletedWithErrors, 5 Stopped  
* TotalAccounts, SuccessfulCount, FailedCount, ReconciliationCount: INT \- Không âm; ReconciliationCount là một phần của FailedCount  
* TotalCredited: DECIMAL(18,2) \- Tổng các khoản Successful của run; là Total Spending của run  
* StartedAt, CompletedAt, CreatedAt, UpdatedAt, RowVersion: DATETIME2(3), ROWVERSION \- UTC. Index duy nhất trên CampaignId (mỗi campaign một run)

#### ***Run Item (topup\_run\_items)***

* Id, RunId: VARCHAR(50) \- PK, FK Run; duy nhất theo (RunId, EducationAccountId)  
* EducationAccountId: UNIQUEIDENTIFIER \- FK logic tới EA (Function 1\)  
* AccountNumber, StudentProfileId: VARCHAR(50), UNIQUEIDENTIFIER \- Tham chiếu hiển thị; NRIC lấy qua Student Profile, không sao chép  
* MatchedCriteria: VARCHAR(100) \- Danh sách loại criterion tài khoản thỏa ở lần đánh giá gần nhất (ví dụ AGE\_RANGE,CLASS); dùng để hiển thị và audit  
* AgeAtEligibility, BalanceSnapshot, SchoolingStatusSnapshot, ExpectedAmount: SMALLINT, DECIMAL(18,2), INT, DECIMAL(18,2) \- Giá trị lúc lập danh sách và lúc đánh giá; dùng để hiển thị và audit  
* Outcome: INT \- 1 Pending, 2 Successful, 3 Failed, 4 ReconciliationRequired  
* FailureCode, FailureReason: VARCHAR(50), NVARCHAR(500) \- Bắt buộc khi Failed; mã lỗi (gồm lý do không còn đủ điều kiện như CRITERIA\_NOT\_MATCH, RUN\_STOPPED) và nguyên nhân đã làm sạch  
* FundingReference: NVARCHAR(50) \- Duy nhất; sinh một lần, dùng lại khi thử lại  
* TopUpTransactionId: VARCHAR(50) \- FK Transaction; bắt buộc khi Successful  
* ProcessedAt, RowVersion: DATETIME2(3), ROWVERSION \- UTC

#### ***Top-Up Transaction (topup\_transactions)***

* Id: VARCHAR(50) \- PK  
* TransactionReference: NVARCHAR(50) \- Duy nhất  
* SourceType: INT \- 1 Individual, 2 Bulk  
* EducationAccountId: UNIQUEIDENTIFIER \- FK logic tới EA (Function 1\)  
* RunItemId: VARCHAR(50) \- FK Run Item; bắt buộc khi Bulk, cấm ở loại khác  
* InitiatedByUserId: VARCHAR(50) \- IAM ID của HQ User; với Bulk là HQ User đã xác nhận campaign  
* IdempotencyKey: VARCHAR(100) \- Duy nhất theo (InitiatedByUserId, IdempotencyKey); dùng cho Individual  
* FundingReference: NVARCHAR(50) \- Duy nhất; gửi sang Function 1 để đối soát  
* Amount, CurrencyCode: DECIMAL(18,2), CHAR(3) \- Lớn hơn 0; SGD  
* Reason: NVARCHAR(200) \- Bắt buộc khi Individual; không hiển thị cho Parent  
* Status: INT \- 1 Pending, 2 Success, 3 Failed, 4 ReconciliationRequired  
* FailureCode, FailureReason: VARCHAR(50), NVARCHAR(500) \- Đã làm sạch  
* EducationAccountTransactionId: BIGINT \- ID logic sổ cái Function 1; bắt buộc khi Success; duy nhất  
* CreatedAt, UpdatedAt, CompletedAt, RowVersion: DATETIME2(3), ROWVERSION \- UTC; CompletedAt rỗng khi đang xử lý

*Giá trị dẫn xuất (không lưu):* Top-Up Summary ở SCR-05 tính theo bộ lọc. Total Spending là tổng Amount các giao dịch Success. Successful và Failed: top-up lẻ đếm theo Status của giao dịch (Failed gồm ReconciliationRequired), bulk đếm theo Outcome của topup\_run\_items. Số tiền Failed là số tiền dự kiến chưa ghi có (ExpectedAmount của run item, hoặc Amount của giao dịch lẻ Failed).

2. #### ***Tham chiếu ngoài & Audit Log***

* **Function 1:** EA, sổ cái, API ghi có, Closure Eligibility Check (Function 2 chỉ lưu ID logic: EducationAccountId, EducationAccountTransactionId).  
* **R1:** Student Profile (họ tên, NRIC, DOB, Citizenship).  
* **R3:** academic\_years, student\_school\_enrollments, liên kết Student–EA.  
* **AuditLog:** actor, action, entity, entity\_id, old\_value, new\_value, timestamp. Ghi: tạo, sửa, xác nhận, hủy campaign; bắt đầu, dừng, kết thúc run; mỗi top-up.

## 

## **5\. Validation**

11. ### **5.1. Thông báo lỗi hiển thị cho HQ User**

| Mã | Nội dung hiển thị | Hành vi UI |
| ----- | ----- | ----- |
| **MSG-0201** | No Education Account found. Check the Account Number or NRIC and try again. | Giữ ở SCR-01 |
| **MSG-0202** | Enter an amount greater than 0, with up to 2 decimal places. | Giữ ở SCR-02, đánh dấu ô nhập |
| **MSG-0203** | The amount is more than the limit for one top-up. (TBC, OQ-03) | Giữ ở SCR-02 hoặc SCR-08 |
| **MSG-0204** | This Education Account is not active. Top-up is not allowed. | Vô hiệu ô nhập số tiền |
| **MSG-0205** | We could not check the account status. No amount was credited. Please try again later. | SCR-04, cho thử lại; không đổi dữ liệu |
| **MSG-0206** | Enter a reason (up to 200 characters). | Giữ ở SCR-02 |
| **MSG-0207** | Top-up completed. Reference: {Transaction Reference}. | SCR-04, hiện số dư mới |
| **MSG-0208** | The top-up could not be completed. No amount was credited. | SCR-04, cho thử lại |
| **MSG-0209** | We are verifying this top-up. Please check the history later. | SCR-04, trạng thái đang xác minh |
| **MSG-0214** | No accounts match these criteria. | SCR-09, vô hiệu nút Confirm |
| **MSG-0215** | This campaign is running and cannot be changed. | Mọi nút sửa bị vô hiệu |
| **MSG-0216** | The campaign has changed. Preview again before confirming. | Quay về SCR-09, bắt buộc preview lại |
| **MSG-0217** | Enter an age range from 7 to 15, with the minimum not more than the maximum. | SCR-08, đánh dấu ô nhập |
| **MSG-0218** | Enter a balance operator and an amount of 0 or more. | SCR-08, đánh dấu ô nhập |
| **MSG-0220** | This Academic Year is closed. Choose another Academic Year. | SCR-08 |
| **MSG-0221** | Add at least one criterion. | SCR-08 |
| **MSG-0224** | Select at least one value for {criterion}, or remove the criterion. | SCR-08, đánh dấu criterion |
| **MSG-0222** | This campaign was changed by another user. Refresh and try again. | Làm mới dữ liệu |
| **MSG-0001** | Enter your \<field\> | Bỏ trống trường bắt buộc, báo theo từng trường |
| **MSG-0002** | Your session has expired. Please log in again. | Chuyển đến đăng nhập Admin Portal |
| **MSG-0003** | You do not have permission to perform this action. | Quay về màn hình chính |

    12. ### **5.2. Tiêu chí chấp nhận (AC)**

        1. #### ***Individual Top-Up***

| ID | Given / When / Then |
| ----- | ----- |
| **AC-01** | **Given** HQ User, **when** tìm theo Account Number hoặc NRIC đầy đủ, **then** thấy đúng một EA với holder, status, balance; NRIC hiển thị che một phần. |
| **AC-02** | **Given** Account Number hoặc NRIC không có EA, hoặc NRIC nhập thiếu, thừa ký tự hoặc chỉ khớp một phần, **when** tìm, **then** báo MSG-0201, không hiển thị tài khoản hay danh sách gợi ý nào. |
| **AC-03** | **Given** EA Active, **when** HQ User xác nhận top-up 50.00, **then** số dư tăng đúng 50.00 một lần, transaction Success, có mã bút toán của Function 1, Transaction Reference và audit log. |
| **AC-04** | **Given** EA Closed, **when** xác nhận top-up, **then** bị từ chối, số dư không đổi, transaction Failed được ghi log. |
| **AC-05** | **Given** học sinh vừa đủ 16 tuổi và EA chưa Closed, **when** xác nhận top-up, **then** F02 đóng EA trước, top-up bị từ chối, số dư không đổi. |
| **AC-06** | **Given** Government API không phản hồi, **when** xác nhận top-up, **then** không ghi có, Account Status không tự đổi, báo MSG-0205. |
| **AC-07** | **Given** HQ User bấm xác nhận hai lần, **then** chỉ tạo một transaction và chỉ ghi có một lần. |
| **AC-08** | **Given** Function 1 timeout sau khi nhận lệnh ghi có, **when** hỏi lại bằng FundingReference, **then** đã ghi thì Success đúng một lần; không xác định được thì ReconciliationRequired, và số dư không bị ghi có lần hai. |
| **AC-09** | **Given** số tiền bằng 0, âm, hoặc có hơn 2 chữ số thập phân, **then** bị từ chối MSG-0202, không có dữ liệu nào đổi. |
| **AC-10** | **Given** top-up thất bại, **then** số dư không đổi và lý do được ghi log. |
| **AC-11** | **Given** School User hoặc Parent gọi API Top-Up, **then** bị từ chối 403 và ghi log bảo mật. |

           2. #### ***Cấu hình Campaign, Preview***

| ID | Given / When / Then |
| ----- | ----- |
| **AC-18** | **Given** Academic Year, ít nhất một criterion, số tiền hợp lệ, **when** Save, **then** campaign được tạo ở trạng thái Draft với Code do hệ thống sinh. |
| **AC-19** | **Given** Minimum Age lớn hơn Maximum Age, hoặc nằm ngoài 7 đến 15, **then** bị từ chối MSG-0217. |
| **AC-20** | **Given** campaign có criterion tuổi 7 đến 12, số dư dưới SGD 100 và Actively Enrolled, **when** Preview, **then** danh sách gồm mọi EA Active thỏa ít nhất một criterion (OR), kèm Student Name, Age, Balance, Schooling Status, School, Academic Level, Class, Matched Criteria, Top-Up Amount; tài khoản thỏa nhiều criterion chỉ xuất hiện một lần; tổng số tài khoản và tổng tiền đúng. |
| **AC-21** | **Given** học sinh có enrollment đã kết thúc trước Eligibility Date, hoặc là PR hoặc IS không có EA, **then** không xuất hiện trong preview qua criterion Schooling Status, School, Academic Level hay Class; PR hoặc IS không bao giờ xuất hiện. |
| **AC-22** | **Given** campaign đã lưu, **when** HQ User Preview, **then** hiển thị tổng số tài khoản và tổng tiền dự kiến (Total amount) để kiểm tra trước khi Confirm; Confirm bật khi có ít nhất một tài khoản eligible. |
| **AC-23** | **Given** đã preview, **when** HQ User sửa criterion hoặc số tiền, **then** campaign về Draft và phải preview lại mới Confirm được. |
| **AC-24** | **Given** hai campaign cùng Academic Year với criterion khác nhau, **then** cả hai chạy được; tài khoản thuộc cả hai nhận hai khoản và preview cảnh báo. |

           3. #### ***Chạy và kết quả***

| ID | Given / When / Then |
| ----- | ----- |
| **AC-25** | **Given** campaign đã Confirm, **when** HQ User Confirm, **then** mỗi tài khoản eligible được ghi có đúng một lần; run summary có Successful, Failed; số tiền tổng khớp tổng các giao dịch Success. |
| **AC-26** | **Given** giữa preview và lúc chạy một tài khoản không còn thỏa criterion nào (ví dụ số dư tăng vượt ngưỡng và không thỏa criterion khác), **then** bị Failed (CRITERIA\_NOT\_MATCH), không ghi có; nếu vẫn thỏa ít nhất một criterion thì vẫn được ghi có. |
| **AC-27** | **Given** tài khoản bị đóng trước lúc chạy, **then** Failed (EA\_NOT\_ACTIVE), không ghi có; **given** học sinh không còn học và không còn thỏa criterion nào (ví dụ campaign chỉ có Schooling Status), **then** Failed (CRITERIA\_NOT\_MATCH). |
| **AC-28** | **Given** run có 5 tài khoản eligible, số tiền mỗi tài khoản 100.00, **when** kết quả là 3 Successful, 2 Failed, **then** run summary hiển thị Total Spending 300.00, Successful 3, Failed 2; các số này được cộng vào Top-Up Summary của campaign. |
| **AC-29** | **Given** Government API lỗi với một số tài khoản, **then** các tài khoản đó Failed (ELIGIBILITY\_CHECK\_UNAVAILABLE), run vẫn xử lý các tài khoản khác, trạng thái CompletedWithErrors. |
| **AC-30** | **Given** có run item Failed, **when** Retry failed, **then** chỉ các item Failed được thử lại với cùng FundingReference và mỗi tài khoản ghi có tối đa một lần. |
| **AC-31** | **Given** server khởi động lại giữa run, **then** run tiếp tục từ các item chưa xử lý, không ghi có trùng. |
| **AC-32** | **Given** run Running, **when** HQ User Stop, **then** các tài khoản còn lại Failed (RUN\_STOPPED), các khoản đã ghi có giữ nguyên. |
| **AC-33** | **Given** run item Failed, **then** số dư EA tương ứng không đổi. |
| **AC-34** | **Given** campaign Running, **when** HQ User sửa hoặc hai HQ User thao tác đồng thời, **then** bị từ chối MSG-0215 hoặc MSG-0222. |

           4. #### ***Xác nhận và chạy***

| ID | Given / When / Then |
| ----- | ----- |
| **AC-35** | **Given** preview đạt và campaign Draft, **when** HQ User Confirm, **then** campaign chuyển Running và run bắt đầu ngay; không có bước chọn chế độ chạy hay lịch chạy. |
| **AC-36** | **Given** HQ User bấm Confirm hai lần, hoặc hai HQ User Confirm cùng lúc, **then** chỉ tạo một run; campaign đã Running không còn Confirm hay sửa được (MSG-0215). |

           5. #### ***Audit và Parent (R8)***

| ID | Given / When / Then |
| ----- | ----- |
| **AC-39** | **Given** mọi giao dịch Top-Up, **then** có Transaction Reference, số tiền, thời điểm, người thực hiện, campaign và run (nếu có); không xóa cứng. |
| **AC-40** | **Given** top-up thành công, **when** Parent xem Transaction History (R8), **then** thấy Type Top-up, Money in, Status Completed; Description không chứa lý do nội bộ. |

           6. #### ***Top-Up Summary khi xem history***

| ID | Given / When / Then |
| ----- | ----- |
| **AC-42** | **Given** Top-Up History có bộ lọc khoảng ngày và nguồn, **when** HQ User mở SCR-05, **then** khối Top-Up Summary hiển thị Total Spending bằng tổng Amount các giao dịch Success trong bộ lọc, cùng số lượng Successful, Failed; đổi bộ lọc thì số liệu đổi theo. |
| **AC-43** | **Given** campaign đã chạy xong, **when** xem SCR-07, **then** Total Spending, Successful, Failed của campaign khớp với run tương ứng ở SCR-11. |
| **AC-44** | **Given** run item Failed hoặc ReconciliationRequired, **then** số tiền đó không được cộng vào Total Spending; chỉ khi item chuyển sang Successful mới cộng. |
| **AC-45** | **Given** SCR-05 lọc nguồn Individual, **then** Total Spending chỉ gồm top-up lẻ Success. |

           7. #### ***Criterion OR, School, Academic Level, Class***

| ID | Given / When / Then |
| ----- | ----- |
| **AC-46** | **Given** campaign có criterion Age Range 7 đến 9 và criterion Class chọn lớp 5A, **when** Preview, **then** danh sách gồm học sinh tuổi 7 đến 9 hoặc thuộc lớp 5A; học sinh thỏa cả hai chỉ xuất hiện một lần và nhận một khoản. |
| **AC-47** | **Given** criterion School chọn hai trường, **when** Preview, **then** gồm học sinh có enrollment hiệu lực tại Eligibility Date thuộc một trong hai trường. |
| **AC-48** | **Given** criterion Academic Level chọn Primary, **when** Preview, **then** chỉ gồm học sinh có cấp học hiện tại là Primary; chọn cả Primary và Secondary thì gồm cả hai cấp. |
| **AC-49** | **Given** criterion School, Academic Level hoặc Class chưa có giá trị nào, **when** Save, **then** bị từ chối MSG-0224. |
| **AC-50** | **Given** criterion Class đã chọn lớp, **when** HQ User đổi Academic Year, **then** các lớp không thuộc năm mới bị bỏ chọn và danh sách lớp hiển thị theo năm mới. |

## **6\. Appendices**

13. ### **Appendix A. Trạng thái Campaign, Run, Run Item và Transaction**

| Đối tượng | Từ | Sang | Điều kiện | Ghi chú |
| ----- | ----- | ----- | ----- | ----- |
| **Campaign** | (mới) | Draft | HQ User Save | Sửa được |
| **Campaign** | Draft | Running | Preview đạt, HQ User Confirm | Run bắt đầu ngay; không sửa được nữa |
| **Campaign** | Running | Completed | Run kết thúc (Completed, CompletedWithErrors hoặc Stopped) | Không sửa được nữa |
| **Campaign** | Draft | Cancelled | HQ User Cancel | Không tạo run |
| **Run** | (mới) | Pending | HQ User Confirm campaign | Khóa campaign |
| **Run** | Pending | Running | Bắt đầu lập danh sách và xử lý |  |
| **Run** | Running | Completed | Hết danh sách, không còn run item Failed hoặc ReconciliationRequired |  |
| **Run** | Running | CompletedWithErrors | Hết danh sách, còn run item Failed hoặc ReconciliationRequired |  |
| **Run** | Running | Stopped | HQ User Stop | Item còn lại Failed (RUN\_STOPPED) |
| **Run** | CompletedWithErrors | Completed | Thử lại hoặc vận hành xử lý hết Failed và ReconciliationRequired |  |
| **Run Item** | (mới) | Pending | Lập danh sách khi run bắt đầu |  |
| **Run Item** | Pending | Successful | Function 1 ghi có thành công | Số dư tăng một lần |
| **Run Item** | Pending | Failed | Lỗi xử lý hoặc kiểm tra; không còn đủ điều kiện khi chạy; run bị Stop | Số dư không đổi; có Failure Code |
| **Run Item** | Pending | ReconciliationRequired | Không xác định được kết quả ghi có | Tính trong nhóm Failed |
| **Run Item** | Failed | Successful hoặc Failed | HQ User Retry failed | Dùng lại FundingReference |
| **Run Item** | ReconciliationRequired | Successful hoặc Failed | Bộ phận vận hành xử lý |  |
| **Transaction** | (mới) | Pending | HQ User xác nhận, hoặc run item bắt đầu ghi có | Có FundingReference |
| **Transaction** | Pending | Success | Function 1 ghi sổ cái thành công | Có mã bút toán của Function 1 |
| **Transaction** | Pending | Failed | Không đủ điều kiện, hoặc Function 1 báo lỗi | Số dư không đổi |
| **Transaction** | Pending | ReconciliationRequired | Không xác định được kết quả sau khi hỏi lại Function 1 | Cảnh báo vận hành |
| **Transaction** | ReconciliationRequired | Success hoặc Failed | Bộ phận vận hành xử lý |  |

    14. ### **Appendix B. Open Questions & Assumptions**

| ID | Câu hỏi | Ảnh hưởng | Phương án tạm trong FS |
| ----- | ----- | ----- | ----- |
| **OQ-01** | Hạn mức tối đa mỗi lần top-up lẻ và mỗi tài khoản trong bulk | BR-F2-03, BR-F2-19, MSG-0203 | Chưa đặt hạn mức; cấu hình được |
| **OQ-03** | Có cần phê duyệt hai bước (maker-checker) cho campaign | OOS \#6 | Không; HQ User xác nhận một bước, có audit |
| **OQ-06** | Actively Enrolled chỉ dựa trên enrollment hay cần cả class assignment | BR-F2-17 | Actively Enrolled chỉ dựa trên enrollment; riêng criterion Class dùng phân lớp của R3 |
| **OQ-07** | Campaign Eligibility Date dùng ngày xác nhận hay một ngày cố định (ví dụ đầu năm học) | BR-F2-16 | HQ User chọn ở SCR-08, mặc định ngày hiện tại |
| **OQ-08** | Description của top-up hiển thị cho Parent: tên campaign hay "MOE Top-up" chung | Mục 2.2 (R8) | "MOE Top-up" chung |
| **OQ-09** | Tài khoản thỏa nhiều campaign cùng kỳ: cho nhận nhiều khoản hay chặn | BR-F2-28 | Cho phép, preview cảnh báo |
| **OQ-11** | Ngưỡng thời gian Pending trước khi chuyển ReconciliationRequired; chu kỳ hỏi lại Function 1 | EX-05 | Do Dev cấu hình; không tự Failed |
| **OQ-12** | Nguồn dữ liệu School, Academic Level, Class ở R3 (bảng, trường dữ liệu, cách xác định cấp học) | BR-F2-14, SCR-08 | Tạm dùng master data trường, cấp học, lớp và phân lớp của R3; tên bảng TBC |

        15. ### **Appendix C. Danh sách màn hình**

| Mã | Màn hình | Thành phần chính | Hành động | Trạng thái UI |
| ----- | ----- | ----- | ----- | ----- |
| **SCR-01** | Individual Top-Up: Tìm EA | Chọn kiểu tìm, ô nhập Account Number hoặc NRIC | Search | Loading, Empty (không có kết quả), Error |
| **SCR-02** | Xác minh chủ tài khoản và nhập số tiền | Tên, NRIC che một phần, tuổi, Account Number, Account Status, Current Balance, ô Top-Up Amount, Reason | Continue, quay lại | Ô nhập bị vô hiệu khi EA không Active |
| **SCR-03** | Xem lại và xác nhận | Chủ tài khoản, số tiền, số dư sau top-up, lý do | Xác nhận, hủy | Nút xác nhận bị vô hiệu sau khi bấm; Processing |
| **SCR-04** | Kết quả top-up | Trạng thái, Transaction Reference, số dư mới, thông báo | Về SCR-01, xem Top-Up History | Success, Failed, Verifying |
| **SCR-05** | Top-Up History | Bộ lọc, Top-Up Summary (Total Spending, Successful, Failed), bảng giao dịch | Lọc, xem chi tiết | Loading, Empty, Error |
| **SCR-07** | Danh sách Campaign | Bảng campaign (kèm Total Spending, Successful, Failed), bộ lọc Academic Year, Status | Create, mở, Cancel | Loading, Empty |
| **SCR-08** | Cấu hình Campaign | Name, Academic Year, criterion (Age Range, Account Balance, Schooling Status, School, Academic Level, Class), Top-Up Amount, Eligibility Date | Save, Preview | Draft; lỗi từng trường |
| **SCR-09** | Preview | Danh sách eligible, tổng số tài khoản, tổng tiền dự kiến, cảnh báo trùng campaign, thời điểm preview | Confirm, quay lại sửa | Confirm bị vô hiệu khi không có tài khoản |
| **SCR-11** | Danh sách Run | Bảng run: trạng thái, số liệu, Eligibility Date | Mở run, Stop | Pending, Running, Completed, CompletedWithErrors, Stopped |
| **SCR-12** | Run summary và Run Item | Total Spending, Successful, Failed (số lượng và tiền), bảng run item, bộ lọc Outcome | Export CSV, Retry failed | Loading, Empty, Error |

