"""User Story 1 - Bing search and access target website (VTV earliest video) test suite."""
import pytest
from playwright.sync_api import Page
from pages.bing_home_page import BingHomePage
from pages.bing_results_page import BingResultsPage
from pages.youtube_page import YouTubePage


@pytest.mark.search
def test_user_story_1_bing_search_and_access_target(page: Page, search_data, step):
    """
    User Story 1:
    - Step 1: Navigate to Bing homepage
    - Step 2: Search for Keyword 1 (Facebook) and verify results
    - Step 3: Search for Keyword 2 (YouTube) and verify results
    - Step 4: Access target website from Bing search results
    - Step 5: Perform defined page actions:
              + Search for VTV channel on YouTube
              + Open channel and navigate to Videos tab
              + Sort by Oldest (ngày sớm nhất)
              + Click to play the earliest video
              + Capture screenshot evidence to reports/execution_step5.png
    """
    # Arrange
    home_page = BingHomePage(page)
    results_page = BingResultsPage(page)
    term_facebook = search_data["search_terms"][0]
    term_youtube = search_data["search_terms"][1]
    channel_query = search_data.get("target_action", {}).get("channel_search", "VTV24")
    filter_mode = search_data.get("target_action", {}).get("filter_mode", "Latest")

    # Step 1: Navigate to bing.com
    with step("Step 1: Navigate to bing.com"):
        home_page.navigate()

    # Step 2: Search for {Keyword1} (Facebook) and verify results
    with step("Step 2: Search for {Keyword1} (Facebook) and verify results"):
        home_page.search(term_facebook["keyword"])
        fb_title = results_page.get_first_result_title()
        assert term_facebook["expected_title_fragment"] in fb_title.lower(), (
            f"Expected '{term_facebook['expected_title_fragment']}' in first result title: '{fb_title}'"
        )

    # Step 3: Search for {Keyword2} (YouTube) and verify results
    with step("Step 3: Search for {Keyword2} (YouTube) and verify results"):
        results_page.search_again(term_youtube["keyword"])
        yt_title = results_page.get_first_result_title()
        assert term_youtube["expected_title_fragment"] in yt_title.lower(), (
            f"Expected '{term_youtube['expected_title_fragment']}' in first result title: '{yt_title}'"
        )

    # Step 4: Access the target website (YouTube)
    with step("Step 4: Access the target website (YouTube)"):
        target_page = results_page.access_first_result()
        step.set_page(target_page)

    # Step 5: Perform defined page actions on VTV YouTube channel
    with step("Step 5: Perform defined page actions on VTV YouTube channel"):
        youtube_page = YouTubePage(target_page)
        assert youtube_page.is_loaded(), "Target YouTube page was not loaded successfully"

        # Search for VTV channel
        youtube_page.search(channel_query)

        # Open VTV channel from search results
        youtube_page.open_channel_from_results("VTV")

        # Select Videos tab
        youtube_page.select_videos_tab()

        # Sort videos and play target video
        if filter_mode.lower() == "oldest":
            youtube_page.sort_by_oldest()
            video_title = youtube_page.play_earliest_video()
        else:
            youtube_page.sort_by_latest()
            video_title = youtube_page.play_latest_video()

        assert "watch" in youtube_page.page.url, "Video playback page was not opened"

        # Capture execution screenshot evidence
        youtube_page.take_screenshot("reports/execution_step5.png")
        step.attach_screenshot("reports/execution_step5.png")
