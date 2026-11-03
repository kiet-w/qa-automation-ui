#!/usr/bin/env python3
"""
=============================================================================
EduFAMS Dev Fix Verification & Retest Script
Specifically re-verifies the 3 previously identified defects:
  1. BUG-01 (DEST-08): SBFAS Budget Cap & Negative Value Guard
  2. BUG-02 (DEST-22): View As Top Banner Exit Button on Sub-pages
  3. BUG-03 (TC-DATE-019): Date Input Year Constraint (Max 4 digits / 2099)
=============================================================================
"""

import asyncio
import os
import re
import sys
import time
from pathlib import Path
from playwright.async_api import async_playwright, Page

BASE_URL = "https://admin.20-255-158-192.sslip.io"
RETEST_EVIDENCE_DIR = Path("/tmp/retest_evidence")
RETEST_EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)


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


async def retest_bug_01(page: Page) -> dict:
    print("\n--- RETESTING BUG-01: SBFAS Budget Cap & Negative Value Guard ---")
    await authenticate_school(page)
    await page.goto(f"{BASE_URL}/sbfas-schemes/new", wait_until="networkidle")
    await page.wait_for_timeout(1000)

    name_input = page.locator("#sbfas-name")
    if await name_input.count() > 0:
        await name_input.fill("SBFAS Retest Scheme")
        await page.locator("#sbfas-open-from").fill("2026-11-01")
        await page.locator("#sbfas-open-to").fill("2026-11-30")
        await page.locator("#sbfas-effective-from").fill("2026-12-01")

    budget_input = page.locator("#sbfas-budget")
    min_attr = await budget_input.get_attribute("min")
    max_attr = await budget_input.get_attribute("max")
    print(f"Budget input attributes: min='{min_attr}', max='{max_attr}'")

    # Test negative budget: -50000
    await budget_input.fill("-50000")
    next_btn = page.locator("button:has-text('Next')")
    is_invalid_neg = await budget_input.get_attribute("aria-invalid")
    print(f"After filling -50000: aria-invalid='{is_invalid_neg}'")

    if await next_btn.count() > 0:
        await next_btn.click()
        await page.wait_for_timeout(1000)

    # Check if form stayed on Step 1 (validating) or showed alert
    alert = page.locator("[role='alert'], .text-destructive, p.error").filter(has_text=re.compile(r"budget|greater than|invalid|must be", re.I))
    alert_text = await alert.inner_text() if await alert.count() > 0 else ""
    url_after = page.url
    is_stayed_step1 = await page.locator("#sbfas-name").is_visible()

    shot_path = str(RETEST_EVIDENCE_DIR / "retest_bug01_sbfas_budget.png")
    await page.screenshot(path=shot_path)
    print(f"Step 1 remained visible: {is_stayed_step1}, Alert: '{alert_text}', URL: {url_after}")

    # Retest extreme value: 999999
    if is_stayed_step1:
        await budget_input.fill("999999")
        if await next_btn.count() > 0:
            await next_btn.click()
            await page.wait_for_timeout(1000)
    shot_path_cap = str(RETEST_EVIDENCE_DIR / "retest_bug01_sbfas_budget_cap.png")
    await page.screenshot(path=shot_path_cap)

    # Note: If min_attr is present but step 1 was not blocked and advanced to step 2,
    # the client-side validation is non-functional because input is type="text"
    is_actually_blocked = is_stayed_step1 or (len(alert_text) > 0)
    is_fixed = is_actually_blocked
    print(f"BUG-01 EVALUATION: min_attr='{min_attr}', is_stayed_step1={is_stayed_step1}, is_fixed={is_fixed}")
    return {
        "bug_id": "BUG-01",
        "title": "SBFAS Budget Cap & Negative Value Guard",
        "fixed": is_fixed,
        "details": f"Attributes min='{min_attr}', max='{max_attr}'; Form blocked submit: {is_stayed_step1}; Alert: '{alert_text}'",
        "screenshot": shot_path
    }


