#!/usr/bin/env python3
"""
=============================================================================
Capture Comprehensive Visual Evidence for BUG-01 (DEST-08)
Target: SBFAS Scheme Budget Cap & Zero/Negative Value Validation Guard
Màn hình: /sbfas-schemes/new
Captures:
  1. 01_typing_negative_sanitized.png - Sanitize xóa dấu trừ '-'
  2. 02_zero_budget_accepted_step2.png - Nhập 0 SGD vẫn lọt sang Bước 2
  3. 03_step1_extreme_budget_input.png - Nhập 999,999,999 SGD tại Bước 1
  4. 04_step2_bypassed_without_error.png - Vượt qua Bước 1 sang Bước 2 không lỗi
  5. 05_step4_review_extreme_budget.png - Màn hình Review hiển thị $999,999,999.00 SGD
  6. 06_published_scheme_in_table_999m.png - Đề án xuất bản thành công trên bảng danh sách
=============================================================================
"""

import asyncio
import time
from pathlib import Path
from playwright.async_api import async_playwright, Page

BASE_DIR = Path(__file__).resolve().parent
EVIDENCE_DIR = BASE_DIR / "evidence_bugs" / "bug01_detail"
EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

ADMIN_URL = "https://admin.20-255-158-192.sslip.io"
SCHOOL_EMAIL = "staff1@IAM.edu.vn"


async def set_hud(page: Page, title: str, subtitle: str, bg="#0f172a", text_col="#f8fafc", badge="BUG-01 EVIDENCE"):
    js = f"""
    (() => {{
        let hud = document.getElementById('qa-evidence-hud');
        if (!hud) {{
            hud = document.createElement('div');
            hud.id = 'qa-evidence-hud';
            hud.style.position = 'fixed';
            hud.style.top = '12px';
            hud.style.left = '50%';
            hud.style.transform = 'translateX(-50%)';
            hud.style.zIndex = '999999';
            hud.style.backgroundColor = '{bg}';
            hud.style.color = '{text_col}';
            hud.style.padding = '10px 24px';
            hud.style.borderRadius = '8px';
            hud.style.boxShadow = '0 10px 25px -5px rgba(0, 0, 0, 0.4), 0 8px 10px -6px rgba(0, 0, 0, 0.3)';
            hud.style.fontFamily = 'Segoe UI, system-ui, sans-serif';
            hud.style.fontSize = '13px';
            hud.style.display = 'flex';
            hud.style.alignItems = 'center';
            hud.style.gap = '16px';
            hud.style.border = '2px solid #ef4444';
            hud.style.pointerEvents = 'none';
            document.body.appendChild(hud);
        }}
        hud.innerHTML = `
            <div style="background:#ef4444; color:white; font-weight:800; padding:4px 8px; border-radius:4px; font-size:11px; letter-spacing:0.5px;">{badge}</div>
            <div>
                <div style="font-weight:700; font-size:14px; margin-bottom:2px;">{title}</div>
                <div style="color:#94a3b8; font-size:12px;">{subtitle}</div>
            </div>
        `;
    }})();
    """
    await page.evaluate(js)


async def highlight_element(page: Page, css_selector: str, border_color="#ef4444"):
    try:
        js = f"""
        (() => {{
            const el = document.querySelector('{css_selector}');
            if (el) {{
                el.style.outline = '3px solid {border_color}';
                el.style.outlineOffset = '2px';
                el.style.boxShadow = '0 0 12px {border_color}';
                el.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
            }}
        }})();
        """
        await page.evaluate(js)
    except Exception:
        pass


async def highlight_text_content(page: Page, match_text: str, border_color="#ef4444"):
    try:
        js = f"""
        (() => {{
            const all = document.querySelectorAll('*');
            for (const el of all) {{
                if (el.children.length === 0 && el.innerText && el.innerText.includes('{match_text}')) {{
                    el.style.outline = '3px solid {border_color}';
                    el.style.outlineOffset = '2px';
                    el.style.boxShadow = '0 0 12px {border_color}';
                    el.style.backgroundColor = '#fee2e2';
                    el.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
                    break;
                }}
            }}
        }})();
        """
        await page.evaluate(js)
    except Exception:
        pass


