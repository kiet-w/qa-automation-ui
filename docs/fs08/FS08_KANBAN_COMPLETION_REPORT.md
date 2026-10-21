# BÁO CÁO NGHIỆM THU KIỂM THỬ TỰ ĐỘNG & XÁC NHẬN HOÀN THÀNH KANBAN
## PHÂN HỆ FS08 / R8 — PARENT PORTAL (SINGPASS AUTH, ACCOUNT DASHBOARD & PROFILE)

> **Kính gửi**: Business Analyst (BA) / Product Owner (PO) / Project Manager  
> **Người thực hiện**: QA Automation & SDET Team  
> **Ngày lập báo cáo**: 21/10/2026  
> **Tiêu chuẩn áp dụng**: `/combo-qa` | `/combo-docs` | ISO/IEC/IEEE 29119-3 Compliant  
> **Các Thẻ Kanban Xác Nhận Hoàn Thành**:
> 1. `[DEV] [TSK-R8-03] Integrate Singpass Authentication & Parent-Student Authorization` (Assignee: Ryan, Nathan)
> 2. `[DEV] [TSK-R8-05] Build e-Service Portal UI: Account Dashboard & Profile Management` (Assignee: Ryan, Nathan)

---

## 🎯 1. KẾT LUẬN & KHUYẾN NGHỊ ĐIỀU HÀNH (EXECUTIVE VERDICT)

> ### 🟢 QUYẾT NGHỊ CHẤT LƯỢNG: **`GO` — XÁC NHẬN HOÀN THÀNH (MOVE TO DONE)**
> 
> Đội ngũ QA Automation đã hoàn tất chu kỳ kiểm thử tự động toàn diện (E2E Playwright, BVA Boundaries, Adversarial Chaos & Regression Testing) cho cả 2 hạng mục công việc `TSK-R8-03` và `TSK-R8-05`. 
> 
> * **Tỷ lệ Pass**: **100% (43/43 Automated Test Scenarios Passed)** trên môi trường SIT.
> * **Độ ổn định kỹ thuật**: 0 Uncaught JS Exceptions, 0 White Screen of Death (WSoD), 0 lỗi rò rỉ NRIC trên URL.
> * **Khuyến nghị cho BA**: **Đủ điều kiện chuyển cả 2 thẻ `TSK-R8-03` và `TSK-R8-05` sang cột `DONE` trên Kanban Board** để chuẩn bị bàn giao Sprint Review và Demo khách hàng MOE Singapore.

---

## 📊 2. TỔNG HỢP KẾT QUẢ KIỂM THỬ THEO 2 THẺ KANBAN

```text
 ┌──────────────────────────────────────────────┬──────────────────────────────────────────────┐
 │ [TSK-R8-03] SINGPASS & AUTHORIZATION         │ [TSK-R8-05] UI DASHBOARD & PROFILE           │
 ├──────────────────────────────────────────────┼──────────────────────────────────────────────┤
 │ • 17 Test Cases FSD (11 Automated Playwright)│ • 38 Test Cases FSD (24 Automated Playwright)│
 │ • Tỷ lệ Đạt: 100% (11/11 P0/P1 Passed)       │ • Tỷ lệ Đạt: 100% (24/24 P0/P1 Passed)       │
 │ • Chặn IDOR URL: Pass (MSG-0003)             │ • Sort thẻ con 3 tầng: Pass                  │
 │ • Hard Timeout 10s API (D-31): Pass (MSG-0809)│ • Form BVA Phone/Email: Pass (MSG-0805/0806) │
 │ • Dual Parent Equality (D-19): Pass          │ • SingPass Read-Only (D-20): Pass            │
 └──────────────────────────────────────────────┴──────────────────────────────────────────────┘
```

### Bảng Đối Soát Nghiệm Thu Chi Tiết

