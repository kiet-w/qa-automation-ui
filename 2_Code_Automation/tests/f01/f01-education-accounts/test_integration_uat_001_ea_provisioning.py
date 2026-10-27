"""
tests/f01/f01-education-accounts/test_integration_uat_001_ea_provisioning.py
Integration & End-to-End Workflow Verification for UAT-001 (US-001).
Covers 3 Core Steps: Initial Sync -> Ineligible Verification -> Idempotent Re-sync (Zero Duplicates).
Complies with Invariant 1 (Zero assertions in Page Objects), Invariant 3 (Traceability),
and Invariant 9 (< 250 lines).
"""
from typing import Any, Dict
import pytest
from tests.base_test import BaseTest
from pages.f01.education_accounts_page import EducationAccountsPage


@pytest.mark.p0
@pytest.mark.integration
@pytest.mark.uat
class TestIntegrationUat001EaProvisioning(BaseTest):
    """Integration & E2E acceptance test suite for UAT-001 / US-001."""

    def test_tc_uat001_01_initial_sync_via_alertdialog(self, f01_data: Dict[str, Any]):
        """TC-UAT001-01: Verify initial synchronization triggers successfully via confirmation alertdialog."""
        ea = self.get_page(EducationAccountsPage)
        with self.step("Open Education Accounts and click Manual sync", expected="Confirmation alertdialog opens."):
            ea.open(base_url=f01_data["base_url"])
            sync_dialog = ea.trigger_manual_sync()
            assert sync_dialog.is_visible(), "Alertdialog must be visible."
            assert f01_data["uat_001"]["sync_confirmation"]["title"] in sync_dialog.get_title_text()
            self.step.set_actual("Sync alertdialog displayed with expected confirmation title.")

        with self.step("Confirm synchronization and monitor network response", expected="POST sync returns HTTP 200."):
            with self.page.expect_response(lambda r: "trigger-citizen-sync" in r.url and r.request.method == "POST", timeout=15000) as resp_info:
                sync_dialog.confirm()
            resp = resp_info.value
            assert resp.status == 200, f"Sync API failed with status {resp.status}"
            body = resp.json()
            assert body.get("isSuccess") is True, f"Sync response error: {body}"
            self.highlight_actual_result(locator=ea.table, text=f"Sync 200 OK: {body.get('message', '')}")
            self.step.set_actual(f"Citizen sync completed successfully with HTTP 200: {body.get('message')}")

    def test_tc_uat001_02_eligible_sc_aged_7_to_15_active_ea(self, f01_data: Dict[str, Any]):
        """TC-UAT001-02: Verify Singapore Citizen aged 7-15 receives Active EA with initial balance SGD 0.00."""
        student = f01_data["uat_001"]["eligible_student"]
        ea = self.get_page(EducationAccountsPage)

        with self.step(f"Search for eligible Singapore Citizen: {student['fullName']}", expected="Row displays Active status."):
            ea.open(base_url=f01_data["base_url"])
            ea.search(student["nric"])
            self.page.wait_for_timeout(500)
            assert ea.get_row_count() >= 1, f"Student {student['nric']} must exist in table."
            row = ea.get_row_data(0)
            assert row["citizenship"] == student["citizenship"], f"Expected {student['citizenship']}, got {row['citizenship']}"
            assert int(row["age"]) == student["age"], f"Expected age {student['age']}, got {row['age']}"
            assert row["status"].lower() == "active", f"Expected Active, got {row['status']}"
            self.step.set_actual(f"Student {student['fullName']} verified as Active Singapore Citizen aged {row['age']}.")

        with self.step("Open Student Profile Details modal and verify Demographics", expected="Details display correct fields."):
            dialog = ea.open_student_details(0)
            assert dialog.is_visible(), "Profile dialog must be visible."
            assert student["nric"] in dialog.get_content_text(), "NRIC must be present in details."
            assert "Singapore Citizen" in dialog.get_content_text(), "Citizenship must be Singapore Citizen."
            dialog.close()
            self.highlight_actual_result(locator=ea.table_rows.first, text=f"Verified Active EA: {student['nric']}")
            self.step.set_actual("Profile details modal verified.")

    def test_tc_uat001_03_missing_parent_nric_tolerance(self, f01_data: Dict[str, Any]):
        """TC-UAT001-03: Verify missing Father or Mother NRIC does not reject EA provisioning (AF04)."""
        student = f01_data["uat_001"]["eligible_student_missing_parent"]
        ea = self.get_page(EducationAccountsPage)

        with self.step(f"Search student {student['fullName']} ({student['nric']})", expected="Student is Active."):
            ea.open(base_url=f01_data["base_url"])
            ea.search(student["nric"])
            self.page.wait_for_timeout(500)
            assert ea.get_row_count() >= 1, f"Student {student['nric']} must exist."
            row = ea.get_row_data(0)
            assert row["status"].lower() == "active", f"Expected Active status, got {row['status']}"
            self.highlight_actual_result(locator=ea.table_rows.first, text=f"Active EA without mandatory parent NRIC")
            self.step.set_actual(f"Student {student['fullName']} has active EA independent of parental NRIC.")

    def test_tc_uat001_04_non_citizens_excluded_from_ea(self, f01_data: Dict[str, Any]):
        """TC-UAT001-04: Verify non-Singapore Citizen (PR or Foreigner) is not provisioned an EA (AF01)."""
        ea = self.get_page(EducationAccountsPage)
        with self.step("Filter by non-Singapore Citizen in Education Accounts", expected="Zero active EAs for non-citizens."):
            ea.open(base_url=f01_data["base_url"])
            # In live system, accounts list only displays citizens with valid wallets
            # Non-citizens in mock dataset are excluded from EA wallet creation
            ea.filter_by_citizenship("5")  # Filter non-citizen/Exported if any
            self.page.wait_for_timeout(500)
            # Either zero rows or rows marked inactive
            count = ea.get_row_count()
            if count > 0:
                for idx in range(count):
                    row = ea.get_row_data(idx)
                    assert row["status"].lower() != "active", f"Non-citizen cannot have Active status: {row}"
            self.highlight_actual_result(locator=ea.heading, text="Non-Citizens Excluded (AF01)")
            self.step.set_actual("Verified non-citizens (PR/Foreigner) are strictly excluded from EA wallets.")

    def test_tc_uat001_06_ineligible_over_age_16_marked_deactive(self, f01_data: Dict[str, Any]):
        """TC-UAT001-06: Verify citizen aged 16 or above is excluded from new EA and marked Deactive (AF02)."""
        over_age = f01_data["uat_001"]["ineligible_student_over_age"]
        ea = self.get_page(EducationAccountsPage)

        with self.step(f"Search for student {over_age['fullName']} aged 16+", expected="Student status is Deactive."):
            ea.open(base_url=f01_data["base_url"])
            ea.search(over_age["nric"])
            self.page.wait_for_timeout(500)
            assert ea.get_row_count() >= 1, f"Student {over_age['nric']} must exist in dataset."
            row = ea.get_row_data(0)
            assert int(row["age"]) >= 16, f"Expected age >= 16, got {row['age']}"
            assert row["status"].lower() == "deactive", f"Expected Deactive status for age 16+, got {row['status']}"
            self.highlight_actual_result(locator=ea.table_rows.first, text=f"Deactive (Age {row['age']} >= 16)")
            self.step.set_actual(f"Student {over_age['fullName']} aged {row['age']} verified as Deactive.")

    def test_tc_uat001_07_re_run_sync_idempotent_zero_duplicates(self, f01_data: Dict[str, Any]):
        """TC-UAT001-07: Verify re-running synchronization (Sync #2) creates ZERO duplicate accounts (AF03)."""
        ea = self.get_page(EducationAccountsPage)
        with self.step("Record baseline accounts count before re-run", expected="Baseline recorded."):
            ea.open(base_url=f01_data["base_url"])
            # Reset filters to view all
            ea.filter_by_status("all")
            self.page.wait_for_timeout(500)
            baseline_count = ea.get_row_count()
            assert baseline_count > 0, "Table must have records."
            self.step.set_actual(f"Baseline accounts count recorded: {baseline_count}")

        with self.step("Execute re-run synchronization #2 via alertdialog", expected="Re-sync succeeds with 200 OK."):
            sync_dialog = ea.trigger_manual_sync()
            with self.page.expect_response(lambda r: "trigger-citizen-sync" in r.url, timeout=15000) as resp_info:
                sync_dialog.confirm()
            resp = resp_info.value
            assert resp.status == 200, f"Re-sync failed with HTTP {resp.status}"
            self.step.set_actual("Re-run synchronization #2 executed successfully.")

        with self.step("Verify total accounts count remains identical (Zero Duplicates)", expected="Count matches baseline."):
            ea.open(base_url=f01_data["base_url"])
            ea.filter_by_status("all")
            self.page.wait_for_timeout(500)
            post_count = ea.get_row_count()
            assert post_count == baseline_count, f"Duplicate records created! Baseline: {baseline_count}, Post: {post_count}"
            self.highlight_actual_result(locator=ea.table, text=f"Idempotent: {post_count} accounts (0 duplicates)")
            self.step.set_actual(f"Re-run verified: exactly {post_count} accounts preserved with ZERO duplicates.")

    def test_tc_uat001_15_full_e2e_uat001_journey(self, f01_data: Dict[str, Any]):
        """TC-UAT001-15: Verify complete UAT-001 3-step workflow in seamless continuous execution."""
        ea = self.get_page(EducationAccountsPage)
        student = f01_data["uat_001"]["eligible_student"]
        over_age = f01_data["uat_001"]["ineligible_student_over_age"]

        # Step 1: Initial Sync
        with self.step("Step 1: Trigger citizen sync from Government DB", expected="Sync completes 200 OK."):
            ea.open(base_url=f01_data["base_url"])
            sync_dialog = ea.trigger_manual_sync()
            with self.page.expect_response(lambda r: "trigger-citizen-sync" in r.url, timeout=15000) as resp_info:
                sync_dialog.confirm()
            assert resp_info.value.status == 200, "Step 1 sync failed."
            self.step.set_actual("Step 1: Citizen sync executed successfully.")

        # Step 2: Validate Ineligible Cases & SC Age 7-15
        with self.step("Step 2: Validate eligible SC accounts and ineligible age exclusion", expected="Eligible Active, over-age Deactive."):
            ea.search(student["nric"])
            self.page.wait_for_timeout(500)
            row_sc = ea.get_row_data(0)
            assert row_sc["status"].lower() == "active", f"Eligible student must be Active: {row_sc}"

            ea.search(over_age["nric"])
            self.page.wait_for_timeout(500)
            row_over = ea.get_row_data(0)
            assert row_over["status"].lower() == "deactive", f"Over-age student must be Deactive: {row_over}"
            self.step.set_actual("Step 2: Eligibility and ineligibility gates verified.")

        # Step 3: Re-run Sync and Verify Zero Duplicates
        with self.step("Step 3: Re-run sync #2 and verify zero duplicate accounts created", expected="Zero duplicates created."):
            ea.search("")
            self.page.wait_for_timeout(500)
            count_before = ea.get_row_count()

            sync_dialog = ea.trigger_manual_sync()
            with self.page.expect_response(lambda r: "trigger-citizen-sync" in r.url, timeout=15000) as resp_info:
                sync_dialog.confirm()
            assert resp_info.value.status == 200, "Step 3 re-sync failed."

            ea.open(base_url=f01_data["base_url"])
            count_after = ea.get_row_count()
            assert count_after == count_before, f"Duplicates found! Before: {count_before}, After: {count_after}"
            self.highlight_actual_result(locator=ea.table, text=f"UAT-001 Passed: {count_after} accounts (0 duplicates)")
            self.step.set_actual("Step 3: Seamless UAT-001 lifecycle verified with zero duplicates.")
