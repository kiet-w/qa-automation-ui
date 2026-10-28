# TỔNG QUAN THƯ MỤC TÀI LIỆU DỰ ÁN (PROJECT DOCUMENTATION CATALOG)

> **Dự án**: MOE Education Account & Fee Management System (Agile Project)  
> **Nguồn gốc**: Trích xuất và đồng bộ từ Google Drive (`1wry8P-LjWUMaXIg70qa4spuGU4VJc42a`)  
> **Thư mục lưu trữ**: `/home/baudui/Projects/fs/document/`  
> **Cập nhật ngày**: 19/10/2026 (Đồng bộ toàn diện Google Drive)  
> **Định dạng lưu trữ**: **100% Markdown (.md)** phục vụ quản lý mã nguồn, tìm kiếm toàn văn và theo dõi biến động trên GitHub.

---

## 1. HƯỚNG DẪN CẬP NHẬT TÀI LIỆU (MAINTENANCE WORKFLOW)

> [!TIP]
> **Quy tắc cập nhật phân tán theo Module:**  
> Hệ thống tài liệu đã được chuẩn hóa thành các tệp Markdown độc lập từ **FS-01 đến FS-10**.
> - **Khi có cập nhật nghiệp vụ:** Đội ngũ BA / Dev / QA **chỉ cần chỉnh sửa trực tiếp vào file `FS-XX_<Name>.md` tương ứng**.
> - Không sửa đổi tập trung trên một tệp duy nhất nhằm tránh xung đột code/tài liệu (merge conflicts).

---

## 2. MA TRẬN PHÂN RÃ ĐẶC TẢ CHỨC NĂNG (MODULAR FS MATRIX: R1 – R10)

| Mã FS | Yêu Cầu (Tender) | Tên Phân Hệ & Chức Năng | Tác Tử Chính (Actor) | Phân Hệ (Portal) | Phân Bổ Sprint | Tài Liệu Markdown (.md) | Trạng Thái Baseline |
| :---: | :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **FS-01** | **R1** | **Vòng đời Tài khoản Giáo dục (Lifecycle & Closure)**<br>Tự động tạo & kích hoạt lúc 7 tuổi, tất toán chuyển sang CPF lúc 16 tuổi. | System / Batch | Admin Portal | **Sprint 1** | [FS-01.md](FS%20document/FS-01_Education_Account_Lifecycle.md) | Official Baseline v1.2 |
| **FS-02** | **R2** | **Nạp tiền Tài khoản (Top-Up Management)**<br>Nạp theo lô (Bulk Campaign, Preview & Launch); Nạp lẻ cá nhân; Bút toán hiệu chỉnh. | MOE HQ | Admin Portal | **Sprint 2** | [FS-02.md](FS%20document/FS-02_Education_Account_TopUp.md) | Official FSD Baseline (691 dòng, 24 tables) |
| **FS-03** | **R3** | **Quản lý Trường học, Học sinh & Cấu hình Phí**<br>Quản lý School, Class, Student, Enrolment, Fee Component, Rate Rules & Generation. | MOE HQ, School User | Admin Portal | **Sprint 1** (Enrolment)<br>**Sprint 2** (Fees) | [FS-03.md](FS%20document/FS-03_School_Student_Fee_Management.md) | Official Baseline v1.2 |
| **FS-04** | **R4** | **Trợ cấp Tài chính (FAS) & AI Scoring Engine**<br>Review Drawer, MOE HQ vs School Admin view, Need Score 0-100, Risk Tiers, Suggested Tiers. | School User, MOE HQ | Admin Portal | **Sprint 3** | [FS-04.md](FS%20document/FS-04_Financial_Assistance_Scheme_FAS.md) | Official FSD Baseline (v1.1 @Huy) |
| **FS-05** | **R5** | **Xử lý Đơn giấy Ngoại tuyến (Hardcopy FAS)**<br>Nhập đơn giấy thay phụ huynh, đính kèm bản quét scan, tự động kiểm tra trùng đơn trực tuyến. | School User | Admin Portal | **Sprint 3** | [FS-05.md](FS%20document/FS-05_Hardcopy_Applications_Offline.md) | Specification Ready |
| **FS-06** | **R6** | **Quản lý Ngân sách & Thống kê Trợ cấp**<br>Quản lý ngân sách MOEFAS & SBFAS, thống kê trợ cấp, theo dõi giải ngân & cảnh báo vượt ngưỡng. | MOE HQ, School User | Admin Portal | **Sprint 3** | [FS-06.md](FS%20document/FS-06_FAS_Budget_and_Statistics.md) | Official FSD Baseline (738 dòng, 20 tables) |
| **FS-07** | **R7** | **Giả lập Giao diện Người dùng (View-As Simulation)**<br>MOE HQ đóng vai School User hoặc Phụ huynh để hỗ trợ xử lý sự cố (chế độ Read-only). | MOE HQ Support | Admin Portal | **Post-MVP** | [FS-07.md](FS%20document/FS-07_User_Simulation_ViewAs.md) | Specification Ready |
| **FS-08** | **R8** | **Cổng Dịch vụ Phụ huynh (Parent Portal & Profile)**<br>Đăng nhập SingPass, On-demand Sync dữ liệu con, Bento cards xem số dư EA và cập nhật My Details. | Parent / Guardian | e-Service Portal | **Sprint 1** | [FS-08.md](FS%20document/FS-08_Parent_Portal_SingPass_Profile.md) | Official Baseline v0.4 |
| **FS-09** | **R9** | **Công nợ Học phí & Thanh toán (Fee Payment)**<br>Xem công nợ, Thanh toán qua EA, Cổng trực tuyến Sandbox, Chia đôi (Split payment) & Tự động hoàn tiền. | Parent / Guardian | e-Service Portal | **Sprint 1** | [FS-09.md](FS%20document/FS-09_Outstanding_Fees_and_Payment.md) | Official Baseline Final |
| **FS-10** | **R10** | **Nộp đơn FAS theo Hộ gia đình (Family Unit & AI)**<br>Nộp đơn trợ cấp chung cho các con trong gia đình; AI Auto-Fill tự động điền đơn từ hồ sơ. | Parent / Guardian | e-Service Portal | **Sprint 3** | [FS-10.md](FS%20document/FS-10_FAS_Family_Application_Portal.md) | Specification Ready |

