# FS-05: Hardcopy FAS Applications Processing (Requirement 5)

> **Phân hệ**: Admin Portal (School Users)  
> **Requirement**: R5 – Hardcopy Application Processing  
> **Product Backlog**: PB-20 (Sprint 3) | **User Story**: US-06 (FR6)  
> **Trạng thái**: Specification Ready  

---

## 1. TỔNG QUAN (OVERVIEW)
Chức năng dành cho cán bộ nhà trường (School Users) nhằm tiếp nhận, nhập liệu và xử lý các đơn xin trợ cấp tài chính (FAS) bản giấy do phụ huynh nộp trực tiếp tại trường học. Chức năng này hỗ trợ những phụ huynh không thể truy cập e-Service Portal hoặc gặp khó khăn về thiết bị kỹ thuật số.

---

## 2. QUY TRÌNH XỬ LÝ ĐƠN GIẤY OFFLINE

1. **Tiếp nhận & Thu thập đơn giấy:** Phụ huynh điền mẫu đơn FAS theo mẫu của Bộ và nộp tại phòng văn thư nhà trường kèm giấy tờ tùy thân.
2. **Nhập dữ liệu vào Admin Portal:**
   - Cán bộ trường đăng nhập Admin Portal, chọn chức năng `New Hardcopy FAS Application`.
   - Nhập thông tin cha mẹ (Father NRIC, Mother NRIC), thông tin học sinh và thông tin nhân khẩu hộ gia đình.
   - Tải lên bản quét điện tử (PDF/JPG Scan Attachment) của hồ sơ gốc.
3. **Kiểm tra trùng lặp tự động (Deduplication Check):**
   - Hệ thống quét cơ sở dữ liệu dựa trên NRIC của học sinh và cha mẹ.
   - Nếu phát hiện gia đình đã có đơn nộp trực tuyến (Online FAS) đang chờ xử lý hoặc đã duyệt, hệ thống phát cảnh báo `DUPLICATE_APPLICATION_DETECTED` và chặn tạo đơn trùng lặp.
4. **Đưa vào quy trình thẩm định tập trung (Unified Assessment Flow):**
   - Đơn giấy sau khi nhập thành công sẽ được gán thuộc tính `submission_channel = 'PAPER'`.
   - Chuyển vào luồng xử lý tự động của FS-04 (kiểm tra điều kiện MOEFAS, gọi AI scoring, xét duyệt SBFAS).

---

## 3. RÀNG BUỘC NGHIỆP VỤ (BUSINESS RULES)
- **BR-R5-01 (Mandatory Attachment):** Đơn nhập giấy bắt buộc phải có ít nhất 1 tệp đính kèm bản scan hợp lệ.
- **BR-R5-02 (Anti-Duplication):** Mỗi học sinh chỉ được có 1 hồ sơ FAS đang mở (Pending/Draft) trong cùng một năm học.
- **BR-R5-03 (Equal Treatment):** Hồ sơ nộp giấy có giá trị pháp lý và quy tắc tính trợ cấp hoàn toàn tương đương với hồ sơ nộp trực tuyến.
