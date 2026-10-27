#!/usr/bin/env bash
# ==============================================================================
# tools/seed_all_environments.sh - Seed Dữ liệu Toàn diện cho Cả Hai Cổng Local
# 1. Admin Portal (:5173) - Quản trị MOE HQ, Trường học, Biểu phí, Trợ cấp FAS, Thông báo
# 2. Citizen E-Service Portal (:5174) - Phụ huynh SingPass, Học sinh, Ví Edusave, Công nợ & Hóa đơn
# 100% Non-Invasive: Không sửa đổi mã nguồn trong copy/
# ==============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
BACKEND_DIR="$WORKSPACE_DIR/copy/edufams-backend"

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

echo -e "${CYAN}======================================================================${NC}"
echo -e "${CYAN}   SEED DATA TOÀN DIỆN CHO CẢ HAI CỔNG LOCAL (ADMIN & CITIZEN PORTAL)${NC}"
echo -e "${CYAN}======================================================================${NC}"

# 0. Kiểm tra Docker SQL Server
echo -e "\n${YELLOW}[0/5] Kiểm tra Container Database template-sqlserver...${NC}"
if ! docker ps --format '{{.Names}}' | grep -q "^template-sqlserver$"; then
    echo -e "  Khởi động container template-sqlserver..."
    docker start template-sqlserver 2>/dev/null || true
fi

# Đợi SQL Server sẵn sàng
for i in {1..30}; do
    if docker exec template-sqlserver /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "YourStrong@Password123" -C -Q "SELECT 1" > /dev/null 2>&1; then
        echo -e "  ${GREEN}✓${NC} SQL Server đã kết nối thành công."
        break
    fi
    sleep 1
done

run_sql_file() {
    local db_name="$1"
    local file_path="$2"
    local label="$3"

    if [ -f "$file_path" ]; then
        printf "  -> [%-22s] Seeding %s ...\n" "$db_name" "$label"
        docker exec -i template-sqlserver /opt/mssql-tools18/bin/sqlcmd \
            -S localhost -U sa -P "YourStrong@Password123" \
            -d "$db_name" -C -I < "$file_path" > /dev/null 2>&1 || true
    fi
}

run_sql_query() {
    local db_name="$1"
    local query="$2"
    docker exec template-sqlserver /opt/mssql-tools18/bin/sqlcmd \
        -S localhost -U sa -P "YourStrong@Password123" \
        -d "$db_name" -C -I -Q "SET QUOTED_IDENTIFIER ON; SET ANSI_NULLS ON; $query" > /dev/null 2>&1 || true
}

# ==============================================================================
# PHẦN 1: SEED DỮ LIỆU CHO ADMIN PORTAL (:5173)
# ==============================================================================
echo -e "\n${YELLOW}[1/5] Seeding Dữ liệu Admin Portal (:5173) - Trường học & Quản trị...${NC}"

# 1.1 StudentSchoolDatabase (Trường, Khối, Lớp, Niên khóa)
SS_DIR="$BACKEND_DIR/StudentSchoolService/StudentSchoolService.Database/dbo/SeedData"
run_sql_file "StudentSchoolDatabase" "$SS_DIR/01_SeedSchools.sql" "Danh mục trường học"
run_sql_file "StudentSchoolDatabase" "$SS_DIR/02_SeedAcademicYears.sql" "Niên khóa học tập"
run_sql_file "StudentSchoolDatabase" "$SS_DIR/03_SeedAcademicLevels.sql" "Khối lớp (Primary 1-6)"
run_sql_file "StudentSchoolDatabase" "$SS_DIR/04_SeedSchoolLevelOfferings.sql" "Chương trình cấp học"
run_sql_file "StudentSchoolDatabase" "$SS_DIR/05_SeedSchoolClasses.sql" "Danh sách lớp học"
run_sql_file "StudentSchoolDatabase" "$SS_DIR/08_SeedStudents.sql" "Hồ sơ học sinh"
run_sql_file "StudentSchoolDatabase" "$SS_DIR/09_SeedStudentSchoolEnrollments.sql" "Nhập học trường"
run_sql_file "StudentSchoolDatabase" "$SS_DIR/10_SeedStudentClassAssignments.sql" "Phân lớp học sinh"

