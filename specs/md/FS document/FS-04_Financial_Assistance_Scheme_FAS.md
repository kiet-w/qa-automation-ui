# **R4**

# **FS F4 – Đơn FAS (FAS Applications)**

21/10/2026 · Phiên bản 1.3 · @Huy

Chức năng 4 hiển thị các đơn FAS (MOEFAS và SBFAS) trên Admin Portal và cho phép từng trường quyết định đơn SBFAS của mình. Mỗi scheme FAS có một khoảng thời gian mở form nộp đơn và một khoảng thời gian hiệu lực. Đơn MOEFAS được giữ ở trạng thái chờ cho đến khi form MOEFAS đóng; sau đó hệ thống xếp hạng theo mức độ cần hỗ trợ rồi tự động duyệt hoặc từ chối. MOE HQ chỉ xem đơn và quản lý scheme MOEFAS; mỗi trường tự quản lý scheme SBFAS của mình (mỗi tier là một scheme).

| Mục | Chi tiết |
| ----- | ----- |
| Chức năng | F4 – Đơn FAS và scheme FAS |
| Dự án | Education Account (EA) và website FAS |
| Portal | Admin Portal |
| Người dùng | School Admin, MOE HQ |
| Phiên bản | 1.3 |
| Chức năng liên quan | F5 Đơn giấy, F10 Phụ huynh nộp đơn FAS (cả hai tạo đơn), F6 Ngân sách & thống kê, F3 Fee component và khoản phí, FAS Scoring & Decision Engine |
| Tham chiếu UI | Figma "Edusave" · trang F4 · FAS applications, F4 · FAS schemes · Prototype: edusave.vercel.app |

### **Thay đổi so với v1.2**

| \# | Thay đổi |
| ----- | ----- |
| 1 | Mỗi scheme có khoảng thời gian mở form (Form opens, Form closes) và khoảng thời gian hiệu lực (Effective from, Effective to). Chỉ nộp đơn được khi có form đang mở. Form phải đóng trước khi scheme có hiệu lực. |
| 2 | MOEFAS không còn được quyết định ngay lúc nộp. Đơn ở trạng thái Pending (System check "Waiting") cho đến khi form MOEFAS đóng. Sau đó hệ thống xếp hạng đơn theo mức cần hỗ trợ (thu nhập bình quân đầu người thấp nhất trước) và xét lần lượt. |
| 3 | Scheme không còn tier bên trong. Mỗi trường tạo một scheme SBFAS cho mỗi tier (ví dụ Tier 1, Tier 2, Tier 3), mỗi scheme có điều kiện riêng (quốc tịch, GHI, PCI). Quyết định "Tier" của trường \= scheme SBFAS mà trường cấp. |
| 4 | Wizard tạo scheme còn 3 bước (General → Eligibility → Subsidy). Bước General không còn trường Scheme type và Level. |
| 5 | Subsidy: MOEFAS là một scheme chung cho mọi cấp, mỗi cấp một dòng (Primary, Secondary, Pre-University). SBFAS mỗi khối trường có một dòng (P1–P6, S1–S5 …). Chọn fee component là thêm cột ngay (không còn nút "+ Add"). |
| 6 | Add fee: có thể thêm fee component vào scheme đang Active hoặc Upcoming (không được xoá hay sửa), dùng cho khoản phí phát sinh cuối năm. |
| 7 | Danh sách đơn: cột Grade (khối) thay cho Class; cột Tier (quyết định cuối cùng) đứng trước ML recommendation và ML risk. Danh sách của MOE HQ cũng có cột Grade. |

## **1\. Giới thiệu**

### **1.1 Phạm vi**

| Trong phạm vi | Ngoài phạm vi |
| ----- | ----- |
| Xếp hạng và tự động duyệt MOEFAS sau khi form đóng (mục 2\) | Tạo đơn (F5 đơn giấy, F10 đơn online) |
| Danh sách đơn FAS, bộ lọc, tab, thẻ thống kê, xuất file | Thiết lập ngân sách và thống kê (F6) |
| Drawer xem chi tiết (xem và quyết định SBFAS) | Màn hình phụ huynh (F8, F10) |
| Approve / Reject SBFAS | Huấn luyện mô hình machine learning (engine hiện là rule-based) |
| Scheme FAS: MOEFAS (MOE HQ) và SBFAS (trường), thời gian form và hiệu lực, Add fee |  |

