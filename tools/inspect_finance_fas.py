#!/usr/bin/env python3
"""
Deep DOM Inspector for Admin Portal Finance and FAS modules.
"""
import json
import os
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright, Page

BASE_URL = "http://localhost:5173"

def login(page: Page, email: str = "admin@IAM.edu.vn"):
    page.goto(f"{BASE_URL}/login", wait_until="networkidle", timeout=15000)
    if "login" not in page.url:
        print(f"Already logged in. URL: {page.url}", flush=True)
        return
    btn = page.locator("button:has-text('Sign in with Microsoft')")
    if btn.count() > 0:
        btn.click()
        page.wait_for_selector(f".account-tile:has-text('{email}'), [onclick*='{email}']", timeout=15000)
        tile = page.locator(f".account-tile:has-text('{email}'), [onclick*='{email}']")
        tile.first.click()
        page.wait_for_selector('nav, header, [aria-label*="Language"]', timeout=15000)
    print(f"Logged in as {email}. Current URL: {page.url}", flush=True)

def inspect_current_dom(page: Page) -> dict:
    return page.evaluate("""() => {
        const results = {
            url: window.location.href,
            pathname: window.location.pathname,
            title: document.title,
            headings: Array.from(document.querySelectorAll('h1, h2, h3')).map(h => ({
                tag: h.tagName.toLowerCase(),
                text: (h.innerText || h.textContent || '').trim(),
                id: h.id || ''
            })),
            inputs: [],
            selects: [],
            buttons: [],
            tables: [],
            dialogs: [],
            alerts: [],
            badges: []
        };

        function getBestSelector(el, tag) {
            const testId = el.getAttribute('data-testid');
            if (testId) return `[data-testid="${testId}"]`;
            const id = el.id;
            if (id && !id.startsWith('_r_') && !id.startsWith(':r')) return `#${id}`;
            const name = el.getAttribute('name');
            if (name) return `${tag}[name="${name}"]`;
            const ariaLabel = el.getAttribute('aria-label');
            if (ariaLabel) return `${tag}[aria-label="${ariaLabel}"]`;
            const text = (el.innerText || el.textContent || '').trim().split('\\n')[0].substring(0, 35);
            if (tag === 'button' && text) return `button:has-text("${text}")`;
            const placeholder = el.getAttribute('placeholder');
            if (placeholder) return `${tag}[placeholder*="${placeholder}"]`;
            return tag;
        }

        // Inputs
        document.querySelectorAll('input, textarea').forEach(el => {
            const tag = el.tagName.toLowerCase();
            const type = el.getAttribute('type') || 'text';
            const name = el.getAttribute('name') || '';
            const id = el.id || '';
            const placeholder = el.getAttribute('placeholder') || '';
            const disabled = el.disabled || el.getAttribute('aria-disabled') === 'true';
            const required = el.required || el.getAttribute('aria-required') === 'true';
            let label = '';
            if (id) {
                const labelEl = document.querySelector(`label[for="${id}"]`);
                if (labelEl) label = labelEl.innerText.trim();
            }
            if (!label && el.closest('label')) label = el.closest('label').innerText.trim();
            results.inputs.push({
                tag, type, name, id, placeholder, label, disabled, required,
                selector: getBestSelector(el, tag)
            });
        });

        // Selects
        document.querySelectorAll('select, [role="combobox"]').forEach(el => {
            const tag = el.tagName.toLowerCase();
            const name = el.getAttribute('name') || '';
            const id = el.id || '';
            let options = [];
            if (tag === 'select') {
                options = Array.from(el.options).map(o => ({ value: o.value, text: o.text.trim() }));
            }
            let label = '';
            if (id) {
                const labelEl = document.querySelector(`label[for="${id}"]`);
                if (labelEl) label = labelEl.innerText.trim();
            }
            results.selects.push({
                tag, name, id, label, options,
                selector: getBestSelector(el, tag)
            });
        });

        // Buttons
        document.querySelectorAll('button, [role="button"]').forEach(el => {
            const tag = el.tagName.toLowerCase();
            const text = (el.innerText || el.textContent || '').trim().split('\\n')[0].substring(0, 45);
            const type = el.getAttribute('type') || 'button';
            const disabled = el.disabled || el.getAttribute('aria-disabled') === 'true';
            const ariaLabel = el.getAttribute('aria-label') || '';
            results.buttons.push({
                text: text || ariaLabel,
                type, disabled,
                selector: getBestSelector(el, tag)
            });
        });

        // Tables
        document.querySelectorAll('table').forEach(table => {
            const headers = Array.from(table.querySelectorAll('th')).map(th => th.innerText.trim());
            const rowCount = table.querySelectorAll('tbody tr').length;
            results.tables.push({
                headers,
                rowCount,
                caption: table.querySelector('caption')?.innerText?.trim() || ''
            });
        });

        // Dialogs
        document.querySelectorAll('[role="dialog"], [role="alertdialog"], dialog').forEach(d => {
            results.dialogs.push({
                title: d.querySelector('h2, h3, [class*="title"]')?.innerText?.trim() || '',
                text: d.innerText?.trim()?.substring(0, 100) || '',
                isOpen: true
            });
        });

        // Alerts
        document.querySelectorAll('[role="alert"], [class*="alert"]').forEach(a => {
            results.alerts.push({
                text: a.innerText?.trim()?.substring(0, 100) || ''
            });
        });

        return results;
    }""")

