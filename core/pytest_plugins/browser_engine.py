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
from playwright.sync_api import Page
from playwright_stealth import Stealth

REPO_ROOT = Path(__file__).resolve().parents[2]
WORKSPACE_DIR = REPO_ROOT
DEFAULT_REPORTS_DIR = WORKSPACE_DIR / "reports"
THANKS_PAGE = WORKSPACE_DIR / "docs" / "thanks.html"

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

    # Apply Chromium-specific anti-bot arguments only when running Chromium-family engines
    effective_browser = browser_name or profile.get("browser_name", "chromium")
    if effective_browser == "chromium":
        anti_bot_args = [
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-infobars",
            "--disable-dev-shm-usage",
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

    if profile.get("executable") == "brave":
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
    elif not target_explicit and effective_browser == "chromium":
        # Default behavior: If system has Brave installed, auto-use it to prevent bot detection
        auto_brave = _find_brave()
        if auto_brave and Path(auto_brave).exists():
            opts["executable_path"] = auto_brave

    # If running parallel and user did not explicitly request --headed on CLI, enforce headless=True
    if is_parallel_execution(pytestconfig) and not is_cli_headed_explicit(pytestconfig):
        opts["headless"] = True
    elif is_cli_headed_explicit(pytestconfig):
        opts["headless"] = False

    return opts


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure realistic desktop browser profile with Full HD 1080p resolution and crisp video recording."""
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "record_video_size": {"width": 1920, "height": 1080},
        "device_scale_factor": 1,
        "user_agent": (
            "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "locale": "en-US",
        "timezone_id": "America/New_York",
    }


@pytest.fixture(autouse=True)
def setup_page(page: Page, json_metadata, request, browser_name):
    """
    Apply comprehensive stealth patches and auto-dismiss consent overlays.
    Teardown: Safely closes browser context, captures 1:1 video per test,
    and records video_path into json_metadata["video_path"].
    """
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
    test_failed = False
    try:
        yield page
    except BaseException:
        test_failed = True
        raise
    finally:
        # 1. Auto-capture Final Evidence Screenshot if test passed and last step has no screenshot
        try:
            step_tracker = request.node.funcargs.get("step")
            if not test_failed and step_tracker and getattr(step_tracker, "steps", None):
                last_step = step_tracker.steps[-1]
                if not last_step.get("screenshot"):
                    active_page = getattr(step_tracker, "page", None) or page
                    if active_page and not active_page.is_closed():
                        prefix = f"{step_tracker.test_slug}_" if step_tracker.test_slug else ""
                        evidence_filename = f"{prefix}evidence.png"
                        evidence_path = step_tracker.screenshots_dir / evidence_filename
                        evidence_path.parent.mkdir(parents=True, exist_ok=True)
                        active_page.screenshot(path=str(evidence_path), full_page=False)
                        try:
                            rel_evidence_path = str(evidence_path.relative_to(WORKSPACE_DIR))
                        except Exception:
                            rel_evidence_path = str(evidence_path)
                        last_step["screenshot"] = rel_evidence_path
        except Exception:
            pass

        # 2. Teardown: Safely close context and record video path 1:1 per test
        try:
            active_page = None
            step_tracker = request.node.funcargs.get("step")
            if step_tracker:
                active_page = getattr(step_tracker, "page", None)
            target_page_for_video = active_page or page

            video = getattr(target_page_for_video, "video", None) or getattr(page, "video", None)
            context = getattr(page, "context", None)

            if context:
                try:
                    context.close()
                except Exception:
                    pass

            if video:
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
