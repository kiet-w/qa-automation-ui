# FS-06: FAS Budget & Statistics Tracking (Requirement 6)

> **Phân hệ**: Admin Portal (MOE HQ & School Users)  
> **Requirement**: R6 – FAS Budget & Statistics Tracking  
> **Product Backlog**: PB-21 (Sprint 3) | **User Story**: US-07 (FR7)  
> **Phiên bản baseline**: Official FSD Baseline (R6 — analysis.docx - Version 0.1 Draft for BA Review)  
> **Trạng thái**: Production Ready / Fully Aligned  

---

Document Version: 0.1 – Draft for BA Review / Client Clarification
Project: Education Account Management System
Requirement Reference: R6 – FAS Budget & Statistics
Portal: Administration Portal (Admin Portal)
Priority: TBC – cần đối chiếu Agile Requirements
Scope: Happy Case
Status: Draft – bao gồm các yêu cầu đã xác định và các nội dung chờ xác nhận.

# 1. Introduction

## 1.1. Overview

R6 – FAS Budget & Statistics cung cấp chức năng thiết lập ngân sách và theo dõi thống kê các khoản trợ cấp Financial Assistance Scheme (FAS) đã được cấp thông qua Admin Portal.

Requirement bao gồm ba nhóm chức năng chính:

R6.1 – Budget Management: Cho phép người dùng thiết lập và xem ngân sách của chương trình FAS thuộc phạm vi quản lý.

R6.2 – Subsidy Statistics: Cho phép người dùng xem thống kê các khoản trợ cấp đã được granted.

R6.3 – Budget Tracking: Cho phép người dùng theo dõi tình hình sử dụng ngân sách và ngân sách còn lại nếu được xác nhận trong phạm vi yêu cầu.

Phạm vi quản lý phụ thuộc vào loại người dùng:

MOE HQ User: Quản lý và theo dõi ngân sách, thống kê của MOEFAS trong phạm vi được phân quyền.

School User: Quản lý và theo dõi ngân sách, thống kê của SBFAS thuộc trường mình.

R6 tập trung vào việc quản lý ngân sách và cung cấp thông tin thống kê. Việc tạo, phê duyệt hoặc thay đổi trạng thái của một Grant không mặc định thuộc phạm vi requirement này.

## 1.2. Users / Actors

| Actor | Description | Responsibility |
| :--- | :--- | :--- |
| MOE HQ User | Người dùng thuộc MOE HQ | Thiết lập ngân sách MOEFAS và xem thống kê, tình hình sử dụng ngân sách MOEFAS trong phạm vi được phân quyền. |
| School User | Người dùng thuộc một trường | Thiết lập ngân sách SBFAS và xem thống kê, tình hình sử dụng ngân sách SBFAS của trường mình. |
| System | Hệ thống | Lưu và hiển thị ngân sách đã cấu hình; tổng hợp, hiển thị thống kê trợ cấp và cung cấp thông tin theo dõi ngân sách theo các quy tắc nghiệp vụ đã xác nhận. |

## 1.3. Related Requirements

| Requirement | Description |
| :--- | :--- |
| R6.1 | Budget Management |
| R6.2 | Subsidy Statistics |
| R6.3 | Budget Tracking |

Các requirement liên quan đến quy trình tạo, xử lý, phê duyệt, thay đổi hoặc thu hồi Grant cần được đối chiếu với requirement tương ứng để xác định nguồn dữ liệu và thời điểm cập nhật cho R6.

# 2. Confirmed Requirements

| ID | Requirement |
| :--- | :--- |
| R6-01 | Hệ thống hỗ trợ quản lý ngân sách cho MOEFAS và SBFAS. |
| R6-02 | MOE HQ User có thể thiết lập ngân sách MOEFAS trong phạm vi được phân quyền. |
| R6-03 | School User có thể thiết lập ngân sách SBFAS thuộc trường mình. |
| R6-04 | Hệ thống lưu và hiển thị Budget Amount đã cấu hình. |
| R6-05 | MOE HQ User có thể xem thống kê các khoản MOEFAS subsidy đã được granted. |
| R6-06 | School User có thể xem thống kê các khoản SBFAS subsidy đã được granted tại trường mình. |
| R6-07 | Hệ thống hiển thị tổng số tiền subsidy đã được granted theo từng loại FAS trong phạm vi người dùng được phép xem. |
| R6-08 | Hệ thống cung cấp thông tin về tình hình sử dụng ngân sách dựa trên Budget Amount và số tiền trợ cấp được tính là đã sử dụng. |
| R6-09 | Hệ thống chỉ hiển thị dữ liệu thống kê thuộc phạm vi người dùng được phép xem. |
| R6-10 | Hệ thống hiển thị Remaining Budget nếu chức năng này nằm trong phạm vi yêu cầu được thống nhất. |

