# RULE MODULE 02: KỸ THUẬT KIỂM THỬ Ô INPUT & MA TRẬN TOÀN DIỆN (FIELD-LEVEL TEST MATRIX)
> **Mục đích**: Áp dụng khi thiết kế ca kiểm thử chi tiết cho từng ô nhập liệu, validate form, chống tràn/vỡ layout, bảo mật PII, và chống leak raw i18n keys.
> **Trọng tâm**: Bộ 12 lớp kiểm thử chung, quy chuẩn 8 nhóm ô nhập liệu, ma trận vòng đời form, UI health, PII client-side, và mô hình 3 trụ cột.

> [!IMPORTANT]
> **Applicability & path contract**: Đây là thư viện coverage, không phải nguồn để tự bịa business rule. Mỗi case phải được đánh dấu `Applicable`, `N/A` kèm lý do, hoặc `SPEC GAP`. Đọc/ghi bằng canonical paths (`specs/`, `testcases/`, `data/`, `tests/`); ba folder đánh số chỉ là navigation views bằng symlink.

> #### 4. Kỹ Thuật Kiểm Thử Bắt Buộc Cho Từng Ô Input (Universal Field-Level Black-Box & UI Integrity Matrix)
> [!IMPORTANT]
> **CẤM SINH TEST CASE HỜI HỢT (CHỈ TEST FILL ĐÚNG / SAI RỒI BẤM NÚT)**:
> Mọi ca kiểm thử cho từng ô nhập liệu (Input Field) BẮT BUỘC phải áp dụng đầy đủ Bộ Ma Trận 12 Lớp Kiểm Thử Chung và Các Quy Chuẩn Chuyên Biệt Theo Phân Nhóm Ô Nhập dưới đây. Tuyệt đối không được bỏ sót lỗi UI hiển thị raw translation key (như `features.parentProfile.validation.mobileInvalid` thay vì câu thông báo thật) hoặc thiếu kiểm tra viền đỏ (`aria-invalid="true"`).
>
> ##### A. Nhóm Kiểm Thử Chung Cho MỌI Loại Ô Nhập Liệu (12 Lớp Bắt Buộc 100%):
> 1. **Để trống ô bắt buộc (Empty Required Field)**: Xóa trắng ô -> Bắt buộc kích hoạt thông báo lỗi bắt buộc cụ thể (`MSG-0001`: *"Enter your <field>"*). Cấm để lỗi chung chung.
> 2. **Để trống ô không bắt buộc (Empty Optional Field)**: Để trống ô tùy chọn (ví dụ Block, Unit) -> Không báo lỗi, hệ thống cho phép Save thành công.
> 3. **Chỉ toàn dấu cách (All Whitespace - ASM-15)**: Nhập toàn ký tự khoảng trắng `"     "` -> Phải tự động trim và coi như rỗng, kích hoạt lỗi bắt buộc `MSG-0001`.
> 4. **Dấu cách đầu / cuối (Leading / Trailing Whitespaces)**: Nhập `"  abc  "` -> Tự động trim sạch khoảng trắng trước khi lưu hoặc báo lỗi theo Business Rule.
> 5. **Độ dài biên dưới (BVA Min: $Min-1$, $Min$, $Min+1$)**: Kiểm tra chính xác giới hạn tối thiểu của trường.
> 6. **Độ dài biên trên (BVA Max: $Max-1$, $Max$, $Max+1$)**: Kiểm tra chính xác giới hạn tối đa ($N-1, N, N+1$) (ví dụ: Block/Unit 20 vs 21; Street/Country 100 vs 101; Email 150 vs 151; Postal 6 vs 5/7; Mobile 8 vs 7/9) -> Ký tự thứ $N+1$ phải bị chặn bởi thuộc tính `maxlength` hoặc báo lỗi độ dài.
> 7. **Dán (paste) chuỗi cực dài (Stress Paste 1000+ chars)**: Dán 1000 ký tự -> Không treo trình duyệt, không tràn/vỡ layout, cắt ngắn an toàn hoặc từ chối hợp lệ.
> 8. **Ký tự đặc biệt & Ký tự cấm**: Thử nghiệm các ký tự `!@#$%^&*()`, và đối với các trường địa chỉ/tên kiểm tra các ký tự cấm `< > { } ;`.
> 9. **Ký tự Emoji, Tiếng Việt có dấu, chữ Trung/Nhật**: Thử `😀`, `Nguyễn Văn Minh`, `中文` -> Đảm bảo mã hóa UTF-8 toàn vẹn, không gây lỗi database/serialization.
> 10. **Chuỗi tấn công cơ bản (Security / XSS / SQLi)**: Bơm `<script>alert(1)</script>`, `' OR 1=1 --` -> Hệ thống phải mã hóa an toàn HTML entities, không thực thi script, không lỗi cú pháp.
> 11. **Xác thực Thông báo Lỗi UI & Chống Lộ Translation Key (i18n Key Leakage Prevention - BẮT BUỘC)**:
>     - ⛔ **CẤM HIỂN THỊ RAW I18N KEY**: Thông báo lỗi trên UI TUYỆT ĐỐI KHÔNG ĐƯỢC chứa các raw translation keys (ví dụ: `features.parentProfile.validation.mobileInvalid`, `features.*`, `validation.*`, `*.undefined`, `t(...)`). Kiểm thử tự động phải assert rằng thông báo lỗi là câu từ hoàn chỉnh (`MSG-0805`, `MSG-0806`, `MSG-0001`...) chứ không phải i18n key!
>     - **Visual Feedback**: Ô nhập khi có lỗi phải bật cờ `aria-invalid="true"` và có chỉ báo viền đỏ (red glowing border / class error).
>     - **Cơ chế tự xóa lỗi (Auto-dismissal)**: Thông báo lỗi và viền đỏ phải biến mất ngay lập tức khi người dùng nhập lại giá trị hợp lệ.
> 12. **Lưu bền vững và Reload (Persistence Integrity)**: Sau khi Save thành công, F5 reload trang -> Dữ liệu lưu đúng 100%, không bị cắt cụt, mất số 0 đầu hay biến dạng.
>
> ##### B. Quy Chuẩn Chuyên Biệt Cho 8 Phân Nhóm Ô Nhập Liệu & UI Controls (Thư Viện Case Sẵn Dùng Khi Màn Hình Có):
> 1. **Nhóm 1: Ô chỉ nhập SỐ (Numeric Fields: Mobile Number, Postal Code)**:
>    - Toàn số hợp lệ (`91234567`, `238888`).
>    - Lẫn chữ (`12345qqqq`, `1234abcd`) hoặc Chỉ toàn chữ (`abcdefgh`) -> Báo lỗi hoặc tự động chặn nhập chữ.
>    - Có dấu cách giữa (`9123 4567`) -> Tự trim hoặc báo lỗi theo rule.
>    - Ký tự toán học & số âm & thập phân (`+`, `-`, `()`, `91.234567`, `-9123456`) -> Từ chối hợp lệ.
>    - Chữ số Unicode kiểu khác: Full-width (`９１２３４５６７`), số Ả Rập Đông (`٩١٢٣`) -> Xử lý hoặc từ chối rõ ràng.
>    - Thiếu / Thừa số: 7 số hoặc 9 số đối với Mobile; 5 số hoặc 7 số đối với Postal Code -> Báo lỗi độ dài.
>    - **Bảo toàn số 0 đứng đầu (Leading Zero)**: `01234567`, `018956`, `000000` phải được giữ nguyên số 0 dưới dạng chuỗi, không bị ép kiểu làm mất số 0.
>    - Quy tắc đầu số Singapore: Số điện thoại phải bắt đầu bằng 6, 8, hoặc 9 (các đầu số khác như 1, 2, 3, 4, 5, 7 bị từ chối với `MSG-0805`).
>    - Dán số có ký tự ẩn từ clipboard (Excel/Zalo).
>    - Thuộc tính bàn phím di động: Kiểm tra `type="tel"` hoặc `inputmode="numeric"`.
> 2. **Nhóm 2: Ô chỉ nhập CHỮ (Alpha Fields: Full Name, Country)**:
>    - Chữ thường, chữ HOA, hoa thường lẫn lộn.
>    - Có số lẫn (`Singapore1`, `123`) -> Báo lỗi hoặc chặn.
>    - Chữ có dấu, tên có dấu gạch nối hoặc nháy đơn hợp lệ (`Anne-Marie`, `O'Connor`) -> Phải chấp nhận.
>    - Nhiều dấu cách liên tiếp giữa các từ (`New   York`).
> 3. **Nhóm 3: Ô nhập CHỮ + SỐ (Alphanumeric Fields: Block, Street, Unit)**:
>    - Chữ và số hợp lệ (`Blk 123`, `ORCHARD ROAD 1`).
>    - Chỉ toàn số (`123`) hoặc Chỉ toàn chữ (`ORCHARD ROAD`) -> Hợp lệ.
>    - Định dạng Singapore Unit (`#12-34`, `#02-01`, `12-34A`, `Level 2`).
>    - Ký tự thường gặp trong địa chỉ (`/`, `,`, `.`, `-`, `#`) -> Chấp nhận. Ký tự cấm (`< > { } ;`) -> Báo lỗi hoặc loại bỏ.
>    - Giới hạn độ dài biên: 20 vs 21 ký tự (Block, Unit); 100 vs 101 ký tự (Street).
>    - Xuống dòng (Enter) khi dán nhiều dòng -> Không vỡ giao diện, tự chuẩn hóa thành 1 dòng.
> 4. **Nhóm 4: Ô Email (Email Format)**:
>    - Hợp lệ: Chuẩn RFC 5322, subdomain (`abc@mail.company.com.sg`), tag (`a+tag@gmail.com`), chuẩn hóa chữ thường.
>    - Không hợp lệ: Thiếu @ (`abc`), thiếu domain (`abc@`), thiếu user (`@gmail.com`), thiếu TLD (`abc@gmail`), hai dấu @ (`abc@@gmail.com`), khoảng cách (`a b@gmail.com`), hai chấm (`abc@gmail..com`), dấu phẩy (`abc@gmail,com`), TLD ngắn (`abc@gmail.c`).
>    - Quá dài: Tổng độ dài >254 ký tự hoặc phần trước @ >64 ký tự.
> 5. **Nhóm 5: Dropdown / Combobox (ví dụ ô Language, Country, Role filter)**:
>    - *Mở danh sách*: Thấy đủ các tùy chọn (English / Vietnamese), đúng thứ tự quy định.
>    - *Giá trị mặc định*: Khớp chính xác với ngôn ngữ/trạng thái hiện tại của người dùng.
>    - *Chọn bằng chuột / Bàn phím*: Hỗ trợ phím mũi tên `Up`/`Down`, phím `Enter` để chọn, phím `Esc` để đóng dropdown mà không đổi giá trị.
>    - *Gõ để lọc*: Gõ ký tự tìm kiếm lọc options; khi gõ không có kết quả phải hiển thị trạng thái rỗng ("No results found" / "Không có kết quả").
>    - *Xóa lựa chọn*: (Nếu là optional) Nút Clear đưa về trạng thái chưa chọn; nếu là bắt buộc thì chặn xóa hoặc báo lỗi.
>    - *Danh sách dài*: Hỗ trợ cuộn mượt (virtual scrolling/scrollbar), không tràn màn hình hoặc vỡ modal.
>    - *Lưu và tải lại*: Sau khi chọn rồi F5 reload trang, lựa chọn phải được bảo toàn (cookie/localStorage/profile DB).
>    - *Đổi khi form đang dirty*: Thay đổi dropdown khi form đang sửa dở thì các dữ liệu đang nhập không bị mất.
> 6. **Nhóm 6: Date Picker (khi màn hình có ngày sinh, ngày giao dịch, kỳ hạn)**:
>    - *Gõ tay vs Chọn lịch*: Gõ `25/12/2026` hoặc bấm chọn ngày 25/12/2026 trên popup lịch phải cho cùng 1 kết quả.
>    - *Sai định dạng*: `2026-12-25`, `25-12-2026`, `abc` -> Bị từ chối hoặc tự chuẩn hóa.
>    - *Ngày không tồn tại*: `31/02/2026`, `00/00/0000`, `32/01/2026` -> Bị chặn hoặc báo lỗi không hợp lệ.
>    - *Năm nhuận*: `29/02/2028` (năm nhuận) -> Hợp lệ; `29/02/2027` (năm thường) -> Bị từ chối.
>    - *Quá khứ / Tương lai*: Ngày sinh không được ở tương lai; ngày hiệu lực không được ở quá khứ (theo Business Rule).
>    - *Ngày bị khóa*: Các ngày nằm ngoài phạm vi bị bôi xám (disabled) trên popup lịch, không thể click chọn.
>    - *Khoảng ngày*: Ngày bắt đầu (From) > Ngày kết thúc (To) -> Bị chặn và báo lỗi.
>    - *Múi giờ*: Thao tác gần thời điểm 00:00 hoặc chuyển đổi múi giờ (UTC vs SGT UTC+8) không làm lệch sang ngày hôm trước/hôm sau.
>    - *Bàn phím*: Phím mũi tên di chuyển ô ngày, `PageUp`/`PageDown` chuyển tháng/năm, `Esc` đóng lịch.
> 7. **Nhóm 7: Checkbox / Radio / Toggle Switch (ví dụ Show/Hide NRIC, Agree Terms, Tri-state)**:
>    - *Trạng thái mặc định*: NRIC đang che dạng `*****123F`, nút hiển thị nhãn "Show NRIC".
>    - *Bấm Show*: Hiển thị đầy đủ số NRIC, nhãn nút đổi ngay thành "Hide NRIC".
>    - *Bấm Hide*: Che lại số NRIC, nhãn nút hoàn nguyên về "Show NRIC".
>    - *Tự che lại & Reload*: Chuyển trang hoặc reload F5 thì NRIC luôn tự động che lại về mặc định an toàn.
>    - *Không làm dirty form*: Thao tác Show/Hide NRIC chỉ thay đổi hiển thị, không làm bẩn form (Save button vẫn disabled).
>    - *CLS = 0*: Thao tác Show/Hide NRIC không gây giật layout, không làm xô lệch các trường lân cận.
>    - *Bàn phím & Screen Reader*: Phím `Space`/`Enter` để bật/tắt; có `aria-label`, `aria-pressed` hoặc `aria-checked` rõ ràng.
>    - *Checkbox bắt buộc (Điều khoản PDPA)*: Chưa tích checkbox cam kết -> Chặn Save và hiển thị lỗi bắt buộc.
>    - *Radio Button*: Trong cùng một nhóm chỉ chọn được đúng 1 tùy chọn; nếu bắt buộc mà chưa chọn -> Báo lỗi.
>    - *Checkbox Tri-state*: Trạng thái `indeterminate` (chọn một phần) hiển thị đúng gạch ngang trên UI.
> 8. **Nhóm 8: File Upload / Drag & Drop (khi màn hình có tải tài liệu minh chứng, đính kèm)**:
>    - *File hợp lệ*: File `.pdf`, `.jpg`, `.png` có dung lượng $< 5\text{MB}$ tải lên thành công.
>    - *Biên dung lượng BVA*: Đúng $5\text{MB}$ -> Chấp nhận; $5\text{MB} + 1\text{ byte}$ -> Bị từ chối và báo lỗi kích thước.
>    - *Đuôi file cấm*: `.exe`, `.sh`, `.bat`, `.js`, `.vbs`, `.php` -> Bị từ chối ngay lập tức.
>    - *Đổi đuôi giả (Magic Bytes check)*: Đổi tên `virus.exe` thành `virus.pdf` -> Hệ thống phải kiểm tra MIME-type/Magic header thật và từ chối.
>    - *Tấn công 2 đuôi*: `malware.pdf.exe` -> Bị chặn hoàn toàn.
>    - *File rỗng & File hỏng*: File $0\text{ byte}$ hoặc file bị hỏng cấu trúc -> Báo lỗi không hợp lệ.
>    - *Tên file đặc biệt*: Tên chứa tiếng Việt có dấu, khoảng trắng, ký tự đặc biệt, hoặc độ dài $> 255$ ký tự -> Xử lý an toàn, không vỡ layout.
>    - *Kéo thả & Nhiều file*: Hỗ trợ kéo-thả (drag-and-drop); nếu cho phép nhiều file phải hiển thị danh sách đính kèm rõ ràng; xử lý trùng tên file.
>    - *Tiến trình & Thao tác*: Có thanh tiến trình (progress bar), nút Hủy khi đang tải, nút Xóa file đã tải kèm xác nhận.
>    - *Mất mạng giữa chừng*: Đứt kết nối khi đang tải file -> Báo lỗi kết nối thân thiện, cho phép người dùng thử lại (Retry).
>
> ---
>
> ##### C. Ma Trận Vòng Đời Form & Trạng Thái Tương Tác (Form Interaction & State Lifecycle Matrix):
> | Trạng Thái / Hành Vi | Kịch Bản Kiểm Thử Chi Tiết | Kết Quả Kỳ Vọng Bắt Buộc |
> | :--- | :--- | :--- |
> | **Pristine $\leftrightarrow$ Dirty** | • Mới mở trang / Mới chuyển Edit Mode<br>• Sửa 1 ký tự bất kỳ trên form<br>• Gõ lại ký tự cũ (hoàn nguyên baseline)<br>• Chỉ thêm dấu cách thừa / đổi chữ hoa thường | • Nút Save bị vô hiệu hóa (`disabled=true`) kèm gợi ý *"Make a change to enable saving."*<br>• Nút Save sáng lên kích hoạt (`disabled=false`), ẩn gợi ý.<br>• Nút Save tự động khóa lại (`disabled=true`) khi dữ liệu trùng khớp baseline ban đầu.<br>• Phải đối soát Business Rule xem khoảng cách thừa có được tính là Dirty hay tự động trim. |
> | **Validate khi Save** | • Form đang có 1 ô nhập bị lỗi cú pháp<br>• Form có nhiều ô nhập bị lỗi cùng lúc | • Bấm Save thay vì gửi request sẽ chặn lại, tự động scroll và focus vào ô lỗi đầu tiên.<br>• Toàn bộ các ô lỗi đều bật viền đỏ `aria-invalid="true"` và hiện câu thông báo lỗi đầy đủ đồng thời. |
> | **Save thành công** | • Toàn bộ trường dữ liệu hợp lệ và bấm Save | • Hiển thị toast/banner thành công (`MSG-0807`), nút Save tắt lại, mốc baseline "chưa sửa" được cập nhật thành dữ liệu mới. |
> | **Save thất bại (API Fault)** | • API trả về mã lỗi HTTP 400, 401, 403, 409, 422, 500, hoặc Network Timeout | • Hiển thị thông báo lỗi hệ thống dễ hiểu (`MSG-0808`), **giữ nguyên toàn bộ dữ liệu người dùng đã gõ** (không xóa trắng form), cho phép bấm thử lại. |
> | **Chống bấm đúp (Debounce)** | • Người dùng click chuột liên tiếp 2-3 lần vào nút Save trong khoảng thời gian ngắn (<300ms) | • Nút Save lập tức khóa click (`isSubmitting=true`); **chỉ gửi duy nhất 1 request** lên server, không sinh duplicate record hay xung đột dữ liệu. |
> | **Trạng thái Loading** | • Trong quá trình chờ backend phản hồi API mutation | • Nút Save bị khóa, hiển thị spinner xoay tròn, gán cờ `aria-busy="true"`, toàn bộ các ô nhập bị vô hiệu hóa tạm thời để chống sửa đổi chéo. |
> | **Phím Enter trong ô nhập** | • Nhấn phím Enter khi đang focus trong ô text input | • Thực hiện Submit (nếu thiết kế hỗ trợ) hoặc không làm gì, nhưng hành vi phải nhất quán trên toàn bộ các trường. |
> | **Thao tác Cancel (Hủy)** | • Đang có dữ liệu dirty $\rightarrow$ Bấm nút Cancel<br>• Form chưa sửa gì (Pristine) $\rightarrow$ Bấm nút Cancel | • Hoàn nguyên toàn bộ giá trị về ban đầu, xóa sạch các thông báo lỗi inline validation, quay về View Mode (nếu có modal xác nhận thì phải tuân theo rule).<br>• Quay về View Mode an toàn, không sinh lỗi. |
> | **Rời trang khi chưa lưu (Unsaved Changes)** | • Đang có dữ liệu dirty mà người dùng bấm Menu điều hướng, bấm nút Back trình duyệt, refresh (F5), đóng tab, Log out hoặc đổi ngôn ngữ | • Hệ thống phải bật cảnh báo xác nhận *"Bạn có thay đổi chưa lưu. Bạn có chắc chắn muốn rời đi?"* để ngăn chặn mất mát dữ liệu vô ý. |
> | **Hộp thoại xác nhận (Modal Alertdialog)** | • Bấm nút Save mở modal xác nhận (nếu có) | • Focus bàn phím bị giữ chặt bên trong modal (Focus Trap); phím `Tab` xoay vòng giữa các nút; phím `Esc` đóng modal; click ra nền mờ không làm mất dữ liệu trên form. |
> | **Hết phiên (Session Timeout)** | • Hết hạn phiên đăng nhập trong lúc đang điền form rồi bấm Save | • Chuyển hướng về trang đăng nhập, không âm thầm làm mất dữ liệu đã gõ, hiển thị thông báo yêu cầu đăng nhập lại rõ ràng. |
> | **Đồng thời (Concurrency)** | • Mở 2 tab cùng sửa hồ sơ của 1 người dùng, lưu lần lượt | • Hệ thống phải áp dụng cơ chế Khóa Lạc Quan (Optimistic Locking) hoặc thông báo xung đột dữ liệu: tab lưu sau cảnh báo dữ liệu đã bị sửa đổi ở phiên khác. |
> | **Mạng chập chờn / Ngoại lệ** | • Mất kết nối mạng (Offline) hoặc Slow 3G khi bấm Save | • Báo lỗi kết nối mạng thân thiện, không treo đơ trình duyệt, không lưu nửa vời (inconsistent partial save). |
> | **Tính nhất quán liên trang** | • Sau khi Save thành công tại trang Profile, điều hướng sang các trang Transactions / FAS / Billing | • Dữ liệu liên hệ mới (Phone, Email, Mailing Address) phải được cập nhật đồng bộ tức thì, không bị cache dữ liệu cũ. |
>
> ---
>
> ##### D. Ma Trận Sức Khỏe Giao Diện & Trải Nghiệm Người Dùng (UI Health & Visual Integrity Matrix - Coverage under Invariant 7):
> | Tiêu Chí Sức Khỏe | Phương Pháp Kiểm Tra / Đo Lường | Tiêu Chuẩn Nghiệm Thu Bắt Buộc (Đạt Khi) |
> | :--- | :--- | :--- |
> | **Console sạch (Zero Console Errors)** | Gắn lắng nghe `page.on('pageerror')` và `page.on('console')`, thao tác qua toàn bộ chức năng, chuyển tab, kích hoạt lỗi | **0 lỗi JavaScript (Uncaught exceptions)**, **0 request tài nguyên thất bại (HTTP 404/500)**, 0 cảnh báo nghiêm trọng. |
> | **Không cuộn ngang (Zero Horizontal Scroll)** | Đo lường `document.documentElement.scrollWidth === clientWidth` trên toàn bộ dải kích thước màn hình | **Không xuất hiện thanh cuộn ngang** tại mọi breakpoint: 1920, 1440, 1366, 1280, 1024, 768, 480, 375, 320 px. |
> | **Navbar & Header Responsive** | Thay đổi chiều rộng trình duyệt (resize viewport) từ 1920px xuống 320px | **Không bị vỡ thành 3 dòng chữ lộn xộn** (đặc biệt tại ngưỡng ~880px); khi thu hẹp phải tự động co gọn hoặc chuyển thành Hamburger Menu. |
> | **Độ ổn định Layout (CLS = 0)** | Thao tác Show/Hide NRIC, hiển thị lỗi inline, chuyển đổi ngôn ngữ, xuất hiện thông báo toast | **Cumulative Layout Shift = 0**; không làm giật form, không đẩy lệch vị trí các ô nhập khác (ví dụ: lỗi ô Mobile không được đẩy lệch ô Email). |
> | **Tương phản màu (WCAG 2.1 AA)** | Sử dụng công cụ kiểm tra độ tương phản màu (Color Contrast Analyzer) trên toàn bộ phần tử UI | • Văn bản thường: Độ tương phản $\ge 4.5:1$.<br>• Văn bản lớn, badges, viền ô nhập, chỉ báo focus: Độ tương phản $\ge 3:1$. |
> | **Zoom & Co giãn bố cục (Reflow)** | Phóng to trang ở các mức 100%, 125%, 150%, 200%, 400% | Không bị mất nội dung văn bản, không bị che khuất các nút bấm hành động (Action Buttons), hỗ trợ cuộn dọc mượt mà. |
> | **Xoay màn hình (Orientation)** | Giả lập xoay màn hình thiết bị di động (Dọc Portrait $\leftrightarrow$ Ngang Landscape) | Bố cục tự động thích nghi mượt mà, các nút bấm và ô nhập không bị tràn ra ngoài khung nhìn. |
> | **Điều hướng Bàn phím (Keyboard Accessible)** | Chỉ sử dụng duy nhất bàn phím (`Tab`, `Shift+Tab`, `Enter`, `Space`, `Esc`, Mũi tên) từ đầu đến cuối | Thực hiện được $100\%$ mọi tác vụ trên trang; **vòng viền Focus (Focus Ring Outline) hiển thị rõ nét**, không bị mất dấu. |
> | **Liên kết bỏ qua (Skip Link)** | Nhấn phím `Tab` đầu tiên ngay khi trang vừa tải xong | Xuất hiện nút "Skip to main content" (Bỏ qua đến nội dung chính); bấm `Enter` nhảy thẳng tiêu điểm vào thẻ `<main>`. |
> | **Cấu trúc ngữ nghĩa (Semantic HTML)** | Kiểm tra cây DOM HTML của trang web | Thứ bậc thẻ tiêu đề đúng chuẩn (`<h1>` duy nhất, sau đó đến `<h2>`, `<h3>`); đầy đủ các vùng mốc ngữ nghĩa (`<header>`, `<nav>`, `<main>`, `<footer>`); thuộc tính `<html lang="...">` cập nhật đúng theo ngôn ngữ đang chọn. |
> | **Hỗ trợ trình đọc màn hình (Screen Reader)** | Sử dụng công cụ kiểm tra trợ năng / ARIA tree (NVDA / VoiceOver) | Đọc đúng nhãn (label) của ô nhập, đọc dấu hiệu bắt buộc (`aria-required="true"`), đọc đúng câu thông báo lỗi thực tế (`role="alert"`), **tuyệt đối không đọc raw i18n key**. |
> | **Bảo toàn văn bản dài (Text Truncation)** | Thử nghiệm với Họ tên cực dài, Địa chỉ dài 100 ký tự, tiếng Việt có dấu (chuỗi dài hơn tiếng Anh) | Tự động xuống dòng hoặc cắt ngắn an toàn kèm Tooltip hiển thị đầy đủ; không bị vỡ khung viền hoặc tràn chữ đè lên nút khác. |
> | **Trạng thái hiển thị toàn diện** | Kiểm tra các trạng thái CSS của mọi control tương tác | Thể hiện trực quan, rõ ràng và nhất quán giữa các trạng thái: `default`, `hover`, `focus`, `active`, `disabled`, `error`, và `loading`. |
> | **Quốc tế hóa toàn vẹn (i18n Integrity)** | Duyệt toàn bộ các màn hình và trạng thái lỗi ở cả 2 ngôn ngữ (English và Vietnamese) | **Không chứa raw translation key** (`features.*`, `validation.*`); không bị lẫn lộn ngôn ngữ trên cùng 1 trang; hiển thị đầy đủ dấu tiếng Việt, không lỗi font. |
> | **Tương thích đa trình duyệt & Thiết bị** | Chạy kiểm thử tự động trên Chrome, Edge, Firefox, WebKit (Safari), Mobile Safari iOS, Chrome Android | Mọi tính năng, bố cục và thông báo lỗi hoạt động đồng nhất, không phát sinh lỗi riêng biệt trên từng engine trình duyệt. |
> | **Hiệu năng giao diện (UI Performance)** | Đo thời gian tải trang ban đầu (FCP, LCP) và thời gian phản hồi khi bấm nút Save | Nằm trong ngưỡng SLA thỏa thuận (<2 giây tải trang); giao diện mượt mà 60fps, không bị giật lag khi gõ văn bản. |
>
> ---
>
> ##### E. Ma Trận Bảo Mật Phía Trình Duyệt & Dữ Liệu Cá Nhân PII (Client-Side Security & PII Protection):
> | Vùng Bảo Mật | Phương Pháp Kiểm Tra & Đánh Giá | Tiêu Chuẩn Nghiệm Thu An Toàn Bắt Buộc (Đạt Khi) |
> | :--- | :--- | :--- |
> | **URL / Thanh địa chỉ / History** | Kiểm tra chuỗi URL, hash `#`, và lịch sử trình duyệt sau khi thực hiện các thao tác | **Tuyệt đối không chứa PII nhạy cảm** (Số NRIC, Số điện thoại, Email, Địa chỉ nhà) trên URL query parameters hay history. |
> | **Bộ nhớ trình duyệt (Browser Storage)** | Kiểm tra DevTools $\rightarrow$ Application: `localStorage`, `sessionStorage`, `IndexedDB`, và `Cookies` | **Không lưu trữ PII dưới dạng văn bản rõ (cleartext)**; token xác thực phải được bảo vệ an toàn (HttpOnly/Secure cookies nếu dùng cookie). |
> | **Kiểm tra DOM (DOM Inspection)** | Kiểm tra cây DOM HTML trước khi người dùng bấm nút "Show NRIC" | Các thuộc tính `data-*`, thẻ `<input type="hidden">`, hoặc các node HTML ẩn **không được chứa số NRIC đầy đủ** trước khi người dùng chủ động yêu cầu giải mã. |
> | **Nhật ký mạng (Network Payloads)** | Kiểm tra gói tin Network response trả về trước khi bấm Show NRIC và URL query | NRIC trả về ban đầu phải được che mặt nạ từ phía máy chủ; PII không được truyền tải qua query string của các request GET/POST. |
> | **Nhật ký Log & Thông báo lỗi** | Kiểm tra Console trình duyệt và nội dung các hộp thoại thông báo lỗi | **Không in PII nhạy cảm ra Console**; không để lộ dấu vết ngăn xếp máy chủ (Server Stack Trace) hay thông tin cấu trúc cơ sở dữ liệu khi có lỗi phát sinh. |
> | **Phân quyền truy cập (BOLA / IDOR)** | Thay đổi User ID / Parent ID trên URL hoặc trong payload request API (gọi chéo hồ sơ người khác) | Hệ thống từ chối với mã HTTP `403 Forbidden` hoặc `404 Not Found` kèm `MSG-0003`; **tuyệt đối không xem hoặc sửa được hồ sơ của người khác**. |
> | **Chống gán dữ liệu hàng loạt (Mass Assignment)** | Cố tình inject thêm các trường read-only (`fullName`, `nric`, `residentialAddress`) vào payload PUT/PATCH | Backend API tự động bỏ qua (ignore) hoặc từ chối request; các dữ liệu nguồn từ Singpass MyInfo được bảo toàn bất biến tuyệt đối. |
> | **Trạng thái chưa đăng nhập (Unauthenticated)** | Cố tình truy cập trực tiếp URL trang cá nhân (`/profile`) khi chưa đăng nhập | Hệ thống lập tức chặn lại và chuyển hướng về trang đăng nhập Singpass; không để lộ bất kỳ mẩu dữ liệu cá nhân nào. |
> | **Sau khi Đăng xuất (Post-Logout Cache)** | Sau khi bấm Log out, nhấn nút Back trên trình duyệt | Hệ thống không hiển thị lại dữ liệu hồ sơ cá nhân đã cache; yêu cầu đăng nhập lại ngay lập tức. |
> | **Quản lý phiên (Session Security)** | Token hết hạn, hoặc đăng nhập đồng thời từ 2 vị trí khác nhau | Xử lý chấm dứt phiên an toàn, yêu cầu xác thực lại, không phát sinh lỗi bất thường. |
> | **Tiêu đề bảo mật & Truyền tải (Security Headers)** | Kiểm tra các HTTP Response Headers của trang web | Bắt buộc kết nối an toàn qua **HTTPS**; có header `Cache-Control: no-store, no-cache` cho các trang chứa dữ liệu cá nhân; có `Content-Security-Policy (CSP)`; có `X-Frame-Options: DENY` hoặc `SAMEORIGIN` để chống clickjacking. |
> | **Chống tấn công lặp lại & CSRF (Rate Limit / Anti-CSRF)** | Gửi liên tục hàng loạt request Save trong thời gian cực ngắn | Hệ thống kích hoạt cơ chế giới hạn tần suất (Rate Limiting) hoặc chặn CSRF hợp lệ; không bị treo server hay tê liệt dịch vụ. |
> | **Payload lạ & Dữ liệu độc hại (Data Injection)** | Gửi dữ liệu sai kiểu, payload JSON hỏng cú pháp, hoặc body dung lượng lớn (>1MB) | Hệ thống xử lý từ chối sạch sẽ với các mã lỗi HTTP 4xx (400 Bad Request, 413 Payload Too Large, 422 Unprocessable Entity); **tuyệt đối không bị sập máy chủ (HTTP 500)**. |
>
> ---
>
> ##### F. Chuẩn Hóa "Mô Hình 3 Trụ Cột (3-Tier Test Architecture)" Cho Toàn Bộ Dự Án:
> Mọi file đặc tả Test Case (`.md`) và Bảng tính Excel Evidence (`TEST_EXECUTION_EVIDENCE_*.xlsx`) khi được AI Coding khởi tạo hoặc cập nhật **BẮT BUỘC PHẢI PHÂN CHIA ĐẦY ĐỦ THÀNH 3 TRỤ CỘT ĐỘC LẬP**:
> 1. ⚖️ **Trụ Cột 1: Business Rules (BR)**: Toàn bộ các ca kiểm thử luật nghiệp vụ cốt lõi, điều kiện tiên quyết, phân quyền vòng đời (ví dụ: tuổi con $\ge 16$), tính độc lập dữ liệu giữa cha mẹ, bảo mật BOLA/IDOR, tính bất biến Singpass (`D-20`), và quy định cấm gửi email (`D-28`).
> 2. 🎯 **Trụ Cột 2: Acceptance Criteria (AC)**: Toàn bộ các ca kiểm thử tiêu chuẩn nghiệm thu chức năng User Story (Given - When - Then, che/hiện NRIC, bật tắt chế độ Edit, hộp thoại Modal Alertdialog, định dạng chuẩn hợp lệ Singapore, các mã lỗi thông báo hệ thống chuẩn `MSG-0805`, `MSG-0806`, `MSG-0001`, `MSG-0808`).
> 3. 🛠️ **Trụ Cột 3: Tech & UI Matrix**: Toàn bộ các ca kiểm thử kỹ thuật sâu theo Ma Trận Ô Nhập 12 lớp, các UI Controls mở rộng (Dropdown, DatePicker, Checkbox/Radio, FileUpload), Ma trận Vòng đời Form (Pristine/Dirty, Debounce, Cancel), Sức khỏe UI và Ma trận Bảo mật PII thuộc phạm vi độ phủ của Invariant 7 (0 Console Error, 0 Scrollbar ngang, CLS = 0, WCAG 2.1 AA, không rò rỉ dữ liệu nhạy cảm).
>
> ---
>

