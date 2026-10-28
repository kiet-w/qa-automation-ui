"""
tests/f01/f01-uat001-ea-provisioning/test_integration_uat001_e2e.py

TC-UAT001-15 — Full End-to-End Acceptance Journey
==================================================
Scenario ID : TS-UAT001-E2E
Severity    : S1 (Critical) | Priority: Critical
Test Type   : E2E Acceptance | Environment: Localhost :5173
Persona     : MOE HQ Admin (admin@IAM.edu.vn)
Traceability: US-001, UAT-001, F01-BR01~BR05, F01-AC01/03/04/05/06/09/12

Phase 1 — Initial Sync & Provisioning  (Steps  1– 4)
Phase 2 — Data Classification Check    (Steps  5–11)  → delegated to e2e_phase2_helpers
Phase 3 — Re-Sync Idempotency (Sync#2) (Steps 12–14)

Invariant compliance:
  I-1: No assert in Page Objects   I-2: All data via deepcopy from JSON
  I-4: Zero time.sleep()           I-9: File < 250 lines
  I-11: AI does NOT run this test
"""
import copy
import pytest

from tests.base_test import BaseTest
from pages.f01.education_accounts_page import EducationAccountsPage

import sys
from pathlib import Path
_THIS_DIR = str(Path(__file__).parent)
if _THIS_DIR not in sys.path:
    sys.path.insert(0, _THIS_DIR)

from e2e_phase2_helpers import (
    verify_eligible_student_active,
    verify_missing_parent_active,
    verify_over_age_deactive,
    verify_status_filters,
)


@pytest.fixture(scope="class")
def e2e_data(raw_uat001_data):
    """Deep-copied UAT-001 dataset scoped to test class (Invariant 2)."""
    return copy.deepcopy(raw_uat001_data)


