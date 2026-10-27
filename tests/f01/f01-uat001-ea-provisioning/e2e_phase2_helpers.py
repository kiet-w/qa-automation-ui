"""
tests/f01/f01-uat001-ea-provisioning/e2e_phase2_helpers.py

Phase 2 helper functions for TC-UAT001-15 E2E test.
Encapsulates data classification verification steps (Steps 5–11):
  - Eligible SC student Active verification
  - Student Profile dialog open/close
  - Missing parent NRIC still Active (F01-BR04)
  - Over-age Deactive assertion (F01-BR02)
  - Status filter Active/Deactive isolation

Called from test_integration_uat001_e2e.py to keep the main file < 250 lines.
Complies with Invariant 1 (zero assertions in Page Objects) and Invariant 9 (< 200 lines).
"""
import copy
from typing import Any, Dict, TYPE_CHECKING

from pages.f01.education_accounts_page import EducationAccountsPage

if TYPE_CHECKING:
    from tests.base_test import BaseTest


def verify_eligible_student_active(
    test: "BaseTest",
    ea_page: EducationAccountsPage,
    e2e_data: Dict[str, Any],
) -> int:
    """
    Step 5–6: Search eligible student, assert Active status and profile dialog.
    Returns: row_count after search (for downstream assertions).
    Source: F01-BR01, F01-BR02, F01-AC01.
    """
    eligible = copy.deepcopy(e2e_data["eligible_students"]["primary"])

    with test.step("Step 5: Verify eligible SC student (Isaac Teo) has Active status"):
        ea_page.search(eligible["nric"])
        found_row = ea_page.find_row_by_nric(eligible["nric"])
        assert found_row is not None, \
            f"Eligible student {eligible['nric']} must appear in table after Sync #1"
        assert eligible["expected_status"].lower() in found_row.get("status", "").lower(), \
            (
                f"Student {eligible['nric']} must have status '{eligible['expected_status']}'. "
                f"Got: '{found_row.get('status')}'"
            )
        assert "Singapore Citizen".lower() in found_row.get("citizenship", "").lower(), \
            f"Student {eligible['nric']} citizenship must show 'Singapore Citizen'"
        test.step.set_actual(
            f"Isaac Teo ({eligible['nric']}): Status='{found_row.get('status')}', "
            f"Citizenship='{found_row.get('citizenship')}'. Active confirmed. F01-BR01/BR02."
        )

    with test.step("Step 6: Verify Student Profile modal opens, shows data, and closes cleanly"):
        profile_meta = copy.deepcopy(e2e_data["profile_dialog"])
        profile_dlg = ea_page.open_student_details(0)
        assert profile_dlg.is_visible(timeout=5000), \
            "Student Profile dialog must open when 'View details' is clicked"
        content = profile_dlg.get_content_text()
        assert profile_meta["expected_heading_fragment"].lower() in content.lower(), \
            f"Profile dialog must contain '{profile_meta['expected_heading_fragment']}'"
        profile_dlg.close()
        assert not profile_dlg.is_visible(timeout=3000), \
            "Profile dialog must close after clicking 'Close'"
        test.step.set_actual("Student Profile dialog: opened, content verified, closed. F01-AC01.")

    return ea_page.get_row_count()


def verify_missing_parent_active(
    test: "BaseTest",
    ea_page: EducationAccountsPage,
    e2e_data: Dict[str, Any],
) -> None:
    """
    Step 7: Verify student with missing parental NRIC still gets Active EA.
    Source: F01-BR04, F01-AC09.
    """
    missing = copy.deepcopy(e2e_data["eligible_student_missing_parent"])

    with test.step("Step 7: Verify missing parent NRIC student is still Active (F01-BR04)"):
        ea_page.search(missing["nric"])
        found = ea_page.find_row_by_nric(missing["nric"])
        assert found is not None, \
            f"Student with missing parent NRIC ({missing['nric']}) must appear after sync"
        assert missing["expected_status"].lower() in found.get("status", "").lower(), \
            (
                f"Missing-parent student must be '{missing['expected_status']}'. "
                f"Got: '{found.get('status')}'"
            )
        test.step.set_actual(
            f"Adam Wong ({missing['nric']}): '{found.get('status')}'. "
            "Parental NRIC absence does NOT block Active EA. F01-BR04 confirmed."
        )


def verify_over_age_deactive(
    test: "BaseTest",
    ea_page: EducationAccountsPage,
    e2e_data: Dict[str, Any],
) -> None:
    """
    Step 8: Verify over-age (17 yrs) citizen is Deactive or absent from table.
    Source: F01-BR02, F01-AC05.
    """
    over_age = copy.deepcopy(e2e_data["ineligible_students"]["over_age_17"])

    with test.step("Step 8: Verify over-age citizen (17 yrs) is Deactive (F01-BR02)"):
        ea_page.search(over_age["nric"])
        found = ea_page.find_row_by_nric(over_age["nric"])
        if found is not None:
            status = found.get("status", "")
            assert over_age["expected_status"].lower() in status.lower(), \
                (
                    f"Over-age citizen ({over_age['nric']}, age {over_age['age']}) must be "
                    f"'{over_age['expected_status']}'. Got: '{status}'"
                )
            test.step.set_actual(
                f"Ethan Rahman ({over_age['nric']}, age {over_age['age']}): "
                f"'{status}'. Deactive confirmed. F01-BR02."
            )
        else:
            test.step.set_actual(
                f"Over-age citizen {over_age['nric']} not found in table "
                "(skip outcome — no EA created). F01-BR02 verified."
            )


def verify_status_filters(
    test: "BaseTest",
    ea_page: EducationAccountsPage,
    e2e_data: Dict[str, Any],
) -> None:
    """
    Steps 9–10: Verify Active and Deactive status filter isolation.
    Source: TC-UAT001-10, BSK dropdown selectors.
    """
    status_vals = copy.deepcopy(e2e_data["status_filter_values"])

    with test.step("Step 9: Status filter 'Active' — all visible rows must be Active"):
        ea_page.clear_search()
        ea_page.filter_by_status(status_vals["active"])
        active_rows = ea_page.get_all_rows_data()
        assert len(active_rows) >= 1, \
            "At least 1 Active account must be visible after Active filter"
        for row in active_rows:
            assert "deactive" not in row.get("status", "").lower(), \
                f"Row {row.get('nric')} must NOT be Deactive under Active filter"
        test.step.set_actual(
            f"Active filter: {len(active_rows)} row(s) visible. All are Active."
        )

    with test.step("Step 10: Status filter 'Deactive' — all visible rows must be Deactive"):
        ea_page.filter_by_status(status_vals["deactive"])
        deactive_rows = ea_page.get_all_rows_data()
        for row in deactive_rows:
            row_status = row.get("status", "").lower()
            assert "deactive" in row_status or "active" not in row_status, \
                f"Row {row.get('nric')} must be Deactive under Deactive filter"
        test.step.set_actual(
            f"Deactive filter: {len(deactive_rows)} row(s) visible. Filter isolation confirmed."
        )
