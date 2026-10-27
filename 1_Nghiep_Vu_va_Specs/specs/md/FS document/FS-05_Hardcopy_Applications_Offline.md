# **R5**

# **FS F5 – Đơn giấy (Paper Applications)**

21/10/2026 · Phiên bản 1.2 · @Huy

Chức năng 5 cho phép School user nhập liệu Mẫu đơn FAS in sẵn (mỗi gia đình một mẫu) mà phụ huynh điền tay: tải lên bản scan có chữ ký, kiểm tra năm phần của mẫu (thông tin người khai và từng con được tự động điền từ hồ sơ), xem lại toàn bộ và nộp. Chỉ nhận đơn khi có form FAS đang mở. Mỗi con tạo một đơn và chuyển sang Chức năng 4: MOEFAS chờ đến khi form MOEFAS đóng rồi mới được xếp hạng và quyết định tự động; SBFAS do trường của con quyết định.

| Mục | Chi tiết |
| ----- | ----- |
| Chức năng | F5 – Đơn giấy (Upload applications) |
| Portal | Admin Portal |
| Người dùng | School user (School Admin) |
| Phiên bản | 1.2 – chỉ nộp được khi có form FAS đang mở; MOEFAS được xét sau khi form đóng (F4 v1.3) |
| Chức năng liên quan | F3 Học sinh & ghi danh (đối chiếu học sinh), F1 Tài khoản giáo dục, F4 Đơn FAS (quyết định), F10 Phụ huynh nộp đơn FAS (cùng dữ liệu) |
| Tham chiếu UI | Figma "Edusave" · trang F5 · Paper applications · Prototype: edusave.vercel.app (School user → Upload applications) |

### **Thay đổi so với v1.1**

| \# | Thay đổi |
| ----- | ----- |
| 1 | Thêm điều kiện chặn mới: chỉ nộp được đơn khi form MOEFAS hoặc form SBFAS của trường của con đang mở ("{con}: the FAS application form is closed (next opens DD/MM/YYYY)."). |
| 2 | Sau khi nộp, đơn MOEFAS ở trạng thái Pending cho đến khi form MOEFAS đóng; sau đó hệ thống xếp hạng theo mức cần hỗ trợ và quyết định tự động (F4 mục 2.2). |
| 3 | Phụ đề của màn Review before submitting: "One application per child. MOEFAS is assessed automatically after the application form closes." |

## **1\. Giới thiệu**

### **1.1 Phạm vi**

| Trong phạm vi | Ngoài phạm vi |
| ----- | ----- |
| Danh sách Upload applications (đã nộp và Draft) | Quyết định MOEFAS/SBFAS (F4) |
| Hộp thoại Upload scans và việc đọc bản scan | Engine OCR thật (prototype mô phỏng việc đọc và tô vàng các trường không chắc chắn) |
| Màn Review application (các phần A–G), tự điền, context | Phụ huynh nộp đơn online (F10) |
| Lưu nháp, huỷ, xem lại trước khi nộp, nộp |  |
| Xem đơn đã nộp; sửa khi còn Pending |  |

### **1.2 Quyền truy cập**

School user chỉ thấy và nhập đơn giấy của học sinh đang học tại trường của mình. MOE HQ không có quyền truy cập màn hình này.

## **2\. Luồng xử lý**

