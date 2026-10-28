"""
core/pytest_plugins/browser_engine.py - Multi-browser setup, anti-bot stealth, and launch fixtures.
Handles --target-browser (chromium, chrome, edge, brave, firefox, webkit) and custom binary detection.
"""
import os
from pathlib import Path
import re
import shutil
import sys
import time
from typing import Optional
import pytest
from playwright.sync_api import Locator, Page
from playwright_stealth import Stealth

REPO_ROOT = Path(__file__).resolve().parents[2]
WORKSPACE_DIR = REPO_ROOT
DEFAULT_REPORTS_DIR = WORKSPACE_DIR / "reports"
THANKS_PAGE = WORKSPACE_DIR / "docs" / "thanks.html"

_CURRENT_ACTIVE_NODE = None

# Patch Locator methods to capture action/input screenshot automatically ("lúc nhập xong / thực hiện")
_ORIG_LOCATOR_FILL = Locator.fill
_ORIG_LOCATOR_SELECT = Locator.select_option
_ORIG_LOCATOR_CHECK = Locator.check
_ORIG_LOCATOR_CLICK = Locator.click

_ORIG_PAGE_FILL = Page.fill
_ORIG_PAGE_SELECT = Page.select_option
_ORIG_PAGE_CHECK = Page.check
_ORIG_PAGE_CLICK = Page.click

def _capture_action_from_locator(locator, is_button: bool = False, action_type: str = "fill", value: str = ""):
    global _CURRENT_ACTIVE_NODE
    node = _CURRENT_ACTIVE_NODE
    if not node:
        return
    try:
        page = getattr(locator, "page", None)
        if not page or page.is_closed():
            return
        reports_dir = getattr(node.config, "_ticket_reports_dir", DEFAULT_REPORTS_DIR)
        test_slug = re.sub(r"[^\w]+", "_", node.name.lower()).strip("_")

        # 1. Test-specific folder: reports/screenshots/<test_slug>/
        test_screenshots_dir = Path(reports_dir) / "screenshots" / test_slug
        test_screenshots_dir.mkdir(parents=True, exist_ok=True)
        screenshots_dir = Path(reports_dir) / "screenshots"
        screenshots_dir.mkdir(parents=True, exist_ok=True)

        # 2. Highlight action element in browser DOM
        from core.evidence_annotator import EvidenceAnnotator
        act_name = "click" if is_button else action_type
        clean_val = str(value) if value is not None else ""
        EvidenceAnnotator.highlight_action_input(page, locator, value=clean_val, action_type=act_name)

        # 3. Determine action/step index
        action_counter = getattr(node, "_qa_action_counter", 0) + 1
        setattr(node, "_qa_action_counter", action_counter)

        # 4. Save step action screenshot
        action_file = test_screenshots_dir / f"step_{action_counter}_{act_name}.png"
        page.screenshot(path=str(action_file), full_page=False)

        # 5. Keep legacy action screenshot for backward compatibility
        legacy_action_file = screenshots_dir / f"{test_slug}_action.png"
        try:
            shutil.copy2(action_file, legacy_action_file)
        except Exception:
            pass

        try:
            rel_path = str(action_file.relative_to(WORKSPACE_DIR))
        except Exception:
            rel_path = str(action_file)

        step_screens = getattr(node, "_qa_step_screenshots", [])
        step_screens.append((action_counter, act_name, clean_val, rel_path))
        setattr(node, "_qa_step_screenshots", step_screens)
        setattr(node, "_qa_action_screenshot", rel_path)

        # 6. Clear overlay
        EvidenceAnnotator.clear_overlays(page)
    except Exception:
        pass

def _patched_locator_fill(self, *args, **kwargs):
    val = args[0] if args else kwargs.get("value", "")
    res = _ORIG_LOCATOR_FILL(self, *args, **kwargs)
    _capture_action_from_locator(self, action_type="fill", value=str(val))
    return res

def _patched_locator_select(self, *args, **kwargs):
    val = args[0] if args else (kwargs.get("value") or kwargs.get("label") or "")
    res = _ORIG_LOCATOR_SELECT(self, *args, **kwargs)
    _capture_action_from_locator(self, action_type="select", value=str(val))
    return res

