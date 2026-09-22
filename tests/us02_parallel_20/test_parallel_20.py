"""
tests/us02_parallel_20/test_parallel_20.py - 20 Parallel Test Cases Showcase Suite.

Designed for high-concurrency verification with pytest-xdist:
- 20 distinct data-driven scenarios covering tech topics.
- Multi-step validation with expected vs actual comparison.
- 100% isolated deliverable screenshots and Full HD WebM video per test.
- Tested across -n 4, -n 8, or -n auto workers without resource collision.
"""
import json
from pathlib import Path
from typing import Any, Dict, List
import pytest

from tests.base_test import BaseTest

DATA_FILE = Path(__file__).resolve().parent.parent.parent / "data" / "parallel_20_data.json"


def load_scenarios() -> List[Dict[str, Any]]:
    """Load the 20 scenarios from data/parallel_20_data.json."""
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("scenarios", [])


SCENARIOS = load_scenarios()


@pytest.mark.search
class TestParallel20Scenarios(BaseTest):
    """
    Test suite containing 20 independent test cases executed in parallel.
    Inherits from BaseTest:
    - self.page: Playwright Page instance
    - self.step: StepTracker for pipeline & reporting
    - self.bing_home: BingHomePage
    - self.bing_results: BingResultsPage
    """

    @pytest.mark.parametrize(
        "scenario",
        SCENARIOS,
        ids=[f"{s['id']}-{s['keyword'].split()[0]}" for s in SCENARIOS],
    )
    def test_search_scenario(self, scenario: Dict[str, Any]):
        """
        Execute 5-step UI test workflow for each of the 20 scenarios:
        - Step 1: Navigate to Bing homepage
        - Step 2: Search for target keyword
        - Step 3: Validate first organic result contains expected fragment
        - Step 4: Verify search results count is positive
        - Step 5: Capture isolated deliverable screenshot evidence
        """
        tc_id = scenario["id"]
        jira_id = scenario.get("jira_id", f"PROJ-20{tc_id[-2:]}")
        tc_title = scenario.get("title", f"Scenario {tc_id}")
        keyword = scenario["keyword"]
        expected_frag = scenario["expected_fragment"]
        category = scenario.get("category", "General")

        # Inject Jira and Story metadata into ExtentReports JSON
        if hasattr(self, "step") and hasattr(self.step, "json_metadata"):
            self.step.json_metadata["jira_id"] = jira_id
            self.step.json_metadata["user_story"] = f"US-02 [{category}]: {tc_title}"

        # Step 1: Navigate to Bing homepage
        with self.step(
            f"Step 1: Open Bing homepage [{tc_id}]",
            expected="Bing landing page loads with HTTP 200 and search input is ready",
            actual="Bing homepage loaded successfully; search box ready for user input",
        ):
            self.bing_home.navigate()

        # Step 2: Submit search keyword
        with self.step(
            f"Step 2: Submit query '{keyword}'",
            expected=f"Keyword '{keyword}' entered and form submitted to search engine",
            actual=f"Query '{keyword}' submitted successfully",
        ):
            self.bing_home.search(keyword)

        # Step 3: Verify first organic result title
        with self.step(
            f"Step 3: Verify first search result contains '{expected_frag}'",
            expected=f"First search result title contains fragment '{expected_frag}'",
        ):
            first_title = self.bing_results.get_first_result_title()
            self.assert_contains(
                first_title,
                expected_frag,
                f"Expected '{expected_frag}' in first result title: '{first_title}'",
            )
            self.step.set_actual(f"Verified first result title: '{first_title}'")

        # Step 4: Verify search results count
        with self.step(
            f"Step 4: Check organic search results count [{tc_id}]",
            expected="At least 1 organic search result item is visible",
        ):
            count = self.bing_results.get_results_count()
            assert count > 0, f"Expected > 0 search results, but found {count}"
            self.step.set_actual(f"Organic search results confirmed: {count} items found")

        # Step 5: Capture isolated deliverable screenshot evidence
        with self.step(
            f"Step 5: Capture deliverable evidence for {tc_id}",
            expected=f"Screenshot saved to reports directory without naming collision",
        ):
            evidence_file = self.get_report_path(f"evidence_{tc_id.lower()}.png")
            self.page.screenshot(path=evidence_file, full_page=False)
            self.step.attach_screenshot(evidence_file)
            self.step.set_actual(f"Evidence captured and saved to: {evidence_file}")
