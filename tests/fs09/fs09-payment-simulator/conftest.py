"""
tests/fs09/fs09-payment-simulator/conftest.py - Fixtures for fs09/fs09-payment-simulator.
Invariant 2 compliant: All test data loaded via fixtures from data/fs09/payment_checkout_data.json.
"""
import copy
import json
from pathlib import Path
from typing import Any, Dict
import pytest
from playwright.sync_api import Page
from pages.fs09.payment_gateway_simulator_page import PaymentGatewaySimulatorPage

DATA_PATH = Path(__file__).resolve().parents[3] / "data" / "fs09/payment_checkout_data.json"


@pytest.fixture(scope="session")
def raw_payment_checkout_data() -> Dict[str, Any]:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def payment_checkout_data(raw_payment_checkout_data: Dict[str, Any]) -> Dict[str, Any]:
    return copy.deepcopy(raw_payment_checkout_data)


@pytest.fixture
def gateway_simulator_page(page: Page) -> PaymentGatewaySimulatorPage:
    return PaymentGatewaySimulatorPage(page)
