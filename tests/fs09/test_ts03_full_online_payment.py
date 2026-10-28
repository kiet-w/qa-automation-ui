"""
tests/fs09/test_ts03_full_online_payment.py - Test Suite TS03: Full Online Payment & Sandbox Gateway.
Covers Stream 3:
- TC-R9-08: 100% Online Payment Success via Hosted Sandbox Gateway
- TC-R9-09: Online Payment Cancellation/Failure Leaves Invoice Unpaid
- TC-R9-10: Webhook HMAC-SHA256 Signature Verification & Anti-Tampering
- TC_R9_AUTO_02: Online Payment Webhook Lifecycle & Deduplication Invariants

Traceability:
- FSD: [agile] fs/md/FS document/FS-09_Outstanding_Fees_and_Payment.md §3.3, §4.2, §5.1
- Rules: BR-F9-05, BR-F9-06, BR-F9-07, DA-01, EX-02, EX-06, EX-07, EX-08
- ACs: AC-08, AC-09, AC-10
- Invariants: 0 to 8
"""
import copy
import json
import time
from typing import Any, Dict
import uuid
import pytest
import requests

from tests.base_test import BaseTest
from pages.fs09.billing_account_selection_page import BillingAccountSelectionPage
from pages.fs09.billing_payment_page import BillingPaymentPage
from pages.fs09.payment_gateway_simulator_page import PaymentGatewaySimulatorPage
from pages.fs09.payment_result_page import PaymentResultPage
from tests.fs09.conftest import DatabaseHelper, WebhookSigner


