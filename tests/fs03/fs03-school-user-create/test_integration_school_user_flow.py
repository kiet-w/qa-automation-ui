"""
tests/fs03/fs03-school-user-create/test_integration_school_user_flow.py - End-to-End Functional Flow & Navigation Test Suite.

Traceability:
- Specification: FS-03_School_Student_Fee_Management.md §3.2 F02
- User Journey: moehq login -> sidebar 'School Users' -> '+ Create School User' -> 5-field create (Image 1) -> 'Back to list' -> review table (Image 2)
- Constitution: AGENTS.md Invariants 1, 2, 3, 4, 5
"""
import pytest
from playwright.sync_api import expect, Page
from pages.fs03.school_user_create_page import SchoolUserCreatePage
from pages.fs03.school_user_management_page import SchoolUserManagementPage


@pytest.mark.flow
class TestSchoolUserCreationFlowAndReview:
    """
    Covers the end-to-end user journey:
    1. moehq account verification in sidebar
    2. Navigation via sidebar to School Users (/school-user-management)
    3. Click '+ Create School User' to open creation form (/school-user-management/new)
    4. Fill all 5 fields, submit and verify Image 1 (Toast & Result Card)
    5. Click 'Back to list' and verify Image 2 (Table review & Search)
    """

    def test_tc_fs03_flow_001_moehq_login_and_navigate_via_sidebar_to_school_users(
        self, page: Page, fs03_data: dict
    ):
        """
        TC-FS03-FLOW-001: Verify MOE HQ admin logged in, sidebar shows moehq, and navigation to School Users works.
        Traceability: User Rule: "phải vào từ cái moehq account xong vào schooluser để thực hiện create"
        """
        mgmt_page = SchoolUserManagementPage(page)
        # Navigate to portal root / dashboard
        page.goto(f"{fs03_data['base_url']}/")
        page.wait_for_load_state("domcontentloaded")

        # 1. Verify moehq System Admin profile is rendered in bottom-left of sidebar
        expect(mgmt_page.admin_profile_role).to_be_visible()
        expect(mgmt_page.admin_profile_username).to_be_visible()
        assert mgmt_page.is_moehq_logged_in(), "Expected 'moehq' 'System Admin' profile to be active in sidebar"

        # 2. Navigate to School Users via sidebar
        mgmt_page.navigate_via_sidebar()

        # 3. Verify landing on School user management (Image 2)
        expect(page).to_have_url(f"{fs03_data['base_url']}/school-user-management")
        expected_heading = fs03_data["acceptance_criteria"]["school_user_management_screen"]["heading"]
        assert mgmt_page.get_heading_text() == expected_heading, (
            f"Expected heading '{expected_heading}', got: '{mgmt_page.get_heading_text()}'"
        )
        assert mgmt_page.is_create_button_visible(), "Expected '+ Create School User' button to be visible"

    def test_tc_fs03_flow_002_click_create_school_user_navigates_to_new_form(
        self, school_user_management_page: SchoolUserManagementPage, fs03_data: dict
    ):
        """
        TC-FS03-FLOW-002: Verify clicking '+ Create School User' button opens the creation form screen.
        Traceability: User Rule: "xong vào schooluser để thực hiện create"
        """
        school_user_management_page.click_create_school_user()

        # Verify page URL and form components (Image 1)
        expect(school_user_management_page.page).to_have_url(
            f"{fs03_data['base_url']}/school-user-management/new"
        )
        create_page = SchoolUserCreatePage(school_user_management_page.page)
        expect(create_page.page_heading.first).to_be_visible()
        expect(create_page.nric_input).to_be_visible()
        expect(create_page.create_button).to_be_visible()
        assert create_page.is_single_tab_active(), "Expected Single tab to be active by default"

    def test_tc_fs03_flow_003_create_school_user_with_5_fields_and_assigned_school(
        self, school_user_page: SchoolUserCreatePage, fs03_data: dict, unique_generator
    ):
        """
        TC-FS03-FLOW-003: Verify successful creation with all 5 fields renders success toast and result card (Image 1).
        Traceability: User Rule: "tạo thành công sẽ như vậy trên hình ảnh 1"
        """
        nric, _ = unique_generator("flow03")
        payload = fs03_data["sample_payloads"]["image1_matching"]
        school = fs03_data["schools"]["valid_active"]
        email = f"{payload['email_prefix']}_{nric.lower()}{payload['email_domain']}"

        # 1. Fill all 5 fields as demonstrated in Image 1
        school_user_page.fill_form(
            nric=nric,
            first_name=payload["first_name"],
            last_name=payload["last_name"],
            email=email,
            school_code=school["code"],
        )
        assert not school_user_page.is_create_button_disabled(), (
            "Create button must be enabled with all 5 fields populated"
        )

        # 2. Click Create
        school_user_page.click_create()

        # 3. Verify Success Toast Notification (Image 1 top-right)
        school_user_page.wait_for_toast()
        toast_texts = school_user_page.get_toast_texts()
        expected_toast_title = fs03_data["acceptance_criteria"]["toast"]["success_title"]
        expected_toast_desc = fs03_data["acceptance_criteria"]["toast"]["success_description"]

        assert any(expected_toast_title.lower() in t.lower() for t in toast_texts), (
            f"Expected toast title '{expected_toast_title}' in: {toast_texts}"
        )
        assert any(expected_toast_desc.lower() in t.lower() for t in toast_texts), (
            f"Expected toast description '{expected_toast_desc}' in: {toast_texts}"
        )

        # 4. Verify Result Card (Image 1 bottom)
        school_user_page.wait_for_result_card()
        card_text = school_user_page.get_result_card_text()
        expected_card_title = fs03_data["acceptance_criteria"]["result_card"]["title"]
        expected_card_sub = fs03_data["acceptance_criteria"]["result_card"]["subtitle"]
        full_name = f"{payload['first_name']} {payload['last_name']}"

        assert expected_card_title in card_text, f"Expected '{expected_card_title}' in result card"
        assert expected_card_sub in card_text, f"Expected '{expected_card_sub}' in result card"
        assert nric in card_text, f"Expected created Username '{nric}' in result card"
        assert full_name in card_text, f"Expected created Name '{full_name}' in result card"
        assert school["name"] in card_text, f"Expected assigned School '{school['name']}' in result card"

    def test_tc_fs03_flow_004_back_to_list_and_review_created_user_in_table(
        self, school_user_page: SchoolUserCreatePage, fs03_data: dict, unique_generator
    ):
        """
        TC-FS03-FLOW-004: Verify 'Back to list' button returns to School User Management table and allows review (Image 2).
        Traceability: User Rule: "trowr về sẽ có cái hình ảnh hai để review xem lại"
        """
        nric, _ = unique_generator("flow04")
        payload = fs03_data["sample_payloads"]["image1_matching"]
        school = fs03_data["schools"]["valid_active"]
        email = f"{payload['email_prefix']}_{nric.lower()}{payload['email_domain']}"
        full_name = f"{payload['first_name']} {payload['last_name']}"

        # 1. Create a user with 5 fields
        school_user_page.fill_form(
            nric=nric,
            first_name=payload["first_name"],
            last_name=payload["last_name"],
            email=email,
            school_code=school["code"],
        )
        school_user_page.click_create()
        school_user_page.wait_for_result_card()

        # 2. Click 'Back to list' button to return to table (Image 2)
        school_user_page.click_back_to_list()

        # 3. Verify landing on School user management screen
        mgmt_page = SchoolUserManagementPage(school_user_page.page)
        mgmt_page.wait_for_page_loaded()
        expect(school_user_page.page).to_have_url(f"{fs03_data['base_url']}/school-user-management")

        # 4. Search for the newly created user by NRIC/Username
        mgmt_page.search_user(nric)

        # 5. Review the user row in the table (Image 2)
        assert mgmt_page.is_user_present_in_table(nric), (
            f"Expected newly created user with NRIC '{nric}' to be present in table rows"
        )
        user_row = mgmt_page.get_row_by_username(nric)
        assert user_row is not None, f"Row for user '{nric}' not found"

        row_text = user_row.inner_text()
        assert nric in row_text, f"Row text must contain username '{nric}': {row_text}"
        assert full_name in row_text, f"Row text must contain full name '{full_name}': {row_text}"
        assert school["name"] in row_text, f"Row text must contain assigned school '{school['name']}': {row_text}"

        # Verify action buttons exist in the row (Detail, Edit, Delete per Image 2)
        action_buttons = user_row.locator("button")
        assert action_buttons.count() >= 3, f"Expected at least 3 action buttons in row, got {action_buttons.count()}"

    def test_tc_fs03_flow_005_create_unassigned_school_user_and_review_in_table(
        self, school_user_page: SchoolUserCreatePage, fs03_data: dict, unique_generator
    ):
        """
        TC-FS03-FLOW-005: Verify creating school user without School Code shows 'Unassigned in any school' in table (Image 2).
        Traceability: FS-03 §3.2 F02; BR-R3-04
        """
        nric, _ = unique_generator("flow05")
        payload = fs03_data["sample_payloads"]["image1_matching"]
        email = f"unassigned_{nric.lower()}{payload['email_domain']}"
        full_name = f"{payload['first_name']} {payload['last_name']}"
        unassigned_label = fs03_data["acceptance_criteria"]["school_user_management_screen"]["unassigned_school_text"]

        # 1. Fill 4 fields, leave School Code empty
        school_user_page.fill_form(
            nric=nric,
            first_name=payload["first_name"],
            last_name=payload["last_name"],
            email=email,
            school_code="",
        )
        school_user_page.click_create()
        school_user_page.wait_for_result_card()

        # 2. Return to list
        school_user_page.click_back_to_list()
        mgmt_page = SchoolUserManagementPage(school_user_page.page)
        mgmt_page.wait_for_page_loaded()

        # 3. Search and review in table
        mgmt_page.search_user(nric)
        assert mgmt_page.is_user_present_in_table(nric), f"User '{nric}' must be found in table"

        user_row = mgmt_page.get_row_by_username(nric)
        assert user_row is not None
        row_text = user_row.inner_text()
        assert unassigned_label in row_text, (
            f"Expected '{unassigned_label}' in row text: {row_text}"
        )
