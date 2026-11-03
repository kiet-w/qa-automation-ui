"""Session context for testcase5173 school-user management automation."""
import copy
import json
import re
from urllib.parse import parse_qs, urlparse
from playwright.sync_api import Browser, Page
import pytest

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, moehq_auth_state):
    """Use the freshly validated MOEHQ simulator session for this module."""
    options = {**browser_context_args, "viewport": {"width": 1280, "height": 800}}
    options["storage_state"] = str(moehq_auth_state)
    return options


@pytest.fixture
def school_role_page(browser: Browser, school_auth_state) -> Page:
    """Open an isolated page with the validated SCHOOL-role simulator state."""
    context = browser.new_context(storage_state=str(school_auth_state), viewport={"width": 1280, "height": 800})
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture(autouse=True)
def isolated_school_user_api(page: Page):
    """Keep CRUD automation isolated from the shared simulator database."""
    schools = [
        {
            "id": "test-school",
            "moeSchoolCode": "RPS-0201",
            "code": "RPS-0201",
            "name": "Rosyth Primary School",
            "fullName": "Rosyth Primary School",
            "schoolType": "GOVERNMENT",
            "isActive": True,
        }
    ]
    users = [
        {
            "id": "test-user-unassigned",
            "code": "USR-AUTO-01",
            "userName": "staff1",
            "fullName": "Test Staff",
            "isActive": True,
            "school": None,
        },
        {
            "id": "test-user-assigned",
            "code": "USR-AUTO-02",
            "userName": "moehq",
            "fullName": "Test Admin",
            "isActive": True,
            "school": schools[0],
        },
    ]

    def handler(route):
        request = route.request
        url = urlparse(request.url)
        path = url.path
        if "/users/v1/school-users/table" in path:
            search = parse_qs(urlparse(request.url).query).get("search", [""])[0].strip().lower()
            rows = [
                row for row in users
                if not search or search in " ".join(
                    (row["code"], row["userName"], row["fullName"], (row["school"] or {}).get("name", ""))
                ).lower()
            ]
            route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps({
                    "isSuccess": True,
                    "data": {
                        "items": rows,
                        "metadata": {
                            "pageNumber": 1,
                            "pageSize": 10,
                            "totalRecords": len(rows),
                            "totalPages": 1,
                            "hasPreviousPage": False,
                            "hasNextPage": False,
                        },
                    },
                }),
            )
        elif "/users/v1/school-users/cursor" in path or "/academic-resources/v1/schools/cursor" in path:
            route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps({
                    "isSuccess": True,
                    "data": {
                        "items": schools,
                        "metadata": {
                            "pageSize": 20,
                            "nextCursor": None,
                            "hasNextPage": False,
                        },
                    },
                }),
            )
        elif "/users/v1/school-users/single" in path:
            payload = request.post_data_json or {}
            if not re.fullmatch(r"[STFG]\d{7}[A-Z]", str(payload.get("nric", ""))):
                route.fulfill(
                    status=400,
                    content_type="application/json",
                    body=json.dumps({"isSuccess": False, "message": "Validation failed"}),
                )
            elif payload.get("nric") == "S8407384A" or payload.get("email") == "staff1@IAM.edu.vn":
                route.fulfill(
                    status=409,
                    content_type="application/json",
                    body=json.dumps({
                        "isSuccess": False,
                        "message": "A user with username 'S8407384A' already exists.",
                    }),
                )
            else:
                assigned_school = schools[0] if payload.get("moeSchoolCode") == "RPS-0201" else None
                route.fulfill(
                    status=201,
                    content_type="application/json",
                    body=json.dumps({
                        "isSuccess": True,
                        "data": {
                            "username": payload.get("nric", "automation.test"),
                            "firstName": payload.get("firstName", "Automation"),
                            "lastName": payload.get("lastName", "Test"),
                            "email": payload.get("email", "automation@example.test"),
                            "password": "temporary",
                            "school": assigned_school,
                        },
                    }),
                )
        elif "/users/v1/school-users/bulk" in path:
            upload = request.post_data or ""
            if 'filename="missing_columns.csv"' in upload:
                route.fulfill(status=400, content_type="application/json", body=json.dumps({
                    "isSuccess": False, "message": "Missing CSV column: School User Email"
                }))
            elif 'filename="over_limit.csv"' in upload:
                route.fulfill(status=413, content_type="application/json", body=json.dumps({
                    "isSuccess": False, "message": "The CSV file may contain at most 1000 rows."
                }))
            else:
                accounts = [
                    {"username": f"auto.{index}", "email": f"auto.{index}@example.test",
                     "school": schools[0], "rowNumber": index + 1}
                    for index in range(1, 4 if 'filename="three_valid.csv"' in upload else 3)
                ]
                failed = ([{"rowNumber": 4, "reason": "NRIC must contain 1 letter, 7 digits, and 1 letter."}]
                          if 'filename="partial.csv"' in upload else [])
                route.fulfill(status=200, content_type="application/json", body=json.dumps({
                    "isSuccess": True,
                    "data": {"successfulAccounts": accounts, "failedAccounts": failed},
                }))
        elif "/users/v1/school-users/test-user-unassigned/assign-school" in path:
            users[0]["school"] = schools[0]
            route.fulfill(status=200, content_type="application/json", body=json.dumps({"isSuccess": True, "data": None}))
        elif "/users/v1/school-users/test-user-unassigned" in path:
            detail = {
                "id": "test-user-unassigned",
                "code": "USR-AUTO-01",
                "userName": "staff1",
                "email": "staff1@IAM.edu.vn",
                "isActive": True,
                "isEmailVerified": True,
                "lastLoginAt": None,
                "createdAt": "2026-01-01T00:00:00Z",
                "updatedAt": "2026-01-01T00:00:00Z",
                "profile": {
                    "firstName": "Test",
                    "lastName": "Staff",
                    "fullName": "Test Staff",
                    "phoneNumber": None,
                    "avatarUrl": None,
                    "gender": None,
                    "birthDate": None,
                    "address": None,
                    "bio": None,
                    "isVerified": True,
                },
                "school": users[0]["school"],
            }
            route.fulfill(status=200, content_type="application/json", body=json.dumps({"isSuccess": True, "data": detail}))
        elif "/users/v1/school-users/test-user-assigned" in path:
            detail = {
                "id": "test-user-assigned",
                "code": "USR-AUTO-02",
                "userName": "moehq",
                "email": "admin@example.test",
                "isActive": True,
                "isEmailVerified": True,
                "lastLoginAt": None,
                "createdAt": "2026-01-01T00:00:00Z",
                "updatedAt": "2026-01-01T00:00:00Z",
                "profile": {
                    "firstName": "Test",
                    "lastName": "Admin",
                    "fullName": "Test Admin",
                    "phoneNumber": None,
                    "avatarUrl": None,
                    "gender": None,
                    "birthDate": None,
                    "address": None,
                    "bio": None,
                    "isVerified": True,
                },
                "school": schools[0],
            }
            route.fulfill(status=200, content_type="application/json", body=json.dumps({"isSuccess": True, "data": detail}))
        else:
            route.continue_()

    page.route("**/users/v1/school-users/**", handler)
    page.route("**/academic-resources/v1/schools/cursor**", handler)
