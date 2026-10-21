# [AGILE] FS — SINGLE SOURCE OF TRUTH (DỰ ÁN MOE EDUCATION ACCOUNT & FEE MANAGEMENT SYSTEM)

> [!CAUTION]
> # 🚨 NGUYÊN TẮC BẤT DI BẤT DỊCH: KHÔNG ĐƯỢC PHÉP ASSUMPTION (ZERO ASSUMPTIONS)
> **DÀNH CHO TẤT CẢ AI CODING AGENTS & DEVELOPERS:**
>
> 1. **TUYỆT ĐỐI KHÔNG SUY DIỄN / ĐOÁN MÒ (ZERO ASSUMPTION):**
>    - Trong BẤT KỲ trường hợp nào, AI coding **KHÔNG ĐƯỢC PHÉP** tự ý giả định (assumption) về:
>      - Quy tắc nghiệp vụ (Business Rules), điều kiện hợp lệ (Eligibility Criteria), công thức tính phí hoặc tính trợ cấp FAS.
>      - Các trạng thái (Status Lifecycle), mã lỗi (Error codes), thông báo lỗi UI (Validation messages).
>      - Quyền hạn người dùng (Roles & RBAC: MOE HQ vs School User vs Parent).
>      - Luồng tích hợp (SingPass Mock API, Government Citizen Dataset, Payment Gateway sandbox).
> 2. **BẮT BUỘC TRÍCH DẪN NGUỒN CỤ THỂ (EVIDENCE-FIRST TRACEABILITY):**
>    - Khi viết mã nguồn, thiết kế Page Object, viết Test Case hoặc viết Assertion, AI coding **BẮT BUỘC** phải đối chiếu và trích dẫn trực tiếp từ tài liệu Markdown trong thư mục `[agile] fs/md/` (ghi rõ tên file `.md`, Section ID, Rule ID, hoặc Story ID `US-xxx`).
> 3. **XỬ LÝ ĐIỂM THIẾU HOẶC MÂU THUẪN (AMBIGUITY & GAP HANDLING):**
>    - Nếu tài liệu chưa có thông tin, bị mâu thuẫn giữa các phiên bản, hoặc chưa chốt phương án:
>      - Tra cứu ngay `FSD_ALIGNMENT_AND_GAP_AUDIT_REPORT.md` và `MEETINGS_AND_DECISIONS_SUMMARY.md`.
>      - Kiểm tra biên bản cuộc họp mới nhất: `Documentation/Meeting Transcript - 19 Oct 2026.md`.
>      - Nếu vẫn chưa có quy định: **DỪNG LẠI VÀ BÁO CÁO / HỎI NGƯỜI DÙNG**; tuyệt đối không tự bịa logic hay giả định hệ thống hoạt động thế nào.

---

## 📁 Cấu Trúc Thư Mục

Thư mục này được chia thành 2 phân hệ độc lập:

```text
[agile] fs/
├── raw/                              # TÀI LIỆU GỐC NGUYÊN BẢN TỪ GOOGLE DRIVE
│   ├── [Agile] High-level Solution.docx
│   ├── Feature list.docx
│   ├── First meeting questions.docx
│   ├── Nội dung Overview Sprint 1.docx
│   ├── Product Backlog V2.xlsm       # Backlog V2 (kèm Acceptance Criteria)
│   ├── Test Cases + Defect sprint 1.xlsx # [MỚI] 465 Test Cases & 14 Defects (R1, R3, R8, R9)
│   ├── Documentation/
│   │   ├── Agile Glossary.docx       # Bảng thuật ngữ chuyên ngành
│   │   ├── Agile requirements.xlsx   # Ma trận 10 requirements, User Stories, Sprint Plan
│   │   ├── Kickoff Transcript refined.docx
│   │   ├── Meeting Transcript - 19 Oct 2026.docx # [MỚI] Cuộc họp chốt F3/F4/OCR/Budget
│   │   ├── MoM - Kickoff meeting - 12_10.docx
│   │   ├── MoM - Sprint 1 - 16_10.docx
│   │   ├── Questionaire.xlsx         # Bảng câu hỏi làm rõ (Clarification Questionnaire)
│   │   └── Sprint 1 Review Transcript.docx
│   ├── FS document/
│   │   ├── Tổng hợp FS.docx          # FSD tổng hợp chính thức (4.96 MB)
│   │   ├── FS Function 9 - Outstanding Fees and Payment (Final).docx
│   │   ├── FS R2 – Top-Up Management.docx
│   │   ├── FS-08 Parent Portal – SingPass, Education Account, Profile.docx
│   │   └── R6 — analysis.docx
│   └── Requirement analysis/
│       ├── Function Requirements.docx
│       └── Functional Reqirement 3.docx
│
└── md/                               # TOÀN BỘ TÀI LIỆU ĐÃ CHUYỂN ĐỔI SANG MARKDOWN (.md)
    ├── [Agile] High-level Solution.md
    ├── Feature list.md               # Danh mục tính năng chi tiết
    ├── First meeting questions.md
    ├── Nội dung Overview Sprint 1.md
    ├── Product Backlog V2.md         # Toàn bộ User Stories US-001 đến US-058 & AC
    ├── Documentation/
    │   ├── Agile Glossary.md         # Thuật ngữ Agile & Domain chuẩn
    │   ├── Agile requirements.md     # Requirements (EN/VN), US + AC, Sprint Plan
    │   ├── Kickoff Transcript refined.md
    │   ├── Meeting Transcript - 19 Oct 2026.md # Transcript cuộc họp 19/10/2026
    │   ├── MoM - Kickoff meeting - 12_10.md
    │   ├── MoM - Sprint 1 - 16_10.md
    │   ├── Questionaire.md           # Questionnaire các sheet
    │   └── Sprint 1 Review Transcript.md
    ├── FS document/
    │   ├── Tổng hợp FS.md            # Đặc tả FSD tổng thể toàn hệ thống (1.97 MB)
    │   ├── FS-01_Education_Account_Lifecycle.md       # R1: Vòng đời tài khoản EA
    │   ├── FS-02_Education_Account_TopUp.md          # R2: Nạp tiền đơn lẻ & theo lô
    │   ├── FS-03_School_Student_Fee_Management.md     # R3: Quản lý Trường, Lớp & Biểu phí
    │   ├── FS-04_Financial_Assistance_Scheme_FAS.md   # R4: Trợ cấp tài chính FAS & AI Scoring
    │   ├── FS-05_Hardcopy_Applications_Offline.md     # R5: Xử lý đơn giấy (OCR)
    │   ├── FS-06_FAS_Budget_and_Statistics.md         # R6: Ngân sách & Cảnh báo FAS
    │   ├── FS-07_User_Simulation_ViewAs.md            # R7: Giả lập góc nhìn người dùng
    │   ├── FS-08_Parent_Portal_SingPass_Profile.md    # R8: Cổng Phụ huynh (SingPass, Profile)
    │   ├── FS-09_Outstanding_Fees_and_Payment.md      # R9: Công nợ & Thanh toán (EA / Online / Split)
    │   ├── FS-10_FAS_Family_Application_Portal.md     # R10: Phụ huynh nộp đơn FAS trực tuyến
    │   ├── FS R2 – Top-Up Management.md
    │   ├── FS Function 9 - Outstanding Fees and Payment (Final).md
    │   ├── FS-08 Parent Portal – SingPass, Education Account, Profile.md
    │   └── R6 — analysis.md
    ├── Requirement analysis/
    │   ├── Function Requirements.md
    │   └── Functional Reqirement 3.md
    ├── diagrams/                     # Sơ đồ tương tác SVG & HTML luồng hệ thống
    ├── FSD_ALIGNMENT_AND_GAP_AUDIT_REPORT.md # Báo cáo đối soát gap, mâu thuẫn & quyết định
    ├── FSD_R3_GAP_AUDIT_REPORT.md    # Báo cáo gap chuyên sâu Requirement 3
    ├── FS_SPECIFICATIONS_SUMMARY.md  # Tóm tắt kiến trúc 10 Functions
    ├── REQUIREMENTS_AND_BACKLOG_SUMMARY.md # Tóm tắt ma trận Requirements & Backlog
    ├── MEETINGS_AND_DECISIONS_SUMMARY.md   # Tổng hợp quyết định từ các cuộc họp
    ├── Test Cases + Defect sprint 1.md    # [MỚI] Master Table toàn bộ 465 Test Cases & 14 Defects
    ├── Test Cases/                        # [MỚI] Phân hệ Test Cases & Defects chi tiết theo Module
    │   ├── README.md                      # Mục lục & hướng dẫn đối soát Test Cases
    │   ├── TC_R1_Education_Account_Lifecycle.md  # 73 Test Cases R1 (Vòng đời TK & Đóng TK)
    │   ├── TC_R3_School_Student_Fee_Management.md # 105 Test Cases R3 (Trường, Lớp, Biểu phí)
    │   ├── TC_R8_Parent_Portal_SingPass_Profile.md # 125 Test Cases R8 (SingPass, Profile)
    │   ├── TC_R9_Outstanding_Fees_and_Payment.md # 162 Test Cases R9 (Thanh toán học phí & Split)
    │   └── DEFECTS_Sprint_1_Master.md     # 14 Bugs Sprint 1 (BUG-R1, BUG-R3, BUG-R8, BUG-R9)
    ├── EAFAMS_SPLIT_PAYMENT_AND_AI_FAS_TEST_CASES_AND_AC.md
    └── EAFAMS_UI_SPECIFICATION_AND_INTERACTION_GUIDE.md
```