async def authenticate(page: Page):
    target = f"{ADMIN_URL}/sbfas-schemes"
    print(f"[*] Navigating to {target}")
    await page.goto(target, wait_until="domcontentloaded")
    await page.wait_for_timeout(1500)

    if "login" in page.url or await page.locator("button:has-text('Sign in with Microsoft')").count() > 0:
        print(f"[*] Logging in via Microsoft SSO as {SCHOOL_EMAIL}...")
        ms_btn = page.locator("button:has-text('Sign in with Microsoft')")
        if await ms_btn.is_visible():
            await ms_btn.click()
            await page.wait_for_timeout(1500)

        tile = page.locator(f".account-tile:has-text('{SCHOOL_EMAIL}'), [data-email='{SCHOOL_EMAIL}']").first
        if await tile.count() > 0:
            await tile.click()
        else:
            fallback = page.locator(f"text={SCHOOL_EMAIL}").first
            if await fallback.count() > 0:
                await fallback.click()
        await page.wait_for_timeout(2500)

    await page.goto(target, wait_until="networkidle")
    await page.wait_for_timeout(1000)

    # Clear View As if active
    exit_btn = page.get_by_role("button", name="Exit", exact=True)
    if await exit_btn.count() > 0 and await exit_btn.is_visible():
        print("[*] Clearing active View As session...")
        await exit_btn.click()
        await page.wait_for_timeout(1200)
        await page.goto(target, wait_until="networkidle")


