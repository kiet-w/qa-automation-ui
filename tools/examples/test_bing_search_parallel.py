"""
User Story 1 - Parallel Data-Driven Testing (DDT) Test Suite.
Executes Bing search and YouTube channel actions across multiple scenarios concurrently.
"""
import json
from pathlib import Path
from typing import Any, Dict, List
import pytest

from tests.base_test import BaseTest

DATA_FILE = Path(__file__).resolve().parent.parent.parent / "data" / "search_data.json"


def load_parallel_scenarios() -> List[Dict[str, Any]]:
    """Load parallel test scenarios from search_data.json."""
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("parallel_scenarios", [])


SCENARIOS = load_parallel_scenarios()


@pytest.mark.search
class TestBingSearchParallel(BaseTest):
    """
    User Story 1 Parallel Data-Driven Testing Suite.
    Inherits from BaseTest (self.page, self.step, self.bing_home, self.bing_results, self.youtube).
    """

    @pytest.mark.parametrize(
        "scenario",
        SCENARIOS,
        ids=[s.get("scenario_id", f"SC_{idx+1}") for idx, s in enumerate(SCENARIOS)],
    )
    def test_user_story_1_parallel_scenario(self, scenario: Dict[str, Any]):
        """
        Execute User Story 1 workflow for a given data-driven scenario:
        - Step 1: Navigate to bing.com
        - Step 2: Search for Keyword 1 and verify first organic result title
        - Step 3: Search for Keyword 2 and verify first organic result title
        - Step 4: Access target website (YouTube)
        - Step 5: Perform defined actions on YouTube channel (search, Videos tab, sort by filter_mode, play video, capture evidence).
        """
        # Metadata configuration for HTML reporting engine
        jira_id = scenario.get("jira_id") or scenario.get("scenario_id", "PROJ-1042")
        user_story_title = scenario.get("title", f"User Story 1 - Scenario {scenario.get('scenario_id')}")

        if hasattr(self, "step") and hasattr(self.step, "json_metadata"):
            self.step.json_metadata["jira_id"] = jira_id
            self.step.json_metadata["user_story"] = user_story_title

        term_1 = scenario["term_1"]
        term_2 = scenario["term_2"]
        expected_frag_1 = scenario.get("expected_fragment_1", term_1)
        expected_frag_2 = scenario.get("expected_fragment_2", term_2)
        channel_name = scenario.get("channel", "VTV24")
        filter_mode = scenario.get("filter_mode", "Latest")
        evidence_name = scenario.get("evidence_name", f"execution_step5_{scenario.get('scenario_id', 'unknown')}.png")

        # Step 1: Navigate to bing.com
        with self.step(
            "Step 1: Navigate to bing.com",
            expected="Bing search engine landing page loads with HTTP 200 and search input ready",
            actual="Bing homepage loaded; search input ready for user interaction",
        ):
            self.bing_home.navigate()

        # Step 2: Search for Keyword 1 and verify first organic result title
        with self.step(
            f"Step 2: Search for {term_1} and verify results",
            expected=f"Keyword 1 ({term_1}) submitted; first organic result contains expected title fragment '{expected_frag_1}'",
        ):
            self.bing_home.search(term_1)
            first_title_1 = self.bing_results.get_first_result_title()
            self.assert_contains(
                first_title_1,
                expected_frag_1,
                f"Expected '{expected_frag_1}' in first result title: '{first_title_1}'",
            )
            self.step.set_actual(f"Search executed; first result title verified: '{first_title_1}'")

        # Step 3: Search for Keyword 2 and verify first organic result title
        with self.step(
            f"Step 3: Search for {term_2} and verify results",
            expected=f"Keyword 2 ({term_2}) submitted; first organic result contains expected title fragment '{expected_frag_2}'",
        ):
            self.bing_results.search_again(term_2)
            first_title_2 = self.bing_results.get_first_result_title()
            self.assert_contains(
                first_title_2,
                expected_frag_2,
                f"Expected '{expected_frag_2}' in first result title: '{first_title_2}'",
            )
            self.step.set_actual(f"Search executed; first result title verified: '{first_title_2}'")

        # Step 4: Access target website (YouTube)
        with self.step(
            "Step 4: Access the target website (YouTube)",
            expected="Target website accessed from search result and switched to target page context",
            actual="Target YouTube page context opened and document ready",
        ):
            target_page = self.bing_results.access_first_result()
            self.step.set_page(target_page)
            # Rebind YouTubePage to the active target page
            self.youtube = self.youtube.__class__(target_page)

        # Step 5: Perform defined actions on YouTube channel
        with self.step(
            f"Step 5: Perform defined actions on {channel_name} YouTube channel ({filter_mode})",
            expected=f"Channel {channel_name} opened, Videos tab selected, sorted by {filter_mode}, video played, and screenshot captured",
        ):
            assert self.youtube.is_loaded(), "Target YouTube page was not loaded successfully"

            # Search for channel
            self.youtube.search(channel_name)

            # Open channel from search results
            self.youtube.open_channel_from_results(channel_name)

            # Select Videos tab
            self.youtube.select_videos_tab()

            # Sort videos and play target video
            if filter_mode.lower() == "oldest":
                self.youtube.sort_by_oldest()
                video_title = self.youtube.play_earliest_video()
            else:
                self.youtube.sort_by_latest()
                video_title = self.youtube.play_latest_video()

            # 3-Layer Strict Assertion (Zero Hallucination)
            # Layer 1: Video title must be genuinely extracted from the sorted channel grid
            assert video_title and len(video_title.strip()) > 0, (
                "Verification Failure (Layer 1): Video title is empty. Grid failed to load or sorting failed."
            )

            # Layer 2: Current browser URL must strictly contain video playback path
            current_url = self.youtube.page.url
            assert "/watch" in current_url, (
                f"Verification Failure (Layer 2): Expected video playback URL with '/watch', got: '{current_url}'"
            )

            # Layer 3: HTML5 main video element must be present in the player DOM
            player_loc = self.youtube.page.locator("video.html5-main-video, video").first
            assert player_loc.count() > 0, (
                "Verification Failure (Layer 3): HTML5 video player element not found on playback page"
            )

            # Capture execution screenshot evidence into the ticket's isolated reports directory
            evidence_path = self.get_report_path(evidence_name, test_scoped=True)
            self.youtube.take_screenshot(evidence_path)
            self.step.attach_screenshot(evidence_path)
            self.step.set_actual(
                f"Target video playback confirmed ('{video_title}'); evidence screenshot saved to {evidence_path}"
            )
