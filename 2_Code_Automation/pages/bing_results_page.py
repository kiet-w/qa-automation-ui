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

    @staticmethod
    def _extract_clean_target_url(href: str) -> str:
        """
        Extract direct destination URL from Bing click-tracking redirect link (bing.com/ck/a),
        preventing Bing's tracking script (&ntb=1) from calling window.close() and aborting Playwright.
        """
        if not href:
            return ""
        if "bing.com/ck/a" in href:
            import base64
            import urllib.parse
            parsed = urllib.parse.urlparse(href)
            params = urllib.parse.parse_qs(parsed.query)
            if "u" in params and params["u"]:
                raw_u = params["u"][0]
                encoded = raw_u[2:] if raw_u.startswith(("a1", "a0")) else raw_u
                padding = 4 - (len(encoded) % 4)
                if padding and padding < 4:
                    encoded += "=" * padding
                try:
                    decoded = base64.urlsafe_b64decode(encoded).decode("utf-8")
                    if decoded.startswith("http"):
                        return decoded
                except Exception:
                    pass
            import re
            return re.sub(r"[?&]ntb=\d+", "", href)
        return href

    def access_first_result(self) -> Page:
        """
        Navigate to the first search result URL cleanly in the same tab,
        preventing Bing's redirect script from triggering window.close().
        """
        self.wait_for_results()
        href = self.first_result_link.get_attribute("href") or ""
        clean_url = self._extract_clean_target_url(href)

        if clean_url:
            self.page.goto(clean_url, wait_until="domcontentloaded")
        else:
            try:
                self.first_result_link.evaluate("el => el.removeAttribute('target')")
            except Exception:
                pass
            self.first_result_link.click()
            self.page.wait_for_load_state("domcontentloaded")

        # Safely recover page reference if a popup opened or original page switched
        if self.page.is_closed():
            active_pages = [p for p in self.page.context.pages if not p.is_closed()]
            if active_pages:
                self.page = active_pages[-1]

        return self.page

    def search_again(self, keyword: str):
        """Perform a new search directly from the results page using the reusable component."""
        self.search_box.search_for(keyword)
        self.wait_for_results()
