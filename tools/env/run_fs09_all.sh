#!/usr/bin/env bash
# ==============================================================================
# tools/run_fs09_all.sh - Lệnh duy nhất: Tự chuẩn bị môi trường + Chạy Test + Xuất báo cáo
# ==============================================================================
set -e

SCRIPT_PATH="$(realpath "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(dirname "$SCRIPT_PATH")"
WORKSPACE_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

AUTO_STOP=false
TEST_ARGS=()

for arg in "$@"; do
    if [[ "$arg" == "--stop" || "$arg" == "--clean" ]]; then
        AUTO_STOP=true
    else
        TEST_ARGS+=("$arg")
    fi
done

echo -e "${CYAN}===================================================================${NC}"
echo -e "${CYAN}   EduSave FS09 All-In-One Test Runner                             ${NC}"
echo -e "${CYAN}===================================================================${NC}"

# 1. Kiểm tra môi trường xem đã chạy chưa
check_health() {
    local code
    code=$(curl -s -o /dev/null -w "%{http_code}" "$1" 2>/dev/null || echo "000")
    [ "$code" = "200" ]
}

echo -e "\n${YELLOW}[1/3] Kiểm tra trạng thái dịch vụ nền...${NC}"
SERVICES_READY=true

if ! check_health "http://localhost:5174/" || \
   ! check_health "http://localhost:5176/" || \
   ! check_health "http://localhost:5008/health" || \
   ! check_health "http://localhost:5016/health" || \
   ! check_health "http://localhost:5156/singpass/login"; then
    SERVICES_READY=false
fi

if [ "$SERVICES_READY" = true ]; then
    echo -e "  ${GREEN}✓ Toàn bộ môi trường FS09 đang hoạt động tốt.${NC}"
else
    echo -e "  ${YELLOW}Môi trường chưa đầy đủ. Đang tự động khởi động...${NC}"
    bash "$SCRIPT_DIR/start_fs09_env.sh" -b
    
    echo -e "  Đợi các dịch vụ khởi động hoàn tất..."
    for i in {1..20}; do
        if check_health "http://localhost:5174/" && \
           check_health "http://localhost:5176/" && \
           check_health "http://localhost:5008/health" && \
           check_health "http://localhost:5016/health" && \
           check_health "http://localhost:5156/singpass/login"; then
            echo -e "  ${GREEN}✓ Toàn bộ dịch vụ đã sẵn sàng.${NC}"
            break
        fi
        sleep 1
    done
fi

# 2. Thực thi Test Suite
echo -e "\n${YELLOW}[2/3] Bắt đầu thực thi bộ Automation Test FS09...${NC}"
cd "$WORKSPACE_DIR"

TEST_EXIT_CODE=0
if [ ${#TEST_ARGS[@]} -eq 0 ]; then
    python3 "$WORKSPACE_DIR/run_tests.py" tests/fs09/ || TEST_EXIT_CODE=$?
else
    python3 "$WORKSPACE_DIR/run_tests.py" tests/fs09/ "${TEST_ARGS[@]}" || TEST_EXIT_CODE=$?
fi

# 3. Tổng kết & Báo cáo
echo -e "\n${YELLOW}[3/3] Báo cáo & Dọn dẹp...${NC}"
REPORT_HTML="$WORKSPACE_DIR/reports/fs09/execution_report.html"

if [ -f "$REPORT_HTML" ]; then
    echo -e "${GREEN}===================================================================${NC}"
    echo -e "${GREEN}   ✓ BÁO CÁO EXTENTREPORTS HTML ĐÃ ĐƯỢC SINH THÀNH CÔNG!          ${NC}"
    echo -e "${GREEN}===================================================================${NC}"
    echo -e "  • Báo cáo trực tiếp   : ${BOLD}${CYAN}$REPORT_HTML${NC}"
    echo -e "  • Mở xem bằng trình duyệt: ${YELLOW}xdg-open reports/fs09/execution_report.html${NC}"
    echo -e "${GREEN}===================================================================${NC}"
fi

# Dọn dẹp nếu người dùng yêu cầu cờ --stop
if [ "$AUTO_STOP" = true ]; then
    echo -e "\n${YELLOW}Đang dừng toàn bộ dịch vụ (--stop)...${NC}"
    bash "$SCRIPT_DIR/stop_fs09_env.sh"
else
    echo -e "\n${CYAN}Ghi chú: Môi trường vẫn đang chạy ngầm để bạn có thể xem lại UI.${NC}"
    echo -e "Khi nào muốn tắt toàn bộ dịch vụ, gõ: ${YELLOW}bash tools/env/stop_fs09_env.sh${NC}\n"
fi

exit $TEST_EXIT_CODE
