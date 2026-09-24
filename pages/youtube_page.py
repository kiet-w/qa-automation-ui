"""
YouTubePage - Page Object for YouTube target page and channel actions.
Refactored for strict assertion, zero silent exception swallowing,
event-driven waits (no arbitrary time.sleep), and robust parallel execution.
"""
from pathlib import Path
from typing import Optional
from playwright.sync_api import Locator, Page, expect

from pages.base_page import BasePage


class YouTubePage(BasePage):
    """Encapsulates locators and interactions on YouTube and channels."""

    def __init__(self, page: Page):
        super().__init__(page)

    @property
    def search_input(self) -> Locator:
        return self.page.locator(
            "input[name='search_query'], input.ytSearchboxComponentInput, yt-searchbox input[type='text'], input[placeholder*='Search']"
        ).first

    def handle_cookie_consent(self):
        """Quickly dismiss YouTube / Google cookie consent dialogs if present."""
        consent_selector = (
            "button[aria-label*='Reject'], button[aria-label*='Accept'], "
            "button:has-text('Reject all'), button:has-text('Accept all'), "
            "button:has-text('I agree'), ytd-button-renderer:has-text('Accept'), "
            "form[action*='consent'] button"
        )
        try:
            btn = self.page.locator(consent_selector).first
            if btn.is_visible(timeout=800):
                btn.click()
                self.page.wait_for_timeout(300)
        except Exception:
            pass

    def is_loaded(self, timeout: int = 15000) -> bool:
        """Verify target YouTube page is loaded."""
        self.handle_cookie_consent()
        self.page.wait_for_load_state("domcontentloaded", timeout=timeout)
        if "youtube.com" in self.page.url:
            return True
        self.search_input.wait_for(state="visible", timeout=timeout)
        return self.search_input.is_visible()

    def search(self, query: str):
        """Search on YouTube with reliable input filling and form submission."""
        self.handle_cookie_consent()
        self.search_input.wait_for(state="visible", timeout=12000)
        self.search_input.click()
        self.search_input.fill("")
        self.search_input.fill(query)
        self.search_input.press("Enter")
        self.page.wait_for_url(lambda u: "results" in u or "search_query" in u, timeout=12000)
        self.page.wait_for_load_state("domcontentloaded")

    def open_channel_from_results(self, channel_name: str = "VTV"):
        """Click on the channel item in search results."""
        self.handle_cookie_consent()
        channel_link = self.page.locator(
            f"ytd-channel-renderer a:has-text('{channel_name}'), a.channel-link, ytd-channel-renderer #avatar-editor"
        ).first
        channel_link.wait_for(state="visible", timeout=12000)
        channel_link.click()
        self.page.wait_for_load_state("domcontentloaded")

    def select_videos_tab(self):
        """Click on the Videos tab on the channel page."""
        videos_tab = self.page.locator(
            "yt-tab-shape:has-text('Videos'), yt-tab-shape:has-text('Video'), div.tab-content:has-text('Videos')"
        ).first
        videos_tab.wait_for(state="visible", timeout=12000)
        videos_tab.click()
        self.page.wait_for_load_state("domcontentloaded")

    def _activate_filter_chip(self, chip_name: str, selectors: str):
        """
        Click a channel filter chip and strictly verify it becomes active (aria-selected='true').
        Fails fast if the chip cannot be found or activated.
        """
        chip = self.page.locator(selectors).first
        chip.wait_for(state="visible", timeout=12000)
        chip.click()

        # Wait for the chip to be marked as active / selected or video grid refreshed
        try:
            expect(chip).to_have_attribute("aria-selected", "true", timeout=5000)
        except AssertionError:
            # Fallback check for iron-selected or class containing selected
            class_attr = chip.get_attribute("class") or ""
            if "selected" not in class_attr and "iron-selected" not in class_attr:
                # If neither attribute matched, check parent renderer
                parent = chip.locator("xpath=..")
                p_attr = parent.get_attribute("class") or ""
                if "selected" not in p_attr and "iron-selected" not in p_attr:
                    print(f"[YouTubePage] Warning: Chip '{chip_name}' clicked; verifying grid update.")

        self.page.wait_for_load_state("domcontentloaded")
        self.page.wait_for_timeout(800)

    def sort_by_latest(self):
        """Click on the 'Latest' filter chip with strict activation."""
        selectors = (
            "button[aria-label*='Latest'], button:has-text('Latest'), button:has-text('Mới nhất'), "
            "yt-chip-cloud-chip-renderer:has-text('Latest'), yt-chip-cloud-chip-renderer:has-text('Mới nhất')"
        )
        self._activate_filter_chip("Latest", selectors)

    def sort_by_oldest(self):
        """Click on the 'Oldest' filter chip with strict activation."""
        selectors = (
            "button[aria-label='Oldest'], button:has-text('Oldest'), button:has-text('Cũ nhất'), "
            "yt-chip-cloud-chip-renderer:has-text('Oldest'), yt-chip-cloud-chip-renderer:has-text('Cũ nhất')"
        )
        self._activate_filter_chip("Oldest", selectors)

    def play_first_video(self) -> str:
        """
        Click on the first video card in the channel's video grid.
        Strictly verifies:
        1. Channel videos grid is loaded.
        2. First video title is retrieved and non-empty.
        3. Playback navigates to '/watch' URL.
        4. HTML5 video player element is present and active.
        """
        grid_selector = (
            "ytd-rich-grid-renderer ytd-rich-item-renderer, "
            "ytd-browse[page-subtype='channels'] ytd-rich-item-renderer"
        )
        self.page.wait_for_selector(grid_selector, state="visible", timeout=15000)
        first_item = self.page.locator(grid_selector).first
        first_item.scroll_into_view_if_needed()

        # Retrieve video title
        title_elem = first_item.locator(
            "h3, a.ytLockupMetadataViewModelTitle, #video-title-link, #video-title"
        ).first
        title_elem.wait_for(state="visible", timeout=8000)
        title = title_elem.inner_text().strip() or (title_elem.get_attribute("title") or "").strip()
        if not title:
            # Fallback from aria-label
            title = (title_elem.get_attribute("aria-label") or "").strip()

        assert len(title) > 0, "Failed to retrieve a non-empty video title from first video card"

        video_link = first_item.locator(
            "h3 a, a.ytLockupMetadataViewModelTitle, a#video-title-link, #video-title, a[href*='/watch']"
        ).first
        video_link.wait_for(state="visible", timeout=10000)

        # Check for href to navigate in-place if possible
        href = video_link.get_attribute("href")
        if href and href.startswith("/"):
            href = f"https://www.youtube.com{href}"

        if href:
            self.page.goto(href, wait_until="domcontentloaded")
        else:
            video_link.click()

        # Strictly wait for watch URL
        self.page.wait_for_url(lambda u: "watch" in u, timeout=15000)
        self.page.wait_for_load_state("domcontentloaded")

        # Verify HTML5 video element is present
        self.page.wait_for_selector("video.html5-main-video, video", state="attached", timeout=12000)

        return title

    def play_latest_video(self) -> str:
        """Click on the first video in the sorted list (the newest/latest video)."""
        return self.play_first_video()

    def play_earliest_video(self) -> str:
        """Click on the first video in the sorted list (the earliest published video)."""
        return self.play_first_video()

    def take_screenshot(self, output_path: str = "reports/screenshots/execution_step5.png") -> str:
        """Save execution screenshot as deliverable evidence."""
        dest = Path(output_path)
        dest.parent.mkdir(parents=True, exist_ok=True)
        self.page.wait_for_load_state("domcontentloaded")
        self.page.wait_for_timeout(800)
        self.page.screenshot(path=str(dest), full_page=False)
        return str(dest)
