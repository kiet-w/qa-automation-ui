#!/usr/bin/env python3
"""
md_runner.py - Lean Markdown-First UI Automation Testing Engine.

Allows QA Engineers and AI agents to define end-to-end UI tests purely in Markdown (.md),
automatically executing them via Playwright with smart locators, recording video and screenshots,
and generating self-contained interactive HTML dashboards.

Usage:
    python3 md_runner.py [specs_path] [--headed] [--slowmo 200] [--open-report]
"""

import argparse
import datetime
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Auto re-execute with local .venv if system python lacks Playwright
try:
    import playwright
except ImportError:
    venv_py = Path(__file__).resolve().parent / ".venv" / "bin" / "python"
    if venv_py.exists():
        os.execv(str(venv_py), [str(venv_py)] + sys.argv)
    else:
        print("[Error] Playwright is not installed. Run: pip install playwright && playwright install chromium")
        sys.exit(1)

from playwright.sync_api import Browser, BrowserContext, Page, expect, sync_playwright


# ==============================================================================
# 1. MARKDOWN SPEC PARSER
# ==============================================================================

class Step:
    def __init__(self, action: str, target: str = "", value: str = "", expected: str = "", raw_line: str = ""):
        self.action = action.strip().lower()
        self.target = target.strip()
        self.value = value.strip()
        self.expected = expected.strip()
        self.raw_line = raw_line.strip()

    def __repr__(self):
        return f"Step({self.action}, target='{self.target}', val='{self.value}', exp='{self.expected}')"


class Scenario:
    def __init__(self, title: str, tc_id: str = ""):
        self.raw_title = title
        self.tags = re.findall(r"@[\w-]+", title)
        self.title = re.sub(r"@[\w-]+", "", title).strip()
        self.tc_id = tc_id or self._extract_id(self.title)
        self.steps: List[Step] = []
        tags_lower = [t.lower() for t in self.tags]
        self.is_uat = "@uat" in tags_lower
        self.is_break_it = "@break_it" in tags_lower or "@break" in tags_lower or "@adversarial" in tags_lower
        self.is_integration = "@integration" in tags_lower or "@api" in tags_lower or "@contract" in tags_lower

    def _extract_id(self, title: str) -> str:
        m = re.search(r"((?:TC|TS|US|SC|BRK)[_-]?\d+[a-z0-9_-]*)", title, re.IGNORECASE)
        if m:
            return m.group(1).upper().replace("_", "-")
        return "TC-" + hashlib.md5(title.encode()).hexdigest()[:4].upper()


class FeatureSpec:
    def __init__(self, title: str, file_path: Path):
        self.title = title
        self.file_path = file_path
        self.scenarios: List[Scenario] = []