### **1.2 Người dùng và quyền truy cập**

| Vai trò | Đơn FAS | Scheme FAS |
| ----- | ----- | ----- |
| School Admin | Thấy đơn SBFAS của học sinh đang học tại trường. Duyệt (chọn tier) hoặc từ chối. Không bao giờ thấy đơn MOEFAS hay thu nhập trong đơn MOEFAS. | Menu "SBFAS schemes": tạo, lưu nháp và publish scheme SBFAS của trường (mỗi tier một scheme); thêm fee component vào scheme đã publish. |
| MOE HQ | Thấy đơn của mọi trường (MOEFAS và SBFAS). Chỉ xem: không có Approve hay Reject ở bất kỳ đâu. | Menu "MOEFAS schemes": tạo, lưu nháp và publish scheme MOEFAS; thêm fee component vào scheme đã publish. Không thấy scheme SBFAS. |
| Hệ thống | Phân luồng đơn lúc nộp; xếp hạng và quyết định MOEFAS khi form MOEFAS đóng. |  |

### **1.3 Thuật ngữ**

| Thuật ngữ | Ý nghĩa |
| ----- | ----- |
| MOEFAS | FAS toàn quốc. Mỗi năm một scheme cho mọi cấp. Hệ thống tự động quyết định sau khi form đóng. Không có tier. |
| SBFAS | FAS do trường quản lý. Mỗi trường tự tạo scheme; mỗi scheme là một tier (Tier 1, Tier 2 …). Trường quyết định đơn. |
| Thời gian mở form | Form opens – Form closes của scheme. Phụ huynh (F10) và trường (F5) chỉ nộp được trong thời gian form mở. Ví dụ: form 01/08/2026 – 31/12/2026, scheme có hiệu lực từ 01/01/2027. |
| Thời gian hiệu lực | Effective from – Effective to (hoặc không có ngày kết thúc). Trợ cấp áp dụng cho các khoản phí đến hạn trong khoảng này. |
| GHI / PCI | Tổng thu nhập hộ gia đình mỗi tháng / thu nhập bình quân đầu người \= GHI ÷ số người trong hộ. Thu nhập lấy từ dữ liệu Chính phủ (API). |
| Thứ hạng ưu tiên | Thứ tự xét đơn MOEFAS sau khi form đóng: PCI thấp nhất trước, rồi GHI thấp nhất, rồi nộp sớm nhất. |
| Grade / Level | Grade \= khối (P1–P6, S1–S5, PU1–PU3), lấy từ lớp của học sinh. Level \= cấp (Primary, Secondary, Pre-University), lấy từ trường. |
| Tier | Scheme SBFAS mà trường cấp (quyết định cuối cùng). Hiển thị trong danh sách trước ML recommendation. |
| ML recommendation | Tier gợi ý \= scheme SBFAS đầu tiên của trường mà hộ gia đình thoả điều kiện. "—" khi không scheme nào phù hợp và với MOEFAS. |
| ML risk | Low / Medium / High: khả năng khó khăn khi trả phần phí còn lại (tính từ Need Score). |
| Context | Văn bản tự do tuỳ chọn (tối đa 2000 ký tự) về hoàn cảnh hoặc mong muốn của gia đình, nhập ở F10 (phụ huynh) hoặc F5 (trường). |
| Nhóm quốc tịch | SC \= Singapore Citizen, PR \= Singapore PR, IS\_ASEAN / IS\_NON\_ASEAN \= học sinh quốc tế thuộc / không thuộc ASEAN. |

## **2\. Luồng xử lý và trạng thái**

### **2.1 Lúc nộp đơn (hệ thống)**

