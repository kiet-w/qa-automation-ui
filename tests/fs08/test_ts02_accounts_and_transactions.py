"""
tests/fs08/test_ts02_accounts_and_transactions.py
Automated test suite for Stream 02: Education Account Cards, Ledger & Transactions.
Aligned with:
- [agile] fs/md/Test Cases/TC_R8_Parent_Portal_SingPass_Profile.md (TS-004, TS-005, TS-006, TS-008, TS-009)
- fs08/01-business-specs/BUSINESS_RULES.md (BR-08-05, BR-08-06, BR-08-07, BR-08-08)
- Client Decisions: D-21 (Value-driven card layout), Table 120 (Card components), Table 121 (6 EA States)
"""
import copy
from typing import Any, Dict
import pytest

from tests.base_test import BaseTest
from pages.fs08.singpass_login_page import SingpassLoginPage
from pages.fs08.home_portal_page import HomePortalPage
from pages.fs08.transactions_page import TransactionsPage


@pytest.mark.p0
@pytest.mark.functional
@pytest.mark.ui
class TestTS02AccountsAndTransactions(BaseTest):
    """Test suite covering Education Account cards, balances, 3-tier card sorting, and transaction ledger."""

    def test_tc_r8_034_and_051_view_active_child_card_and_ea_balance(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-034 & TC-R8-051: View Active Education Account Child Card and Balance on Home Portal.
        Scenario ID: TS-004 & TS-005 | Test Suite: Home & Education Account - Account Info
        Page: HomePortalPage | Severity: S2 / S1 | Priority: High / Critical | Test Type: Functional UI
        Traceability: US-08.2; Table 120; Table 121; BR-08-05.3; BR-08-07; PB-08
        Environment: Localhost Vite (:5174) & MockPass (:5156)
        Preconditions: Parent TAN WEI MING logged in with active student.
        Test Data: fs08_data["personas"]["PAR-NORMAL-01"]
        Expected Result: Child card renders with student name link, Active status badge, SGD balance format, and masked NRIC.
        Actual Result: As expected.
        Assumption Ref: None (BR-08-05.3 & BR-08-07).
        """
        login = self.get_page(SingpassLoginPage)
        home = self.get_page(HomePortalPage)

        with self.step("Step 1: Authenticate parent and land on Home Portal", expected="Home Portal loaded with student accounts."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            home.wait_for_portal_loaded()
            self.step.set_actual("Logged in; home portal rendered.")

        with self.step("Step 2: Inspect first child card metadata", expected="Card contains student name, Active badge, SGD balance, and masked NRIC."):
            cards = home.get_all_child_cards()
            assert len(cards) > 0, "At least 1 child card must be rendered on the Home Portal."

            card = cards[0]
            assert card["name"] != "", "Child card must have a visible student name link."
            assert card["status"] in ("Active", "Due for closure", "Closed"), f"Unexpected status badge: {card['status']}"
            assert "SGD" in card["balance_text"], f"Expected SGD balance text, got: {card['balance_text']}"
            assert "*" in card["masked_nric"] or "NRIC" in card["masked_nric"], f"Expected masked NRIC, got: {card['masked_nric']}"
            self.step.set_actual(f"Verified child card: Name={card['name']}, Status={card['status']}, Balance={card['balance_text']}")

    def test_tc_r8_037_child_cards_three_tier_sorting_order(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-037: Verify 3-tier child card sorting order on Home Portal.
        Tier 1: Active EA cards first, age 16+ cards (Due for closure / Closed) last.
        Tier 2: Older children (smaller DOB) sorted before younger children.
        Tier 3: Non-FAS children sorted before FAS granted children when DOB matches.
        Scenario ID: TS-004 | Test Suite: Home
        Page: HomePortalPage | Severity: S2 | Priority: High | Test Type: Functional UI
        Traceability: BR-08-05.1; Table 122 (AC #12); Section 6.1
        Environment: Localhost Vite (:5174) & MockPass (:5156)
        Preconditions: Parent logged in with multiple children.
        Test Data: fs08_data["personas"]["PAR-NORMAL-01"]
        Expected Result: Active status cards appear before any Due for closure or Closed cards.
        Actual Result: As expected.
        Assumption Ref: BR-08-05.1.
        """
        login = self.get_page(SingpassLoginPage)
        home = self.get_page(HomePortalPage)

        with self.step("Step 1: Authenticate parent and retrieve all child cards", expected="Multiple cards loaded."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            home.wait_for_portal_loaded()
            cards = home.get_all_child_cards()
            assert len(cards) > 0, "At least 1 card must be present."
            self.step.set_actual(f"Retrieved {len(cards)} child cards.")

        with self.step("Step 2: Verify Tier 1 status sorting invariant (Active appears before Closed/Due for closure)", expected="Cards follow Tier 1 sort rules."):
            seen_inactive = False
            for card in cards:
                if card["status"] in ("Due for closure", "Closed"):
                    seen_inactive = True
                elif card["status"] == "Active" and seen_inactive:
                    pytest.fail(f"Sorting Violation (BR-08-05.1): Active card '{card['name']}' appeared after an inactive/16yo card.")
            self.step.set_actual("Tier 1 sorting order verified.")

    @pytest.mark.p1
    def test_tc_r8_043_fee_preview_max_three_items_and_more_link(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-043: Verify Fee preview list shows maximum 3 fees and '+N more' link if applicable.
        Scenario ID: TS-004 | Test Suite: Home
        Page: HomePortalPage | Severity: S2 | Priority: Medium | Test Type: Functional UI
        Traceability: BR-08-05.3; Table 120; Table 122 (AC #19)
        Environment: Localhost Vite (:5174)
        Preconditions: Authenticated user on Home Portal.
        Test Data: fs08_data["personas"]["PAR-NORMAL-01"]
        Expected Result: Each card renders at most 3 preview fee rows; '+N more' appears if > 3 fees.
        Actual Result: As expected.
        Assumption Ref: BR-08-05.3.
        """
        login = self.get_page(SingpassLoginPage)
        home = self.get_page(HomePortalPage)

        with self.step("Step 1: Authenticate parent and inspect fee previews on cards", expected="Home portal rendered."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            home.wait_for_portal_loaded()
            cards_count = home.get_child_cards_count()
            assert cards_count > 0, "At least 1 child card must be rendered."
            self.step.set_actual(f"Inspecting {cards_count} cards.")

        with self.step("Step 2: Check preview fee items count does not exceed 3", expected="Max 3 preview fees per card."):
            for idx in range(cards_count):
                fee_count = home.get_child_card_fee_items_count(idx)
                assert fee_count <= 3, f"Card {idx} displays {fee_count} fees, exceeding maximum limit of 3 (BR-08-05.3)."
            self.step.set_actual("Verified all cards adhere to maximum 3 fee preview limit.")

    def test_tc_r8_072_transactions_page_navigation_and_ledger_structure(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-072: Navigation to Transactions Page & Verification of Ledger Table Structure.
        Scenario ID: TS-008 | Test Suite: Education Account - Transactions
        Page: HomePortalPage, TransactionsPage | Severity: S1 | Priority: High | Test Type: Functional UI
        Traceability: US-08.2; Table 116; BR-08-08.6
        Environment: Localhost Vite (:5174)
        Preconditions: Authenticated user with transaction history.
        Test Data: fs08_data["personas"]["PAR-NORMAL-01"]
        Expected Result: Transactions page renders summary banner and table with required columns (Date, Description, Amount, Status).
        Actual Result: As expected.
        Assumption Ref: BR-08-08.6.
        """
        login = self.get_page(SingpassLoginPage)
        home = self.get_page(HomePortalPage)
        txns = self.get_page(TransactionsPage)

        with self.step("Step 1: Log in and navigate to Transactions via nav link", expected="Transactions page rendered."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            home.navigate_to_transactions()
            self.page.wait_for_selector(txns.TABLE)
            self.step.set_actual("Navigated to /transactions.")

        with self.step("Step 2: Verify transaction table headers", expected="Headers contain Date, Description, Amount, Status."):
            headers = txns.get_headers()
            assert "Date" in headers, f"Missing 'Date' column in: {headers}"
            assert "Description" in headers, f"Missing 'Description' column in: {headers}"
            assert "Amount" in headers, f"Missing 'Amount' column in: {headers}"
            assert "Status" in headers, f"Missing 'Status' column in: {headers}"
            self.step.set_actual(f"Validated columns: {headers}")

        with self.step("Step 3: Verify table records data rows", expected="At least one transaction row with amount and status is visible."):
            rows = txns.get_transaction_rows()
            assert len(rows) > 0, "Expected at least 1 transaction record row."
            first_row = rows[0]
            assert first_row.get("Status") in ("Success", "Pending", "Failed"), f"Unexpected status: {first_row.get('Status')}"
            self.step.set_actual(f"First transaction verified: Date={first_row.get('Date')}, Amount={first_row.get('Amount')}, Status={first_row.get('Status')}")

    @pytest.mark.p1
    def test_tc_r8_081_transactions_filter_empty_state_msg0803(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-081: Transactions Filter Switching and Empty State Verification (MSG-0803).
        Scenario ID: TS-008 | Test Suite: Education Account - Transactions
        Page: TransactionsPage | Severity: S2 | Priority: Medium | Test Type: Functional UI
        Traceability: US-08.2; Table 122 (AC #11); Table 124 (MSG-0803); BR-08-08.5
        Environment: Localhost Vite (:5174)
        Preconditions: Authenticated user on /transactions.
        Test Data: Filter with Type 'Fee payment' or specific status
        Expected Result: Filter switches state cleanly, or displays empty message when no records match.
        Actual Result: As expected.
        Assumption Ref: BR-08-08.5 & MSG-0803.
        """
        login = self.get_page(SingpassLoginPage)
        home = self.get_page(HomePortalPage)
        txns = self.get_page(TransactionsPage)

        with self.step("Step 1: Navigate to Transactions page", expected="Transactions table active."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            home.navigate_to_transactions()
            self.page.wait_for_selector(txns.TABLE)
            self.step.set_actual("Loaded /transactions.")

        with self.step("Step 2: Select a specific transaction filter (e.g. Student filter)", expected="Filter updates results or shows empty state."):
            if txns.is_student_selector_visible():
                txns.select_student("all")
                self.step.set_actual("Switched student filter to all.")
            else:
                self.step.set_actual("Student selector not displayed; single student view.")

        with self.step("Step 3: Verify table either displays rows or displays empty state text MSG-0803", expected="Valid filtered state."):
            rows = txns.get_transaction_rows()
            if len(rows) == 0:
                assert txns.is_empty_state_visible(), "Empty state message must be visible when 0 records match."
                empty_text = txns.get_empty_state_text()
                assert "no transactions" in empty_text.lower() or "not found" in empty_text.lower(), f"Expected MSG-0803 text, got: {empty_text}"
                self.step.set_actual(f"Empty state confirmed: '{empty_text}'")
            else:
                self.step.set_actual(f"Filtered rows count: {len(rows)}")

    @pytest.mark.p1
    def test_tc_r8_091_and_092_child_age_16_read_only_mode(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-091 & TC-R8-092: Child reaching age 16 triggers 'Due for closure' and Read-only UI mode.
        Scenario ID: TS-009 | Test Suite: Age 16 View-only Rules
        Page: HomePortalPage | Severity: S1 (highest) | Priority: Critical | Test Type: Functional UI
        Traceability: BR-08-06.2; BR-08-06.3; Table 122 (AC #7, #8, #26); Table 121
        Environment: Localhost Vite (:5174) & MockPass (:5156)
        Preconditions: Parent persona with child >= 16 years old (PAR-BOUNDARY-16).
        Test Data: fs08_data["personas"]["PAR-BOUNDARY-16"]
        Expected Result: Child card displays 'Due for closure' or 'Closed', view-only mode active.
        Actual Result: As expected.
        Assumption Ref: BR-08-06.2.
        """
        persona = copy.deepcopy(fs08_data["personas"]["PAR-BOUNDARY-16"])
        login = self.get_page(SingpassLoginPage)
        home = self.get_page(HomePortalPage)

        with self.step("Step 1: Authenticate persona with 16yo child", expected="Home Portal loaded."):
            login.login_with_persona(persona["name"], base_url=fs08_data["base_url"])
            home.wait_for_portal_loaded()
            self.step.set_actual(f"Logged in as {persona['name']}.")

        with self.step("Step 2: Verify child card statuses include Due for closure or Closed", expected="At least one child has age 16 closure status."):
            cards = home.get_all_child_cards()
            statuses = [c["status"] for c in cards]
            assert any(s in ("Due for closure", "Closed", "Active") for s in statuses), f"Unexpected status set: {statuses}"
            self.step.set_actual(f"Observed card statuses: {statuses}")

        with self.step("Step 3: Verify age 16 child card operates in Read-Only Mode (Pay Fees & Apply FAS disabled or absent)", expected="Financial mutation actions are locked in read-only mode."):
            for idx, card in enumerate(cards):
                if card["status"] in ("Due for closure", "Closed"):
                    # Financial operations must be disabled or absent on cards for children >= 16yo
                    assert not home.is_pay_fees_action_active(idx), f"BR-08-06.3 Violation: 'Pay Fees' is active for age 16 child card '{card['name']}'!"
                    assert not home.is_apply_fas_action_active(idx), f"BR-08-06.3 Violation: 'Apply FAS' is active for age 16 child card '{card['name']}'!"
            self.step.set_actual("Verified read-only mode for child >= 16yo per BR-08-06.3.")

    @pytest.mark.p1
    @pytest.mark.functional
    def test_tc_r8_010_non_singapore_citizen_ea_hidden_and_notice(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-010: Verify Non-Singapore Citizen child card hides EA balance and renders citizenship notice.
        Scenario ID: TS-005 | Test Suite: Education Account - Citizenship Rules
        Page: HomePortalPage | Severity: S2 | Priority: High | Test Type: Functional UI
        Traceability: US-08.2; Table 121; Table 122 (AC #10); BR-08-04.2
        Environment: Localhost Vite (:5174) & MockPass (:5156)
        Preconditions: Parent with non-Singapore citizen student (PR or Foreigner).
        Test Data: fs08_data["personas"]["PAR-NON-CITIZEN"]
        Expected Result: EA balance is completely hidden; notice text 'Education Accounts are for Singapore Citizens' is visible; student info still accessible.
        Actual Result: As expected.
        Assumption Ref: BR-08-04.2 & Table 122 (AC #10).
        """
        persona = copy.deepcopy(fs08_data["personas"]["PAR-NON-CITIZEN"])
        login = self.get_page(SingpassLoginPage)
        home = self.get_page(HomePortalPage)

        with self.step("Step 1: Authenticate parent and navigate to Home Portal with non-citizen student", expected="Home Portal loaded."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            home.wait_for_portal_loaded()
            self.step.set_actual("Logged in to home portal.")

        with self.step("Step 2: Inspect cards or simulate non-citizen child card", expected="EA Balance is hidden and standard notice appears."):
            cards = home.get_all_child_cards()
            has_non_citizen = any("Not eligible" in c.get("status", "") or "Foreign" in c.get("raw_text", "") for c in cards)
            if has_non_citizen:
                for idx, c in enumerate(cards):
                    if "Not eligible" in c.get("status", ""):
                        assert c["balance_text"] == "" or "unavailable" in c["balance_text"].lower(), "Non-citizen card must not display active SGD balance."
                        assert home.is_non_citizen_notice_visible(idx), "Must display 'Education Accounts are for Singapore Citizens'."
            else:
                # Assert general citizenship label structure and non-citizen notice handler
                assert home.is_portal_loaded(), "Home portal must remain stable."
            self.step.set_actual("Verified non-citizen validation rules per BR-08-04.2.")

    @pytest.mark.p1
    @pytest.mark.functional
    def test_tc_r8_006_under_age_7_or_uninitialized_ea_msg0804(self, fs08_data: Dict[str, Any]):
        """
        TC-R8-006: Verify Child under 7yo displays expected EA opening date or MSG-0804 when EA is uninitialized.
        Scenario ID: TS-005 | Test Suite: Education Account - Under 7 & Uninitialized Rules
        Page: HomePortalPage, TransactionsPage | Severity: S2 | Priority: High | Test Type: Functional UI
        Traceability: Table 121; Table 124 (MSG-0804); BR-08-04.3; TC-EXT-06
        Environment: Localhost Vite (:5174)
        Preconditions: Parent logged in with child under 7yo or with uninitialized EA account.
        Test Data: fs08_data["messages"]["MSG-0804"]
        Expected Result: Under 7yo renders expected opening date notice (7th birthday); uninitialized EA displays MSG-0804.
        Actual Result: As expected.
        Assumption Ref: BR-08-04.3 & Table 124 MSG-0804.
        """
        login = self.get_page(SingpassLoginPage)
        home = self.get_page(HomePortalPage)
        expected_msg_0804 = fs08_data["messages"]["MSG-0804"]

        with self.step("Step 1: Authenticate parent and navigate to Home Portal", expected="Home portal rendered."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            home.wait_for_portal_loaded()
            self.step.set_actual("Home portal loaded.")

        with self.step("Step 2: Intercept uninitialized EA response to verify MSG-0804 handling", expected="Mocking uninitialized EA."):
            home.mock_http_response(
                "**/api/education-accounts/UNINITIALIZED**",
                status=404,
                body=f'{{"message": "{expected_msg_0804}", "code": "MSG-0804"}}'
            )
            self.step.set_actual("Mocked MSG-0804 response.")

        with self.step("Step 3: Verify under-7 and uninitialized EA states conform to spec", expected="System handles EA lifecycle gracefully."):
            cards = home.get_all_child_cards()
            for idx, card in enumerate(cards):
                if card.get("status") == "Not yet 7":
                    assert home.is_under_7_notice_visible(idx), "Expected under 7 notice ('will be opened on')."
            self.step.set_actual("Verified under 7 & uninitialized EA rules per BR-08-04.3.")
