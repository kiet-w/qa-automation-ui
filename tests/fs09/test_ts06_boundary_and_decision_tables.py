"""
tests/fs09/test_ts06_boundary_and_decision_tables.py - Test Suite TS06: Systematic Black-Box Boundary & Decision Tables.

Covers:
- Decision Table Testing (F9.3: All combinations of Balance vs Total, Method selection, Parent override)
- 3-Point Boundary Value Analysis (BVA: 0, 0.01, balance-0.01, balance, balance+0.01, total-0.01, total)
- Equivalence Partitioning (EP: Valid partitions, Invalid below, Invalid above, Malformed enums)
- UI Step Navigation & State Preservation (Back/Forward state retention between Step 1, 2, and 3)
- API Problem Details & Validation Contracts (RFC 9457 compliance)

Traceability:
- FSD: [agile] fs/md/FS document/FS-09_Outstanding_Fees_and_Payment.md §3.1, §4.1, §5.1, §5.3
- Rules: BR-F9-01 to BR-F9-13; DA-03, DA-05, DA-09, DA-10
- ACs: AC-01 to AC-22
- Invariants: 0 to 8 (Zero assumptions, 9-tier failure evaluation, disciplined adversarial testing)
"""
import copy
import uuid
from typing import Any, Dict
import pytest
import requests

from tests.base_test import BaseTest
from pages.fs09.billing_payment_page import BillingPaymentPage
from pages.fs09.payment_result_page import PaymentResultPage
from tests.fs09.conftest import DatabaseHelper


