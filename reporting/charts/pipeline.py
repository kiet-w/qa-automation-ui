"""
reporting/charts/pipeline.py - Interactive Horizontal SVG Step Pipeline.
"""

import html
from typing import Any, Dict, List


def generate_pipeline_svg(steps: List[Dict[str, Any]], test_idx: int = 0) -> str:
    """
    Generates a Pure SVG Interactive Horizontal Flow Pipeline for execution steps.
    - Status-colored nodes: Green (#10b981) for passed, Red (#ef4444) for failed, Slate (#94a3b8) for skipped.
    - Connecting flow lines between consecutive nodes.
    - Interactive click navigation: seeks the video recording to step start time and scrolls to video container.
    - Real-time highlight synchronization with video playback.
    """
    n = len(steps)
    if n == 0:
        return '<div class="no-steps-hint" style="color: var(--text-secondary, #8b949e);" data-i18n="no_steps">No detailed steps recorded.</div>'

    total_width = max(880, n * 170)
    height = 145
    margin_x = 80
    usable_width = total_width - 2 * margin_x
    step_gap = usable_width / (n - 1) if n > 1 else 0

    svg_parts = [
        '<div class="pipeline-scroll-wrapper">',
        f'<svg viewBox="0 0 {total_width} {height}" class="pipeline-svg" width="{total_width}" height="{height}" xmlns="http://www.w3.org/2000/svg">',
        '  <defs>',
        '    <filter id="node-glow" x="-20%" y="-20%" width="140%" height="140%">',
        '      <feDropShadow dx="0" dy="1" stdDeviation="2" flood-color="#000000" flood-opacity="0.25"/>',
        '    </filter>',
        '    <filter id="active-pulse-glow" x="-30%" y="-30%" width="160%" height="160%">',
        '      <feDropShadow dx="0" dy="0" stdDeviation="3" flood-color="#3fb950" flood-opacity="0.4"/>',
        '    </filter>',
        '  </defs>',
    ]

    # Connector lines
    for i in range(n - 1):
        x1 = margin_x + i * step_gap
        x2 = margin_x + (i + 1) * step_gap
        y = 44

        curr_status = steps[i].get("status", "passed").lower()
        next_status = steps[i + 1].get("status", "passed").lower()

        if curr_status == "passed" and next_status == "passed":
            line_color = "var(--status-pass, #3fb950)"
            dash = ""
        elif "failed" in (curr_status, next_status):
            line_color = "var(--status-fail, #f85149)"
            dash = 'stroke-dasharray="6,4"'
        elif "skipped" in (curr_status, next_status):
            line_color = "var(--status-skip, #d29922)"
            dash = 'stroke-dasharray="4,4"'
        else:
            line_color = "var(--border-color, #30363d)"
            dash = 'stroke-dasharray="4,4"'

        svg_parts.append(
            f'  <line x1="{x1 + 22:.1f}" y1="{y}" x2="{x2 - 22:.1f}" y2="{y}" stroke="{line_color}" stroke-width="3.5" stroke-linecap="round" {dash}/>'
        )

    # Nodes and step labels
    for i, step in enumerate(steps):
        x = margin_x + i * step_gap if n > 1 else total_width / 2
        y = 44
        status = step.get("status", "passed").lower()
        raw_title = step.get("title", f"Step {i + 1}")
        duration = float(step.get("duration", 0.0))
        start_time = float(step.get("start_time", 0.0))
        end_time = float(step.get("end_time", start_time + duration))

        short_title = raw_title
        if ":" in raw_title:
            short_title = raw_title.split(":", 1)[1].strip()
        if len(short_title) > 22:
            short_title = short_title[:20] + "…"

        node_id = f"pipeline-node-{test_idx}-{i}"
        card_target_id = f"step-card-{test_idx}-{i}"

        if status == "passed":
            fill_color = "var(--status-pass, #3fb950)"
            icon_svg = (
                f'<path d="M {x - 6:.1f} {y:.1f} L {x - 1:.1f} {y + 5:.1f} L {x + 7:.1f} {y - 4:.1f}" '
                f'fill="none" stroke="#ffffff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>'
            )
        elif status == "failed":
            fill_color = "var(--status-fail, #f85149)"
            icon_svg = (
                f'<path d="M {x - 5:.1f} {y - 5:.1f} L {x + 5:.1f} {y + 5:.1f} M {x + 5:.1f} {y - 5:.1f} L {x - 5:.1f} {y + 5:.1f}" '
                f'fill="none" stroke="#ffffff" stroke-width="2.6" stroke-linecap="round"/>'
            )
        else:
            fill_color = "var(--status-skip, #d29922)"
            icon_svg = (
                f'<line x1="{x - 5:.1f}" y1="{y:.1f}" x2="{x + 5:.1f}" y2="{y:.1f}" stroke="#ffffff" stroke-width="2.6" stroke-linecap="round"/>'
            )

        step_num_text = f"Step {i + 1}"
        node_tooltip = f"Step {i + 1}: {html.escape(raw_title)} • {start_time:.1f}s-{end_time:.1f}s ({duration:.2f}s) • Click to seek video"

        svg_parts.extend([
            f'  <g id="{node_id}" class="pipeline-node" '
            f'data-test-idx="{test_idx}" data-step-idx="{i}" '
            f'data-start="{start_time:.2f}" data-end="{end_time:.2f}" '
            f'onclick="seekVideoAndScroll({start_time:.2f}, \'{card_target_id}\', {test_idx}, {i})" '
            f'role="button" tabindex="0" title="{node_tooltip}">',
            f'    <!-- Outer halo & active pulse circle -->',
            f'    <circle class="pipeline-node-halo" cx="{x:.1f}" cy="{y}" r="26" fill="rgba(148, 163, 184, 0.08)" stroke="{fill_color}" stroke-width="2" opacity="0.9"/>',
            f'    <circle class="pipeline-node-core" cx="{x:.1f}" cy="{y}" r="19" fill="{fill_color}"/>',
            f'    {icon_svg}',
            f'    <!-- Step Number Header -->',
            f'    <text x="{x:.1f}" y="{y + 40}" text-anchor="middle" font-size="12" font-weight="700" fill="var(--text-primary, #e6edf3)" class="chart-text-main" font-family="system-ui, -apple-system, sans-serif">{step_num_text}</text>',
            f'    <!-- Step Short Description -->',
            f'    <text x="{x:.1f}" y="{y + 56}" text-anchor="middle" font-size="10.5" font-weight="500" fill="var(--text-secondary, #8b949e)" class="chart-text-sub" font-family="system-ui, -apple-system, sans-serif">{html.escape(short_title)}</text>',
            f'    <!-- Duration and seek timing pill -->',
            f'    <rect x="{x - 32:.1f}" y="{y + 64}" width="64" height="18" rx="9" fill="rgba(148, 163, 184, 0.08)" stroke="var(--border-color, #30363d)" stroke-width="1"/>',
            f'    <text x="{x:.1f}" y="{y + 76}" text-anchor="middle" font-size="9" font-weight="700" fill="var(--text-secondary, #8b949e)" font-family="monospace">▶ {start_time:.1f}s ({duration:.1f}s)</text>',
            '  </g>',
        ])

    svg_parts.extend([
        '</svg>',
        '</div>',
    ])
    return "\n".join(svg_parts)
