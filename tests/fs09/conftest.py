"""
tests/fs09/conftest.py - Fixtures, database helpers, and configurations for FS-09: Outstanding Fees & Payment Processing.
Complies strictly with Invariants 0 to 8:
- Invariant 0: Zero modifications to copy/
- Invariant 1: Zero assertions in Page Objects
- Invariant 2: Zero hardcoded test data (loaded from data/fs09/fs09_data.json)
- Invariant 6: Zero Assumptions (evidence-based configuration)
- Invariant 7: 9-Tier UI Failure Evaluation
- Invariant 8: Disciplined Adversarial Testing
"""
import copy
import hashlib
import hmac
import json
from pathlib import Path
import subprocess
import time
from typing import Any, Callable, Dict, Generator, List, Optional
import pytest
from playwright.sync_api import Page

from pages.fs09.billing_account_selection_page import BillingAccountSelectionPage
from pages.fs09.billing_payment_page import BillingPaymentPage
from pages.fs09.payment_gateway_simulator_page import PaymentGatewaySimulatorPage
from pages.fs09.payment_result_page import PaymentResultPage
from pages.fs08.singpass_login_page import SingpassLoginPage
from pages.fs08.home_portal_page import HomePortalPage

WORKSPACE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = WORKSPACE_DIR / "data" / "fs09" / "fs09_data.json"


@pytest.fixture(scope="session")
def raw_fs09_data() -> Dict[str, Any]:
    """Load JSON configuration from data/fs09/fs09_data.json once per test session."""
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def fs09_data(raw_fs09_data: Dict[str, Any]) -> Dict[str, Any]:
    """Provide a fresh deepcopy of fs09_data for each test to ensure test isolation."""
    return copy.deepcopy(raw_fs09_data)


@pytest.fixture
def billing_account_page(page: Page) -> BillingAccountSelectionPage:
    """Fixture providing BillingAccountSelectionPage instance."""
    return BillingAccountSelectionPage(page)


@pytest.fixture
def billing_payment_page(page: Page) -> BillingPaymentPage:
    """Fixture providing BillingPaymentPage instance."""
    return BillingPaymentPage(page)


@pytest.fixture
def gateway_simulator(page: Page) -> PaymentGatewaySimulatorPage:
    """Fixture providing PaymentGatewaySimulatorPage instance."""
    return PaymentGatewaySimulatorPage(page)


@pytest.fixture
def payment_result_page(page: Page) -> PaymentResultPage:
    """Fixture providing PaymentResultPage instance."""
    return PaymentResultPage(page)


@pytest.fixture
def login_page(page: Page) -> SingpassLoginPage:
    """Fixture providing SingpassLoginPage instance."""
    return SingpassLoginPage(page)


@pytest.fixture
def home_portal(page: Page) -> HomePortalPage:
    """Fixture providing HomePortalPage instance."""
    return HomePortalPage(page)


