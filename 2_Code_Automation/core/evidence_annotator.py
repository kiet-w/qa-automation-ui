"""
core/evidence_annotator.py - Precision Visual Evidence Highlighting Engine.

Provides non-destructive SVG & DOM visual overlays for:
1. Input / Action Steps: Crisp blue/orange framing with smart badge (e.g. Input: "91234567" or Click: [Button]).
2. Actual Result: Prominent green (Pass) or red (Defect/Validation) framing with smart badge (e.g. Actual Result: ...).
3. Auto-detection of on-screen validation messages, alerts, and badges when no explicit locator is specified.
"""

from typing import Optional, Union, Dict, Any
from playwright.sync_api import Locator, Page


class EvidenceAnnotator:
    """Injects high-contrast action and actual result visual highlights into the browser DOM."""

    @staticmethod
    def highlight_action_input(
        page: Optional[Page],
        locator_or_selector: Union[str, Locator],
        value: str = "",
        action_type: str = "input",
    ) -> bool:
        """
        Highlights an input or interactive element with a bright blue/orange reticle and action badge.
        Returns True if element was successfully highlighted.
        """
        if not page or page.is_closed():
            return False
        try:
            loc = locator_or_selector
            if isinstance(loc, str):
                loc = page.locator(loc)
            target = loc.first if hasattr(loc, "first") else loc
            if not target.is_visible(timeout=800):
                return False

            clean_val = str(value).strip()
            if len(clean_val) > 40:
                clean_val = clean_val[:37] + "..."

            is_input = action_type in ("fill", "type", "input", "select")
            border_color = "#2563eb" if is_input else "#f97316"
            badge_bg = (
                "linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%)"
                if is_input
                else "linear-gradient(135deg, #ea580c 0%, #c2410c 100%)"
            )
            action_icon = "✏️" if is_input else "👆"
            label_text = f'{action_icon} {action_type.upper()}: "{clean_val}"' if clean_val else f"{action_icon} {action_type.upper()}"

            data = {
                "border_color": border_color,
                "badge_bg": badge_bg,
                "label_text": label_text,
            }

            target.evaluate(
                r"""(el, data) => {
                const old = document.getElementById('__qa_evidence_action_overlay__');
                if (old) old.remove();

                const rect = el.getBoundingClientRect();
                const overlay = document.createElement('div');
                overlay.id = '__qa_evidence_action_overlay__';
                overlay.style.position = 'absolute';
                overlay.style.pointerEvents = 'none';
                overlay.style.userSelect = 'none';
                overlay.style.zIndex = '2147483644';
                overlay.style.top = (window.scrollY + rect.top) + 'px';
                overlay.style.left = (window.scrollX + rect.left) + 'px';
                overlay.style.width = rect.width + 'px';
                overlay.style.height = rect.height + 'px';

                const isNearTop = (rect.top < 38);
                const pillPos = isNearTop
                    ? 'top: calc(100% + 5px); bottom: auto;'
                    : 'bottom: calc(100% + 5px); top: auto;';

                overlay.innerHTML = `
                    <div style="
                        position: absolute;
                        inset: -3px;
                        border: 3px solid ${data.border_color};
                        border-radius: 6px;
                        box-shadow: 0 0 12px ${data.border_color}88, inset 0 0 6px ${data.border_color}44;
                        box-sizing: border-box;
                    "></div>
                    <div style="
                        position: absolute;
                        ${pillPos}
                        left: 0;
                        background: ${data.badge_bg};
                        border: 1.5px solid rgba(255, 255, 255, 0.7);
                        color: #ffffff;
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                        font-size: 11px;
                        font-weight: 700;
                        padding: 3px 9px;
                        border-radius: 5px;
                        white-space: nowrap;
                        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.45);
                    ">${data.label_text}</div>
                `;
                document.body.appendChild(overlay);
            }""",
                data,
            )
            return True
        except Exception:
            return False

    @staticmethod
    def highlight_actual_result(
        page: Optional[Page],
        locator_or_selector: Optional[Union[str, Locator]] = None,
        status: str = "passed",
        actual_text: Optional[str] = None,
    ) -> bool:
        """
        Highlights the Actual Result element with a vivid green (Passed) or red (Defect/Validation)
        border and an 'Actual Result' smart badge.
        If locator is None, automatically searches the DOM for visible alerts/errors/toasts.
        """
        if not page or page.is_closed():
            return False
        try:
            target_el = None
            if locator_or_selector is not None:
                loc = locator_or_selector
                if isinstance(loc, str):
                    loc = page.locator(loc)
                target = loc.first if hasattr(loc, "first") else loc
                if target.is_visible(timeout=800):
                    target_el = target

            # Auto-detect result elements if no explicit locator provided
            if target_el is None:
                candidate_selectors = [
                    '[role="alert"]:visible',
                    '[aria-invalid="true"]:visible',
                    '.text-danger:visible',
                    '.error-message:visible',
                    '[data-testid*="error"]:visible',
                    '[class*="error"]:visible',
                    '[class*="alert"]:visible',
                    '[class*="toast"]:visible',
                    '[class*="badge"]:visible',
                    'form:visible',
                ]
                for sel in candidate_selectors:
                    try:
                        cand = page.locator(sel).first
                        if cand.is_visible(timeout=300):
                            target_el = cand
                            break
                    except Exception:
                        continue

            is_pass = status.lower() in ("passed", "pass", "ok")
            border_color = "#10b981" if is_pass else "#ef4444"
            badge_bg = (
                "linear-gradient(135deg, #059669 0%, #047857 100%)"
                if is_pass
                else "linear-gradient(135deg, #dc2626 0%, #b91c1c 100%)"
            )
            icon = "✅" if is_pass else "⚠️"
            title = "ACTUAL RESULT (PASS)" if is_pass else "ACTUAL RESULT (DEFECT/ERROR)"

            clean_text = (actual_text or "").strip()
            if not clean_text and target_el:
                try:
                    dom_text = (target_el.inner_text() or "").strip()
                    if dom_text:
                        clean_text = dom_text[:50]
                except Exception:
                    pass

            if clean_text:
                if len(clean_text) > 45:
                    clean_text = clean_text[:42] + "..."
                badge_title = f'{icon} {title}: "{clean_text}"'
            else:
                badge_title = f"{icon} {title}"

            data = {
                "border_color": border_color,
                "badge_bg": badge_bg,
                "badge_title": badge_title,
            }

            if target_el:
                target_el.evaluate(
                    r"""(el, data) => {
                    const old = document.getElementById('__qa_evidence_actual_overlay__');
                    if (old) old.remove();

                    const rect = el.getBoundingClientRect();
                    const overlay = document.createElement('div');
                    overlay.id = '__qa_evidence_actual_overlay__';
                    overlay.style.position = 'absolute';
                    overlay.style.pointerEvents = 'none';
                    overlay.style.userSelect = 'none';
                    overlay.style.zIndex = '2147483644';
                    overlay.style.top = (window.scrollY + rect.top) + 'px';
                    overlay.style.left = (window.scrollX + rect.left) + 'px';
                    overlay.style.width = rect.width + 'px';
                    overlay.style.height = rect.height + 'px';

                    const isNearTop = (rect.top < 40);
                    const pillPos = isNearTop
                        ? 'top: calc(100% + 6px); bottom: auto;'
                        : 'bottom: calc(100% + 6px); top: auto;';

                    overlay.innerHTML = `
                        <div style="
                            position: absolute;
                            inset: -4px;
                            border: 3.5px solid ${data.border_color};
                            border-radius: 8px;
                            box-shadow: 0 0 16px ${data.border_color}99, inset 0 0 8px ${data.border_color}55;
                            box-sizing: border-box;
                        "></div>
                        <div style="
                            position: absolute;
                            ${pillPos}
                            left: 0;
                            background: ${data.badge_bg};
                            border: 2px solid rgba(255, 255, 255, 0.85);
                            color: #ffffff;
                            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                            font-size: 12px;
                            font-weight: 800;
                            padding: 4px 12px;
                            border-radius: 6px;
                            white-space: nowrap;
                            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.5);
                        ">${data.badge_title}</div>
                    `;
                    document.body.appendChild(overlay);
                }""",
                    data,
                )
                return True
            else:
                # Full-page banner if no single element matches
                page.evaluate(
                    r"""(data) => {
                    const old = document.getElementById('__qa_evidence_actual_overlay__');
                    if (old) old.remove();

                    const banner = document.createElement('div');
                    banner.id = '__qa_evidence_actual_overlay__';
                    banner.style.position = 'fixed';
                    banner.style.bottom = '24px';
                    banner.style.left = '50%';
                    banner.style.transform = 'translateX(-50%)';
                    banner.style.zIndex = '2147483644';
                    banner.style.pointerEvents = 'none';
                    banner.style.background = data.badge_bg;
                    banner.style.border = '2px solid rgba(255, 255, 255, 0.85)';
                    banner.style.color = '#ffffff';
                    banner.style.fontFamily = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif';
                    banner.style.fontSize = '13px';
                    banner.style.fontWeight = '800';
                    banner.style.padding = '8px 20px';
                    banner.style.borderRadius = '8px';
                    banner.style.boxShadow = '0 6px 20px rgba(0,0,0,0.5)';
                    banner.textContent = data.badge_title;
                    document.body.appendChild(banner);
                }""",
                    data,
                )
                return True
        except Exception:
            return False

    @staticmethod
    def clear_overlays(page: Optional[Page]) -> None:
        """Removes all action and actual result visual overlays from the page."""
        if not page or page.is_closed():
            return
        try:
            page.evaluate(
                r"""(() => {
                ['__qa_evidence_action_overlay__', '__qa_evidence_actual_overlay__'].forEach(id => {
                    const el = document.getElementById(id);
                    if (el) el.remove();
                });
            })();"""
            )
        except Exception:
            pass