##### G. THƯ VIỆN TEST CASE & BẢNG ĐỐI CHIẾU NHANH (QUICK TEST CASE CHEAT-SHEET)
> [!TIP]
> Bảng tra cứu đối chiếu nhanh khi thiết kế Test Case cho các Controls mở rộng, Vòng đời Form, UI Health và PII. Sử dụng để bổ sung trực tiếp vào Trụ Cột 3 (Tech & UI Matrix) khi màn hình có các thành phần tương ứng.

### 7. Controls khác (thư viện case sẵn dùng khi màn hình có)

#### Dropdown / Combobox (ví dụ ô Language)
| Case | Kỳ vọng |
| :--- | :--- |
| Mở danh sách, thấy đủ English / Vietnamese | Đúng, đúng thứ tự |
| Giá trị mặc định | Đúng ngôn ngữ hiện tại |
| Chọn bằng chuột / bàn phím (Up/Down/Enter/Esc) | Hoạt động, Esc đóng không đổi |
| Gõ để lọc, gõ không có kết quả | Có trạng thái rỗng “không có kết quả” |
| Xóa lựa chọn (nếu có) | Về trạng thái chưa chọn, báo bắt buộc nếu cần |
| Danh sách dài | Cuộn mượt, không tràn màn hình |
| Chọn rồi reload | Lựa chọn được nhớ (cookie/localStorage/profile) |
| Đổi khi đang có form dirty | Dữ liệu đang nhập không bị mất |