class TestTSUAT001E2E(BaseTest):
    """
    TS-UAT001-E2E: Complete 3-Phase UAT-001 lifecycle in one continuous authenticated session.
    Uses e2e_phase2_helpers.py for Phase 2 delegation (Invariant 9 — file < 250 lines).
    """

    @pytest.mark.p0
    @pytest.mark.priority_critical
    @pytest.mark.functional
    @pytest.mark.regression
    @pytest.mark.uat
    def test_tc_uat001_15_full_e2e_provisioning_journey(
        self,
        e2e_data,
        ea_page: EducationAccountsPage,
    ):
        """
        TC-UAT001-15 — Verify complete UAT-001 3-step lifecycle in seamless E2E execution.

        Preconditions : Authenticated as MOE HQ Admin. Government citizen dataset populated.
        Test Data     : data/f01/f01_uat001_data.json (deep-copied via e2e_data fixture)
        Expected      :
          [Phase 1] Sync #1 triggers OK; Active EAs provisioned; dialog closes; POST fired.
          [Phase 2] SC age 7–15 → Active; missing parent → Active; age 17 → Deactive.
                    Active/Deactive filters isolate records correctly.
          [Phase 3] Sync #2 → total row count unchanged (0 duplicates). F01-BR05/AC12 pass.
        """

        # ════════════════════════════════════════════════════════════════════════
        # PHASE 1: Navigate & Trigger Initial Sync (#1)
        # ════════════════════════════════════════════════════════════════════════

        with self.step("Step 1: Navigate to /education-accounts and verify heading visible"):
            ea_page.open()
            assert ea_page.heading.is_visible(timeout=10000), \
                "Page heading 'Education Accounts' must be visible after navigation"
            self.step.set_actual("Navigated to /education-accounts. Heading confirmed visible.")

        with self.step("Step 2: Click 'Manual sync' — verify sync dialog appears (alertdialog)"):
            sync_dlg = ea_page.trigger_manual_sync()
            assert sync_dlg.is_visible(timeout=5000), \
                "Sync confirmation dialog must appear after 'Manual sync' click"
            title = sync_dlg.get_title_text()
            assert title, "Sync dialog title text must not be empty"
            self.step.set_actual(f"Sync dialog visible. Title: '{title}'.")

        with self.step("Step 3: Click 'Confirm' — POST /trigger-citizen-sync must fire, dialog closes"):
            sync_fired: list = []
            self.page.on(
                "request",
                lambda req: sync_fired.append(req.url)
                if "trigger-citizen-sync" in req.url and req.method == "POST"
                else None,
            )
            sync_dlg.confirm()
            assert not sync_dlg.is_visible(timeout=3000), \
                "Sync dialog must close after clicking Confirm"
            assert len(sync_fired) >= 1, \
                "POST /trigger-citizen-sync must be dispatched when Confirm is clicked"
            self.step.set_actual(
                f"Confirm clicked. Dialog closed. Sync POST fired: {len(sync_fired)} request(s)."
            )

        with self.step("Step 4: Sync #1 result — table shows ≥ 1 student account (F01-AC01)"):
            ea_page.page.wait_for_load_state("domcontentloaded")
            row_count_sync1 = ea_page.get_row_count()
            assert row_count_sync1 >= 1, \
                f"Table must contain ≥ 1 account after Sync #1. Got {row_count_sync1}."
            self.step.set_actual(
                f"Sync #1 complete. Table: {row_count_sync1} account(s) visible."
            )

        # ════════════════════════════════════════════════════════════════════════
        # PHASE 2: Data Classification Verification (Steps 5–10)
        # Delegated to e2e_phase2_helpers.py (Invariant 9)
        # ════════════════════════════════════════════════════════════════════════

        verify_eligible_student_active(self, ea_page, e2e_data)   # Steps 5–6
        verify_missing_parent_active(self, ea_page, e2e_data)      # Step 7
        verify_over_age_deactive(self, ea_page, e2e_data)          # Step 8
        verify_status_filters(self, ea_page, e2e_data)             # Steps 9–10

        with self.step("Step 11: Record baseline total count before Sync #2 (all statuses)"):
            status_vals = copy.deepcopy(e2e_data["status_filter_values"])
            ea_page.filter_by_status(status_vals["all"])
            total_before_sync2 = ea_page.get_row_count()
            assert total_before_sync2 >= 1, \
                "Baseline count must be ≥ 1 before triggering Sync #2"
            self.step.set_actual(
                f"Baseline captured: {total_before_sync2} total account(s) before Sync #2."
            )

        # ════════════════════════════════════════════════════════════════════════
        # PHASE 3: Re-Sync Idempotency — Sync #2 (Steps 12–14)
        # ════════════════════════════════════════════════════════════════════════

        with self.step("Step 12: Trigger Sync #2 — 'Manual sync' → Confirm"):
            sync_dlg2 = ea_page.trigger_manual_sync()
            assert sync_dlg2.is_visible(timeout=5000), \
                "Sync dialog must appear for Sync #2"
            sync_fired2: list = []
            self.page.on(
                "request",
                lambda req: sync_fired2.append(req.url)
                if "trigger-citizen-sync" in req.url and req.method == "POST"
                else None,
            )
            sync_dlg2.confirm()
            assert not sync_dlg2.is_visible(timeout=3000), \
                "Sync #2 dialog must close after Confirm"
            assert len(sync_fired2) >= 1, \
                "POST /trigger-citizen-sync must fire on Sync #2"
            ea_page.page.wait_for_load_state("domcontentloaded")
            self.step.set_actual(
                f"Sync #2 triggered. POST fired {len(sync_fired2)} time(s). Dialog closed."
            )

        with self.step("Step 13: IDEMPOTENCY — Sync #2 produces ZERO duplicate accounts (F01-BR05, AC12)"):
            total_after_sync2 = ea_page.get_row_count()
            assert total_after_sync2 == total_before_sync2, (
                f"IDEMPOTENCY FAILURE (F01-BR05 / F01-AC12): "
                f"Expected row count={total_before_sync2}, Got={total_after_sync2}. "
                f"Duplicates detected: {total_after_sync2 - total_before_sync2}."
            )
            self.step.set_actual(
                f"Idempotency OK: Before={total_before_sync2}, After={total_after_sync2}. "
                "Delta=0. Zero duplicate accounts. F01-BR05 + F01-AC12 VERIFIED."
            )

        with self.step("Step 14: Eligible student still Active after Sync #2 (balance preserved)"):
            eligible_final = copy.deepcopy(e2e_data["eligible_students"]["primary"])
            ea_page.search(eligible_final["nric"])
            final_row = ea_page.find_row_by_nric(eligible_final["nric"])
            assert final_row is not None, \
                f"Eligible student {eligible_final['nric']} must still exist after Sync #2"
            assert eligible_final["expected_status"].lower() in final_row.get("status", "").lower(), \
                (
                    f"Student {eligible_final['nric']} must remain "
                    f"'{eligible_final['expected_status']}' after Sync #2. "
                    f"Got: '{final_row.get('status')}'"
                )
            self.step.set_actual(
                f"Post-Sync #2: Isaac Teo ({eligible_final['nric']}) "
                f"status='{final_row.get('status')}'. State preserved. "
                "━━━ UAT-001 E2E Full Journey: ALL 3 PHASES PASSED ━━━"
            )