def _patched_locator_check(self, *args, **kwargs):
    res = _ORIG_LOCATOR_CHECK(self, *args, **kwargs)
    _capture_action_from_locator(self, action_type="check", value="checked")
    return res

def _patched_locator_click(self, *args, **kwargs):
    tag = ""
    try:
        tag = self.evaluate("el => (el.tagName + ' ' + (el.type || '') + ' ' + (el.className || '') + ' ' + (el.innerText || '')).toLowerCase()")
    except Exception:
        pass
    res = _ORIG_LOCATOR_CLICK(self, *args, **kwargs)
    try:
        if any(w in tag for w in ("button", "submit", "create", "cancel", "tạo", "hủy", "btn", "save", "tiếp", "next")):
            label = ""
            try:
                label = (self.inner_text() or "").strip()[:30]
            except Exception:
                pass
            _capture_action_from_locator(self, is_button=True, action_type="click", value=label)
    except Exception:
        pass
    return res

Locator.fill = _patched_locator_fill
Locator.select_option = _patched_locator_select
Locator.check = _patched_locator_check
Locator.click = _patched_locator_click

def _patched_page_fill(self, selector, value, *args, **kwargs):
    res = _ORIG_PAGE_FILL(self, selector, value, *args, **kwargs)
    try:
        loc = self.locator(selector).first
        _capture_action_from_locator(loc, action_type="fill", value=str(value))
    except Exception:
        pass
    return res

def _patched_page_select(self, selector, *args, **kwargs):
    val = args[0] if args else (kwargs.get("value") or kwargs.get("label") or "")
    res = _ORIG_PAGE_SELECT(self, selector, *args, **kwargs)
    try:
        loc = self.locator(selector).first
        _capture_action_from_locator(loc, action_type="select", value=str(val))
    except Exception:
        pass
    return res

def _patched_page_check(self, selector, *args, **kwargs):
    res = _ORIG_PAGE_CHECK(self, selector, *args, **kwargs)
    try:
        loc = self.locator(selector).first
        _capture_action_from_locator(loc, action_type="check", value="checked")
    except Exception:
        pass
    return res

Page.fill = _patched_page_fill
Page.select_option = _patched_page_select
Page.check = _patched_page_check

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    global _CURRENT_ACTIVE_NODE
    _CURRENT_ACTIVE_NODE = item

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_call(item):
    global _CURRENT_ACTIVE_NODE
    _CURRENT_ACTIVE_NODE = item

BROWSER_PROFILES = {
    "chromium": {"browser_name": "chromium"},
    "firefox": {"browser_name": "firefox"},
    "webkit": {"browser_name": "webkit"},
    "chrome": {"browser_name": "chromium", "channel": "chrome"},
    "edge": {"browser_name": "chromium", "channel": "msedge"},
    "brave": {"browser_name": "chromium", "executable": "brave"},
}


def _find_brave() -> Optional[str]:
    """Auto-detect Brave browser executable path across Linux, macOS, and Windows."""
    for name in ("brave", "brave-browser"):
        found = shutil.which(name)
        if found:
            return found
    candidates = [
        "/usr/bin/brave",
        "/usr/bin/brave-browser",
        "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
        r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
        r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe",
    ]
    for c in candidates:
        if Path(c).exists():
            return c
    return None


def is_parallel_execution(config) -> bool:
    """Check if pytest is running in parallel mode via pytest-xdist (-n > 1 or -n auto/logical)."""
    numproc = getattr(config.option, "numprocesses", None)
    if numproc is not None:
        if isinstance(numproc, int) and numproc > 1:
            return True
        if isinstance(numproc, str):
            if numproc.isdigit() and int(numproc) > 1:
                return True
            if numproc.lower() in ("auto", "logical"):
                return True

    cli_args = list(getattr(config.invocation_params, "args", [])) + sys.argv
    for idx, arg in enumerate(cli_args):
        if arg in ("-n", "--numprocesses"):
            if idx + 1 < len(cli_args) and str(cli_args[idx + 1]) not in ("0", "1"):
                return True
        elif str(arg).startswith(("-n=", "--numprocesses=")):
            val = str(arg).split("=", 1)[1]
            if val not in ("0", "1"):
                return True
    return False


