#!/usr/bin/env python3
"""
tools/comprehensive_bsk_recon.py - Deep DOM Reconnaissance & Full Locator Extractor
Extracts all interactive elements, form fields, buttons, tables, dialogs, and navigation
elements from live web applications (localhost:5173 and localhost:5174).
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional

try:
    from playwright.sync_api import sync_playwright, Page, BrowserContext
except ImportError:
    print("[Error] Playwright is required in the virtualenv (.venv/bin/python)")
    sys.exit(1)


def authenticate_5174(page: Page, base_url: str = "http://localhost:5174"):
    """Logs into E-Service via SingPass MockPass if needed."""
    try:
        page.goto(f"{base_url}/parent/login", wait_until="domcontentloaded", timeout=10000)
    except Exception:
        pass
    
    if page.locator("button:has-text('Sign in with Singpass')").count() > 0:
        page.click("button:has-text('Sign in with Singpass')")
        try:
            page.wait_for_selector("button:has-text('Log in with Singpass')", timeout=10000)
            page.click("button:has-text('Log in with Singpass')")
            page.wait_for_url(lambda u: "login" not in u and "callback" not in u, timeout=15000)
        except Exception as e:
            print(f"[Warn] Singpass login redirect issue: {e}")
        page.wait_for_timeout(1000)


def authenticate_5173(page: Page, base_url: str = "http://localhost:5173"):
    """Logs into Admin Portal via Microsoft SSO if needed."""
    try:
        page.goto(f"{base_url}/login", wait_until="domcontentloaded", timeout=10000)
    except Exception:
        pass
    
    if page.locator("button:has-text('Sign in with Microsoft')").count() > 0:
        page.click("button:has-text('Sign in with Microsoft')")
        try:
            page.wait_for_url("**/microsoft-provider/**", timeout=15000)
            admin_tile = page.locator(".account-tile:has-text('admin@IAM.edu.vn'), [onclick*='admin@IAM.edu.vn']")
            admin_tile.first.click()
            page.wait_for_url(lambda u: "login" not in u and "callback" not in u, timeout=15000)
        except Exception as e:
            print(f"[Warn] Admin login redirect issue: {e}")
        page.wait_for_timeout(1000)


def inspect_dom(page: Page) -> Dict[str, Any]:
    """Runs in-page JS evaluation to extract all interactive and key elements."""
    js_code = """() => {
        const results = {
            title: document.title,
            url: window.location.href,
            heading: document.querySelector('h1, h2')?.innerText?.trim() || '',
            breadcrumbs: Array.from(document.querySelectorAll('nav[aria-label*="breadcrumb" i] a, ol.breadcrumb li, .breadcrumb a'))
                              .map(el => el.innerText.trim()).filter(Boolean),
            inputs: [],
            buttons: [],
            selects: [],
            links: [],
            tables: [],
            dialogs: [],
            alerts: []
        };

        const seenSelectors = new Set();

        function getBestSelector(el, tag) {
            const testId = el.getAttribute('data-testid');
            if (testId) return `[data-testid="${testId}"]`;

            const name = el.getAttribute('name');
            if (name) return `${tag}[name="${name}"]`;

            const id = el.id;
            if (id && !id.startsWith('_r_') && !id.startsWith(':r')) return `#${id}`;

            const text = (el.innerText || el.textContent || '').trim().split('\\n')[0].substring(0, 35);
            if (tag === 'button' && text) return `button:has-text("${text}")`;

            const placeholder = el.getAttribute('placeholder');
            if (placeholder) return `${tag}[placeholder*="${placeholder}"]`;

            const ariaLabel = el.getAttribute('aria-label');
            if (ariaLabel) return `${tag}[aria-label="${ariaLabel}"]`;

            const role = el.getAttribute('role');
            if (role && text) return `[role="${role}"]:has-text("${text}")`;

            if (el.className && typeof el.className === 'string') {
                const firstClass = el.className.split(' ').filter(c => c && !c.includes(':') && !c.includes('/'))[0];
                if (firstClass) return `${tag}.${firstClass}`;
            }

            return tag;
        }

        // 1. Inputs & Textareas
        document.querySelectorAll('input, textarea').forEach(el => {
            const tag = el.tagName.toLowerCase();
            const type = el.getAttribute('type') || 'text';
            const name = el.getAttribute('name') || '';
            const id = el.id || '';
            const placeholder = el.getAttribute('placeholder') || '';
            const value = el.value || '';
            const disabled = el.disabled || el.getAttribute('aria-disabled') === 'true';
            const required = el.required || el.getAttribute('aria-required') === 'true';
            
            let label = '';
            if (id) {
                const labelEl = document.querySelector(`label[for="${id}"]`);
                if (labelEl) label = labelEl.innerText.trim();
            }
            if (!label && el.closest('label')) {
                label = el.closest('label').innerText.trim();
            }
            if (!label) {
                const parent = el.parentElement;
                if (parent) {
                    const prev = el.previousElementSibling;
                    if (prev && (prev.tagName === 'LABEL' || prev.tagName === 'SPAN')) {
                        label = prev.innerText.trim();
                    }
                }
            }

            const selector = getBestSelector(el, tag);
            results.inputs.push({
                tag,
                type,
                name,
                id,
                label: label.substring(0, 50),
                placeholder,
                value: type !== 'password' ? value.substring(0, 40) : '***',
                disabled,
                required,
                selector
            });
        });

        // 2. Selects
        document.querySelectorAll('select, [role="combobox"]').forEach(el => {
            const tag = el.tagName.toLowerCase();
            const name = el.getAttribute('name') || '';
            const id = el.id || '';
            let options = [];
            if (tag === 'select') {
                options = Array.from(el.options).map(o => o.text.trim()).slice(0, 10);
            }
            let label = '';
            if (id) {
                const labelEl = document.querySelector(`label[for="${id}"]`);
                if (labelEl) label = labelEl.innerText.trim();
            }

            const selector = getBestSelector(el, tag);
            results.selects.push({
                tag,
                name,
                id,
                label: label.substring(0, 50),
                options,
                selector
            });
        });

        // 3. Buttons & Action controls
        document.querySelectorAll('button, [role="button"]').forEach(el => {
            const tag = el.tagName.toLowerCase();
            const text = (el.innerText || el.textContent || '').trim().split('\\n')[0].substring(0, 50);
            const type = el.getAttribute('type') || 'button';
            const disabled = el.disabled || el.getAttribute('aria-disabled') === 'true';
            const ariaLabel = el.getAttribute('aria-label') || '';
            const selector = getBestSelector(el, tag);
            
            if (text || ariaLabel) {
                results.buttons.push({
                    text: text || ariaLabel,
                    type,
                    disabled,
                    selector
                });
            }
        });

        // 4. Links in navigation and main content
        document.querySelectorAll('nav a, header a, main a').forEach(el => {
            const text = (el.innerText || el.textContent || '').trim().split('\\n')[0].substring(0, 50);
            const href = el.getAttribute('href') || '';
            if (text && href && !href.startsWith('javascript:')) {
                results.links.push({
                    text,
                    href,
                    selector: `a[href="${href}"]`
                });
            }
        });

        // 5. Tables & Grids
        document.querySelectorAll('table').forEach(table => {
            const headers = Array.from(table.querySelectorAll('th')).map(th => th.innerText.trim()).filter(Boolean);
            const rowCount = table.querySelectorAll('tbody tr').length;
            results.tables.push({
                headers,
                rowCount,
                selector: 'table'
            });
        });

        // 6. Dialogs & Modals
        document.querySelectorAll('[role="dialog"], [role="alertdialog"], .modal').forEach(dlg => {
            const title = dlg.querySelector('h2, h3, [class*="title"]')?.innerText?.trim() || '';
            const actions = Array.from(dlg.querySelectorAll('button')).map(b => b.innerText.trim());
            results.dialogs.push({
                title,
                actions,
                selector: '[role="dialog"]'
            });
        });

        // 7. Alerts & Feedback
        document.querySelectorAll('[role="alert"], [role="status"], .alert').forEach(al => {
            const text = al.innerText.trim().substring(0, 80);
            if (text) {
                results.alerts.push({
                    text,
                    selector: '[role="alert"]'
                });
            }
        });

        return results;
    }"""
    return page.evaluate(js_code)


def recon_page(url: str, is_admin: bool = False, expand_actions: bool = True) -> Dict[str, Any]:
    """Inspects a single page thoroughly with Playwright."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        # Handle authentication if required
        if is_admin:
            authenticate_5173(page, "http://localhost:5173")
        else:
            authenticate_5174(page, "http://localhost:5174")

        print(f"[*] Navigating to target: {url}")
        try:
            page.goto(url, wait_until="networkidle", timeout=15000)
        except Exception:
            page.goto(url, wait_until="domcontentloaded", timeout=15000)
        page.wait_for_timeout(1000)

        # Base snapshot
        data = inspect_dom(page)

        # Dynamic state inspection (e.g. edit mode buttons, tabs)
        dynamic_elements = []
        if expand_actions:
            # Check for tabs
            tabs = page.locator("[role='tab'], .tab-button, button[id*='tab']").all()
            for i, tab in enumerate(tabs[:4]):
                try:
                    tab_name = tab.inner_text().strip()
                    if tab_name:
                        tab.click(timeout=2000)
                        page.wait_for_timeout(500)
                        sub_data = inspect_dom(page)
                        dynamic_elements.append({
                            "trigger": f"Tab: {tab_name}",
                            "data": sub_data
                        })
                except Exception:
                    pass

            # Check for edit mode button
            edit_btn = page.locator("button:has-text('Update details'), button:has-text('Edit'), button:has-text('Add')").first
            if edit_btn.count() > 0 and edit_btn.is_visible():
                try:
                    btn_text = edit_btn.inner_text().strip()
                    edit_btn.click(timeout=2000)
                    page.wait_for_timeout(800)
                    edit_data = inspect_dom(page)
                    dynamic_elements.append({
                        "trigger": f"Action: {btn_text}",
                        "data": edit_data
                    })
                except Exception:
                    pass

        data["dynamic_states"] = dynamic_elements
        browser.close()
        return data


