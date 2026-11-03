"""
pages/fs03/admin_dashboard_shell_page.py - Page Object for EduFAMS Admin Dashboard Shell.
Complies with Invariant 1 (Zero assertions in POM) and modularity limits (<200 lines).
"""
from typing import Dict, List
from playwright.sync_api import Locator, Page

from pages.base_page import BasePage
from pages.fs03.admin_dashboard_shell_locators import AdminDashboardShellLocators


class AdminDashboardShellPage(BasePage):
    """Encapsulates UI interactions and state extraction for the Admin Portal Shell."""

    def __init__(self, page: Page):
        super().__init__(page)
        # Header components
        self.header = self.page.locator(AdminDashboardShellLocators.HEADER)
        self.collapse_sidebar_btn = self.page.locator(AdminDashboardShellLocators.COLLAPSE_SIDEBAR_BTN)
        self.mobile_navigation_btn = self.page.locator(AdminDashboardShellLocators.MOBILE_NAVIGATION_BTN)
        self.breadcrumb = self.page.locator(AdminDashboardShellLocators.BREADCRUMB)
        self.user_name = self.page.locator(AdminDashboardShellLocators.USER_NAME)
        self.user_role_or_code = self.page.locator(AdminDashboardShellLocators.USER_ROLE_OR_CODE)
        self.skip_link = self.page.locator(AdminDashboardShellLocators.SKIP_LINK)

        # Sidebar navigation components
        self.sidebar_container = self.page.locator(AdminDashboardShellLocators.SIDEBAR_CONTAINER)
        self.brand_link = self.page.locator(AdminDashboardShellLocators.BRAND_LINK)
        self.nav = self.page.locator(AdminDashboardShellLocators.NAV)
        self.nav_links = self.page.locator(AdminDashboardShellLocators.NAV_LINKS)
        self.active_nav_link = self.page.locator(AdminDashboardShellLocators.NAV_ACTIVE_LINK)
        self.sign_out_btn = self.page.locator(AdminDashboardShellLocators.SIGN_OUT_BTN)

        # Main content & fallbacks
        self.main_content = self.page.locator(AdminDashboardShellLocators.MAIN_CONTENT)
        self.page_body = self.page.locator(AdminDashboardShellLocators.PAGE_BODY)
        self.page_heading = self.page.locator(AdminDashboardShellLocators.PAGE_HEADING)
        self.not_found_container = self.page.locator(AdminDashboardShellLocators.NOT_FOUND_CONTAINER)
        self.back_to_home_link = self.page.locator(AdminDashboardShellLocators.BACK_TO_HOME_LINK)

        # Alerts and notifications
        self.alert = self.page.locator(AdminDashboardShellLocators.ALERT)
        self.access_restricted_alert = self.page.locator(AdminDashboardShellLocators.ACCESS_RESTRICTED_ALERT)
        self.school_badge = self.page.locator(AdminDashboardShellLocators.SCHOOL_BADGE)
        self.school_badge_code = self.page.locator(AdminDashboardShellLocators.SCHOOL_BADGE_CODE)

    def open(self, base_url: str = "http://localhost:5173", path: str = "/") -> None:
        """Navigate to target route within admin shell."""
        url = f"{base_url.rstrip('/')}/{path.lstrip('/')}"
        self.page.goto(url, wait_until="domcontentloaded")

    def get_user_display_name(self) -> str:
        """Return user full name from global header."""
        if self.user_name.first.is_visible():
            return self.user_name.first.inner_text().strip()
        return ""

    def get_header_text(self) -> str:
        """Return combined header text."""
        if self.header.first.is_visible():
            return self.header.first.inner_text().strip()
        return ""

    def get_sidebar_width(self) -> float:
        """Return bounding box width of the sidebar container."""
        box = self.sidebar_container.bounding_box()
        return float(box["width"]) if box else 0.0

    def toggle_sidebar(self) -> None:
        """Click the collapse/expand sidebar button."""
        self.collapse_sidebar_btn.first.click()
        self.page.wait_for_load_state("domcontentloaded")

    def get_nav_link_texts(self) -> List[str]:
        """Return visible trimmed texts of all sidebar navigation links."""
        texts: List[str] = []
        count = self.nav_links.count()
        for i in range(count):
            link = self.nav_links.nth(i)
            if link.is_visible():
                t = link.inner_text().strip()
                if t:
                    texts.append(t)
        return texts

    def get_nav_link_hrefs(self) -> List[str]:
        """Return href values of all visible sidebar navigation links."""
        hrefs: List[str] = []
        count = self.nav_links.count()
        for i in range(count):
            link = self.nav_links.nth(i)
            if link.is_visible():
                h = link.get_attribute("href")
                if h:
                    hrefs.append(h)
        return hrefs

    def click_nav_link_by_href(self, href: str) -> None:
        """Click sidebar navigation link with specified href attribute."""
        target = self.page.locator(AdminDashboardShellLocators.nav_link_by_href(href))
        target.first.click()

    def nav_link_by_href(self, href: str) -> Locator:
        """Return a sidebar link for test assertions without exposing selectors."""
        return self.page.locator(AdminDashboardShellLocators.nav_link_by_href(href))

    def action_by_label(self, label: str) -> Locator:
        """Return an action control by its specified visible label."""
        return self.page.locator(AdminDashboardShellLocators.action_by_label(label))

    def get_active_nav_info(self) -> Dict[str, str]:
        """Return text, href, and aria-current of the currently active navigation item."""
        if self.active_nav_link.count() > 0:
            link = self.active_nav_link.first
            return {
                "text": link.inner_text().strip(),
                "href": link.get_attribute("href") or "",
                "aria_current": link.get_attribute("aria-current") or "",
            }
        return {"text": "", "href": "", "aria_current": ""}

    def sign_out(self) -> None:
        """Click Sign out button in sidebar."""
        self.sign_out_btn.first.click()

    def click_action_by_label(self, label: str) -> None:
        """Click an externally specified shell action."""
        self.action_by_label(label).first.click()

    def click_back_to_home(self) -> None:
        """Return from the not-found page to the dashboard."""
        self.back_to_home_link.click()

    def get_main_content_text(self) -> str:
        """Return visible main content text for assertions owned by tests."""
        if self.main_content.first.is_visible():
            return self.main_content.first.inner_text().strip()
        return ""

    def get_alert_texts(self) -> List[str]:
        """Return all inner texts of visible alerts."""
        alerts: List[str] = []
        count = self.alert.count()
        for i in range(count):
            al = self.alert.nth(i)
            if al.is_visible():
                alerts.append(al.inner_text().strip())
        return alerts
