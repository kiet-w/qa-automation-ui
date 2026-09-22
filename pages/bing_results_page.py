"""BingResultsPage - Page Object for Bing search results page."""
from playwright.sync_api import Page
from components.search_box import SearchBoxComponent
from pages.base_page import BasePage


class BingResultsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.search_box = SearchBoxComponent(page)

    @property
    def result_items(self):
        return self.page.locator("#b_results > li.b_algo")

    @property
    def first_result_link(self):
        return self.page.locator("#b_results li.b_algo h2 a, li.b_algo h2 a").first

    def wait_for_results(self, timeout: int = 15000):
        """Wait until search result items are present on the page."""
        self.first_result_link.wait_for(state="visible", timeout=timeout)

    def get_first_result_title(self) -> str:
        """Retrieve the text title of the first search result."""
        self.wait_for_results()
        return self.first_result_link.inner_text().strip()

    def get_results_count(self) -> int:
        """Return the number of result items found."""
        self.wait_for_results()
        return self.result_items.count()

    def click_first_result(self):
        """Click on the first search result link."""
        self.wait_for_results()
        self.first_result_link.click()

    def access_first_result(self) -> Page:
        """
        Click on the first search result link in the same tab.
        Removes target='_blank' so the entire journey stays in 1 single tab,
        ensuring Playwright records exactly ONE unified video from start to finish.
        """
        self.wait_for_results()
        try:
            self.first_result_link.evaluate("el => el.removeAttribute('target')")
        except Exception:
            pass
        self.first_result_link.click()
        self.page.wait_for_load_state("domcontentloaded")
        return self.page

    def search_again(self, keyword: str):
        """Perform a new search directly from the results page using the reusable component."""
        self.search_box.search_for(keyword)
        self.wait_for_results()
