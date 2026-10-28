"""
pages/fs03/admin_dashboard_shell_locators.py - Verified BSK Locators for Admin Dashboard Shell.
Strictly locator constants. Complies with Invariant 1 and modularity limits (<100 lines).
"""

class AdminDashboardShellLocators:
    """BSK-verified locators for EduFAMS Admin Portal Shell & Navigation (:5173)."""

    # Global Header & Controls
    HEADER = "header"
    COLLAPSE_SIDEBAR_BTN = 'header button[aria-label*="sidebar" i], header button[title*="sidebar" i]'
    BREADCRUMB = 'nav[aria-label="Breadcrumb"]'
    USER_NAME = "header strong"
    USER_ROLE_OR_CODE = "header strong + span, header strong + div, header"
    SKIP_LINK = 'a:has-text("Skip to main content")'

    # Sidebar Navigation Container & Elements
    SIDEBAR_CONTAINER = "aside"
    BRAND_LINK = 'aside a[aria-label*="Admin Portal" i], aside a[class*="brand" i], aside > a[href="/"]'
    NAV = "aside nav"
    NAV_LINKS = "aside nav a[href]"
    NAV_ACTIVE_LINK = "aside nav a[aria-current='page'], aside nav a[class*='active' i]"
    SIGN_OUT_BTN = 'aside button:has-text("Sign out"), button:has-text("Sign out")'

    # Main Content Area & Fallbacks
    MAIN_CONTENT = "#admin-main-content, main"
    PAGE_BODY = "body"
    PAGE_HEADING = "h1"
    NOT_FOUND_CONTAINER = "#admin-main-content, main"

    # Feedback, Banners & Notifications
    ALERT = '[role="alert"]'
    ACCESS_RESTRICTED_ALERT = '[role="alert"]:has-text("Access restricted")'
    NOTIFICATIONS_LIST = 'ul[aria-label="Notifications"], [role="status"]'

    @staticmethod
    def nav_link_by_href(href: str) -> str:
        return f'aside nav a[href="{href}"]'

    @staticmethod
    def action_by_label(label: str) -> str:
        return f'button:has-text("{label}"), a:has-text("{label}")'
