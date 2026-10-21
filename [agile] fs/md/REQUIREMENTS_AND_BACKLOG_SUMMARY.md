# BÁO CÁO PHÂN TÍCH YÊU CẦU VÀ PRODUCT BACKLOG DỰ ÁN EDUCATION ACCOUNT
*(Comprehensive Requirements, Agile Backlog, Sprint Allocation & Questionnaire Analysis Report)*

> **Tác giả:** Chuyên viên Phân tích Yêu cầu & Backlog (Requirements & Backlog Analyst)
> **Dự án:** Education Account System (Admin Portal & e-Service Portal)
> **Tài liệu nguồn:** `Product Backlog.xlsx`, `Agile requirements.xlsx`, `Questionaire.xlsx`
> **Ngày lập báo cáo:** 17/10/2026

---
## MỤC LỤC TỔNG QUAN
1. [Tổng quan & Danh mục các File / Sheet](#1-tổng-quan--danh-mục-các-file--sheet)
2. [Danh mục Chi tiết User Stories & Product Backlog](#2-danh-mục-chi-tiết-user-stories--product-backlog)
   - 2.1. Bảng Chi tiết 28 Product Backlog Items (Product Backlog.xlsx)
   - 2.2. Bảng 14 User Stories & Acceptance Criteria chuẩn Agile (Agile requirements.xlsx)
   - 2.3. Ma trận Truy vết Yêu cầu Nguồn (R1–R10 Traceability Matrix)
3. [Kế hoạch Phân bổ Sprint & Tiến độ Thực thi](#3-kế-hoạch-phân-bổ-sprint--tiến-độ-thực-thi)
   - 3.1. So sánh 2 Mô hình Phân bổ Sprint
   - 3.2. Trọng tâm Sprint 1: Walking Skeleton & Thanh toán R9
   - 3.3. Kế hoạch Sprint 2 & Sprint 3
   - 3.4. Nhóm Hạng mục Hậu MVP (Unscheduled / Deferred AI & ML)
   - 3.5. Hiện trạng Ước lượng (Story Points / Estimation)
4. [Ma trận Phân bổ Tính năng theo Portal (Admin vs e-Service)](#4-ma-trận-phân-bổ-tính-năng-theo-portal-admin-vs-e-service)
5. [Phân tích Bảng Câu hỏi & Quyết định của Khách hàng (Questionnaire & Decisions)](#5-phân-tích-bảng-câu-hỏi--quyết-định-của-khách-hàng)
   - 5.1. 12 Quyết định & Làm rõ Cốt lõi của Khách hàng (Client Decisions CD-01 đến CD-12)
   - 5.2. Bảng 30 Câu hỏi Clarification trong Updated Questionaire
   - 5.3. 17 Câu hỏi Mở Ưu tiên Cao trong Product Backlog (Open Questions OQ-01 đến OQ-17)
   - 5.4. Bảng câu hỏi chuyên sâu cho Sprint 2
6. [Nhận định Rủi ro, Lỗ hổng Yêu cầu & Khuyến nghị Hành động](#6-nhận-định-rủi-ro-lỗ-hổng-yêu-cầu--khuyến-nghị-hành-động)

---

## 1. TỔNG QUAN & DANH MỤC CÁC FILE / SHEET

Toàn bộ yêu cầu và kế hoạch triển khai của hệ thống **Education Account** được quản lý tập trung qua 3 tài liệu Excel trong thư mục `document/`. Hệ thống phục vụ 2 nhóm người dùng chính tương ứng với 2 portal riêng biệt: **Admin Portal** (dành cho MOE HQ và Ban giám hiệu/Văn phòng Nhà trường) và **e-Service Portal** (dành cho Phụ huynh/Người giám hộ học sinh).

### 1.1. File `Product Backlog.xlsx`
- **Đường dẫn:** `/home/baudui/Projects/fs/document/Product Backlog.xlsx`
- **Mô tả chung:** Tài liệu backlog trung tâm phục vụ quản lý thực thi kỹ thuật hàng ngày của Dev, BA và PO. Bao gồm 28 hạng mục công việc được đánh số theo trình tự xây dựng (Build Sequence), tích hợp đầy đủ kiểm soát rủi ro, dependencies, điều kiện sẵn sàng (readiness) và câu hỏi mở.

| Tên Sheet | Số dòng dữ liệu | Số cột | Nội dung chính |
|---|---|---|---|
| **Product Backlog** | 32 | 18 | Chứa 28 hạng mục công việc (25 PBI PB-01..PB-25 và 3 hạng mục User Authentication), phân loại theo Epic, Sprint mục tiêu, Độ ưu tiên, Điều kiện sẵn sàng, Tiêu chí nghiệm thu và Dependencies. |
| **Sprint Tracker** | 18 | 8 | Bảng theo dõi trạng thái tiến độ theo Sprint (Sprint 1: 14 items, Sprint 2: 4 items, Sprint 3: 6 items, Unscheduled: 4 items), mục tiêu demo sprint và cảnh báo rủi ro. |
| **Open Questions** | 20 | 10 | Tổng hợp 17 câu hỏi làm rõ (OQ-01 đến OQ-17) dành cho phiên họp 30 phút thứ Hai với khách hàng, phân loại theo độ khẩn cấp (P1/P2/P3) và Sprint liên quan. |
| **Client Decisions** | 15 | 5 | Ghi nhận 12 quyết định và sự kiện đã được khách hàng làm rõ (CD-01 đến CD-12) trong cuộc họp kickoff kèm trích dẫn timestamp cuộc họp và tác động kỹ thuật. |
| **Read Me** | 11 | 4 | Quy định nguyên tắc vận hành backlog trên Google Sheets cho PO/BA và Dev team, quy tắc đánh số ID, quy ước demo và cập nhật trạng thái. |

### 1.2. File `Agile requirements.xlsx`
- **Đường dẫn:** `/home/baudui/Projects/fs/document/Documentation/Agile requirements.xlsx`
- **Mô tả chung:** Tài liệu đặc tả yêu cầu chức năng (Functional Requirements - FR) dưới dạng Agile nguyên bản, bao gồm User Stories, Tiêu chí chấp nhận (AC) viết theo chuẩn Given-When-Then, và Kế hoạch phân bổ 3 Sprint lặp (Iteration Plan) theo mô hình chuẩn.

| Tên Sheet | Số dòng dữ liệu | Số cột | Nội dung chính |
|---|---|---|---|
| **Requirements (EN)** | 11 | 26 | Danh sách 10 yêu cầu chức năng nguồn (R1 đến R10) viết bằng tiếng Anh, phân bổ theo Portal và tính năng AI mở rộng. |
| **Requirements (VN)** | 12 | 26 | Bản dịch tiếng Việt tương ứng của 10 yêu cầu chức năng nguồn (R1 đến R10). |
| **User Stories + AC** | 15 | 26 | 14 User Stories chuẩn Agile kèm Acceptance Criteria (Gherkin style: Given-When-Then) và độ ưu tiên MoSCoW (US-01 đến US-11 và 3 story AI: US-AI1, US-AI2, US-AI3). |
| **Sprint Plan** | 5 | 26 | Kế hoạch 3 Sprint (Sprint 1 Walking skeleton, Sprint 2 FAS core rule, Sprint 3 Parent portal & payment) và giai đoạn Deferred (sau MVP) cho AI/ML. |

### 1.3. File `Questionaire.xlsx`
- **Đường dẫn:** `/home/baudui/Projects/fs/document/Documentation/Questionaire.xlsx`
- **Mô tả chung:** Bảng tổng hợp câu hỏi làm rõ các khoảng trống nghiệp vụ (Gap analysis), các giả định kỹ thuật, đề xuất giải pháp của nhóm phát triển và phản hồi chính thức từ phía Khách hàng / PO.

| Tên Sheet | Số dòng dữ liệu | Số cột | Nội dung chính |
|---|---|---|---|
| **Updated Questionaire** | 31 | 27 | Bảng 30 câu hỏi làm rõ toàn diện (ID 1.0 đến 30.0) bao gồm trạng thái (Resolved, Partly, Need confirm, Open), phản hồi chính thức của Client và giải pháp đề xuất. |
| **Sheet1** | 28 | 26 | Bảng câu hỏi nghiệp vụ bằng tiếng Việt (G01 đến G24) tập trung vào Master data, Quản lý phí, và Vận hành tài khoản giáo dục. |
| **questionaire** | 35 | 26 | Bản tiếng Anh tương ứng của Sheet1 (G01 đến G24) với câu hỏi chi tiết gửi cho Client. |
| **Sheet3** | 43 | 3 | Bảng tổng hợp Requirement Gaps, Proposed Solutions và Clarification Questions dạng rút gọn. |
| **Sprint 2** | 31 | 26 | Bộ câu hỏi chuyên sâu phục vụ chuẩn bị cho Sprint 2 (F2 Top-up, F4 Income information, F10 FAS application). |

---

## 2. DANH MỤC CHI TIẾT USER STORIES & PRODUCT BACKLOG

### 2.1. Bảng Chi tiết 28 Product Backlog Items (Product Backlog.xlsx)

Product Backlog bao gồm **28 hạng mục công việc** (trong đó có 25 PBI được mã hóa chính thức từ `PB-01` đến `PB-25` theo proposed build sequence, và 3 hạng mục xác thực/đăng nhập `User Authentication & Access Management` được phân bổ vào Sprint 1). Tất cả các hạng mục đều được liên kết trực tiếp với các yêu cầu nguồn R1–R10 hoặc NFR kiến trúc.

| ID | Epic | Tên Feature / User Story | Portal / Actor | Yêu cầu nguồn | Sprint dự kiến | Ưu tiên | Readiness | Tiêu chí AC / Demo Check | Rủi ro / Câu hỏi mở |
|---|---|---|---|---|---|---|---|---|---|
| **PB-01** | Technical Enabler | **Capacity, concurrency and test baseline** | `Cross-cutting · Dev / QA` | No direct R# (meeting NFR) | **Sprint 1** | P2 - Medium | `Needs team estimate` | Proposed concurrency/load assumptions documented and reviewed by team/client. | 500 HQ users, 300 schools x ~200 users, ~2M parents are population estimates, NOT concurrency targets. |
| **PB-02** | Core Data | **Maintain school, level/cohort, class & student records** | `Admin · MOE HQ / School` | R3 | **Sprint 1** | P1 - High | `Needs AC` | Authorized users can view/edit permitted records; school users cannot edit school-level master data. | Exact HQ/School operations and cross-school scope need refinement. |
| **PB-03** | Access Control | **HQ vs School role-based permissions** | `Admin · MOE HQ / School` | R3 (clarified in meeting) | **Sprint 1** | P1 - High | `Needs AC` | HQ has broad management access; School role cannot modify unauthorized records. | Clarify school record visibility and finer permission matrix. |
| **PB-04** | Core Data | **Obtain student data from external source** | `Backend / Integration` | R1, R3, R8 (supporting enabler) | **Sprint 1** | P1 - High | `Blocked / external` | Sample student record can be loaded accurately with source and validation documented. | Actual provider, API access, keys, schema, refresh and guardian source not confirmed. |
| **PB-05** | Education Account | **Create and activate Education Account at age 7** | `Backend / Admin` | R1 | **Sprint 1** | P1 - High | `Needs AC` | Eligible example has an active account; ineligible example is not auto-created. | Age-calculation trigger, backfill, citizenship changes and ledger source not confirmed. |
| **PB-06** | Parent Portal | **Parent authentication via SingPass** | `e-Service · Parent` | R8 | **Sprint 1** | P1 - High | `Blocked / external` | Authorized test parent can sign in and sign out; unauthenticated data access is blocked. | Confirm sandbox access and identity attributes required for parent match. |
| **PB-07** | Parent Portal | **Authorize parent/guardian to linked children** | `e-Service · Parent` | R8 (supporting access control) | **Sprint 1** | P1 - High | `Needs client decision` | A parent sees only linked children and cannot request another child's account. | Guardian data source, access for multiple guardians and revocation not confirmed. |
| **PB-08** | Parent Portal | **View child account, balance & transactions** | `e-Service · Parent` | R8 | **Sprint 1** | P1 - High | `Needs AC` | Authorized parent sees correct child, balance, transaction list and empty state. | Confirm exact fields, source of transaction records and visibility for closed accounts. |
| **PB-09** | Parent Portal | **View outstanding charges** | `e-Service · Parent` | R9 | **Sprint 1** | P1 - High | `At risk / dependency` | Parent sees correct charges only for their linked child, with amounts/status and an empty state; can choose a payable charge for one of the R9 payment paths. | For Sprint 1, confirm authoritative or demo charge dataset, due/remaining amount, and which child can see each charge. Billing generation is not yet confirmed. |
| **PB-10** | Payments | **Pay eligible charges using Education Account** | `e-Service / Backend` | R3, R9 | **Sprint 1** | P1 - High | `At risk / dependency` | Given an eligible unpaid charge and sufficient balance, authorized parent pays once; account balance and amount outstanding both reduce exactly once; failures do not alter balances. | P1 clarification: eligible charge categories, sufficient/insufficient balance, full vs partial payment, duplicate submission and settlement rules; validate financial ledger feasibility with Dev. |
| **PB-11** | Payments | **Pay fees via online payment method** | `e-Service · Parent` | R9 | **Sprint 1** | P1 - High | `Blocked / external` | Parent can select an available online method, complete a successful test payment and see outstanding charge updated; failed/cancelled payment remains outstanding and does not double-collect. | PAYMENT GATE: gateway, permitted methods, test credentials, callbacks, payment confirmation, failed/cancelled payments, refund and reconciliation are not yet defined. |
| ***(Auth)*** | User Authentication & Access Management | **Admin Portal Login** | `Admin · MOE HQ / School` | R3 (Inferred — supporting capability) | **Sprint 1** | P1 - High | `` |  |  |
| ***(Auth)*** | User Authentication & Access Management | **Parent Login via SingPass** | `e-Service · Parent` | R8 | **Sprint 1** | P1 - High | `` |  |  |
| ***(Auth)*** | User Authentication & Access Management | **School User Login** | `Admin · MOE HQ / School` | R3 (Inferred — supporting capability) | **Sprint 1** | P1 - High | `` |  |  |
| **PB-12** | Fee Management | **Maintain fee types and components** | `Admin · MOE HQ / School` | R3 | **Sprint 2** | P1 - High | `Needs AC` | User can configure fee type/component and retrieve valid fee definition. | Fees, attributes, owners, effective dates; GST reuse suggested if feasible, not mandatory. |
| **PB-13** | Fee Management | **Create/record payable charges for students** | `Admin / Backend` | R3, R9 (proposed billing flow) | **Sprint 2** | P1 - High | `Needs client decision` | A valid charge appears against correct student, with source and status traceable. | Client challenged manual fee assignment; confirm bill source, actor and billing process first. |
| **PB-14** | Top-Up | **MOE HQ individual & batch Education Account top-up** | `Admin · MOE HQ` | R2 | **Sprint 2** | P1 - High | `Needs client decision` | Eligible accounts credited once per approved run; ineligible accounts skipped. | Exact selection rules, run schedules, amount calculation, rerun handling and audit controls needed. |
| **PB-15** | Parent Portal | **Update editable personal details** | `e-Service · Parent` | R8 | **Sprint 2** | P2 - Medium | `Needs client decision` | Editable fields save successfully; protected fields remain read-only. | Which fields are writable? Does system push changes back to source of truth? |
| **PB-16** | Education Account | **Close Education Account at age 16** | `Backend / Admin` | R1 | **Sprint 3** | P1 - High | `Blocked / external` | Closure scenario shows correct status; reconciliation/CPF flow tested against agreed design. | Client expects no pending transactions and residual balance to CPF; exact handling/API not agreed. |
| **PB-17** | FAS | **Configure FAS schemes, criteria and subsidy tiers** | `Admin · MOE HQ / School` | R4 | **Sprint 3** | P1 - High | `Needs client decision` | Admin can define example scheme and evaluate an agreed eligibility test case. | Thresholds, tier definitions, scheme authority, eligibility versioning and external income source missing. |
| **PB-18** | FAS | **Online FAS application by family unit** | `e-Service · Parent` | R10 | **Sprint 3** | P1 - High | `Needs client decision` | Parent submits a family application; submission can be retrieved for review. | Define family-unit members, required evidence, consent and submission rules. |
| **PB-19** | FAS | **Assess FAS and apply approved subsidies** | `Admin / Backend` | R4 | **Sprint 3** | P1 - High | `Needs client decision` | Approved subsidy changes payable fee correctly; rejected cases do not get subsidy. | Approval roles/states, precedence between schemes, income lookup and recalculation rules missing. |
| **PB-20** | FAS | **School entry of offline FAS applications** | `Admin · School` | R5 | **Sprint 3** | P2 - Medium | `Needs AC` | School can enter an offline application that follows agreed assessment flow. | Identity/consent checks, evidence capture, deduplication and workflow need clarification. |
| **PB-21** | FAS / Reporting | **Set and track MOEFAS / SBFAS budgets** | `Admin · MOE HQ / School` | R6 | **Sprint 3** | P2 - Medium | `Needs AC` | Award totals and remaining budget match agreed calculations per scope. | Budget period, overspend rules, approval trail, calculations and reporting breakdown missing. |
| **PB-22** | Support | **Simulate school/parent view for support** | `Admin · MOE HQ` | R7 | **Unscheduled / trade-off** | P3 - Low | `Needs client decision` | Support role can inspect authorized user experience with recorded audit trail. | Read-only vs impersonation, privacy, audit and consent requirements not defined. |
| **PB-23** | AI | **AI conversational help for e-Service users** | `e-Service · Parent` | R8, R9 (AI Feature) | **Unscheduled / trade-off** | P3 - Low | `Needs client decision` | Assistant addresses supported portal-use question and handles unknowns safely. | Approved knowledge source, model/provider, privacy and expected quality need definition. |
| **PB-24** | AI | **AI-assisted FAS application prefill** | `e-Service · Parent` | R10 (AI Feature) | **Unscheduled / trade-off** | P3 - Low | `Needs client decision` | Prefilled draft shown for confirmation; no unapproved submission. | Consent, field mapping, verification of generated values and privacy unknown. |
| **PB-25** | AI / ML | **Predict financial difficulty risk tiers** | `Admin / Backend` | R4 (AI Feature) | **Unscheduled / trade-off** | P3 - Low | `Blocked / feasibility` | Demonstrable validated prediction on agreed test set if feasible. | Training dataset, outcome labels, explainability, bias evaluation and decision authority missing. |

#### Bảng Mô tả Chi tiết Từng Hạng mục Product Backlog (User Story & Context):

**[PB-01] Capacity, concurrency and test baseline** (Seq: 1.0)
- **Mô tả / User Story:** Description: Define the performance and capacity baseline for the HQ, School and Parent portals. Propose concurrency targets and QA load-test scenarios from the client-provided user populations and usage periods; population counts are not confirmed concurrent user targets.
- **Cơ sở yêu cầu (Basis):** Client estimates + proposed task
- **Phụ thuộc kỹ thuật (Dependencies):** Architecture + expected usage profile

**[PB-02] Maintain school, level/cohort, class & student records** (Seq: 2.0)
- **Mô tả / User Story:** As an authorized MOE HQ or School User, I want to maintain the school, level/cohort, class and student records within my permissions, so that the system has accurate school and student information.
- **Cơ sở yêu cầu (Basis):** Initial + client clarified
- **Phụ thuộc kỹ thuật (Dependencies):** School/student data model

**[PB-03] HQ vs School role-based permissions** (Seq: 3.0)
- **Mô tả / User Story:** As an MOE HQ administrator, I want HQ and School Users to have access limited by their roles and authorized records, so that school and student data can only be managed by permitted users.
- **Cơ sở yêu cầu (Basis):** Client clarified
- **Phụ thuộc kỹ thuật (Dependencies):** PB-02; user identity/roles

**[PB-04] Obtain student data from external source** (Seq: 4.0)
- **Mô tả / User Story:** Description: Retrieve or import student master data from the agreed external source, including name, date of birth, citizenship and address where available. Establish student identifiers and determine how trusted parent/guardian relationships will be sourced; the interface and mapping remain unconfirmed.
- **Cơ sở yêu cầu (Basis):** Proposed implementation
- **Phụ thuộc kỹ thuật (Dependencies):** External source/API, unique identifiers

**[PB-05] Create and activate Education Account at age 7** (Seq: 5.0)
- **Mô tả / User Story:** As an MOE HQ user, I want an Education Account to be created and activated automatically for an eligible Singapore Citizen at age 7, so that the child's education funding can be administered.
- **Cơ sở yêu cầu (Basis):** Initial + client clarified
- **Phụ thuộc kỹ thuật (Dependencies):** PB-04; account data design

**[PB-06] Parent authentication via SingPass** (Seq: 6.0)
- **Mô tả / User Story:** As a parent/guardian, I want to sign in to the e-Service Portal through SingPass, so that I can securely access the services available to me.
- **Cơ sở yêu cầu (Basis):** Initial requirement
- **Phụ thuộc kỹ thuật (Dependencies):** SingPass environment, test identities

**[PB-07] Authorize parent/guardian to linked children** (Seq: 7.0)
- **Mô tả / User Story:** As a parent/guardian, I want to see only the children I am authorized to represent after signing in, so that I can access their information without seeing other students' records.
- **Cơ sở yêu cầu (Basis):** Proposed solution / implied
- **Phụ thuộc kỹ thuật (Dependencies):** PB-04, PB-06; trusted guardian mapping

**[PB-08] View child account, balance & transactions** (Seq: 8.0)
- **Mô tả / User Story:** As a parent/guardian, I want to view my linked child's Education Account details, balance and transaction history, so that I can understand how the education funds have been used.
- **Cơ sở yêu cầu (Basis):** Initial requirement
- **Phụ thuộc kỹ thuật (Dependencies):** PB-05, PB-07; ledger/source

**[PB-09] View outstanding charges** (Seq: 9.0)
- **Mô tả / User Story:** As a parent/guardian, I want to see my linked child's outstanding school charges and the amounts due, so that I know what remains to be paid.
- **Cơ sở yêu cầu (Basis):** Initial requirement
- **Phụ thuộc kỹ thuật (Dependencies):** PB-07, charge data / PB-13

**[PB-10] Pay eligible charges using Education Account** (Seq: 10.0)
- **Mô tả / User Story:** As a parent/guardian, I want to pay eligible outstanding school charges using the available balance in my child's Education Account, so that I can use those funds toward school fees. Eligibility, partial-payment and insufficient-funds rules remain open.
- **Cơ sở yêu cầu (Basis):** Initial requirement
- **Phụ thuộc kỹ thuật (Dependencies):** PB-05, PB-07, PB-08; charge dataset (PB-13 or agreed test fixtures); transactional ledger

**[PB-11] Pay fees via online payment method** (Seq: 11.0)
- **Mô tả / User Story:** As a parent/guardian, I want to pay outstanding school charges through an available online payment method, so that I can settle fees electronically. Supported methods and payment provider are not yet confirmed.
- **Cơ sở yêu cầu (Basis):** Initial requirement
- **Phụ thuộc kỹ thuật (Dependencies):** PB-07, PB-09; charge dataset; selected payment provider/gateway or test sandbox; callbacks

**[Auth-01] Admin Portal Login** (Seq: )
- **Mô tả / User Story:** As an MOE HQ or School User, I want to log in to the Admin Portal securely, so that I can access the system functions and data according to my assigned role.
- **Cơ sở yêu cầu (Basis):** 
- **Phụ thuộc kỹ thuật (Dependencies):** User authentication mechanism, user roles and permissions

**[Auth-02] Parent Login via SingPass** (Seq: )
- **Mô tả / User Story:** As a Parent/Guardian, I want to log in to the e-Service Portal using SingPass, so that I can securely access my child's education-related information.
- **Cơ sở yêu cầu (Basis):** 
- **Phụ thuộc kỹ thuật (Dependencies):** Không có

**[Auth-03] School User Login** (Seq: )
- **Mô tả / User Story:** As a School User, I want to securely log in to the Admin Portal, so that I can access and manage school-related information according to my assigned permissions.
- **Cơ sở yêu cầu (Basis):** 
- **Phụ thuộc kỹ thuật (Dependencies):** Không có

**[PB-12] Maintain fee types and components** (Seq: 12.0)
- **Mô tả / User Story:** As an authorized administrative user, I want to maintain fee types and their components, so that school charges can be defined consistently. Reusable components such as GST are subject to feasibility and scope confirmation.
- **Cơ sở yêu cầu (Basis):** Initial + client examples
- **Phụ thuộc kỹ thuật (Dependencies):** PB-02; fee/charge data model

**[PB-13] Create/record payable charges for students** (Seq: 13.0)
- **Mô tả / User Story:** Description: Provide an agreed mechanism to create or receive payable charge records for students, including the charge amount, type and outstanding amount/status. The originating system, responsible actor and charging process are NOT yet confirmed; do not assume manual fee assignment.
- **Cơ sở yêu cầu (Basis):** Gap / proposed solution
- **Phụ thuộc kỹ thuật (Dependencies):** PB-02, PB-12

**[PB-14] MOE HQ individual & batch Education Account top-up** (Seq: 14.0)
- **Mô tả / User Story:** As an MOE HQ user, I want to top up an individual Education Account or a batch of eligible accounts using configurable rules, so that education funding can be allocated efficiently.
- **Cơ sở yêu cầu (Basis):** Initial requirement
- **Phụ thuộc kỹ thuật (Dependencies):** PB-05; transaction ledger

**[PB-15] Update editable personal details** (Seq: 15.0)
- **Mô tả / User Story:** As a parent/guardian, I want to update the personal information fields that I am authorized to edit, so that my details remain current. The editable fields and source-of-truth update process need confirmation.
- **Cơ sở yêu cầu (Basis):** Initial; details open
- **Phụ thuộc kỹ thuật (Dependencies):** PB-06; profile source

**[PB-16] Close Education Account at age 16** (Seq: 16.0)
- **Mô tả / User Story:** As an MOE HQ user, I want an Education Account to be closed when the child reaches age 16 and any remaining balance transferred to CPF, so that the account's funds are handled on closure. Pending transactions and transfer processing still need clarification.
- **Cơ sở yêu cầu (Basis):** Initial + client clarified
- **Phụ thuộc kỹ thuật (Dependencies):** PB-05; CPF transfer integration

**[PB-17] Configure FAS schemes, criteria and subsidy tiers** (Seq: 17.0)
- **Mô tả / User Story:** As an authorized FAS administrator, I want to configure MOEFAS and SBFAS eligibility criteria and subsidy tiers, so that applications can be assessed using the applicable scheme rules. Detailed thresholds and authority remain to be confirmed.
- **Cơ sở yêu cầu (Basis):** Initial; rules open
- **Phụ thuộc kỹ thuật (Dependencies):** Student/household model; income API

**[PB-18] Online FAS application by family unit** (Seq: 18.0)
- **Mô tả / User Story:** As a parent/guardian, I want to submit an online FAS application for my family unit, so that my family can request financial assistance for education costs.
- **Cơ sở yêu cầu (Basis):** Initial requirement
- **Phụ thuộc kỹ thuật (Dependencies):** PB-06, PB-17; household data model

**[PB-19] Assess FAS and apply approved subsidies** (Seq: 19.0)
- **Mô tả / User Story:** Description: Assess MOEFAS eligibility according to agreed rules, support school-level decisions for SBFAS, and reflect approved assistance in eligible school charges. Assessment criteria, approvals, overlaps and fee application rules need clarification.
- **Cơ sở yêu cầu (Basis):** Initial; rules open
- **Phụ thuộc kỹ thuật (Dependencies):** PB-13, PB-17, PB-18

**[PB-20] School entry of offline FAS applications** (Seq: 20.0)
- **Mô tả / User Story:** As a School User, I want to enter an FAS application received on paper, so that families who cannot apply through the e-Service Portal can still request assistance.
- **Cơ sở yêu cầu (Basis):** Initial requirement
- **Phụ thuộc kỹ thuật (Dependencies):** PB-17, PB-18

**[PB-21] Set and track MOEFAS / SBFAS budgets** (Seq: 21.0)
- **Mô tả / User Story:** As an authorized MOE HQ or School User, I want to track scheme budgets and subsidy statistics within my responsibility, so that I can monitor financial assistance allocations and usage.
- **Cơ sở yêu cầu (Basis):** Initial requirement
- **Phụ thuộc kỹ thuật (Dependencies):** PB-19; subsidy award data

**[PB-22] Simulate school/parent view for support** (Seq: 22.0)
- **Mô tả / User Story:** As an authorized MOE HQ support user, I want to view the portal experience of a School User or Parent, so that I can investigate reported issues. Simulation permissions, privacy, read-only behavior and audit requirements remain to be confirmed.
- **Cơ sở yêu cầu (Basis):** Initial requirement
- **Phụ thuộc kỹ thuật (Dependencies):** PB-03, PB-06, PB-08

**[PB-23] AI conversational help for e-Service users** (Seq: 23.0)
- **Mô tả / User Story:** As a parent/guardian, I want an AI assistant to answer questions about using the e-Service Portal and ask follow-up questions when needed, so that I can get help completing supported tasks.
- **Cơ sở yêu cầu (Basis):** Initial AI feature
- **Phụ thuộc kỹ thuật (Dependencies):** Product help content, security and AI service

**[PB-24] AI-assisted FAS application prefill** (Seq: 24.0)
- **Mô tả / User Story:** As a parent/guardian, I want a draft FAS application to be prefilled with permitted existing information or answers I provide through the AI assistant, so that I can review it before submission.
- **Cơ sở yêu cầu (Basis):** Initial AI feature
- **Phụ thuộc kỹ thuật (Dependencies):** PB-18, PB-23

**[PB-25] Predict financial difficulty risk tiers** (Seq: 25.0)
- **Mô tả / User Story:** Description: Develop an ML-based financial difficulty prediction capability that groups cases into Low, Medium and High risk and suggests an assistance tier, subject to an agreed dataset, evaluation approach and human decision responsibilities.
- **Cơ sở yêu cầu (Basis):** Initial AI feature
- **Phụ thuộc kỹ thuật (Dependencies):** Historical labeled data, PB-17, ML approach

---

### 2.2. Bảng 14 User Stories & Acceptance Criteria chuẩn Agile (Agile requirements.xlsx)

Tài liệu `Agile requirements.xlsx` định nghĩa **14 User Stories**, trong đó 11 story thuộc nghiệp vụ cốt lõi (US-01 đến US-11) và 3 story thuộc năng lực trí tuệ nhân tạo (US-AI1 đến US-AI3). Tiêu chí chấp nhận được định dạng theo chuẩn kiểm thử hành vi (Behavior-Driven Development / Gherkin format: Given-When-Then):

| Story ID (FR ref) | User Story (As a... I want... So that...) | Acceptance Criteria (Given - When - Then) | MoSCoW |
|---|---|---|---|
| **US-01 (FR1)** | As a MOE HQ user, I want education accounts to be automatically created when a child turns 7 and automatically closed at 16, so that no manual setup is needed. | Given a Singapore Citizen child turns 7 years old, When the daily batch job runs, Then an education account is created and activated automatically. - Given an account holder turns 16 years old, When the daily batch job runs, Then the education account is closed automatically. | **Must** |
| **US-02 (FR2)** | As a MOE HQ user, I want to top up education accounts in batches or individually, so that funds reach eligible students on a regular or ad-hoc basis. | Given batch rules are configured (age, balance, schooling status), When a batch top-up is executed, Then only matching accounts receive the top-up amount. - Given a specific account holder, When an ad-hoc top-up is performed, Then the balance increases and a transaction is recorded. | **Should** |
| **US-03 (FR3)** | As a MOE HQ or School user, I want to maintain master data of schools, levels/cohorts, classes, students, fee types and fee components, so that fees and accounts are computed correctly. | Given the master data screen, When a School user adds a student to a class, Then the student is linked to the school and class. - When a fee type is updated with new fee components, Then subsequent charges use the new components. | **Must** |
| **US-04 (FR4)** | As a student, I want to pay fees using my education account balance, so that I can settle school fees without cash. | Given an outstanding fee and sufficient account balance, When payment is made from the education account, Then the outstanding amount is reduced and a transaction is recorded. | **Must** |
| **US-05 (FR5)** | As a parent, I want to apply for FAS for my child, so that financial assistance is granted if we are eligible. | Given an application meeting all predefined MOEFAS criteria (nationality, income bands), When household income is verified via the third-party API, Then MOEFAS is auto-granted and the fees payable are reduced accordingly. - Given MOEFAS is not granted, When a School user approves School-based FAS (SBFAS), Then the subsidy applies to the configured fee components. | **Must** |
| **US-06 (FR6)** | As a School user, I want to capture and process hardcopy FAS applications, so that parents without portal access can still apply. | Given a hardcopy form collected from a parent, When the School user enters it into the system, Then it is processed with the same eligibility logic as an online application. - Given the same family already applied online, When the hardcopy is entered, Then the system flags the duplicate. | **Should** |
| **US-07 (FR7)** | As a MOE HQ or School user, I want to set a budget and view statistics of subsidies granted, so that I can monitor spending against budget. | Given subsidies granted in a period, When the user opens the statistics view, Then totals per scheme and tier are shown against the set budget. - Given the budget is nearly exhausted, When new subsidies are granted, Then the view highlights the utilization. | **Should** |
| **US-08 (FR8)** | As a MOE HQ user, I want to simulate the School user and Parent views, so that I can address their queries accurately. | Given simulation mode, When the MOE HQ user selects a role (School user or Parent), Then the system displays exactly what that role would see. | **Could** |
| **US-09 (FR9)** | As a parent, I want to log in to the e-Service Portal via SingPass, so that I can view my child's education account and keep my details up to date. | Given valid SingPass credentials, When the parent logs in, Then account details, balance and transactions are displayed. - When the parent updates residential address, mailing address or contact number, Then the changes are saved and reflected in the profile. | **Must** |
| **US-10 (FR10)** | As a parent, I want to view outstanding charges and pay them, so that I can settle fees conveniently. | Given outstanding charges exist, When the parent chooses to pay from the education account balance, Then the charge is settled and a transaction is recorded. - When the parent chooses an online payment method and completes payment, Then the charge is settled via the payment gateway. | **Must** |
| **US-11 (FR11)** | As a parent, I want to apply for FAS as a family unit, so that all my children are assessed together in one application. | Given a family unit with multiple children, When the parent submits one FAS application, Then all students in the family are assessed under the same application and receive the same outcome. | **Must** |
| **US-AI1 (FR5-AI)** | As a School user, I want an ML model to classify the applicant's remaining financial difficulty (Low/Medium/High Risk) and recommend an assistance tier, so that I can make faster SBFAS decisions. | Given rule-based eligibility passes, When the ML model scores the application, Then a Low/Medium/High Risk classification and a tier recommendation are shown to the School user for decision. | **Could** |
| **US-AI2 (FR9-AI)** | As a parent, I want an AI chatbot to answer questions about the e-Service Portal, so that I can self-serve without calling support. | Given the parent asks a portal-related question, When the chatbot lacks context, Then it asks dynamic follow-up questions and then provides a relevant answer. | **Could** |
| **US-AI3 (FR11-AI)** | As a parent, I want the FAS application form to be auto-filled from my profile, so that I can apply faster with fewer errors. | Given the parent profile and answers gathered from the chatbot, When the FAS form is opened, Then relevant fields are pre-filled and the parent only confirms and submits. | **Could** |

---
### 2.3. Ma trận Truy vết Yêu cầu Nguồn (R1–R10 Traceability Matrix)

Dưới đây là ma trận đối chiếu 10 yêu cầu chức năng nguồn (Source Requirements R1–R10) với các User Stories Agile và các hạng mục Product Backlog Items tương ứng:

| Yêu cầu nguồn | Nội dung tóm tắt | Portal | User Story tương ứng | PBI tương ứng (Product Backlog) |
|---|---|---|---|---|
| **R1** | Education account is available to Singapore Citizen for education related spending. Auto created/activated at age 7, auto closed at age 16. | `Admin / Backend` | **US-01 (FR1)** | PB-05 (Create at 7 - Sprint 1), PB-16 (Close at 16 - Sprint 3) |
| **R2** | MOE HQ users can perform 'Top-Up' to education accounts (batch by rules: age, balance, schooling status; or ad-hoc to specific accounts). | `Admin Portal` | **US-02 (FR2)** | PB-14 (Sprint 2) |
| **R3** | MOE HQ & School users maintain master data: schools, levels/cohorts, classes, students, fee types & fee components. Singaporean students can use balance to pay fees. | `Admin & e-Service` | **US-03 (FR3), US-04 (FR4)** | PB-02 (School/Student - S1), PB-03 (RBAC - S1), PB-04 (Ext Data - S1), PB-10 (Pay via Account - S1), PB-12 (Fee Config - S2), PB-13 (Charges - S2) |
| **R4** | Students with financial needs apply for FAS. Multiple schemes (MOEFAS auto-granted by rules + income API; SBFAS granted by School users). Reflected in payable fees. | `Admin & e-Service` | **US-05 (FR5), US-AI1 (FR5-AI)** | PB-17 (Scheme Config - S3), PB-19 (Assess Subsidies - S3), PB-25 (ML Risk Tiers - Unscheduled) |
| **R5** | Support capturing and processing hardcopy FAS applications filled offline by parents and entered by School users. | `Admin Portal` | **US-06 (FR6)** | PB-20 (Sprint 3) |
| **R6** | MOE HQ users set budget & track MOEFAS statistics. School users set budget & track SBFAS statistics. | `Admin Portal` | **US-07 (FR7)** | PB-21 (Sprint 3) |
| **R7** | MOE HQ users can simulate how School users and Parents access and see the system to address queries better. | `Admin Portal` | **US-08 (FR8)** | PB-22 (Unscheduled / Trade-off) |
| **R8** | Parents access e-Service portal via SingPass to view education account details, balance, transactions, and update basic personal details (address, contact). | `e-Service Portal` | **US-09 (FR9), US-AI2 (FR9-AI)** | PB-06 (SingPass Login - S1), PB-07 (Parent-Child Link - S1), PB-08 (View Account - S1), PB-15 (Profile Update - S2), PB-23 (AI Chatbot - Unscheduled) |
| **R9** | Parents view outstanding charges and pay fees using Education Account balance or online payment methods. | `e-Service Portal` | **US-10 (FR10)** | PB-09 (View Charges - S1), PB-10 (Pay via Account - S1), PB-11 (Online Payment - S1) |
| **R10** | Parents apply for financial assistance schemes (FAS) as a family unit online. | `e-Service Portal` | **US-11 (FR11), US-AI3 (FR11-AI)** | PB-18 (Family Unit FAS - S3), PB-24 (AI Prefill - Unscheduled) |
| **NFR** | Technical Enabler: Concurrency, capacity, response times, RBAC security, and load testing baseline. | `Cross-cutting` | **N/A** | PB-01 (Capacity Baseline - S1), Admin Login (S1), School Login (S1) |

---

## 3. KẾ HOẠCH PHÂN BỔ SPRINT & TIẾN ĐỘ THỰC THI

### 3.1. So sánh 2 Mô hình Phân bổ Sprint

Khi đối soát giữa `Agile requirements.xlsx` và `Product Backlog.xlsx`, ta phát hiện **sự tiến hóa về mặt chiến lược release** của nhóm dự án:
1. **Mô hình A (Chuẩn theo User Story - `Agile requirements.xlsx`):**
   - **Sprint 1 (Tuần 1):** Chỉ tập trung vào Vòng đời tài khoản (US-01) và Master Data CRUD (US-03) dưới dạng Walking Skeleton.
   - **Sprint 2 (Tuần 2):** Tập trung hoàn toàn vào FAS Rule-based core (US-05), Top-up (US-02), và Budget/Stats (US-07).
   - **Sprint 3 (Tuần 3):** Đẩy toàn bộ Parent Portal (US-09), Thanh toán học phí (US-10, US-04), Nộp đơn FAS gia đình (US-11) và Đơn giấy (US-06) vào tuần cuối.
2. **Mô hình B (Mô hình Backlog Thực thi - `Product Backlog.xlsx`):**
   - Nhóm phát triển và PO đã **kéo toàn bộ trải nghiệm người dùng cuối (Parent SingPass Auth, Xem tài khoản, và đặc biệt là luồng Thanh toán R9)** lên ngay **Sprint 1**.
   - Mục đích: Sớm có bản demo end-to-end cho khách hàng về luồng thanh toán (Payment flow) và xác thực SingPass ngay cuối tuần 1.
   - Đổi lại, việc đóng tài khoản tuổi 16 (PB-16) và cấu hình FAS (PB-17..21) được lùi sang Sprint 3; Cấu hình biểu phí chi tiết (PB-12, PB-13) và Nạp tiền (PB-14) được đưa vào Sprint 2.

### 3.2. Trọng tâm Sprint 1: Walking Skeleton & Thanh toán R9

Trong `Product Backlog.xlsx`, Sprint 1 bao gồm **14 hạng mục công việc** (chiếm 50% tổng số backlog items). Đây là sprint đồ sộ nhất và quyết định sự thành bại của dự án:

| ID PBI | Phân hệ (Epic) | Hạng mục công việc | Đối tượng sử dụng | Cơ sở / Ghi chú kỹ thuật |
|---|---|---|---|---|
| **PB-01** | Technical Enabler | Capacity, concurrency and test baseline | Cross-cutting · Dev / QA | Thiết lập baseline tải dựa trên ước lượng dân số của Client (~500 HQ, 300 trường, 2M phụ huynh). |
| **PB-02** | Core Data | Maintain school, level/cohort, class & student records | Admin · MOE HQ / School | CRUD dữ liệu trường, khối/lớp, học sinh. Phân cấp quyền HQ quản lý tất cả, School quản lý từ khối trở xuống. |
| **PB-03** | Access Control | HQ vs School role-based permissions | Admin · MOE HQ / School | Ma trận phân quyền RBAC phân tách tuyệt đối dữ liệu giữa các trường học. |
| **PB-04** | Core Data | Obtain student data from external source | Backend / Integration | Kết nối / import dữ liệu học sinh từ nguồn định danh ngoài (name, DOB, citizenship, address). |
| **PB-05** | Education Account | Create and activate Education Account at age 7 | Backend / Admin | Tự động tạo và kích hoạt tài khoản tài chính giáo dục khi trẻ đủ 7 tuổi (quốc tịch Singapore). |
| **PB-06** | Parent Portal | Parent authentication via SingPass | e-Service · Parent | Xác thực phụ huynh qua cổng SingPass (dùng môi trường Sandbox/Mock cho demo). |
| **PB-07** | Parent Portal | Authorize parent/guardian to linked children | e-Service · Parent | Phân quyền phụ huynh chỉ được xem đúng hồ sơ con em được liên kết hợp lệ. |
| **PB-08** | Parent Portal | View child account, balance & transactions | e-Service · Parent | Hiển thị thông tin tài khoản giáo dục của con, số dư khả dụng và lịch sử giao dịch. |
| **PB-09** | Parent Portal | View outstanding charges | e-Service · Parent | Phụ huynh xem danh sách các khoản phí nợ trường của con kèm số tiền và hạn nộp. |
| **PB-10** | Payments | Pay eligible charges using Education Account | e-Service / Backend | Khấu trừ số dư tài khoản giáo dục để trả các khoản phí hợp lệ (xử lý atomic balance deduction). |
| **PB-11** | Payments | Pay fees via online payment method | e-Service · Parent | Thanh toán các khoản phí còn lại qua cổng thanh toán trực tuyến (thẻ/ví điện tử). |
| *(Auth-1)* | User Authentication | Admin Portal Login | Admin · MOE HQ / School | Đăng nhập an toàn cho quản trị viên MOE HQ và nhân viên nhà trường. |
| *(Auth-2)* | User Authentication | Parent Login via SingPass | e-Service · Parent | Cổng đăng nhập OIDC/SAML SingPass cho phụ huynh. |
| *(Auth-3)* | User Authentication | School User Login | Admin · MOE HQ / School | Đăng nhập phân quyền theo từng đơn vị trường học. |

> [!WARNING] Cảnh báo Rủi ro Cực kỳ Cao trong Sprint 1 (Sprint Planning Risk):
> Backlog đã cảnh báo rõ ràng: *'High risk: Sprint 1 targets all R9 options but charge source/payment gateway, account ledger and business rules remain unresolved.'*
> Cụ thể: Việc triển khai tính năng thanh toán (PB-10, PB-11) và xem công nợ (PB-09) trong Sprint 1 phụ thuộc vào **khoản phí phải thu (PB-13)** và **cấu hình phí (PB-12)** vốn đang được lên lịch ở **Sprint 2**. Do đó, trong Sprint 1, team bắt buộc phải sử dụng **bộ dữ liệu giả lập (Test/Imported charge fixtures)** và **Mock Payment Gateway** để demo, thay vì tích hợp production thật.

### 3.3. Kế hoạch Sprint 2 & Sprint 3

#### A. Sprint 2: Hoàn thiện Biểu phí, Nạp tiền & Hồ sơ Phụ huynh (4 items)
| ID PBI | Phân hệ (Epic) | Hạng mục công việc | Đối tượng | Mục tiêu bàn giao |
|---|---|---|---|---|
| **PB-12** | Fee Management | Maintain fee types and components | Admin · MOE HQ / School | Quản lý danh mục loại phí và thành phần phí (học phí, phụ phí, hoạt động ngoại khóa, tái sử dụng component GST). |
| **PB-13** | Fee Management | Create/record payable charges for students | Admin / Backend | Cơ chế tạo/ghi nhận khoản phí phát sinh cho từng học sinh (chuyển giao từ nguồn ghi nợ chính thức). |
| **PB-14** | Top-Up | MOE HQ individual & batch Education Account top-up | Admin · MOE HQ | Phân hệ nạp tiền định kỳ hoặc đột xuất theo lô dựa trên cấu hình quy tắc (độ tuổi, số dư, tình trạng đi học) và audit log. |
| **PB-15** | Parent Portal | Update editable personal details | e-Service · Parent | Cho phép phụ huynh chỉnh sửa các trường thông tin được phép (địa chỉ liên lạc, số điện thoại, email) có kiểm soát. |

#### B. Sprint 3: Đóng tài khoản tuổi 16 & Quy trình Trợ cấp Tài chính FAS (6 items)
| ID PBI | Phân hệ (Epic) | Hạng mục công việc | Đối tượng | Mục tiêu bàn giao |
|---|---|---|---|---|
| **PB-16** | Education Account | Close Education Account at age 16 | Backend / Admin | Tự động đóng tài khoản khi trẻ đủ 16 tuổi, đối soát giao dịch và chuyển toàn bộ số dư còn lại sang tài khoản CPF của công dân. |
| **PB-17** | FAS | Configure FAS schemes, criteria and subsidy tiers | Admin · MOE HQ / School | Cấu hình các gói trợ cấp (MOEFAS toàn quốc, SBFAS cấp trường), các ngưỡng thu nhập hộ gia đình và tỷ lệ miễn giảm theo thành phần phí. |
| **PB-18** | FAS | Online FAS application by family unit | e-Service · Parent | Phụ huynh nộp đơn xin trợ cấp trực tuyến gộp chung cho toàn bộ con em trong cùng đơn vị hộ gia đình. |
| **PB-19** | FAS | Assess FAS and apply approved subsidies | Admin / Backend | Động cơ thẩm định quy tắc MOEFAS tự động qua API thu nhập; hỗ trợ nhà trường duyệt SBFAS thủ công và tự động giảm trừ vào công nợ học phí. |
| **PB-20** | FAS | School entry of offline FAS applications | Admin · School | Cho phép văn phòng nhà trường nhập dữ liệu từ đơn giấy do phụ huynh nộp offline, tích hợp cơ chế chống trùng lặp với đơn online. |
| **PB-21** | FAS / Reporting | Set and track MOEFAS / SBFAS budgets | Admin · MOE HQ / School | Thiết lập hạn mức ngân sách trợ cấp theo năm/kỳ và theo dõi thống kê giải ngân thực tế so với ngân sách. |

### 3.4. Nhóm Hạng mục Hậu MVP (Unscheduled / Deferred AI & ML)

Nhóm bao gồm **4 hạng mục** được đánh dấu `Unscheduled / trade-off` trong `Product Backlog.xlsx` và `Deferred (sau MVP)` trong `Agile requirements.xlsx`. Đây là các tính năng giá trị gia tăng, đòi hỏi dữ liệu huấn luyện hoặc quyết định phạm vi bổ sung từ phía Khách hàng:

| ID PBI | Story ID | Tên tính năng | Bản chất kỹ thuật | Lý do trì hoãn (Trade-off Rationale) |
|---|---|---|---|---|
| **PB-22** | US-08 | Simulate school/parent view for support | Giả lập giao diện (Impersonation/Read-only view) cho MOE HQ | Tiềm ẩn rủi ro bảo mật dữ liệu riêng tư cá nhân (PII); cần chốt cơ chế audit trail và quyền read-only trước khi làm. |
| **PB-23** | US-AI2 | AI conversational help for e-Service users | Trợ lý ảo AI Chatbot hỏi đáp tính năng cổng phụ huynh | Cần chuẩn bị kho dữ liệu tri thức (Knowledge Base) đã được phê duyệt, prompt engineering và kịch bản hỏi ngược (follow-up). |
| **PB-24** | US-AI3 | AI-assisted FAS application prefill | Tự động điền đơn xin trợ cấp FAS bằng AI | Phụ thuộc vào việc triển khai hoàn tất form FAS (PB-18) và chatbot (PB-23); cần cơ chế consent và kiểm tra tính chính xác của dữ liệu sinh ra. |
| **PB-25** | US-AI1 | Predict financial difficulty risk tiers (ML) | Mô hình Học máy phân loại rủi ro tài chính (Low/Med/High) | Thiếu tập dữ liệu lịch sử có nhãn (Historical labeled dataset); cần kiểm thử độ chuẩn xác và tuân thủ nguyên tắc Human-in-the-loop. |

### 3.5. Hiện trạng Ước lượng (Story Points / Estimation)

- **Hiện trạng dữ liệu:** Trong cột `Estimate SP (update)` của file `Product Backlog.xlsx`, **toàn bộ giá trị hiện đang để trống (Blank)**. Tại cột `Readiness`, các PBI được gắn cờ `Needs team estimate` hoặc `Needs AC`.
- **Giải thích quy trình Agile:** Đây là thiết kế có chủ đích theo chuẩn Scrum. File `Read Me` quy định rõ: *'Dev updates backlog columns K (Dev Status), L (Owner), M (Estimate SP), Q (Notes). Change G (Target Sprint) only after team reprioritization.'* PO và BA chỉ đưa ra đề xuất phạm vi (Proposed sprint allocation), còn việc ước lượng Story Points (bằng Planning Poker hoặc T-shirt sizing) thuộc toàn quyền của Đội ngũ Phát triển (Developers) trong buổi họp Sprint Planning.
- **Khuyến nghị ước lượng sơ bộ (Indicative SP Reference):**
  - *PBI độ phức tạp thấp (1–2 SP):* Admin Login, School Login, Parent SingPass Login (nếu mock), PB-01 (Capacity baseline doc).
  - *PBI độ phức tạp trung bình (3–5 SP):* PB-02, PB-03, PB-05, PB-07, PB-08, PB-09, PB-12, PB-14, PB-15, PB-20.
  - *PBI độ phức tạp cao / rủi ro tích hợp (8–13 SP):* PB-04 (Tích hợp dữ liệu công dân nguồn), PB-10 (Giao dịch trừ số dư nguyên tử), PB-11 (Cổng thanh toán trực tuyến & webhook), PB-13 (Cơ chế tính toán và tạo công nợ), PB-16 (Đóng tài khoản & đối soát CPF), PB-17/19 (Động cơ thẩm định quy tắc FAS đa tầng).

---

## 4. MA TRẬN PHÂN BỔ TÍNH NĂNG THEO PORTAL (ADMIN VS E-SERVICE)

Hệ thống được thiết kế theo kiến trúc tách biệt rõ ràng giữa cổng vận hành quản trị (Admin Portal) và cổng dịch vụ công cộng cho công dân (e-Service Portal):

| Phân hệ / Epic | Tính năng cụ thể | Admin Portal (MOE HQ / School) | e-Service Portal (Parent / Guardian) | Vai trò sử dụng chính | Ghi chú phạm vi & Quy tắc ranh giới |
|---|---|:---:|:---:|---|---|
| **Xác thực & Truy cập** | Đăng nhập Quản trị viên | **Có** | - | MOE HQ, School Staff | Xác thực tài khoản công vụ, phân quyền theo vai trò (HQ vs School). |
| | Đăng nhập Phụ huynh | - | **Có** | Phụ huynh / Người giám hộ | Bắt buộc xác thực qua SingPass; chỉ phụ huynh hợp lệ mới được truy cập. |
| | Phân quyền Phụ huynh - Con | - | **Có** | Phụ huynh | Bảo mật dữ liệu: Phụ huynh chỉ thấy con mình được liên kết, tuyệt đối không thấy học sinh khác. |
| **Dữ liệu Nguồn (Core)** | Quản lý Trường, Khối/Lớp, Học sinh | **Có** | - | MOE HQ, School Staff | HQ quản lý toàn diện; School chỉ quản lý học sinh và lớp thuộc phạm vi trường mình. |
| | Đồng bộ Dữ liệu Công dân | **Có** (Backend) | - | Hệ thống / Quản trị | Thu nhận dữ liệu định danh từ cơ quan chức năng (Name, DOB, NRIC, Citizenship, Address). |
| **Tài khoản Giáo dục** | Tự động mở tài khoản lúc 7 tuổi | **Có** (Backend) | - | Hệ thống / MOE HQ | Tự động kích hoạt khi công dân Singapore đủ 7 tuổi; tách biệt với tình trạng đi học. |
| | Tự động đóng tài khoản lúc 16 tuổi | **Có** (Backend) | - | Hệ thống / MOE HQ | Tự động đóng khi đủ 16 tuổi; chuyển số dư sang CPF (không cho phép giao dịch tồn đọng). |
| | Xem tài khoản, số dư & giao dịch | - | **Có** | Phụ huynh | Phụ huynh theo dõi biến động số dư và sao kê các khoản chi tiêu của con. |
| | Nạp tiền (Top-Up) theo lô & ad-hoc | **Có** | - | MOE HQ | Chức năng độc quyền của MOE HQ; cấu hình quy tắc theo độ tuổi, số dư, trạng thái học tập. |
| **Quản lý Học phí** | Định nghĩa Loại phí & Thành phần phí | **Có** | - | MOE HQ, School Staff | Thiết lập cấu trúc phí; hỗ trợ tái sử dụng thành phần thuế GST chung cho nhiều loại phí. |
| | Tạo & Phân bổ Công nợ Học sinh | **Có** | - | Kế toán Trường / Backend | Ghi nhận các khoản phí phải nộp (học phí, phụ phí, hoạt động ngoại khóa, tiền bồi thường hư hại). |
| | Xem Các khoản phí còn nợ | - | **Có** | Phụ huynh | Hiển thị chi tiết từng khoản nợ, hạn thanh toán và trạng thái công nợ. |
| **Thanh toán Học phí** | Thanh toán bằng Số dư TK Giáo dục | - | **Có** | Phụ huynh | Khấu trừ trực tiếp số dư được cấp để trả học phí hợp lệ. |
| | Thanh toán qua Cổng trực tuyến | - | **Có** | Phụ huynh | Thanh toán số tiền còn thiếu qua thẻ ngân hàng, PayNow hoặc ví điện tử. |
| **Hồ sơ Cá nhân** | Cập nhật Thông tin Phụ huynh | - | **Có** | Phụ huynh | Cập nhật địa chỉ nhận thư, SĐT, email (địa chỉ cư trú cố định có thể lấy từ MyInfo). |
| **Trợ cấp Tài chính (FAS)**| Cấu hình Quy tắc & Hạn mức Scheme | **Có** | - | MOE HQ, School Staff | Cấu hình tiêu chí MOEFAS (thu nhập hộ gia đình) và SBFAS (quy tắc cấp trường). |
| | Nộp Đơn Trợ cấp Trực tuyến | - | **Có** | Phụ huynh | Đăng ký theo Đơn vị Gia đình (Family Unit) - đánh giá một lần cho tất cả các con. |
| | Nhập Đơn Trợ cấp Bản giấy (Offline) | **Có** | - | Nhân viên Trường | Hỗ trợ phụ huynh không có điều kiện trực tuyến; hệ thống kiểm tra chống nộp trùng. |
| | Thẩm định & Giảm trừ Học phí | **Có** | - | Hệ thống / School Staff | MOEFAS duyệt tự động bằng rule; SBFAS do nhà trường xét duyệt; tự động giảm trừ công nợ. |
| | Quản lý Ngân sách & Thống kê FAS | **Có** | - | MOE HQ, School Staff | HQ giám sát ngân sách toàn quốc; Trường kiểm soát ngân sách quỹ hỗ trợ của trường. |
| **Hỗ trợ & AI** | Giả lập Giao diện Hỗ trợ (Simulation)| **Có** | - | MOE HQ Support | Giúp đội ngũ hỗ trợ nhìn thấy màn hình của trường/phụ huynh để hướng dẫn xử lý lỗi. |
| | Trợ lý Ảo AI Chatbot | - | **Có** | Phụ huynh | Trả lời thắc mắc, tự động đặt câu hỏi làm rõ (dynamic follow-up questions). |
| | AI Điền Đơn FAS Tự động | - | **Có** | Phụ huynh | Tự động trích xuất thông tin hồ sơ và đoạn chat để điền sẵn vào đơn trợ cấp. |
| | AI/ML Phân loại Rủi ro Tài chính | **Có** | - | Hội đồng Duyệt Trường | Đưa ra gợi ý mức rủi ro (Low/Med/High) và đề xuất gói SBFAS phù hợp. |

---

## 5. PHÂN TÍCH BẢNG CÂU HỎI & QUYẾT ĐỊNH CỦA KHÁCH HÀNG (QUESTIONNAIRE & DECISIONS)

### 5.1. 12 Quyết định & Làm rõ Cốt lõi của Khách hàng (Client Decisions CD-01 đến CD-12)

Trong sheet `Client Decisions` của `Product Backlog.xlsx`, 12 sự thật và quyết định nghiệp vụ then chốt từ cuộc họp kickoff đã được chuẩn hóa kèm trích dẫn timestamp:
#### **[CD-01] Education Account is a financial/spending account, NOT a user login account; Singapore Citizens can have it. PR/foreign students may attend schools without one.**
- **Tác động tới Dev & QA:** Model education account separately from portal identity; fees exist for students without Education Accounts.
- **Nguồn chứng cứ & Độ tin cậy:** `Mtg 15:03–16:30` | **Client explicitly clarified**

#### **[CD-02] Education Account balance should transfer to CPF at closure; the client expects no pending transactions.**
- **Tác động tới Dev & QA:** Plan closure/CPF workflow; pending transaction handling needs additional design confirmation.
- **Nguồn chứng cứ & Độ tin cậy:** `Mtg 11:19–12:13` | **Client explicitly clarified**

#### **[CD-03] Student source fields suggested: name, date of birth, citizenship, address where available.**
- **Tác động tới Dev & QA:** Use these as candidate integration fields; actual API payload, identifiers and address availability remain open.
- **Nguồn chứng cứ & Độ tin cậy:** `Mtg 12:58–13:15` | **Client explicitly clarified**

#### **[CD-04] Level and cohort mean essentially the same thing; class is a separate dimension.**
- **Tác động tới Dev & QA:** Avoid creating independent Level and Cohort concepts without a need.
- **Nguồn chứng cứ & Độ tin cậy:** `Mtg 18:06–18:27` | **Client explicitly clarified**

#### **[CD-05] MOE HQ should manage all listed records; School users can edit from level down.**
- **Tác động tới Dev & QA:** Start access design with this restriction; precise row-level scope still needs definition.
- **Nguồn chứng cứ & Độ tin cậy:** `Mtg 18:33–19:03` | **Client explicitly clarified**

#### **[CD-06] School enrollment/schooling status and Education Account status are distinct.**
- **Tác động tới Dev & QA:** Do not automatically open/close the Education Account on school transfer/enrollment status.
- **Nguồn chứng cứ & Độ tin cậy:** `Mtg 19:03–19:59` | **Client explicitly clarified**

#### **[CD-07] Shared GST fee component was welcomed if feasible, rather than strictly required.**
- **Tác động tới Dev & QA:** Treat component reuse as an enhancement/implementation choice, not a mandatory Sprint 2 contract.
- **Nguồn chứng cứ & Độ tin cậy:** `Mtg 20:17–22:03` | **Client expressed preference**

#### **[CD-08] Fee examples: school/miscellaneous fees, ad hoc activities and damage charges.**
- **Tác động tới Dev & QA:** Fee data model should support more than one recurring monthly tuition fee.
- **Nguồn chứng cứ & Độ tin cậy:** `Mtg 22:33–23:53` | **Client gave examples**

#### **[CD-09] Client estimates ~500 HQ users, ~300 schools, ~200 School users each, ~2M possible parents; these are NOT concurrency numbers.**
- **Tác động tới Dev & QA:** Dev/QA must propose and validate concurrent load targets rather than treating population as simultaneous sessions.
- **Nguồn chứng cứ & Độ tin cậy:** `Mtg 24:52–25:38` | **Client estimate only**

#### **[CD-10] HQ/school activity roughly 08:00–19:00; parent portal access around 06:00–02:00; usage may spike around payment dates.**
- **Tác động tới Dev & QA:** Use for preliminary load profile, not fixed availability/peak SLA.
- **Nguồn chứng cứ & Độ tin cậy:** `Mtg 26:25–27:17` | **Client estimate only**

#### **[CD-11] The client considered the high-level modules broadly present, but said it was too early to confirm detailed design.**
- **Tác động tới Dev & QA:** Do not treat overview diagrams or BA assumptions as full sign-off.
- **Nguồn chứng cứ & Độ tin cậy:** `Mtg 07:39–08:02` | **Explicit non-approval**

#### **[CD-12] Team proposed Sprint 1 focus on IR #1/#3/#8/#9; client said this was acceptable while questioning backend availability.**
- **Tác động tới Dev & QA:** Sprint 1 scope here is a proposal and must still be estimated/selected by Developers.
- **Nguồn chứng cứ & Độ tin cậy:** `Mtg 08:47–11:15` | **Proposed scope discussed**

---

### 5.2. Bảng 30 Câu hỏi Clarification trong Updated Questionaire

Sheet `Updated Questionaire` trong `Questionaire.xlsx` ghi nhận **30 câu hỏi làm rõ khoảng trống yêu cầu**. Dưới đây là bảng tổng hợp toàn bộ 30 câu hỏi kèm trạng thái và phản hồi chính thức của Khách hàng:

| ID | Vấn đề / Khoảng trống (Gap) | Đề xuất của Team (Solution) | Câu hỏi gửi Khách hàng (Clarification Question) | Trạng thái | Quyết định / Phản hồi của Khách hàng |
|---|---|---|---|---|---|
| **1.0** | Eligibility: Additional eligibility criteria are unclear. | Use citizenship and age as primary criteria. | Apart from citizenship and age, are school enrolment or Singapore residency required? | **`Open`** | *Chưa phản hồi (Đang mở)* |
| **2.0** | Existing Eligible Citizens: Handling of eligible citizens without accounts is undefined. | Create accounts for eligible citizens without existing accounts. | Should eligible citizens aged 8–15 without accounts be automatically registered? | **`Open`** | *Chưa phản hồi (Đang mở)* |
| **3.0** | Citizenship Updates: Effective date of account changes is unclear. | Reevaluate eligibility upon receiving citizenship updates. | Should account changes take effect on the citizenship change date or the processing date? | **`Open`** | *Chưa phản hồi (Đang mở)* |
| **4.0** | Account Closure: Remaining balances and pending transactions are undefined. | Apply the agreed balance and transaction handling rules. | What happens to remaining balances and pending transactions when an account closes? | **`Resolved`** | Client confirmed that there should be no pending transactions at account closure, and any remaining balance should be transferred to CPF. |
| **5.0** | Data Source: Authoritative citizen data source is unspecified. | Simulate an authorized data source, potentially Myinfo, using mock data. | Which data source should provide and update citizen information? | **`Partly`** | các trường dữ liệu có thể lấy: name, date of birth, citizenship và address nếu có. |
| **6.0** | Data Storage & Sync: Permitted data storage and update frequency are unclear. | Store essential data and perform daily synchronization, subject to approval. | Which personal data can be stored, and how frequently must it be updated? | **`Open`** | *Chưa phản hồi (Đang mở)* |
| **7.0** | Parent–Child Relationship: Source of verified relationships is unclear. | Use mock verified relationship data for Parent authorization. | Can the data source provide verified Parent/Guardian relationships? | **`Open`** | *Chưa phản hồi (Đang mở)* |
| **8.0** | Unclear definitions and relationships between School, Level, Cohort, Class, and Student. | Confirm definitions and build an ERD illustrating the data relationships. | Could you clarify the definitions of Level and Cohort and their relationships with School, Class and Student? | **`Resolved`** | Client làm rõ rằng: - Level và Cohort có thể được dùng tương đương tùy cách gọi của trường. - Class là khái niệm riêng biệt. |
| **9.0** | Unclear rules for class assignment, class transfers, school transfers, and progression to the next academic year. | Define the enrollment lifecycle and record class/academic year history as needed. | How should student transfers, class changes and progression to a new academic year be handled? Is historical enrollment required? | **`Open`** | *Chưa phản hồi (Đang mở)* |
| **10.0** | Unclear data management scope between MOE HQ and School users. | Establish a permissions matrix by role and school scope. | What permissions should MOE HQ and School users have? Can School users access and manage only their own school's data? | **`Resolved`** | Client đã nêu phạm vi tổng quát: - MOE HQ users: quản lý tất cả records liên quan. - School users: quản lý records thuộc phạm vi trường mình, ở level của trường và các level bên dưới. |
| **11.0** | Unclear who can create and manage Fee Types/Fee Components: MOE HQ, School, or both. | Determine ownership and responsibilities for each role. | Who is responsible for creating and maintaining Fee Types and Fee Components: MOE HQ, School users, or both? | **`Need confirm`** | có lẽ cho cả 2 đều có thể take responsible cho việc creating và maintaining fee type & fee components |
| **12.0** | List and definitions of Fee Component types have not been defined. | Collect component catalog, definitions, attributes, and real-world examples. | What Fee Component types must be supported? Could you provide their definitions and examples? | **`Partly`** | Client đã đưa ví dụ: - School fees. - Miscellaneous fees. - Extracurricular activities, music classes và school trips. - Ad hoc charges, ví dụ làm hư hỏng tài sản lớp học. Một số khoản phí chỉ áp dụng cho một level hoặc class nhất định. Danh mục đầy đủ và các thuộc tính bắt buộc của từng component chưa được xác nhận. |
| **13.0** | Unclear relationship between Fee Type and Fee Component. | Define cardinality, reusability, and fee data structure. | Can one Fee Type contain multiple Fee Components? Can a component be reused across multiple Fee Types? | **`Resolved`** | Client confirmed that common fee components, such as GST, should be reusable across multiple Fee Types. |
| **14.0** | Unclear restrictions on permissions to create, edit, and deactivate each fee type by role. | Build a permission matrix by role, fee type, and data scope. | Are there restrictions on which Fee Types or Components each role can create, update or deactivate? Is approval required for fee changes? | **`Open`** | *Chưa phản hồi (Đang mở)* |
| **15.0** | Unclear whether fees are applied by school, class, education level, student, or academic year. | Define eligibility/applicability rules and how fees are assigned to target subjects. | Are fees configured centrally or per school? What determines which fees apply to each student? | **`Open`** | *Chưa phản hồi (Đang mở)* |
| **16.0** | Unclear eligibility conditions for Singaporean students to use the Education Account. | Define eligibility rules and validate before permitting payment. | Does eligibility depend solely on Singaporean nationality, or are there additional eligibility criteria? | **`Resolved`** | Client làm rõ rằng Education Account là tài khoản phục vụ chi phí giáo dục do chính phủ tài trợ, không phải tài khoản đăng nhập. PR và foreign students vẫn có thể đi học mà không có Education Account và có thể phải tự trả học phí. Điều kiện của Education Account và FAS là hai bộ tiêu chí riêng. |
| **17.0** | Unclear handling when the Education Account balance is insufficient to pay fees. | Confirm whether partial payment or paying the remaining amount via another method is allowed. | What should happen when the available balance is insufficient? Should partial payment or another payment method be allowed? | **`Open`** | *Chưa phản hồi (Đang mở)* |
| **18.0** | Unclear requirements for transaction history retention and payment audit trails. | Define transaction history, audit fields, and retention period. | Is a transaction history or audit trail required? What information and retention period are needed? | **`Open`** | *Chưa phản hồi (Đang mở)* |
| **19.0** | Unclear whether an audit trail is required for master data changes. | Define data to log, actor, timestamp, and pre/post-change values. | Do you require an audit trail for master data changes? | **`Open`** | *Chưa phản hồi (Đang mở)* |
| **20.0** | The scope of outstanding charges, payment due dates, and transaction display format are not clearly defined. | Define the charge categories, due date rules, and whether charges should be displayed per child or consolidated at the parent account level. | What does “outstanding charges” include (school fees, miscellaneous fees, enrichment activities)? What are the payment due dates, and should charges be displayed per child or combined? | **`Partly`** | Đã có ví dụ về các loại khoản phí, gồm school fees, miscellaneous fees, extracurricular activities/trips và ad hoc charges. Tuy nhiên, chưa xác nhận: - Payment due dates. - Outstanding charges hiển thị theo từng child hay tổng hợp cho parent. - Cách trình bày chi tiết trên giao diện |
| **21.0** | The supported online payment methods and payment gateway have not been specified. | Confirm the supported payment methods and select the payment gateway based on business, technical, and security requirements. | Which online payment methods are in scope (card, Visa, Amex), and which payment gateway will be used? | **`Open`** | *Chưa phản hồi (Đang mở)* |
| **22.0** | The processes for failed payments, refunds, and responsibility assignment are unclear. | Define the payment failure and refund workflows, responsible parties, refund eligibility, and refund destination rules. | When a payment fails, or a refund is needed, what is the process and who is responsible? Should refunds go back to the education account balance or to the original payment source? | **`Open`** | *Chưa phản hồi (Đang mở)* |
| **23.0** | The display of fees after Financial Assistance Scheme (FAS) reductions is not specified. | Define how the original fee, FAS reduction, and final payable amount should be displayed to ensure transparency. | How should a fee that has been reduced by FAS be displayed, and does the original amount also need to be shown? | **`Open`** | *Chưa phản hồi (Đang mở)* |
| **24.0** | The requirement does not clarify whether the residential address should be retrieved from MyInfo through Singpass and displayed as read-only, where applicable. | Clarify the MyInfo integration scope, address retrieval rules, and whether the retrieved address should be read-only. | When users log in using Singpass, should the residential address be retrieved from MyInfo and displayed as read-only? What does “where applicable” mean in this context? | **`Open`** | *Chưa phản hồi (Đang mở)* |
| **25.0** | The requirement does not specify the escalation process when the AI assistant cannot answer a parent's question. | Define the escalation flow and available support channels, such as live chat, email, hotline, or support ticket. | When the AI assistant cannot answer a question, which support channel should parents be directed to? | **`Open`** | *Chưa phản hồi (Đang mở)* |
| **26.0** | The content owner and approval process for the information used by the AI assistant are not defined. | Define content ownership, approval responsibilities, and the process for updating outdated information. | Who will be responsible for providing, reviewing, and approving the content used by the AI assistant to answer users' questions? | **`Open`** | *Chưa phản hồi (Đang mở)* |
| **27.0** | The test dataset and evaluation criteria for validating the AI assistant's response accuracy are not specified. | Obtain a test question set and define the evaluation methodology, scoring criteria, and acceptance threshold. | Can the client provide a set of test questions before 21 October? How will the target of 90% response accuracy be measured and evaluated? | **`Open`** | *Chưa phản hồi (Đang mở)* |
| **28.0** | The transaction history retention period and PDF statement download requirements are unclear. | Define the transaction history period, available transaction details, and whether PDF statement generation is required. | How far back should parents be able to view their transaction history? Is downloading transaction statements in PDF format required? | **`Open`** | *Chưa phản hồi (Đang mở)* |
| **29.0** | The fields included in “basic personal details, etc.” are not explicitly listed. | Confirm the complete list of personal information fields and specify which fields users can view or edit. | Which fields are included in “basic personal details, etc.” beyond residential address, mailing address, mobile number, and email address? Which fields can users edit? | **`Open`** | *Chưa phản hồi (Đang mở)* |
| **30.0** | The verification requirements for updated mobile numbers and email addresses are not specified. | Confirm the verification rules and identify any required SMS or email service integrations. | Do updated mobile numbers and email addresses require OTP verification? If so, should verification be performed through SMS, email, or both? | **`Open`** | *Chưa phản hồi (Đang mở)* |

#### Tổng hợp Phân loại Trạng thái của 30 Câu hỏi:
- **Đã giải quyết dứt điểm (Resolved - 5 items):**
  1. **Q04 (Đóng tài khoản):** Khách hàng chốt không có giao dịch pending khi đóng tài khoản; số dư thừa chuyển sang CPF.
  2. **Q08 (Định nghĩa Level & Cohort):** Khách hàng làm rõ Level và Cohort có thể dùng tương đương nhau tùy cách gọi của trường; Class là khái niệm riêng biệt.
  3. **Q10 (Phân quyền dữ liệu):** MOE HQ quản lý toàn bộ records; School users chỉ quản lý records thuộc trường mình, từ cấp level trở xuống.
  4. **Q13 (Tái sử dụng Component phí):** Thành phần phí dùng chung như thuế GST có thể được tái sử dụng qua nhiều loại phí khác nhau.
  5. **Q16 (Bản chất Tài khoản Giáo dục):** Education Account là tài khoản tài trợ tài chính của chính phủ, KHÔNG PHẢI tài khoản đăng nhập. Học sinh PR và người nước ngoài không có tài khoản này nhưng vẫn đi học và đóng học phí bình thường.
- **Đã làm rõ một phần (Partly Resolved - 3 items):**
  1. **Q05 (Trường dữ liệu nguồn học sinh):** Client gợi ý lấy Name, DOB, Citizenship, Address (chưa chốt API và format chuẩn).
  2. **Q12 (Danh mục các loại phí):** Client đưa ra ví dụ (học phí, phụ phí, hoạt động ngoại khóa, dã ngoại, bồi thường hư hại), nhưng danh mục chính thức chưa chốt.
  3. **Q20 (Phạm vi công nợ):** Đã có ví dụ về loại phí nhưng chưa chốt ngày đến hạn (due dates) và cách hiển thị công nợ gom theo phụ huynh hay riêng từng con.
- **Cần xác nhận thêm (Need confirm - 1 item):**
  1. **Q11 (Trách nhiệm quản lý biểu phí):** Đang nghiêng về phương án cả HQ và School đều có quyền tạo/quản lý phí theo phân cấp.
- **Còn mở hoàn toàn (Open - 21 items):** Tập trung vào quy tắc eligibility chi tiết (Q01-Q03), tần suất sync dữ liệu (Q06), nguồn xác thực quan hệ cha-con (Q07), quy trình chuyển trường/lên lớp (Q09), xử lý khi thiếu số dư (Q17), đối soát và log audit (Q18-Q19), cổng thanh toán và hoàn tiền (Q21-Q22), MyInfo read-only (Q24), các kịch bản AI (Q25-Q27), xuất sao kê PDF (Q28), các trường hồ sơ cá nhân và xác thực OTP (Q29-Q30).

---

### 5.3. 17 Câu hỏi Mở Ưu tiên Cao trong Product Backlog (Open Questions OQ-01 đến OQ-17)

Sheet `Open Questions` trong `Product Backlog.xlsx` lọc ra **17 câu hỏi trọng yếu**, đặc biệt nhấn mạnh các câu hỏi có mức độ khẩn cấp `P1 - Now` cần phải mang ra chốt dứt điểm với khách hàng trong buổi họp 30 phút sáng thứ Hai:

| ID | Mức khẩn cấp | Cho Sprint | Câu hỏi làm rõ / Quyết định còn thiếu | Lý do cần thiết cho Dev / QA | PBI liên quan |
|---|---|---|---|---|---|
| **OQ-01** | **P1 - Now** | `Sprint 1` | What is the authoritative student data source/API, identifier, refresh frequency and data schema? | Cannot trust account eligibility or link source records. | `PB-04, PB-05` |
| **OQ-02** | **P1 - Now** | `Sprint 1` | Where do trusted guardian relationships come from, and which parents/guardians may access each child? | Security and access-control design must be testable. | `PB-04, PB-07` |
| **OQ-03** | **P1 - Now** | `Sprint 1` | Is SingPass test/sandbox access available, and which identifier maps to a parent? | Parent demo/integration feasibility. | `PB-06, PB-07` |
| **OQ-04** | **P1 - Now** | `Sprint 1` | What is the authoritative source of outstanding charges? For Sprint 1, is a test/imported charge dataset acceptable until full billing flow is confirmed? | Blocks R9 view and either payment path; must avoid treating a fixture as production billing. | `PB-13, PB-09, PB-10, PB-11` |
| **OQ-05** | **P1 - Now** | `Sprint 1` | Which data/source is authoritative for Education Account balance and transaction history? | Account balance and transaction source determine whether an Education Account debit can be reliable and testable in Sprint 1. | `PB-05, PB-08, PB-10` |
| **OQ-06** | **P1 - Now** | `Sprint 1` | At age 7, exactly how is account opening triggered? Need backfill / changes to citizenship handling? | Eligibility logic and QA edge cases. | `PB-05` |
| **OQ-07** | **P1 - Now** | `Sprint 1` | Confirm HQ and school user view/edit matrix, including cross-school student records. | Protects school/student data; affects UI and API. | `PB-02, PB-03` |
| **OQ-08** | **P1 - Now** | `Sprint 1` | For Sprint 1 R9 payment demos, which confirmed charge dataset and account balances may be used, and must online payment be live or sandbox? | Clarifies release/demo acceptance without representing mocked transactions as integrated payments. | `PB-09, PB-10, PB-11` |
| **OQ-09** | **P2 - Before Sprint 2** | `Sprint 2` | Which parent profile fields are editable and where are edits synchronized? | Scope and permission for profile update. | `PB-15` |
| **OQ-10** | **P2 - Before Sprint 2** | `Sprint 2` | Which fee types, components and calculation/charging rules are needed? Is shared GST in scope? | Data model and billing rules need examples. | `PB-12, PB-13` |
| **OQ-11** | **P1 - Now** | `Sprint 1` | For R9 Sprint 1, confirm Education Account payment rules (eligible fees, insufficient/partial balance) and online provider/methods, sandbox/API access, callbacks and settlement behavior. | Both R9 payment options target Sprint 1; unconfirmed financial rules/provider may block implementation and QA. | `PB-10, PB-11` |
| **OQ-12** | **P2 - Before Sprint 2** | `Sprint 2` | Exact HQ batch top-up rules, calculation, rerun behavior, authorization and audit? | Prevents unintended duplicate credits. | `PB-14` |
| **OQ-13** | **P2 - Before Sprint 3** | `Sprint 3` | CPF transfer API, reconciliation and what happens if a transaction is still pending at closure? | Closure implementation cannot be specified fully. | `PB-16` |
| **OQ-14** | **P2 - Before Sprint 3** | `Sprint 3` | MOEFAS/SBFAS eligibility thresholds, household definition, income API and approval workflow? | Major dependency for FAS end-to-end. | `PB-17–PB-20` |
| **OQ-15** | **P3 - Later** | `Sprint 3` | Budget periods, reporting breakdown, carry-forward and overspend behavior? | Reporting accuracy and permission scopes. | `PB-21` |
| **OQ-16** | **P1 - Now** | `Sprint 1` | Which AI/ML/support functions are genuinely expected within the three-week delivery? What trade-off is acceptable? | Current breadth is high-risk for capacity and demo commitments. | `PB-22–PB-25` |
| **OQ-17** | **P2 - Before Sprint 2** | `Sprint 1` | What concurrency targets and response-time thresholds should QA test for each portal? | Population estimates are not performance acceptance criteria. | `PB-01` |

> [!IMPORTANT] 7 Câu hỏi Khẩn cấp Cấp độ P1 (Bắt buộc chốt trong buổi họp thứ Hai):
> 1. **OQ-01 (Nguồn dữ liệu học sinh):** API/Schema chính thức của dữ liệu học sinh là gì, tần suất đồng bộ và mã định danh duy nhất?
> 2. **OQ-02 (Quan hệ Phụ huynh - Con):** Dữ liệu quan hệ thân nhân tin cậy được lấy từ đâu để bảo mật quyền truy cập?
> 3. **OQ-03 (Môi trường SingPass Sandbox):** Đã có tài khoản SingPass sandbox để dev/test tích hợp OIDC chưa?
> 4. **OQ-04 (Nguồn dữ liệu công nợ):** Nguồn chính thức của các khoản phí phải thu là gì? Có chấp nhận dùng fixture dữ liệu mẫu cho demo Sprint 1 không?
> 5. **OQ-05 (Nguồn quản lý số dư tài khoản):** Hệ thống nào là nguồn chân lý (Single Source of Truth) của số dư và lịch sử giao dịch tài khoản giáo dục?
> 6. **OQ-08 (Dữ liệu demo thanh toán R9):** Bộ dữ liệu nào được phép dùng để demo thanh toán trong Sprint 1 và cổng thanh toán là giả lập hay sandbox?
> 7. **OQ-11 (Quy tắc trừ tiền và Cổng thanh toán):** Quy tắc xử lý khi thiếu tiền (cho phép trả một phần không?), phương thức thanh toán online nào được hỗ trợ?

---
### 5.4. Bảng câu hỏi chuyên sâu cho Sprint 2

Sheet `Sprint 2` trong `Questionaire.xlsx` chuẩn bị trước các câu hỏi kỹ thuật chuyên sâu cho các tính năng sẽ triển khai trong Sprint 2:
- **F2 (Nạp tiền Top-Up):**
  - *Chu kỳ nạp:* Định kỳ theo mốc thời gian nào trong năm (đầu năm học, theo kỳ hay theo tháng)?
  - *Hạn mức:* Có thiết lập mức trần tối đa cho số dư tài khoản giáo dục hay không?
  - *Bộ lọc giao dịch:* Lịch sử nạp tiền và audit log có thể lọc theo những tiêu chí nào (Trường, Lớp, Học sinh, Khoảng thời gian)?
- **F4 (Thông tin Thu nhập hộ gia đình):**
  - Việc tích hợp API bên thứ ba để lấy thông tin thu nhập chỉ lấy khoảng thu nhập (range) hay con số chính xác? Mối quan hệ giữa dữ liệu bên thứ ba và thông tin phụ huynh tự khai báo trong đơn FAS (F10) là gì?
- **F10 (Hồ sơ đăng ký FAS):**
  - Đơn đăng ký FAS trực tuyến cần chứa những trường thông tin bắt buộc nào? Bằng chứng chứng minh tài chính đi kèm gồm những gì?

---

## 6. NHẬN ĐỊNH RỦI RO, LỖ HỔNG YÊU CẦU & KHUYẾN NGHỊ HÀNH ĐỘNG

### 6.1. Nhận định Rủi ro Kiến trúc & Tiến độ (Architecture & Delivery Risks)

1. **Nghịch lý Phụ thuộc trong Sprint 1 (Sprint 1 Inverted Dependency):**
   - Nhóm đặt mục tiêu demo tính năng thanh toán R9 (PB-10, PB-11) và xem công nợ (PB-09) ngay tuần 1.
   - Tuy nhiên, các phân hệ cốt lõi để tạo ra công nợ như Cấu hình biểu phí (PB-12) và Ghi nhận khoản thu (PB-13) lại được lên lịch ở **Sprint 2**.
   - **Hệ quả:** Nếu không thống nhất rõ ràng với khách hàng, đội ngũ sẽ bị sa lầy vào việc cố gắng xây dựng toàn bộ hệ thống hóa đơn/kế toán trong Sprint 1, dẫn đến nguy cơ vỡ tiến độ.
2. **Bẫy Ngộ nhận Tích hợp Ngoài (External Integration Pitfall):**
   - Cả 3 cổng tích hợp lớn: **SingPass** (OIDC), **Cơ sở dữ liệu Công dân/Học sinh**, và **Cổng Thanh toán (Payment Gateway)** hiện đều chưa có thông tin kết nối, tài liệu API hay môi trường Sandbox.
   - Nếu coi việc tích hợp thật là tiêu chí Done của Sprint 1, sprint này chắc chắn sẽ thất bại.
3. **Rủi ro Dữ liệu Tài chính (Financial Ledger Integrity):**
   - Khách hàng đã khẳng định Education Account là tài khoản tài chính thực (CD-01). Các nghiệp vụ trừ tiền (PB-10), nạp tiền (PB-14), và tất toán chuyển CPF (PB-16) đòi hỏi tính nhất quán dữ liệu cực cao (ACID transactions, tránh double-spending, bảo vệ số dư khi thao tác đồng thời).

### 6.2. Khuyến nghị Kế hoạch Hành động Cụ thể (Actionable Recommendations)

#### A. Cho Buổi họp 30 Phút Sáng Thứ Hai với Khách hàng (Monday Alignment Agenda)
1. **Chốt Phạm vi Demo Sprint 1 (Agreed Demo Boundary):** Thống nhất với Khách hàng rằng buổi Demo Sprint 1 sẽ trình diễn luồng đi xuyên suốt (Walking Skeleton) sử dụng **dữ liệu mẫu đã kiểm duyệt (Pre-approved test fixtures)** cho công nợ học sinh, và **môi trường giả lập (Mock/Stub)** cho SingPass và Cổng thanh toán.
2. **Đóng 7 Câu hỏi Khẩn cấp P1:** Yêu cầu Khách hàng chỉ định đầu mối kỹ thuật (Technical POC) để cung cấp API schema học sinh (OQ-01) và sandbox SingPass (OQ-03).
3. **Chốt Quy tắc Trừ tiền Tài khoản Giáo dục:** Làm rõ việc có cho phép thanh toán từng phần (Partial payment) khi số dư không đủ hay không (OQ-11).

#### B. Cho Đội ngũ Phát triển & QA (Dev & QA Next Steps)
1. **Tổ chức Buổi Sprint Planning & Ước lượng Story Points:** Đội ngũ Dev cần họp ngay để phân tích kỹ thuật cho 14 PBI của Sprint 1, bẻ nhỏ các PBI thành các Technical Tasks và chấm điểm Story Points vào cột M của `Product Backlog.xlsx`.
2. **Thiết kế Contract-First & Mock Services:**
   - Xây dựng Mock SingPass Identity Provider cho môi trường phát triển nội bộ.
   - Thiết kế Schema nội bộ cho Dữ liệu Học sinh và Công nợ (Charge Dataset) để độc lập tiến độ phát triển giao diện và logic.
   - Xây dựng Stub Payment Gateway hỗ trợ các kịch bản thành công, thất bại, và timeout.
3. **Phân tách Rõ ràng Mô hình Dữ liệu Tài chính:** Tách bạch tuyệt đối giữa thực thể Người dùng hệ thống (User/Identity) và Tài khoản tài chính (Education Account/Ledger) đúng theo quyết định CD-01 của Khách hàng.