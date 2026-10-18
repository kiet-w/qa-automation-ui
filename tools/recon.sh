#!/usr/bin/env bash
# tools/recon.sh - Trinh sát thụ động màn hình Staging bằng bsk (Passive Recon)
set -euo pipefail

TARGET_URL="${1:?Cách dùng: ./tools/recon.sh <TARGET_URL> <BROWSER_ID>}"
BROWSER_PROFILE="${2:?Lỗi: Bắt buộc truyền BROWSER_ID (tra cứu qua: bsk browsers). Không được phép để trống để tránh can thiệp nhầm trình duyệt ngoài ý muốn.}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_DIR="reports/recon_${TIMESTAMP}"
mkdir -p "$OUTPUT_DIR"

SESSION=""
cleanup() {
    if [ -n "$SESSION" ]; then
        bsk session stop "$SESSION" >/dev/null 2>&1 || true
    fi
}
trap cleanup EXIT INT TERM

echo "=== [1/4] Khởi tạo BSK Session ==="
echo "Sử dụng Browser ID chỉ định: $BROWSER_PROFILE"
SESSION=$(bsk session start --browser "$BROWSER_PROFILE" --json | jq -r .session_id)

echo "=== [2/4] Điều hướng tới: $TARGET_URL (wait-until: networkidle, timeout: 30s) ==="
bsk navigate "$TARGET_URL" --wait-until networkidle --timeout 30s --session "$SESSION"

echo "=== [3/4] Thu thập dữ liệu ==="
# 1. Snapshot cây Accessibility
bsk snapshot --session "$SESSION" > "$OUTPUT_DIR/accessibility_snapshot.txt"

# 2. Dump HTML DOM hoàn chỉnh
bsk get-html --session "$SESSION" --out "$OUTPUT_DIR/page_dom.html"

# 3. Lấy log Console và Network từ bộ đệm của extension
bsk console --session "$SESSION" --include-stack > "$OUTPUT_DIR/console_logs.txt"
bsk network --session "$SESSION" > "$OUTPUT_DIR/network_logs.txt"

# 4. Chụp ảnh màn hình giao diện (thử full-page trước, ghi stderr ra log nếu lỗi rồi fallback viewport)
if ! bsk screenshot --session "$SESSION" --full-page --out "$OUTPUT_DIR/initial_screen.png" 2> "$OUTPUT_DIR/screenshot_error.log"; then
    echo "CẢNH BÁO: Chụp --full-page thất bại (chi tiết xem tại: $OUTPUT_DIR/screenshot_error.log), tự động chuyển sang chụp viewport."
    bsk screenshot --session "$SESSION" --out "$OUTPUT_DIR/initial_screen.png"
else
    rm -f "$OUTPUT_DIR/screenshot_error.log"
fi

echo "=== [4/4] Hoàn tất trinh sát thụ động ==="
echo "Artifacts đã lưu tại: $OUTPUT_DIR"
echo "Checklist bảo mật: Rà soát $OUTPUT_DIR/network_logs.txt và page_dom.html trước khi chia sẻ."
