"""
=============================================================================
EduFAMS Pytest Suite: Date Form Inputs, BVA & Persistence Lifecycle
Executes all 32 date scenarios (TC-DATE-001 to TC-DATE-032) within Pytest.
=============================================================================
"""

import json
import pytest
import sys
from pathlib import Path
from playwright.async_api import Page

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATE_TEST_DIR = PROJECT_ROOT / "automation-uat" / "date_testing"
sys.path.insert(0, str(DATE_TEST_DIR))

from run_master_date_suite import MasterDateSuiteRunner


@pytest.fixture(scope="module")
def date_runner():
    runner = MasterDateSuiteRunner(headed=False, slow_mo=0, hold=0)
    return runner


@pytest.mark.asyncio
async def test_date_groups_1_2_3_inputs_and_boundaries(page: Page, date_runner: MasterDateSuiteRunner):
    """Executes Groups 1, 2, 3: Formats, Leap Years, BVA, and Malformed Date Inputs."""
    await date_runner.authenticate_admin(page)
    try:
        from test_date_inputs_and_boundaries import run_date_input_bva_tests
        await run_date_input_bva_tests(date_runner, page)
    except ImportError:
        pytest.skip("test_date_inputs_and_boundaries module not yet ready")

    # Assert that no critical defects occurred
    defects = [r for r in date_runner.results if r["verdict"] == "DEFECT"]
    assert len(defects) == 0, f"Critical date input defects found: {defects}"


@pytest.mark.asyncio
async def test_date_groups_4_5_business_and_persistence(page: Page, date_runner: MasterDateSuiteRunner):
    """Executes Groups 4, 5: Business Date Ranges, Parity, Timezone & Persistence."""
    await date_runner.authenticate_admin(page)
    try:
        from test_date_business_and_persistence import run_date_business_persistence_tests
        await run_date_business_persistence_tests(date_runner, page)
    except ImportError:
        pytest.skip("test_date_business_and_persistence module not yet ready")

    defects = [r for r in date_runner.results if r["verdict"] == "DEFECT"]
    assert len(defects) == 0, f"Critical date business/persistence defects found: {defects}"
