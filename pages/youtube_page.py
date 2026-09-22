"""YouTubePage - Page Object for YouTube target page and channel actions."""
import random
import time
from pathlib import Path
from playwright.sync_api import Page
from pages.base_page import BasePage


class YouTubePage(BasePage):
    """Encapsulates locators and interactions on YouTube and channels."""

    def __init__(self, page: Page):
        super().__init__(page)

    @property
    def search_input(self):
        # Target visible search input box (ignoring hidden file inputs)
        return self.page.locator(
            "input[name='search_query'], input.ytSearchboxComponentInput, yt-searchbox input[type='text'], input[placeholder*='Search']"
        ).first

    def handle_cookie_consent(self):
        """Dismiss YouTube / Google cookie consent dialogs if present."""
        consent_selectors = [
            "button[aria-label*='Reject']",
            "button[aria-label*='Accept']",
            "button:has-text('Reject all')",
            "button:has-text('Accept all')",
            "button:has-text('I agree')",
            "ytd-button-renderer:has-text('Accept')",
            "form[action*='consent'] button",
        ]
        for selector in consent_selectors:
            try:
                btn = self.page.locator(selector).first
                if btn.is_visible(timeout=1500):
                    btn.click()
                    self.page.wait_for_timeout(500)
                    break
            except Exception:
                continue

    def is_loaded(self, timeout: int = 15000) -> bool:
        """Verify target YouTube page is loaded."""
        try:
            self.handle_cookie_consent()
            self.page.wait_for_load_state("domcontentloaded", timeout=timeout)
            if "youtube.com" in self.page.url:
                return True
            self.search_input.wait_for(state="visible", timeout=timeout)
            return self.search_input.is_visible()
        except Exception:
            return "youtube.com" in self.page.url

    def search(self, query: str):
        """Search on YouTube with human-like typing."""
        self.handle_cookie_consent()
        self.search_input.wait_for(state="visible", timeout=10000)
        self.search_input.click()
        time.sleep(random.uniform(0.2, 0.5))
        self.search_input.fill("")
        self.search_input.press_sequentially(query, delay=random.randint(50, 90))
        time.sleep(random.uniform(0.4, 0.8))
        self.search_input.press("Enter")
        try:
            self.page.wait_for_url(lambda u: "results" in u or "search_query" in u, timeout=10000)
        except Exception:
            pass
        self.page.wait_for_load_state("domcontentloaded")

    def open_channel_from_results(self, channel_name: str = "VTV"):
        """Click on the channel item in search results."""
        channel_link = self.page.locator(
            f"ytd-channel-renderer a:has-text('{channel_name}'), a.channel-link, ytd-channel-renderer #avatar-editor"
        ).first
        channel_link.wait_for(state="visible", timeout=10000)
        channel_link.click()
        self.page.wait_for_load_state("domcontentloaded")
        self.page.wait_for_timeout(2000)

    def select_videos_tab(self):
        """Click on the Videos tab on the channel page."""
        videos_tab = self.page.locator(
            "yt-tab-shape:has-text('Videos'), yt-tab-shape:has-text('Video'), div.tab-content:has-text('Videos')"
        ).first
        videos_tab.wait_for(state="visible", timeout=10000)
        videos_tab.click()
        self.page.wait_for_load_state("domcontentloaded")
        self.page.wait_for_timeout(2000)

    def sort_by_latest(self):
        """Click on the 'Latest' (Mới nhất) filter chip."""
        latest_btn = self.page.locator(
            "button[aria-label*='Latest'], button:has-text('Latest'), button:has-text('Mới nhất'), "
            "yt-chip-cloud-chip-renderer:has-text('Latest'), yt-chip-cloud-chip-renderer:has-text('Mới nhất')"
        ).first
        try:
            latest_btn.wait_for(state="visible", timeout=8000)
            latest_btn.click()
            self.page.wait_for_timeout(2000)
        except Exception:
            pass

    def sort_by_oldest(self):
        """Click on the 'Oldest' (Cũ nhất / Ngày sớm nhất) filter chip."""
        oldest_btn = self.page.locator(
            "button[aria-label='Oldest'], button:has-text('Oldest'), button:has-text('Cũ nhất'), "
            "yt-chip-cloud-chip-renderer:has-text('Oldest'), yt-chip-cloud-chip-renderer:has-text('Cũ nhất')"
        ).first
        oldest_btn.wait_for(state="visible", timeout=10000)
        oldest_btn.click()
        self.page.wait_for_timeout(2000)

    def play_first_video(self) -> str:
        """Click on the first video card in the channel's video grid."""
        print("[DEBUG] play_first_video: waiting for channel videos grid...")
        self.page.wait_for_selector(
            "ytd-rich-grid-renderer ytd-rich-item-renderer, ytd-browse[page-subtype='channels'] ytd-rich-item-renderer",
            state="visible",
            timeout=15000,
        )
        first_item = self.page.locator(
            "ytd-rich-grid-renderer ytd-rich-item-renderer, ytd-browse[page-subtype='channels'] ytd-rich-item-renderer"
        ).first
        first_item.scroll_into_view_if_needed()

        # Retrieve video title from h3 or title link
        title = ""
        try:
            title_elem = first_item.locator(
                "h3, a.ytLockupMetadataViewModelTitle, #video-title-link, #video-title"
            ).first
            if title_elem.is_visible(timeout=3000):
                title = title_elem.inner_text().strip()
        except Exception as e:
            print(f"[DEBUG] Failed to get title: {e}")

        print(f"[DEBUG] Found video title: {title}")

        # Check if clicking opens a new page/tab or navigates in-place
        video_link = first_item.locator(
            "h3 a, a.ytLockupMetadataViewModelTitle, a#video-title-link, #video-title, a[href*='/watch']"
        ).first
        video_link.wait_for(state="visible", timeout=10000)

        pages_before = len(self.page.context.pages)
        print(f"[DEBUG] Pages before click: {pages_before}, current page is_closed: {self.page.is_closed()}")

        # Click the video
        video_link.click()
        print("[DEBUG] Clicked video link")

        # Wait a moment and check open pages
        time.sleep(1)
        pages_after = self.page.context.pages
        print(f"[DEBUG] Pages after click: {len(pages_after)}")
        for i, p in enumerate(pages_after):
            print(f"[DEBUG] Page {i}: closed={p.is_closed()}, url={p.url if not p.is_closed() else 'closed'}")

        # If a new tab was opened, update self.page
        if len(pages_after) > pages_before and not pages_after[-1].is_closed():
            self.page = pages_after[-1]
            print(f"[DEBUG] Switched to new tab: {self.page.url}")

        if not self.page.is_closed():
            try:
                self.page.wait_for_url(lambda u: "watch" in u, timeout=10000)
            except Exception as e:
                print(f"[DEBUG] wait_for_url: {e}")
            self.page.wait_for_load_state("domcontentloaded")
            self.page.wait_for_timeout(2000)

        return title

    def play_latest_video(self) -> str:
        """Click on the first video in the sorted list (the newest/latest video)."""
        return self.play_first_video()

    def play_earliest_video(self) -> str:
        """Click on the first video in the sorted list (the earliest published video)."""
        return self.play_first_video()

    def take_screenshot(self, output_path: str = "reports/execution_step5.png") -> str:
        """Save execution screenshot as deliverable evidence."""
        dest = Path(output_path)
        dest.parent.mkdir(parents=True, exist_ok=True)
        self.page.wait_for_timeout(1500)
        self.page.screenshot(path=str(dest), full_page=False)
        return str(dest)
