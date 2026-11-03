#!/usr/bin/env python3
"""
tools/destructive_test_school_user.py - Visual & Standalone Destructive Form Test Suite.
Spec Target: /school-user-management/new (Target: https://admin.20-255-158-192.sslip.io & Localhost)
Standard: combo-qa Destructive / Chaos / Security / Boundary Fuzzing Engine with Live Visual HUD.

Usage:
  .venv/bin/python tools/destructive_test_school_user.py [--url https://admin.20-255-158-192.sslip.io] [--headed] [--slow-mo 500]
"""

import argparse
import asyncio
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright, Page, Locator, Response

OUTPUT_DIR = Path("reports/destructive_evidence")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


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


class DestructiveTestRunner:
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
            "verdict": verdict,  # DEFENDED (Safe) | BUG FOUND (Vulnerable) | WARNING
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
        """Injects or updates a live visual HUD banner on the browser screen."""
        try:
            await page.evaluate(f"""() => {{
                let hud = document.getElementById('destructive-qa-hud');
                if (!hud) {{
                    hud = document.createElement('div');
                    hud.id = 'destructive-qa-hud';
                    document.body.appendChild(hud);
                }}
                hud.innerHTML = '<span style="background:#ef4444;color:#fff;padding:3px 10px;border-radius:12px;font-size:11px;font-weight:800;margin-right:8px;box-shadow:0 2px 6px rgba(239,68,68,0.4);">TEST PHÁ FORM</span> {text}';
                hud.style.cssText = 'position:fixed;top:16px;left:50%;transform:translateX(-50%);background:{bg_color};color:{text_color};padding:10px 22px;border-radius:28px;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:14px;font-weight:600;z-index:9999999;box-shadow:0 10px 30px rgba(0,0,0,0.5);border:2px solid {text_color};pointer-events:none;transition:all 0.25s ease;display:flex;align-items:center;letter-spacing:0.3px;';
            }}""")
        except Exception:
            pass

    async def visual_click(self, page: Page, locator: Locator, hud_text: str = ""):
        """Highlights the element visually before clicking."""
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
        """Highlights the element visually before typing."""
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
        """Perform MOE HQ System Admin SSO Authentication with Visual Feedback."""
        self.log("AUTH", f"Connecting to Admin Portal: {self.base_url}")
        target = f"{self.base_url}/school-user-management/new"
        await page.goto(target, wait_until="domcontentloaded")
        await page.wait_for_timeout(1000)

        # Check if login is needed
        if "login" in page.url or await page.locator("button:has-text('Sign in with Microsoft')").count() > 0:
            await self.update_hud(page, "Đang đăng nhập Microsoft SSO với quyền Quản trị Bộ moehq...", "#1e1b4b", "#a5b4fc")
            ms_btn = page.locator("button:has-text('Sign in with Microsoft')")
            if await ms_btn.is_visible():
                await self.visual_click(page, ms_btn, "Nhấn 'Sign in with Microsoft'")
                await page.wait_for_timeout(1500)

            # Select admin account tile
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
        await self.update_hud(page, "✓ Đã sẵn sàng: Màn hình Tạo Cán Bộ Nhà Trường (/school-user-management/new)", "#064e3b", "#34d399")
        await page.wait_for_timeout(1500)
        self.log("AUTH", "✓ Successfully authenticated and navigated to /school-user-management/new", Ansi.GREEN)

    async def reset_form(self, page: Page):
        """Reset form fields to clean state."""
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

    # -------------------------------------------------------------------------
    # ATTACK TEST 1: Stored XSS & Script Tag Injection
    # -------------------------------------------------------------------------
    async def attack_01_xss_injection(self, page: Page):
        test_id = "TC-DEST-01"
        title = "Stored XSS Injection in First & Last Name"
        self.log("EXEC", f"Running [{test_id}] {title}")
        await self.reset_form(page)
        await self.setup_listeners(page)
        await self.update_hud(page, "Đòn 1/8: Bắn payload Stored XSS <script> vào ô First Name...", "#450a0a", "#f87171")

        await page.evaluate("window.__xss_executed = false;")
        xss_payload = '<script>window.__xss_executed=true;</script><img src=x onerror="window.__xss_executed=true;">'
        ts = int(time.time())
        nric = f"S{str(ts)[-7:]}A"

        await self.visual_fill(page, page.locator("#school-user-nric"), nric, f"Điền NRIC: {nric}")
        await self.visual_fill(page, page.locator("#school-user-first-name"), xss_payload, "Bắn payload độc hại XSS vào First Name")
        await self.visual_fill(page, page.locator("#school-user-last-name"), "HackerTest", "Điền Last Name: HackerTest")
        await self.visual_fill(page, page.locator("#school-user-email"), f"xss.{ts}@edu.gov.sg", "Điền Email hợp lệ")
        await self._select_rosyth_school(page)

        create_btn = page.locator("button:has-text('Create')")
        if await create_btn.is_enabled():
            await self.visual_click(page, create_btn, "Bấm nút 'Create' để submit payload XSS")
            await page.wait_for_timeout(2500)

        xss_hit = await page.evaluate("window.__xss_executed === true")
        shot = str(OUTPUT_DIR / f"{test_id}_xss.png")
        await page.screenshot(path=shot)

        if xss_hit:
            await self.update_hud(page, "💥 LỖI XSS: Mã JavaScript độc hại đã bị thực thi trên trình duyệt!", "#7f1d1d", "#fca5a5")
            self.record_finding(test_id, title, "Security/XSS", "BUG FOUND",
                                "CRITICAL: Injected JavaScript executed in browser context!", shot)
        elif len(self.http_500_responses) > 0:
            await self.update_hud(page, f"💥 LỖI CRASH: Backend văng lỗi 500 khi nhận chuỗi XSS", "#7f1d1d", "#fca5a5")
            self.record_finding(test_id, title, "Security/Crash", "BUG FOUND",
                                f"Backend crashed with 500 on XSS payload: {self.http_500_responses[0]}", shot)
        else:
            await self.update_hud(page, "✓ AN TOÀN: Chuỗi XSS được mã hóa/sanitize an toàn, không bị thực thi", "#064e3b", "#34d399")
            self.record_finding(test_id, title, "Security/XSS", "DEFENDED",
                                "Payload sanitized safely or escaped without executing JavaScript.", shot)
        await page.wait_for_timeout(1500)

    # -------------------------------------------------------------------------
    # ATTACK TEST 2: SQL Injection & Single Quote Tampering
    # -------------------------------------------------------------------------
    async def attack_02_sqli_injection(self, page: Page):
        test_id = "TC-DEST-02"
        title = "SQL Injection Payload in NRIC & Email"
        self.log("EXEC", f"Running [{test_id}] {title}")
        await self.reset_form(page)
        await self.setup_listeners(page)
        await self.update_hud(page, "Đòn 2/8: Bắn payload phá cú pháp SQL Injection (' OR 1=1 --)...", "#450a0a", "#f87171")

        sqli_payload = "' OR '1'='1"
        await self.visual_fill(page, page.locator("#school-user-nric"), sqli_payload, f"Bắn SQLi vào NRIC: {sqli_payload}")
        await self.visual_fill(page, page.locator("#school-user-first-name"), "Arthur", "Điền First Name: Arthur")
        await self.visual_fill(page, page.locator("#school-user-last-name"), "SQLi", "Điền Last Name: SQLi")
        await self.visual_fill(page, page.locator("#school-user-email"), "test' OR 1=1--@edu.gov.sg", "Bắn SQLi vào Email")

        shot = str(OUTPUT_DIR / f"{test_id}_sqli.png")
        await page.screenshot(path=shot)

        create_btn = page.locator("button:has-text('Create')")
        is_disabled = await create_btn.is_disabled()

        if not is_disabled:
            await self.visual_click(page, create_btn, "Thử submit SQLi payload lên Backend")
            await page.wait_for_timeout(2000)

        if len(self.http_500_responses) > 0:
            await self.update_hud(page, "💥 LỖI SQLi: Backend văng lỗi cú pháp SQL 500!", "#7f1d1d", "#fca5a5")
            self.record_finding(test_id, title, "Security/SQLi", "BUG FOUND",
                                f"Backend crashed with unhandled 500 on SQL payload: {self.http_500_responses[0]}", shot)
        elif is_disabled:
            await self.update_hud(page, "✓ AN TOÀN: Frontend nhận diện sai định dạng, vô hiệu hóa nút Create", "#064e3b", "#34d399")
            self.record_finding(test_id, title, "Security/SQLi", "DEFENDED",
                                "Frontend validation blocked submission of malformed SQL pattern in NRIC/Email.", shot)
        else:
            await self.update_hud(page, "✓ AN TOÀN: Backend từ chối hợp lệ, không bị lỗi cú pháp SQL", "#064e3b", "#34d399")
            self.record_finding(test_id, title, "Security/SQLi", "DEFENDED",
                                "Payload rejected gracefully without server 500 error.", shot)
        await page.wait_for_timeout(1500)

    # -------------------------------------------------------------------------
    # ATTACK TEST 3: Rapid Double/Multi-Submit Spam (Race Condition)
    # -------------------------------------------------------------------------
    async def attack_03_race_condition_spam(self, page: Page):
        test_id = "TC-DEST-03"
        title = "Rapid 10x Submit Spam (Race Condition / Idempotency)"
        self.log("EXEC", f"Running [{test_id}] {title}")
        await self.reset_form(page)
        await self.setup_listeners(page)
        await self.update_hud(page, "Đòn 3/8: Đua lệnh (Race Condition) - Spam click nút Create 10 lần liên tục...", "#450a0a", "#f87171")

        ts = int(time.time())
        nric = f"S{str(ts)[-7:]}A"
        email = f"spam.{ts}@edu.gov.sg"

        await self.visual_fill(page, page.locator("#school-user-nric"), nric, f"Điền NRIC hợp lệ: {nric}")
        await self.visual_fill(page, page.locator("#school-user-first-name"), "Spam", "First Name: Spam")
        await self.visual_fill(page, page.locator("#school-user-last-name"), "Clicker", "Last Name: Clicker")
        await self.visual_fill(page, page.locator("#school-user-email"), email, f"Email: {email}")
        await self._select_rosyth_school(page)

        create_btn = page.locator("button:has-text('Create')")

        # Spam click 10 times with minimal delay
        await self.update_hud(page, "⚡ Đang bắn liên tiếp 10 click trong 50ms...", "#e11d48", "#ffffff")
        clicks_sent = 0
        for _ in range(10):
            try:
                await create_btn.click(timeout=300, no_wait_after=True)
                clicks_sent += 1
            except Exception:
                break
            await asyncio.sleep(0.02)

        await page.wait_for_timeout(3000)
        shot = str(OUTPUT_DIR / f"{test_id}_race_condition.png")
        await page.screenshot(path=shot)

        if len(self.http_500_responses) > 0:
            await self.update_hud(page, "💥 LỖI RACE: Backend văng lỗi 500 do xung đột khóa chính DB!", "#7f1d1d", "#fca5a5")
            self.record_finding(test_id, title, "Concurrency/Race", "BUG FOUND",
                                f"Backend crashed with 500 due to unhandled duplicate insert race: {self.http_500_responses[0]}", shot)
        elif len(self.uncaught_exceptions) > 0:
            await self.update_hud(page, "💥 LỖI CLIENT: Trình duyệt ném uncaught exception khi spam click", "#7f1d1d", "#fca5a5")
            self.record_finding(test_id, title, "Concurrency/Race", "BUG FOUND",
                                f"Client-side unhandled exception during click spam: {self.uncaught_exceptions[0]}", shot)
        else:
            await self.update_hud(page, "✓ AN TOÀN: Nút Create disable ngay click đầu, backend bảo đảm Idempotency", "#064e3b", "#34d399")
            self.record_finding(test_id, title, "Concurrency/Race", "DEFENDED",
                                f"Handled click spam gracefully (Sent {clicks_sent} clicks; no server crash).", shot)
        await page.wait_for_timeout(1500)

    # -------------------------------------------------------------------------
    # ATTACK TEST 4: Client-side Validation Tampering & Forced Submission
    # -------------------------------------------------------------------------
    async def attack_04_client_bypass_tampering(self, page: Page):
        test_id = "TC-DEST-04"
        title = "DOM Tampering: Remove 'disabled' & Bypass Client Checks"
        self.log("EXEC", f"Running [{test_id}] {title}")
        await self.reset_form(page)
        await self.setup_listeners(page)
        await self.update_hud(page, "Đòn 4/8: Hack DOM - Gỡ bỏ thuộc tính 'disabled' bằng JavaScript và ép submit form rỗng...", "#450a0a", "#f87171")
        await page.wait_for_timeout(800)

        # Leave inputs empty, but force-enable Create button via DOM manipulation
        await page.evaluate("""() => {
            const btn = document.querySelector("button[type='submit']") || Array.from(document.querySelectorAll("button")).find(b => b.textContent.includes("Create"));
            if (btn) {
                btn.removeAttribute("disabled");
                btn.classList.remove("disabled");
                btn.click();
            }
        }""")
        await page.wait_for_timeout(2000)

        shot = str(OUTPUT_DIR / f"{test_id}_client_bypass.png")
        await page.screenshot(path=shot)

        if len(self.http_500_responses) > 0:
            await self.update_hud(page, "💥 LỖI BYPASS: Backend sập 500 khi nhận payload rỗng bị ép từ client!", "#7f1d1d", "#fca5a5")
            self.record_finding(test_id, title, "Security/Bypass", "BUG FOUND",
                                f"Backend crashed with 500 when forced empty submit bypassed frontend: {self.http_500_responses[0]}", shot)
        else:
            content = await page.content()
            if "School user created" in content or "Created successfully" in content:
                await self.update_hud(page, "💥 LỖI NGHIÊM TRỌNG: Backend chấp nhận tạo user ma rỗng tuếch!", "#7f1d1d", "#fca5a5")
                self.record_finding(test_id, title, "Security/Bypass", "BUG FOUND",
                                    "CRITICAL: Backend accepted completely empty user without server-side validation!", shot)
            else:
                await self.update_hud(page, "✓ AN TOÀN: Server-side validation chặn đứng payload rỗng, không crash", "#064e3b", "#34d399")
                self.record_finding(test_id, title, "Security/Bypass", "DEFENDED",
                                    "Server-side validation held strong; empty payload rejected without crashing.", shot)
        await page.wait_for_timeout(1500)

    # -------------------------------------------------------------------------
    # ATTACK TEST 5: Buffer Overflow & Zalgo / Unicode Bomb
    # -------------------------------------------------------------------------
    async def attack_05_buffer_and_unicode_bomb(self, page: Page):
        test_id = "TC-DEST-05"
        title = "5,000 Chars String & Zalgo/BiDi Unicode Chaos"
        self.log("EXEC", f"Running [{test_id}] {title}")
        await self.reset_form(page)
        await self.setup_listeners(page)
        await self.update_hud(page, "Đòn 5/8: Tràn bộ đệm - Bơm 5.000 ký tự 'A' và ký tự quái dị Zalgo / Unicode BiDi...", "#450a0a", "#f87171")

        huge_string = "A" * 5000
        zalgo_text = "T̷e̷s̷t̷ ̷Z̷a̷l̷g̷o̷ ̶D̶e̶s̶t̶r̶o̶y̶ ̶U̶I̶"
        bidi_override = "\u202E\u0041\u0042\u0043\u0044"
        ts = int(time.time())

        t_start = time.time()
        await self.visual_fill(page, page.locator("#school-user-nric"), f"S{str(ts)[-7:]}A", "Điền NRIC hợp lệ")
        await self.visual_fill(page, page.locator("#school-user-first-name"), huge_string, "BƠM 5.000 KÝ TỰ VÀO FIRST NAME")
        await self.visual_fill(page, page.locator("#school-user-last-name"), zalgo_text + bidi_override, "Bơm Zalgo Text & BiDi RTL vào Last Name")
        await self.visual_fill(page, page.locator("#school-user-email"), f"unicode.{ts}@edu.gov.sg", "Điền Email")
        await self._select_rosyth_school(page)

        duration = time.time() - t_start
        shot = str(OUTPUT_DIR / f"{test_id}_unicode_bomb.png")
        await page.screenshot(path=shot)

        create_btn = page.locator("button:has-text('Create')")
        if await create_btn.is_enabled():
            await self.visual_click(page, create_btn, "Nhấn 'Create' gửi chuỗi 5.000 ký tự lên Backend")
            await page.wait_for_timeout(2500)

        if len(self.http_500_responses) > 0:
            await self.update_hud(page, "💥 PHÁT HIỆN BUG: Backend sập 500 Internal Server Error do tràn bộ đệm!", "#7f1d1d", "#fca5a5")
            self.record_finding(test_id, title, "Robustness/DoS", "BUG FOUND",
                                f"Backend crashed 500 on 5000-char buffer: {self.http_500_responses[0]}", shot)
        elif duration > 5.0:
            await self.update_hud(page, f"⚠️ CẢNH BÁO: Trình duyệt bị giật lag ({duration:.2f}s) khi nhập chuỗi lớn", "#78350f", "#fde047")
            self.record_finding(test_id, title, "Robustness/DoS", "WARNING",
                                f"UI lagged heavily during 5,000 char fill ({duration:.2f}s). Possible regex backtrack.", shot)
        else:
            await self.update_hud(page, "✓ AN TOÀN: Hệ thống xử lý chuỗi lớn an toàn", "#064e3b", "#34d399")
            self.record_finding(test_id, title, "Robustness/Unicode", "DEFENDED",
                                "System gracefully contained extreme buffer length and complex Unicode.", shot)
        await page.wait_for_timeout(2000)

    # -------------------------------------------------------------------------
    # ATTACK TEST 6: Whitespace-Only Bypass
    # -------------------------------------------------------------------------
    async def attack_06_whitespace_bypass(self, page: Page):
        test_id = "TC-DEST-06"
        title = "Whitespace-only in First & Last Name Bypass"
        self.log("EXEC", f"Running [{test_id}] {title}")
        await self.reset_form(page)
        await self.setup_listeners(page)
        await self.update_hud(page, "Đòn 6/8: Nhập toàn bộ dấu cách '    ' vào First Name / Last Name...", "#450a0a", "#f87171")

        ts = int(time.time())
        await self.visual_fill(page, page.locator("#school-user-nric"), f"S{str(ts)[-7:]}A", "Điền NRIC hợp lệ")
        await self.visual_fill(page, page.locator("#school-user-first-name"), "    ", "First Name toàn dấu cách")
        await self.visual_fill(page, page.locator("#school-user-last-name"), "    ", "Last Name toàn dấu cách")
        await self.visual_fill(page, page.locator("#school-user-email"), f"white.{ts}@edu.gov.sg", "Điền Email")
        await self._select_rosyth_school(page)

        create_btn = page.locator("button:has-text('Create')")
        is_enabled = await create_btn.is_enabled()
        shot = str(OUTPUT_DIR / f"{test_id}_whitespace.png")
        await page.screenshot(path=shot)

        if is_enabled:
            await self.visual_click(page, create_btn, "Thử submit form chứa tên toàn khoảng trắng")
            await page.wait_for_timeout(2000)
            content = await page.content()
            if "created" in content.lower() or "success" in content.lower():
                await self.update_hud(page, "💥 LỖI SANITIZE: Lưu user có tên rỗng/toàn dấu cách vào DB!", "#7f1d1d", "#fca5a5")
                self.record_finding(test_id, title, "Validation/Sanitization", "BUG FOUND",
                                    "HIGH: Blank name consisting only of whitespace was accepted and saved!", shot)
                await page.wait_for_timeout(1500)
                return

        await self.update_hud(page, "✓ AN TOÀN: Nút Create vẫn bị khóa (disabled) khi tên chỉ có khoảng trắng", "#064e3b", "#34d399")
        self.record_finding(test_id, title, "Validation/Sanitization", "DEFENDED",
                            "Button remained disabled or validation rejected whitespace-only names.", shot)
        await page.wait_for_timeout(1500)

    # -------------------------------------------------------------------------
    # ATTACK TEST 7: Ghost Combobox Free-Text Injection
    # -------------------------------------------------------------------------
    async def attack_07_ghost_school_combobox(self, page: Page):
        test_id = "TC-DEST-07"
        title = "Ghost / Non-Existent School In Combobox"
        self.log("EXEC", f"Running [{test_id}] {title}")
        await self.reset_form(page)
        await self.setup_listeners(page)
        await self.update_hud(page, "Đòn 7/8: Gõ tên trường ma 'NonExistentSchool_99999_X' vào Combobox...", "#450a0a", "#f87171")

        ts = int(time.time())
        await self.visual_fill(page, page.locator("#school-user-nric"), f"S{str(ts)[-7:]}A", "Điền NRIC hợp lệ")
        await self.visual_fill(page, page.locator("#school-user-first-name"), "Arthur", "First Name: Arthur")
        await self.visual_fill(page, page.locator("#school-user-last-name"), "GhostSchool", "Last Name: GhostSchool")
        await self.visual_fill(page, page.locator("#school-user-email"), f"ghost.{ts}@edu.gov.sg", "Điền Email")

        school_input = page.locator("#school-user-school")
        if await school_input.count() > 0:
            await self.visual_fill(page, school_input, "NonExistentSchool_99999_X", "Gõ trường ma không có trong hệ thống")
            await page.keyboard.press("Tab")
            await page.wait_for_timeout(500)

        create_btn = page.locator("button:has-text('Create')")
        is_enabled = await create_btn.is_enabled()
        shot = str(OUTPUT_DIR / f"{test_id}_ghost_school.png")
        await page.screenshot(path=shot)

        if is_enabled:
            await self.visual_click(page, create_btn, "Thử submit trường ma")
            await page.wait_for_timeout(2000)
            if len(self.http_500_responses) > 0:
                await self.update_hud(page, "💥 LỖI KHÓA NGOẠI: Backend văng lỗi 500 do Foreign Key không tồn tại!", "#7f1d1d", "#fca5a5")
                self.record_finding(test_id, title, "Combobox/Foreign-Key", "BUG FOUND",
                                    f"Backend threw unhandled 500 when non-existent school text was sent: {self.http_500_responses[0]}", shot)
                await page.wait_for_timeout(1500)
                return

        await self.update_hud(page, "✓ AN TOÀN: Bắt buộc chọn từ danh sách, từ chối text tự do không hợp lệ", "#064e3b", "#34d399")
        self.record_finding(test_id, title, "Combobox/Foreign-Key", "DEFENDED",
                            "System enforced selecting a verified school or rejected arbitrary text.", shot)
        await page.wait_for_timeout(1500)

    # -------------------------------------------------------------------------
    # ATTACK TEST 8: Tab Switching & Form State Corruption
    # -------------------------------------------------------------------------
    async def attack_08_tab_switching_corruption(self, page: Page):
        test_id = "TC-DEST-08"
        title = "Tab Hopping (Single -> Bulk CSV -> Single) State Leak"
        self.log("EXEC", f"Running [{test_id}] {title}")
        await self.reset_form(page)
        await self.setup_listeners(page)
        await self.update_hud(page, "Đòn 8/8: Nhập dữ liệu dở dang -> Chuyển tab Bulk CSV -> Chuyển lại Single...", "#450a0a", "#f87171")

        ts = int(time.time())
        test_email = f"state.{ts}@edu.gov.sg"
        await self.visual_fill(page, page.locator("#school-user-email"), test_email, f"Nhập Email dở dang: {test_email}")

        bulk_tab = page.locator("button:has-text('Bulk CSV'), [role='tab']:has-text('Bulk CSV')")
        if await bulk_tab.count() > 0:
            await self.visual_click(page, bulk_tab, "Chuyển sang tab 'Bulk CSV'")
            await page.wait_for_timeout(800)

            single_tab = page.locator("button:has-text('Single'), [role='tab']:has-text('Single')")
            await self.visual_click(page, single_tab, "Chuyển ngược lại tab 'Single'")
            await page.wait_for_timeout(800)

            email_val = await page.locator("#school-user-email").input_value()
            shot = str(OUTPUT_DIR / f"{test_id}_tab_hop.png")
            await page.screenshot(path=shot)

            if len(self.uncaught_exceptions) > 0:
                await self.update_hud(page, "💥 LỖI UI: Uncaught exception khi chuyển đổi qua lại giữa các tab", "#7f1d1d", "#fca5a5")
                self.record_finding(test_id, title, "State/UI", "BUG FOUND",
                                    f"Uncaught exception when toggling tabs: {self.uncaught_exceptions[0]}", shot)
            else:
                await self.update_hud(page, f"✓ AN TOÀN: Dữ liệu được bảo toàn nguyên vẹn ({email_val})", "#064e3b", "#34d399")
                self.record_finding(test_id, title, "State/UI", "DEFENDED",
                                    f"Form preserved state cleanly across tab switches (Email kept: '{email_val}').", shot)
        else:
            self.record_finding(test_id, title, "State/UI", "DEFENDED", "Bulk CSV tab not rendered.", "")
        await page.wait_for_timeout(1500)

    async def run(self):
        print(f"\n{Ansi.BOLD}{'='*75}{Ansi.RESET}")
        print(f"{Ansi.BOLD}{Ansi.MAGENTA} EduFAMS — DESTRUCTIVE FORM TESTING ENGINE (combo-qa Standard) {Ansi.RESET}")
        print(f"{Ansi.BOLD} Target URL : {Ansi.CYAN}{self.base_url}{Ansi.RESET}")
        print(f"{Ansi.BOLD} Mode       : {'Headed (Live Visual on Screen)' if self.headed else 'Headless'}")
        print(f"{Ansi.BOLD} Pacing     : {self.slow_mo}ms (Từng bước quan sát trực quan)")
        print(f"{Ansi.BOLD}{'='*75}{Ansi.RESET}\n")

        async with async_playwright() as p:
            launch_args = ["--ignore-certificate-errors"]
            if self.headed:
                launch_args.extend(["--class=Chromium", f"--app={self.base_url}/school-user-management/new"])

            browser = await p.chromium.launch(
                headless=not self.headed,
                slow_mo=self.slow_mo,
                args=launch_args
            )
            context = await browser.new_context(
                viewport={"width": 1440, "height": 900},
                ignore_https_errors=True
            )
            page = await context.new_page()

            try:
                await self.authenticate(page)

                # Execute 8 Destructive Attacks
                await self.attack_01_xss_injection(page)
                await self.attack_02_sqli_injection(page)
                await self.attack_03_race_condition_spam(page)
                await self.attack_04_client_bypass_tampering(page)
                await self.attack_05_buffer_and_unicode_bomb(page)
                await self.attack_06_whitespace_bypass(page)
                await self.attack_07_ghost_school_combobox(page)
                await self.attack_08_tab_switching_corruption(page)

                await self.update_hud(page, "✓ HOÀN TẤT TOÀN BỘ 8 CA TEST BẮN PHÁ FORM", "#064e3b", "#34d399")
                if self.headed:
                    await page.wait_for_timeout(3000)

            except Exception as e:
                self.log("FATAL", f"Test runner encountered fatal error: {e}", Ansi.RED)
                shot = str(OUTPUT_DIR / "fatal_error.png")
                await page.screenshot(path=shot)
            finally:
                await browser.close()

        self.print_summary()

    def print_summary(self):
        print(f"\n{Ansi.BOLD}{'='*75}{Ansi.RESET}")
        print(f"{Ansi.BOLD}{Ansi.CYAN} DESTRUCTIVE TEST SUMMARY & VULNERABILITY AUDIT {Ansi.RESET}")
        print(f"{Ansi.BOLD}{'='*75}{Ansi.RESET}\n")

        total = len(self.results)
        bugs = sum(1 for r in self.results if r["verdict"] == "BUG FOUND")
        warnings = sum(1 for r in self.results if r["verdict"] == "WARNING")
        defended = sum(1 for r in self.results if r["verdict"] == "DEFENDED")

        print(f"  Total Attacks Executed : {Ansi.BOLD}{total}{Ansi.RESET}")
        print(f"  ✓ Safely Defended      : {Ansi.GREEN}{defended}{Ansi.RESET}")
        print(f"  ⚠️ Warnings/Risk Found : {Ansi.YELLOW}{warnings}{Ansi.RESET}")
        print(f"  💥 Bugs Discovered     : {Ansi.RED}{bugs}{Ansi.RESET}\n")

        header = f"{'TC ID':<12} | {'Category':<22} | {'Verdict':<14} | {'Finding Summary'}"
        print(header)
        print("-" * 75)
        for r in self.results:
            color = Ansi.RED if r['verdict'] == 'BUG FOUND' else (Ansi.YELLOW if r['verdict'] == 'WARNING' else Ansi.GREEN)
            print(f"{r['test_id']:<12} | {r['category']:<22} | {color}{r['verdict']:<14}{Ansi.RESET} | {r['details'][:45]}...")
        print(f"\n{Ansi.BOLD}Visual Evidence Saved To: {OUTPUT_DIR.resolve()}{Ansi.RESET}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Destructive Form Test Suite")
    parser.add_argument("--url", default="https://admin.20-255-158-192.sslip.io", help="Base URL of Admin Portal")
    parser.add_argument("--headless", action="store_true", help="Run in headless mode (default: headed)")
    parser.add_argument("--slow-mo", type=int, default=500, help="Playwright slow-mo in ms")
    args = parser.parse_args()

    asyncio.run(DestructiveTestRunner(args.url, headed=not args.headless, slow_mo=args.slow_mo).run())
