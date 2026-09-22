"""
reporting/core/builder.py - Facade module re-exporting reporting components.

Modularized for maintainability and token efficiency:
- generator.py: ReportGenerator class
- document.py: assemble_html_document
- views_dashboard.py: build_extent_dashboard_html
- views_tests.py: build_extent_tests_html, build_test_cards_html
"""

from reporting.core.document import assemble_html_document
from reporting.core.generator import ReportGenerator
from reporting.core.views_dashboard import build_extent_dashboard_html
from reporting.core.views_tests import build_extent_tests_html, build_test_cards_html

__all__ = [
    "ReportGenerator",
    "assemble_html_document",
    "build_extent_dashboard_html",
    "build_extent_tests_html",
    "build_test_cards_html",
]