---

## 3. CẤU TRÚC THƯ MỤC TÀI LIỆU (100% MARKDOWN)

```
document/
├── README.md                                       # Bảng chỉ mục và hướng dẫn này
├── Feature_list.md                                 # [MỚI] Toàn bộ danh mục tính năng chức năng hệ thống (R1-R4, R8, R9)
├── FSD_ALIGNMENT_AND_GAP_AUDIT_REPORT.md           # Báo cáo kiểm toán khoảng cách đối soát baseline
├── FSD_R3_GAP_AUDIT_REPORT.md                      # Báo cáo kiểm toán khoảng cách đặc tả R3 (21 Gaps, 16 CIRs)
├── REQUIREMENTS_AND_BACKLOG_SUMMARY.md             # Báo cáo phân tích Backlog & Questionnaire
├── FS_SPECIFICATIONS_SUMMARY.md                    # Báo cáo phân tích kỹ thuật chuyên sâu FS-08 & FS-09
├── MEETINGS_AND_DECISIONS_SUMMARY.md               # Báo cáo biên bản họp & Decisions Log
├── First_meeting_questions.md                      # Bộ câu hỏi sơ khởi phiên làm việc đầu tiên
├── Noi_dung_Overview_Sprint_1.md                   # Kế hoạch thực hiện Sprint 1
├── Test Cases + Defect sprint 1.md                 # [MỚI] Master Table toàn bộ 465 Test Cases & 14 Defects
├── Test Cases/                                     # [MỚI] Phân hệ Test Cases & Defects chi tiết theo Module
│   ├── README.md                                   # Mục lục & hướng dẫn đối soát Test Cases
│   ├── TC_R1_Education_Account_Lifecycle.md       # 73 Test Cases R1 (Vòng đời TK & Đóng TK)
│   ├── TC_R3_School_Student_Fee_Management.md      # 105 Test Cases R3 (Trường, Lớp, Biểu phí)
│   ├── TC_R8_Parent_Portal_SingPass_Profile.md     # 125 Test Cases R8 (SingPass, Profile)
│   ├── TC_R9_Outstanding_Fees_and_Payment.md      # 162 Test Cases R9 (Thanh toán học phí & Split)
│   └── DEFECTS_Sprint_1_Master.md                  # 14 Bugs Sprint 1 (BUG-R1, BUG-R3, BUG-R8, BUG-R9)
│
├── Documentation/                                  # Biên bản họp, Transcript, Glossary
│   ├── Agile_Glossary.md                           # Từ điển thuật ngữ chuẩn hóa
│   ├── Kickoff_Transcript_refined.md               # Bản ghi chi tiết cuộc họp Kickoff
│   ├── MoM_Kickoff_meeting_12_10.md                # Biên bản họp Kickoff ngày 12/10
│   ├── MoM_Sprint_1_16_10.md                       # Biên bản họp tổng kết Sprint 1 ngày 16/10
│   └── Sprint_1_Review_Transcript.md               # Bản ghi âm rà soát Sprint 1
│
├── FS document/                                    # Hồ sơ đặc tả chức năng Module hóa (R1 – R10)
│   ├── FS-01_Education_Account_Lifecycle.md        # [R1] Vòng đời EA (Official Baseline v1.2)
│   ├── FS-02_Education_Account_TopUp.md            # [R2] Nạp tiền Top-Up (Official FSD Baseline)
│   ├── FS-03_School_Student_Fee_Management.md      # [R3] Quản lý Trường & Phí (Official Baseline v1.2)
│   ├── FS-04_Financial_Assistance_Scheme_FAS.md    # [R4] Trợ cấp FAS & AI Scoring (Official Baseline v1.1)
│   ├── FS-05_Hardcopy_Applications_Offline.md      # [R5] Đơn giấy offline
│   ├── FS-06_FAS_Budget_and_Statistics.md          # [R6] Ngân sách & Thống kê FAS (Official FSD Baseline)
│   ├── FS-07_User_Simulation_ViewAs.md             # [R7] Giả lập giao diện
│   ├── FS-08_Parent_Portal_SingPass_Profile.md     # [R8] Cổng Phụ huynh (Official Baseline v0.4)
│   ├── FS-09_Outstanding_Fees_and_Payment.md       # [R9] Công nợ & Thanh toán (Official Baseline Final)
│   └── FS-10_FAS_Family_Application_Portal.md      # [R10] Đơn FAS hộ gia đình
│
└── Requirement analysis/                           # Tài liệu phân tích yêu cầu & kiến trúc giải pháp
    ├── High-level_Solution.md                      # Giải pháp kỹ thuật 10 Functions (bổ sung F8 AI & Open Questions)
    ├── Function_Requirements.md                    # Yêu cầu chức năng song ngữ
    └── Functional_Requirement_3.md                 # Phân tích chi tiết Requirement 3
```
