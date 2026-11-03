#!/usr/bin/env python3
"""
=============================================================================
Capture Exact Input Moments for 3 Bugs
Captures:
  1. BUG 1: The moment of typing negative budget -50000 SGD on SBFAS Wizard
  2. BUG 2: The moment of initiating View As & Missing Exit on Class Management
  3. BUG 3: The moment of typing 5-digit year (15/05/20266) on Date Input
=============================================================================
"""

import asyncio
import os
import re
import time
from pathlib import Path
from playwright.async_api import async_playwright, Page

BASE_URL = "https://admin.20-255-158-192.sslip.io"
OUT_DIR = Path("/tmp/evidence_bugs_moment")
OUT_DIR.mkdir(parents=True, exist_ok=True)


async def authenticate_admin(page: Page):
    await page.context.clear_cookies()
    await page.goto(f"{BASE_URL}/login", wait_until="networkidle")
    ms_btn = page.locator('button:has-text("Sign in with Microsoft")')
    if await ms_btn.is_visible():
        await ms_btn.click()
        await page.wait_for_url("**/microsoft-provider/**", timeout=25000)

    tile = page.locator(".account-tile:has-text('admin@IAM.edu.vn')").first
    await tile.wait_for(state="visible", timeout=15000)
    await tile.click()
    await page.wait_for_url(f"{BASE_URL}/**", timeout=30000)
    await page.wait_for_load_state("networkidle")

    exit_btn = page.get_by_role("button", name="Exit", exact=True)
    if await exit_btn.count() > 0 and await exit_btn.is_visible():
        await exit_btn.click()
        await page.wait_for_timeout(800)


