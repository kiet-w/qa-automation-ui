#!/usr/bin/env bash
# ==============================================================================
# tools/start_fs09_env.sh - Khởi động toàn bộ môi trường phục vụ Automation Testing FS09
# 100% Non-invasive (Không sửa đổi copy/)
# ==============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
BACKEND_DIR="$WORKSPACE_DIR/copy/edufams-backend"
FRONTEND_DIR="$WORKSPACE_DIR/copy/edugovernment-frontend"
PID_FILE="$WORKSPACE_DIR/.fs09_services.pid"
LOG_DIR="$WORKSPACE_DIR/reports/fs09_env_logs"

mkdir -p "$LOG_DIR"

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

echo -e "${CYAN}===================================================================${NC}"
echo -e "${CYAN}   Khởi động Môi trường Phục vụ Test Tự động FS09 / R9            ${NC}"
echo -e "${CYAN}===================================================================${NC}"

# Dừng phiên trước nếu đang chạy
if [ -f "$PID_FILE" ]; then
    bash "$SCRIPT_DIR/stop_fs09_env.sh" > /dev/null 2>&1 || true
fi
> "$PID_FILE"

# 1. Khởi động các Docker container nền
echo -e "\n${YELLOW}[1/5] Khởi động các Docker Containers nền...${NC}"
REQUIRED_CONTAINERS=("template-sqlserver" "template-rabbitmq" "template-redis" "template-consul")
for c in "${REQUIRED_CONTAINERS[@]}"; do
    if ! docker ps --format '{{.Names}}' | grep -q "^${c}$"; then
        echo -e "  Starting container $c..."
        docker start "$c" 2>/dev/null || true
    else
        echo -e "  ${GREEN}✓${NC} $c đang chạy"
    fi
done

# Đợi SQL Server sẵn sàng
echo -e "  Đợi SQL Server sẵn sàng..."
for i in {1..30}; do
    if docker exec template-sqlserver /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "YourStrong@Password123" -C -Q "SELECT 1" > /dev/null 2>&1; then
        echo -e "  ${GREEN}✓${NC} SQL Server đã sẵn sàng."
        break
    fi
    sleep 1
done

# Biến môi trường dùng chung
export ASPNETCORE_ENVIRONMENT=Production
export RabbitMQ__Host="localhost"
export RabbitMQ__Port=5672
export RabbitMQ__Username="guest"
export RabbitMQ__Password="guest"
export RabbitMQ__VirtualHost="/"
export Redis__ConnectionString="localhost:6379"
export SQL_SERVER_HOST="localhost,1433"
export SQL_USER="sa"
export SQL_PASS="YourStrong@Password123"

run_dotnet() {
    local name="$1"
    local port="$2"
    local dir_rel="$3"
    local dll_rel="$4"
    local db_name="$5"
    local extra_env="$6"

    local conn="Server=$SQL_SERVER_HOST;Database=$db_name;User Id=$SQL_USER;Password=$SQL_PASS;TrustServerCertificate=True;MultipleActiveResultSets=True;"
    local log_file="$LOG_DIR/${name}.log"

    printf "  -> Khởi chạy %-24s trên port :%-5s ...\n" "$name" "$port"
    (
        cd "$BACKEND_DIR/$dir_rel"
        export Database__ConnectionString="$conn"
        export ConnectionStrings__DefaultConnection="$conn"
        export ConnectionStrings__SqlServer="$conn"
        if [ -n "$extra_env" ]; then
            eval "$extra_env"
        fi
        nohup dotnet "$BACKEND_DIR/$dll_rel" --urls "http://0.0.0.0:${port}" > "$log_file" 2>&1 &
        echo $!
    ) >> "$PID_FILE"
}

# 2. Khởi chạy Simulators
echo -e "\n${YELLOW}[2/5] Khởi chạy Simulators...${NC}"

# MockPass (SingPass)
printf "  -> Khởi chạy %-24s trên port :5156 ...\n" "MockPass"
(
    cd "$BACKEND_DIR/Simulation/mockpass"
    setsid node index.js </dev/null > "$LOG_DIR/MockPass.log" 2>&1 &
    PID=$!
    echo $PID >> "$PID_FILE"
)

# CitizenDataSim
(
    cd "$BACKEND_DIR/Simulation/GovernmentCitizenDataSimulation"
    setsid dotnet "$BACKEND_DIR/Simulation/GovernmentCitizenDataSimulation/bin/Debug/net10.0/GovernmentCitizenDataSimulation.dll" --urls "http://0.0.0.0:5287" </dev/null > "$LOG_DIR/CitizenDataSim.log" 2>&1 &
    PID=$!
    echo $PID >> "$PID_FILE"
)

# OnlinePaymentGatewaySimulation (với HMAC secret đúng cho FS09)
printf "  -> Khởi chạy %-24s trên port :5286 ...\n" "PaymentGatewaySim"
(
    cd "$BACKEND_DIR/Simulation/OnlinePaymentGatewaySimulation"
    export ASPNETCORE_ENVIRONMENT=Development
    export Gateway__WebhookSecret="whsec_f9_demo_shared_secret"
    setsid dotnet "$BACKEND_DIR/Simulation/OnlinePaymentGatewaySimulation/bin/Debug/net10.0/OnlinePaymentGatewaySimulation.dll" --urls "http://0.0.0.0:5286" </dev/null > "$LOG_DIR/PaymentSim.log" 2>&1 &
    PID=$!
    echo $PID >> "$PID_FILE"
)

