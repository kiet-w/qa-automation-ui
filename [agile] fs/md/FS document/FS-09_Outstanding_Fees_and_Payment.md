# FS-09: Outstanding Fees and Payment (Requirement 9)


# FS Function 9 - Outstanding Fees and Payment (Final)

Oct 14, 2026


## 1. Introduction


### 1.1. Preface

Tài liệu này là Functional Specification (FS) cho Function 9 (R9) – Outstanding Fees & Payment trên e-Service Portal của hệ thống Education Account & FAS (MOE Singapore). Function 9 cho phép Parent/Guardian xem các khoản phí chưa thanh toán của con và thanh toán bằng số dư Education Account (EA), bằng phương thức thanh toán trực tuyến, hoặc chia đôi một invoice giữa hai nguồn này.


### 1.2. Personas



| Persona | Loại | Vai trò trong Function 9 |
| --- | --- | --- |
| Parent / Guardian | Primary actor, đăng nhập qua Singpass | Xem invoice chưa thanh toán của con đã liên kết, chọn cách thanh toán (EA, online hoặc chia đôi), xác nhận, xem kết quả và biên lai |
| School User, MOE HQ User | Indirect actor, Admin Portal | Thiết lập fee type, fee component, gán phí cho student và phát hành invoice (R3). |
| Student | Đối tượng dữ liệu | Là chủ invoice và chủ EA. Không đăng nhập |
| e-Service System | Hệ thống | Xác minh quyền, hiển thị khoản phí, kiểm tra EA, điều phối thanh toán, ghi nhận kết quả |
| Education Account service (Function 1) | Hệ thống nội bộ | Giữ sổ cái EA; ghi nợ và hoàn (reversal) EA, mỗi thao tác và idempotent theo FundingReference |
| Online Payment Provider | Bên thứ ba | Xử lý thanh toán trực tuyến, gửi kết quả qua webhook. Sprint 1 dùng sandbox |
| Singpass | Bên thứ ba | Xác thực Parent. Sprint 1 dùng mock/sandbox |



### 1.3. Design Assumptions and Limitations

Design assumptions:



| ID | Assumption |
| --- | --- |
| DA-01 | Thanh toán online Sprint 1 đi qua sandbox gateway giả lập (success, failure, cancel). Hệ thống không lưu dữ liệu thẻ |
| DA-02 | Số dư EA và sổ cái nằm ở Function 1; Function 9 chỉ lưu ID tham chiếu giao dịch sổ cái. EA chỉ bị trừ khi nhánh EA của giao dịch thành công, và được hoàn (reversal) nếu giao dịch không hoàn tất |
| DA-03 | Chỉ student là Singapore Citizen mới có EA. Permanent Resident và foreign student trả phí bằng phương thức online |
| DA-04 | Liên kết Parent–Student được tạo khi nạp dữ liệu student. Sau khi đăng nhập Singpass, hệ thống kiểm tra liên kết và chỉ hiển thị các con đã liên kết. Guardian nào có liên kết đều xem và trả được |
| DA-05 | Đơn vị thanh toán là invoice của một student tại một trường, gồm một hay nhiều dòng (invoice item, mỗi dòng ứng với một student charge của Function 3). Parent thanh toán cả invoice, không trả từng dòng. Trạng thái hiển thị: Issued (chưa thanh toán), Pending, Paid, Cancelled. Danh sách theo từng con, hiển thị fee type, fee component (kể cả GST, lấy từ Function 3) và tổng tiền |
| DA-06 | Quyền dùng EA chỉ phụ thuộc EA status Active |
| DA-07 | Parent có thể trả invoice bằng EA, bằng online, hoặc chia đôi giữa EA và online (split payment). Tổng các phần bằng đúng số phải trả. Không hỗ trợ trả một phần invoice (partial payment): invoice chỉ Paid khi một giao dịch thanh toán đủ số tiền thành công |
| DA-08 | Parent chủ động chọn cách thanh toán và số tiền từng phần cho mỗi invoice; hệ thống tự động đề xuất EA nếu đủ số dư |
| DA-09 | Sprint 1 hiển thị số gốc. Invoice và từng dòng lưu snapshot subsidy (mặc định 0), Net = Gross trừ Subsidy, để FAS cắm vào sau mà không đổi cấu trúc |
| DA-10 | Tiền tệ SGD (CurrencyCode mặc định SGD); GST là fee component dùng lại được |
| DA-11 | Dữ liệu invoice và số dư EA cho demo là seed/mock, gắn nhãn rõ là dữ liệu mẫu, và phải thỏa các ràng buộc ở BR-F9-12; không trình bày như billing thật |
| DA-12 | Mỗi lần thanh toán tạo một transaction gồm một hay hai funding leg (nhánh nguồn tiền: EA hoặc online) và check idempotency key để tránh phát sinh 2 giao dịch trùng lặp |
| DA-13 | Mỗi invoice có tối đa một transaction đang mở và tối đa một transaction thành công (DB đảm bảo bằng index duy nhất có điều kiện) |
| DA-14 | Giao dịch chia đôi không nằm trong một database transaction duy nhất vì sổ cái EA thuộc Function 1. Hệ thống trừ EA trước, tạo thanh toán online phần còn lại, và hoàn EA khi online không thành công |


Limitations:

Nguồn invoice chính thức, quy tắc thanh toán EA, nhà cung cấp thanh toán online và phương thức được hỗ trợ chưa được client xác nhận (OQ-04, OQ-08, OQ-11).

Nguồn authoritative của số dư và giao dịch EA chưa chốt (OQ-05). Function 1 cần có API ghi nợ và hoàn EA idempotent theo FundingReference.

Mức tối thiểu của từng phần khi chia đôi, thời hạn session và phiên online (đề xuất 10 phút) và ngưỡng chuyển sang ReconciliationRequired chưa được chốt (TBC).

Thanh toán online khi chưa có gateway hay sandbox không được tính là Done.

Function 9 chỉ được coi là đạt khi chức năng xem invoice và cả ba cách thanh toán (EA, online, chia đôi) chạy đúng tiêu chí chấp nhận.


### 1.4. Definitions, Acronyms and Abbreviations