Các yêu cầu R6-08 và R6-10 cần được làm rõ về công thức và điều kiện áp dụng trước khi chốt thiết kế chi tiết.

# 3. Business Rules

| ID | Business Rule |
| :--- | :--- |
| BR6.01 | MOE HQ User quản lý MOEFAS; School User quản lý SBFAS thuộc School mình. |
| BR6.02 | Thống kê phải phản ánh đúng các khoản trợ cấp thuộc phạm vi người dùng được phép xem. |
| BR6.03 | Budget Amount được hiển thị phải phản ánh ngân sách đã được cấu hình và lưu trong hệ thống. |
| BR6.04 | Tổng Subsidy Amount Granted phải được tổng hợp theo định nghĩa nghiệp vụ được thống nhất. |
| BR6.05 | Cách xác định số tiền trợ cấp được tính là ngân sách đã sử dụng phải được thống nhất trước khi hoàn thiện chức năng Budget Tracking. |

BR6.03–BR6.05 là các quy tắc được diễn giải từ requirement để phục vụ đặc tả chức năng; cần xác nhận với khách hàng trước khi coi là business rules chính thức.

# 4. Functional Scope

## 4.1. R6.1 – Budget Management

| Feature ID | Feature | Functional Description |
| :--- | :--- | :--- |
| R6.1.1 | Manage MOEFAS Budget | MOE HQ User có thể thiết lập ngân sách cho MOEFAS. |
| R6.1.2 | Manage SBFAS Budget | School User có thể thiết lập ngân sách SBFAS thuộc trường mình. |
| R6.1.3 | View Configured Budget | Người dùng có thể xem ngân sách đã thiết lập trong phạm vi quyền hạn của mình. |

## 4.2. R6.2 – Subsidy Statistics

| Feature ID | Feature | Functional Description |
| :--- | :--- | :--- |
| R6.2.1 | View MOEFAS Subsidy Statistics | MOE HQ User có thể xem thống kê MOEFAS subsidies đã được granted. |
| R6.2.2 | View SBFAS Subsidy Statistics | School User có thể xem thống kê SBFAS subsidies đã được granted tại trường mình. |
| R6.2.3 | View Total Subsidy Amount Granted | Hệ thống hiển thị tổng số tiền subsidy đã được granted theo từng loại FAS trong phạm vi người dùng được phép xem. |

## 4.3. R6.3 – Budget Tracking

| Feature ID | Feature | Functional Description |
| :--- | :--- | :--- |
| R6.3.1 | Track MOEFAS Budget Usage | MOE HQ User có thể theo dõi tình hình sử dụng ngân sách MOEFAS dựa trên dữ liệu subsidy đã được granted. |
| R6.3.2 | Track SBFAS Budget Usage | School User có thể theo dõi tình hình sử dụng ngân sách SBFAS của trường mình. |
| R6.3.3 | View Remaining Budget | Hệ thống hiển thị ngân sách còn lại nếu chức năng này nằm trong phạm vi yêu cầu đã thống nhất. |

# 5. Functional Specification

## 5.1. R6.1.1 – Manage MOEFAS Budget

### 5.1.1. Description

Cho phép MOE HQ User thiết lập ngân sách cho chương trình MOEFAS trong phạm vi được phân quyền.

### 5.1.2. Preconditions

Người dùng đã đăng nhập vào Admin Portal.

Người dùng có quyền quản lý ngân sách MOEFAS.

### 5.1.3. UI Elements

| UI ID | UI Element | Type | Description |
| :--- | :--- | :--- | :--- |
| UI-R6-001 | FAS Type | Label / Read-only field | Hiển thị loại FAS là MOEFAS. |
| UI-R6-002 | Budget Amount | Numeric input | Cho phép nhập số tiền ngân sách cần thiết lập. |
| UI-R6-003 | Save | Button | Lưu ngân sách đã nhập. |
| UI-R6-004 | Cancel | Button | Hủy thao tác đang thực hiện và quay lại màn hình trước đó. |
| UI-R6-005 | Configured Budget Amount | Display field | Hiển thị ngân sách đã được lưu thành công. |

Lưu ý: Các UI Element trên là đề xuất cho thiết kế giao diện dựa trên chức năng đã xác định, không phải danh sách UI đã được khách hàng phê duyệt. Quy tắc định dạng tiền tệ, trường bắt buộc và bố cục cụ thể cần được xác nhận.