#### Date Picker (khi có)
| Case | Dữ liệu | Kỳ vọng |
| :--- | :--- | :--- |
| Gõ tay vs chọn lịch | 25/12/2026 | Cùng kết quả |
| Sai định dạng | 2026-12-25, 25-12-2026, abc | ✖ |
| Ngày không tồn tại | 31/02/2026, 00/00/0000 | ✖ |
| Năm nhuận | 29/02/2028 ✔, 29/02/2027 ✖ | đúng |
| Quá khứ / tương lai | hôm qua, năm 1800, năm 9999 | theo rule |
| Ngày bị khóa | ô xám trong lịch | không chọn được |
| Khoảng ngày | từ > đến | ✖ |
| Múi giờ | gần 00:00, đổi múi giờ | Không lệch ngày |
| Bàn phím | mũi tên, PageUp/Down, Esc | Hoạt động |

#### Checkbox / Radio / Toggle (ví dụ Show NRIC)
| Case | Kỳ vọng |
| :--- | :--- |
| Trạng thái mặc định | NRIC đang che *****123F, nút “Show NRIC” |
| Bấm Show | Hiện đủ NRIC, nút đổi thành Hide |
| Bấm Hide | Che lại |
| Tự che lại | ❓ sau bao lâu / sau khi chuyển trang |
| Reload hoặc quay lại trang | Mặc định che lại |
| Không làm form “dirty” | Save vẫn tắt |
| Không làm layout giật | CLS = 0 |
| Bàn phím + screen reader | Space/Enter bật tắt; có tên đọc được, trạng thái (aria-pressed) |
| Checkbox bắt buộc (điều khoản) | Chưa tích → ✖ chặn Save |
| Radio | chỉ chọn được 1; không chọn → ✖ nếu bắt buộc |
| Checkbox tri-state | trạng thái indeterminate hiển thị đúng |

