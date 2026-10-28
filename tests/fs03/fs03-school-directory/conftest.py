"""
tests/fs03/fs03-school-directory/conftest.py - Fixtures for School Management Test Suites.
Complies with Invariant 2 (zero hardcoded test data, deepcopy per test) and modularity limits (<150 lines).
"""
import copy
import json
from pathlib import Path
from typing import Any, Dict
import pytest
from playwright.sync_api import Browser, Page, Route

from pages.fs03.school_directory_page import SchoolDirectoryPage
from pages.fs03.school_create_page import SchoolCreatePage
from pages.fs03.school_detail_page import SchoolDetailPage

WORKSPACE_DIR = Path(__file__).resolve().parents[3]
DATA_PATH = WORKSPACE_DIR / "data" / "fs03" / "school_directory_data.json"
AUTH_STATE_PATH = WORKSPACE_DIR / "data" / "fs03" / "auth_state.json"


@pytest.fixture(scope="session")
def raw_school_directory_data() -> Dict[str, Any]:
    """Load school directory test data from JSON once per session."""
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def school_directory_data(raw_school_directory_data: Dict[str, Any]) -> Dict[str, Any]:
    """Provide fresh deepcopy of school directory test data per test."""
    return copy.deepcopy(raw_school_directory_data)


@pytest.fixture
def school_directory_page(page: Page) -> SchoolDirectoryPage:
    """Instantiate SchoolDirectoryPage for current page."""
    return SchoolDirectoryPage(page)


@pytest.fixture
def school_create_page(page: Page) -> SchoolCreatePage:
    """Instantiate SchoolCreatePage for current page."""
    return SchoolCreatePage(page)


@pytest.fixture
def school_detail_page(page: Page) -> SchoolDetailPage:
    """Instantiate SchoolDetailPage for current page."""
    return SchoolDetailPage(page)


@pytest.fixture
def auth_mock(page: Page, school_directory_data: Dict[str, Any]):
    """
    Factory fixture providing route handler to mock auth & backend APIs.
    Ensures routes are cleanly unrouted during teardown (Rule 04 §14).
    """
    active_routes = []

    def _setup_persona(persona_key: str = "moehq", mock_schools: bool = True):
        persona = school_directory_data["personas"][persona_key]
        auth_payload = {
            "isSuccess": True,
            "statusCode": 200,
            "message": "User profile retrieved successfully",
            "data": {
                "id": persona["user_id"],
                "code": persona["code"],
                "username": persona["username"],
                "firstName": persona["first_name"],
                "lastName": persona["last_name"],
                "fullName": persona["full_name"],
                "schoolId": persona.get("school_id"),
                "roles": [
                    {"code": f"ROL-{r}", "name": r, "isActive": True}
                    for r in persona["roles"]
                ],
                "permissions": [],
            },
            "errors": [],
        }

        def handler(route: Route):
            route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps(auth_payload),
            )

        def session_handler(route: Route):
            route.fulfill(status=204, body="")

        endpoint_pattern = "**/auth/me"
        session_pattern = "**/support/sessions/current"

        page.route(endpoint_pattern, handler)
        page.route(session_pattern, session_handler)
        active_routes.extend([endpoint_pattern, session_pattern])

        if mock_schools:
            samples = school_directory_data["sample_schools"]
            schools_items = [
                {
                    "id": samples["active_with_students"]["id"],
                    "moeSchoolCode": samples["active_with_students"]["code"],
                    "name": samples["active_with_students"]["name"],
                    "schoolType": samples["active_with_students"]["type"],
                    "activeClasses": samples["active_with_students"]["active_classes"],
                    "activeStudents": samples["active_with_students"]["active_students"],
                    "isActive": True,
                },
                {
                    "id": samples["eligible_deactivate"]["id"],
                    "moeSchoolCode": samples["eligible_deactivate"]["code"],
                    "name": samples["eligible_deactivate"]["name"],
                    "schoolType": samples["eligible_deactivate"]["type"],
                    "activeClasses": samples["eligible_deactivate"]["active_classes"],
                    "activeStudents": samples["eligible_deactivate"]["active_students"],
                    "isActive": True,
                },
                {
                    "id": samples["inactive_school"]["id"],
                    "moeSchoolCode": samples["inactive_school"]["code"],
                    "name": samples["inactive_school"]["name"],
                    "schoolType": samples["inactive_school"]["type"],
                    "activeClasses": samples["inactive_school"]["active_classes"],
                    "activeStudents": samples["inactive_school"]["active_students"],
                    "isActive": False,
                },
            ]

            def schools_handler(route: Route):
                req = route.request
                if req.method == "GET":
                    route.fulfill(
                        status=200,
                        content_type="application/json",
                        body=json.dumps({
                            "isSuccess": True,
                            "statusCode": 200,
                            "data": {
                                "items": schools_items,
                                "totalRecords": len(schools_items),
                                "metadata": {"totalRecords": len(schools_items), "pageNumber": 1, "pageSize": 10},
                            },
                        }),
                    )
                else:
                    route.continue_()

            school_pattern = "**/school/v1/schools*"
            page.route(school_pattern, schools_handler)
            active_routes.append(school_pattern)

    yield _setup_persona

    for pattern in active_routes:
        try:
            page.unroute(pattern)
        except Exception:
            pass


@pytest.fixture
def browser_context_args(browser_context_args) -> Dict[str, Any]:
    """Configure browser context with default desktop viewport and optional cached session."""
    args = {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 800},
    }
    if AUTH_STATE_PATH.exists():
        args["storage_state"] = str(AUTH_STATE_PATH)
    return args
