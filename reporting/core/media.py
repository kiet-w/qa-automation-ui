"""
reporting/core/media.py - Video and Screenshot processing & Base64 encoding.

Encodes binary media assets (WebM videos, PNG screenshots) into Base64 data URLs
for generating 100% self-contained offline HTML reports.
"""

import base64
import re
from pathlib import Path
from typing import List, Optional


def file_to_base64_data_url(filepath: Path, mime_type: str) -> Optional[str]:
    """Reads a binary file and returns a Base64 data URL string."""
    if not filepath or not filepath.exists() or not filepath.is_file():
        return None
    try:
        with open(filepath, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
            return f"data:{mime_type};base64,{encoded}"
    except Exception as err:
        print(f"[Warning] Failed to encode file {filepath} to Base64: {err}")
        return None


def slugify(text: str) -> str:
    """Normalize test nodeids or titles for robust directory/file matching."""
    slug = re.sub(r"[^\w]+", "-", text.lower())
    return slug.strip("-")


def find_video_for_test(
    test_nodeid: str,
    test_results_dir: Path,
    all_videos: List[Path],
    test_index: int,
    total_tests: int,
    test_metadata: Optional[dict] = None,
) -> Optional[Path]:
    """
    Matches a test case to its corresponding .webm video recording in test-results/.
    Uses multiple strategies:
    0. Direct metadata match: check test_metadata['video_path'] directly (stored by conftest/fixture).
    1. Directory name contains slugified test function name.
    2. Directory name contains slugified nodeid fragments.
    3. Direct single-test 1:1 mapping fallback.
    4. Index-based pairing if counts match.
    """
    # 0. Check direct video_path in test_metadata (stored by conftest)
    if test_metadata and isinstance(test_metadata, dict):
        raw_video_path = test_metadata.get("video_path")
        if raw_video_path:
            p = Path(raw_video_path)
            if p.exists() and p.is_file():
                return p.resolve()
            # Also check relative to test_results_dir or test_results_dir.parent
            if test_results_dir:
                cand1 = test_results_dir / p.name
                if cand1.exists() and cand1.is_file():
                    return cand1.resolve()
                cand2 = test_results_dir / p
                if cand2.exists() and cand2.is_file():
                    return cand2.resolve()
                if test_results_dir.exists():
                    for sub_v in test_results_dir.glob(f"**/{p.name}"):
                        if sub_v.exists() and sub_v.is_file():
                            return sub_v.resolve()

    if not all_videos:
        return None

    test_func_name = test_nodeid.split("::")[-1] if "::" in test_nodeid else test_nodeid
    slug_func = slugify(test_func_name)
    slug_node = slugify(test_nodeid)

    # Heuristic 1: directory matching test function name
    for video in all_videos:
        parent_name = video.parent.name.lower()
        if slug_func in parent_name or parent_name in slug_func:
            return video

    # Heuristic 2: directory matching nodeid fragments
    for video in all_videos:
        parent_name = video.parent.name.lower()
        parts = [p for p in slug_node.split("-") if len(p) > 3]
        match_count = sum(1 for p in parts if p in parent_name)
        if match_count >= max(2, len(parts) // 2):
            return video

    # Heuristic 3: If only one test and videos exist, pair the first video
    if total_tests == 1 and all_videos:
        return all_videos[0]

    # Heuristic 4: Index-based mapping if counts match
    if test_index < len(all_videos):
        return all_videos[test_index]

    return None


def resolve_screenshot_path(
    screenshot_path: Optional[str],
    reports_dir: Path,
    workspace_dir: Path,
    step_title: str = "",
    test_name: str = "",
) -> Optional[Path]:
    """
    Locates screenshot on disk using multiple fallback resolution strategies.
    Supports relative paths, absolute paths, reports/ subdirectories, test-specific slugs, and Step 5 convention.
    """
    candidates: List[Path] = []

    if screenshot_path:
        p = Path(screenshot_path)
        candidates.extend([
            p,
            reports_dir / "screenshots" / p.name,
            reports_dir / p,
            reports_dir / p.name,
            workspace_dir / p,
            workspace_dir / "reports" / "screenshots" / p.name,
        ])

    # Fallback with test_name slug if provided
    if test_name:
        slug = slugify(test_name)
        candidates.extend([
            reports_dir / "screenshots" / f"execution_step5_{slug}.png",
            reports_dir / f"execution_step5_{slug}.png",
            workspace_dir / "reports" / "screenshots" / f"execution_step5_{slug}.png",
            workspace_dir / "reports" / f"execution_step5_{slug}.png",
        ])

    # Fallback convention for Step 5 / target action screenshot evidence
    if "step 5" in step_title.lower() or "defined page actions" in step_title.lower():
        candidates.extend([
            reports_dir / "screenshots" / "execution_step5.png",
            reports_dir / f"execution_step5.png",
            workspace_dir / "reports" / "screenshots" / "execution_step5.png",
            workspace_dir / "reports" / "execution_step5.png",
        ])

    for cand in candidates:
        if cand.exists() and cand.is_file():
            return cand.resolve()

    return None