| Bước | Điều kiện | Kết quả |
| ----- | ----- | ----- |
| 1 | Nộp từ F5 hoặc F10. Chỉ cho nộp khi hôm nay form MOEFAS hoặc form SBFAS của trường học sinh đang mở; nếu không, màn hình chặn ("the FAS application form is closed (next opens DD/MM/YYYY)"). | History "Submitted". |
| 2 | Nhóm quốc tịch của học sinh không nằm trong scheme MOEFAS đang mở (ví dụ PR, International) | Đơn trở thành SBFAS, trạng thái Pending, gửi cho trường của học sinh. History "SBFAS application (not eligible for MOEFAS by nationality)". |
| 3 | Các trường hợp còn lại | Đơn là MOEFAS, gắn với scheme MOEFAS đang mở, trạng thái Pending, System check "Waiting". History "Waiting for the MOEFAS form to close on DD/MM/YYYY". |

### **2.2 Khi form MOEFAS đóng (hệ thống)**

Chạy tự động vào cuối ngày Form closes của scheme MOEFAS (prototype có nút "Close form now (demo)" ở MOEFAS schemes để chạy sớm).

| Bước | Quy tắc |
| ----- | ----- |
| 1 | Lấy tất cả đơn MOEFAS đang Pending của scheme. |
| 2 | Xếp hạng theo mức cần hỗ trợ: thu nhập bình quân đầu người thấp nhất trước, rồi tổng thu nhập hộ thấp nhất, rồi nộp sớm nhất. Lưu hạng "n of N" và History "Form closed · priority n of N (lowest per capita income first)". |
| 3 | Xét lần lượt theo thứ tự đó dựa trên điều kiện của scheme (quốc tịch, GHI, PCI, match rule): Đạt → Approved, người quyết định "System (auto-approved)", Effective from \= Effective from của scheme (hoặc hôm nay nếu muộn hơn), áp trợ cấp theo cấp của học sinh (mục 8), gửi email kết quả cho phụ huynh. Không đạt và "Also consider for SBFAS" \= Yes → thành SBFAS Pending gửi trường của học sinh. Không đạt và "Also consider for SBFAS" \= No → Rejected, lý do "Not eligible for MOEFAS", người quyết định "System". Email lý do cho phụ huynh. |
| 4 | Scheme hiển thị "Assessed DD/MM/YYYY". Không nhận thêm đơn MOEFAS cho scheme này. |

Ngân sách MOEFAS (F6) chỉ để hiển thị; nếu sau này có giới hạn ngân sách thì thứ hạng quyết định thứ tự xét.

### **2.3 SBFAS (trường)**

School Admin của trường học sinh duyệt (chọn tier \= một scheme SBFAS của trường trong kỳ nộp đơn) hoặc từ chối (lý do và ghi chú). Trợ cấp áp dụng từ Effective from của scheme, hoặc từ hôm nay nếu scheme đã có hiệu lực. Quyết định đầu tiên là quyết định cuối.

### **2.4 Trạng thái**

| Trạng thái | Ý nghĩa | Tiếp theo |
| ----- | ----- | ----- |
| Pending | MOEFAS đang chờ form đóng (System check "Waiting"), hoặc SBFAS đang chờ trường | Approved, Rejected (hoặc MOEFAS → SBFAS Pending) |
| Approved | Đã cấp trợ cấp (MOEFAS: không tier · SBFAS: kèm tier) | Không (cuối cùng) |
| Rejected | Không cấp, có lý do | Không (cuối cùng) |

Đơn Draft chỉ tồn tại ở F5 và F10 cho đến khi nộp; không hiển thị ở F4.

## **3\. Màn hình: Danh sách đơn FAS**

Đường dẫn menu: Financial assistance \> FAS applications.

### **3.1 Giao diện MOE HQ**

**![Danh sách MOE HQ][image8]**

*Hình: MOE HQ – FAS applications (tab All). Đơn MOEFAS nộp trong kỳ form mở có System check "Waiting".*