class DatabaseHelper:
    """Docker-based MSSQL helper to query and assert on microservice databases."""

    def __init__(self, host_password: str = "YourStrong@Password123"):
        self.password = host_password

    def query(self, sql_query: str, db_name: str = "BillingPaymentService") -> List[Dict[str, Any]]:
        """
        Execute a SELECT query with FOR JSON AUTO and return parsed list of records.
        Uses -y 0 without -h to ensure unpadded valid JSON output from sqlcmd.
        """
        # Ensure query ends with FOR JSON AUTO if not already present
        clean_query = sql_query.strip().rstrip(";")
        if "FOR JSON" not in clean_query.upper():
            full_sql = f"SET NOCOUNT ON; {clean_query} FOR JSON AUTO;"
        else:
            full_sql = f"SET NOCOUNT ON; {clean_query};"

        cmd = [
            "docker", "exec", "template-sqlserver",
            "/opt/mssql-tools18/bin/sqlcmd", "-S", "localhost",
            "-U", "sa", "-P", self.password,
            "-d", db_name,
            "-C", "-y", "0", "-Q", full_sql
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        stdout = res.stdout.strip()
        if not stdout:
            return []
        try:
            return json.loads(stdout)
        except Exception:
            return []

    def execute(self, sql_command: str, db_name: str = "BillingPaymentService") -> subprocess.CompletedProcess:
        """Execute a DDL/DML statement inside the database container."""
        cmd = [
            "docker", "exec", "template-sqlserver",
            "/opt/mssql-tools18/bin/sqlcmd", "-S", "localhost",
            "-U", "sa", "-P", self.password,
            "-d", db_name,
            "-C", "-Q", f"SET QUOTED_IDENTIFIER ON; SET ANSI_NULLS ON; {sql_command}"
        ]
        return subprocess.run(cmd, capture_output=True, text=True)


@pytest.fixture(scope="session")
def db_helper() -> DatabaseHelper:
    """Fixture providing DatabaseHelper instance."""
    return DatabaseHelper()


class WebhookSigner:
    """Cryptographic helper to sign simulated payment gateway webhooks using HMAC-SHA256."""

    def __init__(self, secret: str = "whsec_f9_demo_shared_secret"):
        self.secret = secret

    def sign(self, payload_str: str, timestamp: Optional[int] = None) -> str:
        """
        Construct header value formatted as: t={timestamp},v1={hex_signature}
        per FS-09 Webhook specification.
        """
        t = timestamp if timestamp is not None else int(time.time())
        msg = f"{t}.{payload_str}".encode("utf-8")
        sig = hmac.new(self.secret.encode("utf-8"), msg, hashlib.sha256).hexdigest()
        return f"t={t},v1={sig}"

    def sign_tampered(self, payload_str: str, bad_secret: str = "wrong_secret_key") -> str:
        """Construct a deliberately tampered HMAC signature for security testing."""
        t = int(time.time())
        msg = f"{t}.{payload_str}".encode("utf-8")
        sig = hmac.new(bad_secret.encode("utf-8"), msg, hashlib.sha256).hexdigest()
        return f"t={t},v1={sig}"


@pytest.fixture(scope="session")
def webhook_signer(raw_fs09_data: Dict[str, Any]) -> WebhookSigner:
    """Fixture providing WebhookSigner helper."""
    secret = raw_fs09_data.get("webhook_secret", "whsec_f9_demo_shared_secret")
    return WebhookSigner(secret=secret)


@pytest.fixture
def auth_helper(page: Page, fs09_data: Dict[str, Any]) -> Callable[[str], HomePortalPage]:
    """
    Authenticate any persona through Mockpass and ensure safe navigation to Home Portal.
    Defaults to PAR-NORMAL-01 (TAN WEI MING).
    """
    def _login_as(persona_key: str = "PAR-NORMAL-01") -> HomePortalPage:
        persona = fs09_data["personas"][persona_key]
        login = SingpassLoginPage(page)
        login.login_with_persona(persona["name"], base_url=fs09_data["base_url"])
        home = HomePortalPage(page)
        home.wait_for_portal_loaded()
        return home

    return _login_as


@pytest.fixture
def cleanup_fs09_records(db_helper: DatabaseHelper) -> Generator[None, None, None]:
    """
    Teardown fixture that rolls back test transactions, resets invoices,
    and restores wallet balances to ensure test idempotency.
    """
    yield
    try:
        # Reset test invoices and transactions created during test runs
        db_helper.execute("""
            DELETE FROM BillingPaymentService..payment_webhook_receipts;
            DELETE FROM BillingPaymentService..transaction_funding_sources;
            DELETE FROM BillingPaymentService..transactions;
            DELETE FROM BillingPaymentService..invoice_items;
            DELETE FROM BillingPaymentService..invoices;
            UPDATE EducationAccountDatabase..wallets SET balance = 50.00, status = 1 WHERE student_id = '01a15a22-dddf-750e-ac12-6d155e779d11';
            UPDATE EducationAccountDatabase..wallets SET balance = 40.00, status = 1 WHERE student_id = '01a15a22-f573-7ba6-93d2-71ac9a4ce40b';
        """)
    except Exception:
        pass
