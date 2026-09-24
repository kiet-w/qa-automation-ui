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
    """Extract report JSON path if overridden by user arguments or inferred from ticket folder."""
    for arg in user_args:
        if arg.startswith("--json-report-file="):
            return arg.split("=", 1)[1]

    # Detect ticket folder from CLI arguments (e.g. tests/us01_bing_search or tests/us01_bing_search/test_bing_search.py)
    for arg in user_args:
        if not arg.startswith("-"):
            parts = Path(arg).parts
            if "tests" in parts:
                idx = parts.index("tests")
                if idx + 1 < len(parts):
                    candidate = parts[idx + 1]
                    ticket = candidate if not candidate.endswith(".py") else Path(arg).parent.name
                    if ticket and not ticket.startswith(("_", ".")) and ticket != "tests":
                        return f"reports/{ticket}/report.json"

    # If no ticket specified in args, check if exactly one ticket folder exists in tests/
    tests_dir = Path(__file__).resolve().parent / "tests"
    if tests_dir.exists():
        subdirs = [d.name for d in tests_dir.iterdir() if d.is_dir() and not d.name.startswith(("_", "."))]
        if len(subdirs) == 1:
            return f"reports/{subdirs[0]}/report.json"

    return default_path


def resolve_actual_report_json(base_dir: Path, configured_path: str) -> str:
    """
    Find the actual report.json file generated during the test run.
    Falls back to locating the newest report.json in reports/ if conftest redirected it.
    """
    p = base_dir / configured_path
    if p.exists():
        return configured_path

    reports_dir = base_dir / "reports"
    if reports_dir.exists():
        candidates = [f for f in reports_dir.glob("**/report.json") if f.is_file()]
        if candidates:
            newest = max(candidates, key=lambda f: f.stat().st_mtime)
            try:
                return str(newest.relative_to(base_dir))
            except Exception:
                return str(newest)

    return configured_path


def run_pytest_phase(base_dir: Path, env: dict, user_args: list[str], report_json_path: str) -> int:
    """
    Phase 1: Run Pytest with JSON reporting and user-provided CLI arguments.
    Supports -n <workers> for parallel execution via pytest-xdist.
    Outputs stream directly to terminal console in real-time.
    """
    print(f"\n{BOLD}{CYAN}{'=' * 68}{RESET}")
    print(f"{BOLD}{CYAN}▶ PHASE 1: EXECUTING TESTS WITH PYTEST{RESET}")
    print(f"{BOLD}{CYAN}{'=' * 68}{RESET}")

    # Resolve pytest binary or python executable
    venv_bin = base_dir / ".venv" / "bin"
    pytest_bin = None
    if (venv_bin / "pytest").exists():
        pytest_bin = str(venv_bin / "pytest")
    elif shutil.which("pytest", path=env.get("PATH", "")):
        pytest_bin = shutil.which("pytest", path=env.get("PATH", ""))
    elif (Path(sys.executable).parent / "pytest").exists():
        pytest_bin = str(Path(sys.executable).parent / "pytest")

    # Base pytest arguments
    if pytest_bin:
        cmd = [pytest_bin]
    elif (venv_bin / "python").exists():
        cmd = [str(venv_bin / "python"), "-m", "pytest"]
    else:
        cmd = [sys.executable, "-m", "pytest"]

    # Add json-report flags if not already provided in user_args
    if not any(arg.startswith("--json-report") for arg in user_args):
        cmd.append("--json-report")
    if not any(arg.startswith("--json-report-file=") for arg in user_args):
        cmd.append(f"--json-report-file={report_json_path}")

    cmd.extend(user_args)

    cmd_display = " ".join(cmd)
    print(f"{GRAY}Execution command: {cmd_display}{RESET}\n")

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
        print(f"\n{GRAY}Pytest completed in {duration:.2f}s (Return Code: {proc.returncode}){RESET}")
        return proc.returncode
    except FileNotFoundError:
        print(f"{RED}[ERROR] 'pytest' executable not found. Please install pytest or activate virtual environment!{RESET}")
        return 1
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[CANCELLED] Test execution interrupted by user (Ctrl+C).{RESET}")
        return 130



