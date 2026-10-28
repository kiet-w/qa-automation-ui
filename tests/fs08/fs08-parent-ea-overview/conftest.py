"""
tests/fs08/fs08-parent-ea-overview/conftest.py - Fixtures for fs08/fs08-parent-ea-overview.
Invariant 2 compliant: All test data loaded via fixtures from data/fs08/transaction_history_data.json.
"""
import copy
import json
from pathlib import Path
from typing import Any, Dict
import pytest
from playwright.sync_api import Page
from pages.fs08.transactions_page import TransactionsPage

DATA_PATH = Path(__file__).resolve().parents[3] / "data" / "fs08/transaction_history_data.json"


@pytest.fixture(scope="session")
def raw_transaction_history_data() -> Dict[str, Any]:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def transaction_history_data(raw_transaction_history_data: Dict[str, Any]) -> Dict[str, Any]:
    return copy.deepcopy(raw_transaction_history_data)


@pytest.fixture
def transactions_page(page: Page) -> TransactionsPage:
    return TransactionsPage(page)
