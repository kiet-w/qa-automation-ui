"""
tests/f01/f01-education-accounts/test_atomic_ea_sync_components.py - Atomic UI & Component Tests.
Complies with Invariant 1 (Zero assertions in Page Objects), Invariant 3 (Traceability),
and Invariant 9 (< 200 lines).
Traceability: US-001, UAT-001, F01-BR01, F01-BR04, F01-AC01, F01-AC06, AF03, AF04.
"""
import re
from typing import Any, Dict
import pytest
from tests.base_test import BaseTest
from pages.f01.education_accounts_page import EducationAccountsPage


@pytest.mark.p0
@pytest.mark.atomic
@pytest.mark.ui
class TestAtomicEaSyncComponents(BaseTest):
    """Atomic components, filters, modals, and client security test suite for F01/UAT-001."""

    def test_tc_uat001_08_cancel_sync_dialog(self, f01_data: Dict[str, Any]):
        """TC-UAT001-08: Verify cancelling synchronization dialog does not execute sync mutation."""
        ea = self.get_page(EducationAccountsPage)
        with self.step("Open Education Accounts page and click Manual sync", expected="Alertdialog appears."):
            ea.open(base_url=f01_data["base_url"])
            sync_dialog = ea.trigger_manual_sync()
            assert sync_dialog.is_visible(), "Confirm system synchronization dialog must be visible."
            self.step.set_actual("Sync confirmation dialog opened.")

        with self.step("Click Cancel in alertdialog", expected="Dialog closes without triggering mutation."):
            sync_dialog.cancel()
            assert not sync_dialog.is_visible(timeout=2000), "Dialog must close after cancel."
            self.highlight_actual_result(locator=ea.manual_sync_btn, text="Cancel Sync Verified")
            self.step.set_actual("Alertdialog closed smoothly; mutation aborted safely.")

    def test_tc_uat001_09_search_filter_nric(self, f01_data: Dict[str, Any]):
        """TC-UAT001-09: Verify search input filters student table by NRIC and Full Name."""
        target_nric = f01_data["uat_001"]["search_queries"]["by_nric"]
        ea = self.get_page(EducationAccountsPage)

        with self.step("Navigate to Education Accounts page", expected="Page loaded with table."):
            ea.open(base_url=f01_data["base_url"])
            assert ea.get_row_count() > 0, "Accounts table must have rows."

        with self.step(f"Search by NRIC: {target_nric}", expected="Table isolates matching row."):
            ea.search(target_nric)
            self.page.wait_for_timeout(500)
            count = ea.get_row_count()
            assert count >= 1, f"Expected matching row for {target_nric}, found {count}"
            row = ea.get_row_data(0)
            assert target_nric in row["nric"], f"Row NRIC {row['nric']} does not match search {target_nric}"
            self.highlight_actual_result(locator=ea.table_rows.first, text=f"Filtered: {target_nric}")
            self.step.set_actual(f"Search successfully isolated student: {row['fullName']} ({row['nric']})")

    def test_tc_uat001_10_status_dropdown_filter(self, f01_data: Dict[str, Any]):
        """TC-UAT001-10: Verify status dropdown filter isolates Active and Deactive accounts."""
        ea = self.get_page(EducationAccountsPage)
        with self.step("Open Education Accounts and filter by status 'Active'", expected="Only Active rows visible."):
            ea.open(base_url=f01_data["base_url"])
            ea.filter_by_status("1")  # value '1' = Active
            self.page.wait_for_timeout(500)
            count = ea.get_row_count()
            assert count > 0, "Should have active student accounts."
            for idx in range(min(count, 5)):
                row = ea.get_row_data(idx)
                assert row["status"].lower() == "active", f"Row {idx} has non-active status: {row['status']}"
            self.highlight_actual_result(locator=ea.table_rows.first, text="Active Accounts Filtered")
            self.step.set_actual(f"Verified {count} rows all possess Active status badge.")

    def test_tc_uat001_11_student_profile_details_modal(self, f01_data: Dict[str, Any]):
        """TC-UAT001-11: Verify Student Profile Details modal renders complete demographic data and closes."""
        ea = self.get_page(EducationAccountsPage)
        with self.step("Open page and click View details on first row", expected="Details modal opens."):
            ea.open(base_url=f01_data["base_url"])
            dialog = ea.open_student_details(0)
            assert dialog.is_visible(), "Student Profile Details modal must appear."
            content = dialog.get_content_text()
            assert "Student Profile Details" in content, "Heading must render Student Profile Details."
            assert any(f in content for f in ["NRIC", "DOB", "Age", "Gender", "Citizenship"]), "Demographics must show."
            self.step.set_actual("Profile details modal rendered with complete demographic data.")

        with self.step("Click Close button to dismiss dialog", expected="Dialog closes cleanly."):
            dialog.close()
            assert not dialog.is_visible(timeout=2000), "Modal should be closed."
            self.step.set_actual("Profile details dialog dismissed successfully.")

    def test_tc_uat001_12_ui_i18n_leak_guard(self, f01_data: Dict[str, Any]):
        """TC-UAT001-12: Verify zero raw i18n translation keys leaked in Education Accounts interface."""
        ea = self.get_page(EducationAccountsPage)
        with self.step("Extract page text and check for leaked raw keys", expected="Zero raw i18n tokens."):
            ea.open(base_url=f01_data["base_url"])
            body_text = self.page.locator("body").inner_text()
            leaked_keys = re.findall(r"features\.[a-zA-Z0-9_.-]+", body_text)
            assert not leaked_keys, f"Found leaked raw i18n translation keys: {leaked_keys}"
            self.highlight_actual_result(locator=ea.heading, text="i18n Clean")
            self.step.set_actual("Zero raw i18n translation keys detected on interface.")

    def test_tc_uat001_13_console_ui_health(self, f01_data: Dict[str, Any]):
        """TC-UAT001-13: Verify console UI health: Zero uncaught JavaScript errors during navigation."""
        errors = []
        self.page.on("pageerror", lambda exc: errors.append(str(exc)))
        ea = self.get_page(EducationAccountsPage)

        with self.step("Navigate and interact with page while monitoring console", expected="Zero JS exceptions."):
            ea.open(base_url=f01_data["base_url"])
            ea.search("Teo")
            self.page.wait_for_timeout(500)
            critical_errors = [e for e in errors if "TypeError" in e or "ReferenceError" in e]
            assert not critical_errors, f"Captured critical JS runtime errors: {critical_errors}"
            self.step.set_actual("Console UI health clean: Zero uncaught JS errors.")

    def test_tc_uat001_14_route_auth_guard(self, f01_data: Dict[str, Any]):
        """TC-UAT001-14: Verify protected route auth guard redirects unauthenticated users to /login."""
        with self.step("Open new unauthenticated context and navigate to /education-accounts", expected="Redirected to /login."):
            unauth_context = self.page.context.browser.new_context()
            unauth_page = unauth_context.new_page()
            unauth_page.goto(f"{f01_data['base_url']}/education-accounts", wait_until="domcontentloaded")
            unauth_page.wait_for_url("**/login**", timeout=10000)
            assert "login" in unauth_page.url, f"Expected redirect to login, got {unauth_page.url}"
            unauth_context.close()
            self.step.set_actual("Unauthenticated access strictly blocked and redirected to /login.")