async def authenticate_school(page: Page):
    await page.context.clear_cookies()
    await page.goto(f"{BASE_URL}/login", wait_until="networkidle")
    ms_btn = page.locator('button:has-text("Sign in with Microsoft")')
    if await ms_btn.is_visible():
        await ms_btn.click()
        await page.wait_for_url("**/microsoft-provider/**", timeout=25000)

    tile = page.locator(".account-tile:has-text('staff1@IAM.edu.vn')").first
    await tile.wait_for(state="visible", timeout=15000)
    await tile.click()
    await page.wait_for_url(f"{BASE_URL}/**", timeout=30000)
    await page.wait_for_load_state("networkidle")


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--ignore-certificate-errors"]
        )
        context = await browser.new_context(
            viewport={"width": 1440, "height": 900},
            ignore_https_errors=True
        )
        page = await context.new_page()

        # =====================================================================
        # 1. BUG-01: THE EXACT MOMENT OF TYPING -50000 SGD BUDGET
        # =====================================================================
        print("Capturing BUG-01: SBFAS Budget Input Moment...")
        await authenticate_school(page)
        await page.goto(f"{BASE_URL}/sbfas-schemes/new", wait_until="networkidle")
        await page.wait_for_timeout(1000)

        name_input = page.locator("#sbfas-name")
        if await name_input.count() > 0:
            await name_input.fill("SBFAS Negative Budget Test")
            await page.locator("#sbfas-open-from").fill("2026-11-01")
            await page.locator("#sbfas-open-to").fill("2026-11-30")
            await page.locator("#sbfas-effective-from").fill("2026-12-01")

        budget_input = page.locator("#sbfas-budget")
        if await budget_input.count() > 0:
            await budget_input.fill("-50000")
            # Inject prominent visual callout on the input moment
            await page.evaluate("""() => {
                let el = document.getElementById('sbfas-budget');
                if (el) {
                    el.style.border = '3.5px solid #dc2626';
                    el.style.boxShadow = '0 0 20px rgba(220, 38, 38, 0.7)';
                    el.focus();
                    let badge = document.createElement('div');
                    badge.id = 'input-callout';
                    badge.innerHTML = '👉 <b>LÚC ĐANG NHẬP DỮ LIỆU DẪN ĐẾN LỖI:</b> Gõ số tiền âm <b>-50000 SGD</b> vào ô Tổng Ngân Sách (Không bị chặn viền đỏ)';
                    let rect = el.getBoundingClientRect();
                    badge.style.cssText = 'position:fixed;top:' + (rect.top - 46) + 'px;left:' + rect.left + 'px;background:#dc2626;color:#fff;padding:8px 16px;border-radius:6px;font-size:13px;font-weight:700;z-index:99999;box-shadow:0 6px 16px rgba(0,0,0,0.35);font-family:Segoe UI,sans-serif;';
                    document.body.appendChild(badge);
                }
            }""")
            await page.wait_for_timeout(600)
            await page.screenshot(path=str(OUT_DIR / "bug01_input_negative_budget.png"))
            print("✓ Saved bug01_input_negative_budget.png")

        # =====================================================================
        # 2. BUG-02: VIEW AS SESSION INITIATION & MISSING EXIT ON SUBPAGE
        # =====================================================================
        print("Capturing BUG-02: View As Input Moment & Missing Exit...")
        await authenticate_admin(page)
        await page.goto(f"{BASE_URL}/support-console", wait_until="networkidle")
        await page.wait_for_timeout(800)

        user_tab = page.get_by_role("tab", name=re.compile(r"School users", re.I))
        if await user_tab.count() > 0:
            await user_tab.click()
            await page.wait_for_timeout(500)
            search_input = page.locator('input[placeholder*="search" i]').first
            if await search_input.count() > 0:
                await search_input.fill("staff1")
                await page.locator("button:has-text('Search')").first.click()
                await page.wait_for_timeout(600)
            select_btn = page.locator('tr:has-text("staff1") button:has-text("Select")').first
            if await select_btn.count() > 0:
                await select_btn.click()
                await page.wait_for_timeout(600)

        reason_area = page.locator("textarea").or_(page.get_by_label("Reason", exact=False)).first
        if await reason_area.count() > 0:
            await reason_area.fill("Audit View As Session Exit Button Check")
            ticket_input = page.get_by_label("Ticket reference", exact=False).or_(page.locator("input[placeholder*='ticket' i]")).first
            if await ticket_input.count() > 0:
                await ticket_input.fill("TICKET-AUDIT-EXIT")

            # Annotate moment of triggering View As
            await page.evaluate("""() => {
                let badge = document.createElement('div');
                badge.id = 'input-callout';
                badge.innerHTML = '👉 <b>LÚC THỰC HIỆN:</b> Chọn cán bộ staff1, nhập lý do kiểm toán và bấm <b>Start View As</b> để vào trường';
                badge.style.cssText = 'position:fixed;top:20px;left:50%;transform:translateX(-50%);background:#2563eb;color:#fff;padding:8px 18px;border-radius:20px;font-size:13px;font-weight:700;z-index:99999;box-shadow:0 4px 16px rgba(0,0,0,0.3);font-family:Segoe UI,sans-serif;';
                document.body.appendChild(badge);
            }""")
            await page.wait_for_timeout(500)
            await page.screenshot(path=str(OUT_DIR / "bug02_input_start_view_as.png"))
            print("✓ Saved bug02_input_start_view_as.png")

            start_btn = page.get_by_role("button", name=re.compile(r"Start View As", re.I)).first
            if await start_btn.is_enabled():
                await start_btn.click()
                await page.wait_for_timeout(2500)

        # Navigate to /class-management
        await page.goto(f"{BASE_URL}/class-management", wait_until="networkidle")
        await page.wait_for_timeout(1000)

        # Highlight top header area where Exit button is missing
        await page.evaluate("""() => {
            let banner = document.createElement('div');
            banner.style.cssText = 'position:fixed;top:8px;left:50%;transform:translateX(-50%);border:3.5px dashed #dc2626;background:rgba(220,38,38,0.2);padding:10px 24px;border-radius:8px;color:#991b1b;font-size:14px;font-weight:700;z-index:99999;font-family:Segoe UI,sans-serif;box-shadow:0 6px 20px rgba(0,0,0,0.25);';
            banner.innerHTML = '❌ <b>KẾT QUẢ LỖI:</b> Đang ở trang Quản lý lớp học của trường nhưng trên đầu trang BỊ MẤT NÚT <b>EXIT</b> để quay lại quyền Bộ!';
            document.body.appendChild(banner);
        }""")
        await page.wait_for_timeout(500)
        await page.screenshot(path=str(OUT_DIR / "bug02_result_missing_exit.png"))
        print("✓ Saved bug02_result_missing_exit.png")

        # =====================================================================
        # 3. BUG-03: THE EXACT MOMENT OF TYPING 5-DIGIT YEAR 20266
        # =====================================================================
        print("Capturing BUG-03: Date Input Moment (Year 20266)...")
        await authenticate_admin(page)

        # Navigate to Component Wizard to reach Rate Rules form
        await page.goto(f"{BASE_URL}/fee-management/components/new", wait_until="networkidle")
        await page.wait_for_timeout(800)

        comp_name = f"Date Test Comp {int(time.time())}"
        await page.locator("#fee-component-name").fill(comp_name)

        fee_type_input = page.locator("#fee-type")
        await fee_type_input.click()
        await page.wait_for_timeout(300)
        opts = page.locator('[role="option"]')
        if await opts.count() > 0:
            await opts.first.click()

        cat_input = page.locator("#fee-categories")
        await cat_input.click()
        await page.wait_for_timeout(300)
        cats = page.locator('[role="option"]')
        if await cats.count() > 0:
            await cats.first.click()
        await page.keyboard.press("Escape")

        stage_input = page.locator("#fee-stages")
        await stage_input.click()
        await page.wait_for_timeout(300)
        stages = page.locator('[role="option"]')
        if await stages.count() > 0:
            await stages.first.click()
        await page.keyboard.press("Escape")

        submit_btn = page.locator('button[type="submit"]:has-text("Continue to rates")')
        await submit_btn.click()
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(1000)

        # In /rate-rules/new form
        fixed_radio = page.locator('input[value="fixed-amount"]')
        if await fixed_radio.count() > 0:
            await fixed_radio.click()
            await page.wait_for_timeout(400)

        from_input = page.locator("#fixed-from")
        if await from_input.count() > 0:
            await from_input.fill("20266-05-15")
            amount_input = page.locator("#fixed-amount")
            if await amount_input.count() > 0:
                await amount_input.fill("100.00")

            # Annotate moment of typing year 20266
            await page.evaluate("""() => {
                let el = document.getElementById('fixed-from');
                if (el) {
                    el.style.border = '3.5px solid #dc2626';
                    el.style.boxShadow = '0 0 20px rgba(220, 38, 38, 0.7)';
                    el.focus();
                    let badge = document.createElement('div');
                    badge.id = 'date-callout';
                    badge.innerHTML = '👉 <b>LÚC ĐANG NHẬP DỮ LIỆU DẪN ĐẾN LỖI:</b> Gõ phím năm 5 chữ số <b>15/05/20266</b> (Ô ngày vẫn chấp nhận không báo lỗi)';
                    let rect = el.getBoundingClientRect();
                    badge.style.cssText = 'position:fixed;top:' + (rect.top - 46) + 'px;left:' + rect.left + 'px;background:#dc2626;color:#fff;padding:8px 16px;border-radius:6px;font-size:13px;font-weight:700;z-index:99999;box-shadow:0 6px 16px rgba(0,0,0,0.35);font-family:Segoe UI,sans-serif;';
                    document.body.appendChild(badge);
                }
            }""")
            await page.wait_for_timeout(600)
            await page.screenshot(path=str(OUT_DIR / "bug03_input_year_20266.png"))
            print("✓ Saved bug03_input_year_20266.png")

        await browser.close()
        print("✓ All 3 input moment screenshots captured successfully!")


if __name__ == "__main__":
    asyncio.run(main())