| Thuật ngữ | Giải thích |
| --- | --- |
| EA | Education Account. Tài khoản chi tiêu do chính phủ tài trợ cho Singapore Citizen, dùng cho chi phí giáo dục. Không phải tài khoản đăng nhập. Số dư và sổ cái nằm ở Function 1 |
| Invoice | Nghĩa vụ thanh toán bất biến của một student tại một trường, gồm một hay nhiều dòng. Parent là người trả được ủy quyền, không phải chủ invoice. Trạng thái: Draft, Issued, PaymentPending, Paid, Cancelled |
| Invoice item | Một dòng của invoice, ứng với đúng một student charge của Function 3; lưu snapshot Gross, Subsidy, Net |
| Charge (student charge) | Khoản phí gán cho một student ở Function 3. Mỗi charge xuất hiện ở tối đa một invoice |
| Fee type / Fee component | Loại phí (school fee, miscellaneous fee, extracurricular, ad hoc) / thành phần cấu thành, có thể xuất hiện trong nhiều fee type. Một fee type có thể có nhiều fee component |
| Level / Cohort | Cùng một khái niệm. Class là riêng |
| Transaction (Payment) | Một lần thanh toán toàn bộ một invoice, gồm một hay hai funding leg. Sơ đồ chuyển trạng thái ở Appendix A |
| Funding leg | Nhánh nguồn tiền của một transaction: Education Account hoặc Online. Mỗi nhánh có FundingReference riêng |
| Split payment | Trả một invoice bằng hai nguồn (EA và online), tổng hai phần bằng đúng số phải trả |
| Reversal | Bút toán hoàn của Function 1 để trả lại số tiền đã ghi nợ EA khi giao dịch không hoàn tất → Refuned |
| Idempotency key | Khóa đảm bảo một yêu cầu thanh toán chỉ được xử lý một lần dù bị gửi lại; duy nhất theo Parent |
| Webhook | Callback mà payment provider gọi về hệ thống để báo kết quả thanh toán |
| Online payment method | Phương thức thanh toán trực tuyến cho nhánh online, chuyển sang third party (app ngân hàng). Parent chọn phương thức và nhập thông tin trên trang của provider. |
| HMAC | Hash-based Message Authentication Code: chữ ký tính từ nội dung thông điệp và một khóa bí mật mà chỉ hệ thống và provider biết. |
| Reconciliation | Đối soát kết quả giữa hệ thống, Function 1 và provider. ReconciliationRequired là trạng thái khi kết quả chưa rõ hoặc hoàn EA lỗi, cần bộ phận vận hành xử lý |
| Ledger | Sổ ghi giao dịch EA, chỉ thêm mới, thuộc Function 1 |
| FAS | Financial Assistance Scheme (MOEFAS, SBFAS) |
| CPF | Central Provident Fund |
| SGD | Singapore dollar |
| PR | Permanent Resident |



### 1.5. Exclusions

FS này không đặc tả:

Thiết lập fee type, fee component, gán phí cho student và phát hành invoice trên Admin Portal (R3). Function 9 chỉ hiển thị kết quả đã có.

Logic áp trợ cấp FAS vào số phải trả (R4).

Top-up EA (R2), tạo và đóng EA (R1), chuyển số dư sang CPF.

Sổ cái EA và việc triển khai API ghi nợ, hoàn EA (Function 1). FS chỉ mô tả cách Function 9 gọi các API này.

Đăng nhập Singpass và phân quyền Parent–Student ngoài phần Function 9 sử dụng (R8).

Cập nhật thông tin cá nhân Parent, AI assistant.

Xác thực Admin Portal.


### 1.6. OOS List



| # | Hạng mục ngoài phạm vi | Lý do / nguồn | Dự kiến |
| --- | --- | --- | --- |
| 1 | Gộp nhiều invoice trong một lần thanh toán | Mỗi transaction ứng một invoice (index duy nhất theo InvoiceId) | Chưa xếp lịch |
| 2 | Trả một phần invoice (partial payment) | DB không có PaidAmount hay PartiallyPaid; khác với chia đôi EA + online, vốn trong phạm vi | Chưa xếp lịch |
| 3 | Hoàn tiền (refund) số tiền đã thu qua online | DB chỉ có reversal cho nhánh EA; chưa định nghĩa ai chịu trách nhiệm và hoàn về đâu | Sprint sau |
| 4 | Áp trợ cấp FAS | FAS thuộc Sprint 3, hiện chưa hỗ trợ | Sprint 3 |
| 5 | Sinh invoice tự động và fee batch | PB-13, Sprint 2 | Sprint 2 |
| 6 | Thông báo email/SMS khi thanh toán | Chưa có trong requirement | Chưa xếp lịch |
| 7 | Thanh toán qua provider thật, phương thức cụ thể (thẻ, PayNow) | Chưa chọn provider (OQ-11) | Sau khi chọn provider |
| 8 | Thanh toán EA khi EA đã đóng, invoice còn nợ sau khi đóng EA | EA closure thuộc Sprint 3; chỉ trả online | Sprint 3 |
| 9 | Biên lai gửi qua email | Chưa có trong requirement | Chưa xếp lịch |



## 2. System Process and Function Overview


## 2.1. Process Flow Diagrams

Thất bại cho phép thử lại (quay về bước chọn phương thức) hoặc thoát. Không đủ điều kiện dùng EA thì Parent chọn lại phương thức khác.

Khi Parent chọn trả chia đôi (một phần từ EA, phần còn lại online), luồng đi theo sơ đồ dưới đây: trừ EA trước, chỉ mở thanh toán online khi phần EA đã trừ thành công, và hoàn lại phần EA nếu phần online thất bại, bị hủy hoặc hết hạn. Tổng hai phần phải bằng đúng số tiền của invoice


## 3. Detailed Functions and Solution Design


### 3.1.1. Function Description

Function 9 cho Parent xem invoice chưa thanh toán của con và thanh toán bằng số dư EA, thanh toán trực tuyến, hoặc chia đôi giữa hai nguồn. Thanh toán thành công cập nhật invoice sang Paid và trả mã tham chiếu; thanh toán thất bại không làm invoice Paid, và phần EA đã trừ (nếu có) được hoàn lại.



| Mục | Nội dung |
| --- | --- |
| Function ID | F9 (R9) |
| Portal | e-Service Portal |
| Actor chính | Parent/Guardian đăng nhập qua Singpass |
| Precondition | Parent đã đăng nhập thành công; có ít nhất một Student đã liên kết; invoice đã được phát hành (Issued) cho Student (seed trong Sprint 1) |
| Postcondition (thành công) | Transaction = Succeeded và mọi funding leg = Succeeded; invoice = Paid; mỗi nhánh EA có bút toán ghi nợ ở Function 1, số dư giảm đúng một lần; Parent thấy xác nhận kèm mã tham chiếu |
| Postcondition (thất bại hay hủy) | Transaction = Failed hoặc Cancelled; invoice về Issued; nhánh EA đã trừ (nếu có) = Reversed, số dư EA trở về như trước |
| Postcondition (đang chờ) | Transaction = Pending; invoice = PaymentPending; không cho tạo thêm transaction cho cùng invoice |
| Postcondition (cần xử lý tay) | Transaction hoặc nhánh = ReconciliationRequired khi không xác định được kết quả hoặc hoàn EA lỗi; invoice giữ PaymentPending; bộ phận vận hành xử lý |


Sub-function:



| ID | Sub-function | Mục đích |
| --- | --- | --- |
| F9.1 | Xác minh quyền và liệt kê con đã liên kết | Chỉ hiển thị con của Parent đang đăng nhập |
| F9.2 | Xem invoice chưa thanh toán và số dư EA | Danh sách invoice theo con, các dòng, trạng thái rỗng |
| F9.3 | Chọn invoice và cách thanh toán | EA, online hoặc chia đôi; kiểm tra điều kiện EA và số tiền từng phần |
| F9.4 | Thanh toán bằng EA (nhánh EA) | Ghi nợ EA nguyên tử ở Function 1 |
| F9.5 | Thanh toán online (nhánh online) | Tạo payment session với provider |
| F9.6 | Nhận và đối soát kết quả thanh toán | Webhook ghi nhận trước, xử lý sau; truy vấn định kỳ; Pending và ReconciliationRequired |
| F9.7 | Xác nhận, biên lai, lỗi, hoàn EA và thử lại | Mã tham chiếu khi thành công; hoàn phần EA khi giao dịch không hoàn tất; thử lại hay thoát khi lỗi |


Business rules:



| ID | Rule |
| --- | --- |
| BR-F9-01 | Parent chỉ xem và thanh toán invoice của con đã liên kết; kiểm tra ở server cho mọi API |
| BR-F9-02 | Chỉ dùng EA: chỉ bật khi student có EA ở trạng thái Active và số dư khả dụng ≥ toàn bộ số phải trả của invoice. Chia đôi: cần EA Active và số dư khả dụng > 0; phần EA balance phải bằng số dư khả dụng, phần online là số còn lại (xem BR-F9-11). Nếu số dư nhỏ hơn số phải trả, lựa chọn chỉ dùng EA bị tắt và hệ thống đề xuất chia đôi |
| BR-F9-03 | Việc trừ tiền EA do Function 1 làm trọn gói: kiểm tra số dư, trừ số dư và ghi sổ cái cùng thành công hoặc cùng không xảy ra. Gửi lại cùng một FundingReference thì chỉ trừ một lần. Function 9 chỉ lưu kết quả vào nhánh EA, kèm mã bút toán của Function 1. Nếu lỗi hoặc không rõ kết quả: hỏi lại Function 1 bằng cùng FundingReference; nếu tiền đã bị trừ thì hoàn lại (reversal); nếu vẫn không xác định được thì chuyển ReconciliationRequired cho bộ phận vận hành. Hệ thống không tự đoán là đã trừ hay chưa |
| BR-F9-04 | Một invoice chỉ bị thu một lần: idempotency key duy nhất theo Parent, nút submit bị vô hiệu sau khi bấm, mỗi invoice tối đa một transaction thành công |
| BR-F9-05 | Giao dịch thất bại, hủy hoặc lỗi thì invoice không thành Paid; phần EA đã trừ phải được hoàn (reversal); phần online chưa thành công không bị thu |
| BR-F9-06 | Webhook chỉ được xử lý khi chữ ký HMAC hợp lệ (provider ký nội dung bằng khóa bí mật chung, hệ thống tính lại và so sánh; xem định nghĩa HMAC ở 1.4); ghi nhận ngay (Received) rồi xử lý bất đồng bộ; idempotent theo ProviderCode + ProviderEventId; không lưu payload thô, chỉ lưu hash |
| BR-F9-07 | Student không có EA chỉ thanh toán online |
| BR-F9-08 | Sprint 1 hiển thị số gốc; dòng subsidy mặc định 0 |
| BR-F9-09 | Mỗi invoice chỉ có một giao dịch đang mở. Khi có transaction chưa hoàn tất, không cho khởi tạo thêm (DB đảm bảo bằng index duy nhất có điều kiện) |
| BR-F9-10 | Parent chủ động chọn cách thanh toán và số tiền từng phần; hệ thống không tự động trừ EA |
| BR-F9-11 | Chia đôi: tổng số tiền các nhánh bằng đúng số phải trả của invoice; mỗi nhánh lớn hơn 0; thứ tự EA trước, online sau; nếu online không thành công thì hoàn nhánh EA |
| BR-F9-12 | Ràng buộc invoice (theo DB): mọi dòng cùng một trường; mỗi student charge chỉ ở một invoice; Net = Gross trừ Subsidy và Net > 0 với invoice đã phát hành; số tiền không âm. Dữ liệu seed phải thỏa các ràng buộc này |
| BR-F9-13 | Không trả một phần invoice: số tiền yêu cầu của transaction bằng đúng NetAmount của invoice; transaction thành công thì số tiền quyết toán bằng số yêu cầu |



### 3.1.2. Process Flow Description and Screens

Bước 1. Đăng nhập và liệt kê con đã liên kết (F9.1)

Parent đăng nhập qua Singpass (mock/sandbox ở Sprint 1).

Hệ thống xác minh quyền truy cập và truy vấn danh sách Student đã liên kết với Parent.

Hệ thống hiển thị màn hình chọn con (SCR-01).

Luồng thay thế: đăng nhập thất bại hoặc bị hủy thì không tạo session và hiển thị lỗi; Parent không có liên kết nào thì hiển thị trạng thái rỗng kèm hướng dẫn liên hệ trường; Parent chỉ có một con thì có thể chuyển thẳng sang SCR-02.

Bước 2. Chọn con và xem khoản phí chưa thanh toán (F9.2)

Parent chọn một con trên SCR-01.

Hệ thống kiểm tra liên kết Parent–Student cho con được chọn, rồi hiển thị SCR-02: các khoản thu chưa thanh toán và số dư EA của con nếu có EA.

Danh sách invoice của con; mỗi invoice mở ra các dòng (nhóm theo fee type) với fee component (kể cả GST), subsidy, số phải trả, hạn nộp và trạng thái; đơn vị SGD.

Luồng thay thế: student không có EA thì không hiển thị số dư, hiển thị ghi chú không có Education Account.

Bước 3. Trường hợp không có invoice chưa thanh toán

Nếu không có invoice Issued, hệ thống hiển thị trạng thái không có phí chưa thanh toán (SCR-03) và kết thúc luồng. Parent có thể quay lại SCR-01 để chọn con khác hoặc thoát.

Bước 4. Chọn invoice và cách thanh toán (F9.3)

Parent chọn một invoice trên SCR-02.

Hệ thống mở SCR-04 với ba lựa chọn: Số dư EA, Thanh toán trực tuyến

Parent chọn cách thanh toán. Hệ thống kiểm tra số dư EA trước. Nếu số dư EA nhỏ hơn số phải trả của invoice, lựa chọn chỉ dùng EA bị tắt và hệ thống đề xuất chia đôi: phần EA mặc định là toàn bộ số dư khả dụng (Parent không được nhập số), phần online là số còn lại do hệ thống tự tính dựa trên só EA đã được nhập, Parent không nhập tay. Nếu số dư EA lớn hơn hoặc bằng số phải trả, Parent chỉ được chọn EA hoặc online payment.

Bước 5. Kiểm tra điều kiện khi chọn EA (F9.3)

Khi Parent chọn EA hoặc chia đôi, hệ thống kiểm tra EA của con: tồn tại, trạng thái Active, số dư khả dụng ≥ phần EA.

Với chia đôi, kiểm tra thêm: hai phần đều lớn hơn 0, tổng bằng số phải trả, phần online không nhỏ hơn mức tối thiểu của provider.

