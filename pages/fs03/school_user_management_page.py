"""
pages/fs03/school_user_management_page.py - Page Object for School User Management screen.
Complies with Invariant 1 (Zero assertions in Page Objects) and ADR-0006.
"""
from typing import List, Optional
from playwright.sync_api import Locator, Page
from pages.base_page import BasePage


class SchoolUserManagementPage(BasePage):
    """
    Page Object encapsulating DOM elements and interactions for:
    EduFAMS Admin Portal > School User Management (/school-user-management)
    """

    def __init__(self, page: Page):
        super().__init__(page)

        # Navigation & Sidebar Elements
        self.sidebar_nav: Locator = self.page.locator("nav")
        self.school_users_nav_link: Locator = self.page.locator(
            "nav a[href='/school-user-management'], nav a:has-text('School Users')"
        )
        self.admin_profile_role: Locator = self.page.locator("text=System Admin")
        self.admin_profile_username: Locator = self.page.locator("text=moehq")

        # Page Header & Controls
        self.page_heading: Locator = self.page.locator("h1:has-text('School user management')")
        self.page_subtitle: Locator = self.page.locator("text=Manage users assigned to schools.")
        self.create_school_user_button: Locator = self.page.locator("button:has-text('Create School User')")

        # Table & Search Elements
        self.search_input: Locator = self.page.locator("input[type='search']")
        self.table: Locator = self.page.locator("table")
        self.table_rows: Locator = self.page.locator("table tbody tr")
        self.table_headers: Locator = self.page.locator("table thead th")
        self.pagination: Locator = self.page.locator("nav[aria-label*='pagination' i], [class*='pagination']")

    # --- Navigation Methods ---
    def open(self, base_url: str = "http://localhost:5173") -> None:
        """Directly navigate to School User Management page with robust session recovery."""
        target_url = f"{base_url}/school-user-management"
        self.page.goto(target_url)
        self.page.wait_for_load_state("domcontentloaded")

        try:
            self.page.wait_for_selector(
                "h1:has-text('School user management'), button:has-text('Sign in with Microsoft')",
                timeout=5000
            )
        except Exception:
            pass

        if target_url not in self.page.url or "login" in self.page.url or self.page.locator("button:has-text('Sign in with Microsoft')").is_visible():
            from pages.fs03.admin_login_page import AdminLoginPage
            login_page = AdminLoginPage(self.page)
            login_page.login_with_microsoft_as_admin(base_url=base_url)
            self.page.goto(target_url)
            self.page.wait_for_load_state("domcontentloaded")

        self.wait_for_page_loaded()

    def navigate_via_sidebar(self) -> None:
        """Click 'School Users' in sidebar navigation."""
        self.school_users_nav_link.first.wait_for(state="visible", timeout=10000)
        self.school_users_nav_link.first.click()
        self.page.wait_for_url("**/school-user-management", timeout=10000)
        self.wait_for_page_loaded()

    def wait_for_page_loaded(self) -> None:
        """Wait until page heading and table or empty message are loaded."""
        self.page_heading.wait_for(state="visible", timeout=15000)
        self.table.wait_for(state="visible", timeout=15000)

    # --- Action Methods ---
    def click_create_school_user(self) -> None:
        """Click '+ Create School User' button to navigate to create screen."""
        self.create_school_user_button.wait_for(state="visible", timeout=10000)
        self.create_school_user_button.click()
        self.page.wait_for_url("**/school-user-management/new", timeout=10000)

    def search_user(self, query: str) -> None:
        """Type query into search input and wait for network/table update."""
        self.search_input.fill("")
        self.search_input.fill(query)
        try:
            self.page.wait_for_load_state("networkidle", timeout=3000)
        except Exception:
            pass

    # --- Query & State Inspection Methods ---
    def get_heading_text(self) -> str:
        """Return inner text of page heading."""
        return self.page_heading.inner_text().strip()

    def is_create_button_visible(self) -> bool:
        """Return True if Create School User button is visible."""
        return self.create_school_user_button.is_visible()

    def is_moehq_logged_in(self) -> bool:
        """Return True if moehq admin profile is displayed in sidebar."""
        return self.admin_profile_username.is_visible() and self.admin_profile_role.is_visible()

    def get_row_count(self) -> int:
        """Return number of rendered rows in table body."""
        return self.table_rows.count()

    def get_all_row_texts(self) -> List[str]:
        """Return list of text contents for all rows in table body."""
        count = self.table_rows.count()
        return [self.table_rows.nth(i).inner_text().strip() for i in range(count)]

    def get_row_by_username(self, username: str) -> Optional[Locator]:
        """Return Locator for specific table row matching username/NRIC."""
        row_locator = self.page.locator(f"table tbody tr:has-text('{username}')")
        if row_locator.count() > 0:
            return row_locator.first
        return None

    def wait_for_user_in_table(self, identifier: str, timeout: int = 10000) -> None:
        """Wait until a table row containing identifier is visible."""
        row = self.page.locator(f"table tbody tr:has-text('{identifier}')").first
        row.wait_for(state="visible", timeout=timeout)

    def is_user_present_in_table(self, identifier: str, timeout: int = 10000) -> bool:
        """Return True if identifier (username or full name) exists in table body."""
        try:
            self.wait_for_user_in_table(identifier, timeout=timeout)
            return True
        except Exception:
            return False