### 5.1.4. Main Flow – Happy Case

MOE HQ User truy cập chức năng quản lý ngân sách MOEFAS.

System hiển thị thông tin MOEFAS và Budget Amount đã cấu hình, nếu có.

User nhập Budget Amount cần thiết lập.

User chọn Save.

System lưu Budget Amount.

System hiển thị Budget Amount đã lưu thành công.

### 5.1.5. Expected Result

Ngân sách MOEFAS được lưu trong hệ thống.

Người dùng có thể xem ngân sách đã cấu hình.

Ngân sách thuộc phạm vi quản lý của MOE HQ User.

### 5.1.6. Pending Confirmation

Ngân sách được thiết lập theo năm học, năm tài chính hay một khoảng thời gian khác?

Có cho phép chỉnh sửa ngân sách sau khi đã lưu không?

Nếu cho phép chỉnh sửa, ngân sách mới có áp dụng ngay không?

Có cần lưu lịch sử thay đổi ngân sách không?

## 5.2. R6.1.2 – Manage SBFAS Budget

### 5.2.1. Description

Cho phép School User thiết lập ngân sách cho chương trình SBFAS thuộc trường mình.

### 5.2.2. Preconditions

Người dùng đã đăng nhập vào Admin Portal.

Người dùng có quyền quản lý ngân sách SBFAS của trường mình.

### 5.2.3. UI Elements

| UI ID | UI Element | Type | Description |
| :--- | :--- | :--- | :--- |
| UI-R6-006 | School | Label / Read-only field | Hiển thị trường thuộc phạm vi quản lý của người dùng. |
| UI-R6-007 | FAS Type | Label / Read-only field | Hiển thị loại FAS là SBFAS. |
| UI-R6-008 | Budget Amount | Numeric input | Cho phép nhập số tiền ngân sách SBFAS. |
| UI-R6-009 | Save | Button | Lưu ngân sách SBFAS. |
| UI-R6-010 | Cancel | Button | Hủy thao tác đang thực hiện. |
| UI-R6-011 | Configured Budget Amount | Display field | Hiển thị ngân sách SBFAS đã được lưu. |

### 5.2.4. Main Flow – Happy Case

School User truy cập chức năng quản lý ngân sách SBFAS.

System hiển thị thông tin trường và Budget Amount đã cấu hình, nếu có.

User nhập Budget Amount.

User chọn Save.

System lưu ngân sách SBFAS thuộc trường của User.

System hiển thị ngân sách đã lưu thành công.

### 5.2.5. Expected Result

Ngân sách SBFAS được lưu và hiển thị.

Ngân sách được gắn với trường tương ứng.

School User chỉ quản lý ngân sách SBFAS thuộc trường mình.

### 5.2.6. Pending Confirmation

Một trường có thể có nhiều ngân sách SBFAS theo từng năm học hoặc kỳ ngân sách không?

School User có được chỉnh sửa ngân sách sau khi lưu không?

Có cần hỗ trợ lịch sử thay đổi ngân sách không?

## 5.3. R6.1.3 – View Configured Budget

### 5.3.1. Description

Cho phép người dùng xem Budget Amount đã được cấu hình cho chương trình FAS thuộc phạm vi quản lý.

### 5.3.2. UI Elements

| UI ID | UI Element | Type | Description |
| :--- | :--- | :--- | :--- |
| UI-R6-012 | FAS Type | Display field | Hiển thị loại FAS tương ứng. |
| UI-R6-013 | School | Display field | Hiển thị trường tương ứng đối với SBFAS; việc hiển thị ở MOEFAS cần xác nhận. |
| UI-R6-014 | Budget Amount | Display field | Hiển thị ngân sách đã cấu hình. |
| UI-R6-015 | Edit | Button | Cho phép chỉnh sửa ngân sách nếu được phân quyền và nghiệp vụ cho phép. |

### 5.3.3. Main Flow – Happy Case

User truy cập màn hình xem ngân sách.

System xác định phạm vi dữ liệu theo quyền của User.

System hiển thị loại FAS và Budget Amount đã cấu hình.

Nếu chức năng chỉnh sửa được hỗ trợ và User có quyền, System hiển thị thao tác Edit.

### 5.3.4. Expected Result

User xem được ngân sách đã cấu hình thuộc phạm vi quản lý của mình.

## 5.4. R6.2.1 – View MOEFAS Subsidy Statistics

### 5.4.1. Description

Cho phép MOE HQ User theo dõi thống kê các khoản MOEFAS subsidy đã được granted.

### 5.4.2. Preconditions

Người dùng đã đăng nhập vào Admin Portal.