| \# | Thành phần | Hành vi |
| ----- | ----- | ----- |
| 1 | Phụ đề | "All schools. MOEFAS is assessed automatically by the system after its application form closes. SBFAS is decided by each school." |
| 2 | Export | CSV của danh sách đã lọc (mục 3.4). |
| 3 | Thẻ thống kê | Total applications · MOEFAS approved · Approved (MOEFAS và SBFAS) · Rejected (MOEFAS và SBFAS). Không bị ảnh hưởng bởi bộ lọc. |
| 4 | Tab | Pending, All (mặc định), Approved, Rejected, kèm số lượng. |
| 5 | Bộ lọc | Search, School, Scheme, Grade, Tier, Status, ML risk, Submitted (mục 3.3). |
| 6 | Bảng | Application, Student, School, Grade, Scheme, Submitted, System check, Tier, ML recommendation, ML risk, Status, View. |
| 7 | Nút View | Mở drawer (mục 4\) chỉ đọc. MOE HQ không có Review/Approve/Reject. |
| 8 | Ghi chú | "MOEFAS has no tiers. Its applications wait until the application form closes; the system then ranks them by need (lowest per capita income first) and approves or rejects them automatically. SBFAS is decided by each school (view only here)." |

### **3.2 Giao diện School Admin**

**![Danh sách trường][image9]**

*Hình: School Admin – FAS applications (tab Pending): cột Grade, rồi Tier đứng trước ML recommendation và ML risk*

| \# | Thành phần | Hành vi |
| ----- | ----- | ----- |
| 1 | Dòng hiển thị | Chỉ đơn SBFAS của học sinh hiện đang học tại trường của người dùng. |
| 2 | Thẻ thống kê | Pending (SBFAS đang chờ) · SBFAS approved (năm nay) · SBFAS rejected (năm nay). |
| 3 | Tab | Pending (mặc định), All, Approved, Rejected. |
| 4 | Bộ lọc | Search, Grade, Tier, Status, ML risk, Submitted. |
| 5 | Bảng | Application, Student, Grade, Submitted, Tier, ML recommendation, ML risk, Status, Review/View. |
| 6 | Review / View | Review (nút chính) cho đơn SBFAS Pending của trường; View cho đơn đã quyết định. |
| 7 | Ghi chú | "Tier is the SBFAS scheme your school grants. MOEFAS applications and income details are visible to MOE HQ only." |

### **3.3 Bộ lọc**

Các bộ lọc kết hợp bằng AND; đổi bộ lọc thì quay về trang 1\. Search khớp Application ID, tên học sinh hoặc NRIC/FIN (chứa chuỗi, không phân biệt hoa thường).

| Bộ lọc | Giá trị | MOE HQ | Trường |
| ----- | ----- | ----- | ----- |
| School | Tất cả trường | Có | Không |
| Scheme | MOEFAS, SBFAS | Có | Không |
| Grade | Các khối mà trường trong phạm vi có (P1–P6, S1–S4 …) | Có | Có |
| Tier | MOE HQ: MOEFAS, SBFAS – {tên scheme} · Trường: tên các scheme SBFAS của trường. Đơn Pending khớp theo tier ML gợi ý. | Có | Có |
| Status | Pending, Approved, Rejected | Có | Có |
| ML risk | Low, Medium, High | Có | Có |
| Submitted | Last 7 days, Last 30 days, Any time (mặc định) | Có | Có |

### **3.4 Cột và xuất file**

| Cột | Quy tắc |
| ----- | ----- |
| Application | APP-YYYY-NNNNN |
| Student | Tên, bên dưới là NRIC/FIN |
| School | Chỉ MOE HQ |
| Grade | Khối của lớp hiện tại của học sinh (P3, S1 …); "—" khi học sinh chưa có lớp |
| Scheme | Chỉ MOE HQ. MOEFAS hoặc SBFAS |
| Submitted | DD/MM/YYYY |
| System check | Chỉ MOE HQ. MOEFAS: Waiting (Pending) / Pass (Approved) / Fail (Rejected) · SBFAS: "—" |
| Tier | SBFAS: tên scheme SBFAS đã cấp khi Approved, ngược lại để trống · MOEFAS: "—" |
| ML recommendation | Chỉ ghi tier gợi ý ("Tier 3"); "—" với MOEFAS hoặc khi không có tier phù hợp |
| ML risk | Low / Medium / High |
| Status | Pending / Approved / Rejected |

Cột CSV: Application, Student, NRIC, School (chỉ MOE HQ), Grade, Scheme, Submitted, System check, Tier, ML recommendation, ML risk, Status. Sắp xếp: Submitted, mới nhất trước. 10 dòng mỗi trang. Khi không có kết quả: "No applications found."

## **4\. Màn hình: Drawer xem chi tiết**

