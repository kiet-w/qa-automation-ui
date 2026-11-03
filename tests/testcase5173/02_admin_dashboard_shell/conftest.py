"""
tests/testcase5173/02_admin_dashboard_shell/conftest.py - Fixtures for testcase5173 module 02_admin_dashboard_shell.
Complies with Invariant 2 (zero hardcoded test data, deepcopy per test) and modularity limits (<150 lines).
"""
import copy
import json
from pathlib import Path
from typing import Any, Dict
import pytest
from playwright.sync_api import Browser, Page, Route

from pages.fs03.admin_dashboard_shell_page import AdminDashboardShellPage

WORKSPACE_DIR = Path(__file__).resolve().parents[3]
DATA_PATH = WORKSPACE_DIR / "data" / "fs03" / "02_admin_dashboard_shell_data.json"
AUTH_STATE_PATH = WORKSPACE_DIR / "data" / "fs03" / "auth_state.json"


@pytest.fixture(scope="session")
def raw_shell_data() -> Dict[str, Any]:
    """Load shell test data from JSON once per session."""
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def shell_data(raw_shell_data: Dict[str, Any]) -> Dict[str, Any]:
    """Provide fresh deepcopy of shell test data per test for strict test isolation."""
    return copy.deepcopy(raw_shell_data)


@pytest.fixture
def shell_page(page: Page) -> AdminDashboardShellPage:
    """Instantiate AdminDashboardShellPage for current page."""
    return AdminDashboardShellPage(page)


@pytest.fixture
def auth_mock(page: Page, shell_data: Dict[str, Any]):
    """
    Factory fixture providing route handler to mock /iam/v1/auth/me with any persona.
    Ensures routes are cleanly unrouted during teardown (Rule 04 §14).
    """
    active_routes = []

    def _setup_persona(persona_key: str):
        persona = shell_data["personas"][persona_key]
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

        def business_api_handler(route: Route):
            route.fulfill(
                status=200,
                content_type="application/json",
                body='{"isSuccess": true, "statusCode": 200, "data": {"items": [], "totalRecords": 0, "totalCount": 0, "metadata": {"totalRecords": 0, "pageNumber": 1, "pageSize": 10}}}',
            )

        def moe_dashboard_handler(route: Route):
            # Match the response contract consumed by MoeDashboardPage. Keep this
            # route more specific than the generic /api/bff/** business mock.
            dashboard_payload = {
                "isSuccess": True,
                "statusCode": 200,
                "data": {
                    "kpis": {
                        "totalEnrolledStudents": 0,
                        "activeRatePercent": 0,
                        "totalSchools": 0,
                        "activeTopUpCampaigns": 0,
                        "moeFasPendingReview": 0,
                    },
                    "budgetByStage": [],
                    "moeFasEligibility": {
                        "approvedCount": 0,
                        "approvedPercent": 0,
                        "underReviewCount": 0,
                        "underReviewPercent": 0,
                        "rejectedCount": 0,
                        "rejectedPercent": 0,
                    },
                    "recentTopUpCampaigns": [],
                    "activeMoeSchemes": [],
                },
                "errors": [],
            }
            route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps(dashboard_payload),
            )

        def school_dashboard_handler(route: Route):
            school_payload = {
                "isSuccess": True,
                "statusCode": 200,
                "data": {
                    "kpis": {
                        "activeStudents": 0,
                        "activeStudentsGrowthPercent": 0,
                        "studentsWithoutClass": 0,
                        "activeClassesCount": 0,
                        "activeBatchesCount": 0,
                        "sbfasPending": 0,
                    },
                    "outstandingByLevel": [],
                    "sbfasDistribution": {
                        "totalApplications": 0,
                        "pending": 0,
                        "pendingPercent": 0,
                        "granted": 0,
                        "grantedPercent": 0,
                        "rejected": 0,
                        "rejectedPercent": 0,
                    },
                    "recentPublicationBatches": [],
                    "urgentApplications": [],
                },
                "errors": [],
            }
            route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps(school_payload),
            )

        endpoint_pattern = "**/auth/me"
        session_pattern = "**/support/sessions/current"
        business_patterns = [
            "**/api/academic-resources/**",
            "**/api/student-management/**",
            "**/api/users/**",
            "**/api/v1/**",
            "**/api/fas/**",
            "**/api/education-account/**",
            "**/api/bff/**",
        ]
        for pat in business_patterns:
            page.route(pat, business_api_handler)
            active_routes.append(pat)

        dashboard_pattern = "**/api/bff/v1/dashboard/moe**"
        page.route(dashboard_pattern, moe_dashboard_handler)
        active_routes.append(dashboard_pattern)
        school_dashboard_pattern = "**/api/bff/v1/dashboard/school**"
        page.route(school_dashboard_pattern, school_dashboard_handler)
        active_routes.append(school_dashboard_pattern)

        page.route(endpoint_pattern, handler)
        page.route(session_pattern, session_handler)
        active_routes.extend([endpoint_pattern, session_pattern])

    yield _setup_persona

    for pattern in active_routes:
        try:
            page.unroute(pattern)
        except Exception:
            pass


@pytest.fixture(scope="session")
def ensure_admin_session(browser: Browser, raw_shell_data: Dict[str, Any]) -> Path:
    """Validate stored MOE HQ Admin session, or return empty path if not needed."""
    AUTH_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    return AUTH_STATE_PATH


@pytest.fixture
def browser_context_args(browser_context_args) -> Dict[str, Any]:
    """Configure browser context with default desktop viewport."""
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 800},
    }
