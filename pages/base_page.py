"""
pages/base_page.py - Base Page Object providing shared web interactions and utilities.
All specific Page Objects inherit from this class to ensure reusability and consistent behavior.
"""
from pathlib import Path
from typing import Union
from playwright.sync_api import Locator, Page


class BasePage:
    """Base class for all Page Objects in the automation framework."""

    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str, wait_until: str = "domcontentloaded"):
        """Navigate to a specified URL."""
        self.page.goto(url, wait_until=wait_until)
        return self

    def get_locator(self, selector_or_locator: Union[str, Locator]) -> Locator:
        """Helper to normalize selector strings or Locator objects."""
        if isinstance(selector_or_locator, str):
            return self.page.locator(selector_or_locator)
        return selector_or_locator

    def wait_for_visible(self, selector_or_locator: Union[str, Locator], timeout: int = 10000) -> Locator:
        """Wait until an element is visible on the page."""
        locator = self.get_locator(selector_or_locator)
        locator.wait_for(state="visible", timeout=timeout)
        return locator

    def click_element(self, selector_or_locator: Union[str, Locator], timeout: int = 10000):
        """Wait for an element to be visible and clickable, then click it."""
        locator = self.wait_for_visible(selector_or_locator, timeout=timeout)
        locator.click()

    def fill_text(self, selector_or_locator: Union[str, Locator], text: str, timeout: int = 10000):
        """Wait for an input element and fill text."""
        locator = self.wait_for_visible(selector_or_locator, timeout=timeout)
        locator.fill(text)

    def get_title(self) -> str:
        """Return the current document title."""
        return self.page.title()

    def get_current_url(self) -> str:
        """Return the current browser URL."""
        return self.page.url

    def wait_for_page_load(self, state: str = "domcontentloaded", timeout: int = 15000):
        """Wait for page load state."""
        self.page.wait_for_load_state(state, timeout=timeout)

    def take_screenshot(self, filepath: Union[str, Path], full_page: bool = False) -> str:
        """Capture screenshot and save to the given file path."""
        path_obj = Path(filepath)
        path_obj.parent.mkdir(parents=True, exist_ok=True)
        self.page.screenshot(path=str(path_obj), full_page=full_page)
        return str(path_obj)
