# Đối chiếu testcase 04 với UI đang chạy

Quan sát trực tiếp tại `http://localhost:5173/school-user-management` và chạy
Playwright với dữ liệu API cô lập trong `tests/testcase5173/04_school_user_management/conftest.py`.

| Case | Kết luận hiện tại | Oracle automation |
| --- | --- | --- |
| TC-USR-002 | Màn chi tiết có trạng thái chưa gán và nút Assign school; không thấy Unassign. | Kiểm tra thông báo chưa gán và combobox. Luồng Unassign cần quyết định sản phẩm. |
| TC-USR-004 | Danh sách School Users có Deactivate/Activate, không có Delete. Tài khoản MOEHQ hiện không nằm trong danh sách này. | Kiểm tra không có Delete trên bảng; không thể kiểm chứng self-delete riêng. |
| TC-USR-008 | Nút Get Template tải `school-users-template.xlsx`. | Kiểm tra download và tên file quan sát được. |
| TC-USR-009 | Với NRIC sai, UI hiện thông báo chung `Validation failed`; không gắn `aria-invalid` riêng vào ô NRIC. | Kiểm tra thông báo nhìn thấy, vẫn ở form và không có thẻ tạo thành công. Phản hồi 400 do fixture cô lập cung cấp. |
| TC-USR-011 | Lỗi thiếu header được mô phỏng theo đặc tả thành phần. | Kiểm tra alert hiển thị đúng cột thiếu. |
| TC-USR-012 | Quy tắc được đặc tả là tối đa 1.000 dòng, không phải 5 MB. | Tệp 1.001 dòng nhận lỗi giới hạn dòng. |
| TC-USR-014 | Sau Import có bảng Import result; không thấy bước Preview trước Import. | Kiểm tra ba hàng thành công trong bảng kết quả. |
| TC-USR-017 | Kết quả partial success có hàng lỗi và lý do. | Kiểm tra số hàng, lý do lỗi; phản hồi API được cô lập. |
| TC-USR-018 | Nút Deactivate mở hộp thoại, nút Close hủy. | Đóng hộp thoại và kiểm tra tài khoản vẫn Active. |

Các ca CSV xác nhận cách **UI trình bày phản hồi từ API giả lập**. Chúng không
chứng minh backend thực tế tự kiểm tra header, số dòng hay từng NRIC.
Tài liệu ma trận và workbook cũ vẫn mô tả Delete, Preview và giới hạn 5 MB;
cần BA/Product Owner chốt thay đổi nghiệp vụ trước khi cập nhật chúng.