Người dùng có quyền xem thống kê MOEFAS.

Hệ thống có dữ liệu subsidy phù hợp để tổng hợp.

### 5.4.3. Proposed UI Elements

| UI ID | UI Element | Type | Description |
| :--- | :--- | :--- | :--- |
| UI-R6-016 | Page Title | Label | Hiển thị tiêu đề trang MOEFAS Subsidy Statistics. |
| UI-R6-017 | FAS Type | Display field | Hiển thị loại FAS là MOEFAS. |
| UI-R6-018 | Total Subsidy Amount Granted | Summary field | Hiển thị tổng số tiền trợ cấp MOEFAS đã được granted. |
| UI-R6-019 | Subsidy Statistics Table | Data table | Hiển thị các số liệu thống kê được thống nhất trong phạm vi MOEFAS. |

Các cột chi tiết của Subsidy Statistics Table chưa được xác định đầy đủ trong requirement. Không mặc định bổ sung Student Count, Grant Count, thời gian hoặc các chỉ số khác khi chưa được xác nhận.

### 5.4.4. Main Flow – Happy Case

MOE HQ User truy cập trang MOEFAS Subsidy Statistics.

System lấy dữ liệu MOEFAS subsidy thuộc phạm vi được phép xem.

System tổng hợp dữ liệu theo định nghĩa nghiệp vụ đã thống nhất.

System hiển thị tổng số tiền subsidy đã được granted.

System hiển thị các số liệu thống kê khác nếu đã được xác nhận trong phạm vi chức năng.

### 5.4.5. Expected Result

MOE HQ User xem được thống kê MOEFAS.

Total Subsidy Amount Granted phản ánh dữ liệu thuộc phạm vi được phép xem.

Dữ liệu hiển thị phản ánh các khoản subsidy đã được granted theo định nghĩa nghiệp vụ đã thống nhất.

## 5.5. R6.2.2 – View SBFAS Subsidy Statistics

### 5.5.1. Description

Cho phép School User xem thống kê các khoản SBFAS subsidy đã được granted tại trường mình.

### 5.5.2. Proposed UI Elements

| UI ID | UI Element | Type | Description |
| :--- | :--- | :--- | :--- |
| UI-R6-020 | Page Title | Label | Hiển thị tiêu đề trang SBFAS Subsidy Statistics. |
| UI-R6-021 | School | Display field | Hiển thị trường thuộc phạm vi quản lý của User. |
| UI-R6-022 | FAS Type | Display field | Hiển thị loại FAS là SBFAS. |
| UI-R6-023 | Total Subsidy Amount Granted | Summary field | Hiển thị tổng số tiền SBFAS subsidy đã được granted tại trường. |
| UI-R6-024 | Subsidy Statistics Table | Data table | Hiển thị các số liệu thống kê SBFAS đã được thống nhất. |

### 5.5.3. Main Flow – Happy Case

School User truy cập trang SBFAS Subsidy Statistics.

System xác định School thuộc phạm vi quản lý của User.

System lấy dữ liệu SBFAS subsidy đã được granted thuộc School đó.

System tổng hợp và hiển thị Total Subsidy Amount Granted.

System hiển thị các số liệu thống kê khác nếu đã được xác nhận.

### 5.5.4. Expected Result

School User xem được thống kê SBFAS của trường mình.

Thống kê không bao gồm dữ liệu SBFAS thuộc trường khác.

Total Subsidy Amount Granted phản ánh các khoản trợ cấp phù hợp với định nghĩa nghiệp vụ đã thống nhất.

## 5.6. R6.2.3 – View Total Subsidy Amount Granted

### 5.6.1. Description

Hệ thống hiển thị tổng số tiền subsidy đã được granted theo từng loại FAS trong phạm vi người dùng được phép xem.

### 5.6.2. Proposed UI Elements

| UI ID | UI Element | Type | Description |
| :--- | :--- | :--- | :--- |
| UI-R6-025 | FAS Type | Display field | Hiển thị loại FAS tương ứng. |
| UI-R6-026 | Total Subsidy Amount Granted | Summary field | Hiển thị tổng số tiền trợ cấp đã được granted. |
| UI-R6-027 | Currency / Amount Format | Display format | Định dạng số tiền theo quy ước được thống nhất. |

### 5.6.3. Main Flow – Happy Case

User truy cập màn hình thống kê trợ cấp thuộc phạm vi được phân quyền.

System lấy dữ liệu subsidy đã được granted tương ứng với loại FAS.

System tổng hợp tổng số tiền subsidy theo định nghĩa nghiệp vụ đã thống nhất.

System hiển thị tổng số tiền theo loại FAS tương ứng.

