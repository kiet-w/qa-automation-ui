# FS-10: FAS Family Unit Application & AI Auto-Fill (Requirement 10)

> **Phân hệ**: e-Service Portal (Parents / Legal Guardians)  
> **Requirement**: R10 – Financial Assistance Application  
> **Product Backlog**: PB-18, PB-24 (Sprint 3) | **User Story**: US-11, US-AI3  
> **Trạng thái**: Specification Ready  

---

## 1. TỔNG QUAN (OVERVIEW)
Chức năng trên Cổng Dịch vụ công (e-Service Portal) cho phép Phụ huynh nộp đơn xin trợ cấp tài chính (FAS) chung cho toàn bộ con cái trong gia đình theo một **Đơn vị Hộ gia đình (Family Unit)** duy nhất. Phụ huynh chỉ cần khai báo một lần thay vì phải làm đơn riêng lẻ cho từng học sinh. Hệ thống tích hợp Trợ lý Trí tuệ Nhân tạo (AI Auto-Fill) để tự động điền đơn từ hồ sơ có sẵn.

---

## 2. CÁC BƯỚC NỘI DUNG NỘP ĐƠN GIA ĐÌNH

1. **Bước 1: Chọn học sinh thụ hưởng (Select Children):**
   - Hệ thống liệt kê toàn bộ con em liên kết với tài khoản SingPass của phụ huynh.
   - Phụ huynh tích chọn các con cần đưa vào danh sách xin hỗ trợ trong năm học.
2. **Bước 2: Khai báo nhân khẩu & Thu nhập (Household & Income Declaration):**
   - Danh sách thành viên cùng chung sống trong gia đình.
   - Nhập thông tin việc làm và thu nhập hàng tháng của từng thành viên.
   - Đồng ý điều khoản cho phép hệ thống gọi API dữ liệu chính phủ để xác thực thu nhập (Consent for Income Verification API).
3. **Bước 3: Trợ lý AI tự động điền đơn (AI Form Auto-Fill - US-AI3):**
   - AI tự động trích xuất các thông tin từ hồ sơ cha mẹ (FS-08) và dữ liệu thu thập qua các phiên hỏi đáp trước đó.
   - Tự động điền các trường biểu mẫu, giảm thiểu 80% thời gian gõ phím của phụ huynh.
4. **Bước 4: Rà soát & Xác nhận (Review & Submit):**
   - Phụ huynh kiểm tra lại thông tin, chỉnh sửa nếu có sai sót và bấm `Xác nhận & Nộp đơn`.
   - Hệ thống phát sinh mã hồ sơ duy nhất `FAS-YYYY-XXXXX`.
5. **Bước 5: Theo dõi kết quả trực tuyến (Track Outcome):**
   - Trạng thái xử lý (`SUBMITTED` -> `UNDER_ASSESSMENT` -> `APPROVED` / `REJECTED`) hiển thị thời gian thực trên Cổng Phụ huynh.
   - Khi được duyệt, huy hiệu FAS Granted tự động hiển thị trên Dashboard học sinh (FS-08).