| Bước | Người dùng | Hệ thống |
| ----- | ----- | ----- |
| 1 | Bấm Upload scans, thêm các trang scan (PDF/JPG/PNG), bấm Upload and read. | Đọc mẫu đơn và mở màn Review application với các giá trị tìm được. Trường nào không chắc chắn được tô vàng. |
| 2 | Nhập hoặc xác nhận NRIC của người khai và NRIC của từng con. | Tự điền thông tin người khai (hồ sơ phụ huynh \+ dữ liệu Chính phủ) và thông tin từng con (hồ sơ MOE: trường, cấp, khối, lớp) rồi khoá lại. |
| 3 | Hoàn tất quan hệ, các thành viên gia đình khác (họ tên, NRIC, giới tính), context và các mục xác nhận cam kết. | Tra thu nhập từ dữ liệu Chính phủ cho người khai và từng thành viên gia đình. |
| 4a | Save draft | Lưu nháp; danh sách hiển thị với trạng thái Draft. |
| 4b | Review and submit | Kiểm tra hợp lệ (mục 6). Nếu hợp lệ, mở màn Review before submitting. |
| 5 | Confirm and submit | Tạo một đơn cho mỗi con (nguồn Paper; dùng chung một mã gia đình khi có nhiều con) và phân luồng từng đơn theo quy tắc F4: MOEFAS Pending cho đến khi form MOEFAS đóng (sau đó được xếp hạng và quyết định tự động), hoặc SBFAS Pending gửi trường của con khi con không đủ điều kiện MOEFAS về quốc tịch. Xoá bản nháp. Toast "Application submitted for assessment." / "Applications submitted." |

## **3\. Màn hình: Danh sách Upload applications**

**![Upload applications][image23]**

*Hình: Upload applications có một dòng Draft*

| \# | Thành phần | Hành vi |
| ----- | ----- | ----- |
| 1 | Upload scans | Mở hộp thoại Upload scans (mục 4). |
| 2 | Thẻ thống kê (bấm để lọc) | PENDING (chờ xét) · MOEFAS (duyệt tự động) · SBFAS (do trường quyết định). Số đơn giấy của trường. Bấm thẻ để lọc danh sách; bấm lần nữa để bỏ lọc. |
| 3 | Search | Application ID, người tải lên, số EA hoặc tên học sinh. |
| 4 | Bộ lọc | Status: All, Draft, Pending, Approved · MOEFAS, Approved · SBFAS, Rejected · Tier (các tier SBFAS của trường) · Uploaded: Last 7 days (mặc định), Last 30 days, Any time. |
| 5 | Bảng | File, Uploaded by, Uploaded at, Student (tên, số EA · lớp), Application ID, Status (+ scheme và tier khi đã duyệt), Tier (khi lọc SBFAS hoặc lọc theo tier). |
| 6 | Dòng Draft | Bản nháp được liệt kê trước, Application ID "Not submitted", trạng thái Draft, nút Continue / Delete. Bấm vào dòng cũng tiếp tục bản nháp. |
| 7 | Dòng đã nộp | Bấm để mở View application (mục 8). |
| 8 | Ghi chú cuối trang | "Student is matched by NRIC/FIN against the school's enrolment (Function 3). Applications can be submitted only while a FAS application form is open. A student who already has an application this year is blocked at submit. Drafts appear in the list with status Draft until they are submitted." |

## **4\. Hộp thoại: Upload scans**

**![Upload scans][image24]**

| Quy tắc | Thông báo |
| ----- | ----- |
| Chỉ nhận file PDF, JPG, PNG | "{file}: only PDF, JPG or PNG files." |
| Tối đa 10 MB mỗi file | "{file} is larger than 10 MB." |
| Tối đa 5 file mỗi đơn (một đơn \= một học sinh) | "Up to 5 files per application." |
| Upload and read được bật khi đã thêm ít nhất một file | — |

## **5\. Màn hình: Review application**

**![Review application][image25]**

*Hình: Review application – bản scan bên trái, các Part 1–5 của mẫu đơn bên phải (xám \= tự điền và khoá, vàng \= trình đọc không chắc chắn)*

Nút ở đầu trang: Discard (xoá bản scan hoặc bản nháp), Save draft, Review and submit. Các phần bám theo Mẫu đơn FAS in sẵn.

