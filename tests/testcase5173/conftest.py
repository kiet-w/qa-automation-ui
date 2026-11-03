"""Fresh, role-specific sessions for the administration portal suites."""
import json
from pathlib import Path

import pytest
from playwright.sync_api import Browser, expect


ROOT = Path(__file__).resolve().parents[2]
LOGIN_DATA = ROOT / "data" / "fs03" / "admin_login_data.json"


def _create_auth_state(browser: Browser, directory: Path, persona_key: str) -> Path:
    """Authenticate via the real local simulator and validate the resulting role."""
    data = json.loads(LOGIN_DATA.read_text(encoding="utf-8"))
    persona = data["personas"][persona_key]
    base_url = data["base_url"].rstrip("/")
    context = browser.new_context()
    try:
        page = context.new_page()
        page.goto(f"{base_url}/login", wait_until="domcontentloaded")
        page.get_by_role("button", name="Sign in with Microsoft").click()
        page.wait_for_url("**/microsoft-provider/**", timeout=30000)
        page.get_by_text(persona["email"], exact=True).click()
        page.wait_for_url(f"{base_url}/", wait_until="domcontentloaded", timeout=30000)
        expect(page.get_by_role("banner")).to_be_visible(timeout=30000)

        response = context.request.get(f"{base_url}/api/iam/v1/auth/me")
        if not response.ok:
            pytest.fail(f"Simulator login for {persona_key} did not produce a valid session (HTTP {response.status}).")
        profile = response.json().get("data") or {}
        roles = {role.get("name") for role in profile.get("roles", []) if isinstance(role, dict)}
        if persona["role"] not in roles:
            pytest.fail(f"Simulator login for {persona_key} returned roles {sorted(roles)}, expected {persona['role']}.")
        state = directory / f"{persona_key}.json"
        context.storage_state(path=str(state))
        return state
    finally:
        context.close()


@pytest.fixture(scope="session")
def school_auth_state(browser: Browser, tmp_path_factory: pytest.TempPathFactory) -> Path:
    return _create_auth_state(browser, tmp_path_factory.mktemp("school_auth"), "school_assigned")


@pytest.fixture(scope="session")
def moehq_auth_state(browser: Browser, tmp_path_factory: pytest.TempPathFactory) -> Path:
    return _create_auth_state(browser, tmp_path_factory.mktemp("moehq_auth"), "moehq")