#### File Upload (khi có)
| Case | Dữ liệu | Kỳ vọng |
| :--- | :--- | :--- |
| Hợp lệ | .pdf, .jpg < 5MB | ✔ |
| Đúng 5MB / 5MB + 1 byte | | ✔ / ✖ |
| Đuôi cấm | .exe, .sh, .bat, .js | ✖ |
| Đổi đuôi giả | virus.exe → virus.pdf | ✖ (kiểm tra nội dung thật) |
| Hai đuôi | a.pdf.exe | ✖ |
| File rỗng 0 byte, file hỏng | | ✖ |
| Tên file lạ | tiếng Việt, ký tự đặc biệt, 255+ ký tự | Xử lý an toàn |
| Kéo-thả, nhiều file, trùng tên | | Theo rule |
| Thanh tiến trình, hủy, xóa file đã tải | | Hoạt động |
| Mất mạng giữa chừng | | Báo lỗi, cho thử lại |

---

### 8. Vòng đời form (nút Save / Cancel, trạng thái)
| Nhóm | Case | Kỳ vọng |
| :--- | :--- | :--- |
| **Pristine ↔ Dirty** | Mới mở trang | Save tắt + gợi ý “Make a change to enable saving.” |
| | Sửa 1 ký tự | Save bật |
| | Sửa rồi gõ lại như cũ | Save tắt lại |
| | Chỉ thêm dấu cách / đổi hoa thường | ❓ có tính là thay đổi không |
| **Save khi lỗi** | Có ô lỗi, bấm Save | Không gửi request, focus nhảy tới ô lỗi đầu tiên, nhiều lỗi hiện cùng lúc |
| **Save thành công** | Dữ liệu hợp lệ | Thông báo thành công, Save tắt lại, mốc “chưa sửa” được cập nhật |
| **Save thất bại** | API 400/401/403/409/422/500/timeout | Báo lỗi dễ hiểu, giữ nguyên dữ liệu đã nhập, cho thử lại |
| **Double-click** | Bấm Save 2 lần liên tiếp | Chỉ gửi 1 request |
| **Loading** | Trong lúc lưu | Nút khóa, có spinner, aria-busy="true", không sửa thêm được |
| **Enter** | Nhấn Enter trong ô | Submit (nếu thiết kế) hoặc không làm gì, nhưng nhất quán |
| **Cancel** | Đang sửa → Cancel | Về giá trị cũ, xóa lỗi; ❓ có hỏi xác nhận không |
| | Cancel khi chưa sửa | Không lỗi |
| **Rời trang khi chưa lưu** | Menu, nút Back, refresh, đóng tab, Log out, đổi ngôn ngữ | ❓ có cảnh báo không |
| **Hộp thoại xác nhận (nếu có)** | Mở modal | Focus bị giữ trong modal, Tab xoay vòng, Esc đóng, bấm nền không mất dữ liệu |
| **Phiên** | Hết phiên khi đang sửa rồi Save | Về đăng nhập, không mất dữ liệu âm thầm, báo rõ |
| **Đồng thời** | 2 tab cùng sửa, lưu lần lượt | ❓ ai thắng, có báo xung đột |
| **Mạng** | Offline / Slow 3G khi Save | Báo lỗi, không treo, không lưu nửa vời |
| **Tính nhất quán** | Sau Save, xem Transactions/FAS/Billing | ❓ thông tin liên hệ đồng bộ |

