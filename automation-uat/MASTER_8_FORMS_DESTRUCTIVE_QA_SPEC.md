# 📋 Master QA Test Specification: 40 Destructive Test Cases Across 8 Core Forms
## Phân Tích & Tấn Công Toàn Bộ 8 Form Nhập Liệu EduFAMS (5 Test Cases / Form)

> **Phương pháp luận:** `/combo-qa` (ISTQB Advanced Test Design Techniques: EP, BVA, Error Guessing & State Mutation)  
> **Mục tiêu:** Tấn công dữ liệu biên dị thường, kiểm soát form validation, chống rác CSDL và phát hiện tối đa lỗ hổng trên cả 8 form nghiệp vụ.  
> **Môi trường mục tiêu:**  
> - Admin Portal: `https://admin.20-255-158-192.sslip.io`  
> - Parent Portal: `https://eservice.20-255-158-192.sslip.io`  

---

## 1. Ma Trận 40 Test Cases Chi Tiết (Chuẩn ISTQB 10 Cột)

| Form # | Mã TC | Phân Hệ & Form | Loại Kiểm Thử | Dữ Liệu Input Tấn Công | Thao Tác Thực Hiện | Kết Quả Kỳ Vọng (Oracle) | Mức Độ Rủi Ro | Mã Lỗi / DOM Indicator | Trạng Thái |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- | :---: | :--- | :---: |
| **F01** | `TC-F01-01` | Form 1: Tạo Cán Bộ (`/school-user-management/new`) | Mandatory Validation | Để trống toàn bộ các trường | Bấm nút `Create` | Form viền đỏ toàn bộ ô bắt buộc; chặn gửi request | High | `aria-invalid="true"` | **READY** |
| **F01** | `TC-F01-02` | Form 1: Tạo Cán Bộ | Email Format Regex | `invalid.email@`, `no-domain`, `@test.com` | Nhập ô `#school-user-email` | Báo lỗi định dạng email không hợp lệ | Medium | `Email is invalid` | **READY** |
| **F01** | `TC-F01-03` | Form 1: Tạo Cán Bộ | NRIC Format Regex | `1234567A`, `S1234567`, `!@#$%^&*` | Nhập ô `#school-user-nric` | Báo lỗi NRIC sai cấu trúc chuẩn Singapore | High | `NRIC is invalid` | **READY** |
| **F01** | `TC-F01-04` | Form 1: Tạo Cán Bộ | XSS Injection | `<script>alert('XSS')</script>` | Nhập ô `#school-user-name` | Escape plain text; không thực thi popup | High | Sanitized string | **READY** |
| **F01** | `TC-F01-05` | Form 1: Tạo Cán Bộ | Leading/Trailing Whitespace | `   Arthur Kent   ` | Nhập NRIC & Tên có khoảng trắng | Hệ thống tự động `trim()` khoảng trắng thừa | Low | Auto-trimmed | **READY** |
| **F02** | `TC-F02-01` | Form 2: View As (`/support-console`) | BVA Boundary (<10 chars) | Reason = `9 chars!!` (9 ký tự) | Nhập Reason, nhập Ticket | Nút `Start View As` bị **DISABLED** | Medium | `disabled="true"` | **READY** |
| **F02** | `TC-F02-02` | Form 2: View As | BVA Boundary (=10 chars) | Reason = `10 chars!!` (10 ký tự) | Nhập đủ 10 ký tự Reason | Nút `Start View As` chuyển sang **ENABLED** | Medium | `disabled="false"` | **READY** |
| **F02** | `TC-F02-03` | Form 2: View As | Missing Ticket Ref | Reason = `10 chars!!`, Ticket = `""` | Xóa rỗng ô Ticket reference | Nút `Start View As` lập tức bị khóa lại | Medium | Form incomplete | **READY** |
| **F02** | `TC-F02-04` | Form 2: View As | SQLi in Ticket | Ticket = `' OR '1'='1' --` | Nhập Ticket chứa mã SQL | Thoát chuỗi an toàn; không gây lỗi 500 server | High | Handled safe | **READY** |
| **F02** | `TC-F02-05` | Form 2: View As | Persona Unselected | Reason & Ticket điền đủ nhưng chưa chọn User | Bấm Start View As | Bị chặn, yêu cầu phải chọn Persona/User trước | High | Blocked | **READY** |
| **F03** | `TC-F03-01` | Form 3: Tạo Lớp (`/class-management/new`) | Mandatory Check | Để trống Code, Name, Offering | Bấm `Create class` | Báo lỗi cả 3 trường: *"Class code is required..."* | High | `aria-invalid="true"` | **READY** |
| **F03** | `TC-F03-02` | Form 3: Tạo Lớp | Duplicate Code Collision | Code = `P1-A` (đã có trong năm 2026) | Nhập mã lớp trùng lặp | Báo lỗi: *"Class code 'P1-A' already exists..."* | High | Unique conflict | **READY** |
| **F03** | `TC-F03-03` | Form 3: Tạo Lớp | Special Chars in Code | Code = `P1/A#@$!` | Nhập ký tự lạ vào Class code | Chặn hoặc sanitize ký tự không hợp lệ | Medium | Format validation | **READY** |
| **F03** | `TC-F03-04` | Form 3: Tạo Lớp | Long Class Name (255+) | Name = `"Primary 1-A "*30` | Nhập tên lớp dài hơn 255 ký tự | Giới hạn độ dài hoặc báo lỗi không cho submit | Low | Length limit | **READY** |
| **F03** | `TC-F03-05` | Form 3: Tạo Lớp | HTML Tag Injection | Name = `<img src=x onerror=alert(1)>` | Nhập mã HTML vào tên lớp | Render plain text; không kích hoạt onerror alert | High | XSS sanitized | **READY** |
| **F04** | `TC-F04-01` | Form 4: Biểu Phí (`/rate-rules/new`) | Negative Rate Amount | Amount = `-100.00 SGD` | Nhập số âm vào `#fixed-amount` | Viền đỏ; báo lỗi số tiền phải lớn hơn 0 | Critical | `Invalid amount` | **READY** |
| **F04** | `TC-F04-02` | Form 4: Biểu Phí | Zero Rate Amount | Amount = `0.00 SGD` | Nhập số 0 vào `#fixed-amount` | Báo lỗi hoặc yêu cầu xác nhận nếu miễn phí | High | Zero check | **READY** |
| **F04** | `TC-F04-03` | Form 4: Biểu Phí | Decimal Tampering | Amount = `100.12345` hoặc `NaN` | Nhập quá 2 chữ số thập phân | Tự động làm tròn hoặc từ chối chữ cái NaN | High | Decimal(10,2) | **READY** |
| **F04** | `TC-F04-04` | Form 4: Biểu Phí | Date Inversion | From = `2026-12-31`, To = `2026-01-01` | Nhập ngày bắt đầu > ngày kết thúc | Chặn submit; giữ nguyên form tại bước 2 | High | Range error | **READY** |
| **F04** | `TC-F04-05` | Form 4: Biểu Phí | Century Overflow (20266) | From = `20266-05-15` | Nhập năm 5 chữ số | HTML5 validation kích hoạt `rangeOverflow=True` | High | `max="2099-12-31"` | **READY** |
| **F05** | `TC-F05-01` | Form 5: Đợt Thu (`/fee-batches/new`) | Missing Component ID | Mở URL `/fee-batches/new` trực tiếp | Không truyền param `feeComponentId` | Hiện cảnh báo bắt buộc mở từ Fee Component; khóa form | High | Prerequisite warn | **READY** |
| **F05** | `TC-F05-02` | Form 5: Đợt Thu | Inverted Period Dates | Period Start > Period End | Nhập kỳ thu đảo ngược | Chặn submit: *"Period end must be after start"* | High | Period validation | **READY** |
| **F05** | `TC-F05-03` | Form 5: Đợt Thu | Inverted Due Date | Due Date < Charge Date | Hạn nộp tiền trước ngày phát hành nợ | Báo lỗi hạn nộp phải sau ngày phát hành nợ | High | Due date check | **READY** |
| **F05** | `TC-F05-04` | Form 5: Đợt Thu | Empty Title | Title = `""` | Xóa rỗng tiêu đề đợt thu | Viền đỏ trường Title; chặn tạo đợt thu rỗng | Medium | Required check | **READY** |
| **F05** | `TC-F05-05` | Form 5: Đợt Thu | Special Chars in Title | Title = `Batch <script> & %$#` | Nhập tiêu đề chứa ký tự đặc biệt | Escape an toàn chuỗi tiêu đề trong DB | Low | Sanitized | **READY** |
| **F06** | `TC-F06-01` | Form 6: Đề Án SBFAS (`/sbfas-schemes/new`) | Negative Budget Sanitization | Budget = `-50000 SGD` | Nhập hoặc dán `-50000` | Lọc bỏ dấu trừ `-` thành `50000` | High | Sanitized minus | **READY** |
| **F06** | `TC-F06-02` | Form 6: Đề Án SBFAS | Zero Budget Progression | Budget = `0 SGD` | Nhập 0 rồi bấm Next | **PHẢI CHẶN LẠI** tại Bước 1, không cho chuyển bước | Critical | **DEFECT FOUND** | 💥 **DEFECT** |
| **F06** | `TC-F06-03` | Form 6: Đề Án SBFAS | Budget Cap Overflow ($999M) | Budget = `999999999 SGD` | Nhập số cực lớn vượt trần | **PHẢI CHẶN LẠI** tại Bước 1, cảnh báo trần $50,000 | Critical | **DEFECT FOUND** | 💥 **DEFECT** |
| **F06** | `TC-F06-04` | Form 6: Đề Án SBFAS | Empty Income Band | Xóa rỗng GHI To và PCI To | Bấm Next ở Bước 2 | Báo lỗi: *"Enter the upper value of income band"* | High | Required threshold | **READY** |
| **F06** | `TC-F06-05` | Form 6: Đề Án SBFAS | Abnormal Subsidy Rate | Rate = `150%` hoặc `-50%` | Nhập vào ma trận Bước 3 | Chặn tỷ lệ ngoài khoảng $[0, 100]\%$; khóa nút Review | High | `VR-FEE-04` | **READY** |
| **F07** | `TC-F07-01` | Form 7: Duyệt FAS (`/fas-applications`) | Reject Remarks BVA (14 chars) | Remarks = `14 chars text!` | Mở modal Reject, nhập 14 ký tự | Nút `Reject application` bị **DISABLED** | Medium | `disabled="true"` | **READY** |
| **F07** | `TC-F07-02` | Form 7: Duyệt FAS | Reject Remarks BVA (15 chars) | Remarks = `15 characters!!` | Nhập đủ 15 ký tự vào Remarks | Nút `Reject application` chuyển sang **ENABLED** | Medium | `disabled="false"` | **READY** |
| **F07** | `TC-F07-03` | Form 7: Duyệt FAS | Missing Reject Reason | Bỏ trống Dropdown Reason | Nhập remarks $\ge 15$ ký tự | Nút Reject vẫn bị khóa nếu chưa chọn lý do | High | Reason mandatory | **READY** |
| **F07** | `TC-F07-04` | Form 7: Duyệt FAS | MOE HQ Read-Only Lock | Đăng nhập tài khoản `admin@IAM.edu.vn` | Mở đơn trợ cấp trường | Tuyệt đối **0 nút Approve / 0 nút Reject** | Critical | RBAC boundary | **READY** |
| **F07** | `TC-F07-05` | Form 7: Duyệt FAS | Approve Remarks Optional | Chọn Tier 1, không nhập remarks | Bấm nút xác nhận duyệt | Duyệt thành công (Remarks là tùy chọn khi Approve) | Low | Optional check | **READY** |
| **F08** | `TC-F08-01` | Form 8: Thanh Toán (`/accounts/STU-001/pay`) | Zero Selection Validation | Bỏ tick toàn bộ checkbox nợ | Nhìn nút Pay / Authorize | Nút thanh toán bị khóa hoặc tổng tiền = $0.00 | High | No selection lock | **READY** |
| **F08** | `TC-F08-02` | Form 8: Thanh Toán | Masked NRIC Privacy | NRIC hiển thị trên màn hình | Kiểm tra text NRIC học sinh | NRIC bắt buộc hiển thị dạng che: `*****854C` | Critical | PDPA Privacy | **READY** |
| **F08** | `TC-F08-03` | Form 8: Thanh Toán | Financial Subtraction Check | Gross $100 - Trợ cấp $100 | Kiểm tra cột Amount due | Amount due phải bằng đúng `$0.00 SGD` | Critical | Math accuracy | **READY** |
| **F08** | `TC-F08-04` | Form 8: Thanh Toán | Edusave Balance Update | Nợ $40.00, Ví có $500.00 | Bấm `Authorize & Pay` | Ví EA trừ chính xác còn lại `$460.00 SGD` | Critical | Wallet Ledger | **READY** |
| **F08** | `TC-F08-05` | Form 8: Thanh Toán | Unauthenticated Payment Access | Mở trực tiếp link `/pay` ẩn danh | Chưa đăng nhập Singpass | Chuyển hướng ngay về màn hình Singpass login | Critical | Auth guard | **READY** |