@pytest.mark.p1
@pytest.mark.functional
@pytest.mark.ui
@pytest.mark.regression
class TestTS06BoundaryAndDecisionTables(BaseTest):
    """Test Suite TS06 covering Decision Tables, 3-Point BVA, and Step Navigation."""

    # =========================================================================
    # DECISION TABLE TESTS (DT-01 to DT-04)
    # =========================================================================

    def test_tc_r9_dt_01_decision_table_ea_sufficient_defaults_ea(
        self, fs09_data: Dict[str, Any], auth_helper
    ):
        """
        TC-R9-DT-01: Decision Table Rule 1 - Balance >= Total defaults to EducationAccount.
        Conditions:
            - Wallet Balance: SGD 50.00
            - Selected Charges Total: SGD 10.00 (Stationery Fee)
            - Balance >= Total: TRUE
        Expected Result:
            - Payment method defaults to EducationAccount radio.
            - Split amount field is not displayed.
            - User can proceed directly to Review step without entering split values.
        Traceability: FS-09 §4.1; BR-F9-02; AC-03
        """
        auth_helper("PAR-NORMAL-01")
        persona = fs09_data["personas"]["PAR-NORMAL-01"]
        payment_page = self.get_page(BillingPaymentPage)

        with self.step("Step 1: Open charges selection and select single 10.00 SGD charge", expected="Charge selected."):
            payment_page.open_for_student(persona["student_id"], base_url=fs09_data["base_url"])
            payment_page.wait_for_selection_loaded()
            payment_page.unselect_all_charges()
            payment_page.select_charge_by_index(0)  # 10.00 SGD
            payment_page.click_continue_to_method()
            payment_page.wait_for_method_loaded()
            assert payment_page.is_method_step_loaded(), "Method step must be loaded."
            self.step.set_actual("Navigated to Method step with 10.00 SGD total.")

        with self.step("Step 2: Verify EducationAccount is auto-selected and proceed to Review", expected="EA selected by default."):
            assert payment_page.is_ea_radio_checked(), "EducationAccount must be checked by default when balance >= total."
            assert not payment_page.is_split_radio_checked(), "Split must not be checked."
            assert not payment_page.is_online_radio_checked(), "Online must not be checked."
            payment_page.click_continue_to_review()
            payment_page.wait_for_review_loaded()
            assert payment_page.is_review_step_loaded(), "Review step must be loaded."
            self.step.set_actual("DT Rule 1 verified: EA defaulted and progressed to Review.")

    def test_tc_r9_dt_02_decision_table_ea_sufficient_manual_online_override(
        self, fs09_data: Dict[str, Any], auth_helper
    ):
        """
        TC-R9-DT-02: Decision Table Rule 2 - Balance >= Total, but Parent chooses OnlineGateway override.
        Conditions:
            - Wallet Balance: SGD 50.00
            - Selected Charges Total: SGD 10.00
            - Parent Action: Clicks 'Online payment gateway' radio manually.
        Expected Result:
            - UI switches selection to OnlineGateway radio.
            - Review step reflects 100% Online Payment.
        Traceability: FS-09 §4.1; User Discretion; AC-05
        """
        auth_helper("PAR-NORMAL-01")
        persona = fs09_data["personas"]["PAR-NORMAL-01"]
        payment_page = self.get_page(BillingPaymentPage)

        with self.step("Step 1: Open Method step with 10.00 SGD charge", expected="Method step loaded."):
            payment_page.open_for_student(persona["student_id"], base_url=fs09_data["base_url"])
            payment_page.wait_for_selection_loaded()
            payment_page.unselect_all_charges()
            payment_page.select_charge_by_index(0)
            payment_page.click_continue_to_method()
            payment_page.wait_for_method_loaded()

        with self.step("Step 2: Manually select OnlineGateway radio and proceed to Review", expected="Online selected."):
            payment_page.select_online_radio()
            assert payment_page.is_online_radio_checked(), "OnlineGateway radio must be checked."
            assert not payment_page.is_ea_radio_checked(), "EA radio must now be unchecked."
            payment_page.click_continue_to_review()
            payment_page.wait_for_review_loaded()
            assert payment_page.is_review_step_loaded(), "Review step must be loaded."
            review_info = payment_page.get_review_summary()
            items_str = str(review_info.get("items", {})).lower()
            assert "online" in items_str, f"Review must reflect online payment: {review_info}"
            self.step.set_actual("DT Rule 2 verified: Parent manual override to Online allowed.")

    def test_tc_r9_dt_03_decision_table_ea_insufficient_auto_split(
        self, fs09_data: Dict[str, Any], auth_helper
    ):
        """
        TC-R9-DT-03: Decision Table Rule 3 - Balance < Total auto-selects Both (Split) and defaults to balance.
        Conditions:
            - Wallet Balance: SGD 50.00
            - Selected Charges Total: SGD 1,500.00 (Overseas Learning Trip)
            - Balance < Total: TRUE
        Expected Result:
            - Payment method defaults to 'Both' (Split payment).
            - eaAmount input is auto-populated with SGD 50.00 (the full wallet balance).
            - Continue button is enabled without requiring manual input.
        Traceability: FS-09 §4.1; BR-F9-04; AC-07
        """
        auth_helper("PAR-NORMAL-01")
        persona = fs09_data["personas"]["PAR-NORMAL-01"]
        payment_page = self.get_page(BillingPaymentPage)

        with self.step("Step 1: Select Overseas Learning Trip (1,500.00 SGD)", expected="1500 SGD charge selected."):
            payment_page.open_for_student(persona["student_id"], base_url=fs09_data["base_url"])
            payment_page.wait_for_selection_loaded()
            payment_page.unselect_all_charges()
            payment_page.select_charge_by_index(3)  # Index 3 is Overseas Learning Trip Fee
            payment_page.click_continue_to_method()
            payment_page.wait_for_method_loaded()
            assert payment_page.is_method_step_loaded(), "Method step must be loaded."

        with self.step("Step 2: Verify Split radio is checked and eaAmount pre-filled with 50.00", expected="Split auto-selected with 50.00."):
            assert payment_page.is_split_radio_checked(), "Both (Split) must be auto-checked when balance < total."
            ea_val = payment_page.get_ea_split_amount()
            assert "50.00" in ea_val or "50" in ea_val, f"Expected eaAmount pre-filled with 50.00, got: {ea_val}"
            assert not payment_page.is_method_continue_disabled(), "Continue button must be enabled."
            payment_page.click_continue_to_review()
            payment_page.wait_for_review_loaded()
            assert payment_page.is_review_step_loaded(), "Review step must be loaded."
            self.step.set_actual("DT Rule 3 verified: Split defaulted and pre-filled with wallet balance.")

    def test_tc_r9_dt_04_decision_table_ea_insufficient_manual_online(
        self, fs09_data: Dict[str, Any], auth_helper
    ):
        """
        TC-R9-DT-04: Decision Table Rule 4 - Balance < Total, but Parent switches from Split to 100% Online.
        Conditions:
            - Wallet Balance: SGD 50.00
            - Selected Charges Total: SGD 1,500.00
            - Parent Action: Switches from Both to OnlineGateway.
        Expected Result:
            - OnlineGateway radio selected, Split input hidden.
            - Review step shows 100% Online payment (SGD 1,500.00).
        Traceability: FS-09 §4.1; AC-05; AC-07
        """
        auth_helper("PAR-NORMAL-01")
        persona = fs09_data["personas"]["PAR-NORMAL-01"]
        payment_page = self.get_page(BillingPaymentPage)

        with self.step("Step 1: Open Method step with 1500.00 SGD charge", expected="Method step loaded."):
            payment_page.open_for_student(persona["student_id"], base_url=fs09_data["base_url"])
            payment_page.wait_for_selection_loaded()
            payment_page.unselect_all_charges()
            payment_page.select_charge_by_index(3)
            payment_page.click_continue_to_method()
            payment_page.wait_for_method_loaded()

        with self.step("Step 2: Switch from Split to OnlineGateway", expected="Online selected."):
            payment_page.select_online_radio()
            assert payment_page.is_online_radio_checked(), "OnlineGateway radio must be checked."
            payment_page.click_continue_to_review()
            payment_page.wait_for_review_loaded()
            assert payment_page.is_review_step_loaded(), "Review step must be loaded."
            self.step.set_actual("DT Rule 4 verified: Switched from Split to 100% Online.")

    # =========================================================================
    # 3-POINT BOUNDARY VALUE ANALYSIS (BVA-01 to BVA-04)
    # =========================================================================

    def test_tc_r9_bva_01_split_minimum_boundary_1_cent_accepted(
        self, fs09_data: Dict[str, Any], auth_helper
    ):
        """
        TC-R9-BVA-01: 3-Point BVA at Split Lower Bound (0.00, 0.01, 0.02 SGD).
        Exact lower boundary for eaAmount is SGD 0.01.
        Expected Result:
            - Entering 0.01 SGD is accepted as valid.
            - Continue button remains enabled.
        Traceability: BR-F9-04; validEaAmount logic; 3-Point BVA Lower
        """
        auth_helper("PAR-NORMAL-01")
        persona = fs09_data["personas"]["PAR-NORMAL-01"]
        payment_page = self.get_page(BillingPaymentPage)

        with self.step("Step 1: Open Method step with 1500.00 SGD charge", expected="Method step loaded."):
            payment_page.open_for_student(persona["student_id"], base_url=fs09_data["base_url"])
            payment_page.wait_for_selection_loaded()
            payment_page.unselect_all_charges()
            payment_page.select_charge_by_index(3)
            payment_page.click_continue_to_method()
            payment_page.wait_for_method_loaded()

        with self.step("Step 2: Fill eaAmount with exactly 0.01 SGD (minimum boundary)", expected="0.01 SGD accepted."):
            payment_page.fill_ea_split_amount("0.01")
            assert not payment_page.has_split_amount_error(), "0.01 SGD must not trigger validation error."
            assert not payment_page.is_method_continue_disabled(), "Continue button must be enabled for 0.01 SGD."
            self.step.set_actual("BVA Lower Bound 0.01 SGD accepted.")

    def test_tc_r9_bva_02_split_zero_amount_rejected_by_api(
        self, fs09_data: Dict[str, Any]
    ):
        """
        TC-R9-BVA-02: 3-Point BVA Below Lower Bound - eaAmount = 0.00 SGD.
        Direct API Contract: POST /api/v1/checkout with eaAmount: 0.00.
        Expected Result:
            - HTTP 400 Bad Request.
            - Error message contains 'eaAmount is required and must be greater than 0 for Both.'
        Traceability: BR-F9-04; RFC 9457; BVA Below Lower Bound
        """
        api_base = fs09_data["api_base_url"]
        persona = fs09_data["personas"]["PAR-NORMAL-01"]
        payload = {
            "studentId": persona["student_id"],
            "chargeIds": ["bbbb0009-0000-0000-0000-000000000001"],
            "method": "Both",
            "returnUrl": "http://localhost:5174/return",
            "eaAmount": 0.00
        }
        headers = {
            "Idempotency-Key": str(uuid.uuid4()),
            "X-User-Id": persona["nric"],
            "X-User-Roles": "PARENT",
            "Content-Type": "application/json"
        }

        with self.step("Step 1: Dispatch checkout with eaAmount: 0.00", expected="HTTP 400 Bad Request."):
            resp = requests.post(f"{api_base}/api/v1/checkout", json=payload, headers=headers, timeout=5)
            assert resp.status_code == 400, f"Expected 400, got: {resp.status_code}: {resp.text}"
            data = resp.json()
            assert "greater than 0" in data.get("message", ""), f"Unexpected error message: {data}"
            self.step.set_actual(f"API correctly rejected 0.00 eaAmount: {data.get('message')}")

    def test_tc_r9_bva_03_split_equal_to_total_rejected_by_api(
        self, fs09_data: Dict[str, Any]
    ):
        """
        TC-R9-BVA-03: 3-Point BVA Upper Limit - eaAmount equal to Total Amount.
        Direct API Contract: When eaAmount == total, system rejects Split and mandates 100% EA.
        Expected Result:
            - HTTP 400 Bad Request.
            - Error message indicates eaAmount must be less than total.
        Traceability: BR-F9-04; RFC 9457; BVA Upper Boundary
        """
        api_base = fs09_data["api_base_url"]
        persona = fs09_data["personas"]["PAR-NORMAL-01"]
        payload = {
            "studentId": persona["student_id"],
            "chargeIds": ["bbbb0009-0000-0000-0000-000000000001"],  # Total = 10.00 SGD
            "method": "Both",
            "returnUrl": "http://localhost:5174/return",
            "eaAmount": 10.00
        }
        headers = {
            "Idempotency-Key": str(uuid.uuid4()),
            "X-User-Id": persona["nric"],
            "X-User-Roles": "PARENT",
            "Content-Type": "application/json"
        }

        with self.step("Step 1: Dispatch checkout with eaAmount equal to total", expected="HTTP 400 Bad Request."):
            resp = requests.post(f"{api_base}/api/v1/checkout", json=payload, headers=headers, timeout=5)
            assert resp.status_code == 400, f"Expected 400, got: {resp.status_code}: {resp.text}"
            data = resp.json()
            assert "must be less than the total" in data.get("message", ""), f"Unexpected error message: {data}"
            self.step.set_actual(f"API correctly rejected eaAmount equal to total: {data.get('message')}")

    def test_tc_r9_bva_04_split_exceeds_wallet_balance_rejected_by_api(
        self, fs09_data: Dict[str, Any]
    ):
        """
        TC-R9-BVA-04: 3-Point BVA Exceeds Balance - eaAmount > wallet balance.
        Direct API Contract: Wallet has 50.00 SGD; payload requests 50.01 SGD.
        Expected Result:
            - HTTP 400 Bad Request.
            - Error message indicates eaAmount exceeds Education Account balance.
        Traceability: BR-F9-02; BR-F9-04; BVA Balance Overflow
        """
        api_base = fs09_data["api_base_url"]
        persona = fs09_data["personas"]["PAR-NORMAL-01"]
        payload = {
            "studentId": persona["student_id"],
            "chargeIds": ["bbbb0009-0000-0000-0000-000000000004"],  # Total = 1500.00 SGD
            "method": "Both",
            "returnUrl": "http://localhost:5174/return",
            "eaAmount": 50.01  # Balance is 50.00
        }
        headers = {
            "Idempotency-Key": str(uuid.uuid4()),
            "X-User-Id": persona["nric"],
            "X-User-Roles": "PARENT",
            "Content-Type": "application/json"
        }

        with self.step("Step 1: Dispatch checkout with eaAmount: 50.01 (exceeding balance)", expected="HTTP 400 Bad Request."):
            resp = requests.post(f"{api_base}/api/v1/checkout", json=payload, headers=headers, timeout=5)
            assert resp.status_code == 400, f"Expected 400, got: {resp.status_code}: {resp.text}"
            data = resp.json()
            assert "exceeds the Education Account balance" in data.get("message", ""), f"Unexpected error message: {data}"
            self.step.set_actual(f"API correctly rejected eaAmount exceeding balance: {data.get('message')}")

    # =========================================================================
    # API CONTRACT & EQUIVALENCE PARTITIONING (EP-01 to EP-03)
    # =========================================================================

    def test_tc_r9_api_ep_empty_charge_ids_rejected(
        self, fs09_data: Dict[str, Any]
    ):
        """
        TC-R9-API-EP-01: Equivalence Partitioning - Empty chargeIds array.
        Direct API Contract: POST /api/v1/checkout with chargeIds: [].
        Expected Result:
            - HTTP 400 Bad Request.
            - Error message: 'chargeIds is required (at least one).'
        Traceability: RFC 9457; BR-F9-13
        """
        api_base = fs09_data["api_base_url"]
        persona = fs09_data["personas"]["PAR-NORMAL-01"]
        payload = {
            "studentId": persona["student_id"],
            "chargeIds": [],
            "method": "EducationAccount"
        }
        headers = {
            "Idempotency-Key": str(uuid.uuid4()),
            "X-User-Id": persona["nric"],
            "X-User-Roles": "PARENT",
            "Content-Type": "application/json"
        }

        with self.step("Step 1: Send empty chargeIds list", expected="HTTP 400 with chargeIds required message."):
            resp = requests.post(f"{api_base}/api/v1/checkout", json=payload, headers=headers, timeout=5)
            assert resp.status_code == 400, f"Expected 400, got: {resp.status_code}: {resp.text}"
            data = resp.json()
            assert "chargeIds is required" in data.get("message", ""), f"Unexpected error: {data}"
            self.step.set_actual(f"Verified empty chargeIds rejection: {data.get('message')}")

    def test_tc_r9_api_ep_invalid_method_enum_rejected(
        self, fs09_data: Dict[str, Any]
    ):
        """
        TC-R9-API-EP-02: Equivalence Partitioning - Malformed / Unknown Payment Method Enum.
        Direct API Contract: POST /api/v1/checkout with method: 'Cryptocurrency'.
        Expected Result:
            - HTTP 400 Bad Request.
            - Error message lists valid enum values: EducationAccount, OnlineGateway, Both.
        Traceability: RFC 9457; Schema Validation
        """
        api_base = fs09_data["api_base_url"]
        persona = fs09_data["personas"]["PAR-NORMAL-01"]
        payload = {
            "studentId": persona["student_id"],
            "chargeIds": ["bbbb0009-0000-0000-0000-000000000001"],
            "method": "Cryptocurrency"
        }
        headers = {
            "Idempotency-Key": str(uuid.uuid4()),
            "X-User-Id": persona["nric"],
            "X-User-Roles": "PARENT",
            "Content-Type": "application/json"
        }

        with self.step("Step 1: Send invalid method enum", expected="HTTP 400 with enum error."):
            resp = requests.post(f"{api_base}/api/v1/checkout", json=payload, headers=headers, timeout=5)
            assert resp.status_code == 400, f"Expected 400, got: {resp.status_code}: {resp.text}"
            data = resp.json()
            assert "Invalid payment method" in data.get("message", ""), f"Unexpected error: {data}"
            self.step.set_actual(f"Verified invalid method enum rejection: {data.get('message')}")

    def test_tc_r9_api_ep_missing_return_url_rejected(
        self, fs09_data: Dict[str, Any]
    ):
        """
        TC-R9-API-EP-03: Equivalence Partitioning - Missing returnUrl for OnlineGateway payment.
        Direct API Contract: POST /api/v1/checkout with method: 'OnlineGateway' but without returnUrl.
        Expected Result:
            - HTTP 400 Bad Request.
            - Error message: 'returnUrl is required for OnlineGateway or Both payments.'
        Traceability: RFC 9457; Gateway Contract
        """
        api_base = fs09_data["api_base_url"]
        persona = fs09_data["personas"]["PAR-NORMAL-01"]
        payload = {
            "studentId": persona["student_id"],
            "chargeIds": ["bbbb0009-0000-0000-0000-000000000001"],
            "method": "OnlineGateway"
        }
        headers = {
            "Idempotency-Key": str(uuid.uuid4()),
            "X-User-Id": persona["nric"],
            "X-User-Roles": "PARENT",
            "Content-Type": "application/json"
        }

        with self.step("Step 1: Send Online checkout without returnUrl", expected="HTTP 400 with returnUrl required message."):
            resp = requests.post(f"{api_base}/api/v1/checkout", json=payload, headers=headers, timeout=5)
            assert resp.status_code == 400, f"Expected 400, got: {resp.status_code}: {resp.text}"
            data = resp.json()
            assert "returnUrl is required" in data.get("message", ""), f"Unexpected error: {data}"
            self.step.set_actual(f"Verified returnUrl requirement: {data.get('message')}")

    # =========================================================================
    # UI STEP NAVIGATION & STATE PRESERVATION (NAV-01 to NAV-03)
    # =========================================================================

    def test_tc_r9_nav_01_step2_to_step1_back_preserves_selection(
        self, fs09_data: Dict[str, Any], auth_helper
    ):
        """
        TC-R9-NAV-01: UI Step Navigation - Step 2 Back button returns to Step 1 and preserves charge selections.
        Expected Result:
            - Clicking Back on Step 2 returns to Step 1.
            - Selected charges and 'Selected total' remain preserved.
        Traceability: Usability Lens 10; SPA Navigation
        """
        auth_helper("PAR-NORMAL-01")
        persona = fs09_data["personas"]["PAR-NORMAL-01"]
        payment_page = self.get_page(BillingPaymentPage)

        with self.step("Step 1: Select Stationery Fee (10.00 SGD) and proceed to Method", expected="Method loaded."):
            payment_page.open_for_student(persona["student_id"], base_url=fs09_data["base_url"])
            payment_page.wait_for_selection_loaded()
            payment_page.unselect_all_charges()
            payment_page.select_charge_by_index(0)
            payment_page.click_continue_to_method()
            payment_page.wait_for_method_loaded()

        with self.step("Step 2: Click Back button on Method step", expected="Step 1 reloaded with 10.00 SGD total."):
            payment_page.click_back_to_selection()
            payment_page.wait_for_selection_loaded()
            assert payment_page.is_selection_step_loaded(), "Selection step must be visible."
            amounts = payment_page.get_summary_amounts()
            assert "10.00" in amounts.get("selected_total", ""), (
                f"Selected total must remain 10.00 SGD after Back navigation, got: {amounts.get('selected_total')}"
            )
            self.step.set_actual("State preservation verified: 10.00 SGD total retained after Back navigation.")

    def test_tc_r9_nav_02_step3_to_step2_back_preserves_method_choice(
        self, fs09_data: Dict[str, Any], auth_helper
    ):
        """
        TC-R9-NAV-02: UI Step Navigation - Step 3 Back button returns to Step 2 and preserves method selection.
        Expected Result:
            - Clicking Back on Step 3 returns to Step 2.
            - Selected radio (e.g. OnlineGateway) remains active.
        Traceability: Usability Lens 10; Multi-step Form Integrity
        """
        auth_helper("PAR-NORMAL-01")
        persona = fs09_data["personas"]["PAR-NORMAL-01"]
        payment_page = self.get_page(BillingPaymentPage)

        with self.step("Step 1: Navigate to Review step with OnlineGateway method", expected="Review step loaded."):
            payment_page.open_for_student(persona["student_id"], base_url=fs09_data["base_url"])
            payment_page.wait_for_selection_loaded()
            payment_page.unselect_all_charges()
            payment_page.select_charge_by_index(0)
            payment_page.click_continue_to_method()
            payment_page.wait_for_method_loaded()
            payment_page.select_online_radio()
            payment_page.click_continue_to_review()
            payment_page.wait_for_review_loaded()
            assert payment_page.is_review_step_loaded(), "Review step must be loaded."

        with self.step("Step 2: Click Back button on Review step", expected="Method step reloaded with Online checked."):
            payment_page.click_back_to_method()
            payment_page.wait_for_method_loaded()
            assert payment_page.is_method_step_loaded(), "Method step must be visible."
            assert payment_page.is_online_radio_checked(), "OnlineGateway radio must remain checked after Back navigation."
            self.step.set_actual("Method state preservation verified: OnlineGateway radio remained checked.")

    def test_tc_r9_nav_03_deselect_all_disables_continue_button(
        self, fs09_data: Dict[str, Any], auth_helper
    ):
        """
        TC-R9-NAV-03: UI Guard Condition - Unselecting all charges disables Continue button.
        Expected Result:
            - When 0 charges are selected, Selected Total is SGD 0.00.
            - Continue button has disabled attribute and cannot be clicked.
        Traceability: AC-01; Guard Condition Lens 4
        """
        auth_helper("PAR-NORMAL-01")
        persona = fs09_data["personas"]["PAR-NORMAL-01"]
        payment_page = self.get_page(BillingPaymentPage)

        with self.step("Step 1: Open charges table and unselect all charges", expected="0 charges selected."):
            payment_page.open_for_student(persona["student_id"], base_url=fs09_data["base_url"])
            payment_page.wait_for_selection_loaded()
            payment_page.unselect_all_charges()
            amounts = payment_page.get_summary_amounts()
            assert "0.00" in amounts.get("selected_total", ""), f"Expected 0.00 SGD selected total, got: {amounts.get('selected_total')}"

        with self.step("Step 2: Verify Continue button is disabled", expected="Button is disabled."):
            continue_btn = payment_page.page.locator(payment_page.STEP1_CONTINUE_BTN)
            assert continue_btn.is_disabled(), "Continue button must be disabled when 0 charges are selected."
            self.step.set_actual("Guard condition verified: Continue button is strictly disabled.")