def parse_markdown_spec(md_path: Path) -> FeatureSpec:
    """Parses a markdown test specification supporting both natural bullet steps and data tables."""
    content = md_path.read_text(encoding="utf-8")
    lines = content.splitlines()

    feature_title = md_path.stem.replace("_", " ").title()
    spec = FeatureSpec(title=feature_title, file_path=md_path)

    current_scenario: Optional[Scenario] = None
    table_mode = False
    table_headers: List[str] = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            table_mode = False
            continue

        # Header 1: Feature Title
        if stripped.startswith("# ") and not stripped.startswith("## "):
            feature_title = stripped.lstrip("#").strip()
            if feature_title.lower().startswith("feature:"):
                feature_title = feature_title[8:].strip()
            spec.title = feature_title
            continue

        # Header 2 or 3: Scenario Definition
        if stripped.startswith("## ") or stripped.startswith("### "):
            sc_raw = stripped.lstrip("#").strip()
            lower_sc = sc_raw.lower()
            if lower_sc.startswith(("scenario:", "test case:", "tc-", "uat-", "ts-", "sc-", "hp-", "brk-")):
                if lower_sc.startswith("scenario:"):
                    sc_raw = sc_raw[9:].strip()
                elif lower_sc.startswith("test case:"):
                    sc_raw = sc_raw[10:].strip()

                current_scenario = Scenario(title=sc_raw)
                spec.scenarios.append(current_scenario)
                table_mode = False
                continue
            else:
                # Informational / Documentation section (e.g. ## Locators đã xác minh...)
                current_scenario = None
                table_mode = False
                continue

        if current_scenario is None:
            # Auto-create default scenario if steps appear before scenario header
            current_scenario = Scenario(title="Default Scenario")
            spec.scenarios.append(current_scenario)

        # Markdown Table Detection
        if stripped.startswith("|") and stripped.endswith("|"):
            parts = [p.strip() for p in stripped.strip("|").split("|")]
            # Check if separator row (e.g. | :--- | :--- |)
            if all(set(p).issubset({"-", ":", " "}) for p in parts):
                continue

            lower_parts = [p.lower() for p in parts]
            if any("action" in h or "hành động" in h for h in lower_parts):
                table_mode = True
                canonical_headers = []
                for h in lower_parts:
                    if "action" in h or "hành động" in h:
                        canonical_headers.append("action")
                    elif "target" in h or "selector" in h or "phần tử" in h or "nhãn" in h:
                        canonical_headers.append("target")
                    elif "value" in h or "dữ liệu" in h or "nhập" in h:
                        canonical_headers.append("value")
                    elif "expected" in h or "kỳ vọng" in h or "assertion" in h:
                        canonical_headers.append("expected")
                    elif "step" in h or "bước" in h:
                        canonical_headers.append("step")
                    else:
                        canonical_headers.append(h)
                table_headers = canonical_headers
                continue

            if table_mode and table_headers:
                row_dict = {table_headers[i]: parts[i] if i < len(parts) else "" for i in range(len(table_headers))}
                act = (row_dict.get("action") or "").lower()
                tgt = (row_dict.get("target") or "")
                val = (row_dict.get("value") or "")
                exp = (row_dict.get("expected") or "")

                if act:
                    current_scenario.steps.append(Step(action=act, target=tgt, value=val, expected=exp, raw_line=stripped))
                continue

        # Natural Bullet List Detection: - Action: Target with Value
        if stripped.startswith("- ") or stripped.startswith("* "):
            step_text = stripped[2:].strip()
            step_obj = _parse_natural_step(step_text, raw_line=stripped)
            if step_obj:
                current_scenario.steps.append(step_obj)
            continue

    # Filter out any scenarios without executable steps (e.g. documentation sections)
    spec.scenarios = [s for s in spec.scenarios if len(s.steps) > 0]
    return spec


