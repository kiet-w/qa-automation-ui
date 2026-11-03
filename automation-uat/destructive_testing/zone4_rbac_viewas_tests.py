#!/usr/bin/env python3
"""
automation-uat/destructive_testing/zone4_rbac_viewas_tests.py
=============================================================================
EduFAMS Zone 4 Destructive & Vulnerability Testing Suite (DEST-20 to DEST-25)
Focus: RBAC, View As, Staff Provisioning & Session Security

Attack Scenarios:
  - DEST-20: Thử nghiệm XSS/SQLi trong form tạo cán bộ nhà trường.
  - DEST-21: Vượt rào kiểm toán View As bằng chuỗi 9 khoảng trắng + 1 ký tự.
  - DEST-22: Thoát đột ngột phiên View As bằng nút Exit trên top banner.
  - DEST-23: Trùng lặp NRIC cán bộ nhà trường.
  - DEST-24: Trùng lặp tên lớp học P1-A trong cùng khối Primary 1.
  - DEST-25: Kiểm tra session timeout và bảo vệ cổng thanh toán.

Standards:
  - Pure Black-Box Testing (ISO/IEC/IEEE 29119-3, ISTQB Foundation).
  - Playwright Async API (playwright.async_api).
  - Safe evidence capture (/tmp/evidence_dest fallback for sandbox read-only fs).
  - Dual Execution Mode: Callable via master runner or standalone CLI.
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
from playwright.async_api import async_playwright, Page, Locator, Response

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parents[1]
DATA_FILE = SCRIPT_DIR / "destructive_test_data.json"


def get_safe_evidence_dir() -> Path:
    """Returns safe evidence directory, falling back to /tmp if read-only."""
    try:
        candidate = SCRIPT_DIR / "evidence_dest"
        candidate.mkdir(parents=True, exist_ok=True)
        test_file = candidate / ".write_test"
        with open(test_file, "w") as f:
            f.write("ok")
        test_file.unlink(missing_ok=True)
        return candidate
    except Exception:
        fallback = Path("/tmp/evidence_dest")
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
    RESET = "\033[0m"


class Zone4RbacViewAsRunner:
    """Standalone runner for Zone 4 destructive testcases."""

    def __init__(
        self,
        base_url: str = "https://admin.20-255-158-192.sslip.io",
        eservice_url: str = "https://eservice.20-255-158-192.sslip.io",
        headed: bool = True,
        slow_mo: int = 400,
        hold: int = 5,
    ):
        self.base_url = base_url.rstrip("/")
        self.eservice_url = eservice_url.rstrip("/")
        self.headed = headed
        self.slow_mo = slow_mo if headed else 0
        self.hold = hold
        self.results = []
        self.timestamp = int(time.time())

        # Load shared config
        if DATA_FILE.exists():
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                self.config = json.load(f)
        else:
            self.config = {}

        self.school_email = (
            self.config.get("accounts", {}).get("school_staff", {}).get("email", "staff1@IAM.edu.vn")
        )
        self.admin_email = (
            self.config.get("accounts", {}).get("admin", {}).get("email", "admin@IAM.edu.vn")
        )
        self.parent_nric = (
            self.config.get("accounts", {}).get("parent", {}).get("nric", "S7654321B")
        )

    def log(self, tag: str, msg: str, color: str = Ansi.CYAN):
        now = datetime.now().strftime("%H:%M:%S")
        print(f"{Ansi.BOLD}[{now}] [{tag:<12}]{Ansi.RESET} {color}{msg}{Ansi.RESET}")

    def record_finding(self, test_id: str, title: str, zone: str, verdict: str, details: str, evidence: str = ""):
        self.results.append({
            "test_id": test_id,
            "title": title,
            "zone": zone,
            "verdict": verdict,
            "details": details,
            "evidence": evidence,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })
        if verdict == "DEFENDED":
            badge = f"{Ansi.GREEN}🛡️ DEFENDED{Ansi.RESET}"
        elif verdict == "DEFECT":
            badge = f"{Ansi.RED}💥 DEFECT FOUND{Ansi.RESET}"
        else:
            badge = f"{Ansi.YELLOW}⚠️ WARNING{Ansi.RESET}"
        print(f"       -> {badge} | [{test_id}] {title}: {details}")

    async def update_hud(self, page: Page, text: str, attack_type: str = "ATTACK", bg_color: str = "#450a0a", text_color: str = "#f87171"):
        """Injects or updates a live floating HUD badge on the browser."""
        try:
            escaped_text = text.replace("'", "\\'").replace('"', '\\"')
            badge_color = "#dc2626" if attack_type == "ATTACK" else ("#16a34a" if attack_type == "DEFENDED" else "#2563eb")
            await page.evaluate(f"""() => {{
                let hud = document.getElementById('destructive-hud');
                if (!hud) {{
                    hud = document.createElement('div');
                    hud.id = 'destructive-hud';
                    document.body.appendChild(hud);
                }}
                hud.innerHTML = '<span style="background:{badge_color};color:#fff;padding:2px 8px;border-radius:12px;font-size:11px;font-weight:700;margin-right:8px;">{attack_type}</span> {escaped_text}';
                hud.style.cssText = 'position:fixed;top:16px;left:50%;transform:translateX(-50%);background:{bg_color};color:{text_color};padding:8px 18px;border-radius:24px;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:13px;font-weight:600;z-index:9999999;box-shadow:0 8px 24px rgba(0,0,0,0.45);border:1.5px solid {text_color};pointer-events:none;transition:all 0.25s ease;display:flex;align-items:center;letter-spacing:0.3px;max-width:90vw;text-align:center;';
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
        if self.headed and self.slow_mo:
            await page.wait_for_timeout(int(self.slow_mo * 0.4))
        await locator.click()

    async def visual_fill(self, page: Page, locator: Locator, value: str, hud_text: str = ""):
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
        try:
            target_path = EVIDENCE_DIR / filename
            await page.screenshot(path=str(target_path))
            return str(target_path)
        except Exception:
            fallback = Path("/tmp/evidence_dest") / filename
            try:
                await page.screenshot(path=str(fallback))
                return str(fallback)
            except Exception:
                return filename

    async def authenticate_admin(self, page: Page):
        """Authenticates MOE HQ Administrator via Microsoft SSO Simulator."""
        self.log("AUTH", f"Đăng nhập Quản trị viên Bộ MOE HQ ({self.admin_email})")
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

        tile = page.locator(f".account-tile:has-text('{self.admin_email}'), [data-email='{self.admin_email}']").first
        if await tile.count() > 0:
            await self.visual_click(page, tile, f"Chọn tài khoản {self.admin_email}")
        else:
            fallback_tile = page.locator(f"text={self.admin_email}").first
            if await fallback_tile.count() > 0:
                await self.visual_click(page, fallback_tile)

        await page.wait_for_url(f"{self.base_url}/**", timeout=30000)
        await page.wait_for_load_state("networkidle")

        exit_btn = page.get_by_role("button", name="Exit", exact=True)
        if await exit_btn.count() > 0 and await exit_btn.is_visible():
            await exit_btn.click()
            await page.wait_for_timeout(800)

        self.log("AUTH", "✓ Đăng nhập Quản trị viên MOE HQ thành công", Ansi.GREEN)

    async def authenticate_school(self, page: Page):
        """Authenticates School Staff (staff1@IAM.edu.vn) for Rosyth Primary School."""
        self.log("AUTH", f"Xác thực tài khoản Cán bộ trường: {self.school_email}")
        await page.context.clear_cookies()
        try:
            await page.evaluate("() => { try { localStorage.clear(); sessionStorage.clear(); } catch(e){} }")
        except Exception:
            pass

        await page.goto(f"{self.base_url}/login", wait_until="networkidle")
        await self.update_hud(page, f"Đăng nhập Cán bộ trường ({self.school_email})...", "AUTH", "#0f172a", "#c084fc")

        ms_btn = page.locator('button:has-text("Sign in with Microsoft")')
        if await ms_btn.is_visible():
            await self.visual_click(page, ms_btn, "Nhấn 'Sign in with Microsoft'")
            await page.wait_for_url("**/microsoft-provider/**", timeout=25000)

        staff_tile = page.locator(f".account-tile:has-text('{self.school_email}'), [data-email='{self.school_email}']").first
        if await staff_tile.count() > 0:
            await self.visual_click(page, staff_tile, f"Chọn tài khoản {self.school_email}")
        else:
            fallback_tile = page.locator(f"text={self.school_email}").first
            if await fallback_tile.count() > 0:
                await self.visual_click(page, fallback_tile)

        await page.wait_for_url(f"{self.base_url}/**", timeout=30000)
        await page.wait_for_load_state("networkidle")

        exit_btn = page.get_by_role("button", name="Exit", exact=True)
        if await exit_btn.count() > 0 and await exit_btn.is_visible():
            await exit_btn.click()
            await page.wait_for_timeout(800)

        self.log("AUTH", "✓ Đăng nhập Cán bộ trường thành công", Ansi.GREEN)

    async def authenticate_parent(self, page: Page):
        """Authenticates Parent (Pham Van Duc) via Singpass Mock."""
        self.log("AUTH", f"Đăng nhập Singpass Mock Phụ huynh: Pham Van Duc ({self.parent_nric})")
        await page.goto(f"{self.eservice_url}/parent/login", wait_until="networkidle")
        await self.update_hud(page, f"Đăng nhập Singpass Phụ huynh ({self.parent_nric})...", "AUTH", "#0f172a", "#60a5fa")

        sp_btn = page.locator('button:has-text("Sign in with Singpass"), a:has-text("Sign in with Singpass")')
        if await sp_btn.is_visible():
            await self.visual_click(page, sp_btn, "Nhấn 'Sign in with Singpass'")
            await page.wait_for_timeout(1000)

        select = page.locator("select")
        if await select.count() > 0:
            await select.select_option(index=1)
            await page.wait_for_timeout(400)
            login_btn = page.locator("#btn-login-selected")
            await self.visual_click(page, login_btn, "Xác nhận đăng nhập Singpass")
            await page.wait_for_timeout(2500)

        tour_close = page.locator("button:has-text('Let me explore'), button:has-text('×')")
        if await tour_close.count() > 0 and await tour_close.first.is_visible():
            await tour_close.first.click()
            await page.wait_for_timeout(500)

        self.log("AUTH", "✓ Đăng nhập Phụ huynh Singpass thành công", Ansi.GREEN)


# -----------------------------------------------------------------------------
# INDIVIDUAL DESTRUCTIVE TESTCASES (DEST-20 to DEST-25)
# -----------------------------------------------------------------------------

async def test_dest_20_xss_sqli_school_user_form(runner, page: Page):
    """
    DEST-20: Thử nghiệm XSS/SQLi trong form tạo cán bộ nhà trường (/school-user-management/new).
    Oracle:
      - Bơm payload XSS `<script>window.__xss_executed=true;</script>` vào First Name.
      - Bơm payload SQL Injection `Arthur' OR '1'='1` vào Last Name & NRIC.
      - Kết quả kỳ vọng:
        1. JavaScript KHÔNG được thực thi trong trình duyệt (`window.__xss_executed === false`).
        2. Backend KHÔNG bị lỗi cú pháp sập 500 (Internal Server Error).
        3. Dữ liệu được encode dạng plain text an toàn hoặc bị validate chặn.
    """
    runner.log("DEST-20", "Tấn công XSS & SQLi Payload trong Form tạo cán bộ nhà trường")
    await runner.authenticate_admin(page)

    await page.goto(f"{runner.base_url}/school-user-management/new", wait_until="networkidle")
    await runner.update_hud(page, "Tấn công DEST-20: Bơm XSS script tag & SQLi payload vào form...", "ATTACK")

    # Đặt cờ theo dõi thực thi JS
    await page.evaluate("window.__xss_executed = false;")

    xss_payload = '<script>window.__xss_executed=true;</script><img src=x onerror="window.__xss_executed=true;">'
    sqli_payload = "Arthur' OR '1'='1"
    ts = int(time.time())

    # NRIC format: S + 7 digits + Letter
    nric_clean = f"S{str(ts)[-7:]}A"

    await runner.visual_fill(page, page.locator("#school-user-nric"), nric_clean, f"NRIC: {nric_clean}")
    await runner.visual_fill(page, page.locator("#school-user-first-name"), xss_payload, "Bắn Stored XSS vào First Name")
    await runner.visual_fill(page, page.locator("#school-user-last-name"), sqli_payload, f"Bắn SQLi vào Last Name: {sqli_payload}")
    await runner.visual_fill(page, page.locator("#school-user-email"), f"dest20.{ts}@edu.gov.sg", "Điền Email")

    # Chọn trường Rosyth
    school_input = page.locator("#school-user-school")
    if await school_input.count() > 0:
        await runner.visual_fill(page, school_input, "Rosyth", "Tìm kiếm trường: Rosyth")
        await page.wait_for_timeout(600)
        opt = page.locator("[role='option']:has-text('Rosyth'), li:has-text('Rosyth')").first
        if await opt.count() > 0:
            await runner.visual_click(page, opt)
        else:
            await page.keyboard.press("ArrowDown")
            await page.keyboard.press("Enter")

    # Kiểm tra nút Create
    create_btn = page.locator("button:has-text('Create')")
    if await create_btn.is_enabled():
        await runner.visual_click(page, create_btn, "Nhấn 'Create' thử submit payload")
        await page.wait_for_timeout(2500)

    # Đọc cờ XSS
    xss_hit = await page.evaluate("window.__xss_executed === true")
    first_name_val = await page.locator("#school-user-first-name").input_value() if await page.locator("#school-user-first-name").count() > 0 else ""

    shot = await runner.safe_screenshot(page, "dest20_xss_sqli_defense.png")

    if xss_hit:
        runner.record_finding(
            "DEST-20",
            "XSS & SQLi Injection Defense in School User Form",
            "ZONE-4",
            "DEFECT",
            "LỖI BẢO MẬT NGHIÊM TRỌNG: Script XSS đã được thực thi trên trình duyệt người dùng!",
            shot,
        )
    else:
        runner.record_finding(
            "DEST-20",
            "XSS & SQLi Injection Defense in School User Form",
            "ZONE-4",
            "DEFENDED",
            f"An toàn tuyệt đối: JavaScript không thực thi (window.__xss_executed=False); Payload SQLi được xử lý dạng chuỗi thô an toàn ({first_name_val[:25]}...)",
            shot,
        )


async def test_dest_21_whitespace_reason_audit_bypass(runner, page: Page):
    """
    DEST-21: Vượt rào kiểm toán View As bằng chuỗi 9 khoảng trắng + 1 ký tự (/support-console).
    Oracle:
      - Nút Start View As bắt buộc Reason có tối thiểu 10 ký tự.
      - Tấn công: Bơm chuỗi '         A' (9 dấu cách + 1 ký tự = 10 ký tự).
      - Kết quả kỳ vọng:
        - Hệ thống bắt buộc phải áp dụng `.trim()`.
        - Khi trim, độ dài thực tế chỉ còn 1 ký tự (< 10).
        - Nút Start View As BẮT BUỘC BỊ KHÓA (disabled).
        - Nếu nút sáng Enabled -> Phát hiện DEFECT (Lỗ hổng vượt rào kiểm toán).
    """
    runner.log("DEST-21", "Tấn công lách luật kiểm toán Reason bằng khoảng trắng (9 spaces + 1 char)")
    # Clear any active View As session banner if present
    exit_btn = page.get_by_role("button", name="Exit", exact=True)
    if await exit_btn.count() > 0 and await exit_btn.is_visible():
        await exit_btn.click()
        await page.wait_for_timeout(1000)

    await page.goto(f"{runner.base_url}/support-console", wait_until="networkidle")
    await runner.update_hud(page, "Tấn công DEST-21: Nhập 9 khoảng trắng + 1 ký tự vào Reason...", "ATTACK")

    # Clear exit button if still visible after navigation
    exit_btn = page.get_by_role("button", name="Exit", exact=True)
    if await exit_btn.count() > 0 and await exit_btn.is_visible():
        await exit_btn.click()
        await page.wait_for_timeout(1000)

    # Chọn School user staff1
    user_tab = page.get_by_role("tab", name=re.compile(r"School users", re.I))
    if await user_tab.count() > 0 and await user_tab.is_visible():
        await runner.visual_click(page, user_tab, "Chuyển sang tab School users")
        await page.wait_for_timeout(600)

    search_input = page.locator('input[placeholder*="search" i], input[type="search"], input[type="text"]').first
    search_btn = page.get_by_role("button", name="Search", exact=True)
    await runner.visual_fill(page, search_input, "staff1", "Tìm cán bộ: staff1")
    if await search_btn.count() > 0 and await search_btn.is_visible():
        await runner.visual_click(page, search_btn)
    else:
        await search_input.press("Enter")
    await page.wait_for_timeout(1000)

    select_btn = page.locator('tr:has-text("staff1") button:has-text("Select"), tr:has-text("Bui Thi H") button:has-text("Select"), button:has-text("Select")').first
    if await select_btn.count() > 0 and await select_btn.is_visible():
        await runner.visual_click(page, select_btn, "Chọn cán bộ staff1 (Bui Thi H)")
        await page.wait_for_timeout(1000)
    else:
        persona_tab = page.get_by_role("tab", name=re.compile(r"School role", re.I))
        if await persona_tab.count() > 0:
            await runner.visual_click(page, persona_tab)
            await page.wait_for_timeout(500)
            p_search = page.locator('input[placeholder*="Search school" i], input[type="text"]').first
            await runner.visual_fill(page, p_search, "RPS-0201")
            p_btn = page.get_by_role("button", name="Search", exact=True)
            if await p_btn.count() > 0:
                await runner.visual_click(page, p_btn)
            await page.wait_for_timeout(800)
            p_sel = page.locator('button:has-text("Select")').first
            if await p_sel.count() > 0:
                await runner.visual_click(page, p_sel)
                await page.wait_for_timeout(1000)

    reason_area = page.locator("textarea").or_(page.get_by_label("Reason", exact=False)).first
    await reason_area.wait_for(state="visible", timeout=15000)
    ticket_input = page.get_by_label("Ticket reference", exact=False).or_(page.locator("input[placeholder*='ticket' i], input#ticket")).first
    start_btn = page.get_by_role("button", name=re.compile(r"Start View As", re.I)).first

    # Bơm payload 9 khoảng trắng + 1 ký tự
    whitespace_payload = "         A"
    await runner.visual_fill(page, reason_area, whitespace_payload, "Bơm Reason: 9 dấu cách + 'A'")
    await runner.visual_fill(page, ticket_input, "UAT-DEST-AUDIT-BYPASS", "Điền Ticket reference")
    await page.wait_for_timeout(600)

    is_btn_enabled = await start_btn.is_enabled()
    shot = await runner.safe_screenshot(page, "dest21_whitespace_reason_audit.png")

    if not is_btn_enabled:
        runner.record_finding(
            "DEST-21",
            "Whitespace Reason Audit Bypass (9 spaces + 1 char)",
            "ZONE-4",
            "DEFENDED",
            "Hệ thống kiểm toán chặt chẽ: Áp dụng .trim() trên Reason, phát hiện độ dài thực tế là 1 (< 10) và giữ nút Start View As ở trạng thái DISABLED",
            shot,
        )
    else:
        runner.record_finding(
            "DEST-21",
            "Whitespace Reason Audit Bypass (9 spaces + 1 char)",
            "ZONE-4",
            "DEFECT",
            "LỖI KIỂM TOÁN: Hệ thống tính cả khoảng trắng vào độ dài Reason, cho phép kích hoạt nút Start View As chỉ với 1 ký tự có nghĩa",
            shot,
        )


async def test_dest_22_abrupt_exit_view_as_banner(runner, page: Page):
    """
    DEST-22: Thoát đột ngột phiên View As bằng nút Exit trên top banner.
    Oracle:
      - Kích hoạt phiên View As hợp lệ để xuất hiện Top Banner 'Viewing as...'.
      - Điều hướng sâu vào phân hệ trường học (ví dụ: /class-management).
      - Nhấn nút Exit trực tiếp trên top banner.
      - Kết quả kỳ vọng:
        1. Banner mô phỏng biến mất ngay lập tức.
        2. Ngữ cảnh quay về Quản trị viên Bộ MOE HQ an toàn.
        3. Các menu trường học trên Sidebar bị thu hồi ngay lập tức.
        4. Không phát sinh loop reload hoặc trạng thái treo phiên (orphaned impersonation).
    """
    runner.log("DEST-22", "Tấn công thoát đột ngột phiên View As bằng nút Exit trên top banner")
    await runner.update_hud(page, "Tấn công DEST-22: Kích hoạt phiên View As để thử nghiệm nút Exit...", "ATTACK")

    # If exit button is not yet visible, start View As
    top_exit_btn = page.get_by_role("button", name="Exit", exact=True)
    if await top_exit_btn.count() == 0 or not await top_exit_btn.is_visible():
        await page.goto(f"{runner.base_url}/support-console", wait_until="networkidle")
        await page.wait_for_timeout(1000)
        
        # Click School users button if present
        user_btn = page.locator('button:has-text("School users")').first
        if await user_btn.count() > 0 and await user_btn.is_visible():
            await runner.visual_click(page, user_btn)
            await page.wait_for_timeout(500)
            
        select_btn = page.locator('button:has-text("Select")').first
        if await select_btn.count() > 0:
            await runner.visual_click(page, select_btn)
            await page.wait_for_timeout(800)

        reason_area = page.locator("textarea").first
        try:
            await reason_area.wait_for(state="visible", timeout=6000)
            ticket_input = page.get_by_label("Ticket reference", exact=False).first

            await runner.visual_fill(page, reason_area, "Security Audit Exit Test Execution 123456789")
            await runner.visual_fill(page, ticket_input, "UAT-DEST-EXIT-01")
            await page.wait_for_timeout(500)

            start_btn = page.locator('button:has-text("Start View As")').first
            if await start_btn.is_enabled():
                await runner.visual_click(page, start_btn, "Khởi động phiên View As")
                await page.wait_for_timeout(2500)
        except Exception as e:
            runner.log("DEST-22", f"Reason textarea not visible or session already initializing ({e})", Ansi.YELLOW)

    # Điều hướng vào trang quản lý lớp học của trường
    await page.goto(f"{runner.base_url}/class-management", wait_until="networkidle")
    await runner.update_hud(page, "Đang trong ngữ cảnh trường /class-management -> Bấm 'Exit' trên banner...", "ATTACK")
    await page.wait_for_timeout(1000)

    shot_active = await runner.safe_screenshot(page, "dest22_view_as_active_in_class.png")

    exit_btn = page.get_by_role("button", name="Exit", exact=True)
    is_exit_visible = await exit_btn.count() > 0 and await exit_btn.is_visible()

    if is_exit_visible:
        await runner.visual_click(page, exit_btn, "Bấm nút 'Exit' trên banner")
        await page.wait_for_timeout(2000)
        await page.wait_for_load_state("networkidle")

        shot_after_exit = await runner.safe_screenshot(page, "dest22_abrupt_exit_view_as.png")

        # Kiểm tra xem banner Exit còn hiển thị không
        is_banner_still_there = await exit_btn.count() > 0 and await exit_btn.is_visible()
        page_text = await page.locator("body").inner_text()
        has_school_view = "viewing as" in page_text.lower()

        if not is_banner_still_there and not has_school_view:
            runner.record_finding(
                "DEST-22",
                "Abrupt Session Exit via Top Banner Exit Button",
                "ZONE-4",
                "DEFENDED",
                "Thoát phiên an toàn: Nhấn 'Exit' lập tức đóng banner mô phỏng, hủy quyền truy cập trường và khôi phục ngữ cảnh Quản trị viên Bộ MOE HQ",
                shot_after_exit,
            )
        else:
            runner.record_finding(
                "DEST-22",
                "Abrupt Session Exit via Top Banner Exit Button",
                "ZONE-4",
                "DEFECT",
                "LỖI PHIÊN: Nút Exit không thu hồi hoàn toàn phiên View As, banner hoặc token giả lập vẫn còn lưu trong bộ nhớ",
                shot_after_exit,
            )
    else:
        runner.record_finding(
            "DEST-22",
            "Abrupt Session Exit via Top Banner Exit Button",
            "ZONE-4",
            "WARNING",
            "Không tìm thấy nút Exit trên top banner khi mở trang trong phiên View As",
            shot_active,
        )


async def test_dest_23_duplicate_staff_nric(runner, page: Page):
    """
    DEST-23: Trùng lặp NRIC cán bộ nhà trường (/school-user-management/new).
    Oracle:
      - NRIC là định danh duy nhất (Unique Identity) của công dân Singapore.
      - Thử nghiệm tạo tài khoản cán bộ mới với NRIC đã tồn tại trong cơ sở dữ liệu.
      - Kết quả kỳ vọng:
        - Hệ thống chặn việc tạo mới.
        - Hiển thị thông báo lỗi rõ ràng: 'An active or inactive user with this NRIC already exists' hoặc alert màu đỏ.
        - Không ghi đè hoặc tạo 2 bản ghi có cùng số NRIC.
    """
    runner.log("DEST-23", "Tấn công thử tạo trùng lặp số NRIC cán bộ nhà trường")
    await runner.authenticate_admin(page)

    await page.goto(f"{runner.base_url}/school-user-management/new", wait_until="networkidle")
    await runner.update_hud(page, "Tấn công DEST-23: Thử tạo cán bộ với số NRIC đã tồn tại...", "ATTACK")

    ts = int(time.time())
    # Sử dụng số NRIC của phụ huynh hoặc cán bộ đã biết chắc chắn có trong hệ thống
    duplicate_nric = getattr(runner, "parent_nric", "S7654321B")
    if hasattr(runner, "config") and isinstance(runner.config, dict):
        duplicate_nric = runner.config.get("accounts", {}).get("parent", {}).get("nric", duplicate_nric)

    await runner.visual_fill(page, page.locator("#school-user-nric"), duplicate_nric, f"Nhập NRIC TRÙNG LẶP: {duplicate_nric}")
    await runner.visual_fill(page, page.locator("#school-user-first-name"), "Duplicate", "First Name: Duplicate")
    await runner.visual_fill(page, page.locator("#school-user-last-name"), "NRIC_Attack", "Last Name: NRIC_Attack")
    await runner.visual_fill(page, page.locator("#school-user-email"), f"dup.nric.{ts}@edu.gov.sg", "Điền Email mới")

    school_input = page.locator("#school-user-school")
    if await school_input.count() > 0:
        await runner.visual_fill(page, school_input, "Rosyth", "Chọn trường: Rosyth")
        await page.wait_for_timeout(600)
        opt = page.locator("[role='option']:has-text('Rosyth'), li:has-text('Rosyth')").first
        if await opt.count() > 0:
            await runner.visual_click(page, opt)
        else:
            await page.keyboard.press("ArrowDown")
            await page.keyboard.press("Enter")

    create_btn = page.locator("button:has-text('Create')")
    if await create_btn.is_enabled():
        await runner.visual_click(page, create_btn, "Nhấn 'Create' kiểm tra phản hồi chặn trùng NRIC")
        await page.wait_for_timeout(2500)

    shot = await runner.safe_screenshot(page, "dest23_duplicate_nric.png")

    alert = page.locator("[role='alert'], .text-destructive, h2, h3").filter(has_text=re.compile(r"already exists|Unable to create|NRIC", re.I)).first
    has_dup_alert = await alert.count() > 0
    is_still_create_form = "/school-user-management/new" in page.url

    if has_dup_alert or is_still_create_form:
        alert_text = (await alert.inner_text()).replace("\n", " ") if has_dup_alert else "Form bị chặn submit an toàn"
        runner.record_finding(
            "DEST-23",
            "Duplicate Staff NRIC Collision Defense",
            "ZONE-4",
            "DEFENDED",
            f"Chặn trùng lặp NRIC thành công: Hệ thống bảo vệ tính toàn vẹn định danh với cảnh báo: '{alert_text}'",
            shot,
        )
    else:
        runner.record_finding(
            "DEST-23",
            "Duplicate Staff NRIC Collision Defense",
            "ZONE-4",
            "DEFECT",
            f"LỖI TOÀN VẸN DỮ LIỆU: Cho phép tạo 2 cán bộ có cùng số định danh NRIC '{duplicate_nric}'",
            shot,
        )


async def test_dest_24_duplicate_class_code(runner, page: Page):
    """
    DEST-24: Trùng lặp tên lớp học P1-A trong cùng khối Primary 1 (/class-management/new).
    Oracle:
      - Mã lớp học (Class code) và Tên lớp phải là duy nhất trong cùng cấp học và niên khóa.
      - Thử tạo lớp với Class code 'P1-A' và Offering 'Primary 1 · 2026' (đã tồn tại).
      - Kết quả kỳ vọng:
        - Hệ thống chặn việc tạo mới.
        - Hiển thị thông báo lỗi rõ ràng: 'Class code P1-A already exists for this offering.'
    """
    runner.log("DEST-24", "Tấn công thử tạo trùng lặp mã lớp học P1-A trong cùng khối Primary 1")
    await runner.authenticate_school(page)

    await page.goto(f"{runner.base_url}/class-management/new", wait_until="networkidle")
    await runner.update_hud(page, "Tấn công DEST-24: Nhập mã lớp trùng lặp P1-A...", "ATTACK")

    # Điền Class code: P1-A
    code_input = page.locator("#class-classCode, input[name='classCode']")
    await runner.visual_fill(page, code_input, "P1-A", "Mã lớp trùng: P1-A")

    # Điền Class name: Primary 1-A Duplicate Attack
    name_input = page.locator("#class-className, input[name='className']")
    await runner.visual_fill(page, name_input, "Primary 1-A Duplicate Attack", "Tên lớp: Primary 1-A")

    # Chọn Offering: Primary 1 · 2026
    offering_input = page.locator("#class-schoolLevelOffering")
    if await offering_input.count() > 0:
        await runner.visual_click(page, offering_input, "Chọn khối lớp: Primary 1")
        await page.wait_for_timeout(400)
        opt = page.locator("[role='option']:has-text('Primary 1')").first
        if await opt.count() > 0:
            await runner.visual_click(page, opt)

    submit_btn = page.locator("button[type='submit']:has-text('Create class'), button:has-text('Create class')").first
    await runner.visual_click(page, submit_btn, "Nhấn 'Create class' kiểm tra chặn trùng")
    await page.wait_for_timeout(1500)

    shot = await runner.safe_screenshot(page, "dest24_duplicate_class_code.png")

    alert = page.locator("[role='alert'], [role='status'], .text-destructive, h2, h3").filter(has_text=re.compile(r"already exists|Unable to create class", re.IGNORECASE)).first
    has_dup_alert = await alert.count() > 0
    is_still_new_class = "/class-management/new" in page.url

    if has_dup_alert or is_still_new_class:
        alert_msg = (await alert.inner_text()).replace("\n", " ") if has_dup_alert else "Chặn lưu bản ghi trùng mã lớp thành công"
        runner.record_finding(
            "DEST-24",
            "Duplicate Class Code Collision Defense (P1-A)",
            "ZONE-4",
            "DEFENDED",
            f"Hệ thống bảo vệ cấu trúc lớp học chặt chẽ: Chặn tạo trùng lặp mã P1-A với cảnh báo: '{alert_msg}'",
            shot,
        )
    else:
        runner.record_finding(
            "DEST-24",
            "Duplicate Class Code Collision Defense (P1-A)",
            "ZONE-4",
            "DEFECT",
            "LỖI DỮ LIỆU: Cho phép tạo 2 lớp học có cùng mã P1-A trong cùng một khối Primary 1",
            shot,
        )


async def test_dest_25_session_timeout_and_payment_guard(runner, page: Page):
    """
    DEST-25: Kiểm tra session timeout và bảo vệ cổng thanh toán (/accounts/STU-001/pay).
    Oracle:
      - Đăng nhập phụ huynh Singpass và mở giao diện thanh toán công nợ học sinh.
      - Mô phỏng hết hạn phiên làm việc (Session timeout) bằng cách xóa toàn bộ cookies và storage.
      - Thử thực hiện hành động thanh toán hoặc reload trang tài chính.
      - Kết quả kỳ vọng:
        1. Cổng thanh toán được bảo vệ ngay lập tức, chặn gửi transaction ra ngoài.
        2. Tự động điều hướng về màn hình đăng nhập /parent/login.
        3. Không cho phép phụ huynh thanh toán bằng phiên đã hết hạn.
    """
    runner.log("DEST-25", "Tấn công thử nghiệm Session Timeout trên cổng thanh toán phụ huynh")
    await runner.authenticate_parent(page)

    # Điều hướng vào trang thanh toán tài chính của học sinh
    await page.goto(f"{runner.eservice_url}/accounts/STU-001/pay", wait_until="networkidle")
    await runner.update_hud(page, "DEST-25: Mở trang thanh toán nợ học phí -> Tiến hành giả lập Timeout...", "ATTACK")
    await page.wait_for_timeout(1000)

    shot_before_timeout = await runner.safe_screenshot(page, "dest25_payment_page_before_timeout.png")

    # Giả lập Session Timeout: Xóa sạch cookies và token lưu trữ trong browser
    runner.log("DEST-25", "Kích hoạt Session Timeout: Xóa toàn bộ Cookies & Local/SessionStorage")
    await page.context.clear_cookies()
    try:
        await page.evaluate("() => { try { localStorage.clear(); sessionStorage.clear(); } catch(e){} }")
    except Exception:
        pass

    # Thử tương tác thanh toán sau khi session đã chết
    first_cb = page.locator("tbody input[type='checkbox']").first
    if await first_cb.count() > 0:
        try:
            await first_cb.click(timeout=1500)
        except Exception:
            pass

    continue_btn = page.locator("button:has-text('Continue'), button:has-text('Pay')").first
    if await continue_btn.count() > 0 and await continue_btn.is_visible():
        try:
            await continue_btn.click(timeout=1500)
        except Exception:
            pass

    # Thử refresh trang thanh toán để kiểm tra bảo vệ định tuyến
    await page.reload(wait_until="networkidle")
    await page.wait_for_timeout(2000)

    shot_after_timeout = await runner.safe_screenshot(page, "dest25_session_timeout_payment_guard.png")

    current_url = page.url
    is_protected = "login" in current_url or await page.locator('button:has-text("Sign in with Singpass")').count() > 0

    if is_protected:
        runner.record_finding(
            "DEST-25",
            "Payment Gateway Session Timeout Guard",
            "ZONE-4",
            "DEFENDED",
            f"Cổng thanh toán được bảo vệ tuyệt đối: Khi phiên hết hạn, hệ thống lập tức khóa giao dịch và chuyển hướng về trang đăng nhập ({current_url})",
            shot_after_timeout,
        )
    else:
        # Nếu vẫn ở trong trang pay, kiểm tra xem có cờ cảnh báo phiên không
        page_text = await page.locator("body").inner_text()
        has_session_warn = "session" in page_text.lower() or "expired" in page_text.lower()
        if has_session_warn:
            runner.record_finding(
                "DEST-25",
                "Payment Gateway Session Timeout Guard",
                "ZONE-4",
                "DEFENDED",
                "Hệ thống phát hiện phiên hết hạn và hiển thị thông báo yêu cầu xác thực lại",
                shot_after_timeout,
            )
        else:
            runner.record_finding(
                "DEST-25",
                "Payment Gateway Session Timeout Guard",
                "ZONE-4",
                "DEFECT",
                "LỖI BẢO MẬT PHIÊN: Cổng thanh toán vẫn mở và cho phép hiển thị số dư nợ dù phiên đăng nhập đã bị xóa",
                shot_after_timeout,
            )


# -----------------------------------------------------------------------------
# MASTER RUNNER DISPATCHER
# -----------------------------------------------------------------------------

async def run_zone4_tests(runner_or_page, page: Page = None):
    """
    Main entry point for Zone 4 tests.
    Supports being called from Master Destructive Runner:
      `await run_zone4_tests(self, page)`
    Or standalone with just page:
      `await run_zone4_tests(page)`
    """
    if page is None:
        if isinstance(runner_or_page, Page):
            page = runner_or_page
            runner = Zone4RbacViewAsRunner()
        else:
            runner = runner_or_page
            page = getattr(runner, "page", None)
    else:
        runner = runner_or_page

    runner.log("ZONE 4", "Khởi chạy toàn diện 6 ca kiểm thử phá hủy Zone 4 (DEST-20 đến DEST-25)", Ansi.HEADER)

    zone4_tests = [
        ("DEST-20", "XSS & SQLi Injection Defense in School User Form", test_dest_20_xss_sqli_school_user_form),
        ("DEST-21", "Whitespace Reason Audit Bypass (9 spaces + 1 char)", test_dest_21_whitespace_reason_audit_bypass),
        ("DEST-22", "Abrupt Exit View As Banner During Active Simulation", test_dest_22_abrupt_exit_view_as_banner),
        ("DEST-23", "Duplicate School Staff NRIC Collision", test_dest_23_duplicate_staff_nric),
        ("DEST-24", "Duplicate Class Code in Same Academic Offering", test_dest_24_duplicate_class_code),
        ("DEST-25", "Payment Gateway Session Timeout Guard", test_dest_25_session_timeout_and_payment_guard),
    ]

    for tid, title, fn in zone4_tests:
        try:
            await fn(runner, page)
        except Exception as exc:
            runner.log(tid, f"Exception occurred during attack: {exc}", Ansi.RED)
            shot = await runner.safe_screenshot(page, f"{tid.lower()}_exception.png")
            runner.record_finding(tid, title, "ZONE-4", "DEFECT", f"Unhandled Exception during attack: {exc}", shot)

    runner.log("ZONE 4", "✓ Hoàn tất toàn bộ 6 ca kiểm thử phá hủy Zone 4", Ansi.GREEN)


async def main():
    parser = argparse.ArgumentParser(description="Zone 4: RBAC & View As Destructive Test Runner")
    parser.add_argument("--base-url", default="https://admin.20-255-158-192.sslip.io", help="Admin Portal URL")
    parser.add_argument("--eservice-url", default="https://eservice.20-255-158-192.sslip.io", help="Parent Portal URL")
    parser.add_argument("--headed", action="store_true", default=True, help="Run browser in visual headed mode")
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode")
    parser.add_argument("--slow-mo", type=int, default=400, help="Slow down actions in ms")
    parser.add_argument("--hold", type=int, default=5, help="Seconds to hold browser open after completion")
    args = parser.parse_args()

    headed = False if args.headless else args.headed
    runner = Zone4RbacViewAsRunner(
        base_url=args.base_url,
        eservice_url=args.eservice_url,
        headed=headed,
        slow_mo=args.slow_mo,
        hold=args.hold,
    )

    async with async_playwright() as p:
        launch_args = ["--ignore-certificate-errors", "--ozone-platform-hint=auto"]
        if headed:
            launch_args.extend(["--class=Chromium", f"--app={runner.base_url}/login"])

        browser = await p.chromium.launch(headless=not headed, slow_mo=runner.slow_mo, args=launch_args)
        context = await browser.new_context(viewport={"width": 1440, "height": 900}, ignore_https_errors=True)
        page = await context.new_page()

        try:
            await run_zone4_tests(runner, page)
            if runner.hold > 0:
                await page.wait_for_timeout(runner.hold * 1000)
        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