---

### 9. Sức khỏe giao diện (UI health)
| Nhóm | Case | Kỳ vọng |
| :--- | :--- | :--- |
| **Console** | Mở trang, thao tác mọi nút, đổi ngôn ngữ, bật lỗi | 0 lỗi JS, 0 request lỗi (404), 0 cảnh báo nghiêm trọng |
| **Cuộn ngang** | Rộng 1920 / 1440 / 1366 / 1280 / 1024 / 768 / 480 / 375 / 320 px | Không có thanh cuộn ngang |
| **Navbar** | Mỗi độ rộng ở trên | Không vỡ 3 dòng (bạn đã thấy ở ~880px); nếu thu gọn thì có menu hamburger |
| **Zoom** | 100%, 125%, 150%, 200%, 400% | Không mất nội dung, không che nút |
| **Xoay màn hình** | Dọc ⇄ ngang | Bố cục thích nghi |
| **CLS = 0** | Show/Hide NRIC, hiện lỗi inline, đổi ngôn ngữ, hiện toast | Không giật, không đẩy lệch ô khác (Email lệch khi Mobile báo lỗi = lỗi) |
| **Tương phản** | Chữ thường, chữ lớn, badge, thông báo lỗi, placeholder, viền ô | ≥ 4.5:1 (chữ thường), ≥ 3:1 (chữ lớn, thành phần UI) |
| **Bàn phím** | Chỉ dùng bàn phím từ đầu đến cuối | Làm được mọi thao tác, focus thấy rõ |
| **Skip link** | Tab đầu tiên | Hiện “Skip to main content”, nhảy đúng vùng nội dung |
| **Cấu trúc** | Heading, landmark (nav, main, footer), lang của trang | Đúng thứ bậc, lang đổi theo ngôn ngữ |
| **Screen reader** | Đọc nhãn, dấu *, lỗi, nút | Đọc đúng, không đọc key |
| **Văn bản dài** | Tên dài, địa chỉ dài, tiếng Việt (dài hơn tiếng Anh) | Xuống dòng hoặc cắt có tooltip, không tràn |
| **Trạng thái hiển thị** | Hover, focus, active, disabled, lỗi, loading | Mỗi trạng thái rõ ràng, nhất quán |
| **i18n** | Duyệt toàn trang ở English và Vietnamese | Không có key thô, không lẫn ngôn ngữ, không lỗi font dấu |
| **Trình duyệt** | Chrome, Edge, Firefox, Safari, Safari iOS, Chrome Android | Hoạt động như nhau |
| **Hiệu năng** | Tải trang, thời gian Save, mạng chậm | Trong ngưỡng đã thỏa thuận, không giật |