def _parse_natural_step(text: str, raw_line: str) -> Optional[Step]:
    """Parses natural language step syntax."""
    # Pattern: Open: <url>
    m_open = re.match(r"^(?:Open|Mở|Goto|Navigate to|Truy cập):\s*(.+)$", text, re.I)
    if m_open:
        return Step(action="open", target=m_open.group(1).strip(), raw_line=raw_line)

    # Pattern: Fill / Nhập: <target> with "<val>"
    m_fill = re.match(r"^(?:Fill|Nhập|Type|Gõ):\s*(.*?)\s+(?:with|với|bằng|=)\s+[\"']?(.*?)[\"']?$", text, re.I)
    if m_fill:
        return Step(action="fill", target=m_fill.group(1).strip(), value=m_fill.group(2).strip(), raw_line=raw_line)

    # Pattern: Click / Bấm: <target>
    m_click = re.match(r"^(?:Click|Bấm|Chọn|Nhấp):\s*(.+)$", text, re.I)
    if m_click:
        return Step(action="click", target=m_click.group(1).strip(), raw_line=raw_line)

    # Pattern: Double click: <target>
    m_dbl = re.match(r"^(?:Double click|Nhấp đúp):\s*(.+)$", text, re.I)
    if m_dbl:
        return Step(action="dblclick", target=m_dbl.group(1).strip(), raw_line=raw_line)

    # Pattern: Select / Chọn option: <target> with "<val>"
    m_sel = re.match(r"^(?:Select|Chọn option):\s*(.*?)\s+(?:with|với|=)\s+[\"']?(.*?)[\"']?$", text, re.I)
    if m_sel:
        return Step(action="select", target=m_sel.group(1).strip(), value=m_sel.group(2).strip(), raw_line=raw_line)

    # Pattern: Check / Đánh dấu: <target>
    m_chk = re.match(r"^(?:Check|Đánh dấu|Tick):\s*(.+)$", text, re.I)
    if m_chk:
        return Step(action="check", target=m_chk.group(1).strip(), raw_line=raw_line)

    # Pattern: Uncheck: <target>
    m_unchk = re.match(r"^(?:Uncheck|Bỏ chọn):\s*(.+)$", text, re.I)
    if m_unchk:
        return Step(action="uncheck", target=m_unchk.group(1).strip(), raw_line=raw_line)

    # Pattern: Press: "<key>"
    m_key = re.match(r"^(?:Press|Nhấn phím):\s*[\"']?([a-zA-Z0-9_-]+)[\"']?$", text, re.I)
    if m_key:
        return Step(action="press", value=m_key.group(1).strip(), raw_line=raw_line)

    # Pattern: Wait: <time>
    m_wait = re.match(r"^(?:Wait|Chờ):\s*(.+)$", text, re.I)
    if m_wait:
        return Step(action="wait", value=m_wait.group(1).strip(), raw_line=raw_line)

    # Pattern: Assert / Kiểm tra: <target> <condition>
    m_assert = re.match(r"^(?:Assert|Kiểm tra|Verify):\s*(.+)$", text, re.I)
    if m_assert:
        raw_cond = m_assert.group(1).strip()
        # Parse common sub-patterns
        # Case A: URL contains / Title contains
        m_url = re.match(r"^URL\s+contains\s+[\"']?(.*?)[\"']?$", raw_cond, re.I)
        if m_url:
            return Step(action="assert_url", value=m_url.group(1), raw_line=raw_line)
        m_title = re.match(r"^Title\s+contains\s+[\"']?(.*?)[\"']?$", raw_cond, re.I)
        if m_title:
            return Step(action="assert_title", value=m_title.group(1), raw_line=raw_line)

        # Case B: <target> is visible / not visible
        m_vis = re.match(r"^(.*?)\s+is\s+(visible|hiển thị)$", raw_cond, re.I)
        if m_vis:
            return Step(action="assert_visible", target=m_vis.group(1), raw_line=raw_line)
        m_invis = re.match(r"^(.*?)\s+is\s+(not visible|ẩn|không hiển thị)$", raw_cond, re.I)
        if m_invis:
            return Step(action="assert_not_visible", target=m_invis.group(1), raw_line=raw_line)

        # Case C: <target> contains "<text>"
        m_contains = re.match(r"^(.*?)\s+(?:contains|chứa)\s+[\"']?(.*?)[\"']?$", raw_cond, re.I)
        if m_contains:
            return Step(action="assert_contains", target=m_contains.group(1), value=m_contains.group(2), raw_line=raw_line)

        # Case D: <target> is disabled / enabled
        m_dis = re.match(r"^(.*?)\s+is\s+(disabled|bị vô hiệu)$", raw_cond, re.I)
        if m_dis:
            return Step(action="assert_disabled", target=m_dis.group(1), raw_line=raw_line)
        m_en = re.match(r"^(.*?)\s+is\s+(enabled|hoạt động)$", raw_cond, re.I)
        if m_en:
            return Step(action="assert_enabled", target=m_en.group(1), raw_line=raw_line)

        # Case E: Technical health & visual asserts
        if raw_cond.lower() in ("no_console_errors", "no console errors", "0 console errors"):
            return Step(action="assert_no_console_errors", raw_line=raw_line)
        if raw_cond.lower() in ("no_overflow", "no overflow", "no horizontal overflow"):
            return Step(action="assert_no_overflow", raw_line=raw_line)

        # Generic assert fallback
        return Step(action="assert", target=raw_cond, raw_line=raw_line)

    return None


# ==============================================================================
# 2. SMART LOCATOR & RUNNER ENGINE
# ==============================================================================

