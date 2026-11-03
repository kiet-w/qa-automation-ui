#!/usr/bin/env python3
"""
Detailed verification of 3 dev fixes with precise timing and logging.
"""

import asyncio
import re
from pathlib import Path
from playwright.async_api import async_playwright, Page

BASE_URL = "https://admin.20-255-158-192.sslip.io"
OUT_DIR = Path("/tmp/retest_dev_detailed")
OUT_DIR.mkdir(parents=True, exist_ok=True)


async def test_all_3_fixes():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
        context = await browser.new_context(viewport={"width": 1440, "height": 900}, ignore_https_errors=True)
        page = await context.new_page()

        # =====================================================================
        # 1. VERIFY BUG-03: RATE RULES DATE INPUT CONSTRAINT
        # =====================================================================
        print("\n================== [1/3] VERIFYING BUG-03 (DATE 5-DIGIT YEAR) ==================")
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

        await page.goto(f"{BASE_URL}/fee-management/components/new", wait_until="networkidle")
        await page.locator("#fee-component-name").fill("Dev Retest Date Comp")
        await page.locator("#fee-type").click()
        await page.locator('[role="option"]').first.click()
        await page.locator("#fee-categories").click()
        await page.locator('[role="option"]').first.click()
        await page.keyboard.press("Escape")
        await page.locator("#fee-stages").click()
        await page.locator('[role="option"]').first.click()
        await page.keyboard.press("Escape")
        await page.locator('button[type="submit"]:has-text("Continue to rates")').click()
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(1000)

        # Select fixed amount
        fixed_radio = page.locator('input[value="fixed-amount"]')
        if await fixed_radio.count() > 0:
            await fixed_radio.click()
            await page.wait_for_timeout(300)

        date_input = page.locator("#fixed-from")
        min_v = await date_input.get_attribute("min")
        max_v = await date_input.get_attribute("max")
        print(f"BUG-03 DOM Attributes: min='{min_v}', max='{max_v}'")

        # Fill 20266
        await date_input.fill("20266-05-15")
        validity = await date_input.evaluate("el => el.checkValidity()")
        val_msg = await date_input.evaluate("el => el.validationMessage")
        print(f"BUG-03 checkValidity()={validity}, validationMessage='{val_msg}'")

        await page.locator("#fixed-amount").fill("100.00")
        save_btn = page.locator('button[type="submit"]:has-text("Save rates")')
        await save_btn.click()
        await page.wait_for_timeout(1000)
        url_after_save = page.url
        print(f"BUG-03 URL after save click: {url_after_save}")
        is_blocked = "rate-rules/new" in url_after_save and not validity
        print(f"BUG-03 RESULT: {'FIXED (PASS)' if is_blocked else 'NOT FIXED'}")
        await page.screenshot(path=str(OUT_DIR / "bug03_fixed_evidence.png"))

        # =====================================================================
        # 2. VERIFY BUG-02: VIEW AS EXIT BUTTON ON SUBPAGES
        # =====================================================================
        print("\n================== [2/3] VERIFYING BUG-02 (VIEW AS EXIT BUTTON) ================")
        await page.goto(f"{BASE_URL}/support-console", wait_until="networkidle")
        user_tab = page.get_by_role("tab", name=re.compile(r"School users", re.I))
        if await user_tab.count() > 0:
            await user_tab.click()
            await page.wait_for_timeout(600)
            search_input = page.locator('input[placeholder*="search" i]').first
            if await search_input.count() > 0:
                await search_input.fill("staff1")
                await page.locator("button:has-text('Search')").first.click()
                await page.wait_for_timeout(800)

            select_btn = page.locator('tr:has-text("staff1") button:has-text("Select"), button:has-text("Select")').first
            if await select_btn.count() > 0:
                await select_btn.click()
                await page.wait_for_timeout(800)

        reason_area = page.locator("textarea").or_(page.get_by_label("Reason", exact=False)).first
        await reason_area.wait_for(state="visible", timeout=10000)
        await reason_area.fill("Verifying View As Exit Button On Subpages")
        ticket_input = page.locator("input[placeholder*='ticket' i]").or_(page.get_by_label("Ticket", exact=False)).first
        if await ticket_input.count() > 0:
            await ticket_input.fill("UAT-VERIFY-EXIT")

        start_btn = page.get_by_role("button", name=re.compile(r"Start View As", re.I)).first
        await start_btn.click()
        await page.wait_for_timeout(3000)
        await page.wait_for_load_state("networkidle")
        print(f"View As started. Current URL: {page.url}")

        # Check for View As banner
        top_banner = page.locator("header, nav, [class*='banner' i], [class*='impersonat' i]").filter(has_text=re.compile(r"viewing as", re.I))
        print("Banner visible on Home:", await top_banner.count() > 0)

        # Navigate to /class-management
        await page.goto(f"{BASE_URL}/class-management", wait_until="networkidle")
        await page.wait_for_timeout(1500)
        print("Navigated to /class-management")

        exit_btn = page.locator("button:has-text('Exit')")
        exit_count = await exit_btn.count()
        exit_visible = False
        if exit_count > 0:
            exit_visible = await exit_btn.first.is_visible()

        print(f"On /class-management: Exit button count={exit_count}, is_visible={exit_visible}")
        await page.screenshot(path=str(OUT_DIR / "bug02_class_management_banner.png"))

        if exit_visible:
            await exit_btn.first.click()
            await page.wait_for_timeout(2000)
            await page.wait_for_load_state("networkidle")
            body_txt = await page.locator("body").inner_text()
            still_impersonating = "viewing as" in body_txt.lower()
            print(f"After clicking Exit: still_impersonating={still_impersonating}")
            print(f"BUG-02 RESULT: {'FIXED (PASS)' if not still_impersonating else 'NOT FIXED'}")
        else:
            print("BUG-02 RESULT: NOT FIXED (Exit button missing on /class-management)")

        # =====================================================================
        # 3. VERIFY BUG-01: SBFAS BUDGET NEGATIVE & CAP
        # =====================================================================
        print("\n================== [3/3] VERIFYING BUG-01 (SBFAS BUDGET CAP) ==================")
        await page.context.clear_cookies()
        await page.goto(f"{BASE_URL}/login", wait_until="networkidle")
        ms_btn = page.locator('button:has-text("Sign in with Microsoft")')
        if await ms_btn.is_visible():
            await ms_btn.click()
            await page.wait_for_url("**/microsoft-provider/**", timeout=25000)
        staff_tile = page.locator(".account-tile:has-text('staff1@IAM.edu.vn')").first
        await staff_tile.wait_for(state="visible", timeout=15000)
        await staff_tile.click()
        await page.wait_for_url(f"{BASE_URL}/**", timeout=30000)
        await page.wait_for_load_state("networkidle")

        await page.goto(f"{BASE_URL}/sbfas-schemes/new", wait_until="networkidle")
        await page.locator("#sbfas-name").fill("Dev Retest Scheme")
        await page.locator("#sbfas-open-from").fill("2026-11-01")
        await page.locator("#sbfas-open-to").fill("2026-11-30")
        await page.locator("#sbfas-effective-from").fill("2026-12-01")

        budget_el = page.locator("#sbfas-budget")
        b_min = await budget_el.get_attribute("min")
        b_max = await budget_el.get_attribute("max")
        print(f"BUG-01 SBFAS budget attributes: min='{b_min}', max='{b_max}'")

        # Test entering -50000
        await budget_el.fill("-50000")
        next_btn = page.locator("button:has-text('Next')")
        await next_btn.click()
        await page.wait_for_timeout(1000)

        # Check if it stayed on Step 1 (blocked) or went to Step 2
        step1_active = await page.locator("#sbfas-name").is_visible()
        step2_active = await page.locator("text=/income bands/i").count() > 0
        print(f"After filling -50000 and clicking Next: step1_active={step1_active}, step2_active={step2_active}")

        await page.screenshot(path=str(OUT_DIR / "bug01_sbfas_step1_retest.png"))

        await browser.close()


if __name__ == "__main__":
    asyncio.run(test_all_3_fixes())