### 5.6.4. Expected Result

Tổng số tiền subsidy đã được granted được hiển thị theo đúng phạm vi dữ liệu và định nghĩa nghiệp vụ đã thống nhất.

### 5.6.5. Pending Confirmation

Tổng số tiền được tính từ Grant Amount, số tiền thực tế được chi trả hay một trường dữ liệu khác?

Nếu một Grant có nhiều lần thanh toán hoặc nhiều lần cập nhật số tiền, hệ thống lấy giá trị nào?

Có cần phân loại theo thời gian, School hoặc các tiêu chí khác không?

## 5.7. R6.3.1 – Track MOEFAS Budget Usage

### 5.7.1. Description

Cho phép MOE HQ User theo dõi tình hình sử dụng ngân sách MOEFAS dựa trên dữ liệu subsidy đã được granted.

### 5.7.2. Proposed UI Elements

| UI ID | UI Element | Type | Description |
| :--- | :--- | :--- | :--- |
| UI-R6-028 | Budget Amount | Summary field | Hiển thị ngân sách MOEFAS đã cấu hình. |
| UI-R6-029 | Subsidy Amount Used | Summary field | Hiển thị tổng số tiền được tính là đã sử dụng ngân sách. |
| UI-R6-030 | Budget Utilization | Summary field | Hiển thị tỷ lệ sử dụng ngân sách nếu được xác nhận trong phạm vi dashboard. |
| UI-R6-031 | Remaining Budget | Summary field | Hiển thị ngân sách còn lại nếu chức năng được xác nhận. |

### 5.7.3. Main Flow – Happy Case

MOE HQ User truy cập trang theo dõi ngân sách MOEFAS.

System lấy Budget Amount đã cấu hình.

System lấy dữ liệu subsidy được tính là đã sử dụng ngân sách.

System hiển thị Budget Amount và Subsidy Amount Used.

Nếu được xác nhận trong phạm vi chức năng, System tính và hiển thị Budget Utilization và Remaining Budget.

### 5.7.4. Expected Result

MOE HQ User có thể theo dõi tình hình sử dụng ngân sách MOEFAS dựa trên ngân sách đã cấu hình và dữ liệu subsidy phù hợp.

### 5.7.5. Pending Confirmation

Subsidy Amount Used có bằng tổng số tiền của các Grant đã granted không?

Grant bị thu hồi hoặc thay đổi số tiền có làm thay đổi Subsidy Amount Used không?

Budget Utilization (%) có bắt buộc phải hiển thị không?

Remaining Budget có bắt buộc phải hiển thị không?

## 5.8. R6.3.2 – Track SBFAS Budget Usage

### 5.8.1. Description

Cho phép School User theo dõi tình hình sử dụng ngân sách SBFAS thuộc trường mình.

### 5.8.2. Proposed UI Elements

| UI ID | UI Element | Type | Description |
| :--- | :--- | :--- | :--- |
| UI-R6-032 | School | Display field | Hiển thị trường tương ứng. |
| UI-R6-033 | Budget Amount | Summary field | Hiển thị ngân sách SBFAS đã cấu hình. |
| UI-R6-034 | Subsidy Amount Used | Summary field | Hiển thị tổng số tiền được tính là đã sử dụng ngân sách SBFAS của trường. |
| UI-R6-035 | Budget Utilization | Summary field | Hiển thị tỷ lệ sử dụng ngân sách nếu được xác nhận. |
| UI-R6-036 | Remaining Budget | Summary field | Hiển thị ngân sách còn lại nếu được xác nhận. |

### 5.8.3. Main Flow – Happy Case

School User truy cập trang theo dõi ngân sách SBFAS.

System xác định School thuộc phạm vi quản lý của User.

System lấy Budget Amount của SBFAS thuộc School đó.

System tổng hợp Subsidy Amount Used từ dữ liệu phù hợp.

System hiển thị ngân sách và số tiền đã sử dụng.

Nếu được xác nhận, System hiển thị Budget Utilization và Remaining Budget.

### 5.8.4. Expected Result

School User theo dõi được tình hình sử dụng ngân sách SBFAS của trường mình, không bao gồm dữ liệu của trường khác.

## 5.9. R6.3.3 – View Remaining Budget

### 5.9.1. Description

Cho phép người dùng xem ngân sách còn lại nếu chức năng này được xác nhận thuộc phạm vi R6.

### 5.9.2. Proposed Calculation

Nếu nghiệp vụ xác nhận ngân sách còn lại được tính bằng ngân sách đã cấu hình trừ đi số tiền được tính là đã sử dụng, công thức đề xuất là:

