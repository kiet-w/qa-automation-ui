# EAFAMS Enterprise UAT Hub (Trung Tâm Điều Phối UAT Theo Phân Hệ)

> **Governing Constitution**: [`AGENTS.md`](../AGENTS.md) (Invariant 10: Per-Module UAT Segregation & Unified Master Report)  
> **Master UAT Specifications**: [`master/uat-plan.md`](master/uat-plan.md) • [`master/uat-workbook.xlsx`](master/uat-workbook.xlsx) • [UI/BSK screen coverage supplement](master/ui-bsk-coverage.md)

The master plan covers business journeys; `master/ui-bsk-coverage.md` maps all 26 captured UI/BSK screen groups to UAT scenario families and identifies missing business oracles as `SPEC GAP`. BSK describes observed UI structure and is not authority for business rules. These documents are test design, not proof of execution or sign-off.

---

## 1. Cấu Trúc Phân Tầng UAT Theo Phân Hệ Nghiệp Vụ (R-Segregated)

Để tránh tình trạng tài liệu và báo cáo UAT bị lưu phân tán, trôi nổi ngoài thư mục gốc hoặc đặt tên có khoảng trắng, toàn bộ hoạt động kiểm thử chấp nhận người dùng (UAT) được phân bổ nghiêm ngặt vào các thư mục con tương ứng với từng phân hệ:

| Thư Mục Phân Hệ | Tên Nghiệp Vụ Chính Thức | QA Lead Phụ Trách | Trạng Thái Hoàn Thiện | Tài Sản Cốt Lõi Đi Kèm |
| :---: | :--- | :---: | :---: | :--- |
| [`uat/r01/`](./r01/) | **Education Account Lifecycle** (Khởi tạo, đóng tài khoản & quyết toán CPF) | Josh | 🟡 Đang hoàn thiện | Kế hoạch UAT-001 đến UAT-004 |
| [`uat/r02/`](./r02/) | **Top-Up Management** (Nạp tiền đơn lẻ & chiến dịch bulk) | Josh | 🟡 Sẵn sàng kịch bản mẫu | [`uat-sample-f2.md`](./r02/uat-sample-f2.md), [`uat-sample-f2.xlsx`](./r02/uat-sample-f2.xlsx) |
| [`uat/r03/`](./r03/) | **School Admin & Fee Management** (Trường, nhân sự & biểu phí) | Kent & Chan | 🟡 Đang hoàn thiện | [`diagram_kent_workflow.html`](./r03/diagram_kent_workflow.html) |
| [`uat/r08/`](./r08/) | **Parent Portal & Online FAS** (Singpass, Profile, EA & Nộp đơn FAS) | Howard | ⚪ Legacy README records 222 TCs; current full UI coverage/sign-off is not established here | [`README.md`](./r08/README.md); execution artifacts are under [`reports/uat/r08/`](../reports/uat/r08/) |
| [`uat/r09/`](./r09/) | **Outstanding Fees & Payment** (Công nợ & Thanh toán) | Gavin | 🟡 Đang hoàn thiện | Kịch bản UAT-009 đến UAT-012 |
| [`uat/r10/`](./r10/) | **Family FAS Application Portal** (Nộp đơn gia đình nhiều con) | Phối hợp | 🟡 Đang hoàn thiện | Kịch bản UAT-049 |
| [`uat/master/`](./master/) | **Master Coordination Pack** (Kế hoạch tổng thể và ma trận truy vết) | Josh | 📋 Master Plan | [`uat-plan.md`](./master/uat-plan.md), [`uat-workbook.xlsx`](./master/uat-workbook.xlsx) |

---

## 2. Invariant 10: Quy Chuẩn Bắt Buộc Khi Làm Việc Với UAT

1. **Phân Tầng Tuyệt Đối**: UAT scenarios/plans belong in `uat/r<xx>/`; generated execution reports and evidence belong in `reports/uat/r<xx>/`.
2. **Cấm Dấu Cách**: Tuyệt đối không đặt tên folder có khoảng trắng (ví dụ `uat r8`, `r08 uat`). Bắt buộc dùng `kebab-case` hoặc `r08`.
3. **Một File Thống Nhất (Single Master Evidence)**: Khi một phân hệ chạy xong, gom kết quả vào **1 Excel Master (1 tab, 20 cột gồm `Steps Test`)** và dashboard trong `reports/uat/r<xx>/`; thư mục `uat/r<xx>/` giữ kịch bản/đặc tả UAT.