---

## 🧭 Hướng Dẫn AI Coding Tra Cứu Tài Liệu (Navigation Matrix)

| Bạn cần code / test gì? | Nguồn chuẩn bắt buộc phải đọc trong `[agile] fs/md/` |
| :--- | :--- |
| **Test Cases Sprint 1 (Toàn bộ 465 Test Cases R1, R3, R8, R9)** | `Test Cases/` (`TC_R1_...`, `TC_R3_...`, `TC_R8_...`, `TC_R9_...`) & `Test Cases + Defect sprint 1.md` |
| **Defect Log & Known Issues (BUG-R1, BUG-R3, BUG-R8, BUG-R9)** | `Test Cases/DEFECTS_Sprint_1_Master.md` (kèm cú pháp `@pytest.mark.xfail`) |
| **Vòng đời TK Education Account (Tạo, Đóng, Chuyển CPF)** | `FS document/FS-01_Education_Account_Lifecycle.md` & `Test Cases/TC_R1_Education_Account_Lifecycle.md` |
| **Nạp tiền Top-Up (Lẻ, Lô, Campaign, Hiệu chỉnh bút toán)** | `FS document/FS-02_Education_Account_TopUp.md` & `FS R2 – Top-Up Management.md` |
| **Quản lý Trường học, Lớp, Học sinh, Biểu phí & Đợt thu** | `FS document/FS-03_School_Student_Fee_Management.md` & `Test Cases/TC_R3_School_Student_Fee_Management.md` |
| **Xét duyệt Trợ cấp FAS, Mô hình AI/ML Scoring, Tiêu chí** | `FS document/FS-04_Financial_Assistance_Scheme_FAS.md` & `Meeting Transcript - 19 Oct 2026.md` |
| **Đơn FAS giấy Offline & OCR trích xuất dữ liệu** | `FS document/FS-05_Hardcopy_Applications_Offline.md` |
| **Ngân sách MOEFAS, SBFAS & Cảnh báo vượt ngân sách** | `FS document/FS-06_FAS_Budget_and_Statistics.md` & `FS document/R6 — analysis.md` |
| **Giả lập góc nhìn View-As (Simulation Mode)** | `FS document/FS-07_User_Simulation_ViewAs.md` |
| **Cổng Phụ huynh: SingPass Login, Tra cứu EA, Cập nhật Profile** | `FS document/FS-08_Parent_Portal_SingPass_Profile.md` & `Test Cases/TC_R8_Parent_Portal_SingPass_Profile.md` |
| **Thanh toán học phí (Trừ EA, Online Sandbox, Split Payment, Reversal)** | `FS document/FS-09_Outstanding_Fees_and_Payment.md` & `Test Cases/TC_R9_Outstanding_Fees_and_Payment.md` |
| **Phụ huynh nộp đơn FAS trực tuyến & AI Auto-fill** | `FS document/FS-10_FAS_Family_Application_Portal.md` |
| **User Stories, Acceptance Criteria (AC), Priority, Dependencies** | `Product Backlog V2.md` & `Documentation/Agile requirements.md` |
| **Định nghĩa thuật ngữ chuẩn Singapore GovTech** | `Documentation/Agile Glossary.md` |
| **Quyết định chốt từ Client / Product Owner qua các cuộc họp** | `MEETINGS_AND_DECISIONS_SUMMARY.md` & `Documentation/Meeting Transcript - 19 Oct 2026.md` |
| **Kiểm tra Gap, Mâu thuẫn hoặc điểm chưa thống nhất** | `FSD_ALIGNMENT_AND_GAP_AUDIT_REPORT.md` |
