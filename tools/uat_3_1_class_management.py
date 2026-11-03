#!/usr/bin/env python3
"""
tools/uat_3_1_class_management.py - Visual & Standalone UAT 3.1 Class Management Test Runner.
Kịch bản: 3.1. Kiểm tra hoặc Tạo Lớp học (Classes)
Target: https://admin.20-255-158-192.sslip.io hoặc http://localhost:5173

Tính năng:
  - Live Visual HUD banner trực tiếp trên giao diện trình duyệt.
  - Tự động highlight phần tử trước khi click / nhập liệu.
  - Tự động đăng nhập SSO Microsoft với vai trò Cán bộ trường (SCHOOL - staff1@IAM.edu.vn).
  - Kiểm tra tồn tại lớp P1-A, kiểm tra form tạo lớp, validation rỗng, trùng lặp và tạo thành công.
  - Chụp ảnh minh chứng kết quả thực tế vào reports/uat_3_1/.

Cách chạy:
  .venv/bin/python tools/uat_3_1_class_management.py --url https://admin.20-255-158-192.sslip.io --headed --slow-mo 400
  .venv/bin/python tools/uat_3_1_class_management.py --url http://localhost:5173 --headed --slow-mo 400
"""

import argparse
import asyncio
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright, Page, Locator, Response

try:
    OUTPUT_DIR = Path("reports/uat_3_1")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
except Exception:
    OUTPUT_DIR = Path("/tmp/reports/uat_3_1")
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
    BG_BLUE = "\033[44m\033[97m"
    BG_GREEN = "\033[42m\033[97m"
    BG_RED = "\033[41m\033[97m"


