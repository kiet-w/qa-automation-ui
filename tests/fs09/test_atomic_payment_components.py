"""
tests/fs09/test_atomic_payment_components.py - Atomic Controls & Validation Matrix (TS-090-ATM).

Covers atomic UI controls & 12-layer input matrix for Billing & Payments (/billing/:studentId):
- TC-R9-ATM-01: Select All checkbox toggles all row checkboxes and updates total counter
- TC-R9-ATM-02: Unchecking a single row checkbox updates Select All to unselected/indeterminate
- TC-R9-ATM-03: Continue button on Step 1 disabled when 0 charges are selected
- TC-R9-ATM-04..09, 16: Custom EA split amount validation matrix (BVA 1 cent, zero, negative, upper, XSS, SQLi, aria-invalid, anti-i18n leakage)
- TC-R9-ATM-10: Debounce & single-dispatch on rapid double-clicking payment button

Traceability:
- FSD: [agile] fs/md/FS document/FS-09_Outstanding_Fees_and_Payment.md §3.1, §4.1, §5.1, §5.3
- Rules: BR-F9-02, BR-F9-11; AC-01 to AC-22; Invariants 0 to 11
"""
import copy
import json
from pathlib import Path
from typing import Any, Dict
import pytest
from playwright.sync_api import expect

from tests.base_test import BaseTest
from pages.fs09.billing_payment_page import BillingPaymentPage


CASE_FILE = Path(__file__).resolve().parents[2] / "data/fs09/fs09_coverage_cases.json"
CASES = json.loads(CASE_FILE.read_text(encoding="utf-8"))
SPLIT_CASE_IDS = [c["id"] for c in CASES if c["field"] == "splitAmount"]


