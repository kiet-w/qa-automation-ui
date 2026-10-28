"""
core/sketch_annotator.py - Visual Defect Precision Engine for Playwright.

Provides non-destructive, real-time SVG and DOM visual annotations:
1. Live Step HUD: Floating top status bar burned into video recordings showing current step with glassmorphism.
2. Action Spotlight: High-contrast radar pulse and action pill (Click, Type) when interacting with elements.
3. Defect Precision Framing:
   - Content-Aware Bounding Box: Accurately wraps inner error text/children instead of arbitrary wide block divs.
   - Zero Text Obstruction: 100% transparent fill ('fill="none"') preserving native text contrast and readability.
   - Spotlight Mask: Page-wide translucent backdrop dimming with a clear cutout hole for the defect.
   - Reticle Frame: High-contrast glowing red border (#ef4444) with HUD corner brackets.
   - Smart Badge & Arrow: Positioned strictly outside the bounding box, never cutting through or covering text.
4. 100% Non-Blocking: All overlays use 'pointer-events: none' to preserve native Playwright interactions.
"""

from typing import Optional, Union
from playwright.sync_api import Locator, Page


class SketchAnnotator:
    """Injects high-precision visual defect frames, step HUDs, and action spotlights into the browser."""

    @staticmethod
    def show_step_hud(page: Optional[Page], step_title: str, step_index: int = 1) -> None:
        """
        Renders a sleek, floating glassmorphism HUD bar at the top of the browser.
        Captured in Playwright WebM video recordings so viewers can track test execution in real time.
        """
        if not page:
            return
        try:
            if page.is_closed():
                return

            clean_title = (step_title or "").strip()
            data = {
                "step_index": int(step_index),
                "title": clean_title[:100] if clean_title else "Execution Step",
            }

            page.evaluate(
                r"""(data) => {
                let hud = document.getElementById('__qa_sketch_step_hud__');
                if (!hud) {
                    hud = document.createElement('div');
                    hud.id = '__qa_sketch_step_hud__';
                    hud.style.position = 'fixed';
                    hud.style.top = '12px';
                    hud.style.left = '50%';
                    hud.style.transform = 'translateX(-50%)';
                    hud.style.zIndex = '2147483646';
                    hud.style.pointerEvents = 'none';
                    hud.style.userSelect = 'none';
                    hud.style.transition = 'all 0.25s cubic-bezier(0.16, 1, 0.3, 1)';
                    const mountHud = (el) => {
                        const target = document.body || document.documentElement;
                        if (target && !document.getElementById('__qa_sketch_step_hud__')) {
                            target.appendChild(el);
                        }
                    };
                    if (document.body || document.documentElement) {
                        mountHud(hud);
                    } else {
                        document.addEventListener('DOMContentLoaded', () => mountHud(hud));
                    }
                }

                // Inject animation keyframes if not present
                if (!document.getElementById('__qa_sketch_hud_styles__')) {
                    const style = document.createElement('style');
                    style.id = '__qa_sketch_hud_styles__';
                    style.textContent = `
                        @keyframes qa_hud_pulse {
                            0% { transform: scale(0.95); opacity: 0.9; }
                            50% { transform: scale(1.6); opacity: 0; }
                            100% { transform: scale(0.95); opacity: 0; }
                        }
                    `;
                    const targetHead = document.head || document.documentElement;
                    if (targetHead) {
                        targetHead.appendChild(style);
                    }
                }

                hud.innerHTML = `
                    <div style="
                        display: inline-flex;
                        align-items: center;
                        gap: 10px;
                        background: rgba(15, 23, 42, 0.96);
                        backdrop-filter: blur(16px);
                        -webkit-backdrop-filter: blur(16px);
                        border: 1.5px solid rgba(56, 189, 248, 0.55);
                        border-radius: 9999px;
                        padding: 6px 18px 6px 10px;
                        box-shadow: 0 12px 28px -4px rgba(0, 0, 0, 0.65), 0 0 16px rgba(56, 189, 248, 0.25);
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    ">
                        <span style="
                            background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
                            color: #ffffff;
                            font-size: 11px;
                            font-weight: 800;
                            padding: 3px 10px;
                            border-radius: 9999px;
                            letter-spacing: 0.5px;
                            text-transform: uppercase;
                            box-shadow: 0 2px 8px rgba(2, 132, 199, 0.5);
                            white-space: nowrap;
                        ">STEP ${data.step_index}</span>
                        <span style="
                            color: #f8fafc;
                            font-size: 12.5px;
                            font-weight: 600;
                            max-width: 60vw;
                            white-space: nowrap;
                            overflow: hidden;
                            text-overflow: ellipsis;
                            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.7);
                        ">${data.title}</span>
                        <span style="position:relative;display:inline-flex;align-items:center;justify-content:center;width:10px;height:10px;margin-left:2px;">
                            <span style="position:absolute;width:100%;height:100%;border-radius:50%;background:#4ade80;animation:qa_hud_pulse 1.8s cubic-bezier(0,0,0.2,1) infinite;"></span>
                            <span style="position:relative;width:8px;height:8px;border-radius:50%;background:#22c55e;box-shadow:0 0 8px #22c55e;"></span>
                        </span>
                    </div>
                `;
            }""",
                data,
            )
        except Exception:
            pass

    @staticmethod
    def spotlight_action(
        page: Optional[Page],
        selector_or_locator: Union[str, Locator],
        action_type: str = "click",
        label: str = "",
    ) -> None:
        """
        Briefly flashes an animated radar ripple and action pill over the target element.
        Creates an intuitive visual trace in recorded video without blocking DOM interaction.
        """
        if not page:
            return
        try:
            if page.is_closed():
                return
            loc = selector_or_locator
            if isinstance(loc, str):
                loc = page.locator(loc)
            target = loc.first if hasattr(loc, "first") else loc
            if not target.is_visible(timeout=500):
                return

            clean_label = (label or "").strip()[:40]
            action_icon = "👆" if action_type == "click" else "✏️"
            action_text = f"{action_icon} {action_type.upper()}"
            if clean_label:
                action_text += f': "{clean_label}"'

            data = {
                "action_text": action_text,
            }

            target.evaluate(
                r"""(el, data) => {
                const rect = el.getBoundingClientRect();
                const containerId = '__qa_sketch_action_overlay__';
                let overlay = document.getElementById(containerId);
                if (overlay) overlay.remove();

                overlay = document.createElement('div');
                overlay.id = containerId;
                overlay.style.position = 'absolute';
                overlay.style.pointerEvents = 'none';
                overlay.style.userSelect = 'none';
                overlay.style.zIndex = '2147483645';
                overlay.style.top = (window.scrollY + rect.top) + 'px';
                overlay.style.left = (window.scrollX + rect.left) + 'px';
                overlay.style.width = rect.width + 'px';
                overlay.style.height = rect.height + 'px';

                const isNearTop = (rect.top < 40);
                const pillPosition = isNearTop
                    ? 'top: calc(100% + 6px); bottom: auto;'
                    : 'bottom: calc(100% + 6px); top: auto;';

                overlay.innerHTML = `
                    <style>
                        @keyframes qa_radar_pulse {
                            0% { transform: scale(0.96); opacity: 0.95; box-shadow: 0 0 0 0 rgba(14, 165, 233, 0.8), inset 0 0 8px rgba(14, 165, 233, 0.4); }
                            70% { transform: scale(1.03); opacity: 0.6; box-shadow: 0 0 0 14px rgba(14, 165, 233, 0), inset 0 0 12px rgba(14, 165, 233, 0); }
                            100% { transform: scale(1); opacity: 0; box-shadow: 0 0 0 0 rgba(14, 165, 233, 0), inset 0 0 0 rgba(14, 165, 233, 0); }
                        }
                    </style>
                    <div style="
                        position: absolute;
                        inset: -4px;
                        border: 2.5px solid #0ea5e9;
                        border-radius: 8px;
                        animation: qa_radar_pulse 0.75s ease-out forwards;
                    "></div>
                    <div style="
                        position: absolute;
                        ${pillPosition}
                        left: 0;
                        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
                        border: 1px solid rgba(186, 230, 253, 0.5);
                        color: #ffffff;
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                        font-size: 11.5px;
                        font-weight: 700;
                        padding: 3px 10px;
                        border-radius: 6px;
                        white-space: nowrap;
                        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.4), 0 0 8px rgba(2, 132, 199, 0.4);
                        opacity: 0.98;
                    ">${data.action_text}</div>
                `;

                document.body.appendChild(overlay);
                setTimeout(() => {
                    if (overlay && overlay.parentNode) overlay.remove();
                }, 700);
            }""",
                data,
            )
        except Exception:
            pass

    @staticmethod
    def highlight_action_input(page: Optional[Page], selector_or_locator: Union[str, Locator], value: str = "", action_type: str = "input") -> bool:
        """Delegates to EvidenceAnnotator to highlight input and action elements."""
        try:
            from core.evidence_annotator import EvidenceAnnotator
            return EvidenceAnnotator.highlight_action_input(page, selector_or_locator, value, action_type)
        except Exception:
            return False

    @staticmethod
    def highlight_actual_result(page: Optional[Page], locator_or_selector: Optional[Union[str, Locator]] = None, status: str = "passed", actual_text: Optional[str] = None) -> bool:
        """Delegates to EvidenceAnnotator to highlight actual result elements with green/red status reticle."""
        try:
            from core.evidence_annotator import EvidenceAnnotator
            return EvidenceAnnotator.highlight_actual_result(page, locator_or_selector, status, actual_text)
        except Exception:
            return False

    @staticmethod
    def highlight_defect(
        page: Optional[Page],
        step_title: str,
        error_msg: str,
        hold_ms: int = 2500,
    ) -> None:
        """
        Highlights defective UI elements using Precision Reticle & Spotlight Framing:
        1. Content-Aware Bounding Box: detects wide block elements and wraps inner content tightly.
        2. Zero Text Obstruction: 100% transparent fill inside the box so error text is never tinted or dimmed.
        3. Spotlight Mask: Page-wide subtle backdrop dimming with a clear cutout hole for maximum defect contrast.
        4. Reticle Framing: Crisp glowing red border (#ef4444) with sleek HUD corner brackets.
        5. Smart Badge & Directional Arrow: Positioned strictly outside the bounding box, never crossing over text.
        6. Holds frame for hold_ms (default 2.5s) to guarantee high-fidelity Playwright video capture.
        """
        if not page:
            return
        try:
            if page.is_closed():
                return

            clean_err = error_msg.splitlines()[0] if error_msg else "Assertion / Execution Failure"
            clean_err = clean_err.strip()
            clean_title = (step_title or "").strip()

            eval_payload = {
                "clean_err": clean_err,
                "clean_title": clean_title,
            }

            page.evaluate(
                r"""(payload) => {
                const clean_err = payload.clean_err || "Assertion / Execution Failure";
                const clean_title = payload.clean_title || "";

                // 1. Remove previous overlays
                ['__qa_sketch_defect_svg__', '__qa_sketch_defect_banner__', '__qa_sketch_defect_badge__'].forEach(id => {
                    const el = document.getElementById(id);
                    if (el) el.remove();
                });

                // 2. Inject Top Diagnostic Evidence Banner
                const banner = document.createElement('div');
                banner.id = '__qa_sketch_defect_banner__';
                banner.style.position = 'fixed';
                banner.style.top = '0';
                banner.style.left = '0';
                banner.style.right = '0';
                banner.style.zIndex = '2147483647';
                banner.style.background = 'linear-gradient(90deg, #991b1b 0%, #dc2626 50%, #991b1b 100%)';
                banner.style.color = '#ffffff';
                banner.style.padding = '8px 24px';
                banner.style.fontFamily = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif';
                banner.style.fontSize = '12.5px';
                banner.style.fontWeight = '700';
                banner.style.display = 'flex';
                banner.style.alignItems = 'center';
                banner.style.justifyContent = 'space-between';
                banner.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.5), 0 0 15px rgba(220, 38, 38, 0.5)';
                banner.style.borderBottom = '2px solid rgba(254, 202, 202, 0.65)';
                banner.style.pointerEvents = 'none';
                banner.style.userSelect = 'none';

                banner.innerHTML = `
                    <div style="display:flex;align-items:center;gap:12px;">
                        <span style="background:#ffffff;color:#dc2626;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:900;letter-spacing:0.5px;">DEFECT CAPTURE</span>
                        <span style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:62vw;color:#fef2f2;">${clean_err.slice(0, 140)}</span>
                    </div>
                    <span style="font-size:11.5px;color:#fecaca;font-weight:600;white-space:nowrap;">Step: ${clean_title.slice(0, 45)}</span>
                `;
                (document.body || document.documentElement).appendChild(banner);

                // 3. Smart Defect Element Locator
                const contextText = (clean_title + " " + clean_err).toLowerCase();
                const tokens = [];
                const quoteRegex = /['"]([^'"]+)['"]/g;
                let match;
                while ((match = quoteRegex.exec(clean_title + " " + clean_err)) !== null) {
                    if (match[1].trim() && match[1].trim().length > 1) tokens.push(match[1].trim());
                }

                let targetEl = null;
                let defectDescription = "ASSERTION / EXECUTION FAILURE";

                // Priority A: Validation & Error Containers
                const errorSelectors = [
                    '[role="alert"]',
                    '[role="alertdialog"]',
                    '.toast-error',
                    '.alert-danger',
                    '.alert-error',
                    '.error-box',
                    '.is-invalid',
                    '.error-message',
                    '.field-error',
                    '.invalid-feedback',
                    '[aria-invalid="true"]',
                    ':invalid'
                ];

                for (const sel of errorSelectors) {
                    try {
                        const elements = Array.from(document.querySelectorAll(sel));
                        for (const el of elements) {
                            const r = el.getBoundingClientRect();
                            if (r.width > 0 && r.height > 0 && el.offsetParent !== null) {
                                targetEl = el;
                                const txt = (el.innerText || el.textContent || "").trim();
                                defectDescription = txt ? `DEFECT: ${txt.slice(0, 60)}` : "DEFECT: Validation Failure";
                                break;
                            }
                        }
                        if (targetEl) break;
                    } catch (e) {}
                }

                // Priority B: Error text match in DOM elements (e.g. "Unable to load", "ResourceNotFound")
                if (!targetEl && clean_err) {
                    const words = clean_err.replace(/[^a-zA-Z0-9\s]/g, ' ')
                        .split(/\s+/)
                        .filter(w => w.length >= 5 && !['error', 'failed', 'assert', 'assertion', 'expect', 'expected', 'status'].includes(w.toLowerCase()));

                    if (words.length > 0) {
                        const candidates = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, h6, p, span, div, li, td'));
                        let bestEl = null;
                        let bestScore = 0;
                        for (const el of candidates) {
                            if (el.children.length > 6) continue;
                            const r = el.getBoundingClientRect();
                            if (r.width === 0 || r.height === 0) continue;
                            const t = (el.textContent || "").toLowerCase();
                            let score = 0;
                            for (const w of words) {
                                if (t.includes(w.toLowerCase())) score++;
                            }
                            if (score > bestScore) {
                                bestScore = score;
                                bestEl = el;
                            }
                        }
                        if (bestEl && bestScore >= 1) {
                            targetEl = bestEl;
                            const txt = (bestEl.innerText || bestEl.textContent || "").trim();
                            defectDescription = txt ? `DEFECT: ${txt.slice(0, 60)}` : `DEFECT: ${clean_err.slice(0, 60)}`;
                        }
                    }
                }

                // Priority C: Form inputs containing tested value
                if (!targetEl) {
                    const allInputs = Array.from(document.querySelectorAll('input, textarea, select'));
                    for (const input of allInputs) {
                        const val = (input.value || "").trim();
                        if (!val) continue;
                        for (const tok of tokens) {
                            if (val === tok || val.includes(tok) || tok.includes(val)) {
                                targetEl = input;
                                defectDescription = `DEFECT: Value "${val.slice(0, 30)}" accepted without validation`;
                                break;
                            }
                        }
                        if (targetEl) break;
                    }
                }

                // Priority D: Semantic Field Selectors
                if (!targetEl) {
                    let semanticSelector = null;
                    if (/phone|mobile|prefix|7/.test(contextText)) {
                        semanticSelector = "input[name='phoneNumber'], input[type='tel'], input[name*='phone' i], input[name*='mobile' i]";
                        defectDescription = "DEFECT: Invalid Mobile Phone Number";
                    } else if (/email|mail/.test(contextText)) {
                        semanticSelector = "input[name='email'], input[type='email'], input[name*='email' i]";
                        defectDescription = "DEFECT: Invalid Email Address";
                    } else if (/postal|zip/.test(contextText)) {
                        semanticSelector = "input[name*='postal' i], input[name*='zip' i]";
                        defectDescription = "DEFECT: Postal Code";
                    } else if (/street|address/.test(contextText)) {
                        semanticSelector = "input[name*='street' i], input[name*='address' i]";
                        defectDescription = "DEFECT: Street Address";
                    } else if (/block/.test(contextText)) {
                        semanticSelector = "input[name*='block' i]";
                        defectDescription = "DEFECT: Block Number";
                    } else if (/nric/.test(contextText)) {
                        semanticSelector = "[data-testid='nric'], input[name*='nric' i]";
                        defectDescription = "DEFECT: NRIC Identity Field";
                    }

                    if (semanticSelector) {
                        const found = document.querySelector(semanticSelector);
                        if (found) {
                            targetEl = found;
                            const val = (targetEl.value || "").trim();
                            if (val) defectDescription = `DEFECT: Value "${val.slice(0, 30)}" accepted without validation`;
                        }
                    }
                }

                // Priority E: Active element or main container fallback
                if (!targetEl && document.activeElement && document.activeElement !== document.body) {
                    const tag = document.activeElement.tagName.toLowerCase();
                    if (['input', 'textarea', 'select', 'button'].includes(tag)) {
                        targetEl = document.activeElement;
                        defectDescription = "DEFECT: Active Element Failure";
                    }
                }

                if (!targetEl) {
                    targetEl = document.querySelector('main, [role="main"], #root > div, body > div');
                    defectDescription = clean_err ? `DEFECT: ${clean_err.slice(0, 60)}` : "DEFECT: Assertion Failure";
                }

                if (!targetEl) return;

                // Dismiss blocking modal if obscuring target
                const modalDialog = document.querySelector('div[role="alertdialog"], [aria-modal="true"], .modal');
                if (modalDialog && targetEl && !modalDialog.contains(targetEl)) {
                    modalDialog.style.display = 'none';
                    document.querySelectorAll('.fixed.inset-0, [class*="backdrop" i]').forEach(b => b.style.display = 'none');
                }

                try {
                    targetEl.scrollIntoView({ behavior: 'instant', block: 'center' });
                } catch (e) {}

                // 4. Content-Aware Bounding Box Calculation
                const rawRect = targetEl.getBoundingClientRect();
                const isFormInput = ['INPUT', 'TEXTAREA', 'SELECT'].includes(targetEl.tagName);
                const isWideBlock = !isFormInput && (rawRect.width > 550 || rawRect.width > window.innerWidth * 0.75);

                let contentLeft = rawRect.left;
                let contentTop = rawRect.top;
                let contentRight = rawRect.right;
                let contentBottom = rawRect.bottom;

                if (isWideBlock) {
                    let tLeft = Infinity, tTop = Infinity, tRight = -Infinity, tBottom = -Infinity;
                    let foundInnerContent = false;

                    // A. Check Range over text nodes
                    try {
                        const range = document.createRange();
                        range.selectNodeContents(targetEl);
                        const rects = range.getClientRects();
                        for (let i = 0; i < rects.length; i++) {
                            const r = rects[i];
                            if (r.width > 4 && r.height > 4) {
                                tLeft = Math.min(tLeft, r.left);
                                tTop = Math.min(tTop, r.top);
                                tRight = Math.max(tRight, r.right);
                                tBottom = Math.max(tBottom, r.bottom);
                                foundInnerContent = true;
                            }
                        }
                    } catch (e) {}

                    // B. Check visible child elements (buttons, svg icons, spans, p, headings, alerts)
                    const descendants = targetEl.querySelectorAll('button, svg, p, span, h1, h2, h3, h4, h5, h6, [role="alert"], a, input, select');
                    for (const child of descendants) {
                        const cr = child.getBoundingClientRect();
                        if (cr.width > 4 && cr.height > 4 && cr.width < rawRect.width * 0.98) {
                            tLeft = Math.min(tLeft, cr.left);
                            tTop = Math.min(tTop, cr.top);
                            tRight = Math.max(tRight, cr.right);
                            tBottom = Math.max(tBottom, cr.bottom);
                            foundInnerContent = true;
                        }
                    }

                    if (foundInnerContent && tRight > tLeft && tBottom > tTop) {
                        const padX = 14;
                        const padY = 10;
                        contentLeft = Math.max(rawRect.left, tLeft - padX);
                        contentRight = Math.min(rawRect.right, tRight + padX);
                        contentTop = Math.max(rawRect.top, tTop - padY);
                        contentBottom = Math.min(rawRect.bottom, tBottom + padY);
                    }
                }

                const scrollX = window.scrollX;
                const scrollY = window.scrollY;

                const boxX = scrollX + contentLeft;
                const boxY = scrollY + contentTop;
                const boxW = Math.max(40, contentRight - contentLeft);
                const boxH = Math.max(24, contentBottom - contentTop);

                const docW = Math.max(document.documentElement.scrollWidth, document.body.scrollWidth, window.innerWidth);
                const docH = Math.max(document.documentElement.scrollHeight, document.body.scrollHeight, window.innerHeight);

                // 5. Smart Defect Badge & Directional Arrow Positioning
                const topBannerHeight = 44;
                const isNearTop = (contentTop < topBannerHeight + 60);

                const badgeH = 34;
                let badgeY = isNearTop ? (boxY + boxH + 16) : Math.max(topBannerHeight + 8, boxY - badgeH - 14);
                let badgeX = Math.max(16, Math.min(boxX, window.innerWidth - 440));

                let arrowStartX, arrowStartY, arrowEndX, arrowEndY, ctrlX, ctrlY;

                if (isNearTop) {
                    // Badge is BELOW the box -> Arrow starts at top of badge, points to bottom border of box
                    arrowStartX = badgeX + 36;
                    arrowStartY = badgeY;
                    arrowEndX = Math.min(boxX + 28, boxX + boxW / 2);
                    arrowEndY = boxY + boxH + 4;
                    ctrlX = arrowStartX - 14;
                    ctrlY = (arrowStartY + arrowEndY) / 2;
                } else {
                    // Badge is ABOVE the box -> Arrow starts at bottom of badge, points to top border of box
                    arrowStartX = badgeX + 36;
                    arrowStartY = badgeY + badgeH;
                    arrowEndX = Math.min(boxX + 28, boxX + boxW / 2);
                    arrowEndY = boxY - 4;
                    ctrlX = arrowStartX - 14;
                    ctrlY = (arrowStartY + arrowEndY) / 2;
                }

                const arrowPathD = `M ${arrowStartX} ${arrowStartY} Q ${ctrlX} ${ctrlY} ${arrowEndX} ${arrowEndY}`;
                const rLen = Math.min(14, Math.floor(boxW / 3), Math.floor(boxH / 3));

                // 6. SVG Reticle Overlay with Spotlight Mask Cutout
                const svgNS = "http://www.w3.org/2000/svg";
                const svg = document.createElementNS(svgNS, "svg");
                svg.id = '__qa_sketch_defect_svg__';
                svg.setAttribute("width", docW + "px");
                svg.setAttribute("height", docH + "px");
                svg.style.position = "absolute";
                svg.style.top = "0";
                svg.style.left = "0";
                svg.style.pointerEvents = "none";
                svg.style.zIndex = "2147483646";

                svg.innerHTML = `
                    <defs>
                        <marker id="qa-sketch-arrowhead" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                            <path d="M 0 1.5 L 9 5 L 0 8.5 z" fill="#ef4444" />
                        </marker>
                        <filter id="qa-sketch-glow" x="-20%" y="-20%" width="140%" height="140%">
                            <feDropShadow dx="0" dy="0" stdDeviation="3.5" flood-color="#ef4444" flood-opacity="0.9"/>
                            <feDropShadow dx="0" dy="2" stdDeviation="6" flood-color="#dc2626" flood-opacity="0.5"/>
                        </filter>
                        <mask id="qa-spotlight-mask">
                            <rect x="0" y="0" width="100%" height="100%" fill="white" />
                            <rect x="${boxX - 6}" y="${boxY - 6}" width="${boxW + 12}" height="${boxH + 12}" rx="10" ry="10" fill="black" />
                        </mask>
                    </defs>

                    <!-- 1. Spotlight Dimming Mask: Dims page around target, leaving target in crystal-clear spotlight hole -->
                    <rect x="0" y="0" width="100%" height="100%" fill="rgba(15, 23, 42, 0.42)" mask="url(#qa-spotlight-mask)" />

                    <!-- 2. Zero-Obstruction High-Contrast Bounding Rect (fill='none' is 100% transparent!) -->
                    <rect x="${boxX - 4}" y="${boxY - 4}" width="${boxW + 8}" height="${boxH + 8}" rx="8" ry="8"
                          fill="none" stroke="#ef4444" stroke-width="3" filter="url(#qa-sketch-glow)" />

                    <!-- 3. Sleek Reticle / HUD Corner Accents -->
                    <!-- Top-Left -->
                    <path d="M ${boxX - 4} ${boxY + rLen} L ${boxX - 4} ${boxY - 4} L ${boxX + rLen} ${boxY - 4}"
                          fill="none" stroke="#ffffff" stroke-width="2.5" stroke-linecap="round" />
                    <!-- Top-Right -->
                    <path d="M ${boxX + boxW + 4 - rLen} ${boxY - 4} L ${boxX + boxW + 4} ${boxY - 4} L ${boxX + boxW + 4} ${boxY + rLen}"
                          fill="none" stroke="#ffffff" stroke-width="2.5" stroke-linecap="round" />
                    <!-- Bottom-Left -->
                    <path d="M ${boxX - 4} ${boxY + boxH + 4 - rLen} L ${boxX - 4} ${boxY + boxH + 4} L ${boxX + rLen} ${boxY + boxH + 4}"
                          fill="none" stroke="#ffffff" stroke-width="2.5" stroke-linecap="round" />
                    <!-- Bottom-Right -->
                    <path d="M ${boxX + boxW + 4 - rLen} ${boxY + boxH + 4} L ${boxX + boxW + 4} ${boxY + boxH + 4} L ${boxX + boxW + 4} ${boxY + boxH + 4 - rLen}"
                          fill="none" stroke="#ffffff" stroke-width="2.5" stroke-linecap="round" />

                    <!-- 4. Directional Pointer Arrow (Points cleanly to outer edge of box, NEVER crossing text) -->
                    <path d="${arrowPathD}" fill="none" stroke="#ef4444" stroke-width="2.5" stroke-linecap="round"
                          marker-end="url(#qa-sketch-arrowhead)" filter="url(#qa-sketch-glow)" />
                `;
                (document.body || document.documentElement).appendChild(svg);

                // 7. High-Contrast Floating Defect Badge
                let badge = document.getElementById('__qa_sketch_defect_badge__');
                if (!badge) {
                    badge = document.createElement('div');
                    badge.id = '__qa_sketch_defect_badge__';
                    badge.style.position = 'absolute';
                    badge.style.zIndex = '2147483647';
                    badge.style.pointerEvents = 'none';
                    badge.style.userSelect = 'none';
                    (document.body || document.documentElement).appendChild(badge);
                }

                badge.style.top = badgeY + 'px';
                badge.style.left = badgeX + 'px';

                const displayDesc = defectDescription.replace(/^DEFECT:\s*/i, '');
                badge.innerHTML = `
                    <div style="
                        background: linear-gradient(135deg, #1e1e2e 0%, #11111b 100%);
                        border: 1.5px solid #ef4444;
                        border-radius: 8px;
                        padding: 5px 12px;
                        display: inline-flex;
                        align-items: center;
                        gap: 8px;
                        box-shadow: 0 12px 28px -4px rgba(0, 0, 0, 0.7), 0 0 16px rgba(239, 68, 68, 0.4);
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                        color: #ffffff;
                        white-space: nowrap;
                        max-width: 80vw;
                    ">
                        <span style="
                            background: #ef4444;
                            color: #ffffff;
                            font-size: 11px;
                            font-weight: 800;
                            padding: 3px 8px;
                            border-radius: 5px;
                            letter-spacing: 0.5px;
                            text-transform: uppercase;
                            display: inline-flex;
                            align-items: center;
                            gap: 4px;
                            box-shadow: 0 2px 6px rgba(239, 68, 68, 0.4);
                        ">
                            <span>🎯</span>
                            <span>DEFECT</span>
                        </span>
                        <span style="
                            font-size: 12px;
                            font-weight: 600;
                            color: #fca5a5;
                            overflow: hidden;
                            text-overflow: ellipsis;
                            max-width: 55vw;
                        ">${displayDesc}</span>
                    </div>
                `;

                // 8. Force layout calculation and browser compositor repaint tick
                const bRef = document.body || document.documentElement;
                if (bRef) void bRef.offsetHeight;
                requestAnimationFrame(() => {
                    const rRef = document.body || document.documentElement;
                    if (rRef) void rRef.offsetHeight;
                });
            }""",
                eval_payload,
            )
            page.wait_for_timeout(hold_ms)
        except Exception:
            pass

    @staticmethod
    def clear_overlays(page: Optional[Page]) -> None:
        """Removes all active sketch overlays, HUDs, and badges."""
        if not page:
            return
        try:
            if page.is_closed():
                return
            page.evaluate(
                r"""(() => {
                const ids = [
                    '__qa_sketch_step_hud__',
                    '__qa_sketch_action_overlay__',
                    '__qa_sketch_defect_svg__',
                    '__qa_sketch_defect_banner__',
                    '__qa_sketch_defect_badge__',
                    '__qa_evidence_action_overlay__',
                    '__qa_evidence_actual_overlay__'
                ];
                ids.forEach(id => {
                    const el = document.getElementById(id);
                    if (el) el.remove();
                });
            })();"""
            )
        except Exception:
            pass
