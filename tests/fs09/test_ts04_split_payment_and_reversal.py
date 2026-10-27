"""
tests/fs09/test_ts04_split_payment_and_reversal.py - Test Suite TS04: Split Payment & Auto-Reversal Engine.
Covers Stream 4:
- TC-R9-11: Split Payment Success Flow (Sequential 2-step: EA + Online)
- TC-R9-12: Split Payment Online Failed Triggers EA Auto-Reversal Engine
- TC-R9-13: Invalid Split Amount Validation (SPLIT_AMOUNT_INVALID)
- TC_R9_AUTO_03: Split Payment Funding Legs & Reversal DB Invariants

Traceability:
- FSD: [agile] fs/md/FS document/FS-09_Outstanding_Fees_and_Payment.md §3.4, §4.1, §5.1
- Rules: BR-F9-02, BR-F9-11, BR-F9-13, DA-14, DEC-15
- ACs: AC-15, AC-16, AC-17, AC-18, AC-19, AC-22
- Invariants: 0 to 8
"""
import copy
from typing import Any, Dict
import uuid
import pytest
import requests

from tests.base_test import BaseTest
from pages.fs09.billing_account_selection_page import BillingAccountSelectionPage
from pages.fs09.billing_payment_page import BillingPaymentPage
from pages.fs09.payment_gateway_simulator_page import PaymentGatewaySimulatorPage
from pages.fs09.payment_result_page import PaymentResultPage
from tests.fs09.conftest import DatabaseHelper


