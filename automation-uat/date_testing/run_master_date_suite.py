#!/usr/bin/env python3
"""
=============================================================================
EduFAMS Master Date Form Testing Suite (ISTQB Standard)
Automated Visual & Logic Verification across 32 Date Scenarios (TC-DATE-001 to 032)
Features:
  - Dynamic Floating HUD with Date Test vector badges.
  - Interactive element highlighting before each date action.
  - Paced execution (--slow-mo) for live visual observation on Hyprland Workspace 1.
  - Safe evidence capture (/tmp/evidence_date fallback for sandbox read-only filesystems).
  - Comprehensive Markdown summary report detailing Defended vs Defect vulnerabilities,
    storage lifecycle parity, and off-by-one timezone shift checks.
=============================================================================
"""

import argparse
import asyncio
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List
from playwright.async_api import async_playwright, Page, Locator

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parents[1]
DATA_FILE = SCRIPT_DIR / "date_test_data.json"
sys.path.insert(0, str(SCRIPT_DIR))


def get_safe_evidence_dir() -> Path:
    try:
        candidate = SCRIPT_DIR / "evidence_date"
        candidate.mkdir(parents=True, exist_ok=True)
        test_file = candidate / ".write_test"
        with open(test_file, "w") as f:
            f.write("test")
        test_file.unlink()
        return candidate
    except Exception:
        fallback = Path("/tmp/evidence_date")
        fallback.mkdir(parents=True, exist_ok=True)
        return fallback


EVIDENCE_DIR = get_safe_evidence_dir()


class Ansi:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"