@pytest.mark.p0
@pytest.mark.functional
@pytest.mark.ui
class TestTS03FullOnlinePayment(BaseTest):
    """Test Suite TS03 covering 100% Online Payment, Sandbox Gateway Simulator, and HMAC Webhooks."""

    def test_tc_r9_08_online_payment_success_via_gateway(
        self, fs09_data: Dict[str, Any], auth_helper, db_helper: DatabaseHelper, cleanup_fs09_records
    ):
        """
        TC-R9-08: Verify 100% Online Payment redirects to simulator, completes with Pay Successful, and marks Invoice Paid.
        Scenario ID: TS-015 / TS-016 | Test Suite: TS03 Full Online Payment
        Page: /billing/:studentId -> :5286/checkout/:id -> /payment-result | Severity: S1 | Priority: Critical | Test Type: Functional E2E
        Traceability: BR-F9-05; BR-F9-06; AC-08; AC-10; DA-01
        Environment: Localhost Vite (:5174), Sandbox Gateway (:5286) & Backend (:5008)
        Preconditions: Chloe Chan has charges; parent selects OnlineGateway.
        Expected Result:
            - UI redirects to Hosted Checkout Simulator at http://localhost:5286/checkout/:sessionId.
            - Clicking 'Pay successful' dispatches webhook and redirects back to /payment-result.
            - Result page renders green success banner with receipt.
            - DB invoices table: status = 4 (Paid).
            - DB transactions table: status = 2 (Succeeded).
        """
        persona = fs09_data["personas"]["PAR-NORMAL-01"]
        student_id = persona["student_id"]
        auth_helper("PAR-NORMAL-01")

        payment_page = self.get_page(BillingPaymentPage)
        gateway_page = self.get_page(PaymentGatewaySimulatorPage)
        result_page = self.get_page(PaymentResultPage)

        with self.step("Step 1: Open charges selection and select charge for online payment", expected="Charge selected."):
            payment_page.open_for_student(student_id, base_url=fs09_data["base_url"])
            payment_page.wait_for_selection_loaded()
            payment_page.unselect_all_charges()
            payment_page.select_charge_by_index(0)  # 10.00 SGD Stationery Fee
            payment_page.click_continue_to_method()
            payment_page.wait_for_method_loaded()
            self.step.set_actual("Charge selected; reached method selection.")

        with self.step("Step 2: Choose Online Gateway and proceed through review to pay", expected="Redirects to Simulator."):
            payment_page.select_payment_method("OnlineGateway")
            payment_page.click_continue_to_review()
            payment_page.wait_for_review_loaded()
            payment_page.click_confirm_pay()

            # Wait for navigation to simulator
            gateway_page.wait_for_simulator_loaded(timeout=15000)
            assert gateway_page.is_loaded(), "Payment Gateway Simulator checkout page must be loaded."
            self.step.set_actual("Successfully redirected to Payment Gateway Simulator.")

        with self.step("Step 3: Simulate customer payment success on Gateway", expected="Dispatches webhook and redirects to result page."):
            gateway_page.click_pay_successful()
            result_page.wait_for_result_loaded(timeout=15000)
            result_page.wait_for_terminal_status(timeout=15000)
            assert result_page.is_loaded(), "PaymentResultPage must render."
            assert result_page.get_result_tone() == "success" or "success" in result_page.get_result_title().lower(), f"Expected success tone, got: {result_page.get_result_tone()}"
            self.step.set_actual("Online payment processed; payment result displayed.")

        with self.step("Step 4: Verify Database Invariants (Invoice Paid, Transaction Succeeded)", expected="DB verified."):
            invoices = db_helper.query(f"SELECT TOP 1 id, status, gross_amount FROM BillingPaymentService.dbo.invoices WHERE student_id = '{student_id}' ORDER BY created_at DESC")
            assert len(invoices) > 0 and invoices[0]["status"] == 4, f"Invoice must be status 4 (Paid), got: {invoices}"

            txns = db_helper.query("SELECT TOP 1 status, requested_amount, settled_amount FROM BillingPaymentService.dbo.transactions ORDER BY created_at DESC")
            assert len(txns) > 0 and txns[0]["status"] == 2, f"Transaction must be status 2 (Succeeded), got: {txns}"
            self.step.set_actual("DB records confirmed: Invoice Paid, Transaction Succeeded.")

    def test_tc_r9_09_online_payment_failed_leaves_invoice_issued(
        self, fs09_data: Dict[str, Any], auth_helper, db_helper: DatabaseHelper, cleanup_fs09_records
    ):
        """
        TC-R9-09: Verify Online Payment cancellation/failure leaves invoice unpaid (AC-09, EX-02).
        Scenario ID: TS-016 | Test Suite: TS03 Full Online Payment
        Page: /billing/:studentId -> :5286 -> /payment-result | Severity: S2 | Priority: High | Test Type: Functional
        Traceability: BR-F9-05; AC-09; EX-02; Error Code: PAYMENT_FAILED
        Expected Result:
            - Clicking 'Pay failed' on Gateway simulator redirects back to /payment-result with failure tone.
            - Invoice status in DB remains unpaid (not 4).
        """
        persona = fs09_data["personas"]["PAR-NORMAL-01"]
        student_id = persona["student_id"]
        auth_helper("PAR-NORMAL-01")

        payment_page = self.get_page(BillingPaymentPage)
        gateway_page = self.get_page(PaymentGatewaySimulatorPage)
        result_page = self.get_page(PaymentResultPage)

        with self.step("Step 1: Select charge and initiate Online Checkout", expected="Navigates to simulator."):
            payment_page.open_for_student(student_id, base_url=fs09_data["base_url"])
            payment_page.wait_for_selection_loaded()
            payment_page.unselect_all_charges()
            payment_page.select_charge_by_index(1)  # 15.00 SGD
            payment_page.click_continue_to_method()
            payment_page.wait_for_method_loaded()
            payment_page.select_payment_method("OnlineGateway")
            payment_page.click_continue_to_review()
            payment_page.wait_for_review_loaded()
            payment_page.click_confirm_pay()
            gateway_page.wait_for_simulator_loaded(timeout=15000)
            self.step.set_actual("Arrived at simulator page.")

        with self.step("Step 2: Click 'Pay failed' and observe failure handling", expected="Redirects with failure tone."):
            gateway_page.click_pay_failed()
            result_page.wait_for_result_loaded(timeout=15000)
            assert result_page.is_loaded(), "Result page must be loaded."
            tone = result_page.get_result_tone()
            assert tone in ("failure", "pending"), f"Expected failure or pending tone, got: {tone}"
            self.step.set_actual(f"Failure result rendered with tone: {tone}")

        with self.step("Step 3: Assert Invoice is NOT Paid in DB", expected="Invoice status != 4."):
            invoices = db_helper.query(f"SELECT TOP 1 status FROM BillingPaymentService.dbo.invoices WHERE student_id = '{student_id}' ORDER BY created_at DESC")
            assert len(invoices) > 0 and invoices[0]["status"] != 4, f"Invoice must NOT be Paid, got status: {invoices[0]['status']}"
            self.step.set_actual(f"Verified invoice status in DB is {invoices[0]['status']} (not Paid).")

    def test_tc_r9_10_webhook_hmac_sha256_validation(
        self, fs09_data: Dict[str, Any], webhook_signer: WebhookSigner
    ):
        """
        TC-R9-10: Verify payment webhook endpoint enforces HMAC-SHA256 signature verification (EX-06).
        Scenario ID: TS-019 | Test Suite: TS03 Full Online Payment
        Protocol Level: POST /api/v1/payment-webhooks/gateway | Severity: S1 | Priority: Critical | Test Type: Security Contract
        Traceability: BR-F9-06; EX-06; 4.2 WebhookReceipt
        Expected Result:
            - Valid HMAC header returns HTTP 200 OK.
            - Tampered signature header is rejected with HTTP 400 or 401.
        """
        api_base = fs09_data["api_base_url"]
        webhook_url = f"{api_base}/api/v1/payment-webhooks/gateway"

        payload_obj = {
            "eventId": f"evt_test_{uuid.uuid4().hex[:8]}",
            "providerCode": "SIMULATION",
            "transactionId": f"txn_mock_{uuid.uuid4().hex[:8]}",
            "referenceId": f"FUND-ONL-TEST-{uuid.uuid4().hex[:8]}",
            "eventType": "payment.succeeded",
            "status": "Succeeded",
            "amountCents": 1000,
            "currency": "SGD"
        }
        raw_body = json.dumps(payload_obj, separators=(",", ":"))

        with self.step("Step 1: Send webhook with deliberately tampered HMAC signature", expected="Rejected with 400 or 401."):
            tampered_sig = webhook_signer.sign_tampered(raw_body)
            headers = {
                "X-Gateway-Signature": tampered_sig,
                "Content-Type": "application/json"
            }
            resp_bad = requests.post(webhook_url, data=raw_body, headers=headers, timeout=5)
            assert resp_bad.status_code in (400, 401), f"Tampered webhook must be rejected, got: {resp_bad.status_code}"
            self.step.set_actual(f"Tampered webhook rejected with HTTP {resp_bad.status_code}.")

        with self.step("Step 2: Send webhook with authentic HMAC signature", expected="Accepted with HTTP 200 OK."):
            valid_sig = webhook_signer.sign(raw_body)
            headers["X-Gateway-Signature"] = valid_sig
            resp_good = requests.post(webhook_url, data=raw_body, headers=headers, timeout=5)
            assert resp_good.status_code == 200, f"Valid webhook must be accepted, got: {resp_good.status_code}: {resp_good.text}"
            self.step.set_actual("Authentic HMAC signature accepted with HTTP 200 OK.")

    def test_tc_r9_auto_02_online_payment_webhook_lifecycle(
        self, fs09_data: Dict[str, Any], webhook_signer: WebhookSigner, db_helper: DatabaseHelper, cleanup_fs09_records
    ):
        """
        TC_R9_AUTO_02: Verify webhook receipt persistence and deduplication (TC-115, EX-07).
        Scenario ID: AUTO-02 | Test Suite: TS03 Full Online Payment
        Traceability: TC-115; EX-07; AC-10; BR-F9-06; 4.2 WebhookReceipt
        Expected Result:
            - The same webhook event sent twice is processed idempotently without duplicates.
            - Query DB payment_webhook_receipts confirms receipt entry.
        """
        api_base = fs09_data["api_base_url"]
        webhook_url = f"{api_base}/api/v1/payment-webhooks/gateway"
        event_id = f"evt_dedup_{uuid.uuid4().hex[:8]}"

        payload_obj = {
            "eventId": event_id,
            "providerCode": "SIMULATION",
            "transactionId": f"txn_dedup_{uuid.uuid4().hex[:8]}",
            "referenceId": f"FUND-ONL-DEDUP-{uuid.uuid4().hex[:8]}",
            "eventType": "payment.succeeded",
            "status": "Succeeded",
            "amountCents": 1500,
            "currency": "SGD"
        }
        raw_body = json.dumps(payload_obj, separators=(",", ":"))
        valid_sig = webhook_signer.sign(raw_body)
        headers = {"X-Gateway-Signature": valid_sig, "Content-Type": "application/json"}

        with self.step("Step 1: Send webhook event for the first time", expected="HTTP 200 OK."):
            resp1 = requests.post(webhook_url, data=raw_body, headers=headers, timeout=5)
            assert resp1.status_code == 200, f"First send must succeed, got {resp1.status_code}"
            self.step.set_actual("First webhook call succeeded.")

        with self.step("Step 2: Re-send identical webhook event (replay attempt)", expected="HTTP 200 OK handled idempotently."):
            resp2 = requests.post(webhook_url, data=raw_body, headers=headers, timeout=5)
            assert resp2.status_code == 200, f"Replay must succeed idempotently, got {resp2.status_code}"
            self.step.set_actual("Second webhook call handled idempotently.")

        with self.step("Step 3: Query DB payment_webhook_receipts for deduplication", expected="Exactly 1 receipt record exists."):
            receipts = db_helper.query(f"SELECT provider_event_id, processing_status FROM BillingPaymentService.dbo.payment_webhook_receipts WHERE provider_event_id = '{event_id}'")
            assert len(receipts) == 1, f"Expected exactly 1 receipt for event {event_id}, found: {len(receipts)}"
            self.step.set_actual(f"Confirmed deduplication: exactly 1 receipt in DB (status={receipts[0]['processing_status']}).")
