"""BingHomePage - Page Object for Bing home page."""
from playwright.sync_api import Page
from components.search_box import SearchBoxComponent
from pages.base_page import BasePage


class BingHomePage(BasePage):
    URL = "https://www.bing.com"

    def __init__(self, page: Page):
        super().__init__(page)
        self.search_box = SearchBoxComponent(page)

    def navigate(self, url: str = None):
        """Navigate to Bing homepage."""
        return super().navigate(url or self.URL, wait_until="domcontentloaded")

    def search(self, keyword: str):
        """Execute a search from the home page."""
        self.search_box.search_for(keyword)