| Phần | Trường | Quy tắc |
| ----- | ----- | ----- |
| Part 1 · Applicant (Người khai) | NRIC \*, Full name \*, Date of birth \*, Gender \* (Male, Female, Other), Category \* (Singapore Citizen, Singapore PR, International – ASEAN, International – non-ASEAN), Nationality \* (Chinese, Malay, Indian, Eurasian, Others), Relationship to child \* (Father, Mother, Legal guardian, Grandfather, Grandmother, Sibling, Uncle, Aunt, Cousin, Other), Phone number \*, Email \*, Address \*, School-based FAS (Yes/No) | Nhập NRIC của người khai thì họ tên, ngày sinh, giới tính, category, nationality, điện thoại, email và địa chỉ được điền từ hồ sơ phụ huynh và dữ liệu Chính phủ rồi khoá lại. Quan hệ lấy từ mẫu đơn. Điện thoại: chỉ chữ số, tối đa 10\. School-based FAS \= "Also consider for SBFAS" (mặc định Yes). |
| Part 2 · Children applying (Các con nộp đơn) | Mỗi con: NRIC, Full name, Date of birth, Gender, School, Level, Grade, Class; \+ Add child | Ít nhất một con. Nhập NRIC của con thì các cột còn lại được điền từ hồ sơ MOE (học sinh, ghi danh hiện tại, lớp) và khoá lại. Level \= Primary / Secondary / Pre-University suy ra từ khối (P1–P6, S1–S5, PU1–PU3). |
| Part 3 · Other family members (Thành viên gia đình khác) | Mỗi thành viên: Full name, NRIC, Gender; \+ Add member | Tuỳ chọn. Không lặp lại người khai hay các con. Không có ô thu nhập: thu nhập lấy từ dữ liệu Chính phủ cho người khai và từng thành viên. Hiển thị GHI, số người trong hộ (người khai \+ các con \+ các thành viên) và PCI. |
| Part 4 · Circumstances and wishes (Hoàn cảnh và mong muốn) | Context | Tuỳ chọn, tối đa 2000 ký tự, đúng như viết trên mẫu đơn. Người xét đơn thấy ở F4. |
| Part 5 · Declaration (Cam kết) | Declaration ticked \*, Applicant's signature checked \*, Date signed \*, Received by (trường, chỉ đọc), Date received (chỉ đọc) | Received by \= School user; Date received \= hôm nay. |

Nếu tên của con khác với dữ liệu Chính phủ, có ghi chú cho biết MOE sẽ thấy cảnh báo sai lệch dữ liệu; người dùng vẫn nộp được.

## **6\. Kiểm tra hợp lệ (Review and submit)**

**![Bị chặn khi nộp][image26]**

*Hình: Bị chặn khi nộp – thiếu trường bắt buộc và form nộp đơn đã đóng*

| Trường hợp | Thông báo (ghi chú đỏ ở đầu trang) |
| ----- | ----- |
| Thiếu trường bắt buộc | "Complete: {danh sách}." (Applicant NRIC, Applicant full name, Applicant date of birth, Gender, Category, Nationality, Relationship to child, Phone number (up to 10 digits), Email, Address, At least one child, Family members (name and NRIC), Declaration, Applicant signature checked, Date signed) |
| NRIC của con trống hoặc không tìm thấy | "Child {n}: enter the NRIC/FIN." / "Child {n}: no student with NRIC/FIN {nric} in MOE records." |
| Con ngoài độ tuổi 7–16 | "{tên} must be 7 to 16 years old (now {tuổi})." |
| Con đã có đơn trong năm nay | "{tên} already has an application this year ({id}, {status})." |
| Không có con nào đang học tại trường của người dùng | "At least one child must be enrolled at {trường}." |
| Không có form FAS nào đang mở cho con (ngoài khoảng Form opens – Form closes của MOEFAS và của SBFAS của trường) | "{tên}: the FAS application form is closed (next opens DD/MM/YYYY)." (bỏ phần ngày khi chưa có form kế tiếp được publish) |
| Trùng NRIC | "The same NRIC/FIN appears twice. The applicant, each child and each family member must have a different NRIC/FIN." |

## **7\. Hộp thoại: Review before submitting**

**![Review before submitting][image27]**

Hiển thị Part 1 Applicant (tên, NRIC, quan hệ, category · nationality, liên hệ, school-based FAS), Part 2 Children (tên, NRIC, trường, khối, lớp, EA), Part 3 Household (các thành viên khác, số người, GHI từ dữ liệu Chính phủ, PCI) và Part 4 Context. Nút: Back to edit (đóng hộp thoại, không lưu gì) và Confirm and submit (nộp, mục 2 bước 5).