def run_report_phase(base_dir: Path, env: dict, report_json_path: str) -> bool:
    """
    Phase 2: Trigger generate_report.py to build self-contained HTML report.
    Reports success message with absolute and relative paths.
    """
    print(f"\n{BOLD}{CYAN}{'=' * 68}{RESET}")
    print(f"{BOLD}{CYAN}▶ PHASE 2: GENERATING HTML EXECUTION REPORT{RESET}")
    print(f"{BOLD}{CYAN}{'=' * 68}{RESET}")

    report_script = base_dir / "generate_report.py"
    if not report_script.exists():
        print(f"{YELLOW}[WARNING] '{report_script.name}' not found. Skipping HTML report generation.{RESET}")
        return False

    report_json_file = base_dir / report_json_path
    if not report_json_file.exists():
        print(f"{YELLOW}[WARNING] JSON report file '{report_json_path}' not found. Skipping HTML report generation.{RESET}")
        return False

    venv_python = base_dir / ".venv" / "bin" / "python"
    python_bin = str(venv_python) if venv_python.exists() else (sys.executable or "python")
    cmd = [python_bin, "generate_report.py", report_json_path]
    cmd_display = " ".join(cmd)
    print(f"{GRAY}Execution command: {cmd_display}{RESET}\n")

    try:
        proc = subprocess.run(
            cmd,
            cwd=str(base_dir),
            env=env,
            stdout=None,
            stderr=None,
        )

        expected_html = report_json_file.parent / "execution_report.html"
        if proc.returncode == 0 and expected_html.exists():
            rel_html = os.path.relpath(expected_html, base_dir)
            abs_html = str(expected_html.resolve())
            print(f"\n{GREEN}{BOLD}✓ HTML execution report generated successfully!{RESET}")
            print(f"  • Relative path: {CYAN}{rel_html}{RESET}")
            print(f"  • Absolute path: {CYAN}{abs_html}{RESET}\n")
            return True
        elif proc.returncode == 0:
            print(f"\n{GREEN}{BOLD}✓ Report generation completed successfully!{RESET}")
            return True
        else:
            print(f"\n{RED}[ERROR] Report generation failed with exit code: {proc.returncode}{RESET}")
            return False
    except Exception as e:
        print(f"\n{RED}[ERROR] Could not launch report generation script: {e}{RESET}")
        return False


def print_summary(base_dir: Path, pytest_returncode: int, report_json_path: str):
    """
    Phase 3: Parse report.json (if available) and display clear, ANSI-colored summary.
    Supports multi-test scenario breakdown for parallel execution.
    """
    report_json_file = base_dir / report_json_path
    total = 0
    passed = 0
    failed = 0
    skipped = 0
    error = 0
    duration = None
    tests_summary = []

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

            raw_tests = data.get("tests", [])
            for t in raw_tests:
                nodeid = t.get("nodeid", "")
                name = nodeid.split("::")[-1] if "::" in nodeid else nodeid
                outcome = t.get("outcome", "unknown").upper()
                dur = float(t.get("duration", t.get("call", {}).get("duration", 0.0)))
                tests_summary.append((name, outcome, dur))
        except Exception:
            pass

    if total == 0 and tests_summary:
        total = len(tests_summary)
        passed = sum(1 for _, out, _ in tests_summary if out == "PASSED")
        failed = sum(1 for _, out, _ in tests_summary if out == "FAILED")
        skipped = sum(1 for _, out, _ in tests_summary if out == "SKIPPED")

    status_color = GREEN if pytest_returncode == 0 else RED
    status_text = "PASSED" if pytest_returncode == 0 else "FAILED"

    print(f"\n{BOLD}{CYAN}{'=' * 68}{RESET}")
    print(f"{BOLD}{CYAN}📊 TEST EXECUTION SUMMARY{RESET}")
    print(f"{BOLD}{CYAN}{'=' * 68}{RESET}")
    print(f"  Overall Status : {status_color}{BOLD}[{status_text}]{RESET}")
    print(f"  Exit Code      : {status_color}{pytest_returncode}{RESET}")

    if total > 0 or passed > 0 or failed > 0:
        print(f"  Total Tests    : {BOLD}{total}{RESET}")
        print(f"  Passed         : {GREEN}{BOLD}{passed}{RESET}")
        if failed > 0:
            print(f"  Failed         : {RED}{BOLD}{failed}{RESET}")
        else:
            print(f"  Failed         : {GRAY}0{RESET}")
        if skipped > 0:
            print(f"  Skipped        : {YELLOW}{skipped}{RESET}")
        if error > 0:
            print(f"  Error          : {RED}{error}{RESET}")

    if duration is not None:
        print(f"  Execution Time : {BOLD}{duration:.2f}s{RESET}")

    if tests_summary and len(tests_summary) > 1:
        print(f"\n  {BOLD}Parallel Scenario Breakdown ({len(tests_summary)} test cases):{RESET}")
        for name, outcome, dur in tests_summary:
            symbol = f"{GREEN}✓{RESET}" if outcome == "PASSED" else f"{RED}✗{RESET}"
            out_color = GREEN if outcome == "PASSED" else RED
            print(f"    {symbol} {name} [{out_color}{outcome}{RESET} - {dur:.2f}s]")

    print(f"{BOLD}{CYAN}{'=' * 68}{RESET}\n")


def main():
    base_dir = Path(__file__).resolve().parent
    reports_dir = base_dir / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    user_args = sys.argv[1:]
    report_json_path = determine_report_json_path(user_args)

    env = setup_environment(base_dir)

    # Phase 1: Run Pytest
    pytest_returncode = run_pytest_phase(base_dir, env, user_args, report_json_path)

    # Determine the actual generated JSON report path
    actual_json_path = resolve_actual_report_json(base_dir, report_json_path)

    # Phase 2: Generate HTML Report
    run_report_phase(base_dir, env, actual_json_path)

    # Phase 3: Display terminal summary
    print_summary(base_dir, pytest_returncode, actual_json_path)

    # Propagate pytest exit code for CI/CD
    sys.exit(pytest_returncode)


if __name__ == "__main__":
    main()
