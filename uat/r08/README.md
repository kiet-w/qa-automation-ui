# R08 Parent Portal & Online FAS: Master UAT Execution Hub

> **Phân hệ**: `R08` / `FS08` (Parent Portal — SingPass, Education Account, Profile & Online FAS Submission)  
> **QA Lead Phụ Trách**: Howard  
> **Trạng thái thực thi**: Tài liệu legacy ghi nhận 222 TCs; trạng thái đó chưa chứng minh coverage đầy đủ cho toàn bộ UI/BSK hiện tại hoặc sign-off hiện hành. Thiết kế mới bắt đầu `Not Run`; xem [UI/BSK coverage matrix](../master/ui-bsk-coverage.md).  
> **Governing Invariant**: [`AGENTS.md`](../../AGENTS.md) (Invariant 10: Per-Module UAT Segregation & Single Master Evidence)

---

## 1. File Bằng Chứng & Báo Cáo Thống Nhất Duy Nhất (Unified Master Deliverables)

README legacy từng mô tả master evidence và dashboard. Các artifact thực thi (nếu có) được lưu dưới `reports/uat/r08/`; số lượng testcase hoặc trạng thái trong tài liệu cũ không thay thế việc kiểm tra run ID, build, evidence và coverage theo từng màn hình:

| Loại Tài Sản | Tên File Cốt Lõi | Đường Dẫn Truy Cập Trực Tiếp | Mô Tả & Tính Năng |
| :--- | :--- | :--- | :--- |
| 📊 **Excel Master Evidence** | `TEST_EXECUTION_EVIDENCE_R08_UAT_MASTER.xlsx` | [`reports/uat/r08/`](../../reports/uat/r08/) | Kiểm tra artifact thực tế tại thư mục báo cáo; README này không khẳng định artifact đang nằm cạnh file README hoặc trạng thái còn hiện hành. |
| 🌐 **Master HTML Dashboard** | `R08_UAT_MASTER_DASHBOARD.html` | [`reports/uat/r08/`](../../reports/uat/r08/) | Kiểm tra artifact thực tế và metadata run trước khi dùng làm bằng chứng sign-off. |

---

## 2. Bảng Thống Kê 5 UAT Sub-Modules Đã Hoàn Thành Của R8

| Mã Module UAT | Tên Kịch Bản Nghiệp Vụ | Số Lượng TCs (legacy) | Trạng Thái Được README Cũ Ghi Nhận | File Đặc Tả Chi Tiết Trong `testcases/` |
| :---: | :--- | :---: | :---: | :--- |
| **`UAT-005`** | **Parent SingPass Login & Verified Children** (Xác thực SingPass, bình đẳng Cha/Mẹ, chống IDOR) | **17 TCs** | README cũ ghi Passed; xác minh run/evidence trước khi dùng | [`testcases/fs08-parent-child-auth/`](./testcases/fs08-parent-child-auth/) |
| **`UAT-006`** | **Parent Balances, Enrolment & Filtered History** (Xem số dư EA, thông tin học tập, lọc sổ cái giao dịch) | **18 TCs** | README cũ ghi Passed; xác minh run/evidence trước khi dùng | [`testcases/fs08-parent-ea-overview/`](./testcases/fs08-parent-ea-overview/) |
| **`UAT-007`** | **Parent Contact Update** (Cập nhật nhanh Mobile & Email có hộp thoại xác nhận) | **10 TCs** | README cũ ghi Passed; xác minh run/evidence trước khi dùng | [`testcases/fs08-uat007-contact-update/`](./testcases/fs08-uat007-contact-update/) |
| **`UAT-Profile`** | **Parent Profile 12-Layer Validation Matrix** (Đi sâu 12 lớp validation form: NRIC, Mobile, Email, Mailing Address, Dialog) | **105 TCs** | README cũ ghi Passed; xác minh run/evidence trước khi dùng | [`testcases/fs08-parent-profile/`](./testcases/fs08-parent-profile/) |
| **`UAT-028`** | **Online FAS Application Submission** (Nộp đơn FAS trực tuyến, khai báo người thụ hưởng & thu nhập) | **66 TCs** | README cũ ghi Passed; xác minh run/evidence trước khi dùng | [`testcases/fs08-uat028-fas-submission/`](./testcases/fs08-uat028-fas-submission/) |
| **TỔNG CỘNG** | **Toàn bộ 5 Modules Phân Hệ R8** | **222 TCs được ghi trong README cũ** | Không xác nhận trạng thái hiện hành; chưa chứng minh full UI coverage | Đối chiếu [UI/BSK coverage matrix](../master/ui-bsk-coverage.md) và evidence tại `reports/uat/r08/` |

---

## 3. Vị Trí Lưu Trữ Báo Cáo Thực Thi Chi Tiết (Execution Reports)

- **Báo cáo UAT cấp doanh nghiệp**: [`reports/uat/r08/`](../../reports/uat/r08/)
- **Mã nguồn test tự động tương ứng**:
  - `tests/fs08/fs08-parent-child-auth/`
  - `tests/fs08/fs08-parent-ea-overview/`
  - `tests/fs08/fs08-uat007-contact-update/`
  - `tests/fs08/fs08-parent-profile/`
