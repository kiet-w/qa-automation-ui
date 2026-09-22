#!/usr/bin/env python3
"""
run_tests.py - Test Execution Coordinator & Report Trigger.

Architecture:
- Phase 1: Executes Pytest with live streaming console output and JSON report generation.
  Supports all CLI options passed by user (e.g. -n 4, -m search, -k test_name).
  Safely awaits completion of all worker processes (pytest-xdist compatible).
- Phase 2: Triggers generate_report.py to convert JSON report into self-contained HTML report.
- Phase 3: Displays formatted ANSI terminal summary and propagates pytest returncode for CI/CD.
"""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

# ANSI color codes for terminal output
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
GRAY = "\033[90m"


def setup_environment(base_dir: Path) -> dict:
    """Ensure virtualenv bin directory is in PATH for finding pytest and python tools."""
    env = os.environ.copy()
    venv_bin = Path(sys.executable).parent
    possible_bins = [str(venv_bin), str(base_dir / ".venv" / "bin")]
    current_path = env.get("PATH", "")
    new_path_parts = [p for p in possible_bins if p not in current_path and Path(p).exists()]
    if new_path_parts:
        env["PATH"] = os.pathsep.join(new_path_parts + [current_path])
    return env


def determine_report_json_path(user_args: list[str], default_path: str = "reports/report.json") -> str:
    """Extract report JSON path if overridden by user arguments."""
    for arg in user_args:
        if arg.startswith("--json-report-file="):
            return arg.split("=", 1)[1]
    return default_path


def run_pytest_phase(base_dir: Path, env: dict, user_args: list[str], report_json_path: str) -> int:
    """
    Phase 1: Run Pytest with JSON reporting and user-provided CLI arguments.
    Outputs stream directly to terminal console in real-time.
    Waits for full completion (sequential or multi-worker xdist).
    """
    print(f"\n{BOLD}{CYAN}{'=' * 68}{RESET}")
    print(f"{BOLD}{CYAN}▶ PHA 1: THỰC THI KIỂM THỬ VỚI PYTEST{RESET}")
    print(f"{BOLD}{CYAN}{'=' * 68}{RESET}")

    # Resolve pytest command
    pytest_bin = "pytest"
    if not shutil.which("pytest", path=env.get("PATH", "")):
        venv_pytest = Path(sys.executable).parent / "pytest"
        if venv_pytest.exists():
            pytest_bin = str(venv_pytest)
        else:
            pytest_bin = None

    # Base pytest arguments
    cmd = [pytest_bin] if pytest_bin else [sys.executable, "-m", "pytest"]

    # Add json-report flags if not already provided in user_args
    if not any(arg.startswith("--json-report") for arg in user_args):
        cmd.append("--json-report")
    if not any(arg.startswith("--json-report-file=") for arg in user_args):
        cmd.append(f"--json-report-file={report_json_path}")


    cmd.extend(user_args)

    cmd_display = " ".join(cmd)
    print(f"{GRAY}Lệnh thực thi: {cmd_display}{RESET}\n")

    # Run subprocess synchronously, streaming stdout and stderr live to console
    start_time = time.time()
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(base_dir),
            env=env,
            stdout=None,
            stderr=None,
        )
        duration = time.time() - start_time
        print(f"\n{GRAY}Pytest đã kết thúc sau {duration:.2f}s (Return Code: {proc.returncode}){RESET}")
        return proc.returncode
    except FileNotFoundError:
        print(f"{RED}[LỖI] Không tìm thấy thực thi 'pytest'. Vui lòng cài đặt pytest hoặc kích hoạt virtual environment!{RESET}")
        return 1
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[HỦY] Người dùng đã dừng thực thi kiểm thử bằng Ctrl+C.{RESET}")
        return 130


