"""
tests/fs03/fs03-school-directory/directory_helpers.py - Shared data builders and read-only helpers.
No assertions here (assertions live in test functions, Invariant 1 applies to POM only).
All inputs come from JSON fixtures; uniqueness is generated per test (Invariant 2 / Rule 03 anti-noise).
"""
import re
import uuid
from typing import Dict, List

RAW_I18N_KEY = re.compile(r"^\s*\{\{|__\w+__|^[a-z][a-z0-9]*(\.[a-z0-9_]+){1,}$")


def unique_code(data: Dict) -> str:
    """Isolated MOE code per test run, e.g. QA5173-<uuid8>."""
    return f"{data['unique_code_prefix']}{uuid.uuid4().hex[:8].upper()}"


def unique_name(data: Dict, label: str = "") -> str:
    """Isolated school name per test run."""
    suffix = uuid.uuid4().hex[:6]
    return f"{data['unique_name_prefix']} {label} {suffix}".strip()


def status_is(status_text: str, expected: str) -> bool:
    """Compare a badge status against 'active'/'inactive' without the substring trap (inactive contains active)."""
    normalized = (status_text or "").strip().lower()
    if expected.lower() == "inactive":
        return "inactive" in normalized
    return "active" in normalized and "inactive" not in normalized


def active_student_count(row: Dict[str, str]) -> int:
    """Parse the sourced 'Active students' column into an int (0 when unparsable)."""
    try:
        return int(re.sub(r"[^\d]", "", row.get("students", "")) or 0)
    except ValueError:
        return 0


def find_row(rows: List[Dict[str, str]], code: str) -> Dict[str, str]:
    """Return the row whose MOE code matches exactly, else an empty dict."""
    for row in rows:
        if row.get("code", "").strip() == code:
            return row
    return {}


def has_raw_i18n_key(texts: List[str]) -> bool:
    """True when any visible message still looks like an untranslated translation key."""
    return any(RAW_I18N_KEY.search(t.strip()) for t in texts if t and t.strip())


def has_stack_trace(text: str, markers: List[str]) -> bool:
    """True when a server error leaked raw stack-trace markers into the UI."""
    return any(marker in (text or "") for marker in markers)


def red_dominant(color: str) -> bool:
    """True when a computed CSS color is red-dominant (sourced 'viền đỏ' error styling, DOM-SCH §4.2)."""
    nums = re.findall(r"[\d.]+", color or "")
    if len(nums) < 3:
        return False
    r, g, b = (float(nums[0]), float(nums[1]), float(nums[2]))
    return r > 120 and r > g * 1.4 and r > b * 1.4


def has_error_styling(locator) -> bool:
    """True when the control currently carries red error styling (border/outline/shadow), DOM-SCH §4.2."""
    computed = locator.evaluate(
        "el => { const s = getComputedStyle(el);"
        " return [s.borderTopColor, s.borderLeftColor, s.outlineColor, s.boxShadow].join(' | '); }"
    )
    return any(red_dominant(part) for part in str(computed).split("|"))
