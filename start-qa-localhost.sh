#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Reuse a working stack. Re-running the underlying launcher republishes databases
# and restarts frontends, which is unnecessary when all endpoints are available.
if [[ $# -eq 0 || ( $# -eq 1 && ( "$1" == "-b" || "$1" == "--background" ) ) ]]; then
    if curl -fsS --max-time 3 http://127.0.0.1:5273/health >/dev/null 2>&1 \
        && curl -fkSs --max-time 3 https://127.0.0.1:5173/ >/dev/null 2>&1 \
        && curl -fkSs --max-time 3 https://127.0.0.1:5174/ >/dev/null 2>&1 \
        && curl -fsS --max-time 3 http://127.0.0.1:5176/ >/dev/null 2>&1; then
        printf 'EduFAMS QA is already responding:\n  Admin Portal:     https://localhost:5173/\n  E-Service Portal: https://localhost:5174/\n  Payment Checkout: http://localhost:5176/\n  API health:       http://localhost:5273/health\n'
        exit 0
    fi
fi

exec bash "$ROOT_DIR/copy/start-qa-localhost.sh" "$@"