Mở từ nút Review/View. Chỉ đọc, trừ các nút quyết định. Đóng bằng X hoặc bấm ra ngoài.

![MOEFAS đang chờ][image10] ![MOEFAS đã duyệt][image11] ![SBFAS][image12]

*Hình: MOEFAS đang chờ form đóng · MOEFAS đã duyệt sau khi form đóng (có thứ hạng) · Drawer duyệt SBFAS (School Admin)*

| Mục | MOEFAS | SBFAS | Nội dung |
| ----- | ----- | ----- | ----- |
| Header | Có | Có | "MOEFAS REVIEW" / "SBFAS REVIEW", Application ID, học sinh · trường (MOE HQ) hoặc khối (School Admin). |
| Decision | Khi đã quyết định | Khi đã quyết định | Result; MOEFAS: "Granted · MOEFAS ({tên scheme}) · from DD/MM/YYYY" và "Priority · n of N (lowest per capita income first)" · SBFAS: Tier · from; Reason; Comment; Decided by · ngày giờ. |
| Eligibility check | Có | Không | Khi Pending: ghi chú xanh "Waiting for the {scheme} form to close on DD/MM/YYYY. The system then ranks all applications by need (lowest per capita income first) and assesses them in that order. The check below is indicative." Các dòng: Scheme (tên · hiệu lực từ), Level (cấp · khối), Nationality, GHI, PCI kèm Pass/Fail. Ghi chú: "MOEFAS is decided automatically after the form closes: Pass → approved from Effective from, Fail → the school's SBFAS (if the parent agreed) or rejected." |
| Student / Parent | Không | Có | Tên, NRIC/FIN, Grade, Class, trường (MOE HQ), quốc tịch · tên phụ huynh và quan hệ, NRIC/FIN, số điện thoại, email. |
| Household and income | Có | Có | GHI, số người trong hộ, PCI, nguồn thu nhập. |
| Context | Có | Có | Nội dung từ F5/F10, hoặc "No context given." |
| ML recommendation | Không | Có | Chỉ ghi tier, kèm nhãn "Recommendation only". Ghi chú đỏ khi trường chưa có scheme SBFAS cho kỳ nộp đơn. |
| Documents / History | Có | Có | Danh sách file có link View · lịch sử, cũ nhất trước. |
| Nút | Không | School Admin của trường, chỉ khi Pending | Reject, Approve. |

## **5\. Đánh giá ML**

FAS Scoring & Decision Engine (rule-based) chạy cho mọi đơn. Màn hình chỉ hiển thị tier SBFAS gợi ý và ML risk. Engine không bao giờ tự quyết định.

* Tier ứng viên \= các scheme SBFAS đã publish của trường mà kỳ form chứa ngày nộp (nếu không có thì lấy các scheme đang hiệu lực hôm nay), sắp theo tên.  
* Tier gợi ý \= ứng viên đầu tiên mà hộ thoả điều kiện (quốc tịch, GHI, PCI, match rule); nếu không có thì lấy ứng viên cuối cùng vượt giới hạn không quá 5%; ngược lại "—".  
* ML risk tính từ Need Score (Adjusted Tier): điểm ≥ 75 → High, 50–74,99 → Medium, còn lại Low.  
* Need Score \= 100 × Σ(trọng số × đặc trưng): thu nhập 0,70, phụ thuộc 0,05, ổn định việc làm 0,10, thời gian từ lần hỗ trợ gần nhất 0,10, nhóm dễ tổn thương 0,05. Các quy tắc deny cho điểm 0\.

## **6\. Hộp thoại (School Admin, chỉ SBFAS)**

### **6.1 Approve SBFAS**

**![Approve SBFAS][image13]**

| Thành phần | Quy tắc |
| ----- | ----- |
| Phụ đề | "FUNCTION 4 · SBFAS · {đơn} · {học sinh} · {khối}" |
| Tier \* | Các scheme SBFAS ứng viên (mục 5), theo tên. Mặc định chọn tier ML gợi ý (gợi ý "ML suggests Tier n"), nếu không có thì chọn tier cuối. |
| Comment | Tuỳ chọn, tối đa 500 ký tự, bộ đếm n/500. |
| Confirm approval | Bị khoá khi không có scheme ứng viên hoặc ghi chú quá 500 ký tự. Effective from \= Effective from của scheme, hoặc hôm nay nếu scheme đã có hiệu lực. History "Approved · {tier} · from DD/MM/YYYY". Toast "Subsidy applied to the student's EA fees." |