## **8\. Xem và sửa đơn đã nộp**

* Bấm vào một dòng đã nộp để mở View application: cùng mẫu đơn đó, chỉ đọc, có nút Back to list.  
* Chỉ được Edit khi đơn còn Pending. Save changes cập nhật mẫu đơn, hộ gia đình, thu nhập, quan hệ, "also consider SBFAS" và context của đơn đó, và thêm History "Paper application edited". Luồng quyết định không chạy lại.

## **9\. Quy tắc nghiệp vụ**

| ID | Quy tắc |
| ----- | ----- |
| BR1 | Một mẫu đơn in \= một gia đình \= một đơn cho mỗi con (dùng chung mã gia đình khi có nhiều con). |
| BR2 | Mỗi con phải có trong hồ sơ MOE, từ 7–16 tuổi và chưa có đơn trong năm hiện tại; ít nhất một con phải đang học tại trường của người dùng. |
| BR3 | Thông tin người khai và từng con lấy từ hồ sơ khi NRIC khớp, và không sửa được trên mẫu. |
| BR4 | Thu nhập lấy từ dữ liệu Chính phủ (API) cho người khai và từng thành viên gia đình; mẫu không có ô thu nhập. NRIC phải khác nhau trong cùng một mẫu. |
| BR5 | Context là tuỳ chọn, văn bản thuần, tối đa 2000 ký tự, được lưu cùng đơn. |
| BR6 | Bản nháp được lưu theo trường kèm người lưu và thời gian lưu, hiển thị với trạng thái Draft, và bị xoá khi nộp hoặc khi Discard/Delete. |
| BR7 | Nộp luôn phải qua bước Review before submitting. |
| BR8 | Sau khi nộp áp dụng quy tắc F4: MOEFAS Pending cho đến khi form MOEFAS đóng, sau đó xếp hạng theo mức cần hỗ trợ và duyệt nếu đủ điều kiện; nếu không thì SBFAS của trường (khi Also consider SBFAS \= Yes) hoặc Rejected; không đủ điều kiện về quốc tịch → SBFAS ngay lúc nộp. |
| BR9 | Chỉ được nộp khi form MOEFAS hoặc form SBFAS của trường của con đang mở. Vẫn được sửa đơn Pending sau khi form đã đóng. |

## **10\. Kịch bản kiểm thử**

| ID | Kịch bản | Kết quả mong đợi |
| ----- | ----- | ----- |
| T1 | Tải lên file .docx | "…: only PDF, JPG or PNG files." |
| T2 | Nhập NRIC của người khai | Họ tên, ngày sinh, giới tính, category, nationality, điện thoại, email, địa chỉ được điền và khoá. |
| T3 | Nhập NRIC của con | Họ tên, ngày sinh, giới tính, trường, cấp, khối, lớp được điền và khoá. |
| T4 | NRIC của con không có trong hồ sơ MOE | Bị chặn: "Child n: no student with NRIC/FIN …". |
| T5 | Con 17 tuổi | Bị chặn: "… must be 7 to 16 years old". |
| T6 | Không có con nào của trường người dùng | Bị chặn: "At least one child must be enrolled at …". |
| T7 | Thành viên gia đình trùng NRIC với người khai | Bị chặn: "The same NRIC/FIN appears twice…". |
| T8 | Chưa kiểm tra chữ ký | "Complete: Applicant signature checked." |
| T9 | Save draft, rồi Continue | Dòng có trạng thái Draft (tên các con, người khai); mẫu đơn được khôi phục. |
| T10 | Mẫu có 2 con → Confirm and submit | 2 đơn dùng chung một mã gia đình; các con là Singapore Citizen là MOEFAS Pending ("Waiting") cho đến khi form đóng. |
| T11 | Có nhập context | Hiển thị ở Review before submitting và ở drawer F4. |
| T12 | Sửa đơn đang Pending | Save changes cập nhật đơn; History "Paper application edited". |
| T13 | Nộp khi không có form FAS nào đang mở | Bị chặn: "{tên}: the FAS application form is closed (next opens …)." |

