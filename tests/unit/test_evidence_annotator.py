"""
tests/unit/test_evidence_annotator.py - Unit tests for EvidenceAnnotator, Step Action, and Actual Result Highlighting.
"""
from pathlib import Path
from unittest.mock import MagicMock
from core.evidence_annotator import EvidenceAnnotator
from core.sketch_annotator import SketchAnnotator


def test_evidence_annotator_action_input_handles_none_page():
    # Must handle None page gracefully
    res = EvidenceAnnotator.highlight_action_input(None, "#input", "123456", "fill")
    assert res is False


def test_evidence_annotator_actual_result_handles_none_page():
    # Must handle None page gracefully
    res = EvidenceAnnotator.highlight_actual_result(None, None, "passed", "Success")
    assert res is False


def test_evidence_annotator_clear_handles_none_page():
    # Must not throw when page is None
    EvidenceAnnotator.clear_overlays(None)


def test_evidence_annotator_highlights_action_input_with_page():
    mock_page = MagicMock()
    mock_page.is_closed.return_value = False
    mock_locator = MagicMock()
    mock_locator.first = mock_locator
    mock_locator.is_visible.return_value = True

    res = EvidenceAnnotator.highlight_action_input(mock_page, mock_locator, value="91234567", action_type="fill")
    assert res is True
    assert mock_locator.evaluate.called


def test_evidence_annotator_highlights_actual_result_with_locator():
    mock_page = MagicMock()
    mock_page.is_closed.return_value = False
    mock_locator = MagicMock()
    mock_locator.first = mock_locator
    mock_locator.is_visible.return_value = True

    res = EvidenceAnnotator.highlight_actual_result(mock_page, mock_locator, status="passed", actual_text="Valid mobile")
    assert res is True
    assert mock_locator.evaluate.called


def test_evidence_annotator_highlights_actual_result_autodetect():
    mock_page = MagicMock()
    mock_page.is_closed.return_value = False
    mock_candidate = MagicMock()
    mock_candidate.first = mock_candidate
    mock_candidate.is_visible.return_value = True
    mock_candidate.inner_text.return_value = "Phone number is required"
    mock_page.locator.return_value = mock_candidate

    res = EvidenceAnnotator.highlight_actual_result(mock_page, None, status="defect")
    assert res is True
    assert mock_candidate.evaluate.called


def test_sketch_annotator_delegation_to_evidence_annotator():
    mock_page = MagicMock()
    mock_page.is_closed.return_value = False
    mock_locator = MagicMock()
    mock_locator.first = mock_locator
    mock_locator.is_visible.return_value = True

    res_action = SketchAnnotator.highlight_action_input(mock_page, mock_locator, "abc", "input")
    assert res_action is True

    res_actual = SketchAnnotator.highlight_actual_result(mock_page, mock_locator, "passed", "OK")
    assert res_actual is True