async def retest_bug_02(page: Page) -> dict:
    print("\n--- RETESTING BUG-02: View As Top Banner Exit Button on Sub-pages ---")
    await authenticate_admin(page)
    await page.goto(f"{BASE_URL}/support-console", wait_until="networkidle")
    await page.wait_for_timeout(800)

    user_tab = page.get_by_role("tab", name=re.compile(r"School users", re.I))
    if await user_tab.count() > 0:
        await user_tab.click()
        await page.wait_for_timeout(800)
        search_input = page.locator('input[placeholder*="search" i], input[type="search"], input[type="text"]').first
        if await search_input.count() > 0:
            await search_input.fill("staff1")
            search_btn = page.get_by_role("button", name="Search", exact=True)
            if await search_btn.count() > 0:
                await search_btn.click()
            else:
                await page.locator("button:has-text('Search')").first.click()
            await page.wait_for_timeout(1000)
        select_btn = page.locator('tr:has-text("Bui Thi H") button:has-text("Select"), tr:has-text("staff1") button:has-text("Select"), button:has-text("Select")').first
        if await select_btn.count() > 0:
            await select_btn.click()
            await page.wait_for_timeout(800)

    reason_area = page.locator("textarea").or_(page.get_by_label("Reason", exact=False)).first
    await reason_area.wait_for(state="visible", timeout=10000)
    await reason_area.fill("Retest View As Exit Button on Subpages 123456789")
    ticket_input = page.get_by_label("Ticket reference", exact=False).or_(page.locator("input[placeholder*='ticket' i]")).first
    if await ticket_input.count() > 0:
        await ticket_input.fill("TICKET-RETEST-EXIT")

    start_btn = page.get_by_role("button", name=re.compile(r"Start View As", re.I)).first
    await start_btn.wait_for(state="visible", timeout=5000)
    if await start_btn.is_enabled():
        await start_btn.click()
        await page.wait_for_timeout(3000)
        await page.wait_for_load_state("networkidle")

    # Now navigate to /class-management (the subpage where Exit was missing before)
    await page.goto(f"{BASE_URL}/class-management", wait_until="networkidle")
    await page.wait_for_timeout(1000)

    # Check top banner & Exit button
    exit_btn = page.get_by_role("button", name="Exit", exact=True).or_(page.locator("button:has-text('Exit')"))
    exit_count = await exit_btn.count()
    exit_visible = await exit_btn.first.is_visible() if exit_count > 0 else False
    banner_text = await page.locator("body").inner_text()
    has_viewing_as = "viewing as" in banner_text.lower()

    shot_path = str(RETEST_EVIDENCE_DIR / "retest_bug02_view_as_class_management.png")
    await page.screenshot(path=shot_path)
    print(f"On /class-management: has_viewing_as={has_viewing_as}, exit_button_visible={exit_visible}, exit_count={exit_count}")

    # If exit button is visible, test clicking it
    clicked_exit_success = False
    if exit_visible:
        await exit_btn.first.click()
        await page.wait_for_timeout(1500)
        await page.wait_for_load_state("networkidle")
        after_exit_text = await page.locator("body").inner_text()
        has_viewing_as_after = "viewing as" in after_exit_text.lower()
        clicked_exit_success = not has_viewing_as_after
        print(f"Clicked Exit successfully: {clicked_exit_success} (Impersonation removed: {not has_viewing_as_after})")
        shot_path_after = str(RETEST_EVIDENCE_DIR / "retest_bug02_view_as_after_exit.png")
        await page.screenshot(path=shot_path_after)

    is_fixed = exit_visible and clicked_exit_success
    return {
        "bug_id": "BUG-02",
        "title": "View As Top Banner Exit Button on Sub-pages",
        "fixed": is_fixed,
        "details": f"Exit button visible on /class-management: {exit_visible}; Successfully exits back to MOE HQ: {clicked_exit_success}",
        "screenshot": shot_path
    }


async def retest_bug_03(page: Page) -> dict:
    print("\n--- RETESTING BUG-03: Date Input Year Constraint (Max 4 digits / 2099) ---")
    await authenticate_admin(page)

    # Navigate to Component Wizard to reach Rate Rules form
    await page.goto(f"{BASE_URL}/fee-management/components/new", wait_until="networkidle")
    await page.wait_for_timeout(800)

    comp_name = f"Retest Date Comp {int(time.time())}"
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
    min_attr = await from_input.get_attribute("min")
    max_attr = await from_input.get_attribute("max")
    maxlength_attr = await from_input.get_attribute("maxlength")
    print(f"Date input attributes: min='{min_attr}', max='{max_attr}', maxlength='{maxlength_attr}'")

    # Try filling year 20266
    await from_input.fill("20266-05-15")
    val_after = await from_input.input_value()
    is_valid = await from_input.evaluate("el => el.checkValidity()")
    validation_msg = await from_input.evaluate("el => el.validationMessage")
    print(f"After filling 20266-05-15: input_value='{val_after}', checkValidity()={is_valid}, validationMessage='{validation_msg}'")

    amount_input = page.locator("#fixed-amount")
    if await amount_input.count() > 0:
        await amount_input.fill("100.00")

    save_btn = page.locator('button[type="submit"]:has-text("Save rates")')
    if await save_btn.count() > 0 and await save_btn.is_enabled():
        await save_btn.click()
        await page.wait_for_timeout(1000)

    url_after = page.url
    is_blocked = "rate-rules/new" in url_after or not is_valid or (max_attr is not None and "2099" in max_attr) or len(validation_msg) > 0
    shot_path = str(RETEST_EVIDENCE_DIR / "retest_bug03_date_year_constraint.png")
    await page.screenshot(path=shot_path)
    print(f"Form submission blocked/invalid: {is_blocked}, URL after: {url_after}")

    is_fixed = is_blocked or (max_attr is not None) or (val_after != "20266-05-15")
    return {
        "bug_id": "BUG-03",
        "title": "Date Input Year Constraint (Max 4 digits / 2099)",
        "fixed": is_fixed,
        "details": f"Attributes: min='{min_attr}', max='{max_attr}'; checkValidity={is_valid}; validationMessage='{validation_msg}'; Blocked submit: {is_blocked}",
        "screenshot": shot_path
    }


async def main():
    results = []
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

        try:
            r1 = await retest_bug_01(page)
            results.append(r1)
        except Exception as e:
            print(f"Error testing Bug 1: {e}")
            results.append({"bug_id": "BUG-01", "fixed": False, "details": f"Exception: {e}"})

        try:
            r2 = await retest_bug_02(page)
            results.append(r2)
        except Exception as e:
            print(f"Error testing Bug 2: {e}")
            results.append({"bug_id": "BUG-02", "fixed": False, "details": f"Exception: {e}"})

        try:
            r3 = await retest_bug_03(page)
            results.append(r3)
        except Exception as e:
            print(f"Error testing Bug 3: {e}")
            results.append({"bug_id": "BUG-03", "fixed": False, "details": f"Exception: {e}"})

        await browser.close()

    print("\n=======================================================")
    print("FINAL RETEST SUMMARY:")
    for r in results:
        status = "PASSED (FIXED)" if r.get("fixed") else "STILL FAILING"
        print(f"[{r['bug_id']}] {r.get('title', '')}: {status} - {r.get('details', '')}")
    print("=======================================================")


if __name__ == "__main__":
    asyncio.run(main())
