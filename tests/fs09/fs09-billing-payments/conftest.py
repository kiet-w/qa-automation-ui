"""
tests/fs09/fs09-billing-payments/conftest.py - Fixtures for fs09/fs09-billing-payments.
Invariant 2 compliant: All test data loaded via fixtures from data/fs09/billing_payments_data.json.
"""
import copy
import json
from pathlib import Path
from typing import Any, Dict
import pytest
from playwright.sync_api import Page
from pages.fs09.billing_payment_page import BillingPaymentPage

DATA_PATH = Path(__file__).resolve().parents[3] / "data" / "fs09/billing_payments_data.json"


@pytest.fixture(scope="session")
def raw_billing_payment_data() -> Dict[str, Any]:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def billing_payment_data(raw_billing_payment_data: Dict[str, Any]) -> Dict[str, Any]:
    return copy.deepcopy(raw_billing_payment_data)


@pytest.fixture
def billing_payment_page(page: Page) -> BillingPaymentPage:
    return BillingPaymentPage(page)
