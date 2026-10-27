"""
reporting/core/sanitizer.py - High-Performance Error & Traceback Sanitization Engine.

Prevents report bloating, CSS dump leakage, and unreadable DOM assertions by:
1. Stripping raw embedded HTML DOM documents (<!doctype html...</html>).
2. Stripping raw CSS stylesheets (<style>...</style>, @font-face rules, minified bundles).
3. Stripping script injection code (<script>...</script>).
4. Providing clean, human-readable defect hints for executive summaries.
5. Slicing oversized tracebacks with clean truncation boundaries.
"""

import re
from typing import Optional


def clean_error_message(err_str: Optional[str], max_len: int = 3000) -> str:
    """
    Cleans and sanitizes error / assertion / traceback messages.
    Replaces massive HTML DOM dumps (e.g. from page.content()) and CSS stylesheet
    blocks with compact placeholders, preserving stack traces and assertion logic.
    """
    if not err_str:
        return ""

    s = str(err_str)

    # 1. Replace single- or double-quoted HTML documents (common in pytest assertion dumps)
    s = re.sub(
        r"[\'\"]<!doctype\s+html.*?</html>[\'\"]",
        "'[HTML Page DOM]'",
        s,
        flags=re.DOTALL | re.IGNORECASE,
    )
    s = re.sub(
        r"[\'\"]<html\b.*?</html>[\'\"]",
        "'[HTML Page DOM]'",
        s,
        flags=re.DOTALL | re.IGNORECASE,
    )

    # 2. Replace unquoted raw HTML documents
    s = re.sub(
        r"<!doctype\s+html.*?</html>",
        "[HTML Page DOM]",
        s,
        flags=re.DOTALL | re.IGNORECASE,
    )
    s = re.sub(
        r"<html\b.*?</html>",
        "[HTML Page DOM]",
        s,
        flags=re.DOTALL | re.IGNORECASE,
    )

    # 3. Strip large style / script / font blocks if any remain
    s = re.sub(r"<style\b.*?</style>", "[CSS Styles]", s, flags=re.DOTALL | re.IGNORECASE)
    s = re.sub(r"<script\b.*?</script>", "[Script Code]", s, flags=re.DOTALL | re.IGNORECASE)
    s = re.sub(r"@font-face\s*\{[^}]+\}", "[Font Definition]", s, flags=re.DOTALL)

    # 4. Truncate single lines longer than 600 chars (e.g. minified CSS or Base64 dumps)
    clean_lines = []
    for line in s.splitlines():
        if len(line) > 600:
            clean_lines.append(line[:600] + "... [line truncated]")
        else:
            clean_lines.append(line)
    s = "\n".join(clean_lines)

    # 5. Collapse excessive blank lines
    s = re.sub(r"\n{3,}", "\n\n", s)

    # 6. Global maximum length boundary
    if len(s) > max_len:
        s = s[:max_len].rstrip() + "\n... [Traceback truncated for readability]"

    return s.strip()


def extract_clean_defect_hint(err_str: Optional[str], max_len: int = 180) -> str:
    """
    Extracts a crisp, single-line, professional defect summary suitable for
    executive summary cards and takeaway bullet points.
    """
    if not err_str:
        return "Kỳ vọng giao diện không khớp với trạng thái thực tế."

    cleaned = clean_error_message(err_str, max_len=2000)

    # Priority 1: Check for explicit AssertionError or custom business rule message
    m_assert = re.search(r"AssertionError:\s*([^\n]+)", cleaned)
    if m_assert:
        hint = m_assert.group(1).strip()
    else:
        # Priority 2: Extract first informative line
        lines = [line.strip() for line in cleaned.splitlines() if line.strip()]
        hint = "Kỳ vọng giao diện không khớp với trạng thái thực tế."
        for line in lines:
            if line.startswith("assert ") or line.startswith("E "):
                hint = line.lstrip("E ").strip()
                break
            elif not line.startswith("Traceback") and not line.startswith("File "):
                hint = line
                break

    # Clean escaped newlines and collapse whitespace
    hint = hint.replace("\\\\n", " ").replace("\\n", " ")
    hint = re.sub(r"\s+", " ", hint).strip()
    hint = hint.strip("\'\" ")

    if len(hint) > max_len:
        hint = hint[: max_len - 3] + "..."

    return hint