# 1.2 TemplateIAMDatabase & IAMDatabase (Tài khoản MOE HQ & School Staff)
IAM_DIR="$BACKEND_DIR/IAMService/IAMService.Database/dbo/SeedData"
for target_iam in "TemplateIAMDatabase" "IAMDatabase"; do
    run_sql_file "$target_iam" "$IAM_DIR/01_SeedRoles.sql" "Vai trò phân quyền (Roles)"
    run_sql_file "$target_iam" "$IAM_DIR/02_SeedPermissions.sql" "Quyền hạn hệ thống (Permissions)"
    run_sql_file "$target_iam" "$IAM_DIR/03_SeedRolePermissions.sql" "Gán quyền theo vai trò"
    run_sql_file "$target_iam" "$IAM_DIR/04_SeedUsers.sql" "Người dùng (Admin moehq, School staff)"
    run_sql_file "$target_iam" "$IAM_DIR/05_SeedUserPermissions.sql" "Gán quyền người dùng"
    run_sql_file "$target_iam" "$IAM_DIR/06_SeedEserviceRoles.sql" "Vai trò e-Service"
done

# 1.3 FASDatabase (Chương trình hỗ trợ tài chính FAS & Đơn mẫu)
FAS_DIR="$BACKEND_DIR/FASService/FASService.Database/dbo/SeedData"
run_sql_file "FASDatabase" "$FAS_DIR/05_SeedMoeFasSchemes.sql" "Chương trình MOE FAS"
run_sql_file "FASDatabase" "$FAS_DIR/06_SeedMoeFasSchemeNationalities.sql" "Quốc tịch áp dụng FAS"
run_sql_file "FASDatabase" "$FAS_DIR/07_SeedMoeFasSchemeSubsidies.sql" "Mức trợ cấp MOE FAS"
run_sql_file "FASDatabase" "$FAS_DIR/08_SeedMoeFasSchemeBudgets.sql" "Ngân sách MOE FAS"
run_sql_file "FASDatabase" "$FAS_DIR/09_SeedSbfasSchemes.sql" "Chương trình SBFAS trường"
run_sql_file "FASDatabase" "$FAS_DIR/10_SeedSbfasSchemeNationalities.sql" "Quốc tịch áp dụng SBFAS"
run_sql_file "FASDatabase" "$FAS_DIR/11_SeedSbfasSchemeSubsidies.sql" "Mức trợ cấp SBFAS"
run_sql_file "FASDatabase" "$FAS_DIR/12_SeedSbfasSchemeBudgets.sql" "Ngân sách SBFAS"
run_sql_file "FASDatabase" "$FAS_DIR/01_SeedApplications.sql" "Hồ sơ đăng ký FAS mẫu"
run_sql_file "FASDatabase" "$FAS_DIR/02_SeedApplicants.sql" "Người nộp đơn FAS"
run_sql_file "FASDatabase" "$FAS_DIR/03_SeedBeneficiaries.sql" "Học sinh thụ hưởng FAS"
run_sql_file "FASDatabase" "$FAS_DIR/04_SeedFamilyMembers.sql" "Thành viên gia đình"
run_sql_file "FASDatabase" "$FAS_DIR/13_SeedMoeSchemeApplications.sql" "Đơn đăng ký MOE FAS"
run_sql_file "FASDatabase" "$FAS_DIR/14_SeedSbfasSchemeApplications.sql" "Đơn đăng ký SBFAS"

# 1.4 AnnouncementDatabase (Phòng ban, Khóa học & Thông báo trường)
ANN_DIR="$BACKEND_DIR/AnnouncementService/AnnouncementService.Database/dbo/SeedData"
run_sql_file "AnnouncementDatabase" "$ANN_DIR/01_SeedDepartments.sql" "Phòng ban trường"
run_sql_file "AnnouncementDatabase" "$ANN_DIR/02_SeedClasses.sql" "Lớp học thông báo"
run_sql_file "AnnouncementDatabase" "$ANN_DIR/03_SeedCourses.sql" "Khóa học"
run_sql_file "AnnouncementDatabase" "$ANN_DIR/04_SeedUsers.sql" "Giáo viên & Người dùng"
run_sql_file "AnnouncementDatabase" "$ANN_DIR/05_SeedCourseStudents.sql" "Học sinh khóa học"
run_sql_file "AnnouncementDatabase" "$ANN_DIR/06_SeedAnnouncements.sql" "Bảng tin thông báo"
run_sql_file "AnnouncementDatabase" "$ANN_DIR/07_SeedAnnouncementStudents.sql" "Người nhận thông báo"
run_sql_file "AnnouncementDatabase" "$ANN_DIR/08_SeedWhitelistedEmails.sql" "Email whitelist"

