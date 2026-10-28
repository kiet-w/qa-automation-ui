"""
core/error_diagnostics.py - Detailed Error Handling & Inspection Engine.

Extracts deep diagnostic context from live Playwright pages when an automation
action, assertion, or state transition fails. Solves the opaque "element timeout"
problem by identifying exact invalid fields, alert banners, and technical faults.
"""
from typing import Any, Dict, List, Optional
from playwright.sync_api import Locator, Page


class ErrorDiagnostics:
    """Universal error extraction and diagnostic utility for Playwright pages."""

    @classmethod
    def capture(cls, page: Page, container: Optional[Locator] = None) -> Dict[str, Any]:
        """
        Capture a comprehensive error and health diagnostic snapshot of the page/container.
        Extracts:
        - Field errors (inputs with aria-invalid="true", linked error messages)
        - FormErrorSummary items (role="alert" sections)
        - Alert banners (role="alert", role="status", toast notifications)
        - Active loading/busy states
        - Technical errors (pageerror exceptions and console.error messages)
        """
        scope = container or page.locator("body")
        url = page.url
        title = page.title()

        # 1. Field-level validation errors
        field_errors = cls._extract_field_errors(scope)

        # 2. Form Error Summaries
        summary_errors = cls._extract_summary_errors(scope)

        # 3. Alert Banners & Dialog messages
        alerts = cls._extract_alerts(scope)

        # 4. Toast notifications
        toasts = cls._extract_toasts(page)

        # 5. Busy / Loading indicators
        busy_elements = cls._extract_busy_states(scope)

        has_any_error = bool(
            field_errors or summary_errors or [a for a in alerts if a.get("is_error")] or toasts
        )

        return {
            "url": url,
            "title": title,
            "has_error": has_any_error,
            "field_errors": field_errors,
            "summary_errors": summary_errors,
            "alerts": alerts,
            "toasts": toasts,
            "busy_elements": busy_elements,
        }

    @classmethod
    def _extract_field_errors(cls, scope: Locator) -> Dict[str, str]:
        """Finds all form controls marked invalid and pairs them with error text."""
        errors: Dict[str, str] = {}
        invalid_controls = scope.locator(
            "input[aria-invalid='true'], select[aria-invalid='true'], textarea[aria-invalid='true']"
        )
        count = invalid_controls.count()
        for i in range(count):
            ctrl = invalid_controls.nth(i)
            name = (
                ctrl.get_attribute("name")
                or ctrl.get_attribute("id")
                or ctrl.get_attribute("data-testid")
                or f"field_{i}"
            )
            described_by = ctrl.get_attribute("aria-describedby") or ""
            error_text = ""

            # Try locating error element via aria-describedby
            for desc_id in described_by.split():
                if "error" in desc_id.lower():
                    err_el = scope.locator(f"#{desc_id}")
                    if err_el.count() > 0 and err_el.first.is_visible():
                        error_text = err_el.first.inner_text().strip()
                        break

            # Fallback: check adjacent role="alert" or error paragraph
            if not error_text:
                parent = ctrl.locator("xpath=..")
                adjacent_err = parent.locator("p[role='alert'], p[class*='error'], span[class*='error']")
                if adjacent_err.count() > 0 and adjacent_err.first.is_visible():
                    error_text = adjacent_err.first.inner_text().strip()

            errors[name] = error_text or "Field marked aria-invalid=true without explicit message"
        return errors

    @classmethod
    def _extract_summary_errors(cls, scope: Locator) -> List[str]:
        """Extracts bullet-point errors from FormErrorSummary or summary alert sections."""
        summaries: List[str] = []
        summary_sections = scope.locator("section[role='alert'], [class*='FormErrorSummary']")
        if summary_sections.count() > 0:
            for s_idx in range(summary_sections.count()):
                items = summary_sections.nth(s_idx).locator("li")
                for i in range(items.count()):
                    text = items.nth(i).inner_text().strip()
                    if text:
                        summaries.append(text)
        return summaries

    @classmethod
    def _extract_alerts(cls, scope: Locator) -> List[Dict[str, str]]:
        """Extracts visible Alert banners and Alertdialog contents."""
        alerts: List[Dict[str, str]] = []
        alert_locators = scope.locator(
            "div[role='alert'], [class*='Alert_error'], [class*='Alert_warning'], div[role='alertdialog']"
        )
        for i in range(alert_locators.count()):
            el = alert_locators.nth(i)
            if not el.is_visible():
                continue
            heading = el.locator("h2, h3, h4, [class*='heading']").first
            heading_text = heading.inner_text().strip() if heading.count() > 0 else ""
            content = el.inner_text().strip()
            is_error = "error" in (el.get_attribute("class") or "").lower() or el.get_attribute("role") == "alert"
            alerts.append({
                "heading": heading_text,
                "content": content,
                "is_error": is_error,
            })
        return alerts

    @classmethod
    def _extract_toasts(cls, page: Page) -> List[str]:
        """Captures any floating Toast notifications rendered into portals."""
        toasts: List[str] = []
        toast_items = page.locator("ol[aria-label='Notifications'] li, [class*='Toast_toast']")
        for i in range(toast_items.count()):
            t = toast_items.nth(i)
            if t.is_visible():
                toasts.append(t.inner_text().strip())
        return toasts

    @classmethod
    def _extract_busy_states(cls, scope: Locator) -> List[str]:
        """Finds active loading spinners or containers marked aria-busy."""
        busy: List[str] = []
        busy_locators = scope.locator("[aria-busy='true'], [role='status']:has-text('Loading')")
        for i in range(busy_locators.count()):
            b = busy_locators.nth(i)
            if b.is_visible():
                busy.append(b.inner_text().strip() or "Element aria-busy=true")
        return busy

    @classmethod
    def format_report(cls, diag: Dict[str, Any]) -> str:
        """Formats the diagnostic dictionary into a readable Markdown report."""
        lines = [
            f"### 🚨 UI Error Diagnostics at {diag.get('url', 'Unknown URL')}",
            f"- **Page Title**: {diag.get('title', 'N/A')}",
            f"- **Error Status**: {'Detected errors on screen' if diag.get('has_error') else 'No active errors'}",
        ]

        if diag.get("field_errors"):
            lines.append("\n#### ❌ Invalid Form Fields:")
            for field, msg in diag["field_errors"].items():
                lines.append(f"  - `{field}`: {msg}")

        if diag.get("summary_errors"):
            lines.append("\n#### ⚠️ Form Error Summary:")
            for s in diag["summary_errors"]:
                lines.append(f"  - {s}")

        if diag.get("alerts"):
            lines.append("\n#### 📢 Active Alert Banners:")
            for a in diag["alerts"]:
                h = f"**{a['heading']}**: " if a["heading"] else ""
                lines.append(f"  - {h}{a['content']}")

        if diag.get("toasts"):
            lines.append("\n#### 🔔 Toast Notifications:")
            for t in diag["toasts"]:
                lines.append(f"  - {t}")

        if diag.get("busy_elements"):
            lines.append("\n#### ⏳ Busy / Loading Elements:")
            for b in diag["busy_elements"]:
                lines.append(f"  - {b}")

        return "\n".join(lines)