class MasterDateSuiteRunner:
    """Master orchestrator for executing all 32 date form testcases visually."""

    def __init__(
        self,
        base_url: str = "https://admin.20-255-158-192.sslip.io",
        eservice_url: str = "https://eservice.20-255-158-192.sslip.io",
        headed: bool = True,
        slow_mo: int = 400,
        hold: int = 10,
        selected_groups: list = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.eservice_url = eservice_url.rstrip("/")
        self.headed = headed
        self.slow_mo = slow_mo if headed else 0
        self.hold = hold
        self.selected_groups = selected_groups or [1, 2, 3, 4, 5]
        self.results: List[Dict[str, Any]] = []
        self.timestamp = int(time.time())
        self.start_time = None
        self.end_time = None

        if DATA_FILE.exists():
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                self.config = json.load(f)
        else:
            self.config = {}

        self.parent_nric = self.config.get("accounts", {}).get("parent", {}).get("nric", "S7654321B")

    def log(self, tag: str, msg: str, color: str = Ansi.CYAN):
        now = datetime.now().strftime("%H:%M:%S")
        print(f"{Ansi.BOLD}[{now}] [{tag:<12}]{Ansi.RESET} {color}{msg}{Ansi.RESET}")

    def record_finding(self, test_id: str, title: str, group: str, verdict: str, details: str, evidence: str = ""):
        self.results.append({
            "test_id": test_id,
            "title": title,
            "group": group,
            "verdict": verdict,
            "details": details,
            "evidence": evidence,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        if verdict == "PASS":
            badge = f"{Ansi.GREEN}✓ PASS{Ansi.RESET}"
        elif verdict == "DEFENDED":
            badge = f"{Ansi.GREEN}🛡️ DEFENDED{Ansi.RESET}"
        elif verdict == "DEFECT":
            badge = f"{Ansi.RED}💥 DEFECT FOUND{Ansi.RESET}"
        else:
            badge = f"{Ansi.YELLOW}⚠️ WARNING{Ansi.RESET}"
        print(f"       -> {badge} | [{test_id}] {title}: {details}")

    async def update_hud(self, page: Page, text: str, badge_type: str = "DATE", bg_color: str = "#0f172a", text_color: str = "#38bdf8"):
        """Injects or updates a live floating HUD badge on the webpage for transparent observation."""
        try:
            escaped_text = text.replace("'", "\\'")
            badge_color = "#3b82f6" if badge_type == "DATE" else ("#16a34a" if badge_type == "PASS" else "#ef4444")
            await page.evaluate(f"""() => {{
                let hud = document.getElementById('date-test-hud');
                if (!hud) {{
                    hud = document.createElement('div');
                    hud.id = 'date-test-hud';
                    document.body.appendChild(hud);
                }}
                hud.innerHTML = '<span style="background:{badge_color};color:#fff;padding:2px 8px;border-radius:12px;font-size:11px;font-weight:700;margin-right:8px;">{badge_type}</span> {escaped_text}';
                hud.style.cssText = 'position:fixed;top:16px;left:50%;transform:translateX(-50%);background:{bg_color};color:{text_color};padding:8px 18px;border-radius:24px;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:13px;font-weight:600;z-index:9999999;box-shadow:0 8px 24px rgba(0,0,0,0.45);border:1.5px solid {text_color};pointer-events:none;transition:all 0.25s ease;display:flex;align-items:center;letter-spacing:0.3px;';
            }}""")
        except Exception:
            pass

    async def visual_click(self, page: Page, locator: Locator, hud_text: str = ""):
        """Visually highlights an element before clicking it."""
        if hud_text:
            await self.update_hud(page, hud_text)
        try:
            await locator.highlight()
        except Exception:
            pass
        if self.headed and self.slow_mo:
            await page.wait_for_timeout(int(self.slow_mo * 0.4))
        await locator.click()

    async def visual_fill(self, page: Page, locator: Locator, value: str, hud_text: str = ""):
        """Visually highlights an element before typing into it."""
        if hud_text:
            await self.update_hud(page, hud_text)
        try:
            await locator.highlight()
        except Exception:
            pass
        if self.headed and self.slow_mo:
            await page.wait_for_timeout(int(self.slow_mo * 0.3))
        await locator.fill(value)

    async def safe_screenshot(self, page: Page, filename: str) -> str:
        """Saves screenshot safely with fallback to /tmp."""
        target = str(EVIDENCE_DIR / filename)
        try:
            await page.screenshot(path=target)
            return target
        except Exception:
            try:
                fallback = f"/tmp/evidence_date/{filename}"
                Path("/tmp/evidence_date").mkdir(parents=True, exist_ok=True)
                await page.screenshot(path=fallback)
                return fallback
            except Exception:
                return target

    # -------------------------------------------------------------------------
    # AUTHENTICATION HELPERS
    # -------------------------------------------------------------------------

    async def authenticate_admin(self, page: Page):
        """Authenticates MOE HQ Administrator via Microsoft SSO Simulator."""
        self.log("AUTH", "Đăng nhập Microsoft SSO với tài khoản Quản trị Bộ (admin@IAM.edu.vn)")
        await page.context.clear_cookies()
        try:
            await page.evaluate("() => { try { localStorage.clear(); sessionStorage.clear(); } catch(e){} }")
        except Exception:
            pass

        await page.goto(f"{self.base_url}/login", wait_until="networkidle")
        await self.update_hud(page, "Đăng nhập Cổng Quản trị MOE HQ via Microsoft SSO...", "AUTH", "#0f172a", "#38bdf8")

        ms_btn = page.locator('button:has-text("Sign in with Microsoft")')
        if await ms_btn.is_visible():
            await self.visual_click(page, ms_btn, "Nhấn 'Sign in with Microsoft'")
            await page.wait_for_url("**/microsoft-provider/**", timeout=25000)

        tile = page.locator(".account-tile:has-text('admin@IAM.edu.vn')").first
        await tile.wait_for(state="visible", timeout=15000)
        await self.visual_click(page, tile, "Chọn tài khoản admin@IAM.edu.vn")

        await page.wait_for_url(f"{self.base_url}/**", timeout=30000)
        await page.wait_for_load_state("networkidle")

        exit_btn = page.get_by_role("button", name="Exit", exact=True)
        if await exit_btn.count() > 0 and await exit_btn.is_visible():
            await exit_btn.click()
            await page.wait_for_timeout(800)

        self.log("AUTH", "✓ Đăng nhập Quản trị viên MOE HQ thành công", Ansi.GREEN)

    # -------------------------------------------------------------------------
    # MASTER SUITE RUNNER
    # -------------------------------------------------------------------------

    async def run(self):
        self.start_time = datetime.now()
        self.log("INIT", "=========================================================", Ansi.BOLD)
        self.log("INIT", "Khởi Động Master Date Form Testing Suite (32 Scenarios)", Ansi.BOLD)
        self.log("INIT", f"Target Admin: {self.base_url} | E-Service: {self.eservice_url}")
        self.log("INIT", f"Headed: {self.headed} | slow_mo: {self.slow_mo}ms | hold: {self.hold}s")
        self.log("INIT", f"Selected Groups: {self.selected_groups}")
        self.log("INIT", "=========================================================", Ansi.BOLD)

        async with async_playwright() as p:
            launch_args = ["--ignore-certificate-errors", "--ozone-platform-hint=auto"]
            if self.headed:
                launch_args.extend(["--class=Chromium", f"--app={self.base_url}/login"])

            browser = await p.chromium.launch(
                headless=not self.headed,
                slow_mo=self.slow_mo,
                args=launch_args,
            )
            context = await browser.new_context(
                viewport={"width": 1440, "height": 900},
                ignore_https_errors=True,
            )
            page = await context.new_page()

            try:
                # Groups 1, 2, 3: Input Formats, BVA Boundaries & Malformed/Security
                active_g123 = [g for g in [1, 2, 3] if g in self.selected_groups]
                if active_g123:
                    self.log("DISPATCH", f"Khởi chạy Nhóm 1, 2, 3 (Date Inputs & Boundaries)...", Ansi.HEADER)
                    try:
                        from test_date_inputs_and_boundaries import run_date_input_bva_tests
                        await run_date_input_bva_tests(self, page)
                    except Exception as e:
                        self.log("DISPATCH", f"Lỗi chạy test_date_inputs_and_boundaries: {e}", Ansi.RED)

                # Groups 4, 5: Business Ranges & Persistence/Timezone Parity
                active_g45 = [g for g in [4, 5] if g in self.selected_groups]
                if active_g45:
                    self.log("DISPATCH", f"Khởi chạy Nhóm 4, 5 (Business Rules & Persistence Parity)...", Ansi.HEADER)
                    try:
                        from test_date_business_and_persistence import run_date_business_persistence_tests
                        await run_date_business_persistence_tests(self, page)
                    except Exception as e:
                        self.log("DISPATCH", f"Lỗi chạy test_date_business_and_persistence: {e}", Ansi.RED)

                await self.update_hud(page, f"✓ HOÀN TẤT BỘ TEST FORM DATE! (Giữ mở {self.hold}s)", "COMPLETED", "#064e3b", "#34d399")
                if self.headed and self.hold > 0:
                    self.log("DONE", f"Giữ trình duyệt mở {self.hold}s để quan sát...", Ansi.GREEN)
                    await page.wait_for_timeout(self.hold * 1000)

            except Exception as exc:
                self.log("ERROR", f"Execution encountered exception: {exc}", Ansi.RED)
                await self.safe_screenshot(page, "error_date_suite_crash.png")
            finally:
                await browser.close()

        self.end_time = datetime.now()
        self.generate_report()

    # -------------------------------------------------------------------------
    # REPORT GENERATOR
    # -------------------------------------------------------------------------

    def generate_report(self):
        duration = (self.end_time - self.start_time).total_seconds() if self.start_time and self.end_time else 0
        total = len(self.results)
        passed = sum(1 for r in self.results if r["verdict"] in ["PASS", "DEFENDED"])
        defects = sum(1 for r in self.results if r["verdict"] == "DEFECT")
        warnings = sum(1 for r in self.results if r["verdict"] == "WARNING")

        report_md = f"""# 📅 EduFAMS Date Form Testing Execution Report
## Comprehensive Date Format, BVA Boundary & Lifecycle Parity Audit

- **Execution Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **Total Execution Time:** {duration:.1f} seconds
- **Total Scenarios Evaluated:** {total}
- **Passed / Defended Scenarios:** **{passed} / {total}**
- **Defects Identified:** **{defects}**
- **Warnings / Observations:** **{warnings}**

---

## 📊 Summary of Scenarios & Findings

| Test ID | Scenario / Test Objective | Group | Verdict | Observable Result & Diagnostic Observations | Evidence |
| :--- | :--- | :---: | :---: | :--- | :--- |
"""
        for r in self.results:
            if r["verdict"] == "PASS":
                badge = "✓ **PASS**"
            elif r["verdict"] == "DEFENDED":
                badge = "🛡️ **DEFENDED**"
            elif r["verdict"] == "DEFECT":
                badge = "💥 **DEFECT**"
            else:
                badge = "⚠️ **WARNING**"
            ev_name = Path(r["evidence"]).name if r["evidence"] else "N/A"
            report_md += f"| **{r['test_id']}** | {r['title']} | `{r['group']}` | {badge} | {r['details']} | [`{ev_name}`]({r['evidence']}) |\n"

        report_md += f"""
---

## 🔍 Key Architectural Insights for Dev Team

1. **Date-Only Wire Serialization:**
   Always serialize calendar dates as pure date strings (`YYYY-MM-DD`, e.g. `"2026-05-15"`) across HTTP payloads instead of ISO-8601 UTC timestamps with timezone offsets (`"2026-05-14T16:00:00.000Z"`). This eliminates the classic **off-by-one day bug** when clients operate in non-UTC zones.
2. **Strict Client-Side BVA Validation:**
   Enforce day validation based on the specific month (e.g., February 28/29, April 30) before submitting to prevent unparsed payload exceptions.
3. **View/Edit Parity:**
   Verify that Edit forms parse stored date strings in the user's local timezone (`DD/MM/YYYY`) without shifting or wiping the field blank.
4. **Excel Export Date Types:**
   Format date cells in `.xlsx` exports as real ISO Date types with `DD/MM/YYYY` cell formatting rather than raw strings.

---
*Report generated automatically by `run_master_date_suite.py` (/combo-qa & /combo-code standard).*
"""
        target_file = SCRIPT_DIR / "DATE_TESTING_EXECUTION_REPORT.md"
        try:
            with open(target_file, "w", encoding="utf-8") as f:
                f.write(report_md)
            self.log("REPORT", f"✓ Đã xuất báo cáo: {target_file}", Ansi.GREEN)
        except Exception:
            fallback = Path("/tmp/DATE_TESTING_EXECUTION_REPORT.md")
            with open(fallback, "w", encoding="utf-8") as f:
                f.write(report_md)
            self.log("REPORT", f"✓ Đã xuất báo cáo fallback: {fallback}", Ansi.GREEN)


def main():
    parser = argparse.ArgumentParser(description="EduFAMS Master Date Form Visual Runner")
    parser.add_argument("--base-url", default="https://admin.20-255-158-192.sslip.io", help="Admin Portal URL")
    parser.add_argument("--eservice-url", default="https://eservice.20-255-158-192.sslip.io", help="Parent Portal URL")
    parser.add_argument("--headed", action="store_true", default=True, help="Run browser in headed mode")
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode")
    parser.add_argument("--slow-mo", type=int, nargs="?", const=400, default=400, help="Paced delay between actions in ms")
    parser.add_argument("--hold", type=int, nargs="?", const=10, default=5, help="Seconds to hold browser open upon completion")
    parser.add_argument("--groups", default="1,2,3,4,5", help="Comma-separated groups to run (e.g. 1,2,3,4,5)")
    args = parser.parse_args()

    is_headed = False if args.headless else args.headed
    selected_groups = [int(g.strip()) for g in args.groups.split(",") if g.strip().isdigit()]

    runner = MasterDateSuiteRunner(
        base_url=args.base_url,
        eservice_url=args.eservice_url,
        headed=is_headed,
        slow_mo=args.slow_mo,
        hold=args.hold,
        selected_groups=selected_groups,
    )
    asyncio.run(runner.run())


if __name__ == "__main__":
    main()