class PlaywrightSmartRunner:
    def __init__(self, workspace_dir: Path, headed: bool = False, slow_mo: int = 0, base_url: str = ""):
        self.workspace_dir = workspace_dir
        self.headed = headed
        self.slow_mo = slow_mo
        self.base_url = base_url or f"file://{workspace_dir.resolve()}"
        self.reports_dir = workspace_dir / "reports" / "uat"
        self.test_results_dir = self.reports_dir / "test-results"
        self.screenshots_dir = self.reports_dir / "screenshots"

        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.test_results_dir.mkdir(parents=True, exist_ok=True)
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)

    def resolve_locator(self, page: Page, target: str, action: str = "click"):
        """Resolves target into Playwright locator with smart user-facing heuristic."""
        clean = target.strip().strip("\"'").strip()
        if not clean:
            raise ValueError(f"Target selector or label cannot be empty for action '{action}'")

        # Check if technical selector
        is_technical = (
            clean.startswith("#")
            or clean.startswith(".")
            or clean.startswith("//")
            or clean.startswith("xpath=")
            or clean.startswith("css=")
            or "[" in clean
            or ":has-text(" in clean
            or ":has(" in clean
            or ">" in clean
            or ":nth-" in clean
        )
        if is_technical:
            return page.locator(clean).first

        # User-facing text / role heuristic
        esc_pattern = re.compile(re.escape(clean), re.IGNORECASE)

        if action in ("click", "dblclick"):
            # Try button or link role first
            btn = page.get_by_role("button", name=esc_pattern)
            if btn.count() > 0:
                return btn.first
            link = page.get_by_role("link", name=esc_pattern)
            if link.count() > 0:
                return link.first

        if action in ("fill", "select"):
            # Try label, placeholder
            lbl = page.get_by_label(esc_pattern)
            if lbl.count() > 0:
                return lbl.first
            ph = page.get_by_placeholder(esc_pattern)
            if ph.count() > 0:
                return ph.first

        # General text locator fallback
        by_txt = page.get_by_text(esc_pattern)
        if by_txt.count() > 0:
            return by_txt.first

        # Safe fallback: get_by_text exact or attribute query if identifier-safe
        if re.match(r"^[a-zA-Z0-9_-]+$", clean):
            return page.locator(f"[data-testid='{clean}'], [id='{clean}'], [name='{clean}']").first

        return page.get_by_text(clean).first

    def execute_scenario(
        self,
        browser: Browser,
        spec: FeatureSpec,
        scenario: Scenario,
        run_id: str,
        sc_index: int,
    ) -> Dict[str, Any]:
        """Executes a single scenario inside an isolated browser context with video and console error watchdogs."""
        scenario_slug = re.sub(r"[^a-zA-Z0-9_-]", "_", scenario.title.lower())
        tc_dir = self.test_results_dir / run_id / scenario_slug
        tc_dir.mkdir(parents=True, exist_ok=True)

        context = browser.new_context(
            record_video_dir=str(tc_dir),
            record_video_size={"width": 1280, "height": 720},
            viewport={"width": 1280, "height": 720},
        )
        page = context.new_page()
        page_holder = [page]

        def _attach_listeners(p: Page):
            p.on("dialog", lambda dialog: dialog.accept())
            p.on("console", lambda msg: console_errors.append(f"[{msg.type.upper()}] {msg.text}") if msg.type in ("error",) else None)
            p.on("pageerror", lambda err: console_errors.append(f"[UNCAUGHT] {err}"))
            p.on("response", lambda resp: network_errors.append(f"HTTP {resp.status} on {resp.url}") if resp.status >= 400 else None)

        def _on_new_page(new_p: Page):
            _attach_listeners(new_p)
            page_holder[0] = new_p

        context.on("page", _on_new_page)
        _attach_listeners(page)

        console_errors: List[str] = []
        network_errors: List[str] = []

        recorded_steps: List[Dict[str, Any]] = []
        scenario_start = time.time()
        tc_passed = True
        err_msg = None
        err_trace = None

        print(f"\n  ▶ Running Scenario [{scenario.tc_id}]: {scenario.title}")

        for idx, step in enumerate(scenario.steps, start=1):
            s_start = time.time()
            step_title = step.raw_line or f"Step {idx}: {step.action} {step.target}"
            step_status = "passed"
            step_screenshot = None
            step_err = None

            try:
                self._run_single_step(page_holder, step, context=context, console_errors=console_errors)
                s_duration = time.time() - s_start
                print(f"    ✓ {step_title} ({s_duration:.2f}s)")
            except Exception as exc:
                s_duration = time.time() - s_start
                step_status = "failed"
                tc_passed = False
                err_msg = str(exc)
                err_trace = str(exc)
                step_err = err_msg

                # Capture failure screenshot
                ss_name = f"{scenario_slug}_step_{idx}_fail.png"
                ss_path = self.screenshots_dir / ss_name
                try:
                    active_p = page_holder[0] if (page_holder and not page_holder[0].is_closed()) else (context.pages[-1] if context.pages else None)
                    if active_p:
                        active_p.screenshot(path=str(ss_path), full_page=True)
                        step_screenshot = ss_name
                except Exception:
                    pass

                print(f"    ✗ {step_title} FAILED: {exc}")
                recorded_steps.append({
                    "title": step_title,
                    "status": step_status,
                    "duration": s_duration,
                    "screenshot": step_screenshot,
                    "error": step_err,
                })
                break

            recorded_steps.append({
                "title": step_title,
                "status": step_status,
                "duration": s_duration,
                "screenshot": step_screenshot,
                "error": None,
            })

        # Finalize and close context to save video
        page.close()
        context.close()

        tc_duration = time.time() - scenario_start

        # Locate recorded video
        video_files = list(tc_dir.glob("*.webm"))
        video_rel = f"reports/test-results/{run_id}/{scenario_slug}/{video_files[0].name}" if video_files else None

        return {
            "nodeid": f"{spec.file_path.name}::{scenario.title}",
            "outcome": "passed" if tc_passed else "failed",
            "duration": tc_duration,
            "metadata": {
                "jira_id": scenario.tc_id,
                "suite": spec.title,
                "scenario": scenario.title,
                "tags": scenario.tags,
                "is_uat": scenario.is_uat,
                "is_break_it": scenario.is_break_it,
                "is_integration": scenario.is_integration,
                "user_story": spec.title,
                "video_path": video_rel,
                "steps": recorded_steps,
                "console_errors": console_errors,
                "network_errors": network_errors,
            },
            "call": {
                "crash": {"message": err_msg} if err_msg else {},
                "longrepr": err_trace if err_trace else "",
            },
        }

    def _run_single_step(
        self,
        page_or_holder: Any,
        step: Step,
        context: Optional[BrowserContext] = None,
        console_errors: Optional[List[str]] = None,
    ):
        """Executes one step against the active page, supporting cross-page navigation & tabs."""
        if isinstance(page_or_holder, list):
            page_holder = page_or_holder
            page = page_holder[0]
        else:
            page_holder = [page_or_holder]
            page = page_or_holder

        act = step.action

        # --- NAVIGATION & CROSS-PAGE FLOW ---
        if act in ("open", "goto"):
            url = step.target or step.value
            if not url.startswith("http://") and not url.startswith("https://") and not url.startswith("file://"):
                url = f"{self.base_url.rstrip('/')}/{url.lstrip('/')}"

            # Pre-authenticate if opening a protected portal page
            if (":5174" in url or "localhost" in url) and "/parent/login" not in url:
                page.goto("http://localhost:5174/parent/login", wait_until="load", timeout=10000)
                try:
                    sp_btn = page.locator("button:has-text('Sign in with Singpass')").first
                    sp_btn.wait_for(state="visible", timeout=5000)
                    sp_btn.click()
                    page.wait_for_selector("button:has-text('Log in with Singpass')", timeout=10000)
                    page.click("button:has-text('Log in with Singpass')")
                    page.wait_for_url(lambda u: "/parent/callback" not in u and ":5156" not in u, timeout=10000)
                except Exception as e:
                    print(f"    [Auth Warning] {e}")

            page.goto(url, wait_until="load", timeout=10000)
            if "profile" in url.lower():
                try:
                    loading = page.locator("p[role='status']:has-text('Loading')")
                    if loading.count() > 0:
                        loading.wait_for(state="detached", timeout=15000)
                    page.wait_for_selector("button:has-text('Update details'), button:has-text('Save changes')", timeout=15000)
                except Exception:
                    pass
            return

        if act in ("auth_singpass", "login_singpass"):
            persona = step.value or step.target or "TAN WEI MING"
            page.goto("http://localhost:5174/parent/login", wait_until="load", timeout=10000)
            if page.locator("button:has-text('Sign in with Singpass')").count() > 0:
                page.click("button:has-text('Sign in with Singpass')")
                page.wait_for_selector("button:has-text('Log in with Singpass')", timeout=10000)
                if persona:
                    page.evaluate("""(p) => {
                        const sel = document.querySelector('select');
                        if (!sel) return;
                        const opt = Array.from(sel.options).find(o => o.text.includes(p) || o.value.includes(p));
                        if (opt) {
                            sel.value = opt.value;
                            sel.dispatchEvent(new Event('change', { bubbles: true }));
                        }
                    }""", persona)
                page.click("button:has-text('Log in with Singpass')")
                page.wait_for_timeout(2000)
            return

        if act in ("back", "go_back"):
            page.go_back(wait_until="load", timeout=10000)
            return

        if act in ("forward", "go_forward"):
            page.go_forward(wait_until="load", timeout=10000)
            return

        if act in ("reload", "refresh"):
            page.reload(wait_until="load", timeout=10000)
            return

        # --- MULTI-TAB & WINDOW SWITCHING ---
        if act in ("switch_tab", "switch_page", "switch_window") and context:
            target_val = (step.value or step.target or "next").lower().strip()
            pages = context.pages
            if target_val in ("next", "last", "new"):
                page_holder[0] = pages[-1]
            elif target_val in ("first", "main", "parent", "0"):
                page_holder[0] = pages[0]
            elif target_val.isdigit():
                idx = int(target_val) - 1
                if 0 <= idx < len(pages):
                    page_holder[0] = pages[idx]
            page_holder[0].bring_to_front()
            return

        if act in ("close_tab", "close_page") and context:
            page.close()
            if context.pages:
                page_holder[0] = context.pages[-1]
                page_holder[0].bring_to_front()
            return

        if act in ("set_viewport", "viewport"):
            vp_str = step.target or step.value or "1280x720"
            parts = vp_str.lower().split("x")
            page.set_viewport_size({"width": int(parts[0]), "height": int(parts[1])})
            return

        # --- STANDARD INTERACTIONS ---
        if act == "fill":
            loc = self.resolve_locator(page, step.target, action="fill")
            loc.fill(step.value, timeout=10000)
            return

        if act == "click":
            loc = self.resolve_locator(page, step.target, action="click")
            loc.click(timeout=10000)
            return

        if act == "dblclick":
            loc = self.resolve_locator(page, step.target, action="dblclick")
            loc.dblclick(timeout=5000)
            return

        if act == "select":
            loc = self.resolve_locator(page, step.target, action="select")
            try:
                loc.select_option(label=step.value, timeout=3000)
            except Exception:
                loc.select_option(value=step.value, timeout=3000)
            return

        if act == "check":
            loc = self.resolve_locator(page, step.target, action="check")
            loc.check(timeout=5000)
            return

        if act == "uncheck":
            loc = self.resolve_locator(page, step.target, action="uncheck")
            loc.uncheck(timeout=5000)
            return

        if act == "press":
            key = step.value or step.target
            page.keyboard.press(key)
            return

        if act == "wait":
            val_str = step.value or step.target or "1s"
            if val_str.endswith("ms"):
                ms = int(val_str[:-2])
            elif val_str.endswith("s"):
                ms = int(float(val_str[:-1]) * 1000)
            else:
                ms = int(float(val_str) * 1000)
            page.wait_for_timeout(ms)
            return

        # --- ADVERSARIAL & BREAK_IT ACTIONS ---
        if act in ("strip_constraints", "bypass_client", "remove_constraints"):
            page.evaluate("""() => {
                document.querySelectorAll('input, select, textarea, button').forEach(el => {
                    el.removeAttribute('required');
                    el.removeAttribute('disabled');
                    el.removeAttribute('maxlength');
                    el.removeAttribute('pattern');
                    el.removeAttribute('min');
                    el.removeAttribute('max');
                    el.removeAttribute('readonly');
                    el.disabled = false;
                    el.readOnly = false;
                });
            }""")
            return

        if act in ("force_fill", "force_set"):
            loc_str = step.target
            val = step.value
            page.evaluate("""([sel, val]) => {
                let el = document.querySelector(sel);
                if (!el) {
                    el = document.querySelector(`[name="${sel}"]`) || document.querySelector(`[data-testid="${sel}"]`);
                }
                if (el) {
                    el.removeAttribute('disabled');
                    el.removeAttribute('readonly');
                    el.removeAttribute('maxlength');
                    const prototype = el instanceof HTMLTextAreaElement ? window.HTMLTextAreaElement.prototype : window.HTMLInputElement.prototype;
                    const setter = Object.getOwnPropertyDescriptor(prototype, 'value')?.set;
                    if (setter) {
                        setter.call(el, val);
                    } else {
                        el.value = val;
                    }
                    el.dispatchEvent(new Event('input', { bubbles: true }));
                    el.dispatchEvent(new Event('change', { bubbles: true }));
                } else {
                    throw new Error(`Element not found for force_fill: ${sel}`);
                }
            }""", [loc_str, val])
            return

        if act in ("enable", "enable_element"):
            page.evaluate("""(sel) => {
                const el = document.querySelector(sel);
                if (el) {
                    el.removeAttribute('disabled');
                    el.disabled = false;
                }
            }""", step.target)
            return

        if act in ("mock_status", "mock_error", "mock_500"):
            url_pattern = step.target or "**/api/**"
            status_code = int(step.value or 500)
            page.route(url_pattern, lambda route: route.fulfill(
                status=status_code,
                content_type="application/json",
                body=json.dumps({"error": "Simulated Chaos / Server Error", "status": status_code})
            ))
            return

        if act in ("mock_response", "mock_json"):
            url_pattern = step.target or "**/api/**"
            body_val = step.value or "{}"
            try:
                body_data = json.loads(body_val)
            except Exception:
                body_data = {"data": body_val}
            page.route(url_pattern, lambda route: route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps(body_data)
            ))
            return

        # --- ASSERTIONS ---
        if act == "assert_url":
            expect(page).to_have_url(re.compile(re.escape(step.value)), timeout=5000)
            return

        if act == "assert_title":
            expect(page).to_have_title(re.compile(re.escape(step.value)), timeout=5000)
            return

        if act == "assert_visible":
            loc = self.resolve_locator(page, step.target)
            expect(loc).to_be_visible(timeout=5000)
            return

        if act == "assert_not_visible":
            loc = self.resolve_locator(page, step.target)
            expect(loc).not_to_be_visible(timeout=5000)
            return

        if act == "assert_contains":
            loc = self.resolve_locator(page, step.target)
            expect(loc).to_contain_text(step.value, timeout=5000)
            return

        if act == "assert_disabled":
            loc = self.resolve_locator(page, step.target)
            expect(loc).to_be_disabled(timeout=5000)
            return

        if act == "assert_enabled":
            loc = self.resolve_locator(page, step.target)
            expect(loc).to_be_enabled(timeout=5000)
            return

        if act in ("assert_no_overflow", "no_overflow"):
            has_overflow = page.evaluate("() => document.documentElement.scrollWidth > document.documentElement.clientWidth")
            if has_overflow:
                raise AssertionError("Horizontal overflow (scrollWidth > clientWidth) detected!")
            return

        if act in ("assert_no_console_errors", "no_console_errors"):
            if console_errors:
                raise AssertionError(f"Uncaught console errors detected ({len(console_errors)}): " + "; ".join(console_errors[:2]))
            return

        # Table-driven or fallback assert
        if act in ("assert", "verify"):
            exp_text = step.expected or step.value
            loc = self.resolve_locator(page, step.target)
            if "visible" in exp_text.lower():
                expect(loc).to_be_visible(timeout=5000)
            elif "disabled" in exp_text.lower():
                expect(loc).to_be_disabled(timeout=5000)
            elif "enabled" in exp_text.lower():
                expect(loc).to_be_enabled(timeout=5000)
            elif "contains" in exp_text.lower():
                m = re.search(r"contains\s+[\"']?(.*?)[\"']?$", exp_text, re.I)
                txt = m.group(1) if m else exp_text
                expect(loc).to_contain_text(txt, timeout=5000)
            else:
                expect(loc).to_be_visible(timeout=5000)
            return

        raise ValueError(f"Unknown action: '{act}' in step: {step.raw_line}")