# ==============================================================================
# PHẦN 2: SEED DỮ LIỆU CHO CITIZEN E-SERVICE PORTAL (:5174)
# ==============================================================================
echo -e "\n${YELLOW}[2/5] Seeding Dữ liệu Citizen E-Service Portal (:5174) - Phụ huynh & Ví...${NC}"

# 2.1 EducationAccountDatabase (Tài khoản công dân & Ví Edusave)
EA_DIR="$BACKEND_DIR/EducationAccountService/EducationAccountService.Database/dbo/SeedData"
run_sql_file "EducationAccountDatabase" "$EA_DIR/01_SeedTreasuryAccounts.sql" "Tài khoản Kho bạc Nhà nước"
run_sql_file "EducationAccountDatabase" "$EA_DIR/02_SeedStudentData.sql" "Hồ sơ học sinh Edusave"

# Đồng bộ công dân từ Simulation qua API nếu microservice đang bật
if curl -s "http://localhost:5006/health" > /dev/null 2>&1; then
    printf "  -> Kích hoạt Citizen Sync từ Simulation qua EducationAccountService...\n"
    curl -s -X POST "http://localhost:5006/api/v1/accounts/trigger-citizen-sync" \
        -H "Content-Type: application/json" \
        -H "X-User-Roles: MOEHQ" \
        -H "X-User-Id: system" \
        -d '{"targetFromDob":"2000-01-01","targetToDob":"2026-01-01"}' > /dev/null 2>&1 || true
fi

# Thiết lập liên kết Cha Mẹ - Con Cái & Nạp tiền ví mẫu
printf "  -> Thiết lập liên kết phụ huynh SingPass và nạp tiền ví Edusave...\n"
run_sql_query "EducationAccountDatabase" "
    -- Phụ huynh S7654321B (Tan Wei Ming / PAR-NORMAL-01) liên kết với con Chloe Chan
    UPDATE Students SET father_nric = 'S7654321B' WHERE id = '01a15a22-dddf-750e-ac12-6d155e779d11' OR nric = 'T0000784X';
    
    -- Phụ huynh S7890123F (PAR-NORMAL-02) liên kết với con Tan Wei Ming (S1234567A)
    UPDATE Students SET father_nric = 'S7890123F' WHERE id = '01a15a22-f573-7ba6-93d2-71ac9a4ce40b' OR nric = 'S1234567A';

    -- Phụ huynh S3456789C (PAR-NO-CHILD) không liên kết với học sinh nào đang theo học
    UPDATE Students SET father_nric = 'T1000536X' WHERE nric = 'T0000536X';

    -- Đảm bảo ví Edusave của Chloe Chan có đúng 50.00 SGD (cho test Full EA & Split)
    UPDATE Wallets SET balance = 50.00, status = 1 WHERE student_id = '01a15a22-dddf-750e-ac12-6d155e779d11';

    -- Đảm bảo ví Edusave của Tan Wei Ming có đúng 40.00 SGD
    UPDATE Wallets SET balance = 40.00, status = 1 WHERE student_id = '01a15a22-f573-7ba6-93d2-71ac9a4ce40b';
"

# Đảm bảo tài khoản SingPass có trong IAM Database
for target_iam in "TemplateIAMDatabase" "IAMDatabase"; do
    run_sql_query "$target_iam" "
        IF NOT EXISTS (SELECT 1 FROM users WHERE username = 'S7654321B')
        BEGIN
            INSERT INTO users (id, code, username, email, password_hash, provider, is_active, created_at)
            VALUES (NEWID(), 'USR-S7654321B', 'S7654321B', 's7654321b@singpass.local', '', 'Singpass', 1, GETUTCDATE());
        END
        IF NOT EXISTS (SELECT 1 FROM users WHERE username = 'S7890123F')
        BEGIN
            INSERT INTO users (id, code, username, email, password_hash, provider, is_active, created_at)
            VALUES (NEWID(), 'USR-S7890123F', 'S7890123F', 's7890123f@singpass.local', '', 'Singpass', 1, GETUTCDATE());
        END
    "
done

