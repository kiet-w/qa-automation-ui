"""
tests/fs08/fs08-uat007-contact-update/test_atomic_mailing.py
UAT-007 Mailing Address validation matrix: TC-UAT007-47..73, R8-AC15, MSG-0001/0805.
Ultra-lean parameterized implementation powered by FieldMatrixEngine.
Strictly compliant with Invariant 1 (Zero assertions in POM) and Invariant 9 (< 200 lines).
"""
import json
from pathlib import Path
import pytest
from tests.base_test import BaseTest

CASE_FILE = Path(__file__).resolve().parents[3] / "data/fs08/uat007_coverage_cases.json"
CASES = [c["id"] for c in json.loads(CASE_FILE.read_text(encoding="utf-8")) if c["field"].startswith("mailing")]


@pytest.mark.p0
@pytest.mark.atomic
class TestAtomicMailing(BaseTest):
    """Data-driven test suite for UAT-007 Mailing Address validation matrix (27 test cases)."""

    @pytest.mark.parametrize("case_id", CASES, ids=CASES)
    def test_tc_uat007_mailing_matrix(self, fs08_data, uat007_case_runner, case_id):
        uat007_case_runner(self, fs08_data, case_id)