def run_recon():
    out_dir = Path("specs/ui_bsk/localhost-5173/finance-and-fas/raw_inspections")
    out_dir.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        # 1. MOEHQ Admin Session
        context_admin = browser.new_context(viewport={"width": 1440, "height": 900})
        page_admin = context_admin.new_page()
        login(page_admin, "admin@IAM.edu.vn")

        routes_admin = [
            ("01_education_accounts", "/education-accounts"),
            ("02_top_up_list", "/top-up"),
            ("02_top_up_campaigns_new", "/top-up/campaigns/new"),
            ("03_fee_management", "/fee-management"),
            ("03_fee_components", "/fee-management/components"),
            ("03_fee_components_new", "/fee-management/components/new"),
            ("04_fee_batches", "/fee-batches"),
            ("05_moe_fas_list", "/moe-hq/moe-fas"),
            ("05_moe_fas_new", "/moe-hq/moe-fas/new"),
            ("07_fas_application_management", "/fas-application-management"),
        ]

        for name, route in routes_admin:
            try:
                print(f"Inspecting {name} ({route})...")
                page_admin.goto(f"{BASE_URL}{route}", wait_until="networkidle", timeout=12000)
                page_admin.wait_for_timeout(1000)
                dom_data = inspect_current_dom(page_admin)
                with open(out_dir / f"{name}.json", "w") as f:
                    json.dump(dom_data, f, indent=2)
            except Exception as e:
                print(f"Error inspecting {name}: {e}")

        # Check detail links from tables to get real IDs
        # Top-up campaigns list tab
        page_admin.goto(f"{BASE_URL}/top-up?tab=campaigns", wait_until="networkidle")
        page_admin.wait_for_timeout(1000)
        dom_data = inspect_current_dom(page_admin)
        with open(out_dir / "02_top_up_campaigns_tab.json", "w") as f:
            json.dump(dom_data, f, indent=2)

        # Check top-up history tab
        page_admin.goto(f"{BASE_URL}/top-up?tab=history", wait_until="networkidle")
        page_admin.wait_for_timeout(1000)
        dom_data = inspect_current_dom(page_admin)
        with open(out_dir / "02_top_up_history_tab.json", "w") as f:
            json.dump(dom_data, f, indent=2)

        # 2. SCHOOL Staff Session (staff1@IAM.edu.vn)
        context_school = browser.new_context(viewport={"width": 1440, "height": 900})
        page_school = context_school.new_page()
        login(page_school, "staff1@IAM.edu.vn")

        routes_school = [
            ("06_sbfas_schemes", "/sbfas-schemes"),
            ("06_sbfas_schemes_new", "/sbfas-schemes/new"),
        ]

        for name, route in routes_school:
            try:
                print(f"Inspecting {name} ({route})...")
                page_school.goto(f"{BASE_URL}{route}", wait_until="networkidle", timeout=12000)
                page_school.wait_for_timeout(1000)
                dom_data = inspect_current_dom(page_school)
                with open(out_dir / f"{name}.json", "w") as f:
                    json.dump(dom_data, f, indent=2)
            except Exception as e:
                print(f"Error inspecting {name}: {e}")

        browser.close()
        print("Reconnaissance complete! Saved to:", out_dir)

if __name__ == "__main__":
    run_recon()
