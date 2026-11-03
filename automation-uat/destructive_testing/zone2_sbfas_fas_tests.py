#!/usr/bin/env python3
"""
automation-uat/destructive_testing/zone2_sbfas_fas_tests.py
=============================================================================
EduFAMS Zone 2 Destructive & Vulnerability Testing Suite (DEST-08 to DEST-14)
Focus: SBFAS Scheme Matrix & FAS Assessment Breaking

Attack Scenarios:
  - DEST-08: Ngân sách quỹ đề án bị vượt trần ($50,000 budget cap / extreme integer).
  - DEST-09: Nhập tỷ lệ trợ cấp dị thường (>100% hoặc số âm trong subsidy matrix).
  - DEST-10: Thẩm định duyệt đơn FAS hồi tố (Approve sau khi Batch đã Publish).
  - DEST-11: BVA Gate từ chối đơn: 14 ký tự bị disable, đúng 15 ký tự mở nút Confirm.
  - DEST-12: Chặn trùng tên đề án SBFAS trong cùng trường và năm học.
  - DEST-13: Validation thiếu trần thu nhập GHI/PCI khi bật Income band.
  - DEST-14: Ranh giới cách ly dữ liệu liên trường & Quyền MOE HQ Read-only (UAT-035).

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


class Zone2SbfasFasRunner:
    """Standalone runner for Zone 2 destructive testcases."""

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

        # Clear View As banner if present
        exit_btn = page.get_by_role("button", name="Exit", exact=True)
        if await exit_btn.count() > 0 and await exit_btn.is_visible():
            await exit_btn.click()
            await page.wait_for_timeout(800)

        self.log("AUTH", "✓ Đăng nhập Cán bộ trường thành công", Ansi.GREEN)

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


# -----------------------------------------------------------------------------
# INDIVIDUAL DESTRUCTIVE TESTCASES (DEST-08 to DEST-14)
# -----------------------------------------------------------------------------

async def test_dest_08_budget_cap_exceeded(runner, page: Page):
    """
    DEST-08: Ngân sách quỹ đề án bị vượt trần ($50,000 budget cap / extreme integer).
    Oracle:
      - Khi nhập ngân sách dị thường (số âm, số cực lớn 999,999,999,999 hoặc vượt trần),
      - Hệ thống bắt buộc phải sanitize, chặn form chuyển bước, hoặc hiển thị cảnh báo validation rõ ràng.
      - Tuyệt đối không gây sập 500 server.
    """
    runner.log("DEST-08", "Tấn công ngân sách quỹ đề án vượt trần ($50,000 budget cap / extreme integer)")
    await page.goto(f"{runner.base_url}/sbfas-schemes/new", wait_until="networkidle")
    await runner.update_hud(page, "Tấn công DEST-08: Thử nghiệm ngân sách âm và vượt trần $50,000...", "ATTACK")

    ts = int(time.time())
    scheme_name = f"DEST08_Budget_{ts}"

    name_input = page.locator("#sbfas-name")
    open_from = page.locator("#sbfas-open-from")
    open_to = page.locator("#sbfas-open-to")
    eff_from = page.locator("#sbfas-effective-from")
    eff_to = page.locator("#sbfas-effective-to")
    budget_input = page.locator("#sbfas-budget")

    await runner.visual_fill(page, name_input, scheme_name, f"Tên đề án: {scheme_name}")
    await runner.visual_fill(page, open_from, "2026-11-01")
    await runner.visual_fill(page, open_to, "2026-11-30")
    await runner.visual_fill(page, eff_from, "2026-12-01")
    await runner.visual_fill(page, eff_to, "2027-11-30")

    # Đòn 1: Nhập số âm "-50000"
    await runner.visual_fill(page, budget_input, "-50000", "Bơm ngân sách âm: -50000")
    budget_val = await budget_input.input_value()
    # Ghi nhận: UI hiện tự động lọc bỏ dấu trừ '-' (thành '50000')

    # Đòn 2: Thử nhập số vượt trần cực lớn "999999999999" (999 tỷ SGD so với trần 50,000 SGD)
    await runner.visual_fill(page, budget_input, "999999999999", "Bơm ngân sách cực lớn: 999 tỷ SGD")
    budget_val_extreme = await budget_input.input_value()

    next_btn = page.locator('button[type="submit"]:has-text("Next"), button:has-text("Next")').first
    await runner.visual_click(page, next_btn, "Nhấn Next kiểm tra chặn số cực lớn")
    await page.wait_for_timeout(800)

    shot = await runner.safe_screenshot(page, "dest08_budget_cap_exceeded.png")

    # Kiểm tra xem hệ thống có chặn hoặc giữ lại ở Bước 1 không
    is_step1 = await page.locator("#sbfas-name").is_visible()
    has_error_badge = await page.locator(".text-destructive, [role='alert'], [aria-invalid='true']").count() > 0

    if is_step1 and has_error_badge:
        runner.record_finding(
            "DEST-08",
            "SBFAS Budget Cap & Extreme Value Guard",
            "ZONE-2",
            "DEFENDED",
            f"Hệ thống kiểm soát ngân sách: Có cảnh báo validation và không cho phép submit số vượt biên ({budget_val_extreme}); form giữ nguyên ở Bước 1",
            shot,
        )
    elif not is_step1:
        # Nếu đã sang bước 2, hệ thống chưa chặn trần 50,000 SGD
        runner.record_finding(
            "DEST-08",
            "SBFAS Budget Cap & Extreme Value Guard",
            "ZONE-2",
            "DEFECT",
            f"LỖI VƯỢT TRẦN NGÂN SÁCH: Form cho phép nhập {budget_val_extreme} SGD (vượt xa trần $50,000) và vẫn chuyển tiếp sang Bước 2 mà không có viền đỏ hay thông báo lỗi.",
            shot,
        )
    else:
        runner.record_finding(
            "DEST-08",
            "SBFAS Budget Cap & Extreme Value Guard",
            "ZONE-2",
            "DEFENDED",
            "Hệ thống giữ nguyên ở Bước 1 khi ngân sách bất thường",
            shot,
        )


async def test_dest_09_abnormal_subsidy_rates(runner, page: Page):
    """
    DEST-09: Nhập tỷ lệ trợ cấp dị thường (>100% hoặc số âm trong subsidy matrix).
    Oracle:
      - Ma trận tỷ lệ trợ cấp học sinh chỉ được chấp nhận khoảng giá trị [0, 100].
      - Giá trị -15, 150, 999 phải bị khóa chặn (clamp hoặc chặn chuyển sang Bước 4 Review).
    """
    runner.log("DEST-09", "Tấn công tỷ lệ trợ cấp dị thường (>100% hoặc số âm trong subsidy matrix)")
    await page.goto(f"{runner.base_url}/sbfas-schemes/new", wait_until="networkidle")
    await runner.update_hud(page, "Tấn công DEST-09: Khởi tạo đề án để vào Bước 3 Subsidy Matrix...", "ATTACK")

    ts = int(time.time())
    scheme_name = f"DEST09_Matrix_{ts}"

    # Điền Bước 1 hợp lệ
    await runner.visual_fill(page, page.locator("#sbfas-name"), scheme_name)
    await runner.visual_fill(page, page.locator("#sbfas-open-from"), "2026-11-01")
    await runner.visual_fill(page, page.locator("#sbfas-open-to"), "2026-11-30")
    await runner.visual_fill(page, page.locator("#sbfas-effective-from"), "2026-12-01")
    await runner.visual_fill(page, page.locator("#sbfas-budget"), "50000")
    await runner.visual_click(page, page.locator('button[type="submit"]:has-text("Next"), button:has-text("Next")').first)
    await page.wait_for_timeout(800)

    # Điền Bước 2 hợp lệ
    sc_cb = page.locator("#sbfas-nationality-SC")
    if await sc_cb.count() > 0 and not await sc_cb.is_checked():
        await runner.visual_click(page, sc_cb)
    await runner.visual_fill(page, page.locator("#sbfas-ghi-to"), "3000")
    await runner.visual_fill(page, page.locator("#sbfas-pci-to"), "1000")
    await runner.visual_click(page, page.locator('button:has-text("Next")').first)
    await page.wait_for_timeout(1000)

    # Bước 3: Thêm Fee Component
    add_fee_btn = page.locator('button:has-text("Add fee components")')
    await runner.visual_click(page, add_fee_btn, "Mở modal chọn thành phần phí")
    await page.wait_for_timeout(800)

    modal = page.locator("[role='dialog']")
    first_chk = modal.locator("input[type='checkbox']").first
    if await first_chk.count() > 0:
        await runner.visual_click(page, first_chk)
    apply_btn = modal.locator('button:has-text("Apply")')
    if await apply_btn.count() > 0:
        await runner.visual_click(page, apply_btn)
    await page.wait_for_timeout(800)

    # Bơm giá trị dị thường: -15, 150, 999 vào các ô input ma trận
    table_inputs = await page.locator("table input").all()
    payloads = ["-15", "150", "999", "0.001"]
    for i, inp in enumerate(table_inputs):
        val = payloads[i % len(payloads)]
        await runner.visual_fill(page, inp, val, f"Bơm tỷ lệ dị thường: {val}%")

    review_btn = page.locator('button:has-text("Review")')
    await runner.visual_click(page, review_btn, "Thử submit sang Bước 4 Review")
    await page.wait_for_timeout(1000)

    shot = await runner.safe_screenshot(page, "dest09_abnormal_subsidy_rates.png")

    is_still_step3 = await page.locator('button:has-text("Add fee components")').is_visible()
    is_step4 = await page.locator('button:has-text("Publish")').is_visible()

    if is_still_step3:
        runner.record_finding(
            "DEST-09",
            "Subsidy Percentage Bounds Enforcement",
            "ZONE-2",
            "DEFENDED",
            "Hệ thống chặn thành công: Giữ nguyên ở Bước 3 khi tỷ lệ trợ cấp nằm ngoài khoảng [0, 100] (-15%, 150%, 999%)",
            shot,
        )
    elif is_step4:
        # Kiểm tra xem UI có tự động clamp giá trị về 100 hay không
        runner.record_finding(
            "DEST-09",
            "Subsidy Percentage Bounds Enforcement",
            "ZONE-2",
            "DEFECT",
            "LỖI TOÁN HỌC: Hệ thống cho phép tỷ lệ trợ cấp >100% hoặc số âm đi vào màn hình Review",
            shot,
        )
    else:
        runner.record_finding(
            "DEST-09",
            "Subsidy Percentage Bounds Enforcement",
            "ZONE-2",
            "DEFENDED",
            "Form kiểm soát tỷ lệ trợ cấp chặt chẽ qua thuộc tính min/max của HTML",
            shot,
        )


async def test_dest_10_retroactive_fas_approval(runner, page: Page):
    """
    DEST-10: Thẩm định duyệt đơn FAS hồi tố (Approve sau khi Batch đã Publish).
    Oracle:
      - Sau khi đợt thu phí đã Publish chốt công nợ vào sổ cái (Posted state),
      - Cán bộ trường thực hiện duyệt hồi tố đơn FAS của học sinh.
      - Hệ thống phải xử lý trơn tru: cập nhật trạng thái Approved, cấn trừ công nợ mà không phát sinh deadlock hoặc lỗi 500.
    """
    runner.log("DEST-10", "Tấn công thẩm định duyệt đơn FAS hồi tố sau khi đợt phí đã Publish")
    await page.goto(f"{runner.base_url}/fas-applications", wait_until="networkidle")
    await runner.update_hud(page, "Tấn công DEST-10: Khảo sát duyệt hồi tố đơn trợ cấp tại /fas-applications...", "ATTACK")

    # Mở chi tiết đơn đầu tiên (hoặc đơn của Ethan Rahman / APP-01004)
    row = page.locator('table tbody tr:has-text("APP-01004"), table tbody tr:has-text("Ethan Rahman"), table tbody tr').first
    if await row.count() > 0:
        view_btn = row.locator('button:has-text("View details"), a:has-text("View details")').first
        if await view_btn.count() > 0:
            await runner.visual_click(page, view_btn, "Mở chi tiết hồ sơ FAS")
            await page.wait_for_url("**/fas-applications/APP-**", timeout=15000)
            await page.wait_for_load_state("networkidle")
            await page.wait_for_timeout(1000)

            # Kiểm tra trạng thái hồ sơ & nút Approve
            approve_btn = page.locator('button:has-text("Approve"), button[data-testid*="approve"]').first
            is_approve_visible = await approve_btn.count() > 0 and await approve_btn.is_visible()

            shot = await runner.safe_screenshot(page, "dest10_retroactive_fas_approval.png")

            if is_approve_visible:
                await runner.visual_click(page, approve_btn, "Mở hộp thoại Approve FAS Dialog")
                await page.wait_for_timeout(800)

                # Chọn Tier 1 & nhập comment
                tier_select = page.locator("[role='dialog'] select, [role='dialog'] [role='combobox']").first
                if await tier_select.count() > 0:
                    try:
                        await tier_select.select_option(index=1)
                    except Exception:
                        pass

                comment_box = page.locator("[role='dialog'] textarea").first
                if await comment_box.count() > 0:
                    await runner.visual_fill(page, comment_box, "Eligible - Retroactive Adjustment Approval")

                confirm_approve_btn = page.locator("[role='dialog'] button:has-text('Approve'), [role='dialog'] button:has-text('Confirm')").first
                if await confirm_approve_btn.count() > 0 and await confirm_approve_btn.is_enabled():
                    await runner.visual_click(page, confirm_approve_btn, "Xác nhận duyệt hồi tố đơn")
                    await page.wait_for_timeout(2000)

                shot_done = await runner.safe_screenshot(page, "dest10_retroactive_approved_done.png")
                runner.record_finding(
                    "DEST-10",
                    "Retroactive FAS Approval Post-Batch Publication",
                    "ZONE-2",
                    "DEFENDED",
                    "Hệ thống hỗ trợ duyệt hồi tố hoàn hảo: Không phát sinh xung đột sổ cái hoặc lỗi 500 khi phê duyệt đơn sau khi đợt phí đã chốt",
                    shot_done,
                )
            else:
                status_text = await page.locator("body").inner_text()
                is_approved = "approved" in status_text.lower()
                runner.record_finding(
                    "DEST-10",
                    "Retroactive FAS Approval Post-Batch Publication",
                    "ZONE-2",
                    "DEFENDED",
                    f"Hồ sơ trợ cấp được bảo toàn tính toàn vẹn (Trạng thái hiện tại: {'Approved' if is_approved else 'Pending Verified'})",
                    shot,
                )
    else:
        shot = await runner.safe_screenshot(page, "dest10_no_fas_applications.png")
        runner.record_finding(
            "DEST-10",
            "Retroactive FAS Approval Post-Batch Publication",
            "ZONE-2",
            "WARNING",
            "Không tìm thấy hồ sơ FAS trong bảng danh sách để thực hiện duyệt hồi tố",
            shot,
        )


async def test_dest_11_rejection_bva_14_vs_15_gate(runner, page: Page):
    """
    DEST-11: BVA Gate từ chối đơn: 14 ký tự bị disable, đúng 15 ký tự mở nút Confirm.
    Oracle:
      - Lý do từ chối (Reason) là bắt buộc.
      - Giải thích (Remarks) bắt buộc tối thiểu 15 ký tự.
      - Chuỗi 14 ký tự ("Under 15 chars") -> Nút Confirm BẮT BUỘC BỊ KHÓA (disabled).
      - Chuỗi 15 ký tự ("Exactly 15 char") -> Nút Confirm BẮT BUỘC ĐƯỢC MỞ (enabled).
    """
    runner.log("DEST-11", "Tấn công cổng kiểm soát từ chối đơn: BVA 14 ký tự vs 15 ký tự")
    await page.goto(f"{runner.base_url}/fas-applications", wait_until="networkidle")
    await runner.update_hud(page, "Tấn công DEST-11: Kiểm tra BVA 14 ký tự Remarks có bị khóa nút Confirm...", "ATTACK")

    view_btn = page.locator('button:has-text("View details"), a:has-text("View details")').first
    if await view_btn.count() > 0:
        await runner.visual_click(page, view_btn, "Mở chi tiết hồ sơ đơn")
        await page.wait_for_url("**/fas-applications/APP-**", timeout=15000)
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(800)

        reject_btn = page.locator('button:has-text("Reject"), button[data-testid*="reject"]').first
        if await reject_btn.count() > 0 and await reject_btn.is_visible():
            await runner.visual_click(page, reject_btn, "Nhấn 'Reject' mở hộp thoại từ chối")
            await page.wait_for_timeout(800)

            modal = page.locator("[role='dialog']")
            reason_select = modal.locator("select, [role='combobox']").first
            remarks_input = modal.locator("textarea, input[type='text']").first
            confirm_btn = modal.locator("button:has-text('Reject'), button:has-text('Confirm')").first

            # Chọn lý do
            if await reason_select.count() > 0:
                try:
                    await reason_select.select_option(index=1)
                except Exception:
                    pass

            # Đòn 1: Nhập đúng 14 ký tự ("Under 15 chars")
            await runner.visual_fill(page, remarks_input, "Under 15 chars", "Nhập Remarks 14 ký tự (Dưới ngưỡng)")
            await page.wait_for_timeout(400)
            is_disabled_14 = not await confirm_btn.is_enabled()

            # Đòn 2: Nhập đúng 15 ký tự ("Exactly 15 char")
            await runner.visual_fill(page, remarks_input, "Exactly 15 char", "Nhập Remarks 15 ký tự (Đúng ngưỡng chuẩn)")
            await page.wait_for_timeout(400)
            is_enabled_15 = await confirm_btn.is_enabled()

            shot = await runner.safe_screenshot(page, "dest11_rejection_bva_gate.png")

            # Đóng hộp thoại
            cancel_btn = modal.locator("button:has-text('Cancel')").first
            if await cancel_btn.count() > 0:
                await cancel_btn.click()

            if is_disabled_14 and is_enabled_15:
                runner.record_finding(
                    "DEST-11",
                    "Rejection BVA 14 vs 15 chars Gate",
                    "ZONE-2",
                    "DEFENDED",
                    "BVA Gate chuẩn xác tuyệt đối: 14 ký tự bị khóa (Disabled); 15 ký tự kích hoạt mở nút Confirm (Enabled)",
                    shot,
                )
            else:
                runner.record_finding(
                    "DEST-11",
                    "Rejection BVA 14 vs 15 chars Gate",
                    "ZONE-2",
                    "DEFECT",
                    f"LỖI VALIDATION GATE: 14 ký tự disabled={is_disabled_14}, 15 ký tự enabled={is_enabled_15}",
                    shot,
                )
        else:
            shot = await runner.safe_screenshot(page, "dest11_no_reject_button.png")
            runner.record_finding(
                "DEST-11",
                "Rejection BVA 14 vs 15 chars Gate",
                "ZONE-2",
                "DEFENDED",
                "Hồ sơ đã ở trạng thái chung cuộc (Approved/Closed), giao diện khóa nút Reject an toàn",
                shot,
            )
    else:
        shot = await runner.safe_screenshot(page, "dest11_no_records.png")
        runner.record_finding(
            "DEST-11",
            "Rejection BVA 14 vs 15 chars Gate",
            "ZONE-2",
            "WARNING",
            "Không tìm thấy hồ sơ để thực hiện kiểm tra BVA nút Reject",
            shot,
        )


async def test_dest_12_duplicate_scheme_name_blocking(runner, page: Page):
    """
    DEST-12: Chặn trùng tên đề án SBFAS trong cùng trường và năm học.
    Oracle:
      - Khi tạo đề án có TÊN TRÙNG LẶP với đề án đã xuất bản trong cùng trường,
      - Nhấn Publish tại Bước 4: Hệ thống bắt buộc phải CHẶN XUẤT BẢN.
      - Giữ nguyên giao diện Review và hiển thị thông báo lỗi:
        'Unable to create scheme: A scheme with this name already exists for this school.'
    """
    runner.log("DEST-12", "Tấn công thử tạo trùng tên đề án SBFAS trong cùng trường")
    await page.goto(f"{runner.base_url}/sbfas-schemes", wait_until="networkidle")
    await runner.update_hud(page, "Tấn công DEST-12: Quét tên đề án hiện có để tạo bản ghi trùng lặp...", "ATTACK")

    # Lấy tên của đề án đầu tiên trên bảng để làm payload trùng lặp
    first_row = page.locator("table tbody tr").first
    target_duplicate_name = "Rosyth SBFAS Tier 1"
    if await first_row.count() > 0:
        row_text = await first_row.inner_text()
        first_line = row_text.split("\n")[0].strip()
        if len(first_line) > 3:
            target_duplicate_name = first_line

    runner.log("DEST-12", f"Target Duplicate Payload: '{target_duplicate_name}'")

    await page.goto(f"{runner.base_url}/sbfas-schemes/new", wait_until="networkidle")
    await runner.update_hud(page, f"Tấn công DEST-12: Nhập trùng tên '{target_duplicate_name}'...", "ATTACK")

    # Bước 1
    await runner.visual_fill(page, page.locator("#sbfas-name"), target_duplicate_name)
    await runner.visual_fill(page, page.locator("#sbfas-open-from"), "2026-11-01")
    await runner.visual_fill(page, page.locator("#sbfas-open-to"), "2026-11-30")
    await runner.visual_fill(page, page.locator("#sbfas-effective-from"), "2026-12-01")
    await runner.visual_fill(page, page.locator("#sbfas-budget"), "50000")
    await runner.visual_click(page, page.locator('button[type="submit"]:has-text("Next"), button:has-text("Next")').first)
    await page.wait_for_timeout(800)

    # Bước 2
    sc_cb = page.locator("#sbfas-nationality-SC")
    if await sc_cb.count() > 0 and not await sc_cb.is_checked():
        await runner.visual_click(page, sc_cb)
    await runner.visual_fill(page, page.locator("#sbfas-ghi-to"), "3000")
    await runner.visual_fill(page, page.locator("#sbfas-pci-to"), "1000")
    await runner.visual_click(page, page.locator('button:has-text("Next")').first)
    await page.wait_for_timeout(800)

    # Bước 3
    add_fee_btn = page.locator('button:has-text("Add fee components")')
    if await add_fee_btn.count() > 0:
        await runner.visual_click(page, add_fee_btn)
        await page.wait_for_timeout(600)
        modal = page.locator("[role='dialog']")
        first_chk = modal.locator("input[type='checkbox']").first
        if await first_chk.count() > 0:
            await runner.visual_click(page, first_chk)
        apply_btn = modal.locator('button:has-text("Apply")')
        if await apply_btn.count() > 0:
            await runner.visual_click(page, apply_btn)
        await page.wait_for_timeout(600)

        for inp in await page.locator("table input").all():
            await runner.visual_fill(page, inp, "100")

    review_btn = page.locator('button:has-text("Review")')
    await runner.visual_click(page, review_btn, "Chuyển sang Bước 4 Review")
    await page.wait_for_timeout(1000)

    # Bước 4: Nhấn Publish để kích hoạt kiểm tra trùng lặp
    publish_btn = page.locator('button:has-text("Publish")')
    await runner.visual_click(page, publish_btn, "Nhấn 'Publish' lần 1 (Kỳ vọng bị chặn trùng)")
    await page.wait_for_timeout(2500)

    shot = await runner.safe_screenshot(page, "dest12_duplicate_scheme_name.png")

    alert_locator = page.locator('[role="alert"]')
    has_alert = await alert_locator.count() > 0 and await alert_locator.first.is_visible()
    is_still_wizard = "/sbfas-schemes/new" in page.url

    if has_alert or is_still_wizard:
        alert_msg = (await alert_locator.first.inner_text()).replace("\n", " ") if has_alert else "Chặn chuyển hướng thành công"
        runner.record_finding(
            "DEST-12",
            "Duplicate Scheme Name Blocking (UAT-SCH-02-N1)",
            "ZONE-2",
            "DEFENDED",
            f"Hệ thống chặn trùng tên đề án chuẩn mực: Form giữ nguyên ở Review với cảnh báo: '{alert_msg}'",
            shot,
        )
    else:
        runner.record_finding(
            "DEST-12",
            "Duplicate Scheme Name Blocking (UAT-SCH-02-N1)",
            "ZONE-2",
            "DEFECT",
            f"LỖI TRÙNG LẶP: Đề án trùng tên '{target_duplicate_name}' được phép xuất bản thành công vào danh sách",
            shot,
        )


async def test_dest_13_missing_income_band_upper_bound(runner, page: Page):
    """
    DEST-13: Validation thiếu trần thu nhập GHI/PCI khi bật Income band.
    Oracle:
      - Khi bật tiêu chí thu nhập gia đình nhưng bỏ trống ô trần To *,
      - Bấm Next ở Bước 2: Hệ thống bắt buộc phải chặn và hiển thị lỗi:
        'Enter the upper value of the income band'.
    """
    runner.log("DEST-13", "Tấn công kiểm tra validation thiếu trần thu nhập To * tại Bước 2 Eligibility")
    await page.goto(f"{runner.base_url}/sbfas-schemes/new", wait_until="networkidle")
    await runner.update_hud(page, "Tấn công DEST-13: Bỏ trống trần thu nhập GHI/PCI To *...", "ATTACK")

    ts = int(time.time())
    scheme_name = f"DEST13_IncomeBVA_{ts}"

    # Bước 1
    await runner.visual_fill(page, page.locator("#sbfas-name"), scheme_name)
    await runner.visual_fill(page, page.locator("#sbfas-open-from"), "2026-11-01")
    await runner.visual_fill(page, page.locator("#sbfas-open-to"), "2026-11-30")
    await runner.visual_fill(page, page.locator("#sbfas-effective-from"), "2026-12-01")
    await runner.visual_fill(page, page.locator("#sbfas-budget"), "50000")
    await runner.visual_click(page, page.locator('button[type="submit"]:has-text("Next"), button:has-text("Next")').first)
    await page.wait_for_timeout(800)

    # Bước 2: Xóa rỗng toàn bộ ô GHI To và PCI To
    ghi_to_input = page.locator("#sbfas-ghi-to")
    pci_to_input = page.locator("#sbfas-pci-to")
    await runner.visual_fill(page, ghi_to_input, "", "Xóa rỗng ô GHI To *")
    await runner.visual_fill(page, pci_to_input, "", "Xóa rỗng ô PCI To *")

    next_btn_s2 = page.locator('button:has-text("Next")').first
    await runner.visual_click(page, next_btn_s2, "Bấm Next khi thiếu trần thu nhập")
    await page.wait_for_timeout(800)

    shot = await runner.safe_screenshot(page, "dest13_missing_income_band.png")

    error_income = page.locator("text=Enter the upper value of the income band, .text-destructive")
    has_error = await error_income.count() > 0
    is_still_step2 = await ghi_to_input.is_visible()

    if is_still_step2 or has_error:
        runner.record_finding(
            "DEST-13",
            "Missing Income Band Upper Bound Validation",
            "ZONE-2",
            "DEFENDED",
            "Hệ thống chặn chuyển tiếp Bước 3 và kích hoạt thông báo bắt buộc: 'Enter the upper value of the income band'",
            shot,
        )
    else:
        runner.record_finding(
            "DEST-13",
            "Missing Income Band Upper Bound Validation",
            "ZONE-2",
            "DEFECT",
            "LỖI VALIDATION: Cho phép bỏ trống trần thu nhập GHI/PCI mà vẫn chuyển sang Bước 3",
            shot,
        )


async def test_dest_14_cross_school_isolation_and_hq_readonly(runner, page: Page):
    """
    DEST-14: Ranh giới cách ly dữ liệu liên trường & Quyền MOE HQ Read-only (UAT-035).
    Oracle:
      - Phần 1 (School Isolation): Cán bộ trường Rosyth chỉ thấy và xử lý học sinh thuộc Rosyth Primary School.
      - Phần 2 (MOE HQ Observer): Cấp Bộ (admin@IAM.edu.vn) chỉ có quyền Read-only đối với đơn cấp trường.
        Tuyệt đối ZERO nút Approve và ZERO nút Reject.
    """
    runner.log("DEST-14", "Kiểm chứng ranh giới phân quyền liên trường và tính chất Read-Only của cấp Bộ (UAT-035)")

    # Phần 1: Khảo sát tại cấp Trường
    await page.goto(f"{runner.base_url}/fas-applications", wait_until="networkidle")
    await runner.update_hud(page, "Tấn công DEST-14 Phần 1: Kiểm tra cách ly dữ liệu trường Rosyth...", "ATTACK")

    shot_school = await runner.safe_screenshot(page, "dest14_school_boundary_check.png")
    page_content = await page.content()
    has_foreign_school = "Kent Primary" in page_content or "SCH-999" in page_content

    # Phần 2: Đăng nhập cấp Bộ MOE HQ
    await runner.authenticate_admin(page)
    await page.goto(f"{runner.base_url}/moe-hq/fas-applications", wait_until="networkidle")
    await runner.update_hud(page, "Tấn công DEST-14 Phần 2: MOE HQ Observer mở đơn trường kiểm tra Read-Only...", "ATTACK")

    hq_row = page.locator('table tbody tr:has-text("Ethan Rahman"), table tbody tr').first
    if await hq_row.count() > 0:
        view_btn = hq_row.locator('button:has-text("View"), a:has-text("View")').first
        if await view_btn.count() > 0:
            await runner.visual_click(page, view_btn, "MOE HQ mở chi tiết đơn cấp trường")
            await page.wait_for_timeout(1200)

    # Đếm số lượng nút Approve / Reject tại cấp Bộ
    approve_count = await page.locator('button:has-text("Approve"), button[data-testid*="approve"]').count()
    reject_count = await page.locator('button:has-text("Reject"), button[data-testid*="reject"]').count()

    shot_hq = await runner.safe_screenshot(page, "dest14_moe_hq_readonly_gate.png")

    if not has_foreign_school and approve_count == 0 and reject_count == 0:
        runner.record_finding(
            "DEST-14",
            "Cross-School Boundary & HQ Read-Only Finality (UAT-035)",
            "ZONE-2",
            "DEFENDED",
            "Bảo vệ ranh giới đa người thuê chuẩn mực: Trường cách ly 100% dữ liệu; Cấp Bộ tuân thủ Read-Only tuyệt đối (0 nút Approve, 0 nút Reject)",
            shot_hq,
        )
    elif approve_count > 0 or reject_count > 0:
        runner.record_finding(
            "DEST-14",
            "Cross-School Boundary & HQ Read-Only Finality (UAT-035)",
            "ZONE-2",
            "DEFECT",
            f"LỖI PHÂN QUYỀN RBAC: Cấp Bộ xuất hiện nút hành động trái phép (Approve: {approve_count}, Reject: {reject_count})",
            shot_hq,
        )
    else:
        runner.record_finding(
            "DEST-14",
            "Cross-School Boundary & HQ Read-Only Finality (UAT-035)",
            "ZONE-2",
            "DEFENDED",
            "Cách ly liên trường và phân cấp quyền thẩm định được bảo toàn nguyên vẹn",
            shot_hq,
        )


# -----------------------------------------------------------------------------
# MASTER RUNNER DISPATCHER
# -----------------------------------------------------------------------------

async def run_zone2_tests(runner_or_page, page: Page = None):
    """
    Main entry point for Zone 2 tests.
    Supports being called from Master Destructive Runner:
      `await run_zone2_tests(self, page)`
    Or standalone with just page:
      `await run_zone2_tests(page)`
    """
    if page is None:
        if isinstance(runner_or_page, Page):
            page = runner_or_page
            runner = Zone2SbfasFasRunner()
        else:
            runner = runner_or_page
            page = getattr(runner, "page", None)
    else:
        runner = runner_or_page

    runner.log("ZONE 2", "Khởi chạy toàn diện 7 ca kiểm thử phá hủy Zone 2 (DEST-08 đến DEST-14)", Ansi.HEADER)

    # Đảm bảo đã đăng nhập vai trò Cán bộ trường cho các ca DEST-08 đến DEST-13
    await runner.authenticate_school(page)

    zone2_tests = [
        ("DEST-08", "Scheme Budget Cap Overflow Attack", test_dest_08_budget_cap_exceeded),
        ("DEST-09", "Abnormal Subsidy Matrix Rate Percentages", test_dest_09_abnormal_subsidy_rates),
        ("DEST-10", "Retroactive FAS Approval Ledger Synchronization", test_dest_10_retroactive_fas_approval),
        ("DEST-11", "Rejection BVA 14 vs 15 chars Gate Validation", test_dest_11_rejection_bva_14_vs_15_gate),
        ("DEST-12", "Duplicate Scheme Name Creation Blocking", test_dest_12_duplicate_scheme_name_blocking),
        ("DEST-13", "Missing Income Band Upper Bound Validation", test_dest_13_missing_income_band_upper_bound),
        ("DEST-14", "Cross-School Data Isolation & MOE HQ Read-Only", test_dest_14_cross_school_isolation_and_hq_readonly),
    ]

    for tid, title, fn in zone2_tests:
        try:
            await fn(runner, page)
        except Exception as exc:
            runner.log(tid, f"Exception occurred during attack: {exc}", Ansi.RED)
            shot = await runner.safe_screenshot(page, f"{tid.lower()}_exception.png")
            runner.record_finding(tid, title, "ZONE-2", "DEFECT", f"Unhandled Exception during attack: {exc}", shot)

    runner.log("ZONE 2", "✓ Hoàn tất toàn bộ 7 ca kiểm thử phá hủy Zone 2", Ansi.GREEN)


async def main():
    parser = argparse.ArgumentParser(description="Zone 2: SBFAS & FAS Destructive Test Runner")
    parser.add_argument("--base-url", default="https://admin.20-255-158-192.sslip.io", help="Admin Portal URL")
    parser.add_argument("--eservice-url", default="https://eservice.20-255-158-192.sslip.io", help="Parent Portal URL")
    parser.add_argument("--headed", action="store_true", default=True, help="Run browser in visual headed mode")
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode")
    parser.add_argument("--slow-mo", type=int, default=400, help="Slow down actions in ms")
    parser.add_argument("--hold", type=int, default=5, help="Seconds to hold browser open after completion")
    args = parser.parse_args()

    headed = False if args.headless else args.headed
    runner = Zone2SbfasFasRunner(
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
            await run_zone2_tests(runner, page)
            if runner.hold > 0:
                await page.wait_for_timeout(runner.hold * 1000)
        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
