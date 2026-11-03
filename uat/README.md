# Sprint 3 UAT — Kế Hoạch & Ma Trận Kiểm Thử Nghiệm Thu Người Dùng (UAT Master)

> **Nguồn dữ liệu:** Đồng bộ trực tiếp từ Google Spreadsheet chính thức Sprint 3 UAT: essential test plan.
> **Tổng số kịch bản:** 61 kịch bản kiểm thử bao phủ toàn bộ 10 phân hệ nghiệp vụ Sprint 1, Sprint 2 và các tính năng mở rộng.

## 1. Bảng Chỉ Số Tổng Quan (Executive Summary)

- 🟢 **Đạt (Pass):** 15 ca
- 🔴 **Không Đạt (Fail):** 6 ca
- 🟡 **Đang Thực Hiện (In Progress):** 5 ca
- 🚫 **Bị Chặn (Blocked):** 2 ca
- ⚪ **Chưa Chạy (Not Run):** 33 ca
- 📊 **Tổng Cộng:** **61** test cases

## 2. Phân Bổ Theo 10 Phân Hệ Nghiệp Vụ (10 UAT Areas)

| STT | Phân Hệ Nghiệp Vụ (Area) | Tên Tiếng Việt | Số Ca | Thư Mục Chi Tiết |
| :---: | :--- | :--- | :---: | :--- |
| 1 | `EA lifecycle` | Vòng Đời Tài Khoản Giáo Dục (Education Account) | **4** | [`modules/01_ea_lifecycle`](modules/01_ea_lifecycle/README.md) |
| 2 | `Parent access and results` | Cổng Phụ Huynh & Tra Cứu Kết Quả | **4** | [`modules/02_parent_access_and_results`](modules/02_parent_access_and_results/README.md) |
| 3 | `School setup` | Thiết Lập Dữ Liệu Trường & Học Sinh | **6** | [`modules/03_school_setup`](modules/03_school_setup/README.md) |
| 4 | `Fees and payments` | Học Phí, Biểu Phí & Thanh Toán | **9** | [`modules/04_fees_and_payments`](modules/04_fees_and_payments/README.md) |
| 5 | `Top-up` | Nạp Tiền Vào Tài Khoản Giáo Dục (Top-Up) | **6** | [`modules/05_top_up`](modules/05_top_up/README.md) |
| 6 | `FAS submission` | Nộp Hồ Sơ Trợ Cấp Tài Chính (FAS Submission) | **8** | [`modules/06_fas_submission`](modules/06_fas_submission/README.md) |
| 7 | `FAS assessment` | Đánh Giá & Phê Duyệt Hồ Sơ Trợ Cấp (FAS Assessment) | **9** | [`modules/07_fas_assessment`](modules/07_fas_assessment/README.md) |
| 8 | `Budget and statistics` | Ngân Sách & Thống Kê MOE / Trường | **8** | [`modules/08_budget_and_statistics`](modules/08_budget_and_statistics/README.md) |
| 9 | `Access and help` | Quyền Truy Cập, View As & Trợ Giúp FAQ | **5** | [`modules/09_access_and_help`](modules/09_access_and_help/README.md) |
| 10 | `End-to-end` | Hành Trình Nghiệp Vụ Xuyên Suốt (End-to-End Journeys) | **2** | [`modules/10_end_to_end`](modules/10_end_to_end/README.md) |

## 3. Phân Công Trách Nhiệm Nhân Sự (Team Allocation)

| Thành Viên | Số Ca Phụ Trách | Phân Hệ Chính | Reviewer |
| :--- | :---: | :--- | :--- |
| **Josh** | **18** ca | EA lifecycle, top-up, integrated journeys, business decisions and final readiness report, budgets and statistics | **Gavin** |
| **Kent** | **11** ca | Fees and charges, school SBFAS schemes, subsidies, school review | **Chan** |
| **Chan** | **15** ca | Environment, roles, data and reset, school and enrolment, CSV, paper FAS, View As | **Kent** |
| **Howard** | **10** ca | Parent access and profile, online FAS, FAQ, evidence format | **Gavin** |
| **Gavin** | **7** ca | Payments and receipts, FAS assessment, subsidies | **Howard** |

## 4. Mục Lục Tài Liệu Cấu Thành Bộ UAT

- 📑 **[MASTER_UAT_SPRINT_3.xlsx](MASTER_UAT_SPRINT_3.xlsx)**: File Excel gốc nguyên bản tải từ Google Spreadsheet
- 📋 **[TESTS.md](TESTS.md)**: Danh sách đầy đủ 61 test cases 10 cột
- ⏱️ **[TIMELINE.md](TIMELINE.md)**: Kế hoạch mốc thời gian thực thi nội bộ & bàn giao khách hàng
- 🚪 **[GATES.md](GATES.md)**: 4 Cổng kiểm soát (G1-G4) & các giả định kỹ thuật D05-D09
- 💾 **[TEST_DATA.md](TEST_DATA.md)**: 12 bộ dữ liệu test (DATA-ROLES, DATA-LIFE, DATA-CSV, v.v.)
- ✅ **[READINESS.md](READINESS.md)**: 10 điều kiện sẵn sàng vào UAT (READY-01..10) và 3 điều kiện nghiệm thu (EXIT-01..03)
- 👥 **[TEAM.md](TEAM.md)**: Bảng phân công vai trò và người review chéo
- 📦 **[json/](json/)**: Dữ liệu JSON chuẩn hóa cho hệ thống script và máy đọc