# ==============================================================================
# PHẦN 3: SEED BIỂU PHÍ & CÔNG NỢ HỌC SINH (FS03 & FS09)
# ==============================================================================
echo -e "\n${YELLOW}[3/5] Seeding Cấu phần Phí, Hóa đơn & Công nợ học sinh...${NC}"

BP_DIR="$BACKEND_DIR/BillingPaymentService/BillingPaymentService.Database/dbo/SeedData"
run_sql_file "BillingPaymentService" "$BP_DIR/00_SeedFeeTypesAndComponents.sql" "Loại phí & Cấu phần phí"
run_sql_file "BillingPaymentService" "$BP_DIR/01_SeedInvoices.sql" "Biểu mẫu Hóa đơn"
run_sql_file "BillingPaymentService" "$BP_DIR/02_SeedStudentCharges.sql" "Khoản thu học sinh tiêu chuẩn"

# Reset các giao dịch tạm thời để hóa đơn luôn ở trạng thái sẵn sàng kiểm thử
printf "  -> Làm sạch các giao dịch cũ và thiết lập công nợ chuẩn cho Chloe Chan...\n"
run_sql_query "BillingPaymentService" "
    DELETE FROM payment_webhook_receipts;
    DELETE FROM transaction_funding_sources;
    DELETE FROM transactions;
    DELETE FROM invoice_items;
    DELETE FROM invoices;

    -- Đảm bảo 4 khoản công nợ chuẩn cho Chloe Chan (Tổng cộng 1,550.00 SGD)
    IF NOT EXISTS (SELECT 1 FROM student_charges WHERE id = 'bbbb0009-0000-0000-0000-000000000001')
    BEGIN
        INSERT INTO student_charges (id, student_id, enrollment_id, school_id, academic_year_id, academic_level_id,
            fee_component_id, fee_component_name_snapshot, pricing_date, period_start, period_end_exclusive,
            charge_date, due_date, base_amount, tax_amount, total_amount, currency_code, status, posted_at)
        VALUES ('bbbb0009-0000-0000-0000-000000000001', '01a15a22-dddf-750e-ac12-6d155e779d11',
            'cccc0001-0000-0000-0000-000000000001', '22222222-2222-2222-2222-222222222222',
            'dddd0001-0000-0000-0000-000000000001', 'dddd0002-0000-0000-0000-000000000001',
            'ffff0004-0000-0000-0000-000000000001', 'Term 4 Stationery Fee', '2026-10-15', '2026-11-01',
            '2027-02-01', '2026-10-15', '2026-11-15', 10.00, 0.00, 10.00, 'SGD', 'POSTED', '2026-10-15T00:00:00');
    END
    ELSE
    BEGIN
        UPDATE student_charges SET status = 'POSTED', total_amount = 10.00 WHERE id = 'bbbb0009-0000-0000-0000-000000000001';
    END

    IF NOT EXISTS (SELECT 1 FROM student_charges WHERE id = 'bbbb0009-0000-0000-0000-000000000002')
    BEGIN
        INSERT INTO student_charges (id, student_id, enrollment_id, school_id, academic_year_id, academic_level_id,
            fee_component_id, fee_component_name_snapshot, pricing_date, period_start, period_end_exclusive,
            charge_date, due_date, base_amount, tax_amount, total_amount, currency_code, status, posted_at)
        VALUES ('bbbb0009-0000-0000-0000-000000000002', '01a15a22-dddf-750e-ac12-6d155e779d11',
            'cccc0001-0000-0000-0000-000000000001', '22222222-2222-2222-2222-222222222222',
            'dddd0001-0000-0000-0000-000000000001', 'dddd0002-0000-0000-0000-000000000001',
            'ffff0004-0000-0000-0000-000000000002', 'Field Trip - Science Centre', '2026-10-15', '2026-11-01',
            '2027-02-01', '2026-10-15', '2026-11-20', 15.00, 0.00, 15.00, 'SGD', 'POSTED', '2026-10-15T00:00:00');
    END
    ELSE
    BEGIN
        UPDATE student_charges SET status = 'POSTED', total_amount = 15.00 WHERE id = 'bbbb0009-0000-0000-0000-000000000002';
    END

    IF NOT EXISTS (SELECT 1 FROM student_charges WHERE id = 'bbbb0009-0000-0000-0000-000000000003')
    BEGIN
        INSERT INTO student_charges (id, student_id, enrollment_id, school_id, academic_year_id, academic_level_id,
            fee_component_id, fee_component_name_snapshot, pricing_date, period_start, period_end_exclusive,
            charge_date, due_date, base_amount, tax_amount, total_amount, currency_code, status, posted_at)
        VALUES ('bbbb0009-0000-0000-0000-000000000003', '01a15a22-dddf-750e-ac12-6d155e779d11',
            'cccc0001-0000-0000-0000-000000000001', '22222222-2222-2222-2222-222222222222',
            'dddd0001-0000-0000-0000-000000000001', 'dddd0002-0000-0000-0000-000000000001',
            'ffff0004-0000-0000-0000-000000000003', 'Sports Fee', '2026-10-15', '2026-11-01',
            '2027-02-01', '2026-10-15', '2026-12-05', 25.00, 0.00, 25.00, 'SGD', 'POSTED', '2026-10-15T00:00:00');
    END
    ELSE
    BEGIN
        UPDATE student_charges SET status = 'POSTED', total_amount = 25.00 WHERE id = 'bbbb0009-0000-0000-0000-000000000003';
    END

    IF NOT EXISTS (SELECT 1 FROM student_charges WHERE id = 'bbbb0009-0000-0000-0000-000000000004')
    BEGIN
        INSERT INTO student_charges (id, student_id, enrollment_id, school_id, academic_year_id, academic_level_id,
            fee_component_id, fee_component_name_snapshot, pricing_date, period_start, period_end_exclusive,
            charge_date, due_date, base_amount, tax_amount, total_amount, currency_code, status, posted_at)
        VALUES ('bbbb0009-0000-0000-0000-000000000004', '01a15a22-dddf-750e-ac12-6d155e779d11',
            'cccc0001-0000-0000-0000-000000000001', '22222222-2222-2222-2222-222222222222',
            'dddd0001-0000-0000-0000-000000000001', 'dddd0002-0000-0000-0000-000000000001',
            'ffff0004-0000-0000-0000-000000000004', 'Overseas Learning Trip Fee', '2026-10-15', '2026-11-01',
            '2027-02-01', '2026-10-15', '2027-01-15', 1500.00, 0.00, 1500.00, 'SGD', 'POSTED', '2026-10-15T00:00:00');
    END
    ELSE
    BEGIN
        UPDATE student_charges SET status = 'POSTED', total_amount = 1500.00 WHERE id = 'bbbb0009-0000-0000-0000-000000000004';
    END

    -- Đảm bảo công nợ cho học sinh Tan Wei Ming (PAR-NORMAL-02)
    IF NOT EXISTS (SELECT 1 FROM student_charges WHERE id = 'cccc0009-0000-0000-0000-000000000001')
    BEGIN
        INSERT INTO student_charges (id, student_id, enrollment_id, school_id, academic_year_id, academic_level_id,
            fee_component_id, fee_component_name_snapshot, pricing_date, period_start, period_end_exclusive,
            charge_date, due_date, base_amount, tax_amount, total_amount, currency_code, status, posted_at)
        VALUES ('cccc0009-0000-0000-0000-000000000001', '01a15a22-f573-7ba6-93d2-71ac9a4ce40b',
            'cccc0001-0000-0000-0000-000000000001', '22222222-2222-2222-2222-222222222222',
            'dddd0001-0000-0000-0000-000000000001', 'dddd0002-0000-0000-0000-000000000001',
            'ffff0004-0000-0000-0000-000000000004', 'Library Fee', '2026-10-15', '2026-11-01',
            '2027-02-01', '2026-10-15', '2026-11-25', 20.00, 0.00, 20.00, 'SGD', 'POSTED', '2026-10-15T00:00:00');
    END
