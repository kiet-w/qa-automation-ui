"""Use the shared SCHOOL session for module 06."""
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict, school_auth_state: Path) -> dict:
    return {
        **browser_context_args,
        "storage_state": str(school_auth_state),
        "viewport": {"width": 1280, "height": 800},
    }