### **6.2 Reject**

**![Reject][image14]**

Reason \* (Income above limit, Not eligible nationality, Incomplete documents, Other) và Comment \* (tối đa 500, placeholder "Explain the decision. Parent receives the reason by email."). Nút Reject application bị khoá cho đến khi điền cả hai. Toast "Application rejected. Parent notified by email."

## **7\. Scheme FAS**

### **7.1 Danh sách scheme**

**![MOEFAS schemes][image15]**

*Hình: MOE HQ – MOEFAS schemes*

*![SBFAS schemes][image16]*

*Hình: School Admin – SBFAS schemes (mỗi tier một scheme)*

| \# | Thành phần | Hành vi |
| ----- | ----- | ----- |
| 1 | Ai thấy gì | MOE HQ: chỉ scheme MOEFAS. School Admin: chỉ scheme SBFAS của trường mình. |
| 2 | Thẻ thống kê | Active (đang hiệu lực hôm nay) · Upcoming (đã publish, chưa hiệu lực) · Closed (Effective to đã qua) · Draft. |
| 3 | Bảng | Scheme (tên; "Approved automatically" với MOEFAS, "Approved by school" với SBFAS) · Eligibility (quốc tịch · giới hạn GHI/PCI) · Application form (DD/MM/YYYY – DD/MM/YYYY kèm nhãn Open / Not open yet / Closed; MOEFAS còn có "n waiting" hoặc "Assessed DD/MM/YYYY") · Effective from · Effective to ("No end date") · Status · thao tác. |
| 4 | Thao tác | Draft: Edit. Đã publish: View. Active hoặc Upcoming: Add fee (mục 7.4). MOE HQ, scheme MOEFAS có form đang Open: "Close form now (demo)" (chỉ prototype; hệ thống thật tự chạy mục 2.2 khi form đóng). |
| 5 | Sắp xếp | Effective from mới nhất trước, rồi theo tên. |

### **7.2 Wizard tạo scheme mới**

**![General][image17]**

*Hình: Bước 1 General (không có Scheme type, không có Level)*

| Bước | Trường và quy tắc |
| ----- | ----- |
| 1 General | Scheme name \* (MOEFAS ví dụ "MOEFAS 2028"; SBFAS ví dụ "Tier 1"). APPLICATION FORM: Form opens \*, Form closes \*. EFFECTIVE PERIOD: Effective from \*, Effective to (để trống \= không có ngày kết thúc). Loại scheme lấy theo vai trò người dùng (MOE HQ → MOEFAS, trường → SBFAS của trường đó) và không hiển thị. Ghi chú xanh tóm tắt: form mở → đánh giá → trợ cấp áp dụng từ ngày nào. |
| 2 Eligibility | Nationality (Singapore Citizen, Singapore PR, International – ASEAN, International – non-ASEAN); băng GHI (từ–đến, tuỳ chọn); băng PCI (từ–đến, tuỳ chọn); match rule: đạt bất kỳ / đạt tất cả các băng đã chọn. |
| 3 Subsidy | Value type (Percentage of fee / Fixed amount S$).Feecomponent(selecttoadd):chọnmộtcomponentlàthêmngaymộtcộtvớigiátrị0chomọidòng;✕đểbỏ(chỉkhiđangsoạn).Dòng:MOEFAS=cáccấpPrimary,Secondary,Pre-University;SBFAS=cáckhốimàtrườngcó.Mỗiô0–100%(hoặcS$ ≥ 0). |

![MOEFAS subsidy][image18]

*Hình: MOEFAS – Bước 3 Subsidy theo cấp (ví dụ Primary 100 %, Secondary 70 %, Pre-University 50 %)*

*![SBFAS subsidy][image19]*

*Hình: SBFAS – Bước 3 Subsidy theo khối (ví dụ Tier 1: P1 100 %, P2 80 %, P3 60 %, P4 50 %, P5 40 %)*