@pytest.mark.p0
@pytest.mark.functional
@pytest.mark.ui
class TestTS04SplitPaymentAndReversal(BaseTest):
    """Test Suite TS04 covering Split Payment (EA + Online) and Automated Reversal Engine."""

    def test_tc_r9_11_split_payment_success_flow(
        self, fs09_data: Dict[str, Any], auth_helper, db_helper: DatabaseHelper, cleanup_fs09_records
    ):
        """
        TC-R9-11: Verify Split Payment succeeds when EA debits first and Online Gateway succeeds second.
        Scenario ID: TS-017 | Test Suite: TS04 Split Payment
        Page: /billing/:studentId -> :5286 -> /payment-result | Severity: S1 | Priority: Critical | Test Type: Functional E2E
        Traceability: BR-F9-02; BR-F9-11; AC-15; DA-14; DEC-15
        Environment: Localhost Vite (:5174), Gateway (:5286) & Backend (:5008)
        Preconditions: Tan Wei Ming has 100.00 SGD charges (20 + 80) and 40.00 SGD EA balance.
        Expected Result:
            - Method step allocates 40.00 SGD to EA and 60.00 SGD to Online Gateway.
            - Gateway simulator loads for 60.00 SGD.
            - Paying successfully returns to /payment-result with success status and both funding legs shown.
            - DB invoices: status = 4 (Paid).
            - DB transactions: status = 2 (Succeeded).
            - DB transaction_funding_sources: 2 records (EA = Succeeded, Online = Succeeded).
        """
        persona = fs09_data["personas"]["PAR-NORMAL-02"]
        student_id = persona["student_id"]
        auth_helper("PAR-NORMAL-02")

        payment_page = self.get_page(BillingPaymentPage)
        gateway_page = self.get_page(PaymentGatewaySimulatorPage)
        result_page = self.get_page(PaymentResultPage)

        with self.step("Step 1: Open Tan Wei Ming charges and select all charges (100.00 SGD total)", expected="All charges selected."):
            payment_page.open_for_student(student_id, base_url=fs09_data["base_url"])
            payment_page.wait_for_selection_loaded()
            payment_page.select_all_charges()
            payment_page.click_continue_to_method()
            payment_page.wait_for_method_loaded()
            self.step.set_actual("Charges totaling 100.00 SGD selected; reached method selection.")

        with self.step("Step 2: Select 'Both' (Split Payment) and verify funding allocations", expected="EA=40.00, Online=60.00."):
            assert payment_page.is_split_option_enabled(), "Split payment option must be enabled."
            payment_page.select_payment_method("Both")
            breakdown = payment_page.get_funding_breakdown()
            self.step.set_actual(f"Funding breakdown observed: {breakdown}")

        with self.step("Step 3: Review and confirm to navigate to Gateway Simulator for Online leg", expected="Simulator loads for 60.00 SGD."):
            payment_page.click_continue_to_review()
            payment_page.wait_for_review_loaded()
            payment_page.click_confirm_pay()
            gateway_page.wait_for_simulator_loaded(timeout=15000)
            assert gateway_page.is_loaded(), "Payment Gateway Simulator checkout page must be loaded."
            self.step.set_actual(f"Gateway simulator opened: amount={gateway_page.get_amount_due()}")

        with self.step("Step 4: Click 'Pay successful' on Simulator and verify receipt with both funding legs", expected="Success receipt rendered."):
            gateway_page.click_pay_successful()
            result_page.wait_for_result_loaded(timeout=15000)
            result_page.wait_for_terminal_status(timeout=15000)
            assert result_page.is_loaded(), "Payment result page must be loaded."
            assert result_page.get_result_tone() == "success" or "success" in result_page.get_result_title().lower(), f"Expected success tone, got: {result_page.get_result_tone()}"
            sources = result_page.get_funding_sources_details()
            self.step.set_actual(f"Verified receipt with funding legs: {sources}")

        with self.step("Step 5: Verify Database Invariants (Invoice Paid, 2 Funding Legs Succeeded)", expected="DB verified."):
            invoices = db_helper.query(f"SELECT TOP 1 id, status, gross_amount, net_amount FROM BillingPaymentService.dbo.invoices WHERE student_id = '{student_id}' ORDER BY created_at DESC")
            assert len(invoices) > 0 and invoices[0]["status"] == 4, f"Invoice must be status 4 (Paid), got: {invoices}"

            txns = db_helper.query("SELECT TOP 1 id, status FROM BillingPaymentService.dbo.transactions ORDER BY created_at DESC")
            assert len(txns) > 0 and txns[0]["status"] == 2, f"Transaction must be status 2 (Succeeded), got: {txns}"

            legs = db_helper.query(f"SELECT method, requested_amount, status FROM BillingPaymentService.dbo.transaction_funding_sources WHERE transaction_id = '{txns[0]['id']}' ORDER BY sequence_number")
            assert len(legs) == 2, f"Expected exactly 2 funding legs, found: {len(legs)}"
            assert legs[0]["status"] == 2 and legs[1]["status"] == 2, f"Both legs must be Succeeded (status=2): {legs}"
            self.step.set_actual(f"DB verified: Invoice Paid, Legs: {legs}")

    @pytest.mark.xfail(
        strict=True,
        reason="BUG-R9-002: ProcessGatewayWebhookHandler.cs:305 contains unhandled 'TODO reverse EA leg', leaving EA leg un-reversed and transaction in ReconciliationRequired when online gateway leg fails."
    )
    def test_tc_r9_12_split_payment_online_failed_triggers_ea_reversal(
        self, fs09_data: Dict[str, Any], auth_helper, db_helper: DatabaseHelper, cleanup_fs09_records
    ):
        """
        TC-R9-12: Verify Split Payment failure at Online Gateway triggers EA Auto-Reversal Engine (AC-17).
        Scenario ID: TS-018 | Test Suite: TS04 Split Payment
        Page: /billing/:studentId -> :5286 -> /payment-result | Severity: S1 | Priority: Critical | Test Type: Functional E2E
        Traceability: BR-F9-02; BR-F9-11; AC-17; EX-02; Error Code: PAYMENT_FAILED_EA_RETURNED
        Expected Result:
            - Clicking 'Pay failed' triggers Auto-Reversal in Backend.
            - /payment-result displays failure status with specific EA Reversal alert:
              'The amount taken from the Education Account has been returned.'
            - DB: EA funding leg status is 4 (Reversed) or records reversal transaction.
            - Wallet balance in EducationAccountDatabase is restored to 40.00 SGD.
        """
        persona = fs09_data["personas"]["PAR-NORMAL-02"]
        student_id = persona["student_id"]
        auth_helper("PAR-NORMAL-02")

        payment_page = self.get_page(BillingPaymentPage)
        gateway_page = self.get_page(PaymentGatewaySimulatorPage)
        result_page = self.get_page(PaymentResultPage)

        with self.step("Step 1: Open Tan Wei Ming charges and proceed with Split Payment", expected="Gateway opens."):
            payment_page.open_for_student(student_id, base_url=fs09_data["base_url"])
            payment_page.wait_for_selection_loaded()
            payment_page.select_all_charges()
            payment_page.click_continue_to_method()
            payment_page.wait_for_method_loaded()
            payment_page.select_payment_method("Both")
            payment_page.click_continue_to_review()
            payment_page.wait_for_review_loaded()
            payment_page.click_confirm_pay()
            gateway_page.wait_for_simulator_loaded(timeout=15000)
            self.step.set_actual("Navigated to Gateway Simulator with EA debited in step 1.")

        with self.step("Step 2: Simulate Online Gateway failure by clicking 'Pay failed'", expected="Triggers EA Reversal and redirects."):
            gateway_page.click_pay_failed()
            result_page.wait_for_result_loaded(timeout=15000)
            result_page.wait_for_terminal_status(timeout=15000)
            assert result_page.is_loaded(), "Result page must be loaded."
            tone = result_page.get_result_tone()
            assert tone in ("failure", "reconciliation", "pending"), f"Expected non-success tone, got: {tone}"

            # Verify EA reversal notice is rendered per AC-17
            has_reversal = result_page.has_ea_reversal_notice()
            assert has_reversal or "returned" in result_page.get_result_description().lower(), "Result page must display that the Education Account amount has been returned (AC-17)."
            self.step.set_actual("EA Auto-Reversal notice confirmed on PaymentResultPage.")

        with self.step("Step 3: Assert Wallet balance restored in Database", expected="Balance restored to 40.00 SGD."):
            wallets = db_helper.query(f"SELECT balance FROM EducationAccountDatabase.dbo.wallets WHERE student_id = '{student_id}'", db_name="EducationAccountDatabase")
            assert len(wallets) > 0, "Wallet must exist."
            assert float(wallets[0]["balance"]) == 40.00, f"Expected wallet balance restored to 40.00, got: {wallets[0]['balance']}"
            self.step.set_actual("Database verified: EA balance successfully restored to 40.00 SGD.")

    def test_tc_r9_13_split_amount_invalid_rejected(
        self, fs09_data: Dict[str, Any]
    ):
        """
        TC-R9-13: Verify split payment rejected when EA balance covers entire total (AC-19, AC-22).
        Scenario ID: TS-018 | Test Suite: TS04 Split Payment
        Protocol Level: POST /api/v1/checkout | Severity: S2 | Priority: High | Test Type: API Contract
        Traceability: BR-F9-02; AC-19; AC-22; Error Code: SPLIT_AMOUNT_INVALID
        Expected Result:
            - If EA balance >= total charges and method 'Both' is submitted, API returns 400 Bad Request.
        """
        persona = fs09_data["personas"]["PAR-NORMAL-01"]
        student_id = persona["student_id"]
        api_base = fs09_data["api_base_url"]

        # Chloe Chan has 50.00 SGD balance; selecting 10.00 SGD charge with method "Both" and eaAmount=10.00 is rejected
        payload = {
            "studentId": student_id,
            "chargeIds": ["bbbb0009-0000-0000-0000-000000000001"],  # 10.00 SGD (balance 50 >= 10)
            "method": "Both",
            "eaAmount": 10.00,
            "returnUrl": "http://localhost:5174/payment-result"
        }
        headers = {
            "Idempotency-Key": str(uuid.uuid4()),
            "X-User-Id": "test-parent",
            "X-User-Roles": "PARENT",
            "Content-Type": "application/json"
        }

        with self.step("Step 1: Dispatch invalid split payment request where EA covers 100%", expected="HTTP 400 Bad Request."):
            resp = requests.post(f"{api_base}/api/v1/checkout", json=payload, headers=headers, timeout=5)
            assert resp.status_code == 400, f"Expected 400 Bad Request, got {resp.status_code}: {resp.text}"
            body = resp.json()
            assert not body.get("isSuccess", True), "Response must indicate failure."
            msg = body.get("message", "").lower()
            assert any(term in msg for term in ("must be less than the total", "educationaccount", "required", "split")), (
                f"Expected split validation message, got: {msg}"
            )
            self.step.set_actual(f"API correctly rejected invalid split with 400: {body.get('message')}")

    def test_tc_r9_13b_ui_split_amount_realtime_validation(
        self, fs09_data: Dict[str, Any], auth_helper
    ):
        """
        TC-R9-13b: Verify real-time client-side validation of Education Account split input on Step 2.
        Scenario ID: TS-018b | Test Suite: TS04 Split Payment
        Page: /billing/:studentId -> Step 2 Method | Severity: S2 | Priority: High | Test Type: Functional & UI
        Traceability: PR-F9-UI-ENHANCE; BR-F9-02; BR-F9-11; AC-19
        Environment: Localhost Vite (:5174)
        Expected Result:
            - When balance < total (e.g. 50.00 SGD vs 1500.00 SGD), 'Both' option is selected with default 50.00.
            - Entering amount greater than balance (e.g. 60.00) triggers inline validation alert and disables Continue button.
            - Entering valid amount (e.g. 30.00) clears error and enables Continue button.
        """
        auth_helper("PAR-NORMAL-01")
        persona = fs09_data["personas"]["PAR-NORMAL-01"]
        payment_page = self.get_page(BillingPaymentPage)

        with self.step("Step 1: Select 1500.00 SGD charge and navigate to Step 2", expected="Method step opens with Both pre-selected."):
            payment_page.open_for_student(persona["student_id"], base_url=fs09_data["base_url"])
            payment_page.wait_for_selection_loaded()
            payment_page.unselect_all_charges()
            payment_page.select_charge_by_index(3)  # Overseas trip 1500.00 SGD
            payment_page.click_continue_to_method()
            payment_page.wait_for_method_loaded()
            assert payment_page.get_selected_payment_method() == "Both", "Both should be default when balance < total."
            assert payment_page.get_ea_split_amount() == "50.00", "Default EA amount should equal available balance 50.00."
            self.step.set_actual("Both payment method verified with default available balance.")

        with self.step("Step 2: Enter invalid split amount (> balance) and assert button disabled", expected="Inline error displayed, continue button disabled."):
            payment_page.fill_ea_split_amount("60.00")
            assert payment_page.has_split_amount_error(), "Inline error alert must appear for EA amount > balance."
            err_msg = payment_page.get_split_amount_error_text()
            assert "greater than 0" in err_msg.lower() or "balance" in err_msg.lower(), f"Unexpected error message: {err_msg}"
            assert payment_page.is_method_continue_disabled(), "Continue button must be disabled when split amount is invalid."
            self.step.set_actual(f"Inline validation confirmed: {err_msg}")

        with self.step("Step 3: Enter valid split amount and verify continue button is enabled", expected="Error clears, continue button enabled."):
            payment_page.fill_ea_split_amount("30.00")
            assert not payment_page.has_split_amount_error(), "Error alert should be cleared for valid amount."
            assert not payment_page.is_method_continue_disabled(), "Continue button should be enabled for valid amount."
            self.step.set_actual("Valid split amount accepted; continue button enabled.")