Remaining Budget = Budget Amount − Subsidy Amount Used

Công thức trên là đề xuất để xác nhận, chưa phải business rule đã chốt.

### 5.9.3. Main Flow – Happy Case

User truy cập màn hình theo dõi ngân sách.

System lấy Budget Amount đã cấu hình.

System xác định Subsidy Amount Used theo quy tắc nghiệp vụ đã thống nhất.

System tính Remaining Budget theo công thức được xác nhận.

System hiển thị Remaining Budget.

### 5.9.4. Expected Result

Người dùng xem được ngân sách còn lại của chương trình FAS thuộc phạm vi được phân quyền, nếu chức năng được triển khai.

# 6. UI Summary

Bảng dưới đây tổng hợp các thông tin cần xem xét trên UI. Đây là đề xuất thiết kế ở mức functional, chưa phải UI design đã được duyệt.

| Screen / Section | MOE HQ User | School User |
| :--- | :--- | :--- |
| Budget Management | FAS Type, Budget Amount, Save, Cancel và ngân sách đã lưu | School, FAS Type, Budget Amount, Save, Cancel và ngân sách đã lưu |
| Subsidy Statistics | MOEFAS statistics, Total Subsidy Amount Granted | SBFAS statistics của trường, Total Subsidy Amount Granted |
| Budget Tracking | Budget Amount, Subsidy Amount Used; Budget Utilization và Remaining Budget nếu được xác nhận | Budget Amount, Subsidy Amount Used; Budget Utilization và Remaining Budget nếu được xác nhận |

## 6.1. UI Items cần xác nhận

Có cần hiển thị Budget Year / Financial Year không?

Có cần hiển thị thời điểm cập nhật dữ liệu thống kê gần nhất không?

Có cần bảng chi tiết Grant bên dưới các số liệu tổng hợp không?

Có cần biểu đồ thể hiện Budget Amount so với Subsidy Amount Used không?

Có cần bộ lọc theo thời gian hoặc theo School không?

Có cần lịch sử thay đổi Budget Amount không?

Không nên mặc định đưa tất cả các thành phần trên vào MVP khi chưa được xác nhận.

# 7. Acceptance Criteria

## AC-R6.1 – Budget Management

AC-R6.1.1 – Configure MOEFAS Budget

Given MOE HQ User có quyền quản lý ngân sách MOEFAS,

When User nhập Budget Amount và chọn Save,

Then System lưu ngân sách MOEFAS và hiển thị giá trị đã lưu.

AC-R6.1.2 – Configure SBFAS Budget

Given School User có quyền quản lý SBFAS của trường mình,

When User nhập Budget Amount và chọn Save,

Then System lưu ngân sách SBFAS thuộc trường đó và hiển thị giá trị đã lưu.

AC-R6.1.3 – View Configured Budget

Given ngân sách đã được cấu hình,

When User truy cập chức năng xem ngân sách,

Then System hiển thị Budget Amount thuộc phạm vi quản lý của User.

## AC-R6.2 – Subsidy Statistics

AC-R6.2.1 – View MOEFAS Statistics

Given MOE HQ User có quyền xem thống kê MOEFAS,

When User truy cập trang MOEFAS Subsidy Statistics,

Then System hiển thị các số liệu thống kê MOEFAS đã được granted thuộc phạm vi được phép xem.

AC-R6.2.2 – View SBFAS Statistics

Given School User có quyền xem thống kê SBFAS của trường mình,

When User truy cập trang SBFAS Subsidy Statistics,

Then System hiển thị số liệu thống kê của trường tương ứng.

AC-R6.2.3 – View Total Subsidy Amount Granted

Given dữ liệu subsidy đã được granted,

When System tổng hợp thống kê,

Then System hiển thị Total Subsidy Amount Granted theo loại FAS và phạm vi dữ liệu được phép xem, dựa trên định nghĩa nghiệp vụ đã thống nhất.

## AC-R6.3 – Budget Tracking

AC-R6.3.1 – Track MOEFAS Budget Usage

Given Budget Amount MOEFAS đã được cấu hình và có dữ liệu subsidy phù hợp,

When MOE HQ User truy cập trang theo dõi ngân sách,

Then System hiển thị Budget Amount và Subsidy Amount Used.

AC-R6.3.2 – Track SBFAS Budget Usage

Given Budget Amount SBFAS đã được cấu hình và có dữ liệu subsidy phù hợp,

When School User truy cập trang theo dõi ngân sách,

Then System hiển thị Budget Amount và Subsidy Amount Used của trường mình.

AC-R6.3.3 – View Remaining Budget