### **7.3 Kiểm tra, xem lại và publish**

**![Review][image20]**

| Quy tắc | Thông báo |
| ----- | ----- |
| Bắt buộc có tên | "Enter a scheme name." |
| Bắt buộc có ngày form; Form closes ≥ Form opens | "Enter Form opens and Form closes." / "Form closes must be on or after Form opens." |
| Bắt buộc có Effective from và phải sau Form closes | "Effective from must be after Form closes (applications are assessed after the form closes)." |
| Effective to phải sau Effective from | "Effective to must be after Effective from." |
| Ít nhất một quốc tịch và một băng thu nhập | "Select at least one nationality." / "Use at least one income band (GHI or PCI)." |
| Ít nhất một fee component; mọi ô hợp lệ | "Add at least one fee component." / "{dòng} · {fee}: enter 0–100 %." |
| Publish: cùng "slot" không được chồng lấn (MOEFAS: mọi scheme MOEFAS; SBFAS: cùng trường và cùng tên) | "The period overlaps with {scheme} (…). Change Effective from / Effective to." / "The application form period overlaps with {scheme} (…). Change Form opens / Form closes." |
| Publish: scheme trước đó cùng slot đang không có ngày kết thúc | Effective to của nó được đặt \= ngày trước Effective from mới (ghi chú xanh trong màn xem lại). |

Có thể lưu Draft bất kỳ lúc nào (cần có tên). View mở "Review scheme before publishing" gồm General, Eligibility và Subsidy; Publish làm scheme chuyển sang chỉ xem.

### **7.4 Add fee vào scheme đã publish**

**![Add fee][image21]**

| Thành phần | Quy tắc |
| ----- | ----- |
| Khi nào | Scheme đang Active hoặc Upcoming. Không áp dụng cho scheme Closed hoặc Draft. |
| Fee component | Các fee component đang Active chưa có trong scheme. Chọn một component là thêm một cột có thể sửa (0 cho mọi cấp/khối). Cột mới thêm có thể bỏ bằng ✕ trước khi lưu. |
| Component đã có | Hiển thị chỉ đọc; không được xoá hay sửa. |
| Add to scheme | Bị khoá cho đến khi có ít nhất một component mới và mọi ô mới hợp lệ. Lưu component và giá trị, ghi lại "added at / by", và áp trợ cấp cho các khoản phí đang mở của component đó với học sinh đã được cấp scheme này; các khoản phí sau đó tự động áp dụng. Toast "Fee components added to the scheme." |

### **7.5 Close form now (chỉ demo)**

**![Close form][image22]**

Nút chỉ có trên prototype cho MOE HQ, ở scheme MOEFAS có form đang Open. Nút đặt Form closes \= hôm nay rồi chạy mục 2.2. Ở hệ thống thật, quy trình này chạy tự động khi form đóng.

## **8\. Sau khi có quyết định**

| Sự kiện | Hệ thống cập nhật |
| ----- | ----- |
| MOEFAS được duyệt (sau khi form đóng) | Áp trợ cấp theo cấp của học sinh cho các khoản phí chưa trả đến hạn trong kỳ hiệu lực, và cho phí phát hành sau. History "Form closed · priority n of N", "MOEFAS rules met · approved automatically", "Email with result sent to parent". |
| MOEFAS không đạt | SBFAS Pending cho trường (phụ huynh đồng ý) hoặc Rejected kèm email (phụ huynh không đồng ý). |
| SBFAS được duyệt | Lưu tier (scheme), Effective from, Comment, người quyết định; áp trợ cấp theo khối của học sinh cho phí hiện tại và phí sau trong kỳ hiệu lực của scheme; gửi email cho phụ huynh. |
| SBFAS bị từ chối | Lưu Reason, Comment; gửi email lý do cho phụ huynh. |
| Mọi quyết định | Thẻ thống kê và số lượng tab cập nhật; đơn chuyển sang chỉ đọc. |

## **9\. Quy tắc nghiệp vụ**

