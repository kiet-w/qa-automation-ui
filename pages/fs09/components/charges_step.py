"""
pages/fs09/components/charges_step.py - Step 1: Outstanding Charges Selection Component.
Encapsulates table data extraction, filtering, select-all checkboxes, and summary amounts.
Complies strictly with Invariant 1 (Zero assertions in Page Objects/Components).
"""
from typing import Any, Dict, List, Optional
from playwright.sync_api import Page
from pages.fs09.locators import BillingPaymentLocators as Loc


class ChargesSelectionStep:
    """Component managing Step 1: Outstanding Charges Selection table & summary cards."""

    def __init__(self, page: Page):
        self.page = page

    def is_loaded(self) -> bool:
        """Check if Step 1 (Charges Selection) is currently active and visible."""
        return (
            self.page.locator(Loc.PAGE_HEADING).is_visible()
            and (self.page.locator(Loc.CHARGES_TABLE).is_visible() or self.has_empty_charges_notice())
            and not self.page.locator(Loc.METHOD_HEADING).is_visible()
            and not self.page.locator(Loc.REVIEW_HEADING).is_visible()
        )

    def wait_for_loaded(self, timeout: int = 15000) -> None:
        """Wait for the Step 1 charges selection view or error state."""
        self.page.wait_for_selector(
            f"table, {Loc.EMPTY_CHARGES_NOTICE}, {Loc.INVALID_CONTEXT_HEADING}, {Loc.WALLET_ERROR_HEADING}, {Loc.ALERT}",
            timeout=timeout,
        )

    def get_summary_amounts(self) -> Dict[str, str]:
        """Extract amounts from the summary cards in Step 1."""
        res: Dict[str, str] = {
            "outstanding_fees": "",
            "ea_balance": "",
            "selected_total": "",
            "child_name": "",
        }
        out_loc = self.page.locator(Loc.OUTSTANDING_FEES_SUMMARY)
        if out_loc.count() > 0:
            res["outstanding_fees"] = out_loc.first.inner_text().strip()

        ea_loc = self.page.locator(Loc.EA_BALANCE_SUMMARY)
        if ea_loc.count() > 0:
            res["ea_balance"] = ea_loc.first.inner_text().strip()

        total_loc = self.page.locator(Loc.SELECTED_TOTAL_SUMMARY)
        if total_loc.count() > 0:
            res["selected_total"] = total_loc.first.inner_text().strip()

        child_loc = self.page.locator(Loc.CHILD_NAME_SUMMARY)
        if child_loc.count() > 0:
            raw_child = child_loc.first.inner_text().strip()
            if "for " in raw_child:
                raw_child = raw_child.split("for ")[-1].strip()
            res["child_name"] = raw_child

        return res

    def set_status_filter(self, filter_value: str) -> None:
        """Change the status filter dropdown ('All', 'Overdue', 'DueSoon')."""
        select = self.page.locator(Loc.STATUS_FILTER_SELECT).first
        select.select_option(value=filter_value)
        self.wait_for_loaded()

    def get_status_filter(self) -> str:
        """Get the currently selected filter value."""
        return self.page.locator(Loc.STATUS_FILTER_SELECT).first.input_value()

    def get_selected_total_amount(self) -> str:
        """Extract the amount from the 'Selected total' card."""
        loc = self.page.locator(Loc.SELECTED_TOTAL_SUMMARY)
        return loc.first.inner_text().strip() if loc.count() > 0 else ""

    def get_charge_count(self) -> int:
        """Return the number of charge rows in the outstanding charges table."""
        if self.has_empty_charges_notice():
            return 0
        return self.page.locator(Loc.CHARGES_ROWS).count()

    def get_charge_rows_data(self) -> List[Dict[str, Any]]:
        """Extract structured data from all rows in the outstanding charges table."""
        if self.has_empty_charges_notice():
            return []

        rows = self.page.locator(Loc.CHARGES_ROWS)
        count = rows.count()
        charges: List[Dict[str, Any]] = []

        for i in range(count):
            row = rows.nth(i)
            cells = row.locator("td")
            cell_count = cells.count()
            if cell_count < 5:
                continue

            checkbox = cells.nth(0).locator("input[type='checkbox']")
            is_checked = checkbox.is_checked() if checkbox.count() > 0 else False
            is_disabled = not checkbox.is_enabled() if checkbox.count() > 0 else True

            description = cells.nth(1).inner_text().strip()
            gross_amount = cells.nth(2).inner_text().strip()
            subsidy = cells.nth(3).inner_text().strip()
            net_amount = cells.nth(4).inner_text().strip()

            due_date = ""
            status = ""
            if cell_count >= 6:
                cell_5_text = cells.nth(5).inner_text().strip()
                if cell_count >= 7:
                    due_date = cell_5_text
                    status = cells.nth(6).inner_text().strip()
                else:
                    if any(s in cell_5_text.lower() for s in ("upcoming", "due", "overdue")):
                        status = cell_5_text
                    else:
                        due_date = cell_5_text

            charges.append({
                "index": i,
                "selected": is_checked,
                "disabled": is_disabled,
                "description": description,
                "gross_amount": gross_amount,
                "subsidy": subsidy,
                "net_amount": net_amount,
                "due_date": due_date,
                "status": status,
            })

        return charges

    def select_all_charges(self) -> None:
        """Click the 'Select all' checkbox."""
        checkbox = self.page.locator(Loc.SELECT_ALL_CHECKBOX).first
        checkbox.check()

    def unselect_all_charges(self) -> None:
        """Uncheck the 'Select all' checkbox."""
        checkbox = self.page.locator(Loc.SELECT_ALL_CHECKBOX).first
        checkbox.uncheck()

    def is_all_selected(self) -> bool:
        """Check if 'Select all' checkbox is checked."""
        checkbox = self.page.locator(Loc.SELECT_ALL_CHECKBOX).first
        return checkbox.is_checked() if checkbox.count() > 0 else False

    def select_charge_by_index(self, index: int) -> None:
        """Select an individual charge row by row index."""
        rows = self.page.locator(Loc.CHARGES_ROWS)
        if index < rows.count():
            row = rows.nth(index)
            checkbox = row.locator("input[type='checkbox']").first
            if not checkbox.is_checked():
                checkbox.check()

    def unselect_charge_by_index(self, index: int) -> None:
        """Unselect an individual charge row by row index."""
        rows = self.page.locator(Loc.CHARGES_ROWS)
        if index < rows.count():
            row = rows.nth(index)
            checkbox = row.locator("input[type='checkbox']").first
            if checkbox.is_checked():
                checkbox.uncheck()

    def toggle_charge_by_description(self, description_substring: str) -> None:
        """Toggle checkbox for a charge matching description."""
        row = self.page.locator(f"{Loc.CHARGES_ROWS}:has-text('{description_substring}')").first
        if row.count() > 0:
            checkbox = row.locator("input[type='checkbox']").first
            checkbox.click()

    def get_selected_charges_count_text(self) -> str:
        """Return the text of the selected count indicator."""
        loc = self.page.locator(Loc.SELECTED_COUNTER)
        return loc.inner_text().strip() if loc.count() > 0 else ""

    def click_continue(self) -> None:
        """Click the Continue button to proceed from Step 1 to Step 2."""
        self.page.locator(Loc.STEP1_CONTINUE_BTN).first.click()

    def has_empty_charges_notice(self) -> bool:
        """Check if empty charges state is visible."""
        return self.page.locator(Loc.EMPTY_CHARGES_NOTICE).is_visible()

    def get_empty_charges_text(self) -> str:
        """Get the text from the empty charges state."""
        loc = self.page.locator(Loc.EMPTY_CHARGES_NOTICE)
        return loc.inner_text().strip() if loc.count() > 0 else ""
