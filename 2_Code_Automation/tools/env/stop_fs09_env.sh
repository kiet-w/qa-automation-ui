#!/usr/bin/env bash
# ==============================================================================
# tools/stop_fs09_env.sh - Dừng toàn bộ môi trường phục vụ Automation Testing FS09
# ==============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
PID_FILE="$WORKSPACE_DIR/.fs09_services.pid"

YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${YELLOW}Đang dừng toàn bộ các tiến trình môi trường FS09...${NC}"

if [ -f "$PID_FILE" ]; then
    while IFS= read -r pid; do
        if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then
            kill "$pid" 2>/dev/null || true
        fi
    done < "$PID_FILE"
    rm -f "$PID_FILE"
fi

# Quét và dọn các cổng đã sử dụng
PORTS=(5174 5176 5156 5286 5287 5016 5006 5008 5290 5273)
for port in "${PORTS[@]}"; do
    fuser -k "${port}/tcp" > /dev/null 2>&1 || true
done

echo -e "${GREEN}✓ Đã dừng toàn bộ dịch vụ môi trường FS09 thành công!${NC}"