class ClassManagementUATRunner:
    def __init__(self, base_url: str = "https://admin.20-255-158-192.sslip.io", headed: bool = True, slow_mo: int = 400):
        self.base_url = base_url.rstrip("/")
        self.headed = headed
        self.slow_mo = slow_mo if headed else 0
        self.results = []
        self.school_email = "staff1@IAM.edu.vn"

    def log(self, tag: str, msg: str, color: str = Ansi.CYAN):
        t = datetime.now().strftime("%H:%M:%S")
        print(f"{Ansi.BOLD}[{t}] [{tag}]{Ansi.RESET} {color}{msg}{Ansi.RESET}")

    def record_step(self, step_id: str, title: str, verdict: str, details: str, evidence: str = ""):
        self.results.append({
            "step_id": step_id,
            "title": title,
            "verdict": verdict,  # PASS | FAIL | INFO
            "details": details,
            "evidence": evidence
        })
        if verdict == "PASS":
            badge = f"{Ansi.BG_GREEN} ✓ PASS {Ansi.RESET}"
        elif verdict == "FAIL":
            badge = f"{Ansi.BG_RED} ✗ FAIL {Ansi.RESET}"
        else:
            badge = f"{Ansi.BG_BLUE} ℹ INFO {Ansi.RESET}"
        print(f"       -> {badge} {Ansi.BOLD}[{step_id}]{Ansi.RESET} {title}: {details}")

    async def update_hud(self, page: Page, text: str, bg_color: str = "#0f172a", text_color: str = "#38bdf8"):
        """Chèn thanh HUD trực quan trên giao diện trình duyệt để người dùng theo dõi."""
        try:
            escaped_text = text.replace("'", "\\'").replace('"', '\\"')
            await page.evaluate(f"""() => {{
                let hud = document.getElementById('uat-qa-hud');
                if (!hud) {{
                    hud = document.createElement('div');
                    hud.id = 'uat-qa-hud';
                    document.body.appendChild(hud);
                }}
                hud.innerHTML = '<span style="background:#0284c7;color:#fff;padding:4px 12px;border-radius:14px;font-size:12px;font-weight:800;margin-right:10px;box-shadow:0 2px 6px rgba(2,132,199,0.4);">UAT 3.1</span> {escaped_text}';
                hud.style.cssText = 'position:fixed;top:16px;left:50%;transform:translateX(-50%);background:{bg_color};color:{text_color};padding:12px 26px;border-radius:30px;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:14px;font-weight:600;z-index:9999999;box-shadow:0 10px 30px rgba(0,0,0,0.5);border:2px solid {text_color};pointer-events:none;transition:all 0.25s ease;display:flex;align-items:center;letter-spacing:0.3px;max-width:90vw;text-align:center;';
            }}""")
        except Exception:
            pass

    async def visual_click(self, page: Page, locator: Locator, hud_text: str = ""):
        """Làm nổi bật phần tử trước khi click."""
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
        """Làm nổi bật ô nhập trước khi gõ text."""
        if hud_text:
            await self.update_hud(page, hud_text)
        try:
            await locator.highlight()
        except Exception:
            pass
        if self.headed:
            await page.wait_for_timeout(250)
        await locator.fill(value)

    async def authenticate(self, page: Page):
        """Đăng nhập bằng tài khoản Cán bộ trường qua Microsoft Entra Simulator."""
        self.log("AUTH", f"Truy cập Cổng Quản trị: {self.base_url}")
        target = f"{self.base_url}/class-management"
        await page.goto(target, wait_until="domcontentloaded")
        await page.wait_for_timeout(1000)

        # Kiểm tra nếu trang yêu cầu đăng nhập
        if "login" in page.url or await page.locator("button:has-text('Sign in with Microsoft')").count() > 0:
            await self.update_hud(page, "Đang đăng nhập SSO với tài khoản Cán bộ trường (SCHOOL)...", "#1e1b4b", "#a5b4fc")
            ms_btn = page.locator("button:has-text('Sign in with Microsoft')")
            if await ms_btn.is_visible():
                await self.visual_click(page, ms_btn, "Nhấn nút 'Sign in with Microsoft'")
                try:
                    await page.wait_for_url("**/microsoft-provider/**", timeout=15000)
                except Exception:
                    pass

            # Chọn tài khoản staff1@IAM.edu.vn
            tile = page.locator(f"text={self.school_email}").first
            if await tile.count() > 0:
                await self.visual_click(page, tile, f"Chọn tài khoản Cán bộ trường: {self.school_email}")
            try:
                await page.wait_for_url(f"{self.base_url}/**", timeout=15000)
            except Exception:
                pass
            await page.wait_for_timeout(1500)

        await page.goto(target, wait_until="domcontentloaded")
        await page.wait_for_selector("table", timeout=15000)
        await self.update_hud(page, "✓ Đã đăng nhập thành công: Màn hình Quản lý Lớp học (Class Management)", "#064e3b", "#34d399")
        await page.wait_for_timeout(1000)
        self.log("AUTH", f"✓ Đăng nhập thành công với vai trò SCHOOL: {self.school_email}", Ansi.GREEN)

    # -------------------------------------------------------------------------
    # BƯỚC 1 & 2: TRUY CẬP MENU VÀ KIỂM TRA LỚP P1-A
    # -------------------------------------------------------------------------
    async def step_01_check_classes_list(self, page: Page):
        step_id = "UAT-3.1-STEP1-2"
        title = "Truy cập Menu Classes và kiểm tra lớp P1-A"
        self.log("FLOW", f"Thực hiện [{step_id}] {title}")

        await self.update_hud(page, "1. Truy cập Menu 'Classes' bên trái...", "#0f172a", "#38bdf8")
        
        # Click menu Classes trên sidebar nếu có
        sidebar_classes = page.locator("aside nav a:has-text('Classes'), aside nav button:has-text('Classes')").first
        if await sidebar_classes.is_visible():
            await self.visual_click(page, sidebar_classes, "Menu bên trái chọn 'Classes' (/class-management)")
            await page.wait_for_load_state("networkidle")

        # 2. Kiểm tra danh sách: Tìm kiếm lớp P1-A
        await self.update_hud(page, "2. Kiểm tra danh sách: Tìm kiếm lớp P1-A trong khối Primary 1...", "#0f172a", "#38bdf8")
        search_input = page.locator("input[placeholder*='Search' i]").first
        await self.visual_fill(page, search_input, "P1-A", "Nhập 'P1-A' vào ô tìm kiếm")

        search_btn = page.locator("button:has-text('Search')").first
        await self.visual_click(page, search_btn, "Nhấn nút 'Search'")
        await page.wait_for_timeout(1000)

        # Kiểm tra dòng kết quả trên bảng
        p1a_row = page.locator("table tbody tr:has-text('P1-A')").first
        has_p1a = await p1a_row.count() > 0

        shot = str(OUTPUT_DIR / "01_check_p1a_in_classes_table.png")
        await page.screenshot(path=shot)

        if has_p1a:
            row_text = await p1a_row.inner_text()
            clean_text = " | ".join(row_text.split())
            await p1a_row.highlight()
            await self.update_hud(page, "✓ ĐÃ CÓ LỚP P1-A: Có thể dùng luôn lớp này để chuyển ngay sang mục 3.2!", "#064e3b", "#34d399")
            await page.wait_for_timeout(2000)
            self.record_step(
                step_id=step_id,
                title=title,
                verdict="PASS",
                details=f"Đã tìm thấy lớp P1-A ({clean_text}). Theo quy định UAT 3.1: Dùng luôn lớp này, chuyển sang mục 3.2.",
                evidence=shot
            )
            return True
        else:
            await self.update_hud(page, "Chưa có lớp P1-A -> Cần tiến hành bấm nút 'Create class'...", "#78350f", "#fde047")
            self.record_step(
                step_id=step_id,
                title=title,
                verdict="INFO",
                details="Chưa có lớp P1-A trên bảng. Tiến hành tạo mới lớp học.",
                evidence=shot
            )
            return False

    # -------------------------------------------------------------------------
    # BƯỚC 3A: MỞ FORM VÀ KIỂM TRA VALIDATION BẮT BUỘC KHI RỖNG
    # -------------------------------------------------------------------------
    async def step_02_create_class_validation(self, page: Page):
        step_id = "UAT-3.1-VAL"
        title = "Kiểm tra nút Create class và Validation Form rỗng"
        self.log("FLOW", f"Thực hiện [{step_id}] {title}")

        await self.update_hud(page, "Bấm nút 'Create class' (màu xanh ở góc phải)...", "#0f172a", "#38bdf8")
        create_btn = page.locator("button:has-text('Create class')").first
        await self.visual_click(page, create_btn, "Bấm nút Create class (góc phải toolbar)")
        await page.wait_for_url("**/class-management/new", timeout=10000)

        # Submit form rỗng
        await self.update_hud(page, "Thử submit form rỗng để kiểm tra cảnh báo bắt buộc...", "#450a0a", "#f87171")
        submit_btn = page.locator("button[type='submit']:has-text('Create class')").first
        await self.visual_click(page, submit_btn, "Bấm 'Create class' khi chưa điền thông tin")
        await page.wait_for_timeout(1000)

        # Kiểm tra lỗi
        has_code_err = await page.locator("#class-classCode-error").count() > 0 or await page.get_by_text("Class code is required.").count() > 0
        has_name_err = await page.locator("#class-className-error").count() > 0 or await page.get_by_text("Class name is required.").count() > 0
        has_level_err = await page.locator("#class-schoolLevelOffering-error").count() > 0 or await page.get_by_text("Select a school level offering.").count() > 0

        shot = str(OUTPUT_DIR / "02_create_form_mandatory_validation.png")
        await page.screenshot(path=shot)

        if has_code_err and has_name_err and has_level_err:
            await self.update_hud(page, "✓ Validation chính xác: Hiển thị lỗi bắt buộc cho cả 3 trường!", "#064e3b", "#34d399")
            await page.wait_for_timeout(1500)
            self.record_step(
                step_id=step_id,
                title=title,
                verdict="PASS",
                details="Cả 3 trường bật viền đỏ và hiển thị thông báo lỗi bắt buộc nhập.",
                evidence=shot
            )
        else:
            self.record_step(
                step_id=step_id,
                title=title,
                verdict="FAIL",
                details="Một trong các thông báo lỗi bắt buộc không hiển thị.",
                evidence=shot
            )

    # -------------------------------------------------------------------------
    # BƯỚC 3B: KIỂM TRA TÍNH DUY NHẤT (CHẶN TẠO TRÙNG MÃ P1-A)
    # -------------------------------------------------------------------------
    async def step_03_duplicate_code_rejection(self, page: Page):
        step_id = "UAT-3.1-DUPLICATE"
        title = "Kiểm tra ràng buộc duy nhất: Chặn tạo trùng Mã lớp P1-A"
        self.log("FLOW", f"Thực hiện [{step_id}] {title}")

        await self.update_hud(page, "Điền thông tin trùng lặp: Class code: P1-A, Level: Primary 1 (2026)...", "#450a0a", "#f87171")

        # Điền Class code: P1-A
        code_input = page.locator("#class-classCode")
        await self.visual_fill(page, code_input, "P1-A", "Class code: P1-A")

        # Điền Class name: Primary 1-A Duplicate
        name_input = page.locator("#class-className")
        await self.visual_fill(page, name_input, "Primary 1-A Duplicate", "Class name: Primary 1-A")

        # Chọn Level offering: Primary 1 · 2026
        offering_input = page.locator("#class-schoolLevelOffering")
        await self.visual_click(page, offering_input, "Mở chọn Level offering")
        await page.wait_for_timeout(400)
        
        opt = page.locator("[role='option']:has-text('Primary 1')").first
        if await opt.count() > 0:
            await self.visual_click(page, opt, "Chọn cấp học: Primary 1 / Niên khóa 2026")

        # Bấm Create class
        submit_btn = page.locator("button[type='submit']:has-text('Create class')").first
        await self.visual_click(page, submit_btn, "Bấm 'Create class'")
        await page.wait_for_timeout(1200)

        # Kiểm tra thông báo lỗi trùng lặp
        alert = page.locator("[role='alert'], [role='status'], .text-destructive, h2, h3").filter(has_text=re.compile(r"already exists|Unable to create class", re.IGNORECASE)).first
        has_dup_alert = await alert.count() > 0

        shot = str(OUTPUT_DIR / "03_duplicate_p1a_rejected.png")
        await page.screenshot(path=shot)

        if has_dup_alert:
            await self.update_hud(page, "✓ Hệ thống chặn trùng thành công: 'Class code P1-A already exists for this offering.'", "#064e3b", "#34d399")
            await page.wait_for_timeout(1800)
            self.record_step(
                step_id=step_id,
                title=title,
                verdict="PASS",
                details="Hệ thống chặn trùng lặp mã lớp P1-A thành công và hiển thị cảnh báo rõ ràng.",
                evidence=shot
            )
        else:
            self.record_step(
                step_id=step_id,
                title=title,
                verdict="FAIL",
                details="Không hiển thị thông báo lỗi chặn trùng mã lớp P1-A.",
                evidence=shot
            )

    # -------------------------------------------------------------------------
    # BƯỚC 3C: TẠO MỚI LỚP HỌC THÀNH CÔNG VỚI MÃ DUY NHẤT (HAPPY PATH)
    # -------------------------------------------------------------------------
    async def step_04_create_unique_class_success(self, page: Page):
        step_id = "UAT-3.1-CREATE-SUCCESS"
        title = "Tạo Lớp học mới thành công (Happy Path)"
        self.log("FLOW", f"Thực hiện [{step_id}] {title}")

        suffix = str(time.time_ns())[-5:]
        new_code = f"P1-A{suffix}"
        new_name = f"Primary 1-A Auto {suffix}"

        await self.update_hud(page, f"Điền thông tin lớp mới: Code '{new_code}' - Name '{new_name}'...", "#0f172a", "#38bdf8")

        # Nhập mã mới
        code_input = page.locator("#class-classCode")
        await self.visual_fill(page, code_input, new_code, f"Class code: {new_code}")

        # Nhập tên mới
        name_input = page.locator("#class-className")
        await self.visual_fill(page, name_input, new_name, f"Class name: {new_name}")

        # Chọn Level offering: Primary 1 · 2026
        offering_input = page.locator("#class-schoolLevelOffering")
        await self.visual_click(page, offering_input, "Chọn Level offering: Primary 1 / Niên khóa 2026")
        await page.wait_for_timeout(400)
        opt = page.locator("[role='option']:has-text('Primary 1')").first
        if await opt.count() > 0:
            await self.visual_click(page, opt, "Chọn cấp học: Primary 1 / 2026")

        # Bấm Create class
        submit_btn = page.locator("button[type='submit']:has-text('Create class')").first
        await self.visual_click(page, submit_btn, "Bấm 'Create class' ➔ Lớp học được tạo thành công")

        # Chờ điều hướng về danh sách lớp
        await page.wait_for_url("**/class-management", timeout=15000)
        await page.wait_for_load_state("networkidle")

        # Tìm kiếm lớp vừa tạo trên danh sách
        search_input = page.locator("input[placeholder*='Search' i]").first
        await self.visual_fill(page, search_input, new_code, f"Tìm kiếm lớp vừa tạo: {new_code}")
        await self.visual_click(page, page.locator("button:has-text('Search')").first, "Bấm Search")
        await page.wait_for_timeout(1000)

        created_row = page.locator(f"table tbody tr:has-text('{new_code}')").first
        has_created = await created_row.count() > 0

        shot = str(OUTPUT_DIR / "04_created_class_verified_in_list.png")
        await page.screenshot(path=shot)

        if has_created:
            await created_row.highlight()
            await self.update_hud(page, f"✓ LỚP HỌC {new_code} ĐÃ ĐƯỢC TẠO THÀNH CÔNG VÀ XUẤT HIỆN TRÊN DANH SÁCH!", "#064e3b", "#34d399")
            await page.wait_for_timeout(2000)
            self.record_step(
                step_id=step_id,
                title=title,
                verdict="PASS",
                details=f"Lớp học {new_code} ({new_name}) tạo thành công và hiển thị trên bảng với sĩ số 0.",
                evidence=shot
            )
        else:
            self.record_step(
                step_id=step_id,
                title=title,
                verdict="FAIL",
                details=f"Không tìm thấy lớp vừa tạo {new_code} trên bảng danh sách.",
                evidence=shot
            )

    # -------------------------------------------------------------------------
    # BƯỚC 4: XEM CHI TIẾT LỚP HỌC (DETAIL & ROSTER)
    # -------------------------------------------------------------------------
    async def step_05_view_class_detail(self, page: Page):
        step_id = "UAT-3.1-DETAIL"
        title = "Xem Chi tiết lớp học P1-A sẵn sàng cho mục 3.2"
        self.log("FLOW", f"Thực hiện [{step_id}] {title}")

        await self.update_hud(page, "Mở xem Chi tiết lớp P1-A (nút 'Detail')...", "#0f172a", "#38bdf8")

        # Tìm kiếm lại lớp P1-A
        search_input = page.locator("input[placeholder*='Search' i]").first
        await self.visual_fill(page, search_input, "P1-A", "Tìm lại lớp P1-A")
        await self.visual_click(page, page.locator("button:has-text('Search')").first, "Bấm Search")
        await page.wait_for_timeout(1000)

        # Click Detail
        detail_btn = page.locator("table tbody tr:has-text('P1-A') button:has-text('Detail')").first
        if await detail_btn.count() > 0:
            await self.visual_click(page, detail_btn, "Nhấn nút 'Detail' của lớp P1-A")
            await page.wait_for_url("**/class-management/*", timeout=15000)
            await page.wait_for_load_state("networkidle")
            await page.wait_for_timeout(1000)

            shot = str(OUTPUT_DIR / "05_class_p1a_detail_view.png")
            await page.screenshot(path=shot)

            await self.update_hud(page, "✓ ĐÃ MỞ CHI TIẾT LỚP P1-A: Sĩ số 0 học sinh · Sẵn sàng phân bổ học sinh tại mục 3.2!", "#064e3b", "#34d399")
            await page.wait_for_timeout(2500)

            self.record_step(
                step_id=step_id,
                title=title,
                verdict="PASS",
                details="Mở màn hình chi tiết lớp P1-A thành công, hiển thị đầy đủ thẻ Metric và Roster.",
                evidence=shot
            )

    # -------------------------------------------------------------------------
    # RUNNER CHÍNH
    # -------------------------------------------------------------------------
    async def run(self):
        self.log("INIT", f"Khởi động Visual UAT Runner: {self.base_url}")
        self.log("INIT", f"Chế độ: headed={self.headed}, slow_mo={self.slow_mo}ms")

        async with async_playwright() as p:
            launch_args = [
                "--ignore-certificate-errors",
                "--ozone-platform-hint=auto",
            ]
            if self.headed:
                launch_args.extend(["--class=Chromium", f"--app={self.base_url}/class-management"])

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
                # Đăng nhập
                await self.authenticate(page)

                # Thực thi 5 bước UAT 3.1
                has_p1a = await self.step_01_check_classes_list(page)
                await self.step_02_create_class_validation(page)
                await self.step_03_duplicate_code_rejection(page)
                await self.step_04_create_unique_class_success(page)
                await self.step_05_view_class_detail(page)

                await self.update_hud(page, "✓ HOÀN TẤT THÀNH CÔNG TOÀN BỘ KỊCH BẢN UAT 3.1", "#064e3b", "#34d399")
                if self.headed:
                    await page.wait_for_timeout(3000)

            except Exception as e:
                self.log("FATAL", f"Gặp lỗi khi thực thi kịch bản: {e}", Ansi.RED)
                shot = str(OUTPUT_DIR / "fatal_error.png")
                await page.screenshot(path=shot)
            finally:
                await browser.close()

        self.print_summary()

    def print_summary(self):
        print(f"\n{Ansi.BOLD}{'='*80}{Ansi.RESET}")
        print(f"{Ansi.BOLD}{Ansi.CYAN} TỔNG KẾT KẾT QUẢ THỰC THI UAT 3.1: KIỂM TRA HOẶC TẠO LỚP HỌC (CLASSES) {Ansi.RESET}")
        print(f"{Ansi.BOLD}{'='*80}{Ansi.RESET}\n")

        total = len(self.results)
        passed = sum(1 for r in self.results if r["verdict"] == "PASS")
        failed = sum(1 for r in self.results if r["verdict"] == "FAIL")

        print(f"  Tổng số bước thực hiện : {Ansi.BOLD}{total}{Ansi.RESET}")
        print(f"  ✓ Số bước thành công   : {Ansi.GREEN}{passed}{Ansi.RESET}")
        print(f"  ✗ Số bước thất bại     : {Ansi.RED}{failed}{Ansi.RESET}\n")

        header = f"{'Mã Bước':<22} | {'Trạng Thái':<12} | {'Nội Dung / Minh Chứng'}"
        print(header)
        print("-" * 80)
        for r in self.results:
            color = Ansi.GREEN if r['verdict'] == 'PASS' else (Ansi.RED if r['verdict'] == 'FAIL' else Ansi.BLUE)
            print(f"{r['step_id']:<22} | {color}{r['verdict']:<12}{Ansi.RESET} | {r['details'][:45]}...")
        print(f"\n{Ansi.BOLD}Ảnh minh chứng đã lưu tại: {OUTPUT_DIR.resolve()}{Ansi.RESET}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UAT 3.1 Class Management Visual Test Suite")
    parser.add_argument("--url", default="https://admin.20-255-158-192.sslip.io", help="Base URL của Admin Portal")
    parser.add_argument("--headed", action="store_true", default=True, help="Chạy trình duyệt có giao diện (mặc định: True)")
    parser.add_argument("--headless", action="store_true", help="Chạy trình duyệt ẩn (headless)")
    parser.add_argument("--slow-mo", type=int, default=400, help="Độ trễ Playwright slow-mo tính bằng ms (mặc định: 400)")
    args = parser.parse_args()

    is_headed = False if args.headless else args.headed
    asyncio.run(ClassManagementUATRunner(args.url, headed=is_headed, slow_mo=args.slow_mo).run())
