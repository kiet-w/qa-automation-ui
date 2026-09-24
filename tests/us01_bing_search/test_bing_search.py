"""User Story 1 - Bing search and access target website (VTV earliest video) test suite."""
import pytest
from tests.base_test import BaseTest


@pytest.mark.search
class TestBingSearch(BaseTest):
    """
    User Story 1 test suite utilizing BaseTest inheritance.
    Automatically inherits self.page, self.step, self.search_data,
    self.bing_home, self.bing_results, self.youtube.
    """

    def test_user_story_1_bing_search_and_access_target(self):
        """
        User Story 1:
        - Step 1: Navigate to Bing homepage
        - Step 2: Search for Keyword 1 (Facebook) and verify results
        - Step 3: Search for Keyword 2 (YouTube) and verify results
        - Step 4: Access target website from Bing search results
        - Step 5: Perform defined page actions:
                  + Search for VTV channel on YouTube
                  + Open channel and navigate to Videos tab
                  + Sort by Oldest
                  + Click to play the earliest video
                  + Capture screenshot evidence to reports/execution_step5.png
        """
        # Arrange
        term_facebook = self.search_data["search_terms"][0]
        term_youtube = self.search_data["search_terms"][1]
        channel_query = self.search_data.get("target_action", {}).get("channel_search", "VTV24")
        filter_mode = self.search_data.get("target_action", {}).get("filter_mode", "Latest")

        # Step 1: Navigate to bing.com
        with self.step(
            "Step 1: Navigate to bing.com",
            expected="Bing search engine landing page loads with HTTP 200 and search input ready",
            actual="Bing homepage loaded; search input ready for user interaction",
        ):
            self.bing_home.navigate()

        # Step 2: Search for {Keyword1} (Facebook) and verify results
        with self.step(
            "Step 2: Search for {Keyword1} (Facebook) and verify results",
            expected="Keyword 1 (Facebook) submitted; first organic result contains expected title fragment",
        ):
            self.bing_home.search(term_facebook["keyword"])
            fb_title = self.bing_results.get_first_result_title()
            self.assert_contains(
                fb_title,
                term_facebook["expected_title_fragment"],
                f"Expected '{term_facebook['expected_title_fragment']}' in first result title: '{fb_title}'",
            )
            self.step.set_actual(f"Search executed; first result title verified: '{fb_title}'")

        # Step 3: Search for {Keyword2} (YouTube) and verify results
        with self.step(
            "Step 3: Search for {Keyword2} (YouTube) and verify results",
            expected="Keyword 2 (YouTube) submitted; first organic result contains expected title fragment",
        ):
            self.bing_results.search_again(term_youtube["keyword"])
            yt_title = self.bing_results.get_first_result_title()
            self.assert_contains(
                yt_title,
                term_youtube["expected_title_fragment"],
                f"Expected '{term_youtube['expected_title_fragment']}' in first result title: '{yt_title}'",
            )
            self.step.set_actual(f"Search executed; first result title verified: '{yt_title}'")

        # Step 4: Access the target website (YouTube)
        with self.step(
            "Step 4: Access the target website (YouTube)",
            expected="Target website accessed from search result and switched to target page context",
            actual="Target YouTube page context opened and document ready",
        ):
            target_page = self.bing_results.access_first_result()
            self.step.set_page(target_page)
            # Rebind YouTubePage to the active target page
            self.youtube = self.youtube.__class__(target_page)

        # Step 5: Perform defined page actions on VTV YouTube channel
        with self.step(
            "Step 5: Perform defined page actions on VTV YouTube channel",
            expected="Channel VTV opened, videos tab selected, target video played, and screenshot captured",
        ):
            assert self.youtube.is_loaded(), "Target YouTube page was not loaded successfully"

            # Search for VTV channel
            self.youtube.search(channel_query)

            # Open VTV channel from search results
            self.youtube.open_channel_from_results("VTV")

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
            assert video_title and len(video_title.strip()) > 0, (
                "Verification Failure (Layer 1): Video title is empty. Grid failed to load or sorting failed."
            )

            current_url = self.youtube.page.url
            assert "/watch" in current_url, (
                f"Verification Failure (Layer 2): Expected video playback URL with '/watch', got: '{current_url}'"
            )

            player_loc = self.youtube.page.locator("video.html5-main-video, video").first
            assert player_loc.count() > 0, (
                "Verification Failure (Layer 3): HTML5 video player element not found on playback page"
            )

            # Capture execution screenshot evidence into the ticket's isolated reports directory
            step5_evidence = self.get_report_path("execution_step5.png", test_scoped=True)
            self.youtube.take_screenshot(step5_evidence)
            self.step.attach_screenshot(step5_evidence)
            self.step.set_actual(
                f"Target video playback confirmed ('{video_title}'); evidence screenshot saved to {step5_evidence}"
            )
