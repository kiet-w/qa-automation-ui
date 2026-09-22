"""
reporting/core - Core parsing, media processing, and HTML assembly components.
"""

from reporting.core.builder import ReportGenerator, assemble_html_document, build_test_cards_html
from reporting.core.media import file_to_base64_data_url, find_video_for_test, resolve_screenshot_path, slugify
from reporting.core.parser import load_report_json, process_report_data

__all__ = [
    "ReportGenerator",
    "assemble_html_document",
    "build_test_cards_html",
    "file_to_base64_data_url",
    "find_video_for_test",
    "resolve_screenshot_path",
    "slugify",
    "load_report_json",
    "process_report_data",
]