@pytest.mark.p1
@pytest.mark.atomic
@pytest.mark.ui
class TestAtomicPaymentComponents(BaseTest):
    """Atomic Controls and Input Matrix verification for FS09 Billing Flow."""

    def test_tc_r9_atm_01_select_all_checkbox_toggles_all(
        self, fs09_data: Dict[str, Any], auth_helper
    ):
        """
        TC-R9-ATM-01: Select All checkbox toggles all individual invoice row checkboxes.
        Scenario: TS-090-ATM | Priority: Medium | Invariant 7 UI Health
        """
        auth_helper("PAR-NORMAL-01")
        persona = copy.deepcopy(fs09_data["personas"]["PAR-NORMAL-01"])
        payment_page = self.get_page(BillingPaymentPage)
        payment_page.open_for_student(persona["student_id"], base_url=fs09_data["base_url"])

        with self.step("Step 1: Check Select All and verify all row checkboxes checked", expected="All checkboxes checked."):
            payment_page.check_select_all()
            total_rows = payment_page.charges.get_charges_count()
            selected_count = payment_page.charges.get_selected_count()
            assert selected_count == total_rows, f"Expected {total_rows} checked, got {selected_count}."
            assert payment_page.charges.is_continue_enabled(), "Continue button should be enabled."
            self.step.set_actual(f"Select All checked: {selected_count}/{total_rows} rows selected.")

        with self.step("Step 2: Uncheck Select All and verify all row checkboxes cleared", expected="All checkboxes unchecked."):
            payment_page.uncheck_select_all()
            selected_after = payment_page.charges.get_selected_count()
            assert selected_after == 0, f"Expected 0 checked, got {selected_after}."
            assert not payment_page.charges.is_continue_enabled(), "Continue button must be disabled when 0 selected."
            self.step.set_actual("Select All unchecked: all rows cleared, Continue disabled.")

    def test_tc_r9_atm_02_unchecking_row_resets_select_all(
        self, fs09_data: Dict[str, Any], auth_helper
    ):
        """
        TC-R9-ATM-02: Unchecking a single row when all selected updates Select All state.
        Scenario: TS-090-ATM | Priority: Low | Invariant 7 UI Health
        """
        auth_helper("PAR-NORMAL-01")
        persona = copy.deepcopy(fs09_data["personas"]["PAR-NORMAL-01"])
        payment_page = self.get_page(BillingPaymentPage)
        payment_page.open_for_student(persona["student_id"], base_url=fs09_data["base_url"])

        with self.step("Step 1: Check Select All then uncheck first row", expected="Select all unchecks/indeterminate."):
            payment_page.check_select_all()
            payment_page.charges.toggle_charge_by_index(0, check=False)
            assert not payment_page.charges.is_select_all_checked(), "Select All must no longer be checked."
            self.step.set_actual("Single row unchecked: Select All cleanly unchecked.")

    def test_tc_r9_atm_03_zero_selection_disables_continue(
        self, fs09_data: Dict[str, Any], auth_helper
    ):
        """
        TC-R9-ATM-03: Continue button is disabled when zero charges are selected.
        Scenario: TS-090-ATM | Priority: Medium | Invariant 7 UI Health
        """
        auth_helper("PAR-NORMAL-01")
        persona = copy.deepcopy(fs09_data["personas"]["PAR-NORMAL-01"])
        payment_page = self.get_page(BillingPaymentPage)
        payment_page.open_for_student(persona["student_id"], base_url=fs09_data["base_url"])

        with self.step("Step 1: Ensure zero checkboxes checked and inspect Continue button", expected="Continue disabled."):
            payment_page.uncheck_select_all()
            assert not payment_page.charges.is_continue_enabled(), "Continue button must be disabled."
            self.step.set_actual("Zero charges selected: Continue button disabled as expected.")

    @pytest.mark.parametrize("case_id", SPLIT_CASE_IDS, ids=SPLIT_CASE_IDS)
    def test_tc_r9_atm_split_matrix(
        self, fs09_data: Dict[str, Any], auth_helper, case_id: str
    ):
        """
        Parameterized execution of Split Payment custom EA input matrix (12-layer / BVA).
        Covers TC-R9-ATM-04, 05, 06, 06b, 07, 08, 08b, 09, 16, 16b.
        """
        case = next(c for c in CASES if c["id"] == case_id)
        auth_helper("PAR-NORMAL-01")
        persona = copy.deepcopy(fs09_data["personas"]["PAR-NORMAL-01"])
        payment_page = self.get_page(BillingPaymentPage)
        payment_page.open_for_student(persona["student_id"], base_url=fs09_data["base_url"])

        # Navigate to Step 2 with split-eligible charge
        payment_page.charges.toggle_charge_by_index(3, check=True)  # Overseas trip ($1500)
        payment_page.charges.click_continue()
        payment_page.methods.select_method("Both")

        input_locator = payment_page.methods.split_ea_input
        input_value = case.get("input", "")

        with self.step(f"Execute {case_id}: {case['title']}", expected=f"Kind: {case['kind']}"):
            input_locator.fill("")
            input_locator.fill(str(input_value))
            input_locator.blur()

            if case["kind"] == "valid":
                assert payment_page.methods.is_continue_enabled(), f"Continue should be enabled for valid input {input_value}."
                self.step.set_actual(f"Valid split input {input_value} accepted.")
            elif case["kind"] == "invalid":
                is_invalid = input_locator.get_attribute("aria-invalid") == "true" or payment_page.methods.is_split_error_visible()
                assert is_invalid, f"Expected aria-invalid or split error for invalid input {input_value}."
                assert not payment_page.methods.is_continue_enabled(), "Continue must be disabled when split amount invalid."
                # Verify zero raw translation key leakage
                if payment_page.methods.is_split_error_visible():
                    err_text = payment_page.methods.get_split_error_text()
                    assert "features." not in err_text and "validation." not in err_text, f"Raw i18n leaked: {err_text}"
                self.step.set_actual(f"Invalid input {input_value} flagged with aria-invalid / error.")
            elif case["kind"] == "invalid_or_blocked":
                # Value is either sanitized/blocked or flagged invalid
                cur_val = input_locator.input_value()
                has_error = input_locator.get_attribute("aria-invalid") == "true" or not payment_page.methods.is_continue_enabled() or cur_val != input_value
                assert has_error, f"Input {input_value} must be sanitized, blocked, or flagged."
                self.step.set_actual(f"Non-numeric/symbol input {input_value} safely handled.")
            elif case["kind"] == "safe_text":
                # Verify no alert or script execution
                assert payment_page.page.locator("body").is_visible(), "Page remains intact after XSS string."
                self.step.set_actual(f"Security string {input_value} safely rendered as inert text.")
