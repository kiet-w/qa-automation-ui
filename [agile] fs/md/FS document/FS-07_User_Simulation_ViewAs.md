# FS-07: User View Simulation / Impersonation (Requirement 7)

> **Phân hệ**: Admin Portal (MOE HQ Support Users)  
> **Requirement**: R7 – User View Simulation  
> **Product Backlog**: PB-22 (Post-MVP / Support) | **User Story**: US-08 (FR8)  
> **Trạng thái**: Specification Ready  

---

## 1. TỔNG QUAN (OVERVIEW)
Chức năng cho phép người dùng Trụ sở chính Bộ Giáo dục (MOE HQ Users / Helpdesk Officers) giả lập góc nhìn (View As) của Cán bộ Trường học (School User) hoặc Phụ huynh (Parent) nhằm hỗ trợ giải đáp thắc mắc, khắc phục sự cố và hỗ trợ kỹ thuật chính xác nhất.

---

## 2. QUY TRÌNH VẬN HÀNH GIẢ LẬP (SIMULATION WORKFLOW)

1. **Khởi tạo phiên giả lập (Initiate Simulation):**
   - Chuyên viên hỗ trợ MOE HQ chọn đối tượng cần giả lập:
     - Nhập `User ID` hoặc `Email` của School User, HOẶC
     - Nhập `Parent NRIC` của phụ huynh cần hỗ trợ.
   - Nhập lý do giả lập (Ticket ID, Helpdesk Request Number).
2. **Kích hoạt chế độ "View-As":**
   - Hệ thống tải giao diện chính xác theo phân quyền và dữ liệu của người dùng mục tiêu.
   - **Chế độ Chỉ xem tuyệt đối (Strict Read-Only Mode):** Vô hiệu hóa toàn bộ các nút thực thi (Thanh toán, Nộp đơn, Sửa thông tin, Xóa dữ liệu).
   - **Biểu ngữ nhận diện (Prominent Banner):** Luôn hiển thị thanh banner màu vàng/cam cố định ở đầu màn hình:
     > *"⚠️ BẠN ĐANG TRONG PHIÊN GIẢ LẬP VỚI TƯ CÁCH [TÊN NGƯỜI DÙNG]. MỌI THAO TÁC GHI ĐỀU BỊ KHÓA."*
3. **Kết thúc phiên & Ghi nhật ký an ninh (Audit & Termination):**
   - Bấm nút `Exit Simulation` để quay lại tài khoản HQ ban đầu.
   - Hệ thống tự động ghi nhật ký an ninh: `operator_id`, `target_user_id`, `session_start`, `session_end`, `pages_visited`, `ticket_reference`.