| ID | Quy tắc |
| ----- | ----- |
| BR1 | Chỉ nộp được đơn khi có form FAS (MOEFAS hoặc SBFAS của trường học sinh) đang mở. |
| BR2 | MOEFAS chỉ do hệ thống quyết định, sau khi form MOEFAS đóng, theo thứ tự ưu tiên (PCI thấp nhất, rồi GHI thấp nhất, rồi nộp sớm nhất). Không người dùng nào được duyệt hay từ chối MOEFAS. |
| BR3 | Form của scheme phải đóng trước khi scheme có hiệu lực (Effective from \> Form closes). |
| BR4 | Scheme không có tier bên trong. MOEFAS: một scheme cho mọi cấp, trợ cấp theo cấp. SBFAS: mỗi tier một scheme, trợ cấp theo khối mà trường có. |
| BR5 | Chỉ School Admin của trường hiện tại của học sinh quyết định SBFAS, bằng cách chọn một scheme SBFAS của trường. MOE HQ chỉ xem. |
| BR6 | Mỗi đơn chỉ có một quyết định; đơn đã quyết định là chỉ đọc. Nếu hai người cùng quyết định một đơn, người sau nhận "This application was already decided by {user} on {date}." |
| BR7 | Giới hạn điều kiện và giá trị trợ cấp luôn lấy từ scheme, không lấy từ màn hình. |
| BR8 | Scheme đã publish chỉ xem, trừ việc được thêm fee component vào scheme Active/Upcoming; component đã có không bao giờ được xoá hay sửa. |
| BR9 | MOE HQ chỉ quản lý scheme MOEFAS và không thấy scheme SBFAS; mỗi trường quản lý scheme SBFAS của mình. |
| BR10 | ML (tier, risk) chỉ mang tính tham khảo. |
| BR11 | Từ chối cần lý do và ghi chú (≤ 500 ký tự). Phụ huynh nhận email sau mỗi quyết định. |
| BR12 | School Admin không bao giờ thấy đơn MOEFAS. |
| BR13 | Tiền tệ S\$; ngày DD/MM/YYYY; giờ HH:mm theo giờ Singapore. |

## **10\. Kịch bản kiểm thử**

| ID | Kịch bản | Kết quả mong đợi |
| ----- | ----- | ----- |
| T1 | Công dân nộp đơn khi form MOEFAS đang mở | MOEFAS Pending, System check "Waiting", History "Waiting for the MOEFAS form to close on …". |
| T2 | Nộp khi không có form nào mở | F5/F10 chặn: "the FAS application form is closed (next opens …)". |
| T3 | Form đóng với 3 đơn đang chờ | Xếp hạng 1–3 theo PCI; mỗi đơn được xét lần lượt; History có "priority n of 3". |
| T4 | Đơn đang chờ nằm trong giới hạn MOEFAS | Approved từ Effective from của scheme; trợ cấp theo cấp của học sinh. |
| T5 | Vượt giới hạn, "Also consider for SBFAS" \= Yes / No | SBFAS Pending tại trường / Rejected kèm email. |
| T6 | Học sinh PR hoặc quốc tế nộp đơn | SBFAS Pending ngay. |
| T7 | Cột trong danh sách của trường | Grade thay cho Class; Tier đứng trước ML recommendation và ML risk. |
| T8 | Approve SBFAS | Danh sách Tier \= các scheme SBFAS của trường; tier ML được chọn sẵn; Effective from \= ngày bắt đầu scheme hoặc hôm nay. |
| T9 | Tạo scheme có Effective from bằng hoặc trước Form closes | Lỗi "Effective from must be after Form closes …". |
| T10 | MOEFAS Bước 3 | Dòng Primary, Secondary, Pre-University; chọn một fee là thêm cột ngay. |
| T11 | SBFAS Bước 3 | Dòng \= các khối mà trường có (P1–P6). |
| T12 | Publish SBFAS "Tier 1" chồng kỳ với một "Tier 1" khác | Báo lỗi chồng kỳ; tên khác (Tier 2\) thì được phép. |
| T13 | Add fee vào scheme Active | Cột mới sửa được, các cột cũ chỉ đọc; sau khi lưu, khoản phí mới được giảm cho học sinh đã được cấp. |
| T14 | Add fee ở scheme Closed | Không hiển thị nút. |
| T15 | Export kèm bộ lọc | CSV chỉ có các dòng đã lọc và các cột ở mục 3.4. |

