"""Use the shared, role-validated MOEHQ session for module 05."""
import pytest


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, moehq_auth_state):
    return {
        **browser_context_args,
        "storage_state": str(moehq_auth_state),
        "viewport": {"width": 1280, "height": 800},
    }
