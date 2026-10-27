#!/usr/bin/env python3
"""
tools/recon_bsk.py - Automated DOM Reconnaissance & Locator Extractor.

Bridge between live web applications and Markdown test specs.
Queries DOM elements via BSK (Browser-Skill) or Playwright headless CDP,
extracting 100% verified IDs, classes, and accessible roles into a Markdown locator table.

Usage:
    python3 tools/recon_bsk.py --url http://localhost:8080/curricula
    python3 tools/recon_bsk.py --url curricula_trainer_account.html
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional

# Ensure Playwright from local venv if available
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    venv_py = Path(__file__).resolve().parent.parent / ".venv" / "bin" / "python"
    if venv_py.exists():
        os.execv(str(venv_py), [str(venv_py)] + sys.argv)
    else:
        print("[Error] Playwright is required. Run: pip install playwright")
        sys.exit(1)


def inspect_page_elements(url_or_path: str, workspace_dir: Path) -> List[Dict[str, str]]:
    """Navigates to the page and extracts verified interactive elements."""
    target_url = url_or_path
    if not target_url.startswith("http://") and not target_url.startswith("https://"):
        local_file = (workspace_dir / target_url).resolve()
        if not local_file.exists():
            local_file = (workspace_dir / "data" / "fixtures" / "mock_pages" / target_url).resolve()
        target_url = local_file.as_uri()

    print(f"[*] Reconnaissance target: {target_url}")

    elements = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        try:
            page.goto(target_url, wait_until="networkidle", timeout=15000)
        except Exception:
            page.goto(target_url, wait_until="load", timeout=15000)
        page.wait_for_timeout(1000)

        # Handle Mock SingPass authentication if redirected to login
        if page.locator("button:has-text('Sign in with Singpass')").count() > 0:
            print("[*] Detected Singpass authentication gate. Auto-authenticating via MockPass...")
            page.click("button:has-text('Sign in with Singpass')")
            page.wait_for_selector("button:has-text('Log in with Singpass')", timeout=10000)
            page.click("button:has-text('Log in with Singpass')")
            page.wait_for_timeout(3000)
            print(f"[*] Navigating back to reconnaissance target: {target_url}")
            page.goto(target_url, wait_until="networkidle", timeout=15000)
            page.wait_for_timeout(1500)

        # Handle Microsoft SSO authentication if redirected to login
        if page.locator("button:has-text('Sign in with Microsoft')").count() > 0:
            print("[*] Detected Microsoft SSO authentication gate. Auto-authenticating...")
            page.click("button:has-text('Sign in with Microsoft')")
            page.wait_for_url("**/microsoft-provider/**", timeout=15000)
            admin_tile = page.locator(".account-tile:has-text('admin@IAM.edu.vn'), [onclick*='admin@IAM.edu.vn']")
            admin_tile.first.click()
            page.wait_for_load_state("domcontentloaded")
            page.wait_for_timeout(2000)
            print(f"[*] Navigating back to reconnaissance target: {target_url}")
            page.goto(target_url, wait_until="networkidle", timeout=15000)
            page.wait_for_timeout(1500)

        # If on profile view mode, also capture edit mode elements
        if page.locator("button:has-text('Update details')").count() > 0:
            print("[*] Detected 'Update details' button. Expanding edit mode elements...")
            page.click("button:has-text('Update details')")
            page.wait_for_timeout(1000)

        # Extract interactive form fields and buttons
        raw_elements = page.evaluate("""() => {
            const results = [];
            const queried = document.querySelectorAll('input, button, select, textarea, [role="button"], [role="alert"], .section-title, .error');
            
            queried.forEach(el => {
                const tag = el.tagName.toLowerCase();
                const id = el.id ? `#${el.id}` : '';
                const name = el.getAttribute('name');
                const testId = el.getAttribute('data-testid');
                const text = (el.innerText || el.textContent || '').trim().split('\\n')[0].substring(0, 40);
                const placeholder = el.getAttribute('placeholder') || '';
                const type = el.getAttribute('type') || '';
                const role = el.getAttribute('role') || '';
                const cls = el.className ? `.${Array.from(el.classList).slice(0, 2).join('.')}` : '';

                // Determine best selector (prefer semantic name / testId over React dynamic useId)
                let selector = '';
                if (testId) {
                    selector = `[data-testid="${testId}"]`;
                } else if (name) {
                    selector = `${tag}[name="${name}"]`;
                } else if (id && !id.startsWith('#_r_') && !id.startsWith('#:r')) {
                    selector = id;
                } else if (tag === 'button' && text) {
                    selector = `button:has-text("${text}")`;
                } else if (cls) {
                    selector = cls;
                } else {
                    selector = tag;
                }

                // Determine display label
                let label = text || placeholder || name || id.replace('#', '') || 'Element';

                // Look for preceding or parent label
                if (id) {
                    const labelEl = document.querySelector(`label[for="${el.id}"]`);
                    if (labelEl) {
                        label = labelEl.innerText.trim();
                    }
                }

                results.push({
                    name: label,
                    selector: selector,
                    type: `<${tag}${type ? ' type="' + type + '"' : ''}>`,
                    raw_text: text
                });
            });
            return results;
        }""")

        browser.close()

    # Deduplicate by selector
    seen = set()
    for item in raw_elements:
        sel = item["selector"]
        if sel and sel not in seen and not sel.startswith(".ng-") and len(sel) < 60:
            seen.add(sel)
            elements.append(item)

    return elements


def format_markdown_table(elements: List[Dict[str, str]]) -> str:
    """Formats elements into a standardized Markdown locator reference table."""
    lines = [
        "## 🔍 Locators đã xác minh qua BSK (Browser-Skill Reconnaissance)",
        "| Tên Phần Tử | Nhãn Hiển Thị | Selector / ID Thực Tế | Loại Phần Tử |",
        "| :--- | :--- | :--- | :--- |",
    ]
    for el in elements[:20]:  # Top 20 relevant elements
        name = el["name"].replace("|", "\\|")
        sel = f"`{el['selector']}`"
        el_type = f"`{el['type']}`"
        lines.append(f"| {name} | {name} | {sel} | {el_type} |")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Extract verified DOM locators into Markdown specs")
    parser.add_argument("--url", required=True, help="URL or relative HTML file path to inspect")
    parser.add_argument("--output", help="Optional Markdown file to append/save to")
    args = parser.parse_args()

    workspace_dir = Path(__file__).resolve().parent.parent
    elements = inspect_page_elements(args.url, workspace_dir)
    table_md = format_markdown_table(elements)

    print("\n" + "="*70)
    print("✨ BSK RECONNAISSANCE LOCATOR TABLE")
    print("="*70)
    print(table_md)
    print("="*70)

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(table_md + "\n", encoding="utf-8")
        print(f"\n[+] Saved locator table to: {out_path}")


if __name__ == "__main__":
    main()
