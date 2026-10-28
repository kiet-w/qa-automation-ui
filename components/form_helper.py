"""
components/form_helper.py - Reusable Component for Form Automation & Validation Extraction.

Provides standardized form interaction, automated field population, and granular
error extraction for any form across the EduFAMS design system.
Complies with Invariant 1 (UI interaction and state reading only; zero assertions).
"""
from typing import Any, Dict, List, Optional, Union
from playwright.sync_api import Locator, Page
from core.error_diagnostics import ErrorDiagnostics


class FormHelper:
    """Component helper to automate form flows and inspect validation errors."""

    def __init__(self, page: Page, container: Optional[Union[str, Locator]] = None):
        self.page = page
        if isinstance(container, str):
            self.container = page.locator(container)
        elif container is not None:
            self.container = container
        else:
            self.container = page.locator("form, main, [role='main']").first

    def fill_fields(self, data: Dict[str, Any]) -> None:
        """Fill multiple form inputs, selects, textareas, or checkboxes by name/id."""
        for name, value in data.items():
            self.fill_field(name, value)

    def fill_field(self, name_or_id: str, value: Any) -> None:
        """Set a single field value based on its type (input, select, checkbox, radio)."""
        field = self._find_control(name_or_id)
        tag = field.evaluate("el => el.tagName.toLowerCase()")
        input_type = field.get_attribute("type") or ""

        if tag == "select":
            field.select_option(str(value))
        elif input_type in ("checkbox", "radio"):
            if bool(value):
                field.check()
            else:
                field.uncheck()
        else:
            field.fill(str(value))

    def clear_field(self, name_or_id: str) -> None:
        """Clear text from an input or textarea."""
        field = self._find_control(name_or_id)
        field.fill("")

    def _find_control(self, name_or_id: str) -> Locator:
        """Finds control by name, id, or test-id with CSS fallback."""
        loc = self.container.locator(
            f"input[name='{name_or_id}'], select[name='{name_or_id}'], textarea[name='{name_or_id}'], "
            f"#{name_or_id}, [data-testid='{name_or_id}']"
        )
        if loc.count() == 0:
            loc = self.page.locator(f"#{name_or_id}, [name='{name_or_id}']")
        return loc.first

    def get_field_errors(self) -> Dict[str, str]:
        """Extract all validation error messages mapped to field names."""
        diag = ErrorDiagnostics.capture(self.page, container=self.container)
        return diag.get("field_errors", {})

    def get_summary_errors(self) -> List[str]:
        """Extract list of errors listed in the FormErrorSummary alert section."""
        diag = ErrorDiagnostics.capture(self.page, container=self.container)
        return diag.get("summary_errors", [])

    def is_field_invalid(self, name_or_id: str) -> bool:
        """Check if a specific field has aria-invalid="true"."""
        ctrl = self._find_control(name_or_id)
        return ctrl.get_attribute("aria-invalid") == "true" if ctrl.count() > 0 else False

    def is_submit_disabled(self, submit_selector: str = "button[type='submit']") -> bool:
        """Check if form submit button is disabled."""
        btn = self.container.locator(submit_selector).first
        return btn.is_disabled() if btn.count() > 0 else True

    def click_submit(self, submit_selector: str = "button[type='submit']") -> None:
        """Click the form submit button."""
        self.container.locator(submit_selector).first.click()

    def get_form_snapshot(
        self,
        success_selector: str = "p[role='status'], [class*='success'], [class*='toast']",
        submit_selector: str = "button[type='submit']",
    ) -> Dict[str, Any]:
        """
        Produce a standardized snapshot for Exceptor consumption:
        - success_visible: bool
        - visible_errors: Dict[str, str] (maps field names to error messages)
        - summary_errors: List[str]
        - is_submit_disabled: bool
        """
        field_errors = self.get_field_errors()
        summary_errors = self.get_summary_errors()

        # Check for success toast or alert
        success_loc = self.page.locator(success_selector)
        success_visible = (
            success_loc.first.is_visible(timeout=1000) if success_loc.count() > 0 else False
        )

        return {
            "success_visible": success_visible,
            "visible_errors": field_errors,
            "summary_errors": summary_errors,
            "is_submit_disabled": self.is_submit_disabled(submit_selector),
        }
