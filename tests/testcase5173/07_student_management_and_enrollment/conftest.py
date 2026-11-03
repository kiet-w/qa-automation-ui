"""Use a freshly authenticated SCHOOL session for student workflows."""
from pathlib import Path
import copy
import json
import random

import pytest
from playwright.sync_api import Page


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict, school_auth_state: Path) -> dict:
    return {**browser_context_args, "storage_state": str(school_auth_state)}


@pytest.fixture(autouse=True)
def isolate_student_test_rate_limit(page: Page) -> None:
    """Keep parallel student UI tests from sharing the QA gateway rate-limit key."""
    client_ip = f"10.{random.randint(10, 250)}.{random.randint(10, 250)}.{random.randint(1, 254)}"
    page.set_extra_http_headers({"X-Forwarded-For": client_ip})


@pytest.fixture
def student_lifecycle_data() -> dict:
    data_file = (
        Path(__file__).resolve().parents[3]
        / "data/testcase5173/07_student_management_and_enrollment/student_lifecycle.json"
    )
    return copy.deepcopy(json.loads(data_file.read_text(encoding="utf-8")))