Given chức năng Remaining Budget đã được xác nhận và có đủ dữ liệu cần thiết,

When User truy cập trang theo dõi ngân sách,

Then System hiển thị Remaining Budget theo công thức nghiệp vụ đã thống nhất.

# 8. Requirement Gaps & Proposed Solutions

| ID | Gap / Open Question | Proposed Clarification |
| :--- | :--- | :--- |
| G1 | Budget Period | Xác nhận ngân sách được thiết lập theo năm học, năm tài chính hay khoảng thời gian khác. |
| G2 | Budget Editing | Xác nhận có được chỉnh sửa ngân sách đã lưu và quy tắc áp dụng ngân sách mới. |
| G3 | Budget Exhaustion | Xác nhận cách xử lý khi ngân sách đã sử dụng hết hoặc vượt ngân sách. |
| G4 | Definition of Subsidy Amount Granted | Xác nhận trường dữ liệu và quy tắc dùng để tính tổng số tiền subsidy đã granted. |
| G5 | Additional Statistics | Xác nhận có cần hiển thị Student Count, Grant Count hoặc thống kê theo thời gian không. |
| G6 | Budget Usage Calculation | Xác nhận cách tính số tiền trợ cấp được xem là đã sử dụng ngân sách. |
| G7 | Grant Changes / Revocation | Xác nhận cách cập nhật số tiền đã sử dụng khi Grant thay đổi hoặc bị thu hồi. |
| G8 | Remaining Budget | Xác nhận Remaining Budget có bắt buộc trong MVP và công thức tính chính thức. |
| G9 | Budget Utilization | Xác nhận có cần hiển thị tỷ lệ sử dụng ngân sách và công thức tính. |
| G10 | Currency and Number Format | Xác nhận currency, decimal precision và cách định dạng số tiền trên UI. |
| G11 | Statistics Refresh | Xác nhận thống kê được cập nhật ngay lập tức hay theo lịch đồng bộ. |
| G12 | Budget History | Xác nhận có cần lưu và hiển thị lịch sử chỉnh sửa ngân sách. |

# 9. Out of Scope / Not Yet Confirmed

Các chức năng sau không được tự động xem là thuộc phạm vi R6 nếu chưa có yêu cầu hoặc xác nhận bổ sung:

Tạo mới, phê duyệt hoặc từ chối Grant.

Thay đổi trạng thái Grant hoặc xử lý quy trình thu hồi Grant.

Thanh toán subsidy hoặc thực hiện giao dịch tài chính.

Xuất báo cáo Excel/PDF.

Dashboard với biểu đồ nâng cao.

Lọc và phân tích theo nhiều chiều dữ liệu.

Cảnh báo khi ngân sách sắp hết hoặc đã hết.

Audit log và lịch sử thay đổi ngân sách.

Phân bổ ngân sách giữa các School.

Thiết lập ngân sách theo nhiều năm học hoặc nhiều kỳ, nếu chưa được xác nhận.

Các chức năng này chỉ được bổ sung khi có cơ sở từ requirement liên quan hoặc quyết định thống nhất với khách hàng.

# 10. Questions for Client Clarification

Ưu tiên làm rõ các câu hỏi sau trước khi hoàn thiện FS và chốt UI:

Budget Period: Ngân sách MOEFAS/SBFAS được thiết lập theo năm học, năm tài chính hay một khoảng thời gian khác?

Budget Editing: Người dùng có được chỉnh sửa ngân sách sau khi đã lưu không? Nếu có, ngân sách mới có áp dụng ngay không?

Total Subsidy Amount Granted: Tổng tiền được tính theo Grant Amount hiện tại, số tiền thực tế đã chi trả hay một giá trị nghiệp vụ khác?

Budget Usage: Những khoản Grant nào được tính là đã sử dụng ngân sách? Grant bị thay đổi hoặc thu hồi sẽ được xử lý thế nào?

Remaining Budget: Có bắt buộc hiển thị ngân sách còn lại không? Nếu có, công thức chính thức là gì?

Budget Utilization: Có cần hiển thị tỷ lệ sử dụng ngân sách (%) không?

Statistics: Ngoài tổng số tiền subsidy đã granted, có cần hiển thị số học sinh thụ hưởng, số lượng Grant và thống kê theo thời gian không?

Data Refresh: Các số liệu thống kê cần cập nhật ngay sau khi Grant thay đổi hay có thể cập nhật theo lịch?

Budget Exhaustion: Khi ngân sách hết, hệ thống chỉ hiển thị trạng thái ngân sách hay phải ngăn cản một thao tác khác? Nếu có, thao tác nào?

