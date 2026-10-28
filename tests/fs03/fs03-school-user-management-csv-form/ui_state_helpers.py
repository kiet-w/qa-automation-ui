"""
tests/fs03/fs03-school-user-management-csv-form/ui_state_helpers.py - Shared state-reading helpers
for TC-FS03-SUM assertions (tests-side only; contains no product logic and performs no UI access).
"""
import re
from typing import Any, Dict, List

_I18N_KEY_RE = re.compile(r"[a-z][a-z0-9_]*(?:\.[a-z0-9_]+)+")


def with_form_error(snapshot: Dict[str, Any]) -> Dict[str, Any]:
    """Ensure visible_errors['form'] always carries the joined visible feedback (field-level
    errors mapped by ErrorDiagnostics + alert/toast messages), so Exceptor.expect_rejection can
    adjudicate both inline-field and alert-level rejections through one stable field key."""
    errors = dict(snapshot.get("visible_errors") or {})
    alerts = [a for a in (snapshot.get("alerts") or []) if a]
    if "form" not in errors:
        joined = " | ".join([v for v in errors.values() if v] + alerts)
        if joined:
            errors["form"] = joined
    snapshot["visible_errors"] = errors
    return snapshot


def feedback_texts(snapshot: Dict[str, Any]) -> List[str]:
    """Return every visible feedback string (field errors + alerts/toasts), de-duplicated."""
    seen, out = set(), []
    for text in list((snapshot.get("visible_errors") or {}).values()) + list(
        snapshot.get("alerts") or []
    ):
        if text and text not in seen:
            seen.add(text)
            out.append(text)
    return out


def contains_fragment(snapshot: Dict[str, Any], fragment: str) -> bool:
    """True when any visible feedback contains the fragment (case-insensitive)."""
    return fragment.lower() in " | ".join(feedback_texts(snapshot)).lower()


def has_raw_i18n_key(snapshot: Dict[str, Any]) -> bool:
    """True when a feedback string is a bare dotted i18n key (e.g. validation.nric.invalid)."""
    return any(_I18N_KEY_RE.fullmatch(text.strip()) for text in feedback_texts(snapshot))


def submit_create(create: Any) -> Dict[str, Any]:
    """Click Create when enabled and return the Exceptor state snapshot (no assertions here)."""
    if create.is_create_button_disabled():
        return {"success_visible": False, "visible_errors": {}, "alerts": []}
    create.click_create()
    create.wait_for_condition(
        lambda: create.is_result_card_visible()
        or bool(create.get_toast_texts())
        or bool(create.get_alert_texts()),
        timeout=10000,
    )
    return with_form_error(create.get_state_snapshot())


def success_blob(create: Any, snapshot: Dict[str, Any]) -> str:
    """Join every visible success surface (field errors, alerts, toasts, result card)."""
    parts = feedback_texts(snapshot) + create.get_toast_texts() + [create.get_result_card_text()]
    return " ".join(p for p in parts if p).strip()


def server_5xx(monitor: Any) -> List[str]:
    """Return captured HTTP 5xx API failures recorded by a UIHealthMonitor."""
    return [e for e in getattr(monitor, "failed_api_requests", []) if e.strip().startswith("5")]


_PASSWORD_VALUE_RE = re.compile(r'"(?:password|passwd|pwd)"\s*:\s*"[^"]+"', re.IGNORECASE)


def has_stored_password_value(texts: Any) -> bool:
    """True when any captured API body carries a non-empty password field value."""
    for text in texts or []:
        if text and _PASSWORD_VALUE_RE.search(text):
            return True
    return False
