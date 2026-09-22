"""SearchBox component - Reusable across Bing home and result pages."""
import random
import time
from playwright.sync_api import Page


class SearchBoxComponent:
    """Component handling search input with human-like typing and submit actions."""

    def __init__(self, page: Page):
        self.page = page

    @property
    def search_input(self):
        return self.page.locator("textarea[name='q'], input[name='q'], #sb_form_q").first

    def is_visible(self) -> bool:
        """Check if search input is visible."""
        return self.search_input.is_visible()

    def search_for(self, query: str):
        """Fill search query with human-like keystroke delays and natural pauses."""
        self.search_input.wait_for(state="visible", timeout=10000)
        self.search_input.click()
        time.sleep(random.uniform(0.3, 0.6))
        self.search_input.fill("")

        # Type character-by-character with random delay (simulating real human typing)
        self.search_input.press_sequentially(query, delay=random.randint(60, 110))

        # Natural human pause before pressing Enter
        time.sleep(random.uniform(0.5, 1.0))
        self.search_input.press("Enter")

        # Ensure page navigates to search results
        try:
            self.page.wait_for_url(lambda u: "/search" in u, wait_until="domcontentloaded", timeout=8000)
        except Exception:
            self.page.keyboard.press("Enter")
            self.page.wait_for_url(lambda u: "/search" in u, wait_until="domcontentloaded", timeout=8000)