def format_markdown(page_name: str, url: str, portal_type: str, data: Dict[str, Any], functional_flow: str = "") -> str:
    """Renders structured Markdown document compliant with AGENTS.md standards."""
    lines = [
        f"# 📋 BSK Locator & Functional Flow Spec: {page_name}",
        "",
        "| Trường Thông Tin | Chi Tiết |",
        "| :--- | :--- |",
        f"| **Portal / Cổng Dịch Vụ** | `{portal_type}` |",
        f"| **Đường Dẫn Thực Tế (URL)** | `{url}` |",
        f"| **Tiêu Đề Trang (Title)** | `{data.get('title', '')}` |",
        f"| **Heading Chính (H1/H2)** | `{data.get('heading', '')}` |",
        f"| **Thời Điểm Trích Xuất (BSK)** | `Live DOM Verified` |",
        "",
        "---",
        "",
        "## 🔍 1. Bảng Locators Chi Tiết (BSK Verified DOM Elements)",
        "",
        "### 1.1 Ô Nhập Liệu & Form Controls (Inputs / Textareas)",
        "| Tên Trường / Nhãn | Loại | Name / ID | Selector Tối Ưu (Playwright) | Bắt Buộc | Disabled |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |"
    ]

    inputs = data.get("inputs", [])
    if inputs:
        for inp in inputs:
            lbl = inp.get("label") or inp.get("placeholder") or inp.get("name") or "Input"
            lbl = lbl.replace("|", "\\|")
            tag_type = f"`<{inp['tag']} type='{inp['type']}'>`"
            ident = inp.get("name") or inp.get("id") or "-"
            sel = f"`{inp['selector']}`"
            req = "✅ Có" if inp.get("required") else "❌ Không"
            dis = "🔒 Khóa" if inp.get("disabled") else "🔓 Mở"
            lines.append(f"| {lbl} | {tag_type} | `{ident}` | {sel} | {req} | {dis} |")
    else:
        lines.append("| *Không có ô nhập liệu trực tiếp trên màn hình này* | - | - | - | - | - |")

    lines.extend([
        "",
        "### 1.2 Hộp Chọn & Dropdowns (Selects / Comboboxes)",
        "| Tên Dropdown / Nhãn | ID / Name | Selector Tối Ưu | Các Lựa Chọn Khả Dụng (Options Sample) |",
        "| :--- | :--- | :--- | :--- |"
    ])
    selects = data.get("selects", [])
    if selects:
        for sel_item in selects:
            lbl = sel_item.get("label") or sel_item.get("name") or "Select"
            ident = sel_item.get("id") or sel_item.get("name") or "-"
            sel = f"`{sel_item['selector']}`"
            opts = ", ".join([f"'{o}'" for o in sel_item.get("options", [])[:5]]) or "Dynamic"
            lines.append(f"| {lbl} | `{ident}` | {sel} | {opts} |")
    else:
        lines.append("| *Không có thẻ dropdown/select trên view này* | - | - | - |")

    lines.extend([
        "",
        "### 1.3 Nút Bấm & Thao Tác (Buttons & Interactive Actions)",
        "| Nhãn Nút / Action | Kiểu (Type) | Trạng Thái | Selector Thực Nghiệm |",
        "| :--- | :--- | :--- | :--- |"
    ])
    buttons = data.get("buttons", [])
    if buttons:
        seen_btn = set()
        for b in buttons:
            txt = b.get("text", "").replace("|", "\\|")
            sel = b.get("selector", "")
            if sel in seen_btn:
                continue
            seen_btn.add(sel)
            status = "🔒 Disabled" if b.get("disabled") else "🟢 Enabled"
            lines.append(f"| {txt} | `{b.get('type')}` | {status} | `{sel}` |")
    else:
        lines.append("| *Không có nút bấm thao tác* | - | - | - |")

    lines.extend([
        "",
        "### 1.4 Bảng Dữ Liệu & Danh Sách (Tables & Grids)",
        "| Thành Phần Bảng | Headers / Các Cột Nhận Diện | Selector Đại Diện |",
        "| :--- | :--- | :--- |"
    ])
    tables = data.get("tables", [])
    if tables:
        for tbl in tables:
            hdrs = " \\| ".join(tbl.get("headers", [])) or "No header"
            lines.append(f"| Table Grid ({tbl.get('rowCount', 0)} rows) | `{hdrs}` | `{tbl['selector']}` |")
    else:
        lines.append("| *Không chứa bảng dữ liệu (Table)* | - | - |")

    lines.extend([
        "",
        "### 1.5 Hộp Thoại & Thông Báo (Modals / Dialogs / Alerts)",
        "| Loại Thông Báo / Modal | Tiêu Đề / Nội Dung Nhận Diện | Selector Tối Ưu |",
        "| :--- | :--- | :--- |"
    ])
    dialogs = data.get("dialogs", []) + data.get("alerts", [])
    if dialogs:
        for dlg in dialogs:
            title = dlg.get("title") or dlg.get("text") or "Alert Dialog"
            title = title.replace("|", "\\|")
            lines.append(f"| Alert / Dialog | {title} | `{dlg['selector']}` |")
    else:
        lines.append("| *Không có dialog / alert nào đang hiển thị mặc định* | - | `[role='alert'], [role='dialog']` |")

    # Dynamic states if captured
    dynamic_states = data.get("dynamic_states", [])
    if dynamic_states:
        lines.extend([
            "",
            "### 1.6 Locators Bổ Sung Từ Trạng Thái Động (Dynamic States / Modals / Sub-Tabs)",
            ""
        ])
        for ds in dynamic_states:
            lines.append(f"#### 🔹 Khi kích hoạt `{ds['trigger']}`:")
            sub = ds["data"]
            sub_inputs = sub.get("inputs", [])
            sub_buttons = sub.get("buttons", [])
            if sub_inputs:
                lines.append("| Nhãn Ô Nhập | Selector Playwright |")
                lines.append("| :--- | :--- |")
                for si in sub_inputs:
                    lines.append(f"| {si.get('label') or si.get('name')} | `{si['selector']}` |")
            if sub_buttons:
                lines.append("| Nút Xuất Hiện | Selector |")
                lines.append("| :--- | :--- |")
                for sb in sub_buttons:
                    lines.append(f"| {sb.get('text')} | `{sb['selector']}` |")
            lines.append("")

    # Functional flow section
    lines.extend([
        "",
        "---",
        "",
        "## 🔄 2. Đặc Tả Luồng Nghiệp Vụ Chi Tiết (Functional Flow & State Machine)",
        "",
        functional_flow or "Đặc tả luồng nghiệp vụ chi tiết cho màn hình.",
        "",
        "---",
        "",
        "## 💻 3. Playwright Page Object Snippet Khuyến Nghị",
        "```python",
        f"class {page_name.replace(' ', '').replace('-', '').replace('_', '')}Page(BasePage):",
        f'    """Page Object đại diện cho màn hình {page_name} - Verified via BSK DOM Recon."""',
        f'    URL = "{url}"',
        ""
    ])

    for inp in inputs[:10]:
        var_name = re.sub(r'[^a-zA-Z0-9_]', '_', (inp.get('name') or inp.get('label') or 'field').lower())
        var_name = re.sub(r'_+', '_', var_name).strip('_')
        lines.append(f'    # {inp.get("label") or inp.get("name")}')
        lines.append(f'    {var_name}_input = property(lambda self: self.page.locator("{inp["selector"]}"))')

    for btn in buttons[:10]:
        txt = btn.get("text", "")
        if txt:
            var_name = re.sub(r'[^a-zA-Z0-9_]', '_', txt.lower())
            var_name = re.sub(r'_+', '_', var_name).strip('_')
            lines.append(f'    # Nút {txt}')
            lines.append(f'    {var_name}_btn = property(lambda self: self.page.locator("{btn["selector"]}"))')

    lines.extend([
        "```",
        ""
    ])

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="BSK Full Reconnaissance Tool")
    parser.add_argument("--url", required=True, help="Full URL to inspect")
    parser.add_argument("--name", required=True, help="Friendly name of the page")
    parser.add_argument("--portal", choices=["5173", "5174", "admin", "eservice"], default="5174", help="Portal type")
    parser.add_argument("--output", required=True, help="Path to markdown output file")
    parser.add_argument("--flow-file", help="Path to markdown file containing functional flow description to merge")
    args = parser.parse_args()

    is_admin = args.portal in ["5173", "admin"]
    data = recon_page(args.url, is_admin=is_admin)

    flow_content = ""
    if args.flow_file and Path(args.flow_file).exists():
        flow_content = Path(args.flow_file).read_text(encoding="utf-8")

    md_output = format_markdown(args.name, args.url, f"localhost:{args.portal}", data, flow_content)

    out_file = Path(args.output)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(md_output, encoding="utf-8")
    print(f"\n[✓] Successfully saved comprehensive BSK locator & flow spec to: {out_file}")


if __name__ == "__main__":
    main()