Đủ điều kiện: chuyển sang bước 6. Không đủ điều kiện hoặc không đủ số dư cho toàn bộ số phải trả: hiển thị lý do và gợi ý (trả online, hoặc chia đôi nếu EA còn dùng được).

Bước 6. Xem lại và xác nhận thanh toán (F9.4, F9.5)

Hệ thống hiển thị SCR-05 để Parent xem lại: con, invoice, tổng phải trả, cách thanh toán và số tiền từng phần (EA, online), số dư EA sau thanh toán (nếu dùng EA).

Parent xác nhận. Nút xác nhận bị vô hiệu ngay sau lần bấm đầu; client gửi kèm idempotency key.

Hệ thống tạo transaction (Pending) cùng các funding leg, mỗi nhánh có FundingReference riêng; invoice chuyển sang PaymentPending; rồi xử lý theo cách thanh toán:

EA: gọi Function 1 ghi nợ toàn bộ số phải trả (nguyên tử, idempotent theo FundingReference).

Thành công: nhánh Succeeded, transaction Succeeded, invoice Paid.

Không đủ số dư hoặc lỗi: nhánh Failed, transaction Failed, invoice về Issued, EA không đổi.

Online: tạo payment session với provider (sandbox), nhánh Pending, chuyển Parent đến trang thanh toán của provider, nơi Parent chọn phương thức thanh toán trực tuyến.

EA + online (chia đôi): ghi nợ phần EA trước. Chỉ khi nhánh EA thành công mới tạo payment session cho phần online. Nếu nhánh EA thất bại thì dừng, không thu tiền online, transaction Failed.

Bước 7. Nhận kết quả và hiển thị (F9.6, F9.7)

Nhánh EA có kết quả ngay (Succeeded hoặc Failed). Nhánh online nhận kết quả qua webhook, đồng thời hệ thống truy vấn provider định kỳ cho các nhánh còn Pending.

Pending: hiển thị trạng thái đang chờ (SCR-06) cho đến khi được cập nhật. SCR-06, tương tự với split payment.

Mọi nhánh Succeeded: transaction Succeeded, invoice Paid, hiển thị xác nhận kèm mã tham chiếu và từng phần thanh toán (SCR-07).

Chia đôi mà nhánh online Failed, Cancelled hoặc hết hạn: hệ thống gọi Function 1 hoàn phần EA (reversal). Nhánh EA = Reversed, transaction Failed, invoice về Issued; hiển thị lỗi và cho phép thử lại hoặc thoát (SCR-08).

Online đơn lẻ Failed hoặc Cancelled: invoice về Issued, không thu tiền; hiển thị SCR-08.

Không xác định được kết quả quá ngưỡng, hoặc hoàn EA lỗi: transaction và nhánh liên quan = ReconciliationRequired, invoice giữ PaymentPending, cảnh báo vận hành; Parent thấy trạng thái đang xác minh (SCR-06).

Thử lại: quay về SCR-04. Bấm đúp cùng một yêu cầu dùng cùng idempotency key (không thu hai lần); thử lại sau khi thất bại là một transaction mới với key mới (DB duy nhất theo Parent và key); chỉ cho thử lại khi giao dịch cũ đã đóng và phần EA (nếu có) đã được hoàn.

Trường hợp ngoại lệ:



| # | Tình huống | Xử lý |
| --- | --- | --- |
| EX-01 | Parent sửa ID student trên URL hoặc trong API để xem hay thanh toán invoice của học sinh không phải con mình (ví dụ đổi /students/101 thành /students/102) | Server kiểm tra liên kết Parent–Student cho mọi request, không chỉ ở màn hình. Không có liên kết thì trả 403, không lộ dữ liệu, ghi log bảo mật |
| EX-02 | Session hết hạn khi đang thanh toán | Session portal hết hạn sau 10 phút không hoạt động (TBC, theo chính sách Singpass/MOE). Hết hạn trước khi Parent xác nhận: yêu cầu đăng nhập lại, chưa có transaction nào được tạo. Hết hạn sau khi đã xác nhận: transaction vẫn được xử lý theo kết quả provider; Parent đăng nhập lại sẽ thấy trạng thái hiện tại. Phiên thanh toán tại provider hết hạn sau 10 phút nếu Parent không hoàn tất (TBC); khi đó nhánh online Failed và phần EA (nếu có) được hoàn |
| EX-03 | Hai request đồng thời cho cùng invoice | DB chỉ cho một transaction đang mở: một request thành công, request kia bị từ chối (409 PAYMENT_PENDING) |
| EX-04 | Invoice đã Paid, đang PaymentPending hoặc Cancelled khi Parent bấm xác nhận | Từ chối, hiển thị trạng thái hiện tại |
| EX-05 | Số dư đổi giữa lúc xem và lúc xác nhận | Function 1 kiểm tra lại khi ghi nợ; không đủ thì nhánh EA Failed với EA_INSUFFICIENT_BALANCE. Với chia đôi, chưa tạo phiên online nên không thu tiền online |
| EX-06 | Webhook sai chữ ký | Từ chối, ghi log bảo mật, không lưu vào webhook receipt (chỉ lưu callback đã xác thực), không đổi trạng thái |
| EX-07 | Webhook gửi lại nhiều lần | Xử lý idempotent theo ProviderCode + ProviderEventId, chỉ áp dụng một lần |
| EX-08 | Provider timeout hay lỗi mạng | Giữ Pending, không tự đánh dấu Failed; job đối soát hỏi lại provider; quá ngưỡng (NQ-10) thì chuyển ReconciliationRequired |
| EX-09 | Parent đóng trình duyệt khi đang ở trang provider | Transaction vẫn Pending cho đến khi có kết quả từ webhook hay đối soát; Parent thấy trạng thái khi vào lại |
| EX-10 | Lỗi giữa chừng khi ghi nợ EA | Function 1 rollback phần ghi nợ của nó; Function 9 ghi nhánh Failed, không đánh dấu Paid. Nếu không chắc đã trừ hay chưa: ReconciliationRequired |
| EX-11 | Hệ thống lỗi sau khi nhánh EA thành công, trước khi tạo phiên online | Job quét: transaction Pending có nhánh EA Succeeded nhưng không có nhánh online sau X phút (Dev chốt X) thì hoàn EA |
| EX-12 | Provider báo thành công muộn sau khi EA đã hoàn | Hủy hoặc cho phiên provider hết hạn trước khi hoàn EA; nếu vẫn nhận thành công muộn thì nhánh online = ReconciliationRequired để vận hành xử lý (chưa có hoàn online, xem OOS #3) |
| EX-13 | Hoàn EA thất bại | Nhánh và transaction = ReconciliationRequired, cảnh báo vận hành, không tự thử vô hạn |
| EX-14 | Invoice bị Cancelled trong lúc Parent đang xem | Từ chối khi xác nhận (INVOICE_NOT_PAYABLE); invoice đã phát hành là bất biến, chỉ có thể bị hủy |



## 4. Data Fields Table


### 4.1. Trường hiển thị và nhập trên màn hình



| Màn hình | Trường | Kiểu | Nguồn | Nhập | Bắt buộc | Quy tắc / ghi chú |
| --- | --- | --- | --- | --- | --- | --- |
| SCR-01 | Student name | Text | Student | Không | Có | Chỉ con đã liên kết |
| SCR-01 | School, Level, Class | Text | School, Level, Class | Không | Có | Level còn gọi là Cohort |
| SCR-01 | Has outstanding invoices | Boolean | Tính từ invoice Issued | Không | Có | Hiển thị nhãn có hay không có nợ |
| SCR-02 | EA balance | Decimal(18,2), SGD | Function 1 | Không | Không | Chỉ hiển thị khi student có EA |
| SCR-02 | EA status | Enum Active, Closed | Function 1 | Không | Không | Chỉ Active mới được dùng để trả |
| SCR-02 | Invoice number | Text | Invoice | Không | Có | Mã nghiệp vụ duy nhất |
| SCR-02 | Fee type | Text | Function 3, qua StudentChargeId | Không | Có | School fee, miscellaneous, extracurricular, ad hoc |
| SCR-02 | Line description | Text | Function 3, qua StudentChargeId | Không | Có | Ví dụ phí hoạt động, phí hư hại tài sản |
| SCR-02 | Fee components (name, amount) | List | Function 3 (TBC, câu hỏi D4) | Không | Có | Bao gồm GST; tổng các dòng bằng Gross của dòng invoice |
| SCR-02 | Gross amount | Decimal(18,2) | Invoice, invoice item | Không | Có | Trước trợ cấp; là snapshot |
| SCR-02 | Subsidy amount | Decimal(18,2) | Invoice, invoice item | Không | Có | Mặc định 0 ở Sprint 1 |
| SCR-02 | Net amount (số phải trả) | Decimal(18,2) | Invoice | Không | Có | Bằng Gross trừ Subsidy, lớn hơn 0 |
| SCR-02 | Invoice status | Enum Issued, PaymentPending, Paid, Cancelled | Invoice | Không | Có | Không có Partially Paid; Draft không hiển thị cho Parent |
| SCR-02 | Due date | Date | Invoice | Không | Có | Bắt buộc sau khi phát hành, là hạn sớm nhất của các dòng. Quá hạn tính từ Due date; cách hiển thị TBC (OQ-04) |
| SCR-02 | Selected invoice | Invoice ID | Parent chọn | Có | Có | Chỉ Issued; không có giao dịch đang mở |
| SCR-04 | Payment method | Enum EA, ONLINE, SPLIT | Parent chọn | Có | Có | EA và SPLIT chỉ khi EA đủ điều kiện |
| SCR-04 | EA amount | Decimal(18,2) | Mặc định toàn bộ số dư khả dụng | Có | Có khi SPLIT | Lớn hơn 0, không vượt số dư khả dụng, bằng số phải trả |
| SCR-04 | Online amount | Decimal(18,2) | Tính: Net trừ EA amount | Không | Có khi SPLIT | Lớn hơn 0; không nhỏ hơn mức tối thiểu của provider (TBC) |
| SCR-04 | Ineligibility reason | Enum | Hệ thống | Không | Không | EA_NOT_AVAILABLE, EA_NOT_ACTIVE, EA_INSUFFICIENT_BALANCE, SPLIT_AMOUNT_INVALID |
| SCR-05 | Amount to pay | Decimal(18,2) | Invoice | Không | Có | Bằng Net amount (không trả một phần); với SPLIT hiển thị thêm từng phần |
| SCR-05 | EA balance after payment | Decimal(18,2) | Tính | Không | Không | Chỉ để tham khảo, với EA hoặc SPLIT |
| SCR-05 | Idempotency key | Text, tối đa 100 ký tự | Client sinh | Không | Có | Duy nhất theo Parent; mỗi lần thử mới dùng key mới; bấm đúp giữ cùng key |
| SCR-06, 07, 08 | Transaction status | Enum Pending, Succeeded, Failed, Cancelled, ReconciliationRequired | Transaction | Không | Có | ReconciliationRequired hiển thị là đang xác minh |
| SCR-06, 07, 08 | Leg status (từng phần) | Enum Pending, Succeeded, Failed, Reversed, ReconciliationRequired, Cancelled | Funding leg | Không | Có | Reversed chỉ đúng với nhánh EA |
| SCR-07 | Transaction reference | Text, tối đa 50 ký tự | Hệ thống sinh | Không | Có | Duy nhất; định dạng đề xuất PAY-YYYYMMDD-XXXXXX (TBC). Mã từng nhánh (FundingReference) dùng đối soát |
| SCR-07 | Paid at | Datetime | Transaction (CompletedAt) | Không | Có | Hiển thị SGT |
| SCR-07 | Settled amount mỗi phần | Decimal(18,2) | Funding leg | Không | Có | Tổng bằng Net amount |
| SCR-08 | Failure reason | Text | Hệ thống, FailureCode đã làm sạch | Không | Có | Thông điệp thân thiện, không lộ chi tiết kỹ thuật; nêu phần EA đã được hoàn nếu có |



### 4.2. Thực thể dữ liệu liên quan



| Thực thể | Trường | Kiểu | Ràng buộc |
| --- | --- | --- | --- |
| Invoice (invoices) | Id | VARCHAR(50) | PK |
|  | StudentId, SchoolId | UNIQUEIDENTIFIER | FK logic tới Function 3; mọi dòng thuộc SchoolId |
|  | InvoiceNumber | VARCHAR(50) | Unique |
|  | CurrencyCode | CHAR(3) | Mặc định SGD |
|  | GrossAmount, SubsidyAmount, NetAmount | DECIMAL(18,2) | Không âm; Net = Gross trừ Subsidy; Net > 0 khi không phải Draft |
|  | Status | INT | 1 Draft, 2 Issued, 3 PaymentPending, 4 Paid, 5 Cancelled |
|  | IssuedAt, DueDate, PaidAt, CancelledAt | DATETIME2(3), DATE | IssuedAt và DueDate bắt buộc sau khi phát hành; PaidAt chỉ khi Paid; CancelledAt chỉ khi Cancelled |
|  | CreatedAt, UpdatedAt, RowVersion | DATETIME2(3), ROWVERSION | UTC; RowVersion là token kiểm soát đồng thời lạc quan |
| InvoiceItem (invoice_items) | Id, InvoiceId | VARCHAR(50) | PK, FK Invoice (không cascade delete) |
|  | LineNumber | SMALLINT | Dương, duy nhất trong invoice |
|  | StudentChargeId | UNIQUEIDENTIFIER | Unique; tham chiếu logic tới student_charges của Function 3 |
|  | GrossAmount, SubsidyAmount, NetAmount | DECIMAL(18,2) | Gross > 0; 0 ≤ Subsidy < Gross; Net = Gross trừ Subsidy và Net > 0. FeeComponentId, ComponentType, IsFasSubsidizable không sao chép (thuộc Function 3 và FAS) |
| Transaction (transactions) | Id, InvoiceId | VARCHAR(50) | PK, FK Invoice |
|  | InitiatedByUserId | VARCHAR(50) | IAM ID của Parent khởi tạo |
|  | TransactionReference | NVARCHAR(50) | Unique |
|  | IdempotencyKey | VARCHAR(100) | Unique theo (InitiatedByUserId, IdempotencyKey) |
|  | RequestedAmount, SettledAmount, CurrencyCode | DECIMAL(18,2), CHAR(3) | Requested > 0 và bằng NetAmount; 0 ≤ Settled ≤ Requested; Succeeded thì Settled = Requested |
|  | Status | INT | 1 Pending, 2 Succeeded, 3 Failed, 4 Cancelled, 5 ReconciliationRequired |
|  | CreatedAt, UpdatedAt, CompletedAt, RowVersion | DATETIME2(3), ROWVERSION | CompletedAt rỗng khi đang xử lý. Index duy nhất trên InvoiceId khi CompletedAt rỗng (một checkout mở) và khi Status = Succeeded (một giao dịch thành công) |
| FundingLeg (transaction_funding_sources) | Id, TransactionId | VARCHAR(50) | PK, FK Transaction |
|  | SequenceNumber | SMALLINT | Dương, duy nhất trong transaction |
|  | FundingReference | NVARCHAR(50) | Unique; gửi sang Function 1 hoặc provider để đối soát |
|  | Method | INT | 1 EducationAccount, 2 OnlineGateway |
|  | RequestedAmount, SettledAmount | DECIMAL(18,2) | Requested > 0; Tổng Requested các nhánh bằng Requested của transaction cha |
|  | Status | INT | 1 Pending, 2 Succeeded, 3 Failed, 4 Reversed, 5 ReconciliationRequired, 6 Cancelled |
|  | WalletId | UNIQUEIDENTIFIER | Logic FK tới EA (Function 1). Bắt buộc nếu Method = 1, cấm nếu Method = 2 |
|  | EducationAccountTransactionId, EducationAccountReversalTransactionId | BIGINT | ID logic sổ cái Function 1; bắt buộc sau khi ghi nợ thành công; Reversal ID bắt buộc khi Reversed; mỗi ID duy nhất |
|  | ProviderCode, ProviderTransactionId | VARCHAR(40), VARCHAR(128) | ProviderCode bắt buộc nếu Method = 2; ProviderTransactionId bắt buộc khi thành công; duy nhất theo cặp |
|  | FailureCode, FailureReason | VARCHAR(50), NVARCHAR(500) | Mã lỗi kỹ thuật và nguyên nhân đã làm sạch |
|  | CreatedAt, UpdatedAt, CompletedAt, RowVersion | DATETIME2(3), ROWVERSION | UTC |
| WebhookReceipt (payment_webhook_receipts) | Id, FundingTransactionId | VARCHAR(50) | PK, FK FundingLeg (sau khi khớp nối) |
|  | ProviderCode, ProviderEventId | VARCHAR(40), VARCHAR(128) | Unique theo cặp, chống sự kiện trùng |
|  | ProviderTransactionId, FundingReference, EventType | VARCHAR(128), NVARCHAR(50), VARCHAR(50) | Do provider gửi trong callback |
|  | PayloadHash | VARBINARY(32) | SHA-256, không lưu payload thô hay dữ liệu thẻ |
|  | ProcessingStatus | INT | 1 Received, 2 Processed, 3 Ignored, 4 Failed |
|  | ReceivedAt, ProcessedAt, ErrorMessage | DATETIME2(3), NVARCHAR(500) | Chỉ lưu callback đã qua HMAC; ProcessedAt rỗng khi chờ xử lý; lỗi đã làm sạch |
| Tham chiếu ngoài | Function 1: EA, sổ cái, API ghi nợ và reversal |  | Function 9 chỉ lưu ID logic (WalletId, EducationAccountTransactionId) |
|  | Function 3: student_charges, fee component |  | Function 9 chỉ lưu StudentChargeId |
| AuditLog | actor, action, entity, entity_id, old_value, new_value, timestamp |  | Ghi mọi thay đổi trạng thái thanh toán. Chủ sở hữu (dịch vụ chung hay bảng riêng) chờ Dev xác nhận (D5) |



## 5. Validation


### 5.1. Thông báo lỗi hiển thị cho Parent



| Mã | Nội dung hiển thị | Hành vi UI |
| --- | --- | --- |
| EA_NOT_AVAILABLE | This student does not have an Education Account. Please pay online. | Vô hiệu tùy chọn EA, gợi ý Online |
| EA_NOT_ACTIVE | The Education Account is not active. Please pay online. | Như trên |
| EA_INSUFFICIENT_BALANCE | Your Education Account balance is not enough for this amount. You can pay the rest online. | Quay lại chọn phương thức, gợi ý chia đôi |
| SPLIT_AMOUNT_INVALID | The two amounts must be more than zero and add up to the total. | Giữ ở SCR-04, đánh dấu ô nhập |
| INVOICE_ALREADY_PAID | This invoice has already been paid. | Làm mới danh sách |
| INVOICE_NOT_PAYABLE | This invoice can no longer be paid. | Làm mới danh sách |
| PAYMENT_PENDING | A payment for this invoice is still being processed. | Chuyển đến SCR-06 |
| PAYMENT_FAILED | Your payment could not be completed. No amount was deducted. | SCR-08, nút Try again, Exit |
| PAYMENT_FAILED_EA_RETURNED | Your online payment could not be completed. The amount taken from the Education Account has been returned. | SCR-08, nút Try again, Exit |
| PAYMENT_CANCELLED | The payment was cancelled. No amount was deducted. | SCR-08; với chia đôi mà EA đã trừ thì dùng PAYMENT_FAILED_EA_RETURNED |
| FORBIDDEN_CHILD | You do not have access to this student's records. | Quay về SCR-01 |
| AUTH_REQUIRED | Your session has expired. Please sign in again. | Chuyển đến đăng nhập Singpass |
| SYSTEM_ERROR | Something went wrong. Please try again later. | Cho thử lại; không đổi dữ liệu |



### 5.3. Tiêu chí chấp nhận (AC)



| ID | Given / When / Then |
| --- | --- |
| AC-01 | Given Parent đã đăng nhập và có con đã liên kết, when chọn con, then thấy đúng invoice chưa trả của con đó kèm số tiền, hạn nộp và trạng thái; không thấy invoice của con khác |
| AC-02 | Given con không có invoice Issued, when mở SCR-02, then hiển thị trạng thái không có phí chưa thanh toán |
| AC-03 | Given EA Active và số dư đủ, when Parent xác nhận thanh toán EA, then số dư EA giảm đúng một lần bằng số phải trả, nhánh EA Succeeded, invoice Paid, có mã giao dịch sổ cái và mã tham chiếu |
| AC-04 | Given số dư EA không đủ cho toàn bộ số phải trả, when Parent chọn EA, then thấy lý do và gợi ý trả online hoặc chia đôi; không có dữ liệu nào đổi |
| AC-05 | Given Parent bấm xác nhận hai lần liên tiếp, then chỉ tạo một transaction và chỉ trừ một lần |
| AC-06 | Given hai request đồng thời cho cùng invoice, then chỉ một transaction được mở và một request thành công; số dư không âm; không có trường hợp trừ tiền mà invoice không được cập nhật hoặc không được hoàn |
| AC-07 | Given Function 1 lỗi giữa chừng khi ghi nợ, then nhánh EA Failed (hoặc ReconciliationRequired nếu không chắc), invoice không Paid, không trừ EA hai lần |
| AC-08 | Given Parent chọn thanh toán online và hoàn tất trên sandbox thành công, then nhánh online Succeeded sau webhook hợp lệ và invoice Paid |
| AC-09 | Given thanh toán online thất bại hoặc bị hủy, then invoice về Issued và không bị thu |
| AC-10 | Given webhook sai chữ ký, then bị từ chối và ghi log bảo mật; given webhook gửi lại, then chỉ áp dụng một lần; given webhook hợp lệ, then được ghi nhận ngay và xử lý sau |
| AC-11 | Given transaction Pending, when Parent vào lại, then thấy trạng thái đang chờ và không tạo được transaction thêm |
| AC-12 | Given Parent đổi ID con khác trong request, then bị từ chối và ghi log |
| AC-13 | Given thanh toán thành công, then Parent xem và tải/in được biên lai PDF kèm mã tham chiếu và từng phần thanh toán |
| AC-14 | Given Student không có EA, then chỉ có thanh toán online, không hiển thị lỗi |
| AC-15 | Given EA Active số dư 20.00 và invoice 50.00 SGD, when Parent chọn chia đôi EA 20.00 + online 30.00 và cả hai thành công, then EA giảm 20.00, nhánh online 30.00 Succeeded, invoice Paid, biên lai hiện hai phần |
| AC-16 | Given chia đôi, when số dư EA đã giảm dưới phần EA trước lúc xác nhận, then nhánh EA Failed, không tạo phiên online, không thu tiền online, invoice về Issued |
| AC-17 | Given chia đôi và nhánh EA thành công, when online thất bại, bị hủy hoặc hết hạn, then phần EA được hoàn (nhánh Reversed), số dư EA trở về như trước, transaction Failed, invoice về Issued |
| AC-18 | Given chia đôi và hoàn EA lỗi, then transaction ReconciliationRequired, invoice giữ PaymentPending, Parent thấy trạng thái đang xác minh, vận hành được cảnh báo |
| AC-19 | Given tổng hai phần khác số phải trả hoặc một phần bằng 0, then bị từ chối với SPLIT_AMOUNT_INVALID và không có dữ liệu nào đổi |
| AC-20 | Given provider báo thành công muộn sau khi nhánh EA đã hoàn, then nhánh online ReconciliationRequired và invoice không tự chuyển Paid |
| AC-21 | Given invoice bị Cancelled giữa lúc xem và lúc xác nhận, then bị từ chối với INVOICE_NOT_PAYABLE |
| AC-22 | Given EA Active số dư 20.00 và invoice 50.00 SGD, when Parent chọn chia đôi, then hệ thống vô hiệu lựa chọn chỉ dùng EA, đề xuất phần EA mặc định 20.00 và tự tính phần online 30.00; Parent có thể đổi phần EA thành số nhỏ hơn và phần online tự cập nhật |



## 6. Appendices


### Appendix A. Trạng thái Transaction, nhánh và Invoice



| Đối tượng | Từ | Sang | Điều kiện | Invoice |
| --- | --- | --- | --- | --- |
| Transaction | (mới) | Pending | Parent xác nhận; tạo các nhánh | PaymentPending |
| Transaction | Pending | Succeeded | Mọi nhánh Succeeded | Paid |
| Transaction | Pending | Failed | Một nhánh Failed, hoặc online Failed, Cancelled, hết hạn và nhánh EA (nếu có) đã Reversed | Issued |
| Transaction | Pending | Cancelled | Parent hủy trên trang provider và nhánh EA (nếu có) đã Reversed | Issued |
| Transaction | Pending | ReconciliationRequired | Không xác định được kết quả quá ngưỡng, hoặc hoàn EA lỗi | PaymentPending |
| Transaction | ReconciliationRequired | Succeeded, Failed hoặc Cancelled | Bộ phận vận hành xử lý | Paid hoặc Issued |
| Nhánh EA | Pending | Succeeded | Function 1 ghi nợ thành công | - |
| Nhánh EA | Pending | Failed | Không đủ số dư hoặc lỗi khi ghi nợ | - |
| Nhánh EA | Succeeded | Reversed | Hoàn khi giao dịch không hoàn tất | - |
| Nhánh EA | Pending hoặc Succeeded | ReconciliationRequired | Không chắc kết quả ghi nợ hoặc hoàn | - |
| Nhánh online | Pending | Succeeded | Webhook hợp lệ hoặc đối soát báo thành công | - |
| Nhánh online | Pending | Failed hoặc Cancelled | Provider báo thất bại, Parent hủy, hoặc phiên hết hạn | - |
| Nhánh online | Pending | ReconciliationRequired | Không xác định được kết quả, hoặc thành công muộn sau khi EA đã hoàn | - |



### Appendix B.



| ID | Câu hỏi | Ảnh hưởng | Phương án tạm trong FS |
| --- | --- | --- | --- |
| OQ-04 | Nguồn invoice chính thức; dataset test có được chấp nhận không | SCR-02 | Seed gắn nhãn |
| OQ-05 | Nguồn authoritative của số dư và giao dịch EA | Function 1, F9.4 | Function 1 giữ sổ cái; Function 9 lưu ID logic |
| OQ-08 | Dataset demo; online thật hay sandbox | Demo | Sandbox, seed gắn nhãn |
| OQ-11 | Loại phí được trả bằng EA, partial, provider, phương thức, callback, settlement | 3.1.2 bước 5, 6 | Trả đủ invoice một lần (EA, online hoặc chia đôi), sandbox |
| NQ-03 | Outstanding invoices gồm gì, có hạn nộp/overdue, theo từng con hay gộp | SCR-02 | Theo từng con; hạn nộp bắt buộc theo DB, cách hiển thị quá hạn TBC |
| NQ-04 | Khi có FAS, hiển thị số gốc hay sau giảm hay cả hai | SCR-02 | Chỉ số gốc; subsidy = 0 |
| NQ-05 | Hoàn tiền về đâu, ai chịu trách nhiệm khi lỗi | 1.6 OOS #3 | Ngoài phạm vi |
| NQ-09 | Có cho trả riêng từng dòng hoặc gộp nhiều invoice không | SCR-02, 05; 1.6 OOS #1, #2 | Một invoice mỗi lần, trả cả invoice |
| NQ-10 | Ngưỡng thời gian Pending trước khi chuyển ReconciliationRequired; chu kỳ truy vấn provider | F9.6 | Do Dev cấu hình; không tự Failed |
| NQ-11 | Thử lại dùng key mới hay cùng key | Bước 7 | Key mới cho lần thử mới (đề xuất) |
| NQ-12 | Định dạng mã tham chiếu và nội dung biên lai | SCR-07 | PAY-YYYYMMDD-XXXXXX (đề xuất) |
| NQ-13 | Mức tối thiểu cho phần EA và phần online khi chia đôi (C1) | SCR-04, VAL-18 | Không đặt mức cho phần EA; phần online theo provider (TBC) |
| NQ-14 | Ai xử lý hoàn tiền online khi provider báo thành công muộn sau khi EA đã hoàn (C2) | EX-12 | ReconciliationRequired, vận hành xử lý |
| NQ-15 | Function 1 có API ghi nợ và hoàn EA idempotent theo FundingReference không (D1) | BR-F9-03, F9.4 | Giả định có |
| NQ-16 | Dòng được trợ cấp 100% (Net = 0) không biểu diễn được vì DB yêu cầu Net > 0 (D3) | FAS Sprint 3 | Ngoài Sprint 1 |
| NQ-17 | Fee component và GST lấy từ Function 3 bằng API hay join (D4) | SCR-02 | Seed gắn sẵn trong Sprint 1 |
| NQ-18 | Thời hạn session portal và phiên online (đề xuất 10 phút) và thời gian quét nhánh mồ côi (D8) | EX-02, EX-11 | Do Dev cấu hình |
| NQ-19 | Danh sách phương thức thanh toán trực tuyến được hỗ trợ (thẻ Visa, Mastercard, PayNow...) và cơ chế ký webhook của provider | 1.4, Bước 6, BR-F9-06 | Thẻ và PayNow là giả định; HMAC-SHA256 trên sandbox |


Appendix C. Danh sách màn hình:



| Mã | Màn hình | Thành phần chính | Hành động | Trạng thái UI |
| --- | --- | --- | --- | --- |
| SCR-01 | Chọn con | Danh sách con đã liên kết (tên, trường, lớp), trạng thái có hay không có phí chưa thanh toán | Chọn con | Loading, Empty (không có liên kết), Error |
| SCR-02 | Phí chưa thanh toán | Widget số dư EA (nếu có EA), danh sách invoice của con (mở ra các dòng nhóm theo fee type: mô tả, fee component, GST, subsidy), số phải trả, hạn nộp, trạng thái, tổng còn nợ | Chọn invoice, đổi con | Loading, Error, Empty (xem SCR-03) |
| SCR-03 | Không có phí chưa thanh toán | Thông báo và liên kết quay lại | Quay lại SCR-01 | - |
| SCR-04 | Chọn cách thanh toán | Tóm tắt invoice; ba lựa chọn: Số dư EA (kèm số dư), Thanh toán trực tuyến, EA + trực tuyến (trừ hết EA balance, online tự tính phần còn lại) | Chọn cách thanh toán, tiếp tục, quay lại | EA và chia đôi bị vô hiệu khi EA không đủ điều kiện |
| SCR-05 | Xem lại và xác nhận | Con, invoice, tổng phải trả, từng phần (EA, online), số dư EA sau thanh toán | Xác nhận, hủy | Nút xác nhận bị vô hiệu sau khi bấm; Processing |
| SCR-06 | Đang chờ xử lý | Thông báo Pending hoặc đang xác minh (ReconciliationRequired), mã tham chiếu tạm; với chia đôi nêu rõ phần EA đã được trừ | Làm mới trạng thái, quay về SCR-02 | Pending, Verifying |
| SCR-07 | Xác nhận thanh toán | Trạng thái thành công, mã tham chiếu, thời gian, từng phần thanh toán (EA, online), tổng tiền, biên lai in hay tải PDF | Tải hay in biên lai, về SCR-02 | Success |
| SCR-08 | Thanh toán thất bại | Lỗi, lý do, mã tham chiếu, thông báo phần EA đã được hoàn (nếu có) | Thử lại (về SCR-04), thoát (về SCR-02) | Failed, Cancelled |


## 7. Ghi chú Thống nhất & Quyết định Nghiệp vụ (Reviewer & Team Decisions)

Dưới đây là các ghi chú, phản biện nghiệp vụ trực tiếp từ bản Google Doc FSD (chú thích `[a]` đến `[g]`):

| Mã | Loại | Vị trí liên quan | Nội dung thống nhất & Hướng dẫn triển khai |
| :--- | :---: | :--- | :--- |
| **`[a]`** | `[TD]` | SCR-02 (Danh sách phí) | **Hiển thị trạng thái Invoice:** Cần hiển thị rõ tình trạng của từng invoice trên giao diện (Unpaid, Paid, Overdue) để Parent dễ nhận biết. |
| **`[b]`** | `[WA]` | 1.3 Scope & Limitations | **Thời hạn phiên giao dịch:** Cần xác định thời hạn của mỗi phiên giao dịch thanh toán để tránh treo hóa đơn. |
| **`[c]`** | `[TD]` | 1.5 Exclusions & Split-Payment | **Quy tắc tính Bill khi Split-Payment:** Ví dụ 1 hóa đơn $100 không được tách thành 2 bill $50 + $50 rời rạc, mà chỉ được thanh toán đồng thời từ EA và Online trong 1 lần duy nhất $\rightarrow$ Hệ thống vẫn ghi nhận là thanh toán cho 1 invoice duy nhất. |
| **`[d]`** | `[WA]` | EX-02 / Refund Rule | **Chính sách hoàn tiền (Refund):** Giả định hiện tại là hoàn lại trực tiếp vào tài khoản nguồn đã thanh toán nếu giao dịch đã trừ tiền nhưng thất bại ở khâu xác nhận cuối; nếu lỗi xảy ra trước khi trừ tiền thì chặn từ đầu $\rightarrow$ chưa phát sinh giao dịch nên chưa cần hoàn. |
| **`[e]`** | `[TD]` | SCR-04 & Split-Payment Flow | **Quy tắc trừ số dư EA:** Không cho phép Parent tự nhập số tiền EA tùy ý. Hệ thống mặc định số tiền EA tự động bằng đúng giá trị hóa đơn (nếu EA đủ tiền) hoặc bằng toàn bộ số dư còn lại trong EA (nếu không đủ tiền, phần thiếu chuyển sang Online). |
| **`[f]`** | `[WA - Deferred]` | EX-02 Timeout | **Thời gian timeout phiên Online:** Giả định là 10 phút (theo thông lệ các cổng thanh toán ngân hàng). Nội dung này chưa triển khai trong Sprint 1 MVP mà làm ở Sprint sau. |
| **`[g]`** | `[REF]` | 4. Data Fields Table | **Rà soát ma trận dữ liệu:** Đội ngũ Dev/QA đối chiếu bảng Data Fields với bảng Master Data & Fee Calculation matrix của dự án. |


