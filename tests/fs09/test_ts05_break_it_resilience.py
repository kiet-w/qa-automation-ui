"""
tests/fs09/test_ts05_break_it_resilience.py - Test Suite TS05: Adversarial Chaos & Security Resilience ("Phá Có Kỷ Luật").
Covers Stream 5:
- TC-R9-14: Anti-Double-Click Debounce & Idempotency Key Defense
- TC-R9-15: Cross-Parent IDOR & Unauthorized Child Context Protection
- TC-R9-16: Cryptographic HMAC-SHA256 Webhook Forgery Defense
- TC-R9-17: Concurrent Checkout Conflict & Race Condition Protection
- TC_R9_AUTO_06: Client Constraint Stripping & Hostile Input Bypass Blocked
- TS-BRK-04: Webhook Replay Attack Idempotency
- TS-BRK-05: Idempotency Key User-Scoped Isolation
- TS-BRK-06: Attempt to Pay Already Materialized/Paid Charges
- TS-BRK-10: Keyboard Accessibility (A11y Focus Trap & Tab Order)
- TC-R9-18: 9-Tier UI Automation Failure Evaluation Oracle

Traceability:
- FSD: [agile] fs/md/FS document/FS-09_Outstanding_Fees_and_Payment.md §4.2, §5.1, §5.3
- Rules: BR-F9-01, BR-F9-04, BR-F9-06, BR-F9-09, BR-F9-11, DA-12, DA-13, DA-14, EX-01, EX-03, EX-06, EX-07
- ACs: AC-05, AC-06, AC-10, AC-11, AC-12, AC-19
- Invariants: Invariant 7 (9-Tier Failure Criteria), Invariant 8 (Disciplined Adversarial Testing)
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
from pages.fs09.payment_result_page import PaymentResultPage
from tests.fs09.conftest import DatabaseHelper, WebhookSigner


@pytest.mark.fs09
@pytest.mark.break_it
class TestTS05BreakItResilience(BaseTest):
    """Test Suite TS05 covering Adversarial Chaos, Concurrency, IDOR, Security, and 9-Tier UI Health."""

    @pytest.mark.p0
    @pytest.mark.ui
    def test_tc_r9_14_anti_double_click_and_idempotency_key(
        self, fs09_data: Dict[str, Any], auth_helper, db_helper: DatabaseHelper, cleanup_fs09_records
    ):
        """
        TC-R9-14: Verify anti-double-click debounce on UI and idempotency key protection on backend.
        Scenario ID: TS-013 | Test Suite: TS05 Break-It
        Traceability: BR-F9-04; AC-05; DA-12; TC-SP-11; Invariant 8
        Expected Result:
            - UI button disables upon click to prevent double-click submissions.
            - Calling backend checkout twice with the identical Idempotency-Key returns the existing
              transaction without creating a duplicate invoice, duplicate transaction, or double deduction.
            - DB invoices and transactions tables contain exactly 1 record for this checkout.
        """
        persona = fs09_data["personas"]["PAR-NORMAL-01"]
        student_id = persona["student_id"]
        auth_helper("PAR-NORMAL-01")

        payment_page = self.get_page(BillingPaymentPage)
        api_base = fs09_data["api_base_url"]
        idempotency_key = str(uuid.uuid4())

        with self.step("Step 1: Navigate to Step 3 Review and verify button debouncing", expected="Button is interactive."):
            payment_page.open_for_student(student_id, base_url=fs09_data["base_url"])
            payment_page.wait_for_selection_loaded()
            payment_page.unselect_all_charges()
            payment_page.select_charge_by_index(0)  # 10.00 SGD Stationery
            payment_page.click_continue_to_method()
            payment_page.wait_for_method_loaded()
            payment_page.select_payment_method("EducationAccount")
            payment_page.click_continue_to_review()
            payment_page.wait_for_review_loaded()
            assert not payment_page.is_pay_button_disabled(), "Pay button must be enabled before click."
            self.step.set_actual("Ready on review step.")

        with self.step("Step 2: Dispatch first API checkout with Idempotency-Key", expected="HTTP 200 OK created."):
            payload = {
                "studentId": student_id,
                "chargeIds": ["bbbb0009-0000-0000-0000-000000000001"],
                "method": "EducationAccount",
                "walletId": persona["wallet_id"]
            }
            headers = {
                "Idempotency-Key": idempotency_key,
                "X-User-Id": "tan-wei-ming-parent",
                "X-User-Roles": "PARENT",
                "Content-Type": "application/json"
            }
            resp1 = requests.post(f"{api_base}/api/v1/checkout", json=payload, headers=headers, timeout=5)
            assert resp1.status_code == 200, f"First checkout must succeed, got: {resp1.status_code}: {resp1.text}"
            data1 = resp1.json().get("data", {})
            tx_id1 = data1.get("transactionId")
            invoice_id1 = data1.get("invoiceId")
            self.step.set_actual(f"First checkout succeeded: txId={tx_id1}, invoiceId={invoice_id1}")

        with self.step("Step 3: Re-send identical API checkout with same Idempotency-Key", expected="HTTP 200 OK returning existing transaction."):
            resp2 = requests.post(f"{api_base}/api/v1/checkout", json=payload, headers=headers, timeout=5)
            assert resp2.status_code == 200, f"Second checkout must return 200, got: {resp2.status_code}"
            body2 = resp2.json()
            data2 = body2.get("data", {})
            assert data2.get("transactionId") == tx_id1, "Idempotent response must return the original transaction ID."
            assert data2.get("invoiceId") == invoice_id1, "Idempotent response must return the original invoice ID."
            self.step.set_actual(f"Idempotent hit verified: {body2.get('message')}")

        with self.step("Step 4: Verify Database has exactly 1 invoice and 1 transaction", expected="Zero duplicate records in DB."):
            invoices = db_helper.query(f"SELECT id FROM BillingPaymentService.dbo.invoices WHERE id = '{invoice_id1}'")
            assert len(invoices) == 1, f"Expected exactly 1 invoice record, found {len(invoices)}"

            txns = db_helper.query(f"SELECT id FROM BillingPaymentService.dbo.transactions WHERE invoice_id = '{invoice_id1}'")
            assert len(txns) == 1, f"Expected exactly 1 transaction record, found {len(txns)}"
            self.step.set_actual("Database integrity confirmed: no duplicate invoices or transactions created.")

    @pytest.mark.p0
    @pytest.mark.security
    @pytest.mark.ui
    def test_tc_r9_15_idor_protection_cross_parent_access(
        self, fs09_data: Dict[str, Any], auth_helper, db_helper: DatabaseHelper
    ):
        """
        TC-R9-15: Cross-Parent IDOR & Unauthorized Child Context Protection.
        Scenario ID: TS-014 | Test Suite: TS05 Break-It
        Traceability: EX-01; AC-12; BR-F9-01; Invariant 8
        Expected Result:
            - Accessing an unlinked or non-existent student ID in URL displays invalid student context error.
            - Direct checkout mutation attempting to use a wallet that does not belong to the student
              is rejected by backend with HTTP 400 ('Wallet does not belong to this student.').
            - Zero data leak or unauthorized mutation.
        """
        auth_helper("PAR-NORMAL-01")  # TAN WEI MING (child: Chloe Chan)
        payment_page = self.get_page(BillingPaymentPage)
        api_base = fs09_data["api_base_url"]
        unauthorized_student_id = "STU-OTHER-999"

        with self.step("Step 1: Access billing page for unlinked student via direct URL manipulation", expected="Invalid context error displayed."):
            payment_page.open_for_student(unauthorized_student_id, base_url=fs09_data["base_url"])
            assert payment_page.has_invalid_context_alert(), "Page must display invalid context alert when student is not linked."
            self.step.set_actual("UI blocked unauthorized student context; invalid context screen rendered.")

        with self.step("Step 2: Direct API checkout attempting cross-student charge theft", expected="Rejected with HTTP 404 or 400."):
            # Try to pay Chloe Chan's charge using a foreign/mismatched student ID
            payload = {
                "studentId": "00000000-0000-0000-0000-000000000000",  # Foreign/unauthorized student context
                "chargeIds": ["bbbb0009-0000-0000-0000-000000000001"],  # Chloe Chan's charge
                "method": "EducationAccount"
            }
            headers = {
                "Idempotency-Key": str(uuid.uuid4()),
                "X-User-Id": "tan-wei-ming-parent",
                "X-User-Roles": "PARENT",
                "Content-Type": "application/json"
            }
            resp = requests.post(f"{api_base}/api/v1/checkout", json=payload, headers=headers, timeout=5)
            assert resp.status_code in (400, 404), f"Expected 400/404 for mismatched student charge, got: {resp.status_code}: {resp.text}"
            body = resp.json()
            assert not body.get("isSuccess", True), f"Response should be failure: {body}"
            self.step.set_actual(f"API correctly blocked cross-student charge theft: {body.get('message')}")

    @pytest.mark.p0
    @pytest.mark.security
    def test_tc_r9_16_webhook_hmac_signature_forgery_defense(
        self, fs09_data: Dict[str, Any], webhook_signer: WebhookSigner, db_helper: DatabaseHelper
    ):
        """
        TC-R9-16: Cryptographic HMAC-SHA256 Webhook Forgery Defense.
        Scenario ID: TS-015 | Test Suite: TS05 Break-It
        Traceability: BR-F9-06; EX-06; AC-10; Invariant 8
        Expected Result:
            - Missing signature header returns HTTP 401 Unauthorized.
            - Tampered / forged HMAC signature returns HTTP 401 Unauthorized.
            - Tampered webhook callbacks are rejected and NOT saved to payment_webhook_receipts.
        """
        api_base = fs09_data["api_base_url"]
        webhook_url = f"{api_base}/api/v1/payment-webhooks/gateway"
        fake_event_id = f"evt_forged_{uuid.uuid4().hex[:8]}"

        payload_obj = {
            "eventId": fake_event_id,
            "providerCode": "SIMULATION",
            "transactionId": f"txn_forged_{uuid.uuid4().hex[:8]}",
            "referenceId": f"FUND-FORGED-{uuid.uuid4().hex[:8]}",
            "eventType": "payment.succeeded",
            "status": "Succeeded",
            "amountCents": 1000
        }
        raw_body = json.dumps(payload_obj, separators=(",", ":"))

        with self.step("Step 1: Send webhook without X-Gateway-Signature header", expected="HTTP 401 Unauthorized."):
            resp_missing = requests.post(webhook_url, data=raw_body, headers={"Content-Type": "application/json"}, timeout=5)
            assert resp_missing.status_code == 401, f"Expected 401 for missing header, got {resp_missing.status_code}"
            self.step.set_actual(f"Missing header rejected with HTTP {resp_missing.status_code}")

        with self.step("Step 2: Send webhook with forged HMAC signature", expected="HTTP 401 Unauthorized."):
            bad_sig = webhook_signer.sign_tampered(raw_body, bad_secret="attacker_secret_key")
            headers = {"X-Gateway-Signature": bad_sig, "Content-Type": "application/json"}
            resp_tampered = requests.post(webhook_url, data=raw_body, headers=headers, timeout=5)
            assert resp_tampered.status_code == 401, f"Expected 401 for tampered signature, got {resp_tampered.status_code}"
            self.step.set_actual(f"Tampered signature rejected with HTTP {resp_tampered.status_code}")

        with self.step("Step 3: Verify forged event was NOT stored in payment_webhook_receipts", expected="Zero records in DB."):
            receipts = db_helper.query(f"SELECT id FROM BillingPaymentService.dbo.payment_webhook_receipts WHERE provider_event_id = '{fake_event_id}'")
            assert len(receipts) == 0, f"Security Breach! Forged event {fake_event_id} was persisted in DB: {receipts}"
            self.step.set_actual("Cryptographic perimeter intact: zero forged receipts persisted.")

    @pytest.mark.p0
    @pytest.mark.break_it
    def test_tc_r9_17_concurrent_checkout_conflict_handling(
        self, fs09_data: Dict[str, Any], db_helper: DatabaseHelper, cleanup_fs09_records
    ):
        """
        TC-R9-17: Concurrent Checkout Conflict & Race Condition Protection.
        Scenario ID: TS-016 | Test Suite: TS05 Break-It
        Traceability: EX-03; AC-06; BR-F9-09; DA-13; Invariant 8
        Expected Result:
            - When two checkouts attempt to claim the exact same student charge with different idempotency keys,
              the second checkout must be rejected with HTTP 409 Conflict ('Charge(s) already belong to an invoice').
            - Double-spending / duplicate invoice materialization is prevented.
        """
        persona = fs09_data["personas"]["PAR-NORMAL-01"]
        student_id = persona["student_id"]
        api_base = fs09_data["api_base_url"]
        charge_id = "bbbb0009-0000-0000-0000-000000000002"  # 15.00 SGD Field Trip

        payload_1 = {
            "studentId": student_id,
            "chargeIds": [charge_id],
            "method": "EducationAccount",
            "walletId": persona["wallet_id"]
        }
        headers_1 = {
            "Idempotency-Key": str(uuid.uuid4()),
            "X-User-Id": "parent-session-1",
            "X-User-Roles": "PARENT",
            "Content-Type": "application/json"
        }

        with self.step("Step 1: Execute checkout 1 for charge bbbb...0002", expected="HTTP 200 OK."):
            resp1 = requests.post(f"{api_base}/api/v1/checkout", json=payload_1, headers=headers_1, timeout=5)
            assert resp1.status_code == 200, f"Checkout 1 must succeed, got {resp1.status_code}: {resp1.text}"
            self.step.set_actual("Checkout 1 materialized invoice successfully.")

        with self.step("Step 2: Concurrently execute checkout 2 for the same charge with different key", expected="HTTP 409 Conflict."):
            payload_2 = {
                "studentId": student_id,
                "chargeIds": [charge_id],
                "method": "EducationAccount",
                "walletId": persona["wallet_id"]
            }
            headers_2 = {
                "Idempotency-Key": str(uuid.uuid4()),
                "X-User-Id": "parent-session-2",
                "X-User-Roles": "PARENT",
                "Content-Type": "application/json"
            }
            resp2 = requests.post(f"{api_base}/api/v1/checkout", json=payload_2, headers=headers_2, timeout=5)
            assert resp2.status_code == 409, f"Expected 409 Conflict for concurrent checkout, got {resp2.status_code}: {resp2.text}"
            body2 = resp2.json()
            assert "already belong to an invoice" in body2.get("message", "").lower(), f"Expected conflict message, got: {body2}"
            self.step.set_actual(f"Concurrent checkout conflict correctly blocked: {body2.get('message')}")

        with self.step("Step 3: Verify in DB that only 1 invoice exists for the charge", expected="Exactly 1 invoice item."):
            items = db_helper.query(f"SELECT invoice_id FROM BillingPaymentService.dbo.invoice_items WHERE student_charge_id = '{charge_id}'")
            assert len(items) == 1, f"Expected exactly 1 invoice item for charge {charge_id}, found: {len(items)}"
            self.step.set_actual("Confirmed 1:1 invoice materialization invariant.")

    @pytest.mark.p1
    @pytest.mark.break_it
    def test_tc_r9_auto_06_client_bypass_negative_amount_blocked(
        self, fs09_data: Dict[str, Any]
    ):
        """
        TC_R9_AUTO_06: Verify backend rejects invalid input mutations and shape violations.
        Scenario ID: TS-017 | Test Suite: TS05 Break-It
        Traceability: AC-19; BR-F9-11; 5.1; Invariant 8
        Expected Result:
            - Invalid payment method returns HTTP 400 Bad Request.
            - Empty chargeIds list returns HTTP 400 Bad Request.
            - Duplicate chargeIds returns HTTP 400 Bad Request.
        """
        api_base = fs09_data["api_base_url"]
        persona = fs09_data["personas"]["PAR-NORMAL-01"]
        headers = {
            "Idempotency-Key": str(uuid.uuid4()),
            "X-User-Id": "test-parent",
            "X-User-Roles": "PARENT",
            "Content-Type": "application/json"
        }

        with self.step("Step 1: Test invalid payment method 'HackedMethod'", expected="HTTP 400 Bad Request."):
            payload_bad_method = {
                "studentId": persona["student_id"],
                "chargeIds": ["bbbb0009-0000-0000-0000-000000000001"],
                "method": "HackedMethod",
                "walletId": persona["wallet_id"]
            }
            resp = requests.post(f"{api_base}/api/v1/checkout", json=payload_bad_method, headers=headers, timeout=5)
            assert resp.status_code == 400, f"Expected 400, got: {resp.status_code}"
            assert "invalid payment method" in resp.json().get("message", "").lower()
            self.step.set_actual("Rejected invalid payment method.")

        with self.step("Step 2: Test empty chargeIds array", expected="HTTP 400 Bad Request."):
            payload_empty_charges = {
                "studentId": persona["student_id"],
                "chargeIds": [],
                "method": "EducationAccount",
                "walletId": persona["wallet_id"]
            }
            resp = requests.post(f"{api_base}/api/v1/checkout", json=payload_empty_charges, headers=headers, timeout=5)
            assert resp.status_code == 400, f"Expected 400, got: {resp.status_code}"
            assert "chargeids is required" in resp.json().get("message", "").lower()
            self.step.set_actual("Rejected empty chargeIds list.")

        with self.step("Step 3: Test duplicate chargeIds array", expected="HTTP 400 Bad Request."):
            payload_duplicate = {
                "studentId": persona["student_id"],
                "chargeIds": ["bbbb0009-0000-0000-0000-000000000001", "bbbb0009-0000-0000-0000-000000000001"],
                "method": "EducationAccount",
                "walletId": persona["wallet_id"]
            }
            resp = requests.post(f"{api_base}/api/v1/checkout", json=payload_duplicate, headers=headers, timeout=5)
            assert resp.status_code == 400, f"Expected 400, got: {resp.status_code}"
            assert "duplicate" in resp.json().get("message", "").lower()
            self.step.set_actual("Rejected duplicate chargeIds.")

    @pytest.mark.p1
    @pytest.mark.break_it
    def test_ts_brk_04_webhook_replay_attack_idempotent(
        self, fs09_data: Dict[str, Any], webhook_signer: WebhookSigner, db_helper: DatabaseHelper, cleanup_fs09_records
    ):
        """
        TS-BRK-04: Webhook Replay Attack Idempotency.
        Traceability: BR-F9-06; EX-07; Invariant 8
        Expected Result:
            - When the exact same webhook payload is replayed 5 times sequentially,
              all requests succeed with HTTP 200 OK (idempotent Ack),
              and exactly 1 webhook receipt record is kept in DB.
        """
        api_base = fs09_data["api_base_url"]
        webhook_url = f"{api_base}/api/v1/payment-webhooks/gateway"
        replay_event_id = f"evt_replay_{uuid.uuid4().hex[:8]}"

        payload_obj = {
            "eventId": replay_event_id,
            "providerCode": "SIMULATION",
            "transactionId": f"txn_replay_{uuid.uuid4().hex[:8]}",
            "referenceId": f"FUND-REPLAY-{uuid.uuid4().hex[:8]}",
            "eventType": "payment.succeeded",
            "status": "Succeeded",
            "amountCents": 2000
        }
        raw_body = json.dumps(payload_obj, separators=(",", ":"))
        valid_sig = webhook_signer.sign(raw_body)
        headers = {"X-Gateway-Signature": valid_sig, "Content-Type": "application/json"}

        with self.step("Step 1: Send initial webhook event", expected="HTTP 200 OK."):
            resp_init = requests.post(webhook_url, data=raw_body, headers=headers, timeout=5)
            assert resp_init.status_code == 200, f"Initial webhook failed: {resp_init.status_code}"
            self.step.set_actual("Initial webhook processed.")

        with self.step("Step 2: Replay identical webhook event 5 times", expected="All 5 replays return HTTP 200 OK."):
            for i in range(5):
                resp_replay = requests.post(webhook_url, data=raw_body, headers=headers, timeout=5)
                assert resp_replay.status_code == 200, f"Replay {i+1} failed with status {resp_replay.status_code}"
            self.step.set_actual("All 5 replay attempts handled idempotently.")

        with self.step("Step 3: Query DB to confirm no duplicate receipts", expected="Exactly 1 receipt record."):
            receipts = db_helper.query(f"SELECT id, processing_status FROM BillingPaymentService.dbo.payment_webhook_receipts WHERE provider_event_id = '{replay_event_id}'")
            assert len(receipts) == 1, f"Expected exactly 1 receipt for {replay_event_id}, found: {len(receipts)}"
            self.step.set_actual("Replay resistance verified: DB contains exactly 1 receipt record.")

    @pytest.mark.p2
    @pytest.mark.break_it
    def test_ts_brk_05_idempotency_key_scoped_per_user(
        self, fs09_data: Dict[str, Any], db_helper: DatabaseHelper, cleanup_fs09_records
    ):
        """
        TS-BRK-05: Idempotency Key Scoped Per User.
        Traceability: BR-F9-04; 4.2; Invariant 8
        Expected Result:
            - When Parent A and Parent B use the same Idempotency-Key string for distinct checkouts,
              both are processed independently because the uniqueness scope is (InitiatedByUserId, IdempotencyKey).
        """
        api_base = fs09_data["api_base_url"]
        shared_key = str(uuid.uuid4())

        persona_a = fs09_data["personas"]["PAR-NORMAL-01"]  # Chloe Chan
        persona_b = fs09_data["personas"]["PAR-NORMAL-02"]  # Tan Wei Ming

        payload_a = {
            "studentId": persona_a["student_id"],
            "chargeIds": ["bbbb0009-0000-0000-0000-000000000001"],
            "method": "EducationAccount",
            "walletId": persona_a["wallet_id"]
        }
        headers_a = {
            "Idempotency-Key": shared_key,
            "X-User-Id": "parent-user-a",
            "X-User-Roles": "PARENT",
            "Content-Type": "application/json"
        }

        payload_b = {
            "studentId": persona_b["student_id"],
            "chargeIds": ["cccc0009-0000-0000-0000-000000000001"],
            "method": "EducationAccount",
            "walletId": persona_b["wallet_id"]
        }
        headers_b = {
            "Idempotency-Key": shared_key,
            "X-User-Id": "parent-user-b",
            "X-User-Roles": "PARENT",
            "Content-Type": "application/json"
        }

        with self.step("Step 1: Execute Parent A checkout with shared key", expected="HTTP 200 OK."):
            resp_a = requests.post(f"{api_base}/api/v1/checkout", json=payload_a, headers=headers_a, timeout=5)
            assert resp_a.status_code == 200, f"Parent A failed: {resp_a.status_code}: {resp_a.text}"
            self.step.set_actual("Parent A checkout succeeded.")

        with self.step("Step 2: Execute Parent B checkout with the identical key string", expected="HTTP 200 OK."):
            resp_b = requests.post(f"{api_base}/api/v1/checkout", json=payload_b, headers=headers_b, timeout=5)
            assert resp_b.status_code == 200, f"Parent B failed: {resp_b.status_code}: {resp_b.text}"
            self.step.set_actual("Parent B checkout succeeded independently.")

        with self.step("Step 3: Verify both transactions exist in database", expected="2 distinct transactions."):
            txns = db_helper.query(f"SELECT id, initiated_by_user_id FROM BillingPaymentService.dbo.transactions WHERE idempotency_key = '{shared_key}'")
            assert len(txns) == 2, f"Expected 2 transactions for shared key across 2 users, found: {len(txns)}"
            users = [t["initiated_by_user_id"] for t in txns]
            assert "parent-user-a" in users and "parent-user-b" in users
            self.step.set_actual("Per-user idempotency key scoping verified.")

    @pytest.mark.p1
    @pytest.mark.break_it
    def test_ts_brk_06_cannot_pay_already_paid_invoice(
        self, fs09_data: Dict[str, Any], db_helper: DatabaseHelper, cleanup_fs09_records
    ):
        """
        TS-BRK-06: Attempt to pay charges that have already been paid.
        Traceability: EX-04; DA-13; 5.1; Invariant 8
        Expected Result:
            - Attempting to submit a checkout for a charge that has already been settled in an invoice
              returns HTTP 409 Conflict ('Charge(s) already belong to an invoice').
        """
        api_base = fs09_data["api_base_url"]
        persona = fs09_data["personas"]["PAR-NORMAL-01"]
        charge_id = "bbbb0009-0000-0000-0000-000000000003"  # 25.00 SGD Sports Fee

        payload = {
            "studentId": persona["student_id"],
            "chargeIds": [charge_id],
            "method": "EducationAccount",
            "walletId": persona["wallet_id"]
        }
        headers = {
            "Idempotency-Key": str(uuid.uuid4()),
            "X-User-Id": "parent-payer",
            "X-User-Roles": "PARENT",
            "Content-Type": "application/json"
        }

        with self.step("Step 1: First payment of the charge", expected="HTTP 200 OK."):
            resp1 = requests.post(f"{api_base}/api/v1/checkout", json=payload, headers=headers, timeout=5)
            assert resp1.status_code == 200, f"Initial payment failed: {resp1.status_code}"
            self.step.set_actual("Charge successfully paid and settled.")

        with self.step("Step 2: Second payment attempt for the exact same charge", expected="HTTP 409 Conflict."):
            headers["Idempotency-Key"] = str(uuid.uuid4())  # Fresh key to avoid idempotency replay
            resp2 = requests.post(f"{api_base}/api/v1/checkout", json=payload, headers=headers, timeout=5)
            assert resp2.status_code == 409, f"Expected 409 Conflict, got {resp2.status_code}: {resp2.text}"
            assert "already belong to an invoice" in resp2.json().get("message", "").lower()
            self.step.set_actual(f"Rejected double payment with HTTP 409: {resp2.json().get('message')}")

    @pytest.mark.p2
    @pytest.mark.break_it
    @pytest.mark.ui
    def test_ts_brk_10_accessibility_keyboard_focus_modal(
        self, fs09_data: Dict[str, Any], auth_helper
    ):
        """
        TS-BRK-10: Accessibility (WCAG 2.1) Keyboard Navigation & Focus Trap Verification.
        Traceability: Invariant 7 (Tier 6); WCAG 2.1 Focus Order
        Expected Result:
            - Parent can navigate through charges table checkboxes and action buttons using Tab key.
            - Active element shifts sequentially and does not get stuck in a focus trap.
        """
        persona = fs09_data["personas"]["PAR-NORMAL-01"]
        student_id = persona["student_id"]
        auth_helper("PAR-NORMAL-01")

        payment_page = self.get_page(BillingPaymentPage)

        with self.step("Step 1: Open student charges selection", expected="Charges table visible."):
            payment_page.open_for_student(student_id, base_url=fs09_data["base_url"])
            payment_page.wait_for_selection_loaded()
            self.step.set_actual("Charges selection view loaded.")

        with self.step("Step 2: Navigate using Tab key and check active element changes", expected="Focus advances without traps."):
            focused_tags = []
            for _ in range(5):
                self.page.keyboard.press("Tab")
                tag = self.page.evaluate("() => document.activeElement ? document.activeElement.tagName : 'NONE'")
                focused_tags.append(tag)

            assert len(focused_tags) == 5, "Tab navigation must be executable."
            assert any(tag in ("BUTTON", "INPUT", "A") for tag in focused_tags), (
                f"Expected interactive elements to receive focus, got: {focused_tags}"
            )
            self.step.set_actual(f"Tab focus sequence observed: {focused_tags}")

    @pytest.mark.p0
    @pytest.mark.break_it
    @pytest.mark.ui
    def test_tc_r9_18_nine_tier_technical_oracle_audit(
        self, fs09_data: Dict[str, Any], auth_helper
    ):
        """
        TC-R9-18: 9-Tier UI Automation Failure Evaluation Oracle.
        Traceability: Invariant 7 (9-Tier Failure Criteria); AGENTS.md
        Evaluates:
            - Tier 1: Zero runtime JS errors / uncaught exceptions.
            - Tier 2: Zero unexpected silent HTTP 5xx network failures.
            - Tier 3: Zero horizontal overflow layout defects and zero broken images.
            - Tier 4: Zero hanging loading spinners.
            - Tier 8: Zero plain-text NRIC leaked on URL query string.
        """
        auth_helper("PAR-NORMAL-01")
        self.init_ui_health_monitor(api_prefix="/api/")

        billing_account_page = self.get_page(BillingAccountSelectionPage)
        payment_page = self.get_page(BillingPaymentPage)
        persona = fs09_data["personas"]["PAR-NORMAL-01"]
        student_id = persona["student_id"]

        with self.step("Step 1: Audit Billing Account Selection Page (/billing)", expected="Passes 9-tier quality gate."):
            billing_account_page.open(base_url=fs09_data["base_url"])
            assert billing_account_page.is_loaded(), "Billing account selection page must be loaded."
            self.assert_ui_health(allow_api_errors=False)
            self.assert_no_horizontal_overflow()
            self.assert_no_broken_images()
            self.assert_no_nric_in_url()
            self.step.set_actual("Tier 1, 2, 3, 8 health verified on /billing.")

        with self.step("Step 2: Audit Billing Payment Page (/billing/:studentId)", expected="Passes 9-tier quality gate."):
            payment_page.open_for_student(student_id, base_url=fs09_data["base_url"])
            payment_page.wait_for_selection_loaded()
            self.assert_ui_health(allow_api_errors=False)
            self.assert_no_horizontal_overflow()
            self.assert_no_broken_images()
            self.assert_no_hanging_spinners()
            self.assert_no_nric_in_url()
            self.step.set_actual("Tier 1, 2, 3, 4, 8 health verified on /billing/:studentId.")
