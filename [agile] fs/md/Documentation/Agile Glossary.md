# Glossary — Education Account \+ FAS System

# **Project: MOE Education Account & Financial Assistance Scheme (Agile Training Practice — Cohort 3, 10/2026)**

# **Thuật ngữ giữ nguyên tiếng Anh, định nghĩa bằng tiếng Việt. Team đề xuất bổ sung qua comment.**

| Thuật ngữ (Term) | Giải thích |
| :---- | :---- |
| **1\. ROLES — VAI TRÒ & NGƯỜI DÙNG** |  |
| **MOE** | Ministry of Education (Bộ Giáo dục Singapore) — chủ hệ thống, tài trợ MOEFAS. |
| **MOE HQ users** | Nhân viên trụ sở MOE. Thao tác trên Admin Portal: Top-Up, cấu hình scheme, ngân sách & thống kê MOEFAS, mô phỏng giao diện (simulate views). |
| **School users** | Nhân viên trường học. Duy trì master data cấp trường, quyết định cấp SBFAS, thu nhận đơn hardcopy, ngân sách & thống kê SBFAS. |
| **Parents** | Phụ huynh học sinh. Dùng e-Service Portal qua SingPass: xem account, thanh toán phí, nộp đơn FAS. |
| **Students (Singapore Citizens)** | Học sinh — chủ sở hữu Education Account. |
| **2\. SYSTEMS & INTEGRATIONS — HỆ THỐNG & TÍCH HỢP** |  |
| **Admin Portal** | Cổng quản trị dành cho MOE HQ users và School users. |
| **e-Service Portal** | Cổng dịch vụ dành cho phụ huynh, đăng nhập bằng SingPass. |
| **SingPass** | Hệ thống định danh và đăng nhập quốc gia của Singapore. |
| **Third-party income API** | Hệ thống bên thứ ba cung cấp dữ liệu thu nhập hộ gia đình phục vụ việc xét eligibility. |
| **Online payment methods / Payment gateway** | Phương thức thanh toán trực tuyến cho phụ huynh, song song với thanh toán bằng số dư Education Account. |
| **3\. BUSINESS TERMS — THUẬT NGỮ NGHIỆP VỤ** |  |
| **Education Account** | Tài khoản giáo dục của công dân Singapore cho chi tiêu liên quan đến giáo dục. Tự động tạo & kích hoạt khi trẻ đủ 7 tuổi; tự động đóng khi đủ 16 tuổi. |
| **Top-Up** | Nạp tiền vào Education Account. Hai phạm vi: batch (theo lô, chạy theo rule cấu hình) và specific (từng account). Hai nhịp: regular (định kỳ) và ad-hoc (đột xuất). |
| **Batch top-up rules** | Rule lọc người nhận khi nạp theo lô: độ tuổi, số dư tài khoản (account balance), trạng thái học tập (schooling status). |
| **Master data** | Danh mục nền của hệ thống: trường, level/cohort, lớp, học sinh trong lớp, fee types, fee components. |
| **Level / Cohort** | Khối/niên khóa của học sinh. |
| **Fee type** | Loại phí phải nộp (ví dụ: học phí, phí hoạt động). |
| **Fee component** | Thành phần cấu thành bên trong một fee type. Subsidy áp dụng trên từng component — đơn vị tính subsidy nhỏ nhất. Lưu ý: dễ nhầm với fee type. |
| **FAS (Financial Assistance Scheme)** | Chương trình hỗ trợ tài chính cho học sinh có khó khăn tài chính. |
| **Scheme** | Một phác đồ hỗ trợ cụ thể, cấu hình được trong hệ thống (tiêu chí \+ tier \+ subsidy). Nhiều scheme có thể chạy song song. |
| **MOEFAS** | Scheme FAS toàn quốc do MOE tài trợ. Tự động cấp (auto-grant) khi hồ sơ đạt các tiêu chí định sẵn. |
| **SBFAS (School-based FAS)** | FAS cấp trường. School users quyết định cấp hay không khi hồ sơ không đạt MOEFAS. |
| **Funding source** | Nguồn tài trợ của scheme; một scheme có thể ghép nhiều nguồn (ví dụ: 90% MOE tài trợ). |
| **Eligibility criteria** | Tiêu chí đủ điều kiện của scheme: quốc tịch, household income band, per-capita income band. |
| **Household income band** | Nhóm/thang thu nhập tổng của hộ gia đình. |
| **Per-capita income band** | Nhóm/thang thu nhập bình quân đầu người (tổng thu nhập hộ chia số thành viên). |
| **Tier** | Bậc hỗ trợ trong một scheme; mỗi tier gắn với một mức subsidy trên từng fee component. |
| **Subsidy amount** | Số tiền trợ cấp giảm trừ vào fee component theo tier đã cấp. |
| **Auto-grant** | Cơ chế tự động cấp MOEFAS khi hồ sơ đạt tiêu chí, không cần duyệt tay. |
| **Application outcome** | Kết quả xét đơn FAS; phải được phản ánh chính xác vào fees payable. |
| **Fees payable** | Khoản phí thực tế phải nộp sau khi áp subsidy. |
| **Outstanding charges** | Khoản phí còn nợ, hiển thị trên e-Service Portal để phụ huynh thanh toán. |
| **Hardcopy application** | Đơn FAS giấy do phụ huynh điền offline, School users thu thập và nhập vào hệ thống. Dành cho phụ huynh không truy cập được e-Service Portal. |
| **Family unit** | Đơn vị gia đình: một đơn FAS đánh giá tất cả anh chị em trong hộ chung một kết quả. |
| **Budget & statistics** | Quản lý ngân sách và thống kê subsidy đã cấp: MOE HQ theo dõi MOEFAS; School users theo dõi SBFAS. |
| **Simulate views** | Chế độ để MOE HQ mô phỏng màn hình của School users/Parents nhằm giải đáp thắc mắc. |
| **4\. AI TERMS — THUẬT NGỮ AI** |  |
| **Rule-based logic** | Bước 1 của eligibility: xét theo rule cấu hình, quyết định đạt/không đạt tiêu chí. |
| **ML risk classification** | Model Machine Learning dự đoán mức độ khó khăn tài chính còn lại của hồ sơ; phân loại Low / Medium / High Risk. |
| **Assistance tier recommendation** | Tier hỗ trợ do model đề xuất; School user vẫn là người quyết định cuối cùng (human-in-the-loop). |
| **AI chatbot** | Trợ lý Q\&A trên e-Service Portal, trả lời câu hỏi về chức năng của portal. |
| **Dynamic follow-up questions** | Khả năng chatbot chủ động hỏi thêm để làm rõ ngữ cảnh trước khi trả lời. |
| **Auto-fill form** | Tự động điền đơn FAS từ profile phụ huynh và các câu trả lời thu được từ chatbot. |
| **5\. AGILE / BA TERMS — THUẬT NGỮ QUY TRÌNH** |  |
| **User Story** | Yêu cầu viết theo mẫu "As a..., I want..., so that...". Danh sách đầy đủ trong sheet Agile requirements, tab User Stories \+ AC. |
| **Acceptance Criteria (AC) / Gherkin** | Tiêu chí nghiệm thu của story, viết dạng Given / When / Then. |
| **MoSCoW** | Thang ưu tiên: Must have / Should have / Could have / Won't have. |
| **Sprint** | Chu kỳ 1 tuần; dự án dùng 3 sprint. Chi tiết trong sheet Agile requirements, tab Sprint Plan. |
| **DoR / DoD** | Definition of Ready / Definition of Done — tiêu chí story đủ điều kiện vào sprint / hoàn thành. |
| **Product backlog** | Danh sách story có thứ tự ưu tiên, do BA duy trì cùng PO. |
| **Walking skeleton** | Phiên bản chạy end-to-end tối thiểu (mục tiêu Sprint 1). |
| **MVP** | Minimum Viable Product — phiên bản nhỏ nhất dùng được thật. |
| **Mock / Stub** | Giả lập tích hợp ngoài (SingPass, income API, payment gateway) trong phạm vi prototype. |
| **Vertical slice** | Cắt story theo chiều đầy đủ UI → logic → data để demo được từng sprint. |

# 