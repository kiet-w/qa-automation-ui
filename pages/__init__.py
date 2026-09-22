"""Pages package - How to interact with pages."""
from pages.base_page import BasePage
from pages.bing_home_page import BingHomePage
from pages.bing_results_page import BingResultsPage
from pages.youtube_page import YouTubePage

__all__ = [
    "BasePage",
    "BingHomePage",
    "BingResultsPage",
    "YouTubePage",
]