# 3. Khởi chạy Sidecar Proxy & Microservices
echo -e "\n${YELLOW}[3/5] Khởi chạy QA Proxy & Microservices...${NC}"

# QA Proxy trên cổng 5016
printf "  -> Khởi chạy %-24s trên port :5016 ...\n" "EduAccountProxy"
setsid python3 "$WORKSPACE_DIR/tools/env/qa_eduaccount_proxy.py" </dev/null > "$LOG_DIR/EduAccountProxy.log" 2>&1 &
PID=$!
echo $PID >> "$PID_FILE"

# EducationAccountService
printf "  -> Khởi chạy %-24s trên port :5006 ...\n" "EducationAccountService"
(
    cd "$BACKEND_DIR/EducationAccountService/EducationAccountService.API"
    local_conn="Server=$SQL_SERVER_HOST;Database=EducationAccountDatabase;User Id=$SQL_USER;Password=$SQL_PASS;TrustServerCertificate=True;MultipleActiveResultSets=True;"
    export Database__ConnectionString="$local_conn"
    export ConnectionStrings__DefaultConnection="$local_conn"
    export ConnectionStrings__SqlServer="$local_conn"
    export GovernmentSimulation__BaseUrl="http://localhost:5287"
    export GovernmentSimulation__ApiKey="YOUR_SIMULATION_GOV_API_KEY"
    export GovernmentSiumulation__BaseUrl="http://localhost:5287"
    export GovernmentSiumulation__ApiKey="YOUR_SIMULATION_GOV_API_KEY"
    setsid dotnet "$BACKEND_DIR/EducationAccountService/EducationAccountService.API/bin/Debug/net10.0/EducationAccountService.API.dll" --urls "http://0.0.0.0:5006" </dev/null > "$LOG_DIR/EducationAccountService.log" 2>&1 &
    PID=$!
    echo $PID >> "$PID_FILE"
)

# IAMService (trỏ qua proxy 5016)
printf "  -> Khởi chạy %-24s trên port :5290 ...\n" "IAMService"
(
    cd "$BACKEND_DIR/IAMService/IAMService.API"
    export Database__ConnectionString="Server=$SQL_SERVER_HOST;Database=TemplateIAMDatabase;User Id=$SQL_USER;Password=$SQL_PASS;TrustServerCertificate=True;MultipleActiveResultSets=True;"
    export ConnectionStrings__DefaultConnection="Server=$SQL_SERVER_HOST;Database=TemplateIAMDatabase;User Id=$SQL_USER;Password=$SQL_PASS;TrustServerCertificate=True;MultipleActiveResultSets=True;"
    export EduAccount__BaseUrl="http://localhost:5016"
    setsid dotnet "$BACKEND_DIR/IAMService/IAMService.API/bin/Debug/net10.0/IAMService.API.dll" --urls "http://0.0.0.0:5290" </dev/null > "$LOG_DIR/IAMService.log" 2>&1 &
    PID=$!
    echo $PID >> "$PID_FILE"
)

# BillingPaymentService (trỏ qua proxy 5016)
printf "  -> Khởi chạy %-24s trên port :5008 ...\n" "BillingPaymentService"
(
    cd "$BACKEND_DIR/BillingPaymentService/BillingPaymentService.API"
    local_conn="Server=$SQL_SERVER_HOST;Database=BillingPaymentService;User Id=$SQL_USER;Password=$SQL_PASS;TrustServerCertificate=True;MultipleActiveResultSets=True;"
    export Database__ConnectionString="$local_conn"
    export ConnectionStrings__DefaultConnection="$local_conn"
    export ConnectionStrings__SqlServer="$local_conn"
    export EducationAccount__BaseUrl="http://localhost:5016"
    setsid dotnet "$BACKEND_DIR/BillingPaymentService/BillingPaymentService.API/bin/Debug/net10.0/BillingPaymentService.API.dll" --urls "http://0.0.0.0:5008" </dev/null > "$LOG_DIR/BillingPaymentService.log" 2>&1 &
    PID=$!
    echo $PID >> "$PID_FILE"
)

# ApiGateway
printf "  -> Khởi chạy %-24s trên port :5273 ...\n" "ApiGateway"
(
    cd "$BACKEND_DIR/ApiGateway"
    setsid dotnet "$BACKEND_DIR/ApiGateway/bin/Debug/net10.0/ApiGateway.dll" --urls "http://0.0.0.0:5273" --Clusters:education-account-cluster:Url=http://localhost:5016 </dev/null > "$LOG_DIR/ApiGateway.log" 2>&1 &
    PID=$!
    echo $PID >> "$PID_FILE"
)

# 4. Khởi chạy Ứng dụng Giao diện (Frontend)
echo -e "\n${YELLOW}[4/5] Khởi chạy Ứng dụng Frontend Vite...${NC}"