Budget History: Có cần theo dõi lịch sử thay đổi ngân sách để phục vụ kiểm tra và đối soát không?

End of Functional Specification – R6, Draft v0.1
Next Step: BA Review → Client Clarification → Confirm Business Rules → Finalize UI Specification → Dev & QA Review.

# R6 — FAS Budget & Statistics

## Overview

Admin Portal · MOEFAS / SBFAS

MOE HQ users có thể thiết lập ngân sách và theo dõi thống kê các khoản trợ cấp MOEFAS đã cấp. School users có thể làm tương tự đối với SBFAS của trường mình.

Set a budget: Người dùng thiết lập ngân sách cho chương trình trợ cấp thuộc phạm vi mình quản lý.

Track statistics: Người dùng theo dõi số liệu về các khoản trợ cấp đã cấp và tình hình ngân sách.

## Requirement analysis

### R6.1 — Budget Management

Thiết lập và quản lý ngân sách

System hỗ trợ quản lý ngân sách cho MOEFAS và SBFAS.

MOE HQ User có thể thiết lập ngân sách MOEFAS trong phạm vi được phân quyền.

School User có thể thiết lập ngân sách SBFAS thuộc School mình.

System lưu và hiển thị Budget Amount đã cấu hình.

Cần xác nhận quy tắc chỉnh sửa ngân sách, thời gian áp dụng và cách xử lý khi ngân sách hết.

### R6.2 — Subsidy Statistics

Theo dõi thống kê trợ cấp đã cấp

MOE HQ User có thể theo dõi thống kê MOEFAS subsidies granted.

School User có thể theo dõi thống kê SBFAS subsidies granted thuộc School mình.

System tổng hợp và hiển thị số liệu trợ cấp theo phạm vi được phân quyền.

System hiển thị tổng số tiền trợ cấp đã cấp theo định nghĩa nghiệp vụ được thống nhất.

Cần xác nhận những chỉ số bổ sung như số học sinh thụ hưởng, số lượt Grant và thống kê theo thời gian.

### R6.3 — Budget Utilization & Remaining Budget

Theo dõi tình hình sử dụng ngân sách

System thể hiện tình hình sử dụng ngân sách dựa trên Budget Amount và số tiền trợ cấp được tính là đã sử dụng.

System hiển thị Remaining Budget nếu nghiệp vụ yêu cầu theo dõi số dư ngân sách.

System tính Budget Utilization (%) nếu được xác nhận trong phạm vi dashboard.

Cần xác nhận cách tính số tiền đã sử dụng và cách cập nhật khi Grant bị thay đổi hoặc thu hồi.

## Business rule

BR6.01 - MOE HQ User quản lý MOEFAS; School User quản lý SBFAS thuộc School mình.

BR6.02 - Thống kê phải phản ánh đúng các khoản trợ cấp thuộc phạm vi người dùng được phép xem.

## Feature List (Happy Case)

### R6.1 – Budget Management

| ID | Feature | Description |
| :--- | :--- | :--- |
| R6.1.1 | Manage MOEFAS Budget | MOE HQ User có thể thiết lập ngân sách cho MOEFAS. |
| R6.1.2 | Manage SBFAS Budget | School User có thể thiết lập ngân sách cho SBFAS thuộc trường mình. |
| R6.1.3 | View Configured Budget | Người dùng có thể xem ngân sách đã thiết lập trong phạm vi quyền hạn của mình. |

### R6.2 – Subsidy Statistics

| ID | Feature | Description |
| :--- | :--- | :--- |
| R6.2.1 | View MOEFAS Subsidy Statistics | MOE HQ User có thể xem thống kê MOEFAS subsidies đã được granted. |
| R6.2.2 | View SBFAS Subsidy Statistics | School User có thể xem thống kê SBFAS subsidies đã được granted tại trường mình. |
| R6.2.3 | View Total Subsidy Amount Granted | Hệ thống hiển thị tổng số tiền subsidy đã được granted theo từng loại FAS trong phạm vi người dùng được phép xem. |

### R6.3 – Budget Tracking

| ID | Feature | Description |
| :--- | :--- | :--- |
| R6.3.1 | Track MOEFAS Budget Usage | MOE HQ User có thể theo dõi tình hình sử dụng ngân sách MOEFAS dựa trên dữ liệu subsidy đã được granted. |
| R6.3.2 | Track SBFAS Budget Usage | School User có thể theo dõi tình hình sử dụng ngân sách SBFAS của trường mình. |
| R6.3.3 | View Remaining Budget | Hệ thống hiển thị ngân sách còn lại nếu chức năng này nằm trong phạm vi yêu cầu đã thống nhất. |

## G