"

# ==============================================================================
# PHẦN 4: KIỂM TRA ĐỐI SOÁT & THỐNG KÊ DỮ LIỆU
# ==============================================================================
echo -e "\n${YELLOW}[4/5] Đối soát số lượng bản ghi đã seed...${NC}"

query_scalar() {
    local db="$1"
    local sql="$2"
    docker exec template-sqlserver /opt/mssql-tools18/bin/sqlcmd \
        -S localhost -U sa -P "YourStrong@Password123" \
        -d "$db" -C -h -1 -W -Q "SET NOCOUNT ON; $sql" 2>/dev/null | tr -d ' \r\n'
}

CNT_SCHOOLS=$(query_scalar "StudentSchoolDatabase" "SELECT COUNT(*) FROM schools")
CNT_CLASSES=$(query_scalar "StudentSchoolDatabase" "SELECT COUNT(*) FROM school_classes")
CNT_STUDENTS=$(query_scalar "StudentSchoolDatabase" "SELECT COUNT(*) FROM students")
CNT_USERS=$(query_scalar "TemplateIAMDatabase" "SELECT COUNT(*) FROM users")
CNT_EA_ACCOUNTS=$(query_scalar "EducationAccountDatabase" "SELECT COUNT(*) FROM Students")
CNT_WALLETS=$(query_scalar "EducationAccountDatabase" "SELECT COUNT(*) FROM Wallets")
CNT_CHARGES=$(query_scalar "BillingPaymentService" "SELECT COUNT(*) FROM student_charges")
CNT_FAS=$(query_scalar "FASDatabase" "SELECT COUNT(*) FROM moe_fas_schemes")