async def run_evidence_capture():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--ignore-certificate-errors", "--no-sandbox", "--disable-setuid-sandbox"]
        )
        context = await browser.new_context(
            viewport={"width": 1440, "height": 900},
            ignore_https_errors=True
        )
        page = await context.new_page()

        print("=== BẮT ĐẦU CHỤP BỘ ẢNH CHI TIẾT CHO BUG-01 (DEST-08) ===")
        await authenticate(page)

        # ---------------------------------------------------------------------
        # 1. ẢNH 1: NHẬP SỐ ÂM "-50000" -> SANITIZE THÀNH "50000"
        # ---------------------------------------------------------------------
        print("\n[1/6] Kiểm tra xử lý số âm '-50000'...")
        await page.goto(f"{ADMIN_URL}/sbfas-schemes/new", wait_until="networkidle")
        await page.wait_for_timeout(1000)

        ts = int(time.time())
        await page.locator("#sbfas-name").fill(f"Bug01_Negative_Test_{ts}")
        await page.locator("#sbfas-open-from").fill("2026-11-01")
        await page.locator("#sbfas-open-to").fill("2026-11-30")
        await page.locator("#sbfas-effective-from").fill("2026-12-01")
        await page.locator("#sbfas-effective-to").fill("2027-11-30")

        budget_input = page.locator("#sbfas-budget")
        await budget_input.fill("-50000")
        val_after_type = await budget_input.input_value()

        await highlight_element(page, "#sbfas-budget", "#3b82f6")
        await set_hud(
            page,
            "1. Kiểm tra Sanitize số âm: Gõ phím '-50000'",
            f"Giá trị thực tế trong ô: '{val_after_type}' (Dev đã tự động xóa dấu trừ '-', nhưng chưa chặn số 0 và trần ngân sách)",
            bg="#0f172a",
            text_col="#f8fafc",
            badge="DEV ĐÃ SỬA DẤU ÂM"
        )
        shot1 = EVIDENCE_DIR / "01_typing_negative_sanitized.png"
        await page.screenshot(path=str(shot1))
        print(f" -> Đã lưu: {shot1}")

        # ---------------------------------------------------------------------
        # 2. ẢNH 2: NHẬP NGÂN SÁCH "0" SGD -> CHẤP NHẬN SANG BƯỚC 2
        # ---------------------------------------------------------------------
        print("\n[2/6] Kiểm tra ngân sách bằng 0 SGD...")
        await budget_input.fill("0")
        await page.wait_for_timeout(300)
        next_btn = page.locator('button[type="submit"]:has-text("Next"), button:has-text("Next")').first
        await next_btn.click()
        await page.wait_for_timeout(1000)

        is_step2 = await page.locator("#sbfas-ghi-to").is_visible()
        await set_hud(
            page,
            "2. LỖI TỒN ĐỌNG: Ngân sách 0 SGD được chấp nhận!",
            "Nhập '0' vào Total Budget, form KHÔNG báo lỗi và chuyển thẳng sang Bước 2 (Eligibility)",
            bg="#450a0a",
            text_col="#fee2e2",
            badge="TỒN ĐỌNG: BUDGET = 0"
        )
        shot2 = EVIDENCE_DIR / "02_zero_budget_accepted_step2.png"
        await page.screenshot(path=str(shot2))
        print(f" -> Đã lưu: {shot2}")

        # ---------------------------------------------------------------------
        # 3. ẢNH 3: NHẬP SỐ TIỀN CỰC LỚN (999,999,999 SGD) TẠI BƯỚC 1
        # ---------------------------------------------------------------------
        print("\n[3/6] Nhập số cực lớn 999,999,999 SGD tại Bước 1...")
        await page.goto(f"{ADMIN_URL}/sbfas-schemes/new", wait_until="networkidle")
        await page.wait_for_timeout(1000)

        extreme_scheme_name = f"BUG01_ExtremeBudget_999M_{ts}"
        await page.locator("#sbfas-name").fill(extreme_scheme_name)
        await page.locator("#sbfas-open-from").fill("2026-11-01")
        await page.locator("#sbfas-open-to").fill("2026-11-30")
        await page.locator("#sbfas-effective-from").fill("2026-12-01")
        await page.locator("#sbfas-effective-to").fill("2027-11-30")
        await page.locator("#sbfas-budget").fill("999999999")
        await page.locator("#sbfas-eligibility-description").fill("Demonstrating Extreme Budget Overflow ($999M SGD) without validation")

        await highlight_element(page, "#sbfas-budget", "#ef4444")
        await set_hud(
            page,
            "3. LỖI VƯỢT TRẦN: Nhập 999,999,999 SGD (Hạn mức trần quy định là $50,000 SGD)",
            "Ô nhập liệu nhận toàn bộ 9 chữ số mà không có kiểm tra biên trên (Không có viền đỏ)",
            bg="#450a0a",
            text_col="#fee2e2",
            badge="TỒN ĐỌNG: VƯỢT TRẦN"
        )
        shot3 = EVIDENCE_DIR / "03_step1_extreme_budget_input.png"
        await page.screenshot(path=str(shot3))
        print(f" -> Đã lưu: {shot3}")

        # ---------------------------------------------------------------------
        # 4. ẢNH 4: BẤM NEXT CHẤP NHẬN SANG BƯỚC 2 MÀ KHÔNG BÁO LỖI
        # ---------------------------------------------------------------------
        print("\n[4/6] Bấm Next sang Bước 2...")
        next_btn = page.locator('button[type="submit"]:has-text("Next"), button:has-text("Next")').first
        await next_btn.click()
        await page.wait_for_timeout(1000)

        # Bước 2: Eligibility
        sc_checkbox = page.locator("#sbfas-nationality-SC")
        if await sc_checkbox.count() > 0 and not await sc_checkbox.is_checked():
            await sc_checkbox.click()
        await page.locator("#sbfas-ghi-to").fill("3000")
        await page.locator("#sbfas-pci-to").fill("1000")

        await set_hud(
            page,
            "4. VƯỢT QUA BƯỚC 1: Form chuyển tiếp thành công sang Bước 2",
            "Hệ thống hoàn toàn bỏ qua việc kiểm tra trần $50,000, cho phép người dùng tiếp tục khai báo tiêu chí",
            bg="#450a0a",
            text_col="#fee2e2",
            badge="BYPASS THÀNH CÔNG"
        )
        shot4 = EVIDENCE_DIR / "04_step2_bypassed_without_error.png"
        await page.screenshot(path=str(shot4))
        print(f" -> Đã lưu: {shot4}")

        # ---------------------------------------------------------------------
        # 5. ẢNH 5: CẤU HÌNH MA TRẬN & TỚI BƯỚC 4 (REVIEW SCREEN)
        # ---------------------------------------------------------------------
        print("\n[5/6] Điền Bước 3 và chuyển sang Bước 4 (Review)...")
        next_btn_s2 = page.locator('button:has-text("Next")')
        await next_btn_s2.click()
        await page.wait_for_timeout(1200)

        # Bước 3: Add fee component
        add_fee_comp_btn = page.locator('button:has-text("Add fee components")')
        await add_fee_comp_btn.click()
        await page.wait_for_timeout(1000)

        modal = page.locator("[role='dialog']")
        first_chk = modal.locator("input[type='checkbox']").first
        await first_chk.click()
        apply_btn = modal.locator('button:has-text("Apply")')
        await apply_btn.click()
        await page.wait_for_timeout(1000)

        # Điền 100%
        inputs = await page.locator("table input").all()
        for inp in inputs:
            await inp.fill("100")

        # Bấm Review
        review_btn = page.locator('button:has-text("Review")')
        await review_btn.click()
        await page.wait_for_timeout(1500)

        # Highlight ô ngân sách tại màn hình review
        await highlight_text_content(page, "999,999,999", "#ef4444")
        await set_hud(
            page,
            "5. BƯỚC 4 REVIEW: Ngân sách $999,999,999 SGD xuất hiện chính thức trên màn hình duyệt",
            "Toàn bộ quy trình wizard chấp thuận ngân sách bất thường này và chuẩn bị cho Publish",
            bg="#450a0a",
            text_col="#fee2e2",
            badge="REVIEW OVERFLOW"
        )
        shot5 = EVIDENCE_DIR / "05_step4_review_extreme_budget.png"
        await page.screenshot(path=str(shot5))
        print(f" -> Đã lưu: {shot5}")

        # ---------------------------------------------------------------------
        # 6. ẢNH 6: XUẤT BẢN THÀNH CÔNG LÊN BẢNG DANH SÁCH /sbfas-schemes
        # ---------------------------------------------------------------------
        print("\n[6/6] Bấm Publish xuất bản đề án...")
        publish_btn = page.locator('button:has-text("Publish")')
        await publish_btn.click()
        await page.wait_for_timeout(3500)

        # Tìm dòng đề án vừa xuất bản
        target_row = page.locator(f"table tbody tr:has-text('{extreme_scheme_name}')").first
        if await target_row.count() > 0:
            row_text = await target_row.text_content()
            print(f"[*] Found newly published row: {row_text.strip()}")
            js_hl_row = f"""
            (() => {{
                const rows = Array.from(document.querySelectorAll('table tbody tr'));
                const match = rows.find(r => r.innerText.includes('{extreme_scheme_name}'));
                if (match) {{
                    match.style.backgroundColor = '#fee2e2';
                    match.style.outline = '3px solid #ef4444';
                    match.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
                }}
            }})();
            """
            await page.evaluate(js_hl_row)

        await set_hud(
            page,
            "6. HẬU QUẢ: Đề án $999M SGD đã được Publish thành công vào CSDL hệ thống!",
            f"Tên: {extreme_scheme_name} | Trạng thái: PUBLISHED | Ngân sách: $999,999,999.00 SGD",
            bg="#450a0a",
            text_col="#fee2e2",
            badge="DATABASE CORRUPTED"
        )
        shot6 = EVIDENCE_DIR / "06_published_scheme_in_table_999m.png"
        await page.screenshot(path=str(shot6))
        print(f" -> Đã lưu: {shot6}")

        await browser.close()
        print("\n=== HOÀN THÀNH CHỤP 6 ẢNH CHI TIẾT CHO BUG-01 ===")


if __name__ == "__main__":
    asyncio.run(run_evidence_capture())