| Thẻ Kanban | Hạng Mục Nghiệp Vụ Cốt Lõi | Căn Cứ FSD & Quyết Định | Trạng Thái Test | Bằng Chứng / Assertion Xác Thực |
| :--- | :--- | :--- | :---: | :--- |
| **`TSK-R8-03`** | Đăng nhập SingPass lần đầu tạo tài khoản | FSD Mục 5.1; AC #1 | ✅ **PASSED** | Tạo `Parent_Profile`, gán `IsActivate = true`, mở Home hiển thị thẻ con (`TC-R8-002`). |
| **`TSK-R8-03`** | Tái đăng nhập dùng lại tài khoản | FSD Mục 5.1; AC #2 | ✅ **PASSED** | Tái sử dụng `UserId`, không sinh bản ghi trùng lặp trong cơ sở dữ liệu (`TC-R8-003`). |
| **`TSK-R8-03`** | Bấm Hủy hoặc lỗi SingPass Mock | FSD Mục 5.1; AC #5 | ✅ **PASSED** | Điều hướng an toàn về Login, hiển thị cảnh báo chuẩn `MSG-0802` (`TC-R8-004`, `005`). |
| **`TSK-R8-03`** | Phụ huynh không có con liên kết | FSD Mục 5.1; AC #3 | ✅ **PASSED** | Chặn vào Home, hiển thị thông báo lỗi `MSG-0801` (`TC-R8-007`). |
| **`TSK-R8-03`** | Quyền bình đẳng Cha và Mẹ | Quyết định `D-19` | ✅ **PASSED** | Cha và Mẹ đăng nhập độc lập đều thấy đầy đủ thông tin con cái chung (`TC-R8-012`). |
| **`TSK-R8-03`** | Chặn IDOR xem con người khác | FSD Mục 7; AC #13 | ✅ **PASSED** | Đổi URL `student=STU-UNAUTH` bị chặn với HTTP 403, báo lỗi `MSG-0003` (`TC-R8-013`). |
| **`TSK-R8-03`** | Timeout Gov API quá 10 giây | Quyết định `D-31`; AC #23 | ✅ **PASSED** | API phản hồi trễ > 10s tự động ngắt kết nối an toàn, báo `MSG-0809` (`TC-R8-023`). |
| **`TSK-R8-03`** | Hết hạn phiên sau 15 phút idle | Quyết định `D-22`; AC #20 | ✅ **PASSED** | Phiên idle quá 15 phút tự thu hồi token, điều hướng về login báo `MSG-0002` (`TC-R8-020`). |
| **`TSK-R8-05`** | Hiển thị thẻ con & số dư khả dụng | FSD Mục 6.1; AC #6 | ✅ **PASSED** | Thẻ Active hiển thị định dạng `SGD <amount>`, mã EA chuẩn `EA<number>` (`TC-R8-034`). |
| **`TSK-R8-05`** | Thuật toán sắp xếp thẻ con 3 tầng | FSD v0.4 Mục 6.1; AC #12 | ✅ **PASSED** | Active lên đầu $\rightarrow$ Lớn tuổi xếp trước $\rightarrow$ Con chưa FAS xếp trước có FAS (`TC-R8-037`). |
| **`TSK-R8-05`** | Xem trước công nợ tối đa 3 khoản | FSD Mục 6.1; AC #19 | ✅ **PASSED** | Hiển thị đúng 3 khoản gần hạn nhất kèm liên kết `+N more` (`TC-R8-043`). |
| **`TSK-R8-05`** | Con tròn 16 tuổi chuyển Read-only | FSD Mục 5.2; AC #7, #8 | ✅ **PASSED** | Nhãn `Due for closure`, ẩn nút thanh toán/FAS; con dưới 16t vẫn thao tác bình thường (`TC-R8-091`). |
| **`TSK-R8-05`** | Học sinh quốc tịch nước ngoài | FSD Mục 6.2; AC #10 | ✅ **PASSED** | Ẩn số dư EA, hiển thị câu chuẩn: *"Education Accounts are for Singapore Citizens"* (`TC-R8-010`). |
| **`TSK-R8-05`** | Bất biến định danh SingPass | Quyết định `D-20`; AC #18 | ✅ **PASSED** | Full Name, NRIC, Residential Address không có input; NRIC có nút ẩn/hiện (`TC-R8-094`). |
| **`TSK-R8-05`** | BVA Số điện thoại Singapore | FSD Bảng 119; AC #15 | ✅ **PASSED** | Chấp nhận đầu 6, 8, 9; từ chối đầu 7, 5, chữ cái báo lỗi inline `MSG-0805` (`TC-R8-099`). |
| **`TSK-R8-05`** | BVA Email RFC 5322 (Max 150) | FSD Bảng 119; AC #15 | ✅ **PASSED** | Email sai format báo `MSG-0806`; độ dài 150 ký tự lưu thành công (`TC-R8-101`). |
| **`TSK-R8-05`** | Vòng đời form Dirty state & Cancel | FSD Mục 5.3; AC #14 | ✅ **PASSED** | Nút Save chỉ enable khi sửa dữ liệu; bấm Cancel hoàn tác 100% dữ liệu gốc (`TC-R8-096`). |
| **`TSK-R8-05`** | Xác nhận lưu qua Confirm Dialog | FSD Mục 5.3; AC #14 | ✅ **PASSED** | Bấm Save mở alertdialog; xác nhận lưu hiển thị Toast xanh `MSG-0807` (`TC-R8-097`). |
| **`TSK-R8-05`** | Xử lý lỗi máy chủ Server 500 | FSD Mục 5.3; AC #17 | ✅ **PASSED** | Server trả HTTP 500 hiển thị thông báo `MSG-0808`, giữ nguyên dữ liệu trên form (`TC-R8-017`). |

---

## 🛡️ 3. KẾT QUẢ KIỂM ĐỊNH PHÁ HỆ THỐNG (ADVERSARIAL "BREAK-IT" & RESILIENCE)

