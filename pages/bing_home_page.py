"""BingHomePage - Page Object for Bing home page."""
from playwright.sync_api import Page
from components.search_box import SearchBoxComponent


class BingHomePage:
    URL = "https://www.bing.com"

    def __init__(self, page: Page):
        self.page = page
        self.search_box = SearchBoxComponent(page)

    def navigate(self):
        """Navigate to Bing homepage."""
        self.page.goto(self.URL, wait_until="domcontentloaded")
        return self

    def search(self, keyword: str):
        """Execute a search from the home page."""
        self.search_box.search_for(keyword)