def is_cli_headed_explicit(config) -> bool:
    """Check if --headed was explicitly passed by the user on the CLI."""
    cli_args = list(getattr(config.invocation_params, "args", [])) + sys.argv
    return "--headed" in cli_args


def is_option_explicit(config, option_name: str) -> bool:
    """Check if an option was explicitly specified by the user on the CLI."""
    cli_args = list(getattr(config.invocation_params, "args", [])) + sys.argv
    return any(arg == option_name or str(arg).startswith(f"{option_name}=") for arg in cli_args)


def pytest_addoption(parser):
    """Register custom CLI options for browser selection and custom binary path."""
    parser.addoption(
        "--target-browser",
        action="store",
        default="chromium",
        choices=list(BROWSER_PROFILES),
        help=f"Target browser to execute tests: {', '.join(BROWSER_PROFILES)} (default: chromium)",
    )
    parser.addoption(
        "--browser-path",
        action="store",
        default=os.environ.get("BROWSER_PATH") or os.environ.get("BRAVE_PATH"),
        help="Custom executable path for browser (overrides auto-detection or default bundled Chromium)",
    )
    parser.addoption(
        "--thanks",
        action="store_true",
        help="Display thank-you acknowledgement page for 4 seconds upon completion (used with --headed)",
    )


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args, pytestconfig, browser_name):
    """
    Configure pytest-playwright launch options according to the selected target browser.
    Respects --target-browser (chromium, chrome, edge, brave, firefox, webkit) and --browser-path.
    Anti-bot flags are strictly applied for Chromium-family browsers.
    Automatically forces headless=True when running parallel unless --headed is explicitly passed on CLI.
    """
    args = list(browser_type_launch_args.get("args", []))
    target_choice = pytestconfig.getoption("--target-browser", default="chromium")
    profile = BROWSER_PROFILES.get(target_choice, {"browser_name": "chromium"})

    # Apply Chromium-specific anti-bot and RAM-optimization arguments
    effective_browser = browser_name or profile.get("browser_name", "chromium")
    if effective_browser == "chromium":
        anti_bot_args = [
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-infobars",
            "--disable-dev-shm-usage",
            "--mute-audio",
            "--disable-extensions",
            "--disable-background-networking",
            "--disable-background-timer-throttling",
            "--disable-backgrounding-occluded-windows",
            "--disable-breakpad",
            "--disable-component-update",
            "--disable-default-apps",
            "--disable-sync",
            "--no-first-run",
            "--js-flags=--max-old-space-size=256",
            "--disable-gpu",
            "--disable-software-rasterizer",
            "--renderer-process-limit=2",
            "--disk-cache-size=1",
            "--media-cache-size=1",
            "--disable-features=Translate,BackForwardCache,AcceptCHFrame,MediaRouter,OptimizationHints",
            "--window-size=1920,1080",
            "--start-maximized",
        ]
        for arg in anti_bot_args:
            if arg not in args:
                args.append(arg)

    opts = {
        **browser_type_launch_args,
        "args": args,
    }

    # Handle system channels (Chrome / Edge)
    if profile.get("channel"):
        opts["channel"] = profile["channel"]

    # Handle custom executable / Brave path
    custom_path = pytestconfig.getoption("--browser-path")
    target_explicit = is_option_explicit(pytestconfig, "--target-browser")

    if profile.get("executable") == "brave" or (target_explicit and pytestconfig.getoption("--target-browser") == "brave"):
        brave_bin = custom_path or _find_brave()
        if not brave_bin or not Path(brave_bin).exists():
            raise pytest.UsageError(
                f"[conftest] Brave browser executable not found at: '{brave_bin}'. "
                "Please install Brave or specify its path via --browser-path=<path> "
                "or the BROWSER_PATH environment variable."
            )
        opts["executable_path"] = brave_bin
    elif custom_path:
        if not Path(custom_path).exists():
            raise FileNotFoundError(f"[conftest] Specified --browser-path does not exist: {custom_path}")
        opts["executable_path"] = custom_path
    # Note: When target is default chromium, use Playwright's lightweight bundled Chromium (saves ~70% RAM over desktop Brave)

    # If running parallel and user did not explicitly request --headed on CLI, enforce headless=True
    if is_parallel_execution(pytestconfig) and not is_cli_headed_explicit(pytestconfig):
        opts["headless"] = True
    elif is_cli_headed_explicit(pytestconfig):
        opts["headless"] = False

    return opts


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, pytestconfig):
    """Configure realistic desktop browser profile with Full HD 1080p resolution and conditional video recording."""
    video_mode = pytestconfig.getoption("--video", default="off")
    args = {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "device_scale_factor": 1,
        "user_agent": (
            "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "locale": "en-US",
        "timezone_id": "America/New_York",
    }
    if video_mode != "off":
        args["record_video_size"] = {"width": 1280, "height": 720}
    return args


@pytest.fixture(autouse=True)
def setup_page(page: Page, json_metadata, request, browser_name):
    """
    Apply comprehensive stealth patches and auto-dismiss consent overlays.
    Teardown: Safely closes browser context, captures 1:1 video per test,
    and records video_path into json_metadata["video_path"].
    """
    global _CURRENT_ACTIVE_NODE
    _CURRENT_ACTIVE_NODE = request.node
    test_start_time = time.time()

    # 1. Apply Playwright Stealth evasion patches (Chromium only)
    if browser_name == "chromium":
        try:
            stealth = Stealth()
            stealth.apply_stealth_sync(page)
        except Exception:
            pass

    # 2. Auto-dismiss cookie consent overlays (Bing/Google/YouTube)
    page.add_init_script("""
        const initObserver = () => {
            const target = document.documentElement || document.body;
            if (!target) return;
            const observer = new MutationObserver(() => {
                const btn = document.querySelector(
                    '#bnp_btn_accept a, #bnp_btn_reject a, #bnp_cookie_banner a, ' +
                    'button[aria-label*="Reject"], button[aria-label*="Accept"], ' +
                    'button[aria-label*="Từ chối"], button[aria-label*="Chấp nhận"], ' +
                    'ytd-button-renderer button[aria-label*="Accept"], ' +
                    'form[action*="consent"] button'
                );
                if (btn && btn.offsetParent !== null) {
                    try { btn.click(); } catch(e) {}
                }
            });
            observer.observe(target, { childList: true, subtree: true });
        };
        if (document.documentElement || document.body) {
            initObserver();
        } else {
            document.addEventListener('DOMContentLoaded', initObserver);
        }
    """)

    # 3. Automatic Action Spotlight & Ripple Visualizer for Recorded Videos (Only active when video is enabled)
    video_mode = getattr(request.config.option, "video", "off")
    is_video_enabled = (video_mode in ("on", "retain-on-failure"))
    if is_video_enabled:
        page.add_init_script(r"""
        (() => {
            if (window.__qa_action_visualizer_initialized) return;
            window.__qa_action_visualizer_initialized = true;

            const injectStyles = () => {
                if (document.getElementById('__qa_action_visualizer_styles__')) return;
                const style = document.createElement('style');
                style.id = '__qa_action_visualizer_styles__';
                style.textContent = `
                    @keyframes qa_video_ripple {
                        0% { transform: translate(-50%, -50%) scale(0.2); opacity: 1; border-width: 4px; }
                        50% { opacity: 0.8; }
                        100% { transform: translate(-50%, -50%) scale(2.4); opacity: 0; border-width: 1px; }
                    }
                    @keyframes qa_element_pulse {
                        0% { outline: 3px solid #38bdf8; outline-offset: 2px; }
                        50% { outline: 4px solid #0284c7; outline-offset: 4px; }
                        100% { outline: 2px solid transparent; outline-offset: 2px; }
                    }
                    .qa-action-ripple {
                        position: absolute;
                        border-radius: 50%;
                        pointer-events: none;
                        z-index: 2147483646;
                        box-sizing: border-box;
                    }
                    .qa-action-badge {
                        position: absolute;
                        pointer-events: none;
                        z-index: 2147483647;
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                        font-size: 11px;
                        font-weight: 700;
                        padding: 3px 8px;
                        border-radius: 6px;
                        white-space: nowrap;
                        color: #ffffff;
                        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.45);
                        transition: opacity 0.3s ease, transform 0.3s ease;
                        opacity: 0.96;
                    }
                `;
                (document.head || document.documentElement).appendChild(style);
            };

            const triggerRipple = (x, y, color = '#0284c7', label = '👆 CLICK') => {
                injectStyles();
                const container = document.body || document.documentElement;
                if (!container) return;

                // 1. Radar Ripple Circle
                const ripple = document.createElement('div');
                ripple.className = 'qa-action-ripple';
                const size = 44;
                ripple.style.width = size + 'px';
                ripple.style.height = size + 'px';
                ripple.style.left = x + 'px';
                ripple.style.top = y + 'px';
                ripple.style.border = `3px solid ${color}`;
                ripple.style.background = `radial-gradient(circle, ${color}33 0%, transparent 70%)`;
                ripple.style.animation = 'qa_video_ripple 0.65s cubic-bezier(0.1, 0.8, 0.3, 1) forwards';
                container.appendChild(ripple);

                // 2. Action Badge Pill
                const badge = document.createElement('div');
                badge.className = 'qa-action-badge';
                badge.style.left = (x + 14) + 'px';
                badge.style.top = (y - 28) + 'px';
                badge.style.background = color === '#10b981' ? 'linear-gradient(135deg, #10b981 0%, #059669 100%)' : 'linear-gradient(135deg, #0284c7 0%, #0369a1 100%)';
                badge.textContent = label;
                container.appendChild(badge);

                setTimeout(() => {
                    ripple.remove();
                    badge.style.opacity = '0';
                    badge.style.transform = 'translateY(-4px)';
                    setTimeout(() => badge.remove(), 300);
                }, 600);
            };

            // Global capture-phase listeners for clicks & form inputs
            window.addEventListener('click', (e) => {
                const x = e.pageX;
                const y = e.pageY;
                const target = e.target;
                let label = '👆 CLICK';
                if (target && target.innerText && target.innerText.trim().length <= 25) {
                    label = `👆 CLICK: "${target.innerText.trim()}"`;
                } else if (target && target.tagName) {
                    label = `👆 CLICK: <${target.tagName.toLowerCase()}>`;
                }
                triggerRipple(x, y, '#0284c7', label);

                if (target && target.style) {
                    const origAnimation = target.style.animation;
                    target.style.animation = 'qa_element_pulse 0.7s ease-out';
                    setTimeout(() => {
                        target.style.animation = origAnimation;
                    }, 700);
                }
            }, true);

            window.addEventListener('input', (e) => {
                const target = e.target;
                if (!target || !target.getBoundingClientRect) return;
                const rect = target.getBoundingClientRect();
                const x = window.scrollX + rect.left + 15;
                const y = window.scrollY + rect.top + rect.height / 2;
                const val = target.value ? (target.type === 'password' ? '••••••' : String(target.value).slice(0, 15)) : '';
                const label = val ? `✏️ INPUT: "${val}"` : '✏️ INPUT';
                triggerRipple(x, y, '#10b981', label);
            }, true);
        })();
    """)

    # 4. Step HUD auto-persistence across page navigations
    def _on_page_nav(frame):
        try:
            st = request.node.funcargs.get("step") if hasattr(request.node, "funcargs") else None
            if st and getattr(st, "current_step", None) and not page.is_closed():
                cur = st.current_step
                title = cur.get("title", "")
                idx = cur.get("step_index", getattr(st, "_step_counter", 1))
                if title:
                    from core.sketch_annotator import SketchAnnotator
                    SketchAnnotator.show_step_hud(page, title, idx)
        except Exception:
            pass

    page.on("framenavigated", lambda frame: _on_page_nav(frame) if frame == page.main_frame else None)
    page.on("domcontentloaded", lambda _: _on_page_nav(None))

    test_failed = False
    exc_caught = None
    try:
        yield page
    except BaseException as exc:
        test_failed = True
        exc_caught = exc
        setattr(request.node, "_has_failed", True)
        setattr(request.node, "_failure_exc", exc)
        raise
    finally:
        # Determine failure status across fixtures, assertions, and steps
        step_tracker = None
        try:
            step_tracker = request.node.funcargs.get("step") if hasattr(request.node, "funcargs") else None
        except Exception:
            pass

        has_failed = (
            test_failed
            or getattr(request.node, "_has_failed", False)
            or (step_tracker and any(s.get("status") == "failed" for s in getattr(step_tracker, "steps", [])))
        )
        active_page = getattr(step_tracker, "page", None) if step_tracker else None
        target_page = active_page or page

        # 1. Fallback Defect Annotation & Video Frame Flushing on Test Failure
        if has_failed and target_page and not target_page.is_closed():
            try:
                overlay_present = False
                try:
                    overlay_present = target_page.evaluate("""() => {
                        return !!(document.getElementById('__qa_sketch_defect_svg__') || 
                                  document.getElementById('__qa_sketch_defect_banner__'));
                    }""")
                except Exception:
                    overlay_present = False

                if not overlay_present:
                    last_step_title = "Test Failure"
                    error_msg = ""

                    if exc_caught:
                        error_msg = str(exc_caught)
                    elif getattr(request.node, "_failure_exc", None):
                        error_msg = str(request.node._failure_exc)

                    if step_tracker and getattr(step_tracker, "steps", None):
                        failed_step = next((s for s in reversed(step_tracker.steps) if s.get("status") == "failed"), None)
                        if failed_step:
                            last_step_title = failed_step.get("title") or last_step_title
                            if not error_msg:
                                error_msg = failed_step.get("error") or failed_step.get("actual") or ""
                        elif step_tracker.steps:
                            last_step = step_tracker.steps[-1]
                            last_step_title = last_step.get("title") or last_step_title
                            if not error_msg:
                                error_msg = last_step.get("error") or last_step.get("actual") or ""

                    if not error_msg:
                        for prop, val in getattr(request.node, "user_properties", []):
                            if prop in ("error_hint", "error_category") and val:
                                error_msg = val
                                break

                    if not error_msg:
                        error_msg = "Assertion / Execution Failure"

                    from core.sketch_annotator import SketchAnnotator
                    SketchAnnotator.highlight_defect(
                        target_page,
                        step_title=last_step_title,
                        error_msg=error_msg,
                        hold_ms=3000 if is_video_enabled else 300,
                    )
                elif is_video_enabled:
                    # Overlay already present, hold at least 2500ms to guarantee video buffer flush
                    target_page.wait_for_timeout(2500)
            except Exception:
                pass

        # 2. Auto-capture Step Actions & Highlighted Actual Result Evidence Screenshot
        try:
            reports_dir = getattr(request.config, "_ticket_reports_dir", DEFAULT_REPORTS_DIR)
            test_slug = re.sub(r"[^\w]+", "_", request.node.name.lower()).strip("_")
            screenshots_dir = Path(reports_dir) / "screenshots"
            screenshots_dir.mkdir(parents=True, exist_ok=True)
            test_screenshots_dir = screenshots_dir / test_slug
            test_screenshots_dir.mkdir(parents=True, exist_ok=True)

            if target_page and not target_page.is_closed():
                from core.evidence_annotator import EvidenceAnnotator

                status_label = "defect" if has_failed else "passed"
                actual_loc = getattr(request.node, "_qa_actual_locator", None)
                actual_text = getattr(request.node, "_qa_actual_text", None)

                # Highlight Actual Result element in DOM
                EvidenceAnnotator.highlight_actual_result(
                    target_page,
                    locator_or_selector=actual_loc,
                    status=status_label,
                    actual_text=actual_text,
                )

                # Capture Actual Result Screenshot into test directory
                actual_filename = "actual_result.png"
                actual_path = test_screenshots_dir / actual_filename
                target_page.screenshot(path=str(actual_path), full_page=False)

                # Legacy fallback copies for backward compatibility
                legacy_filename = f"fail_{test_slug}_teardown.png" if has_failed else f"{test_slug}_pass.png"
                legacy_path = screenshots_dir / legacy_filename
                try:
                    shutil.copy2(actual_path, legacy_path)
                    shutil.copy2(actual_path, screenshots_dir / f"{test_slug}_actual_result.png")
                except Exception:
                    pass

                try:
                    rel_actual_path = str(actual_path.relative_to(WORKSPACE_DIR))
                except Exception:
                    rel_actual_path = str(actual_path)

                setattr(request.node, "_qa_actual_screenshot", rel_actual_path)
                EvidenceAnnotator.clear_overlays(target_page)

                # Synchronize with step_tracker or json_metadata
                step_screens = getattr(request.node, "_qa_step_screenshots", [])
                if step_tracker and getattr(step_tracker, "steps", None):
                    # Preserve all captured setup / action screenshots into steps timeline
                    existing_screenshots = {s.get("screenshot") for s in step_tracker.steps if s.get("screenshot")}
                    for idx, act, val, path in step_screens:
                        if path not in existing_screenshots:
                            insert_pos = max(0, len(step_tracker.steps) - 1)
                            step_tracker.steps.insert(insert_pos, {
                                "title": f"Setup / Thao tác {act.upper()} {f'\"{val}\"' if val else ''}".strip(),
                                "step_index": len(step_tracker.steps) + 1,
                                "status": "passed",
                                "duration": 0.1,
                                "start_offset": 0.0,
                                "end_offset": 0.1,
                                "expected": f"Thực hiện thành công thao tác {act}",
                                "actual": f"Đã thực hiện {act} trên trường tương ứng",
                                "screenshot": path,
                                "error": None,
                            })
                            existing_screenshots.add(path)

                    # Ensure actual result has its own dedicated evidence without overwriting setup images
                    last_step_shot = step_tracker.steps[-1].get("screenshot")
                    if last_step_shot and last_step_shot != rel_actual_path and ("step_" in str(last_step_shot)):
                        actual_step_title = "Kiểm chứng kết quả thực tế (PASSED)" if not has_failed else "Kiểm chứng kết quả thực tế (DEFECT / FAILED)"
                        err_msg = str(exc_caught) if exc_caught else None
                        step_tracker.steps.append({
                            "title": actual_step_title,
                            "step_index": len(step_tracker.steps) + 1,
                            "status": "failed" if has_failed else "passed",
                            "duration": 0.1,
                            "start_offset": 0.0,
                            "end_offset": 0.1,
                            "expected": "Các điều kiện kiểm tra (assertions) và trạng thái giao diện đạt chuẩn nghiệp vụ",
                            "actual": f"FAILED: {err_msg}" if has_failed else (actual_text or "Kết quả thực tế (Actual Result) chính xác theo đặc tả"),
                            "screenshot": rel_actual_path,
                            "error": err_msg,
                            "is_actual_result": True,
                        })
                    else:
                        step_tracker.steps[-1]["screenshot"] = rel_actual_path
                        step_tracker.steps[-1]["is_actual_result"] = True
                else:
                    # Construct steps list with captured step actions + final actual result
                    func_name = request.node.name
                    doc = getattr(request.node.obj, "__doc__", "") or ""
                    first_line = doc.strip().split("\n")[0].strip() if doc.strip() else ""
                    m_tc = re.search(r"\b(TC-[A-Za-z0-9_-]+)\b", first_line)
                    tc_badge = m_tc.group(1) if m_tc else func_name

                    dur_total = round(time.time() - test_start_time, 2) if 'test_start_time' in locals() else 0.5
                    steps_list = []
                    step_screens = getattr(request.node, "_qa_step_screenshots", [])
                    if step_screens:
                        step_dur = round(dur_total / (len(step_screens) + 1), 2)
                        for idx, act, val, path in step_screens:
                            steps_list.append({
                                "title": f"Bước {idx}: Thao tác {act.upper()} {f'\"{val}\"' if val else ''}".strip(),
                                "status": "passed",
                                "duration": step_dur,
                                "start_offset": 0.0,
                                "end_offset": step_dur,
                                "expected": f"Thực hiện thành công thao tác {act}",
                                "actual": f"Đã thực hiện {act} trên trường tương ứng",
                                "screenshot": path,
                                "error": None,
                            })
                    else:
                        rel_action = getattr(request.node, "_qa_action_screenshot", rel_actual_path)
                        steps_list.append({
                            "title": f"Bước 1: Trạng thái nhập liệu hoàn tất ({tc_badge})",
                            "status": "passed",
                            "duration": round(dur_total / 2, 2),
                            "start_offset": 0.0,
                            "end_offset": round(dur_total / 2, 2),
                            "expected": "Giao diện và các trường thông tin được nhập liệu chính xác",
                            "actual": "Đã hoàn thành các bước tương tác / nhập liệu trên giao diện màn hình",
                            "screenshot": rel_action,
                            "error": None,
                        })

                    actual_step_title = "Kiểm chứng kết quả thực tế (PASSED)" if not has_failed else "Kiểm chứng kết quả thực tế (DEFECT / FAILED)"
                    err_msg = str(exc_caught) if exc_caught else None
                    steps_list.append({
                        "title": f"Bước {len(steps_list) + 1}: {actual_step_title}",
                        "status": "failed" if has_failed else "passed",
                        "duration": round(dur_total / 2, 2),
                        "start_offset": round(dur_total / 2, 2),
                        "end_offset": dur_total,
                        "expected": "Các điều kiện kiểm tra (assertions) và trạng thái giao diện đạt chuẩn nghiệp vụ",
                        "actual": f"FAILED: {err_msg}" if has_failed else (actual_text or "Kết quả thực tế (Actual Result) chính xác theo đặc tả"),
                        "screenshot": rel_actual_path,
                        "error": err_msg,
                        "is_actual_result": True,
                    })

                    if "steps" not in json_metadata:
                        json_metadata["steps"] = []
                    json_metadata["steps"].clear()
                    json_metadata["steps"].extend(steps_list)
        except Exception:
            pass

        # 3. Teardown: Safely close context and record video path 1:1 per test
        try:
            target_page_for_video = target_page or page

            video = getattr(target_page_for_video, "video", None) or getattr(page, "video", None)
            context = getattr(page, "context", None)

            if context:
                try:
                    context.close()
                except Exception:
                    pass

            video_mode = getattr(request.config.option, "video", "retain-on-failure")
            should_save_video = (video_mode == "on") or (has_failed)

            if video and should_save_video:
                video_path = None
                try:
                    video_path = video.path()
                except Exception:
                    pass

                # If output directory is defined, save/copy video to test-scoped artifact folder inside run_id
                reports_dir = getattr(request.config, "_ticket_reports_dir", DEFAULT_REPORTS_DIR)
                run_id = getattr(request.config, "_run_id", None) or os.environ.get("PYTEST_RUN_ID", "RUN-UNKNOWN")
                test_results_dir = Path(getattr(request.config.option, "output", reports_dir / "test-results" / run_id))
                clean_slug = re.sub(r"[^\w]+", "-", request.node.nodeid.lower()).strip("-")

                if test_results_dir.name != run_id and run_id not in test_results_dir.parts:
                    target_video_dir = test_results_dir / run_id / clean_slug
                else:
                    target_video_dir = test_results_dir / clean_slug
                target_video_file = target_video_dir / "video.webm"

                try:
                    target_video_dir.mkdir(parents=True, exist_ok=True)
                    video.save_as(str(target_video_file))
                    recorded_path = str(target_video_file.resolve())
                except Exception:
                    recorded_path = str(Path(video_path).resolve()) if video_path else None

                if recorded_path:
                    json_metadata["video_path"] = recorded_path
            elif video and not should_save_video:
                try:
                    video.delete()
                except Exception:
                    pass
        except Exception:
            pass


@pytest.fixture(scope="session", autouse=True)
def thanks_at_end(request, browser_type, browser_type_launch_args):
    """
    Session-scoped hook to display a thank-you postcard for 4 seconds upon test completion.
    Only triggers when explicitly requested via --thanks and --headed, and skips on xdist workers.
    """
    yield  # all tests execute here

    if hasattr(request.config, "workerinput"):  # xdist worker: skip
        return
    if not (request.config.getoption("--thanks") and request.config.getoption("--headed")):
        return

    # If US01 was run, Step 6 already displayed the thank-you page in the active window
    ticket = getattr(request.config, "_ticket_name", None)
    if ticket == "us01_bing_search":
        return

    if THANKS_PAGE.exists():
        browser = browser_type.launch(**{**browser_type_launch_args, "headless": False})
        page = browser.new_page()
        page.goto(THANKS_PAGE.resolve().as_uri(), wait_until="domcontentloaded")
        # Hold display for 4 seconds for the viewer to read
        page.wait_for_timeout(4000)
        browser.close()
