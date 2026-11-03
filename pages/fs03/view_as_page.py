"""
pages/fs03/view_as_page.py - Page Object Model for View As Support Console (/support-console).
Pure Black-Box implementation adhering to ISO 29119-3 & Core Pillars (NO assertions in POM).
"""
import re
from typing import List, Optional
from playwright.sync_api import Locator, Page
from pages.base_page import BasePage


class ViewAsPage(BasePage):
    """Page Object Model for the View As Support Console screen (/support-console)."""

    URL_PATH = "/support-console"

    def __init__(self, page: Page):
        super().__init__(page)

        # -------------------------------------------------------------
        # 1. Navigation & Shell Elements
        # -------------------------------------------------------------
        self.sidebar_nav: Locator = page.locator('aside nav[aria-label*="navigation" i], aside nav')
        self.sidebar_link_view_as: Locator = page.locator('aside nav a[href="/support-console"]')
        self.page_heading: Locator = page.get_by_role("heading", name=re.compile(r"View As", re.IGNORECASE))

        # -------------------------------------------------------------
        # 2. Main Tabs
        # -------------------------------------------------------------
        self.tab_school_users: Locator = page.get_by_role("tab", name=re.compile(r"School users", re.IGNORECASE))
        self.tab_persona: Locator = page.get_by_role("tab", name=re.compile(r"School role \(persona\)", re.IGNORECASE))
        self.tab_parents: Locator = page.get_by_role("tab", name=re.compile(r"Parents", re.IGNORECASE))

        # -------------------------------------------------------------
        # 3. Tab A: School Role (Persona) Elements
        # -------------------------------------------------------------
        self.persona_school_search_input: Locator = (
            page.locator('input[placeholder*="Search school" i]')
            .or_(page.locator('input[aria-label*="Search school" i]'))
            .or_(page.locator('input[type="text"]').first)
        )
        self.persona_search_button: Locator = page.get_by_role("button", name="Search", exact=True)
        self.persona_school_rosyth: Locator = page.locator('text="Rosyth Primary School"')
        self.persona_role_select: Locator = page.locator('select, [role="combobox"]').first
        self.persona_select_button: Locator = page.get_by_role("button", name="Select", exact=True)

        # -------------------------------------------------------------
        # 4. Tab B: School Users Elements
        # -------------------------------------------------------------
        self.user_search_input: Locator = (
            page.locator('input[placeholder*="search" i]')
            .or_(page.locator('input[type="search"]'))
            .or_(page.locator('input[type="text"]').first)
        )
        self.user_search_button: Locator = page.get_by_role("button", name="Search", exact=True)
        self.user_row_staff1: Locator = page.locator('tr:has-text("staff1@IAM.edu.vn"), tr:has-text("Bui Thi H")')
        self.user_select_button: Locator = page.locator('tr:has-text("staff1@IAM.edu.vn") button:has-text("Select"), button:has-text("Select")')

        # -------------------------------------------------------------
        # 5. Audit Trail Form: "Start View As"
        # -------------------------------------------------------------
        self.form_container: Locator = page.locator('form, div:has(button:has-text("Start View As"))')
        self.reason_textarea: Locator = page.get_by_label("Reason", exact=False)
        self.ticket_input: Locator = page.get_by_label("Ticket reference", exact=False)
        self.start_view_as_button: Locator = page.get_by_role("button", name="Start View As", exact=True)

        # -------------------------------------------------------------
        # 6. Session Context Verification Elements
        # -------------------------------------------------------------
        self.header_element: Locator = page.get_by_role("banner").or_(page.locator("header")).first
        self.exit_view_as_button: Locator = page.get_by_role("button", name="Exit", exact=True)

        # School Menu Links
        self.menu_classes: Locator = page.locator('aside nav a[href="/class-management"]')
        self.menu_school_config: Locator = page.locator('aside nav a[href="/school-config"]')
        self.menu_students: Locator = page.locator('aside nav a[href="/student-management"]')
        self.menu_fee_batches: Locator = page.locator('aside nav a[href*="fee"]')
        self.menu_fas: Locator = page.locator('aside nav a[href*="fas"]')

    # -----------------------------------------------------------------
    # Interaction Methods (Actions & State Retrieval ONLY - NO ASSERTS)
    # -----------------------------------------------------------------

    def open(self, base_url: str = "https://admin.20-255-158-192.sslip.io") -> None:
        """Directly navigate to the /support-console URL."""
        self.page.goto(f"{base_url.rstrip('/')}{self.URL_PATH}", wait_until="domcontentloaded")

    def click_sidebar_view_as(self) -> None:
        """Navigate to View As screen via Sidebar link."""
        self.sidebar_link_view_as.click()

    def switch_to_persona_tab(self) -> None:
        """Switch to 'School role (persona)' tab."""
        self.tab_persona.click()

    def switch_to_school_users_tab(self) -> None:
        """Switch to 'School users' tab."""
        self.tab_school_users.click()

    def search_and_select_persona(self, school_code_or_name: str = "RPS-0201", role_name: str = "School Admin") -> None:
        """Search school and select target role under Persona tab."""
        self.switch_to_persona_tab()
        self.persona_school_search_input.fill(school_code_or_name)
        self.persona_search_button.click()
        self.page.wait_for_timeout(400)
        
        # Click the matched school item
        target_school = self.page.locator(f'text="{school_code_or_name}"').or_(self.persona_school_rosyth).first
        if target_school.is_visible():
            target_school.click()

        # Select role if dropdown is available
        if self.persona_role_select.count() > 0 and self.persona_role_select.is_visible():
            try:
                self.persona_role_select.select_option(label=role_name)
            except Exception:
                try:
                    self.persona_role_select.select_option(value=role_name)
                except Exception:
                    pass

        self.persona_select_button.click()

    def search_and_select_school_user(self, search_query: str = "staff1") -> None:
        """Search and select specific school user under School users tab."""
        self.switch_to_school_users_tab()
        self.user_search_input.fill(search_query)
        self.user_search_button.click()
        self.page.wait_for_timeout(500)
        
        # Click Select button on the matched user row
        select_btn = self.page.locator(f'tr:has-text("{search_query}") button:has-text("Select")').first
        if select_btn.is_visible():
            select_btn.click()
        else:
            self.user_select_button.first.click()

    def fill_audit_reason(self, reason: str) -> None:
        """Fill Reason field in Start View As form."""
        self.reason_textarea.fill(reason)

    def fill_ticket_reference(self, ticket: str) -> None:
        """Fill Ticket reference field in Start View As form."""
        self.ticket_input.fill(ticket)

    def fill_audit_form(self, reason: str, ticket: str) -> None:
        """Fill both Reason and Ticket reference fields."""
        self.fill_audit_reason(reason)
        self.fill_ticket_reference(ticket)

    def is_start_button_enabled(self) -> bool:
        """Return True if Start View As button is active and enabled."""
        return self.start_view_as_button.is_enabled()

    def click_start_view_as(self) -> None:
        """Click Start View As button to initiate simulation session."""
        self.start_view_as_button.click()

    def get_header_text(self) -> str:
        """Read text content from header element."""
        return self.header_element.inner_text()

    def is_school_sidebar_visible(self) -> bool:
        """Check if school-level sidebar menu items are visible."""
        return self.menu_classes.is_visible()

    def exit_simulation(self) -> None:
        """Exit the current View As simulation session."""
        if self.exit_view_as_button.is_visible():
            self.exit_view_as_button.click()
