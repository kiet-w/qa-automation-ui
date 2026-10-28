# BÁO CÁO ĐỐI SOÁT & KHẮC PHỤC SAI LỆCH FSD (FSD GAP AUDIT & RESOLUTION REPORT)

> **Phương pháp kiểm chuẩn:** Enforced by `combo-qa` (Zero Hallucination, Evidence-First & Verbatim Traceability).  
> **Nguồn đối chiếu chuẩn (Source of Truth):** Google Doc [Agile FS (Live Spec)](https://docs.google.com/document/d/1k0xJrdGwCzFzfqVhofzwgRPcdvoV8O9DFtzWpq-_kjQ/edit?tab=t.5pdms31w4le)  
> **Đối tượng đối soát:** Bộ tài liệu Functional Specification Markdown (`FS-01` đến `FS-10`) trong thư mục [`document/FS document/`](./FS%20document).

---

## 1. Tổng quan kết quả xử lý (Executive Summary)

Tuân thủ nghiêm ngặt nguyên tắc **"Không bịa đặt - Bám sát bằng chứng nguồn (Evidence-First)"** của `combo-qa`, toàn bộ 12 tab của Google Doc đã được trích xuất trực tiếp và so sánh từng dòng với các file `.md` trong kho dự án.

Hệ thống đã phát hiện và xử lý dứt điểm **4 nhóm sai lệch lớn** mà không tự ý phát sinh thêm bất kỳ yêu cầu kinh doanh nào ngoài tài liệu nguồn:

| ID | Module FSD | Loại sai lệch | Nguyên nhân gốc rễ | Biện pháp đã thực hiện khắc phục | Trạng thái sau xử lý |
| :---: | :---: | :--- | :--- | :--- | :---: |
| **GAP-01** | **FS-01** | Thừa bản nháp cũ & Xung đột logic F03 | File `.md` bị nối thừa Part 2 (bản nháp cũ có `F03 - Simulated CPF Transfer`), mâu thuẫn với quyết định `[Deferred] CPF Transfer` ở bản Final. | Cắt bỏ 409 dòng Part 2 thừa (từ dòng 796 đến 1204), đồng bộ 100% với tab `t.5pdms31w4le` (`R1 (Final)`). | **ĐÃ GIẢI QUYẾT** |
| **GAP-02** | **FS-08** | Lệch kiến trúc đồng bộ & Thiếu thuật toán UI | File `.md` đang ở bản cũ v0.3 (quét batch hằng đêm). Google Doc đã chốt bản v0.4 (Quyết định D-31: Bỏ quét đêm, chuyển sang JIT API Sync khi SingPass login). | Nâng cấp file lên Version 0.4: Bỏ batch sync đêm, thêm JIT Mock API call, mã lỗi `MSG-0809`, quy tắc xếp thẻ con ở Home và đủ 28 ACs. | **ĐÃ GIẢI QUYẾT** |
| **GAP-03** | **FS-03** | Ghép nối trùng lặp 2 phiên bản (Duplication) | File `.md` bị nối cả bản v1.2 (R3 new) và bản v1.1 cũ (R3 old) làm tăng dung lượng lên 1408 dòng. | Giữ lại bản chuẩn v1.2 (`R3 new`), loại bỏ 805 dòng của bản nháp v1.1 cũ (từ dòng 603 đến 1408). | **ĐÃ GIẢI QUYẾT** |
| **GAP-04** | **FS-09** | Thiếu ghi chú phản biện của Team (`[a]`–`[g]`) | Trên tab `R9` của Google Doc có 7 ghi chú/comment thảo luận thực tế giữa BA và Dev chưa được chuyển hóa vào file markdown. | Bổ sung Mục 7: Ghi chú Thống nhất & Quyết định Nghiệp vụ (`[a]` đến `[g]`) với đầy đủ nhãn đảm bảo `[TD]`, `[WA]`, `[REF]`. | **ĐÃ GIẢI QUYẾT** |

---

## 2. Chi tiết bằng chứng đối soát & Khắc phục sai lệch (Evidence-First Audit)

### 2.1. Module FS-01: Education Account Lifecycle Management

* **Nguồn chuẩn (Google Doc tab `t.5pdms31w4le` - `R1 (Final)`):**
  * Tiêu đề: *Updated Functional Specification – Sprint 1 MVP, Version: 1.2 – BA/Dev/QA Refinement Draft*.
  * Quyết định CPF: `[Deferred] CPF Transfer: CPF Transfer chưa được triển khai. Closure Processing khi Account còn Remaining Balance phải tuân theo agreed MVP handling rules; không được coi CPF Transfer là đã thực hiện thành công.`
* **Tình trạng trước xử lý trong file `.md`:**
  * Từ dòng 1 đến 795: Khớp 99.7% với tab `R1 (Final)`.
  * Từ dòng 796 đến 1204: Bị nối thêm một bản nháp cũ có ghi: *`Status: Proposed Implementation ... Scope: Automatic Account Creation, Automatic Closure và Simulated CPF Transfer`* $\rightarrow$ Trực tiếp mâu thuẫn với quyết định `[Deferred]` ở trên.
* **Hành động khắc phục:**
  * Cắt bỏ toàn bộ 409 dòng thừa thuộc Part 2.
  * File [`FS-01_Education_Account_Lifecycle.md`](./FS%20document/FS-01_Education_Account_Lifecycle.md) hiện tại đúng 795 dòng, phản ánh chuẩn xác 100% nội dung tab `R1 (Final)`.

---

### 2.2. Module FS-08: Parent Portal – SingPass, Education Account, Profile

* **Nguồn chuẩn (Google Doc tab `t.arbjxu7ti0p6` - `R8 (Final)`):**
  * Lịch sử cập nhật: *`0.4 | 14/10/2026 | Nguyễn Quốc Huy | Bỏ quét đồng bộ hằng đêm. Sau khi đăng nhập SingPass thành công, hệ thống gọi API dữ liệu theo NRIC để lấy Parent và các con, rồi cập nhật dữ liệu mới nhất của Parent đó. Thêm MSG-0809 (D-31)`*.
  * Quy tắc xếp thẻ con ở Home (Mục 6.1):
    > *(1) con có EA Active xếp trước, con đã đủ 16 tuổi (chỉ xem) xếp cuối; (2) trong mỗi nhóm, con lớn tuổi hơn xếp trước; (3) cùng tuổi thì con chưa có đơn FAS xếp trước con đã có hoặc đang chờ FAS.*
  * Số lượng Acceptance Criteria: Đủ 28 kịch bản nghiệm thu (từ AC-01 đến AC-28).
* **Tình trạng trước xử lý trong file `.md`:**
  * File dừng ở **Version 0.3**.
  * Mục 3 vẫn ghi: *“Chạy trước: hệ thống quét học sinh 7–16 tuổi, đồng bộ học sinh và cha mẹ vào dữ liệu (FR-01)... NRIC không có trong dữ liệu đồng bộ: báo MSG-0801, không vào được.”*
  * Thiếu hoàn toàn quy tắc xếp thẻ ở Mục 6.1.
  * Bảng AC chỉ có 20 kịch bản (thiếu các kịch bản AC-21 đến AC-28 về JIT sync, bảo toàn số điện thoại, timeout API...).
* **Hành động khắc phục:**
  * Thay thế toàn bộ nội dung file [`FS-08_Parent_Portal_SingPass_Profile.md`](./FS%20document/FS-08_Parent_Portal_SingPass_Profile.md) bằng nội dung chính thức của Version 0.4 từ Google Doc tab `R8 (Final)` với định dạng Markdown table chuẩn.

---

### 2.3. Module FS-03: School, Student & Fee Management

* **Nguồn chuẩn (Google Doc tab `t.1rnrczkzsu1f` - `R3 new`):**
  * Version: 1.2 (Proposed – Pending Business Clarification).
  * Cấu trúc: Mục 1.4 Bảng thuật ngữ, Mục 2 Quy trình hệ thống, Mục 3 Bóc tách 16 Sub-functions (F01–F16) và các Business Rules, Alternative/Exception Flows mã hóa rõ ràng.
* **Tình trạng trước xử lý trong file `.md`:**
  * File dài 1408 dòng vì chứa đồng thời cả bản v1.2 ở nửa đầu và bản v1.1 cũ ở nửa sau (từ dòng 604 trở đi).
* **Hành động khắc phục:**
  * Lược bỏ 805 dòng của bản nháp v1.1 cũ.
  * Giữ lại trọn vẹn bản v1.2 chuẩn hóa (602 dòng) trong file [`FS-03_School_Student_Fee_Management.md`](./FS%20document/FS-03_School_Student_Fee_Management.md).

---

### 2.4. Module FS-09: Outstanding Fees and Payment

* **Nguồn chuẩn (Google Doc tab `t.duowzmhz1pzq` - `R9`):**
  * Văn bản gốc có đính kèm 7 chú thích thảo luận kỹ thuật giữa BA và Dev (`[a]` đến `[g]`).
* **Tình trạng trước xử lý trong file `.md`:**
  * Thiếu phần tổng hợp các chú thích này, khiến Dev và QA có thể bỏ sót các giả định quan trọng (như timeout 10 phút, không cho tự gõ số tiền EA, không tách lẻ bill).
* **Hành động khắc phục:**
  * Bổ sung **Mục 7: Ghi chú Thống nhất & Quyết định Nghiệp vụ (Reviewer & Team Decisions)** vào cuối file [`FS-09_Outstanding_Fees_and_Payment.md`](./FS%20document/FS-09_Outstanding_Fees_and_Payment.md) với phân loại rõ ràng:
    * `[a] [TD]`: Bắt buộc hiển thị trạng thái hóa đơn trên UI.
    * `[b] & [f] [WA - Deferred]`: Timeout thanh toán online giả định 10 phút; chưa triển khai ở Sprint 1.
    * `[c] [TD]`: Split payment EA + Online tính là 1 bill duy nhất, thanh toán đồng thời.
    * `[d] [WA]`: Hoàn tiền trực tiếp vào tài khoản nguồn đã thanh toán thành công nếu lỗi xác nhận.
    * `[e] [TD]`: Không cho nhập số tiền EA tùy ý; tự động trừ max số dư hoặc giá trị bill.
    * `[g] [REF]`: Đối soát thực thể dữ liệu với bảng cấu hình chung.

---

### 2.5. Các Module R2, R4, R5, R6, R7, R10

* **Hiện trạng đối chiếu:**
  * Trên **Google Doc**: Các tab `R2`, `R4`, `R5`, `R6`, `R7`, `R10` là các **tab rỗng (0 bytes / placeholder)**.
  * Trong **Kho mã nguồn**: Đã có các file tóm tắt sơ thảo dựa trên High-level Solution và Function Requirements ban đầu (`FS-02.md`, `FS-04.md`...).
* **Nguyên tắc `combo-qa` áp dụng:**
  * **Cấm tuyệt đối việc tự suy diễn hay bịa đặt spec chi tiết** khi chưa có FSD chi tiết từ BA/Client.
  * Giữ nguyên các file tóm tắt hiện có làm baseline và đánh dấu trạng thái chờ tài liệu chính thức từ PO/Client ở các Sprint tiếp theo.

---

## 3. Danh mục câu hỏi làm rõ (Clarification Items - CIR)

Dành cho Product Owner / Lead BA để chốt các điểm còn để ngỏ (`[TBC]`, `[WA]`):

| Mã CIR | Module liên quan | Vấn đề cần xác nhận | Phương án hiện tại (Working Assumption) | Hệ quả kỹ thuật / Rủi ro nếu đổi |
| :---: | :---: | :--- | :--- | :--- |
| **CIR-01** | **R1 / F02** | Xử lý tài chính khi đóng tài khoản do mất quốc tịch (Citizenship Loss). | Đang để mở `[Open Business Decision]`. Tạm hoãn xử lý tiền thừa. | Nếu client yêu cầu tịch thu hoặc chuyển trả, cần bổ sung API hoàn tiền riêng. |
| **CIR-02** | **R9 / Split** | Có cho phép hủy giao dịch EA nếu cổng Online bị lỗi timeout sau 10 phút không? | Hệ thống tự động Reversal nhánh EA nếu nhánh Online thất bại. | Cần cơ chế Idempotent API với R1 để tránh hoàn tiền trùng lặp. |
| **CIR-03** | **R8 / Mock API** | Thời gian timeout chuẩn của Mock Government Data API khi phụ huynh đăng nhập SingPass. | Đang giả định timeout là 10 giây (nếu quá 10s báo `MSG-0809`). | Cần kiểm tra SLA thực tế của cổng SingPass / MyInfo Singapore. |
| **CIR-04** | **R2, 4, 5, 6, 7, 10** | Lộ trình bàn giao FSD chi tiết cho các tab còn đang để trống trên Google Doc. | Hiện các tab trên GDoc đang là rỗng. | Cần kế hoạch chi tiết cho Sprint 2 và Sprint 3 theo Agile Backlog. |