---

### 10. Bảo mật phía trình duyệt & dữ liệu cá nhân (PII)
| Nhóm | Case | Kỳ vọng |
| :--- | :--- | :--- |
| **URL** | Xem thanh địa chỉ, history, hash | Không chứa NRIC, SĐT, email, địa chỉ |
| **Storage** | F12 → Application: localStorage, sessionStorage, IndexedDB, cookie | Không lưu PII dạng rõ |
| **DOM** | Inspect: data-*, `<input type="hidden">`, HTML ẩn | Không chứa NRIC đầy đủ trước khi bấm Show NRIC |
| **Network** | Xem response trước khi bấm Show | NRIC vẫn che; PII không nằm trong query string |
| **Log** | Console, thông báo lỗi | Không in PII, không lộ stack trace |
| **Phân quyền** | Đổi ID người dùng trong URL/API (BOLA/IDOR) | 403/404, không xem/sửa được hồ sơ người khác |
| **Mass assignment** | Gửi thêm fullName, nric, residentialAddress qua API | Bị bỏ qua hoặc từ chối (dữ liệu Singpass bất biến) |
| **Chưa đăng nhập** | Vào thẳng /profile | Chuyển về đăng nhập |
| **Sau khi Log out** | Bấm Back của trình duyệt | Không xem lại được dữ liệu |
| **Phiên** | Token hết hạn, đăng nhập 2 nơi | Xử lý đúng |
| **Header & truyền tải** | HTTPS, Cache-Control: no-store cho dữ liệu hồ sơ, CSP, chống nhúng iframe | Có đủ |
| **CSRF / giới hạn tần suất** | Gửi Save lặp lại hàng loạt | Bị chặn hợp lý |
| **Payload lạ** | Sai kiểu dữ liệu, JSON hỏng, body 1MB | Báo lỗi sạch (4xx), không 500 |
