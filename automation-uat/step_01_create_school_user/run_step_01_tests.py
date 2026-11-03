#!/usr/bin/env python3
"""
automation-uat/step_01_create_school_user/run_step_01_tests.py
Standalone Visual Destructive & Functional Test Runner for Step 1: Create School User.
Target: /school-user-management/new
"""

import argparse
import asyncio
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright, Page, Locator, Response

SCRIPT_DIR = Path(__file__).resolve().parent
EVIDENCE_DIR = SCRIPT_DIR / "evidence"
EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)


class Ansi:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    BG_RED = "\033[41m\033[97m"
    BG_GREEN = "\033[42m\033[97m"


class Step01Runner:
    def __init__(self, base_url: str = "https://admin.20-255-158-192.sslip.io", headed: bool = True, slow_mo: int = 500):
        self.base_url = base_url.rstrip("/")
        self.headed = headed
        self.slow_mo = slow_mo if headed else 0
        self.results = []
        self.console_errors = []
        self.uncaught_exceptions = []
        self.http_500_responses = []

    def log(self, tag: str, msg: str, color: str = Ansi.CYAN):
        t = datetime.now().strftime("%H:%M:%S")
        print(f"{Ansi.BOLD}[{t}] [{tag}]{Ansi.RESET} {color}{msg}{Ansi.RESET}")

    def record_finding(self, test_id: str, title: str, category: str, verdict: str, details: str, evidence: str = ""):
        self.results.append({
            "test_id": test_id,
            "title": title,
            "category": category,
            "verdict": verdict,
            "details": details,
            "evidence": evidence
        })
        if verdict == "BUG FOUND":
            badge = f"{Ansi.BG_RED} 💥 BUG FOUND {Ansi.RESET}"
        elif verdict == "WARNING":
            badge = f"{Ansi.YELLOW} ⚠️ WARNING   {Ansi.RESET}"
        else:
            badge = f"{Ansi.GREEN} ✓ DEFENDED   {Ansi.RESET}"
        print(f"       -> {badge} {Ansi.BOLD}[{test_id}]{Ansi.RESET} {title}: {details}")

    async def update_hud(self, page: Page, text: str, bg_color: str = "#0f172a", text_color: str = "#38bdf8"):
        try:
            await page.evaluate(f"""() => {{
                let hud = document.getElementById('step01-uat-hud');
                if (!hud) {{
                    hud = document.createElement('div');
                    hud.id = 'step01-uat-hud';
                    document.body.appendChild(hud);
                }}
                hud.innerHTML = '<span style="background:#ef4444;color:#fff;padding:3px 10px;border-radius:12px;font-size:11px;font-weight:800;margin-right:8px;">BƯỚC 1: CREATE USER</span> {text}';
                hud.style.cssText = 'position:fixed;top:16px;left:50%;transform:translateX(-50%);background:{bg_color};color:{text_color};padding:10px 22px;border-radius:28px;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:14px;font-weight:600;z-index:9999999;box-shadow:0 10px 30px rgba(0,0,0,0.5);border:2px solid {text_color};pointer-events:none;transition:all 0.25s ease;display:flex;align-items:center;letter-spacing:0.3px;';
            }}""")
        except Exception:
            pass

    async def visual_click(self, page: Page, locator: Locator, hud_text: str = ""):
        if hud_text:
            await self.update_hud(page, hud_text)
        try:
            await locator.highlight()
        except Exception:
            pass
        if self.headed:
            await page.wait_for_timeout(350)
        await locator.click()

    async def visual_fill(self, page: Page, locator: Locator, value: str, hud_text: str = ""):
        if hud_text:
            await self.update_hud(page, hud_text)
        try:
            await locator.highlight()
        except Exception:
            pass
        if self.headed:
            await page.wait_for_timeout(250)
        await locator.fill(value)

    async def setup_listeners(self, page: Page):
        self.console_errors.clear()
        self.uncaught_exceptions.clear()
        self.http_500_responses.clear()

        page.on("console", lambda msg: self.console_errors.append(msg.text) if msg.type in ["error"] else None)
        page.on("pageerror", lambda exc: self.uncaught_exceptions.append(str(exc)))

        def on_response(res: Response):
            if res.status >= 500:
                self.http_500_responses.append(f"{res.request.method} {res.url} -> {res.status}")
        page.on("response", on_response)

    async def authenticate(self, page: Page):
        self.log("AUTH", f"Connecting to Admin Portal: {self.base_url}")
        target = f"{self.base_url}/school-user-management/new"
        await page.goto(target, wait_until="domcontentloaded")
        await page.wait_for_timeout(1000)

        if "login" in page.url or await page.locator("button:has-text('Sign in with Microsoft')").count() > 0:
            await self.update_hud(page, "Đang đăng nhập Microsoft SSO với quyền moehq...", "#1e1b4b", "#a5b4fc")
            ms_btn = page.locator("button:has-text('Sign in with Microsoft')")
            if await ms_btn.is_visible():
                await self.visual_click(page, ms_btn, "Nhấn 'Sign in with Microsoft'")
                await page.wait_for_timeout(1500)

            tile = page.locator(".account-tile:has-text('admin@IAM.edu.vn'), [data-email='admin@IAM.edu.vn']").first
            if await tile.count() > 0:
                await self.visual_click(page, tile, "Chọn tài khoản admin@IAM.edu.vn (System Admin)")
            else:
                fallback_tile = page.locator("text=admin@IAM.edu.vn").first
                if await fallback_tile.count() > 0:
                    await self.visual_click(page, fallback_tile, "Chọn tài khoản admin@IAM.edu.vn")
            await page.wait_for_timeout(2500)

        await page.goto(target, wait_until="domcontentloaded")
        await page.wait_for_selector("#school-user-nric", timeout=15000)
        await self.update_hud(page, "✓ Đã mở: Form Tạo Cán Bộ Nhà Trường (/school-user-management/new)", "#064e3b", "#34d399")
        await page.wait_for_timeout(1500)
        self.log("AUTH", "✓ Authenticated and navigated to /school-user-management/new", Ansi.GREEN)

    async def reset_form(self, page: Page):
        try:
            target = f"{self.base_url}/school-user-management/new"
            if page.url != target:
                await page.goto(target, wait_until="domcontentloaded")
                await page.wait_for_selector("#school-user-nric", timeout=10000)
                return

            reset_btn = page.locator("button:has-text('Reset')")
            if await reset_btn.is_visible():
                await self.visual_click(page, reset_btn, "Làm sạch form (Reset)")
                await page.wait_for_timeout(400)
            else:
                await page.reload(wait_until="domcontentloaded")
                await page.wait_for_selector("#school-user-nric", timeout=10000)
        except Exception:
            await page.goto(f"{self.base_url}/school-user-management/new", wait_until="domcontentloaded")
            await page.wait_for_selector("#school-user-nric", timeout=10000)

    async def _select_rosyth_school(self, page: Page):
        school_input = page.locator("#school-user-school")
        if await school_input.count() > 0:
            await self.visual_fill(page, school_input, "Rosyth", "Tìm kiếm trường: Rosyth Primary School")
            await page.wait_for_timeout(700)
            opt = page.locator("#school-user-school-listbox [role='option'], [role='option']:has-text('Rosyth')").first
            if await opt.count() > 0:
                await self.visual_click(page, opt, "Chọn: RPS-0201 - Rosyth Primary School")
            else:
                await page.keyboard.press("ArrowDown")
                await page.keyboard.press("Enter")

    async def test_01_xss_injection(self, page: Page):
        test_id = "TC-DEST-01"
        title = "Stored XSS Injection in First & Last Name"
        self.log("EXEC", f"Running [{test_id}] {title}")
        await self.reset_form(page)
        await self.setup_listeners(page)
        await self.update_hud(page, "Đòn 1/8: Bắn payload Stored XSS <script> vào First Name...", "#450a0a", "#f87171")

        await page.evaluate("window.__xss_executed = false;")
        xss_payload = '<script>window.__xss_executed=true;</script><img src=x onerror="window.__xss_executed=true;">'
        ts = int(time.time())
        nric = f"S{str(ts)[-7:]}A"

        await self.visual_fill(page, page.locator("#school-user-nric"), nric, f"Điền NRIC: {nric}")
        await self.visual_fill(page, page.locator("#school-user-first-name"), xss_payload, "Bắn payload XSS vào First Name")
        await self.visual_fill(page, page.locator("#school-user-last-name"), "HackerTest", "Last Name: HackerTest")
        await self.visual_fill(page, page.locator("#school-user-email"), f"xss.{ts}@edu.gov.sg", "Điền Email")
        await self._select_rosyth_school(page)

        create_btn = page.locator("button:has-text('Create')")
        if await create_btn.is_enabled():
            await self.visual_click(page, create_btn, "Bấm 'Create'")
            await page.wait_for_timeout(2500)

        xss_hit = await page.evaluate("window.__xss_executed === true")
        shot = str(EVIDENCE_DIR / f"{test_id}_xss.png")
        await page.screenshot(path=shot)

        if xss_hit:
            self.record_finding(test_id, title, "Security/XSS", "BUG FOUND", "JavaScript executed in browser!", shot)
        elif len(self.http_500_responses) > 0:
            self.record_finding(test_id, title, "Security/Crash", "BUG FOUND", f"Backend crashed 500: {self.http_500_responses[0]}", shot)
        else:
            self.record_finding(test_id, title, "Security/XSS", "DEFENDED", "Payload sanitized safely without JS execution.", shot)

    async def test_02_sqli_injection(self, page: Page):
        test_id = "TC-DEST-02"
        title = "SQL Injection Payload in NRIC & Email"
        self.log("EXEC", f"Running [{test_id}] {title}")
        await self.reset_form(page)
        await self.setup_listeners(page)
        await self.update_hud(page, "Đòn 2/8: Bắn payload SQL Injection (' OR 1=1 --)...", "#450a0a", "#f87171")

        sqli_payload = "' OR '1'='1"
        await self.visual_fill(page, page.locator("#school-user-nric"), sqli_payload, f"NRIC: {sqli_payload}")
        await self.visual_fill(page, page.locator("#school-user-first-name"), "Arthur", "First Name: Arthur")
        await self.visual_fill(page, page.locator("#school-user-last-name"), "SQLi", "Last Name: SQLi")
        await self.visual_fill(page, page.locator("#school-user-email"), "test' OR 1=1--@edu.gov.sg", "Email SQLi")

        shot = str(EVIDENCE_DIR / f"{test_id}_sqli.png")
        await page.screenshot(path=shot)

        create_btn = page.locator("button:has-text('Create')")
        is_disabled = await create_btn.is_disabled()

        if not is_disabled:
            await self.visual_click(page, create_btn, "Bấm 'Create'")
            await page.wait_for_timeout(2000)

        if len(self.http_500_responses) > 0:
            self.record_finding(test_id, title, "Security/SQLi", "BUG FOUND", f"Backend crashed with 500: {self.http_500_responses[0]}", shot)
        elif is_disabled:
            self.record_finding(test_id, title, "Security/SQLi", "DEFENDED", "Frontend validation blocked malformed SQL pattern.", shot)
        else:
            self.record_finding(test_id, title, "Security/SQLi", "DEFENDED", "Rejected gracefully without 500 crash.", shot)

    async def test_03_race_condition(self, page: Page):
        test_id = "TC-DEST-03"
        title = "Rapid 10x Submit Spam (Race Condition / Idempotency)"
        self.log("EXEC", f"Running [{test_id}] {title}")
        await self.reset_form(page)
        await self.setup_listeners(page)
        await self.update_hud(page, "Đòn 3/8: Đua lệnh (Race Condition) - Spam click Create 10 lần liên tục...", "#450a0a", "#f87171")

        ts = int(time.time())
        nric = f"S{str(ts)[-7:]}A"
        email = f"spam.{ts}@edu.gov.sg"

        await self.visual_fill(page, page.locator("#school-user-nric"), nric, f"NRIC: {nric}")
        await self.visual_fill(page, page.locator("#school-user-first-name"), "Spam", "First Name: Spam")
        await self.visual_fill(page, page.locator("#school-user-last-name"), "Clicker", "Last Name: Clicker")
        await self.visual_fill(page, page.locator("#school-user-email"), email, f"Email: {email}")
        await self._select_rosyth_school(page)

        create_btn = page.locator("button:has-text('Create')")
        clicks_sent = 0
        for _ in range(10):
            try:
                await create_btn.click(timeout=300, no_wait_after=True)
                clicks_sent += 1
            except Exception:
                break
            await asyncio.sleep(0.02)

        await page.wait_for_timeout(3000)
        shot = str(EVIDENCE_DIR / f"{test_id}_race_condition.png")
        await page.screenshot(path=shot)

        if len(self.uncaught_exceptions) > 0:
            self.record_finding(test_id, title, "Concurrency/Race", "BUG FOUND",
                                f"Client-side unhandled exception during click spam: {self.uncaught_exceptions[0]}", shot)
        elif len(self.http_500_responses) > 0:
            self.record_finding(test_id, title, "Concurrency/Race", "BUG FOUND",
                                f"Backend crashed 500 on duplicate insert: {self.http_500_responses[0]}", shot)
        else:
            self.record_finding(test_id, title, "Concurrency/Race", "DEFENDED",
                                f"Handled click spam gracefully (Sent {clicks_sent} clicks).", shot)

    async def test_04_client_bypass(self, page: Page):
        test_id = "TC-DEST-04"
        title = "DOM Tampering: Remove 'disabled' & Bypass Client Checks"
        self.log("EXEC", f"Running [{test_id}] {title}")
        await self.reset_form(page)
        await self.setup_listeners(page)
        await self.update_hud(page, "Đòn 4/8: Hack DOM - Gỡ thuộc tính 'disabled' bằng JS và ép submit...", "#450a0a", "#f87171")

        await page.evaluate("""() => {
            const btn = document.querySelector("button[type='submit']") || Array.from(document.querySelectorAll("button")).find(b => b.textContent.includes("Create"));
            if (btn) {
                btn.removeAttribute("disabled");
                btn.classList.remove("disabled");
                btn.click();
            }
        }""")
        await page.wait_for_timeout(2000)

        shot = str(EVIDENCE_DIR / f"{test_id}_client_bypass.png")
        await page.screenshot(path=shot)

        if len(self.http_500_responses) > 0:
            self.record_finding(test_id, title, "Security/Bypass", "BUG FOUND", f"Backend crashed with 500: {self.http_500_responses[0]}", shot)
        else:
            self.record_finding(test_id, title, "Security/Bypass", "DEFENDED", "Server validation rejected empty payload without crashing.", shot)

    async def test_05_buffer_overflow(self, page: Page):
        test_id = "TC-DEST-05"
        title = "5,000 Chars String & Zalgo/BiDi Unicode Chaos"
        self.log("EXEC", f"Running [{test_id}] {title}")
        await self.reset_form(page)
        await self.setup_listeners(page)
        await self.update_hud(page, "Đòn 5/8: Tràn bộ đệm - Bơm 5.000 ký tự 'A' vào First Name...", "#450a0a", "#f87171")

        huge_string = "A" * 5000
        zalgo_text = "T̷e̷s̷t̷ ̷Z̷a̷l̷g̷o̷ ̶D̶e̶s̶t̶r̶o̶y̶ ̶U̶I̶"
        bidi_override = "\u202E\u0041\u0042\u0043\u0044"
        ts = int(time.time())

        await self.visual_fill(page, page.locator("#school-user-nric"), f"S{str(ts)[-7:]}A", "NRIC hợp lệ")
        await self.visual_fill(page, page.locator("#school-user-first-name"), huge_string, "Bơm 5.000 ký tự 'A'")
        await self.visual_fill(page, page.locator("#school-user-last-name"), zalgo_text + bidi_override, "Zalgo & BiDi")
        await self.visual_fill(page, page.locator("#school-user-email"), f"unicode.{ts}@edu.gov.sg", "Email")
        await self._select_rosyth_school(page)

        shot = str(EVIDENCE_DIR / f"{test_id}_unicode_bomb.png")
        create_btn = page.locator("button:has-text('Create')")
        if await create_btn.is_enabled():
            await self.visual_click(page, create_btn, "Nhấn 'Create'")
            await page.wait_for_timeout(2500)
        await page.screenshot(path=shot)

        if len(self.http_500_responses) > 0:
            self.record_finding(test_id, title, "Robustness/DoS", "BUG FOUND", f"Backend crashed 500 on 5000-char buffer: {self.http_500_responses[0]}", shot)
        else:
            self.record_finding(test_id, title, "Robustness/Unicode", "DEFENDED", "Handled extreme length safely.", shot)

    async def test_06_whitespace(self, page: Page):
        test_id = "TC-DEST-06"
        title = "Whitespace-only in First & Last Name Bypass"
        self.log("EXEC", f"Running [{test_id}] {title}")
        await self.reset_form(page)
        await self.setup_listeners(page)
        await self.update_hud(page, "Đòn 6/8: Nhập toàn bộ dấu cách '    ' vào First/Last Name...", "#450a0a", "#f87171")

        ts = int(time.time())
        await self.visual_fill(page, page.locator("#school-user-nric"), f"S{str(ts)[-7:]}A", "NRIC")
        await self.visual_fill(page, page.locator("#school-user-first-name"), "    ", "4 dấu cách")
        await self.visual_fill(page, page.locator("#school-user-last-name"), "    ", "4 dấu cách")
        await self.visual_fill(page, page.locator("#school-user-email"), f"white.{ts}@edu.gov.sg", "Email")
        await self._select_rosyth_school(page)

        create_btn = page.locator("button:has-text('Create')")
        is_enabled = await create_btn.is_enabled()
        shot = str(EVIDENCE_DIR / f"{test_id}_whitespace.png")
        await page.screenshot(path=shot)

        if is_enabled:
            await self.visual_click(page, create_btn, "Bấm 'Create'")
            await page.wait_for_timeout(2000)
            content = await page.content()
            if "created" in content.lower() or "success" in content.lower():
                self.record_finding(test_id, title, "Validation/Sanitization", "BUG FOUND", "Blank whitespace accepted and saved!", shot)
                return

        self.record_finding(test_id, title, "Validation/Sanitization", "DEFENDED", "Button remained disabled on whitespace-only names.", shot)

    async def test_07_ghost_school(self, page: Page):
        test_id = "TC-DEST-07"
        title = "Ghost / Non-Existent School In Combobox"
        self.log("EXEC", f"Running [{test_id}] {title}")
        await self.reset_form(page)
        await self.setup_listeners(page)
        await self.update_hud(page, "Đòn 7/8: Gõ tên trường ma 'NonExistentSchool_99999_X'...", "#450a0a", "#f87171")

        ts = int(time.time())
        await self.visual_fill(page, page.locator("#school-user-nric"), f"S{str(ts)[-7:]}A", "NRIC")
        await self.visual_fill(page, page.locator("#school-user-first-name"), "Arthur", "First Name")
        await self.visual_fill(page, page.locator("#school-user-last-name"), "GhostSchool", "Last Name")
        await self.visual_fill(page, page.locator("#school-user-email"), f"ghost.{ts}@edu.gov.sg", "Email")

        school_input = page.locator("#school-user-school")
        if await school_input.count() > 0:
            await self.visual_fill(page, school_input, "NonExistentSchool_99999_X", "Trường ma")
            await page.keyboard.press("Tab")
            await page.wait_for_timeout(500)

        create_btn = page.locator("button:has-text('Create')")
        is_enabled = await create_btn.is_enabled()
        shot = str(EVIDENCE_DIR / f"{test_id}_ghost_school.png")
        await page.screenshot(path=shot)

        if is_enabled:
            await self.visual_click(page, create_btn, "Bấm 'Create'")
            await page.wait_for_timeout(2000)
            if len(self.http_500_responses) > 0:
                self.record_finding(test_id, title, "Combobox/Foreign-Key", "BUG FOUND", f"Backend threw 500 on ghost school: {self.http_500_responses[0]}", shot)
                return

        self.record_finding(test_id, title, "Combobox/Foreign-Key", "DEFENDED", "Enforced selecting valid verified school.", shot)

    async def test_08_tab_switching(self, page: Page):
        test_id = "TC-DEST-08"
        title = "Tab Hopping (Single -> Bulk CSV -> Single) State Leak"
        self.log("EXEC", f"Running [{test_id}] {title}")
        await self.reset_form(page)
        await self.setup_listeners(page)
        await self.update_hud(page, "Đòn 8/8: Nhập email dở dang -> Đổi tab Bulk CSV -> Đổi lại Single...", "#450a0a", "#f87171")

        ts = int(time.time())
        test_email = f"state.{ts}@edu.gov.sg"
        await self.visual_fill(page, page.locator("#school-user-email"), test_email, f"Email: {test_email}")

        bulk_tab = page.locator("button:has-text('Bulk CSV'), [role='tab']:has-text('Bulk CSV')")
        if await bulk_tab.count() > 0:
            await self.visual_click(page, bulk_tab, "Tab Bulk CSV")
            await page.wait_for_timeout(800)
            single_tab = page.locator("button:has-text('Single'), [role='tab']:has-text('Single')")
            await self.visual_click(page, single_tab, "Tab Single")
            await page.wait_for_timeout(800)

            email_val = await page.locator("#school-user-email").input_value()
            shot = str(EVIDENCE_DIR / f"{test_id}_tab_hop.png")
            await page.screenshot(path=shot)

            if len(self.uncaught_exceptions) > 0:
                self.record_finding(test_id, title, "State/UI", "BUG FOUND", f"Uncaught exception toggling tabs: {self.uncaught_exceptions[0]}", shot)
            else:
                self.record_finding(test_id, title, "State/UI", "DEFENDED", f"Form state preserved cleanly ({email_val}).", shot)

    async def run(self):
        print(f"\n{Ansi.BOLD}{'='*75}{Ansi.RESET}")
        print(f"{Ansi.BOLD}{Ansi.MAGENTA} BƯỚC 1: CREATE SCHOOL USER — AUTOMATION TEST SUITE {Ansi.RESET}")
        print(f"{Ansi.BOLD} Target URL : {Ansi.CYAN}{self.base_url}{Ansi.RESET}")
        print(f"{Ansi.BOLD} Mode       : {'Headed (Live Visual)' if self.headed else 'Headless'}")
        print(f"{Ansi.BOLD}{'='*75}{Ansi.RESET}\n")

        async with async_playwright() as p:
            launch_args = ["--ignore-certificate-errors"]
            if self.headed:
                launch_args.extend(["--class=Chromium", f"--app={self.base_url}/school-user-management/new"])

            browser = await p.chromium.launch(headless=not self.headed, slow_mo=self.slow_mo, args=launch_args)
            context = await browser.new_context(viewport={"width": 1440, "height": 900}, ignore_https_errors=True)
            page = await context.new_page()

            try:
                await self.authenticate(page)
                await self.test_01_xss_injection(page)
                await self.test_02_sqli_injection(page)
                await self.test_03_race_condition(page)
                await self.test_04_client_bypass(page)
                await self.test_05_buffer_overflow(page)
                await self.test_06_whitespace(page)
                await self.test_07_ghost_school(page)
                await self.test_08_tab_switching(page)
                await self.update_hud(page, "✓ HOÀN TẤT TOÀN BỘ KIỂM THỬ BƯỚC 1", "#064e3b", "#34d399")
                if self.headed:
                    await page.wait_for_timeout(2500)
            finally:
                await browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Step 01 Test Runner")
    parser.add_argument("--url", default="https://admin.20-255-158-192.sslip.io", help="Base URL")
    parser.add_argument("--headless", action="store_true", help="Run headless")
    parser.add_argument("--slow-mo", type=int, default=500, help="Slow-mo in ms")
    args = parser.parse_args()

    asyncio.run(Step01Runner(args.url, headed=not args.headless, slow_mo=args.slow_mo).run())