# E-Service Portal (cổng :5174)
printf "  -> Khởi chạy %-24s trên port :5174 ...\n" "E-Service Portal"
(
    cd "$FRONTEND_DIR/apps/e-service"
    setsid npx vite --port 5174 --host </dev/null > "$LOG_DIR/e-service.log" 2>&1 &
    PID=$!
    echo $PID >> "$PID_FILE"
)

# Payment Checkout Simulator (cổng :5176)
printf "  -> Khởi chạy %-24s trên port :5176 ...\n" "Checkout Simulator"
(
    cd "$FRONTEND_DIR/apps/payment-checkout-simulator"
    setsid npx vite --port 5176 --host </dev/null > "$LOG_DIR/payment-checkout-simulator.log" 2>&1 &
    PID=$!
    echo $PID >> "$PID_FILE"
)

# 5. Khởi tạo & Đồng bộ Dữ liệu Test (Seed Data)
echo -e "\n${YELLOW}[5/5] Khởi tạo & Kiểm tra Dữ liệu Test...${NC}"
sleep 3

# Đồng bộ Citizen & Students
curl -s -X POST "http://localhost:5006/api/v1/accounts/trigger-citizen-sync" \
    -H "Content-Type: application/json" \
    -H "X-User-Roles: MOEHQ" \
    -H "X-User-Id: system" \
    -d '{"targetFromDob":"2000-01-01","targetToDob":"2026-01-01"}' > /dev/null 2>&1 || true

# Liên kết tài khoản phụ huynh & con cái
docker exec template-sqlserver /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "YourStrong@Password123" -C -Q "SET QUOTED_IDENTIFIER ON; UPDATE EducationAccountDatabase..Students SET father_nric = 'S7654321B' WHERE nric = 'T0000784X'; UPDATE EducationAccountDatabase..Students SET father_nric = 'S7890123F' WHERE nric = 'S1234567A';" > /dev/null 2>&1 || true

# Đảm bảo có student charges trong BillingPaymentService
docker exec template-sqlserver /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "YourStrong@Password123" -C -Q "
SET QUOTED_IDENTIFIER ON;
IF NOT EXISTS (SELECT 1 FROM BillingPaymentService..student_charges WHERE student_id = '01a15a22-dddf-750e-ac12-6d155e779d11')
BEGIN
    INSERT INTO BillingPaymentService..student_charges (id, student_id, fee_structure_id, academic_year, status, due_date, gross_amount, subsidy_amount, net_payable, created_at, created_by, updated_at, updated_by)
    VALUES (NEWID(), '01a15a22-dddf-750e-ac12-6d155e779d11', NEWID(), 2026, 0, DATEADD(day, 30, GETDATE()), 100.00, 0.00, 100.00, GETDATE(), 'SYSTEM', GETDATE(), 'SYSTEM');
END
" > /dev/null 2>&1 || true

echo -e "\n${GREEN}===================================================================${NC}"
echo -e "${GREEN}   ✓ MÔI TRƯỜNG FS09 ĐÃ SẴN SÀNG!                                  ${NC}"
echo -e "${GREEN}===================================================================${NC}"
echo -e "  • E-Service Parent Portal : ${CYAN}http://localhost:5174${NC}"
echo -e "  • Payment Gateway Sim     : ${CYAN}http://localhost:5176${NC} / ${CYAN}:5286${NC}"
echo -e "  • SingPass MockPass       : ${CYAN}http://localhost:5156/singpass/login${NC}"
echo -e "  • BillingPaymentService   : ${CYAN}http://localhost:5008${NC}"
echo -e "  • EducationAccountProxy   : ${CYAN}http://localhost:5016${NC}"
echo -e "  • SQL Server              : ${CYAN}localhost:1433 (sa / YourStrong@Password123)${NC}"
echo -e "  • Logs Directory          : ${CYAN}$LOG_DIR${NC}"
echo -e "  • Để dừng môi trường      : ${YELLOW}bash tools/env/stop_fs09_env.sh${NC}"
echo -e "${GREEN}===================================================================${NC}\n"

BACKGROUND_MODE=false
if [[ "$1" == "-b" || "$1" == "--background" || "$1" == "--daemon" ]]; then
    BACKGROUND_MODE=true
fi

if [ "$BACKGROUND_MODE" = false ]; then
    echo -e "${YELLOW}Đang giữ môi trường hoạt động trong terminal này.${NC}"
    echo -e "${YELLOW}Mở một terminal khác để chạy test: ${GREEN}./run_tests.py tests/fs09/${NC}"
    echo -e "${YELLOW}Nhấn [Ctrl+C] tại terminal này khi muốn dừng toàn bộ dịch vụ.${NC}\n"
    cleanup() {
        echo -e "\n${YELLOW}Đang dừng toàn bộ dịch vụ FS09...${NC}"
        bash "$SCRIPT_DIR/stop_fs09_env.sh"
        exit 0
    }
    trap cleanup SIGINT SIGTERM EXIT
    while true; do
        sleep 2
    done
fi