Thực thi theo chuẩn **Invariant 8 ("Phá có kỷ luật")**: Toàn bộ **8 kịch bản phá đều ĐẠT (Passed)** — chứng minh hệ thống phòng thủ tốt:
1. **Gỡ ràng buộc Client (`TC-R8-BRK-001`)**: Xóa `novalidate`, `required`, ép email sai qua prototype setter $\rightarrow$ Server lớp 2 chặn đứng, không bị lưu bẩn.
2. **Can thiệp DOM SingPass (`TC-R8-BRK-002`)**: Sửa thẻ HTML họ tên $\rightarrow$ Backend loại bỏ trường read-only, bảo vệ danh tính gốc.
3. **Bơm XSS 3 Vectors (`TC-R8-BRK-003`)**: Bơm `<script>`, `<img>`, `<svg>` vào địa chỉ $\rightarrow$ Hệ thống mã hóa an toàn plain-text, 0 popup alert.
4. **Tràn bộ đệm 10.000 ký tự (`TC-R8-BRK-004`)**: Input tự động cắt ngắn an toàn, không làm crash trình duyệt.
5. **Double-click liên tục (`TC-R8-BRK-005`)**: Cơ chế Debounce kích hoạt ngay lập tức, chỉ có duy nhất 1 mutation request được dispatch.
6. **Mô phỏng sập máy chủ 500 (`TC-R8-BRK-006`)**: Giao diện không bị White Screen of Death (WSoD), hiển thị câu thông báo thân thiện `MSG-0808`.
7. **Leo thang đặc quyền (`TC-R8-BRK-007`)**: Phụ huynh gõ URL `/admin/fees` bị chặn và đẩy về trang thông báo phân quyền.
8. **Khả năng tiếp cận WCAG 2.1 (`TC-R8-BRK-008`)**: Modal không bị kẹt phím Tab (No Focus Trap); phím `Escape` đóng modal an toàn.

---

## 📋 4. BẢNG THEO DÕI HỒI QUY 5 LỖI SPRINT 1 (`DEFECT REGRESSION STATUS`)

Tất cả 5 lỗi trong Sprint 1 đã được cài đặt chốt chặn kiểm thử tự động (Automation Guards):

| Defect ID | Tóm Tắt Khiếm Khuyết | Mức Độ | Trạng Thái Kiểm Định | Chốt Chặn Automation Guard |
| :---: | :--- | :---: | :---: | :--- |
| **`BUG-R8-001`** | My details: Không hiện toast thành công sau khi lưu | S2 (High) | ✅ **VERIFIED** | `TC-R8-097`: Bắt buộc render Toast xanh chứa chính xác `MSG-0807`. |
| **`BUG-R8-002`** | My details: Chấp nhận lưu SĐT đầu 7, 5 | S2 (High) | ✅ **GUARDED** | `TC-R8-099`: Chặn submit nếu SĐT không bắt đầu bằng 6, 8, 9. |
| **`BUG-R8-003`** | My details: SĐT nhập có space lưu nguyên space | S4 (Low) | ✅ **GUARDED** | `TC-PROF-P09`: Hệ thống tự động trim khoảng trắng khi persist. |
| **`BUG-R8-004`** | My details: Báo lỗi email thiếu đoạn ví dụ `MSG-0806` | S4 (Low) | ✅ **GUARDED** | `TC-R8-101`: Chuỗi báo lỗi phải khớp 100% từng ký tự `MSG-0806`. |
| **`BUG-R8-005`** | My details: Không xóa trắng được ô bắt buộc (tự revert) | S2 (High) | ✅ **GUARDED** | `TC-PROF-P13`: Xóa trắng ô bắt buộc tự động disable nút Save hoặc hiện `MSG-0001`. |

---

## 📂 5. TÀI NGUYÊN KIỂM THỬ KÈM THEO BÁO CÁO

BA và các bên liên quan có thể truy cập trực tiếp các artifacts sau để đối soát:
1. **File Đặc Tả Chi Tiết 133 Test Cases**: [`docs/fs08/FS08_TEST_CASES.md`](file:///home/baudui/Projects/automation-ui/docs/fs08/FS08_TEST_CASES.md)
2. **File Ma Trận Excel Doanh Nghiệp 4 Tabs**: [`docs/fs08/FS08_TEST_CASES.xlsx`](file:///home/baudui/Projects/automation-ui/docs/fs08/FS08_TEST_CASES.xlsx)
3. **Báo Cáo HTML ExtentReports**: [`reports/fs08/execution_report.html`](file:///home/baudui/Projects/automation-ui/reports/fs08/execution_report.html)
4. **Mã Nguồn Test Pytest**: `tests/fs08/` (`test_ts01` đến `test_ts04`)

---

### 📝 HÀNH ĐỘNG ĐỀ XUẤT CHO BA TRÊN KANBAN:
1. Kéo thẻ **`[DEV] [TSK-R8-03]`** từ cột `In Review / Testing` sang cột **`DONE`**.
2. Kéo thẻ **`[DEV] [TSK-R8-05]`** từ cột `In Review / Testing` sang cột **`DONE`**.
3. Đính kèm liên kết file báo cáo này vào phần comment của 2 thẻ task để lưu vết kiểm toán (Audit Trail) cho Sprint Review.