# ==============================================================================
# 3. CLI & ORCHESTRATOR
# ==============================================================================

def discover_specs(paths: List[str], workspace_dir: Path) -> List[Path]:
    """Finds all markdown specification files matching given paths or defaults to test_specs/."""
    specs: List[Path] = []
    candidates = paths if paths else ["test_specs"]

    for c in candidates:
        p = (workspace_dir / c) if not Path(c).is_absolute() else Path(c)
        if p.is_file() and p.suffix.lower() == ".md":
            specs.append(p)
        elif p.is_dir():
            for f in sorted(p.glob("**/*.md")):
                if f.name.lower() != "readme.md" and not f.name.startswith((".", "_")):
                    specs.append(f)

    return specs


def run_all_specs(
    spec_paths: List[Path],
    workspace_dir: Path,
    tags: Optional[List[str]] = None,
    headed: bool = False,
    slow_mo: int = 0,
    open_report: bool = False,
):
    """Main runner orchestrating Playwright execution, data recording, and HTML report compilation."""
    t_start = time.time()
    run_id = f"RUN-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}"

    print("=" * 70)
    print(f"🚀 Markdown-First UI Automation Testing Engine")
    print(f"   Run ID: {run_id}")
    print(f"   Specs Found: {len(spec_paths)}")
    if tags:
        print(f"   Tag Filter:  {', '.join(tags)}")
    print("=" * 70)

    if not spec_paths:
        print("[Warning] No .md test specs found. Please place markdown test files in test_specs/.")
        return

    runner = PlaywrightSmartRunner(workspace_dir=workspace_dir, headed=headed, slow_mo=slow_mo)

    all_test_results: List[Dict[str, Any]] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not headed, slow_mo=slow_mo)

        for spec_file in spec_paths:
            spec = parse_markdown_spec(spec_file)

            matching_scenarios = []
            for scenario in spec.scenarios:
                if tags:
                    sc_tags_lower = [t.lower().lstrip("@") for t in scenario.tags]
                    match = any(t.lower().lstrip("@") in sc_tags_lower for t in tags)
                    if not match:
                        continue
                matching_scenarios.append(scenario)

            if not matching_scenarios:
                continue

            print(f"\n📂 Feature: {spec.title} ({spec_file.relative_to(workspace_dir) if workspace_dir in spec_file.parents else spec_file.name})")

            for sc_idx, scenario in enumerate(matching_scenarios, start=1):
                res = runner.execute_scenario(browser, spec, scenario, run_id, sc_idx)
                all_test_results.append(res)

        browser.close()

    total_duration = time.time() - t_start
    passed_count = sum(1 for t in all_test_results if t["outcome"] == "passed")
    failed_count = sum(1 for t in all_test_results if t["outcome"] == "failed")
    total_count = len(all_test_results)
    pass_rate = round((passed_count / total_count) * 100, 1) if total_count > 0 else 0.0

    print("\n" + "=" * 70)
    print(f"📊 EXECUTION SUMMARY")
    print(f"   Total Scenarios: {total_count}")
    print(f"   Passed:          {passed_count}")
    print(f"   Failed:          {failed_count}")
    print(f"   Pass Rate:       {pass_rate}%")
    print(f"   Duration:        {total_duration:.2f}s")
    print("=" * 70)

    # Compile report.json
    report_json_path = runner.reports_dir / "report.json"
    report_payload = {
        "created": time.time(),
        "duration": total_duration,
        "run_id": run_id,
        "summary": {
            "total": total_count,
            "passed": passed_count,
            "failed": failed_count,
            "skipped": 0,
            "xfailed": 0,
            "xpassed": 0,
        },
        "tests": all_test_results,
    }

    with open(report_json_path, "w", encoding="utf-8") as f:
        json.dump(report_payload, f, indent=2)

    # Generate HTML Report using existing reporting package
    try:
        from reporting import ReportGenerator
        from reporting.clean_report import generate_clean_report

        generator = ReportGenerator(workspace_dir=workspace_dir)
        html_out = runner.reports_dir / "execution_report.html"
        generator.generate(json_path=report_json_path, output_html_path=html_out, embed_media=True)
        print(f"\n✨ Interactive ExtentReport Generated: {html_out}")

        clean_html_out = runner.reports_dir / "bao_cao_tinh_gon.html"
        generate_clean_report(json_path=report_json_path, output_html_path=clean_html_out)
        print(f"✨ Minimalist Clean Report:        {clean_html_out}")

        if open_report:
            import webbrowser
            webbrowser.open(clean_html_out.as_uri())
    except Exception as exc:
        print(f"[Warning] Failed to generate HTML report: {exc}")


def main():
    parser = argparse.ArgumentParser(description="Markdown-First UI Automation Testing Engine")
    parser.add_argument("specs", nargs="*", help="Markdown test specification paths or directory (default: test_specs/)")
    parser.add_argument("--tags", "-t", nargs="+", help="Filter scenarios by tag (e.g. --tags @smoke @p0 @uat)")
    parser.add_argument("--headed", action="store_true", help="Launch real visible browser instead of headless")
    parser.add_argument("--slowmo", type=int, default=0, help="Delay in milliseconds between actions")
    parser.add_argument("--open-report", action="store_true", help="Open generated HTML report automatically in browser")

    args = parser.parse_args()
    workspace_dir = Path(__file__).resolve().parent

    specs = discover_specs(args.specs, workspace_dir)
    run_all_specs(
        spec_paths=specs,
        workspace_dir=workspace_dir,
        tags=args.tags,
        headed=args.headed,
        slow_mo=args.slowmo,
        open_report=args.open_report,
    )


if __name__ == "__main__":
    main()
