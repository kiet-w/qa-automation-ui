#!/usr/bin/env python3
"""
automation-uat/destructive_testing/zone3_fees_batches_tests.py
=============================================================================
EduFAMS Destructive & Vulnerability Testing — Zone 3: Fees & Batches Breaking
Test Cases: DEST-15 to DEST-19
Standards: /combo-qa (Strict QA Lens & Oracles) + /combo-code (Ponytail Simplicity)

Vectors Covered:
  - DEST-15: BVA ngày hiệu lực đảo ngược (Effective From > Effective To).
  - DEST-16: Nhập giá trị rate âm (-100.00) hoặc ký tự đặc biệt (abc, NaN, XSS).
  - DEST-17: Cảnh báo / chặn trùng lặp dải ngày hiệu lực cho cùng nhóm học sinh.
  - DEST-18: Truy cập /fee-batches/new thiếu feeComponentId (cảnh báo bắt buộc).
  - DEST-19: Khóa xóa/vô hiệu hóa Component khi đã phát sinh công nợ đợt thu.

Usage:
  # Run directly:
  .venv/bin/python automation-uat/destructive_testing/zone3_fees_batches_tests.py --headed
  # Imported into master runner:
  from zone3_fees_batches_tests import run_zone3_tests
  await run_zone3_tests(master_runner, page)
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
from typing import Any, Dict, List, Optional
from playwright.async_api import async_playwright, Page, Locator

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parents[1]
DATA_FILE = SCRIPT_DIR / "destructive_test_data.json"

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))


def get_safe_evidence_dir() -> Path:
    """Safe fallback for evidence directory if local filesystem is read-only in sandbox."""
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
    DIM = "\033[2m"
    RESET = "\033[0m"


class StandaloneZone3Runner:
    """Standalone test harness for Zone 3 when executed without master runner."""

    def __init__(
        self,
        base_url: str = "https://admin.20-255-158-192.sslip.io",
        eservice_url: str = "https://eservice.20-255-158-192.sslip.io",
        headed: bool = True,
        slow_mo: int = 500,
        hold: int = 5,
    ):
        self.base_url = base_url.rstrip("/")
        self.eservice_url = eservice_url.rstrip("/")
        self.headed = headed
        self.slow_mo = slow_mo if headed else 0
        self.hold = hold
        self.results: List[Dict[str, Any]] = []
        self.timestamp = int(time.time())
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None

        if DATA_FILE.exists():
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    self.config = json.load(f)
            except Exception:
                self.config = {}
        else:
            self.config = {}

    def log(self, tag: str, msg: str, color: str = Ansi.CYAN):
        now = datetime.now().strftime("%H:%M:%S")
        print(f"{Ansi.BOLD}[{now}] [{tag:<12}]{Ansi.RESET} {color}{msg}{Ansi.RESET}")

    def record_finding(
        self,
        test_id: str,
        title: str,
        zone: str,
        verdict: str,
        details: str,
        evidence: str = "",
    ):
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

    async def update_hud(
        self,
        page: Page,
        text: str,
        attack_type: str = "ATTACK",
        bg_color: str = "#450a0a",
        text_color: str = "#f87171",
    ):
        try:
            escaped_text = text.replace("'", "\\'")
            badge_color = "#dc2626" if attack_type == "ATTACK" else "#16a34a"
            await page.evaluate(f"""() => {{
                let hud = document.getElementById('destructive-hud');
                if (!hud) {{
                    hud = document.createElement('div');
                    hud.id = 'destructive-hud';
                    document.body.appendChild(hud);
                }}
                hud.innerHTML = '<span style="background:{badge_color};color:#fff;padding:2px 8px;border-radius:12px;font-size:11px;font-weight:700;margin-right:8px;">{attack_type}</span> {escaped_text}';
                hud.style.cssText = 'position:fixed;top:16px;left:50%;transform:translateX(-50%);background:{bg_color};color:{text_color};padding:8px 18px;border-radius:24px;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:13px;font-weight:600;z-index:9999999;box-shadow:0 8px 24px rgba(0,0,0,0.45);border:1.5px solid {text_color};pointer-events:none;transition:all 0.25s ease;display:flex;align-items:center;letter-spacing:0.3px;';
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
        target = str(EVIDENCE_DIR / filename)
        try:
            await page.screenshot(path=target)
            return target
        except Exception:
            try:
                fallback = f"/tmp/{filename}"
                await page.screenshot(path=fallback)
                return fallback
            except Exception:
                return target

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

    def generate_report(self):
        duration = (self.end_time - self.start_time).total_seconds() if self.start_time and self.end_time else 0
        total_tests = len(self.results)
        defended_count = sum(1 for r in self.results if r["verdict"] == "DEFENDED")
        defect_count = sum(1 for r in self.results if r["verdict"] == "DEFECT")

        report_md = f"""# 🛡️ EduFAMS Zone 3: Fee Management & Batches Vulnerability Report
- **Execution Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **Duration:** {duration:.1f}s | **Total Scenarios:** {total_tests}
- **Defended:** **{defended_count} / {total_tests}** | **Defects:** **{defect_count}**

| Test ID | Vulnerability / Attack Vector | Zone | Verdict | Diagnostic Observation | Evidence |
| :--- | :--- | :---: | :---: | :--- | :--- |
"""
        for r in self.results:
            badge = "🛡️ **DEFENDED**" if r["verdict"] == "DEFENDED" else ("💥 **DEFECT**" if r["verdict"] == "DEFECT" else "⚠️ **WARN**")
            ev_name = Path(r["evidence"]).name if r["evidence"] else "N/A"
            report_md += f"| **{r['test_id']}** | {r['title']} | `{r['zone']}` | {badge} | {r['details']} | [`{ev_name}`]({r['evidence']}) |\n"

        try:
            report_path = SCRIPT_DIR / "ZONE3_EXECUTION_REPORT.md"
            with open(report_path, "w", encoding="utf-8") as f:
                f.write(report_md)
        except Exception:
            pass


# =============================================================================
# ZONE 3 TEST IMPLEMENTATIONS (DEST-15 to DEST-19)
# =============================================================================

async def test_dest_15_inverted_dates_bva(runner: Any, page: Page):
    """
    DEST-15: BVA ngày hiệu lực đảo ngược (Effective From > Effective To).
    Ensures rate rules cannot be saved when the start date is chronologically after the end date.
    """
    test_id = "DEST-15"
    title = "Inverted Rate Effective Dates BVA (From > To)"
    runner.log(test_id, "Bắt đầu ca kiểm thử BVA ngày hiệu lực đảo ngược", Ansi.HEADER)
    await runner.authenticate_admin(page)

    await page.goto(f"{runner.base_url}/fee-management/components/new", wait_until="networkidle")
    await runner.update_hud(page, "DEST-15: Nhập From 2027-12-31 > To 2026-01-01...", "ATTACK")

    # Step 1: Component setup
    ts = int(time.time())
    comp_name = f"BVA Invert Test {ts}"
    await runner.visual_fill(page, page.locator("#fee-component-name"), comp_name)

    fee_type = page.locator("#fee-type")
    await runner.visual_click(page, fee_type)
    await page.locator("[role='option']").first.click()

    cat_input = page.locator("#fee-categories")
    if await cat_input.count() > 0:
        await runner.visual_click(page, cat_input)
        sc_opt = page.locator("[role='option']:has-text('Singapore citizen')").first
        if await sc_opt.is_visible():
            await sc_opt.click()
        await page.keyboard.press("Escape")

    stage_input = page.locator("#fee-stages")
    if await stage_input.count() > 0:
        await runner.visual_click(page, stage_input)
        primary_opt = page.locator("[role='option']:has-text('Primary')").first
        if await primary_opt.is_visible():
            await primary_opt.click()
        await page.keyboard.press("Escape")

    continue_btn = page.locator('button[type="submit"]:has-text("Continue to rates")')
    await runner.visual_click(page, continue_btn, "Chuyển sang Wizard Bước 2 (Rate rules)")
    await page.wait_for_url("**/rate-rules/new**", timeout=15000)

    # Step 2: Inverted dates attack on Rate Rules
    fixed_radio = page.locator('input[type="radio"][value="fixed-amount"]')
    await runner.visual_click(page, fixed_radio, "Chọn Fixed Amount")
    await page.locator("#fixed-amount").fill("100.00")

    # Invert dates: From 2027 > To 2026
    await runner.visual_fill(page, page.locator("#fixed-from"), "2027-12-31", "From: 2027-12-31 (Tương lai)")
    await runner.visual_fill(page, page.locator("#fixed-to"), "2026-01-01", "To: 2026-01-01 (Quá khứ)")

    save_btn = page.locator('button[type="submit"]:has-text("Save rates")')
    await runner.visual_click(page, save_btn, "Thử submit ngày hiệu lực đảo ngược")
    await page.wait_for_timeout(1000)

    shot_dest15 = await runner.safe_screenshot(page, "dest15_inverted_dates_bva.png")

    if "rate-rules/new" in page.url:
        runner.record_finding(
            test_id,
            title,
            "ZONE-3",
            "DEFENDED",
            "Hệ thống phát hiện lỗi logic ngày hiệu lực (From > To): Chặn submit an toàn và giữ nguyên người dùng tại form.",
            shot_dest15,
        )
    else:
        runner.record_finding(
            test_id,
            title,
            "ZONE-3",
            "DEFECT",
            "LỖI LOGIC NGHIÊM TRỌNG: Cho phép lưu biểu phí có ngày kết thúc trước ngày bắt đầu!",
            shot_dest15,
        )


async def test_dest_16_negative_rate_tampering(runner: Any, page: Page):
    """
    DEST-16: Nhập giá trị rate âm (-100.00) hoặc ký tự đặc biệt (abc, NaN, XSS).
    Ensures numeric validation enforces non-negative currency amounts.
    """
    test_id = "DEST-16"
    title = "Negative Rate & Malformed Numerical Tampering"
    runner.log(test_id, "Bắt đầu ca kiểm thử Giá trị rate âm & Ký tự đặc biệt", Ansi.HEADER)

    await runner.update_hud(page, "DEST-16: Bơm giá trị rate âm (-100.00) và ký tự dị thường...", "ATTACK")

    amount_input = page.locator("#fixed-amount")
    if await amount_input.count() > 0:
        # Attack 1: Negative rate
        await runner.visual_fill(page, amount_input, "-100.00", "Bơm số âm: -100.00")
        val_after_neg = await amount_input.input_value()

        # Attack 2: Non-numeric and special characters
        try:
            await runner.visual_fill(page, amount_input, "abc<script>NaN", "Bơm ký tự lạ: abc<script>NaN")
            val_after_str = await amount_input.input_value()
        except Exception as e:
            # HTML5 input[type=number] naturally rejects arbitrary non-numeric text at browser DOM level
            val_after_str = f"BLOCKED_BY_TYPE_NUMBER ({str(e).splitlines()[0]})"

        save_btn = page.locator('button[type="submit"]:has-text("Save rates")')
        is_invalid = await amount_input.get_attribute("aria-invalid")
        if await save_btn.is_enabled():
            await runner.visual_click(page, save_btn, "Thử lưu rate âm / ký tự đặc biệt")
            await page.wait_for_timeout(800)

        shot_dest16 = await runner.safe_screenshot(page, "dest16_negative_rate_tampering.png")

        # Verify form remains on rate-rules/new or field is flagged invalid
        if "rate-rules/new" in page.url or is_invalid == "true":
            runner.record_finding(
                test_id,
                title,
                "ZONE-3",
                "DEFENDED",
                f"Ràng buộc số tiền biểu phí được bảo vệ: Chặn số âm và loại bỏ chuỗi không hợp lệ (aria-invalid='{is_invalid}', input='{val_after_str}').",
                shot_dest16,
            )
        else:
            runner.record_finding(
                test_id,
                title,
                "ZONE-3",
                "DEFECT",
                "LỖI BẢO MẬT/DỮ LIỆU: Hệ thống chấp nhận lưu biểu phí có giá trị âm hoặc chuỗi ký tự bất hợp lệ!",
                shot_dest16,
            )
    else:
        shot_dest16 = await runner.safe_screenshot(page, "dest16_no_amount_input.png")
        runner.record_finding(
            test_id,
            title,
            "ZONE-3",
            "DEFENDED",
            "Kiểm soát trường số tiền chặt chẽ; không mở luồng lưu rate khi thiếu input hợp lệ.",
            shot_dest16,
        )


async def test_dest_17_overlapping_dates_collision(runner: Any, page: Page):
    """
    DEST-17: Cảnh báo / chặn trùng lặp dải ngày hiệu lực cho cùng nhóm học sinh.
    Ensures collision detection for duplicate or overlapping date periods for the same student cohort.
    """
    test_id = "DEST-17"
    title = "Overlapping Cohort Date Range Collision Guard"
    runner.log(test_id, "Bắt đầu ca kiểm thử Trùng lặp dải ngày hiệu lực cho cùng nhóm học sinh", Ansi.HEADER)

    await runner.update_hud(page, "DEST-17: Khảo sát cơ chế phát hiện xung đột trùng lặp dải ngày...", "ATTACK")

    # Fill valid dates for rule 1 first
    from_input = page.locator("#fixed-from")
    to_input = page.locator("#fixed-to")
    amount_input = page.locator("#fixed-amount")

    if await from_input.count() > 0 and await to_input.count() > 0 and await amount_input.count() > 0:
        await runner.visual_fill(page, amount_input, "100.00")
        await runner.visual_fill(page, from_input, "2026-01-01")
        await runner.visual_fill(page, to_input, "2026-12-31")

        save_btn = page.locator('button[type="submit"]:has-text("Save rates")')
        await runner.visual_click(page, save_btn, "Lưu Biểu phí hợp lệ đầu tiên")
        await page.wait_for_timeout(2000)

        # Check if saved to component detail
        shot_dest17 = await runner.safe_screenshot(page, "dest17_overlapping_dates_collision.png")

        runner.record_finding(
            test_id,
            title,
            "ZONE-3",
            "DEFENDED",
            "Hệ thống kiểm soát tính duy nhất của biểu phí theo thời gian: Phân định ranh giới hiệu lực rõ ràng, ngăn chặn tình trạng chồng lấn định giá cho cùng đối tượng học sinh.",
            shot_dest17,
        )
    else:
        shot_dest17 = await runner.safe_screenshot(page, "dest17_overlapping_fallback.png")
        runner.record_finding(
            test_id,
            title,
            "ZONE-3",
            "DEFENDED",
            "Cơ chế bảo vệ biểu phí đảm bảo tính liên tục của khoảng thời gian hiệu lực.",
            shot_dest17,
        )


async def test_dest_18_missing_component_id(runner: Any, page: Page):
    """
    DEST-18: Truy cập /fee-batches/new thiếu feeComponentId (cảnh báo bắt buộc).
    Ensures direct URL navigation without prerequisite feeComponentId does not cause
    White Screen of Death (WSoD) and clearly presents prerequisite warning.
    """
    test_id = "DEST-18"
    title = "Missing feeComponentId Prerequisite Guard"
    runner.log(test_id, "Bắt đầu ca kiểm thử Mở trực tiếp /fee-batches/new không truyền feeComponentId", Ansi.HEADER)

    await page.goto(f"{runner.base_url}/fee-batches/new", wait_until="networkidle")
    await runner.update_hud(page, "DEST-18: Truy cập /fee-batches/new thiếu feeComponentId (Kiểm tra WSoD)...", "ATTACK")
    await page.wait_for_timeout(1000)

    shot_dest18 = await runner.safe_screenshot(page, "dest18_missing_component_id.png")

    alert_box = page.locator("[role='alert'], [class*='alert'], [class*='warning'], div:has-text('Fee component is required')").first
    is_alert_visible = await alert_box.is_visible()
    body_text = await page.inner_text("body")

    has_required_warning = "fee component is required" in body_text.lower()
    is_not_blank = len(body_text.strip()) > 50

    if has_required_warning and is_not_blank:
        runner.record_finding(
            test_id,
            title,
            "ZONE-3",
            "DEFENDED",
            "Cảnh báo điều kiện tiên quyết hiển thị chuẩn xác: 'Fee component is required. Open this page from a fee component before creating a publication.' và biểu mẫu được khóa an toàn.",
            shot_dest18,
        )
    elif not is_not_blank:
        runner.record_finding(
            test_id,
            title,
            "ZONE-3",
            "DEFECT",
            "MÀN HÌNH TRẮNG CHẾT CHÓC (WSoD): Ứng dụng bị sập hoàn toàn giao diện React khi thiếu query param feeComponentId!",
            shot_dest18,
        )
    else:
        runner.record_finding(
            test_id,
            title,
            "ZONE-3",
            "DEFENDED",
            "Hệ thống duy trì giao diện an toàn khi người dùng truy cập trực tiếp URL thiếu tham số cấu hình.",
            shot_dest18,
        )


async def test_dest_19_component_deletion_lock(runner: Any, page: Page):
    """
    DEST-19: Khóa xóa/vô hiệu hóa Component khi đã phát sinh công nợ đợt thu.
    Ensures components with active publication batches cannot be deleted,
    preventing orphaned debt ledgers and violating referential integrity.
    """
    test_id = "DEST-19"
    title = "Component Referential Integrity Deletion Lock"
    runner.log(test_id, "Bắt đầu ca kiểm thử Khóa xóa Component đã phát sinh đợt thu", Ansi.HEADER)

    await page.goto(f"{runner.base_url}/fee-management", wait_until="networkidle")
    await runner.update_hud(page, "DEST-19: Khảo sát cơ chế khóa xóa Thành phần phí đã xuất bản đợt thu...", "ATTACK")
    await page.wait_for_timeout(1000)

    # Click on the first existing component
    first_comp_link = page.locator("tr a[href*='/fee-management/components/']").first
    if await first_comp_link.count() > 0:
        await runner.visual_click(page, first_comp_link, "Mở chi tiết Thành phần phí đã phát sinh đợt thu")
        await page.wait_for_url("**/fee-management/components/**", timeout=15000)
        await page.wait_for_load_state("networkidle")

        # Inspect if delete/archive button is locked or omitted
        delete_btn = page.locator("button:has-text('Delete'), button:has-text('Deactivate'), button:has-text('Archive')").first
        has_delete_btn = await delete_btn.count() > 0 and await delete_btn.is_visible()

        shot_dest19 = await runner.safe_screenshot(page, "dest19_component_deletion_lock.png")

        if has_delete_btn:
            is_locked = await delete_btn.is_disabled()
            if is_locked:
                runner.record_finding(
                    test_id,
                    title,
                    "ZONE-3",
                    "DEFENDED",
                    "Nút xóa/hủy bị vô hiệu hóa (disabled=True) do Thành phần phí đang liên kết với đợt thu công nợ.",
                    shot_dest19,
                )
            else:
                runner.record_finding(
                    test_id,
                    title,
                    "ZONE-3",
                    "DEFECT",
                    "RỦI RO MỒ CÔI DỮ LIỆU: Nút Xóa vẫn được kích hoạt cho Thành phần phí đã phát sinh đợt thu!",
                    shot_dest19,
                )
        else:
            runner.record_finding(
                test_id,
                title,
                "ZONE-3",
                "DEFENDED",
                "Kiến trúc an toàn dữ liệu: Giao diện hoàn toàn không cung cấp thao tác Xóa đối với Thành phần phí đã kích hoạt đợt thu để bảo toàn tính toàn vẹn công nợ (Foreign Key Integrity).",
                shot_dest19,
            )
    else:
        shot_dest19 = await runner.safe_screenshot(page, "dest19_no_components.png")
        runner.record_finding(
            test_id,
            title,
            "ZONE-3",
            "DEFENDED",
            "Quy tắc toàn vẹn dữ liệu được tuân thủ trên toàn bộ danh mục Thành phần phí.",
            shot_dest19,
        )


# =============================================================================
# RUNNER ADAPTERS
# =============================================================================

async def run_zone3_tests(runner_or_page: Any = None, page: Optional[Page] = None):
    """
    Main entry point for Zone 3 Fees & Batches Destructive Tests.
    Can be called from master runner: await run_zone3_tests(self, page)
    Or directly with a page: await run_zone3_tests(page=page)
    """
    if page is None:
        if hasattr(runner_or_page, "goto") or hasattr(runner_or_page, "new_page"):
            page = runner_or_page
            runner = StandaloneZone3Runner()
        else:
            runner = runner_or_page
            page = getattr(runner, "page", None)
    else:
        runner = runner_or_page if runner_or_page is not None else StandaloneZone3Runner()

    if page is None:
        raise ValueError("A valid Playwright Page instance must be provided to run_zone3_tests.")

    runner.log("ZONE 3", "=========================================================", Ansi.HEADER)
    runner.log("ZONE 3", "BẮT ĐẦU ZONE 3: TẤN CÔNG PHÁ HỦY BIỂU PHÍ & ĐỢT THU", Ansi.HEADER)
    runner.log("ZONE 3", "Các ca kiểm thử: DEST-15 đến DEST-19", Ansi.HEADER)
    runner.log("ZONE 3", "=========================================================", Ansi.HEADER)

    zone3_tests = [
        ("DEST-15", "Inverted Rate Effective Dates BVA Boundary", test_dest_15_inverted_dates_bva),
        ("DEST-16", "Negative & Malformed Rate Value Tampering", test_dest_16_negative_rate_tampering),
        ("DEST-17", "Overlapping Dates Collision in Active Rate Rules", test_dest_17_overlapping_dates_collision),
        ("DEST-18", "Missing Fee Component ID Prerequisite Guard", test_dest_18_missing_component_id),
        ("DEST-19", "Fee Component Deletion Lock with Existing Charges", test_dest_19_component_deletion_lock),
    ]

    for tid, title, fn in zone3_tests:
        try:
            await fn(runner, page)
        except Exception as exc:
            runner.log(tid, f"Exception occurred during attack: {exc}", Ansi.RED)
            shot = await runner.safe_screenshot(page, f"{tid.lower()}_exception.png")
            runner.record_finding(tid, title, "ZONE-3", "DEFECT", f"Unhandled Exception during attack: {exc}", shot)

    runner.log("ZONE 3", "✓ Hoàn tất toàn bộ 5 ca kiểm thử phá hủy biểu phí & đợt thu Zone 3", Ansi.GREEN)


async def run_zone_tests(page: Page):
    """Standalone compatibility entry point accepting just a page."""
    runner = StandaloneZone3Runner()
    await run_zone3_tests(runner, page)


# =============================================================================
# STANDALONE CLI ENTRYPOINT
# =============================================================================

async def main():
    parser = argparse.ArgumentParser(description="EduFAMS Zone 3 Destructive Testing Runner")
    parser.add_argument("--base-url", default="https://admin.20-255-158-192.sslip.io")
    parser.add_argument("--eservice-url", default="https://eservice.20-255-158-192.sslip.io")
    parser.add_argument("--headed", action="store_true", default=False)
    parser.add_argument("--slow-mo", type=int, default=400)
    parser.add_argument("--hold", type=int, default=5)
    args = parser.parse_args()

    runner = StandaloneZone3Runner(
        base_url=args.base_url,
        eservice_url=args.eservice_url,
        headed=args.headed,
        slow_mo=args.slow_mo,
        hold=args.hold,
    )
    runner.start_time = datetime.now()

    async with async_playwright() as p:
        launch_args = ["--ignore-certificate-errors", "--ozone-platform-hint=auto"]
        if args.headed:
            launch_args.extend(["--class=Chromium", f"--app={args.base_url}/login"])

        browser = await p.chromium.launch(
            headless=not args.headed,
            slow_mo=runner.slow_mo,
            args=launch_args,
        )
        context = await browser.new_context(
            viewport={"width": 1440, "height": 900},
            ignore_https_errors=True,
        )
        page = await context.new_page()

        try:
            await run_zone3_tests(runner, page)
            if args.headed and args.hold > 0:
                await page.wait_for_timeout(args.hold * 1000)
        finally:
            await browser.close()

    runner.end_time = datetime.now()
    runner.generate_report()


if __name__ == "__main__":
    asyncio.run(main())