def run_report_phase(base_dir: Path, env: dict, report_json_path: str) -> bool:
    """
    Phase 2: Trigger generate_report.py to build self-contained HTML report.
    Reports success message with absolute and relative paths.
    """
    print(f"\n{BOLD}{CYAN}{'=' * 68}{RESET}")
    print(f"{BOLD}{CYAN}▶ PHA 2: SINH BÁO CÁO KIỂM THỬ HTML{RESET}")
    print(f"{BOLD}{CYAN}{'=' * 68}{RESET}")

    report_script = base_dir / "generate_report.py"
    if not report_script.exists():
        print(f"{YELLOW}[CẢNH BÁO] Không tìm thấy '{report_script.name}'. Bỏ qua bước tạo HTML report.{RESET}")
        return False

    report_json_file = base_dir / report_json_path
    if not report_json_file.exists():
        print(f"{YELLOW}[CẢNH BÁO] Không tìm thấy file dữ liệu JSON '{report_json_path}'. Bỏ qua bước tạo HTML report.{RESET}")
        return False

    python_bin = sys.executable or "python"
    cmd = [python_bin, "generate_report.py", report_json_path]
    cmd_display = " ".join(cmd)
    print(f"{GRAY}Lệnh thực thi: {cmd_display}{RESET}\n")

    try:
        proc = subprocess.run(
            cmd,
            cwd=str(base_dir),
            env=env,
            stdout=None,
            stderr=None,
        )

        expected_html = base_dir / "reports" / "execution_report.html"
        if proc.returncode == 0 and expected_html.exists():
            rel_html = os.path.relpath(expected_html, base_dir)
            abs_html = str(expected_html.resolve())
            print(f"\n{GREEN}{BOLD}✓ Báo cáo kiểm thử HTML đã được tạo thành công!{RESET}")
            print(f"  • Đường dẫn tương đối: {CYAN}{rel_html}{RESET}")
            print(f"  • Đường dẫn tuyệt đối: {CYAN}{abs_html}{RESET}\n")
            return True
        elif proc.returncode == 0:
            print(f"\n{GREEN}{BOLD}✓ Script sinh báo cáo đã chạy hoàn tất!{RESET}")
            return True
        else:
            print(f"\n{RED}[LỖI] Script sinh báo cáo thất bại với mã lỗi: {proc.returncode}{RESET}")
            return False
    except Exception as e:
        print(f"\n{RED}[LỖI] Không thể khởi chạy script sinh báo cáo: {e}{RESET}")
        return False


def print_summary(base_dir: Path, pytest_returncode: int, report_json_path: str):
    """
    Phase 3: Parse report.json (if available) and display clear, ANSI-colored summary.
    """
    report_json_file = base_dir / report_json_path
    total = 0
    passed = 0
    failed = 0
    skipped = 0
    error = 0
    duration = None

    if report_json_file.exists():
        try:
            with open(report_json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            summary = data.get("summary", {})
            total = summary.get("total", summary.get("collected", 0))
            passed = summary.get("passed", 0)
            failed = summary.get("failed", 0)
            skipped = summary.get("skipped", 0)
            error = summary.get("error", 0)
            duration = data.get("duration", None)
        except Exception:
            pass

    status_color = GREEN if pytest_returncode == 0 else RED
    status_text = "PASSED" if pytest_returncode == 0 else "FAILED"

    print(f"\n{BOLD}{CYAN}{'=' * 68}{RESET}")
    print(f"{BOLD}{CYAN}📊 TỔNG KẾT KẾT QUẢ KIỂM THỬ (TEST EXECUTION SUMMARY){RESET}")
    print(f"{BOLD}{CYAN}{'=' * 68}{RESET}")
    print(f"  Trạng thái tổng thể : {status_color}{BOLD}[{status_text}]{RESET}")
    print(f"  Mã thoát (Exit Code): {status_color}{pytest_returncode}{RESET}")

    if total > 0 or passed > 0 or failed > 0:
        print(f"  Tổng số bài test    : {BOLD}{total}{RESET}")
        print(f"  Thành công (Passed) : {GREEN}{BOLD}{passed}{RESET}")
        if failed > 0:
            print(f"  Thất bại (Failed)   : {RED}{BOLD}{failed}{RESET}")
        else:
            print(f"  Thất bại (Failed)   : {GRAY}0{RESET}")
        if skipped > 0:
            print(f"  Bỏ qua (Skipped)    : {YELLOW}{skipped}{RESET}")
        if error > 0:
            print(f"  Lỗi hệ thống (Error): {RED}{error}{RESET}")

    if duration is not None:
        print(f"  Thời gian thực thi  : {BOLD}{duration:.2f}s{RESET}")

    print(f"{BOLD}{CYAN}{'=' * 68}{RESET}\n")


def main():
    base_dir = Path(__file__).resolve().parent
    reports_dir = base_dir / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    user_args = sys.argv[1:]
    report_json_path = determine_report_json_path(user_args)

    env = setup_environment(base_dir)

    # Pha 1: Chạy Pytest
    pytest_returncode = run_pytest_phase(base_dir, env, user_args, report_json_path)

    # Pha 2: Sinh Báo cáo HTML
    run_report_phase(base_dir, env, report_json_path)

    # Tóm tắt kết quả trên Terminal
    print_summary(base_dir, pytest_returncode, report_json_path)

    # Thoát với đúng mã lỗi của Pytest cho CI/CD
    sys.exit(pytest_returncode)


if __name__ == "__main__":
    main()