printf "  • StudentSchoolDatabase : %s Trường, %s Lớp, %s Học sinh\n" "$CNT_SCHOOLS" "$CNT_CLASSES" "$CNT_STUDENTS"
printf "  • TemplateIAMDatabase   : %s Người dùng (Admin moehq, School staff, SingPass)\n" "$CNT_USERS"
printf "  • EducationAccountDB    : %s Học sinh công dân, %s Ví Edusave hoạt động\n" "$CNT_EA_ACCOUNTS" "$CNT_WALLETS"
printf "  • BillingPaymentService : %s Khoản phí công nợ sẵn sàng thanh toán\n" "$CNT_CHARGES"
printf "  • FASDatabase           : %s Chương trình Hỗ trợ Tài chính FAS\n" "$CNT_FAS"

# ==============================================================================
# PHẦN 5: THÔNG TIN TRUY CẬP CHO CẢ HAI MÔI TRƯỜNG LOCAL
# ==============================================================================
echo -e "\n${GREEN}======================================================================${NC}"
echo -e "${GREEN}   ✅ HOÀN TẤT SEED DỮ LIỆU CHO CẢ HAI CỔNG LOCAL THÀNH CÔNG!       ${NC}"
echo -e "${GREEN}======================================================================${NC}"
echo -e ""
echo -e "  ${BOLD}${CYAN}1. ADMIN PORTAL (Quản trị & Nhà trường):${NC}"
echo -e "     • Địa chỉ URL:        ${GREEN}http://localhost:5173${NC}"
echo -e "     • Tài khoản MOE HQ:   Username: ${BOLD}moehq${NC} | Email: ${BOLD}admin@IAM.edu.vn${NC}"
echo -e "     • Tài khoản Trường:   Username: ${BOLD}school${NC} | Email: ${BOLD}staff1@IAM.edu.vn${NC}"
echo -e "     • Phạm vi dữ liệu:    8 trường học, cấu phần học phí, trợ cấp FAS, thông báo."
echo -e ""
echo -e "  ${BOLD}${CYAN}2. CITIZEN E-SERVICE PORTAL (Cổng Công dân & Phụ huynh):${NC}"
echo -e "     • Địa chỉ URL:        ${GREEN}http://localhost:5174${NC}"
echo -e "     • Đăng nhập SingPass: Qua MockPass ${GREEN}http://localhost:5156${NC}"
echo -e "     • Persona 1 (Chính):  NRIC: ${BOLD}S7654321B${NC} (Tan Wei Ming / Chloe Chan)"
echo -e "                           Ví Edusave: ${BOLD}50.00 SGD${NC} | Công nợ: ${BOLD}1,550.00 SGD${NC} (4 khoản phí)"
echo -e "     • Persona 2 (Phụ):    NRIC: ${BOLD}S7890123F${NC} (Nguyễn Văn Minh / Tan Wei Ming)"
echo -e "                           Ví Edusave: ${BOLD}40.00 SGD${NC} | Công nợ: ${BOLD}100.00 SGD${NC} (2 khoản phí)"
echo -e "     • Persona 3 (Không con): NRIC: ${BOLD}S3456789C${NC} (Kiểm thử màn hình Empty State)"
echo -e "     • Persona 4 (PR/IS):  NRIC: ${BOLD}S9012345H${NC} (Kiểm thử học sinh không quốc tịch SC)"
echo -e ""
echo -e "${GREEN}======================================================================${NC}"
